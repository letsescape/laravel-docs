"""annotate 동작과 경계 조건 검증."""

import io
import tempfile
import unittest
from collections import Counter
from contextlib import redirect_stderr
from unittest.mock import patch

import annotate_cli
from sync import annotate, postprocess, verify
from sync.verification.document import build_expected_annotation_map


class CanonicalAnnotationTests(unittest.TestCase):
    """canonical annotation 동작과 경계 조건 테스트 모음."""

    def test_uses_exact_pre_stale_owner_bytes_for_every_owner_shape(self):
        """구조 정렬 기준인 후처리 영어 문서와 별개로 모든 소유자 형태의 원문 바이트를 정확히 사용하는지 검증."""

        source = (
            "## Title {.class #stable}\n\n"
            "First physical line\ncontinues with <img src=\"x\">.\n\n"
            "| Name | Value |\n"
            "| --- | --- |\n"
            "| Widget | enabled |\n"
        )
        english_view = postprocess.postprocess(source, "13.x", {})
        locale = (
            "## Title {#stable}\n\n"
            "첫 물리 줄이\n이어지는 <img src=\"x\"/> 설명입니다.\n\n"
            "| 이름 | 값 |\n"
            "| --- | --- |\n"
            "| Widget | 활성 |\n"
        )

        out, drifts = annotate.annotate(
            source,
            locale,
            "13.x",
            canonical=True,
            alignment_source=english_view,
            preserved_comment_indexes=frozenset(),
        )
        expected = build_expected_annotation_map(source)

        self.assertEqual(drifts, [])
        for entry in expected.entries:
            self.assertEqual(out.count(entry.annotation), 1)
        self.assertIn("<!-- ## Title {.class #stable} -->", out)
        self.assertIn('continues with <img src="x">. -->', out)
        self.assertNotIn('continues with <img src="x"/>. -->', out)
        self.assertIn(
            "<!-- | Name | Value | | --- | --- | | Widget | enabled | -->",
            out,
        )


