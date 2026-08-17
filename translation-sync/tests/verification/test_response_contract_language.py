"""응답 계약의 언어 판정 동작과 경계 조건 검증."""

import unittest

from sync import response_contract


class ResponseContractLanguageTests(unittest.TestCase):
    """로캘별 응답의 언어 판정 경계 테스트 모음."""

    def test_feedback_retry_is_limited_to_the_supported_completed_shapes(self):
        """교정 재요청을 복구 가능한 완료 응답 형태로 제한."""

        source = "Use [Docs](docs) before updating the shared cache value.\n"
        link_mismatch = (
            "<!-- Use [Docs](docs) before updating the shared cache value. -->\n"
            "[Wrong](wrong)를 사용해 공유 캐시 값을 갱신합니다.\n"
        )
        wrong_language = (
            "<!-- Use [Docs](docs) before updating the shared cache value. -->\n"
            "Use [Docs](docs) before updating the shared cache value.\n"
        )
        annotation_only = (
            "<!-- Use [Docs](docs) before updating the shared cache value. -->\n"
        )

        link_issues = response_contract.verify(
            link_mismatch,
            source,
            locale="ko",
        )
        language_issues = response_contract.verify(
            wrong_language,
            source,
            locale="ko",
        )
        annotation_issues = response_contract.verify(
            annotation_only,
            source,
            locale="ko",
        )

        self.assertTrue(
            response_contract.supports_feedback_retry(
                link_mismatch,
                source,
                link_issues,
            )
        )
        self.assertTrue(
            response_contract.supports_feedback_retry(
                wrong_language,
                source,
                language_issues,
            )
        )
        self.assertTrue(
            response_contract.supports_feedback_retry(
                annotation_only,
                source,
                annotation_issues,
            )
        )
        self.assertFalse(
            response_contract.supports_feedback_retry(
                link_mismatch,
                source,
                ["provider code block mismatch"],
            )
        )

    def test_accepts_a_pipe_table_owner_with_or_without_annotation(self):
        """GFM 표 전체는 canonical 소유 주석 유무 모두 허용."""

        source = """| Name | Detail |
| --- | --- |
| Widget | Safe work |
"""
        translated_table = """| 이름 | 설명 |
| --- | --- |
| Widget | 안전 작업 |
"""
        annotation = (
            "<!-- | Name | Detail | | --- | --- | | Widget | Safe work | -->\n"
        )

        omitted = response_contract.verify(
            translated_table,
            source,
            locale="ko",
        )
        annotated = response_contract.verify(
            annotation + translated_table,
            source,
            locale="ko",
        )

        self.assertEqual(omitted, [])
        self.assertEqual(annotated, [])

    def test_requires_one_canonical_annotation_for_a_legacy_pipe_table_owner(self):
        """기존 표 전체에 canonical 소유 주석을 하나만 요구."""

        source = """Name | Detail
--- | ---
Widget | Safe work
"""
        translated = """<!-- Name | Detail --- | --- Widget | Safe work -->
이름 | 설명
--- | ---
Widget | 안전 작업
"""

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_row_annotation_is_optional_for_bare_row_requests(self):
        """구분자 없는 표 행 요청은 행 annotation 생략을 허용."""

        row = "| Embeddings | OpenAI, Gemini, Azure, Bedrock, Cohere |"
        translated = "| 임베딩 | OpenAI, Gemini, Azure, Bedrock, Cohere |\n"

        self.assertEqual(
            response_contract.verify(translated, row + "\n", locale="ko"),
            [],
        )

    def test_table_annotation_is_optional_for_whole_table_requests(self):
        """구분자를 포함한 표 전체 요청도 annotation 생략을 허용."""

        source = (
            "| Feature | Providers |\n"
            "|---|---|\n"
            "| Text | OpenAI, Anthropic, Gemini |\n"
            "| Images | OpenAI, Gemini, xAI |\n"
        )
        translated = (
            "| 기능 | 프로바이더 |\n"
            "|---|---|\n"
            "| 텍스트 | OpenAI, Anthropic, Gemini |\n"
            "| 이미지 | OpenAI, Gemini, xAI |\n"
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_table_and_prose_requests_still_require_annotations(self):
        """표와 문단이 섞인 요청은 annotation을 계속 요구."""

        source = (
            "The following table lists supported providers.\n"
            "\n"
            "| Feature | Providers |\n"
            "|---|---|\n"
            "| Text | OpenAI, Anthropic, Gemini |\n"
        )
        translated = (
            "다음 표는 지원되는 프로바이더를 정리한 것입니다.\n"
            "\n"
            "| 기능 | 프로바이더 |\n"
            "|---|---|\n"
            "| 텍스트 | OpenAI, Anthropic, Gemini |\n"
        )

        self.assertIn(
            "provider original comment mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_reports_mismatched_required_comments_for_feedback(self):
        """어긋난 required 주석 원문을 feedback용으로 보고."""

        source = "Use the cache lock before updating the shared value.\n"
        translated = (
            "<!-- Use the cache lock before updating shared values. -->\n"
            "공유 값을 갱신하기 전에 캐시 락을 사용합니다.\n"
        )

        self.assertEqual(
            response_contract.mismatched_required_comments(translated, source),
            ["Use the cache lock before updating the shared value."],
        )

    def test_identifier_only_paragraphs_may_echo_the_source(self):
        """기술 식별자로만 구성된 문단은 원문 echo를 허용."""

        source = "**whereLike / orWhereLike / whereNotLike / orWhereNotLike**\n"
        translated = (
            "<!-- **whereLike / orWhereLike / whereNotLike / orWhereNotLike** -->\n"
            "**whereLike / orWhereLike / whereNotLike / orWhereNotLike**\n"
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ja"),
            [],
        )

    def test_allows_absorbed_emphasis_but_rejects_invented_emphasis(self):
        """강조를 어휘로 흡수한 누락은 허용하고 임의 추가는 거부."""

        source = "Retrieve all posts that **don't** have any comments.\n"
        absorbed = (
            "<!-- Retrieve all posts that **don't** have any comments. -->\n"
            "댓글이 하나도 없는 모든 게시물을 조회합니다.\n"
        )
        invented = (
            "<!-- Retrieve all posts that **don't** have any comments. -->\n"
            "댓글이 **하나도** 없는 **모든** 게시물을 조회합니다.\n"
        )

        self.assertEqual(
            response_contract.verify(absorbed, source, locale="ko"),
            [],
        )
        self.assertIn(
            "provider inline markup mismatch",
            response_contract.verify(invented, source, locale="ko"),
        )

    def test_definition_list_labels_are_excluded_from_the_script_floor(self):
        """정의 목록 label을 하한 계산에서 제외하고 본문만 판정."""

        source = (
            "- Amazon SQS: `aws/aws-sdk-php ~3.0`\n"
            "- Beanstalkd: `pda/pheanstalk ~5.0`\n"
            "- Redis: `predis/predis ~3.0` or phpredis PHP extension\n"
        )
        annotation = (
            "<!-- - Amazon SQS: `aws/aws-sdk-php ~3.0`"
            " - Beanstalkd: `pda/pheanstalk ~5.0`"
            " - Redis: `predis/predis ~3.0` or phpredis PHP extension -->\n"
        )
        translated = source.replace(
            "or phpredis PHP extension",
            "또는 phpredis PHP 확장",
        )

        self.assertEqual(
            response_contract.verify(annotation + translated, source, locale="ko"),
            [],
        )
        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(annotation + source, source, locale="ko"),
        )

    def test_admonition_markers_are_excluded_from_the_script_floor(self):
        """GFM admonition marker는 하한 계산 표본에서 제외."""

        source = (
            "> [!WARNING]\n"
            "> Laravel Pail requires the [PCNTL](https://php.net/pcntl) PHP"
            " extension.\n"
        )
        translated = (
            "> [!WARNING]\n"
            "> Laravel Pail은 [PCNTL](https://php.net/pcntl) PHP 확장이"
            " 필요합니다.\n"
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )
        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(source, source, locale="ko"),
        )

    def test_prose_paragraphs_still_require_the_script_floor(self):
        """일반 산문은 하한을 계속 요구."""

        body = (
            "The cache configuration file determines which store your "
            "application uses by default"
        )
        source = f"{body}\n"
        translated = f"<!-- {body} -->\n{body} 그리고 캐시\n"

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_sidebar_category_lists_do_not_require_target_script(self):
        """사이드바 카테고리 label과 링크 목록에 목표 문자를 요구하지 않음."""

        source = (
            "- ## Getting Started\n"
            "    - [Installation](/docs/13.x/installation)\n"
            "    - [Configuration](/docs/13.x/configuration)\n"
        )
        translated = (
            "<!-- - ## Getting Started - [Installation](/docs/13.x/installation)"
            " - [Configuration](/docs/13.x/configuration) -->\n" + source
        )

        self.assertEqual(
            response_contract.verify(translated, source, locale="ko"),
            [],
        )

    def test_allows_link_reordering_for_target_word_order(self):
        """목표 언어 어순에 따른 링크 등장 순서 재배열을 허용."""

        source = (
            "Search through [files](#files) stored in "
            "[vector stores](#vector-stores).\n"
        )
        reordered = (
            "<!-- Search through [files](#files) stored in "
            "[vector stores](#vector-stores). -->\n"
            "[vector stores](#vector-stores)에 저장된 [files](#files)를 "
            "검색합니다.\n"
        )
        crossed = (
            "<!-- Search through [files](#files) stored in "
            "[vector stores](#vector-stores). -->\n"
            "[vector stores](#files)에 저장된 [files](#vector-stores)를 "
            "검색합니다.\n"
        )

        self.assertEqual(
            response_contract.verify(reordered, source, locale="ko"),
            [],
        )
        self.assertIn(
            "provider link pair mismatch",
            response_contract.verify(crossed, source, locale="ko"),
        )

    def test_proper_noun_table_rows_do_not_require_target_script(self):
        """고유명사 셀만 가진 표 행 응답에 목표 문자를 요구하지 않음."""

        row = (
            "| Embeddings | OpenAI, OpenAI-Compatible, Gemini, Azure, "
            "Bedrock, Cohere, Mistral, Jina, VoyageAI, Ollama, OpenRouter |"
        )
        source = f"{row}\n"
        translated = f"<!-- {row} -->\n{row}\n"

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_rejects_swapped_targets_for_repeated_inline_link_labels(self):
        """label이 같은 반복 inline link의 target 교환을 거부."""

        source = "Use [Cache](cache) before [Cache](routing).\n"
        translated = (
            "<!-- Use [Cache](cache) before [Cache](routing). -->\n"
            "Use [Cache](routing) before [Cache](cache).\n"
        )

        issues = response_contract.verify(translated, source, locale=None)

        self.assertIn("provider link pair mismatch", issues)

    def test_hash_prefixed_prose_is_not_treated_as_an_atx_heading(self):
        """공백 없는 hash prefix 산문을 ATX heading에서 제외."""

        for source_body in (
            "#hashtag describes an ordinary paragraph with sufficient source prose.",
            "####### this is prose because ATX headings have at most six markers.",
        ):
            with self.subTest(source_body=source_body):
                translated = (
                    f"<!-- {source_body} -->\n"
                    "이 문장은 제목이 아닌 일반 문단으로 번역되었습니다.\n"
                )

                self.assertEqual(
                    response_contract.verify(
                        translated,
                        source_body + "\n",
                        locale="ko",
                    ),
                    [],
                )

    def test_does_not_require_target_script_below_exact_copy_threshold(self):
        """exact-copy 최소 길이 미만에는 대상 문자 체계를 요구하지 않음."""

        source = "abcdefghi jklmnopqrs\n"
        translated = """<!-- abcdefghi jklmnopqrs -->
abcdefghi jklmnopqrs
"""

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_accepts_hangul_jamo_as_korean_target_script(self):
        """한글 자모를 한국어 대상 문자로 인정."""

        source_body = "α" * 40
        source = f"{source_body}\n"
        translated = f"""<!-- {source_body} -->
ㄱㄴㄷㄹㅁㅂㅅㅇ
"""

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_accepts_han_without_kana_as_japanese_target_script(self):
        """가나 없는 한자를 일본어 대상 문자로 인정."""

        source = """| Feature Name | Detailed Description |
| --- | --- |
| Cache Lock | Prevent Concurrent Writes |
"""
        translated = """| 機能名称 | 詳細説明 |
| --- | --- |
| Cache Lock | 同時書込防止 |
"""

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ja"),
        )

    def test_exact_copy_comparison_preserves_internal_whitespace(self):
        """exact-copy 비교에서 내부 공백 차이 보존."""

        source = "abcdefghij  klmnopqrst\n"
        translated = """<!-- abcdefghij klmnopqrst -->
abcdefghij klmnopqrst
"""

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_accepts_supplementary_han_as_japanese_target_script(self):
        """보충 평면 한자를 일본어 대상 문자로 인정."""

        source_body = "β" * 40
        source = f"{source_body}\n"
        translated = f"""<!-- {source_body} -->
{"𠀀" * 8}
"""

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ja"),
        )

    def test_excludes_front_matter_from_target_language_check(self):
        """목표 언어 판정에서 머리말 제외."""

        source = """---
title: Cache Locks
description: Configure distributed cache locks before serving requests.
---
"""

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(source, source, locale="ko"),
        )

    def test_counts_unicode_letters_in_table_prose_cells(self):
        """표 산문 셀의 Unicode Letter 수를 반영."""

        source_body = "γ" * 40
        source = f"""| {source_body} |
| --- |
"""
        translated = f"""| {"가" * 3} |
| --- |
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_does_not_treat_product_like_general_prose_as_protected(self):
        """제품명처럼 보이는 일반 산문을 보호 데이터로 오인하지 않음."""

        source = "LaravelFrameworkPackage\n"
        translated = """<!-- LaravelFrameworkPackage -->
