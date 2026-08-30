"""원문 diff hunk의 번역 결과를 annotation 포함 locale Markdown에 적용.

영어 HTML 주석을 안정된 anchor로 사용.
변경된 영어 hunk를 개별 번역한 뒤 대응하는 annotation block의 교체, 삽입 또는 삭제를 통해 기존 locale 문서에 병합.
"""
from __future__ import annotations

import re
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass, field, replace
from enum import Enum

from ..annotation.annotate import Block, split_blocks
from ..common.markdown import (
    closes_fence,
    fence_token,
    front_matter_description,
    gfm_table_row_cells,
    has_malformed_html_comment_delimiters,
    html_code_contents,
    html_comment_spans,
    html_tags,
    inline_code_contents,
    is_gfm_pipe_table,
    is_gfm_pipe_table_candidate,
    is_heading_line,
    is_named_anchor_line,
    is_non_annotatable_line,
    is_structural_html_fragment,
    is_structural_html_line,
    normalize_annotation_anchor,
    reference_definition_line_numbers,
    standalone_html_comment_line_numbers,
    strip_html_code_elements,
    strip_inline_code,
    strip_title_attr_line,
)
from ..source.diff import DiffHunk, DiffLine, hunks_between

_ADMONITION_MARKER_RE = re.compile(
    r"^>\s*\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT)]\s*$", re.IGNORECASE
)
_ANY_ADMONITION_MARKER_RE = re.compile(
    r"^>\s*\[!([A-Z][A-Z0-9_-]*)]\s*$", re.IGNORECASE
)
_BARE_INTERNAL_LINK_RE = re.compile(r"^\[[^]\n]+]\(#[^)\s]+\)$")
_LIST_ITEM_PREFIX_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
_SIDEBAR_LINK_ITEM_RE = re.compile(r"\[[^]\n]+]\([^)\s]+\)")
_SIDEBAR_CATEGORY_ITEM_RE = re.compile(r"#{1,6}\s+\S[^\n]*")


def _is_sidebar_structure_line(line: str) -> bool:
    """링크 label 또는 카테고리 heading만 있는 사이드바 구조 라인 여부."""

    stripped, marker_count = _LIST_ITEM_PREFIX_RE.subn("", line)
    if not marker_count:
        return False
    return bool(
        _SIDEBAR_LINK_ITEM_RE.fullmatch(stripped)
        or _SIDEBAR_CATEGORY_ITEM_RE.fullmatch(stripped)
    )
_LEGACY_ADMONITION_RE = re.compile(
    r"^>\s*(?:"
    r"\{(?P<braced>note|tip|warning|caution|important|참고|注意)\}"
    r"|\*\*(?P<strong>note|tip|warning|caution|important|참고|注意)"
    r"(?::\*\*|\*\*:)"
    r")\s*(?P<body>.*)$",
    re.IGNORECASE,
)
_LEGACY_ADMONITION_TYPES = {
    "note": "NOTE",
    "tip": "TIP",
    "warning": "WARNING",
    "caution": "CAUTION",
    "important": "IMPORTANT",
    "참고": "NOTE",
    "注意": "NOTE",
}
_TOC_LINK_RE = re.compile(r"^\s*[-*]\s+\[[^\]\n]*\]\(#([^)\s]+)\)\s*$")
_NAMED_ANCHOR_NAME_RE = re.compile(r'name="([^"]+)"')


class PatchError(ValueError):
    """diff hunk를 기존 번역문에 적용할 수 없는 patch 오류."""


class PlanState(Enum):
    """계획 상태."""

    CREATE = "create"
    UNGUARDED = "unguarded"
    SOURCE = "source"
    TARGET = "target"


@dataclass(frozen=True)
class BlockChange:
    """원문 delta와 해당 변경이 속한 전체 Markdown block의 결합.

    ``old_lines``와 ``new_lines``는 선택적 원문 정규화 이후의 effective delta.
    번역과 locale 교체에 사용하는 전체 block은 ``old_source``와 ``new_source``에 보존.
    두 개념의 분리를 통해 block 확장이 한 줄 추가를 전체 추가 diff로 바꾸는 문제 방지.
    """

    old_lines: tuple[str, ...]
    new_lines: tuple[str, ...]
    before_context: str | None
    after_context: str | None
    old_linenos: tuple[int, ...] = ()
    new_linenos: tuple[int, ...] = ()
    before_old_lineno: int | None = None
    before_new_lineno: int | None = None
    after_old_lineno: int | None = None
    after_new_lineno: int | None = None
    old_source: str | None = None
    old_anchors: tuple[str, ...] = ()
    old_block_ordinal: int | None = None
    old_anchor_occurrences: int | None = None
    old_block_start: int | None = None
    old_block_end: int | None = None
    old_previous_anchor: str | None = None
    old_previous_anchor_ordinal: int | None = None
    old_next_anchor: str | None = None
    old_next_anchor_ordinal: int | None = None
    new_source: str | None = None
    new_anchor: str | None = None
    new_anchors: tuple[str, ...] = ()
    new_block_ordinal: int | None = None
    new_anchor_occurrences: int | None = None
    new_block_start: int | None = None
    new_block_end: int | None = None
    new_previous_anchor: str | None = None
    new_next_anchor: str | None = None
    # 코드 블록 내부 변경은 번역하지 않고 원문 블록 전체로 교체
    code_block: CodeChange | None = None
    inserted_code_block_index: int | None = None
    inserted_code_block: str | None = None
    deleted_code_block_index: int | None = None
    deleted_code_block: str | None = None
    # 번역된 로캘 행도 찾을 수 있도록 구조 위치로 주소화한 표 행 변경
    table_row: TableRowChange | None = None

    @property
    def needs_translation(self) -> bool:
        """provider 번역이 필요한 segment인지 여부."""

        if self.code_block is not None:
            return False
        return bool(_meaningful_lines(self.new_lines)) or bool(
            self.new_source and self.new_source.strip()
        )

    @property
    def provider_free(self) -> bool:
        """provider 호출 없이 결정할 수 있는 segment인지 여부."""

        rendered = [
            line for line in source_text(self).splitlines() if line.strip()
        ]
        if rendered and all(is_structural_html_line(line) for line in rendered):
            return True
        if not self.new_source:
            return False
        if self.inserted_code_block is not None:
            return True
        if _is_fenced_code_source(self.new_source):
            return True
        if self.is_named_anchor_change:
            return True
        if self.is_inline_code_identifier_list:
            return True
        lines = [line.strip() for line in self.new_source.splitlines() if line.strip()]
        if bool(lines) and all(
            _BARE_INTERNAL_LINK_RE.fullmatch(line) for line in lines
        ):
            return True
        return bool(lines) and all(
            _is_sidebar_structure_line(line) for line in lines
        )

    @property
    def is_inline_code_identifier_list(self) -> bool:
        """inline code identifier list 여부."""

        return bool(self.new_source) and _is_inline_code_identifier_list(
            self.new_source
        )

    @property
    def is_named_anchor_change(self) -> bool:
        """named anchor 변경 여부."""

        old_lines = _meaningful_lines(self.old_lines)
        new_lines = _meaningful_lines(self.new_lines)
        lines = old_lines + new_lines
        return (
            bool(lines)
            and len(old_lines) <= 1
            and len(new_lines) <= 1
            and all(is_named_anchor_line(line) for line in lines)
        )

    @property
    def is_admonition_marker_change(self) -> bool:
        """admonition marker 변경 여부."""

        old_lines = _meaningful_lines(self.old_lines)
        new_lines = _meaningful_lines(self.new_lines)
        return (
            len(old_lines) == 1
            and len(new_lines) == 1
            and bool(_ADMONITION_MARKER_RE.fullmatch(old_lines[0].strip()))
            and bool(_ADMONITION_MARKER_RE.fullmatch(new_lines[0].strip()))
        )

    @property
    def is_deletion(self) -> bool:
        """deletion 여부."""

        if self.code_block is not None:
            return False
        has_old_source = bool(self.old_source or _meaningful_lines(self.old_lines))
        return has_old_source and not self.needs_translation

    @property
    def is_block_range(self) -> bool:
        """블록 range 여부."""

        return len(self.old_anchors) > 1 or len(self.new_anchors) > 1


@dataclass(frozen=True)
class CodeChange:
    """단일 fenced code block 내부의 변경.

    code는 번역 없이 원문에서 그대로 복사.
    변경 block을 문서 순서의 이전·신규 index로 찾은 뒤 전체 block을 신규 원문 block으로 교체.
    locale code와 영어 원문의 byte 동일성 및 재실행 idempotency 보장.

    ``anchors``는 새로 추가된 줄을 제외한 변경되지 않은 block 줄.
    탐색한 block이 모든 anchor를 포함할 때만 교체.
    순서만 바뀐 동등 code는 canonical 상태로 판정하고 다른 divergence는 ``_code_plan_state``에서 거부.
    """

    block_index: int
    new_block: str
    anchors: tuple[str, ...]
    old_block_index: int | None = None
    old_block: str | None = None
    old_block_count: int = 0
    new_block_count: int = 0


@dataclass(frozen=True)
class TableRowChange:
    """구조 위치로 주소화된 단일 변경 table row.

    ``table_ordinal``은 code fence 외부 table 순서, ``table_count``와 ``row_count``는 원문 cardinality, ``row_ordinal``은 separator가 아닌 row 사이의 변경 row 순서.
    locale 전용 table이나 row가 구조 주소를 다른 내용으로 이동시키는 경우 거부.
    """

    table_ordinal: int
    row_ordinal: int
    row_count: int
    table_count: int


@dataclass(frozen=True)
class NamedSectionSignature:
    """이름이 지정된 section의 안정된 구조 서명."""

    anchor: str
    source_anchors: tuple[str, ...]


@dataclass(frozen=True)
class NamedSectionReorder:
    """provider 호출 없이 적용할 named section 순서 변경."""

    old_order: tuple[NamedSectionSignature, ...]
    new_order: tuple[NamedSectionSignature, ...]
    new_separators: tuple[str, ...]
    reorder_prefix_links: bool = False


@dataclass(frozen=True)
class CreateBlock:
    """신규 원문 문서의 분할 불가능한 단일 owner 단위."""

    kind: str
    source: str
    leading: str
    provider_required: bool


@dataclass(frozen=True)
class PatchPlan:
    """단일 이전·신규 원문 쌍에서 파생된 순서가 보존된 block 변경."""

    changes: tuple[BlockChange, ...]
    old_source_anchors: tuple[str, ...] | None = None
    new_source_anchors: tuple[str, ...] | None = None
    old_code_blocks: tuple[str, ...] | None = None
    new_code_blocks: tuple[str, ...] | None = None
    old_source_comments: tuple[SourceComment, ...] = ()
    new_source_comments: tuple[SourceComment, ...] = ()
    named_section_reorder: NamedSectionReorder | None = None
    old_front_matter: str | None = None
    new_front_matter: str | None = None
    create_blocks: tuple[CreateBlock, ...] = ()
    create_suffix: str = ""
    is_create: bool = False

    @property
    def is_noop(self) -> bool:
        """noop 여부."""

        return (
            not self.is_create
            and not self.changes
            and self.named_section_reorder is None
            and self.old_source_anchors == self.new_source_anchors
            and self.old_code_blocks == self.new_code_blocks
            and self.old_source_comments == self.new_source_comments
            and self.old_front_matter == self.new_front_matter
        )


@dataclass(frozen=True)
class AnnotatedBlock:
    """원문 annotation과 번역 본문을 포함한 locale block."""

    start: int
    end: int
    comment: str
    text: str


@dataclass(frozen=True)
class SourceBlock:
    """줄 범위와 annotation anchor를 보존한 원문 block."""

    start_lineno: int
    end_lineno: int
    comment: str
    text: str


@dataclass(frozen=True)
class SourceComment:
    """원문에 작성된 HTML 주석과 원문 block 사이의 위치."""

    body: str
    anchor_position: int
    raw: str
    placement: str


@dataclass(frozen=True)
class _NamedSection:
    """이름 anchor로 구분한 내부 section 범위."""

    core: str
    separator: str
    signature: NamedSectionSignature


def build_create_plan(source_text: str) -> PatchPlan:
    """신규 원문 문서를 순서가 보존된 분할 불가능 owner 단위로 분해."""

    _validate_create_source(source_text)
    front_matter = _front_matter_text(source_text)
    source_lines = source_text.splitlines(keepends=True)
    plain_lines = source_text.splitlines()
    ranges = _create_owner_ranges(source_text, plain_lines)
    create_blocks, cursor = _create_blocks_from_ranges(
        source_lines,
        plain_lines,
        ranges,
    )
    if any(line.strip() for line in source_lines[cursor:]):
        raise PatchError("source contains an unsupported create owner block")
    return PatchPlan(
        changes=(),
        new_front_matter=front_matter,
        create_blocks=tuple(create_blocks),
        create_suffix="".join(source_lines[cursor:]),
        is_create=True,
    )


def _validate_create_source(source_text: str) -> None:
    """신규 원문의 주석·admonition·머리말 지원 범위 검증.

    Args:
        source_text: 신규 영어 원문.

    Raises:
        PatchError: 지원하지 않는 원문 구조 발견.
    """

    if has_malformed_html_comment_delimiters(source_text):
        raise PatchError("malformed standalone source HTML comment")
    _require_supported_admonition_markers(source_text)
    front_matter = _front_matter_text(source_text)
    if front_matter is not None:
        _require_supported_front_matter(front_matter)


def _create_owner_ranges(
    source_text: str,
    plain_lines: list[str],
) -> list[tuple[int, int, str]]:
    """신규 원문을 분할 불가능 owner 줄 범위로 분해.

    Args:
        source_text: 신규 영어 원문.
        plain_lines: 줄바꿈을 제외한 원문 줄.

    Returns:
        시작·끝 줄과 기본 블록 유형 목록.
    """

    comment_ranges = _standalone_source_comment_ranges(source_text)
    ranges: list[tuple[int, int, str]] = []
    for block in split_blocks(plain_lines):
        ranges.extend(_block_owner_ranges(block, comment_ranges))
    ranges.extend((start, end, "source_comment") for start, end in comment_ranges)
    return sorted(
        item
        for item in ranges
        if any(line.strip() for line in plain_lines[item[0] : item[1]])
    )


def _block_owner_ranges(
    block: Block,
    comment_ranges: tuple[tuple[int, int], ...],
) -> list[tuple[int, int, str]]:
    """Markdown 블록에서 독립 원문 주석을 제외한 owner 범위 추출.

    Args:
        block: ``split_blocks``가 반환한 Markdown 블록.
        comment_ranges: 독립 원문 주석 줄 범위.

    Returns:
        주석 사이의 시작·끝 줄과 블록 유형.
    """

    ranges: list[tuple[int, int, str]] = []
    cursor = block.start
    for comment_start, comment_end in comment_ranges:
        if comment_end <= cursor or comment_start >= block.end:
            continue
        if cursor < comment_start:
            ranges.append((cursor, comment_start, block.kind))
        cursor = max(cursor, comment_end)
    if cursor < block.end:
        ranges.append((cursor, block.end, block.kind))
    return ranges


def _create_blocks_from_ranges(
    source_lines: list[str],
    plain_lines: list[str],
    ranges: list[tuple[int, int, str]],
) -> tuple[list[CreateBlock], int]:
    """owner 줄 범위를 신규 문서 patch 블록으로 변환.

    Args:
        source_lines: 줄바꿈을 보존한 원문 줄.
        plain_lines: 줄바꿈을 제외한 원문 줄.
        ranges: 시작·끝 줄과 기본 블록 유형 목록.

    Returns:
        생성 블록 목록과 마지막 소비 줄 위치.

    Raises:
        PatchError: owner 범위가 겹치거나 지원하지 않는 공백 외 내용 발견.
    """

    create_blocks: list[CreateBlock] = []
    cursor = 0
    for start, end, base_kind in ranges:
        if start < cursor:
            raise PatchError("overlapping create owner blocks")
        if any(line.strip() for line in source_lines[cursor:start]):
            raise PatchError("source contains an unsupported create owner block")
        source = "".join(source_lines[start:end])
        kind = _create_block_kind(base_kind, source)
        if kind == "table":
            _require_rectangular_create_table(source)
        create_blocks.append(
            CreateBlock(
                kind=kind,
                source=source,
                leading="".join(source_lines[cursor:start]),
                provider_required=_create_block_requires_provider(kind, source),
            )
        )
        cursor = end
    return create_blocks, cursor


def _create_block_kind(base_kind: str, source: str) -> str:
    """기본 분류와 원문 형태로 신규 블록 유형 결정."""

    if base_kind != "text":
        return base_kind
    stripped = source.lstrip()
    if is_gfm_pipe_table_candidate(source):
        return "table"
    if stripped.startswith(">"):
        return "admonition"
    if _LIST_ITEM_PREFIX_RE.match(stripped):
        return "list"
    if stripped.startswith("<"):
        return "html"
    return "prose"


def _create_block_requires_provider(kind: str, source: str) -> bool:
    """신규 블록에 번역 제공자 호출이 필요한지 판정."""

    if kind in {
        "frontmatter",
        "source_comment",
        "heading",
        "code",
        "anchor",
        "structure",
    }:
        return False
    if kind == "list" and _is_inline_code_identifier_list(source):
        return False
    lines = [line.strip() for line in source.splitlines() if line.strip()]
    if kind == "list" and lines and all(
        _BARE_INTERNAL_LINK_RE.fullmatch(_LIST_ITEM_PREFIX_RE.sub("", line))
        for line in lines
    ):
        return False
    if lines and all(_BARE_INTERNAL_LINK_RE.fullmatch(line) for line in lines):
        return False
    if lines and all(_is_sidebar_structure_line(line) for line in lines):
        return False
    return True


def _standalone_source_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """독립된 원문 HTML 주석의 0 기반 줄 범위."""

    lines = text.splitlines(keepends=True)
    source_comment_lines = standalone_html_comment_line_numbers(text)
    front_matter_lines = _front_matter_line_numbers(text)
    ranges: list[tuple[int, int]] = []
    for start in _comment_starts(lines):
        if (
            start + 1 not in source_comment_lines
            or start + 1 in front_matter_lines
        ):
            continue
        end, _body = _read_comment(lines, start)
        closing = lines[end - 1]
        suffix = closing[closing.find("-->") + 3 :].strip()
        if suffix:
            raise PatchError("source HTML comment must be standalone")
        ranges.append((start, end))
    covered = {
        lineno
        for start, end in ranges
        for lineno in range(start + 1, end + 1)
    }
    expected = set(source_comment_lines) - front_matter_lines
    if covered != expected:
        raise PatchError("source HTML comment must be standalone")
    return tuple(ranges)


def _render_create_plan(plan: PatchPlan, translated_blocks: list[str]) -> str:
    """신규 문서 계획과 번역 결과를 하나의 문서로 조립."""

    expected = sum(block.provider_required for block in plan.create_blocks)
    if len(translated_blocks) != expected:
        raise PatchError(
            f"translation count mismatch: expected {expected}, got {len(translated_blocks)}"
        )
    translated = iter(translated_blocks)
    output: list[str] = []
    for block in plan.create_blocks:
        output.append(block.leading)
        rendered = (
            next(translated)
            if block.provider_required
            else _render_deterministic_create_block(block)
        )
        output.append(_with_source_line_ending(rendered, block.source))
    output.append(plan.create_suffix)
    return _ensure_single_eof_newline("".join(output))


def _render_deterministic_create_block(block: CreateBlock) -> str:
    """번역 호출이 필요 없는 신규 블록 생성."""

    if block.kind != "heading":
        return block.source
    heading = strip_title_attr_line(block.source.rstrip("\r\n"))
    comment = _normalize_text(heading).replace("*/", "*&#47;").replace(
        "-->", "--&gt;"
    )
    ending = "\r\n" if block.source.endswith("\r\n") else "\n"
    source_heading = block.source.rstrip("\r\n")
    return f"<!-- {comment} -->{ending}{source_heading}"


def _with_source_line_ending(rendered: str, source: str) -> str:
    """생성된 블록에 원문의 끝 줄바꿈 형식 적용."""

    ending = (
        "\r\n"
        if source.endswith("\r\n")
        else "\n"
        if source.endswith("\n")
        else ""
    )
    return rendered.rstrip("\r\n") + ending


def reconstruct_source_pair(
    hunks: tuple[DiffHunk, ...],
    source_text: str,
) -> tuple[str, str]:
    """diff hunk를 역적용해 이전·현재 원문 쌍 재구성.

    Args:
        hunks: 현재 원문에 적용된 통합 diff 변경 구간.
        source_text: 변경 이후의 전체 원문.

    Returns:
        변경 이전 원문과 현재 원문 쌍.
    """

    source_lines = source_text.splitlines()
    old_source_lines = _reverse_apply_hunks(source_lines, hunks)
    return _lines_text(old_source_lines, source_text), source_text


@dataclass(frozen=True)
class _PlanSources:
    """patch 계획에 반복 사용되는 이전·현재 원문 구조."""

    old_text: str
    new_text: str
    old_lines: list[str]
    new_lines: list[str]
    old_front_matter: str | None
    new_front_matter: str | None
    old_blocks: list[SourceBlock]
    new_blocks: list[SourceBlock]
    old_regions: list[tuple[int, int]]
    new_regions: list[tuple[int, int]]
    old_control_lines: set[int]
    new_control_lines: set[int]


def _plan_sources(old_text: str, new_text: str) -> _PlanSources:
    """이전·현재 원문에서 patch 계획용 구조 정보 구성.

    Args:
        old_text: 변경 이전 영어 원문.
        new_text: 변경 이후 영어 원문.

    Returns:
        줄·블록·code 영역·제어 줄을 포함한 계획 원문 상태.
    """

    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()
    old_front_matter = _front_matter_text(old_text)
    new_front_matter = _front_matter_text(new_text)
    if old_front_matter != new_front_matter and new_front_matter is not None:
        _require_supported_front_matter(new_front_matter)
    old_comments = _source_comment_line_numbers(old_text)
    new_comments = _source_comment_line_numbers(new_text)
    return _PlanSources(
        old_text=old_text,
        new_text=new_text,
        old_lines=old_lines,
        new_lines=new_lines,
        old_front_matter=old_front_matter,
        new_front_matter=new_front_matter,
        old_blocks=_source_blocks(old_text),
        new_blocks=_source_blocks(new_text),
        old_regions=_code_fence_regions(old_lines),
        new_regions=_code_fence_regions(new_lines),
        old_control_lines=old_comments | _front_matter_line_numbers(old_text),
        new_control_lines=new_comments | _front_matter_line_numbers(new_text),
    )


