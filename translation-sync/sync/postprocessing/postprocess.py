"""번역 결과에 적용하는 결정론적 Markdown 후처리.

- ``<img>`` 태그를 자체 닫힘 형식으로 변환
- 레거시 경고문을 GFM 경고문으로 표준화
- ``{{version}}`` 플레이스홀더 치환
- 제목 뒤의 ``{.class}`` 잔여물 제거
- 알려진 오래된 업스트림 링크 대상과 폐기된 목록 레이블 정규화
- HTML 주석 안의 JavaScript 주석 종료 구분자 무력화
- GFM 경고문 안의 코드 펜스와 본문에 인용문 표식 보완
- Base64 이미지 플레이스홀더 복원
- 명시적 강제 줄바꿈을 제외한 줄 끝 공백 제거
"""
from __future__ import annotations

import re
from typing import Mapping

from ..common.admonitions import parse_legacy_admonition_line
from ..common.javascript import balanced_expression_end
from ..common.markdown import (
    MarkdownLink,
    _fenced_code_ranges,
    _inline_code_spans,
    _strip_reference_container,
    closes_fence,
    fence_token,
    html_comment_spans,
    is_heading_line,
    markdown_links,
    mask_html_comments,
    strip_html_comments,
    strip_title_attrs,
)
from ..common.stale_links import (
    DEFAULT_STALE_LINK_REGISTRY,
    StaleLinkRegistry,
    canonical_stale_link_target,
)

_VERSION_RE = re.compile(r"\{\{\s*version\s*\}\}")
_GFM_ADMONITION_RE = re.compile(
    r"^>\s*\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT)]\s*$", re.IGNORECASE
)
_GFM_ADMONITION_TYPE_RE = re.compile(
    r"^[ \t]{0,3}\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT)]",
)
_UNQUOTED_ATTRIBUTE_AT_END_RE = re.compile(
    r"(?:^|\s)[A-Za-z_:][\w:.-]*\s*=\s*[^\s\"'`{][^\s]*$"
)
_LIST_ITEM_PREFIX_RE = re.compile(r"^[ \t]*(?:[-*+]\s+|\d+[.)]\s+)$")


def _map_outside_code_blocks(text: str, transform) -> str:
    """코드 펜스 밖의 연속 구간에만 변환 함수 적용."""

    out: list[str] = []
    pending: list[str] = []
    in_code = False
    fence = ""

    def flush_pending() -> None:
        """대기 중인 코드 펜스 외부 구간을 변환해 결과에 추가."""

        if pending:
            out.append(transform("".join(pending)))
            pending.clear()

    for line in text.splitlines(keepends=True):
        token = fence_token(line)
        if token:
            if not in_code:
                flush_pending()
                in_code = True
                fence = token
                out.append(line)
                continue
            if closes_fence(line, fence):
                in_code = False
                fence = ""
                out.append(line)
                continue

        if in_code:
            out.append(line)
        else:
            pending.append(line)

    flush_pending()
    return "".join(out)


def _map_outside_html_comments(text: str, transform) -> str:
    """HTML 주석 밖의 연속 구간에만 변환 함수 적용."""

    out: list[str] = []
    index = 0
    for start, end, _body in html_comment_spans(text):
        out.append(transform(text[index:start]))
        out.append(text[start:end])
        index = end
    out.append(transform(text[index:]))
    return "".join(out)


def _containing_span_end(
    position: int,
    spans: list[tuple[int, int, str]],
) -> int | None:
    """지정 위치를 포함하는 보호 범위의 끝 위치 조회.

    Args:
        position: 확인할 문자열 위치.
        spans: 시작·끝·본문으로 구성된 보호 범위 목록.

    Returns:
        포함하는 범위의 끝 위치. 없으면 ``None``.
    """

    return next(
        (
            end
            for span_start, end, _body in spans
            if span_start <= position < end
        ),
        None,
    )


def _img_tag_end(text: str, after_name: int) -> int | None:
    """속성 따옴표와 표현식을 건너뛰어 ``img`` 태그 종료 위치 탐색.

    Args:
        text: 태그를 포함한 문자열.
        after_name: ``<img`` 바로 다음 위치.

    Returns:
        닫는 ``>`` 위치. 닫히지 않았으면 ``None``.
    """

    position = after_name
    while position < len(text):
        char = text[position]
        if char in ("\"", "'"):
            quote = char
            position = text.find(quote, position + 1)
            if position < 0:
                return None
            position += 1
            continue
        if char == "{":
            expression_end = balanced_expression_end(text, position)
            if expression_end is None:
                return None
            position = expression_end
            continue
        if char == ">":
            return position
        position += 1
    return None


