"""안정된 워크플로 실패와 결정적 실패 보고서."""

from __future__ import annotations

import json
import os
import re
import secrets
import stat
import sys
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import IntEnum, StrEnum
from pathlib import Path, PurePosixPath
from typing import TextIO

_MAX_MESSAGE_LENGTH = 240


class ErrorClassification(StrEnum):
    """워크플로 단계 소유권별 오류 분류."""

    CONFIGURATION = "C"
    INPUT = "I"
    PLAN = "P"
    TRANSLATION = "T"
    POSTPROCESSING = "R"
    VERIFICATION = "V"
    SIDEBAR = "S"
    OUTPUT = "A"
    INFRASTRUCTURE = "X"


class ExitCode(IntEnum):
    """호출자가 구분할 워크플로 종료 의미."""

    SUCCESS = 0
    CONTROLLED_FAILURE = 1
    INFRASTRUCTURE_FAILURE = 2


class IssueCode(StrEnum):
    """보고서와 로그에서 공유할 안정된 문제 코드."""

    PROVIDER_SELECTION_INVALID = "PROVIDER_SELECTION_INVALID"
    PROVIDER_CREDENTIAL_MISSING = "PROVIDER_CREDENTIAL_MISSING"
    REQUIRED_CONFIG_MISSING = "REQUIRED_CONFIG_MISSING"
    STALE_LINK_REGISTRY_INVALID = "STALE_LINK_REGISTRY_INVALID"
    TOKENIZER_METADATA_UNAVAILABLE = "TOKENIZER_METADATA_UNAVAILABLE"
    INVALID_REQUEST_BUDGET = "INVALID_REQUEST_BUDGET"
    INVALID_RUNTIME_OPTION = "INVALID_RUNTIME_OPTION"

    FILE_STATE_CONFLICT = "FILE_STATE_CONFLICT"
    RAW_DIFF_MISSING = "RAW_DIFF_MISSING"
    PREPROCESS_PLACEHOLDER_INVALID = "PREPROCESS_PLACEHOLDER_INVALID"
    PREPROCESS_BOUNDARY_AMBIGUOUS = "PREPROCESS_BOUNDARY_AMBIGUOUS"
    INVALID_SELECTOR = "INVALID_SELECTOR"
    INVALID_MANIFEST = "INVALID_MANIFEST"
    MANIFEST_COMMIT_UNRESOLVED = "MANIFEST_COMMIT_UNRESOLVED"
    MANIFEST_DIGEST_MISMATCH = "MANIFEST_DIGEST_MISMATCH"
    MANIFEST_EXPORT_CONFLICT = "MANIFEST_EXPORT_CONFLICT"
    STALE_LINK_REGISTRY_CHANGED = "STALE_LINK_REGISTRY_CHANGED"

    BLOCK_BOUNDARY_AMBIGUOUS = "BLOCK_BOUNDARY_AMBIGUOUS"
    PATCH_LOCATION_AMBIGUOUS = "PATCH_LOCATION_AMBIGUOUS"
    ANNOTATION_STATE_INVALID = "ANNOTATION_STATE_INVALID"
    PATCH_RESULT_CARDINALITY_INVALID = "PATCH_RESULT_CARDINALITY_INVALID"
    UNSUPPORTED_OVERSIZE_BLOCK = "UNSUPPORTED_OVERSIZE_BLOCK"
    UNSUPPORTED_CHANGE_UNIT = "UNSUPPORTED_CHANGE_UNIT"

    PROVIDER_TRANSIENT_EXHAUSTED = "PROVIDER_TRANSIENT_EXHAUSTED"
    PROVIDER_REQUEST_REJECTED = "PROVIDER_REQUEST_REJECTED"
    CLI_PROVIDER_FAILED = "CLI_PROVIDER_FAILED"
    PROVIDER_PARTIAL_RESPONSE = "PROVIDER_PARTIAL_RESPONSE"
    RESPONSE_CONTRACT_FAILED = "RESPONSE_CONTRACT_FAILED"
    RUN_DEADLINE_EXCEEDED = "RUN_DEADLINE_EXCEEDED"

    RESTORE_MAP_INVALID = "RESTORE_MAP_INVALID"
    MARKUP_RESTORE_AMBIGUOUS = "MARKUP_RESTORE_AMBIGUOUS"
    POSTPROCESS_RESIDUE = "POSTPROCESS_RESIDUE"
    VERIFICATION_BASIS_GENERATION_FAILED = "VERIFICATION_BASIS_GENERATION_FAILED"
    NO_WRITE_MUTATION = "NO_WRITE_MUTATION"

    RESIDUAL_PATTERN = "RESIDUAL_PATTERN"
    SOURCE_STRUCTURE_MISMATCH = "SOURCE_STRUCTURE_MISMATCH"
    LIST_TABLE_STRUCTURE_MISMATCH = "LIST_TABLE_STRUCTURE_MISMATCH"
    PIPELINE_ANNOTATION_MISMATCH = "PIPELINE_ANNOTATION_MISMATCH"
    SOURCE_COMMENT_MISMATCH = "SOURCE_COMMENT_MISMATCH"
    FRONT_MATTER_MISMATCH = "FRONT_MATTER_MISMATCH"
    VERIFICATION_INPUT_CHANGED = "VERIFICATION_INPUT_CHANGED"

    SIDEBAR_INPUT_INVALID = "SIDEBAR_INPUT_INVALID"
    SIDEBAR_DANGLING_DOC = "SIDEBAR_DANGLING_DOC"
    SIDEBAR_PATH_INVALID = "SIDEBAR_PATH_INVALID"
    SIDEBAR_CONTENT_MISMATCH = "SIDEBAR_CONTENT_MISMATCH"
    SIDEBAR_OVERRIDE_REMAINS = "SIDEBAR_OVERRIDE_REMAINS"
    SIDEBAR_INPUT_CHANGED = "SIDEBAR_INPUT_CHANGED"

    OUTPUT_PATH_FORBIDDEN = "OUTPUT_PATH_FORBIDDEN"

    RUNNER_OPERATION_FAILED = "RUNNER_OPERATION_FAILED"
    REPORT_WRITE_FAILED = "REPORT_WRITE_FAILED"
    UNCLASSIFIED_INTERNAL = "UNCLASSIFIED_INTERNAL"


