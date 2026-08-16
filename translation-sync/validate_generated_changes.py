#!/usr/bin/env python3
"""번역 동기화 출력 계약을 벗어난 후보 변경 거부."""

from __future__ import annotations

import math
import os
import re
import stat
import subprocess
import sys
import time
import unicodedata
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from sync import postprocess, preprocess
from sync.common.stale_links import (
    StaleLinkRegistry,
    StaleLinkRegistryError,
    load_stale_link_registry,
)
from sync.common.versions import UNTRANSLATED_DOCUMENTS, load_versions
from sync.runtime.failure import (
    ExitCode,
    FailureEvent,
    FailureReport,
    IssueCode,
    final_exit_code,
    write_failure_report_exact,
)
from sync.runtime.process import ProcessTreeError, run_process_tree
from sync.verification import document as document_verification
from sync.verification.document import VerifiedLocaleArtifact

REPO_ROOT = Path(__file__).resolve().parent.parent
FAILURE_REPORT_ENV = "TRANSLATION_FAILURE_REPORT"
RUN_ID_ENV = "TRANSLATION_RUN_ID"
WORKFLOW_DEADLINE_ENV = "TRANSLATION_WORKFLOW_DEADLINE_MONOTONIC"
_STAGE = "path-validation"
_VERSION = r"(?:master|\d+\.x)"
_DOCUMENT = r"(?P<doc>.+\.md)"
_SHA256_RE = re.compile(r"[0-9a-f]{64}")
_ALLOWED_PATHS = (
    re.compile(
        rf"i18n/en/docusaurus-plugin-content-docs/version-{_VERSION}/{_DOCUMENT}"
    ),
    re.compile(
        rf"i18n/ja/docusaurus-plugin-content-docs/version-{_VERSION}/{_DOCUMENT}"
    ),
    re.compile(rf"versioned_docs/version-{_VERSION}/{_DOCUMENT}"),
    re.compile(rf"versioned_sidebars/version-{_VERSION}-sidebars\.json"),
    re.compile(
        rf"i18n/(?:ko|ja)/docusaurus-plugin-content-docs/version-{_VERSION}\.json"
    ),
)
_DOCUMENT_PATHS = (
    (
        "en",
        re.compile(
            rf"i18n/en/docusaurus-plugin-content-docs/"
            rf"version-(?P<version>{_VERSION})/{_DOCUMENT}"
        ),
    ),
    (
        "ko",
        re.compile(
            rf"versioned_docs/version-(?P<version>{_VERSION})/"
            rf"{_DOCUMENT}"
        ),
    ),
    (
        "ja",
        re.compile(
            rf"i18n/ja/docusaurus-plugin-content-docs/"
            rf"version-(?P<version>{_VERSION})/{_DOCUMENT}"
        ),
    ),
)
_PATH_VERSION_RE = re.compile(r"(?:^|/)version-(?P<version>master|\d+\.x)(?:/|[-.])")
_SIDEBAR_OVERRIDE_GLOB = "i18n/{locale}/docusaurus-plugin-content-docs/version-*.json"
_SHARED_SIDEBAR_RE = re.compile(
    rf"versioned_sidebars/version-(?P<version>{_VERSION})-sidebars\.json"
)
_LOCALE_SIDEBAR_RE = re.compile(
    rf"i18n/(?:ko|ja)/docusaurus-plugin-content-docs/"
    rf"version-(?P<version>{_VERSION})\.json"
)
_NAME_STATUS_RE = re.compile(r"(?:[ADMTUXB]|[CR](?:100|0\d{2}))")
_INVALID_NAME_STATUS = "invalid git name-status output"
_UNCHANGED_LOCALE_PATHS = {
    "ko": "versioned_docs/version-{version}/{doc}",
    "ja": ("i18n/ja/docusaurus-plugin-content-docs/version-{version}/{doc}"),
}
_GIT_PASSTHROUGH_ENV = frozenset(
    {
        "LANG",
        "LANGUAGE",
        "PATH",
        "SYSTEMROOT",
        "TMPDIR",
    }
)
_GIT_PREFIX = ("git", "-c", "core.fsmonitor=false")

ProcessRunner = Callable[..., subprocess.CompletedProcess[bytes]]


