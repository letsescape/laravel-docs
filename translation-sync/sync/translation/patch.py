"""Apply translated source diff hunks to annotated locale Markdown.

The translation workflow uses English HTML comments as stable anchors. A
changed English hunk is translated separately, then merged into the existing
locale document by replacing, inserting, or deleting the matching annotated
block.
"""
from __future__ import annotations

import re
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass, replace
from enum import Enum

from ..common.markdown import (
    closes_fence,
    fence_token,
    html_tags,
    html_comment_spans,
    inline_code_contents,
    is_heading_line,
    is_named_anchor_line,
    is_non_annotatable_line,
    is_structural_html_fragment,
    is_structural_html_line,
    normalize_annotation_anchor,
    reference_definition_line_numbers,
    standalone_html_comment_line_numbers,
    strip_inline_code,
    strip_title_attr_line,
)
from ..source.diff import DiffHunk, hunks_between

_ADMONITION_MARKER_RE = re.compile(
    r"^>\s*\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT)]\s*$", re.IGNORECASE
)
_BARE_INTERNAL_LINK_RE = re.compile(r"^\[[^]\n]+]\(#[^)\s]+\)$")
_LIST_ITEM_PREFIX_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
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
    """Raised when a diff hunk cannot be applied to the existing translation."""


class PlanState(Enum):
    UNGUARDED = "unguarded"
    SOURCE = "source"
    TARGET = "target"


@dataclass(frozen=True)
class BlockChange:
    """A source delta paired with the complete Markdown blocks it changes.

    ``old_lines`` / ``new_lines`` are the effective delta after optional source
    normalization. The complete blocks used for translation and locale
    replacement live in ``old_source`` / ``new_source``. Keeping those concepts
    separate prevents block expansion from turning one added line into an
    all-added diff.
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
    # An interior change to one fenced code block (see CodeChange). Code is never
    # translated, so it is handled by a verbatim block swap, not the LLM path.
    code_block: CodeChange | None = None
    inserted_code_block_index: int | None = None
    inserted_code_block: str | None = None
    deleted_code_block_index: int | None = None
    deleted_code_block: str | None = None
    # A single changed table row addressed by structural position (see
    # TableRowChange). Locale rows may be fully translated, so tail-cell
    # matching alone cannot locate them.
    table_row: TableRowChange | None = None

    @property
    def needs_translation(self) -> bool:
        if self.code_block is not None:
            return False
        return bool(_meaningful_lines(self.new_lines)) or bool(
            self.new_source and self.new_source.strip()
        )

    @property
    def provider_free(self) -> bool:
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
        return bool(lines) and all(_BARE_INTERNAL_LINK_RE.fullmatch(line) for line in lines)

    @property
    def is_inline_code_identifier_list(self) -> bool:
        return bool(self.new_source) and _is_inline_code_identifier_list(
            self.new_source
        )

    @property
    def is_named_anchor_change(self) -> bool:
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
        if self.code_block is not None:
            return False
        has_old_source = bool(self.old_source or _meaningful_lines(self.old_lines))
        return has_old_source and not self.needs_translation

    @property
    def is_block_range(self) -> bool:
        return len(self.old_anchors) > 1 or len(self.new_anchors) > 1


@dataclass(frozen=True)
class CodeChange:
    """An interior change to one fenced code block.

    Code is copied verbatim from the source and never translated, so a changed
    block is located by its old and new indexes in document order and the whole
    block is swapped for the new source block. This keeps the locale code
    byte-identical to English (which verification requires, even for things like
    reordered imports) and stays idempotent: a re-run finds the block already
    equal to ``new_block`` and does nothing.

    ``anchors`` are the block's unchanged lines (everything except the freshly
    added lines). The swap only happens when the located block still contains
    all of them. Reordered-but-equivalent code is still recognised and
    canonicalised, while any other divergence fails closed in
    ``_code_plan_state`` so a drifted document is never silently rewritten.
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
    """A single changed table row addressed by structural position.

    ``table_ordinal`` indexes the table among all tables outside code fences,
    ``table_count`` and ``row_count`` pin the source cardinalities, and
    ``row_ordinal`` indexes the changed row among the table's non-separator
    rows. Locale-only tables or rows therefore fail closed instead of shifting
    the structural address onto unrelated content.
    """

    table_ordinal: int
    row_ordinal: int
    row_count: int
    table_count: int


@dataclass(frozen=True)
class NamedSectionSignature:
    anchor: str
    source_anchors: tuple[str, ...]


@dataclass(frozen=True)
class NamedSectionReorder:
    old_order: tuple[NamedSectionSignature, ...]
    new_order: tuple[NamedSectionSignature, ...]
    new_separators: tuple[str, ...]
    reorder_prefix_links: bool = False


@dataclass(frozen=True)
class PatchPlan:
    """Ordered block changes derived from one old/new source pair."""

    changes: tuple[BlockChange, ...]
    old_source_anchors: tuple[str, ...] | None = None
    new_source_anchors: tuple[str, ...] | None = None
    old_code_blocks: tuple[str, ...] | None = None
    new_code_blocks: tuple[str, ...] | None = None
    old_source_comments: tuple[SourceComment, ...] = ()
    new_source_comments: tuple[SourceComment, ...] = ()
    named_section_reorder: NamedSectionReorder | None = None


@dataclass(frozen=True)
class AnnotatedBlock:
    start: int
    end: int
    comment: str
    text: str


@dataclass(frozen=True)
class SourceBlock:
    start_lineno: int
    end_lineno: int
    comment: str
    text: str


@dataclass(frozen=True)
class SourceComment:
    """A source-authored HTML comment and its position between source blocks."""

    body: str
    anchor_position: int


@dataclass(frozen=True)
class _NamedSection:
    core: str
    separator: str
    signature: NamedSectionSignature


