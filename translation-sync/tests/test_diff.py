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

        self.assertEqual(
            changes,
            [
                diff.SourceChange(
                    path="i18n/en/docusaurus-plugin-content-docs/version-12.x/new-topic.md",
                    status="A",
                )
            ],
        )


if __name__ == "__main__":
    unittest.main()
