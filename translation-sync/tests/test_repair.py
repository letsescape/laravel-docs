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

    def test_repairs_swapped_link_targets_without_touching_prose(self):
        source = (
            "Generate a [redirect HTTP response](responses#redirects) "
            "for a [named route](routing#named-routes)."
        )
        translated = """<!-- Generate a [redirect HTTP response](responses#redirects) for a [named route](routing#named-routes). -->
[redirect HTTP response](routing#named-routes)에 대한 [named route](responses#redirects)을 생성합니다.
"""

        result = repair.repair_preserved_markup(source, translated)

        self.assertTrue(result.changed)
        self.assertIn(
            "[redirect HTTP response](responses#redirects)에 대한 [named route](routing#named-routes)",
            result.text,
        )
        self.assertEqual([], verify.verify(result.text, source=source))

    def test_fails_closed_when_link_counts_do_not_match(self):
        source = "See [Routing](routing.md)."
        translated = "링크가 없습니다."

        with self.assertRaises(repair.RepairError):
            repair.repair_preserved_markup(source, translated)

    def test_skips_blockquoted_annotation_comments_before_repairing_links(self):
        source = "> [!NOTE]\n> See [Routing](routing.md).\n"
        translated = """> [!NOTE]
> <!-- See [Routing](routing.md). -->
> [라우팅](wrong.md)을 참고하세요.
"""

        result = repair.repair_preserved_markup(source, translated)

        self.assertTrue(result.changed)
        self.assertIn("> <!-- See [Routing](routing.md). -->", result.text)
        self.assertIn("[Routing](routing.md)을 참고하세요.", result.text)
        self.assertEqual([], verify.verify(result.text, source=source))

    def test_repairs_missing_anchor_before_repaired_heading_comment(self):
        source = '<a name="callouts"></a>\n## Callouts\n'
        translated = "<!-- ## Callouts -->\n## 콜아웃\n"

        result = repair.repair_preserved_markup(source, translated)

        self.assertTrue(result.changed)
        self.assertEqual(
            result.text,
            '<a name="callouts"></a>\n'
            "<!-- ## Callouts -->\n"
            "## Callouts\n",
        )
        self.assertEqual([], verify.verify(result.text, source=source))


class RestoreListMarkersTests(unittest.TestCase):
    def test_restores_dropped_list_markers_from_source(self):
        source = (
            "- [Using Eloquent](https://example.com/a/) stores models.\n"
            "- [Write queries](https://example.com/b/) with the builder.\n"
            "- The `mongodb` cache driver clears expired entries.\n"
        )
        # Model dropped the `-` markers, returning blank-separated paragraphs.
        translated = (
            "[Using Eloquent](https://example.com/a/) 모델을 저장합니다.\n"
            "\n"
            "[Write queries](https://example.com/b/) 빌더로 작성합니다.\n"
            "\n"
            "`mongodb` 캐시 드라이버는 만료 항목을 정리합니다.\n"
        )

        result = repair.restore_list_markers(source, translated)
        content = [line for line in result.splitlines() if line.strip()]

        self.assertEqual(len(content), 3)
        self.assertTrue(all(line.startswith("- ") for line in content))

    def test_leaves_already_marked_list_unchanged(self):
        source = "- a\n- b\n"
        translated = "- 가\n- 나\n"

        self.assertEqual(repair.restore_list_markers(source, translated), translated)

    def test_no_op_when_content_count_does_not_align(self):
        source = "- a\n- b\n- c\n"
        translated = "가 나 다가 한 줄로 합쳐졌습니다.\n"

        self.assertEqual(repair.restore_list_markers(source, translated), translated)

    def test_no_op_when_source_is_not_a_pure_list(self):
        source = "Intro paragraph.\n\n- a\n- b\n"
        translated = "도입 문단입니다.\n\n- 가\n- 나\n"

        self.assertEqual(repair.restore_list_markers(source, translated), translated)


if __name__ == "__main__":
    unittest.main()
