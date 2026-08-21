"""Page style block과 heading class 정규화 경계 검증."""

import unittest

from sync import preprocess


class PageArtifactTests(unittest.TestCase):
    """보호 영역을 제외한 page 전용 Markdown 장식 제거를 검증."""

    def test_keeps_long_fenced_code_blocks_intact(self):
        """더 긴 구분자로 감싼 fenced code 내부의 style 예시를 보존."""

        source = (
            "````markdown\n"
            "```php\n"
            "<style>.example { color: red; }</style>\n"
            "```\n"
            "````\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_keeps_quoted_fenced_style_examples_intact(self):
        """인용문 내부 fenced code의 style 예시를 보존."""

        source = (
            "> ```html\n"
            "> <style>.example { color: red; }</style>\n"
            "> ```\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_keeps_inline_style_tag_references(self):
        """inline code span에 작성된 style tag를 보존."""

        source = (
            "Pulse will include this file within a `<style>` tag so it does not "
            "need to be published.\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_keeps_style_tags_inside_multi_backtick_code_spans(self):
        """여러 backtick으로 감싼 style tag를 보존."""

        source = "Use ``<style>`` and ``</style>`` literally.\n"

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_keeps_style_blocks_inside_multiline_code_spans(self):
        """여러 줄 inline code span 내부의 style block을 보존."""

        for delimiter in ("`", "``", "```", "````"):
            with self.subTest(delimiter=delimiter):
                source = (
                    f"Use {delimiter}\n"
                    "<style>\n"
                    ".example { color: red; }\n"
                    "</style>\n"
                    f"end {delimiter} literally.\n"
                )

                result = preprocess.preprocess(source)

                self.assertEqual(result.text, source)

    def test_does_not_treat_stylesheet_as_style(self):
        """stylesheet element를 style tag로 오인하지 않음."""

        source = "<stylesheet>keep this</stylesheet>\nAfter.\n"

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_converts_indented_style_examples_to_fenced_code(self):
        """들여쓰기된 style 예시는 제거하지 않고 fenced code로 변환."""

        cases = (
            (
                "    <style>\n        .example { color: red; }\n    </style>\n",
                "```\n<style>\n    .example { color: red; }\n</style>\n```\n",
            ),
            (
                "\t<style>\n\t.example { color: red; }\n\t</style>\n",
                "```\n<style>\n.example { color: red; }\n</style>\n```\n",
            ),
        )
        for source, expected in cases:
            with self.subTest(source=source):
                result = preprocess.preprocess(source)

                self.assertEqual(result.text, expected)

    def test_removes_unindented_page_style_blocks(self):
        """일반 문서 영역의 닫힌 page style block을 제거."""

        source = "Before.\n\n<style>\n.example { color: red; }\n</style>\n\nAfter.\n"

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, "Before.\n\nAfter.\n")

    def test_preserves_unclosed_style_block_and_following_text(self):
        """닫는 tag가 없는 style block과 이후 내용을 보존."""

        source = "Before.\n\n<style>\nbody {}\nAfter should survive.\n"

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_preserves_explicit_heading_ids_while_removing_classes(self):
        """heading class만 제거하고 명시적 ID를 보존."""

        cases = (
            ("# Stable {#stable}\n", "# Stable {#stable}\n"),
            ("# Stable {.page-title #stable}\n", "# Stable {#stable}\n"),
            ("# Stable {#stable .page-title}\n", "# Stable {#stable}\n"),
        )
        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(preprocess.preprocess(source).text, expected)

    def test_preserves_html_class_attributes(self):
        """HTML element의 class 속성을 보존."""

        source = '<img class="hero" src="image.png">\n'

        self.assertEqual(preprocess.preprocess(source).text, source)

    def test_preserves_link_url_and_anchor_while_removing_heading_class(self):
        """heading class를 제거하는 동안 link URL과 anchor를 보존."""

        source = (
            "# [Title](https://example.com/docs?q=1#anchor) "
            "{.page-title #stable}\n"
        )
        expected = (
            "# [Title](https://example.com/docs?q=1#anchor) {#stable}\n"
        )

        self.assertEqual(preprocess.preprocess(source).text, expected)

    def test_preserves_heading_attributes_in_indented_code(self):
        """들여쓰기 코드 예시의 heading attribute를 보존."""

        source = "Example:\n\n    # Title {.class}\n"

        self.assertEqual(
            preprocess.preprocess(source).text,
            "Example:\n\n```\n# Title {.class}\n```\n",
        )

    def test_preserves_heading_attributes_inside_html_comments(self):
        """HTML 주석 내부의 heading attribute를 보존."""

        source = "<!--\n# Title {.class}\n-->\n"

        self.assertEqual(preprocess.preprocess(source).text, source)

    def test_preserves_heading_attributes_after_unclosed_html_comment(self):
        """닫히지 않은 HTML 주석 이후의 heading attribute를 보존."""

        source = "<!-- example\n# Title {.class}\n"

        self.assertEqual(preprocess.preprocess(source).text, source)

    def test_inline_comment_literal_does_not_hide_following_heading(self):
        """inline code의 comment literal 뒤에서 heading class를 정상적으로 제거."""

        source = "Use `<!--` literally.\n# Title {.class}\n"

        self.assertEqual(
            preprocess.preprocess(source).text,
            "Use `<!--` literally.\n# Title\n",
        )


    def test_preserves_heading_attributes_inside_a_multiline_code_span(self):
        """여러 줄 인라인 코드 범위 안의 제목 클래스를 보존하는지 검증."""

        source = "Use ``\n# Title {.class}\n`` literally.\n"

        self.assertEqual(preprocess.preprocess(source).text, source)

    def test_strips_heading_attributes_when_the_span_closes_on_the_line(self):
        """한 줄 인라인 코드가 있는 제목에서는 클래스를 계속 제거하는지 검증."""

        self.assertEqual(
            preprocess.preprocess("# Using `make:controller` {.page-title}\n").text,
            "# Using `make:controller`\n",
        )


if __name__ == "__main__":
    unittest.main()
