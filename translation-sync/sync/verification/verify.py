"""candidate 문서와 번역 내용의 결정적 Python 검증.

문서와 번역 내용 검증은 Python이 담당.
Docusaurus build 산출물 검증은 JS validate-anchors.mjs가 담당.

최종 문서에 허용되지 않는 잔존 pattern 검사 및 위반 목록 반환.
빈 목록은 성공.
"""
from __future__ import annotations

import re
from collections import Counter

from ..annotation.annotate import split_blocks
from ..common.admonitions import parse_legacy_admonition_line
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
    is_structural_html_fragment,
    is_structural_html_line,
    mask_fenced_code_contents,
    markdown_autolinks,
    markdown_links,
    mask_reference_definitions,
    normalize_annotation_anchor,
    reference_definitions,
    reference_definition_line_numbers,
    reference_link_display_signatures,
    reference_link_signatures,
    standalone_html_comment_line_numbers,
    strip_html_code_elements,
    strip_title_attr_line,
    strip_html_comments,
    strip_inline_code,
)
from ..common.stale_links import (
    DEFAULT_STALE_LINK_REGISTRY,
    StaleLinkRegistry,
    canonical_stale_link_target,
)
from ..postprocessing.postprocess import admonition_types, img_self_closing
from .response_contract import (
    _comment_position_matches as _response_comment_position_matches,
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
from .structure import (
    front_matter_contract,
    is_locale_routing_front_matter,
    list_structure_signature,
    table_structure_signature,
)

# 최종 문서의 코드 블록 밖에 남아 있으면 검증 실패인 내부 placeholder.
_FORBIDDEN = {
    "unreplaced {{version}}": re.compile(r"\{\{\s*version\s*\}\}"),
    "unrestored base64 placeholder": re.compile(r"__BASE64_IMAGE_\d+__"),
}
_ONE_LINE_COMMENT_RE = re.compile(
    r"^([ \t]*(?:>[ \t]*)*)<!--[ \t]*(.*?)[ \t]*-->[ \t]*$"
)
_TABLE_BOUNDARY_TAG_RE = re.compile(
    r"^[ \t]*</?table(?:[ \t][^>]*)?>[ \t]*$",
    re.IGNORECASE,
)

_URI_SCHEME_RE = re.compile(
    r"^[a-z][a-z0-9+.-]*:",
    re.IGNORECASE,
)
_INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
_ANCHOR_TAG_RE = re.compile(
    r"<a\b[^>]*\bname\s*=\s*[\"'][^\"']+[\"'][^>]*>",
    re.IGNORECASE,
)
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
_PROSE_TRIM_CHARACTERS = " `*_~.,:;()[]&/,+"
_LINK_TARGET_MISMATCH = "link target mismatch"
_LINK_LABEL_MISMATCH = "link label mismatch"
_LINK_PAIR_MISMATCH = "link pair mismatch"
_LINK_TITLE_MISMATCH = "link title mismatch"
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


def _strip_heading_lines(text: str) -> str:
    """heading 라인 제거.

    heading 텍스트 자체는 ``_heading_lines``에서 원문과 비교.
    여기서는 heading의 inline code와 링크가 본문 비교에 중복 반영되지 않도록 제외.
    """
    return _HEADING_LINE_RE.sub("", text)


def _strip_code_blocks(text: str) -> str:
    """Fenced code block을 제거해 코드 예시의 패턴을 검사 대상에서 제외."""
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
    """HTML 주석 제거."""

    return strip_html_comments(text)


def _mask_html_comments(text: str) -> str:
    """줄바꿈을 보존하며 HTML comment 영역 마스킹."""

    chars = list(text)
    for start, end, _body in html_comment_spans(text):
        for index in range(start, end):
            if chars[index] not in "\r\n":
                chars[index] = " "
    return "".join(chars)


def _fenced_code_blocks(text: str) -> list[str]:
    """Fenced code 블록을 원본 문서 순서로 수집."""

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
    """문서 경계 newline을 제외한 fenced code 블록 정규화."""

    # 마지막 newline은 문서 경계 소유.
    # 블록 내부 내용과 후행 공백은 원문 소유.

    return [block.rstrip("\n") for block in _fenced_code_blocks(text)]


def _link_targets(
    text: str,
    version: str | None = None,
    *,
    registry: StaleLinkRegistry = DEFAULT_STALE_LINK_REGISTRY,
) -> Counter[str]:
    """정규화된 Markdown 링크 target 출현 횟수 수집."""

    body = mask_reference_definitions(
        _strip_heading_lines(_strip_code_blocks(_strip_comments(text)))
    )
    targets = [link.target for link in markdown_links(body)]
    targets += [link.target for link in markdown_autolinks(body)]
    normalized = (
        _comparable_link_target(target, version=version, registry=registry)
        for target in targets
    )
    return Counter(target for target in normalized if target is not None)


def _link_labels(
    text: str,
    version: str | None = None,
    *,
    registry: StaleLinkRegistry = DEFAULT_STALE_LINK_REGISTRY,
) -> list[str]:
    """정렬된 multiset 순서의 Markdown 링크 label 수집."""

    body = mask_reference_definitions(
        _strip_code_blocks(_strip_comments(text))
    )
    labels = [
        " ".join(link.label.split())
        for link in markdown_links(body)
        if not link.image
        and (
            _comparable_link_target(
                link.target,
                version=version,
                registry=registry,
            )
            is not None
        )
    ]
    labels.extend(link.label for link in markdown_autolinks(body))
    return sorted(labels)


def _link_pairs(
    text: str,
    version: str | None = None,
    *,
    registry: StaleLinkRegistry = DEFAULT_STALE_LINK_REGISTRY,
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """label별 target 순서를 보존한 Markdown 링크 쌍 서명 수집.

    등장 순서 재배열은 허용하되, 같은 label이 반복되면 그 label의
    target 등장 순서는 보존해야 한다.
    """

    body = mask_reference_definitions(
        _strip_heading_lines(_strip_code_blocks(_strip_comments(text)))
    )
    pairs: list[tuple[int, tuple[str, str]]] = []
    for link in markdown_links(body):
        target = _comparable_link_target(
            link.target,
            version=version,
            registry=registry,
        )
        if not link.image and target is not None:
            pairs.append(
                (link.start, (" ".join(link.label.split()), target))
            )
    for autolink in markdown_autolinks(body):
        target = _comparable_link_target(
            autolink.target,
            version=version,
            registry=registry,
        )
        if target is not None:
            pairs.append((autolink.start, (autolink.label, target)))
    per_label_targets: dict[str, list[str]] = {}
    for _position, (label, target) in sorted(pairs):
        per_label_targets.setdefault(label, []).append(target)
    return tuple(
        sorted(
            (label, tuple(targets))
            for label, targets in per_label_targets.items()
        )
    )


def _link_titles(
    text: str,
    version: str | None = None,
    *,
    registry: StaleLinkRegistry = DEFAULT_STALE_LINK_REGISTRY,
) -> list[str]:
    """문서 순서의 Markdown 링크 title 수집."""

    body = mask_reference_definitions(
        _strip_heading_lines(_strip_code_blocks(_strip_comments(text)))
    )
    return [
        link.title
        for link in markdown_links(body)
        if (
            _comparable_link_target(
                link.target,
                version=version,
                registry=registry,
            )
            is not None
        )
    ]


def _image_signatures(
    text: str,
    version: str | None = None,
    *,
    registry: StaleLinkRegistry = DEFAULT_STALE_LINK_REGISTRY,
) -> list[tuple[str, str]]:
    """Markdown 이미지의 정규화된 target·title 서명 수집."""

    body = mask_reference_definitions(
        _strip_heading_lines(_strip_code_blocks(_strip_comments(text)))
    )
    signatures: list[tuple[str, str]] = []
    for link in markdown_links(body):
        target = _comparable_link_target(
            link.target,
            version=version,
            registry=registry,
        )
        if link.image and target is not None:
            signatures.append((target, link.title))
    return signatures


def _reference_definition_signatures(
    text: str,
    version: str | None = None,
    *,
    registry: StaleLinkRegistry = DEFAULT_STALE_LINK_REGISTRY,
) -> tuple[
    tuple[str | None, ...],
    tuple[str, ...],
    tuple[tuple[str, str | None], ...],
    tuple[tuple[str, str | None, str], ...],
]:
    """Reference definition의 target·label·title 서명 수집."""

    definitions = [
        (
            definition.label,
            _comparable_link_target(
                definition.target,
                version=version,
                registry=registry,
            ),
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


def _normalize_link_target(
    target: str,
    version: str | None = None,
    *,
    registry: StaleLinkRegistry = DEFAULT_STALE_LINK_REGISTRY,
) -> str | None:
    """문서 버전과 stale-link 규칙을 적용해 링크 target 정규화."""

    target = _strip_matching_docs_prefix(
        target,
        _LARAVEL_DOCS_PREFIX_RE,
        version,
    )
    if _URI_SCHEME_RE.match(target):
        return target
    target = _strip_matching_docs_prefix(target, _DOCS_PREFIX_RE, version)

    if target.startswith("./"):
        remainder = target[2:]
        if (
            remainder
            and remainder[0] not in "/#?"
            and not _URI_SCHEME_RE.match(remainder)
        ):
            target = remainder

    return canonical_stale_link_target(
        target,
        version,
        registry=registry,
    )


def _strip_matching_docs_prefix(
    target: str,
    pattern: re.Pattern[str],
    version: str | None,
) -> str:
    """현재 버전과 일치하는 문서 링크 접두사를 비교용으로 제거.

    Args:
        target: 링크 대상.
        pattern: 버전 named group을 가진 문서 접두사 정규식.
        version: 현재 문서 버전.

    Returns:
        제거 조건을 충족하면 접두사 없는 대상, 아니면 원본 대상.
    """

    match = pattern.match(target)
    if match is None or match.group("version") != version:
        return target
    remainder = target[match.end() :]
    prefix = target[: match.end()]
    if (
        remainder
        and not remainder.startswith("/")
        and not (prefix.endswith("/") and remainder.startswith(("#", "?")))
    ):
        return remainder
    return target


def _comparable_link_target(
    target: str,
    version: str | None = None,
    *,
    registry: StaleLinkRegistry = DEFAULT_STALE_LINK_REGISTRY,
) -> str | None:
    """폐기 규칙을 포함해 비교 가능한 링크 target 반환."""

    return _normalize_link_target(
        target,
        version=version,
        registry=registry,
    )


def _has_legacy_admonition(text: str) -> bool:
    """legacy admonition 포함 여부."""

    visible = strip_html_comments(_strip_code_blocks(text))
    return any(
        parse_legacy_admonition_line(line) is not None
        for line in visible.splitlines()
    )


def _inline_codes(text: str) -> Counter[str]:
    """문서의 inline code 내용별 출현 횟수 수집."""

    body = _strip_heading_lines(_strip_code_blocks(_strip_comments(text)))
    return Counter(inline_code_contents(body))


def _anchors(text: str) -> Counter[str]:
    """명시적 HTML anchor 이름별 출현 횟수 수집."""

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
    """번역으로 변경할 수 없는 구조 HTML 서명 수집."""

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
    """HTML img 태그의 원문 소유 src를 문서 순서로 수집."""

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
    """ATX heading level을 문서 순서로 수집."""

    body = _strip_code_blocks(_strip_comments(text))
    levels: list[int] = []
    for line in body.splitlines():
        stripped = line.lstrip()
        level = len(stripped) - len(stripped.lstrip("#"))
        if 1 <= level <= 6 and len(stripped) > level and stripped[level].isspace():
            levels.append(level)
    return levels


def _heading_lines(text: str) -> list[str]:
    """속성 줄을 제거한 ATX heading 텍스트 수집."""

    body = _strip_code_blocks(_strip_comments(text))
    headings: list[str] = []
    for line in body.splitlines():
        if is_heading_line(line):
            headings.append(strip_title_attr_line(line).strip())
    return headings


def _front_matter_title(text: str) -> str | None:
    """선행 front matter의 title 문자열 조회."""

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
    """언어 검사용 일반 prose 본문 수집."""

    blocks = split_blocks(
        mask_reference_definitions(
            _strip_comments(_strip_code_blocks(text))
        ).splitlines()
    )
    bodies: list[str] = []
    for block in blocks:
        if block.kind != "text" or not block.lines:
            continue
        block_text = "\n".join(block.lines)
        if _is_legacy_prose_table(block.lines):
            bodies.append(block_text)
            continue
        if _is_non_prose_block(block.lines, block_text):
            continue
        bodies.append(" ".join(" ".join(block.lines).split()))
    return bodies


def _is_complete_link_line(line: str) -> bool:
    """줄 전체가 단일 Markdown 링크인지 판정.

    Args:
        line: Markdown 물리 줄.

    Returns:
        공백 제거 후 단일 링크만 남는지 여부.
    """

    stripped = line.strip()
    links = markdown_links(stripped)
    return len(links) == 1 and links[0].start == 0 and links[0].end == len(stripped)


def _is_legacy_prose_table(lines: list[str]) -> bool:
    """일반 prose 블록이 레거시 pipe table인지 판정.

    Args:
        lines: 텍스트 블록 줄.

    Returns:
        레거시 pipe table 여부.
    """

    return bool(
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


def _is_non_prose_block(lines: list[str], block_text: str) -> bool:
    """텍스트 블록이 언어 검사를 제외할 식별자·구조·literal인지 판정.

    Args:
        lines: 텍스트 블록 줄.
        block_text: 줄바꿈으로 결합한 블록 본문.

    Returns:
        일반 prose 검사 제외 여부.
    """

    identifier_links = all(
        _is_complete_link_line(line)
        or (
            bool(inline_code_contents(line.strip()))
            and not strip_inline_code(line.strip()).strip(_PROSE_TRIM_CHARACTERS)
        )
        for line in lines
    )
    indented_literal = all(
        line.startswith("\t") or len(line) - len(line.lstrip(" ")) >= 4
        for line in lines
    )
    inline_code_only = bool(inline_code_contents(block_text)) and not (
        strip_inline_code(block_text).strip(_PROSE_TRIM_CHARACTERS)
    )
    first = lines[0].lstrip()
    return bool(
        all(_is_complete_link_line(line) for line in lines)
        or identifier_links
        or indented_literal
        or inline_code_only
        or is_non_annotatable_line(first)
        or first.startswith((">", "|", "<", "@", "- ", "* ", "+ "))
        or re.match(r"\d+[.)]\s", first)
    )


def _has_untranslated_source_prose(text: str, source: str) -> bool:
    """untranslated 원문 prose 포함 여부."""

    return any(
        contains_untranslated_source_phrase(source_body, translated_body)
        for source_body, translated_body in zip(
            _plain_prose_bodies(source),
            _plain_prose_bodies(text),
            strict=False,
        )
    )


def _has_admonition_body_outside_blockquote(text: str) -> bool:
    """admonition 본문이 blockquote 밖에 있는지 여부."""

    original = _strip_code_blocks(text)
    body = _mask_html_comments(original)
    original_lines = original.splitlines()
    lines = body.splitlines()
    for index, line in enumerate(lines[:-1]):
        if not _ADMONITION_RE.match(line.strip()):
            continue

        next_line = lines[index + 1]
        if (
            original_lines[index + 1].strip()
            and not next_line.lstrip().startswith(">")
        ):
            return True
    return False


def _has_duplicated_admonition_marker(text: str) -> bool:
    """부분 블록 치환에서 admonition marker가 두 줄 연속 중복됐는지 여부."""
    body = _mask_html_comments(_strip_code_blocks(text))
    lines = body.splitlines()
    for index in range(len(lines) - 1):
        if _ADMONITION_RE.match(lines[index].strip()) and _ADMONITION_RE.match(
            lines[index + 1].strip()
        ):
            return True
    return False


def _list_markers(text: str) -> int:
    """code block·주석을 제외한 순서가 없는 목록 항목(`-`/`*`/`+`) 수."""
    body = _strip_code_blocks(_strip_comments(text))
    return len(_LIST_MARKER_RE.findall(body))


def _normalize_comment_text(text: str) -> str:
    """비교용 HTML comment 본문 정규화."""

    return normalize_annotation_anchor(text)


def _list_item_is_identifier_only(stripped: str) -> bool:
    """목록 항목 본문이 inline 또는 HTML code 식별자만 포함하는지 판정.

    Args:
        stripped: 앞뒤 공백이 제거된 Markdown 줄.

    Returns:
        목록 표식 뒤에 code 식별자만 있는지 여부.
    """

    list_body = re.sub(r"^(?:[-*+]\s+|\d+[.)]\s+)", "", stripped)
    return bool(
        list_body != stripped
        and (inline_code_contents(list_body) or html_code_contents(list_body))
        and not strip_html_code_elements(strip_inline_code(list_body)).strip(
            _PROSE_TRIM_CHARACTERS
        )
    )


def _required_comment_line_kind(
    line: str,
    index: int,
    *,
    in_front_matter: bool,
    source_comment_lines: frozenset[int],
    reference_lines: frozenset[int],
) -> tuple[str, bool]:
    """영어 원문 줄의 annotation 처리 종류와 머리말 상태 결정.

    Args:
        line: 영어 원문 물리 줄.
        index: 0-based 줄 위치.
        in_front_matter: 이전 줄까지 머리말 내부 여부.
        source_comment_lines: 원문 작성 주석의 1-based 줄 번호.
        reference_lines: 참조 정의의 0-based 줄 번호.

    Returns:
        ``skip``, ``flush``, ``heading`` 또는 ``append``와 다음 머리말 상태.
    """

    stripped = line.strip()
    if stripped == "---" and index == 0:
        return "skip", True
    if stripped == "---" and in_front_matter:
        return "skip", False
    if in_front_matter:
        return "skip", True
    if index + 1 in source_comment_lines or index in reference_lines:
        return "flush", False
    if not stripped:
        return "flush", False
    if stripped.startswith("#"):
        return "heading", False
    if (
        is_structural_html_line(line)
        or is_non_annotatable_line(line)
        or _list_item_is_identifier_only(stripped)
    ):
        return "flush", False
    return "append", False


def _required_comments(source: str) -> list[str]:
    """영어 원문에서 locale에 필요한 annotation 본문 생성."""

    body = _strip_code_blocks(source)
    source_comment_lines = standalone_html_comment_line_numbers(body)
    reference_lines = reference_definition_line_numbers(body)
    comments: list[str] = []
    paragraph: list[str] = []
    in_front_matter = False

    def flush_paragraph() -> None:
        """누적된 paragraph를 annotation 본문으로 확정."""

        if paragraph:
            if not is_structural_html_fragment("\n".join(paragraph)):
                comments.append(_normalize_comment_text(" ".join(paragraph)))
            paragraph.clear()

    for idx, line in enumerate(body.splitlines()):
        stripped = line.strip()
        kind, in_front_matter = _required_comment_line_kind(
            line,
            idx,
            in_front_matter=in_front_matter,
            source_comment_lines=source_comment_lines,
            reference_lines=reference_lines,
        )
        if kind == "skip":
            continue
        if kind == "heading":
            flush_paragraph()
            comments.append(_normalize_comment_text(stripped))
            continue
        if kind == "flush":
            flush_paragraph()
            continue
        paragraph.append(stripped)

    flush_paragraph()
    return [comment for comment in comments if comment]


def _annotation_comment(body: str) -> str | None:
    """HTML comment 본문이 pipeline annotation이면 정규화해 반환."""

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


def _translated_comments(text: str) -> list[str]:
    """Locale 문서의 pipeline annotation 본문 수집."""

    return [
        normalized
        for body in html_comment_bodies(text)
        if (normalized := _annotation_comment(body))
    ]


def _comment_positions(
    text: str,
) -> list[tuple[str, int, str, int, int, bool, bool, int]]:
    """HTML comment의 줄과 구조 위치 수집."""

    return _response_comment_positions(text)


def _source_comment_indexes(
    actual: list[tuple[str, int, str, int, int, bool, bool, int]],
    source: str,
) -> set[int] | None:
    """Locale comment 중 원문 작성 comment의 index 식별."""

    expected = _comment_positions(source)
    cursor = 0
    indexes: set[int] = set()
    for comment in expected:
        while cursor < len(actual) and not _response_comment_position_matches(
            actual[cursor],
            comment,
        ):
            cursor += 1
        if cursor == len(actual):
            return None
        indexes.add(cursor)
        cursor += 1
    return indexes


def _has_extra_empty_comment(text: str, source: str | None = None) -> bool:
    """원문에 없는 빈 HTML comment 포함 여부."""

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
    """HTML 주석 바로 다음 줄의 내용과 줄 끝 위치 반환."""

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


def _normalized_source_comment_indexes(
    actual: list[tuple[int, int, str]],
    source: str,
) -> set[int] | None:
    """정규 본문 순서로 locale 내 원문 작성 주석 위치 식별.

    Args:
        actual: locale HTML 주석 범위와 본문 목록.
        source: 영어 원문.

    Returns:
        원문 작성 주석 위치 집합. 순서대로 찾지 못하면 ``None``.
    """

    source_comments = [
        _normalize_comment_text(body)
        for _start, _end, body in html_comment_spans(
            mask_fenced_code_contents(source)
        )
    ]
    indexes: set[int] = set()
    cursor = 0
    for source_comment in source_comments:
        while (
            cursor < len(actual)
            and _normalize_comment_text(actual[cursor][2]) != source_comment
        ):
            cursor += 1
        if cursor == len(actual):
            return None
        indexes.add(cursor)
        cursor += 1
    return indexes


def _annotation_sentence_pair_is_valid(
    masked: str,
    *,
    end: int,
    body: str,
    required_comments: list[str],
) -> bool:
    """단일 prose annotation과 다음 번역 문장의 문장 수 계약 검사.

    Args:
        masked: 코드 펜스가 제거된 locale 문서.
        end: annotation 끝 문자 위치.
        body: HTML 주석 본문.
        required_comments: 원문에서 요구한 annotation 본문 목록.

    Returns:
        적용 대상이 아니거나 문장 수 계약을 충족하는지 여부.
    """

    annotation = _annotation_comment(body)
    if annotation is None or annotation not in required_comments or annotation.startswith("#"):
        return True
    following = _line_after_comment(masked, end)
    if following is None:
        return True
    translated_body, body_end = following
    stripped = translated_body.lstrip()
    if (
        not stripped
        or stripped.startswith((">", "|", "<", "- ", "* ", "+ "))
        or re.match(r"\d+[.)]\s", stripped)
    ):
        return True
    following_body = _line_after_comment(masked, body_end)
    if following_body is not None and following_body[0].strip():
        return True
    return _sentence_cardinality_pair_is_valid(annotation, translated_body)


def _annotation_sentence_cardinality_is_valid(
    text: str,
    source: str,
) -> bool:
    """Annotation과 번역 소유 블록의 문장 수 계약 검증."""

    masked = mask_fenced_code_contents(text)
    actual = html_comment_spans(masked)
    source_comment_indexes = _normalized_source_comment_indexes(actual, source)
    if source_comment_indexes is None:
        return True
    required_comments = _required_comments(source)
    for index, (_start, end, body) in enumerate(actual):
        if index in source_comment_indexes:
            continue
        if not _annotation_sentence_pair_is_valid(
            masked,
            end=end,
            body=body,
            required_comments=required_comments,
        ):
            return False
    return True


def _quote_depth(line: str) -> int:
    """Markdown 줄의 blockquote 깊이 계산."""

    stripped = line.lstrip()
    depth = 0
    while stripped.startswith(">"):
        depth += 1
        stripped = stripped[1:].lstrip()
    return depth


def _quote_body(line: str) -> str:
    """Markdown blockquote marker를 제거한 본문 반환."""

    stripped = line.lstrip()
    while stripped.startswith(">"):
        stripped = stripped[1:].lstrip()
    return stripped


def _structural_line_matches(expected: str, actual: str) -> bool:
    """Annotation 원문과 소유 구조 줄의 대응 여부."""

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


def _structural_owner_ordinal_is_valid(
    text: str,
    *,
    start: int,
    cursor: int,
    expected: str,
    actual: str,
    line_index: int,
    expected_quote_ordinal: int | None,
    expected_table_ordinal: int | None,
) -> bool:
    """첫 구조 annotation의 인용 깊이와 문서 내 구조 순번 검증.

    Args:
        text: locale 문서.
        start: annotation 시작 문자 위치.
        cursor: 소유 구조 줄 끝 위치.
        expected: annotation의 기대 구조 줄.
        actual: 실제 소유 구조 줄.
        line_index: 여러 줄 annotation 내부 위치.
        expected_quote_ordinal: 기대 인용 줄 순번.
        expected_table_ordinal: 기대 표 줄 순번.

    Returns:
        구조 깊이와 순번 계약 충족 여부.
    """

    if line_index != 0:
        return True
    normalized = _normalize_comment_text(expected)
    if normalized.startswith(">"):
        line_start = max(
            text.rfind("\n", 0, start),
            text.rfind("\r", 0, start),
        ) + 1
        if _quote_depth(text[line_start:start]) != _quote_depth(actual):
            return False
        ordinal = sum(
            1
            for line in text[:cursor].splitlines()
            if line.lstrip().startswith(">")
            and not _ONE_LINE_COMMENT_RE.fullmatch(line)
        ) - 1
        return ordinal == expected_quote_ordinal
    if normalized.startswith("|"):
        ordinal = sum(
            1
            for line in strip_html_comments(text[:cursor]).splitlines()
            if line.lstrip().startswith("|")
        ) - 1
        return ordinal == expected_table_ordinal
    return True


def _structural_annotation_owns_following(
    text: str,
    start: int,
    end: int,
    comment_body: str,
    *,
    expected_quote_ordinal: int | None = None,
    expected_table_ordinal: int | None = None,
) -> bool:
    """구조 annotation이 올바른 다음 블록을 소유하는지 검사."""

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
        if not _structural_owner_ordinal_is_valid(
            text,
            start=start,
            cursor=cursor,
            expected=expected,
            actual=actual,
            line_index=index,
            expected_quote_ordinal=expected_quote_ordinal,
            expected_table_ordinal=expected_table_ordinal,
        ):
            return False
    return True


def _source_structural_comment_counts(source: str) -> Counter[str]:
    """원문의 연속된 구조 HTML 조각 묶음을 정규화해 출현 횟수 수집."""

    counts: Counter[str] = Counter()
    run: list[str] = []

    def flush() -> None:
        """누적된 구조 HTML 조각을 하나의 서명으로 확정."""

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


def _optional_quoted_annotations_are_valid(
    text: str,
    source: str,
    source_comment_indexes: set[int],
) -> bool:
    """원문 주석 이외의 선택적 인용 annotation 위치와 횟수 검증.

    Args:
        text: locale 문서.
        source: 영어 원문.
        source_comment_indexes: locale 내 원문 작성 주석 위치.

    Returns:
        모든 선택적 인용 annotation이 허용 계약을 충족하는지 여부.
    """

    optional = _optional_quoted_comments(source)
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
        key = (normalized, depth, _quote_block_ordinal(lines, start_line + 1))
        next_line = end_line + 1
        if (
            not _optional_quote_annotation_starts_block(lines, start_line)
            or not optional[key]
            or next_line >= len(lines)
            or _quote_depth(lines[next_line]) != depth
            or not _quote_body(lines[next_line])
        ):
            return False
        optional[key] -= 1
    return True


def _source_structural_annotation_state(
    source: str,
) -> tuple[
    Counter[str],
    Counter[str],
    dict[str, list[int]],
    dict[str, list[int]],
]:
    """원문 구조 annotation 횟수와 인용·표 순번 mapping 구성.

    Args:
        source: 영어 원문.

    Returns:
        단일 줄·블록 구조 횟수와 인용·표 순번 mapping.
    """

    structural_annotations = Counter(
        normalized
        for line in strip_html_comments(_strip_code_blocks(source)).splitlines()
        if (normalized := _normalize_comment_text(line))
    )
    quote_ordinals: dict[str, list[int]] = {}
    table_ordinals: dict[str, list[int]] = {}
    quote_ordinal = 0
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
    return (
        structural_annotations,
        _source_structural_comment_counts(source),
        quote_ordinals,
        table_ordinals,
    )


def _consume_structural_annotation(
    normalized: str,
    *,
    structural_annotations: Counter[str],
    structural_blocks: Counter[str],
    quote_ordinals: dict[str, list[int]],
    table_ordinals: dict[str, list[int]],
    consumed_quote_ordinals: Counter[str],
    consumed_table_ordinals: Counter[str],
) -> tuple[bool, int | None, int | None]:
    """구조 annotation occurrence와 기대 인용·표 순번 소비.

    Args:
        normalized: 정규화된 구조 annotation 본문.
        structural_annotations: 남은 단일 줄 구조 횟수.
        structural_blocks: 남은 여러 줄 구조 블록 횟수.
        quote_ordinals: 본문별 기대 인용 순번.
        table_ordinals: 본문별 기대 표 순번.
        consumed_quote_ordinals: 본문별 소비한 인용 순번 수.
        consumed_table_ordinals: 본문별 소비한 표 순번 수.

    Returns:
        소비 성공 여부와 기대 인용·표 순번.
    """

    if structural_annotations[normalized]:
        structural_annotations[normalized] -= 1
    elif structural_blocks[normalized]:
        structural_blocks[normalized] -= 1
    else:
        return False, None, None
    expected_quote: int | None = None
    expected_table: int | None = None
    if normalized.lstrip().startswith(">"):
        occurrence = consumed_quote_ordinals[normalized]
        values = quote_ordinals.get(normalized, [])
        if occurrence >= len(values):
            return False, None, None
        expected_quote = values[occurrence]
        consumed_quote_ordinals[normalized] += 1
    elif normalized.lstrip().startswith("|"):
        occurrence = consumed_table_ordinals[normalized]
        values = table_ordinals.get(normalized, [])
        if occurrence >= len(values):
            return False, None, None
        expected_table = values[occurrence]
        consumed_table_ordinals[normalized] += 1
    return True, expected_quote, expected_table


def _structural_annotations_are_valid(
    text: str,
    source: str,
    source_comment_indexes: set[int],
) -> bool:
    """pipeline 구조 annotation의 occurrence·순번·소유 블록 검증.

    Args:
        text: locale 문서.
        source: 영어 원문.
        source_comment_indexes: locale 내 원문 작성 주석 위치.

    Returns:
        모든 구조 annotation 계약 충족 여부.
    """

    state = _source_structural_annotation_state(source)
    structural_annotations, structural_blocks, quote_ordinals, table_ordinals = state
    consumed_quote_ordinals: Counter[str] = Counter()
    consumed_table_ordinals: Counter[str] = Counter()
    masked = mask_fenced_code_contents(text)
    for index, (start, end, body) in enumerate(html_comment_spans(masked)):
        if index in source_comment_indexes:
            continue
        if any(_TABLE_BOUNDARY_TAG_RE.fullmatch(line) for line in body.splitlines()):
            return False
        normalized = _normalize_comment_text(body)
        if not normalized or not (
            is_non_annotatable_line(normalized)
            or is_structural_html_fragment(normalized)
        ):
            continue
        consumed, quote_ordinal, table_ordinal = _consume_structural_annotation(
            normalized,
            structural_annotations=structural_annotations,
            structural_blocks=structural_blocks,
            quote_ordinals=quote_ordinals,
            table_ordinals=table_ordinals,
            consumed_quote_ordinals=consumed_quote_ordinals,
            consumed_table_ordinals=consumed_table_ordinals,
        )
        if not consumed or not _structural_annotation_owns_following(
            masked,
            start,
            end,
            body,
            expected_quote_ordinal=quote_ordinal,
            expected_table_ordinal=table_ordinal,
        ):
            return False
    return True


def _source_comments_are_preserved(text: str, source: str) -> bool:
    """원문 작성 HTML 주석의 값·순서·구조 위치 보존 여부."""

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

    return _optional_quoted_annotations_are_valid(
        text,
        source,
        source_comment_indexes,
    ) and _structural_annotations_are_valid(
        text,
        source,
        source_comment_indexes,
    )


def missing_original_comments(text: str, source: str) -> list[str]:
    """Locale 문서에서 누락된 필수 영어 annotation 목록 반환.

    Args:
        text: 검사할 locale 문서.
        source: annotation 기준 영어 원문.

    Returns:
        UTF-8 바이트 순으로 정렬된 누락 annotation 본문.
    """
    missing = Counter(_required_comments(source)) - Counter(
        _translated_comments(text)
    )
    return sorted(missing.elements(), key=lambda value: value.encode("utf-8"))


def _append_issue_once(issues: list[str], issue: str) -> None:
    """검증 이슈를 중복 없이 추가.

    Args:
        issues: 발견 순서대로 누적 중인 이슈 목록.
        issue: 추가할 이슈 label.
    """

    if issue not in issues:
        issues.append(issue)


def _basic_issues(text: str, source: str | None) -> list[str]:
    """원문 비교 전 locale 문서 자체의 잔존 패턴 검사.

    Args:
        text: 검사할 locale 문서.
        source: 비교 기준 영어 문서.

    Returns:
        발견 순서의 기본 위반 label.
    """

    body = _strip_code_blocks(text)
    issues = [label for label, pattern in _FORBIDDEN.items() if pattern.search(body)]
    checks = (
        (_has_legacy_admonition(text), "legacy note marker"),
        (has_malformed_html_comment_delimiters(text), "malformed HTML comment"),
        (
            source is not None and admonition_types(source) != admonition_types(text),
            "admonition type mismatch",
        ),
        (_has_extra_empty_comment(body, source), "empty HTML comment"),
        (img_self_closing(body) != body, "unclosed img tag"),
        (has_title_attr_line(body), "title style class"),
        (
            _has_admonition_body_outside_blockquote(body),
            "admonition body outside blockquote",
        ),
        (_has_duplicated_admonition_marker(body), "duplicate admonition marker"),
    )
    issues.extend(label for failed, label in checks if failed)
    return issues


def _inline_link_issues(
    text: str,
    source: str,
    *,
    version: str | None,
    registry: StaleLinkRegistry,
) -> list[str]:
    """inline 링크·이미지 보존 이슈 수집.

    Args:
        text: 검사할 locale 문서.
        source: 비교 기준 영어 문서.
        version: 내부 문서 링크 정규화용 현재 버전.
        registry: 알려진 원문 stale link 정규화 규칙.

    Returns:
        발견 순서의 링크 위반 label.
    """

    issues: list[str] = []
    comparisons = (
        (
            _link_targets(source, version=version, registry=registry),
            _link_targets(text, version=version, registry=registry),
            _LINK_TARGET_MISMATCH,
        ),
        (
            _link_labels(source, version=version, registry=registry),
            _link_labels(text, version=version, registry=registry),
            _LINK_LABEL_MISMATCH,
        ),
        (
            _link_pairs(source, version=version, registry=registry),
            _link_pairs(text, version=version, registry=registry),
            _LINK_PAIR_MISMATCH,
        ),
        (
            _link_titles(source, version=version, registry=registry),
            _link_titles(text, version=version, registry=registry),
            _LINK_TITLE_MISMATCH,
        ),
    )
    for expected, actual, issue in comparisons:
        if expected != actual:
            _append_issue_once(issues, issue)
    _append_image_link_issues(
        issues,
        text,
        source,
        version=version,
        registry=registry,
    )
    return issues


def _append_image_link_issues(
    issues: list[str],
    text: str,
    source: str,
    *,
    version: str | None,
    registry: StaleLinkRegistry,
) -> None:
    """inline 이미지 link signature 이슈 추가.

    Args:
        issues: 발견 순서대로 누적 중인 링크 이슈.
        text: 검사할 locale 문서.
        source: 비교 기준 영어 문서.
        version: 내부 문서 링크 정규화용 현재 버전.
        registry: 알려진 원문 stale link 정규화 규칙.
    """

    expected = _image_signatures(source, version=version, registry=registry)
    actual = _image_signatures(text, version=version, registry=registry)
    if [target for target, _title in expected] != [
        target for target, _title in actual
    ]:
        _append_issue_once(issues, _LINK_TARGET_MISMATCH)
    if [title for _target, title in expected] != [
        title for _target, title in actual
    ]:
        _append_issue_once(issues, _LINK_TITLE_MISMATCH)
    if _mixed_image_order(source) != _mixed_image_order(text):
        _append_issue_once(issues, _LINK_TARGET_MISMATCH)


def _reference_definition_issues(
    text: str,
    source: str,
    *,
    version: str | None,
    registry: StaleLinkRegistry,
) -> list[str]:
    """참조 정의의 target·label·title 보존 이슈 수집.

    Args:
        text: 검사할 locale 문서.
        source: 비교 기준 영어 문서.
        version: 내부 문서 링크 정규화용 현재 버전.
        registry: 알려진 원문 stale link 정규화 규칙.

    Returns:
        발견 순서의 참조 정의 위반 label.
    """

    expected = _reference_definition_signatures(
        source,
        version=version,
        registry=registry,
    )
    actual = _reference_definition_signatures(
        text,
        version=version,
        registry=registry,
    )
    issues: list[str] = []
    for expected_value, actual_value, issue in zip(
        expected[:3],
        actual[:3],
        (_LINK_TARGET_MISMATCH, _LINK_LABEL_MISMATCH, _LINK_PAIR_MISMATCH),
        strict=True,
    ):
        if expected_value != actual_value:
            issues.append(issue)
    if expected[2] == actual[2] and expected[3] != actual[3]:
        issues.append(_LINK_TITLE_MISMATCH)
    return issues


def _comparable_reference_links(
    text: str,
    *,
    version: str | None,
    registry: StaleLinkRegistry,
) -> tuple[tuple[bool, str | None, str], ...]:
    """참조 링크 target을 비교 가능한 값으로 정규화.

    Args:
        text: Markdown 문서.
        version: 내부 문서 링크 정규화용 현재 버전.
        registry: 알려진 원문 stale link 정규화 규칙.

    Returns:
        이미지 여부·정규화 target·title tuple 목록.
    """

    return tuple(
        (
            image,
            _comparable_link_target(target, version=version, registry=registry),
            title,
        )
        for image, target, title in reference_link_signatures(text)
    )


def _reference_link_issues(
    text: str,
    source: str,
    *,
    version: str | None,
    registry: StaleLinkRegistry,
) -> list[str]:
    """참조 링크 사용부의 표시·target·title 보존 이슈 수집.

    Args:
        text: 검사할 locale 문서.
        source: 비교 기준 영어 문서.
        version: 내부 문서 링크 정규화용 현재 버전.
        registry: 알려진 원문 stale link 정규화 규칙.

    Returns:
        발견 순서의 참조 링크 위반 label.
    """

    expected = _comparable_reference_links(
        source,
        version=version,
        registry=registry,
    )
    actual = _comparable_reference_links(
        text,
        version=version,
        registry=registry,
    )
    issues: list[str] = []
    if reference_link_display_signatures(source) != reference_link_display_signatures(
        text
    ):
        issues.append(_LINK_LABEL_MISMATCH)
    if tuple((image, target) for image, target, _title in expected) != tuple(
        (image, target) for image, target, _title in actual
    ):
        issues.append(_LINK_TARGET_MISMATCH)
    if tuple(title for _image, _target, title in expected) != tuple(
        title for _image, _target, title in actual
    ):
        issues.append(_LINK_TITLE_MISMATCH)
    return issues


def _link_issues(
    text: str,
    source: str,
    *,
    version: str | None,
    registry: StaleLinkRegistry,
) -> list[str]:
    """모든 Markdown 링크 계약 이슈를 중복 없이 수집.

    Args:
        text: 검사할 locale 문서.
        source: 비교 기준 영어 문서.
        version: 내부 문서 링크 정규화용 현재 버전.
        registry: 알려진 원문 stale link 정규화 규칙.

    Returns:
        발견 순서의 링크 위반 label.
    """

    issues = _inline_link_issues(
        text,
        source,
        version=version,
        registry=registry,
    )
    for group in (
        _reference_definition_issues(
            text,
            source,
            version=version,
            registry=registry,
        ),
        _reference_link_issues(
            text,
            source,
            version=version,
            registry=registry,
        ),
    ):
        for issue in group:
            _append_issue_once(issues, issue)
    return issues


def _html_structure_issues(text: str, source: str) -> list[str]:
    """inline code·HTML 구조 보존 이슈 수집.

    Args:
        text: 검사할 locale 문서.
        source: 비교 기준 영어 문서.

    Returns:
        발견 순서의 inline·HTML 위반 label.
    """

    source_body = _strip_comments(_strip_code_blocks(source))
    translated_body = _strip_comments(_strip_code_blocks(text))
    checks = (
        (_inline_codes(source) != _inline_codes(text), "inline code mismatch"),
        (_anchors(source) != _anchors(text), "anchor mismatch"),
        (
            _structural_html_signature(source) != _structural_html_signature(text),
            "html tag mismatch",
        ),
        (
            _dynamic_display_attribute_signatures(source)
            != _dynamic_display_attribute_signatures(text),
            "html display expression mismatch",
        ),
        (_html_img_sources(source) != _html_img_sources(text), "html image source mismatch"),
        (
            _dynamic_display_attribute_signatures(source, tag_name="img")
            != _dynamic_display_attribute_signatures(text, tag_name="img"),
            "html image display expression mismatch",
        ),
        (
            html_code_contents(source_body) != html_code_contents(translated_body),
            "html code mismatch",
        ),
    )
    return [label for failed, label in checks if failed]


def _markdown_structure_issues(text: str, source: str) -> list[str]:
    """Markdown 코드·제목·목록·표 구조 보존 이슈 수집.

    Args:
        text: 검사할 locale 문서.
        source: 비교 기준 영어 문서.

    Returns:
        발견 순서의 Markdown 구조 위반 label.
    """

    checks = (
        (
            _normalized_fenced_code_blocks(source)
            != _normalized_fenced_code_blocks(text),
            "code block mismatch",
        ),
        (_heading_levels(source) != _heading_levels(text), "heading mismatch"),
        (_heading_lines(source) != _heading_lines(text), "heading text mismatch"),
        (
            list_structure_signature(source) != list_structure_signature(text),
            "list marker mismatch",
        ),
        (
            table_structure_signature(source) != table_structure_signature(text),
            "table structure mismatch",
        ),
    )
    return [label for failed, label in checks if failed]


def _front_matter_issues(text: str, source: str) -> list[str]:
    """front matter 구조·번역값 계약 이슈 수집.

    Args:
        text: 검사할 locale 문서.
        source: 비교 기준 영어 문서.

    Returns:
        발견 순서의 front matter 위반 label.
    """

    expected = front_matter_contract(source)
    actual = front_matter_contract(text)
    issues: list[str] = []
    if (
        not expected.valid
        or not actual.valid
        or (
            not is_locale_routing_front_matter(expected, actual)
            and (
                expected.present != actual.present
                or expected.signature != actual.signature
            )
        )
    ):
        issues.append("front matter structure mismatch")
    if _front_matter_title(source) != _front_matter_title(text):
        issues.append("front matter title mismatch")
    description = front_matter_description(text)
    if description is not None and not description.valid:
        issues.append("front matter description invalid")
    return issues


def _annotation_issues(
    text: str,
    source: str,
    *,
    allow_source_echo: bool,
) -> list[str]:
    """원문 annotation·번역 문장 계약 이슈 수집.

    Args:
        text: 검사할 locale 문서.
        source: 비교 기준 영어 문서.
        allow_source_echo: 영어 원문 prose 잔존 허용 여부.

    Returns:
        발견 순서의 annotation·문장 위반 label.
    """

    checks = (
        (not _source_comments_are_preserved(text, source), "source comment mismatch"),
        (bool(missing_original_comments(text, source)), "missing original comment"),
        (
            not allow_source_echo and _has_untranslated_source_prose(text, source),
            "untranslated source text",
        ),
        (
            not _annotation_sentence_cardinality_is_valid(text, source),
            "sentence cardinality mismatch",
        ),
    )
    return [label for failed, label in checks if failed]


def verify(
    text: str,
    source: str | None = None,
    *,
    version: str | None = None,
    allow_source_echo: bool = False,
    registry: StaleLinkRegistry = DEFAULT_STALE_LINK_REGISTRY,
) -> list[str]:
    """Locale 문서의 잔존 패턴과 원문 구조 보존 검증.

    Args:
        text: 검사할 locale 문서.
        source: 비교 기준 영어 문서. 없으면 잔존 패턴만 검사.
        version: 내부 문서 링크 정규화에 사용할 현재 버전.
        allow_source_echo: 영어 원문 prose 잔존 허용 여부.
        registry: 알려진 원문 stale link 정규화 규칙.

    Returns:
        발견 순서의 위반 label. 빈 목록이면 통과.
    """
    issues = _basic_issues(text, source)
    if source is None:
        return issues
    issues.extend(
        _link_issues(text, source, version=version, registry=registry)
    )
    issues.extend(_html_structure_issues(text, source))
    issues.extend(_markdown_structure_issues(text, source))
    issues.extend(_front_matter_issues(text, source))
    issues.extend(
        _annotation_issues(text, source, allow_source_echo=allow_source_echo)
    )
    return issues
