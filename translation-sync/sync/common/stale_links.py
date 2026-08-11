"""오래된 링크의 정규 레지스트리 로딩과 대체 대상 조회."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

from .versions import validate_version_token


SCHEMA_VERSION = 1
REGISTRY_PATH = Path(__file__).resolve().parents[2] / "stale-links.json"
_TOP_LEVEL_KEYS = ("schema_version", "links")
_ENTRY_KEYS = ("version", "from", "to", "retire_mode")
_RETIRE_MODES = {"standalone-list-label", "bare-inline-code"}


class StaleLinkRegistryError(ValueError):
    """``stale-links.json`` 누락 또는 형식 오류."""


@dataclass(frozen=True)
class StaleLinkRule:
    """버전별 오래된 링크의 원본·대체 대상·폐기 방식."""

    version: str
    source: str
    target: str | None
    retire_mode: str | None


def _is_supported_target(target: str) -> bool:
    """레지스트리를 적용할 수 있는 Laravel 문서 링크 여부."""

    parsed = urlsplit(target)
    if target.startswith("//"):
        return False
    if not parsed.scheme:
        return True
    return (
        parsed.scheme in {"http", "https"}
        and parsed.netloc.lower() == "laravel.com"
        and parsed.path.startswith("/docs/")
    )


def _matches_suffix_rule(rule: StaleLinkRule, target: str) -> bool:
    """링크가 대체 규칙의 경계가 보존된 접미사와 일치하는지 여부."""

    if rule.target is None or not target.endswith(rule.source):
        return False
    start = len(target) - len(rule.source)
    return (
        start == 0
        or rule.source.startswith("#")
        or (start > 0 and target[start - 1] == "/")
    )


@dataclass(frozen=True)
class StaleLinkRegistry:
    """정규 JSON 원본 바이트와 SHA-256 해시를 포함한 오래된 링크 규칙 집합."""

    raw: bytes
    sha256: str
    rules: tuple[StaleLinkRule, ...]

    def matching_rule(
        self,
        target: str,
        version: str | None,
    ) -> StaleLinkRule | None:
        """버전과 링크 대상에 대응하는 정확한 폐기 규칙 또는 원본 접미사가 가장 긴 대체 규칙 조회."""

        if not _is_supported_target(target):
            return None

        effective_version = version or "master"
        exact_retired: StaleLinkRule | None = None
        suffix_matches: list[StaleLinkRule] = []
        for rule in self.rules:
            if rule.version != effective_version:
                continue
            if rule.target is None and target == rule.source:
                exact_retired = rule
                break
            if _matches_suffix_rule(rule, target):
                suffix_matches.append(rule)
        if exact_retired is not None:
            return exact_retired
        if not suffix_matches:
            return None
        return max(suffix_matches, key=lambda rule: len(rule.source.encode("utf-8")))


def _canonical_json(value: object) -> bytes:
    """레지스트리 값을 정규 UTF-8 JSON 바이트로 직렬화."""

    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _invalid(message: str) -> StaleLinkRegistryError:
    """일관된 접두사가 붙은 레지스트리 형식 오류 생성."""

    return StaleLinkRegistryError(f"invalid stale-link registry: {message}")


def _decode_registry(raw: bytes) -> dict[str, object]:
    """레지스트리 바이트를 순서가 보존된 JSON 객체로 디코딩.

    Args:
        raw: 레지스트리 원본 바이트.

    Returns:
        검증 전 최상위 JSON 객체.

    Raises:
        StaleLinkRegistryError: UTF-8, JSON 또는 최상위 필드 계약 위반.
    """

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _invalid("file must be UTF-8") from exc
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise _invalid("malformed JSON") from exc
    if not isinstance(value, dict) or tuple(value) != _TOP_LEVEL_KEYS:
        raise _invalid("top-level fields or key order")
    return value


def _validated_retire_mode(
    target: str | None,
    retire_mode: object,
    index: int,
) -> str | None:
    """대체 대상 유무와 폐기 방식 조합 검증."""

    if target is None:
        if not isinstance(retire_mode, str) or retire_mode not in _RETIRE_MODES:
            raise _invalid(f"links[{index}].retire_mode")
        return retire_mode
    if retire_mode is not None:
        raise _invalid(f"links[{index}].retire_mode")
    return None


def _parse_rule(entry: object, index: int) -> StaleLinkRule:
    """JSON 항목 하나를 정규 오래된 링크 규칙으로 변환."""

    if not isinstance(entry, dict) or tuple(entry) != _ENTRY_KEYS:
        raise _invalid(f"links[{index}] fields or key order")
    try:
        version = validate_version_token(entry["version"])
    except ValueError as exc:
        raise _invalid(f"links[{index}] version") from exc
    source = entry["from"]
    target = entry["to"]
    if not isinstance(source, str) or not source:
        raise _invalid(f"links[{index}].from")
    if target is not None and (not isinstance(target, str) or not target):
        raise _invalid(f"links[{index}].to")
    try:
        source.encode("utf-8")
        if target is not None:
            target.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise _invalid(f"links[{index}] strings must be UTF-8") from exc
    retire_mode = _validated_retire_mode(target, entry["retire_mode"], index)
    return StaleLinkRule(version, source, target, retire_mode)


def _validate_rules(rules: list[StaleLinkRule], raw: bytes, value: object) -> None:
    """규칙 고유성·정렬·정규 JSON 바이트 계약 검증."""

    identities: set[tuple[str, str]] = set()
    for index, rule in enumerate(rules):
        identity = (rule.version, rule.source)
        if identity in identities:
            raise _invalid(f"duplicate version/from at links[{index}]")
        identities.add(identity)
    ordering = [
        (rule.version.encode("utf-8"), rule.source.encode("utf-8"))
        for rule in rules
    ]
    if ordering != sorted(ordering):
        raise _invalid("links must be sorted by version/from UTF-8 bytes")
    if raw != _canonical_json(value):
        raise _invalid("file must use canonical JSON")


def load_stale_link_registry(path: Path = REGISTRY_PATH) -> StaleLinkRegistry:
    """정규 JSON 형식과 규칙 순서를 검증해 오래된 링크 레지스트리 로딩.

    Raises:
        StaleLinkRegistryError: 파일 누락, 인코딩 오류 또는 스키마 위반.
    """

    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise StaleLinkRegistryError(
            f"stale-link registry is unavailable: {path}"
        ) from exc

    value = _decode_registry(raw)
    schema_version = value["schema_version"]
    if type(schema_version) is not int or schema_version != SCHEMA_VERSION:
        raise _invalid("unsupported schema_version")
    entries = value["links"]
    if not isinstance(entries, list):
        raise _invalid("links must be an array")

    rules = [_parse_rule(entry, index) for index, entry in enumerate(entries)]
    _validate_rules(rules, raw, value)

    return StaleLinkRegistry(
        raw=raw,
        sha256=hashlib.sha256(raw).hexdigest(),
        rules=tuple(rules),
    )


DEFAULT_STALE_LINK_REGISTRY = load_stale_link_registry()


def canonical_stale_link_target(
    target: str,
    version: str | None,
    *,
    registry: StaleLinkRegistry = DEFAULT_STALE_LINK_REGISTRY,
) -> str | None:
    """레지스트리 규칙에 따른 정규 링크 대상 또는 폐기 상태 반환."""

    rule = registry.matching_rule(target, version)
    if rule is None or rule.target is None:
        return None if rule is not None else target
    return target[: -len(rule.source)] + rule.target
