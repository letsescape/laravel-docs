"""provider 설정 검증.

provider 종류, 모델, token 예산, timeout 및 CLI argv를 실행 전에 검증.
설정 오류는 provider 호출이나 문서 변경 없이 즉시 중단.

TRANSLATION_PROVIDER: openai | azure | cli | identity(replay 전용)
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import shlex
import time
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

import tiktoken

from .failure import IssueCode


class ConfigError(Exception):
    """누락·형식·provider 조합에 대한 재시도 불가 설정 오류."""

    def __init__(
        self,
        message: str,
        issue_code: IssueCode = IssueCode.REQUIRED_CONFIG_MISSING,
    ) -> None:
        """설정 오류 초기화."""

        super().__init__(message)
        self.issue_code = issue_code


_REQUIRED: dict[str, tuple[str, ...]] = {
    "identity": (),
    "openai": ("TRANSLATION_MODEL", "OPENAI_API_KEY"),
    "azure": (
        "TRANSLATION_MODEL",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_API_VERSION",
        "AZURE_OPENAI_ENDPOINT",
    ),
    "cli": ("TRANSLATION_CLI_COMMAND", "TRANSLATION_MODEL"),
}
_OPTIONAL = (
    "TRANSLATION_CLI_TIMEOUT",
    "TRANSLATION_REASONING_EFFORT",
)
_REQUEST_BUDGET_KEYS = (
    "TRANSLATION_CONTEXT_WINDOW_TOKENS",
    "TRANSLATION_RESERVED_OUTPUT_TOKENS",
    "TRANSLATION_REQUEST_TIMEOUT_SECONDS",
    "TRANSLATION_RUN_TIMEOUT_SECONDS",
    "TRANSLATION_WORKFLOW_TIMEOUT_SECONDS",
)
_TOKENIZER_KEY = "TRANSLATION_TOKENIZER_ENCODING"
_MODEL_PROFILE_KEY = "TRANSLATION_MODEL_PROFILE"
_CLI_TOKEN_KEYS = (
    "CODEX_ACCESS_TOKEN",
    "CODEX_API_KEY",
)
WORKFLOW_DEADLINE_ENV = "TRANSLATION_WORKFLOW_DEADLINE_MONOTONIC"
RUN_DEADLINE_ENV = "TRANSLATION_RUN_DEADLINE_MONOTONIC"
PROVIDER_BUDGET_PROFILE_VERSION = 1
# 두 요청 문자열에 나타나지 않는 provider/API/CLI 프레이밍의 보수적 승인 여유분.
# 측정된 overhead가 아닌 프로젝트 고정값.
PROVIDER_FRAMING_OVERHEAD_TOKENS = 128_000
OPENAI_API_BASE_URL = "https://api.openai.com/v1"


@dataclass(frozen=True)
class ModelProfile:
    """승인된 모델의 tokenizer와 token 한도."""

    tokenizer_encoding: str
    context_window_tokens: int
    max_output_tokens: int


# context/output 한도와 tokenizer 조합을 명시적으로 승인한 모델 profile.
_MODEL_PROFILES: Mapping[str, ModelProfile] = {
    name: ModelProfile(
        tokenizer_encoding="o200k_base",
        context_window_tokens=1_050_000,
        max_output_tokens=128_000,
    )
    for name in (
        "gpt-5.6",
        "gpt-5.6-luna",
        "gpt-5.6-sol",
        "gpt-5.6-terra",
    )
}


@dataclass(frozen=True)
class RequestBudget:
    """provider 요청의 token·시간 예산."""

    context_window_tokens: int
    reserved_output_tokens: int
    request_timeout_seconds: int
    run_timeout_seconds: int
    workflow_timeout_seconds: int
    tokenizer_encoding: str

    @property
    def max_input_tokens(self) -> int:
        """출력 예약량을 제외한 최대 입력 token 수."""

        return self.context_window_tokens - self.reserved_output_tokens


@dataclass(frozen=True)
class Config:
    """검증 후 변경할 수 없는 provider 설정."""

    provider: str
    values: Mapping[str, str]

    def __post_init__(self) -> None:
        """설정값 복사본을 읽기 전용 mapping으로 봉인."""

        object.__setattr__(self, "values", MappingProxyType(dict(self.values)))

    def get(self, key: str, default: str = "") -> str:
        """설정값 조회."""

        return self.values.get(key, default)

    def request_budget(self) -> RequestBudget | None:
        """설정에 포함된 검증된 live provider 요청 예산."""

        if not any(key in self.values for key in _REQUEST_BUDGET_KEYS):
            return None
        missing = [key for key in _REQUEST_BUDGET_KEYS if key not in self.values]
        if _TOKENIZER_KEY not in self.values:
            missing.append(_TOKENIZER_KEY)
        if missing:
            raise ConfigError(
                "INVALID_REQUEST_BUDGET: incomplete request budget: "
                + ", ".join(missing),
                IssueCode.INVALID_REQUEST_BUDGET,
            )
        try:
            budget = RequestBudget(
                context_window_tokens=int(
                    self.values["TRANSLATION_CONTEXT_WINDOW_TOKENS"]
                ),
                reserved_output_tokens=int(
                    self.values["TRANSLATION_RESERVED_OUTPUT_TOKENS"]
                ),
                request_timeout_seconds=int(
                    self.values["TRANSLATION_REQUEST_TIMEOUT_SECONDS"]
                ),
                run_timeout_seconds=int(
                    self.values["TRANSLATION_RUN_TIMEOUT_SECONDS"]
                ),
                workflow_timeout_seconds=int(
                    self.values["TRANSLATION_WORKFLOW_TIMEOUT_SECONDS"]
                ),
                tokenizer_encoding=self.values[_TOKENIZER_KEY],
            )
        except (TypeError, ValueError) as exc:
            raise ConfigError(
                "INVALID_REQUEST_BUDGET: request budget values must be integers",
                IssueCode.INVALID_REQUEST_BUDGET,
            ) from exc
        _validate_request_budget_values(budget)
        _validate_model_metadata(self.provider, self.values, budget)
        return budget


def validate_cli_command(command: str) -> tuple[str, str]:
    """옵션이 없는 Codex entrypoint 명령만 허용."""

    try:
        parts = shlex.split(command)
    except ValueError as exc:
        raise ConfigError(
            "TRANSLATION_CLI_COMMAND must be an options-free 'codex exec' entrypoint",
            IssueCode.INVALID_RUNTIME_OPTION,
        ) from exc
    executable = (
        parts[0].replace("\\", "/").rsplit("/", 1)[-1].lower()
        if parts
        else ""
    )
    if (
        len(parts) != 2
        or executable not in {"codex", "codex.exe"}
        or parts[1] != "exec"
    ):
        raise ConfigError(
            "TRANSLATION_CLI_COMMAND must be an options-free 'codex exec' entrypoint",
            IssueCode.INVALID_RUNTIME_OPTION,
        )
    return parts[0], parts[1]


def cli_auth_environment(cfg: Config) -> dict[str, str]:
    """검증된 설정의 단일 명시적 CLI 인증 방식."""

    configured: list[tuple[str, str]] = []
    for key in _CLI_TOKEN_KEYS:
        value = cfg.get(key).strip()
        if value:
            configured.append((key, value))
    codex_home = cfg.get("CODEX_HOME").strip()
    if codex_home:
        configured.append(("CODEX_HOME", codex_home))
    if not configured:
        raise ConfigError(
            "CLI provider requires explicit CODEX_HOME or an allowed token",
            IssueCode.PROVIDER_CREDENTIAL_MISSING,
        )
    if len(configured) != 1:
        raise ConfigError(
            "CLI provider requires exactly one authentication mode",
            IssueCode.INVALID_RUNTIME_OPTION,
        )
    key, value = configured[0]
    if key == "CODEX_HOME":
        path = Path(value)
        if not path.is_absolute():
            raise ConfigError(
                "CODEX_HOME must be an absolute path for the CLI provider",
                IssueCode.INVALID_RUNTIME_OPTION,
            )
        return {"CODEX_HOME": str(path)}
    return {key: value}


def _model_profile_name(provider: str, values: Mapping[str, str]) -> str:
    """provider 종류에 대응하는 승인 모델 profile 이름."""

    if provider == "azure":
        return values.get(_MODEL_PROFILE_KEY, "").strip()
    return values.get("TRANSLATION_MODEL", "").strip()


def provider_model_profile(cfg: Config) -> str:
    """검증 증거에 사용할 최종 승인 모델 profile 이름."""

    return cfg.get(
        _MODEL_PROFILE_KEY,
        cfg.get("TRANSLATION_MODEL"),
    ).strip()


def provider_config_sha256(cfg: Config) -> str:
    """비밀값을 제외한 최종 live provider 계약의 결정적 해시."""

    auth_modes: list[str] = []
    if cfg.provider == "openai":
        if cfg.get("OPENAI_API_KEY"):
            auth_modes.append("OPENAI_API_KEY")
        adapter: dict[str, object] = {
            "api_base_url": OPENAI_API_BASE_URL,
        }
    elif cfg.provider == "azure":
        if cfg.get("AZURE_OPENAI_API_KEY"):
            auth_modes.append("AZURE_OPENAI_API_KEY")
        adapter = {
            "api_version": cfg.get("AZURE_OPENAI_API_VERSION"),
            "endpoint": cfg.get("AZURE_OPENAI_ENDPOINT"),
        }
    elif cfg.provider == "cli":
        auth_modes.extend(
            key for key in _CLI_TOKEN_KEYS if cfg.get(key).strip()
        )
        if cfg.get("CODEX_HOME").strip():
            auth_modes.append("CODEX_HOME")
        adapter = {
            "command": cfg.get("TRANSLATION_CLI_COMMAND"),
            "timeout_seconds": cfg.get("TRANSLATION_CLI_TIMEOUT", "1800"),
        }
    else:
        adapter = {}

    payload = {
        "adapter": adapter,
        "auth_modes": auth_modes,
        "budget_profile_version": PROVIDER_BUDGET_PROFILE_VERSION,
        "context_window_tokens": cfg.get(
            "TRANSLATION_CONTEXT_WINDOW_TOKENS"
        ),
        "framing_allowance_tokens": PROVIDER_FRAMING_OVERHEAD_TOKENS,
        "model": cfg.get("TRANSLATION_MODEL"),
        "model_profile": provider_model_profile(cfg),
        "provider": cfg.provider,
        "reasoning_effort": cfg.get(
            "TRANSLATION_REASONING_EFFORT", "medium"
        ),
        "request_timeout_seconds": cfg.get(
            "TRANSLATION_REQUEST_TIMEOUT_SECONDS"
        ),
        "reserved_output_tokens": cfg.get(
            "TRANSLATION_RESERVED_OUTPUT_TOKENS"
        ),
        "run_timeout_seconds": cfg.get("TRANSLATION_RUN_TIMEOUT_SECONDS"),
        "tokenizer_encoding": cfg.get("TRANSLATION_TOKENIZER_ENCODING"),
        "workflow_timeout_seconds": cfg.get(
            "TRANSLATION_WORKFLOW_TIMEOUT_SECONDS"
        ),
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _validate_model_metadata(
    provider: str,
    values: Mapping[str, str],
    budget: RequestBudget,
) -> None:
    """모델 메타데이터 검증."""

    profile_name = _model_profile_name(provider, values)
    profile = _MODEL_PROFILES.get(profile_name)
    if profile is None:
        label = _MODEL_PROFILE_KEY if provider == "azure" else "TRANSLATION_MODEL"
        raise ConfigError(
            f"TOKENIZER_METADATA_UNAVAILABLE: no approved profile for {label} "
            f"{profile_name!r}",
            IssueCode.TOKENIZER_METADATA_UNAVAILABLE,
        )
    if budget.tokenizer_encoding != profile.tokenizer_encoding:
        raise ConfigError(
            "TOKENIZER_METADATA_UNAVAILABLE: configured tokenizer does not match "
            f"model profile {profile_name!r}",
            IssueCode.TOKENIZER_METADATA_UNAVAILABLE,
        )
    if budget.context_window_tokens > profile.context_window_tokens:
        raise ConfigError(
            "INVALID_REQUEST_BUDGET: configured context window exceeds verified "
            f"model profile {profile_name!r}",
            IssueCode.INVALID_REQUEST_BUDGET,
        )
    if budget.reserved_output_tokens > profile.max_output_tokens:
        raise ConfigError(
            "INVALID_REQUEST_BUDGET: reserved output exceeds verified model "
            f"profile {profile_name!r}",
            IssueCode.INVALID_REQUEST_BUDGET,
        )


def _validate_request_budget_values(budget: RequestBudget) -> None:
    """요청 token과 timeout 값 사이의 제약 검증."""

    numeric_values = (
        budget.context_window_tokens,
        budget.reserved_output_tokens,
        budget.request_timeout_seconds,
        budget.run_timeout_seconds,
        budget.workflow_timeout_seconds,
    )
    if any(value <= 0 for value in numeric_values):
        raise ConfigError(
            "INVALID_REQUEST_BUDGET: request budget values must be positive",
            IssueCode.INVALID_REQUEST_BUDGET,
        )
    if budget.reserved_output_tokens >= budget.context_window_tokens:
        raise ConfigError(
            "INVALID_REQUEST_BUDGET: "
            "TRANSLATION_RESERVED_OUTPUT_TOKENS must be less than "
            "TRANSLATION_CONTEXT_WINDOW_TOKENS",
            IssueCode.INVALID_REQUEST_BUDGET,
        )
    if not (
        budget.request_timeout_seconds
        <= budget.run_timeout_seconds
        <= budget.workflow_timeout_seconds
    ):
        raise ConfigError(
            "INVALID_REQUEST_BUDGET: require "
            "TRANSLATION_REQUEST_TIMEOUT_SECONDS <= "
            "TRANSLATION_RUN_TIMEOUT_SECONDS <= "
            "TRANSLATION_WORKFLOW_TIMEOUT_SECONDS",
            IssueCode.INVALID_REQUEST_BUDGET,
        )


def _validate_integer_option(key: str, value: str, *, allow_zero: bool) -> None:
    """정수형 실행 옵션의 범위 검증."""

    constraint = ">= 0" if allow_zero else "> 0"
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ConfigError(
            f"{key} must be an integer {constraint}",
            IssueCode.INVALID_RUNTIME_OPTION,
        ) from exc
    if parsed < 0 or (parsed == 0 and not allow_zero):
        raise ConfigError(
            f"{key} must be an integer {constraint}",
            IssueCode.INVALID_RUNTIME_OPTION,
        )


def _validate_tokenizer_encoding(name: str) -> None:
    """설치된 tiktoken encoding 이름 검증."""

    if name not in tiktoken.list_encoding_names():
        raise ConfigError(
            f"TOKENIZER_METADATA_UNAVAILABLE: unknown tokenizer encoding {name!r}",
            IssueCode.TOKENIZER_METADATA_UNAVAILABLE,
        )


def load_config(env: Mapping[str, str] | None = None) -> Config:
    """환경 변수에서 검증된 provider 설정 로딩.

    Raises:
        ConfigError: 필수 값 누락, 허용되지 않은 조합 또는 예산 오류.
    """
    env = env if env is not None else os.environ

    provider = env.get("TRANSLATION_PROVIDER", "").strip()
    if provider not in _REQUIRED:
        raise ConfigError(
            f"TRANSLATION_PROVIDER must be one of {sorted(_REQUIRED)}, got {provider!r}",
            IssueCode.PROVIDER_SELECTION_INVALID,
        )
    if provider == "identity" and env.get("TRANSLATION_REPLAY") != "1":
        raise ConfigError(
            "identity provider is only available during translation replay",
            IssueCode.REPLAY_PROVIDER_FORBIDDEN,
        )

    values: dict[str, str] = {"TRANSLATION_PROVIDER": provider}
    missing: list[str] = []
    for key in _REQUIRED[provider]:
        val = env.get(key, "").strip()
        if not val:
            missing.append(key)
        else:
            values[key] = val

    if missing:
        issue_code = (
            IssueCode.PROVIDER_CREDENTIAL_MISSING
            if any(key.endswith("API_KEY") for key in missing)
            else IssueCode.REQUIRED_CONFIG_MISSING
        )
        raise ConfigError(
            f"missing env for provider {provider!r}: {', '.join(missing)}",
            issue_code,
        )

    if provider == "identity":
        return Config(provider=provider, values=values)
    if provider == "cli":
        validate_cli_command(values["TRANSLATION_CLI_COMMAND"])
        auth_config = Config(provider=provider, values=env)
        values.update(cli_auth_environment(auth_config))
    if provider == "azure":
        model_profile = env.get(_MODEL_PROFILE_KEY, "").strip()
        if not model_profile:
            raise ConfigError(
                f"TOKENIZER_METADATA_UNAVAILABLE: missing {_MODEL_PROFILE_KEY}",
                IssueCode.TOKENIZER_METADATA_UNAVAILABLE,
            )
        values[_MODEL_PROFILE_KEY] = model_profile
    missing_budget = [
        key for key in _REQUEST_BUDGET_KEYS if not env.get(key, "").strip()
    ]
    if missing_budget:
        raise ConfigError(
            "INVALID_REQUEST_BUDGET: missing " + ", ".join(missing_budget),
            IssueCode.INVALID_REQUEST_BUDGET,
        )
    tokenizer_encoding = env.get(_TOKENIZER_KEY, "").strip()
    if not tokenizer_encoding:
        raise ConfigError(
            f"TOKENIZER_METADATA_UNAVAILABLE: missing {_TOKENIZER_KEY}",
            IssueCode.TOKENIZER_METADATA_UNAVAILABLE,
        )
    _validate_tokenizer_encoding(tokenizer_encoding)
    for key in _REQUEST_BUDGET_KEYS:
        value = env[key].strip()
        try:
            _validate_integer_option(key, value, allow_zero=False)
        except ConfigError as exc:
            raise ConfigError(
                f"INVALID_REQUEST_BUDGET: {exc}",
                IssueCode.INVALID_REQUEST_BUDGET,
            ) from exc
        values[key] = value
    values[_TOKENIZER_KEY] = tokenizer_encoding

    budget = Config(provider=provider, values=values).request_budget()
    assert budget is not None

    for key in _OPTIONAL:
        val = env.get(key, "").strip()
        if val:
            if key == "TRANSLATION_CLI_TIMEOUT":
                _validate_integer_option(key, val, allow_zero=False)
            values[key] = val

    return Config(provider=provider, values=values)


def required_run_deadline(
    cfg: Config,
    env: Mapping[str, str] | None = None,
    *,
    clock=time.monotonic,
) -> float | None:
    """live provider fixture 전에 환경의 절대 실행 기한 검증 및 로딩."""
    if cfg.provider == "identity":
        return None
    budget = cfg.request_budget()
    if budget is None:
        return None
    env = env if env is not None else os.environ
    try:
        workflow_deadline = float(env.get(WORKFLOW_DEADLINE_ENV, ""))
        run_deadline = float(env.get(RUN_DEADLINE_ENV, ""))
    except ValueError as exc:
        raise ConfigError(
            "INVALID_RUNTIME_OPTION: absolute translation deadline is missing or invalid",
            IssueCode.INVALID_RUNTIME_OPTION,
        ) from exc
    now = clock()
    if (
        not math.isfinite(workflow_deadline)
        or not math.isfinite(run_deadline)
        or run_deadline <= now
        or workflow_deadline <= now
        or run_deadline > workflow_deadline
        or run_deadline > now + budget.run_timeout_seconds
    ):
        raise ConfigError(
            "INVALID_RUNTIME_OPTION: absolute translation deadline is missing or invalid",
            IssueCode.INVALID_RUNTIME_OPTION,
        )
    return run_deadline
