"""document verification contract 동작과 경계 조건 검증."""

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
    """테스트 항목으로 schema version 1 annotation map 생성.

    Args:
        *entries: 문서 순서의 예상 annotation 항목.

    Returns:
        테스트에 사용할 예상 annotation map.
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
        registry_at_start: 시작 시점 registry. 없으면 기본 snapshot 복제본 사용.
        registry_at_end: 종료 시점 registry. 없으면 기본 snapshot 복제본 사용.

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
    """expected annotation map 동작과 경계 조건 테스트 모음."""

    def test_round_trips_only_canonical_bytes_and_preserves_duplicates(self):
        """`round_trips_only_canonical_bytes_and`의 duplicates 보존 검증."""

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
        """비정규 map bytes 및 occurrence gaps 거부 검증."""

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
    """문서 verification 동작과 경계 조건 테스트 모음."""

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
            annotations: 별도로 지정할 예상 annotation map.
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
        """`front_matter_key_order_and_scalar_shape_are_exact` 시나리오 검증."""

        source = "---\ntitle: Cache\ndescription: Cache guide.\n---\n"
        translated = "---\ndescription: 캐시 안내입니다.\ntitle: Cache\n---\n"

        result = self._verify(source, translated)

        self.assertEqual(
            [issue.code for issue in result.issues],
            ["FRONT_MATTER_MISMATCH"],
        )
        self.assertIsNone(result.artifact)

    def test_front_matter_rejects_non_string_scalar(self):
        """`front_matter`의 non string scalar 거부 검증."""

        source = "---\ntitle: Cache\n---\n"
        translated = "---\ntitle: Cache\nenabled: true\n---\n"

        result = self._verify(source, translated)

        self.assertIn(
            "FRONT_MATTER_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_front_matter_delimiters_must_be_exact_bytes(self):
        """`front_matter_delimiters_must_be_exact_bytes` 시나리오 검증."""

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
        """`source_owned_block_scalar_bytes_are_exact` 시나리오 검증."""

        source = "---\ntitle: |\n  Cache\n---\n"
        translated = "---\ntitle: |\n  Cache  \n---\n"

        result = self._verify(source, translated)

        self.assertIn(
            "FRONT_MATTER_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_list_marker_depth_checkbox_and_occurrence_are_exact(self):
        """`list_marker_depth_checkbox_and_occurrence_are_exact` 시나리오 검증."""

        source = "- [ ] First.\n  * Nested.\n1. Ordered.\n"
        translated = "* [x] 첫째.\n- 중첩.\n1) 순서.\n- 추가.\n"

        result = self._verify(source, translated)

        self.assertIn(
            "LIST_TABLE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_comment_only_list_item_still_preserves_its_marker(self):
        """`comment_only_list_item_still`의 its marker 보존 검증."""

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
        """`list_and_table_signatures_include_blockquote_containers` 시나리오 검증."""

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
        """`indented_code`의 않음 misread 로 table 또는 quote list 판정 검증."""

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
        """`nested_quote_list` 관련 경계 조건 검증."""

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
        """`table_rows_columns_and_alignment_are_exact` 시나리오 검증."""

        source = "| Left | Right |\n| :--- | ---: |\n| A | B |\n"
        translated = "| 왼쪽 | 오른쪽 |\n| ---: | :--- |\n| 가 | 나 |\n| 다 | 라 |\n"

        result = self._verify(source, translated)

        self.assertIn(
            "LIST_TABLE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_final_table_has_one_full_table_owner_before_the_table(self):
        """`final_table_has_one_full_table_owner_before_the_table` 시나리오 검증."""

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
        """`table_separator`의 at least three hyphens 요구 검증."""

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
        """`legacy_pipe_table_shape`의 also exact 판정 검증."""

        source = "Name | Value\n:--- | ---:\nCache | Lock\n"
        translated = "이름 | 값\n---: | :---\n캐시 | 잠금\n추가 | 행\n"

        result = self._verify(source, translated)

        self.assertIn(
            "LIST_TABLE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_legacy_table_also_uses_one_full_table_owner(self):
        """`legacy_table_also`의 one 전체 table owner 사용 검증."""

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
        """`expected_map`의 every duplicate annotation occurrence 요구 검증."""

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
        """`legacy_final_verifier_also`의 duplicate occurrences 보존 검증."""

        source = "Repeated guidance.\n\nRepeated guidance.\n"
        translated = "<!-- Repeated guidance. -->\n반복 안내입니다.\n"

        issues = legacy_verify.verify(translated, source=source)

        self.assertIn("source comment mismatch", issues)
        self.assertEqual(
            legacy_verify.missing_original_comments(translated, source),
            ["Repeated guidance."],
        )

    def test_duplicate_annotations_must_each_own_a_following_block(self):
        """`duplicate_annotations_must_each_own_a_following_block` 시나리오 검증."""

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
        """`annotation_cannot_be_moved_to_a_nonannotatable_owner` 시나리오 검증."""

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
        """`annotation_owner_kind_must_match_the_following_block` 시나리오 검증."""

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
        """`heading_class`의 kept in annotation but 않음 visible heading 판정 검증."""

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
        """`every_annotatable_locale_block_must_have_an_owner` 시나리오 검증."""

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
        """`pipeline_annotation_must_be_an_exact_standalone_line` 시나리오 검증."""

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
        """`comparison_operator_before_extra_comment`의 않음 quote prefix 판정 검증."""

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
        """`extra_unannotated_blockquote`의 rejected 판정 검증."""

        source = "> Guidance.\n"
        translated = "> 안내입니다.\n\n> 소스에 없는 인용입니다.\n"

        result = self._verify(source, translated)

        self.assertIn(
            "SOURCE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_checked_inline_code_only_lists_do_not_require_annotations(self):
        """`checked_inline_code` 관련 경계 조건 검증."""

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
        """`every_bare_internal_link_list_marker`의 non annotatable 판정 검증."""

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
        """`hash_prefixed_prose`의 않음 misclassified 로 heading 판정 검증."""

        source = "#hashtag guidance.\n"
        translated = (
            "<!-- #hashtag guidance. -->\n"
            "해시태그 안내입니다.\n"
        )

        result = self._verify(source, translated)

        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.artifact)

    def test_final_structure_stage_does_not_repeat_language_or_sentence_checks(self):
        """`final_structure_stage`의 않음 repeat 언어 또는 sentence checks 동작 검증."""

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
        """`expected_map`의 derived from 원문 및 checks 대상 bytes 판정 검증."""

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
        """`expected_map_structural_address`의 원문 derived 판정 검증."""

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
        """`same_shape_wrong_annotation_map`의 rejected at 입력 creation 판정 검증."""

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
        """`builder_derives_section` 관련 경계 조건 검증."""

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
        """`input_factory`의 expected map from separate annotation 원문 생성 검증."""

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
        """`reference_definition_targets` 관련 경계 조건 검증."""

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
        """`reference_definition_root_fragments_are_canonical` 시나리오 검증."""

        source = "[part]: #part\n"
        translated = "[PART]: https://laravel.com/docs/13.x#part\n"

        result = self._verify(source, translated)

        self.assertEqual(result.issues, ())

    def test_reference_definition_title_and_order_stay_exact(self):
        """`reference_definition_title_and_order_stay_exact` 시나리오 검증."""

        source = "[a]: cache \"A\"\n\n[b]: routing \"B\"\n"
        translated = "[b]: routing \"B\"\n\n[a]: cache \"changed\"\n"

        result = self._verify(source, translated)

        self.assertIn(
            "SOURCE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_reference_style_visible_label_is_source_owned(self):
        """`reference_style_visible_label`의 원문 owned 판정 검증."""

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
        """산출물 creation 전 commonmark 링크 forms checked 시나리오 검증."""

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
        """`inline_link_pairs_preserve_ordered_occurrences` 시나리오 검증."""

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
        """`anchor_name_with_whitespace_around_equals`의 compared 판정 검증."""

        source = '<a name = "old"></a>\n'
        translated = '<a name = "new"></a>\n'

        result = self._verify(source, translated)

        self.assertIn(
            "SOURCE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_fenced_code_trailing_bytes_are_source_owned(self):
        """`fenced_code_trailing_bytes_are_source_owned` 시나리오 검증."""

        source = "```sh\necho hi  \n```\n"
        translated = "```sh\necho hi\n```\n"

        result = self._verify(source, translated)

        self.assertIn(
            "SOURCE_STRUCTURE_MISMATCH",
            {issue.code for issue in result.issues},
        )

    def test_annotation_source_remains_pre_stale_while_english_view_is_canonical(self):
        """`annotation_source_remains`의 상태 판정 경계 검증."""

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
        """폐기된 bare 링크의 pre stale annotation ownership 유지."""

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
        """`inline_source_authored_comment`의 않음 pipeline map 오류 판정 검증."""

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
        """`inline_source_comment_survives_soft_wrap_folding` 시나리오 검증."""

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
        """`success`의 hash bound immutable 산출물 반환 검증."""

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
        """`tampered_input_hash`의 no 산출물 및 writes nothing 반환 검증."""

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
        """`invalid_version`의 rejected by factory 및 integrity check 판정 검증."""

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
        """`expected_map`의 non utf8 unicode scalars 거부 검증."""

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
        """`factory`의 non utf8 unicode 문서 거부 검증."""

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
        """`factory`의 expected map 및 entry subclasses 거부 검증."""

        class ForgedEntry(ExpectedAnnotationEntry):
            """정확한 dataclass 타입 검사용 위조 entry."""

            pass

        class ForgedMap(ExpectedAnnotationMap):
            """동작 재정의 검사용 위조 map."""

            def __ne__(self, other):
                """비동등 비교 결과 위조."""

                return False

            def canonical_bytes(self):
                """Canonical 바이트 결과 위조."""

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
        """`registry_digest`의 and after verification 전 rechecked 판정 검증."""

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
        """`claimed_digest_must` 관련 경계 조건 검증."""

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
        """`registry_rules_must` 관련 경계 조건 검증."""

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
        """`registry_snapshot`의 non utf8 unicode scalars 거부 검증."""

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
        """`registry_snapshot`의 unhashable retire mode 로 문제 거부 검증."""

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
        """`registry_rule_subclasses` 관련 경계 조건 검증."""

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
        """`registry_internal_container_subclasses_are_rejected` 시나리오 검증."""

        class ForgedBytes(bytes):
            """정확한 바이트 타입 검사용 하위 클래스."""

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
        """`registry_snapshot`의 behavior overriding subclasses 거부 검증."""

        class OverridingRegistry(StaleLinkRegistry):
            """규칙 조회 동작을 재정의한 registry."""

            def matching_rule(self, target, version):
                """원본 바이트와 다른 규칙 반환."""

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
        """`final_input_snapshot`의 산출물 creation 전 rechecked 판정 검증."""

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
        """`final_snapshot_callback`의 invoked once at admission 판정 검증."""

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
        """`input_and_final_snapshot_subclasses_fail_closed` 시나리오 검증."""

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
        """`input_byte_subclasses_fail_closed` 시나리오 검증."""

        class ForgedBytes(bytes):
            """정확한 입력 바이트 타입 검사용 하위 클래스."""

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
        """`missing_start_or_end_recheck`의 closed 실패 처리 검증."""

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
        """`same_input_object`의 않음 fresh final snapshot 판정 검증."""

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
        """`issues_are_deduplicated_and_sorted_by_stable_fields` 시나리오 검증."""

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
