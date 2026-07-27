"""Strict structural contract for newly generated provider responses.

The final document verifier accepts historical translation shapes. This module
is deliberately narrower: it validates a fresh provider response before that
response is patched into a document.
"""
from __future__ import annotations

import re
from bisect import bisect_right
from collections import Counter

from ..annotation.annotate import Block, split_blocks
from ..common.javascript import (
    balanced_expression_end,
    top_level_plus_positions,
)
from ..common.markdown import (
    closes_fence,
    fence_token,
    front_matter_description,
    has_malformed_html_comment_delimiters,
    html_code_contents,
    html_comment_spans,
    inline_code_contents,
    is_heading_line,
    is_named_anchor_line,
    is_non_annotatable_line,
    is_ordered_list_marker,
    is_reference_definition_block,
    is_reference_definition_line,
    is_structural_html_fragment,
    is_structural_html_line,
    mask_fenced_code_contents,
    markdown_links,
    mask_reference_definitions,
    normalize_annotation_anchor,
    reference_definitions,
    reference_definition_line_numbers,
    reference_link_signatures,
    standalone_html_comment_line_numbers,
    strip_html_comments,
    strip_html_code_elements,
    strip_inline_code,
    strip_markdown_links,
)
from ..postprocessing.postprocess import admonition_types

_UNORDERED_LIST_RE = re.compile(r"^([ \t]*)([-*+])[ \t]+(\S.*)$")
_ORDERED_LIST_RE = re.compile(r"^([ \t]*)(\d+)([.)])[ \t]+(\S.*)$")
_EMPTY_QUOTE_RE = re.compile(r"^[ \t]*(?:>[ \t]*)+$")
_ASCII_WORD_RE = re.compile(r"[A-Za-z]{2,}")
_TASK_CHECKBOX_RE = re.compile(r"^\[([ xX])](?:[ \t]+|$)")
_ADMONITION_MARKER_RE = re.compile(
    r"^\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT)](?:[ \t]+|$)", re.IGNORECASE
)
_TARGET_SCRIPT = {
    "ko": re.compile(r"[가-힣]"),
    "ja": re.compile(r"[ぁ-ゖァ-ヺ㐀-鿿]"),
}
_JAPANESE_KANA_RE = re.compile(r"[ぁ-ゖァ-ヺ]")
_OTHER_TARGET_SCRIPT = {
    "ko": re.compile(r"[ぁ-ゖァ-ヺ\u3400-\u9fff]"),
    "ja": re.compile(r"[가-힣]"),
}
_DISPLAY_ATTRIBUTES = frozenset(
    ("alt", "placeholder", "aria-label", "aria-description")
)
_AUTOLINK_RE = re.compile(r"<https?://[^>]+>", re.IGNORECASE)
_URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
_SENTENCE_END_RE = re.compile(
    r"""[.!?。！？]+(?:["'’”)\]}]+)?(?=\s|$)"""
)
_SOURCE_CLAUSE_SPLIT_RE = re.compile(
    r"[,;:—–]|\s-\s"
    r"|\b(?:and|but|or|nor|yet|so|then|while|whereas|because|although|"
    r"though|which|that|without)\b",
    re.IGNORECASE,
)
_TAG_RE = re.compile(r"</?[A-Za-z][^>]*>")
_HTML_ENTITY_RE = re.compile(r"&(?:#[xX]?[0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]+);")
_LEGAL_TEXT_MARKERS = (
    "the mit license",
    "copyright (c)",
    "permission is hereby granted",
    "the above copyright notice",
    'the software is provided "as is"',
)
_LOWERCASE_TECH_TERMS = frozenset(("npm", "php", "macos"))
_PRODUCT_NAME_PREFIXES = frozenset(("laravel",))
_PROSE_SIGNAL_WORDS = frozenset(
    (
        "all",
        "and",
        "are",
        "be",
        "been",
        "being",
        "delete",
        "deleted",
        "deletes",
        "handling",
        "is",
        "prevent",
        "prevents",
        "retried",
        "retries",
        "retry",
        "this",
        "was",
        "were",
        "works",
        "write",
        "writes",
    )
)
_VERSION_VALUE_RE = re.compile(
    r"^(?:core\s*,?\s*)?"
    r"[v^~<>=]*\d+(?:\.[0-9x*]+)*(?:\+)?(?:\s+[A-Za-z][\w-]*)?"
    r"(?:\s*(?:[-–,/]|\bor\b)\s*"
    r"[v^~<>=]*\d+(?:\.[0-9x*]+)*(?:\+)?"
    r"(?:\s+[A-Za-z][\w-]*)?)*$",
    re.IGNORECASE,
)
_DATE_VALUE_RE = re.compile(
    r"^(?:January|February|March|April|May|June|July|August|"
    r"September|October|November|December)\s+"
    r"\d{1,2}(?:st|nd|rd|th)?,\s+\d{4}$",
    re.IGNORECASE,
)
_CONFIG_VALUE_RE = re.compile(
    r"^\([A-Za-z_][\w-]*\)\s+"
    r"(?:true|false|null|''|\"\"|'[^']*'|\"[^\"]*\"|"
    r"-?\d+(?:\.\d+)?|\[\]|\{\})$",
    re.IGNORECASE,
)
_ENV_ASSIGNMENT_RE = re.compile(r"^[A-Z][A-Z0-9_]*=\S+$")
_PARENTHESIZED_LITERAL_RE = re.compile(
    r"^\((?:true|false|empty|null)\)$", re.IGNORECASE
)
_TYPE_VALUE_RE = re.compile(
    r"^\??[A-Za-z_][\w.\\-]*(?:<[^<>\s]+>)?(?:\[\])?"
    r"(?:\|\??[A-Za-z_][\w.\\-]*(?:<[^<>\s]+>)?(?:\[\])?)*$"
)
_SCALAR_TOKEN_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.+#:-]*$")
_SCALAR_LIST_RE = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_.+#:-]*"
    r"(?:\s*[,/]\s*[A-Za-z_][A-Za-z0-9_.+#:-]*)+$"
)
_RAW_HTML_TEXT_TAGS = frozenset(
    (
        "article",
        "blockquote",
        "dd",
        "details",
        "div",
        "dl",
        "dt",
        "figcaption",
        "figure",
        "footer",
        "header",
        "li",
        "main",
        "nav",
        "ol",
        "p",
        "section",
        "summary",
        "table",
        "tbody",
        "td",
        "tfoot",
        "th",
        "thead",
        "tr",
        "ul",
    )
)
_OPENING_TAG_NAME_RE = re.compile(r"<([A-Za-z][\w:.-]*)\b")
_IDENTIFIER_HEADER_TERMS = frozenset(
    (
        "action",
        "command",
        "default",
        "event",
        "key",
        "method",
        "option",
        "parameter",
        "route",
        "skill",
        "type",
        "value",
        "version",
    )
)
_IDENTIFIER_LIST_HEADER_TERMS = frozenset(
    ("default", "option", "type", "value", "version")
)
_PRODUCT_HEADER_TERMS = frozenset(
    (
        "backend",
        "class",
        "database",
        "driver",
        "facade",
        "feature",
        "framework",
        "implementation",
        "library",
        "package",
        "product",
        "provider",
        "service",
        "tool",
    )
)
_PROTECTED_CELL_TOKEN_RE = re.compile(
    r"[A-Za-z_][A-Za-z0-9_.+#:-]*|\d+(?:\.[0-9A-Za-z*]+)*"
)
_ONE_LINE_COMMENT_RE = re.compile(
    r"^([ \t]*(?:>[ \t]*)*)<!--[ \t]*(.*?)[ \t]*-->[ \t]*$"
)


def _strip_code_blocks(text: str) -> str:
    out: list[str] = []
    in_code = False
    fence = ""
    for line in text.splitlines(keepends=True):
        token = fence_token(line)
        if token:
            if not in_code:
                in_code = True
                fence = token
                continue
            if closes_fence(line, fence):
                in_code = False
                continue
        if not in_code:
            out.append(line)
    return "".join(out)


def _normalized_fenced_code_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    fence = ""
    for line in text.splitlines(keepends=True):
        token = fence_token(line)
        if token and not fence:
            fence = token
            current = [line]
            continue
        if not fence:
            continue
        current.append(line)
        if closes_fence(line, fence):
            blocks.append(
                "\n".join(
                    item.rstrip(" \t")
                    for item in "".join(current).rstrip("\n").split("\n")
                )
            )
            current = []
            fence = ""
    if fence:
        blocks.append(
            "\n".join(
                item.rstrip(" \t")
                for item in "".join(current).rstrip("\n").split("\n")
            )
        )
    return blocks


def _normalize_comment(text: str) -> str:
    return normalize_annotation_anchor(text)


