"""번역 비교에 사용할 작업 사본의 결정적 전처리.

원문(``i18n/en``)은 그대로 보존하고 번역 파이프라인의 작업 사본에만 적용.

- Base64 이미지: 플레이스홀더로 치환하고 복원용 매핑 생성
- 페이지 디자인용 ``<style>``: 코드 블록 밖에서만 제거
- 제목 옆 ``{.class}``: 스타일 클래스 제거
- 명확한 들여쓰기 코드: 코드 펜스 블록으로 변환

목록의 들여쓰기인지 코드 블록인지 불분명해 의미가 달라질 수 있는 구조는 변경 대상에서 제외.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

from ..common.markdown import (
    _inline_code_spans,
    closes_fence,
    fence_token,
    strip_title_attrs,
)

# Markdown과 HTML 이미지의 `data:image/...;base64,...` 패턴.
_BASE64_RE = re.compile(
    r"data:image/[a-zA-Z0-9.+-]+"
    r"(?:;[^;,=\s\"'<>]+=[^;,\s\"'<>]+)*"
    r";base64,[A-Za-z0-9+/=]+?(?=/>|$|[)>\"'\s])"
)
_INDENTED_CODE_RE = re.compile(r"^(?: {4}|\t)(.*)$")
_LIST_MARKER_RE = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s)")
_STYLE_OPEN = "<style"
_STYLE_CLOSE = "</style>"


@dataclass
class Preprocessed:
    """정규화된 작업 사본과 원본 복원용 플레이스홀더 매핑.

    Attributes:
        text: 정규화된 문서 내용.
        placeholders: 플레이스홀더와 원본 데이터 URI의 대응표.
    """

    text: str
    placeholders: dict[str, str] = field(default_factory=dict)


@dataclass
class PreprocessedPair:
    """동일한 할당표로 전처리한 이전·현재 작업 사본.

    Attributes:
        previous: 이전 영어 원문의 전처리 결과.
        current: 현재 영어 원문의 전처리 결과.
    """

    previous: Preprocessed
    current: Preprocessed


def preprocess_pair(previous: str, current: str) -> PreprocessedPair:
    """이전·현재 원문에 동일한 결정적 플레이스홀더 할당 적용.

    Args:
        previous: 승인 기준인 이전 영어 원문.
        current: 번역 후보인 현재 영어 원문.

    Returns:
        동일한 할당표로 정규화한 이전·현재 작업 사본.

    Raises:
        ValueError: 서로 다른 데이터 URI의 SHA-256 해시값이 충돌한 경우.
    """

    allocation = _allocate_base64_placeholders(previous, current)
    return PreprocessedPair(
        previous=_preprocess_with_allocation(previous, allocation),
        current=_preprocess_with_allocation(current, allocation),
    )


def _segment_fence_token(line: str) -> str | None:
    """CommonMark에서 허용하는 위치의 코드 펜스 구분자 반환."""

    stripped = line.lstrip(" ")
    if len(line) - len(stripped) > 3 or stripped.startswith("\t"):
        return None
    while stripped.startswith(">"):
        stripped = stripped[1:]
        if stripped.startswith((" ", "\t")):
            stripped = stripped[1:]
        indented = stripped.lstrip(" ")
        if len(stripped) - len(indented) > 3 or indented.startswith("\t"):
            return None
        stripped = indented
    return fence_token(line)


def _split_code_segments(text: str) -> list[tuple[str, bool]]:
    """코드 펜스 블록 포함 여부에 따라 텍스트 분할."""
    segments: list[tuple[str, bool]] = []
    pending: list[str] = []
    in_code = False
    fence = ""

    def flush(is_code: bool) -> None:
        """대기 중인 줄을 지정한 구간으로 확정."""

        if pending:
            segments.append(("".join(pending), is_code))
            pending.clear()

    for line in text.splitlines(keepends=True):
        token = _segment_fence_token(line)
        if token and not in_code:
            flush(False)
            in_code = True
            fence = token
            pending.append(line)
            continue

        pending.append(line)
        if token and in_code and closes_fence(line, fence):
            flush(True)
            in_code = False
            fence = ""

    flush(in_code)
    if not segments:
        segments.append(("", False))
    return segments


# 줄 시작 구조로 코드 또는 설정을 식별하는 패턴.
# Blade 디렉티브, `.env`, YAML, 셸 명령, 경로 등 판별.
# 일치하는 들여쓰기 블록을 코드 펜스 블록으로 변환해 영어 주석이 코드에 잘못 병기되는 문제 방지.
_STRUCT_CODE_PATS = (
    re.compile(r"^\s*@\w+"),                        # Blade/Envoy 디렉티브(`@auth`, `@once` 등)
    re.compile(r"^\s*[A-Za-z][\w-]*="),             # `.env`·설정(`STRIPE_KEY=...`, `process_name=...`)
    re.compile(r"^\s*(//|#\s|/\*)"),               # 소스 코드 주석
    re.compile(r"^\s*[\w./-]+:\s\S"),               # YAML/설정의 `키: 값`
    re.compile(r"^\s*[\w-]+:\s*$"),                 # YAML의 `키:`
    re.compile(
        r"^\s*[\w.]+\s*-\s*(integer|string|timestamp|bigInteger|boolean"
        r"|text|date|float|increments|json|uuid|id|datetime|char|decimal|enum|binary)\b"
    ),                                              # DB 스키마 열(`id - integer` 등)
    re.compile(r"^\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"),  # IP 주소
    re.compile(r"^\s*[a-z_][\w]*\s*$"),             # 단일 소문자 토큰(테이블명 등)
    re.compile(r"^\s*[\w-]+\.\w{1,6}\s*$"),         # 파일명(`messages.php` 등)
    re.compile(
        r"^\s*</?(?!(?:div|span|img|p|a|br|hr|i|b|em|strong|small|sup|sub"
        r"|ul|ol|li|h[1-6]|blockquote|figure|figcaption)\b)[a-zA-Z][\w-]*[\s/>]"
    ),  # 코드 예시의 HTML/Blade 태그(콘텐츠/인라인 태그 제외)
    re.compile(r"^\s*/[\w][\w./-]*\s*$"),           # 경로/디렉터리 트리
    re.compile(r"^\s*(alias\s|php\d|ssh\s|cd\s|ls\s|git\s|vendor/bin)"),  # 셸 명령
    re.compile(r"^\s*\[[\w:.-]+\]\s*$"),            # INI 섹션(`[program:horizon]` 등)
    re.compile(r"^\s*[a-zA-Z_]\w*(\.\w+)*\("),      # 함수 호출(`mix.js(...)` 등)
)


def _looks_like_code(lines: list[str]) -> bool:
    """들여쓰기 영역이 명확한 코드 또는 설정인지 판별."""

    markers = (
        "<?php",
        "=>",
        "::",
        "->",
        "$",
        "{",
        "}",
        ";",
        "php artisan",
        "composer ",
        "npm ",
        "Route::",
        "use ",
        "namespace ",
        "class ",
        "function ",
        "/**",
        "*/",
    )
    if any(any(marker in line for marker in markers) for line in lines):
        return True
    nonblank = [line for line in lines if line.strip()]
    if not nonblank:
        return False
    hits = sum(
        1 for line in nonblank if any(pat.match(line) for pat in _STRUCT_CODE_PATS)
    )
    return hits >= max(1, (len(nonblank) + 1) // 2)


def _strip_code_indent(line: str) -> str:
    """코드 줄의 선행 탭 또는 공백 네 칸 제거."""

    if line.startswith("\t"):
        return line[1:]
    return line[4:] if line.startswith("    ") else line


def _line_comment_state(
    line: str,
    *,
    offset: int,
    inline_spans: list[tuple[int, int, str]],
    inline_index: int,
    in_comment: bool,
) -> tuple[bool, int, bool]:
    """한 줄의 보호 대상 HTML 주석 상태 추적.

    Args:
        line: 원본 줄.
        offset: 문서에서 줄의 시작 위치.
        inline_spans: 인라인 코드 범위 목록.
        inline_index: 현재 인라인 코드 범위 위치.
        in_comment: 이전 줄에서 시작한 주석 내부 여부.

    Returns:
        줄 보호 여부, 다음 인라인 범위 위치, 다음 주석 내부 상태.
    """

    protected = in_comment or bool(_INDENTED_CODE_RE.match(line))
    cursor = 0
    while cursor < len(line):
        if in_comment:
            close = line.find("-->", cursor)
            if close < 0:
                break
            in_comment = False
            cursor = close + 3
            continue
        opener = line.find("<!--", cursor)
        if opener < 0:
            break
        absolute_opener = offset + opener
        while (
            inline_index < len(inline_spans)
            and inline_spans[inline_index][1] <= absolute_opener
        ):
            inline_index += 1
        if (
            inline_index < len(inline_spans)
            and inline_spans[inline_index][0]
            <= absolute_opener
            < inline_spans[inline_index][1]
        ):
            cursor = inline_spans[inline_index][1] - offset
            continue
        protected = True
        in_comment = True
        cursor = opener + 4
    return protected, inline_index, in_comment


def _strip_title_attrs_outside_protected_regions(text: str) -> str:
    """HTML 주석과 들여쓰기 코드 밖의 제목 클래스 제거."""

    inline_spans = _inline_code_spans(text)
    inline_index = 0
    in_comment = False
    offset = 0
    out: list[str] = []

    for line in text.splitlines(keepends=True):
        protected, inline_index, in_comment = _line_comment_state(
            line,
            offset=offset,
            inline_spans=inline_spans,
            inline_index=inline_index,
            in_comment=in_comment,
        )
        out.append(line if protected else strip_title_attrs(line))
        offset += len(line)
    return "".join(out)


def _containing_inline_span_end(
    position: int,
    spans: list[tuple[int, int, str]],
) -> int | None:
    """지정 위치를 포함하는 인라인 코드 범위의 끝 조회.

    Args:
        position: 확인할 문자열 위치.
        spans: 인라인 코드 범위 목록.

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


