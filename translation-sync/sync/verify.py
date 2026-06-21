"""문서·번역 검증 (Python). translation-sync/docs/04.

docs/05(T5)에 따라 문서·번역 콘텐츠 검증은 Python으로 처리한다.
(Docusaurus 빌드 산출물 검증은 JS validate-anchors.mjs가 담당.)

최종 문서에 남으면 안 되는 잔존 패턴을 검사하고 위반 목록을 반환한다(빈 목록 = success).
"""
from __future__ import annotations

import re
from collections import Counter

# 코드 블록 밖에서 남으면 안 되는 패턴 (docs/04 §14)
_FORBIDDEN = {
    "unreplaced {{version}}": re.compile(r"\{\{\s*version\s*\}\}"),
    "unrestored base64 placeholder": re.compile(r"__BASE64_IMAGE_\d+__"),
    "title style class": re.compile(r"^#{1,6}\s+.+?\s+\{[.#][^}]*\}\s*$", re.MULTILINE),
    "legacy note marker": re.compile(
        r"^>\s*(\{note\}|\*\*Note\*\*|Note:)", re.MULTILINE | re.IGNORECASE
    ),
    "unclosed img tag": re.compile(r"<img\b(?![^>]*/>)[^>]*>", re.IGNORECASE),
}

_FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})", re.MULTILINE)
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_HTML_COMMENT_BODY_RE = re.compile(r"<!--\s*(.*?)\s*-->", re.DOTALL)
_MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_AUTOLINK_RE = re.compile(r"<(https?://[^>\s]+)>")
_INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
_ANCHOR_TAG_RE = re.compile(r"<a\b[^>]*\bname=[\"'][^\"']+[\"'][^>]*>", re.IGNORECASE)
_ANCHOR_NAME_RE = re.compile(r"\bname=[\"']([^\"']+)[\"']", re.IGNORECASE)


def _strip_code_blocks(text: str) -> str:
    """fenced code block을 제거해 코드 예시 안의 패턴을 검사 대상에서 뺀다."""
    out: list[str] = []
    in_code = False
    fence = ""
    for line in text.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            token = stripped[:3]
            if not in_code:
                in_code, fence = True, token
                continue
            if stripped.startswith(fence):
                in_code = False
                continue
        if not in_code:
            out.append(line)
    return "\n".join(out)


def _strip_comments(text: str) -> str:
    return _HTML_COMMENT_RE.sub("", text)


def _fenced_code_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    in_code = False
    fence = ""
    cur: list[str] = []
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            token = stripped[:3]
            if not in_code:
                in_code, fence = True, token
                cur = [line]
                continue
            if stripped.startswith(fence):
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
    body = _strip_code_blocks(_strip_comments(text))
    return Counter(_MARKDOWN_LINK_RE.findall(body) + _AUTOLINK_RE.findall(body))


def _inline_codes(text: str) -> Counter[str]:
    body = _strip_code_blocks(_strip_comments(text))
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


def _normalize_comment_text(text: str) -> str:
    text = text.replace("*&#47;", "*/").replace("--&gt;", "-->")
    return " ".join(text.split())


def _required_comments(source: str) -> set[str]:
    body = _strip_code_blocks(source)
    comments: set[str] = set()
    paragraph: list[str] = []
    in_front_matter = False
    seen_content = False

    def flush_paragraph() -> None:
        if paragraph:
            comments.add(_normalize_comment_text(" ".join(paragraph)))
            paragraph.clear()

    for line in body.splitlines():
        stripped = line.strip()
        if stripped == "---" and not seen_content:
            in_front_matter = not in_front_matter
            continue
        if in_front_matter:
            continue
        if not stripped:
            flush_paragraph()
            continue
        seen_content = True
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
        _normalize_comment_text(match)
        for match in _HTML_COMMENT_BODY_RE.findall(text)
        if _normalize_comment_text(match)
    }


def verify(text: str, source: str | None = None) -> list[str]:
    """위반 라벨 목록 반환. 빈 목록이면 success."""
    body = _strip_code_blocks(text)
    issues = [label for label, pattern in _FORBIDDEN.items() if pattern.search(body)]

    if source is None:
        return issues

    if _link_targets(source) != _link_targets(text):
        issues.append("link target mismatch")
    if _inline_codes(source) != _inline_codes(text):
        issues.append("inline code mismatch")
    if _anchors(source) != _anchors(text):
        issues.append("anchor mismatch")
    if _normalized_fenced_code_blocks(source) != _normalized_fenced_code_blocks(text):
        issues.append("code block mismatch")
    if not _required_comments(source).issubset(_translated_comments(text)):
        issues.append("missing original comment")

    return issues
