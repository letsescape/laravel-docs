import unittest

from sync import repair, verify


class RepairPreservedMarkupTests(unittest.TestCase):
    def test_repairs_translated_heading_and_link_label_without_touching_prose(self):
        source = "# Title\n\nSee [Routing](routing.md#basic-routing).\n"
        translated = """<!-- # Title -->
# 제목 (Title)

<!-- See [Routing](routing.md#basic-routing). -->
[라우팅](routing.md#basic-routing)을 참고하세요.
"""

        result = repair.repair_preserved_markup(source, translated)

        self.assertTrue(result.changed)
        self.assertIn("# Title", result.text)
        self.assertIn("[Routing](routing.md#basic-routing)", result.text)
        self.assertIn("참고하세요", result.text)
        self.assertEqual([], verify.verify(result.text, source=source))

    def test_fails_closed_when_link_counts_do_not_match(self):
        source = "See [Routing](routing.md)."
        translated = "링크가 없습니다."

        with self.assertRaises(repair.RepairError):
            repair.repair_preserved_markup(source, translated)


if __name__ == "__main__":
    unittest.main()
