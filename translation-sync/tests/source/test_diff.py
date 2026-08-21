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
        """프로세스 트리 정리 실패를 제어된 Git 오류로 변환하는지 검증."""

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
        """`changed_sources`가 rename을 삭제 후 추가로 정규화하는지 검증."""

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
        """`changed_sources`가 실제 Git rename을 정규화하는지 검증."""

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
        """`changed_sources`가 비정규 원문 경로를 거부하는지 검증."""

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
        """`changed_sources`가 hunk를 로드하기 전에 심볼릭 링크인 원문을 거부하는지 검증."""

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
        """`changed_sources`가 모든 record를 검증한 뒤 hunk를 로드하는지 확인."""

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
        """`changed_sources`가 worktree rename을 정규화하는지 검증."""

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
        """`SourceChange`가 공개 계약에 없는 상태를 거부하는지 검증."""

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
        """`SourceChange`가 중첩 원문 경로에서 버전과 문서 상대 경로를 파싱하는지 검증."""

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
        """`SourceChange`가 canonical 버전 root 밖의 경로를 거부하는지 검증."""

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
        """`changed_sources`가 지원하지 않는 Git 상태를 거부하는지 검증."""

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
        """`changed_sources`가 종결되지 않은 porcelain record를 거부하는지 검증."""

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
        """`changed_sources`가 선택적 Git 잠금을 비활성화하는지 검증."""

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
        """`changed_sources`가 경로, 로캘 및 격리된 Git 환경만 전달하는지 검증."""

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
        """`changed_sources`의 Git diff 명령이 외부 diff와 textconv를 비활성화하는지 검증."""

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
                args[1:5],
                [
                    "-c",
                    "core.fsmonitor=false",
                    "-c",
                    f"safe.directory={diff.REPO_ROOT}",
                ],
            )
            self.assertIn("diff", args)
            self.assertIn("--no-ext-diff", args)
            self.assertIn("--no-textconv", args)

    def test_local_external_diff_configuration_is_not_executed(self):
        """로컬 external diff 설정을 실행하지 않는지 검증."""

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
        """로컬 textconv 설정을 실행하지 않는지 검증."""

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

    def test_changed_sources_includes_untracked_new_markdown_files(self):
        """`changed_sources`가 미추적 신규 Markdown 파일을 포함하는지 검증."""

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
        """`changed_sources`가 수정 파일의 unified hunk를 포함하는지 검증."""

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
        """`_parse_unified_diff`가 빈 줄을 문맥으로 취급하는지 검증."""

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
