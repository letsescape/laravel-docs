"""전처리에서 공유하는 Markdown 보호 경계 검증."""

import unittest

from sync.common.markdown import (
    _inline_code_spans,
    closes_fence,
    fence_token,
    strip_title_attr_line,
)


class MarkdownBoundaryTests(unittest.TestCase):
    """Inline code, fenced code 및 heading attribute의 경계 검증."""

    def test_finds_multiline_inline_code_with_matching_delimiter_width(self):
        """같은 길이의 backtick으로 닫힌 여러 줄 code span을 탐색."""

        text = "before ``line one\nline ` two`` after"

        self.assertEqual(
            _inline_code_spans(text),
            [(7, 30, "line one\nline ` two")],
        )

    def test_ignores_escaped_inline_code_opener(self):
        """이스케이프된 백틱을 인라인 코드의 시작으로 사용하지 않음."""

        self.assertEqual(_inline_code_spans(r"literal \`code`"), [])

    def test_tracks_blockquote_depth_in_fence_token(self):
        """blockquote 깊이를 fenced code 구분자에 포함하는지 검증."""

        self.assertEqual(fence_token("> > ```python\n"), ">>```")
        self.assertIsNone(fence_token("    ```python\n"))

    def test_requires_matching_blockquote_depth_for_closing_fence(self):
        """같은 blockquote 깊이와 충분한 길이의 fence만 종료로 판정하는지 검증."""

        self.assertTrue(closes_fence("> ````\n", ">```"))
        self.assertFalse(closes_fence("````\n", ">```"))
        self.assertFalse(closes_fence("> ```python\n", ">```"))

    def test_removes_heading_classes_while_preserving_ids(self):
        """Heading attribute에서 class만 제거하고 ID를 보존."""

        self.assertEqual(
            strip_title_attr_line("# Title {.page-title #stable}\n"),
            "# Title {#stable}\n",
        )
        self.assertEqual(
            strip_title_attr_line("# Title {#stable}\n"),
            "# Title {#stable}\n",
        )


if __name__ == "__main__":
    unittest.main()
