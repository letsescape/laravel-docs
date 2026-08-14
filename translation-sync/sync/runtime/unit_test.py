"""격리된 승인 기준본 checkout에서 등록된 단위 테스트 증명."""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import stat
import subprocess
import tempfile
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from .failure import IssueCode, exit_code_for
from .process import ProcessTreeError, run_process_tree


_PASSTHROUGH_ENV = {
    "CI",
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


@dataclass(frozen=True, slots=True)
class ApprovedBaseUnitTestProof:
    """통과한 원문과 명령을 증명하는 데 필요한 식별자."""

    base_commit: str
    base_tree: str
    argv_digest: str


@dataclass(frozen=True, slots=True)
class ApprovedBaseUnitTestFailure:
    """승인된 기준본 단위 테스트 실패 정보."""

    stage: str
    issue_code: IssueCode
    returncode: int | None = None


@dataclass(frozen=True, slots=True)
class ApprovedBaseUnitTestResult:
    """승인된 기준본 단위 테스트 결과."""

    proof: ApprovedBaseUnitTestProof | None = None
    failure: ApprovedBaseUnitTestFailure | None = None
    sandbox_path: Path | None = None
    sandbox_cleaned: bool = True

    @property
    def succeeded(self) -> bool:
        """증거 생성과 sandbox 정리가 모두 성공했는지 여부."""

        return self.proof is not None and self.failure is None and self.sandbox_cleaned


@dataclass(frozen=True, slots=True)
class _RepositoryDiskLayout:
    """활성 저장소 변경 감지에 필요한 디스크 경로와 추적 파일."""

    repo: Path
    git_dir: Path
    common_dir: Path
    tracked_paths: tuple[bytes, ...]


class _PreflightError(RuntimeError):
    """preflight 오류."""

    def __init__(
        self,
        *,
        stage: str,
        issue_code: IssueCode,
        returncode: int | None = None,
    ) -> None:
        """preflight 오류 초기화."""

        super().__init__(issue_code.value)
        self.failure = ApprovedBaseUnitTestFailure(
            stage=stage,
            issue_code=issue_code,
            returncode=returncode,
        )


class _DeadlineExceeded(RuntimeError):
    """공유 워크플로 기한 초과."""

    pass


class _ProcessStartFailed(RuntimeError):
    """격리 하위 프로세스 시작 또는 정리 실패."""

    pass


class _GitFailed(RuntimeError):
    """0이 아닌 종료 코드를 반환한 Git 명령."""

    def __init__(self, returncode: int) -> None:
        """Git 명령 오류 초기화."""

        super().__init__(returncode)
        self.returncode = returncode


def _prefer_failure(
    current: ApprovedBaseUnitTestFailure | None,
    candidate: ApprovedBaseUnitTestFailure,
) -> ApprovedBaseUnitTestFailure:
    """종료 코드 우선순위가 높은 실패 선택."""

    if current is None or exit_code_for(candidate.issue_code) > exit_code_for(
        current.issue_code
    ):
        return candidate
    return current


def unit_test_argv_digest(argv: Sequence[str]) -> str:
    """성공 증거에 사용할 argv의 결정적 SHA-256 digest 계산."""

    payload = json.dumps(
        list(argv),
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


class ApprovedBaseUnitTestRunner:
    """정확한 커밋의 폐기 가능한 detached clone에서 단일 argv 명령 실행."""

    def __init__(
        self,
        *,
        source_repo: Path,
        artifact_root: Path,
        remaining_seconds: Callable[[], float],
    ) -> None:
        """원본 저장소, 산출 경로 및 공유 기한 공급자 설정."""

        self._source_repo = source_repo.resolve()
        self._artifact_root = artifact_root.resolve(strict=False)
        self._remaining_seconds = remaining_seconds

    def run(
        self,
        *,
        base_commit: str,
        unit_test_argv: Sequence[str],
    ) -> ApprovedBaseUnitTestResult:
        """승인 기준본 clone에서 설정된 단위 테스트 실행 및 증명.

        Args:
            base_commit: 검증할 승인 기준본의 완전한 커밋 객체 ID.
            unit_test_argv: shell 해석 없이 실행할 단위 테스트 argv.

        Returns:
            성공 증거 또는 안정된 실패 정보와 sandbox 정리 결과.
        """

        sandbox: Path | None = None
        proof: ApprovedBaseUnitTestProof | None = None
        failure: ApprovedBaseUnitTestFailure | None = None
        active_layout: _RepositoryDiskLayout | None = None
        active_fingerprint: bytes | None = None
        stage = "configuration"

        try:
            command = self._command_argv(unit_test_argv)
            if not self._valid_full_oid(base_commit):
                raise _PreflightError(
                    stage=stage,
                    issue_code=IssueCode.INVALID_RUNTIME_OPTION,
                )
            if (
                self._artifact_root == self._source_repo
                or self._artifact_root.is_relative_to(self._source_repo)
            ):
                raise _PreflightError(
                    stage="sandbox",
                    issue_code=IssueCode.SANDBOX_OPERATION_FAILED,
                )

            self._remaining_timeout()
            stage = "active-fingerprint"
            active_layout = self._repository_disk_layout(self._source_repo)
            active_fingerprint = self._disk_fingerprint(active_layout)

            stage = "approved-base"
            resolved_base, base_tree = self._resolve_base(base_commit)

            stage = "sandbox"
            sandbox = self._new_sandbox()
            self._populate_clone(sandbox, resolved_base)

            stage = "unit-test-fingerprint"
            before_test = self._source_fingerprint(sandbox)

            stage = "unit-test"
            completed = self._process(
                command,
                cwd=sandbox,
                environment=self._unit_test_environment(sandbox),
                capture_output=False,
            )

            stage = "unit-test-fingerprint"
            after_test = self._source_fingerprint(sandbox)
            if after_test != before_test:
                raise _PreflightError(
                    stage=stage,
                    issue_code=IssueCode.UNIT_TEST_SOURCE_MUTATION,
                )
            if completed.returncode:
                raise _PreflightError(
                    stage="unit-test",
                    issue_code=IssueCode.UNIT_TEST_FAILED,
                    returncode=completed.returncode,
                )

            proof = ApprovedBaseUnitTestProof(
                base_commit=resolved_base,
                base_tree=base_tree,
                argv_digest=unit_test_argv_digest(command),
            )
        except _PreflightError as exc:
            failure = exc.failure
        except _DeadlineExceeded:
            failure = ApprovedBaseUnitTestFailure(
                stage=stage,
                issue_code=IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            )
        except _ProcessStartFailed:
            issue_code = (
                IssueCode.SANDBOX_OPERATION_FAILED
                if stage == "sandbox"
                else IssueCode.RUNNER_OPERATION_FAILED
            )
            failure = ApprovedBaseUnitTestFailure(
                stage=stage,
                issue_code=issue_code,
            )
        except _GitFailed as exc:
            issue_code = (
                IssueCode.SANDBOX_OPERATION_FAILED
                if stage == "sandbox"
                else IssueCode.RUNNER_OPERATION_FAILED
            )
            failure = ApprovedBaseUnitTestFailure(
                stage=stage,
                issue_code=issue_code,
                returncode=exc.returncode,
            )
        except OSError:
            issue_code = (
                IssueCode.SANDBOX_OPERATION_FAILED
                if stage == "sandbox"
                else IssueCode.RUNNER_OPERATION_FAILED
            )
            failure = ApprovedBaseUnitTestFailure(
                stage=stage,
                issue_code=issue_code,
            )
        except Exception:
            failure = ApprovedBaseUnitTestFailure(
                stage=stage,
                issue_code=IssueCode.UNCLASSIFIED_INTERNAL,
            )

        sandbox_cleaned = True
        if sandbox is not None:
            try:
                shutil.rmtree(sandbox)
            except OSError:
                sandbox_cleaned = False
                failure = _prefer_failure(
                    failure,
                    ApprovedBaseUnitTestFailure(
                        stage="sandbox-cleanup",
                        issue_code=IssueCode.SANDBOX_OPERATION_FAILED,
                    ),
                )
                proof = None

        if active_layout is not None and active_fingerprint is not None:
            final_failure: ApprovedBaseUnitTestFailure | None = None
            try:
                self._remaining_timeout()
                final_fingerprint = self._disk_fingerprint(active_layout)
                self._remaining_timeout()
            except _DeadlineExceeded:
                final_failure = ApprovedBaseUnitTestFailure(
                    stage="active-fingerprint",
                    issue_code=IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
                )
            except _PreflightError as exc:
                final_failure = ApprovedBaseUnitTestFailure(
                    stage="active-fingerprint",
                    issue_code=exc.failure.issue_code,
                )
            except OSError:
                final_failure = ApprovedBaseUnitTestFailure(
                    stage="active-fingerprint",
                    issue_code=IssueCode.RUNNER_OPERATION_FAILED,
                )
            else:
                if final_fingerprint != active_fingerprint:
                    final_failure = ApprovedBaseUnitTestFailure(
                        stage="active-fingerprint",
                        issue_code=IssueCode.ACTIVE_WORKTREE_MUTATED,
                    )
            if final_failure is not None:
                failure = _prefer_failure(failure, final_failure)
                proof = None

        return ApprovedBaseUnitTestResult(
            proof=proof,
            failure=failure,
            sandbox_path=sandbox,
            sandbox_cleaned=sandbox_cleaned,
        )

    @staticmethod
    def _valid_full_oid(value: object) -> bool:
        """완전한 SHA-1 또는 SHA-256 객체 ID 형태 여부."""

        return (
            isinstance(value, str)
            and len(value) in {40, 64}
            and all(character in "0123456789abcdefABCDEF" for character in value)
        )

    @staticmethod
    def _command_argv(argv: Sequence[str]) -> tuple[str, ...]:
        """설정의 단위 테스트 argv 정규화."""

        if isinstance(argv, (str, bytes)):
            raise _PreflightError(
                stage="configuration",
                issue_code=IssueCode.REQUIRED_CONFIG_MISSING,
            )
        command = tuple(argv)
        if not command:
            raise _PreflightError(
                stage="configuration",
                issue_code=IssueCode.REQUIRED_CONFIG_MISSING,
            )
        if any(
            not isinstance(argument, str)
            or not argument
            or "\0" in argument
            for argument in command
        ):
            raise _PreflightError(
                stage="configuration",
                issue_code=IssueCode.INVALID_RUNTIME_OPTION,
            )
        return command

    def _remaining_timeout(self) -> float:
        """유효하고 양수인 남은 워크플로 시간 반환."""

        try:
            remaining = float(self._remaining_seconds())
        except Exception as exc:
            raise _PreflightError(
                stage="configuration",
                issue_code=IssueCode.INVALID_RUNTIME_OPTION,
            ) from exc
        if not math.isfinite(remaining):
            raise _PreflightError(
                stage="configuration",
                issue_code=IssueCode.INVALID_RUNTIME_OPTION,
            )
        if remaining <= 0:
            raise _DeadlineExceeded
        return remaining

    def _minimal_environment(self, sandbox: Path | None = None) -> dict[str, str]:
        """사용자 설정과 자격 증명을 제거한 최소 실행 환경 구성."""

        environment = {
            key: value
            for key, value in os.environ.items()
            if key in _PASSTHROUGH_ENV or key.startswith("LC_")
        }
        home = Path(os.devnull) if sandbox is None else sandbox / ".git/unit-test-home"
        if sandbox is not None:
            home.mkdir(parents=True, exist_ok=True)
        environment.update(
            {
                "HOME": str(home),
                "XDG_CACHE_HOME": str(home / "cache"),
                "XDG_CONFIG_HOME": str(home),
                "UV_CACHE_DIR": str(home / "cache/uv"),
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_CONFIG_SYSTEM": os.devnull,
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_TERMINAL_PROMPT": "0",
            }
        )
        return environment

    def _unit_test_environment(self, sandbox: Path) -> Mapping[str, str]:
        """sandbox 내부 캐시와 설정 경로를 사용하는 테스트 환경 구성."""

        return self._minimal_environment(sandbox)

    def _process(
        self,
        argv: Sequence[str],
        *,
        cwd: Path,
        environment: Mapping[str, str],
        capture_output: bool,
    ) -> subprocess.CompletedProcess[bytes]:
        """남은 공유 기한으로 격리된 argv 하위 프로세스 실행."""

        kwargs: dict[str, object] = {
            "cwd": cwd,
            "env": dict(environment),
            "check": False,
            "timeout": self._remaining_timeout(),
            "shell": False,
        }
        if capture_output:
            kwargs.update(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            return run_process_tree(list(argv), **kwargs)  # type: ignore[arg-type]
        except subprocess.TimeoutExpired as exc:
            raise _DeadlineExceeded from exc
        except (OSError, ProcessTreeError) as exc:
            raise _ProcessStartFailed from exc

    def _git_process(
        self,
        repo: Path,
        *args: str,
    ) -> subprocess.CompletedProcess[bytes]:
        """최소 환경에서 Git 명령 실행."""

        return self._process(
            ("git", *args),
            cwd=repo,
            environment=self._minimal_environment(),
            capture_output=True,
        )

    def _git(self, repo: Path, *args: str) -> bytes:
        """성공한 Git 명령의 표준 출력 반환."""

        result = self._git_process(repo, *args)
        if result.returncode:
            raise _GitFailed(result.returncode)
        return result.stdout

    def _git_text(self, repo: Path, *args: str) -> str:
        """성공한 Git 명령의 ASCII 출력 반환."""

        return self._git(repo, *args).strip().decode("ascii")

    def _resolve_base(self, base_commit: str) -> tuple[str, str]:
        """승인 커밋과 그 tree 객체 ID를 정확히 해석."""

        object_format = self._git_text(
            self._source_repo,
            "rev-parse",
            "--show-object-format",
        )
        expected_length = {"sha1": 40, "sha256": 64}.get(object_format)
        if expected_length is None or len(base_commit) != expected_length:
            raise _PreflightError(
                stage="approved-base",
                issue_code=IssueCode.INVALID_RUNTIME_OPTION,
            )

        resolved = self._git_process(
            self._source_repo,
            "rev-parse",
            "--verify",
            "--end-of-options",
            f"{base_commit}^{{commit}}",
        )
        if resolved.returncode:
            raise _PreflightError(
                stage="approved-base",
                issue_code=IssueCode.MANIFEST_COMMIT_UNRESOLVED,
            )
        resolved_base = resolved.stdout.strip().decode("ascii")
        if resolved_base.lower() != base_commit.lower():
            raise _PreflightError(
                stage="approved-base",
                issue_code=IssueCode.MANIFEST_COMMIT_UNRESOLVED,
            )
        base_tree = self._git_text(
            self._source_repo,
            "rev-parse",
            "--verify",
            "--end-of-options",
            f"{resolved_base}^{{tree}}",
        )
        return resolved_base, base_tree

    def _new_sandbox(self) -> Path:
        """artifact root 아래에 예측 불가능한 sandbox 생성."""

        self._artifact_root.mkdir(parents=True, exist_ok=True)
        return Path(
            tempfile.mkdtemp(
                prefix="translation-unit-test-",
                dir=self._artifact_root,
            )
        )

    def _populate_clone(self, sandbox: Path, base_commit: str) -> None:
        """로컬 객체 공유 없는 detached 승인 기준본 clone 구성."""

        clone = self._process(
            (
                "git",
                "clone",
                "--local",
                "--no-hardlinks",
                "--no-checkout",
                "--quiet",
                "--",
                str(self._source_repo),
                str(sandbox),
            ),
            cwd=self._source_repo.parent,
            environment=self._minimal_environment(),
            capture_output=True,
        )
        if clone.returncode:
            raise _GitFailed(clone.returncode)
        self._git(sandbox, "checkout", "--detach", "--quiet", base_commit)
        if self._git_text(sandbox, "rev-parse", "HEAD") != base_commit:
            raise _PreflightError(
                stage="sandbox",
                issue_code=IssueCode.SANDBOX_OPERATION_FAILED,
            )
        alternates = sandbox / ".git/objects/info/alternates"
        if alternates.exists():
            raise _PreflightError(
                stage="sandbox",
                issue_code=IssueCode.SANDBOX_OPERATION_FAILED,
            )

    def _source_fingerprint(self, repo: Path) -> bytes:
        """clone의 HEAD, index 및 추적 파일 fingerprint 계산."""

        head = self._git(repo, "rev-parse", "HEAD")
        index = self._git(repo, "ls-files", "--stage", "-z")
        paths = tuple(
            sorted(
                entry.split(b"\t", 1)[1]
                for entry in index.split(b"\0")
                if entry and b"\t" in entry
            )
        )
        return self._fingerprint(
            repo=repo,
            head=head,
            index=index,
            tracked_paths=paths,
        )

    def _repository_disk_layout(self, repo: Path) -> _RepositoryDiskLayout:
        """활성 저장소의 Git 메타데이터와 추적 파일 경로 해석."""

        git_dir = Path(
            self._git_text(repo, "rev-parse", "--absolute-git-dir")
        ).resolve()
        common_value = self._git_text(repo, "rev-parse", "--git-common-dir")
        common_dir = Path(common_value)
        if not common_dir.is_absolute():
            common_dir = repo / common_dir
        tracked = self._git(repo, "ls-files", "--stage", "-z")
        tracked_paths = tuple(
            sorted(
                entry.split(b"\t", 1)[1]
                for entry in tracked.split(b"\0")
                if entry and b"\t" in entry
            )
        )
        return _RepositoryDiskLayout(
            repo=repo,
            git_dir=git_dir,
            common_dir=common_dir.resolve(),
            tracked_paths=tracked_paths,
        )

    def _disk_fingerprint(self, layout: _RepositoryDiskLayout) -> bytes:
        """활성 저장소의 감시 대상 디스크 상태에 대한 SHA-256 fingerprint 계산."""

        digest = hashlib.sha256()
        for label, path in (
            (b"HEAD", layout.git_dir / "HEAD"),
            (b"INDEX", layout.git_dir / "index"),
            (b"PACKED_REFS", layout.common_dir / "packed-refs"),
        ):
            digest.update(label + b"\0")
            self._update_path_digest(digest.update, path)

        head_path = layout.git_dir / "HEAD"
        try:
            head_value = head_path.read_bytes().strip()
        except OSError:
            head_value = b""
        if head_value.startswith(b"ref: "):
            ref = os.fsdecode(head_value[5:])
            digest.update(b"HEAD_REF\0")
            self._update_path_digest(digest.update, layout.git_dir / ref)
            if layout.common_dir != layout.git_dir:
                self._update_path_digest(digest.update, layout.common_dir / ref)

        for raw_path in layout.tracked_paths:
            digest.update(b"PATH\0")
            digest.update(raw_path)
            self._update_path_digest(
                digest.update,
                layout.repo / Path(os.fsdecode(raw_path)),
            )
        return digest.digest()

    def _fingerprint(
        self,
        *,
        repo: Path,
        head: bytes,
        index: bytes,
        tracked_paths: Sequence[bytes],
    ) -> bytes:
        """주어진 Git 상태와 추적 파일의 SHA-256 fingerprint 계산."""

        digest = hashlib.sha256()
        digest.update(b"HEAD\0")
        digest.update(head)
        digest.update(b"INDEX\0")
        digest.update(index)
        for raw_path in tracked_paths:
            digest.update(b"PATH\0")
            digest.update(raw_path)
            self._update_path_digest(
                digest.update,
                repo / Path(os.fsdecode(raw_path)),
            )
        return digest.digest()

    @staticmethod
    def _update_path_digest(
        update: Callable[[bytes], object],
        path: Path,
    ) -> None:
        """파일 종류, 모드 및 내용을 fingerprint digest에 반영."""

        try:
            metadata = path.lstat()
        except FileNotFoundError:
            update(b"MISSING\0")
            return
        mode = metadata.st_mode
        update((mode & 0o177777).to_bytes(4, "big"))
        if stat.S_ISLNK(mode):
            update(b"LINK\0")
            update(os.fsencode(os.readlink(path)))
        elif stat.S_ISREG(mode):
            update(b"FILE\0")
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    update(chunk)
        else:
            update(b"OTHER\0")
