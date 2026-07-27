"""문서·번역 검증 (Python). translation-sync/docs/04.

문서·번역 콘텐츠 검증은 Python으로 처리한다.
Docusaurus 빌드 산출물 검증은 JS validate-anchors.mjs가 담당한다.

최종 문서에 남으면 안 되는 잔존 패턴을 검사하고 위반 목록을 반환한다(빈 목록 = success).
"""
from __future__ import annotations

import re
from collections import Counter

from ..annotation.annotate import split_blocks
from ..common.markdown import (
    closes_fence,
    fence_token,
    front_matter_description,
    has_malformed_html_comment_delimiters,
    has_title_attr_line,
    inline_code_contents,
    html_comment_bodies,
    html_comment_spans,
    html_code_contents,
    is_heading_line,
    is_non_annotatable_line,
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
    strip_html_code_elements,
    strip_title_attr_line,
    strip_html_comments,
    strip_inline_code,
)
from ..postprocessing.postprocess import admonition_types, img_self_closing
from .response_contract import (
    _comment_records as _response_comment_records,
    _comment_positions as _response_comment_positions,
    _dynamic_display_attribute_signatures,
    _html_markup_signature,
    _markup_tokens,
    _mixed_image_order,
    _optional_quote_annotation_starts_block,
    _optional_quoted_comments,
    _quote_block_ordinal,
    _sentence_cardinality_pair_is_valid,
    _table_line_signature,
    _UNPARSED_MARKUP_PREFIX,
    contains_untranslated_source_phrase,
)

# 코드 블록 밖에서 남으면 안 되는 패턴 (docs/04 §14)
_FORBIDDEN = {
    "unreplaced {{version}}": re.compile(r"\{\{\s*version\s*\}\}"),
    "unrestored base64 placeholder": re.compile(r"__BASE64_IMAGE_\d+__"),
    "legacy note marker": re.compile(
        r"^>\s*(?:"
        r"\{(?:note|tip|warning|caution|important|참고|注意|注)\}"
        r"|\*\*(?:note|tip|warning|caution|important|참고|注意|注)(?::\*\*|\*\*:?)"
        r"|(?:note|tip|warning|caution|important|참고|注意|注):"
        r")",
        re.MULTILINE | re.IGNORECASE,
    ),
}
_ONE_LINE_COMMENT_RE = re.compile(
    r"^([ \t]*(?:>[ \t]*)*)<!--[ \t]*(.*?)[ \t]*-->[ \t]*$"
)
_TABLE_BOUNDARY_TAG_RE = re.compile(
    r"^[ \t]*</?table(?:[ \t][^>]*)?>[ \t]*$",
    re.IGNORECASE,
)