def _required_comments(source: str) -> list[str]:
    body = _strip_code_blocks(source)
    source_comment_lines = standalone_html_comment_line_numbers(body)
    reference_lines = reference_definition_line_numbers(body)
    comments: list[str] = []
    paragraph: list[str] = []
    paragraph_kind: str | None = None
    in_front_matter = False

    def flush() -> None:
        nonlocal paragraph_kind
        if paragraph:
            if not is_structural_html_fragment("\n".join(paragraph)):
                comments.append(_normalize_comment(" ".join(paragraph)))
            paragraph.clear()
        paragraph_kind = None

    def append_paragraph(kind: str, text: str) -> None:
        nonlocal paragraph_kind
        if paragraph_kind not in (None, kind):
            flush()
        paragraph_kind = kind
        paragraph.append(text)

    for index, line in enumerate(body.splitlines()):
        stripped = line.strip()
        if index == 0 and stripped == "---":
            in_front_matter = True
            continue
        if in_front_matter and stripped == "---":
            in_front_matter = False
            continue
        if in_front_matter:
            continue
        if index + 1 in source_comment_lines:
            flush()
            continue
        if index in reference_lines:
            flush()
            continue
        if not stripped:
            flush()
            continue
        if stripped.startswith("#"):
            flush()
            comments.append(_normalize_comment(stripped))
            continue
        if stripped.startswith(">"):
            flush()
            continue
        if is_structural_html_line(line) or is_non_annotatable_line(line):
            flush()
            continue
        marker = _UNORDERED_LIST_RE.match(stripped) or _ORDERED_LIST_RE.match(stripped)
        if marker:
            item_body = marker.group(marker.lastindex or 0)
            checkbox = _TASK_CHECKBOX_RE.match(item_body)
            if checkbox:
                item_body = item_body[checkbox.end() :]
            if _is_inline_code_only_list_item(item_body):
                flush()
                continue
        append_paragraph("paragraph", stripped)

    flush()
    return [comment for comment in comments if comment]


def _optional_quoted_comments(
    source: str,
) -> Counter[tuple[str, int, int]]:
    comments: Counter[tuple[str, int, int]] = Counter()
    quote_block = 0
    for block in _blocks(source):
        if _text_kind(block.lines[0]) != "quote":
            continue
        block_ordinal = quote_block
        quote_block += 1
        if block.kind != "text":
            continue
        bodies: list[str] = []
        for line in block.lines:
            content = line.lstrip()
            while content.startswith(">"):
                content = content[1:].lstrip()
            if not content or _ADMONITION_MARKER_RE.match(content):
                continue
            bodies.append(content)
        normalized = _normalize_comment(" ".join(bodies))
        if normalized:
            comments[
                (normalized, _quote_depth(block.lines[0]), block_ordinal)
            ] += 1
    return comments


def _quote_block_ordinal(lines: list[str], line_index: int) -> int:
    ordinal = -1
    in_quote = False
    for line in lines[: line_index + 1]:
        if _ONE_LINE_COMMENT_RE.fullmatch(line):
            continue
        quote = line.lstrip().startswith(">")
        if quote and not in_quote:
            ordinal += 1
        in_quote = quote
    return ordinal


def _optional_quote_annotation_starts_block(
    lines: list[str], line_index: int
) -> bool:
    cursor = line_index - 1
    while cursor >= 0 and lines[cursor].lstrip().startswith(">"):
        if _ONE_LINE_COMMENT_RE.fullmatch(lines[cursor]):
            cursor -= 1
            continue
        content = lines[cursor].lstrip()
        while content.startswith(">"):
            content = content[1:].lstrip()
        if content and not _ADMONITION_MARKER_RE.match(content):
            return False
        cursor -= 1
    return True


def _annotation_comments(text: str, source: str) -> list[str]:
    _preserved, source_comment_indexes = _matched_source_comment_indexes(
        text, source
    )
    optional_quoted_annotations = _optional_quoted_comments(source)
    annotations: list[str] = []
    lines = text.splitlines()
    for index, (body, start_line, end_line, _position) in enumerate(
        _comment_records(text)
    ):
        if index in source_comment_indexes:
            continue
        normalized = _normalize_comment(body)
        if not normalized:
            continue
        if (
            not is_non_annotatable_line(normalized)
            and not is_structural_html_fragment(normalized)
        ):
            match = (
                _ONE_LINE_COMMENT_RE.fullmatch(lines[start_line])
                if start_line == end_line
                else None
            )
            depth = _quote_depth(match.group(1)) if match else 0
            optional_key = (
                normalized,
                depth,
                _quote_block_ordinal(lines, start_line + 1),
            )
            if (
                match
                and depth > 0
                and _optional_quote_annotation_starts_block(
                    lines, start_line
                )
                and optional_quoted_annotations[optional_key]
            ):
                optional_quoted_annotations[optional_key] -= 1
            else:
                annotations.append(normalized)
    return annotations


def _text_kind(line: str) -> str:
    stripped = line.lstrip()
    if stripped.startswith("|"):
        return "table"
    if stripped.startswith(">"):
        return "quote"
    if (
        stripped.startswith(("- ", "* ", "+ "))
        or is_ordered_list_marker(stripped)
        or _ORDERED_LIST_RE.match(stripped)
    ):
        return "list"
    if stripped.startswith("@"):
        return "directive"
    if stripped.startswith("<"):
        if is_structural_html_fragment(stripped):
            return "html"
        tag = _OPENING_TAG_NAME_RE.match(stripped)
        if tag and (
            tag.group(1).lower() in _RAW_HTML_TEXT_TAGS
            or tag.group(1)[:1].isupper()
        ):
            return "html"
    return "paragraph"


def _has_markdown_hard_break(line: str) -> bool:
    trailing_backslashes = len(line) - len(line.rstrip("\\"))
    return line.endswith("  ") or trailing_backslashes % 2 == 1


def _signature(block: Block) -> tuple[object, ...]:
    if block.kind == "heading":
        stripped = block.lines[0].lstrip()
        return ("heading", len(stripped) - len(stripped.lstrip("#")))
    if block.kind != "text":
        return (block.kind,)

    kind = _text_kind(block.lines[0])
    if kind == "list":
        markers: list[str] = []
        for line in block.lines:
            unordered = _UNORDERED_LIST_RE.match(line)
            ordered = _ORDERED_LIST_RE.match(line)
            if unordered:
                checkbox = _TASK_CHECKBOX_RE.match(unordered.group(3))
                state = checkbox.group(1).lower() if checkbox else ""
                markers.append(
                    f"{unordered.group(1)}{unordered.group(2)}[{state}]"
                )
            elif ordered:
                markers.append(
                    f"{ordered.group(1)}{ordered.group(2)}{ordered.group(3)}"
                )
        return ("text", kind, tuple(markers))
    if kind == "quote":
        depths = tuple(
            (_quote_depth(line), _has_markdown_hard_break(line))
            for line in block.lines
        )
        return ("text", kind, depths)
    if kind == "table":
        return ("text", kind, tuple(_table_line_signature(line) for line in block.lines))
    if kind == "html":
        return ("text", kind, len(block.lines))
    return ("text", kind)


def _quote_depth(line: str) -> int:
    stripped = line.lstrip()
    depth = 0
    while stripped.startswith(">"):
        depth += 1
        stripped = stripped[1:].lstrip()
    return depth


def _table_line_signature(line: str) -> tuple[object, ...]:
    cells = _table_cells(line)
    if cells and all(re.fullmatch(r":?-+:?", cell) for cell in cells):
        return (
            "separator",
            tuple((cell.startswith(":"), cell.endswith(":")) for cell in cells),
        )
    return ("row", len(cells))


def _table_cells(line: str) -> list[str]:
    """Split a table row without treating escaped or inline-markup pipes as cells."""

    body = line.strip()
    links = {link.start: link for link in markdown_links(body)}
    cells: list[str] = []
    current: list[str] = []
    index = 0
    while index < len(body):
        link = links.get(index)
        if link is not None:
            current.append(body[link.start : link.end])
            index = link.end
            continue
        if body[index] == "\\" and index + 1 < len(body):
            current.append(body[index : index + 2])
            index += 2
            continue
        if body[index] == "`":
            end = index + 1
            while end < len(body) and body[end] == "`":
                end += 1
            fence = body[index:end]
            closing = body.find(fence, end)
            if closing >= 0:
                closing += len(fence)
                current.append(body[index:closing])
                index = closing
                continue
        if body[index] == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(body[index])
        index += 1
    cells.append("".join(current).strip())
    if cells and not cells[0]:
        cells.pop(0)
    if cells and not cells[-1]:
        cells.pop()
    return cells


def _blocks(text: str) -> list[Block]:
    lines = [
        line
        for line in strip_html_comments(text).splitlines()
        if not _EMPTY_QUOTE_RE.fullmatch(line)
    ]
    return split_blocks(lines)


