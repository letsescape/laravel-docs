import io
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

import validate_generated_changes


class GeneratedChangeTests(unittest.TestCase):
    def test_changed_entries_normalizes_staged_rename_records(self):
        rename_and_modify = (
            b"R100\0versioned_docs/version-13.x/old.md\0"
            b"versioned_docs/version-13.x/new.md\0"
            b"M\0versioned_sidebars/version-13.x-sidebars.json\0"
        )

        with patch.object(
            validate_generated_changes.subprocess,
            "run",
            side_effect=[
                CompletedProcess([], 0, stdout=b""),
                CompletedProcess([], 0, stdout=rename_and_modify),
                CompletedProcess([], 0, stdout=b""),
            ],
        ):
            changes = validate_generated_changes.changed_entries(Path("/repo"))

        self.assertEqual(
            changes,
            {
                "versioned_docs/version-13.x/old.md": {"D"},
                "versioned_docs/version-13.x/new.md": {"A"},
                "versioned_sidebars/version-13.x-sidebars.json": {"M"},
            },
        )

    def test_changed_entries_normalizes_copy_records_to_the_new_path(self):
        copy = (
            b"C087\0versioned_docs/version-13.x/source.md\0"
            b"versioned_docs/version-13.x/copy.md\0"
        )

        with patch.object(
            validate_generated_changes.subprocess,
            "run",
            side_effect=[
                CompletedProcess([], 0, stdout=b""),
                CompletedProcess([], 0, stdout=copy),
                CompletedProcess([], 0, stdout=b""),
            ],
        ):
            changes = validate_generated_changes.changed_entries(Path("/repo"))

        self.assertEqual(
            changes,
            {"versioned_docs/version-13.x/copy.md": {"A"}},
        )

    def test_changed_entries_rejects_malformed_name_status_output(self):
        invalid_outputs = (
            b"R100\0versioned_docs/version-13.x/old.md\0",
            b"M\0../README.md\0",
            b"R999\0versioned_docs/version-13.x/old.md\0"
            b"versioned_docs/version-13.x/new.md\0",
        )

        for output in invalid_outputs:
            with self.subTest(output=output), patch.object(
                validate_generated_changes.subprocess,
                "run",
                side_effect=[CompletedProcess([], 0, stdout=output)],
            ):
                with self.assertRaisesRegex(
                    RuntimeError, "invalid git name-status output"
                ):
                    validate_generated_changes.changed_entries(Path("/repo"))

    def test_only_translation_outputs_are_allowed(self):
        paths = {
            "i18n/en/docusaurus-plugin-content-docs/version-13.x/cache.md",
            "versioned_docs/version-13.x/cache.md",
            "i18n/ja/docusaurus-plugin-content-docs/version-13.x/cache.md",
            "versioned_sidebars/version-13.x-sidebars.json",
            "i18n/ko/docusaurus-plugin-content-docs/version-13.x.json",
            "i18n/ja/docusaurus-plugin-content-docs/version-master.json",
            "README.md",
            ".github/workflows/deploy.yml",
        }

        self.assertEqual(
            validate_generated_changes.unexpected_paths(paths),
            [".github/workflows/deploy.yml", "README.md"],
        )

    def test_rejects_unsupported_versions_and_unpaired_locale_outputs(self):
        changes = {
            "i18n/en/docusaurus-plugin-content-docs/version-999.x/cache.md": {"M"},
            "versioned_docs/version-13.x/orphan.md": {"M"},
        }

        self.assertEqual(
            validate_generated_changes.validate_changes(changes, {"13.x", "master"}),
            [
                "unsupported translation version: "
                "i18n/en/docusaurus-plugin-content-docs/version-999.x/cache.md",
                "unpaired translation document: version-13.x/orphan.md",
            ],
        )

    def test_accepts_complete_translation_document_triplet(self):
        changes = {
            "i18n/en/docusaurus-plugin-content-docs/version-13.x/cache.md": {"M"},
            "versioned_docs/version-13.x/cache.md": {"M"},
            "i18n/ja/docusaurus-plugin-content-docs/version-13.x/cache.md": {"M"},
        }

        self.assertEqual(
            validate_generated_changes.validate_changes(changes, {"13.x"}),
            [],
        )

    def test_accepts_unchanged_locale_that_is_already_at_target(self):
        changes = {
            "i18n/en/docusaurus-plugin-content-docs/version-13.x/cache.md": {"M"},
            "i18n/ja/docusaurus-plugin-content-docs/version-13.x/cache.md": {"M"},
        }

        self.assertEqual(
            validate_generated_changes.validate_changes(changes, {"13.x"}),
            [
                "unverified unchanged translation: "
                "version-13.x/cache.md (ko)"
            ],
        )
        self.assertEqual(
            validate_generated_changes.validate_changes(
                changes,
                {"13.x"},
                verified_unchanged={("13.x", "cache.md", "ko")},
            ),
            [],
        )

    def test_rejects_en_only_modification_without_locale_proof(self):
        changes = {
            "i18n/en/docusaurus-plugin-content-docs/version-13.x/cache.md": {"M"},
        }

        self.assertEqual(
            validate_generated_changes.validate_changes(changes, {"13.x"}),
            [
                "unverified unchanged translation: "
                "version-13.x/cache.md (ja)",
                "unverified unchanged translation: "
                "version-13.x/cache.md (ko)",
            ],
        )

    def test_proves_unchanged_locale_content_with_the_final_verifier(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/"
                "version-13.x/cache.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text("Install the package.\n", encoding="utf-8")
            target = root / "versioned_docs/version-13.x/cache.md"
            target.parent.mkdir(parents=True)
            target.write_text(
                "<!-- Install the package. -->\n패키지를 설치합니다.\n",
                encoding="utf-8",
            )
            changes = {str(source.relative_to(root)): {"M"}}

            self.assertEqual(
                validate_generated_changes.verified_unchanged_locales(
                    changes,
                    root,
                ),
                {("13.x", "cache.md", "ko")},
            )

    def test_rejects_symlink_output_leaf_and_ancestor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root / "outside"
            outside.mkdir()
            (outside / "cache.md").write_text("outside\n", encoding="utf-8")

            leaf = (
                root
                / "versioned_docs/version-13.x/cache.md"
            )
            leaf.parent.mkdir(parents=True)
            leaf.symlink_to(outside / "cache.md")

            ancestor = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x"
            )
            ancestor.parent.mkdir(parents=True)
            ancestor.symlink_to(outside, target_is_directory=True)

            self.assertEqual(
                validate_generated_changes.unsafe_output_paths(
                    {
                        "versioned_docs/version-13.x/cache.md",
                        "i18n/en/docusaurus-plugin-content-docs/"
                        "version-13.x/cache.md",
                    },
                    root,
                ),
                [
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-13.x/cache.md",
                    "versioned_docs/version-13.x/cache.md",
                ],
            )

    def test_accepts_regular_and_deleted_output_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            regular = root / "versioned_docs/version-13.x/cache.md"
            regular.parent.mkdir(parents=True)
            regular.write_text("translated\n", encoding="utf-8")

            self.assertEqual(
                validate_generated_changes.unsafe_output_paths(
                    {
                        "versioned_docs/version-13.x/cache.md",
                        "versioned_docs/version-13.x/deleted.md",
                    },
                    root,
                ),
                [],
            )

    def test_rejects_mismatched_translation_deletion(self):
        changes = {
            "i18n/en/docusaurus-plugin-content-docs/version-13.x/cache.md": {"D"},
            "versioned_docs/version-13.x/cache.md": {"D"},
            "i18n/ja/docusaurus-plugin-content-docs/version-13.x/cache.md": {"M"},
        }

        self.assertEqual(
            validate_generated_changes.validate_changes(changes, {"13.x"}),
            ["inconsistent translation status: version-13.x/cache.md"],
        )

    def test_locale_sidebar_overrides_must_not_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            override = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs/version-13.x.json"
            )
            override.parent.mkdir(parents=True)
            override.write_text("{}\n", encoding="utf-8")

            self.assertEqual(
                validate_generated_changes.existing_sidebar_overrides(root),
                ["i18n/ja/docusaurus-plugin-content-docs/version-13.x.json"],
            )

    def test_main_rejects_invalid_versions_file_cleanly(self):
        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            validate_generated_changes,
            "changed_entries",
            return_value={},
        ), patch.object(
            validate_generated_changes,
            "load_versions",
            side_effect=ValueError("versions.json must not be empty"),
        ):
            result = validate_generated_changes.main()

        self.assertEqual(result, 1)
        self.assertEqual(
            stderr.getvalue(),
            "invalid versions.json: versions.json must not be empty\n",
        )


if __name__ == "__main__":
    unittest.main()
