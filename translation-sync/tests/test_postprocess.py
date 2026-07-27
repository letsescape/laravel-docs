import unittest

from sync import postprocess


class PostprocessTests(unittest.TestCase):
    def test_postprocesses_html_and_title_classes_outside_code_blocks_only(self):
        text = """# Title {.page-title}

<img src="/docs/example.png">

```blade
#### `after()` {.collection-method}
<img src="{{ $message->embed($pathToImage) }}">
```
"""

        out = postprocess.postprocess(text, "12.x", {})

        self.assertIn("# Title\n", out)
        self.assertIn('<img src="/docs/example.png"/>', out)
        self.assertIn("#### `after()` {.collection-method}", out)
        self.assertIn('<img src="{{ $message->embed($pathToImage) }}">', out)

    def test_strips_trailing_whitespace_from_final_output(self):
        text = "# Title   \nPlain text. \n```php\nreturn true;    \n```\n"

        out = postprocess.postprocess(text, "12.x", {})

        self.assertEqual(
            out,
            "# Title\nPlain text.\n```php\nreturn true;\n```\n",
        )

    def test_preserves_explicit_markdown_hard_break_outside_code(self):
        text = "First line.  \nSecond line.\n"

        out = postprocess.postprocess(text, "12.x", {})

        self.assertEqual(out, text)

    def test_preserves_quoted_markdown_hard_break_outside_code(self):
        text = "> First line.  \n> Second line.\n"

        out = postprocess.postprocess(text, "12.x", {})

        self.assertEqual(out, text)

    def test_escapes_js_comment_closer_inside_html_comments(self):
        text = "<!-- Use `DB::raw(/* ... */)` carefully. -->\n本文です。\n"

        out = postprocess.postprocess(text, "12.x", {})

        self.assertIn("<!-- Use `DB::raw(/* ... *&#47;)` carefully. -->", out)
        self.assertNotIn("*/)` carefully. -->", out)

    def test_normalizes_localized_legacy_admonitions(self):
        cases = (
            ("> **참고:**\n> 한국어 본문입니다.\n", "> [!NOTE]\n> 한국어 본문입니다.\n"),
            ("> **注意:**\n> 日本語の本文です。\n", "> [!NOTE]\n> 日本語の本文です。\n"),
            ("> **注:**\n> 日本語の本文です。\n", "> [!NOTE]\n> 日本語の本文です。\n"),
        )

        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(
                    postprocess.postprocess(text, "12.x", {}),
                    expected,
                )

    def test_normalizes_known_stale_links_without_touching_code_or_comments(self):
        text = (
            "[Agents](#agents-integration)\n"
            "[Controller](#actions-handled-by-resource-controller)\n"
            "[Table](/docs/8.x/migrations#writing-migrations)\n"
            "[Date](/docs/8.x/eloquent-mutators##date-casting)\n"
            "[Factory](/docs/8.x/database-testing#writing-factories)\n"
            "[assertSimilarJson](#assert-similar-json)\n"
            "[Shortcode](#formatting-shortcode-notifications)\n"
            "- [List Shortcode](#formatting-shortcode-notifications)\n"
            "`[Code](#agents-integration)`\n"
            "<!-- [Comment](#agents-integration) -->\n"
        )

        out = postprocess.postprocess(text, "12.x", {})

        self.assertEqual(
            out,
            "[Agents](#agent-integration)\n"
            "[Controller](#actions-handled-by-resource-controllers)\n"
            "[Table](/docs/8.x/migrations#creating-tables)\n"
            "[Date](/docs/8.x/eloquent-mutators#date-casting)\n"
            "[Factory](/docs/8.x/database-testing#defining-model-factories)\n"
            "`assertSimilarJson`\n"
            "`Shortcode`\n"
            "- List Shortcode\n"
            "`[Code](#agents-integration)`\n"
            "<!-- [Comment](#agents-integration) -->\n",
        )
        self.assertEqual(postprocess.postprocess(out, "12.x", {}), out)

    def test_uses_legacy_controller_and_fluent_string_targets_in_v8_v9(self):
        text = (
            "[Old Controller](#actions-handled-by-resource-controllers)\n"
            "[Current Controller](#actions-handled-by-resource-controller)\n"
            "[Old Strings](/docs/9.x/strings#fluent-strings)\n"
            "[Current Helpers](/docs/9.x/helpers#fluent-strings)\n"
        )

        self.assertEqual(
            postprocess.postprocess(text, "9.x", {}),
            (
                "[Old Controller](#actions-handled-by-resource-controller)\n"
                "[Current Controller](#actions-handled-by-resource-controller)\n"
                "[Old Strings](/docs/9.x/helpers#fluent-strings)\n"
                "[Current Helpers](/docs/9.x/helpers#fluent-strings)\n"
            ),
        )

    def test_uses_the_plural_agents_target_in_v13(self):
        text = (
            "[Current Agents](#agents-integration)\n"
            "[Prior Agents](#agent-integration)\n"
        )

        self.assertEqual(
            postprocess.postprocess(text, "13.x", {}),
            (
                "[Current Agents](#agents-integration)\n"
                "[Prior Agents](#agents-integration)\n"
            ),
        )

    def test_normalizes_retired_list_label_from_a_prior_run(self):
        text = (
            "    - `Formatting Shortcode Notifications`\n"
            "```md\n"
            "- `Formatting Shortcode Notifications`\n"
            "```\n"
            "<!-- - `Formatting Shortcode Notifications` -->\n"
        )

        self.assertEqual(
            postprocess.postprocess(text, "8.x", {}),
            (
                "    - Formatting Shortcode Notifications\n"
                "```md\n"
                "- `Formatting Shortcode Notifications`\n"
                "```\n"
                "<!-- - `Formatting Shortcode Notifications` -->\n"
            ),
        )

    def test_keeps_existing_gfm_admonition_body_inside_blockquote(self):
        text = """> [!NOTE]
<!-- Original note body. -->
번역된 note 본문입니다.

다음 문단입니다.
"""

        out = postprocess.postprocess(text, "12.x", {})

        self.assertEqual(
            out,
            """> [!NOTE]
> <!-- Original note body. -->
> 번역된 note 본문입니다.

다음 문단입니다.
""",
        )

    def test_keeps_fenced_code_admonition_body_inside_blockquote(self):
        text = """> [!NOTE]
```php
return true;
```

다음 문단입니다.
"""

        out = postprocess.postprocess(text, "12.x", {})

        self.assertEqual(
            out,
            """> [!NOTE]
> ```php
> return true;
> ```

다음 문단입니다.
""",
        )

    def test_keeps_literal_alerts_inside_outer_fenced_code(self):
        for marker in ("NOTE", "TIP", "WARNING", "CAUTION", "IMPORTANT"):
            with self.subTest(marker=marker):
                text = (
                    "```markdown\n"
                    f"> [!{marker}]\n"
                    "> literal alert example\n"
                    "```\n"
                )

                self.assertEqual(postprocess.postprocess(text, "12.x", {}), text)

    def test_does_not_close_outer_fence_at_an_inner_fence_with_info(self):
        text = (
            "```markdown\n"
            "```php\n"
            "> [!NOTE]\n"
            '<img src="example.png">\n'
            "```\n"
            "After.\n"
            "```\n"
        )

        self.assertEqual(postprocess.postprocess(text, "12.x", {}), text)

    def test_standardizes_bold_note_with_colon_inside_bold_text(self):
        text = "> **Note:** Keep this.\n"

        out = postprocess.postprocess(text, "12.x", {})

        self.assertEqual(out, "> [!NOTE]\n> Keep this.\n")

    def test_self_closes_img_with_greater_than_in_quoted_attribute(self):
        text = '<img src="example.png" alt="1 > 0">\n'

        out = postprocess.postprocess(text, "12.x", {})

        self.assertEqual(out, '<img src="example.png" alt="1 > 0"/>\n')

    def test_keeps_img_inside_inline_code_spans(self):
        cases = (
            'Use `<img src="inline.png">`.\n<img src="outside.png">\n',
            'Use ``<img src="inline.png">``.\n<img src="outside.png">\n',
            (
                "Use ``\n"
                '<img src="inline.png">\n'
                "end ``.\n"
                '<img src="outside.png">\n'
            ),
        )

        for text in cases:
            with self.subTest(text=text):
                out = postprocess.postprocess(text, "12.x", {})

                self.assertIn('<img src="inline.png">', out)
                self.assertNotIn('<img src="inline.png"/>', out)
                self.assertIn('<img src="outside.png"/>', out)

    def test_keeps_self_closed_img_with_greater_than_in_jsx_expression(self):
        text = "<img hidden={count > 0} />\n"

        out = postprocess.postprocess(text, "12.x", {})

        self.assertEqual(out, text)

    def test_keeps_self_closed_img_with_escaped_template_literal_content(self):
        text = '<img alt={`say \\`hi\\` } > text`} />\n'

        out = postprocess.postprocess(text, "12.x", {})

        self.assertEqual(out, text)

    def test_keeps_self_closed_img_with_complex_jsx_expression(self):
        cases = (
            '<img alt={label /* } > */ + "English"} />\n',
            '<img alt={`outer ${`inner } > English ${label}`}`} />\n',
        )

        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(
                    postprocess.postprocess(text, "12.x", {}),
                    text,
                )

    def test_keeps_long_fenced_code_blocks_unmodified(self):
        text = (
            "````blade\n"
            "```html\n"
            '<img src="{{ $message->embed($pathToImage) }}">\n'
            "```\n"
            "````\n"
        )

        out = postprocess.postprocess(text, "12.x", {})

        self.assertEqual(out, text)

    def test_replaces_version_placeholders_outside_fenced_code_only(self):
        text = (
            "Read /docs/{{version}}/cache.\n\n"
            "```text\n"
            "{{version}}\n"
            "```\n"
        )

        out = postprocess.postprocess(text, "12.x", {})

        self.assertEqual(
            out,
            "Read /docs/12.x/cache.\n\n```text\n{{version}}\n```\n",
        )

    def test_preserves_version_placeholder_in_quoted_fence(self):
        text = "> ```text\n> {{version}}\n> ```\n"

        out = postprocess.postprocess(text, "12.x", {})

        self.assertEqual(out, text)


if __name__ == "__main__":
    unittest.main()
