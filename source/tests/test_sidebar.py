import json
import os
import tempfile

import pytest

from utils.sidebar import generate_all_sidebars, generate_sidebar, parse_documentation_md

SAMPLE_DOC = """- ## Prologue
    - [Release Notes](/docs/{{version}}/releases)
    - [Upgrade Guide](/docs/{{version}}/upgrade)
- ## Getting Started
    - [Installation](/docs/{{version}}/installation)
    - [Configuration](/docs/{{version}}/configuration)
- [API Documentation](https://api.laravel.com/docs/{{version}})
"""

SAMPLE_DOC_WITH_ANCHORS = """- ## Category
    - [Starter Kits](/docs/{{version}}/starter-kits#laravel-breeze)
    - [Installation](/docs/{{version}}/installation)
"""


class TestParseDocumentationMd:
    def test_parses_categories(self):
        sidebar = parse_documentation_md(SAMPLE_DOC, "12.x")
        categories = [
            item for item in sidebar["tutorialSidebar"] if item["type"] == "category"
        ]
        assert len(categories) == 2
        assert categories[0]["label"] == "Prologue"
        assert categories[1]["label"] == "Getting Started"

    def test_parses_items(self):
        sidebar = parse_documentation_md(SAMPLE_DOC, "12.x")
        prologue = sidebar["tutorialSidebar"][0]
        assert prologue["items"] == ["releases", "upgrade"]

        getting_started = sidebar["tutorialSidebar"][1]
        assert getting_started["items"] == ["installation", "configuration"]

    def test_first_category_collapsed(self):
        sidebar = parse_documentation_md(SAMPLE_DOC, "12.x")
        assert sidebar["tutorialSidebar"][0]["collapsed"] is True

    def test_second_category_expanded(self):
        sidebar = parse_documentation_md(SAMPLE_DOC, "12.x")
        assert sidebar["tutorialSidebar"][1]["collapsed"] is False

    def test_api_documentation_link(self):
        sidebar = parse_documentation_md(SAMPLE_DOC, "12.x")
        api_link = sidebar["tutorialSidebar"][-1]
        assert api_link["type"] == "link"
        assert api_link["label"] == "API Documentation"
        assert api_link["href"] == "https://api.laravel.com/docs/12.x"

    def test_version_placeholder_replaced_in_api_url(self):
        sidebar = parse_documentation_md(SAMPLE_DOC, "11.x")
        api_link = sidebar["tutorialSidebar"][-1]
        assert api_link["href"] == "https://api.laravel.com/docs/11.x"

    def test_anchor_links_stripped(self):
        sidebar = parse_documentation_md(SAMPLE_DOC_WITH_ANCHORS, "12.x")
        category = sidebar["tutorialSidebar"][0]
        assert category["items"] == ["starter-kits", "installation"]

    def test_empty_content(self):
        sidebar = parse_documentation_md("", "12.x")
        assert sidebar["tutorialSidebar"] == []

    def test_single_category_stays_collapsed(self):
        doc = "- ## Only Category\n    - [Item](/docs/{{version}}/item)\n"
        sidebar = parse_documentation_md(doc, "12.x")
        assert len(sidebar["tutorialSidebar"]) == 1
        assert sidebar["tutorialSidebar"][0]["collapsed"] is True


class TestGenerateSidebar:
    def test_generates_json_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Set up directory structure
            version = "12.x"
            doc_dir = os.path.join(tmpdir, "versioned_docs", f"version-{version}", "origin")
            sidebar_dir = os.path.join(tmpdir, "versioned_sidebars")
            os.makedirs(doc_dir)

            with open(os.path.join(doc_dir, "documentation.md"), "w") as f:
                f.write(SAMPLE_DOC)

            result = generate_sidebar(version, tmpdir)
            assert result is True

            output_path = os.path.join(sidebar_dir, f"version-{version}-sidebars.json")
            assert os.path.exists(output_path)

            with open(output_path, "r") as f:
                sidebar = json.load(f)
            assert "tutorialSidebar" in sidebar
            assert len(sidebar["tutorialSidebar"]) == 3

    def test_returns_false_when_doc_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = generate_sidebar("99.x", tmpdir)
            assert result is False


class TestGenerateAllSidebars:
    def test_skips_master_branch(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Set up only 12.x
            doc_dir = os.path.join(tmpdir, "versioned_docs", "version-12.x", "origin")
            os.makedirs(doc_dir)
            with open(os.path.join(doc_dir, "documentation.md"), "w") as f:
                f.write(SAMPLE_DOC)

            generate_all_sidebars(["master", "12.x"], tmpdir)

            # Should generate 12.x but not master
            sidebar_dir = os.path.join(tmpdir, "versioned_sidebars")
            assert os.path.exists(os.path.join(sidebar_dir, "version-12.x-sidebars.json"))
            assert not os.path.exists(os.path.join(sidebar_dir, "version-master-sidebars.json"))
