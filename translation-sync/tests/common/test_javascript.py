"""JSX 보호 구조에 사용하는 JavaScript lexical scan 검증."""

import unittest

from sync.common.javascript import (
    balanced_expression_end,
    top_level_plus_positions,
)


class BalancedExpressionTests(unittest.TestCase):
    """괄호와 JavaScript literal을 포함한 표현식 경계 검증."""

    def test_finds_balanced_expression_end(self):
        """중첩 괄호 다음의 정확한 종료 위치 반환."""

        text = "{render([first, second])} suffix"

        self.assertEqual(
            balanced_expression_end(text, 0),
            text.index(" suffix"),
        )

    def test_ignores_brackets_inside_literals_and_comments(self):
        """문자열·정규식·주석 내부 괄호 제외."""

        cases = (
            '{value === "}" ? left : right}',
            "{pattern.test(/[/}]/) ? left : right}",
            "{value /* } */ + other}",
            "{value // }\n + other}",
        )

        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(balanced_expression_end(text, 0), len(text))

    def test_follows_nested_template_expressions(self):
        """template literal 내부 표현식 경계 추적."""

        text = "{`prefix ${format({value: `nested ${item}`})} suffix`}"

        self.assertEqual(balanced_expression_end(text, 0), len(text))

    def test_rejects_unbalanced_or_non_expression_input(self):
        """닫히지 않은 표현식과 괄호가 아닌 시작 위치 거부."""

        self.assertIsNone(balanced_expression_end("{value", 0))
        self.assertIsNone(balanced_expression_end("value", 0))


class TopLevelPlusTests(unittest.TestCase):
    """JavaScript 최상위 덧셈 연산자 위치 검증."""

    def test_returns_only_top_level_plus_positions(self):
        """중첩 표현식과 literal 외부의 덧셈 연산자만 반환."""

        text = "left + render(a + b) + `x + ${c + d}` + /a+b/.source"

        self.assertEqual(
            tuple(text[index] for index in top_level_plus_positions(text) or ()),
            ("+", "+", "+"),
        )
        self.assertEqual(
            top_level_plus_positions(text),
            (5, 21, 38),
        )

    def test_rejects_unbalanced_input(self):
        """닫히지 않은 괄호나 literal 거부."""

        self.assertIsNone(top_level_plus_positions("left + (right"))
        self.assertIsNone(top_level_plus_positions("left + 'right"))


if __name__ == "__main__":
    unittest.main()
