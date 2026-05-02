"""Markdown link parsing utilities for updater validation.

번역 구조 검증/디버깅이 의존하는 Markdown 파싱 유틸. fenced code block(```,
~~~)과 inline code(`...`)는 검사 대상에서 빠지고, 링크는 [label](url)
형태만 다룬다. `{{version}}` 플레이스홀더 치환과 `{{ version }}` 띄어쓰기
변형도 모두 처리한다.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


_FENCE_TOKENS = ("```", "~~~")


def _fence_at(src: str, index: int) -> str | None:
    for token in _FENCE_TOKENS:
        if src.startswith(token, index):
            return token
    return None


def _find_inline_code_end(src: str, index: int) -> int:
    end = src.find("`", index + 1)
    if end < 0:
        return -1

    newline = src.find("\n", index + 1)
    if 0 <= newline < end:
        return -1

    return end


def strip_code(src: str) -> str:
    """Code fence/inline code 영역을 제거해 비교 가능한 텍스트만 남긴다."""
    out = []
    i = 0
    length = len(src)
    while i < length:
        fence = _fence_at(src, i)
        if fence:
            end = src.find(fence, i + len(fence))
            if end < 0:
                return "".join(out)
            i = end + len(fence)
            continue
        if src[i] == "`":
            end = _find_inline_code_end(src, i)
            if end < 0:
                out.append(src[i])
                i += 1
                continue
            i = end + 1
            continue
        out.append(src[i])
        i += 1
    return "".join(out)


def _strip_title_suffix(raw: str) -> str:
    """링크 url 뒤 공백/제목 부분을 잘라낸다. {{...}} 안 공백은 url의 일부."""
    in_placeholder = False
    i = 0
    length = len(raw)
    while i < length:
        if not in_placeholder and raw.startswith("{{", i):
            in_placeholder = True
            i += 2
            continue
        if in_placeholder and raw.startswith("}}", i):
            in_placeholder = False
            i += 2
            continue

        ch = raw[i]
        if not in_placeholder and ch in (" ", "\t", "\n", "\r"):
            return raw[:i]
        i += 1
    return raw


@dataclass(frozen=True)
class MarkdownLink:
    text: str
    url: str


def extract_markdown_links(text: str) -> list[MarkdownLink]:
    """`[label](url)` 형태의 링크를 모두 추출. fenced/inline code 안은 무시."""
    stripped = strip_code(text)
    links: list[MarkdownLink] = []
    i = 0
    length = len(stripped)
    while i < length:
        label_start = stripped.find("[", i)
        if label_start < 0:
            break

        label_end = stripped.find("]", label_start + 1)
        if label_end < 0:
            break

        if label_end + 1 >= length or stripped[label_end + 1] != "(":
            i = label_end + 1
            continue

        url_end = stripped.find(")", label_end + 2)
        if url_end < 0:
            break

        url = _strip_title_suffix(stripped[label_end + 2 : url_end])
        if url:
            links.append(
                MarkdownLink(
                    text=stripped[label_start + 1 : label_end],
                    url=url,
                )
            )
        i = url_end + 1
    return links


def is_internal_docs_link(url: str) -> bool:
    return (
        url.startswith("/docs/")
        or url.startswith("#")
        or url.startswith("{{version}}")
        or url.startswith("{{ version }}")
    )


def extract_internal_markdown_links(text: str) -> list[MarkdownLink]:
    return [link for link in extract_markdown_links(text) if is_internal_docs_link(link.url)]


_VERSION_DIR_RE = re.compile(r"version-(?P<version>[^/]+)")


def extract_version_from_path(path: str) -> str | None:
    for part in str(path).split("/"):
        if part.startswith("version-"):
            return part[len("version-") :]
    return None


_VERSION_TOKEN_RE = re.compile(r"\{\{\s*version\s*\}\}")


def replace_version_placeholders(value: str, version: str = "") -> str:
    """`{{version}}`, `{{ version }}` 모두 동일한 문자열로 치환한다."""
    return _VERSION_TOKEN_RE.sub(version, value)
