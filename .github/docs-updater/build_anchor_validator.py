#!/usr/bin/env python3
"""Validate built site anchors against the source Markdown.

배포 워크플로우 단계에서 사용한다. `versioned_docs/` 의 markdown 안 `#fragment`
링크가 `build/` 산출물 HTML 의 id 와 일치하는지 검사해, 한국어 slug 와 라라벨
원문 anchor 사이의 매핑이 깨지지 않았는지 확인한다. 사이트(Docusaurus) 자체에는
의존을 만들지 않으며, deploy.yml 이 빌드 후에 호출한다.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

from markdown_link_utils import (
    extract_markdown_links,
    replace_version_placeholders,
    strip_code,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_ROOT = REPO_ROOT / "versioned_docs"
BUILD_ROOT = REPO_ROOT / "build"


@dataclass(frozen=True)
class BrokenAnchor:
    md: str
    src: str
    target: str
    anchor: str
    reason: str


@dataclass
class AnchorReport:
    total: int = 0
    ok: int = 0
    missing_html: int = 0
    id_not_found: int = 0
    broken: list[BrokenAnchor] = field(default_factory=list)

    @property
    def has_failures(self) -> bool:
        return bool(self.broken)


def walk_markdown(docs_root: Path) -> list[Path]:
    markdown_files: list[Path] = []
    for path in sorted(docs_root.rglob("*.md")):
        if "origin" in path.relative_to(docs_root).parts:
            continue
        if path.name == "documentation.md":
            continue
        markdown_files.append(path)
    return markdown_files


def to_url_path(docs_root: Path, md_path: Path) -> str:
    parts = md_path.relative_to(docs_root).parts
    version = parts[0].removeprefix("version-")
    tail = "/".join(parts[1:])[:-3]
    if tail == "installation":
        return f"/docs/{version}"
    return f"/docs/{version}/{tail}"


def html_path_for(build_root: Path, url: str) -> Path:
    relative_url = (url[1:] if url.startswith("/") else url).strip("/")
    if not relative_url:
        return build_root / "index.html"

    clean_url_path = build_root / f"{relative_url}.html"
    if clean_url_path.exists():
        return clean_url_path

    return build_root / relative_url / "index.html"


def docs_version_from_url(url: str) -> str | None:
    prefix = "/docs/"
    if not url.startswith(prefix):
        return None
    end = url.find("/", len(prefix))
    return url[len(prefix) : end] if end >= 0 else None


def rewrite_installation_route(path: str) -> str:
    suffix = "/installation"
    return path[: -len(suffix)] if path.endswith(suffix) else path


def _is_external_url(href: str) -> bool:
    lower = href.lower()
    return (
        lower.startswith("http://")
        or lower.startswith("https://")
        or lower.startswith("mailto:")
    )


def _target_from_href(href: str, src_url: str, src_version: str | None) -> tuple[str, str]:
    if href.startswith("#"):
        return src_url, href[1:]

    hash_index = href.find("#")
    path = href[:hash_index]
    anchor = href[hash_index + 1 :]
    if src_version:
        path = replace_version_placeholders(path, src_version)
    if not path.startswith("/") and src_version:
        path = f"/docs/{src_version}/{path}"
    path = rewrite_installation_route(path)
    return path, anchor


def validate_anchors(repo_root: Path | str = REPO_ROOT) -> AnchorReport:
    repo_root = Path(repo_root)
    docs_root = repo_root / "versioned_docs"
    build_root = repo_root / "build"
    if not build_root.exists():
        raise FileNotFoundError("build/ not found. Run `npm run build` first.")

    report = AnchorReport()
    html_cache: dict[Path, str] = {}

    for md_path in walk_markdown(docs_root):
        source = strip_code(md_path.read_text(encoding="utf-8"))
        src_url = to_url_path(docs_root, md_path)
        src_version = docs_version_from_url(src_url)

        for link in extract_markdown_links(source):
            href = link.url
            if "#" not in href or _is_external_url(href):
                continue

            target_url, anchor = _target_from_href(href, src_url, src_version)
            report.total += 1
            html_path = html_path_for(build_root, target_url)
            if not html_path.exists():
                report.missing_html += 1
                report.broken.append(
                    BrokenAnchor(
                        md=str(md_path.relative_to(repo_root)),
                        src=src_url,
                        target=target_url,
                        anchor=anchor,
                        reason="target HTML missing",
                    )
                )
                continue

            html = html_cache.setdefault(
                html_path,
                html_path.read_text(encoding="utf-8"),
            )
            if f'id="{anchor}"' in html:
                report.ok += 1
            else:
                report.id_not_found += 1
                report.broken.append(
                    BrokenAnchor(
                        md=str(md_path.relative_to(repo_root)),
                        src=src_url,
                        target=target_url,
                        anchor=anchor,
                        reason="id not found in HTML",
                    )
                )

    return report


def render_report(report: AnchorReport) -> str:
    lines = [
        f"Total anchor links:  {report.total}",
        f"  OK (id in HTML):   {report.ok}",
        f"  Target HTML gone:  {report.missing_html}",
        f"  id not found:      {report.id_not_found}",
    ]

    if report.broken:
        lines.append("")
        lines.append("Broken details:")
        for item in report.broken:
            lines.append(
                f"  [{item.reason}] {item.md} on {item.src} -> "
                f"{item.target}#{item.anchor}"
            )

    return "\n".join(lines)


def main() -> int:
    try:
        report = validate_anchors(REPO_ROOT)
    except FileNotFoundError:
        print("[validate-anchors] build/ not found. Run `npm run build` first.", file=sys.stderr)
        return 2

    print(render_report(report))
    return 1 if report.has_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
