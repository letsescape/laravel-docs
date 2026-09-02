"""새로 생성된 provider 응답의 엄격한 구조 계약.

최종 문서 verifier는 과거 번역 형태를 허용하지만 이 모듈은 신규 provider 응답을 문서에 patch하기 전 검증하는 더 좁은 범위만 담당.
"""
from __future__ import annotations

import math
import re
import unicodedata
from bisect import bisect_right
from collections import Counter
from dataclasses import dataclass, field

from ..annotation.annotate import Block, split_blocks
from ..common.admonitions import admonition_types
from ..common.javascript import (
    balanced_expression_end,
    top_level_plus_positions,
)
from ..common.markdown import (
    FrontMatterDescription,
    closes_fence,
    fence_token,
    front_matter_description,
    has_malformed_html_comment_delimiters,
    html_code_contents,
    html_comment_spans,
    inline_code_contents,
    is_gfm_pipe_table,
    is_escaped,
    is_heading_line,
    is_named_anchor_line,
    is_non_annotatable_line,
    is_ordered_list_marker,
    is_reference_definition_block,
    is_reference_definition_line,
    is_structural_html_fragment,
    is_structural_html_line,
    markdown_autolinks,
    markdown_links,
    mask_fenced_code_contents,
    mask_reference_definitions,
    normalize_annotation_anchor,
    quote_depth,
    reference_definition_line_numbers,
    reference_definitions,
    reference_link_display_signatures,
    reference_link_signatures,
    standalone_html_comment_line_numbers,
    strip_html_code_elements,
    strip_html_comments,
    strip_inline_code,
    strip_markdown_links,
    strip_title_attr_line,
    table_row_cells,
)
from ..common.versions import validate_version_token
from ..postprocessing.postprocess import replace_version

RESPONSE_CONTRACT_VERSION = 1

