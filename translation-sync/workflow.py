#!/usr/bin/env python3
"""격리된 단계에서 단일 번역 워크플로의 준비·게시·배포 수행."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import os
import re
import secrets
import stat
import sys
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Mapping, NoReturn, Sequence
from urllib.parse import urlsplit

from sync.runtime.base import RepositoryStateError, active_repository_fingerprint
from sync.runtime.deadline import DeadlineExceeded, WorkflowDeadline
from sync.runtime.deploy import (
    DeploymentCoordinator,
    DeploymentRequest,
    DeploymentResult,
    SubprocessArgvRunner,
)
from sync.runtime.failure import (
    REPORT_FILENAME,
    ExitCode,
    FailureEvent,
    FailureReport,
    IssueCode,
    ProviderAttempts,
    classification_for,
    ErrorClassification,
    final_exit_code,
    write_failure_report,
)
from sync.runtime.publication import (
    PreparedPublication,
    PublicationBase,
    PublicationError,
    PublicationResult,
    Publisher,
)
from sync.runtime.settings import SettingsError, load_workflow_settings
from sync.runtime.workflow import (
    DEPLOYED_STATE_FILENAME,
    FIXTURE_EVIDENCE_FILENAME,
    MANIFEST_FILENAME,
    PREPARATION_KEY_FILENAME,
    PREPARED_STATE_FILENAME,
    PUBLISHED_STATE_FILENAME,
    PrepareRequest,
    WorkflowPreparer,
    _canonical_json,
    _deployment_host_for,
    _prepare_git_environment,
    _sealed_mapping,
    _write_no_replace,
    default_workflow_hooks,
    verify_sealed_mapping,
)


SYNC_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = SYNC_ROOT.parent
SETTINGS_PATH = SYNC_ROOT / "workflow.json"
_MAX_STATE_BYTES = 2_000_000
_FULL_OID_LENGTHS = {40, 64}
_DEPLOY_REPOSITORY = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?"
    r"/[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?\Z"
)
_REPORT_WRITE_FAILED = "REPORT_WRITE_FAILED: failure report could not be written"


@dataclass(frozen=True, slots=True)
class PreparedState:
    """봉인을 검증해 게시 단계로 전달할 준비 상태."""

    run_id: str
    workflow_deadline: WorkflowDeadline
    branch: str
    push_endpoint: str
    deploy_repository: str
    deploy_host: str
    deploy_workflow: str
    manifest_digest: str
    base: PublicationBase
    candidate_path: Path
    candidate_relative: str
    has_changes: bool
    prepared: PreparedPublication
    preparation_key: bytes


@dataclass(frozen=True, slots=True)
class PublishedState:
    """봉인을 검증해 배포 단계로 전달할 게시 상태."""

    run_id: str
    workflow_deadline: WorkflowDeadline
    branch: str
    push_endpoint: str
    deploy_repository: str
    deploy_host: str
    deploy_workflow: str
    manifest_digest: str
    active_fingerprint: str
    base_commit: str
    published_commit: str
    remote_commit: str
    has_changes: bool
    preparation_key: bytes


@dataclass(frozen=True, slots=True)
class _PreparedStateParts:
    """준비 상태의 검증 전 중첩 매핑."""

    push_endpoint: str
    deploy_host: str
    base: dict[str, object]
    candidate: dict[str, object]
    replay: dict[str, object]
    fixture: dict[str, object]


class EntrypointError(RuntimeError):
    """워크플로 진입점 경계에서 사용하는 안정적 오류."""

    def __init__(
        self,
        code: IssueCode,
        *,
        stage: str,
        published_commit: str | None = None,
    ) -> None:
        """진입점 오류 초기화."""

        self.code = code
        self.stage = stage
        self.published_commit = published_commit
        super().__init__(code.value)


class _PushEnvironmentCleanupError(OSError):
    """푸시 자격 증명용 임시 환경 정리 실패."""

    def __init__(self, pending_error: Exception | None) -> None:
        """푸시 환경 정리 오류 초기화."""

        self.pending_error = pending_error
        super().__init__("push credential cleanup failed")


class _ArgumentParseError(ValueError):
    """워크플로 CLI 인수 검증 실패."""


class _ArgumentHelpRequested(Exception):
    """워크플로 CLI 도움말 출력 완료."""


class _WorkflowArgumentParser(argparse.ArgumentParser):
    """프로세스를 종료하지 않고 인수 오류를 전달하는 워크플로 파서."""

    def exit(self, status: int = 0, message: str | None = None) -> NoReturn:
        """도움말 출력을 프로세스 종료 없이 호출자에게 전달.

        Args:
            status: argparse 종료 상태.
            message: 종료 전에 출력할 선택 메시지.

        Raises:
            _ArgumentHelpRequested: 도움말을 정상적으로 출력한 경우.
            SystemExit: 0이 아닌 상태로 종료하는 경우.
        """

        if status == 0:
            if message:
                self._print_message(message, sys.stderr)
            raise _ArgumentHelpRequested
        super().exit(status, message)

    def error(self, message: str) -> NoReturn:
        """인수 오류를 제어된 예외로 변환.

        Args:
            message: argparse가 생성한 오류 설명.

        Raises:
            _ArgumentParseError: 사용자가 잘못된 인수를 전달한 경우.
        """

        self.print_usage(sys.stderr)
        print(f"{self.prog}: error: {message}", file=sys.stderr)
        raise _ArgumentParseError(message)


def _is_oid(value: object) -> bool:
    """정규 SHA-1 또는 SHA-256 객체 ID 여부."""

    return (
        isinstance(value, str)
        and len(value) in _FULL_OID_LENGTHS
        and value == value.lower()
        and all(character in "0123456789abcdef" for character in value)
    )


def _is_sha256(value: object) -> bool:
    """정규 SHA-256 16진수 문자열 여부."""

    return (
        isinstance(value, str)
        and len(value) == 64
        and value == value.lower()
        and all(character in "0123456789abcdef" for character in value)
    )


def _deploy_repository(value: object) -> str:
    """배포 저장소의 명시적 ``owner/name`` 값 검증."""

    if not isinstance(value, str) or not _DEPLOY_REPOSITORY.fullmatch(value):
        raise EntrypointError(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="state-read",
        )
    return value


def _artifact_root(value: Path) -> Path:
    """활성 저장소와 분리된 기존 산출물 루트 검증."""

    if value.is_symlink() or not value.is_dir():
        raise EntrypointError(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="configuration",
        )
    root = value.resolve()
    repository = REPOSITORY_ROOT.resolve()
    if (
        root == repository
        or root.is_relative_to(repository)
        or repository.is_relative_to(root)
    ):
        raise EntrypointError(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="configuration",
        )
    return root


def _candidate_directory(root: Path, relative: str) -> Path:
    """산출물 루트 내부의 실제 후보 디렉터리 해석."""

    current = root
    try:
        for component in relative.split("/"):
            current = current / component
            if not stat.S_ISDIR(current.lstat().st_mode):
                raise ValueError("candidate path component is not a directory")
        resolved = current.resolve(strict=True)
    except OSError as exc:
        raise ValueError("candidate directory cannot be resolved") from exc
    if not resolved.is_relative_to(root):
        raise ValueError("candidate directory escaped the artifact root")
    return resolved


def _read_artifact(
    root: Path,
    filename: str,
    *,
    maximum: int,
    private: bool = False,
) -> bytes:
    """심볼릭 링크와 교체 경쟁을 차단한 제한적 산출물 읽기."""

    directory_flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        directory_flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        directory_flags |= os.O_NOFOLLOW
    directory = os.open(root, directory_flags)
    try:
        before = os.fstat(directory)
        file_flags = os.O_RDONLY
        if hasattr(os, "O_CLOEXEC"):
            file_flags |= os.O_CLOEXEC
        if hasattr(os, "O_NOFOLLOW"):
            file_flags |= os.O_NOFOLLOW
        descriptor = os.open(filename, file_flags, dir_fd=directory)
        try:
            metadata = os.fstat(descriptor)
            if (
                not stat.S_ISREG(metadata.st_mode)
                or metadata.st_size <= 0
                or metadata.st_size > maximum
                or (private and metadata.st_mode & 0o077)
            ):
                raise EntrypointError(
                    IssueCode.INVALID_RUNTIME_OPTION,
                    stage="state-read",
                )
            chunks: list[bytes] = []
            remaining = metadata.st_size
            while remaining:
                chunk = os.read(descriptor, min(remaining, 64 * 1024))
                if not chunk:
                    raise EntrypointError(
                        IssueCode.RUNNER_OPERATION_FAILED,
                        stage="state-read",
                    )
                chunks.append(chunk)
                remaining -= len(chunk)
        finally:
            os.close(descriptor)
        if not os.path.samestat(before, root.stat()):
            raise EntrypointError(
                IssueCode.RUNNER_OPERATION_FAILED,
                stage="state-read",
            )
        return b"".join(chunks)
    except FileNotFoundError as exc:
        raise EntrypointError(
            IssueCode.REQUIRED_CONFIG_MISSING,
            stage="state-read",
        ) from exc
    except OSError as exc:
        raise EntrypointError(
            IssueCode.RUNNER_OPERATION_FAILED,
            stage="state-read",
        ) from exc
    finally:
        os.close(directory)


def _load_json_artifact(root: Path, filename: str) -> dict[str, object]:
    """정규 JSON 산출물을 매핑으로 로드."""

    raw = _read_artifact(root, filename, maximum=_MAX_STATE_BYTES)
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise EntrypointError(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="state-read",
        ) from exc
    if (
        not isinstance(value, dict)
        or raw != _canonical_json(value)
    ):
        raise EntrypointError(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="state-read",
        )
    return value


def _preparation_key(root: Path) -> bytes:
    """비공개 모드로 기록된 256비트 준비 키 로드."""

    key = _read_artifact(
        root,
        PREPARATION_KEY_FILENAME,
        maximum=64,
        private=True,
    )
    if len(key) != 32:
        raise EntrypointError(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="state-read",
        )
    return key


def _short_identifier(value: object) -> str:
    """상태에 포함된 짧고 비밀 정보가 없는 식별자 검증."""

    if (
        not isinstance(value, str)
        or not value
        or len(value) > 128
        or not value[0].isalnum()
        or any(not (character.isalnum() or character in "._-") for character in value)
    ):
        raise EntrypointError(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="state-read",
        )
    return value


def _branch_name(value: object) -> str:
    """상태에 포함된 Git 브랜치 이름의 안전한 구문 검증."""

    if (
        not isinstance(value, str)
        or not value
        or len(value) > 240
        or value.startswith(("-", "/", "."))
        or value.endswith(("/", "."))
        or ".." in value
        or "@{" in value
        or any(
            ord(character) < 32
            or ord(character) == 127
            or character in " ~^:?*[\\"
            for character in value
        )
        or any(
            not component
            or component.startswith(".")
            or component.endswith(".lock")
            for component in value.split("/")
        )
    ):
        raise EntrypointError(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="state-read",
        )
    return value


def _deadline(value: object) -> WorkflowDeadline:
    """상태의 유한한 단조 시계 값을 워크플로 기한으로 변환."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise EntrypointError(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="state-read",
        )
    parsed = float(value)
    if not math.isfinite(parsed):
        raise EntrypointError(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="state-read",
        )
    return WorkflowDeadline(expires_at=parsed)


