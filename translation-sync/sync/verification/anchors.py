"""최종 빌드 HTML의 내부 문서 앵커를 검증하는 독립 CLI.

Markdown 원문 대신 출력 페이지의 href와 id/name을 검사한다.
placeholder와 stale 링크는 렌더러가 처리한 결과를 그대로 검증한다.
진단 위치는 원문 파일이 아닌 출력 HTML 파일과 줄 번호다.
"""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import quote, unquote, urljoin, urlsplit, urlunsplit


class HtmlPage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.anchors = set()
        self.links = []
        self.canonical = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id") is not None:
            self.anchors.add(attributes["id"])
        if tag == "a" and attributes.get("name") is not None:
            self.anchors.add(attributes["name"])
        if tag in {"a", "area"} and attributes.get("href") is not None:
            self.links.append((attributes["href"], self.getpos()[0]))
        if tag == "link" and "canonical" in attributes.get("rel", "").split():
            self.canonical = attributes.get("href")


def decode_component(value):
    if re.search(r"%(?![0-9a-fA-F]{2})", value):
        raise ValueError("invalid URL encoding")
    try:
        return unquote(value, errors="strict")
    except UnicodeDecodeError as error:
        raise ValueError("invalid URL encoding") from error


def origin(url):
    port = url.port if url.port is not None else (443 if url.scheme == "https" else 80)
    return url.scheme.lower(), url.hostname, port


def validate_anchors(build_root):
    root = Path(build_root).resolve()
    if not root.is_dir():
        raise ValueError(f"build directory not found: {root}; run npm run build first")

    pages = {}
    for path in sorted(root.rglob("*.html")):
        if not path.resolve().is_relative_to(root):
            continue
        page = HtmlPage()
        page.feed(path.read_text(encoding="utf-8"))
        page.close()
        pages[path] = page

    home = pages.get(root / "index.html")
    if home is None or not home.canonical:
        raise ValueError("build/index.html must contain the site's canonical URL")
    site = urlsplit(home.canonical)
    if site.scheme not in {"https", "http"} or not site.hostname:
        raise ValueError("the homepage canonical URL must be an absolute HTTP URL")
    base_path = decode_component(site.path).rstrip("/") + "/"
    site_url = urlunsplit((site.scheme, site.netloc, site.path.rstrip("/") + "/", "", ""))
    site_origin = origin(site)
    total = 0
    broken = []

    for source, page in pages.items():
        relative = source.relative_to(root).as_posix()
        route = relative.removesuffix("index.html") if relative.endswith("/index.html") else relative
        if relative == "index.html":
            route = ""
        source_url = urljoin(site_url, quote(route))

        for href, line in page.links:
            if "#" not in href:
                continue
            try:
                target = urlsplit(urljoin(source_url, href))
                if target.scheme not in {"http", "https"} or origin(target) != site_origin:
                    continue
            except ValueError as error:
                total += 1
                broken.append(f"{relative}:{line} -> {href}: {error}")
                continue
            path = unquote(target.path)
            local_path = path.removeprefix(base_path)
            parts = local_path.strip("/").split("/")
            if not (parts[0] == "docs" or len(parts) > 1 and parts[1] == "docs"):
                continue

            total += 1
            try:
                path = decode_component(target.path)
                if not path.startswith(base_path) or "\\" in path:
                    raise ValueError("target path outside build")
                target_file = root / path.removeprefix(base_path)
                if not path.endswith(".html"):
                    target_file /= "index.html"
                target_file = target_file.resolve()
                if not target_file.is_relative_to(root):
                    raise ValueError("target path outside build")
                target_page = pages.get(target_file)
                if target_page is None:
                    raise ValueError("target HTML missing")
                anchor = decode_component(target.fragment)
                if anchor and anchor not in target_page.anchors:
                    raise ValueError("anchor id/name not found")
            except ValueError as error:
                broken.append(f"{relative}:{line} -> {href}: {error}")

    return total, broken


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "build_root", nargs="?", type=Path,
        default=Path(__file__).resolve().parents[3] / "build",
    )
    args = parser.parse_args(argv)
    try:
        total, broken = validate_anchors(args.build_root)
    except (OSError, ValueError) as error:
        print(f"[validate-anchors] {error}", file=sys.stderr)
        return 2
    print(f"Total HTML anchor links: {total}")
    print(f"  OK: {total - len(broken)}")
    print(f"  Broken: {len(broken)}")
    for diagnostic in broken:
        print(f"  {diagnostic}")
    return 1 if broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
