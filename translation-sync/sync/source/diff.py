"""Git 상태에서 변경된 영어 원문 식별.

고정 upstream commit을 영어 cache에 동기화한 뒤 승인 기준본과 현재
worktree를 비교. canonical Markdown 경로만 선택하고 변경 상태를 추가(A),
수정(M), 삭제(D)로 제한하며 Git rename은 삭제와 추가로 분해.
"""
from __future__ import annotations

import difflib
import math
import os
import re
import subprocess
import time
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from ..runtime.process import ProcessTreeError, run_process_tree

REPO_ROOT = Path(__file__).resolve().parents[3]
EN_PREFIX = "i18n/en/docusaurus-plugin-content-docs/"
_HUNK_RE = re.compile(
    r"^@@ -(?P<old_start>\d+)(?:,(?P<old_count>\d+))? "
    r"\+(?P<new_start>\d+)(?:,(?P<new_count>\d+))? @@"
)
_RENAME_STATUS_RE = re.compile(r"R(?P<score>\d{1,3})")
_VERSION_RE = re.compile(r"^(?:master|(?:0|[1-9]\d*)\.x)$")
WORKFLOW_DEADLINE_ENV = "TRANSLATION_WORKFLOW_DEADLINE_MONOTONIC"
_LOCALE_ENV_NAMES = frozenset(("LANG", "LANGUAGE", "PATH"))
_GIT_CONFIG_OVERRIDES = ("-c", "core.fsmonitor=false")


class SourceDiffError(ValueError):
    """A/M/D 계약으로 표현할 수 없는 Git 원문 상태 오류."""


def _git_environment() -> dict[str, str]:
    """사용자 설정과 credential을 제거한 diff용 Git 환경 구성."""

    environment = {
        key: value
        for key, value in os.environ.items()
        if key in _LOCALE_ENV_NAMES or key.startswith("LC_")
    }
    if not environment.get("PATH"):
        raise SourceDiffError("git environment requires PATH")
    environment.update(
        {
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
        }
    )
    return environment


def _remaining_workflow_timeout() -> float | None:
    """환경 변수의 공유 기한에서 남은 실행 시간 계산."""

    raw_deadline = os.environ.get(WORKFLOW_DEADLINE_ENV)
    if raw_deadline is None:
        return None
    try:
        deadline = float(raw_deadline)
    except (TypeError, ValueError):
        raise SourceDiffError("invalid workflow deadline") from None
    if not math.isfinite(deadline):
        raise SourceDiffError("invalid workflow deadline")
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise SourceDiffError("workflow deadline exceeded")
    return remaining


def _git_command(command: str, *arguments: str) -> list[str]:
    """fsmonitor를 비활성화한 Git argv 구성."""

    return ["git", *_GIT_CONFIG_OVERRIDES, command, *arguments]


def _run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    """격리된 환경과 공유 기한으로 Git 명령 실행."""

    timeout = _remaining_workflow_timeout()
    try:
        return run_process_tree(
            args,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
            env=_git_environment(),
            timeout=timeout,
            stdin=subprocess.DEVNULL,
            shell=False,
        )
    except subprocess.TimeoutExpired:
        raise SourceDiffError("workflow deadline exceeded") from None
    except (OSError, ProcessTreeError):
        raise SourceDiffError("git subprocess failed") from None


def _parse_source_path(path: str) -> tuple[str, str]:
    """영어 cache 경로에서 버전과 canonical 문서 경로 추출."""

    if not isinstance(path, str) or not path.startswith(EN_PREFIX):
        raise SourceDiffError(f"invalid source path: {path!r}")
    if (
        not path
        or "\\" in path
        or "\0" in path
        or unicodedata.normalize("NFC", path) != path
    ):
        raise SourceDiffError(f"invalid source path: {path!r}")

    candidate = PurePosixPath(path)
    if candidate.is_absolute() or candidate.as_posix() != path:
        raise SourceDiffError(f"invalid source path: {path!r}")

    relative = path[len(EN_PREFIX) :]
    parts = relative.split("/")
    if len(parts) < 2 or any(part in {"", ".", ".."} for part in parts):
        raise SourceDiffError(f"invalid source path: {path!r}")

    version_root = parts[0]
    if not version_root.startswith("version-"):
        raise SourceDiffError(f"invalid source path: {path!r}")
    version = version_root[len("version-") :]
    document = "/".join(parts[1:])
    if not _VERSION_RE.fullmatch(version) or not document.endswith(".md"):
        raise SourceDiffError(f"invalid source path: {path!r}")
    return version, document


