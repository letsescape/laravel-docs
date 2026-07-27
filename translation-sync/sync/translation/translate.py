"""번역 (provider 호출). translation-sync/docs/02.

호출자가 전달한 locale별 운영 프롬프트를 시스템 프롬프트로 사용한다.
청크 분할은 라인 수를 기준으로 하되 fenced code block은 중간에서 끊지 않는다(workflow).
provider: openai | azure | cli.
"""
from __future__ import annotations

import os
import re
import shlex
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from ..common.markdown import closes_fence, fence_token
from ..runtime.config import Config

REPO_ROOT = Path(__file__).resolve().parents[3]
PROMPT_PATH = REPO_ROOT / "translation-sync" / "prompt.md"
MAX_CHUNK_LINES = 400
MAX_ATTEMPTS = 3
MAX_COMPLETED_RESPONSE_ATTEMPTS = 2
RETRY_DELAY_SECONDS = 300
_CLI_DISABLED_FEATURES = (
    "apps",
    "browser_use",
    "browser_use_external",
    "browser_use_full_cdp_access",
    "computer_use",
    "hooks",
    "image_generation",
    "in_app_browser",
    "multi_agent",
    "plugins",
    "plugin_sharing",
    "remote_plugin",
    "shell_snapshot",
    "shell_tool",
    "tool_suggest",
    "unified_exec",
    "workspace_dependencies",
)
_CLI_ENVIRONMENT_KEYS = (
    "PATH",
    "HOME",
    "USERPROFILE",
    "SYSTEMROOT",
    "WINDIR",
    "COMSPEC",
    "PATHEXT",
    "LOCALAPPDATA",
    "APPDATA",
    "TMPDIR",
    "TMP",
    "TEMP",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "CODEX_HOME",
    "CODEX_ACCESS_TOKEN",
    "OPENAI_API_KEY",
    "CODEX_API_KEY",
    "OPENAI_BASE_URL",
    "OPENAI_ORGANIZATION",
    "OPENAI_PROJECT",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "NO_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
    "no_proxy",
    "SSL_CERT_FILE",
    "SSL_CERT_DIR",
    "REQUESTS_CA_BUNDLE",
    "CURL_CA_BUNDLE",
    "NODE_EXTRA_CA_CERTS",
)
_SENSITIVE_ENVIRONMENT_KEYS = (
    "OPENAI_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "CODEX_ACCESS_TOKEN",
    "CODEX_API_KEY",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
)
_CLI_RETRYABLE_STATUS_RE = re.compile(
    r"(?:^|\n)\s*(?:429|5\d{2})(?:\s|$)"
    r"|\b(?:"
    r"http(?:\s+status)?|status(?:\s+code)?|response\s+status"
    r"|(?:api\s+)?error|upstream\s+returned"
    r"|(?:codex|command|process|provider)\s+exited"
    r")"
    r"\s*[:=]?\s*(?:429|5\d{2})\b",
    re.IGNORECASE,
)
_CLI_RETRYABLE_TRANSPORT_RE = re.compile(
    r"\b(?:"
    r"connection (?:aborted|closed|error|failed|refused|reset)"
    r"|network (?:error|failure|is unreachable|unreachable)"
    r"|stream disconnected"
    r"|error sending request"
    r"|could not resolve host"
    r"|(?:temporary failure in )?name resolution"
    r"|dns error"
    r"|lookup address information"
    r"|rate limit(?:ed)?"
    r"|temporarily unavailable"
    r"|(?:request|operation|connection) (?:timed out|timeout)"
    r"|context deadline exceeded"
    r"|timed out"
    r"|timeout"
    r")\b",
    re.IGNORECASE,
)


class IncompleteTranslation(Exception):
    """provider 재시도 초과로 완료하지 못한 chunk."""


def verification_feedback(issues: list[str]) -> str:
    """Return the bounded correction instruction for one completed response."""
    return (
        f"The previous output failed verification: {', '.join(issues)}.\n"
        "Translate the English Source again. Preserve every Markdown link label "
        "and target, heading, anchor, inline code span, fenced code block, and "
        "list marker exactly as it appears in the English Source. Include the "
        "English source comments required by the existing annotated format."
    )


