import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main
from sync import config, diff, translate


class MainPipelineTests(unittest.TestCase):
    def test_translate_one_reports_incomplete_translation_without_writing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("# Example\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="M",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translate.IncompleteTranslation("timeout"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertTrue(
                any(issue.startswith("incomplete translation") for issue in issues)
            )
            self.assertFalse(dest.exists())

    def test_translate_one_passes_existing_translation_as_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("# Example\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text("# 기존 예제\n", encoding="utf-8")
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="M",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                sent.append(content)
                self.assertFalse(split)
                return "<!-- # Example -->\n# Example\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 1)
            self.assertIn("## English Source", sent[0])
            self.assertIn("# Example", sent[0])
            self.assertIn("## Existing Translation", sent[0])
            self.assertIn("# 기존 예제", sent[0])

    def test_translate_one_chunks_source_before_building_translation_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("# One\n\n# Two\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="M",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                sent.append(content)
                self.assertFalse(split)
                if "# One" in content:
                    return "<!-- # One -->\n# One\n\n"
                return "<!-- # Two -->\n# Two\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "split_chunks",
                return_value=["# One\n\n", "# Two\n"],
            ), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 2)
            self.assertIn("# One", sent[0])
            self.assertNotIn("# Two", sent[0])
            self.assertIn("# Two", sent[1])

    def test_delete_outputs_removes_ko_and_ja_documents_for_deleted_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ko_doc = root / "versioned_docs/version-12.x/example.md"
            ja_doc = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            ko_doc.parent.mkdir(parents=True)
            ja_doc.parent.mkdir(parents=True)
            ko_doc.write_text("ko", encoding="utf-8")
            ja_doc.write_text("ja", encoding="utf-8")
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="D",
            )

            with patch.object(main, "REPO_ROOT", root):
                main._delete_outputs(change)

            self.assertFalse(ko_doc.exists())
            self.assertFalse(ja_doc.exists())

    def test_loads_ko_and_ja_prompts_from_separate_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sync_root = root / "translation-sync"
            sync_root.mkdir()
            (sync_root / "prompt.md").write_text("KO\n", encoding="utf-8")
            (sync_root / "prompt_jp.md").write_text("JA\n", encoding="utf-8")

            with patch.object(main, "PROMPT_PATH", sync_root / "prompt.md"), patch.object(
                main,
                "JA_PROMPT_PATH",
                sync_root / "prompt_jp.md",
                create=True,
            ):
                prompts = main._load_prompts()

        self.assertEqual(prompts["ko"], "KO")
        self.assertEqual(prompts["ja"], "JA")

    def test_select_changes_migrate_existing_uses_all_source_markdown_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text("# Example\n", encoding="utf-8")

            with patch.object(main, "REPO_ROOT", root):
                changes = main._select_changes(migrate_existing=True)

        self.assertEqual(
            changes,
            [
                diff.SourceChange(
                    path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                    status="M",
                )
            ],
        )

    def test_select_changes_migrate_existing_can_filter_by_version_and_doc(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for path in (
                "i18n/en/docusaurus-plugin-content-docs/version-12.x/a.md",
                "i18n/en/docusaurus-plugin-content-docs/version-12.x/b.md",
                "i18n/en/docusaurus-plugin-content-docs/version-13.x/b.md",
            ):
                source = root / path
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text("# Example\n", encoding="utf-8")

            with patch.object(main, "REPO_ROOT", root):
                changes = main._select_changes(
                    migrate_existing=True,
                    version="12.x",
                    doc="b.md",
                )

        self.assertEqual(
            changes,
            [
                diff.SourceChange(
                    path="i18n/en/docusaurus-plugin-content-docs/version-12.x/b.md",
                    status="M",
                )
            ],
        )

    def test_sidebar_versions_include_changed_versions_and_master_once(self):
        changes = [
            diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/a.md",
                status="M",
            ),
            diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-master/b.md",
                status="M",
            ),
        ]

        self.assertEqual(main._sidebar_versions(changes, None), ["12.x", "master"])

    def test_main_syncs_master_sidebar_when_no_sources_changed(self):
        calls: list[tuple[list[str], bool]] = []

        def sync_versions(versions, *, write=False, repo_root=None):
            calls.append((versions, write))
            return [main.sidebar.SidebarResult("master", False, [])]

        with patch.object(main.sys, "argv", ["main.py"]), patch.object(
            main.upstream, "main"
        ), patch.object(main.diff, "changed_sources", return_value=[]), patch.object(
            main.sidebar, "sync_versions", side_effect=sync_versions
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(calls, [(["master"], True)])

    def test_check_existing_annotations_reports_unannotated_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-12.x/example.md"
            ja_doc = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            ja_doc.parent.mkdir(parents=True)
            source.write_text("# Example\n\nBody text.\n", encoding="utf-8")
            ko_doc.write_text("# 예제\n\n본문입니다.\n", encoding="utf-8")
            ja_doc.write_text("# 例\n\n本文です。\n", encoding="utf-8")

            with patch.object(main, "REPO_ROOT", root):
                issues = main._check_existing_annotations()

        self.assertEqual(
            issues,
            [
                "ko i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md: heading text mismatch",
                "ko i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md: missing original comment",
                "ja i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md: heading text mismatch",
                "ja i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md: missing original comment",
            ],
        )

    def test_check_existing_annotations_accepts_comment_annotated_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-12.x/example.md"
            ja_doc = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            ja_doc.parent.mkdir(parents=True)
            source.write_text("# Example\n\nBody text.\n", encoding="utf-8")
            annotated = "<!-- # Example -->\n# Example\n\n<!-- Body text. -->\n본문입니다.\n"
            ko_doc.write_text(annotated, encoding="utf-8")
            ja_doc.write_text(annotated, encoding="utf-8")

            with patch.object(main, "REPO_ROOT", root):
                issues = main._check_existing_annotations()

        self.assertEqual(issues, [])

    def test_check_existing_annotations_skips_missing_existing_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-12.x/example.md"
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            source.write_text("# Example\n\nBody text.\n", encoding="utf-8")
            ko_doc.write_text(
                "<!-- # Example -->\n# Example\n\n<!-- Body text. -->\n본문입니다.\n",
                encoding="utf-8",
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._check_existing_annotations()

        self.assertEqual(issues, [])

    def test_annotate_existing_writes_clean_ko_and_ja_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-12.x/example.md"
            ja_doc = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            ja_doc.parent.mkdir(parents=True)
            source.write_text("# Example\n\nBody text.\n", encoding="utf-8")
            ko_doc.write_text("# 예제\n\n본문입니다.\n", encoding="utf-8")
            ja_doc.write_text("# 例\n\n本文です。\n", encoding="utf-8")

            with patch.object(main, "REPO_ROOT", root):
                written, failures = main._annotate_existing(apply=True)

            self.assertEqual(written, 2)
            self.assertEqual(failures, [])
            self.assertIn("<!-- # Example -->", ko_doc.read_text(encoding="utf-8"))
            self.assertIn("<!-- Body text. -->", ja_doc.read_text(encoding="utf-8"))

    def test_annotate_existing_skips_documents_that_already_verify(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-12.x/example.md"
            ja_doc = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            ja_doc.parent.mkdir(parents=True)
            source.write_text("# Example\n\nBody text.\n", encoding="utf-8")
            annotated = "<!-- # Example -->\n# Example\n\n<!-- Body text. -->\n본문입니다.\n"
            ko_doc.write_text(annotated, encoding="utf-8")
            ja_doc.write_text(annotated, encoding="utf-8")

            with patch.object(main, "REPO_ROOT", root):
                written, failures = main._annotate_existing(apply=True)

            self.assertEqual(written, 0)
            self.assertEqual(failures, [])
            self.assertEqual(ko_doc.read_text(encoding="utf-8"), annotated)
            self.assertEqual(ja_doc.read_text(encoding="utf-8"), annotated)

    def test_annotate_existing_dry_run_counts_writable_documents_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-12.x/example.md"
            ja_doc = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            ja_doc.parent.mkdir(parents=True)
            source.write_text("# Example\n\nBody text.\n", encoding="utf-8")
            ko_original = "# 예제\n\n본문입니다.\n"
            ja_original = "# 例\n\n本文です。\n"
            ko_doc.write_text(ko_original, encoding="utf-8")
            ja_doc.write_text(ja_original, encoding="utf-8")

            with patch.object(main, "REPO_ROOT", root):
                writable, failures = main._annotate_existing(apply=False)

            self.assertEqual(writable, 2)
            self.assertEqual(failures, [])
            self.assertEqual(ko_doc.read_text(encoding="utf-8"), ko_original)
            self.assertEqual(ja_doc.read_text(encoding="utf-8"), ja_original)

    def test_annotate_existing_writes_comments_with_residual_non_annotation_issues(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-12.x/example.md"
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            source.write_text("Use `Cache::get`.\n", encoding="utf-8")
            ko_original = "`Cache::put`을 사용합니다.\n"
            ko_doc.write_text(ko_original, encoding="utf-8")

            with patch.object(main, "REPO_ROOT", root):
                writable, failures = main._annotate_existing(apply=True)

            self.assertEqual(writable, 1)
            self.assertEqual(failures, [])
            self.assertEqual(
                ko_doc.read_text(encoding="utf-8"),
                "<!-- Use `Cache::get`. -->\n" + ko_original,
            )

    def test_annotate_existing_skips_missing_existing_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-12.x/example.md"
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            source.write_text("# Example\n\nBody text.\n", encoding="utf-8")
            ko_original = "# 예제\n\n본문입니다.\n"
            ko_doc.write_text(ko_original, encoding="utf-8")

            with patch.object(main, "REPO_ROOT", root):
                writable, failures = main._annotate_existing(apply=False)

            self.assertEqual(writable, 1)
            self.assertEqual(failures, [])
            self.assertEqual(ko_doc.read_text(encoding="utf-8"), ko_original)

    def test_annotate_existing_reports_drift_without_writing_document(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-12.x/example.md"
            ja_doc = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            ja_doc.parent.mkdir(parents=True)
            source.write_text(
                "# Example\n\nBody text.\n\nNew text.\n", encoding="utf-8"
            )
            original = "# 예제\n\n본문입니다.\n"
            ko_doc.write_text(original, encoding="utf-8")
            ja_doc.write_text("# 例\n\n本文です。\n", encoding="utf-8")

            with patch.object(main, "REPO_ROOT", root):
                written, failures = main._annotate_existing(apply=True)

            self.assertEqual(written, 0)
            self.assertTrue(any("drift" in failure for failure in failures))
            self.assertEqual(ko_doc.read_text(encoding="utf-8"), original)

    def test_annotate_existing_writes_when_drifted_output_still_verifies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-12.x/example.md"
            ja_doc = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            ja_doc.parent.mkdir(parents=True)
            source.write_text("# Example\n\nBody text.\n", encoding="utf-8")
            ko_doc.write_text(
                "# 예제\n\n본문입니다.\n\n로컬 보충 문장입니다.\n",
                encoding="utf-8",
            )

            with patch.object(main, "REPO_ROOT", root):
                written, failures = main._annotate_existing(apply=True)

            self.assertEqual(written, 1)
            self.assertEqual(failures, [])
            self.assertIn("<!-- # Example -->", ko_doc.read_text(encoding="utf-8"))
            self.assertIn("로컬 보충 문장입니다.", ko_doc.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
