import json
import os
import tempfile

import main


def test_replace_version_placeholder_uses_branch_version():
    content = "See [events](/docs/{{version}}/events) and {{ version }}."

    assert main.replace_version_placeholder(content, "12.x") == (
        "See [events](/docs/12.x/events) and 12.x."
    )


def test_split_markdown_chunks_uses_blank_boundaries_after_line_limit():
    content = "\n".join(
        [
            "a1",
            "a2",
            "",
            "b1",
            "b2",
            "b3",
            "",
            "c1",
            "c2",
            "",
        ]
    )

    chunks = main.split_markdown_chunks(content, max_lines=2)

    assert chunks == ["a1\na2\n\n", "b1\nb2\nb3\n\n", "c1\nc2\n"]


def test_split_markdown_chunks_does_not_split_inside_fenced_code():
    content = "\n".join(
        [
            "intro",
            "",
            "```php",
            "$items = [",
            "",
            "    'first',",
            "];",
            "```",
            "",
            "outro",
            "",
        ]
    )

    chunks = main.split_markdown_chunks(content, max_lines=3)

    assert "".join(chunks) == content
    assert any("```php\n$items" in chunk and "];\n```" in chunk for chunk in chunks)


def test_parse_documentation_md_creates_sidebar():
    content = (
        "- ## Prologue\n"
        "    - [Release Notes](/docs/{{version}}/releases)\n"
        "- ## Getting Started\n"
        "    - [Installation](/docs/{{version}}/installation#server-requirements)\n"
        "- [API Documentation](https://api.laravel.com/docs/{{version}})\n"
    )

    sidebar = main.parse_documentation_md(content, "12.x")

    assert sidebar["tutorialSidebar"][0]["label"] == "Prologue"
    assert sidebar["tutorialSidebar"][1]["collapsed"] is False
    assert sidebar["tutorialSidebar"][1]["items"] == ["installation"]
    assert sidebar["tutorialSidebar"][2]["href"] == "https://api.laravel.com/docs/12.x"


def test_generate_sidebar_writes_versioned_sidebar_json():
    with tempfile.TemporaryDirectory() as tmpdir:
        origin_dir = os.path.join(tmpdir, "versioned_docs", "version-12.x", "origin")
        os.makedirs(origin_dir)
        with open(
            os.path.join(origin_dir, "documentation.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write("- ## Prologue\n    - [Release Notes](/docs/{{version}}/releases)\n")

        assert main.generate_sidebar(tmpdir, "12.x") is True

        output = os.path.join(tmpdir, "versioned_sidebars", "version-12.x-sidebars.json")
        with open(output, encoding="utf-8") as f:
            data = json.load(f)
        assert data["tutorialSidebar"][0]["items"] == ["releases"]


def test_validate_anchors_rejects_missing_anchor():
    source = '<a name="intro"></a>\n- [Intro](#intro)\n'
    translated = "- [소개](#intro)\n"

    is_valid, errors = main.validate_anchors(source, translated)

    assert is_valid is False
    assert any("intro" in error for error in errors)


def test_prepare_translation_content_replaces_version_only():
    content = (
        "# Title {.kept}\n\n"
        "> {note} Kept as source syntax.\n\n"
        '<img src="/x.png">\n\n'
        "See /docs/{{version}}/queues.\n"
    )

    result = main.prepare_translation_content(content, "11.x")

    assert "# Title {.kept}" in result
    assert "> {note} Kept as source syntax." in result
    assert '<img src="/x.png">' in result
    assert "/docs/11.x/queues" in result


def test_translate_markdown_content_splits_long_documents(monkeypatch):
    calls = []

    def fake_translate(text, system_prompt):
        calls.append(text)
        return text.upper()

    monkeypatch.setattr(main, "translate_text", fake_translate)
    content = "a1\na2\n\nb1\nb2\n\nc1\nc2\n"

    result = main.translate_markdown_content(content, "prompt", max_lines=3)

    assert len(calls) == 3
    assert result == "A1\nA2\n\nB1\nB2\n\nC1\nC2\n"


def test_translate_file_validates_after_joined_translation(monkeypatch):
    source = '<a name="intro"></a>\n## Intro\n'

    def fake_translate(text, system_prompt):
        return text.replace("Intro", "소개")

    monkeypatch.setattr(main, "translate_text", fake_translate)
    monkeypatch.setattr(main, "get_system_prompt", lambda: "prompt")

    with tempfile.TemporaryDirectory() as tmpdir:
        source_dir = os.path.join(tmpdir, "versioned_docs", "version-12.x", "origin")
        os.makedirs(source_dir)
        source_file = os.path.join(source_dir, "routing.md")
        target_file = os.path.join(tmpdir, "versioned_docs", "version-12.x", "routing.md")
        with open(source_file, "w", encoding="utf-8") as f:
            f.write(source)

        assert main.translate_file(source_file, target_file, max_lines=2) is True

        with open(target_file, encoding="utf-8") as f:
            assert '<a name="intro"></a>' in f.read()


def test_sync_branch_docs_removes_stale_origin_and_translation():
    with tempfile.TemporaryDirectory() as tmpdir:
        upstream = os.path.join(tmpdir, "upstream")
        docs_dir = os.path.join(tmpdir, "versioned_docs", "version-12.x")
        origin_dir = os.path.join(docs_dir, "origin")
        os.makedirs(upstream)
        os.makedirs(origin_dir)

        with open(os.path.join(upstream, "routing.md"), "w", encoding="utf-8") as f:
            f.write("# Routing\n")
        with open(os.path.join(upstream, "license.md"), "w", encoding="utf-8") as f:
            f.write("license\n")
        with open(os.path.join(origin_dir, "old.md"), "w", encoding="utf-8") as f:
            f.write("old\n")
        with open(os.path.join(docs_dir, "old.md"), "w", encoding="utf-8") as f:
            f.write("old translated\n")

        main.sync_branch_docs(upstream, docs_dir, {"license.md"})

        assert os.path.exists(os.path.join(origin_dir, "routing.md"))
        assert os.path.exists(os.path.join(docs_dir, "license.md"))
        assert not os.path.exists(os.path.join(origin_dir, "old.md"))
        assert not os.path.exists(os.path.join(docs_dir, "old.md"))


def test_extract_changed_origin_files_from_git_status():
    status = (
        " M versioned_docs/version-12.x/origin/routing.md\n"
        "?? versioned_docs/version-11.x/origin/new.md\n"
        " M versioned_docs/version-12.x/routing.md\n"
        " D versioned_docs/version-10.x/origin/old.md\n"
    )

    assert main.extract_changed_origin_files(status) == [
        "versioned_docs/version-10.x/origin/old.md",
        "versioned_docs/version-11.x/origin/new.md",
        "versioned_docs/version-12.x/origin/routing.md",
    ]


def test_main_returns_nonzero_when_clone_fails(monkeypatch):
    monkeypatch.setattr(main, "clone_docs", lambda *_args: False)

    assert main.main() == 1