def build_plan(
    hunks: tuple[DiffHunk, ...],
    source_text: str,
    *,
    normalize_source: Callable[[str], str] | None = None,
) -> PatchPlan:
    """Pair effective line deltas with their complete old/new source blocks."""

    source_lines = source_text.splitlines()
    old_source_lines = _reverse_apply_hunks(source_lines, hunks)
    old_source_text = _lines_text(old_source_lines, source_text)
    if _front_matter_text(old_source_text) != _front_matter_text(source_text):
        raise PatchError("front matter changes require a full document sync")
    if normalize_source is not None:
        normalized_old = normalize_source(old_source_text)
        normalized_new = normalize_source(source_text)
        return build_plan(
            hunks_between(normalized_old, normalized_new),
            normalized_new,
        )

    named_section_reorder = _named_section_reorder(
        old_source_text,
        source_text,
    )
    if named_section_reorder is not None:
        old_source_blocks = _source_blocks(old_source_text)
        new_source_blocks = _source_blocks(source_text)
        old_regions = _code_fence_regions(old_source_lines)
        new_regions = _code_fence_regions(source_lines)
        return PatchPlan(
            changes=(),
            old_source_anchors=tuple(
                block.comment for block in _plan_source_blocks(old_source_blocks)
            ),
            new_source_anchors=tuple(
                block.comment for block in _plan_source_blocks(new_source_blocks)
            ),
            old_code_blocks=_code_blocks_from_regions(
                old_source_lines,
                old_regions,
            ),
            new_code_blocks=_code_blocks_from_regions(
                source_lines,
                new_regions,
            ),
            old_source_comments=_source_comment_locations(old_source_text),
            new_source_comments=_source_comment_locations(source_text),
            named_section_reorder=named_section_reorder,
        )

    old_comment_lines = _source_comment_line_numbers(old_source_text)
    new_comment_lines = _source_comment_line_numbers(source_text)
    if any(
        (line.kind == "delete" and line.old_lineno in old_comment_lines)
        or (line.kind == "add" and line.new_lineno in new_comment_lines)
        for hunk in hunks
        for line in hunk.lines
    ):
        raise PatchError("source HTML comment changes require a full document sync")

    segments: list[BlockChange] = []

    for hunk in hunks:
        if _hunk_has_code_fence_change(hunk):
            segments.append(_hunk_region_segment(hunk, source_lines))
            continue

        before_context: DiffLine | None = None
        old_lines: list[str] = []
        new_lines: list[str] = []
        old_linenos: list[int] = []
        new_linenos: list[int] = []

        def flush(after_context: DiffLine | None = None) -> None:
            nonlocal before_context, old_lines, new_lines, old_linenos, new_linenos
            if old_lines or new_lines:
                segments.append(
                    BlockChange(
                        old_lines=tuple(old_lines),
                        new_lines=tuple(new_lines),
                        before_context=_context_text(before_context),
                        after_context=_context_text(after_context),
                        old_linenos=tuple(old_linenos),
                        new_linenos=tuple(new_linenos),
                        before_old_lineno=(
                            before_context.old_lineno if before_context else None
                        ),
                        before_new_lineno=(
                            before_context.new_lineno if before_context else None
                        ),
                        after_old_lineno=(
                            after_context.old_lineno if after_context else None
                        ),
                        after_new_lineno=(
                            after_context.new_lineno if after_context else None
                        ),
                    )
                )
                old_lines = []
                new_lines = []
                old_linenos = []
                new_linenos = []
            if after_context is not None:
                before_context = after_context

        for line in hunk.lines:
            if line.kind == "context":
                context = _normalize_text(line.text)
                if old_lines or new_lines:
                    if context:
                        flush(line)
                elif context:
                    before_context = line
                continue
            if line.kind == "delete":
                old_lines.append(line.text)
                if line.old_lineno is not None:
                    old_linenos.append(line.old_lineno)
            elif line.kind == "add":
                new_lines.append(line.text)
                if line.new_lineno is not None:
                    new_linenos.append(line.new_lineno)

        flush(None)

    new_regions = _code_fence_regions(source_lines)
    old_regions = _code_fence_regions(old_source_lines)
    filtered = [
        segment
        for segment in segments
        if segment.old_lines or segment.new_lines
    ]
    new_source_blocks = _source_blocks(source_text)
    old_source_blocks = _source_blocks(old_source_text)
    new_signature_text = (
        normalize_source(source_text) if normalize_source else source_text
    )
    old_signature_text = (
        normalize_source(old_source_text) if normalize_source else old_source_text
    )
    new_signature_blocks = _source_blocks(new_signature_text)
    old_signature_blocks = _source_blocks(old_signature_text)

    expanded: list[BlockChange] = []
    emitted_regions: set[int] = set()
    for segment in filtered:
        region, old_region = _code_region_indexes(
            segment, new_regions, old_regions
        )
        if region is not None and region < len(new_regions):
            if region in emitted_regions:
                continue
            emitted_regions.add(region)
            group = [
                other
                for other in filtered
                if _code_region_indexes(other, new_regions, old_regions)[0] == region
            ]
            old_region_candidates = {
                candidate
                for other in group
                for candidate in [
                    _code_region_indexes(other, new_regions, old_regions)[1]
                ]
                if candidate is not None
            }
            if len(old_region_candidates) == 1:
                old_region = old_region_candidates.pop()
            expanded.append(
                _code_block_segment(
                    group,
                    source_lines,
                    new_regions[region],
                    region,
                    old_source_lines=old_source_lines,
                    old_regions=old_regions,
                    old_block_index=old_region,
                )
            )
            continue
        expanded.extend(
            _expand_to_source_blocks(
                segment,
                new_source_blocks=new_source_blocks,
                old_source_blocks=old_source_blocks,
                new_source_lines=source_lines,
                old_source_lines=old_source_lines,
            )
        )
    coalesced = _coalesce_source_block_segments(expanded)
    return PatchPlan(
        changes=tuple(
            _add_neighbor_anchors(
                _attach_deleted_code_block(
                    change,
                    old_source_lines=old_source_lines,
                    old_regions=old_regions,
                    new_source_lines=source_lines,
                    new_regions=new_regions,
                ),
                old_source_blocks=old_source_blocks,
                new_source_blocks=new_source_blocks,
            )
            for change in coalesced
        ),
        old_source_anchors=tuple(
            block.comment for block in _plan_source_blocks(old_signature_blocks)
        ),
        new_source_anchors=tuple(
            block.comment for block in _plan_source_blocks(new_signature_blocks)
        ),
        old_code_blocks=_code_blocks_from_regions(old_source_lines, old_regions),
        new_code_blocks=_code_blocks_from_regions(source_lines, new_regions),
        old_source_comments=_source_comment_locations(old_source_text),
        new_source_comments=_source_comment_locations(source_text),
    )


def _context_text(line: DiffLine | None) -> str | None:
    return _normalize_text(line.text) if line is not None else None


def _lines_text(lines: list[str], template: str) -> str:
    text = "\n".join(lines)
    return text + "\n" if template.endswith("\n") else text


def _front_matter_text(text: str) -> str | None:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[: index + 1])
    return "".join(lines)


