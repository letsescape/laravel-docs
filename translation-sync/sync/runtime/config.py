"""provider 설정 확인.

translation-sync/docs/01(설정 확인)·00-summary(2장 기술 기준)을 따른다.
설정 확인 오류는 재시도하지 않고 전처리 단계에서 중단한다.

TRANSLATION_PROVIDER: openai | azure | cli
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping


class ConfigError(Exception):
    """설정 확인 오류 (env 누락/형식 오류/provider 조합 오류). 재시도하지 않는다."""


_REQUIRED: dict[str, tuple[str, ...]] = {
    "openai": ("TRANSLATION_MODEL", "OPENAI_API_KEY"),
    "azure": (
        "TRANSLATION_MODEL",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_API_VERSION",
        "AZURE_OPENAI_ENDPOINT",
    ),
    "cli": ("TRANSLATION_CLI_COMMAND",),
}


@dataclass(frozen=True)
class Config:
    provider: str
    values: Mapping[str, str]

    def get(self, key: str, default: str = "") -> str:
        return self.values.get(key, default)


def load_config(env: Mapping[str, str] | None = None) -> Config:
    """환경 변수를 확인해 Config를 반환한다. 오류 시 ConfigError를 던진다."""
    env = env if env is not None else os.environ

    provider = env.get("TRANSLATION_PROVIDER", "").strip()
    if provider not in _REQUIRED:
        raise ConfigError(
            f"TRANSLATION_PROVIDER must be one of {sorted(_REQUIRED)}, got {provider!r}"
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
        raise ConfigError(f"missing env for provider {provider!r}: {', '.join(missing)}")

    return Config(provider=provider, values=values)
