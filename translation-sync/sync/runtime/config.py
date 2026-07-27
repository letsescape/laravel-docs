"""provider 설정 확인.

translation-sync/docs/01(설정 확인)·00-summary(2장 기술 기준)을 따른다.
설정 확인 오류는 재시도하지 않고 전처리 단계에서 중단한다.

TRANSLATION_PROVIDER: openai | azure | cli | identity(replay only)
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping


class ConfigError(Exception):
    """설정 확인 오류 (env 누락/형식 오류/provider 조합 오류). 재시도하지 않는다."""


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
    "TRANSLATION_RETRY_DELAY",
)


@dataclass(frozen=True)
class Config:
    provider: str
    values: Mapping[str, str]

    def get(self, key: str, default: str = "") -> str:
        return self.values.get(key, default)


def _validate_integer_option(key: str, value: str, *, allow_zero: bool) -> None:
    constraint = ">= 0" if allow_zero else "> 0"
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ConfigError(f"{key} must be an integer {constraint}") from exc
    if parsed < 0 or (parsed == 0 and not allow_zero):
        raise ConfigError(f"{key} must be an integer {constraint}")


def load_config(env: Mapping[str, str] | None = None) -> Config:
    """환경 변수를 확인해 Config를 반환한다. 오류 시 ConfigError를 던진다."""
    env = env if env is not None else os.environ

    provider = env.get("TRANSLATION_PROVIDER", "").strip()
    if provider not in _REQUIRED:
        raise ConfigError(
            f"TRANSLATION_PROVIDER must be one of {sorted(_REQUIRED)}, got {provider!r}"
        )
    if provider == "identity" and env.get("TRANSLATION_REPLAY") != "1":
        raise ConfigError("identity provider is only available during translation replay")

    values: dict[str, str] = {"TRANSLATION_PROVIDER": provider}
    missing: list[str] = []
    for key in _REQUIRED[provider]:
        val = env.get(key, "").strip()
        if not val:
            missing.append(key)
        else:
            values[key] = val

    if missing:
        raise ConfigError(f"missing env for provider {provider!r}: {', '.join(missing)}")

    for key in _OPTIONAL:
        val = env.get(key, "").strip()
        if val:
            if key == "TRANSLATION_CLI_TIMEOUT":
                _validate_integer_option(key, val, allow_zero=False)
            elif key == "TRANSLATION_RETRY_DELAY":
                _validate_integer_option(key, val, allow_zero=True)
            values[key] = val

    return Config(provider=provider, values=values)