@dataclass(frozen=True)
class TranslationRequest:
    """Structured source block request shared by live and local adapters."""

    source: str
    existing_translation: str | None
    diff_text: str | None = None
    verification_feedback: str | None = None

    def render(self) -> str:
        existing = (
            self.existing_translation.rstrip()
            if self.existing_translation
            else "(none)"
        )
        diff_section = (
            "## English Diff\n\n"
            f"{_fenced_payload(self.diff_text, 'diff')}\n\n"
            if self.diff_text
            else ""
        )
        feedback_section = (
            "## Previous Output Verification Failure\n\n"
            f"{self.verification_feedback.rstrip()}\n\n"
            if self.verification_feedback
            else ""
        )
        return (
            "# Translation Sync Input\n\n"
            f"{diff_section}"
            "## English Source\n\n"
            f"{self.source.rstrip()}\n\n"
            "## Existing Translation Context\n\n"
            f"{existing}\n\n"
            f"{feedback_section}"
            "## Output\n\n"
            "Return only the translated Markdown block(s) for the English Source."
        )


def _fenced_payload(text: str, language: str) -> str:
    longest = 0
    current = 0
    for char in text:
        if char == "`":
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    fence = "`" * max(3, longest + 1)
    return f"{fence}{language}\n{text.rstrip()}\n{fence}"


# 영어 원문 주석 병기 형식 (docs/02·05 T2, versioned_docs 레퍼런스).
# Locale별 제목 병기 규칙과 공존한다.
_ANNOTATION_FORMAT = """

## Output Format (Required)

Add the original English source as HTML comments in the translated output. For
each translated heading and paragraph, place the corresponding English source on
the line immediately above it as a one-line HTML comment.

Example:
<!-- # Section Title -->
# Section Title

<!-- English paragraph text on one line. -->
Translated paragraph in the target language.

Rules:
- Collapse line breaks inside English comments into spaces so each comment stays
  on one line.
- Within an English source comment, escape literal `-->` as `--&gt;` so it
  cannot terminate the HTML comment early.
- Render each translated prose paragraph on one physical line. If the English
  paragraph contains explicit Markdown hard breaks, preserve exactly those hard
  breaks and do not add other body lines.
- Keep headings exactly as written in the English source and add the English
  source comment above the heading, including its complete Markdown marker
  (`#`, `##`, `###`, and so on) inside the comment.
- Keep `<a name="..."></a>` anchors in their original position without adding
  comments for them.
- Do not add English source comments to TOC link lists.
- Do not add English source comments to blockquoted prose. Preserve the quote
  markers and translate only the quoted prose.
- Preserve lists made entirely of inline-code identifiers exactly, without
  translating or annotating them.
- Keep fenced code blocks unchanged. Do not translate or annotate them.
"""


def load_prompt() -> str:
    return PROMPT_PATH.read_text("utf-8")


def effective_prompt(prompt: str) -> str:
    return prompt + _ANNOTATION_FORMAT


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
    system = effective_prompt(prompt)
    chunks = split_chunks(content) if split else [content]
    translated = [
        _with_retries(_translate_chunk, chunk, config, system)
        for chunk in chunks
    ]
    if not split:
        return "".join(translated)
    return join_chunk_outputs(chunks, translated)


def join_chunk_outputs(source_chunks: list[str], translated_chunks: list[str]) -> str:
    return "".join(
        _preserve_source_ending(source, translated)
        for source, translated in zip(source_chunks, translated_chunks, strict=True)
    )


def _preserve_source_ending(source: str, translated: str) -> str:
    trailing = source[len(source.rstrip("\r\n")) :]
    return translated.rstrip("\r\n") + trailing


def translate_request(
    request: TranslationRequest,
    config: Config,
    prompt: str | None = None,
) -> str:
    """Translate one structured block, or echo its source for local replay."""

    if config.provider == "identity":
        return request.source
    return translate_text(request.render(), config, prompt, split=False)


def _is_retryable(exc: BaseException) -> bool:
    if isinstance(exc, (FileNotFoundError, PermissionError)):
        return False
    if isinstance(exc, subprocess.CalledProcessError):
        detail = f"{exc.stderr or ''}\n{exc.stdout or ''}"
        return bool(
            _CLI_RETRYABLE_STATUS_RE.search(detail)
            or _CLI_RETRYABLE_TRANSPORT_RE.search(detail)
        )
    retryable = (
        TimeoutError,
        subprocess.TimeoutExpired,
        ConnectionError,
    )
    if isinstance(exc, retryable):
        return True
    status_code = getattr(exc, "status_code", None)
    if isinstance(status_code, int) and (
        status_code == 429 or 500 <= status_code < 600
    ):
        return True
    name = exc.__class__.__name__.lower()
    return "timeout" in name or "connection" in name or "network" in name


