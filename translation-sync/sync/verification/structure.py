"""최종 문서 검증에서 공유하는 순수 구조 signature."""
from __future__ import annotations

import re
from dataclasses import dataclass

from ..common.markdown import front_matter_description, strip_html_comments
from .response_contract import (
    _is_legacy_pipe_table_text,
    _strip_code_blocks,
    _table_line_signature,
)


_FRONT_MATTER_KEY_RE = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$")
_LIST_ITEM_RE = re.compile(
    r"^(?P<indent>[ \t]*)"
    r"(?:(?P<bullet>[-*+])|(?P<number>\d{1,9})(?P<delimiter>[.)]))"
    r"[ \t]+(?P<body>.*)$"
)
_TASK_CHECKBOX_RE = re.compile(r"^\[([ xX])\](?:[ \t]+|$)")


@dataclass(frozen=True)
class FrontMatterContract:
    """머리말 존재 여부와 scalar 구조 서명."""

    present: bool
    valid: bool
    signature: tuple[tuple[object, ...], ...]


def _scalar_contract(
    key: str,
    first_value: str,
    continuation: list[str],
) -> tuple[tuple[object, ...], bool]:
    """머리말 key와 scalar 원문에서 구조 서명 생성."""

    synthetic = "\n".join(
        ("---", f"description: {first_value}", *continuation, "---", "")
    )
    scalar = front_matter_description(synthetic)
    if scalar is None or not scalar.valid:
        return ((key, "invalid"), False)

    # description만 번역 가능하며 scalar 형식·주석·빈 값 여부는 구조로 보존
    # title을 포함한 나머지 값은 원문 소유이므로 byte 단위로 보존
    value: object = (
        ("present" if scalar.value else "empty")
        if key == "description"
        else scalar.value
    )
    continuation_shape: tuple[object, ...]
    if key == "description":
        continuation_shape = tuple(
            (
                len(line) - len(line.lstrip(" ")),
                bool(line.strip()),
                "\t" in line[: len(line) - len(line.lstrip(" \t"))],
            )
            for line in continuation
        )
    else:
        continuation_shape = tuple(continuation)
    return (
        (
            key,
            scalar.style,
            scalar.comment,
            value,
            continuation_shape,
        ),
        True,
    )


def front_matter_contract(text: str) -> FrontMatterContract:
    """선행 YAML 머리말의 fail-closed key·scalar 구조 서명."""

    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return FrontMatterContract(False, True, ())

    closing = next(
        (
            index
            for index, line in enumerate(lines[1:], start=1)
            if line == "---"
        ),
        None,
    )
    if closing is None:
        return FrontMatterContract(True, False, ())

    signature: list[tuple[object, ...]] = []
    keys: set[str] = set()
    valid = True
    index = 1
    while index < closing:
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            signature.append(("comment-or-blank", line.rstrip()))
            index += 1
            continue
        if line[:1].isspace():
            valid = False
            signature.append(("orphan-continuation", line.rstrip()))
            index += 1
            continue
        match = _FRONT_MATTER_KEY_RE.fullmatch(line)
        if match is None:
            valid = False
            signature.append(("invalid-line", line.rstrip()))
            index += 1
            continue

        key, first_value = match.groups()
        if key in keys:
            valid = False
        keys.add(key)
        continuation: list[str] = []
        index += 1
        while index < closing and (
            not lines[index].strip() or lines[index][:1].isspace()
        ):
            continuation.append(lines[index])
            index += 1
        scalar_signature, scalar_valid = _scalar_contract(
            key,
            first_value,
            continuation,
        )
        signature.append(scalar_signature)
        valid = valid and scalar_valid

    return FrontMatterContract(True, valid, tuple(signature))


def list_structure_signature(text: str) -> tuple[tuple[object, ...], ...]:
    """보호 범위 밖 목록 표식·깊이·checkbox의 순서 서명."""

    signature: list[tuple[object, ...]] = []
    for quote_depth, content in _visible_structural_lines(text):
        match = _LIST_ITEM_RE.match(content)
        if match is None:
            continue
        marker = match.group("bullet") or (
            f"{match.group('number')}{match.group('delimiter')}"
        )
        checkbox = _TASK_CHECKBOX_RE.match(match.group("body"))
        signature.append(
            (
                "list",
                quote_depth,
                len(match.group("indent").expandtabs(4)),
                marker,
                checkbox.group(1).lower() if checkbox else "",
            )
        )
    return tuple(signature)