def _normalized_patch_plan(
    hunks: tuple[DiffHunk, ...],
    old_text: str,
    new_text: str,
    *,
    normalize_source: Callable[[str], str] | None,
    normalize_source_pair: Callable[[str, str], tuple[str, str]] | None,
) -> PatchPlan | None:
    """요청된 원문 정규화를 적용한 재귀 patch 계획 생성.

    Args:
        hunks: 현재 원문에 적용된 통합 diff 변경 구간.
        old_text: 변경 이전 영어 원문.
        new_text: 변경 이후 영어 원문.
        normalize_source: 문서별 단일 원문 정규화 함수.
        normalize_source_pair: 이전·현재 원문 쌍 정규화 함수.

    Returns:
        정규화가 요청됐으면 재구성한 계획, 아니면 ``None``.

    Raises:
        PatchError: 정규화 계약이 잘못되었거나 두 계약을 동시에 지정.
    """

    if normalize_source is not None and normalize_source_pair is not None:
        raise PatchError("specify only one source normalizer contract")
    if normalize_source_pair is not None:
        normalized = normalize_source_pair(old_text, new_text)
        if (
            not isinstance(normalized, tuple)
            or len(normalized) != 2
            or not all(isinstance(item, str) for item in normalized)
        ):
            raise PatchError("source pair normalizer must return two strings")
        normalized_old, normalized_new = normalized
        return build_plan(hunks_between(normalized_old, normalized_new), normalized_new)
    if normalize_source is not None:
        normalized_old = normalize_source(old_text)
        normalized_new = normalize_source(new_text)
        return build_plan(hunks_between(normalized_old, normalized_new), normalized_new)
    return None


def _named_reorder_patch_plan(
    sources: _PlanSources,
    reorder: NamedSectionReorder | None,
) -> PatchPlan | None:
    """이름 anchor section 재정렬 전용 patch 계획 생성.

    Args:
        sources: 이전·현재 원문 구조.
        reorder: 재정렬된 section 서명 또는 ``None``.

    Returns:
        section 재정렬 계획. 일반 diff면 ``None``.
    """

    if reorder is None:
        return None
    return PatchPlan(
        changes=(),
        old_source_anchors=tuple(
            block.comment for block in _plan_source_blocks(sources.old_blocks)
        ),
        new_source_anchors=tuple(
            block.comment for block in _plan_source_blocks(sources.new_blocks)
        ),
        old_code_blocks=_code_blocks_from_regions(
            sources.old_lines,
            sources.old_regions,
        ),
        new_code_blocks=_code_blocks_from_regions(
            sources.new_lines,
            sources.new_regions,
        ),
        old_source_comments=_source_comment_locations(sources.old_text),
        new_source_comments=_source_comment_locations(sources.new_text),
        named_section_reorder=reorder,
        old_front_matter=sources.old_front_matter,
        new_front_matter=sources.new_front_matter,
    )


@dataclass
class _SegmentAccumulator:
    """단일 hunk의 연속 add·delete 줄을 초기 segment로 누적."""

    segments: list[BlockChange]
    before_context: DiffLine | None = None
    old_lines: list[str] = field(default_factory=list)
    new_lines: list[str] = field(default_factory=list)
    old_linenos: list[int] = field(default_factory=list)
    new_linenos: list[int] = field(default_factory=list)

    @property
    def pending(self) -> bool:
        """확정하지 않은 add·delete 줄 존재 여부."""

        return bool(self.old_lines or self.new_lines)

    def flush(self, after_context: DiffLine | None = None) -> None:
        """누적 diff 줄을 하나의 초기 segment로 확정.

        Args:
            after_context: 변경 바로 다음 문맥 줄.
        """

        if self.pending:
            self.segments.append(
                BlockChange(
                    old_lines=tuple(self.old_lines),
                    new_lines=tuple(self.new_lines),
                    before_context=_context_text(self.before_context),
                    after_context=_context_text(after_context),
                    old_linenos=tuple(self.old_linenos),
                    new_linenos=tuple(self.new_linenos),
                    before_old_lineno=(
                        self.before_context.old_lineno if self.before_context else None
                    ),
                    before_new_lineno=(
                        self.before_context.new_lineno if self.before_context else None
                    ),
                    after_old_lineno=after_context.old_lineno if after_context else None,
                    after_new_lineno=after_context.new_lineno if after_context else None,
                )
            )
            self.old_lines.clear()
            self.new_lines.clear()
            self.old_linenos.clear()
            self.new_linenos.clear()
        if after_context is not None:
            self.before_context = after_context

    def consume(
        self,
        line: DiffLine,
        *,
        old_control_lines: set[int],
        new_control_lines: set[int],
    ) -> None:
        """hunk 줄을 제어 줄·문맥·add·delete 규칙으로 누적.

        Args:
            line: 통합 diff 줄.
            old_control_lines: 이전 원문의 annotation·머리말 줄.
            new_control_lines: 현재 원문의 annotation·머리말 줄.
        """

        if line.old_lineno in old_control_lines or line.new_lineno in new_control_lines:
            if self.pending:
                self.flush()
            self.before_context = None
            return
        if line.kind == "context":
            context = _normalize_text(line.text)
            if self.pending and context:
                self.flush(line)
            elif context:
                self.before_context = line
            return
        if line.kind == "delete":
            self.old_lines.append(line.text)
            if line.old_lineno is not None:
                self.old_linenos.append(line.old_lineno)
        elif line.kind == "add":
            self.new_lines.append(line.text)
            if line.new_lineno is not None:
                self.new_linenos.append(line.new_lineno)


def _hunk_without_control_lines(hunk: DiffHunk, sources: _PlanSources) -> DiffHunk:
    """annotation·머리말 제어 줄을 제외한 hunk 생성.

    Args:
        hunk: 원본 통합 diff hunk.
        sources: 이전·현재 원문 구조.

    Returns:
        patch 대상 줄만 포함한 hunk.
    """

    return DiffHunk(
        old_start=hunk.old_start,
        old_count=hunk.old_count,
        new_start=hunk.new_start,
        new_count=hunk.new_count,
        lines=tuple(
            line
            for line in hunk.lines
            if line.old_lineno not in sources.old_control_lines
            and line.new_lineno not in sources.new_control_lines
        ),
    )


def _initial_segments(
    hunks: tuple[DiffHunk, ...],
    sources: _PlanSources,
) -> list[BlockChange]:
    """통합 diff를 code 영역 또는 연속 줄 단위 초기 segment로 변환.

    Args:
        hunks: 현재 원문에 적용된 통합 diff 변경 구간.
        sources: 이전·현재 원문 구조.

    Returns:
        원문 블록 확장 전 초기 변경 segment.
    """

    segments: list[BlockChange] = []
    for hunk in hunks:
        if _hunk_has_code_fence_change(
            hunk,
            old_ignored=sources.old_control_lines,
            new_ignored=sources.new_control_lines,
        ):
            segments.append(
                _hunk_region_segment(
                    _hunk_without_control_lines(hunk, sources),
                    sources.new_lines,
                )
            )
            continue
        accumulator = _SegmentAccumulator(segments)
        for line in hunk.lines:
            accumulator.consume(
                line,
                old_control_lines=sources.old_control_lines,
                new_control_lines=sources.new_control_lines,
            )
        accumulator.flush()
    return [segment for segment in segments if segment.old_lines or segment.new_lines]


def _expanded_code_segment(
    segment: BlockChange,
    filtered: list[BlockChange],
    sources: _PlanSources,
    emitted_regions: set[int],
) -> BlockChange | None:
    """code fence 영역 변경을 블록 전체 교체 segment로 확장.

    Args:
        segment: 현재 초기 변경 segment.
        filtered: 전체 초기 변경 segment.
        sources: 이전·현재 원문 구조.
        emitted_regions: 이미 확정한 현재 code 영역 순번.

    Returns:
        처음 방문한 code 영역의 확장 segment. 일반 변경 또는 중복이면 ``None``.
    """

    region, old_region = _code_region_indexes(
        segment,
        sources.new_regions,
        sources.old_regions,
    )
    if region is None or region >= len(sources.new_regions):
        return None
    if region in emitted_regions:
        return None
    emitted_regions.add(region)
    group = [
        other
        for other in filtered
        if _code_region_indexes(
            other,
            sources.new_regions,
            sources.old_regions,
        )[0]
        == region
    ]
    candidates = {
        candidate
        for other in group
        for candidate in [
            _code_region_indexes(
                other,
                sources.new_regions,
                sources.old_regions,
            )[1]
        ]
        if candidate is not None
    }
    if len(candidates) == 1:
        old_region = candidates.pop()
    return _code_block_segment(
        group,
        sources.new_lines,
        sources.new_regions[region],
        region,
        old_source_lines=sources.old_lines,
        old_regions=sources.old_regions,
        old_block_index=old_region,
    )


def _expanded_segments(
    filtered: list[BlockChange],
    sources: _PlanSources,
) -> list[BlockChange]:
    """초기 변경을 번역 소유 블록 또는 code 블록 전체로 확장.

    Args:
        filtered: 제어 줄과 빈 변경을 제외한 초기 segment.
        sources: 이전·현재 원문 구조.

    Returns:
        병합 전 소유 블록 변경 segment.

    Raises:
        PatchError: 수정 표 행의 안정 주소가 없거나 한 표의 여러 행 수정.
    """

    expanded: list[BlockChange] = []
    emitted_regions: set[int] = set()
    modified_tables: set[int] = set()
    for segment in filtered:
        region, _old_region = _code_region_indexes(
            segment,
            sources.new_regions,
            sources.old_regions,
        )
        code_segment = _expanded_code_segment(
            segment,
            filtered,
            sources,
            emitted_regions,
        )
        if region is not None and region < len(sources.new_regions):
            if code_segment is not None:
                expanded.append(code_segment)
            continue
        _require_supported_modified_admonition(segment)
        if _require_supported_modified_table(segment, sources.old_lines):
            table_row = _source_table_row_change(segment, sources.old_lines)
            if table_row is None:
                raise PatchError("modified table row has no stable source address")
            if table_row.table_ordinal in modified_tables:
                raise PatchError("modified table must change exactly one row")
            modified_tables.add(table_row.table_ordinal)
            segment = replace(segment, table_row=table_row)
        expanded.extend(
            _expand_to_source_blocks(
                segment,
                new_source_blocks=sources.new_blocks,
                old_source_blocks=sources.old_blocks,
                new_source_lines=sources.new_lines,
                old_source_lines=sources.old_lines,
            )
        )
    return expanded


def _final_patch_plan(
    changes: list[BlockChange],
    sources: _PlanSources,
) -> PatchPlan:
    """확장된 변경과 원문 구조 서명을 최종 patch 계획으로 조립.

    Args:
        changes: 병합이 끝난 소유 블록 변경.
        sources: 이전·현재 원문 구조.

    Returns:
        번역 적용에 사용할 완성된 patch 계획.
    """

    return PatchPlan(
        changes=tuple(
            _add_neighbor_anchors(
                _attach_deleted_code_block(
                    change,
                    old_source_lines=sources.old_lines,
                    old_regions=sources.old_regions,
                    new_source_lines=sources.new_lines,
                    new_regions=sources.new_regions,
                ),
                old_source_blocks=sources.old_blocks,
                new_source_blocks=sources.new_blocks,
            )
            for change in changes
        ),
        old_source_anchors=tuple(
            block.comment for block in _plan_source_blocks(sources.old_blocks)
        ),
        new_source_anchors=tuple(
            block.comment for block in _plan_source_blocks(sources.new_blocks)
        ),
        old_code_blocks=_code_blocks_from_regions(
            sources.old_lines,
            sources.old_regions,
        ),
        new_code_blocks=_code_blocks_from_regions(
            sources.new_lines,
            sources.new_regions,
        ),
        old_source_comments=_source_comment_locations(sources.old_text),
        new_source_comments=_source_comment_locations(sources.new_text),
        old_front_matter=sources.old_front_matter,
        new_front_matter=sources.new_front_matter,
    )


def build_plan(
    hunks: tuple[DiffHunk, ...],
    source_text: str,
    *,
    normalize_source: Callable[[str], str] | None = None,
    normalize_source_pair: Callable[[str, str], tuple[str, str]] | None = None,
) -> PatchPlan:
    """effective line delta와 전체 이전·신규 원문 block의 결합."""

    old_source_text, source_text = reconstruct_source_pair(hunks, source_text)
    normalized = _normalized_patch_plan(
        hunks,
        old_source_text,
        source_text,
        normalize_source=normalize_source,
        normalize_source_pair=normalize_source_pair,
    )
    if normalized is not None:
        return normalized
    sources = _plan_sources(old_source_text, source_text)
    reorder_plan = _named_reorder_patch_plan(
        sources,
        _named_section_reorder(old_source_text, source_text),
    )
    if reorder_plan is not None:
        return reorder_plan
    initial = _initial_segments(hunks, sources)
    expanded = _expanded_segments(initial, sources)
    return _final_patch_plan(_coalesce_source_block_segments(expanded), sources)


def _context_text(line: DiffLine | None) -> str | None:
    """diff 문맥 줄의 원문 내용."""

    return _normalize_text(line.text) if line is not None else None


def _lines_text(lines: list[str], template: str) -> str:
    """template의 끝 줄바꿈 형식으로 결합한 줄 목록."""

    text = "\n".join(lines)
    return text + "\n" if template.endswith("\n") else text


def _front_matter_text(text: str) -> str | None:
    """문서 선두 YAML front matter 원문."""

    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[: index + 1])
    return "".join(lines)


def _front_matter_line_numbers(text: str) -> set[int]:
    """front matter가 차지하는 1-based 줄 번호 집합."""

    front_matter = _front_matter_text(text)
    if front_matter is None:
        return set()
    return set(range(1, len(front_matter.splitlines()) + 1))


def _require_supported_front_matter(front_matter: str) -> None:
    """front matter의 지원 조건 검증."""

    lines = front_matter.splitlines()
    if (
        len(lines) < 2
        or lines[0].strip() != "---"
        or lines[-1].strip() != "---"
    ):
        raise PatchError("unsupported front matter: missing closing delimiter")
    keys: set[str] = set()
    index = 1
    while index < len(lines) - 1:
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        index = _validate_front_matter_scalar(lines, index, keys)


def _validate_front_matter_scalar(
    lines: list[str],
    index: int,
    keys: set[str],
) -> int:
    """단일 머리말 key와 scalar를 검증하고 다음 key 위치 반환.

    Args:
        lines: 머리말 물리 줄.
        index: 현재 key 줄 위치.
        keys: 이미 확인한 key 집합.

    Returns:
        다음 key 또는 닫는 구분자 위치.

    Raises:
        PatchError: 중첩값·잘못된 scalar·중복 key 발견.
    """

    line = lines[index]
    if line[:1].isspace():
        raise PatchError("unsupported front matter: nested values are not supported")
    match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)", line)
    if match is None:
        raise PatchError("unsupported front matter string scalar")
    key = match.group(1)
    if key in keys:
        raise PatchError("unsupported front matter: duplicate key")
    keys.add(key)
    end = index + 1
    while end < len(lines) - 1 and (
        not lines[end].strip() or lines[end][:1].isspace()
    ):
        end += 1
    candidate = "\n".join(
        ["---", f"description: {match.group(2)}", *lines[index + 1 : end], "---"]
    )
    description = front_matter_description(candidate)
    if description is None or not description.valid:
        raise PatchError("unsupported front matter string scalar")
    return end


def _source_comment_line_numbers(text: str) -> set[int]:
    """독립 원문 HTML 주석이 차지하는 줄 번호 집합."""

    return set(standalone_html_comment_line_numbers(text))


def diff_text(segment: BlockChange) -> str:
    """provider에 전달할 segment의 통합 diff."""

    lines: list[str] = []
    for old_line in segment.old_lines:
        lines.append(f"- {old_line}")
    for new_line in segment.new_lines:
        lines.append(f"+ {new_line}")
    return "\n".join(lines)


def source_text(segment: BlockChange) -> str:
    """segment가 소유한 현재 원문 block."""

    if segment.inserted_code_block is not None:
        return segment.inserted_code_block.rstrip("\n") + "\n"
    if segment.new_source is not None:
        return segment.new_source.rstrip() + "\n"
    return "\n".join(_meaningful_lines(segment.new_lines)).rstrip() + "\n"


def existing_context(text: str, segment: BlockChange) -> str:
    """segment 주소를 기준으로 찾은 기존 locale 문맥."""

    if segment.is_admonition_marker_change:
        return _existing_admonition_context(text, segment)
    blocks = _blocks(text)
    old_anchor = segment.old_source or _joined(segment.old_lines)
    if old_anchor:
        return _existing_replacement_context(text, blocks, segment)
    applied = _find_applied_new_blocks(blocks, segment)
    if applied:
        return "".join(block.text for block in applied).strip()
    context = _neighbor_existing_context(blocks, segment)
    return context if context is not None else "(none)"


def _existing_replacement_context(
    text: str,
    blocks: list[AnnotatedBlock],
    segment: BlockChange,
) -> str:
    """교체·삭제 segment의 기존 locale 문맥 탐색.

    Args:
        text: 기존 locale 문서.
        blocks: annotation block 목록.
        segment: 적용할 변경 segment.

    Returns:
        기존 또는 이미 적용된 locale 문맥.

    Raises:
        PatchError: 안정적인 기존 주소를 찾지 못함.
    """

    try:
        found = _find_old_blocks(blocks, segment)
        return "".join(block.text for block in found).strip()
    except PatchError:
        applied = _find_applied_new_blocks(blocks, segment)
        if applied:
            return "".join(block.text for block in applied).strip()
        if segment.is_block_range:
            raise
        if _single_table_row_lines(segment) is not None:
            context = _table_row_context(text, segment)
            if context:
                return context.strip()
            raise
        context = _context_between_raw_contexts(text, segment)
        if context:
            return context.strip()
        raise


def _neighbor_existing_context(
    blocks: list[AnnotatedBlock],
    segment: BlockChange,
) -> str | None:
    """삽입 segment의 이전·다음 anchor 문맥 탐색.

    Args:
        blocks: annotation block 목록.
        segment: 적용할 삽입 segment.

    Returns:
        발견한 이웃 block 본문 또는 ``None``.
    """

    for anchor, neighbor, ordinal in (
        (
            segment.before_context,
            segment.old_previous_anchor,
            segment.old_previous_anchor_ordinal,
        ),
        (
            segment.after_context,
            segment.old_next_anchor,
            segment.old_next_anchor_ordinal,
        ),
    ):
        if anchor:
            block = _context_anchor_block(blocks, anchor, neighbor, ordinal)
            if block:
                return block.text.strip()
    return None


def _existing_admonition_context(text: str, segment: BlockChange) -> str:
    """marker 변경에 대응하는 기존 locale admonition 문맥."""

    lines = text.splitlines(keepends=True)
    starts = _admonition_start_indexes(lines)
    ordinal = segment.old_block_ordinal
    if (
        ordinal is None
        or ordinal >= len(starts)
        or not _admonition_marker_count_matches(len(starts), segment)
    ):
        raise PatchError("missing existing admonition marker")
    start = starts[ordinal]
    current_type = _admonition_marker_type(lines[start].strip())
    old_type = _admonition_marker_type(_meaningful_lines(segment.old_lines)[0])
    new_type = _admonition_marker_type(_meaningful_lines(segment.new_lines)[0])
    if current_type not in (old_type, new_type):
        raise PatchError("existing admonition marker does not match the plan")
    end = start + 1
    while end < len(lines) and lines[end].strip().startswith(">"):
        end += 1
    return "".join(lines[start:end]).strip()


def _admonition_marker_count_matches(actual: int, segment: BlockChange) -> bool:
    """locale과 원문의 admonition marker 개수 일치 여부."""

    expected = {
        count
        for count in (
            segment.old_anchor_occurrences,
            segment.new_anchor_occurrences,
        )
        if count is not None
    }
    return not expected or actual in expected


def _changes_fenced_code(segment: BlockChange) -> bool:
    """segment가 fenced code 경계를 변경하는지 여부."""

    if (
        segment.code_block is not None
        or segment.inserted_code_block is not None
        or segment.deleted_code_block is not None
    ):
        return True
    source_lines = (
        segment.old_lines
        + segment.new_lines
        + tuple((segment.old_source or "").splitlines())
        + tuple((segment.new_source or "").splitlines())
    )
    return any(fence_token(line) for line in source_lines)


def apply_segments(
    existing: str,
    segments: list[BlockChange],
    translated_blocks: list[str],
    *,
    source_state: bool = False,
    target_state: bool = False,
    code_state: PlanState = PlanState.UNGUARDED,
) -> str:
    """segment 목록 적용."""

    translated_iter = iter(translated_blocks)
    original_blocks = _blocks(existing)
    prepared: list[
        tuple[BlockChange, str | None, tuple[AnnotatedBlock, ...] | None]
    ] = []
    for segment in segments:
        translated = next(translated_iter, None) if segment.needs_translation else None
        if translated is not None:
            translated = _strip_retained_admonition_marker(segment, translated)
        old_found = (
            _find_old_blocks(original_blocks, segment, required=False)
            if segment.code_block is None
            else None
        )
        prepared.append((segment, translated, old_found))
    text = existing
    offsets_shifted = False

    ordered = [
        item for item in prepared if item[0].is_admonition_marker_change
    ] + [
        item
        for item in reversed(prepared)
        if not item[0].is_admonition_marker_change
    ]
    for segment, translated, old_found in ordered:
        fenced_code_change = _changes_fenced_code(segment)
        if code_state is PlanState.TARGET and fenced_code_change:
            continue
        if segment.code_block is not None:
            text = _apply_code_block(text, segment.code_block, state=code_state)
            continue
        if segment.is_named_anchor_change:
            text = _apply_named_anchor_change(text, segment, translated)
            continue
        if segment.is_admonition_marker_change:
            before_line_count = len(text.splitlines(keepends=True))
            text = _apply_admonition_marker_change(text, segment, translated)
            offsets_shifted = offsets_shifted or (
                len(text.splitlines(keepends=True)) != before_line_count
            )
            continue
        if segment.is_inline_code_identifier_list and _inline_code_list_is_applied(
            text, segment
        ):
            continue
        if target_state and (segment.old_anchors or segment.new_anchors):
            if segment.is_deletion:
                _reject_target_deletion_residue(text, segment)
            elif segment.needs_translation:
                _require_target_block_bodies(text, segment)
            continue
        has_old_source = bool(
            segment.old_source or _meaningful_lines(segment.old_lines)
        )
        if offsets_shifted and has_old_source:
            old_found = _find_old_blocks(_blocks(text), segment, required=False)
        if has_old_source and segment.needs_translation:
            if translated is None:
                raise PatchError("missing translated replacement block")
            text = (
                _replace_resolved_blocks(text, old_found, translated)
                if old_found
                else _replace_segment(text, segment, translated)
            )
        elif segment.is_deletion:
            if segment.deleted_code_block is not None:
                text = _delete_fenced_code_block(text, segment)
            else:
                text = (
                    _delete_resolved_blocks(text, old_found)
                    if old_found
                    else _delete_segment(text, segment)
                )
        elif segment.needs_translation:
            if translated is None:
                raise PatchError("missing translated insertion block")
            # 신규 diff가 중복 블록을 삽입 후 삭제로 재정렬할 수 있어 계획된 삽입 유지
            if (
                segment.inserted_code_block is not None
                and code_state is PlanState.SOURCE
            ):
                if (
                    segment.old_previous_anchor
                    or segment.old_next_anchor
                    or segment.before_context
                    or segment.after_context
                ):
                    text = _insert_block(text, segment, translated, force=True)
                else:
                    text = _insert_fenced_code_block(text, segment, translated)
            else:
                text = _insert_block(
                    text,
                    segment,
                    translated,
                    force=source_state
                    or (code_state is PlanState.SOURCE and fenced_code_change),
                )

    return _ensure_single_eof_newline(text)