def _source_comment_line_numbers(text: str) -> set[int]:
    return set(standalone_html_comment_line_numbers(text))


def diff_text(segment: BlockChange) -> str:
    lines: list[str] = []
    for old_line in segment.old_lines:
        lines.append(f"- {old_line}")
    for new_line in segment.new_lines:
        lines.append(f"+ {new_line}")
    return "\n".join(lines)


def source_text(segment: BlockChange) -> str:
    if segment.inserted_code_block is not None:
        return segment.inserted_code_block.rstrip("\n") + "\n"
    if segment.new_source is not None:
        return segment.new_source.rstrip() + "\n"
    return "\n".join(_meaningful_lines(segment.new_lines)).rstrip() + "\n"


def existing_context(text: str, segment: BlockChange) -> str:
    if segment.is_admonition_marker_change:
        return _existing_admonition_context(text, segment)
    blocks = _blocks(text)
    old_anchor = segment.old_source or _joined(segment.old_lines)
    if old_anchor:
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
    applied = _find_applied_new_blocks(blocks, segment)
    if applied:
        return "".join(block.text for block in applied).strip()
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
    return "(none)"


def _existing_admonition_context(text: str, segment: BlockChange) -> str:
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
            # A fresh line diff may realign duplicates as an insertion followed
            # by a deletion. Apply every planned insertion from the source state.
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
    existing: str, plan: PatchPlan, translated_blocks: list[str]
) -> str:
    if (
        plan.named_section_reorder is None
        and tuple(comment.body for comment in plan.old_source_comments)
        != tuple(comment.body for comment in plan.new_source_comments)
    ):
        raise PatchError("source HTML comment changes require a full document sync")
    expected = sum(change.needs_translation for change in plan.changes)
    if len(translated_blocks) != expected:
        raise PatchError(
            f"translation count mismatch: expected {expected}, got {len(translated_blocks)}"
        )
    state = plan_state(existing, plan)
    code_state = _code_plan_state(existing, plan)
    source_state = state is PlanState.SOURCE
    target_state = state is PlanState.TARGET
    source_anchors = (
        plan.new_source_anchors
        if target_state
        else plan.old_source_anchors
    )
    source_comments = (
        plan.new_source_comments
        if target_state
        else plan.old_source_comments
    )
    masked_existing, source_comment_replacements = _mask_source_comment_anchors(
        existing, source_anchors or (), source_comments
    )
    if plan.named_section_reorder is not None and source_state:
        result = _apply_named_section_reorder(
            masked_existing,
            plan.named_section_reorder,
        )
    else:
        result = apply_segments(
            masked_existing,
            list(plan.changes),
            translated_blocks,
            source_state=source_state,
            target_state=target_state,
            code_state=code_state,
        )
    result = _ensure_single_eof_newline(result)
    if (
        plan.named_section_reorder is not None
        and tuple(
            section.signature
            for section in _split_named_sections(result, translated=True)[1]
        )
        != plan.named_section_reorder.new_order
    ):
        raise PatchError("patched named section order does not match the target source")
    if (
        plan.named_section_reorder is None
        and plan.new_source_anchors is not None
    ):
        result_anchors = _annotation_anchor_sequence(result)
        if result_anchors != plan.new_source_anchors:
            raise PatchError("patched block order does not match the target source")
    restored = _restore_source_comment_anchors(
        result, source_comment_replacements
    )
    if (
        plan.named_section_reorder is None
        and plan.new_source_anchors is not None
        and _locate_source_comment_blocks(
            restored, plan.new_source_anchors, plan.new_source_comments
        )
        is None
    ):
        raise PatchError("patched source HTML comment order does not match the target source")
    return restored


def plan_state(existing: str, plan: PatchPlan) -> PlanState:
    if plan.named_section_reorder is not None:
        if _matches_named_section_state(
            existing,
            plan.old_source_anchors or (),
            plan.old_source_comments,
            plan.named_section_reorder.old_order,
        ):
            return PlanState.SOURCE
        if _matches_named_section_state(
            existing,
            plan.new_source_anchors or (),
            plan.new_source_comments,
            plan.named_section_reorder.new_order,
        ):
            return PlanState.TARGET
        raise PatchError(
            "existing named section order matches neither source nor target plan state"
        )

    has_anchor_transition = (
        plan.old_source_anchors is not None
        and plan.new_source_anchors is not None
        and plan.old_source_anchors != plan.new_source_anchors
        and any(change.old_anchors or change.new_anchors for change in plan.changes)
    )
    if not has_anchor_transition:
        return PlanState.UNGUARDED
    if _locate_source_comment_blocks(
        existing, plan.old_source_anchors, plan.old_source_comments
    ) is not None:
        return PlanState.SOURCE
    if _locate_source_comment_blocks(
        existing, plan.new_source_anchors, plan.new_source_comments
    ) is not None:
        return PlanState.TARGET
    raise PatchError(
        "existing block order matches neither source nor target plan state"
    )


def _matches_named_section_state(
    existing: str,
    anchors: tuple[str, ...],
    comments: tuple[SourceComment, ...],
    expected_order: tuple[NamedSectionSignature, ...],
) -> bool:
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
    """True when each block pairs with the expected one modulo line order."""
    if len(current) != len(expected) or current == expected:
        return False
    return all(
        Counter(have.split("\n")) == Counter(want.split("\n"))
        for have, want in zip(current, expected)
    )


def _strip_retained_admonition_marker(
    segment: BlockChange, translated: str
) -> str:
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
    return tuple(block.comment for block in _blocks(text) if _is_plan_anchor(block))


def _source_comment_locations(text: str) -> tuple[SourceComment, ...]:
    lines = text.splitlines(keepends=True)
    source_blocks = _plan_source_blocks(_source_blocks(text))
    comments: list[SourceComment] = []
    for start in _comment_starts(lines):
        body = _normalize_text(_read_comment(lines, start)[1])
        lineno = start + 1
        comments.append(
            SourceComment(
                body=body,
                anchor_position=sum(
                    block.start_lineno < lineno for block in source_blocks
                ),
            )
        )
    return tuple(comments)


def _mask_source_comment_anchors(
    text: str,
    anchors: tuple[str, ...],
    comments: tuple[SourceComment, ...],
) -> tuple[str, tuple[tuple[str, str], ...]]:
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
    for marker, original in replacements:
        if text.count(marker) != 1:
            raise PatchError("source HTML comment was lost or duplicated while patching")
        text = text.replace(marker, original, 1)
    return text


