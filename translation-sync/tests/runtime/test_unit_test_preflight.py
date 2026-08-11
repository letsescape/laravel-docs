"""승인 기준본 단위 테스트 사전 실행 동작과 경계 조건 검증."""

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
    """Git 명령 실행."""

    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _init_repo(root: Path) -> tuple[str, str]:
    """테스트용 Git 저장소 초기화."""

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
    """저장소의 커밋·트리·작업 트리 상태 조회."""

    return (
        _git(repo, "rev-parse", "HEAD"),
        _git(repo, "symbolic-ref", "HEAD"),
        _git(repo, "write-tree"),
        (repo / "tracked.txt").read_bytes(),
    )


def _python(script: str) -> tuple[str, ...]:
    """Python 명령 구성."""

    return (sys.executable, "-c", script)


class _Deadline:
    """제어 가능한 테스트 기한."""

    def __init__(self, seconds: float = 30.0) -> None:
        """남은 시간과 호출 횟수 초기화."""

        self.seconds = seconds
        self.calls = 0

    def remaining(self) -> float:
        """호출 횟수를 기록하고 남은 시간 반환."""

        self.calls += 1
        return self.seconds


class ApprovedBaseUnitTestRunnerTests(unittest.TestCase):
    """승인 기준본 단위 테스트 실행기의 동작과 경계 조건 테스트 모음."""

    def test_success_proves_base_tree_and_argv_in_a_cleaned_detached_clone(
        self,
    ) -> None:
        """성공 시 정리된 분리 복제본의 기준 트리와 명령 인수를 증명하는지 검증."""

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
                """하위 프로세스 호출 기록."""

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
        """테스트 성공에도 작업 트리·인덱스·HEAD 변경 시 실패하고 정리하는지 검증."""

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
        """0이 아닌 테스트 종료 시 정리 후 단위 테스트 실패 반환 검증."""

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
        """빈 명령과 완전하지 않은 기준 커밋의 설정 실패 판정 검증."""

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
        """해석할 수 없는 전체 커밋의 입력 실패 판정 검증."""

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
        """프로세스 시작 실패의 안정적 판정과 샌드박스 정리 검증."""

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
        """프로세스 트리 실패의 안정적 판정과 샌드박스 정리 검증."""

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
                """단위 테스트 프로세스 실패용 대체 동작."""

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
        """만료된 기한에서 하위 프로세스를 시작하지 않는지 검증."""

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
        """하위 프로세스 기한 초과 시 정리 후 기한 실패 반환 검증."""

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
                """테스트 프로세스만 기한 초과시키는 대체 동작."""

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
        """정리 실패가 성공을 샌드박스 실패로 대체하는지 검증."""

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
        """정리 실패가 제어된 테스트 실패보다 우선하는지 검증."""

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
        """정리 실패가 앞선 인프라 실패를 대체하지 않는지 검증."""

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
                """테스트 프로세스만 기한 초과시키는 대체 동작."""

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
        """최종 활성 저장소 지문 입출력 실패의 실행기 실패 판정 검증."""

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
                """최종 지문 조회만 실패시키는 테스트 대체 동작."""

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
        """최종 활성 저장소 지문 기한 초과의 워크플로 기한 실패 판정 검증."""

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
                """샌드박스를 정리한 뒤 기한 소진."""

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
        """활성 저장소 변경이 테스트 결과보다 우선하는지 검증."""

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
        """활성 저장소 변경이 정리 실패보다 우선하는지 검증."""

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
        """활성 저장소 내부의 산출물 루트 거부 검증."""

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
