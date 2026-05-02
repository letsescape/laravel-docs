"""Validate source and translated document structure.

원문 캐시(`.github/docs-updater/source/version-*`) 와 번역본
(`versioned_docs/version-*`) 사이의 명시적 앵커, heading 구조, 내부 링크 대상이
일치하는지 검증한다. main.py 의 마지막 단계에서 호출되어, 어떤 파일이라도 실패가
기록되면 exit code 1을 반환한다.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from markdown_link_utils import (
    extract_internal_markdown_links,
    replace_version_placeholders,
    strip_code,
)


EXCLUDED_FILES: frozenset[str] = frozenset({"license.md", "readme.md", "documentation.md"})


@dataclass(frozen=True)
class StructureIssue:
    type: str
    detail: object


@dataclass(frozen=True)
class FileIssues:
    version: str
    file: str
    issues: tuple[StructureIssue, ...]


@dataclass
class StructureReport:
    total: int = 0
    files_with_issues: int = 0
    issues: list[FileIssues] = field(default_factory=list)

    @property
    def has_issues(self) -> bool:
        return bool(self.issues)


def extract_anchors(text: str) -> list[str]:
    """`<a name="...">` 명시적 앵커를 코드 영역을 제외하고 추출."""
    anchors: list[str] = []
    stripped = strip_code(text)
    index = 0
    length = len(stripped)
    while index < length:
        tag_start = stripped.find("<a", index)
        if tag_start < 0:
            break

        tag_end = stripped.find(">", tag_start + 2)
        if tag_end < 0:
            break

        tag = stripped[tag_start : tag_end + 1]
        name_pos = tag.find("name=")
        if name_pos >= 0:
            quote_index = name_pos + len("name=")
            if quote_index < len(tag):
                quote = tag[quote_index]
                if quote in ('"', "'"):
                    value_start = quote_index + 1
                    value_end = tag.find(quote, value_start)
                    if value_end >= 0:
                        anchors.append(tag[value_start:value_end])
        index = tag_end + 1
    return anchors


@dataclass(frozen=True)
class Heading:
    level: int
    text: str


def extract_headings(text: str) -> list[Heading]:
    """`#` 으로 시작하는 ATX heading 만 추출. setext heading은 다루지 않는다."""
    stripped = strip_code(text)
    headings: list[Heading] = []
    for line in stripped.split("\n"):
        level = 0
        while level < len(line) and line[level] == "#":
            level += 1
        if level < 1 or level > 6:
            continue
        if level >= len(line):
            continue
        if line[level] not in (" ", "\t"):
            continue
        headings.append(Heading(level=level, text=line[level + 1 :].strip()))
    return headings


def _replace_suffix(value: str, search: str, replacement: str) -> str:
    if not value.endswith(search):
        return value
    return value[: -len(search)] + replacement


# upstream(공식 라라벨 문서)에 남아 있는 stale anchor/링크 매핑.
# 번역본은 "원문이 의도한" 앵커로 치환된 채로 빌드되므로, 비교 시 동일 매핑을
# 적용해 차이가 위양성으로 잡히지 않게 한다. JS 버전과 같은 의미를 유지한다.
_DROP_LINKS: frozenset[str] = frozenset(
    {"#assert-similar-json", "#formatting-shortcode-notifications"}
)


def normalize_internal_link(url: str, version: str) -> str | None:
    normalized = replace_version_placeholders(url, version)
    laravel_docs_prefix = f"https://laravel.com/docs/{version}"
    if (
        normalized == laravel_docs_prefix
        or normalized.startswith(laravel_docs_prefix + "/")
        or normalized.startswith(laravel_docs_prefix + "#")
    ):
        normalized = "/docs/" + version + normalized[len(laravel_docs_prefix) :]

    normalized = normalized.replace("#agents-integration", "#agent-integration")
    normalized = _replace_suffix(
        normalized,
        "#actions-handled-by-resource-controller",
        "#actions-handled-by-resource-controllers",
    )
    normalized = normalized.replace(
        "/migrations#writing-migrations",
        "/migrations#creating-tables",
    )
    normalized = normalized.replace(
        "#method-array-sort-recursive-desc",
        "#method-array-sort-recursive",
    )
    normalized = normalized.replace("/errors#logging", "/logging")
    normalized = normalized.replace(
        "/helpers#fluent-strings",
        "/strings#fluent-strings",
    )
    normalized = normalized.replace("##date-casting", "#date-casting")
    normalized = normalized.replace(
        "/database-testing#writing-factories",
        "/database-testing#defining-model-factories",
    )

    if normalized in _DROP_LINKS:
        return None

    return normalized


def extract_internal_links(text: str, version: str) -> list[str]:
    links: list[str] = []
    for link in extract_internal_markdown_links(text):
        normalized = normalize_internal_link(link.url, version)
        if normalized is None:
            continue
        links.append(normalized)
    return links


@dataclass(frozen=True)
class LinkDiff:
    link: str
    source: int
    translated: int


def compare_link_targets(
    source: str, translated: str, version: str
) -> list[LinkDiff]:
    src_links = Counter(extract_internal_links(source, version))
    tr_links = Counter(extract_internal_links(translated, version))
    keys = set(src_links) | set(tr_links)
    diffs: list[LinkDiff] = []
    for link in keys:
        src_count = src_links.get(link, 0)
        tr_count = tr_links.get(link, 0)
        if src_count != tr_count:
            diffs.append(LinkDiff(link=link, source=src_count, translated=tr_count))
    diffs.sort(key=lambda diff: diff.link)
    return diffs


def compare(
    source: str, translated: str, version: str
) -> tuple[StructureIssue, ...]:
    issues: list[StructureIssue] = []

    src_anchors = sorted(extract_anchors(source))
    tr_anchors = sorted(extract_anchors(translated))
    if src_anchors != tr_anchors:
        missing = sorted(set(src_anchors) - set(tr_anchors))
        extra = sorted(set(tr_anchors) - set(src_anchors))
        if missing:
            issues.append(StructureIssue(type="anchor-missing", detail=missing))
        if extra:
            issues.append(StructureIssue(type="anchor-extra", detail=extra))

    src_headings = extract_headings(source)
    tr_headings = extract_headings(translated)
    if len(src_headings) == len(tr_headings):
        for index, (src_h, tr_h) in enumerate(zip(src_headings, tr_headings)):
            if src_h.level != tr_h.level:
                issues.append(
                    StructureIssue(
                        type="heading-level",
                        detail=(
                            f"#{index}: source={src_h.level} ({src_h.text}) "
                            f"translated={tr_h.level} ({tr_h.text})"
                        ),
                    )
                )
    else:
        issues.append(
            StructureIssue(
                type="heading-count",
                detail=(
                    f"source={len(src_headings)} translated={len(tr_headings)}"
                ),
            )
        )

    link_diffs = compare_link_targets(source, translated, version)
    if link_diffs:
        issues.append(
            StructureIssue(
                type="internal-link-target",
                detail=tuple(
                    {
                        "link": diff.link,
                        "source": diff.source,
                        "translated": diff.translated,
                    }
                    for diff in link_diffs
                ),
            )
        )

    return tuple(issues)


def _iter_versioned_md_files(source_dir: Path) -> Iterable[Path]:
    for entry in sorted(source_dir.iterdir()):
        if entry.is_file() and entry.suffix == ".md":
            yield entry


def _format_excluded(name: str) -> bool:
    return name.lower() in EXCLUDED_FILES


def validate_structure(
    source_root: Path | str,
    docs_root: Path | str,
) -> StructureReport:
    source_root = Path(source_root)
    docs_root = Path(docs_root)
    report = StructureReport()

    if not source_root.exists():
        return report

    for version_dir in sorted(
        entry for entry in source_root.iterdir() if entry.is_dir()
    ):
        if not version_dir.name.startswith("version-"):
            continue
        docs_dir = docs_root / version_dir.name
        if not docs_dir.exists():
            continue
        version = version_dir.name.removeprefix("version-")

        for entry in _iter_versioned_md_files(version_dir):
            if _format_excluded(entry.name):
                continue
            translated_path = docs_dir / entry.name
            report.total += 1
            if not translated_path.exists():
                report.issues.append(
                    FileIssues(
                        version=version_dir.name,
                        file=entry.name,
                        issues=(StructureIssue(type="translation-missing", detail=None),),
                    )
                )
                report.files_with_issues += 1
                continue

            source_text = entry.read_text(encoding="utf-8")
            translated_text = translated_path.read_text(encoding="utf-8")
            issues = compare(source_text, translated_text, version)
            if issues:
                report.issues.append(
                    FileIssues(
                        version=version_dir.name,
                        file=entry.name,
                        issues=issues,
                    )
                )
                report.files_with_issues += 1

    return report


def render_report(report: StructureReport) -> str:
    lines = [
        f"Total: {report.total} files",
        f"Files with structural issues: {report.files_with_issues}",
    ]

    if not report.issues:
        return "\n".join(lines)

    by_version: Counter[str] = Counter()
    by_type: Counter[str] = Counter()
    for file_issue in report.issues:
        by_version[file_issue.version] += 1
        for issue in file_issue.issues:
            by_type[issue.type] += 1

    lines.append("")
    lines.append("--- Issues by version ---")
    for version in sorted(by_version):
        lines.append(f"  {version}: {by_version[version]}")

    lines.append("")
    lines.append("--- Issues by type ---")
    for issue_type, count in sorted(
        by_type.items(), key=lambda item: (-item[1], item[0])
    ):
        lines.append(f"  {issue_type}: {count}")

    lines.append("")
    lines.append("--- Detailed issues ---")
    for file_issue in report.issues:
        lines.append("")
        lines.append(f"[{file_issue.version}/{file_issue.file}]")
        for issue in file_issue.issues:
            lines.append(f"  {issue.type}: {_format_detail(issue.detail)}")

    return "\n".join(lines)


def _format_detail(detail: object) -> str:
    if detail is None:
        return "null"
    if isinstance(detail, (str, int, float, bool)):
        return json.dumps(detail, ensure_ascii=False)
    if isinstance(detail, (list, tuple)):
        return json.dumps(list(detail), ensure_ascii=False, separators=(",", ":"))
    if isinstance(detail, dict):
        return json.dumps(detail, ensure_ascii=False, separators=(",", ":"))
    return json.dumps(str(detail), ensure_ascii=False)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    source_root = repo_root / ".github" / "docs-updater" / "source"
    docs_root = repo_root / "versioned_docs"
    report = validate_structure(source_root, docs_root)
    print(render_report(report))
    return 1 if report.has_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