def apply_plan(
    existing: str | None, plan: PatchPlan, translated_blocks: list[str]
) -> str:
    """patch 계획 적용."""

    state = plan_state(existing, plan)
    if state is PlanState.CREATE:
        return _render_create_plan(plan, translated_blocks)
    if existing is None:
        raise PatchError("non-create plan requires an existing locale document")
    _validate_plan_translation_count(state, plan, translated_blocks)
    code_state = _code_plan_state(existing, plan)
    source_state = state is PlanState.SOURCE
    target_state = state is PlanState.TARGET
    working = _apply_front_matter_change(existing, plan) if source_state else existing
    source_anchors = plan.new_source_anchors if target_state else plan.old_source_anchors
    source_comments = plan.new_source_comments if target_state else plan.old_source_comments
    masked_existing, source_comment_replacements = _mask_source_comment_anchors(
        working, source_anchors or (), source_comments
    )
    result = _apply_plan_body(
        masked_existing,
        plan,
        translated_blocks,
        source_state=source_state,
        target_state=target_state,
        code_state=code_state,
    )
    result = _ensure_single_eof_newline(result)
    _validate_plan_body_order(result, plan)
    restored = _restore_plan_source_comments(
        result,
        plan,
        source_comment_replacements,
        source_state=source_state,
    )
    _validate_restored_source_comments(restored, plan)
    return restored


def _validate_plan_translation_count(
    state: PlanState,
    plan: PatchPlan,
    translated_blocks: list[str],
) -> None:
    """계획 상태에 맞는 provider 번역 블록 개수 검증.

    Args:
        state: 현재 locale 문서의 계획 상태.
        plan: 적용할 patch 계획.
        translated_blocks: provider 번역 결과.

    Raises:
        PatchError: 기대 개수와 실제 번역 블록 개수가 다름.
    """

    expected = (
        0
        if state is PlanState.TARGET
        else sum(change.needs_translation for change in plan.changes)
    )
    if len(translated_blocks) != expected:
        raise PatchError(
            f"translation count mismatch: expected {expected}, got {len(translated_blocks)}"
        )


def _apply_plan_body(
    existing: str,
    plan: PatchPlan,
    translated_blocks: list[str],
    *,
    source_state: bool,
    target_state: bool,
    code_state: PlanState,
) -> str:
    """section 재정렬 또는 일반 segment를 마스킹된 문서에 적용.

    Args:
        existing: 원문 작성 주석 anchor를 마스킹한 locale 문서.
        plan: 적용할 patch 계획.
        translated_blocks: provider 번역 결과.
        source_state: 문서가 변경 이전 상태인지 여부.
        target_state: 문서가 변경 이후 상태인지 여부.
        code_state: fenced code 구조의 현재 계획 상태.

    Returns:
        source comment 복원 전 patch 결과.
    """

    if plan.named_section_reorder is not None and source_state:
        return _apply_named_section_reorder(existing, plan.named_section_reorder)
    return apply_segments(
        existing,
        list(plan.changes),
        translated_blocks,
        source_state=source_state,
        target_state=target_state,
        code_state=code_state,
    )


def _validate_plan_body_order(result: str, plan: PatchPlan) -> None:
    """patch 결과의 section 또는 annotation anchor 순서 검증.

    Args:
        result: source comment 복원 전 patch 결과.
        plan: 적용한 patch 계획.

    Raises:
        PatchError: 결과 block 순서가 목표 원문과 다름.
    """

    if plan.named_section_reorder is not None:
        order = tuple(
            section.signature
            for section in _split_named_sections(result, translated=True)[1]
        )
        if order != plan.named_section_reorder.new_order:
            raise PatchError("patched named section order does not match the target source")
        return
    if (
        plan.new_source_anchors is not None
        and _annotation_anchor_sequence(result) != plan.new_source_anchors
    ):
        raise PatchError("patched block order does not match the target source")


def _restore_plan_source_comments(
    result: str,
    plan: PatchPlan,
    replacements: tuple[tuple[str, str], ...],
    *,
    source_state: bool,
) -> str:
    """마스킹된 원문 작성 주석을 목표 계획에 맞게 복원.

    Args:
        result: source comment 복원 전 patch 결과.
        plan: 적용한 patch 계획.
        replacements: 임시 anchor별 원래 주석 mapping.
        source_state: 문서가 변경 이전 상태였는지 여부.

    Returns:
        원문 작성 주석 복원이 끝난 locale 문서.
    """

    if source_state and plan.named_section_reorder is None:
        return _rewrite_source_comment_anchors(
            result,
            replacements,
            plan.old_source_comments,
            plan.new_source_comments,
            plan.new_source_anchors or (),
        )
    return _restore_source_comment_anchors(result, replacements)


def _validate_restored_source_comments(result: str, plan: PatchPlan) -> None:
    """복원된 원문 작성 주석의 목표 block 순서 검증.

    Args:
        result: source comment 복원이 끝난 locale 문서.
        plan: 적용한 patch 계획.

    Raises:
        PatchError: 주석 순서가 목표 원문과 다름.
    """

    if (
        plan.named_section_reorder is None
        and plan.new_source_anchors is not None
        and _locate_source_comment_blocks(
            result,
            plan.new_source_anchors,
            plan.new_source_comments,
        )
        is None
    ):
        raise PatchError("patched source HTML comment order does not match the target source")


def plan_state(existing: str | None, plan: PatchPlan) -> PlanState:
    """기존 locale 문서에서 계획의 create/source/target 상태 판정."""

    if plan.is_create:
        if existing is not None:
            raise PatchError("create plan requires an absent locale destination")
        return PlanState.CREATE
    if existing is None:
        raise PatchError("non-create plan requires an existing locale document")
    if plan.named_section_reorder is not None:
        return _named_section_plan_state(existing, plan)
    if not _has_guarded_transition(plan):
        return PlanState.UNGUARDED
    if _matches_document_state(
        existing,
        plan.old_front_matter,
        plan.old_source_anchors or (),
        plan.old_source_comments,
    ):
        return PlanState.SOURCE
    if _matches_document_state(
        existing,
        plan.new_front_matter,
        plan.new_source_anchors or (),
        plan.new_source_comments,
    ):
        return PlanState.TARGET
    raise PatchError("existing document matches neither source nor target plan state")


def _has_guarded_transition(plan: PatchPlan) -> bool:
    """계획에 상태 판정이 필요한 구조 전환이 있는지 판정.

    Args:
        plan: 판정할 patch 계획.

    Returns:
        anchor·머리말·원문 주석 구조가 변경되는지 여부.
    """

    anchor_transition = (
        plan.old_source_anchors is not None
        and plan.new_source_anchors is not None
        and plan.old_source_anchors != plan.new_source_anchors
        and any(change.old_anchors or change.new_anchors for change in plan.changes)
    )
    front_matter_transition = plan.old_front_matter != plan.new_front_matter
    comment_transition = _source_comment_signatures(
        plan.old_source_comments
    ) != _source_comment_signatures(plan.new_source_comments)
    return anchor_transition or front_matter_transition or comment_transition


def _named_section_plan_state(existing: str, plan: PatchPlan) -> PlanState:
    """이름 anchor section 재정렬 계획의 현재 상태 판정.

    Args:
        existing: 기존 locale 문서.
        plan: section 재정렬 patch 계획.

    Returns:
        변경 이전 또는 이후 상태.

    Raises:
        PatchError: 어느 section 순서와도 일치하지 않음.
    """

    reorder = plan.named_section_reorder
    if reorder is None:
        raise PatchError("named section plan requires a reorder contract")
    if _matches_named_section_state(
        existing,
        plan.old_source_anchors or (),
        plan.old_source_comments,
        reorder.old_order,
    ):
        return PlanState.SOURCE
    if _matches_named_section_state(
        existing,
        plan.new_source_anchors or (),
        plan.new_source_comments,
        reorder.new_order,
    ):
        return PlanState.TARGET
    raise PatchError(
        "existing named section order matches neither source nor target plan state"
    )


def _source_comment_signatures(
    comments: tuple[SourceComment, ...],
) -> tuple[tuple[str, int, str], ...]:
    """원문 HTML 주석 문자열과 구조 위치의 서명."""

    return tuple(
        (comment.raw, comment.anchor_position, comment.placement)
        for comment in comments
    )


_LOCALE_ROUTING_FRONT_MATTER_RE = re.compile(
    r"\A---\r?\nslug:[ \t]*\S[^\r\n]*\r?\n---\r?\n\Z"
)


def is_locale_routing_front_matter_text(front_matter: str | None) -> bool:
    """저장소 소유 locale 라우팅 ``slug`` 머리말 여부."""

    return front_matter is not None and bool(
        _LOCALE_ROUTING_FRONT_MATTER_RE.match(front_matter)
    )


def _matches_document_state(
    existing: str,
    front_matter: str | None,
    anchors: tuple[str, ...],
    comments: tuple[SourceComment, ...],
) -> bool:
    """locale 문서가 계획의 원문 또는 대상 상태와 일치하는지 여부."""

    existing_front_matter = _front_matter_text(existing)
    if existing_front_matter != front_matter and not (
        front_matter is None
        and is_locale_routing_front_matter_text(existing_front_matter)
    ):
        return False
    return _locate_source_comment_blocks(existing, anchors, comments) is not None


def _apply_front_matter_change(existing: str, plan: PatchPlan) -> str:
    """front matter 변경 적용."""

    old = plan.old_front_matter
    new = plan.new_front_matter
    if old == new:
        return existing
    if _front_matter_text(existing) != old:
        raise PatchError("existing front matter does not match the source plan state")
    if old is not None:
        return (new or "") + existing[len(old) :]
    if new is None:
        return existing
    separator = "" if not existing or existing.startswith(("\n", "\r")) else "\n"
    return new + separator + existing


def _matches_named_section_state(
    existing: str,
    anchors: tuple[str, ...],
    comments: tuple[SourceComment, ...],
    expected_order: tuple[NamedSectionSignature, ...],
) -> bool:
    """named section 순서가 지정된 계획 상태와 일치하는지 여부."""

    if comments:
        try:
            existing, _replacements = _mask_source_comment_anchors(
                existing,
                anchors,
                comments,
            )
        except PatchError:
            return False
    _prefix, sections = _split_named_sections(existing, translated=True)
    return tuple(section.signature for section in sections) == expected_order


def _code_plan_state(existing: str, plan: PatchPlan) -> PlanState:
    """fenced code block 집합에 대한 계획 상태 판정."""

    if plan.old_code_blocks is None or plan.new_code_blocks is None:
        return PlanState.UNGUARDED
    if plan.old_code_blocks == plan.new_code_blocks:
        return PlanState.UNGUARDED

    current = _fenced_code_blocks(existing)
    if current == plan.old_code_blocks:
        return PlanState.SOURCE
    if current == plan.new_code_blocks:
        return PlanState.TARGET
    permuted_new = _permuted_code_blocks(current, plan.new_code_blocks)
    pure_fenced_insertion = any(
        change.inserted_code_block is not None for change in plan.changes
    ) and all(
        change.code_block is None and change.deleted_code_block is None
        for change in plan.changes
    )
    if permuted_new and pure_fenced_insertion:
        return PlanState.TARGET
    if _permuted_code_blocks(current, plan.old_code_blocks) or permuted_new:
        return PlanState.SOURCE
    raise PatchError(
        "existing code block state matches neither source nor target plan state"
    )


def _permuted_code_blocks(
    current: tuple[str, ...], expected: tuple[str, ...]
) -> bool:
    """줄 순서를 제외한 각 block과 예상 block의 일치 여부."""
    if len(current) != len(expected) or current == expected:
        return False
    return all(
        Counter(have.split("\n")) == Counter(want.split("\n"))
        for have, want in zip(current, expected)
    )


def _strip_retained_admonition_marker(
    segment: BlockChange, translated: str
) -> str:
    """번역 결과에 남은 admonition marker 제거."""

    marker = segment.before_context
    if not marker or not _ADMONITION_MARKER_RE.fullmatch(marker.strip()):
        return translated

    lines = translated.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        if line.strip() == marker.strip():
            del lines[index]
        break
    return "".join(lines)


def _blocks(text: str) -> list[AnnotatedBlock]:
    """locale 문서의 annotation 소유 block 목록."""

    lines = text.splitlines(keepends=True)
    starts = _comment_starts(lines)
    blocks: list[AnnotatedBlock] = []

    for index, start in enumerate(starts):
        comment_end, comment = _read_comment(lines, start)
        next_start = starts[index + 1] if index + 1 < len(starts) else len(lines)
        end = _translated_block_end(lines, comment_end, next_start)
        blocks.append(
            AnnotatedBlock(
                start=start,
                end=end,
                comment=_normalize_text(comment),
                text="".join(lines[start:end]),
            )
        )

    return blocks


def _annotation_anchor_sequence(text: str) -> tuple[str, ...]:
    """locale 문서 순서로 정규화한 annotation anchor 목록."""

    return tuple(block.comment for block in _blocks(text) if _is_plan_anchor(block))


def _source_comment_locations(text: str) -> tuple[SourceComment, ...]:
    """코드 영역 밖 원문 HTML 주석의 위치 정보."""

    lines = text.splitlines(keepends=True)
    source_blocks = _plan_source_blocks(_source_blocks(text))
    source_comment_lines = _source_comment_line_numbers(text)
    front_matter_lines = _front_matter_line_numbers(text)
    has_other_content = any(
        line.strip()
        and lineno not in source_comment_lines
        and lineno not in front_matter_lines
        for lineno, line in enumerate(lines, start=1)
    )
    comments: list[SourceComment] = []
    for start in _comment_starts(lines):
        if (
            start + 1 not in source_comment_lines
            or start + 1 in front_matter_lines
        ):
            continue
        comments.append(
            _source_comment_location(
                lines,
                start,
                source_blocks,
                has_other_content=has_other_content,
            )
        )
    return tuple(comments)


def _source_comment_location(
    lines: list[str],
    start: int,
    source_blocks: list[SourceBlock],
    *,
    has_other_content: bool,
) -> SourceComment:
    """단일 원문 작성 주석의 anchor 위치와 배치 계산.

    Args:
        lines: 줄바꿈을 보존한 원문 줄.
        start: 주석 시작 줄 위치.
        source_blocks: 번역 계획 원문 블록.
        has_other_content: 주석·머리말 이외의 문서 내용 존재 여부.

    Returns:
        구조 주소가 포함된 원문 주석.
    """

    end, comment_body = _read_comment(lines, start)
    lineno = start + 1
    position = sum(block.start_lineno < lineno for block in source_blocks)
    previous = source_blocks[position - 1] if position > 0 else None
    following = source_blocks[position] if position < len(source_blocks) else None
    before_following = bool(following) and not any(
        line.strip() for line in lines[end : following.start_lineno - 1]
    )
    after_previous = bool(previous) and not any(
        line.strip() for line in lines[previous.end_lineno : start]
    )
    if before_following:
        placement = "before"
    elif after_previous:
        placement = "after"
    elif not source_blocks and not has_other_content:
        placement = "document"
    else:
        placement = "ambiguous"
    return SourceComment(
        body=_normalize_text(comment_body),
        anchor_position=position,
        raw="".join(lines[start:end]),
        placement=placement,
    )


def _mask_source_comment_anchors(
    text: str,
    anchors: tuple[str, ...],
    comments: tuple[SourceComment, ...],
) -> tuple[str, tuple[tuple[str, str], ...]]:
    """원문 주석 anchor 마스킹."""

    if not comments:
        return text, ()
    located = _locate_source_comment_blocks(text, anchors, comments)
    if located is None:
        raise PatchError("could not locate source HTML comments in the locale document")
    lines = text.splitlines(keepends=True)
    replacements: list[tuple[str, str]] = []
    spans: list[tuple[int, int, str]] = []
    for index, block in enumerate(located):
        end, _body = _read_comment(lines, block.start)
        original = "".join(lines[block.start:end])
        line_ending = "\n" if original.endswith("\n") else ""
        marker = (
            "<!-- <translation-sync-source-comment "
            f'data-index="{index}"></translation-sync-source-comment> -->'
            f"{line_ending}"
        )
        replacements.append((marker, original))
        spans.append((block.start, end, marker))
    for start, end, marker in reversed(spans):
        lines[start:end] = [marker]
    return "".join(lines), tuple(replacements)


def _restore_source_comment_anchors(
    text: str, replacements: tuple[tuple[str, str], ...]
) -> str:
    """원문 주석 anchor 복원."""

    for marker, original in replacements:
        if text.count(marker) != 1:
            raise PatchError("source HTML comment was lost or duplicated while patching")
        text = text.replace(marker, original, 1)
    return text


def _rewrite_source_comment_anchors(
    text: str,
    replacements: tuple[tuple[str, str], ...],
    old_comments: tuple[SourceComment, ...],
    new_comments: tuple[SourceComment, ...],
    new_anchors: tuple[str, ...],
) -> str:
    """원문 HTML 주석 anchor를 현재 원문 기준으로 재작성."""

    old_by_position: dict[tuple[int, str], list[tuple[str, SourceComment]]] = {}
    for replacement, comment in zip(replacements, old_comments, strict=True):
        marker, _original = replacement
        old_by_position.setdefault(
            (comment.anchor_position, comment.placement), []
        ).append(
            (marker, comment)
        )
    new_by_position: dict[tuple[int, str], list[SourceComment]] = {}
    for comment in new_comments:
        new_by_position.setdefault(
            (comment.anchor_position, comment.placement), []
        ).append(comment)

    pending: list[SourceComment] = []
    updates: list[tuple[str, str]] = []
    for position in sorted(set(old_by_position) | set(new_by_position)):
        old_group = old_by_position.get(position, [])
        new_group = new_by_position.get(position, [])
        paired = min(len(old_group), len(new_group))
        for index in range(paired):
            marker = old_group[index][0]
            updates.append((marker, new_group[index].raw))
        for marker, _comment in old_group[paired:]:
            updates.append((marker, ""))
        pending.extend(new_group[paired:])

    if pending:
        new_order = {id(comment): index for index, comment in enumerate(new_comments)}
        pending.sort(key=lambda comment: new_order[id(comment)])
        text = _insert_source_comments(text, new_anchors, pending)
    for marker, replacement in updates:
        if text.count(marker) != 1:
            raise PatchError("source HTML comment was lost or duplicated while patching")
        text = text.replace(marker, replacement, 1)
    return text


def _insert_source_comments(
    text: str,
    anchors: tuple[str, ...],
    comments: list[SourceComment],
) -> str:
    """현재 원문에 새로 추가된 독립 HTML 주석 삽입."""

    blocks = [block for block in _blocks(text) if _is_plan_anchor(block)]
    if tuple(block.comment for block in blocks) != anchors:
        raise PatchError("could not resolve source HTML comment insertion boundary")
    lines = text.splitlines(keepends=True)
    insertions: dict[int, list[SourceComment]] = {}
    for comment in comments:
        index = _source_comment_insertion_index(text, blocks, comment)
        insertions.setdefault(index, []).append(comment)

    for index, group in sorted(insertions.items(), reverse=True):
        ending, rendered = _render_source_comment_group(group)
        before = "" if index == 0 or not lines[index - 1].strip() else ending
        after = "" if index >= len(lines) or not lines[index].strip() else ending
        lines[index:index] = [before + rendered + after]
    return "".join(lines)


def _source_comment_insertion_index(
    text: str,
    blocks: list[AnnotatedBlock],
    comment: SourceComment,
) -> int:
    """원문 작성 주석의 locale 삽입 줄 위치 계산.

    Args:
        text: 기존 locale 문서.
        blocks: 번역 계획 annotation 블록.
        comment: 삽입할 원문 작성 주석.

    Returns:
        0-based 삽입 줄 위치.

    Raises:
        PatchError: 구조 주소가 모호하거나 이웃 anchor가 없음.
    """

    if comment.placement == "ambiguous":
        raise PatchError("source HTML comment structural address is ambiguous")
    if comment.placement == "before":
        if comment.anchor_position >= len(blocks):
            raise PatchError("source HTML comment next anchor is missing")
        return blocks[comment.anchor_position].start
    if comment.placement == "after":
        if comment.anchor_position == 0 or comment.anchor_position > len(blocks):
            raise PatchError("source HTML comment previous anchor is missing")
        return blocks[comment.anchor_position - 1].end
    if blocks:
        raise PatchError("source HTML comment document boundary is ambiguous")
    front_matter = _front_matter_text(text)
    return len(front_matter.splitlines()) if front_matter else 0


def _render_source_comment_group(
    comments: list[SourceComment],
) -> tuple[str, str]:
    """같은 위치의 원문 주석을 원래 줄바꿈 형식으로 렌더링.

    Args:
        comments: 같은 삽입 위치의 원문 주석.

    Returns:
        사용할 줄바꿈과 결합된 주석 본문.
    """

    ending = "\r\n" if any(comment.raw.endswith("\r\n") for comment in comments) else "\n"
    rendered = ending.join(comment.raw.rstrip("\r\n") for comment in comments)
    return ending, rendered + ending


def _locate_source_comment_blocks(
    text: str,
    anchors: tuple[str, ...],
    comments: tuple[SourceComment, ...],
) -> tuple[AnnotatedBlock, ...] | None:
    """원문 주석을 번역 anchor와 구분하여 탐색."""

    blocks = _blocks(text)
    plan_blocks = [block for block in blocks if _is_plan_anchor(block)]
    expected, plan_prefixes = _source_comment_expectations(anchors, comments)
    if tuple(block.comment for block in plan_blocks) != tuple(
        body for body, _index in expected
    ):
        return None
    located, anchor_blocks = _located_plan_comment_blocks(
        plan_blocks,
        expected,
        len(comments),
    )
    if not _locate_non_plan_comment_blocks(
        blocks,
        plan_blocks,
        comments,
        plan_prefixes,
        located,
    ):
        return None
    if any(block is None for block in located):
        return None
    resolved = tuple(block for block in located if block is not None)
    lines = text.splitlines(keepends=True)
    if not all(
        _source_comment_placement_is_valid(lines, block, comment, anchor_blocks)
        for block, comment in zip(resolved, comments, strict=True)
    ):
        return None
    return resolved


def _source_comment_expectations(
    anchors: tuple[str, ...],
    comments: tuple[SourceComment, ...],
) -> tuple[list[tuple[str, int | None]], dict[int, int]]:
    """원문 주석과 번역 anchor의 기대 순서 구성.

    Args:
        anchors: 번역 계획 annotation anchor 순서.
        comments: 구조 주소가 포함된 원문 작성 주석.

    Returns:
        기대 주석 순서와 비계획 주석별 앞선 계획 anchor 수.
    """

    expected: list[tuple[str, int | None]] = []
    plan_prefixes: dict[int, int] = {}
    by_position: dict[int, list[tuple[int, SourceComment]]] = {}
    for index, comment in enumerate(comments):
        by_position.setdefault(comment.anchor_position, []).append((index, comment))

    for position in range(len(anchors) + 1):
        for index, comment in by_position.get(position, []):
            plan_prefixes[index] = len(expected)
            if _is_plan_anchor_comment(comment.body):
                expected.append((comment.body, index))
        if position < len(anchors):
            expected.append((anchors[position], None))
    return expected, plan_prefixes


