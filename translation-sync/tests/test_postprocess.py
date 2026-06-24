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
        text = "# Title   \n\n```php\nreturn true;    \n```\n"

        out = postprocess.postprocess(text, "12.x", {})

        self.assertEqual(out, "# Title\n\n```php\nreturn true;\n```\n")

    def test_escapes_js_comment_closer_inside_html_comments(self):
        text = "<!-- Use `DB::raw(/* ... */)` carefully. -->\n本文です。\n"

        out = postprocess.postprocess(text, "12.x", {})

        self.assertIn("<!-- Use `DB::raw(/* ... *&#47;)` carefully. -->", out)
        self.assertNotIn("*/)` carefully. -->", out)

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


if __name__ == "__main__":
    unittest.main()
