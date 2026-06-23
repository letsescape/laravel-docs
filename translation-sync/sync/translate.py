"""번역 (provider 호출). translation-sync/docs/02.

호출자가 전달한 locale별 운영 프롬프트를 시스템 프롬프트로 사용한다.
청크 분할은 라인 수를 기준으로 하되 fenced code block은 중간에서 끊지 않는다(workflow).
provider: openai | azure | cli.
"""
from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Callable

from .config import Config
from .markdown import closes_fence, fence_token

REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPT_PATH = REPO_ROOT / "translation-sync" / "prompt.md"
MAX_CHUNK_LINES = 400
MAX_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 300


class IncompleteTranslation(Exception):
    """provider 재시도 초과로 완료하지 못한 chunk."""


# 영어 원문 주석 병기 형식 (docs/02·05 T2, versioned_docs 레퍼런스).
# Locale별 제목 병기 규칙과 공존한다.
_ANNOTATION_FORMAT = """

## Output Format (Required)

Add the original English source as HTML comments in the translated output. For
each translated heading and paragraph, place the corresponding English source on
the line immediately above it as a one-line HTML comment.

Example:
<!-- # Section Title -->
# Translated Section Title (Section Title)

<!-- English paragraph text on one line. -->
Translated paragraph in the target language.

Rules:
- Collapse line breaks inside English comments into spaces so each comment stays
  on one line.
- Follow the locale prompt's heading style and add the English source comment
  above the heading.
- Keep `<a name="..."></a>` anchors in their original position without adding
  comments for them.
- Do not add English source comments to TOC link lists.
- Keep fenced code blocks unchanged. Do not translate or annotate them.
"""


def load_prompt() -> str:
    return PROMPT_PATH.read_text("utf-8")


def _is_anchor_line(line: str) -> bool:
    stripped = line.strip().lower()
    return stripped.startswith("<a ") and "name=" in stripped


def _is_heading_line(line: str) -> bool:
    stripped = line.lstrip()
    level = len(stripped) - len(stripped.lstrip("#"))
    return 1 <= level <= 6 and len(stripped) > level and stripped[level].isspace()


def _previous_nonblank_index(lines: list[str], index: int) -> int | None:
    cursor = index - 1
    while cursor >= 0:
        if lines[cursor].strip():
            return cursor
        cursor -= 1
    return None


def _next_nonblank_index(lines: list[str], index: int) -> int | None:
    cursor = index + 1
    while cursor < len(lines):
        if lines[cursor].strip():
            return cursor
        cursor += 1
    return None


def _is_anchor_heading_gap(lines: list[str], index: int) -> bool:
    previous = _previous_nonblank_index(lines, index)
    following = _next_nonblank_index(lines, index)
    if previous is None or following is None:
        return False
    return _is_anchor_line(lines[previous]) and _is_heading_line(lines[following])


def split_chunks(content: str, max_lines: int = MAX_CHUNK_LINES) -> list[str]:
    """라인 수 기준 청크 분할. 공백 줄을 절단 후보로 삼고 코드 블록은 끊지 않는다."""
    lines = content.splitlines(keepends=True)
    chunks: list[str] = []
    cur: list[str] = []
    in_code = False
    fence = ""
    count = 0
    for idx, line in enumerate(lines):
        token = fence_token(line)
        if token:
            if not in_code:
                in_code, fence = True, token
            elif closes_fence(line, fence):
                in_code = False
        cur.append(line)
        count += 1
        can_split = (
            count >= max_lines
            and not in_code
            and line.strip() == ""
            and not _is_anchor_heading_gap(lines, idx)
        )
        if can_split:
            chunks.append("".join(cur))
            cur, count = [], 0
    if cur:
        chunks.append("".join(cur))
    return chunks


def translate_text(
    content: str, config: Config, prompt: str | None = None, *, split: bool = True
) -> str:
    prompt = prompt if prompt is not None else load_prompt()
    system = prompt + _ANNOTATION_FORMAT
    chunks = split_chunks(content) if split else [content]
    return "".join(
        _with_retries(_translate_chunk, chunk, config, system)
        for chunk in chunks
    )


def _is_retryable(exc: BaseException) -> bool:
    retryable = (
        TimeoutError,
        subprocess.TimeoutExpired,
        subprocess.CalledProcessError,
        OSError,
    )
    if isinstance(exc, retryable):
        return True
    name = exc.__class__.__name__.lower()
    return "timeout" in name or "connection" in name or "network" in name


def _with_retries(
    func: Callable[[str, Config, str], str],
    chunk: str,
    config: Config,
    prompt: str,
    *,
    sleep: Callable[[float], None] = time.sleep,
) -> str:
    last_error: BaseException | None = None
    delay = int(config.get("TRANSLATION_RETRY_DELAY", str(RETRY_DELAY_SECONDS)))

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return func(chunk, config, prompt)
        except Exception as exc:
            if not _is_retryable(exc):
                raise
            last_error = exc
            if attempt < MAX_ATTEMPTS:
                sleep(delay)

    raise IncompleteTranslation(str(last_error)) from last_error


def _translate_chunk(chunk: str, config: Config, prompt: str) -> str:
    if config.provider == "cli":
        return _translate_cli(chunk, config, prompt)
    return _translate_openai(chunk, config, prompt)


def _translate_cli(chunk: str, config: Config, prompt: str) -> str:
    command = config.get("TRANSLATION_CLI_COMMAND")
    timeout = int(config.get("TRANSLATION_CLI_TIMEOUT", "1800"))
    payload = f"{prompt}\n\n# 번역할 Markdown\n\n{chunk}"
    result = subprocess.run(
        command,
        shell=True,
        input=payload,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )
    return result.stdout


def _translate_openai(chunk: str, config: Config, prompt: str) -> str:
    if config.provider == "azure":
        from openai import AzureOpenAI

        client = AzureOpenAI(
            api_key=config.get("AZURE_OPENAI_API_KEY"),
            api_version=config.get("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=config.get("AZURE_OPENAI_ENDPOINT"),
        )
    else:
        from openai import OpenAI

        client = OpenAI(api_key=config.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model=config.get("TRANSLATION_MODEL"),
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": chunk},
        ],
    )
    return response.choices[0].message.content or ""