def _next_style_opening(
    text: str,
    lower: str,
    start_at: int,
    inline_spans: list[tuple[int, int, str]],
) -> tuple[int, int] | None:
    """제거 가능한 다음 ``style`` 시작 태그 범위 탐색.

    Args:
        text: 원본 문서.
        lower: 소문자로 변환한 문서.
        start_at: 검색 시작 위치.
        inline_spans: 인라인 코드 범위 목록.

    Returns:
        시작 태그의 시작과 끝 위치. 없으면 ``None``.
    """

    cursor = start_at
    while True:
        start = lower.find(_STYLE_OPEN, cursor)
        if start < 0:
            return None
        code_span_end = _containing_inline_span_end(start, inline_spans)
        if code_span_end is not None:
            cursor = code_span_end
            continue
        after_open = start + len(_STYLE_OPEN)
        if after_open < len(text) and not (
            text[after_open].isspace() or text[after_open] == ">"
        ):
            cursor = after_open
            continue
        line_start = text.rfind("\n", 0, start) + 1
        if text[line_start:start] not in ("", " ", "  ", "   "):
            cursor = after_open
            continue
        tag_end = text.find(">", after_open)
        return None if tag_end < 0 else (start, tag_end)


def _style_close_start(
    lower: str,
    start_at: int,
    inline_spans: list[tuple[int, int, str]],
) -> int | None:
    """인라인 코드를 제외한 ``style`` 닫는 태그 위치 탐색.

    Args:
        lower: 소문자로 변환한 문서.
        start_at: 검색 시작 위치.
        inline_spans: 인라인 코드 범위 목록.

    Returns:
        닫는 태그 시작 위치. 없으면 ``None``.
    """

    close_start = lower.find(_STYLE_CLOSE, start_at)
    while close_start >= 0:
        code_span_end = _containing_inline_span_end(close_start, inline_spans)
        if code_span_end is None:
            return close_start
        close_start = lower.find(_STYLE_CLOSE, code_span_end)
    return None


