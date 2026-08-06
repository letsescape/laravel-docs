#!/usr/bin/env python3
"""격리된 단계에서 단일 번역 워크플로의 준비, publication 및 배포."""

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
from typing import Iterator, Mapping, Sequence
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


@dataclass(frozen=True, slots=True)
class PreparedState:
    """검증 후 publication 단계에 전달하는 봉인 해제 상태."""

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
    """publication 후 배포 단계에 전달하는 봉인 해제 상태."""

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


class EntrypointError(RuntimeError):
    """워크플로 entrypoint 경계의 안정된 오류."""

    def __init__(
        self,
        code: IssueCode,
        *,
        stage: str,
        published_commit: str | None = None,
    ) -> None:
        """entrypoint 오류 초기화."""

        self.code = code
        self.stage = stage
        self.published_commit = published_commit
        super().__init__(code.value)


class _PushEnvironmentCleanupError(OSError):
    """push credential 임시 환경 정리 실패."""

    def __init__(self, pending_error: Exception | None) -> None:
        """push 환경 cleanup 오류 초기화."""

        self.pending_error = pending_error
        super().__init__("push credential cleanup failed")


def _is_oid(value: object) -> bool:
    """canonical SHA-1 또는 SHA-256 객체 ID 여부."""

    return (
        isinstance(value, str)
        and len(value) in _FULL_OID_LENGTHS
        and value == value.lower()
        and all(character in "0123456789abcdef" for character in value)
    )


def _is_sha256(value: object) -> bool:
    """canonical SHA-256 16진수 문자열 여부."""

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
    """활성 저장소와 분리된 기존 artifact root 검증."""

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
    """artifact root 내부의 실제 candidate 디렉터리 해석."""

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
    """symlink와 교체 경쟁을 차단하며 제한된 artifact 읽기."""

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
    """canonical JSON artifact를 mapping으로 로딩."""

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
    """비공개 mode로 기록된 256 bit preparation key 로딩."""

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


def _short_identifier(value: object, *, name: str) -> str:
    """state 내부의 짧은 비밀정보 비포함 식별자 검증."""

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
    """state 내부 Git branch 이름의 안전한 구문 검증."""

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
    """state의 유한한 단조 시계 값을 워크플로 기한으로 변환."""

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


