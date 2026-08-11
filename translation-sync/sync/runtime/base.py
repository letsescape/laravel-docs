"""추적 변경이 없는 publication 기준본 캡처와 저장소 fingerprint 생성."""

from __future__ import annotations

import hashlib
import math
import os
import stat
import subprocess
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

from .failure import IssueCode
from .process import ProcessTreeError, run_process_tree


_OWNED_PREFIXES = (
    b"i18n/en/docusaurus-plugin-content-docs/",
    b"i18n/ja/docusaurus-plugin-content-docs/",
    b"versioned_docs/",
    b"versioned_sidebars/",
)

_READ_ONLY_GIT_ENV = frozenset(
    {
        "ALL_PROXY",
        "COMSPEC",
        "CURL_CA_BUNDLE",
        "FTP_PROXY",
        "GIT_SSL_CAINFO",
        "GIT_SSL_CAPATH",
        "HTTPS_PROXY",
        "HTTP_PROXY",
        "LANG",
        "LANGUAGE",
        "NO_PROXY",
        "PATH",
        "PATHEXT",
        "SSL_CERT_DIR",
        "SSL_CERT_FILE",
        "SYSTEMROOT",
        "TEMP",
        "TMP",
        "TMPDIR",
        "WINDIR",
        "all_proxy",
        "ftp_proxy",
        "http_proxy",
        "https_proxy",
        "no_proxy",
    }
)


def _read_only_git_environment() -> dict[str, str]:
    """자격 증명과 사용자 설정을 제거한 읽기 전용 Git 환경 구성."""

    environment = {
        key: value
        for key, value in os.environ.items()
        if key in _READ_ONLY_GIT_ENV or key.startswith("LC_")
    }
    environment.setdefault("PATH", os.defpath)
    environment.update(
        {
            "HOME": os.devnull,
            "XDG_CONFIG_HOME": os.devnull,
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "credential.helper",
            "GIT_CONFIG_VALUE_0": "",
            "GIT_ASKPASS": os.devnull,
            "SSH_ASKPASS": os.devnull,
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_TERMINAL_PROMPT": "0",
        }
    )
    return environment


class RepositoryStateError(RuntimeError):
    """저장소 상태 오류."""

    def __init__(self, code: IssueCode) -> None:
        """저장소 상태 오류 초기화."""

        self.code = code
        super().__init__(code.value)


@dataclass(frozen=True, slots=True)
class ApprovedPublicationBase:
    """실행 시작 시 고정한 publication 기준본 식별자."""

    head: str
    tree: str
    remote_ref: str
    remote_oid: str
    active_fingerprint: str


class _Git:
    """공유 기한과 격리 환경을 적용하는 읽기 전용 Git 실행기."""

    def __init__(
        self,
        repo: Path,
        remaining_seconds: Callable[[], float],
    ) -> None:
        """저장소와 남은 실행 시간 공급자 설정."""

        self.repo = repo.resolve()
        self.remaining_seconds = remaining_seconds
        if not self.repo.is_dir():
            raise RepositoryStateError(IssueCode.RUNNER_OPERATION_FAILED)

    def run(self, args: Sequence[str]) -> subprocess.CompletedProcess[bytes]:
        """남은 기한 안에서 Git 하위 프로세스 실행."""

        try:
            remaining = float(self.remaining_seconds())
        except Exception:
            raise RepositoryStateError(IssueCode.RUNNER_OPERATION_FAILED) from None
        if not math.isfinite(remaining) or remaining <= 0:
            raise RepositoryStateError(IssueCode.WORKFLOW_DEADLINE_EXCEEDED)
        environment = _read_only_git_environment()
        try:
            return run_process_tree(
                ("git", *args),
                cwd=self.repo,
                env=environment,
                check=False,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=remaining,
                shell=False,
            )
        except subprocess.TimeoutExpired:
            raise RepositoryStateError(IssueCode.WORKFLOW_DEADLINE_EXCEEDED) from None
        except (OSError, ProcessTreeError):
            raise RepositoryStateError(IssueCode.RUNNER_OPERATION_FAILED) from None

    def output(self, *args: str, code: IssueCode) -> bytes:
        """성공한 Git 명령의 표준 출력 반환."""

        result = self.run(args)
        if result.returncode != 0:
            raise RepositoryStateError(code)
        return result.stdout


