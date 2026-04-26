import json
import os
from pathlib import Path
import tempfile

import main


def test_replace_version_placeholder_uses_branch_version():
    content = "See [events](/docs/{{version}}/events) and {{ version }}."

    assert main.replace_version_placeholder(content, "12.x") == (
        "See [events](/docs/12.x/events) and 12.x."
    )


def test_default_chunk_line_limit_is_conservative():
    assert main.MAX_CHUNK_LINES == 400


def test_branch_targets_cover_master_and_supported_versions():
    assert main.BRANCHES == ["master", "13.x", "12.x", "11.x", "10.x", "9.x", "8.x"]


def test_reusable_translation_branches_excludes_target_branch():
    assert "13.x" not in main.reusable_translation_branches("13.x")
    assert main.reusable_translation_branches("13.x")[0] == "12.x"


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


def test_split_markdown_chunks_does_not_split_inside_tilde_fenced_code():
    content = "\n".join(
        [
            "intro",
            "",
            "~~~php",
            "$items = [",
            "",
            "    'first',",
            "];",
            "~~~",
            "",
            "outro",
            "",
        ]
    )

    chunks = main.split_markdown_chunks(content, max_lines=3)

    assert "".join(chunks) == content
    assert any("~~~php\n$items" in chunk and "];\n~~~" in chunk for chunk in chunks)


def test_split_markdown_chunks_falls_back_without_blank_boundaries():
    content = "".join(f"line {index}\n" for index in range(30))

    chunks = main.split_markdown_chunks(content, max_lines=3)

    assert "".join(chunks) == content
    assert all(len(chunk.splitlines()) <= 13 for chunk in chunks)


def test_split_markdown_chunks_waits_for_fence_close_before_fallback():
    content = "intro\n\n```text\n" + "".join(
        f"line {index}\n" for index in range(20)
    ) + "```\n\noutro\n"

    chunks = main.split_markdown_chunks(content, max_lines=3)

    assert "".join(chunks) == content
    assert any(
        chunk.startswith("intro\n\n```text\n")
        and "line 19\n```\n" in chunk
        for chunk in chunks
    )


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


def test_parse_documentation_md_accepts_spaced_version_placeholder():
    content = "- ## Getting Started\n    - [Installation](/docs/{{ version }}/installation)\n"

    sidebar = main.parse_documentation_md(content, "12.x")

    assert sidebar["tutorialSidebar"][0]["items"] == ["installation"]


