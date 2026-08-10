"""`patch` 동작과 경계 조건을 검증함."""

import difflib
import unittest

from sync import diff, patch, preprocess, verify


def _plan(
    old_en: str,
    new_en: str,
    *,
    normalize_source=None,
    normalize_source_pair=None,
) -> patch.PatchPlan:
    """실제 통합 diff의 헝크를 이용해 파이프라인 방식으로 세그먼트를 생성함."""
    diff_text = "\n".join(
        difflib.unified_diff(old_en.splitlines(), new_en.splitlines(), lineterm="")
    )
    hunks = diff._parse_unified_diff(diff_text)  # noqa: SLF001
    return patch.build_plan(
        hunks,
        new_en,
        normalize_source=normalize_source,
        normalize_source_pair=normalize_source_pair,
    )


def _segments(old_en: str, new_en: str) -> list[patch.BlockChange]:
    """두 원문에서 번역 계획 세그먼트를 생성함."""

    return list(_plan(old_en, new_en).changes)


class CreatePatchPlanTests(unittest.TestCase):
    """`create` 패치 계획의 동작과 경계 조건을 검증함."""

    def test_create_plan_uses_atomic_owner_blocks_and_renders_deterministic_units(self):
        """신규 문서의 원자적 소유 블록 분류와 결정론적 단위 렌더링을 검증함."""

        source = (
            "---\nslug: guide\ntitle: Guide\n---\n\n"
            "<!-- source directive -->\n\n"
            "# Guide\n\n"
            "First paragraph.\n\n"
            "Second paragraph.\n\n"
            "- first item\n- second item\n\n"
            "> [!NOTE]\n> Note body.\n\n"
            "| A | B |\n|---|---|\n| x | y |\n\n"
            "```php\necho 'ok';\n```\n"
        )

        plan = patch.build_create_plan(source)

        self.assertIs(patch.plan_state(None, plan), patch.PlanState.CREATE)
        self.assertEqual(
            [block.kind for block in plan.create_blocks],
            [
                "frontmatter",
                "source_comment",
                "heading",
                "prose",
                "prose",
                "list",
                "admonition",
                "table",
                "code",
            ],
        )
        self.assertEqual(
            [block.kind for block in plan.create_blocks if block.provider_required],
            ["prose", "prose", "list", "admonition", "table"],
        )

        rendered = patch.apply_plan(
            None,
            plan,
            [
                "<!-- First paragraph. -->\n첫 문단.",
                "<!-- Second paragraph. -->\n둘째 문단.",
                "<!-- - first item - second item -->\n- 첫 항목\n- 둘째 항목",
                "> [!NOTE]\n> 참고 본문.",
                "| A | B |\n|---|---|\n| 가 | 나 |",
            ],
        )

        self.assertTrue(rendered.startswith("---\nslug: guide\ntitle: Guide\n---"))
        self.assertIn("<!-- source directive -->", rendered)
        self.assertIn("<!-- # Guide -->\n# Guide", rendered)
        self.assertIn("```php\necho 'ok';\n```", rendered)

    def test_create_plan_does_not_guess_split_for_one_large_owner_block(self):
        """분할할 수 없는 대형 소유 블록을 임의로 분리하지 않음."""

        source = ("word " * 5000).rstrip() + "\n"

        plan = patch.build_create_plan(source)

        self.assertEqual(len(plan.create_blocks), 1)
        self.assertEqual(plan.create_blocks[0].source, source)
        self.assertTrue(plan.create_blocks[0].provider_required)

    def test_create_plan_rejects_an_existing_destination(self):
        """이미 존재하는 로캘 대상에 대한 `create` 계획을 거부함."""

        plan = patch.build_create_plan("Paragraph.\n")

        with self.assertRaisesRegex(patch.PatchError, "create plan requires an absent"):
            patch.plan_state("", plan)

    def test_create_plan_rejects_unsupported_front_matter_values(self):
        """지원하지 않는 `front matter` 값이 있으면 `create` 계획을 거부함."""

        with self.assertRaisesRegex(patch.PatchError, "unsupported front matter"):
            patch.build_create_plan("---\ntags: [one, two]\n---\n\nParagraph.\n")

    def test_create_plan_accepts_yaml_block_string_scalars(self):
        """YAML 블록 문자열 스칼라를 포함한 `create` 계획을 허용함."""

        source = "---\ndescription: >-\n  A folded description.\n---\n\nParagraph.\n"

        plan = patch.build_create_plan(source)

        self.assertEqual(plan.create_blocks[0].kind, "frontmatter")
        self.assertFalse(plan.create_blocks[0].provider_required)

    def test_create_plan_rejects_a_ragged_table(self):
        """열 수가 일정하지 않은 표의 `create` 계획을 거부함."""

        source = "| A | B |\n|---|---|\n| only one |\n"

        with self.assertRaisesRegex(patch.PatchError, "rectangular"):
            patch.build_create_plan(source)

    def test_create_plan_rejects_an_unsupported_admonition_marker(self):
        """지원하지 않는 알림 표식이 있으면 `create` 계획을 거부함."""

        with self.assertRaisesRegex(patch.PatchError, "admonition marker"):
            patch.build_create_plan("> [!INFO]\n> Body.\n")

    def test_create_plan_ignores_admonition_examples_inside_fences(self):
        """펜스 코드 내부의 알림 예시를 구조로 오인하지 않음."""

        plan = patch.build_create_plan("```markdown\n> [!INFO]\n```\n")

        self.assertEqual([block.kind for block in plan.create_blocks], ["code"])


# 두 코드 블록 중 첫 번째만 `Exception`에서 `Throwable`로 변경함.
# 두 번째의 동일한 `use` 문은 변경 범위가 블록 안에 한정되는지 확인하는 데 사용함.
_OLD_EN = (
    '<a name="retry"></a>\n'
    "## Retrying Requests\n"
    "\n"
    "First paragraph describing the retry callback.\n"
    "\n"
    "```php\n"
    "use Exception;\n"
    "use App\\Support\\Helper;\n"
    "\n"
    "$response = retry(function (Exception $e) {\n"
    "    return true;\n"
    "});\n"
    "```\n"
    "\n"
    "Second paragraph that must stay untouched.\n"
    "\n"
    "```php\n"
    "use Exception;\n"
    "\n"
    "$other = keep(Exception::class);\n"
    "```\n"
)
_NEW_EN = _OLD_EN.replace(
    "use Exception;\nuse App\\Support\\Helper;\n\n$response = retry(function (Exception $e) {",
    "use Throwable;\nuse App\\Support\\Helper;\n\n$response = retry(function (Throwable $e) {",
)


