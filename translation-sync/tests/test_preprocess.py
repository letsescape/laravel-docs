import unittest

from sync import postprocess, preprocess, verify


class PreprocessTests(unittest.TestCase):
    def test_converts_indented_code_blocks_to_fenced_code_blocks(self):
        source = (
            "Configure the commands array:\n\n"
            "    'commands' => [\n"
            "        // App\\Console\\Commands\\ExampleCommand::class,\n"
            "    ],\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(
            result.text,
            "Configure the commands array:\n\n"
            "```\n"
            "'commands' => [\n"
            "    // App\\Console\\Commands\\ExampleCommand::class,\n"
            "],\n"
            "```\n",
        )

    def test_keeps_blank_lines_inside_indented_code_blocks(self):
        source = (
            "Example:\n\n"
            "    <?php\n"
            "\n"
            "    namespace App\\Console\\Commands;\n"
            "\n"
            "    use Illuminate\\Console\\Command;\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(
            result.text,
            "Example:\n\n"
            "```\n"
            "<?php\n"
            "\n"
            "namespace App\\Console\\Commands;\n"
            "\n"
            "use Illuminate\\Console\\Command;\n"
            "```\n",
        )

    def test_keeps_phpdoc_lines_inside_indented_code_blocks(self):
        source = (
            "Example:\n\n"
            "    class SendEmails extends Command\n"
            "    {\n"
            "        /**\n"
            "         * Execute the console command.\n"
            "         */\n"
            "        public function handle(): void\n"
            "        {\n"
            "            // ...\n"
            "        }\n"
            "    }\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(
            result.text,
            "Example:\n\n"
            "```\n"
            "class SendEmails extends Command\n"
            "{\n"
            "    /**\n"
            "     * Execute the console command.\n"
            "     */\n"
            "    public function handle(): void\n"
            "    {\n"
            "        // ...\n"
            "    }\n"
            "}\n"
            "```\n",
        )

    def test_does_not_convert_indented_nested_lists_to_code_blocks(self):
        source = (
            "- First item\n"
            "    - Nested item\n"
            "    - Another nested item\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_keeps_long_fenced_code_blocks_intact(self):
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
        source = (
            "> ```html\n"
            "> <style>.example { color: red; }</style>\n"
            "> ```\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_keeps_inline_style_tag_references(self):
        source = (
            "Pulse will include this file within a `<style>` tag so it does not "
            "need to be published.\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_keeps_style_tags_inside_multi_backtick_code_spans(self):
        source = "Use ``<style>`` and ``</style>`` literally.\n"

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_keeps_style_blocks_inside_multiline_code_spans(self):
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
        source = "<stylesheet>keep this</stylesheet>\nAfter.\n"

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_converts_indented_style_examples_to_fenced_code(self):
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
        source = "Before.\n\n<style>\n.example { color: red; }\n</style>\n\nAfter.\n"

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, "Before.\n\nAfter.\n")

    def test_preserves_unclosed_style_block_and_following_text(self):
        source = "Before.\n\n<style>\nbody {}\nAfter should survive.\n"

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_preserves_explicit_heading_ids_while_removing_classes(self):
        cases = (
            ("# Stable {#stable}\n", "# Stable {#stable}\n"),
            ("# Stable {.page-title #stable}\n", "# Stable {#stable}\n"),
            ("# Stable {#stable .page-title}\n", "# Stable {#stable}\n"),
        )
        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(preprocess.preprocess(source).text, expected)

    def test_avoids_colliding_with_literal_base64_placeholder_text(self):
        source = (
            "Literal __BASE64_IMAGE_001__.\n\n"
            "![x](data:image/png;base64,QUJD)\n"
        )

        result = preprocess.preprocess(source)

        self.assertIn("__BASE64_IMAGE_002__", result.text)
        self.assertEqual(
            postprocess.postprocess(result.text, "12.x", result.placeholders),
            source,
        )

    def test_round_trips_base64_image_with_media_type_parameters(self):
        source = "![x](data:image/svg+xml;charset=utf-8;base64,QUJD)\n"

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, "![x](__BASE64_IMAGE_001__)\n")
        self.assertEqual(
            postprocess.postprocess(result.text, "12.x", result.placeholders),
            source,
        )

    def test_round_trips_base64_images_terminated_by_angle_brackets(self):
        cases = (
            (
                "![x](<data:image/png;base64,QUJD>)\n",
                "![x](<__BASE64_IMAGE_001__>)\n",
                "![x](<data:image/png;base64,QUJD>)\n",
            ),
            (
                "<img src=data:image/png;base64,QUJD>\n",
                "<img src=__BASE64_IMAGE_001__>\n",
                "<img src=data:image/png;base64,QUJD />\n",
            ),
        )
        for source, expected_preprocessed, expected_final in cases:
            with self.subTest(source=source):
                result = preprocess.preprocess(source)

                self.assertEqual(result.text, expected_preprocessed)
                self.assertEqual(
                    postprocess.postprocess(
                        result.text, "12.x", result.placeholders
                    ),
                    expected_final,
                )

    def test_unquoted_base64_image_round_trip_passes_final_verification(self):
        source = "<img src=data:image/png;base64,QUJD>\n"

        result = preprocess.preprocess(source)
        final = postprocess.postprocess(
            result.text,
            "12.x",
            result.placeholders,
        )

        self.assertEqual(verify.verify(final, source=source), [])

    def test_preserves_unquoted_self_closing_base64_image(self):
        source = "<img src=data:image/png;base64,QQ==/>\n"

        result = preprocess.preprocess(source)
        final = postprocess.postprocess(
            result.text,
            "12.x",
            result.placeholders,
        )

        self.assertEqual(
            result.text,
            "<img src=__BASE64_IMAGE_001__/>\n",
        )
        self.assertEqual(final, source)
        self.assertEqual(verify.verify(final, source=source), [])

    def test_round_trips_base64_image_at_end_of_input(self):
        source = "data:image/png;base64,QUJD"

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, "__BASE64_IMAGE_001__")
        self.assertEqual(
            postprocess.postprocess(result.text, "12.x", result.placeholders),
            source,
        )

    def test_keeps_indented_children_with_unindented_directive_parent(self):
        source = (
            "@once\n"
            "    @push('scripts')\n"
            "        <script>\n"
            "            // ...\n"
            "        </script>\n"
            "    @endpush\n"
            "@endonce\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_keeps_indented_yaml_children_with_list_parent(self):
        source = (
            "features:\n"
            "- elasticsearch:\n"
            "    version: 7.9.0\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_keeps_code_looking_list_continuations_indented(self):
        cases = (
            "- Configure the worker\n"
            "    Run php artisan queue:work in the project.\n",
            "1. Configure the worker\n\n"
            "    APP_ENV=local\n",
        )
        for source in cases:
            with self.subTest(source=source):
                self.assertEqual(preprocess.preprocess(source).text, source)

    def test_keeps_parenthesized_ordered_list_continuations_indented(self):
        source = "1) Configure the worker\n\n    APP_ENV=local\n"

        self.assertEqual(preprocess.preprocess(source).text, source)

    def test_converts_indented_literal_fence_as_code_content(self):
        source = "Example:\n\n    echo one;\n    ```\n    echo two;\n"

        self.assertEqual(
            preprocess.preprocess(source).text,
            "Example:\n\n````\necho one;\n```\necho two;\n````\n",
        )

    def test_preserves_heading_attributes_in_indented_code(self):
        source = "Example:\n\n    # Title {.class}\n"

        self.assertEqual(
            preprocess.preprocess(source).text,
            "Example:\n\n```\n# Title {.class}\n```\n",
        )

    def test_preserves_heading_attributes_inside_html_comments(self):
        source = "<!--\n# Title {.class}\n-->\n"

        self.assertEqual(preprocess.preprocess(source).text, source)

    def test_preserves_heading_attributes_after_unclosed_html_comment(self):
        source = "<!-- example\n# Title {.class}\n"

        self.assertEqual(preprocess.preprocess(source).text, source)

    def test_inline_comment_literal_does_not_hide_following_heading(self):
        source = "Use `<!--` literally.\n# Title {.class}\n"

        self.assertEqual(
            preprocess.preprocess(source).text,
            "Use `<!--` literally.\n# Title\n",
        )


if __name__ == "__main__":
    unittest.main()
