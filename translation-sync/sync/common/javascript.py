"""균형 잡힌 JSX 표현식을 위한 최소 JavaScript 어휘 스캔."""
from __future__ import annotations

from dataclasses import dataclass, field


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
    """JavaScript 문자열 리터럴의 종료 위치."""

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
    """JavaScript 정규식 리터럴의 종료 위치."""

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
            return _regex_flags_end(text, cursor + 1)
        cursor += 1
    return None


def _regex_flags_end(text: str, start: int) -> int:
    """JavaScript 정규식 플래그 바로 다음 위치 탐색.

    Args:
        text: JavaScript 원문.
        start: 닫는 슬래시 바로 다음 위치.

    Returns:
        영문자·숫자 플래그가 끝나는 위치.
    """

    cursor = start
    while cursor < len(text) and (
        text[cursor].isalpha() or text[cursor].isdigit()
    ):
        cursor += 1
    return cursor


def _possible_regex_end(
    text: str,
    start: int,
    *,
    expects_operand: bool,
) -> int | None:
    """현재 문맥에서 정규식일 수 있는 리터럴의 종료 위치."""

    end = _regex_end(text, start)
    if end is None:
        return None
    if expects_operand:
        return end
    if any(char in "()[]{}'\"`" for char in text[start + 1 : end]):
        return end
    return None


def _template_end(text: str, start: int) -> int | None:
    """중첩 표현식을 포함한 템플릿 리터럴의 종료 위치."""

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


@dataclass
class _ScanState:
    """JavaScript 어휘 스캔의 현재 위치와 연산자 문맥."""

    cursor: int
    stack: list[tuple[str, bool]] = field(default_factory=list)
    expects_operand: bool = True
    pending_control_parenthesis: bool = False

    def consume_value(self, end: int) -> None:
        """값 token 소비 뒤 위치와 연산자 문맥 갱신.

        Args:
            end: 소비한 token 바로 다음 위치.
        """

        self.cursor = end
        self.expects_operand = False
        self.pending_control_parenthesis = False

    def consume_operator(self, width: int = 1) -> None:
        """연산자 token 소비 뒤 위치와 피연산자 문맥 갱신.

        Args:
            width: 소비할 문자 수.
        """

        self.cursor += width
        self.expects_operand = True
        self.pending_control_parenthesis = False


def _line_comment_end(text: str, start: int) -> int:
    """한 줄 주석 다음 줄바꿈 또는 문서 끝 위치 탐색.

    Args:
        text: JavaScript 원문.
        start: 주석 본문 시작 위치.

    Returns:
        첫 줄바꿈 위치 또는 문서 길이.
    """

    return min(
        (
            position
            for position in (text.find("\n", start), text.find("\r", start))
            if position >= 0
        ),
        default=len(text),
    )


def _consume_literal_or_comment(text: str, state: _ScanState) -> tuple[bool, bool]:
    """현재 위치의 문자열·템플릿·주석·정규식 또는 나눗셈 소비.

    Args:
        text: JavaScript 원문.
        state: 변경할 스캔 상태.

    Returns:
        token 처리 여부와 구문 유효 여부.
    """

    char = text[state.cursor]
    if char in ("'", '"'):
        end = _string_end(text, state.cursor)
        if end is None:
            return True, False
        state.consume_value(end)
        return True, True
    if char == "`":
        end = _template_end(text, state.cursor)
        if end is None:
            return True, False
        state.consume_value(end)
        return True, True
    if char != "/" or state.cursor + 1 >= len(text):
        return False, True
    following = text[state.cursor + 1]
    if following == "/":
        state.cursor = _line_comment_end(text, state.cursor + 2)
        return True, True
    if following == "*":
        end = text.find("*/", state.cursor + 2)
        if end < 0:
            return True, False
        state.cursor = end + 2
        return True, True
    end = _possible_regex_end(
        text,
        state.cursor,
        expects_operand=state.expects_operand,
    )
    if end is not None:
        state.consume_value(end)
    else:
        state.consume_operator()
    return True, True


def _consume_group(
    char: str,
    state: _ScanState,
    *,
    stop_at_outer_close: bool,
) -> tuple[bool, bool, bool]:
    """괄호 token을 소비하고 중첩·완료 상태 검증.

    Args:
        char: 현재 문자.
        state: 변경할 스캔 상태.
        stop_at_outer_close: 최외곽 닫는 괄호에서 완료할지 여부.

    Returns:
        token 처리 여부, 구문 유효 여부, 스캔 완료 여부.
    """

    pairs = {"(": ")", "[": "]", "{": "}"}
    if char in pairs:
        control_parenthesis = char == "(" and state.pending_control_parenthesis
        state.stack.append((pairs[char], control_parenthesis))
        state.consume_operator()
        return True, True, False
    if char not in ")]}":
        return False, True, False
    if not state.stack or char != state.stack[-1][0]:
        return True, False, False
    _closer, control_parenthesis = state.stack.pop()
    state.cursor += 1
    state.expects_operand = control_parenthesis
    state.pending_control_parenthesis = False
    completed = stop_at_outer_close and not state.stack
    return True, True, completed