@dataclass(frozen=True, slots=True)
class _ChangeIssue:
    """산출물 경로 또는 상태 정합성 문제."""

    code: IssueCode
    message: str
    version: str | None = None
    locale: str | None = None
    document: str | None = None
    structural_address: str | None = None

    def event(self) -> FailureEvent:
        """안정적 경로 검증 실패 이벤트로 변환."""

        return FailureEvent(
            code=self.code,
            stage=_STAGE,
            message=self.message,
            version=self.version,
            locale=self.locale,
            document=self.document,
            structural_address=self.structural_address,
        )


class _ValidationFailure(RuntimeError):
    """검증 실패 정보."""

    def __init__(self, code: IssueCode, message: str) -> None:
        """안정적 문제 코드와 진단 메시지 저장."""

        super().__init__(message)
        self.code = code

    def event(self) -> FailureEvent:
        """안정적 경로 검증 실패 이벤트로 변환."""

        return FailureEvent(
            code=self.code,
            stage=_STAGE,
            message=str(self),
        )


def _canonical_document(document: str) -> bool:
    """문서 경로가 정규 UTF-8 상대 경로인지 판정."""

    try:
        document.encode("utf-8")
    except UnicodeEncodeError:
        return False

    if (
        not document
        or document.startswith("/")
        or "\\" in document
        or "\0" in document
        or unicodedata.normalize("NFC", document) != document
        or not document.endswith(".md")
    ):
        return False
    return all(part not in {"", ".", ".."} for part in document.split("/"))


def _allowed_path(path: str) -> bool:
    """경로가 번역 동기화 소유 범위인지 판정."""

    for pattern in _ALLOWED_PATHS:
        match = pattern.fullmatch(path)
        if match is None:
            continue
        document = match.groupdict().get("doc")
        return document is None or _canonical_document(document)
    return False


def unexpected_paths(paths: Iterable[str]) -> list[str]:
    """번역 동기화 소유 범위 밖의 경로를 정렬해 반환."""

    return sorted(path for path in set(paths) if not _allowed_path(path))


def _artifact_matches_key(
    artifact: object,
    *,
    version: str,
) -> bool:
    """검증 산출물이 문서 키의 최소 계약을 충족하는지 확인."""

    return bool(
        isinstance(artifact, VerifiedLocaleArtifact)
        and type(artifact.schema_version) is int
        and artifact.schema_version == 1
        and isinstance(artifact.locale_bytes, bytes)
        and artifact.version == version
        and isinstance(artifact.registry_sha256, str)
        and _SHA256_RE.fullmatch(artifact.registry_sha256)
        and isinstance(artifact.verification_input_sha256, str)
        and _SHA256_RE.fullmatch(artifact.verification_input_sha256)
    )


def _record_change(
    path: str,
    statuses: set[str],
    *,
    supported_versions: set[str],
    documents: dict[tuple[str, str], dict[str, set[str]]],
) -> _ChangeIssue | None:
    """단일 Git 변경을 검증하고 문서 로케일 상태에 반영.

    Args:
        path: 저장소 상대 변경 경로.
        statuses: 경로에서 관찰한 Git 상태 집합.
        supported_versions: 허용된 문서 버전.
        documents: 문서 키별 로케일 상태 누적 mapping.

    Returns:
        즉시 보고할 변경 문제. 문제가 없으면 ``None``.
    """

    version_match = _PATH_VERSION_RE.search(path)
    if version_match and version_match.group("version") not in supported_versions:
        return _ChangeIssue(
            IssueCode.SIDEBAR_INPUT_INVALID,
            f"unsupported translation version: {path}",
            version=version_match.group("version"),
        )
    if statuses not in ({"A"}, {"M"}, {"D"}):
        return _ChangeIssue(
            IssueCode.OUTPUT_STATE_MISMATCH,
            f"unsupported translation status: {path}",
        )
    if _SHARED_SIDEBAR_RE.fullmatch(path) and statuses == {"D"}:
        return _ChangeIssue(
            IssueCode.OUTPUT_STATE_MISMATCH,
            f"shared sidebar deletion is forbidden: {path}",
        )
    if _LOCALE_SIDEBAR_RE.fullmatch(path) and statuses != {"D"}:
        return _ChangeIssue(
            IssueCode.SIDEBAR_OVERRIDE_FORBIDDEN,
            f"locale sidebar override must only be deleted: {path}",
        )
    for locale, pattern in _DOCUMENT_PATHS:
        match = pattern.fullmatch(path)
        if match and _canonical_document(match.group("doc")):
            key = (match.group("version"), match.group("doc"))
            documents.setdefault(key, {})[locale] = statuses
            break
    return None


