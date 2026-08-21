#!/usr/bin/env python3
"""고정된 업스트림 커밋의 Laravel 영어 원문 캐시 동기화.

지원 버전별 브랜치 끝을 한 번 조회해 정규 매니페스트로 고정.
이후 모든 체크아웃에 매니페스트의 커밋 객체 ID만 사용.
원문 Markdown 바이트를 정규화하지 않고 ``i18n/en/docusaurus-plugin-content-docs/version-<v>/``에 복사.
전체 동기화 시 업스트림에 없는 기존 캐시 파일 삭제.
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
UPSTREAM_FETCH_TIMEOUT = 300
UPSTREAM_REF_QUERY_TIMEOUT = 30
_COMMIT_RE = {
    "sha1": re.compile(r"^[0-9a-f]{40}$"),
    "sha256": re.compile(r"^[0-9a-f]{64}$"),
}
_VERSION_RE = re.compile(r"^(?:master|(?:0|[1-9]\d*)\.x)$")
_MANIFEST_TOP_LEVEL_KEYS = ("schema_version", "entries")
_MANIFEST_ENTRY_KEYS = ("version", "repository", "object_format", "commit")
_INVALID_REF_ADVERTISEMENT = "invalid upstream ref advertisement"
_UPSTREAM_PROCESS_ISOLATION_FAILED = "upstream process isolation failed"
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


class _UpstreamFailure(RuntimeError):
    """CLI 진단과 종료 코드를 함께 전달하는 제어된 동기화 실패."""

    def __init__(self, message: str, exit_code: int) -> None:
        """출력할 진단과 종료 코드 저장.

        Args:
            message: 표준 오류에 출력할 진단.
            exit_code: CLI 종료 코드.
        """

        super().__init__(message)
        self.exit_code = exit_code


def supported_versions() -> list[str]:
    """``versions.json``을 단일 출처로 사용하는 지원 버전 목록."""
    return load_versions(REPO_ROOT / "versions.json")


def _git_environment() -> dict[str, str]:
    """자격 증명과 사용자 설정을 제거한 업스트림 Git 환경 구성."""

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
    """격리된 환경에서 업스트림 Git 인수 벡터 실행."""

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
    """격리된 환경에서 Git 인수 벡터를 실행하고 표준 출력 반환."""

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
    """공유 기한과 단계별 상한 중 더 짧은 제한 시간 계산."""

    if deadline is None:
        return cap
    if not math.isfinite(deadline) or deadline <= 0:
        raise ValueError("invalid source synchronization deadline")
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise subprocess.TimeoutExpired(["source-sync-deadline"], 0)
    return min(remaining, cap) if cap is not None else remaining


def _prepare_upstream(
    repo_dir: Path,
    refs: dict[str, str],
    *,
    doc: str | None = None,
    deadline: float | None = None,
) -> None:
    """고정 커밋만 포함하는 희소 업스트림 저장소 준비."""

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
    """지원 버전별 업스트림 브랜치 참조 이름 구성."""

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
    """단일 문서 경로를 리터럴 희소 체크아웃 패턴으로 변환."""

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
    """Git 원격 참조 응답을 버전별 커밋으로 파싱."""

    if not isinstance(output, str) or not output:
        raise ValueError(_INVALID_REF_ADVERTISEMENT)
    commits_by_ref: dict[str, str] = {}
    for line in output.splitlines():
        if line.count("\t") != 1:
            raise ValueError(_INVALID_REF_ADVERTISEMENT)
        commit, ref_name = line.split("\t")
        if ref_name not in expected_refs or ref_name in commits_by_ref:
            raise ValueError(_INVALID_REF_ADVERTISEMENT)
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
    """단일 원격 조회로 지원 버전 브랜치의 커밋 수집."""

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
    """커밋 객체 ID 길이로 Git 객체 형식 판별."""

    if not isinstance(commit, str):
        raise ValueError("manifest commit must be a lowercase full object ID")
    if _COMMIT_RE["sha1"].fullmatch(commit):
        return "sha1"
    if _COMMIT_RE["sha256"].fullmatch(commit):
        return "sha256"
    raise ValueError("manifest commit must be a lowercase full object ID")


def _manifest_payload(refs: dict[str, str]) -> dict[str, object]:
    """버전별 커밋 매핑을 정규 매니페스트 페이로드로 변환."""

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
    """버전별 업스트림 커밋의 정규 매니페스트 바이트 생성."""

    return (
        json.dumps(
            _manifest_payload(refs),
            ensure_ascii=False,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def manifest_digest(contents: bytes) -> str:
    """정규 매니페스트 바이트의 SHA-256 해시 계산."""

    return hashlib.sha256(contents).hexdigest()


def write_manifest(path: Path, refs: dict[str, str]) -> None:
    """심볼릭 링크를 따라가지 않고 정규 매니페스트를 원자적으로 기록."""

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


def _decode_manifest_payload(contents: bytes) -> dict[str, object]:
    """정규 매니페스트 JSON과 최상위 schema 검증.

    Args:
        contents: UTF-8 JSON 매니페스트 바이트.

    Returns:
        검증된 최상위 JSON object.
    """

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
    return payload


def _manifest_entry_ref(entry: object, refs: dict[str, str]) -> tuple[str, str]:
    """단일 매니페스트 항목을 검증해 버전과 커밋 추출.

    Args:
        entry: JSON에서 읽은 매니페스트 항목.
        refs: 중복 검사용 기존 버전별 커밋 mapping.

    Returns:
        검증된 버전과 커밋.
    """

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
    return version, commit


def load_manifest_bytes(
    contents: bytes,
    *,
    expected_versions: list[str] | None = None,
) -> dict[str, str]:
    """정규 매니페스트 바이트를 검증하고 버전별 커밋 로딩."""

    payload = _decode_manifest_payload(contents)
    entries = payload["entries"]
    if not isinstance(entries, list):
        raise TypeError("invalid upstream manifest schema")
    refs: dict[str, str] = {}
    for entry in entries:
        version, commit = _manifest_entry_ref(entry, refs)
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
    """파일에서 정규 업스트림 매니페스트 로딩."""

    return load_manifest_bytes(
        path.read_bytes(),
        expected_versions=expected_versions,
    )


def resolve_manifest(
    versions: list[str],
    *,
    deadline: float | None = None,
) -> bytes:
    """원격 브랜치를 한 번 조회해 고정 업스트림 매니페스트 확정."""

    return canonical_manifest(_query_remote_refs(versions, deadline=deadline))


def manifest_ref(refs: dict[str, str], version: str) -> str:
    """매니페스트에서 요청 버전의 고정 커밋 조회."""

    try:
        return refs[version]
    except KeyError as exc:
        raise ValueError(f"upstream manifest missing ref for version-{version}") from exc


def _has_symlink_component(path: Path, *, root: Path) -> bool:
    """루트부터 대상까지 경로 구성 요소의 심볼릭 링크 포함 여부."""

    current = root
    if current.is_symlink():
        return True
    for part in path.relative_to(root).parts:
        current /= part
        if current.is_symlink():
            return True
    return False


def _version_destination(version: str) -> Path:
    """검증된 버전의 영어 원문 캐시 디렉터리 반환."""

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
    """버전 캐시 내부의 정규 문서 대상 경로 검증."""

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
    """중첩 Markdown 문서 선택자를 정규 POSIX 경로로 정규화."""

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


def _collect_markdown_entry(
    path: Path,
    *,
    directory: Path,
    root: Path,
    exclude_git: bool,
    pending: list[Path],
    documents: list[Path],
) -> None:
    """재귀 순회 중 단일 경로를 검증해 디렉터리 또는 문서로 수집.

    Args:
        path: 검사할 직접 하위 경로.
        directory: 현재 순회 중인 디렉터리.
        root: 순회 기준 루트.
        exclude_git: 루트의 ``.git`` 제외 여부.
        pending: 이후 순회할 디렉터리 stack.
        documents: 검증된 Markdown 파일 누적 목록.
    """

    if exclude_git and directory == root and path.name == ".git":
        return
    if path.is_symlink():
        raise ValueError(
            "upstream Markdown symlink: "
            + path.relative_to(root).as_posix()
        )
    if path.is_dir():
        pending.append(path)
        return
    if path.suffix != ".md":
        return
    if not path.is_file():
        raise ValueError(
            "upstream Markdown path is unsafe: "
            + path.relative_to(root).as_posix()
        )
    relative = path.relative_to(root).as_posix()
    if normalize_document_selector(relative) != relative:
        raise ValueError(f"upstream Markdown path is not canonical: {relative}")
    documents.append(path)


def _recursive_markdown_files(root: Path, *, exclude_git: bool = False) -> list[Path]:
    """심볼릭 링크를 거부하며 루트 아래의 Markdown 파일을 재귀적으로 수집."""

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
            _collect_markdown_entry(
                path,
                directory=directory,
                root=root,
                exclude_git=exclude_git,
                pending=pending,
                documents=documents,
            )
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


def _validated_version_destination(version: str, doc: str | None) -> tuple[Path, Path | None]:
    """버전 캐시와 선택 문서 대상을 기존 파일까지 포함해 검증.

    Args:
        version: 지원 문서 버전.
        doc: 선택 문서 경로.

    Returns:
        버전 캐시 경로와 선택 문서 대상 경로.
    """

    destination = _version_destination(version)
    if doc is not None:
        return destination, _document_destination(destination, doc)
    for cached in _recursive_markdown_files(destination):
        relative = cached.relative_to(destination).as_posix()
        _document_destination(destination, relative)
    return destination, None


def _sync_selected_document(
    repo_dir: Path,
    destination: Path,
    target: Path,
    document: str,
) -> int:
    """선택한 단일 업스트림 Markdown 문서를 캐시에 동기화.

    Args:
        repo_dir: 체크아웃된 업스트림 저장소.
        destination: 버전 캐시 경로.
        target: 캐시의 선택 문서 대상 경로.
        document: 업스트림 기준 문서 경로.

    Returns:
        적재한 문서 수.
    """

    source = repo_dir / document
    if _has_symlink_component(source, root=repo_dir):
        raise ValueError(f"upstream Markdown symlink: {source.name}")
    try:
        source_mode = source.lstat().st_mode
    except FileNotFoundError:
        unlink_file(target, missing_ok=True)
        _remove_empty_parents(target.parent, stop=destination)
        return 0
    if not stat.S_ISREG(source_mode):
        raise ValueError(f"upstream Markdown path is unsafe: {document}")
    target.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_bytes(target, source.read_bytes())
    return 1


def _remove_stale_documents(
    destination: Path,
    source_names: set[str],
) -> None:
    """업스트림에 없는 캐시 문서와 비게 된 상위 디렉터리 제거.

    Args:
        destination: 버전 캐시 경로.
        source_names: 업스트림의 정규 문서 경로 집합.
    """

    stale_parents: set[Path] = set()
    for stale in _recursive_markdown_files(destination):
        relative = stale.relative_to(destination).as_posix()
        if relative not in source_names:
            unlink_file(stale, missing_ok=True)
            stale_parents.add(stale.parent)
    for parent in sorted(
        stale_parents,
        key=lambda path: len(path.relative_to(destination).parts),
        reverse=True,
    ):
        _remove_empty_parents(parent, stop=destination)


def _sync_all_documents(repo_dir: Path, destination: Path) -> int:
    """업스트림 Markdown 전체를 캐시에 복사하고 오래된 문서 제거.

    Args:
        repo_dir: 체크아웃된 업스트림 저장소.
        destination: 버전 캐시 경로.

    Returns:
        적재한 문서 수.
    """

    sources = _recursive_markdown_files(repo_dir, exclude_git=True)
    for source in sources:
        relative = source.relative_to(repo_dir).as_posix()
        _document_destination(destination, relative)
    for source in sources:
        relative = source.relative_to(repo_dir).as_posix()
        target = _document_destination(destination, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_bytes(target, source.read_bytes())
    source_names = {
        source.relative_to(repo_dir).as_posix() for source in sources
    }
    _remove_stale_documents(destination, source_names)
    return len(sources)


def sync_version(
    repo_dir: Path,
    version: str,
    *,
    ref: str | None = None,
    doc: str | None = None,
    deadline: float | None = None,
) -> int:
    """고정 커밋의 단일 버전 원문을 영어 캐시에 파일별로 원자적 적재.

    Args:
        repo_dir: 희소 체크아웃으로 준비된 업스트림 저장소 경로.
        version: 적재 대상 문서 버전.
        ref: 매니페스트가 고정한 업스트림 커밋 객체 ID. 생략 시 ``version`` 사용.
        doc: 선택적으로 적재할 단일 정규 Markdown 경로.
        deadline: 전체 워크플로의 단조 시계 기한.

    Returns:
        영어 캐시에 적재한 Markdown 파일 수.

    Raises:
        ValueError: 버전, 커밋 또는 문서 선택자가 부적합한 경우.
        ProcessTreeError: 하위 프로세스 격리 실패.
        subprocess.CalledProcessError: 업스트림 Git 명령 실패.
        subprocess.TimeoutExpired: 공유 기한을 초과한 경우.
    """
    if doc is not None:
        doc = normalize_document_selector(doc)
    _validated_version_destination(version, doc)
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
    dest, target = _validated_version_destination(version, doc)

    if doc is not None:
        if target is None:
            raise ValueError(f"invalid document destination: {doc}")
        return _sync_selected_document(repo_dir, dest, target, doc)
    return _sync_all_documents(repo_dir, dest)


def _selected_scope(
    manifest_versions: list[str],
    version: str | None,
    document: str | None,
) -> tuple[list[str], str | None]:
    """CLI 버전과 문서 필터를 검증해 동기화 범위 결정.

    Args:
        manifest_versions: 매니페스트 전체 지원 버전.
        version: 선택 버전.
        document: 선택 문서 경로.

    Returns:
        선택된 버전 목록과 정규 문서 경로.
    """

    if document is not None and version is None:
        raise ValueError("invalid document filter: --doc requires --version")
    if version is not None and version not in manifest_versions:
        raise ValueError(f"unsupported version: {version}")
    selected_versions = manifest_versions if version is None else [version]
    if document is None:
        return selected_versions, None
    try:
        return selected_versions, normalize_document_selector(document)
    except ValueError:
        raise ValueError(f"invalid document filter: {document}") from None


def _load_manifest_state(
    manifest_versions: list[str],
) -> tuple[Path | None, bytes | None, dict[str, str] | None]:
    """환경이 지정한 기존 매니페스트와 digest 검증.

    Args:
        manifest_versions: 매니페스트에 필요한 전체 지원 버전.

    Returns:
        매니페스트 경로, 기존 바이트, 고정 ref mapping.
    """

    manifest_value = os.environ.get(MANIFEST_ENV, "").strip()
    manifest_path = Path(manifest_value).resolve() if manifest_value else None
    manifest_contents: bytes | None = None
    pinned_refs: dict[str, str] | None = None
    if manifest_path is not None and manifest_path.exists():
        manifest_contents = manifest_path.read_bytes()
        pinned_refs = load_manifest_bytes(
            manifest_contents,
            expected_versions=manifest_versions,
        )
    expected_digest = os.environ.get(MANIFEST_DIGEST_ENV, "").strip()
    if expected_digest and (
        manifest_contents is None
        or manifest_digest(manifest_contents) != expected_digest
    ):
        raise ValueError("upstream manifest digest mismatch")
    return manifest_path, manifest_contents, pinned_refs


def _resolve_manifest_refs(
    manifest_versions: list[str],
    *,
    deadline: float | None,
) -> tuple[bytes, dict[str, str]]:
    """원격 ref를 조회해 정규 매니페스트와 고정 ref 구성.

    Args:
        manifest_versions: 조회할 전체 지원 버전.
        deadline: 선택적 원문 동기화 기한.

    Returns:
        생성한 매니페스트 바이트와 버전별 고정 ref.
    """

    try:
        contents = resolve_manifest(manifest_versions, deadline=deadline)
        refs = load_manifest_bytes(
            contents,
            expected_versions=manifest_versions,
        )
        return contents, refs
    except ProcessTreeError as exc:
        raise _UpstreamFailure(_UPSTREAM_PROCESS_ISOLATION_FAILED, 2) from exc
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        exit_code = 2 if deadline is not None else 1
        raise _UpstreamFailure("upstream ref query failed", exit_code) from exc
    except ValueError as exc:
        raise _UpstreamFailure(f"upstream manifest error: {exc}", 1) from exc


def _prepare_repository(
    repo_dir: Path,
    selected_refs: dict[str, str],
    *,
    document: str | None,
    deadline: float | None,
) -> None:
    """선택 ref를 임시 업스트림 저장소에 준비.

    Args:
        repo_dir: 임시 업스트림 저장소 경로.
        selected_refs: 선택 버전별 고정 ref.
        document: 선택 문서 경로.
        deadline: 공통 워크플로 기한.
    """

    try:
        _prepare_upstream(
            repo_dir,
            selected_refs,
            doc=document,
            deadline=deadline,
        )
    except ProcessTreeError as exc:
        raise _UpstreamFailure(_UPSTREAM_PROCESS_ISOLATION_FAILED, 2) from exc
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        exit_code = 2 if deadline is not None else 1
        raise _UpstreamFailure("upstream fetch failed", exit_code) from exc
    except ValueError as exc:
        raise _UpstreamFailure(str(exc), 1) from exc


def _sync_selected_version(
    repo_dir: Path,
    version: str,
    pinned_refs: dict[str, str],
    *,
    document: str | None,
    deadline: float | None,
) -> int:
    """준비된 저장소에서 단일 버전 원문 동기화.

    Args:
        repo_dir: 준비된 업스트림 저장소.
        version: 동기화할 버전.
        pinned_refs: 전체 버전별 고정 ref.
        document: 선택 문서 경로.
        deadline: 공통 워크플로 기한.

    Returns:
        적재한 문서 수.
    """

    try:
        ref = manifest_ref(pinned_refs, version)
        sync_kwargs: dict[str, object] = {"ref": ref, "doc": document}
        if deadline is not None:
            sync_kwargs["deadline"] = deadline
        return sync_version(repo_dir, version, **sync_kwargs)
    except subprocess.TimeoutExpired as exc:
        raise _UpstreamFailure("source synchronization deadline exceeded", 2) from exc
    except ProcessTreeError as exc:
        raise _UpstreamFailure(_UPSTREAM_PROCESS_ISOLATION_FAILED, 2) from exc
    except subprocess.CalledProcessError as exc:
        message = f"version-{version}: pinned commit unavailable"
        raise _UpstreamFailure(message, 1) from exc
    except ValueError as exc:
        raise _UpstreamFailure(str(exc), 1) from exc


def _sync_selected_versions(
    selected_versions: list[str],
    pinned_refs: dict[str, str],
    *,
    document: str | None,
    deadline: float | None,
) -> None:
    """임시 저장소에서 선택 범위 전체를 동기화하고 수량 출력.

    Args:
        selected_versions: 동기화할 버전 목록.
        pinned_refs: 전체 버전별 고정 ref.
        document: 선택 문서 경로.
        deadline: 공통 워크플로 기한.
    """

    selected_refs = {
        selected_version: manifest_ref(pinned_refs, selected_version)
        for selected_version in selected_versions
    }
    with tempfile.TemporaryDirectory() as tmp:
        repo_dir = Path(tmp) / "laravel-docs"
        _prepare_repository(
            repo_dir,
            selected_refs,
            document=document,
            deadline=deadline,
        )
        total = 0
        for selected_version in selected_versions:
            count = _sync_selected_version(
                repo_dir,
                selected_version,
                pinned_refs,
                document=document,
                deadline=deadline,
            )
            total += count
            print(f"version-{selected_version}: {count} files")
        print(f"total: {total} files")


def main(*, version: str | None = None, doc: str | None = None) -> int:
    """매니페스트 확정 또는 재사용 후 선택 범위의 원문 동기화.

    Args:
        version: 선택적으로 동기화할 단일 지원 버전.
        doc: ``version`` 내부의 선택적 정규 Markdown 경로.

    Returns:
        성공 시 0.
        제어된 입력·매니페스트·일반 Git 실패 시 1.
        프로세스 격리 실패 또는 원격 프로세스 실패 시 2.
    """

    try:
        manifest_versions = supported_versions()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"versions.json error: {exc}", file=sys.stderr)
        return 1
    try:
        selected_versions, doc = _selected_scope(manifest_versions, version, doc)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    try:
        manifest_path, _, pinned_refs = _load_manifest_state(manifest_versions)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"upstream manifest error: {exc}", file=sys.stderr)
        return 1
    generated_manifest = pinned_refs is None
    if pinned_refs is None:
        try:
            _, pinned_refs = _resolve_manifest_refs(
                manifest_versions,
                deadline=None,
            )
        except _UpstreamFailure as exc:
            print(exc, file=sys.stderr)
            return exc.exit_code

    try:
        _sync_selected_versions(
            selected_versions,
            pinned_refs,
            document=doc,
            deadline=None,
        )
    except _UpstreamFailure as exc:
        print(exc, file=sys.stderr)
        return exc.exit_code
    except ValueError as exc:
        print(f"upstream manifest error: {exc}", file=sys.stderr)
        return 1

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
