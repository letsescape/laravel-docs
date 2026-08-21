"""번역 동기화 단계에서 공유하는 Markdown 파싱 도구."""
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
    """인라인 Markdown 링크 또는 이미지와 원문 범위."""

    start: int
    end: int
    image: bool
    label: str
    target: str
    title: str


@dataclass(frozen=True)
class MarkdownReferenceDefinition:
    """단일 참조형 링크 정의."""

    label: str
    target: str
    title: str
    start: int
    end: int
    start_line: int
    end_line: int


@dataclass(frozen=True)
class MarkdownAutolink:
    """단일 CommonMark URI 또는 이메일 자동 링크와 원문 범위."""

    start: int
    end: int
    label: str
    target: str


@dataclass(frozen=True)
class FrontMatterDescription:
    """최상위 YAML ``description`` 스칼라와 검증 상태."""

    value: str
    style: str
    comment: str
    valid: bool


def _matching_code_span(
    text: str,
    *,
    opener_end: int,
    width: int,
) -> tuple[int, str] | None:
    """인라인 코드 opener와 같은 너비의 paragraph 내부 closer 탐색.

    Args:
        text: Markdown 원문.
        opener_end: opener 바로 다음 위치.
        width: 백틱 opener 너비.

    Returns:
        closer 다음 위치와 코드 본문. 없으면 ``None``.
    """

    paragraph_break = _PARAGRAPH_BREAK_RE.search(text, opener_end)
    search_end = paragraph_break.start() if paragraph_break else len(text)
    cursor = opener_end
    while cursor < search_end:
        close = text.find("`", cursor, search_end)
        if close < 0:
            return None
        close_end = close + 1
        while close_end < len(text) and text[close_end] == "`":
            close_end += 1
        if close_end - close == width:
            return close_end, text[opener_end:close]
        cursor = close_end
    return None


def _inline_code_spans(text: str) -> list[tuple[int, int, str]]:
    """Markdown 인라인 코드의 시작·종료 위치와 내용."""

    spans: list[tuple[int, int, str]] = []
    index = 0
    while index < len(text):
        start = text.find("`", index)
        if start < 0:
            break
        if is_escaped(text, start):
            index = start + 1
            continue
        opener_end = start + 1
        while opener_end < len(text) and text[opener_end] == "`":
            opener_end += 1
        width = opener_end - start
        matched = _matching_code_span(
            text,
            opener_end=opener_end,
            width=width,
        )
        if matched is None:
            index = opener_end
            continue
        close_end, content = matched
        spans.append((start, close_end, content))
        index = close_end
    return spans


def inline_code_contents(text: str) -> list[str]:
    """모든 백틱 구분자 길이를 지원하는 Markdown 인라인 코드 내용 목록."""

    return [content for _start, _end, content in _inline_code_spans(text)]


def strip_inline_code(text: str) -> str:
    """인라인 코드와 같은 구분자 파서로 Markdown 인라인 코드 제거."""

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


def _yaml_escape_end(inner: str, index: int) -> int | None:
    """큰따옴표 YAML escape를 검증하고 다음 위치 반환.

    Args:
        inner: 따옴표 내부 문자열.
        index: 역슬래시 다음 escape 문자 위치.

    Returns:
        유효한 escape 다음 위치. 잘못됐으면 ``None``.
    """

    if index >= len(inner):
        return None
    escape = inner[index]
    if escape in '0abtnvfre"/\\N_LP ':
        return index + 1
    width = {"x": 2, "u": 4, "U": 8}.get(escape)
    if width is None:
        return None
    digits = inner[index + 1 : index + 1 + width]
    if len(digits) != width or not all(
        digit in "0123456789abcdefABCDEF" for digit in digits
    ):
        return None
    return index + width + 1


def _double_quoted_yaml_scalar(value: str) -> tuple[str, bool]:
    """큰따옴표 YAML 스칼라의 값과 유효성."""

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
        next_index = _yaml_escape_end(inner, index + 1)
        if next_index is None:
            return inner, False
        index = next_index
    return inner, True


def _single_quoted_yaml_scalar(value: str) -> tuple[str, bool]:
    """작은따옴표 YAML 스칼라의 값과 유효성."""

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
    """따옴표 없는 YAML 값의 문자열 해석 가능 여부."""

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
    """gray-matter에 고정된 js-yaml 3 정수 해석기와의 일치 여부."""

    if not value:
        return False
    index = 1 if value[0] in "+-" else 0
    if index == len(value):
        return False

    if value[index] == "0":
        return _zero_prefixed_yaml_integer(value[index:])

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


def _zero_prefixed_yaml_integer(value: str) -> bool:
    """부호를 제외한 0 시작 YAML 정수 형식 판정.

    Args:
        value: 0으로 시작하는 부호 없는 정수 후보.

    Returns:
        이진수·16진수·8진수 또는 0 형식의 유효 여부.
    """

    if len(value) == 1:
        return True
    prefix = value[1]
    if prefix == "b":
        digits = value[2:]
        alphabet = "01_"
        meaningful = "01"
    elif prefix == "x":
        digits = value[2:]
        alphabet = "0123456789abcdefABCDEF_"
        meaningful = "0123456789abcdefABCDEF"
    else:
        digits = value[1:]
        alphabet = "01234567_"
        meaningful = "01234567"
    return bool(digits) and digits[-1] != "_" and all(
        char in alphabet for char in digits
    ) and any(char in meaningful for char in digits)


def _quoted_yaml_parts(raw: str, quote: str) -> tuple[str, str]:
    """따옴표 YAML 값과 뒤따르는 주석 분리."""

    index = 1
    while index < len(raw):
        if raw[index] != quote:
            index += 1
            continue
        if quote == '"' and is_escaped(raw, index):
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
    """따옴표 없는 YAML 값과 뒤따르는 주석 분리."""

    comment = re.search(r"[ \t]+#", raw)
    if comment is None:
        return raw, ""
    return raw[: comment.start()].rstrip(), raw[comment.start() :]


def _block_description(
    lines: list[str],
    index: int,
    closing: int,
    block: re.Match[str],
) -> tuple[FrontMatterDescription, int]:
    """YAML block scalar description과 다음 머리말 줄 위치 파싱.

    Args:
        lines: 전체 문서 줄.
        index: description 줄 위치.
        closing: 머리말 닫는 구분자 위치.
        block: block scalar marker 정규식 일치 결과.

    Returns:
        파싱한 description과 다음 줄 위치.
    """

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
        line = lines[index]
        line_valid, detected_indentation = _block_scalar_line(
            line,
            detected_indentation=detected_indentation,
            leading_blank_indents=leading_blank_indents,
        )
        valid = valid and line_valid
        if line.strip():
            content.append(line.strip())
        index += 1
    return (
        FrontMatterDescription(
            " ".join(content),
            f"block:{block.group('marker')}",
            block.group("comment") or "",
            valid,
        ),
        index,
    )