def _located_plan_comment_blocks(
    plan_blocks: list[AnnotatedBlock],
    expected: list[tuple[str, int | None]],
    comment_count: int,
) -> tuple[list[AnnotatedBlock | None], list[AnnotatedBlock]]:
    """계획 anchor로 사용되는 원문 주석과 번역 블록 배치.

    Args:
        plan_blocks: locale 문서의 계획 annotation 블록.
        expected: 기대 계획 주석·anchor 순서.
        comment_count: 전체 원문 작성 주석 수.

    Returns:
        원문 주석별 위치와 순수 번역 anchor 블록.
    """

    located: list[AnnotatedBlock | None] = [None] * comment_count
    anchor_blocks: list[AnnotatedBlock] = []
    for block, (_body, comment_index) in zip(plan_blocks, expected, strict=True):
        if comment_index is not None:
            located[comment_index] = block
        else:
            anchor_blocks.append(block)
    return located, anchor_blocks


def _locate_non_plan_comment_blocks(
    blocks: list[AnnotatedBlock],
    plan_blocks: list[AnnotatedBlock],
    comments: tuple[SourceComment, ...],
    plan_prefixes: dict[int, int],
    located: list[AnnotatedBlock | None],
) -> bool:
    """구조·식별자 원문 주석을 본문과 앞선 계획 anchor 수로 탐색.

    Args:
        blocks: locale 문서의 전체 annotation 블록.
        plan_blocks: 계획 anchor로 분류된 블록.
        comments: 구조 주소가 포함된 원문 작성 주석.
        plan_prefixes: 주석별 앞선 계획 anchor 수.
        located: 원문 주석별 위치 누적 목록.

    Returns:
        모든 비계획 주석 occurrence가 유일하게 대응하는지 여부.
    """

    non_plan_groups: dict[tuple[str, int], list[int]] = {}
    for index, comment in enumerate(comments):
        if located[index] is None:
            key = (comment.body, plan_prefixes[index])
            non_plan_groups.setdefault(key, []).append(index)
    for (body, prefix), indexes in non_plan_groups.items():
        candidates = [
            block
            for block in blocks
            if not _is_plan_anchor(block)
            and block.comment == body
            and sum(candidate.start < block.start for candidate in plan_blocks) == prefix
        ]
        if len(candidates) != len(indexes):
            return False
        for index, block in zip(indexes, candidates, strict=True):
            located[index] = block
    return True


def _source_comment_placement_is_valid(
    lines: list[str],
    block: AnnotatedBlock,
    comment: SourceComment,
    anchor_blocks: list[AnnotatedBlock],
) -> bool:
    """탐색된 원문 주석의 원문값과 이웃 anchor 배치 검증.

    Args:
        lines: 줄바꿈을 보존한 locale 문서 줄.
        block: 탐색된 원문 주석 block.
        comment: 기대 원문 작성 주석.
        anchor_blocks: 순수 번역 계획 anchor 블록.

    Returns:
        주석 원문과 before·after·document 배치 일치 여부.
    """

    end, _body = _read_comment(lines, block.start)
    if "".join(lines[block.start:end]) != comment.raw:
        return False
    if comment.placement == "before":
        if comment.anchor_position >= len(anchor_blocks):
            return False
        return not any(
            line.strip()
            for line in lines[end : anchor_blocks[comment.anchor_position].start]
        )
    if comment.placement == "after":
        if comment.anchor_position == 0:
            return False
        return not any(
            line.strip()
            for line in lines[
                anchor_blocks[comment.anchor_position - 1].end : block.start
            ]
        )
    if comment.placement == "document":
        return not anchor_blocks
    return False


def _is_plan_anchor_comment(comment: str) -> bool:
    """계획 anchor comment 여부."""

    return (
        not is_non_annotatable_line(comment)
        and not is_structural_html_fragment(comment)
        and not _is_inline_code_identifier_list_comment(comment)
    )


def _is_plan_anchor(block: AnnotatedBlock) -> bool:
    """계획 anchor 여부."""

    return _is_plan_anchor_comment(block.comment)


def _is_inline_code_identifier_list_comment(comment: str) -> bool:
    """code identifier list comment 여부."""

    if not _LIST_ITEM_PREFIX_RE.match(comment):
        return False
    if not (inline_code_contents(comment) or html_code_contents(comment)):
        return False
    remainder = strip_html_code_elements(strip_inline_code(comment))
    remainder = re.sub(r"(?:[-*+]|\d+[.)])", " ", remainder)
    return not remainder.strip(" `*_~.,:;()[]&/,+")


def _translated_block_end(lines: list[str], start: int, limit: int) -> int:
    """annotation 다음에 오는 번역 block의 종료 줄 위치."""

    index = start
    seen_content = False
    while index < limit:
        if is_structural_html_line(lines[index]):
            return index
        if not lines[index].strip():
            if seen_content:
                return index + 1
            index += 1
            continue
        seen_content = True
        index += 1
    return index


def _comment_starts(lines: list[str]) -> list[int]:
    """독립 HTML 주석이 시작되는 줄 위치 목록."""

    starts: list[int] = []
    in_code = False
    fence = ""
    for index, line in enumerate(lines):
        token = fence_token(line)
        if token:
            if not in_code:
                in_code = True
                fence = token
            elif closes_fence(line, fence):
                in_code = False
            continue
        stripped = line.lstrip()
        if not in_code and stripped.startswith("<!--"):
            starts.append(index)
    return starts


def _read_comment(lines: list[str], start: int) -> tuple[int, str]:
    """HTML 주석 읽기."""

    line = lines[start]
    if "-->" in line:
        spans = html_comment_spans(line)
        if not spans:
            raise PatchError("invalid HTML comment anchor")
        return start + 1, spans[0][2]

    body: list[str] = []
    index = start + 1
    while index < len(lines):
        if "-->" in lines[index]:
            closing_line = lines[index]
            content_before = closing_line[: closing_line.find("-->")].rstrip("\r\n")
            if content_before:
                body.append(content_before)
            return index + 1, "\n".join(body)
        body.append(lines[index].rstrip("\r\n"))
        index += 1
    raise PatchError("unclosed HTML comment anchor")


def _find_block(
    blocks: list[AnnotatedBlock],
    comment: str,
    *,
    occurrence: int | None = None,
    required: bool = True,
) -> AnnotatedBlock | None:
    """블록 탐색."""

    matches = _matching_blocks(blocks, comment)
    if matches:
        if occurrence is not None:
            if occurrence < len(matches):
                return matches[occurrence]
            matches = []
        else:
            return matches[0]
    if required:
        raise PatchError(
            f"missing existing translation block for: {_normalize_text(comment)}"
        )
    return None


def _find_anchored_blocks(
    blocks: list[AnnotatedBlock],
    anchors: tuple[str, ...],
    *,
    occurrence: int | None = None,
    previous_anchor: str | None = None,
    next_anchor: str | None = None,
    required: bool = True,
) -> tuple[AnnotatedBlock, ...] | None:
    """변경되지 않은 인접 block 내부의 연속 annotation 범위 탐색."""

    if not anchors:
        return None
    candidates = _anchored_block_candidates(blocks, anchors)
    candidates = _filter_anchored_block_candidates(
        blocks,
        candidates,
        previous_anchor=previous_anchor,
        next_anchor=next_anchor,
    )
    if len(candidates) == 1:
        return candidates[0]
    first_matches = _matching_blocks(blocks, anchors[0])
    if occurrence is not None and occurrence < len(first_matches):
        preferred = first_matches[occurrence]
        for candidate in candidates:
            if candidate[0] == preferred:
                return candidate
    if required:
        raise PatchError(
            "missing existing translation block for: "
            + " | ".join(_normalize_text(anchor) for anchor in anchors)
        )
    return None


def _anchored_block_candidates(
    blocks: list[AnnotatedBlock],
    anchors: tuple[str, ...],
) -> list[tuple[AnnotatedBlock, ...]]:
    """연속 annotation anchor와 일치하는 locale 블록 후보 수집.

    Args:
        blocks: locale annotation 블록.
        anchors: 순서가 보존된 원문 annotation anchor.

    Returns:
        연속 block 범위 후보.
    """

    matches = [set(_matching_blocks(blocks, anchor)) for anchor in anchors]
    return [
        tuple(blocks[start : start + len(anchors)])
        for start in range(len(blocks) - len(anchors) + 1)
        if all(
            blocks[start + offset] in anchor_matches
            for offset, anchor_matches in enumerate(matches)
        )
    ]


def _filter_anchored_block_candidates(
    blocks: list[AnnotatedBlock],
    candidates: list[tuple[AnnotatedBlock, ...]],
    *,
    previous_anchor: str | None,
    next_anchor: str | None,
) -> list[tuple[AnnotatedBlock, ...]]:
    """변경되지 않은 이전·다음 anchor로 연속 block 후보 제한.

    Args:
        blocks: locale annotation 블록.
        candidates: 연속 block 범위 후보.
        previous_anchor: 기대 이전 원문 anchor.
        next_anchor: 기대 다음 원문 anchor.

    Returns:
        이웃 anchor 조건을 충족하는 후보.
    """

    if previous_anchor:
        previous = set(_matching_blocks(blocks, previous_anchor))
        if previous:
            candidates = [
                candidate
                for candidate in candidates
                if _neighboring_plan_anchor(blocks, blocks.index(candidate[0]), -1)
                in previous
            ]
    if next_anchor:
        following = set(_matching_blocks(blocks, next_anchor))
        if following:
            candidates = [
                candidate
                for candidate in candidates
                if _neighboring_plan_anchor(blocks, blocks.index(candidate[-1]), 1)
                in following
            ]
    return candidates


def _neighboring_plan_anchor(
    blocks: list[AnnotatedBlock], index: int, direction: int
) -> AnnotatedBlock | None:
    """block 주변에서 계획에 포함된 가장 가까운 anchor."""

    index += direction
    while 0 <= index < len(blocks):
        if _is_plan_anchor(blocks[index]):
            return blocks[index]
        index += direction
    return None


def _matching_blocks(blocks: list[AnnotatedBlock], comment: str) -> list[AnnotatedBlock]:
    """정규화한 annotation이 일치하는 locale block 목록."""

    normalized = _normalize_text(comment)
    exact = [block for block in blocks if block.comment == normalized]
    if exact:
        return exact
    if not _can_match_partial_comment(normalized):
        return []
    candidates = [block for block in blocks if normalized in block.comment]
    return candidates if len(candidates) == 1 else []


def _can_match_partial_comment(normalized: str) -> bool:
    """여러 줄 annotation의 부분 anchor 사용 가능 여부."""

    return any(char.isalpha() for char in normalized)


def _replace_block(
    text: str,
    old_comment: str,
    translated: str,
    *,
    occurrence: int | None = None,
    previous_anchor: str | None = None,
    next_anchor: str | None = None,
    anchors: tuple[str, ...] = (),
) -> str:
    """블록 교체."""

    lines = text.splitlines(keepends=True)
    found = _find_anchored_blocks(
        _blocks(text),
        anchors or (old_comment,),
        occurrence=occurrence,
        previous_anchor=previous_anchor,
        next_anchor=next_anchor,
    )
    replacement = _format_replacement(
        translated, trailing=_trailing_separator(found[-1].text)
    )
    return "".join(lines[: found[0].start]) + replacement + "".join(lines[found[-1].end :])


def _replace_resolved_blocks(
    text: str, found: tuple[AnnotatedBlock, ...], translated: str
) -> str:
    """탐색된 블록 교체."""

    lines = text.splitlines(keepends=True)
    replacement = _format_replacement(
        translated, trailing=_trailing_separator(found[-1].text)
    )
    return "".join(lines[: found[0].start]) + replacement + "".join(
        lines[found[-1].end :]
    )


def _replace_segment(text: str, segment: BlockChange, translated: str) -> str:
    """segment 교체."""

    blocks = _blocks(text)
    old_found = _find_old_blocks(blocks, segment, required=False)
    if old_found is None and _find_applied_new_blocks(blocks, segment):
        return text
    try:
        return _replace_block(
            text,
            segment.old_source or _joined(segment.old_lines),
            translated,
            occurrence=segment.old_block_ordinal,
            previous_anchor=segment.old_previous_anchor,
            next_anchor=segment.old_next_anchor,
            anchors=segment.old_anchors,
        )
    except PatchError:
        if segment.old_anchors or segment.new_anchors:
            raise
        if _single_table_row_lines(segment) is not None:
            table_replaced = _replace_table_row(text, segment, translated)
            if table_replaced is not None:
                return table_replaced
            raise
        replaced = _replace_between_raw_contexts(text, segment, translated)
        if replaced is not None:
            return replaced
        raise


def _find_old_blocks(
    blocks: list[AnnotatedBlock],
    segment: BlockChange,
    *,
    required: bool = True,
) -> tuple[AnnotatedBlock, ...] | None:
    """기존 블록 탐색."""

    old_anchor = segment.old_source or _joined(segment.old_lines)
    if not old_anchor:
        return None
    return _find_anchored_blocks(
        blocks,
        segment.old_anchors or (old_anchor,),
        occurrence=segment.old_block_ordinal,
        previous_anchor=segment.old_previous_anchor,
        next_anchor=segment.old_next_anchor,
        required=required,
    )


def _find_applied_new_blocks(
    blocks: list[AnnotatedBlock], segment: BlockChange
) -> tuple[AnnotatedBlock, ...] | None:
    """이미 적용된 신규 블록 탐색."""

    if not segment.new_source:
        return None
    if (
        segment.new_anchor
        and segment.new_anchor_occurrences is not None
        and len(_matching_blocks(blocks, segment.new_anchor))
        < segment.new_anchor_occurrences
    ):
        return None
    return _find_anchored_blocks(
        blocks,
        segment.new_anchors or (segment.new_anchor or segment.new_source,),
        occurrence=segment.new_block_ordinal,
        previous_anchor=segment.new_previous_anchor,
        next_anchor=segment.new_next_anchor,
        required=False,
    )


def _delete_block(
    text: str,
    old_comment: str,
    *,
    occurrence: int | None = None,
    previous_anchor: str | None = None,
    next_anchor: str | None = None,
    anchors: tuple[str, ...] = (),
) -> str:
    """블록 삭제."""

    lines = text.splitlines(keepends=True)
    found = _find_anchored_blocks(
        _blocks(text),
        anchors or (old_comment,),
        occurrence=occurrence,
        previous_anchor=previous_anchor,
        next_anchor=next_anchor,
    )
    return "".join(lines[: found[0].start]) + "".join(lines[found[-1].end :])


def _delete_resolved_blocks(
    text: str, found: tuple[AnnotatedBlock, ...]
) -> str:
    """탐색된 블록 삭제."""

    lines = text.splitlines(keepends=True)
    return "".join(lines[: found[0].start]) + "".join(lines[found[-1].end :])


def _insert_fenced_code_block(
    text: str, segment: BlockChange, translated: str
) -> str:
    """계획의 구조 주소에 fenced code block 삽입."""

    expected = segment.inserted_code_block
    index = segment.inserted_code_block_index
    if expected is None or index is None:
        raise PatchError("missing fenced code block selected for insertion")
    if translated.strip() != expected:
        raise PatchError("provider-free fenced code insertion has diverged")

    lines = text.splitlines(keepends=True)
    plain_lines = [line.rstrip("\r\n") for line in lines]
    regions = _code_fence_regions(plain_lines)
    if not regions:
        return _insert_block(text, segment, expected, force=True)
    if index < len(regions):
        start = regions[index][0]
        insertion = expected.rstrip("\n") + "\n\n"
        return "".join(lines[:start]) + insertion + "".join(lines[start:])
    if index == len(regions):
        end = regions[-1][1] + 1
        insertion = "\n" + expected.rstrip("\n") + "\n"
        return "".join(lines[:end]) + insertion + "".join(lines[end:])
    raise PatchError("fenced code insertion index exceeds source state")


def _delete_fenced_code_block(text: str, segment: BlockChange) -> str:
    """fenced code block 삭제."""

    lines = text.splitlines(keepends=True)
    plain_lines = [line.rstrip("\r\n") for line in lines]
    regions = _code_fence_regions(plain_lines)
    index = segment.deleted_code_block_index
    if index is None or not 0 <= index < len(regions):
        raise PatchError("missing fenced code block selected for deletion")

    start, end = regions[index]
    actual = "\n".join(plain_lines[start : end + 1])
    if actual != segment.deleted_code_block:
        raise PatchError("fenced code block selected for deletion has diverged")

    delete_end = end + 1
    while delete_end < len(lines) and not lines[delete_end].strip():
        delete_end += 1
    if delete_end == len(lines):
        while start > 0 and not lines[start - 1].strip():
            start -= 1
    return "".join(lines[:start]) + "".join(lines[delete_end:])


def _delete_segment(text: str, segment: BlockChange) -> str:
    """segment 삭제."""

    try:
        return _delete_block(
            text,
            segment.old_source or _joined(segment.old_lines),
            occurrence=segment.old_block_ordinal,
            previous_anchor=segment.old_previous_anchor,
            next_anchor=segment.old_next_anchor,
            anchors=segment.old_anchors,
        )
    except PatchError:
        if segment.old_anchors or segment.new_anchors:
            raise
        if _deletion_boundary_is_empty(text, segment):
            return text
        if not _raw_evidence_lines(segment):
            raise
        replaced = _replace_between_raw_contexts(text, segment, "")
        if replaced is not None:
            return replaced
        raise


def _reject_target_deletion_residue(text: str, segment: BlockChange) -> None:
    """대상 상태에 남은 삭제 잔여물 검증."""

    evidence = _raw_evidence_lines(segment)
    lines = text.splitlines(keepends=True)
    blocks = _blocks(text)
    bounds = _raw_context_bounds(
        lines,
        blocks,
        segment,
        match_evidence=False,
    )
    if bounds is None:
        return
    start, end = bounds
    unowned = [
        line
        for index, line in enumerate(lines[start:end], start=start)
        if not any(block.start <= index < block.end for block in blocks)
    ]
    if evidence and _contains_ordered_raw_lines(unowned, evidence):
        raise PatchError("deleted source remains outside its annotated block")
    if any(_is_orphan_translation_line(line) for line in unowned):
        raise PatchError(
            "deleted source translation remains outside its annotated block"
        )


def _is_orphan_translation_line(line: str) -> bool:
    """소유 annotation이 없는 번역 줄 여부."""

    stripped = line.strip()
    if not stripped:
        return False
    if is_named_anchor_line(line) or is_structural_html_line(line):
        return False
    return not is_non_annotatable_line(line)


def _require_target_block_bodies(text: str, segment: BlockChange) -> None:
    """대상 상태 block의 번역 본문 존재 여부 검증."""
    if not segment.new_anchors and not segment.new_anchor:
        return
    blocks = _blocks(text)
    found = _find_applied_new_blocks(blocks, segment)
    if not found:
        raise PatchError(
            "missing translated block for target plan state: "
            + (segment.new_anchor or segment.new_anchors[0])
        )
    lines = text.splitlines(keepends=True)
    for block in found:
        comment_end, _body = _read_comment(lines, block.start)
        if not any(line.strip() for line in lines[comment_end : block.end]):
            raise PatchError(
                f"annotated block is missing its translated body: {block.comment}"
            )


def _deletion_boundary_is_empty(text: str, segment: BlockChange) -> bool:
    """삭제 대상이 있던 위치가 현재 locale에서 비어 있는지 여부."""

    lines = text.splitlines(keepends=True)
    bounds = _raw_context_bounds(
        lines,
        _blocks(text),
        segment,
        match_evidence=False,
    )
    if bounds is None:
        return False
    start, end = bounds
    return not "".join(lines[start:end]).strip()


def _insert_block(
    text: str, segment: BlockChange, translated: str, *, force: bool = False
) -> str:
    """계획의 인접 anchor를 기준으로 번역 block 삽입."""

    lines = text.splitlines(keepends=True)
    blocks = _blocks(text)
    if not force:
        if _find_applied_new_blocks(blocks, segment):
            return text
        if _translated_insertion_exists(text, segment, translated):
            return text
    insertion = _format_replacement(translated, trailing="\n\n")
    existing_insert = _replace_existing_insertion(text, segment, translated)
    if existing_insert is not None:
        return existing_insert
    annotated_boundary = _annotated_insertion_boundary(blocks, segment)
    if annotated_boundary is not None:
        return (
            "".join(lines[:annotated_boundary])
            + insertion
            + "".join(lines[annotated_boundary:])
        )
    raw_insertion = _format_raw_insertion(translated, segment)
    raw_text = _insert_near_raw_context(lines, segment, raw_insertion)
    if raw_text is not None:
        return raw_text
    extended = _replace_leading_code_region_insertion(lines, segment, translated)
    if extended is not None:
        return extended
    windowed = _insert_within_code_region_window(lines, segment, raw_insertion)
    if windowed is not None:
        return windowed
    contextual = _insert_at_annotation_context(
        text,
        lines,
        blocks,
        segment,
        translated,
        insertion,
    )
    if contextual is not None:
        return contextual
    raise PatchError("missing insertion context")


def _insert_at_annotation_context(
    text: str,
    lines: list[str],
    blocks: list[AnnotatedBlock],
    segment: BlockChange,
    translated: str,
    insertion: str,
) -> str | None:
    """이전·다음 annotation 문맥 또는 문서 끝에 번역 블록 삽입.

    Args:
        text: 기존 locale 문서.
        lines: 줄바꿈을 보존한 locale 문서 줄.
        blocks: locale annotation 블록.
        segment: 적용할 삽입 segment.
        translated: provider 번역 블록.
        insertion: 줄바꿈이 정규화된 번역 블록.

    Returns:
        삽입 결과 또는 해석 가능한 문맥이 없으면 ``None``.
    """

    if segment.before_context:
        block = _context_anchor_block(
            blocks,
            segment.before_context,
            segment.old_previous_anchor,
            segment.old_previous_anchor_ordinal,
        )
        if block:
            separator = "" if block.text.endswith("\n\n") else "\n"
            return (
                "".join(lines[: block.end])
                + separator
                + insertion
                + "".join(lines[block.end :])
            )
    if segment.after_context:
        block = _context_anchor_block(
            blocks,
            segment.after_context,
            segment.old_next_anchor,
            segment.old_next_anchor_ordinal,
        )
        if block:
            return "".join(lines[: block.start]) + insertion + "".join(lines[block.start :])
    if segment.after_context is None and segment.before_context:
        # 원문 끝 추가는 이전 문맥의 번역 여부와 관계없이 같은 경계 사용
        return text.rstrip("\n") + "\n\n" + _format_replacement(translated, trailing="\n")
    return None