_AUTOLINK_RE = re.compile(r"<(https?://[^>\s]+)>")
_URI_SCHEME_RE = re.compile(
    r"^[a-z][a-z0-9+.-]*:",
    re.IGNORECASE,
)
_INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
_ANCHOR_TAG_RE = re.compile(r"<a\b[^>]*\bname=[\"'][^\"']+[\"'][^>]*>", re.IGNORECASE)
_IGNORED_ANCHOR_ATTR_RE = (
    r"(?:\bname=[\"'][^\"']+[\"']"
    r"|\bdata-translation-alias\s*=\s*[\"']true[\"'])"
)
_IGNORED_EMPTY_ANCHOR_RE = re.compile(
    rf"<a\b(?=[^>]*{_IGNORED_ANCHOR_ATTR_RE})[^>]*>\s*</a>", re.IGNORECASE
)
_IGNORED_ANCHOR_OPEN_RE = re.compile(
    rf"<a\b(?=[^>]*{_IGNORED_ANCHOR_ATTR_RE})[^>]*>", re.IGNORECASE
)
_ANCHOR_NAME_RE = re.compile(
    r"(?<!\S)name\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE
)
_HTML_TAG_NAME_RE = re.compile(r"<\s*(/?)\s*([A-Za-z][\w:.-]*)")
_HTML_IMG_SRC_RE = re.compile(
    r"""(?<!\S)src\s*=\s*(?:"([^"]*)"|'([^']*)'|(\{(?:[^{}]|\{[^{}]*\})*\})|([^\s>]+))""",
    re.IGNORECASE,
)
_HEADING_LINE_RE = re.compile(r"^[ \t]*#{1,6}\s.*$", re.MULTILINE)
_DOCS_PREFIX_RE = re.compile(
    r"^/docs/(?P<version>[^/#?]+)(?=/|#|\?|$)/?"
)
_LARAVEL_DOCS_PREFIX_RE = re.compile(
    r"^https://laravel\.com/docs/(?P<version>master|\d+\.x)(?=/|#|\?|$)/?"
)
_ADMONITION_RE = re.compile(
    r"^>\s*\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT)]\s*$", re.IGNORECASE
)
_LIST_MARKER_RE = re.compile(r"^[ \t]*[-*+][ \t]+\S", re.MULTILINE)
_STALE_LINK_TARGETS = {
    "#agents-integration": "#agent-integration",
    "#method-array-sort-recursive-desc": "#method-array-sort-recursive",
    "controllers#actions-handled-by-resource-controller": "controllers#actions-handled-by-resource-controllers",
    "#actions-handled-by-resource-controller": "#actions-handled-by-resource-controllers",
    "database-testing#writing-factories": "database-testing#defining-model-factories",
    "eloquent-mutators##date-casting": "eloquent-mutators#date-casting",
    "errors#logging": "logging",
    "helpers#fluent-strings": "strings#fluent-strings",
    "migrations#writing-migrations": "migrations#creating-tables",
    "##date-casting": "#date-casting",
}
_VERSION_SCOPED_STALE_TARGETS = {
    "controllers#actions-handled-by-resource-controller",
    "#actions-handled-by-resource-controller",
    "helpers#fluent-strings",
}
_LEGACY_VERSION_STALE_LINK_TARGETS = {
    "controllers#actions-handled-by-resource-controllers": "controllers#actions-handled-by-resource-controller",
    "#actions-handled-by-resource-controllers": "#actions-handled-by-resource-controller",
    "strings#fluent-strings": "helpers#fluent-strings",
}
_LEGACY_STALE_LINK_VERSIONS = {"8.x", "9.x"}
_V13_AGENT_REVERSE_TARGET = {"#agent-integration": "#agents-integration"}
_EXCLUDED_LINK_TARGETS = {
    "#assert-similar-json",
    "#formatting-shortcode-notifications",
}


def _strip_heading_lines(text: str) -> str:
    """heading 라인 제거.

    heading 텍스트 자체는 `_heading_lines`에서 원문과 비교한다. 여기서는 heading에
    포함된 인라인 코드/링크가 본문 비교에서 한 번 더 계산되지 않도록 제외한다.
    """
    return _HEADING_LINE_RE.sub("", text)


def _strip_code_blocks(text: str) -> str:
    """fenced code block을 제거해 코드 예시 안의 패턴을 검사 대상에서 뺀다."""
    out: list[str] = []
    in_code = False
    fence = ""
    for line in text.split("\n"):
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
    return "\n".join(out)


def _strip_comments(text: str) -> str:
    return strip_html_comments(text)


def _fenced_code_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    in_code = False
    fence = ""
    cur: list[str] = []
    for line in text.splitlines(keepends=True):
        token = fence_token(line)
        if token:
            if not in_code:
                in_code, fence = True, token
                cur = [line]
                continue
            if closes_fence(line, fence):
                cur.append(line)
                blocks.append("".join(cur))
                in_code = False
                cur = []
                continue
        if in_code:
            cur.append(line)
    if in_code:
        blocks.append("".join(cur))
    return blocks


def _normalized_fenced_code_blocks(text: str) -> list[str]:
    return [
        "\n".join(line.rstrip(" \t") for line in block.rstrip("\n").split("\n"))
        for block in _fenced_code_blocks(text)
    ]


def _link_targets(text: str, version: str | None = None) -> Counter[str]:
    body = mask_reference_definitions(
        _strip_heading_lines(_strip_code_blocks(_strip_comments(text)))
    )
    targets = [link.target for link in markdown_links(body)]
    targets += _AUTOLINK_RE.findall(body)
    normalized = (
        _comparable_link_target(target, version=version) for target in targets
    )
    return Counter(target for target in normalized if target is not None)


def _link_labels(text: str, version: str | None = None) -> list[str]:
    body = mask_reference_definitions(
        _strip_code_blocks(_strip_comments(text))
    )
    return [
        " ".join(link.label.split())
        for link in markdown_links(body)
        if not link.image
        and _comparable_link_target(link.target, version=version) is not None
    ]


def _link_pairs(
    text: str, version: str | None = None
) -> Counter[tuple[str, str]]:
    body = mask_reference_definitions(
        _strip_heading_lines(_strip_code_blocks(_strip_comments(text)))
    )
    pairs: list[tuple[str, str]] = []
    for link in markdown_links(body):
        target = _comparable_link_target(link.target, version=version)
        if not link.image and target is not None:
            pairs.append((" ".join(link.label.split()), target))
    for autolink in _AUTOLINK_RE.findall(body):
        target = _comparable_link_target(autolink, version=version)
        if target is not None:
            pairs.append((autolink, target))
    return Counter(pairs)