def _strip_style_blocks(text: str) -> str:
    """보호 영역 밖에서 닫힌 페이지 ``<style>`` 블록 제거."""

    out: list[str] = []
    lower = text.lower()
    inline_code_spans = _inline_code_spans(text)
    index = 0

    while index < len(text):
        opening = _next_style_opening(text, lower, index, inline_code_spans)
        if opening is None:
            out.append(text[index:])
            break
        start, tag_end = opening

        remove_start = start
        while remove_start > index and text[remove_start - 1] in " \t":
            remove_start -= 1

        close_start = _style_close_start(
            lower,
            tag_end + 1,
            inline_code_spans,
        )
        if close_start is None:
            out.append(text[index:])
            break

        remove_end = close_start + len(_STYLE_CLOSE)
        while remove_end < len(text) and text[remove_end] in " \t\r\n":
            remove_end += 1

        out.append(text[index:remove_start])
        index = remove_end
    return "".join(out)


def _is_ordered_item_opener(stripped: str) -> bool:
    """줄이 하위 구조를 여는 순서 있는 목록 항목인지 판별."""

    marker_end = 0
    while marker_end < len(stripped) and stripped[marker_end].isdigit():
        marker_end += 1
    if marker_end == 0 or marker_end >= len(stripped) or stripped[marker_end] != ".":
        return False
    remainder = stripped[marker_end + 1:]
    return bool(remainder[:1].isspace() and remainder.rstrip().endswith(":"))