def _markdown_structure_signature(text: str) -> list[tuple[object, ...]]:
    body = strip_html_comments(_strip_code_blocks(text))
    signature: list[tuple[object, ...]] = []
    in_front_matter = False

    for index, line in enumerate(body.splitlines()):
        stripped = line.strip()
        if index == 0 and stripped == "---":
            in_front_matter = True
            continue
        if in_front_matter:
            if stripped == "---":
                in_front_matter = False
            continue
        if not stripped or _EMPTY_QUOTE_RE.fullmatch(line):
            continue

        unordered = _UNORDERED_LIST_RE.match(line)
        ordered = _ORDERED_LIST_RE.match(line)
        if unordered or ordered:
            if unordered:
                indent, marker, remainder = unordered.groups()
                checkbox = _TASK_CHECKBOX_RE.match(remainder)
                list_marker = (marker, checkbox.group(1).lower() if checkbox else "")
            else:
                assert ordered is not None
                indent, number, delimiter, remainder = ordered.groups()
                list_marker = (f"{number}{delimiter}", "")
            signature.append(
                (
                    "list",
                    indent,
                    list_marker,
                    _quote_depth(remainder),
                )
            )
            continue

        if line.lstrip().startswith(">"):
            quote = line.lstrip()
            depth = _quote_depth(quote)
            content = quote
            for _ in range(depth):
                content = content[1:].lstrip()
            marker = _ADMONITION_MARKER_RE.match(content)
            signature.append(
                (
                    "quote",
                    line[: len(line) - len(line.lstrip())],
                    depth,
                    marker.group(1).upper() if marker else "",
                    _has_markdown_hard_break(line),
                )
            )
            continue

        if line.lstrip().startswith("|"):
            signature.append(("table", *_table_line_signature(line)))

    return signature


def _normalized_body(block: Block) -> str:
    lines: list[str] = []
    for line in block.lines:
        stripped = line.strip()
        stripped = re.sub(
            r"^(?:[-*+]\s+|\d+[.)]\s+|>+\s*|\|\s*)", "", stripped
        )
        lines.append(stripped)
    return " ".join(" ".join(lines).split())


def _is_indented_literal_block(block: Block) -> bool:
    return bool(block.lines) and all(
        line.startswith("\t") or len(line) - len(line.lstrip(" ")) >= 4
        for line in block.lines
    )


def _is_legacy_pipe_table_block(block: Block) -> bool:
    return _is_legacy_pipe_table_text("\n".join(block.lines))


def _is_legacy_pipe_table_text(text: str) -> bool:
    lines = text.splitlines()
    return (
        len(lines) >= 2
        and all("|" in line for line in lines)
        and any(
            re.fullmatch(
                r"\s*:?-{3,}:?(?:\s*\|\s*:?-{3,}:?)+\s*",
                line,
            )
            for line in lines
        )
    )


def _is_toc_link_list(block: Block) -> bool:
    return bool(block.lines) and all(
        line.strip().startswith(("- [", "* [")) and "](#" in line
        for line in block.lines
    )


def _front_matter_signature(blocks: list[Block]) -> list[tuple[str, ...]]:
    signatures: list[tuple[str, ...]] = []
    for block in blocks:
        if block.kind != "frontmatter":
            continue
        description = front_matter_description("\n".join(block.lines))
        lines: list[str] = []
        description_block = False
        description_content = False

        def flush_description() -> None:
            nonlocal description_block, description_content
            if description_block:
                lines.append(
                    "description-content: present"
                    if description_content
                    else "description-content: empty"
                )
            description_block = False
            description_content = False

        for line in block.lines:
            key = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*", line)
            if key:
                flush_description()
                if key.group(1) != "description":
                    lines.append(line.rstrip())
                    continue

                if description is None or not description.valid:
                    lines.append("description: invalid")
                    continue
                state = "present" if description.value else "empty"
                lines.append(
                    f"description: {description.style}:{state}:"
                    f"{description.comment}"
                )
                if description.style.startswith("block:"):
                    description_block = True
                continue
            if description_block and line[:1].isspace():
                description_content = description_content or bool(line.strip())
                continue
            flush_description()
            lines.append(line.rstrip())
        flush_description()
        signatures.append(tuple(lines))
    return signatures


def _front_matter_description(text: str) -> str | None:
    description = front_matter_description(text)
    if description is None or not description.valid:
        return None
    return description.value


def _front_matter_language_is_valid(
    text: str, source: str, locale: str
) -> bool:
    source_description = _front_matter_description(source)
    if source_description is None:
        return True
    translated_description = _front_matter_description(text) or ""
    source_word_count = len(_ASCII_WORD_RE.findall(source_description))
    if source_word_count < 2:
        return True
    return _has_target_language(
        translated_description,
        locale,
        source_word_count,
    )


def _comment_positions(
    text: str,
) -> list[tuple[str, int, str, int, int, bool, bool, int]]:
    masked = mask_fenced_code_contents(text)
    positions: list[
        tuple[str, int, str, int, int, bool, bool, int]
    ] = []
    for start, end, body in html_comment_spans(masked):
        line_start = masked.rfind("\n", 0, start) + 1
        line_end = masked.find("\n", end)
        if line_end < 0:
            line_end = len(masked)
        prefix = masked[line_start:start]
        suffix = masked[end:line_end]
        standalone = bool(
            re.fullmatch(r"[ \t]*(?:>[ \t]*)*", prefix)
            and not suffix.strip()
        )
        prefix_blocks = _blocks(masked[:start])
        physical_line = (
            max(0, len(prefix_blocks[-1].lines) - 1)
            if not standalone and prefix_blocks
            else 0
        )
        positions.append(
            (
                body,
                len(prefix_blocks),
                "standalone" if standalone else "inline",
                _quote_depth(prefix) if standalone else 0,
                len(prefix) - len(prefix.lstrip(" \t"))
                if standalone
                else 0,
                bool(prefix.strip()) if not standalone else False,
                bool(suffix.strip()) if not standalone else False,
                physical_line,
            )
        )
    return positions


def _comment_records(text: str) -> list[tuple[str, int, int, int]]:
    line_starts = [0]
    line_starts.extend(
        match.end() for match in re.finditer(r"\n", text)
    )
    fenced_lines: set[int] = set()
    in_code = False
    fence = ""
    for line_index, line in enumerate(text.splitlines(keepends=True)):
        token = fence_token(line)
        if token:
            if not in_code:
                in_code = True
                fence = token
                fenced_lines.add(line_index)
                continue
            if closes_fence(line, fence):
                fenced_lines.add(line_index)
                in_code = False
                fence = ""
                continue
        if in_code:
            fenced_lines.add(line_index)

    positions = _comment_positions(text)
    records: list[tuple[str, int, int, int]] = []
    position_index = 0
    for start, end, body in html_comment_spans(text):
        start_line = bisect_right(line_starts, start) - 1
        if start_line in fenced_lines:
            continue
        end_line = bisect_right(line_starts, end - 1) - 1
        if position_index >= len(positions):
            break
        records.append(
            (body, start_line, end_line, positions[position_index][1])
        )
        position_index += 1
    return records


def _matched_source_comment_indexes(
    text: str, source: str
) -> tuple[bool, set[int]]:
    expected = _comment_positions(source)
    actual = _comment_positions(text)
    matched: set[int] = set()
    cursor = 0
    for source_comment in expected:
        while cursor < len(actual) and actual[cursor] != source_comment:
            cursor += 1
        if cursor == len(actual):
            return False, matched
        matched.add(cursor)
        cursor += 1
    return True, matched


def _structural_annotation_owns_next_line(
    annotation: str,
    end_line: int,
    lines: list[str],
    *,
    expected_quote_ordinal: int | None = None,
    expected_table_ordinal: int | None = None,
) -> bool:
    next_line_index = end_line + 1
    if next_line_index >= len(lines):
        return False
    next_line = lines[next_line_index]
    if not next_line.strip():
        return False
    if _normalize_comment(next_line) == annotation:
        return True

    if annotation.lstrip().startswith(">"):
        actual_quote_ordinal = sum(
            1
            for line in lines[: next_line_index + 1]
            if line.lstrip().startswith(">")
            and not _ONE_LINE_COMMENT_RE.fullmatch(line)
        ) - 1
        return (
            _quote_depth(annotation) > 0
            and _quote_depth(next_line) == _quote_depth(annotation)
            and actual_quote_ordinal == expected_quote_ordinal
        )
    if annotation.lstrip().startswith("|"):
        visible_lines = strip_html_comments(
            "\n".join(lines[: next_line_index + 1])
        ).splitlines()
        actual_table_ordinal = sum(
            1 for line in visible_lines if line.lstrip().startswith("|")
        ) - 1
        return (
            next_line.lstrip().startswith("|")
            and _table_line_signature(next_line)
            == _table_line_signature(annotation)
            and actual_table_ordinal == expected_table_ordinal
        )

    source_toc = _UNORDERED_LIST_RE.match(annotation)
    translated_toc = _UNORDERED_LIST_RE.match(next_line)
    if source_toc and translated_toc and "](#" in annotation:
        return (
            source_toc.group(2) == translated_toc.group(2)
            and [link.target for link in markdown_links(annotation)]
            == [link.target for link in markdown_links(next_line)]
        )

    if is_structural_html_fragment(annotation):
        expected = tuple(
            re.sub(r"\s+/>$", "/>", token)
            for token in _html_markup_signature(annotation)
        )
        actual_lines: list[str] = []
        for line in lines[next_line_index:]:
            if not is_structural_html_fragment(line):
                break
            actual_lines.append(line)
            actual = tuple(
                re.sub(r"\s+/>$", "/>", token)
                for token in _html_markup_signature(
                    "\n".join(actual_lines)
                )
            )
            if len(actual) >= len(expected):
                return actual == expected
        return False

    return _normalize_comment(next_line) == annotation


