"""봉인된 candidate tree의 생성과 compare-and-swap publication."""

from __future__ import annotations

import hashlib
import hmac
import json
import math
import os
import re
import subprocess
import tempfile
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .failure import IssueCode
from .process import ProcessTreeError, run_process_tree


_INVALID_REF_CHARACTERS = frozenset(" ~^:?*[\\")
_SCP_ENDPOINT_RE = re.compile(r"(?:[^/@:\s]+@)?[^/:\s]+:.+\Z")
_DANGEROUS_GIT_ENV_KEYS = frozenset(
    {
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "GIT_COMMON_DIR",
        "GIT_CONFIG",
        "GIT_CONFIG_COUNT",
        "GIT_CONFIG_PARAMETERS",
        "GIT_DIR",
        "GIT_OBJECT_DIRECTORY",
        "GIT_TEMPLATE_DIR",
        "GIT_WORK_TREE",
    }
)
_PREPARE_CREDENTIAL_KEY_RE = re.compile(
    r"(?:^|_)(?:AUTH|AUTHORIZATION|CREDENTIALS?|PASSWORD|SECRET|TOKEN|"
    r"API_KEY|ACCESS_KEY|SSH_AUTH_SOCK|ASKPASS)(?:_|$)",
    re.IGNORECASE,
)


def _is_oid(value: object) -> bool:
    """정규화된 Git SHA-1 또는 SHA-256 객체 ID 판별."""

    return (
        isinstance(value, str)
        and len(value) in {40, 64}
        and value == value.lower()
        and all(character in "0123456789abcdef" for character in value)
    )


def _is_branch_ref(value: object) -> bool:
    """완전한 로컬 브랜치 ref 형식 판별."""

    if not isinstance(value, str) or not value.startswith("refs/heads/"):
        return False
    branch = value.removeprefix("refs/heads/")
    components = branch.split("/")
    return bool(branch) and not (
        any(not component or component.startswith(".") for component in components)
        or any(component.endswith(".lock") for component in components)
        or branch.endswith(".")
        or ".." in branch
        or "@{" in branch
        or any(character in _INVALID_REF_CHARACTERS for character in branch)
        or any(ord(character) < 32 or ord(character) == 127 for character in branch)
    )