def _context_anchor_block(
    blocks: list[AnnotatedBlock],
    context: str,
    neighbor_anchor: str | None,
    neighbor_ordinal: int | None,
) -> AnnotatedBlock | None:
    """출현 순서를 고려한 문맥 줄과 annotation block 대응.

    중복 문맥이 인접 block 자체일 때 원문 측 ordinal로 해석하고 그 밖의 문맥은 고유성 요구.
    """
    matches = _matching_blocks(blocks, context)
    if not matches:
        return None
    if (
        neighbor_ordinal is not None
        and neighbor_anchor is not None
        and _normalize_text(context) == _normalize_text(neighbor_anchor)
    ):
        return matches[neighbor_ordinal] if neighbor_ordinal < len(matches) else None
    if len(matches) == 1:
        return matches[0]
    return None


def _replace_leading_code_region_insertion(
    lines: list[str], segment: BlockChange, translated: str
) -> str | None:
    """주변 원문 영역이 확장된 기존 code block의 연장.

    diff alignment로 삽입 범위가 기존 fenced block부터 시작하는 경우 해당 block을 byte 그대로 탐색한 뒤 확장된 전체 영역으로 제자리 교체.
    """
    source = segment.new_source
    if not source:
        return None
    source_lines = source.rstrip("\n").split("\n")
    if not source_lines or not fence_token(source_lines[0]):
        return None
    regions = _code_fence_regions(source_lines)
    if not regions or regions[0][0] != 0:
        return None
    leading_end = regions[0][1]
    if not any(line.strip() for line in source_lines[leading_end + 1 :]):
        return None
    leading = source_lines[: leading_end + 1]
    plain = [line.rstrip("\r\n") for line in lines]
    matches = [
        (start, end)
        for start, end in _code_fence_regions(plain)
        if plain[start : end + 1] == leading
    ]
    if len(matches) != 1:
        return None
    start, end = matches[0]
    ending = "\n" if lines[end].endswith("\n") else ""
    return (
        "".join(lines[:start])
        + translated.rstrip("\n")
        + ending
        + "".join(lines[end + 1 :])
    )


def _insert_within_code_region_window(
    lines: list[str], segment: BlockChange, insertion: str
) -> str | None:
    """원문에서 삽입 위치를 둘러싼 code region 사이에 삽입."""
    offset = segment.inserted_code_block_index
    if offset is None:
        return None
    plain = [line.rstrip("\r\n") for line in lines]
    regions = _code_fence_regions(plain)
    if offset > len(regions):
        return None
    window_start = regions[offset - 1][1] + 1 if offset else 0
    window_end = regions[offset][0] if offset < len(regions) else len(lines)
    if segment.after_context:
        matches = [
            index
            for index in _raw_context_indexes(lines, segment.after_context)
            if window_start <= index < window_end
        ]
        if len(matches) == 1:
            return (
                "".join(lines[: matches[0]])
                + insertion
                + "".join(lines[matches[0] :])
            )
    if segment.before_context:
        matches = [
            index
            for index in _raw_context_indexes(lines, segment.before_context)
            if window_start <= index < window_end
        ]
        if len(matches) == 1:
            index = matches[0] + 1
            return "".join(lines[:index]) + insertion + "".join(lines[index:])
    if segment.before_context is None or fence_token(segment.before_context):
        index = next(
            (
                position
                for position in range(window_start, window_end)
                if lines[position].strip()
            ),
            window_end,
        )
        separator = "\n" if index == window_start and window_start else ""
        return (
            "".join(lines[:index])
            + separator
            + insertion
            + "".join(lines[index:])
        )
    return None


def _raw_line_indexes(lines: list[str], expected: str) -> list[int]:
    """원문 줄과 byte 단위로 일치하는 줄 위치 목록."""

    return [
        index
        for index in _searchable_raw_indexes(lines)
        if lines[index].rstrip("\r\n") == expected
    ]


def _apply_named_anchor_change(
    text: str, segment: BlockChange, translated: str | None
) -> str:
    """named anchor 변경 적용."""

    old_lines = _meaningful_lines(segment.old_lines)
    new_lines = _meaningful_lines(segment.new_lines)
    old_anchor = old_lines[0] if old_lines else None
    new_anchor = new_lines[0] if new_lines else None
    lines = text.splitlines(keepends=True)

    if new_anchor is not None:
        _validate_named_anchor_translation(new_anchor, translated)
        if _named_anchor_target_is_applied(text, lines, new_anchor, segment):
            return text
    if old_anchor is not None:
        return _replace_or_delete_named_anchor(
            text,
            lines,
            old_anchor,
            new_anchor,
            translated,
            segment,
        )
    if new_anchor is None or translated is None:
        raise PatchError("named anchor insertion is missing its target")
    insertion = _format_raw_insertion(translated, segment)
    annotated_index = _named_anchor_insertion_boundary(
        _blocks(text), segment
    )
    if annotated_index is not None:
        return (
            "".join(lines[:annotated_index])
            + insertion
            + "".join(lines[annotated_index:])
        )
    inserted = _insert_near_raw_context(lines, segment, insertion)
    if inserted is None:
        raise PatchError("missing named anchor insertion context")
    return inserted


def _validate_named_anchor_translation(
    new_anchor: str,
    translated: str | None,
) -> None:
    """provider-free named anchor 결과가 목표 원문과 같은지 검증.

    Args:
        new_anchor: 목표 named anchor 줄.
        translated: provider-free 렌더링 결과.

    Raises:
        PatchError: 결과가 목표 anchor와 다름.
    """

    if translated is None or translated.strip() != new_anchor:
        raise PatchError("provider-free named anchor change has diverged")


def _named_anchor_target_is_applied(
    text: str,
    lines: list[str],
    new_anchor: str,
    segment: BlockChange,
) -> bool:
    """목표 named anchor occurrence와 구조 위치가 이미 적용됐는지 판정.

    Args:
        text: 기존 locale 문서.
        lines: 줄바꿈을 보존한 locale 문서 줄.
        new_anchor: 목표 named anchor 줄.
        segment: 적용할 anchor 변경 segment.

    Returns:
        목표 occurrence가 이미 존재하는지 여부.

    Raises:
        PatchError: occurrence는 있지만 구조 위치가 목표와 다름.
    """

    target_count = segment.new_anchor_occurrences
    matches = _raw_line_indexes(lines, new_anchor)
    if target_count is None or len(matches) < target_count:
        return False
    placement = _anchor_occurrence_at_context(lines, _blocks(text), matches, segment)
    if placement is False:
        raise PatchError(
            "existing named anchor placement does not match the target: " + new_anchor
        )
    return True


def _replace_or_delete_named_anchor(
    text: str,
    lines: list[str],
    old_anchor: str,
    new_anchor: str | None,
    translated: str | None,
    segment: BlockChange,
) -> str:
    """기존 named anchor occurrence를 교체 또는 삭제.

    Args:
        text: 기존 locale 문서.
        lines: 줄바꿈을 보존한 locale 문서 줄.
        old_anchor: 변경 이전 named anchor 줄.
        new_anchor: 목표 named anchor 줄 또는 삭제를 뜻하는 ``None``.
        translated: provider-free 렌더링 결과.
        segment: 적용할 anchor 변경 segment.

    Returns:
        anchor 교체·삭제 결과 또는 이미 적용된 문서.
    """

    matches = _raw_line_indexes(lines, old_anchor)
    if (
        new_anchor is None
        and segment.new_anchor_occurrences is not None
        and len(matches) <= segment.new_anchor_occurrences
    ):
        placement = _anchor_occurrence_at_context(lines, _blocks(text), matches, segment)
        if placement is True:
            raise PatchError(
                "deleted named anchor still occupies its source position: " + old_anchor
            )
        return text
    occurrence = segment.old_block_ordinal or 0
    if occurrence >= len(matches):
        raise PatchError(f"missing existing named anchor: {old_anchor}")
    index = matches[occurrence]
    if new_anchor is None:
        return "".join(lines[:index] + lines[index + 1 :])
    if translated is None:
        raise PatchError("named anchor replacement is missing its target")
    ending = "\n" if lines[index].endswith("\n") else ""
    replacement = translated.rstrip("\r\n") + ending
    return "".join(lines[:index]) + replacement + "".join(lines[index + 1 :])


def _anchor_occurrence_at_context(
    lines: list[str],
    blocks: list[AnnotatedBlock],
    anchor_indexes: list[int],
    segment: BlockChange,
) -> bool | None:
    """segment 문맥 경계에 anchor가 존재하는지 여부.

    두 문맥 모두 문서에서 해석되지 않을 때 ``None`` 반환.
    이 경우 출현 횟수만 검증 가능.
    """
    after_checked, after_matched = _anchor_after_context_match(
        lines,
        blocks,
        anchor_indexes,
        segment.after_context,
    )
    if after_matched:
        return True
    before_checked, before_matched = _anchor_before_context_match(
        lines,
        blocks,
        anchor_indexes,
        segment.before_context,
    )
    if before_matched:
        return True
    return False if after_checked or before_checked else None


def _anchor_after_context_match(
    lines: list[str],
    blocks: list[AnnotatedBlock],
    anchor_indexes: list[int],
    context: str | None,
) -> tuple[bool, bool]:
    """named anchor가 다음 문맥 바로 앞에 있는지 판정.

    Args:
        lines: 줄바꿈을 보존한 locale 문서 줄.
        blocks: locale annotation 블록.
        anchor_indexes: named anchor 줄 위치.
        context: 변경 다음 원문 문맥.

    Returns:
        문맥 해석 여부와 anchor 배치 일치 여부.
    """

    if not context:
        return False, False
    following_blocks = _matching_blocks(blocks, context)
    raw_following = _raw_context_indexes(lines, context)
    boundaries = [block.start for block in following_blocks] + raw_following
    matched = any(
        index < boundary
        and _only_anchor_or_blank_between(lines, index + 1, boundary)
        for index in anchor_indexes
        for boundary in boundaries
    )
    return bool(boundaries), matched


def _anchor_before_context_match(
    lines: list[str],
    blocks: list[AnnotatedBlock],
    anchor_indexes: list[int],
    context: str | None,
) -> tuple[bool, bool]:
    """named anchor가 이전 문맥 바로 뒤에 있는지 판정.

    Args:
        lines: 줄바꿈을 보존한 locale 문서 줄.
        blocks: locale annotation 블록.
        anchor_indexes: named anchor 줄 위치.
        context: 변경 이전 원문 문맥.

    Returns:
        문맥 해석 여부와 anchor 배치 일치 여부.
    """

    if not context:
        return False, False
    previous_blocks = _matching_blocks(blocks, context)
    raw_previous = _raw_context_indexes(lines, context)
    boundaries = [block.end for block in previous_blocks] + [
        position + 1 for position in raw_previous
    ]
    matched = any(
        boundary <= index and _only_anchor_or_blank_between(lines, boundary, index)
        for index in anchor_indexes
        for boundary in boundaries
    )
    return bool(boundaries), matched


def _only_anchor_or_blank_between(lines: list[str], start: int, end: int) -> bool:
    """범위 안에 named anchor와 빈 줄만 있는지 여부."""

    return all(
        not line.strip() or is_named_anchor_line(line) for line in lines[start:end]
    )


def _apply_admonition_marker_change(
    text: str, segment: BlockChange, translated: str | None
) -> str:
    """admonition marker 변경 적용."""

    old_marker = _meaningful_lines(segment.old_lines)[0].strip()
    new_marker = _meaningful_lines(segment.new_lines)[0].strip()
    translated_lines = _validated_admonition_translation(new_marker, translated)
    expected_lines = [
        line for line in (segment.new_source or "").splitlines() if line.strip()
    ]
    lines = text.splitlines(keepends=True)
    index = _admonition_change_index(lines, segment, old_marker)
    line = lines[index]
    stripped = line.strip()
    current_type = _admonition_marker_type(stripped)
    old_type = _admonition_marker_type(old_marker)
    new_type = _admonition_marker_type(new_marker)
    if current_type == new_type and stripped == new_marker:
        return text
    if current_type != old_type and current_type != new_type:
        raise PatchError(
            f"existing admonition marker does not match the plan: {old_marker}"
        )

    if len(expected_lines) > 1 and len(translated_lines) <= 1:
        raise PatchError("translated admonition body is missing")
    if len(expected_lines) > 1:
        return _replace_admonition_block(text, lines, index, translated or "")
    if not _admonition_body_matches_source(lines, index, segment):
        raise PatchError(
            "could not verify existing admonition body: "
            + (segment.after_context or old_marker)
        )

    return _replace_admonition_marker_line(
        text,
        lines,
        index,
        new_marker,
        old_marker,
        old_type,
        new_type,
    )


def _validated_admonition_translation(
    new_marker: str,
    translated: str | None,
) -> list[str]:
    """admonition marker 번역 결과의 목표 유형 검증.

    Args:
        new_marker: 목표 admonition marker.
        translated: provider 번역 결과.

    Returns:
        공백 줄을 제거한 번역 결과 줄.

    Raises:
        PatchError: 번역 결과가 없거나 marker 유형이 다름.
    """

    lines = (
        [line for line in translated.splitlines() if line.strip()]
        if translated is not None
        else []
    )
    if not lines or _admonition_marker_type(lines[0]) != _admonition_marker_type(
        new_marker
    ):
        raise PatchError("translated admonition marker change has diverged")
    return lines


def _admonition_change_index(
    lines: list[str],
    segment: BlockChange,
    old_marker: str,
) -> int:
    """계획 ordinal에 해당하는 기존 locale admonition marker 위치 탐색.

    Args:
        lines: 줄바꿈을 보존한 locale 문서 줄.
        segment: 적용할 admonition 변경 segment.
        old_marker: 오류 보고용 변경 이전 marker.

    Returns:
        기존 marker 줄 위치.

    Raises:
        PatchError: ordinal 또는 전체 marker 수가 계획과 다름.
    """

    starts = _admonition_start_indexes(lines)
    ordinal = segment.old_block_ordinal
    if (
        ordinal is None
        or ordinal >= len(starts)
        or not _admonition_marker_count_matches(len(starts), segment)
    ):
        raise PatchError(f"missing existing admonition marker: {old_marker}")
    return starts[ordinal]


def _replace_admonition_block(
    text: str,
    lines: list[str],
    index: int,
    translated: str,
) -> str:
    """본문을 포함한 admonition 블록 전체 교체.

    Args:
        text: 기존 locale 문서.
        lines: 줄바꿈을 보존한 locale 문서 줄.
        index: 기존 marker 줄 위치.
        translated: marker와 본문을 포함한 번역 결과.

    Returns:
        교체 결과 또는 이미 같은 문서.
    """

    end = index + 1
    while end < len(lines) and lines[end].strip().startswith(">"):
        end += 1
    current = "".join(lines[index:end])
    replacement = _format_replacement(
        translated,
        trailing=_trailing_separator(current),
    )
    if current == replacement:
        return text
    return "".join(lines[:index]) + replacement + "".join(lines[end:])


def _replace_admonition_marker_line(
    text: str,
    lines: list[str],
    index: int,
    new_marker: str,
    old_marker: str,
    old_type: str | None,
    new_type: str | None,
) -> str:
    """표준 또는 legacy admonition marker 한 줄 교체.

    Args:
        text: 기존 locale 문서.
        lines: 줄바꿈을 보존한 locale 문서 줄.
        index: 기존 marker 줄 위치.
        new_marker: 목표 marker.
        old_marker: 오류 보고용 변경 이전 marker.
        old_type: 변경 이전 admonition 유형.
        new_type: 목표 admonition 유형.

    Returns:
        marker 교체 결과.

    Raises:
        PatchError: 기존 줄이 지원되는 marker 형태가 아님.
    """

    line = lines[index]
    stripped = line.strip()
    current_type = _admonition_marker_type(stripped)
    prefix = line[: len(line) - len(line.lstrip(" \t"))]
    ending = line[len(line.rstrip("\r\n")) :]
    if current_type in (old_type, new_type) and _ADMONITION_MARKER_RE.fullmatch(
        stripped
    ):
        return (
            "".join(lines[:index])
            + prefix
            + new_marker
            + ending
            + "".join(lines[index + 1 :])
        )
    legacy = _LEGACY_ADMONITION_RE.match(stripped)
    if legacy is not None:
        rest = legacy.group("body").strip()
        replacement = prefix + new_marker + ending
        if rest:
            replacement = (
                prefix
                + new_marker
                + ending
                + prefix
                + "> "
                + rest
                + ending
            )
        return "".join(lines[:index]) + replacement + "".join(lines[index + 1 :])
    raise PatchError(
        f"existing admonition marker does not match the plan: {old_marker}"
    )


def _admonition_marker_type(line: str) -> str | None:
    """blockquote 줄의 지원되는 admonition 종류."""

    marker = _ADMONITION_MARKER_RE.fullmatch(line.strip())
    if marker is not None:
        return marker.group(1).upper()
    legacy = _LEGACY_ADMONITION_RE.match(line.strip())
    if legacy is None:
        return None
    label = legacy.group("braced") or legacy.group("strong")
    return _LEGACY_ADMONITION_TYPES.get(label.lower(), label.upper())


def _admonition_body_matches_source(
    lines: list[str],
    target: int,
    segment: BlockChange,
) -> bool:
    """locale admonition 본문이 원문 구조 주소와 일치하는지 여부."""

    quote_starts = _blockquote_start_indexes(lines)
    context = segment.after_context
    if context is None or not context.strip().startswith(">"):
        return False
    expected = _normalize_text(context.strip()[1:].lstrip())
    matches: list[int] = []
    for start in quote_starts:
        for offset, line in enumerate(lines[start:]):
            stripped = line.strip()
            if offset and not stripped.startswith(">"):
                break
            body = stripped[1:].lstrip()
            if _normalize_text(body) == expected or any(
                _normalize_text(comment) == expected
                for _begin, _end, comment in html_comment_spans(body)
            ):
                matches.append(start)
                break
    return matches == [target]


def _blockquote_start_indexes(lines: list[str]) -> list[int]:
    """code 외부 최상위 blockquote group의 시작 index 목록."""
    starts: list[int] = []
    searchable = set(_searchable_raw_indexes(lines))
    previous_quote = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if index not in searchable:
            previous_quote = stripped.startswith(">")
            continue
        if not stripped:
            previous_quote = False
            continue
        is_quote = stripped.startswith(">")
        if is_quote and not previous_quote:
            starts.append(index)
        previous_quote = is_quote
    return starts


def _admonition_start_indexes(lines: list[str]) -> list[int]:
    """code 외부의 GFM 또는 legacy admonition 시작 줄 index 목록."""
    return [
        index
        for index in _blockquote_start_indexes(lines)
        if _ADMONITION_MARKER_RE.fullmatch(lines[index].strip())
        or _LEGACY_ADMONITION_RE.match(lines[index].strip())
    ]


def _admonition_marker_ordinal(source_lines: list[str], lineno: int) -> int:
    """지정한 원문 줄의 admonition marker 순번."""

    starts = _admonition_start_indexes(source_lines)
    target = lineno - 1
    if target not in starts:
        raise PatchError("source admonition marker occurrence is missing")
    return starts.index(target)


def _admonition_source_region(
    source_lines: list[str], lineno: int
) -> tuple[str, int, int]:
    """marker와 해당 본문을 포함한 원문 admonition 범위."""

    start = lineno - 1
    if start < 0 or start >= len(source_lines):
        raise PatchError("source admonition marker occurrence is missing")
    end = start + 1
    while end < len(source_lines) and source_lines[end].strip().startswith(">"):
        end += 1
    return (
        "\n".join(source_lines[start:end]).rstrip("\n") + "\n",
        start + 1,
        end,
    )


def _named_anchor_insertion_boundary(
    blocks: list[AnnotatedBlock], segment: BlockChange
) -> int | None:
    """named anchor 주변의 유일한 삽입 경계."""

    previous = (
        _matching_blocks(blocks, segment.before_context)
        if segment.before_context
        else []
    )
    following = (
        _matching_blocks(blocks, segment.after_context)
        if segment.after_context
        else []
    )
    if previous and following:
        pairs = [
            (right.start - left.end, right.start)
            for left in previous
            for right in following
            if left.end <= right.start
        ]
        if pairs:
            distance = min(pair[0] for pair in pairs)
            indexes = {
                index for pair_distance, index in pairs if pair_distance == distance
            }
            if len(indexes) == 1:
                return indexes.pop()
    if len(following) == 1:
        return following[0].start
    if len(previous) == 1:
        return previous[0].end
    return None


def _annotated_insertion_boundary(
    blocks: list[AnnotatedBlock], segment: BlockChange
) -> int | None:
    """annotation 소유 block 사이의 유일한 삽입 경계."""

    if not segment.new_anchors and not _is_fenced_code_source(segment.new_source or ""):
        return None
    if segment.old_previous_anchor:
        previous = _find_block(
            blocks,
            segment.old_previous_anchor,
            occurrence=segment.old_previous_anchor_ordinal,
            required=False,
        )
        if previous is not None:
            return previous.end
    if segment.old_next_anchor:
        following = _find_block(
            blocks,
            segment.old_next_anchor,
            occurrence=segment.old_next_anchor_ordinal,
            required=False,
        )
        if following is not None:
            return following.start
    return None


def _translated_insertion_exists(
    text: str, segment: BlockChange, translated: str
) -> bool:
    """동일한 번역 삽입이 계획 위치에 이미 존재하는지 여부."""

    lines = text.splitlines(keepends=True)
    bounds = _raw_context_bounds(lines, _blocks(text), segment)
    if bounds is None:
        return False
    start, end = bounds
    region = "".join(lines[start:end]).strip()
    expected = translated.strip()
    if region == expected:
        return True
    if segment.new_anchors:
        return False
    if segment.before_context and not segment.after_context:
        return text.rstrip().endswith(expected)
    if segment.after_context and not segment.before_context:
        return text.lstrip().startswith(expected)
    return False


def _format_replacement(translated: str, *, trailing: str) -> str:
    """replacement 형식화."""

    return translated.rstrip() + trailing


def _trailing_separator(block_text: str) -> str:
    """block 뒤의 빈 줄과 EOF 줄바꿈 구분자."""

    if block_text.endswith("\n\n"):
        return "\n\n"
    if block_text.endswith("\n"):
        return "\n"
    return ""


def _meaningful_lines(lines: tuple[str, ...]) -> tuple[str, ...]:
    """빈 줄을 제외한 원문 줄 목록."""

    return tuple(line for line in lines if line.strip())


def _joined(lines: tuple[str, ...]) -> str:
    """빈 줄을 제외한 원문 줄을 공백으로 결합."""

    return " ".join(_meaningful_lines(lines))


def _normalize_text(text: str) -> str:
    """텍스트 정규화."""

    return normalize_annotation_anchor(text)


def _ensure_single_eof_newline(text: str) -> str:
    """텍스트 끝에 줄바꿈 하나 보장."""

    return text.rstrip("\n") + "\n" if text else text