LaravelFrameworkPackage
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_always_treats_table_headers_as_prose(self):
        """표 header를 항상 번역 가능한 산문으로 판정."""

        source = """| LaravelFrameworkPackage |
| --- |
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(source, source, locale="ko"),
        )

    def test_exact_copy_comparison_uses_nfc(self):
        """exact-copy 비교에 NFC 정규화 적용."""

        source_body = "é" * 20
        translated_body = "e\u0301" * 20
        source = f"{source_body}\n"
        translated = f"""<!-- {source_body} -->
{translated_body}
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_requires_minimum_target_characters_at_forty_source_letters(self):
        """원문 Letter 40자에서 대상 문자 최소 8자 요구."""

        source_body = "δ" * 40
        source = f"{source_body}\n"

        for target_count, expected in ((7, True), (8, False)):
            with self.subTest(target_count=target_count):
                translated = f"""<!-- {source_body} -->
{"가" * target_count}
"""
                issues = response_contract.verify(
                    translated, source, locale="ko"
                )
                assertion = self.assertIn if expected else self.assertNotIn
                assertion("provider target language mismatch", issues)

    def test_rounds_ten_percent_requirement_up(self):
        """대상 문자 10% 하한을 올림 계산."""

        source_body = "ε" * 81
        source = f"{source_body}\n"

        for target_count, expected in ((8, True), (9, False)):
            with self.subTest(target_count=target_count):
                translated = f"""<!-- {source_body} -->
{"가" * target_count}
"""
                issues = response_contract.verify(
                    translated, source, locale="ko"
                )
                assertion = self.assertIn if expected else self.assertNotIn
                assertion("provider target language mismatch", issues)

    def test_counts_source_letters_after_nfc_normalization(self):
        """NFC 정규화 후 원문 Letter 수를 계산."""

        source_body = "ζ" * 39 + "e\u0301"
        source = f"{source_body}\n"
        translated = f"""<!-- {source_body} -->
{"가" * 3}
"""

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_accepts_each_japanese_target_script(self):
        """히라가나·가타카나·한자를 일본어 대상 문자로 인정."""

        source_body = "η" * 40
        source = f"{source_body}\n"

        for target in ("あ" * 8, "ア" * 8, "日" * 8):
            with self.subTest(target=target):
                translated = f"""<!-- {source_body} -->
{target}
"""
                self.assertNotIn(
                    "provider target language mismatch",
                    response_contract.verify(
                        translated, source, locale="ja"
                    ),
                )

    def test_does_not_apply_ascii_or_other_script_ratio_limits(self):
        """ASCII나 다른 문자 체계에 별도 비율 하한을 적용하지 않음."""

        source_body = "θ" * 40
        source = f"{source_body}\n"
        translated = f"""<!-- {source_body} -->
{"가" * 8} {"English" * 20} {"日本語" * 20}
"""

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_excludes_link_labels_and_inline_code_from_language_check(self):
        """언어 판정에서 링크 label과 inline code 제외."""

        protected = "EnglishReferenceLabel" * 3
        source_body = f"Go to [{protected}](/docs) with `{protected}`."
        source = f"{source_body}\n"
        translated = f"""<!-- {source_body} -->
{source_body}
"""

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_uses_unicode_15_1_letter_assignments(self):
        """Unicode 15.1의 Letter 할당 범위를 고정."""

        source_body = "ι" * 39 + "\u1c89"
        source = f"{source_body}\n"
        translated = f"""<!-- {source_body} -->
{"가" * 3}
"""

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_excludes_admonition_markers_from_source_letter_count(self):
        """원문 Letter 수에서 admonition 표식을 제외."""

        source = f"""> [!NOTE]
>
> {"κ" * 36}
"""
        translated = f"""> [!NOTE]
>
> {"가" * 3}
"""

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_counts_unicode_letters_in_legacy_table_prose_cells(self):
        """기존 표 산문 셀의 Unicode Letter 수를 반영."""

        source_body = "λ" * 40
        source = f"{source_body} | ID\n{'-' * 40} | ---\n"
        translated = (
            f"<!-- {source_body} | ID {'-' * 40} | --- -->\n"
            f"{'가' * 3} | ID\n{'-' * 40} | ---\n"
        )

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )


if __name__ == "__main__":
    unittest.main()