@dataclass(frozen=True)
class DiffLine:
    """unified diff hunk 내부의 단일 줄."""

    kind: str  # context | add | delete
    text: str
    old_lineno: int | None
    new_lineno: int | None


@dataclass(frozen=True)
class DiffHunk:
    """단일 원문 파일에 대한 unified diff hunk."""

    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: tuple[DiffLine, ...]


@dataclass(frozen=True)
class SourceChange:
    """변경된 원문 한 건. status: A(추가)/M(수정)/D(삭제)."""

    path: str
    status: str
    hunks: tuple[DiffHunk, ...] = ()

    def __post_init__(self) -> None:
        """공개 A/M/D 상태와 canonical 원문 경로 검증."""

        if self.status not in {"A", "M", "D"}:
            raise SourceDiffError(f"unsupported source status: {self.status!r}")
        _parse_source_path(self.path)

    @property
    def version(self) -> str:
        """원문 cache 경로의 문서 버전."""

        return _parse_source_path(self.path)[0]

    @property
    def document(self) -> str:
        """원문 버전 root 기준의 canonical Markdown 상대 경로."""
        return _parse_source_path(self.path)[1]

    @property
    def name(self) -> str:
        """중첩 경로를 제외한 Markdown 파일 이름."""

        return PurePosixPath(self.document).name


def hunks_between(old_text: str, new_text: str) -> tuple[DiffHunk, ...]:
    """메모리의 이전·현재 원문 사이 unified diff hunk 계산."""
    output = "\n".join(
        difflib.unified_diff(
            old_text.splitlines(),
            new_text.splitlines(),
            lineterm="",
        )
    )
    return _parse_unified_diff(output)


def changed_sources(base_ref: str | None = None) -> list[SourceChange]:
    """변경된 영어 원문 목록.

    ``base_ref``가 없으면 원문 동기화 직후 worktree 상태를 사용하고, 값이
    있으면 해당 commit과 현재 상태를 비교. Git rename은 삭제와 추가로 분해.

    Args:
        base_ref: 비교 기준 commit 또는 ref. 생략 시 index와 worktree 사용.

    Returns:
        canonical 경로 순서로 정렬된 A/M/D 원문 변경 목록.

    Raises:
        SourceDiffError: Git 상태나 원문 경로가 공개 계약에 맞지 않는 경우.
    """
    if base_ref:
        args = _git_command(
            "diff",
            "--no-ext-diff",
            "--no-textconv",
            "--name-status",
            "--find-renames",
            "-z",
            base_ref,
            "--",
            EN_PREFIX,
        )
    else:
        args = _git_command(
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
            "--find-renames",
            "-z",
            "--",
            EN_PREFIX,
        )
    result = _run_git(args)

    if base_ref:
        records = _parse_name_status(result.stdout)
    else:
        records = _parse_porcelain_status(result.stdout)

    for _, path in records:
        _validate_git_source_path(path)

    return [
        SourceChange(
            path=path,
            status=status,
            hunks=_file_hunks(path, status=status, base_ref=base_ref),
        )
        for status, path in records
        if path.endswith(".md")
    ]


def _validate_git_source_path(path: str) -> None:
    """Git이 반환한 원문 경로와 실제 파일의 symlink 안전성 검증."""

    try:
        _parse_source_path(path)
    except SourceDiffError as exc:
        raise SourceDiffError(f"invalid git source path: {path!r}") from exc

    candidate = PurePosixPath(path)

    root = REPO_ROOT.absolute()
    current = root
    for part in candidate.parts:
        current /= part
        if current.is_symlink():
            raise SourceDiffError(f"unsafe git source path: {path!r}")
    if not current.resolve(strict=False).is_relative_to(root.resolve()):
        raise SourceDiffError(f"unsafe git source path: {path!r}")


def _parse_name_status(output: str) -> list[tuple[str, str]]:
    """NUL 구분 ``git diff --name-status`` 결과를 A/M/D로 파싱."""

    if not output:
        return []
    if not output.endswith("\0"):
        raise SourceDiffError("malformed git name-status output")

    fields = output[:-1].split("\0")
    records: list[tuple[str, str]] = []
    index = 0
    while index < len(fields):
        status = fields[index]
        index += 1
        if status in {"A", "M", "D"}:
            if index >= len(fields):
                raise SourceDiffError("malformed git name-status output")
            records.append((status, fields[index]))
            index += 1
            continue

        match = _RENAME_STATUS_RE.fullmatch(status)
        if match and 0 < int(match.group("score")) <= 100:
            if index + 1 >= len(fields):
                raise SourceDiffError("malformed git rename output")
            old_path, new_path = fields[index : index + 2]
            records.extend((("D", old_path), ("A", new_path)))
            index += 2
            continue

        raise SourceDiffError(f"unsupported git status: {status!r}")
    return records