def _link_titles(text: str, version: str | None = None) -> list[str]:
    body = mask_reference_definitions(
        _strip_heading_lines(_strip_code_blocks(_strip_comments(text)))
    )
    return [
        link.title
        for link in markdown_links(body)
        if _comparable_link_target(link.target, version=version) is not None
    ]


def _image_signatures(
    text: str, version: str | None = None
) -> list[tuple[str, str]]:
    body = mask_reference_definitions(
        _strip_heading_lines(_strip_code_blocks(_strip_comments(text)))
    )
    signatures: list[tuple[str, str]] = []
    for link in markdown_links(body):
        target = _comparable_link_target(link.target, version=version)
        if link.image and target is not None:
            signatures.append((target, link.title))
    return signatures


def _reference_definition_signatures(
    text: str, version: str | None = None
) -> tuple[
    tuple[str, ...],
    tuple[str, ...],
    tuple[tuple[str, str], ...],
    tuple[tuple[str, str, str], ...],
]:
    definitions = [
        (
            definition.label,
            definition.target,
            definition.title,
        )
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


def _normalize_stale_link_target(target: str, version: str | None) -> str:
    if version == "13.x":
        if target in _V13_AGENT_REVERSE_TARGET:
            return _V13_AGENT_REVERSE_TARGET[target]
        if target == "#agents-integration":
            return target
    if version in _LEGACY_STALE_LINK_VERSIONS:
        if target in _LEGACY_VERSION_STALE_LINK_TARGETS:
            return _LEGACY_VERSION_STALE_LINK_TARGETS[target]
        if target in _VERSION_SCOPED_STALE_TARGETS:
            return target
    return _STALE_LINK_TARGETS.get(target, target)


def _normalize_link_target(target: str, version: str | None = None) -> str:
    laravel_match = _LARAVEL_DOCS_PREFIX_RE.match(target)
    if laravel_match and laravel_match.group("version") == version:
        remainder = target[laravel_match.end() :]
        if remainder and remainder[0] not in "/#?":
            target = remainder
    if _URI_SCHEME_RE.match(target):
        return target

    docs_match = _DOCS_PREFIX_RE.match(target)
    if docs_match and docs_match.group("version") == version:
        remainder = target[docs_match.end() :]
        if remainder and remainder[0] not in "/#?":
            target = remainder

    if target.startswith("./"):
        remainder = target[2:]
        if (
            remainder
            and remainder[0] not in "/#?"
            and not _URI_SCHEME_RE.match(remainder)
        ):
            target = remainder

    return _normalize_stale_link_target(target, version)


def _comparable_link_target(
    target: str, version: str | None = None
) -> str | None:
    normalized = _normalize_link_target(target, version=version)
    return None if normalized in _EXCLUDED_LINK_TARGETS else normalized


def _inline_codes(text: str) -> Counter[str]:
    body = _strip_heading_lines(_strip_code_blocks(_strip_comments(text)))
    return Counter(inline_code_contents(body))


def _anchors(text: str) -> Counter[str]:
    body = _strip_code_blocks(_strip_comments(text))
    anchors: list[str] = []
    for tag in _ANCHOR_TAG_RE.findall(body):
        if re.search(r"\bdata-translation-alias\s*=\s*[\"']true[\"']", tag, re.IGNORECASE):
            continue
        match = _ANCHOR_NAME_RE.search(tag)
        if match:
            anchors.append(match.group(1))
    return Counter(anchors)


def _structural_html_signature(text: str) -> list[str]:
    body = _strip_code_blocks(_strip_comments(text))
    body = _IGNORED_EMPTY_ANCHOR_RE.sub("", body)
    body = _IGNORED_ANCHOR_OPEN_RE.sub("", body)
    signature: list[str] = []
    for tag in _markup_tokens(body):
        if tag.startswith(_UNPARSED_MARKUP_PREFIX):
            signature.append(tag)
            continue
        match = _HTML_TAG_NAME_RE.match(tag)
        if match:
            slash, name = match.groups()
            signature.append(f"<{slash}{name.lower()}>")
    return signature


def _html_img_sources(text: str) -> tuple[str | None, ...]:
    body = _strip_code_blocks(_strip_comments(text))
    sources: list[str | None] = []
    for tag in _markup_tokens(body):
        name_match = _HTML_TAG_NAME_RE.match(tag)
        if name_match is None or name_match.group(2).lower() != "img":
            continue
        source_match = _HTML_IMG_SRC_RE.search(tag)
        if source_match is None:
            sources.append(None)
            continue
        sources.append(
            next(group for group in source_match.groups() if group is not None)
        )
    return tuple(sources)


def _heading_levels(text: str) -> list[int]:
    body = _strip_code_blocks(_strip_comments(text))
    levels: list[int] = []
    for line in body.splitlines():
        stripped = line.lstrip()
        level = len(stripped) - len(stripped.lstrip("#"))
        if 1 <= level <= 6 and len(stripped) > level and stripped[level].isspace():
            levels.append(level)
    return levels


def _heading_lines(text: str) -> list[str]:
    body = _strip_code_blocks(_strip_comments(text))
    headings: list[str] = []
    for line in body.splitlines():
        if is_heading_line(line):
            headings.append(strip_title_attr_line(line).strip())
    return headings


def _front_matter_title(text: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            return None
        if not stripped or stripped.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key.strip() != "title":
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        return value
    return None


def _plain_prose_bodies(text: str) -> list[str]:
    blocks = split_blocks(
        mask_reference_definitions(
            _strip_comments(_strip_code_blocks(text))
        ).splitlines()
    )
    bodies: list[str] = []
    for block in blocks:
        if block.kind != "text" or not block.lines:
            continue
        first = block.lines[0].lstrip()
        bare_links = all(
            len(links := markdown_links(line.strip())) == 1
            and links[0].start == 0
            and links[0].end == len(line.strip())
            for line in block.lines
        )
        identifier_links = all(
            (
                len(links := markdown_links(line.strip())) == 1
                and links[0].start == 0
                and links[0].end == len(line.strip())
            )
            or (
                bool(inline_code_contents(line.strip()))
                and not strip_inline_code(line.strip()).strip(
                    " `*_~.,:;()[]&/,+"
                )
            )
            for line in block.lines
        )
        indented_literal = all(
            line.startswith("\t") or len(line) - len(line.lstrip(" ")) >= 4
            for line in block.lines
        )
        legacy_pipe_table = (
            len(block.lines) >= 2
            and all("|" in line for line in block.lines)
            and any(
                re.fullmatch(
                    r"\s*:?-{3,}:?(?:\s*\|\s*:?-{3,}:?)+\s*",
                    line,
                )
                for line in block.lines
            )
        )
        block_text = "\n".join(block.lines)
        inline_code_only = bool(inline_code_contents(block_text)) and not (
            strip_inline_code(block_text).strip(" `*_~.,:;()[]&/,+")
        )
        if legacy_pipe_table:
            bodies.append(block_text)
            continue
        if (
            bare_links
            or identifier_links
            or indented_literal
            or inline_code_only
            or is_non_annotatable_line(first)
            or first.startswith((">", "|", "<", "@", "- ", "* ", "+ "))
            or re.match(r"\d+[.)]\s", first)
        ):
            continue
        bodies.append(" ".join(" ".join(block.lines).split()))
    return bodies


def _has_untranslated_source_prose(text: str, source: str) -> bool:
    return any(
        contains_untranslated_source_phrase(source_body, translated_body)
        for source_body, translated_body in zip(
            _plain_prose_bodies(source),
            _plain_prose_bodies(text),
            strict=False,
        )
    )


def _has_admonition_body_outside_blockquote(text: str) -> bool:
    body = _strip_code_blocks(text)
    lines = body.splitlines()
    for index, line in enumerate(lines[:-1]):
        if not _ADMONITION_RE.match(line.strip()):
            continue

        next_line = lines[index + 1]
        if next_line.strip() and not next_line.lstrip().startswith(">"):
            return True
    return False


def _has_duplicated_admonition_marker(text: str) -> bool:
    """`> [!NOTE]`가 연속 2줄로 중복되면 True (부분블록 치환 시 마커 중복 결함)."""
    body = _strip_code_blocks(text)
    lines = body.splitlines()
    for index in range(len(lines) - 1):
        if _ADMONITION_RE.match(lines[index].strip()) and _ADMONITION_RE.match(
            lines[index + 1].strip()
        ):
            return True
    return False


def _list_markers(text: str) -> int:
    """code block·주석을 제외한 순서 없는 리스트 항목(`-`/`*`/`+`) 수."""
    body = _strip_code_blocks(_strip_comments(text))
    return len(_LIST_MARKER_RE.findall(body))


def _normalize_comment_text(text: str) -> str:
    return normalize_annotation_anchor(text)


def _required_comments(source: str) -> set[str]:
    body = _strip_code_blocks(source)
    source_comment_lines = standalone_html_comment_line_numbers(body)
    reference_lines = reference_definition_line_numbers(body)
    comments: set[str] = set()
    paragraph: list[str] = []
    in_front_matter = False

    def flush_paragraph() -> None:
        if paragraph:
            if not is_structural_html_fragment("\n".join(paragraph)):
                comments.add(_normalize_comment_text(" ".join(paragraph)))
            paragraph.clear()

    for idx, line in enumerate(body.splitlines()):
        stripped = line.strip()
        if stripped == "---" and idx == 0:
            in_front_matter = True
            continue
        if stripped == "---" and in_front_matter:
            in_front_matter = False
            continue
        if in_front_matter:
            continue
        if idx + 1 in source_comment_lines:
            flush_paragraph()
            continue
        if idx in reference_lines:
            flush_paragraph()
            continue
        if not stripped:
            flush_paragraph()
            continue
        if stripped.startswith("#"):
            flush_paragraph()
            comments.add(_normalize_comment_text(stripped))
            continue
        if is_structural_html_line(line):
            flush_paragraph()
            continue
        if is_non_annotatable_line(line):
            flush_paragraph()
            continue
        list_body = re.sub(r"^(?:[-*+]\s+|\d+[.)]\s+)", "", stripped)
        if (
            list_body != stripped
            and (
                inline_code_contents(list_body)
                or html_code_contents(list_body)
            )
            and not strip_html_code_elements(
                strip_inline_code(list_body)
            ).strip(
                " `*_~.,:;()[]&/,+"
            )
        ):
            flush_paragraph()
            continue
        paragraph.append(stripped)

    flush_paragraph()
    return {comment for comment in comments if comment}


def _annotation_comment(body: str) -> str | None:
    annotatable = "\n".join(
        line for line in body.splitlines() if not is_structural_html_line(line)
    )
    normalized = _normalize_comment_text(annotatable)
    if (
        not normalized
        or is_non_annotatable_line(normalized)
        or is_structural_html_fragment(normalized)
    ):
        return None
    return normalized


def _translated_comments(text: str) -> set[str]:
    return {
        normalized
        for body in html_comment_bodies(text)
        if (normalized := _annotation_comment(body))
    }


def _comment_positions(
    text: str,
) -> list[tuple[str, int, str, int, int, bool, bool, int]]:
    return _response_comment_positions(text)


def _source_comment_indexes(
    actual: list[tuple[str, int, str, int, int, bool, bool, int]],
    source: str,
) -> set[int] | None:
    expected = _comment_positions(source)
    cursor = 0
    indexes: set[int] = set()
    for comment in expected:
        while cursor < len(actual) and actual[cursor] != comment:
            cursor += 1
        if cursor == len(actual):
            return None
        indexes.add(cursor)
        cursor += 1
    return indexes


def _has_extra_empty_comment(text: str, source: str | None = None) -> bool:
    actual = sum(not body.strip() for body in html_comment_bodies(text))
    if not actual:
        return False
    if source is None:
        return True
    expected = sum(
        not body.strip()
        for body in html_comment_bodies(_strip_code_blocks(source))
    )
    return actual > expected


def _line_after_comment(text: str, end: int) -> tuple[str, int] | None:
    cursor = end
    while cursor < len(text) and text[cursor] in " \t":
        cursor += 1
    if text.startswith("\r\n", cursor):
        cursor += 2
    elif cursor < len(text) and text[cursor] in "\r\n":
        cursor += 1
    else:
        return None

    line_end = cursor
    while line_end < len(text) and text[line_end] not in "\r\n":
        line_end += 1
    return text[cursor:line_end], line_end


def _annotation_sentence_cardinality_is_valid(
    text: str,
    source: str,
) -> bool:
    masked = mask_fenced_code_contents(text)
    actual = html_comment_spans(masked)
    source_comments = [
        _normalize_comment_text(body)
        for _start, _end, body in html_comment_spans(
            mask_fenced_code_contents(source)
        )
    ]
    source_comment_indexes: set[int] = set()
    cursor = 0
    for source_comment in source_comments:
        while (
            cursor < len(actual)
            and _normalize_comment_text(actual[cursor][2]) != source_comment
        ):
            cursor += 1
        if cursor == len(actual):
            return True
        source_comment_indexes.add(cursor)
        cursor += 1
    required_comments = _required_comments(source)
    for index, (_start, end, body) in enumerate(actual):
        if index in source_comment_indexes:
            continue
        annotation = _annotation_comment(body)
        if (
            annotation is None
            or annotation not in required_comments
            or annotation.startswith("#")
        ):
            continue
        following = _line_after_comment(masked, end)
        if following is None:
            continue
        translated_body, body_end = following
        stripped = translated_body.lstrip()
        if (
            not stripped
            or stripped.startswith((">", "|", "<", "- ", "* ", "+ "))
            or re.match(r"\d+[.)]\s", stripped)
        ):
            continue
        following_body = _line_after_comment(masked, body_end)
        if following_body is not None and following_body[0].strip():
            continue
        if not _sentence_cardinality_pair_is_valid(
            annotation,
            translated_body,
        ):
            return False
    return True


def _quote_depth(line: str) -> int:
    stripped = line.lstrip()
    depth = 0
    while stripped.startswith(">"):
        depth += 1
        stripped = stripped[1:].lstrip()
    return depth


def _quote_body(line: str) -> str:
    stripped = line.lstrip()
    while stripped.startswith(">"):
        stripped = stripped[1:].lstrip()
    return stripped


def _structural_line_matches(expected: str, actual: str) -> bool:
    expected_normalized = _normalize_comment_text(expected)
    actual_normalized = _normalize_comment_text(actual)
    if expected_normalized == actual_normalized:
        return True
    if expected_normalized.startswith(">"):
        return bool(
            _quote_depth(expected_normalized) == _quote_depth(actual_normalized)
            and (
                not _quote_body(expected_normalized)
                or _quote_body(actual_normalized)
            )
        )
    if expected_normalized.startswith("|"):
        return _table_line_signature(expected) == _table_line_signature(actual)
    if expected_normalized.startswith(("- [", "* [")):
        return (
            actual_normalized.startswith(expected_normalized[:2])
            and _link_pairs(expected) == _link_pairs(actual)
        )
    return bool(
        (
            _html_img_sources(expected)
            and _html_img_sources(expected) == _html_img_sources(actual)
            and _structural_html_signature(expected)
            == _structural_html_signature(actual)
        )
        or (
            _html_markup_signature(expected)
            and _html_markup_signature(expected)
            == _html_markup_signature(actual)
        )
    )


def _structural_annotation_owns_following(
    text: str,
    start: int,
    end: int,
    comment_body: str,
    *,
    expected_quote_ordinal: int | None = None,
    expected_table_ordinal: int | None = None,
) -> bool:
    expected_lines = [line for line in comment_body.splitlines() if line.strip()]
    if not expected_lines:
        return False

    cursor = end
    for index, expected in enumerate(expected_lines):
        following = _line_after_comment(text, cursor)
        if following is None:
            return False
        actual, cursor = following
        if not _structural_line_matches(expected, actual):
            return False
        if index == 0 and _normalize_comment_text(expected).startswith(">"):
            line_start = (
                max(
                    text.rfind("\n", 0, start),
                    text.rfind("\r", 0, start),
                )
                + 1
            )
            if _quote_depth(text[line_start:start]) != _quote_depth(actual):
                return False
            actual_quote_ordinal = sum(
                1
                for line in text[:cursor].splitlines()
                if line.lstrip().startswith(">")
                and not _ONE_LINE_COMMENT_RE.fullmatch(line)
            ) - 1
            if actual_quote_ordinal != expected_quote_ordinal:
                return False
        if index == 0 and _normalize_comment_text(expected).startswith("|"):
            actual_table_ordinal = sum(
                1
                for line in strip_html_comments(text[:cursor]).splitlines()
                if line.lstrip().startswith("|")
            ) - 1
            if actual_table_ordinal != expected_table_ordinal:
                return False
    return True


def _source_structural_comment_counts(source: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    run: list[str] = []

    def flush() -> None:
        if len(run) > 1:
            counts[_normalize_comment_text("\n".join(run))] += 1
        run.clear()

    for line in strip_html_comments(_strip_code_blocks(source)).splitlines():
        if line.strip() and is_structural_html_fragment(line):
            run.append(line)
        else:
            flush()
    flush()
    return counts


def _source_comments_are_preserved(text: str, source: str) -> bool:
    actual = _comment_positions(text)
    source_comment_indexes = _source_comment_indexes(actual, source)
    if source_comment_indexes is None:
        return False

    required_counts = Counter(_required_comments(source))
    actual_counts = Counter(
        normalized
        for index, (body, *_position) in enumerate(actual)
        if index not in source_comment_indexes
        if (normalized := _annotation_comment(body))
    )
    if required_counts - actual_counts:
        return False

    optional_quoted_annotations = _optional_quoted_comments(source)
    lines = text.splitlines()
    for index, (body, start_line, end_line, _position) in enumerate(
        _response_comment_records(text)
    ):
        if index in source_comment_indexes:
            continue
        if start_line >= len(lines):
            return False
        match = (
            _ONE_LINE_COMMENT_RE.fullmatch(lines[start_line])
            if start_line == end_line
            else None
        )
        if match is None or _quote_depth(match.group(1)) == 0:
            continue
        normalized = _annotation_comment(body)
        if normalized is None:
            continue
        depth = _quote_depth(match.group(1))
        key = (
            normalized,
            depth,
            _quote_block_ordinal(lines, start_line + 1),
        )
        if (
            not _optional_quote_annotation_starts_block(lines, start_line)
            or not optional_quoted_annotations[key]
        ):
            return False
        next_line_index = end_line + 1
        if (
            next_line_index >= len(lines)
            or _quote_depth(lines[next_line_index]) != depth
            or not _quote_body(lines[next_line_index])
        ):
            return False
        optional_quoted_annotations[key] -= 1

    structural_annotations = Counter(
        normalized
        for line in strip_html_comments(_strip_code_blocks(source)).splitlines()
        if (normalized := _normalize_comment_text(line))
    )
    structural_blocks = _source_structural_comment_counts(source)
    quote_ordinals: dict[str, list[int]] = {}
    quote_ordinal = 0
    table_ordinals: dict[str, list[int]] = {}
    table_ordinal = 0
    for line in _strip_code_blocks(source).splitlines():
        if _ONE_LINE_COMMENT_RE.fullmatch(line):
            continue
        normalized = _normalize_comment_text(line)
        if line.lstrip().startswith(">"):
            quote_ordinals.setdefault(normalized, []).append(quote_ordinal)
            quote_ordinal += 1
        elif line.lstrip().startswith("|"):
            table_ordinals.setdefault(normalized, []).append(table_ordinal)
            table_ordinal += 1
    consumed_quote_ordinals: Counter[str] = Counter()
    consumed_table_ordinals: Counter[str] = Counter()
    masked = mask_fenced_code_contents(text)
    spans = html_comment_spans(masked)
    for index, (start, end, body) in enumerate(spans):
        if index in source_comment_indexes:
            continue
        if any(
            _TABLE_BOUNDARY_TAG_RE.fullmatch(line)
            for line in body.splitlines()
        ):
            return False
        normalized = _normalize_comment_text(body)
        if normalized and (
            is_non_annotatable_line(normalized)
            or is_structural_html_fragment(normalized)
        ):
            if structural_annotations[normalized]:
                structural_annotations[normalized] -= 1
            elif structural_blocks[normalized]:
                structural_blocks[normalized] -= 1
            else:
                return False
            expected_quote_ordinal = None
            expected_table_ordinal = None
            if normalized.lstrip().startswith(">"):
                occurrence = consumed_quote_ordinals[normalized]
                if occurrence >= len(quote_ordinals.get(normalized, [])):
                    return False
                expected_quote_ordinal = quote_ordinals[normalized][occurrence]
                consumed_quote_ordinals[normalized] += 1
            elif normalized.lstrip().startswith("|"):
                occurrence = consumed_table_ordinals[normalized]
                if occurrence >= len(table_ordinals.get(normalized, [])):
                    return False
                expected_table_ordinal = table_ordinals[normalized][occurrence]
                consumed_table_ordinals[normalized] += 1
            if not _structural_annotation_owns_following(
                masked,
                start,
                end,
                body,
                expected_quote_ordinal=expected_quote_ordinal,
                expected_table_ordinal=expected_table_ordinal,
            ):
                return False
    return True


def missing_original_comments(text: str, source: str) -> list[str]:
    """Return required English source comments missing from translated text."""
    return sorted(_required_comments(source) - _translated_comments(text))


def verify(
    text: str,
    source: str | None = None,
    *,
    version: str | None = None,
    allow_source_echo: bool = False,
) -> list[str]:
    """위반 라벨 목록 반환. version은 현재 문서 링크 prefix 비교에 사용한다."""
    body = _strip_code_blocks(text)
    issues = [label for label, pattern in _FORBIDDEN.items() if pattern.search(body)]
    if has_malformed_html_comment_delimiters(text):
        issues.append("malformed HTML comment")
    if source is not None and admonition_types(source) != admonition_types(text):
        issues.append("admonition type mismatch")
    if _has_extra_empty_comment(body, source):
        issues.append("empty HTML comment")
    if img_self_closing(body) != body:
        issues.append("unclosed img tag")
    if has_title_attr_line(body):
        issues.append("title style class")
    if _has_admonition_body_outside_blockquote(body):
        issues.append("admonition body outside blockquote")
    if _has_duplicated_admonition_marker(body):
        issues.append("duplicate admonition marker")

    if source is None:
        return issues

    if _link_targets(source, version=version) != _link_targets(text, version=version):
        issues.append("link target mismatch")
    if _link_labels(source, version=version) != _link_labels(text, version=version):
        issues.append("link label mismatch")
    if _link_pairs(source, version=version) != _link_pairs(text, version=version):
        issues.append("link pair mismatch")
    if _link_titles(source, version=version) != _link_titles(text, version=version):
        issues.append("link title mismatch")
    source_image_signatures = _image_signatures(source, version=version)
    translated_image_signatures = _image_signatures(text, version=version)
    if (
        [target for target, _title in source_image_signatures]
        != [target for target, _title in translated_image_signatures]
        and "link target mismatch" not in issues
    ):
        issues.append("link target mismatch")
    if (
        [title for _target, title in source_image_signatures]
        != [title for _target, title in translated_image_signatures]
        and "link title mismatch" not in issues
    ):
        issues.append("link title mismatch")
    if (
        _mixed_image_order(source) != _mixed_image_order(text)
        and "link target mismatch" not in issues
    ):
        issues.append("link target mismatch")
    (
        source_definition_targets,
        source_definition_labels,
        source_definition_pairs,
        source_definition_signatures,
    ) = _reference_definition_signatures(source, version=version)
    (
        translated_definition_targets,
        translated_definition_labels,
        translated_definition_pairs,
        translated_definition_signatures,
    ) = _reference_definition_signatures(text, version=version)
    if (
        source_definition_targets != translated_definition_targets
        and "link target mismatch" not in issues
    ):
        issues.append("link target mismatch")
    if (
        source_definition_labels != translated_definition_labels
        and "link label mismatch" not in issues
    ):
        issues.append("link label mismatch")
    definition_pairs_match = (
        source_definition_pairs == translated_definition_pairs
    )
    if (
        not definition_pairs_match
        and "link pair mismatch" not in issues
    ):
        issues.append("link pair mismatch")
    if (
        definition_pairs_match
        and source_definition_signatures
        != translated_definition_signatures
        and "link title mismatch" not in issues
    ):
        issues.append("link title mismatch")
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
        and "link target mismatch" not in issues
    ):
        issues.append("link target mismatch")
    if (
        tuple(title for _image, _target, title in source_reference_links)
        != tuple(
            title
            for _image, _target, title in translated_reference_links
        )
        and "link title mismatch" not in issues
    ):
        issues.append("link title mismatch")
    if _inline_codes(source) != _inline_codes(text):
        issues.append("inline code mismatch")
    if _anchors(source) != _anchors(text):
        issues.append("anchor mismatch")
    if _structural_html_signature(source) != _structural_html_signature(text):
        issues.append("html tag mismatch")
    if _dynamic_display_attribute_signatures(
        source
    ) != _dynamic_display_attribute_signatures(text):
        issues.append("html display expression mismatch")
    if _html_img_sources(source) != _html_img_sources(text):
        issues.append("html image source mismatch")
    if _dynamic_display_attribute_signatures(
        source,
        tag_name="img",
    ) != _dynamic_display_attribute_signatures(text, tag_name="img"):
        issues.append("html image display expression mismatch")
    if html_code_contents(_strip_comments(_strip_code_blocks(source))) != html_code_contents(
        _strip_comments(_strip_code_blocks(text))
    ):
        issues.append("html code mismatch")
    if _normalized_fenced_code_blocks(source) != _normalized_fenced_code_blocks(text):
        issues.append("code block mismatch")
    if _heading_levels(source) != _heading_levels(text):
        issues.append("heading mismatch")
    if _heading_lines(source) != _heading_lines(text):
        issues.append("heading text mismatch")
    if _list_markers(text) < _list_markers(source):
        issues.append("list marker mismatch")
    if _front_matter_title(source) != _front_matter_title(text):
        issues.append("front matter title mismatch")
    description = front_matter_description(text)
    if description is not None and not description.valid:
        issues.append("front matter description invalid")
    if not _source_comments_are_preserved(text, source):
        issues.append("source comment mismatch")
    if missing_original_comments(text, source):
        issues.append("missing original comment")
    if not allow_source_echo and _has_untranslated_source_prose(text, source):
        issues.append("untranslated source text")
    if not _annotation_sentence_cardinality_is_valid(text, source):
        issues.append("sentence cardinality mismatch")

    return issues