def _source_comments_are_preserved(text: str, source: str) -> bool:
    preserved, source_comment_indexes = _matched_source_comment_indexes(
        text, source
    )
    if not preserved:
        return False

    structural_annotations = Counter(
        normalized
        for line in strip_html_comments(_strip_code_blocks(source)).splitlines()
        if (normalized := _normalize_comment(line))
    )
    quote_ordinals: dict[str, list[int]] = {}
    quote_ordinal = 0
    table_ordinals: dict[str, list[int]] = {}
    table_ordinal = 0
    for line in _strip_code_blocks(source).splitlines():
        if _ONE_LINE_COMMENT_RE.fullmatch(line):
            continue
        normalized = _normalize_comment(line)
        if line.lstrip().startswith(">"):
            quote_ordinals.setdefault(normalized, []).append(quote_ordinal)
            quote_ordinal += 1
        elif line.lstrip().startswith("|"):
            table_ordinals.setdefault(normalized, []).append(table_ordinal)
            table_ordinal += 1
    consumed_quote_ordinals: Counter[str] = Counter()
    consumed_table_ordinals: Counter[str] = Counter()
    lines = text.splitlines()
    for index, (body, _start_line, end_line, _position) in enumerate(
        _comment_records(text)
    ):
        if index in source_comment_indexes:
            continue
        normalized = _normalize_comment(body)
        if not normalized:
            return False
        if (
            is_non_annotatable_line(normalized)
            or is_structural_html_fragment(normalized)
        ):
            if structural_annotations[normalized]:
                structural_annotations[normalized] -= 1
                expected_quote_ordinal = None
                expected_table_ordinal = None
                if normalized.lstrip().startswith(">"):
                    occurrence = consumed_quote_ordinals[normalized]
                    expected_quote_ordinal = quote_ordinals[normalized][
                        occurrence
                    ]
                    consumed_quote_ordinals[normalized] += 1
                elif normalized.lstrip().startswith("|"):
                    occurrence = consumed_table_ordinals[normalized]
                    expected_table_ordinal = table_ordinals[normalized][
                        occurrence
                    ]
                    consumed_table_ordinals[normalized] += 1
                if _structural_annotation_owns_next_line(
                    normalized,
                    end_line,
                    lines,
                    expected_quote_ordinal=expected_quote_ordinal,
                    expected_table_ordinal=expected_table_ordinal,
                ):
                    continue
            return False
    return True


def _is_legal_source_text(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in _LEGAL_TEXT_MARKERS)


def _list_layout(block: Block) -> tuple[int, int]:
    hard_breaks = 0
    continuations = 0
    for line in block.lines:
        if _UNORDERED_LIST_RE.match(line) or _ORDERED_LIST_RE.match(line):
            hard_breaks += _has_markdown_hard_break(line)
            continue
        stripped = line.lstrip()
        if (
            stripped.startswith((">", "|"))
            or is_structural_html_fragment(stripped)
        ):
            continue
        continuations += 1
        hard_breaks += _has_markdown_hard_break(line)
    return hard_breaks, continuations


def _paragraph_layout_is_valid(
    source_blocks: list[Block],
    translated_blocks: list[Block],
    *,
    allow_source_echo: bool,
) -> bool:
    for source_block, translated_block in zip(
        source_blocks, translated_blocks, strict=False
    ):
        if source_block.kind != "text" or translated_block.kind != "text":
            continue
        if is_reference_definition_block(
            "\n".join(source_block.lines)
        ):
            continue
        source_kind = _text_kind(source_block.lines[0])
        translated_kind = _text_kind(translated_block.lines[0])
        if _is_legacy_pipe_table_block(source_block) and (
            _is_legacy_pipe_table_block(translated_block)
        ):
            continue
        if source_kind == "list" and translated_kind == "list":
            source_hard_breaks, _source_continuations = _list_layout(source_block)
            translated_hard_breaks, translated_continuations = _list_layout(
                translated_block
            )
            if (
                translated_hard_breaks != source_hard_breaks
                or translated_continuations != source_hard_breaks
            ):
                return False
            continue
        if source_kind == "html" or translated_kind == "html":
            if (
                source_kind != translated_kind
                or len(source_block.lines) != len(translated_block.lines)
            ):
                return False
            continue
        if source_kind != "paragraph" or translated_kind != "paragraph":
            continue

        source_body = _normalized_body(source_block)
        if allow_source_echo and _is_legal_source_text(source_body):
            continue

        source_hard_breaks = sum(
            _has_markdown_hard_break(line) for line in source_block.lines[:-1]
        )
        translated_hard_breaks = sum(
            _has_markdown_hard_break(line) for line in translated_block.lines[:-1]
        )
        if (
            len(translated_block.lines) != source_hard_breaks + 1
            or translated_hard_breaks != source_hard_breaks
        ):
            return False
    return True


def _sentence_count(text: str) -> int:
    sample = strip_html_code_elements(strip_inline_code(text))
    sample = _URL_RE.sub("", sample)
    sample = re.sub(r"\b(?:\d+\.)+\d+\b", "", sample)
    if not any(char.isalnum() for char in sample):
        return 0
    endings = list(_SENTENCE_END_RE.finditer(sample))
    if not endings:
        return 1
    return len(endings) + int(
        any(char.isalnum() for char in sample[endings[-1].end() :])
    )


def _sentence_cardinality_pair_is_valid(
    source_body: str,
    translated_body: str,
) -> bool:
    source_capacity = _sentence_count(source_body) + len(
        _SOURCE_CLAUSE_SPLIT_RE.findall(source_body)
    )
    return _sentence_count(translated_body) <= source_capacity


def _paragraph_sentence_cardinality_is_valid(
    source: str,
    translated: str,
) -> bool:
    for source_block, translated_block in zip(
        _blocks(source), _blocks(translated), strict=False
    ):
        if source_block.kind != "text" or translated_block.kind != "text":
            continue
        if (
            _text_kind(source_block.lines[0]) != "paragraph"
            or _text_kind(translated_block.lines[0]) != "paragraph"
            or _is_legacy_pipe_table_block(source_block)
            or _is_legacy_pipe_table_block(translated_block)
        ):
            continue
        source_body = _normalized_body(source_block)
        translated_body = _normalized_body(translated_block)
        if not _sentence_cardinality_pair_is_valid(
            source_body,
            translated_body,
        ):
            return False
    return True


def _paragraph_indentation_is_valid(
    source_blocks: list[Block], translated_blocks: list[Block]
) -> bool:
    def indented_as_code(line: str) -> bool:
        return line.startswith("\t") or len(line) - len(line.lstrip(" ")) >= 4

    for source_block, translated_block in zip(
        source_blocks, translated_blocks, strict=False
    ):
        if source_block.kind != "text" or translated_block.kind != "text":
            continue
        if is_reference_definition_block(
            "\n".join(source_block.lines)
        ):
            continue
        if _text_kind(source_block.lines[0]) != "paragraph":
            continue
        if not any(indented_as_code(line) for line in source_block.lines) and any(
            indented_as_code(line) for line in translated_block.lines
        ):
            return False
    return True


def _html_markup_signature(text: str) -> list[str]:
    body = strip_html_comments(_strip_code_blocks(text))
    return [_mask_display_attribute_values(tag) for tag in _markup_tokens(body)]


def _is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def _quoted_value_end(text: str, start: int) -> int:
    quote = text[start]
    cursor = start + 1
    while cursor < len(text):
        if text[cursor] == quote and not _is_escaped(text, cursor):
            return cursor + 1
        cursor += 1
    return len(text)


def _braced_value_end(text: str, start: int) -> int:
    return balanced_expression_end(text, start) or len(text)


def _tag_attribute_value_spans(
    tag: str,
) -> tuple[tuple[str, int, int], ...]:
    name = re.match(r"</?[A-Za-z][\w:.-]*", tag)
    if not name or tag.startswith("</"):
        return ()

    spans: list[tuple[str, int, int]] = []
    index = name.end()
    while index < len(tag):
        if tag.startswith("/>", index) or tag[index] == ">":
            break
        if tag[index].isspace():
            index += 1
            continue
        if tag[index] == "{":
            index = _braced_value_end(tag, index)
            continue

        attribute = re.match(r"[A-Za-z_:][\w:.-]*", tag[index:])
        if not attribute:
            index += 1
            continue
        attribute_name = attribute.group(0)
        index += attribute.end()
        while index < len(tag) and tag[index].isspace():
            index += 1
        if index >= len(tag) or tag[index] != "=":
            continue
        index += 1
        while index < len(tag) and tag[index].isspace():
            index += 1
        if index >= len(tag):
            break

        value_start = index
        if tag[index] in ("'", '"', "`"):
            value_end = _quoted_value_end(tag, index)
        elif tag[index] == "{":
            value_end = _braced_value_end(tag, index)
        else:
            value_end = index
            while value_end < len(tag) and not tag[value_end].isspace() and tag[value_end] != ">":
                value_end += 1
        spans.append((attribute_name, value_start, value_end))
        index = value_end
    return tuple(spans)


