import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import replay


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )


def _init_repo(root: Path, main_source: str) -> None:
    (root / "translation-sync").mkdir()
    (root / "translation-sync/main.py").write_text(main_source, encoding="utf-8")
    (root / "tracked.txt").write_text("original\n", encoding="utf-8")
    (root / "deleted.txt").write_text("delete me\n", encoding="utf-8")
    _git(root, "init", "--quiet")
    _git(root, "config", "user.name", "Replay Tests")
    _git(root, "config", "user.email", "replay-tests@localhost")
    _git(root, "add", "-A")
    _git(root, "commit", "--quiet", "-m", "fixture")


def _workflow_run_script(step_name: str) -> str:
    workflow = (
        Path(__file__).resolve().parents[2]
        / ".github"
        / "workflows"
        / "sync-translation.yml"
    ).read_text(encoding="utf-8")
    step = workflow.split(f"      - name: {step_name}\n", 1)[1]
    step = step.split("\n      - name:", 1)[0]
    body = step.split("        run: |\n", 1)[1]
    return "\n".join(line[10:] if line else "" for line in body.splitlines())


class TranslationReplayTests(unittest.TestCase):
    def setUp(self) -> None:
        manifest_environment = patch.dict(
            os.environ,
            {replay.MANIFEST_ENV: ""},
        )
        manifest_environment.start()
        self.addCleanup(manifest_environment.stop)

    def test_missing_external_manifest_is_exported_only_after_sandbox_replay(
        self,
    ) -> None:
        main_source = """\
import os
from pathlib import Path

root = Path(__file__).resolve().parent.parent
manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"]).resolve()
if not manifest.is_relative_to(root):
    raise SystemExit(9)
if manifest.exists():
    raise SystemExit(
        0 if manifest.read_text(encoding="utf-8") == "generated\\n" else 9
    )
manifest.write_text("generated\\n", encoding="utf-8")
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"
            external_manifest = Path(tmp) / "outputs/upstream-refs.json"

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(external_manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_OK)
            self.assertEqual(
                external_manifest.read_text(encoding="utf-8"),
                "generated\n",
            )
            self.assertEqual(list(sandboxes.iterdir()), [])

    def test_existing_external_manifest_is_staged_as_read_only_input(self) -> None:
        main_source = """\
import os
from pathlib import Path