def _block_scalar_line(
    line: str,
    *,
    detected_indentation: int | None,
    leading_blank_indents: list[int],
) -> tuple[bool, int | None]:
    """YAML block scalar 단일 줄의 들여쓰기 유효성 검사.

    Args:
        line: block scalar 본문 줄.
        detected_indentation: 명시되거나 앞서 감지된 들여쓰기.
        leading_blank_indents: 앞선 빈 줄의 들여쓰기 목록.

    Returns:
        줄 유효 여부와 갱신된 들여쓰기.
    """

    prefix = line[: len(line) - len(line.lstrip(" \t"))]
    valid = "\t" not in prefix
    if not line.strip():
        leading_blank_indents.append(len(prefix))
        return valid, detected_indentation
    if detected_indentation is None:
        detected_indentation = len(prefix)
        valid = valid and not any(
            blank_indent > detected_indentation
            for blank_indent in leading_blank_indents
        )
    if len(prefix) < detected_indentation:
        valid = False
    return valid, detected_indentation


def _scalar_description(
    raw: str,
    *,
    has_continuation: bool,
) -> FrontMatterDescription:
    """단일 줄 description scalar의 값·style·주석 파싱.

    Args:
        raw: description 콜론 다음 문자열.
        has_continuation: 다음 줄이 들여쓰기된 여부.

    Returns:
        파싱한 description scalar.
    """

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
    return FrontMatterDescription(
        value,
        style,
        comment,
        valid and not has_continuation,
    )


