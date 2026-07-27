"""Markdown parsing helpers shared by translation sync steps."""
from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache

_HTML_TAG_RE = re.compile(
    r'''</?[A-Za-z][\w:.-]*(?:\s+(?:[^<>"']|"[^"]*"|'[^']*')*)?\s*/?>'''
)
_HTML_CODE_ELEMENT_RE = re.compile(
    r"<code\b[^>]*>(.*?)</code\s*>", re.IGNORECASE | re.DOTALL
)
_PARAGRAPH_BREAK_RE = re.compile(r"\r?\n[ \t]*\r?\n")


@dataclass(frozen=True)
class MarkdownLink:
    """One inline Markdown link or image and its source span."""

    start: int
    end: int
    image: bool
    label: str
    target: str
    title: str


@dataclass(frozen=True)
class MarkdownReferenceDefinition:
    """One reference-style link definition."""

    label: str
    target: str
    title: str
    start: int
    end: int
    start_line: int
    end_line: int


@dataclass(frozen=True)
class FrontMatterDescription:
    """A top-level YAML ``description`` scalar and its validation state."""

    value: str
    style: str
    comment: str
    valid: bool


def _inline_code_spans(text: str) -> list[tuple[int, int, str]]:
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


def inline_code_contents(text: str) -> list[str]:
    """Return contents of Markdown code spans for any backtick delimiter width."""

    return [content for _start, _end, content in _inline_code_spans(text)]


def strip_inline_code(text: str) -> str:
    """Remove Markdown code spans using the same delimiter parser."""

    out: list[str] = []
    index = 0
    for start, end, _content in _inline_code_spans(text):
        out.append(text[index:start])
        index = end
    out.append(text[index:])
    return "".join(out)


_YAML_BLOCK_SCALAR_RE = re.compile(
    r"(?P<marker>(?P<kind>[|>])(?:[1-9][+-]?|[+-][1-9]?)?)"
    r"(?P<comment>[ \t]+#.*)?"
)
_YAML_FLOAT_RE = re.compile(
    r"(?:[-+]?(?:0|[1-9][0-9_]*)(?:\.[0-9_]*)?"
    r"(?:[eE][-+]?[0-9]+)?|"
    r"\.[0-9_]+(?:[eE][-+]?[0-9]+)?|"
    r"[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\.[0-9_]*|"
    r"[-+]?\.(?:inf|Inf|INF)|\.(?:nan|NaN|NAN))"
)
_YAML_DATE_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
_YAML_TIMESTAMP_RE = re.compile(
    r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}"
    r"(?:[Tt]|[ \t]+)[0-9]{1,2}:[0-9]{2}:[0-9]{2}"
    r"(?:\.[0-9]*)?"
    r"(?:[ \t]*(?:Z|[-+][0-9]{1,2}(?::[0-9]{2})?))?"
)
_YAML_BOOLEAN_VALUES = frozenset(("true", "True", "TRUE", "false", "False", "FALSE"))
_YAML_NULL_VALUES = frozenset(("~", "null", "Null", "NULL"))


def _double_quoted_yaml_scalar(value: str) -> tuple[str, bool]:
    if len(value) < 2 or value[-1] != '"':
        return value[1:], False

    inner = value[1:-1]
    index = 0
    while index < len(inner):
        char = inner[index]
        if char == '"':
            return inner, False
        if char != "\\":
            index += 1
            continue
        index += 1
        if index >= len(inner):
            return inner, False
        escape = inner[index]
        if escape in '0abtnvfre"/\\N_LP ':
            index += 1
            continue
        widths = {"x": 2, "u": 4, "U": 8}
        width = widths.get(escape)
        if width is None:
            return inner, False
        digits = inner[index + 1 : index + 1 + width]
        if len(digits) != width or not all(
            digit in "0123456789abcdefABCDEF" for digit in digits
        ):
            return inner, False
        index += width + 1
    return inner, True


def _single_quoted_yaml_scalar(value: str) -> tuple[str, bool]:
    if len(value) < 2 or value[-1] != "'":
        return value[1:], False

    inner = value[1:-1]
    index = 0
    while index < len(inner):
        if inner[index] != "'":
            index += 1
            continue
        if index + 1 >= len(inner) or inner[index + 1] != "'":
            return inner, False
        index += 2
    return inner.replace("''", "'"), True


def _plain_yaml_string(value: str) -> bool:
    if not value or value[0] in "!&*#|>{[,@`\"'%]}":
        return False
    if value[0] in "-?:" and (len(value) == 1 or value[1].isspace()):
        return False
    if re.search(r":(?:[ \t]|$)", value):
        return False
    non_string = (
        value in _YAML_BOOLEAN_VALUES
        or value in _YAML_NULL_VALUES
        or _is_yaml_integer(value)
        or (
            bool(_YAML_FLOAT_RE.fullmatch(value))
            and not value.endswith("_")
        )
        or bool(_YAML_DATE_RE.fullmatch(value))
        or bool(_YAML_TIMESTAMP_RE.fullmatch(value))
    )
    return not non_string