_UNORDERED_LIST_RE = re.compile(r"^([ \t]*)([-*+])[ \t]+(\S.*)$")
_ORDERED_LIST_RE = re.compile(r"^([ \t]*)(\d+)([.)])[ \t]+(\S.*)$")
_EMPTY_QUOTE_RE = re.compile(r"^[ \t]*(?:>[ \t]*)+$")
_ASCII_WORD_RE = re.compile(r"[A-Za-z]{2,}")
_TASK_CHECKBOX_RE = re.compile(r"^\[([ xX])](?:[ \t]+|$)")
_ADMONITION_MARKER_RE = re.compile(
    r"^\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT)](?:[ \t]+|$)", re.IGNORECASE
)
_TARGET_LOCALES = frozenset(("ko", "ja"))
# Python 3.14의 Unicode 16.0 대신 계약 버전 1의 문자 범위를 Unicode 15.1로 고정
_POST_UNICODE_15_1_LETTER_RANGES = (
    (0x1C89, 0x1C8A),
    (0xA7CB, 0xA7CD),
    (0xA7DA, 0xA7DC),
    (0x105C0, 0x105F3),
    (0x10D4A, 0x10D65),
    (0x10D6F, 0x10D85),
    (0x10EC2, 0x10EC4),
    (0x11380, 0x11389),
    (0x1138B, 0x1138B),
    (0x1138E, 0x1138E),
    (0x11390, 0x113B5),
    (0x113B7, 0x113B7),
    (0x113D1, 0x113D1),
    (0x113D3, 0x113D3),
    (0x11BC0, 0x11BE0),
    (0x13460, 0x143FA),
    (0x16100, 0x1611D),
    (0x16D40, 0x16D6C),
    (0x18CFF, 0x18CFF),
    (0x1E5D0, 0x1E5ED),
    (0x1E5F0, 0x1E5F0),
)
_DISPLAY_ATTRIBUTES = frozenset(
    ("alt", "placeholder", "aria-label", "aria-description")
)
_QUOTED_ADMONITION_MARKER_RE = re.compile(
    r"^([ \t]*(?:>[ \t]*)*)\[!(?:NOTE|TIP|WARNING|CAUTION|IMPORTANT)]",
    re.IGNORECASE,
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
_PROSE_TRIM_CHARACTERS = " `*_~.,:;()[]&/,+"
_MARKDOWN_TRIM_CHARACTERS = " `*_~"
_PROTECTED_WORD_PATTERN = r"[A-Za-z][A-Za-z0-9.+#-]*"
_DATA_ITEM_SEPARATOR_RE = re.compile(r"\s*[,/]\s*|\s+and\s+")
_QUOTED_LITERAL_RE = re.compile(r'"[^"\n]*"')
_JSON_STRUCTURE_CHARACTERS = " \t\n{}[]:,"
_PROVIDER_LINK_TARGET_MISMATCH = "provider link target mismatch"
_PROVIDER_LINK_LABEL_MISMATCH = "provider link label mismatch"
_PROVIDER_LINK_PAIR_MISMATCH = "provider link pair mismatch"
_PROVIDER_LINK_TITLE_MISMATCH = "provider link title mismatch"
_FEEDBACK_RETRYABLE_ISSUES = frozenset(
    (
        _PROVIDER_LINK_TARGET_MISMATCH,
        _PROVIDER_LINK_LABEL_MISMATCH,
        _PROVIDER_LINK_PAIR_MISMATCH,
        _PROVIDER_LINK_TITLE_MISMATCH,
        "provider inline code mismatch",
        "provider inline markup mismatch",
        "provider original comment mismatch",
        "provider admonition type mismatch",
        "provider target language mismatch",
    )
)
_PROVIDER_PROTECTED_TERM_MISMATCH = "provider protected term mismatch"
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
_VERSION_CORE_PREFIX_RE = re.compile(r"core\s*,?\s*", re.IGNORECASE)
_VERSION_TOKEN_RE = re.compile(
    r"[v^~<>=]*\d+(?:\.[0-9x*]+)*(?:\+)?", re.IGNORECASE
)
_VERSION_LABEL_RE = re.compile(r"\s+[A-Za-z][\w-]*", re.IGNORECASE)
_VERSION_SEPARATOR_RE = re.compile(
    r"\s*(?:[-–,/]|\bor\b)\s*", re.IGNORECASE
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
    """검사 대상에서 fenced code 블록 내용 제거."""

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
    """문서 순서대로 정규화한 fenced code 블록 목록."""

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
    """HTML 주석 본문의 공백 정규화."""

    return normalize_annotation_anchor(text)


def _table_owner_spans(text: str) -> tuple[dict[int, str], frozenset[int]]:
    """표 전체를 소유하는 주석 위치와 표 줄 집합."""

    comments: dict[int, str] = {}
    member_lines: set[int] = set()
    for block in split_blocks(text.splitlines()):
        if block.kind != "text" or not block.lines:
            continue
        if not (
            _text_kind(block.lines[0]) == "table"
            or _is_legacy_pipe_table_block(block)
        ):
            continue
        comment = _normalize_comment(
            " ".join(line.strip() for line in block.lines)
        )
        if not comment:
            continue
        comments[block.start] = comment
        member_lines.update(range(block.start, block.end))
    return comments, frozenset(member_lines)


def _required_table_comments(source: str) -> frozenset[str]:
    """원문 표에 필요한 canonical 주석 집합."""

    comments, _member_lines = _table_owner_spans(_strip_code_blocks(source))
    return frozenset(comments.values())


def _annotation_line_action(
    line: str,
    index: int,
    *,
    in_front_matter: bool,
    source_comment_lines: frozenset[int],
    reference_lines: frozenset[int],
    table_comments: dict[int, str],
    table_member_lines: frozenset[int],
) -> tuple[str, bool, str]:
    """원문 줄의 annotation 처리 종류와 다음 머리말 상태 결정.

    Args:
        line: 원문 물리 줄.
        index: code block을 제외한 0-based 줄 위치.
        in_front_matter: 이전 줄까지 머리말 내부 여부.
        source_comment_lines: 원문 작성 주석의 1-based 줄 번호.
        reference_lines: 참조 정의의 0-based 줄 번호.
        table_comments: 표 시작 줄별 canonical 주석.
        table_member_lines: 표에 속한 전체 줄 위치.

    Returns:
        처리 종류, 다음 머리말 상태, 주석 또는 문단 본문.
    """

    stripped = line.strip()
    if index == 0 and stripped == "---":
        return "skip", True, ""
    if in_front_matter and stripped == "---":
        return "skip", False, ""
    if in_front_matter:
        return "skip", True, ""
    return _annotation_body_action(
        line,
        index,
        source_comment_lines=source_comment_lines,
        reference_lines=reference_lines,
        table_comments=table_comments,
        table_member_lines=table_member_lines,
    )


def _annotation_body_action(
    line: str,
    index: int,
    *,
    source_comment_lines: frozenset[int],
    reference_lines: frozenset[int],
    table_comments: dict[int, str],
    table_member_lines: frozenset[int],
) -> tuple[str, bool, str]:
    """머리말 밖 원문 줄의 annotation 처리 종류 결정.

    Args:
        line: 원문 물리 줄.
        index: code block을 제외한 0-based 줄 위치.
        source_comment_lines: 원문 작성 주석의 1-based 줄 번호.
        reference_lines: 참조 정의의 0-based 줄 번호.
        table_comments: 표 시작 줄별 canonical 주석.
        table_member_lines: 표에 속한 전체 줄 위치.

    Returns:
        처리 종류, ``False`` 머리말 상태, 주석 또는 문단 본문.
    """

    stripped = line.strip()
    if index in table_comments:
        return "table", False, table_comments[index]
    if index in table_member_lines:
        return "skip", False, ""
    if index + 1 in source_comment_lines or index in reference_lines:
        return "flush", False, ""
    if not stripped:
        return "flush", False, ""
    if is_heading_line(line):
        return "heading", False, stripped
    if stripped.startswith(">"):
        return "flush", False, ""
    if is_structural_html_line(line) or is_non_annotatable_line(line):
        return "flush", False, ""
    if _line_is_inline_code_only_list_item(stripped):
        return "flush", False, ""
    return "paragraph", False, stripped


def _line_is_inline_code_only_list_item(stripped: str) -> bool:
    """Markdown 줄이 inline code만 포함한 목록 항목인지 판정.

    Args:
        stripped: 앞뒤 공백이 제거된 Markdown 줄.

    Returns:
        inline code 전용 목록 항목 여부.
    """

    marker = _UNORDERED_LIST_RE.match(stripped) or _ORDERED_LIST_RE.match(stripped)
    if marker is None:
        return False
    item_body = marker.group(marker.lastindex or 0)
    checkbox = _TASK_CHECKBOX_RE.match(item_body)
    if checkbox:
        item_body = item_body[checkbox.end() :]
    return _is_inline_code_only_list_item(item_body)


@dataclass
class _RequiredCommentAccumulator:
    """필수 annotation 본문 누적 상태."""

    comments: list[str] = field(default_factory=list)
    paragraph: list[str] = field(default_factory=list)
    paragraph_kind: str | None = None

    def flush(self) -> None:
        """누적 문단을 canonical 주석 본문으로 확정."""

        if self.paragraph:
            if not is_structural_html_fragment("\n".join(self.paragraph)):
                self.comments.append(
                    _normalize_comment(" ".join(self.paragraph))
                )
            self.paragraph.clear()
        self.paragraph_kind = None

    def append(self, kind: str, text: str) -> None:
        """같은 유형의 문단 본문 누적.

        Args:
            kind: 번역 소유 블록 유형.
            text: canonical 원문 조각.
        """

        if self.paragraph_kind not in (None, kind):
            self.flush()
        self.paragraph_kind = kind
        self.paragraph.append(text)


def mismatched_required_comments(text: str, source: str) -> list[str]:
    """응답 annotation과 위치가 대응하지만 내용이 어긋난 required 주석 원문."""

    required = _required_comments(source)
    actual = _annotation_comments(text, source)
    return [
        expected
        for expected, received in zip(required, actual)
        if expected != received
    ]


def target_script_ratio(text: str, locale: str) -> float:
    """산문에서 목표 문자 체계가 차지하는 비율.

    문서 단위 판정에 사용하며, 코드·링크·heading 등 보호 구간은 제외한다.
    """

    sample = _normalized_language_prose(text)
    letters = _unicode_letter_count(sample)
    if not letters:
        return 1.0
    return _target_script_count(sample, locale) / letters


def echoed_header_cells(text: str, source: str) -> list[str]:
    """번역되지 않고 원문 그대로 돌아온 표 머리글 셀 원문."""

    echoed: list[str] = []
    for source_block, translated_block in zip(
        _blocks(source),
        _blocks(text),
        strict=False,
    ):
        if source_block.kind != "text" or translated_block.kind != "text":
            continue
        if not source_block.lines or _text_kind(source_block.lines[0]) != "table":
            continue
        if not translated_block.lines:
            continue
        source_cells = table_row_cells(source_block.lines[0])
        translated_cells = table_row_cells(translated_block.lines[0])
        echoed.extend(
            expected
            for expected, received in zip(source_cells, translated_cells)
            if _cell_echoes_translatable_prose(expected, received)
        )
    return echoed


def _required_comments(source: str) -> list[str]:
    """원문 블록에 필요한 canonical 주석 순서."""

    body = _strip_code_blocks(source)
    source_comment_lines = standalone_html_comment_line_numbers(body)
    reference_lines = reference_definition_line_numbers(body)
    table_comments, table_member_lines = _table_owner_spans(body)
    accumulator = _RequiredCommentAccumulator()
    in_front_matter = False

    for index, line in enumerate(body.splitlines()):
        action, in_front_matter, content = _annotation_line_action(
            line,
            index,
            in_front_matter=in_front_matter,
            source_comment_lines=source_comment_lines,
            reference_lines=reference_lines,
            table_comments=table_comments,
            table_member_lines=table_member_lines,
        )
        if action == "skip":
            continue
        if action == "table":
            accumulator.flush()
            accumulator.comments.append(content)
            continue
        if action == "flush":
            accumulator.flush()
            continue
        if action == "heading":
            accumulator.flush()
            accumulator.comments.append(_normalize_comment(content))
            continue
        accumulator.append("paragraph", content)

    accumulator.flush()
    return [comment for comment in accumulator.comments if comment]


def _optional_quoted_comments(
    source: str,
) -> Counter[tuple[str, int, int]]:
    """호환 가능한 인용문 주석과 대응 원문 위치."""

    comments: Counter[tuple[str, int, int]] = Counter()
    quote_block = 0
    for block in _blocks(source):
        if _text_kind(block.lines[0]) != "quote":
            continue
        block_ordinal = quote_block
        quote_block += 1
        if block.kind != "text":
            continue
        normalized = _normalize_comment(" ".join(_quote_prose_lines(block)))
        if normalized:
            comments[
                (normalized, quote_depth(block.lines[0]), block_ordinal)
            ] += 1
    return comments


def _quote_prose_lines(block: Block) -> list[str]:
    """인용 블록에서 annotation 대상 산문 줄 추출.

    Args:
        block: 인용 Markdown 블록.

    Returns:
        인용 표식과 admonition 표식을 제거한 산문 줄.
    """

    bodies: list[str] = []
    for line in block.lines:
        content = line.lstrip()
        while content.startswith(">"):
            content = content[1:].lstrip()
        if content and not _ADMONITION_MARKER_RE.match(content):
            bodies.append(content)
    return bodies


def _quote_block_ordinal(lines: list[str], line_index: int) -> int:
    """지정한 줄이 속한 최상위 인용 블록 순번."""

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
    """선택적 인용문 주석이 해당 인용 블록을 소유하는지 여부."""

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
    """응답에서 원문 작성 주석을 제외한 annotation 순서."""

    _preserved, source_comment_indexes = _matched_source_comment_indexes(
        text, source
    )
    optional_quoted_annotations = _optional_quoted_comments(source)
    table_annotations = _required_table_comments(source)
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
        if not _is_annotation_body(normalized, table_annotations):
            continue
        if _consume_optional_quote_annotation(
            normalized,
            lines,
            start_line,
            end_line,
            optional_quoted_annotations,
        ):
            continue
        annotations.append(normalized)
    return annotations


def _is_annotation_body(
    normalized: str,
    table_annotations: frozenset[str],
) -> bool:
    """정규화된 주석이 번역 annotation 본문인지 판정.

    Args:
        normalized: 정규화된 주석 본문.
        table_annotations: 필수 표 annotation 집합.

    Returns:
        번역 annotation 포함 대상 여부.
    """

    return bool(
        (
            normalized in table_annotations
            or not is_non_annotatable_line(normalized)
        )
        and not is_structural_html_fragment(normalized)
    )


def _consume_optional_quote_annotation(
    normalized: str,
    lines: list[str],
    start_line: int,
    end_line: int,
    optional: Counter[tuple[str, int, int]],
) -> bool:
    """선택적 인용 annotation occurrence 소비.

    Args:
        normalized: 정규화된 주석 본문.
        lines: 응답 물리 줄.
        start_line: 주석 시작 줄.
        end_line: 주석 종료 줄.
        optional: 남은 선택적 인용 annotation 횟수.

    Returns:
        허용된 선택적 인용 annotation인지 여부.
    """

    match = (
        _ONE_LINE_COMMENT_RE.fullmatch(lines[start_line])
        if start_line == end_line
        else None
    )
    if match is None:
        return False
    depth = quote_depth(match.group(1))
    key = (normalized, depth, _quote_block_ordinal(lines, start_line + 1))
    if (
        depth == 0
        or not _optional_quote_annotation_starts_block(lines, start_line)
        or not optional[key]
    ):
        return False
    optional[key] -= 1
    return True


def _text_kind(line: str) -> str:
    """줄이 나타내는 번역 소유 블록 유형."""

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
    """줄 끝에 명시적 Markdown hard break가 있는지 여부."""

    trailing_backslashes = len(line) - len(line.rstrip("\\"))
    return line.endswith("  ") or trailing_backslashes % 2 == 1


def _signature(block: Block) -> tuple[object, ...]:
    """Markdown 블록의 구조 비교 서명."""

    if block.kind == "heading":
        stripped = block.lines[0].lstrip()
        return ("heading", len(stripped) - len(stripped.lstrip("#")))
    if block.kind != "text":
        return (block.kind,)

    kind = _text_kind(block.lines[0])
    if kind == "list":
        return ("text", kind, _list_marker_signature(block.lines))
    if kind == "quote":
        depths = tuple(
            (quote_depth(line), _has_markdown_hard_break(line))
            for line in block.lines
        )
        return ("text", kind, depths)
    if kind == "table":
        return ("text", kind, tuple(_table_line_signature(line) for line in block.lines))
    if kind == "html":
        return ("text", kind, len(block.lines))
    return ("text", kind)


def _list_marker_signature(lines: list[str]) -> tuple[str, ...]:
    """목록 줄의 들여쓰기·표식·checkbox 상태 서명 생성.

    Args:
        lines: 목록 블록 물리 줄.

    Returns:
        목록 항목별 구조 서명.
    """

    markers: list[str] = []
    for line in lines:
        unordered = _UNORDERED_LIST_RE.match(line)
        ordered = _ORDERED_LIST_RE.match(line)
        if unordered:
            checkbox = _TASK_CHECKBOX_RE.match(unordered.group(3))
            state = checkbox.group(1).lower() if checkbox else ""
            markers.append(f"{unordered.group(1)}{unordered.group(2)}[{state}]")
        elif ordered:
            markers.append(f"{ordered.group(1)}{ordered.group(2)}{ordered.group(3)}")
    return tuple(markers)


def _table_line_signature(line: str) -> tuple[object, ...]:
    """표 행의 셀 수와 separator 정렬 서명."""

    cells = table_row_cells(line)
    if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
        return (
            "separator",
            tuple((cell.startswith(":"), cell.endswith(":")) for cell in cells),
        )
    return ("row", len(cells))


def _strip_comments_for_blocks(text: str) -> str:
    """Markdown 줄바꿈을 만들지 않는 독립 주석 줄 제거."""

    out: list[str] = []
    cursor = 0
    for start, end, _body in html_comment_spans(text):
        line_start = text.rfind("\n", 0, start) + 1
        line_end = text.find("\n", end)
        content_end = len(text) if line_end < 0 else line_end
        prefix = text[line_start:start]
        suffix = text[end:content_end]
        standalone = bool(
            re.fullmatch(r"[ \t]*(?:>[ \t]*)*", prefix)
            and not suffix.strip()
        )
        if standalone:
            out.append(text[cursor:line_start])
            cursor = len(text) if line_end < 0 else line_end + 1
        else:
            out.append(text[cursor:start])
            cursor = end
    out.append(text[cursor:])
    return "".join(out)


def _blocks(text: str) -> list[Block]:
    """응답 계약 검증에 사용할 Markdown 소유 블록 목록."""

    lines = [
        line
        for line in _strip_comments_for_blocks(text).splitlines()
        if not _EMPTY_QUOTE_RE.fullmatch(line)
    ]
    return split_blocks(lines)


def _markdown_structure_signature(text: str) -> list[tuple[object, ...]]:
    """문서 순서를 보존한 Markdown 블록 구조 서명."""

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

        line_signature = _markdown_line_signature(line)
        if line_signature is not None:
            signature.append(line_signature)

    return signature


def _markdown_line_signature(line: str) -> tuple[object, ...] | None:
    """단일 표시 줄의 목록·인용·표 구조 서명 생성.

    Args:
        line: Markdown 물리 줄.

    Returns:
        구조 서명. 대상 줄이 아니면 ``None``.
    """

    unordered = _UNORDERED_LIST_RE.match(line)
    ordered = _ORDERED_LIST_RE.match(line)
    if unordered:
        indent, marker, remainder = unordered.groups()
        checkbox = _TASK_CHECKBOX_RE.match(remainder)
        list_marker = (marker, checkbox.group(1).lower() if checkbox else "")
        return "list", indent, list_marker, quote_depth(remainder)
    if ordered:
        indent, number, delimiter, remainder = ordered.groups()
        return "list", indent, (f"{number}{delimiter}", ""), quote_depth(remainder)
    if line.lstrip().startswith(">"):
        return _quote_line_signature(line)
    if line.lstrip().startswith("|"):
        return "table", *_table_line_signature(line)
    return None


def _quote_line_signature(line: str) -> tuple[object, ...]:
    """인용 줄의 들여쓰기·깊이·admonition·hard break 서명 생성.

    Args:
        line: 인용 Markdown 줄.

    Returns:
        인용 구조 서명.
    """

    quote = line.lstrip()
    depth = quote_depth(quote)
    content = quote
    for _ in range(depth):
        content = content[1:].lstrip()
    marker = _ADMONITION_MARKER_RE.match(content)
    return (
        "quote",
        line[: len(line) - len(line.lstrip())],
        depth,
        marker.group(1).upper() if marker else "",
        _has_markdown_hard_break(line),
    )


def _normalized_body(block: Block) -> str:
    """구조 접두사와 바깥 공백을 제거한 블록 본문."""

    lines: list[str] = []
    for line in block.lines:
        stripped = line.strip()
        stripped = re.sub(
            r"^(?:[-*+]\s+|\d+[.)]\s+|>+\s*|\|\s*)", "", stripped
        )
        lines.append(stripped)
    return " ".join(" ".join(lines).split())


def _block_language_text(block: Block) -> str:
    """목표 언어 판정에 사용할 블록의 번역 가능 본문."""

    lines: list[str] = []
    for line in block.lines:
        content = line.lstrip(" \t")
        while content.startswith(">"):
            content = content[1:].lstrip(" \t")
        list_item = _UNORDERED_LIST_RE.match(content) or _ORDERED_LIST_RE.match(
            content
        )
        if list_item:
            content = list_item.group(list_item.lastindex or 0)
        checkbox = _TASK_CHECKBOX_RE.match(content)
        if checkbox:
            content = content[checkbox.end() :]
        admonition = _ADMONITION_MARKER_RE.match(content)
        if admonition:
            content = content[admonition.end() :]
        lines.append(content)
    return "\n".join(lines)


def _is_indented_literal_block(block: Block) -> bool:
    """블록이 들여쓰기 literal 코드인지 여부."""

    return bool(block.lines) and all(
        line.startswith("\t") or len(line) - len(line.lstrip(" ")) >= 4
        for line in block.lines
    )


def _is_legacy_pipe_table_block(block: Block) -> bool:
    """블록이 단일 legacy pipe table인지 여부."""

    return _is_legacy_pipe_table_text("\n".join(block.lines))


def _is_legacy_pipe_table_text(text: str) -> bool:
    """문자열이 legacy pipe table 형태인지 여부."""

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
    """목록 블록이 내부 앵커만 나열한 목차인지 여부."""

    return bool(block.lines) and all(
        line.strip().startswith(("- [", "* [")) and "](#" in line
        for line in block.lines
    )


@dataclass
class _FrontMatterSignatureState:
    """머리말 scalar 구조 서명 누적 상태."""

    lines: list[str] = field(default_factory=list)
    description_block: bool = False
    description_content: bool = False
    source_owned_block: bool = False

    def flush_description(self) -> None:
        """누적 description scalar의 본문 존재 상태 확정."""

        if self.description_block:
            self.lines.append(
                "description-content: present"
                if self.description_content
                else "description-content: empty"
            )
        self.description_block = False
        self.description_content = False


def _front_matter_block_signature(block: Block) -> tuple[str, ...]:
    """단일 머리말 블록의 key·scalar 구조 서명 생성.

    Args:
        block: 머리말 Markdown 블록.

    Returns:
        줄 순서를 보존한 머리말 구조 서명.
    """

    description = front_matter_description("\n".join(block.lines))
    state = _FrontMatterSignatureState()
    for line in block.lines:
        key = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*", line)
        if key:
            _append_front_matter_key(state, line, key, description)
            continue
        if state.description_block and line[:1].isspace():
            state.description_content = state.description_content or bool(line.strip())
            continue
        if state.source_owned_block and (not line or line[:1].isspace()):
            state.lines.append(line)
            continue
        state.flush_description()
        state.source_owned_block = False
        state.lines.append(line.rstrip())
    state.flush_description()
    return tuple(state.lines)


def _append_front_matter_key(
    state: _FrontMatterSignatureState,
    line: str,
    key: re.Match[str],
    description: FrontMatterDescription | None,
) -> None:
    """머리말 key와 scalar 형태를 구조 서명에 추가.

    Args:
        state: 머리말 구조 서명 누적 상태.
        line: key가 포함된 원문 줄.
        key: key 정규식 match.
        description: 파싱된 description 계약 또는 ``None``.
    """

    state.flush_description()
    state.source_owned_block = False
    if key.group(1) != "description":
        state.lines.append(line.rstrip())
        state.source_owned_block = line[key.end() :].lstrip().startswith(("|", ">"))
        return
    if description is None or not description.valid:
        state.lines.append("description: invalid")
        return
    value_state = "present" if description.value else "empty"
    state.lines.append(
        f"description: {description.style}:{value_state}:{description.comment}"
    )
    state.description_block = description.style.startswith("block:")


def _front_matter_signature(blocks: list[Block]) -> list[tuple[str, ...]]:
    """머리말 블록의 key·scalar 구조 서명."""

    return [
        _front_matter_block_signature(block)
        for block in blocks
        if block.kind == "frontmatter"
    ]


def _comment_positions(
    text: str,
) -> list[tuple[str, int, str, int, int, bool, bool, int]]:
    """각 HTML 주석과 인접한 표시 줄 위치."""

    masked = mask_fenced_code_contents(text)
    positions: list[
        tuple[str, int, str, int, int, bool, bool, int]
    ] = []
    for start, end, body in html_comment_spans(masked):
        positions.append(_comment_position(masked, start, end, body))
    return positions


def _comment_position(
    text: str,
    start: int,
    end: int,
    body: str,
) -> tuple[str, int, str, int, int, bool, bool, int]:
    """단일 HTML 주석의 인접 표시 줄 위치 서명 생성.

    Args:
        text: fenced code를 가린 Markdown 문서.
        start: 주석 시작 offset.
        end: 주석 종료 offset.
        body: 주석 본문.

    Returns:
        본문·블록·배치·인용·들여쓰기·인접 본문 위치 서명.
    """

    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end < 0:
        line_end = len(text)
    prefix = text[line_start:start]
    suffix = text[end:line_end]
    standalone = bool(
        re.fullmatch(r"[ \t]*(?:>[ \t]*)*", prefix) and not suffix.strip()
    )
    prefix_blocks = _blocks(text[:start])
    physical_line = 0
    if not standalone and prefix_blocks:
        physical_line = sum(
            _has_markdown_hard_break(line)
            for line in prefix_blocks[-1].lines[:-1]
        )
    return (
        body,
        len(prefix_blocks),
        "standalone" if standalone else "inline",
        quote_depth(prefix) if standalone else 0,
        len(prefix) - len(prefix.lstrip(" \t")) if standalone else 0,
        bool(prefix.strip()) if not standalone else False,
        bool(suffix.strip()) if not standalone else False,
        physical_line,
    )


def _comment_position_matches(
    actual: tuple[str, int, str, int, int, bool, bool, int],
    expected: tuple[str, int, str, int, int, bool, bool, int],
) -> bool:
    """두 주석 위치가 같은 구조 경계를 가리키는지 여부."""

    return actual == expected


def _comment_records(text: str) -> list[tuple[str, int, int, int]]:
    """HTML 주석 본문과 원문 범위·줄 번호 기록."""

    line_starts = [0]
    line_starts.extend(
        match.end() for match in re.finditer(r"\n", text)
    )
    fenced_lines = _fenced_line_indexes(text)
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
        records.append((body, start_line, end_line, positions[position_index][1]))
        position_index += 1
    return records


def _fenced_line_indexes(text: str) -> set[int]:
    """fenced code block에 속한 물리 줄 위치 수집.

    Args:
        text: Markdown 문서.

    Returns:
        여닫는 fence를 포함한 0-based code 줄 위치.
    """

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
    return fenced_lines


def _matched_source_comment_indexes(
    text: str, source: str
) -> tuple[bool, set[int]]:
    """원문 작성 주석의 보존 여부와 응답에서 대응하는 주석 index 집합."""

    expected = _comment_positions(source)
    actual = _comment_positions(text)
    matched: set[int] = set()
    cursor = 0
    for source_comment in expected:
        while cursor < len(actual) and not _comment_position_matches(
            actual[cursor],
            source_comment,
        ):
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
    """구조 주석이 바로 다음 표시 줄을 소유하는지 여부."""

    next_line_index = end_line + 1
    if next_line_index >= len(lines):
        return False
    next_line = lines[next_line_index]
    if not next_line.strip():
        return False
    if _normalize_comment(next_line) == annotation:
        return True
    if annotation.lstrip().startswith(">"):
        return _quote_annotation_owns_line(
            annotation,
            next_line,
            lines,
            next_line_index,
            expected_quote_ordinal,
        )
    if annotation.lstrip().startswith("|"):
        return _table_annotation_owns_line(
            annotation,
            next_line,
            lines,
            next_line_index,
            expected_table_ordinal,
        )
    toc_match = _toc_annotation_owns_line(annotation, next_line)
    if toc_match is not None:
        return toc_match
    if is_structural_html_fragment(annotation):
        return _html_annotation_owns_lines(annotation, lines[next_line_index:])
    return _normalize_comment(next_line) == annotation


def _quote_annotation_owns_line(
    annotation: str,
    next_line: str,
    lines: list[str],
    next_line_index: int,
    expected_ordinal: int | None,
) -> bool:
    """인용 구조 annotation의 다음 줄 순번·깊이 검증.

    Args:
        annotation: 정규화된 인용 annotation.
        next_line: 바로 다음 표시 줄.
        lines: 응답 물리 줄.
        next_line_index: 다음 표시 줄 위치.
        expected_ordinal: 원문의 기대 인용 줄 순번.

    Returns:
        인용 줄 소유권 일치 여부.
    """

    actual_ordinal = sum(
        1
        for line in lines[: next_line_index + 1]
        if line.lstrip().startswith(">")
        and not _ONE_LINE_COMMENT_RE.fullmatch(line)
    ) - 1
    return bool(
        quote_depth(annotation) > 0
        and quote_depth(next_line) == quote_depth(annotation)
        and actual_ordinal == expected_ordinal
    )


def _table_annotation_owns_line(
    annotation: str,
    next_line: str,
    lines: list[str],
    next_line_index: int,
    expected_ordinal: int | None,
) -> bool:
    """표 구조 annotation의 다음 줄 순번·형태 검증.

    Args:
        annotation: 정규화된 표 annotation.
        next_line: 바로 다음 표시 줄.
        lines: 응답 물리 줄.
        next_line_index: 다음 표시 줄 위치.
        expected_ordinal: 원문의 기대 표 줄 순번.

    Returns:
        표 줄 소유권 일치 여부.
    """

    visible_lines = strip_html_comments(
        "\n".join(lines[: next_line_index + 1])
    ).splitlines()
    actual_ordinal = sum(
        1 for line in visible_lines if line.lstrip().startswith("|")
    ) - 1
    return bool(
        next_line.lstrip().startswith("|")
        and _table_line_signature(next_line) == _table_line_signature(annotation)
        and actual_ordinal == expected_ordinal
    )


def _toc_annotation_owns_line(annotation: str, next_line: str) -> bool | None:
    """목차 annotation의 목록 표식·anchor target 보존 판정.

    Args:
        annotation: 정규화된 목차 annotation.
        next_line: 바로 다음 표시 줄.

    Returns:
        목차라면 소유권 일치 여부, 아니면 ``None``.
    """

    source_toc = _UNORDERED_LIST_RE.match(annotation)
    translated_toc = _UNORDERED_LIST_RE.match(next_line)
    if not (source_toc and translated_toc and "](#" in annotation):
        return None
    return bool(
        source_toc.group(2) == translated_toc.group(2)
        and [link.target for link in markdown_links(annotation)]
        == [link.target for link in markdown_links(next_line)]
    )


def _html_annotation_owns_lines(annotation: str, following: list[str]) -> bool:
    """구조 HTML annotation과 뒤따르는 연속 HTML 줄 비교.

    Args:
        annotation: 정규화된 구조 HTML annotation.
        following: annotation 다음 물리 줄.

    Returns:
        구조 HTML token 순서 일치 여부.
    """

    expected = tuple(
        re.sub(r"\s+/>$", "/>", token)
        for token in _html_markup_signature(annotation)
    )
    actual_lines: list[str] = []
    for line in following:
        if not is_structural_html_fragment(line):
            break
        actual_lines.append(line)
        actual = tuple(
            re.sub(r"\s+/>$", "/>", token)
            for token in _html_markup_signature("\n".join(actual_lines))
        )
        if len(actual) >= len(expected):
            return actual == expected
    return False


@dataclass
class _StructuralAnnotationState:
    """원문 구조 annotation occurrence와 기대 순번 상태."""

    annotations: Counter[str]
    quote_ordinals: dict[str, list[int]]
    table_ordinals: dict[str, list[int]]
    consumed_quotes: Counter[str] = field(default_factory=Counter)
    consumed_tables: Counter[str] = field(default_factory=Counter)


def _structural_annotation_state(source: str) -> _StructuralAnnotationState:
    """원문의 구조 annotation occurrence와 인용·표 순번 구성.

    Args:
        source: 영어 원문.

    Returns:
        구조 annotation 검증 초기 상태.
    """

    annotations = Counter(
        normalized
        for line in strip_html_comments(_strip_code_blocks(source)).splitlines()
        if (normalized := _normalize_comment(line))
    )
    quote_ordinals: dict[str, list[int]] = {}
    table_ordinals: dict[str, list[int]] = {}
    quote_ordinal = 0
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
    return _StructuralAnnotationState(annotations, quote_ordinals, table_ordinals)


def _consume_structural_annotation(
    state: _StructuralAnnotationState,
    normalized: str,
) -> tuple[bool, int | None, int | None]:
    """구조 annotation occurrence와 기대 인용·표 순번 소비.

    Args:
        state: 남은 구조 annotation 상태.
        normalized: 정규화된 annotation 본문.

    Returns:
        소비 성공 여부와 기대 인용·표 순번.
    """

    if not state.annotations[normalized]:
        return False, None, None
    state.annotations[normalized] -= 1
    quote_ordinal = None
    table_ordinal = None
    if normalized.lstrip().startswith(">"):
        occurrence = state.consumed_quotes[normalized]
        values = state.quote_ordinals.get(normalized, [])
        if occurrence >= len(values):
            return False, None, None
        quote_ordinal = values[occurrence]
        state.consumed_quotes[normalized] += 1
    elif normalized.lstrip().startswith("|"):
        occurrence = state.consumed_tables[normalized]
        values = state.table_ordinals.get(normalized, [])
        if occurrence >= len(values):
            return False, None, None
        table_ordinal = values[occurrence]
        state.consumed_tables[normalized] += 1
    return True, quote_ordinal, table_ordinal


def _source_comments_are_preserved(text: str, source: str) -> bool:
    """원문 작성 HTML 주석의 순서와 구조 위치 보존 여부."""

    preserved, source_comment_indexes = _matched_source_comment_indexes(
        text, source
    )
    if not preserved:
        return False
    table_annotations = _required_table_comments(source)
    state = _structural_annotation_state(source)
    lines = text.splitlines()
    for index, (body, _start_line, end_line, _position) in enumerate(
        _comment_records(text)
    ):
        if index in source_comment_indexes:
            continue
        normalized = _normalize_comment(body)
        if not normalized:
            return False
        if normalized in table_annotations:
            continue
        if (
            is_non_annotatable_line(normalized)
            or is_structural_html_fragment(normalized)
        ):
            consumed, quote_ordinal, table_ordinal = _consume_structural_annotation(
                state,
                normalized,
            )
            if not consumed or not _structural_annotation_owns_next_line(
                normalized,
                end_line,
                lines,
                expected_quote_ordinal=quote_ordinal,
                expected_table_ordinal=table_ordinal,
            ):
                return False
    return True


def _list_layout(block: Block) -> tuple[int, int]:
    """목록 블록의 hard break 수와 연속 본문 줄 수."""

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
) -> bool:
    """문단 줄 수와 hard break 구조의 계약 충족 여부."""

    for source_block, translated_block in zip(
        source_blocks, translated_blocks, strict=False
    ):
        if not _block_layout_is_valid(source_block, translated_block):
            return False
    return True


def _prose_runs(block: Block) -> list[list[str]]:
    """블록에서 비교 가능한 연속 문단 줄 묶음 추출.

    Args:
        block: Markdown 소유 블록.

    Returns:
        참조 정의로 분리된 연속 문단 줄 묶음.
    """

    runs: list[list[str]] = []
    current: list[str] = []
    for line in block.lines:
        if is_reference_definition_line(line):
            if current:
                runs.append(current)
                current = []
            continue
        current.append(line)
    if current:
        runs.append(current)
    return runs


def _paragraph_runs_layout_is_valid(
    source_block: Block,
    translated_block: Block,
) -> bool:
    """대응 문단 run의 줄 수와 hard break 구조 검증.

    Args:
        source_block: 영어 원문 문단 블록.
        translated_block: locale 응답 문단 블록.

    Returns:
        모든 문단 run의 줄 구조 일치 여부.
    """

    source_runs = _prose_runs(source_block)
    translated_runs = _prose_runs(translated_block)
    if len(source_runs) != len(translated_runs):
        return False
    for source_run, translated_run in zip(source_runs, translated_runs, strict=True):
        source_breaks = sum(
            _has_markdown_hard_break(line) for line in source_run[:-1]
        )
        translated_breaks = sum(
            _has_markdown_hard_break(line) for line in translated_run[:-1]
        )
        if len(translated_run) != source_breaks + 1 or translated_breaks != source_breaks:
            return False
    return True


def _block_layout_is_valid(source_block: Block, translated_block: Block) -> bool:
    """대응 Markdown 블록의 줄 layout 계약 검증.

    Args:
        source_block: 영어 원문 블록.
        translated_block: locale 응답 블록.

    Returns:
        블록 유형별 줄 구조 일치 여부.
    """

    if source_block.kind != "text" or translated_block.kind != "text":
        return True
    if is_reference_definition_block("\n".join(source_block.lines)):
        return True
    source_kind = _text_kind(source_block.lines[0])
    translated_kind = _text_kind(translated_block.lines[0])
    if _is_legacy_pipe_table_block(source_block) and _is_legacy_pipe_table_block(
        translated_block
    ):
        return True
    if source_kind == "list" and translated_kind == "list":
        return _list_layout(source_block) == _list_layout(translated_block)
    if source_kind == "html" or translated_kind == "html":
        return bool(
            source_kind == translated_kind
            and len(source_block.lines) == len(translated_block.lines)
        )
    if source_kind != "paragraph" or translated_kind != "paragraph":
        return True
    return _paragraph_runs_layout_is_valid(source_block, translated_block)


def _sentence_count(text: str) -> int:
    """보호 markup을 제외한 문장의 보수적 개수."""

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
    """원문과 응답의 문장 수 차이가 허용 범위인지 여부."""

    source_capacity = _sentence_count(source_body) + len(
        _SOURCE_CLAUSE_SPLIT_RE.findall(source_body)
    )
    return _sentence_count(translated_body) <= source_capacity


def _paragraph_sentence_cardinality_is_valid(
    source: str,
    translated: str,
) -> bool:
    """모든 대응 문단의 문장 수 계약 충족 여부."""

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


def supports_feedback_retry(
    text: str,
    source: str,
    issues: list[str] | tuple[str, ...],
    *,
    live: bool = True,
) -> bool:
    """현재 응답 위반을 한 번의 feedback completion으로 복구 가능한지 여부.

    ``live``가 거짓인 결정적 profile은 언어·링크·inline code·원문 주석
    위반을 재요청하지 않는다.
    """

    issue_set = frozenset(issues)
    if live and issue_set & _FEEDBACK_RETRYABLE_ISSUES:
        return True

    source_blocks = _blocks(source)
    translated_blocks = _blocks(text)
    actual_annotations = _annotation_comments(text, source)
    required_annotations = _required_comments(source)

    # 주석만 있는 응답은 필수 형식을 시작했지만 본문이 누락된 상태
    # 추가 블록이나 주석은 요청한 원문 소유 범위 밖에 provider가 만든 출력
    if actual_annotations and len(translated_blocks) < len(source_blocks):
        return True
    if len(translated_blocks) > len(source_blocks):
        return True
    if len(actual_annotations) > len(required_annotations):
        return True

    if "provider sentence cardinality mismatch" not in issue_set:
        return False
    for source_block, translated_block in zip(
        source_blocks,
        translated_blocks,
        strict=False,
    ):
        if source_block.kind != "text" or translated_block.kind != "text":
            continue
        if (
            _text_kind(source_block.lines[0]) == "paragraph"
            and _text_kind(translated_block.lines[0]) == "paragraph"
            and not _sentence_cardinality_pair_is_valid(
                _normalized_body(source_block),
                _normalized_body(translated_block),
            )
        ):
            return True
    return False


def _paragraph_indentation_is_valid(
    source_blocks: list[Block], translated_blocks: list[Block]
) -> bool:
    """응답 문단에 code로 해석될 추가 들여쓰기가 없는지 여부."""

    def indented_as_code(line: str) -> bool:
        """문단 줄이 Markdown 들여쓰기 code로 바뀌었는지 여부."""

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
    """번역 가능한 표시 속성을 가린 HTML·JSX markup 서명."""

    body = strip_html_comments(_strip_code_blocks(text))
    return [_mask_display_attribute_values(tag) for tag in _markup_tokens(body)]


def _quoted_value_end(text: str, start: int) -> int:
    """따옴표 속성값의 닫는 구분자 다음 위치."""

    quote = text[start]
    cursor = start + 1
    while cursor < len(text):
        if text[cursor] == quote and not is_escaped(text, cursor):
            return cursor + 1
        cursor += 1
    return len(text)


def _braced_value_end(text: str, start: int) -> int:
    """중괄호 속성값의 닫는 구분자 다음 위치."""

    return balanced_expression_end(text, start) or len(text)


def _tag_attribute_value_spans(
    tag: str,
) -> tuple[tuple[str, int, int], ...]:
    """HTML·JSX tag에서 속성명과 값 범위 추출."""

    name = re.match(r"</?[A-Za-z][\w:.-]*", tag)
    if not name or tag.startswith("</"):
        return ()

    spans: list[tuple[str, int, int]] = []
    index = name.end()
    while index < len(tag):
        index, span, complete = _next_tag_attribute(tag, index)
        if complete:
            break
        if span is None:
            continue
        spans.append(span)
    return tuple(spans)


def _next_tag_attribute(
    tag: str,
    index: int,
) -> tuple[int, tuple[str, int, int] | None, bool]:
    """tag scanner의 다음 속성값 범위 추출.

    Args:
        tag: HTML·JSX tag token.
        index: 현재 scanner 위치.

    Returns:
        다음 위치, 속성값 범위, tag 종료 여부.
    """

    if tag.startswith("/>", index) or tag[index] == ">":
        return index, None, True
    if tag[index].isspace():
        return index + 1, None, False
    if tag[index] == "{":
        return _braced_value_end(tag, index), None, False
    attribute = re.match(r"[A-Za-z_:][\w:.-]*", tag[index:])
    if attribute is None:
        return index + 1, None, False
    name = attribute.group(0)
    cursor = _skip_whitespace(tag, index + attribute.end())
    if cursor >= len(tag) or tag[cursor] != "=":
        return cursor, None, False
    value_start = _skip_whitespace(tag, cursor + 1)
    if value_start >= len(tag):
        return value_start, None, True
    value_end = _attribute_value_end(tag, value_start)
    return value_end, (name, value_start, value_end), False


def _skip_whitespace(text: str, index: int) -> int:
    """지정 위치부터 이어지는 공백 다음 위치 반환.

    Args:
        text: 검색할 문자열.
        index: 검색 시작 위치.

    Returns:
        첫 비공백 문자 또는 문자열 끝 위치.
    """

    while index < len(text) and text[index].isspace():
        index += 1
    return index


def _attribute_value_end(tag: str, start: int) -> int:
    """HTML·JSX 속성값 종료 위치 탐색.

    Args:
        tag: HTML·JSX tag token.
        start: 속성값 시작 위치.

    Returns:
        속성값 바로 다음 위치.
    """

    if tag[start] in ("'", '"', "`"):
        return _quoted_value_end(tag, start)
    if tag[start] == "{":
        return _braced_value_end(tag, start)
    end = start
    while end < len(tag) and not tag[end].isspace() and tag[end] != ">":
        end += 1
    return end


def _pure_braced_display_string(value: str) -> bool:
    """중괄호 표시 속성값이 단일 문자열 literal인지 여부."""

    if not (value.startswith("{") and value.endswith("}")):
        return False
    inner = value[1:-1].strip()
    if len(inner) < 2 or inner[0] not in ("'", '"', "`"):
        return False
    if inner[0] == "`" and "${" in inner:
        return False
    return _quoted_value_end(inner, 0) == len(inner)


def _mask_js_expression_strings(expression: str) -> str:
    """최상위 ``+``로 연결된 JavaScript 문자열과 template literal 내용 마스킹."""

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
        """양끝 공백을 보존하며 JavaScript literal 내용 마스킹."""

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
    """번역 가능한 표시 문자열을 가린 속성값."""

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
    """tag에서 번역 가능한 표시 속성값 마스킹."""

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
    """동적 표시 속성의 속성명과 보호 식 서명."""

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
    """보존 여부를 비교할 inline markup token 목록."""

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

        end = _markup_token_end(text, start)
        if end is None:
            tokens.append(_UNPARSED_MARKUP_PREFIX + text[start:])
            break
        tokens.append(text[start:end])
        index = max(end, start + 1)
    return tokens


def _markup_token_end(text: str, start: int) -> int | None:
    """HTML·JSX markup token의 닫는 ``>`` 다음 위치 탐색.

    Args:
        text: markup을 포함한 문서.
        start: 여는 ``<`` 위치.

    Returns:
        닫는 구분자 다음 위치. 구문이 닫히지 않으면 ``None``.
    """

    cursor = start + 1
    while cursor < len(text):
        char = text[cursor]
        if char in ("'", '"', "`"):
            end = _quoted_value_end(text, cursor)
            if end == len(text) and (
                text[-1] != char or is_escaped(text, len(text) - 1)
            ):
                return None
            cursor = end
            continue
        if char == "{":
            end = balanced_expression_end(text, cursor)
            if end is None:
                return None
            cursor = end
            continue
        if char == ">":
            return cursor + 1
        cursor += 1
    return None


def _term_like(token: str) -> bool:
    """token이 번역 제외 기술 용어 형태인지 여부."""

    lowered = token.lower()
    return bool(
        lowered in _LOWERCASE_TECH_TERMS
        or token.isupper()
        or token[:1].isupper()
        or any(char.isdigit() for char in token)
        or any(char.isupper() for char in token[1:])
    )


def _distinctive_technical_term(token: str) -> bool:
    """token이 일반 산문과 구별되는 기술 식별자인지 여부."""

    return bool(
        token.lower() in _LOWERCASE_TECH_TERMS
        or token.isupper()
        or any(char.isdigit() for char in token)
        or any(char.isupper() for char in token[1:])
    )


def _is_inline_code_only_list_item(body: str) -> bool:
    """목록 항목이 code 식별자만 포함하는지 여부."""

    if not (inline_code_contents(body) or html_code_contents(body)):
        return False
    remainder = strip_html_code_elements(strip_inline_code(body))
    return not remainder.strip(_PROSE_TRIM_CHARACTERS)


def _version_item_end_positions(text: str, start: int) -> list[int]:
    """단일 버전 항목이 끝날 수 있는 위치 목록."""

    token = _VERSION_TOKEN_RE.match(text, start)
    if token is None:
        return []
    token_end = token.end()
    ends = [token_end]
    label = _VERSION_LABEL_RE.match(text, token_end)
    if label is not None:
        ends.extend(
            separator.start()
            for separator in _VERSION_SEPARATOR_RE.finditer(
                text,
                token_end,
                label.end(),
            )
        )
        ends.append(label.end())
    return ends


def _is_version_value(text: str) -> bool:
    """버전·edition 목록을 backtracking 없이 판별."""

    prefix = _VERSION_CORE_PREFIX_RE.match(text)
    pending = [prefix.end() if prefix is not None else 0]
    visited: set[int] = set()
    while pending:
        start = pending.pop()
        if start in visited:
            continue
        visited.add(start)
        for end in _version_item_end_positions(text, start):
            if end == len(text):
                return True
            separator = _VERSION_SEPARATOR_RE.match(text, end)
            if separator is not None and separator.end() not in visited:
                pending.append(separator.end())
    return False


def _legacy_pipe_table_rows(
    text: str,
) -> list[tuple[bool, list[str]]]:
    """legacy pipe table의 구분 행 여부와 행별 셀 목록."""

    return [
        (_table_line_signature(line)[0] == "separator", table_row_cells(line))
        for line in text.splitlines()
    ]


def _legacy_pipe_cell_is_protected(
    cell: str, *, header: str | None = None
) -> bool:
    """legacy 표 셀이 번역 제외 데이터인지 여부."""

    if inline_code_contents(cell) and not strip_inline_code(cell).strip(
        _PROSE_TRIM_CHARACTERS
    ):
        return True
    if markdown_links(cell) and not strip_markdown_links(cell).strip(
        _PROSE_TRIM_CHARACTERS
    ):
        return True
    visible = strip_inline_code(cell).strip(_MARKDOWN_TRIM_CHARACTERS)
    if _HTML_ENTITY_RE.fullmatch(visible):
        return True
    visible = visible.strip(".,:;")
    if (
        _is_version_value(visible)
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
    words = re.findall(_PROTECTED_WORD_PATTERN, visible)
    if len(words) == 1 and words[0] == visible:
        return (
            words[0].lower() in _PRODUCT_NAME_PREFIXES
            or _distinctive_technical_term(words[0])
        )
    return _is_protected_source_phrase(visible)


def _legacy_pipe_table_prose_roles(
    text: str, *, translate_headers: bool
) -> list[list[bool] | None]:
    """legacy 표의 각 셀에 대한 산문·보호 데이터 역할."""

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
                    and _unicode_letter_count(
                        _normalized_language_prose(cell)
                    )
                    > 0
                    for cell in cells
                ]
            )
        else:
            roles.append(_legacy_data_row_roles(cells, headers))
        content_index += 1
    return roles


