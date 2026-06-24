"""문서·번역 검증 (Python). translation-sync/docs/04.

문서·번역 콘텐츠 검증은 Python으로 처리한다.
Docusaurus 빌드 산출물 검증은 JS validate-anchors.mjs가 담당한다.

최종 문서에 남으면 안 되는 잔존 패턴을 검사하고 위반 목록을 반환한다(빈 목록 = success).
"""
from __future__ import annotations

import re
from collections import Counter

from .markdown import (
    closes_fence,
    fence_token,
    has_title_attr_line,
    html_comment_bodies,
    is_heading_line,
    strip_title_attr_line,
    strip_html_comments,
)

# 코드 블록 밖에서 남으면 안 되는 패턴 (docs/04 §14)
_FORBIDDEN = {
    "unreplaced {{version}}": re.compile(r"\{\{\s*version\s*\}\}"),
    "unrestored base64 placeholder": re.compile(r"__BASE64_IMAGE_\d+__"),
    "legacy note marker": re.compile(
        r"^>\s*(\{note\}|\*\*Note\*\*|Note:)", re.MULTILINE | re.IGNORECASE
    ),
    "unclosed img tag": re.compile(r"<img\b(?![^>]*/>)[^>]*>", re.IGNORECASE),
}

_MARKDOWN_LINK_RE = re.compile(r"(!?)\[([^\]\n]*)]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_AUTOLINK_RE = re.compile(r"<(https?://[^>\s]+)>")
_INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
_ANCHOR_TAG_RE = re.compile(r"<a\b[^>]*\bname=[\"'][^\"']+[\"'][^>]*>", re.IGNORECASE)
_ANCHOR_NAME_RE = re.compile(r"\bname=[\"']([^\"']+)[\"']", re.IGNORECASE)
_HEADING_LINE_RE = re.compile(r"^[ \t]*#{1,6}\s.*$", re.MULTILINE)
_DOCS_PREFIX_RE = re.compile(r"^/docs/[^/#?]+/?")
_STALE_LINK_TARGETS = {
    "#agents-integration": "#agent-integration",
    "#method-array-sort-recursive-desc": "#method-array-sort-recursive",
    "controllers#actions-handled-by-resource-controller": "controllers#actions-handled-by-resource-controllers",
    "database-testing#writing-factories": "database-testing#defining-model-factories",
    "eloquent-mutators##date-casting": "eloquent-mutators#date-casting",
    "errors#logging": "logging",
    "helpers#fluent-strings": "strings#fluent-strings",
    "migrations#writing-migrations": "migrations#creating-tables",
    "##date-casting": "#date-casting",
}


def _strip_heading_lines(text: str) -> str:
    """heading 라인 제거.

    heading 텍스트 자체는 `_heading_lines`에서 원문과 비교한다. 여기서는 heading에
    포함된 인라인 코드/링크가 본문 비교에서 한 번 더 계산되지 않도록 제외한다.
    """
    return _HEADING_LINE_RE.sub("", text)


def _strip_code_blocks(text: str) -> str:
    """fenced code block을 제거해 코드 예시 안의 패턴을 검사 대상에서 뺀다."""
    out: list[str] = []
    in_code = False
    fence = ""
    for line in text.split("\n"):
        token = fence_token(line)
        if token:
            if not in_code:
                in_code, fence = True, token
                continue
            if closes_fence(line, fence):
                in_code = False
                continue
        if not in_code:
            out.append(line)
    return "\n".join(out)


def _strip_comments(text: str) -> str:
    return strip_html_comments(text)


def _fenced_code_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    in_code = False
    fence = ""
    cur: list[str] = []
    for line in text.splitlines(keepends=True):
        token = fence_token(line)
        if token:
            if not in_code:
                in_code, fence = True, token
                cur = [line]
                continue
            if closes_fence(line, fence):
                cur.append(line)
                blocks.append("".join(cur))
                in_code = False
                cur = []
                continue
        if in_code:
            cur.append(line)
    return blocks


def _normalized_fenced_code_blocks(text: str) -> list[str]:
    return [
        "\n".join(line.rstrip(" \t") for line in block.rstrip("\n").split("\n"))
        for block in _fenced_code_blocks(text)
    ]


def _link_targets(text: str) -> Counter[str]:
    body = _strip_heading_lines(_strip_code_blocks(_strip_comments(text)))
    targets = [match.group(3) for match in _MARKDOWN_LINK_RE.finditer(body)]
    targets += _AUTOLINK_RE.findall(body)
    return Counter(_normalize_link_target(target) for target in targets)


def _link_labels(text: str) -> list[str]:
    body = _strip_code_blocks(_strip_comments(text))
    return [
        " ".join(match.group(2).split())
        for match in _MARKDOWN_LINK_RE.finditer(body)
        if match.group(1) != "!"
    ]


def _normalize_link_target(target: str) -> str:
    if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
        return target
    target = _DOCS_PREFIX_RE.sub("", target)
    if target.startswith("./"):
        target = target[2:]
    if target.startswith("/"):
        target = target[1:]
    return _STALE_LINK_TARGETS.get(target, target)


def _inline_codes(text: str) -> Counter[str]:
    body = _strip_heading_lines(_strip_code_blocks(_strip_comments(text)))
    return Counter(_INLINE_CODE_RE.findall(body))


def _anchors(text: str) -> Counter[str]:
    body = _strip_code_blocks(_strip_comments(text))
    anchors: list[str] = []
    for tag in _ANCHOR_TAG_RE.findall(body):
        if re.search(r"\bdata-translation-alias\s*=\s*[\"']true[\"']", tag, re.IGNORECASE):
            continue
        match = _ANCHOR_NAME_RE.search(tag)
        if match:
            anchors.append(match.group(1))
    return Counter(anchors)


def _heading_levels(text: str) -> list[int]:
    body = _strip_code_blocks(_strip_comments(text))
    levels: list[int] = []
    for line in body.splitlines():
        stripped = line.lstrip()
        level = len(stripped) - len(stripped.lstrip("#"))
        if 1 <= level <= 6 and len(stripped) > level and stripped[level].isspace():
            levels.append(level)
    return levels


def _heading_lines(text: str) -> list[str]:
    body = _strip_code_blocks(_strip_comments(text))
    headings: list[str] = []
    for line in body.splitlines():
        if is_heading_line(line):
            headings.append(strip_title_attr_line(line).strip())
    return headings


def _front_matter_title(text: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            return None
        if not stripped or stripped.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key.strip() != "title":
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        return value
    return None


def _normalize_comment_text(text: str) -> str:
    text = text.replace("*&#47;", "*/").replace("--&gt;", "-->")
    return " ".join(text.split())


def _required_comments(source: str) -> set[str]:
    body = _strip_code_blocks(source)
    comments: set[str] = set()
    paragraph: list[str] = []
    in_front_matter = False

    def flush_paragraph() -> None:
        if paragraph:
            comments.add(_normalize_comment_text(" ".join(paragraph)))
            paragraph.clear()

    for idx, line in enumerate(body.splitlines()):
        stripped = line.strip()
        if stripped == "---" and idx == 0:
            in_front_matter = True
            continue
        if stripped == "---" and in_front_matter:
            in_front_matter = False
            continue
        if in_front_matter:
            continue
        if not stripped:
            flush_paragraph()
            continue
        if stripped.startswith("<a ") and "name=" in stripped:
            flush_paragraph()
            continue
        if stripped.startswith("#"):
            flush_paragraph()
            comments.add(_normalize_comment_text(stripped))
            continue
        if stripped.startswith(("- [", "* [")) and "](#" in stripped:
            flush_paragraph()
            continue
        if stripped.startswith(("<!--", ">", "|")):
            flush_paragraph()
            continue
        paragraph.append(stripped)

    flush_paragraph()
    return {comment for comment in comments if comment}


def _translated_comments(text: str) -> set[str]:
    return {
        _normalize_comment_text(body)
        for body in html_comment_bodies(text)
        if _normalize_comment_text(body)
    }


def verify(text: str, source: str | None = None) -> list[str]:
    """위반 라벨 목록 반환. 빈 목록이면 success."""
    body = _strip_code_blocks(text)
    issues = [label for label, pattern in _FORBIDDEN.items() if pattern.search(body)]
    if has_title_attr_line(body):
        issues.append("title style class")

    if source is None:
        return issues

    if _link_targets(source) != _link_targets(text):
        issues.append("link target mismatch")
    if _link_labels(source) != _link_labels(text):
        issues.append("link label mismatch")
    if _inline_codes(source) != _inline_codes(text):
        issues.append("inline code mismatch")
    if _anchors(source) != _anchors(text):
        issues.append("anchor mismatch")
    if _normalized_fenced_code_blocks(source) != _normalized_fenced_code_blocks(text):
        issues.append("code block mismatch")
    if _heading_levels(source) != _heading_levels(text):
        issues.append("heading mismatch")
    if _heading_lines(source) != _heading_lines(text):
        issues.append("heading text mismatch")
    if _front_matter_title(source) != _front_matter_title(text):
        issues.append("front matter title mismatch")
    if not _required_comments(source).issubset(_translated_comments(text)):
        issues.append("missing original comment")

    return issues