def _pure_braced_display_string(value: str) -> bool:
    if not (value.startswith("{") and value.endswith("}")):
        return False
    inner = value[1:-1].strip()
    if len(inner) < 2 or inner[0] not in ("'", '"', "`"):
        return False
    if inner[0] == "`" and "${" in inner:
        return False
    return _quoted_value_end(inner, 0) == len(inner)


def _mask_js_expression_strings(expression: str) -> str:
    pluses = top_level_plus_positions(expression)
    if not pluses:
        return expression

    boundaries = [-1, *pluses, len(expression)]
    segments = [
        expression[start + 1 : end]
        for start, end in zip(boundaries, boundaries[1:], strict=False)
    ]
    if any(not segment.strip() for segment in segments):
        return expression

    def mask_literal(segment: str) -> str:
        leading = len(segment) - len(segment.lstrip())
        trailing = len(segment) - len(segment.rstrip())
        end = len(segment) - trailing if trailing else len(segment)
        token = segment[leading:end]
        if (
            len(token) >= 2
            and token[0] in ("'", '"', "`")
            and _quoted_value_end(token, 0) == len(token)
            and (token[0] != "`" or "${" not in token)
        ):
            return segment[:leading] + token[0] * 2 + segment[end:]
        return segment

    out: list[str] = []
    for segment, plus in zip(segments, pluses, strict=False):
        out.extend((mask_literal(segment), expression[plus]))
    out.append(mask_literal(segments[-1]))
    return "".join(out)


def _masked_display_attribute_value(value: str) -> str:
    if not value:
        return value
    if value[0] in ("'", '"', "`"):
        return value[0] * 2
    if value.startswith("{") and value.endswith("}"):
        inner = value[1:-1].strip()
        if _pure_braced_display_string(value):
            return "{" + inner[0] * 2 + "}"
        return "{" + _mask_js_expression_strings(inner) + "}"
    return ""


def _mask_display_attribute_values(tag: str) -> str:
    out = tag
    for name, start, end in reversed(_tag_attribute_value_spans(tag)):
        if name.lower() not in _DISPLAY_ATTRIBUTES:
            continue
        out = (
            out[:start]
            + _masked_display_attribute_value(tag[start:end])
            + out[end:]
        )
    return out


def _dynamic_display_attribute_signatures(
    text: str,
    *,
    tag_name: str | None = None,
) -> tuple[tuple[tuple[str, str], ...], ...]:
    body = strip_html_comments(_strip_code_blocks(text))
    signatures: list[tuple[tuple[str, str], ...]] = []
    for tag in _markup_tokens(body):
        name = re.match(r"<([A-Za-z][\w:.-]*)", tag)
        if name is None or (
            tag_name is not None
            and name.group(1).lower() != tag_name.lower()
        ):
            continue
        attributes: list[tuple[str, str]] = []
        for attribute, start, end in _tag_attribute_value_spans(tag):
            value = tag[start:end]
            if (
                attribute.lower() in _DISPLAY_ATTRIBUTES
                and value.startswith("{")
                and not _pure_braced_display_string(value)
            ):
                attributes.append(
                    (
                        attribute.lower(),
                        _masked_display_attribute_value(value),
                    )
                )
        if attributes:
            signatures.append(tuple(attributes))
    return tuple(signatures)


_UNPARSED_MARKUP_PREFIX = "\0unparsed-markup:"


def _markup_tokens(text: str) -> list[str]:
    tokens: list[str] = []
    index = 0
    while index < len(text):
        start = text.find("<", index)
        if start < 0:
            break
        if re.match(r"<https?://", text[start:], re.IGNORECASE):
            index = start + 1
            continue
        if not re.match(r"</?[A-Za-z][\w:.-]*(?:\s|/?>)", text[start:]):
            index = start + 1
            continue

        cursor = start + 1
        closed = False
        while cursor < len(text):
            char = text[cursor]
            if char in ("'", '"', "`"):
                end = _quoted_value_end(text, cursor)
                if (
                    end == len(text)
                    and (
                        not text
                        or text[-1] != char
                        or _is_escaped(text, len(text) - 1)
                    )
                ):
                    break
                cursor = end
                continue
            if char == "{":
                end = balanced_expression_end(text, cursor)
                if end is None:
                    break
                cursor = end
                continue
            if char == ">":
                tokens.append(text[start : cursor + 1])
                cursor += 1
                closed = True
                break
            cursor += 1
        if not closed:
            tokens.append(_UNPARSED_MARKUP_PREFIX + text[start:])
            break
        index = max(cursor, start + 1)
    return tokens


def _term_like(token: str) -> bool:
    lowered = token.lower()
    return bool(
        lowered in _LOWERCASE_TECH_TERMS
        or token.isupper()
        or token[:1].isupper()
        or any(char.isdigit() for char in token)
        or any(char.isupper() for char in token[1:])
    )


def _distinctive_technical_term(token: str) -> bool:
    return bool(
        token.lower() in _LOWERCASE_TECH_TERMS
        or token.isupper()
        or any(char.isdigit() for char in token)
        or any(char.isupper() for char in token[1:])
    )


def _is_inline_code_only_list_item(body: str) -> bool:
    if not inline_code_contents(body):
        return False
    remainder = strip_inline_code(body)
    return not remainder.strip(" `*_~.,:;()[]&/,+")


def _legacy_pipe_table_rows(
    text: str,
) -> list[tuple[bool, list[str]]]:
    return [
        (_table_line_signature(line)[0] == "separator", _table_cells(line))
        for line in text.splitlines()
    ]


def _legacy_pipe_cell_is_protected(
    cell: str, *, header: str | None = None
) -> bool:
    if inline_code_contents(cell) and not strip_inline_code(cell).strip(
        " `*_~.,:;()[]&/,+"
    ):
        return True
    if markdown_links(cell) and not strip_markdown_links(cell).strip(
        " `*_~.,:;()[]&/,+"
    ):
        return True
    visible = strip_inline_code(cell).strip(" `*_~")
    if _HTML_ENTITY_RE.fullmatch(visible):
        return True
    visible = visible.strip(".,:;")
    if (
        _VERSION_VALUE_RE.fullmatch(visible)
        or _DATE_VALUE_RE.fullmatch(visible)
        or _CONFIG_VALUE_RE.fullmatch(visible)
        or _PARENTHESIZED_LITERAL_RE.fullmatch(visible)
    ):
        return True
    if (
        header is not None
        and "type" in {word.lower() for word in re.findall(r"[A-Za-z]+", header)}
        and _TYPE_VALUE_RE.fullmatch(visible)
    ):
        return True
    if _protected_cell_kind(visible, header=header) is not None:
        return True
    if not visible:
        return False
    words = re.findall(r"[A-Za-z][A-Za-z0-9.+#-]*", visible)
    if len(words) == 1 and words[0] == visible:
        return (
            words[0].lower() in _PRODUCT_NAME_PREFIXES
            or _distinctive_technical_term(words[0])
        )
    return _is_protected_source_phrase(visible)


def _legacy_pipe_table_prose_roles(
    text: str, *, translate_headers: bool
) -> list[list[bool] | None]:
    rows = _legacy_pipe_table_rows(text)
    content_rows = [cells for separator, cells in rows if not separator]
    if not content_rows:
        return [None for _row in rows]
    headers = content_rows[0]
    content_index = 0
    roles: list[list[bool] | None] = []
    for separator, cells in rows:
        if separator:
            roles.append(None)
            continue
        if content_index == 0:
            roles.append(
                [
                    translate_headers
                    and bool(_ASCII_WORD_RE.search(cell))
                    and not _legacy_pipe_cell_is_protected(cell)
                    for cell in cells
                ]
            )
        else:
            roles.append(
                [
                    bool(_ASCII_WORD_RE.search(cell))
                    and not _legacy_pipe_cell_is_protected(
                        cell,
                        header=(
                            headers[column]
                            if column < len(headers)
                            else None
                        ),
                    )
                    for column, cell in enumerate(cells)
                ]
            )
        content_index += 1
    return roles


def legacy_pipe_table_contains_prose(
    text: str, *, include_headers: bool = True
) -> bool:
    if not _is_legacy_pipe_table_text(text):
        return False
    return any(
        any(row_roles)
        for row_roles in _legacy_pipe_table_prose_roles(
            text,
            translate_headers=include_headers,
        )
        if row_roles is not None
    )