def _legacy_data_row_roles(cells: list[str], headers: list[str]) -> list[bool]:
    """legacy 표 데이터 행의 셀별 산문 여부 판정.

    Args:
        cells: 데이터 행 셀.
        headers: 원문 머리글 셀.

    Returns:
        셀별 번역 가능 산문 여부.
    """

    return [
        _unicode_letter_count(_normalized_language_prose(cell)) > 0
        and not _legacy_pipe_cell_is_protected(
            cell,
            header=headers[column] if column < len(headers) else None,
        )
        for column, cell in enumerate(cells)
    ]


def legacy_pipe_table_contains_prose(
    text: str, *, include_headers: bool = True
) -> bool:
    """legacy pipe table에 번역 가능한 산문 셀이 있는지 여부."""

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
    """legacy 표의 산문 셀이 원문 그대로 남았는지 여부."""

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
    """legacy 표의 구조·보호 셀·번역 산문 계약 충족 여부."""

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
    for source_row, translated_row, row_roles in zip(
        source_rows, translated_rows, roles, strict=True
    ):
        row_result = _legacy_pipe_row_contract(
            source_row,
            translated_row,
            row_roles,
            locale,
        )
        row_shape, row_protected, row_target = row_result
        shape_valid = shape_valid and row_shape
        protected_valid = protected_valid and row_protected
        target_valid = target_valid and row_target
    return shape_valid, protected_valid, target_valid


