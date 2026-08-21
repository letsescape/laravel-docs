"""upstream 동작과 경계 조건 검증."""

import hashlib
import io
import json
import os
import subprocess
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from sync import upstream


class UpstreamSyncTests(unittest.TestCase):
    """upstream 동기화 동작과 경계 조건 테스트 모음."""

    def test_git_environment_allows_network_metadata_but_not_credentials(self) -> None:
        """`_git_environment`가 허용된 실행·네트워크·로캘 변수와 Git 격리 설정만 포함하고 인증 정보를 제거하는지 검증."""

        with patch.dict(
            os.environ,
            {
                "PATH": "/usr/bin",
                "HTTPS_PROXY": "http://proxy.invalid",
                "SSL_CERT_FILE": "/certs/ca-bundle",
                "LC_TEST": "locale",
                "OPENAI_API_KEY": "secret",
                "AZURE_OPENAI_API_KEY": "secret",
                "CODEX_API_KEY": "secret",
                "GH_TOKEN": "secret",
                "SSH_AUTH_SOCK": "/secret/socket",
            },
            clear=True,
        ):
            env = upstream._git_environment()  # noqa: SLF001

        self.assertEqual(env["PATH"], "/usr/bin")
        self.assertEqual(env["HTTPS_PROXY"], "http://proxy.invalid")
        self.assertEqual(env["SSL_CERT_FILE"], "/certs/ca-bundle")
        self.assertEqual(env["LC_TEST"], "locale")
        self.assertEqual(env["GIT_TERMINAL_PROMPT"], "0")
        self.assertEqual(env["GIT_CONFIG_GLOBAL"], os.devnull)
        for secret in (
            "OPENAI_API_KEY",
            "AZURE_OPENAI_API_KEY",
            "CODEX_API_KEY",
            "GH_TOKEN",
            "SSH_AUTH_SOCK",
        ):
            self.assertNotIn(secret, env)

    def test_git_subprocesses_receive_only_the_sanitized_environment(self) -> None:
        """Git 하위 프로세스에 정제된 환경만 전달하는지 검증."""

        with patch.object(upstream, "_PROCESS_RUNNER") as run:
            upstream._run(["git", "status"])  # noqa: SLF001
            upstream._output(["git", "rev-parse", "HEAD"], Path("."))  # noqa: SLF001

        self.assertEqual(len(run.call_args_list), 2)
        for call in run.call_args_list:
            self.assertEqual(call.kwargs["env"], upstream._git_environment())  # noqa: SLF001

    def _assert_versions_rejected_before_source_setup(
        self,
        contents: str,
        message: str,
    ) -> None:
        """원문 준비 전 버전 거부를 검증하는 도우미."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "versions.json").write_text(contents, encoding="utf-8")
            stderr = io.StringIO()

            with redirect_stderr(stderr), patch.dict(
                os.environ, {}, clear=True
            ), patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "_prepare_upstream"
            ) as prepare, patch.object(
                upstream, "sync_version", return_value=1
            ):
                result = upstream.main()

            self.assertEqual(result, 1)
            prepare.assert_not_called()
            self.assertEqual(stderr.getvalue().count("\n"), 1)
            self.assertIn(message, stderr.getvalue())

    def test_main_rejects_empty_versions_before_source_setup(self) -> None:
        """`main`이 원문 준비 전에 빈 버전 목록을 거부하는지 검증."""

        self._assert_versions_rejected_before_source_setup(
            "[]\n",
            "versions.json must not be empty",
        )

    def test_main_reports_invalid_versions_json_without_traceback(self) -> None:
        """`main`이 잘못된 버전 JSON을 추적 정보 없이 보고하는지 검증."""

        self._assert_versions_rejected_before_source_setup(
            "[\n",
            "versions.json error:",
        )

    def test_main_rejects_non_list_versions_before_source_setup(self) -> None:
        """`main`이 원문 준비 전에 목록이 아닌 버전 값을 거부하는지 검증."""

        self._assert_versions_rejected_before_source_setup(
            "{}\n",
            "must contain a list",
        )

    def test_main_rejects_invalid_version_tokens_before_source_setup(self) -> None:
        """`main`이 원문 준비 전에 잘못된 버전 토큰을 거부하는지 검증."""

        for token in (13, "13", "../13.x"):
            with self.subTest(token=token):
                self._assert_versions_rejected_before_source_setup(
                    json.dumps(["master", token]),
                    "invalid version",
                )

    def test_main_requires_master_first_before_source_setup(self) -> None:
        """`main`이 원문 준비 전에 master를 첫 번째 항목으로 요구하는지 검증."""

        for versions in (["13.x", "12.x"], ["13.x", "master"]):
            with self.subTest(versions=versions):
                self._assert_versions_rejected_before_source_setup(
                    json.dumps(versions),
                    "master once",
                )

    def test_main_rejects_duplicate_versions_before_source_setup(self) -> None:
        """`main`이 원문 준비 전에 중복 버전을 거부하는지 검증."""

        for versions in (
            ["master", "master", "13.x"],
            ["master", "13.x", "13.x"],
        ):
            with self.subTest(versions=versions):
                self._assert_versions_rejected_before_source_setup(
                    json.dumps(versions),
                    "unique",
                )

    def test_main_rejects_misordered_versions_before_source_setup(self) -> None:
        """`main`이 원문 준비 전에 순서가 잘못된 버전을 거부하는지 검증."""

        self._assert_versions_rejected_before_source_setup(
            json.dumps(["master", "12.x", "13.x"]),
            "descending order",
        )

    def test_sync_version_copies_markdown_bytes_without_normalization(self) -> None:
        """`sync_version`이 Markdown 바이트를 정규화 없이 복사하는지 검증."""

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
        """`sync_version`이 upstream Markdown symlink를 거부하는지 검증."""

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
        """`sync_version`이 고정 commit의 checkout 명령을 사용하는지 검증."""

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

    def test_sync_version_caps_checkout_to_shared_workflow_deadline(self) -> None:
        """`sync_version`이 공유 워크플로 기한으로 checkout 시간을 제한하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            repo_dir = Path(tmp)
            en_root = repo_dir / "en"
            with patch.object(
                upstream, "REPO_ROOT", repo_dir
            ), patch.object(upstream, "EN_ROOT", en_root), patch.object(
                upstream.time,
                "monotonic",
                return_value=100,
            ), patch.object(
                upstream, "_run"
            ) as run:
                upstream.sync_version(
                    repo_dir,
                    "13.x",
                    ref="a" * 40,
                    deadline=130,
                )

            self.assertEqual(run.call_args.kwargs["timeout"], 30)

    def test_sync_version_updates_only_the_selected_document(self) -> None:
        """`sync_version`이 선택한 문서만 갱신하는지 검증."""

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

    def test_sync_version_updates_a_nested_selected_document(self) -> None:
        """`sync_version`이 중첩 경로의 선택 문서를 갱신하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            source = repo_dir / "guides/queues.md"
            source.parent.mkdir(parents=True)
            source.write_text("new\n", encoding="utf-8")
            en_root = root / "en"

            with patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(upstream, "_run"):
                count = upstream.sync_version(
                    repo_dir,
                    "13.x",
                    doc="guides/queues.md",
                )

            self.assertEqual(count, 1)
            self.assertEqual(
                (en_root / "version-13.x/guides/queues.md").read_text(
                    encoding="utf-8"
                ),
                "new\n",
            )

    def test_full_sync_recursively_copies_and_deletes_nested_markdown(self) -> None:
        """전체 동기화가 중첩 Markdown을 재귀적으로 복사하고 삭제하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            (repo_dir / "guides").mkdir(parents=True)
            (repo_dir / "guides/queues.md").write_bytes(b"nested\r\n")
            (repo_dir / "root.md").write_bytes(b"root\n")

            en_root = root / "en"
            destination = en_root / "version-13.x"
            (destination / "guides").mkdir(parents=True)
            (destination / "guides/queues.md").write_text(
                "old\n", encoding="utf-8"
            )
            (destination / "obsolete/deep").mkdir(parents=True)
            (destination / "obsolete/deep/stale.md").write_text(
                "stale\n", encoding="utf-8"
            )

            with patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(upstream, "_run"):
                count = upstream.sync_version(repo_dir, "13.x")

            self.assertEqual(count, 2)
            self.assertEqual(
                (destination / "guides/queues.md").read_bytes(),
                b"nested\r\n",
            )
            self.assertEqual((destination / "root.md").read_bytes(), b"root\n")
            self.assertFalse((destination / "obsolete").exists())

    def test_full_sync_rejects_nested_upstream_symlink_directory(self) -> None:
        """전체 동기화가 중첩 upstream symlink 디렉터리를 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            outside = root / "outside"
            outside.mkdir()
            (outside / "leak.md").write_text("secret\n", encoding="utf-8")
            (repo_dir / "guides").symlink_to(outside, target_is_directory=True)
            en_root = root / "en"

            with patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(upstream, "_run"):
                with self.assertRaisesRegex(
                    ValueError,
                    "upstream Markdown symlink",
                ):
                    upstream.sync_version(repo_dir, "13.x")

            self.assertFalse((en_root / "version-13.x/guides/leak.md").exists())

    def test_sync_version_preserves_selected_cache_when_replace_fails(self) -> None:
        """`sync_version`이 교체 실패 시 선택 문서의 cache를 보존하고 임시 파일을 정리하는지 검증."""

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
        """`sync_version`이 선택한 hardlink를 교체하고 파일 mode를 보존하는지 검증."""

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
        """전체 동기화가 첫 교체 실패 시 cache를 보존하는지 검증."""

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
        """전체 동기화가 기존 파일 mode를 보존하는지 검증."""

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
        """`sync_version`이 선택한 upstream Markdown symlink를 거부하는지 검증."""

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
        """`sync_version`이 upstream에서 누락된 선택 문서만 삭제하는지 검증."""

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

    def test_sync_version_rejects_selected_non_file_markdown_source(self) -> None:
        """`sync_version`이 파일이 아닌 선택 Markdown 원문을 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            (repo_dir / "guides/queues.md").mkdir(parents=True)
            en_root = root / "en"
            destination = en_root / "version-13.x/guides"
            destination.mkdir(parents=True)
            cached = destination / "queues.md"
            cached.write_text("cached\n", encoding="utf-8")

            with patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(upstream, "_run"):
                with self.assertRaisesRegex(
                    ValueError,
                    "upstream Markdown path is unsafe",
                ):
                    upstream.sync_version(
                        repo_dir,
                        "13.x",
                        doc="guides/queues.md",
                    )

            self.assertEqual(cached.read_text(encoding="utf-8"), "cached\n")

    def test_full_sync_rejects_nested_destination_symlink_before_checkout(self) -> None:
        """전체 동기화가 checkout 전에 중첩 목적지 symlink를 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            (repo_dir / "root.md").write_text("source\n", encoding="utf-8")
            en_root = root / "en"
            destination = en_root / "version-13.x"
            destination.mkdir(parents=True)
            outside = root / "outside"
            outside.mkdir()
            victim = outside / "victim.md"
            victim.write_text("keep\n", encoding="utf-8")
            (destination / "guides").symlink_to(
                outside,
                target_is_directory=True,
            )

            with patch.object(upstream, "REPO_ROOT", root), patch.object(
                upstream, "EN_ROOT", en_root
            ), patch.object(upstream, "_run") as run:
                with self.assertRaisesRegex(ValueError, "symlink"):
                    upstream.sync_version(repo_dir, "13.x")

            run.assert_not_called()
            self.assertEqual(victim.read_text(encoding="utf-8"), "keep\n")

    def test_manifest_round_trip_records_repository_and_version_refs(self) -> None:
        """manifest 왕복 변환이 저장소와 버전 ref를 기록하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "refs.json"
            refs = {"master": "a" * 40, "13.x": "b" * 40}

            upstream.write_manifest(path, refs)

            contents = path.read_bytes()
            self.assertEqual(
                contents,
                (
                    '{"schema_version":1,"entries":['
                    '{"version":"master","repository":"https://github.com/laravel/docs.git",'
                    '"object_format":"sha1","commit":"' + "a" * 40 + '"},'
                    '{"version":"13.x","repository":"https://github.com/laravel/docs.git",'
                    '"object_format":"sha1","commit":"' + "b" * 40 + '"}]}'
                    "\n"
                ).encode("utf-8"),
            )
            self.assertEqual(
                upstream.load_manifest(path, expected_versions=["master", "13.x"]),
                refs,
            )
            self.assertEqual(
                upstream.manifest_digest(contents),
                hashlib.sha256(contents).hexdigest(),
            )

    def test_manifest_round_trip_supports_sha256_object_ids(self) -> None:
        """manifest 왕복 변환이 SHA-256 객체 ID를 지원하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "refs.json"
            refs = {"master": "a" * 64}

            upstream.write_manifest(path, refs)

            self.assertIn(b'"object_format":"sha256"', path.read_bytes())
            self.assertEqual(
                upstream.load_manifest(path, expected_versions=["master"]),
                refs,
            )

    def test_manifest_rejects_boolean_schema_version(self) -> None:
        """manifest가 boolean schema 버전을 거부하는지 검증."""

        contents = (
            '{"schema_version":true,"entries":[]}' "\n"
        ).encode("utf-8")

        with self.assertRaisesRegex(ValueError, "schema"):
            upstream.load_manifest_bytes(contents)

    def test_manifest_rejects_non_string_object_format_cleanly(self) -> None:
        """manifest가 문자열이 아닌 객체 형식을 명확히 거부하는지 검증."""

        contents = (
            '{"schema_version":1,"entries":['
            '{"version":"master","repository":"https://github.com/laravel/docs.git",'
            '"object_format":[],"commit":"' + "a" * 40 + '"}]}\n'
        ).encode("utf-8")

        with self.assertRaisesRegex(ValueError, "object format"):
            upstream.load_manifest_bytes(contents)

    def test_manifest_writer_rejects_non_string_commit_cleanly(self) -> None:
        """`canonical_manifest`가 문자열이 아닌 commit을 명확히 거부하는지 검증."""

        with self.assertRaisesRegex(ValueError, "object ID"):
            upstream.canonical_manifest({"master": 1})  # type: ignore[dict-item]

    def test_manifest_rejects_noncanonical_json_and_version_order(self) -> None:
        """manifest가 비정규 JSON과 잘못된 버전 순서를 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "refs.json"
            refs = {"13.x": "b" * 40, "master": "a" * 40}
            upstream.write_manifest(path, refs)

            with self.assertRaisesRegex(ValueError, "versions do not match"):
                upstream.load_manifest(
                    path,
                    expected_versions=["master", "13.x"],
                )

            payload = json.loads(path.read_text(encoding="utf-8"))
            path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not canonical JSON"):
                upstream.load_manifest(path)

    def test_write_manifest_does_not_follow_predictable_temp_symlink(self) -> None:
        """`write_manifest`가 예측 가능한 임시 symlink를 따라가지 않는지 검증."""

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
        """`write_manifest`가 동시 기록을 지원하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "refs.json"
            refs = [
                {"13.x": format(index, "x") * 40}
                for index in range(8)
            ]
            barrier = threading.Barrier(len(refs))

            def write(candidate: dict[str, str]) -> None:
                """동시 시작 시점을 맞춘 뒤 manifest 기록."""

                barrier.wait()
                upstream.write_manifest(path, candidate)

            with ThreadPoolExecutor(max_workers=len(refs)) as executor:
                futures = [executor.submit(write, candidate) for candidate in refs]
                for future in futures:
                    future.result()

            self.assertIn(upstream.load_manifest(path), refs)
            self.assertEqual(list(root.glob(".refs.json.*.tmp")), [])

    def test_write_manifest_cleans_up_only_its_temp_after_replace_failure(self) -> None:
        """`write_manifest`가 교체 실패 후 자체 임시 파일만 정리하는지 검증."""

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
        """manifest가 누락된 버전 ref를 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "refs.json"
            upstream.write_manifest(path, {"12.x": "b" * 40})

            with self.assertRaisesRegex(ValueError, "missing ref for version-13.x"):
                upstream.manifest_ref({"12.x": "b" * 40}, "13.x")

    def test_resolve_manifest_uses_one_remote_query_without_clone(self) -> None:
        """`resolve_manifest`가 clone 없이 한 번의 원격 조회만 사용하는지 검증."""

        commits = {
            "master": "a" * 40,
            "13.x": "b" * 40,
        }
        advertisement = (
            f'{commits["13.x"]}\trefs/heads/13.x\n'
            f'{commits["master"]}\trefs/heads/master\n'
        )

        def run(args: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            """원격 ref 광고와 객체 형식 확인 결과를 반환하는 모의 Git 실행기."""

            if "ls-remote" in args:
                stdout = advertisement
            elif "rev-parse" in args:
                stdout = next(
                    commit
                    for version, commit in commits.items()
                    if version in args[-1]
                )
            else:
                stdout = ""
            return subprocess.CompletedProcess(args, 0, stdout=stdout)

        with patch.object(upstream, "_PROCESS_RUNNER", side_effect=run) as runner:
            contents = upstream.resolve_manifest(["master", "13.x"])

        self.assertEqual(contents, upstream.canonical_manifest(commits))
        self.assertEqual(runner.call_count, 1)
        self.assertEqual(
            runner.call_args.args[0],
            [
                "git",
                "-c",
                "http.version=HTTP/1.1",
                "ls-remote",
                "--heads",
                "--refs",
                "--exit-code",
                upstream.UPSTREAM_REPO,
                "refs/heads/master",
                "refs/heads/13.x",
            ],
        )

    def test_resolve_manifest_rejects_invalid_remote_advertisements(self) -> None:
        """`resolve_manifest`가 잘못된 원격 ref 광고를 거부하는지 검증."""

        valid_master = f'{"a" * 40}\trefs/heads/master'
        valid_version = f'{"b" * 40}\trefs/heads/13.x'
        invalid_outputs = {
            "partial": f"{valid_master}\n",
            "duplicate": f"{valid_master}\n{valid_master}\n{valid_version}\n",
            "unexpected": (
                f"{valid_master}\n{valid_version}\n"
                f'{"c" * 40}\trefs/heads/12.x\n'
            ),
            "malformed": f"{valid_master} extra\n{valid_version}\n",
            "short OID": f"abc\trefs/heads/master\n{valid_version}\n",
            "uppercase OID": f'{"A" * 40}\trefs/heads/master\n{valid_version}\n',
        }

        for name, output in invalid_outputs.items():
            with self.subTest(name=name), patch.object(
                upstream,
                "_output",
                return_value=output,
            ):
                with self.assertRaises(ValueError):
                    upstream.resolve_manifest(["master", "13.x"])

    def test_resolve_manifest_validates_versions_before_network(self) -> None:
        """`resolve_manifest`가 네트워크 접근 전에 모든 버전을 검증하는지 확인."""

        for versions in ([], ["master", "master"], ["../master"]):
            with self.subTest(versions=versions), patch.object(
                upstream,
                "_PROCESS_RUNNER",
            ) as runner:
                with self.assertRaises(ValueError):
                    upstream.resolve_manifest(versions)
                runner.assert_not_called()

    def test_resolve_manifest_allows_shared_sha256_branch_tip(self) -> None:
        """`resolve_manifest`가 공유된 SHA-256 branch tip을 허용하는지 검증."""

        commit = "a" * 64
        advertisement = (
            f"{commit}\trefs/heads/13.x\n"
            f"{commit}\trefs/heads/master\n"
        )
        with patch.object(upstream, "_output", return_value=advertisement):
            contents = upstream.resolve_manifest(["master", "13.x"])

        self.assertEqual(
            upstream.load_manifest_bytes(
                contents,
                expected_versions=["master", "13.x"],
            ),
            {"master": commit, "13.x": commit},
        )

    def test_resolve_manifest_does_not_retry_remote_query_failure(self) -> None:
        """`resolve_manifest`가 원격 조회 실패를 재시도하지 않는지 검증."""

        error = subprocess.CalledProcessError(128, ["git", "ls-remote"])
        with patch.object(
            upstream,
            "_output",
            side_effect=error,
        ) as output:
            with self.assertRaises(subprocess.CalledProcessError):
                upstream.resolve_manifest(["master"])

        output.assert_called_once()
        self.assertEqual(
            output.call_args.kwargs["timeout"],
            upstream.UPSTREAM_REF_QUERY_TIMEOUT,
        )

    def test_main_fetches_only_the_selected_pinned_source_without_clone(self) -> None:
        """`main`이 clone 없이 선택한 고정 원문만 가져오는지 검증."""

        commit = "a" * 40

        def run(args: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            """`rev-parse` 호출에 고정 commit을 반환하는 모의 Git 실행기."""

            stdout = commit if "rev-parse" in args else ""
            return subprocess.CompletedProcess(args, 0, stdout=stdout)

        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "refs.json"
            upstream.write_manifest(manifest, {"13.x": commit})
            with patch.dict(
                os.environ,
                {upstream.MANIFEST_ENV: str(manifest)},
                clear=True,
            ), patch.object(
                upstream, "supported_versions", return_value=["13.x"]
            ), patch.object(
                upstream, "_PROCESS_RUNNER", side_effect=run
            ) as runner, patch.object(
                upstream, "sync_version", return_value=1
            ):
                result = upstream.main(
                    version="13.x",
                    doc="collections.md",
                )

        commands = [call.args[0] for call in runner.call_args_list]
        self.assertEqual(result, 0)
        self.assertFalse(any("clone" in command for command in commands))
        fetch_commands = [command for command in commands if "fetch" in command]
        self.assertEqual(len(fetch_commands), 1)
        self.assertIn("--depth=1", fetch_commands[0])
        self.assertIn("--filter=blob:none", fetch_commands[0])
        self.assertIn("--no-tags", fetch_commands[0])
        self.assertIn(
            f"{commit}:refs/translation-sync/13.x",
            fetch_commands[0],
        )
        sparse_index = next(
            index
            for index, command in enumerate(commands)
            if "sparse-checkout" in command
        )
        fetch_index = commands.index(fetch_commands[0])
        self.assertLess(sparse_index, fetch_index)

    def test_prepare_upstream_uses_partial_atomic_markdown_fetch(self) -> None:
        """`_prepare_upstream`이 부분적이고 원자적인 Markdown fetch를 사용하는지 검증."""

        commit = "a" * 40

        def run(args: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            """`rev-parse` 호출에 고정 commit을 반환하는 모의 Git 실행기."""

            stdout = commit if "rev-parse" in args else ""
            return subprocess.CompletedProcess(args, 0, stdout=stdout)

        with tempfile.TemporaryDirectory() as tmp, patch.object(
            upstream,
            "_PROCESS_RUNNER",
            side_effect=run,
        ) as runner:
            upstream._prepare_upstream(  # noqa: SLF001
                Path(tmp) / "source",
                {"13.x": commit},
            )

        commands = [call.args[0] for call in runner.call_args_list]
        init = next(command for command in commands if "init" in command)
        self.assertIn("--object-format=sha1", init)
        sparse = next(
            command for command in commands if "sparse-checkout" in command
        )
        self.assertEqual(sparse[-1], "*.md")
        fetch = next(command for command in commands if "fetch" in command)
        self.assertIn("--atomic", fetch)
        self.assertIn("--no-write-fetch-head", fetch)
        self.assertIn("--recurse-submodules=no", fetch)
        fetch_index = commands.index(fetch)
        for key, value in (
            ("remote.origin.promisor", "true"),
            ("remote.origin.partialclonefilter", "blob:none"),
        ):
            config_index = next(
                index
                for index, command in enumerate(commands)
                if command[-2:] == [key, value]
            )
            self.assertLess(config_index, fetch_index)

    def test_prepare_upstream_supports_sha256_object_repositories(self) -> None:
        """`_prepare_upstream`이 SHA-256 객체 저장소를 지원하는지 검증."""

        commit = "a" * 64

        def run(args: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            """`rev-parse` 호출에 고정 commit을 반환하는 모의 Git 실행기."""

            stdout = commit if "rev-parse" in args else ""
            return subprocess.CompletedProcess(args, 0, stdout=stdout)

        with tempfile.TemporaryDirectory() as tmp, patch.object(
            upstream,
            "_PROCESS_RUNNER",
            side_effect=run,
        ) as runner:
            upstream._prepare_upstream(  # noqa: SLF001
                Path(tmp) / "source",
                {"master": commit},
            )

        init = next(
            call.args[0]
            for call in runner.call_args_list
            if "init" in call.args[0]
        )
        self.assertIn("--object-format=sha256", init)

    def test_prepare_upstream_rejects_mixed_object_formats_before_git(self) -> None:
        """`_prepare_upstream`이 Git 실행 전에 혼합 객체 형식을 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp, patch.object(
            upstream,
            "_PROCESS_RUNNER",
        ) as runner:
            with self.assertRaisesRegex(ValueError, "object formats"):
                upstream._prepare_upstream(  # noqa: SLF001
                    Path(tmp) / "source",
                    {"master": "a" * 40, "13.x": "b" * 64},
                )

        runner.assert_not_called()

    def test_prepare_upstream_escapes_literal_document_sparse_pattern(self) -> None:
        """`_prepare_upstream`이 문서 경로의 sparse pattern 메타 문자를 이스케이프하는지 검증."""

        commit = "a" * 40

        def run(args: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            """`rev-parse` 호출에 고정 commit을 반환하는 모의 Git 실행기."""

            stdout = commit if "rev-parse" in args else ""
            return subprocess.CompletedProcess(args, 0, stdout=stdout)

        with tempfile.TemporaryDirectory() as tmp, patch.object(
            upstream,
            "_PROCESS_RUNNER",
            side_effect=run,
        ) as runner:
            upstream._prepare_upstream(  # noqa: SLF001
                Path(tmp) / "source",
                {"13.x": commit},
                doc="guides/[draft]*?.md",
            )

        sparse = next(
            call.args[0]
            for call in runner.call_args_list
            if "sparse-checkout" in call.args[0]
        )
        self.assertEqual(sparse[-1], "/guides/\\[draft\\]\\*\\?.md")

    def test_prepare_upstream_uses_markdown_fallback_for_line_break_doc(self) -> None:
        """`_prepare_upstream`이 줄바꿈 포함 문서에 Markdown fallback을 사용하는지 검증."""

        commit = "a" * 40

        def run(args: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            """`rev-parse` 호출에 고정 commit을 반환하는 모의 Git 실행기."""

            stdout = commit if "rev-parse" in args else ""
            return subprocess.CompletedProcess(args, 0, stdout=stdout)

        with tempfile.TemporaryDirectory() as tmp, patch.object(
            upstream,
            "_PROCESS_RUNNER",
            side_effect=run,
        ) as runner:
            upstream._prepare_upstream(  # noqa: SLF001
                Path(tmp) / "source",
                {"13.x": commit},
                doc="guides/line\nbreak.md",
            )

        sparse = next(
            call.args[0]
            for call in runner.call_args_list
            if "sparse-checkout" in call.args[0]
        )
        self.assertEqual(sparse[-1], "*.md")

    def test_main_writes_branch_ref_then_reuses_pinned_ref(self) -> None:
        """`main`이 branch ref를 기록한 뒤 고정 ref를 재사용하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "refs.json"
            commit = "a" * 40
            with patch.dict(
                os.environ,
                {upstream.MANIFEST_ENV: str(path)},
                clear=True,
            ), patch.object(
                upstream, "supported_versions", return_value=["13.x"]
            ), patch.object(
                upstream,
                "resolve_manifest",
                return_value=upstream.canonical_manifest({"13.x": commit}),
            ) as resolve_manifest, patch.object(
                upstream, "_prepare_upstream"
            ), patch.object(
                upstream, "sync_version", return_value=1
            ) as sync_version:
                self.assertEqual(upstream.main(), 0)
                self.assertEqual(
                    sync_version.call_args.kwargs["ref"], commit
                )

                sync_version.reset_mock()
                self.assertEqual(upstream.main(), 0)

            resolve_manifest.assert_called_once_with(
                ["13.x"],
                deadline=None,
            )
            self.assertEqual(sync_version.call_args.kwargs["ref"], commit)

    def test_main_does_not_log_absolute_manifest_artifact_path(self) -> None:
        """`main`이 manifest 산출물의 절대 경로를 기록하지 않는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "refs.json"
            stdout = io.StringIO()

            with redirect_stdout(stdout), patch.dict(
                os.environ,
                {upstream.MANIFEST_ENV: str(path)},
            ), patch.object(
                upstream, "supported_versions", return_value=["13.x"]
            ), patch.object(
                upstream,
                "resolve_manifest",
                return_value=upstream.canonical_manifest({"13.x": "a" * 40}),
            ), patch.object(
                upstream, "_prepare_upstream"
            ), patch.object(
                upstream, "sync_version", return_value=1
            ):
                result = upstream.main()

            self.assertEqual(result, 0)
            self.assertNotIn(str(path), stdout.getvalue())
            self.assertIn("upstream manifest: written", stdout.getvalue())

    def test_main_scopes_checkout_and_copy_to_requested_filters(self) -> None:
        """`main`이 요청한 버전·문서 filter를 `sync_version`에 전달하는지 검증."""

        commits = {"12.x": "a" * 40, "13.x": "b" * 40}
        with patch.dict(os.environ, {}, clear=True), patch.object(
            upstream, "supported_versions", return_value=["12.x", "13.x"]
        ), patch.object(
            upstream,
            "resolve_manifest",
            return_value=upstream.canonical_manifest(commits),
        ), patch.object(
            upstream, "_prepare_upstream"
        ), patch.object(
            upstream, "sync_version", return_value=1
        ) as sync_version:
            result = upstream.main(version="13.x", doc="collections.md")

        self.assertEqual(result, 0)
        sync_version.assert_called_once()
        self.assertEqual(sync_version.call_args.args[1], "13.x")
        self.assertEqual(sync_version.call_args.kwargs["doc"], "collections.md")

    def test_main_requires_version_for_document_before_source_setup(self) -> None:
        """`main`이 원문 준비 전에 문서 선택용 버전을 요구하는지 검증."""

        stderr = io.StringIO()
        with redirect_stderr(stderr), patch.dict(
            os.environ,
            {},
            clear=True,
        ), patch.object(
            upstream,
            "supported_versions",
            return_value=["master", "13.x"],
        ), patch.object(upstream, "_prepare_upstream") as prepare:
            result = upstream.main(doc="guides/queues.md")

        self.assertEqual(result, 1)
        prepare.assert_not_called()
        self.assertEqual(
            stderr.getvalue(),
            "invalid document filter: --doc requires --version\n",
        )

    def test_main_selector_does_not_reduce_generated_manifest_entries(self) -> None:
        """`main`의 selector가 생성된 manifest entry를 줄이지 않는지 검증."""

        commits = {
            "master": "a" * 40,
            "13.x": "b" * 40,
        }

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "refs.json"
            with patch.dict(
                os.environ,
                {upstream.MANIFEST_ENV: str(path)},
            ), patch.object(
                upstream,
                "supported_versions",
                return_value=["master", "13.x"],
            ), patch.object(
                upstream,
                "resolve_manifest",
                return_value=upstream.canonical_manifest(commits),
            ) as resolve_manifest, patch.object(
                upstream, "_prepare_upstream"
            ), patch.object(
                upstream,
                "sync_version",
                return_value=1,
            ) as sync_version:
                result = upstream.main(version="13.x", doc="collections.md")

            self.assertEqual(result, 0)
            resolve_manifest.assert_called_once_with(
                ["master", "13.x"],
                deadline=None,
            )
            self.assertEqual(
                upstream.load_manifest(
                    path,
                    expected_versions=["master", "13.x"],
                ),
                commits,
            )
            sync_version.assert_called_once_with(
                unittest.mock.ANY,
                "13.x",
                ref=commits["13.x"],
                doc="collections.md",
            )

    def test_main_rejects_manifest_missing_a_supported_version(self) -> None:
        """`main`이 지원 버전이 누락된 manifest를 거부하는지 검증."""

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

    def test_main_rejects_manifest_digest_mismatch_before_source_setup(self) -> None:
        """`main`이 원문 준비 전에 manifest digest 불일치를 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "refs.json"
            upstream.write_manifest(path, {"13.x": "a" * 40})

            with patch.dict(
                os.environ,
                {
                    upstream.MANIFEST_ENV: str(path),
                    upstream.MANIFEST_DIGEST_ENV: "0" * 64,
                },
            ), patch.object(
                upstream, "supported_versions", return_value=["13.x"]
            ), patch.object(
                upstream, "_prepare_upstream"
            ) as prepare:
                result = upstream.main()

            self.assertEqual(result, 1)
            prepare.assert_not_called()

    def test_main_accepts_matching_manifest_digest(self) -> None:
        """`main`이 일치하는 manifest digest를 허용하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "refs.json"
            upstream.write_manifest(path, {"13.x": "a" * 40})
            digest = upstream.manifest_digest(path.read_bytes())

            with patch.dict(
                os.environ,
                {
                    upstream.MANIFEST_ENV: str(path),
                    upstream.MANIFEST_DIGEST_ENV: digest,
                },
            ), patch.object(
                upstream, "supported_versions", return_value=["13.x"]
            ), patch.object(
                upstream, "_prepare_upstream"
            ), patch.object(
                upstream, "sync_version", return_value=1
            ) as sync_version:
                result = upstream.main()

            self.assertEqual(result, 0)
            sync_version.assert_called_once()

    def test_main_reports_manifest_write_failure(self) -> None:
        """`main`이 manifest 기록 실패 시 종료 코드 1을 반환하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "refs.json"
            refs = {"13.x": "a" * 40}
            with patch.dict(
                os.environ, {upstream.MANIFEST_ENV: str(path)}
            ), patch.object(
                upstream, "supported_versions", return_value=["13.x"]
            ), patch.object(
                upstream,
                "resolve_manifest",
                return_value=upstream.canonical_manifest(refs),
            ), patch.object(
                upstream, "_prepare_upstream"
            ), patch.object(
                upstream, "sync_version", return_value=1
            ), patch.object(
                upstream, "write_manifest", side_effect=OSError("read-only")
            ):
                result = upstream.main()

            self.assertEqual(result, 1)

    def test_sync_version_rejects_unsafe_version_before_checkout_or_write(self) -> None:
        """`sync_version`이 checkout 또는 기록 전에 안전하지 않은 버전을 거부하는지 검증."""

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
        """`sync_version`이 기록 전에 선행 0이 있는 버전을 거부하는지 검증."""

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
        """`sync_version`이 다른 버전을 가리키는 목적지 symlink를 거부하는지 검증."""

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
        """`sync_version`이 checkout 전에 symlink인 영어 원문 root를 거부하는지 검증."""

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
        """`sync_version`이 symlink인 영어 원문 root의 상위 경로를 거부하는지 검증."""

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
        """`sync_version`이 symlink인 목적지 leaf를 거부하는지 검증."""

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
        """`sync_version`이 checkout 후 목적지 leaf를 다시 검사하는지 검증."""

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
                """checkout 도중 목적지 symlink 생성."""

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
        """`sync_version`이 checkout 또는 unlink 전에 안전하지 않은 문서를 거부하는지 검증."""

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

    def test_sync_version_rejects_non_string_document_before_checkout(self) -> None:
        """`sync_version`이 checkout 전에 문자열이 아닌 문서를 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()

            with patch.object(upstream, "EN_ROOT", root / "en"), patch.object(
                upstream, "_run"
            ) as run:
                with self.assertRaisesRegex(ValueError, "invalid document"):
                    upstream.sync_version(
                        repo_dir,
                        "13.x",
                        doc=13,  # type: ignore[arg-type]
                    )

            run.assert_not_called()

    def test_main_reports_fetch_failure_without_traceback(self) -> None:
        """`main`이 fetch 실패를 추적 정보 없이 보고하는지 검증."""

        stderr = io.StringIO()
        error = subprocess.CalledProcessError(128, ["git", "fetch"])
        manifest = upstream.canonical_manifest({"13.x": "a" * 40})

        with redirect_stderr(stderr), patch.dict(
            os.environ, {}, clear=True
        ), patch.object(
            upstream, "supported_versions", return_value=["13.x"]
        ), patch.object(
            upstream, "resolve_manifest", return_value=manifest
        ), patch.object(
            upstream, "_prepare_upstream", side_effect=error
        ):
            result = upstream.main(version="13.x")

        self.assertEqual(result, 1)
        self.assertEqual(stderr.getvalue(), "upstream fetch failed\n")

    def test_main_reports_fetch_timeout_without_traceback(self) -> None:
        """`main`이 fetch timeout을 추적 정보 없이 보고하는지 검증."""

        stderr = io.StringIO()
        error = subprocess.TimeoutExpired(["git", "fetch"], 300)
        manifest = upstream.canonical_manifest({"13.x": "a" * 40})

        with redirect_stderr(stderr), patch.dict(
            os.environ, {}, clear=True
        ), patch.object(
            upstream, "supported_versions", return_value=["13.x"]
        ), patch.object(
            upstream, "resolve_manifest", return_value=manifest
        ), patch.object(
            upstream, "_prepare_upstream", side_effect=error
        ):
            result = upstream.main(version="13.x")

        self.assertEqual(result, 1)
        self.assertEqual(stderr.getvalue(), "upstream fetch failed\n")

    def test_prepare_upstream_does_not_retry_fetch_failure(self) -> None:
        """`_prepare_upstream`이 fetch 실패를 재시도하지 않는지 검증."""

        commit = "a" * 40
        fetch_error = subprocess.CalledProcessError(128, ["git", "fetch"])

        def run(args: list[str], **_kwargs: object) -> None:
            """fetch 호출에서 지정 오류를 발생시키는 모의 Git 실행기."""

            if "fetch" in args:
                raise fetch_error

        with tempfile.TemporaryDirectory() as tmp, patch.object(
            upstream,
            "_run",
            side_effect=run,
        ) as process:
            with self.assertRaises(subprocess.CalledProcessError):
                upstream._prepare_upstream(  # noqa: SLF001
                    Path(tmp) / "source",
                    {"13.x": commit},
                )

        fetch_calls = [
            call for call in process.call_args_list if "fetch" in call.args[0]
        ]
        self.assertEqual(len(fetch_calls), 1)
        self.assertEqual(
            fetch_calls[0].kwargs["timeout"],
            upstream.UPSTREAM_FETCH_TIMEOUT,
        )

    def test_main_fails_when_requested_branch_is_unavailable(self) -> None:
        """`main`이 요청한 branch를 사용할 수 없을 때 실패하는지 검증."""

        error = subprocess.CalledProcessError(1, ["git", "checkout"])
        manifest = upstream.canonical_manifest({"13.x": "a" * 40})

        with patch.dict(os.environ, {}, clear=True), patch.object(
            upstream, "supported_versions", return_value=["13.x"]
        ), patch.object(
            upstream, "resolve_manifest", return_value=manifest
        ), patch.object(
            upstream, "_prepare_upstream"
        ), patch.object(
            upstream, "sync_version", side_effect=error
        ):
            result = upstream.main(version="13.x", doc="example.md")

        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