def _is_named_child_opener(stripped: str) -> bool:
    """줄이 이름 있는 하위 구조를 여는지 판별."""

    if not stripped.endswith(":"):
        return False
    name = stripped[:-1].strip()
    return bool(name) and all(char.isalnum() or char in "_.-" for char in name)


def _opens_indented_children(line: str) -> bool:
    """줄이 들여쓰기 하위 구조를 여는지 판별."""

    stripped = line.lstrip()
    if stripped.startswith("@"):
        return True
    if _is_ordered_item_opener(stripped):
        return True
    if stripped[:2] in ("- ", "* ", "+ ") and stripped.rstrip().endswith(":"):
        return True
    return _is_named_child_opener(stripped)


def _has_indented_parent(lines: list[str], index: int) -> bool:
    """대상 줄이 목록 또는 디렉티브의 하위 구조인지 판별."""

    cursor = index - 1
    saw_blank = False
    while cursor >= 0:
        line = lines[cursor]
        if line == "":
            saw_blank = True
            cursor -= 1
            continue
        if _INDENTED_CODE_RE.match(line):
            cursor -= 1
            continue
        if _LIST_MARKER_RE.match(line):
            return True
        return not saw_blank and _opens_indented_children(line)
    return False


def _convert_indented_code_blocks(text: str) -> str:
    """명확한 들여쓰기 코드 블록을 코드 펜스 블록으로 변환."""

    rebuilt_segments: list[str] = []
    for segment, is_code in _split_code_segments(text):
        if is_code:
            rebuilt_segments.append(segment)
            continue

        lines = segment.split("\n")
        out: list[str] = []
        i = 0
        while i < len(lines):
            line = lines[i]
            match = _INDENTED_CODE_RE.match(line)
            if not match or _LIST_MARKER_RE.match(match.group(1)):
                out.append(line)
                i += 1
                continue
            if _has_indented_parent(lines, i):
                out.append(line)
                i += 1
                continue

            block: list[str] = []
            while i < len(lines):
                current = lines[i]
                current_match = _INDENTED_CODE_RE.match(current)
                if current == "":
                    next_nonblank = next(
                        (lines[k] for k in range(i + 1, len(lines)) if lines[k] != ""),
                        "",
                    )
                    next_match = _INDENTED_CODE_RE.match(next_nonblank)
                    if next_match and (
                        not _LIST_MARKER_RE.match(next_match.group(1))
                        or _looks_like_code(block)
                    ):
                        block.append("")
                        i += 1
                        continue
                    break
                if not current_match:
                    break
                stripped = current_match.group(1)
                if _LIST_MARKER_RE.match(stripped) and not _looks_like_code(block):
                    break
                block.append(_strip_code_indent(current))
                i += 1

            if _looks_like_code(block):
                longest_backtick_run = max(
                    (
                        len(match.group(0))
                        for item in block
                        for match in re.finditer(r"`+", item)
                    ),
                    default=0,
                )
                fence = "`" * max(3, longest_backtick_run + 1)
                out.append(fence)
                out.extend(block)
                out.append(fence)
            else:
                out.extend(("    " + item) if item else "" for item in block)

        rebuilt_segments.append("\n".join(out))
    return "".join(rebuilt_segments)


def _outside_inline_code(text: str) -> list[tuple[str, bool]]:
    """인라인 코드 범위 여부에 따라 텍스트 분할."""

    segments: list[tuple[str, bool]] = []
    cursor = 0
    for start, end, _body in _inline_code_spans(text):
        if cursor < start:
            segments.append((text[cursor:start], False))
        segments.append((text[start:end], True))
        cursor = end
    if cursor < len(text):
        segments.append((text[cursor:], False))
    if not segments:
        segments.append(("", False))
    return segments