root = Path(__file__).resolve().parent.parent
manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"]).resolve()
checks = [
    manifest.is_relative_to(root),
    manifest.read_text(encoding="utf-8") == "pinned\\n",
    manifest.stat().st_mode & 0o222 == 0,
]
raise SystemExit(0 if all(checks) else 9)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"
            external_manifest = Path(tmp) / "upstream-refs.json"
            external_manifest.write_text("pinned\n", encoding="utf-8")

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(external_manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_OK)
            self.assertEqual(
                external_manifest.read_text(encoding="utf-8"),
                "pinned\n",
            )
            self.assertEqual(list(sandboxes.iterdir()), [])

    def test_manifest_destination_inside_active_repository_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"
            manifest = root / "generated/upstream-refs.json"

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertFalse(manifest.exists())
            self.assertFalse(sandboxes.exists())
            self.assertEqual(_git(root, "status", "--porcelain").stdout, "")

    def test_case_alias_inside_active_repository_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(
                root,
                """\
import os
from pathlib import Path

manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"])
if not manifest.exists():
    manifest.write_text("generated\\n", encoding="utf-8")
""",
            )
            alias = root.with_name(root.name.upper())
            try:
                same_repository = alias.samefile(root)
            except OSError:
                same_repository = False
            if not same_repository:
                self.skipTest("filesystem is case-sensitive")
            sandboxes = Path(tmp) / "sandboxes"
            manifest = alias / "upstream-refs.json"

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertFalse(root.joinpath("upstream-refs.json").exists())
            self.assertFalse(sandboxes.exists())

    def test_manifest_ancestor_created_as_active_repo_symlink_is_rejected(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            late_parent = Path(tmp) / "outputs/late"
            late_parent.parent.mkdir()
            main_source = f"""\
import os
from pathlib import Path

manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"])
if not manifest.exists():
    manifest.write_text("generated\\n", encoding="utf-8")
late_parent = Path({str(late_parent)!r})
if not late_parent.exists():
    late_parent.symlink_to(Path({str(root)!r}), target_is_directory=True)
"""
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"
            manifest = late_parent / "upstream-refs.json"

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertFalse(root.joinpath("upstream-refs.json").exists())

    def test_symlink_manifest_target_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"
            target = Path(tmp) / "actual-refs.json"
            target.write_text("pinned\n", encoding="utf-8")
            manifest = Path(tmp) / "upstream-refs.json"
            manifest.symlink_to(target)

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertTrue(manifest.is_symlink())
            self.assertEqual(target.read_text(encoding="utf-8"), "pinned\n")
            self.assertFalse(sandboxes.exists())

    def test_non_regular_manifest_target_is_rejected_before_replay(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"
            manifest = Path(tmp) / "upstream-refs.json"
            manifest.mkdir()

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertTrue(manifest.is_dir())
            self.assertFalse(sandboxes.exists())

    def test_manifest_created_during_replay_is_never_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            external_manifest = Path(tmp) / "upstream-refs.json"
            main_source = f"""\
import os
from pathlib import Path

manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"])
if not manifest.exists():
    manifest.write_text("generated\\n", encoding="utf-8")
external = Path({str(external_manifest)!r})
if not external.exists():
    external.write_text("created concurrently\\n", encoding="utf-8")
"""
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(external_manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertEqual(
                external_manifest.read_text(encoding="utf-8"),
                "created concurrently\n",
            )
            self.assertEqual(list(sandboxes.iterdir()), [])

    def test_failed_replay_does_not_export_generated_manifest(self) -> None:
        main_source = """\
import os
from pathlib import Path

manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"])
manifest.write_text("must not escape\\n", encoding="utf-8")
raise SystemExit(9)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"
            external_manifest = Path(tmp) / "upstream-refs.json"

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(external_manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertFalse(external_manifest.exists())
            self.assertEqual(len(list(sandboxes.iterdir())), 1)

    def test_existing_manifest_is_snapshotted_before_replay_setup(self) -> None:
        main_source = """\
import os
from pathlib import Path

manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"])
raise SystemExit(
    0 if manifest.read_text(encoding="utf-8") == "pinned\\n" else 9
)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"
            external_manifest = Path(tmp) / "upstream-refs.json"
            external_manifest.write_text("pinned\n", encoding="utf-8")
            replacement = Path(tmp) / "replacement.json"
            replacement.write_text("replacement\n", encoding="utf-8")
            original_create_sandbox = replay._create_sandbox  # noqa: SLF001

            def replace_after_sandbox(
                source: Path, sandbox_parent: Path | None
            ) -> Path:
                sandbox = original_create_sandbox(source, sandbox_parent)
                external_manifest.unlink()
                external_manifest.symlink_to(replacement)
                return sandbox

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(external_manifest)},
            ), patch.object(
                replay,
                "_create_sandbox",
                side_effect=replace_after_sandbox,
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_OK)
            self.assertTrue(external_manifest.is_symlink())
            self.assertEqual(
                replacement.read_text(encoding="utf-8"),
                "replacement\n",
            )

    def test_manifest_is_not_published_until_complete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "sandbox-manifest.json"
            source.write_text("generated\n", encoding="utf-8")
            destination = Path(tmp) / "published/manifest.json"
            observed: list[bool] = []
            real_fsync = os.fsync

            def observe_publication(descriptor: int) -> None:
                observed.append(destination.exists())
                real_fsync(descriptor)

            with patch.object(replay.os, "fsync", side_effect=observe_publication):
                replay._export_manifest(source, destination)  # noqa: SLF001

            self.assertEqual(observed, [False])
            self.assertEqual(
                destination.read_text(encoding="utf-8"),
                "generated\n",
            )

    def test_interrupted_manifest_export_leaves_no_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "sandbox-manifest.json"
            source.write_text("generated\n", encoding="utf-8")
            destination = Path(tmp) / "published/manifest.json"

            with patch.object(replay.os, "fsync", side_effect=KeyboardInterrupt):
                with self.assertRaises(KeyboardInterrupt):
                    replay._export_manifest(source, destination)  # noqa: SLF001

            self.assertFalse(destination.exists())
            self.assertEqual(list(destination.parent.iterdir()), [])

    def test_failed_export_does_not_delete_concurrent_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "sandbox-manifest.json"
            source.write_text("generated\n", encoding="utf-8")
            destination = Path(tmp) / "published/manifest.json"
            moved = Path(tmp) / "opened-manifest.json"

            def replace_and_fail(_descriptor: int) -> None:
                if destination.exists():
                    destination.rename(moved)
                destination.write_text("concurrent\n", encoding="utf-8")
                raise OSError("injected write failure")

            with patch.object(replay.os, "fsync", side_effect=replace_and_fail):
                with self.assertRaises(OSError):
                    replay._export_manifest(source, destination)  # noqa: SLF001

            self.assertEqual(
                destination.read_text(encoding="utf-8"),
                "concurrent\n",
            )
            self.assertEqual(list(destination.parent.iterdir()), [destination])

    def test_cleanup_failure_prevents_manifest_export(self) -> None:
        main_source = """\
import os
from pathlib import Path

manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"])
if not manifest.exists():
    manifest.write_text("generated\\n", encoding="utf-8")
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"
            external_manifest = Path(tmp) / "upstream-refs.json"

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(external_manifest)},
            ), patch.object(
                replay.shutil,
                "rmtree",
                side_effect=OSError("injected cleanup failure"),
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertFalse(external_manifest.exists())

    def test_success_replays_current_worktree_with_filters_and_removes_sandbox(self) -> None:
        main_source = """\
import os
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
checks = [
    os.environ.get("TRANSLATION_PROVIDER") == "identity",
    os.environ.get("TRANSLATION_REPLAY") == "1",
    "OPENAI_API_KEY" not in os.environ,
    "GH_TOKEN" not in os.environ,
    "SSH_AUTH_SOCK" not in os.environ,
    "PWD" not in os.environ,
    sys.argv[1:] == ["--version", "13.x", "--doc", "collections.md"],
    (root / "tracked.txt").read_text(encoding="utf-8") == "modified\\n",
    not (root / "deleted.txt").exists(),
    (root / "untracked.txt").read_text(encoding="utf-8") == "new\\n",
    subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout == "",
]
raise SystemExit(0 if all(checks) else 9)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            (root / "tracked.txt").write_text("modified\n", encoding="utf-8")
            (root / "deleted.txt").unlink()
            (root / "untracked.txt").write_text("new\n", encoding="utf-8")
            before = replay._worktree_fingerprint(root)  # noqa: SLF001
            sandboxes = Path(tmp) / "sandboxes"

            with patch.dict(
                os.environ,
                {
                    "OPENAI_API_KEY": "must-not-leak",
                    "GH_TOKEN": "must-not-leak",
                    "SSH_AUTH_SOCK": "/must/not/leak",
                },
            ):
                result = replay.run_replay(
                    repo_root=root,
                    version="13.x",
                    doc="collections.md",
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_OK)
            self.assertEqual(list(sandboxes.iterdir()), [])
            self.assertEqual(replay._worktree_fingerprint(root), before)  # noqa: SLF001

    def test_failed_sync_preserves_sandbox(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(9)\n")
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            preserved = list(sandboxes.iterdir())
            self.assertEqual(len(preserved), 1)
            self.assertEqual(
                _git(preserved[0], "status", "--porcelain").stdout,
                "",
            )

    def test_active_worktree_status_change_is_reported_and_preserves_sandbox(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            (root / "tracked.txt").write_text("dirty before replay\n", encoding="utf-8")
            sandboxes = Path(tmp) / "sandboxes"

            def modify_active_worktree(
                _sandbox: Path, *, version: str | None, doc: str | None
            ) -> int:
                self.assertIsNone(version)
                self.assertIsNone(doc)
                (root / "tracked.txt").write_text("changed during replay\n", encoding="utf-8")
                return 0

            with patch.object(
                replay, "_execute_sync", side_effect=modify_active_worktree
            ) as execute_sync:
                result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_WORKTREE_CHANGED)
            self.assertEqual(len(list(sandboxes.iterdir())), 1)
            execute_sync.assert_called_once()

    def test_active_index_content_change_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            (root / "tracked.txt").write_text("staged before\n", encoding="utf-8")
            _git(root, "add", "tracked.txt")
            (root / "tracked.txt").write_text("worktree\n", encoding="utf-8")
            sandboxes = Path(tmp) / "sandboxes"

            def modify_active_index(
                _sandbox: Path, *, version: str | None, doc: str | None
            ) -> int:
                self.assertIsNone(version)
                self.assertIsNone(doc)
                (root / "tracked.txt").write_text("staged after\n", encoding="utf-8")
                _git(root, "add", "tracked.txt")
                (root / "tracked.txt").write_text("worktree\n", encoding="utf-8")
                return 0

            with patch.object(
                replay, "_execute_sync", side_effect=modify_active_index
            ):
                result = replay.run_replay(
                    repo_root=root, sandbox_parent=sandboxes
                )

            self.assertEqual(result, replay.EXIT_WORKTREE_CHANGED)
            self.assertEqual(len(list(sandboxes.iterdir())), 1)

    def test_active_clean_commit_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"

            def commit_active_worktree(
                _sandbox: Path, *, version: str | None, doc: str | None
            ) -> int:
                self.assertIsNone(version)
                self.assertIsNone(doc)
                (root / "tracked.txt").write_text(
                    "committed during replay\n", encoding="utf-8"
                )
                _git(root, "add", "tracked.txt")
                _git(root, "commit", "--quiet", "-m", "concurrent commit")
                return 0

            with patch.object(
                replay, "_execute_sync", side_effect=commit_active_worktree
            ):
                result = replay.run_replay(
                    repo_root=root, sandbox_parent=sandboxes
                )

            self.assertEqual(result, replay.EXIT_WORKTREE_CHANGED)
            self.assertEqual(len(list(sandboxes.iterdir())), 1)

    def test_interrupt_while_verifying_active_worktree_is_reported_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"

            with patch.object(
                replay,
                "_execute_sync",
                return_value=0,
            ), patch.object(
                replay,
                "_worktree_fingerprint",
                side_effect=[b"before", KeyboardInterrupt],
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertEqual(len(list(sandboxes.iterdir())), 1)

    def test_git_environment_ignores_global_and_system_config(self) -> None:
        env = replay._git_environment()  # noqa: SLF001

        self.assertEqual(env["GIT_CONFIG_GLOBAL"], os.devnull)
        self.assertEqual(env["GIT_CONFIG_SYSTEM"], os.devnull)
        self.assertEqual(env["XDG_CONFIG_HOME"], env["HOME"])

    def test_git_environment_does_not_reuse_predictable_home_ignore_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            hidden = root / "untracked.secret"
            hidden.write_text("must be replayed\n", encoding="utf-8")
            predictable_home = Path(tmp) / "translation-replay-git-home"
            ignore = predictable_home / ".config/git/ignore"
            ignore.parent.mkdir(parents=True)
            ignore.write_text("*.secret\n", encoding="utf-8")

            with patch.object(replay.tempfile, "gettempdir", return_value=tmp):
                output = replay._git(  # noqa: SLF001
                    root,
                    "ls-files",
                    "--others",
                    "--exclude-standard",
                    "-z",
                ).stdout

            self.assertIn(b"untracked.secret\0", output)

    def test_untracked_file_mode_is_part_of_worktree_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            script = root / "script.sh"
            script.write_text("#!/bin/sh\n", encoding="utf-8")
            script.chmod(0o644)
            before = replay._worktree_fingerprint(root)  # noqa: SLF001

            script.chmod(0o755)

            self.assertNotEqual(
                replay._worktree_fingerprint(root),  # noqa: SLF001
                before,
            )

    def test_tmpdir_inside_active_repository_is_rejected_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandbox_parent = root / "tmp"
            sandbox_parent.mkdir()

            with patch.object(
                replay.tempfile,
                "gettempdir",
                return_value=str(sandbox_parent),
            ):
                result = replay.run_replay(repo_root=root)

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertEqual(list(sandbox_parent.iterdir()), [])
            self.assertEqual(_git(root, "status", "--porcelain").stdout, "")

    def test_tmpdir_inside_repository_is_rejected_with_explicit_sandbox_parent(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            temp_parent = root / "tmp"
            temp_parent.mkdir()
            sandbox_parent = Path(tmp) / "sandboxes"

            with patch.object(
                replay.tempfile,
                "gettempdir",
                return_value=str(temp_parent),
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandbox_parent,
                )

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertEqual(list(temp_parent.iterdir()), [])
            self.assertFalse(sandbox_parent.exists())

    def test_untracked_symlink_is_rejected_without_following_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            external = Path(tmp) / "external.txt"
            external.write_text("outside\n", encoding="utf-8")
            (root / "external-link").symlink_to(external)
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertEqual(external.read_text(encoding="utf-8"), "outside\n")
            self.assertEqual(len(list(sandboxes.iterdir())), 1)

    def test_tracked_symlink_is_rejected_without_following_it(self) -> None:
        main_source = """\
from pathlib import Path

root = Path(__file__).resolve().parent.parent
(root / "tracked.txt").write_text("changed\\n", encoding="utf-8")
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            external = Path(tmp) / "external.txt"
            external.write_text("outside\n", encoding="utf-8")
            (root / "tracked.txt").unlink()
            (root / "tracked.txt").symlink_to(external)
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertEqual(external.read_text(encoding="utf-8"), "outside\n")
            self.assertFalse(sandboxes.exists())

    def test_unchanged_tracked_symlink_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            (root / "target.txt").write_text("inside\n", encoding="utf-8")
            (root / "tracked-link").symlink_to("target.txt")
            _git(root, "add", "target.txt", "tracked-link")
            _git(root, "commit", "--quiet", "-m", "add tracked link")
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_OK)
            self.assertEqual(list(sandboxes.iterdir()), [])

    def test_unchanged_external_tracked_symlink_is_rejected(self) -> None:
        main_source = """\
from pathlib import Path

root = Path(__file__).resolve().parent.parent
(root / "external-link").write_text("escaped\\n", encoding="utf-8")
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            external = Path(tmp) / "external.txt"
            external.write_text("outside\n", encoding="utf-8")
            (root / "external-link").symlink_to(external)
            _git(root, "add", "external-link")
            _git(root, "commit", "--quiet", "-m", "add external link")
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertEqual(external.read_text(encoding="utf-8"), "outside\n")
            self.assertFalse(sandboxes.exists())

    def test_tracked_symlink_cannot_leave_and_reenter_repository(self) -> None:
        main_source = """\
from pathlib import Path

root = Path(__file__).resolve().parent.parent
(root / "external-hop").write_text("escaped\\n", encoding="utf-8")
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            target = root / "target.txt"
            target.write_text("inside\n", encoding="utf-8")
            outside = Path(tmp) / "outside"
            outside.mkdir()
            (outside / "back-inside").symlink_to(target)
            (root / "external-hop").symlink_to("../outside/back-inside")
            _git(root, "add", "target.txt", "external-hop")
            _git(root, "commit", "--quiet", "-m", "add external hop")
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertEqual(target.read_text(encoding="utf-8"), "inside\n")
            self.assertFalse(sandboxes.exists())

    def test_second_sync_must_leave_first_sync_result_unchanged(self) -> None:
        main_source = """\
from pathlib import Path

root = Path(__file__).resolve().parent.parent
marker = root / ".git/replay-pass"
(root / "tracked.txt").write_text(
    "first\\n" if not marker.exists() else "second\\n",
    encoding="utf-8",
)
marker.write_text("ran\\n", encoding="utf-8")
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertEqual(len(list(sandboxes.iterdir())), 1)

    def test_sandbox_is_removed_when_setup_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"

            with patch.object(
                replay,
                "_command",
                side_effect=replay.ReplayError("fixture failure"),
            ):
                with self.assertRaises(replay.ReplayError):
                    replay._create_sandbox(root, sandboxes)  # noqa: SLF001

            self.assertFalse(sandboxes.exists())

    def test_sandbox_is_removed_when_setup_is_interrupted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"

            with patch.object(
                replay,
                "_command",
                side_effect=KeyboardInterrupt,
            ):
                with self.assertRaises(KeyboardInterrupt):
                    replay._create_sandbox(root, sandboxes)  # noqa: SLF001

            self.assertFalse(sandboxes.exists())


class TranslationWorkflowTests(unittest.TestCase):
    def test_missing_manifest_preserves_nonzero_preflight_status(self) -> None:
        script = _workflow_run_script("Run translation preflight")
        harness = 'make() { return "$PREFLIGHT_STATUS"; }\n' + script

        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "missing.json"
            for status in (2, 3):
                with self.subTest(status=status):
                    env = os.environ.copy()
                    env.update(
                        {
                            "MANIFEST": str(manifest),
                            "PREFLIGHT_STATUS": str(status),
                        }
                    )
                    result = subprocess.run(
                        ["bash", "-e", "-c", harness],
                        env=env,
                        capture_output=True,
                        text=True,
                        check=False,
                    )

                    self.assertEqual(result.returncode, status)


if __name__ == "__main__":
    unittest.main()