def _self_closing_img_tag(text: str, start: int, end: int) -> str:
    """단일 닫힌 ``img`` 태그를 자체 닫힘 형식으로 변환.

    Args:
        text: 태그를 포함한 문자열.
        start: ``<img`` 시작 위치.
        end: 닫는 ``>`` 위치.

    Returns:
        자체 닫힘으로 정규화한 태그.
    """

    after_name = start + len("<img")
    attrs = text[after_name:end].strip()
    if attrs.endswith("/"):
        return text[start : end + 1]
    if not attrs:
        return "<img/>"
    separator = " " if _UNQUOTED_ATTRIBUTE_AT_END_RE.search(attrs) else ""
    return f"<img {attrs}{separator}/>"


def _img_self_closing(text: str) -> str:
    """인라인 코드 밖의 닫히지 않은 ``<img>`` 태그를 자체 닫힘 형식으로 변환."""

    out: list[str] = []
    lower = text.lower()
    inline_code_spans = _inline_code_spans(text)
    index = 0
    while index < len(text):
        start = lower.find("<img", index)
        if start < 0:
            out.append(text[index:])
            break
        code_span_end = _containing_span_end(start, inline_code_spans)
        if code_span_end is not None:
            out.append(text[index:code_span_end])
            index = code_span_end
            continue
        after_name = start + len("<img")
        if after_name < len(text) and not (
            text[after_name].isspace() or text[after_name] in "/>"
        ):
            out.append(text[index:after_name])
            index = after_name
            continue
        end = _img_tag_end(text, after_name)
        if end is None:
            out.append(text[index:])
            break

        out.append(text[index:start])
        out.append(_self_closing_img_tag(text, start, end))
        index = end + 1
    return "".join(out)


def img_self_closing(text: str) -> str:
    """HTML 주석과 인라인 코드를 보존하며 ``<img>`` 태그를 자체 닫힘 형식으로 정규화."""

    return _map_outside_html_comments(text, _img_self_closing)


def _standardized_note_lines(line: str) -> list[str] | None:
    """지원하는 레거시 경고문 한 줄을 표준 GFM 경고문으로 변환."""

    note = parse_legacy_admonition_line(line)
    if note is None:
        return None

    lines = [f"> [!{note.kind}]"]
    if note.body:
        lines.append(f"> {note.body}")
    return lines


def _continue_admonition_line(line: str) -> tuple[str, bool]:
    """경고문 본문 줄에 인용문 표식을 보완하고 경고문 지속 여부 반환."""

    if not line.strip():
        return line, False
    if line.lstrip().startswith(">"):
        return line, True
    return f"> {line}", True


def _standardize_admonitions(text: str) -> str:
    """레거시 경고문과 이어지는 본문을 GFM 형식으로 정규화."""

    out: list[str] = []
    in_gfm_admonition = False
    for line in text.split("\n"):
        note_lines = _standardized_note_lines(line)
        if note_lines is not None:
            out.extend(note_lines)
            in_gfm_admonition = True
            continue
        if _GFM_ADMONITION_RE.match(line.strip()):
            out.append(line)
            in_gfm_admonition = True
            continue
        if in_gfm_admonition:
            repaired_line, in_gfm_admonition = _continue_admonition_line(line)
            out.append(repaired_line)
            continue
        out.append(line)
    return "\n".join(out)


def standardize_admonitions(text: str) -> str:
    """HTML 주석을 보존하며 레거시 경고문을 GFM 형식으로 정규화."""

    return _map_outside_html_comments(text, _standardize_admonitions)


def standardize_admonitions_outside_code(text: str) -> str:
    """코드 블록 밖에서만 경고문과 이어지는 비인용 본문을 GFM 형식으로 정규화."""

    return _map_outside_code_blocks(text, standardize_admonitions)


def admonition_types(text: str) -> tuple[str, ...]:
    """HTML 주석과 코드 펜스 밖의 표준 GFM 경고문 유형을 문서 순서로 반환."""

    without_comments = strip_html_comments(text)
    normalized = _map_outside_code_blocks(
        without_comments,
        standardize_admonitions,
    )
    types: list[str] = []
    for line in normalized.splitlines():
        logical, containers = _strip_reference_container(line)
        if not containers or containers[-1] != "quote":
            continue
        match = _GFM_ADMONITION_TYPE_RE.match(logical)
        if match:
            types.append(match.group(1).upper())
    return tuple(types)