def _legacy_pipe_row_contract(
    source_row: tuple[bool, list[str]],
    translated_row: tuple[bool, list[str]],
    roles: list[bool] | None,
    locale: str | None,
) -> tuple[bool, bool, bool]:
    """legacy 표의 단일 행 구조·보호 셀·언어 계약 검증.

    Args:
        source_row: 원문 구분 행 여부와 셀.
        translated_row: 응답 구분 행 여부와 셀.
        roles: 셀별 산문 여부. 구분 행이면 ``None``.
        locale: 목표 locale 또는 언어 검사를 생략하는 ``None``.

    Returns:
        행 구조, 보호 셀, 목표 언어 유효 여부.
    """

    source_separator, source_cells = source_row
    translated_separator, translated_cells = translated_row
    if (
        source_separator != translated_separator
        or len(source_cells) != len(translated_cells)
    ):
        return False, True, True
    if source_separator:
        return source_cells == translated_cells, True, True
    if roles is None:
        return False, True, True
    protected_valid = True
    target_valid = True
    for source_cell, translated_cell, prose in zip(
        source_cells, translated_cells, roles, strict=True
    ):
        if not prose:
            protected_valid = protected_valid and source_cell == translated_cell
        elif locale is not None and not _table_cell_language_is_valid(
            source_cell,
            translated_cell,
            locale,
            header=None,
            is_data_cell=True,
        ):
            target_valid = False
    return True, protected_valid, target_valid


