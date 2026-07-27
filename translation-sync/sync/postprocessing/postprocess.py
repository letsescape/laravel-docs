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

from ..common.javascript import balanced_expression_end
from ..common.markdown import (
    _inline_code_spans,
    _strip_reference_container,
    closes_fence,
    fence_token,
    html_comment_spans,
    is_heading_line,
    markdown_links,
    mask_fenced_code_contents,
    strip_html_comments,
    strip_title_attrs,
)

_VERSION_RE = re.compile(r"\{\{\s*version\s*\}\}")
_NOTE_TYPES = {
    "note": "NOTE",
    "tip": "TIP",
    "warning": "WARNING",
    "caution": "CAUTION",
    "important": "IMPORTANT",
    "참고": "NOTE",
    "注意": "NOTE",
    "注": "NOTE",
}
_GFM_ADMONITION_RE = re.compile(
    r"^>\s*\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT)]\s*$", re.IGNORECASE
)
_GFM_ADMONITION_TYPE_RE = re.compile(
    r"^[ \t]{0,3}\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT)]",
)
_UNQUOTED_ATTRIBUTE_AT_END_RE = re.compile(
    r"(?:^|\s)[A-Za-z_:][\w:.-]*\s*=\s*[^\s\"'`{][^\s]*$"
)
_STALE_LINK_REPLACEMENTS = (
    ("controllers#actions-handled-by-resource-controller", "controllers#actions-handled-by-resource-controllers"),
    ("#actions-handled-by-resource-controller", "#actions-handled-by-resource-controllers"),
    ("database-testing#writing-factories", "database-testing#defining-model-factories"),
    ("eloquent-mutators##date-casting", "eloquent-mutators#date-casting"),
    ("errors#logging", "logging"),
    ("helpers#fluent-strings", "strings#fluent-strings"),
    ("migrations/#writing-migrations", "migrations/#creating-tables"),
    ("migrations#writing-migrations", "migrations#creating-tables"),
    ("#method-array-sort-recursive-desc", "#method-array-sort-recursive"),
    ("#agents-integration", "#agent-integration"),
)
_VERSION_SCOPED_STALE_TARGETS = {
    "controllers#actions-handled-by-resource-controller",
    "#actions-handled-by-resource-controller",
    "helpers#fluent-strings",
}
_LEGACY_VERSION_STALE_LINK_REPLACEMENTS = (
    (
        "controllers#actions-handled-by-resource-controllers",
        "controllers#actions-handled-by-resource-controller",
    ),
    (
        "#actions-handled-by-resource-controllers",
        "#actions-handled-by-resource-controller",
    ),
    ("strings#fluent-strings", "helpers#fluent-strings"),
)
_LEGACY_STALE_LINK_VERSIONS = {"8.x", "9.x"}
_V13_AGENT_REVERSE_REPLACEMENT = (
    ("#agent-integration", "#agents-integration"),
)
_RETIRED_FRAGMENT_TARGETS = {
    "#assert-similar-json",
    "#formatting-shortcode-notifications",
}
_LIST_ITEM_PREFIX_RE = re.compile(r"^[ \t]*(?:[-*+]\s+|\d+[.)]\s+)$")
_RETIRED_LIST_LABEL_RE = re.compile(
    r"(?m)^(?P<prefix>[ \t]*(?:[-*+]\s+|\d+[.)]\s+))"
    r"`(?P<label>Formatting Shortcode Notifications)`(?P<suffix>[ \t]*)$"
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
    inline_code_spans = _inline_code_spans(text)
    index = 0
    while index < len(text):
        start = lower.find("<img", index)
        if start < 0:
            out.append(text[index:])
            break
        code_span_end = next(
            (
                end
                for span_start, end, _body in inline_code_spans
                if span_start <= start < end
            ),
            None,
        )
        if code_span_end is not None:
            out.append(text[index:code_span_end])
            index = code_span_end
            continue
        after_name = start + len("<img")
        if after_name < len(text) and not (text[after_name].isspace() or text[after_name] in "/>"):
            out.append(text[index:after_name])
            index = after_name
            continue
        end = -1
        position = after_name
        while position < len(text):
            char = text[position]
            if char in ("\"", "'"):
                quote = char
                position += 1
                while position < len(text) and text[position] != quote:
                    position += 1
                if position >= len(text):
                    break
                position += 1
                continue
            if char == "{":
                expression_end = balanced_expression_end(text, position)
                if expression_end is None:
                    break
                position = expression_end
                continue
            if char == ">":
                end = position
                break
            position += 1
        if end < 0:
            out.append(text[index:])
            break

        out.append(text[index:start])
        attrs = text[after_name:end].strip()
        if attrs.endswith("/"):
            out.append(text[start : end + 1])
        elif attrs:
            separator = (
                " " if _UNQUOTED_ATTRIBUTE_AT_END_RE.search(attrs) else ""
            )
            out.append(f"<img {attrs}{separator}/>")
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
            kind = content[2:close].strip().removesuffix(":").lower()
            return kind, rest.strip()

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


def admonition_types(text: str) -> tuple[str, ...]:
    """Return normalized admonition marker types outside comments and code."""
    without_comments = strip_html_comments(text)
    normalized = _map_outside_code_blocks(
        without_comments,
        standardize_admonitions,
    )
    types: list[str] = []
    for line in normalized.splitlines():
        logical, containers = _strip_reference_container(line)
        if not containers or containers[-1] != "quote":
            continue
        match = _GFM_ADMONITION_TYPE_RE.match(logical)
        if match:
            types.append(match.group(1).upper())
    return tuple(types)


def _quote_admonition_fences(text: str) -> str:
    out: list[str] = []
    lines = text.split("\n")
    index = 0
    in_gfm_admonition = False
    outer_fence = ""

    while index < len(lines):
        line = lines[index]
        if outer_fence:
            out.append(line)
            if closes_fence(line, outer_fence):
                outer_fence = ""
            index += 1
            continue

        if _GFM_ADMONITION_RE.match(line.strip()):
            out.append(line)
            in_gfm_admonition = True
            index += 1
            continue

        if not in_gfm_admonition:
            out.append(line)
            outer_fence = fence_token(line) or ""
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


def _mask_link_excluded_spans(text: str, *, mask_inline_code: bool = True) -> str:
    chars = list(mask_fenced_code_contents(text))
    masked = "".join(chars)
    spans = [*html_comment_spans(masked)]
    if mask_inline_code:
        spans.extend(_inline_code_spans(masked))
    for start, end, _body in spans:
        for index in range(start, end):
            if chars[index] not in "\r\n":
                chars[index] = " "
    return "".join(chars)


def _stale_link_replacements(version: str) -> tuple[tuple[str, str], ...]:
    if version == "13.x":
        return (
            tuple(
                (stale, replacement)
                for stale, replacement in _STALE_LINK_REPLACEMENTS
                if stale != "#agents-integration"
            )
            + _V13_AGENT_REVERSE_REPLACEMENT
        )
    if version not in _LEGACY_STALE_LINK_VERSIONS:
        return _STALE_LINK_REPLACEMENTS
    return (
        tuple(
            (stale, replacement)
            for stale, replacement in _STALE_LINK_REPLACEMENTS
            if stale not in _VERSION_SCOPED_STALE_TARGETS
        )
        + _LEGACY_VERSION_STALE_LINK_REPLACEMENTS
    )


def _canonical_stale_link_target(target: str, version: str) -> str | None:
    if target in _RETIRED_FRAGMENT_TARGETS:
        return None
    if "://" in target and not target.startswith("https://laravel.com/docs/"):
        return target
    canonical = target
    for stale, replacement in _stale_link_replacements(version):
        if canonical.endswith(stale):
            return canonical[: -len(stale)] + replacement
    return canonical


def _is_standalone_list_link(text: str, start: int, end: int) -> bool:
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end < 0:
        line_end = len(text)
    return bool(_LIST_ITEM_PREFIX_RE.fullmatch(text[line_start:start])) and not text[
        end:line_end
    ].strip()


def normalize_retired_list_labels(text: str) -> str:
    """Remove a prior-run inline-code wrapper from a retired list label."""
    masked = _mask_link_excluded_spans(text, mask_inline_code=False)
    out: list[str] = []
    cursor = 0
    for match in _RETIRED_LIST_LABEL_RE.finditer(masked):
        out.append(text[cursor : match.start()])
        out.append(match.group("prefix") + match.group("label") + match.group("suffix"))
        cursor = match.end()
    out.append(text[cursor:])
    return "".join(out)


def normalize_stale_link_targets(text: str, version: str) -> str:
    """Rewrite known upstream stale destinations without touching code/comments."""
    masked = _mask_link_excluded_spans(text)
    out: list[str] = []
    cursor = 0
    for link in markdown_links(masked):
        target = _canonical_stale_link_target(link.target, version)
        if target == link.target:
            continue
        out.append(text[cursor : link.start])
        if target is None:
            out.append(
                link.label
                if _is_standalone_list_link(text, link.start, link.end)
                else f"`{link.label}`"
            )
        else:
            image = "!" if link.image else ""
            out.append(f"{image}[{link.label}]({target}{link.title})")
        cursor = link.end
    out.append(text[cursor:])
    return "".join(out)


def replace_version(text: str, version: str) -> str:
    return _VERSION_RE.sub(version, text)


def restore_placeholders(text: str, placeholders: Mapping[str, str]) -> str:
    for key, original in placeholders.items():
        text = text.replace(key, original)
    return text


def strip_trailing_whitespace(text: str) -> str:
    out: list[str] = []
    in_code = False
    fence = ""
    for line in text.split("\n"):
        token = fence_token(line)
        was_in_code = in_code
        if token:
            if not in_code:
                in_code = True
                fence = token
            elif closes_fence(line, fence):
                in_code = False
                fence = ""

        stripped = line.rstrip(" \t")
        if (
            not was_in_code
            and token is None
            and not is_heading_line(stripped)
            and stripped
            and line.endswith("  ")
        ):
            out.append(stripped + "  ")
        else:
            out.append(stripped)
    return "\n".join(out)


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


def _postprocess_markdown_body(text: str, version: str) -> str:
    text = replace_version(text, version)
    text = img_self_closing(text)
    text = standardize_admonitions(text)
    text = strip_title_attrs(text)
    text = normalize_stale_link_targets(text, version)
    text = normalize_retired_list_labels(text)
    text = escape_html_comments(text)
    return text


def postprocess(text: str, version: str, placeholders: Mapping[str, str]) -> str:
    text = _map_outside_code_blocks(
        text, lambda body: _postprocess_markdown_body(body, version)
    )
    text = _quote_admonition_fences(text)
    text = restore_placeholders(text, placeholders)
    text = strip_trailing_whitespace(text)
    return text
