"""Apply translated source diff hunks to annotated locale Markdown.

The translation workflow uses English HTML comments as stable anchors. A
changed English hunk is translated separately, then merged into the existing
locale document by replacing, inserting, or deleting the matching annotated
block.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from ..common.markdown import (
    closes_fence,
    fence_token,
    html_comment_spans,
    is_heading_line,
    is_named_anchor_line,
    strip_title_attr_line,
)
from ..source.diff import DiffHunk

_ADMONITION_MARKER_RE = re.compile(
    r"^>\s*\[!(?:NOTE|TIP|WARNING|CAUTION|IMPORTANT)]\s*$", re.IGNORECASE
)


class PatchError(ValueError):
    """Raised when a diff hunk cannot be applied to the existing translation."""


@dataclass(frozen=True)
class Segment:
    old_lines: tuple[str, ...]
    new_lines: tuple[str, ...]
    before_context: str | None
    after_context: str | None
    old_linenos: tuple[int, ...] = ()
    new_linenos: tuple[int, ...] = ()
    new_source: str | None = None
    # An interior change to one fenced code block (see CodeChange). Code is never
    # translated, so it is handled by a verbatim block swap, not the LLM path.
    code_block: CodeChange | None = None

    @property
    def needs_translation(self) -> bool:
        if self.code_block is not None:
            return False
        return bool(_meaningful_lines(self.new_lines)) or bool(
            self.new_source and self.new_source.strip()
        )

    @property
    def is_deletion(self) -> bool:
        if self.code_block is not None:
            return False
        return bool(_meaningful_lines(self.old_lines)) and not self.needs_translation


@dataclass(frozen=True)
class CodeChange:
    """An interior change to one fenced code block.

    Code is copied verbatim from the source and never translated, so a changed
    block is located by its index in document order and the whole block is
    swapped for the new source block. This keeps the locale code byte-identical
    to English (which verification requires, even for things like reordered
    imports) and stays idempotent: a re-run finds the block already equal to
    ``new_block`` and does nothing.

    ``anchors`` are the block's unchanged lines (everything except the freshly
    added lines). The swap only happens when the located block still contains
    all of them, so a diverged document is left untouched rather than corrupted,
    while reordered-but-equivalent code is still recognised and canonicalised.
    """

    block_index: int
    new_block: str
    anchors: tuple[str, ...]


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


def segments_from_hunks(
    hunks: tuple[DiffHunk, ...], source_text: str | None = None
) -> list[Segment]:
    segments: list[Segment] = []

    for hunk in hunks:
        before_context: str | None = None
        old_lines: list[str] = []
        new_lines: list[str] = []
        old_linenos: list[int] = []
        new_linenos: list[int] = []

        def flush(after_context: str | None = None) -> None:
            nonlocal before_context, old_lines, new_lines, old_linenos, new_linenos
            if old_lines or new_lines:
                segments.append(
                    Segment(
                        old_lines=tuple(old_lines),
                        new_lines=tuple(new_lines),
                        before_context=before_context,
                        after_context=after_context,
                        old_linenos=tuple(old_linenos),
                        new_linenos=tuple(new_linenos),
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
                        flush(context)
                elif context:
                    before_context = context
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

    filtered = [
        segment
        for segment in segments
        if _meaningful_lines(segment.old_lines) or _meaningful_lines(segment.new_lines)
    ]
    if source_text is None:
        return filtered

    source_lines = source_text.splitlines()
    new_regions = _code_fence_regions(source_lines)
    old_regions = _code_fence_regions(_reverse_apply_hunks(source_lines, hunks))
    source_blocks = _source_blocks(source_text)

    expanded: list[Segment] = []
    emitted_regions: set[int] = set()
    for segment in filtered:
        region = _code_region_index(segment, new_regions, old_regions)
        if region is not None and region < len(new_regions):
            if region in emitted_regions:
                continue
            emitted_regions.add(region)
            group = [
                other
                for other in filtered
                if _code_region_index(other, new_regions, old_regions) == region
            ]
            expanded.append(
                _code_block_segment(group, source_lines, new_regions[region], region)
            )
            continue
        expanded.extend(_expand_to_source_blocks(segment, source_blocks))
    return _coalesce_source_block_segments(expanded)


def diff_text(segment: Segment) -> str:
    lines: list[str] = []
    for old_line in segment.old_lines:
        lines.append(f"- {old_line}")
    for new_line in segment.new_lines:
        lines.append(f"+ {new_line}")
    return "\n".join(lines)


def source_text(segment: Segment) -> str:
    if segment.new_source is not None:
        return segment.new_source.rstrip() + "\n"
    return "\n".join(_meaningful_lines(segment.new_lines)).rstrip() + "\n"


def existing_context(text: str, segment: Segment) -> str:
    blocks = _blocks(text)
    if _meaningful_lines(segment.old_lines):
        try:
            block = _find_block(blocks, _joined(segment.old_lines))
            return block.text.strip()
        except PatchError:
            context = _context_between_raw_contexts(text, segment)
            if context:
                return context.strip()
            raise
    for anchor in (segment.before_context, segment.after_context):
        if anchor:
            block = _find_block(blocks, anchor, required=False)
            if block:
                return block.text.strip()
    return "(none)"


def apply_segments(
    existing: str, segments: list[Segment], translated_blocks: list[str]
) -> str:
    translated_iter = iter(translated_blocks)
    text = existing

    for segment in segments:
        if segment.code_block is not None:
            text = _apply_code_block(text, segment.code_block)
            continue
        translated = next(translated_iter, None) if segment.needs_translation else None
        if _meaningful_lines(segment.old_lines) and segment.needs_translation:
            if translated is None:
                raise PatchError("missing translated replacement block")
            text = _replace_segment(text, segment, translated)
        elif segment.is_deletion:
            text = _delete_block(text, _joined(segment.old_lines))
        elif segment.needs_translation:
            if translated is None:
                raise PatchError("missing translated insertion block")
            text = _insert_block(text, segment, translated)

    text = _collapse_consecutive_admonition_markers(text)
    return _ensure_single_eof_newline(text)


def _collapse_consecutive_admonition_markers(text: str) -> str:
    """Drop a second consecutive identical admonition marker line.

    A changed admonition body is translated without its ``> [!NOTE]`` marker
    (that line stays as context), but the model often re-emits the marker in
    its output. Placing that block right after the retained anchor marker would
    leave two markers in a row, which is never valid Markdown. Collapse
    identical consecutive markers back into one.
    """
    out: list[str] = []
    for line in text.split("\n"):
        if (
            out
            and _ADMONITION_MARKER_RE.match(line.strip())
            and line.strip() == out[-1].strip()
        ):
            continue
        out.append(line)
    return "\n".join(out)


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


def _translated_block_end(lines: list[str], start: int, limit: int) -> int:
    index = start
    seen_content = False
    while index < limit:
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
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            token = stripped[:3]
            if not in_code:
                in_code = True
                fence = token
            elif stripped.startswith(fence):
                in_code = False
            continue
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
    blocks: list[AnnotatedBlock], comment: str, *, required: bool = True
) -> AnnotatedBlock | None:
    matches = _matching_blocks(blocks, comment)
    if matches:
        return matches[0]
    if required:
        raise PatchError(
            f"missing existing translation block for: {_normalize_text(comment)}"
        )
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


def _replace_block(text: str, old_comment: str, translated: str) -> str:
    lines = text.splitlines(keepends=True)
    block = _find_block(_blocks(text), old_comment)
    replacement = _format_replacement(translated, trailing=_trailing_separator(block.text))
    return "".join(lines[: block.start]) + replacement + "".join(lines[block.end :])


def _replace_segment(text: str, segment: Segment, translated: str) -> str:
    try:
        return _replace_block(text, _joined(segment.old_lines), translated)
    except PatchError:
        replaced = _replace_between_raw_contexts(text, segment, translated)
        if replaced is not None:
            return replaced
        raise


def _delete_block(text: str, old_comment: str) -> str:
    lines = text.splitlines(keepends=True)
    block = _find_block(_blocks(text), old_comment)
    return "".join(lines[: block.start]) + "".join(lines[block.end :])


def _insert_block(text: str, segment: Segment, translated: str) -> str:
    lines = text.splitlines(keepends=True)
    blocks = _blocks(text)
    insertion = _format_replacement(translated, trailing="\n\n")
    existing_insert = _replace_existing_insertion(text, segment, translated)
    if existing_insert is not None:
        return existing_insert
    if segment.before_context:
        block = _find_block(blocks, segment.before_context, required=False)
        if block:
            return "".join(lines[: block.end]) + insertion + "".join(lines[block.end :])
    if segment.after_context:
        block = _find_block(blocks, segment.after_context, required=False)
        if block:
            return "".join(lines[: block.start]) + insertion + "".join(lines[block.start :])
    raw_insertion = _format_raw_insertion(translated, segment)
    raw_text = _insert_near_raw_context(lines, segment, raw_insertion)
    if raw_text is not None:
        return raw_text
    raise PatchError("missing insertion context")


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
    return " ".join(text.split())


def _ensure_single_eof_newline(text: str) -> str:
    return text.rstrip("\n") + "\n" if text else text


def _expand_to_source_blocks(
    segment: Segment, source_blocks: list[SourceBlock]
) -> list[Segment]:
    if _has_structural_lines(segment.new_lines):
        return [
            Segment(
                old_lines=segment.old_lines,
                new_lines=segment.new_lines,
                before_context=segment.before_context,
                after_context=segment.after_context,
                old_linenos=segment.old_linenos,
                new_linenos=segment.new_linenos,
                new_source=_source_from_lines(segment.new_lines),
            )
        ]

    new_blocks = _blocks_for_linenos(source_blocks, segment.new_linenos)
    before_block = _block_for_text(source_blocks, segment.before_context)
    after_block = _block_for_text(source_blocks, segment.after_context)

    if not new_blocks and before_block is not None and before_block == after_block:
        new_blocks = [before_block]

    if not new_blocks:
        return [segment]

    expanded: list[Segment] = []
    previous_comment = segment.before_context
    for index, new_block in enumerate(new_blocks):
        old_lines = segment.old_lines
        if not _meaningful_lines(old_lines):
            if before_block == new_block and segment.before_context:
                old_lines = (segment.before_context,)
            elif after_block == new_block and segment.after_context:
                old_lines = (segment.after_context,)

        expanded.append(
            Segment(
                old_lines=old_lines,
                new_lines=tuple(new_block.text.rstrip("\n").split("\n")),
                before_context=previous_comment,
                after_context=(
                    segment.after_context if index == len(new_blocks) - 1 else None
                ),
                old_linenos=segment.old_linenos,
                new_linenos=tuple(range(new_block.start_lineno, new_block.end_lineno + 1)),
                new_source=new_block.text,
            )
        )
        previous_comment = new_block.comment

    return expanded


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


def _reverse_apply_hunks(new_lines: list[str], hunks: tuple[DiffHunk, ...]) -> list[str]:
    """Reconstruct the old source lines by reversing each hunk on the new source."""
    lines = list(new_lines)
    for hunk in sorted(hunks, key=lambda item: item.new_start, reverse=True):
        old_segment = [
            line.text for line in hunk.lines if line.kind in ("context", "delete")
        ]
        start = hunk.new_start - 1
        lines[start : start + hunk.new_count] = old_segment
    return lines


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


def _region_of_index(regions: list[tuple[int, int]], index: int) -> int | None:
    """Index of the region whose interior (between the fences) holds `index`."""
    for position, (start, end) in enumerate(regions):
        if start < index < end:
            return position
    return None


def _code_region_index(
    segment: Segment,
    new_regions: list[tuple[int, int]],
    old_regions: list[tuple[int, int]],
) -> int | None:
    """Region index when a segment changes only the interior of one code block.

    Insertions and modifications are located by their new line numbers; pure
    deletions by their old line numbers (which map to the same block, since an
    interior edit never adds or removes a whole fence). Whole-block changes carry
    a fence line and are left to the annotated-block path.
    """
    if segment.new_linenos:
        if _has_structural_lines(segment.new_lines):
            return None
        found = {_region_of_index(new_regions, line - 1) for line in segment.new_linenos}
        return found.pop() if len(found) == 1 and None not in found else None
    if segment.old_linenos and _meaningful_lines(segment.old_lines):
        if _has_structural_lines(segment.old_lines):
            return None
        found = {_region_of_index(old_regions, line - 1) for line in segment.old_linenos}
        return found.pop() if len(found) == 1 and None not in found else None
    return None


def _code_block_segment(
    group: list[Segment],
    source_lines: list[str],
    region: tuple[int, int],
    block_index: int,
) -> Segment:
    """Build a verbatim swap of one code fence to its new source block."""
    start, end = region
    new_block_lines = source_lines[start : end + 1]
    new_block = "\n".join(new_block_lines)
    added = {line for segment in group for line in segment.new_lines}
    anchors = tuple(
        line for line in new_block_lines if line.strip() and line not in added
    )
    return Segment(
        old_lines=(),
        new_lines=(),
        before_context=None,
        after_context=None,
        code_block=CodeChange(
            block_index=block_index, new_block=new_block, anchors=anchors
        ),
    )


def _apply_code_block(text: str, change: CodeChange) -> str:
    lines = text.split("\n")
    regions = _code_fence_regions(lines)
    if not 0 <= change.block_index < len(regions):
        return text  # block count diverged; cannot locate safely, leave as is
    start, end = regions[change.block_index]
    block = lines[start : end + 1]
    if block == change.new_block.split("\n"):
        return text  # already the new source block (idempotent re-run)
    if not _contains_all(block, change.anchors):
        return text  # diverged from source; skip rather than corrupt
    return "\n".join(lines[:start] + change.new_block.split("\n") + lines[end + 1 :])


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


def _format_raw_insertion(translated: str, segment: Segment) -> str:
    trailing_blank_lines = 0
    for line in reversed(segment.new_lines):
        if line.strip():
            break
        trailing_blank_lines += 1
    return translated.rstrip("\n") + ("\n" * max(1, trailing_blank_lines + 1))


def _insert_near_raw_context(
    lines: list[str], segment: Segment, insertion: str
) -> str | None:
    if segment.after_context:
        index = _find_raw_context_line(lines, segment.after_context)
        if index is not None:
            return "".join(lines[:index]) + insertion + "".join(lines[index:])
    if segment.before_context:
        index = _find_raw_context_line(lines, segment.before_context)
        if index is not None:
            return "".join(lines[: index + 1]) + insertion + "".join(lines[index + 1 :])
    return None


def _context_between_raw_contexts(text: str, segment: Segment) -> str | None:
    lines = text.splitlines(keepends=True)
    bounds = _raw_context_bounds(lines, _blocks(text), segment)
    if bounds is None:
        return None
    start, end = bounds
    return "".join(lines[start:end])


def _replace_between_raw_contexts(
    text: str, segment: Segment, translated: str
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
    text: str, segment: Segment, translated: str
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
    lines: list[str], segment: Segment
) -> int | None:
    for source_line in _source_text_lines(segment):
        if not is_named_anchor_line(source_line):
            continue
        index = _find_raw_context_line(lines, source_line)
        if index is not None:
            return index
    return None


def _find_existing_insertion_end(
    lines: list[str], segment: Segment, start: int
) -> int | None:
    if segment.after_context:
        index = _find_raw_context_line_after(lines, segment.after_context, start)
        if index is not None:
            return index
    for index in range(start + 1, len(lines)):
        if is_named_anchor_line(lines[index]):
            return index
    return len(lines)


def _source_text_lines(segment: Segment) -> tuple[str, ...]:
    if segment.new_source is not None:
        return tuple(segment.new_source.rstrip("\n").split("\n"))
    return _meaningful_lines(segment.new_lines)


def _raw_context_bounds(
    lines: list[str], blocks: list[AnnotatedBlock], segment: Segment
) -> tuple[int, int] | None:
    if not segment.before_context or not segment.after_context:
        return None

    before_bounds = _before_context_boundaries(lines, blocks, segment.before_context)
    after_bounds = _after_context_boundaries(lines, blocks, segment.after_context)
    candidates = [
        (end - start, start, end)
        for start in before_bounds
        for end in after_bounds
        if start <= end
    ]
    if not candidates:
        return None
    _distance, start, end = min(candidates)
    return start, end


def _before_context_boundaries(
    lines: list[str], blocks: list[AnnotatedBlock], context: str
) -> list[int]:
    bounds = [block.end for block in _matching_blocks(blocks, context)]
    normalized = _normalize_text(context)
    if normalized:
        bounds.extend(
            index + 1
            for index, line in enumerate(lines)
            if _normalize_text(line) == normalized
        )
    return bounds


def _after_context_boundaries(
    lines: list[str], blocks: list[AnnotatedBlock], context: str
) -> list[int]:
    bounds = [block.start for block in _matching_blocks(blocks, context)]
    normalized = _normalize_text(context)
    if normalized:
        bounds.extend(
            index
            for index, line in enumerate(lines)
            if _normalize_text(line) == normalized
        )
    return bounds


def _find_raw_context_line(lines: list[str], context: str) -> int | None:
    normalized = _normalize_text(context)
    if not normalized:
        return None
    for index, line in enumerate(lines):
        if _normalize_text(line) == normalized:
            return index
    return None


def _find_raw_context_line_after(
    lines: list[str], context: str, after_index: int
) -> int | None:
    normalized = _normalize_text(context)
    if not normalized:
        return None
    for index in range(max(0, after_index + 1), len(lines)):
        if _normalize_text(lines[index]) == normalized:
            return index
    return None


def _coalesce_source_block_segments(segments: list[Segment]) -> list[Segment]:
    result: list[Segment] = []
    indexes: dict[tuple[int, ...], int] = {}

    for segment in segments:
        key = segment.new_linenos if segment.new_source else ()
        if not key or key not in indexes:
            if key:
                indexes[key] = len(result)
            result.append(segment)
            continue

        index = indexes[key]
        current = result[index]
        result[index] = Segment(
            old_lines=(
                current.old_lines
                if _meaningful_lines(current.old_lines)
                else segment.old_lines
            ),
            new_lines=current.new_lines,
            before_context=current.before_context,
            after_context=segment.after_context or current.after_context,
            old_linenos=current.old_linenos + segment.old_linenos,
            new_linenos=current.new_linenos,
            new_source=current.new_source,
        )

    return result


def _block_for_text(
    source_blocks: list[SourceBlock], text: str | None
) -> SourceBlock | None:
    normalized = _normalize_text(text or "")
    if not normalized:
        return None
    matches = [block for block in source_blocks if normalized in block.comment]
    return matches[0] if len(matches) == 1 else None


def _source_blocks(source: str) -> list[SourceBlock]:
    blocks: list[SourceBlock] = []
    paragraph: list[tuple[int, str]] = []
    in_code = False
    fence = ""
    in_front_matter = False

    def flush_paragraph() -> None:
        if not paragraph:
            return
        comment = _normalize_text(" ".join(line.strip() for _lineno, line in paragraph))
        text = "\n".join(line for _lineno, line in paragraph) + "\n"
        blocks.append(SourceBlock(paragraph[0][0], paragraph[-1][0], comment, text))
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
        if is_named_anchor_line(line):
            flush_paragraph()
            continue
        if is_heading_line(line):
            flush_paragraph()
            heading = strip_title_attr_line(line).strip()
            blocks.append(SourceBlock(lineno, lineno, _normalize_text(heading), line + "\n"))
            continue
        if stripped.startswith(("- [", "* [")) and "](#" in stripped:
            flush_paragraph()
            continue
        if stripped.startswith(("<!--", ">", "|")):
            flush_paragraph()
            continue
        paragraph.append((lineno, line))

    flush_paragraph()
    return blocks