class CodeBlockPatchTests(unittest.TestCase):
    """코드 블록 패치의 동작과 경계 조건을 검증함."""

    def test_interior_change_becomes_code_block_segment(self):
        """펜스 코드 내부 변경을 전체 코드 블록 세그먼트로 확장함."""

        segments = _segments(_OLD_EN, _NEW_EN)
        code = [s for s in segments if s.code_block is not None]
        self.assertEqual(len(code), 1)
        self.assertEqual(code[0].code_block.block_index, 0)
        self.assertFalse(code[0].needs_translation)

    def test_applies_change_scoped_to_the_right_block(self):
        # 기존 코드를 포함한 번역문에서도 첫 번째 블록만 변경 대상으로 삼음.
        """동일한 코드가 있어도 주소로 지정된 블록만 교체함."""

        result = patch.apply_segments(_OLD_EN, _segments(_OLD_EN, _NEW_EN), [])
        self.assertIn("$response = retry(function (Throwable $e) {", result)
        # 두 번째 블록은 변경하지 않아 동일한 줄을 그대로 보존함.
        self.assertIn("$other = keep(Exception::class);", result)
        self.assertEqual(result.count("use Exception;"), 1)
        # 적용 후 로캘 코드 블록이 검증 기준인 영어 원문과 일치하는지 확인함.
        self.assertEqual(
            verify._normalized_fenced_code_blocks(result),  # noqa: SLF001
            verify._normalized_fenced_code_blocks(_NEW_EN),  # noqa: SLF001
        )

    def test_apply_plan_rejects_diverged_code_state(self):
        """원문과 대상 어느 쪽에도 해당하지 않는 코드 상태의 적용을 거부함."""

        old = "```php\nfoo();\n```\n"
        new = "```php\nbar();\n```\n"
        diverged = "```php\nfoo();\n$local = 'custom';\n```\n"

        with self.assertRaisesRegex(patch.PatchError, "code block state"):
            patch.apply_plan(diverged, _plan(old, new), [])

    def test_apply_plan_canonicalizes_permuted_code_state(self):
        """순서만 바뀐 코드 블록 상태를 정규 형식으로 복원함."""

        old = "```php\nuse A;\nuse B;\n\nrun();\n```\n"
        new = old.replace("run();", "go();")
        permuted = "```php\nuse B;\nuse A;\n\nrun();\n```\n"
        plan = _plan(old, new)

        first = patch.apply_plan(permuted, plan, [])

        self.assertEqual(first, new)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_reapplying_permuted_fenced_insertion_is_a_noop(self):
        """순서가 바뀐 펜스 코드 삽입을 다시 적용할 때 변경 없음으로 판정함."""

        old = "Before.\n\nAfter.\n"
        inserted = "```php\nuse A;\nuse B;\n```"
        new = f"Before.\n\n{inserted}\n\nAfter.\n"
        existing = (
            "<!-- Before. -->\n앞입니다.\n\n"
            "```php\nuse B;\nuse A;\n```\n\n"
            "<!-- After. -->\n뒤입니다.\n"
        )

        result = patch.apply_plan(existing, _plan(old, new), [inserted])

        self.assertEqual(result, existing)

    def test_canonicalizes_block_when_translation_already_updated_and_reordered(self):
        # 이미 `Throwable`이 반영됐지만 `import` 순서가 다른 번역문도 오류 없이 영어 원문 순서로 복원해 검증을 통과함.
        """번역과 순서가 이미 바뀐 코드 블록을 정규 형식으로 복원함."""

        already = _NEW_EN.replace(
            "use Throwable;\nuse App\\Support\\Helper;",
            "use App\\Support\\Helper;\nuse Throwable;",
        )
        segments = _segments(_OLD_EN, _NEW_EN)
        result = patch.apply_segments(already, segments, [])
        self.assertEqual(
            verify._normalized_fenced_code_blocks(result),  # noqa: SLF001
            verify._normalized_fenced_code_blocks(_NEW_EN),  # noqa: SLF001
        )
        # 다시 적용한 뒤에도 추가 변경이 없는지 확인함.
        self.assertEqual(patch.apply_segments(result, segments, []), result)

    def test_pure_code_line_insertion_is_applied(self):
        """코드 줄만 추가된 변경을 적용함."""

        old = (
            "Intro paragraph.\n"
            "\n"
            "```php\n"
            "use Throwable;\n"
            "$response = run();\n"
            "```\n"
        )
        new = old.replace(
            "use Throwable;\n$response = run();",
            "use Throwable;\n$debug = config('app.debug');\n$response = run();",
        )
        result = patch.apply_segments(old, _segments(old, new), [])
        self.assertIn("$debug = config('app.debug');", result)
        self.assertEqual(
            verify._normalized_fenced_code_blocks(result),  # noqa: SLF001
            verify._normalized_fenced_code_blocks(new),  # noqa: SLF001
        )

    def test_blank_line_only_code_change_is_applied_idempotently(self):
        """빈 줄만 바뀐 코드 변경을 멱등적으로 적용함."""

        old = "```php\nfirst();\n\nsecond();\n```\n"
        new = "```php\nfirst();\nsecond();\n```\n"
        plan = _plan(old, new)

        self.assertEqual(len(plan.changes), 1)
        first = patch.apply_plan(old, plan, [])

        self.assertEqual(first, new)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_blank_line_splits_one_paragraph_into_two_blocks(self):
        """빈 줄 추가로 하나의 문단을 두 소유 블록으로 분리함."""

        old = "First line.\nSecond line.\n"
        new = "First line.\n\nSecond line.\n"
        existing = (
            "<!-- First line. Second line. -->\n"
            "첫째 줄과 둘째 줄입니다.\n"
        )
        translated = (
            "<!-- First line. -->\n첫째 줄입니다.\n\n"
            "<!-- Second line. -->\n둘째 줄입니다.\n"
        )
        plan = _plan(old, new)

        self.assertEqual(len(plan.changes), 1)
        first = patch.apply_plan(existing, plan, [translated])

        self.assertEqual(verify.verify(first, source=new), [])
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_deletes_a_whole_fenced_code_block_between_contexts(self):
        """두 문맥 사이의 펜스 코드 블록 전체를 삭제함."""

        old = "Before.\n\n```php\nremove();\n```\n\nAfter.\n"
        new = "Before.\n\nAfter.\n"
        existing = (
            "<!-- Before. -->\n앞입니다.\n\n"
            "```php\nremove();\n```\n\n"
            "<!-- After. -->\n뒤입니다.\n"
        )

        result = patch.apply_plan(existing, _plan(old, new), [])

        self.assertNotIn("remove();", result)
        self.assertEqual(verify.verify(result, source=new), [])
        self.assertEqual(patch.apply_plan(result, _plan(old, new), []), result)

    def test_reapplying_unannotated_structural_insertions_is_idempotent(self):
        """파이프라인 주석이 없는 구조 삽입을 멱등적으로 다시 적용함."""

        structures = (
            "```php\ninserted();\n```",
            "> New warning.",
            "- [Thing](#thing)",
        )
        for inserted in structures:
            with self.subTest(inserted=inserted):
                old = "Before.\n\nAfter.\n"
                new = f"Before.\n\n{inserted}\n\nAfter.\n"
                existing = (
                    "<!-- Before. -->\n앞입니다.\n\n"
                    "<!-- After. -->\n뒤입니다.\n"
                )
                plan = _plan(old, new)

                first = patch.apply_plan(existing, plan, [inserted])

                self.assertEqual(patch.apply_plan(first, plan, [inserted]), first)

    def test_rejects_a_whole_table_insertion_in_a_modified_document(self):
        """수정 문서에 표 전체를 삽입하는 변경을 거부함."""

        old = "Before.\n\nAfter.\n"
        new = (
            "Before.\n\n"
            "| Name | Value |\n| --- | --- |\n| New | 1 |\n\n"
            "After.\n"
        )

        with self.assertRaisesRegex(patch.PatchError, "exactly one"):
            _plan(old, new)

    def test_reapplying_fenced_insertions_at_document_edges_is_idempotent(self):
        """문서 양 끝의 펜스 코드 삽입을 멱등적으로 다시 적용함."""

        code = "```php\ninserted();\n```"
        cases = (
            (
                "After.\n",
                f"{code}\n\nAfter.\n",
                "<!-- After. -->\n뒤입니다.\n",
            ),
            (
                "Before.\n",
                f"Before.\n\n{code}\n",
                "<!-- Before. -->\n앞입니다.\n",
            ),
        )
        for old, new, existing in cases:
            with self.subTest(new=new):
                plan = _plan(old, new)
                first = patch.apply_plan(existing, plan, [code])

                self.assertEqual(patch.apply_plan(first, plan, [code]), first)

    def test_fenced_insertion_uses_prose_context_after_existing_code(self):
        """기존 코드 다음 삽입에서 산문 문맥을 사용함."""

        old = (
            "```php\nexisting();\n```\n\n"
            "Far one.\n\nFar two.\n\nBefore.\n\nAfter.\n"
        )
        inserted = "```php\ninserted();\n```"
        new = old.replace("Before.\n\nAfter.", f"Before.\n\n{inserted}\n\nAfter.")
        existing = (
            "```php\nexisting();\n```\n\n"
            "<!-- Far one. -->\n먼 하나입니다.\n\n"
            "<!-- Far two. -->\n먼 둘입니다.\n\n"
            "<!-- Before. -->\n앞입니다.\n\n"
            "<!-- After. -->\n뒤입니다.\n"
        )
        plan = _plan(old, new)

        result = patch.apply_plan(existing, plan, [inserted])

        self.assertLess(result.index("앞입니다."), result.index("inserted();"))
        self.assertLess(result.index("inserted();"), result.index("뒤입니다."))

    def test_fenced_insertion_uses_raw_context_after_existing_code(self):
        """기존 코드 다음 삽입에서 원시 문맥을 사용함."""

        old = (
            "```php\nexisting();\n```\n\n"
            "> Far one.\n\n> Far two.\n\n> Before.\n\n> After.\n"
        )
        inserted = "```php\ninserted();\n```"
        new = old.replace(
            "> Before.\n\n> After.",
            f"> Before.\n\n{inserted}\n\n> After.",
        )
        plan = _plan(old, new)

        result = patch.apply_plan(old, plan, [inserted])

        self.assertLess(result.index("> Before."), result.index("inserted();"))
        self.assertLess(result.index("inserted();"), result.index("> After."))

    def test_fenced_insertion_after_trailing_translated_admonition(self):
        """번역된 마지막 알림 블록 뒤에 펜스 코드를 삽입함."""

        old = "```php\nold();\n```\n\n> [!NOTE]\n> Keep this warning.\n"
        new = old + "\n```php\ninserted();\n```\n"
        existing = "```php\nold();\n```\n\n> [!NOTE]\n> 이 경고를 유지합니다.\n"
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, ["```php\ninserted();\n```\n"])

        self.assertLess(first.index("이 경고를"), first.index("inserted();"))
        self.assertEqual(
            patch.apply_plan(first, plan, ["```php\ninserted();\n```\n"]), first
        )

    def test_prose_code_insertion_stays_between_code_and_admonition(self):
        # 13.x `ai-sdk` 문서의 실제 형태: 닫는 펜스와 중복 알림 표식 사이에 문단과 코드를 함께 삽입함.
        # 코드 영역 창은 앞 예제와 뒤 알림 사이의 위치를 보존함.
        """코드와 알림 블록 사이의 산문·코드 삽입 위치를 보존함."""

        old = (
            "Intro.\n\n```php\nfirst();\n```\n\n> [!NOTE]\n> First note.\n\n"
            "```php\nsecond();\n```\n\n> [!NOTE]\n> Second note.\n"
        )
        new = old.replace(
            "> [!NOTE]\n> First note.",
            "More prose:\n\n```php\nthird();\n```\n\n> [!NOTE]\n> First note.",
            1,
        )
        hunk_text = (
            "@@ -3,6 +3,12 @@\n"
            " ```php\n"
            " first();\n"
            " ```\n"
            " \n"
            "+More prose:\n"
            "+\n"
            "+```php\n"
            "+third();\n"
            "+```\n"
            "+\n"
            " > [!NOTE]\n"
            " > First note.\n"
        )
        hunks = diff._parse_unified_diff(hunk_text)  # noqa: SLF001
        plan = patch.build_plan(hunks, new)
        translated = "<!-- More prose: -->\n더 많은 설명:\n\n```php\nthird();\n```"
        for first_note, second_note in (
            ("> [!NOTE]\n> 첫 메모입니다.", "> [!NOTE]\n> 둘째 메모입니다."),
            ("> **참고:** 첫 메모입니다.", "> **참고:** 둘째 메모입니다."),
        ):
            with self.subTest(note=first_note.splitlines()[0]):
                existing = (
                    "<!-- Intro. -->\n소개.\n\n```php\nfirst();\n```\n\n"
                    f"{first_note}\n\n"
                    "```php\nsecond();\n```\n\n"
                    f"{second_note}\n"
                )
                first = patch.apply_plan(existing, plan, [translated])

                self.assertLess(first.index("first();"), first.index("third();"))
                self.assertLess(first.index("third();"), first.index("첫 메모"))
                self.assertLess(first.index("첫 메모"), first.index("second();"))
                self.assertEqual(
                    patch.apply_plan(first, plan, [translated]), first
                )

    def test_insertion_extends_existing_code_block_region(self):
        # `diff` 정렬로 삽입 범위가 기존 블록의 닫는 펜스에서 시작하면 확장된 영역 앞에 그 블록이 그대로 포함됨.
        # 펜스 문맥에서 실패하지 않고 기존 로캘 블록을 제자리에서 교체함.
        """기존 코드 영역에 인접한 삽입 범위를 확장함."""

        old = "```php\nalpha();\nbeta();\n```\n\n> [!NOTE]\n> Tail note.\n"
        new = (
            "```php\nalpha();\nbeta();\n```\n\nAfter prose.\n\n"
            "```php\ngamma();\n```\n\n> [!NOTE]\n> Tail note.\n"
        )
        hunk_text = (
            "@@ -1,7 +1,13 @@\n"
            " ```php\n"
            " alpha();\n"
            " beta();\n"
            "+```\n"
            "+\n"
            "+After prose.\n"
            "+\n"
            "+```php\n"
            "+gamma();\n"
            " ```\n"
            " \n"
            " > [!NOTE]\n"
            " > Tail note.\n"
        )
        hunks = diff._parse_unified_diff(hunk_text)  # noqa: SLF001
        plan = patch.build_plan(hunks, new)
        existing = "```php\nalpha();\nbeta();\n```\n\n> [!NOTE]\n> 꼬리 메모입니다.\n"
        translated = (
            "```php\nalpha();\nbeta();\n```\n\n"
            "<!-- After prose. -->\n뒤 설명입니다.\n\n"
            "```php\ngamma();\n```"
        )

        first = patch.apply_plan(existing, plan, [translated])

        self.assertLess(first.index("beta();"), first.index("뒤 설명입니다."))
        self.assertLess(first.index("뒤 설명입니다."), first.index("gamma();"))
        self.assertLess(first.index("gamma();"), first.index("꼬리 메모"))
        self.assertEqual(patch.apply_plan(first, plan, [translated]), first)

    def test_fenced_code_insertion_is_provider_free(self):
        """펜스 코드만 삽입하는 변경을 `provider-free`로 판정함."""

        old = "Before.\n\nAfter.\n"
        new = "Before.\n\n```php\ninserted();\n```\n\nAfter.\n"

        plan = _plan(old, new)

        self.assertEqual(len(plan.changes), 1)
        self.assertTrue(plan.changes[0].provider_free)

    def test_fenced_code_inside_prose_insertion_requires_translation(self):
        """문단과 코드 블록이 섞인 삽입에는 번역 출력을 요구함."""

        old = "Before.\n\nAfter.\n"
        inserted = "## Added\n\nNew prose.\n\n```php\ninserted();\n```"
        new = f"Before.\n\n{inserted}\n\nAfter.\n"

        plan = _plan(old, new)

        self.assertEqual(len(plan.changes), 1)
        self.assertFalse(plan.changes[0].provider_free)
        self.assertEqual(patch.source_text(plan.changes[0]), f"{inserted}\n")

    def test_renames_the_selected_duplicate_named_anchor_provider_free(self):
        """중복 이름 앵커 중 선택된 항목의 이름 변경을 `provider-free`로 적용함."""

        old = (
            '<a name="same"></a>\nFirst.\n\n'
            '<a name="same"></a>\nSecond.\n'
        )
        new = (
            '<a name="same"></a>\nFirst.\n\n'
            '<a name="second"></a>\nSecond.\n'
        )
        existing = (
            '<a name="same"></a>\n'
            '<!-- First. -->\n첫째입니다.\n\n'
            '<a name="same"></a>\n'
            '<!-- Second. -->\n둘째입니다.\n'
        )
        translated = '<a name="second"></a>'
        plan = _plan(old, new)

        self.assertTrue(plan.changes[0].provider_free)
        first = patch.apply_plan(existing, plan, [translated])

        self.assertEqual(first.count('<a name="same"></a>'), 1)
        self.assertEqual(first.count('<a name="second"></a>'), 1)
        self.assertIn('<a name="same"></a>\n<!-- First. -->', first)
        self.assertIn('<a name="second"></a>\n<!-- Second. -->', first)
        self.assertEqual(patch.apply_plan(first, plan, [translated]), first)

    def test_inserts_and_deletes_named_anchors_provider_free(self):
        """이름 앵커 삽입과 삭제를 `provider-free`로 적용함."""

        anchor = '<a name="middle"></a>'
        old = "Before.\n\nAfter.\n"
        new = f"Before.\n\n{anchor}\nAfter.\n"
        existing = (
            "<!-- Before. -->\n앞입니다.\n\n"
            "<!-- After. -->\n뒤입니다.\n"
        )

        insertion = _plan(old, new)
        self.assertTrue(insertion.changes[0].provider_free)
        inserted = patch.apply_plan(existing, insertion, [anchor])

        self.assertIn(f"앞입니다.\n\n{anchor}\n", inserted)
        self.assertEqual(patch.apply_plan(inserted, insertion, [anchor]), inserted)

        deletion = _plan(new, old)
        deleted = patch.apply_plan(inserted, deletion, [])

        self.assertNotIn(anchor, deleted)
        self.assertEqual(patch.apply_plan(deleted, deletion, []), deleted)

    def test_insertion_preserves_blank_line_before_raw_anchor_context(self):
        """원시 앵커 문맥 앞에 삽입할 때 빈 줄을 보존함."""

        anchor = '<a name="section-1"></a>'
        old = f"{anchor}\n## Section 1\n"
        new = f"Paragraph 99.\n\n{anchor}\n## Section 1\n"
        existing = (
            f"{anchor}\n"
            "<!-- ## Section 1 -->\n"
            "## Section 1\n"
        )
        translated = "<!-- Paragraph 99. -->\n문단 99."
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])

        self.assertIn(f"문단 99.\n\n{anchor}", first)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_deletes_the_selected_duplicate_named_anchor(self):
        """중복 이름 앵커 중 선택된 항목을 삭제함."""

        anchor = '<a name="same"></a>'
        old = f"{anchor}\nFirst.\n\n{anchor}\nSecond.\n"
        new = f"{anchor}\nFirst.\n\nSecond.\n"
        existing = (
            f"{anchor}\n<!-- First. -->\n첫째입니다.\n\n"
            f"{anchor}\n<!-- Second. -->\n둘째입니다.\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [])

        self.assertEqual(first.count(anchor), 1)
        self.assertIn(f"{anchor}\n<!-- First. -->", first)
        self.assertIn("<!-- Second. -->", first)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_deleting_duplicate_anchor_rejects_position_drift(self):
        """중복 앵커의 삭제 위치가 분기된 상태를 거부함."""

        old = (
            '<a name="dup"></a>\n## Section One\n\nOne body.\n\n'
            '<a name="dup"></a>\n## Section Two\n\nTwo body.\n'
        )
        new = old.replace('<a name="dup"></a>\n## Section One', "## Section One", 1)
        drifted = (
            '<a name="dup"></a>\n<!-- ## Section One -->\n## 섹션 하나\n\n'
            "<!-- One body. -->\n하나 본문.\n\n"
            '<!-- ## Section Two -->\n## 섹션 둘\n\n'
            "<!-- Two body. -->\n둘 본문.\n"
        )

        with self.assertRaisesRegex(patch.PatchError, "source position"):
            patch.apply_plan(drifted, _plan(old, new), [])

    def test_deleting_duplicate_anchor_moves_the_correct_occurrence(self):
        """중복 앵커 중 구조 주소가 가리키는 항목만 삭제함."""

        old = (
            '<a name="dup"></a>\n## Section One\n\nOne body.\n\n'
            '<a name="dup"></a>\n## Section Two\n\nTwo body.\n'
        )
        new = old.replace('<a name="dup"></a>\n## Section One', "## Section One", 1)
        plan = _plan(old, new)
        existing = (
            '<a name="dup"></a>\n<!-- ## Section One -->\n## 섹션 하나\n\n'
            "<!-- One body. -->\n하나 본문.\n\n"
            '<a name="dup"></a>\n<!-- ## Section Two -->\n## 섹션 둘\n\n'
            "<!-- Two body. -->\n둘 본문.\n"
        )

        first = patch.apply_plan(existing, plan, [])

        self.assertEqual(first.count('<a name="dup"></a>'), 1)
        self.assertLess(first.index("하나 본문"), first.index('<a name="dup"></a>'))
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_anchor_insertion_count_at_wrong_position_fails_closed(self):
        """잘못된 위치에 같은 수의 앵커가 있으면 삽입을 거부함."""

        old = "## Section One\n\nOne body.\n\n## Section Two\n\nTwo body.\n"
        new = old.replace("## Section Two", '<a name="dup"></a>\n## Section Two')
        misplaced = (
            '<a name="dup"></a>\n<!-- ## Section One -->\n## 섹션 하나\n\n'
            "<!-- One body. -->\n하나 본문.\n\n"
            '<!-- ## Section Two -->\n## 섹션 둘\n\n'
            "<!-- Two body. -->\n둘 본문.\n"
        )

        with self.assertRaisesRegex(patch.PatchError, "placement"):
            patch.apply_plan(misplaced, _plan(old, new), ['<a name="dup"></a>'])

    def test_deletes_fenced_blocks_at_document_edges(self):
        """문서 양 끝의 펜스 코드 블록을 삭제함."""

        code = "```php\nremove();\n```"
        cases = (
            (
                f"{code}\n\nAfter.\n",
                "After.\n",
                f"{code}\n\n<!-- After. -->\n뒤입니다.\n",
            ),
            (
                f"Before.\n\n{code}\n",
                "Before.\n",
                f"<!-- Before. -->\n앞입니다.\n\n{code}\n",
            ),
        )
        for old, new, existing in cases:
            with self.subTest(old=old):
                plan = _plan(old, new)
                first = patch.apply_plan(existing, plan, [])

                self.assertNotIn("remove();", first)
                self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_pure_code_line_deletion_is_applied(self):
        """코드 줄만 삭제된 변경을 적용함."""

        old = (
            "Intro paragraph.\n"
            "\n"
            "```php\n"
            "use Throwable;\n"
            "$debug = config('app.debug');\n"
            "$response = run();\n"
            "```\n"
        )
        new = old.replace("use Throwable;\n$debug = config('app.debug');\n", "use Throwable;\n")
        result = patch.apply_segments(old, _segments(old, new), [])
        self.assertNotIn("$debug = config('app.debug');", result)
        self.assertEqual(
            verify._normalized_fenced_code_blocks(result),  # noqa: SLF001
            verify._normalized_fenced_code_blocks(new),  # noqa: SLF001
        )

    def test_normalized_indented_code_change_becomes_code_change(self):
        """정규화된 들여쓰기 코드 변경을 코드 세그먼트로 변환함."""

        old = "Before.\n\n    old();\n\nAfter.\n"
        new = "Before.\n\n    new();\n\nAfter.\n"
        existing = (
            "<!-- Before. -->\n앞입니다.\n\n"
            "```\nold();\n```\n\n"
            "<!-- After. -->\n뒤입니다.\n"
        )
        normalizer = lambda source: preprocess.preprocess(source).text
        plan = _plan(old, new, normalize_source=normalizer)

        self.assertEqual(len(plan.changes), 1)
        self.assertIsNotNone(plan.changes[0].code_block)

        first = patch.apply_plan(existing, plan, [])

        self.assertIn("```\nnew();\n```", first)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_code_edit_uses_old_index_before_front_code_insertion(self):
        """선행 코드 삽입 전 인덱스로 기존 코드 변경을 주소화함."""

        old = (
            "Intro.\n\n"
            "Middle one.\n\nMiddle two.\n\nMiddle three.\n\n"
            "```php\nold();\n```\n\nAfter.\n"
        )
        inserted = "```php\nfront();\n```"
        new = old.replace("Intro.\n", f"Intro.\n\n{inserted}\n").replace(
            "```php\nold();\n```", "```php\nnew();\n```"
        )
        existing = (
            "<!-- Intro. -->\n도입입니다.\n\n"
            "<!-- Middle one. -->\n중간 하나.\n\n"
            "<!-- Middle two. -->\n중간 둘.\n\n"
            "<!-- Middle three. -->\n중간 셋.\n\n"
            "```php\nold();\n```\n\n"
            "<!-- After. -->\n뒤입니다.\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [inserted])

        self.assertEqual(
            verify._normalized_fenced_code_blocks(first),  # noqa: SLF001
            verify._normalized_fenced_code_blocks(new),  # noqa: SLF001
        )
        self.assertEqual(patch.apply_plan(first, plan, [inserted]), first)

    def test_code_edit_does_not_use_duplicate_at_new_index(self):
        """코드 변경에서 신규 인덱스의 다른 중복 블록을 사용하지 않음."""

        old = (
            "Intro.\n\n"
            "Middle one.\n\nMiddle two.\n\nMiddle three.\n\n"
            "```php\nold();\n```\n\n"
            "Between code blocks.\n\n"
            "```php\nnew();\n```\n\nAfter.\n"
        )
        inserted = "```php\nfront();\n```"
        new = old.replace("Intro.\n", f"Intro.\n\n{inserted}\n").replace(
            "```php\nold();\n```", "```php\nnew();\n```"
        )
        existing = (
            "<!-- Intro. -->\n도입입니다.\n\n"
            "<!-- Middle one. -->\n중간 하나.\n\n"
            "<!-- Middle two. -->\n중간 둘.\n\n"
            "<!-- Middle three. -->\n중간 셋.\n\n"
            "```php\nold();\n```\n\n"
            "<!-- Between code blocks. -->\n코드 블록 사이.\n\n"
            "```php\nnew();\n```\n\n"
            "<!-- After. -->\n뒤입니다.\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [inserted])

        self.assertEqual(
            verify._normalized_fenced_code_blocks(first),  # noqa: SLF001
            verify._normalized_fenced_code_blocks(new),  # noqa: SLF001
        )
        self.assertEqual(patch.apply_plan(first, plan, [inserted]), first)

    def test_shifted_code_insertion_stays_between_annotated_blocks(self):
        """이동된 코드 삽입을 두 파이프라인 주석 블록 사이에 유지함."""

        old = (
            "Intro.\n\nBefore insertion.\n\nAfter insertion.\n\n"
            "Gap one.\n\nGap two.\n\nGap three.\n\n"
            "```php\nB();\n```\n\nAfter.\n"
        )
        inserted = "```php\nC();\n```"
        new = old.replace(
            "Before insertion.\n", f"Before insertion.\n\n{inserted}\n"
        ).replace("```php\nB();\n```", "```php\nC();\n```")
        existing = (
            "<!-- Intro. -->\nIntro.\n\n"
            "<!-- Before insertion. -->\nBefore insertion.\n\n"
            "<!-- After insertion. -->\nAfter insertion.\n\n"
            "<!-- Gap one. -->\nGap one.\n\n"
            "<!-- Gap two. -->\nGap two.\n\n"
            "<!-- Gap three. -->\nGap three.\n\n"
            "```php\nB();\n```\n\n"
            "<!-- After. -->\nAfter.\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [inserted])

        self.assertIn(
            "<!-- Before insertion. -->\nBefore insertion.\n\n"
            "```php\nC();\n```\n\n"
            "<!-- After insertion. -->\nAfter insertion.",
            first,
        )
        self.assertEqual(patch.apply_plan(first, plan, [inserted]), first)

    def test_deletes_one_of_adjacent_fenced_code_blocks(self):
        """인접한 펜스 코드 블록 중 선택된 하나만 삭제함."""

        old = (
            "Intro.\n\n```php\nA();\n```\n\n```php\nC();\n```\n\n"
            "```php\nB();\n```\n\nAfter.\n"
        )
        new = (
            "Intro.\n\n```php\nA();\n```\n\n```php\nB();\n```\n\nAfter.\n"
        )
        existing = (
            "<!-- Intro. -->\nIntro.\n\n```php\nA();\n```\n\n"
            "```php\nC();\n```\n\n```php\nB();\n```\n\n"
            "<!-- After. -->\nAfter.\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [])

        self.assertEqual(
            verify._normalized_fenced_code_blocks(first),  # noqa: SLF001
            verify._normalized_fenced_code_blocks(new),  # noqa: SLF001
        )
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_ambiguous_shifted_code_change_fails_safe_without_plan_state(self):
        """위치가 이동해 모호해진 코드 변경의 계획 상태 판정을 거부함."""

        old_block = "```php\nA();\n```"
        new_block = "```php\nB();\n```"
        target = f"{new_block}\n\n{old_block}\n"
        change = patch.CodeChange(
            block_index=0,
            new_block=new_block,
            anchors=("```php", "```"),
            old_block_index=1,
            old_block=old_block,
            old_block_count=2,
            new_block_count=2,
        )

        self.assertEqual(patch._apply_code_block(target, change), target)  # noqa: SLF001

    def test_code_edit_uses_old_index_before_front_code_deletion(self):
        """선행 코드 삭제 전 인덱스로 기존 코드 변경을 주소화함."""

        removed = "```php\nfront();\n```"
        old = (
            f"Intro.\n\n{removed}\n\n"
            "Middle one.\n\nMiddle two.\n\nMiddle three.\n\n"
            "```php\nold();\n```\n\nAfter.\n"
        )
        new = old.replace(f"\n{removed}\n", "\n").replace(
            "```php\nold();\n```", "```php\nnew();\n```"
        )
        existing = (
            "<!-- Intro. -->\n도입입니다.\n\n"
            f"{removed}\n\n"
            "<!-- Middle one. -->\n중간 하나.\n\n"
            "<!-- Middle two. -->\n중간 둘.\n\n"
            "<!-- Middle three. -->\n중간 셋.\n\n"
            "```php\nold();\n```\n\n"
            "<!-- After. -->\n뒤입니다.\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [])

        self.assertEqual(
            verify._normalized_fenced_code_blocks(first),  # noqa: SLF001
            verify._normalized_fenced_code_blocks(new),  # noqa: SLF001
        )
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_code_fence_replacement_uses_complete_source_region(self):
        """코드 펜스 교체에서 완전한 원문 영역을 사용함."""

        old = (
            "### Storing Payment Methods\n\n"
            "Old setup instructions.\n\n"
            "```js\n"
            "confirmCardSetup();\n"
            "```\n\n"
            '<a name="next"></a>\n'
            "### Next\n"
        )
        new = (
            "### Storing Payment Methods\n\n"
            "New setup instructions.\n\n"
            "```php\n"
            "use Illuminate\\Http\\Request;\n"
            "\n"
            "Route::get('/subscription/complete', function (Request $request) {\n"
            "    return redirect('/dashboard');\n"
            "});\n"
            "```\n\n"
            '<a name="next"></a>\n'
            "### Next\n"
        )

        segments = _segments(old, new)
        translated = patch.source_text(segments[0])

        self.assertEqual(len(segments), 1)
        self.assertEqual(translated.count("```"), 2)
        self.assertIn("Route::get('/subscription/complete'", translated)
        self.assertNotIn('<a name="next"></a>', translated)

    def test_diverged_block_is_left_untouched_not_corrupted(self):
        # 주소로 지정된 블록에 변경 표식이 없으면 수정하지 않음.
        """분기된 로캘 블록을 손상하지 않도록 적용을 거부함."""

        diverged = _OLD_EN.replace(
            "use Exception;\n"
            "use App\\Support\\Helper;\n"
            "\n"
            "$response = retry(function (Exception $e) {\n"
            "    return true;\n"
            "});",
            "echo 'totally unrelated block';",
        )
        result = patch.apply_segments(diverged, _segments(_OLD_EN, _NEW_EN), [])
        self.assertIn("echo 'totally unrelated block';", result)

    def test_replaces_paragraph_between_nearest_raw_contexts_when_old_comment_is_gone(self):
        """이전 파이프라인 주석이 없을 때 가장 가까운 원시 문맥 사이의 문단을 교체함."""

        old = (
            "## PHP Versions\n\n"
            "The default PHP version is PHP 8.4.\n\n"
            "```yaml\n"
            "context: ./vendor/laravel/sail/runtimes/8.4\n"
            "```\n"
        )
        new = old.replace("PHP 8.4.", "PHP 8.5.")
        existing = (
            "```yaml\n"
            "unrelated: true\n"
            "```\n\n"
            "<!-- ## PHP Versions -->\n"
            "## PHP Versions\n\n"
            "<!-- The default PHP version is PHP 8.5. -->\n"
            "기본 PHP 버전은 PHP 8.5입니다.\n\n"
            "```yaml\n"
            "context: ./vendor/laravel/sail/runtimes/8.4\n"
            "```\n"
        )
        translated = (
            "<!-- The default PHP version is PHP 8.5. -->\n"
            "기본 PHP 버전은 PHP 8.5입니다.\n"
        )

        segments = _segments(old, new)
        self.assertIn("기본 PHP 버전", patch.existing_context(existing, segments[0]))
        self.assertEqual(
            patch.apply_segments(existing, segments, [translated]),
            existing,
        )

    def test_replaces_mixed_code_tail_and_deleted_paragraph_by_nearest_contexts(self):
        """혼합된 코드 꼬리와 삭제 문단을 가장 가까운 문맥으로 교체함."""

        existing = (
            "```php\n"
            "class Earlier\n"
            "{\n"
            "}\n"
            "```\n\n"
            "<!-- Before text. -->\n"
            "앞 문단입니다.\n\n"
            "```js\n"
            "if (error) {\n"
            "    show(error);\n"
            "} else {\n"
            "    done();\n"
            "}\n"
            "});\n"
            "```\n\n"
            "<!-- Old paragraph. -->\n"
            "예전 문단입니다.\n\n"
            '<a name="next"></a>\n'
            "<!-- ## Next -->\n"
            "## Next\n"
        )
        segment = patch.BlockChange(
            old_lines=("});", "```", "Old paragraph."),
            new_lines=(
                "    return redirect('/dashboard');",
                "})->name('payment.complete');",
                "```",
            ),
            before_context="}",
            after_context='<a name="next"></a>',
            new_source=(
                "    return redirect('/dashboard');\n"
                "})->name('payment.complete');\n"
                "```\n"
            ),
        )
        translated = (
            "    return redirect('/dashboard');\n"
            "})->name('payment.complete');\n"
            "```\n"
        )
        expected = (
            "```php\n"
            "class Earlier\n"
            "{\n"
            "}\n"
            "```\n\n"
            "<!-- Before text. -->\n"
            "앞 문단입니다.\n\n"
            "```js\n"
            "if (error) {\n"
            "    show(error);\n"
            "} else {\n"
            "    done();\n"
            "}\n"
            "    return redirect('/dashboard');\n"
            "})->name('payment.complete');\n"
            "```\n\n"
            '<a name="next"></a>\n'
            "<!-- ## Next -->\n"
            "## Next\n"
        )

        self.assertIn("예전 문단입니다.", patch.existing_context(existing, segment))
        self.assertEqual(patch.apply_segments(existing, [segment], [translated]), expected)

    def test_replaces_existing_inserted_anchor_section_instead_of_duplicating_it(self):
        """이미 삽입된 앵커 절을 중복 생성 없이 교체함."""

        old = (
            '<a name="next"></a>\n'
            "## Next\n"
        )
        new = (
            '<a name="inserted"></a>\n'
            "#### Inserted\n\n"
            "Inserted paragraph.\n\n"
            "```php\n"
            "example();\n"
            "```\n\n"
            '<a name="next"></a>\n'
            "## Next\n"
        )
        existing = (
            '<a name="inserted"></a>\n'
            "<!-- #### Inserted -->\n"
            "#### Inserted\n\n"
            "<!-- Inserted paragraph. -->\n"
            "삽입된 문단입니다.\n\n"
            "```php\n"
            "example();\n"
            "```\n\n"
            '<a name="next"></a>\n'
            "<!-- ## Next -->\n"
            "## Next\n"
        )
        translated = (
            '<a name="inserted"></a>\n'
            "<!-- #### Inserted -->\n"
            "#### Inserted\n\n"
            "<!-- Inserted paragraph. -->\n"
            "삽입된 문단입니다.\n\n"
            "```php\n"
            "example();\n"
            "```\n"
        )

        result = patch.apply_segments(existing, _segments(old, new), [translated])

        self.assertEqual(result.count('<a name="inserted"></a>'), 1)
        self.assertEqual(
            verify._normalized_fenced_code_blocks(result),  # noqa: SLF001
            verify._normalized_fenced_code_blocks(new),  # noqa: SLF001
        )
        self.assertEqual(result, existing)

    def test_replaces_annotated_paragraph_and_following_code_block_before_common_context(self):
        """공통 문맥 앞의 파이프라인 주석 문단과 뒤의 코드 블록 교체를 검증함."""

        old = (
            "```php\n"
            "'redis' => [\n"
            "],\n"
            "```\n\n"
            "```php\n"
            "'unrelated' => [\n"
            "    'prefix' => 'app',\n"
            "],\n"
            "```\n\n"
            "Predis supports retry configuration via the `Retry` class:\n\n"
            "```php\n"
            "use Predis\\Retry;\n"
            "use Predis\\Retry\\Strategy\\ExponentialBackoff;\n\n"
            "'default' => [\n"
            "    'retry' => new Retry(\n"
            "        new ExponentialBackoff(\n"
            "            true, // Enables jitter\n"
            "        ),\n"
            "    )\n"
            "],\n"
            "```\n\n"
            '<a name="after"></a>\n'
            "## After\n"
        )
        new = (
            "```php\n"
            "'redis' => [\n"
            "],\n"
            "```\n\n"
            "```php\n"
            "'unrelated' => [\n"
            "    'prefix' => 'app',\n"
            "],\n"
            "```\n\n"
            "Predis supports retry configuration via the `Retry` class. "
            "Configure the `retry` and `max_retries` options:\n\n"
            "```php\n"
            "use Predis\\Retry\\Strategy\\ExponentialBackoff;\n\n"
            "'default' => [\n"
            "    'retry' => [\n"
            "        ExponentialBackoff::class => [\n"
            "            true, // Enable jitter...\n"
            "        ],\n"
            "    ],\n"
            "    'max_retries' => env('REDIS_MAX_RETRIES', 3),\n"
            "],\n"
            "```\n\n"
            "Cluster retries can be configured in `parameters`:\n\n"
            "```php\n"
            "'parameters' => [\n"
            "    'max_retries' => env('REDIS_MAX_RETRIES', 3),\n"
            "],\n"
            "```\n\n"
            '<a name="after"></a>\n'
            "## After\n"
        )
        existing = (
            "```php\n"
            "'redis' => [\n"
            "],\n"
            "```\n\n"
            "```php\n"
            "'unrelated' => [\n"
            "    'prefix' => 'app',\n"
            "],\n"
            "```\n\n"
            "<!-- Predis supports retry configuration via the `Retry` class: -->\n"
            "Predis는 `Retry` 클래스로 재시도 설정을 지원합니다.\n\n"
            "```php\n"
            "use Predis\\Retry;\n"
            "use Predis\\Retry\\Strategy\\ExponentialBackoff;\n\n"
            "'default' => [\n"
            "    'retry' => new Retry(\n"
            "        new ExponentialBackoff(\n"
            "            true, // Enables jitter\n"
            "        ),\n"
            "    )\n"
            "],\n"
            "```\n\n"
            '<a name="after"></a>\n'
            "<!-- ## After -->\n"
            "## After\n"
        )
        translated = (
            "<!-- Predis supports retry configuration via the `Retry` class. "
            "Configure the `retry` and `max_retries` options: -->\n"
            "Predis는 `Retry`, `retry`, `max_retries` 옵션으로 재시도를 설정합니다.\n\n"
            "```php\n"
            "use Predis\\Retry\\Strategy\\ExponentialBackoff;\n\n"
            "'default' => [\n"
            "    'retry' => [\n"
            "        ExponentialBackoff::class => [\n"
            "            true, // Enable jitter...\n"
            "        ],\n"
            "    ],\n"
            "    'max_retries' => env('REDIS_MAX_RETRIES', 3),\n"
            "],\n"
            "```\n\n"
            "<!-- Cluster retries can be configured in `parameters`: -->\n"
            "클러스터 재시도는 `parameters`에서 설정할 수 있습니다.\n\n"
            "```php\n"
            "'parameters' => [\n"
            "    'max_retries' => env('REDIS_MAX_RETRIES', 3),\n"
            "],\n"
            "```\n"
        )

        result = patch.apply_segments(existing, _segments(old, new), [translated])

        self.assertIn("Predis는 `Retry`, `retry`, `max_retries`", result)
        self.assertIn('<a name="after"></a>', result)
        self.assertNotIn("use Predis\\Retry;\n", result)
        self.assertEqual(result.count("'redis' => ["), 1)
        self.assertEqual(result.count("## After"), 2)
        self.assertEqual(
            verify._normalized_fenced_code_blocks(result),  # noqa: SLF001
            verify._normalized_fenced_code_blocks(new),  # noqa: SLF001
        )


class PatchTests(unittest.TestCase):
    """`patch` 동작과 경계 조건을 검증함."""

    def test_moves_named_anchor_sections_without_retranslation(self):
        """이름 앵커 절을 재번역 없이 이동함."""

        alpha = (
            '<a name="alpha"></a>\n'
            "## Alpha\n\n"
            "Alpha body.\n\n"
            "```php\n"
            "alpha();\n"
            "```\n"
        )
        beta = (
            '<a name="beta"></a>\n'
            "## Beta\n\n"
            "Beta body.\n\n"
            "```php\n"
            "beta();\n"
            "```\n"
        )
        old = f"{alpha}\n{beta}"
        new = f"{beta}\n{alpha}"
        existing_alpha = (
            '<a name="alpha"></a>\n'
            "<!-- ## Alpha -->\n"
            "## Alpha\n\n"
            "<!-- Alpha body. -->\n"
            "알파 본문.\n\n"
            "```php\n"
            "alpha();\n"
            "```\n"
        )
        existing_beta = (
            '<a name="beta"></a>\n'
            "<!-- ## Beta -->\n"
            "## Beta\n\n"
            "<!-- Beta body. -->\n"
            "베타 본문.\n\n"
            "```php\n"
            "beta();\n"
            "```\n"
        )
        existing = f"{existing_alpha}\n{existing_beta}"
        expected = f"{existing_beta}\n{existing_alpha}"
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [])

        self.assertEqual(first, expected)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_section_move_normalizes_a_missing_eof_newline_once(self):
        """절 이동 시 누락된 파일 끝 개행을 한 번만 복원함."""

        old = (
            '<a name="alpha"></a>\n## Alpha\n\n'
            '<a name="beta"></a>\n## Beta\n\n'
            '<a name="gamma"></a>\n## Gamma\n'
        )
        new = (
            '<a name="beta"></a>\n## Beta\n\n'
            '<a name="alpha"></a>\n## Alpha\n\n'
            '<a name="gamma"></a>\n## Gamma\n'
        )
        existing = (
            '<a name="alpha"></a>\n<!-- ## Alpha -->\n## Alpha\n\n'
            '<a name="beta"></a>\n<!-- ## Beta -->\n## Beta\n\n'
            '<a name="gamma"></a>\n<!-- ## Gamma -->\n## Gamma'
        )
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [])

        self.assertTrue(first.endswith("\n"))
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_moves_unique_named_sections_with_legacy_annotation_shape(self):
        """기존 주석 형식으로 식별한 고유 이름 절을 이동함."""

        alpha = '<a name="alpha"></a>\n## Alpha\n\nAlpha body.\n'
        beta = '<a name="beta"></a>\n## Beta\n\nBeta body.\n'
        old = f"{alpha}\n{beta}"
        new = f"{beta}\n{alpha}"
        existing_alpha = (
            '<a name="alpha"></a>\n'
            "<!-- ## Alpha -->\n## Alpha\n\n"
            "<!-- Alpha body. </div> -->\n알파 본문.\n"
        )
        existing_beta = (
            '<a name="beta"></a>\n'
            "<!-- ## Beta -->\n## Beta\n\n"
            "<!-- Beta body. -->\n베타 본문.\n"
        )
        existing = f"{existing_alpha}\n{existing_beta}"
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [])

        self.assertEqual(first, f"{existing_beta}\n{existing_alpha}")
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_unique_named_section_reorder_rejects_crossed_annotation_ownership(self):
        """서로 교차한 주석 소유권을 가진 이름 절의 이동을 거부함."""

        old = (
            '<a name="a"></a>\n## A\n\nA body.\n\n'
            '<a name="b"></a>\n## B\n\nB body.\n'
        )
        new = (
            '<a name="b"></a>\n## B\n\nB body.\n\n'
            '<a name="a"></a>\n## A\n\nA body.\n'
        )
        existing = (
            '<a name="a"></a>\n<!-- ## A -->\n## A\n\n'
            '<!-- B body. -->\n에이 번역.\n\n'
            '<a name="b"></a>\n<!-- ## B -->\n## B\n\n'
            '<!-- A body. -->\n비 번역.\n'
        )
        plan = _plan(old, new)

        with self.assertRaisesRegex(patch.PatchError, "neither source nor target"):
            patch.apply_plan(existing, plan, [])

    def test_moves_repeated_named_anchors_by_their_annotation_signature(self):
        """반복된 이름 앵커를 주석 서명에 따라 이동함."""

        alpha = '<a name="same"></a>\n## Alpha\n\nAlpha body.\n'
        beta = '<a name="same"></a>\n## Beta\n\nBeta body.\n'
        old = f"{alpha}\n{beta}"
        new = f"{beta}\n{alpha}"
        existing_alpha = (
            '<a name="same"></a>\n'
            "<!-- ## Alpha -->\n## Alpha\n\n"
            "<!-- Alpha body. -->\n알파 본문.\n"
        )
        existing_beta = (
            '<a name="same"></a>\n'
            "<!-- ## Beta -->\n## Beta\n\n"
            "<!-- Beta body. -->\n베타 본문.\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(
            f"{existing_alpha}\n{existing_beta}",
            plan,
            [],
        )

        self.assertEqual(first, f"{existing_beta}\n{existing_alpha}")
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_named_section_reorder_preserves_moved_source_comments(self):
        """이름 절 이동 시 함께 이동한 원문 주석을 보존함."""

        alpha = (
            '<a name="a"></a>\n## A\n\n'
            "<!-- directive-a -->\n\nA body.\n"
        )
        beta = (
            '<a name="b"></a>\n## B\n\n'
            "<!-- directive-b -->\n\nB body.\n"
        )
        old = f"{alpha}\n{beta}"
        new = f"{beta}\n{alpha}"
        existing_alpha = (
            '<a name="a"></a>\n<!-- ## A -->\n## A\n\n'
            "<!-- directive-a -->\n\n<!-- A body. -->\n에이.\n"
        )
        existing_beta = (
            '<a name="b"></a>\n<!-- ## B -->\n## B\n\n'
            "<!-- directive-b -->\n\n<!-- B body. -->\n비.\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(
            f"{existing_alpha}\n{existing_beta}",
            plan,
            [],
        )

        self.assertEqual(first, f"{existing_beta}\n{existing_alpha}")
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_named_section_reorder_accepts_matching_toc_permutation(self):
        """이름 절 순서와 일치하는 목차 순열을 허용함."""

        old = (
            "# Doc\n\n- [Alpha](#alpha)\n- [Beta](#beta)\n\n"
            '<a name="alpha"></a>\n## Alpha\n\nAlpha body.\n\n'
            '<a name="beta"></a>\n## Beta\n\nBeta body.\n'
        )
        new = (
            "# Doc\n\n- [Beta](#beta)\n- [Alpha](#alpha)\n\n"
            '<a name="beta"></a>\n## Beta\n\nBeta body.\n\n'
            '<a name="alpha"></a>\n## Alpha\n\nAlpha body.\n'
        )
        plan = _plan(old, new)
        self.assertIsNotNone(plan.named_section_reorder)
        self.assertEqual(plan.changes, ())
        existing = (
            "# 문서\n\n- [알파](#alpha)\n- [베타](#beta)\n\n"
            '<a name="alpha"></a>\n<!-- ## Alpha -->\n## 알파\n\n'
            "<!-- Alpha body. -->\n알파 본문.\n\n"
            '<a name="beta"></a>\n<!-- ## Beta -->\n## 베타\n\n'
            "<!-- Beta body. -->\n베타 본문.\n"
        )

        first = patch.apply_plan(existing, plan, [])

        self.assertLess(first.index("## 베타"), first.index("## 알파"))
        self.assertLess(
            first.index("- [베타](#beta)"), first.index("- [알파](#alpha)")
        )
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_named_section_reorder_rejects_unrelated_prefix_changes(self):
        """이름 절 이동과 무관한 문서 접두부 변경을 거부함."""

        old = (
            "# Doc\n\n- [Alpha](#alpha)\n- [Beta](#beta)\n\n"
            '<a name="alpha"></a>\n## Alpha\n\nAlpha body.\n\n'
            '<a name="beta"></a>\n## Beta\n\nBeta body.\n'
        )
        swapped = (
            "# Doc\n\n- [Beta](#beta)\n- [Alpha](#alpha)\n\n"
            '<a name="beta"></a>\n## Beta\n\nBeta body.\n\n'
            '<a name="alpha"></a>\n## Alpha\n\nAlpha body.\n'
        )

        self.assertIsNone(
            _plan(old, swapped.replace("# Doc", "# Docs")).named_section_reorder
        )
        self.assertIsNone(
            _plan(
                old, swapped.replace("- [Beta](#beta)", "- [Renamed](#beta)")
            ).named_section_reorder
        )

    def test_front_matter_change_is_copied_without_a_provider_output(self):
        """머리말 변경을 번역 출력 없이 원문에서 복사함."""

        old = """---
slug: cache
description: Old cache guide.
---

Paragraph.
"""
        new = old.replace("Old cache guide.", "New cache guide.")
        existing = old.replace("Paragraph.", "<!-- Paragraph. -->\n문단입니다.")
        plan = _plan(old, new)

        self.assertIs(patch.plan_state(existing, plan), patch.PlanState.SOURCE)
        first = patch.apply_plan(existing, plan, [])

        self.assertIn("description: New cache guide.", first)
        self.assertNotIn("description: Old cache guide.", first)
        self.assertIs(patch.plan_state(first, plan), patch.PlanState.TARGET)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_front_matter_change_rejects_an_unsupported_new_value(self):
        """지원하지 않는 신규 머리말 값을 거부함."""

        old = "---\ntags: old\n---\n\nParagraph.\n"
        new = "---\ntags: [new]\n---\n\nParagraph.\n"

        with self.assertRaisesRegex(patch.PatchError, "unsupported front matter"):
            _plan(old, new)

    def test_front_matter_and_fenced_code_change_remain_separate_owner_units(self):
        """머리말과 코드 블록 변경을 별도 소유 단위로 유지함."""

        old = "---\ndescription: Old.\n---\n\n```php\nold();\n```\n"
        new = "---\ndescription: New.\n---\n\n```php\nnew();\n```\n"
        plan = _plan(old, new)

        self.assertEqual(len(plan.changes), 1)
        self.assertIsNotNone(plan.changes[0].code_block)

        first = patch.apply_plan(old, plan, [])

        self.assertEqual(first, new)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_normalized_style_only_change_has_no_operations(self):
        """정규화 후 스타일 차이만 남은 변경에 대해 빈 계획을 생성함."""

        old = "<style>\n.example { color: red; }\n</style>\n\nBefore.\n"
        new = "<style>\n.example { color: blue; }\n</style>\n\nBefore.\n"
        existing = "<!-- Before. -->\n앞입니다.\n"
        plan = _plan(
            old,
            new,
            normalize_source=lambda source: preprocess.preprocess(source).text,
        )

        self.assertEqual(plan.changes, ())
        self.assertTrue(plan.is_noop)
        self.assertIs(patch.plan_state(existing, plan), patch.PlanState.UNGUARDED)
        self.assertEqual(patch.apply_plan(existing, plan, []), existing)

    def test_pair_normalizer_receives_old_and_current_source_once(self):
        """이전·현재 원문 쌍 정규화기의 단일 호출을 검증함."""

        old = "    old();\n"
        new = "    new();\n"
        calls = []

        def normalize_pair(old_source, current_source):
            """원문 쌍을 정규화함."""

            calls.append((old_source, current_source))
            return (
                "```\nold();\n```\n",
                "```\nnew();\n```\n",
            )

        plan = _plan(old, new, normalize_source_pair=normalize_pair)

        self.assertEqual(calls, [(old, new)])
        self.assertEqual(len(plan.changes), 1)
        self.assertIsNotNone(plan.changes[0].code_block)

    def test_build_plan_rejects_both_normalizer_contracts(self):
        """서로 다른 두 정규화 계약의 동시 사용을 거부함."""

        with self.assertRaisesRegex(patch.PatchError, "normalizer"):
            patch.build_plan(
                (),
                "Current.\n",
                normalize_source=lambda source: source,
                normalize_source_pair=lambda old, current: (old, current),
            )

    def test_reapplying_chained_replacements_is_noop(self):
        """연쇄 교체 결과에 같은 계획을 다시 적용할 때 변경 없음으로 판정함."""

        old = "A.\n\nB.\n"
        new = "B.\n\nC.\n"
        existing = (
            "<!-- A. -->\n첫째입니다.\n\n"
            "<!-- B. -->\n둘째입니다.\n"
        )
        translated = [
            "<!-- B. -->\n새 첫째입니다.\n",
            "<!-- C. -->\n새 둘째입니다.\n",
        ]
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, translated)

        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_reapplying_last_duplicate_replacement_is_noop(self):
        """마지막 중복 블록 교체 결과를 다시 적용할 때 변경 없음으로 판정함."""

        old = "A.\n\nA.\n\nA.\n"
        new = "A.\n\nA.\n\nB.\n"
        existing = (
            "<!-- A. -->\n첫째입니다.\n\n"
            "<!-- A. -->\n둘째입니다.\n\n"
            "<!-- A. -->\n셋째입니다.\n"
        )
        translated = ["<!-- B. -->\n변경된 셋째입니다.\n"]
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, translated)

        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_target_state_rejects_unannotated_deleted_body(self):
        """대상 상태에 주석 없이 남은 삭제 본문을 거부함."""

        old = "Before.\n\nDelete foo();\n\nAfter.\n"
        new = "Before.\n\nAfter.\n"
        existing = (
            "<!-- Before. -->\n앞입니다.\n\n"
            "Delete foo();\n\n"
            "<!-- After. -->\n뒤입니다.\n"
        )
        plan = _plan(old, new)

        self.assertIs(patch.plan_state(existing, plan), patch.PlanState.TARGET)
        with self.assertRaisesRegex(patch.PatchError, "deleted source remains"):
            patch.apply_plan(existing, plan, [])

    def test_target_deletion_ignores_owned_identity_translation(self):
        """대상 삭제 상태에서 원문과 같은 소유 본문을 허용함."""

        old = "A();\n\nA();\n\nA();\n"
        new = "A();\n\nA();\n"
        existing = (
            "<!-- A(); -->\nA();\n\n"
            "<!-- A(); -->\nA();\n\n"
            "<!-- A(); -->\nA();\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [])

        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_comment_only_target_insertion_fails_closed(self):
        """본문 없이 파이프라인 주석만 있는 대상 삽입 상태를 거부함."""

        old = "Before.\n\nAfter.\n"
        new = "Before.\n\nInserted meaning.\n\nAfter.\n"
        existing = (
            "<!-- Before. -->\n이전 문단.\n\n"
            "<!-- Inserted meaning. -->\n\n"
            "<!-- After. -->\n이후 문단.\n"
        )
        plan = _plan(old, new)

        self.assertIs(patch.plan_state(existing, plan), patch.PlanState.TARGET)
        with self.assertRaisesRegex(patch.PatchError, "translated body"):
            patch.apply_plan(existing, plan, [])

        complete = existing.replace(
            "<!-- Inserted meaning. -->\n",
            "<!-- Inserted meaning. -->\n삽입된 의미.\n",
        )
        self.assertEqual(patch.apply_plan(complete, plan, []), complete)

    def test_target_deletion_rejects_translated_orphan_body(self):
        """대상 삭제 후 남은 번역 고아 본문을 거부함."""

        old = "Before.\n\nDoomed.\n\nAfter.\n"
        new = "Before.\n\nAfter.\n"
        existing = (
            "<!-- Before. -->\n이전 문단.\n\n"
            "삭제되어야 할 번역.\n\n"
            "<!-- After. -->\n이후 문단.\n"
        )
        plan = _plan(old, new)

        self.assertIs(patch.plan_state(existing, plan), patch.PlanState.TARGET)
        with self.assertRaisesRegex(
            patch.PatchError, "remains outside its annotated block"
        ):
            patch.apply_plan(existing, plan, [])

        clean = "<!-- Before. -->\n이전 문단.\n\n<!-- After. -->\n이후 문단.\n"
        self.assertEqual(patch.apply_plan(clean, plan, []), clean)

    def test_annotated_deletion_does_not_fall_back_to_raw_contexts(self):
        """파이프라인 주석 삭제에 실패하면 원시 문맥으로 대체하지 않음."""

        segment = patch.BlockChange(
            old_lines=("Delete foo();",),
            new_lines=(),
            before_context="Before raw context.",
            after_context="After raw context.",
            old_source="Delete foo();\n",
            old_anchors=("Delete foo();",),
        )
        existing = (
            "Before raw context.\n"
            "Delete foo();\n"
            "After raw context.\n"
        )

        with self.assertRaises(patch.PatchError):
            patch.apply_segments(existing, [segment], [])

    def test_inserts_paragraph_before_complete_first_annotated_block(self):
        """첫 파이프라인 주석 블록 전체 앞에 문단을 삽입함."""

        old = "Gamma.\n"
        new = "Inserted.\n\nGamma.\n"
        existing = "<!-- Gamma. -->\nGamma.\n"
        translated = "<!-- Inserted. -->\nInserted.\n"
        expected = (
            "<!-- Inserted. -->\nInserted.\n\n"
            "<!-- Gamma. -->\nGamma.\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])

        self.assertEqual(first, expected)
        self.assertEqual(
            [(block.comment, block.text) for block in patch._blocks(first)],  # noqa: SLF001
            [
                ("Inserted.", "<!-- Inserted. -->\nInserted.\n\n"),
                ("Gamma.", "<!-- Gamma. -->\nGamma.\n"),
            ],
        )
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_inserts_paragraph_between_duplicate_context_blocks(self):
        """중복 문맥 블록 사이에 새 문단을 삽입함."""

        old = "B.\n\nB.\n\nB.\n"
        new = "B.\n\nB.\n\nInserted.\n\nB.\n"
        existing = (
            "<!-- B. -->\n첫째입니다.\n\n"
            "<!-- B. -->\n둘째입니다.\n\n"
            "<!-- B. -->\n셋째입니다.\n"
        )
        translated = "<!-- Inserted. -->\n삽입됐습니다.\n"
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])

        self.assertLess(first.index("둘째입니다."), first.index("삽입됐습니다."))
        self.assertLess(first.index("삽입됐습니다."), first.index("셋째입니다."))
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_inserts_duplicate_of_first_paragraph_at_document_start(self):
        """문서 시작에 첫 문단과 동일한 문단을 삽입함."""

        old = "Alpha.\n\nGamma.\n"
        new = "Alpha.\n\nAlpha.\n\nGamma.\n"
        existing = (
            "<!-- Alpha. -->\nAlpha.\n\n"
            "<!-- Gamma. -->\nGamma.\n"
        )
        translated = "<!-- Alpha. -->\nAlpha.\n"
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])

        self.assertEqual(first.count("<!-- Alpha. -->"), 2)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_inserts_paragraph_after_last_duplicate_at_document_end(self):
        """문서 끝에서 마지막 중복 문단 뒤에 삽입함."""

        old = "B.\n\nB.\n\nB.\n"
        new = "B.\n\nB.\n\nB.\n\nInserted.\n"
        existing = (
            "<!-- B. -->\n첫째입니다.\n\n"
            "<!-- B. -->\n둘째입니다.\n\n"
            "<!-- B. -->\n셋째입니다.\n"
        )
        translated = "<!-- Inserted. -->\n삽입됐습니다.\n"
        plan = _plan(old, new)
        self.assertIn("셋째입니다.", patch.existing_context(existing, plan.changes[0]))

        first = patch.apply_plan(existing, plan, [translated])

        self.assertGreater(first.index("삽입됐습니다."), first.index("셋째입니다."))
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_structural_insertion_follows_the_last_duplicate_annotation(self):
        """구조 삽입을 마지막 중복 주석 뒤에 배치함."""

        old = "Repeat.\n\nRepeat.\n"
        new = old + "\n> [!NOTE]\n> New warning.\n"
        existing = (
            "<!-- Repeat. -->\n첫 번째 반복입니다.\n\n"
            "<!-- Repeat. -->\n두 번째 반복입니다.\n"
        )
        translated = "> [!NOTE]\n> 새 경고입니다.\n"
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])

        self.assertLess(first.index("두 번째 반복입니다."), first.index("> [!NOTE]"))
        self.assertEqual(patch.apply_plan(first, plan, [translated]), first)

    def test_structural_insertion_with_ambiguous_context_fails_closed(self):
        """문맥이 모호한 구조 블록 삽입을 거부함."""

        old = "A one.\nA two.\n\nA one.\nA two.\n"
        new = "A one.\nA two.\n\n> [!NOTE]\n> W.\n\nA one.\nA two.\n"
        existing = (
            "<!-- A one. A two. -->\n에이 하나입니다.\n\n"
            "<!-- A one. A two. -->\n에이 둘입니다.\n"
        )

        with self.assertRaisesRegex(patch.PatchError, "missing insertion context"):
            patch.apply_plan(existing, _plan(old, new), ["> [!NOTE]\n> 경고.\n"])

    def test_reapplying_inserted_paragraph_is_idempotent(self):
        """삽입 문단에 같은 계획을 다시 적용해도 멱등성을 보장함."""

        old = "Before.\n\nAfter.\n"
        new = "Before.\n\nInserted.\n\nAfter.\n"
        existing = (
            "<!-- Before. -->\n이전입니다.\n\n"
            "<!-- After. -->\n이후입니다.\n"
        )
        translated = "<!-- Inserted. -->\n삽입됐습니다.\n"
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])
        second = patch.apply_plan(first, plan, [])

        self.assertEqual(second, first)

    def test_inserts_two_identical_paragraphs_without_applied_ordinal_drift(self):
        """동일한 두 문단을 적용 순서에서 벗어나지 않게 삽입함."""

        old = "Before.\n\nAfter.\n"
        new = "Before.\n\nInserted.\n\nInserted.\n\nAfter.\n"
        existing = (
            "<!-- Before. -->\n이전입니다.\n\n"
            "<!-- After. -->\n이후입니다.\n"
        )
        translated = [
            "<!-- Inserted. -->\n첫 삽입입니다.\n\n"
            "<!-- Inserted. -->\n둘째 삽입입니다.\n"
        ]
        plan = _plan(old, new)

        self.assertEqual(len(plan.changes), 1)
        self.assertEqual(plan.changes[0].new_anchors, ("Inserted.", "Inserted."))
        first = patch.apply_plan(existing, plan, translated)

        self.assertIn("첫 삽입입니다.", first)
        self.assertIn("둘째 삽입입니다.", first)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_reapplying_first_duplicate_block_does_not_replace_second(self):
        """첫 중복 블록을 다시 적용할 때 두 번째 블록의 교체를 방지함."""

        old_block = "Old duplicate.\n"
        new_block = "Changed first duplicate.\n"
        old = f"{old_block}\n{old_block}"
        new = f"{new_block}\n{old_block}"
        existing = (
            "<!-- Old duplicate. -->\n첫 번째입니다.\n\n"
            "<!-- Old duplicate. -->\n두 번째입니다.\n"
        )
        translated = (
            "<!-- Changed first duplicate. -->\n변경된 첫 번째입니다.\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])
        second = patch.apply_plan(first, plan, [])

        self.assertEqual(second, first)
        self.assertIn("<!-- Old duplicate. -->\n두 번째입니다.", second)

    def test_replaces_adjacent_duplicate_blocks_without_ordinal_drift(self):
        """인접한 중복 블록을 적용 순서에서 벗어나지 않게 교체함."""

        old = "Same.\n\nSame.\n"
        new = "First changed.\n\nSecond changed.\n"
        existing = (
            "<!-- Same. -->\n첫 번째입니다.\n\n"
            "<!-- Same. -->\n두 번째입니다.\n"
        )
        translated = [
            "<!-- First changed. -->\n첫 번째 변경입니다.\n",
            "<!-- Second changed. -->\n두 번째 변경입니다.\n",
        ]
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, translated)

        self.assertIn("첫 번째 변경입니다.", first)
        self.assertIn("두 번째 변경입니다.", first)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_existing_equal_new_block_elsewhere_is_not_applied_target(self):
        """다른 위치의 동일한 신규 블록을 대상 상태로 오인하지 않음."""

        old = "Alpha.\n\nBeta.\n"
        new = "Beta.\n\nBeta.\n"
        existing = (
            "<!-- Alpha. -->\n알파.\n\n"
            "<!-- Beta. -->\n기존 베타.\n"
        )
        translated = "<!-- Beta. -->\n변경된 첫 블록.\n"
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])
        second = patch.apply_plan(first, plan, [])

        self.assertIn("변경된 첫 블록.", first)
        self.assertIn("기존 베타.", first)
        self.assertNotEqual(first, existing)
        self.assertEqual(second, first)

    def test_equal_new_block_in_a_repeated_neighborhood_does_not_skip_old_target(self):
        """반복 문맥의 동일한 신규 블록이 기존 대상을 건너뛰지 않도록 제한함."""

        old = "Prev.\n\nOld.\n\nNext.\n\nPrev.\n\nNew.\n\nNext.\n"
        new = "Prev.\n\nNew.\n\nNext.\n\nPrev.\n\nNew.\n\nNext.\n"
        existing = (
            "<!-- Prev. -->\n앞입니다.\n\n"
            "<!-- Old. -->\n바뀔 대상입니다.\n\n"
            "<!-- Next. -->\n뒤입니다.\n\n"
            "<!-- Prev. -->\n다른 앞입니다.\n\n"
            "<!-- New. -->\n기존 새 문단입니다.\n\n"
            "<!-- Next. -->\n다른 뒤입니다.\n"
        )
        translated = "<!-- New. -->\n변경된 문단입니다.\n"
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])

        self.assertIn("변경된 문단입니다.", first)
        self.assertIn("기존 새 문단입니다.", first)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_replaces_one_source_block_with_two_blocks_as_one_change(self):
        """원문 블록 하나를 두 블록으로 한 번에 교체함."""

        old = "Combined paragraph.\n"
        new = "First paragraph.\n\nSecond paragraph.\n"
        existing = "<!-- Combined paragraph. -->\n합쳐진 문단입니다.\n"
        translated = (
            "<!-- First paragraph. -->\n첫 문단입니다.\n\n"
            "<!-- Second paragraph. -->\n둘째 문단입니다.\n"
        )
        plan = _plan(old, new)

        self.assertEqual(len(plan.changes), 1)
        first = patch.apply_plan(existing, plan, [translated])

        self.assertIn("첫 문단입니다.", first)
        self.assertIn("둘째 문단입니다.", first)
        self.assertEqual(verify.verify(first, source=new), [])
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_replaces_two_source_blocks_with_one_block_as_one_change(self):
        """원문 블록 두 개를 한 블록으로 한 번에 교체함."""

        old = "First paragraph.\n\nSecond paragraph.\n"
        new = "Combined paragraph.\n"
        existing = (
            "<!-- First paragraph. -->\n첫 문단입니다.\n\n"
            "<!-- Second paragraph. -->\n둘째 문단입니다.\n"
        )
        translated = "<!-- Combined paragraph. -->\n합쳐진 문단입니다.\n"
        plan = _plan(old, new)

        self.assertEqual(len(plan.changes), 1)
        first = patch.apply_plan(existing, plan, [translated])

        self.assertIn("합쳐진 문단입니다.", first)
        self.assertNotIn("둘째 문단입니다.", first)
        self.assertEqual(verify.verify(first, source=new), [])
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_incomplete_old_block_range_fails_closed(self):
        """이전 원문 블록 범위가 불완전하면 계획을 거부함."""

        old = "First paragraph.\n\nSecond paragraph.\n"
        new = "Combined paragraph.\n"
        existing = "<!-- First paragraph. -->\n첫 문단입니다.\n"
        translated = "<!-- Combined paragraph. -->\n합쳐진 문단입니다.\n"

        with self.assertRaises(patch.PatchError):
            patch.apply_plan(existing, _plan(old, new), [translated])

    def test_reapplying_paragraph_deletions_at_document_edges_is_idempotent(self):
        """문서 양끝 문단 삭제 계획을 다시 적용해도 멱등성을 보장함."""

        cases = (
            (
                "Delete.\n\nAfter.\n",
                "After.\n",
                "<!-- Delete. -->\n삭제됩니다.\n\n<!-- After. -->\n뒤입니다.\n",
            ),
            (
                "Before.\n\nDelete.\n",
                "Before.\n",
                "<!-- Before. -->\n앞입니다.\n\n<!-- Delete. -->\n삭제됩니다.\n",
            ),
        )
        for old, new, existing in cases:
            with self.subTest(old=old):
                plan = _plan(old, new)
                first = patch.apply_plan(existing, plan, [])

                self.assertNotIn("삭제됩니다.", first)
                self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_reapplying_duplicate_paragraph_deletion_keeps_remaining_blocks(self):
        """중복 문단 삭제 계획을 다시 적용할 때 남은 블록을 보존함."""

        old = "B.\n\nB.\n\nB.\n"
        new = "B.\n\nB.\n"
        existing = (
            "<!-- B. -->\n첫째입니다.\n\n"
            "<!-- B. -->\n둘째입니다.\n\n"
            "<!-- B. -->\n셋째입니다.\n"
        )
        expected = (
            "<!-- B. -->\n첫째입니다.\n\n"
            "<!-- B. -->\n둘째입니다.\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [])

        self.assertEqual(first, expected)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_reapplying_deletion_between_duplicate_neighbors_is_idempotent(self):
        """중복 이웃 사이의 삭제 계획을 다시 적용해도 멱등성을 보장함."""

        old = "B.\n\nB.\n\nDelete.\n\nB.\n"
        new = "B.\n\nB.\n\nB.\n"
        existing = (
            "<!-- B. -->\n첫째입니다.\n\n"
            "<!-- B. -->\n둘째입니다.\n\n"
            "<!-- Delete. -->\n삭제됩니다.\n\n"
            "<!-- B. -->\n셋째입니다.\n"
        )
        expected = (
            "<!-- B. -->\n첫째입니다.\n\n"
            "<!-- B. -->\n둘째입니다.\n\n"
            "<!-- B. -->\n셋째입니다.\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [])

        self.assertEqual(first, expected)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_deletes_before_reinserting_a_realigned_duplicate_block(self):
        """재정렬된 중복 블록을 다시 삽입하기 전에 기존 블록을 삭제함."""

        old = "Gamma.\n\nGamma.\n\nBeta.\n\nGamma.\n\nBeta.\n\nBeta.\n\nBeta.\n\nSame.\n"
        new = "Gamma.\n\nGamma.\n\nBeta.\n\nBeta.\n\nBeta.\n\nBeta.\n\nSame.\n"
        existing = "\n\n".join(
            f"<!-- {anchor} -->\n번역-{index}"
            for index, anchor in enumerate(
                ("Gamma.", "Gamma.", "Beta.", "Gamma.", "Beta.", "Beta.", "Beta.", "Same.")
            )
        ) + "\n"
        translated = "<!-- Beta. -->\n재배치된 번역입니다."
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])

        self.assertEqual(first.count("<!-- Gamma. -->"), 2)
        self.assertEqual(first.count("<!-- Beta. -->"), 4)
        self.assertIn("재배치된 번역입니다.", first)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_rejects_a_partial_realigned_block_state(self):
        """일부만 재정렬된 블록 상태를 거부함."""

        old = "A.\n\nB.\n\nA.\n\nB.\n\nB.\n"
        new = "A.\n\nB.\n\nB.\n\nB.\n"
        translated = "<!-- B. -->\n이미 삽입됐습니다."
        existing = (
            "<!-- A. -->\n첫째 A입니다.\n\n"
            "<!-- B. -->\n첫째 B입니다.\n\n"
            "<!-- A. -->\n둘째 A입니다.\n\n"
            "<!-- B. -->\n둘째 B입니다.\n\n"
            "<!-- B. -->\n셋째 B입니다.\n\n"
            f"{translated}\n"
        )
        plan = _plan(old, new)

        with self.assertRaisesRegex(patch.PatchError, "neither source nor target"):
            patch.apply_plan(existing, plan, [translated])

    def test_realigns_duplicates_against_the_complete_target_sequence(self):
        """완전한 대상 순서를 기준으로 중복 블록을 재정렬함."""

        old_blocks = ("A.", "A.", "B.", "A.", "B.", "A.", "A.")
        new_blocks = ("A.", "A.", "A.", "B.", "A.", "A.")
        old = "\n\n".join(old_blocks) + "\n"
        new = "\n\n".join(new_blocks) + "\n"
        existing = "\n\n".join(
            f"<!-- {anchor} -->\n번역-{index}"
            for index, anchor in enumerate(old_blocks)
        ) + "\n"
        translated = "<!-- A. -->\n재배치된 A입니다."
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])

        self.assertEqual(
            tuple(block.comment for block in patch._blocks(first)),  # noqa: SLF001
            new_blocks,
        )
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_reapplies_paragraph_deletion_next_to_fenced_code(self):
        """펜스 코드 옆 문단 삭제를 다시 적용해도 안정적으로 처리함."""

        old = "Before.\n\nDelete.\n\n```php\nkeep();\n```\n\nAfter.\n"
        new = "Before.\n\n```php\nkeep();\n```\n\nAfter.\n"
        existing = (
            "<!-- Before. -->\n앞입니다.\n\n"
            "<!-- Delete. -->\n삭제됩니다.\n\n"
            "```php\nkeep();\n```\n\n"
            "<!-- After. -->\n뒤입니다.\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [])

        self.assertNotIn("삭제됩니다.", first)
        self.assertIn("```php\nkeep();\n```", first)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_plan_state_uses_only_normalized_annotatable_comments(self):
        """계획 상태 판정에 정규화된 주석 대상 문장만 사용함."""

        old = (
            '<div class="grid">\n\n'
            "Before.\n\n"
            "</div>\n\n"
            "Use `DB::raw(/* ... */)` carefully.\n"
        )
        new = old + "\nInserted.\n"
        existing = (
            '<!-- <div class="grid"> -->\n<div class="grid">\n\n'
            "<!-- Before. -->\n앞입니다.\n\n"
            "<!-- </div> -->\n</div>\n\n"
            "<!-- Use `DB::raw(/* ... *&#47;)` carefully. -->\n"
            "주의해서 사용합니다.\n"
        )
        translated = "<!-- Inserted. -->\n삽입됐습니다."
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])

        self.assertEqual(
            plan.old_source_anchors,
            ("Before.", "Use `DB::raw(/* ... */)` carefully."),
        )
        self.assertIn("삽입됐습니다.", first)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_plan_state_ignores_preserved_source_html_comments(self):
        """보존된 원문 HTML 주석을 계획 상태 판정에서 제외함."""

        old = "<!-- keep -->\n\nOld paragraph.\n"
        new = "<!-- keep -->\n\nNew paragraph.\n"
        existing = (
            "<!-- keep -->\n\n"
            "<!-- Old paragraph. -->\n"
            "기존 문단입니다.\n"
        )
        translated = "<!-- New paragraph. -->\n새 문단입니다."
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])

        self.assertIn("<!-- keep -->", first)
        self.assertIn("새 문단입니다.", first)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_source_comment_is_not_confused_with_an_identical_annotation(self):
        """동일한 원문 주석과 파이프라인 주석의 역할을 구분함."""

        old = "Same.\n\n<!-- Same. -->\n\nB.\n"
        new = "Changed.\n\n<!-- Same. -->\n\nB.\n"
        existing = (
            "<!-- Same. -->\n"
            "동일합니다.\n\n"
            "<!-- Same. -->\n\n"
            "<!-- B. -->\n"
            "B 번역입니다.\n"
        )
        translated = "<!-- Changed. -->\n바뀌었습니다."
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])

        self.assertIn(
            "<!-- Changed. -->\n바뀌었습니다.\n\n"
            "<!-- Same. -->\n\n"
            "<!-- B. -->",
            first,
        )
        self.assertNotIn("동일합니다.", first)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_preserves_a_multiline_source_comment_while_patching(self):
        """패치 적용 중 여러 줄 원문 주석을 보존함."""

        source_comment = "<!--\nkeep line 1\nkeep line 2\n-->"
        old = f"{source_comment}\n\nOld.\n"
        new = f"{source_comment}\n\nNew.\n"
        existing = (
            f"{source_comment}\n\n"
            "<!-- Old. -->\n예전 문단입니다.\n"
        )
        translated = "<!-- New. -->\n새 문단입니다."
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])

        self.assertIn(f"{source_comment}\n\n<!-- New. -->", first)
        self.assertEqual(first.count(source_comment), 1)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_source_comment_replacement_is_copied_without_a_provider_output(self):
        """원문 주석 교체를 번역 출력 없이 복사함."""

        old = "<!-- old directive -->\n\nParagraph.\n"
        new = "<!-- new directive -->\n\nParagraph.\n"
        existing = (
            "<!-- old directive -->\n\n"
            "<!-- Paragraph. -->\n문단입니다.\n"
        )
        plan = _plan(old, new)

        self.assertIs(patch.plan_state(existing, plan), patch.PlanState.SOURCE)
        first = patch.apply_plan(existing, plan, [])

        self.assertIn("<!-- new directive -->", first)
        self.assertNotIn("<!-- old directive -->", first)
        self.assertIs(patch.plan_state(first, plan), patch.PlanState.TARGET)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_source_comment_addition_and_deletion_use_a_unique_anchor_boundary(self):
        """고유 앵커 경계를 이용해 원문 주석을 추가하고 삭제함."""

        without = "Before.\n\nAfter.\n"
        with_comment = "Before.\n\n<!-- directive -->\n\nAfter.\n"
        existing = (
            "<!-- Before. -->\n이전 문단.\n\n"
            "<!-- After. -->\n다음 문단.\n"
        )

        add_plan = _plan(without, with_comment)
        added = patch.apply_plan(existing, add_plan, [])

        self.assertIn("이전 문단.\n\n<!-- directive -->\n\n<!-- After. -->", added)
        self.assertEqual(patch.apply_plan(added, add_plan, []), added)

        delete_plan = _plan(with_comment, without)
        deleted = patch.apply_plan(added, delete_plan, [])

        self.assertNotIn("<!-- directive -->", deleted)
        self.assertEqual(patch.apply_plan(deleted, delete_plan, []), deleted)

    def test_source_comment_addition_preserves_an_existing_comment_at_the_boundary(self):
        """원문 주석 추가 시 경계에 있던 기존 주석을 보존함."""

        old = "Before.\n\n<!-- keep -->\n\nAfter.\n"
        new = "Before.\n\n<!-- keep -->\n<!-- added -->\n\nAfter.\n"
        existing = (
            "<!-- Before. -->\n이전 문단.\n\n"
            "<!-- keep -->\n\n"
            "<!-- After. -->\n다음 문단.\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [])

        self.assertLess(first.index("<!-- keep -->"), first.index("<!-- added -->"))
        self.assertEqual(first.count("<!-- keep -->"), 1)
        self.assertEqual(first.count("<!-- added -->"), 1)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_source_comment_move_across_code_uses_its_structural_side(self):
        """코드를 가로지르는 원문 주석 이동에 구조상 인접 면을 사용함."""

        code = "```php\nrun();\n```"
        old = f"Before.\n\n<!-- move -->\n\n{code}\n\nAfter.\n"
        new = f"Before.\n\n{code}\n\n<!-- move -->\n\nAfter.\n"
        existing = (
            "<!-- Before. -->\n이전 문단.\n\n"
            "<!-- move -->\n\n"
            f"{code}\n\n"
            "<!-- After. -->\n다음 문단.\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [])

        self.assertLess(first.index(code), first.index("<!-- move -->"))
        self.assertLess(first.index("<!-- move -->"), first.index("<!-- After. -->"))
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_target_state_requires_zero_translation_outputs(self):
        """대상 상태에서 번역 출력이 없어야 함을 확인함."""

        old = "Old.\n"
        new = "New.\n"
        existing = "<!-- Old. -->\n예전 문단.\n"
        translated = "<!-- New. -->\n새 문단."
        plan = _plan(old, new)
        target = patch.apply_plan(existing, plan, [translated])

        self.assertIs(patch.plan_state(target, plan), patch.PlanState.TARGET)
        self.assertEqual(patch.apply_plan(target, plan, []), target)
        with self.assertRaisesRegex(
            patch.PatchError, "translation count mismatch: expected 0, got 1"
        ):
            patch.apply_plan(target, plan, [translated])

    def test_plan_state_excludes_preprocessed_indented_code(self):
        """전처리된 들여쓰기 코드를 계획 상태 판정에서 제외함."""

        old = "Before.\n\n    example();\n\nAfter.\n"
        new = old + "\nInserted.\n"
        existing = (
            "<!-- Before. -->\n앞입니다.\n\n"
            "```\nexample();\n```\n\n"
            "<!-- After. -->\n뒤입니다.\n"
        )
        translated = "<!-- Inserted. -->\n삽입됐습니다."
        plan = _plan(
            old,
            new,
            normalize_source=lambda source: preprocess.preprocess(source).text,
        )

        first = patch.apply_plan(existing, plan, [translated])

        self.assertEqual(plan.old_source_anchors, ("Before.", "After."))
        self.assertIn("```\nexample();\n```", first)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_plan_state_ignores_structural_html_annotations(self):
        """구조용 HTML 주석을 계획 상태 판정에서 제외함."""

        old = (
            '<p align="center">\n'
            '    <img src="/img/logo.png" alt="Logo"/>\n'
            "</p>\n\n"
            "Before.\n"
        )
        new = old + "\nInserted.\n"
        existing = (
            "<!--\n"
            '<p align="center">\n'
            '    <img src="/img/logo.png" alt="Logo"/>\n'
            "</p>\n"
            "-->\n"
            '<p align="center">\n'
            '    <img src="/img/logo.png" alt="Logo"/>\n'
            "</p>\n\n"
            "<!-- Before. -->\n앞입니다.\n"
        )
        translated = "<!-- Inserted. -->\n삽입됐습니다."
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])

        self.assertEqual(plan.old_source_anchors, ("Before.",))
        self.assertIn("삽입됐습니다.", first)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_replaces_blankless_body_inside_html_wrapper(self):
        """빈 줄 없는 HTML 래퍼 내부 본문을 교체함."""

        old = '<div class="content-list">\nOld.\n</div>\n'
        new = '<div class="content-list">\nNew.\n</div>\n'
        existing = (
            '<div class="content-list">\n'
            '<!-- Old. -->\n'
            '기존 번역입니다.\n'
            '</div>\n'
        )
        translated = '<!-- New. -->\n새 번역입니다.'
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])

        self.assertEqual(verify.verify(first, source=new), [])
        self.assertIn('새 번역입니다.', first)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_bare_link_update_ignores_structural_wrapper_annotations(self):
        """`bare link` 변경에서 구조 `wrapper annotation`을 제외함."""

        old = (
            '<div class="links" markdown="1">\n\n'
            "[reduce](#method-reduce)\n"
            "[reject](#method-reject)\n\n"
            "</div>\n\n"
            "### Next\n"
        )
        new = old.replace(
            "[reduce](#method-reduce)\n",
            "[reduce](#method-reduce)\n"
            "[reduceInto](#method-reduce-into)\n",
        )
        existing = (
            '<!-- <div class="links" markdown="1"> -->\n'
            '<div class="links" markdown="1">\n\n'
            "<!--\n"
            "[reduce](#method-reduce)\n"
            "[reject](#method-reject)\n"
            "-->\n"
            "[reduce](#method-reduce)\n"
            "[reject](#method-reject)\n\n"
            "<!-- </div> -->\n"
            "</div>\n\n"
            "<!-- ### Next -->\n"
            "### Next\n"
        )
        translated = (
            "<!--\n"
            "[reduce](#method-reduce)\n"
            "[reduceInto](#method-reduce-into)\n"
            "[reject](#method-reject)\n"
            "-->\n"
            "[reduce](#method-reduce)\n"
            "[reduceInto](#method-reduce-into)\n"
            "[reject](#method-reject)\n"
        )

        result = patch.apply_plan(existing, _plan(old, new), [translated])

        self.assertEqual(result.count("[reduceInto](#method-reduce-into)"), 2)
        self.assertEqual(patch.apply_plan(result, _plan(old, new), []), result)

    def test_missing_deleted_paragraph_does_not_remove_unrelated_content(self):
        """이미 삭제된 문단이 무관한 내용을 제거하지 않도록 함."""

        old = "Before.\n\nDelete.\n\nAfter.\n"
        new = "Before.\n\nAfter.\n"
        existing = (
            "<!-- Before. -->\n앞입니다.\n\n"
            "<!-- Different. -->\n다른 내용입니다.\n\n"
            "<!-- After. -->\n뒤입니다.\n"
        )

        with self.assertRaises(patch.PatchError):
            patch.apply_plan(existing, _plan(old, new), [])

        self.assertIn("다른 내용입니다.", existing)

    def test_split_with_wrong_old_anchor_fails_closed(self):
        """이전 앵커가 다른 블록 범위를 분할하면 거부함."""

        old = "Combined paragraph.\n"
        new = "First paragraph.\n\nSecond paragraph.\n"
        existing = "<!-- Wrong paragraph. -->\n다른 문단입니다.\n"
        translated = (
            "<!-- First paragraph. -->\n첫 문단입니다.\n\n"
            "<!-- Second paragraph. -->\n둘째 문단입니다.\n"
        )

        with self.assertRaises(patch.PatchError):
            patch.apply_plan(existing, _plan(old, new), [translated])

    def test_annotated_change_does_not_fall_back_to_raw_contexts(self):
        """파이프라인 주석 변경에 실패하면 원시 문맥으로 대체하지 않음."""

        segment = patch.BlockChange(
            old_lines=("Old paragraph.",),
            new_lines=("New paragraph.",),
            before_context="Before raw context.",
            after_context="After raw context.",
            old_source="Old paragraph.\n",
            old_anchors=("Old paragraph.",),
            new_source="New paragraph.\n",
            new_anchor="New paragraph.",
            new_anchors=("New paragraph.",),
        )
        existing = (
            "Before raw context.\n"
            "Old paragraph.\n"
            "After raw context.\n"
        )
        translated = "<!-- New paragraph. -->\n새 문단입니다.\n"

        with self.assertRaises(patch.PatchError):
            patch.apply_segments(existing, [segment], [translated])

    def test_block_range_neighbors_stay_outside_the_changed_range(self):
        """블록 범위 이웃 앵커를 변경 범위 바깥에 유지함."""

        old = "Before.\n\nCombined paragraph.\n\nAfter.\n"
        new = (
            "Before.\n\nFirst paragraph.\n\n"
            "Second paragraph.\n\nAfter.\n"
        )

        change = _plan(old, new).changes[0]

        self.assertEqual(change.old_anchors, ("Combined paragraph.",))
        self.assertEqual(
            change.new_anchors,
            ("First paragraph.", "Second paragraph."),
        )
        self.assertEqual(change.new_previous_anchor, "Before.")
        self.assertEqual(change.new_next_anchor, "After.")

    def test_block_range_ordinal_updates_only_the_second_duplicate_sequence(self):
        """중복 블록 범위 중 두 번째 순서만 갱신함."""

        pair = "Alpha.\n\nBeta.\n"
        old = f"{pair}\n{pair}"
        new = f"{pair}\nCombined.\n"
        first_pair = (
            "<!-- Alpha. -->\n첫 알파.\n\n"
            "<!-- Beta. -->\n첫 베타.\n"
        )
        second_pair = (
            "<!-- Alpha. -->\n둘째 알파.\n\n"
            "<!-- Beta. -->\n둘째 베타.\n"
        )
        existing = f"{first_pair}\n{second_pair}"
        translated = "<!-- Combined. -->\n합쳐졌습니다.\n"
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])

        self.assertIn(first_pair.rstrip(), first)
        self.assertNotIn("둘째 알파.", first)
        self.assertIn("합쳐졌습니다.", first)
        self.assertEqual(patch.apply_plan(first, plan, []), first)

    def test_plan_keeps_literal_delta_separate_from_complete_link_block(self):
        """문자열 변경과 완전한 링크 블록을 별도 변경으로 유지함."""

        first = "[reduce](#reduce)\n[reject](#reject)\n"
        old = f"{first}\n{first}"
        changed = "[reduce](#reduce)\n[reduceInto](#reduce-into)\n[reject](#reject)\n"
        new = f"{first}\n{changed}"

        plan = _plan(old, new)

        self.assertEqual(len(plan.changes), 1)
        block_change = plan.changes[0]
        self.assertEqual(
            patch.diff_text(block_change),
            "+ [reduceInto](#reduce-into)",
        )
        self.assertEqual(block_change.old_source, first)
        self.assertEqual(patch.source_text(block_change), changed)

    def test_plan_inserts_between_visible_contexts_not_annotation_comments(self):
        """주석이 아닌 표시 문맥 사이에 새 블록을 삽입함."""

        before = "- [Before](#before)"
        after = "- [After](#after)"
        inserted = "- [Inserted](#inserted)"
        existing = (
            "<!--\n"
            f"{before}\n"
            f"{after}\n"
            "-->\n"
            f"{before}\n"
            f"{after}\n"
        )
        change = patch.BlockChange(
            old_lines=(),
            new_lines=(inserted,),
            before_context=before,
            after_context=after,
        )

        result = patch.apply_plan(
            existing,
            patch.PatchPlan((change,)),
            [f"{inserted}\n"],
        )

        self.assertEqual(
            result,
            (
                "<!--\n"
                f"{before}\n"
                f"{after}\n"
                "-->\n"
                f"{before}\n"
                f"{inserted}\n"
                f"{after}\n"
            ),
        )

    def test_blocks_parse_indented_multiline_comments_with_closing_content(self):
        """닫는 줄에 내용이 있는 들여쓰기 여러 줄 주석을 파싱함."""

        blocks = patch._blocks(  # noqa: SLF001
            "  <!--\n"
            "First line.\n"
            "Second line. -->\n"
            "번역입니다.\n"
        )

        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].comment, "First line. Second line.")

    def test_updates_unannotated_inline_code_identifier_list(self):
        """주석 없는 인라인 코드 식별자 목록을 갱신함."""

        old = (
            "Before.\n\n"
            "- `FirstEvent`\n"
            "- `LastEvent`\n\n"
            "After.\n"
        )
        new = old.replace(
            "- `LastEvent`",
            "- `AddedEvent`\n- `LastEvent`",
        )
        existing = (
            "<!-- Before. -->\n이전입니다.\n\n"
            "<!--\n"
            "- `FirstEvent`\n"
            "- `LastEvent`\n"
            "-->\n"
            "- `FirstEvent`\n"
            "- `LastEvent`\n\n"
            "<!-- After. -->\n이후입니다.\n"
        )

        result = patch.apply_plan(
            existing,
            _plan(old, new),
            ["- `FirstEvent`\n- `AddedEvent`\n- `LastEvent`"],
        )

        self.assertIn("- `FirstEvent`\n- `AddedEvent`\n- `LastEvent`", result)
        self.assertNotIn("<!--\n- `FirstEvent`", result)


