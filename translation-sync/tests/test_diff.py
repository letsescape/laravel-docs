import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sync import diff


class DiffTests(unittest.TestCase):
    def test_changed_sources_disables_optional_git_locks(self):
        calls = []

        def fake_run(args, **kwargs):
            calls.append((args, kwargs))
            return subprocess.CompletedProcess(args, 0, stdout="", stderr="")

        with patch.object(diff.subprocess, "run", side_effect=fake_run):
            changes = diff.changed_sources()

        self.assertEqual(changes, [])
        self.assertEqual(calls[0][1]["env"]["GIT_OPTIONAL_LOCKS"], "0")

    def test_changed_sources_includes_untracked_new_markdown_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/new-topic.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text("# New Topic\n", encoding="utf-8")

            with patch.object(diff, "REPO_ROOT", root):
                changes = diff.changed_sources()

        self.assertEqual(len(changes), 1)
        self.assertEqual(
            changes[0].path,
            "i18n/en/docusaurus-plugin-content-docs/version-12.x/new-topic.md",
        )
        self.assertEqual(changes[0].status, "A")
        self.assertEqual(
            [(line.kind, line.text) for line in changes[0].hunks[0].lines],
            [("add", "# New Topic")],
        )

    def test_changed_sources_includes_unified_hunks_for_modified_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=root,
                check=True,
            )
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-master/example.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text("Before.\n\nOld text.\n\nAfter.\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-m", "baseline"],
                cwd=root,
                check=True,
                capture_output=True,
            )

            source.write_text("Before.\n\nNew text.\n\nAfter.\n", encoding="utf-8")

            with patch.object(diff, "REPO_ROOT", root):
                changes = diff.changed_sources()

        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].status, "M")
        self.assertEqual(changes[0].version, "master")
        self.assertEqual(changes[0].name, "example.md")
        self.assertEqual(len(changes[0].hunks), 1)
        self.assertEqual(
            [(line.kind, line.text) for line in changes[0].hunks[0].lines],
            [
                ("context", "Before."),
                ("context", ""),
                ("delete", "Old text."),
                ("add", "New text."),
                ("context", ""),
                ("context", "After."),
            ],
        )


if __name__ == "__main__":
    unittest.main()