class AnnotateCliTests(unittest.TestCase):
    """annotate CLI 동작과 경계 조건 테스트 모음."""

    def test_rejects_invalid_version_before_reading_documents(self):
        """문서를 읽기 전에 잘못된 버전을 거부하는지 검증."""

        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            annotate_cli.sys,
            "argv",
            ["annotate_cli.py", "../../outside", "example.md"],
        ), patch.object(
            annotate_cli.Path,
            "read_text",
            side_effect=AssertionError("documents should not be read"),
        ):
            exit_code = annotate_cli.main()

        self.assertEqual(exit_code, 2)
        self.assertIn("invalid version", stderr.getvalue())

    def test_rejects_nested_document_name_before_reading_documents(self):
        """문서를 읽기 전에 중첩된 문서 이름을 거부하는지 검증."""

        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            annotate_cli.sys,
            "argv",
            ["annotate_cli.py", "12.x", "../example.md"],
        ), patch.object(
            annotate_cli.Path,
            "read_text",
            side_effect=AssertionError("documents should not be read"),
        ):
            exit_code = annotate_cli.main()

        self.assertEqual(exit_code, 2)
        self.assertIn("invalid document", stderr.getvalue())

    def test_rejects_non_markdown_document_before_reading_documents(self):
        """문서를 읽기 전에 Markdown이 아닌 문서를 거부하는지 검증."""

        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            annotate_cli.sys,
            "argv",
            ["annotate_cli.py", "12.x", "example.txt"],
        ), patch.object(
            annotate_cli.Path,
            "read_text",
            side_effect=AssertionError("documents should not be read"),
        ):
            exit_code = annotate_cli.main()

        self.assertEqual(exit_code, 2)
        self.assertIn("invalid document", stderr.getvalue())

    def test_rejects_empty_markdown_basename_before_reading_documents(self):
        """문서를 읽기 전에 비어 있는 Markdown 기본 이름을 거부하는지 검증."""

        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            annotate_cli.sys,
            "argv",
            ["annotate_cli.py", "12.x", ".md"],
        ), patch.object(
            annotate_cli.Path,
            "read_text",
            side_effect=AssertionError("documents should not be read"),
        ):
            exit_code = annotate_cli.main()

        self.assertEqual(exit_code, 2)
        self.assertIn("invalid document", stderr.getvalue())

    def test_rejects_symlinked_locale_root_before_write(self):
        """쓰기 전에 심볼릭 링크인 로캘 루트를 거부하는지 검증."""

        stderr = io.StringIO()

        with tempfile.TemporaryDirectory() as tmp:
            root = annotate_cli.Path(tmp)
            en_root = root / "i18n/en/docusaurus-plugin-content-docs"
            (en_root / "version-12.x").mkdir(parents=True)
            internal = root / "internal-versioned-docs"
            (internal / "version-12.x").mkdir(parents=True)
            (root / "versioned_docs").symlink_to(
                internal,
                target_is_directory=True,
            )

            with redirect_stderr(stderr), patch.object(
                annotate_cli,
                "REPO",
                root,
            ), patch.object(
                annotate_cli.sys,
                "argv",
                ["annotate_cli.py", "12.x", "example.md", "--write"],
            ), patch.object(
                annotate_cli.Path,
                "read_text",
                side_effect=AssertionError("documents should not be read"),
            ), patch.object(
                annotate_cli.Path,
                "write_text",
                side_effect=AssertionError("documents should not be written"),
            ):
                exit_code = annotate_cli.main()

        self.assertEqual(exit_code, 2)
        self.assertIn("invalid locale root", stderr.getvalue())

    def test_rejects_symlinked_locale_root_parent(self):
        """심볼릭 링크인 로캘 루트 상위 디렉터리를 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            repo = annotate_cli.Path(tmp)
            (repo / "i18n").mkdir()
            internal = repo / "internal-ja"
            locale_root = internal / "docusaurus-plugin-content-docs"
            (locale_root / "version-12.x").mkdir(parents=True)
            (repo / "i18n/ja").symlink_to(
                internal,
                target_is_directory=True,
            )

            with patch.object(annotate_cli, "REPO", repo):
                with self.assertRaisesRegex(ValueError, "invalid locale root"):
                    annotate_cli._document_path(
                        repo / "i18n/ja/docusaurus-plugin-content-docs",
                        "12.x",
                        "example.md",
                    )

    def test_rejects_symlinked_version_root_with_internal_target(self):
        """로캘 루트 내부 경로를 가리키더라도 심볼릭 링크인 버전 루트를 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            repo = annotate_cli.Path(tmp)
            locale_root = repo / "versioned_docs"
            internal = locale_root / "internal-version"
            internal.mkdir(parents=True)
            (locale_root / "version-12.x").symlink_to(
                internal,
                target_is_directory=True,
            )

            with patch.object(annotate_cli, "REPO", repo):
                with self.assertRaisesRegex(ValueError, "invalid document path"):
                    annotate_cli._document_path(
                        locale_root,
                        "12.x",
                        "example.md",
                    )

    def test_rejects_symlinked_document_with_internal_target(self):
        """로캘 루트 내부 파일을 가리키더라도 심볼릭 링크인 문서를 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            repo = annotate_cli.Path(tmp)
            locale_root = repo / "versioned_docs"
            version_root = locale_root / "version-12.x"
            version_root.mkdir(parents=True)
            target = locale_root / "shared.md"
            target.write_text("shared", encoding="utf-8")
            (version_root / "example.md").symlink_to(target)

            with patch.object(annotate_cli, "REPO", repo):
                with self.assertRaisesRegex(ValueError, "invalid document path"):
                    annotate_cli._document_path(
                        locale_root,
                        "12.x",
                        "example.md",
                    )

    def test_rejects_unexpected_lexical_locale_root(self):
        """허용 목록에 없는 로캘 루트 경로를 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            repo = annotate_cli.Path(tmp)
            locale_root = repo / "internal-versioned-docs"
            (locale_root / "version-12.x").mkdir(parents=True)

            with patch.object(annotate_cli, "REPO", repo):
                with self.assertRaisesRegex(ValueError, "unexpected locale root"):
                    annotate_cli._document_path(
                        locale_root,
                        "12.x",
                        "example.md",
                    )

    def test_rejects_document_path_outside_locale_root_before_reading(self):
        """읽기 전에 로캘 루트 밖의 문서 경로를 거부하는지 검증."""

        stderr = io.StringIO()

        with tempfile.TemporaryDirectory() as tmp:
            root = annotate_cli.Path(tmp)
            en_root = (
                root / "i18n/en/docusaurus-plugin-content-docs"
            )
            en_root.mkdir(parents=True)
            outside = root / "outside"
            outside.mkdir()
            (en_root / "version-12.x").symlink_to(outside, target_is_directory=True)

            with redirect_stderr(stderr), patch.object(
                annotate_cli,
                "REPO",
                root,
            ), patch.object(
                annotate_cli.sys,
                "argv",
                ["annotate_cli.py", "12.x", "example.md"],
            ), patch.object(
                annotate_cli.Path,
                "read_text",
                side_effect=AssertionError("documents should not be read"),
            ):
                exit_code = annotate_cli.main()

        self.assertEqual(exit_code, 2)
        self.assertIn("document path escapes locale root", stderr.getvalue())

    def test_write_replaces_hardlink_without_mutating_other_name(self):
        """하드 링크인 로캘 문서를 새 파일로 교체하고 기존 링크 대상은 변경하지 않는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = annotate_cli.Path(tmp)
            en = (
                root
                / "i18n/en/docusaurus-plugin-content-docs"
                / "version-12.x/example.md"
            )
            en.parent.mkdir(parents=True)
            en.write_text("# Example\n", encoding="utf-8")
            victim = root / "outside.md"
            victim.write_text("# Example\n", encoding="utf-8")
            ko = root / "versioned_docs/version-12.x/example.md"
            ko.parent.mkdir(parents=True)
            ko.hardlink_to(victim)

            with patch.object(
                annotate_cli,
                "REPO",
                root,
            ), patch.object(
                annotate_cli.sys,
                "argv",
                ["annotate_cli.py", "12.x", "example.md", "--write"],
            ):
                exit_code = annotate_cli.main()

            self.assertEqual(exit_code, 0)
            self.assertEqual(victim.read_text(encoding="utf-8"), "# Example\n")
            self.assertEqual(
                ko.read_text(encoding="utf-8"),
                "<!-- # Example -->\n# Example\n",
            )
            self.assertFalse(ko.samefile(victim))

    def test_reports_unresolvable_document_path_without_traceback(self):
        """해결할 수 없는 문서 경로에서 종료 코드 2와 오류 메시지를 반환하는지 검증."""

        stderr = io.StringIO()

        with tempfile.TemporaryDirectory() as tmp:
            root = annotate_cli.Path(tmp)
            en_root = root / "i18n/en/docusaurus-plugin-content-docs"
            en_root.mkdir(parents=True)
            (en_root / "version-12.x").symlink_to(
                "version-12.x",
                target_is_directory=True,
            )

            with redirect_stderr(stderr), patch.object(
                annotate_cli,
                "REPO",
                root,
            ), patch.object(
                annotate_cli.sys,
                "argv",
                ["annotate_cli.py", "12.x", "example.md"],
            ), patch.object(
                annotate_cli.Path,
                "read_text",
                side_effect=AssertionError("documents should not be read"),
            ):
                exit_code = annotate_cli.main()

        self.assertEqual(exit_code, 2)
        self.assertIn("invalid document path", stderr.getvalue())


class AnnotateTests(unittest.TestCase):
    """annotate 동작과 경계 조건 테스트 모음."""

    def test_emits_source_comment_when_content_present_but_block_misaligned(self):
        # 번역문이 링크를 포함한 내용을 유지해도 목록 구조가 없으면 블록 정렬 불일치
        # "missing original comment" 오류 방지를 위해 영어 주석 출력 필요
        """내용은 있지만 블록 정렬이 어긋날 때 원문 주석을 출력하는지 검증."""

        en = (
            "- [One](https://a.test/one) first item.\n"
            "- [Two](https://a.test/two) second item.\n"
        )
        ko = (
            "<!-- placeholder. -->\n"
            "[One](https://a.test/one) 첫째 항목.\n"
            "[Two](https://a.test/two) 둘째 항목.\n"
        )
        out, _drifts = annotate.annotate(en, ko, "13.x")
        self.assertTrue(
            not (
                Counter(verify._required_comments(en))  # noqa: SLF001
                - Counter(verify._translated_comments(out))  # noqa: SLF001
            )
        )

    def test_keeps_drift_when_content_is_genuinely_untranslated(self):
        # 축어적 표식 없는 새 문단은 번역문에서 실제로 누락된 상태
        # drift를 계속 보고하고 불완전한 문서를 거부하려면 억지 보완 금지
        """실제로 누락된 미번역 원문에 대한 drift를 유지하는지 검증."""

        en = "Body text.\n\nNew untranslated paragraph.\n"
        ko = "<!-- Body text. -->\n본문입니다.\n"
        out, drifts = annotate.annotate(en, ko, "13.x")
        self.assertFalse(
            not (
                Counter(verify._required_comments(en))  # noqa: SLF001
                - Counter(verify._translated_comments(out))  # noqa: SLF001
            )
        )
        self.assertTrue(any(d.op == "delete" for d in drifts))

    def test_inserts_original_english_comments_without_rewriting_translation(self):
        """번역문을 다시 쓰지 않고 원문 영어 주석을 삽입하는지 검증."""

        en = "# Installation\n\nInstall Laravel with Composer.\n"
        ko = "# 설치 (Installation)\n\nComposer로 Laravel을 설치합니다.\n"

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertEqual(
            out,
            "<!-- # Installation -->\n"
            "# 설치 (Installation)\n\n"
            "<!-- Install Laravel with Composer. -->\n"
            "Composer로 Laravel을 설치합니다.\n",
        )

    def test_reports_drift_when_source_has_unmatched_text_block(self):
        """대응하지 않는 원문 텍스트 블록을 drift로 보고하는지 검증."""

        en = "# Installation\n\nInstall Laravel with Composer.\n\nRun the server.\n"
        ko = "# 설치 (Installation)\n\nComposer로 Laravel을 설치합니다.\n"

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertIn("<!-- # Installation -->", out)
        self.assertEqual(len(drifts), 1)
        self.assertEqual(drifts[0].op, "delete")
        self.assertEqual(drifts[0].en_lines, ["Run the server."])

    def test_replaces_version_placeholder_in_inserted_comments(self):
        """삽입한 원문 주석의 version placeholder를 대상 버전으로 치환하는지 검증."""

        en = "See [Routing](/docs/{{version}}/routing)."
        ko = "[라우팅](/docs/12.x/routing)을 참고하세요."

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertIn("<!-- See [Routing](/docs/12.x/routing). -->", out)

    def test_does_not_insert_comments_for_toc_link_lists(self):
        """목차 링크 목록에는 주석을 삽입하지 않는지 검증."""

        en = "# Concurrency\n\n- [Introduction](#introduction)\n\n<a name=\"introduction\"></a>\n## Introduction\n"
        ko = "# 동시 실행 (Concurrency)\n\n- [소개](#introduction)\n\n<a name=\"introduction\"></a>\n## 소개 (Introduction)\n"

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertNotIn("<!-- - [Introduction](#introduction) -->", out)
        self.assertIn("- [소개](#introduction)", out)
        self.assertIn("<!-- ## Introduction -->", out)

    def test_does_not_insert_comments_for_standalone_html_tags(self):
        """단독 HTML 태그에는 주석을 삽입하지 않는지 검증."""

        en = '<div class="grid">\n\nBody.\n\n</div>\n'
        ko = '<div class="grid">\n\n본문입니다.\n\n</div>\n'

        out, drifts = annotate.annotate(en, ko, "13.x")

        self.assertEqual(drifts, [])
        self.assertNotIn('<!-- <div class="grid"> -->', out)
        self.assertNotIn("<!-- </div> -->", out)
        self.assertIn("<!-- Body. -->", out)

    def test_preserves_trailing_blank_line_count(self):
        """뒤따르는 빈 줄 수를 보존하는지 검증."""

        en = "# Example\n\nBody.\n\n"
        ko = "# 예제\n\n본문.\n\n"

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertTrue(out.endswith("\n\n"))

    def test_replaces_existing_original_comments_when_reannotating(self):
        """재annotation 시 기존 원문 주석을 현재 영어 원문으로 교체하는지 검증."""

        en = "# Updated\n\nUpdated body.\n"
        ko = "<!-- # Old -->\n# 예제\n\n<!-- Old body. -->\n본문.\n"

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertNotIn("<!-- # Old -->", out)
        self.assertNotIn("<!-- Old body. -->", out)
        self.assertIn("<!-- # Updated -->", out)
        self.assertIn("<!-- Updated body. -->", out)

    def test_aligns_paragraph_after_list_without_blank_line(self):
        """빈 줄 없는 번역 목록 뒤 문단을 원문 문단과 정렬하는지 검증."""

        en = (
            "- First item.\n"
            "- Second item.\n"
            "\n"
            "Paragraph after list.\n"
        )
        ko = (
            "- 첫 번째 항목입니다.\n"
            "- 두 번째 항목입니다.\n"
            "목록 뒤 문단입니다.\n"
        )

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertIn("<!-- Paragraph after list. -->", out)

    def test_aligns_paragraph_after_parenthesized_ordered_list(self):
        """괄호형 순서 목록 뒤 문단을 원문 문단과 정렬하는지 검증."""

        en = (
            "1) First item.\n"
            "2) Second item.\n"
            "\n"
            "Paragraph after list.\n"
        )
        ko = (
            "1) 첫 번째 항목입니다.\n"
            "2) 두 번째 항목입니다.\n"
            "목록 뒤 문단입니다.\n"
        )

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertIn("<!-- Paragraph after list. -->", out)

    def test_places_html_body_comment_inside_structural_wrapper(self):
        """구조용 HTML wrapper 내부에 본문 원문 주석을 배치하는지 검증."""

        en = (
            '<button type="submit">\n'
            '    Submit\n'
            '</button>\n'
        )
        ko = (
            '<button type="submit">\n'
            '    제출\n'
            '</button>\n'
        )

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertEqual(
            out,
            '<button type="submit">\n'
            '<!--     Submit -->\n'
            '    제출\n'
            '</button>\n',
        )

    def test_keeps_blade_directive_example_lines_in_one_original_comment(self):
        """Blade directive 예시 줄을 하나의 원문 주석으로 유지하는지 검증."""

        en = (
            "@once\n"
            "    @push('scripts')\n"
            "        <script>\n"
            "            // Your custom JavaScript...\n"
            "        </script>\n"
            "    @endpush\n"
            "@endonce\n"
        )
        ko = en

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertIn(
            "<!--\n"
            "@once\n"
            "    @push('scripts')\n"
            "        <script>\n"
            "            // Your custom JavaScript...\n"
            "        </script>\n"
            "    @endpush\n"
            "@endonce\n"
            "-->",
            out,
        )

    def test_keeps_collection_link_list_separate_from_closing_div(self):
        """컬렉션 링크 목록을 닫는 div와 분리해 유지하는지 검증."""

        en = (
            '<div class="collection-method-list" markdown="1">\n'
            "\n"
            "[Arr::accessible](#method-array-accessible)\n"
            "[Arr::add](#method-array-add)\n"
            "</div>\n"
        )
        ko = en

        out, drifts = annotate.annotate(en, ko, "master")

        self.assertEqual(drifts, [])
        self.assertNotIn("missing original comment", verify.verify(out, source=en))
        self.assertIn(
            "<!--\n"
            "[Arr::accessible](#method-array-accessible)\n"
            "[Arr::add](#method-array-add)\n"
            "-->",
            out,
        )
        self.assertNotIn("[Arr::add](#method-array-add)\n</div>\n-->", out)

    def test_places_blankless_body_comment_inside_html_wrapper(self):
        """빈 줄 없는 HTML wrapper 내부에 본문 원문 주석을 배치하는지 검증."""

        source = '<div class="content-list">\nBody.\n</div>\n'

        out, drifts = annotate.annotate(source, source, "13.x")

        self.assertEqual(drifts, [])
        self.assertEqual(
            out,
            '<div class="content-list">\n'
            "<!-- Body. -->\n"
            "Body.\n"
            "</div>\n",
        )

    def test_keeps_yaml_key_and_following_list_in_one_original_comment(self):
        """YAML 키와 이어지는 목록을 하나의 원문 주석으로 유지하는지 검증."""

        en = (
            "features:\n"
            "- docker: true\n"
            "- elasticsearch:\n"
            "    version: 7.9.0\n"
        )
        ko = en

        out, drifts = annotate.annotate(en, ko, "8.x")

        self.assertEqual(drifts, [])
        self.assertIn(
            "<!--\n"
            "features:\n"
            "- docker: true\n"
            "- elasticsearch:\n"
            "    version: 7.9.0\n"
            "-->",
            out,
        )

    def test_split_blocks_keeps_long_fenced_code_blocks_intact(self):
        """`split`이 긴 fenced code 블록을 온전히 유지하는지 검증."""

        lines = [
            "````markdown",
            "```php",
            "echo 'ok';",
            "```",
            "````",
            "Paragraph.",
        ]

        blocks = annotate.split_blocks(lines)

        self.assertEqual(blocks[0].kind, "code")
        self.assertEqual(blocks[0].lines, lines[:5])
        self.assertEqual(blocks[1].kind, "text")

    def test_strip_annotations_preserves_indented_code_comments(self):
        """`strip_annotations`가 들여쓴 코드 주석을 보존하는지 검증."""

        ko = (
            "    <!-- Equivalent to csrf_token() -->\n"
            "    {{ csrf_field() }}\n"
        )

        out = annotate.strip_annotations(ko)

        self.assertEqual(out, ko)

    def test_reannotation_preserves_source_authored_html_comments(self):
        """재annotation 시 원문 작성 HTML 주석을 보존하는지 검증."""

        source = (
            "<!-- source-authored note -->\n"
            "# Example\n"
            "\n"
            "Body text.\n"
        )
        translated = (
            "<!-- source-authored note -->\n"
            "<!-- # Example -->\n"
            "# Example\n"
            "\n"
            "<!-- Body text. -->\n"
            "본문입니다.\n"
        )

        out, drifts = annotate.annotate(source, translated, "13.x")

        self.assertEqual(drifts, [])
        self.assertEqual(
            verify.verify(out, source=source, version="13.x"),
            [],
        )
        self.assertEqual(out.count("<!-- source-authored note -->"), 1)

    def test_reannotation_splits_pure_code_list_items_from_prose_items(self):
        """재annotation 시 순수 inline-code 목록과 산문 항목의 소유 경계를 분리하는지 검증."""

        source = (
            "- `::1`\n"
            "- `localhost`\n"
            "- `APP_URL` in the project's `.env`\n"
        )
        translated = (
            "- `::1`\n"
            "- `localhost`\n"
            "- 프로젝트의 `.env`에 지정된 `APP_URL`\n"
        )

        out, drifts = annotate.annotate(source, translated, "13.x")

        self.assertEqual(drifts, [])
        self.assertIn(
            "<!-- - `APP_URL` in the project's `.env` -->",
            out,
        )
        self.assertEqual(verify.verify(out, source=source, version="13.x"), [])

    def test_reannotation_removes_stale_blockquote_annotation(self):
        """재annotation 시 오래된 blockquote annotation을 제거하는지 검증."""

        source = "> [!NOTE]\n> English guidance.\n"
        translated = (
            "> <!-- {note} English guidance. -->\n"
            "> [!NOTE]\n"
            "> 한국어 안내입니다.\n"
        )

        out, drifts = annotate.annotate(source, translated, "13.x")

        self.assertEqual(drifts, [])
        self.assertNotIn("{note} English guidance.", out)
        self.assertEqual(verify.verify(out, source=source, version="13.x"), [])


if __name__ == "__main__":
    unittest.main()
