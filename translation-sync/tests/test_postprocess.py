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


if __name__ == "__main__":
    unittest.main()