def table_structure_signature(text: str) -> tuple[tuple[object, ...], ...]:
    """표 행 유형·열 수·정렬 표식의 순서 서명."""

    records = _visible_structural_lines(text)
    signature: list[tuple[object, ...]] = []
    index = 0
    while index < len(records):
        quote_depth, content = records[index]
        if content.lstrip(" \t").startswith("|"):
            signature.append(
                ("table", quote_depth, *_table_line_signature(content))
            )
            index += 1
            continue
        if "|" not in content:
            index += 1
            continue

        end = index
        legacy_lines: list[str] = []
        while end < len(records):
            next_depth, next_content = records[end]
            if next_depth != quote_depth or "|" not in next_content:
                break
            legacy_lines.append(next_content)
            end += 1
        if _is_legacy_pipe_table_text("\n".join(legacy_lines)):
            signature.extend(
                (
                    "table",
                    quote_depth,
                    *_table_line_signature(line),
                )
                for line in legacy_lines
            )
        index = end
    return tuple(signature)


def blockquote_structure_signature(text: str) -> tuple[tuple[int, bool], ...]:
    """code 외부 인용 깊이와 명시적 hard break의 순서 서명."""

    return tuple(
        (quote_depth, content.endswith(("  ", "\\")))
        for quote_depth, content in _visible_structural_lines(text)
        if quote_depth and content.strip()
    )


def _visible_structural_lines(text: str) -> tuple[tuple[int, str], ...]:
    """code와 HTML 주석을 제외한 표시 구조 줄."""

    body = strip_html_comments(_strip_code_blocks(text))
    records: list[tuple[int, str]] = []
    in_front_matter = False
    list_content_indents: dict[int, int] = {}
    for index, line in enumerate(body.splitlines()):
        if index == 0 and line == "---":
            in_front_matter = True
            continue
        if in_front_matter:
            if line == "---":
                in_front_matter = False
            continue

        initial = line[: len(line) - len(line.lstrip(" \t"))]
        initial_width = len(initial.expandtabs(4))
        raw_list = _LIST_ITEM_RE.match(line)
        root_list_indent = list_content_indents.get(0)
        if (
            line.strip()
            and root_list_indent is not None
            and initial_width < root_list_indent
            and raw_list is None
        ):
            list_content_indents.pop(0, None)
            root_list_indent = None
        if (
            initial_width >= 4
            and (
                root_list_indent is None
                or initial_width < root_list_indent
            )
        ):
            # 최상위 4칸 들여쓰기는 code이며 목록 내부에서는 컨테이너 본문
            continue

        cursor = 0
        quote_depth = 0
        while True:
            whitespace_start = cursor
            while cursor < len(line) and line[cursor] in " \t":
                cursor += 1
            if cursor >= len(line) or line[cursor] != ">":
                cursor = whitespace_start
                break
            quote_depth += 1
            cursor += 1
            if cursor < len(line) and line[cursor] in " \t":
                cursor += 1
        content = line[cursor:]
        content_indent = content[: len(content) - len(content.lstrip(" \t"))]
        content_indent_width = len(content_indent.expandtabs(4))
        content_list = _LIST_ITEM_RE.match(content)
        quote_list_indent = list_content_indents.get(quote_depth)
        if (
            content.strip()
            and quote_list_indent is not None
            and content_indent_width < quote_list_indent
            and content_list is None
        ):
            list_content_indents.pop(quote_depth, None)
            quote_list_indent = None
        if (
            content_indent_width >= 4
            and (
                quote_list_indent is None
                or content_indent_width < quote_list_indent
            )
        ):
            continue
        records.append((quote_depth, content))
        if content_list is not None:
            list_content_indents[quote_depth] = len(
                content[: content_list.start("body")].expandtabs(4)
            )
        if line.strip():
            for depth in tuple(list_content_indents):
                if depth > quote_depth:
                    list_content_indents.pop(depth, None)
    return tuple(records)