class TableRowPatchTests(unittest.TestCase):
    """표 행 패치의 동작과 경계 조건을 검증함."""

    _OLD = (
        "Intro.\n\n| Name | Value |\n|---|---|\n"
        "| First | same |\n| Second | same |\n\nTail.\n"
    )

    def test_rejects_a_change_to_multiple_table_rows(self):
        """여러 표 행에 걸친 단일 변경을 거부함."""

        new = self._OLD.replace("First", "Changed first").replace(
            "Second", "Changed second"
        )

        with self.assertRaisesRegex(patch.PatchError, "exactly one"):
            _plan(self._OLD, new)

    def test_rejects_nonadjacent_row_changes_in_the_same_table(self):
        """같은 표에서 인접하지 않은 행 변경을 거부함."""

        old = (
            "| Name | Value |\n|---|---|\n"
            "| First | old |\n| Middle | same |\n| Last | old |\n"
        )
        new = old.replace("| First | old |", "| First | new |").replace(
            "| Last | old |", "| Last | new |"
        )

        with self.assertRaisesRegex(patch.PatchError, "exactly one"):
            _plan(old, new)

    def test_rejects_a_table_row_column_count_change(self):
        """표 행의 열 수 변경 거부를 검증함."""

        new = self._OLD.replace(
            "| First | same |",
            "| First | same | extra |",
        )

        with self.assertRaisesRegex(patch.PatchError, "same column count"):
            _plan(self._OLD, new)

    def test_rejects_a_table_separator_change(self):
        """표 구분선 변경 거부를 검증함."""

        new = self._OLD.replace("|---|---|", "|:---|---:|")

        with self.assertRaisesRegex(patch.PatchError, "non-separator"):
            _plan(self._OLD, new)

    def test_rejects_an_unsupported_admonition_marker_change(self):
        """지원하지 않는 알림 표식 변경 거부를 검증함."""

        old = "> [!NOTE]\n> Body.\n"
        new = "> [!INFO]\n> Body.\n"

        with self.assertRaisesRegex(patch.PatchError, "admonition marker"):
            _plan(old, new)

    def test_updates_only_the_intended_duplicate_tail_row(self):
        """중복된 마지막 행 중 의도한 행만 갱신함."""

        new = self._OLD.replace("| First | same |", "| Changed | same |")
        existing = (
            "<!-- Intro. -->\n소개.\n\n| Name | Value |\n|---|---|\n"
            "| First | same |\n| Second | same |\n\n<!-- Tail. -->\n꼬리.\n"
        )
        plan = _plan(self._OLD, new)

        first = patch.apply_plan(existing, plan, ["| 변경됨 | same |"])

        self.assertIn("| 변경됨 | same |", first)
        self.assertIn("| Second | same |", first)
        self.assertNotIn("| First | same |", first)
        self.assertEqual(
            patch.apply_plan(first, plan, ["| 변경됨 | same |"]), first
        )

    def test_single_tail_candidate_without_matching_row_fails_closed(self):
        # 로캘 표에 형제 행만 남은 경우 유일한 마지막 셀 후보를 덮어쓰지 않음.
        """행 내용이 다른 단일 꼬리 후보를 거부함."""

        new = self._OLD.replace("| First | same |", "| Changed | same |")
        existing = (
            "<!-- Intro. -->\n소개.\n\n| Name | Value |\n|---|---|\n"
            "| Second | same |\n\n<!-- Tail. -->\n꼬리.\n"
        )

        with self.assertRaisesRegex(
            patch.PatchError, "missing existing translation block"
        ):
            patch.apply_plan(existing, _plan(self._OLD, new), ["| 변경됨 | same |"])

    def test_translated_rows_resolve_by_source_table_ordinal(self):
        """번역된 행을 원문 표 순번으로 식별함."""

        old = (
            "Intro one.\n\n| Key | Meaning |\n|---|---|\n"
            "| `foo` | Old explanation |\n\n"
            "Intro two.\n\n| Key | Meaning |\n|---|---|\n"
            "| `foo` | Existing explanation |\n"
        )
        new = old.replace("Old explanation", "New explanation")
        existing = (
            "<!-- Intro one. -->\n소개 하나.\n\n| Key | Meaning |\n|---|---|\n"
            "| `foo` | 이전 설명 |\n\n"
            "<!-- Intro two. -->\n소개 둘.\n\n| Key | Meaning |\n|---|---|\n"
            "| `foo` | 기존 설명 |\n"
        )
        plan = _plan(old, new)

        self.assertIn(
            "| `foo` | 이전 설명 |",
            patch.existing_context(existing, plan.changes[0]),
        )

        first = patch.apply_plan(existing, plan, ["| `foo` | 새 설명 |"])

        self.assertIn("| `foo` | 새 설명 |", first)
        self.assertIn("| `foo` | 기존 설명 |", first)
        self.assertNotIn("이전 설명", first)
        self.assertEqual(
            patch.apply_plan(first, plan, ["| `foo` | 새 설명 |"]), first
        )

    def test_reordered_same_shape_tables_fail_closed_before_replacement(self):
        """형태가 같은 표의 순서 변경을 교체 전에 거부함."""

        old = (
            "| Key | Meaning |\n|---|---|\n| `foo` | Alpha old |\n\n"
            "| Key | Meaning |\n|---|---|\n| `foo` | Beta keep |\n"
        )
        new = old.replace("Alpha old", "Alpha new")
        existing = (
            "| 키 | 의미 |\n|---|---|\n| `foo` | 베타 유지 |\n\n"
            "| 키 | 의미 |\n|---|---|\n| `foo` | 알파 기존 |\n"
        )

        with self.assertRaises(patch.PatchError):
            patch.apply_plan(existing, _plan(old, new), ["| `foo` | 알파 신규 |"])

    def test_unique_all_cell_translated_row_uses_its_structural_address(self):
        """모든 셀이 번역된 고유 행에 구조 주소를 사용함."""

        old = (
            "Intro.\n\n| Key | Meaning |\n|---|---|\n"
            "| Old name | Old value |\n\nTail.\n"
        )
        new = old.replace(
            "| Old name | Old value |",
            "| New name | New value |",
        )
        existing = (
            "<!-- Intro. -->\n소개.\n\n| 키 | 의미 |\n|---|---|\n"
            "| 이전 이름 | 이전 값 |\n\n<!-- Tail. -->\n꼬리.\n"
        )
        translated = "| 새 이름 | 새 값 |"
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, [translated])

        self.assertIn(translated, first)
        self.assertNotIn("| 이전 이름 | 이전 값 |", first)
        self.assertEqual(patch.apply_plan(first, plan, [translated]), first)

    def test_all_cell_translated_row_with_two_tables_fails_closed(self):
        """두 표에서 모든 셀이 번역된 행의 모호성을 거부함."""

        old = (
            "| Key | Meaning |\n|---|---|\n| Old name | Old value |\n\n"
            "| Key | Meaning |\n|---|---|\n| Other name | Other value |\n"
        )
        new = old.replace(
            "| Old name | Old value |",
            "| New name | New value |",
        )
        existing = (
            "| 키 | 의미 |\n|---|---|\n| 이전 이름 | 이전 값 |\n\n"
            "| 키 | 의미 |\n|---|---|\n| 다른 이름 | 다른 값 |\n"
        )

        with self.assertRaises(patch.PatchError):
            patch.apply_plan(existing, _plan(old, new), ["| 새 이름 | 새 값 |"])

    def test_reordered_localized_table_rows_fail_closed(self):
        """로캘 표 행 순서가 바뀐 상태를 거부함."""

        old = (
            "Intro.\n\n| Key | Meaning |\n|---|---|\n"
            "| Foo | Old explanation |\n| Bar | Keep explanation |\n\nTail.\n"
        )
        new = old.replace("Old explanation", "New explanation")
        existing = (
            "<!-- Intro. -->\n소개.\n\n| 키 | 의미 |\n|---|---|\n"
            "| 바 | 유지 설명 |\n| 푸 | 이전 설명 |\n\n"
            "<!-- Tail. -->\n꼬리.\n"
        )

        for translated in ("| 푸 | 새 설명 |", "| 바 | 새 설명 |"):
            with self.subTest(translated=translated):
                with self.assertRaises(patch.PatchError):
                    patch.apply_plan(existing, _plan(old, new), [translated])

    def test_locale_only_preceding_table_fails_closed(self):
        """로캘 전용 선행 표로 구조 순번이 이동한 상태를 거부함."""

        old = (
            "Before.\n\n| Key | Value |\n|---|---|\n"
            "| First | Stable |\n\n"
            "Middle.\n\n| Key | Value |\n|---|---|\n"
            "| Target old | Stable |\n\nAfter.\n"
        )
        new = old.replace("| Target old | Stable |", "| Target new | Stable |")
        existing = (
            "| 추가 | 표 |\n|---|---|\n| 미끼 | 안정 |\n\n"
            "<!-- Before. -->\n이전입니다.\n\n"
            "| 키 | 값 |\n|---|---|\n| 첫째 | 안정 |\n\n"
            "<!-- Middle. -->\n중간입니다.\n\n"
            "| 키 | 값 |\n|---|---|\n| 대상 기존 | 안정 |\n\n"
            "<!-- After. -->\n이후입니다.\n"
        )

        with self.assertRaises(patch.PatchError):
            patch.apply_plan(
                existing,
                _plan(old, new),
                ["| 대상 신규 | 안정 |"],
            )

    def test_drifted_locale_row_count_fails_closed(self):
        """로캘 표 행 수가 분기된 상태를 거부함."""

        old = (
            "Intro one.\n\n| Key | Meaning |\n|---|---|\n"
            "| `foo` | Old explanation |\n"
        )
        new = old.replace("Old explanation", "New explanation")
        existing = (
            "<!-- Intro one. -->\n소개 하나.\n\n| Key | Meaning |\n|---|---|\n"
            "| `foo` | 이전 설명 |\n| `bar` | 추가 행 |\n"
        )

        with self.assertRaises(patch.PatchError):
            patch.apply_plan(existing, _plan(old, new), ["| `foo` | 새 설명 |"])

    def test_candidates_exclude_rows_inside_code_fences(self):
        """펜스 코드 내부에서 표 형태인 줄을 후보에서 제외함."""

        old = (
            "Intro.\n\n| Key | State |\n|---|---|\n| `old` | Available |\n\n"
            "```text\n| `old` | Available |\n```\n\nTail.\n"
        )
        new = old.replace("| `old` | Available |", "| `new` | Available |", 1)
        existing = (
            "<!-- Intro. -->\n소개.\n\n| Key | State |\n|---|---|\n"
            "| `old` | 사용 가능 |\n\n"
            "```text\n| `old` | Available |\n```\n\n<!-- Tail. -->\n꼬리.\n"
        )
        plan = _plan(old, new)

        first = patch.apply_plan(existing, plan, ["| `new` | 사용 가능 |"])

        self.assertIn("| `new` | 사용 가능 |", first)
        self.assertIn("```text\n| `old` | Available |\n```", first)
        self.assertEqual(
            patch.apply_plan(first, plan, ["| `new` | 사용 가능 |"]), first
        )


