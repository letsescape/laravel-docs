#!/usr/bin/env python3
"""Reject worktree changes outside translation sync output paths."""
from __future__ import annotations

import re
import stat
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path

from sync import verify
from sync.common.versions import load_versions

REPO_ROOT = Path(__file__).resolve().parent.parent
_VERSION = r"(?:master|\d+\.x)"
_ALLOWED_PATHS = (
    re.compile(
        rf"i18n/en/docusaurus-plugin-content-docs/version-{_VERSION}/[^/]+\.md"
    ),
    re.compile(
        rf"i18n/ja/docusaurus-plugin-content-docs/version-{_VERSION}/[^/]+\.md"
    ),
    re.compile(rf"versioned_docs/version-{_VERSION}/[^/]+\.md"),
    re.compile(rf"versioned_sidebars/version-{_VERSION}-sidebars\.json"),
    re.compile(
        rf"i18n/(?:ko|ja)/docusaurus-plugin-content-docs/version-{_VERSION}\.json"
    ),
)
_DOCUMENT_PATHS = (
    (
        "en",
        re.compile(
            rf"i18n/en/docusaurus-plugin-content-docs/"
            rf"version-(?P<version>{_VERSION})/(?P<doc>[^/]+\.md)"
        ),
    ),
    (
        "ko",
        re.compile(
            rf"versioned_docs/version-(?P<version>{_VERSION})/"
            rf"(?P<doc>[^/]+\.md)"
        ),
    ),
    (
        "ja",
        re.compile(
            rf"i18n/ja/docusaurus-plugin-content-docs/"
            rf"version-(?P<version>{_VERSION})/(?P<doc>[^/]+\.md)"
        ),
    ),
)
_PATH_VERSION_RE = re.compile(r"(?:^|/)version-(?P<version>master|\d+\.x)(?:/|[-.])")
_SIDEBAR_OVERRIDE_GLOB = "i18n/{locale}/docusaurus-plugin-content-docs/version-*.json"
_NAME_STATUS_RE = re.compile(r"(?:[ADMTUXB]|[CR](?:100|0\d{2}))")
_UNCHANGED_LOCALE_PATHS = {
    "ko": "versioned_docs/version-{version}/{doc}",
    "ja": (
        "i18n/ja/docusaurus-plugin-content-docs/"
        "version-{version}/{doc}"
    ),
}


def unexpected_paths(paths: Iterable[str]) -> list[str]:
    return sorted(
        path
        for path in set(paths)
        if not any(pattern.fullmatch(path) for pattern in _ALLOWED_PATHS)
    )


def validate_changes(
    changes: dict[str, set[str]],
    supported_versions: set[str],
    *,
    verified_unchanged: set[tuple[str, str, str]] | None = None,
) -> list[str]:
    issues: list[str] = []
    verified_unchanged = verified_unchanged or set()
    documents: dict[tuple[str, str], dict[str, set[str]]] = {}

    for path, statuses in sorted(changes.items()):
        version_match = _PATH_VERSION_RE.search(path)
        if version_match and version_match.group("version") not in supported_versions:
            issues.append(f"unsupported translation version: {path}")
            continue
        if not statuses or not statuses <= {"A", "M", "D"}:
            issues.append(f"unsupported translation status: {path}")
            continue
        for locale, pattern in _DOCUMENT_PATHS:
            match = pattern.fullmatch(path)
            if match:
                key = (match.group("version"), match.group("doc"))
                documents.setdefault(key, {})[locale] = statuses
                break

    required_locales = {"en", "ko", "ja"}
    for (version, doc), locale_statuses in sorted(documents.items()):
        label = f"version-{version}/{doc}"
        source_status = locale_statuses.get("en")
        if source_status is None:
            issues.append(f"unpaired translation document: {label}")
            continue

        if source_status == {"M"}:
            if any(
                statuses != {"M"}
                for locale, statuses in locale_statuses.items()
                if locale != "en"
            ):
                issues.append(f"inconsistent translation status: {label}")
            for locale in sorted(required_locales - set(locale_statuses)):
                if (version, doc, locale) not in verified_unchanged:
                    issues.append(
                        "unverified unchanged translation: "
                        f"{label} ({locale})"
                    )
            continue

        if set(locale_statuses) != required_locales:
            issues.append(f"unpaired translation document: {label}")
            continue
        if source_status not in ({"A"}, {"D"}) or any(
            statuses != source_status for statuses in locale_statuses.values()
        ):
            issues.append(f"inconsistent translation status: {label}")
    return issues


def verified_unchanged_locales(
    changes: dict[str, set[str]],
    repo_root: Path = REPO_ROOT,
) -> set[tuple[str, str, str]]:
    verified: set[tuple[str, str, str]] = set()
    source_pattern = _DOCUMENT_PATHS[0][1]
    for source_path, statuses in changes.items():
        match = source_pattern.fullmatch(source_path)
        if match is None or statuses != {"M"}:
            continue
        version = match.group("version")
        doc = match.group("doc")
        source = repo_root / source_path
        for locale, template in _UNCHANGED_LOCALE_PATHS.items():
            target_path = template.format(version=version, doc=doc)
            if target_path in changes:
                continue
            if unsafe_output_paths({source_path, target_path}, repo_root):
                continue
            target = repo_root / target_path
            try:
                source_text = source.read_text(encoding="utf-8")
                target_text = target.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
            if not verify.verify(
                target_text,
                source=source_text,
                version=version,
            ):
                verified.add((version, doc, locale))
    return verified