def _canonical_oid(value: bytes, *, code: IssueCode) -> str:
    """Git 출력의 SHA-1 또는 SHA-256 객체 ID 정규화."""

    try:
        oid = value.strip().decode("ascii")
    except UnicodeDecodeError:
        raise RepositoryStateError(code) from None
    if (
        len(oid) not in {40, 64}
        or oid != oid.lower()
        or any(character not in "0123456789abcdef" for character in oid)
    ):
        raise RepositoryStateError(code)
    return oid


def active_repository_fingerprint(
    repo: Path,
    *,
    remaining_seconds: Callable[[], float],
) -> str:
    """활성 저장소의 HEAD, index 및 파일 상태 fingerprint 계산.

    Args:
        repo: fingerprint 대상 Git 저장소.
        remaining_seconds: 각 Git 호출에 사용할 남은 시간 공급자.

    Returns:
        저장소 상태를 대표하는 SHA-256 16진수 digest.

    Raises:
        RepositoryStateError: 저장소 상태를 완전하게 읽지 못한 경우.
    """

    git = _Git(repo, remaining_seconds)
    digest = hashlib.sha256()
    head = git.output("rev-parse", "--verify", "HEAD^{commit}", code=IssueCode.RUNNER_OPERATION_FAILED)
    index = git.output("ls-files", "--stage", "-z", code=IssueCode.RUNNER_OPERATION_FAILED)
    untracked = git.output(
        "ls-files",
        "--others",
        "--exclude-standard",
        "-z",
        code=IssueCode.RUNNER_OPERATION_FAILED,
    )
    digest.update(b"HEAD\0" + head)
    digest.update(b"INDEX\0" + index)
    digest.update(b"UNTRACKED\0" + untracked)

    tracked_paths = {
        entry.split(b"\t", 1)[1]
        for entry in index.split(b"\0")
        if entry and b"\t" in entry
    }
    paths = tracked_paths | {entry for entry in untracked.split(b"\0") if entry}
    for raw_path in sorted(paths):
        digest.update(b"PATH\0" + raw_path + b"\0")
        path = git.repo / Path(os.fsdecode(raw_path))
        try:
            metadata = path.lstat()
        except FileNotFoundError:
            digest.update(b"MISSING\0")
            continue
        mode = metadata.st_mode
        digest.update((mode & 0o177777).to_bytes(4, "big"))
        if stat.S_ISLNK(mode):
            digest.update(b"LINK\0" + os.fsencode(os.readlink(path)))
        elif stat.S_ISREG(mode):
            digest.update(b"FILE\0")
            try:
                with path.open("rb") as handle:
                    for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                        digest.update(chunk)
            except OSError:
                raise RepositoryStateError(IssueCode.RUNNER_OPERATION_FAILED) from None
        else:
            digest.update(b"OTHER\0")
    return digest.hexdigest()


def read_remote_ref_oid(
    repo: Path,
    *,
    remote: str,
    remote_ref: str,
    remaining_seconds: Callable[[], float],
) -> str:
    """원격 저장소의 단일 branch ref 객체 ID 조회.

    Args:
        repo: Git 명령을 실행할 로컬 저장소.
        remote: 조회 대상 remote 이름 또는 endpoint.
        remote_ref: 완전한 원격 branch ref.
        remaining_seconds: 각 Git 호출에 사용할 남은 시간 공급자.

    Returns:
        정규화된 원격 commit 객체 ID.

    Raises:
        RepositoryStateError: ref가 없거나 결과가 모호한 경우.
    """

    git = _Git(repo, remaining_seconds)
    output = git.output(
        "ls-remote",
        "--exit-code",
        "--heads",
        remote,
        remote_ref,
        code=IssueCode.PUBLICATION_BASE_CHANGED,
    )
    lines = [line for line in output.splitlines() if line]
    if len(lines) != 1:
        raise RepositoryStateError(IssueCode.PUBLICATION_BASE_CHANGED)
    parts = lines[0].split(b"\t")
    if len(parts) != 2 or parts[1] != remote_ref.encode("utf-8"):
        raise RepositoryStateError(IssueCode.PUBLICATION_BASE_CHANGED)
    return _canonical_oid(parts[0], code=IssueCode.PUBLICATION_BASE_CHANGED)


