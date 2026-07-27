import io
import json
import os
import subprocess
from contextlib import redirect_stderr
from concurrent.futures import ThreadPoolExecutor
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from sync import upstream


class UpstreamSyncTests(unittest.TestCase):
    def _assert_versions_rejected_before_clone(
        self,
        contents: str,
        message: str,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "versions.json").write_text(contents, encoding="utf-8")
            stderr = io.StringIO()

            with redirect_stderr(stderr), patch.dict(
                os.environ, {}, clear=True
            ), patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "_clone_upstream"
            ) as clone, patch.object(
                upstream, "sync_version", return_value=1
            ), patch.object(
                upstream, "_output", return_value="a" * 40
            ):
                result = upstream.main()

            self.assertEqual(result, 1)
            clone.assert_not_called()
            self.assertEqual(stderr.getvalue().count("\n"), 1)
            self.assertIn(message, stderr.getvalue())

    def test_main_rejects_empty_versions_before_clone(self) -> None:
        self._assert_versions_rejected_before_clone(
            "[]\n",
            "versions.json must not be empty",
        )

    def test_main_reports_invalid_versions_json_without_traceback(self) -> None:
        self._assert_versions_rejected_before_clone("[\n", "versions.json error:")

    def test_main_rejects_non_list_versions_before_clone(self) -> None:
        self._assert_versions_rejected_before_clone(
            "{}\n",
            "must contain a list",
        )

    def test_main_rejects_invalid_version_tokens_before_clone(self) -> None:
        for token in (13, "13", "../13.x"):
            with self.subTest(token=token):
                self._assert_versions_rejected_before_clone(
                    json.dumps(["master", token]),
                    "invalid version",
                )

    def test_main_requires_master_as_the_first_version_before_clone(self) -> None:
        for versions in (["13.x", "12.x"], ["13.x", "master"]):
            with self.subTest(versions=versions):
                self._assert_versions_rejected_before_clone(
                    json.dumps(versions),
                    "master once",
                )

    def test_main_rejects_duplicate_versions_before_clone(self) -> None:
        for versions in (
            ["master", "master", "13.x"],
            ["master", "13.x", "13.x"],
        ):
            with self.subTest(versions=versions):
                self._assert_versions_rejected_before_clone(
                    json.dumps(versions),
                    "unique",
                )

    def test_main_rejects_misordered_stable_versions_before_clone(self) -> None:
        self._assert_versions_rejected_before_clone(
            json.dumps(["master", "12.x", "13.x"]),
            "descending order",
        )

    def test_sync_version_copies_markdown_bytes_without_normalization(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            source = repo_dir / "example.md"
            raw = (
                b"# Title  \n"
                b"\n"
                b"> [!NOTE]  \n"
                b"Text with internal  spaces.   \n"
                b"```php\n"
                b"$value = 'kept';   \n"
                b"```"
            )
            source.write_bytes(raw)

            en_root = root / "i18n/en/docusaurus-plugin-content-docs"
            with patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(
                upstream, "_run"
            ):
                count = upstream.sync_version(repo_dir, "13.x")

            self.assertEqual(count, 1)
            self.assertEqual((en_root / "version-13.x/example.md").read_bytes(), raw)

    def test_sync_version_rejects_upstream_markdown_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            outside = root / "outside.md"
            outside.write_text("host data\n", encoding="utf-8")
            (repo_dir / "linked.md").symlink_to(outside)

            en_root = root / "i18n/en/docusaurus-plugin-content-docs"
            with patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(
                upstream, "_run"
            ):
                with self.assertRaisesRegex(
                    ValueError, "upstream Markdown symlink"
                ):
                    upstream.sync_version(repo_dir, "13.x")

            self.assertFalse((en_root / "version-13.x/linked.md").exists())

    def test_sync_version_can_checkout_a_pinned_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_dir = Path(tmp)
            en_root = repo_dir / "en"
            with patch.object(
                upstream, "REPO_ROOT", repo_dir
            ), patch.object(upstream, "EN_ROOT", en_root), patch.object(
                upstream, "_run"
            ) as run:
                upstream.sync_version(repo_dir, "13.x", ref="a" * 40)

            self.assertEqual(
                run.call_args_list[0].args[0],
                ["git", "checkout", "--force", "a" * 40],
            )

    def test_sync_version_updates_only_the_selected_document(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            (repo_dir / "selected.md").write_text("new\n", encoding="utf-8")
            (repo_dir / "other.md").write_text("upstream\n", encoding="utf-8")

            en_root = root / "en"
            destination = en_root / "version-13.x"
            destination.mkdir(parents=True)
            (destination / "selected.md").write_text("old\n", encoding="utf-8")
            (destination / "other.md").write_text("cached\n", encoding="utf-8")

            with patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(
                upstream, "_run"
            ):
                count = upstream.sync_version(
                    repo_dir, "13.x", doc="selected.md"
                )

            self.assertEqual(count, 1)
            self.assertEqual(
                (destination / "selected.md").read_text(encoding="utf-8"),
                "new\n",
            )
            self.assertEqual(
                (destination / "other.md").read_text(encoding="utf-8"),
                "cached\n",
            )

    def test_sync_version_preserves_selected_cache_when_replace_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            (repo_dir / "selected.md").write_text("new\n", encoding="utf-8")

            en_root = root / "en"
            destination = en_root / "version-13.x"
            destination.mkdir(parents=True)
            cached = destination / "selected.md"
            cached.write_text("cached\n", encoding="utf-8")

            with patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(upstream, "_run"), patch.object(
                upstream.os,
                "replace",
                side_effect=OSError("replace failed"),
            ):
                with self.assertRaisesRegex(OSError, "replace failed"):
                    upstream.sync_version(
                        repo_dir,
                        "13.x",
                        doc="selected.md",
                    )

            self.assertEqual(cached.read_text(encoding="utf-8"), "cached\n")
            self.assertEqual(list(destination.glob(".selected.md.*.tmp")), [])

    def test_sync_version_replaces_selected_hardlink_and_preserves_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            (repo_dir / "selected.md").write_bytes(b"new\r\n")

            en_root = root / "en"
            destination = en_root / "version-13.x"
            destination.mkdir(parents=True)
            victim = root / "victim.md"
            victim.write_bytes(b"cached\n")
            victim.chmod(0o640)
            cached = destination / "selected.md"
            cached.hardlink_to(victim)

            with patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(upstream, "_run"):
                upstream.sync_version(
                    repo_dir,
                    "13.x",
                    doc="selected.md",
                )

            self.assertEqual(cached.read_bytes(), b"new\r\n")
            self.assertEqual(victim.read_bytes(), b"cached\n")
            self.assertEqual(cached.stat().st_mode & 0o777, 0o640)

    def test_full_sync_preserves_cache_when_first_replace_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            (repo_dir / "selected.md").write_text("new\n", encoding="utf-8")

            en_root = root / "en"
            destination = en_root / "version-13.x"
            destination.mkdir(parents=True)
            selected = destination / "selected.md"
            selected.write_text("cached\n", encoding="utf-8")
            stale = destination / "stale.md"
            stale.write_text("stale\n", encoding="utf-8")

            with patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(upstream, "_run"), patch.object(
                upstream.os,
                "replace",
                side_effect=OSError("replace failed"),
            ):
                with self.assertRaisesRegex(OSError, "replace failed"):
                    upstream.sync_version(repo_dir, "13.x")

            self.assertEqual(selected.read_text(encoding="utf-8"), "cached\n")
            self.assertEqual(stale.read_text(encoding="utf-8"), "stale\n")
            self.assertEqual(list(destination.glob(".selected.md.*.tmp")), [])

    def test_full_sync_preserves_existing_file_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            (repo_dir / "selected.md").write_text("new\n", encoding="utf-8")

            en_root = root / "en"
            destination = en_root / "version-13.x"
            destination.mkdir(parents=True)
            selected = destination / "selected.md"
            selected.write_text("cached\n", encoding="utf-8")
            selected.chmod(0o640)

            with patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(upstream, "_run"):
                upstream.sync_version(repo_dir, "13.x")

            self.assertEqual(selected.read_text(encoding="utf-8"), "new\n")
            self.assertEqual(selected.stat().st_mode & 0o777, 0o640)

    def test_sync_version_rejects_selected_upstream_markdown_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            outside = root / "outside.md"
            outside.write_text("host data\n", encoding="utf-8")
            (repo_dir / "selected.md").symlink_to(outside)

            en_root = root / "en"
            destination = en_root / "version-13.x"
            destination.mkdir(parents=True)
            cached = destination / "selected.md"
            cached.write_text("cached\n", encoding="utf-8")

            with patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(
                upstream, "_run"
            ):
                with self.assertRaisesRegex(
                    ValueError, "upstream Markdown symlink"
                ):
                    upstream.sync_version(
                        repo_dir,
                        "13.x",
                        doc="selected.md",
                    )

            self.assertEqual(cached.read_text(encoding="utf-8"), "cached\n")

    def test_sync_version_deletes_only_a_selected_document_missing_upstream(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            en_root = root / "en"
            destination = en_root / "version-13.x"
            destination.mkdir(parents=True)
            (destination / "removed.md").write_text("stale\n", encoding="utf-8")
            (destination / "other.md").write_text("cached\n", encoding="utf-8")

            with patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(
                upstream, "_run"
            ):
                count = upstream.sync_version(
                    repo_dir, "13.x", doc="removed.md"
                )

            self.assertEqual(count, 0)
            self.assertFalse((destination / "removed.md").exists())
            self.assertEqual(
                (destination / "other.md").read_text(encoding="utf-8"),
                "cached\n",
            )

    def test_manifest_round_trip_records_repository_and_version_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "refs.json"
            refs = {"13.x": "a" * 40, "12.x": "b" * 40}

            upstream.write_manifest(path, refs)

            self.assertEqual(upstream.load_manifest(path), refs)
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["repository"], upstream.UPSTREAM_REPO)

    def test_write_manifest_does_not_follow_predictable_temp_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "refs.json"
            victim = root / "victim.json"
            victim.write_text("keep\n", encoding="utf-8")
            predictable_temp = root / ".refs.json.tmp"
            predictable_temp.symlink_to(victim)

            upstream.write_manifest(path, {"13.x": "a" * 40})

            self.assertEqual(victim.read_text(encoding="utf-8"), "keep\n")
            self.assertTrue(predictable_temp.is_symlink())
            self.assertFalse(path.is_symlink())
            self.assertEqual(
                upstream.load_manifest(path),
                {"13.x": "a" * 40},
            )

    def test_write_manifest_supports_concurrent_writers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "refs.json"
            refs = [
                {"13.x": format(index, "x") * 40}
                for index in range(8)
            ]
            barrier = threading.Barrier(len(refs))

            def write(candidate: dict[str, str]) -> None:
                barrier.wait()
                upstream.write_manifest(path, candidate)

            with ThreadPoolExecutor(max_workers=len(refs)) as executor:
                futures = [executor.submit(write, candidate) for candidate in refs]
                for future in futures:
                    future.result()

            self.assertIn(upstream.load_manifest(path), refs)
            self.assertEqual(list(root.glob(".refs.json.*.tmp")), [])

    def test_write_manifest_cleans_up_only_its_temp_after_replace_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "refs.json"
            preexisting = root / ".refs.json.tmp"
            preexisting.write_text("keep\n", encoding="utf-8")

            with patch.object(
                upstream.os,
                "replace",
                side_effect=OSError("replace failed"),
            ):
                with self.assertRaisesRegex(OSError, "replace failed"):
                    upstream.write_manifest(path, {"13.x": "a" * 40})

            self.assertEqual(preexisting.read_text(encoding="utf-8"), "keep\n")
            self.assertEqual(list(root.glob(".refs.json.*.tmp")), [])

    def test_manifest_rejects_missing_version_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "refs.json"
            upstream.write_manifest(path, {"12.x": "b" * 40})

            with self.assertRaisesRegex(ValueError, "missing ref for version-13.x"):
                upstream.manifest_ref({"12.x": "b" * 40}, "13.x")

    def test_main_writes_branch_ref_then_reuses_pinned_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "refs.json"
            commit = "a" * 40
            with patch.dict(
                os.environ, {upstream.MANIFEST_ENV: str(path)}
            ), patch.object(
                upstream, "supported_versions", return_value=["13.x"]
            ), patch.object(
                upstream, "_run"
            ), patch.object(
                upstream, "_output", return_value=commit
            ), patch.object(
                upstream, "sync_version", return_value=1
            ) as sync_version:
                self.assertEqual(upstream.main(), 0)
                self.assertEqual(
                    sync_version.call_args.kwargs["ref"], "13.x"
                )

                sync_version.reset_mock()
                self.assertEqual(upstream.main(), 0)

            self.assertEqual(sync_version.call_args.kwargs["ref"], commit)

    def test_main_scopes_checkout_and_copy_to_requested_filters(self) -> None:
        with patch.dict(os.environ, {}, clear=True), patch.object(
            upstream, "supported_versions", return_value=["12.x", "13.x"]
        ), patch.object(upstream, "_run"), patch.object(
            upstream, "_output", return_value="a" * 40
        ), patch.object(
            upstream, "sync_version", return_value=1
        ) as sync_version:
            result = upstream.main(version="13.x", doc="collections.md")

        self.assertEqual(result, 0)
        sync_version.assert_called_once()
        self.assertEqual(sync_version.call_args.args[1], "13.x")
        self.assertEqual(sync_version.call_args.kwargs["doc"], "collections.md")

    def test_main_rejects_manifest_missing_a_supported_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "refs.json"
            upstream.write_manifest(path, {"12.x": "b" * 40})
            with patch.dict(
                os.environ, {upstream.MANIFEST_ENV: str(path)}
            ), patch.object(
                upstream, "supported_versions", return_value=["13.x"]
            ), patch.object(
                upstream, "_run"
            ), patch.object(
                upstream, "sync_version"
            ) as sync_version:
                result = upstream.main()

            self.assertEqual(result, 1)
            sync_version.assert_not_called()

    def test_main_reports_manifest_write_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "refs.json"
            with patch.dict(
                os.environ, {upstream.MANIFEST_ENV: str(path)}
            ), patch.object(
                upstream, "supported_versions", return_value=[]
            ), patch.object(
                upstream, "_run"
            ), patch.object(
                upstream, "write_manifest", side_effect=OSError("read-only")
            ):
                result = upstream.main()

            self.assertEqual(result, 1)

    def test_sync_version_rejects_unsafe_version_before_checkout_or_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            en_root = root / "en"

            with patch.object(upstream, "EN_ROOT", en_root), patch.object(
                upstream, "_run"
            ) as run:
                with self.assertRaisesRegex(ValueError, "invalid version"):
                    upstream.sync_version(repo_dir, "x/../../escaped")

            run.assert_not_called()
            self.assertFalse((root / "escaped").exists())

    def test_sync_version_rejects_leading_zero_version_before_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            en_root = root / "en"

            with patch.object(
                upstream, "REPO_ROOT", root
            ), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(upstream, "_run") as run:
                with self.assertRaisesRegex(ValueError, "invalid version"):
                    upstream.sync_version(repo_dir, "013.x")

            run.assert_not_called()
            self.assertFalse((en_root / "version-013.x").exists())

    def test_sync_version_rejects_destination_symlink_to_another_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            (repo_dir / "new.md").write_text("new\n", encoding="utf-8")

            en_root = root / "en"
            other_version = en_root / "version-12.x"
            other_version.mkdir(parents=True)
            victim = other_version / "victim.md"
            victim.write_text("keep\n", encoding="utf-8")
            (en_root / "version-13.x").symlink_to(other_version)

            with patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(
                upstream, "_run"
            ) as run:
                with self.assertRaisesRegex(
                    ValueError, "invalid version destination"
                ):
                    upstream.sync_version(repo_dir, "13.x")

            run.assert_not_called()
            self.assertEqual(victim.read_text(encoding="utf-8"), "keep\n")
            self.assertFalse((other_version / "new.md").exists())

    def test_sync_version_rejects_symlinked_english_root_before_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_root = root / "repo"
            repo_root.mkdir()
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            (repo_dir / "new.md").write_text("new\n", encoding="utf-8")

            outside = root / "outside"
            outside.mkdir()
            en_root = (
                repo_root
                / "i18n/en/docusaurus-plugin-content-docs"
            )
            en_root.parent.mkdir(parents=True)
            en_root.symlink_to(outside, target_is_directory=True)

            with patch.object(
                upstream, "REPO_ROOT", repo_root
            ), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(upstream, "_run") as run:
                with self.assertRaisesRegex(
                    ValueError, "invalid version destination"
                ):
                    upstream.sync_version(repo_dir, "13.x")

            run.assert_not_called()
            self.assertEqual(list(outside.iterdir()), [])

    def test_sync_version_rejects_symlinked_english_root_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_root = root / "repo"
            repo_root.mkdir()
            repo_dir = root / "upstream"
            repo_dir.mkdir()

            outside = root / "outside"
            outside.mkdir()
            (repo_root / "i18n").symlink_to(
                outside,
                target_is_directory=True,
            )
            en_root = (
                repo_root
                / "i18n/en/docusaurus-plugin-content-docs"
            )

            with patch.object(
                upstream, "REPO_ROOT", repo_root
            ), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(upstream, "_run") as run:
                with self.assertRaisesRegex(
                    ValueError, "invalid version destination"
                ):
                    upstream.sync_version(repo_dir, "13.x")

            run.assert_not_called()
            self.assertEqual(list(outside.iterdir()), [])

    def test_sync_version_rejects_symlinked_destination_leaf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_root = root / "repo"
            repo_root.mkdir()
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            (repo_dir / "selected.md").write_text("new\n", encoding="utf-8")

            en_root = (
                repo_root
                / "i18n/en/docusaurus-plugin-content-docs"
            )
            destination = en_root / "version-13.x"
            destination.mkdir(parents=True)
            victim = root / "victim.md"
            victim.write_text("keep\n", encoding="utf-8")
            target = destination / "selected.md"
            target.symlink_to(victim)

            with patch.object(
                upstream, "REPO_ROOT", repo_root
            ), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(upstream, "_run") as run:
                with self.assertRaisesRegex(
                    ValueError, "invalid document destination"
                ):
                    upstream.sync_version(
                        repo_dir,
                        "13.x",
                        doc="selected.md",
                    )

            run.assert_not_called()
            self.assertTrue(target.is_symlink())
            self.assertEqual(victim.read_text(encoding="utf-8"), "keep\n")

    def test_sync_version_rechecks_leaf_after_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_root = root / "repo"
            repo_root.mkdir()
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            (repo_dir / "selected.md").write_text("new\n", encoding="utf-8")

            en_root = (
                repo_root
                / "i18n/en/docusaurus-plugin-content-docs"
            )
            destination = en_root / "version-13.x"
            destination.mkdir(parents=True)
            victim = root / "victim.md"
            victim.write_text("keep\n", encoding="utf-8")
            target = destination / "selected.md"

            def checkout(*_args: object, **_kwargs: object) -> None:
                target.symlink_to(victim)

            with patch.object(
                upstream, "REPO_ROOT", repo_root
            ), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(
                upstream, "_run", side_effect=checkout
            ):
                with self.assertRaisesRegex(
                    ValueError, "invalid document destination"
                ):
                    upstream.sync_version(
                        repo_dir,
                        "13.x",
                        doc="selected.md",
                    )

            self.assertTrue(target.is_symlink())
            self.assertEqual(victim.read_text(encoding="utf-8"), "keep\n")

    def test_sync_version_rejects_unsafe_document_before_checkout_or_unlink(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            en_root = root / "en"
            victim = root / "victim.md"
            victim.write_text("keep\n", encoding="utf-8")

            with patch.object(upstream, "EN_ROOT", en_root), patch.object(
                upstream, "_run"
            ) as run:
                with self.assertRaisesRegex(ValueError, "invalid document"):
                    upstream.sync_version(
                        repo_dir,
                        "13.x",
                        doc="../../victim.md",
                    )

            run.assert_not_called()
            self.assertEqual(victim.read_text(encoding="utf-8"), "keep\n")

    def test_main_reports_clone_failure_without_traceback(self) -> None:
        stderr = io.StringIO()
        error = subprocess.CalledProcessError(128, ["git", "clone"])

        with redirect_stderr(stderr), patch.dict(
            os.environ, {}, clear=True
        ), patch.object(
            upstream, "supported_versions", return_value=["13.x"]
        ), patch.object(upstream, "_run", side_effect=error):
            result = upstream.main(version="13.x")

        self.assertEqual(result, 1)
        self.assertEqual(stderr.getvalue(), "upstream clone failed\n")

    def test_main_reports_clone_timeout_without_traceback(self) -> None:
        stderr = io.StringIO()
        error = subprocess.TimeoutExpired(["git", "clone"], 300)

        with redirect_stderr(stderr), patch.dict(
            os.environ, {}, clear=True
        ), patch.object(
            upstream, "supported_versions", return_value=["13.x"]
        ), patch.object(upstream, "_run", side_effect=error):
            result = upstream.main(version="13.x")

        self.assertEqual(result, 1)
        self.assertEqual(stderr.getvalue(), "upstream clone failed\n")

    def test_main_retries_transient_clone_failures(self) -> None:
        commit = "a" * 40
        clone_error = subprocess.CalledProcessError(128, ["git", "clone"])
        with patch.dict(os.environ, {}, clear=True), patch.object(
            upstream, "supported_versions", return_value=["13.x"]
        ), patch.object(
            upstream, "_run", side_effect=[clone_error, None, None]
        ) as run, patch.object(
            upstream, "_output", return_value=commit
        ), patch.object(
            upstream, "sync_version", return_value=1
        ):
            result = upstream.main(version="13.x")

        self.assertEqual(result, 0)
        clone_calls = [
            call
            for call in run.call_args_list
            if "clone" in call.args[0]
        ]
        self.assertEqual(len(clone_calls), 2)
        self.assertTrue(
            all(
                call.kwargs["timeout"] == upstream.UPSTREAM_CLONE_TIMEOUT
                for call in clone_calls
            )
        )

    def test_main_fails_when_requested_branch_is_unavailable(self) -> None:
        error = subprocess.CalledProcessError(1, ["git", "checkout"])

        with patch.dict(os.environ, {}, clear=True), patch.object(
            upstream, "supported_versions", return_value=["13.x"]
        ), patch.object(upstream, "_run"), patch.object(
            upstream, "sync_version", side_effect=error
        ):
            result = upstream.main(version="13.x", doc="example.md")

        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