class AdmonitionMarkerTests(unittest.TestCase):
    """알림 표식의 동작과 경계 조건을 검증함."""

    def test_apply_preserves_duplicate_markers_outside_the_plan(self):
        """계획 범위 밖에 있는 중복 표식을 보존함."""

        old = "Old paragraph.\n\nAfter.\n"
        new = "New paragraph.\n\nAfter.\n"
        existing = (
            "> [!NOTE]\n"
            "> [!NOTE]\n"
            "> Existing content outside the plan.\n\n"
            "<!-- Old paragraph. -->\n"
            "기존 문단입니다.\n\n"
            "<!-- After. -->\n"
            "뒤 문단입니다.\n"
        )
        translated = "<!-- New paragraph. -->\n새 문단입니다.\n"

        result = patch.apply_plan(existing, _plan(old, new), [translated])

        self.assertIn("> [!NOTE]\n> [!NOTE]", result)
        self.assertIn("새 문단입니다.", result)

    def test_apply_does_not_duplicate_admonition_marker(self):
        # `NOTE` 본문만 바뀌어 표식 줄은 문맥으로 유지함.
        # 모델이 번역 결과에 표식을 다시 출력하더라도 기존 표식 뒤의 중복 표식을 제거함.
        """적용 과정에서 알림 표식 중복을 방지함."""

        old = (
            "The basic workflow paragraph.\n\n"
            "> [!NOTE]\n"
            "> Vector search requires a PostgreSQL database.\n\n"
            '<a name="generating-embeddings"></a>\n'
            "### Generating Embeddings\n"
        )
        new = old.replace(
            "> Vector search requires a PostgreSQL database.",
            "> Vector search requires the AI SDK and PostgreSQL or MongoDB.",
        )
        existing = (
            "<!-- The basic workflow paragraph. -->\n"
            "기본 워크플로 문단입니다.\n\n"
            "> [!NOTE]\n"
            "> 벡터 검색은 PostgreSQL 데이터베이스가 필요합니다.\n\n"
            '<a name="generating-embeddings"></a>\n'
            "<!-- ### Generating Embeddings -->\n"
            "### Generating Embeddings\n"
        )
        translated = (
            "> [!NOTE]\n"
            "> <!-- Vector search requires the AI SDK and PostgreSQL or MongoDB. -->\n"
            "> 벡터 검색에는 AI SDK가 필요하며 PostgreSQL 또는 MongoDB를 지원합니다.\n"
        )

        result = patch.apply_segments(existing, _segments(old, new), [translated])

        self.assertNotIn("> [!NOTE]\n> [!NOTE]", result)
        self.assertEqual(result.count("> [!NOTE]"), 1)

    def test_marker_flip_requires_provider_translation_and_updates_gfm_locale(self):
        """표식 전환 시 번역 출력을 요구하고 GFM 로캘을 갱신함."""

        old = (
            '<a name="s"></a>\n#### Remembering\n\n'
            "> [!NOTE]\n> Keep body here.\n\nTail prose.\n"
        )
        new = old.replace("> [!NOTE]", "> [!WARNING]")
        plan = _plan(old, new)
        self.assertFalse(plan.changes[0].provider_free)
        existing = (
            '<a name="s"></a>\n<!-- #### Remembering -->\n#### 기억하기\n\n'
            "> [!NOTE]\n> 본문을 유지합니다.\n\n"
            "<!-- Tail prose. -->\n꼬리 문단.\n"
        )
        translated = "> [!WARNING]\n> 본문을 유지합니다."

        first = patch.apply_plan(existing, plan, [translated])

        self.assertIn("> [!WARNING]\n> 본문을 유지합니다.", first)
        self.assertNotIn("> [!NOTE]", first)
        self.assertEqual(patch.apply_plan(first, plan, [translated]), first)

    def test_marker_flip_converts_a_legacy_locale_admonition(self):
        """기존 로캘 알림 블록을 새 표식으로 변환함."""

        old = (
            '<a name="s"></a>\n#### Remembering\n\n'
            "> [!NOTE]\n> Keep body here.\n\nTail prose.\n"
        )
        new = old.replace("> [!NOTE]", "> [!WARNING]")
        existing = (
            '<a name="s"></a>\n<!-- #### Remembering -->\n#### 기억하기\n\n'
            "> **참고:** 본문을 유지합니다.\n\n"
            "<!-- Tail prose. -->\n꼬리 문단.\n"
        )
        plan = _plan(old, new)
        translated = "> [!WARNING]\n> 본문을 유지합니다."

        first = patch.apply_plan(existing, plan, [translated])

        self.assertIn("> [!WARNING]\n> 본문을 유지합니다.", first)
        self.assertNotIn("> **참고:**", first)
        self.assertEqual(patch.apply_plan(first, plan, [translated]), first)

    def test_marker_flip_rejects_a_marker_only_replacement_for_a_quote_body(self):
        """일반 인용 본문에 표식만 적용하는 교체를 거부함."""

        old = "Before.\n\n> [!NOTE]\n> Source body.\n\nAfter.\n"
        new = old.replace("[!NOTE]", "[!WARNING]")
        existing = (
            "<!-- Before. -->\n이전.\n\n"
            "> [!NOTE]\n> 관련 없는 본문.\n\n"
            "<!-- After. -->\n이후.\n"
        )

        with self.assertRaisesRegex(patch.PatchError, "admonition body"):
            patch.apply_plan(
                existing,
                _plan(old, new),
                ["> [!WARNING]"],
            )

    def test_marker_flip_retranslates_the_selected_localized_admonition(self):
        """선택한 현지화 알림 블록을 표식 전환과 함께 다시 번역함."""

        old = (
            "Before.\n\n"
            "> [!NOTE]\n> First body.\n\n"
            "Middle.\n\n"
            "> [!NOTE]\n> Second body.\n\n"
            "After.\n"
        )
        new = old.replace(
            "> [!NOTE]\n> Second body.",
            "> [!WARNING]\n> Second body.",
        )
        existing = (
            "<!-- Before. -->\n이전 문단.\n\n"
            "> [!NOTE]\n> 첫째 본문.\n\n"
            "<!-- Middle. -->\n중간 문단.\n\n"
            "> [!NOTE]\n> 둘째 본문.\n\n"
            "<!-- After. -->\n다음 문단.\n"
        )

        result = patch.apply_plan(
            existing,
            _plan(old, new),
            ["> [!WARNING]\n> 둘째 본문."],
        )

        self.assertIn("> [!NOTE]\n> 첫째 본문.", result)
        self.assertIn("> [!WARNING]\n> 둘째 본문.", result)

    def test_marker_flip_is_addressed_against_the_old_admonition_set(self):
        """기존 알림 블록 집합에서 표식 전환 주소를 판정함."""

        old = (
            "Before.\n\n"
            "> [!NOTE]\n> Existing body.\n\n"
            "Middle one.\n\nMiddle two.\n\nMiddle three.\n\n"
            "After.\n"
        )
        new = old.replace("> [!NOTE]", "> [!WARNING]").replace(
            "After.",
            "After.\n\n> [!TIP]\n> Newly inserted body.",
        )
        plan = _plan(old, new)
        marker_change = next(
            change
            for change in plan.changes
            if change.is_admonition_marker_change
        )
        existing = (
            "<!-- Before. -->\n이전 문단.\n\n"
            "> [!NOTE]\n> 기존 본문.\n\n"
            "<!-- Middle one. -->\n중간 하나.\n\n"
            "<!-- Middle two. -->\n중간 둘.\n\n"
            "<!-- Middle three. -->\n중간 셋.\n\n"
            "<!-- After. -->\n다음 문단.\n"
        )
        translated = "> [!WARNING]\n> 기존 본문."

        self.assertEqual(
            patch.existing_context(existing, marker_change),
            "> [!NOTE]\n> 기존 본문.",
        )
        result = patch.apply_plan(
            existing,
            plan,
            [translated, "> [!TIP]\n> 새로 삽입한 본문."],
        )

        self.assertIn("> [!WARNING]\n> 기존 본문.", result)
        self.assertIn("> [!TIP]\n> 새로 삽입한 본문.", result)

    def test_marker_flip_accepts_an_already_target_admonition_set(self):
        """이미 대상 상태인 알림 표식 집합을 허용함."""

        old = (
            "Before.\n\n"
            "> [!NOTE]\n> Existing body.\n\n"
            "After.\n"
        )
        new = old.replace("> [!NOTE]", "> [!WARNING]").replace(
            "After.",
            "After.\n\n> [!TIP]\n> Newly inserted body.",
        )
        marker_change = next(
            change
            for change in _plan(old, new).changes
            if change.is_admonition_marker_change
        )
        existing = (
            "<!-- Before. -->\n이전 문단.\n\n"
            "> [!WARNING]\n> 기존 본문.\n\n"
            "<!-- After. -->\n다음 문단.\n\n"
            "> [!TIP]\n> 새로 삽입한 본문.\n"
        )

        self.assertEqual(
            patch.existing_context(existing, marker_change),
            "> [!WARNING]\n> 기존 본문.",
        )
        self.assertEqual(
            patch.apply_segments(
                existing,
                [marker_change],
                ["> [!WARNING]\n> 기존 본문."],
            ),
            existing,
        )

    def test_marker_flip_does_not_treat_bold_quote_label_as_admonition(self):
        """굵은 인용 레이블을 알림 블록으로 오인하지 않음."""

        old = "> [!NOTE]\n> Old guidance.\n"
        new = "> [!WARNING]\n> Old guidance.\n"
        existing = "> **Question:** unrelated text.\n"

        with self.assertRaisesRegex(
            patch.PatchError, "existing admonition marker"
        ):
            patch.apply_plan(
                existing,
                _plan(old, new),
                ["> [!WARNING]\n"],
            )

    def test_reordered_localized_admonition_bodies_fail_closed(self):
        """로캘 알림 본문 순서가 바뀐 상태를 거부함."""

        old = (
            "Before.\n\n"
            "> [!NOTE]\n> First body.\n\n"
            "Middle.\n\n"
            "> [!NOTE]\n> Second body.\n\n"
            "After.\n"
        )
        new = old.replace(
            "> [!NOTE]\n> Second body.",
            "> [!WARNING]\n> Second body.",
        )
        existing = (
            "<!-- Before. -->\n이전 문단.\n\n"
            "> [!NOTE]\n> 둘째 본문.\n\n"
            "<!-- Middle. -->\n중간 문단.\n\n"
            "> [!NOTE]\n> 첫째 본문.\n\n"
            "<!-- After. -->\n다음 문단.\n"
        )

        with self.assertRaisesRegex(patch.PatchError, "admonition body"):
            patch.apply_plan(existing, _plan(old, new), ["> [!WARNING]"])

    def test_admonition_body_swapped_with_plain_quote_fails_closed(self):
        """알림 본문과 일반 인용문이 바뀐 상태를 거부함."""

        old = (
            "Before.\n\n"
            "> Plain body.\n\n"
            "Middle.\n\n"
            "> [!NOTE]\n> Note body.\n\n"
            "After.\n"
        )
        new = old.replace("> [!NOTE]", "> [!WARNING]")
        existing = (
            "<!-- Before. -->\n이전 문단.\n\n"
            "> 메모 본문.\n\n"
            "<!-- Middle. -->\n중간 문단.\n\n"
            "> [!NOTE]\n> 일반 본문.\n\n"
            "<!-- After. -->\n다음 문단.\n"
        )

        with self.assertRaisesRegex(patch.PatchError, "admonition body"):
            patch.apply_plan(existing, _plan(old, new), ["> [!WARNING]"])

    def test_marker_flip_with_a_drifted_marker_fails_closed(self):
        """로캘 표식이 분기된 알림 변경을 거부함."""

        old = (
            '<a name="s"></a>\n#### Remembering\n\n'
            "> [!NOTE]\n> Keep body here.\n\nTail prose.\n"
        )
        new = old.replace("> [!NOTE]", "> [!WARNING]")
        existing = (
            '<a name="s"></a>\n<!-- #### Remembering -->\n#### 기억하기\n\n'
            "> [!TIP]\n> 본문을 유지합니다.\n\n"
            "<!-- Tail prose. -->\n꼬리 문단.\n"
        )

        with self.assertRaisesRegex(patch.PatchError, "admonition marker"):
            patch.apply_plan(existing, _plan(old, new), ["> [!WARNING]"])

    def test_marker_flip_rejects_a_legacy_third_type(self):
        """표식 전환에서 기존의 제3 알림 유형을 거부함."""

        old = (
            "Before.\n\n"
            "> [!NOTE]\n> Source body.\n\n"
            "Middle.\n\n"
            "> Plain quote.\n"
        )
        new = old.replace("> [!NOTE]", "> [!WARNING]", 1)
        existing = (
            "<!-- Before. -->\n이전.\n\n"
            "> **Caution:**\n"
            "> <!-- Source body. -->\n"
            "> 번역 본문.\n\n"
            "<!-- Middle. -->\n중간.\n\n"
            "> 다른 인용문.\n"
        )

        with self.assertRaisesRegex(patch.PatchError, "admonition marker"):
            patch.apply_plan(existing, _plan(old, new), ["> [!WARNING]"])

    def test_marker_flip_preserves_markdown_container_indentation(self):
        """표식 전환 시 마크다운 컨테이너 들여쓰기를 보존함."""

        old = "  > [!NOTE]\n  > Source body.\n"
        new = old.replace("[!NOTE]", "[!WARNING]")
        existing = "  > [!NOTE]\n  > 번역 본문.\n"

        result = patch.apply_plan(
            existing,
            _plan(old, new),
            ["  > [!WARNING]\n  > 번역 본문."],
        )

        self.assertEqual(result, "  > [!WARNING]\n  > 번역 본문.\n")


if __name__ == "__main__":
    unittest.main()