def _hunk_has_code_fence_change(
    hunk: DiffHunk,
    *,
    old_ignored: set[int] | None = None,
    new_ignored: set[int] | None = None,
) -> bool:
    """diff hunk가 fenced code 경계를 변경하는지 여부."""

    old_ignored = old_ignored or set()
    new_ignored = new_ignored or set()
    return any(
        line.kind in {"add", "delete"}
        and line.old_lineno not in old_ignored
        and line.new_lineno not in new_ignored
        and fence_token(line.text)
        for line in hunk.lines
    )


def _hunk_region_segment(hunk: DiffHunk, source_lines: list[str]) -> BlockChange:
    """확장 전 diff hunk 범위의 초기 segment."""

    before = _before_hunk_context_line(hunk)
    after = _after_hunk_context_line(hunk)
    new_linenos = tuple(
        line.new_lineno
        for line in hunk.lines
        if line.kind == "add" and line.new_lineno is not None
    )
    if not new_linenos:
        return BlockChange(
            old_lines=tuple(line.text for line in hunk.lines if line.kind == "delete"),
            new_lines=(),
            before_context=_context_text(before),
            after_context=_context_text(after),
            old_linenos=tuple(
                line.old_lineno
                for line in hunk.lines
                if line.kind == "delete" and line.old_lineno is not None
            ),
            before_old_lineno=before.old_lineno if before else None,
            before_new_lineno=before.new_lineno if before else None,
            after_old_lineno=after.old_lineno if after else None,
            after_new_lineno=after.new_lineno if after else None,
        )

    start, end = _expanded_source_range(new_linenos, source_lines)
    new_source = "\n".join(source_lines[start : end + 1]) + "\n"
    return BlockChange(
        old_lines=tuple(line.text for line in hunk.lines if line.kind == "delete"),
        new_lines=tuple(line.text for line in hunk.lines if line.kind == "add"),
        before_context=_context_text(before),
        after_context=_context_text(after),
        old_linenos=tuple(
            line.old_lineno
            for line in hunk.lines
            if line.kind == "delete" and line.old_lineno is not None
        ),
        new_linenos=new_linenos,
        before_old_lineno=before.old_lineno if before else None,
        before_new_lineno=before.new_lineno if before else None,
        after_old_lineno=after.old_lineno if after else None,
        after_new_lineno=after.new_lineno if after else None,
        new_source=new_source,
        new_anchor=(
            _primary_source_anchor(new_source)
            if not any(
                line.kind == "delete" and line.text.strip() for line in hunk.lines
            )
            else None
        ),
        new_block_start=start + 1,
        new_block_end=end + 1,
    )


def _before_hunk_context_line(hunk: DiffHunk) -> DiffLine | None:
    """hunk 이전에 남은 가장 가까운 문맥 줄."""

    context: DiffLine | None = None
    for line in hunk.lines:
        if line.kind != "context":
            return context
        if _normalize_text(line.text):
            context = line
    return context


def _after_hunk_context_line(hunk: DiffHunk) -> DiffLine | None:
    """hunk 이후에 남은 가장 가까운 문맥 줄."""

    context: DiffLine | None = None
    for line in reversed(hunk.lines):
        if line.kind != "context":
            return context
        if _normalize_text(line.text):
            context = line
    return context


def _expanded_source_range(
    linenos: tuple[int, ...], source_lines: list[str]
) -> tuple[int, int]:
    """변경 줄을 완전한 원문 소유 block 범위로 확장."""

    regions = _code_fence_regions(source_lines)
    starts: list[int] = []
    ends: list[int] = []
    for lineno in linenos:
        index = lineno - 1
        region = _inclusive_region_of_index(regions, index)
        if region is None:
            starts.append(index)
            ends.append(index)
            continue
        starts.append(region[0])
        ends.append(region[1])
    return min(starts), max(ends)


def _inclusive_region_of_index(
    regions: list[tuple[int, int]], index: int
) -> tuple[int, int] | None:
    """지정한 줄을 포함하는 영역 범위."""

    for start, end in regions:
        if start <= index <= end:
            return start, end
    return None


def _expand_to_source_blocks(
    segment: BlockChange,
    *,
    new_source_blocks: list[SourceBlock],
    old_source_blocks: list[SourceBlock],
    new_source_lines: list[str],
    old_source_lines: list[str],
) -> list[BlockChange]:
    """segment를 원문 소유 block과 구조 단위로 확장."""

    if _has_structural_lines(segment.new_lines) or _has_structural_lines(
        segment.old_lines
    ):
        return [_expand_structural_segment(segment, new_source_lines, old_source_lines)]
    new_blocks, old_blocks, unchanged = _resolved_segment_blocks(
        segment,
        new_source_blocks,
        old_source_blocks,
    )
    if unchanged:
        return []
    range_change = _range_block_change(
        segment,
        new_blocks,
        old_blocks,
        new_source_blocks=new_source_blocks,
        old_source_blocks=old_source_blocks,
        new_source_lines=new_source_lines,
        old_source_lines=old_source_lines,
    )
    if range_change is not None:
        return [range_change]
    return _paired_block_changes(
        segment,
        new_blocks,
        old_blocks,
        new_source_blocks,
        old_source_blocks,
    )


def _expand_structural_segment(
    segment: BlockChange,
    new_lines: list[str],
    old_lines: list[str],
) -> BlockChange:
    """구조 줄 변경에 raw 또는 admonition occurrence 주소 부여.

    Args:
        segment: 구조 줄을 포함한 초기 변경.
        new_lines: 현재 영어 원문 줄.
        old_lines: 이전 영어 원문 줄.

    Returns:
        구조 주소가 포함된 변경 segment.
    """

    new_source = segment.new_source or _source_from_lines(segment.new_lines)
    old_ordinal = segment.old_block_ordinal
    old_occurrences = segment.old_anchor_occurrences
    new_occurrences = segment.new_anchor_occurrences
    replacements: dict[str, object] = {}
    if segment.is_named_anchor_change and _meaningful_lines(segment.old_lines):
        old_ordinal = _raw_line_ordinal(
            old_lines,
            _meaningful_lines(segment.old_lines)[0],
            segment.old_linenos[0],
        )
    elif segment.is_admonition_marker_change and segment.old_linenos:
        old_ordinal = _admonition_marker_ordinal(old_lines, segment.old_linenos[0])
        old_occurrences = len(_admonition_start_indexes(old_lines))
        old_source, old_start, old_end = _admonition_source_region(
            old_lines, segment.old_linenos[0]
        )
        new_source, new_start, new_end = _admonition_source_region(
            new_lines, segment.new_linenos[0]
        )
        replacements.update(
            old_source=old_source,
            old_block_start=old_start,
            old_block_end=old_end,
            new_block_start=new_start,
            new_block_end=new_end,
        )
    if segment.is_named_anchor_change:
        meaningful = _meaningful_lines(segment.new_lines) or _meaningful_lines(
            segment.old_lines
        )
        new_occurrences = sum(line == meaningful[0] for line in new_lines)
    elif segment.is_admonition_marker_change:
        new_occurrences = len(_admonition_start_indexes(new_lines))
    new_anchor = segment.new_anchor
    if new_anchor is None and not _meaningful_lines(segment.old_lines):
        new_anchor = _primary_source_anchor(new_source)
    return replace(
        segment,
        new_source=new_source,
        new_anchor=new_anchor,
        old_block_ordinal=old_ordinal,
        old_anchor_occurrences=old_occurrences,
        new_anchor_occurrences=new_occurrences,
        table_row=_source_table_row_change(segment, old_lines),
        **replacements,
    )


def _resolved_segment_blocks(
    segment: BlockChange,
    new_source_blocks: list[SourceBlock],
    old_source_blocks: list[SourceBlock],
) -> tuple[list[SourceBlock], list[SourceBlock], bool]:
    """변경 줄 또는 공유 문맥으로 이전·현재 원문 블록 해석.

    Args:
        segment: 초기 변경 segment.
        new_source_blocks: 현재 원문 블록.
        old_source_blocks: 이전 원문 블록.

    Returns:
        현재 블록, 이전 블록, 의미 없는 공백 변경 여부.
    """

    new_blocks = _blocks_for_linenos(new_source_blocks, segment.new_linenos)
    old_blocks = _blocks_for_linenos(old_source_blocks, segment.old_linenos)
    whitespace = not _meaningful_lines(segment.old_lines) and not _meaningful_lines(
        segment.new_lines
    )
    if whitespace:
        new_blocks = _context_boundary_blocks(
            new_source_blocks, segment.before_new_lineno, segment.after_new_lineno
        )
        old_blocks = _context_boundary_blocks(
            old_source_blocks, segment.before_old_lineno, segment.after_old_lineno
        )
        if [block.text for block in old_blocks] == [block.text for block in new_blocks]:
            return new_blocks, old_blocks, True
    if not new_blocks:
        context = _shared_context_block(
            new_source_blocks, segment.before_new_lineno, segment.after_new_lineno
        )
        if context is not None:
            new_blocks = [context]
    if not old_blocks:
        context = _shared_context_block(
            old_source_blocks, segment.before_old_lineno, segment.after_old_lineno
        )
        if context is not None:
            old_blocks = [context]
    return new_blocks, old_blocks, False


def _range_block_change(
    segment: BlockChange,
    new_blocks: list[SourceBlock],
    old_blocks: list[SourceBlock],
    *,
    new_source_blocks: list[SourceBlock],
    old_source_blocks: list[SourceBlock],
    new_source_lines: list[str],
    old_source_lines: list[str],
) -> BlockChange | None:
    """삽입·개수 변경·삭제 범위를 단일 block range 변경으로 확장.

    Args:
        segment: 초기 변경 segment.
        new_blocks: 변경에 대응하는 현재 원문 블록.
        old_blocks: 변경에 대응하는 이전 원문 블록.
        new_source_blocks: 현재 원문 전체 블록.
        old_source_blocks: 이전 원문 전체 블록.
        new_source_lines: 현재 원문 줄.
        old_source_lines: 이전 원문 줄.

    Returns:
        범위 변경 또는 1:1 블록 처리가 필요하면 ``None``.
    """

    if not old_blocks and len(new_blocks) > 1:
        _require_plain_block_range(new_blocks, new_source_lines)
        return replace(segment, **_new_block_range_fields(new_blocks, new_source_blocks))
    if old_blocks and new_blocks and len(old_blocks) != len(new_blocks):
        _require_plain_block_range(old_blocks, old_source_lines)
        _require_plain_block_range(new_blocks, new_source_lines)
        return replace(
            segment,
            **_old_block_range_fields(old_blocks, old_source_blocks),
            **_new_block_range_fields(new_blocks, new_source_blocks),
        )
    if not new_blocks and old_blocks:
        return replace(segment, **_old_block_range_fields(old_blocks, old_source_blocks))
    if not new_blocks:
        return segment
    return None


def _old_block_range_fields(
    blocks: list[SourceBlock],
    all_blocks: list[SourceBlock],
) -> dict[str, object]:
    """이전 원문 block range의 ``BlockChange`` 필드 구성."""

    return {
        "old_source": _join_source_blocks(blocks),
        "old_anchors": tuple(block.comment for block in blocks),
        "old_block_ordinal": _block_ordinal(all_blocks, blocks[0]),
        "old_block_start": blocks[0].start_lineno,
        "old_block_end": blocks[-1].end_lineno,
        "old_previous_anchor": _range_neighbor_anchor(all_blocks, blocks, -1),
        "old_next_anchor": _range_neighbor_anchor(all_blocks, blocks, 1),
    }


def _new_block_range_fields(
    blocks: list[SourceBlock],
    all_blocks: list[SourceBlock],
) -> dict[str, object]:
    """현재 원문 block range의 ``BlockChange`` 필드 구성."""

    return {
        "new_source": _join_source_blocks(blocks),
        "new_anchor": blocks[0].comment,
        "new_anchors": tuple(block.comment for block in blocks),
        "new_block_ordinal": _block_ordinal(all_blocks, blocks[0]),
        "new_block_start": blocks[0].start_lineno,
        "new_block_end": blocks[-1].end_lineno,
        "new_previous_anchor": _range_neighbor_anchor(all_blocks, blocks, -1),
        "new_next_anchor": _range_neighbor_anchor(all_blocks, blocks, 1),
    }


def _paired_block_changes(
    segment: BlockChange,
    new_blocks: list[SourceBlock],
    old_blocks: list[SourceBlock],
    new_source_blocks: list[SourceBlock],
    old_source_blocks: list[SourceBlock],
) -> list[BlockChange]:
    """대응 원문 블록별 1:1 변경 segment 생성."""

    expanded: list[BlockChange] = []
    previous = segment.before_context
    for index, new_block in enumerate(new_blocks):
        old_block = _paired_old_block(old_blocks, new_blocks, index)
        expanded.append(
            replace(
                segment,
                old_lines=_lines_in_block(segment.old_lines, segment.old_linenos, old_block),
                new_lines=_lines_in_block(segment.new_lines, segment.new_linenos, new_block),
                before_context=previous,
                after_context=segment.after_context if index == len(new_blocks) - 1 else None,
                old_source=old_block.text if old_block is not None else None,
                old_anchors=(old_block.comment,) if old_block is not None else (),
                old_block_ordinal=_block_ordinal(old_source_blocks, old_block) if old_block is not None else None,
                old_block_start=old_block.start_lineno if old_block is not None else None,
                old_block_end=old_block.end_lineno if old_block is not None else None,
                new_source=new_block.text,
                new_anchor=new_block.comment,
                new_anchors=(new_block.comment,),
                new_block_ordinal=_block_ordinal(new_source_blocks, new_block),
                new_block_start=new_block.start_lineno,
                new_block_end=new_block.end_lineno,
            )
        )
        previous = new_block.comment
    return expanded


def _shared_context_block(
    blocks: list[SourceBlock],
    before_lineno: int | None,
    after_lineno: int | None,
) -> SourceBlock | None:
    """앞뒤 문맥 줄이 함께 속한 원문 block."""

    if before_lineno is None or after_lineno is None:
        return None
    before = _block_for_lineno(blocks, before_lineno)
    after = _block_for_lineno(blocks, after_lineno)
    return before if before is not None and before == after else None


def _context_boundary_blocks(
    blocks: list[SourceBlock],
    before_lineno: int | None,
    after_lineno: int | None,
) -> list[SourceBlock]:
    """segment 앞뒤의 변경되지 않은 문맥 block 목록."""

    found: list[SourceBlock] = []
    for lineno in (before_lineno, after_lineno):
        if lineno is None:
            continue
        block = _block_for_lineno(blocks, lineno)
        if block is not None and block not in found:
            found.append(block)
    return found


def _block_for_lineno(
    blocks: list[SourceBlock], lineno: int
) -> SourceBlock | None:
    """지정한 줄 번호를 포함하는 원문 block."""

    return next(
        (
            block
            for block in blocks
            if block.start_lineno <= lineno <= block.end_lineno
        ),
        None,
    )


def _paired_old_block(
    old_blocks: list[SourceBlock],
    new_blocks: list[SourceBlock],
    index: int,
) -> SourceBlock | None:
    """현재 원문 block과 대응하는 이전 원문 block."""

    if len(old_blocks) == len(new_blocks):
        return old_blocks[index]
    return None


def _join_source_blocks(blocks: list[SourceBlock]) -> str:
    """연속 원문 block을 빈 줄 하나로 결합."""

    return "\n\n".join(block.text.rstrip("\n") for block in blocks) + "\n"


def _require_plain_block_range(
    blocks: list[SourceBlock], source_lines: list[str]
) -> None:
    """plain block 범위의 지원 조건 검증."""

    for previous, following in zip(blocks, blocks[1:]):
        between = source_lines[previous.end_lineno : following.start_lineno - 1]
        if any(line.strip() for line in between):
            raise PatchError(
                "changed source block range contains unsupported structural markup"
            )


def _range_neighbor_anchor(
    all_blocks: list[SourceBlock], range_blocks: list[SourceBlock], offset: int
) -> str | None:
    """변경 범위 바깥의 가장 가까운 이웃 anchor."""

    target = range_blocks[0] if offset < 0 else range_blocks[-1]
    index = all_blocks.index(target) + offset
    return all_blocks[index].comment if 0 <= index < len(all_blocks) else None


def _lines_in_block(
    lines: tuple[str, ...],
    linenos: tuple[int, ...],
    block: SourceBlock | None,
) -> tuple[str, ...]:
    """block 범위 안에서 선택된 줄 번호 목록."""

    if block is None:
        return lines
    selected = tuple(
        line
        for line, lineno in zip(lines, linenos, strict=True)
        if block.start_lineno <= lineno <= block.end_lineno
    )
    return selected or lines


def _block_ordinal(blocks: list[SourceBlock], target: SourceBlock) -> int:
    """동일한 원문 block이 출현한 순번."""

    matching = [block for block in blocks if block.comment == target.comment]
    return matching.index(target)


def _primary_source_anchor(source: str) -> str | None:
    """원문 block의 대표 annotation anchor."""

    blocks = _source_blocks(source)
    return blocks[0].comment if blocks else None


def _blocks_for_linenos(
    source_blocks: list[SourceBlock], linenos: tuple[int, ...]
) -> list[SourceBlock]:
    """지정한 줄 번호 집합과 겹치는 원문 block 목록."""

    return [
        block
        for block in source_blocks
        if any(block.start_lineno <= lineno <= block.end_lineno for lineno in linenos)
    ]


def _has_structural_lines(lines: tuple[str, ...]) -> bool:
    """structural 줄 포함 여부."""

    in_code = False
    fence = ""
    for line in lines:
        stripped = line.strip()
        token = fence_token(line)
        if token:
            if not in_code:
                in_code, fence = True, token
            elif closes_fence(line, fence):
                in_code = False
            return True
        if in_code:
            return True
        if is_named_anchor_line(line):
            return True
        if stripped.startswith(("- [", "* [")) and "](#" in stripped:
            return True
        if stripped.startswith((">", "|")):
            return True
    return False


def _raw_line_ordinal(
    source_lines: list[str], expected: str, lineno: int
) -> int:
    """동일한 raw 줄이 원문에 출현한 순번."""

    indexes = [
        index for index, line in enumerate(source_lines) if line == expected
    ]
    target = lineno - 1
    if target not in indexes:
        raise PatchError(f"source line occurrence is missing: {expected}")
    return indexes.index(target)


def _reverse_apply_hunks(new_lines: list[str], hunks: tuple[DiffHunk, ...]) -> list[str]:
    """신규 원문의 각 hunk를 역적용한 이전 원문 줄 재구성."""
    lines = list(new_lines)
    for hunk in sorted(hunks, key=lambda item: item.new_start, reverse=True):
        old_segment = [
            line.text for line in hunk.lines if line.kind in ("context", "delete")
        ]
        new_segment = [
            line.text for line in hunk.lines if line.kind in ("context", "add")
        ]
        start = hunk.new_start - 1
        end = start + hunk.new_count
        if lines[start:end] != new_segment:
            bounds = _locate_hunk_segment(lines, new_segment)
            if bounds is None:
                raise PatchError("source hunk does not match the new document")
            start, end = bounds
        lines[start:end] = old_segment
    return lines


def _locate_hunk_segment(
    lines: list[str], segment: list[str]
) -> tuple[int, int] | None:
    """원문 전체에서 diff hunk의 정확한 segment 위치 탐색."""

    exact = [
        (index, index + len(segment))
        for index in range(len(lines) - len(segment) + 1)
        if lines[index : index + len(segment)] == segment
    ]
    if len(exact) == 1:
        return exact[0]

    meaningful = [line for line in segment if line.strip()]
    if not meaningful:
        return None
    starts = [index for index, line in enumerate(lines) if line == meaningful[0]]
    ends = [index for index, line in enumerate(lines) if line == meaningful[-1]]
    compact = [
        (start, end + 1)
        for start in starts
        for end in ends
        if start <= end
        and [line for line in lines[start : end + 1] if line.strip()] == meaningful
    ]
    return compact[0] if len(compact) == 1 else None


def _code_fence_regions(lines: list[str]) -> list[tuple[int, int]]:
    """각 fenced code block의 시작·종료 줄 index를 포함한 범위 목록."""
    regions: list[tuple[int, int]] = []
    in_code = False
    fence = ""
    start = 0
    for index, line in enumerate(lines):
        token = fence_token(line)
        if not token:
            continue
        if not in_code:
            in_code, fence, start = True, token, index
        elif closes_fence(line, fence):
            in_code = False
            regions.append((start, index))
    return regions


def _code_blocks_from_regions(
    lines: list[str], regions: list[tuple[int, int]]
) -> tuple[str, ...]:
    """줄 범위로 추출한 fenced code block 목록."""

    return tuple("\n".join(lines[start : end + 1]) for start, end in regions)


def _fenced_code_blocks(text: str) -> tuple[str, ...]:
    """문서 순서로 추출한 fenced code block 목록."""

    lines = text.splitlines()
    return _code_blocks_from_regions(lines, _code_fence_regions(lines))


def _is_fenced_code_source(source: str) -> bool:
    """fenced code 원문 여부."""

    lines = source.splitlines()
    regions = _code_fence_regions(lines)
    if len(regions) != 1:
        return False
    start, end = regions[0]
    return not any(line.strip() for line in lines[:start] + lines[end + 1 :])


def _attach_deleted_code_block(
    change: BlockChange,
    *,
    old_source_lines: list[str],
    old_regions: list[tuple[int, int]],
    new_source_lines: list[str],
    new_regions: list[tuple[int, int]],
) -> BlockChange:
    """삭제 segment에 대응하는 fenced code 변경 정보 결합."""

    if change.code_block is not None:
        return change

    inserted_source = change.new_source or _source_from_lines(change.new_lines)
    if not _meaningful_lines(change.old_lines) and _is_fenced_code_source(
        inserted_source
    ):
        index = _single_region_index(new_regions, change.new_linenos)
        if index is not None:
            start, end = new_regions[index]
            return replace(
                change,
                inserted_code_block_index=index,
                inserted_code_block="\n".join(new_source_lines[start : end + 1]),
            )

    if (
        change.inserted_code_block is None
        and not _meaningful_lines(change.old_lines)
        and _meaningful_lines(change.new_lines)
        and any(fence_token(line) for line in change.new_lines)
    ):
        boundary = change.before_old_lineno
        offset = (
            sum(end <= boundary - 1 for _start, end in old_regions)
            if boundary is not None
            else 0
        )
        return replace(change, inserted_code_block_index=offset)

    if _meaningful_lines(change.new_lines) or not any(
        fence_token(line) for line in change.old_lines
    ):
        return change

    index = _single_region_index(old_regions, change.old_linenos)
    if index is None:
        return change
    start, end = old_regions[index]
    return replace(
        change,
        deleted_code_block_index=index,
        deleted_code_block="\n".join(old_source_lines[start : end + 1]),
    )


def _region_of_index(regions: list[tuple[int, int]], index: int) -> int | None:
    """``index``가 fence 내부에 포함된 region의 순번."""
    for position, (start, end) in enumerate(regions):
        if start < index < end:
            return position
    return None