def _is_protected_source_phrase(text: str) -> bool:
    """문구 전체가 번역 제외 기술 데이터인지 여부."""

    if _is_legacy_pipe_table_text(text):
        return not legacy_pipe_table_contains_prose(text)
    if _ENV_ASSIGNMENT_RE.fullmatch(text.strip(_MARKDOWN_TRIM_CHARACTERS)):
        return True
    words = re.findall(_PROTECTED_WORD_PATTERN, text)
    if not words:
        return False
    remainder = re.sub(_PROTECTED_WORD_PATTERN, "", text)
    if remainder.strip(_PROSE_TRIM_CHARACTERS):
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
    """번역 결과에 보호 대상이 아닌 원문 문구가 남았는지 여부."""

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
        and not _is_protected_source_phrase(source)
    )


def _language_sample(text: str) -> str:
    """언어 판정에서 보호 markup을 제거한 표본."""

    text = strip_html_comments(text)
    # heading과 GFM admonition marker는 번역 대상이 아니므로 표본에서 제외.
    text = "\n".join(
        _QUOTED_ADMONITION_MARKER_RE.sub(r"\1", line, count=1)
        for line in text.splitlines()
        if not is_heading_line(line)
    )
    text = strip_html_code_elements(text)
    text = strip_inline_code(text)
    text = strip_markdown_links(text)
    text = _AUTOLINK_RE.sub("", text)
    text = _URL_RE.sub("", text)
    text = _TAG_RE.sub("", text)
    return _HTML_ENTITY_RE.sub("", text)


def _normalized_language_prose(text: str) -> str:
    """exact-copy 비교용으로 NFC 정규화한 산문."""

    return unicodedata.normalize(
        "NFC", _language_sample(text).replace("\r\n", "\n")
    ).strip()


def _unicode_letter_count(text: str) -> int:
    """NFC 정규화 후 Unicode 15.1 Letter code point 수."""

    return sum(
        _is_unicode_15_1_letter(char)
        for char in unicodedata.normalize("NFC", text)
    )


def _is_unicode_15_1_letter(char: str) -> bool:
    """문자가 Unicode 15.1의 Letter 범주인지 여부."""

    if not unicodedata.category(char).startswith("L"):
        return False
    codepoint = ord(char)
    return not any(
        start <= codepoint <= end
        for start, end in _POST_UNICODE_15_1_LETTER_RANGES
    )


def _target_script_count(text: str, locale: str) -> int:
    """로캘에 해당하는 문자 체계의 code point 수."""

    def belongs(char: str) -> bool:
        """문자가 현재 로캘의 허용 문자 범위에 속하는지 여부."""

        if not _is_unicode_15_1_letter(char):
            return False
        name = unicodedata.name(char, "")
        if locale == "ko":
            return name.startswith(("HANGUL ", "HALFWIDTH HANGUL "))
        return (
            "HIRAGANA" in name
            or "KATAKANA" in name
            or name.startswith("CJK UNIFIED IDEOGRAPH-")
            or name.startswith("CJK COMPATIBILITY IDEOGRAPH-")
        )

    return sum(belongs(char) for char in text)


def _inline_markup_is_subset(
    actual: tuple[str, ...],
    expected: tuple[str, ...],
) -> bool:
    """응답 강조 구분자가 원문 구분자의 부분 multiset인지 여부.

    목표 언어가 강조를 어휘로 흡수하는 누락은 허용하고,
    원문에 없는 강조 추가는 거부한다.
    """

    return not (Counter(actual) - Counter(expected))


def _inline_markup_signature(text: str) -> tuple[str, ...]:
    """번역 중 보존해야 할 inline markup 순서 서명."""

    body = strip_html_comments(_strip_code_blocks(text))
    body = strip_inline_code(body)
    delimiters: list[str] = []
    index = 0
    while index < len(body):
        run = _inline_delimiter_run(body, index)
        if run is None:
            index += 1
            continue
        token, index, significant = run
        if significant:
            delimiters.append(token)
    return tuple(delimiters)


def _inline_delimiter_run(
    body: str,
    index: int,
) -> tuple[str, int, bool] | None:
    """inline 강조 구분자 run과 의미 여부 판정.

    Args:
        body: code를 제거한 Markdown 본문.
        index: 현재 문자 위치.

    Returns:
        구분자, 다음 위치, 구조 구분자 여부. 대상이 아니면 ``None``.
    """

    marker = body[index]
    if marker not in "*_~" or is_escaped(body, index):
        return None
    end = index + 1
    while end < len(body) and body[end] == marker:
        end += 1
    flanking = _delimiter_flanking(body, index, end)
    left_flanking, right_flanking, previous_punctuation, following_punctuation = (
        flanking
    )
    if marker == "_":
        can_open = left_flanking and (not right_flanking or previous_punctuation)
        can_close = right_flanking and (not left_flanking or following_punctuation)
    else:
        can_open = left_flanking
        can_close = right_flanking
    token = body[index:end]
    significant = (marker != "~" or len(token) >= 2) and (can_open or can_close)
    return token, end, significant


def _delimiter_flanking(
    body: str,
    start: int,
    end: int,
) -> tuple[bool, bool, bool, bool]:
    """Markdown delimiter run의 좌우 flanking 상태 계산.

    Args:
        body: code를 제거한 Markdown 본문.
        start: delimiter 시작 위치.
        end: delimiter 종료 위치.

    Returns:
        좌측·우측 flanking과 이전·다음 문자의 문장부호 여부.
    """

    previous = body[start - 1] if start else "\n"
    following = body[end] if end < len(body) else "\n"
    previous_punctuation = bool(re.match(r"[^\w\s]", previous))
    following_punctuation = bool(re.match(r"[^\w\s]", following))
    left_flanking = not following.isspace() and (
        not following_punctuation or previous.isspace() or previous_punctuation
    )
    right_flanking = not previous.isspace() and (
        not previous_punctuation or following.isspace() or following_punctuation
    )
    return (
        left_flanking,
        right_flanking,
        previous_punctuation,
        following_punctuation,
    )


def _table_rows(block: Block) -> list[str]:
    """표 블록에서 비어 있지 않은 행 목록."""

    rows: list[str] = []
    for line in block.lines:
        if _table_line_signature(line)[0] == "separator":
            continue
        rows.append(" ".join(table_row_cells(line)))
    return rows


def _markdown_link_signatures(
    text: str,
) -> tuple[
    Counter[str],
    list[str],
    tuple[tuple[str, tuple[str, ...]], ...],
    list[tuple[str, str, str]],
]:
    """Markdown 링크 target 횟수, 비이미지 label·(label, target) 쌍 multiset과 전체 title 순서 서명.

    label·쌍·title은 정렬된 multiset으로 비교해 목표 언어 어순에 따른
    블록 내 등장 순서 재배열을 허용하되, 같은 label이 반복되면
    그 label의 target 등장 순서는 보존해야 한다.
    """

    body = mask_reference_definitions(
        strip_html_comments(_strip_code_blocks(text))
    )
    links = markdown_links(body)
    autolinks = markdown_autolinks(body)
    ordered_pairs = sorted(
        (
            (link.start, link.label, link.target)
            for link in links
            if not link.image
        ),
        key=lambda item: item[0],
    )
    ordered_pairs.extend(
        (link.start, link.label, link.target) for link in autolinks
    )
    ordered_pairs.sort(key=lambda item: item[0])
    per_label_targets: dict[str, list[str]] = {}
    for _start, label, target in ordered_pairs:
        per_label_targets.setdefault(label, []).append(target)
    return (
        Counter(
            [link.target for link in links]
            + [link.target for link in autolinks]
        ),
        sorted(label for _start, label, _target in ordered_pairs),
        tuple(
            sorted(
                (label, tuple(targets))
                for label, targets in per_label_targets.items()
            )
        ),
        sorted(
            ("" if link.image else link.label, link.target, link.title)
            for link in links
            if link.title
        ),
    )


def _markdown_image_signatures(text: str) -> list[tuple[str, str]]:
    """Markdown 이미지의 target·title 순서 서명."""

    body = mask_reference_definitions(
        strip_html_comments(_strip_code_blocks(text))
    )
    return [
        (link.target, link.title)
        for link in markdown_links(body)
        if link.image
    ]


