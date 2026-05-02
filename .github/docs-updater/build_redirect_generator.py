#!/usr/bin/env python3
"""Generate unversioned docs redirects for the latest stable version.

배포 워크플로우 단계에서 사용한다. 사이트가 정적 파일로만 호스팅되는
GitHub Pages 환경에서, `/docs/<slug>` 같은 비-versioned 경로가 latest stable
버전(`/docs/<latest>/<slug>`)으로 redirect 되도록 build/ 하위에 redirect
HTML을 만들어 둔다. Docusaurus가 시작 시 client-side로도 같은 redirect를
하지만, 정적 응답이 있어야 unknown URL 직접 접근에서도 빠르게 동작한다.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOCALES = ("", "en", "ja")


def latest_stable_version(versions: list[str]) -> str:
    return next((version for version in versions if version != "master"), versions[0])


def front_matter_slug(content: str) -> str | None:
    if not content.startswith("---\n"):
        return None

    end = content.find("\n---", 4)
    if end < 0:
        return None

    front_matter = content[4:end]
    match = re.search(r"^slug:\s*['\"]?([^'\"\n]+)['\"]?\s*$", front_matter, re.M)
    if not match:
        return None
    return match.group(1).strip("/")


def redirect_html(target: str) -> str:
    json_target = json.dumps(target)
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<link rel="canonical" href="{target}">
<meta http-equiv="refresh" content="0; url={target}">
<script>window.location.replace({json_target} + window.location.search + window.location.hash)</script>
</head>
<body>
<a href="{target}">Redirecting...</a>
</body>
</html>
"""


def write_redirect(build_root: Path, locale: str, slug: str, latest_version: str) -> None:
    locale_prefix = f"/{locale}" if locale else ""
    target = (
        f"{locale_prefix}/docs/{latest_version}/{slug}"
        if slug
        else f"{locale_prefix}/docs/{latest_version}"
    )
    html = redirect_html(target)

    output_dir = build_root / locale / "docs" / slug
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text(html, encoding="utf-8")

    clean_url_file = build_root / locale / "docs.html" if not slug else (
        build_root / locale / "docs" / f"{slug}.html"
    )
    clean_url_file.parent.mkdir(parents=True, exist_ok=True)
    clean_url_file.write_text(html, encoding="utf-8")


def collect_slugs(docs_root: Path) -> set[str]:
    slugs = {""}
    for entry in docs_root.iterdir():
        if not entry.is_file() or entry.suffix != ".md":
            continue
        if entry.name in {"documentation.md", "readme.md"}:
            continue

        content = entry.read_text(encoding="utf-8")
        slug = front_matter_slug(content)
        slugs.add(slug if slug is not None else entry.stem)

    return slugs


def create_latest_doc_redirects(
    repo_root: Path | str = REPO_ROOT,
    locales: tuple[str, ...] = DEFAULT_LOCALES,
) -> int:
    repo_root = Path(repo_root)
    versions = json.loads((repo_root / "versions.json").read_text(encoding="utf-8"))
    latest_version = latest_stable_version(versions)
    docs_root = repo_root / "versioned_docs" / f"version-{latest_version}"
    build_root = repo_root / "build"

    slugs = collect_slugs(docs_root)
    for locale in locales:
        for slug in slugs:
            write_redirect(build_root, locale, slug, latest_version)

    print(
        f"[create-latest-doc-redirects] {len(slugs)} redirects generated for {latest_version}"
    )
    return len(slugs)


def main() -> int:
    create_latest_doc_redirects(REPO_ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
