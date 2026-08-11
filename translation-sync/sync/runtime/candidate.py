"""publication을 수행하지 않는 격리 번역 candidate 생성과 봉인."""

from __future__ import annotations

import hashlib
import math
import os
import stat
import subprocess
import tempfile
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from .failure import IssueCode
from .process import ProcessTreeError, run_process_tree

_PASSTHROUGH_ENV = {
    "LANG",
    "LC_ALL",
    "PATH",
    "SSL_CERT_DIR",
    "SSL_CERT_FILE",
    "SYSTEMROOT",
    "TEMP",
    "TMP",
    "TMPDIR",
    "UV_CACHE_DIR",
}
_SAFE_NODE_OPTIONS = frozenset({"--max-old-space-size=4096"})
FAILURE_REPORT_ENV = "TRANSLATION_FAILURE_REPORT"
RUN_ID_ENV = "TRANSLATION_RUN_ID"
WORKFLOW_DEADLINE_ENV = "TRANSLATION_WORKFLOW_DEADLINE_MONOTONIC"
SYNC_FAILURE_REPORT_FILENAME = "translation-sync-candidate-sync-failure.json"
PATH_FAILURE_REPORT_FILENAME = "translation-sync-candidate-path-failure.json"
_SYNC_INPUT_DIRECTORY = "translation-candidate-inputs"
_SYNC_FILE_INPUT_PATHS = {
    "TRANSLATION_UPSTREAM_MANIFEST": "translation-upstream-refs.json",
}


@dataclass(frozen=True, slots=True)
class CandidateFailure:
    """fail-closed candidate 실패 결과.

    호출된 sync core 또는 경로 validator가 ``report_path``의 더 구체적인 안정된 문제 코드를 소유할 때만 ``issue_code`` 생략.
    """

    stage: str
    issue_code: IssueCode | None
    returncode: int | None = None
    report_path: Path | None = None


@dataclass(frozen=True, slots=True)
class CandidateResult:
    """봉인된 candidate 식별자 또는 publication을 금지하는 실패."""

    sandbox: Path | None
    base_commit: str | None
    verified_tree: str | None = None
    has_changes: bool = False
    failure: CandidateFailure | None = None

    @property
    def publication_allowed(self) -> bool:
        """봉인된 tree의 publication 허용 여부."""

        return self.failure is None and self.verified_tree is not None


class _CandidateError(RuntimeError):
    """예상 가능한 candidate 생성 실패."""

    def __init__(
        self,
        *,
        stage: str,
        issue_code: IssueCode | None,
        returncode: int | None = None,
        report_path: Path | None = None,
    ) -> None:
        """실패 단계와 안정된 문제 코드 저장."""

        super().__init__(stage)
        self.failure = CandidateFailure(
            stage=stage,
            issue_code=issue_code,
            returncode=returncode,
            report_path=report_path,
        )


class _DeadlineExceeded(RuntimeError):
    """공통 워크플로 기한 초과."""


class _ProcessStartFailed(RuntimeError):
    """하위 프로세스 시작 또는 격리 보장 실패."""


class _GitFailed(RuntimeError):
    """0이 아닌 종료 코드를 반환한 Git 명령."""

    def __init__(self, returncode: int) -> None:
        """Git 종료 코드 저장."""

        super().__init__(returncode)
        self.returncode = returncode


@dataclass(slots=True)
class _CandidateRunState:
    """candidate 실행 중 실패 분류에 필요한 현재 단계와 식별자."""

    stage: str = "configuration"
    sandbox: Path | None = None
    resolved_base: str | None = None