def _quote_admonition_fences(text: str) -> str:
    """GFM 경고문 안의 코드 펜스와 본문에 인용문 표식 적용."""

    out: list[str] = []
    lines = text.split("\n")
    visible_lines = mask_html_comments(text).split("\n")
    index = 0
    in_gfm_admonition = False
    outer_fence = ""

    while index < len(lines):
        line = lines[index]
        visible = visible_lines[index]
        if outer_fence:
            out.append(line)
            if closes_fence(visible, outer_fence):
                outer_fence = ""
            index += 1
            continue

        if _GFM_ADMONITION_RE.match(visible.strip()):
            out.append(line)
            in_gfm_admonition = True
            index += 1
            continue

        if not in_gfm_admonition:
            out.append(line)
            outer_fence = fence_token(visible) or ""
            index += 1
            continue

        if not visible.strip():
            if line.strip():
                out.append(line if line.lstrip().startswith(">") else f"> {line}")
                index += 1
                continue
            out.append(line)
            in_gfm_admonition = False
            index += 1
            continue

        if visible.lstrip().startswith(">"):
            out.append(line)
            index += 1
            continue

        token = fence_token(visible)
        if token:
            opening_index = index
            while index < len(lines):
                current = lines[index]
                current_visible = visible_lines[index]
                out.append(f"> {current}" if current else ">")
                index += 1
                if index > opening_index + 1 and closes_fence(current_visible, token):
                    break
            continue

        repaired_line, in_gfm_admonition = _continue_admonition_line(line)
        out.append(repaired_line)
        index += 1

    return "\n".join(out)


def _mask_link_excluded_spans(text: str, *, mask_inline_code: bool = True) -> str:
    """링크 정규화에서 제외하는 코드와 HTML 주석 범위를 공백으로 마스킹."""

    chars = list(text)
    spans = [
        (start, end, "") for start, end in _fenced_code_ranges(text)
    ]
    spans.extend(html_comment_spans(text))
    if mask_inline_code:
        spans.extend(_inline_code_spans(text))
    for start, end, _body in spans:
        for index in range(start, end):
            if chars[index] not in "\r\n":
                chars[index] = " "
    return "".join(chars)


def _is_standalone_list_link(text: str, start: int, end: int) -> bool:
    """링크가 목록 항목의 전체 레이블인지 판정."""

    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end < 0:
        line_end = len(text)
    return bool(_LIST_ITEM_PREFIX_RE.fullmatch(text[line_start:start])) and not text[
        end:line_end
    ].strip()


def _heading_label_for_fragment(text: str, fragment: str) -> str | None:
    """같은 문서에서 명시적 앵커 다음의 제목 레이블 조회.

    Args:
        text: 앵커와 제목을 찾을 Markdown 문서.
        fragment: 선행 ``#``을 제외한 앵커 이름.

    Returns:
        앵커 다음의 첫 번째 제목 레이블.
        대응 앵커나 제목이 없으면 ``None``.
    """

    anchor_re = re.compile(
        rf"<a\b[^>]*\b(?:name|id)=[\"']{re.escape(fragment)}[\"'][^>]*>"
        r"(?:[ \t]*</a>)?",
        re.IGNORECASE,
    )
    match = anchor_re.search(text)
    if match is None:
        return None
    for line in strip_html_comments(text[match.end() :]).splitlines():
        if not line.strip():
            continue
        if not is_heading_line(line):
            return None
        stripped = line.lstrip(" ")
        level = len(stripped) - len(stripped.lstrip("#"))
        return re.sub(r"\s+#+\s*$", "", stripped[level:].strip())
    return None


def normalize_retired_list_labels(
    text: str,
    version: str,
    *,
    registry: StaleLinkRegistry = DEFAULT_STALE_LINK_REGISTRY,
) -> str:
    """폐기 대상 목록 레이블에서 이전 실행이 추가한 인라인 코드 구분자 제거."""
    labels = {
        rule.source.removeprefix("#").replace("-", " ").title()
        for rule in registry.rules
        if rule.version == version
        and rule.target is None
        and rule.retire_mode == "standalone-list-label"
    }
    if not labels:
        return text
    label_pattern = "|".join(
        sorted((re.escape(label) for label in labels), key=len, reverse=True)
    )
    retired_label_re = re.compile(
        r"(?m)^(?P<prefix>[ \t]*(?:[-*+]\s+|\d+[.)]\s+))"
        rf"`(?P<label>{label_pattern})`(?P<suffix>[ \t]*)$"
    )
    masked = _mask_link_excluded_spans(text, mask_inline_code=False)
    out: list[str] = []
    cursor = 0
    for match in retired_label_re.finditer(masked):
        out.append(text[cursor : match.start()])
        out.append(match.group("prefix") + match.group("label") + match.group("suffix"))
        cursor = match.end()
    out.append(text[cursor:])
    return "".join(out)


def normalize_stale_link_targets(
    text: str,
    version: str,
    *,
    registry: StaleLinkRegistry = DEFAULT_STALE_LINK_REGISTRY,
) -> str:
    """코드와 주석을 보존하며 알려진 오래된 업스트림 링크 대상 보정."""
    masked = _mask_link_excluded_spans(text)
    out: list[str] = []
    cursor = 0
    for link in markdown_links(masked):
        should_replace, replacement = _stale_link_replacement(
            text,
            link,
            version=version,
            registry=registry,
        )
        if not should_replace:
            continue
        out.append(text[cursor : link.start])
        out.append(replacement)
        cursor = link.end
    out.append(text[cursor:])
    return "".join(out)