def test_generate_sidebar_writes_versioned_sidebar_json():
    with tempfile.TemporaryDirectory() as tmpdir:
        source_dir = os.path.join(tmpdir, "source", "version-12.x")
        os.makedirs(source_dir)
        with open(
            os.path.join(source_dir, "documentation.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write("- ## Prologue\n    - [Release Notes](/docs/{{version}}/releases)\n")

        assert main.generate_sidebar(tmpdir, "12.x", updater_root=tmpdir) is True

        output = os.path.join(tmpdir, "versioned_sidebars", "version-12.x-sidebars.json")
        with open(output, encoding="utf-8") as f:
            data = json.load(f)
        assert data["tutorialSidebar"][0]["items"] == ["releases"]


def test_generate_sidebars_includes_master(monkeypatch):
    calls = []

    def fake_generate_sidebar(repo_root, version, updater_root=main.UPDATER_ROOT):
        calls.append((repo_root, version, updater_root))
        return True

    monkeypatch.setattr(main, "generate_sidebar", fake_generate_sidebar)

    assert main.generate_sidebars("/repo", branches=["master", "13.x"]) is True
    assert [call[1] for call in calls] == ["master", "13.x"]


def test_validate_anchors_rejects_missing_anchor():
    source = '<a name="intro"></a>\n- [Intro](#intro)\n'
    translated = "- [소개](#intro)\n"

    is_valid, errors = main.validate_anchors(source, translated)

    assert is_valid is False
    assert any("intro" in error for error in errors)


def test_validate_anchors_ignores_tilde_fenced_blocks():
    source = '~~~html\n<a name="example"></a>\n~~~\n'
    translated = "~~~html\n<!-- translated example -->\n~~~\n"

    is_valid, errors = main.validate_anchors(source, translated)

    assert is_valid is True
    assert errors == []


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
        source_dir = os.path.join(
            tmpdir, ".github", "docs-updater", "source", "version-12.x"
        )
        os.makedirs(source_dir)
        source_file = os.path.join(source_dir, "routing.md")
        target_file = os.path.join(tmpdir, "versioned_docs", "version-12.x", "routing.md")
        with open(source_file, "w", encoding="utf-8") as f:
            f.write(source)

        assert main.translate_file(source_file, target_file, max_lines=2) is True

        with open(target_file, encoding="utf-8") as f:
            assert '<a name="intro"></a>' in f.read()


def test_sync_branch_docs_removes_stale_source_cache_and_translation():
    with tempfile.TemporaryDirectory() as tmpdir:
        upstream = os.path.join(tmpdir, "upstream")
        source_dir = os.path.join(
            tmpdir, ".github", "docs-updater", "source", "version-12.x"
        )
        docs_dir = os.path.join(tmpdir, "versioned_docs", "version-12.x")
        os.makedirs(upstream)
        os.makedirs(source_dir)
        os.makedirs(docs_dir)

        with open(os.path.join(upstream, "routing.md"), "w", encoding="utf-8") as f:
            f.write("# Routing\n")
        with open(os.path.join(upstream, "license.md"), "w", encoding="utf-8") as f:
            f.write("license\n")
        with open(os.path.join(source_dir, "old.md"), "w", encoding="utf-8") as f:
            f.write("old\n")
        with open(os.path.join(docs_dir, "old.md"), "w", encoding="utf-8") as f:
            f.write("old translated\n")

        main.sync_branch_docs(upstream, source_dir, docs_dir, {"license.md"})

        assert os.path.exists(os.path.join(source_dir, "routing.md"))
        assert os.path.exists(os.path.join(docs_dir, "license.md"))
        assert not os.path.exists(os.path.join(source_dir, "old.md"))
        assert not os.path.exists(os.path.join(docs_dir, "old.md"))


def test_sync_branch_docs_replaces_version_placeholder_in_excluded_rendered_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        upstream = os.path.join(tmpdir, "upstream")
        source_dir = os.path.join(
            tmpdir, ".github", "docs-updater", "source", "version-11.x"
        )
        docs_dir = os.path.join(tmpdir, "versioned_docs", "version-11.x")
        os.makedirs(upstream)

        with open(
            os.path.join(upstream, "documentation.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write("- [Routing](/docs/{{version}}/routing)\n")

        main.sync_branch_docs(upstream, source_dir, docs_dir, {"documentation.md"})

        rendered_file = os.path.join(docs_dir, "documentation.md")
        source_file = os.path.join(source_dir, "documentation.md")
        with open(rendered_file, encoding="utf-8") as f:
            rendered = f.read()
        with open(source_file, encoding="utf-8") as f:
            source = f.read()

        assert "/docs/11.x/routing" in rendered
        assert "{{version}}" not in rendered
        assert "/docs/{{version}}/routing" in source


def test_extract_changed_source_files_from_git_status():
    status = (
        " M .github/docs-updater/source/version-12.x/routing.md\n"
        "?? .github/docs-updater/source/version-11.x/new.md\n"
        " M versioned_docs/version-12.x/routing.md\n"
        " D .github/docs-updater/source/version-10.x/old.md\n"
    )

    assert main.extract_changed_source_files(status) == [
        ".github/docs-updater/source/version-10.x/old.md",
        ".github/docs-updater/source/version-11.x/new.md",
        ".github/docs-updater/source/version-12.x/routing.md",
    ]


def test_main_returns_nonzero_when_clone_fails(monkeypatch):
    monkeypatch.setattr(main, "clone_docs", lambda *_args: False)

    assert main.main() == 1


def test_main_retries_rate_limit_once(monkeypatch):
    class FakeRateLimitError(Exception):
        pass

    attempts = []

    def fake_translate_file(_source_path, _target_path):
        attempts.append("attempt")
        if len(attempts) == 1:
            raise FakeRateLimitError("rate limit")
        return True

    with tempfile.TemporaryDirectory() as tmpdir:
        repo_root = Path(tmpdir)
        updater_root = repo_root / ".github" / "docs-updater"
        source_dir = updater_root / "source" / "version-12.x"
        source_dir.mkdir(parents=True)
        (source_dir / "routing.md").write_text("# Routing\n", encoding="utf-8")

        monkeypatch.setattr(main, "REPO_ROOT", repo_root)
        monkeypatch.setattr(main, "UPDATER_ROOT", updater_root)
        monkeypatch.setattr(main.openai, "RateLimitError", FakeRateLimitError)
        monkeypatch.setattr(main, "BRANCHES", [])
        monkeypatch.setattr(main, "clone_docs", lambda *_args: True)
        monkeypatch.setattr(main, "generate_sidebars", lambda *_args: True)
        monkeypatch.setattr(main, "get_changed_source_files", lambda *_args: [
            ".github/docs-updater/source/version-12.x/routing.md",
        ])
        monkeypatch.setattr(main, "read_translation_delay", lambda: 0)
        monkeypatch.setattr(main, "translate_file", fake_translate_file)
        monkeypatch.setattr(main, "stage_outputs", lambda *_args: True)
        monkeypatch.setattr(main.time, "sleep", lambda *_args: None)

        assert main.main() == 0

    assert len(attempts) == 2


def test_main_reports_failure_when_rate_limit_retry_fails(monkeypatch):
    class FakeRateLimitError(Exception):
        pass

    attempts = []

    def fake_translate_file(_source_path, _target_path):
        attempts.append("attempt")
        raise FakeRateLimitError("rate limit")

    with tempfile.TemporaryDirectory() as tmpdir:
        repo_root = Path(tmpdir)
        updater_root = repo_root / ".github" / "docs-updater"
        source_dir = updater_root / "source" / "version-12.x"
        source_dir.mkdir(parents=True)
        (source_dir / "routing.md").write_text("# Routing\n", encoding="utf-8")

        monkeypatch.setattr(main, "REPO_ROOT", repo_root)
        monkeypatch.setattr(main, "UPDATER_ROOT", updater_root)
        monkeypatch.setattr(main.openai, "RateLimitError", FakeRateLimitError)
        monkeypatch.setattr(main, "BRANCHES", [])
        monkeypatch.setattr(main, "clone_docs", lambda *_args: True)
        monkeypatch.setattr(main, "generate_sidebars", lambda *_args: True)
        monkeypatch.setattr(main, "get_changed_source_files", lambda *_args: [
            ".github/docs-updater/source/version-12.x/routing.md",
        ])
        monkeypatch.setattr(main, "read_translation_delay", lambda: 0)
        monkeypatch.setattr(main, "translate_file", fake_translate_file)
        monkeypatch.setattr(main, "stage_outputs", lambda *_args: True)
        monkeypatch.setattr(main.time, "sleep", lambda *_args: None)

        assert main.main() == 1

    assert len(attempts) == 2
