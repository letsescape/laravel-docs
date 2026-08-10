#!/usr/bin/env python3
"""격리된 로컬 복제본에서 운영용 번역 동기화 재현 실행."""
from __future__ import annotations

import argparse
import base64
import contextvars
import hashlib
import json
import math
import os
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from sync import upstream
from sync.common.versions import load_versions
from sync.runtime.candidate import CandidateFailure, CandidateResult, CandidateRunner
from sync.runtime.deadline import DeadlineExceeded, WorkflowDeadline
from sync.runtime.failure import (
    ErrorClassification,
    FailureEvent,
    FailureReport,
    IssueCode,
    ProviderAttempts,
    classification_for,
    exit_code_for,
    final_exit_code,
    redact_message,
    write_failure_report_exact,
)
from sync.runtime.process import ProcessTreeError, run_process_tree
from sync.runtime.settings import (
    SettingsError,
    WorkflowSettings,
    load_workflow_settings,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_ENV = "TRANSLATION_UPSTREAM_MANIFEST"
MANIFEST_DIGEST_ENV = "TRANSLATION_UPSTREAM_MANIFEST_DIGEST"
SELECTOR_ENV = "TRANSLATION_SELECTOR_JSON"
SELECTOR_DIGEST_ENV = "TRANSLATION_SELECTOR_DIGEST"
WORKFLOW_DEADLINE_ENV = "TRANSLATION_WORKFLOW_DEADLINE_MONOTONIC"
FAILURE_REPORT_ENV = "TRANSLATION_FAILURE_REPORT"
RUN_ID_ENV = "TRANSLATION_RUN_ID"

EXIT_OK = 0
EXIT_SYNC_FAILED = 1
EXIT_REPLAY_ERROR = 2
EXIT_WORKTREE_CHANGED = 3

_PASSTHROUGH_ENV = {
    "PATH",
    "LANG",
    "LC_ALL",
    "SSL_CERT_FILE",
    "SSL_CERT_DIR",
    "TMPDIR",
    "TMP",
    "TEMP",
    "SYSTEMROOT",
    "UV_CACHE_DIR",
    "TRANSLATION_UPSTREAM_MANIFEST",
}
_PROCESS_RUNNER = run_process_tree


class ReplayError(RuntimeError):
    """격리된 재현 실행의 준비 또는 실행 실패 오류."""


class ReplayInputError(ReplayError):
    """결정적 경로 또는 선택자 계약을 위반한 재현 실행 입력 오류."""


class ReplayDeadlineExceeded(ReplayError):
    """재현 실행 완료 전 공통 워크플로 기한 초과 오류."""


class ReplayManifestMismatch(ReplayInputError):
    """재현 실행 도중 고정된 정규 매니페스트 변경 오류."""


class ReplayIsolationViolation(ReplayError):
    """재현 실행 후보의 게시 경로 격리 위반 오류."""


_ACTIVE_DEADLINE: contextvars.ContextVar[WorkflowDeadline | None] = (
    contextvars.ContextVar("translation_replay_deadline", default=None)
)
_ACTIVE_SETTINGS: contextvars.ContextVar[WorkflowSettings | None] = (
    contextvars.ContextVar("translation_replay_settings", default=None)
)


@dataclass(slots=True)
class _ReplayDiagnostics:
    """재현 실행의 실패 증거와 보존된 샌드박스 정보."""

    run_id: str
    report_target: Path | None
    artifact_root: Path | None = None
    manifest_digest: str | None = None
    base_head: str | None = None
    candidate_debug_path: str | None = None
    failures: list[FailureEvent] = field(default_factory=list)

    def record(
        self,
        code: IssueCode,
        *,
        stage: str,
        message: str,
    ) -> None:
        """안정적 문제 코드와 민감 정보를 가린 진단을 실행 증거에 추가."""

        self.failures.append(
            FailureEvent(code=code, stage=stage, message=message)
        )

    def preserve_sandbox(self, sandbox: Path) -> None:
        """보존된 샌드박스를 산출물 루트 기준 상대 경로로 기록."""

        if self.artifact_root is None:
            return
        try:
            relative = sandbox.resolve().relative_to(self.artifact_root)
        except (OSError, ValueError):
            return
        relative_path = relative.as_posix()
        if relative_path and relative_path != ".":
            self.candidate_debug_path = relative_path


_ACTIVE_DIAGNOSTICS: contextvars.ContextVar[_ReplayDiagnostics | None] = (
    contextvars.ContextVar("translation_replay_diagnostics", default=None)
)


def _record_failure(
    code: IssueCode,
    *,
    stage: str,
    message: str,
) -> None:
    """현재 재현 실행 진단 문맥에 실패 이벤트 추가."""

    diagnostics = _ACTIVE_DIAGNOSTICS.get()
    if diagnostics is not None:
        diagnostics.record(code, stage=stage, message=message)


def _safe_error(error: BaseException) -> str:
    """외부 경로와 비밀값을 가린 오류 문자열 반환."""

    return redact_message(str(error))


def _deadline_timeout() -> float | None:
    """공통 워크플로 기한 안에서 현재 단계에 남은 시간 반환."""

    deadline = _ACTIVE_DEADLINE.get()
    if deadline is None:
        return None
    try:
        return deadline.phase_remaining()
    except DeadlineExceeded as exc:
        raise ReplayDeadlineExceeded("workflow deadline exceeded") from exc


def _resolve_workflow_context(
    repo_root: Path,
) -> tuple[WorkflowDeadline, WorkflowSettings]:
    """설정 파일과 선택적 외부 기한을 사용해 재현 실행 문맥 구성."""

    raw_deadline = os.environ.get(WORKFLOW_DEADLINE_ENV)
    if raw_deadline is None:
        settings = load_workflow_settings(
            repo_root / "translation-sync/workflow.json"
        )
        return (
            WorkflowDeadline.start(settings.workflow_timeout_seconds),
            settings,
        )
    try:
        expires_at = float(raw_deadline)
    except ValueError as exc:
        raise ReplayInputError("invalid workflow deadline") from exc
    if not math.isfinite(expires_at) or expires_at <= 0:
        raise ReplayInputError("invalid workflow deadline")
    deadline = WorkflowDeadline(expires_at=expires_at)
    try:
        deadline.phase_remaining()
    except DeadlineExceeded as exc:
        raise ReplayDeadlineExceeded("workflow deadline exceeded") from exc
    settings = load_workflow_settings(
        repo_root / "translation-sync/workflow.json"
    )
    return deadline, settings


def normalize_selector(
    *,
    version: str | None,
    doc: str | None,
    supported_versions: list[str],
) -> bytes:
    """버전·문서 선택자를 검증해 정규 JSON 바이트로 직렬화."""

    if version is not None and not isinstance(version, str):
        raise ReplayInputError("invalid version selector")
    if version is not None and version not in supported_versions:
        raise ReplayInputError(f"unsupported version selector: {version}")

    normalized_doc: str | None = None
    if doc is not None:
        if not isinstance(doc, str):
            raise ReplayInputError("invalid document selector")
        if version is None:
            raise ReplayInputError("document selector requires a version selector")
        normalized_doc = unicodedata.normalize("NFC", doc)
        if "\\" in normalized_doc or "\0" in normalized_doc:
            raise ReplayInputError("unsafe document selector")
        parts = normalized_doc.split("/")
        if (
            normalized_doc.startswith("/")
            or any(part in {"", ".", ".."} for part in parts)
            or not normalized_doc.endswith(".md")
        ):
            raise ReplayInputError("unsafe document selector")

    payload = {"document": normalized_doc, "version": version}
    return (
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def canonical_replay_state(manifest: bytes, selector: bytes) -> bytes:
    """매니페스트와 선택자를 재사용 가능한 정규 재현 실행 상태로 직렬화."""

    payload = {
        "schema_version": 1,
        "manifest_base64": base64.b64encode(manifest).decode("ascii"),
        "manifest_digest": upstream.manifest_digest(manifest),
        "selector_base64": base64.b64encode(selector).decode("ascii"),
        "selector_digest": hashlib.sha256(selector).hexdigest(),
    }
    return (
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def _command(
    args: list[str],
    *,
    cwd: Path,
    input_data: bytes | None = None,
) -> subprocess.CompletedProcess[bytes]:
    """남은 공통 기한 안에서 격리된 하위 프로세스 실행."""

    try:
        return _PROCESS_RUNNER(
            args,
            cwd=cwd,
            env=_git_environment(),
            input=input_data,
            capture_output=True,
            check=True,
            timeout=_deadline_timeout(),
        )
    except subprocess.TimeoutExpired as exc:
        raise ReplayDeadlineExceeded("workflow deadline exceeded") from exc
    except subprocess.CalledProcessError as exc:
        command = args[0] if args else "subprocess"
        raise ReplayError(f"command failed ({command})") from exc
    except ProcessTreeError as exc:
        raise ReplayError("command process tree failed") from exc


def _git_environment() -> dict[str, str]:
    """사용자 설정과 프롬프트를 차단한 Git 실행 환경 구성."""

    env = {
        key: value
        for key, value in os.environ.items()
        if key in _PASSTHROUGH_ENV or key.startswith("LC_")
    }
    env.update(
        {
            "HOME": os.devnull,
            "XDG_CONFIG_HOME": os.devnull,
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
        }
    )
    return env


def _git(
    repo: Path, *args: str, input_data: bytes | None = None
) -> subprocess.CompletedProcess[bytes]:
    """지정 저장소에서 격리된 환경으로 Git 명령 실행."""

    return _command(["git", *args], cwd=repo, input_data=input_data)


def _worktree_status(repo: Path) -> bytes:
    """미추적 파일을 포함한 작업 트리 상태 바이트 반환."""

    return _git(
        repo,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
    ).stdout


def _worktree_fingerprint(repo: Path) -> bytes:
    """HEAD·참조·인덱스·작업 트리·미추적 파일의 상태 지문 계산."""

    digest = hashlib.sha256()
    digest.update(b"HEAD\0")
    digest.update(_git(repo, "rev-parse", "HEAD").stdout)
    digest.update(b"REFS\0")
    digest.update(
        _git(
            repo,
            "for-each-ref",
            "--sort=refname",
            "--format=%(refname)%00%(objectname)%00",
        ).stdout
    )
    digest.update(b"TREE\0")
    digest.update(_git(repo, "rev-parse", "HEAD^{tree}").stdout)
    digest.update(_worktree_status(repo))
    digest.update(_git(repo, "diff", "--binary", "--full-index", "HEAD", "--").stdout)
    digest.update(
        _git(
            repo,
            "diff",
            "--cached",
            "--binary",
            "--full-index",
            "HEAD",
            "--",
        ).stdout
    )
    untracked = _git(
        repo, "ls-files", "--others", "--exclude-standard", "-z"
    ).stdout
    for raw_path in sorted(path for path in untracked.split(b"\0") if path):
        path = repo / Path(os.fsdecode(raw_path))
        digest.update(raw_path)
        if path.is_symlink():
            digest.update(b"L")
            digest.update(os.fsencode(os.readlink(path)))
        else:
            digest.update(b"F")
            digest.update((path.stat().st_mode & 0o7777).to_bytes(2, "big"))
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.digest()


def _copy_untracked(source: Path, sandbox: Path) -> None:
    """심볼릭 링크를 거부하며 미추적 파일을 재현 실행 샌드박스에 복사."""

    output = _git(
        source, "ls-files", "--others", "--exclude-standard", "-z"
    ).stdout
    for raw_path in output.split(b"\0"):
        if not raw_path:
            continue
        relative = Path(os.fsdecode(raw_path))
        src = source / relative
        dest = sandbox / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.is_symlink():
            raise ReplayInputError(
                f"untracked symlink is not replay-safe: {relative}"
            )
        shutil.copy2(src, dest)


def _reject_changed_tracked_symlinks(source: Path) -> None:
    """작업 트리에서 변경된 추적 대상 심볼릭 링크 거부."""

    output = _git(source, "diff", "--name-only", "-z", "HEAD", "--").stdout
    for raw_path in output.split(b"\0"):
        if not raw_path:
            continue
        relative = Path(os.fsdecode(raw_path))
        if (source / relative).is_symlink():
            raise ReplayInputError(
                f"tracked symlink is not replay-safe: {relative}"
            )


def _reject_external_tracked_symlinks(source: Path) -> None:
    """저장소 밖을 가리키는 추적 대상 심볼릭 링크 거부."""

    root = source.resolve()
    output = _git(source, "ls-files", "-z").stdout
    for raw_path in output.split(b"\0"):
        if not raw_path:
            continue
        relative = Path(os.fsdecode(raw_path))
        link = source / relative
        if not link.is_symlink():
            continue
        target = Path(os.readlink(link))
        lexical_target = Path(os.path.abspath(link.parent / target))
        try:
            resolved_target = link.resolve(strict=False)
        except (OSError, RuntimeError) as exc:
            raise ReplayInputError(
                f"could not resolve tracked symlink: {relative}"
            ) from exc
        if (
            target.is_absolute()
            or not lexical_target.is_relative_to(root)
            or not resolved_target.is_relative_to(root)
        ):
            raise ReplayInputError(
                f"tracked symlink escapes repository: {relative}"
            )


def _sandbox_parent(source: Path, requested: Path | None) -> Path:
    """활성 저장소 밖의 재현 실행 샌드박스 상위 경로 확정."""

    temp_parent = Path(tempfile.gettempdir()).resolve()
    if temp_parent == source or temp_parent.is_relative_to(source):
        raise ReplayInputError("temporary directory is inside active repository")
    parent = requested.resolve() if requested is not None else temp_parent
    if parent == source or parent.is_relative_to(source):
        raise ReplayInputError("sandbox parent is inside active repository")
    return parent


def _path_is_within_directory(path: Path, root: Path) -> bool:
    """존재하는 가장 가까운 조상을 기준으로 경로가 디렉터리 내부인지 판정."""

    current = path
    while True:
        try:
            if current.samefile(root):
                return True
        except FileNotFoundError:
            pass
        parent = current.parent
        if parent == current:
            return False
        current = parent


def _manifest_destination(repo_root: Path) -> Path | None:
    """환경 변수로 지정한 외부 매니페스트 입출력 경로 검증."""

    value = os.environ.get(MANIFEST_ENV, "").strip()
    if not value:
        return None
    lexical_destination = Path(os.path.abspath(value))
    if lexical_destination.is_symlink():
        raise ReplayInputError("upstream manifest target must not be a symlink")
    if lexical_destination.exists() and not lexical_destination.is_file():
        raise ReplayInputError("upstream manifest target must be a regular file")
    destination = (
        lexical_destination.parent.resolve(strict=False)
        / lexical_destination.name
    )
    if (
        lexical_destination == repo_root
        or lexical_destination.is_relative_to(repo_root)
        or destination == repo_root
        or destination.is_relative_to(repo_root)
        or _path_is_within_directory(destination, repo_root)
    ):
        raise ReplayInputError(
            "upstream manifest destination is inside active repository"
        )
    return destination


def _state_output_destination(
    repo_root: Path,
    requested: Path | None,
) -> Path | None:
    """새 재현 실행 상태를 기록할 저장소 외부 경로 검증."""

    if requested is None:
        return None
    lexical_destination = Path(os.path.abspath(requested))
    if lexical_destination.is_symlink():
        raise ReplayInputError("replay state target must not be a symlink")
    if lexical_destination.exists():
        raise ReplayInputError("replay state destination already exists")
    destination = (
        lexical_destination.parent.resolve(strict=False)
        / lexical_destination.name
    )
    if (
        lexical_destination == repo_root
        or lexical_destination.is_relative_to(repo_root)
        or destination == repo_root
        or destination.is_relative_to(repo_root)
        or _path_is_within_directory(destination, repo_root)
    ):
        raise ReplayInputError(
            "replay state destination is inside active repository"
        )
    return destination


def _failure_report_destination(repo_root: Path) -> Path | None:
    """실패 보고서를 기록할 저장소 외부 경로 검증."""

    value = os.environ.get(FAILURE_REPORT_ENV, "").strip()
    if not value:
        return None
    lexical_destination = Path(os.path.abspath(value))
    if lexical_destination.is_symlink():
        raise ReplayInputError("failure report target must not be a symlink")
    if lexical_destination.exists() and not lexical_destination.is_file():
        raise ReplayInputError("failure report target must be a regular file")
    destination = (
        lexical_destination.parent.resolve(strict=False)
        / lexical_destination.name
    )
    if (
        lexical_destination == repo_root
        or lexical_destination.is_relative_to(repo_root)
        or destination == repo_root
        or destination.is_relative_to(repo_root)
        or _path_is_within_directory(destination, repo_root)
    ):
        raise ReplayInputError(
            "failure report destination is inside active repository"
        )
    return destination


def _new_run_id() -> str:
    """충돌하기 어려운 재현 실행 식별자 생성."""

    return f"replay-{secrets.token_hex(16)}"


def _run_id_from_environment() -> tuple[str, bool]:
    """외부 실행 식별자를 검증하고, 없거나 유효하지 않으면 새 식별자로 대체."""

    value = os.environ.get(RUN_ID_ENV, "")
    if not value:
        return _new_run_id(), True
    valid = (
        len(value) <= 128
        and value[0].isalnum()
        and all(
            character.isalnum() or character in "._-"
            for character in value
        )
    )
    return (value, True) if valid else (_new_run_id(), False)


def _coherent_failure_result(
    result: int,
    diagnostics: _ReplayDiagnostics,
) -> int:
    """실제 종료 코드와 실패 증거의 최종 종료 코드 일치 조정."""

    reported_result = int(final_exit_code(diagnostics.failures))
    if reported_result == result:
        return result
    if result == EXIT_WORKTREE_CHANGED:
        diagnostics.record(
            IssueCode.ACTIVE_WORKTREE_MUTATED,
            stage="active-worktree",
            message="active repository fingerprint changed",
        )
    elif result == EXIT_REPLAY_ERROR:
        diagnostics.record(
            IssueCode.RUNNER_OPERATION_FAILED,
            stage="replay",
            message="replay failed without stable infrastructure evidence",
        )
    elif result == EXIT_SYNC_FAILED:
        diagnostics.record(
            IssueCode.RUNNER_OPERATION_FAILED,
            stage="replay",
            message="replay child failed without stable controlled-failure evidence",
        )
    return int(final_exit_code(diagnostics.failures))


def _write_replay_failure_report(
    result: int,
    diagnostics: _ReplayDiagnostics,
) -> int:
    """재현 실행 실패 증거를 기존 파일을 덮어쓰지 않는 정규 보고서로 기록."""

    if result == EXIT_OK:
        return result
    result = _coherent_failure_result(result, diagnostics)
    if diagnostics.report_target is None:
        return result
    try:
        report = FailureReport.build(
            run_id=diagnostics.run_id,
            failures=diagnostics.failures,
            manifest_digest=diagnostics.manifest_digest,
            base_head=diagnostics.base_head,
            candidate_debug_path=diagnostics.candidate_debug_path,
        )
    except (TypeError, ValueError):
        print(
            "REPORT_WRITE_FAILED: failure report could not be written",
            file=sys.stderr,
        )
        return result
    write_failure_report_exact(report, target=diagnostics.report_target)
    return result


def _snapshot_manifest(
    path: Path,
    *,
    repo_root: Path | None = None,
) -> bytes | None:
    """심볼릭 링크를 따르지 않고 매니페스트의 단일 시점 바이트 읽기."""

    flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    if hasattr(os, "O_NONBLOCK"):
        flags |= os.O_NONBLOCK

    try:
        parent_descriptor, _ = _open_manifest_parent(
            path,
            create=False,
            repo_root=repo_root,
        )
    except FileNotFoundError:
        return None
    descriptor = -1
    try:
        try:
            descriptor = os.open(
                path.name,
                flags,
                dir_fd=parent_descriptor,
            )
        except FileNotFoundError:
            return None
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ReplayInputError(
                "upstream manifest target must be a regular file"
            )
        with os.fdopen(descriptor, "rb", closefd=False) as input_stream:
            return input_stream.read()
    finally:
        try:
            if descriptor >= 0:
                os.close(descriptor)
        finally:
            os.close(parent_descriptor)


def _create_sandbox(source: Path, sandbox_parent: Path | None) -> Path:
    """원격 저장소와 객체 대체 경로가 없는 독립 재현 실행 복제본 생성."""

    _reject_external_tracked_symlinks(source)
    if sandbox_parent is not None:
        sandbox_parent.mkdir(parents=True, exist_ok=True)
    sandbox = Path(
        tempfile.mkdtemp(prefix="translation-replay-", dir=sandbox_parent)
    )
    try:
        head = _git(source, "rev-parse", "HEAD").stdout.strip().decode("ascii")
        try:
            _command(
                [
                    "git",
                    "clone",
                    "--local",
                    "--no-hardlinks",
                    "--quiet",
                    "--no-checkout",
                    str(source),
                    str(sandbox),
                ],
                cwd=source,
            )
        except ReplayError as exc:
            raise ReplayError("sandbox clone failed") from exc
        _git(sandbox, "checkout", "--detach", "--quiet", head)
        _git(sandbox, "remote", "remove", "origin")
        if _git(sandbox, "remote").stdout.strip():
            raise ReplayError("sandbox remote isolation failed")
        if _git(
            sandbox,
            "for-each-ref",
            "--format=%(refname)",
            "refs/remotes/",
        ).stdout.strip():
            raise ReplayError("sandbox remote refs remain")
        alternates = sandbox / ".git" / "objects" / "info" / "alternates"
        if alternates.exists():
            if alternates.read_bytes():
                raise ReplayError("sandbox object alternates are forbidden")
            alternates.unlink()
    except BaseException:
        shutil.rmtree(sandbox, ignore_errors=True)
        raise
    return sandbox


def _overlay_worktree(source: Path, sandbox: Path) -> None:
    """활성 작업 트리의 변경과 미추적 파일을 샌드박스에 투영."""

    _reject_external_tracked_symlinks(source)
    _reject_changed_tracked_symlinks(source)
    patch = _git(source, "diff", "--binary", "--full-index", "HEAD", "--").stdout
    if patch:
        _git(
            sandbox,
            "apply",
            "--binary",
            "--whitespace=nowarn",
            "-",
            input_data=patch,
        )
    _copy_untracked(source, sandbox)


def _commit_snapshot(sandbox: Path, message: str) -> str:
    """샌드박스의 현재 상태를 로컬 재현 실행 커밋으로 기록."""

    _git(sandbox, "add", "-A")
    _git(
        sandbox,
        "-c",
        "user.name=translation-replay",
        "-c",
        "user.email=translation-replay@localhost",
        "-c",
        "commit.gpgsign=false",
        "commit",
        "--allow-empty",
        "--no-verify",
        "--quiet",
        "-m",
        message,
    )
    return _git(sandbox, "rev-parse", "HEAD").stdout.strip().decode("ascii")


def _commit_baseline(sandbox: Path) -> str:
    """첫 후보 실행의 승인 기준 커밋 생성."""

    return _commit_snapshot(sandbox, "chore: local translation replay baseline")


def _sandbox_manifest_path(sandbox: Path) -> Path:
    """샌드박스 Git 영역의 고정 매니페스트 경로 반환."""

    return sandbox / ".git" / "translation-upstream-refs.json"


def _directory_open_flags() -> int:
    """심볼릭 링크 방지에 필요한 디렉터리 열기 플래그 구성."""

    required_dir_fd_operations = (
        os.open,
        os.mkdir,
        os.stat,
        os.unlink,
        os.link,
    )
    if (
        not hasattr(os, "O_DIRECTORY")
        or not hasattr(os, "O_NOFOLLOW")
        or any(
            operation not in os.supports_dir_fd
            for operation in required_dir_fd_operations
        )
    ):
        raise ReplayError("secure upstream manifest paths are not supported")
    flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    flags |= os.O_DIRECTORY | os.O_NOFOLLOW
    return flags


def _directory_fd_is_within(
    descriptor: int,
    root_status: os.stat_result,
) -> bool:
    """열린 디렉터리가 기준 디렉터리 내부인지 inode로 판정."""

    current = os.dup(descriptor)
    try:
        while True:
            current_status = os.fstat(current)
            if os.path.samestat(current_status, root_status):
                return True
            parent = os.open("..", _directory_open_flags(), dir_fd=current)
            parent_status = os.fstat(parent)
            if os.path.samestat(current_status, parent_status):
                os.close(parent)
                return False
            previous = current
            current = parent
            os.close(previous)
    finally:
        os.close(current)


def _open_manifest_parent(
    destination: Path,
    *,
    create: bool,
    repo_root: Path | None,
) -> tuple[int, Path]:
    """각 경로 요소의 심볼릭 링크를 거부하며 매니페스트 상위 디렉터리 열기."""

    parent_path = destination.parent.resolve(strict=False)
    parts = parent_path.parts
    if not parent_path.is_absolute() or not parts:
        raise ReplayInputError(
            "upstream manifest destination must be absolute"
        )

    root_status = repo_root.stat() if repo_root is not None else None
    descriptor = os.open(parts[0], _directory_open_flags())
    try:
        for component in parts[1:]:
            if (
                root_status is not None
                and _directory_fd_is_within(descriptor, root_status)
            ):
                raise ReplayInputError(
                    "upstream manifest destination is inside active repository"
                )
            try:
                child = os.open(
                    component,
                    _directory_open_flags(),
                    dir_fd=descriptor,
                )
            except FileNotFoundError:
                if not create:
                    raise
                try:
                    os.mkdir(component, mode=0o777, dir_fd=descriptor)
                except FileExistsError:
                    pass
                child = os.open(
                    component,
                    _directory_open_flags(),
                    dir_fd=descriptor,
                )
            previous = descriptor
            descriptor = child
            os.close(previous)

        if (
            root_status is not None
            and _directory_fd_is_within(descriptor, root_status)
        ):
            raise ReplayInputError(
                "upstream manifest destination is inside active repository"
            )
        return descriptor, parent_path
    except BaseException:
        os.close(descriptor)
        raise


def _manifest_parent_is_stable(
    descriptor: int,
    path: Path,
    *,
    repo_root: Path | None,
) -> bool:
    """열린 매니페스트 상위 디렉터리의 경로와 inode 안정성 확인."""

    if repo_root is not None and _directory_fd_is_within(
        descriptor,
        repo_root.stat(),
    ):
        return False
    try:
        path_status = path.stat()
    except OSError:
        return False
    return os.path.samestat(os.fstat(descriptor), path_status)


def _unlink_temp_manifest(
    parent_descriptor: int,
    name: str,
    expected_status: os.stat_result,
) -> None:
    """inode가 같은 미완성 매니페스트 임시 파일만 삭제."""

    try:
        current_status = os.stat(
            name,
            dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
    except OSError:
        return
    if not os.path.samestat(current_status, expected_status):
        return
    try:
        os.unlink(name, dir_fd=parent_descriptor)
    except OSError:
        pass


def _export_manifest(
    source: Path | bytes,
    destination: Path,
    *,
    repo_root: Path | None = None,
) -> None:
    """매니페스트 바이트를 교체 경쟁에 안전한 비덮어쓰기 방식으로 내보내기."""

    if isinstance(source, Path):
        contents = _snapshot_manifest(source)
        if contents is None:
            raise ReplayError(
                f"sandbox did not produce an upstream manifest: {source}"
            )
    else:
        contents = source

    destination = destination.parent.resolve(strict=False) / destination.name
    temp_name = f".translation-replay-{secrets.token_hex(16)}.tmp"
    parent_descriptor, parent_path = _open_manifest_parent(
        destination,
        create=True,
        repo_root=repo_root,
    )
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW

    temp_descriptor: int | None = None
    temp_status: os.stat_result | None = None
    try:
        temp_descriptor = os.open(
            temp_name,
            flags,
            0o600,
            dir_fd=parent_descriptor,
        )
        temp_status = os.fstat(temp_descriptor)
        remaining = memoryview(contents)
        while remaining:
            written = os.write(temp_descriptor, remaining)
            if written == 0:
                raise OSError("could not write upstream manifest")
            remaining = remaining[written:]
        os.fsync(temp_descriptor)

        if not _manifest_parent_is_stable(
            parent_descriptor,
            parent_path,
            repo_root=repo_root,
        ):
            raise ReplayInputError(
                "upstream manifest parent changed during replay"
            )
        try:
            os.link(
                temp_name,
                destination.name,
                src_dir_fd=parent_descriptor,
                dst_dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except FileExistsError as exc:
            raise ReplayInputError(
                "upstream manifest destination already exists"
            ) from exc
    finally:
        try:
            if temp_status is None and temp_descriptor is not None:
                try:
                    temp_status = os.fstat(temp_descriptor)
                except OSError:
                    pass
            if temp_status is not None:
                _unlink_temp_manifest(
                    parent_descriptor,
                    temp_name,
                    temp_status,
                )
        finally:
            try:
                if temp_descriptor is not None:
                    os.close(temp_descriptor)
            finally:
                os.close(parent_descriptor)


def _candidate_sync_environment(
    *,
    manifest_digest: str,
    selector: bytes,
) -> dict[str, str]:
    """후보 실행 두 회차가 공유할 동일성 확인용 실행 환경 구성."""

    deadline = _ACTIVE_DEADLINE.get()
    if deadline is None:
        raise ReplayError("workflow deadline is unavailable")
    return {
        "TRANSLATION_PROVIDER": "identity",
        "TRANSLATION_REPLAY": "1",
        MANIFEST_DIGEST_ENV: manifest_digest,
        SELECTOR_ENV: selector.decode("utf-8"),
        SELECTOR_DIGEST_ENV: hashlib.sha256(selector).hexdigest(),
        WORKFLOW_DEADLINE_ENV: repr(deadline.expires_at),
    }


def _read_child_failure(
    path: Path,
    *,
    expected_returncode: int,
    run_id: str,
) -> FailureEvent | None:
    """하위 후보의 정규 실패 보고서를 검증해 이벤트로 복원."""

    try:
        if path.is_symlink() or not path.is_file():
            raise ValueError("missing child failure report")
        raw = path.read_bytes()
        if len(raw) > 1_000_000:
            raise ValueError("child failure report is too large")
        value = json.loads(raw.decode("utf-8"))
        if not isinstance(value, dict):
            raise ValueError("invalid child failure report")
        canonical = (
            json.dumps(
                value,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
        if raw != canonical:
            raise ValueError("noncanonical child failure report")
        required = {
            "schema_version",
            "run_id",
            "stage",
            "classification",
            "code",
            "exit_code",
            "version",
            "locale",
            "document",
            "plan_id",
            "structural_address",
            "attempts",
            "issues",
        }
        if (
            not required.issubset(value)
            or value["schema_version"] != 1
            or value["run_id"] != run_id
            or isinstance(value["exit_code"], bool)
            or value["exit_code"] != expected_returncode
            or not isinstance(value["stage"], str)
            or not value["stage"]
            or not isinstance(value["issues"], list)
            or not value["issues"]
        ):
            raise ValueError("invalid child failure report contract")
        code = IssueCode(value["code"])
        if (
            value["classification"] != classification_for(code).value
            or int(exit_code_for(code)) != expected_returncode
        ):
            raise ValueError("child failure code mismatch")

        attempts_value = value["attempts"]
        attempts: ProviderAttempts | None = None
        if classification_for(code) is ErrorClassification.TRANSLATION:
            if not isinstance(attempts_value, dict) or set(attempts_value) != {
                "response_evaluation",
                "transport",
            }:
                raise ValueError("invalid child provider attempts")
            attempts = ProviderAttempts(
                response_evaluation=attempts_value["response_evaluation"],
                transport=attempts_value["transport"],
            )
        elif attempts_value is not None:
            raise ValueError("unexpected child provider attempts")

        primary_issue: dict[str, object] | None = None
        issue_exit = 0
        for issue in value["issues"]:
            if (
                not isinstance(issue, dict)
                or set(issue) != {"code", "structural_address", "message"}
                or not isinstance(issue["message"], str)
            ):
                raise ValueError("invalid child failure issue")
            issue_code = IssueCode(issue["code"])
            issue_exit = max(issue_exit, int(exit_code_for(issue_code)))
            if (
                primary_issue is None
                and issue_code is code
                and issue["structural_address"]
                == value["structural_address"]
            ):
                primary_issue = issue
        if issue_exit != expected_returncode or primary_issue is None:
            raise ValueError("child failure issue mismatch")

        event = FailureEvent(
            code=code,
            stage=value["stage"],
            message=primary_issue["message"],
            version=value["version"],
            locale=value["locale"],
            document=value["document"],
            plan_id=value["plan_id"],
            structural_address=value["structural_address"],
            attempts=attempts,
        )
        FailureReport.build(run_id=run_id, failures=[event])
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        TypeError,
        ValueError,
    ):
        return None
    return event


def _candidate_failure_result(failure: CandidateFailure) -> int:
    """후보 실패 증거를 재현 실행 진단과 종료 코드로 변환."""

    diagnostics = _ACTIVE_DIAGNOSTICS.get()
    if diagnostics is None:
        raise ReplayError("replay diagnostics are unavailable")
    if failure.issue_code is not None:
        diagnostics.record(
            failure.issue_code,
            stage=failure.stage,
            message="candidate replay stage failed",
        )
        return int(exit_code_for(failure.issue_code))
    if failure.report_path is not None and isinstance(failure.returncode, int):
        event = _read_child_failure(
            failure.report_path,
            expected_returncode=failure.returncode,
            run_id=diagnostics.run_id,
        )
        if event is not None:
            diagnostics.failures.append(event)
            return int(event.exit_code)
    diagnostics.record(
        IssueCode.RUNNER_OPERATION_FAILED,
        stage=failure.stage,
        message="candidate child failed without valid stable failure evidence",
    )
    return EXIT_REPLAY_ERROR


def _candidate_remaining_seconds() -> float:
    """후보 실행에 남은 공통 워크플로 시간 계산."""

    deadline = _ACTIVE_DEADLINE.get()
    if deadline is None:
        raise ReplayError("workflow deadline is unavailable")
    return deadline.expires_at - time.monotonic()


def _verify_candidate_isolation(result: CandidateResult) -> None:
    """후보 Git 상태가 봉인된 트리와 격리 조건을 유지하는지 검증."""

    if (
        result.sandbox is None
        or result.base_commit is None
        or result.verified_tree is None
    ):
        raise ReplayError("candidate result is incomplete")
    sandbox = result.sandbox
    head = _git(sandbox, "rev-parse", "HEAD").stdout.strip().decode("ascii")
    index_tree = _git(sandbox, "write-tree").stdout.strip().decode("ascii")
    if head != result.base_commit or index_tree != result.verified_tree:
        raise ReplayIsolationViolation("candidate Git state escaped its sealed tree")
    if _git(sandbox, "remote").stdout.strip():
        raise ReplayIsolationViolation("candidate retained a Git remote")
    if _git(
        sandbox,
        "for-each-ref",
        "--format=%(refname)",
        "refs/remotes/",
    ).stdout.strip():
        raise ReplayIsolationViolation("candidate retained a remote-tracking ref")
    alternates = sandbox / ".git" / "objects" / "info" / "alternates"
    if alternates.exists() and alternates.read_bytes():
        raise ReplayIsolationViolation("candidate uses object alternates")


def _commit_verified_candidate(
    sandbox: Path,
    *,
    verified_tree: str,
    parent_commit: str,
) -> str:
    """첫 회차의 봉인된 트리를 샌드박스 내부 기준 커밋으로 연결."""

    current_tree = _git(sandbox, "write-tree").stdout.strip().decode("ascii")
    current_head = _git(sandbox, "rev-parse", "HEAD").stdout.strip().decode("ascii")
    if current_tree != verified_tree or current_head != parent_commit:
        raise ReplayError("first replay candidate no longer matches its sealed tree")
    commit = (
        _git(
            sandbox,
            "-c",
            "user.name=translation-replay",
            "-c",
            "user.email=translation-replay@localhost",
            "-c",
            "commit.gpgsign=false",
            "commit-tree",
            verified_tree,
            "-p",
            parent_commit,
            input_data=b"chore: translation replay first verified tree\n",
        )
        .stdout.strip()
        .decode("ascii")
    )
    _git(sandbox, "reset", "--hard", "--quiet", commit)
    committed_tree = (
        _git(sandbox, "rev-parse", f"{commit}^{{tree}}")
        .stdout.strip()
        .decode("ascii")
    )
    if committed_tree != verified_tree:
        raise ReplayError("first replay commit tree differs from verified tree")
    return commit


def _remove_candidate_sandboxes(
    sandboxes: list[Path],
    artifact_roots: list[Path],
) -> int:
    """성공한 후보 샌드박스와 빈 산출물 디렉터리 제거."""

    diagnostics = _ACTIVE_DIAGNOSTICS.get()
    if diagnostics is None:
        raise ReplayError("replay diagnostics are unavailable")
    for sandbox in reversed(sandboxes):
        try:
            _deadline_timeout()
            shutil.rmtree(sandbox)
        except ReplayDeadlineExceeded as exc:
            diagnostics.preserve_sandbox(sandbox)
            diagnostics.record(
                IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
                stage="replay-cleanup",
                message=str(exc),
            )
            return EXIT_REPLAY_ERROR
        except OSError:
            diagnostics.preserve_sandbox(sandbox)
            diagnostics.record(
                IssueCode.SANDBOX_OPERATION_FAILED,
                stage="replay-cleanup",
                message="candidate sandbox could not be removed",
            )
            return EXIT_REPLAY_ERROR
    for artifact_root in reversed(artifact_roots):
        try:
            artifact_root.rmdir()
        except OSError:
            diagnostics.preserve_sandbox(artifact_root)
            diagnostics.record(
                IssueCode.SANDBOX_OPERATION_FAILED,
                stage="replay-cleanup",
                message="candidate artifact directory could not be removed",
            )
            return EXIT_REPLAY_ERROR
    diagnostics.candidate_debug_path = None
    return EXIT_OK


def _candidate_result_code(result: CandidateResult) -> int:
    """후보 결과를 재현 실행 종료 코드와 보존 정보에 반영."""

    diagnostics = _ACTIVE_DIAGNOSTICS.get()
    if diagnostics is None:
        raise ReplayError("replay diagnostics are unavailable")
    if result.sandbox is not None:
        diagnostics.preserve_sandbox(result.sandbox)
    if result.failure is not None:
        return _candidate_failure_result(result.failure)
    if not result.publication_allowed:
        diagnostics.record(
            IssueCode.RUNNER_OPERATION_FAILED,
            stage="replay-candidate",
            message="candidate runner returned an incomplete success result",
        )
        return EXIT_REPLAY_ERROR
    return EXIT_OK


def _verify_sandbox_manifest(sandbox: Path, expected_digest: str) -> bytes:
    """샌드박스 매니페스트가 고정 다이제스트를 유지하는지 검증."""

    try:
        contents = _snapshot_manifest(_sandbox_manifest_path(sandbox))
    except (OSError, ReplayError) as exc:
        raise ReplayManifestMismatch(
            "canonical manifest changed during replay"
        ) from exc
    if contents is None or not secrets.compare_digest(
        upstream.manifest_digest(contents),
        expected_digest,
    ):
        raise ReplayManifestMismatch("canonical manifest changed during replay")
    return contents


def _execute_sync(
    sandbox: Path,
    *,
    version: str | None,
    doc: str | None,
    manifest_digest: str,
    selector: bytes,
) -> int:
    """같은 입력으로 후보 파이프라인을 두 번 실행해 수렴성 검증."""

    settings = _ACTIVE_SETTINGS.get()
    diagnostics = _ACTIVE_DIAGNOSTICS.get()
    if settings is None or diagnostics is None:
        raise ReplayError("replay workflow context is unavailable")
    if len(settings.site_validation_commands) != 4:
        diagnostics.record(
            IssueCode.REQUIRED_CONFIG_MISSING,
            stage="replay-configuration",
            message="replay requires exactly four site validators",
        )
        return EXIT_SYNC_FAILED

    sync_core_argv = list(settings.sync_core_command)
    if version:
        sync_core_argv.extend(["--version", version])
    if doc:
        sync_core_argv.extend(["--doc", doc])
    sync_environment = _candidate_sync_environment(
        manifest_digest=manifest_digest,
        selector=selector,
    )
    artifact_root = sandbox.parent.resolve()
    pass_artifact_roots = [
        artifact_root / "replay-pass-1",
        artifact_root / "replay-pass-2",
    ]
    baseline_commit = _git(sandbox, "rev-parse", "HEAD").stdout.strip().decode("ascii")
    candidates: list[Path] = []

    manifest_bytes = _verify_sandbox_manifest(sandbox, manifest_digest)
    first = CandidateRunner(
        source_repo=sandbox,
        artifact_root=pass_artifact_roots[0],
        run_id=diagnostics.run_id,
        remaining_seconds=_candidate_remaining_seconds,
        sync_environment=sync_environment,
        sync_file_inputs={MANIFEST_ENV: manifest_bytes},
    ).run(
        base_commit=baseline_commit,
        setup_argvs=settings.candidate_setup_commands,
        sync_core_argv=tuple(sync_core_argv),
        site_validator_argvs=settings.site_validation_commands,
        path_validator_argv=settings.path_validation_command,
    )
    if first.sandbox is not None:
        candidates.append(first.sandbox)
    first_result = _candidate_result_code(first)
    _verify_sandbox_manifest(sandbox, manifest_digest)
    if first_result:
        return first_result
    _verify_candidate_isolation(first)
    assert first.sandbox is not None
    assert first.base_commit is not None
    assert first.verified_tree is not None
    first_commit = _commit_verified_candidate(
        first.sandbox,
        verified_tree=first.verified_tree,
        parent_commit=first.base_commit,
    )

    _verify_sandbox_manifest(sandbox, manifest_digest)
    second = CandidateRunner(
        source_repo=first.sandbox,
        artifact_root=pass_artifact_roots[1],
        run_id=diagnostics.run_id,
        remaining_seconds=_candidate_remaining_seconds,
        sync_environment=sync_environment,
        sync_file_inputs={MANIFEST_ENV: manifest_bytes},
    ).run(
        base_commit=first_commit,
        setup_argvs=settings.candidate_setup_commands,
        sync_core_argv=tuple(sync_core_argv),
        site_validator_argvs=settings.site_validation_commands,
        path_validator_argv=settings.path_validation_command,
    )
    if second.sandbox is not None:
        candidates.append(second.sandbox)
    second_result = _candidate_result_code(second)
    _verify_sandbox_manifest(sandbox, manifest_digest)
    if second_result:
        return second_result
    _verify_candidate_isolation(second)
    assert second.verified_tree is not None
    if second.has_changes or second.verified_tree != first.verified_tree:
        _record_failure(
            IssueCode.REPLAY_NON_CONVERGENT,
            stage="replay-convergence",
            message="second full candidate replay changed the first verified tree",
        )
        print(
            "[translation-replay] second candidate changed the first verified tree",
            file=sys.stderr,
        )
        return EXIT_SYNC_FAILED
    return _remove_candidate_sandboxes(candidates, pass_artifact_roots)


def _display_status(status: bytes) -> str:
    """NUL로 구분된 Git 상태 바이트를 진단용 여러 줄 문자열로 변환."""

    lines = [
        os.fsdecode(item)
        for item in status.split(b"\0")
        if item
    ]
    return "\n".join(lines) if lines else "(clean)"


def _run_replay_core(
    *,
    repo_root: Path = REPO_ROOT,
    version: str | None = None,
    doc: str | None = None,
    sandbox_parent: Path | None = None,
    artifact_root: Path | None = None,
    state_output: Path | None = None,
) -> int:
    """매니페스트 준비부터 격리 재현 실행·정리·상태 내보내기까지 수행."""

    repo_root = repo_root.resolve()
    deadline = _ACTIVE_DEADLINE.get()
    if deadline is None:
        raise ReplayError("workflow deadline is unavailable")
    diagnostics = _ACTIVE_DIAGNOSTICS.get()
    if diagnostics is None:
        raise ReplayError("replay diagnostics are unavailable")
    sandbox: Path | None = None
    manifest_destination: Path | None = None
    manifest_input: bytes | None = None
    manifest_was_missing = False
    state_destination: Path | None = None
    state_contents: bytes | None = None

    setup_code = IssueCode.INVALID_MANIFEST
    try:
        supported_versions = load_versions(repo_root / "versions.json")
        setup_code = IssueCode.INVALID_SELECTOR
        selector = normalize_selector(
            version=version,
            doc=doc,
            supported_versions=supported_versions,
        )
        selector_payload = json.loads(selector)
        version = selector_payload["version"]
        doc = selector_payload["document"]
        setup_code = IssueCode.REPLAY_PATH_UNSAFE
        state_destination = _state_output_destination(repo_root, state_output)
        setup_code = IssueCode.MANIFEST_EXPORT_CONFLICT
        manifest_destination = _manifest_destination(repo_root)
        if (
            state_destination is not None
            and manifest_destination == state_destination
        ):
            raise ReplayInputError(
                "manifest and replay state destinations must differ"
            )
        if (
            diagnostics.report_target is not None
            and diagnostics.report_target
            in {manifest_destination, state_destination}
        ):
            setup_code = IssueCode.REPLAY_PATH_UNSAFE
            raise ReplayInputError(
                "failure report and replay output destinations must differ"
            )
        setup_code = IssueCode.REPLAY_PATH_UNSAFE
        if artifact_root is not None:
            resolved_artifact_root = _sandbox_parent(repo_root, artifact_root)
            if (
                sandbox_parent is not None
                and sandbox_parent.resolve() != resolved_artifact_root
            ):
                raise ReplayInputError(
                    "artifact root and sandbox parent must identify the same path"
                )
            sandbox_parent = resolved_artifact_root
            diagnostics.artifact_root = resolved_artifact_root
            if (
                diagnostics.report_target is not None
                and not diagnostics.report_target.is_relative_to(
                    resolved_artifact_root
                )
            ):
                diagnostics.report_target = None
                print(
                    "REPORT_WRITE_FAILED: failure report could not be written",
                    file=sys.stderr,
                )
                raise ReplayInputError(
                    "failure report target is outside the artifact root"
                )
        elif diagnostics.report_target is not None:
            diagnostics.artifact_root = diagnostics.report_target.parent

        setup_code = IssueCode.INVALID_MANIFEST
        manifest_input = (
            _snapshot_manifest(
                manifest_destination,
                repo_root=repo_root,
            )
            if manifest_destination is not None
            else None
        )
        manifest_was_missing = manifest_input is None
        if manifest_input is None:
            manifest_input = upstream.resolve_manifest(
                supported_versions,
                deadline=deadline.expires_at,
            )
        upstream.load_manifest_bytes(
            manifest_input,
            expected_versions=supported_versions,
        )
        manifest_input_digest = upstream.manifest_digest(manifest_input)
        diagnostics.manifest_digest = manifest_input_digest
        state_contents = canonical_replay_state(manifest_input, selector)
        setup_code = IssueCode.REPLAY_PATH_UNSAFE
        sandbox_parent = _sandbox_parent(repo_root, sandbox_parent)
        diagnostics.artifact_root = sandbox_parent
        setup_code = IssueCode.RUNNER_OPERATION_FAILED
        diagnostics.base_head = (
            _git(repo_root, "rev-parse", "HEAD")
            .stdout.strip()
            .decode("ascii")
        )
        before_status = _worktree_status(repo_root)
        before_fingerprint = _worktree_fingerprint(repo_root)
    except ReplayDeadlineExceeded as exc:
        diagnostics.record(
            IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            stage="replay-setup",
            message=str(exc),
        )
        print(
            f"[translation-replay] setup failed: {_safe_error(exc)}",
            file=sys.stderr,
        )
        return EXIT_REPLAY_ERROR
    except (ReplayInputError, ValueError) as exc:
        diagnostics.record(
            setup_code,
            stage="replay-setup",
            message=str(exc),
        )
        print(
            f"[translation-replay] setup failed: {_safe_error(exc)}",
            file=sys.stderr,
        )
        return EXIT_SYNC_FAILED
    except (
        OSError,
        ProcessTreeError,
        ReplayError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
    ):
        diagnostics.record(
            IssueCode.RUNNER_OPERATION_FAILED,
            stage="replay-setup",
            message="replay setup operation failed",
        )
        print("[translation-replay] setup operation failed", file=sys.stderr)
        return EXIT_REPLAY_ERROR

    result = EXIT_OK
    interrupted = False
    operation_code = IssueCode.SANDBOX_OPERATION_FAILED
    try:
        sandbox = _create_sandbox(repo_root, sandbox_parent)
        diagnostics.preserve_sandbox(sandbox)
        print(f"[translation-replay] sandbox={sandbox.name}", flush=True)
        _overlay_worktree(repo_root, sandbox)
        baseline = _commit_baseline(sandbox)
        sandbox_manifest = _sandbox_manifest_path(sandbox)
        sandbox_manifest.write_bytes(manifest_input)
        sandbox_manifest.chmod(0o400)
        print(f"[translation-replay] baseline: {baseline}", flush=True)
        print("[translation-replay] provider: identity", flush=True)

        operation_code = IssueCode.RUNNER_OPERATION_FAILED
        sync_result = _execute_sync(
            sandbox,
            version=version,
            doc=doc,
            manifest_digest=manifest_input_digest,
            selector=selector,
        )
        if sync_result == 0:
            final_manifest = _snapshot_manifest(sandbox_manifest)
            if final_manifest != manifest_input:
                print(
                    "[translation-replay] canonical manifest changed during replay",
                    file=sys.stderr,
                )
                diagnostics.record(
                    IssueCode.MANIFEST_DIGEST_MISMATCH,
                    stage="replay-core",
                    message="canonical manifest changed during replay",
                )
                result = EXIT_SYNC_FAILED
            else:
                result = EXIT_OK
        else:
            print(
                f"[translation-replay] translation sync exited {sync_result}",
                file=sys.stderr,
            )
            if sync_result in {
                EXIT_SYNC_FAILED,
                EXIT_REPLAY_ERROR,
                EXIT_WORKTREE_CHANGED,
            }:
                result = sync_result
            else:
                result = EXIT_SYNC_FAILED
    except KeyboardInterrupt:
        print("[translation-replay] interrupted", file=sys.stderr)
        interrupted = True
        result = EXIT_REPLAY_ERROR
    except ReplayDeadlineExceeded as exc:
        diagnostics.record(
            IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            stage="replay-core",
            message=str(exc),
        )
        print(
            f"[translation-replay] replay failed: {_safe_error(exc)}",
            file=sys.stderr,
        )
        result = max(result, EXIT_REPLAY_ERROR)
    except ReplayManifestMismatch as exc:
        diagnostics.record(
            IssueCode.MANIFEST_DIGEST_MISMATCH,
            stage="replay-core",
            message=str(exc),
        )
        print(
            f"[translation-replay] replay failed: {_safe_error(exc)}",
            file=sys.stderr,
        )
        result = max(result, EXIT_SYNC_FAILED)
    except ReplayInputError as exc:
        diagnostics.record(
            IssueCode.REPLAY_PATH_UNSAFE,
            stage="replay-core",
            message=str(exc),
        )
        print(
            f"[translation-replay] replay failed: {_safe_error(exc)}",
            file=sys.stderr,
        )
        result = max(result, EXIT_SYNC_FAILED)
    except ReplayIsolationViolation as exc:
        diagnostics.record(
            IssueCode.PUBLICATION_ISOLATION_VIOLATION,
            stage="replay-isolation",
            message=str(exc),
        )
        print(
            f"[translation-replay] replay failed: {_safe_error(exc)}",
            file=sys.stderr,
        )
        result = max(result, EXIT_REPLAY_ERROR)
    except OSError:
        diagnostics.record(
            operation_code,
            stage="replay-core",
            message="replay operation failed",
        )
        print(
            "[translation-replay] replay operation failed",
            file=sys.stderr,
        )
        result = max(result, EXIT_REPLAY_ERROR)
    except ReplayError as exc:
        diagnostics.record(
            operation_code,
            stage="replay-core",
            message=str(exc),
        )
        print(
            f"[translation-replay] replay failed: {_safe_error(exc)}",
            file=sys.stderr,
        )
        result = max(result, EXIT_REPLAY_ERROR)

    try:
        after_status = _worktree_status(repo_root)
        after_fingerprint = _worktree_fingerprint(repo_root)
    except KeyboardInterrupt:
        print(
            "[translation-replay] interrupted while verifying active worktree",
            file=sys.stderr,
        )
        interrupted = True
        result = max(result, EXIT_REPLAY_ERROR)
    except ReplayDeadlineExceeded as exc:
        diagnostics.record(
            IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            stage="active-worktree",
            message=str(exc),
        )
        print(
            "[translation-replay] could not verify active worktree status: "
            f"{_safe_error(exc)}",
            file=sys.stderr,
        )
        result = max(result, EXIT_REPLAY_ERROR)
    except (OSError, ReplayError):
        diagnostics.record(
            IssueCode.RUNNER_OPERATION_FAILED,
            stage="active-worktree",
            message="active worktree fingerprint could not be verified",
        )
        print(
            "[translation-replay] could not verify active worktree status",
            file=sys.stderr,
        )
        result = max(result, EXIT_REPLAY_ERROR)
    else:
        if after_fingerprint != before_fingerprint:
            diagnostics.record(
                IssueCode.ACTIVE_WORKTREE_MUTATED,
                stage="active-worktree",
                message="active repository fingerprint changed during replay",
            )
            print(
                "[translation-replay] active repository state changed during replay",
                file=sys.stderr,
            )
            print(
                f"[translation-replay] before:\n{_display_status(before_status)}",
                file=sys.stderr,
            )
            print(
                f"[translation-replay] after:\n{_display_status(after_status)}",
                file=sys.stderr,
            )
            result = EXIT_WORKTREE_CHANGED

    if result == EXIT_OK:
        try:
            _deadline_timeout()
        except ReplayDeadlineExceeded as exc:
            diagnostics.record(
                IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
                stage="replay-cleanup",
                message=str(exc),
            )
            print(
                f"[translation-replay] replay failed: {_safe_error(exc)}",
                file=sys.stderr,
            )
            result = EXIT_REPLAY_ERROR

    manifest_output: bytes | None = None
    if (
        result == EXIT_OK
        and sandbox is not None
        and manifest_destination is not None
        and manifest_was_missing
    ):
        manifest_output = manifest_input

    if result == EXIT_OK and sandbox is not None:
        try:
            shutil.rmtree(sandbox)
        except KeyboardInterrupt:
            print(
                "[translation-replay] interrupted while removing sandbox "
                f"{sandbox.name}",
                file=sys.stderr,
            )
            raise
        except OSError:
            diagnostics.record(
                IssueCode.SANDBOX_OPERATION_FAILED,
                stage="replay-cleanup",
                message="replay sandbox could not be removed",
            )
            print(
                "[translation-replay] could not remove sandbox "
                f"{sandbox.name}",
                file=sys.stderr,
            )
            result = EXIT_REPLAY_ERROR
        else:
            sandbox = None
            diagnostics.candidate_debug_path = None

    if result == EXIT_OK:
        try:
            _deadline_timeout()
        except ReplayDeadlineExceeded as exc:
            diagnostics.record(
                IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
                stage="manifest-export",
                message=str(exc),
            )
            print(
                f"[translation-replay] replay failed: {_safe_error(exc)}",
                file=sys.stderr,
            )
            result = EXIT_REPLAY_ERROR

    if (
        result == EXIT_OK
        and manifest_output is not None
        and manifest_destination is not None
    ):
        try:
            _export_manifest(
                manifest_output,
                manifest_destination,
                repo_root=repo_root,
            )
        except KeyboardInterrupt:
            print(
                "[translation-replay] interrupted while exporting upstream manifest",
                file=sys.stderr,
            )
            raise
        except ReplayInputError as exc:
            diagnostics.record(
                IssueCode.MANIFEST_EXPORT_CONFLICT,
                stage="manifest-export",
                message=str(exc),
            )
            print(
                "[translation-replay] could not export upstream manifest: "
                f"{_safe_error(exc)}",
                file=sys.stderr,
            )
            result = max(result, EXIT_SYNC_FAILED)
        except (OSError, ReplayError):
            diagnostics.record(
                IssueCode.RUNNER_OPERATION_FAILED,
                stage="manifest-export",
                message="upstream manifest export failed",
            )
            print(
                "[translation-replay] could not export upstream manifest",
                file=sys.stderr,
            )
            result = max(result, EXIT_REPLAY_ERROR)

    if result == EXIT_OK:
        try:
            _deadline_timeout()
        except ReplayDeadlineExceeded as exc:
            diagnostics.record(
                IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
                stage="state-export",
                message=str(exc),
            )
            print(
                f"[translation-replay] replay failed: {_safe_error(exc)}",
                file=sys.stderr,
            )
            result = EXIT_REPLAY_ERROR

    if (
        result == EXIT_OK
        and state_destination is not None
        and state_contents is not None
    ):
        try:
            _export_manifest(
                state_contents,
                state_destination,
                repo_root=repo_root,
            )
        except KeyboardInterrupt:
            print(
                "[translation-replay] interrupted while exporting replay state",
                file=sys.stderr,
            )
            raise
        except ReplayInputError as exc:
            diagnostics.record(
                IssueCode.REPLAY_PATH_UNSAFE,
                stage="state-export",
                message=str(exc),
            )
            print(
                "[translation-replay] could not export replay state: "
                f"{_safe_error(exc)}",
                file=sys.stderr,
            )
            result = max(result, EXIT_SYNC_FAILED)
        except (OSError, ReplayError):
            diagnostics.record(
                IssueCode.RUNNER_OPERATION_FAILED,
                stage="state-export",
                message="replay state export failed",
            )
            print(
                "[translation-replay] could not export replay state",
                file=sys.stderr,
            )
            result = max(result, EXIT_REPLAY_ERROR)

    if result == EXIT_OK:
        print("[translation-replay] completed; sandbox removed")
    elif diagnostics.candidate_debug_path is not None:
        print(
            "[translation-replay] failed; "
            f"sandbox={diagnostics.candidate_debug_path}",
            file=sys.stderr,
        )
    elif sandbox is not None:
        print(
            f"[translation-replay] failed; sandbox={sandbox.name}",
            file=sys.stderr,
        )

    if interrupted:
        raise KeyboardInterrupt
    return result


def run_replay(
    *,
    repo_root: Path = REPO_ROOT,
    version: str | None = None,
    doc: str | None = None,
    sandbox_parent: Path | None = None,
    artifact_root: Path | None = None,
    state_output: Path | None = None,
) -> int:
    """공통 실행 문맥과 실패 보고서를 포함한 격리 재현 실행."""

    try:
        resolved_root = repo_root.resolve()
        report_target = _failure_report_destination(resolved_root)
    except ReplayInputError as exc:
        print(
            f"[translation-replay] setup failed: {_safe_error(exc)}",
            file=sys.stderr,
        )
        print(
            "REPORT_WRITE_FAILED: failure report could not be written",
            file=sys.stderr,
        )
        return EXIT_SYNC_FAILED
    except OSError:
        print("[translation-replay] setup operation failed", file=sys.stderr)
        return EXIT_REPLAY_ERROR

    run_id, run_id_is_valid = _run_id_from_environment()
    diagnostics = _ReplayDiagnostics(
        run_id=run_id,
        report_target=report_target,
    )
    if not run_id_is_valid:
        diagnostics.record(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="replay-setup",
            message="workflow run id is invalid",
        )
        print("[translation-replay] setup failed: invalid run id", file=sys.stderr)
        return _write_replay_failure_report(EXIT_SYNC_FAILED, diagnostics)

    try:
        deadline, settings = _resolve_workflow_context(resolved_root)
    except ReplayDeadlineExceeded as exc:
        diagnostics.record(
            IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            stage="replay-setup",
            message=str(exc),
        )
        print(
            f"[translation-replay] setup failed: {_safe_error(exc)}",
            file=sys.stderr,
        )
        return _write_replay_failure_report(EXIT_REPLAY_ERROR, diagnostics)
    except (ReplayInputError, SettingsError, ValueError) as exc:
        diagnostics.record(
            IssueCode.INVALID_RUNTIME_OPTION,
            stage="replay-setup",
            message=str(exc),
        )
        print(
            f"[translation-replay] setup failed: {_safe_error(exc)}",
            file=sys.stderr,
        )
        return _write_replay_failure_report(EXIT_SYNC_FAILED, diagnostics)
    except OSError:
        diagnostics.record(
            IssueCode.RUNNER_OPERATION_FAILED,
            stage="replay-setup",
            message="workflow settings could not be read",
        )
        print("[translation-replay] setup operation failed", file=sys.stderr)
        return _write_replay_failure_report(EXIT_REPLAY_ERROR, diagnostics)

    deadline_token = _ACTIVE_DEADLINE.set(deadline)
    settings_token = _ACTIVE_SETTINGS.set(settings)
    diagnostics_token = _ACTIVE_DIAGNOSTICS.set(diagnostics)
    try:
        result = _run_replay_core(
            repo_root=resolved_root,
            version=version,
            doc=doc,
            sandbox_parent=sandbox_parent,
            artifact_root=artifact_root,
            state_output=state_output,
        )
    except KeyboardInterrupt:
        raise
    except Exception:
        diagnostics.record(
            IssueCode.UNCLASSIFIED_INTERNAL,
            stage="replay",
            message="unexpected replay exception",
        )
        print("[translation-replay] unexpected replay failure", file=sys.stderr)
        result = EXIT_REPLAY_ERROR
    finally:
        _ACTIVE_DIAGNOSTICS.reset(diagnostics_token)
        _ACTIVE_SETTINGS.reset(settings_token)
        _ACTIVE_DEADLINE.reset(deadline_token)
    return _write_replay_failure_report(result, diagnostics)


def _parse_args() -> argparse.Namespace:
    """재현 실행용 명령행 선택자와 외부 산출물 경로 파싱."""

    parser = argparse.ArgumentParser(
        description="Replay the production translation sync in an isolated clone."
    )
    parser.add_argument("--version", help="Optional version filter, for example 13.x")
    parser.add_argument("--doc", help="Optional Markdown document filter")
    parser.add_argument(
        "--state-output",
        type=Path,
        help="Write canonical replay state to a new artifact file",
    )
    parser.add_argument(
        "--artifact-root",
        type=Path,
        help="Store replay sandboxes under this external artifact directory",
    )
    return parser.parse_args()


def main() -> int:
    """격리 재현 실행의 명령줄 진입점 실행."""

    args = _parse_args()
    return run_replay(
        version=args.version,
        doc=args.doc,
        artifact_root=args.artifact_root,
        state_output=args.state_output,
    )


if __name__ == "__main__":
    raise SystemExit(main())