def _locate_source_comment_blocks(
    text: str,
    anchors: tuple[str, ...],
    comments: tuple[SourceComment, ...],
) -> tuple[AnnotatedBlock, ...] | None:
    """Resolve source comments without confusing them with translation anchors."""

    blocks = _blocks(text)
    plan_blocks = [block for block in blocks if _is_plan_anchor(block)]
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

    if tuple(block.comment for block in plan_blocks) != tuple(
        body for body, _index in expected
    ):
        return None

    located: list[AnnotatedBlock | None] = [None] * len(comments)
    for block, (_body, comment_index) in zip(plan_blocks, expected, strict=True):
        if comment_index is not None:
            located[comment_index] = block

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
            return None
        for index, block in zip(indexes, candidates, strict=True):
            located[index] = block

    if any(block is None for block in located):
        return None
    return tuple(block for block in located if block is not None)


def _is_plan_anchor_comment(comment: str) -> bool:
    return (
        not is_non_annotatable_line(comment)
        and not is_structural_html_fragment(comment)
        and not _is_inline_code_identifier_list_comment(comment)
    )


def _is_plan_anchor(block: AnnotatedBlock) -> bool:
    return _is_plan_anchor_comment(block.comment)


def _is_inline_code_identifier_list_comment(comment: str) -> bool:
    if not inline_code_contents(comment):
        return False
    remainder = strip_inline_code(comment)
    remainder = re.sub(r"(?:[-*+]|\d+[.)])", " ", remainder)
    return not remainder.strip(" `*_~.,:;()[]&/,+")


def _translated_block_end(lines: list[str], start: int, limit: int) -> int:
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
    """Locate a contiguous annotated range inside unchanged neighbors."""

    if not anchors:
        return None
    matches_by_anchor = [set(_matching_blocks(blocks, anchor)) for anchor in anchors]
    candidates = [
        tuple(blocks[start : start + len(anchors)])
        for start in range(len(blocks) - len(anchors) + 1)
        if all(
            blocks[start + offset] in matches
            for offset, matches in enumerate(matches_by_anchor)
        )
    ]

    if previous_anchor:
        previous = _matching_blocks(blocks, previous_anchor)
        if previous:
            previous_set = set(previous)
            candidates = [
                candidate
                for candidate in candidates
                if _neighboring_plan_anchor(
                    blocks, blocks.index(candidate[0]), -1
                ) in previous_set
            ]
    if next_anchor:
        following = _matching_blocks(blocks, next_anchor)
        if following:
            following_set = set(following)
            candidates = [
                candidate
                for candidate in candidates
                if _neighboring_plan_anchor(
                    blocks, blocks.index(candidate[-1]), 1
                ) in following_set
            ]

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


def _neighboring_plan_anchor(
    blocks: list[AnnotatedBlock], index: int, direction: int
) -> AnnotatedBlock | None:
    index += direction
    while 0 <= index < len(blocks):
        if _is_plan_anchor(blocks[index]):
            return blocks[index]
        index += direction
    return None


def _matching_blocks(blocks: list[AnnotatedBlock], comment: str) -> list[AnnotatedBlock]:
    normalized = _normalize_text(comment)
    exact = [block for block in blocks if block.comment == normalized]
    if exact:
        return exact
    if not _can_match_partial_comment(normalized):
        return []
    candidates = [block for block in blocks if normalized in block.comment]
    return candidates if len(candidates) == 1 else []


def _can_match_partial_comment(normalized: str) -> bool:
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
    lines = text.splitlines(keepends=True)
    replacement = _format_replacement(
        translated, trailing=_trailing_separator(found[-1].text)
    )
    return "".join(lines[: found[0].start]) + replacement + "".join(
        lines[found[-1].end :]
    )


def _replace_segment(text: str, segment: BlockChange, translated: str) -> str:
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
    lines = text.splitlines(keepends=True)
    return "".join(lines[: found[0].start]) + "".join(lines[found[-1].end :])


def _insert_fenced_code_block(
    text: str, segment: BlockChange, translated: str
) -> str:
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
    stripped = line.strip()
    if not stripped:
        return False
    if is_named_anchor_line(line) or is_structural_html_line(line):
        return False
    return not is_non_annotatable_line(line)


def _require_target_block_bodies(text: str, segment: BlockChange) -> None:
    """Fail closed when a target-state block exists as a comment without body."""
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
        # The source appends at end of document; mirror that boundary even
        # when the before context is translated or structural.
        return text.rstrip("\n") + "\n\n" + _format_replacement(translated, trailing="\n")
    raise PatchError("missing insertion context")


def _context_anchor_block(
    blocks: list[AnnotatedBlock],
    context: str,
    neighbor_anchor: str | None,
    neighbor_ordinal: int | None,
) -> AnnotatedBlock | None:
    """Resolve a context line to its annotated block, occurrence-aware.

    A duplicated context resolves through the source-side ordinal when the
    context is the neighbor block itself; otherwise it must be unique.
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
    """Extend an existing code block whose source region grew around it.

    Diff alignment can expand an insertion so it starts at an existing fenced
    block (the close fence realigns to the trailing context). That block is
    located verbatim and the whole grown region replaces it in place.
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
    """Place an insertion between the code regions that bound it in the source."""
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
    return [
        index
        for index in _searchable_raw_indexes(lines)
        if lines[index].rstrip("\r\n") == expected
    ]


def _apply_named_anchor_change(
    text: str, segment: BlockChange, translated: str | None
) -> str:
    old_lines = _meaningful_lines(segment.old_lines)
    new_lines = _meaningful_lines(segment.new_lines)
    old_anchor = old_lines[0] if old_lines else None
    new_anchor = new_lines[0] if new_lines else None
    lines = text.splitlines(keepends=True)

    if new_anchor is not None:
        if translated is None or translated.strip() != new_anchor:
            raise PatchError("provider-free named anchor change has diverged")
        target_count = segment.new_anchor_occurrences
        matches_new = _raw_line_indexes(lines, new_anchor)
        if target_count is not None and len(matches_new) >= target_count:
            placement = _anchor_occurrence_at_context(
                lines, _blocks(text), matches_new, segment
            )
            if placement is False:
                raise PatchError(
                    "existing named anchor placement does not match the target: "
                    + new_anchor
                )
            return text

    if old_anchor is not None:
        matches = _raw_line_indexes(lines, old_anchor)
        if (
            new_anchor is None
            and segment.new_anchor_occurrences is not None
            and len(matches) <= segment.new_anchor_occurrences
        ):
            placement = _anchor_occurrence_at_context(
                lines, _blocks(text), matches, segment
            )
            if placement is True:
                raise PatchError(
                    "deleted named anchor still occupies its source position: "
                    + old_anchor
                )
            return text
        occurrence = segment.old_block_ordinal or 0
        if occurrence >= len(matches):
            raise PatchError(f"missing existing named anchor: {old_anchor}")
        index = matches[occurrence]
        if new_anchor is None:
            return "".join(lines[:index] + lines[index + 1 :])
        ending = "\n" if lines[index].endswith("\n") else ""
        replacement = translated.rstrip("\r\n") + ending
        return "".join(lines[:index]) + replacement + "".join(lines[index + 1 :])

    assert new_anchor is not None
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


