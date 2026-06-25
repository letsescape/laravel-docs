import unittest

from sync import annotate, verify


class AnnotateTests(unittest.TestCase):
    def test_emits_source_comment_when_content_present_but_block_misaligned(self):
        # The translation kept the content (links intact) but lost the list
        # structure, so block alignment slips. The English comment must still be
        # emitted so verification's "missing original comment" cannot fail.
        en = (
            "- [One](https://a.test/one) first item.\n"
            "- [Two](https://a.test/two) second item.\n"
        )
        ko = (
            "<!-- placeholder. -->\n"
            "[One](https://a.test/one) 첫째 항목.\n"
            "[Two](https://a.test/two) 둘째 항목.\n"
        )
        out, _drifts = annotate.annotate(en, ko, "13.x")
        self.assertTrue(
            verify._required_comments(en).issubset(verify._translated_comments(out))  # noqa: SLF001
        )

    def test_keeps_drift_when_content_is_genuinely_untranslated(self):
        # A new paragraph with no verbatim marker is genuinely missing from the
        # translation: do NOT paper it over, so drift is still reported and the
        # incomplete document is not silently accepted.
        en = "Body text.\n\nNew untranslated paragraph.\n"
        ko = "<!-- Body text. -->\n본문입니다.\n"
        out, drifts = annotate.annotate(en, ko, "13.x")
        self.assertFalse(
            verify._required_comments(en).issubset(verify._translated_comments(out))  # noqa: SLF001
        )
        self.assertTrue(any(d.op == "delete" for d in drifts))

    def test_inserts_original_english_comments_without_rewriting_translation(self):
        en = "# Installation\n\nInstall Laravel with Composer.\n"
        ko = "# 설치 (Installation)\n\nComposer로 Laravel을 설치합니다.\n"

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertEqual(
            out,
            "<!-- # Installation -->\n"
            "# 설치 (Installation)\n\n"
            "<!-- Install Laravel with Composer. -->\n"
            "Composer로 Laravel을 설치합니다.\n",
        )

    def test_reports_drift_when_source_has_unmatched_text_block(self):
        en = "# Installation\n\nInstall Laravel with Composer.\n\nRun the server.\n"
        ko = "# 설치 (Installation)\n\nComposer로 Laravel을 설치합니다.\n"

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertIn("<!-- # Installation -->", out)
        self.assertEqual(len(drifts), 1)
        self.assertEqual(drifts[0].op, "delete")
        self.assertEqual(drifts[0].en_lines, ["Run the server."])

    def test_replaces_version_placeholder_in_inserted_comments(self):
        en = "See [Routing](/docs/{{version}}/routing)."
        ko = "[라우팅](/docs/12.x/routing)을 참고하세요."

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertIn("<!-- See [Routing](/docs/12.x/routing). -->", out)

    def test_does_not_insert_comments_for_toc_link_lists(self):
        en = "# Concurrency\n\n- [Introduction](#introduction)\n\n<a name=\"introduction\"></a>\n## Introduction\n"
        ko = "# 동시 실행 (Concurrency)\n\n- [소개](#introduction)\n\n<a name=\"introduction\"></a>\n## 소개 (Introduction)\n"

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertNotIn("<!-- - [Introduction](#introduction) -->", out)
        self.assertIn("- [소개](#introduction)", out)
        self.assertIn("<!-- ## Introduction -->", out)

    def test_preserves_trailing_blank_line_count(self):
        en = "# Example\n\nBody.\n\n"
        ko = "# 예제\n\n본문.\n\n"

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertTrue(out.endswith("\n\n"))

    def test_replaces_existing_original_comments_when_reannotating(self):
        en = "# Updated\n\nUpdated body.\n"
        ko = "<!-- # Old -->\n# 예제\n\n<!-- Old body. -->\n본문.\n"

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertNotIn("<!-- # Old -->", out)
        self.assertNotIn("<!-- Old body. -->", out)
        self.assertIn("<!-- # Updated -->", out)
        self.assertIn("<!-- Updated body. -->", out)

    def test_aligns_paragraph_after_list_without_blank_line(self):
        en = (
            "- First item.\n"
            "- Second item.\n"
            "\n"
            "Paragraph after list.\n"
        )
        ko = (
            "- 첫 번째 항목입니다.\n"
            "- 두 번째 항목입니다.\n"
            "목록 뒤 문단입니다.\n"
        )

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertIn("<!-- Paragraph after list. -->", out)

    def test_keeps_html_example_lines_in_one_original_comment(self):
        en = (
            '<button type="submit">\n'
            '    Submit\n'
            '</button>\n'
        )
        ko = (
            '<button type="submit">\n'
            '    제출\n'
            '</button>\n'
        )

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertIn(
            '<!--\n<button type="submit">\n    Submit\n</button>\n-->',
            out,
        )

    def test_keeps_blade_directive_example_lines_in_one_original_comment(self):
        en = (
            "@once\n"
            "    @push('scripts')\n"
            "        <script>\n"
            "            // Your custom JavaScript...\n"
            "        </script>\n"
            "    @endpush\n"
            "@endonce\n"
        )
        ko = en

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertIn(
            "<!--\n"
            "@once\n"
            "    @push('scripts')\n"
            "        <script>\n"
            "            // Your custom JavaScript...\n"
            "        </script>\n"
            "    @endpush\n"
            "@endonce\n"
            "-->",
            out,
        )

    def test_keeps_collection_link_list_closing_div_in_original_comment(self):
        en = (
            '<div class="collection-method-list" markdown="1">\n'
            "\n"
            "[Arr::accessible](#method-array-accessible)\n"
            "[Arr::add](#method-array-add)\n"
            "</div>\n"
        )
        ko = en

        out, drifts = annotate.annotate(en, ko, "master")

        self.assertEqual(drifts, [])
        self.assertNotIn("missing original comment", verify.verify(out, source=en))
        self.assertIn(
            "<!--\n"
            "[Arr::accessible](#method-array-accessible)\n"
            "[Arr::add](#method-array-add)\n"
            "</div>\n"
            "-->",
            out,
        )

    def test_keeps_yaml_key_and_following_list_in_one_original_comment(self):
        en = (
            "features:\n"
            "- docker: true\n"
            "- elasticsearch:\n"
            "    version: 7.9.0\n"
        )
        ko = en

        out, drifts = annotate.annotate(en, ko, "8.x")

        self.assertEqual(drifts, [])
        self.assertIn(
            "<!--\n"
            "features:\n"
            "- docker: true\n"
            "- elasticsearch:\n"
            "    version: 7.9.0\n"
            "-->",
            out,
        )

    def test_split_blocks_keeps_long_fenced_code_blocks_intact(self):
        lines = [
            "````markdown",
            "```php",
            "echo 'ok';",
            "```",
            "````",
            "Paragraph.",
        ]

        blocks = annotate.split_blocks(lines)

        self.assertEqual(blocks[0].kind, "code")
        self.assertEqual(blocks[0].lines, lines[:5])
        self.assertEqual(blocks[1].kind, "text")

    def test_strip_annotations_preserves_indented_code_comments(self):
        ko = (
            "    <!-- Equivalent to csrf_token() -->\n"
            "    {{ csrf_field() }}\n"
        )

        out = annotate.strip_annotations(ko)

        self.assertEqual(out, ko)


if __name__ == "__main__":
    unittest.main()
