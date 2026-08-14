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

    def test_restores_a_translated_label_for_a_unique_target(self):
        """target이 고유한 링크의 번역된 label을 원문 label로 복원."""

        source = "Use the same [file classes](#attachments) as before.\n"
        translated = (
            "<!-- Use the same [file classes](#attachments) as before. -->\n"
            "이전과 동일한 [파일 클래스](#attachments)를 사용합니다.\n"
        )

        result = repair.restore_translated_link_labels(source, translated)

        self.assertTrue(result.changed)
        self.assertIn("[file classes](#attachments)", result.text.splitlines()[1])

    def test_keeps_translated_labels_for_ambiguous_targets(self):
        """같은 target이 서로 다른 원문 label로 등장하면 복원하지 않음."""

        source = "See [first](#x) and [second](#x).\n"
        translated = (
            "<!-- See [first](#x) and [second](#x). -->\n"
            "[첫째](#x)와 [둘째](#x)를 보세요.\n"
        )

        result = repair.restore_translated_link_labels(source, translated)

        self.assertFalse(result.changed)

    def test_removes_a_blank_line_between_annotation_and_body(self):
        """annotation 주석과 소유 본문 사이의 빈 줄을 제거."""

        source = "**Supported providers:** Anthropic, Gemini\n"
        translated = (
            "<!-- **Supported providers:** Anthropic, Gemini -->\n"
            "\n"
            "**サポートされているプロバイダ:** Anthropic, Gemini\n"
        )

        result = repair.remove_blank_lines_after_annotations(source, translated)

        self.assertTrue(result.changed)
        self.assertEqual(
            result.text,
            "<!-- **Supported providers:** Anthropic, Gemini -->\n"
            "**サポートされているプロバイダ:** Anthropic, Gemini\n",
        )

    def test_keeps_blank_lines_when_source_has_html_comments(self):
        """source-authored 주석이 있으면 빈 줄을 제거하지 않음."""

        source = "<!-- keep this -->\n\nA paragraph.\n"
        translated = "<!-- keep this -->\n\n<!-- A paragraph. -->\n문단입니다.\n"

        result = repair.remove_blank_lines_after_annotations(source, translated)

        self.assertFalse(result.changed)

    def test_collapses_a_multiline_annotation_comment(self):
        """여러 줄로 갈라진 annotation 주석을 한 줄로 접기."""

        source = "| Package | Versions |\n| --- | --- |\n| Laravel | 13.x |\n"
        translated = (
            "<!-- | Package | Versions |\n"
            "| --- | --- |\n"
            "| Laravel | 13.x | -->\n"
            "| 패키지 | 버전 |\n| --- | --- |\n| Laravel | 13.x |\n"
        )

        result = repair.collapse_multiline_annotations(source, translated)

        self.assertTrue(result.changed)
        self.assertTrue(
            result.text.startswith(
                "<!-- | Package | Versions | | --- | --- | | Laravel | 13.x | -->\n"
            )
        )

    def test_keeps_multiline_comments_when_source_has_html_comments(self):
        """source-authored 주석이 있으면 여러 줄 주석을 접지 않음."""

        source = "<!-- keep\nthis -->\nA paragraph.\n"
        translated = "<!-- keep\nthis -->\n<!-- A paragraph. -->\n문단입니다.\n"

        result = repair.collapse_multiline_annotations(source, translated)

        self.assertFalse(result.changed)

    def test_normalizes_japanese_inline_code_spacing(self):
        """일본어 inline code와 CJK 경계에 반각 공백 하나를 보장."""

        result = repair.normalize_cjk_code_spacing(
            "キューに`Bus::dispatch`を渡し、`dispatch`ヘルパも使います。\n"
        )

        self.assertTrue(result.changed)
        self.assertEqual(
            result.text,
            "キューに `Bus::dispatch` を渡し、`dispatch` ヘルパも使います。\n",
        )

    def test_keeps_spacing_that_already_matches_or_uses_punctuation(self):
        """이미 공백이거나 CJK 구두점이 인접한 경계는 유지."""

        for text in (
            "`dispatch` ヘルパ関数を使用します。\n",
            "`dispatch`。次の行です。\n",
            "`key`를 설정합니다.\n",
            "```php\n$x = `a`あ;\n```\n",
        ):
            with self.subTest(text=text):
                self.assertFalse(
                    repair.normalize_cjk_code_spacing(text).changed
                )

    def test_restores_a_missing_anchor_line_before_its_heading(self):
        """누락된 앵커 줄을 heading의 annotation 앞에 복원."""

        source = (
            '<a name="laravel-blade"></a>\n'
            "##### `Pint/laravel_blade`\n"
            "\n"
            "This rule formats your Blade templates.\n"
        )
        translated = (
            "<!-- ##### `Pint/laravel_blade` -->\n"
            "##### `Pint/laravel_blade`\n"
            "\n"
            "<!-- This rule formats your Blade templates. -->\n"
            "이 규칙은 Blade 템플릿을 포맷합니다.\n"
        )

        result = repair.restore_missing_anchor_lines(source, translated)

        self.assertTrue(result.changed)
        self.assertTrue(
            result.text.startswith(
                '<a name="laravel-blade"></a>\n'
                "<!-- ##### `Pint/laravel_blade` -->\n"
            )
        )

    def test_keeps_output_when_anchor_follower_is_ambiguous(self):
        """앵커 다음 줄이 응답에 유일하지 않으면 복원하지 않음."""

        source = '<a name="x"></a>\n## Title\n'
        translated = "## Title\n\n## Title\n"

        result = repair.restore_missing_anchor_lines(source, translated)

        self.assertFalse(result.changed)

    def test_merges_split_html_annotations(self):
        """HTML 연속 라인의 행별 annotation 주석을 하나로 병합."""

        source = (
            "<tr><td><strong>Command</strong></td><td><code>php</code></td></tr>\n"
            "<tr><td><strong>Args</strong></td><td><code>boost:mcp</code></td></tr>\n"
        )
        translated = (
            "<!-- <tr><td><strong>Command</strong></td><td><code>php</code></td></tr> -->\n"
            "<tr><td><strong>명령어</strong></td><td><code>php</code></td></tr>\n"
            "<!-- <tr><td><strong>Args</strong></td><td><code>boost:mcp</code></td></tr> -->\n"
            "<tr><td><strong>인수</strong></td><td><code>boost:mcp</code></td></tr>\n"
        )

        result = repair.merge_split_html_annotations(source, translated)

        self.assertTrue(result.changed)
        self.assertEqual(
            result.text,
            "<!-- <tr><td><strong>Command</strong></td><td><code>php</code></td></tr>"
            " <tr><td><strong>Args</strong></td><td><code>boost:mcp</code></td></tr> -->\n"
            "<tr><td><strong>명령어</strong></td><td><code>php</code></td></tr>\n"
            "<tr><td><strong>인수</strong></td><td><code>boost:mcp</code></td></tr>\n",
        )

    def test_keeps_annotations_for_separate_prose_blocks(self):
        """빈 줄로 나뉜 별도 블록의 주석은 병합하지 않음."""

        source = "First paragraph.\n\nSecond paragraph.\n"
        translated = (
            "<!-- First paragraph. -->\n"
            "첫 문단입니다.\n"
            "\n"
            "<!-- Second paragraph. -->\n"
            "둘째 문단입니다.\n"
        )

        result = repair.merge_split_html_annotations(source, translated)

        self.assertFalse(result.changed)

    def test_strips_invented_inline_code_spans(self):
        """원문에 없는 내용의 inline code span에서 backtick을 제거."""

        source = 'The "help" screen describes the `help` command.\n'
        translated = (
            '<!-- The "help" screen describes the `help` command. -->\n'
            '`"help"` 화면은 `help` 명령어를 설명합니다.\n'
        )

        result = repair.strip_invented_inline_code(source, translated)

        self.assertTrue(result.changed)
        self.assertIn('"help" 화면은 `help` 명령어', result.text)

    def test_keeps_fabricated_inline_code_for_the_contract_to_reject(self):
        """원문에 없는 내용의 code span은 되돌리지 않고 계약 판정에 맡김."""

        source = "Install the package before continuing.\n"
        translated = (
            "<!-- Install the package before continuing. -->\n"
            "계속하기 전에 `artisan fabricate` 패키지를 설치합니다.\n"
        )

        result = repair.strip_invented_inline_code(source, translated)

        self.assertFalse(result.changed)
        self.assertIn("`artisan fabricate`", result.text)

    def test_does_not_fold_a_fenced_block_into_an_annotation(self):
        """닫히지 않은 주석이 코드 펜스를 삼키지 않음."""

        source = "A paragraph.\n\n```php\n$x = 1;\n```\n"
        translated = "<!-- A paragraph.\n문단입니다.\n\n```php\n$x = 1;\n```\n"

        result = repair.collapse_multiline_annotations(source, translated)

        self.assertFalse(result.changed)
        self.assertEqual(result.text.count("```"), 2)

    def test_refuses_to_merge_annotations_that_do_not_cover_the_source(self):
        """병합 결과가 요청 source 전체와 다르면 병합하지 않음."""

        source = (
            "<tr><td>A</td></tr>\n<tr><td>B</td></tr>\n<tr><td>C</td></tr>\n"
        )
        translated = (
            "<!-- <tr><td>A</td></tr> -->\n<tr><td>가</td></tr>\n"
            "<!-- <tr><td>B</td></tr> -->\n<tr><td>나</td></tr>\n"
        )

        result = repair.merge_split_html_annotations(source, translated)

        self.assertFalse(result.changed)

    def test_keeps_inline_code_inside_headings(self):
        """heading 안의 inline code span은 invented로 판정하지 않음."""

        source = "##### `Pint/laravel_blade`\n\nThis rule formats templates.\n"
        translated = (
            "<!-- ##### `Pint/laravel_blade` -->\n"
            "##### `Pint/laravel_blade`\n"
            "\n"
            "<!-- This rule formats templates. -->\n"
            "이 규칙은 템플릿을 포맷합니다.\n"
        )

        result = repair.strip_invented_inline_code(source, translated)

        self.assertFalse(result.changed)

    def test_strips_repeated_inline_code_spans_beyond_source_count(self):
        """원문 빈도를 초과한 반복 span은 뒤쪽 등장부터 복원."""

        source = "Set the `key` option once.\n"
        translated = (
            "<!-- Set the `key` option once. -->\n"
            "`key` 옵션을 설정합니다. `key`는 한 번만 지정합니다.\n"
        )

        result = repair.strip_invented_inline_code(source, translated)

        self.assertTrue(result.changed)
        self.assertIn(
            "`key` 옵션을 설정합니다. key는 한 번만 지정합니다.",
            result.text,
        )

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