def _modified_document_issues(
    *,
    version: str,
    document: str,
    label: str,
    locale_statuses: Mapping[str, set[str]],
    proofs: Mapping[tuple[str, str, str], VerifiedLocaleArtifact],
) -> list[_ChangeIssue]:
    """수정된 영어 문서와 변경·검증된 번역문의 정합성 검사.

    Args:
        version: 문서 버전.
        document: 버전 루트 기준 문서 경로.
        label: 진단에 사용할 문서 식별자.
        locale_statuses: 로케일별 Git 상태.
        proofs: 변경되지 않은 로케일 검증 산출물.

    Returns:
        수정 문서의 상태와 증명 문제 목록.
    """

    issues: list[_ChangeIssue] = []
    if any(
        statuses != {"M"}
        for locale, statuses in locale_statuses.items()
        if locale != "en"
    ):
        issues.append(
            _ChangeIssue(
                IssueCode.OUTPUT_STATE_MISMATCH,
                f"inconsistent translation status: {label}",
                version=version,
                document=document,
            )
        )
    for locale in sorted({"en", "ko", "ja"} - set(locale_statuses)):
        artifact = proofs.get((version, document, locale))
        if not _artifact_matches_key(artifact, version=version):
            issues.append(
                _ChangeIssue(
                    IssueCode.UNVERIFIED_ENGLISH_ONLY_CHANGE,
                    f"unverified unchanged translation: {label} ({locale})",
                    version=version,
                    locale=locale,
                    document=document,
                )
            )
    return issues


def _document_change_issues(
    *,
    version: str,
    document: str,
    locale_statuses: Mapping[str, set[str]],
    proofs: Mapping[tuple[str, str, str], VerifiedLocaleArtifact],
) -> list[_ChangeIssue]:
    """단일 문서 키의 영어·한국어·일본어 변경 상태 검사.

    Args:
        version: 문서 버전.
        document: 버전 루트 기준 문서 경로.
        locale_statuses: 로케일별 Git 상태.
        proofs: 변경되지 않은 로케일 검증 산출물.

    Returns:
        문서 변경 상태 문제 목록.
    """

    label = f"version-{version}/{document}"
    if (
        document in UNTRANSLATED_DOCUMENTS
        and set(locale_statuses) == {"en"}
        and locale_statuses["en"] != {"D"}
    ):
        return []
    source_status = locale_statuses.get("en")
    if source_status is None:
        return [
            _ChangeIssue(
                IssueCode.OUTPUT_STATE_MISMATCH,
                f"unpaired translation document: {label}",
                version=version,
                document=document,
            )
        ]
    if source_status == {"M"}:
        return _modified_document_issues(
            version=version,
            document=document,
            label=label,
            locale_statuses=locale_statuses,
            proofs=proofs,
        )
    required_locales = {"en", "ko", "ja"}
    if set(locale_statuses) != required_locales:
        message = f"unpaired translation document: {label}"
    elif source_status not in ({"A"}, {"D"}) or any(
        statuses != source_status for statuses in locale_statuses.values()
    ):
        message = f"inconsistent translation status: {label}"
    else:
        return []
    return [
        _ChangeIssue(
            IssueCode.OUTPUT_STATE_MISMATCH,
            message,
            version=version,
            document=document,
        )
    ]


def _change_issues(
    changes: Mapping[str, set[str]],
    supported_versions: set[str],
    *,
    verified_unchanged: Mapping[tuple[str, str, str], VerifiedLocaleArtifact]
    | None = None,
) -> list[_ChangeIssue]:
    """버전·경로별 Git 상태와 영어·한국어·일본어 문서 세 파일의 정합성 검사."""

    issues: list[_ChangeIssue] = []
    proofs = verified_unchanged if isinstance(verified_unchanged, Mapping) else {}
    documents: dict[tuple[str, str], dict[str, set[str]]] = {}

    for path, statuses in sorted(changes.items()):
        issue = _record_change(
            path,
            statuses,
            supported_versions=supported_versions,
            documents=documents,
        )
        if issue is not None:
            issues.append(issue)

    for (version, doc), locale_statuses in sorted(documents.items()):
        issues.extend(
            _document_change_issues(
                version=version,
                document=doc,
                locale_statuses=locale_statuses,
                proofs=proofs,
            )
        )
    return issues