def _exact_mapping(
    value: object,
    expected_keys: set[str],
) -> dict[str, object]:
    """정확한 키 집합을 가진 JSON 매핑 검증.

    Args:
        value: 매핑 여부를 확인할 JSON 값.
        expected_keys: 허용할 전체 키 집합.

    Returns:
        키 검증을 마친 매핑.

    Raises:
        ValueError: 값이 매핑이 아니거나 키 집합이 다른 경우.
    """

    if not isinstance(value, dict) or set(value) != expected_keys:
        raise ValueError("state mapping has unexpected fields")
    return value


def _required_state_string(
    value: Mapping[str, object],
    key: str,
) -> str:
    """상태 매핑의 필수 문자열 필드 검증."""

    field = value[key]
    if not isinstance(field, str):
        raise TypeError(f"state field {key} must be a string")
    return field


def _canonical_state_oid(value: object) -> str:
    """상태 필드를 정규 Git 객체 ID로 검증."""

    if not isinstance(value, str) or not _is_oid(value):
        raise ValueError("state field must be a canonical Git object ID")
    return value


def _state_sha256(value: object) -> str:
    """상태 필드를 정규 SHA-256 문자열로 검증."""

    if not isinstance(value, str) or not _is_sha256(value):
        raise ValueError("state field must be a canonical SHA-256 digest")
    return value