_CODES_BY_CLASSIFICATION: Mapping[ErrorClassification, frozenset[IssueCode]] = {
    ErrorClassification.CONFIGURATION: frozenset(
        {
            IssueCode.PROVIDER_SELECTION_INVALID,
            IssueCode.PROVIDER_CREDENTIAL_MISSING,
            IssueCode.REQUIRED_CONFIG_MISSING,
            IssueCode.STALE_LINK_REGISTRY_INVALID,
            IssueCode.TOKENIZER_METADATA_UNAVAILABLE,
            IssueCode.INVALID_REQUEST_BUDGET,
            IssueCode.INVALID_RUNTIME_OPTION,
        }
    ),
    ErrorClassification.INPUT: frozenset(
        {
            IssueCode.FILE_STATE_CONFLICT,
            IssueCode.RAW_DIFF_MISSING,
            IssueCode.PREPROCESS_PLACEHOLDER_INVALID,
            IssueCode.PREPROCESS_BOUNDARY_AMBIGUOUS,
            IssueCode.INVALID_SELECTOR,
            IssueCode.INVALID_MANIFEST,
            IssueCode.MANIFEST_COMMIT_UNRESOLVED,
            IssueCode.MANIFEST_DIGEST_MISMATCH,
            IssueCode.MANIFEST_EXPORT_CONFLICT,
            IssueCode.STALE_LINK_REGISTRY_CHANGED,
        }
    ),
    ErrorClassification.PLAN: frozenset(
        {
            IssueCode.BLOCK_BOUNDARY_AMBIGUOUS,
            IssueCode.PATCH_LOCATION_AMBIGUOUS,
            IssueCode.ANNOTATION_STATE_INVALID,
            IssueCode.PATCH_RESULT_CARDINALITY_INVALID,
            IssueCode.UNSUPPORTED_OVERSIZE_BLOCK,
            IssueCode.UNSUPPORTED_CHANGE_UNIT,
        }
    ),
    ErrorClassification.TRANSLATION: frozenset(
        {
            IssueCode.PROVIDER_TRANSIENT_EXHAUSTED,
            IssueCode.PROVIDER_REQUEST_REJECTED,
            IssueCode.CLI_PROVIDER_FAILED,
            IssueCode.PROVIDER_PARTIAL_RESPONSE,
            IssueCode.RESPONSE_CONTRACT_FAILED,
            IssueCode.RUN_DEADLINE_EXCEEDED,
        }
    ),
    ErrorClassification.POSTPROCESSING: frozenset(
        {
            IssueCode.RESTORE_MAP_INVALID,
            IssueCode.MARKUP_RESTORE_AMBIGUOUS,
            IssueCode.POSTPROCESS_RESIDUE,
            IssueCode.VERIFICATION_BASIS_GENERATION_FAILED,
            IssueCode.NO_WRITE_MUTATION,
        }
    ),
    ErrorClassification.VERIFICATION: frozenset(
        {
            IssueCode.RESIDUAL_PATTERN,
            IssueCode.SOURCE_STRUCTURE_MISMATCH,
            IssueCode.LIST_TABLE_STRUCTURE_MISMATCH,
            IssueCode.PIPELINE_ANNOTATION_MISMATCH,
            IssueCode.SOURCE_COMMENT_MISMATCH,
            IssueCode.FRONT_MATTER_MISMATCH,
            IssueCode.VERIFICATION_INPUT_CHANGED,
        }
    ),
    ErrorClassification.SIDEBAR: frozenset(
        {
            IssueCode.SIDEBAR_INPUT_INVALID,
            IssueCode.SIDEBAR_DANGLING_DOC,
            IssueCode.SIDEBAR_PATH_INVALID,
            IssueCode.SIDEBAR_CONTENT_MISMATCH,
            IssueCode.SIDEBAR_OVERRIDE_REMAINS,
            IssueCode.SIDEBAR_INPUT_CHANGED,
        }
    ),
    ErrorClassification.OUTPUT: frozenset(
        {
            IssueCode.OUTPUT_PATH_FORBIDDEN,
        }
    ),
    ErrorClassification.INFRASTRUCTURE: frozenset(
        {
            IssueCode.RUNNER_OPERATION_FAILED,
            IssueCode.REPORT_WRITE_FAILED,
            IssueCode.UNCLASSIFIED_INTERNAL,
        }
    ),
}

