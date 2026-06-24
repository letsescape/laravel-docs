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
_GFM_ADMONITION_RE = re.compile(
    r"^>\s*\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT)]\s*$", re.IGNORECASE
)


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


def _standardized_note_lines(line: str) -> list[str] | None:
    note = _parse_note_line(line)
    if note is None:
        return None

    kind, rest = note
    marker = _NOTE_TYPES.get(kind)
    if marker is None:
        return None

    lines = [f"> [!{marker}]"]
    if rest:
        lines.append(f"> {rest}")
    return lines


def _continue_admonition_line(line: str) -> tuple[str, bool]:
    if not line.strip():
        return line, False
    if line.lstrip().startswith(">"):
        return line, True
    return f"> {line}", True


def standardize_admonitions(text: str) -> str:
    out: list[str] = []
    in_gfm_admonition = False
    for line in text.split("\n"):
        note_lines = _standardized_note_lines(line)
        if note_lines is not None:
            out.extend(note_lines)
            in_gfm_admonition = True
            continue
        if _GFM_ADMONITION_RE.match(line.strip()):
            out.append(line)
            in_gfm_admonition = True
            continue
        if in_gfm_admonition:
            repaired_line, in_gfm_admonition = _continue_admonition_line(line)
            out.append(repaired_line)
            continue
        out.append(line)
    return "\n".join(out)


def _quote_admonition_fences(text: str) -> str:
    out: list[str] = []
    lines = text.split("\n")
    index = 0
    in_gfm_admonition = False

    while index < len(lines):
        line = lines[index]
        if _GFM_ADMONITION_RE.match(line.strip()):
            out.append(line)
            in_gfm_admonition = True
            index += 1
            continue

        if not in_gfm_admonition:
            out.append(line)
            index += 1
            continue

        if not line.strip():
            out.append(line)
            in_gfm_admonition = False
            index += 1
            continue

        if line.lstrip().startswith(">"):
            out.append(line)
            index += 1
            continue

        token = fence_token(line)
        if token:
            opening_index = index
            while index < len(lines):
                current = lines[index]
                out.append(f"> {current}" if current else ">")
                index += 1
                if index > opening_index + 1 and closes_fence(current, token):
                    break
            continue

        repaired_line, in_gfm_admonition = _continue_admonition_line(line)
        out.append(repaired_line)
        index += 1

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
    text = _quote_admonition_fences(text)
    text = restore_placeholders(text, placeholders)
    text = strip_trailing_whitespace(text)
    return text
