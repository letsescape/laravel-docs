#!/usr/bin/env python3
"""고정 upstream commit의 Laravel 영어 원문 cache 동기화.

지원 버전별 branch tip을 한 번 조회해 canonical manifest로 고정하고, 이후
모든 checkout은 manifest의 commit 객체 ID만 사용. 원문 Markdown은 byte를
정규화하지 않고 ``i18n/en/docusaurus-plugin-content-docs/version-<v>/``에
복사하며, 전체 동기화에서는 upstream에 없는 기존 cache 파일을 삭제.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import stat
import subprocess
import sys
import tempfile
import time
import unicodedata
from pathlib import Path

from ..common.files import atomic_write_bytes, unlink_file
from ..common.versions import load_versions
from ..runtime.process import ProcessTreeError, run_process_tree

REPO_ROOT = Path(__file__).resolve().parents[3]
UPSTREAM_REPO = "https://github.com/laravel/docs.git"
EN_ROOT = REPO_ROOT / "i18n" / "en" / "docusaurus-plugin-content-docs"
MANIFEST_ENV = "TRANSLATION_UPSTREAM_MANIFEST"
MANIFEST_DIGEST_ENV = "TRANSLATION_UPSTREAM_MANIFEST_DIGEST"
WORKFLOW_DEADLINE_ENV = "TRANSLATION_WORKFLOW_DEADLINE_MONOTONIC"
UPSTREAM_FETCH_TIMEOUT = 300
UPSTREAM_REF_QUERY_TIMEOUT = 30
_COMMIT_RE = {
    "sha1": re.compile(r"^[0-9a-f]{40}$"),
    "sha256": re.compile(r"^[0-9a-f]{64}$"),
}
_VERSION_RE = re.compile(r"^(?:master|(?:0|[1-9]\d*)\.x)$")
_MANIFEST_TOP_LEVEL_KEYS = ("schema_version", "entries")
_MANIFEST_ENTRY_KEYS = ("version", "repository", "object_format", "commit")
_GIT_PASSTHROUGH_ENV = {
    "ALL_PROXY",
    "GIT_SSL_CAINFO",
    "HTTPS_PROXY",
    "HTTP_PROXY",
    "LANG",
    "LC_ALL",
    "NO_PROXY",
    "PATH",
    "SSL_CERT_DIR",
    "SSL_CERT_FILE",
    "SYSTEMROOT",
    "all_proxy",
    "https_proxy",
    "http_proxy",
    "no_proxy",
}
_PROCESS_RUNNER = run_process_tree


def supported_versions() -> list[str]:
    """versions.json을 단일 출처로 사용하는 지원 버전 목록."""
    return load_versions(REPO_ROOT / "versions.json")


def _git_environment() -> dict[str, str]:
    """자격 증명과 사용자 설정을 제거한 upstream Git 환경 구성."""

    env = {
        key: value
        for key, value in os.environ.items()
        if key in _GIT_PASSTHROUGH_ENV or key.startswith("LC_")
    }
    env.update(
        {
            "HOME": os.devnull,
            "XDG_CONFIG_HOME": os.devnull,
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
        }
    )
    return env


def _run(
    args: list[str],
    cwd: Path | None = None,
    quiet: bool = False,
    timeout: float | None = None,
) -> None:
    """격리된 환경에서 upstream Git argv 실행."""

    _PROCESS_RUNNER(
        args,
        cwd=cwd,
        env=_git_environment(),
        check=True,
        timeout=timeout,
        stdout=subprocess.DEVNULL if quiet else None,
        stderr=subprocess.DEVNULL if quiet else None,
    )


def _output(
    args: list[str],
    cwd: Path,
    *,
    strip: bool = True,
    timeout: float | None = None,
) -> str:
    """격리된 환경에서 Git argv를 실행하고 표준 출력 반환."""

    output = _PROCESS_RUNNER(
        args,
        cwd=cwd,
        env=_git_environment(),
        check=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    ).stdout
    return output.strip() if strip else output


def _remaining_timeout(
    deadline: float | None,
    *,
    cap: float | None = None,
) -> float | None:
    """공유 기한과 단계 상한 중 짧은 timeout 계산."""

    if deadline is None:
        return cap
    if not math.isfinite(deadline) or deadline <= 0:
        raise ValueError("invalid workflow deadline")
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise subprocess.TimeoutExpired(["workflow-deadline"], 0)
    return min(remaining, cap) if cap is not None else remaining


def _environment_deadline() -> float | None:
    """환경 변수의 단조 시계 워크플로 기한 검증 및 반환."""

    raw_deadline = os.environ.get(WORKFLOW_DEADLINE_ENV)
    if raw_deadline is None:
        return None
    try:
        deadline = float(raw_deadline)
    except ValueError as exc:
        raise ValueError("invalid workflow deadline") from exc
    _remaining_timeout(deadline)
    return deadline


def _prepare_upstream(
    repo_dir: Path,
    refs: dict[str, str],
    *,
    doc: str | None = None,
    deadline: float | None = None,
) -> None:
    """고정 commit만 포함하는 sparse upstream 저장소 준비."""

    if not refs:
        raise ValueError("upstream source refs must not be empty")
    refspecs: list[str] = []
    local_refs: dict[str, str] = {}
    object_formats: set[str] = set()
    for version, commit in refs.items():
        if not isinstance(version, str) or not _VERSION_RE.fullmatch(version):
            raise ValueError(f"invalid version: {version!r}")
        object_formats.add(_object_format(commit))
        local_ref = f"refs/translation-sync/{version}"
        local_refs[version] = local_ref
        refspecs.append(f"{commit}:{local_ref}")
    if len(object_formats) != 1:
        raise ValueError("upstream refs use mixed object formats")
    if doc is not None:
        doc = normalize_document_selector(doc)
        sparse_pattern = (
            "*.md"
            if "\r" in doc or "\n" in doc
            else _literal_sparse_pattern(doc)
        )
    else:
        sparse_pattern = "*.md"

    local_timeout = _remaining_timeout(deadline)
    _run(
        [
            "git",
            "init",
            "--quiet",
            f"--object-format={next(iter(object_formats))}",
            str(repo_dir),
        ],
        quiet=True,
        timeout=local_timeout,
    )
    _run(
        ["git", "remote", "add", "origin", UPSTREAM_REPO],
        cwd=repo_dir,
        quiet=True,
        timeout=_remaining_timeout(deadline),
    )
    for key, value in (
        ("remote.origin.promisor", "true"),
        ("remote.origin.partialclonefilter", "blob:none"),
    ):
        _run(
            ["git", "config", key, value],
            cwd=repo_dir,
            quiet=True,
            timeout=_remaining_timeout(deadline),
        )
    _run(
        [
            "git",
            "sparse-checkout",
            "set",
            "--no-cone",
            "--",
            sparse_pattern,
        ],
        cwd=repo_dir,
        quiet=True,
        timeout=_remaining_timeout(deadline),
    )

    fetch_args = [
        "git",
        "-c",
        "http.version=HTTP/1.1",
        "fetch",
        "--quiet",
        "--depth=1",
        "--filter=blob:none",
        "--no-tags",
        "--atomic",
        "--no-write-fetch-head",
        "--recurse-submodules=no",
        "origin",
        *refspecs,
    ]
    _run(
        fetch_args,
        cwd=repo_dir,
        quiet=True,
        timeout=_remaining_timeout(
            deadline,
            cap=UPSTREAM_FETCH_TIMEOUT,
        ),
    )

    for version, commit in refs.items():
        resolved = _output(
            [
                "git",
                "rev-parse",
                "--verify",
                "--end-of-options",
                f"{local_refs[version]}^{{commit}}",
            ],
            repo_dir,
            timeout=_remaining_timeout(deadline),
        )
        if resolved != commit:
            raise ValueError(f"version-{version}: pinned commit mismatch")


def _manifest_ref_names(versions: list[str]) -> dict[str, str]:
    """지원 버전별 upstream branch ref 이름 구성."""

    if not versions:
        raise ValueError("manifest versions must not be empty")
    ref_names: dict[str, str] = {}
    seen: set[str] = set()
    for version in versions:
        if not isinstance(version, str) or not _VERSION_RE.fullmatch(version):
            raise ValueError(f"invalid manifest version: {version!r}")
        if version in seen:
            raise ValueError(f"duplicate manifest version: {version}")
        seen.add(version)
        ref_names[f"refs/heads/{version}"] = version
    return ref_names


def _literal_sparse_pattern(document: str) -> str:
    """단일 문서 경로를 literal sparse-checkout pattern으로 변환."""

    escaped = "".join(
        f"\\{character}"
        if character in {"\\", "*", "?", "[", "]", " "}
        else character
        for character in document
    )
    return f"/{escaped}"


def _parse_remote_refs(
    output: str,
    expected_refs: dict[str, str],
) -> dict[str, str]:
    """Git protocol v2의 원격 ref 응답을 버전별 commit으로 파싱."""

    if not isinstance(output, str) or not output:
        raise ValueError("invalid upstream ref advertisement")
    commits_by_ref: dict[str, str] = {}
    for line in output.splitlines():
        if line.count("\t") != 1:
            raise ValueError("invalid upstream ref advertisement")
        commit, ref_name = line.split("\t")
        if ref_name not in expected_refs or ref_name in commits_by_ref:
            raise ValueError("invalid upstream ref advertisement")
        _object_format(commit)
        commits_by_ref[ref_name] = commit
    if set(commits_by_ref) != set(expected_refs):
        raise ValueError("upstream ref advertisement is incomplete")
    return {
        version: commits_by_ref[ref_name]
        for ref_name, version in expected_refs.items()
    }


def _query_remote_refs(
    versions: list[str],
    *,
    deadline: float | None = None,
) -> dict[str, str]:
    """단일 원격 조회로 지원 버전 branch commit 수집."""

    expected_refs = _manifest_ref_names(versions)
    args = [
        "git",
        "-c",
        "http.version=HTTP/1.1",
        "ls-remote",
        "--heads",
        "--refs",
        "--exit-code",
        UPSTREAM_REPO,
        *expected_refs,
    ]
    output = _output(
        args,
        REPO_ROOT,
        strip=False,
        timeout=_remaining_timeout(
            deadline,
            cap=UPSTREAM_REF_QUERY_TIMEOUT,
        ),
    )
    return _parse_remote_refs(output, expected_refs)


def _object_format(commit: str) -> str:
    """commit 객체 ID 길이에서 Git object format 판별."""

    if not isinstance(commit, str):
        raise ValueError("manifest commit must be a lowercase full object ID")
    if _COMMIT_RE["sha1"].fullmatch(commit):
        return "sha1"
    if _COMMIT_RE["sha256"].fullmatch(commit):
        return "sha256"
    raise ValueError("manifest commit must be a lowercase full object ID")


def _manifest_payload(refs: dict[str, str]) -> dict[str, object]:
    """버전별 commit mapping을 canonical manifest payload로 변환."""

    entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for version, commit in refs.items():
        if not isinstance(version, str) or not _VERSION_RE.fullmatch(version):
            raise ValueError(f"invalid manifest version: {version!r}")
        if version in seen:
            raise ValueError(f"duplicate manifest version: {version}")
        seen.add(version)
        entries.append(
            {
                "version": version,
                "repository": UPSTREAM_REPO,
                "object_format": _object_format(commit),
                "commit": commit,
            }
        )
    return {"schema_version": 1, "entries": entries}


def canonical_manifest(refs: dict[str, str]) -> bytes:
    """버전별 upstream commit의 canonical manifest bytes 생성."""

    return (
        json.dumps(
            _manifest_payload(refs),
            ensure_ascii=False,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def manifest_digest(contents: bytes) -> str:
    """canonical manifest bytes의 SHA-256 digest 계산."""

    return hashlib.sha256(contents).hexdigest()


def write_manifest(path: Path, refs: dict[str, str]) -> None:
    """canonical manifest를 symlink 비추적 방식으로 원자적 기록."""

    path.parent.mkdir(parents=True, exist_ok=True)
    contents = canonical_manifest(refs)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as stream:
            temporary = Path(stream.name)
            stream.write(contents)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def load_manifest_bytes(
    contents: bytes,
    *,
    expected_versions: list[str] | None = None,
) -> dict[str, str]:
    """canonical manifest bytes 검증 및 버전별 commit 로딩."""

    try:
        payload = json.loads(contents.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid upstream manifest JSON") from exc
    if not isinstance(payload, dict) or tuple(payload) != _MANIFEST_TOP_LEVEL_KEYS:
        raise ValueError("invalid upstream manifest schema")
    if (
        type(payload["schema_version"]) is not int
        or payload["schema_version"] != 1
        or not isinstance(payload["entries"], list)
    ):
        raise ValueError("invalid upstream manifest schema")

    refs: dict[str, str] = {}
    for entry in payload["entries"]:
        if not isinstance(entry, dict) or tuple(entry) != _MANIFEST_ENTRY_KEYS:
            raise ValueError("invalid upstream manifest entry schema")
        version = entry["version"]
        repository = entry["repository"]
        object_format = entry["object_format"]
        commit = entry["commit"]
        if not isinstance(version, str) or not _VERSION_RE.fullmatch(version):
            raise ValueError("invalid upstream manifest version")
        if version in refs:
            raise ValueError(f"duplicate upstream manifest version: {version}")
        if repository != UPSTREAM_REPO:
            raise ValueError("upstream manifest repository mismatch")
        if (
            not isinstance(object_format, str)
            or object_format not in _COMMIT_RE
            or not isinstance(commit, str)
        ):
            raise ValueError("invalid upstream manifest object format")
        if not _COMMIT_RE[object_format].fullmatch(commit):
            raise ValueError("invalid upstream manifest commit")
        refs[version] = commit

    if expected_versions is not None and list(refs) != expected_versions:
        raise ValueError("upstream manifest versions do not match versions.json")
    if contents != canonical_manifest(refs):
        raise ValueError("upstream manifest is not canonical JSON")
    return refs


def load_manifest(
    path: Path,
    *,
    expected_versions: list[str] | None = None,
) -> dict[str, str]:
    """파일에서 canonical upstream manifest 로딩."""

    return load_manifest_bytes(
        path.read_bytes(),
        expected_versions=expected_versions,
    )


def resolve_manifest(
    versions: list[str],
    *,
    deadline: float | None = None,
) -> bytes:
    """원격 branch를 한 번 조회해 고정 upstream manifest 확정."""

    return canonical_manifest(_query_remote_refs(versions, deadline=deadline))


def manifest_ref(refs: dict[str, str], version: str) -> str:
    """manifest에서 요청 버전의 고정 commit 조회."""

    try:
        return refs[version]
    except KeyError as exc:
        raise ValueError(f"upstream manifest missing ref for version-{version}") from exc


def _has_symlink_component(path: Path, *, root: Path) -> bool:
    """root부터 대상까지 경로 구성 요소의 symlink 포함 여부."""

    current = root
    if current.is_symlink():
        return True
    for part in path.relative_to(root).parts:
        current /= part
        if current.is_symlink():
            return True
    return False


def _version_destination(version: str) -> Path:
    """검증된 버전의 영어 원문 cache 디렉터리 반환."""

    if not _VERSION_RE.fullmatch(version):
        raise ValueError(f"invalid version: {version}")
    repo_root = REPO_ROOT.absolute()
    en_root = EN_ROOT.absolute()
    candidate = en_root / f"version-{version}"
    if (
        not en_root.is_relative_to(repo_root)
        or not candidate.is_relative_to(en_root)
        or _has_symlink_component(candidate, root=repo_root)
    ):
        raise ValueError(f"invalid version destination: {version}")
    if not candidate.resolve(strict=False).is_relative_to(repo_root.resolve()):
        raise ValueError(f"invalid version destination: {version}")
    return candidate


def _document_destination(destination: Path, name: str) -> Path:
    """버전 cache 내부의 canonical 문서 대상 경로 검증."""

    repo_root = REPO_ROOT.absolute()
    en_root = EN_ROOT.absolute()
    target = (destination / name).absolute()
    if (
        not target.is_relative_to(destination)
        or not target.is_relative_to(en_root)
        or _has_symlink_component(target, root=repo_root)
        or not target.resolve(strict=False).is_relative_to(repo_root.resolve())
    ):
        raise ValueError(f"invalid document destination: {name}")
    return target


def normalize_document_selector(document: str) -> str:
    """중첩 Markdown 문서 selector를 canonical POSIX 경로로 정규화."""

    if not isinstance(document, str):
        raise ValueError(f"invalid document: {document!r}")
    normalized = unicodedata.normalize("NFC", document)
    if (
        "\\" in normalized
        or "\0" in normalized
        or normalized.startswith("/")
    ):
        raise ValueError(f"invalid document: {document}")
    parts = normalized.split("/")
    if any(part in {"", ".", ".."} for part in parts) or not normalized.endswith(
        ".md"
    ):
        raise ValueError(f"invalid document: {document}")
    return normalized


def _recursive_markdown_files(root: Path, *, exclude_git: bool = False) -> list[Path]:
    """symlink를 거부하며 root 아래 Markdown 파일을 재귀 수집."""

    if root.is_symlink() or (root.exists() and not root.is_dir()):
        raise ValueError(f"upstream Markdown path is unsafe: {root.name}")
    if not root.exists():
        return []

    documents: list[Path] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        entries = sorted(
            directory.iterdir(),
            key=lambda path: path.name.encode("utf-8"),
            reverse=True,
        )
        for path in entries:
            if exclude_git and directory == root and path.name == ".git":
                continue
            if path.is_symlink():
                raise ValueError(
                    "upstream Markdown symlink: "
                    + path.relative_to(root).as_posix()
                )
            if path.is_dir():
                pending.append(path)
                continue
            if path.suffix != ".md":
                continue
            if not path.is_file():
                raise ValueError(
                    "upstream Markdown path is unsafe: "
                    + path.relative_to(root).as_posix()
                )
            relative = path.relative_to(root).as_posix()
            if normalize_document_selector(relative) != relative:
                raise ValueError(
                    f"upstream Markdown path is not canonical: {relative}"
                )
            documents.append(path)
    return sorted(
        documents,
        key=lambda path: path.relative_to(root).as_posix().encode("utf-8"),
    )


def _remove_empty_parents(path: Path, *, stop: Path) -> None:
    """지정 경계까지 비어 있는 상위 디렉터리 제거."""

    current = path
    while current != stop:
        if not current.is_relative_to(stop) or current.is_symlink():
            raise ValueError(f"invalid document destination: {current}")
        try:
            current.rmdir()
        except (FileNotFoundError, OSError):
            return
        current = current.parent


def sync_version(
    repo_dir: Path,
    version: str,
    *,
    ref: str | None = None,
    doc: str | None = None,
    deadline: float | None = None,
) -> int:
    """고정 commit의 단일 버전 원문을 영어 cache에 원자적으로 적재.

    Args:
        version: 적재 대상 문서 버전.
        source_ref: manifest가 고정한 upstream commit 객체 ID.
        document: 선택적으로 적재할 단일 canonical Markdown 경로.
        deadline: 전체 워크플로의 단조 시계 기한.

    Returns:
        영어 cache에 적재하거나 삭제한 Markdown 파일 수.

    Raises:
        ValueError: 버전, commit 또는 문서 selector가 부적합한 경우.
        subprocess.CalledProcessError: upstream Git 명령이 실패한 경우.
        subprocess.TimeoutExpired: 공유 기한을 초과한 경우.
    """
    if doc is not None:
        doc = normalize_document_selector(doc)
    dest = _version_destination(version)
    if doc is not None:
        target = _document_destination(dest, doc)
    else:
        for cached in _recursive_markdown_files(dest):
            _document_destination(dest, cached.relative_to(dest).as_posix())
    checkout_args = ["git", "checkout", "--force", ref or version]
    _run(
        checkout_args,
        cwd=repo_dir,
        quiet=True,
        timeout=_remaining_timeout(
            deadline,
            cap=UPSTREAM_FETCH_TIMEOUT,
        ),
    )
    dest = _version_destination(version)
    dest.mkdir(parents=True, exist_ok=True)
    dest = _version_destination(version)
    if doc is not None:
        target = _document_destination(dest, doc)
    else:
        for cached in _recursive_markdown_files(dest):
            _document_destination(dest, cached.relative_to(dest).as_posix())

    if doc is not None:
        source = repo_dir / doc
        if _has_symlink_component(source, root=repo_dir):
            raise ValueError(f"upstream Markdown symlink: {source.name}")
        try:
            source_mode = source.lstat().st_mode
        except FileNotFoundError:
            unlink_file(target, missing_ok=True)
            _remove_empty_parents(target.parent, stop=dest)
            return 0
        if not stat.S_ISREG(source_mode):
            raise ValueError(f"upstream Markdown path is unsafe: {doc}")
        target.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_bytes(target, source.read_bytes())
        return 1

    sources = _recursive_markdown_files(repo_dir, exclude_git=True)
    for source in sources:
        relative = source.relative_to(repo_dir).as_posix()
        _document_destination(dest, relative)

    count = 0
    for md in sources:
        relative = md.relative_to(repo_dir).as_posix()
        target = _document_destination(dest, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_bytes(
            target,
            md.read_bytes(),
        )
        count += 1

    source_names = {
        source.relative_to(repo_dir).as_posix() for source in sources
    }
    stale_parents: set[Path] = set()
    for stale in _recursive_markdown_files(dest):
        relative = stale.relative_to(dest).as_posix()
        if relative not in source_names:
            unlink_file(stale, missing_ok=True)
            stale_parents.add(stale.parent)
    for parent in sorted(
        stale_parents,
        key=lambda path: len(path.relative_to(dest).parts),
        reverse=True,
    ):
        _remove_empty_parents(parent, stop=dest)
    return count


def main(*, version: str | None = None, doc: str | None = None) -> int:
    """manifest 확정 또는 재사용 후 선택 범위의 원문 동기화.

    Args:
        version: 선택적으로 동기화할 단일 지원 버전.
        doc: ``version`` 내부의 선택적 canonical Markdown 경로.

    Returns:
        성공 시 0, 제어된 입력·manifest·Git 실패 시 1.
    """

    try:
        workflow_deadline = _environment_deadline()
    except ValueError as exc:
        print(f"workflow deadline error: {exc}", file=sys.stderr)
        return 1
    except subprocess.TimeoutExpired:
        print("workflow deadline exceeded", file=sys.stderr)
        return 2
    try:
        manifest_versions = supported_versions()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"versions.json error: {exc}", file=sys.stderr)
        return 1
    selected_versions = manifest_versions
    if doc is not None and version is None:
        print(
            "invalid document filter: --doc requires --version",
            file=sys.stderr,
        )
        return 1
    if version is not None:
        if version not in manifest_versions:
            print(f"unsupported version: {version}", file=sys.stderr)
            return 1
        selected_versions = [version]
    if doc is not None:
        try:
            doc = normalize_document_selector(doc)
        except ValueError:
            print(f"invalid document filter: {doc}", file=sys.stderr)
            return 1

    manifest_value = os.environ.get(MANIFEST_ENV, "").strip()
    manifest_path = Path(manifest_value).resolve() if manifest_value else None
    manifest_contents: bytes | None = None
    try:
        if manifest_path is not None and manifest_path.exists():
            manifest_contents = manifest_path.read_bytes()
            pinned_refs = load_manifest_bytes(
                manifest_contents,
                expected_versions=manifest_versions,
            )
        else:
            pinned_refs = None
        expected_manifest_digest = os.environ.get(
            MANIFEST_DIGEST_ENV,
            "",
        ).strip()
        if expected_manifest_digest and (
            manifest_contents is None
            or manifest_digest(manifest_contents) != expected_manifest_digest
        ):
            raise ValueError("upstream manifest digest mismatch")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"upstream manifest error: {exc}", file=sys.stderr)
        return 1
    generated_manifest = pinned_refs is None
    if pinned_refs is None:
        try:
            manifest_contents = resolve_manifest(
                manifest_versions,
                deadline=workflow_deadline,
            )
            pinned_refs = load_manifest_bytes(
                manifest_contents,
                expected_versions=manifest_versions,
            )
        except ProcessTreeError:
            print("upstream process isolation failed", file=sys.stderr)
            return 2
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            print("upstream ref query failed", file=sys.stderr)
            return 2 if workflow_deadline is not None else 1
        except ValueError as exc:
            print(f"upstream manifest error: {exc}", file=sys.stderr)
            return 1

    try:
        selected_refs = {
            selected_version: manifest_ref(pinned_refs, selected_version)
            for selected_version in selected_versions
        }
    except ValueError as exc:
        print(f"upstream manifest error: {exc}", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        repo_dir = Path(tmp) / "laravel-docs"
        try:
            _prepare_upstream(
                repo_dir,
                selected_refs,
                doc=doc,
                deadline=workflow_deadline,
            )
        except ProcessTreeError:
            print("upstream process isolation failed", file=sys.stderr)
            return 2
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            print("upstream fetch failed", file=sys.stderr)
            return 2 if workflow_deadline is not None else 1
        except ValueError as exc:
            print(exc, file=sys.stderr)
            return 1

        total = 0
        for selected_version in selected_versions:
            try:
                ref = manifest_ref(pinned_refs, selected_version)
                sync_kwargs: dict[str, object] = {
                    "ref": ref,
                    "doc": doc,
                }
                if workflow_deadline is not None:
                    sync_kwargs["deadline"] = workflow_deadline
                n = sync_version(
                    repo_dir,
                    selected_version,
                    **sync_kwargs,
                )
            except subprocess.TimeoutExpired:
                print("workflow deadline exceeded", file=sys.stderr)
                return 2
            except ProcessTreeError:
                print("upstream process isolation failed", file=sys.stderr)
                return 2
            except subprocess.CalledProcessError:
                print(
                    f"version-{selected_version}: pinned commit unavailable",
                    file=sys.stderr,
                )
                return 1
            except ValueError as exc:
                print(exc, file=sys.stderr)
                return 1
            total += n
            print(f"version-{selected_version}: {n} files")
        print(f"total: {total} files")

    if manifest_path is not None and generated_manifest:
        try:
            write_manifest(manifest_path, pinned_refs)
        except (OSError, ValueError) as exc:
            print(f"upstream manifest error: {exc}", file=sys.stderr)
            return 1
        print("upstream manifest: written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