def _consume_atom(text: str, state: _ScanState) -> bool:
    """식별자·숫자·점 token을 소비.

    Args:
        text: JavaScript 원문.
        state: 변경할 스캔 상태.

    Returns:
        token 처리 여부.
    """

    char = text[state.cursor]
    if char.isalpha() or char in "_$" or ord(char) > 127:
        end = state.cursor + 1
        while end < len(text) and (
            text[end].isalnum() or text[end] in "_$" or ord(text[end]) > 127
        ):
            end += 1
        token = text[state.cursor:end]
        state.expects_operand = token in _REGEX_PREFIX_KEYWORDS
        state.pending_control_parenthesis = token in _CONTROL_PAREN_KEYWORDS
        state.cursor = end
        return True
    if char.isdigit():
        end = state.cursor + 1
        while end < len(text) and (
            text[end].isalnum() or text[end] in "._"
        ):
            end += 1
        state.consume_value(end)
        return True
    if char != ".":
        return False
    if text.startswith("...", state.cursor):
        state.consume_operator(3)
    else:
        state.consume_value(state.cursor + 1)
    return True


def _scan_javascript(
    text: str,
    state: _ScanState,
    *,
    stop_at_outer_close: bool,
    pluses: list[int] | None = None,
) -> int | None:
    """공유 어휘 규칙으로 JavaScript 표현식 범위 스캔.

    Args:
        text: JavaScript 원문.
        state: 초기 위치와 괄호 stack을 가진 상태.
        stop_at_outer_close: 최외곽 닫는 괄호에서 종료할지 여부.
        pluses: 최상위 덧셈 위치 누적 목록.

    Returns:
        성공한 스캔의 종료 위치. 잘못된 구문이면 ``None``.
    """

    while state.cursor < len(text):
        valid, completed = _advance_javascript_token(
            text,
            state,
            stop_at_outer_close=stop_at_outer_close,
            pluses=pluses,
        )
        if not valid:
            return None
        if completed:
            return state.cursor
    return None if state.stack else state.cursor


def _advance_javascript_token(
    text: str,
    state: _ScanState,
    *,
    stop_at_outer_close: bool,
    pluses: list[int] | None,
) -> tuple[bool, bool]:
    """현재 JavaScript token 하나를 소비하고 유효·완료 상태 반환.

    Args:
        text: JavaScript 원문.
        state: 변경할 스캔 상태.
        stop_at_outer_close: 최외곽 닫는 괄호에서 종료할지 여부.
        pluses: 최상위 덧셈 위치 누적 목록.

    Returns:
        구문 유효 여부와 스캔 완료 여부.
    """

    char = text[state.cursor]
    if char.isspace():
        state.cursor += 1
        return True, False
    handled, valid = _consume_literal_or_comment(text, state)
    if handled:
        return valid, False
    handled, valid, completed = _consume_group(
        char,
        state,
        stop_at_outer_close=stop_at_outer_close,
    )
    if handled:
        return valid, completed
    if _consume_atom(text, state):
        return True, False
    if char in ",;:?=+*-!~%&|^<>":
        if char == "+" and pluses is not None and not state.stack:
            pluses.append(state.cursor)
        state.consume_operator()
        return True, False
    state.consume_value(state.cursor + 1)
    return True, False


def balanced_expression_end(text: str, start: int) -> int | None:
    """괄호와 리터럴을 고려한 JavaScript 표현식의 종료 위치."""

    pairs = {"(": ")", "[": "]", "{": "}"}
    opener = text[start]
    if opener not in pairs:
        return None
    state = _ScanState(
        cursor=start + 1,
        stack=[(pairs[opener], False)],
    )
    return _scan_javascript(text, state, stop_at_outer_close=True)


def top_level_plus_positions(text: str) -> tuple[int, ...] | None:
    """JavaScript 최상위 덧셈 연산자 위치 목록."""

    pluses: list[int] = []
    state = _ScanState(cursor=0)
    end = _scan_javascript(
        text,
        state,
        stop_at_outer_close=False,
        pluses=pluses,
    )
    if end is None:
        return None
    return tuple(pluses)