class CandidateRunner:
    """분리된 로컬 clone에서 candidate core와 validator 실행.

    모든 명령은 argv sequence로 shell 없이 직접 실행.
    process runner의 non-detachment 계약 준수.
    ``remaining_seconds``는 공통 워크플로 기한의 잔여 시간 반환.
    ``sync_environment``는 sync core에만 노출.
    core와 경로 validator는 동일 ``run_id``와 서로 다른 failure report 경로 사용.
    setup, site validator 및 Git에는 failure report 환경 변수 미제공.
    """

    def __init__(
        self,
        *,
        source_repo: Path,
        artifact_root: Path,
        run_id: str,
        remaining_seconds: Callable[[], float],
        sync_environment: Mapping[str, str] | None = None,
        sync_file_inputs: Mapping[str, bytes] | None = None,
        process_runner: Callable[..., subprocess.CompletedProcess[bytes]] | None = None,
    ) -> None:
        """격리 candidate 실행에 필요한 고정 입력 저장."""

        self._source_repo = source_repo.resolve()
        self._artifact_root = artifact_root.resolve(strict=False)
        self._run_id = run_id
        self._remaining_seconds = remaining_seconds
        self._sync_environment = dict(sync_environment or {})
        self._sync_file_inputs = dict(sync_file_inputs or {})
        self._process_runner = (
            run_process_tree if process_runner is None else process_runner
        )
        self._sync_report_path = self._artifact_root / SYNC_FAILURE_REPORT_FILENAME
        self._path_report_path = self._artifact_root / PATH_FAILURE_REPORT_FILENAME

    def _validated_commands(
        self,
        *,
        base_commit: str,
        setup_argvs: Sequence[Sequence[str]],
        sync_core_argv: Sequence[str],
        site_validator_argvs: Sequence[Sequence[str]],
        path_validator_argv: Sequence[str],
    ) -> tuple[
        tuple[tuple[str, ...], ...],
        tuple[str, ...],
        tuple[tuple[str, ...], ...],
        tuple[str, ...],
        dict[str, bytes],
    ]:
        """candidate 명령·식별자·외부 경로 설정을 실행 전에 검증.

        Args:
            base_commit: 승인 기준 Git commit ID.
            setup_argvs: 후보 준비 명령 목록.
            sync_core_argv: 번역 동기화 core 명령.
            site_validator_argvs: 사이트 검증 명령 목록.
            path_validator_argv: 출력 경로 검증 명령.

        Returns:
            정규 명령들과 검증된 파일 입력.
        """

        setup_commands = tuple(self._command_argv(command) for command in setup_argvs)
        sync_core = self._command_argv(sync_core_argv)
        site_validators = tuple(
            self._command_argv(command) for command in site_validator_argvs
        )
        path_validator = self._command_argv(path_validator_argv)
        sync_file_inputs = self._validated_sync_file_inputs()
        if not setup_commands or not site_validators:
            raise _CandidateError(
                stage="configuration",
                issue_code=IssueCode.REQUIRED_CONFIG_MISSING,
            )
        if not self._valid_oid(base_commit) or not self._valid_run_id(self._run_id):
            raise _CandidateError(
                stage="configuration",
                issue_code=IssueCode.INVALID_RUNTIME_OPTION,
            )
        if self._artifact_root == self._source_repo or self._artifact_root.is_relative_to(
            self._source_repo
        ):
            raise _CandidateError(
                stage="sandbox",
                issue_code=IssueCode.SANDBOX_OPERATION_FAILED,
            )
        self._require_report_targets_absent()
        return (
            setup_commands,
            sync_core,
            site_validators,
            path_validator,
            sync_file_inputs,
        )

    def _prepare_candidate(
        self,
        state: _CandidateRunState,
        base_commit: str,
    ) -> Path:
        """승인 기준을 확인하고 격리 clone 준비.

        Args:
            state: 갱신할 candidate 실행 상태.
            base_commit: 승인 기준 Git commit ID.

        Returns:
            준비된 sandbox 경로.
        """

        state.stage = "approved-base"
        state.resolved_base = self._resolve_base(base_commit)
        state.stage = "sandbox"
        state.sandbox = self._new_sandbox()
        self._populate_clone(state.sandbox, state.resolved_base)
        return state.sandbox

    def _run_setup_phase(
        self,
        state: _CandidateRunState,
        sandbox: Path,
        setup_commands: tuple[tuple[str, ...], ...],
    ) -> None:
        """후보 준비 명령 전후 승인 기준 fingerprint 불변성 검증.

        Args:
            state: 갱신할 candidate 실행 상태.
            sandbox: 준비된 후보 저장소.
            setup_commands: 정규 후보 준비 명령 목록.
        """

        state.stage = "candidate-setup"
        base_fingerprint = self._source_fingerprint(
            sandbox,
            include_untracked=False,
        )
        for command in setup_commands:
            self._require_unmutated(
                sandbox,
                base_fingerprint,
                state.stage,
                include_untracked=False,
            )
            result = self._child(
                command,
                cwd=sandbox,
                environment={"HUSKY": "0"},
            )
            self._require_unmutated(
                sandbox,
                base_fingerprint,
                state.stage,
                include_untracked=False,
            )
            if result:
                raise _CandidateError(
                    stage=state.stage,
                    issue_code=IssueCode.RUNNER_OPERATION_FAILED,
                    returncode=result,
                )

    def _run_sync_phase(
        self,
        state: _CandidateRunState,
        sandbox: Path,
        sync_core: tuple[str, ...],
        sync_file_inputs: dict[str, bytes],
    ) -> None:
        """파일 입력을 임시 적재해 sync core를 실행하고 보고서 계약 검증.

        Args:
            state: 갱신할 candidate 실행 상태.
            sandbox: 준비된 후보 저장소.
            sync_core: 정규 번역 동기화 core 명령.
            sync_file_inputs: 검증된 환경별 파일 입력.
        """

        staged_environment: dict[str, str] = {}
        if sync_file_inputs:
            state.stage = "candidate-input"
            staged_environment = self._stage_sync_file_inputs(
                sandbox,
                sync_file_inputs,
            )
        state.stage = "sync-core"
        environment = dict(self._sync_environment)
        environment.update(staged_environment)
        environment.update(
            {
                FAILURE_REPORT_ENV: str(self._sync_report_path),
                RUN_ID_ENV: self._run_id,
            }
        )
        try:
            result = self._child(sync_core, cwd=sandbox, environment=environment)
        finally:
            if sync_file_inputs:
                state.stage = "candidate-input"
                self._remove_sync_file_inputs(sandbox, sync_file_inputs)
                state.stage = "sync-core"
        if result:
            raise _CandidateError(
                stage=state.stage,
                issue_code=None,
                returncode=result,
                report_path=self._sync_report_path,
            )
        self._reject_unexpected_report(self._sync_report_path, stage=state.stage)

    def _run_site_validators(
        self,
        state: _CandidateRunState,
        sandbox: Path,
        validators: tuple[tuple[str, ...], ...],
        fingerprint: bytes,
        environment: Mapping[str, str],
    ) -> None:
        """사이트 validator들을 실행하고 각 실행 뒤 후보 불변성 검증.

        Args:
            state: 갱신할 candidate 실행 상태.
            sandbox: 후보 저장소.
            validators: 정규 사이트 검증 명령 목록.
            fingerprint: 검증 전 후보 fingerprint.
            environment: validator 환경 변수.
        """

        state.stage = "site-validation"
        for validator in validators:
            result = self._child(
                validator,
                cwd=sandbox,
                environment=environment,
            )
            self._require_unmutated(sandbox, fingerprint, state.stage)
            if result:
                raise _CandidateError(
                    stage=state.stage,
                    issue_code=IssueCode.SITE_VALIDATION_FAILED,
                    returncode=result,
                )

    def _run_path_validator(
        self,
        state: _CandidateRunState,
        sandbox: Path,
        validator: tuple[str, ...],
        fingerprint: bytes,
        environment: Mapping[str, str],
    ) -> None:
        """경로 validator를 전용 실패 보고서 환경으로 실행.

        Args:
            state: 갱신할 candidate 실행 상태.
            sandbox: 후보 저장소.
            validator: 정규 경로 검증 명령.
            fingerprint: 검증 전 후보 fingerprint.
            environment: 공통 validator 환경 변수.
        """

        state.stage = "path-validation"
        path_environment = dict(environment)
        path_environment.update(
            {
                FAILURE_REPORT_ENV: str(self._path_report_path),
                RUN_ID_ENV: self._run_id,
            }
        )
        result = self._child(
            validator,
            cwd=sandbox,
            environment=path_environment,
        )
        self._require_unmutated(sandbox, fingerprint, state.stage)
        if result:
            raise _CandidateError(
                stage=state.stage,
                issue_code=None,
                returncode=result,
                report_path=self._path_report_path,
            )
        self._reject_unexpected_report(self._path_report_path, stage=state.stage)

    def _validate_candidate(
        self,
        state: _CandidateRunState,
        sandbox: Path,
        site_validators: tuple[tuple[str, ...], ...],
        path_validator: tuple[str, ...],
    ) -> None:
        """후보 index를 고정하고 사이트·경로 validator와 정리 수행.

        Args:
            state: 갱신할 candidate 실행 상태.
            sandbox: 후보 저장소.
            site_validators: 사이트 검증 명령 목록.
            path_validator: 경로 검증 명령.
        """

        state.stage = "candidate-index"
        self._git(sandbox, "add", "-A")
        fingerprint = self._source_fingerprint(sandbox, include_untracked=True)
        environment = self._validator_environment()
        self._run_site_validators(
            state,
            sandbox,
            site_validators,
            fingerprint,
            environment,
        )
        self._run_path_validator(
            state,
            sandbox,
            path_validator,
            fingerprint,
            environment,
        )
        state.stage = "candidate-cleanup"
        self._git(sandbox, "clean", "-dffX")
        self._require_unmutated(sandbox, fingerprint, state.stage)

    def _sealed_result(
        self,
        state: _CandidateRunState,
        sandbox: Path,
    ) -> CandidateResult:
        """검증된 후보 tree와 승인 기준 tree를 비교해 결과 봉인.

        Args:
            state: 갱신할 candidate 실행 상태.
            sandbox: 검증 완료 후보 저장소.

        Returns:
            봉인된 tree 식별자와 변경 여부.
        """

        state.stage = "tree-seal"
        verified_tree = self._git_text(sandbox, "write-tree")
        base_tree = self._git_text(
            sandbox,
            "rev-parse",
            "--verify",
            f"{state.resolved_base}^{{tree}}",
        )
        return CandidateResult(
            sandbox=sandbox,
            base_commit=state.resolved_base,
            verified_tree=verified_tree,
            has_changes=verified_tree != base_tree,
        )

    def _execute_candidate(
        self,
        state: _CandidateRunState,
        *,
        base_commit: str,
        setup_argvs: Sequence[Sequence[str]],
        sync_core_argv: Sequence[str],
        site_validator_argvs: Sequence[Sequence[str]],
        path_validator_argv: Sequence[str],
    ) -> CandidateResult:
        """검증된 단계 메서드를 순서대로 실행해 candidate 봉인.

        Args:
            state: 갱신할 candidate 실행 상태.
            base_commit: 승인 기준 Git commit ID.
            setup_argvs: 후보 준비 명령 목록.
            sync_core_argv: 번역 동기화 core 명령.
            site_validator_argvs: 사이트 검증 명령 목록.
            path_validator_argv: 출력 경로 검증 명령.

        Returns:
            성공한 봉인 candidate 결과.
        """

        commands = self._validated_commands(
            base_commit=base_commit,
            setup_argvs=setup_argvs,
            sync_core_argv=sync_core_argv,
            site_validator_argvs=site_validator_argvs,
            path_validator_argv=path_validator_argv,
        )
        setup, sync_core, site_validators, path_validator, file_inputs = commands
        sandbox = self._prepare_candidate(state, base_commit)
        self._run_setup_phase(state, sandbox, setup)
        self._run_sync_phase(state, sandbox, sync_core, file_inputs)
        self._validate_candidate(
            state,
            sandbox,
            site_validators,
            path_validator,
        )
        return self._sealed_result(state, sandbox)

    def run(
        self,
        *,
        base_commit: str,
        setup_argvs: Sequence[Sequence[str]],
        sync_core_argv: Sequence[str],
        site_validator_argvs: Sequence[Sequence[str]],
        path_validator_argv: Sequence[str],
    ) -> CandidateResult:
        """candidate 생성·검증과 Git이 무시하는 파일 정리 후 최종 tree 식별자 봉인."""

        state = _CandidateRunState()
        try:
            return self._execute_candidate(
                state,
                base_commit=base_commit,
                setup_argvs=setup_argvs,
                sync_core_argv=sync_core_argv,
                site_validator_argvs=site_validator_argvs,
                path_validator_argv=path_validator_argv,
            )
        except _DeadlineExceeded:
            failure = CandidateFailure(
                stage=state.stage,
                issue_code=IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            )
        except _CandidateError as exc:
            failure = exc.failure
        except _GitFailed as exc:
            issue_code = (
                IssueCode.SANDBOX_OPERATION_FAILED
                if state.stage in {"approved-base", "sandbox"}
                else IssueCode.RUNNER_OPERATION_FAILED
            )
            failure = CandidateFailure(
                stage=state.stage,
                issue_code=issue_code,
                returncode=exc.returncode,
            )
        except _ProcessStartFailed:
            failure = CandidateFailure(
                stage=state.stage,
                issue_code=IssueCode.RUNNER_OPERATION_FAILED,
            )
        except OSError, ValueError:
            issue_code = (
                IssueCode.SANDBOX_OPERATION_FAILED
                if state.stage in {"approved-base", "sandbox"}
                else IssueCode.RUNNER_OPERATION_FAILED
            )
            failure = CandidateFailure(stage=state.stage, issue_code=issue_code)
        except Exception:  # noqa: BLE001 - 예기치 않은 실패를 안정된 코드로 변환.
            failure = CandidateFailure(
                stage=state.stage,
                issue_code=IssueCode.UNCLASSIFIED_INTERNAL,
            )

        return CandidateResult(
            sandbox=state.sandbox,
            base_commit=state.resolved_base,
            failure=failure,
        )

    @staticmethod
    def _valid_oid(value: str) -> bool:
        """완전한 소문자 Git 객체 ID 형식 여부."""

        return (
            isinstance(value, str)
            and len(value) in {40, 64}
            and all(character in "0123456789abcdef" for character in value)
        )

    @staticmethod
    def _valid_run_id(value: str) -> bool:
        """실행 ID가 짧고 안전한 식별자인지 확인."""

        return (
            isinstance(value, str)
            and 0 < len(value) <= 128
            and value[0].isalnum()
            and all(character.isalnum() or character in "._-" for character in value)
        )

    def _require_report_targets_absent(self) -> None:
        """하위 단계 보고서 경로의 사전 부재 확인."""

        for path in (self._sync_report_path, self._path_report_path):
            if path.exists() or path.is_symlink():
                raise _CandidateError(
                    stage="configuration",
                    issue_code=IssueCode.INVALID_RUNTIME_OPTION,
                )

    def _validated_sync_file_inputs(self) -> dict[str, bytes]:
        """허용된 동기화 파일 입력의 이름과 바이트 형식 검증."""

        if set(self._sync_file_inputs) - set(_SYNC_FILE_INPUT_PATHS):
            raise _CandidateError(
                stage="configuration",
                issue_code=IssueCode.INVALID_RUNTIME_OPTION,
            )
        if any(
            not isinstance(contents, bytes)
            for contents in self._sync_file_inputs.values()
        ):
            raise _CandidateError(
                stage="configuration",
                issue_code=IssueCode.INVALID_RUNTIME_OPTION,
            )
        return dict(self._sync_file_inputs)

    @staticmethod
    def _directory_open_flags() -> int:
        """symlink 추적을 금지하는 디렉터리 열기 플래그 구성."""

        if not hasattr(os, "O_DIRECTORY") or not hasattr(os, "O_NOFOLLOW"):
            raise OSError("secure candidate input paths are unavailable")
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        if hasattr(os, "O_CLOEXEC"):
            flags |= os.O_CLOEXEC
        return flags

    @classmethod
    def _open_candidate_git(cls, sandbox: Path) -> tuple[int, int]:
        """candidate root와 내부 Git 디렉터리를 파일 설명자로 열기."""

        sandbox_descriptor = os.open(sandbox, cls._directory_open_flags())
        try:
            git_descriptor = os.open(
                ".git",
                cls._directory_open_flags(),
                dir_fd=sandbox_descriptor,
            )
        except BaseException:
            os.close(sandbox_descriptor)
            raise
        return sandbox_descriptor, git_descriptor

    @staticmethod
    def _write_all(descriptor: int, contents: bytes) -> None:
        """전체 바이트가 기록될 때까지 파일 설명자에 쓰기."""

        remaining = memoryview(contents)
        while remaining:
            written = os.write(descriptor, remaining)
            if written <= 0:
                raise OSError("candidate input write did not progress")
            remaining = remaining[written:]

    @staticmethod
    def _read_all(descriptor: int) -> bytes:
        """파일 설명자의 전체 바이트 읽기."""

        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                return b"".join(chunks)
            chunks.append(chunk)

    @classmethod
    def _create_staged_input_files(
        cls,
        input_descriptor: int,
        inputs: Mapping[str, bytes],
        created_files: list[str],
    ) -> None:
        """검증된 candidate 입력 파일을 전용 디렉터리에 생성.

        Args:
            input_descriptor: 전용 입력 디렉터리 설명자.
            inputs: 환경 변수 이름별 입력 바이트.

            created_files: 생성 즉시 파일 이름을 기록할 목록.
        """

        for environment_name, contents in inputs.items():
            filename = _SYNC_FILE_INPUT_PATHS[environment_name]
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
            if hasattr(os, "O_CLOEXEC"):
                flags |= os.O_CLOEXEC
            descriptor = os.open(
                filename,
                flags,
                mode=0,
                dir_fd=input_descriptor,
            )
            created_files.append(filename)
            try:
                cls._write_all(descriptor, contents)
                os.fchmod(descriptor, 0o400)
                os.fsync(descriptor)
            finally:
                os.close(descriptor)

    @staticmethod
    def _remove_created_input_files(
        input_descriptor: int,
        filenames: Sequence[str],
    ) -> None:
        """부분 생성된 candidate 입력 파일을 최선 노력으로 제거.

        Args:
            input_descriptor: 전용 입력 디렉터리 설명자.
            filenames: 제거할 생성 파일 이름 목록.
        """

        for filename in filenames:
            try:
                os.unlink(filename, dir_fd=input_descriptor)
            except OSError:
                pass

    @staticmethod
    def _staged_input_environment(
        sandbox: Path,
        inputs: Mapping[str, bytes],
    ) -> dict[str, str]:
        """적재된 candidate 파일 입력의 절대 환경 변수 mapping 구성.

        Args:
            sandbox: 후보 저장소 경로.
            inputs: 환경 변수 이름별 입력 바이트.

        Returns:
            환경 변수 이름별 적재 파일 절대 경로.
        """

        return {
            environment_name: str(
                sandbox
                / ".git"
                / _SYNC_INPUT_DIRECTORY
                / _SYNC_FILE_INPUT_PATHS[environment_name]
            )
            for environment_name in inputs
        }

    @classmethod
    def _stage_sync_file_inputs(
        cls,
        sandbox: Path,
        inputs: Mapping[str, bytes],
    ) -> dict[str, str]:
        """동기화 파일 입력을 candidate의 Git 전용 영역에 읽기 전용으로 적재."""

        sandbox_descriptor, git_descriptor = cls._open_candidate_git(sandbox)
        input_descriptor = -1
        created_directory = False
        created_files: list[str] = []
        try:
            os.mkdir(
                _SYNC_INPUT_DIRECTORY,
                mode=0o700,
                dir_fd=git_descriptor,
            )
            created_directory = True
            input_descriptor = os.open(
                _SYNC_INPUT_DIRECTORY,
                cls._directory_open_flags(),
                dir_fd=git_descriptor,
            )
            cls._create_staged_input_files(
                input_descriptor,
                inputs,
                created_files,
            )
            os.fsync(input_descriptor)
            return cls._staged_input_environment(sandbox, inputs)
        except BaseException:
            if input_descriptor >= 0:
                cls._remove_created_input_files(input_descriptor, created_files)
            if created_directory:
                try:
                    os.rmdir(_SYNC_INPUT_DIRECTORY, dir_fd=git_descriptor)
                except OSError:
                    pass
            raise
        finally:
            if input_descriptor >= 0:
                os.close(input_descriptor)
            os.close(git_descriptor)
            os.close(sandbox_descriptor)

    @classmethod
    def _remove_sync_file_inputs(
        cls,
        sandbox: Path,
        expected_inputs: Mapping[str, bytes],
    ) -> None:
        """적재한 동기화 파일 입력의 종류·모드·내용을 확인한 뒤 제거."""

        sandbox_descriptor, git_descriptor = cls._open_candidate_git(sandbox)
        input_descriptor = -1
        error: OSError | None = None
        try:
            input_descriptor = os.open(
                _SYNC_INPUT_DIRECTORY,
                cls._directory_open_flags(),
                dir_fd=git_descriptor,
            )
            for environment_name, expected in expected_inputs.items():
                filename = _SYNC_FILE_INPUT_PATHS[environment_name]
                flags = os.O_RDONLY | os.O_NOFOLLOW
                if hasattr(os, "O_CLOEXEC"):
                    flags |= os.O_CLOEXEC
                descriptor = os.open(
                    filename,
                    flags,
                    dir_fd=input_descriptor,
                )
                try:
                    metadata = os.fstat(descriptor)
                    if (
                        not stat.S_ISREG(metadata.st_mode)
                        or stat.S_IMODE(metadata.st_mode) != 0o400
                        or cls._read_all(descriptor) != expected
                    ):
                        error = OSError("candidate input changed during sync")
                finally:
                    os.close(descriptor)
                os.unlink(filename, dir_fd=input_descriptor)
            os.fsync(input_descriptor)
            os.close(input_descriptor)
            input_descriptor = -1
            os.rmdir(_SYNC_INPUT_DIRECTORY, dir_fd=git_descriptor)
            os.fsync(git_descriptor)
            if error is not None:
                raise error
        finally:
            if input_descriptor >= 0:
                os.close(input_descriptor)
            os.close(git_descriptor)
            os.close(sandbox_descriptor)

    @staticmethod
    def _reject_unexpected_report(path: Path, *, stage: str) -> None:
        """성공한 하위 단계가 남긴 예상 밖 실패 보고서 거부."""

        if path.exists() or path.is_symlink():
            raise _CandidateError(
                stage=stage,
                issue_code=IssueCode.UNCLASSIFIED_INTERNAL,
            )

    @staticmethod
    def _command_argv(argv: Sequence[str]) -> tuple[str, ...]:
        """shell 없는 실행에 사용할 argv 검증·고정."""

        if isinstance(argv, (str, bytes)):
            raise _CandidateError(
                stage="configuration",
                issue_code=IssueCode.REQUIRED_CONFIG_MISSING,
            )
        command = tuple(argv)
        if not command:
            raise _CandidateError(
                stage="configuration",
                issue_code=IssueCode.REQUIRED_CONFIG_MISSING,
            )
        if any(
            not isinstance(argument, str) or not argument or "\0" in argument
            for argument in command
        ):
            raise _CandidateError(
                stage="configuration",
                issue_code=IssueCode.INVALID_RUNTIME_OPTION,
            )
        return command

    def _remaining_timeout(self) -> float:
        """공통 워크플로 기한의 유효한 양수 잔여 시간 반환."""

        try:
            remaining = float(self._remaining_seconds())
        except Exception as exc:
            raise _CandidateError(
                stage="configuration",
                issue_code=IssueCode.INVALID_RUNTIME_OPTION,
            ) from exc
        if not math.isfinite(remaining):
            raise _CandidateError(
                stage="configuration",
                issue_code=IssueCode.INVALID_RUNTIME_OPTION,
            )
        if remaining <= 0:
            raise _DeadlineExceeded
        return remaining

    def _minimal_environment(self, sandbox: Path | None = None) -> dict[str, str]:
        """자격 증명과 Git 사용자 설정을 제외한 최소 실행 환경 구성."""

        environment = {
            key: value
            for key, value in os.environ.items()
            if key in _PASSTHROUGH_ENV or key.startswith("LC_")
        }
        home = Path(os.devnull) if sandbox is None else sandbox / ".git/candidate-home"
        if sandbox is not None:
            home.mkdir(exist_ok=True)
        environment.update(
            {
                "HOME": str(home),
                "XDG_CONFIG_HOME": str(home),
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_CONFIG_SYSTEM": os.devnull,
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_TERMINAL_PROMPT": "0",
            }
        )
        return environment

    def _validator_environment(self) -> dict[str, str]:
        """사이트·경로 검증기에 전달할 제한된 환경 구성."""

        environment: dict[str, str] = {}
        if WORKFLOW_DEADLINE_ENV in self._sync_environment:
            environment[WORKFLOW_DEADLINE_ENV] = self._sync_environment[
                WORKFLOW_DEADLINE_ENV
            ]
        node_options = os.environ.get("NODE_OPTIONS", "")
        if node_options in _SAFE_NODE_OPTIONS:
            environment["NODE_OPTIONS"] = node_options
        return environment

    def _process(
        self,
        argv: Sequence[str],
        *,
        cwd: Path,
        environment: Mapping[str, str],
        capture_output: bool,
        input_data: bytes | None = None,
    ) -> subprocess.CompletedProcess[bytes]:
        """공통 기한과 프로세스 격리를 적용한 명령 실행."""

        kwargs: dict[str, object] = {
            "cwd": cwd,
            "env": dict(environment),
            "check": False,
            "timeout": self._remaining_timeout(),
            "shell": False,
        }
        if capture_output:
            kwargs.update(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            kwargs.update(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if input_data is not None:
            kwargs["input"] = input_data
        try:
            return self._process_runner(list(argv), **kwargs)
        except subprocess.TimeoutExpired as exc:
            raise _DeadlineExceeded from exc
        except ProcessTreeError as exc:
            raise _ProcessStartFailed from exc
        except OSError as exc:
            raise _ProcessStartFailed from exc

    def _git_process(
        self,
        repo: Path,
        *args: str,
        input_data: bytes | None = None,
        environment: Mapping[str, str] | None = None,
    ) -> subprocess.CompletedProcess[bytes]:
        """격리 환경에서 Git 명령 실행."""

        result = self._process(
            ("git", *args),
            cwd=repo,
            environment=environment or self._minimal_environment(),
            capture_output=True,
            input_data=input_data,
        )
        if result.returncode:
            raise _GitFailed(result.returncode)
        return result

    def _git(
        self,
        repo: Path,
        *args: str,
        input_data: bytes | None = None,
        environment: Mapping[str, str] | None = None,
    ) -> bytes:
        """성공한 Git 명령의 표준 출력 바이트 반환."""

        return self._git_process(
            repo,
            *args,
            input_data=input_data,
            environment=environment,
        ).stdout

    def _git_text(self, repo: Path, *args: str) -> str:
        """성공한 Git 명령의 공백을 제거한 ASCII 출력 반환."""

        return self._git(repo, *args).strip().decode("ascii")

    def _resolve_base(self, base_commit: str) -> str:
        """승인 기준본 객체 ID를 commit 객체로 해석."""

        return self._git_text(
            self._source_repo,
            "rev-parse",
            "--verify",
            "--end-of-options",
            f"{base_commit}^{{commit}}",
        )

    def _new_sandbox(self) -> Path:
        """artifact root 아래에 예측 불가능한 candidate sandbox 생성."""

        self._artifact_root.mkdir(parents=True, exist_ok=True)
        return Path(
            tempfile.mkdtemp(prefix="translation-candidate-", dir=self._artifact_root)
        )

    def _populate_clone(self, sandbox: Path, base_commit: str) -> None:
        """로컬 객체를 직접 공유하지 않고 승인 기준본만 checkout한 remote 없는 clone 구성."""

        self._git_process(
            self._source_repo.parent,
            "clone",
            "--no-hardlinks",
            "--no-checkout",
            "--quiet",
            "--",
            str(self._source_repo),
            str(sandbox),
        )
        self._git(sandbox, "checkout", "--detach", "--quiet", base_commit)
        self._git(sandbox, "remote", "remove", "origin")
        checked_out = self._git_text(sandbox, "rev-parse", "HEAD")
        if checked_out != base_commit:
            raise _CandidateError(
                stage="sandbox",
                issue_code=IssueCode.SANDBOX_OPERATION_FAILED,
            )

    def _child(
        self,
        argv: Sequence[str],
        *,
        cwd: Path,
        environment: Mapping[str, str] | None = None,
    ) -> int:
        """최소 환경에서 하위 작업 실행 후 종료 코드 반환."""

        child_environment = self._minimal_environment(cwd)
        if environment is not None:
            child_environment.update(environment)
        result = self._process(
            argv,
            cwd=cwd,
            environment=child_environment,
            capture_output=False,
        )
        return result.returncode

    def _source_fingerprint(
        self,
        repo: Path,
        *,
        include_untracked: bool,
    ) -> bytes:
        """candidate의 HEAD·index·추적 파일과 선택적 미추적 파일 상태 지문 계산."""

        digest = hashlib.sha256()
        digest.update(b"HEAD\0")
        digest.update(self._git(repo, "rev-parse", "HEAD"))
        index = self._git(repo, "ls-files", "--stage", "-z")
        digest.update(b"INDEX\0")
        digest.update(index)

        paths = {
            entry.split(b"\t", 1)[1]
            for entry in index.split(b"\0")
            if entry and b"\t" in entry
        }
        if include_untracked:
            untracked = self._git(
                repo,
                "ls-files",
                "--others",
                "--exclude-standard",
                "-z",
            )
            digest.update(b"UNTRACKED\0")
            digest.update(untracked)
            paths.update(path for path in untracked.split(b"\0") if path)

        for raw_path in sorted(paths):
            digest.update(b"PATH\0")
            digest.update(raw_path)
            path = repo / Path(os.fsdecode(raw_path))
            try:
                metadata = path.lstat()
            except FileNotFoundError:
                digest.update(b"MISSING\0")
                continue
            mode = metadata.st_mode
            digest.update((mode & 0o177777).to_bytes(4, "big"))
            if stat.S_ISLNK(mode):
                digest.update(b"LINK\0")
                digest.update(os.fsencode(os.readlink(path)))
            elif stat.S_ISREG(mode):
                digest.update(b"FILE\0")
                with path.open("rb") as handle:
                    for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                        digest.update(chunk)
            else:
                digest.update(b"OTHER\0")
        return digest.digest()

    def _require_unmutated(
        self,
        sandbox: Path,
        expected: bytes,
        stage: str,
        *,
        include_untracked: bool = True,
    ) -> None:
        """candidate 원문 상태와 예상 지문의 일치 확인."""

        if (
            self._source_fingerprint(
                sandbox,
                include_untracked=include_untracked,
            )
            != expected
        ):
            raise _CandidateError(
                stage=stage,
                issue_code=IssueCode.CANDIDATE_SOURCE_MUTATED,
            )
