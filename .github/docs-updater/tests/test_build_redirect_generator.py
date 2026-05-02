from __future__ import annotations

import json
from pathlib import Path

import build_redirect_generator as brg


def test_latest_stable_version_skips_master():
    assert brg.latest_stable_version(["master", "13.x", "12.x"]) == "13.x"


def test_latest_stable_version_falls_back_when_only_master():
    assert brg.latest_stable_version(["master"]) == "master"


def test_front_matter_slug_returns_normalized_slug():
    content = "---\nslug: /custom-page/\n---\n\n# Body\n"
    assert brg.front_matter_slug(content) == "custom-page"


def test_front_matter_slug_returns_none_when_missing():
    assert brg.front_matter_slug("# No front matter\n") is None
    assert brg.front_matter_slug("---\ntitle: x\n---\n\n# Body\n") is None


def test_collect_slugs_includes_root_default_and_filenames(tmp_path: Path):
    docs_root = tmp_path / "docs"
    docs_root.mkdir()
    (docs_root / "documentation.md").write_text("- ## TOC\n", encoding="utf-8")
    (docs_root / "readme.md").write_text("readme", encoding="utf-8")
    (docs_root / "installation.md").write_text(
        "---\nslug: /\n---\n\n# Installation\n",
        encoding="utf-8",
    )
    (docs_root / "routing.md").write_text("# Routing\n", encoding="utf-8")
    (docs_root / "custom.md").write_text(
        "---\nslug: /custom-page\n---\n\n# Custom\n",
        encoding="utf-8",
    )

    slugs = brg.collect_slugs(docs_root)

    assert slugs == {"", "routing", "custom-page"}


def test_create_latest_doc_redirects_writes_per_locale(tmp_path: Path):
    docs_root = tmp_path / "versioned_docs" / "version-13.x"
    docs_root.mkdir(parents=True)
    (tmp_path / "versions.json").write_text(
        json.dumps(["13.x", "master"]) + "\n",
        encoding="utf-8",
    )
    (docs_root / "installation.md").write_text(
        "---\nslug: /\n---\n\n# Installation\n",
        encoding="utf-8",
    )
    (docs_root / "routing.md").write_text("# Routing\n", encoding="utf-8")
    (docs_root / "custom.md").write_text(
        "---\nslug: /custom-page/\n---\n\n# Custom\n",
        encoding="utf-8",
    )

    count = brg.create_latest_doc_redirects(tmp_path, locales=("", "en"))

    assert count == 3
    root_redirect = (tmp_path / "build" / "docs" / "index.html").read_text(
        encoding="utf-8"
    )
    assert "/docs/13.x" in root_redirect
    routing_redirect = (
        tmp_path / "build" / "docs" / "routing" / "index.html"
    ).read_text(encoding="utf-8")
    assert "/docs/13.x/routing" in routing_redirect
    routing_clean_redirect = (
        tmp_path / "build" / "docs" / "routing.html"
    ).read_text(encoding="utf-8")
    assert "/docs/13.x/routing" in routing_clean_redirect
    custom_redirect = (
        tmp_path / "build" / "en" / "docs" / "custom-page" / "index.html"
    ).read_text(encoding="utf-8")
    assert "/en/docs/13.x/custom-page" in custom_redirect


def test_redirect_html_contains_meta_refresh_and_canonical():
    html = brg.redirect_html("/docs/13.x/routing")
    assert 'http-equiv="refresh"' in html
    assert '<link rel="canonical" href="/docs/13.x/routing">' in html
    assert "window.location.replace" in html