def _base64_values(content: str) -> set[str]:
    """보호 영역 밖의 고유 Base64 이미지 데이터 URI 수집."""

    values: set[str] = set()
    for fenced_segment, is_fenced in _split_code_segments(content):
        if is_fenced:
            continue
        for inline_segment, is_inline in _outside_inline_code(fenced_segment):
            if not is_inline:
                values.update(
                    match.group(0)
                    for match in _BASE64_RE.finditer(inline_segment)
                )
    return values


def _allocate_base64_placeholders(previous: str, current: str) -> dict[str, str]:
    """두 원문의 데이터 URI에 결정적 플레이스홀더 할당.

    Args:
        previous: 이전 영어 원문.
        current: 현재 영어 원문.

    Returns:
        데이터 URI를 키로 사용하는 플레이스홀더 할당표.

    Raises:
        ValueError: 서로 다른 데이터 URI의 SHA-256 해시값이 충돌한 경우.
    """

    by_digest: dict[bytes, str] = {}
    for value in _base64_values(previous) | _base64_values(current):
        digest = hashlib.sha256(value.encode("utf-8")).digest()
        existing = by_digest.get(digest)
        if existing is not None and existing != value:
            raise ValueError("different data URIs produced the same SHA-256 digest")
        by_digest[digest] = value

    allocation: dict[str, str] = {}
    placeholder_number = 0
    combined = previous + current
    for digest in sorted(by_digest):
        while True:
            placeholder_number += 1
            placeholder = f"__BASE64_IMAGE_{placeholder_number:03d}__"
            if placeholder not in combined:
                break
        allocation[by_digest[digest]] = placeholder
    return allocation


def _replace_base64(content: str, allocation: dict[str, str]) -> Preprocessed:
    """보호 영역 밖의 Base64 데이터 URI를 할당된 토큰으로 치환."""

    placeholders: dict[str, str] = {}
    rebuilt_fenced: list[str] = []

    for fenced_segment, is_fenced in _split_code_segments(content):
        if is_fenced:
            rebuilt_fenced.append(fenced_segment)
            continue

        rebuilt_inline: list[str] = []
        for inline_segment, is_inline in _outside_inline_code(fenced_segment):
            if is_inline:
                rebuilt_inline.append(inline_segment)
                continue

            def replace(match: re.Match[str]) -> str:
                """일치한 데이터 URI를 토큰으로 치환하고 복원표에 기록."""

                value = match.group(0)
                placeholder = allocation[value]
                existing = placeholders.get(placeholder)
                if existing is not None and existing != value:
                    raise ValueError("a placeholder maps to more than one data URI")
                placeholders[placeholder] = value
                return placeholder

            rebuilt_inline.append(_BASE64_RE.sub(replace, inline_segment))
        rebuilt_fenced.append("".join(rebuilt_inline))

    return Preprocessed(text="".join(rebuilt_fenced), placeholders=placeholders)


def _preprocess_with_allocation(
    content: str,
    allocation: dict[str, str],
) -> Preprocessed:
    """확정된 할당표로 단일 작업 사본 정규화."""

    result = _replace_base64(content, allocation)
    text = result.text

    # 코드 블록 밖에서만 `<style>`과 제목의 `{.class}` 제거.
    # 들여쓰기 코드 변환보다 먼저 적용.
    # 먼저 들여쓰기 코드를 변환하면 내부 CSS가 코드 펜스로 보호되어 페이지 `<style>` 블록이 남는 문제 발생.
    rebuilt: list[str] = []
    for segment, is_code in _split_code_segments(text):
        if is_code:
            rebuilt.append(segment)
            continue
        segment = _strip_style_blocks(segment)
        segment = _strip_title_attrs_outside_protected_regions(segment)
        rebuilt.append(segment)
    text = "".join(rebuilt)

    # 명확한 들여쓰기 코드 블록을 코드 펜스 블록으로 변환해 후속 단계에서 보호.
    text = _convert_indented_code_blocks(text)

    result.text = text
    return result


def preprocess(content: str) -> Preprocessed:
    """단일 원문을 결정적 플레이스홀더 할당으로 정규화.

    Args:
        content: 정규화할 영어 원문.

    Returns:
        정규화된 작업 사본과 복원용 플레이스홀더 매핑.
    """

    return preprocess_pair("", content).current
