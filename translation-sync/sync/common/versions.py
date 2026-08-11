"""공유 versions.json 검증."""
from __future__ import annotations

import json
import re
from pathlib import Path

VERSION_RE = re.compile(r"^(?:master|(?:0|[1-9]\d*)\.x)$")


def validate_version_token(version: object) -> str:
    """``master`` 또는 ``13.x`` 형식의 검증된 버전 토큰 반환."""

    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        raise ValueError(f"invalid version: {version}")
    return version


def load_versions(path: Path) -> list[str]:
    """versions.json에서 형식·순서·중복을 검증한 버전 목록 로딩."""

    raw_versions = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw_versions, list):
        raise ValueError("versions.json must contain a list")
    if not raw_versions:
        raise ValueError("versions.json must not be empty")

    try:
        versions = [validate_version_token(version) for version in raw_versions]
    except ValueError as exc:
        raise ValueError(f"invalid versions.json entry: {exc}") from exc
    if versions[0] != "master":
        raise ValueError("versions.json must list master once as the first version")
    if len(versions) != len(set(versions)):
        raise ValueError("versions.json must contain unique versions")

    stable_versions = versions[1:]
    if not stable_versions:
        raise ValueError("versions.json must contain at least one stable version")
    if stable_versions != sorted(
        stable_versions,
        key=lambda version: int(version.removesuffix(".x")),
        reverse=True,
    ):
        raise ValueError(
            "versions.json must list stable versions in descending order"
        )
    return versions
