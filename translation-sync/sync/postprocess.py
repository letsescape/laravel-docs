"""번역 후 후처리. translation-sync/docs/03.

- <img> self-closing 변환
- 노트/툴팁 → GFM admonition 표준화
- {{version}} 플레이스홀더 치환
- 제목 옆 {.class} 잔존 제거
- base64 이미지 플레이스홀더 복원
"""
from __future__ import annotations

import re
from typing import Mapping

_IMG_OPEN_RE = re.compile(r"<img\b([^>]*?)\s*>", re.IGNORECASE)
_VERSION_RE = re.compile(r"\{\{\s*version\s*\}\}")
_TITLE_ATTR_RE = re.compile(r"^(#{1,6}\s+.+?)\s+\{[.#][^}]*\}\s*$", re.MULTILINE)
_HTML_COMMENT_RE = re.compile(r"<!--(?P<body>.*?)-->", re.DOTALL)
_NOTE_LINE_RE = re.compile(
    r"^>\s*(?:\{(?P<a>\w+)\}|\*\*(?P<b>\w+)\*\*:?|(?P<c>\w+):)\s*(?P<rest>.*)$"
)
_NOTE_TYPES = {
    "note": "NOTE",
    "tip": "TIP",
    "warning": "WARNING",
    "caution": "CAUTION",
    "important": "IMPORTANT",
}


def _map_outside_code_blocks(text: str, transform) -> str:
    out: list[str] = []
    pending: list[str] = []
    in_code = False
    fence = ""

    def flush_pending() -> None:
        if pending:
            out.append(transform("".join(pending)))
            pending.clear()

    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            token = stripped[:3]
            if not in_code:
                flush_pending()
                in_code = True
                fence = token
                out.append(line)
                continue
            if stripped.startswith(fence):
                in_code = False
                fence = ""
                out.append(line)
                continue

        if in_code:
            out.append(line)
        else:
            pending.append(line)

    flush_pending()
    return "".join(out)


def img_self_closing(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        attrs = match.group(1).strip()
        if attrs.endswith("/"):
            return match.group(0)
        return f"<img {attrs}/>" if attrs else "<img/>"

    return _IMG_OPEN_RE.sub(repl, text)


def standardize_admonitions(text: str) -> str:
    out: list[str] = []
    for line in text.split("\n"):
        m = _NOTE_LINE_RE.match(line)
        if m:
            kind = (m.group("a") or m.group("b") or m.group("c") or "").lower()
            if kind in _NOTE_TYPES:
                out.append(f"> [!{_NOTE_TYPES[kind]}]")
                rest = m.group("rest").strip()
                if rest:
                    out.append(f"> {rest}")
                continue
        out.append(line)
    return "\n".join(out)


def replace_version(text: str, version: str) -> str:
    return _VERSION_RE.sub(version, text)


def restore_placeholders(text: str, placeholders: Mapping[str, str]) -> str:
    for key, original in placeholders.items():
        text = text.replace(key, original)
    return text


def strip_trailing_whitespace(text: str) -> str:
    return "\n".join(line.rstrip(" \t") for line in text.split("\n"))


def escape_html_comments(text: str) -> str:
    """MDX가 HTML 주석을 JS 주석으로 바꿀 때 깨지는 delimiter를 무력화한다."""

    def repl(match: re.Match[str]) -> str:
        body = match.group("body").replace("*/", "*&#47;")
        return f"<!--{body}-->"

    return _HTML_COMMENT_RE.sub(repl, text)


def _postprocess_markdown_body(text: str) -> str:
    text = img_self_closing(text)
    text = standardize_admonitions(text)
    text = _TITLE_ATTR_RE.sub(r"\1", text)
    text = escape_html_comments(text)
    return text


def postprocess(text: str, version: str, placeholders: Mapping[str, str]) -> str:
    text = replace_version(text, version)
    text = _map_outside_code_blocks(text, _postprocess_markdown_body)
    text = restore_placeholders(text, placeholders)
    text = strip_trailing_whitespace(text)
    return text
