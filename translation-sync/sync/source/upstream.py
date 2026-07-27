#!/usr/bin/env python3
"""Laravel 공식 문서 원문을 i18n/en에 적재한다.

- 출처: github.com/laravel/docs (버전 문자열 = 브랜치명)
- 대상: i18n/en/docusaurus-plugin-content-docs/version-<v>/
- 공식 원문 Markdown 파일을 byte-for-byte로 복사한다.

이 모듈은 translation-sync/docs/05(T1) 원문 캐시 구축과 workflow의 원문 동기화 단계를 담당한다.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import shutil
import sys
import tempfile
from pathlib import Path

from ..common.files import atomic_write_bytes, unlink_file
from ..common.versions import load_versions

REPO_ROOT = Path(__file__).resolve().parents[3]
UPSTREAM_REPO = "https://github.com/laravel/docs.git"
EN_ROOT = REPO_ROOT / "i18n" / "en" / "docusaurus-plugin-content-docs"
MANIFEST_ENV = "TRANSLATION_UPSTREAM_MANIFEST"
UPSTREAM_CLONE_TIMEOUT = 300
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
_VERSION_RE = re.compile(r"^(?:master|(?:0|[1-9]\d*)\.x)$")


def supported_versions() -> list[str]:
    """versions.json을 단일 출처로 사용한다."""
    return load_versions(REPO_ROOT / "versions.json")


def _run(
    args: list[str],
    cwd: Path | None = None,
    quiet: bool = False,
    timeout: int | None = None,
) -> None:
    subprocess.run(
        args,
        cwd=cwd,
        check=True,
        timeout=timeout,
        stdout=subprocess.DEVNULL if quiet else None,
        stderr=subprocess.DEVNULL if quiet else None,
    )


def _output(args: list[str], cwd: Path) -> str:
    return subprocess.run(
        args,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _clone_upstream(repo_dir: Path) -> None:
    args = [
        "git",
        "-c",
        "http.version=HTTP/1.1",
        "clone",
        "--no-single-branch",
        "--quiet",
        UPSTREAM_REPO,
        str(repo_dir),
    ]
    for attempt in range(3):
        shutil.rmtree(repo_dir, ignore_errors=True)
        try:
            _run(args, timeout=UPSTREAM_CLONE_TIMEOUT)
            return
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            if attempt == 2:
                raise


def write_manifest(path: Path, refs: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "repository": UPSTREAM_REPO,
        "versions": dict(sorted(refs.items())),
    }
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as stream:
            temporary = Path(stream.name)
            stream.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def load_manifest(path: Path) -> dict[str, str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("repository") != UPSTREAM_REPO:
        raise ValueError("upstream manifest repository mismatch")
    refs = payload.get("versions")
    if not isinstance(refs, dict) or not all(
        isinstance(version, str)
        and isinstance(ref, str)
        and _COMMIT_RE.fullmatch(ref)
        for version, ref in refs.items()
    ):
        raise ValueError("invalid upstream manifest version refs")
    return refs


def manifest_ref(refs: dict[str, str], version: str) -> str:
    try:
        return refs[version]
    except KeyError as exc:
        raise ValueError(f"upstream manifest missing ref for version-{version}") from exc


def _has_symlink_component(path: Path, *, root: Path) -> bool:
    current = root
    if current.is_symlink():
        return True
    for part in path.relative_to(root).parts:
        current /= part
        if current.is_symlink():
            return True
    return False


def _version_destination(version: str) -> Path:
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


def sync_version(
    repo_dir: Path,
    version: str,
    *,
    ref: str | None = None,
    doc: str | None = None,
) -> int:
    """단일 버전 브랜치의 원문 .md를 i18n/en에 적재하고 적재 수를 반환한다."""
    if doc is not None and (Path(doc).name != doc or not doc.endswith(".md")):
        raise ValueError(f"invalid document: {doc}")
    dest = _version_destination(version)
    if doc is not None:
        target = _document_destination(dest, doc)
    else:
        for cached in dest.glob("*.md"):
            _document_destination(dest, cached.name)
    _run(["git", "checkout", "--force", ref or version], cwd=repo_dir, quiet=True)
    dest = _version_destination(version)
    dest.mkdir(parents=True, exist_ok=True)
    dest = _version_destination(version)
    if doc is not None:
        target = _document_destination(dest, doc)
    else:
        for cached in dest.glob("*.md"):
            _document_destination(dest, cached.name)

    if doc is not None:
        source = repo_dir / doc
        if source.is_symlink():
            raise ValueError(f"upstream Markdown symlink: {source.name}")
        if not source.is_file():
            unlink_file(target, missing_ok=True)
            return 0
        atomic_write_bytes(target, source.read_bytes())
        return 1

    sources = sorted(repo_dir.glob("*.md"))
    for source in sources:
        if source.is_symlink():
            raise ValueError(f"upstream Markdown symlink: {source.name}")
        _document_destination(dest, source.name)

    count = 0
    for md in sources:
        atomic_write_bytes(
            _document_destination(dest, md.name),
            md.read_bytes(),
        )
        count += 1

    source_names = {source.name for source in sources}
    for stale in dest.glob("*.md"):
        if stale.name not in source_names:
            unlink_file(stale, missing_ok=True)
    return count


def main(*, version: str | None = None, doc: str | None = None) -> int:
    try:
        versions = supported_versions()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"versions.json error: {exc}", file=sys.stderr)
        return 1
    if version is not None:
        if version not in versions:
            print(f"unsupported version: {version}", file=sys.stderr)
            return 1
        versions = [version]
    if doc is not None and (Path(doc).name != doc or not doc.endswith(".md")):
        print(f"invalid document filter: {doc}", file=sys.stderr)
        return 1

    manifest_value = os.environ.get(MANIFEST_ENV, "").strip()
    manifest_path = Path(manifest_value).resolve() if manifest_value else None
    try:
        pinned_refs = (
            load_manifest(manifest_path)
            if manifest_path is not None and manifest_path.exists()
            else None
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"upstream manifest error: {exc}", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        repo_dir = Path(tmp) / "laravel-docs"
        try:
            _clone_upstream(repo_dir)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            print("upstream clone failed", file=sys.stderr)
            return 1

        total = 0
        resolved_refs: dict[str, str] = {}
        for version in versions:
            try:
                ref = manifest_ref(pinned_refs, version) if pinned_refs is not None else version
                n = sync_version(repo_dir, version, ref=ref, doc=doc)
            except subprocess.CalledProcessError:
                if pinned_refs is not None:
                    print(
                        f"version-{version}: pinned commit unavailable",
                        file=sys.stderr,
                    )
                else:
                    print(f"version-{version}: branch unavailable", file=sys.stderr)
                return 1
            except ValueError as exc:
                print(exc, file=sys.stderr)
                return 1
            resolved_refs[version] = _output(["git", "rev-parse", "HEAD"], repo_dir)
            total += n
            print(f"version-{version}: {n} files")
        print(f"total: {total} files")

    if manifest_path is not None and pinned_refs is None:
        try:
            write_manifest(manifest_path, resolved_refs)
        except OSError as exc:
            print(f"upstream manifest error: {exc}", file=sys.stderr)
            return 1
        print(f"upstream manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
