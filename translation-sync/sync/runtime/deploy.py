"""이미 publication된 main 커밋의 배포 요청과 결과 검증."""

from __future__ import annotations

import json
import math
import os
import re
import secrets
import subprocess
import threading
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Protocol

from .deadline import DeadlineExceeded
from .failure import IssueCode
from .process import ProcessTreeError, run_process_tree


_FULL_OID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
_RUN_URL_ID = re.compile(r"/actions/runs/([1-9][0-9]*)(?:[/#?\s]|\Z)")
_REPOSITORY = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?"
    r"/[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?\Z"
)
_CORRELATION = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,30}\Z")
_NONCE = re.compile(r"[0-9a-f]{32}\Z")
_DEPLOY_ENV_KEYS = (
    "GITHUB_ENTERPRISE_TOKEN",
    "GITHUB_TOKEN",
    "GH_ENTERPRISE_TOKEN",
    "GH_HOST",
    "GH_TOKEN",
    "HTTPS_PROXY",
    "HTTP_PROXY",
    "LANG",
    "LC_ALL",
    "NO_PROXY",
    "PATH",
    "SSL_CERT_DIR",
    "SSL_CERT_FILE",
    "SYSTEMROOT",
    "TEMP",
    "TMP",
    "TMPDIR",
    "https_proxy",
    "http_proxy",
    "no_proxy",
)


class ArgvRunner(Protocol):
    """공유 기한을 적용하는 argv 명령 실행 경계."""

    def __call__(
        self,
        argv: Sequence[str],
        *,
        timeout: float,
    ) -> subprocess.CompletedProcess[str]:
        """지정한 timeout 안에서 argv 명령을 실행하고 결과 반환."""

        ...


class SubprocessArgvRunner:
    """명령 출력을 메모리에 보존하는 고정 argv 하위 프로세스 실행기."""

    def __init__(self, environment: Mapping[str, str] | None = None) -> None:
        """배포 명령에 허용된 환경 변수만 선택."""

        source = os.environ if environment is None else environment
        selected: dict[str, str] = {}
        for key in _DEPLOY_ENV_KEYS:
            value = source.get(key)
            if isinstance(value, str) and value:
                selected[key] = value
        self._environment = selected

    def __call__(
        self,
        argv: Sequence[str],
        *,
        timeout: float,
    ) -> subprocess.CompletedProcess[str]:
        """shell 없이 argv를 실행하고 텍스트 출력을 메모리에 보존."""

        return run_process_tree(
            list(argv),
            check=False,
            capture_output=True,
            text=True,
            shell=False,
            timeout=timeout,
            env=self._environment,
        )


@dataclass(frozen=True, slots=True)
class DeploymentRequest:
    """배포 결정에 필요한 branch와 publication 상태."""

    branch: str
    base_commit: str
    published_commit: str
    remote_commit: str
    has_changes: bool


@dataclass(frozen=True, slots=True)
class DeploymentResult:
    """배포 요청 수락 여부와 실행 검증 결과."""

    branch: str
    published_commit: str
    correlation_id: str | None = None
    dispatch_accepted: bool = False
    run_id: int | None = None
    conclusion: str | None = None
    issue_code: IssueCode | None = None
    published_commit_retained: bool = False

    @property
    def success(self) -> bool:
        """안정된 오류 없이 배포 단계가 끝났는지 여부."""

        return self.issue_code is None

    @property
    def triggered(self) -> bool:
        """GitHub의 workflow_dispatch 요청 수락 여부."""

        return self.dispatch_accepted


class _DeployTimeout(RuntimeError):
    """공유 워크플로 기한을 소진한 배포 작업."""

    pass


class _TriggerFailure(RuntimeError):
    """배포 대상 조회, workflow 요청 또는 실행 식별 실패."""

    pass


class _ValidationFailure(RuntimeError):
    """정확한 commit의 배포 성공을 확인하지 못한 상태."""

    pass