def _mixed_image_order(text: str) -> tuple[str, ...]:
    """Markdown 이미지와 HTML img tag의 혼합 출현 순서."""

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
    """reference 정의의 정규화 label·target·title 순서 서명."""

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
    """표 셀 데이터의 번역 처리 유형."""

    body = text.strip(_MARKDOWN_TRIM_CHARACTERS)
    data_cell = header is not None
    if data_cell and _DATE_VALUE_RE.fullmatch(body):
        return "localizable"
    if data_cell and (
        _is_version_value(body)
        or _CONFIG_VALUE_RE.fullmatch(body)
        or _PARENTHESIZED_LITERAL_RE.fullmatch(body)
    ):
        return "invariant"
    words = re.findall(_PROTECTED_WORD_PATTERN, body)
    remainder = re.sub(_PROTECTED_WORD_PATTERN, "", body)
    if _strict_technical_terms(words) and not remainder.strip(
        " &/,+.:-0123456789()[]*"
    ):
        return "invariant"
    if not data_cell:
        return None
    header_terms = _normalized_header_terms(header or "")
    identifier_kind = _identifier_cell_kind(body, header_terms)
    if identifier_kind is not None:
        return identifier_kind
    if _product_cell_is_invariant(words, remainder, header_terms):
        return "invariant"
    return None


def _strict_technical_terms(words: list[str]) -> bool:
    """모든 단어가 엄격한 기술 식별자 형태인지 판정.

    Args:
        words: 표 셀에서 추출한 ASCII token.

    Returns:
        하나 이상의 token이 모두 기술 식별자인지 여부.
    """

    return bool(words) and all(
        word.lower() in _LOWERCASE_TECH_TERMS
        or word.isupper()
        or any(char.isdigit() for char in word)
        or any(char.isupper() for char in word[1:])
        for word in words
    )


def _normalized_header_terms(header: str) -> set[str]:
    """표 머리글 단어와 단순 단수형 후보 수집.

    Args:
        header: 원문 표 머리글.

    Returns:
        소문자 머리글 term 집합.
    """

    terms: set[str] = set()
    for word in re.findall(r"[A-Za-z]+", header):
        lowered = word.lower()
        terms.add(lowered)
        if lowered.endswith("ies"):
            terms.add(lowered[:-3] + "y")
        elif lowered.endswith("sses"):
            terms.add(lowered[:-2])
        elif lowered.endswith("s"):
            terms.add(lowered[:-1])
    return terms


def _identifier_cell_kind(body: str, header_terms: set[str]) -> str | None:
    """식별자 계열 머리글의 scalar 셀 처리 유형 결정.

    Args:
        body: 표 셀 본문.
        header_terms: 정규화된 머리글 term.

    Returns:
        ``localizable``, ``invariant`` 또는 대상이 아닌 ``None``.
    """

    if not header_terms & _IDENTIFIER_HEADER_TERMS:
        return None
    scalar_list = bool(
        header_terms & _IDENTIFIER_LIST_HEADER_TERMS
        and _SCALAR_LIST_RE.fullmatch(body)
    )
    scalar_token = bool(_SCALAR_TOKEN_RE.fullmatch(body) and body[:1].islower())
    if not (scalar_list or scalar_token):
        return None
    return "localizable" if "type" in header_terms else "invariant"


def _product_cell_is_invariant(
    words: list[str],
    remainder: str,
    header_terms: set[str],
) -> bool:
    """제품 계열 머리글의 셀이 고유 이름인지 판정.

    Args:
        words: 표 셀에서 추출한 ASCII token.
        remainder: 기술 token 제거 후 남은 본문.
        header_terms: 정규화된 머리글 term.

    Returns:
        번역하지 않는 제품 이름 여부.
    """

    product_headers = header_terms & _PRODUCT_HEADER_TERMS
    if not product_headers:
        return False
    generic_feature = bool(
        product_headers == {"feature"}
        and len(words) == 1
        and words[0].lower() not in _PRODUCT_NAME_PREFIXES
        and not _distinctive_technical_term(words[0])
    )
    return bool(
        not generic_feature
        and words
        and not remainder.strip(" &/,+.:-0123456789()")
        and all(word[:1].isupper() or _term_like(word) for word in words)
    )


def _protected_cell_matches(source: str, translated: str) -> bool:
    """보호 표 셀이 원문과 동일한 의미 단위를 유지하는지 여부."""

    if _PROTECTED_CELL_TOKEN_RE.findall(source) != _PROTECTED_CELL_TOKEN_RE.findall(
        translated
    ):
        return False
    remainder = _PROTECTED_CELL_TOKEN_RE.sub("", translated)
    return not any(char.isalnum() for char in remainder)


def _table_language_is_valid(
    source_block: Block, translated_block: Block, locale: str
) -> bool:
    """표의 산문 셀이 로캘별 언어 기준을 충족하는지 여부."""

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
    source_headers = table_row_cells(source_lines[0]) if source_lines else []
    # 구분자가 없는 행 단위 요청에는 머리글 행이 없으므로 머리글 규칙을 적용하지 않음.
    has_header_row = any(
        _table_line_signature(line)[0] == "separator"
        for line in source_block.lines
    )
    for row_index, (source_line, translated_line) in enumerate(
        zip(source_lines, translated_lines, strict=False)
    ):
        source_cells = table_row_cells(source_line)
        translated_cells = table_row_cells(translated_line)
        for column, (source_cell, translated_cell) in enumerate(
            zip(source_cells, translated_cells, strict=False)
        ):
            header = source_headers[column] if column < len(source_headers) else None
            if not _table_cell_language_is_valid(
                source_cell,
                translated_cell,
                locale,
                header=header if row_index > 0 else None,
                is_data_cell=row_index > 0 or not has_header_row,
            ):
                return False
    return True


def _table_cell_language_is_valid(
    source: str,
    translated: str,
    locale: str,
    *,
    header: str | None,
    is_data_cell: bool,
) -> bool:
    """단일 표 셀의 보호 데이터 또는 목표 언어 계약 검증.

    Args:
        source: 영어 원문 셀.
        translated: locale 응답 셀.
        locale: 목표 locale.
        header: 데이터 행의 원문 머리글. 머리글 행이면 ``None``.
        is_data_cell: 머리글 이외의 데이터 행 여부.

    Returns:
        셀 언어 계약 충족 여부.
    """

    protected_kind = None
    if is_data_cell:
        protected_kind = _protected_cell_kind(
            _language_sample(source),
            header=header,
        )
    if protected_kind is None:
        if is_data_cell and _cell_has_no_translatable_prose(source):
            return True
        if not is_data_cell and _cell_echoes_translatable_prose(source, translated):
            return False
        return _has_target_language(translated, locale, source_text=source)
    if _protected_cell_matches(source, translated):
        return True
    if protected_kind == "invariant":
        return True
    return _has_target_language(translated, locale, source_text=source)


def _cell_echoes_translatable_prose(source: str, translated: str) -> bool:
    """머리글 셀이 번역 가능한 산문을 그대로 반복했는지 여부.

    머리글은 코퍼스 규약상 번역 대상이므로, 길이 하한과 무관하게
    번역 가능한 단어를 그대로 되돌려준 응답을 거부한다.
    """

    sample = _normalized_language_prose(source)
    if sample != _normalized_language_prose(translated):
        return False
    return any(
        _unicode_letter_count(word) >= 2
        and not _distinctive_technical_term(word)
        and word.lower() not in _PROSE_SIGNAL_WORDS
        for word in sample.split()
    )


def _cell_has_no_translatable_prose(source: str) -> bool:
    """셀이 보호 항목 나열뿐이라 목표 언어 판정이 무의미한지 여부.

    구분자로 나뉜 항목이 둘 이상이고 각 항목이 보호 토큰 하나일 때만 데이터 열거로 본다.
    설명 문구는 항목 하나에 토큰이 여러 개이므로 여기에 해당하지 않는다.
    """

    words = re.findall(_PROTECTED_WORD_PATTERN, source)
    if len(words) < 2:
        return False
    remainder = re.sub(_PROTECTED_WORD_PATTERN, "", source)
    if remainder.strip(_PROSE_TRIM_CHARACTERS):
        return False
    if {word.lower() for word in words} & _PROSE_SIGNAL_WORDS:
        return False
    items = [
        item.strip()
        for item in _DATA_ITEM_SEPARATOR_RE.split(source)
        if item.strip(_PROSE_TRIM_CHARACTERS)
    ]
    return len(items) >= 2 and all(
        len(re.findall(_PROTECTED_WORD_PATTERN, item)) == 1 for item in items
    )


def _has_target_language(
    text: str,
    locale: str,
    *,
    source_text: str,
    is_list: bool = False,
) -> bool:
    """번역 산문이 로캘별 exact-copy와 문자 수 기준을 충족하는지 여부."""

    source_sample = _normalized_language_prose(source_text)
    sample = _normalized_language_prose(text)
    source_letter_count = _unicode_letter_count(source_sample)
    if source_letter_count >= 20 and sample == source_sample:
        if _is_quoted_literal_data(source_sample):
            return True
        identifier_tokens = [
            word
            for word in source_sample.split()
            if _unicode_letter_count(word)
        ]
        if identifier_tokens and all(
            not word[:1].isupper() and _distinctive_technical_term(word)
            for word in identifier_tokens
        ):
            return True
        return False
    if source_letter_count < 40 or _is_label_and_data_list(source_sample):
        return True
    # 열거 항목의 고유명사·식별자와 정의 목록의 label은 데이터이므로 하한 계산에서 제외.
    basis = _enumeration_prose_letter_count(source_sample) if is_list else None
    if basis is None:
        remainder = _definition_list_remainder(source_sample)
        basis = (
            source_letter_count
            if remainder is None
            else _unicode_letter_count(remainder)
        )
    if basis < 40:
        return True
    required = max(8, math.ceil(basis * 0.10))
    return _target_script_count(sample, locale) >= required


def _is_quoted_literal_data(source_sample: str) -> bool:
    """모든 문자가 따옴표 리터럴 안에 있고 밖은 JSON 구조 문장부호뿐인지 여부."""

    remainder = _QUOTED_LITERAL_RE.sub(" ", source_sample)
    if _unicode_letter_count(remainder):
        return False
    return not remainder.strip(_JSON_STRUCTURE_CHARACTERS) and any(
        char in remainder for char in ":{}[]"
    )


def _enumeration_prose_letter_count(source_sample: str) -> int | None:
    """목록 항목 중 번역 대상 산문 토큰의 문자 수.

    목록 marker를 제거한 언어 표본은 항목 하나가 한 줄이다.
    항목이 세 개 미만이면 열거로 보지 않고 ``None`` 반환.
    """

    items = [
        item
        for item in source_sample.splitlines()
        if _unicode_letter_count(item)
    ]
    if len(items) < 3:
        return None
    return sum(
        _unicode_letter_count(token)
        for item in items
        for token in item.split()
        if not _enumeration_token_is_protected(token)
    )


def _enumeration_token_is_protected(token: str) -> bool:
    """열거 항목 토큰이 고유명사·식별자·버전이라 번역되지 않는지 여부."""

    word = token.strip(_PROSE_TRIM_CHARACTERS)
    return not word or word[:1].isupper() or _distinctive_technical_term(word)


def _definition_list_remainder(source_sample: str) -> str | None:
    """모든 항목이 짧은 `label:` 접두를 가진 정의 목록의 label 제외 본문.

    정의 목록이 아니면 ``None``을 반환한다.
    """

    lines = [line.strip() for line in source_sample.splitlines() if line.strip()]
    if len(lines) < 2:
        return None
    remainders: list[str] = []
    for line in lines:
        marker = _UNORDERED_LIST_RE.match(line) or _ORDERED_LIST_RE.match(line)
        item = marker.group(marker.re.groups) if marker else line
        label, separator, rest = item.partition(":")
        if not separator or _unicode_letter_count(label) >= 20:
            return None
        remainders.append(rest)
    return " ".join(remainders)


def _is_label_and_data_list(source_sample: str) -> bool:
    """짧은 label과 보호 데이터 목록만으로 구성된 블록인지 여부.

    표의 data cell과 같은 취급으로, 번역 대상 산문이 exact-copy 하한
    미만인 데이터 열거 블록에는 목표 문자 하한을 적용하지 않는다.
    """

    label, separator, remainder = source_sample.partition(":")
    if not separator or _unicode_letter_count(label) >= 20:
        return False
    items = [item.strip() for item in re.split(r",|\band\b", remainder)]
    items = [item for item in items if _unicode_letter_count(item)]
    if len(items) < 2:
        return False
    return all(
        all(
            word[:1].isupper() or _distinctive_technical_term(word)
            for word in item.split()
            if _unicode_letter_count(word)
        )
        for item in items
    )


