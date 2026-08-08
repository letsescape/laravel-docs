"""response contract language 동작과 경계 조건 검증."""

import unittest

from sync import response_contract


class ResponseContractLanguageTests(unittest.TestCase):
    """로캘별 응답 언어 판정 경계 테스트."""

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

        self.assertFalse(
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

    def test_requires_one_canonical_annotation_for_a_pipe_table_owner(self):
        """GFM 표 전체에 하나의 canonical 소유 주석 요구."""

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

        missing = response_contract.verify(
            translated_table,
            source,
            locale="ko",
        )
        valid = response_contract.verify(
            annotation + translated_table,
            source,
            locale="ko",
        )

        self.assertIn("provider original comment mismatch", missing)
        self.assertIn("provider annotation ownership mismatch", missing)
        self.assertEqual(valid, [])

    def test_requires_one_canonical_annotation_for_a_legacy_pipe_table_owner(self):
        """legacy 표 전체에 하나의 canonical 소유 주석 요구."""

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

    def test_rejects_swapped_targets_for_repeated_inline_link_labels(self):
        """label이 같은 반복 inline 링크의 target 교환 거부."""

        source = "Use [Cache](cache) before [Cache](routing).\n"
        translated = (
            "<!-- Use [Cache](cache) before [Cache](routing). -->\n"
            "Use [Cache](routing) before [Cache](cache).\n"
        )

        issues = response_contract.verify(translated, source, locale=None)

        self.assertIn("provider link pair mismatch", issues)

    def test_hash_prefixed_prose_is_not_treated_as_an_atx_heading(self):
        """공백 없는 hash 접두 산문을 ATX heading에서 제외."""

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
        """exact-copy 최소 길이 미만에는 대상 문자 체계 요구 제외."""

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
        """표 산문 셀의 Unicode Letter 수 반영."""

        source_body = "γ" * 40
        source = f"""| {source_body} |
| --- |
"""
        translated = f"""| {"가" * 7} |
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

    def test_requires_eight_target_characters_at_forty_source_letters(self):
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
        """대상 문자 10퍼센트 하한을 올림 계산."""

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
        """NFC 정규화 후 원문 Letter 수 계산."""

        source_body = "ζ" * 39 + "e\u0301"
        source = f"{source_body}\n"
        translated = f"""<!-- {source_body} -->
{"가" * 7}
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
        """Unicode 15.1 Letter 할당 범위 고정."""

        source_body = "ι" * 39 + "\u1c89"
        source = f"{source_body}\n"
        translated = f"""<!-- {source_body} -->
{"가" * 7}
"""

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_excludes_admonition_markers_from_source_letter_count(self):
        """원문 Letter 수에서 admonition 표식 제외."""

        source = f"""> [!NOTE]
>
> {"κ" * 36}
"""
        translated = f"""> [!NOTE]
>
> {"가" * 7}
"""

        self.assertNotIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )

    def test_counts_unicode_letters_in_legacy_table_prose_cells(self):
        """legacy 표 산문 셀의 Unicode Letter 수 반영."""

        source_body = "λ" * 40
        source = f"{source_body} | ID\n{'-' * 40} | ---\n"
        translated = (
            f"<!-- {source_body} | ID {'-' * 40} | --- -->\n"
            f"{'가' * 7} | ID\n{'-' * 40} | ---\n"
        )

        self.assertIn(
            "provider target language mismatch",
            response_contract.verify(translated, source, locale="ko"),
        )


if __name__ == "__main__":
    unittest.main()
