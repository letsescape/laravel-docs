"""번역 비교용 작업 사본의 결정적 전처리.

원문 source는 raw 상태로 보존하고 번역 pipeline의 작업 사본에만 적용.
Base64 image data를 placeholder로 보호하고 페이지 전용 장식을 제거한 뒤,
명확한 들여쓰기 코드 블록을 fenced code block으로 정규화.
모호한 목록 또는 문장 구조는 변경 대상에서 제외.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

from ..common.markdown import _inline_code_spans, closes_fence, strip_title_attrs

_BASE64_RE = re.compile(
    r"data:image/[a-zA-Z0-9.+-]+"
    r"(?:;[^;,=\s\"'<>]+=[^;,\s\"'<>]+)*"
    r";base64,[A-Za-z0-9+/=]+?(?=/>|$|[)>\"'\s])"
)
_FENCE_RE = re.compile(r"^([ \t]*)(`{3,}|~{3,})", re.MULTILINE)
_INDENTED_CODE_RE = re.compile(r"^(?: {4}|\t)(.*)$")
_LIST_MARKER_RE = re.compile(r"^\s*(?:[-*+]\s|\d+\.\s)")
_STYLE_OPEN = "<style"
_STYLE_CLOSE = "</style>"


@dataclass
class Preprocessed:
    """정규화된 작업 사본과 원본 복원용 placeholder 매핑.

    Attributes:
        text: 정규화된 문서 내용.
        placeholders: placeholder와 원본 data URI의 대응표.
    """

    text: str
    placeholders: dict[str, str] = field(default_factory=dict)


@dataclass
class PreprocessedPair:
    """같은 할당표로 전처리한 이전·현재 작업 사본.

    Attributes:
        previous: 이전 영어 원문의 전처리 결과.
        current: 현재 영어 원문의 전처리 결과.
    """

    previous: Preprocessed
    current: Preprocessed


def preprocess_pair(previous: str, current: str) -> PreprocessedPair:
    """이전·현재 원문에 같은 결정적 placeholder 할당 적용.

    Args:
        previous: 승인 기준본의 이전 영어 원문.
        current: candidate의 현재 영어 원문.

    Returns:
        같은 할당표로 정규화한 이전·현재 작업 사본.

    Raises:
        ValueError: 서로 다른 data URI의 digest가 충돌한 경우.
    """

    allocation = _allocate_base64_placeholders(previous, current)
    return PreprocessedPair(
        previous=_preprocess_with_allocation(previous, allocation),
        current=_preprocess_with_allocation(current, allocation),
    )


def _split_code_segments(text: str) -> list[tuple[str, bool]]:
    """fenced code block 여부에 따라 텍스트 분할."""

    segments: list[tuple[str, bool]] = []
    in_code = False
    fence = ""
    last = 0
    for match in _FENCE_RE.finditer(text):
        token = match.group(2)
        if not in_code:
            in_code, fence = True, token
            segments.append((text[last : match.start()], False))
            last = match.start()
        elif closes_fence(token, fence):
            in_code = False
            segments.append((text[last : match.end()], True))
            last = match.end()
    segments.append((text[last:], in_code))
    return segments


_STRUCT_CODE_PATS = (
    re.compile(r"^\s*@\w+"),
    re.compile(r"^\s*[A-Za-z][\w-]*="),
    re.compile(r"^\s*(//|#\s|/\*)"),
    re.compile(r"^\s*[\w./-]+:\s\S"),
    re.compile(r"^\s*[\w-]+:\s*$"),
    re.compile(
        r"^\s*[\w.]+\s*-\s*(integer|string|timestamp|bigInteger|boolean"
        r"|text|date|float|increments|json|uuid|id|datetime|char|decimal|enum|binary)\b"
    ),
    re.compile(r"^\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"),
    re.compile(r"^\s*[a-z_][\w]*\s*$"),
    re.compile(r"^\s*[\w-]+\.\w{1,6}\s*$"),
    re.compile(
        r"^\s*</?(?!(?:div|span|img|p|a|br|hr|i|b|em|strong|small|sup|sub"
        r"|ul|ol|li|h[1-6]|blockquote|figure|figcaption)\b)[a-zA-Z][\w-]*[\s/>]"
    ),
    re.compile(r"^\s*/[\w][\w./-]*\s*$"),
    re.compile(r"^\s*(alias\s|php\d|ssh\s|cd\s|ls\s|git\s|vendor/bin)"),
    re.compile(r"^\s*\[[\w:.-]+\]\s*$"),
    re.compile(r"^\s*[a-zA-Z_]\w*(\.\w+)*\("),
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
    """코드 줄의 선행 tab 또는 네 칸 들여쓰기 제거."""

    if line.startswith("\t"):
        return line[1:]
    return line[4:] if line.startswith("    ") else line


def _strip_style_blocks(text: str) -> str:
    """한 줄 inline code 밖의 닫힌 page style block 제거."""

    out: list[str] = []
    lower = text.lower()
    index = 0

    def inside_inline_code(position: int) -> bool:
        """대상 위치가 한 줄 inline code 내부인지 판별."""

        line_start = text.rfind("\n", 0, position) + 1
        prefix = text[line_start:position]
        return prefix.count("`") % 2 == 1

    while index < len(text):
        start = lower.find(_STYLE_OPEN, index)
        if start < 0:
            out.append(text[index:])
            break
        if inside_inline_code(start):
            out.append(text[index : start + len(_STYLE_OPEN)])
            index = start + len(_STYLE_OPEN)
            continue
        tag_end = text.find(">", start + len(_STYLE_OPEN))
        if tag_end < 0:
            out.append(text[index:])
            break

        remove_start = start
        while remove_start > index and text[remove_start - 1] in " \t":
            remove_start -= 1

        close_start = lower.find(_STYLE_CLOSE, tag_end + 1)
        if close_start < 0:
            out.append(text[index:remove_start])
            break

        remove_end = close_start + len(_STYLE_CLOSE)
        while remove_end < len(text) and text[remove_end] in " \t\r\n":
            remove_end += 1

        out.append(text[index:remove_start])
        index = remove_end
    return "".join(out)


def _is_ordered_item_opener(stripped: str) -> bool:
    """줄이 하위 구조를 여는 순서 목록 항목인지 판별."""

    marker_end = 0
    while marker_end < len(stripped) and stripped[marker_end].isdigit():
        marker_end += 1
    if marker_end == 0 or marker_end >= len(stripped) or stripped[marker_end] != ".":
        return False
    remainder = stripped[marker_end + 1 :]
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
    """대상 줄이 기존 하위 구조에 포함되는지 판별."""

    cursor = index - 1
    while cursor >= 0:
        line = lines[cursor]
        if line == "":
            return False
        if _INDENTED_CODE_RE.match(line):
            cursor -= 1
            continue
        return _opens_indented_children(line)
    return False


def _convert_indented_code_blocks(text: str) -> str:
    """확실한 들여쓰기 코드 블록을 fenced code block으로 변환."""

    rebuilt_segments: list[str] = []
    for segment, is_code in _split_code_segments(text):
        if is_code:
            rebuilt_segments.append(segment)
            continue

        lines = segment.split("\n")
        out: list[str] = []
        index = 0
        while index < len(lines):
            line = lines[index]
            match = _INDENTED_CODE_RE.match(line)
            if not match or _LIST_MARKER_RE.match(match.group(1)):
                out.append(line)
                index += 1
                continue
            if _has_indented_parent(lines, index):
                out.append(line)
                index += 1
                continue

            block: list[str] = []
            while index < len(lines):
                current = lines[index]
                current_match = _INDENTED_CODE_RE.match(current)
                if current == "":
                    next_nonblank = next(
                        (
                            lines[position]
                            for position in range(index + 1, len(lines))
                            if lines[position] != ""
                        ),
                        "",
                    )
                    next_match = _INDENTED_CODE_RE.match(next_nonblank)
                    if next_match and (
                        not _LIST_MARKER_RE.match(next_match.group(1))
                        or _looks_like_code(block)
                    ):
                        block.append("")
                        index += 1
                        continue
                    break
                if not current_match:
                    break
                stripped = current_match.group(1)
                if _LIST_MARKER_RE.match(stripped) and not _looks_like_code(block):
                    break
                block.append(_strip_code_indent(current))
                index += 1

            if _looks_like_code(block):
                out.append("```")
                out.extend(block)
                out.append("```")
            else:
                out.extend(("    " + item) if item else "" for item in block)

        rebuilt_segments.append("\n".join(out))
    return "".join(rebuilt_segments)


def _outside_inline_code(text: str) -> list[tuple[str, bool]]:
    """inline code span 여부에 따라 텍스트 분할."""

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
    """보호 영역 밖의 고유 Base64 image data URI 수집."""

    values: set[str] = set()
    for fenced_segment, is_fenced in _split_code_segments(content):
        if is_fenced:
            continue
        for inline_segment, is_inline in _outside_inline_code(fenced_segment):
            if not is_inline:
                values.update(
                    match.group(0) for match in _BASE64_RE.finditer(inline_segment)
                )
    return values


def _allocate_base64_placeholders(previous: str, current: str) -> dict[str, str]:
    """두 원문의 data URI에 결정적 placeholder 할당.

    Args:
        previous: 이전 영어 원문.
        current: 현재 영어 원문.

    Returns:
        data URI를 key로 사용하는 placeholder 할당표.

    Raises:
        ValueError: 서로 다른 data URI의 SHA-256 digest가 충돌한 경우.
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
    """보호 영역 밖의 Base64 data URI를 할당된 token으로 치환."""

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
                """일치한 data URI를 token으로 치환하고 복원표에 기록."""

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

    rebuilt: list[str] = []
    for segment, is_code in _split_code_segments(text):
        if is_code:
            rebuilt.append(segment)
            continue
        segment = _strip_style_blocks(segment)
        segment = strip_title_attrs(segment)
        rebuilt.append(segment)
    text = "".join(rebuilt)

    text = _convert_indented_code_blocks(text)

    result.text = text
    return result


def preprocess(content: str) -> Preprocessed:
    """단일 원문을 결정적 placeholder 할당으로 정규화.

    Args:
        content: 정규화할 영어 원문.

    Returns:
        정규화된 작업 사본과 복원용 placeholder 매핑.
    """

    return preprocess_pair("", content).current
