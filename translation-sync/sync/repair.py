"""Targeted repair helpers for preserved Markdown markup.

These helpers do not translate prose. They only restore markup that must stay
identical to the English source: heading lines and Markdown link labels.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterator

from .markdown import (
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


def _link_labels(text: str) -> list[str]:
    return [
        " ".join(match.group(2).split())
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


def _replace_link_labels(line: str, labels: Iterator[str]) -> str:
    def replace(match: re.Match[str]) -> str:
        if match.group(1) == "!":
            return match.group(0)
        try:
            label = next(labels)
        except StopIteration as exc:
            raise RepairError("translated document has more Markdown links than source") from exc
        return f"{match.group(1)}[{label}]({match.group(3)}{match.group(4)})"

    return _MARKDOWN_LINK_RE.sub(replace, line)


def repair_preserved_markup(source: str, translated: str) -> RepairResult:
    """Restore heading lines and link labels from source into translated Markdown.

    The function only edits non-comment, non-code areas. It fails closed when the
    translated document has a different number of headings or Markdown links.
    """
    source_headings = iter(_heading_lines(source))
    source_labels = iter(_link_labels(source))
    changed = False
    out: list[str] = []
    in_code = False
    fence = ""
    in_comment = False

    for original_line in translated.splitlines(keepends=True):
        line, ending = _split_line_ending(original_line)
        stripped = line.lstrip()

        if in_comment:
            out.append(original_line)
            if "-->" in line:
                in_comment = False
            continue
        if stripped.startswith("<!--"):
            out.append(original_line)
            if "-->" not in line:
                in_comment = True
            continue

        token = fence_token(line)
        if token:
            out.append(original_line)
            if not in_code:
                in_code, fence = True, token
            elif closes_fence(line, fence):
                in_code = False
            continue
        if in_code:
            out.append(original_line)
            continue

        if is_heading_line(line):
            try:
                source_heading = next(source_headings)
            except StopIteration as exc:
                raise RepairError("translated document has more headings than source") from exc
            repaired = source_heading + ending
            changed = changed or repaired != original_line
            out.append(repaired)
            continue

        repaired = _replace_link_labels(original_line, source_labels)
        changed = changed or repaired != original_line
        out.append(repaired)

    try:
        next(source_headings)
    except StopIteration:
        pass
    else:
        raise RepairError("translated document has fewer headings than source")

    try:
        next(source_labels)
    except StopIteration:
        pass
    else:
        raise RepairError("translated document has fewer Markdown links than source")

    return RepairResult(text="".join(out), changed=changed)