def _code_region_indexes(
    segment: BlockChange,
    new_regions: list[tuple[int, int]],
    old_regions: list[tuple[int, int]],
) -> tuple[int | None, int | None]:
    """fenced code 내부 변경에 대한 신규·이전 region index.

    전체 block 변경은 fence 줄을 포함하여 구조 경로 유지.
    순수 내부 삽입 또는 삭제에서는 문맥 줄 번호로 변경 줄이 없는 쪽 보완.
    """
    if _has_structural_lines(segment.new_lines) or _has_structural_lines(
        segment.old_lines
    ):
        return None, None

    new_index = _single_region_index(new_regions, segment.new_linenos)
    old_index = _single_region_index(old_regions, segment.old_linenos)
    if new_index is None and old_index is None:
        return None, None
    if new_index is None:
        new_index = _single_region_index(
            new_regions,
            tuple(
                line
                for line in (segment.before_new_lineno, segment.after_new_lineno)
                if line is not None
            ),
            inclusive=True,
        )
    if old_index is None:
        old_index = _single_region_index(
            old_regions,
            tuple(
                line
                for line in (segment.before_old_lineno, segment.after_old_lineno)
                if line is not None
            ),
            inclusive=True,
        )
    if new_index is None and old_index is not None and len(new_regions) == len(old_regions):
        new_index = old_index
    if old_index is None and new_index is not None and len(new_regions) == len(old_regions):
        old_index = new_index
    return new_index, old_index


def _single_region_index(
    regions: list[tuple[int, int]],
    linenos: tuple[int, ...],
    *,
    inclusive: bool = False,
) -> int | None:
    """지정한 줄들이 유일하게 속하는 code 영역의 순번."""

    found: set[int] = set()
    for lineno in linenos:
        line_index = lineno - 1
        region_index = next(
            (
                position
                for position, (start, end) in enumerate(regions)
                if (start <= line_index <= end)
                if inclusive or start < line_index < end
            ),
            None,
        )
        if region_index is not None:
            found.add(region_index)
    return found.pop() if len(found) == 1 else None


def _code_block_segment(
    group: list[BlockChange],
    source_lines: list[str],
    region: tuple[int, int],
    block_index: int,
    *,
    old_source_lines: list[str],
    old_regions: list[tuple[int, int]],
    old_block_index: int | None,
) -> BlockChange:
    """단일 code fence를 신규 원문 block으로 byte 단위 교체하는 segment 생성."""
    start, end = region
    new_block_lines = source_lines[start : end + 1]
    new_block = "\n".join(new_block_lines)
    added = {line for segment in group for line in segment.new_lines}
    anchors = tuple(
        line for line in new_block_lines if line.strip() and line not in added
    )
    old_block = None
    if old_block_index is not None and 0 <= old_block_index < len(old_regions):
        old_start, old_end = old_regions[old_block_index]
        old_block = "\n".join(old_source_lines[old_start : old_end + 1])
    return BlockChange(
        old_lines=(),
        new_lines=(),
        before_context=None,
        after_context=None,
        code_block=CodeChange(
            block_index=block_index,
            new_block=new_block,
            anchors=anchors,
            old_block_index=old_block_index,
            old_block=old_block,
            old_block_count=len(old_regions),
            new_block_count=len(_code_fence_regions(source_lines)),
        ),
    )


def _apply_code_block(
    text: str,
    change: CodeChange,
    *,
    state: PlanState = PlanState.UNGUARDED,
) -> str:
    """code 블록 적용."""

    lines = text.split("\n")
    regions = _code_fence_regions(lines)
    candidate_indexes = list(
        dict.fromkeys(
            index
            for index in (change.block_index, change.old_block_index)
            if index is not None and 0 <= index < len(regions)
        )
    )
    new_block = change.new_block.split("\n")
    old_exact = False
    if change.old_block is not None and change.old_block_index in candidate_indexes:
        old_start, old_end = regions[change.old_block_index]
        old_exact = lines[old_start : old_end + 1] == change.old_block.split("\n")
    new_exact = False
    if change.block_index in candidate_indexes:
        new_start, new_end = regions[change.block_index]
        new_exact = lines[new_start : new_end + 1] == new_block

    if state is PlanState.TARGET:
        return text

    target_index = None
    if state is PlanState.SOURCE and old_exact:
        target_index = change.old_block_index
    elif state is PlanState.UNGUARDED:
        if new_exact:
            return text
        if old_exact:
            target_index = change.old_block_index
    if target_index is None:
        matching = [
            index
            for index in candidate_indexes
            if _contains_all(
                lines[regions[index][0] : regions[index][1] + 1],
                change.anchors,
            )
        ]
        if len(matching) != 1:
            return text
        target_index = matching[0]

    start, end = regions[target_index]
    return "\n".join(lines[:start] + new_block + lines[end + 1 :])


def _contains_all(block: list[str], anchors: tuple[str, ...]) -> bool:
    """중복을 포함해 ``block``이 모든 anchor 줄을 포함하는지 여부."""
    remaining = list(block)
    for line in anchors:
        if line in remaining:
            remaining.remove(line)
        else:
            return False
    return True


def _source_from_lines(lines: tuple[str, ...]) -> str:
    """줄 목록을 마지막 줄바꿈 하나가 있는 원문으로 결합."""

    return "\n".join(lines).rstrip("\n") + "\n"


def _format_raw_insertion(translated: str, segment: BlockChange) -> str:
    """raw insertion 형식화."""

    trailing_blank_lines = 0
    for line in reversed(segment.new_lines):
        if line.strip():
            break
        trailing_blank_lines += 1
    if segment.after_new_lineno is not None and segment.new_block_end is not None:
        trailing_blank_lines = max(
            trailing_blank_lines,
            segment.after_new_lineno - segment.new_block_end - 1,
        )
    return translated.rstrip("\n") + ("\n" * max(1, trailing_blank_lines + 1))


def _insert_near_raw_context(
    lines: list[str], segment: BlockChange, insertion: str
) -> str | None:
    """raw 문맥 줄 주변의 유일한 경계에 내용 삽입."""

    index = _raw_insertion_index(lines, segment)
    if index is not None:
        return "".join(lines[:index]) + insertion + "".join(lines[index:])
    return None


def _raw_insertion_index(lines: list[str], segment: BlockChange) -> int | None:
    """raw 문맥으로 결정한 유일한 삽입 줄 위치."""

    before = (
        _raw_context_indexes(lines, segment.before_context)
        if segment.before_context
        else []
    )
    after = (
        _raw_context_indexes(lines, segment.after_context)
        if segment.after_context
        else []
    )

    if before and after:
        pairs = [(right - left, right) for left in before for right in after if left < right]
        if not pairs:
            return None
        distance = min(pair[0] for pair in pairs)
        nearest = [right for pair_distance, right in pairs if pair_distance == distance]
        return nearest[0] if len(nearest) == 1 else None
    if len(after) == 1:
        return after[0]
    if len(before) == 1:
        return before[0] + 1
    return None


def _context_between_raw_contexts(text: str, segment: BlockChange) -> str | None:
    """앞뒤 raw 문맥 사이의 기존 locale 내용."""

    lines = text.splitlines(keepends=True)
    bounds = _raw_context_bounds(lines, _blocks(text), segment)
    if bounds is None:
        return None
    start, end = bounds
    return "".join(lines[start:end])


def _replace_between_raw_contexts(
    text: str, segment: BlockChange, translated: str
) -> str | None:
    """앞뒤 raw 문맥 사이의 내용 교체."""

    lines = text.splitlines(keepends=True)
    bounds = _raw_context_bounds(lines, _blocks(text), segment)
    if bounds is None:
        return None
    start, end = bounds
    replacement = _format_replacement(
        translated,
        trailing=_trailing_separator("".join(lines[start:end])),
    )
    return "".join(lines[:start]) + replacement + "".join(lines[end:])


def _replace_existing_insertion(
    text: str, segment: BlockChange, translated: str
) -> str | None:
    """기존 삽입 내용 교체."""

    lines = text.splitlines(keepends=True)
    start = _find_existing_insertion_start(lines, segment)
    if start is None:
        return None
    end = _find_existing_insertion_end(lines, segment, start)
    if end is None:
        return None
    replacement = _format_replacement(
        translated,
        trailing=_trailing_separator("".join(lines[start:end])),
    )
    return "".join(lines[:start]) + replacement + "".join(lines[end:])


def _find_existing_insertion_start(
    lines: list[str], segment: BlockChange
) -> int | None:
    """기존 삽입 내용의 시작 위치 탐색."""

    for source_line in _source_text_lines(segment):
        if not is_named_anchor_line(source_line):
            continue
        index = _find_raw_context_line(lines, source_line)
        if index is not None:
            return index
    return None


def _find_existing_insertion_end(
    lines: list[str], segment: BlockChange, start: int
) -> int | None:
    """기존 삽입 내용의 종료 위치 탐색."""

    if segment.after_context:
        index = _find_raw_context_line_after(lines, segment.after_context, start)
        if index is not None:
            return index
    for index in range(start + 1, len(lines)):
        if is_named_anchor_line(lines[index]):
            return index
    return len(lines)


def _source_text_lines(segment: BlockChange) -> tuple[str, ...]:
    """segment의 현재 원문을 구성하는 줄 목록."""

    if segment.new_source is not None:
        return tuple(segment.new_source.rstrip("\n").split("\n"))
    return _meaningful_lines(segment.new_lines)


def _raw_context_bounds(
    lines: list[str],
    blocks: list[AnnotatedBlock],
    segment: BlockChange,
    *,
    match_evidence: bool = True,
) -> tuple[int, int] | None:
    """앞뒤 raw 문맥으로 제한한 유일한 줄 범위."""

    if not segment.before_context and not segment.after_context:
        return None

    evidence = _raw_evidence_lines(segment) if match_evidence else ()
    before_bounds = (
        _before_context_boundaries(
            lines,
            blocks,
            segment.before_context,
            include_code=bool(evidence),
        )
        if segment.before_context
        else [0]
    )
    after_bounds = (
        _after_context_boundaries(
            lines,
            blocks,
            segment.after_context,
            include_code=bool(evidence),
        )
        if segment.after_context
        else [len(lines)]
    )
    candidates = list(
        {
            (end - start, start, end)
            for start in before_bounds
            for end in after_bounds
            if start <= end
        }
    )
    if not candidates:
        return None

    if evidence:
        evidenced: list[tuple[int, int, int]] = []
        for _distance, start, end in candidates:
            expanded_end = _expand_end_to_code_fence(lines, end)
            if _contains_ordered_raw_lines(lines[start:expanded_end], evidence):
                evidenced.append((expanded_end - start, start, expanded_end))
        if not evidenced:
            return None
        candidates = evidenced

    distance = min(candidate[0] for candidate in candidates)
    nearest = [candidate for candidate in candidates if candidate[0] == distance]
    if len(nearest) != 1:
        return None
    _distance, start, end = nearest[0]
    return start, _expand_end_to_code_fence(lines, end)


def _raw_evidence_lines(segment: BlockChange) -> tuple[str, ...]:
    """segment 위치를 증명할 구조·코드 원문 줄 목록."""

    return tuple(
        line
        for line in _meaningful_lines(segment.old_lines)
        if _is_raw_evidence_line(line)
    )


def _is_raw_evidence_line(line: str) -> bool:
    """raw 증거 줄 여부."""

    stripped = line.strip()
    if not stripped:
        return False
    return (
        bool(fence_token(line))
        or line[:1].isspace()
        or "\\" in stripped
        or "=>" in stripped
        or "::" in stripped
        or ";" in stripped
        or stripped in {"}", "},", "]", "],", ")", "),"}
    )


def _contains_ordered_raw_lines(lines: list[str], evidence: tuple[str, ...]) -> bool:
    """후보가 raw 증거 줄을 같은 순서로 포함하는지 여부."""

    index = 0
    normalized_lines = [_normalize_text(line) for line in lines]
    for expected in evidence:
        normalized = _normalize_text(expected)
        while index < len(normalized_lines) and normalized_lines[index] != normalized:
            index += 1
        if index >= len(normalized_lines):
            return False
        index += 1
    return True


def _expand_end_to_code_fence(lines: list[str], end: int) -> int:
    """범위 끝이 포함된 fenced code block의 끝까지 확장."""

    plain_lines = [line.rstrip("\r\n") for line in lines]
    for start, region_end in _code_fence_regions(plain_lines):
        if start < end <= region_end or start <= end - 1 < region_end:
            return region_end + 1
    return end


def _before_context_boundaries(
    lines: list[str],
    blocks: list[AnnotatedBlock],
    context: str,
    *,
    include_code: bool = False,
) -> list[int]:
    """이전 raw 문맥으로 가능한 범위 시작 위치 목록."""

    bounds = [block.end for block in _matching_blocks(blocks, context)]
    normalized = _normalize_text(context)
    if normalized:
        bounds.extend(
            index + 1
            for index in _raw_context_indexes(
                lines, context, include_code=include_code
            )
        )
    return bounds


def _after_context_boundaries(
    lines: list[str],
    blocks: list[AnnotatedBlock],
    context: str,
    *,
    include_code: bool = False,
) -> list[int]:
    """다음 raw 문맥으로 가능한 범위 종료 위치 목록."""

    bounds = [block.start for block in _matching_blocks(blocks, context)]
    normalized = _normalize_text(context)
    if normalized:
        bounds.extend(
            _raw_context_indexes(lines, context, include_code=include_code)
        )
    return bounds


def _find_raw_context_line(lines: list[str], context: str) -> int | None:
    """raw 문맥 줄 탐색."""

    indexes = _raw_context_indexes(lines, context)
    return indexes[0] if indexes else None


def _find_raw_context_line_after(
    lines: list[str], context: str, after_index: int
) -> int | None:
    """지정한 위치 다음의 raw 문맥 줄 탐색."""

    return next(
        (
            index
            for index in _raw_context_indexes(lines, context)
            if index > after_index
        ),
        None,
    )


def _raw_context_indexes(
    lines: list[str], context: str, *, include_code: bool = False
) -> list[int]:
    """raw 문맥 줄과 일치하는 검색 가능 위치 목록."""

    normalized = _normalize_text(context)
    if not normalized:
        return []
    return [
        index
        for index in _searchable_raw_indexes(lines, include_code=include_code)
        if _normalize_text(lines[index]) == normalized
    ]


def _searchable_raw_indexes(
    lines: list[str], *, include_code: bool = False
) -> list[int]:
    """코드·주석 경계를 고려한 raw 줄 검색 위치 목록."""

    indexes: list[int] = []
    in_comment = False
    in_code = False
    fence = ""

    for index, line in enumerate(lines):
        in_comment, in_code, fence, searchable = _raw_line_scan_state(
            line,
            in_comment=in_comment,
            in_code=in_code,
            fence=fence,
            include_code=include_code,
        )
        if searchable:
            indexes.append(index)

    return indexes


def _raw_line_scan_state(
    line: str,
    *,
    in_comment: bool,
    in_code: bool,
    fence: str,
    include_code: bool,
) -> tuple[bool, bool, str, bool]:
    """단일 raw 줄의 주석·code 상태와 검색 가능 여부 계산.

    Args:
        line: Markdown 물리 줄.
        in_comment: 이전 줄까지 여러 줄 HTML 주석 내부 여부.
        in_code: 이전 줄까지 fenced code 내부 여부.
        fence: 현재 fenced code 여는 token.
        include_code: code 줄도 검색할지 여부.

    Returns:
        다음 주석 상태, code 상태, fence token, 검색 가능 여부.
    """

    if in_comment:
        return "-->" not in line, in_code, fence, False
    if "<!--" in line:
        continued = "-->" not in line.split("<!--", 1)[1]
        return continued, in_code, fence, False
    token = fence_token(line)
    if not token:
        return False, in_code, fence, not in_code or include_code
    if not in_code:
        return False, True, token, include_code
    if closes_fence(line, fence):
        return False, False, fence, include_code
    return False, in_code, fence, include_code


def _table_row_cells(line: str) -> tuple[str, ...] | None:
    """Markdown table row에서 분리한 cell 목록."""

    raw_cells = gfm_table_row_cells(line)
    if raw_cells is None:
        return None
    cells = tuple(_normalize_text(cell) for cell in raw_cells)
    return cells if cells and any(cells) else None


def _is_unsupported_admonition_marker(line: str) -> bool:
    """지원하지 않는 admonition marker 여부."""

    stripped = line.strip()
    return bool(_ANY_ADMONITION_MARKER_RE.fullmatch(stripped)) and not bool(
        _ADMONITION_MARKER_RE.fullmatch(stripped)
    )


def _require_supported_admonition_markers(source: str) -> None:
    """원문 admonition marker의 지원 여부 검증."""

    lines = source.splitlines()
    fenced = {
        index
        for start, end in _code_fence_regions(lines)
        for index in range(start, end + 1)
    }
    for index, line in enumerate(lines):
        if index in fenced or line.startswith(("    ", "\t")):
            continue
        if _is_unsupported_admonition_marker(line):
            raise PatchError("unsupported admonition marker type")


def _require_supported_modified_admonition(segment: BlockChange) -> None:
    """변경된 admonition marker의 지원 여부 검증."""

    lines = _meaningful_lines(segment.old_lines) + _meaningful_lines(
        segment.new_lines
    )
    if any(
        not line.startswith(("    ", "\t"))
        and _is_unsupported_admonition_marker(line)
        for line in lines
    ):
        raise PatchError("unsupported admonition marker type")


def _table_match_cells(cells: tuple[str, ...]) -> tuple[str, ...]:
    """table row 위치 판정에 사용할 cell 목록 정규화."""

    return tuple(
        re.sub(r"\s*,\s*", ", ", cell.replace("、", ",")).strip()
        for cell in cells
    )


def _is_table_separator_cells(cells: tuple[str, ...]) -> bool:
    """table separator cells 여부."""

    return all(cell and set(cell) <= {"-", ":"} for cell in cells)


def _single_table_row_lines(segment: BlockChange) -> tuple[str, str] | None:
    """segment의 단일 이전·신규 table row 쌍 또는 row 형식이 아닐 때 ``None``."""
    old_meaningful = _meaningful_lines(segment.old_lines)
    new_meaningful = _meaningful_lines(segment.new_lines)
    if len(old_meaningful) != 1 or len(new_meaningful) != 1:
        return None
    old_cells = _table_row_cells(old_meaningful[0])
    new_cells = _table_row_cells(new_meaningful[0])
    if old_cells is None or new_cells is None or len(old_cells) != len(new_cells):
        return None
    if _is_table_separator_cells(old_cells) or _is_table_separator_cells(new_cells):
        return None
    return old_meaningful[0], new_meaningful[0]


def _require_rectangular_create_table(source: str) -> None:
    """신규 table의 직사각형 구조 검증."""

    rows = [line for line in source.splitlines() if line.strip()]
    cells = [_table_row_cells(line) for line in rows]
    if not cells or any(row is None for row in cells):
        raise PatchError("unsupported create table structure")
    widths = {len(row) for row in cells if row is not None}
    if len(widths) != 1:
        raise PatchError("create table must be rectangular")


def _is_changed_table_row(line: str) -> bool:
    """변경 대상 table row 여부."""

    return not line.startswith(("    ", "\t")) and _table_row_cells(line) is not None


def _require_supported_modified_table(
    segment: BlockChange,
    old_source_lines: list[str] | None = None,
) -> bool:
    """변경된 table 구조의 지원 여부 검증.

    이전 원문에 table row가 없고 추가 줄이 구분 행을 포함하는 순수 추가만
    02 §7의 표 create 사례로 보아 직사각형 구조를 검증하고 일반 추가 블록
    경로로 처리한다. 구분 행이 없으면 기존 표에 행을 더한 변경이므로
    아래 단일 행 검사로 내려보내 §7.2 재생성 강등에 맡긴다.
    """

    old_meaningful = _meaningful_lines(segment.old_lines)
    new_meaningful = _meaningful_lines(segment.new_lines)
    owner_is_table = bool(
        old_source_lines is not None
        and _source_table_row_change(segment, old_source_lines) is not None
    ) or is_gfm_pipe_table(
        "\n".join(new_meaningful)
    )
    outer_pipe_row_changed = any(
        line.strip().startswith("|") and line.strip().endswith("|")
        for line in old_meaningful + new_meaningful
    )
    if not owner_is_table and not outer_pipe_row_changed:
        return False
    if not any(
        _is_changed_table_row(line)
        for line in old_meaningful + new_meaningful
    ):
        return False
    added_rows = [line for line in new_meaningful if _is_changed_table_row(line)]
    if not any(_is_changed_table_row(line) for line in old_meaningful) and any(
        _is_table_separator_cells(cells)
        for cells in (_table_row_cells(line) for line in added_rows)
        if cells is not None
    ):
        _require_rectangular_create_table("\n".join(added_rows))
        return False
    if _single_table_row_lines(segment) is None:
        raise PatchError(
            "modified table must change exactly one existing non-separator row "
            "with the same column count"
        )
    return True


def _table_regions(lines: list[str]) -> list[list[int]]:
    """fenced 또는 indented code 외부 각 table의 non-separator row index 목록."""
    fenced: set[int] = set()
    for start, end in _code_fence_regions(lines):
        fenced.update(range(start, end + 1))
    tables: list[list[int]] = []
    index = 0
    while index + 1 < len(lines):
        if index in fenced or index + 1 in fenced:
            index += 1
            continue
        header = _table_row_cells(lines[index])
        separator = _table_row_cells(lines[index + 1])
        if (
            header is None
            or separator is None
            or len(header) != len(separator)
            or not _is_table_separator_cells(separator)
        ):
            index += 1
            continue

        rows = [index]
        cursor = index + 2
        while cursor < len(lines) and cursor not in fenced:
            cells = _table_row_cells(lines[cursor])
            if cells is None or len(cells) != len(header):
                break
            if not _is_table_separator_cells(cells):
                rows.append(cursor)
            cursor += 1
        tables.append(rows)
        index = cursor
    return tables


def _source_table_row_change(
    segment: BlockChange, old_source_lines: list[str]
) -> TableRowChange | None:
    """구조 주소와 cardinality를 포함한 table row 변경."""

    if _single_table_row_lines(segment) is None or not segment.old_linenos:
        return None
    index = segment.old_linenos[0] - 1
    tables = _table_regions(old_source_lines)
    for table_ordinal, rows in enumerate(tables):
        if index in rows:
            return TableRowChange(
                table_ordinal=table_ordinal,
                row_ordinal=rows.index(index),
                row_count=len(rows),
                table_count=len(tables),
            )
    return None


def _table_row_index(
    lines: list[str],
    segment: BlockChange,
    *,
    translated: str | None = None,
) -> int | None:
    """구조 주소와 문맥이 유일하게 가리키는 table row 위치."""

    row_lines = _single_table_row_lines(segment)
    if row_lines is None:
        return None
    old_row, new_row = row_lines
    old_cells = _table_row_cells(old_row)
    new_cells = _table_row_cells(new_row)
    if old_cells is None or new_cells is None:
        return None
    tables = _table_regions(lines)

    reference = segment.table_row
    if reference is not None:
        return _referenced_table_row_index(
            lines,
            segment,
            tables,
            old_cells,
            new_cells,
            translated,
        )
    return _unreferenced_table_row_index(lines, segment, tables, old_cells)