def _load_prepared_state(root: Path) -> PreparedState:
    """봉인된 prepared state와 참조 artifact의 identity 검증 및 로딩."""

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
        run_id = _short_identifier(value["run_id"], name="run_id")
        branch = _branch_name(value["branch"])
        deploy_repository = _deploy_repository(value["deploy_repository"])
        deploy_workflow = _short_identifier(
            value["deploy_workflow"],
            name="deploy_workflow",
        )
        push_endpoint = value["push_endpoint"]
        deploy_host = value["deploy_host"]
        base_value = value["base"]
        candidate_value = value["candidate"]
        replay_value = value["replay"]
        fixture_value = value["fixture"]
        if (
            not isinstance(push_endpoint, str)
            or deploy_host
            != _deployment_host_for(push_endpoint, deploy_repository)
            or not isinstance(base_value, dict)
            or set(base_value)
            != {"head", "tree", "remote_ref", "remote_oid", "active_fingerprint"}
            or not isinstance(candidate_value, dict)
            or set(candidate_value)
            != {"path", "base_commit", "verified_tree", "has_changes"}
            or not isinstance(replay_value, dict)
            or set(replay_value)
            != {
                "manifest_file",
                "manifest_digest",
                "selector_base64",
                "selector_digest",
            }
            or not isinstance(fixture_value, dict)
            or set(fixture_value) != {"evidence_file", "evidence_digest"}
        ):
            raise ValueError
        base = PublicationBase(
            head=base_value["head"],
            tree=base_value["tree"],
            remote_ref=base_value["remote_ref"],
            active_fingerprint=base_value["active_fingerprint"],
        )
        if base_value["remote_oid"] != base.head:
            raise ValueError
        if base.remote_ref != f"refs/heads/{branch}":
            raise ValueError
        prepared = PreparedPublication.from_mapping(value["publication"])
        if (
            prepared.base_head != base.head
            or prepared.base_tree != base.tree
            or prepared.remote_ref != base.remote_ref
            or candidate_value["base_commit"] != base.head
            or candidate_value["verified_tree"] != prepared.verified_tree
            or not isinstance(candidate_value["has_changes"], bool)
            or (prepared.commit_oid is not None) != candidate_value["has_changes"]
            or not _is_sha256(base.active_fingerprint)
        ):
            raise ValueError
        candidate_relative = candidate_value["path"]
        if (
            not isinstance(candidate_relative, str)
            or not candidate_relative
            or "\\" in candidate_relative
            or Path(candidate_relative).is_absolute()
            or any(part in {"", ".", ".."} for part in candidate_relative.split("/"))
        ):
            raise ValueError
        candidate_path = _candidate_directory(root, candidate_relative)
        if replay_value["manifest_file"] != MANIFEST_FILENAME:
            raise ValueError
        manifest = _read_artifact(
            root,
            MANIFEST_FILENAME,
            maximum=8_000_000,
        )
        if (
            not isinstance(replay_value["manifest_digest"], str)
            or hashlib.sha256(manifest).hexdigest()
            != replay_value["manifest_digest"]
        ):
            raise ValueError
        selector = base64.b64decode(
            replay_value["selector_base64"],
            validate=True,
        )
        if hashlib.sha256(selector).hexdigest() != replay_value["selector_digest"]:
            raise ValueError
        if fixture_value["evidence_file"] != FIXTURE_EVIDENCE_FILENAME:
            raise ValueError
        fixture_evidence = _read_artifact(
            root,
            FIXTURE_EVIDENCE_FILENAME,
            maximum=8192,
        )
        if (
            not isinstance(fixture_value["evidence_digest"], str)
            or hashlib.sha256(fixture_evidence).hexdigest()
            != fixture_value["evidence_digest"]
        ):
            raise ValueError
    except (KeyError, TypeError, ValueError) as exc:
        raise EntrypointError(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="state-read",
        ) from exc
    return PreparedState(
        run_id=run_id,
        workflow_deadline=_deadline(value["workflow_deadline_monotonic"]),
        branch=branch,
        push_endpoint=push_endpoint,
        deploy_repository=deploy_repository,
        deploy_host=deploy_host,
        deploy_workflow=deploy_workflow,
        manifest_digest=replay_value["manifest_digest"],
        base=base,
        candidate_path=candidate_path,
        candidate_relative=candidate_relative,
        has_changes=candidate_value["has_changes"],
        prepared=prepared,
        preparation_key=key,
    )


def _load_published_state(root: Path) -> PublishedState:
    """봉인된 published state와 publication identity 검증 및 로딩."""

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
        run_id = _short_identifier(value["run_id"], name="run_id")
        branch = _branch_name(value["branch"])
        push_endpoint = value["push_endpoint"]
        deploy_repository = _deploy_repository(value["deploy_repository"])
        deploy_host = value["deploy_host"]
        deploy_workflow = _short_identifier(
            value["deploy_workflow"],
            name="deploy_workflow",
        )
        oids = (
            value["base_commit"],
            value["published_commit"],
            value["remote_commit"],
        )
        if (
            not all(_is_oid(oid) for oid in oids)
            or len({len(oid) for oid in oids}) != 1
            or not isinstance(value["has_changes"], bool)
            or not _is_sha256(value["manifest_digest"])
            or not _is_sha256(value["active_fingerprint"])
            or not isinstance(push_endpoint, str)
            or deploy_host
            != _deployment_host_for(push_endpoint, deploy_repository)
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
        manifest_digest=value["manifest_digest"],
        active_fingerprint=value["active_fingerprint"],
        base_commit=value["base_commit"],
        published_commit=value["published_commit"],
        remote_commit=value["remote_commit"],
        has_changes=value["has_changes"],
        preparation_key=key,
    )


