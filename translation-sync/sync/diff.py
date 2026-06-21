"""변경된 영어 원문 식별 (git 기반).

translation-sync/docs/02(변경 감지)·workflow(변경된 원문 문서 확인) 단계를 담당한다.
upstream 동기화로 i18n/en을 갱신한 뒤, working tree에서 변경된 .md를 번역 대상으로 고른다.
"""
from __future__ import annotations

import subprocess
import os
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EN_PREFIX = "i18n/en/docusaurus-plugin-content-docs/"


@dataclass(frozen=True)
class SourceChange:
    """변경된 원문 한 건. status: A(추가)/M(수정)/D(삭제)."""

    path: str
    status: str

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
            changes.append(SourceChange(path=path, status=status))
    return changes