_CLASSIFICATION_BY_CODE = {
    code: classification
    for classification, codes in _CODES_BY_CLASSIFICATION.items()
    for code in codes
}

if set(_CLASSIFICATION_BY_CODE) != set(IssueCode):
    raise RuntimeError("every stable issue code must have exactly one classification")


def _as_issue_code(code: IssueCode | str) -> IssueCode:
    """문자열 또는 열거형 값을 문제 코드 열거형으로 정규화."""

    return code if isinstance(code, IssueCode) else IssueCode(code)


def classification_for(code: IssueCode | str) -> ErrorClassification:
    """문제 코드의 오류 분류 반환."""

    return _CLASSIFICATION_BY_CODE[_as_issue_code(code)]


def exit_code_for(code: IssueCode | str) -> ExitCode:
    """문제 코드의 프로세스 종료 의미 반환."""

    code = _as_issue_code(code)
    if classification_for(code) is ErrorClassification.INFRASTRUCTURE:
        return ExitCode.INFRASTRUCTURE_FAILURE
    return ExitCode.CONTROLLED_FAILURE


@dataclass(frozen=True, slots=True)
class ProviderAttempts:
    """provider transport와 응답 평가 시도 횟수."""

    response_evaluation: int
    transport: int

    def __post_init__(self) -> None:
        """시도 횟수의 정수·비음수 불변식 검증."""

        for name, value in (
            ("response_evaluation", self.response_evaluation),
            ("transport", self.transport),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"{name} must be a non-negative integer")

    def to_mapping(self) -> dict[str, int]:
        """정규 보고서용 mapping 변환."""

        return {
            "response_evaluation": self.response_evaluation,
            "transport": self.transport,
        }


_SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)\b(authorization|api[_-]?key|access[_-]?token|token|secret|password)"
    r"\b\s*[:=]\s*(?:bearer\s+)?(?:\"[^\"]*\"|'[^']*'|[^\s,;]+)"
)
_BEARER_RE = re.compile(r"(?i)\bbearer\s+[^\s,;]+")
_OPENAI_KEY_RE = re.compile(r"(?i)\bsk-[a-z0-9_-]{8,}")
_WINDOWS_ABSOLUTE_PATH_RE = re.compile(r"(?i)\b[a-z]:\\(?:[^\s\\]+\\)*[^\s\\]*")
_POSIX_ABSOLUTE_PATH_RE = re.compile(
    r"(?<![\w./:])/(?!docs(?:/|(?=$)))[^\s\"'`<>()\[\]{},;]+"
)
_BASE64_RE = re.compile(r"(?<![A-Za-z0-9+/=])[A-Za-z0-9+/=]{40,}")
_WHITESPACE_RE = re.compile(r"\s+")


def redact_message(message: str) -> str:
    """진단 메시지의 자격 증명·절대 경로·긴 데이터 제거 후 공백과 길이 정규화."""

    if not isinstance(message, str):
        raise TypeError("message must be a string")
    redacted = _SECRET_ASSIGNMENT_RE.sub(
        lambda match: f"{match.group(1)}=<redacted>",
        message,
    )
    redacted = _BEARER_RE.sub("Bearer <redacted>", redacted)
    redacted = _OPENAI_KEY_RE.sub("<redacted-key>", redacted)
    redacted = _WINDOWS_ABSOLUTE_PATH_RE.sub("<redacted-path>", redacted)
    redacted = _POSIX_ABSOLUTE_PATH_RE.sub("<redacted-path>", redacted)
    redacted = _BASE64_RE.sub("<redacted-base64>", redacted)
    redacted = _WHITESPACE_RE.sub(" ", redacted).strip()
    if not redacted:
        redacted = "redacted failure"
    if len(redacted) > _MAX_MESSAGE_LENGTH:
        redacted = redacted[: _MAX_MESSAGE_LENGTH - 1].rstrip() + "…"
    return redacted


@dataclass(frozen=True, slots=True)
class FailureEvent:
    """단일 문제와 선택적 구조 문맥을 담은 실패 이벤트."""

    code: IssueCode
    stage: str
    message: str
    version: str | None = None
    locale: str | None = None
    document: str | None = None
    plan_id: str | None = None
    structural_address: str | None = None
    attempts: ProviderAttempts | None = None

    def __post_init__(self) -> None:
        """문제 코드·provider 시도 계약 검증과 메시지 정제."""

        code = _as_issue_code(self.code)
        if exit_code_for(code) is ExitCode.SUCCESS:
            raise ValueError(f"{code.value} is not a failure")
        is_provider_failure = (
            classification_for(code) is ErrorClassification.TRANSLATION
        )
        if is_provider_failure != (self.attempts is not None):
            raise ValueError(
                "attempts must be present only for translation provider failures"
            )
        object.__setattr__(self, "code", code)
        object.__setattr__(self, "message", redact_message(self.message))

    @property
    def classification(self) -> ErrorClassification:
        """현재 실패의 오류 분류."""

        return classification_for(self.code)

    @property
    def exit_code(self) -> ExitCode:
        """현재 실패의 프로세스 종료 의미."""

        return exit_code_for(self.code)


def final_exit_code(failures: Iterable[FailureEvent]) -> ExitCode:
    """전체 실패 중 우선순위가 가장 높은 종료 코드 선택."""

    result = ExitCode.SUCCESS
    for failure in failures:
        result = max(result, failure.exit_code)
    return result


def select_primary_failure(failures: Iterable[FailureEvent]) -> FailureEvent:
    """종료 코드 우선순위가 가장 높은 최초 실패 선택."""

    iterator = iter(failures)
    try:
        primary = next(iterator)
    except StopIteration as exc:
        raise ValueError("at least one failure is required") from exc
    for failure in iterator:
        if failure.exit_code > primary.exit_code:
            primary = failure
    return primary