def _failure_event(code: IssueCode, *, stage: str) -> FailureEvent:
    """entrypoint 오류 코드를 안정된 실패 event로 변환."""

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
    """단계 실패를 우선순위화하고 canonical 보고서로 기록."""

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
                "REPORT_WRITE_FAILED: failure report could not be written",
                file=sys.stderr,
            )
    else:
        print(
            "REPORT_WRITE_FAILED: failure report could not be written",
            file=sys.stderr,
        )
    return int(exit_code)


def _verify_active_repository(
    *,
    expected_fingerprint: str,
    deadline: WorkflowDeadline,
    published_commit: str | None,
) -> None:
    """현재 활성 저장소가 준비 시점 fingerprint와 동일한지 검증."""

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
    """HTTPS credential을 일회성 askpass에 격리한 push 환경 제공."""

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
    """승인 기준본부터 봉인된 publication 준비 상태까지 순차 실행.

    Args:
        args: prepare 하위 명령의 검증 전 argparse namespace.
        environment: 단계별로 정제할 원본 환경 변수.
        started_at: entrypoint 진입 직후의 단조 시계 값.

    Returns:
        안정된 워크플로 종료 코드.
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


def run_publish(
    args: argparse.Namespace,
    *,
    environment: Mapping[str, str],
) -> int:
    """봉인된 prepared tree를 실행 branch와 원격에 publication.

    Args:
        args: publish 하위 명령의 argparse namespace.
        environment: Git push에 필요한 원본 환경 변수.

    Returns:
        안정된 워크플로 종료 코드.
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
            """publication timeout과 공유 기한으로 활성 fingerprint 조회."""

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
            expected_commit = state.prepared.commit_oid or state.base.head
            if (
                not isinstance(result, PublicationResult)
                or result.published_oid != expected_commit
                or result.commit_oid != state.prepared.commit_oid
                or result.pushed != state.has_changes
            ):
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
        pending_failure: FailureEvent | None = None
        pending = exc.pending_error
        if isinstance(pending, PublicationError):
            published_commit = pending.published_commit or published_commit
            pending_failure = _failure_event(
                pending.code,
                stage="publication",
            )
        elif isinstance(pending, DeadlineExceeded):
            pending_failure = _failure_event(
                pending.code,
                stage="publication",
            )
        elif isinstance(pending, EntrypointError):
            published_commit = pending.published_commit or published_commit
            pending_failure = _failure_event(
                pending.code,
                stage=pending.stage,
            )
        return _phase_failure(
            root=root,
            run_id=state.run_id if state is not None else None,
            code=IssueCode.RUNNER_OPERATION_FAILED,
            stage="publication",
            base_head=state.base.head if state is not None else None,
            manifest_digest=(state.manifest_digest if state is not None else None),
            published_commit=published_commit,
            candidate_debug_path=(
                state.candidate_relative if state is not None else None
            ),
            active_fingerprint=(
                state.base.active_fingerprint if state is not None else None
            ),
            workflow_deadline=(
                state.workflow_deadline if state is not None else None
            ),
            preceding_failures=(
                (pending_failure,) if pending_failure is not None else ()
            ),
        )
    except PublicationError as exc:
        return _phase_failure(
            root=root,
            run_id=state.run_id if state is not None else None,
            code=exc.code,
            stage="publication",
            base_head=state.base.head if state is not None else None,
            manifest_digest=(state.manifest_digest if state is not None else None),
            published_commit=exc.published_commit or published_commit,
            candidate_debug_path=(
                state.candidate_relative if state is not None else None
            ),
            active_fingerprint=(
                state.base.active_fingerprint if state is not None else None
            ),
            workflow_deadline=(
                state.workflow_deadline if state is not None else None
            ),
        )
    except DeadlineExceeded as exc:
        return _phase_failure(
            root=root,
            run_id=state.run_id if state is not None else None,
            code=exc.code,
            stage="publication",
            base_head=state.base.head if state is not None else None,
            manifest_digest=(state.manifest_digest if state is not None else None),
            published_commit=published_commit,
            candidate_debug_path=(
                state.candidate_relative if state is not None else None
            ),
            active_fingerprint=(
                state.base.active_fingerprint if state is not None else None
            ),
            workflow_deadline=(
                state.workflow_deadline if state is not None else None
            ),
        )
    except EntrypointError as exc:
        return _phase_failure(
            root=root,
            run_id=state.run_id if state is not None else None,
            code=exc.code,
            stage=exc.stage,
            base_head=state.base.head if state is not None else None,
            manifest_digest=(state.manifest_digest if state is not None else None),
            published_commit=exc.published_commit or published_commit,
            candidate_debug_path=(
                state.candidate_relative if state is not None else None
            ),
            active_fingerprint=(
                state.base.active_fingerprint if state is not None else None
            ),
            workflow_deadline=(
                state.workflow_deadline if state is not None else None
            ),
        )
    except OSError:
        return _phase_failure(
            root=root,
            run_id=state.run_id if state is not None else None,
            code=IssueCode.RUNNER_OPERATION_FAILED,
            stage="publication",
            base_head=state.base.head if state is not None else None,
            manifest_digest=(state.manifest_digest if state is not None else None),
            published_commit=published_commit,
            candidate_debug_path=(
                state.candidate_relative if state is not None else None
            ),
            active_fingerprint=(
                state.base.active_fingerprint if state is not None else None
            ),
            workflow_deadline=(
                state.workflow_deadline if state is not None else None
            ),
        )
    except (TypeError, ValueError):
        return _phase_failure(
            root=root,
            run_id=state.run_id if state is not None else None,
            code=IssueCode.INVALID_RUNTIME_OPTION,
            stage="publication",
            base_head=state.base.head if state is not None else None,
            manifest_digest=(state.manifest_digest if state is not None else None),
            published_commit=published_commit,
            candidate_debug_path=(
                state.candidate_relative if state is not None else None
            ),
            active_fingerprint=(
                state.base.active_fingerprint if state is not None else None
            ),
            workflow_deadline=(
                state.workflow_deadline if state is not None else None
            ),
        )
    except Exception:
        return _phase_failure(
            root=root,
            run_id=state.run_id if state is not None else None,
            code=IssueCode.UNCLASSIFIED_INTERNAL,
            stage="publication",
            base_head=state.base.head if state is not None else None,
            manifest_digest=(state.manifest_digest if state is not None else None),
            published_commit=published_commit,
            candidate_debug_path=(
                state.candidate_relative if state is not None else None
            ),
            active_fingerprint=(
                state.base.active_fingerprint if state is not None else None
            ),
            workflow_deadline=(
                state.workflow_deadline if state is not None else None
            ),
        )