def _referenced_table_row_index(
    lines: list[str],
    segment: BlockChange,
    tables: list[list[int]],
    old_cells: tuple[str, ...],
    new_cells: tuple[str, ...],
    translated: str | None,
) -> int | None:
    """계획에 기록된 표·행 ordinal로 locale 행 위치 검증.

    Args:
        lines: locale 문서 줄.
        segment: 적용할 표 행 변경.
        tables: locale 표별 데이터 행 위치.
        old_cells: 변경 이전 원문 셀.
        new_cells: 목표 원문 셀.
        translated: provider 번역 행 또는 ``None``.

    Returns:
        유일하게 검증된 locale 행 위치.
    """

    reference = segment.table_row
    if reference is None or (
        len(tables) != reference.table_count
        or reference.table_ordinal >= len(tables)
    ):
        return None
    rows = tables[reference.table_ordinal]
    if len(rows) != reference.row_count or reference.row_ordinal >= len(rows):
        return None
    index = rows[reference.row_ordinal]
    cells = _table_row_cells(lines[index])
    if cells is None or len(cells) != len(old_cells):
        return None
    if _translated_table_row_matches(cells, translated, table_count=len(tables)):
        return index
    candidates = _identified_table_row_candidates(
        lines,
        [row for table in tables for row in table],
        old_cells,
        new_cells,
    )
    return _validated_referenced_table_candidate(
        lines,
        segment,
        index,
        candidates,
        table_count=len(tables),
    )


def _translated_table_row_matches(
    cells: tuple[str, ...],
    translated: str | None,
    *,
    table_count: int,
) -> bool:
    """단일 locale 표 행이 이미 provider 번역 결과와 같은지 판정.

    Args:
        cells: 현재 locale 표 행 셀.
        translated: provider 번역 행 또는 ``None``.
        table_count: locale 문서의 표 개수.

    Returns:
        표가 하나이고 정규화된 번역 셀이 같은지 여부.
    """

    if translated is None or table_count != 1:
        return False
    translated_cells = _table_row_cells(translated.rstrip("\r\n"))
    return bool(
        translated_cells is not None
        and _table_match_cells(cells) == _table_match_cells(translated_cells)
    )


def _validated_referenced_table_candidate(
    lines: list[str],
    segment: BlockChange,
    index: int,
    candidates: list[int],
    *,
    table_count: int,
) -> int | None:
    """계획 ordinal 행과 원문 cell 후보·문맥의 일치 여부 검증.

    Args:
        lines: locale 문서 줄.
        segment: 적용할 표 행 변경.
        index: 계획 ordinal로 선택된 행 위치.
        candidates: 원문·목표 cell로 식별한 행 후보.
        table_count: locale 문서의 표 개수.

    Returns:
        검증된 행 위치 또는 ``None``.
    """

    if not candidates:
        if table_count != 1 or not _table_context_identifies_row(
            lines, segment, index, [index]
        ):
            return None
        return index
    if index not in candidates:
        return None
    if len(candidates) > 1 and not _table_context_identifies_row(
        lines, segment, index, candidates
    ):
        return None
    return index


def _unreferenced_table_row_index(
    lines: list[str],
    segment: BlockChange,
    tables: list[list[int]],
    old_cells: tuple[str, ...],
) -> int | None:
    """구버전 계획의 안정 셀과 문맥으로 locale 표 행 탐색.

    Args:
        lines: locale 문서 줄.
        segment: 적용할 표 행 변경.
        tables: locale 표별 데이터 행 위치.
        old_cells: 변경 이전 원문 셀.

    Returns:
        유일하게 식별된 locale 행 위치.
    """

    stable_cells = _table_match_cells(old_cells[1:])
    if not stable_cells:
        return None
    candidates = [
        index
        for rows in tables
        for index in rows
        if (cells := _table_row_cells(lines[index])) is not None
        and len(cells) == len(old_cells)
        and _table_match_cells(cells[1:]) == stable_cells
    ]
    narrowed = [
        index
        for index in candidates
        if _table_row_matches_context(lines, segment, index)
    ]
    return narrowed[0] if len(narrowed) == 1 else None


def _identified_table_row_candidates(
    lines: list[str],
    rows: list[int],
    old_cells: tuple[str, ...],
    new_cells: tuple[str, ...],
) -> list[int]:
    """원문·신규 cell 일치도와 구조 위치로 식별한 table row 후보."""

    normalized_old = _table_match_cells(old_cells)
    normalized_new = _table_match_cells(new_cells)
    scored: list[tuple[int, int]] = []
    for index in rows:
        cells = _table_row_cells(lines[index])
        if cells is None or len(cells) != len(old_cells):
            continue
        normalized = _table_match_cells(cells)
        score = max(
            sum(
                bool(expected) and actual == expected
                for actual, expected in zip(
                    normalized, source, strict=True
                )
            )
            for source in (normalized_old, normalized_new)
        )
        scored.append((score, index))

    if not scored:
        return []
    best_score = max(score for score, _index in scored)
    if best_score == 0:
        return []
    return [index for score, index in scored if score == best_score]


def _table_context_identifies_row(
    lines: list[str],
    segment: BlockChange,
    target: int,
    candidates: list[int],
) -> bool:
    """인접 row 문맥이 후보를 유일하게 식별하는지 여부."""

    blocks = _blocks("".join(lines))
    matching = set(candidates)
    validated = False
    for context, before in (
        (segment.before_context, True),
        (segment.after_context, False),
    ):
        if context is None or _table_row_cells(context) is not None:
            continue
        raw = _raw_context_indexes(lines, context)
        annotated = _matching_blocks(blocks, context)
        boundaries = raw + [
            block.end if before else block.start for block in annotated
        ]
        if not boundaries:
            continue
        validated = True
        if before:
            matching = {
                candidate
                for candidate in matching
                if any(boundary <= candidate for boundary in boundaries)
            }
        else:
            matching = {
                candidate
                for candidate in matching
                if any(candidate < boundary for boundary in boundaries)
            }
    return validated and matching == {target}


def _table_row_matches_context(
    lines: list[str], segment: BlockChange, index: int
) -> bool:
    """단일 candidate에 적용할 raw 문맥 검증."""
    validated = False
    if segment.before_context:
        before = [
            position
            for position in _raw_context_indexes(lines, segment.before_context)
            if position < index
        ]
        if not before:
            return False
        validated = True
    if segment.after_context:
        after = [
            position
            for position in _raw_context_indexes(lines, segment.after_context)
            if position > index
        ]
        if not after:
            return False
        validated = True
    return validated


def _table_row_context(text: str, segment: BlockChange) -> str | None:
    """변경 table row가 포함된 기존 locale table 문맥."""

    lines = text.splitlines(keepends=True)
    index = _table_row_index(lines, segment)
    return lines[index] if index is not None else None


def _replace_table_row(text: str, segment: BlockChange, translated: str) -> str | None:
    """table row 교체."""

    lines = text.splitlines(keepends=True)
    index = _table_row_index(lines, segment, translated=translated)
    if index is None:
        return None
    replacement = translated.rstrip("\n") + ("\n" if lines[index].endswith("\n") else "")
    return "".join(lines[:index]) + replacement + "".join(lines[index + 1 :])


def _coalesce_source_block_segments(segments: list[BlockChange]) -> list[BlockChange]:
    """같은 원문 소유 block을 가리키는 segment 병합."""

    result: list[BlockChange] = []
    indexes: dict[tuple[int, int], int] = {}

    for segment in segments:
        key = (
            (segment.new_block_start, segment.new_block_end)
            if segment.new_block_start is not None
            and segment.new_block_end is not None
            else None
        )
        if key is None or key not in indexes:
            if key is not None:
                indexes[key] = len(result)
            result.append(segment)
            continue

        index = indexes[key]
        current = result[index]
        result[index] = replace(
            current,
            old_lines=current.old_lines + segment.old_lines,
            new_lines=current.new_lines + segment.new_lines,
            after_context=segment.after_context or current.after_context,
            old_linenos=current.old_linenos + segment.old_linenos,
            new_linenos=current.new_linenos + segment.new_linenos,
        )

    return result


def _add_neighbor_anchors(
    change: BlockChange,
    *,
    old_source_blocks: list[SourceBlock],
    new_source_blocks: list[SourceBlock],
) -> BlockChange:
    """변경 segment에 이웃 anchor와 신규 anchor 출현 횟수 보강."""

    old_index = _source_block_index(
        old_source_blocks,
        start=change.old_block_start,
        linenos=change.old_linenos,
    )
    new_index = _source_block_index(
        new_source_blocks,
        start=change.new_block_start,
        linenos=change.new_linenos,
    )
    is_complete_insertion = (
        not change.old_source
        and not _meaningful_lines(change.old_lines)
        and (
            change.new_block_start is not None
            or change.before_old_lineno is not None
            or change.after_old_lineno is not None
        )
    )
    insertion_previous = (
        _context_source_block(old_source_blocks, change.before_old_lineno)
        if is_complete_insertion
        else None
    )
    insertion_next = (
        _context_source_block(old_source_blocks, change.after_old_lineno)
        if is_complete_insertion
        else None
    )
    return replace(
        change,
        old_previous_anchor=(
            change.old_previous_anchor
            or (insertion_previous.comment if insertion_previous is not None else None)
            or _range_edge_neighbor(
                old_source_blocks, old_index, len(change.old_anchors), before=True
            )
        ),
        old_previous_anchor_ordinal=(
            _block_ordinal(old_source_blocks, insertion_previous)
            if insertion_previous is not None
            else change.old_previous_anchor_ordinal
        ),
        old_next_anchor=(
            change.old_next_anchor
            or (insertion_next.comment if insertion_next is not None else None)
            or _range_edge_neighbor(
                old_source_blocks, old_index, len(change.old_anchors), before=False
            )
        ),
        old_next_anchor_ordinal=(
            _block_ordinal(old_source_blocks, insertion_next)
            if insertion_next is not None
            else change.old_next_anchor_ordinal
        ),
        new_previous_anchor=(
            change.new_previous_anchor
            or _range_edge_neighbor(
                new_source_blocks, new_index, len(change.new_anchors), before=True
            )
        ),
        new_next_anchor=(
            change.new_next_anchor
            or _range_edge_neighbor(
                new_source_blocks, new_index, len(change.new_anchors), before=False
            )
        ),
        new_anchor_occurrences=(
            sum(
                block.comment == change.new_anchor
                for block in new_source_blocks
            )
            if change.new_anchor
            else change.new_anchor_occurrences
        ),
    )


def _context_source_block(
    blocks: list[SourceBlock], lineno: int | None
) -> SourceBlock | None:
    """diff 문맥 줄이 속한 원문 block."""

    return _block_for_lineno(blocks, lineno) if lineno is not None else None


def _source_block_index(
    blocks: list[SourceBlock],
    *,
    start: int | None,
    linenos: tuple[int, ...],
) -> int | None:
    """원문 block 목록에서 지정한 block의 위치."""

    if start is not None:
        for index, block in enumerate(blocks):
            if block.start_lineno <= start <= block.end_lineno:
                return index
    for lineno in linenos:
        for index, block in enumerate(blocks):
            if block.start_lineno <= lineno <= block.end_lineno:
                return index
    return None


def _range_edge_neighbor(
    blocks: list[SourceBlock],
    index: int | None,
    anchor_count: int,
    *,
    before: bool,
) -> str | None:
    """block 범위 가장자리 바깥의 이웃 block."""

    if index is None:
        return None
    neighbor = index - 1 if before else index + max(1, anchor_count)
    if 0 <= neighbor < len(blocks):
        return blocks[neighbor].comment
    return None


def _split_named_sections(
    text: str,
    *,
    translated: bool,
) -> tuple[str, tuple[_NamedSection, ...]]:
    """named sections 분할."""

    lines = text.splitlines(keepends=True)
    starts = [
        index
        for index in _searchable_raw_indexes(lines)
        if is_named_anchor_line(lines[index])
    ]
    if not starts:
        return text, ()

    anchor_lines = tuple(lines[start].rstrip("\r\n") for start in starts)
    sections: list[_NamedSection] = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        section_lines = lines[start:end]
        separator_start = len(section_lines)
        while separator_start and not section_lines[separator_start - 1].strip():
            separator_start -= 1
        core = "".join(section_lines[:separator_start])
        separator = "".join(section_lines[separator_start:])
        anchor = anchor_lines[position]
        source_anchors = _named_section_source_anchors(
            core,
            translated=translated,
        )
        sections.append(
            _NamedSection(
                core=core,
                separator=separator,
                signature=NamedSectionSignature(
                    anchor=anchor,
                    source_anchors=source_anchors,
                ),
            )
        )
    return "".join(lines[: starts[0]]), tuple(sections)


def _named_section_source_anchors(
    core: str,
    *,
    translated: bool,
) -> tuple[str, ...]:
    """named section에 포함된 원문 annotation anchor 목록."""

    anchors = (
        _annotation_anchor_sequence(core)
        if translated
        else tuple(block.comment for block in _source_blocks(core))
    )
    normalized: list[str] = []
    for anchor in anchors:
        for tag in html_tags(anchor):
            anchor = anchor.replace(tag, " ")
        normalized.append(_normalize_text(anchor))
    return tuple(normalized)


def _named_section_reorder(
    old_source: str,
    new_source: str,
) -> NamedSectionReorder | None:
    """이전·현재 원문에서 계산한 named section 순서 변경."""

    old_prefix, old_sections = _split_named_sections(
        old_source,
        translated=False,
    )
    new_prefix, new_sections = _split_named_sections(
        new_source,
        translated=False,
    )
    if len(old_sections) < 2:
        return None

    old_cores = tuple(section.core for section in old_sections)
    new_cores = tuple(section.core for section in new_sections)
    if old_cores == new_cores or Counter(old_cores) != Counter(new_cores):
        return None

    old_order = tuple(section.signature for section in old_sections)
    new_order = tuple(section.signature for section in new_sections)
    if (
        Counter(old_order) != Counter(new_order)
        or len(set(old_order)) != len(old_order)
    ):
        return None
    reorder_prefix_links = old_prefix != new_prefix
    if reorder_prefix_links and not _prefix_reordered_with_sections(
        old_prefix, new_prefix, new_order
    ):
        return None
    return NamedSectionReorder(
        old_order=old_order,
        new_order=new_order,
        new_separators=tuple(section.separator for section in new_sections),
        reorder_prefix_links=reorder_prefix_links,
    )


def _section_link_positions(
    order: tuple[NamedSectionSignature, ...],
) -> dict[str, int] | None:
    """anchor 이름별 section 위치 또는 이름이 고유하지 않을 때 ``None``."""
    positions: dict[str, int] = {}
    for index, signature in enumerate(order):
        match = _NAMED_ANCHOR_NAME_RE.search(signature.anchor)
        if match is None or match.group(1) in positions:
            return None
        positions[match.group(1)] = index
    return positions


def _prefix_reordered_with_sections(
    old_prefix: str,
    new_prefix: str,
    new_order: tuple[NamedSectionSignature, ...],
) -> bool:
    """section TOC 링크 순열만 변경된 prefix 허용.

    링크가 아닌 모든 prefix 줄의 위치별 동일성 요구.
    알려진 section anchor를 대상으로 하는 link 줄의 순열 관계 및 신규 section 순서에 따른 link 순서 요구.
    """
    old_lines = old_prefix.splitlines(keepends=True)
    new_lines = new_prefix.splitlines(keepends=True)
    if len(old_lines) != len(new_lines):
        return False
    positions = _section_link_positions(new_order)
    if positions is None:
        return False
    old_links: list[str] = []
    new_links: list[str] = []
    for old_line, new_line in zip(old_lines, new_lines):
        pair_valid, is_link = _prefix_line_pair_is_valid(old_line, new_line)
        if not pair_valid:
            return False
        if is_link:
            old_links.append(old_line)
            new_links.append(new_line)
    if not old_links or Counter(old_links) != Counter(new_links):
        return False
    link_positions = _section_link_order(new_links, positions)
    if link_positions is None:
        return False
    return link_positions == sorted(link_positions)


def _prefix_line_pair_is_valid(old_line: str, new_line: str) -> tuple[bool, bool]:
    """section prefix의 대응 줄이 동일 본문 또는 TOC 링크인지 판정.

    Args:
        old_line: 변경 이전 prefix 줄.
        new_line: 변경 이후 prefix 줄.

    Returns:
        줄 쌍 유효 여부와 TOC 링크 여부.
    """

    old_anchor = _toc_link_anchor(old_line)
    new_anchor = _toc_link_anchor(new_line)
    if old_anchor is None and new_anchor is None:
        return old_line == new_line, False
    return old_anchor is not None and new_anchor is not None, True


def _section_link_order(
    lines: list[str],
    positions: dict[str, int],
) -> list[int] | None:
    """TOC 링크 줄을 목표 section 순번으로 변환.

    Args:
        lines: 변경 이후 TOC 링크 줄.
        positions: anchor 이름별 목표 section 순번.

    Returns:
        목표 section 순번 목록. 알 수 없는 anchor면 ``None``.
    """

    order: list[int] = []
    for line in lines:
        anchor = _toc_link_anchor(line)
        if anchor is None or anchor not in positions:
            return None
        order.append(positions[anchor])
    return order


def _toc_link_anchor(line: str) -> str | None:
    """목차 링크 줄이 가리키는 fragment anchor."""

    match = _TOC_LINK_RE.match(line.rstrip("\r\n"))
    return match.group(1) if match is not None else None


def _apply_named_section_reorder(
    text: str,
    reorder: NamedSectionReorder,
) -> str:
    """named section reorder 적용."""

    prefix, sections = _split_named_sections(text, translated=True)
    current_order = tuple(section.signature for section in sections)
    if current_order != reorder.old_order:
        raise PatchError("named section order does not match the source plan state")
    if reorder.reorder_prefix_links:
        prefix = _reorder_prefix_section_links(prefix, reorder.new_order)
    by_signature = {section.signature: section for section in sections}
    return prefix + "".join(
        by_signature[signature].core + separator
        for signature, separator in zip(
            reorder.new_order,
            reorder.new_separators,
            strict=True,
        )
    )


def _reorder_prefix_section_links(
    prefix: str, new_order: tuple[NamedSectionSignature, ...]
) -> str:
    """named section 순서에 맞춘 선행 목차 링크 재배열."""

    lines = prefix.splitlines(keepends=True)
    link_indexes = [
        index for index, line in enumerate(lines) if _toc_link_anchor(line) is not None
    ]
    if not link_indexes:
        return prefix
    positions = _section_link_positions(new_order)
    if positions is None:
        raise PatchError("named section anchors are not unique for TOC reordering")
    keys: list[tuple[int, int]] = []
    for order, index in enumerate(link_indexes):
        anchor = _toc_link_anchor(lines[index])
        if anchor is None or anchor not in positions:
            raise PatchError(
                "translated table of contents does not match the reordered sections"
            )
        keys.append((positions[anchor], order))
    ordered = [lines[link_indexes[original]] for _position, original in sorted(keys)]
    for slot, line in zip(link_indexes, ordered):
        lines[slot] = line
    return "".join(lines)


def _source_blocks(source: str) -> list[SourceBlock]:
    """Markdown 원문을 완전한 소유 block 목록으로 분할."""

    blocks: list[SourceBlock] = []
    paragraph: list[tuple[int, str]] = []
    in_code = False
    fence = ""
    in_front_matter = False
    source_comment_lines = standalone_html_comment_line_numbers(source)
    reference_lines = {
        line + 1 for line in reference_definition_line_numbers(source)
    }
    table_lines = {
        lineno
        for block in split_blocks(source.splitlines())
        if block.kind == "text" and is_gfm_pipe_table("\n".join(block.lines))
        for lineno in range(block.start + 1, block.end + 1)
    }

    def flush_paragraph() -> None:
        """누적된 문단 줄을 하나의 원문 block으로 확정."""

        if not paragraph:
            return
        paragraph_text = "\n".join(line for _lineno, line in paragraph)
        if not is_structural_html_fragment(paragraph_text):
            comment = _normalize_text(
                " ".join(line.strip() for _lineno, line in paragraph)
            )
            text = paragraph_text + "\n"
            blocks.append(
                SourceBlock(paragraph[0][0], paragraph[-1][0], comment, text)
            )
        paragraph.clear()

    for lineno, line in enumerate(source.splitlines(), start=1):
        stripped = line.strip()
        token = fence_token(line)
        if token:
            flush_paragraph()
            if not in_code:
                in_code, fence = True, token
            elif closes_fence(line, fence):
                in_code = False
            continue
        if in_code:
            continue
        if lineno in source_comment_lines:
            flush_paragraph()
            continue
        if lineno in reference_lines:
            flush_paragraph()
            continue
        if stripped == "---" and lineno == 1:
            flush_paragraph()
            in_front_matter = True
            continue
        if stripped == "---" and in_front_matter:
            in_front_matter = False
            continue
        if in_front_matter:
            continue
        if not stripped:
            flush_paragraph()
            continue
        if is_heading_line(line):
            flush_paragraph()
            heading = strip_title_attr_line(line).strip()
            blocks.append(SourceBlock(lineno, lineno, _normalize_text(heading), line + "\n"))
            continue
        if is_structural_html_line(line):
            flush_paragraph()
            continue
        if lineno in table_lines:
            flush_paragraph()
            continue
        if is_non_annotatable_line(line):
            flush_paragraph()
            continue
        paragraph.append((lineno, line))

    flush_paragraph()
    return blocks


def _plan_source_blocks(blocks: list[SourceBlock]) -> list[SourceBlock]:
    """계획 주소에 사용할 구조 단위 원문 block 목록."""

    return [
        block
        for block in blocks
        if not _is_inline_code_identifier_list(block.text)
    ]


def _is_inline_code_identifier_list(text: str) -> bool:
    """code identifier list 여부."""

    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return False
    for line in lines:
        list_item = _LIST_ITEM_PREFIX_RE.match(line)
        if list_item is None:
            return False
        body = line[list_item.end() :]
        if not (inline_code_contents(body) or html_code_contents(body)):
            return False
        if strip_html_code_elements(strip_inline_code(body)).strip(
            " `*_~.,:;()[]&/,+"
        ):
            return False
    return True


def _inline_code_list_is_applied(text: str, segment: BlockChange) -> bool:
    """inline code 식별자 목록 변경이 이미 적용되었는지 여부."""

    source = segment.new_source
    if source is None:
        return False
    expected = source.rstrip("\n").splitlines()
    if not expected:
        return False

    lines = text.splitlines(keepends=True)
    searchable = set(_searchable_raw_indexes(lines))
    matches = [
        start
        for start in searchable
        if start + len(expected) <= len(lines)
        and all(
            start + offset in searchable
            and lines[start + offset].rstrip("\r\n") == line
            for offset, line in enumerate(expected)
        )
    ]
    if len(matches) != 1:
        return False

    if segment.new_anchor:
        for block in _matching_blocks(_blocks(text), segment.new_anchor):
            comment_end, _body = _read_comment(lines, block.start)
            if not any(line.strip() for line in lines[comment_end : block.end]):
                return False
    return True