def _prepared_state_parts(
    value: Mapping[str, object],
    deploy_repository: str,
) -> _PreparedStateParts:
    """준비 상태의 중첩 매핑과 배포 호스트 검증."""

    push_endpoint = value["push_endpoint"]
    if not isinstance(push_endpoint, str):
        raise TypeError("push endpoint must be a string")
    deploy_host = _deployment_host_for(push_endpoint, deploy_repository)
    if value["deploy_host"] != deploy_host:
        raise ValueError("deploy host does not match the push endpoint")
    return _PreparedStateParts(
        push_endpoint=push_endpoint,
        deploy_host=deploy_host,
        base=_exact_mapping(
            value["base"],
            {"head", "tree", "remote_ref", "remote_oid", "active_fingerprint"},
        ),
        candidate=_exact_mapping(
            value["candidate"],
            {"path", "base_commit", "verified_tree", "has_changes"},
        ),
        replay=_exact_mapping(
            value["replay"],
            {
                "manifest_file",
                "manifest_digest",
                "selector_base64",
                "selector_digest",
            },
        ),
        fixture=_exact_mapping(
            value["fixture"],
            {"evidence_file", "evidence_digest"},
        ),
    )


def _prepared_base(
    value: Mapping[str, object],
    branch: str,
) -> PublicationBase:
    """준비 상태의 게시 기준본 검증."""

    base = PublicationBase(
        head=_required_state_string(value, "head"),
        tree=_required_state_string(value, "tree"),
        remote_ref=_required_state_string(value, "remote_ref"),
        active_fingerprint=_required_state_string(value, "active_fingerprint"),
    )
    if value["remote_oid"] != base.head:
        raise ValueError("remote OID does not match the base head")
    if base.remote_ref != f"refs/heads/{branch}":
        raise ValueError("remote ref does not match the branch")
    return base


def _prepared_publication(
    value: object,
    candidate: Mapping[str, object],
    base: PublicationBase,
) -> tuple[PreparedPublication, bool]:
    """게시 계획과 후보 트리 식별 정보의 일관성 검증."""

    if not isinstance(value, Mapping):
        raise TypeError("prepared publication must be a mapping")
    prepared = PreparedPublication.from_mapping(value)
    has_changes = candidate["has_changes"]
    if not isinstance(has_changes, bool):
        raise TypeError("candidate change marker must be a boolean")
    if (
        prepared.base_head != base.head
        or prepared.base_tree != base.tree
        or prepared.remote_ref != base.remote_ref
        or candidate["base_commit"] != base.head
        or candidate["verified_tree"] != prepared.verified_tree
        or (prepared.commit_oid is not None) != has_changes
        or not _is_sha256(base.active_fingerprint)
    ):
        raise ValueError("prepared publication does not match the base state")
    return prepared, has_changes


def _prepared_candidate(
    root: Path,
    value: Mapping[str, object],
) -> tuple[str, Path]:
    """준비 상태의 상대 후보 경로 검증 및 해석."""

    relative = value["path"]
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ValueError("candidate path must be a relative POSIX path")
    if Path(relative).is_absolute() or any(
        part in {"", ".", ".."} for part in relative.split("/")
    ):
        raise ValueError("candidate path escapes the artifact root")
    return relative, _candidate_directory(root, relative)


def _verified_artifact_digest(
    root: Path,
    value: Mapping[str, object],
    *,
    filename_key: str,
    digest_key: str,
    expected_filename: str,
    maximum: int,
) -> str:
    """상태가 참조하는 산출물 이름과 SHA-256 다이제스트 검증."""

    if value[filename_key] != expected_filename:
        raise ValueError("artifact filename does not match the expected file")
    artifact = _read_artifact(root, expected_filename, maximum=maximum)
    digest = value[digest_key]
    if not isinstance(digest, str) or hashlib.sha256(artifact).hexdigest() != digest:
        raise ValueError("artifact digest does not match its contents")
    return digest


def _verify_prepared_artifacts(
    root: Path,
    replay: Mapping[str, object],
    fixture: Mapping[str, object],
) -> str:
    """재현 매니페스트·선택자·픽스처 증거의 식별 정보 검증."""

    manifest_digest = _verified_artifact_digest(
        root,
        replay,
        filename_key="manifest_file",
        digest_key="manifest_digest",
        expected_filename=MANIFEST_FILENAME,
        maximum=8_000_000,
    )
    selector = base64.b64decode(
        _required_state_string(replay, "selector_base64"),
        validate=True,
    )
    if hashlib.sha256(selector).hexdigest() != replay["selector_digest"]:
        raise ValueError("selector digest does not match its contents")
    _verified_artifact_digest(
        root,
        fixture,
        filename_key="evidence_file",
        digest_key="evidence_digest",
        expected_filename=FIXTURE_EVIDENCE_FILENAME,
        maximum=8192,
    )
    return manifest_digest


