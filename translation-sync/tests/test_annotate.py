import io
import tempfile
import unittest
from contextlib import redirect_stderr
from unittest.mock import patch

import annotate_cli
from sync import annotate, verify


class AnnotateCliTests(unittest.TestCase):
    def test_rejects_invalid_version_before_reading_documents(self):
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
    def test_emits_source_comment_when_content_present_but_block_misaligned(self):
        # The translation kept the content (links intact) but lost the list
        # structure, so block alignment slips. The English comment must still be
        # emitted so verification's "missing original comment" cannot fail.
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
            verify._required_comments(en).issubset(verify._translated_comments(out))  # noqa: SLF001
        )

    def test_keeps_drift_when_content_is_genuinely_untranslated(self):
        # A new paragraph with no verbatim marker is genuinely missing from the
        # translation: do NOT paper it over, so drift is still reported and the
        # incomplete document is not silently accepted.
        en = "Body text.\n\nNew untranslated paragraph.\n"
        ko = "<!-- Body text. -->\n본문입니다.\n"
        out, drifts = annotate.annotate(en, ko, "13.x")
        self.assertFalse(
            verify._required_comments(en).issubset(verify._translated_comments(out))  # noqa: SLF001
        )
        self.assertTrue(any(d.op == "delete" for d in drifts))

    def test_inserts_original_english_comments_without_rewriting_translation(self):
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
        en = "# Installation\n\nInstall Laravel with Composer.\n\nRun the server.\n"
        ko = "# 설치 (Installation)\n\nComposer로 Laravel을 설치합니다.\n"

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertIn("<!-- # Installation -->", out)
        self.assertEqual(len(drifts), 1)
        self.assertEqual(drifts[0].op, "delete")
        self.assertEqual(drifts[0].en_lines, ["Run the server."])

    def test_replaces_version_placeholder_in_inserted_comments(self):
        en = "See [Routing](/docs/{{version}}/routing)."
        ko = "[라우팅](/docs/12.x/routing)을 참고하세요."

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertIn("<!-- See [Routing](/docs/12.x/routing). -->", out)

    def test_does_not_insert_comments_for_toc_link_lists(self):
        en = "# Concurrency\n\n- [Introduction](#introduction)\n\n<a name=\"introduction\"></a>\n## Introduction\n"
        ko = "# 동시 실행 (Concurrency)\n\n- [소개](#introduction)\n\n<a name=\"introduction\"></a>\n## 소개 (Introduction)\n"

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertNotIn("<!-- - [Introduction](#introduction) -->", out)
        self.assertIn("- [소개](#introduction)", out)
        self.assertIn("<!-- ## Introduction -->", out)

    def test_does_not_insert_comments_for_standalone_html_tags(self):
        en = '<div class="grid">\n\nBody.\n\n</div>\n'
        ko = '<div class="grid">\n\n본문입니다.\n\n</div>\n'

        out, drifts = annotate.annotate(en, ko, "13.x")

        self.assertEqual(drifts, [])
        self.assertNotIn('<!-- <div class="grid"> -->', out)
        self.assertNotIn("<!-- </div> -->", out)
        self.assertIn("<!-- Body. -->", out)

    def test_preserves_trailing_blank_line_count(self):
        en = "# Example\n\nBody.\n\n"
        ko = "# 예제\n\n본문.\n\n"

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertTrue(out.endswith("\n\n"))

    def test_replaces_existing_original_comments_when_reannotating(self):
        en = "# Updated\n\nUpdated body.\n"
        ko = "<!-- # Old -->\n# 예제\n\n<!-- Old body. -->\n본문.\n"

        out, drifts = annotate.annotate(en, ko, "12.x")

        self.assertEqual(drifts, [])
        self.assertNotIn("<!-- # Old -->", out)
        self.assertNotIn("<!-- Old body. -->", out)
        self.assertIn("<!-- # Updated -->", out)
        self.assertIn("<!-- Updated body. -->", out)

    def test_aligns_paragraph_after_list_without_blank_line(self):
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
        ko = (
            "    <!-- Equivalent to csrf_token() -->\n"
            "    {{ csrf_field() }}\n"
        )

        out = annotate.strip_annotations(ko)

        self.assertEqual(out, ko)

    def test_reannotation_preserves_source_authored_html_comments(self):
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