def front_matter_description(text: str) -> FrontMatterDescription | None:
    """컬렉션을 허용하지 않는 최상위 front matter ``description`` 파싱.

    번역 프롬프트가 허용하는 제한된 YAML 부분집합만 지원.
    단일 줄 일반·따옴표 문자열과 리터럴·접힌 블록 스칼라 지원.
    지원하지 않거나 잘못된 값은 매핑, 시퀀스 또는 null로 해석하지 않고 ``valid=False``로 반환하는 실패 시 거부 계약.
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
            found, index = _block_description(lines, index, closing, block)
            continue
        has_continuation = (
            index + 1 < closing and lines[index + 1][:1].isspace()
        )
        found = _scalar_description(raw, has_continuation=has_continuation)
        index += 1

    return found


def is_escaped(text: str, index: int) -> bool:
    """지정한 문자가 역슬래시로 이스케이프됐는지 여부."""

    backslashes = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return backslashes % 2 == 1


def _closing_label_bracket(text: str, start: int) -> int | None:
    """중첩을 고려한 링크 레이블의 닫는 대괄호 위치."""

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


def _link_title_suffix(
    text: str,
    *,
    index: int,
    target_start: int,
    target_end: int,
    suffix_start: int,
) -> tuple[int, int, int, str] | None:
    """링크 대상 다음의 선택적 제목과 닫는 괄호 파싱.

    Args:
        text: Markdown 원문.
        index: 제목 opener 위치.
        target_start: 링크 대상 시작 위치.
        target_end: 링크 대상 끝 위치.
        suffix_start: 반환할 제목·공백 suffix 시작 위치.

    Returns:
        대상 범위, 링크 끝, 제목 suffix. 잘못됐으면 ``None``.
    """

    if index >= len(text) or text[index] not in ('"', "'", "("):
        return None
    title_opener = text[index]
    title_closer = ")" if title_opener == "(" else title_opener
    index += 1
    while index < len(text):
        if text[index] in "\r\n":
            return None
        if text[index] == title_closer and not is_escaped(text, index):
            index += 1
            break
        index += 1
    else:
        return None
    while index < len(text) and text[index] in " \t":
        index += 1
    if index >= len(text) or text[index] != ")":
        return None
    return target_start, target_end, index + 1, text[suffix_start:index]


def _angle_link_destination(
    text: str,
    start: int,
) -> tuple[int, int, int, str] | None:
    """꺾쇠로 감싼 링크 대상과 선택적 제목 파싱.

    Args:
        text: Markdown 원문.
        start: 여는 꺾쇠 위치.

    Returns:
        대상 범위, 링크 끝, 제목 suffix. 잘못됐으면 ``None``.
    """

    index = start + 1
    while index < len(text):
        char = text[index]
        if char in "\r\n" or char == "<":
            return None
        if char == "\\" and index + 1 < len(text):
            index += 2
            continue
        if char == ">":
            target_end = index
            index += 1
            break
        index += 1
    else:
        return None
    suffix_start = index
    while index < len(text) and text[index] in " \t":
        index += 1
    if index < len(text) and text[index] == ")":
        return start + 1, target_end, index + 1, ""
    return _link_title_suffix(
        text,
        index=index,
        target_start=start + 1,
        target_end=target_end,
        suffix_start=suffix_start,
    )


def _bare_link_destination(
    text: str,
    start: int,
) -> tuple[int, int, int, str] | None:
    """괄호 균형을 적용한 일반 링크 대상과 선택적 제목 파싱.

    Args:
        text: Markdown 원문.
        start: 링크 대상 시작 위치.

    Returns:
        대상 범위, 링크 끝, 제목 suffix. 잘못됐으면 ``None``.
    """

    target = _bare_link_target_end(text, start)
    if target is None:
        return None
    index, closed = target
    if closed:
        return start, index, index + 1, ""
    target_end = index
    while index < len(text) and text[index] in " \t":
        index += 1
    return _link_title_suffix(
        text,
        index=index,
        target_start=start,
        target_end=target_end,
        suffix_start=target_end,
    )


def _bare_link_target_end(text: str, start: int) -> tuple[int, bool] | None:
    """일반 링크 대상의 끝과 즉시 닫힘 여부 탐색.

    Args:
        text: Markdown 원문.
        start: 링크 대상 시작 위치.

    Returns:
        대상 끝 위치와 링크 괄호 닫힘 여부. 잘못됐으면 ``None``.
    """

    depth = 1
    index = start
    while index < len(text):
        index, depth, state = _bare_link_target_step(text, index, depth)
        if state == "invalid":
            return None
        if state == "closed":
            return index, True
        if state == "title":
            return index, False
    return None


def _bare_link_target_step(
    text: str,
    index: int,
    depth: int,
) -> tuple[int, int, str]:
    """일반 링크 대상 문자 하나를 소비하고 괄호 상태 갱신.

    Args:
        text: Markdown 원문.
        index: 현재 문자 위치.
        depth: 현재 괄호 깊이.

    Returns:
        다음 또는 대상 끝 위치, 괄호 깊이, 파싱 상태.
    """

    char = text[index]
    if char in "\r\n":
        return index, depth, "invalid"
    if char == "\\" and index + 1 < len(text):
        return index + 2, depth, "continue"
    if char == "(":
        return index + 1, depth + 1, "continue"
    if char == ")":
        depth -= 1
        next_index = index if depth == 0 else index + 1
        return next_index, depth, "closed" if depth == 0 else "continue"
    if char.isspace():
        return index, depth, "title" if depth == 1 else "invalid"
    return index + 1, depth, "continue"


def _link_destination(
    text: str, start: int
) -> tuple[int, int, int, str] | None:
    """인라인 링크 대상과 제목의 원문 범위."""

    if start >= len(text) or text[start].isspace():
        return None
    if text[start] == ")":
        return start, start, start + 1, ""
    if text[start] == "<":
        return _angle_link_destination(text, start)
    return _bare_link_destination(text, start)


def markdown_links(text: str) -> tuple[MarkdownLink, ...]:
    """destination 괄호 균형을 반영한 인라인 Markdown 링크 목록."""

    links: list[MarkdownLink] = []
    index = 0
    while index < len(text):
        label_start = text.find("[", index)
        if label_start < 0:
            break
        if is_escaped(text, label_start):
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
        target_start, target_end, link_end, title = destination
        image = (
            label_start > 0
            and text[label_start - 1] == "!"
            and not is_escaped(text, label_start - 1)
        )
        link_start = label_start - 1 if image else label_start
        links.append(
            MarkdownLink(
                start=link_start,
                end=link_end,
                image=image,
                label=text[label_start + 1 : label_end],
                target=text[target_start:target_end],
                title=title,
            )
        )
        index = link_end
    return tuple(links)


_URI_AUTOLINK_RE = re.compile(
    r"<([A-Za-z][A-Za-z0-9+.-]{1,31}:[^<>\x00-\x20]+)>"
)
_EMAIL_AUTOLINK_RE = re.compile(
    r"<([A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+)>"
)


def markdown_autolinks(text: str) -> tuple[MarkdownAutolink, ...]:
    """인라인 코드·코드 펜스·HTML 영역 밖의 CommonMark URI·이메일 자동 링크를 문서 순서대로 반환."""

    body = _masked_reference_source(text)
    masked = list(body)
    for start, end, _content in _inline_code_spans(body):
        for index in range(start, end):
            if masked[index] not in "\r\n":
                masked[index] = " "
    body = "".join(masked)

    links: list[MarkdownAutolink] = []
    for match in _URI_AUTOLINK_RE.finditer(body):
        value = match.group(1)
        links.append(MarkdownAutolink(match.start(), match.end(), value, value))
    for match in _EMAIL_AUTOLINK_RE.finditer(body):
        value = match.group(1)
        links.append(
            MarkdownAutolink(
                match.start(),
                match.end(),
                value,
                f"mailto:{value}",
            )
        )
    return tuple(sorted(links, key=lambda link: link.start))


def _normalize_reference_label(label: str) -> str:
    """참조 레이블 정규화."""

    return re.sub(
        r"[ \t\r\n]+",
        " ",
        label.strip(" \t\r\n"),
    ).casefold()


def _reference_label_state(
    value: str,
    start: int,
) -> tuple[str, int | None]:
    """참조 레이블의 완결 상태와 종료 위치."""

    if start >= len(value) or value[start] != "[":
        return "invalid", None
    index = start + 1
    length = 0
    meaningful = False
    while index < len(value):
        index, width, visible, state = _reference_label_step(value, index)
        length += width
        meaningful = meaningful or visible
        if state == "invalid" or length > 999:
            return "invalid", None
        if state == "complete":
            if meaningful and length <= 999:
                return "complete", index - 1
            return "invalid", None
    return "incomplete", None


def _reference_label_step(
    value: str,
    index: int,
) -> tuple[int, int, bool, str]:
    """참조 레이블 문자 하나 또는 escape를 소비.

    Args:
        value: 참조 레이블을 포함한 문자열.
        index: 현재 문자 위치.

    Returns:
        다음 위치, 레이블 길이 증가량, 의미 문자 여부, 상태.
    """

    char = value[index]
    if char == "\\" and index + 1 < len(value):
        escaped = value[index + 1]
        return index + 2, 2, escaped not in " \t\r\n", "continue"
    if char == "[":
        return index + 1, 1, False, "invalid"
    if char == "]":
        return index + 1, 0, False, "complete"
    return index + 1, 1, char not in " \t\r\n", "continue"


def _reference_label_end(value: str, start: int) -> int | None:
    """유효한 참조 레이블의 종료 위치."""

    state, end = _reference_label_state(value, start)
    return end if state == "complete" else None


def _consume_reference_whitespace(
    value: str, index: int
) -> tuple[int, bool]:
    """참조 정의에서 허용되는 공백의 종료 위치."""

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


def _angle_reference_destination(value: str, index: int) -> tuple[str, int] | None:
    """꺾쇠로 감싼 참조 대상과 다음 위치 파싱.

    Args:
        value: 참조 정의 원문.
        index: 여는 꺾쇠 위치.

    Returns:
        대상 문자열과 다음 위치. 잘못됐으면 ``None``.
    """

    start = index + 1
    index = start
    while index < len(value):
        char = value[index]
        if char == "\\" and index + 1 < len(value):
            index += 2
            continue
        if char in "\r\n" or char == "<":
            return None
        if char == ">":
            return value[start:index], index + 1
        index += 1
    return None


def _bare_reference_destination(value: str, index: int) -> tuple[str, int] | None:
    """괄호 균형을 적용한 일반 참조 대상과 다음 위치 파싱.

    Args:
        value: 참조 정의 원문.
        index: 대상 시작 위치.

    Returns:
        대상 문자열과 다음 위치. 잘못됐으면 ``None``.
    """

    start = index
    depth = 0
    while index < len(value) and value[index] not in " \t\r\n":
        char = value[index]
        if char == "\\" and index + 1 < len(value):
            index += 2
            continue
        if char == "<":
            return None
        if char == "(":
            depth += 1
        elif char == ")":
            if depth == 0:
                return None
            depth -= 1
        index += 1
    if index == start or depth:
        return None
    return value[start:index], index


def _reference_destination_at(
    value: str, index: int
) -> tuple[str, int] | None:
    """참조 대상과 대상 다음 위치."""

    if index >= len(value):
        return None
    if value[index] == "<":
        return _angle_reference_destination(value, index)
    return _bare_reference_destination(value, index)


def _scan_reference_title(
    value: str,
    index: int,
    closer: str,
) -> tuple[int | None, bool]:
    """참조 정의 제목의 닫는 구분자와 빈 줄 위반 탐색.

    Args:
        value: 참조 정의 원문.
        index: 제목 본문 시작 위치.
        closer: 제목 닫는 구분자.

    Returns:
        닫는 구분자 다음 위치와 빈 줄 포함 여부.
    """

    while index < len(value):
        char = value[index]
        if char == "\\" and index + 1 < len(value):
            index += 2
            continue
        if char in "\r\n" and _reference_title_has_blank_line(value, index):
            return None, True
        if char == closer:
            return index + 1, False
        index += 1
    return None, False


def _reference_title_has_blank_line(value: str, index: int) -> bool:
    """제목 내부 줄바꿈 다음에 빈 줄이 이어지는지 판정.

    Args:
        value: 참조 정의 원문.
        index: 첫 줄바꿈 위치.

    Returns:
        공백만 있는 다음 줄 포함 여부.
    """

    cursor = index + (2 if value.startswith("\r\n", index) else 1)
    while cursor < len(value) and value[cursor] in " \t":
        cursor += 1
    return cursor < len(value) and value[cursor] in "\r\n"


def _reference_title_start(
    value: str,
    *,
    index: int,
    destination_end: int,
) -> tuple[str, int, int, bool]:
    """참조 대상 뒤 제목의 시작 상태와 위치 결정.

    Args:
        value: 참조 정의 원문.
        index: 대상 바로 다음 위치.
        destination_end: 공백 소비 전 대상 끝 위치.

    Returns:
        상태, 다음 위치, 제목 없는 소비 위치, 다음 줄 제목 여부.
    """

    while index < len(value) and value[index] in " \t":
        index += 1
    no_title_end = index
    if index == len(value):
        return "none", index, no_title_end, False
    title_on_next_line = value[index] in "\r\n"
    if not title_on_next_line:
        state = (
            "title"
            if index != destination_end and value[index] in ('"', "'", "(")
            else "invalid"
        )
        return state, index, no_title_end, False
    index += 2 if value.startswith("\r\n", index) else 1
    while index < len(value) and value[index] in " \t":
        index += 1
    state = (
        "title"
        if index < len(value) and value[index] in ('"', "'", "(")
        else "none"
    )
    return state, index, no_title_end, True


def _reference_definition_title(
    value: str,
    *,
    index: int,
    destination_end: int,
    label: str,
    target: str,
) -> tuple[str, str, str, int] | None:
    """참조 대상 뒤의 선택적 제목과 최종 소비 위치 파싱.

    Args:
        value: 참조 정의 원문.
        index: 대상 다음 위치.
        destination_end: 대상 바로 다음 위치.
        label: 정규화된 참조 레이블.
        target: 파싱한 참조 대상.

    Returns:
        완성된 참조 정의 값. 잘못됐으면 ``None``.
    """

    state, index, no_title_end, title_on_next_line = _reference_title_start(
        value,
        index=index,
        destination_end=destination_end,
    )
    if state == "none":
        return label, target, "", no_title_end
    if state == "invalid":
        return None
    title_start = index
    closer = ")" if value[index] == "(" else value[index]
    title_end, _has_blank_line = _scan_reference_title(value, index + 1, closer)
    if title_end is None:
        if title_on_next_line:
            return label, target, "", no_title_end
        return None
    index = title_end
    while index < len(value) and value[index] in " \t":
        index += 1
    if index < len(value) and value[index] not in "\r\n":
        return (label, target, "", no_title_end) if title_on_next_line else None
    return label, target, value[title_start:title_end], index


def _parse_reference_definition_value(
    value: str,
) -> tuple[str, str, str, int] | None:
    """참조 정의 값 파싱."""

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

    return _reference_definition_title(
        value,
        index=index,
        destination_end=index,
        label=label,
        target=target,
    )


def _reference_container_at(line: str, index: int) -> tuple[int, str] | None:
    """현재 위치의 인용문 또는 목록 컨테이너 접두사 파싱.

    Args:
        line: Markdown 물리 줄.
        index: 컨테이너 검색 시작 위치.

    Returns:
        컨테이너 다음 위치와 종류. 없으면 ``None``.
    """

    spaces = 0
    while index < len(line) and line[index] == " " and spaces < 3:
        index += 1
        spaces += 1
    if index < len(line) and line[index] == ">":
        index += 1
        if index < len(line) and line[index] in " \t":
            index += 1
        return index, "quote"
    marker = re.match(
        r"(?P<bullet>[-+*])|(?P<number>\d{1,9})[.)]",
        line[index:],
    )
    if marker is None or index + marker.end() >= len(line):
        return None
    marker_end = index + marker.end()
    if line[marker_end] not in " \t":
        return None
    padding_end = marker_end
    while padding_end < len(line) and line[padding_end] in " \t":
        padding_end += 1
    padding_width = len(line[:padding_end].expandtabs(4)) - len(
        line[:marker_end].expandtabs(4)
    )
    next_index = padding_end if padding_width <= 4 else marker_end + 1
    kind = "bullet" if marker.group("bullet") else f"ordered:{marker.group('number')}"
    return next_index, kind


def _strip_reference_container(line: str) -> tuple[str, tuple[str, ...]]:
    """참조 정의를 감싼 목록·인용문 컨테이너 제거."""

    index = 0
    containers: list[str] = []
    while index < len(line):
        start = index
        parsed = _reference_container_at(line, index)
        if parsed is None:
            index = start
            break
        index, kind = parsed
        containers.append(kind)
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
    """원시 HTML 블록을 감싼 Markdown 컨테이너의 종료 여부."""

    if not start_container:
        return False
    if current_container[: len(start_container)] == start_container:
        return False
    if "quote" in start_container:
        return True
    leading_width = len(line) - len(line.lstrip(" \t"))
    return leading_width < start_prefix_width


def _raw_html_opening(
    logical: str,
    *,
    line: str,
    offset: int,
    container: tuple[str, ...],
    excluded: list[tuple[int, int]],
) -> tuple[int, re.Pattern[str], tuple[str, ...], int] | None:
    """현재 줄의 명시적 종료형 원시 HTML 시작 규칙 탐색.

    Args:
        logical: Markdown 컨테이너를 제거한 줄.
        line: 원본 물리 줄.
        offset: 문서에서 물리 줄 시작 위치.
        container: 줄을 감싼 Markdown 컨테이너.
        excluded: 시작을 허용하지 않는 코드·주석 범위.

    Returns:
        블록 시작 상태. 일치하는 규칙이 없으면 ``None``.
    """

    logical_offset = len(line) - len(logical)
    for start_pattern, end_pattern in _RAW_HTML_BLOCK_RULES:
        match = start_pattern.match(logical)
        if match is None:
            continue
        opening_offset = offset + logical_offset + match.start()
        if any(start <= opening_offset < end for start, end in excluded):
            continue
        return offset, end_pattern, container, logical_offset
    return None


def _raw_html_block_ranges(
    text: str,
    excluded: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    """명시적인 종료 구분자가 있는 원시 HTML 블록 범위."""

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
            opening = _raw_html_opening(
                logical,
                line=line,
                offset=offset,
                container=container,
                excluded=excluded,
            )
            if opening is not None:
                (
                    start_offset,
                    end_pattern,
                    start_container,
                    start_prefix_width,
                ) = opening

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
    """빈 줄이나 컨테이너 종료로 닫히는 원시 HTML 블록 범위."""

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
    """참조 파싱에서 제외할 코드 펜스·HTML 영역 마스킹."""

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
    """현재 줄에서 참조 정의를 시작할 수 있는지 여부."""

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


def _reference_source_lines(
    text: str,
) -> tuple[list[str], list[str], list[tuple[str, ...]], list[int]]:
    """참조 정의 파싱용 원본·논리 줄과 컨테이너·offset 구성.

    Args:
        text: Markdown 원문.

    Returns:
        원본 줄, 논리 줄, 컨테이너, 줄 시작 offset 목록.
    """

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
    for raw_line, masked_line in zip(raw_lines, masked_lines, strict=True):
        offsets.append(offset)
        offset += len(raw_line)
        line = masked_line.rstrip("\r\n")
        logical, container = _strip_reference_container(line)
        logical_lines.append(logical)
        containers.append(container)
    return raw_lines, logical_lines, containers, offsets


def _multiline_reference_text(
    logical_lines: list[str],
    containers: list[tuple[str, ...]],
    line_index: int,
) -> tuple[str, bool]:
    """현재 줄부터 같은 컨테이너의 참조 정의 후보 결합.

    Args:
        logical_lines: 컨테이너를 제거한 전체 줄.
        containers: 줄별 Markdown 컨테이너.
        line_index: 참조 정의 후보 시작 줄.

    Returns:
        결합한 후보 문자열과 레이블 형식 오류 여부.
    """

    start_container = containers[line_index]
    candidate_lines: list[str] = []
    label_complete = False
    for end_line in range(line_index, len(logical_lines)):
        if end_line > line_index and not _same_reference_container(
            start_container,
            containers[end_line],
        ):
            break
        logical = logical_lines[end_line]
        if end_line > line_index and not logical.strip():
            break
        candidate_lines.append(logical)
        label_complete, invalid = _multiline_label_state(
            candidate_lines,
            label_complete=label_complete,
        )
        if invalid:
            return "\n".join(candidate_lines), True
    return "\n".join(candidate_lines), False


def _same_reference_container(
    start_container: tuple[str, ...],
    current_container: tuple[str, ...],
) -> bool:
    """후속 줄이 참조 정의 시작 컨테이너 내부에 머무는지 판정.

    Args:
        start_container: 시작 줄의 Markdown 컨테이너.
        current_container: 후속 줄의 Markdown 컨테이너.

    Returns:
        같은 컨테이너 범위에 속하는지 여부.
    """

    return len(current_container) <= len(start_container) and start_container[
        : len(current_container)
    ] == current_container


def _multiline_label_state(
    candidate_lines: list[str],
    *,
    label_complete: bool,
) -> tuple[bool, bool]:
    """여러 줄 참조 후보의 레이블 완결·오류 상태 갱신.

    Args:
        candidate_lines: 현재까지 결합한 논리 줄.
        label_complete: 이전 줄까지 레이블 완결 여부.

    Returns:
        갱신된 완결 여부와 형식 오류 여부.
    """

    if label_complete:
        return True, False
    label_candidate = "\n".join(candidate_lines)
    indent = len(label_candidate) - len(label_candidate.lstrip(" "))
    state, label_end = _reference_label_state(label_candidate, indent)
    if state == "invalid":
        return False, True
    if state != "complete":
        return False, False
    return True, not label_candidate.startswith("]:", label_end)


def _reference_definition_at(
    logical_lines: list[str],
    containers: list[tuple[str, ...]],
    line_index: int,
) -> tuple[str, tuple[str, str, str, int]] | None:
    """현재 줄에서 단일 또는 여러 줄 참조 정의 파싱.

    Args:
        logical_lines: 컨테이너를 제거한 전체 줄.
        containers: 줄별 Markdown 컨테이너.
        line_index: 참조 정의 후보 시작 줄.

    Returns:
        파싱에 사용한 문자열과 참조 정의 값. 실패 시 ``None``.
    """

    parsed_text = logical_lines[line_index]
    parsed = _parse_reference_definition_value(parsed_text)
    next_line = line_index + 1
    needs_multiline = parsed is None or (
        not parsed[2]
        and next_line < len(logical_lines)
        and logical_lines[next_line].lstrip(" \t").startswith(('"', "'", "("))
    )
    if needs_multiline:
        parsed_text, invalid = _multiline_reference_text(
            logical_lines,
            containers,
            line_index,
        )
        parsed = None if invalid else _parse_reference_definition_value(parsed_text)
    return None if parsed is None else (parsed_text, parsed)


def _parse_reference_definitions(
    text: str,
) -> tuple[MarkdownReferenceDefinition, ...]:
    """참조 정의 목록 파싱."""

    raw_lines, logical_lines, containers, offsets = _reference_source_lines(text)

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

        definition = _reference_definition_at(
            logical_lines,
            containers,
            line_index,
        )
        if definition is None:
            line_index += 1
            continue
        parsed_text, parsed = definition
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
    """문서별로 캐시된 참조 정의 목록."""

    return _parse_reference_definitions(text)


def reference_definitions(
    text: str,
) -> tuple[MarkdownReferenceDefinition, ...]:
    """주석·코드 펜스·원시 HTML 블록 밖의 참조 정의 목록."""

    if len(text) < 16_384:
        return _parse_reference_definitions(text)
    return _cached_reference_definitions(text)


def reference_definition_line_numbers(text: str) -> frozenset[int]:
    """참조 정의가 차지하는 0-based 줄 번호 집합."""

    return frozenset(
        line
        for definition in reference_definitions(text)
        for line in range(definition.start_line, definition.end_line + 1)
    )


@lru_cache(maxsize=16)
def mask_reference_definitions(text: str) -> str:
    """참조 정의 영역 마스킹."""

    masked = list(text)
    for definition in reference_definitions(text):
        for index in range(definition.start, definition.end):
            if masked[index] not in "\r\n":
                masked[index] = " "
    return "".join(masked)


def is_reference_definition_block(text: str) -> bool:
    """참조 정의만으로 구성된 블록인지 여부."""

    definitions = reference_definitions(text)
    return bool(definitions) and not mask_reference_definitions(text).strip()


def is_reference_definition_line(line: str) -> bool:
    """단일 물리 줄의 완전한 참조 정의 여부."""

    if "\n" in line or "\r" in line:
        return False
    logical, _containers = _strip_reference_container(line)
    parsed = _parse_reference_definition_value(logical)
    return parsed is not None and parsed[3] == len(logical)


def _masked_inline_code(text: str) -> str:
    """인라인 코드 내용을 줄 위치 보존 공백으로 마스킹.

    Args:
        text: Markdown 원문.

    Returns:
        인라인 코드가 마스킹된 문자열.
    """

    masked = list(text)
    for start, end, _content in _inline_code_spans(text):
        for index in range(start, end):
            if masked[index] not in "\r\n":
                masked[index] = " "
    return "".join(masked)


def _reference_link_label(
    body: str,
    *,
    start: int,
    text_end: int,
) -> tuple[str, int] | None:
    """참조형 링크의 해석용 레이블과 마지막 대괄호 위치 추출.

    Args:
        body: 보호 범위가 마스킹된 Markdown.
        start: 표시 레이블 여는 대괄호 위치.
        text_end: 표시 레이블 닫는 대괄호 위치.

    Returns:
        원시 참조 레이블과 참조 구문 끝 위치. 참조형이 아니면 ``None``.
    """

    following = text_end + 1
    if following < len(body) and body[following] == "(":
        return None
    if following < len(body) and body[following] == "[":
        if following + 1 < len(body) and body[following + 1] == "]":
            return body[start + 1 : text_end], following + 1
        label_end = _reference_label_end(body, following)
        if label_end is None:
            return None
        return body[following + 1 : label_end], label_end
    if _reference_label_end(body, start) != text_end:
        return None
    return body[start + 1 : text_end], text_end


def _resolved_reference_at(
    body: str,
    start: int,
    effective: dict[str, tuple[str, str]],
) -> tuple[tuple[bool, str, str, str] | None, int]:
    """현재 대괄호에서 참조형 링크 서명과 다음 검색 위치 계산.

    Args:
        body: 보호 범위가 마스킹된 Markdown.
        start: 표시 레이블 여는 대괄호 위치.
        effective: 최초 정의 우선 참조 대상 mapping.

    Returns:
        해석된 링크 서명과 다음 검색 위치.
    """

    if is_escaped(body, start):
        return None, start + 1
    text_end = _closing_label_bracket(body, start + 1)
    if text_end is None:
        return None, start + 1
    following = text_end + 1
    if following < len(body) and body[following] == "(":
        return None, following + 1
    reference = _reference_link_label(body, start=start, text_end=text_end)
    if reference is None:
        return None, text_end + 1
    raw_label, reference_end = reference
    resolved = effective.get(_normalize_reference_label(raw_label))
    if resolved is None:
        return None, reference_end + 1
    image = (
        start > 0
        and body[start - 1] == "!"
        and not is_escaped(body, start - 1)
    )
    target, title = resolved
    signature = (image, body[start + 1 : text_end], target, title)
    return signature, reference_end + 1


def _resolved_reference_link_signatures(
    text: str,
) -> tuple[tuple[bool, str, str, str], ...]:
    """정의가 확인된 참조형 링크의 구조 서명."""

    effective: dict[str, tuple[str, str]] = {}
    for definition in reference_definitions(text):
        effective.setdefault(
            definition.label,
            (definition.target, definition.title),
        )
    if not effective:
        return ()

    body = _masked_inline_code(
        mask_reference_definitions(_masked_reference_source(text))
    )

    signatures: list[tuple[bool, str, str, str]] = []
    index = 0
    while index < len(body):
        start = body.find("[", index)
        if start < 0:
            break
        signature, index = _resolved_reference_at(body, start, effective)
        if signature is not None:
            signatures.append(signature)
    return tuple(signatures)


def reference_link_signatures(
    text: str,
) -> tuple[tuple[bool, str, str], ...]:
    """CommonMark 최초 정의 우선 규칙으로 해석한 참조형 링크 목록."""

    return tuple(
        (image, target, title)
        for image, _display, target, title in _resolved_reference_link_signatures(
            text
        )
    )


def reference_link_display_signatures(
    text: str,
) -> tuple[tuple[bool, str], ...]:
    """해석된 참조형 링크의 이미지 상태와 정확한 표시 레이블 목록."""

    return tuple(
        (image, display)
        for image, display, _target, _title in _resolved_reference_link_signatures(
            text
        )
    )


def strip_markdown_links(text: str) -> str:
    """텍스트에서 완전한 인라인 Markdown 링크와 이미지 제거."""

    out: list[str] = []
    index = 0
    for link in markdown_links(text):
        out.append(text[index : link.start])
        index = link.end
    out.append(text[index:])
    return "".join(out)


def normalize_annotation_anchor(text: str) -> str:
    """원문과 이스케이프된 HTML 주석 표현을 같은 형식으로 정규화."""

    text = text.replace("*&#47;", "*/").replace("--&gt;", "-->")
    return " ".join(text.split())


def is_non_annotatable_line(line: str) -> bool:
    """Markdown 줄이 번역 대상이 아닌 구조 요소인지 여부."""

    stripped = line.strip()
    if not stripped:
        return False
    if is_named_anchor_line(stripped):
        return True
    if is_reference_definition_line(line):
        return True
    if stripped.startswith(("<!--", ">", "|")):
        return True
    if (
        re.match(r"^(?:[-*+]\s+|\d+[.)]\s+)\[", stripped)
        and "](#" in stripped
    ):
        return True
    return is_structural_html_line(line)


def is_structural_html_fragment(text: str) -> bool:
    """텍스트가 HTML 태그와 공백만 포함하는지 여부."""

    return bool(structural_html_tags(text))


def is_structural_html_line(line: str) -> bool:
    """최상위 Markdown 줄이 HTML 태그만 포함하는지 여부."""

    return bool(line and not line[:1].isspace() and is_structural_html_fragment(line))


def structural_html_tags(text: str) -> tuple[str, ...]:
    """``text``가 태그만 있는 HTML 조각일 때 태그를 문서 순서대로 반환."""

    position = 0
    tags: list[str] = []
    for match in _HTML_TAG_RE.finditer(text):
        if text[position : match.start()].strip():
            return ()
        tags.append(match.group(0))
        position = match.end()
    return tuple(tags) if tags and not text[position:].strip() else ()


def html_tags(text: str) -> tuple[str, ...]:
    """모든 HTML 태그 토큰을 문서 순서대로 반환."""

    return tuple(match.group(0) for match in _HTML_TAG_RE.finditer(text))


def html_code_contents(text: str) -> tuple[str, ...]:
    """원시 HTML ``code`` 요소의 내용을 문서 순서대로 반환."""

    return tuple(match.group(1) for match in _HTML_CODE_ELEMENT_RE.finditer(text))


def strip_html_code_elements(text: str) -> str:
    """보호된 내용을 포함한 원시 HTML ``code`` 요소 제거."""

    return _HTML_CODE_ELEMENT_RE.sub("", text)


def split_line_ending(line: str) -> tuple[str, str]:
    """본문과 줄 끝 문자 분할."""

    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    if line.endswith("\r"):
        return line[:-1], "\r"
    return line, ""


def fence_token(line: str) -> str | None:
    """Markdown 인용문 깊이를 접두사로 포함한 코드 펜스 토큰."""
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
    """현재 줄이 주어진 Markdown 코드 펜스를 닫는지 여부."""

    token = fence_token(line)
    if not token or not opening:
        return False
    token_depth = len(token) - len(token.lstrip(">"))
    opening_depth = len(opening) - len(opening.lstrip(">"))
    token_fence = token[token_depth:]
    opening_fence = opening[opening_depth:]
    stripped, _ending = split_line_ending(line)
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
    """경계 줄을 보존하며 코드 펜스 내용 마스킹."""

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
    """Markdown 제목 줄인지 여부."""

    stripped = line.lstrip(" ")
    if len(line) - len(stripped) > 3 or stripped.startswith("\t"):
        return False
    level = len(stripped) - len(stripped.lstrip("#"))
    return 1 <= level <= 6 and len(stripped) > level and stripped[level].isspace()


def is_ordered_list_marker(line: str) -> bool:
    """순서 있는 목록 표식인지 여부."""

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
    """제목 한 줄에서 ``{.class}`` 형식의 제목 속성 제거."""

    body, ending = split_line_ending(line)
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
    """HTML 주석 밖의 제목에서 ``{.class}`` 형식의 제목 속성 제거."""

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
    """제거 가능한 ``{.class}`` 형식의 제목 속성 포함 여부."""

    return strip_title_attrs(text) != text


def _fenced_code_ranges(text: str) -> list[tuple[int, int]]:
    """문서에 포함된 코드 펜스 블록 범위."""

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
    """HTML 주석 범위 파싱."""

    spans: list[tuple[int, int, str]] = []
    protected_ranges = sorted(
        [
            (start, end)
            for start, end, _content in _inline_code_spans(text)
        ]
        + _fenced_code_ranges(text)
    )
    range_index = 0
    index = 0
    while index < len(text):
        while (
            range_index < len(protected_ranges)
            and protected_ranges[range_index][0] < index
        ):
            range_index += 1

        comment_start = text.find("<!--", index)
        protected_start = (
            protected_ranges[range_index][0]
            if range_index < len(protected_ranges)
            else len(text)
        )
        if comment_start < 0 and protected_start == len(text):
            break
        if comment_start < 0 or protected_start <= comment_start:
            index = protected_ranges[range_index][1]
            range_index += 1
            continue

        end = text.find("-->", comment_start + 4)
        if end < 0:
            break
        spans.append(
            (comment_start, end + 3, text[comment_start + 4 : end])
        )
        index = end + 3
    return tuple(spans)


def _mask_range(characters: list[str], start: int, end: int) -> None:
    """줄바꿈을 보존하며 지정 문자 범위를 공백으로 마스킹.

    Args:
        characters: 변경할 문서 문자 목록.
        start: 마스킹 시작 위치.
        end: 마스킹 끝 위치.
    """

    for position in range(start, end):
        if characters[position] not in "\r\n":
            characters[position] = " "


def _comment_delimiter_source(text: str) -> str:
    """머리말·코드 펜스·들여쓰기 코드를 제외한 구분자 검사 원문 구성.

    Args:
        text: Markdown 원문.

    Returns:
        제외 범위가 공백으로 마스킹된 문자열.
    """

    masked = list(text)
    for start, end in _fenced_code_ranges(text):
        _mask_range(masked, start, end)
    offset = 0
    in_front_matter = False
    for lineno, line in enumerate(text.splitlines(keepends=True)):
        stripped = line.strip()
        if lineno == 0 and stripped == "---":
            in_front_matter = True
        if in_front_matter:
            _mask_range(masked, offset, offset + len(line))
            if lineno > 0 and stripped == "---":
                in_front_matter = False
        elif line.startswith("\t") or len(line) - len(line.lstrip(" ")) >= 4:
            _mask_range(masked, offset, offset + len(line))
        offset += len(line)
    return "".join(masked)


def _mask_inline_code_for_comment_check(body: str) -> str:
    """주석과 충돌하지 않는 인라인 코드만 구분자 검사에서 마스킹.

    Args:
        body: 다른 코드 범위가 이미 마스킹된 Markdown.

    Returns:
        독립 인라인 코드까지 마스킹된 문자열.
    """

    comment_spans = [
        (start, end) for start, end, _body in html_comment_spans(body)
    ]
    inline_spans = [
        (start, end) for start, end, _content in _inline_code_spans(body)
    ]
    if not inline_spans:
        return body
    masked = list(body)
    for start, end in inline_spans:
        relation = _comment_span_relation(start, end, comment_spans)
        if relation == "inside":
            opener = body.find("<!--", start, end)
            while opener >= 0:
                masked[opener : opener + 4] = " " * 4
                opener = body.find("<!--", opener + 4, end)
        elif relation == "outside":
            _mask_range(masked, start, end)
    return "".join(masked)


def _comment_span_relation(
    start: int,
    end: int,
    comment_spans: list[tuple[int, int]],
) -> str:
    """범위와 HTML 주석들의 포함·중첩 관계 분류.

    Args:
        start: 검사 범위 시작 위치.
        end: 검사 범위 끝 위치.
        comment_spans: HTML 주석 범위 목록.

    Returns:
        ``inside``, ``overlap`` 또는 ``outside``.
    """

    if any(
        comment_start <= start and end <= comment_end
        for comment_start, comment_end in comment_spans
    ):
        return "inside"
    if any(
        start < comment_end and end > comment_start
        for comment_start, comment_end in comment_spans
    ):
        return "overlap"
    return "outside"


def _has_malformed_comment_sequence(body: str) -> bool:
    """보호 범위를 제거한 문서의 HTML 주석 구분자 순서 검사.

    Args:
        body: 검사할 마스킹된 Markdown.

    Returns:
        닫힘 누락·선행 닫힘·중첩 opener 포함 여부.
    """

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


@lru_cache(maxsize=16)
def _cached_html_comment_spans(
    text: str,
) -> tuple[tuple[int, int, str], ...]:
    """문서별로 캐시된 HTML 주석 범위."""

    return _parse_html_comment_spans(text)


def html_comment_spans(text: str) -> list[tuple[int, int, str]]:
    """Markdown 인라인 코드와 코드 펜스 밖의 HTML 주석 범위."""

    spans = (
        _parse_html_comment_spans(text)
        if len(text) < 16_384
        else _cached_html_comment_spans(text)
    )
    return list(spans)


def has_malformed_html_comment_delimiters(text: str) -> bool:
    """front matter·코드 펜스·들여쓰기 코드·인라인 코드 밖에서 HTML 주석 구분자의 균형이 깨졌는지 여부."""

    body = _comment_delimiter_source(text)
    return _has_malformed_comment_sequence(
        _mask_inline_code_for_comment_check(body)
    )


def strip_html_comments(text: str) -> str:
    """인라인 코드와 코드 펜스 밖의 HTML 주석 제거."""

    out: list[str] = []
    index = 0
    for start, end, _body in html_comment_spans(text):
        out.append(text[index:start])
        index = end
    out.append(text[index:])
    return "".join(out)


def html_comment_bodies(text: str) -> list[str]:
    """인라인 코드와 코드 펜스 밖의 HTML 주석 본문 목록."""

    return [body for _start, _end, body in html_comment_spans(text)]


def _standalone_comment_line_state(
    line: str,
    *,
    in_code: bool,
    fence: str,
    in_comment: bool,
) -> tuple[bool, bool, str, bool]:
    """단일 줄의 독립 HTML 주석 포함 여부와 parser 상태 갱신.

    Args:
        line: Markdown 물리 줄.
        in_code: 이전 줄까지 코드 펜스 내부 여부.
        fence: 활성 코드 펜스 token.
        in_comment: 이전 줄에서 시작한 독립 주석 내부 여부.

    Returns:
        줄 포함 여부, 코드 내부 상태, fence token, 주석 내부 상태.
    """

    if in_comment:
        return True, in_code, fence, "-->" not in line
    token = fence_token(line)
    if token:
        if not in_code:
            return False, True, token, False
        if closes_fence(line, fence):
            return False, False, fence, False
        return False, in_code, fence, False
    if in_code:
        return False, in_code, fence, False
    stripped = line.lstrip()
    if not stripped.startswith("<!--"):
        return False, in_code, fence, False
    return True, in_code, fence, "-->" not in stripped[4:]


def standalone_html_comment_line_numbers(text: str) -> frozenset[int]:
    """코드 펜스 밖의 독립 HTML 주석이 차지하는 1-based 줄 번호 집합."""

    lines = text.splitlines()
    numbers: set[int] = set()
    in_code = False
    fence = ""
    in_comment = False
    for lineno, line in enumerate(lines, start=1):
        include, in_code, fence, in_comment = _standalone_comment_line_state(
            line,
            in_code=in_code,
            fence=fence,
            in_comment=in_comment,
        )
        if include:
            numbers.add(lineno)
    return frozenset(numbers)


def _protected_table_token(
    body: str,
    index: int,
    links: dict[int, MarkdownLink],
) -> tuple[str, int] | None:
    """표 셀 분할에서 보호할 링크·escape·inline code token 추출.

    Args:
        body: 표 물리 줄.
        index: 현재 문자 위치.
        links: 시작 위치별 Markdown 링크.

    Returns:
        보호 token과 다음 위치. 일반 문자면 ``None``.
    """

    link = links.get(index)
    if link is not None:
        return body[link.start : link.end], link.end
    if body[index] == "\\" and index + 1 < len(body):
        return body[index : index + 2], index + 2
    if body[index] != "`":
        return None
    end = index + 1
    while end < len(body) and body[end] == "`":
        end += 1
    fence = body[index:end]
    closing = body.find(fence, end)
    if closing < 0:
        return None
    closing += len(fence)
    return body[index:closing], closing


def table_row_cells(line: str) -> list[str]:
    """escape, inline code 또는 Markdown 링크에 포함된 pipe를 제외하고 table row 분할.

    GFM 표는 인라인 파싱 이전에 셀을 나누므로, 셀 안의 pipe는 inline code
    안에서도 ``\\|``로만 표현할 수 있다. 표 셀을 다루는 모든 단계가 같은
    경계를 보도록 이 함수를 공용 분할기로 사용한다.

    Args:
        line: 표 물리 줄.

    Returns:
        앞뒤 구분자를 제외한 셀 목록.
    """

    body = line.strip()
    links = {link.start: link for link in markdown_links(body)}
    cells: list[str] = []
    current: list[str] = []
    index = 0
    while index < len(body):
        protected = _protected_table_token(body, index, links)
        if protected is not None:
            token, index = protected
            current.append(token)
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


def gfm_table_row_cells(line: str) -> list[str] | None:
    """바깥쪽 pipe 유무를 반영해 GFM 표 행의 cell을 분리."""

    if line.startswith("\t") or len(line) - len(line.lstrip(" ")) >= 4:
        return None
    body = line.strip()
    cells = table_row_cells(line)
    if len(cells) >= 2 or (
        len(cells) == 1 and body.startswith("|") and body.endswith("|")
    ):
        return cells
    return None


def is_gfm_pipe_table_candidate(text: str) -> bool:
    """문자열이 GFM pipe table의 머리글·구분 행으로 시작하는지 판정."""

    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) < 2:
        return False
    header = gfm_table_row_cells(lines[0])
    separator = gfm_table_row_cells(lines[1])
    return bool(
        header is not None
        and separator is not None
        and all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator)
    )


def is_gfm_pipe_table(text: str) -> bool:
    """문자열이 직사각형 GFM pipe table 블록인지 판정."""

    lines = [line for line in text.splitlines() if line.strip()]
    if not is_gfm_pipe_table_candidate(text):
        return False
    rows = [gfm_table_row_cells(line) for line in lines]
    if any(row is None for row in rows):
        return False
    parsed = [row for row in rows if row is not None]
    if len({len(row) for row in parsed}) != 1:
        return False
    return all(re.fullmatch(r":?-{3,}:?", cell) for cell in parsed[1])


def mask_html_comments(text: str) -> str:
    """줄 위치를 보존하며 HTML 주석의 줄바꿈 외 문자를 공백으로 마스킹."""

    chars = list(text)
    for start, end, _body in html_comment_spans(text):
        for index in range(start, end):
            if chars[index] not in "\r\n":
                chars[index] = " "
    return "".join(chars)


def quote_depth(line: str) -> int:
    """Markdown 줄의 blockquote 깊이 계산."""

    stripped = line.lstrip()
    depth = 0
    while stripped.startswith(">"):
        depth += 1
        stripped = stripped[1:].lstrip()
    return depth


def is_named_anchor_line(line: str) -> bool:
    """이름이 지정된 독립 HTML 앵커 줄인지 여부."""

    stripped = line.strip()
    lower = stripped.lower()
    if not lower.startswith("<a") or "name=" not in lower:
        return False
    if len(stripped) > 2 and not (stripped[2].isspace() or stripped[2] == ">"):
        return False
    if not (stripped.endswith(">") or lower.endswith("</a>")):
        return False
    return True
