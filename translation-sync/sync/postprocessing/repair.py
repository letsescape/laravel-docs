"""Targeted repair helpers for preserved Markdown markup.

These helpers do not translate prose. They only restore markup that must stay
identical to the English source: headings, Markdown links, and inline code.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterator

from ..common.markdown import (
    closes_fence,
    fence_token,
    is_heading_line,
    is_named_anchor_line,
    strip_html_comments,
    strip_title_attr_line,
)

_MARKDOWN_LINK_RE = re.compile(
    r"(!?)\[([^\]\n]*)]\(([^)\s]+)((?:\s+\"[^\"]*\")?)\)"
)
_INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
_LIST_ITEM_RE = re.compile(r"^(\s*)([-*+])(\s+)(\S.*)$")


class RepairError(ValueError):
    """Raised when source and translated Markdown are not structurally aligned."""


@dataclass(frozen=True)
class RepairResult:
    text: str
    changed: bool


@dataclass
class _RepairState:
    source_headings: Iterator[str]
    source_links: Iterator[tuple[str, str, str]]
    source_inline_codes: list[str] = field(default_factory=list)
    source_inline_index: int = 0
    in_code: bool = False
    fence: str = ""
    in_comment: bool = False


def _split_line_ending(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    if line.endswith("\r"):
        return line[:-1], "\r"
    return line, ""


def _heading_lines(text: str) -> list[str]:
    headings: list[str] = []
    for line in strip_html_comments(_without_code_blocks(text)).splitlines():
        if is_heading_line(line):
            headings.append(strip_title_attr_line(line).strip())
    return headings


def _links(text: str) -> list[tuple[str, str, str]]:
    return [
        (" ".join(match.group(2).split()), match.group(3), match.group(4))
        for match in _MARKDOWN_LINK_RE.finditer(
            strip_html_comments(_without_code_blocks(text))
        )
        if match.group(1) != "!"
    ]


def _inline_codes(text: str) -> list[str]:
    state = _RepairState(source_headings=iter(()), source_links=iter(()))
    codes: list[str] = []
    for line in text.splitlines():
        if _is_comment_line(line, state) or _is_code_line(line, state):
            continue
        if is_heading_line(line):
            continue
        codes.extend(match.group(1) for match in _INLINE_CODE_RE.finditer(line))
    return codes


def _without_code_blocks(text: str) -> str:
    out: list[str] = []
    in_code = False
    fence = ""
    for line in text.splitlines(keepends=True):
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
    return "".join(out)


def _replace_links(line: str, links: Iterator[tuple[str, str, str]]) -> str:
    def replace(match: re.Match[str]) -> str:
        if match.group(1) == "!":
            return match.group(0)
        try:
            label, target, title = next(links)
        except StopIteration as exc:
            raise RepairError("translated document has more Markdown links than source") from exc
        return f"{match.group(1)}[{label}]({target}{title})"

    return _MARKDOWN_LINK_RE.sub(replace, line)


def _next_inline_code(state: _RepairState) -> str:
    if state.source_inline_index >= len(state.source_inline_codes):
        raise RepairError("translated document has more inline code spans than source")
    code = state.source_inline_codes[state.source_inline_index]
    state.source_inline_index += 1
    return code


def _replace_inline_codes(line: str, state: _RepairState) -> str:
    def replace(_match: re.Match[str]) -> str:
        return f"`{_next_inline_code(state)}`"

    repaired = _INLINE_CODE_RE.sub(replace, line)
    while state.source_inline_index < len(state.source_inline_codes):
        code = state.source_inline_codes[state.source_inline_index]
        wrapped = _wrap_first_raw_inline_code(repaired, code)
        if wrapped == repaired:
            break
        state.source_inline_index += 1
        repaired = wrapped
    return repaired


def _wrap_first_raw_inline_code(line: str, code: str) -> str:
    if not code:
        return line

    out: list[str] = []
    cursor = 0
    for match in _INLINE_CODE_RE.finditer(line):
        segment = line[cursor : match.start()]
        replaced = _wrap_raw_code_in_segment(segment, code)
        if replaced != segment:
            out.append(replaced)
            out.append(line[match.start() :])
            return "".join(out)
        out.append(segment)
        out.append(match.group(0))
        cursor = match.end()

    tail = line[cursor:]
    replaced = _wrap_raw_code_in_segment(tail, code)
    out.append(replaced)
    return "".join(out)


def _wrap_raw_code_in_segment(segment: str, code: str) -> str:
    start = segment.find(code)
    while start != -1:
        end = start + len(code)
        if _has_raw_code_boundaries(segment, start, end):
            return f"{segment[:start]}`{code}`{segment[end:]}"
        start = segment.find(code, start + 1)
    return segment


def _has_raw_code_boundaries(segment: str, start: int, end: int) -> bool:
    before = segment[start - 1] if start > 0 else ""
    after = segment[end] if end < len(segment) else ""
    return not _is_identifier_char(before) and not _is_identifier_char(after)


def _is_identifier_char(char: str) -> bool:
    return char.isalnum() or char in {"_", "\\"}


def _comment_candidate(line: str) -> str:
    candidate = line.lstrip()
    while candidate.startswith(">"):
        candidate = candidate[1:].lstrip()
    return candidate


def _is_comment_line(line: str, state: _RepairState) -> bool:
    if state.in_comment:
        if "-->" in line:
            state.in_comment = False
        return True

    candidate = _comment_candidate(line)
    if not candidate.startswith("<!--"):
        return False

    state.in_comment = "-->" not in candidate
    return True


def _is_code_line(line: str, state: _RepairState) -> bool:
    token = fence_token(line)
    if token:
        if not state.in_code:
            state.in_code = True
            state.fence = token
        elif closes_fence(line, state.fence):
            state.in_code = False
            state.fence = ""
        return True

    return state.in_code


def _repair_heading_line(ending: str, state: _RepairState) -> str:
    try:
        source_heading = next(state.source_headings)
    except StopIteration as exc:
        raise RepairError("translated document has more headings than source") from exc
    return source_heading + ending


def _repair_translated_line(original_line: str, state: _RepairState) -> str:
    line, ending = _split_line_ending(original_line)

    if _is_comment_line(line, state) or _is_code_line(line, state):
        return original_line

    if is_heading_line(line):
        return _repair_heading_line(ending, state)

    return _replace_inline_codes(_replace_links(original_line, state.source_links), state)


def _ensure_exhausted(iterator: Iterator, message: str) -> None:
    try:
        next(iterator)
    except StopIteration:
        return
    raise RepairError(message)


def _ensure_inline_codes_exhausted(state: _RepairState) -> None:
    if state.source_inline_index < len(state.source_inline_codes):
        raise RepairError("translated document has fewer inline code spans than source")


def _visible_lines(text: str) -> list[str]:
    state = _RepairState(source_headings=iter(()), source_links=iter(()))
    lines: list[str] = []
    for line in text.splitlines():
        if _is_comment_line(line, state) or _is_code_line(line, state):
            continue
        lines.append(line)
    return lines


def _anchor_lines(text: str) -> list[str]:
    return [line.strip() for line in _visible_lines(text) if is_named_anchor_line(line)]


def _source_anchor_bindings(source: str) -> list[tuple[str, str | None]]:
    visible = _visible_lines(source)
    bindings: list[tuple[str, str | None]] = []
    for index, line in enumerate(visible):
        if not is_named_anchor_line(line):
            continue
        heading = None
        for next_line in visible[index + 1 :]:
            if is_named_anchor_line(next_line):
                break
            if is_heading_line(next_line):
                heading = strip_title_attr_line(next_line).strip()
                break
        bindings.append((line.strip(), heading))
    return bindings


def _find_heading_index(lines: list[str], heading: str) -> int | None:
    for index, line in enumerate(lines):
        if strip_title_attr_line(line).strip() == heading:
            return index
    return None


def _anchor_insert_index(lines: list[str], heading_index: int) -> int:
    index = heading_index
    while index > 0 and lines[index - 1].strip().startswith("<!--"):
        index -= 1
    return index


def _repair_anchor_lines(source: str, translated: str) -> RepairResult:
    source_anchors = _anchor_lines(source)
    if not source_anchors:
        return RepairResult(translated, False)
    if _anchor_lines(translated) == source_anchors:
        return RepairResult(translated, False)

    lines = translated.splitlines()
    present = set(_anchor_lines(translated))
    changed = False
    for anchor, heading in _source_anchor_bindings(source):
        if anchor in present:
            continue
        if heading is None:
            raise RepairError(f"missing translated anchor without heading: {anchor}")
        heading_index = _find_heading_index(lines, heading)
        if heading_index is None:
            raise RepairError(f"missing translated heading for anchor: {heading}")
        lines.insert(_anchor_insert_index(lines, heading_index), anchor)
        present.add(anchor)
        changed = True

    repaired = "\n".join(lines) + ("\n" if translated.endswith("\n") else "")
    if _anchor_lines(repaired) != source_anchors:
        raise RepairError("translated document anchors do not match source")
    return RepairResult(repaired, changed)


def _source_list_markers(source: str) -> list[str] | None:
    """Per-item marker prefixes (indent+marker+spacing) when `source` is a pure
    unordered list: every meaningful, non-comment, non-code line is a list item.
    Returns None otherwise."""
    markers: list[str] = []
    state = _RepairState(source_headings=iter(()), source_links=iter(()))
    for line in source.splitlines():
        if _is_comment_line(line, state) or _is_code_line(line, state):
            continue
        if not line.strip():
            continue
        match = _LIST_ITEM_RE.match(line)
        if not match:
            return None
        markers.append(f"{match.group(1)}{match.group(2)}{match.group(3)}")
    return markers or None


def restore_list_markers(source: str, translated: str) -> str:
    """Re-apply dropped unordered-list markers from a pure-list source block.

    Translation must preserve list structure, but models sometimes return a
    bulleted source list as plain paragraphs. When the source block is a pure
    list and the translated block has the same number of content lines but
    fewer list markers, prepend the source markers in order. Fails open
    (returns the input unchanged) whenever the structure cannot be mapped 1:1,
    leaving verification to flag the mismatch.
    """
    markers = _source_list_markers(source)
    if not markers:
        return translated

    lines = translated.splitlines()
    state = _RepairState(source_headings=iter(()), source_links=iter(()))
    content_indexes: list[int] = []
    already_marked = 0
    for index, line in enumerate(lines):
        if _is_comment_line(line, state) or _is_code_line(line, state):
            continue
        if not line.strip():
            continue
        content_indexes.append(index)
        if _LIST_ITEM_RE.match(line):
            already_marked += 1

    if already_marked >= len(markers):
        return translated
    if len(content_indexes) != len(markers):
        return translated

    for marker, index in zip(markers, content_indexes):
        if _LIST_ITEM_RE.match(lines[index]):
            continue
        lines[index] = f"{marker}{lines[index].lstrip()}"

    return "\n".join(lines) + ("\n" if translated.endswith("\n") else "")


def repair_preserved_markup(source: str, translated: str) -> RepairResult:
    """Restore heading lines and links from source into translated Markdown.

    The function only edits non-comment, non-code areas. It fails closed when the
    translated document has a different number of headings or Markdown links.
    """
    state = _RepairState(
        source_headings=iter(_heading_lines(source)),
        source_links=iter(_links(source)),
        source_inline_codes=_inline_codes(source),
    )
    changed = False
    out: list[str] = []

    for original_line in translated.splitlines(keepends=True):
        repaired = _repair_translated_line(original_line, state)
        changed = changed or repaired != original_line
        out.append(repaired)

    _ensure_exhausted(
        state.source_headings,
        "translated document has fewer headings than source",
    )
    _ensure_exhausted(
        state.source_links,
        "translated document has fewer Markdown links than source",
    )
    _ensure_inline_codes_exhausted(state)

    repaired = "".join(out)
    anchor_result = _repair_anchor_lines(source, repaired)
    return RepairResult(
        text=anchor_result.text,
        changed=changed or anchor_result.changed,
    )
