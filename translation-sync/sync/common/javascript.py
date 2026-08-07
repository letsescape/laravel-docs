"""균형 잡힌 JSX 표현식을 위한 최소 JavaScript lexical scan."""
from __future__ import annotations


_REGEX_PREFIX_KEYWORDS = {
    "await",
    "case",
    "delete",
    "do",
    "else",
    "in",
    "instanceof",
    "new",
    "of",
    "return",
    "throw",
    "typeof",
    "void",
    "yield",
}
_CONTROL_PAREN_KEYWORDS = {
    "catch",
    "for",
    "if",
    "switch",
    "while",
    "with",
}


def _string_end(text: str, start: int) -> int | None:
    """JavaScript 문자열 literal의 종료 위치."""

    quote = text[start]
    cursor = start + 1
    while cursor < len(text):
        if text[cursor] == "\\":
            cursor += 2
            continue
        if text[cursor] == quote:
            return cursor + 1
        if text[cursor] in "\r\n":
            return None
        cursor += 1
    return None


def _regex_end(text: str, start: int) -> int | None:
    """JavaScript 정규식 literal의 종료 위치."""

    cursor = start + 1
    in_character_class = False
    while cursor < len(text):
        char = text[cursor]
        if char == "\\":
            cursor += 2
            continue
        if char in "\r\n":
            return None
        if char == "[":
            in_character_class = True
        elif char == "]" and in_character_class:
            in_character_class = False
        elif char == "/" and not in_character_class:
            cursor += 1
            while cursor < len(text) and (
                text[cursor].isalpha() or text[cursor].isdigit()
            ):
                cursor += 1
            return cursor
        cursor += 1
    return None


def _possible_regex_end(
    text: str,
    start: int,
    *,
    expects_operand: bool,
) -> int | None:
    """현재 문맥에서 가능한 정규식 literal의 종료 위치."""

    end = _regex_end(text, start)
    if end is None:
        return None
    if expects_operand:
        return end
    if any(char in "()[]{}'\"`" for char in text[start + 1 : end]):
        return end
    return None


def _template_end(text: str, start: int) -> int | None:
    """중첩 표현식을 포함한 template literal의 종료 위치."""

    cursor = start + 1
    while cursor < len(text):
        char = text[cursor]
        if char == "\\":
            cursor += 2
            continue
        if char == "`":
            return cursor + 1
        if char == "$" and cursor + 1 < len(text) and text[cursor + 1] == "{":
            expression_end = balanced_expression_end(text, cursor + 1)
            if expression_end is None:
                return None
            cursor = expression_end
            continue
        cursor += 1
    return None


def balanced_expression_end(text: str, start: int) -> int | None:
    """괄호와 literal을 고려한 JavaScript 표현식의 종료 위치."""

    pairs = {"(": ")", "[": "]", "{": "}"}
    opener = text[start]
    if opener not in pairs:
        return None

    stack: list[tuple[str, bool]] = [(pairs[opener], False)]
    cursor = start + 1
    expects_operand = True
    pending_control_parenthesis = False
    while cursor < len(text):
        char = text[cursor]
        if char.isspace():
            cursor += 1
            continue
        if char in ("'", '"'):
            end = _string_end(text, cursor)
            if end is None:
                return None
            cursor = end
            expects_operand = False
            pending_control_parenthesis = False
            continue
        if char == "`":
            end = _template_end(text, cursor)
            if end is None:
                return None
            cursor = end
            expects_operand = False
            pending_control_parenthesis = False
            continue
        if char == "/" and cursor + 1 < len(text):
            following = text[cursor + 1]
            if following == "/":
                newline = min(
                    (
                        position
                        for position in (
                            text.find("\n", cursor + 2),
                            text.find("\r", cursor + 2),
                        )
                        if position >= 0
                    ),
                    default=len(text),
                )
                cursor = newline
                continue
            if following == "*":
                end = text.find("*/", cursor + 2)
                if end < 0:
                    return None
                cursor = end + 2
                continue
            end = _possible_regex_end(
                text,
                cursor,
                expects_operand=expects_operand,
            )
            if end is not None:
                cursor = end
                expects_operand = False
                pending_control_parenthesis = False
                continue
            cursor += 1
            expects_operand = True
            pending_control_parenthesis = False
            continue
        if char in pairs:
            control_parenthesis = (
                char == "(" and pending_control_parenthesis
            )
            stack.append((pairs[char], control_parenthesis))
            cursor += 1
            expects_operand = True
            pending_control_parenthesis = False
            continue
        if char in ")]}":
            if char != stack[-1][0]:
                return None
            _closer, control_parenthesis = stack.pop()
            cursor += 1
            if not stack:
                return cursor
            expects_operand = control_parenthesis
            pending_control_parenthesis = False
            continue
        if char.isalpha() or char in "_$" or ord(char) > 127:
            end = cursor + 1
            while end < len(text) and (
                text[end].isalnum()
                or text[end] in "_$"
                or ord(text[end]) > 127
            ):
                end += 1
            token = text[cursor:end]
            expects_operand = token in _REGEX_PREFIX_KEYWORDS
            pending_control_parenthesis = token in _CONTROL_PAREN_KEYWORDS
            cursor = end
            continue
        if char.isdigit():
            cursor += 1
            while cursor < len(text) and (
                text[cursor].isalnum() or text[cursor] in "._"
            ):
                cursor += 1
            expects_operand = False
            pending_control_parenthesis = False
            continue
        if char == ".":
            if text.startswith("...", cursor):
                cursor += 3
                expects_operand = True
            else:
                cursor += 1
                expects_operand = False
            pending_control_parenthesis = False
            continue
        if char in ",;:?=+*-!~%&|^<>":
            cursor += 1
            expects_operand = True
            pending_control_parenthesis = False
            continue
        cursor += 1
        expects_operand = False
        pending_control_parenthesis = False
    return None