def _is_yaml_integer(value: str) -> bool:
    """Match the integer resolver used by gray-matter's locked js-yaml 3."""

    if not value:
        return False
    index = 1 if value[0] in "+-" else 0
    if index == len(value):
        return False

    if value[index] == "0":
        if index + 1 == len(value):
            return True
        index += 1
        prefix = value[index]
        if prefix == "b":
            digits = value[index + 1 :]
            return bool(digits) and digits[-1] != "_" and all(
                char in "01_" for char in digits
            ) and any(char in "01" for char in digits)
        if prefix == "x":
            digits = value[index + 1 :]
            return bool(digits) and digits[-1] != "_" and all(
                char in "0123456789abcdefABCDEF_" for char in digits
            ) and any(char != "_" for char in digits)
        digits = value[index:]
        return digits[-1] != "_" and all(
            char in "01234567_" for char in digits
        ) and any(char in "01234567" for char in digits)

    if value[index] == "_":
        return False
    has_digits = False
    while index < len(value):
        char = value[index]
        if char == "_":
            index += 1
            continue
        if char == ":":
            break
        if not char.isascii() or not char.isdigit():
            return False
        has_digits = True
        index += 1
    if not has_digits:
        return False
    if index == len(value):
        return value[-1] != "_"
    return bool(re.fullmatch(r"(?::[0-5]?[0-9])+", value[index:]))


def _quoted_yaml_parts(raw: str, quote: str) -> tuple[str, str]:
    index = 1
    while index < len(raw):
        if raw[index] != quote:
            index += 1
            continue
        if quote == '"' and _is_escaped(raw, index):
            index += 1
            continue
        if quote == "'" and index + 1 < len(raw) and raw[index + 1] == "'":
            index += 2
            continue
        suffix = raw[index + 1 :]
        if not suffix or re.fullmatch(r"[ \t]+#.*", suffix):
            return raw[: index + 1], suffix
        index += 1
    return raw, ""


def _plain_yaml_parts(raw: str) -> tuple[str, str]:
    comment = re.search(r"[ \t]+#", raw)
    if comment is None:
        return raw, ""
    return raw[: comment.start()].rstrip(), raw[comment.start() :]


def front_matter_description(text: str) -> FrontMatterDescription | None:
    """Parse a top-level front matter description without accepting collections.

    The sync only needs the small YAML subset its prompt allows: a plain or
    quoted string on one line, or a literal/folded block scalar. Unsupported or
    malformed values are returned with ``valid=False`` so provider output fails
    closed instead of being interpreted as a mapping, sequence, or null value.
    """

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    closing = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        len(lines),
    )
    found: FrontMatterDescription | None = None
    index = 1
    while index < closing:
        match = re.match(r"^description\s*:\s*(.*)$", lines[index])
        if not match:
            index += 1
            continue
        if found is not None:
            return FrontMatterDescription(
                found.value, found.style, found.comment, False
            )

        raw = match.group(1).strip()
        block = _YAML_BLOCK_SCALAR_RE.fullmatch(raw)
        if block:
            content: list[str] = []
            index += 1
            valid = True
            indentation = next(
                (int(char) for char in block.group("marker") if char.isdigit()),
                None,
            )
            detected_indentation: int | None = indentation
            leading_blank_indents: list[int] = []
            while index < closing and (
                not lines[index].strip() or lines[index][:1].isspace()
            ):
                prefix = lines[index][
                    : len(lines[index]) - len(lines[index].lstrip(" \t"))
                ]
                if "\t" in prefix:
                    valid = False
                if not lines[index].strip():
                    leading_blank_indents.append(len(prefix))
                elif detected_indentation is None:
                    detected_indentation = len(prefix)
                    if any(
                        blank_indent > detected_indentation
                        for blank_indent in leading_blank_indents
                    ):
                        valid = False
                if (
                    detected_indentation is not None
                    and lines[index].strip()
                    and len(prefix) < detected_indentation
                ):
                    valid = False
                if lines[index].strip():
                    content.append(lines[index].strip())
                index += 1
            found = FrontMatterDescription(
                " ".join(content),
                f"block:{block.group('marker')}",
                block.group("comment") or "",
                valid,
            )
            continue

        if raw.startswith('"'):
            scalar, comment = _quoted_yaml_parts(raw, '"')
            value, valid = _double_quoted_yaml_scalar(scalar)
            style = "double-quoted"
        elif raw.startswith("'"):
            scalar, comment = _quoted_yaml_parts(raw, "'")
            value, valid = _single_quoted_yaml_scalar(scalar)
            style = "single-quoted"
        else:
            value, comment = _plain_yaml_parts(raw)
            valid = _plain_yaml_string(value)
            style = "plain"

        if index + 1 < closing and lines[index + 1][:1].isspace():
            valid = False
        found = FrontMatterDescription(value, style, comment, valid)
        index += 1

    return found


def _is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return backslashes % 2 == 1


def _closing_label_bracket(text: str, start: int) -> int | None:
    depth = 1
    index = start
    while index < len(text):
        char = text[index]
        if char in "\r\n":
            return None
        if char == "\\" and index + 1 < len(text):
            index += 2
            continue
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return None


