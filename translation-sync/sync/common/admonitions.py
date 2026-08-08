"""지원되는 legacy Markdown admonition marker의 canonical 파싱."""
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
    """기존 admonition 표식의 canonical 유형과 본문."""

    kind: str
    body: str


def parse_legacy_admonition_line(line: str) -> LegacyAdmonition | None:
    """들여쓰기 없는 기존 blockquote admonition 한 줄 파싱."""
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


def admonition_types(text: str) -> tuple[str, ...]:
    """HTML 주석과 fenced code 밖의 canonical admonition 유형 순서."""

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

        logical, containers = _strip_reference_container(line)
        if not containers or containers[-1] != "quote":
            continue
        marker = _GFM_MARKER_RE.match(logical)
        if marker is not None:
            types.append(marker.group(1).upper())
            continue
        legacy = parse_legacy_admonition_line(f"> {logical}")
        if legacy is not None:
            types.append(legacy.kind)
    return tuple(types)
