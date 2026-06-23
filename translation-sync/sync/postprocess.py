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

from .markdown import closes_fence, fence_token, html_comment_spans, strip_title_attrs

_VERSION_RE = re.compile(r"\{\{\s*version\s*\}\}")
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
        token = fence_token(line)
        if token:
            if not in_code:
                flush_pending()
                in_code = True
                fence = token
                out.append(line)
                continue
            if closes_fence(line, fence):
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
    out: list[str] = []
    lower = text.lower()
    index = 0
    while index < len(text):
        start = lower.find("<img", index)
        if start < 0:
            out.append(text[index:])
            break
        after_name = start + len("<img")
        if after_name < len(text) and not (text[after_name].isspace() or text[after_name] in "/>"):
            out.append(text[index:after_name])
            index = after_name
            continue
        end = text.find(">", after_name)
        if end < 0:
            out.append(text[index:])
            break

        out.append(text[index:start])
        attrs = text[after_name:end].strip()
        if attrs.endswith("/"):
            out.append(text[start : end + 1])
        elif attrs:
            out.append(f"<img {attrs}/>")
        else:
            out.append("<img/>")
        index = end + 1
    return "".join(out)


def _parse_note_line(line: str) -> tuple[str, str] | None:
    if not line.startswith(">"):
        return None

    content = line[1:].strip()
    if content.startswith("{"):
        close = content.find("}")
        if close > 1:
            return content[1:close].lower(), content[close + 1 :].strip()

    if content.startswith("**"):
        close = content.find("**", 2)
        if close > 2:
            rest = content[close + 2 :]
            if rest.startswith(":"):
                rest = rest[1:]
            return content[2:close].lower(), rest.strip()

    colon = content.find(":")
    if colon > 0 and content[:colon].isalpha():
        return content[:colon].lower(), content[colon + 1 :].strip()

    return None


def standardize_admonitions(text: str) -> str:
    out: list[str] = []
    for line in text.split("\n"):
        note = _parse_note_line(line)
        if note:
            kind, rest = note
            if kind in _NOTE_TYPES:
                out.append(f"> [!{_NOTE_TYPES[kind]}]")
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
    out: list[str] = []
    index = 0
    for start, end, body in html_comment_spans(text):
        out.append(text[index:start])
        out.append(f"<!--{body.replace('*/', '*&#47;')}-->")
        index = end
    out.append(text[index:])
    return "".join(out)


def _postprocess_markdown_body(text: str) -> str:
    text = img_self_closing(text)
    text = standardize_admonitions(text)
    text = strip_title_attrs(text)
    text = escape_html_comments(text)
    return text


def postprocess(text: str, version: str, placeholders: Mapping[str, str]) -> str:
    text = replace_version(text, version)
    text = _map_outside_code_blocks(text, _postprocess_markdown_body)
    text = restore_placeholders(text, placeholders)
    text = strip_trailing_whitespace(text)
    return text
