"""변경된 영어 원문 식별 (git 기반).

translation-sync/docs/02(변경 감지)·workflow(변경된 원문 문서 확인) 단계를 담당한다.
upstream 동기화로 i18n/en을 갱신한 뒤, working tree에서 변경된 .md를 번역 대상으로 고른다.
"""
from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
EN_PREFIX = "i18n/en/docusaurus-plugin-content-docs/"
_HUNK_RE = re.compile(
    r"^@@ -(?P<old_start>\d+)(?:,(?P<old_count>\d+))? "
    r"\+(?P<new_start>\d+)(?:,(?P<new_count>\d+))? @@"
)


@dataclass(frozen=True)
class DiffLine:
    """A single line inside a unified diff hunk."""

    kind: str  # context | add | delete
    text: str
    old_lineno: int | None
    new_lineno: int | None


@dataclass(frozen=True)
class DiffHunk:
    """A unified diff hunk for one source file."""

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

    @property
    def version(self) -> str:
        # i18n/en/docusaurus-plugin-content-docs/version-<v>/<file>.md
        return Path(self.path).parent.name.removeprefix("version-")

    @property
    def name(self) -> str:
        return Path(self.path).name


def changed_sources(base_ref: str | None = None) -> list[SourceChange]:
    """변경된 영어 원문 목록.

    base_ref가 없으면 working tree 변경(동기화 직후)을, 있으면 해당 커밋과의 diff를 본다.
    """
    if base_ref:
        args = ["git", "diff", "--name-status", base_ref, "--", EN_PREFIX]
    else:
        args = ["git", "status", "--porcelain", "--untracked-files=all", "--", EN_PREFIX]

    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
    result = subprocess.run(
        args, cwd=REPO_ROOT, capture_output=True, text=True, check=True, env=env
    )

    changes: list[SourceChange] = []
    for line in result.stdout.splitlines():
        if base_ref:
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            status, path = parts[0][0], parts[-1]
        else:
            status, path = line[:2].strip()[:1], line[3:]
            if status == "?":
                status = "A"
        if path.endswith(".md"):
            changes.append(
                SourceChange(
                    path=path,
                    status=status,
                    hunks=_file_hunks(path, status=status, base_ref=base_ref),
                )
            )
    return changes


def _git_diff_args(path: str, base_ref: str | None) -> list[str]:
    if base_ref:
        return ["git", "diff", "--unified=3", base_ref, "--", path]
    return ["git", "diff", "--unified=3", "HEAD", "--", path]


def _file_hunks(path: str, *, status: str, base_ref: str | None) -> tuple[DiffHunk, ...]:
    if status == "A" and not (REPO_ROOT / path).is_file():
        return ()
    if status == "A":
        return (_added_file_hunk(path),)

    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
    result = subprocess.run(
        _git_diff_args(path, base_ref),
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    return _parse_unified_diff(result.stdout)


def _added_file_hunk(path: str) -> DiffHunk:
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
    hunks: list[DiffHunk] = []
    current_header: tuple[int, int, int, int] | None = None
    current_lines: list[DiffLine] = []
    old_lineno = 0
    new_lineno = 0

    def flush() -> None:
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
