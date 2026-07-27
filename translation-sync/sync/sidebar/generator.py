"""Sidebar sync from documentation.md.

translation-sync/docs/06-sidebar-sync.md is the source of truth for this step:
versioned sidebars are generated from English documentation.md, while locale
sidebar override JSON files are removed.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

from ..common.files import atomic_write_text, unlink_file
from ..common.versions import (
    load_versions as _load_versions,
    validate_version_token as _validate_version_token,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
DOC_LINK_RE = re.compile(r"^\s*-\s*\[([^\]\n]+)]\(([^)\s]+)\)\s*$")
API_DOCS_HREF_RE = re.compile(
    r"^https://api\.laravel\.com/docs/(?:master|\d+\.x)/?$"
)
SIDEBAR_LOCALES = ("ko", "ja")


@dataclass(frozen=True)
class SidebarResult:
    version: str
    changed: bool
    issues: list[str]


def load_versions(repo_root: Path = REPO_ROOT) -> list[str]:
    return _load_versions(repo_root / "versions.json")


def _supported_version(version: str, repo_root: Path = REPO_ROOT) -> str:
    version = _validate_version_token(version)
    for supported in load_versions(repo_root):
        if supported == version:
            _sidebar_filename(supported)
            _locale_sidebar_filename(supported)
            return supported
    raise ValueError(f"unknown version: {version}")


def _safe_repo_path(path: Path, repo_root: Path) -> Path:
    lexical_root = Path(os.path.abspath(repo_root))
    lexical_path = Path(os.path.abspath(path))
    try:
        relative = lexical_path.relative_to(lexical_root)
    except ValueError as exc:
        raise ValueError(f"path escapes repository: {path}") from exc

    resolved_root = repo_root.resolve()
    if not relative.parts:
        return lexical_root

    parent = lexical_root
    for part in relative.parts[:-1]:
        parent /= part
        if parent.is_symlink():
            raise ValueError(f"path escapes repository: {path}")

    resolved_parent = lexical_path.parent.resolve()
    try:
        resolved_parent.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(f"path escapes repository: {path}") from exc
    return lexical_path


def _repo_relative(path: Path, repo_root: Path) -> Path:
    lexical_root = Path(os.path.abspath(repo_root))
    return _safe_repo_path(path, repo_root).relative_to(lexical_root)


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


def _sidebar_filename(version: str) -> str:
    return f"version-{_validate_version_token(version)}-sidebars.json"


def _locale_sidebar_filename(version: str) -> str:
    return f"version-{_validate_version_token(version)}.json"


def _sidebar_path(repo_root: Path, version: str) -> Path:
    return repo_root / "versioned_sidebars" / _sidebar_filename(version)


def locale_sidebar_paths(repo_root: Path, version: str) -> list[Path]:
    filename = _locale_sidebar_filename(version)
    return [
        repo_root
        / "i18n"
        / locale
        / "docusaurus-plugin-content-docs"
        / filename
        for locale in SIDEBAR_LOCALES
    ]


def _doc_id_from_href(href: str) -> str | None:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        return None

    segments = [segment for segment in parsed.path.split("/") if segment]
    if (
        parsed.path.startswith("/docs/")
        and len(segments) == 3
        and segments[0] == "docs"
    ):
        return segments[-1]
    return None


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
    if version == "master" and API_DOCS_HREF_RE.fullmatch(href):
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
    category_keys: set[str] = set()
    link_keys: set[str] = set()

    for line_number, line in enumerate(text.splitlines(), start=1):
        label = _category_label(line)
        if label:
            if label in category_keys:
                issues.append(
                    f"line {line_number}: duplicate category translation key: {label}"
                )
            category_keys.add(label)
            current_category = {
                "type": "category",
                "label": label,
                "collapsed": label != "Getting Started",
                "items": [],
                "key": label,
            }
            items.append(current_category)
            continue

        if re.match(r"^\s*-\s*#", line):
            issues.append(f"line {line_number}: unsupported or malformed category")
            current_category = None
            continue

        link_match = DOC_LINK_RE.match(line)
        if not link_match:
            if re.match(r"^\s*-\s*\[", line):
                issues.append(
                    f"line {line_number}: unsupported or malformed documentation link"
                )
            continue

        label = link_match.group(1).strip()
        href = _normalize_link_href(
            link_match.group(2).strip(), version=version, latest_stable=latest_stable
        )
        doc_id = _doc_id_from_href(href)
        is_indented = bool(line[: len(line) - len(line.lstrip())])

        if doc_id is None:
            if label in link_keys:
                issues.append(
                    f"line {line_number}: duplicate link translation key: {label}"
                )
            link_keys.add(label)
            link_item = {"type": "link", "label": label, "href": href}
            if current_category is not None and is_indented:
                current_category["items"].append(link_item)
            else:
                items.append(link_item)
                current_category = None
            continue

        if current_category is None or not is_indented:
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


def _read_sidebar(version: str, *, repo_root: Path = REPO_ROOT) -> tuple[dict, list[str]]:
    safe_path = _safe_repo_path(_sidebar_path(repo_root, version), repo_root)
    if safe_path.is_symlink():
        return {}, ["sidebar JSON path must not be a symlink"]
    if not safe_path.exists():
        return {}, []
    try:
        sidebar = json.loads(safe_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {}, [f"invalid sidebar JSON: {exc}"]
    if not isinstance(sidebar, dict):
        return {}, ["invalid sidebar JSON schema: root must be an object"]
    if not isinstance(sidebar.get("tutorialSidebar", []), list):
        return {}, [
            "invalid sidebar JSON schema: tutorialSidebar must be a list"
        ]
    return sidebar, []


def _write_sidebar(
    version: str, sidebar: dict, *, repo_root: Path = REPO_ROOT
) -> None:
    safe_path = _safe_repo_path(_sidebar_path(repo_root, version), repo_root)
    safe_path.parent.mkdir(parents=True, exist_ok=True)
    if safe_path.is_symlink():
        raise ValueError("sidebar JSON path must not be a symlink")
    text = json.dumps(sidebar, ensure_ascii=False, indent=2) + "\n"

    atomic_write_text(safe_path, text)


def _existing_repo_paths(paths: list[Path], repo_root: Path) -> list[Path]:
    safe_paths: list[Path] = []
    for path in paths:
        safe_path = _safe_repo_path(path, repo_root)
        if safe_path.exists() or safe_path.is_symlink():
            safe_paths.append(safe_path)
    return safe_paths


def sync_version(
    version: str, *, write: bool = False, repo_root: Path = REPO_ROOT
) -> SidebarResult:
    version = _supported_version(version, repo_root)
    current, issues = _read_sidebar(version, repo_root=repo_root)
    expected, build_issues = build_sidebar(version, current=current, repo_root=repo_root)
    issues.extend(build_issues)

    locale_paths = locale_sidebar_paths(repo_root, version)
    if not issues:
        sidebar_changed = current != expected
        locale_paths_to_remove = _existing_repo_paths(locale_paths, repo_root)
        changed = sidebar_changed or bool(locale_paths_to_remove)

        if write:
            if sidebar_changed:
                _write_sidebar(version, expected, repo_root=repo_root)
            for locale_path in locale_paths_to_remove:
                unlink_file(locale_path, missing_ok=True)

            current, read_issues = _read_sidebar(version, repo_root=repo_root)
            issues.extend(read_issues)
            sidebar_changed = current != expected
            locale_paths_to_remove = _existing_repo_paths(locale_paths, repo_root)

        if sidebar_changed:
            issues.append("sidebar JSON out of sync")
        for locale_path in locale_paths_to_remove:
            issues.append(
                f"locale sidebar JSON remains: {_repo_relative(locale_path, repo_root)}"
            )

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
    target = parser.add_mutually_exclusive_group()
    target.add_argument("--version")
    target.add_argument("--all", action="store_true")
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