def _stale_link_replacement(
    text: str,
    link: MarkdownLink,
    *,
    version: str,
    registry: StaleLinkRegistry,
) -> tuple[bool, str]:
    """단일 오래된 링크의 적용 여부와 대체 Markdown 계산.

    Args:
        text: 원본 Markdown 문서.
        link: 마스킹된 문서에서 파싱한 링크.
        version: 대상 문서 버전.
        registry: 오래된 링크 규칙 모음.

    Returns:
        대체 여부와 대체 문자열.
    """

    rule = registry.matching_rule(link.target, version)
    if rule is None:
        return False, ""
    target = canonical_stale_link_target(
        link.target,
        version,
        registry=registry,
    )
    if target == link.target:
        return False, ""
    standalone_list = _is_standalone_list_link(text, link.start, link.end)
    if target is None:
        incompatible_mode = (
            rule.retire_mode == "standalone-list-label" and not standalone_list
        ) or (rule.retire_mode == "bare-inline-code" and standalone_list)
        if incompatible_mode:
            return False, ""
        replacement = (
            link.label
            if rule.retire_mode == "standalone-list-label"
            else f"`{link.label}`"
        )
        return True, replacement
    image = "!" if link.image else ""
    label = link.label
    if standalone_list and target.startswith("#"):
        label = _heading_label_for_fragment(text, target[1:]) or label
    return True, f"{image}[{label}]({target}{link.title})"


def replace_version(text: str, version: str) -> str:
    """모든 버전 플레이스홀더를 대상 버전 문자열로 치환."""

    return _VERSION_RE.sub(version, text)


def restore_placeholders(text: str, placeholders: Mapping[str, str]) -> str:
    """전처리 복원표의 플레이스홀더를 원본 값으로 복원."""

    for key, original in placeholders.items():
        text = text.replace(key, original)
    return text


def strip_trailing_whitespace(text: str) -> str:
    """HTML 주석과 명시적 강제 줄바꿈을 보존하며 줄 끝 공백 제거."""

    out: list[str] = []
    in_code = False
    fence = ""
    lines = text.split("\n")
    visible_lines = mask_html_comments(text).split("\n")
    comment_lines: set[int] = set()
    for start, end, _body in html_comment_spans(text):
        start_line = text.count("\n", 0, start)
        end_line = text.count("\n", 0, max(start, end - 1))
        comment_lines.update(range(start_line, end_line + 1))

    for line_number, (line, visible) in enumerate(
        zip(lines, visible_lines, strict=True)
    ):
        token = fence_token(visible)
        was_in_code = in_code
        if token:
            if not in_code:
                in_code = True
                fence = token
            elif closes_fence(line, fence):
                in_code = False
                fence = ""

        if line_number in comment_lines:
            out.append(line)
            continue

        stripped = line.rstrip(" \t")
        if (
            not was_in_code
            and token is None
            and not is_heading_line(stripped)
            and stripped
            and line.endswith("  ")
        ):
            out.append(stripped + "  ")
        else:
            out.append(stripped)
    return "\n".join(out)


def escape_html_comments(text: str) -> str:
    """MDX가 HTML 주석을 변환할 때 손상되는 JavaScript 주석 종료 구분자 무력화."""
    out: list[str] = []
    index = 0
    for start, end, body in html_comment_spans(text):
        out.append(text[index:start])
        out.append(f"<!--{body.replace('*/', '*&#47;')}-->")
        index = end
    out.append(text[index:])
    return "".join(out)


def _postprocess_markdown_body(
    text: str,
    version: str,
    registry: StaleLinkRegistry,
) -> str:
    """코드 펜스 밖의 Markdown 본문에 순서가 고정된 형식 변환 적용."""

    text = replace_version(text, version)
    text = img_self_closing(text)
    text = standardize_admonitions(text)
    text = strip_title_attrs(text)
    text = normalize_stale_link_targets(text, version, registry=registry)
    text = normalize_retired_list_labels(text, version, registry=registry)
    text = escape_html_comments(text)
    return text


def postprocess(
    text: str,
    version: str,
    placeholders: Mapping[str, str],
    *,
    registry: StaleLinkRegistry = DEFAULT_STALE_LINK_REGISTRY,
) -> str:
    """번역 Markdown을 정규화하고 현재 복원표의 원본 값 복원."""

    text = _map_outside_code_blocks(
        text, lambda body: _postprocess_markdown_body(body, version, registry)
    )
    text = _quote_admonition_fences(text)
    text = restore_placeholders(text, placeholders)
    text = strip_trailing_whitespace(text)
    return text