def _validate_push_endpoint(value: str) -> str:
    """push endpoint 검증."""

    if (
        not isinstance(value, str)
        or not value
        or value.startswith("-")
        or "\0" in value
        or any(character.isspace() for character in value)
    ):
        raise ValueError("push_endpoint must be a trusted explicit URL or path")
    if Path(value).is_absolute():
        return value
    if "://" in value:
        parsed = urlsplit(value)
        if (
            not parsed.scheme
            or (parsed.scheme != "file" and not parsed.netloc)
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("push_endpoint must be a trusted explicit URL or path")
        if parsed.password is not None:
            raise ValueError("push_endpoint must not contain credentials")
        if parsed.scheme.lower() in {"http", "https"} and parsed.username is not None:
            raise ValueError("push_endpoint must not contain credentials")
        return value
    if _SCP_ENDPOINT_RE.fullmatch(value):
        return value
    raise ValueError("push_endpoint must be a trusted explicit URL or path")


def _validated_environment(values: Mapping[str, str]) -> dict[str, str]:
    """위험한 Git 설정을 제거한 하위 프로세스 환경 구성."""

    if not isinstance(values, Mapping):
        raise TypeError("Git environment must be a mapping")
    environment: dict[str, str] = {}
    for key, value in values.items():
        if (
            not isinstance(key, str)
            or not isinstance(value, str)
            or not key
            or "=" in key
            or "\0" in key
            or "\0" in value
        ):
            raise ValueError("Git environment contains an invalid entry")
        if key in _DANGEROUS_GIT_ENV_KEYS or key.startswith("GIT_CONFIG_KEY_"):
            continue
        if key.startswith("GIT_CONFIG_VALUE_"):
            continue
        environment[key] = value
    if not environment.get("PATH"):
        raise ValueError("Git environment must include PATH")
    environment.update(
        {
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_TERMINAL_PROMPT": "0",
        }
    )
    return environment


@dataclass(frozen=True, slots=True)
class PublicationBase:
    """candidate 생성 시작 전에 고정된 값."""

    head: str
    tree: str
    remote_ref: str
    active_fingerprint: str

    def __post_init__(self) -> None:
        """publication 기준본 식별자 검증."""

        if not _is_oid(self.head):
            raise ValueError("head must be a full canonical Git object ID")
        if not _is_oid(self.tree):
            raise ValueError("tree must be a full canonical Git object ID")
        if not _is_branch_ref(self.remote_ref):
            raise ValueError("remote_ref must be a full refs/heads branch ref")
        if (
            not isinstance(self.active_fingerprint, str)
            or not self.active_fingerprint
            or "\0" in self.active_fingerprint
        ):
            raise ValueError("active_fingerprint must be a non-empty string")


@dataclass(frozen=True, slots=True)
class PreparedPublication:
    """후속 publication process를 위한 직렬화 가능한 detached commit 증거."""

    base_head: str
    base_tree: str
    remote_ref: str
    verified_tree: str
    commit_oid: str | None
    seal: str

    def __post_init__(self) -> None:
        """준비된 publication 증거의 구조와 식별자 검증."""

        if not _is_oid(self.base_head) or not _is_oid(self.base_tree):
            raise ValueError("prepared base identifiers must be canonical Git OIDs")
        if not _is_branch_ref(self.remote_ref) or not _is_oid(self.verified_tree):
            raise ValueError("prepared publication identifiers are invalid")
        if self.commit_oid is None:
            if self.verified_tree != self.base_tree:
                raise ValueError("changed verified tree requires a commit")
        elif not _is_oid(self.commit_oid) or self.verified_tree == self.base_tree:
            raise ValueError("publication commit does not describe a changed tree")
        if (
            len(self.seal) != 64
            or self.seal != self.seal.lower()
            or any(character not in "0123456789abcdef" for character in self.seal)
        ):
            raise ValueError("prepared publication seal is invalid")

    def to_mapping(self) -> dict[str, str | None]:
        """직렬화 가능한 publication 증거 mapping 반환."""

        return {
            "base_head": self.base_head,
            "base_tree": self.base_tree,
            "remote_ref": self.remote_ref,
            "verified_tree": self.verified_tree,
            "commit_oid": self.commit_oid,
            "seal": self.seal,
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> PreparedPublication:
        """엄격한 schema의 mapping에서 publication 증거 복원."""

        expected = {
            "base_head",
            "base_tree",
            "remote_ref",
            "verified_tree",
            "commit_oid",
            "seal",
        }
        if not isinstance(value, Mapping) or set(value) != expected:
            raise ValueError("prepared publication mapping has an invalid schema")
        fields = {key: value[key] for key in expected}
        if any(
            not isinstance(field, str)
            for key, field in fields.items()
            if key != "commit_oid"
        ) or not isinstance(fields["commit_oid"], (str, type(None))):
            raise ValueError("prepared publication mapping has invalid field types")
        return cls(**fields)  # type: ignore[arg-type]


@dataclass(frozen=True, slots=True)
class PublicationResult:
    """원격 반영 여부와 최종 commit 식별자."""

    published_oid: str
    commit_oid: str | None
    pushed: bool


@dataclass(slots=True)
class _CleanupState:
    """임시 저장소 정리 시 보존할 publication 상태."""

    published_commit: str | None = None


class PublicationError(RuntimeError):
    """이미 publication된 커밋 식별자를 선택적으로 포함한 비식별 실패."""

    def __init__(
        self,
        code: IssueCode,
        *,
        published_commit: str | None = None,
    ) -> None:
        """안정된 문제 코드와 이미 반영된 commit 식별자 저장."""

        if published_commit is not None and not _is_oid(published_commit):
            raise ValueError("published_commit must be a canonical Git OID")
        self.code = code
        self.published_commit = published_commit
        super().__init__(code.value)


def build_cas_push_argv(
    *,
    push_endpoint: str,
    remote_ref: str,
    base_head: str,
    commit_oid: str,
) -> tuple[str, ...]:
    """정확한 compare-and-swap lease로 보호된 단일 ref push argv 생성."""

    endpoint = _validate_push_endpoint(push_endpoint)
    if not _is_branch_ref(remote_ref):
        raise ValueError("remote_ref must be a full refs/heads branch ref")
    if not _is_oid(base_head) or not _is_oid(commit_oid):
        raise ValueError("base_head and commit_oid must be full canonical Git OIDs")
    return (
        "git",
        "push",
        "--no-verify",
        "--no-follow-tags",
        f"--force-with-lease={remote_ref}:{base_head}",
        endpoint,
        f"{commit_oid}:{remote_ref}",
    )


class Publisher:
    """credential 없이 준비한 뒤 격리 Git 설정을 통한 publication.

    ``PreparedPublication``은 scalar 식별자만 포함하며 process 경계 통과 가능.
    ``publish``는 해당 scalar만 신뢰하지 않고 신규 shared bare 저장소를 열어 commit,
    tree 및 단일 parent를 다시 해석하며 호출자가 고정한 명시적 endpoint를 ref 읽기와
    push에 모두 사용. 호출자는 credential 없는 준비 환경과 credential 포함 push
    환경을 분리해 제공하며 두 환경 모두 예외에 렌더링하지 않음.
    """

    def __init__(
        self,
        *,
        candidate_repo: Path,
        push_endpoint: str,
        base: PublicationBase,
        read_active_fingerprint: Callable[[float], str],
        remaining_seconds: Callable[[], float],
        prepare_environment: Mapping[str, str],
        preparation_key: bytes,
    ) -> None:
        """격리 저장소와 publication 고정 입력 검증·저장."""

        if not isinstance(candidate_repo, Path):
            raise TypeError("candidate_repo must be a Path")
        candidate_repo = candidate_repo.resolve()
        if not candidate_repo.is_dir():
            raise ValueError("candidate_repo must be an existing directory")
        if not callable(read_active_fingerprint) or not callable(remaining_seconds):
            raise TypeError("publication state readers must be callable")
        if not isinstance(preparation_key, bytes) or len(preparation_key) < 32:
            raise ValueError("preparation_key must contain at least 256 bits")
        prepare_environment = _validated_environment(prepare_environment)
        if any(_PREPARE_CREDENTIAL_KEY_RE.search(key) for key in prepare_environment):
            raise ValueError("prepare_environment must not contain credentials")
        self._candidate_repo = candidate_repo
        self._push_endpoint = _validate_push_endpoint(push_endpoint)
        self._base = base
        self._read_active_fingerprint = read_active_fingerprint
        self._remaining_seconds = remaining_seconds
        self._prepare_environment = prepare_environment
        self._preparation_key = bytes(preparation_key)

    def prepare(
        self,
        *,
        verified_tree: str,
        commit_message: str,
    ) -> PreparedPublication:
        """parent와 tree가 모두 고정된 참조 없는 커밋 생성."""

        if not _is_oid(verified_tree):
            raise ValueError("verified_tree must be a full canonical Git object ID")
        if (
            not isinstance(commit_message, str)
            or not commit_message.strip()
            or "\0" in commit_message
        ):
            raise ValueError("commit_message must be a non-empty string")

        self._validate_candidate_base()
        resolved_verified_tree = self._tree_oid(
            self._candidate_repo,
            verified_tree,
            environment=self._prepare_environment,
        )
        if resolved_verified_tree != verified_tree:
            raise PublicationError(IssueCode.VERIFIED_TREE_MISMATCH)
        if verified_tree == self._base.tree:
            return self._prepared(verified_tree=verified_tree, commit_oid=None)

        commit_oid = self._git_oid(
            self._candidate_repo,
            "-c",
            "commit.gpgSign=false",
            "commit-tree",
            verified_tree,
            "-p",
            self._base.head,
            input_bytes=(commit_message.rstrip() + "\n").encode("utf-8"),
            environment=self._prepare_environment,
            failure_code=IssueCode.RUNNER_OPERATION_FAILED,
        )
        self._validate_commit(
            self._candidate_repo,
            commit_oid=commit_oid,
            verified_tree=verified_tree,
            environment=self._prepare_environment,
        )
        return self._prepared(verified_tree=verified_tree, commit_oid=commit_oid)

    def publish(
        self,
        prepared: PreparedPublication,
        *,
        push_environment: Mapping[str, str],
    ) -> PublicationResult:
        """직렬화된 증거 재검증과 유일한 원격 변경 수행."""

        self._validate_prepared_scalars(prepared)
        environment = _validated_environment(push_environment)
        with self._temporary_push_root() as (temporary_root, cleanup_state):
            push_repo = self._isolated_push_repo(temporary_root)
            self._validate_base(
                push_repo,
                environment=self._prepare_environment,
            )
            if prepared.commit_oid is not None:
                self._validate_commit(
                    push_repo,
                    commit_oid=prepared.commit_oid,
                    verified_tree=prepared.verified_tree,
                    environment=self._prepare_environment,
                )

            self._remaining_timeout()
            remote_oid = self._remote_oid(push_repo, environment)
            active_fingerprint = self._read_fingerprint()
            self._remaining_timeout()
            if (
                remote_oid != self._base.head
                or active_fingerprint != self._base.active_fingerprint
            ):
                raise PublicationError(IssueCode.PUBLICATION_BASE_CHANGED)
            if prepared.commit_oid is None:
                return PublicationResult(
                    published_oid=self._base.head,
                    commit_oid=None,
                    pushed=False,
                )

            argv = build_cas_push_argv(
                push_endpoint=self._push_endpoint,
                remote_ref=self._base.remote_ref,
                base_head=self._base.head,
                commit_oid=prepared.commit_oid,
            )
            push_timeout = self._remaining_timeout() / 2
            try:
                completed = run_process_tree(
                    argv,
                    cwd=push_repo,
                    env=environment,
                    check=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=False,
                    timeout=push_timeout,
                )
            except subprocess.TimeoutExpired:
                return self._reconcile_failed_push(
                    push_repo,
                    prepared.commit_oid,
                    environment,
                    IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
                )
            except ProcessTreeError:
                return self._reconcile_failed_push(
                    push_repo,
                    prepared.commit_oid,
                    environment,
                    IssueCode.RUNNER_OPERATION_FAILED,
                )
            except OSError:
                raise PublicationError(IssueCode.RUNNER_OPERATION_FAILED) from None

            if completed.returncode != 0:
                return self._reconcile_failed_push(
                    push_repo,
                    prepared.commit_oid,
                    environment,
                    IssueCode.RUNNER_OPERATION_FAILED,
                )
            try:
                observed = self._remote_oid(push_repo, environment)
            except PublicationError as exc:
                raise PublicationError(
                    exc.code,
                    published_commit=prepared.commit_oid,
                ) from None
            if observed == prepared.commit_oid:
                cleanup_state.published_commit = prepared.commit_oid
                return PublicationResult(
                    published_oid=prepared.commit_oid,
                    commit_oid=prepared.commit_oid,
                    pushed=True,
                )
            raise PublicationError(
                IssueCode.PUBLICATION_BASE_CHANGED,
                published_commit=prepared.commit_oid,
            )

    @contextmanager
    def _temporary_push_root(self) -> Iterator[tuple[Path, _CleanupState]]:
        """push 전용 임시 저장소 수명과 정리 실패 문맥 관리."""

        try:
            temporary = tempfile.TemporaryDirectory(
                prefix="translation-sync-publish-",
            )
        except OSError:
            raise PublicationError(IssueCode.RUNNER_OPERATION_FAILED) from None
        state = _CleanupState()

        try:
            yield Path(temporary.name), state
        except PublicationError as exc:
            state.published_commit = exc.published_commit
            try:
                temporary.cleanup()
            except OSError:
                raise PublicationError(
                    IssueCode.RUNNER_OPERATION_FAILED,
                    published_commit=state.published_commit,
                ) from None
            raise
        except Exception:
            try:
                temporary.cleanup()
            except OSError:
                raise PublicationError(
                    IssueCode.RUNNER_OPERATION_FAILED,
                    published_commit=state.published_commit,
                ) from None
            raise
        else:
            try:
                temporary.cleanup()
            except OSError:
                raise PublicationError(
                    IssueCode.RUNNER_OPERATION_FAILED,
                    published_commit=state.published_commit,
                ) from None

    def _reconcile_failed_push(
        self,
        push_repo: Path,
        commit_oid: str,
        environment: Mapping[str, str],
        failure_code: IssueCode,
    ) -> PublicationResult:
        """실패하거나 불확실한 push 뒤 원격 ref 상태 재확인."""

        try:
            observed = self._remote_oid(push_repo, environment)
        except PublicationError as exc:
            if exc.code is IssueCode.WORKFLOW_DEADLINE_EXCEEDED:
                raise
            raise PublicationError(failure_code) from None
        if observed == commit_oid:
            raise PublicationError(
                failure_code,
                published_commit=commit_oid,
            )
        if observed != self._base.head:
            raise PublicationError(IssueCode.PUBLICATION_BASE_CHANGED)
        raise PublicationError(failure_code)

    def _validate_prepared_scalars(self, prepared: PreparedPublication) -> None:
        """직렬화된 증거가 현재 기준본과 seal에 맞는지 검증."""

        if not isinstance(prepared, PreparedPublication):
            raise TypeError("prepared must be a PreparedPublication")
        if (
            prepared.base_head != self._base.head
            or prepared.base_tree != self._base.tree
            or prepared.remote_ref != self._base.remote_ref
        ):
            raise PublicationError(IssueCode.PUBLICATION_BASE_CHANGED)
        expected_seal = self._seal(
            base_head=prepared.base_head,
            base_tree=prepared.base_tree,
            remote_ref=prepared.remote_ref,
            verified_tree=prepared.verified_tree,
            commit_oid=prepared.commit_oid,
        )
        if not hmac.compare_digest(prepared.seal, expected_seal):
            raise PublicationError(IssueCode.VERIFIED_TREE_MISMATCH)

    def _prepared(
        self,
        *,
        verified_tree: str,
        commit_oid: str | None,
    ) -> PreparedPublication:
        """현재 기준본에 결합된 봉인 publication 증거 생성."""

        fields = {
            "base_head": self._base.head,
            "base_tree": self._base.tree,
            "remote_ref": self._base.remote_ref,
            "verified_tree": verified_tree,
            "commit_oid": commit_oid,
        }
        return PreparedPublication(
            **fields,
            seal=self._seal(**fields),
        )

    def _seal(
        self,
        *,
        base_head: str,
        base_tree: str,
        remote_ref: str,
        verified_tree: str,
        commit_oid: str | None,
    ) -> str:
        """봉인."""

        payload = json.dumps(
            {
                "base_head": base_head,
                "base_tree": base_tree,
                "commit_oid": commit_oid,
                "remote_ref": remote_ref,
                "verified_tree": verified_tree,
            },
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("ascii")
        return hmac.new(self._preparation_key, payload, hashlib.sha256).hexdigest()

    def _validate_candidate_base(self) -> None:
        """candidate가 승인 기준 commit과 tree를 포함하는지 검증."""

        self._validate_base(
            self._candidate_repo,
            environment=self._prepare_environment,
        )

    def _validate_base(
        self,
        repo: Path,
        *,
        environment: Mapping[str, str],
    ) -> None:
        """저장소의 승인 기준 commit과 tree 식별자 검증."""

        resolved_base = self._git_oid(
            repo,
            "rev-parse",
            "--verify",
            f"{self._base.head}^{{commit}}",
            environment=environment,
            failure_code=IssueCode.PUBLICATION_BASE_CHANGED,
        )
        actual_tree = self._tree_oid(
            repo,
            self._base.head,
            environment=environment,
        )
        if resolved_base != self._base.head or actual_tree != self._base.tree:
            raise PublicationError(IssueCode.PUBLICATION_BASE_CHANGED)

    def _validate_commit(
        self,
        repo: Path,
        *,
        commit_oid: str,
        verified_tree: str,
        environment: Mapping[str, str],
    ) -> None:
        """publication commit의 tree와 단일 parent 검증."""

        resolved = self._git_oid(
            repo,
            "rev-parse",
            "--verify",
            f"{commit_oid}^{{commit}}",
            environment=environment,
            failure_code=IssueCode.VERIFIED_TREE_MISMATCH,
        )
        committed_tree = self._tree_oid(
            repo,
            commit_oid,
            environment=environment,
        )
        parents = self._git_output(
            repo,
            "show",
            "-s",
            "--format=%P",
            commit_oid,
            environment=environment,
            failure_code=IssueCode.VERIFIED_TREE_MISMATCH,
        ).split()
        if (
            resolved != commit_oid
            or committed_tree != verified_tree
            or parents != [self._base.head.encode("ascii")]
        ):
            raise PublicationError(IssueCode.VERIFIED_TREE_MISMATCH)

    def _isolated_push_repo(self, root: Path) -> Path:
        """candidate 객체만 공유하는 push 전용 bare 저장소 생성."""

        template = root / "empty-template"
        try:
            template.mkdir()
        except OSError:
            raise PublicationError(IssueCode.RUNNER_OPERATION_FAILED) from None
        push_repo = root / "push.git"
        environment = dict(self._prepare_environment)
        environment["GIT_TEMPLATE_DIR"] = str(template)
        self._git_output(
            root,
            "clone",
            "--quiet",
            "--bare",
            "--shared",
            str(self._candidate_repo),
            str(push_repo),
            environment=environment,
            failure_code=IssueCode.RUNNER_OPERATION_FAILED,
        )
        return push_repo

    def _remote_oid(self, repo: Path, environment: Mapping[str, str]) -> str:
        """명시된 원격 브랜치 ref의 단일 객체 ID 조회."""

        output = self._git_output(
            repo,
            "ls-remote",
            "--refs",
            self._push_endpoint,
            self._base.remote_ref,
            environment=environment,
            failure_code=IssueCode.RUNNER_OPERATION_FAILED,
        )
        lines = [line for line in output.splitlines() if line]
        expected_ref = self._base.remote_ref.encode("utf-8")
        if len(lines) != 1:
            raise PublicationError(IssueCode.PUBLICATION_BASE_CHANGED)
        fields = lines[0].split(b"\t")
        if len(fields) != 2 or fields[1] != expected_ref:
            raise PublicationError(IssueCode.PUBLICATION_BASE_CHANGED)
        try:
            oid = fields[0].decode("ascii", errors="strict")
        except UnicodeDecodeError:
            raise PublicationError(IssueCode.PUBLICATION_BASE_CHANGED) from None
        if not _is_oid(oid):
            raise PublicationError(IssueCode.PUBLICATION_BASE_CHANGED)
        return oid

    def _read_fingerprint(self) -> str:
        """공유 기한 안에서 활성 저장소 fingerprint 조회."""

        try:
            fingerprint = self._read_active_fingerprint(self._remaining_timeout())
        except PublicationError:
            raise
        except subprocess.TimeoutExpired:
            raise PublicationError(IssueCode.WORKFLOW_DEADLINE_EXCEEDED) from None
        except Exception:
            raise PublicationError(IssueCode.RUNNER_OPERATION_FAILED) from None
        self._remaining_timeout()
        return fingerprint

    def _tree_oid(
        self,
        repo: Path,
        object_oid: str,
        *,
        environment: Mapping[str, str],
    ) -> str:
        """Git 객체가 가리키는 canonical tree ID 조회."""

        return self._git_oid(
            repo,
            "rev-parse",
            "--verify",
            f"{object_oid}^{{tree}}",
            environment=environment,
            failure_code=IssueCode.VERIFIED_TREE_MISMATCH,
        )

    def _git_oid(
        self,
        repo: Path,
        *args: str,
        input_bytes: bytes | None = None,
        environment: Mapping[str, str],
        failure_code: IssueCode,
    ) -> str:
        """Git 명령의 단일 canonical 객체 ID 출력 검증."""

        output = self._git_output(
            repo,
            *args,
            input_bytes=input_bytes,
            environment=environment,
            failure_code=failure_code,
        )
        try:
            value = output.decode("ascii", errors="strict").strip()
        except UnicodeDecodeError:
            raise PublicationError(failure_code) from None
        if not _is_oid(value):
            raise PublicationError(failure_code)
        return value

    def _git_output(
        self,
        repo: Path,
        *args: str,
        input_bytes: bytes | None = None,
        environment: Mapping[str, str],
        failure_code: IssueCode,
    ) -> bytes:
        """공유 기한과 격리 환경으로 Git 명령 실행."""

        try:
            completed = run_process_tree(
                ("git", *args),
                cwd=repo,
                env=dict(environment),
                check=False,
                input=input_bytes,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False,
                timeout=self._remaining_timeout(),
            )
        except subprocess.TimeoutExpired:
            raise PublicationError(IssueCode.WORKFLOW_DEADLINE_EXCEEDED) from None
        except (OSError, ProcessTreeError):
            raise PublicationError(IssueCode.RUNNER_OPERATION_FAILED) from None
        if completed.returncode != 0:
            raise PublicationError(failure_code)
        return completed.stdout

    def _remaining_timeout(self) -> float:
        """publication에 사용할 양의 유한 잔여 시간 반환."""

        try:
            remaining = self._remaining_seconds()
            if isinstance(remaining, bool):
                raise ValueError
            timeout = float(remaining)
        except Exception:
            raise PublicationError(IssueCode.WORKFLOW_DEADLINE_EXCEEDED) from None
        if not math.isfinite(timeout) or timeout <= 0:
            raise PublicationError(IssueCode.WORKFLOW_DEADLINE_EXCEEDED)
        return timeout


__all__ = [
    "PreparedPublication",
    "PublicationBase",
    "PublicationError",
    "PublicationResult",
    "Publisher",
    "build_cas_push_argv",
]