def validate_changes(
    changes: dict[str, set[str]],
    supported_versions: set[str],
    *,
    verified_unchanged: Mapping[tuple[str, str, str], VerifiedLocaleArtifact]
    | None = None,
) -> list[str]:
    """검증 산출물을 증거로 요구하는 읽기 쉬운 문제 목록 반환."""

    return [
        issue.message
        for issue in _change_issues(
            changes,
            supported_versions,
            verified_unchanged=verified_unchanged,
        )
    ]


def _verification_input(
    *,
    source_bytes: bytes,
    locale_bytes: bytes,
    version: str,
    registry: StaleLinkRegistry,
) -> document_verification.VerificationInput:
    """원문과 로케일 바이트로 최종 문서 검증 입력 구성."""

    source_text = source_bytes.decode("utf-8")
    preprocessed = preprocess.preprocess(source_text)
    annotation_source = postprocess.restore_placeholders(
        postprocess.replace_version(preprocessed.text, version),
        preprocessed.placeholders,
    )
    english_view = postprocess.postprocess(
        preprocessed.text,
        version,
        preprocessed.placeholders,
        registry=registry,
    )
    expected_map = document_verification.build_expected_annotation_map(
        annotation_source
    )
    return document_verification.create_verification_input(
        locale_document=locale_bytes,
        english_view=english_view,
        annotation_source=annotation_source,
        version=version,
        registry_sha256=registry.sha256,
        expected_annotation_map=expected_map,
    )


def _load_registry(path: Path) -> StaleLinkRegistry:
    """오래된 링크 레지스트리를 안정적 실패 코드로 로드."""

    try:
        return load_stale_link_registry(path)
    except StaleLinkRegistryError as exc:
        raise _ValidationFailure(
            IssueCode.STALE_LINK_REGISTRY_INVALID,
            "stale-link registry is invalid",
        ) from exc


def _read_source(path: Path) -> bytes:
    """검증 대상 영어 원문 바이트 읽기."""

    try:
        return path.read_bytes()
    except OSError as exc:
        raise _ValidationFailure(
            IssueCode.RUNNER_OPERATION_FAILED,
            "English verification source could not be read",
        ) from exc


def _read_optional_locale(path: Path) -> bytes | None:
    """로케일 문서가 존재할 때만 바이트 읽기."""

    try:
        return path.read_bytes()
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise _ValidationFailure(
            IssueCode.RUNNER_OPERATION_FAILED,
            "locale verification target could not be read",
        ) from exc


def _verified_artifact(
    *,
    source: Path,
    target: Path,
    version: str,
    registry_path: Path,
) -> VerifiedLocaleArtifact | None:
    """최종 스냅샷까지 일치하는 로케일 검증 산출물 생성."""

    start_registry = _load_registry(registry_path)
    source_bytes = _read_source(source)
    locale_bytes = _read_optional_locale(target)
    if locale_bytes is None:
        return None
    try:
        inputs = _verification_input(
            source_bytes=source_bytes,
            locale_bytes=locale_bytes,
            version=version,
            registry=start_registry,
        )
    except UnicodeError, ValueError:
        return None

    final_input: document_verification.VerificationInput | None = None
    final_locale_bytes: bytes | None = None
    end_registry: StaleLinkRegistry | None = None
    final_failure: _ValidationFailure | None = None

    def final_snapshot() -> tuple[
        document_verification.VerificationInput,
        StaleLinkRegistry,
    ]:
        """산출물 생성 직전 입력을 소유 경로에서 다시 읽기."""

        nonlocal final_input, final_locale_bytes, end_registry, final_failure
        try:
            end_registry = _load_registry(registry_path)
            final_source_bytes = _read_source(source)
            final_locale_bytes = _read_optional_locale(target)
            if final_locale_bytes is None:
                raise ValueError("locale verification target disappeared")
            final_input = _verification_input(
                source_bytes=final_source_bytes,
                locale_bytes=final_locale_bytes,
                version=version,
                registry=end_registry,
            )
            return final_input, end_registry
        except _ValidationFailure as exc:
            final_failure = exc
            raise

    try:
        result = document_verification.verify_document(
            inputs,
            registry_at_start=start_registry,
            final_snapshot=final_snapshot,
        )
    except _ValidationFailure:
        raise
    except Exception as exc:
        raise _ValidationFailure(
            IssueCode.RUNNER_OPERATION_FAILED,
            "final document verification could not be completed",
        ) from exc
    if final_failure is not None:
        raise final_failure
    artifact = result.artifact
    expected_hash = inputs.verification_input_sha256
    if (
        result.issues
        or not isinstance(artifact, VerifiedLocaleArtifact)
        or final_input is None
        or final_locale_bytes is None
        or end_registry is None
        or result.verification_input_sha256 != expected_hash
        or final_input.verification_input_sha256 != expected_hash
        or artifact.schema_version != 1
        or artifact.locale_bytes != final_locale_bytes
        or artifact.version != version
        or artifact.registry_sha256 != start_registry.sha256
        or artifact.verification_input_sha256 != expected_hash
    ):
        return None
    return artifact