def _validate_identifier(value: str, *, name: str, maximum: int = 128) -> str:
    """보고서용 짧은 식별자 검증."""

    if not isinstance(value, str) or not value or len(value) > maximum:
        raise ValueError(f"{name} must be a non-empty short identifier")
    if not value[0].isalnum() or any(
        not (character.isalnum() or character in "._-") for character in value
    ):
        raise ValueError(f"{name} contains unsupported characters")
    return value


def _validate_optional_context(value: str | None, *, name: str) -> str | None:
    """선택적 짧은 문맥 문자열 검증."""

    if value is None:
        return None
    if not isinstance(value, str) or not value or len(value) > 256:
        raise ValueError(f"{name} must be a non-empty short string")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError(f"{name} contains control characters")
    return value


def _validate_relative_path(value: str | None, *, name: str) -> str | None:
    """선택적 POSIX 저장소 상대 경로 검증."""

    if value is None:
        return None
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError(f"{name} must be a repository-relative POSIX path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in value.split("/")):
        raise ValueError(f"{name} must be a repository-relative POSIX path")
    return value


@dataclass(frozen=True, slots=True)
class FailureReport:
    """한 실행의 primary 실패와 전체 문제를 담은 정규 보고서."""

    run_id: str
    primary: FailureEvent
    failures: tuple[FailureEvent, ...]

    @classmethod
    def build(
        cls,
        *,
        run_id: str,
        failures: Iterable[FailureEvent],
    ) -> FailureReport:
        """실패 목록을 검증하고 primary 실패가 정해진 보고서 구성."""

        collected = tuple(failures)
        primary = select_primary_failure(collected)
        _validate_identifier(run_id, name="run_id")
        for failure in collected:
            _validate_identifier(failure.stage, name="stage")
            _validate_optional_context(failure.version, name="version")
            _validate_optional_context(failure.locale, name="locale")
            _validate_relative_path(failure.document, name="document")
            _validate_optional_context(failure.plan_id, name="plan_id")
            _validate_optional_context(
                failure.structural_address,
                name="structural_address",
            )
        return cls(
            run_id=run_id,
            primary=primary,
            failures=collected,
        )

    def to_mapping(self) -> dict[str, object]:
        """문제 목록에 결정적 정렬을 적용한 보고서 mapping 변환."""

        primary = self.primary
        issues = sorted(
            self.failures,
            key=lambda failure: (
                failure.code.value.encode("utf-8"),
                (failure.structural_address or "").encode("utf-8"),
                failure.message.encode("utf-8"),
            ),
        )
        return {
            "schema_version": 1,
            "run_id": self.run_id,
            "stage": primary.stage,
            "classification": primary.classification.value,
            "code": primary.code.value,
            "exit_code": int(final_exit_code(self.failures)),
            "version": primary.version,
            "locale": primary.locale,
            "document": primary.document,
            "plan_id": primary.plan_id,
            "structural_address": primary.structural_address,
            "attempts": (
                primary.attempts.to_mapping() if primary.attempts is not None else None
            ),
            "issues": [
                {
                    "code": failure.code.value,
                    "structural_address": failure.structural_address,
                    "message": failure.message,
                }
                for failure in issues
            ],
        }

    def to_bytes(self) -> bytes:
        """키가 정렬되고 공백이 제거된 UTF-8 JSON과 마지막 LF 바이트 생성."""

        return (
            json.dumps(
                self.to_mapping(),
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")


def write_failure_report_exact(
    report: FailureReport,
    *,
    target: Path,
    stderr: TextIO | None = None,
) -> Path | None:
    """symlink가 없는 정확한 경로에 보고서를 교체 없이 원자적으로 기록."""
    target = Path(target)
    try:
        contents = report.to_bytes()
        parent_path = Path(os.path.abspath(target.parent))
        if target.name in {"", ".", ".."} or ".." in target.parts:
            raise ValueError("failure report target is invalid")
        parent_descriptor = _open_directory_without_symlinks(parent_path)
        try:
            _write_no_replace(
                parent_descriptor,
                parent_path=parent_path,
                target_name=target.name,
                contents=contents,
            )
        finally:
            os.close(parent_descriptor)
    except OSError, TypeError, ValueError:
        return _report_write_failed(stderr)
    return target


def _directory_open_flags() -> int:
    """지원되는 symlink 방지 옵션을 포함한 디렉터리 열기 플래그 구성."""

    flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    return flags


def _open_directory_without_symlinks(path: Path) -> int:
    """각 상위 경로의 symlink 여부와 동일성을 확인하며 디렉터리 열기."""

    absolute = Path(os.path.abspath(path))
    if not absolute.is_absolute() or not absolute.anchor:
        raise ValueError("failure report parent must be absolute")

    flags = _directory_open_flags()
    descriptor = os.open(absolute.anchor, flags)
    try:
        for part in absolute.parts[1:]:
            entry_status = os.stat(
                part,
                dir_fd=descriptor,
                follow_symlinks=False,
            )
            if not stat.S_ISDIR(entry_status.st_mode):
                raise NotADirectoryError("failure report ancestor is not a directory")
            child = os.open(part, flags, dir_fd=descriptor)
            try:
                if not os.path.samestat(entry_status, os.fstat(child)):
                    raise OSError("failure report ancestor changed while opening")
            except BaseException:
                os.close(child)
                raise
            os.close(descriptor)
            descriptor = child
    except BaseException:
        os.close(descriptor)
        raise
    return descriptor


def _directory_path_matches(
    descriptor: int,
    path: Path,
) -> bool:
    """열린 파일 설명자와 현재 디렉터리 경로의 동일성 확인."""

    comparison = -1
    try:
        comparison = _open_directory_without_symlinks(path)
        return os.path.samestat(os.fstat(descriptor), os.fstat(comparison))
    except OSError:
        return False
    finally:
        if comparison >= 0:
            os.close(comparison)


def _unlink_if_same(
    parent_descriptor: int,
    name: str,
    expected_status: os.stat_result,
) -> bool:
    """현재 항목이 예상 파일과 같을 때만 제거."""

    try:
        current_status = os.stat(
            name,
            dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
    except FileNotFoundError:
        return True
    except OSError:
        return False
    if not os.path.samestat(current_status, expected_status):
        return False
    try:
        os.unlink(name, dir_fd=parent_descriptor)
    except OSError:
        return False
    return True


def _new_temporary_file(
    parent_descriptor: int,
    target_name: str,
) -> tuple[int, str, os.stat_result]:
    """대상 디렉터리에 고유한 0600 임시 보고서 파일을 배타적으로 생성."""

    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW

    for _ in range(16):
        name = f".translation-sync-failure-{secrets.token_hex(16)}.tmp"
        if name == target_name:
            continue
        try:
            descriptor = os.open(
                name,
                flags,
                0o600,
                dir_fd=parent_descriptor,
            )
        except FileExistsError:
            continue
        try:
            return descriptor, name, os.fstat(descriptor)
        except BaseException:
            try:
                os.close(descriptor)
            finally:
                try:
                    os.unlink(name, dir_fd=parent_descriptor)
                except OSError:
                    pass
            raise
    raise FileExistsError("failure report temporary name is unavailable")


def _write_all(descriptor: int, contents: bytes) -> None:
    """전체 바이트가 기록될 때까지 파일 설명자에 쓰기."""

    remaining = memoryview(contents)
    while remaining:
        try:
            written = os.write(descriptor, remaining)
        except InterruptedError:
            continue
        if not isinstance(written, int) or written <= 0:
            raise OSError("failure report write did not make progress")
        remaining = remaining[written:]


def _require_target_absent(parent_descriptor: int, target_name: str) -> None:
    """기존 실패 보고서 대상이 없는지 확인.

    Args:
        parent_descriptor: 대상 상위 디렉터리 설명자.
        target_name: 기록할 실패 보고서 파일 이름.
    """

    try:
        os.stat(
            target_name,
            dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
    except FileNotFoundError:
        return
    raise FileExistsError("failure report target already exists")


def _write_temporary_report(
    descriptor: int,
    status: os.stat_result,
    contents: bytes,
) -> None:
    """임시 일반 파일에 실패 보고서를 기록하고 동기화.

    Args:
        descriptor: 임시 파일 설명자.
        status: 임시 파일 생성 직후 상태.
        contents: 기록할 직렬화된 실패 보고서.
    """

    if not stat.S_ISREG(status.st_mode):
        raise OSError("failure report temporary file is not regular")
    _write_all(descriptor, contents)
    os.fsync(descriptor)


def _link_temporary_report(
    parent_descriptor: int,
    *,
    parent_path: Path,
    temporary_name: str,
    target_name: str,
    temporary_status: os.stat_result,
) -> None:
    """검증된 임시 파일을 최종 이름으로 연결하고 동일성 확인.

    Args:
        parent_descriptor: 대상 상위 디렉터리 설명자.
        parent_path: 열 때 검증한 상위 디렉터리 경로.
        temporary_name: 임시 파일 이름.
        target_name: 최종 실패 보고서 파일 이름.
        temporary_status: 임시 파일 생성 직후 상태.
    """

    if not _directory_path_matches(parent_descriptor, parent_path):
        raise OSError("failure report parent changed before write")
    os.link(
        temporary_name,
        target_name,
        src_dir_fd=parent_descriptor,
        dst_dir_fd=parent_descriptor,
        follow_symlinks=False,
    )
    try:
        target_status = os.stat(
            target_name,
            dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
        if not os.path.samestat(
            temporary_status, target_status
        ) or not _directory_path_matches(parent_descriptor, parent_path):
            raise OSError("failure report path changed during write")
    except BaseException:
        _unlink_if_same(parent_descriptor, target_name, temporary_status)
        raise


def _cleanup_failed_write(
    parent_descriptor: int,
    *,
    target_name: str,
    temporary_name: str,
    temporary_status: os.stat_result,
    linked: bool,
) -> None:
    """실패한 기록 작업의 동일 파일 링크와 임시 파일 정리.

    Args:
        parent_descriptor: 대상 상위 디렉터리 설명자.
        target_name: 최종 실패 보고서 파일 이름.
        temporary_name: 임시 파일 이름.
        temporary_status: 임시 파일 생성 직후 상태.
        linked: 최종 이름 hard link 생성 여부.
    """

    if linked:
        _unlink_if_same(parent_descriptor, target_name, temporary_status)
    _unlink_if_same(parent_descriptor, temporary_name, temporary_status)
    try:
        os.fsync(parent_descriptor)
    except OSError:
        pass


def _write_no_replace(
    parent_descriptor: int,
    *,
    parent_path: Path,
    target_name: str,
    contents: bytes,
) -> None:
    """fsync된 임시 파일을 기존 대상을 교체하지 않는 hard link로 원자적 기록."""

    _require_target_absent(parent_descriptor, target_name)

    temporary_descriptor, temporary_name, temporary_status = _new_temporary_file(
        parent_descriptor,
        target_name,
    )
    linked = False
    try:
        _write_temporary_report(
            temporary_descriptor,
            temporary_status,
            contents,
        )
        os.close(temporary_descriptor)
        temporary_descriptor = -1

        _link_temporary_report(
            parent_descriptor,
            parent_path=parent_path,
            temporary_name=temporary_name,
            target_name=target_name,
            temporary_status=temporary_status,
        )
        linked = True
        if not _unlink_if_same(
            parent_descriptor,
            temporary_name,
            temporary_status,
        ):
            raise OSError("failure report temporary file could not be removed")
        os.fsync(parent_descriptor)
    except BaseException:
        if temporary_descriptor >= 0:
            try:
                os.close(temporary_descriptor)
            except OSError:
                pass
        _cleanup_failed_write(
            parent_descriptor,
            target_name=target_name,
            temporary_name=temporary_name,
            temporary_status=temporary_status,
            linked=linked,
        )
        raise


def _report_write_failed(stderr: TextIO | None) -> None:
    """고정된 보고서 기록 실패 진단을 표준 오류에 출력."""

    output = stderr if stderr is not None else sys.stderr
    print(
        "REPORT_WRITE_FAILED: failure report could not be written",
        file=output,
    )
