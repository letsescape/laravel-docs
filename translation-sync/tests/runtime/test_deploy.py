"""배포 조정기 동작과 경계 조건 검증."""

from __future__ import annotations

import json
import subprocess
import unittest
from collections.abc import Sequence
from unittest.mock import patch

from sync.runtime.deploy import (
    DeploymentCoordinator,
    DeploymentRequest,
    SubprocessArgvRunner,
)
from sync.runtime.failure import IssueCode
from sync.runtime.process import ProcessTreeCleanupError


BASE = "a" * 40
PUBLISHED = "b" * 40
REPOSITORY = "laravelkr/docs"
CORRELATION = "sync-12345-1"
NONCE = "0123456789abcdef0123456789abcdef"
DISPATCH_CORRELATION = f"{CORRELATION}-{NONCE}"
RUN_NAME = f"translation-deploy:{DISPATCH_CORRELATION}"


def _completed(
    argv: Sequence[str],
    *,
    returncode: int = 0,
    stdout: str = "",
) -> subprocess.CompletedProcess[str]:
    """테스트용 완료된 프로세스 결과 구성."""

    return subprocess.CompletedProcess(
        list(argv),
        returncode,
        stdout=stdout,
        stderr="",
    )


class _FakeRunner:
    """응답을 순서대로 반환하는 가짜 실행기."""

    def __init__(self, responses: Sequence[object]) -> None:
        """반환할 응답과 호출 기록 초기화."""

        self.responses = list(responses)
        self.calls: list[tuple[tuple[str, ...], float]] = []

    def __call__(
        self,
        argv: Sequence[str],
        *,
        timeout: float,
    ) -> subprocess.CompletedProcess[str]:
        """호출을 기록하고 다음 응답 반환."""

        self.calls.append((tuple(argv), timeout))
        if not self.responses:
            raise AssertionError(f"unexpected command: {argv!r}")
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        assert isinstance(response, subprocess.CompletedProcess)
        return response


def _trigger_url(run_id: int) -> str:
    """GitHub Actions 실행 URL 구성."""

    return f"https://github.com/laravelkr/docs/actions/runs/{run_id}\n"


