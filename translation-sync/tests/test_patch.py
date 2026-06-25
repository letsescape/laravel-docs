import unittest

from sync import patch


class PatchTests(unittest.TestCase):
    def test_blocks_parse_indented_multiline_comments_with_closing_content(self):
        blocks = patch._blocks(  # noqa: SLF001
            "  <!--\n"
            "First line.\n"
            "Second line. -->\n"
            "번역입니다.\n"
        )

        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].comment, "First line. Second line.")


if __name__ == "__main__":
    unittest.main()