def _annotation_owner_kind(
    annotation: str,
    table_annotations: frozenset[str],
) -> str:
    """원문 주석 본문이 나타내는 소유 블록 유형."""

    if annotation in table_annotations:
        return "table"
    if is_heading_line(annotation):
        return "heading"
    if _UNORDERED_LIST_RE.match(annotation) or _ORDERED_LIST_RE.match(annotation):
        return "list"
    return "paragraph"


def _following_owner_kind(
    body: str,
    *,
    table_expected: bool,
    allow_indented: bool = True,
) -> str:
    """주석 다음 표시 블록의 소유 유형."""

    indentation = len(body) - len(body.lstrip(" \t"))
    content = body.lstrip()
    while content.startswith(">"):
        content = content[1:].lstrip()
    if (
        fence_token(body)
        or is_named_anchor_line(body)
        or is_structural_html_line(body)
        or content == "---"
    ):
        return "nonannotatable"
    if is_heading_line(content):
        return "heading"
    if table_expected and "|" in content:
        return "table"

    list_kind = _following_list_owner_kind(content)
    if list_kind is not None:
        return list_kind
    if is_non_annotatable_line(content):
        return "nonannotatable"
    if not allow_indented and (body.startswith("\t") or indentation >= 4):
        return "nonannotatable"
    return "paragraph"


def _following_list_owner_kind(content: str) -> str | None:
    """표시 줄이 번역 가능 목록인지 판정.

    Args:
        content: 인용 표식을 제거한 표시 줄.

    Returns:
        ``list``, ``nonannotatable`` 또는 목록이 아닌 ``None``.
    """

    marker = _UNORDERED_LIST_RE.match(content) or _ORDERED_LIST_RE.match(content)
    if marker is None:
        return None
    item_body = marker.group(marker.lastindex or 0)
    checkbox = _TASK_CHECKBOX_RE.match(item_body)
    if checkbox:
        item_body = item_body[checkbox.end() :]
    if is_non_annotatable_line(content) or _is_inline_code_only_list_item(item_body):
        return "nonannotatable"
    return "list"


def _response_annotation_records(
    text: str,
    source: str,
) -> tuple[
    list[tuple[str, int, int, str]],
    list[tuple[str, int, int, str]],
] | None:
    """응답의 필수·선택적 annotation 소유권 record 추출.

    Args:
        text: provider 응답.
        source: 영어 원문.

    Returns:
        필수·선택적 annotation record. 배치가 잘못되면 ``None``.
    """

    table_annotations = _required_table_comments(source)
    optional = _optional_quoted_comments(source)
    _preserved, source_indexes = _matched_source_comment_indexes(text, source)
    lines = text.splitlines()
    annotations: list[tuple[str, int, int, str]] = []
    optional_annotations: list[tuple[str, int, int, str]] = []
    for occurrence, (body, start, end, _position) in enumerate(
        _comment_records(text)
    ):
        if occurrence in source_indexes:
            continue
        normalized = _normalize_comment(body)
        if not _is_owned_annotation(normalized, table_annotations):
            continue
        match = _ONE_LINE_COMMENT_RE.fullmatch(lines[start]) if start == end else None
        if match is None:
            return None
        prefix = match.group(1)
        depth = quote_depth(prefix)
        record = (normalized, end, depth, prefix)
        key = (normalized, depth, _quote_block_ordinal(lines, start + 1))
        if (
            depth > 0
            and _optional_quote_annotation_starts_block(lines, start)
            and optional[key]
        ):
            optional[key] -= 1
            optional_annotations.append(record)
        else:
            annotations.append(record)
    return annotations, optional_annotations


def _is_owned_annotation(
    normalized: str,
    table_annotations: frozenset[str],
) -> bool:
    """주석 본문이 블록 소유권 검증 대상 annotation인지 판정.

    Args:
        normalized: 정규화된 주석 본문.
        table_annotations: 필수 표 annotation 집합.

    Returns:
        소유권 검증 대상 여부.
    """

    return bool(
        normalized
        and not (
            is_non_annotatable_line(normalized)
            and normalized not in table_annotations
        )
        and not is_structural_html_fragment(normalized)
    )


def _annotation_record_owns_following(
    record: tuple[str, int, int, str],
    lines: list[str],
    table_annotations: frozenset[str],
) -> bool:
    """단일 annotation record의 다음 블록 소유권 검증.

    Args:
        record: 본문·끝 줄·인용 깊이·접두사 record.
        lines: 응답 물리 줄.
        table_annotations: 필수 표 annotation 집합.

    Returns:
        위치·들여쓰기·블록 유형 일치 여부.
    """

    annotation, index, depth, prefix = record
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
    if quote_depth(body) != depth:
        return False
    if depth > 0 and indentation != len(body) - len(body.lstrip(" \t")):
        return False
    expected_kind = _annotation_owner_kind(annotation, table_annotations)
    if _following_owner_kind(
        body,
        table_expected=expected_kind == "table",
    ) != expected_kind:
        return False
    return _annotation_heading_is_valid(annotation, body)


def _annotation_heading_is_valid(annotation: str, body: str) -> bool:
    """annotation과 소유 블록의 제목 보존 여부 검증.

    Args:
        annotation: 정규화된 원문 annotation.
        body: annotation 다음 표시 줄.

    Returns:
        제목이 아니거나 제목 내용이 정확히 보존됐는지 여부.
    """

    if not is_heading_line(annotation):
        return not is_heading_line(body)
    heading = body.lstrip()
    while heading.startswith(">"):
        heading = heading[1:].lstrip()
    return strip_title_attr_line(heading) == strip_title_attr_line(annotation)


def _annotation_ownership_is_valid(text: str, source: str) -> bool:
    """각 annotation이 대응 원문과 올바른 블록을 소유하는지 여부."""

    expected = _required_comments(source)
    table_annotations = _required_table_comments(source)
    lines = text.splitlines()
    records = _response_annotation_records(text, source)
    if records is None:
        return False
    annotations, optional_annotations = records
    if [
        annotation for annotation, _index, _depth, _prefix in annotations
    ] != expected:
        return False
    return all(
        _annotation_record_owns_following(record, lines, table_annotations)
        for record in annotations + optional_annotations
    )


def _provider_structure_issues(
    text: str,
    source: str,
    source_blocks: list[Block],
    translated_blocks: list[Block],
) -> list[str]:
    """provider 응답의 문서·markup 구조 이슈 수집.

    Args:
        text: provider 응답.
        source: 영어 원문.
        source_blocks: 원문 소유 블록.
        translated_blocks: 응답 소유 블록.

    Returns:
        발견 순서의 구조 위반 label.
    """

    description = front_matter_description(text)
    source_html_body = strip_html_comments(_strip_code_blocks(source))
    translated_html_body = strip_html_comments(_strip_code_blocks(text))
    checks = (
        (has_malformed_html_comment_delimiters(text), "provider malformed HTML comment"),
        (
            _required_comments(source) != _annotation_comments(text, source)
            and not _table_annotation_omitted(text, source),
            "provider original comment mismatch",
        ),
        (
            _normalized_fenced_code_blocks(source)
            != _normalized_fenced_code_blocks(text),
            "provider code block mismatch",
        ),
        (
            admonition_types(source) != admonition_types(text),
            "provider admonition type mismatch",
        ),
        (
            list(map(_signature, source_blocks))
            != list(map(_signature, translated_blocks)),
            "provider block signature mismatch",
        ),
        (
            _markdown_structure_signature(source)
            != _markdown_structure_signature(text),
            "provider markdown structure mismatch",
        ),
        (
            not _paragraph_indentation_is_valid(source_blocks, translated_blocks),
            "provider paragraph indentation mismatch",
        ),
        (
            not _paragraph_layout_is_valid(source_blocks, translated_blocks),
            "provider paragraph layout mismatch",
        ),
        (
            not _paragraph_sentence_cardinality_is_valid(source, text),
            "provider sentence cardinality mismatch",
        ),
        (description is not None and not description.valid, "provider front matter invalid"),
        (
            _front_matter_signature(source_blocks)
            != _front_matter_signature(translated_blocks),
            "provider front matter mismatch",
        ),
        (
            _html_markup_signature(source) != _html_markup_signature(text),
            "provider HTML markup mismatch",
        ),
        (
            html_code_contents(source_html_body)
            != html_code_contents(translated_html_body),
            "provider HTML code mismatch",
        ),
        (
            not _inline_markup_is_subset(
                _inline_markup_signature(text),
                _inline_markup_signature(source),
            ),
            "provider inline markup mismatch",
        ),
    )
    return [label for failed, label in checks if failed]


def _append_provider_issue_once(issues: list[str], issue: str) -> None:
    """provider 검증 이슈를 중복 없이 추가.

    Args:
        issues: 발견 순서대로 누적 중인 이슈 목록.
        issue: 추가할 이슈 label.
    """

    if issue not in issues:
        issues.append(issue)


def _provider_inline_link_issues(text: str, source: str) -> list[str]:
    """provider 응답의 inline 링크·이미지 보존 이슈 수집.

    Args:
        text: provider 응답.
        source: 영어 원문.

    Returns:
        발견 순서의 inline 링크 위반 label.
    """

    expected = _markdown_link_signatures(source)
    actual = _markdown_link_signatures(text)
    labels = (
        _PROVIDER_LINK_TARGET_MISMATCH,
        _PROVIDER_LINK_LABEL_MISMATCH,
        _PROVIDER_LINK_PAIR_MISMATCH,
        _PROVIDER_LINK_TITLE_MISMATCH,
    )
    issues = [
        issue
        for expected_value, actual_value, issue in zip(
            expected,
            actual,
            labels,
            strict=True,
        )
        if expected_value != actual_value
    ]
    expected_images = _markdown_image_signatures(source)
    actual_images = _markdown_image_signatures(text)
    if [target for target, _title in expected_images] != [
        target for target, _title in actual_images
    ]:
        _append_provider_issue_once(issues, _PROVIDER_LINK_TARGET_MISMATCH)
    if [title for _target, title in expected_images] != [
        title for _target, title in actual_images
    ]:
        _append_provider_issue_once(issues, _PROVIDER_LINK_TITLE_MISMATCH)
    if _mixed_image_order(source) != _mixed_image_order(text):
        _append_provider_issue_once(issues, _PROVIDER_LINK_TARGET_MISMATCH)
    return issues


def _provider_definition_link_issues(text: str, source: str) -> list[str]:
    """provider 응답의 참조 정의 보존 이슈 수집.

    Args:
        text: provider 응답.
        source: 영어 원문.

    Returns:
        발견 순서의 참조 정의 위반 label.
    """

    expected = _reference_definition_signatures(source)
    actual = _reference_definition_signatures(text)
    issues: list[str] = []
    for expected_value, actual_value, issue in zip(
        expected[:3],
        actual[:3],
        (
            _PROVIDER_LINK_TARGET_MISMATCH,
            _PROVIDER_LINK_LABEL_MISMATCH,
            _PROVIDER_LINK_PAIR_MISMATCH,
        ),
        strict=True,
    ):
        if expected_value != actual_value:
            issues.append(issue)
    if expected[2] == actual[2] and expected[3] != actual[3]:
        issues.append(_PROVIDER_LINK_TITLE_MISMATCH)
    return issues


def _provider_reference_link_issues(text: str, source: str) -> list[str]:
    """provider 응답의 참조 링크 사용부 보존 이슈 수집.

    Args:
        text: provider 응답.
        source: 영어 원문.

    Returns:
        발견 순서의 참조 링크 위반 label.
    """

    expected = reference_link_signatures(source)
    actual = reference_link_signatures(text)
    issues: list[str] = []
    if reference_link_display_signatures(source) != reference_link_display_signatures(
        text
    ):
        issues.append(_PROVIDER_LINK_LABEL_MISMATCH)
    if tuple((image, target) for image, target, _title in expected) != tuple(
        (image, target) for image, target, _title in actual
    ):
        issues.append(_PROVIDER_LINK_TARGET_MISMATCH)
    if tuple(title for _image, _target, title in expected) != tuple(
        title for _image, _target, title in actual
    ):
        issues.append(_PROVIDER_LINK_TITLE_MISMATCH)
    return issues


def _provider_link_issues(text: str, source: str) -> list[str]:
    """provider 응답의 모든 Markdown 링크 이슈를 중복 없이 수집.

    Args:
        text: provider 응답.
        source: 영어 원문.

    Returns:
        발견 순서의 링크 위반 label.
    """

    issues = _provider_inline_link_issues(text, source)
    for group in (
        _provider_definition_link_issues(text, source),
        _provider_reference_link_issues(text, source),
    ):
        for issue in group:
            _append_provider_issue_once(issues, issue)
    return issues


def provider_inline_code_contents(text: str) -> list[str]:
    """Provider 응답 계약에서 비교하는 표시 영역의 inline code 목록."""

    return inline_code_contents(strip_html_comments(_strip_code_blocks(text)))


