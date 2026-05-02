"""Print source context for internal links missing from a translation.

번역본에서 누락된 링크가 원문 어디에 있는지 200자 컨텍스트로 보여주는 디버깅
도구. 번역 회귀를 빠르게 추적할 때 사용한다.

Usage:
    uv run python find_link_context.py <source.md> <translated.md>
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

from markdown_link_utils import (
    MarkdownLink,
    extract_internal_markdown_links,
    extract_version_from_path,
    replace_version_placeholders,
)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "Usage: find_link_context.py <source.md> <translated.md>",
            file=sys.stderr,
        )
        return 2

    source_path = Path(argv[1])
    translated_path = Path(argv[2])
    source = source_path.read_text(encoding="utf-8")
    translated = translated_path.read_text(encoding="utf-8")
    version = extract_version_from_path(str(source_path)) or ""

    src_links: list[MarkdownLink] = [
        MarkdownLink(text=link.text, url=replace_version_placeholders(link.url, version))
        for link in extract_internal_markdown_links(source)
    ]
    tr_links = list(extract_internal_markdown_links(translated))

    tr_count = Counter(link.url for link in tr_links)
    seen_src: Counter[str] = Counter()
    missing: list[MarkdownLink] = []
    for link in src_links:
        seen_src[link.url] += 1
        found = tr_count.get(link.url, 0)
        if seen_src[link.url] > found:
            missing.append(link)

    print(f"Missing links count: {len(missing)}")
    for link in missing:
        # `(/docs/{{version}}/...)` 형태도 함께 검색해 컨텍스트를 찾는다.
        placeholder_url = (
            link.url.replace(version, "{{version}}") if version else link.url
        )
        position = -1
        for pattern in (link.url, placeholder_url):
            position = source.find(f"]({pattern})")
            if position >= 0:
                break
        if position < 0:
            print(f"\n  [{link.url}] (text: \"{link.text}\") — context not found")
            continue
        start = max(0, position - 200)
        end = min(len(source), position + 200)
        context = source[start:end].replace("\n", " ")
        print(f"\n  [{link.url}] (text: \"{link.text}\")")
        print(f"  source context: \"...{context[:400]}...\"")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
