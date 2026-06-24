import unittest

from sync import upstream


class UpstreamSyncTests(unittest.TestCase):
    def test_normalizes_trailing_whitespace_without_changing_content(self) -> None:
        source = (
            "# Title  \n"
            "\n"
            "> [!NOTE]  \n"
            "Text with internal  spaces.   \n"
            "```php\n"
            "$value = 'kept';   \n"
            "```\n"
            "\n"
            "\n"
        )

        self.assertEqual(
            upstream.normalize_markdown_source(source),
            (
                "# Title\n"
                "\n"
                "> [!NOTE]\n"
                "Text with internal  spaces.\n"
                "```php\n"
                "$value = 'kept';\n"
                "```\n"
            ),
        )

    def test_adds_single_eof_newline_when_source_has_no_newline(self) -> None:
        self.assertEqual(upstream.normalize_markdown_source("# Title"), "# Title\n")


if __name__ == "__main__":
    unittest.main()
