import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
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

    def test_added_document_preserves_provider_chunk_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                ("Source line.\n" * 399) + "\nFinal line.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="A",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            responses = iter(("first translated chunk", "second translated chunk"))

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                side_effect=lambda *_args, **_kwargs: next(responses),
            ), patch.object(
                main.response_contract,
                "verify",
                return_value=[],
            ), patch.object(main.verify, "verify", return_value=[]):
                issues = main._translate_added_document(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "first translated chunk\n\nsecond translated chunk\n",
            )

    def test_added_document_rejects_invalid_provider_contract_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Acquire the cache lock before updating the value.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="A",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            echoed = (
                "<!-- Acquire the cache lock before updating the value. -->\n"
                "Acquire the cache lock before updating the value.\n"
            )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                return_value=echoed,
            ) as provider, patch.object(
                main.verify,
                "verify",
                return_value=[],
            ):
                issues = main._translate_added_document(change, cfg, "prompt", dest)

            self.assertIn("provider untranslated source text", issues[0])
            self.assertEqual(
                provider.call_count,
                main.MAX_SEGMENT_VERIFICATION_ATTEMPTS,
            )
            self.assertFalse(dest.exists())

    def test_added_document_rejects_wrong_target_language_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("Acquire the cache lock.\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="A",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            japanese = (
                "<!-- Acquire the cache lock. -->\n"
                "キャッシュロックを取得します。\n"
            )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                return_value=japanese,
            ) as provider:
                issues = main._translate_added_document(
                    change,
                    cfg,
                    "prompt",
                    dest,
                    locale="ko",
                )

            self.assertIn("provider target language mismatch", issues[0])
            self.assertEqual(
                provider.call_count,
                main.MAX_SEGMENT_VERIFICATION_ATTEMPTS,
            )
            self.assertFalse(dest.exists())

    def test_added_license_document_allows_preserved_legal_english(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/license.md"
            )
            source_path.parent.mkdir(parents=True)
            source = "Permission is hereby granted to use this software.\n"
            source_path.write_text(source, encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/license.md"
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/license.md",
                status="A",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            translated = (
                "<!-- Permission is hereby granted to use this software. -->\n"
                "Permission is hereby granted to use this software.\n"
            )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                return_value=translated,
            ) as provider:
                issues = main._translate_added_document(
                    change,
                    cfg,
                    "prompt",
                    dest,
                    locale="ko",
                )

            self.assertEqual(issues, [])
            self.assertEqual(provider.call_count, 1)
            self.assertEqual(dest.read_text(encoding="utf-8"), translated)

    def test_added_license_document_rejects_untranslated_nonlegal_intro(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/license.md"
            )
            source_path.parent.mkdir(parents=True)
            source = "Read this introduction before reviewing the legal terms.\n"
            source_path.write_text(source, encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/license.md"
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/license.md",
                status="A",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            untranslated = (
                "<!-- Read this introduction before reviewing the legal terms. -->\n"
                "Read this introduction before reviewing the legal terms.\n"
            )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                return_value=untranslated,
            ) as provider:
                issues = main._translate_added_document(
                    change,
                    cfg,
                    "prompt",
                    dest,
                    locale="ko",
                )

            self.assertIn("provider untranslated source text", issues[0])
            self.assertEqual(
                provider.call_count,
                main.MAX_SEGMENT_VERIFICATION_ATTEMPTS,
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

    def test_translate_one_updates_only_the_changed_duplicate_bare_link_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/collections.md"
            )
            source_path.parent.mkdir(parents=True)
            unchanged_list = (
                "[reduce](#method-reduce)\n"
                "[reduceSpread](#method-reduce-spread)\n"
                "[reject](#method-reject)\n"
            )
            changed_list = (
                "[reduce](#method-reduce)\n"
                "[reduceInto](#method-reduce-into)\n"
                "[reduceSpread](#method-reduce-spread)\n"
                "[reject](#method-reject)\n"
            )
            source_path.write_text(
                f"{unchanged_list}\n{changed_list}",
                encoding="utf-8",
            )

            dest = root / "versioned_docs/version-13.x/collections.md"
            dest.parent.mkdir(parents=True)

            def annotated(link_list: str) -> str:
                return f"<!--\n{link_list}-->\n{link_list}"

            original = f"{annotated(unchanged_list)}\n{annotated(unchanged_list)}"
            expected = f"{annotated(unchanged_list)}\n{annotated(changed_list)}"
            dest.write_text(original, encoding="utf-8")

            change = self._change_with_lines(
                path=(
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-13.x/collections.md"
                ),
                lines=[
                    ("context", "[reduce](#method-reduce)"),
                    ("context", "[reduceSpread](#method-reduce-spread)"),
                    ("context", "[reject](#method-reject)"),
                    ("context", ""),
                    ("context", "[reduce](#method-reduce)"),
                    ("add", "[reduceInto](#method-reduce-into)"),
                    ("context", "[reduceSpread](#method-reduce-spread)"),
                    ("context", "[reject](#method-reject)"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=AssertionError("provider should not run for bare links"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

                self.assertEqual(issues, [])
                self.assertEqual(dest.read_text(encoding="utf-8"), expected)

                rerun_issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(rerun_issues, [])
            self.assertEqual(dest.read_text(encoding="utf-8"), expected)

    def test_translate_one_moves_named_sections_without_provider_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            beta = '<a name="beta"></a>\n## Beta\n\nBeta body.\n'
            alpha = '<a name="alpha"></a>\n## Alpha\n\nAlpha body.\n'
            source_path.write_text(f"{beta}\n{alpha}", encoding="utf-8")

            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            existing_alpha = (
                '<a name="alpha"></a>\n'
                "<!-- ## Alpha -->\n## Alpha\n\n"
                "<!-- Alpha body. -->\n알파 본문.\n"
            )
            existing_beta = (
                '<a name="beta"></a>\n'
                "<!-- ## Beta -->\n## Beta\n\n"
                "<!-- Beta body. -->\n베타 본문.\n"
            )
            dest.write_text(
                f"{existing_alpha}\n{existing_beta}",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path=(
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-13.x/example.md"
                ),
                lines=[
                    ("add", '<a name="beta"></a>'),
                    ("add", "## Beta"),
                    ("add", ""),
                    ("add", "Beta body."),
                    ("add", ""),
                    ("context", '<a name="alpha"></a>'),
                    ("context", "## Alpha"),
                    ("context", ""),
                    ("context", "Alpha body."),
                    ("delete", ""),
                    ("delete", '<a name="beta"></a>'),
                    ("delete", "## Beta"),
                    ("delete", ""),
                    ("delete", "Beta body."),
                ],
            )
            cfg = config.Config(
                provider="cli",
                values={"TRANSLATION_PROVIDER": "cli"},
            )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=AssertionError("provider should not run for a move"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)
                rerun_issues = main._translate_one(change, cfg, "prompt", dest)

            expected = f"{existing_beta}\n{existing_alpha}"
            self.assertEqual(issues, [])
            self.assertEqual(rerun_issues, [])
            self.assertEqual(dest.read_text(encoding="utf-8"), expected)

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

    def test_translate_one_handles_multi_block_insertions_as_one_range(self):
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
                self.assertIn("B.", content)
                self.assertIn("D.", content)
                return (
                    "<!-- B. -->\nB 번역.\n\n"
                    "<!-- D. -->\nD 번역.\n"
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
                return "<!-- See 12.x updated. -->\n새 번역입니다.\n"

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

    def test_translate_one_restores_placeholders_in_plan_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            image = "![Diagram](data:image/png;base64,QUJD)"
            source_path.write_text(
                f"{image}\n\nNew text.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                f"<!-- {image} -->\n{image}\n\n"
                "<!-- Old text. -->\n예전 번역입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", image),
                    ("context", ""),
                    ("delete", "Old text."),
                    ("add", "New text."),
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
                f"<!-- {image} -->\n{image}\n\n"
                "<!-- New text. -->\n새 번역입니다.\n",
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
                [
                    "partial patch failed: existing block order matches neither "
                    "source nor target plan state"
                ],
            )
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "Unrelated translation.\n",
            )

    def test_translate_one_rejects_mixed_plan_state_before_provider(self):
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
            existing = (
                "<!-- Before. -->\n앞 문장입니다.\n\n"
                "<!-- Extra. -->\n추가 문장입니다.\n\n"
                "<!-- Old text. -->\n예전 번역입니다.\n\n"
                "<!-- After. -->\n뒤 문장입니다.\n"
            )
            dest.write_text(existing, encoding="utf-8")
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

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=AssertionError("provider should not run for mixed state"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(
                issues,
                [
                    "partial patch failed: existing block order matches neither "
                    "source nor target plan state"
                ],
            )
            self.assertEqual(dest.read_text(encoding="utf-8"), existing)

    def test_translate_one_verifies_target_state_without_provider(self):
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
            existing = (
                "<!-- Before. -->\n앞 문장입니다.\n\n"
                "<!-- New text. -->\n새 번역입니다.\n\n"
                "<!-- After. -->\n뒤 문장입니다.\n"
            )
            dest.write_text(existing, encoding="utf-8")
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

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=AssertionError("provider should not run for target state"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(dest.read_text(encoding="utf-8"), existing)

    def test_translate_one_skips_an_already_current_prose_and_code_hunk(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            old_source = (
                "Before.\n\n"
                "Use the old key.\n\n"
                "```php\n"
                "$key = 'old';\n"
                "```\n\n"
                "After.\n"
            )
            new_source = (
                "Before.\n\n"
                "Use the new key.\n\n"
                "```php\n"
                "$key = 'new';\n"
                "```\n\n"
                "After.\n"
            )
            source_path.write_text(new_source, encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            existing = (
                "<!-- Before. -->\n이전입니다.\n\n"
                "<!-- Use the new key. -->\n새 키를 사용합니다.\n\n"
                "```php\n"
                "$key = 'new';\n"
                "```\n\n"
                "<!-- After. -->\n이후입니다.\n"
            )
            dest.write_text(existing, encoding="utf-8")
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="M",
                hunks=diff.hunks_between(old_source, new_source),
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.patch_utils,
                "plan_state",
                return_value=main.patch_utils.PlanState.UNGUARDED,
            ), patch.object(
                main.translate,
                "translate_request",
                side_effect=AssertionError("provider should not run for current output"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest, locale="ko")

            self.assertEqual(issues, [])
            self.assertEqual(dest.read_text(encoding="utf-8"), existing)

    def test_translate_one_repairs_unchanged_legacy_admonition_and_annotation(self):
        """Partial replay also normalizes legacy context outside the changed block."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            old_source = (
                "Before.\n\n"
                "> **Note:** Keep this.\n\n"
                "Old text.\n\n"
                "After.\n"
            )
            new_source = old_source.replace("Old text.", "New text.")
            source_path.write_text(new_source, encoding="utf-8")
            dest = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n"
                "前の文です。\n\n"
                "<!-- > **Note:** Keep this. -->\n"
                "> **注意:** 保持する必要があります。\n\n"
                "<!-- Old text. -->\n"
                "古い翻訳です。\n\n"
                "<!-- After. -->\n"
                "後の文です。\n",
                encoding="utf-8",
            )
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="M",
                hunks=diff.hunks_between(old_source, new_source),
            )
            cfg = config.Config(
                provider="identity",
                values={"TRANSLATION_PROVIDER": "identity"},
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._translate_one(change, cfg, "prompt", dest, locale="ja")

            self.assertEqual(issues, [])
            output = dest.read_text(encoding="utf-8")
            self.assertIn("> [!NOTE]\n> 保持する必要があります。", output)
            self.assertNotIn("> **注意:**", output)
            self.assertIn("<!-- New text. -->", output)

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

    def test_translate_one_replaces_localized_table_row_by_stable_cells(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "| Feature | Providers |\n"
                "|---|---|\n"
                "| Text | OpenAI, OpenAI Compatible, Anthropic |\n"
                "| Images | OpenAI |\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "| 기능 | 프로바이더 |\n"
                "|---|---|\n"
                "| 텍스트 | OpenAI, Anthropic |\n"
                "| 이미지 | OpenAI |\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                lines=[
                    ("context", "|---|---|"),
                    ("delete", "| Text | OpenAI, Anthropic |"),
                    ("add", "| Text | OpenAI, OpenAI Compatible, Anthropic |"),
                    ("context", "| Images | OpenAI |"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                sent.append(content)
                self.assertFalse(split)
                self.assertIn("| 텍스트 | OpenAI, Anthropic |", content)
                return "| 텍스트 | OpenAI, OpenAI Compatible, Anthropic |\n"

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
                "| 기능 | 프로바이더 |\n"
                "|---|---|\n"
                "| 텍스트 | OpenAI, OpenAI Compatible, Anthropic |\n"
                "| 이미지 | OpenAI |\n",
            )

    def test_translate_one_replaces_localized_table_row_with_japanese_commas(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "| Feature | Providers |\n"
                "|---|---|\n"
                "| Text | OpenAI, OpenAI Compatible, Anthropic |\n"
                "| Images | OpenAI |\n",
                encoding="utf-8",
            )
            dest = root / "i18n/ja/docusaurus-plugin-content-docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "| 特徴 | プロバイダ |\n"
                "|---|---|\n"
                "| 文章 | OpenAI、Anthropic |\n"
                "| 画像 | OpenAI |\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                lines=[
                    ("context", "|---|---|"),
                    ("delete", "| Text | OpenAI, Anthropic |"),
                    ("add", "| Text | OpenAI, OpenAI Compatible, Anthropic |"),
                    ("context", "| Images | OpenAI |"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                self.assertFalse(split)
                self.assertIn("| 文章 | OpenAI、Anthropic |", content)
                return "| 文章 | OpenAI、OpenAI Compatible、Anthropic |\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "| 特徴 | プロバイダ |\n"
                "|---|---|\n"
                "| 文章 | OpenAI、OpenAI Compatible、Anthropic |\n"
                "| 画像 | OpenAI |\n",
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

    def test_translate_one_keeps_changed_admonition_body_in_blockquote(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/search.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "The basic workflow for vector search.\n\n"
                "> [!NOTE]\n"
                "> Vector search requires the [Laravel AI SDK](/docs/{{version}}/ai-sdk) "
                "and PostgreSQL with `pgvector`.\n\n"
                '<a name="generating-embeddings"></a>\n'
                "### Generating Embeddings\n",
                encoding="utf-8",
            )
            dest = root / "i18n/ja/docusaurus-plugin-content-docs/version-13.x/search.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- The basic workflow for vector search. -->\n"
                "ベクトル検索の基本的なワークフローです。\n\n"
                "> [!NOTE]\n"
                "> ベクトル検索には、`pgvector` 拡張子と [Laravel AI SDK](/docs/13.x/ai-sdk) "
                "を持つ PostgreSQL データベースが必要です。\n\n"
                '<a name="generating-embeddings"></a>\n'
                "<!-- ### Generating Embeddings -->\n"
                "### Generating Embeddings\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/search.md",
                lines=[
                    ("context", "The basic workflow for vector search."),
                    ("context", ""),
                    ("context", "> [!NOTE]"),
                    (
                        "delete",
                        "> Vector search requires PostgreSQL with `pgvector` and the "
                        "[Laravel AI SDK](/docs/{{version}}/ai-sdk).",
                    ),
                    (
                        "add",
                        "> Vector search requires the [Laravel AI SDK](/docs/{{version}}/ai-sdk) "
                        "and PostgreSQL with `pgvector`.",
                    ),
                    ("context", ""),
                    ("context", '<a name="generating-embeddings"></a>'),
                    ("context", "### Generating Embeddings"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                _content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                self.assertFalse(split)
                return (
                    "> <!-- Vector search requires the [Laravel AI SDK](/docs/13.x/ai-sdk) "
                    "and PostgreSQL with `pgvector`. -->\n"
                    "> ベクトル検索には、[Laravel AI SDK](/docs/13.x/ai-sdk) と "
                    "`pgvector` を備えた PostgreSQL が必要です。\n"
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
                "<!-- The basic workflow for vector search. -->\n"
                "ベクトル検索の基本的なワークフローです。\n\n"
                "> [!NOTE]\n"
                "> <!-- Vector search requires the [Laravel AI SDK](/docs/13.x/ai-sdk) "
                "and PostgreSQL with `pgvector`. -->\n"
                "> ベクトル検索には、[Laravel AI SDK](/docs/13.x/ai-sdk) と "
                "`pgvector` を備えた PostgreSQL が必要です。\n\n"
                '<a name="generating-embeddings"></a>\n'
                "<!-- ### Generating Embeddings -->\n"
                "### Generating Embeddings\n",
            )

    def test_translate_one_retranslates_an_admonition_marker_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Before.\n\n"
                "> [!WARNING]\n"
                "> Keep the source body.\n\n"
                "After.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n이전입니다.\n\n"
                "> [!NOTE]\n> 기존 본문입니다.\n\n"
                "<!-- After. -->\n이후입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    ("delete", "> [!NOTE]"),
                    ("add", "> [!WARNING]"),
                    ("context", "> Keep the source body."),
                    ("context", ""),
                    ("context", "After."),
                ],
            )
            cfg = config.Config(
                provider="cli",
                values={"TRANSLATION_PROVIDER": "cli"},
            )

            def translated(request, *_args, **_kwargs):
                self.assertEqual(
                    request.source,
                    "> [!WARNING]\n> Keep the source body.\n",
                )
                return "> [!WARNING]\n> 원문 본문을 유지합니다.\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                side_effect=translated,
            ) as provider:
                issues = main._translate_one(
                    change,
                    cfg,
                    "prompt",
                    dest,
                    locale="ko",
                )

            self.assertEqual(issues, [])
            self.assertEqual(provider.call_count, 1)
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- Before. -->\n이전입니다.\n\n"
                "> [!WARNING]\n> 원문 본문을 유지합니다.\n\n"
                "<!-- After. -->\n이후입니다.\n",
            )

    def test_translate_one_replaces_an_annotated_inline_code_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            old_source = (
                "Before.\n\n"
                "> [!NOTE]\n"
                "> Keep this body.\n\n"
                "Events:\n\n"
                "- `FirstEvent`\n"
                "- `SecondEvent`\n\n"
                "After.\n"
            )
            new_source = old_source.replace(
                "> [!NOTE]",
                "> [!WARNING]",
            ).replace(
                "- `FirstEvent`\n- `SecondEvent`\n",
                "- `FirstEvent`\n- `ThirdEvent`\n- `SecondEvent`\n",
            )
            source_path.write_text(new_source, encoding="utf-8")
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n이전입니다.\n\n"
                "> **Note:** 본문을 유지합니다.\n\n"
                "<!-- Events: -->\n이벤트입니다.\n\n"
                "<!--\n"
                "- `FirstEvent`\n"
                "- `SecondEvent`\n"
                "-->\n"
                "- `FirstEvent`\n"
                "- `SecondEvent`\n\n"
                "<!-- After. -->\n이후입니다.\n",
                encoding="utf-8",
            )
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                status="M",
                hunks=diff.hunks_between(old_source, new_source),
            )
            cfg = config.Config(
                provider="identity",
                values={"TRANSLATION_PROVIDER": "identity"},
            )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                side_effect=lambda request, *_args, **_kwargs: request.source,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest, locale="ko")

            self.assertEqual(issues, [])
            expected = (
                "<!-- Before. -->\n이전입니다.\n\n"
                "> [!WARNING]\n> Keep this body.\n\n"
                "<!-- Events: -->\n이벤트입니다.\n\n"
                "- `FirstEvent`\n"
                "- `ThirdEvent`\n"
                "- `SecondEvent`\n"
                "\n"
                "<!-- After. -->\n이후입니다.\n"
            )
            self.assertEqual(dest.read_text(encoding="utf-8"), expected)

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                side_effect=lambda request, *_args, **_kwargs: request.source,
            ):
                repeated_issues = main._translate_one(
                    change,
                    cfg,
                    "prompt",
                    dest,
                    locale="ko",
                )

            self.assertEqual(repeated_issues, [])
            self.assertEqual(dest.read_text(encoding="utf-8"), expected)

    def test_translate_one_retries_when_segment_still_has_link_mismatches(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Before.\n\n"
                "See [Docs](docs) and [Queues](queues).\n\n"
                "After.\n",
                encoding="utf-8",
            )
            dest = root / "i18n/ja/docusaurus-plugin-content-docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n"
                "前の文です。\n\n"
                "<!-- See [Old Docs](old-docs) and [Queues](queues). -->\n"
                "[Old Docs](old-docs) と [Queues](queues) を参照してください。\n\n"
                "<!-- After. -->\n"
                "後の文です。\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    ("delete", "See [Old Docs](old-docs) and [Queues](queues)."),
                    ("add", "See [Docs](docs) and [Queues](queues)."),
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
                if len(sent) == 1:
                    return (
                        "<!-- See [Docs](docs) and [Queues](queues). -->\n"
                        "[Docs](docs) を参照してください。\n"
                    )
                return (
                    "<!-- See [Docs](docs) and [Queues](queues). -->\n"
                    "[Docs](docs) と [Queues](queues) を参照してください。\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 2)
            self.assertIn("Previous Output Verification Failure", sent[1])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- Before. -->\n"
                "前の文です。\n\n"
                "<!-- See [Docs](docs) and [Queues](queues). -->\n"
                "[Docs](docs) と [Queues](queues) を参照してください。\n\n"
                "<!-- After. -->\n"
                "後の文です。\n",
            )

    def test_translate_one_retries_when_segment_drops_inline_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Before.\n\n"
                "Use `Redis::throttle` with [queues](/docs/13.x/queues).\n\n"
                "After.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n"
                "이전 문장입니다.\n\n"
                "<!-- Use `Redis::funnel` with [queues](/docs/13.x/queues). -->\n"
                "`Redis::funnel`을 [queues](/docs/13.x/queues)와 함께 사용합니다.\n\n"
                "<!-- After. -->\n"
                "이후 문장입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    (
                        "delete",
                        "Use `Redis::funnel` with [queues](/docs/13.x/queues).",
                    ),
                    (
                        "add",
                        "Use `Redis::throttle` with [queues](/docs/13.x/queues).",
                    ),
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
                if len(sent) == 1:
                    return (
                        "<!-- Use `Redis::throttle` with [queues](/docs/13.x/queues). -->\n"
                        "[queues](/docs/13.x/queues)와 함께 사용합니다.\n"
                    )
                return (
                    "<!-- Use `Redis::throttle` with [queues](/docs/13.x/queues). -->\n"
                    "`Redis::throttle`을 [queues](/docs/13.x/queues)와 함께 사용합니다.\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 2)
            self.assertIn("Previous Output Verification Failure", sent[1])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- Before. -->\n"
                "이전 문장입니다.\n\n"
                "<!-- Use `Redis::throttle` with [queues](/docs/13.x/queues). -->\n"
                "`Redis::throttle`을 [queues](/docs/13.x/queues)와 함께 사용합니다.\n\n"
                "<!-- After. -->\n"
                "이후 문장입니다.\n",
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

    def test_delete_outputs_rejects_symlinked_parent_without_partial_deletion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            outside = Path(tmp) / "outside"
            outside.mkdir()
            external_doc = outside / "example.md"
            external_doc.write_text("external\n", encoding="utf-8")
            ko_root = root / "versioned_docs"
            ko_root.mkdir()
            (ko_root / "version-13.x").symlink_to(
                outside,
                target_is_directory=True,
            )
            ja_doc = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs"
                / "version-13.x/example.md"
            )
            ja_doc.parent.mkdir(parents=True)
            ja_doc.write_text("ja\n", encoding="utf-8")
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                status="D",
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._delete_outputs(change)

            self.assertTrue(external_doc.exists())
            self.assertEqual(external_doc.read_text(encoding="utf-8"), "external\n")
            self.assertEqual(ja_doc.read_text(encoding="utf-8"), "ja\n")
            self.assertEqual(
                issues,
                [
                    "unsafe translation output path: "
                    + str(ko_root / "version-13.x/example.md")
                ],
            )

    def test_delete_outputs_validates_ja_path_before_deleting_ko_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            ko_doc = root / "versioned_docs/version-13.x/example.md"
            ko_doc.parent.mkdir(parents=True)
            ko_doc.write_text("ko\n", encoding="utf-8")
            outside = Path(tmp) / "outside"
            outside.mkdir()
            external_doc = outside / "example.md"
            external_doc.write_text("external\n", encoding="utf-8")
            ja_root = root / "i18n/ja/docusaurus-plugin-content-docs"
            ja_root.mkdir(parents=True)
            (ja_root / "version-13.x").symlink_to(
                outside,
                target_is_directory=True,
            )
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                status="D",
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._delete_outputs(change)

            self.assertEqual(ko_doc.read_text(encoding="utf-8"), "ko\n")
            self.assertEqual(external_doc.read_text(encoding="utf-8"), "external\n")
            self.assertEqual(
                issues,
                [
                    "unsafe translation output path: "
                    + str(ja_root / "version-13.x/example.md")
                ],
            )

    def test_added_document_rejects_symlinked_final_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs"
                / "version-13.x/example.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text("# Example\n", encoding="utf-8")
            outside = Path(tmp) / "outside.md"
            outside.write_text("external\n", encoding="utf-8")
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.symlink_to(outside)
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                status="A",
            )
            cfg = config.Config(
                provider="identity",
                values={"TRANSLATION_PROVIDER": "identity"},
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(outside.read_text(encoding="utf-8"), "external\n")
            self.assertTrue(dest.is_symlink())
            self.assertEqual(
                issues,
                ["unsafe translation output path: " + str(dest)],
            )

    def test_added_document_replaces_hardlink_without_mutating_other_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs"
                / "version-13.x/example.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text("# Example\n", encoding="utf-8")
            victim = root / "outside.md"
            victim.write_text("external\n", encoding="utf-8")
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.hardlink_to(victim)
            dest.chmod(0o640)
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                status="A",
            )
            cfg = config.Config(
                provider="identity",
                values={"TRANSLATION_PROVIDER": "identity"},
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(victim.read_text(encoding="utf-8"), "external\n")
            self.assertNotEqual(dest.read_text(encoding="utf-8"), "external\n")
            self.assertFalse(dest.samefile(victim))
            self.assertEqual(dest.stat().st_mode & 0o777, 0o640)

    def test_identity_replay_allows_source_echo_after_structural_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old_source = "Before.\n\nOld source sentence.\n\nAfter.\n"
            new_source = "Before.\n\nNew source sentence.\n\nAfter.\n"
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs"
                / "version-13.x/example.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text(new_source, encoding="utf-8")
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n이전입니다.\n\n"
                "<!-- Old source sentence. -->\n기존 문장입니다.\n\n"
                "<!-- After. -->\n이후입니다.\n",
                encoding="utf-8",
            )
            change = diff.SourceChange(
                path=(
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-13.x/example.md"
                ),
                status="M",
                hunks=diff.hunks_between(old_source, new_source),
            )
            cfg = config.Config(
                provider="identity",
                values={"TRANSLATION_PROVIDER": "identity"},
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertIn("<!-- New source sentence. -->", dest.read_text())

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
            (source.parent.parent / "version-12.x.json").write_text(
                "{}\n",
                encoding="utf-8",
            )

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

    def test_select_changes_migrate_existing_rejects_source_symlinks(self):
        for component in ("root", "version", "leaf"):
            with self.subTest(component=component), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                root = base / "repo"
                root.mkdir()
                outside = base / "outside"
                outside.mkdir()

                if component == "root":
                    (outside / "version-13.x").mkdir()
                    (outside / "version-13.x/example.md").write_text(
                        "# External\n",
                        encoding="utf-8",
                    )
                    (root / "i18n/en").mkdir(parents=True)
                    (
                        root
                        / "i18n/en/docusaurus-plugin-content-docs"
                    ).symlink_to(outside, target_is_directory=True)
                elif component == "version":
                    (outside / "example.md").write_text(
                        "# External\n",
                        encoding="utf-8",
                    )
                    en_root = (
                        root / "i18n/en/docusaurus-plugin-content-docs"
                    )
                    en_root.mkdir(parents=True)
                    (en_root / "version-13.x").symlink_to(
                        outside,
                        target_is_directory=True,
                    )
                else:
                    outside_doc = outside / "example.md"
                    outside_doc.write_text("# External\n", encoding="utf-8")
                    version_root = (
                        root
                        / "i18n/en/docusaurus-plugin-content-docs/version-13.x"
                    )
                    version_root.mkdir(parents=True)
                    (version_root / "example.md").symlink_to(outside_doc)

                with patch.object(main, "REPO_ROOT", root):
                    with self.assertRaisesRegex(
                        main.SourcePathError,
                        "unsafe English source path",
                    ):
                        main._select_changes(migrate_existing=True)

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
            main.config,
            "load_config",
            return_value=config.Config(
                provider="cli", values={"TRANSLATION_PROVIDER": "cli"}
            ),
        ), patch.object(
            main.upstream, "main", return_value=0
        ), patch.object(main.diff, "changed_sources", return_value=[]), patch.object(
            main.sidebar, "sync_versions", side_effect=sync_versions
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(calls, [(["master"], True)])

    def test_main_scopes_upstream_sync_to_requested_filters(self):
        with patch.object(
            main.sys,
            "argv",
            ["main.py", "--version", "13.x", "--doc", "collections"],
        ), patch.object(
            main.config,
            "load_config",
            return_value=config.Config(
                provider="cli", values={"TRANSLATION_PROVIDER": "cli"}
            ),
        ), patch.object(
            main.upstream, "main", return_value=0
        ) as upstream_main, patch.object(
            main.diff, "changed_sources", return_value=[]
        ), patch.object(
            main.sidebar,
            "sync_versions",
            return_value=[main.sidebar.SidebarResult("13.x", False, [])],
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 0)
        upstream_main.assert_called_once_with(version="13.x", doc="collections.md")

    def test_main_reports_missing_filter_value_without_traceback(self):
        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            main.sys, "argv", ["main.py", "--version"]
        ), patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 2)
        self.assertEqual(
            stderr.getvalue(),
            "configuration failed: --version requires a value\n",
        )

    def test_main_rejects_unknown_argument_before_upstream_sync(self):
        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            main.sys, "argv", ["main.py", "--versoin", "13.x"]
        ), patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 2)
        self.assertEqual(
            stderr.getvalue(),
            "configuration failed: unknown argument: --versoin\n",
        )

    def test_main_rejects_empty_equals_filter_before_upstream_sync(self):
        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            main.sys, "argv", ["main.py", "--version="]
        ), patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 2)
        self.assertEqual(
            stderr.getvalue(),
            "configuration failed: --version requires a value\n",
        )

    def test_main_rejects_multiple_maintenance_modes(self):
        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            main.sys,
            "argv",
            ["main.py", "--check-annotations", "--annotate-existing"],
        ), patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 2)
        self.assertEqual(
            stderr.getvalue(),
            "configuration failed: maintenance modes are mutually exclusive\n",
        )

    def test_main_rejects_apply_without_writable_maintenance_mode(self):
        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            main.sys, "argv", ["main.py", "--apply"]
        ), patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 2)
        self.assertEqual(
            stderr.getvalue(),
            "configuration failed: --apply requires --annotate-existing or "
            "--fix-preserved-markup\n",
        )

    def test_main_rejects_fail_fast_in_maintenance_mode(self):
        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            main.sys,
            "argv",
            ["main.py", "--check-annotations", "--fail-fast"],
        ), patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 2)
        self.assertEqual(
            stderr.getvalue(),
            "configuration failed: --fail-fast is only valid for translation sync\n",
        )

    def test_main_rejects_broken_migrate_existing_mode(self):
        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            main.sys, "argv", ["main.py", "--migrate-existing"]
        ), patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 2)
        self.assertEqual(
            stderr.getvalue(),
            "configuration failed: --migrate-existing is unsupported; use "
            "--annotate-existing or --fix-preserved-markup\n",
        )

    def test_main_allows_apply_with_annotation_maintenance(self):
        with patch.object(
            main.sys,
            "argv",
            ["main.py", "--annotate-existing", "--apply", "--version=13.x"],
        ), patch.object(
            main, "_annotate_existing", return_value=(0, [])
        ) as annotate_existing, patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 0)
        annotate_existing.assert_called_once_with(
            apply=True,
            version="13.x",
            doc=None,
        )

    def test_fix_preserved_markup_repairs_markdown_image_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-13.x/example.md"
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            source.write_text(
                "![Tutorial](/images/tutorial.png)\n",
                encoding="utf-8",
            )
            ko_doc.write_text(
                "<!-- ![Tutorial](/images/tutorial.png) -->\n"
                "![튜토리얼](/이미지/tutorial.png)\n",
                encoding="utf-8",
            )
            stdout = io.StringIO()

            with redirect_stdout(stdout), patch.object(
                main, "REPO_ROOT", root
            ), patch.object(
                main.sys,
                "argv",
                [
                    "main.py",
                    "--fix-preserved-markup",
                    "--apply",
                    "--version",
                    "13.x",
                    "--doc",
                    "example.md",
                ],
            ):
                exit_code = main.main()

            self.assertEqual(exit_code, 0)
            self.assertEqual(
                stdout.getvalue(),
                "existing preserved markup fixes written: 1\n",
            )
            self.assertEqual(
                ko_doc.read_text(encoding="utf-8"),
                "<!-- ![Tutorial](/images/tutorial.png) -->\n"
                "![튜토리얼](/images/tutorial.png)\n",
            )

    def test_fix_preserved_markup_repairs_markdown_link_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-13.x/example.md"
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            source.write_text(
                'See [Docs](guide.md "Read more").\n',
                encoding="utf-8",
            )
            ko_doc.write_text(
                '<!-- See [Docs](guide.md "Read more"). -->\n'
                '[Docs](guide.md "자세히 보기")를 참고하세요.\n',
                encoding="utf-8",
            )
            stdout = io.StringIO()
            stderr = io.StringIO()

            with redirect_stdout(stdout), redirect_stderr(stderr), patch.object(
                main, "REPO_ROOT", root
            ), patch.object(
                main.sys,
                "argv",
                [
                    "main.py",
                    "--fix-preserved-markup",
                    "--apply",
                    "--version",
                    "13.x",
                    "--doc",
                    "example.md",
                ],
            ):
                exit_code = main.main()

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr.getvalue(), "")
            self.assertEqual(
                stdout.getvalue(),
                "existing preserved markup fixes written: 1\n",
            )
            self.assertEqual(
                ko_doc.read_text(encoding="utf-8"),
                '<!-- See [Docs](guide.md "Read more"). -->\n'
                '[Docs](guide.md "Read more")를 참고하세요.\n',
            )

    def test_fix_preserved_markup_reports_unresolved_fixable_issue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-13.x/example.md"
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            source.write_text(
                "Visit <https://example.com/source>.\n",
                encoding="utf-8",
            )
            original = (
                "<!-- Visit <https://example.com/source>. -->\n"
                "<https://example.com/wrong>을 방문하세요.\n"
            )
            ko_doc.write_text(original, encoding="utf-8")
            stdout = io.StringIO()
            stderr = io.StringIO()

            with redirect_stdout(stdout), redirect_stderr(stderr), patch.object(
                main, "REPO_ROOT", root
            ), patch.object(
                main.sys,
                "argv",
                [
                    "main.py",
                    "--fix-preserved-markup",
                    "--apply",
                    "--version",
                    "13.x",
                    "--doc",
                    "example.md",
                ],
            ):
                exit_code = main.main()

            self.assertEqual(exit_code, 1)
            self.assertEqual(
                stdout.getvalue(),
                "existing preserved markup fixes written: 0\n",
            )
            self.assertIn(
                "preserved markup fix skipped: ko "
                "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md: "
                "link target mismatch, link pair mismatch\n",
                stderr.getvalue(),
            )
            self.assertEqual(ko_doc.read_text(encoding="utf-8"), original)

    def test_main_fail_fast_stops_after_first_verification_failure(self):
        change = diff.SourceChange(
            path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
            status="M",
        )
        calls: list[str] = []

        def translate_one(change, cfg, prompt, dest, *, locale=None):
            self.assertIn(locale, ("ko", "ja"))
            calls.append(str(dest))
            return ["heading mismatch"]

        with patch.object(
            main.sys, "argv", ["main.py", "--fail-fast"]
        ), patch.object(main.upstream, "main", return_value=0), patch.object(
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

    def test_main_stops_when_upstream_sync_fails(self):
        with patch.object(main.sys, "argv", ["main.py"]), patch.object(
            main.config,
            "load_config",
            return_value=config.Config(
                provider="cli", values={"TRANSLATION_PROVIDER": "cli"}
            ),
        ), patch.object(
            main.upstream, "main", return_value=1
        ), patch.object(
            main.diff,
            "changed_sources",
            side_effect=AssertionError("diff should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 1)

    def test_main_reports_invalid_provider_configuration_without_traceback(self):
        change = diff.SourceChange(
            path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
            status="M",
        )
        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            main.sys, "argv", ["main.py"]
        ), patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ), patch.object(
            main.config,
            "load_config",
            side_effect=config.ConfigError(
                "TRANSLATION_CLI_TIMEOUT must be an integer > 0"
            ),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 2)
        self.assertEqual(
            stderr.getvalue(),
            "configuration failed: "
            "TRANSLATION_CLI_TIMEOUT must be an integer > 0\n",
        )

    def test_main_reports_missing_prompt_before_upstream_sync(self):
        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            main.sys, "argv", ["main.py"]
        ), patch.object(
            main.config,
            "load_config",
            return_value=config.Config(
                provider="cli", values={"TRANSLATION_PROVIDER": "cli"}
            ),
        ), patch.object(
            main,
            "_load_prompts",
            side_effect=main.prompt.PromptError("missing prompt file: prompt.md"),
        ), patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 2)
        self.assertEqual(
            stderr.getvalue(),
            "prompt loading failed: missing prompt file: prompt.md\n",
        )

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
                "ko i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md: source comment mismatch",
                "ko i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md: missing original comment",
                "ja i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md: heading text mismatch",
                "ja i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md: source comment mismatch",
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

    def test_annotate_existing_normalizes_legacy_alert_without_missing_comments(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-12.x/example.md"
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            source.write_text(
                "> [!NOTE]\n> Body text.\n",
                encoding="utf-8",
            )
            ko_doc.write_text(
                "> **Note:**\n> 본문입니다.\n",
                encoding="utf-8",
            )

            with patch.object(main, "REPO_ROOT", root):
                written, failures = main._annotate_existing(apply=True)

            self.assertEqual(written, 1)
            self.assertEqual(failures, [])
            self.assertEqual(
                ko_doc.read_text(encoding="utf-8"),
                "> [!NOTE]\n> 본문입니다.\n",
            )

    def test_annotate_existing_repairs_source_comment_mismatch_without_missing_comment(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-12.x/example.md"
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            source.write_text(
                '<a name="cache"></a>\n\nCache body.\n',
                encoding="utf-8",
            )
            ko_doc.write_text(
                '<a name="cache"></a>\n\n'
                "<!-- Cache body. -->\n"
                "캐시 본문입니다.\n\n"
                '<!-- <a name="cache"></a> -->\n',
                encoding="utf-8",
            )

            with patch.object(main, "REPO_ROOT", root):
                written, failures = main._annotate_existing(apply=True)

            self.assertEqual(written, 1)
            self.assertEqual(failures, [])
            self.assertNotIn(
                '<!-- <a name="cache"></a> -->',
                ko_doc.read_text(encoding="utf-8"),
            )

    def test_annotate_existing_writes_canonical_stale_links_when_document_verifies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-12.x/example.md"
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            source.write_text(
                "- [Agents](#agents-integration)\n",
                encoding="utf-8",
            )
            ko_doc.write_text(
                "- [Agents](#agents-integration)\n",
                encoding="utf-8",
            )

            with patch.object(main, "REPO_ROOT", root):
                written, failures = main._annotate_existing(apply=True)

            self.assertEqual(written, 1)
            self.assertEqual(failures, [])
            self.assertIn(
                "- [Agents](#agent-integration)\n",
                ko_doc.read_text(encoding="utf-8"),
            )

    def test_annotate_existing_restores_blank_markdown_link_label(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-12.x/example.md"
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            source.write_text(
                "See [`Type`](guide.md#type).\n",
                encoding="utf-8",
            )
            ko_doc.write_text(
                "<!-- See [`Type`](guide.md#type). -->\n"
                "[    ](guide.md#type)을 참고하세요.\n",
                encoding="utf-8",
            )

            with patch.object(main, "REPO_ROOT", root):
                written, failures = main._annotate_existing(apply=True)

            self.assertEqual(written, 1)
            self.assertEqual(failures, [])
            self.assertIn(
                "[`Type`](guide.md#type)을 참고하세요.\n",
                ko_doc.read_text(encoding="utf-8"),
            )

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
