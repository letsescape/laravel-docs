"""한국어와 일본어 운영 프롬프트 로딩."""
from __future__ import annotations

from pathlib import Path


class PromptError(Exception):
    """프롬프트 파일 오류."""


def load_prompt(path: Path) -> str:
    """UTF-8 프롬프트 본문의 앞뒤 공백을 제거해 로딩.

    Raises:
        PromptError: 파일 누락, 읽기 실패 또는 UTF-8 해석 실패.
    """

    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError as exc:
        raise PromptError(f"missing prompt file: {path}") from exc
    except (OSError, UnicodeError) as exc:
        raise PromptError(f"could not read prompt file: {path}") from exc
