"""Markdown parsing helpers shared by translation sync steps."""
from __future__ import annotations


def _split_line_ending(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    if line.endswith("\r"):
        return line[:-1], "\r"
    return line, ""


def fence_token(line: str) -> str | None:
    """Return the full opening/closing fence token for a Markdown fence line."""
    stripped = line.lstrip()
    if not stripped or stripped[0] not in "`~":
        return None

    char = stripped[0]
    count = 0
    while count < len(stripped) and stripped[count] == char:
        count += 1

    if count < 3:
        return None
    return char * count


def closes_fence(line: str, opening: str) -> bool:
    token = fence_token(line)
    return bool(token and opening and token[0] == opening[0] and len(token) >= len(opening))


def is_heading_line(line: str) -> bool:
    stripped = line.lstrip()
    level = len(stripped) - len(stripped.lstrip("#"))
    return 1 <= level <= 6 and len(stripped) > level and stripped[level].isspace()


def is_ordered_list_marker(line: str) -> bool:
    index = 0
    while index < len(line) and line[index].isdigit():
        index += 1
    return index > 0 and index + 1 < len(line) and line[index] == "." and line[index + 1].isspace()


def strip_title_attr_line(line: str) -> str:
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

    return stripped[:start].rstrip(" \t") + ending


def strip_title_attrs(text: str) -> str:
    return "".join(strip_title_attr_line(line) for line in text.splitlines(keepends=True))


def has_title_attr_line(text: str) -> bool:
    return any(strip_title_attr_line(line) != line for line in text.splitlines())


def html_comment_spans(text: str) -> list[tuple[int, int, str]]:
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
    out: list[str] = []
    index = 0
    for start, end, _body in html_comment_spans(text):
        out.append(text[index:start])
        index = end
    out.append(text[index:])
    return "".join(out)


def html_comment_bodies(text: str) -> list[str]:
    return [body for _start, _end, body in html_comment_spans(text)]


def is_named_anchor_line(line: str) -> bool:
    stripped = line.strip()
    lower = stripped.lower()
    if not lower.startswith("<a") or "name=" not in lower:
        return False
    if len(stripped) > 2 and not (stripped[2].isspace() or stripped[2] == ">"):
        return False
    if not (stripped.endswith(">") or lower.endswith("</a>")):
        return False
    return True