def _parse_name_status(output: bytes) -> list[tuple[str, str]]:
    if not output:
        return []
    if not output.endswith(b"\0"):
        raise RuntimeError("invalid git name-status output")

    fields = output[:-1].split(b"\0")
    entries: list[tuple[str, str]] = []
    index = 0
    while index < len(fields):
        try:
            status = fields[index].decode("ascii")
        except UnicodeDecodeError as error:
            raise RuntimeError("invalid git name-status output") from error
        index += 1
        if not _NAME_STATUS_RE.fullmatch(status):
            raise RuntimeError("invalid git name-status output")

        path_count = 2 if status[0] in {"C", "R"} else 1
        if index + path_count > len(fields):
            raise RuntimeError("invalid git name-status output")
        paths = [
            field.decode("utf-8", errors="surrogateescape")
            for field in fields[index : index + path_count]
        ]
        index += path_count
        if any(
            not path
            or path.startswith("/")
            or any(part in {"", ".", ".."} for part in path.split("/"))
            for path in paths
        ):
            raise RuntimeError("invalid git name-status output")

        if status.startswith("R"):
            entries.extend((("D", paths[0]), ("A", paths[1])))
        elif status.startswith("C"):
            entries.append(("A", paths[1]))
        else:
            entries.append((status, paths[0]))
    return entries


def changed_entries(repo_root: Path = REPO_ROOT) -> dict[str, set[str]]:
    commands = (
        ["git", "diff", "--name-status", "--no-renames", "-z"],
        ["git", "diff", "--cached", "--name-status", "--no-renames", "-z"],
    )
    changes: dict[str, set[str]] = {}
    for command in commands:
        output = subprocess.run(
            command,
            cwd=repo_root,
            check=True,
            capture_output=True,
        ).stdout
        for status, path in _parse_name_status(output):
            changes.setdefault(path, set()).add(status)

    output = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=repo_root,
        check=True,
        capture_output=True,
    ).stdout
    for raw_path in output.split(b"\0"):
        if raw_path:
            path = raw_path.decode("utf-8", errors="surrogateescape")
            changes.setdefault(path, set()).add("A")
    return changes


def changed_paths(repo_root: Path = REPO_ROOT) -> set[str]:
    return set(changed_entries(repo_root))


def unsafe_output_paths(
    paths: Iterable[str], repo_root: Path = REPO_ROOT
) -> list[str]:
    """Return output paths that traverse symlinks or end at non-files."""

    unsafe: list[str] = []
    for path in set(paths):
        candidate = repo_root
        try:
            for part in Path(path).parts:
                candidate /= part
                try:
                    mode = candidate.lstat().st_mode
                except FileNotFoundError:
                    break
                if stat.S_ISLNK(mode):
                    unsafe.append(path)
                    break
            else:
                if not stat.S_ISREG(mode):
                    unsafe.append(path)
        except OSError:
            unsafe.append(path)
    return sorted(unsafe)


def existing_sidebar_overrides(repo_root: Path = REPO_ROOT) -> list[str]:
    paths: list[str] = []
    for locale in ("ko", "ja"):
        for path in repo_root.glob(_SIDEBAR_OVERRIDE_GLOB.format(locale=locale)):
            paths.append(str(path.relative_to(repo_root)))
    return sorted(paths)


def main() -> int:
    changes = changed_entries()
    paths = set(changes)
    try:
        supported_versions = set(load_versions(REPO_ROOT / "versions.json"))
    except (OSError, ValueError) as exc:
        print(f"invalid versions.json: {exc}", file=sys.stderr)
        return 1
    issues = validate_changes(
        changes,
        supported_versions,
        verified_unchanged=verified_unchanged_locales(changes),
    )
    unexpected = unexpected_paths(paths)
    unsafe = unsafe_output_paths(paths)
    existing_overrides = existing_sidebar_overrides()
    if unexpected or issues or unsafe or existing_overrides:
        if unexpected:
            print("unexpected translation sync changes:", file=sys.stderr)
        for path in unexpected:
            print(f"- {path}", file=sys.stderr)
        if issues:
            print("invalid translation sync changes:", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        if unsafe:
            print("unsafe translation sync output paths:", file=sys.stderr)
        for path in unsafe:
            print(f"- {path}", file=sys.stderr)
        if existing_overrides:
            print("locale sidebar overrides must be deleted:", file=sys.stderr)
        for path in existing_overrides:
            print(f"- {path}", file=sys.stderr)
        return 1
    print(f"translation sync output paths verified: {len(paths)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