def _link_destination(
    text: str, start: int
) -> tuple[int, int, str] | None:
    if start >= len(text) or text[start].isspace() or text[start] == ")":
        return None

    depth = 1
    index = start
    while index < len(text):
        char = text[index]
        if char in "\r\n":
            return None
        if char == "\\" and index + 1 < len(text):
            index += 2
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index, index + 1, ""
        elif char.isspace():
            if depth != 1:
                return None
            break
        index += 1
    else:
        return None

    target_end = index
    while index < len(text) and text[index] in " \t":
        index += 1
    if index >= len(text) or text[index] not in ('"', "'", "("):
        return None

    title_opener = text[index]
    title_closer = ")" if title_opener == "(" else title_opener
    index += 1
    while index < len(text):
        if text[index] in "\r\n":
            return None
        if text[index] == title_closer and not _is_escaped(text, index):
            index += 1
            break
        index += 1
    else:
        return None

    while index < len(text) and text[index] in " \t":
        index += 1
    if index >= len(text) or text[index] != ")":
        return None
    return target_end, index + 1, text[target_end:index]


def markdown_links(text: str) -> tuple[MarkdownLink, ...]:
    """Return inline Markdown links, balancing parentheses in destinations."""

    links: list[MarkdownLink] = []
    index = 0
    while index < len(text):
        label_start = text.find("[", index)
        if label_start < 0:
            break
        if _is_escaped(text, label_start):
            index = label_start + 1
            continue
        label_end = _closing_label_bracket(text, label_start + 1)
        if (
            label_end is None
            or label_end + 1 >= len(text)
            or text[label_end + 1] != "("
        ):
            index = label_start + 1
            continue

        destination = _link_destination(text, label_end + 2)
        if destination is None:
            index = label_start + 1
            continue
        target_end, link_end, title = destination
        image = (
            label_start > 0
            and text[label_start - 1] == "!"
            and not _is_escaped(text, label_start - 1)
        )
        link_start = label_start - 1 if image else label_start
        links.append(
            MarkdownLink(
                start=link_start,
                end=link_end,
                image=image,
                label=text[label_start + 1 : label_end],
                target=text[label_end + 2 : target_end],
                title=title,
            )
        )
        index = link_end
    return tuple(links)


def _normalize_reference_label(label: str) -> str:
    return re.sub(
        r"[ \t\r\n]+",
        " ",
        label.strip(" \t\r\n"),
    ).casefold()


def _reference_label_state(
    value: str,
    start: int,
) -> tuple[str, int | None]:
    if start >= len(value) or value[start] != "[":
        return "invalid", None
    index = start + 1
    length = 0
    meaningful = False
    while index < len(value):
        char = value[index]
        if char == "\\" and index + 1 < len(value):
            meaningful = meaningful or value[index + 1] not in " \t\r\n"
            index += 2
            length += 2
            if length > 999:
                return "invalid", None
            continue
        if char == "[":
            return "invalid", None
        if char == "]":
            if meaningful and length <= 999:
                return "complete", index
            return "invalid", None
        meaningful = meaningful or char not in " \t\r\n"
        index += 1
        length += 1
        if length > 999:
            return "invalid", None
    return "incomplete", None


def _reference_label_end(value: str, start: int) -> int | None:
    state, end = _reference_label_state(value, start)
    return end if state == "complete" else None


def _consume_reference_whitespace(
    value: str, index: int
) -> tuple[int, bool]:
    start = index
    while index < len(value) and value[index] in " \t":
        index += 1
    if index < len(value) and value[index] in "\r\n":
        if value.startswith("\r\n", index):
            index += 2
        else:
            index += 1
        while index < len(value) and value[index] in " \t":
            index += 1
    return index, index > start


def _reference_destination_at(
    value: str, index: int
) -> tuple[str, int] | None:
    if index >= len(value):
        return None
    if value[index] == "<":
        start = index + 1
        index = start
        while index < len(value):
            if value[index] == "\\" and index + 1 < len(value):
                index += 2
                continue
            if value[index] in "\r\n" or value[index] == "<":
                return None
            if value[index] == ">":
                return value[start:index], index + 1
            index += 1
        return None

    start = index
    depth = 0
    while index < len(value) and value[index] not in " \t\r\n":
        if value[index] == "\\" and index + 1 < len(value):
            index += 2
            continue
        if value[index] == "<":
            return None
        if value[index] == "(":
            depth += 1
        elif value[index] == ")":
            if depth == 0:
                return None
            depth -= 1
        index += 1
    if index == start or depth:
        return None
    return value[start:index], index


