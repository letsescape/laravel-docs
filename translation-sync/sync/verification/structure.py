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


def _front_matter_entry(
    lines: list[str],
    index: int,
    closing: int,
    keys: set[str],
) -> tuple[tuple[object, ...], bool, int]:
    """머리말의 단일 주석·빈 줄·key 항목을 구조 서명으로 변환.

    Args:
        lines: 전체 문서 줄.
        index: 현재 머리말 줄 위치.
        closing: 머리말 닫는 구분자 위치.
        keys: 앞서 관찰한 key 집합.

    Returns:
        구조 서명 항목, 유효 여부, 다음 줄 위치.
    """

    line = lines[index]
    if not line.strip() or line.lstrip().startswith("#"):
        return ("comment-or-blank", line.rstrip()), True, index + 1
    if line[:1].isspace():
        return ("orphan-continuation", line.rstrip()), False, index + 1
    match = _FRONT_MATTER_KEY_RE.fullmatch(line)
    if match is None:
        return ("invalid-line", line.rstrip()), False, index + 1
    return _front_matter_scalar_entry(lines, index, closing, keys, match)


def _front_matter_scalar_entry(
    lines: list[str],
    index: int,
    closing: int,
    keys: set[str],
    match: re.Match[str],
) -> tuple[tuple[object, ...], bool, int]:
    """검증된 머리말 key 줄과 연속 scalar 줄을 구조 서명으로 변환.

    Args:
        lines: 전체 문서 줄.
        index: key 줄 위치.
        closing: 머리말 닫는 구분자 위치.
        keys: 앞서 관찰한 key 집합.
        match: key 줄 정규식 일치 결과.

    Returns:
        scalar 구조 서명, 유효 여부, 다음 줄 위치.
    """

    key, first_value = match.groups()
    unique = key not in keys
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
    return scalar_signature, unique and scalar_valid, index


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
        entry, entry_valid, index = _front_matter_entry(
            lines,
            index,
            closing,
            keys,
        )
        signature.append(entry)
        valid = valid and entry_valid

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


def _quote_content(line: str) -> tuple[int, str]:
    """줄의 인용 깊이와 인용 표식을 제외한 본문 추출.

    Args:
        line: 표시 가능한 Markdown 줄.

    Returns:
        인용 깊이와 나머지 본문.
    """

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
    return quote_depth, line[cursor:]


def _is_root_indented_code(
    line: str,
    list_content_indents: dict[int, int],
) -> bool:
    """최상위 들여쓰기 줄이 목록 본문이 아닌 코드인지 판정.

    Args:
        line: 표시 가능한 Markdown 줄.
        list_content_indents: 인용 깊이별 활성 목록 본문 들여쓰기.

    Returns:
        최상위 들여쓰기 코드 여부.
    """

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
    return initial_width >= 4 and (
        root_list_indent is None or initial_width < root_list_indent
    )


def _visible_line_record(
    line: str,
    list_content_indents: dict[int, int],
) -> tuple[int, str] | None:
    """단일 줄을 보호 범위 밖 구조 레코드로 변환.

    Args:
        line: 표시 가능한 Markdown 줄.
        list_content_indents: 인용 깊이별 활성 목록 본문 들여쓰기.

    Returns:
        인용 깊이와 본문. 들여쓰기 코드이면 ``None``.
    """

    if _is_root_indented_code(line, list_content_indents):
        return None
    quote_depth, content = _quote_content(line)
    indent = content[: len(content) - len(content.lstrip(" \t"))]
    indent_width = len(indent.expandtabs(4))
    content_list = _LIST_ITEM_RE.match(content)
    quote_list_indent = list_content_indents.get(quote_depth)
    if (
        content.strip()
        and quote_list_indent is not None
        and indent_width < quote_list_indent
        and content_list is None
    ):
        list_content_indents.pop(quote_depth, None)
        quote_list_indent = None
    if indent_width >= 4 and (
        quote_list_indent is None or indent_width < quote_list_indent
    ):
        return None
    if content_list is not None:
        list_content_indents[quote_depth] = len(
            content[: content_list.start("body")].expandtabs(4)
        )
    if line.strip():
        for depth in tuple(list_content_indents):
            if depth > quote_depth:
                list_content_indents.pop(depth, None)
    return quote_depth, content


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

        record = _visible_line_record(line, list_content_indents)
        if record is not None:
            records.append(record)
    return tuple(records)