def run_deploy(
    args: argparse.Namespace,
    *,
    environment: Mapping[str, str],
) -> int:
    """published state를 검증하고 main branch 배포 결과 확인.

    Args:
        args: deploy 하위 명령의 argparse namespace.
        environment: 배포 coordinator에 전달할 원본 환경 변수.

    Returns:
        안정된 워크플로 종료 코드.
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
        result = coordinator.deploy(
            DeploymentRequest(
                branch=state.branch,
                base_commit=state.base_commit,
                published_commit=state.published_commit,
                remote_commit=state.remote_commit,
                has_changes=state.has_changes,
            )
        )
        if (
            not isinstance(result, DeploymentResult)
            or result.branch != state.branch
            or result.published_commit != state.published_commit
            or not isinstance(result.issue_code, (IssueCode, type(None)))
        ):
            raise EntrypointError(
                IssueCode.DEPLOY_VALIDATION_FAILED,
                stage="deploy",
                published_commit=state.published_commit,
            )
        if not result.success:
            assert result.issue_code is not None
            raise EntrypointError(
                result.issue_code,
                stage="deploy",
                published_commit=state.published_commit,
            )
        if state.branch == "main":
            if (
                not result.triggered
                or not isinstance(result.correlation_id, str)
                or not result.correlation_id
                or isinstance(result.run_id, bool)
                or not isinstance(result.run_id, int)
                or result.run_id <= 0
                or result.conclusion != "success"
            ):
                raise EntrypointError(
                    IssueCode.DEPLOY_VALIDATION_FAILED,
                    stage="deploy",
                    published_commit=state.published_commit,
                )
        elif any(
            value is not None
            for value in (
                result.correlation_id,
                result.run_id,
                result.conclusion,
            )
        ) or result.triggered:
            raise EntrypointError(
                IssueCode.DEPLOY_VALIDATION_FAILED,
                stage="deploy",
                published_commit=state.published_commit,
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
        return _phase_failure(
            root=root,
            run_id=state.run_id if state is not None else None,
            code=exc.code,
            stage="deploy",
            base_head=state.base_commit if state is not None else None,
            manifest_digest=(state.manifest_digest if state is not None else None),
            published_commit=state.published_commit if state is not None else None,
            active_fingerprint=(
                state.active_fingerprint if state is not None else None
            ),
            workflow_deadline=(
                state.workflow_deadline if state is not None else None
            ),
        )
    except EntrypointError as exc:
        return _phase_failure(
            root=root,
            run_id=state.run_id if state is not None else None,
            code=exc.code,
            stage=exc.stage,
            base_head=state.base_commit if state is not None else None,
            manifest_digest=(state.manifest_digest if state is not None else None),
            published_commit=(
                exc.published_commit
                or (state.published_commit if state is not None else None)
            ),
            active_fingerprint=(
                state.active_fingerprint if state is not None else None
            ),
            workflow_deadline=(
                state.workflow_deadline if state is not None else None
            ),
        )
    except OSError:
        return _phase_failure(
            root=root,
            run_id=state.run_id if state is not None else None,
            code=IssueCode.RUNNER_OPERATION_FAILED,
            stage="deploy",
            base_head=state.base_commit if state is not None else None,
            manifest_digest=(state.manifest_digest if state is not None else None),
            published_commit=state.published_commit if state is not None else None,
            active_fingerprint=(
                state.active_fingerprint if state is not None else None
            ),
            workflow_deadline=(
                state.workflow_deadline if state is not None else None
            ),
        )
    except (TypeError, ValueError):
        return _phase_failure(
            root=root,
            run_id=state.run_id if state is not None else None,
            code=IssueCode.INVALID_RUNTIME_OPTION,
            stage="deploy",
            base_head=state.base_commit if state is not None else None,
            manifest_digest=(state.manifest_digest if state is not None else None),
            published_commit=state.published_commit if state is not None else None,
            active_fingerprint=(
                state.active_fingerprint if state is not None else None
            ),
            workflow_deadline=(
                state.workflow_deadline if state is not None else None
            ),
        )
    except Exception:
        return _phase_failure(
            root=root,
            run_id=state.run_id if state is not None else None,
            code=IssueCode.UNCLASSIFIED_INTERNAL,
            stage="deploy",
            base_head=state.base_commit if state is not None else None,
            manifest_digest=(state.manifest_digest if state is not None else None),
            published_commit=state.published_commit if state is not None else None,
            active_fingerprint=(
                state.active_fingerprint if state is not None else None
            ),
            workflow_deadline=(
                state.workflow_deadline if state is not None else None
            ),
        )


def _parser() -> argparse.ArgumentParser:
    """prepare, publish 및 deploy 하위 명령 parser 구성."""

    parser = argparse.ArgumentParser(description=__doc__)
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
    """워크플로 하위 명령을 제어된 종료 코드로 실행.

    Args:
        argv: 선택적으로 주입한 명령행 인수. 생략 시 ``sys.argv`` 사용.
        environment: 선택적으로 주입한 환경 변수. 생략 시 현재 환경 사용.

    Returns:
        선택한 단계의 안정된 워크플로 종료 코드.
    """

    started_at = time.monotonic()
    try:
        args = _parser().parse_args(argv)
    except SystemExit as exc:
        if exc.code == 0:
            return int(ExitCode.SUCCESS)
        print(
            "REPORT_WRITE_FAILED: failure report could not be written",
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
