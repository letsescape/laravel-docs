import json
import os
from pathlib import Path
import subprocess
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


def test_parse_documentation_md_uses_latest_stable_api_link_for_master():
    content = "- [API Documentation](https://api.laravel.com/docs/{{version}})\n"

    sidebar = main.parse_documentation_md(content, "master", latest_stable="13.x")

    assert sidebar["tutorialSidebar"][0]["href"] == "https://api.laravel.com/docs/13.x"


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

    def fake_generate_sidebar(
        repo_root,
        version,
        updater_root=main.UPDATER_ROOT,
        latest_stable=None,
    ):
        calls.append((repo_root, version, updater_root, latest_stable))
        return True

    monkeypatch.setattr(main, "generate_sidebar", fake_generate_sidebar)

    assert main.generate_sidebars("/repo", branches=["master", "13.x"]) is True
    assert [call[1] for call in calls] == ["master", "13.x"]
    assert [call[3] for call in calls] == ["13.x", "13.x"]


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


def test_validate_anchors_keeps_anchors_after_unmatched_inline_backtick():
    source = (
        "Use the `using` method`:\n\n"
        "```php\n"
        "Route::get('/orders');\n"
        "```\n\n"
        '<a name="retrieving-tokens"></a>\n'
        "## Retrieving Tokens\n"
    )
    translated = source.replace("Retrieving Tokens", "토큰 조회")

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


def test_prepare_translation_content_normalizes_known_broken_anchor_reference():
    content = (
        "- [Agents Integration](#agents-integration)\n\n"
        '<a name="agent-integration"></a>\n'
        "### Agents Integration\n"
    )

    result = main.prepare_translation_content(content, "13.x")

    assert "#agents-integration" not in result
    assert "#agent-integration" in result


def test_ensure_docs_front_matter_adds_installation_slug():
    result = main.ensure_docs_front_matter("# 설치\n", "installation.md")

    assert result.startswith("---\nslug: /\n---\n\n# 설치\n")


def test_ensure_docs_front_matter_preserves_existing_front_matter():
    content = "---\nslug: /\n---\n\n# 설치\n"

    assert main.ensure_docs_front_matter(content, "installation.md") == content


def test_normalize_anchor_spacing_adds_blank_before_anchor():
    content = "문단입니다.\n<a name=\"intro\"></a>\n## Intro\n"

    result = main.normalize_anchor_spacing(content)

    assert result == "문단입니다.\n\n<a name=\"intro\"></a>\n## Intro\n"


def test_finalize_translation_content_combines_anchor_spacing_and_installation_slug():
    content = "# 설치\n\n문단입니다.\n<a name=\"intro\"></a>\n## Intro\n"

    result = main.finalize_translation_content(content, "installation.md")

    assert result.startswith("---\nslug: /\n---\n\n# 설치\n")
    assert "\n\n<a name=\"intro\"></a>\n## Intro\n" in result


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


def test_translate_text_uses_cli_provider(monkeypatch):
    calls = []

    def fake_run(args, **kwargs):
        calls.append((args, kwargs))
        return subprocess.CompletedProcess(args, 0, stdout="번역 결과\n", stderr="")

    monkeypatch.setenv("TRANSLATION_PROVIDER", "cli")
    monkeypatch.setenv("TRANSLATION_CLI_COMMAND", "ai translate")
    monkeypatch.setattr(main.subprocess, "run", fake_run)

    assert main.translate_text("# Hello\n", "system prompt") == "번역 결과\n"

    args, kwargs = calls[0]
    assert args == ["ai", "translate"]
    assert "system prompt" in kwargs["input"]
    assert "# Hello\n" in kwargs["input"]
    assert kwargs["text"] is True
    assert kwargs["capture_output"] is True
    assert kwargs["check"] is True


def test_translate_text_cli_requires_command(monkeypatch):
    monkeypatch.setenv("TRANSLATION_PROVIDER", "cli")
    monkeypatch.delenv("TRANSLATION_CLI_COMMAND", raising=False)

    try:
        main.translate_text("# Hello\n", "system prompt")
    except main.FatalCliError as error:
        assert "TRANSLATION_CLI_COMMAND" in str(error)
    else:
        raise AssertionError("expected TRANSLATION_CLI_COMMAND error")


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


