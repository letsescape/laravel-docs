"""PatchPlan owner 단위의 번역 provider 호출과 제한된 재시도.

호출자가 전달한 locale별 운영 prompt를 system prompt로 사용.
PatchPlan에서 확정한 atomic owner block을 분할하지 않는 요청.
provider: openai | azure | cli.
"""
from __future__ import annotations

import math
import os
import re
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import tiktoken

from ..common.versions import validate_version_token
from ..runtime.config import (
    Config,
    ConfigError,
    OPENAI_API_BASE_URL,
    PROVIDER_FRAMING_OVERHEAD_TOKENS,
    RequestBudget,
    cli_auth_environment,
    validate_cli_command,
)
from ..runtime.failure import IssueCode
from ..runtime.process import ProcessTreeError, run_process_tree
from ..verification.response_contract import RESPONSE_CONTRACT_VERSION

REPO_ROOT = Path(__file__).resolve().parents[3]
PROMPT_PATH = REPO_ROOT / "translation-sync" / "prompt.md"
MAX_CHUNK_LINES = 400
MAX_ATTEMPTS = 5
MAX_COMPLETED_RESPONSE_ATTEMPTS = 5
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
_CLI_RUNTIME_ENVIRONMENT_KEYS = (
    "PATH",
    "SYSTEMROOT",
    "WINDIR",
    "COMSPEC",
    "PATHEXT",
    "TMPDIR",
    "TMP",
    "TEMP",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
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


class ProviderTransientExhausted(IncompleteTranslation):
    """일시적 transport 실패로 물리 재시도 예산이 소진된 오류."""


class ProviderRequestRejected(IncompleteTranslation):
    """설정된 provider가 안전한 응답 없이 요청을 거부한 오류."""


class CliProviderFailed(IncompleteTranslation):
    """capture한 출력을 노출하지 않는 로컬 CLI provider 실패 오류."""


class ProviderPartialResponse(IncompleteTranslation):
    """사용 가능한 완전한 응답 없이 완료된 provider 오류."""


class UnsupportedOversizeBlock(IncompleteTranslation):
    """설정된 요청 예산에 들어가지 않는 atomic owner block 오류."""


class RunDeadlineExceeded(IncompleteTranslation):
    """다음 transport 작업을 실행 기한 내 완료할 수 없는 오류."""


@dataclass
class ProviderAttemptCounter:
    """단일 fixture 또는 문서에서 수행한 provider 시도 횟수."""

    transport: int = 0
    response_evaluation: int = 0

    def record_transport(self) -> None:
        """물리 provider adapter 호출 횟수 증가."""

        self.transport += 1

    def record_response_evaluation(self) -> None:
        """완료된 provider 응답의 계약 평가 횟수 증가."""

        self.response_evaluation += 1


_FEEDBACK_COMMENT_BUDGET = 2000


def _bounded_comment_snippets(comments: list[str] | None) -> str:
    """재시도 지침에 붙일 주석을 고정 예산 안에서 결정적으로 자른다."""

    if not comments:
        return ""
    snippets: list[str] = []
    remaining = _FEEDBACK_COMMENT_BUDGET
    for comment in comments[:2]:
        rendered = f"<!-- {comment} -->"
        if len(rendered) > remaining:
            break
        snippets.append(rendered)
        remaining -= len(rendered)
    return " ".join(snippets)


def verification_feedback(
    issues: list[str],
    exact_comments: list[str] | None = None,
    echoed_cells: list[str] | None = None,
) -> str:
    """완료된 단일 응답에 대한 길이가 제한된 교정 지침."""
    guidance = (
        "Translate the English Source again. Preserve every Markdown link label "
        "and target, heading, anchor, inline code span, fenced code block, and "
        "list marker exactly as it appears in the English Source. Include the "
        "English source comments required by the existing annotated format."
    )
    if any("link" in issue for issue in issues):
        guidance += (
            " Copy every Markdown link verbatim from the English Source: the "
            "display text between [ and ] must stay in English, untranslated."
        )
    if any("inline code" in issue for issue in issues):
        guidance += (
            " Use each inline code span exactly as many times as it appears "
            "in the English Source: do not repeat, drop, or invent `code` spans."
        )
    if any("target language mismatch" in issue for issue in issues):
        guidance += (
            " Translate the prose into the target language; keep only code, "
            "identifiers, link labels and product names in English."
        )
        if echoed_cells:
            named = ", ".join(f"`{cell}`" for cell in echoed_cells[:8])
            guidance += (
                f" These table header cells came back untranslated: {named}. "
                "Translate each of them."
            )
    if any("inline markup" in issue for issue in issues):
        guidance += (
            " Do not add emphasis that the English Source does not have."
        )
    if any("block signature" in issue for issue in issues):
        guidance += (
            " Return the complete English Source: translate every line of "
            "the English Source section, not only the lines highlighted in "
            "the English Diff."
        )
    if any("admonition" in issue for issue in issues):
        guidance += (
            " Keep every admonition at the same level as the English Source: "
            "translate a Note marker as a note and a Warning marker as a "
            "warning, without changing the admonition type."
        )
    if any("original comment" in issue for issue in issues):
        guidance += (
            " Reproduce each English source comment character-for-character "
            "from the English Source: do not rephrase or change punctuation "
            "inside comments."
        )
        quoted = _bounded_comment_snippets(exact_comments)
        if quoted:
            guidance += (
                " The following comments must appear exactly as written here: "
                + quoted
            )
    return (
        f"The previous output failed verification: {', '.join(issues)}.\n"
        + guidance
    )


@dataclass(frozen=True)
class TranslationRequest:
    """live 및 local adapter가 공유하는 구조화된 원문 block 요청."""

    source: str
    existing_translation: str | None
    diff_text: str | None = None
    verification_feedback: str | None = None
    version: str | None = None
    response_contract_version: int = RESPONSE_CONTRACT_VERSION

    def render(self) -> str:
        """source·기존 문맥·diff·feedback을 단일 provider 입력으로 렌더링."""

        existing = (
            self.existing_translation
            if self.existing_translation is not None
            else "(none)"
        )
        diff_section = (
            _request_section(
                "English Diff",
                _fenced_payload(self.diff_text, "diff"),
            )
            if self.diff_text is not None
            else ""
        )
        feedback_section = (
            _request_section(
                "Previous Output Verification Failure",
                self.verification_feedback,
            )
            if self.verification_feedback is not None
            else ""
        )
        return (
            "# Translation Sync Input\n\n"
            f"{diff_section}"
            f"{_request_section('English Source', self.source)}"
            f"{_request_section('Existing Translation Context', existing)}"
            f"{feedback_section}"
            "## Output\n\n"
            "Return only the translated Markdown block(s) for the English Source."
        )


def _request_section(title: str, payload: str) -> str:
    """payload의 끝 줄바꿈을 보존한 provider 요청 section 생성."""

    separator = "" if payload.endswith("\n") else "\n"
    return f"## {title}\n\n{payload}{separator}\n"


def _fenced_payload(text: str, language: str) -> str:
    """본문의 backtick보다 긴 fence로 요청 payload 감싸기."""

    longest = 0
    current = 0
    for char in text:
        if char == "`":
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    fence = "`" * max(3, longest + 1)
    separator = "" if text.endswith("\n") else "\n"
    return f"{fence}{language}\n{text}{separator}{fence}"


# provider 응답이 각 번역 heading과 paragraph 바로 위에 보존할 원문 주석 형식.
# Locale별 제목 병기 규칙과 공존.
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
- Treat each consecutive Markdown list as one unit: place one English source
  comment containing the whole list collapsed to one line immediately above the
  first translated item, keep the translated items consecutive, and do not add
  blank lines or per-item comments between them.
- Do not add English source comments to TOC link lists.
- Do not add English source comments to blockquoted prose. Preserve the quote
  markers and translate only the quoted prose.
- Preserve lists made entirely of inline-code identifiers exactly, without
  translating or annotating them.
- Keep fenced code blocks unchanged. Do not translate or annotate them.
"""


def load_prompt() -> str:
    """기본 한국어 운영 프롬프트 로드."""

    return PROMPT_PATH.read_text("utf-8")


def effective_prompt(prompt: str) -> str:
    """locale 운영 프롬프트에 공통 annotation 출력 계약 결합."""

    return prompt + _ANNOTATION_FORMAT


def split_chunks(content: str, max_lines: int = MAX_CHUNK_LINES) -> list[str]:
    """호출자가 제공한 atomic owner를 단일 provider 요청으로 보존.

    ``max_lines``는 이전 호출자와의 호환성만을 위해 유지.
    문서 분해는 PatchPlan 생성 단계가 소유하며 provider 경계에서 물리 줄 수 기반의 안전한 분할 추론은 금지.
    """

    del max_lines
    return [content] if content else []


def translate_text(
    content: str,
    config: Config,
    prompt: str | None = None,
    *,
    split: bool = True,
    deadline: float | None = None,
    clock: Callable[[], float] = time.monotonic,
    attempt_counter: ProviderAttemptCounter | None = None,
) -> str:
    """고정 실행 기한과 요청 예산 안에서 atomic text를 번역."""

    prompt = prompt if prompt is not None else load_prompt()
    system = effective_prompt(prompt)
    if config.provider not in {"openai", "azure", "cli"}:
        raise ConfigError(
            f"invalid live provider {config.provider!r}",
            IssueCode.PROVIDER_SELECTION_INVALID,
        )
    budget = config.request_budget()
    if budget is None:
        raise ConfigError(
            "INVALID_REQUEST_BUDGET: live provider request budget is required",
            IssueCode.INVALID_REQUEST_BUDGET,
        )
    if deadline is None or not math.isfinite(deadline):
        raise RunDeadlineExceeded(
            "RUN_DEADLINE_EXCEEDED: an injected absolute deadline is required "
            "for every live provider request"
        )
    chunks = split_chunks(content) if split else [content]
    for chunk in chunks:
        _validate_request_budget(system, chunk, config)
    translated = [
        _with_retries(
            _translate_chunk,
            chunk,
            config,
            system,
            deadline=deadline,
            clock=clock,
            attempt_counter=attempt_counter,
        )
        for chunk in chunks
    ]
    if not split:
        return "".join(translated)
    return join_chunk_outputs(chunks, translated)


def _validate_request_budget(instructions: str, payload: str, config: Config) -> int:
    """요청 예산 검증."""

    budget = config.request_budget()
    if budget is None:
        raise ConfigError(
            "INVALID_REQUEST_BUDGET: live provider request budget is required",
            IssueCode.INVALID_REQUEST_BUDGET,
        )
    try:
        exact_input_tokens = _count_tokens(
            instructions, budget.tokenizer_encoding
        ) + _count_tokens(payload, budget.tokenizer_encoding)
    except Exception as exc:
        raise ConfigError(
            "TOKENIZER_METADATA_UNAVAILABLE: tokenizer could not be loaded "
            f"{budget.tokenizer_encoding!r}",
            IssueCode.TOKENIZER_METADATA_UNAVAILABLE,
        ) from exc
    utf8_byte_upper_bound = len((instructions + payload).encode("utf-8"))
    input_tokens = max(
        exact_input_tokens + PROVIDER_FRAMING_OVERHEAD_TOKENS,
        utf8_byte_upper_bound + PROVIDER_FRAMING_OVERHEAD_TOKENS,
    )
    if input_tokens + budget.reserved_output_tokens > budget.context_window_tokens:
        raise UnsupportedOversizeBlock(
            "UNSUPPORTED_OVERSIZE_BLOCK: atomic request conservatively requires "
            f"{input_tokens} input tokens including provider framing plus "
            f"{budget.reserved_output_tokens} reserved output tokens, exceeding "
            f"the {budget.context_window_tokens}-token context window"
        )
    return input_tokens


def _count_tokens(text: str, encoding_name: str) -> int:
    """지정 tokenizer encoding으로 text의 정확한 token 수 계산."""

    return len(
        tiktoken.get_encoding(encoding_name).encode(
            text,
            disallowed_special=(),
        )
    )


def _require_response_contract_version(request: TranslationRequest) -> None:
    """요청의 응답 계약 버전 지원 여부 검증."""

    if request.response_contract_version != RESPONSE_CONTRACT_VERSION:
        raise ProviderRequestRejected(
            "unsupported response contract version: "
            f"{request.response_contract_version}"
        )


def preflight_request(
    request: TranslationRequest,
    config: Config,
    prompt: str | None = None,
) -> None:
    """provider 호출 없는 단일 완전 논리 요청 검증."""

    _require_response_contract_version(request)
    if config.provider == "identity":
        return
    if config.provider not in {"openai", "azure", "cli"}:
        raise ConfigError(
            f"invalid live provider {config.provider!r}",
            IssueCode.PROVIDER_SELECTION_INVALID,
        )
    budget = config.request_budget()
    if budget is None:
        return
    instructions = effective_prompt(prompt if prompt is not None else load_prompt())
    _validate_request_budget(instructions, request.render(), config)


def join_chunk_outputs(source_chunks: list[str], translated_chunks: list[str]) -> str:
    """source별 줄바꿈 끝을 복원하며 번역 chunk 결합."""

    return "".join(
        _preserve_source_ending(source, translated)
        for source, translated in zip(source_chunks, translated_chunks, strict=True)
    )


def _preserve_source_ending(source: str, translated: str) -> str:
    """번역 결과의 끝 줄바꿈을 source와 동일하게 복원."""

    trailing = source[len(source.rstrip("\r\n")) :]
    return translated.rstrip("\r\n") + trailing


def translate_request(
    request: TranslationRequest,
    config: Config,
    prompt: str | None = None,
    *,
    deadline: float | None = None,
    clock: Callable[[], float] = time.monotonic,
    attempt_counter: ProviderAttemptCounter | None = None,
) -> str:
    """단일 구조화 block의 번역 또는 canonical replay 형태 렌더링."""

    _require_response_contract_version(request)
    if config.provider == "identity":
        if request.version is None:
            raise ProviderRequestRejected(
                "identity request is missing version metadata"
            )
        try:
            validate_version_token(request.version)
            from ..verification.response_contract import (
                render_identity_response,
            )

            return render_identity_response(request.source, request.version)
        except (TypeError, ValueError):
            raise ProviderRequestRejected(
                "identity response could not be rendered canonically"
            ) from None
    counter_arguments = (
        {"attempt_counter": attempt_counter}
        if attempt_counter is not None
        else {}
    )
    if deadline is None and clock is time.monotonic:
        return translate_text(
            request.render(),
            config,
            prompt,
            split=False,
            **counter_arguments,
        )
    return translate_text(
        request.render(),
        config,
        prompt,
        split=False,
        deadline=deadline,
        clock=clock,
        **counter_arguments,
    )


def start_translation_deadline(
    config: Config,
    workflow_deadline: float,
    *,
    clock: Callable[[], float] = time.monotonic,
) -> float:
    """첫 live fixture 시점의 단일 번역 실행 기한 시작."""

    budget = config.request_budget()
    if budget is None:
        raise ConfigError(
            "INVALID_REQUEST_BUDGET: request budget is required",
            IssueCode.INVALID_REQUEST_BUDGET,
        )
    return min(workflow_deadline, clock() + budget.run_timeout_seconds)


def _is_retryable(exc: BaseException) -> bool:
    """provider 오류가 제한된 transport 재시도 대상인지 판별."""

    if isinstance(exc, ProcessTreeError):
        return False
    if isinstance(exc, (FileNotFoundError, PermissionError)):
        return False
    if isinstance(exc, subprocess.CalledProcessError):
        detail = "\n".join(
            value
            for value in (exc.stderr, exc.stdout)
            if isinstance(value, str)
        )
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
    try:
        status_code = getattr(exc, "status_code", None)
    except Exception:
        return False
    if isinstance(status_code, int) and (
        status_code == 429 or 500 <= status_code < 600
    ):
        return True
    name = exc.__class__.__name__.lower()
    return "timeout" in name or "connection" in name or "network" in name


def _provider_error_message(exc: BaseException) -> str:
    """길이가 제한된 metadata만 반환하고 provider 제어 텍스트 렌더링은 금지."""

    if isinstance(exc, subprocess.CalledProcessError):
        return_code = (
            str(exc.returncode)
            if isinstance(exc.returncode, int) and not isinstance(exc.returncode, bool)
            else "unknown"
        )
        return f"provider command failed (exit_code={return_code})"
    if isinstance(exc, (TimeoutError, subprocess.TimeoutExpired)):
        return "provider request timed out"
    if isinstance(exc, ProcessTreeError):
        return "provider process isolation failed"
    if isinstance(exc, FileNotFoundError):
        return "provider command is unavailable"
    if isinstance(exc, PermissionError):
        return "provider command is not executable"
    try:
        status_code = getattr(exc, "status_code", None)
    except Exception:
        status_code = None
    if (
        isinstance(status_code, int)
        and not isinstance(status_code, bool)
        and 100 <= status_code <= 599
    ):
        return f"provider request failed (http_status={status_code})"
    return "provider request failed"


def _transport_attempt(
    func: Callable[[str, Config, str], str],
    chunk: str,
    config: Config,
    prompt: str,
    *,
    deadline: float | None,
    clock: Callable[[], float],
    attempt_counter: ProviderAttemptCounter | None,
) -> tuple[str | None, BaseException | None]:
    """provider 전송 한 번을 실행하고 재시도 가능한 실패를 값으로 반환.

    Args:
        func: provider 호출 함수.
        chunk: 번역 요청 본문.
        config: 검증된 provider 설정.
        prompt: 번역 system prompt.
        deadline: 전체 번역 실행 기한.
        clock: 단조 시계 함수.
        attempt_counter: 전송 시도 횟수 기록기.

    Returns:
        성공 응답과 재시도 가능한 마지막 오류.
    """

    try:
        if attempt_counter is not None:
            attempt_counter.record_transport()
        result = func(chunk, config, prompt)
    except Exception as exc:
        if isinstance(exc, ProviderPartialResponse):
            raise
        if _is_retryable(exc):
            return None, exc
        error_type = (
            CliProviderFailed if config.provider == "cli" else ProviderRequestRejected
        )
        raise error_type(_provider_error_message(exc)) from None
    require_run_deadline(deadline, clock=clock)
    if result.strip():
        return result, None
    return None, ProviderPartialResponse("provider response was empty")


def _with_retries(
    func: Callable[[str, Config, str], str],
    chunk: str,
    config: Config,
    prompt: str,
    *,
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
    deadline: float | None = None,
    attempt_counter: ProviderAttemptCounter | None = None,
) -> str:
    """공유 기한과 transport 상한 안에서 provider 호출 재시도."""

    last_error: BaseException | None = None
    delay = RETRY_DELAY_SECONDS
    request_timeout = _request_timeout_seconds(config)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        _require_deadline_budget(deadline, request_timeout, clock())
        result, last_error = _transport_attempt(
            func,
            chunk,
            config,
            prompt,
            deadline=deadline,
            clock=clock,
            attempt_counter=attempt_counter,
        )
        if result is not None:
            return result
        if attempt < MAX_ATTEMPTS:
            _require_deadline_budget(
                deadline,
                delay + request_timeout,
                clock(),
            )
            sleep(delay)

    if isinstance(last_error, ProviderPartialResponse):
        raise ProviderTransientExhausted(
            "provider returned an empty response on every transport attempt"
        ) from None
    if last_error is None:
        raise ProviderTransientExhausted("provider request failed") from None
    raise ProviderTransientExhausted(
        _provider_error_message(last_error)
    ) from None


def _request_timeout_seconds(config: Config) -> int:
    """검증된 요청 예산 또는 CLI 설정에서 단일 호출 timeout 반환."""

    budget = config.request_budget()
    if budget is not None:
        return budget.request_timeout_seconds
    return int(config.get("TRANSLATION_CLI_TIMEOUT", "1800"))


def _require_deadline_budget(
    deadline: float | None,
    required_seconds: int,
    now: float,
) -> None:
    """다음 provider 작업에 필요한 실행 기한 잔여 예산 검증."""

    if deadline is not None and deadline - now < required_seconds:
        raise RunDeadlineExceeded(
            "RUN_DEADLINE_EXCEEDED: insufficient time remains for the next "
            "provider operation"
        )


def require_run_deadline(
    deadline: float | None,
    *,
    clock: Callable[[], float] = time.monotonic,
) -> None:
    """번역 실행 기한 초과 여부 검증."""

    if deadline is not None and clock() >= deadline:
        raise RunDeadlineExceeded(
            "RUN_DEADLINE_EXCEEDED: translation run deadline was exceeded"
        )


def _translate_chunk(chunk: str, config: Config, prompt: str) -> str:
    """설정된 CLI 또는 API adapter로 atomic chunk 전달."""

    if config.provider == "cli":
        return _translate_cli(chunk, config, prompt)
    return _translate_openai(chunk, config, prompt)


def _cli_environment(config: Config, isolated_home: Path) -> dict[str, str]:
    """격리 HOME과 허용된 인증·통신 변수만 가진 CLI 환경 구성."""

    environment = {
        key: os.environ[key]
        for key in _CLI_RUNTIME_ENVIRONMENT_KEYS
        if key in os.environ
    }
    isolated_home.mkdir(mode=0o700)
    environment.update(
        {
            "HOME": str(isolated_home),
            "USERPROFILE": str(isolated_home),
            "XDG_CONFIG_HOME": str(isolated_home / ".config"),
            "XDG_CACHE_HOME": str(isolated_home / ".cache"),
        }
    )
    auth = cli_auth_environment(config)
    codex_home = auth.get("CODEX_HOME")
    if codex_home is None:
        isolated_codex_home = isolated_home / ".codex"
        isolated_codex_home.mkdir(mode=0o700)
        environment["CODEX_HOME"] = str(isolated_codex_home)
    else:
        dotenv = Path(codex_home) / ".env"
        if dotenv.exists() or dotenv.is_symlink():
            raise RuntimeError(
                "refusing CLI provider because CODEX_HOME/.env bypasses the "
                "process environment allowlist; use a dedicated CODEX_HOME "
                "without .env"
            )
    environment.update(auth)
    return environment


def _translate_cli(chunk: str, config: Config, prompt: str) -> str:
    """도구·사용자 설정을 차단한 일회성 sandbox에서 CLI provider 실행."""

    command = validate_cli_command(config.get("TRANSLATION_CLI_COMMAND"))
    timeout = _request_timeout_seconds(config)
    model = config.get("TRANSLATION_MODEL")
    reasoning_effort = config.get("TRANSLATION_REASONING_EFFORT", "medium")
    disabled_features = [
        argument
        for feature in _CLI_DISABLED_FEATURES
        for argument in ("--disable", feature)
    ]
    with tempfile.TemporaryDirectory(prefix="translation-cli-") as tmp:
        output_path = Path(tmp) / "last-message.md"
        isolated_home = Path(tmp) / "home"
        run_process_tree(
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
            env=_cli_environment(config, isolated_home),
        )
        return output_path.read_text(encoding="utf-8") if output_path.exists() else ""


def _known_provider_status(value: object, allowed: set[str]) -> str:
    """provider 상태값을 허용 목록 또는 ``unknown``으로 제한.

    Args:
        value: SDK가 반환한 상태값.
        allowed: 진단에 노출할 수 있는 상태 문자열 집합.

    Returns:
        허용된 상태 또는 ``unknown``.
    """

    return value if isinstance(value, str) and value in allowed else "unknown"


def _translate_azure(
    chunk: str,
    config: Config,
    prompt: str,
    *,
    client_runtime: dict[str, object],
    budget: RequestBudget | None,
) -> str:
    """Azure chat completions adapter로 단일 번역 요청 실행.

    Args:
        chunk: 번역 요청 본문.
        config: 검증된 provider 설정.
        prompt: 번역 system prompt.
        client_runtime: SDK 재시도·timeout 설정.
        budget: 검증된 요청 예산.

    Returns:
        완료된 번역 응답 본문.
    """

    from openai import AzureOpenAI

    client = AzureOpenAI(
        api_key=config.get("AZURE_OPENAI_API_KEY"),
        api_version=config.get("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=config.get("AZURE_OPENAI_ENDPOINT"),
        organization="",
        project="",
        **client_runtime,
    )
    response = client.chat.completions.create(
        model=config.get("TRANSLATION_MODEL"),
        reasoning_effort=config.get("TRANSLATION_REASONING_EFFORT", "medium"),
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": chunk},
        ],
        **(
            {"max_completion_tokens": budget.reserved_output_tokens}
            if budget is not None
            else {}
        ),
    )
    choice = response.choices[0]
    if choice.finish_reason != "stop":
        finish_reason = _known_provider_status(
            choice.finish_reason,
            {"content_filter", "function_call", "length", "null", "tool_calls"},
        )
        raise ProviderPartialResponse(
            "provider response was incomplete "
            f"(adapter=azure, status={finish_reason})"
        )
    return choice.message.content or ""


def _translate_responses_api(
    chunk: str,
    config: Config,
    prompt: str,
    *,
    client_runtime: dict[str, object],
    budget: RequestBudget | None,
) -> str:
    """OpenAI Responses adapter로 단일 번역 요청 실행.

    Args:
        chunk: 번역 요청 본문.
        config: 검증된 provider 설정.
        prompt: 번역 instructions.
        client_runtime: SDK 재시도·timeout 설정.
        budget: 검증된 요청 예산.

    Returns:
        완료된 번역 응답 본문.
    """

    from openai import OpenAI

    client = OpenAI(
        api_key=config.get("OPENAI_API_KEY"),
        base_url=OPENAI_API_BASE_URL,
        organization="",
        project="",
        **client_runtime,
    )
    response = client.responses.create(
        model=config.get("TRANSLATION_MODEL"),
        instructions=prompt,
        input=chunk,
        reasoning={"effort": config.get("TRANSLATION_REASONING_EFFORT", "medium")},
        store=False,
        **(
            {"max_output_tokens": budget.reserved_output_tokens}
            if budget is not None
            else {}
        ),
    )
    if response.status != "completed":
        response_status = _known_provider_status(
            response.status,
            {"cancelled", "failed", "in_progress", "incomplete", "queued"},
        )
        raise ProviderPartialResponse(
            "provider response was incomplete "
            f"(adapter=openai, status={response_status})"
        )
    return response.output_text or ""


def _translate_openai(chunk: str, config: Config, prompt: str) -> str:
    """재시도 없는 OpenAI 또는 Azure adapter로 단일 요청 실행."""

    client_runtime: dict[str, object] = {"max_retries": 0}
    budget = config.request_budget()
    if budget is not None:
        client_runtime["timeout"] = _request_timeout_seconds(config)
    if config.provider == "azure":
        return _translate_azure(
            chunk,
            config,
            prompt,
            client_runtime=client_runtime,
            budget=budget,
        )
    return _translate_responses_api(
        chunk,
        config,
        prompt,
        client_runtime=client_runtime,
        budget=budget,
    )