def _anchor_occurrence_at_context(
    lines: list[str],
    blocks: list[AnnotatedBlock],
    anchor_indexes: list[int],
    segment: BlockChange,
) -> bool | None:
    """Whether any anchor occurrence sits at the segment's context boundary.

    Returns ``None`` when neither context resolves in the document, in which
    case only occurrence counts can be validated.
    """
    checked = False
    if segment.after_context:
        following_blocks = _matching_blocks(blocks, segment.after_context)
        raw_following = _raw_context_indexes(lines, segment.after_context)
        if following_blocks or raw_following:
            checked = True
            boundaries = [block.start for block in following_blocks] + raw_following
            for index in anchor_indexes:
                if any(
                    index < boundary
                    and _only_anchor_or_blank_between(lines, index + 1, boundary)
                    for boundary in boundaries
                ):
                    return True
    if segment.before_context:
        previous_blocks = _matching_blocks(blocks, segment.before_context)
        raw_previous = _raw_context_indexes(lines, segment.before_context)
        if previous_blocks or raw_previous:
            checked = True
            boundaries = [block.end for block in previous_blocks] + [
                position + 1 for position in raw_previous
            ]
            for index in anchor_indexes:
                if any(
                    boundary <= index
                    and _only_anchor_or_blank_between(lines, boundary, index)
                    for boundary in boundaries
                ):
                    return True
    if not checked:
        return None
    return False


def _only_anchor_or_blank_between(lines: list[str], start: int, end: int) -> bool:
    return all(
        not line.strip() or is_named_anchor_line(line) for line in lines[start:end]
    )


def _apply_admonition_marker_change(
    text: str, segment: BlockChange, translated: str | None
) -> str:
    old_marker = _meaningful_lines(segment.old_lines)[0].strip()
    new_marker = _meaningful_lines(segment.new_lines)[0].strip()
    translated_lines = (
        [line for line in translated.splitlines() if line.strip()]
        if translated is not None
        else []
    )
    if (
        not translated_lines
        or _admonition_marker_type(translated_lines[0])
        != _admonition_marker_type(new_marker)
    ):
        raise PatchError("translated admonition marker change has diverged")

    expected_lines = [
        line for line in (segment.new_source or "").splitlines() if line.strip()
    ]

    lines = text.splitlines(keepends=True)
    starts = _admonition_start_indexes(lines)
    ordinal = segment.old_block_ordinal
    if (
        ordinal is None
        or ordinal >= len(starts)
        or not _admonition_marker_count_matches(len(starts), segment)
    ):
        raise PatchError(f"missing existing admonition marker: {old_marker}")

    index = starts[ordinal]
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
        end = index + 1
        while end < len(lines) and lines[end].strip().startswith(">"):
            end += 1
        current = "".join(lines[index:end])
        replacement = _format_replacement(
            translated or "",
            trailing=_trailing_separator(current),
        )
        if current == replacement:
            return text
        return "".join(lines[:index]) + replacement + "".join(lines[end:])

    if not _admonition_body_matches_source(lines, index, segment):
        raise PatchError(
            "could not verify existing admonition body: "
            + (segment.after_context or old_marker)
        )

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
    """Indexes of top-level blockquote groups outside code."""
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
    """Indexes of admonition-opening lines (GFM or legacy), outside code."""
    return [
        index
        for index in _blockquote_start_indexes(lines)
        if _ADMONITION_MARKER_RE.fullmatch(lines[index].strip())
        or _LEGACY_ADMONITION_RE.match(lines[index].strip())
    ]


def _admonition_marker_ordinal(source_lines: list[str], lineno: int) -> int:
    starts = _admonition_start_indexes(source_lines)
    target = lineno - 1
    if target not in starts:
        raise PatchError("source admonition marker occurrence is missing")
    return starts.index(target)


def _admonition_source_region(
    source_lines: list[str], lineno: int
) -> tuple[str, int, int]:
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
    return translated.rstrip() + trailing


def _trailing_separator(block_text: str) -> str:
    if block_text.endswith("\n\n"):
        return "\n\n"
    if block_text.endswith("\n"):
        return "\n"
    return ""