def _parse_reference_definition_value(
    value: str,
) -> tuple[str, str, str, int] | None:
    indent = len(value) - len(value.lstrip(" "))
    if indent > 3 or value.startswith("\t"):
        return None
    index = indent
    label_end = _reference_label_end(value, index)
    if label_end is None or not value.startswith("]:", label_end):
        return None
    label = _normalize_reference_label(value[index + 1 : label_end])
    index = label_end + 2
    index, _separated = _consume_reference_whitespace(value, index)

    destination = _reference_destination_at(value, index)
    if destination is None:
        return None
    target, index = destination
    if index == len(value):
        return label, target, "", index

    destination_end = index
    while index < len(value) and value[index] in " \t":
        index += 1
    no_title_end = index
    if index == len(value):
        return label, target, "", no_title_end

    title_on_next_line = False
    if value[index] in "\r\n":
        if value.startswith("\r\n", index):
            index += 2
        else:
            index += 1
        while index < len(value) and value[index] in " \t":
            index += 1
        if index == len(value) or value[index] not in ('"', "'", "("):
            return label, target, "", no_title_end
        title_on_next_line = True
    elif (
        index == destination_end
        or value[index] not in ('"', "'", "(")
    ):
        return None

    title_start = index
    closer = ")" if value[index] == "(" else value[index]
    index += 1
    while index < len(value):
        if value[index] == "\\" and index + 1 < len(value):
            index += 2
            continue
        if value[index] in "\r\n":
            newline_end = index + 1
            if value.startswith("\r\n", index):
                newline_end += 1
            cursor = newline_end
            while cursor < len(value) and value[cursor] in " \t":
                cursor += 1
            if cursor < len(value) and value[cursor] in "\r\n":
                if title_on_next_line:
                    return label, target, "", no_title_end
                return None
        if value[index] == closer:
            index += 1
            break
        index += 1
    else:
        if title_on_next_line:
            return label, target, "", no_title_end
        return None

    title_end = index
    while index < len(value) and value[index] in " \t":
        index += 1
    if index < len(value) and value[index] not in "\r\n":
        if title_on_next_line:
            return label, target, "", no_title_end
        return None
    return label, target, value[title_start:title_end], index


def _strip_reference_container(line: str) -> tuple[str, tuple[str, ...]]:
    index = 0
    containers: list[str] = []
    while index < len(line):
        start = index
        spaces = 0
        while (
            index < len(line)
            and line[index] == " "
            and spaces < 3
        ):
            index += 1
            spaces += 1
        if index < len(line) and line[index] == ">":
            index += 1
            if index < len(line) and line[index] in " \t":
                index += 1
            containers.append("quote")
            continue
        marker = re.match(
            r"(?P<bullet>[-+*])|(?P<number>\d{1,9})[.)]",
            line[index:],
        )
        if marker and index + marker.end() < len(line):
            marker_end = index + marker.end()
            if line[marker_end] in " \t":
                padding_end = marker_end
                while (
                    padding_end < len(line)
                    and line[padding_end] in " \t"
                ):
                    padding_end += 1
                padding_width = len(
                    line[:padding_end].expandtabs(4)
                ) - len(line[:marker_end].expandtabs(4))
                index = (
                    padding_end
                    if padding_width <= 4
                    else marker_end + 1
                )
                containers.append(
                    "bullet"
                    if marker.group("bullet")
                    else f"ordered:{marker.group('number')}"
                )
                continue
        index = start
        break
    return line[index:], tuple(containers)


_RAW_HTML_BLOCK_RULES = (
    (
        re.compile(
            r" {0,3}<(?:pre|script|style|textarea)(?=[ \t>]|$)",
            re.IGNORECASE,
        ),
        re.compile(
            r"</(?:pre|script|style|textarea)>",
            re.IGNORECASE,
        ),
    ),
    (re.compile(r" {0,3}<!--"), re.compile(r"-->")),
    (re.compile(r" {0,3}<\?"), re.compile(r"\?>")),
    (re.compile(r" {0,3}<!\[CDATA\["), re.compile(r"\]\]>")),
    (re.compile(r" {0,3}<![A-Za-z]"), re.compile(r">")),
)
_RAW_HTML_BLOCK_TAGS = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|"
    "col|colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|"
    "figure|footer|form|frame|frameset|h1|h2|h3|h4|h5|h6|head|header|"
    "hr|html|iframe|legend|li|link|main|menu|menuitem|nav|noframes|ol|"
    "optgroup|option|p|param|search|section|summary|table|tbody|td|tfoot|"
    "th|thead|title|tr|track|ul"
)
_RAW_HTML_TYPE_6_START_RE = re.compile(
    rf" {{0,3}}</?(?:{_RAW_HTML_BLOCK_TAGS})(?=[ \t]|/?>|$)",
    re.IGNORECASE,
)
_HTML_ATTRIBUTE_NAME = r"[A-Za-z_:][A-Za-z0-9_.:-]*"
_HTML_ATTRIBUTE_VALUE = r"""(?:[^ \t\n"'=<>`]+|'[^']*'|"[^"]*")"""
_HTML_ATTRIBUTE = (
    rf"[ \t]+{_HTML_ATTRIBUTE_NAME}"
    rf"(?:[ \t]*=[ \t]*{_HTML_ATTRIBUTE_VALUE})?"
)
_RAW_HTML_TYPE_7_RE = re.compile(
    rf" {{0,3}}(?:"
    rf"<[A-Za-z][A-Za-z0-9-]*(?:{_HTML_ATTRIBUTE})*[ \t]*/?>"
    rf"|</[A-Za-z][A-Za-z0-9-]*[ \t]*>"
    rf")[ \t]*"
)


def _raw_html_container_exited(
    start_container: tuple[str, ...],
    start_prefix_width: int,
    line: str,
    current_container: tuple[str, ...],
) -> bool:
    if not start_container:
        return False
    if current_container[: len(start_container)] == start_container:
        return False
    if "quote" in start_container:
        return True
    leading_width = len(line) - len(line.lstrip(" \t"))
    return leading_width < start_prefix_width