def top_level_plus_positions(text: str) -> tuple[int, ...] | None:
    """JavaScript 최상위 덧셈 연산자의 위치 목록."""

    pairs = {"(": ")", "[": "]", "{": "}"}
    stack: list[tuple[str, bool]] = []
    pluses: list[int] = []
    cursor = 0
    expects_operand = True
    pending_control_parenthesis = False
    while cursor < len(text):
        char = text[cursor]
        if char.isspace():
            cursor += 1
            continue
        if char in ("'", '"'):
            end = _string_end(text, cursor)
            if end is None:
                return None
            cursor = end
            expects_operand = False
            pending_control_parenthesis = False
            continue
        if char == "`":
            end = _template_end(text, cursor)
            if end is None:
                return None
            cursor = end
            expects_operand = False
            pending_control_parenthesis = False
            continue
        if char == "/" and cursor + 1 < len(text):
            following = text[cursor + 1]
            if following == "/":
                cursor = min(
                    (
                        position
                        for position in (
                            text.find("\n", cursor + 2),
                            text.find("\r", cursor + 2),
                        )
                        if position >= 0
                    ),
                    default=len(text),
                )
                continue
            if following == "*":
                end = text.find("*/", cursor + 2)
                if end < 0:
                    return None
                cursor = end + 2
                continue
            end = _possible_regex_end(
                text,
                cursor,
                expects_operand=expects_operand,
            )
            if end is not None:
                cursor = end
                expects_operand = False
                pending_control_parenthesis = False
                continue
            cursor += 1
            expects_operand = True
            pending_control_parenthesis = False
            continue
        if char in pairs:
            control_parenthesis = (
                char == "(" and pending_control_parenthesis
            )
            stack.append((pairs[char], control_parenthesis))
            cursor += 1
            expects_operand = True
            pending_control_parenthesis = False
            continue
        if char in ")]}":
            if not stack or char != stack[-1][0]:
                return None
            _closer, control_parenthesis = stack.pop()
            cursor += 1
            expects_operand = control_parenthesis
            pending_control_parenthesis = False
            continue
        if char.isalpha() or char in "_$" or ord(char) > 127:
            end = cursor + 1
            while end < len(text) and (
                text[end].isalnum()
                or text[end] in "_$"
                or ord(text[end]) > 127
            ):
                end += 1
            token = text[cursor:end]
            expects_operand = token in _REGEX_PREFIX_KEYWORDS
            pending_control_parenthesis = token in _CONTROL_PAREN_KEYWORDS
            cursor = end
            continue
        if char.isdigit():
            cursor += 1
            while cursor < len(text) and (
                text[cursor].isalnum() or text[cursor] in "._"
            ):
                cursor += 1
            expects_operand = False
            pending_control_parenthesis = False
            continue
        if char == ".":
            if text.startswith("...", cursor):
                cursor += 3
                expects_operand = True
            else:
                cursor += 1
                expects_operand = False
            pending_control_parenthesis = False
            continue
        if char == "+":
            if not stack:
                pluses.append(cursor)
            cursor += 1
            expects_operand = True
            pending_control_parenthesis = False
            continue
        if char in ",;:?=*-!~%&|^<>":
            cursor += 1
            expects_operand = True
            pending_control_parenthesis = False
            continue
        cursor += 1
        expects_operand = False
        pending_control_parenthesis = False
    if stack:
        return None
    return tuple(pluses)