def test_translate_file_adds_installation_slug(monkeypatch):
    def fake_translate(text, system_prompt):
        return text.replace("Installation", "설치")

    monkeypatch.setattr(main, "translate_text", fake_translate)
    monkeypatch.setattr(main, "get_system_prompt", lambda: "prompt")

    with tempfile.TemporaryDirectory() as tmpdir:
        source_dir = os.path.join(
            tmpdir, ".github", "docs-updater", "source", "version-13.x"
        )
        os.makedirs(source_dir)
        source_file = os.path.join(source_dir, "installation.md")
        target_file = os.path.join(
            tmpdir, "versioned_docs", "version-13.x", "installation.md"
        )
        with open(source_file, "w", encoding="utf-8") as f:
            f.write("# Installation\n")

        assert main.translate_file(source_file, target_file) is True

        with open(target_file, encoding="utf-8") as f:
            assert f.read().startswith("---\nslug: /\n---\n\n# 설치\n")


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


def test_get_changed_source_files_includes_untracked_files(monkeypatch):
    calls = []

    def fake_run_command(args, cwd=None):
        calls.append((args, cwd))
        return "?? .github/docs-updater/source/version-13.x/new.md\n"

    monkeypatch.setattr(main, "run_command", fake_run_command)

    assert main.get_changed_source_files("/repo") == [
        ".github/docs-updater/source/version-13.x/new.md",
    ]
    assert calls == [
        (
            ["git", "status", "--porcelain", "--untracked-files=all"],
            "/repo",
        )
    ]