def _meaningful_lines(lines: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(line for line in lines if line.strip())


def _joined(lines: tuple[str, ...]) -> str:
    return " ".join(_meaningful_lines(lines))


def _normalize_text(text: str) -> str:
    return normalize_annotation_anchor(text)


def _ensure_single_eof_newline(text: str) -> str:
    return text.rstrip("\n") + "\n" if text else text


def _hunk_has_code_fence_change(hunk: DiffHunk) -> bool:
    return any(
        line.kind in {"add", "delete"} and fence_token(line.text)
        for line in hunk.lines
    )


def _hunk_region_segment(hunk: DiffHunk, source_lines: list[str]) -> BlockChange:
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
    context: DiffLine | None = None
    for line in hunk.lines:
        if line.kind != "context":
            return context
        if _normalize_text(line.text):
            context = line
    return context


def _after_hunk_context_line(hunk: DiffHunk) -> DiffLine | None:
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
    if _has_structural_lines(segment.new_lines) or _has_structural_lines(
        segment.old_lines
    ):
        new_source = segment.new_source or _source_from_lines(segment.new_lines)
        named_anchor_change = segment.is_named_anchor_change
        admonition_marker_change = segment.is_admonition_marker_change
        old_block_ordinal = segment.old_block_ordinal
        old_anchor_occurrences = segment.old_anchor_occurrences
        new_anchor_occurrences = segment.new_anchor_occurrences
        if named_anchor_change and _meaningful_lines(segment.old_lines):
            old_block_ordinal = _raw_line_ordinal(
                old_source_lines,
                _meaningful_lines(segment.old_lines)[0],
                segment.old_linenos[0],
            )
        elif admonition_marker_change and segment.old_linenos:
            old_block_ordinal = _admonition_marker_ordinal(
                old_source_lines, segment.old_linenos[0]
            )
            old_anchor_occurrences = len(
                _admonition_start_indexes(old_source_lines)
            )
            old_source, old_start, old_end = _admonition_source_region(
                old_source_lines,
                segment.old_linenos[0],
            )
            new_source, new_start, new_end = _admonition_source_region(
                new_source_lines,
                segment.new_linenos[0],
            )
        if named_anchor_change:
            new_anchor_occurrences = sum(
                line
                == (
                    _meaningful_lines(segment.new_lines)[0]
                    if _meaningful_lines(segment.new_lines)
                    else _meaningful_lines(segment.old_lines)[0]
                )
                for line in new_source_lines
            )
        elif admonition_marker_change:
            new_anchor_occurrences = len(
                _admonition_start_indexes(new_source_lines)
            )
        return [
            replace(
                segment,
                new_source=new_source,
                new_anchor=(
                    segment.new_anchor
                    or (
                        _primary_source_anchor(new_source)
                        if not _meaningful_lines(segment.old_lines)
                        else None
                    )
                ),
                old_block_ordinal=old_block_ordinal,
                old_anchor_occurrences=old_anchor_occurrences,
                old_source=(
                    old_source if admonition_marker_change else segment.old_source
                ),
                old_block_start=(
                    old_start
                    if admonition_marker_change
                    else segment.old_block_start
                ),
                old_block_end=(
                    old_end if admonition_marker_change else segment.old_block_end
                ),
                new_block_start=(
                    new_start
                    if admonition_marker_change
                    else segment.new_block_start
                ),
                new_block_end=(
                    new_end if admonition_marker_change else segment.new_block_end
                ),
                new_anchor_occurrences=new_anchor_occurrences,
                table_row=_source_table_row_change(segment, old_source_lines),
            )
        ]

    new_blocks = _blocks_for_linenos(new_source_blocks, segment.new_linenos)
    old_blocks = _blocks_for_linenos(old_source_blocks, segment.old_linenos)
    whitespace_only = not _meaningful_lines(
        segment.old_lines
    ) and not _meaningful_lines(segment.new_lines)

    if whitespace_only:
        new_blocks = _context_boundary_blocks(
            new_source_blocks,
            segment.before_new_lineno,
            segment.after_new_lineno,
        )
        old_blocks = _context_boundary_blocks(
            old_source_blocks,
            segment.before_old_lineno,
            segment.after_old_lineno,
        )
        if [block.text for block in old_blocks] == [
            block.text for block in new_blocks
        ]:
            return []

    if not new_blocks:
        context_block = _shared_context_block(
            new_source_blocks,
            segment.before_new_lineno,
            segment.after_new_lineno,
        )
        if context_block is not None:
            new_blocks = [context_block]

    if not old_blocks:
        context_block = _shared_context_block(
            old_source_blocks,
            segment.before_old_lineno,
            segment.after_old_lineno,
        )
        if context_block is not None:
            old_blocks = [context_block]

    if not old_blocks and len(new_blocks) > 1:
        _require_plain_block_range(new_blocks, new_source_lines)
        return [
            replace(
                segment,
                new_source=_join_source_blocks(new_blocks),
                new_anchor=new_blocks[0].comment,
                new_anchors=tuple(block.comment for block in new_blocks),
                new_block_ordinal=_block_ordinal(new_source_blocks, new_blocks[0]),
                new_block_start=new_blocks[0].start_lineno,
                new_block_end=new_blocks[-1].end_lineno,
                new_previous_anchor=_range_neighbor_anchor(
                    new_source_blocks, new_blocks, -1
                ),
                new_next_anchor=_range_neighbor_anchor(
                    new_source_blocks, new_blocks, 1
                ),
            )
        ]

    if old_blocks and new_blocks and len(old_blocks) != len(new_blocks):
        _require_plain_block_range(old_blocks, old_source_lines)
        _require_plain_block_range(new_blocks, new_source_lines)
        return [
            replace(
                segment,
                old_source=_join_source_blocks(old_blocks),
                old_anchors=tuple(block.comment for block in old_blocks),
                old_block_ordinal=_block_ordinal(old_source_blocks, old_blocks[0]),
                old_block_start=old_blocks[0].start_lineno,
                old_block_end=old_blocks[-1].end_lineno,
                old_previous_anchor=_range_neighbor_anchor(
                    old_source_blocks, old_blocks, -1
                ),
                old_next_anchor=_range_neighbor_anchor(
                    old_source_blocks, old_blocks, 1
                ),
                new_source=_join_source_blocks(new_blocks),
                new_anchor=new_blocks[0].comment,
                new_anchors=tuple(block.comment for block in new_blocks),
                new_block_ordinal=_block_ordinal(new_source_blocks, new_blocks[0]),
                new_block_start=new_blocks[0].start_lineno,
                new_block_end=new_blocks[-1].end_lineno,
                new_previous_anchor=_range_neighbor_anchor(
                    new_source_blocks, new_blocks, -1
                ),
                new_next_anchor=_range_neighbor_anchor(
                    new_source_blocks, new_blocks, 1
                ),
            )
        ]

    if not new_blocks and old_blocks:
        return [
            replace(
                segment,
                old_source=_join_source_blocks(old_blocks),
                old_anchors=tuple(block.comment for block in old_blocks),
                old_block_ordinal=_block_ordinal(old_source_blocks, old_blocks[0]),
                old_block_start=old_blocks[0].start_lineno,
                old_block_end=old_blocks[-1].end_lineno,
                old_previous_anchor=_range_neighbor_anchor(
                    old_source_blocks, old_blocks, -1
                ),
                old_next_anchor=_range_neighbor_anchor(
                    old_source_blocks, old_blocks, 1
                ),
            )
        ]

    if not new_blocks:
        return [segment]

    expanded: list[BlockChange] = []
    previous_comment = segment.before_context
    for index, new_block in enumerate(new_blocks):
        old_block = _paired_old_block(old_blocks, new_blocks, index)

        expanded.append(
            replace(
                segment,
                old_lines=_lines_in_block(
                    segment.old_lines,
                    segment.old_linenos,
                    old_block,
                ),
                new_lines=_lines_in_block(
                    segment.new_lines,
                    segment.new_linenos,
                    new_block,
                ),
                before_context=previous_comment,
                after_context=(
                    segment.after_context if index == len(new_blocks) - 1 else None
                ),
                old_source=old_block.text if old_block is not None else None,
                old_anchors=(old_block.comment,) if old_block is not None else (),
                old_block_ordinal=(
                    _block_ordinal(old_source_blocks, old_block)
                    if old_block is not None
                    else None
                ),
                old_block_start=(
                    old_block.start_lineno if old_block is not None else None
                ),
                old_block_end=old_block.end_lineno if old_block is not None else None,
                new_source=new_block.text,
                new_anchor=new_block.comment,
                new_anchors=(new_block.comment,),
                new_block_ordinal=_block_ordinal(new_source_blocks, new_block),
                new_block_start=new_block.start_lineno,
                new_block_end=new_block.end_lineno,
            )
        )
        previous_comment = new_block.comment

    return expanded


def _shared_context_block(
    blocks: list[SourceBlock],
    before_lineno: int | None,
    after_lineno: int | None,
) -> SourceBlock | None:
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
    if len(old_blocks) == len(new_blocks):
        return old_blocks[index]
    return None


def _join_source_blocks(blocks: list[SourceBlock]) -> str:
    return "\n\n".join(block.text.rstrip("\n") for block in blocks) + "\n"


def _require_plain_block_range(
    blocks: list[SourceBlock], source_lines: list[str]
) -> None:
    for previous, following in zip(blocks, blocks[1:]):
        between = source_lines[previous.end_lineno : following.start_lineno - 1]
        if any(line.strip() for line in between):
            raise PatchError(
                "changed source block range contains unsupported structural markup"
            )


def _range_neighbor_anchor(
    all_blocks: list[SourceBlock], range_blocks: list[SourceBlock], offset: int
) -> str | None:
    target = range_blocks[0] if offset < 0 else range_blocks[-1]
    index = all_blocks.index(target) + offset
    return all_blocks[index].comment if 0 <= index < len(all_blocks) else None


def _lines_in_block(
    lines: tuple[str, ...],
    linenos: tuple[int, ...],
    block: SourceBlock | None,
) -> tuple[str, ...]:
    if block is None:
        return lines
    selected = tuple(
        line
        for line, lineno in zip(lines, linenos, strict=True)
        if block.start_lineno <= lineno <= block.end_lineno
    )
    return selected or lines


def _block_ordinal(blocks: list[SourceBlock], target: SourceBlock) -> int:
    matching = [block for block in blocks if block.comment == target.comment]
    return matching.index(target)


def _primary_source_anchor(source: str) -> str | None:
    blocks = _source_blocks(source)
    return blocks[0].comment if blocks else None


def _blocks_for_linenos(
    source_blocks: list[SourceBlock], linenos: tuple[int, ...]
) -> list[SourceBlock]:
    return [
        block
        for block in source_blocks
        if any(block.start_lineno <= lineno <= block.end_lineno for lineno in linenos)
    ]


def _has_structural_lines(lines: tuple[str, ...]) -> bool:
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
    indexes = [
        index for index, line in enumerate(source_lines) if line == expected
    ]
    target = lineno - 1
    if target not in indexes:
        raise PatchError(f"source line occurrence is missing: {expected}")
    return indexes.index(target)


def _reverse_apply_hunks(new_lines: list[str], hunks: tuple[DiffHunk, ...]) -> list[str]:
    """Reconstruct the old source lines by reversing each hunk on the new source."""
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
    """Return (start, end) line indexes (inclusive) of each fenced code block."""
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
    return tuple("\n".join(lines[start : end + 1]) for start, end in regions)


def _fenced_code_blocks(text: str) -> tuple[str, ...]:
    lines = text.splitlines()
    return _code_blocks_from_regions(lines, _code_fence_regions(lines))


def _is_fenced_code_source(source: str) -> bool:
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
    """Index of the region whose interior (between the fences) holds `index`."""
    for position, (start, end) in enumerate(regions):
        if start < index < end:
            return position
    return None


def _code_region_indexes(
    segment: BlockChange,
    new_regions: list[tuple[int, int]],
    old_regions: list[tuple[int, int]],
) -> tuple[int | None, int | None]:
    """New and old region indexes for an interior fenced-code change.

    Whole-block changes carry a fence line and stay on the structural path.
    Context line numbers fill the side without a changed line for pure interior
    insertions or deletions.
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
    """Build a verbatim swap of one code fence to its new source block."""
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
    """True when `block` holds every anchor line (counting duplicates)."""
    remaining = list(block)
    for line in anchors:
        if line in remaining:
            remaining.remove(line)
        else:
            return False
    return True


def _source_from_lines(lines: tuple[str, ...]) -> str:
    return "\n".join(lines).rstrip("\n") + "\n"


def _format_raw_insertion(translated: str, segment: BlockChange) -> str:
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
    index = _raw_insertion_index(lines, segment)
    if index is not None:
        return "".join(lines[:index]) + insertion + "".join(lines[index:])
    return None


def _raw_insertion_index(lines: list[str], segment: BlockChange) -> int | None:
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
    lines = text.splitlines(keepends=True)
    bounds = _raw_context_bounds(lines, _blocks(text), segment)
    if bounds is None:
        return None
    start, end = bounds
    return "".join(lines[start:end])


def _replace_between_raw_contexts(
    text: str, segment: BlockChange, translated: str
) -> str | None:
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
    if segment.after_context:
        index = _find_raw_context_line_after(lines, segment.after_context, start)
        if index is not None:
            return index
    for index in range(start + 1, len(lines)):
        if is_named_anchor_line(lines[index]):
            return index
    return len(lines)


def _source_text_lines(segment: BlockChange) -> tuple[str, ...]:
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
    return tuple(
        line
        for line in _meaningful_lines(segment.old_lines)
        if _is_raw_evidence_line(line)
    )


def _is_raw_evidence_line(line: str) -> bool:
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
    bounds = [block.start for block in _matching_blocks(blocks, context)]
    normalized = _normalize_text(context)
    if normalized:
        bounds.extend(
            _raw_context_indexes(lines, context, include_code=include_code)
        )
    return bounds


def _find_raw_context_line(lines: list[str], context: str) -> int | None:
    indexes = _raw_context_indexes(lines, context)
    return indexes[0] if indexes else None


def _find_raw_context_line_after(
    lines: list[str], context: str, after_index: int
) -> int | None:
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
    indexes: list[int] = []
    in_comment = False
    in_code = False
    fence = ""

    for index, line in enumerate(lines):
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue

        if "<!--" in line:
            if "-->" not in line.split("<!--", 1)[1]:
                in_comment = True
            continue

        token = fence_token(line)
        if token:
            if include_code:
                indexes.append(index)
            if not in_code:
                in_code, fence = True, token
            elif closes_fence(line, fence):
                in_code = False
            continue
        if not in_code or include_code:
            indexes.append(index)

    return indexes


def _table_row_cells(line: str) -> tuple[str, ...] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    cells = tuple(_normalize_text(cell) for cell in stripped.strip("|").split("|"))
    return cells if len(cells) > 1 else None


def _table_match_cells(cells: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        re.sub(r"\s*,\s*", ", ", cell.replace("、", ",")).strip()
        for cell in cells
    )


def _is_table_separator_cells(cells: tuple[str, ...]) -> bool:
    return all(cell and set(cell) <= {"-", ":"} for cell in cells)


def _single_table_row_lines(segment: BlockChange) -> tuple[str, str] | None:
    """The lone old/new table row of a segment, or None when not row-shaped."""
    old_meaningful = _meaningful_lines(segment.old_lines)
    new_meaningful = _meaningful_lines(segment.new_lines)
    if len(old_meaningful) != 1 or len(new_meaningful) != 1:
        return None
    old_cells = _table_row_cells(old_meaningful[0])
    new_cells = _table_row_cells(new_meaningful[0])
    if old_cells is None or new_cells is None or len(old_cells) != len(new_cells):
        return None
    if _is_table_separator_cells(old_cells):
        return None
    return old_meaningful[0], new_meaningful[0]


def _table_regions(lines: list[str]) -> list[list[int]]:
    """Non-separator row indexes of each table outside fenced or indented code."""
    fenced: set[int] = set()
    for start, end in _code_fence_regions(lines):
        fenced.update(range(start, end + 1))
    tables: list[list[int]] = []
    current: list[int] | None = None
    for index, line in enumerate(lines):
        cells = (
            _table_row_cells(line)
            if index not in fenced and not line.startswith(("    ", "\t"))
            else None
        )
        if cells is None:
            current = None
            continue
        if current is None:
            current = []
            tables.append(current)
        if not _is_table_separator_cells(cells):
            current.append(index)
    return tables


def _source_table_row_change(
    segment: BlockChange, old_source_lines: list[str]
) -> TableRowChange | None:
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
        if (
            len(tables) != reference.table_count
            or reference.table_ordinal >= len(tables)
        ):
            return None
        rows = tables[reference.table_ordinal]
        if len(rows) != reference.row_count:
            return None
        index = rows[reference.row_ordinal]
        cells = _table_row_cells(lines[index])
        if cells is None or len(cells) != len(old_cells):
            return None
        if translated is not None and len(tables) == 1:
            translated_cells = _table_row_cells(translated.rstrip("\r\n"))
            if (
                translated_cells is not None
                and _table_match_cells(cells)
                == _table_match_cells(translated_cells)
            ):
                return index
        candidates = _identified_table_row_candidates(
            lines,
            [row for table in tables for row in table],
            old_cells,
            new_cells,
        )
        if not candidates:
            if len(tables) != 1 or not _table_context_identifies_row(
                lines,
                segment,
                index,
                [index],
            ):
                return None
        else:
            if index not in candidates:
                return None
            if len(candidates) > 1 and not _table_context_identifies_row(
                lines,
                segment,
                index,
                candidates,
            ):
                return None
        return index

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
    """Raw-context validation applied to every candidate, even a single one."""
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
    lines = text.splitlines(keepends=True)
    index = _table_row_index(lines, segment)
    return lines[index] if index is not None else None


def _replace_table_row(text: str, segment: BlockChange, translated: str) -> str | None:
    lines = text.splitlines(keepends=True)
    index = _table_row_index(lines, segment, translated=translated)
    if index is None:
        return None
    replacement = translated.rstrip("\n") + ("\n" if lines[index].endswith("\n") else "")
    return "".join(lines[:index]) + replacement + "".join(lines[index + 1 :])


def _coalesce_source_block_segments(segments: list[BlockChange]) -> list[BlockChange]:
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
    return _block_for_lineno(blocks, lineno) if lineno is not None else None


def _source_block_index(
    blocks: list[SourceBlock],
    *,
    start: int | None,
    linenos: tuple[int, ...],
) -> int | None:
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
    """Anchor-name -> section position, or None when names are not unique."""
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
    """Accept a prefix change that only permutes section TOC links.

    Every non-link prefix line must stay identical in place, the link lines
    must be a permutation of each other targeting known section anchors, and
    the new link order must follow the new section order.
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
        old_anchor = _toc_link_anchor(old_line)
        new_anchor = _toc_link_anchor(new_line)
        if old_anchor is None and new_anchor is None:
            if old_line != new_line:
                return False
            continue
        if old_anchor is None or new_anchor is None:
            return False
        old_links.append(old_line)
        new_links.append(new_line)
    if not old_links or Counter(old_links) != Counter(new_links):
        return False
    link_positions: list[int] = []
    for line in new_links:
        anchor = _toc_link_anchor(line)
        if anchor is None or anchor not in positions:
            return False
        link_positions.append(positions[anchor])
    return link_positions == sorted(link_positions)


def _toc_link_anchor(line: str) -> str | None:
    match = _TOC_LINK_RE.match(line.rstrip("\r\n"))
    return match.group(1) if match is not None else None


def _apply_named_section_reorder(
    text: str,
    reorder: NamedSectionReorder,
) -> str:
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
    blocks: list[SourceBlock] = []
    paragraph: list[tuple[int, str]] = []
    in_code = False
    fence = ""
    in_front_matter = False
    source_comment_lines = standalone_html_comment_line_numbers(source)
    reference_lines = {
        line + 1 for line in reference_definition_line_numbers(source)
    }

    def flush_paragraph() -> None:
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
        if is_non_annotatable_line(line):
            flush_paragraph()
            continue
        paragraph.append((lineno, line))

    flush_paragraph()
    return blocks


def _plan_source_blocks(blocks: list[SourceBlock]) -> list[SourceBlock]:
    return [
        block
        for block in blocks
        if not _is_inline_code_identifier_list(block.text)
    ]


def _is_inline_code_identifier_list(text: str) -> bool:
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return False
    for line in lines:
        list_item = _LIST_ITEM_PREFIX_RE.match(line)
        if list_item is None:
            return False
        body = line[list_item.end() :]
        if not inline_code_contents(body) or strip_inline_code(body).strip(
            " `*_~.,:;()[]&/,+"
        ):
            return False
    return True


def _inline_code_list_is_applied(text: str, segment: BlockChange) -> bool:
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