def legacy_pipe_table_has_untranslated_prose(
    source: str,
    translated: str,
    *,
    require_translated_headers: bool = False,
) -> bool:
    if not (
        _is_legacy_pipe_table_text(source)
        and _is_legacy_pipe_table_text(translated)
    ):
        return False
    source_rows = _legacy_pipe_table_rows(source)
    translated_rows = _legacy_pipe_table_rows(translated)
    roles = _legacy_pipe_table_prose_roles(
        source,
        translate_headers=require_translated_headers,
    )
    if len(source_rows) != len(translated_rows):
        return False
    for (source_separator, source_cells), (
        translated_separator,
        translated_cells,
    ), row_roles in zip(source_rows, translated_rows, roles, strict=True):
        if (
            source_separator != translated_separator
            or len(source_cells) != len(translated_cells)
            or row_roles is None
        ):
            continue
        for source_cell, translated_cell, prose in zip(
            source_cells, translated_cells, row_roles, strict=True
        ):
            if prose and (
                source_cell == translated_cell
                or contains_untranslated_source_phrase(
                    source_cell, translated_cell
                )
            ):
                return True
    return False


def _legacy_pipe_table_contract(
    source: str,
    translated: str,
    locale: str | None,
) -> tuple[bool, bool, bool]:
    if not _is_legacy_pipe_table_text(translated):
        return False, False, False
    source_rows = _legacy_pipe_table_rows(source)
    translated_rows = _legacy_pipe_table_rows(translated)
    roles = _legacy_pipe_table_prose_roles(
        source,
        translate_headers=True,
    )
    if len(source_rows) != len(translated_rows):
        return False, False, False

    shape_valid = True
    protected_valid = True
    target_valid = True
    has_japanese_prose = False
    for (source_separator, source_cells), (
        translated_separator,
        translated_cells,
    ), row_roles in zip(source_rows, translated_rows, roles, strict=True):
        if (
            source_separator != translated_separator
            or len(source_cells) != len(translated_cells)
        ):
            shape_valid = False
            continue
        if source_separator:
            shape_valid = shape_valid and source_cells == translated_cells
            continue
        assert row_roles is not None
        for source_cell, translated_cell, prose in zip(
            source_cells, translated_cells, row_roles, strict=True
        ):
            if not prose:
                protected_valid = (
                    protected_valid and source_cell == translated_cell
                )
                continue
            if locale is None:
                continue
            source_words = len(_ASCII_WORD_RE.findall(source_cell))
            if source_words and not _has_target_language(
                translated_cell,
                locale,
                source_words,
                source_text=source_cell,
                minimum_chars=1,
                maximum_chars=1,
                require_japanese_kana=False,
            ):
                target_valid = False
            has_japanese_prose = has_japanese_prose or (
                locale == "ja" and source_words > 0
            )
    if (
        has_japanese_prose
        and not _JAPANESE_KANA_RE.search(translated)
    ):
        target_valid = False
    return shape_valid, protected_valid, target_valid


def _is_protected_source_phrase(text: str) -> bool:
    if _is_legacy_pipe_table_text(text):
        return not legacy_pipe_table_contains_prose(text)
    if _ENV_ASSIGNMENT_RE.fullmatch(text.strip(" `*_~")):
        return True
    words = re.findall(r"[A-Za-z][A-Za-z0-9.+#-]*", text)
    if not words:
        return False
    remainder = re.sub(r"[A-Za-z][A-Za-z0-9.+#-]*", "", text)
    if remainder.strip(" `*_~.,:;()[]&/,+"):
        return False
    lowered_words = {word.lower() for word in words}
    if lowered_words & _PROSE_SIGNAL_WORDS:
        return False
    if all(_distinctive_technical_term(word) for word in words):
        if (
            len(words) > 4
            and all(word.isupper() for word in words)
            and not re.search(r"[/,]", text)
        ):
            return False
        return True
    if len(words) > 4:
        return False
    return (
        _distinctive_technical_term(words[0])
        and all(
            word[:1].isupper() or _distinctive_technical_term(word)
            for word in words[1:]
        )
    ) or (
        words[0].lower() in _PRODUCT_NAME_PREFIXES
        and all(word[:1].isupper() for word in words[1:])
    )


def contains_untranslated_source_phrase(source: str, translated: str) -> bool:
    if _is_legacy_pipe_table_text(source):
        return legacy_pipe_table_has_untranslated_prose(
            source, translated
        )
    source_words = tuple(
        word.casefold() for word in _ASCII_WORD_RE.findall(source)
    )
    translated_words = tuple(
        word.casefold() for word in _ASCII_WORD_RE.findall(translated)
    )
    contains_source_words = any(
        translated_words[index : index + len(source_words)] == source_words
        for index in range(len(translated_words) - len(source_words) + 1)
    )
    return (
        len(source_words) >= 2
        and contains_source_words
        and not _is_legal_source_text(source)
        and not _is_protected_source_phrase(source)
    )


def _protected_ascii_letter_allowance(source: str, translated: str) -> int:
    source_terms = Counter(
        term
        for term in re.findall(r"[A-Za-z][A-Za-z0-9.+#-]*", source)
        if _term_like(term)
    )
    translated_terms = Counter(
        re.findall(r"[A-Za-z][A-Za-z0-9.+#-]*", translated)
    )
    return sum(
        len(re.findall(r"[A-Za-z]", term))
        * min(count, translated_terms[term])
        for term, count in source_terms.items()
    )


def _is_bare_protected_term_list(block: Block) -> bool:
    if _text_kind(block.lines[0]) != "list":
        return False
    for line in block.lines:
        marker = _UNORDERED_LIST_RE.match(line) or _ORDERED_LIST_RE.match(line)
        if not marker:
            return False
        body = marker.group(marker.lastindex or 0)
        checkbox = _TASK_CHECKBOX_RE.match(body)
        if checkbox:
            body = body[checkbox.end() :]
        body = body.strip(" *_~.,:;()[]")
        if _is_inline_code_only_list_item(body):
            continue
        words = re.findall(r"[A-Za-z][A-Za-z0-9.+#-]*", body)
        remainder = re.sub(r"[A-Za-z][A-Za-z0-9.+#-]*", "", body)
        if not words or len(words) > 4 or remainder.strip(" &/,+"):
            return False
        if not all(_term_like(word) for word in words):
            return False
    return True


def _language_sample(text: str) -> str:
    text = strip_html_code_elements(text)
    text = strip_inline_code(text)
    text = strip_markdown_links(text)
    text = _AUTOLINK_RE.sub("", text)
    text = _URL_RE.sub("", text)
    text = _TAG_RE.sub("", text)
    return _HTML_ENTITY_RE.sub("", text)


def _inline_markup_signature(text: str) -> tuple[str, ...]:
    body = strip_html_comments(_strip_code_blocks(text))
    body = strip_inline_code(body)
    delimiters: list[str] = []
    index = 0
    while index < len(body):
        marker = body[index]
        if marker not in "*_~" or _is_escaped(body, index):
            index += 1
            continue
        end = index + 1
        while end < len(body) and body[end] == marker:
            end += 1
        run = body[index:end]
        previous = body[index - 1] if index else "\n"
        following = body[end] if end < len(body) else "\n"
        previous_punctuation = bool(re.match(r"[^\w\s]", previous))
        following_punctuation = bool(re.match(r"[^\w\s]", following))
        left_flanking = not following.isspace() and (
            not following_punctuation
            or previous.isspace()
            or previous_punctuation
        )
        right_flanking = not previous.isspace() and (
            not previous_punctuation
            or following.isspace()
            or following_punctuation
        )
        if marker == "_":
            can_open = left_flanking and (
                not right_flanking or previous_punctuation
            )
            can_close = right_flanking and (
                not left_flanking or following_punctuation
            )
        else:
            can_open = left_flanking
            can_close = right_flanking
        if (marker != "~" or len(run) >= 2) and (can_open or can_close):
            delimiters.append(run)
        index = end
    return tuple(delimiters)


def _table_rows(block: Block) -> list[str]:
    rows: list[str] = []
    for line in block.lines:
        if _table_line_signature(line)[0] == "separator":
            continue
        rows.append(" ".join(_table_cells(line)))
    return rows


def _markdown_link_signatures(
    text: str,
) -> tuple[
    Counter[str],
    list[str],
    Counter[tuple[str, str]],
    list[str],
]:
    body = mask_reference_definitions(
        strip_html_comments(_strip_code_blocks(text))
    )
    links = markdown_links(body)
    return (
        Counter(link.target for link in links),
        [link.label for link in links if not link.image],
        Counter(
            (link.label, link.target)
            for link in links
            if not link.image
        ),
        [link.title for link in links],
    )


def _markdown_image_signatures(text: str) -> list[tuple[str, str]]:
    body = mask_reference_definitions(
        strip_html_comments(_strip_code_blocks(text))
    )
    return [
        (link.target, link.title)
        for link in markdown_links(body)
        if link.image
    ]