def _provider_comment_issues(text: str, source: str) -> list[str]:
    """provider 응답의 inline code·주석 소유권 이슈 수집.

    Args:
        text: provider 응답.
        source: 영어 원문.

    Returns:
        발견 순서의 code·주석 위반 label.
    """

    source_code = Counter(provider_inline_code_contents(source))
    translated_code = Counter(provider_inline_code_contents(text))
    checks = (
        (source_code != translated_code, "provider inline code mismatch"),
        (
            not _source_comments_are_preserved(text, source),
            "provider source comment mismatch",
        ),
        (
            not _annotation_ownership_is_valid(text, source)
            and not _table_annotation_omitted(text, source),
            "provider annotation ownership mismatch",
        ),
    )
    return [label for failed, label in checks if failed]


def _table_annotation_omitted(text: str, source: str) -> bool:
    """표로만 구성된 요청에서 선택적 표 annotation이 생략됐는지 여부.

    표 annotation은 적용 위치 판정 보조용 선택 표현이며, 최종 canonical
    annotation은 후처리가 현재 표 전체 원문으로 재생성한다.
    """

    if "<!--" in text:
        return False
    source_lines = [line.strip() for line in source.splitlines() if line.strip()]
    return is_gfm_pipe_table(source) or bool(
        source_lines
        and all(line.startswith("|") and line.endswith("|") for line in source_lines)
    )


def _provider_table_block_result(
    source_block: Block,
    translated_block: Block,
    locale: str | None,
) -> tuple[list[str], bool]:
    """일반 Markdown 표 블록의 행 중복·목표 언어 결과 수집.

    Args:
        source_block: 영어 원문 표 블록.
        translated_block: provider 응답 표 블록.
        locale: 목표 locale 또는 언어 검사를 생략하는 ``None``.

    Returns:
        표 이슈와 목표 언어 누락 여부.
    """

    expected_rows = _table_rows(source_block)
    actual_rows = _table_rows(translated_block)
    issues: list[str] = []
    if len(expected_rows) == len(set(expected_rows)) and len(actual_rows) != len(
        set(actual_rows)
    ):
        issues.append("provider duplicate table row")
    language_missing = bool(
        locale is not None
        and not _table_language_is_valid(source_block, translated_block, locale)
    )
    return issues, language_missing


def _provider_legacy_table_result(
    source_block: Block,
    translated_block: Block,
    locale: str | None,
) -> tuple[list[str], bool]:
    """legacy pipe 표의 구조·보호 셀·목표 언어 결과 수집.

    Args:
        source_block: 영어 원문 legacy 표 블록.
        translated_block: provider 응답 legacy 표 블록.
        locale: 목표 locale 또는 언어 검사를 생략하는 ``None``.

    Returns:
        표 이슈와 목표 언어 누락 여부.
    """

    shape, protected, target = _legacy_pipe_table_contract(
        "\n".join(source_block.lines),
        "\n".join(translated_block.lines),
        locale,
    )
    issues: list[str] = []
    if not shape:
        issues.append("provider markdown structure mismatch")
    if not protected:
        issues.append(_PROVIDER_PROTECTED_TERM_MISMATCH)
    return issues, not target


def _provider_block_pair_result(
    source_block: Block,
    translated_block: Block,
    locale: str | None,
) -> tuple[list[str], bool]:
    """대응 소유 블록의 보호 내용·목표 언어 결과 수집.

    Args:
        source_block: 영어 원문 소유 블록.
        translated_block: provider 응답 소유 블록.
        locale: 목표 locale 또는 언어 검사를 생략하는 ``None``.

    Returns:
        블록 이슈와 목표 언어 누락 여부.
    """

    if source_block.kind != "text" or translated_block.kind != "text":
        return [], False
    if _is_toc_link_list(source_block):
        return [], False
    if is_reference_definition_block("\n".join(source_block.lines)):
        return [], False
    source_body = _normalized_body(source_block)
    translated_body = _normalized_body(translated_block)
    source_kind = _text_kind(source_block.lines[0])
    if source_kind == "table":
        return _provider_table_block_result(source_block, translated_block, locale)
    if _is_indented_literal_block(source_block):
        return (
            [_PROVIDER_PROTECTED_TERM_MISMATCH]
            if translated_body != source_body
            else [],
            False,
        )
    if _is_legacy_pipe_table_block(source_block):
        return _provider_legacy_table_result(source_block, translated_block, locale)
    if all(is_reference_definition_line(line) for line in source_block.lines):
        return [], False
    if _is_inline_code_only_list_item(source_body):
        return (
            [_PROVIDER_PROTECTED_TERM_MISMATCH]
            if translated_body != source_body
            else [],
            False,
        )
    language_missing = bool(
        locale is not None
        and source_kind in ("paragraph", "list", "quote", "html")
        and not _has_target_language(
            _block_language_text(translated_block),
            locale,
            source_text=_block_language_text(source_block),
            is_list=source_kind == "list",
        )
    )
    return [], language_missing


def _provider_block_issues(
    source_blocks: list[Block],
    translated_blocks: list[Block],
    locale: str | None,
) -> list[str]:
    """모든 대응 소유 블록의 보호 내용·목표 언어 이슈 수집.

    Args:
        source_blocks: 영어 원문 소유 블록.
        translated_blocks: provider 응답 소유 블록.
        locale: 목표 locale 또는 언어 검사를 생략하는 ``None``.

    Returns:
        발견 순서의 블록 위반 label.
    """

    issues: list[str] = []
    target_language_missing = False
    for source_block, translated_block in zip(
        source_blocks,
        translated_blocks,
        strict=False,
    ):
        block_issues, language_missing = _provider_block_pair_result(
            source_block,
            translated_block,
            locale,
        )
        issues.extend(block_issues)
        target_language_missing = target_language_missing or language_missing
    if target_language_missing:
        issues.append("provider target language mismatch")
    return issues


def verify(
    text: str,
    source: str,
    *,
    locale: str | None = None,
    contract_version: int = RESPONSE_CONTRACT_VERSION,
) -> list[str]:
    """단일 신규 provider 응답의 결정적 위반 목록."""

    if contract_version != RESPONSE_CONTRACT_VERSION:
        raise ValueError(
            f"unsupported response contract version: {contract_version}"
        )
    if locale is not None and locale not in _TARGET_LOCALES:
        raise ValueError(f"unsupported response locale: {locale}")

    source_blocks = _blocks(source)
    translated_blocks = _blocks(text)
    issues = _provider_structure_issues(
        text,
        source,
        source_blocks,
        translated_blocks,
    )
    issues.extend(_provider_link_issues(text, source))
    issues.extend(_provider_comment_issues(text, source))
    issues.extend(_provider_block_issues(source_blocks, translated_blocks, locale))
    return issues


def _identity_source_lines(source: str) -> list[tuple[int, str]]:
    """원본의 물리적 줄 번호를 포함한 fenced code block 외부 원문 줄."""

    visible: list[tuple[int, str]] = []
    in_code = False
    fence = ""
    for index, line in enumerate(source.splitlines()):
        token = fence_token(line)
        if token:
            if not in_code:
                in_code = True
                fence = token
                continue
            if closes_fence(line, fence):
                in_code = False
                fence = ""
                continue
        if not in_code:
            visible.append((index, line))
    return visible


def identity_source_view(source: str, version: str) -> str:
    """provider 원문에 응답 단계 version 치환만 적용."""

    if not isinstance(source, str):
        raise TypeError("identity source must be text")
    validate_version_token(version)

    output: list[str] = []
    pending: list[str] = []
    in_code = False
    fence = ""

    def flush_pending() -> None:
        """누적된 identity 원문 줄을 출력 목록에 확정."""

        if pending:
            output.append(replace_version("".join(pending), version))
            pending.clear()

    for line in source.splitlines(keepends=True):
        token = fence_token(line)
        if token:
            if not in_code:
                flush_pending()
                in_code = True
                fence = token
                output.append(line)
                continue
            if closes_fence(line, fence):
                in_code = False
                fence = ""
                output.append(line)
                continue

        if in_code:
            output.append(line)
        else:
            pending.append(line)

    flush_pending()
    return "".join(output)


def _canonical_identity_comment(text: str) -> str:
    """identity 블록의 canonical HTML 주석 생성.

    Args:
        text: 정규화된 원문 annotation.

    Returns:
        닫는 구분자를 escape한 한 줄 HTML 주석.
    """

    escaped = text.replace("*/", "*&#47;").replace("-->", "--&gt;")
    return f"<!-- {escaped} -->"


@dataclass
class _IdentityAnnotationBuilder:
    """identity 응답에 삽입할 annotation 누적 상태."""

    inserts: dict[int, list[str]] = field(default_factory=dict)
    paragraph: list[str] = field(default_factory=list)
    paragraph_start: int | None = None
    paragraph_kind: str | None = None

    def flush(self) -> None:
        """누적 identity 문단을 canonical 주석으로 확정."""

        if self.paragraph:
            combined = " ".join(self.paragraph)
            if not is_structural_html_fragment(combined):
                normalized = _normalize_comment(combined)
                if normalized and self.paragraph_start is not None:
                    self.add(self.paragraph_start, normalized)
            self.paragraph.clear()
        self.paragraph_start = None
        self.paragraph_kind = None

    def add(self, index: int, content: str) -> None:
        """지정 원문 줄 앞에 canonical 주석 추가.

        Args:
            index: 원문 물리 줄 위치.
            content: 정규화된 annotation 본문.
        """

        self.inserts.setdefault(index, []).append(
            _canonical_identity_comment(content)
        )

    def append(self, kind: str, text: str, index: int) -> None:
        """같은 유형의 identity 문단 본문 누적.

        Args:
            kind: 번역 소유 블록 유형.
            text: canonical 원문 조각.
            index: 원문 물리 줄 위치.
        """

        if self.paragraph_kind not in (None, kind):
            self.flush()
        if self.paragraph_start is None:
            self.paragraph_start = index
        self.paragraph_kind = kind
        self.paragraph.append(text)

    def consume(self, action: str, content: str, index: int) -> None:
        """원문 줄 처리 종류를 identity annotation 상태에 반영.

        Args:
            action: ``skip``, ``flush``, ``table``, ``heading`` 또는 ``paragraph``.
            content: canonical 주석 또는 문단 본문.
            index: 원문 물리 줄 위치.
        """

        if action == "skip":
            return
        if action == "paragraph":
            self.append("paragraph", content, index)
            return
        self.flush()
        if action in ("table", "heading"):
            normalized = _normalize_comment(content)
            if normalized:
                self.add(index, normalized)


def _render_identity_lines(
    source_view: str,
    inserts: dict[int, list[str]],
) -> str:
    """원문 물리 줄 앞에 준비된 identity 주석 삽입.

    Args:
        source_view: version 치환이 끝난 영어 원문.
        inserts: 원문 물리 줄별 canonical 주석.

    Returns:
        원래 줄바꿈을 보존한 identity 응답.
    """

    output: list[str] = []
    for index, line in enumerate(source_view.splitlines(keepends=True)):
        ending = "\r\n" if line.endswith("\r\n") else "\n"
        output.extend(comment + ending for comment in inserts.get(index, ()))
        output.append(line)
    return "".join(output)


def render_identity_response(source: str, version: str) -> str:
    """전처리된 단일 owner block의 결정적 테스트 Markdown 렌더링.

    fenced code 외부의 version placeholder를 렌더링되지 않은 요청 metadata로 해석한 뒤 필수 pipeline annotation 삽입.
    restore map 확장과 stale-link 정규화는 후처리 단계가 계속 소유.
    """

    source_view = identity_source_view(source, version)
    if has_malformed_html_comment_delimiters(source_view):
        raise ValueError("identity source contains malformed HTML comments")

    indexed_lines = _identity_source_lines(source_view)
    visible_text = "\n".join(line for _index, line in indexed_lines)
    source_comment_lines = standalone_html_comment_line_numbers(visible_text)
    reference_lines = reference_definition_line_numbers(visible_text)
    table_comments, table_member_lines = _table_owner_spans(visible_text)
    builder = _IdentityAnnotationBuilder()
    in_front_matter = False

    for visible_index, (original_index, line) in enumerate(indexed_lines):
        action, in_front_matter, content = _annotation_line_action(
            line,
            visible_index,
            in_front_matter=in_front_matter,
            source_comment_lines=source_comment_lines,
            reference_lines=reference_lines,
            table_comments=table_comments,
            table_member_lines=table_member_lines,
        )
        builder.consume(action, content, original_index)

    builder.flush()
    rendered = _render_identity_lines(source_view, builder.inserts)

    issues = verify(rendered, source_view, locale=None)
    if issues:
        raise ValueError("identity source cannot satisfy the response contract")
    return rendered
