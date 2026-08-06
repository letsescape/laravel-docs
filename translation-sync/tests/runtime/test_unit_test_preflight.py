"""unit test preflight 동작과 경계 조건 검증."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sync.runtime.failure import IssueCode
from sync.runtime.process import ProcessTreeCleanupError
from sync.runtime.unit_test import ApprovedBaseUnitTestRunner


def _git(repo: Path, *args: str) -> str:
    """Git 처리."""

    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _init_repo(root: Path) -> tuple[str, str]:
    """init repo 처리."""

    root.mkdir()
    _git(root, "init", "--quiet")
    _git(root, "config", "user.name", "Unit Test Preflight")
    _git(root, "config", "user.email", "unit-test-preflight@localhost")
    (root / ".gitignore").write_text(".cache/\n", encoding="utf-8")
    (root / "tracked.txt").write_text("approved\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "--quiet", "-m", "approved base")
    return _git(root, "rev-parse", "HEAD"), _git(root, "rev-parse", "HEAD^{tree}")


def _repository_state(repo: Path) -> tuple[str, str, str, bytes]:
    """저장소 상태 처리."""

    return (
        _git(repo, "rev-parse", "HEAD"),
        _git(repo, "symbolic-ref", "HEAD"),
        _git(repo, "write-tree"),
        (repo / "tracked.txt").read_bytes(),
    )


def _python(script: str) -> tuple[str, ...]:
    """python 처리."""

    return (sys.executable, "-c", script)


class _Deadline:
    """기한 객체."""

    def __init__(self, seconds: float = 30.0) -> None:
        """기한 초기화."""

        self.seconds = seconds
        self.calls = 0

    def remaining(self) -> float:
        """남은 처리."""

        self.calls += 1
        return self.seconds


class ApprovedBaseUnitTestRunnerTests(unittest.TestCase):
    """승인된 기준본 단위 테스트 runner 동작과 경계 조건 테스트 모음."""

    def test_success_proves_base_tree_and_argv_in_a_cleaned_detached_clone(
        self,
    ) -> None:
        """`success_proves_base` 관련 경계 조건 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "active"
            base, tree = _init_repo(source)
            active_before = _repository_state(source)
            artifacts = root / "artifacts"
            marker = root / "test-observation.json"
            command = _python(
                "import json, pathlib, subprocess; "
                f"marker = pathlib.Path({str(marker)!r}); "
                "cwd = pathlib.Path.cwd(); "
                "detached = subprocess.run(["
                "'git', 'symbolic-ref', '-q', 'HEAD'], cwd=cwd).returncode != 0; "
                "alternates = cwd / '.git/objects/info/alternates'; "
                "(cwd / '.cache').mkdir(); "
                "(cwd / '.cache/result').write_text('ignored cache'); "
                "marker.write_text(json.dumps({"
                "'cwd': str(cwd), 'detached': detached, "
                "'alternates': alternates.exists()}))"
            )
            deadline = _Deadline()
            real_run = subprocess.run
            calls: list[tuple[object, dict[str, object]]] = []

            def run_with_recording(*args: object, **kwargs: object):
                """with recording 실행."""

                calls.append((args[0], kwargs.copy()))
                return real_run(*args, **kwargs)

            runner = ApprovedBaseUnitTestRunner(
                source_repo=source,
                artifact_root=artifacts,
                remaining_seconds=deadline.remaining,
            )
            with patch(
                "sync.runtime.unit_test.run_process_tree",
                side_effect=run_with_recording,
            ):
                result = runner.run(base_commit=base, unit_test_argv=command)

            self.assertTrue(result.succeeded)
            self.assertIsNone(result.failure)
            self.assertIsNotNone(result.proof)
            assert result.proof is not None
            self.assertEqual(result.proof.base_commit, base)
            self.assertEqual(result.proof.base_tree, tree)
            self.assertEqual(
                result.proof.argv_digest,
                hashlib.sha256(
                    json.dumps(
                        list(command),
                        ensure_ascii=False,
                        separators=(",", ":"),
                    ).encode("utf-8")
                ).hexdigest(),
            )
            self.assertTrue(result.sandbox_cleaned)
            self.assertIsNotNone(result.sandbox_path)
            assert result.sandbox_path is not None
            self.assertFalse(result.sandbox_path.exists())
            self.assertTrue(result.sandbox_path.is_relative_to(artifacts.resolve()))

            observation = json.loads(marker.read_text(encoding="utf-8"))
            self.assertNotEqual(Path(observation["cwd"]), source)
            self.assertTrue(
                Path(observation["cwd"]).is_relative_to(artifacts.resolve())
            )
            self.assertTrue(observation["detached"])
            self.assertFalse(observation["alternates"])
            self.assertEqual(_repository_state(source), active_before)
            self.assertGreater(deadline.calls, 0)
            self.assertTrue(calls)
            self.assertTrue(
                all(
                    isinstance(kwargs.get("timeout"), (int, float))
                    and 0 < float(kwargs["timeout"]) <= deadline.seconds
                    for _, kwargs in calls
                )
            )
            self.assertTrue(
                all(kwargs.get("shell", False) is False for _, kwargs in calls)
            )

    def test_tracked_worktree_index_or_head_mutation_fails_and_cleans_sandbox(
        self,
    ) -> None:
        """`tracked_worktree_index`의 실패 처리 경계 검증."""

        mutations = {
            "worktree": (
                "from pathlib import Path; "
                "Path('tracked.txt').write_text('mutated\\n')"
            ),
            "index": (
                "from pathlib import Path; import subprocess; "
                "Path('new.txt').write_text('new\\n'); "
                "subprocess.run(['git', 'add', 'new.txt'], check=True)"
            ),
            "head": "import subprocess; subprocess.run(['git', 'reset', '--soft', 'HEAD^'], check=True)",
        }
        for name, script in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                source = root / "active"
                _init_repo(source)
                (source / "second.txt").write_text("second\n", encoding="utf-8")
                _git(source, "add", "second.txt")
                _git(source, "commit", "--quiet", "-m", "second")
                base = _git(source, "rev-parse", "HEAD")
                active_before = _repository_state(source)
                runner = ApprovedBaseUnitTestRunner(
                    source_repo=source,
                    artifact_root=root / "artifacts",
                    remaining_seconds=_Deadline().remaining,
                )

                result = runner.run(
                    base_commit=base,
                    unit_test_argv=_python(script),
                )

                self.assertFalse(result.succeeded)
                self.assertIsNotNone(result.failure)
                assert result.failure is not None
                self.assertEqual(
                    result.failure.issue_code,
                    IssueCode.UNIT_TEST_SOURCE_MUTATION,
                )
                self.assertTrue(result.sandbox_cleaned)
                assert result.sandbox_path is not None
                self.assertFalse(result.sandbox_path.exists())
                self.assertEqual(_repository_state(source), active_before)

    def test_nonzero_test_exit_returns_unit_test_failed_after_cleanup(self) -> None:
        """`nonzero_test_exit`의 cleanup 후 단위 테스트 failed 반환 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "active"
            base, _ = _init_repo(source)
            runner = ApprovedBaseUnitTestRunner(
                source_repo=source,
                artifact_root=root / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )

            result = runner.run(
                base_commit=base,
                unit_test_argv=_python("raise SystemExit(7)"),
            )

            self.assertFalse(result.succeeded)
            self.assertIsNotNone(result.failure)
            assert result.failure is not None
            self.assertEqual(result.failure.issue_code, IssueCode.UNIT_TEST_FAILED)
            self.assertEqual(result.failure.returncode, 7)
            self.assertTrue(result.sandbox_cleaned)
            assert result.sandbox_path is not None
            self.assertFalse(result.sandbox_path.exists())

    def test_empty_command_and_non_full_base_are_configuration_failures(self) -> None:
        """빈 명령 및 non 전체 기준본 설정 실패 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "active"
            base, _ = _init_repo(source)
            runner = ApprovedBaseUnitTestRunner(
                source_repo=source,
                artifact_root=root / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )

            empty = runner.run(base_commit=base, unit_test_argv=())
            abbreviated = runner.run(
                base_commit=base[:12],
                unit_test_argv=_python("raise SystemExit(0)"),
            )

            self.assertEqual(
                empty.failure.issue_code if empty.failure else None,
                IssueCode.REQUIRED_CONFIG_MISSING,
            )
            self.assertEqual(
                abbreviated.failure.issue_code if abbreviated.failure else None,
                IssueCode.INVALID_RUNTIME_OPTION,
            )
            self.assertFalse((root / "artifacts").exists())

    def test_unresolved_full_commit_is_an_input_failure(self) -> None:
        """`unresolved_full_commit`의 입력 실패 판정 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "active"
            _init_repo(source)
            runner = ApprovedBaseUnitTestRunner(
                source_repo=source,
                artifact_root=root / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )

            result = runner.run(
                base_commit="f" * 40,
                unit_test_argv=_python("raise SystemExit(0)"),
            )

            self.assertFalse(result.succeeded)
            self.assertEqual(
                result.failure.issue_code if result.failure else None,
                IssueCode.MANIFEST_COMMIT_UNRESOLVED,
            )
            self.assertIsNone(result.sandbox_path)

    def test_process_start_failure_is_stable_and_sandbox_is_cleaned(self) -> None:
        """`process_start_failure`의 stable 및 sandbox cleaned 판정 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "active"
            base, _ = _init_repo(source)
            runner = ApprovedBaseUnitTestRunner(
                source_repo=source,
                artifact_root=root / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )

            result = runner.run(
                base_commit=base,
                unit_test_argv=("definitely-not-a-real-executable",),
            )

            self.assertFalse(result.succeeded)
            self.assertEqual(
                result.failure.issue_code if result.failure else None,
                IssueCode.RUNNER_OPERATION_FAILED,
            )
            self.assertTrue(result.sandbox_cleaned)
            assert result.sandbox_path is not None
            self.assertFalse(result.sandbox_path.exists())

    def test_process_tree_failure_is_stable_and_sandbox_is_cleaned(self) -> None:
        """`process_tree_failure`의 stable 및 sandbox cleaned 판정 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "active"
            base, _ = _init_repo(source)
            command = _python("raise SystemExit(0)")
            runner = ApprovedBaseUnitTestRunner(
                source_repo=source,
                artifact_root=root / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )
            real_run = subprocess.run

            def fail_test_process(*args: object, **kwargs: object):
                """테스트용 테스트 프로세스 대체 동작."""

                if args[0] == list(command):
                    raise ProcessTreeCleanupError("private cleanup detail")
                return real_run(*args, **kwargs)

            with patch(
                "sync.runtime.unit_test.run_process_tree",
                side_effect=fail_test_process,
            ):
                result = runner.run(
                    base_commit=base,
                    unit_test_argv=command,
                )

            self.assertFalse(result.succeeded)
            self.assertEqual(
                result.failure.issue_code if result.failure else None,
                IssueCode.RUNNER_OPERATION_FAILED,
            )
            self.assertTrue(result.sandbox_cleaned)
            assert result.sandbox_path is not None
            self.assertFalse(result.sandbox_path.exists())

    def test_expired_deadline_starts_no_subprocess(self) -> None:
        """`expired_deadline_starts_no_subprocess` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "active"
            base, _ = _init_repo(source)
            runner = ApprovedBaseUnitTestRunner(
                source_repo=source,
                artifact_root=root / "artifacts",
                remaining_seconds=_Deadline(0).remaining,
            )

            with patch("sync.runtime.unit_test.run_process_tree") as run:
                result = runner.run(
                    base_commit=base,
                    unit_test_argv=_python("raise SystemExit(0)"),
                )

            run.assert_not_called()
            self.assertEqual(
                result.failure.issue_code if result.failure else None,
                IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            )
            self.assertIsNone(result.sandbox_path)

    def test_subprocess_timeout_returns_deadline_failure_after_cleanup(self) -> None:
        """`subprocess_timeout`의 cleanup 후 기한 실패 반환 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "active"
            base, _ = _init_repo(source)
            command = _python("raise SystemExit(0)")
            runner = ApprovedBaseUnitTestRunner(
                source_repo=source,
                artifact_root=root / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )
            real_run = subprocess.run

            def timeout_test_process(*args: object, **kwargs: object):
                """timeout 테스트 프로세스 처리."""

                if args[0] == list(command):
                    raise subprocess.TimeoutExpired(args[0], kwargs["timeout"])
                return real_run(*args, **kwargs)

            with patch(
                "sync.runtime.unit_test.run_process_tree",
                side_effect=timeout_test_process,
            ):
                result = runner.run(
                    base_commit=base,
                    unit_test_argv=command,
                )

            self.assertEqual(
                result.failure.issue_code if result.failure else None,
                IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            )
            self.assertTrue(result.sandbox_cleaned)
            assert result.sandbox_path is not None
            self.assertFalse(result.sandbox_path.exists())

    def test_cleanup_failure_replaces_success_with_sandbox_failure(self) -> None:
        """`cleanup_failure_replaces_success_with_sandbox_failure` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "active"
            base, _ = _init_repo(source)
            runner = ApprovedBaseUnitTestRunner(
                source_repo=source,
                artifact_root=root / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )

            with patch(
                "sync.runtime.unit_test.shutil.rmtree",
                side_effect=OSError("cleanup failed"),
            ):
                result = runner.run(
                    base_commit=base,
                    unit_test_argv=_python("raise SystemExit(0)"),
                )

            self.assertFalse(result.succeeded)
            self.assertIsNone(result.proof)
            self.assertEqual(
                result.failure.issue_code if result.failure else None,
                IssueCode.SANDBOX_OPERATION_FAILED,
            )
            self.assertFalse(result.sandbox_cleaned)
            assert result.sandbox_path is not None
            self.assertTrue(result.sandbox_path.exists())

    def test_cleanup_failure_overrides_a_controlled_test_failure(self) -> None:
        """`cleanup_failure_overrides_a_controlled_test_failure` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "active"
            base, _ = _init_repo(source)
            runner = ApprovedBaseUnitTestRunner(
                source_repo=source,
                artifact_root=root / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )

            with patch(
                "sync.runtime.unit_test.shutil.rmtree",
                side_effect=OSError("cleanup failed"),
            ):
                result = runner.run(
                    base_commit=base,
                    unit_test_argv=_python("raise SystemExit(7)"),
                )

            self.assertEqual(
                result.failure.issue_code if result.failure else None,
                IssueCode.SANDBOX_OPERATION_FAILED,
            )
            self.assertFalse(result.sandbox_cleaned)

    def test_cleanup_failure_does_not_replace_an_earlier_infrastructure_failure(
        self,
    ) -> None:
        """`cleanup_failure`의 않음 replace earlier infrastructure 실패 동작 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "active"
            base, _ = _init_repo(source)
            command = _python("raise SystemExit(0)")
            runner = ApprovedBaseUnitTestRunner(
                source_repo=source,
                artifact_root=root / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )
            real_run = subprocess.run

            def timeout_test_process(*args: object, **kwargs: object):
                """timeout 테스트 프로세스 처리."""

                if args[0] == list(command):
                    raise subprocess.TimeoutExpired(args[0], kwargs["timeout"])
                return real_run(*args, **kwargs)

            with (
                patch(
                    "sync.runtime.unit_test.run_process_tree",
                    side_effect=timeout_test_process,
                ),
                patch(
                    "sync.runtime.unit_test.shutil.rmtree",
                    side_effect=OSError("cleanup failed"),
                ),
            ):
                result = runner.run(base_commit=base, unit_test_argv=command)

            self.assertEqual(
                result.failure.issue_code if result.failure else None,
                IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            )
            self.assertFalse(result.sandbox_cleaned)

    def test_final_active_fingerprint_io_failure_is_a_runner_failure(self) -> None:
        """`final_active_fingerprint_io_failure`의 runner 실패 판정 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "active"
            base, _ = _init_repo(source)
            runner = ApprovedBaseUnitTestRunner(
                source_repo=source,
                artifact_root=root / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )
            real_fingerprint = runner._disk_fingerprint
            fingerprint_calls = 0

            def fail_final_fingerprint(layout: object) -> bytes:
                """테스트용 final fingerprint 대체 동작."""

                nonlocal fingerprint_calls
                fingerprint_calls += 1
                if fingerprint_calls == 2:
                    raise OSError("fingerprint read failed")
                return real_fingerprint(layout)  # type: ignore[arg-type]

            with patch.object(
                runner,
                "_disk_fingerprint",
                side_effect=fail_final_fingerprint,
            ):
                result = runner.run(
                    base_commit=base,
                    unit_test_argv=_python("raise SystemExit(0)"),
                )

            self.assertEqual(fingerprint_calls, 2)
            self.assertEqual(
                result.failure.issue_code if result.failure else None,
                IssueCode.RUNNER_OPERATION_FAILED,
            )
            self.assertTrue(result.sandbox_cleaned)

    def test_final_active_fingerprint_deadline_is_a_workflow_deadline_failure(
        self,
    ) -> None:
        """`final_active_fingerprint_deadline`의 워크플로 기한 실패 판정 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "active"
            base, _ = _init_repo(source)
            deadline = _Deadline()
            runner = ApprovedBaseUnitTestRunner(
                source_repo=source,
                artifact_root=root / "artifacts",
                remaining_seconds=deadline.remaining,
            )
            real_rmtree = shutil.rmtree

            def cleanup_then_expire(path: Path) -> None:
                """then expire 정리."""

                real_rmtree(path)
                deadline.seconds = 0

            with patch(
                "sync.runtime.unit_test.shutil.rmtree",
                side_effect=cleanup_then_expire,
            ):
                result = runner.run(
                    base_commit=base,
                    unit_test_argv=_python("raise SystemExit(0)"),
                )

            self.assertEqual(
                result.failure.issue_code if result.failure else None,
                IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            )
            self.assertTrue(result.sandbox_cleaned)

    def test_active_repository_mutation_overrides_test_outcome(self) -> None:
        """`active_repository_mutation_overrides_test_outcome` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "active"
            base, _ = _init_repo(source)
            artifacts = root / "artifacts"
            runner = ApprovedBaseUnitTestRunner(
                source_repo=source,
                artifact_root=artifacts,
                remaining_seconds=_Deadline().remaining,
            )
            command = _python(
                "from pathlib import Path; "
                f"Path({str(source / 'tracked.txt')!r}).write_text('external mutation\\n')"
            )

            result = runner.run(base_commit=base, unit_test_argv=command)

            self.assertFalse(result.succeeded)
            self.assertEqual(
                result.failure.issue_code if result.failure else None,
                IssueCode.ACTIVE_WORKTREE_MUTATED,
            )
            self.assertTrue(result.sandbox_cleaned)
            assert result.sandbox_path is not None
            self.assertFalse(result.sandbox_path.exists())

    def test_active_repository_mutation_overrides_cleanup_failure(self) -> None:
        """`active_repository_mutation_overrides_cleanup_failure` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "active"
            base, _ = _init_repo(source)
            runner = ApprovedBaseUnitTestRunner(
                source_repo=source,
                artifact_root=root / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )
            command = _python(
                "from pathlib import Path; "
                f"Path({str(source / 'tracked.txt')!r}).write_text('external mutation\\n')"
            )

            with patch(
                "sync.runtime.unit_test.shutil.rmtree",
                side_effect=OSError("cleanup failed"),
            ):
                result = runner.run(base_commit=base, unit_test_argv=command)

            self.assertEqual(
                result.failure.issue_code if result.failure else None,
                IssueCode.ACTIVE_WORKTREE_MUTATED,
            )
            self.assertFalse(result.sandbox_cleaned)

    def test_artifact_root_inside_active_repo_is_rejected(self) -> None:
        """`artifact_root_inside_active_repo`의 rejected 판정 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "active"
            base, _ = _init_repo(source)
            runner = ApprovedBaseUnitTestRunner(
                source_repo=source,
                artifact_root=source / ".artifacts",
                remaining_seconds=_Deadline().remaining,
            )

            result = runner.run(
                base_commit=base,
                unit_test_argv=_python("raise SystemExit(0)"),
            )

            self.assertEqual(
                result.failure.issue_code if result.failure else None,
                IssueCode.SANDBOX_OPERATION_FAILED,
            )
            self.assertFalse((source / ".artifacts").exists())


if __name__ == "__main__":
    unittest.main()