def _mixed_image_order(text: str) -> tuple[str, ...]:
    body = mask_reference_definitions(
        strip_html_comments(_strip_code_blocks(text))
    )
    positions = [
        (link.start, "markdown")
        for link in markdown_links(body)
        if link.image
    ]
    cursor = 0
    for tag in _markup_tokens(body):
        position = body.find(tag, cursor)
        if position < 0:
            continue
        cursor = position + len(tag)
        match = re.match(r"<\s*/?\s*([A-Za-z][\w:.-]*)", tag)
        if match and match.group(1).lower() == "img":
            positions.append((position, "html"))
    return tuple(kind for _position, kind in sorted(positions))


def _reference_definition_signatures(
    text: str,
) -> tuple[
    tuple[str, ...],
    tuple[str, ...],
    tuple[tuple[str, str], ...],
    tuple[tuple[str, str, str], ...],
]:
    definitions = [
        (definition.label, definition.target, definition.title)
        for definition in reference_definitions(text)
    ]
    return (
        tuple(target for _label, target, _title in definitions),
        tuple(label for label, _target, _title in definitions),
        tuple(
            (label, target) for label, target, _title in definitions
        ),
        tuple(definitions),
    )


def _protected_cell_kind(
    text: str, *, header: str | None
) -> str | None:
    body = text.strip(" `*_~")
    data_cell = header is not None
    if data_cell and _DATE_VALUE_RE.fullmatch(body):
        return "localizable"
    if data_cell and (
        _VERSION_VALUE_RE.fullmatch(body)
        or _CONFIG_VALUE_RE.fullmatch(body)
        or _PARENTHESIZED_LITERAL_RE.fullmatch(body)
    ):
        return "invariant"
    words = re.findall(r"[A-Za-z][A-Za-z0-9.+#-]*", body)
    remainder = re.sub(r"[A-Za-z][A-Za-z0-9.+#-]*", "", body)
    strict_terms = bool(words) and all(
        word.lower() in _LOWERCASE_TECH_TERMS
        or word.isupper()
        or any(char.isdigit() for char in word)
        or any(char.isupper() for char in word[1:])
        for word in words
    )
    if strict_terms and not remainder.strip(" &/,+.:-0123456789()[]*"):
        return "invariant"
    if not data_cell:
        return None

    header_terms: set[str] = set()
    for word in re.findall(r"[A-Za-z]+", header or ""):
        lowered = word.lower()
        header_terms.add(lowered)
        if lowered.endswith("ies"):
            header_terms.add(lowered[:-3] + "y")
        elif lowered.endswith("sses"):
            header_terms.add(lowered[:-2])
        elif lowered.endswith("s"):
            header_terms.add(lowered[:-1])
    if header_terms & _IDENTIFIER_HEADER_TERMS:
        if (
            header_terms & _IDENTIFIER_LIST_HEADER_TERMS
            and _SCALAR_LIST_RE.fullmatch(body)
        ):
            return "localizable" if "type" in header_terms else "invariant"
        if _SCALAR_TOKEN_RE.fullmatch(body) and body[:1].islower():
            return "localizable" if "type" in header_terms else "invariant"
    product_headers = header_terms & _PRODUCT_HEADER_TERMS
    if product_headers:
        generic_single_feature = (
            product_headers == {"feature"}
            and len(words) == 1
            and words[0].lower() not in _PRODUCT_NAME_PREFIXES
            and not _distinctive_technical_term(words[0])
        )
        if (
            not generic_single_feature
            and words
            and not remainder.strip(" &/,+.:-0123456789()")
            and all(word[:1].isupper() or _term_like(word) for word in words)
        ):
            return "invariant"
    return None


def _protected_cell_matches(source: str, translated: str) -> bool:
    if _PROTECTED_CELL_TOKEN_RE.findall(source) != _PROTECTED_CELL_TOKEN_RE.findall(
        translated
    ):
        return False
    remainder = _PROTECTED_CELL_TOKEN_RE.sub("", translated)
    return not any(char.isalnum() for char in remainder)


def _table_language_is_valid(
    source_block: Block, translated_block: Block, locale: str
) -> bool:
    source_lines = [
        line
        for line in source_block.lines
        if _table_line_signature(line)[0] != "separator"
    ]
    translated_lines = [
        line
        for line in translated_block.lines
        if _table_line_signature(line)[0] != "separator"
    ]
    source_headers = _table_cells(source_lines[0]) if source_lines else []
    japanese_prose_cell = False
    for row_index, (source_line, translated_line) in enumerate(
        zip(source_lines, translated_lines, strict=False)
    ):
        source_cells = _table_cells(source_line)
        translated_cells = _table_cells(translated_line)
        for column, (source_cell, translated_cell) in enumerate(
            zip(source_cells, translated_cells, strict=False)
        ):
            source_sample = _language_sample(source_cell)
            source_word_count = len(_ASCII_WORD_RE.findall(source_sample))
            if not source_word_count:
                continue
            protected_kind = _protected_cell_kind(
                source_sample,
                header=(
                    source_headers[column]
                    if row_index > 0 and column < len(source_headers)
                    else None
                ),
            )
            if protected_kind is not None:
                if _protected_cell_matches(source_cell, translated_cell):
                    continue
                if protected_kind == "invariant" or not _has_target_language(
                    translated_cell,
                    locale,
                    source_word_count,
                    source_text=source_cell,
                    minimum_chars=1,
                    maximum_chars=1,
                    require_japanese_kana=False,
                ):
                    return False
                continue
            if not _has_target_language(
                translated_cell,
                locale,
                source_word_count,
                source_text=source_cell,
                minimum_chars=1,
                maximum_chars=1,
                require_japanese_kana=False,
            ):
                return False
            japanese_prose_cell = japanese_prose_cell or source_word_count >= 2
    return not (
        locale == "ja"
        and japanese_prose_cell
        and not _JAPANESE_KANA_RE.search("\n".join(translated_block.lines))
    )


def _has_target_language(
    text: str,
    locale: str,
    source_word_count: int,
    *,
    source_text: str | None = None,
    minimum_chars: int = 2,
    maximum_chars: int = 3,
    require_japanese_kana: bool = True,
) -> bool:
    sample = _language_sample(text)
    target_count = len(_TARGET_SCRIPT[locale].findall(sample))
    required = min(maximum_chars, max(minimum_chars, source_word_count))
    if target_count < required:
        return False
    if (
        locale == "ja"
        and require_japanese_kana
        and not _JAPANESE_KANA_RE.search(sample)
    ):
        return False
    other_count = len(_OTHER_TARGET_SCRIPT[locale].findall(sample))
    if locale == "ko" and other_count > target_count * 2:
        return False
    ascii_letters = len(re.findall(r"[A-Za-z]", sample))
    protected_ascii_letters = (
        _protected_ascii_letter_allowance(
            _language_sample(source_text),
            sample,
        )
        if source_text is not None
        else 0
    )
    return ascii_letters <= target_count * 2 + 2 + protected_ascii_letters


def _annotation_ownership_is_valid(text: str, source: str) -> bool:
    expected = _required_comments(source)
    optional_quoted_annotations = _optional_quoted_comments(source)
    _preserved, source_comment_indexes = _matched_source_comment_indexes(
        text, source
    )
    lines = text.splitlines()
    annotations: list[tuple[str, int, int, str]] = []
    optional_annotations: list[tuple[str, int, int, str]] = []

    for occurrence, (
        comment_body,
        start_line,
        end_line,
        _position,
    ) in enumerate(_comment_records(text)):
        if occurrence in source_comment_indexes:
            continue
        normalized = _normalize_comment(comment_body)
        if (
            not normalized
            or is_non_annotatable_line(normalized)
            or is_structural_html_fragment(normalized)
        ):
            continue

        match = (
            _ONE_LINE_COMMENT_RE.fullmatch(lines[start_line])
            if start_line == end_line
            else None
        )
        if match is None:
            return False
        prefix = match.group(1) if match else ""
        depth = _quote_depth(prefix)
        annotation = (normalized, end_line, depth, prefix)
        optional_key = (
            normalized,
            depth,
            _quote_block_ordinal(lines, start_line + 1),
        )
        if (
            match
            and depth > 0
            and _optional_quote_annotation_starts_block(lines, start_line)
            and optional_quoted_annotations[optional_key]
        ):
            optional_quoted_annotations[optional_key] -= 1
            optional_annotations.append(annotation)
        else:
            annotations.append(annotation)

    if [
        annotation for annotation, _index, _depth, _prefix in annotations
    ] != expected:
        return False

    for annotation, index, depth, prefix in annotations + optional_annotations:
        if index + 1 >= len(lines):
            return False
        body = lines[index + 1]
        if not body.strip() or _ONE_LINE_COMMENT_RE.fullmatch(body):
            return False
        if (
            fence_token(body)
            or is_named_anchor_line(body)
            or is_structural_html_line(body)
            or body.strip() == "---"
        ):
            return False
        indentation = len(prefix) - len(prefix.lstrip(" \t"))
        if indentation >= 4 and depth == 0:
            return False
        if _quote_depth(body) != depth:
            return False
        if depth > 0 and indentation != len(body) - len(body.lstrip(" \t")):
            return False
        if annotation.startswith("#"):
            heading = body.lstrip()
            while heading.startswith(">"):
                heading = heading[1:].lstrip()
            if heading != annotation:
                return False
        elif is_heading_line(body):
            return False
    return True