def _raw_html_block_ranges(
    text: str,
    excluded: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    start_offset: int | None = None
    end_pattern: re.Pattern[str] | None = None
    start_container: tuple[str, ...] = ()
    start_prefix_width = 0
    offset = 0

    for raw_line in text.splitlines(keepends=True):
        line = raw_line.rstrip("\r\n")
        logical, container = _strip_reference_container(line)

        if (
            start_offset is not None
            and _raw_html_container_exited(
                start_container,
                start_prefix_width,
                line,
                container,
            )
        ):
            ranges.append((start_offset, offset))
            start_offset = None
            end_pattern = None
            start_container = ()
            start_prefix_width = 0

        if start_offset is None:
            for start_pattern, candidate_end_pattern in (
                _RAW_HTML_BLOCK_RULES
            ):
                match = start_pattern.match(logical)
                logical_offset = len(line) - len(logical)
                opening_offset = (
                    offset + logical_offset + match.start()
                    if match
                    else -1
                )
                if match and not any(
                    start <= opening_offset < end
                    for start, end in excluded
                ):
                    start_offset = offset
                    end_pattern = candidate_end_pattern
                    start_container = container
                    start_prefix_width = len(line) - len(logical)
                    break

        if (
            start_offset is not None
            and end_pattern is not None
            and end_pattern.search(logical)
        ):
            ranges.append((start_offset, offset + len(raw_line)))
            start_offset = None
            end_pattern = None
            start_container = ()
            start_prefix_width = 0
        offset += len(raw_line)

    if start_offset is not None:
        ranges.append((start_offset, len(text)))
    return ranges


def _blank_terminated_raw_html_ranges(
    text: str,
    excluded: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    start_offset: int | None = None
    start_container: tuple[str, ...] = ()
    start_prefix_width = 0
    offset = 0

    for raw_line in text.splitlines(keepends=True):
        line = raw_line.rstrip("\r\n")
        logical, container = _strip_reference_container(line)
        if start_offset is not None:
            if not line.strip():
                ranges.append((start_offset, offset))
                start_offset = None
                start_container = ()
                start_prefix_width = 0
            elif _raw_html_container_exited(
                start_container,
                start_prefix_width,
                line,
                container,
            ):
                ranges.append((start_offset, offset))
                start_offset = None
                start_container = ()
                start_prefix_width = 0
            else:
                offset += len(raw_line)
                continue

        type_6 = _RAW_HTML_TYPE_6_START_RE.match(logical)
        type_7 = _RAW_HTML_TYPE_7_RE.fullmatch(logical)
        match = type_6 or type_7
        logical_offset = len(line) - len(logical)
        opening_offset = (
            offset + logical_offset + match.start()
            if match
            else -1
        )
        if match and not any(
            start <= opening_offset < end
            for start, end in excluded
        ):
            start_offset = offset
            start_container = container
            start_prefix_width = len(line) - len(logical)
        offset += len(raw_line)

    if start_offset is not None:
        ranges.append((start_offset, len(text)))
    return ranges


def _masked_reference_source(text: str) -> str:
    masked = list(text)
    excluded = _fenced_code_ranges(text)
    excluded.extend(
        (start, end) for start, end, _body in html_comment_spans(text)
    )
    excluded.extend(_raw_html_block_ranges(text, excluded))
    excluded.extend(_blank_terminated_raw_html_ranges(text, excluded))
    for start, end in excluded:
        for index in range(start, end):
            if masked[index] not in "\r\n":
                masked[index] = " "
    return "".join(masked)


def _reference_can_start(
    logical_lines: list[str],
    containers: list[tuple[str, ...]],
    line_index: int,
    definition_lines: set[int],
) -> bool:
    if line_index == 0 or not logical_lines[line_index - 1].strip():
        return True
    if line_index - 1 in definition_lines:
        return True
    if containers[line_index] != containers[line_index - 1]:
        previous = containers[line_index - 1]
        current = containers[line_index]
        if (
            len(current) <= len(previous)
            or current[: len(previous)] != previous
        ):
            return False
        interrupting = current[len(previous)]
        return interrupting in ("quote", "bullet", "ordered:1")
    previous = logical_lines[line_index - 1]
    return bool(
        re.match(r" {0,3}#{1,6}(?:[ \t]+|$)", previous)
        or re.fullmatch(
            r" {0,3}(?:(?:\*[ \t]*){3,}|"
            r"(?:-[ \t]*){3,}|(?:_[ \t]*){3,})",
            previous,
        )
    )


def _parse_reference_definitions(
    text: str,
) -> tuple[MarkdownReferenceDefinition, ...]:
    masked = _masked_reference_source(text)
    raw_lines = text.splitlines(keepends=True)
    masked_lines = masked.splitlines(keepends=True)
    if not raw_lines and text:
        raw_lines = [text]
        masked_lines = [masked]

    logical_lines: list[str] = []
    containers: list[tuple[str, ...]] = []
    offsets: list[int] = []
    offset = 0
    for raw_line, masked_line in zip(
        raw_lines, masked_lines, strict=True
    ):
        offsets.append(offset)
        offset += len(raw_line)
        line = masked_line.rstrip("\r\n")
        logical, container = _strip_reference_container(line)
        logical_lines.append(logical)
        containers.append(container)

    definitions: list[MarkdownReferenceDefinition] = []
    definition_lines: set[int] = set()
    line_index = 0
    while line_index < len(logical_lines):
        if (
            not _reference_can_start(
                logical_lines,
                containers,
                line_index,
                definition_lines,
            )
            or not logical_lines[line_index].lstrip(" ").startswith("[")
        ):
            line_index += 1
            continue

        start_container = containers[line_index]
        first_line = logical_lines[line_index]
        parsed_text = first_line
        parsed = _parse_reference_definition_value(parsed_text)
        next_line = line_index + 1
        if (
            parsed is None
            or (
                not parsed[2]
                and next_line < len(logical_lines)
                and logical_lines[next_line]
                .lstrip(" \t")
                .startswith(('"', "'", "("))
            )
        ):
            candidate_lines: list[str] = []
            label_complete = False
            candidate_invalid = False
            for end_line in range(line_index, len(logical_lines)):
                if (
                    end_line > line_index
                    and (
                        len(containers[end_line]) > len(start_container)
                        or start_container[
                            : len(containers[end_line])
                        ] != containers[end_line]
                    )
                ):
                    break
                logical = logical_lines[end_line]
                if end_line > line_index and not logical.strip():
                    break
                candidate_lines.append(logical)
                if not label_complete:
                    label_candidate = "\n".join(candidate_lines)
                    indent = len(label_candidate) - len(
                        label_candidate.lstrip(" ")
                    )
                    state, label_end = _reference_label_state(
                        label_candidate,
                        indent,
                    )
                    if state == "invalid":
                        candidate_invalid = True
                        break
                    if state == "complete":
                        if not label_candidate.startswith(
                            "]:",
                            label_end,
                        ):
                            candidate_invalid = True
                            break
                        label_complete = True
            parsed_text = "\n".join(candidate_lines)
            parsed = (
                None
                if candidate_invalid
                else _parse_reference_definition_value(parsed_text)
            )

        if parsed is None:
            line_index += 1
            continue

        label, target, title, parsed_end = parsed
        end_line = line_index + parsed_text[:parsed_end].count("\n")
        start = offsets[line_index]
        end = offsets[end_line] + len(raw_lines[end_line].rstrip("\r\n"))
        definitions.append(
            MarkdownReferenceDefinition(
                label,
                target,
                title,
                start,
                end,
                line_index,
                end_line,
            )
        )
        definition_lines.update(range(line_index, end_line + 1))
        line_index = end_line + 1
    return tuple(definitions)


@lru_cache(maxsize=16)
def _cached_reference_definitions(
    text: str,
) -> tuple[MarkdownReferenceDefinition, ...]:
    return _parse_reference_definitions(text)


def reference_definitions(
    text: str,
) -> tuple[MarkdownReferenceDefinition, ...]:
    """Return definitions outside comments, code fences, and raw HTML blocks."""

    if len(text) < 16_384:
        return _parse_reference_definitions(text)
    return _cached_reference_definitions(text)


def reference_definition_line_numbers(text: str) -> frozenset[int]:
    return frozenset(
        line
        for definition in reference_definitions(text)
        for line in range(definition.start_line, definition.end_line + 1)
    )


@lru_cache(maxsize=16)
def mask_reference_definitions(text: str) -> str:
    masked = list(text)
    for definition in reference_definitions(text):
        for index in range(definition.start, definition.end):
            if masked[index] not in "\r\n":
                masked[index] = " "
    return "".join(masked)


def is_reference_definition_block(text: str) -> bool:
    definitions = reference_definitions(text)
    return bool(definitions) and not mask_reference_definitions(text).strip()


def is_reference_definition_line(line: str) -> bool:
    """Return whether one physical line is a complete reference definition."""

    if "\n" in line or "\r" in line:
        return False
    logical, _containers = _strip_reference_container(line)
    parsed = _parse_reference_definition_value(logical)
    return parsed is not None and parsed[3] == len(logical)


def reference_link_signatures(
    text: str,
) -> tuple[tuple[bool, str, str], ...]:
    """Return resolved reference links using CommonMark first-definition wins."""

    effective: dict[str, tuple[str, str]] = {}
    for definition in reference_definitions(text):
        effective.setdefault(
            definition.label,
            (definition.target, definition.title),
        )
    if not effective:
        return ()

    body = mask_reference_definitions(_masked_reference_source(text))
    masked = list(body)
    for start, end, _content in _inline_code_spans(body):
        for index in range(start, end):
            if masked[index] not in "\r\n":
                masked[index] = " "
    body = "".join(masked)

    signatures: list[tuple[bool, str, str]] = []
    index = 0
    while index < len(body):
        start = body.find("[", index)
        if start < 0:
            break
        if _is_escaped(body, start):
            index = start + 1
            continue
        text_end = _closing_label_bracket(body, start + 1)
        if text_end is None:
            index = start + 1
            continue

        image = (
            start > 0
            and body[start - 1] == "!"
            and not _is_escaped(body, start - 1)
        )
        following = text_end + 1
        if following < len(body) and body[following] == "(":
            index = following + 1
            continue

        reference_end = text_end
        if following < len(body) and body[following] == "[":
            if following + 1 < len(body) and body[following + 1] == "]":
                raw_label = body[start + 1 : text_end]
                reference_end = following + 1
            else:
                label_end = _reference_label_end(body, following)
                if label_end is None:
                    index = text_end + 1
                    continue
                raw_label = body[following + 1 : label_end]
                reference_end = label_end
        else:
            strict_end = _reference_label_end(body, start)
            if strict_end != text_end:
                index = text_end + 1
                continue
            raw_label = body[start + 1 : text_end]

        resolved = effective.get(_normalize_reference_label(raw_label))
        if resolved is not None:
            target, title = resolved
            signatures.append((image, target, title))
        index = reference_end + 1
    return tuple(signatures)


def strip_markdown_links(text: str) -> str:
    """Remove complete inline Markdown links and images from text."""

    out: list[str] = []
    index = 0
    for link in markdown_links(text):
        out.append(text[index : link.start])
        index = link.end
    out.append(text[index:])
    return "".join(out)


def normalize_annotation_anchor(text: str) -> str:
    """Normalize source text and its escaped HTML-comment representation."""

    text = text.replace("*&#47;", "*/").replace("--&gt;", "-->")
    return " ".join(text.split())


def is_non_annotatable_line(line: str) -> bool:
    """Return whether a Markdown line is structural rather than translatable."""

    stripped = line.strip()
    if not stripped:
        return False
    if is_named_anchor_line(stripped):
        return True
    if is_reference_definition_line(line):
        return True
    if stripped.startswith(("<!--", ">", "|")):
        return True
    if stripped.startswith(("- [", "* [")) and "](#" in stripped:
        return True
    return is_structural_html_line(line)


def is_standalone_html_tag(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped and _HTML_TAG_RE.fullmatch(stripped))


def is_structural_html_fragment(text: str) -> bool:
    """Return whether text contains only HTML tags and whitespace."""

    return bool(structural_html_tags(text))


def is_structural_html_line(line: str) -> bool:
    """Return whether a top-level Markdown line contains only HTML tags."""

    return bool(line and not line[:1].isspace() and is_structural_html_fragment(line))


def structural_html_tags(text: str) -> tuple[str, ...]:
    """Return ordered tags when ``text`` is a tag-only HTML fragment."""

    position = 0
    tags: list[str] = []
    for match in _HTML_TAG_RE.finditer(text):
        if text[position : match.start()].strip():
            return ()
        tags.append(match.group(0))
        position = match.end()
    return tuple(tags) if tags and not text[position:].strip() else ()


def html_tags(text: str) -> tuple[str, ...]:
    """Return every HTML tag token in document order."""

    return tuple(match.group(0) for match in _HTML_TAG_RE.finditer(text))


def html_code_contents(text: str) -> tuple[str, ...]:
    """Return the contents of raw HTML ``code`` elements in document order."""

    return tuple(match.group(1) for match in _HTML_CODE_ELEMENT_RE.finditer(text))


def strip_html_code_elements(text: str) -> str:
    """Remove raw HTML ``code`` elements, including their protected contents."""

    return _HTML_CODE_ELEMENT_RE.sub("", text)


def _split_line_ending(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    if line.endswith("\r"):
        return line[:-1], "\r"
    return line, ""


def fence_token(line: str) -> str | None:
    """Return a fence token prefixed by its Markdown blockquote depth."""
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


def mask_fenced_code_contents(text: str) -> str:
    """Remove fenced code contents while retaining their boundary lines."""

    out: list[str] = []
    in_code = False
    fence = ""
    for line in text.splitlines(keepends=True):
        token = fence_token(line)
        if token:
            if not in_code:
                in_code = True
                fence = token
                out.append(line)
                continue
            if closes_fence(line, fence):
                in_code = False
                fence = ""
                out.append(line)
                continue
        if not in_code:
            out.append(line)
    return "".join(out)


def is_heading_line(line: str) -> bool:
    stripped = line.lstrip(" ")
    if len(line) - len(stripped) > 3 or stripped.startswith("\t"):
        return False
    level = len(stripped) - len(stripped.lstrip("#"))
    return 1 <= level <= 6 and len(stripped) > level and stripped[level].isspace()


def is_ordered_list_marker(line: str) -> bool:
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
    out: list[str] = []
    index = 0
    for start, end, _body in html_comment_spans(text):
        out.append(
            "".join(
                strip_title_attr_line(line)
                for line in text[index:start].splitlines(keepends=True)
            )
        )
        out.append(text[start:end])
        index = end
    out.append(
        "".join(
            strip_title_attr_line(line)
            for line in text[index:].splitlines(keepends=True)
        )
    )
    return "".join(out)


def has_title_attr_line(text: str) -> bool:
    return strip_title_attrs(text) != text


def _fenced_code_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    range_start = 0
    offset = 0
    in_code = False
    fence = ""
    for line in text.splitlines(keepends=True):
        token = fence_token(line)
        if token:
            if not in_code:
                in_code = True
                fence = token
                range_start = offset
            elif closes_fence(line, fence):
                ranges.append((range_start, offset + len(line)))
                in_code = False
                fence = ""
        offset += len(line)
    if in_code:
        ranges.append((range_start, len(text)))
    return ranges


def _parse_html_comment_spans(
    text: str,
) -> tuple[tuple[int, int, str], ...]:
    spans: list[tuple[int, int, str]] = []
    inline_spans = [
        (start, end) for start, end, _content in _inline_code_spans(text)
    ]
    fenced_ranges = _fenced_code_ranges(text)
    inline_index = 0
    fence_index = 0
    index = 0
    while index < len(text):
        while (
            inline_index < len(inline_spans)
            and inline_spans[inline_index][0] < index
        ):
            inline_index += 1
        while (
            fence_index < len(fenced_ranges)
            and fenced_ranges[fence_index][0] < index
        ):
            fence_index += 1

        comment_start = text.find("<!--", index)
        inline_start = (
            inline_spans[inline_index][0]
            if inline_index < len(inline_spans)
            else len(text)
        )
        fence_start = (
            fenced_ranges[fence_index][0]
            if fence_index < len(fenced_ranges)
            else len(text)
        )
        next_start = min(
            comment_start if comment_start >= 0 else len(text),
            inline_start,
            fence_start,
        )
        if next_start == len(text):
            break
        if next_start == inline_start:
            index = inline_spans[inline_index][1]
            inline_index += 1
            continue
        if next_start == fence_start:
            index = fenced_ranges[fence_index][1]
            fence_index += 1
            continue

        end = text.find("-->", comment_start + 4)
        if end < 0:
            break
        spans.append(
            (comment_start, end + 3, text[comment_start + 4 : end])
        )
        index = end + 3
    return tuple(spans)


@lru_cache(maxsize=16)
def _cached_html_comment_spans(
    text: str,
) -> tuple[tuple[int, int, str], ...]:
    return _parse_html_comment_spans(text)


def html_comment_spans(text: str) -> list[tuple[int, int, str]]:
    """Return HTML comments outside Markdown code spans and fenced code."""

    spans = (
        _parse_html_comment_spans(text)
        if len(text) < 16_384
        else _cached_html_comment_spans(text)
    )
    return list(spans)


def has_malformed_html_comment_delimiters(text: str) -> bool:
    """Return whether comment delimiters are unbalanced outside fenced code."""

    masked = list(text)

    def mask_range(start: int, end: int) -> None:
        for position in range(start, end):
            if masked[position] not in "\r\n":
                masked[position] = " "

    for start, end in _fenced_code_ranges(text):
        mask_range(start, end)

    offset = 0
    in_front_matter = False
    for lineno, line in enumerate(text.splitlines(keepends=True)):
        stripped = line.strip()
        if lineno == 0 and stripped == "---":
            in_front_matter = True
        if in_front_matter:
            mask_range(offset, offset + len(line))
            if lineno > 0 and stripped == "---":
                in_front_matter = False
        elif line.startswith("\t") or len(line) - len(line.lstrip(" ")) >= 4:
            mask_range(offset, offset + len(line))
        offset += len(line)

    body = "".join(masked)
    comment_spans = [
        (start, end) for start, end, _body in html_comment_spans(body)
    ]
    inline_spans = [
        (start, end)
        for start, end, _content in _inline_code_spans(body)
    ]
    if inline_spans:
        masked = list(body)
        for start, end in inline_spans:
            inside_comment = any(
                comment_start <= start and end <= comment_end
                for comment_start, comment_end in comment_spans
            )
            overlaps_comment = any(
                start < comment_end and end > comment_start
                for comment_start, comment_end in comment_spans
            )
            if inside_comment:
                opener = body.find("<!--", start, end)
                while opener >= 0:
                    masked[opener : opener + 4] = " " * 4
                    opener = body.find("<!--", opener + 4, end)
                continue
            if overlaps_comment:
                continue
            for index in range(start, end):
                if masked[index] not in "\r\n":
                    masked[index] = " "
        body = "".join(masked)

    index = 0
    while index < len(body):
        opener = body.find("<!--", index)
        closer = body.find("-->", index)
        if closer >= 0 and (opener < 0 or closer < opener):
            return True
        if opener < 0:
            return False

        closer = body.find("-->", opener + 4)
        if closer < 0:
            return True
        nested = body.find("<!--", opener + 4)
        while 0 <= nested < closer:
            escaped_closer = body.find("--&gt;", nested + 4, closer)
            if escaped_closer < 0:
                return True
            nested = body.find("<!--", escaped_closer + 7, closer)
        index = closer + 3
    return False


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


def standalone_html_comment_line_numbers(text: str) -> frozenset[int]:
    """Return one-based line numbers occupied by standalone comments outside code."""

    lines = text.splitlines()
    numbers: set[int] = set()
    in_code = False
    fence = ""
    in_comment = False
    for lineno, line in enumerate(lines, start=1):
        if in_comment:
            numbers.add(lineno)
            if "-->" in line:
                in_comment = False
            continue

        token = fence_token(line)
        if token:
            if not in_code:
                in_code = True
                fence = token
            elif closes_fence(line, fence):
                in_code = False
            continue
        if in_code:
            continue

        stripped = line.lstrip()
        if not stripped.startswith("<!--"):
            continue
        numbers.add(lineno)
        if "-->" not in stripped[4:]:
            in_comment = True
    return frozenset(numbers)


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
