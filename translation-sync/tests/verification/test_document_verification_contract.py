"""문서 검증 계약의 동작과 경계 조건 검증."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from sync import verify as legacy_verify
from sync.common.stale_links import (
    DEFAULT_STALE_LINK_REGISTRY,
    StaleLinkRegistry,
    StaleLinkRule,
)
from sync.verification.document import (
    ExpectedAnnotationEntry,
    ExpectedAnnotationMap,
    VerificationInput,
    build_expected_annotation_map,
    create_verification_input,
    parse_expected_annotation_map,
    verify_document,
)


_REGISTRY_SHA256 = DEFAULT_STALE_LINK_REGISTRY.sha256


def _annotation_map(*entries: ExpectedAnnotationEntry) -> ExpectedAnnotationMap:
    """테스트 항목으로 스키마 버전 1의 annotation map 생성.

    Args:
        *entries: 문서 순서로 정렬된 예상 annotation 항목.

    Returns:
        테스트용 예상 annotation map.
    """

    return ExpectedAnnotationMap(schema_version=1, entries=entries)


def _verify_inputs(
    inputs: VerificationInput,
    *,
    final_input: VerificationInput | None = None,
    registry_at_start: StaleLinkRegistry | None = None,
    registry_at_end: StaleLinkRegistry | None = None,
):
    """시작·종료 snapshot을 구성해 문서 검증 실행.

    Args:
        inputs: 시작 시점의 검증 입력.
        final_input: 종료 시점에 반환할 검증 입력.
        registry_at_start: 시작 시점의 registry.
            없으면 기본 snapshot 복제본 사용.
        registry_at_end: 종료 시점의 registry.
            없으면 기본 snapshot 복제본 사용.

    Returns:
        문서 검증 결과.
    """

    start = registry_at_start or replace(DEFAULT_STALE_LINK_REGISTRY)
    end = registry_at_end or replace(DEFAULT_STALE_LINK_REGISTRY)
    return verify_document(
        inputs,
        registry_at_start=start,
        final_snapshot=lambda: (final_input or replace(inputs), end),
    )


class ExpectedAnnotationMapTests(unittest.TestCase):
    """예상 annotation map의 동작과 경계 조건 테스트 모음."""

    def test_round_trips_only_canonical_bytes_and_preserves_duplicates(self):
        """canonical byte만 왕복 변환하고 중복 항목을 보존하는지 검증."""

        expected = _annotation_map(
            ExpectedAnnotationEntry(
                "section:cache/paragraph:1",
                1,
                "<!-- Repeated guidance. -->",
            ),
            ExpectedAnnotationEntry(
                "section:cache/paragraph:1",
                2,
                "<!-- Repeated guidance. -->",
            ),
        )

        raw = expected.canonical_bytes()

        self.assertEqual(parse_expected_annotation_map(raw), expected)
        self.assertEqual(raw.count(b"Repeated guidance."), 2)
        self.assertTrue(raw.endswith(b"\n"))

    def test_rejects_noncanonical_map_bytes_and_occurrence_gaps(self):
        """map의 비정규 byte와 불연속 occurrence를 거부."""

        value = {
            "schema_version": 1,
            "entries": [
                {
                    "structural_address": "section:cache/paragraph:1",
                    "occurrence": 2,
                    "annotation": "<!-- Cache guidance. -->",
                }
            ],
        }
        compact = (json.dumps(value) + "\n").encode()

        with self.assertRaisesRegex(ValueError, "canonical"):
            parse_expected_annotation_map(compact)
        with self.assertRaisesRegex(ValueError, "occurrence"):
            ExpectedAnnotationMap(
                schema_version=1,
                entries=(
                    ExpectedAnnotationEntry(
                        "section:cache/paragraph:1",
                        2,
                        "<!-- Cache guidance. -->",
                    ),
                ),
            )


class DocumentVerificationTests(unittest.TestCase):
    """문서 검증의 동작과 경계 조건 테스트 모음."""

    def _verify(
        self,
        source: str,
        translated: str,
        annotations: ExpectedAnnotationMap | None = None,
        *,
        version: str = "13.x",
    ):
        """영어·locale 문서로 검증 입력을 구성해 검사.

        Args:
            source: 비교 기준 영어 문서.
            translated: 검사할 locale 문서.
            annotations: 별도로 지정하는 예상 annotation map.
            version: 문서 링크 정규화에 사용할 버전.

        Returns:
            문서 검증 결과.
        """

        inputs = create_verification_input(
            locale_document=translated,
            english_view=source,
            annotation_source=source,
            version=version,
            registry_sha256=_REGISTRY_SHA256,
            expected_annotation_map=annotations,
        )
        return _verify_inputs(inputs)

    def test_front_matter_key_order_and_scalar_shape_are_exact(self):
        """front matter의 key 순서와 scalar 형태가 정확히 일치하는지 검증."""

        source = "---\ntitle: Cache\ndescription: Cache guide.\n---\n"
        translated = "---\ndescription: 캐시 안내입니다.\ntitle: Cache\n---\n"

        result = self._verify(source, translated)

        self.assertEqual(
            [issue.code for issue in result.issues],
            ["FRONT_MATTER_MISMATCH"],
        )
        self.assertIsNone(result.artifact)

    def test_front_matter_rejects_non_string_scalar(self):
        """문자열이 아닌 front matter scalar를 거부."""

        source = "---\ntitle: Cache\n---\n"
        translated = "---\ntitle: Cache\nenabled: true\n---\n"

        result = self._verify(source, translated)

        self.assertIn(
            "FRONT_MATTER_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_front_matter_delimiters_must_be_exact_bytes(self):
        """front matter 구분자의 byte 단위 일치를 요구."""

        source = "---\ntitle: Cache\n---\n"
        variants = (
            "  ---\ntitle: Cache\n---\n",
            "---\ntitle: Cache\n  ---\n",
        )

        for translated in variants:
            with self.subTest(translated=translated):
                result = self._verify(source, translated)
                self.assertIn(
                    "FRONT_MATTER_MISMATCH",
                    {issue.code for issue in result.issues},
                )
                self.assertIsNone(result.artifact)

    def test_source_owned_block_scalar_bytes_are_exact(self):
        """원문이 소유한 block scalar의 byte 단위 일치를 요구."""

        source = "---\ntitle: |\n  Cache\n---\n"
        translated = "---\ntitle: |\n  Cache  \n---\n"

        result = self._verify(source, translated)

        self.assertIn(
            "FRONT_MATTER_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_list_marker_depth_checkbox_and_occurrence_are_exact(self):
        """목록 표식의 깊이·checkbox·occurrence가 정확히 일치하는지 검증."""

        source = "- [ ] First.\n  * Nested.\n1. Ordered.\n"
        translated = "* [x] 첫째.\n- 중첩.\n1) 순서.\n- 추가.\n"

        result = self._verify(source, translated)

        self.assertIn(
            "LIST_TABLE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_comment_only_list_item_still_preserves_its_marker(self):
        """주석만 있는 목록 항목도 표식을 보존하는지 검증."""

        source = "- <!-- keep -->\n"
        translated = (
            "<!-- - <!-- keep --&gt; -->\n"
            "* <!-- keep -->\n"
        )

        result = self._verify(source, translated)

        self.assertIn(
            "LIST_TABLE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_list_and_table_signatures_include_blockquote_containers(self):
        """목록과 표의 signature에 blockquote container를 포함하는지 검증."""

        source = (
            "> - [ ] Quoted item.\n\n"
            "> | Left | Right |\n"
            "> | :--- | ---: |\n"
            "> | A | B |\n"
        )
        translated = (
            "> * [x] 인용 항목입니다.\n\n"
            "> | 왼쪽 | 오른쪽 |\n"
            "> | ---: | :--- |\n"
            "> | 가 | 나 |\n"
        )

        result = self._verify(source, translated)

        self.assertIn(
            "LIST_TABLE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_indented_code_is_not_misread_as_a_table_or_quote_list(self):
        """들여쓰기 코드를 표나 인용 목록으로 오인하지 않는지 검증."""

        cases = (
            (
                "| A | B |\n| --- | --- |\n| C | D |\n",
                "    | 가 | 나 |\n    | --- | --- |\n    | 다 | 라 |\n",
            ),
            (
                "> - Item.\n",
                "    > - 항목입니다.\n",
            ),
            (
                "Name | Value\n--- | ---\nA | B\n",
                "    이름 | 값\n    --- | ---\n    가 | 나\n",
            ),
        )

        for source, translated in cases:
            with self.subTest(source=source):
                result = self._verify(source, translated)
                self.assertIn(
                    "LIST_TABLE_STRUCTURE_MISMATCH",
                    {issue.code for issue in result.issues},
                )

    def test_nested_quote_list_inside_a_list_remains_structurally_visible(self):
        """목록 안에 중첩된 인용 목록이 구조에 노출되는지 검증."""

        source = "- Parent.\n    > - Nested quoted item.\n"
        translated = (
            "<!-- - Parent. -->\n"
            "- 상위 항목입니다.\n"
            "    > * 중첩 인용 항목입니다.\n"
        )

        result = self._verify(
            source,
            translated,
            build_expected_annotation_map(source),
        )

        self.assertIn(
            "LIST_TABLE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_table_rows_columns_and_alignment_are_exact(self):
        """표의 행·열·정렬이 정확히 일치하는지 검증."""

        source = "| Left | Right |\n| :--- | ---: |\n| A | B |\n"
        translated = "| 왼쪽 | 오른쪽 |\n| ---: | :--- |\n| 가 | 나 |\n| 다 | 라 |\n"

        result = self._verify(source, translated)

        self.assertIn(
            "LIST_TABLE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_final_table_has_one_full_table_owner_before_the_table(self):
        """마지막 표 앞에 전체 표의 owner가 하나만 있는지 검증."""

        source = (
            "| Name | Value |\n"
            "| --- | --- |\n"
            "| Widget | enabled |\n"
        )
        annotation = (
            "<!-- | Name | Value | | --- | --- | | Widget | enabled | -->"
        )
        valid = (
            f"{annotation}\n"
            "| 이름 | 값 |\n"
            "| --- | --- |\n"
            "| Widget | 활성 |\n"
        )
        row_internal = (
            "| 이름 | 값 |\n"
            "| --- | --- |\n"
            f"{annotation}\n"
            "| Widget | 활성 |\n"
        )

        valid_result = self._verify(source, valid)
        invalid_result = self._verify(source, row_internal)

        self.assertEqual(valid_result.issues, ())
        self.assertIsNotNone(valid_result.artifact)
        self.assertIn(
            "PIPELINE_ANNOTATION_MISMATCH",
            {issue.code for issue in invalid_result.issues},
        )

    def test_table_separator_requires_at_least_three_hyphens(self):
        """표 구분선에 하이픈을 세 개 이상 요구."""

        source = (
            "| Name | Value |\n"
            "| --- | --- |\n"
            "| Widget | enabled |\n"
        )
        annotation = (
            "<!-- | Name | Value | | --- | --- | | Widget | enabled | -->"
        )
        translated = (
            f"{annotation}\n"
            "| 이름 | 값 |\n"
            "| -- | - |\n"
            "| Widget | 활성 |\n"
        )

        result = self._verify(source, translated)

        self.assertIn(
            "LIST_TABLE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_legacy_pipe_table_shape_is_also_exact(self):
        """기존 pipe 표의 형태도 정확히 일치하는지 검증."""

        source = "Name | Value\n:--- | ---:\nCache | Lock\n"
        translated = "이름 | 값\n---: | :---\n캐시 | 잠금\n추가 | 행\n"

        result = self._verify(source, translated)

        self.assertIn(
            "LIST_TABLE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_legacy_table_also_uses_one_full_table_owner(self):
        """기존 표에도 전체 표의 단일 owner를 사용."""

        source = "Name | Value\n--- | ---\nWidget | enabled\n"
        expected = build_expected_annotation_map(source)
        self.assertEqual(
            [entry.structural_address for entry in expected.entries],
            ["section:document/table:1"],
        )
        translated = (
            f"{expected.entries[0].annotation}\n"
            "이름 | 값\n"
            "--- | ---\n"
            "Widget | 활성\n"
        )

        result = self._verify(source, translated)

        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.artifact)

    def test_expected_map_requires_every_duplicate_annotation_occurrence(self):
        """예상 map에 중복 annotation의 모든 occurrence를 요구."""

        source = "Repeated guidance.\n\nRepeated guidance.\n"
        translated = "<!-- Repeated guidance. -->\n반복 안내입니다.\n"
        annotations = _annotation_map(
            ExpectedAnnotationEntry(
                "section:document/paragraph:1", 1, "<!-- Repeated guidance. -->"
            ),
            ExpectedAnnotationEntry(
                "section:document/paragraph:1", 2, "<!-- Repeated guidance. -->"
            ),
        )

        result = self._verify(source, translated, annotations)

        self.assertIn(
            "PIPELINE_ANNOTATION_MISMATCH",
            {issue.code for issue in result.issues},
        )
        self.assertIsNone(result.artifact)

    def test_legacy_final_verifier_also_preserves_duplicate_occurrences(self):
        """기존 최종 검증기도 중복 occurrence를 보존하는지 검증."""

        source = "Repeated guidance.\n\nRepeated guidance.\n"
        translated = "<!-- Repeated guidance. -->\n반복 안내입니다.\n"

        issues = legacy_verify.verify(translated, source=source)

        self.assertIn("source comment mismatch", issues)
        self.assertEqual(
            legacy_verify.missing_original_comments(translated, source),
            ["Repeated guidance."],
        )

    def test_duplicate_annotations_must_each_own_a_following_block(self):
        """중복 annotation이 각각 후속 block을 소유해야 하는지 검증."""

        source = "Repeated guidance.\n\nRepeated guidance.\n"
        translated = (
            "<!-- Repeated guidance. -->\n"
            "<!-- Repeated guidance. -->\n"
            "첫 번째 반복 안내입니다.\n\n"
            "두 번째 반복 안내입니다.\n"
        )
        annotations = _annotation_map(
            ExpectedAnnotationEntry(
                "section:document/paragraph:1", 1, "<!-- Repeated guidance. -->"
            ),
            ExpectedAnnotationEntry(
                "section:document/paragraph:1", 2, "<!-- Repeated guidance. -->"
            ),
        )

        result = self._verify(source, translated, annotations)

        self.assertIn(
            "PIPELINE_ANNOTATION_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_annotation_cannot_be_moved_to_a_nonannotatable_owner(self):
        """annotation을 주석을 소유할 수 없는 owner로 이동하면 거부."""

        cases = (
            (
                "Paragraph guidance.\n\n- `foo`\n",
                "번역된 안내입니다.\n\n<!-- Paragraph guidance. -->\n- `foo`\n",
            ),
            (
                "- Translate this item.\n\n- `foo`\n",
                "- 이 항목을 번역합니다.\n\n"
                "<!-- - Translate this item. -->\n- `foo`\n",
            ),
            (
                "Paragraph guidance.\n\n```text\nvalue\n```\n",
                "번역된 안내입니다.\n\n"
                "<!-- Paragraph guidance. -->\n```text\nvalue\n```\n",
            ),
            (
                "Paragraph guidance.\n\n<a name=\"stable\"></a>\n",
                "번역된 안내입니다.\n\n"
                "<!-- Paragraph guidance. -->\n<a name=\"stable\"></a>\n",
            ),
        )

        for source, translated in cases:
            with self.subTest(source=source):
                result = self._verify(source, translated)
                self.assertIn(
                    "PIPELINE_ANNOTATION_MISMATCH",
                    {issue.code for issue in result.issues},
                )

    def test_annotation_owner_kind_must_match_the_following_block(self):
        """annotation owner와 후속 block의 종류가 일치해야 함."""

        source = "Paragraph guidance.\n\n- Translate this item.\n"
        translated = (
            "번역된 안내입니다.\n\n"
            "<!-- Paragraph guidance. -->\n"
            "- 번역된 항목입니다.\n\n"
            "<!-- - Translate this item. -->\n"
            "뒤늦은 문단입니다.\n"
        )

        result = self._verify(source, translated)

        self.assertIn(
            "PIPELINE_ANNOTATION_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_heading_class_is_kept_in_annotation_but_not_visible_heading(self):
        """heading class는 annotation에 유지하되 표시 heading에서는 제외."""

        annotation_source = "## Title {.class #stable}\n"
        english_view = "## Title {#stable}\n"
        translated = (
            "<!-- ## Title {.class #stable} -->\n"
            "## Title {#stable}\n"
        )
        expected = build_expected_annotation_map(annotation_source)
        self.assertEqual(
            [entry.structural_address for entry in expected.entries],
            ["section:stable/heading:2"],
        )
        inputs = create_verification_input(
            locale_document=translated,
            english_view=english_view,
            annotation_source=annotation_source,
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
            expected_annotation_map=expected,
        )

        result = _verify_inputs(inputs)

        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.artifact)

    def test_every_annotatable_locale_block_must_have_an_owner(self):
        """locale의 모든 주석 가능 block에 owner를 요구."""

        source = "First guidance.\n\nSecond guidance.\n"
        translated = (
            "<!-- First guidance. -->\n첫 안내입니다.\n\n"
            "소스에 없는 추가 문단입니다.\n\n"
            "<!-- Second guidance. -->\n둘째 안내입니다.\n"
        )

        result = self._verify(
            source,
            translated,
            build_expected_annotation_map(source),
        )

        self.assertIn(
            "PIPELINE_ANNOTATION_MISMATCH",
            {issue.code for issue in result.issues},
        )
        self.assertIsNone(result.artifact)

    def test_pipeline_annotation_must_be_an_exact_standalone_line(self):
        """pipeline annotation이 정확한 독립 줄이어야 하는지 검증."""

        source = "Guidance.\n"
        variants = (
            "소스에 없는 접두문 <!-- Guidance. -->\n안내입니다.\n",
            "    <!-- Guidance. -->\n안내입니다.\n",
        )

        for translated in variants:
            with self.subTest(translated=translated):
                result = self._verify(
                    source,
                    translated,
                    build_expected_annotation_map(source),
                )
                self.assertIn(
                    "PIPELINE_ANNOTATION_MISMATCH",
                    {issue.code for issue in result.issues},
                )

    def test_comparison_operator_before_extra_comment_is_not_a_quote_prefix(self):
        """추가 주석 앞의 비교 연산자를 인용 prefix로 오인하지 않는지 검증."""

        source = "Compare values.\n"
        translated = (
            "<!-- Compare values. -->\n"
            "값을 비교합니다 1 > 0 <!-- Injected extra. -->\n"
        )

        result = self._verify(source, translated)

        self.assertIn(
            "PIPELINE_ANNOTATION_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_extra_unannotated_blockquote_is_rejected(self):
        """annotation이 없는 추가 blockquote를 거부."""

        source = "> Guidance.\n"
        translated = "> 안내입니다.\n\n> 소스에 없는 인용입니다.\n"

        result = self._verify(source, translated)

        self.assertIn(
            "SOURCE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_checked_inline_code_only_lists_do_not_require_annotations(self):
        """체크된 inline code 전용 목록에는 annotation을 요구하지 않음."""

        documents = (
            "- [x] `cache-key`\n",
            "1) [x] `cache-key`\n",
        )

        for document in documents:
            with self.subTest(document=document):
                result = self._verify(document, document)
                self.assertEqual(result.issues, ())
                self.assertIsNotNone(result.artifact)

    def test_every_bare_internal_link_list_marker_is_non_annotatable(self):
        """bare 내부 link 목록의 표식을 모두 주석 불가로 판정."""

        documents = (
            "+ [Anchor](#anchor)\n",
            "1. [Anchor](#anchor)\n",
            "1) [Anchor](#anchor)\n",
        )

        for document in documents:
            with self.subTest(document=document):
                result = self._verify(document, document)
                self.assertEqual(result.issues, ())
                self.assertIsNotNone(result.artifact)

    def test_hash_prefixed_prose_is_not_misclassified_as_a_heading(self):
        """해시 기호로 시작하는 산문을 heading으로 오인하지 않는지 검증."""

        source = "#hashtag guidance.\n"
        translated = (
            "<!-- #hashtag guidance. -->\n"
            "해시태그 안내입니다.\n"
        )

        result = self._verify(source, translated)

        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.artifact)

    def test_final_structure_stage_does_not_repeat_language_or_sentence_checks(self):
        """최종 구조 단계에서 언어·문장 검사를 반복하지 않는지 검증."""

        source = "This guidance explains cache behavior.\n"
        translations = (
            (
                "<!-- This guidance explains cache behavior. -->\n"
                "This guidance explains cache behavior.\n"
            ),
            (
                "<!-- This guidance explains cache behavior. -->\n"
                "이 안내는 캐시 동작을 설명합니다. 두 번째 문장입니다.\n"
            ),
        )

        for translated in translations:
            with self.subTest(translated=translated):
                result = self._verify(
                    source,
                    translated,
                    build_expected_annotation_map(source),
                )
                self.assertEqual(result.issues, ())
                self.assertIsNotNone(result.artifact)

    def test_expected_map_is_derived_from_source_and_checks_target_bytes(self):
        """예상 map을 원문에서 파생하고 대상 byte를 검사하는지 검증."""

        source = "Cache guidance.\n"
        translated = "<!-- Cache guidance. -->\n캐시 안내입니다.\n"
        wrong_source_map = _annotation_map(
            ExpectedAnnotationEntry(
                "document/paragraph:1", 1, "<!-- Different source. -->"
            )
        )

        with self.assertRaisesRegex(ValueError, "annotation_source"):
            self._verify(source, translated, wrong_source_map)
        target_result = self._verify(
            source,
            "<!--  Cache guidance.  -->\n캐시 안내입니다.\n",
            _annotation_map(
                ExpectedAnnotationEntry(
                    "section:document/paragraph:1",
                    1,
                    "<!-- Cache guidance. -->",
                )
            ),
        )

        self.assertIn(
            "PIPELINE_ANNOTATION_MISMATCH",
            {issue.code for issue in target_result.issues},
        )

    def test_expected_map_structural_address_is_source_derived(self):
        """예상 map의 구조 주소를 원문에서 파생하는지 검증."""

        source = "# Cache\n\nCache guidance.\n"
        translated = (
            "<!-- # Cache -->\n# Cache\n\n"
            "<!-- Cache guidance. -->\n캐시 안내입니다.\n"
        )
        wrong_addresses = _annotation_map(
            ExpectedAnnotationEntry(
                "section:wrong/heading:1", 1, "<!-- # Cache -->"
            ),
            ExpectedAnnotationEntry(
                "section:wrong/paragraph:1", 1, "<!-- Cache guidance. -->"
            ),
        )

        with self.assertRaisesRegex(ValueError, "annotation_source"):
            self._verify(source, translated, wrong_addresses)

    def test_same_shape_wrong_annotation_map_is_rejected_at_input_creation(self):
        """형태는 같지만 잘못된 annotation map을 입력 생성 시 거부."""

        source = "Correct guidance.\n"
        wrong = _annotation_map(
            ExpectedAnnotationEntry(
                "section:document/paragraph:1",
                1,
                "<!-- Wrong guidance. -->",
            )
        )

        with self.assertRaisesRegex(ValueError, "annotation_source"):
            self._verify(
                source,
                "<!-- Wrong guidance. -->\n잘못된 안내입니다.\n",
                wrong,
            )

    def test_builder_derives_section_addresses_and_ordered_occurrences(self):
        """builder가 section 주소와 occurrence 순서를 파생하는지 검증."""

        source = (
            "# Cache\n\nRepeated guidance.\n\nRepeated guidance.\n"
        )

        expected = build_expected_annotation_map(source)

        self.assertEqual(
            expected.entries,
            (
                ExpectedAnnotationEntry(
                    "section:cache/heading:1", 1, "<!-- # Cache -->"
                ),
                ExpectedAnnotationEntry(
                    "section:cache/paragraph:1",
                    1,
                    "<!-- Repeated guidance. -->",
                ),
                ExpectedAnnotationEntry(
                    "section:cache/paragraph:1",
                    2,
                    "<!-- Repeated guidance. -->",
                ),
            ),
        )

    def test_input_factory_builds_the_expected_map_from_separate_annotation_source(self):
        """입력 factory가 별도 annotation 원문에서 예상 map을 생성하는지 검증."""

        source = "Cache guidance.\n"
        translated = "<!-- Cache guidance. -->\n캐시 안내입니다.\n"
        inputs = create_verification_input(
            locale_document=translated,
            english_view=source,
            annotation_source=source,
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )

        result = _verify_inputs(inputs)

        self.assertEqual(result.issues, ())
        self.assertEqual(
            result.verification_input_sha256,
            inputs.verification_input_sha256,
        )
        self.assertIsNotNone(result.artifact)

    def test_reference_definition_targets_use_canonical_version_comparison(self):
        """reference definition target을 canonical 버전과 비교하는지 검증."""

        source = "[cache]: cache \"Cache docs\"\n"
        translated = (
            "[CACHE]: https://laravel.com/docs/13.x/cache \"Cache docs\"\n"
        )

        result = self._verify(source, translated)

        self.assertNotIn(
            "SOURCE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_reference_definition_root_fragments_are_canonical(self):
        """reference definition의 root fragment가 canonical 형태인지 검증."""

        source = "[part]: #part\n"
        translated = "[PART]: https://laravel.com/docs/13.x#part\n"

        result = self._verify(source, translated)

        self.assertEqual(result.issues, ())

    def test_reference_definition_title_and_order_stay_exact(self):
        """reference definition의 title과 순서가 정확히 유지되는지 검증."""

        source = "[a]: cache \"A\"\n\n[b]: routing \"B\"\n"
        translated = "[b]: routing \"B\"\n\n[a]: cache \"changed\"\n"

        result = self._verify(source, translated)

        self.assertIn(
            "SOURCE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_reference_style_visible_label_is_source_owned(self):
        """reference style의 표시 label을 원문 소유로 판정."""

        source = "[Cache][x]\n\n[x]: cache\n"
        translated = (
            "<!-- [Cache][x] -->\n"
            "[캐시][x]\n\n"
            "[x]: cache\n"
        )

        result = self._verify(
            source,
            translated,
            build_expected_annotation_map(source),
        )

        self.assertIn(
            "SOURCE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_commonmark_link_forms_are_checked_before_artifact_creation(self):
        """산출물 생성 전에 CommonMark 링크 형식을 검사하는지 검증."""

        cases = (
            (
                "Visit <https://example.com/a>.\n",
                "<!-- Visit <https://example.com/a>. -->\n"
                "<https://example.com/b>를 방문합니다.\n",
            ),
            (
                "Contact <user@example.com>.\n",
                "<!-- Contact <user@example.com>. -->\n"
                "<other@example.com>으로 문의합니다.\n",
            ),
            (
                "Use [Cache]() here.\n",
                "<!-- Use [Cache]() here. -->\n"
                "여기에서 [캐시]()를 사용합니다.\n",
            ),
            (
                "See [Docs](<https://example.com/a b>).\n",
                "<!-- See [Docs](<https://example.com/a b>). -->\n"
                "[Docs](<https://example.com/c d>)를 참고합니다.\n",
            ),
        )

        for source, translated in cases:
            with self.subTest(source=source):
                result = self._verify(source, translated)
                self.assertTrue(
                    any("link" in issue.message for issue in result.issues)
                )
                self.assertIsNone(result.artifact)

    def test_inline_link_pairs_preserve_ordered_occurrences(self):
        """inline link pair가 occurrence 순서를 보존하는지 검증."""

        source = "Use [Cache](cache) before [Cache](routing).\n"
        translated = (
            "<!-- Use [Cache](cache) before [Cache](routing). -->\n"
            "[Cache](routing) 다음 [Cache](cache)를 사용합니다.\n"
        )

        result = self._verify(source, translated)

        self.assertIn(
            "SOURCE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_anchor_name_with_whitespace_around_equals_is_compared(self):
        """등호 주변에 공백이 있는 anchor name도 비교하는지 검증."""

        source = '<a name = "old"></a>\n'
        translated = '<a name = "new"></a>\n'

        result = self._verify(source, translated)

        self.assertIn(
            "SOURCE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_fenced_code_trailing_bytes_are_source_owned(self):
        """fenced code의 후행 byte를 원문 소유로 판정."""

        source = "```sh\necho hi  \n```\n"
        translated = "```sh\necho hi\n```\n"

        result = self._verify(source, translated)

        self.assertIn(
            "SOURCE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_annotation_source_remains_pre_stale_while_english_view_is_canonical(self):
        """영어 view는 canonical 상태로 유지하면서 annotation 원문은 stale 판정 전 상태로 보존."""

        annotation_source = (
            "See [Controller](#actions-handled-by-resource-controller).\n"
        )
        english_view = (
            "See [Controller](#actions-handled-by-resource-controllers).\n"
        )
        translated = (
            "<!-- See [Controller](#actions-handled-by-resource-controller). -->\n"
            "[Controller](#actions-handled-by-resource-controllers)를 참고하세요.\n"
        )
        inputs = create_verification_input(
            locale_document=translated,
            english_view=english_view,
            annotation_source=annotation_source,
            version="10.x",
            registry_sha256=_REGISTRY_SHA256,
        )

        result = _verify_inputs(inputs)

        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.artifact)

    def test_retired_bare_link_keeps_pre_stale_ownership(self):
        """폐기된 bare link의 stale 이전 annotation 소유권 유지."""

        annotation_source = "[assertSimilarJson](#assert-similar-json)\n"
        english_view = "`assertSimilarJson`\n"
        locale_document = (
            "<!-- [assertSimilarJson](#assert-similar-json) -->\n"
            "`assertSimilarJson`\n"
        )
        inputs = create_verification_input(
            locale_document=locale_document,
            english_view=english_view,
            annotation_source=annotation_source,
            version="8.x",
            registry_sha256=_REGISTRY_SHA256,
        )

        result = _verify_inputs(inputs)

        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.artifact)

    def test_inline_source_authored_comment_is_not_a_pipeline_map_error(self):
        """원문 작성 inline 주석을 pipeline map 오류로 오인하지 않는지 검증."""

        source = "Before <!-- keep --> after.\n"
        translated = (
            "<!-- Before <!-- keep --&gt; after. -->\n"
            "이전 <!-- keep --> 이후입니다.\n"
        )
        inputs = create_verification_input(
            locale_document=translated,
            english_view=source,
            annotation_source=source,
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )

        result = _verify_inputs(inputs)

        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.artifact)

    def test_inline_source_comment_survives_soft_wrap_folding(self):
        """soft wrap을 접은 뒤에도 inline 원문 주석을 보존하는지 검증."""

        source = "First physical line\nsecond <!-- keep --> line.\n"
        expected = build_expected_annotation_map(source)
        translated = (
            f"{expected.entries[0].annotation}\n"
            "첫 번째와 두 번째 <!-- keep --> 줄입니다.\n"
        )

        result = self._verify(source, translated, expected)

        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.artifact)

    def test_success_returns_hash_bound_immutable_artifact(self):
        """성공 시 hash에 결합된 불변 산출물을 반환."""

        inputs = create_verification_input(
            locale_document="[cache]: cache\n",
            english_view="[cache]: /docs/13.x/cache\n",
            annotation_source="[cache]: /docs/13.x/cache\n",
            expected_annotation_map=_annotation_map(),
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )

        result = _verify_inputs(inputs)

        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.artifact)
        assert result.artifact is not None
        self.assertEqual(
            result.artifact.verification_input_sha256,
            inputs.verification_input_sha256,
        )
        self.assertEqual(result.artifact.locale_bytes, inputs.locale_bytes)

    def test_tampered_input_hash_returns_no_artifact_and_writes_nothing(self):
        """변조된 입력 hash에는 산출물을 반환하거나 기록하지 않음."""

        inputs = create_verification_input(
            locale_document="Cache guidance.\n",
            english_view="Cache guidance.\n",
            annotation_source="Cache guidance.\n",
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )
        tampered = replace(inputs, locale_bytes=b"changed\n")

        with tempfile.TemporaryDirectory() as directory:
            before = tuple(Path(directory).iterdir())
            result = _verify_inputs(tampered)
            after = tuple(Path(directory).iterdir())

        self.assertEqual(before, after)
        self.assertEqual(
            [issue.code for issue in result.issues],
            ["VERIFICATION_INPUT_CHANGED"],
        )
        self.assertIsNone(result.verification_input_sha256)
        self.assertIsNone(result.artifact)

    def test_invalid_version_is_rejected_by_factory_and_integrity_check(self):
        """잘못된 버전을 factory와 무결성 검사에서 모두 거부."""

        with self.assertRaisesRegex(ValueError, "version"):
            create_verification_input(
                locale_document="Cache.\n",
                english_view="Cache.\n",
                annotation_source="Cache.\n",
                version="garbage/path",
                registry_sha256=_REGISTRY_SHA256,
            )

        valid = create_verification_input(
            locale_document="[cache]: cache\n",
            english_view="[cache]: cache\n",
            annotation_source="[cache]: cache\n",
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )
        result = _verify_inputs(replace(valid, version="garbage/path"))
        self.assertEqual(
            [issue.code for issue in result.issues],
            ["VERIFICATION_INPUT_CHANGED"],
        )

    def test_expected_map_rejects_non_utf8_unicode_scalars(self):
        """예상 map에서 UTF-8로 인코딩할 수 없는 Unicode scalar를 거부."""

        value = {
            "schema_version": 1,
            "entries": [
                {
                    "structural_address": "section:cache/paragraph:1",
                    "occurrence": 1,
                    "annotation": "<!-- " + chr(0xD800) + " -->",
                }
            ],
        }
        raw = (json.dumps(value, ensure_ascii=True, indent=2) + "\n").encode()

        with self.assertRaisesRegex(ValueError, "UTF-8|canonical"):
            parse_expected_annotation_map(raw)

    def test_factory_rejects_non_utf8_unicode_documents(self):
        """factory에서 UTF-8로 인코딩할 수 없는 Unicode 문서를 거부."""

        for field in ("locale_document", "english_view"):
            values = {
                "locale_document": "Cache.\n",
                "english_view": "Cache.\n",
                "annotation_source": "Cache.\n",
                "version": "13.x",
                "registry_sha256": _REGISTRY_SHA256,
            }
            values[field] = chr(0xD800)

            with self.subTest(field=field), self.assertRaisesRegex(
                ValueError,
                "UTF-8",
            ):
                create_verification_input(**values)

    def test_factory_rejects_expected_map_and_entry_subclasses(self):
        """factory에서 예상 map과 entry의 하위 클래스를 거부."""

        class ForgedEntry(ExpectedAnnotationEntry):
            """정확한 dataclass 타입 검사용 위조 entry."""

            pass

        class ForgedMap(ExpectedAnnotationMap):
            """동작 재정의 검사용 위조 map."""

            def __ne__(self, other):
                """비동등 비교 결과 위조."""

                return False

            def canonical_bytes(self):
                """canonical byte 결과 위조."""

                return _annotation_map(
                    ExpectedAnnotationEntry(
                        "section:document/paragraph:1",
                        1,
                        "<!-- Wrong guidance. -->",
                    )
                ).canonical_bytes()

        with self.assertRaisesRegex(ValueError, "invalid expected annotation map"):
            create_verification_input(
                locale_document="<!-- Wrong guidance. -->\n안내입니다.\n",
                english_view="Correct guidance.\n",
                annotation_source="Correct guidance.\n",
                expected_annotation_map=ForgedMap(1, ()),
                version="13.x",
                registry_sha256=_REGISTRY_SHA256,
            )
        with self.assertRaisesRegex(ValueError, "entry"):
            ExpectedAnnotationMap(
                1,
                (
                    ForgedEntry(
                        "section:document/paragraph:1",
                        1,
                        "<!-- Correct guidance. -->",
                    ),
                ),
            )

    def test_registry_digest_is_rechecked_before_and_after_verification(self):
        """registry의 digest를 검증 전후에 다시 검사하는지 검증."""

        inputs = create_verification_input(
            locale_document="[cache]: cache\n",
            english_view="[cache]: cache\n",
            annotation_source="[cache]: cache\n",
            expected_annotation_map=_annotation_map(),
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )

        result = verify_document(
            inputs,
            registry_at_start=replace(
                DEFAULT_STALE_LINK_REGISTRY,
                sha256="b" * 64,
            ),
            final_snapshot=lambda: (
                replace(inputs),
                replace(DEFAULT_STALE_LINK_REGISTRY, sha256="c" * 64),
            ),
        )

        self.assertEqual(
            [issue.code for issue in result.issues],
            ["STALE_LINK_REGISTRY_CHANGED"],
        )
        self.assertEqual(
            result.verification_input_sha256,
            inputs.verification_input_sha256,
        )
        self.assertIsNone(result.artifact)

    def test_claimed_digest_must_match_the_registry_used_for_normalization(self):
        """명시된 digest와 정규화에 사용한 registry의 일치를 요구."""

        inputs = create_verification_input(
            locale_document="[cache]: cache\n",
            english_view="[cache]: cache\n",
            annotation_source="[cache]: cache\n",
            expected_annotation_map=_annotation_map(),
            version="13.x",
            registry_sha256="a" * 64,
        )

        result = _verify_inputs(inputs)

        self.assertEqual(
            [issue.code for issue in result.issues],
            ["STALE_LINK_REGISTRY_CHANGED"],
        )
        self.assertIsNone(result.artifact)

    def test_registry_rules_must_be_the_canonical_parse_of_bound_raw_bytes(self):
        """registry rule이 바인딩된 raw byte의 정규 구문 분석 결과인지 검증."""

        inputs = create_verification_input(
            locale_document="[cache]: bar\n",
            english_view="[cache]: foo\n",
            annotation_source="[cache]: foo\n",
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )
        manipulated = replace(
            DEFAULT_STALE_LINK_REGISTRY,
            rules=(StaleLinkRule("13.x", "foo", "bar", None),),
        )

        result = _verify_inputs(
            inputs,
            registry_at_start=replace(manipulated),
            registry_at_end=replace(manipulated),
        )

        self.assertEqual(
            [issue.code for issue in result.issues],
            ["STALE_LINK_REGISTRY_CHANGED"],
        )
        self.assertIsNone(result.artifact)

    def test_registry_snapshot_rejects_non_utf8_unicode_scalars(self):
        """registry snapshot에서 UTF-8로 인코딩할 수 없는 Unicode scalar를 거부."""

        value = {
            "schema_version": 1,
            "links": [
                {
                    "version": "13.x",
                    "from": chr(0xD800),
                    "to": "bar",
                    "retire_mode": None,
                }
            ],
        }
        raw = (json.dumps(value, ensure_ascii=True, indent=2) + "\n").encode()
        digest = hashlib.sha256(raw).hexdigest()
        snapshot = StaleLinkRegistry(
            raw,
            digest,
            (StaleLinkRule("13.x", chr(0xD800), "bar", None),),
        )
        inputs = create_verification_input(
            locale_document="[cache]: cache\n",
            english_view="[cache]: cache\n",
            annotation_source="[cache]: cache\n",
            version="13.x",
            registry_sha256=digest,
        )

        result = _verify_inputs(
            inputs,
            registry_at_start=replace(snapshot),
            registry_at_end=replace(snapshot),
        )

        self.assertEqual(
            [issue.code for issue in result.issues],
            ["STALE_LINK_REGISTRY_CHANGED"],
        )

    def test_registry_snapshot_rejects_unhashable_retire_mode_as_issue(self):
        """hash할 수 없는 retire mode가 있는 registry snapshot을 문제로 거부."""

        value = {
            "schema_version": 1,
            "links": [
                {
                    "version": "13.x",
                    "from": "#old",
                    "to": None,
                    "retire_mode": [],
                }
            ],
        }
        raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()
        digest = hashlib.sha256(raw).hexdigest()
        snapshot = StaleLinkRegistry(raw, digest, ())
        inputs = create_verification_input(
            locale_document="[cache]: cache\n",
            english_view="[cache]: cache\n",
            annotation_source="[cache]: cache\n",
            version="13.x",
            registry_sha256=digest,
        )

        result = _verify_inputs(
            inputs,
            registry_at_start=snapshot,
            registry_at_end=replace(snapshot),
        )

        self.assertEqual(
            [issue.code for issue in result.issues],
            ["STALE_LINK_REGISTRY_CHANGED"],
        )

    def test_registry_rule_subclasses_cannot_override_canonical_rules(self):
        """registry rule의 하위 클래스가 canonical rule을 재정의하지 못하도록 제한."""

        class ForgedRule(StaleLinkRule):
            """동등 비교 재정의 검사용 위조 규칙."""

            def __eq__(self, other):
                """동등 비교 결과 위조."""

                return True

        snapshot = replace(
            DEFAULT_STALE_LINK_REGISTRY,
            rules=(ForgedRule("13.x", "foo", "bar", None),),
        )
        inputs = create_verification_input(
            locale_document="[cache]: bar\n",
            english_view="[cache]: foo\n",
            annotation_source="[cache]: foo\n",
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )

        result = _verify_inputs(
            inputs,
            registry_at_start=snapshot,
            registry_at_end=replace(snapshot),
        )

        self.assertEqual(
            [issue.code for issue in result.issues],
            ["STALE_LINK_REGISTRY_CHANGED"],
        )

    def test_registry_internal_container_subclasses_are_rejected(self):
        """registry 내부 container의 하위 클래스를 거부."""

        class ForgedBytes(bytes):
            """정확한 byte 타입 검사용 하위 클래스."""

            pass

        snapshot = replace(
            DEFAULT_STALE_LINK_REGISTRY,
            raw=ForgedBytes(DEFAULT_STALE_LINK_REGISTRY.raw),
        )
        inputs = create_verification_input(
            locale_document="[cache]: cache\n",
            english_view="[cache]: cache\n",
            annotation_source="[cache]: cache\n",
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )

        result = _verify_inputs(
            inputs,
            registry_at_start=snapshot,
            registry_at_end=replace(snapshot),
        )

        self.assertEqual(
            [issue.code for issue in result.issues],
            ["STALE_LINK_REGISTRY_CHANGED"],
        )

    def test_registry_snapshot_rejects_behavior_overriding_subclasses(self):
        """동작을 재정의하는 registry snapshot의 하위 클래스를 거부."""

        class OverridingRegistry(StaleLinkRegistry):
            """규칙 조회 동작을 재정의한 registry."""

            def matching_rule(self, target, version):
                """원본 byte와 다른 규칙 반환."""

                return StaleLinkRule("13.x", "foo", "bar", None)

        snapshot = OverridingRegistry(
            DEFAULT_STALE_LINK_REGISTRY.raw,
            DEFAULT_STALE_LINK_REGISTRY.sha256,
            DEFAULT_STALE_LINK_REGISTRY.rules,
        )
        inputs = create_verification_input(
            locale_document="[cache]: bar\n",
            english_view="[cache]: foo\n",
            annotation_source="[cache]: foo\n",
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )

        result = verify_document(
            inputs,
            registry_at_start=OverridingRegistry(
                snapshot.raw,
                snapshot.sha256,
                snapshot.rules,
            ),
            final_snapshot=lambda: (
                replace(inputs),
                OverridingRegistry(
                    snapshot.raw,
                    snapshot.sha256,
                    snapshot.rules,
                ),
            ),
        )

        self.assertEqual(
            [issue.code for issue in result.issues],
            ["STALE_LINK_REGISTRY_CHANGED"],
        )

    def test_final_input_snapshot_is_rechecked_before_artifact_creation(self):
        """산출물 생성 전에 최종 입력 snapshot을 다시 검사."""

        inputs = create_verification_input(
            locale_document="[cache]: cache\n",
            english_view="[cache]: cache\n",
            annotation_source="[cache]: cache\n",
            expected_annotation_map=_annotation_map(),
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )
        final_input = create_verification_input(
            locale_document="[cache]: routing\n",
            english_view="[cache]: cache\n",
            annotation_source="[cache]: cache\n",
            expected_annotation_map=_annotation_map(),
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )

        result = _verify_inputs(inputs, final_input=final_input)

        self.assertEqual(
            [issue.code for issue in result.issues],
            ["VERIFICATION_INPUT_CHANGED"],
        )
        self.assertIsNone(result.artifact)

    def test_final_snapshot_callback_is_invoked_once_at_admission(self):
        """입력 승인 시 최종 snapshot callback을 한 번만 호출."""

        inputs = create_verification_input(
            locale_document="[cache]: cache\n",
            english_view="[cache]: cache\n",
            annotation_source="[cache]: cache\n",
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )
        calls: list[str] = []

        def final_snapshot():
            """호출 횟수를 기록한 종료 snapshot 반환."""

            calls.append("captured")
            return (
                replace(inputs),
                replace(DEFAULT_STALE_LINK_REGISTRY),
            )

        result = verify_document(
            inputs,
            registry_at_start=replace(DEFAULT_STALE_LINK_REGISTRY),
            final_snapshot=final_snapshot,
        )

        self.assertEqual(calls, ["captured"])
        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.artifact)

    def test_input_and_final_snapshot_subclasses_fail_closed(self):
        """입력과 최종 snapshot의 하위 클래스를 fail-closed로 거부."""

        class ForgedInput(VerificationInput):
            """동등 비교를 재정의한 위조 검증 입력."""

            def __eq__(self, other):
                """동등 비교 결과 위조."""

                return True

            def __ne__(self, other):
                """비동등 비교 결과 위조."""

                return False

        inputs = create_verification_input(
            locale_document="[cache]: cache\n",
            english_view="[cache]: cache\n",
            annotation_source="[cache]: cache\n",
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )
        forged = ForgedInput(
            inputs.locale_bytes,
            inputs.english_view_bytes,
            inputs.annotation_map_bytes,
            inputs.version,
            inputs.registry_sha256,
            inputs.envelope_bytes,
            inputs.verification_input_sha256,
        )

        start_result = verify_document(
            forged,
            registry_at_start=replace(DEFAULT_STALE_LINK_REGISTRY),
            final_snapshot=lambda: (
                replace(inputs),
                replace(DEFAULT_STALE_LINK_REGISTRY),
            ),
        )
        final_result = verify_document(
            inputs,
            registry_at_start=replace(DEFAULT_STALE_LINK_REGISTRY),
            final_snapshot=lambda: (
                forged,
                replace(DEFAULT_STALE_LINK_REGISTRY),
            ),
        )

        for result in (start_result, final_result):
            self.assertEqual(
                [issue.code for issue in result.issues],
                ["VERIFICATION_INPUT_CHANGED"],
            )
            self.assertIsNone(result.artifact)

    def test_input_byte_subclasses_fail_closed(self):
        """입력 byte의 하위 클래스를 fail-closed로 거부."""

        class ForgedBytes(bytes):
            """정확한 입력 byte 타입 검사용 하위 클래스."""

            pass

        inputs = create_verification_input(
            locale_document="[cache]: cache\n",
            english_view="[cache]: cache\n",
            annotation_source="[cache]: cache\n",
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )
        forged = replace(inputs, locale_bytes=ForgedBytes(inputs.locale_bytes))

        result = _verify_inputs(forged)

        self.assertEqual(
            [issue.code for issue in result.issues],
            ["VERIFICATION_INPUT_CHANGED"],
        )
        self.assertIsNone(result.artifact)

    def test_missing_start_or_end_recheck_fails_closed(self):
        """시작 또는 종료 재검사가 없으면 fail-closed로 거부."""

        inputs = create_verification_input(
            locale_document="[cache]: cache\n",
            english_view="[cache]: cache\n",
            annotation_source="[cache]: cache\n",
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )

        result = verify_document(
            inputs,
            registry_at_start=replace(DEFAULT_STALE_LINK_REGISTRY),
        )

        self.assertEqual(
            [issue.code for issue in result.issues],
            ["VERIFICATION_INPUT_CHANGED"],
        )
        self.assertIsNone(result.artifact)

    def test_same_input_object_is_not_a_fresh_final_snapshot(self):
        """같은 입력 객체를 새로운 최종 snapshot으로 인정하지 않음."""

        inputs = create_verification_input(
            locale_document="[cache]: cache\n",
            english_view="[cache]: cache\n",
            annotation_source="[cache]: cache\n",
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
        )

        result = verify_document(
            inputs,
            registry_at_start=replace(DEFAULT_STALE_LINK_REGISTRY),
            final_snapshot=lambda: (
                inputs,
                replace(DEFAULT_STALE_LINK_REGISTRY),
            ),
        )

        self.assertEqual(
            [issue.code for issue in result.issues],
            ["VERIFICATION_INPUT_CHANGED"],
        )

    def test_issues_are_deduplicated_and_sorted_by_stable_fields(self):
        """문제를 중복 제거하고 안정적인 field 기준으로 정렬."""

        inputs = VerificationInput(
            locale_bytes=b"---\ntitle: changed\n---\n{{version}}\n",
            english_view_bytes=b"---\ntitle: Source\n---\n- Item.\n",
            annotation_map_bytes=_annotation_map().canonical_bytes(),
            version="13.x",
            registry_sha256=_REGISTRY_SHA256,
            envelope_bytes=b"invalid\n",
            verification_input_sha256=hashlib.sha256(b"invalid\n").hexdigest(),
        )

        result = _verify_inputs(inputs)

        keys = [
            (
                issue.code.encode("utf-8"),
                (issue.structural_address or "").encode("utf-8"),
                issue.message.encode("utf-8"),
            )
            for issue in result.issues
        ]
        self.assertEqual(keys, sorted(set(keys)))


if __name__ == "__main__":
    unittest.main()