def verify(
    text: str,
    source: str,
    *,
    locale: str | None = None,
    allow_source_echo: bool = False,
) -> list[str]:
    """Return deterministic violations for one fresh provider response."""

    if locale is not None and locale not in _TARGET_SCRIPT:
        raise ValueError(f"unsupported response locale: {locale}")

    issues: list[str] = []
    if has_malformed_html_comment_delimiters(text):
        issues.append("provider malformed HTML comment")
    if _required_comments(source) != _annotation_comments(text, source):
        issues.append("provider original comment mismatch")

    if _normalized_fenced_code_blocks(source) != _normalized_fenced_code_blocks(text):
        issues.append("provider code block mismatch")
    if admonition_types(source) != admonition_types(text):
        issues.append("provider admonition type mismatch")

    source_blocks = _blocks(source)
    translated_blocks = _blocks(text)
    if list(map(_signature, source_blocks)) != list(map(_signature, translated_blocks)):
        issues.append("provider block signature mismatch")
    if _markdown_structure_signature(source) != _markdown_structure_signature(text):
        issues.append("provider markdown structure mismatch")
    if not _paragraph_indentation_is_valid(source_blocks, translated_blocks):
        issues.append("provider paragraph indentation mismatch")
    if not _paragraph_layout_is_valid(
        source_blocks,
        translated_blocks,
        allow_source_echo=allow_source_echo,
    ):
        issues.append("provider paragraph layout mismatch")
    if not _paragraph_sentence_cardinality_is_valid(source, text):
        issues.append("provider sentence cardinality mismatch")
    translated_description = front_matter_description(text)
    front_matter_valid = (
        translated_description is None or translated_description.valid
    )
    if not front_matter_valid:
        issues.append("provider front matter invalid")
    if _front_matter_signature(source_blocks) != _front_matter_signature(
        translated_blocks
    ):
        issues.append("provider front matter mismatch")
    if _html_markup_signature(source) != _html_markup_signature(text):
        issues.append("provider HTML markup mismatch")
    if html_code_contents(
        strip_html_comments(_strip_code_blocks(source))
    ) != html_code_contents(strip_html_comments(_strip_code_blocks(text))):
        issues.append("provider HTML code mismatch")
    if _inline_markup_signature(source) != _inline_markup_signature(text):
        issues.append("provider inline markup mismatch")
    (
        source_link_targets,
        source_link_labels,
        source_link_pairs,
        source_link_titles,
    ) = _markdown_link_signatures(source)
    (
        translated_link_targets,
        translated_link_labels,
        translated_link_pairs,
        translated_link_titles,
    ) = _markdown_link_signatures(text)
    if source_link_targets != translated_link_targets:
        issues.append("provider link target mismatch")
    if source_link_labels != translated_link_labels:
        issues.append("provider link label mismatch")
    if source_link_pairs != translated_link_pairs:
        issues.append("provider link pair mismatch")
    if source_link_titles != translated_link_titles:
        issues.append("provider link title mismatch")
    source_image_signatures = _markdown_image_signatures(source)
    translated_image_signatures = _markdown_image_signatures(text)
    if (
        [target for target, _title in source_image_signatures]
        != [target for target, _title in translated_image_signatures]
        and "provider link target mismatch" not in issues
    ):
        issues.append("provider link target mismatch")
    if (
        [title for _target, title in source_image_signatures]
        != [title for _target, title in translated_image_signatures]
        and "provider link title mismatch" not in issues
    ):
        issues.append("provider link title mismatch")
    if (
        _mixed_image_order(source) != _mixed_image_order(text)
        and "provider link target mismatch" not in issues
    ):
        issues.append("provider link target mismatch")
    (
        source_definition_targets,
        source_definition_labels,
        source_definition_pairs,
        source_definition_signatures,
    ) = _reference_definition_signatures(source)
    (
        translated_definition_targets,
        translated_definition_labels,
        translated_definition_pairs,
        translated_definition_signatures,
    ) = _reference_definition_signatures(text)
    if (
        source_definition_targets != translated_definition_targets
        and "provider link target mismatch" not in issues
    ):
        issues.append("provider link target mismatch")
    if (
        source_definition_labels != translated_definition_labels
        and "provider link label mismatch" not in issues
    ):
        issues.append("provider link label mismatch")
    definition_pairs_match = (
        source_definition_pairs == translated_definition_pairs
    )
    if (
        not definition_pairs_match
        and "provider link pair mismatch" not in issues
    ):
        issues.append("provider link pair mismatch")
    if (
        definition_pairs_match
        and source_definition_signatures
        != translated_definition_signatures
        and "provider link title mismatch" not in issues
    ):
        issues.append("provider link title mismatch")
    source_reference_links = reference_link_signatures(source)
    translated_reference_links = reference_link_signatures(text)
    if (
        tuple(
            (image, target)
            for image, target, _title in source_reference_links
        )
        != tuple(
            (image, target)
            for image, target, _title in translated_reference_links
        )
        and "provider link target mismatch" not in issues
    ):
        issues.append("provider link target mismatch")
    if (
        tuple(title for _image, _target, title in source_reference_links)
        != tuple(
            title
            for _image, _target, title in translated_reference_links
        )
        and "provider link title mismatch" not in issues
    ):
        issues.append("provider link title mismatch")
    source_inline_code = Counter(
        inline_code_contents(strip_html_comments(_strip_code_blocks(source)))
    )
    translated_inline_code = Counter(
        inline_code_contents(strip_html_comments(_strip_code_blocks(text)))
    )
    if source_inline_code != translated_inline_code:
        issues.append("provider inline code mismatch")
    if not _source_comments_are_preserved(text, source):
        issues.append("provider source comment mismatch")
    if not _annotation_ownership_is_valid(text, source):
        issues.append("provider annotation ownership mismatch")

    target_language_missing = False
    if (
        locale is not None
        and front_matter_valid
        and not _front_matter_language_is_valid(
        text, source, locale
        )
    ):
        target_language_missing = True
    for source_block, translated_block in zip(
        source_blocks, translated_blocks, strict=False
    ):
        if source_block.kind != "text" or translated_block.kind != "text":
            continue
        if _is_toc_link_list(source_block):
            continue
        if is_reference_definition_block(
            "\n".join(source_block.lines)
        ):
            continue
        source_body = _normalized_body(source_block)
        translated_body = _normalized_body(translated_block)
        if _text_kind(source_block.lines[0]) == "table":
            source_rows = _table_rows(source_block)
            translated_rows = _table_rows(translated_block)
            if (
                len(source_rows) == len(set(source_rows))
                and len(translated_rows) != len(set(translated_rows))
            ):
                issues.append("provider duplicate table row")
            if (
                locale is not None
                and not _table_language_is_valid(
                    source_block, translated_block, locale
                )
            ):
                target_language_missing = True
            continue
        source_word_count = len(_ASCII_WORD_RE.findall(source_body))
        legal_source = allow_source_echo and _is_legal_source_text(source_body)
        if legal_source:
            if translated_body != source_body:
                issues.append("provider license text mismatch")
            continue
        if _is_indented_literal_block(source_block):
            if translated_body != source_body:
                issues.append("provider protected term mismatch")
            continue
        if _is_legacy_pipe_table_block(source_block):
            source_table = "\n".join(source_block.lines)
            translated_table = "\n".join(translated_block.lines)
            shape_valid, protected_valid, table_target_valid = (
                _legacy_pipe_table_contract(
                    source_table,
                    translated_table,
                    locale,
                )
            )
            if not shape_valid:
                issues.append("provider markdown structure mismatch")
            if not protected_valid:
                issues.append("provider protected term mismatch")
            if legacy_pipe_table_has_untranslated_prose(
                source_table,
                translated_table,
                require_translated_headers=True,
            ):
                issues.append("provider untranslated source text")
            if not table_target_valid:
                target_language_missing = True
            continue
        if all(
            is_reference_definition_line(line)
            for line in source_block.lines
        ):
            continue
        if _is_inline_code_only_list_item(source_body):
            if translated_body != source_body:
                issues.append("provider protected term mismatch")
            continue
        if (
            translated_body == source_body
            and _is_protected_source_phrase(source_body)
        ):
            continue
        source_kind = _text_kind(source_block.lines[0])
        if _is_bare_protected_term_list(source_block):
            if translated_body != source_body:
                issues.append("provider protected term mismatch")
            continue
        if contains_untranslated_source_phrase(source_body, translated_body):
            issues.append("provider untranslated source text")

        if (
            locale is not None
            and source_kind in ("paragraph", "list", "quote", "html")
            and source_word_count >= 2
            and not _has_target_language(
                translated_body,
                locale,
                source_word_count,
                source_text=source_body,
            )
        ):
            target_language_missing = True

    if target_language_missing:
        issues.append("provider target language mismatch")

    return issues