def _provider_error_message(exc: BaseException) -> str:
    if isinstance(exc, subprocess.CalledProcessError):
        detail = (exc.stderr or exc.stdout or "").strip()
        suffix = f": {detail}" if detail else ""
        message = f"provider command exited {exc.returncode}{suffix}"
    else:
        message = str(exc)
    for key in _SENSITIVE_ENVIRONMENT_KEYS:
        value = os.environ.get(key)
        if value:
            for candidate in (value, value.strip()):
                if candidate:
                    message = message.replace(candidate, f"[REDACTED:{key}]")
    return message


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
            result = func(chunk, config, prompt)
        except Exception as exc:
            if not _is_retryable(exc):
                raise IncompleteTranslation(_provider_error_message(exc)) from exc
            last_error = exc
        else:
            if result.strip():
                return result
            last_error = IncompleteTranslation("empty provider response")
        if attempt < MAX_ATTEMPTS:
            sleep(delay)

    raise IncompleteTranslation(_provider_error_message(last_error)) from last_error


def _translate_chunk(chunk: str, config: Config, prompt: str) -> str:
    if config.provider == "cli":
        return _translate_cli(chunk, config, prompt)
    return _translate_openai(chunk, config, prompt)


def _cli_environment() -> dict[str, str]:
    environment = {
        key: os.environ[key]
        for key in _CLI_ENVIRONMENT_KEYS
        if key in os.environ
    }
    codex_home = environment.get("CODEX_HOME")
    home = environment.get("HOME") or environment.get("USERPROFILE")
    codex_home_path = (
        Path(codex_home).expanduser()
        if codex_home
        else Path(home).expanduser() / ".codex"
        if home
        else None
    )
    if codex_home_path is not None:
        dotenv = codex_home_path / ".env"
        if dotenv.exists() or dotenv.is_symlink():
            raise RuntimeError(
                "refusing CLI provider because CODEX_HOME/.env bypasses the "
                "process environment allowlist; use a dedicated CODEX_HOME "
                "without .env"
            )
    return environment


def _translate_cli(chunk: str, config: Config, prompt: str) -> str:
    command = shlex.split(config.get("TRANSLATION_CLI_COMMAND"))
    timeout = int(config.get("TRANSLATION_CLI_TIMEOUT", "1800"))
    model = config.get("TRANSLATION_MODEL")
    reasoning_effort = config.get("TRANSLATION_REASONING_EFFORT", "medium")
    disabled_features = [
        argument
        for feature in _CLI_DISABLED_FEATURES
        for argument in ("--disable", feature)
    ]
    with tempfile.TemporaryDirectory(prefix="translation-cli-") as tmp:
        output_path = Path(tmp) / "last-message.md"
        subprocess.run(
            [
                *command,
                "--ignore-user-config",
                "--ignore-rules",
                "--ephemeral",
                "--strict-config",
                *disabled_features,
                "--model",
                model,
                "-c",
                f'model_reasoning_effort="{reasoning_effort}"',
                "-c",
                "project_doc_max_bytes=0",
                "-c",
                'web_search="disabled"',
                "-c",
                'shell_environment_policy.inherit="none"',
                "-c",
                "allow_login_shell=false",
                "--sandbox",
                "read-only",
                "--skip-git-repo-check",
                "--output-last-message",
                str(output_path),
                prompt,
            ],
            cwd=tmp,
            input=chunk,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True,
            env=_cli_environment(),
        )
        return output_path.read_text(encoding="utf-8") if output_path.exists() else ""


def _translate_openai(chunk: str, config: Config, prompt: str) -> str:
    if config.provider == "azure":
        from openai import AzureOpenAI

        client = AzureOpenAI(
            api_key=config.get("AZURE_OPENAI_API_KEY"),
            api_version=config.get("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=config.get("AZURE_OPENAI_ENDPOINT"),
            max_retries=0,
        )
        response = client.chat.completions.create(
            model=config.get("TRANSLATION_MODEL"),
            reasoning_effort=config.get(
                "TRANSLATION_REASONING_EFFORT", "medium"
            ),
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": chunk},
            ],
        )
        choice = response.choices[0]
        if choice.finish_reason != "stop":
            raise IncompleteTranslation(
                f"Azure response finish_reason={choice.finish_reason!r}"
            )
        return choice.message.content or ""
    else:
        from openai import OpenAI

        client = OpenAI(api_key=config.get("OPENAI_API_KEY"), max_retries=0)
    response = client.responses.create(
        model=config.get("TRANSLATION_MODEL"),
        instructions=prompt,
        input=chunk,
        reasoning={
            "effort": config.get("TRANSLATION_REASONING_EFFORT", "medium")
        },
        store=False,
    )
    if response.status != "completed":
        details = getattr(response, "incomplete_details", None)
        reason = getattr(details, "reason", None)
        suffix = f": {reason}" if reason else ""
        raise IncompleteTranslation(
            f"OpenAI response status={response.status!r}{suffix}"
        )
    return response.output_text or ""