def _parse_porcelain_status(output: str) -> list[tuple[str, str]]:
    """NUL 구분 porcelain v1 상태를 A/M/D로 파싱."""

    if not output:
        return []
    if not output.endswith("\0"):
        raise SourceDiffError("malformed git porcelain output")

    fields = output[:-1].split("\0")
    records: list[tuple[str, str]] = []
    index = 0
    while index < len(fields):
        record = fields[index]
        index += 1
        if len(record) < 4 or record[2] != " ":
            raise SourceDiffError("malformed git porcelain record")

        state, path = record[:2], record[3:]
        if state == "??":
            records.append(("A", path))
        elif state in {" M", "M ", "MM"}:
            records.append(("M", path))
        elif state in {" D", "D "}:
            records.append(("D", path))
        elif state in {"A ", "AM"}:
            records.append(("A", path))
        elif state in {"R ", "RM"}:
            if index >= len(fields):
                raise SourceDiffError("malformed git porcelain rename")
            old_path = fields[index]
            index += 1
            records.extend((("D", old_path), ("A", path)))
        else:
            raise SourceDiffError(f"unsupported git status: {state!r}")
    return records


def _git_diff_args(path: str, base_ref: str | None) -> list[str]:
    """외부 diff와 textconv를 차단한 단일 파일 diff argv 구성."""

    if base_ref:
        return _git_command(
            "diff",
            "--no-ext-diff",
            "--no-textconv",
            "--unified=3",
            base_ref,
            "--",
            path,
        )
    return _git_command(
        "diff",
        "--no-ext-diff",
        "--no-textconv",
        "--unified=3",
        "HEAD",
        "--",
        path,
    )


def _file_hunks(path: str, *, status: str, base_ref: str | None) -> tuple[DiffHunk, ...]:
    """원문 상태별 unified diff hunk 로딩."""

    if status == "A" and not (REPO_ROOT / path).is_file():
        return ()
    if status == "A":
        return (_added_file_hunk(path),)

    result = _run_git(_git_diff_args(path, base_ref))
    return _parse_unified_diff(result.stdout)


def _added_file_hunk(path: str) -> DiffHunk:
    """신규 원문 전체를 포함하는 단일 추가 hunk 생성."""

    lines: list[DiffLine] = []
    source_lines = (REPO_ROOT / path).read_text(encoding="utf-8").splitlines()
    for index, text in enumerate(source_lines, start=1):
        lines.append(DiffLine("add", text, None, index))
    return DiffHunk(
        old_start=0,
        old_count=0,
        new_start=1,
        new_count=len(lines),
        lines=tuple(lines),
    )


def _parse_unified_diff(output: str) -> tuple[DiffHunk, ...]:
    """Git unified diff 출력을 구조화된 hunk tuple로 파싱."""

    hunks: list[DiffHunk] = []
    current_header: tuple[int, int, int, int] | None = None
    current_lines: list[DiffLine] = []
    old_lineno = 0
    new_lineno = 0

    def flush() -> None:
        """현재 diff hunk를 결과 목록에 확정."""

        nonlocal current_header, current_lines
        if current_header is None:
            return
        old_start, old_count, new_start, new_count = current_header
        hunks.append(
            DiffHunk(
                old_start=old_start,
                old_count=old_count,
                new_start=new_start,
                new_count=new_count,
                lines=tuple(current_lines),
            )
        )
        current_header = None
        current_lines = []

    for raw_line in output.splitlines():
        match = _HUNK_RE.match(raw_line)
        if match:
            flush()
            old_start = int(match.group("old_start"))
            old_count = int(match.group("old_count") or "1")
            new_start = int(match.group("new_start"))
            new_count = int(match.group("new_count") or "1")
            current_header = (old_start, old_count, new_start, new_count)
            old_lineno = old_start
            new_lineno = new_start
            continue

        if current_header is None:
            continue
        if not raw_line:
            current_lines.append(DiffLine("context", "", old_lineno, new_lineno))
            old_lineno += 1
            new_lineno += 1
            continue
        prefix = raw_line[0]
        text = raw_line[1:]
        if prefix == "\\":
            continue
        if prefix == " ":
            current_lines.append(DiffLine("context", text, old_lineno, new_lineno))
            old_lineno += 1
            new_lineno += 1
        elif prefix == "-":
            current_lines.append(DiffLine("delete", text, old_lineno, None))
            old_lineno += 1
        elif prefix == "+":
            current_lines.append(DiffLine("add", text, None, new_lineno))
            new_lineno += 1

    flush()
    return tuple(hunks)