def _load_prepared_state(root: Path) -> PreparedState:
    """봉인된 준비 상태와 참조 산출물의 식별 정보 검증 및 로드."""

    key = _preparation_key(root)
    sealed = _load_json_artifact(root, PREPARED_STATE_FILENAME)
    try:
        value = verify_sealed_mapping(sealed, key)
    except ValueError as exc:
        raise EntrypointError(
            IssueCode.VERIFIED_TREE_MISMATCH,
            stage="state-read",
        ) from exc
    expected = {
        "schema_version",
        "run_id",
        "workflow_deadline_monotonic",
        "branch",
        "push_endpoint",
        "deploy_repository",
        "deploy_host",
        "deploy_workflow",
        "base",
        "replay",
        "fixture",
        "candidate",
        "publication",
    }
    if set(value) != expected or value["schema_version"] != 1:
        raise EntrypointError(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="state-read",
        )
    try:
        run_id = _short_identifier(value["run_id"])
        branch = _branch_name(value["branch"])
        deploy_repository = _deploy_repository(value["deploy_repository"])
        deploy_workflow = _short_identifier(value["deploy_workflow"])
        parts = _prepared_state_parts(value, deploy_repository)
        base = _prepared_base(parts.base, branch)
        prepared, has_changes = _prepared_publication(
            value["publication"],
            parts.candidate,
            base,
        )
        candidate_relative, candidate_path = _prepared_candidate(
            root,
            parts.candidate,
        )
        manifest_digest = _verify_prepared_artifacts(
            root,
            parts.replay,
            parts.fixture,
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise EntrypointError(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="state-read",
        ) from exc
    return PreparedState(
        run_id=run_id,
        workflow_deadline=_deadline(value["workflow_deadline_monotonic"]),
        branch=branch,
        push_endpoint=parts.push_endpoint,
        deploy_repository=deploy_repository,
        deploy_host=parts.deploy_host,
        deploy_workflow=deploy_workflow,
        manifest_digest=manifest_digest,
        base=base,
        candidate_path=candidate_path,
        candidate_relative=candidate_relative,
        has_changes=has_changes,
        prepared=prepared,
        preparation_key=key,
    )


def _load_published_state(root: Path) -> PublishedState:
    """봉인된 게시 상태와 게시 식별 정보 검증 및 로드."""

    key = _preparation_key(root)
    sealed = _load_json_artifact(root, PUBLISHED_STATE_FILENAME)
    try:
        value = verify_sealed_mapping(sealed, key)
    except ValueError as exc:
        raise EntrypointError(
            IssueCode.VERIFIED_TREE_MISMATCH,
            stage="state-read",
        ) from exc
    expected = {
        "schema_version",
        "run_id",
        "workflow_deadline_monotonic",
        "branch",
        "push_endpoint",
        "deploy_repository",
        "deploy_host",
        "deploy_workflow",
        "manifest_digest",
        "active_fingerprint",
        "base_commit",
        "published_commit",
        "remote_commit",
        "has_changes",
    }
    if set(value) != expected or value["schema_version"] != 1:
        raise EntrypointError(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="state-read",
        )
    try:
        run_id = _short_identifier(value["run_id"])
        branch = _branch_name(value["branch"])
        push_endpoint = _required_state_string(value, "push_endpoint")
        deploy_repository = _deploy_repository(value["deploy_repository"])
        deploy_host = _deployment_host_for(push_endpoint, deploy_repository)
        deploy_workflow = _short_identifier(value["deploy_workflow"])
        base_commit, published_commit, remote_commit = (
            _canonical_state_oid(value[key])
            for key in ("base_commit", "published_commit", "remote_commit")
        )
        manifest_digest = _state_sha256(value["manifest_digest"])
        active_fingerprint = _state_sha256(value["active_fingerprint"])
        has_changes = value["has_changes"]
        if (
            len({len(base_commit), len(published_commit), len(remote_commit)}) != 1
            or not isinstance(has_changes, bool)
            or value["deploy_host"] != deploy_host
        ):
            raise ValueError
    except (KeyError, TypeError, ValueError) as exc:
        raise EntrypointError(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="state-read",
        ) from exc
    return PublishedState(
        run_id=run_id,
        workflow_deadline=_deadline(value["workflow_deadline_monotonic"]),
        branch=branch,
        push_endpoint=push_endpoint,
        deploy_repository=deploy_repository,
        deploy_host=deploy_host,
        deploy_workflow=deploy_workflow,
        manifest_digest=manifest_digest,
        active_fingerprint=active_fingerprint,
        base_commit=base_commit,
        published_commit=published_commit,
        remote_commit=remote_commit,
        has_changes=has_changes,
        preparation_key=key,
    )


def _failure_event(code: IssueCode, *, stage: str) -> FailureEvent:
    """진입점 오류 코드를 안정적 실패 이벤트로 변환."""

    attempts = (
        ProviderAttempts(response_evaluation=0, transport=0)
        if classification_for(code) is ErrorClassification.TRANSLATION
        else None
    )
    return FailureEvent(
        code=code,
        stage=stage,
        message=f"workflow phase failed with {code.value}",
        attempts=attempts,
    )


def _phase_failure(
    *,
    root: Path | None,
    run_id: str | None,
    code: IssueCode,
    stage: str,
    base_head: str | None = None,
    manifest_digest: str | None = None,
    published_commit: str | None = None,
    candidate_debug_path: str | None = None,
    active_fingerprint: str | None = None,
    workflow_deadline: WorkflowDeadline | None = None,
    preceding_failures: Sequence[FailureEvent] = (),
) -> int:
    """단계 실패의 우선순위를 정하고 정규 보고서로 기록."""

    failures = [*preceding_failures, _failure_event(code, stage=stage)]
    if (
        active_fingerprint is not None
        and workflow_deadline is not None
        and not any(
            failure.code
            in {
                IssueCode.ACTIVE_WORKTREE_MUTATED,
                IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            }
            for failure in failures
        )
    ):
        try:
            _verify_active_repository(
                expected_fingerprint=active_fingerprint,
                deadline=workflow_deadline,
                published_commit=published_commit,
            )
        except EntrypointError as exc:
            failures.append(_failure_event(exc.code, stage=exc.stage))
        except Exception:
            failures.append(
                _failure_event(
                    IssueCode.UNCLASSIFIED_INTERNAL,
                    stage="active-fingerprint",
                )
            )
    exit_code = final_exit_code(failures)
    if root is not None and run_id is not None:
        try:
            report = FailureReport.build(
                run_id=run_id,
                failures=failures,
                manifest_digest=manifest_digest,
                base_head=base_head,
                published_commit=published_commit,
                candidate_debug_path=candidate_debug_path,
            )
            if write_failure_report(report, artifact_root=root) is None:
                return int(exit_code)
        except (OSError, TypeError, ValueError):
            print(
                _REPORT_WRITE_FAILED,
                file=sys.stderr,
            )
    else:
        print(
            _REPORT_WRITE_FAILED,
            file=sys.stderr,
        )
    return int(exit_code)


def _verify_active_repository(
    *,
    expected_fingerprint: str,
    deadline: WorkflowDeadline,
    published_commit: str | None,
) -> None:
    """현재 활성 저장소가 준비 시점 지문과 동일한지 검증."""

    try:
        current = active_repository_fingerprint(
            REPOSITORY_ROOT,
            remaining_seconds=deadline.remaining_seconds,
        )
        deadline.phase_remaining()
    except RepositoryStateError as exc:
        raise EntrypointError(
            exc.code,
            stage="active-fingerprint",
            published_commit=published_commit,
        ) from exc
    except DeadlineExceeded as exc:
        raise EntrypointError(
            exc.code,
            stage="active-fingerprint",
            published_commit=published_commit,
        ) from exc
    except OSError as exc:
        raise EntrypointError(
            IssueCode.RUNNER_OPERATION_FAILED,
            stage="active-fingerprint",
            published_commit=published_commit,
        ) from exc
    if current != expected_fingerprint:
        raise EntrypointError(
            IssueCode.ACTIVE_WORKTREE_MUTATED,
            stage="active-fingerprint",
            published_commit=published_commit,
        )


def _base_process_environment(source: Mapping[str, str]) -> dict[str, str]:
    """자격 증명을 제외한 하위 프로세스 기본 환경 구성."""

    allowed = {
        "LANG",
        "LC_ALL",
        "PATH",
        "SSL_CERT_DIR",
        "SSL_CERT_FILE",
        "SYSTEMROOT",
        "TEMP",
        "TMP",
        "TMPDIR",
    }
    return {
        key: value
        for key, value in source.items()
        if isinstance(value, str)
        and value
        and (key in allowed or key.startswith("LC_"))
    }


@contextmanager
def _push_environment(
    endpoint: str,
    source: Mapping[str, str],
) -> Iterator[dict[str, str]]:
    """HTTPS 자격 증명을 일회용 ``askpass`` 도우미로 격리한 푸시 환경 제공."""

    environment = _base_process_environment(source)
    parsed = urlsplit(endpoint)
    if parsed.scheme in {"http", "https"}:
        token = source.get("GH_TOKEN") or source.get("GITHUB_TOKEN")
        if (
            not isinstance(token, str)
            or not token
            or "\0" in token
            or "\n" in token
            or "\r" in token
        ):
            raise EntrypointError(
                IssueCode.PUBLICATION_CREDENTIAL_UNAVAILABLE,
                stage="publication",
            )
        temporary = tempfile.TemporaryDirectory(
            prefix="translation-sync-askpass-"
        )
        pending_error: Exception | None = None
        try:
            tmp = temporary.name
            helper = Path(tmp) / "askpass.py"
            script = (
                f"#!{sys.executable}\n"
                "import os, sys\n"
                "prompt = sys.argv[1].lower() if len(sys.argv) > 1 else ''\n"
                "key = 'TRANSLATION_SYNC_PUSH_USERNAME' if 'username' in prompt "
                "else 'TRANSLATION_SYNC_PUSH_TOKEN'\n"
                "sys.stdout.write(os.environ[key] + '\\n')\n"
            ).encode("utf-8")
            descriptor = os.open(
                helper,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o700,
            )
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(script)
            environment.update(
                {
                    "GIT_ASKPASS": str(helper),
                    "GIT_ASKPASS_REQUIRE": "force",
                    "TRANSLATION_SYNC_PUSH_USERNAME": "x-access-token",
                    "TRANSLATION_SYNC_PUSH_TOKEN": token,
                }
            )
            yield environment
        except Exception as exc:
            pending_error = exc
            raise
        finally:
            try:
                temporary.cleanup()
            except OSError as exc:
                raise _PushEnvironmentCleanupError(pending_error) from exc
        return
    if Path(endpoint).is_absolute() or parsed.scheme == "file":
        yield environment
        return
    raise EntrypointError(
        IssueCode.PUBLICATION_CREDENTIAL_UNAVAILABLE,
        stage="publication",
    )


def run_prepare(
    args: argparse.Namespace,
    *,
    environment: Mapping[str, str],
    started_at: float,
) -> int:
    """승인된 기준본에서 봉인된 게시 준비 상태 생성까지 순차 실행.

    Args:
        args: ``prepare`` 하위 명령의 검증 전 ``argparse`` 네임스페이스.
        environment: 단계별 정제에 사용할 원본 환경 변수.
        started_at: 진입점 진입 직후의 단조 시계 값.

    Returns:
        안정적 워크플로 종료 코드.
    """

    run_id = secrets.token_hex(16)
    root: Path | None = None
    try:
        root = _artifact_root(args.artifact_root)
        settings = load_workflow_settings(SETTINGS_PATH)
        request = PrepareRequest(
            repository=REPOSITORY_ROOT,
            artifact_root=root,
            push_endpoint=args.push_endpoint,
            deploy_repository=args.repository,
            branch=args.branch,
            commit_message=args.commit_message,
            version=args.version,
            document=args.doc,
        )
        outcome = WorkflowPreparer(
            settings=settings,
            environment=environment,
            hooks=default_workflow_hooks(environment),
            run_id_factory=lambda: run_id,
            workflow_started_at=started_at,
        ).prepare(request)
        return int(outcome.exit_code)
    except EntrypointError as exc:
        return _phase_failure(
            root=root,
            run_id=run_id,
            code=exc.code,
            stage=exc.stage,
        )
    except SettingsError:
        return _phase_failure(
            root=root,
            run_id=run_id,
            code=IssueCode.REQUIRED_CONFIG_MISSING,
            stage="configuration",
        )
    except OSError:
        return _phase_failure(
            root=root,
            run_id=run_id,
            code=IssueCode.RUNNER_OPERATION_FAILED,
            stage="configuration",
        )
    except (TypeError, ValueError):
        return _phase_failure(
            root=root,
            run_id=run_id,
            code=IssueCode.INVALID_RUNTIME_OPTION,
            stage="configuration",
        )
    except Exception:
        return _phase_failure(
            root=root,
            run_id=run_id,
            code=IssueCode.UNCLASSIFIED_INTERNAL,
            stage="configuration",
        )


def _publication_phase_failure(
    *,
    root: Path | None,
    state: PreparedState | None,
    code: IssueCode,
    stage: str,
    published_commit: str | None,
    preceding_failures: Sequence[FailureEvent] = (),
) -> int:
    """게시 진행 상태를 공통 실패 보고 인수로 변환."""

    if state is None:
        return _phase_failure(
            root=root,
            run_id=None,
            code=code,
            stage=stage,
            published_commit=published_commit,
            preceding_failures=preceding_failures,
        )
    return _phase_failure(
        root=root,
        run_id=state.run_id,
        code=code,
        stage=stage,
        base_head=state.base.head,
        manifest_digest=state.manifest_digest,
        published_commit=published_commit,
        candidate_debug_path=state.candidate_relative,
        active_fingerprint=state.base.active_fingerprint,
        workflow_deadline=state.workflow_deadline,
        preceding_failures=preceding_failures,
    )


def _publication_cleanup_failure(
    *,
    root: Path | None,
    state: PreparedState | None,
    published_commit: str | None,
    error: _PushEnvironmentCleanupError,
) -> int:
    """푸시 환경 정리 실패와 정리 전 실패를 함께 보고."""

    pending_failure: FailureEvent | None = None
    pending = error.pending_error
    if isinstance(pending, PublicationError):
        published_commit = pending.published_commit or published_commit
        pending_failure = _failure_event(pending.code, stage="publication")
    elif isinstance(pending, DeadlineExceeded):
        pending_failure = _failure_event(pending.code, stage="publication")
    elif isinstance(pending, EntrypointError):
        published_commit = pending.published_commit or published_commit
        pending_failure = _failure_event(pending.code, stage=pending.stage)
    preceding = (pending_failure,) if pending_failure is not None else ()
    return _publication_phase_failure(
        root=root,
        state=state,
        code=IssueCode.RUNNER_OPERATION_FAILED,
        stage="publication",
        published_commit=published_commit,
        preceding_failures=preceding,
    )


def _publication_result_is_valid(
    state: PreparedState,
    result: object,
) -> bool:
    """게시 결과가 봉인된 준비 상태와 일치하는지 여부."""

    if not isinstance(result, PublicationResult):
        return False
    expected_commit = state.prepared.commit_oid or state.base.head
    return (
        result.published_oid == expected_commit
        and result.commit_oid == state.prepared.commit_oid
        and result.pushed == state.has_changes
    )


def run_publish(
    args: argparse.Namespace,
    *,
    environment: Mapping[str, str],
) -> int:
    """봉인된 준비 트리를 실행 브랜치와 원격 저장소에 게시.

    Args:
        args: ``publish`` 하위 명령의 ``argparse`` 네임스페이스.
        environment: Git 푸시에 필요한 원본 환경 변수.

    Returns:
        안정적 워크플로 종료 코드.
    """

    root: Path | None = None
    state: PreparedState | None = None
    published_commit: str | None = None
    try:
        root = _artifact_root(args.artifact_root)
        if any(
            path.exists() or path.is_symlink()
            for path in (
                root / PUBLISHED_STATE_FILENAME,
                root / REPORT_FILENAME,
            )
        ):
            raise EntrypointError(
                IssueCode.INVALID_RUNTIME_OPTION,
                stage="publication",
            )
        state = _load_prepared_state(root)
        state.workflow_deadline.phase_remaining()

        def read_fingerprint(timeout: float) -> str:
            """게시 제한 시간과 공통 기한 안에서 활성 저장소 지문 조회."""

            try:
                return active_repository_fingerprint(
                    REPOSITORY_ROOT,
                    remaining_seconds=lambda: min(
                        timeout,
                        state.workflow_deadline.remaining_seconds(),
                    ),
                )
            except RepositoryStateError as exc:
                raise PublicationError(exc.code) from exc

        publisher = Publisher(
            candidate_repo=state.candidate_path,
            push_endpoint=state.push_endpoint,
            base=state.base,
            read_active_fingerprint=read_fingerprint,
            remaining_seconds=state.workflow_deadline.remaining_seconds,
            prepare_environment=_prepare_git_environment(environment),
            preparation_key=state.preparation_key,
        )
        with _push_environment(state.push_endpoint, environment) as push_environment:
            try:
                result = publisher.publish(
                    state.prepared,
                    push_environment=push_environment,
                )
            except PublicationError as exc:
                published_commit = exc.published_commit or published_commit
                raise
            if not _publication_result_is_valid(state, result):
                raise EntrypointError(
                    IssueCode.VERIFIED_TREE_MISMATCH,
                    stage="publication",
                )
            published_commit = result.published_oid
        state.workflow_deadline.phase_remaining()
        published = _sealed_mapping(
            {
                "schema_version": 1,
                "run_id": state.run_id,
                "workflow_deadline_monotonic": state.workflow_deadline.expires_at,
                "branch": state.branch,
                "push_endpoint": state.push_endpoint,
                "deploy_repository": state.deploy_repository,
                "deploy_host": state.deploy_host,
                "deploy_workflow": state.deploy_workflow,
                "manifest_digest": state.manifest_digest,
                "active_fingerprint": state.base.active_fingerprint,
                "base_commit": state.base.head,
                "published_commit": result.published_oid,
                "remote_commit": result.published_oid,
                "has_changes": state.has_changes,
            },
            state.preparation_key,
        )
        _write_no_replace(
            root / PUBLISHED_STATE_FILENAME,
            _canonical_json(published),
        )
        _verify_active_repository(
            expected_fingerprint=state.base.active_fingerprint,
            deadline=state.workflow_deadline,
            published_commit=published_commit,
        )
        return int(ExitCode.SUCCESS)
    except _PushEnvironmentCleanupError as exc:
        return _publication_cleanup_failure(
            root=root,
            state=state,
            published_commit=published_commit,
            error=exc,
        )
    except PublicationError as exc:
        return _publication_phase_failure(
            root=root,
            state=state,
            code=exc.code,
            stage="publication",
            published_commit=exc.published_commit or published_commit,
        )
    except DeadlineExceeded as exc:
        return _publication_phase_failure(
            root=root,
            state=state,
            code=exc.code,
            stage="publication",
            published_commit=published_commit,
        )
    except EntrypointError as exc:
        return _publication_phase_failure(
            root=root,
            state=state,
            code=exc.code,
            stage=exc.stage,
            published_commit=exc.published_commit or published_commit,
        )
    except OSError:
        return _publication_phase_failure(
            root=root,
            state=state,
            code=IssueCode.RUNNER_OPERATION_FAILED,
            stage="publication",
            published_commit=published_commit,
        )
    except (TypeError, ValueError):
        return _publication_phase_failure(
            root=root,
            state=state,
            code=IssueCode.INVALID_RUNTIME_OPTION,
            stage="publication",
            published_commit=published_commit,
        )
    except Exception:
        return _publication_phase_failure(
            root=root,
            state=state,
            code=IssueCode.UNCLASSIFIED_INTERNAL,
            stage="publication",
            published_commit=published_commit,
        )


def _deployment_phase_failure(
    *,
    root: Path | None,
    state: PublishedState | None,
    code: IssueCode,
    stage: str,
    published_commit: str | None = None,
) -> int:
    """배포 진행 상태를 공통 실패 보고 인수로 변환."""

    if state is None:
        return _phase_failure(
            root=root,
            run_id=None,
            code=code,
            stage=stage,
            published_commit=published_commit,
        )
    return _phase_failure(
        root=root,
        run_id=state.run_id,
        code=code,
        stage=stage,
        base_head=state.base_commit,
        manifest_digest=state.manifest_digest,
        published_commit=published_commit or state.published_commit,
        active_fingerprint=state.active_fingerprint,
        workflow_deadline=state.workflow_deadline,
    )


def _deployment_result_matches_branch(
    state: PublishedState,
    result: DeploymentResult,
) -> bool:
    """배포 결과가 대상 브랜치의 실행 규약을 충족하는지 여부."""

    if state.branch == "main":
        return (
            result.triggered
            and isinstance(result.correlation_id, str)
            and bool(result.correlation_id)
            and not isinstance(result.run_id, bool)
            and isinstance(result.run_id, int)
            and result.run_id > 0
            and result.conclusion == "success"
        )
    return not result.triggered and all(
        value is None
        for value in (
            result.correlation_id,
            result.run_id,
            result.conclusion,
        )
    )


def _validated_deployment_result(
    state: PublishedState,
    value: object,
) -> DeploymentResult:
    """배포 조정기 결과의 식별 정보와 브랜치별 규약 검증."""

    if (
        not isinstance(value, DeploymentResult)
        or value.branch != state.branch
        or value.published_commit != state.published_commit
        or not isinstance(value.issue_code, (IssueCode, type(None)))
    ):
        raise EntrypointError(
            IssueCode.DEPLOY_VALIDATION_FAILED,
            stage="deploy",
            published_commit=state.published_commit,
        )
    if value.issue_code is not None:
        raise EntrypointError(
            value.issue_code,
            stage="deploy",
            published_commit=state.published_commit,
        )
    if not _deployment_result_matches_branch(state, value):
        raise EntrypointError(
            IssueCode.DEPLOY_VALIDATION_FAILED,
            stage="deploy",
            published_commit=state.published_commit,
        )
    return value


def run_deploy(
    args: argparse.Namespace,
    *,
    environment: Mapping[str, str],
) -> int:
    """게시 상태를 검증하고 ``main`` 브랜치 배포 결과 확인.

    Args:
        args: ``deploy`` 하위 명령의 ``argparse`` 네임스페이스.
        environment: 배포 조정기에 전달할 원본 환경 변수.

    Returns:
        안정적 워크플로 종료 코드.
    """

    root: Path | None = None
    state: PublishedState | None = None
    try:
        root = _artifact_root(args.artifact_root)
        if any(
            path.exists() or path.is_symlink()
            for path in (
                root / DEPLOYED_STATE_FILENAME,
                root / REPORT_FILENAME,
            )
        ):
            raise EntrypointError(
                IssueCode.INVALID_RUNTIME_OPTION,
                stage="deploy",
            )
        state = _load_published_state(root)
        state.workflow_deadline.phase_remaining()
        _verify_active_repository(
            expected_fingerprint=state.active_fingerprint,
            deadline=state.workflow_deadline,
            published_commit=state.published_commit,
        )
        prefix = args.correlation_prefix or (
            "sync-" + hashlib.sha256(state.run_id.encode("utf-8")).hexdigest()[:20]
        )
        deploy_environment = dict(environment)
        deploy_environment["GH_HOST"] = state.deploy_host
        coordinator = DeploymentCoordinator(
            repository=state.deploy_repository,
            correlation_id=prefix,
            remaining_seconds=state.workflow_deadline.remaining_seconds,
            workflow_file=state.deploy_workflow,
            runner=SubprocessArgvRunner(deploy_environment),
        )
        result = _validated_deployment_result(
            state,
            coordinator.deploy(
                DeploymentRequest(
                    branch=state.branch,
                    base_commit=state.base_commit,
                    published_commit=state.published_commit,
                    remote_commit=state.remote_commit,
                    has_changes=state.has_changes,
                )
            ),
        )
        state.workflow_deadline.phase_remaining()
        deployed = _sealed_mapping(
            {
                "schema_version": 1,
                "run_id": state.run_id,
                "branch": state.branch,
                "deploy_repository": state.deploy_repository,
                "manifest_digest": state.manifest_digest,
                "active_fingerprint": state.active_fingerprint,
                "published_commit": state.published_commit,
                "triggered": result.triggered,
                "correlation_id": result.correlation_id,
                "deploy_run_id": result.run_id,
                "conclusion": result.conclusion,
            },
            state.preparation_key,
        )
        _write_no_replace(
            root / DEPLOYED_STATE_FILENAME,
            _canonical_json(deployed),
        )
        _verify_active_repository(
            expected_fingerprint=state.active_fingerprint,
            deadline=state.workflow_deadline,
            published_commit=state.published_commit,
        )
        return int(ExitCode.SUCCESS)
    except DeadlineExceeded as exc:
        return _deployment_phase_failure(
            root=root,
            state=state,
            code=exc.code,
            stage="deploy",
        )
    except EntrypointError as exc:
        return _deployment_phase_failure(
            root=root,
            state=state,
            code=exc.code,
            stage=exc.stage,
            published_commit=exc.published_commit,
        )
    except OSError:
        return _deployment_phase_failure(
            root=root,
            state=state,
            code=IssueCode.RUNNER_OPERATION_FAILED,
            stage="deploy",
        )
    except (TypeError, ValueError):
        return _deployment_phase_failure(
            root=root,
            state=state,
            code=IssueCode.INVALID_RUNTIME_OPTION,
            stage="deploy",
        )
    except Exception:
        return _deployment_phase_failure(
            root=root,
            state=state,
            code=IssueCode.UNCLASSIFIED_INTERNAL,
            stage="deploy",
        )


def _parser() -> argparse.ArgumentParser:
    """``prepare``, ``publish``, ``deploy`` 하위 명령 파서 구성."""

    parser = _WorkflowArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare")
    prepare.add_argument("--artifact-root", required=True, type=Path)
    prepare.add_argument("--push-endpoint", required=True)
    prepare.add_argument("--repository", required=True)
    prepare.add_argument("--branch", required=True)
    prepare.add_argument(
        "--commit-message",
        default="docs: synchronize translations",
    )
    prepare.add_argument("--version")
    prepare.add_argument("--doc")

    publish = subparsers.add_parser("publish")
    publish.add_argument("--artifact-root", required=True, type=Path)

    deploy = subparsers.add_parser("deploy")
    deploy.add_argument("--artifact-root", required=True, type=Path)
    deploy.add_argument("--correlation-prefix")
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    environment: Mapping[str, str] | None = None,
) -> int:
    """워크플로 하위 명령을 실행하고 제어된 종료 코드 반환.

    Args:
        argv: 선택적으로 주입한 명령행 인수. 생략 시 ``sys.argv`` 사용.
        environment: 선택적으로 주입한 환경 변수. 생략 시 현재 환경 사용.

    Returns:
        선택한 단계의 안정적 워크플로 종료 코드.
    """

    started_at = time.monotonic()
    try:
        args = _parser().parse_args(argv)
    except _ArgumentHelpRequested:
        return int(ExitCode.SUCCESS)
    except _ArgumentParseError:
        print(
            _REPORT_WRITE_FAILED,
            file=sys.stderr,
        )
        return int(ExitCode.CONTROLLED_FAILURE)
    env = os.environ if environment is None else environment
    if args.command == "prepare":
        return run_prepare(args, environment=env, started_at=started_at)
    if args.command == "publish":
        return run_publish(args, environment=env)
    if args.command == "deploy":
        return run_deploy(args, environment=env)
    return int(ExitCode.CONTROLLED_FAILURE)


if __name__ == "__main__":
    raise SystemExit(main())
