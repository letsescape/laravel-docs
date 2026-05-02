"""Report missing or extra internal links between source and translation.

원문/번역본의 내부 링크 대상을 multiset 으로 비교해 어느 링크가 빠지거나
추가됐는지 출력한다. 디버깅 도구라서 update 워크플로우에서는 호출하지 않는다.

Usage:
    uv run python find_missing_links.py <source.md> <translated.md>
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

from markdown_link_utils import (
    extract_internal_markdown_links,
    extract_version_from_path,
    replace_version_placeholders,
)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "Usage: find_missing_links.py <source.md> <translated.md>",
            file=sys.stderr,
        )
        return 2

    source_path = Path(argv[1])
    translated_path = Path(argv[2])
    source = source_path.read_text(encoding="utf-8")
    translated = translated_path.read_text(encoding="utf-8")
    version = extract_version_from_path(str(source_path)) or ""

    src_links = [
        replace_version_placeholders(link.url, version)
        for link in extract_internal_markdown_links(source)
    ]
    tr_links = [link.url for link in extract_internal_markdown_links(translated)]

    print(f"Source links: {len(src_links)}")
    print(f"Translated links: {len(tr_links)}")

    src_count = Counter(src_links)
    tr_count = Counter(tr_links)

    missing: list[tuple[str, int, int]] = []
    extra: list[tuple[str, int, int]] = []
    for url in sorted(set(src_count) | set(tr_count)):
        s = src_count.get(url, 0)
        t = tr_count.get(url, 0)
        if s > t:
            missing.append((url, s, t))
        elif t > s:
            extra.append((url, s, t))

    if missing:
        print("\nLinks missing in translation:")
        for url, s, t in missing:
            print(f"  {url} (source={s}, translated={t})")
    if extra:
        print("\nLinks extra in translation:")
        for url, s, t in extra:
            print(f"  {url} (source={s}, translated={t})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