def _verification_candidate_paths(
    changes: Mapping[str, set[str]],
) -> set[str]:
    """영어 수정과 함께 검증할 변경 목록 밖의 로케일 경로 계산."""

    paths: set[str] = set()
    source_pattern = _DOCUMENT_PATHS[0][1]
    for source_path, statuses in changes.items():
        match = source_pattern.fullmatch(source_path)
        if match is None or statuses != {"M"}:
            continue
        paths.add(source_path)
        version = match.group("version")
        doc = match.group("doc")
        for template in _UNCHANGED_LOCALE_PATHS.values():
            target_path = template.format(version=version, doc=doc)
            if target_path not in changes:
                paths.add(target_path)
    return paths


def _verified_locales_for_document(
    *,
    source_path: str,
    version: str,
    document: str,
    changes: Mapping[str, set[str]],
    repo_root: Path,
    registry_path: Path,
) -> dict[tuple[str, str, str], VerifiedLocaleArtifact]:
    """변경되지 않은 단일 문서 로케일의 최종 상태 증명.

    Args:
        source_path: 영어 원문 저장소 상대 경로.
        version: 문서 버전.
        document: 버전 루트 기준 문서 경로.
        changes: 전체 변경 경로와 상태.
        repo_root: 저장소 루트.
        registry_path: 오래된 링크 레지스트리 경로.

    Returns:
        검증에 성공한 로케일별 산출물 mapping.
    """

    verified: dict[tuple[str, str, str], VerifiedLocaleArtifact] = {}
    source = repo_root / source_path
    for locale, template in sorted(_UNCHANGED_LOCALE_PATHS.items()):
        target_path = template.format(version=version, doc=document)
        if target_path in changes:
            continue
        if unsafe_output_paths({source_path, target_path}, repo_root):
            continue
        artifact = _verified_artifact(
            source=source,
            target=repo_root / target_path,
            version=version,
            registry_path=registry_path,
        )
        if artifact is not None:
            verified[(version, document, locale)] = artifact
    return verified


def verified_unchanged_locales(
    changes: dict[str, set[str]],
    repo_root: Path = REPO_ROOT,
    *,
    registry_path: Path | None = None,
) -> dict[tuple[str, str, str], VerifiedLocaleArtifact]:
    """최종 문서 검증기만 사용해 변경되지 않은 로케일 파일 증명."""

    verified: dict[tuple[str, str, str], VerifiedLocaleArtifact] = {}
    source_pattern = _DOCUMENT_PATHS[0][1]
    effective_registry_path = (
        registry_path
        if registry_path is not None
        else repo_root / "translation-sync/stale-links.json"
    )
    for source_path, statuses in sorted(changes.items()):
        match = source_pattern.fullmatch(source_path)
        if match is None or statuses != {"M"}:
            continue
        version = match.group("version")
        doc = match.group("doc")
        verified.update(
            _verified_locales_for_document(
                source_path=source_path,
                version=version,
                document=doc,
                changes=changes,
                repo_root=repo_root,
                registry_path=effective_registry_path,
            )
        )
    return verified


