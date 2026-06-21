"""운영 프롬프트 로딩.

한국어 프롬프트는 `translation-sync/prompt.md`, 일본어 프롬프트는
`translation-sync/prompt_jp.md`에서 그대로 읽는다.
"""
from __future__ import annotations

from pathlib import Path


class PromptError(Exception):
    """프롬프트 파일 오류."""


def load_prompt(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError as exc:
        raise PromptError(f"missing prompt file: {path}") from exc