class DeploymentCoordinatorTests(unittest.TestCase):
    """배포 조정기 동작과 경계 조건 테스트 모음."""

    def _coordinator(self, runner: _FakeRunner) -> DeploymentCoordinator:
        """테스트용 배포 조정기 구성."""

        return DeploymentCoordinator(
            repository=REPOSITORY,
            correlation_id=CORRELATION,
            nonce_factory=lambda: NONCE,
            runner=runner,
            remaining_seconds=lambda: 30.0,
            sleep=lambda _seconds: None,
        )

    def test_non_main_branch_never_triggers_or_queries_deploy(self) -> None:
        """main이 아닌 브랜치에서 배포를 실행하거나 조회하지 않는지 검증."""

        runner = _FakeRunner([])
        request = DeploymentRequest(
            branch="feature/docs",
            base_commit=BASE,
            published_commit=PUBLISHED,
            remote_commit=PUBLISHED,
            has_changes=True,
        )

        result = self._coordinator(runner).deploy(request)

        self.assertTrue(result.success)
        self.assertFalse(result.triggered)
        self.assertIsNone(result.run_id)
        self.assertEqual(runner.calls, [])

    def test_process_tree_failure_is_a_stable_trigger_failure(self) -> None:
        """프로세스 트리 실패를 안정적 배포 실행 실패로 판정하는지 검증."""

        runner = _FakeRunner(
            [ProcessTreeCleanupError("private cleanup detail")]
        )

        result = self._coordinator(runner).deploy(
            DeploymentRequest(
                branch="main",
                base_commit=BASE,
                published_commit=PUBLISHED,
                remote_commit=PUBLISHED,
                has_changes=True,
            )
        )

        self.assertEqual(result.issue_code, IssueCode.DEPLOY_TRIGGER_FAILED)
        self.assertFalse(result.dispatch_accepted)
        self.assertTrue(result.published_commit_retained)
        self.assertEqual(len(runner.calls), 1)

    def test_coordinator_is_one_shot_so_its_nonce_cannot_be_reused(self) -> None:
        """일회용 조정기의 nonce를 재사용할 수 없는지 검증."""

        runner = _FakeRunner([])
        coordinator = self._coordinator(runner)
        request = DeploymentRequest(
            branch="feature/docs",
            base_commit=BASE,
            published_commit=PUBLISHED,
            remote_commit=PUBLISHED,
            has_changes=True,
        )

        coordinator.deploy(request)

        with self.assertRaisesRegex(RuntimeError, "one-shot"):
            coordinator.deploy(request)
        self.assertEqual(runner.calls, [])

    def test_no_change_main_requires_base_published_and_remote_to_match(self) -> None:
        """변경 없는 main 배포 시 기준·게시·원격 커밋 일치 요구 검증."""

        cases = (
            DeploymentRequest(
                branch="main",
                base_commit=BASE,
                published_commit=PUBLISHED,
                remote_commit=BASE,
                has_changes=False,
            ),
            DeploymentRequest(
                branch="main",
                base_commit=BASE,
                published_commit=BASE,
                remote_commit=PUBLISHED,
                has_changes=False,
            ),
        )

        for request in cases:
            with self.subTest(request=request):
                runner = _FakeRunner([])
                result = self._coordinator(runner).deploy(request)

                self.assertFalse(result.success)
                self.assertEqual(
                    result.issue_code,
                    IssueCode.PUBLICATION_BASE_CHANGED,
                )
                self.assertFalse(result.triggered)
                self.assertEqual(runner.calls, [])

    def test_no_change_main_can_retry_deploy_for_the_unchanged_base(self) -> None:
        """변경 없는 main 기준 커밋의 배포를 재시도할 수 있는지 검증."""

        runner = _FakeRunner(
            [
                _completed(("gh", "api"), stdout=f"{BASE}\n"),
                _completed(
                    ("gh", "workflow", "run"),
                    stdout=_trigger_url(412),
                ),
                _completed(
                    ("gh", "run", "view"),
                    stdout=json.dumps(
                        {
                            "databaseId": 412,
                            "headSha": BASE,
                            "displayTitle": RUN_NAME,
                            "status": "queued",
                            "conclusion": None,
                        }
                    ),
                ),
                _completed(
                    ("gh", "run", "view"),
                    stdout=json.dumps(
                        {
                            "databaseId": 412,
                            "headSha": BASE,
                            "displayTitle": RUN_NAME,
                            "status": "completed",
                            "conclusion": "success",
                        }
                    ),
                ),
            ]
        )
        request = DeploymentRequest(
            branch="main",
            base_commit=BASE,
            published_commit=BASE,
            remote_commit=BASE,
            has_changes=False,
        )

        result = self._coordinator(runner).deploy(request)

        self.assertTrue(result.success)
        self.assertTrue(result.triggered)
        self.assertEqual(result.run_id, 412)
        self.assertEqual(result.conclusion, "success")
        self.assertEqual(
            runner.calls[0][0],
            (
                "gh",
                "api",
                f"repos/{REPOSITORY}/git/ref/heads/main",
                "--jq",
                ".object.sha",
            ),
        )
        self.assertEqual(
            runner.calls[1][0],
            (
                "gh",
                "workflow",
                "run",
                "deploy.yml",
                "--ref",
                "main",
                "--raw-field",
                f"expected_commit={BASE}",
                "--raw-field",
                f"correlation_id={DISPATCH_CORRELATION}",
                "--repo",
                REPOSITORY,
            ),
        )
        self.assertEqual(
            runner.calls[2][0],
            (
                "gh",
                "run",
                "view",
                "412",
                "--json",
                "databaseId,headSha,displayTitle,status,conclusion",
                "--repo",
                REPOSITORY,
            ),
        )
        self.assertEqual(
            runner.calls[3][0],
            (
                "gh",
                "run",
                "view",
                "412",
                "--json",
                "databaseId,headSha,displayTitle,status,conclusion",
                "--repo",
                REPOSITORY,
            ),
        )
        self.assertTrue(all(timeout <= 30 for _, timeout in runner.calls))

    def test_changed_main_requires_remote_to_equal_published_commit(self) -> None:
        """변경된 main 배포 시 원격과 게시 커밋의 일치 요구 검증."""

        runner = _FakeRunner([])
        result = self._coordinator(runner).deploy(
            DeploymentRequest(
                branch="main",
                base_commit=BASE,
                published_commit=PUBLISHED,
                remote_commit=BASE,
                has_changes=True,
            )
        )

        self.assertFalse(result.success)
        self.assertEqual(result.issue_code, IssueCode.PUBLICATION_BASE_CHANGED)
        self.assertEqual(runner.calls, [])

    def test_changed_publication_rejects_the_base_as_its_result_commit(self) -> None:
        """변경된 게시 결과로 기준 커밋을 반환하면 거부하는지 검증."""

        runner = _FakeRunner([])

        result = self._coordinator(runner).deploy(
            DeploymentRequest(
                branch="main",
                base_commit=BASE,
                published_commit=BASE,
                remote_commit=BASE,
                has_changes=True,
            )
        )

        self.assertFalse(result.success)
        self.assertEqual(result.issue_code, IssueCode.INVALID_RUNTIME_OPTION)
        self.assertEqual(runner.calls, [])

    def test_request_rejects_mixed_git_object_formats(self) -> None:
        """요청에 서로 다른 Git 개체 형식을 섞으면 거부하는지 검증."""

        runner = _FakeRunner([])

        result = self._coordinator(runner).deploy(
            DeploymentRequest(
                branch="main",
                base_commit=BASE,
                published_commit="b" * 64,
                remote_commit="b" * 64,
                has_changes=True,
            )
        )

        self.assertFalse(result.success)
        self.assertEqual(result.issue_code, IssueCode.INVALID_RUNTIME_OPTION)
        self.assertEqual(runner.calls, [])

    def test_trigger_failure_is_distinct_from_deploy_validation_failure(self) -> None:
        """배포 실행 실패와 배포 검증 실패를 구분하는지 검증."""

        trigger_argv = ("gh", "workflow", "run", "deploy.yml", "--ref", "main")
        runner = _FakeRunner(
            [
                _completed(("gh", "api"), stdout=f"{PUBLISHED}\n"),
                _completed(trigger_argv, returncode=1),
            ]
        )

        result = self._coordinator(runner).deploy(
            DeploymentRequest(
                branch="main",
                base_commit=BASE,
                published_commit=PUBLISHED,
                remote_commit=PUBLISHED,
                has_changes=True,
            )
        )

        self.assertFalse(result.success)
        self.assertEqual(result.issue_code, IssueCode.DEPLOY_TRIGGER_FAILED)
        self.assertIsNone(result.run_id)
        self.assertTrue(result.published_commit_retained)

    def test_failed_run_conclusion_keeps_published_commit(self) -> None:
        """실패한 실행 결과에도 게시 커밋을 유지하는지 검증."""

        runner = _FakeRunner(
            [
                _completed((), stdout=f"{PUBLISHED}\n"),
                _completed((), stdout=_trigger_url(801)),
                _completed(
                    (),
                    stdout=json.dumps(
                        {
                            "databaseId": 801,
                            "headSha": PUBLISHED,
                            "displayTitle": RUN_NAME,
                            "status": "in_progress",
                            "conclusion": None,
                        }
                    ),
                ),
                _completed(
                    (),
                    stdout=json.dumps(
                        {
                            "databaseId": 801,
                            "headSha": PUBLISHED,
                            "displayTitle": RUN_NAME,
                            "status": "completed",
                            "conclusion": "failure",
                        }
                    ),
                ),
            ]
        )

        result = self._coordinator(runner).deploy(
            DeploymentRequest(
                branch="main",
                base_commit=BASE,
                published_commit=PUBLISHED,
                remote_commit=PUBLISHED,
                has_changes=True,
            )
        )

        self.assertFalse(result.success)
        self.assertEqual(result.issue_code, IssueCode.DEPLOY_VALIDATION_FAILED)
        self.assertEqual(result.run_id, 801)
        self.assertEqual(result.conclusion, "failure")
        self.assertTrue(result.published_commit_retained)

    def test_success_requires_completed_success_for_exact_commit_and_run(
        self,
    ) -> None:
        """성공 판정에 정확한 커밋과 실행의 완료 성공 상태를 요구하는지 검증."""

        runner = _FakeRunner(
            [
                _completed((), stdout=f"{PUBLISHED}\n"),
                _completed((), stdout=_trigger_url(42)),
                _completed(
                    (),
                    stdout=json.dumps(
                        {
                            "databaseId": 42,
                            "headSha": PUBLISHED,
                            "displayTitle": RUN_NAME,
                            "status": "queued",
                            "conclusion": None,
                        }
                    ),
                ),
                _completed(
                    (),
                    stdout=json.dumps(
                        {
                            "databaseId": 42,
                            "headSha": BASE,
                            "displayTitle": RUN_NAME,
                            "status": "completed",
                            "conclusion": "success",
                        }
                    ),
                ),
            ]
        )

        result = self._coordinator(runner).deploy(
            DeploymentRequest(
                branch="main",
                base_commit=BASE,
                published_commit=PUBLISHED,
                remote_commit=PUBLISHED,
                has_changes=True,
            )
        )

        self.assertFalse(result.success)
        self.assertEqual(result.issue_code, IssueCode.DEPLOY_VALIDATION_FAILED)
        self.assertEqual(result.run_id, 42)
        self.assertTrue(result.published_commit_retained)

    def test_run_poll_timeout_is_reported_as_common_workflow_deadline(self) -> None:
        """실행 조회 제한 시간을 공통 워크플로 기한 초과로 보고하는지 검증."""

        runner = _FakeRunner(
            [
                _completed((), stdout=f"{PUBLISHED}\n"),
                _completed((), stdout=_trigger_url(77)),
                _completed(
                    (),
                    stdout=json.dumps(
                        {
                            "databaseId": 77,
                            "headSha": PUBLISHED,
                            "displayTitle": RUN_NAME,
                            "status": "queued",
                            "conclusion": None,
                        }
                    ),
                ),
                subprocess.TimeoutExpired(["gh", "run", "view", "77"], 9),
            ]
        )

        result = self._coordinator(runner).deploy(
            DeploymentRequest(
                branch="main",
                base_commit=BASE,
                published_commit=PUBLISHED,
                remote_commit=PUBLISHED,
                has_changes=True,
            )
        )

        self.assertFalse(result.success)
        self.assertEqual(
            result.issue_code,
            IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
        )
        self.assertEqual(result.run_id, 77)
        self.assertTrue(result.published_commit_retained)
        self.assertFalse(
            any("revert" in part for argv, _timeout in runner.calls for part in argv)
        )

    def test_correlation_finds_exact_run_when_trigger_url_is_unavailable(
        self,
    ) -> None:
        """실행 URL이 없을 때 상관관계 정보로 정확한 실행을 찾는지 검증."""

        runner = _FakeRunner(
            [
                _completed((), stdout=f"{PUBLISHED}\n"),
                _completed((), stdout="workflow dispatch accepted\n"),
                _completed(
                    (),
                    stdout=json.dumps(
                        [
                            {
                                "databaseId": 66,
                                "headSha": PUBLISHED,
                                "displayTitle": RUN_NAME,
                            }
                        ]
                    ),
                ),
                _completed(
                    (),
                    stdout=json.dumps(
                        {
                            "databaseId": 66,
                            "headSha": PUBLISHED,
                            "displayTitle": RUN_NAME,
                            "status": "completed",
                            "conclusion": "success",
                        }
                    ),
                ),
            ]
        )

        result = self._coordinator(runner).deploy(
            DeploymentRequest(
                branch="main",
                base_commit=BASE,
                published_commit=PUBLISHED,
                remote_commit=PUBLISHED,
                has_changes=True,
            )
        )

        self.assertTrue(result.success)
        self.assertEqual(result.run_id, 66)
        self.assertEqual(result.correlation_id, DISPATCH_CORRELATION)
        self.assertTrue(result.dispatch_accepted)
        self.assertTrue(result.triggered)
        self.assertEqual(
            runner.calls[2][0],
            (
                "gh",
                "run",
                "list",
                "--workflow",
                "deploy.yml",
                "--branch",
                "main",
                "--event",
                "workflow_dispatch",
                "--commit",
                PUBLISHED,
                "--limit",
                "100",
                "--json",
                "databaseId,headSha,displayTitle",
                "--repo",
                REPOSITORY,
            ),
        )

    def test_correlation_fallback_refuses_multiple_matching_run_ids(self) -> None:
        """상관관계 대체 조회에서 일치하는 실행 ID가 여러 개면 거부하는지 검증."""

        runner = _FakeRunner(
            [
                _completed((), stdout=f"{PUBLISHED}\n"),
                _completed((), stdout="workflow dispatch accepted\n"),
                _completed(
                    (),
                    stdout=json.dumps(
                        [
                            {
                                "databaseId": run_id,
                                "headSha": PUBLISHED,
                                "displayTitle": RUN_NAME,
                            }
                            for run_id in (66, 67)
                        ]
                    ),
                ),
            ]
        )

        result = self._coordinator(runner).deploy(
            DeploymentRequest(
                branch="main",
                base_commit=BASE,
                published_commit=PUBLISHED,
                remote_commit=PUBLISHED,
                has_changes=True,
            )
        )

        self.assertFalse(result.success)
        self.assertEqual(result.issue_code, IssueCode.DEPLOY_TRIGGER_FAILED)
        self.assertTrue(result.dispatch_accepted)
        self.assertIsNone(result.run_id)

    def test_remote_main_is_rechecked_immediately_before_dispatch(self) -> None:
        """배포 요청 직전에 원격 main을 다시 확인하는지 검증."""

        runner = _FakeRunner(
            [
                _completed((), stdout=f"{'c' * 40}\n"),
            ]
        )

        result = self._coordinator(runner).deploy(
            DeploymentRequest(
                branch="main",
                base_commit=BASE,
                published_commit=PUBLISHED,
                remote_commit=PUBLISHED,
                has_changes=True,
            )
        )

        self.assertFalse(result.success)
        self.assertEqual(result.issue_code, IssueCode.PUBLICATION_BASE_CHANGED)
        self.assertFalse(result.triggered)
        self.assertEqual(len(runner.calls), 1)

    def test_success_after_the_absolute_deadline_is_still_a_timeout(self) -> None:
        """절대 기한 뒤의 성공도 기한 초과로 판정하는지 검증."""

        runner = _FakeRunner(
            [
                _completed((), stdout=f"{PUBLISHED}\n"),
                _completed((), stdout=_trigger_url(91)),
                _completed(
                    (),
                    stdout=json.dumps(
                        {
                            "databaseId": 91,
                            "headSha": PUBLISHED,
                            "displayTitle": RUN_NAME,
                            "status": "queued",
                            "conclusion": None,
                        }
                    ),
                ),
                _completed(
                    (),
                    stdout=json.dumps(
                        {
                            "databaseId": 91,
                            "headSha": PUBLISHED,
                            "displayTitle": RUN_NAME,
                            "status": "completed",
                            "conclusion": "success",
                        }
                    ),
                ),
            ]
        )
        remaining = iter((30.0, 29.0, 28.0, 27.0, 26.0, 0.0))
        coordinator = DeploymentCoordinator(
            repository=REPOSITORY,
            correlation_id=CORRELATION,
            nonce_factory=lambda: NONCE,
            runner=runner,
            remaining_seconds=lambda: next(remaining),
            sleep=lambda _seconds: None,
        )

        result = coordinator.deploy(
            DeploymentRequest(
                branch="main",
                base_commit=BASE,
                published_commit=PUBLISHED,
                remote_commit=PUBLISHED,
                has_changes=True,
            )
        )

        self.assertFalse(result.success)
        self.assertEqual(
            result.issue_code,
            IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
        )
        self.assertEqual(result.run_id, 91)

    def test_repository_is_explicit_and_cannot_be_inferred_from_cwd(self) -> None:
        """배포 저장소를 명시해야 하며 현재 디렉터리에서 추론하지 않는지 검증."""

        for repository in ("", "owner", "../owner/repo", "owner/repo/extra"):
            with self.subTest(repository=repository):
                with self.assertRaises(ValueError):
                    DeploymentCoordinator(
                        repository=repository,
                        correlation_id=CORRELATION,
                        nonce_factory=lambda: NONCE,
                        runner=_FakeRunner([]),
                        remaining_seconds=lambda: 30.0,
                    )

    def test_correlation_id_must_be_an_explicit_safe_token(self) -> None:
        """상관관계 ID에 명시적인 안전 토큰을 요구하는지 검증."""

        for correlation_id in (
            "",
            " has-space",
            "slash/value",
            "with:colon",
            "_invalid-first",
            "x" * 32,
        ):
            with self.subTest(correlation_id=correlation_id):
                with self.assertRaises(ValueError):
                    DeploymentCoordinator(
                        repository=REPOSITORY,
                        correlation_id=correlation_id,
                        nonce_factory=lambda: NONCE,
                        runner=_FakeRunner([]),
                        remaining_seconds=lambda: 30.0,
                    )

    def test_31_character_prefix_and_nonce_form_a_64_character_input(self) -> None:
        """31자 접두사와 nonce가 64자 입력을 구성하는지 검증."""

        prefix = "a" + "._-" * 10
        self.assertEqual(len(prefix), 31)
        coordinator = DeploymentCoordinator(
            repository=REPOSITORY,
            correlation_id=prefix,
            nonce_factory=lambda: NONCE,
            runner=_FakeRunner([]),
            remaining_seconds=lambda: 30.0,
        )

        result = coordinator.deploy(
            DeploymentRequest(
                branch="main",
                base_commit=BASE,
                published_commit=BASE,
                remote_commit=BASE,
                has_changes=True,
            )
        )

        self.assertEqual(result.issue_code, IssueCode.INVALID_RUNTIME_OPTION)
        self.assertEqual(result.correlation_id, f"{prefix}-{NONCE}")
        assert result.correlation_id is not None
        self.assertEqual(len(result.correlation_id), 64)

    def test_injected_nonce_must_preserve_the_unique_correlation_contract(
        self,
    ) -> None:
        """주입한 nonce가 고유 상관관계 계약을 보존하는지 검증."""

        for nonce in ("", "f" * 31, "g" * 32, "F" * 32):
            with self.subTest(nonce=nonce):
                with self.assertRaises(ValueError):
                    DeploymentCoordinator(
                        repository=REPOSITORY,
                        correlation_id=CORRELATION,
                        nonce_factory=lambda nonce=nonce: nonce,
                        runner=_FakeRunner([]),
                        remaining_seconds=lambda: 30.0,
                    )


class SubprocessArgvRunnerTests(unittest.TestCase):
    """하위 프로세스 인수 실행기 동작과 경계 조건 테스트 모음."""

    def test_runner_uses_explicit_argv_without_shell_or_output_logging(
        self,
    ) -> None:
        """명시적 인수 배열을 사용하고 셸 실행이나 출력 로깅을 하지 않는지 검증."""

        completed = subprocess.CompletedProcess(
            ["gh", "run", "list"],
            0,
            stdout="[]",
            stderr="",
        )
        with patch(
            "sync.runtime.deploy.run_process_tree",
            return_value=completed,
        ) as run:
            result = SubprocessArgvRunner(
                environment={
                    "PATH": "/usr/bin",
                    "GH_TOKEN": "deployment-token",
                    "OPENAI_API_KEY": "must-not-be-inherited",
                }
            )(
                ("gh", "run", "list"),
                timeout=12.5,
            )

        self.assertIs(result, completed)
        run.assert_called_once_with(
            ["gh", "run", "list"],
            check=False,
            capture_output=True,
            text=True,
            shell=False,
            timeout=12.5,
            env={
                "PATH": "/usr/bin",
                "GH_TOKEN": "deployment-token",
            },
        )


if __name__ == "__main__":
    unittest.main()