def _decode_name_status_entry(
    fields: list[bytes],
    index: int,
) -> tuple[tuple[tuple[str, str], ...], int]:
    """Git 이름·상태 필드 한 항목을 정규 A/M/D 항목으로 변환.

    Args:
        fields: NUL 구분을 제거한 전체 출력 필드.
        index: 상태 필드 위치.

    Returns:
        변환한 경로 상태 항목과 다음 상태 필드 위치.
    """

    try:
        status = fields[index].decode("ascii")
    except UnicodeDecodeError as error:
        raise RuntimeError(_INVALID_NAME_STATUS) from error
    if not _NAME_STATUS_RE.fullmatch(status):
        raise RuntimeError(_INVALID_NAME_STATUS)
    path_count = 2 if status[0] in {"C", "R"} else 1
    next_index = index + 1 + path_count
    if next_index > len(fields):
        raise RuntimeError(_INVALID_NAME_STATUS)
    paths = [
        field.decode("utf-8", errors="surrogateescape")
        for field in fields[index + 1 : next_index]
    ]
    if any(not _canonical_repository_path(path) for path in paths):
        raise RuntimeError(_INVALID_NAME_STATUS)
    if status.startswith("R"):
        entries = (("D", paths[0]), ("A", paths[1]))
    elif status.startswith("C"):
        entries = (("A", paths[1]),)
    else:
        entries = ((status, paths[0]),)
    return entries, next_index


def _parse_name_status(output: bytes) -> list[tuple[str, str]]:
    """NUL로 구분된 Git 이름·상태 바이트를 정규 A/M/D 항목으로 변환."""

    if not output:
        return []
    if not output.endswith(b"\0"):
        raise RuntimeError(_INVALID_NAME_STATUS)

    fields = output[:-1].split(b"\0")
    entries: list[tuple[str, str]] = []
    index = 0
    while index < len(fields):
        parsed, index = _decode_name_status_entry(fields, index)
        entries.extend(parsed)
    return entries


def _parse_untracked(output: bytes) -> list[str]:
    """NUL로 구분된 Git 미추적 경로 바이트 파싱."""

    if not output:
        return []
    if not output.endswith(b"\0"):
        raise RuntimeError("invalid git untracked output")
    paths = [
        field.decode("utf-8", errors="surrogateescape")
        for field in output[:-1].split(b"\0")
    ]
    if any(not _canonical_repository_path(path) for path in paths):
        raise RuntimeError("invalid git untracked output")
    return paths


def _canonical_repository_path(path: str) -> bool:
    """Git 경로가 정규 UTF-8 저장소 상대 경로인지 판정."""

    try:
        path.encode("utf-8")
    except UnicodeEncodeError:
        return False

    return bool(
        path
        and not path.startswith("/")
        and "\\" not in path
        and "\0" not in path
        and unicodedata.normalize("NFC", path) == path
        and all(part not in {"", ".", ".."} for part in path.split("/"))
    )


def _git_environment(environment: Mapping[str, str]) -> dict[str, str]:
    """자격 증명과 사용자 설정을 제외한 Git 환경 구성."""

    sanitized = {
        key: value
        for key, value in environment.items()
        if key in _GIT_PASSTHROUGH_ENV or key.startswith("LC_")
    }
    sanitized.setdefault("PATH", os.defpath)
    sanitized.update(
        {
            "HOME": os.devnull,
            "XDG_CONFIG_HOME": os.devnull,
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_PAGER": "",
        }
    )
    return sanitized


def _remaining_timeout(
    deadline: float | None,
    *,
    clock: Callable[[], float],
) -> float | None:
    """공통 워크플로 기한까지 남은 제한 시간 계산."""

    if deadline is None:
        return None
    remaining = deadline - clock()
    if remaining <= 0:
        raise _ValidationFailure(
            IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            "workflow deadline exceeded during path validation",
        )
    return remaining


