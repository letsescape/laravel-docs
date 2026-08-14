"""후보 실행기 동작과 경계 조건 검증."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Callable, Mapping
from pathlib import Path
from unittest.mock import patch

from sync.runtime.candidate import (
    FAILURE_REPORT_ENV,
    PATH_FAILURE_REPORT_FILENAME,
    RUN_ID_ENV,
    SYNC_FAILURE_REPORT_FILENAME,
    WORKFLOW_DEADLINE_ENV,
    CandidateRunner,
)
from sync.runtime.failure import IssueCode
from sync.runtime.process import ProcessTreeCleanupError


def _git(repo: Path, *args: str) -> str:
    """Git 명령 실행."""

    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _init_repo(root: Path) -> str:
    """테스트용 Git 저장소 초기화."""

    root.mkdir()
    (root / ".gitignore").write_text(
        "build/\nnode_modules/\n",
        encoding="utf-8",
    )
    (root / "tracked.txt").write_text("approved\n", encoding="utf-8")
    _git(root, "init", "--quiet")
    _git(root, "config", "user.name", "Candidate Tests")
    _git(root, "config", "user.email", "candidate-tests@localhost")
    _git(root, "add", "-A")
    _git(root, "commit", "--quiet", "-m", "approved base")
    return _git(root, "rev-parse", "HEAD")


def _python(script: str) -> tuple[str, ...]:
    """Python 명령 구성."""

    return (sys.executable, "-c", script)


def _run_subprocess(
    *args: object,
    **kwargs: object,
) -> subprocess.CompletedProcess[bytes]:
    """하위 프로세스 실행."""

    check = kwargs.pop("check", False)
    return subprocess.run(  # type: ignore[call-overload]
        *args,
        check=check,
        **kwargs,
    )


_RUN_ID = "candidate-run-1"


def _runner(
    *,
    source_repo: Path,
    artifact_root: Path,
    remaining_seconds: Callable[[], float],
    sync_environment: Mapping[str, str] | None = None,
    sync_file_inputs: Mapping[str, bytes] | None = None,
    run_id: str = _RUN_ID,
) -> CandidateRunner:
    """테스트용 후보 실행기 구성."""

    return CandidateRunner(
        source_repo=source_repo,
        artifact_root=artifact_root,
        run_id=run_id,
        remaining_seconds=remaining_seconds,
        sync_environment=sync_environment,
        sync_file_inputs=sync_file_inputs,
        process_runner=_run_subprocess,
    )


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


class CandidateRuntimeTests(unittest.TestCase):
    """후보 실행기 동작과 경계 조건 테스트 모음."""

    def test_default_process_runner_uses_process_tree_isolation(self) -> None:
        """기본 프로세스 실행기의 프로세스 트리 격리 사용 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            completed = subprocess.CompletedProcess(
                ["command"],
                0,
                stdout=b"output",
                stderr=b"",
            )
            with patch(
                "sync.runtime.candidate.run_process_tree",
                return_value=completed,
            ) as run_process:
                runner = CandidateRunner(
                    source_repo=Path(tmp) / "repo",
                    artifact_root=Path(tmp) / "artifacts",
                    run_id=_RUN_ID,
                    remaining_seconds=_Deadline(5).remaining,
                )
                result = runner._process(
                    ("command",),
                    cwd=Path(tmp),
                    environment={"LANG": "C"},
                    capture_output=True,
                )

            self.assertIs(result, completed)
            run_process.assert_called_once_with(
                ["command"],
                cwd=Path(tmp),
                env={"LANG": "C"},
                check=False,
                timeout=5.0,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

    def test_process_tree_failure_is_a_runner_failure(self) -> None:
        """프로세스 트리 실패의 실행기 실패 판정 검증."""

        with (
            tempfile.TemporaryDirectory() as tmp,
            patch(
                "sync.runtime.candidate.run_process_tree",
                side_effect=ProcessTreeCleanupError("cleanup failed"),
            ),
        ):
            runner = CandidateRunner(
                source_repo=Path(tmp) / "repo",
                artifact_root=Path(tmp) / "artifacts",
                run_id=_RUN_ID,
                remaining_seconds=_Deadline().remaining,
            )
            result = runner.run(
                base_commit="a" * 40,
                setup_argvs=(_python("raise SystemExit(0)"),),
                sync_core_argv=_python("raise SystemExit(0)"),
                site_validator_argvs=(_python("raise SystemExit(0)"),),
                path_validator_argv=_python("raise SystemExit(0)"),
            )

        self.assertFalse(result.publication_allowed)
        self.assertIsNotNone(result.failure)
        assert result.failure is not None
        self.assertEqual(result.failure.stage, "approved-base")
        self.assertEqual(
            result.failure.issue_code,
            IssueCode.RUNNER_OPERATION_FAILED,
        )

    def test_success_seals_tree_without_moving_approved_base_head(self) -> None:
        """성공 시 승인된 기준 커밋을 이동하지 않고 트리를 봉인하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            artifacts = Path(tmp) / "artifacts"
            deadline = _Deadline()
            real_run = subprocess.run
            subprocess_calls: list[dict[str, object]] = []

            def run_with_recording(*args: object, **kwargs: object):
                """하위 프로세스 호출 기록."""

                subprocess_calls.append(kwargs.copy())
                return real_run(*args, **kwargs)

            runner = _runner(
                source_repo=source,
                artifact_root=artifacts,
                remaining_seconds=deadline.remaining,
            )
            with (
                patch.dict(os.environ, {"HUSKY": "1"}),
                patch(
                    "sync.runtime.candidate.subprocess.run",
                    side_effect=run_with_recording,
                ),
            ):
                result = runner.run(
                    base_commit=base,
                    setup_argvs=(
                        _python(
                            "import os; from pathlib import Path; "
                            "assert os.environ.get('HUSKY') == '0'; "
                            "Path('node_modules').mkdir(); "
                            "Path('node_modules/first').write_text('ready')"
                        ),
                        _python(
                            "from pathlib import Path; "
                            "assert Path('node_modules/first').read_text() == 'ready'; "
                            "Path('node_modules/second').write_text('ready')"
                        ),
                    ),
                    sync_core_argv=_python(
                        "from pathlib import Path; "
                        "assert Path('node_modules/second').read_text() == 'ready'; "
                        "Path('tracked.txt').write_text('candidate\\n')"
                    ),
                    site_validator_argvs=(
                        _python(
                            "from pathlib import Path; "
                            "assert Path('tracked.txt').read_text() == "
                            "'candidate\\n'; "
                            "Path('build').mkdir(); "
                            "Path('build/site.html').write_text('generated')"
                        ),
                    ),
                    path_validator_argv=_python(
                        "from pathlib import Path; "
                        "raise SystemExit("
                        "0 if Path('tracked.txt').read_text() == "
                        "'candidate\\n' else 9)"
                    ),
                )

            self.assertTrue(result.publication_allowed)
            self.assertTrue(result.has_changes)
            self.assertIsNone(result.failure)
            self.assertIsNotNone(result.sandbox)
            self.assertIsNotNone(result.verified_tree)
            assert result.sandbox is not None
            assert result.verified_tree is not None
            self.assertTrue(result.sandbox.is_relative_to(artifacts.resolve()))
            self.assertFalse(result.sandbox.is_relative_to(source.resolve()))
            self.assertEqual(_git(result.sandbox, "rev-parse", "HEAD"), base)
            self.assertEqual(_git(result.sandbox, "remote"), "")
            self.assertEqual(
                _git(result.sandbox, "write-tree"),
                result.verified_tree,
            )
            self.assertEqual(
                _git(result.sandbox, "show", f"{result.verified_tree}:tracked.txt"),
                "candidate",
            )
            self.assertNotIn(
                "build/site.html",
                _git(
                    result.sandbox,
                    "ls-tree",
                    "-r",
                    "--name-only",
                    result.verified_tree,
                ),
            )
            self.assertFalse((result.sandbox / "build").exists())
            self.assertFalse((result.sandbox / "node_modules").exists())
            self.assertEqual(
                (source / "tracked.txt").read_text(encoding="utf-8"),
                "approved\n",
            )
            self.assertGreater(deadline.calls, 0)
            self.assertTrue(subprocess_calls)
            self.assertTrue(
                all(
                    isinstance(call.get("timeout"), (int, float))
                    and float(call["timeout"]) <= deadline.seconds
                    for call in subprocess_calls
                )
            )
            self.assertTrue(
                all(call.get("shell", False) is False for call in subprocess_calls)
            )

    def test_only_safe_node_options_are_exposed_to_validators(self) -> None:
        """검증기에 안전한 Node 옵션만 노출하고 기본 heap 값을 보장하는지 검증."""

        cases = (
            ("--max-old-space-size=4096", "--max-old-space-size=4096"),
            ("--require=/tmp/untrusted.js", "--max-old-space-size=4096"),
        )
        for ambient, expected in cases:
            with self.subTest(ambient=ambient), tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / "repo"
                base = _init_repo(source)
                runner = _runner(
                    source_repo=source,
                    artifact_root=Path(tmp) / "artifacts",
                    remaining_seconds=_Deadline().remaining,
                )
                validator = _python(
                    "import os; "
                    f"raise SystemExit(0 if os.environ.get('NODE_OPTIONS', '') == "
                    f"{expected!r} else 9)"
                )

                with patch.dict(os.environ, {"NODE_OPTIONS": ambient}):
                    result = runner.run(
                        base_commit=base,
                        setup_argvs=(
                            _python(
                                "import os; "
                                "assert 'NODE_OPTIONS' not in os.environ; "
                                "assert os.environ.get('HUSKY') == '0'"
                            ),
                        ),
                        sync_core_argv=_python(
                            "import os; "
                            "raise SystemExit("
                            "1 if 'NODE_OPTIONS' in os.environ else 0)"
                        ),
                        site_validator_argvs=(validator,),
                        path_validator_argv=validator,
                    )

                self.assertTrue(result.publication_allowed)

    def test_only_workflow_deadline_is_added_to_validator_environment(self) -> None:
        """검증기 환경에 워크플로 기한만 추가하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            deadline = "12345.25"
            runner = _runner(
                source_repo=source,
                artifact_root=Path(tmp) / "artifacts",
                remaining_seconds=_Deadline().remaining,
                sync_environment={
                    WORKFLOW_DEADLINE_ENV: deadline,
                    "UNRELATED_VALIDATOR_SECRET": "must-not-leak",
                },
            )
            setup = _python(
                "import os; "
                f"assert {WORKFLOW_DEADLINE_ENV!r} not in os.environ; "
                "assert 'UNRELATED_VALIDATOR_SECRET' not in os.environ"
            )
            sync_core = _python(
                "import os; "
                f"assert os.environ.get({WORKFLOW_DEADLINE_ENV!r}) == "
                f"{deadline!r}; "
                "assert os.environ.get('UNRELATED_VALIDATOR_SECRET') == "
                "'must-not-leak'"
            )
            validator = _python(
                "import os; "
                f"assert os.environ.get({WORKFLOW_DEADLINE_ENV!r}) == "
                f"{deadline!r}; "
                "assert 'UNRELATED_VALIDATOR_SECRET' not in os.environ; "
                "assert 'AMBIENT_VALIDATOR_SECRET' not in os.environ"
            )

            with patch.dict(
                os.environ,
                {
                    WORKFLOW_DEADLINE_ENV: "99999.0",
                    "AMBIENT_VALIDATOR_SECRET": "must-not-leak",
                },
            ):
                result = runner.run(
                    base_commit=base,
                    setup_argvs=(setup,),
                    sync_core_argv=sync_core,
                    site_validator_argvs=(validator,),
                    path_validator_argv=validator,
                )

            self.assertTrue(result.publication_allowed)

    def test_no_change_returns_base_tree_and_false_change_flag(self) -> None:
        """변경이 없을 때 기준 트리와 거짓 변경 플래그 반환 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            runner = _runner(
                source_repo=source,
                artifact_root=Path(tmp) / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )

            result = runner.run(
                base_commit=base,
                setup_argvs=(_python("raise SystemExit(0)"),),
                sync_core_argv=_python("raise SystemExit(0)"),
                site_validator_argvs=(_python("raise SystemExit(0)"),),
                path_validator_argv=_python("raise SystemExit(0)"),
            )

            self.assertTrue(result.publication_allowed)
            self.assertFalse(result.has_changes)
            self.assertIsNotNone(result.sandbox)
            assert result.sandbox is not None
            self.assertEqual(
                result.verified_tree,
                _git(result.sandbox, "rev-parse", f"{base}^{{tree}}"),
            )

    def test_clone_uses_approved_base_instead_of_active_worktree_changes(self) -> None:
        """복제본이 활성 작업 트리 변경 대신 승인된 기준본을 사용하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            (source / "tracked.txt").write_text(
                "active dirty state\n", encoding="utf-8"
            )
            runner = _runner(
                source_repo=source,
                artifact_root=Path(tmp) / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )

            result = runner.run(
                base_commit=base,
                setup_argvs=(_python("raise SystemExit(0)"),),
                sync_core_argv=_python(
                    "from pathlib import Path; "
                    "raise SystemExit("
                    "0 if Path('tracked.txt').read_text() == 'approved\\n' else 9)"
                ),
                site_validator_argvs=(_python("raise SystemExit(0)"),),
                path_validator_argv=_python("raise SystemExit(0)"),
            )

            self.assertTrue(result.publication_allowed)
            self.assertFalse(result.has_changes)
            self.assertEqual(
                (source / "tracked.txt").read_text(encoding="utf-8"),
                "active dirty state\n",
            )

    def test_artifact_root_inside_source_is_rejected_without_subprocess(self) -> None:
        """원문 저장소 내부의 산출물 루트를 하위 프로세스 실행 전에 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            artifacts = source / "candidate-artifacts"
            runner = _runner(
                source_repo=source,
                artifact_root=artifacts,
                remaining_seconds=_Deadline().remaining,
            )

            with patch("sync.runtime.candidate.subprocess.run") as run:
                result = runner.run(
                    base_commit=base,
                    setup_argvs=(_python("raise SystemExit(0)"),),
                    sync_core_argv=_python("raise SystemExit(0)"),
                    site_validator_argvs=(_python("raise SystemExit(0)"),),
                    path_validator_argv=_python("raise SystemExit(0)"),
                )

            run.assert_not_called()
            self.assertFalse(result.publication_allowed)
            self.assertFalse(artifacts.exists())
            self.assertIsNotNone(result.failure)
            assert result.failure is not None
            self.assertEqual(
                result.failure.issue_code,
                IssueCode.SANDBOX_OPERATION_FAILED,
            )

    def test_invalid_run_id_is_rejected_before_subprocess(self) -> None:
        """잘못된 실행 ID를 하위 프로세스 실행 전에 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            artifacts = Path(tmp) / "artifacts"
            runner = _runner(
                source_repo=source,
                artifact_root=artifacts,
                run_id="../not-a-run-id",
                remaining_seconds=_Deadline().remaining,
            )

            with patch("sync.runtime.candidate.subprocess.run") as run:
                result = runner.run(
                    base_commit=base,
                    setup_argvs=(_python("raise SystemExit(0)"),),
                    sync_core_argv=_python("raise SystemExit(0)"),
                    site_validator_argvs=(_python("raise SystemExit(0)"),),
                    path_validator_argv=_python("raise SystemExit(0)"),
                )

            run.assert_not_called()
            self.assertFalse(result.publication_allowed)
            self.assertIsNotNone(result.failure)
            assert result.failure is not None
            self.assertEqual(
                result.failure.issue_code,
                IssueCode.INVALID_RUNTIME_OPTION,
            )
            self.assertFalse(artifacts.exists())

    def test_uppercase_base_oid_is_rejected_before_subprocess(self) -> None:
        """대문자가 포함된 비정규 기준 OID를 하위 프로세스 실행 전에 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            artifacts = Path(tmp) / "artifacts"
            runner = _runner(
                source_repo=source,
                artifact_root=artifacts,
                remaining_seconds=_Deadline().remaining,
            )

            with patch("sync.runtime.candidate.subprocess.run") as run:
                result = runner.run(
                    base_commit=base.upper(),
                    setup_argvs=(_python("raise SystemExit(0)"),),
                    sync_core_argv=_python("raise SystemExit(0)"),
                    site_validator_argvs=(_python("raise SystemExit(0)"),),
                    path_validator_argv=_python("raise SystemExit(0)"),
                )

            run.assert_not_called()
            self.assertFalse(result.publication_allowed)
            self.assertIsNotNone(result.failure)
            assert result.failure is not None
            self.assertEqual(
                result.failure.issue_code,
                IssueCode.INVALID_RUNTIME_OPTION,
            )
            self.assertFalse(artifacts.exists())

    def test_existing_child_report_target_is_not_replaced(self) -> None:
        """기존 하위 작업 보고서 경로를 교체하지 않는지 검증."""

        for filename in (
            SYNC_FAILURE_REPORT_FILENAME,
            PATH_FAILURE_REPORT_FILENAME,
        ):
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / "repo"
                base = _init_repo(source)
                artifacts = Path(tmp) / "artifacts"
                artifacts.mkdir()
                report = artifacts / filename
                report.write_text("existing", encoding="utf-8")
                runner = _runner(
                    source_repo=source,
                    artifact_root=artifacts,
                    remaining_seconds=_Deadline().remaining,
                )

                with patch("sync.runtime.candidate.subprocess.run") as run:
                    result = runner.run(
                        base_commit=base,
                        setup_argvs=(_python("raise SystemExit(0)"),),
                        sync_core_argv=_python("raise SystemExit(0)"),
                        site_validator_argvs=(_python("raise SystemExit(0)"),),
                        path_validator_argv=_python("raise SystemExit(0)"),
                    )

                run.assert_not_called()
                self.assertFalse(result.publication_allowed)
                self.assertIsNotNone(result.failure)
                assert result.failure is not None
                self.assertEqual(
                    result.failure.issue_code,
                    IssueCode.INVALID_RUNTIME_OPTION,
                )
                self.assertEqual(report.read_text(encoding="utf-8"), "existing")

    def test_setup_tracked_source_mutation_blocks_sync(self) -> None:
        """준비 명령의 추적 파일 변경 시 동기화 차단 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            runner = _runner(
                source_repo=source,
                artifact_root=Path(tmp) / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )

            result = runner.run(
                base_commit=base,
                setup_argvs=(
                    _python(
                        "from pathlib import Path; "
                        "Path('tracked.txt').write_text('setup mutation\\n')"
                    ),
                    _python(
                        "from pathlib import Path; "
                        "Path('second-setup-ran').write_text('yes')"
                    ),
                ),
                sync_core_argv=_python(
                    "from pathlib import Path; Path('sync-ran').write_text('yes')"
                ),
                site_validator_argvs=(_python("raise SystemExit(0)"),),
                path_validator_argv=_python("raise SystemExit(0)"),
            )

            self.assertFalse(result.publication_allowed)
            self.assertIsNotNone(result.failure)
            assert result.failure is not None
            self.assertEqual(result.failure.stage, "candidate-setup")
            self.assertEqual(
                result.failure.issue_code,
                IssueCode.CANDIDATE_SOURCE_MUTATED,
            )
            self.assertIsNotNone(result.sandbox)
            assert result.sandbox is not None
            self.assertFalse((result.sandbox / "second-setup-ran").exists())
            self.assertFalse((result.sandbox / "sync-ran").exists())

    def test_setup_failure_blocks_sync_with_runner_issue(self) -> None:
        """준비 실패 시 실행기 문제로 동기화 차단 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            runner = _runner(
                source_repo=source,
                artifact_root=Path(tmp) / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )

            result = runner.run(
                base_commit=base,
                setup_argvs=(_python("raise SystemExit(7)"),),
                sync_core_argv=_python(
                    "from pathlib import Path; Path('sync-ran').write_text('yes')"
                ),
                site_validator_argvs=(_python("raise SystemExit(0)"),),
                path_validator_argv=_python("raise SystemExit(0)"),
            )

            self.assertFalse(result.publication_allowed)
            self.assertIsNotNone(result.failure)
            assert result.failure is not None
            self.assertEqual(result.failure.stage, "candidate-setup")
            self.assertEqual(
                result.failure.issue_code,
                IssueCode.RUNNER_OPERATION_FAILED,
            )
            self.assertEqual(result.failure.returncode, 7)
            self.assertIsNotNone(result.sandbox)
            assert result.sandbox is not None
            self.assertFalse((result.sandbox / "sync-ran").exists())

    def test_empty_setup_commands_are_rejected_before_clone(self) -> None:
        """빈 준비 명령을 저장소 복제 전에 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            artifacts = Path(tmp) / "artifacts"
            runner = _runner(
                source_repo=source,
                artifact_root=artifacts,
                remaining_seconds=_Deadline().remaining,
            )

            result = runner.run(
                base_commit=base,
                setup_argvs=(),
                sync_core_argv=_python("raise SystemExit(0)"),
                site_validator_argvs=(_python("raise SystemExit(0)"),),
                path_validator_argv=_python("raise SystemExit(0)"),
            )

            self.assertFalse(result.publication_allowed)
            self.assertIsNone(result.sandbox)
            self.assertIsNotNone(result.failure)
            assert result.failure is not None
            self.assertEqual(
                result.failure.issue_code,
                IssueCode.REQUIRED_CONFIG_MISSING,
            )
            self.assertFalse(artifacts.exists())

    def test_site_validator_mutation_blocks_tree_seal(self) -> None:
        """사이트 검증기가 추적 파일을 변경하면 트리 봉인을 차단하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            runner = _runner(
                source_repo=source,
                artifact_root=Path(tmp) / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )

            result = runner.run(
                base_commit=base,
                setup_argvs=(_python("raise SystemExit(0)"),),
                sync_core_argv=_python(
                    "from pathlib import Path; "
                    "Path('tracked.txt').write_text('candidate\\n')"
                ),
                site_validator_argvs=(
                    _python(
                        "from pathlib import Path; "
                        "Path('tracked.txt').write_text('validator mutation\\n')"
                    ),
                ),
                path_validator_argv=_python("raise SystemExit(0)"),
            )

            self.assertFalse(result.publication_allowed)
            self.assertIsNone(result.verified_tree)
            self.assertIsNotNone(result.failure)
            assert result.failure is not None
            self.assertEqual(
                result.failure.issue_code,
                IssueCode.CANDIDATE_SOURCE_MUTATED,
            )

    def test_validator_failures_do_not_produce_a_verified_tree(self) -> None:
        """검증 실패 시 검증된 트리를 생성하지 않는지 검증."""

        cases = (
            (
                (_python("raise SystemExit(4)"),),
                _python("raise SystemExit(0)"),
                "site-validation",
                IssueCode.SITE_VALIDATION_FAILED,
                None,
            ),
            (
                (_python("raise SystemExit(0)"),),
                _python("raise SystemExit(5)"),
                "path-validation",
                None,
                PATH_FAILURE_REPORT_FILENAME,
            ),
        )
        for site_commands, path_command, stage, issue_code, report_filename in cases:
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / "repo"
                base = _init_repo(source)
                artifacts = (Path(tmp) / "artifacts").resolve()
                runner = _runner(
                    source_repo=source,
                    artifact_root=artifacts,
                    remaining_seconds=_Deadline().remaining,
                )

                result = runner.run(
                    base_commit=base,
                    setup_argvs=(_python("raise SystemExit(0)"),),
                    sync_core_argv=_python(
                        "from pathlib import Path; "
                        "Path('tracked.txt').write_text('candidate\\n')"
                    ),
                    site_validator_argvs=site_commands,
                    path_validator_argv=path_command,
                )

                self.assertFalse(result.publication_allowed)
                self.assertIsNone(result.verified_tree)
                self.assertIsNotNone(result.failure)
                assert result.failure is not None
                self.assertEqual(result.failure.stage, stage)
                self.assertEqual(result.failure.issue_code, issue_code)
                self.assertEqual(
                    result.failure.report_path,
                    artifacts / report_filename
                    if report_filename is not None
                    else None,
                )

    def test_child_environments_separate_credentials_and_failure_reports(self) -> None:
        """하위 작업 환경에서 자격 증명과 실패 보고서를 분리하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            artifacts = (Path(tmp) / "artifacts").resolve()
            sync_report = artifacts / SYNC_FAILURE_REPORT_FILENAME
            path_report = artifacts / PATH_FAILURE_REPORT_FILENAME
            runner = _runner(
                source_repo=source,
                artifact_root=artifacts,
                remaining_seconds=_Deadline().remaining,
                sync_environment={
                    "OPENAI_API_KEY": "synthetic-provider-key",
                    FAILURE_REPORT_ENV: "/caller/must/not/select/report.json",
                    RUN_ID_ENV: "caller-must-not-select-run-id",
                },
            )

            result = runner.run(
                base_commit=base,
                setup_argvs=(
                    _python(
                        "import os; "
                        "assert os.environ.get('HUSKY') == '0'; "
                        "assert 'OPENAI_API_KEY' not in os.environ; "
                        f"assert {FAILURE_REPORT_ENV!r} not in os.environ; "
                        f"assert {RUN_ID_ENV!r} not in os.environ"
                    ),
                ),
                sync_core_argv=_python(
                    "import os; from pathlib import Path; "
                    "assert os.environ.get('OPENAI_API_KEY') == "
                    "'synthetic-provider-key'; "
                    f"assert os.environ.get({FAILURE_REPORT_ENV!r}) == "
                    f"{str(sync_report)!r}; "
                    f"assert os.environ.get({RUN_ID_ENV!r}) == {_RUN_ID!r}; "
                    "Path('tracked.txt').write_text('candidate\\n')"
                ),
                site_validator_argvs=(
                    _python(
                        "import os; "
                        "assert 'OPENAI_API_KEY' not in os.environ; "
                        f"assert {FAILURE_REPORT_ENV!r} not in os.environ; "
                        f"assert {RUN_ID_ENV!r} not in os.environ"
                    ),
                ),
                path_validator_argv=_python(
                    "import os; "
                    "assert 'OPENAI_API_KEY' not in os.environ; "
                    f"assert os.environ.get({FAILURE_REPORT_ENV!r}) == "
                    f"{str(path_report)!r}; "
                    f"assert os.environ.get({RUN_ID_ENV!r}) == {_RUN_ID!r}"
                ),
            )

            self.assertTrue(result.publication_allowed)
            self.assertTrue(result.has_changes)

    def test_sync_file_input_is_exact_read_only_candidate_git_file(self) -> None:
        """동기화 입력을 후보 Git 디렉터리의 정확한 읽기 전용 파일로 생성하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            canonical_manifest = b'{"schema_version":1,"entries":[]}\n'
            runner = _runner(
                source_repo=source,
                artifact_root=Path(tmp) / "artifacts",
                remaining_seconds=_Deadline().remaining,
                sync_environment={
                    "TRANSLATION_UPSTREAM_MANIFEST": "/caller/path/is-forbidden"
                },
                sync_file_inputs={"TRANSLATION_UPSTREAM_MANIFEST": canonical_manifest},
            )

            result = runner.run(
                base_commit=base,
                setup_argvs=(
                    _python(
                        "import os; "
                        "assert 'TRANSLATION_UPSTREAM_MANIFEST' not in os.environ"
                    ),
                ),
                sync_core_argv=_python(
                    "import os; from pathlib import Path; "
                    "path = Path(os.environ['TRANSLATION_UPSTREAM_MANIFEST']); "
                    "root = Path.cwd().resolve(); "
                    "assert path.is_relative_to(root / '.git'); "
                    f"assert path.read_bytes() == {canonical_manifest!r}; "
                    "assert path.stat().st_mode & 0o777 == 0o400"
                ),
                site_validator_argvs=(
                    _python(
                        "import os; "
                        "assert 'TRANSLATION_UPSTREAM_MANIFEST' not in os.environ"
                    ),
                ),
                path_validator_argv=_python(
                    "import os; "
                    "assert 'TRANSLATION_UPSTREAM_MANIFEST' not in os.environ"
                ),
            )

            self.assertTrue(result.publication_allowed)
            assert result.sandbox is not None
            self.assertEqual(
                _git(result.sandbox, "status", "--porcelain", "--untracked-files=all"),
                "",
            )

    def test_sync_file_inputs_reject_unknown_keys_and_non_bytes_before_clone(
        self,
    ) -> None:
        """알 수 없는 키와 바이트가 아닌 동기화 입력을 복제 전에 거부하는지 검증."""

        for inputs in (
            {"../TRANSLATION_UPSTREAM_MANIFEST": b"manifest"},
            {"TRANSLATION_UPSTREAM_MANIFEST": "not-bytes"},
        ):
            with self.subTest(inputs=inputs), tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / "repo"
                base = _init_repo(source)
                artifacts = Path(tmp) / "artifacts"
                runner = _runner(
                    source_repo=source,
                    artifact_root=artifacts,
                    remaining_seconds=_Deadline().remaining,
                    sync_file_inputs=inputs,  # type: ignore[arg-type]
                )

                with patch("sync.runtime.candidate.subprocess.run") as run:
                    result = runner.run(
                        base_commit=base,
                        setup_argvs=(_python("raise SystemExit(0)"),),
                        sync_core_argv=_python("raise SystemExit(0)"),
                        site_validator_argvs=(_python("raise SystemExit(0)"),),
                        path_validator_argv=_python("raise SystemExit(0)"),
                    )

                run.assert_not_called()
                self.assertFalse(result.publication_allowed)
                assert result.failure is not None
                self.assertEqual(
                    result.failure.issue_code,
                    IssueCode.INVALID_RUNTIME_OPTION,
                )
                self.assertFalse(artifacts.exists())

    def test_sync_file_input_rejects_symlink_or_existing_staging_directory(
        self,
    ) -> None:
        """동기화 입력 준비 디렉터리의 심볼릭 링크 또는 선점을 거부하는지 검증."""

        for attack in ("symlink", "existing"):
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / "repo"
                base = _init_repo(source)
                external = Path(tmp) / "external"
                external.mkdir()
                runner = _runner(
                    source_repo=source,
                    artifact_root=Path(tmp) / "artifacts",
                    remaining_seconds=_Deadline().remaining,
                    sync_file_inputs={"TRANSLATION_UPSTREAM_MANIFEST": b"canonical\n"},
                )
                real_populate = runner._populate_clone

                def populate_with_attack(
                    sandbox: Path,
                    commit: str,
                    *,
                    populate=real_populate,
                    attack_kind=attack,
                    external_path=external,
                ) -> None:
                    """공격용 준비 디렉터리 구성."""

                    populate(sandbox, commit)
                    staging = sandbox / ".git/translation-candidate-inputs"
                    if attack_kind == "symlink":
                        staging.symlink_to(
                            external_path,
                            target_is_directory=True,
                        )
                    else:
                        staging.mkdir()

                with patch.object(
                    runner,
                    "_populate_clone",
                    side_effect=populate_with_attack,
                ):
                    result = runner.run(
                        base_commit=base,
                        setup_argvs=(_python("raise SystemExit(0)"),),
                        sync_core_argv=_python("raise SystemExit(0)"),
                        site_validator_argvs=(_python("raise SystemExit(0)"),),
                        path_validator_argv=_python("raise SystemExit(0)"),
                    )

                self.assertFalse(result.publication_allowed)
                assert result.failure is not None
                self.assertEqual(
                    result.failure.issue_code,
                    IssueCode.RUNNER_OPERATION_FAILED,
                )
                self.assertEqual(list(external.iterdir()), [])

    def test_successful_child_must_not_leave_a_failure_report(self) -> None:
        """성공한 하위 작업이 실패 보고서를 남기면 거부하는지 검증."""

        cases = (
            ("sync-core", True, SYNC_FAILURE_REPORT_FILENAME),
            ("path-validation", False, PATH_FAILURE_REPORT_FILENAME),
        )
        for stage, sync_writes, filename in cases:
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / "repo"
                base = _init_repo(source)
                artifacts = Path(tmp) / "artifacts"
                write_report = _python(
                    "import os; from pathlib import Path; "
                    f"Path(os.environ[{FAILURE_REPORT_ENV!r}]).write_text('{{}}')"
                )
                runner = _runner(
                    source_repo=source,
                    artifact_root=artifacts,
                    remaining_seconds=_Deadline().remaining,
                )

                result = runner.run(
                    base_commit=base,
                    setup_argvs=(_python("raise SystemExit(0)"),),
                    sync_core_argv=(
                        write_report if sync_writes else _python("raise SystemExit(0)")
                    ),
                    site_validator_argvs=(_python("raise SystemExit(0)"),),
                    path_validator_argv=(
                        _python("raise SystemExit(0)") if sync_writes else write_report
                    ),
                )

                self.assertFalse(result.publication_allowed)
                self.assertIsNotNone(result.failure)
                assert result.failure is not None
                self.assertEqual(result.failure.stage, stage)
                self.assertEqual(
                    result.failure.issue_code,
                    IssueCode.UNCLASSIFIED_INTERNAL,
                )
                self.assertTrue((artifacts / filename).exists())

    def test_expired_deadline_starts_no_subprocess(self) -> None:
        """만료된 기한에서 하위 프로세스를 시작하지 않는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            runner = _runner(
                source_repo=source,
                artifact_root=Path(tmp) / "artifacts",
                remaining_seconds=_Deadline(0).remaining,
            )

            with patch("sync.runtime.candidate.subprocess.run") as run:
                result = runner.run(
                    base_commit=base,
                    setup_argvs=(_python("raise SystemExit(0)"),),
                    sync_core_argv=_python("raise SystemExit(0)"),
                    site_validator_argvs=(_python("raise SystemExit(0)"),),
                    path_validator_argv=_python("raise SystemExit(0)"),
                )

            run.assert_not_called()
            self.assertFalse(result.publication_allowed)
            self.assertIsNone(result.sandbox)
            self.assertIsNotNone(result.failure)
            assert result.failure is not None
            self.assertEqual(
                result.failure.issue_code,
                IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            )

    def test_empty_sync_command_is_rejected_before_clone(self) -> None:
        """빈 동기화 명령을 저장소 복제 전에 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            artifacts = Path(tmp) / "artifacts"
            runner = _runner(
                source_repo=source,
                artifact_root=artifacts,
                remaining_seconds=_Deadline().remaining,
            )

            result = runner.run(
                base_commit=base,
                setup_argvs=(_python("raise SystemExit(0)"),),
                sync_core_argv=(),
                site_validator_argvs=(_python("raise SystemExit(0)"),),
                path_validator_argv=_python("raise SystemExit(0)"),
            )

            self.assertFalse(result.publication_allowed)
            self.assertIsNone(result.sandbox)
            self.assertIsNotNone(result.failure)
            assert result.failure is not None
            self.assertEqual(
                result.failure.issue_code,
                IssueCode.REQUIRED_CONFIG_MISSING,
            )
            self.assertFalse(artifacts.exists())

    def test_sync_failure_stops_before_validators_and_seal(self) -> None:
        """동기화 실패 시 검증과 트리 봉인 전에 중단하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            runner = _runner(
                source_repo=source,
                artifact_root=Path(tmp) / "artifacts",
                remaining_seconds=_Deadline().remaining,
            )

            result = runner.run(
                base_commit=base,
                setup_argvs=(_python("raise SystemExit(0)"),),
                sync_core_argv=_python(
                    "import os; from pathlib import Path; "
                    f"Path(os.environ[{FAILURE_REPORT_ENV!r}]).write_text("
                    "'child report'); "
                    "raise SystemExit(6)"
                ),
                site_validator_argvs=(
                    _python(
                        "from pathlib import Path; "
                        "Path('validator-ran').write_text('yes')"
                    ),
                ),
                path_validator_argv=_python("raise SystemExit(0)"),
            )

            self.assertFalse(result.publication_allowed)
            self.assertIsNone(result.verified_tree)
            self.assertIsNotNone(result.failure)
            assert result.failure is not None
            self.assertEqual(result.failure.stage, "sync-core")
            self.assertIsNone(result.failure.issue_code)
            self.assertEqual(result.failure.returncode, 6)
            self.assertEqual(
                result.failure.report_path,
                (Path(tmp) / "artifacts").resolve() / SYNC_FAILURE_REPORT_FILENAME,
            )
            assert result.failure.report_path is not None
            self.assertEqual(
                result.failure.report_path.read_text(encoding="utf-8"),
                "child report",
            )
            self.assertIsNotNone(result.sandbox)
            assert result.sandbox is not None
            self.assertFalse((result.sandbox / "validator-ran").exists())


if __name__ == "__main__":
    unittest.main()
