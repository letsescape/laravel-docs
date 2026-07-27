import os
import json
import stat
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sync.common import files


class AtomicWriteTests(unittest.TestCase):
    def test_text_write_fsyncs_file_and_parent_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "example.md"
            real_fsync = os.fsync
            targets: list[str] = []

            def record(descriptor: int) -> None:
                mode = os.fstat(descriptor).st_mode
                targets.append(
                    "directory" if stat.S_ISDIR(mode) else "file"
                )
                real_fsync(descriptor)

            with patch.object(files.os, "fsync", side_effect=record):
                files.atomic_write_text(path, "new\n")

            self.assertEqual(targets, ["file", "directory"])
            self.assertEqual(path.read_text(encoding="utf-8"), "new\n")

    def test_unlink_fsyncs_parent_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "example.md"
            path.write_text("old\n", encoding="utf-8")
            real_fsync = os.fsync
            targets: list[str] = []

            def record(descriptor: int) -> None:
                mode = os.fstat(descriptor).st_mode
                targets.append(
                    "directory" if stat.S_ISDIR(mode) else "file"
                )
                real_fsync(descriptor)

            with patch.object(files.os, "fsync", side_effect=record):
                removed = files.unlink_file(path)

            self.assertTrue(removed)
            self.assertEqual(targets, ["directory"])
            self.assertFalse(path.exists())


class E2EContainerContractTests(unittest.TestCase):
    def test_e2e_container_uses_node_26_and_the_pinned_playwright_version(self):
        repo_root = Path(__file__).resolve().parents[2]
        package = json.loads((repo_root / "package.json").read_text(encoding="utf-8"))
        playwright_version = package["devDependencies"]["@playwright/test"]
        dockerfile = (repo_root / "Dockerfile.playwright").read_text(encoding="utf-8")

        self.assertIn("FROM node:26-bookworm", dockerfile)
        self.assertIn(f"ARG PLAYWRIGHT_VERSION={playwright_version}", dockerfile)
        self.assertIn("playwright@${PLAYWRIGHT_VERSION}", dockerfile)
        self.assertIn(
            "Dockerfile.playwright",
            package["scripts"]["test:e2e:docker"],
        )


if __name__ == "__main__":
    unittest.main()
