"""지원되는 레거시 Markdown 경고문 표식을 정규 형식으로 파싱."""
from __future__ import annotations

import re
from dataclasses import dataclass

from .markdown import (
    _strip_reference_container,
    closes_fence,
    fence_token,
    strip_html_comments,
)


_CANONICAL_TYPES = {
    "note": "NOTE",
    "tip": "TIP",
    "warning": "WARNING",
    "caution": "CAUTION",
    "important": "IMPORTANT",
    "참고": "NOTE",
    "注意": "NOTE",
    "注": "NOTE",
}
_MARKER_PATTERN = "|".join(
    sorted((re.escape(marker) for marker in _CANONICAL_TYPES), key=len, reverse=True)
)
_BRACED_MARKER_RE = re.compile(
    rf"^\{{(?P<kind>{_MARKER_PATTERN})\}}(?:\s*(?P<body>.*))?$",
    re.IGNORECASE,
)
_BOLD_MARKER_RE = re.compile(
    rf"^\*\*(?P<kind>{_MARKER_PATTERN})(?P<inner_colon>:)?\*\*"
    rf"(?P<outer_colon>:)?(?:\s*(?P<body>.*))?$",
    re.IGNORECASE,
)
_PLAIN_MARKER_RE = re.compile(
    rf"^(?P<kind>{_MARKER_PATTERN})(?P<colon>:)?(?:\s*(?P<body>.*))?$",
    re.IGNORECASE,
)
_GFM_MARKER_RE = re.compile(
    r"^[ \t]{0,3}\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT)]",
)


@dataclass(frozen=True)
class LegacyAdmonition:
    """레거시 경고문 표식의 정규 유형과 본문."""

    kind: str
    body: str


def parse_legacy_admonition_line(line: str) -> LegacyAdmonition | None:
    """들여쓰기 없는 레거시 인용문 경고문 한 줄 파싱."""
    if not line.startswith(">"):
        return None

    content = line[1:].strip()
    match = _BRACED_MARKER_RE.fullmatch(content)
    if match is None:
        match = _BOLD_MARKER_RE.fullmatch(content)
    if match is None:
        match = _PLAIN_MARKER_RE.fullmatch(content)
        if match is not None and match.group("body") and not match.group("colon"):
            return None
    if match is None:
        return None

    marker = match.group("kind")
    canonical = _CANONICAL_TYPES.get(marker.lower(), _CANONICAL_TYPES.get(marker))
    if canonical is None:
        return None
    return LegacyAdmonition(canonical, (match.group("body") or "").strip())


def _visible_admonition_type(line: str) -> str | None:
    """코드 펜스 밖의 인용문 한 줄에서 경고문 유형 추출.

    Args:
        line: HTML 주석을 제거한 Markdown 한 줄.

    Returns:
        정규 경고문 유형 또는 경고문이 아니면 ``None``.
    """

    logical, containers = _strip_reference_container(line)
    if not containers or containers[-1] != "quote":
        return None
    marker = _GFM_MARKER_RE.match(logical)
    if marker is not None:
        return marker.group(1).upper()
    legacy = parse_legacy_admonition_line(f"> {logical}")
    return legacy.kind if legacy is not None else None


def admonition_types(text: str) -> tuple[str, ...]:
    """HTML 주석과 코드 펜스 밖의 정규 경고문 유형을 문서 순서대로 반환."""

    visible = strip_html_comments(text)
    types: list[str] = []
    opening_fence = ""
    for line in visible.splitlines():
        token = fence_token(line)
        if opening_fence:
            if token and closes_fence(line, opening_fence):
                opening_fence = ""
            continue
        if token:
            opening_fence = token
            continue

        admonition_type = _visible_admonition_type(line)
        if admonition_type is not None:
            types.append(admonition_type)
    return tuple(types)