def test_get_translation_source_files_includes_missing_targets(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_root = Path(tmpdir)
        updater_root = repo_root / ".github" / "docs-updater"
        source_dir = updater_root / "source" / "version-master"
        source_dir.mkdir(parents=True)
        (source_dir / "routing.md").write_text("# Routing\n", encoding="utf-8")

        monkeypatch.setattr(main, "get_changed_source_files", lambda _repo: [])

        assert main.get_translation_source_files(
            repo_root,
            branches=["master"],
            updater_root=updater_root,
        ) == [".github/docs-updater/source/version-master/routing.md"]


def test_try_reuse_translation_rewrites_version_placeholder_output():
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_root = Path(tmpdir)
        updater_root = repo_root / ".github" / "docs-updater"
        raw = (
            '<a name="intro"></a>\n'
            "See [Routing](/docs/{{version}}/routing#intro).\n"
        )

        source_13 = updater_root / "source" / "version-13.x"
        source_12 = updater_root / "source" / "version-12.x"
        target_12 = repo_root / "versioned_docs" / "version-12.x"
        for directory in (source_13, source_12, target_12):
            directory.mkdir(parents=True)

        (source_13 / "routing.md").write_text(raw, encoding="utf-8")
        (source_12 / "routing.md").write_text(raw, encoding="utf-8")
        (target_12 / "routing.md").write_text(
            '<a name="intro"></a>\nSee [라우팅](/docs/12.x/routing#intro).\n',
            encoding="utf-8",
        )

        target_13 = repo_root / "versioned_docs" / "version-13.x" / "routing.md"

        assert main.try_reuse_translation(
            source_13 / "routing.md",
            target_13,
            "13.x",
            repo_root,
            updater_root=updater_root,
        ) is True
        assert "/docs/13.x/routing#intro" in target_13.read_text(encoding="utf-8")


def test_try_reuse_translation_skips_literal_candidate_version():
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_root = Path(tmpdir)
        updater_root = repo_root / ".github" / "docs-updater"
        raw = "This text intentionally mentions 12.x.\n"

        source_13 = updater_root / "source" / "version-13.x"
        source_12 = updater_root / "source" / "version-12.x"
        target_12 = repo_root / "versioned_docs" / "version-12.x"
        for directory in (source_13, source_12, target_12):
            directory.mkdir(parents=True)

        (source_13 / "upgrade.md").write_text(raw, encoding="utf-8")
        (source_12 / "upgrade.md").write_text(raw, encoding="utf-8")
        (target_12 / "upgrade.md").write_text(
            "이 문장은 의도적으로 12.x를 언급합니다.\n",
            encoding="utf-8",
        )
        target_13 = repo_root / "versioned_docs" / "version-13.x" / "upgrade.md"

        assert main.try_reuse_translation(
            source_13 / "upgrade.md",
            target_13,
            "13.x",
            repo_root,
            updater_root=updater_root,
        ) is False
        assert not target_13.exists()


def test_main_returns_nonzero_when_clone_fails(monkeypatch):
    monkeypatch.setattr(main, "clone_docs", lambda *_args: False)

    assert main.main() == 1


class _FakeTransientError(Exception):
    """테스트용 일시적 오류."""


def _setup_main_fixture(monkeypatch, tmpdir, *, max_attempts=2):
    repo_root = Path(tmpdir)
    updater_root = repo_root / ".github" / "docs-updater"
    source_dir = updater_root / "source" / "version-12.x"
    source_dir.mkdir(parents=True)
    (source_dir / "routing.md").write_text("# Routing\n", encoding="utf-8")

    monkeypatch.setattr(main, "REPO_ROOT", repo_root)
    monkeypatch.setattr(main, "UPDATER_ROOT", updater_root)
    monkeypatch.setattr(main, "BRANCHES", [])
    monkeypatch.setattr(main, "clone_docs", lambda *_args: True)
    monkeypatch.setattr(main, "generate_sidebars", lambda *_args: True)
    monkeypatch.setattr(main, "get_changed_source_files", lambda *_args: [
        ".github/docs-updater/source/version-12.x/routing.md",
    ])
    monkeypatch.setattr(main, "stage_outputs", lambda *_args: True)
    monkeypatch.setattr(main.time, "sleep", lambda *_args: None)
    monkeypatch.setenv("TRANSLATION_MAX_ATTEMPTS", str(max_attempts))
    monkeypatch.setattr(
        main,
        "TRANSIENT_EXCEPTIONS",
        main.TRANSIENT_EXCEPTIONS + (_FakeTransientError,),
    )


def test_main_retries_transient_error_until_success(monkeypatch):
    attempts = []

    def fake_translate_file(_source_path, _target_path):
        attempts.append("attempt")
        if len(attempts) == 1:
            raise _FakeTransientError("transient")
        return True

    with tempfile.TemporaryDirectory() as tmpdir:
        _setup_main_fixture(monkeypatch, tmpdir, max_attempts=2)
        monkeypatch.setattr(main, "translate_file", fake_translate_file)

        assert main.main() == 0

    assert len(attempts) == 2


def test_main_records_failure_when_retries_exhausted(monkeypatch):
    attempts = []

    def fake_translate_file(_source_path, _target_path):
        attempts.append("attempt")
        raise _FakeTransientError("transient")

    with tempfile.TemporaryDirectory() as tmpdir:
        _setup_main_fixture(monkeypatch, tmpdir, max_attempts=2)
        monkeypatch.setattr(main, "translate_file", fake_translate_file)

        assert main.main() == 1

    assert len(attempts) == 2


# --- Task 1: 안정성 / 재시도 단위 테스트 ---


def test_read_int_env_uses_default_for_invalid_value(monkeypatch):
    monkeypatch.setenv("FOO_INT", "not-a-number")
    assert main._read_int_env("FOO_INT", 7) == 7


def test_read_int_env_enforces_minimum(monkeypatch):
    monkeypatch.setenv("FOO_INT", "-3")
    assert main._read_int_env("FOO_INT", 5, minimum=0) == 5


def test_retry_delays_are_geometric():
    assert main._retry_delays(0) == []
    assert main._retry_delays(3) == [5, 15, 45]


def test_get_translation_client_uses_configurable_timeout(monkeypatch):
    captured = {}

    class FakeOpenAI:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr(main, "_cached_client", None)
    monkeypatch.setattr(main, "_cached_model", None)
    monkeypatch.setattr(main.openai, "OpenAI", FakeOpenAI)
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
    monkeypatch.setenv("TRANSLATION_REQUEST_TIMEOUT", "60")
    monkeypatch.setenv("TRANSLATION_SDK_RETRIES", "0")
    monkeypatch.delenv("TRANSLATION_PROVIDER", raising=False)

    main.get_translation_client()

    assert captured["timeout"] == 60
    assert captured["max_retries"] == 0


def test_translate_with_retry_succeeds_on_second_attempt(monkeypatch):
    calls = []

    def flaky(_source, _target):
        calls.append(1)
        if len(calls) == 1:
            raise _FakeTransientError("transient")
        return True

    monkeypatch.setattr(main, "try_reuse_translation", lambda *a, **k: False)
    monkeypatch.setattr(main, "translate_file", flaky)
    monkeypatch.setattr(main.time, "sleep", lambda *_: None)
    monkeypatch.setattr(
        main,
        "TRANSIENT_EXCEPTIONS",
        main.TRANSIENT_EXCEPTIONS + (_FakeTransientError,),
    )

    assert main.translate_with_retry(
        Path("/tmp/x"), Path("/tmp/y"), "12.x", Path("/tmp"), max_attempts=3
    ) is True
    assert len(calls) == 2


def test_translate_with_retry_does_not_retry_fatal(monkeypatch):
    calls = []

    def fatal(_source, _target):
        calls.append(1)
        raise main.FatalCliError("auth failed")

    monkeypatch.setattr(main, "try_reuse_translation", lambda *a, **k: False)
    monkeypatch.setattr(main, "translate_file", fatal)
    monkeypatch.setattr(main.time, "sleep", lambda *_: None)

    import pytest
    with pytest.raises(main.FatalCliError):
        main.translate_with_retry(
            Path("/tmp/x"), Path("/tmp/y"), "12.x", Path("/tmp"), max_attempts=3
        )
    assert len(calls) == 1


def test_translate_with_retry_gives_up_after_max_attempts(monkeypatch):
    calls = []

    def always_transient(_source, _target):
        calls.append(1)
        raise _FakeTransientError("nope")

    monkeypatch.setattr(main, "try_reuse_translation", lambda *a, **k: False)
    monkeypatch.setattr(main, "translate_file", always_transient)
    monkeypatch.setattr(main.time, "sleep", lambda *_: None)
    monkeypatch.setattr(
        main,
        "TRANSIENT_EXCEPTIONS",
        main.TRANSIENT_EXCEPTIONS + (_FakeTransientError,),
    )

    import pytest
    with pytest.raises(_FakeTransientError):
        main.translate_with_retry(
            Path("/tmp/x"), Path("/tmp/y"), "12.x", Path("/tmp"), max_attempts=3
        )
    assert len(calls) == 3


def test_translate_markdown_content_retries_only_failing_chunk(monkeypatch):
    calls_per_chunk = {}

    def flaky_translate(text, _prompt):
        calls_per_chunk[text] = calls_per_chunk.get(text, 0) + 1
        if text.startswith("c") and calls_per_chunk[text] == 1:
            raise _FakeTransientError("transient on c")
        return f"[ko]{text}"

    monkeypatch.setattr(main, "translate_text", flaky_translate)
    monkeypatch.setattr(main.time, "sleep", lambda *_: None)
    monkeypatch.setattr(
        main,
        "TRANSIENT_EXCEPTIONS",
        main.TRANSIENT_EXCEPTIONS + (_FakeTransientError,),
    )

    content = "a1\na2\n\nb1\nb2\n\nc1\nc2\n"
    result = main.translate_markdown_content(content, "prompt", max_lines=2)

    # c-청크만 두 번 호출, 다른 청크는 한 번만
    assert calls_per_chunk.get("c1\nc2\n", 0) == 2
    assert calls_per_chunk.get("a1\na2\n\n", 0) == 1
    assert calls_per_chunk.get("b1\nb2\n\n", 0) == 1
    assert "[ko]c1\nc2\n" in result


def test_translate_text_with_cli_classifies_transient(monkeypatch):
    monkeypatch.setenv("TRANSLATION_CLI_COMMAND", "/bin/false")
    monkeypatch.setenv("TRANSLATION_CLI_TIMEOUT", "5")

    fake_error = subprocess.CalledProcessError(1, ["/bin/false"])
    fake_error.stderr = "rate limit exceeded"

    def fake_run(*_args, **_kwargs):
        raise fake_error

    monkeypatch.setattr(main.subprocess, "run", fake_run)

    import pytest
    with pytest.raises(main.TransientCliError):
        main.translate_text_with_cli("input", "system prompt")


def test_translate_text_with_cli_classifies_fatal(monkeypatch):
    monkeypatch.setenv("TRANSLATION_CLI_COMMAND", "/bin/false")
    monkeypatch.setenv("TRANSLATION_CLI_TIMEOUT", "5")

    fake_error = subprocess.CalledProcessError(1, ["/bin/false"])
    fake_error.stderr = "syntax error: unexpected token"

    def fake_run(*_args, **_kwargs):
        raise fake_error

    monkeypatch.setattr(main.subprocess, "run", fake_run)

    import pytest
    with pytest.raises(main.FatalCliError):
        main.translate_text_with_cli("input", "system prompt")


def test_translate_text_with_cli_empty_output_is_transient(monkeypatch):
    monkeypatch.setenv("TRANSLATION_CLI_COMMAND", "/bin/echo")
    monkeypatch.setenv("TRANSLATION_CLI_TIMEOUT", "5")

    class FakeResult:
        stdout = "   \n"

    monkeypatch.setattr(main.subprocess, "run", lambda *a, **k: FakeResult())

    import pytest
    with pytest.raises(main.TransientCliError):
        main.translate_text_with_cli("input", "system prompt")


def test_read_translation_delay_default_is_zero(monkeypatch):
    monkeypatch.delenv("TRANSLATION_DELAY", raising=False)
    assert main.read_translation_delay() == 0
