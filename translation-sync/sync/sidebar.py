"""Sidebar sync from documentation.md.

translation-sync/docs/06-sidebar-sync.md is the source of truth for this step:
versioned sidebars are generated from English documentation.md, while locale
sidebar override JSON files are removed.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

REPO_ROOT = Path(__file__).resolve().parents[2]
DOC_LINK_RE = re.compile(r"^\s*-\s*\[([^\]\n]+)]\(([^)\s]+)\)\s*$")
VERSION_RE = re.compile(r"^(?:master|[0-9]+\.x)$")
SIDEBAR_LOCALES = ("ko", "ja")


@dataclass(frozen=True)
class SidebarResult:
    version: str
    changed: bool
    issues: list[str]


def load_versions(repo_root: Path = REPO_ROOT) -> list[str]:
    versions = json.loads((repo_root / "versions.json").read_text(encoding="utf-8"))
    return [_validate_version_token(version) for version in versions]


def _validate_version_token(version: object) -> str:
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        raise ValueError(f"invalid version: {version}")
    return version


def _supported_version(version: str, repo_root: Path = REPO_ROOT) -> str:
    version = _validate_version_token(version)
    if version not in load_versions(repo_root):
        raise ValueError(f"unknown version: {version}")
    return version


def latest_stable_version(repo_root: Path = REPO_ROOT) -> str:
    versions = load_versions(repo_root)
    return next((version for version in versions if version != "master"), versions[0])


def resolve_versions(
    *, all_versions: bool = False, version: str | None = None, repo_root: Path = REPO_ROOT
) -> list[str]:
    versions = load_versions(repo_root)
    if all_versions:
        return versions
    if version:
        if version not in versions:
            raise ValueError(f"unknown version: {version}")
        return [version]
    return ["master"]


def _documentation_path(repo_root: Path, version: str) -> Path:
    return (
        repo_root
        / "i18n"
        / "en"
        / "docusaurus-plugin-content-docs"
        / f"version-{version}"
        / "documentation.md"
    )


def _source_doc_path(repo_root: Path, version: str, doc_id: str) -> Path:
    return (
        repo_root
        / "i18n"
        / "en"
        / "docusaurus-plugin-content-docs"
        / f"version-{version}"
        / f"{doc_id}.md"
    )


def _sidebar_path(repo_root: Path, version: str) -> Path:
    return repo_root / "versioned_sidebars" / f"version-{version}-sidebars.json"


def locale_sidebar_paths(repo_root: Path, version: str) -> list[Path]:
    return [
        repo_root
        / "i18n"
        / locale
        / "docusaurus-plugin-content-docs"
        / f"version-{version}.json"
        for locale in SIDEBAR_LOCALES
    ]


def _doc_id_from_href(href: str) -> str | None:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        return None

    segments = [segment for segment in parsed.path.split("/") if segment]
    if not segments:
        return None
    if segments[0] == "docs" and len(segments) >= 3:
        return segments[-1]
    return segments[-1]


def _category_label(line: str) -> str | None:
    stripped = line.strip()
    if not stripped.startswith("-"):
        return None

    after_dash = stripped[1:].lstrip()
    if not after_dash.startswith("##"):
        return None

    after_hashes = after_dash[2:]
    if not after_hashes or not after_hashes[0].isspace():
        return None

    label = after_hashes.strip()
    return label or None


def _normalize_link_href(href: str, *, version: str, latest_stable: str) -> str:
    if version == "master" and href.startswith("https://api.laravel.com/docs/"):
        return f"https://api.laravel.com/docs/{latest_stable}"
    return href


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "item"


def _unique_doc_key(
    doc_id: str, category_label: str, seen_doc_ids: set[str], used_keys: set[str]
) -> str:
    if doc_id not in seen_doc_ids and doc_id not in used_keys:
        seen_doc_ids.add(doc_id)
        used_keys.add(doc_id)
        return doc_id

    base = f"{doc_id}-{_slug(category_label)}"
    key = base
    index = 2
    while key in used_keys:
        key = f"{base}-{index}"
        index += 1

    seen_doc_ids.add(doc_id)
    used_keys.add(key)
    return key


def parse_documentation(
    text: str, *, version: str, latest_stable: str
) -> tuple[list[dict], list[str]]:
    items: list[dict] = []
    current_category: dict | None = None
    issues: list[str] = []
    seen_doc_ids: set[str] = set()
    used_keys: set[str] = set()

    for line_number, line in enumerate(text.splitlines(), start=1):
        label = _category_label(line)
        if label:
            current_category = {
                "type": "category",
                "label": label,
                "collapsed": label != "Getting Started",
                "items": [],
                "key": label,
            }
            items.append(current_category)
            continue

        link_match = DOC_LINK_RE.match(line)
        if not link_match:
            continue

        label = link_match.group(1).strip()
        href = _normalize_link_href(
            link_match.group(2).strip(), version=version, latest_stable=latest_stable
        )
        doc_id = _doc_id_from_href(href)

        if doc_id is None:
            link_item = {"type": "link", "label": label, "href": href}
            if current_category is not None and line[: len(line) - len(line.lstrip())]:
                current_category["items"].append(link_item)
            else:
                items.append(link_item)
                current_category = None
            continue

        if current_category is None:
            issues.append(f"line {line_number}: doc link is outside a category")
            continue

        category_label = str(current_category["label"])
        current_category["items"].append(
            {
                "type": "doc",
                "id": doc_id,
                "label": label,
                "key": _unique_doc_key(
                    doc_id,
                    category_label,
                    seen_doc_ids,
                    used_keys,
                ),
            }
        )

    return items, issues


def _existing_collapsed(sidebar: dict) -> dict[str, bool]:
    collapsed: dict[str, bool] = {}
    for node in sidebar.get("tutorialSidebar", []):
        if not isinstance(node, dict) or node.get("type") != "category":
            continue
        key = node.get("key") or node.get("label")
        if isinstance(key, str) and isinstance(node.get("collapsed"), bool):
            collapsed[key] = node["collapsed"]
    return collapsed


def _apply_existing_collapsed(items: list[dict], current: dict) -> None:
    collapsed = _existing_collapsed(current)
    for node in items:
        if not isinstance(node, dict) or node.get("type") != "category":
            continue
        key = node.get("key")
        if isinstance(key, str) and key in collapsed:
            node["collapsed"] = collapsed[key]


def _doc_ids(items: list[dict]) -> list[str]:
    ids: list[str] = []
    for node in items:
        if isinstance(node, dict) and node.get("type") == "category":
            ids.extend(
                item["id"]
                for item in node.get("items", [])
                if isinstance(item, dict) and item.get("type") == "doc"
            )
    return ids


def build_sidebar(
    version: str, *, current: dict | None = None, repo_root: Path = REPO_ROOT
) -> tuple[dict, list[str]]:
    version = _supported_version(version, repo_root)
    latest_stable = latest_stable_version(repo_root)
    documentation_path = _documentation_path(repo_root, version)
    if not documentation_path.exists():
        return {}, [f"missing documentation.md for {version}"]

    items, issues = parse_documentation(
        documentation_path.read_text(encoding="utf-8"),
        version=version,
        latest_stable=latest_stable,
    )
    current = current or {}
    _apply_existing_collapsed(items, current)

    for doc_id in _doc_ids(items):
        if not _source_doc_path(repo_root, version, doc_id).exists():
            issues.append(f"missing source doc for sidebar item: {doc_id}")

    return {"tutorialSidebar": items}, issues


def _read_sidebar(path: Path) -> tuple[dict, list[str]]:
    if not path.exists():
        return {}, []
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except json.JSONDecodeError as exc:
        return {}, [f"invalid sidebar JSON: {exc}"]


def _write_sidebar(path: Path, sidebar: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(sidebar, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def sync_version(
    version: str, *, write: bool = False, repo_root: Path = REPO_ROOT
) -> SidebarResult:
    version = _supported_version(version, repo_root)
    path = _sidebar_path(repo_root, version)
    current, issues = _read_sidebar(path)
    expected, build_issues = build_sidebar(version, current=current, repo_root=repo_root)
    issues.extend(build_issues)

    locale_paths = locale_sidebar_paths(repo_root, version)
    if not issues:
        sidebar_changed = current != expected
        locale_paths_to_remove = [path for path in locale_paths if path.exists()]
        changed = sidebar_changed or bool(locale_paths_to_remove)

        if write:
            if sidebar_changed:
                _write_sidebar(path, expected)
            for locale_path in locale_paths_to_remove:
                locale_path.unlink()

            current, read_issues = _read_sidebar(path)
            issues.extend(read_issues)
            sidebar_changed = current != expected
            locale_paths_to_remove = [path for path in locale_paths if path.exists()]

        if sidebar_changed:
            issues.append("sidebar JSON out of sync")
        for locale_path in locale_paths_to_remove:
            issues.append(f"locale sidebar JSON remains: {locale_path.relative_to(repo_root)}")

        return SidebarResult(
            version=version,
            changed=changed,
            issues=issues,
        )

    return SidebarResult(version=version, changed=False, issues=issues)


def sync_versions(
    versions: list[str], *, write: bool = False, repo_root: Path = REPO_ROOT
) -> list[SidebarResult]:
    unique_versions = list(dict.fromkeys(versions))
    return [
        sync_version(version, write=write, repo_root=repo_root)
        for version in unique_versions
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sync versioned sidebars from documentation.md")
    parser.add_argument("--version")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    try:
        versions = resolve_versions(
            all_versions=args.all,
            version=args.version,
            repo_root=REPO_ROOT,
        )
    except ValueError as exc:
        print(exc)
        return 1

    results = sync_versions(versions, write=args.write, repo_root=REPO_ROOT)
    failed = False
    for result in results:
        if result.issues:
            failed = True
            for issue in result.issues:
                print(f"{result.version}: {issue}")
            continue
        status = "updated" if result.changed and args.write else "verified"
        print(f"{result.version}: sidebar {status}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
