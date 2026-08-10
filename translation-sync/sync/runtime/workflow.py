"""봉인된 publication 준비를 위한 fail-closed orchestration.

준비 프로세스는 단계 순서만 소유.
replay, candidate 생성, publication 및 배포는 독립 검증 가능한 계약을 가진 deep module로 유지.
이 모듈은 detached commit을 준비하지만 push와 배포 trigger는 미수행.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import math
import os
import re
import secrets
import stat
import subprocess
import time
import unicodedata
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Protocol
from urllib.parse import urlsplit

from ..common.versions import load_versions, validate_version_token
from ..source import upstream
from ..verification.response_contract import RESPONSE_CONTRACT_VERSION
from .base import (
    ApprovedPublicationBase,
    RepositoryStateError,
    active_repository_fingerprint,
    capture_publication_base,
)
from .candidate import (
    PATH_FAILURE_REPORT_FILENAME,
    SYNC_FAILURE_REPORT_FILENAME,
    CandidateResult,
    CandidateRunner,
)
from .config import (
    PROVIDER_BUDGET_PROFILE_VERSION,
    Config,
    ConfigError,
    load_config,
    provider_config_sha256,
    provider_model_profile,
)
from .deadline import DeadlineExceeded, WorkflowDeadline
from .failure import (
    REPORT_FILENAME,
    ErrorClassification,
    ExitCode,
    FailureEvent,
    FailureReport,
    IssueCode,
    ProviderAttempts,
    classification_for,
    final_exit_code,
    write_failure_report,
)
from .publication import (
    PreparedPublication,
    PublicationBase,
    PublicationError,
    Publisher,
)
from .process import ProcessTreeError, run_process_tree
from .settings import WorkflowSettings
from .unit_test import ApprovedBaseUnitTestResult, ApprovedBaseUnitTestRunner


PREPARED_STATE_FILENAME = "translation-sync-prepared.json"
REPLAY_STATE_FILENAME = "translation-sync-replay.json"
MANIFEST_FILENAME = "translation-sync-manifest.json"
PREPARATION_KEY_FILENAME = ".translation-sync-preparation-key"
REPLAY_FAILURE_FILENAME = "translation-sync-replay-failure.json"
FIXTURE_FAILURE_FILENAME = "translation-sync-fixture-failure.json"
FIXTURE_EVIDENCE_FILENAME = "translation-sync-fixture-evidence.txt"
PUBLISHED_STATE_FILENAME = "translation-sync-published.json"
DEPLOYED_STATE_FILENAME = "translation-sync-deployed.json"
WORKFLOW_DEADLINE_ENV = "TRANSLATION_WORKFLOW_DEADLINE_MONOTONIC"
RUN_DEADLINE_ENV = "TRANSLATION_RUN_DEADLINE_MONOTONIC"
MANIFEST_ENV = "TRANSLATION_UPSTREAM_MANIFEST"
MANIFEST_DIGEST_ENV = "TRANSLATION_UPSTREAM_MANIFEST_DIGEST"
SELECTOR_ENV = "TRANSLATION_SELECTOR_JSON"
SELECTOR_DIGEST_ENV = "TRANSLATION_SELECTOR_DIGEST"
FAILURE_REPORT_ENV = "TRANSLATION_FAILURE_REPORT"
RUN_ID_ENV = "TRANSLATION_RUN_ID"

_BASE_ENVIRONMENT_KEYS = frozenset(
    {
        "CI",
        "ALL_PROXY",
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
        "UV_CACHE_DIR",
        "https_proxy",
        "http_proxy",
        "no_proxy",
    }
)
_PREPARE_GIT_IDENTITY = {
    "GIT_AUTHOR_NAME": "translation-sync",
    "GIT_AUTHOR_EMAIL": "translation-sync@localhost",
    "GIT_COMMITTER_NAME": "translation-sync",
    "GIT_COMMITTER_EMAIL": "translation-sync@localhost",
}
_DEPLOY_REPOSITORY = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?"
    r"/[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?\Z"
)
_DEPLOY_HOST = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9.-]{0,251}[A-Za-z0-9])?"
    r"(?::[1-9][0-9]{0,4})?\Z"
)


def _deployment_host_for(push_endpoint: str, deploy_repository: str) -> str:
    """push endpoint와 배포 저장소에서 검증된 호스트 추출."""

    if not isinstance(push_endpoint, str) or not isinstance(
        deploy_repository,
        str,
    ):
        raise ValueError("deployment target must be textual")
    try:
        parsed = urlsplit(push_endpoint)
        port = parsed.port
    except ValueError as exc:
        raise ValueError("push endpoint is invalid") from exc
    if (
        parsed.scheme != "https"
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or parsed.hostname is None
        or parsed.path != f"/{deploy_repository}.git"
    ):
        raise ValueError("push endpoint does not match deployment repository")
    host = parsed.hostname.lower()
    if port is not None:
        if port > 65535:
            raise ValueError("deployment host port is invalid")
        host = f"{host}:{port}"
    if not _DEPLOY_HOST.fullmatch(host):
        raise ValueError("deployment host is invalid")
    return host


class WorkflowStageError(RuntimeError):
    """단일 orchestration 경계에서 반환하는 비식별 안정 실패."""

    def __init__(
        self,
        *,
        stage: str,
        code: IssueCode,
        message: str,
        attempts: ProviderAttempts | None = None,
        candidate_debug_path: str | None = None,
        reported_failures: tuple[FailureEvent, ...] | None = None,
    ) -> None:
        """워크플로 단계 오류 초기화."""

        self.stage = stage
        self.code = code
        self.message = message
        self.attempts = attempts
        self.candidate_debug_path = candidate_debug_path
        self.reported_failures = reported_failures
        super().__init__(code.value)


@dataclass(frozen=True, slots=True)
class ReplaySnapshot:
    """identity replay가 확정한 manifest와 selector 증거."""

    manifest: bytes
    manifest_digest: str
    selector: bytes
    selector_digest: str

    def __post_init__(self) -> None:
        """snapshot payload와 SHA-256 digest의 일치 확인."""

        for name, payload, digest in (
            ("manifest", self.manifest, self.manifest_digest),
            ("selector", self.selector, self.selector_digest),
        ):
            if not isinstance(payload, bytes) or not payload:
                raise ValueError(f"{name} must be non-empty bytes")
            if (
                not isinstance(digest, str)
                or len(digest) != 64
                or any(character not in "0123456789abcdef" for character in digest)
                or hashlib.sha256(payload).hexdigest() != digest
            ):
                raise ValueError(f"{name} digest mismatch")


@dataclass(frozen=True, slots=True)
class PrepareRequest:
    """publication 준비 단계의 불변 입력."""

    repository: Path
    artifact_root: Path
    push_endpoint: str
    deploy_repository: str
    branch: str
    commit_message: str
    version: str | None = None
    document: str | None = None


@dataclass(frozen=True, slots=True)
class PrepareOutcome:
    """publication 준비 단계의 종료 상태와 증거 경로."""

    exit_code: ExitCode
    state_path: Path | None = None
    report_path: Path | None = None
    failure_code: IssueCode | None = None


class CaptureBase(Protocol):
    """승인 publication 기준본 캡처 경계."""

    def __call__(
        self,
        request: PrepareRequest,
        remaining_seconds: Callable[[], float],
    ) -> ApprovedPublicationBase:
        """현재 실행의 승인 publication 기준본 반환."""

        ...


class RunUnitTests(Protocol):
    """승인 기준본 단위 테스트 실행 경계."""

    def __call__(
        self,
        request: PrepareRequest,
        base: ApprovedPublicationBase,
        argv: tuple[str, ...],
        remaining_seconds: Callable[[], float],
    ) -> ApprovedBaseUnitTestResult:
        """격리된 승인 기준본의 단위 테스트 증거 반환."""

        ...


class RunReplay(Protocol):
    """identity replay 실행 및 스냅샷 반환 경계."""

    def __call__(
        self,
        request: PrepareRequest,
        argv: tuple[str, ...],
        output_path: Path,
        environment: Mapping[str, str],
        remaining_seconds: Callable[[], float],
    ) -> ReplaySnapshot:
        """replay 명령 실행 후 manifest와 selector 스냅샷 반환."""

        ...


class RunCommandStage(Protocol):
    """증거 바이트를 반환하는 하위 명령 단계 경계."""

    def __call__(
        self,
        request: PrepareRequest,
        argv: tuple[str, ...],
        environment: Mapping[str, str],
        remaining_seconds: Callable[[], float],
    ) -> bytes:
        """공유 기한 안에서 명령을 실행하고 증거 바이트 반환."""

        ...


class BuildCandidate(Protocol):
    """격리 candidate 생성과 검증 경계."""

    def __call__(
        self,
        request: PrepareRequest,
        base: ApprovedPublicationBase,
        setup_argvs: tuple[tuple[str, ...], ...],
        sync_argv: tuple[str, ...],
        site_argvs: tuple[tuple[str, ...], ...],
        path_argv: tuple[str, ...],
        environment: Mapping[str, str],
        remaining_seconds: Callable[[], float],
    ) -> CandidateResult:
        """검증된 candidate 또는 안정된 실패 결과 반환."""

        ...


class PreparePublication(Protocol):
    """검증된 candidate의 publication 준비 경계."""

    def __call__(
        self,
        request: PrepareRequest,
        base: ApprovedPublicationBase,
        candidate: CandidateResult,
        preparation_key: bytes,
        remaining_seconds: Callable[[], float],
    ) -> PreparedPublication:
        """candidate tree와 commit을 봉인한 publication 증거 반환."""

        ...


class ReadActiveFingerprint(Protocol):
    """활성 저장소 fingerprint 재검증 경계."""

    def __call__(
        self,
        request: PrepareRequest,
        remaining_seconds: Callable[[], float],
    ) -> str:
        """현재 활성 저장소 fingerprint 반환."""

        ...


@dataclass(frozen=True, slots=True)
class WorkflowHooks:
    """preparer가 순서대로 호출하는 외부 단계 어댑터 집합."""

    capture_base: CaptureBase
    run_unit_tests: RunUnitTests
    run_replay: RunReplay
    run_provider_fixture: RunCommandStage
    build_candidate: BuildCandidate
    prepare_publication: PreparePublication
    read_active_fingerprint: ReadActiveFingerprint


def _format_deadline(value: float) -> str:
    """단조 시계 기한을 손실 없는 환경 변수 문자열로 형식화."""

    if not math.isfinite(value):
        raise ValueError("deadline must be finite")
    return format(value, ".17g")


def _canonical_json(value: Mapping[str, object]) -> bytes:
    """mapping을 키가 정렬되고 공백이 제거된 JSON 바이트로 직렬화."""

    return (
        json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _write_no_replace(path: Path, contents: bytes) -> Path:
    """기존 파일과 symlink를 덮어쓰지 않고 증거 바이트 기록."""

    directory_flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        directory_flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        directory_flags |= os.O_NOFOLLOW
    directory = os.open(path.parent, directory_flags)
    try:
        before = os.fstat(directory)
        file_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, "O_CLOEXEC"):
            file_flags |= os.O_CLOEXEC
        if hasattr(os, "O_NOFOLLOW"):
            file_flags |= os.O_NOFOLLOW
        descriptor = os.open(path.name, file_flags, 0o600, dir_fd=directory)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(contents)
            handle.flush()
            os.fsync(handle.fileno())
        after = path.parent.stat()
        if not os.path.samestat(before, after):
            raise OSError("artifact root changed while writing")
        os.fsync(directory)
    finally:
        os.close(directory)
    return path


def _sealed_mapping(value: Mapping[str, object], key: bytes) -> dict[str, object]:
    """정규 mapping에 HMAC-SHA256 state 봉인 추가."""

    if not isinstance(key, bytes) or len(key) < 32:
        raise ValueError("state sealing key must contain at least 256 bits")
    payload = dict(value)
    if "state_seal" in payload:
        raise ValueError("unsealed state must not contain state_seal")
    payload["state_seal"] = hmac.new(
        key,
        _canonical_json(payload),
        hashlib.sha256,
    ).hexdigest()
    return payload


def verify_sealed_mapping(
    value: Mapping[str, object],
    key: bytes,
) -> dict[str, object]:
    """HMAC으로 봉인된 state mapping 검증 및 payload 반환.

    Args:
        value: ``state_seal``을 포함한 state mapping.
        key: state 봉인에 사용한 256비트 이상의 비밀 키.

    Returns:
        ``state_seal``을 제거한 검증 완료 payload.

    Raises:
        ValueError: seal 형식 또는 HMAC이 유효하지 않은 경우.
    """

    if not isinstance(value, Mapping):
        raise ValueError("sealed state must be a mapping")
    payload = dict(value)
    seal = payload.pop("state_seal", None)
    if (
        not isinstance(seal, str)
        or len(seal) != 64
        or any(character not in "0123456789abcdef" for character in seal)
    ):
        raise ValueError("state seal is invalid")
    expected = _sealed_mapping(payload, key)["state_seal"]
    if not isinstance(expected, str) or not hmac.compare_digest(seal, expected):
        raise ValueError("state seal mismatch")
    return payload


def _safe_relative_directory(path: Path, *, root: Path) -> str:
    """artifact root 내부의 실제 candidate 상대 경로 검증."""

    resolved_root = root.resolve()
    resolved = path.resolve()
    if (
        not path.is_dir()
        or path.is_symlink()
        or not resolved.is_relative_to(resolved_root)
    ):
        raise WorkflowStageError(
            stage="candidate",
            code=IssueCode.SANDBOX_OPERATION_FAILED,
            message="candidate sandbox is outside the artifact root",
        )
    relative = resolved.relative_to(resolved_root)
    if not relative.parts:
        raise WorkflowStageError(
            stage="candidate",
            code=IssueCode.SANDBOX_OPERATION_FAILED,
            message="candidate sandbox path is invalid",
        )
    return PurePosixPath(*relative.parts).as_posix()


def _stage_environment(
    source: Mapping[str, str],
    *,
    validated_values: Mapping[str, str] | None = None,
) -> dict[str, str]:
    """단계 실행에 허용된 환경 변수만 선택."""

    selected: dict[str, str] = {}
    for key, value in source.items():
        if not isinstance(key, str) or not isinstance(value, str) or not value:
            continue
        if (
            key in _BASE_ENVIRONMENT_KEYS
            or key.startswith("LC_")
        ):
            selected[key] = value
    if validated_values is not None:
        selected.update(validated_values)
    return selected


def _prepare_git_environment(source: Mapping[str, str]) -> dict[str, str]:
    """publication 준비용 Git 식별 정보와 최소 환경 구성."""

    selected = {
        key: value
        for key, value in source.items()
        if isinstance(value, str)
        and value
        and (key == "PATH" or key in {"LANG", "LC_ALL"} or key.startswith("LC_"))
    }
    selected.update(_PREPARE_GIT_IDENTITY)
    return selected


def _failure_event(error: WorkflowStageError) -> FailureEvent:
    """단계 오류를 안정된 실패 보고서 이벤트로 변환."""

    attempts = error.attempts
    if classification_for(error.code) is ErrorClassification.TRANSLATION:
        attempts = attempts or ProviderAttempts(response_evaluation=0, transport=0)
    return FailureEvent(
        code=error.code,
        stage=error.stage,
        message=error.message,
        attempts=attempts,
    )


_FIXTURE_EVIDENCE_KEYS = (
    "provider",
    "model",
    "model_profile",
    "reasoning",
    "locale",
    "prompt_sha256",
    "fixture_version",
    "response_contract_version",
    "budget_profile_version",
    "config_sha256",
    "status",
)
_SAFE_EVIDENCE_VALUE = re.compile(r"[A-Za-z0-9._:/+-]{1,160}\Z")
_FIXTURE_VERSION = 1


def _validate_fixture_evidence(value: bytes, live_config: Config) -> bytes:
    """KO·JA live provider fixture 증거와 설정 식별자 검증."""

    try:
        if not isinstance(value, bytes) or not value or len(value) > 8192:
            raise ValueError
        text = value.decode("utf-8", errors="strict")
        if not text.endswith("\n") or text.endswith("\n\n"):
            raise ValueError
        lines = text[:-1].split("\n")
        if len(lines) != 2:
            raise ValueError
        records: list[dict[str, str]] = []
        for line in lines:
            fields = line.split(" ")
            if len(fields) != len(_FIXTURE_EVIDENCE_KEYS):
                raise ValueError
            record: dict[str, str] = {}
            for expected_key, field in zip(_FIXTURE_EVIDENCE_KEYS, fields):
                key, separator, field_value = field.partition("=")
                if (
                    separator != "="
                    or key != expected_key
                    or not _SAFE_EVIDENCE_VALUE.fullmatch(field_value)
                ):
                    raise ValueError
                record[key] = field_value
            records.append(record)
        expected = {
            "provider": live_config.provider,
            "model": live_config.get("TRANSLATION_MODEL"),
            "model_profile": provider_model_profile(live_config),
            "reasoning": live_config.get(
                "TRANSLATION_REASONING_EFFORT",
                "medium",
            ),
            "fixture_version": str(_FIXTURE_VERSION),
            "response_contract_version": str(RESPONSE_CONTRACT_VERSION),
            "budget_profile_version": str(PROVIDER_BUDGET_PROFILE_VERSION),
            "config_sha256": provider_config_sha256(live_config),
            "status": "passed",
        }
        if [record["locale"] for record in records] != ["ko", "ja"]:
            raise ValueError
        for record in records:
            if (
                any(
                    record[key] != expected_value
                    for key, expected_value in expected.items()
                )
                or len(record["prompt_sha256"]) != 64
                or any(
                    character not in "0123456789abcdef"
                    for character in record["prompt_sha256"]
                )
            ):
                raise ValueError
    except (UnicodeError, TypeError, ValueError) as exc:
        raise WorkflowStageError(
            stage="provider-fixture",
            code=IssueCode.FIXTURE_CONTRACT_FAILED,
            message="provider fixture success evidence is invalid",
        ) from exc
    return value


class WorkflowPreparer:
    """원격 자격 증명 없는 단일 불변 publication 상태 준비."""

    def __init__(
        self,
        *,
        settings: WorkflowSettings,
        environment: Mapping[str, str],
        hooks: WorkflowHooks,
        clock: Callable[[], float] = time.monotonic,
        run_id_factory: Callable[[], str],
        preparation_key_factory: Callable[[], bytes] = lambda: secrets.token_bytes(32),
        workflow_started_at: float | None = None,
    ) -> None:
        """설정, 환경, 단계 어댑터 및 단조 시계 고정."""

        self._settings = settings
        self._environment = dict(environment)
        self._hooks = hooks
        self._clock = clock
        self._run_id_factory = run_id_factory
        self._preparation_key_factory = preparation_key_factory
        self._workflow_started_at = workflow_started_at

    def prepare(self, request: PrepareRequest) -> PrepareOutcome:
        """승인 기준본부터 봉인된 publication 상태까지 순서대로 준비.

        Args:
            request: 저장소, 산출 경로, branch 및 selector를 담은 실행 요청.

        Returns:
            성공 state 경로 또는 안정된 실패 보고서 경로.
        """

        deadline = (
            WorkflowDeadline(
                expires_at=(
                    self._workflow_started_at
                    + self._settings.workflow_timeout_seconds
                ),
                _clock=self._clock,
            )
            if self._workflow_started_at is not None
            else WorkflowDeadline.start(
                self._settings.workflow_timeout_seconds,
                clock=self._clock,
            )
        )
        run_id = self._run_id_factory()
        failures: list[FailureEvent] = []
        base: ApprovedPublicationBase | None = None
        snapshot: ReplaySnapshot | None = None
        candidate: CandidateResult | None = None
        prepared: PreparedPublication | None = None
        candidate_relative: str | None = None
        artifact_root: Path | None = None
        live_config: Config | None = None

        try:
            artifact_root = self._validate_artifact_root(request)
            self._validate_request(request)
            self._ensure_output_targets_absent(artifact_root)
            live_config = self._load_live_config()
            run_timeout = self._run_timeout_seconds(live_config)

            deadline.phase_remaining()
            base = self._hooks.capture_base(request, deadline.remaining_seconds)
            self._validate_base(base, request)

            deadline.phase_remaining()
            unit_result = self._hooks.run_unit_tests(
                request,
                base,
                self._settings.unit_test_command,
                deadline.remaining_seconds,
            )
            self._require_unit_success(unit_result, base)

            replay_environment = _stage_environment(
                self._environment,
            )
            replay_environment[WORKFLOW_DEADLINE_ENV] = _format_deadline(
                deadline.expires_at
            )
            replay_environment[FAILURE_REPORT_ENV] = str(
                artifact_root / REPLAY_FAILURE_FILENAME
            )
            replay_environment[RUN_ID_ENV] = run_id
            deadline.phase_remaining()
            snapshot = self._hooks.run_replay(
                request,
                self._settings.replay_command,
                artifact_root / REPLAY_STATE_FILENAME,
                replay_environment,
                deadline.remaining_seconds,
            )
            self._reject_unexpected_child_failure(
                artifact_root / REPLAY_FAILURE_FILENAME,
                stage="replay",
            )
            if not isinstance(snapshot, ReplaySnapshot):
                raise WorkflowStageError(
                    stage="replay",
                    code=IssueCode.UNCLASSIFIED_INTERNAL,
                    message="replay returned an invalid snapshot",
                )
            self._require_snapshot_selector(snapshot, request)
            manifest_path = _write_no_replace(
                artifact_root / MANIFEST_FILENAME,
                snapshot.manifest,
            )

            run_deadline = deadline.cap_from_now(
                run_timeout,
                exceeded_code=IssueCode.RUN_DEADLINE_EXCEEDED,
            )
            live_environment = _stage_environment(
                self._environment,
                validated_values=live_config.values,
            )
            live_environment.update(
                {
                    "HOME": os.devnull,
                    "XDG_CONFIG_HOME": os.devnull,
                    RUN_ID_ENV: run_id,
                    WORKFLOW_DEADLINE_ENV: _format_deadline(deadline.expires_at),
                    RUN_DEADLINE_ENV: _format_deadline(run_deadline.expires_at),
                    MANIFEST_ENV: str(manifest_path),
                    MANIFEST_DIGEST_ENV: snapshot.manifest_digest,
                    SELECTOR_ENV: snapshot.selector.decode("utf-8", errors="strict"),
                    SELECTOR_DIGEST_ENV: snapshot.selector_digest,
                }
            )

            run_deadline.phase_remaining()
            fixture_environment = dict(live_environment)
            fixture_environment[FAILURE_REPORT_ENV] = str(
                artifact_root / FIXTURE_FAILURE_FILENAME
            )
            fixture_evidence = self._hooks.run_provider_fixture(
                request,
                self._settings.provider_fixture_command,
                fixture_environment,
                run_deadline.remaining_seconds,
            )
            fixture_evidence = _validate_fixture_evidence(
                fixture_evidence,
                live_config,
            )
            _write_no_replace(
                artifact_root / FIXTURE_EVIDENCE_FILENAME,
                fixture_evidence,
            )
            self._reject_unexpected_child_failure(
                artifact_root / FIXTURE_FAILURE_FILENAME,
                stage="provider-fixture",
            )

            run_deadline.phase_remaining()
            candidate_environment = dict(live_environment)
            candidate_environment["TRANSLATION_CANDIDATE"] = "1"
            candidate = self._hooks.build_candidate(
                request,
                base,
                self._settings.candidate_setup_commands,
                self._settings.sync_core_command,
                self._settings.site_validation_commands,
                self._settings.path_validation_command,
                candidate_environment,
                deadline.remaining_seconds,
            )
            if isinstance(candidate, CandidateResult) and candidate.sandbox is not None:
                candidate_relative = _safe_relative_directory(
                    candidate.sandbox,
                    root=artifact_root,
                )
            candidate_relative = self._require_candidate_success(
                candidate,
                base=base,
                artifact_root=artifact_root,
                run_id=run_id,
            )

            deadline.phase_remaining()
            preparation_key = self._preparation_key_factory()
            if not isinstance(preparation_key, bytes) or len(preparation_key) < 32:
                raise WorkflowStageError(
                    stage="publication-prepare",
                    code=IssueCode.INVALID_RUNTIME_OPTION,
                    message="publication preparation key is invalid",
                )
            _write_no_replace(
                artifact_root / PREPARATION_KEY_FILENAME,
                preparation_key,
            )
            prepared = self._hooks.prepare_publication(
                request,
                base,
                candidate,
                preparation_key,
                deadline.remaining_seconds,
            )
            self._validate_prepared(prepared, base=base, candidate=candidate)
        except WorkflowStageError as exc:
            if candidate_relative is None and exc.candidate_debug_path is not None:
                candidate_relative = exc.candidate_debug_path
            failures.extend(
                exc.reported_failures
                if exc.reported_failures is not None
                else (_failure_event(exc),)
            )
        except RepositoryStateError as exc:
            failures.append(
                _failure_event(
                    WorkflowStageError(
                        stage="approved-base",
                        code=exc.code,
                        message="approved publication base could not be captured",
                    )
                )
            )
        except PublicationError as exc:
            failures.append(
                _failure_event(
                    WorkflowStageError(
                        stage="publication-prepare",
                        code=exc.code,
                        message="publication commit could not be prepared",
                    )
                )
            )
        except DeadlineExceeded as exc:
            failures.append(
                _failure_event(
                    WorkflowStageError(
                        stage="workflow",
                        code=exc.code,
                        message="workflow deadline expired",
                    )
                )
            )
        except OSError as exc:
            failures.append(
                _failure_event(
                    WorkflowStageError(
                        stage="workflow",
                        code=IssueCode.RUNNER_OPERATION_FAILED,
                        message=f"workflow I/O failed ({type(exc).__name__})",
                    )
                )
            )
        except (UnicodeError, ValueError, TypeError) as exc:
            failures.append(
                _failure_event(
                    WorkflowStageError(
                        stage="workflow",
                        code=IssueCode.INVALID_RUNTIME_OPTION,
                        message=f"workflow input was rejected ({type(exc).__name__})",
                    )
                )
            )
        except Exception as exc:
            failures.append(
                _failure_event(
                    WorkflowStageError(
                        stage="workflow",
                        code=IssueCode.UNCLASSIFIED_INTERNAL,
                        message=f"unexpected workflow failure ({type(exc).__name__})",
                    )
                )
            )

        if base is not None:
            fingerprint_failure = self._active_fingerprint_failure(
                request=request,
                base=base,
                deadline=deadline,
            )
            if fingerprint_failure is not None:
                failures.append(fingerprint_failure)

        if failures:
            return self._failure_outcome(
                failures,
                artifact_root=artifact_root,
                run_id=run_id,
                base=base,
                snapshot=snapshot,
                candidate_relative=candidate_relative,
            )

        assert artifact_root is not None
        assert base is not None
        assert snapshot is not None
        assert candidate is not None
        assert prepared is not None
        assert candidate_relative is not None
        try:
            state_path = _write_no_replace(
                artifact_root / PREPARED_STATE_FILENAME,
                self._prepared_state_bytes(
                    request=request,
                    run_id=run_id,
                    deadline=deadline,
                    base=base,
                    snapshot=snapshot,
                    candidate=candidate,
                    candidate_relative=candidate_relative,
                    prepared=prepared,
                    preparation_key=preparation_key,
                    fixture_evidence=fixture_evidence,
                ),
            )
        except (OSError, ValueError, TypeError) as exc:
            state_failures = [
                FailureEvent(
                    code=IssueCode.RUNNER_OPERATION_FAILED,
                    stage="state-write",
                    message=(
                        "prepared state could not be written "
                        f"({type(exc).__name__})"
                    ),
                )
            ]
            fingerprint_failure = self._active_fingerprint_failure(
                request=request,
                base=base,
                deadline=deadline,
            )
            if fingerprint_failure is not None:
                state_failures.append(fingerprint_failure)
            return self._failure_outcome(
                state_failures,
                artifact_root=artifact_root,
                run_id=run_id,
                base=base,
                snapshot=snapshot,
                candidate_relative=candidate_relative,
            )
        fingerprint_failure = self._active_fingerprint_failure(
            request=request,
            base=base,
            deadline=deadline,
        )
        if fingerprint_failure is not None:
            return self._failure_outcome(
                [fingerprint_failure],
                artifact_root=artifact_root,
                run_id=run_id,
                base=base,
                snapshot=snapshot,
                candidate_relative=candidate_relative,
            )
        return PrepareOutcome(exit_code=ExitCode.SUCCESS, state_path=state_path)

    def _active_fingerprint_failure(
        self,
        *,
        request: PrepareRequest,
        base: ApprovedPublicationBase,
        deadline: WorkflowDeadline,
    ) -> FailureEvent | None:
        """준비 전후 활성 저장소 fingerprint 불변성 재검증."""

        try:
            current_fingerprint = self._hooks.read_active_fingerprint(
                request,
                deadline.remaining_seconds,
            )
            deadline.phase_remaining()
            if current_fingerprint == base.active_fingerprint:
                return None
            return FailureEvent(
                code=IssueCode.ACTIVE_WORKTREE_MUTATED,
                stage="active-fingerprint",
                message="active repository changed during workflow preparation",
            )
        except WorkflowStageError as exc:
            return _failure_event(exc)
        except RepositoryStateError as exc:
            return FailureEvent(
                code=exc.code,
                stage="active-fingerprint",
                message="active repository fingerprint could not be read",
            )
        except DeadlineExceeded as exc:
            return FailureEvent(
                code=exc.code,
                stage="active-fingerprint",
                message="active repository fingerprint deadline expired",
            )
        except Exception:
            return FailureEvent(
                code=IssueCode.RUNNER_OPERATION_FAILED,
                stage="active-fingerprint",
                message="active repository could not be reverified",
            )

    @staticmethod
    def _validate_artifact_root(request: PrepareRequest) -> Path:
        """활성 저장소와 분리된 기존 artifact root 검증."""

        if not isinstance(request, PrepareRequest):
            raise WorkflowStageError(
                stage="configuration",
                code=IssueCode.INVALID_RUNTIME_OPTION,
                message="prepare request has an invalid type",
            )
        repository = request.repository.resolve()
        artifact_root = request.artifact_root.resolve()
        if (
            not repository.is_dir()
            or not artifact_root.is_dir()
            or request.artifact_root.is_symlink()
            or artifact_root == repository
            or artifact_root.is_relative_to(repository)
            or repository.is_relative_to(artifact_root)
        ):
            raise WorkflowStageError(
                stage="configuration",
                code=IssueCode.INVALID_RUNTIME_OPTION,
                message="artifact root must be an external existing directory",
            )
        return artifact_root

    @staticmethod
    def _validate_request(request: PrepareRequest) -> None:
        """publication·배포 입력 문자열과 정규 selector 검증."""

        values = (
            request.push_endpoint,
            request.deploy_repository,
            request.branch,
            request.commit_message,
        )
        if any(
            not isinstance(value, str)
            or not value
            or "\0" in value
            for value in values
        ):
            raise WorkflowStageError(
                stage="configuration",
                code=IssueCode.INVALID_RUNTIME_OPTION,
                message="workflow request contains an invalid string",
            )
        if not _DEPLOY_REPOSITORY.fullmatch(request.deploy_repository):
            raise WorkflowStageError(
                stage="configuration",
                code=IssueCode.INVALID_RUNTIME_OPTION,
                message="deployment repository must be an explicit owner/name",
            )
        try:
            if request.version is not None:
                validate_version_token(request.version)
            if request.document is not None:
                if request.version is None:
                    raise ValueError("document selector requires a version")
                if (
                    upstream.normalize_document_selector(request.document)
                    != request.document
                ):
                    raise ValueError("document selector must already be canonical")
        except (TypeError, ValueError) as exc:
            raise WorkflowStageError(
                stage="selector",
                code=IssueCode.INVALID_SELECTOR,
                message="workflow selector is invalid",
            ) from exc
        try:
            _deployment_host_for(
                request.push_endpoint,
                request.deploy_repository,
            )
        except ValueError as exc:
            raise WorkflowStageError(
                stage="configuration",
                code=IssueCode.INVALID_RUNTIME_OPTION,
                message=(
                    "push endpoint must identify the deployment repository"
                ),
            ) from exc

    @staticmethod
    def _ensure_output_targets_absent(artifact_root: Path) -> None:
        """이번 실행이 생성할 증거 파일의 사전 부재 확인."""

        for filename in (
            PREPARED_STATE_FILENAME,
            REPLAY_STATE_FILENAME,
            MANIFEST_FILENAME,
            PREPARATION_KEY_FILENAME,
            REPLAY_FAILURE_FILENAME,
            FIXTURE_FAILURE_FILENAME,
            FIXTURE_EVIDENCE_FILENAME,
            SYNC_FAILURE_REPORT_FILENAME,
            PATH_FAILURE_REPORT_FILENAME,
            PUBLISHED_STATE_FILENAME,
            DEPLOYED_STATE_FILENAME,
            REPORT_FILENAME,
        ):
            if (artifact_root / filename).exists() or (
                artifact_root / filename
            ).is_symlink():
                raise WorkflowStageError(
                    stage="configuration",
                    code=IssueCode.INVALID_RUNTIME_OPTION,
                    message="workflow artifact target already exists",
                )

    @staticmethod
    def _validate_base(
        base: ApprovedPublicationBase,
        request: PrepareRequest,
    ) -> None:
        """캡처 결과 유형과 요청 branch ref의 일치 검증."""

        if not isinstance(base, ApprovedPublicationBase):
            raise WorkflowStageError(
                stage="approved-base",
                code=IssueCode.UNCLASSIFIED_INTERNAL,
                message="approved base result is invalid",
            )
        if base.remote_ref != f"refs/heads/{request.branch}":
            raise WorkflowStageError(
                stage="approved-base",
                code=IssueCode.PUBLICATION_BASE_CHANGED,
                message="approved branch ref does not match the request",
            )

    @staticmethod
    def _reject_unexpected_child_failure(path: Path, *, stage: str) -> None:
        """성공한 하위 단계가 남긴 예상 밖 실패 보고서 거부."""

        if path.exists() or path.is_symlink():
            raise WorkflowStageError(
                stage=stage,
                code=IssueCode.RUNNER_OPERATION_FAILED,
                message="successful child left contradictory failure evidence",
            )

    @staticmethod
    def _require_unit_success(
        result: ApprovedBaseUnitTestResult,
        base: ApprovedPublicationBase,
    ) -> None:
        """단위 테스트 결과와 승인 기준본 증거의 일치 요구."""

        if not isinstance(result, ApprovedBaseUnitTestResult):
            raise WorkflowStageError(
                stage="unit-test",
                code=IssueCode.UNCLASSIFIED_INTERNAL,
                message="unit test preflight returned an invalid result",
            )
        if not result.succeeded or result.proof is None:
            failure = result.failure
            raise WorkflowStageError(
                stage=failure.stage if failure is not None else "unit-test",
                code=(
                    failure.issue_code
                    if failure is not None
                    else IssueCode.UNIT_TEST_FAILED
                ),
                message="approved-base unit test preflight failed",
            )
        if (
            result.proof.base_commit != base.head
            or result.proof.base_tree != base.tree
        ):
            raise WorkflowStageError(
                stage="unit-test",
                code=IssueCode.PUBLICATION_BASE_CHANGED,
                message="unit test proof does not identify the approved base",
            )

    @staticmethod
    def _require_snapshot_selector(
        snapshot: ReplaySnapshot,
        request: PrepareRequest,
    ) -> None:
        """replay snapshot과 live 요청 selector의 동일성 요구."""

        try:
            value = json.loads(snapshot.selector.decode("utf-8"))
            expected_document = (
                unicodedata.normalize("NFC", request.document)
                if request.document is not None
                else None
            )
            canonical = (
                json.dumps(
                    {
                        "document": expected_document,
                        "version": request.version,
                    },
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
                + "\n"
            ).encode("utf-8")
        except (UnicodeError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise WorkflowStageError(
                stage="replay",
                code=IssueCode.INVALID_SELECTOR,
                message="replay selector could not be verified",
            ) from exc
        if value != {"document": expected_document, "version": request.version} or (
            snapshot.selector != canonical
        ):
            raise WorkflowStageError(
                stage="replay",
                code=IssueCode.INVALID_SELECTOR,
                message="replay selector does not match the live request",
            )

    def _load_live_config(self) -> Config:
        """현재 환경에서 live provider 설정 로딩."""

        try:
            config = load_config(self._environment)
        except ConfigError as exc:
            raise WorkflowStageError(
                stage="configuration",
                code=exc.issue_code,
                message="live provider configuration is invalid",
            ) from exc
        if config.provider == "identity":
            raise WorkflowStageError(
                stage="configuration",
                code=IssueCode.REPLAY_PROVIDER_FORBIDDEN,
                message="identity provider is forbidden in a live workflow",
            )
        return config

    def _run_timeout_seconds(self, config: Config) -> int:
        """provider 설정의 양수 실행 제한 시간 반환."""

        try:
            run_timeout = int(config.values["TRANSLATION_RUN_TIMEOUT_SECONDS"])
            configured_workflow = int(
                config.values["TRANSLATION_WORKFLOW_TIMEOUT_SECONDS"]
            )
        except (KeyError, ValueError) as exc:
            raise WorkflowStageError(
                stage="provider-fixture",
                code=IssueCode.INVALID_REQUEST_BUDGET,
                message="provider run deadline configuration is missing or invalid",
            ) from exc
        if (
            run_timeout <= 0
            or configured_workflow != self._settings.workflow_timeout_seconds
            or run_timeout > configured_workflow
        ):
            raise WorkflowStageError(
                stage="provider-fixture",
                code=IssueCode.INVALID_REQUEST_BUDGET,
                message="provider run deadline configuration is inconsistent",
            )
        return run_timeout

    @staticmethod
    def _require_candidate_success(
        result: CandidateResult,
        *,
        base: ApprovedPublicationBase,
        artifact_root: Path,
        run_id: str,
    ) -> str:
        """candidate 결과의 sandbox, tree 및 검증 증거 요구."""

        if not isinstance(result, CandidateResult):
            raise WorkflowStageError(
                stage="candidate",
                code=IssueCode.UNCLASSIFIED_INTERNAL,
                message="candidate runner returned an invalid result",
            )
        if result.failure is not None or not result.publication_allowed:
            failure = result.failure
            if failure is not None and failure.issue_code is None:
                report_path = failure.report_path
                if (
                    failure.returncode is None
                    or report_path is None
                    or report_path.parent.resolve() != artifact_root.resolve()
                    or report_path.name
                    not in {
                        SYNC_FAILURE_REPORT_FILENAME,
                        PATH_FAILURE_REPORT_FILENAME,
                    }
                ):
                    raise WorkflowStageError(
                        stage=failure.stage,
                        code=IssueCode.RUNNER_OPERATION_FAILED,
                        message="candidate child failure evidence is unavailable",
                    )
                raise _read_child_failure(
                    report_path,
                    expected_returncode=failure.returncode,
                    expected_run_id=run_id,
                    fallback_stage=failure.stage,
                )
            raise WorkflowStageError(
                stage=failure.stage if failure is not None else "candidate",
                code=(
                    failure.issue_code
                    if failure is not None and failure.issue_code is not None
                    else IssueCode.UNCLASSIFIED_INTERNAL
                ),
                message="candidate construction or verification failed",
            )
        if result.base_commit != base.head or result.sandbox is None:
            raise WorkflowStageError(
                stage="candidate",
                code=IssueCode.PUBLICATION_BASE_CHANGED,
                message="candidate does not identify the approved base",
            )
        return _safe_relative_directory(result.sandbox, root=artifact_root)

    @staticmethod
    def _validate_prepared(
        prepared: PreparedPublication,
        *,
        base: ApprovedPublicationBase,
        candidate: CandidateResult,
    ) -> None:
        """prepared publication과 candidate 식별자의 일치 검증."""

        if not isinstance(prepared, PreparedPublication):
            raise WorkflowStageError(
                stage="publication-prepare",
                code=IssueCode.UNCLASSIFIED_INTERNAL,
                message="publication preparer returned an invalid result",
            )
        if (
            prepared.base_head != base.head
            or prepared.base_tree != base.tree
            or prepared.remote_ref != base.remote_ref
            or prepared.verified_tree != candidate.verified_tree
            or (prepared.commit_oid is None) != (not candidate.has_changes)
        ):
            raise WorkflowStageError(
                stage="publication-prepare",
                code=IssueCode.VERIFIED_TREE_MISMATCH,
                message="prepared publication does not match the sealed candidate",
            )

    def _prepared_state_bytes(
        self,
        *,
        request: PrepareRequest,
        run_id: str,
        deadline: WorkflowDeadline,
        base: ApprovedPublicationBase,
        snapshot: ReplaySnapshot,
        candidate: CandidateResult,
        candidate_relative: str,
        prepared: PreparedPublication,
        preparation_key: bytes,
        fixture_evidence: bytes,
    ) -> bytes:
        """봉인할 prepared state의 정규 JSON 바이트 생성."""

        return _canonical_json(
            _sealed_mapping(
                {
                "schema_version": 1,
                "run_id": run_id,
                "workflow_deadline_monotonic": deadline.expires_at,
                "branch": request.branch,
                "push_endpoint": request.push_endpoint,
                "deploy_repository": request.deploy_repository,
                "deploy_host": _deployment_host_for(
                    request.push_endpoint,
                    request.deploy_repository,
                ),
                "deploy_workflow": self._settings.deploy_workflow,
                "base": {
                    "head": base.head,
                    "tree": base.tree,
                    "remote_ref": base.remote_ref,
                    "remote_oid": base.remote_oid,
                    "active_fingerprint": base.active_fingerprint,
                },
                "replay": {
                    "manifest_file": MANIFEST_FILENAME,
                    "manifest_digest": snapshot.manifest_digest,
                    "selector_base64": base64.b64encode(snapshot.selector).decode(
                        "ascii"
                    ),
                    "selector_digest": snapshot.selector_digest,
                },
                "fixture": {
                    "evidence_file": FIXTURE_EVIDENCE_FILENAME,
                    "evidence_digest": hashlib.sha256(
                        fixture_evidence
                    ).hexdigest(),
                },
                "candidate": {
                    "path": candidate_relative,
                    "base_commit": candidate.base_commit,
                    "verified_tree": candidate.verified_tree,
                    "has_changes": candidate.has_changes,
                },
                "publication": prepared.to_mapping(),
                },
                preparation_key,
            )
        )

    @staticmethod
    def _failure_outcome(
        failures: Sequence[FailureEvent],
        *,
        artifact_root: Path | None,
        run_id: str,
        base: ApprovedPublicationBase | None,
        snapshot: ReplaySnapshot | None,
        candidate_relative: str | None,
    ) -> PrepareOutcome:
        """실패 우선순위를 확정하고 안정된 보고서 결과 생성."""

        report_path: Path | None = None
        if artifact_root is not None:
            try:
                report = FailureReport.build(
                    run_id=run_id,
                    failures=failures,
                    manifest_digest=(
                        snapshot.manifest_digest if snapshot is not None else None
                    ),
                    base_head=base.head if base is not None else None,
                    candidate_debug_path=candidate_relative,
                )
                report_path = write_failure_report(
                    report,
                    artifact_root=artifact_root,
                )
            except (OSError, TypeError, ValueError):
                report_path = None
        primary = max(failures, key=lambda failure: int(failure.exit_code))
        return PrepareOutcome(
            exit_code=final_exit_code(failures),
            report_path=report_path,
            failure_code=primary.code,
        )


def _remaining_timeout(
    remaining_seconds: Callable[[], float],
    *,
    stage: str,
    deadline_code: IssueCode,
) -> float:
    """단계 콜백에서 유효한 양수의 남은 시간 획득."""

    try:
        remaining = float(remaining_seconds())
    except Exception as exc:
        raise WorkflowStageError(
            stage=stage,
            code=IssueCode.INVALID_RUNTIME_OPTION,
            message="workflow deadline callback failed",
        ) from exc
    if not math.isfinite(remaining) or remaining <= 0:
        raise WorkflowStageError(
            stage=stage,
            code=deadline_code,
            message="workflow deadline expired",
        )
    return remaining


def _run_stage_command(
    argv: Sequence[str],
    *,
    cwd: Path,
    environment: Mapping[str, str],
    remaining_seconds: Callable[[], float],
    stage: str = "workflow",
    deadline_code: IssueCode = IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
    capture_stdout: bool = False,
) -> subprocess.CompletedProcess[bytes]:
    """허용된 환경과 공유 기한으로 하위 단계 argv 실행."""

    try:
        return run_process_tree(
            tuple(argv),
            cwd=cwd,
            env=dict(environment),
            check=False,
            stdout=subprocess.PIPE if capture_stdout else subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=_remaining_timeout(
                remaining_seconds,
                stage=stage,
                deadline_code=deadline_code,
            ),
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise WorkflowStageError(
            stage=stage,
            code=deadline_code,
            message="workflow child process exceeded the deadline",
        ) from exc
    except ProcessTreeError as exc:
        raise WorkflowStageError(
            stage=stage,
            code=IssueCode.RUNNER_OPERATION_FAILED,
            message="workflow child process isolation failed",
        ) from exc
    except OSError as exc:
        raise WorkflowStageError(
            stage=stage,
            code=IssueCode.RUNNER_OPERATION_FAILED,
            message="workflow child process could not be started",
        ) from exc


def _selector_argv(request: PrepareRequest) -> tuple[str, ...]:
    """정규화된 VERSION·DOC selector를 명령행 argv로 변환."""

    result: list[str] = []
    if request.version is not None:
        result.extend(("--version", request.version))
    if request.document is not None:
        result.extend(("--doc", request.document))
    return tuple(result)


def _read_child_failure(
    path: Path,
    *,
    expected_returncode: int,
    expected_run_id: str,
    fallback_stage: str,
) -> WorkflowStageError:
    """하위 프로세스의 정규 실패 보고서를 단계 오류로 복원."""

    try:
        flags = os.O_RDONLY
        if hasattr(os, "O_CLOEXEC"):
            flags |= os.O_CLOEXEC
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(path, flags)
        try:
            metadata = os.fstat(descriptor)
            if (
                not stat.S_ISREG(metadata.st_mode)
                or metadata.st_size <= 0
                or metadata.st_size > 1_000_000
            ):
                raise ValueError("invalid child failure report file")
            chunks: list[bytes] = []
            remaining = metadata.st_size
            while remaining:
                chunk = os.read(descriptor, min(remaining, 64 * 1024))
                if not chunk:
                    raise ValueError("truncated child failure report")
                chunks.append(chunk)
                remaining -= len(chunk)
            raw = b"".join(chunks)
        finally:
            os.close(descriptor)

        value = json.loads(raw.decode("utf-8", errors="strict"))
        expected = {
            "schema_version",
            "run_id",
            "manifest_digest",
            "base_head",
            "stage",
            "classification",
            "code",
            "exit_code",
            "published_commit",
            "version",
            "locale",
            "document",
            "plan_id",
            "structural_address",
            "attempts",
            "issues",
            "candidate_debug_path",
        }
        if (
            not isinstance(value, dict)
            or set(value) != expected
            or raw != _canonical_json(value)
            or value["schema_version"] != 1
            or value["run_id"] != expected_run_id
            or isinstance(value["exit_code"], bool)
            or value["exit_code"] != expected_returncode
            or not isinstance(value["stage"], str)
            or not value["stage"]
            or len(value["stage"]) > 128
            or not value["stage"][0].isalnum()
            or any(
                not (character.isalnum() or character in "._-")
                for character in value["stage"]
            )
            or not isinstance(value["issues"], list)
            or not value["issues"]
        ):
            raise ValueError("invalid child failure report")
        code = IssueCode(value["code"])
        if value["classification"] != classification_for(code).value:
            raise ValueError("child failure code mismatch")
        attempts_value = value["attempts"]
        candidate_debug_path = value.get("candidate_debug_path")
        if candidate_debug_path is not None and (
            not isinstance(candidate_debug_path, str)
            or not candidate_debug_path
            or "\\" in candidate_debug_path
            or PurePosixPath(candidate_debug_path).is_absolute()
            or any(
                part in {"", ".", ".."}
                for part in candidate_debug_path.split("/")
            )
        ):
            raise ValueError("invalid child candidate debug path")
        attempts: ProviderAttempts | None = None
        if classification_for(code) is ErrorClassification.TRANSLATION:
            if not isinstance(attempts_value, dict) or set(attempts_value) != {
                "response_evaluation",
                "transport",
            }:
                raise ValueError("invalid provider attempts")
            attempts = ProviderAttempts(
                response_evaluation=attempts_value["response_evaluation"],
                transport=attempts_value["transport"],
            )
        elif attempts_value is not None:
            raise ValueError("unexpected provider attempts")

        issue_values = value["issues"]
        parsed_issues: list[tuple[IssueCode, str | None, str]] = []
        primary_index: int | None = None
        for index, issue_value in enumerate(issue_values):
            if not isinstance(issue_value, dict) or set(issue_value) != {
                "code",
                "structural_address",
                "message",
            }:
                raise ValueError("invalid child issue")
            issue_code = IssueCode(issue_value["code"])
            structural_address = issue_value["structural_address"]
            message = issue_value["message"]
            if not isinstance(message, str):
                raise ValueError("invalid child issue message")
            parsed_issues.append((issue_code, structural_address, message))
            if (
                primary_index is None
                and issue_code == code
                and structural_address == value["structural_address"]
            ):
                primary_index = index
        if primary_index is None:
            raise ValueError("child primary issue is missing")

        ordered = [parsed_issues[primary_index]]
        ordered.extend(
            issue
            for index, issue in enumerate(parsed_issues)
            if index != primary_index
        )
        reported_failures: list[FailureEvent] = []
        for index, (issue_code, structural_address, message) in enumerate(ordered):
            primary = index == 0
            issue_attempts = attempts if primary else None
            if (
                not primary
                and classification_for(issue_code)
                is ErrorClassification.TRANSLATION
            ):
                issue_attempts = ProviderAttempts(
                    response_evaluation=0,
                    transport=0,
                )
            reported_failures.append(
                FailureEvent(
                    code=issue_code,
                    stage=value["stage"],
                    message=message,
                    version=value["version"] if primary else None,
                    locale=value["locale"] if primary else None,
                    document=value["document"] if primary else None,
                    plan_id=value["plan_id"] if primary else None,
                    structural_address=structural_address,
                    attempts=issue_attempts,
                )
            )
        report = FailureReport.build(
            run_id=value["run_id"],
            failures=reported_failures,
            manifest_digest=value["manifest_digest"],
            base_head=value["base_head"],
            published_commit=value["published_commit"],
            candidate_debug_path=candidate_debug_path,
        )
        if report.to_bytes() != raw:
            raise ValueError("child failure report is not self-consistent")
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError):
        return WorkflowStageError(
            stage=fallback_stage,
            code=IssueCode.RUNNER_OPERATION_FAILED,
            message="child process failed without valid stable failure evidence",
        )
    return WorkflowStageError(
        stage=value["stage"],
        code=code,
        message=report.primary.message,
        attempts=attempts,
        candidate_debug_path=candidate_debug_path,
        reported_failures=report.failures,
    )


def _read_replay_snapshot(path: Path, *, repository: Path) -> ReplaySnapshot:
    """replay state의 manifest와 selector 증거 검증 및 로딩."""

    try:
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 8_000_000:
            raise ValueError("invalid replay state file")
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise WorkflowStageError(
            stage="replay",
            code=IssueCode.INVALID_MANIFEST,
            message="replay state could not be read",
        ) from exc
    expected = {
        "schema_version",
        "manifest_base64",
        "manifest_digest",
        "selector_base64",
        "selector_digest",
    }
    if not isinstance(value, dict) or set(value) != expected or value.get(
        "schema_version"
    ) != 1:
        raise WorkflowStageError(
            stage="replay",
            code=IssueCode.INVALID_MANIFEST,
            message="replay state schema is invalid",
        )
    try:
        manifest = base64.b64decode(value["manifest_base64"], validate=True)
        manifest_digest = value["manifest_digest"]
        if (
            not isinstance(manifest_digest, str)
            or len(manifest_digest) != 64
            or any(
                character not in "0123456789abcdef"
                for character in manifest_digest
            )
            or hashlib.sha256(manifest).hexdigest() != manifest_digest
        ):
            raise ValueError("manifest digest mismatch")
        versions = load_versions(repository / "versions.json")
        upstream.load_manifest_bytes(manifest, expected_versions=versions)
    except (KeyError, TypeError, ValueError, UnicodeError) as exc:
        raise WorkflowStageError(
            stage="replay",
            code=IssueCode.MANIFEST_DIGEST_MISMATCH,
            message="replay manifest evidence is invalid",
        ) from exc
    try:
        selector = base64.b64decode(value["selector_base64"], validate=True)
        selector_digest = value["selector_digest"]
        if (
            not isinstance(selector_digest, str)
            or len(selector_digest) != 64
            or any(
                character not in "0123456789abcdef"
                for character in selector_digest
            )
            or hashlib.sha256(selector).hexdigest() != selector_digest
        ):
            raise ValueError("selector digest mismatch")
        selector_value = json.loads(selector.decode("utf-8"))
        if (
            not isinstance(selector_value, dict)
            or tuple(selector_value) != ("document", "version")
            or selector
            != (
                json.dumps(
                    selector_value,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
                + "\n"
            ).encode("utf-8")
            or selector_value["version"] not in {None, *versions}
        ):
            raise ValueError("invalid selector")
        document = selector_value["document"]
        if document is not None and (
            selector_value["version"] is None
            or upstream.normalize_document_selector(document) != document
        ):
            raise ValueError("invalid document selector")
    except (
        KeyError,
        TypeError,
        ValueError,
        UnicodeError,
        json.JSONDecodeError,
    ) as exc:
        raise WorkflowStageError(
            stage="replay",
            code=IssueCode.INVALID_SELECTOR,
            message="replay selector evidence is invalid",
        ) from exc
    snapshot = ReplaySnapshot(
        manifest=manifest,
        manifest_digest=manifest_digest,
        selector=selector,
        selector_digest=selector_digest,
    )
    return snapshot


def default_workflow_hooks(
    environment: Mapping[str, str] | None = None,
) -> WorkflowHooks:
    """주입 가능한 단계 경계를 구현하는 운영 어댑터 구성.

    Args:
        environment: 어댑터가 단계별로 정제할 원본 환경 변수. 생략 시 현재 프로세스 환경 사용.

    Returns:
        승인 기준본부터 publication 준비까지의 기본 단계 어댑터 집합.
    """
    source_environment = dict(os.environ if environment is None else environment)

    def capture(
        request: PrepareRequest,
        remaining_seconds: Callable[[], float],
    ) -> ApprovedPublicationBase:
        """활성 저장소의 승인 publication 기준본 캡처."""

        return capture_publication_base(
            request.repository,
            remote=request.push_endpoint,
            branch=request.branch,
            remaining_seconds=remaining_seconds,
        )

    def unit(
        request: PrepareRequest,
        base: ApprovedPublicationBase,
        argv: tuple[str, ...],
        remaining_seconds: Callable[[], float],
    ) -> ApprovedBaseUnitTestResult:
        """승인 기준본의 격리 단위 테스트 실행."""

        return ApprovedBaseUnitTestRunner(
            source_repo=request.repository,
            artifact_root=request.artifact_root,
            remaining_seconds=remaining_seconds,
        ).run(base_commit=base.head, unit_test_argv=argv)

    def replay(
        request: PrepareRequest,
        argv: tuple[str, ...],
        output_path: Path,
        environment: Mapping[str, str],
        remaining_seconds: Callable[[], float],
    ) -> ReplaySnapshot:
        """identity replay 명령 실행과 snapshot 로딩."""

        command = (
            *argv,
            *_selector_argv(request),
            "--state-output",
            str(output_path),
            "--artifact-root",
            str(request.artifact_root),
        )
        completed = _run_stage_command(
            command,
            cwd=request.repository,
            environment=environment,
            remaining_seconds=remaining_seconds,
            stage="replay",
        )
        if completed.returncode:
            raise _read_child_failure(
                Path(environment[FAILURE_REPORT_ENV]),
                expected_returncode=completed.returncode,
                expected_run_id=environment[RUN_ID_ENV],
                fallback_stage="replay",
            )
        return _read_replay_snapshot(output_path, repository=request.repository)

    def fixture(
        request: PrepareRequest,
        argv: tuple[str, ...],
        environment: Mapping[str, str],
        remaining_seconds: Callable[[], float],
    ) -> bytes:
        """live provider fixture 명령 실행과 증거 반환."""

        completed = _run_stage_command(
            argv,
            cwd=request.repository,
            environment=environment,
            remaining_seconds=remaining_seconds,
            stage="provider-fixture",
            deadline_code=IssueCode.RUN_DEADLINE_EXCEEDED,
            capture_stdout=True,
        )
        if completed.returncode:
            raise _read_child_failure(
                Path(environment[FAILURE_REPORT_ENV]),
                expected_returncode=completed.returncode,
                expected_run_id=environment[RUN_ID_ENV],
                fallback_stage="provider-fixture",
            )
        return completed.stdout

    def candidate(
        request: PrepareRequest,
        base: ApprovedPublicationBase,
        setup_argvs: tuple[tuple[str, ...], ...],
        sync_argv: tuple[str, ...],
        site_argvs: tuple[tuple[str, ...], ...],
        path_argv: tuple[str, ...],
        environment: Mapping[str, str],
        remaining_seconds: Callable[[], float],
    ) -> CandidateResult:
        """승인 기준본에서 격리 candidate 생성과 검증 실행."""

        return CandidateRunner(
            source_repo=request.repository,
            artifact_root=request.artifact_root,
            run_id=environment[RUN_ID_ENV],
            remaining_seconds=remaining_seconds,
            sync_environment=environment,
        ).run(
            base_commit=base.head,
            setup_argvs=setup_argvs,
            sync_core_argv=(*sync_argv, *_selector_argv(request)),
            site_validator_argvs=site_argvs,
            path_validator_argv=path_argv,
        )

    def publication(
        request: PrepareRequest,
        base: ApprovedPublicationBase,
        result: CandidateResult,
        preparation_key: bytes,
        remaining_seconds: Callable[[], float],
    ) -> PreparedPublication:
        """검증된 candidate tree의 publication 준비."""

        assert result.sandbox is not None
        assert result.verified_tree is not None

        def read_fingerprint(timeout: float) -> str:
            """호출자 timeout과 공유 기한 중 짧은 값으로 fingerprint 조회."""

            return active_repository_fingerprint(
                request.repository,
                remaining_seconds=lambda: min(timeout, remaining_seconds()),
            )

        prepare_environment = _prepare_git_environment(source_environment)
        publisher = Publisher(
            candidate_repo=result.sandbox,
            push_endpoint=request.push_endpoint,
            base=PublicationBase(
                head=base.head,
                tree=base.tree,
                remote_ref=base.remote_ref,
                active_fingerprint=base.active_fingerprint,
            ),
            read_active_fingerprint=read_fingerprint,
            remaining_seconds=remaining_seconds,
            prepare_environment=prepare_environment,
            preparation_key=preparation_key,
        )
        return publisher.prepare(
            verified_tree=result.verified_tree,
            commit_message=request.commit_message,
        )

    def fingerprint(
        request: PrepareRequest,
        remaining_seconds: Callable[[], float],
    ) -> str:
        """활성 저장소의 현재 fingerprint 조회."""

        return active_repository_fingerprint(
            request.repository,
            remaining_seconds=remaining_seconds,
        )

    return WorkflowHooks(
        capture_base=capture,
        run_unit_tests=unit,
        run_replay=replay,
        run_provider_fixture=fixture,
        build_candidate=candidate,
        prepare_publication=publication,
        read_active_fingerprint=fingerprint,
    )


__all__ = [
    "FAILURE_REPORT_ENV",
    "RUN_ID_ENV",
    "MANIFEST_FILENAME",
    "PREPARATION_KEY_FILENAME",
    "PUBLISHED_STATE_FILENAME",
    "DEPLOYED_STATE_FILENAME",
    "PREPARED_STATE_FILENAME",
    "REPLAY_STATE_FILENAME",
    "PrepareOutcome",
    "PrepareRequest",
    "ReplaySnapshot",
    "WorkflowHooks",
    "WorkflowPreparer",
    "WorkflowStageError",
    "default_workflow_hooks",
    "verify_sealed_mapping",
]
