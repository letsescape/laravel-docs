"""번역 동기화 단계에서 공유하는 Markdown 파싱 도구."""

from __future__ import annotations

import re

_PARAGRAPH_BREAK_RE = re.compile(r"\r?\n[ \t]*\r?\n")


def _is_escaped(text: str, index: int) -> bool:
    """지정한 위치의 문자가 역슬래시로 escape되었는지 판별."""

    backslashes = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return backslashes % 2 == 1


def _inline_code_spans(text: str) -> list[tuple[int, int, str]]:
    """Markdown inline code span의 원문 범위와 내용 반환."""

    spans: list[tuple[int, int, str]] = []
    index = 0
    while index < len(text):
        start = text.find("`", index)
        if start < 0:
            break
        if _is_escaped(text, start):
            index = start + 1
            continue
        opener_end = start + 1
        while opener_end < len(text) and text[opener_end] == "`":
            opener_end += 1
        width = opener_end - start
        paragraph_break = _PARAGRAPH_BREAK_RE.search(text, opener_end)
        search_end = paragraph_break.start() if paragraph_break else len(text)
        cursor = opener_end
        matched = False
        while cursor < search_end:
            close = text.find("`", cursor, search_end)
            if close < 0:
                break
            close_end = close + 1
            while close_end < len(text) and text[close_end] == "`":
                close_end += 1
            if close_end - close == width:
                spans.append((start, close_end, text[opener_end:close]))
                index = close_end
                matched = True
                break
            cursor = close_end
        if not matched:
            index = opener_end
    return spans


def _split_line_ending(line: str) -> tuple[str, str]:
    """줄 본문과 개행 문자 분리."""

    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    if line.endswith("\r"):
        return line[:-1], "\r"
    return line, ""


def fence_token(line: str) -> str | None:
    """Markdown blockquote 깊이가 포함된 fenced code 구분자 반환."""

    stripped = line.lstrip(" ")
    if len(line) - len(stripped) > 3 or stripped.startswith("\t"):
        return None
    quote_depth = 0
    while stripped.startswith(">"):
        quote_depth += 1
        stripped = stripped[1:]
        if stripped.startswith((" ", "\t")):
            stripped = stripped[1:]
        indented = stripped.lstrip(" ")
        if len(stripped) - len(indented) > 3 or indented.startswith("\t"):
            return None
        stripped = indented
    if not stripped or stripped[0] not in "`~":
        return None

    char = stripped[0]
    count = 0
    while count < len(stripped) and stripped[count] == char:
        count += 1

    if count < 3:
        return None
    return ">" * quote_depth + char * count


def closes_fence(line: str, opening: str) -> bool:
    """줄이 지정한 fenced code block을 닫는지 판별."""

    token = fence_token(line)
    if not token or not opening:
        return False
    token_depth = len(token) - len(token.lstrip(">"))
    opening_depth = len(opening) - len(opening.lstrip(">"))
    token_fence = token[token_depth:]
    opening_fence = opening[opening_depth:]
    stripped, _ending = _split_line_ending(line)
    stripped = stripped.lstrip()
    while stripped.startswith(">"):
        stripped = stripped[1:].lstrip()
    remainder = stripped[len(token_fence) :]
    return bool(
        token_depth == opening_depth
        and token_fence
        and opening_fence
        and token_fence[0] == opening_fence[0]
        and len(token_fence) >= len(opening_fence)
        and not remainder.strip(" \t")
    )


def is_heading_line(line: str) -> bool:
    """줄이 CommonMark ATX heading인지 판별."""

    stripped = line.lstrip(" ")
    if len(line) - len(stripped) > 3 or stripped.startswith("\t"):
        return False
    level = len(stripped) - len(stripped.lstrip("#"))
    return 1 <= level <= 6 and len(stripped) > level and stripped[level].isspace()


def is_ordered_list_marker(line: str) -> bool:
    """줄이 점 또는 괄호형 순서 목록 marker인지 판별."""

    index = 0
    while index < len(line) and line[index].isdigit():
        index += 1
    return (
        index > 0
        and index + 1 < len(line)
        and line[index] in ".)"
        and line[index + 1].isspace()
    )


def strip_title_attr_line(line: str) -> str:
    """Heading attribute에서 class만 제거하고 ID 보존."""

    body, ending = _split_line_ending(line)
    if not is_heading_line(body):
        return line

    stripped = body.rstrip(" \t")
    if not stripped.endswith("}"):
        return line

    start = stripped.rfind("{")
    if start <= 0 or stripped[start + 1 : start + 2] not in (".", "#"):
        return line
    if not stripped[start - 1].isspace():
        return line

    attrs = stripped[start + 1 : -1].split()
    if not attrs or not all(
        len(attr) > 1 and attr[0] in (".", "#") for attr in attrs
    ):
        return line

    classes = [attr for attr in attrs if attr.startswith(".")]
    if not classes:
        return line

    ids = [attr for attr in attrs if attr.startswith("#")]
    prefix = stripped[:start].rstrip(" \t")
    if ids:
        return f"{prefix} {{{' '.join(ids)}}}{ending}"
    return prefix + ending


def strip_title_attrs(text: str) -> str:
    """문서의 heading class 제거."""

    return "".join(
        strip_title_attr_line(line) for line in text.splitlines(keepends=True)
    )


def has_title_attr_line(text: str) -> bool:
    """문서에 제거 대상 heading class가 있는지 판별."""

    return any(strip_title_attr_line(line) != line for line in text.splitlines())


def html_comment_spans(text: str) -> list[tuple[int, int, str]]:
    """닫힌 HTML 주석의 원문 범위와 본문 반환."""

    spans: list[tuple[int, int, str]] = []
    index = 0
    while index < len(text):
        start = text.find("<!--", index)
        if start < 0:
            break
        end = text.find("-->", start + 4)
        if end < 0:
            break
        spans.append((start, end + 3, text[start + 4 : end]))
        index = end + 3
    return spans


def strip_html_comments(text: str) -> str:
    """문서에서 닫힌 HTML 주석 제거."""

    out: list[str] = []
    index = 0
    for start, end, _body in html_comment_spans(text):
        out.append(text[index:start])
        index = end
    out.append(text[index:])
    return "".join(out)


def html_comment_bodies(text: str) -> list[str]:
    """문서 순서가 유지된 HTML 주석 본문 반환."""

    return [body for _start, _end, body in html_comment_spans(text)]


def is_named_anchor_line(line: str) -> bool:
    """줄이 name 속성을 가진 HTML anchor인지 판별."""

    stripped = line.strip()
    lower = stripped.lower()
    if not lower.startswith("<a") or "name=" not in lower:
        return False
    if len(stripped) > 2 and not (stripped[2].isspace() or stripped[2] == ">"):
        return False
    if not (stripped.endswith(">") or lower.endswith("</a>")):
        return False
    return True
