"""Targeted repair helpers for preserved Markdown markup.

These helpers do not translate prose. They only restore markup that must stay
identical to the English source: heading lines and Markdown link labels/targets.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterator

from ..common.markdown import (
    closes_fence,
    fence_token,
    is_heading_line,
    strip_html_comments,
    strip_title_attr_line,
)

_MARKDOWN_LINK_RE = re.compile(
    r"(!?)\[([^\]\n]*)]\(([^)\s]+)((?:\s+\"[^\"]*\")?)\)"
)


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

    return _replace_links(original_line, state.source_links)


def _ensure_exhausted(iterator: Iterator, message: str) -> None:
    try:
        next(iterator)
    except StopIteration:
        return
    raise RepairError(message)


def repair_preserved_markup(source: str, translated: str) -> RepairResult:
    """Restore heading lines and links from source into translated Markdown.

    The function only edits non-comment, non-code areas. It fails closed when the
    translated document has a different number of headings or Markdown links.
    """
    state = _RepairState(
        source_headings=iter(_heading_lines(source)),
        source_links=iter(_links(source)),
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

    return RepairResult(text="".join(out), changed=changed)
