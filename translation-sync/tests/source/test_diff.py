"""diff 동작과 경계 조건 검증."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sync import diff
from sync.runtime.process import ProcessTreeCleanupError


class DiffTests(unittest.TestCase):
    """diff 동작과 경계 조건 테스트 모음."""

    def test_process_tree_failure_is_a_controlled_git_error(self):
        """`process_tree_failure`의 제어된 Git 오류 판정 검증."""

        with patch.object(
            diff,
            "run_process_tree",
            side_effect=ProcessTreeCleanupError("private cleanup detail"),
        ):
            with self.assertRaisesRegex(
                diff.SourceDiffError,
                "git subprocess failed",
            ):
                diff.changed_sources()

    def test_changed_sources_normalizes_rename_to_delete_then_add(self):
        """`changed_sources`의 rename 후 삭제 이후 추가 정규화 검증."""

        old_path = (
            "i18n/en/docusaurus-plugin-content-docs/version-12.x/old-topic.md"
        )
        new_path = (
            "i18n/en/docusaurus-plugin-content-docs/version-12.x/new-topic.md"
        )
        result = subprocess.CompletedProcess(
            ["git", "diff"],
            0,
            stdout=f"R100\0{old_path}\0{new_path}\0",
            stderr="",
        )

        with (
            patch.object(diff, "run_process_tree", return_value=result),
            patch.object(diff, "_file_hunks", return_value=()),  # noqa: SLF001
        ):
            changes = diff.changed_sources(base_ref="base")

        self.assertEqual(
            [(change.status, change.path) for change in changes],
            [("D", old_path), ("A", new_path)],
        )

    def test_changed_sources_normalizes_real_git_rename(self):
        """`changed_sources`의 실제 Git rename 정규화 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=root,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test"], cwd=root, check=True
            )
            version_root = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x"
            )
            version_root.mkdir(parents=True)
            old_source = version_root / "old-topic.md"
            new_source = version_root / "new-topic.md"
            old_source.write_text("# Topic\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-m", "baseline"],
                cwd=root,
                check=True,
                capture_output=True,
            )
            old_source.rename(new_source)
            subprocess.run(["git", "add", "-A"], cwd=root, check=True)

            with patch.object(diff, "REPO_ROOT", root):
                changes = diff.changed_sources(base_ref="HEAD")

        prefix = "i18n/en/docusaurus-plugin-content-docs/version-12.x/"
        self.assertEqual(
            [(change.status, change.path) for change in changes],
            [("D", f"{prefix}old-topic.md"), ("A", f"{prefix}new-topic.md")],
        )
        self.assertEqual(
            [line.kind for line in changes[0].hunks[0].lines], ["delete"]
        )
        self.assertEqual(
            [line.kind for line in changes[1].hunks[0].lines], ["add"]
        )

    def test_changed_sources_rejects_noncanonical_source_path(self):
        """`changed_sources`의 비정규 원문 경로 거부 검증."""

        result = subprocess.CompletedProcess(
            ["git", "diff"],
            0,
            stdout="M\0i18n/en/docusaurus-plugin-content-docs/../outside.md\0",
            stderr="",
        )

        with patch.object(diff, "run_process_tree", return_value=result):
            with self.assertRaisesRegex(
                diff.SourceDiffError, "invalid git source path"
            ):
                diff.changed_sources(base_ref="base")

    def test_changed_sources_rejects_symlinked_source_before_loading_hunks(self):
        """`changed_sources`의 로딩 hunk 전 symlink 원문 거부 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            outside = Path(tmp) / "outside.md"
            outside.write_text("sensitive\n", encoding="utf-8")
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/leak.md"
            )
            source.parent.mkdir(parents=True)
            source.symlink_to(outside)

            with patch.object(diff, "REPO_ROOT", root):
                with self.assertRaisesRegex(
                    diff.SourceDiffError, "unsafe git source path"
                ):
                    diff.changed_sources()

    def test_changed_sources_validates_all_records_before_loading_hunks(self):
        """`changed_sources`의 로딩 hunk 전 모든 record 검증."""

        safe_path = (
            "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
        )
        result = subprocess.CompletedProcess(
            ["git", "diff"],
            0,
            stdout=(
                f"M\0{safe_path}\0"
                "M\0i18n/en/docusaurus-plugin-content-docs/../outside.md\0"
            ),
            stderr="",
        )

        with (
            patch.object(diff, "run_process_tree", return_value=result),
            patch.object(diff, "_file_hunks", return_value=()) as file_hunks,  # noqa: SLF001
        ):
            with self.assertRaisesRegex(
                diff.SourceDiffError, "invalid git source path"
            ):
                diff.changed_sources(base_ref="base")

        file_hunks.assert_not_called()

    def test_changed_sources_normalizes_worktree_rename(self):
        """`changed_sources`의 worktree rename 정규화 검증."""

        old_path = (
            "i18n/en/docusaurus-plugin-content-docs/version-12.x/old-topic.md"
        )
        new_path = (
            "i18n/en/docusaurus-plugin-content-docs/version-12.x/new-topic.md"
        )
        result = subprocess.CompletedProcess(
            ["git", "status"],
            0,
            stdout=f"R  {new_path}\0{old_path}\0",
            stderr="",
        )

        with (
            patch.object(diff, "run_process_tree", return_value=result),
            patch.object(diff, "_file_hunks", return_value=()),  # noqa: SLF001
        ):
            changes = diff.changed_sources()

        self.assertEqual(
            [(change.status, change.path) for change in changes],
            [("D", old_path), ("A", new_path)],
        )

    def test_source_change_rejects_status_outside_public_contract(self):
        """`source_change`의 상태 외부 공개 계약 거부 검증."""

        with self.assertRaisesRegex(
            diff.SourceDiffError, "unsupported source status"
        ):
            diff.SourceChange(
                path=(
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-12.x/example.md"
                ),
                status="R",
            )

    def test_source_change_parses_nested_document_relative_to_version_root(self):
        """`source_change`의 중첩 문서 상대 후 버전 root 파싱 검증."""

        change = diff.SourceChange(
            path=(
                "i18n/en/docusaurus-plugin-content-docs/"
                "version-13.x/guides/queues.md"
            ),
            status="M",
        )

        self.assertEqual(change.version, "13.x")
        self.assertEqual(change.document, "guides/queues.md")
        self.assertEqual(change.name, "queues.md")

    def test_source_change_rejects_paths_outside_canonical_version_root(self):
        """`source_change`의 경로 외부 canonical 버전 root 거부 검증."""

        invalid_paths = (
            "version-13.x/guides/queues.md",
            "i18n/en/docusaurus-plugin-content-docs/guides/queues.md",
            "i18n/en/docusaurus-plugin-content-docs/version-013.x/queues.md",
            "i18n/en/docusaurus-plugin-content-docs/version-13.x/../queues.md",
            "i18n/en/docusaurus-plugin-content-docs/version-13.x/guides\\queues.md",
            "i18n/en/docusaurus-plugin-content-docs/version-13.x/guides/queues.txt",
        )

        for path in invalid_paths:
            with self.subTest(path=path), self.assertRaisesRegex(
                diff.SourceDiffError,
                "invalid source path",
            ):
                diff.SourceChange(path=path, status="M")

    def test_changed_sources_rejects_unsupported_git_status(self):
        """`changed_sources`의 지원하지 않는 Git 상태 거부 검증."""

        path = "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
        result = subprocess.CompletedProcess(
            ["git", "diff"],
            0,
            stdout=f"T\0{path}\0",
            stderr="",
        )

        with patch.object(diff, "run_process_tree", return_value=result):
            with self.assertRaisesRegex(
                diff.SourceDiffError, "unsupported git status"
            ):
                diff.changed_sources(base_ref="base")

    def test_changed_sources_rejects_unterminated_porcelain_record(self):
        """`changed_sources`의 종결되지 않은 porcelain record 거부 검증."""

        path = "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
        result = subprocess.CompletedProcess(
            ["git", "status"],
            0,
            stdout=f" M {path}",
            stderr="",
        )

        with patch.object(diff, "run_process_tree", return_value=result):
            with self.assertRaisesRegex(
                diff.SourceDiffError, "malformed git porcelain output"
            ):
                diff.changed_sources()

    def test_changed_sources_disables_optional_git_locks(self):
        """`changed_sources`의 선택적 Git 잠금 비활성화 검증."""

        calls = []

        def fake_run(args, **kwargs):
            """테스트용 실행 대체 동작."""

            calls.append((args, kwargs))
            return subprocess.CompletedProcess(args, 0, stdout="", stderr="")

        with patch.object(diff, "run_process_tree", side_effect=fake_run):
            changes = diff.changed_sources()

        self.assertEqual(changes, [])
        self.assertEqual(calls[0][1]["env"]["GIT_OPTIONAL_LOCKS"], "0")

    def test_changed_sources_passes_only_path_locale_and_isolated_git_environment(self):
        """`changed_sources`의 만 경로 locale 및 isolated Git 환경 전달 검증."""

        captured_environment = None

        def fake_run(args, **kwargs):
            """테스트용 실행 대체 동작."""

            nonlocal captured_environment
            captured_environment = kwargs["env"]
            return subprocess.CompletedProcess(args, 0, stdout="", stderr="")

        process_environment = {
            "PATH": "/safe/bin",
            "LANG": "ko_KR.UTF-8",
            "LC_MESSAGES": "C",
            "OPENAI_API_KEY": "openai-secret",
            "AZURE_OPENAI_API_KEY": "azure-secret",
            "CODEX_API_KEY": "codex-secret",
            "GH_TOKEN": "github-secret",
            "GIT_EXTERNAL_DIFF": "/unsafe/external-diff",
            "GIT_CONFIG_COUNT": "1",
        }
        with patch.dict(
            diff.os.environ,
            process_environment,
            clear=True,
        ), patch.object(diff, "run_process_tree", side_effect=fake_run):
            self.assertEqual(diff.changed_sources(), [])

        self.assertEqual(
            captured_environment,
            {
                "PATH": "/safe/bin",
                "LANG": "ko_KR.UTF-8",
                "LC_MESSAGES": "C",
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_CONFIG_SYSTEM": os.devnull,
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_TERMINAL_PROMPT": "0",
                "GIT_OPTIONAL_LOCKS": "0",
            },
        )

    def test_git_diff_commands_disable_external_diff_and_textconv(self):
        """`git_diff_commands`의 외부 diff 및 textconv 비활성화 검증."""

        path = (
            "i18n/en/docusaurus-plugin-content-docs/"
            "version-13.x/example.md"
        )
        calls = []

        def fake_run(args, **kwargs):
            """테스트용 실행 대체 동작."""

            calls.append(args)
            if len(calls) == 1:
                output = f"M\0{path}\0"
            else:
                output = ""
            return subprocess.CompletedProcess(args, 0, stdout=output, stderr="")

        with patch.object(diff, "run_process_tree", side_effect=fake_run):
            changes = diff.changed_sources(base_ref="base")

        self.assertEqual(len(changes), 1)
        self.assertEqual(len(calls), 2)
        for args in calls:
            self.assertEqual(args[0], "git")
            self.assertEqual(
                args[1:3],
                ["-c", "core.fsmonitor=false"],
            )
            self.assertIn("diff", args)
            self.assertIn("--no-ext-diff", args)
            self.assertIn("--no-textconv", args)

    def test_local_external_diff_configuration_is_not_executed(self):
        """`local_external_diff_configuration`의 실행되지 않음 판정 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=root,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test"],
                cwd=root,
                check=True,
            )
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/"
                "version-13.x/example.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text("Before.\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-m", "baseline"],
                cwd=root,
                check=True,
                capture_output=True,
            )
            marker = root / "external-diff-ran"
            external_diff = root / "external-diff.sh"
            external_diff.write_text(
                "#!/bin/sh\n"
                f"touch '{marker}'\n"
                "exit 1\n",
                encoding="utf-8",
            )
            external_diff.chmod(0o755)
            subprocess.run(
                ["git", "config", "diff.external", str(external_diff)],
                cwd=root,
                check=True,
            )
            source.write_text("After.\n", encoding="utf-8")

            with patch.object(diff, "REPO_ROOT", root):
                changes = diff.changed_sources(base_ref="HEAD")

            self.assertEqual(len(changes), 1)
            self.assertFalse(marker.exists())

    def test_local_textconv_configuration_is_not_executed(self):
        """`local_textconv_configuration`의 실행되지 않음 판정 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=root,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test"],
                cwd=root,
                check=True,
            )
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/"
                "version-13.x/example.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text("Before.\n", encoding="utf-8")
            (root / ".gitattributes").write_text(
                "*.md diff=unsafe\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-m", "baseline"],
                cwd=root,
                check=True,
                capture_output=True,
            )
            marker = root / "textconv-ran"
            textconv = root / "textconv.sh"
            textconv.write_text(
                "#!/bin/sh\n"
                f"touch '{marker}'\n"
                "cat \"$1\"\n",
                encoding="utf-8",
            )
            textconv.chmod(0o755)
            subprocess.run(
                ["git", "config", "diff.unsafe.textconv", str(textconv)],
                cwd=root,
                check=True,
            )
            source.write_text("After.\n", encoding="utf-8")

            with patch.object(diff, "REPO_ROOT", root):
                changes = diff.changed_sources(base_ref="HEAD")

            self.assertEqual(len(changes), 1)
            self.assertFalse(marker.exists())

    def test_expired_workflow_deadline_rejects_before_git_subprocess(self):
        """`expired_workflow_deadline`의 Git 하위 프로세스 전 거부 검증."""

        with patch.dict(
            diff.os.environ,
            {
                "PATH": "/safe/bin",
                diff.WORKFLOW_DEADLINE_ENV: "100.0",
            },
            clear=True,
        ), patch.object(diff.time, "monotonic", return_value=100.0), patch.object(
            diff,
            "run_process_tree",
        ) as run:
            with self.assertRaisesRegex(
                diff.SourceDiffError,
                "workflow deadline exceeded",
            ):
                diff.changed_sources()

        run.assert_not_called()

    def test_git_subprocess_uses_remaining_workflow_deadline(self):
        """`git_subprocess`의 남은 워크플로 기한 사용 검증."""

        completed = subprocess.CompletedProcess(
            ["git", "status"],
            0,
            stdout="",
            stderr="",
        )
        with patch.dict(
            diff.os.environ,
            {
                "PATH": "/safe/bin",
                diff.WORKFLOW_DEADLINE_ENV: "125.5",
            },
            clear=True,
        ), patch.object(diff.time, "monotonic", return_value=100.0), patch.object(
            diff,
            "run_process_tree",
            return_value=completed,
        ) as run:
            self.assertEqual(diff.changed_sources(), [])

        self.assertEqual(run.call_args.kwargs["timeout"], 25.5)

    def test_git_subprocess_timeout_is_a_controlled_deadline_error(self):
        """`git_subprocess_timeout`의 제어된 기한 오류 판정 검증."""

        with patch.dict(
            diff.os.environ,
            {
                "PATH": "/safe/bin",
                diff.WORKFLOW_DEADLINE_ENV: "125.5",
            },
            clear=True,
        ), patch.object(diff.time, "monotonic", return_value=100.0), patch.object(
            diff,
            "run_process_tree",
            side_effect=subprocess.TimeoutExpired(["git", "status"], 25.5),
        ):
            with self.assertRaisesRegex(
                diff.SourceDiffError,
                "workflow deadline exceeded",
            ):
                diff.changed_sources()

    def test_changed_sources_includes_untracked_new_markdown_files(self):
        """`changed_sources`의 미추적 신규 Markdown 파일 포함 검증."""

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
        """`changed_sources`의 unified hunk 대상 수정된 파일 포함 검증."""

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

    def test_parse_unified_diff_treats_empty_lines_as_context(self):
        """`parse_unified_diff`의 빈 줄 로 문맥 취급 검증."""

        hunks = diff._parse_unified_diff(  # noqa: SLF001
            "@@ -1,3 +1,3 @@\n"
            " First.\n"
            "\n"
            "-Old.\n"
            "+New.\n"
        )

        self.assertEqual(
            [(line.kind, line.text, line.old_lineno, line.new_lineno) for line in hunks[0].lines],
            [
                ("context", "First.", 1, 1),
                ("context", "", 2, 2),
                ("delete", "Old.", 3, None),
                ("add", "New.", None, 3),
            ],
        )


if __name__ == "__main__":
    unittest.main()
