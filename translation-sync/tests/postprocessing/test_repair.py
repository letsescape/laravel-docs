"""보존 Markdown markup 복구 동작과 모호성 경계 검증."""

import unittest

from sync import repair, verify


class RepairPreservedMarkupTests(unittest.TestCase):
    """heading·링크·이미지·inline code·anchor 복구 테스트 모음."""

    def test_restores_only_a_blank_markdown_link_label(self):
        """빈 Markdown 링크 label에만 대응하는 원문 label을 복원."""

        source = 'See [Docs](guide.md "Guide").\n'
        translated = (
            '<!-- See [Docs](guide.md "Guide"). -->\n'
            '[](guide.md "Guide")를 참고하세요.\n'
        )

        result = repair.restore_blank_markdown_link_labels(source, translated)

        self.assertTrue(result.changed)
        self.assertIn('[Docs](guide.md "Guide")', result.text)

    def test_rejects_blank_label_repair_when_link_counts_differ(self):
        """빈 label 복구 시 원문과 번역문의 링크 수가 다르면 거부."""

        source = "See [Docs](guide.md).\n"
        translated = "링크가 없습니다.\n"

        with self.assertRaisesRegex(repair.RepairError, "different number"):
            repair.restore_blank_markdown_link_labels(source, translated)

    def test_repairs_translated_heading_and_link_label_without_touching_prose(self):
        """번역 산문을 유지하면서 heading과 링크 label을 복구."""

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

    def test_fails_closed_when_link_targets_are_reordered(self):
        """이미 보존된 링크 target의 순서가 바뀌면 fail-closed로 거부."""

        source = (
            "Generate a [redirect HTTP response](responses#redirects) "
            "for a [named route](routing#named-routes)."
        )
        translated = (
            "<!-- Generate a [redirect HTTP response](responses#redirects) "
            "for a [named route](routing#named-routes). -->\n"
            "[redirect HTTP response](routing#named-routes)에 대한 "
            "[named route](responses#redirects)을 생성합니다.\n"
        )

        with self.assertRaisesRegex(repair.RepairError, "link targets are reordered"):
            repair.repair_preserved_markup(source, translated)

    def test_repairs_complete_link_target_with_balanced_parentheses(self):
        """균형 잡힌 괄호를 포함한 전체 링크 target을 복구."""

        source_target = "https://en.wikipedia.org/wiki/Mode_(statistics)/source"
        translated_target = "https://en.wikipedia.org/wiki/Mode_(statistics)/wrong"
        source = f"See [Mode]({source_target})."
        translated = f"""<!-- See [Mode]({source_target}). -->
[Mode]({translated_target})을 참고하세요.
"""

        result = repair.repair_preserved_markup(source, translated)

        self.assertTrue(result.changed)
        self.assertIn(f"[Mode]({source_target})", result.text)
        self.assertEqual([], verify.verify(result.text, source=source))

    def test_repairs_link_with_title_without_dropping_separator(self):
        """구분자 형식을 유지하며 title이 있는 링크 복구."""

        for title in ('"Read more"', "'Read more'", "(Read more)"):
            with self.subTest(title=title):
                source = f"See [Docs](guide.md {title})."
                translated = (
                    f"<!-- See [Docs](guide.md {title}). -->\n"
                    f"[문서](wrong.md {title})를 참고하세요.\n"
                )

                result = repair.repair_preserved_markup(source, translated)

                self.assertTrue(result.changed)
                self.assertIn(f"[Docs](guide.md {title})", result.text)
                self.assertEqual([], verify.verify(result.text, source=source))

    def test_fails_closed_when_markdown_image_targets_are_reordered(self):
        """Markdown 이미지 target의 순서가 바뀌면 fail-closed로 거부."""

        source = "![Cat](cat.png)\n\n![Dog](dog.png)\n"
        translated = "![개](dog.png)\n\n![고양이](cat.png)\n"

        with self.assertRaises(repair.RepairError):
            repair.repair_preserved_markup(source, translated)

    def test_fails_closed_when_image_reordering_is_mixed_with_a_changed_target(self):
        """순서 변경과 잘못된 target이 섞인 Markdown 이미지를 거부."""

        source = "![Cat](cat.png)\n\n![Dog](dog.png)\n"
        translated = "![개](dog.png)\n\n![고양이](wrong.png)\n"

        with self.assertRaises(repair.RepairError):
            repair.repair_preserved_markup(source, translated)

    def test_repairs_a_changed_markdown_image_target(self):
        """동일 위치에서 변경된 Markdown 이미지 target·title을 복구."""

        source = '![Cat](cat.png "Cat")\n'
        translated = (
            '<!-- ![Cat](cat.png "Cat") -->\n'
            '![고양이](wrong.png "Wrong")\n'
        )

        result = repair.repair_preserved_markup(source, translated)

        self.assertTrue(result.changed)
        self.assertIn('![고양이](cat.png "Cat")', result.text)
        self.assertEqual([], verify.verify(result.text, source=source))

    def test_repairs_a_duplicated_image_target_at_the_same_occurrence(self):
        """뒤쪽 이미지에 중복된 대상을 같은 순번의 원문 대상으로 복구."""

        source = "![Cat](cat.png)\n\n![Dog](dog.png)\n"
        translated = "![고양이](cat.png)\n\n![개](cat.png)\n"

        result = repair.repair_preserved_markup(source, translated)

        self.assertTrue(result.changed)
        self.assertEqual(
            "![고양이](cat.png)\n\n![개](dog.png)\n",
            result.text,
        )

    def test_repairs_translated_inline_code_spans(self):
        """번역된 inline code 내용을 원문 token으로 복구."""

        source = "Use the `FileStorage` and `readOnly` methods."
        translated = """<!-- Use the `FileStorage` and `readOnly` methods. -->
`ファイルストレージ` と `読み取り専用` メソッドを使用します。
"""

        result = repair.repair_preserved_markup(source, translated)

        self.assertTrue(result.changed)
        self.assertIn("`FileStorage` と `readOnly`", result.text)
        self.assertEqual([], verify.verify(result.text, source=source))

    def test_wraps_raw_inline_code_text_when_backticks_are_dropped(self):
        """백틱이 누락된 고유 원문 토큰을 인라인 코드로 복구."""

        source = "Set the `purpose` option with `withProviderOptions`."
        translated = """<!-- Set the `purpose` option with `withProviderOptions`. -->
purpose オプションは withProviderOptions で設定します。
"""

        result = repair.repair_preserved_markup(source, translated)

        self.assertTrue(result.changed)
        self.assertIn("`purpose` オプションは `withProviderOptions`", result.text)
        self.assertEqual([], verify.verify(result.text, source=source))

    def test_fails_closed_when_inline_code_spans_are_reordered(self):
        """이미 보존된 inline code 순서가 바뀌면 fail-closed로 거부."""

        source = "Use `first` before `second`."
        translated = "`second`보다 먼저 `first`를 사용합니다."

        with self.assertRaisesRegex(repair.RepairError, "spans are reordered"):
            repair.repair_preserved_markup(source, translated)

    def test_fails_closed_when_raw_inline_code_match_is_ambiguous(self):
        """backtick이 누락된 원문 token의 후보가 여러 개면 fail-closed로 거부."""

        source = "Use the `cache` option."
        translated = "cache 값을 cache 설정에 사용합니다."

        with self.assertRaisesRegex(repair.RepairError, "ambiguous raw inline code"):
            repair.repair_preserved_markup(source, translated)

    def test_fails_closed_when_headings_are_reordered(self):
        """이미 보존된 heading 순서가 바뀌면 fail-closed로 거부."""

        source = "# First\n\n## Second\n"
        translated = "## Second\n\n# First\n"

        with self.assertRaisesRegex(repair.RepairError, "headings are reordered"):
            repair.repair_preserved_markup(source, translated)

    def test_fails_closed_when_link_counts_do_not_match(self):
        """원문과 번역문의 링크 수가 다르면 fail-closed로 거부."""

        source = "See [Routing](routing.md)."
        translated = "링크가 없습니다."

        with self.assertRaises(repair.RepairError):
            repair.repair_preserved_markup(source, translated)

    def test_skips_blockquoted_annotation_comments_before_repairing_links(self):
        """blockquote 안의 annotation 주석을 건너뛰고 표시 링크를 복구."""

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
        """복구한 heading의 소유 주석 앞에 누락된 named anchor를 삽입."""

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
    """순수 unordered list의 marker 복구 경계 테스트 모음."""

    def test_restores_dropped_list_markers_from_source(self):
        """항목 수가 일치하는 번역문에 누락된 원문 목록 표식을 복구."""

        source = (
            "- [Using Eloquent](https://example.com/a/) stores models.\n"
            "- [Write queries](https://example.com/b/) with the builder.\n"
            "- The `mongodb` cache driver clears expired entries.\n"
        )
        # provider가 목록 표식을 누락하고 빈 줄로 분리된 문단을 반환한 경우
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
        """이미 목록 표식이 있는 번역문을 그대로 보존."""

        source = "- a\n- b\n"
        translated = "- 가\n- 나\n"

        self.assertEqual(repair.restore_list_markers(source, translated), translated)

    def test_no_op_when_content_count_does_not_align(self):
        """원문 항목 수와 번역 내용 줄 수가 다르면 입력을 유지."""

        source = "- a\n- b\n- c\n"
        translated = "가 나 다가 한 줄로 합쳐졌습니다.\n"

        self.assertEqual(repair.restore_list_markers(source, translated), translated)

    def test_no_op_when_source_is_not_a_pure_list(self):
        """원문 블록이 순수 목록이 아니면 번역문을 유지."""

        source = "Intro paragraph.\n\n- a\n- b\n"
        translated = "도입 문단입니다.\n\n- 가\n- 나\n"

        self.assertEqual(repair.restore_list_markers(source, translated), translated)


if __name__ == "__main__":
    unittest.main()