class DeploymentCoordinator:
    """단일 커밋의 deploy.yml dispatch와 정확한 신규 실행 대기.

    호출자는 publication 중 해석한 기준본, publication 결과 및 현재 원격 커밋 객체 ID 제공.
    세 값이 동일 커밋을 식별할 때만 no-change 재시도 허용.
    ``correlation_id``는 1~31자의 workflow-attempt 접두사.
    coordinator가 비공개 128비트 nonce를 붙여 dispatch 값을 최대 64자로 제한.
    deploy workflow의 ``translation-deploy:<id>-<nonce>`` run-name과 dispatch 값 대조.
    원격 변경과 rollback은 이 단계에서 미수행.
    """

    def __init__(
        self,
        *,
        repository: str,
        correlation_id: str,
        remaining_seconds: Callable[[], float],
        runner: ArgvRunner | None = None,
        sleep: Callable[[float], None] = time.sleep,
        workflow_file: str = "deploy.yml",
        poll_interval_seconds: float = 3.0,
        nonce_factory: Callable[[], str] | None = None,
    ) -> None:
        """배포 대상, 고유 correlation 및 polling 계약 검증·고정."""

        if not _REPOSITORY.fullmatch(repository):
            raise ValueError("repository must be an explicit owner/name")
        if not _CORRELATION.fullmatch(correlation_id):
            raise ValueError(
                "correlation_id must match [A-Za-z0-9][A-Za-z0-9._-]{0,30}"
            )
        nonce = (nonce_factory or (lambda: secrets.token_hex(16)))()
        if not isinstance(nonce, str) or not _NONCE.fullmatch(nonce):
            raise ValueError("nonce_factory must return 128-bit lowercase hex")
        if not workflow_file or workflow_file.startswith("-"):
            raise ValueError("workflow_file must be a non-option name")
        if (
            isinstance(poll_interval_seconds, bool)
            or not isinstance(poll_interval_seconds, (int, float))
            or not math.isfinite(float(poll_interval_seconds))
            or poll_interval_seconds <= 0
        ):
            raise ValueError("poll_interval_seconds must be positive and finite")
        self._repository = repository
        self._correlation_id = f"{correlation_id}-{nonce}"
        self._expected_run_name = f"translation-deploy:{self._correlation_id}"
        self._remaining_seconds = remaining_seconds
        self._runner = runner or SubprocessArgvRunner()
        self._sleep = sleep
        self._workflow_file = workflow_file
        self._poll_interval_seconds = float(poll_interval_seconds)
        self._use_lock = threading.Lock()
        self._used = False

    def deploy(self, request: DeploymentRequest) -> DeploymentResult:
        """main publication의 배포 요청과 정확한 commit 실행 결과 검증.

        다른 branch는 dispatch 없는 성공 결과 반환.
        """

        with self._use_lock:
            if self._used:
                raise RuntimeError("DeploymentCoordinator is one-shot")
            self._used = True
        if request.branch != "main":
            return DeploymentResult(
                branch=request.branch,
                published_commit=request.published_commit,
            )

        invalid_code = self._validate_publication(request)
        if invalid_code is not None:
            return DeploymentResult(
                branch=request.branch,
                published_commit=request.published_commit,
                correlation_id=self._correlation_id,
                issue_code=invalid_code,
            )

        triggered = False
        run_id: int | None = None
        try:
            current_remote = self._remote_main_commit()
            if current_remote != request.published_commit:
                return DeploymentResult(
                    branch=request.branch,
                    published_commit=request.published_commit,
                    correlation_id=self._correlation_id,
                    issue_code=IssueCode.PUBLICATION_BASE_CHANGED,
                    published_commit_retained=True,
                )
            trigger = self._command(
                (
                    "gh",
                    "workflow",
                    "run",
                    self._workflow_file,
                    "--ref",
                    "main",
                    "--raw-field",
                    f"expected_commit={request.published_commit}",
                    "--raw-field",
                    f"correlation_id={self._correlation_id}",
                    "--repo",
                    self._repository,
                ),
                failure_type=_TriggerFailure,
            )
            if trigger.returncode != 0:
                raise _TriggerFailure
            triggered = True

            run_id = self._triggered_run_id(trigger)
            if run_id is None:
                run_id = self._wait_for_correlated_run(request.published_commit)
            conclusion = self._wait_for_run(
                run_id=run_id,
                published_commit=request.published_commit,
            )
            return DeploymentResult(
                branch=request.branch,
                published_commit=request.published_commit,
                correlation_id=self._correlation_id,
                dispatch_accepted=True,
                run_id=run_id,
                conclusion=conclusion,
                published_commit_retained=True,
            )
        except _DeployTimeout:
            return DeploymentResult(
                branch=request.branch,
                published_commit=request.published_commit,
                correlation_id=self._correlation_id,
                dispatch_accepted=triggered,
                run_id=run_id,
                issue_code=IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
                published_commit_retained=True,
            )
        except _TriggerFailure:
            return DeploymentResult(
                branch=request.branch,
                published_commit=request.published_commit,
                correlation_id=self._correlation_id,
                dispatch_accepted=triggered,
                run_id=run_id,
                issue_code=IssueCode.DEPLOY_TRIGGER_FAILED,
                published_commit_retained=True,
            )
        except _ValidationFailure as exc:
            conclusion = str(exc) or None
            return DeploymentResult(
                branch=request.branch,
                published_commit=request.published_commit,
                correlation_id=self._correlation_id,
                dispatch_accepted=triggered,
                run_id=run_id,
                conclusion=conclusion,
                issue_code=IssueCode.DEPLOY_VALIDATION_FAILED,
                published_commit_retained=True,
            )

    @staticmethod
    def _validate_publication(request: DeploymentRequest) -> IssueCode | None:
        """변경 여부와 기준·publication·원격 commit 조합 검증."""

        oids = (
            request.base_commit,
            request.published_commit,
            request.remote_commit,
        )
        if (
            not isinstance(request.has_changes, bool)
            or not all(
                isinstance(oid, str) and _FULL_OID.fullmatch(oid)
                for oid in oids
            )
            or len({len(oid) for oid in oids}) != 1
        ):
            return IssueCode.INVALID_RUNTIME_OPTION
        if request.has_changes:
            if request.base_commit == request.published_commit:
                return IssueCode.INVALID_RUNTIME_OPTION
            if request.remote_commit != request.published_commit:
                return IssueCode.PUBLICATION_BASE_CHANGED
            return None
        if not (
            request.base_commit
            == request.published_commit
            == request.remote_commit
        ):
            return IssueCode.PUBLICATION_BASE_CHANGED
        return None

    def _remote_main_commit(self) -> str:
        """GitHub API에서 원격 main commit 객체 ID 조회."""

        result = self._command(
            (
                "gh",
                "api",
                f"repos/{self._repository}/git/ref/heads/main",
                "--jq",
                ".object.sha",
            ),
            failure_type=_TriggerFailure,
        )
        if result.returncode != 0:
            raise _TriggerFailure
        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if len(lines) != 1:
            raise _TriggerFailure
        commit = lines[0]
        if not _FULL_OID.fullmatch(commit):
            raise _TriggerFailure
        return commit

    @staticmethod
    def _triggered_run_id(
        result: subprocess.CompletedProcess[str],
    ) -> int | None:
        """workflow dispatch 출력에서 유일한 양수 실행 ID 추출."""

        output = "\n".join(
            part for part in (result.stdout, result.stderr) if isinstance(part, str)
        )
        run_ids = {int(match) for match in _RUN_URL_ID.findall(output)}
        if len(run_ids) > 1:
            raise _TriggerFailure
        return next(iter(run_ids)) if run_ids else None

    def _wait_for_correlated_run(self, published_commit: str) -> int:
        """정확한 run-name과 publication commit을 가진 신규 workflow 실행 대기."""

        while True:
            result = self._command(
                (
                    "gh",
                    "run",
                    "list",
                    "--workflow",
                    self._workflow_file,
                    "--branch",
                    "main",
                    "--event",
                    "workflow_dispatch",
                    "--commit",
                    published_commit,
                    "--limit",
                    "100",
                    "--json",
                    "databaseId,headSha,displayTitle",
                    "--repo",
                    self._repository,
                ),
                failure_type=_TriggerFailure,
            )
            if result.returncode != 0:
                raise _TriggerFailure
            matching = self._matching_correlated_run_ids(
                result.stdout,
                published_commit=published_commit,
            )
            if len(matching) == 1:
                return next(iter(matching))
            if len(matching) > 1:
                raise _TriggerFailure
            self._sleep(min(self._poll_interval_seconds, self._budget()))

    def _matching_correlated_run_ids(
        self,
        raw: str,
        *,
        published_commit: str,
    ) -> frozenset[int]:
        """workflow 목록에서 예상 run-name과 publication commit이 일치하는 실행 ID 선택."""

        try:
            payload = json.loads(raw)
        except (json.JSONDecodeError, TypeError) as exc:
            raise _TriggerFailure from exc
        if not isinstance(payload, list):
            raise _TriggerFailure
        matching: set[int] = set()
        for item in payload:
            if not isinstance(item, dict):
                raise _TriggerFailure
            run_id = item.get("databaseId")
            head_sha = item.get("headSha")
            title = item.get("displayTitle")
            if (
                isinstance(run_id, bool)
                or not isinstance(run_id, int)
                or run_id <= 0
                or not isinstance(head_sha, str)
                or not _FULL_OID.fullmatch(head_sha)
                or not isinstance(title, str)
            ):
                raise _TriggerFailure
            if (
                head_sha == published_commit
                and title == self._expected_run_name
            ):
                matching.add(run_id)
        return frozenset(matching)

    def _wait_for_run(self, *, run_id: int, published_commit: str) -> str:
        """지정 실행이 예상 run-name과 정확한 commit으로 성공 완료될 때까지 대기."""

        while True:
            state = self._view_run(run_id)
            if (
                state["databaseId"] != run_id
                or state["headSha"] != published_commit
                or state["displayTitle"] != self._expected_run_name
            ):
                raise _ValidationFailure
            status = state["status"]
            conclusion = state["conclusion"]
            if status == "completed":
                self._budget()
                if conclusion != "success":
                    raise _ValidationFailure(conclusion)
                return conclusion
            if conclusion is not None:
                raise _ValidationFailure(conclusion)
            self._sleep(min(self._poll_interval_seconds, self._budget()))

    def _view_run(self, run_id: int) -> dict[str, object]:
        """GitHub CLI에서 배포 실행 상태 조회 후 필수 필드 형식 검증."""

        result = self._command(
            (
                "gh",
                "run",
                "view",
                str(run_id),
                "--json",
                "databaseId,headSha,displayTitle,status,conclusion",
                "--repo",
                self._repository,
            ),
            failure_type=_ValidationFailure,
        )
        if result.returncode != 0:
            raise _ValidationFailure
        try:
            payload = json.loads(result.stdout)
        except (json.JSONDecodeError, TypeError) as exc:
            raise _ValidationFailure from exc
        if not isinstance(payload, dict):
            raise _ValidationFailure
        if (
            isinstance(payload.get("databaseId"), bool)
            or not isinstance(payload.get("databaseId"), int)
            or not isinstance(payload.get("headSha"), str)
            or not isinstance(payload.get("displayTitle"), str)
            or not isinstance(payload.get("status"), str)
            or (
                payload.get("conclusion") is not None
                and not isinstance(payload.get("conclusion"), str)
            )
        ):
            raise _ValidationFailure
        return payload

    def _command(
        self,
        argv: Sequence[str],
        *,
        failure_type: type[RuntimeError],
    ) -> subprocess.CompletedProcess[str]:
        """공유 기한 안에서 GitHub CLI 명령 실행."""

        try:
            return self._runner(argv, timeout=self._budget())
        except (subprocess.TimeoutExpired, DeadlineExceeded) as exc:
            raise _DeployTimeout from exc
        except (OSError, ProcessTreeError) as exc:
            raise failure_type from exc

    def _budget(self) -> float:
        """배포 단계에 사용할 양의 유한 잔여 시간 반환."""

        try:
            remaining = self._remaining_seconds()
        except DeadlineExceeded as exc:
            raise _DeployTimeout from exc
        if (
            isinstance(remaining, bool)
            or not isinstance(remaining, (int, float))
            or not math.isfinite(float(remaining))
            or remaining <= 0
        ):
            raise _DeployTimeout
        return float(remaining)
