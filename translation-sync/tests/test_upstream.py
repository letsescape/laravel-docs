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


if __name__ == "__main__":
    unittest.main()
