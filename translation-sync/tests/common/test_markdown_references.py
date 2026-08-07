"""Markdown reference 정의 파서 검증."""

import unittest

from sync.common.markdown import reference_definitions


class ReferenceDefinitionParserTests(unittest.TestCase):
    """CommonMark reference 정의의 구조와 경계 조건 검증."""

    def test_normalizes_commonmark_labels_and_preserves_definition_fields(self):
        """레이블 정규화와 대상·제목 보존."""

        definitions = reference_definitions(
            '[Cache \t DOC]: /docs/13.x/cache "Cache docs"\n'
        )

        self.assertEqual(len(definitions), 1)
        self.assertEqual(definitions[0].label, "cache doc")
        self.assertEqual(definitions[0].target, "/docs/13.x/cache")
        self.assertEqual(definitions[0].title, '"Cache docs"')

    def test_ignores_definitions_inside_fences_and_html_comments(self):
        """코드 fence와 HTML 주석 내부의 정의 제외."""

        text = """```md
[fenced]: /docs/12.x/cache "Fenced"
```

<!--
[commented]: /docs/12.x/cache "Commented"
-->

[visible]: /docs/13.x/cache "Visible"
"""

        self.assertEqual(
            [
                (definition.label, definition.target, definition.title)
                for definition in reference_definitions(text)
            ],
            [("visible", "/docs/13.x/cache", '"Visible"')],
        )

    def test_parses_container_and_multiline_commonmark_definitions(self):
        """컨테이너와 여러 줄 정의 파싱."""

        text = """> [quote]: /quote

- [list]: /list

   [multi]:
          /destination
               'the
               title'
"""

        self.assertEqual(
            [
                (definition.label, definition.target, definition.title)
                for definition in reference_definitions(text)
            ],
            [
                ("quote", "/quote", ""),
                ("list", "/list", ""),
                ("multi", "/destination", "'the\n               title'"),
            ],
        )

    def test_rejects_invalid_nested_and_overlong_reference_labels(self):
        """중첩되거나 길이 제한을 초과한 레이블 거부."""

        text = (
            "[[Acquire lock]]: /safe\n\n"
            f"[{'a' * 1000}]: /too-long\n"
        )

        self.assertEqual(reference_definitions(text), ())

    def test_does_not_treat_a_definition_as_interrupting_a_paragraph(self):
        """문단을 중단하는 정의 형태의 줄 제외."""

        text = "Paragraph text.\n[ref]: /not-a-definition\n"

        self.assertEqual(reference_definitions(text), ())

    def test_applies_commonmark_block_boundaries_to_definitions(self):
        """CommonMark 블록 경계를 벗어난 정의 제외."""

        invalid = (
            "[r]:\n> /safe\n",
            "-     [r]: /safe\n",
            "paragraph\n2. [r]: /safe\n",
            "paragraph\n01. [r]: /safe\n",
            "#not heading\n[r]: /safe\n",
            "---not hr\n[r]: /safe\n",
            "<span>x</span>\n[r]: /safe\n",
            "<script>\n[r]: /safe\n</script>\n",
            "<script>\n\n[r]: /safe\n",
            "<script>\n> [r]: /safe\n</script>\n",
            "<!--\n\n[r]: /safe\n",
            "<?pi\n\n[r]: /safe\n?>\n",
            "<![CDATA[\n\n[r]: /safe\n]]>\n",
            "<!DOCTYPE html\n\n[r]: /safe\n>\n",
            "<div>\n# heading\n[r]: /safe\n",
            "<x-widget>\n# heading\n[r]: /safe\n",
        )

        for text in invalid:
            with self.subTest(text=text):
                self.assertEqual(reference_definitions(text), ())

        definitions = reference_definitions("> [r]:\n/safe\n")
        self.assertEqual(
            [(definition.label, definition.target) for definition in definitions],
            [("r", "/safe")],
        )

    def test_accepts_an_uncapped_multiline_reference_title(self):
        """임의 길이의 여러 줄 reference 제목 허용."""

        title_lines = [
            f"title line {number}: {'x' * 40}"
            for number in range(120)
        ]
        text = '[r]: /safe "\n' + "\n".join(title_lines) + '\n"\n'

        definitions = reference_definitions(text)

        self.assertEqual(len(definitions), 1)
        self.assertEqual(definitions[0].target, "/safe")
        self.assertGreater(len(definitions[0].title), 4096)

    def test_resumes_reference_parsing_after_a_blank_terminated_html_block(self):
        """빈 줄로 끝난 HTML 블록 이후 파싱 재개."""

        text = (
            "<div>\n"
            "[inside]: /hidden\n\n"
            "[visible]: /safe\n"
        )

        self.assertEqual(
            [
                (definition.label, definition.target)
                for definition in reference_definitions(text)
            ],
            [("visible", "/safe")],
        )

    def test_resumes_reference_parsing_after_raw_html_container_exit(self):
        """raw HTML 컨테이너 종료 이후 파싱 재개."""

        cases = (
            (
                "> <div>\n"
                "# Heading\n"
                '[visible]: /safe "Visible"\n',
                [("visible", "/safe")],
            ),
            (
                "- <div>\n"
                "  [inside]: /hidden\n"
                "# Heading\n"
                '[visible]: /safe "Visible"\n',
                [("visible", "/safe")],
            ),
        )

        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(
                    [
                        (definition.label, definition.target)
                        for definition in reference_definitions(text)
                    ],
                    expected,
                )


if __name__ == "__main__":
    unittest.main()