def _run_git(
    arguments: Sequence[str],
    *,
    repo_root: Path,
    process_runner: ProcessRunner,
    environment: Mapping[str, str],
    workflow_deadline: float | None,
    clock: Callable[[], float],
) -> bytes:
    """격리 환경과 공통 기한을 적용해 Git 검사 실행."""

    command = [*_GIT_PREFIX, *arguments]
    timeout = _remaining_timeout(workflow_deadline, clock=clock)
    try:
        completed = process_runner(
            command,
            cwd=repo_root,
            env=_git_environment(environment),
            check=False,
            capture_output=True,
            timeout=timeout,
            stdin=subprocess.DEVNULL,
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise _ValidationFailure(
            IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            "workflow deadline exceeded during Git path inspection",
        ) from exc
    except (OSError, ProcessTreeError, subprocess.SubprocessError) as exc:
        raise _ValidationFailure(
            IssueCode.RUNNER_OPERATION_FAILED,
            "Git path inspection could not be executed",
        ) from exc
    if not isinstance(completed, subprocess.CompletedProcess):
        raise _ValidationFailure(
            IssueCode.RUNNER_OPERATION_FAILED,
            "Git path inspection returned an invalid result",
        )
    if completed.returncode != 0 or not isinstance(completed.stdout, bytes):
        raise _ValidationFailure(
            IssueCode.RUNNER_OPERATION_FAILED,
            "Git path inspection failed",
        )
    return completed.stdout


def changed_entries(
    repo_root: Path = REPO_ROOT,
    *,
    process_runner: ProcessRunner | None = None,
    workflow_deadline: float | None = None,
    clock: Callable[[], float] = time.monotonic,
    environment: Mapping[str, str] | None = None,
) -> dict[str, set[str]]:
    """스테이징·비 스테이징·미추적 변경을 경로별 Git 상태로 수집."""

    runner = run_process_tree if process_runner is None else process_runner
    source_environment = os.environ if environment is None else environment
    commands = (
        (
            "diff",
            "--no-ext-diff",
            "--no-textconv",
            "--name-status",
            "--no-renames",
            "-z",
        ),
        (
            "diff",
            "--cached",
            "--no-ext-diff",
            "--no-textconv",
            "--name-status",
            "--no-renames",
            "-z",
        ),
    )
    changes: dict[str, set[str]] = {}
    try:
        for command in commands:
            output = _run_git(
                command,
                repo_root=repo_root,
                process_runner=runner,
                environment=source_environment,
                workflow_deadline=workflow_deadline,
                clock=clock,
            )
            for status, path in _parse_name_status(output):
                changes.setdefault(path, set()).add(status)

        output = _run_git(
            ("ls-files", "--others", "--exclude-standard", "-z"),
            repo_root=repo_root,
            process_runner=runner,
            environment=source_environment,
            workflow_deadline=workflow_deadline,
            clock=clock,
        )
        for path in _parse_untracked(output):
            changes.setdefault(path, set()).add("A")
    except _ValidationFailure:
        raise
    except (RuntimeError, UnicodeError) as exc:
        raise _ValidationFailure(
            IssueCode.RUNNER_OPERATION_FAILED,
            "Git path inspection returned malformed output",
        ) from exc
    return changes


def changed_paths(repo_root: Path = REPO_ROOT) -> set[str]:
    """저장소의 전체 변경 경로 수집."""

    return set(changed_entries(repo_root))


def unsafe_output_paths(paths: Iterable[str], repo_root: Path = REPO_ROOT) -> list[str]:
    """심볼릭 링크를 통과하거나 일반 파일이 아닌 대상으로 끝나는 출력 경로 반환."""

    unsafe: list[str] = []
    for path in set(paths):
        candidate = repo_root
        mode: int | None = None
        for part in Path(path).parts:
            candidate /= part
            try:
                mode = candidate.lstat().st_mode
            except FileNotFoundError:
                mode = None
                break
            if stat.S_ISLNK(mode):
                unsafe.append(path)
                break
        else:
            if mode is None or not stat.S_ISREG(mode):
                unsafe.append(path)
    return sorted(unsafe)


def existing_sidebar_overrides(repo_root: Path = REPO_ROOT) -> list[str]:
    """후보에 남은 로케일별 사이드바 재정의 경로 수집."""

    paths: list[str] = []
    for locale in ("ko", "ja"):
        for path in repo_root.glob(_SIDEBAR_OVERRIDE_GLOB.format(locale=locale)):
            paths.append(str(path.relative_to(repo_root)))
    return sorted(paths)


def _deadline_from_environment(environment: Mapping[str, str]) -> float | None:
    """환경 변수에서 공통 단조 시계 기한 파싱."""

    raw = environment.get(WORKFLOW_DEADLINE_ENV)
    if raw is None:
        return None
    try:
        deadline = float(raw)
    except (TypeError, ValueError) as exc:
        raise _ValidationFailure(
            IssueCode.RUNNER_OPERATION_FAILED,
            "workflow deadline is invalid",
        ) from exc
    if not math.isfinite(deadline) or deadline <= 0:
        raise _ValidationFailure(
            IssueCode.RUNNER_OPERATION_FAILED,
            "workflow deadline is invalid",
        )
    return deadline


def _path_issue(code: IssueCode, message: str) -> FailureEvent:
    """경로 검증 단계의 안정적 실패 이벤트 구성."""

    return FailureEvent(code=code, stage=_STAGE, message=message)


def _finish_failures(
    failures: Sequence[FailureEvent],
    *,
    environment: Mapping[str, str],
) -> int:
    """실패 진단과 선택적 정규 보고서를 기록한 뒤 종료 코드 계산."""

    for failure in failures:
        print(f"{failure.code.value}: {failure.message}", file=sys.stderr)

    report_value = environment.get(FAILURE_REPORT_ENV, "").strip()
    run_id = environment.get(RUN_ID_ENV, "").strip()
    if not report_value and not run_id:
        return int(final_exit_code(failures))
    if not report_value or not run_id:
        print(
            "REPORT_WRITE_FAILED: path validation failure report configuration "
            "is incomplete",
            file=sys.stderr,
        )
        return int(ExitCode.INFRASTRUCTURE_FAILURE)
    try:
        report = FailureReport.build(run_id=run_id, failures=failures)
    except TypeError, ValueError:
        print(
            "REPORT_WRITE_FAILED: path validation failure report could not be built",
            file=sys.stderr,
        )
        return int(ExitCode.INFRASTRUCTURE_FAILURE)
    if (
        write_failure_report_exact(
            report,
            target=Path(report_value),
            stderr=sys.stderr,
        )
        is None
    ):
        return int(ExitCode.INFRASTRUCTURE_FAILURE)
    return int(final_exit_code(failures))


def main(
    *,
    repo_root: Path | None = None,
    process_runner: ProcessRunner | None = None,
    environment: Mapping[str, str] | None = None,
    clock: Callable[[], float] = time.monotonic,
) -> int:
    """명령줄 진입점 실행."""

    root = REPO_ROOT if repo_root is None else repo_root
    runtime_environment = os.environ if environment is None else environment
    try:
        workflow_deadline = _deadline_from_environment(runtime_environment)
        changes = changed_entries(
            root,
            process_runner=process_runner,
            workflow_deadline=workflow_deadline,
            clock=clock,
            environment=runtime_environment,
        )
    except _ValidationFailure as exc:
        return _finish_failures([exc.event()], environment=runtime_environment)

    paths = set(changes)
    failures: list[FailureEvent] = []
    for path in unexpected_paths(paths):
        failures.append(
            _path_issue(
                IssueCode.OUTPUT_PATH_FORBIDDEN,
                f"unexpected translation sync output path: {path}",
            )
        )

    verification_paths = paths | _verification_candidate_paths(changes)
    try:
        unsafe = unsafe_output_paths(verification_paths, root)
    except OSError:
        failures.append(
            _path_issue(
                IssueCode.RUNNER_OPERATION_FAILED,
                "translation output paths could not be inspected",
            )
        )
        unsafe = []
    for path in unsafe:
        failures.append(
            _path_issue(
                IssueCode.OUTPUT_PATH_FORBIDDEN,
                f"unsafe translation sync output path: {path}",
            )
        )

    try:
        overrides = existing_sidebar_overrides(root)
    except OSError:
        failures.append(
            _path_issue(
                IssueCode.RUNNER_OPERATION_FAILED,
                "locale sidebar overrides could not be inspected",
            )
        )
        overrides = []
    for path in overrides:
        failures.append(
            _path_issue(
                IssueCode.SIDEBAR_OVERRIDE_FORBIDDEN,
                f"locale sidebar override must be deleted: {path}",
            )
        )

    try:
        supported_versions = set(load_versions(root / "versions.json"))
    except (OSError, ValueError) as exc:
        failures.append(
            _path_issue(
                IssueCode.SIDEBAR_INPUT_INVALID,
                f"invalid versions.json: {exc}",
            )
        )
        supported_versions = None

    if supported_versions is not None:
        try:
            proofs = verified_unchanged_locales(changes, root)
        except _ValidationFailure as exc:
            failures.append(exc.event())
            proofs = {}
        except OSError:
            failures.append(
                _path_issue(
                    IssueCode.RUNNER_OPERATION_FAILED,
                    "locale verification inputs could not be inspected",
                )
            )
            proofs = {}
        failures.extend(
            issue.event()
            for issue in _change_issues(
                changes,
                supported_versions,
                verified_unchanged=proofs,
            )
        )

    if failures:
        return _finish_failures(failures, environment=runtime_environment)
    print(f"translation sync output paths verified: {len(paths)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
