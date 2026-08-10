"""candidate runtime 동작과 경계 조건 검증."""

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
    """Git 처리."""

    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _init_repo(root: Path) -> str:
    """init repo 처리."""

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
    """python 처리."""

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
    """runner 처리."""

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
    """기한 객체."""

    def __init__(self, seconds: float = 30.0) -> None:
        """기한 초기화."""

        self.seconds = seconds
        self.calls = 0

    def remaining(self) -> float:
        """남은 처리."""

        self.calls += 1
        return self.seconds


class CandidateRuntimeTests(unittest.TestCase):
    """candidate runtime 동작과 경계 조건 테스트 모음."""

    def test_default_process_runner_uses_process_tree_isolation(self) -> None:
        """`default_process_runner`의 프로세스 tree isolation 사용 검증."""

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
        """`process_tree_failure`의 runner 실패 판정 검증."""

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
        """`success_seals_tree_without_moving_approved_base_head` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repo"
            base = _init_repo(source)
            artifacts = Path(tmp) / "artifacts"
            deadline = _Deadline()
            real_run = subprocess.run
            subprocess_calls: list[dict[str, object]] = []

            def run_with_recording(*args: object, **kwargs: object):
                """with recording 실행."""

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
        """`only_safe_node_options_are_exposed_to_validators` 시나리오 검증."""

        cases = (
            ("--max-old-space-size=4096", "--max-old-space-size=4096"),
            ("--require=/tmp/untrusted.js", ""),
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
        """`only_workflow_deadline`의 added 후 validator 환경 판정 검증."""

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
        """`no_change`의 기준본 tree 및 false 변경 flag 반환 검증."""

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
        """`clone`의 승인된 기준본 instead of 활성 worktree 변경 사용 검증."""

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
        """`artifact_root_inside_source`의 rejected 제외 하위 프로세스 판정 검증."""

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
        """`invalid_run_id`의 하위 프로세스 전 rejected 판정 검증."""

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
        """대문자가 포함된 비정규 base OID의 사전 거부 검증."""

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
        """`existing_child_report_target`의 않음 replaced 판정 검증."""

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
        """`setup_tracked_source_mutation`의 동기화 차단 검증."""

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
        """`setup_failure`의 동기화 포함 runner 문제 차단 검증."""

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
        """`empty_setup_commands_are_rejected_before_clone` 시나리오 검증."""

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
        """`site_validator_mutation`의 tree seal 차단 검증."""

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
        """`validator_failures_do_not_produce_a_verified_tree` 시나리오 검증."""

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
        """`child_environments_separate`의 보고 경계 검증."""

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
        """`sync_file_input`의 exact read 만 candidate Git 파일 판정 검증."""

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
        """`sync_file_inputs` 관련 경계 조건 검증."""

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
        """`sync_file_input`의 symlink 또는 existing staging 디렉터리 거부 검증."""

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
                    """공격용 staging entry가 포함된 clone 구성."""

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
        """`successful_child_must_not_leave_a_failure_report` 시나리오 검증."""

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
        """`expired_deadline_starts_no_subprocess` 시나리오 검증."""

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
        """`empty_sync_command`의 clone 전 rejected 판정 검증."""

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
        """`sync_failure`의 validators and seal 전 중단 검증."""

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
