#!/usr/bin/env python3
"""Laravel 공식 문서 원문을 i18n/en에 적재한다.

- 출처: github.com/laravel/docs (버전 문자열 = 브랜치명)
- 대상: i18n/en/docusaurus-plugin-content-docs/version-<v>/
- 원문 의미와 {{version}} 등 플레이스홀더는 그대로 둔다.
- 저장소 lint를 위해 줄 끝 공백과 EOF 개행만 정규화한다.

이 모듈은 translation-sync/docs/05(T1) 원문 캐시 구축과 workflow의 원문 동기화 단계를 담당한다.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
UPSTREAM_REPO = "https://github.com/laravel/docs.git"
EN_ROOT = REPO_ROOT / "i18n" / "en" / "docusaurus-plugin-content-docs"


def supported_versions() -> list[str]:
    """versions.json을 단일 출처로 사용한다."""
    return json.loads((REPO_ROOT / "versions.json").read_text("utf-8"))


def _run(args: list[str], cwd: Path | None = None, quiet: bool = False) -> None:
    subprocess.run(
        args,
        cwd=cwd,
        check=True,
        stdout=subprocess.DEVNULL if quiet else None,
        stderr=subprocess.DEVNULL if quiet else None,
    )


def normalize_markdown_source(text: str) -> str:
    """줄 끝 공백만 제거하고 EOF는 하나의 newline으로 정규화한다."""
    normalized_lines: list[str] = []
    for line in text.splitlines(keepends=True):
        if line.endswith("\r\n"):
            body, ending = line[:-2], "\r\n"
        elif line.endswith("\n"):
            body, ending = line[:-1], "\n"
        elif line.endswith("\r"):
            body, ending = line[:-1], "\r"
        else:
            body, ending = line, ""
        normalized_lines.append(body.rstrip(" \t") + ending)

    normalized = "".join(normalized_lines)
    if normalized.endswith(("\n", "\r")):
        return normalized.rstrip("\r\n") + "\n"
    return normalized


def sync_version(repo_dir: Path, version: str) -> int:
    """단일 버전 브랜치의 원문 .md를 i18n/en에 적재하고 적재 수를 반환한다."""
    _run(["git", "checkout", "--force", version], cwd=repo_dir, quiet=True)

    dest = EN_ROOT / f"version-{version}"
    dest.mkdir(parents=True, exist_ok=True)
    for stale in dest.glob("*.md"):
        stale.unlink()

    count = 0
    for md in sorted(repo_dir.glob("*.md")):
        (dest / md.name).write_text(
            normalize_markdown_source(md.read_text(encoding="utf-8")),
            encoding="utf-8",
        )
        count += 1
    return count


def main() -> int:
    versions = supported_versions()
    with tempfile.TemporaryDirectory() as tmp:
        repo_dir = Path(tmp) / "laravel-docs"
        _run(["git", "clone", "--no-single-branch", "--quiet", UPSTREAM_REPO, str(repo_dir)])

        total = 0
        for version in versions:
            try:
                n = sync_version(repo_dir, version)
            except subprocess.CalledProcessError:
                print(f"version-{version}: branch not found, skipped", file=sys.stderr)
                continue
            total += n
            print(f"version-{version}: {n} files")
        print(f"total: {total} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
