from pathlib import Path

import structure_validator as sv


def test_extract_anchors_returns_explicit_anchor_ids():
    text = (
        '<a name="intro"></a>\n'
        "## Introduction\n"
        '<a name="setup"/>\n'
        'Inline code `<a name="ignored">` is not an anchor definition.\n'
    )
    assert sv.extract_anchors(text) == ["intro", "setup"]


def test_extract_anchors_ignores_anchors_inside_fenced_code():
    text = '```html\n<a name="ignored"></a>\n```\n<a name="kept"></a>\n'
    assert sv.extract_anchors(text) == ["kept"]


def test_extract_headings_collects_atx_headings_with_levels():
    text = "# Title\n\n## Sub\n\n### Sub-sub\n\nNot a # heading\n"
    headings = sv.extract_headings(text)
    assert [(heading.level, heading.text) for heading in headings] == [
        (1, "Title"),
        (2, "Sub"),
        (3, "Sub-sub"),
    ]


def test_normalize_internal_link_rewrites_laravel_docs_prefix():
    assert (
        sv.normalize_internal_link(
            "https://laravel.com/docs/12.x/routing#named", "12.x"
        )
        == "/docs/12.x/routing#named"
    )


def test_normalize_internal_link_drops_known_stale_anchor_aliases():
    assert sv.normalize_internal_link("#assert-similar-json", "12.x") is None
    assert (
        sv.normalize_internal_link("/docs/12.x/errors#logging", "12.x")
        == "/docs/12.x/logging"
    )


def test_normalize_internal_link_replaces_agents_integration():
    assert (
        sv.normalize_internal_link("#agents-integration", "12.x")
        == "#agent-integration"
    )


def test_compare_link_targets_reports_count_mismatch():
    source = "[a](/docs/{{version}}/x)\n[a](/docs/{{version}}/x)\n"
    translated = "[a](/docs/12.x/x)\n"
    diffs = sv.compare_link_targets(source, translated, "12.x")
    assert len(diffs) == 1
    assert diffs[0].link == "/docs/12.x/x"
    assert diffs[0].source == 2
    assert diffs[0].translated == 1


def test_compare_returns_no_issues_when_translation_matches():
    source = (
        '<a name="intro"></a>\n'
        "## Intro\n"
        "[Routing](/docs/{{version}}/routing)\n"
    )
    translated = (
        '<a name="intro"></a>\n'
        "## 소개\n"
        "[라우팅](/docs/12.x/routing)\n"
    )
    assert sv.compare(source, translated, "12.x") == ()


def test_compare_detects_missing_anchor_in_translation():
    source = '<a name="intro"></a>\n## Intro\n'
    translated = "## 소개\n"
    issues = sv.compare(source, translated, "12.x")
    types = [issue.type for issue in issues]
    assert "anchor-missing" in types


def test_compare_detects_extra_anchor_in_translation():
    source = "## Intro\n"
    translated = '<a name="extra"></a>\n## 소개\n'
    issues = sv.compare(source, translated, "12.x")
    types = [issue.type for issue in issues]
    assert "anchor-extra" in types


def test_compare_reports_heading_level_difference_when_count_matches():
    source = "## A\n## B\n"
    translated = "### A\n## B\n"
    issues = sv.compare(source, translated, "12.x")
    assert any(issue.type == "heading-level" for issue in issues)


def test_compare_reports_heading_count_difference():
    source = "## A\n## B\n"
    translated = "## A\n"
    issues = sv.compare(source, translated, "12.x")
    types = [issue.type for issue in issues]
    assert "heading-count" in types


def test_validate_structure_flags_missing_translation(tmp_path: Path):
    source_root = tmp_path / "source"
    docs_root = tmp_path / "docs"
    version_dir = source_root / "version-12.x"
    docs_version = docs_root / "version-12.x"
    version_dir.mkdir(parents=True)
    docs_version.mkdir(parents=True)
    (version_dir / "routing.md").write_text(
        '<a name="intro"></a>\n## Intro\n', encoding="utf-8"
    )

    report = sv.validate_structure(source_root, docs_root)

    assert report.total == 1
    assert report.files_with_issues == 1
    assert report.issues[0].issues[0].type == "translation-missing"


def test_validate_structure_skips_excluded_files(tmp_path: Path):
    source_root = tmp_path / "source"
    docs_root = tmp_path / "docs"
    version_dir = source_root / "version-12.x"
    docs_version = docs_root / "version-12.x"
    version_dir.mkdir(parents=True)
    docs_version.mkdir(parents=True)
    (version_dir / "license.md").write_text("LICENSE", encoding="utf-8")
    (version_dir / "documentation.md").write_text("- ## Topic\n", encoding="utf-8")
    (version_dir / "readme.md").write_text("readme", encoding="utf-8")

    report = sv.validate_structure(source_root, docs_root)

    assert report.total == 0
    assert report.files_with_issues == 0


def test_validate_structure_succeeds_when_translation_matches(tmp_path: Path):
    source_root = tmp_path / "source"
    docs_root = tmp_path / "docs"
    version_dir = source_root / "version-12.x"
    docs_version = docs_root / "version-12.x"
    version_dir.mkdir(parents=True)
    docs_version.mkdir(parents=True)
    body = '<a name="intro"></a>\n## Intro\n[Routing](/docs/{{version}}/routing)\n'
    (version_dir / "routing.md").write_text(body, encoding="utf-8")
    translation = (
        '<a name="intro"></a>\n## 소개\n[라우팅](/docs/12.x/routing)\n'
    )
    (docs_version / "routing.md").write_text(translation, encoding="utf-8")

    report = sv.validate_structure(source_root, docs_root)

    assert report.total == 1
    assert report.files_with_issues == 0
    assert report.has_issues is False


def test_render_report_returns_summary_only_when_no_issues():
    report = sv.StructureReport(total=3, files_with_issues=0, issues=[])
    text = sv.render_report(report)
    assert "Total: 3 files" in text
    assert "Files with structural issues: 0" in text
    assert "Detailed issues" not in text


def test_render_report_includes_grouped_breakdown():
    report = sv.StructureReport(
        total=2,
        files_with_issues=1,
        issues=[
            sv.FileIssues(
                version="version-12.x",
                file="routing.md",
                issues=(sv.StructureIssue(type="anchor-missing", detail=["intro"]),),
            )
        ],
    )
    text = sv.render_report(report)
    assert "Issues by version" in text
    assert "version-12.x: 1" in text
    assert "anchor-missing: 1" in text
    assert "[version-12.x/routing.md]" in text
