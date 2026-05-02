from __future__ import annotations

from pathlib import Path

import build_anchor_validator as bav


def test_to_url_path_treats_installation_as_version_root(tmp_path: Path):
    docs_root = tmp_path / "versioned_docs"
    md = docs_root / "version-13.x" / "installation.md"
    md.parent.mkdir(parents=True)
    md.write_text("# Installation\n", encoding="utf-8")
    assert bav.to_url_path(docs_root, md) == "/docs/13.x"


def test_to_url_path_uses_slug_for_other_files(tmp_path: Path):
    docs_root = tmp_path / "versioned_docs"
    md = docs_root / "version-13.x" / "routing.md"
    md.parent.mkdir(parents=True)
    md.write_text("# Routing\n", encoding="utf-8")
    assert bav.to_url_path(docs_root, md) == "/docs/13.x/routing"


def test_target_from_href_resolves_relative_paths_with_version():
    target, anchor = bav._target_from_href(
        "requests#request-data", "/docs/13.x/routing", "13.x"
    )
    assert target == "/docs/13.x/requests"
    assert anchor == "request-data"


def test_target_from_href_handles_pure_anchor_links():
    target, anchor = bav._target_from_href(
        "#intro", "/docs/13.x/routing", "13.x"
    )
    assert target == "/docs/13.x/routing"
    assert anchor == "intro"


def test_target_from_href_replaces_version_placeholder_in_path():
    target, anchor = bav._target_from_href(
        "/docs/{{version}}/installation#install",
        "/docs/13.x/routing",
        "13.x",
    )
    assert target == "/docs/13.x"
    assert anchor == "install"


def test_validate_anchors_succeeds_when_all_ids_present(tmp_path: Path):
    docs_root = tmp_path / "versioned_docs" / "version-13.x"
    docs_root.mkdir(parents=True)
    (docs_root / "routing.md").write_text(
        "[Intro](#intro)\n"
        "[Install](/docs/{{version}}/installation#install)\n"
        "[Requests](requests#request-data)\n",
        encoding="utf-8",
    )

    for path, html in {
        "build/docs/13.x/routing.html": '<h2 id="intro">Intro</h2>',
        "build/docs/13.x.html": '<h2 id="install">Install</h2>',
        "build/docs/13.x/requests.html": '<h2 id="request-data">Data</h2>',
    }.items():
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")

    report = bav.validate_anchors(tmp_path)

    assert report.total == 3
    assert report.ok == 3
    assert report.missing_html == 0
    assert report.id_not_found == 0
    assert report.has_failures is False


def test_validate_anchors_reports_missing_target_html(tmp_path: Path):
    docs_root = tmp_path / "versioned_docs" / "version-13.x"
    docs_root.mkdir(parents=True)
    (docs_root / "routing.md").write_text(
        "[Missing](/docs/{{version}}/missing#intro)\n",
        encoding="utf-8",
    )
    (tmp_path / "build").mkdir()

    report = bav.validate_anchors(tmp_path)

    assert report.total == 1
    assert report.missing_html == 1
    assert report.broken[0].reason == "target HTML missing"


def test_validate_anchors_reports_id_not_found(tmp_path: Path):
    docs_root = tmp_path / "versioned_docs" / "version-13.x"
    docs_root.mkdir(parents=True)
    (docs_root / "routing.md").write_text(
        "[Intro](#intro)\n",
        encoding="utf-8",
    )
    target = tmp_path / "build/docs/13.x/routing/index.html"
    target.parent.mkdir(parents=True)
    target.write_text("<h2>No matching id here</h2>", encoding="utf-8")

    report = bav.validate_anchors(tmp_path)

    assert report.total == 1
    assert report.id_not_found == 1
    assert report.broken[0].reason == "id not found in HTML"


def test_validate_anchors_raises_when_build_missing(tmp_path: Path):
    (tmp_path / "versioned_docs").mkdir()
    try:
        bav.validate_anchors(tmp_path)
    except FileNotFoundError as error:
        assert "build/" in str(error)
    else:
        raise AssertionError("expected FileNotFoundError")