def capture_publication_base(
    repo: Path,
    *,
    remote: str,
    branch: str,
    remaining_seconds: Callable[[], float],
) -> ApprovedPublicationBase:
    """추적 변경과 publication 대상의 미추적 파일이 없는 실행 branch의 원격 기준본 고정.

    Args:
        repo: publication 대상 로컬 저장소.
        remote: 기준 ref를 조회할 remote 이름 또는 endpoint.
        branch: 현재 checkout 및 원격 기준 branch 이름.
        remaining_seconds: 각 Git 호출에 사용할 남은 시간 공급자.

    Returns:
        HEAD, tree, 원격 ref, 원격 commit 및 활성 상태 fingerprint의 고정값.

    Raises:
        RepositoryStateError: branch, worktree 또는 원격 기준이 부적합한 경우.
    """

    if (
        not remote
        or remote.startswith("-")
        or not branch
        or branch.startswith("-")
        or "\0" in remote
        or "\0" in branch
    ):
        raise RepositoryStateError(IssueCode.INVALID_RUNTIME_OPTION)
    git = _Git(repo, remaining_seconds)
    branch_result = git.run(("symbolic-ref", "--quiet", "--short", "HEAD"))
    if branch_result.returncode != 0:
        raise RepositoryStateError(IssueCode.NON_BRANCH_REF)
    try:
        actual_branch = branch_result.stdout.strip().decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        raise RepositoryStateError(IssueCode.NON_BRANCH_REF) from None
    if actual_branch != branch:
        raise RepositoryStateError(IssueCode.NON_BRANCH_REF)

    for args in (("diff", "--quiet"), ("diff", "--cached", "--quiet")):
        status = git.run(args)
        if status.returncode == 1:
            raise RepositoryStateError(IssueCode.DIRTY_PUBLICATION_BASE)
        if status.returncode != 0:
            raise RepositoryStateError(IssueCode.RUNNER_OPERATION_FAILED)

    owned_untracked = git.output(
        "ls-files",
        "--others",
        "--exclude-standard",
        "-z",
        "--",
        *(prefix.decode("ascii") for prefix in _OWNED_PREFIXES),
        code=IssueCode.RUNNER_OPERATION_FAILED,
    )
    if any(owned_untracked.split(b"\0")):
        raise RepositoryStateError(IssueCode.DIRTY_PUBLICATION_BASE)

    head = _canonical_oid(
        git.output("rev-parse", "--verify", "HEAD^{commit}", code=IssueCode.RUNNER_OPERATION_FAILED),
        code=IssueCode.RUNNER_OPERATION_FAILED,
    )
    tree = _canonical_oid(
        git.output("rev-parse", "--verify", "HEAD^{tree}", code=IssueCode.RUNNER_OPERATION_FAILED),
        code=IssueCode.RUNNER_OPERATION_FAILED,
    )
    remote_ref = f"refs/heads/{branch}"
    remote_oid = read_remote_ref_oid(
        repo,
        remote=remote,
        remote_ref=remote_ref,
        remaining_seconds=remaining_seconds,
    )
    if remote_oid != head:
        raise RepositoryStateError(IssueCode.PUBLICATION_BASE_CHANGED)
    fingerprint = active_repository_fingerprint(
        repo,
        remaining_seconds=remaining_seconds,
    )
    return ApprovedPublicationBase(
        head=head,
        tree=tree,
        remote_ref=remote_ref,
        remote_oid=remote_oid,
        active_fingerprint=fingerprint,
    )


__all__ = [
    "ApprovedPublicationBase",
    "RepositoryStateError",
    "active_repository_fingerprint",
    "capture_publication_base",
    "read_remote_ref_oid",
]
