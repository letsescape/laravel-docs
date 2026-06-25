import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main
from sync import config, diff, translate, verify


class MainPipelineTests(unittest.TestCase):
    def _change_with_lines(
        self, path: str, lines: list[tuple[str, str]]
    ) -> diff.SourceChange:
        old_lineno = 1
        new_lineno = 1
        diff_lines: list[diff.DiffLine] = []
        for kind, text in lines:
            if kind == "delete":
                diff_lines.append(diff.DiffLine(kind, text, old_lineno, None))
                old_lineno += 1
            elif kind == "add":
                diff_lines.append(diff.DiffLine(kind, text, None, new_lineno))
                new_lineno += 1
            else:
                diff_lines.append(diff.DiffLine(kind, text, old_lineno, new_lineno))
                old_lineno += 1
                new_lineno += 1
        return diff.SourceChange(
            path=path,
            status="M",
            hunks=(
                diff.DiffHunk(
                    old_start=1,
                    old_count=old_lineno - 1,
                    new_start=1,
                    new_count=new_lineno - 1,
                    lines=tuple(diff_lines),
                ),
            ),
        )

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
                status="A",
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

    def test_repair_segment_translation_adds_missing_original_comments(self):
        source = (
            "- [Using Eloquent](https://example.com/eloquent), models can be stored.\n"
            "- [Full-text search](https://example.com/scout/) using the `mongodb` Scout engine.\n"
        )
        translated = (
            "- [Using Eloquent](https://example.com/eloquent): 모델을 저장할 수 있습니다.\n"
            "- [Full-text search](https://example.com/scout/): `mongodb` Scout engine을 사용합니다.\n"
        )

        repaired = main._repair_segment_translation(source, translated, "13.x")

        self.assertEqual(verify.verify(repaired, source=source), [])

    def test_translate_one_updates_only_changed_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Before.\n\nNew text.\n\nAfter.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n"
                "이전 문장은 유지됩니다.\n\n"
                "<!-- Old text. -->\n"
                "예전 번역입니다.\n\n"
                "<!-- After. -->\n"
                "이후 문장도 유지됩니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    ("delete", "Old text."),
                    ("add", "New text."),
                    ("context", ""),
                    ("context", "After."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                sent.append(content)
                self.assertFalse(split)
                return "<!-- New text. -->\n새 번역입니다.\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 1)
            self.assertIn("## English Diff", sent[0])
            self.assertIn("- Old text.", sent[0])
            self.assertIn("+ New text.", sent[0])
            self.assertIn("## English Source", sent[0])
            self.assertIn("New text.", sent[0])
            self.assertNotIn("Before.", sent[0].split("## English Source", 1)[1])
            self.assertNotIn("After.", sent[0].split("## English Source", 1)[1])
            self.assertIn("## Existing Translation Context", sent[0])
            self.assertIn("예전 번역입니다.", sent[0])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- Before. -->\n"
                "이전 문장은 유지됩니다.\n\n"
                "<!-- New text. -->\n"
                "새 번역입니다.\n\n"
                "<!-- After. -->\n"
                "이후 문장도 유지됩니다.\n",
            )

    def test_translate_one_preserves_following_code_and_anchor_after_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Before.\n\nNew text.\n\n```php\n$value = true;\n```\n\n"
                '<a name="next"></a>\n#### Next\n',
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n"
                "앞 문장입니다.\n\n"
                "<!-- Old text. -->\n"
                "예전 번역입니다.\n\n"
                "```php\n$value = true;\n```\n\n"
                '<a name="next"></a>\n'
                "<!-- #### Next -->\n"
                "#### Next\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    ("delete", "Old text."),
                    ("add", "New text."),
                    ("context", ""),
                    ("context", "```php"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                _content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                self.assertFalse(split)
                return "<!-- New text. -->\n새 번역입니다.\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- Before. -->\n"
                "앞 문장입니다.\n\n"
                "<!-- New text. -->\n"
                "새 번역입니다.\n\n"
                "```php\n$value = true;\n```\n\n"
                '<a name="next"></a>\n'
                "<!-- #### Next -->\n"
                "#### Next\n",
            )

    def test_translate_one_inserts_added_blocks_after_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("Before.\n\nInserted.\n\nAfter.\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n"
                "앞 문장입니다.\n\n"
                "<!-- After. -->\n"
                "뒤 문장입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    ("add", "Inserted."),
                    ("context", ""),
                    ("context", "After."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                sent.append(content)
                self.assertFalse(split)
                return "<!-- Inserted. -->\n삽입된 문장입니다.\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 1)
            self.assertIn("+ Inserted.", sent[0])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- Before. -->\n"
                "앞 문장입니다.\n\n"
                "<!-- Inserted. -->\n"
                "삽입된 문장입니다.\n\n"
                "<!-- After. -->\n"
                "뒤 문장입니다.\n",
            )

    def test_translate_one_inserts_toc_item_with_raw_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "# Example\n\n"
                "- [Before](#before)\n"
                "- [Callouts](#callouts)\n"
                "- [After](#after)\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- # Example -->\n"
                "# Example\n\n"
                "- [Before](#before)\n"
                "- [After](#after)\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                lines=[
                    ("context", "- [Before](#before)"),
                    ("add", "- [Callouts](#callouts)"),
                    ("context", "- [After](#after)"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                sent.append(content)
                self.assertFalse(split)
                return "- [Callouts](#callouts)\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 1)
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- # Example -->\n"
                "# Example\n\n"
                "- [Before](#before)\n"
                "- [Callouts](#callouts)\n"
                "- [After](#after)\n",
            )

    def test_translate_one_inserts_structural_section_before_raw_anchor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "```php\n"
                "old();\n"
                "```\n\n"
                '<a name="callouts"></a>\n'
                "## Callouts\n\n"
                "The `callout` function displays a message.\n\n"
                "```php\n"
                "callout(label: 'Environment Configured');\n"
                "```\n\n"
                '<a name="tables"></a>\n'
                "## Tables\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "```php\n"
                "old();\n"
                "```\n\n"
                '<a name="tables"></a>\n'
                "<!-- ## Tables -->\n"
                "## Tables\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                lines=[
                    ("context", "```"),
                    ("context", ""),
                    ("add", '<a name="callouts"></a>'),
                    ("add", "## Callouts"),
                    ("add", ""),
                    ("add", "The `callout` function displays a message."),
                    ("add", ""),
                    ("add", "```php"),
                    ("add", "callout(label: 'Environment Configured');"),
                    ("add", "```"),
                    ("add", ""),
                    ("context", '<a name="tables"></a>'),
                    ("context", "## Tables"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                sent.append(content)
                self.assertFalse(split)
                self.assertIn('<a name="callouts"></a>', content)
                self.assertIn(
                    "```php\ncallout(label: 'Environment Configured');\n```",
                    content,
                )
                return (
                    '<a name="callouts"></a>\n'
                    "<!-- ## Callouts -->\n"
                    "## Callouts\n\n"
                    "<!-- The `callout` function displays a message. -->\n"
                    "`callout` 함수는 메시지를 표시합니다.\n\n"
                    "```php\n"
                    "callout(label: 'Environment Configured');\n"
                    "```\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 1)
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "```php\n"
                "old();\n"
                "```\n\n"
                '<a name="callouts"></a>\n'
                "<!-- ## Callouts -->\n"
                "## Callouts\n\n"
                "<!-- The `callout` function displays a message. -->\n"
                "`callout` 함수는 메시지를 표시합니다.\n\n"
                "```php\n"
                "callout(label: 'Environment Configured');\n"
                "```\n\n"
                '<a name="tables"></a>\n'
                "<!-- ## Tables -->\n"
                "## Tables\n",
            )

    def test_translate_one_repairs_segment_anchors_and_comments(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                '<a name="callouts"></a>\n'
                "## Callouts\n\n"
                "The `callout` function displays a message.\n\n"
                "```php\n"
                "callout(label: 'Environment Configured');\n"
                "```\n\n"
                '<a name="callout-rich-content"></a>\n'
                "#### Rich Content\n\n"
                "You may pass an array of strings and elements.\n\n"
                '<a name="tables"></a>\n'
                "## Tables\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                '<a name="tables"></a>\n'
                "<!-- ## Tables -->\n"
                "## Tables\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                lines=[
                    ("add", '<a name="callouts"></a>'),
                    ("add", "## Callouts"),
                    ("add", ""),
                    ("add", "The `callout` function displays a message."),
                    ("add", ""),
                    ("add", "```php"),
                    ("add", "callout(label: 'Environment Configured');"),
                    ("add", "```"),
                    ("add", ""),
                    ("add", '<a name="callout-rich-content"></a>'),
                    ("add", "#### Rich Content"),
                    ("add", ""),
                    ("add", "You may pass an array of strings and elements."),
                    ("add", ""),
                    ("context", '<a name="tables"></a>'),
                    ("context", "## Tables"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                _content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                self.assertFalse(split)
                return (
                    "## 콜아웃\n\n"
                    "`callout` 함수는 메시지를 표시합니다.\n\n"
                    "```php\n"
                    "callout(label: 'Environment Configured');\n"
                    "```\n\n"
                    "#### 리치 콘텐츠\n\n"
                    "문자열과 요소의 배열을 전달할 수 있습니다.\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                '<a name="callouts"></a>\n'
                "<!-- ## Callouts -->\n"
                "## Callouts\n\n"
                "<!-- The `callout` function displays a message. -->\n"
                "`callout` 함수는 메시지를 표시합니다.\n\n"
                "```php\n"
                "callout(label: 'Environment Configured');\n"
                "```\n\n"
                '<a name="callout-rich-content"></a>\n'
                "<!-- #### Rich Content -->\n"
                "#### Rich Content\n\n"
                "<!-- You may pass an array of strings and elements. -->\n"
                "문자열과 요소의 배열을 전달할 수 있습니다.\n\n"
                '<a name="tables"></a>\n'
                "<!-- ## Tables -->\n"
                "## Tables\n",
            )

    def test_translate_one_splits_multi_block_insertions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("A.\n\nB.\n\nD.\n\nE.\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- A. -->\n"
                "A 번역.\n\n"
                "<!-- E. -->\n"
                "E 번역.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "A."),
                    ("context", ""),
                    ("add", "B."),
                    ("add", ""),
                    ("add", "D."),
                    ("context", ""),
                    ("context", "E."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                sent.append(content)
                self.assertFalse(split)
                if "B." in content:
                    return "<!-- B. -->\nB 번역.\n"
                return "<!-- D. -->\nD 번역.\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 2)
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- A. -->\n"
                "A 번역.\n\n"
                "<!-- B. -->\n"
                "B 번역.\n\n"
                "<!-- D. -->\n"
                "D 번역.\n\n"
                "<!-- E. -->\n"
                "E 번역.\n",
            )

    def test_translate_one_deletes_removed_blocks_without_provider_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("Before.\n\nAfter.\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n"
                "앞 문장입니다.\n\n"
                "<!-- Removed. -->\n"
                "삭제될 문장입니다.\n\n"
                "<!-- After. -->\n"
                "뒤 문장입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    ("delete", "Removed."),
                    ("context", ""),
                    ("context", "After."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=AssertionError("provider should not run"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- Before. -->\n"
                "앞 문장입니다.\n\n"
                "<!-- After. -->\n"
                "뒤 문장입니다.\n",
            )

    def test_translate_one_coalesces_multiple_edits_in_same_source_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "First.\nNew A.\nMiddle.\nNew B.\nLast.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- First. Old A. Middle. Old B. Last. -->\n"
                "기존 번역입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "First."),
                    ("delete", "Old A."),
                    ("add", "New A."),
                    ("context", "Middle."),
                    ("delete", "Old B."),
                    ("add", "New B."),
                    ("context", "Last."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                sent.append(content)
                self.assertFalse(split)
                return (
                    "<!-- First. New A. Middle. New B. Last. -->\n"
                    "새 번역입니다.\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 1)
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- First. New A. Middle. New B. Last. -->\n"
                "새 번역입니다.\n",
            )

    def test_translate_one_normalizes_old_anchor_text_before_matching(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("See {{version}} updated.\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text("<!-- See 12.x. -->\n기존 번역입니다.\n", encoding="utf-8")
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("delete", "See {{version}}."),
                    ("add", "See {{version}} updated."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                _content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                self.assertFalse(split)
                return "<!-- See {{version}} updated. -->\n새 번역입니다.\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- See 12.x updated. -->\n새 번역입니다.\n",
            )

    def test_translate_one_reports_partial_patch_failure_without_full_retranslation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("New text.\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text("Unrelated translation.\n", encoding="utf-8")
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("delete", "Old text."),
                    ("add", "New text."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=AssertionError("full document fallback should not run"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(
                issues,
                ["partial patch failed: missing existing translation block for: Old text."],
            )
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "Unrelated translation.\n",
            )

    def test_translate_one_expands_line_change_to_containing_paragraph(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "First line.\nNew line.\nThird line.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- First line. Old line. Third line. -->\n"
                "첫 줄입니다. 예전 줄입니다. 세 번째 줄입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "First line."),
                    ("delete", "Old line."),
                    ("add", "New line."),
                    ("context", "Third line."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                sent.append(content)
                self.assertFalse(split)
                return (
                    "<!-- First line. New line. Third line. -->\n"
                    "첫 줄입니다. 새 줄입니다. 세 번째 줄입니다.\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertIn("First line.\nNew line.\nThird line.", sent[0])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- First line. New line. Third line. -->\n"
                "첫 줄입니다. 새 줄입니다. 세 번째 줄입니다.\n",
            )

    def test_translate_one_replaces_paragraph_when_line_is_inserted_inside_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "First line.\nInserted line.\nSecond line.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- First line. Second line. -->\n"
                "첫 줄입니다. 두 번째 줄입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "First line."),
                    ("add", "Inserted line."),
                    ("context", "Second line."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                _content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                self.assertFalse(split)
                return (
                    "<!-- First line. Inserted line. Second line. -->\n"
                    "첫 줄입니다. 삽입된 줄입니다. 두 번째 줄입니다.\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- First line. Inserted line. Second line. -->\n"
                "첫 줄입니다. 삽입된 줄입니다. 두 번째 줄입니다.\n",
            )

    def test_translate_one_replaces_paragraph_when_line_is_deleted_inside_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "First line.\nSecond line.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- First line. Removed line. Second line. -->\n"
                "첫 줄입니다. 삭제될 줄입니다. 두 번째 줄입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "First line."),
                    ("delete", "Removed line."),
                    ("context", "Second line."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                _content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                self.assertFalse(split)
                return "<!-- First line. Second line. -->\n첫 줄입니다. 두 번째 줄입니다.\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- First line. Second line. -->\n첫 줄입니다. 두 번째 줄입니다.\n",
            )

    def test_translate_one_replaces_split_paragraph_and_following_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-master/errors.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Debug configuration.\n\n"
                "During local development, you should set `APP_DEBUG` to `true`.\n\n"
                "> [!WARNING]\n"
                "> In production, `APP_DEBUG` should always be `false`.\n\n"
                '<a name="next"></a>\n'
                "## Next\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-master/errors.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Debug configuration. -->\n"
                "디버그 설정입니다.\n\n"
                "<!-- During local development, you should set `APP_DEBUG` to `true`. -->\n"
                "로컬 개발 중에는 `APP_DEBUG`를 `true`로 설정해야 합니다.\n\n"
                "> [!WARNING]\n"
                "> 프로덕션에서는 `APP_DEBUG`가 항상 `false`여야 합니다.\n\n"
                '<a name="next"></a>\n'
                "<!-- ## Next -->\n"
                "## Next\n",
                encoding="utf-8",
            )
            old = (
                "During local development, you should set `APP_DEBUG` to `true`. "
                "**In production, `APP_DEBUG` should always be `false`.**"
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-master/errors.md",
                lines=[
                    ("context", "Debug configuration."),
                    ("context", ""),
                    ("delete", old),
                    ("add", "During local development, you should set `APP_DEBUG` to `true`."),
                    ("add", ""),
                    ("add", "> [!WARNING]"),
                    ("add", "> In production, `APP_DEBUG` should always be `false`."),
                    ("context", ""),
                    ("context", '<a name="next"></a>'),
                    ("context", "## Next"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                _content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                self.assertFalse(split)
                return (
                    "<!-- During local development, you should set `APP_DEBUG` to `true`. -->\n"
                    "로컬 개발 중에는 `APP_DEBUG`를 `true`로 설정해야 합니다.\n\n"
                    "> [!WARNING]\n"
                    "> <!-- In production, `APP_DEBUG` should always be `false`. -->\n"
                    "> 프로덕션에서는 `APP_DEBUG`가 항상 `false`여야 합니다.\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- Debug configuration. -->\n"
                "디버그 설정입니다.\n\n"
                "<!-- During local development, you should set `APP_DEBUG` to `true`. -->\n"
                "로컬 개발 중에는 `APP_DEBUG`를 `true`로 설정해야 합니다.\n\n"
                "> [!WARNING]\n"
                "> <!-- In production, `APP_DEBUG` should always be `false`. -->\n"
                "> 프로덕션에서는 `APP_DEBUG`가 항상 `false`여야 합니다.\n\n"
                '<a name="next"></a>\n'
                "<!-- ## Next -->\n"
                "## Next\n",
            )

    def test_translate_one_requires_hunks_for_existing_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("# One\n\n# Two\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text("# 기존 문서\n", encoding="utf-8")
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="M",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "split_chunks",
                side_effect=AssertionError("full document fallback should not run"),
            ), patch.object(
                main.translate,
                "translate_text",
                side_effect=AssertionError("full document fallback should not run"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, ["missing diff hunks for partial sync"])
            self.assertEqual(dest.read_text(encoding="utf-8"), "# 기존 문서\n")

    def test_translate_one_translates_new_documents_as_full_changed_content(self):
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
                status="A",
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
            self.assertTrue(dest.exists())

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

    def test_main_require_filters_stops_before_upstream_when_filter_is_missing(self):
        with patch.object(
            main.sys,
            "argv",
            ["main.py", "--require-filters", "--version", "13.x"],
        ), patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 2)

    def test_main_fail_fast_stops_after_first_verification_failure(self):
        change = diff.SourceChange(
            path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
            status="M",
        )
        calls: list[str] = []

        def translate_one(change, cfg, prompt, dest):
            calls.append(str(dest))
            return ["heading mismatch"]

        with patch.object(
            main.sys, "argv", ["main.py", "--fail-fast"]
        ), patch.object(main.upstream, "main"), patch.object(
            main.diff, "changed_sources", return_value=[change]
        ), patch.object(
            main.config,
            "load_config",
            return_value=config.Config(
                provider="cli", values={"TRANSLATION_PROVIDER": "cli"}
            ),
        ), patch.object(
            main, "_load_prompts", return_value={"ko": "ko prompt", "ja": "ja prompt"}
        ), patch.object(
            main, "_translate_one", side_effect=translate_one
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(len(calls), 1)

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
