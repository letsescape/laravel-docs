from markdown_link_utils import (
    extract_internal_markdown_links,
    extract_markdown_links,
    extract_version_from_path,
    is_internal_docs_link,
    replace_version_placeholders,
    strip_code,
)


def test_strip_code_removes_fenced_blocks():
    text = "before\n```php\n[Skip](#anchor)\n```\nafter\n"
    assert "[Skip](#anchor)" not in strip_code(text)
    assert "before" in strip_code(text)
    assert "after" in strip_code(text)


def test_strip_code_removes_tilde_fenced_blocks():
    text = "before\n~~~php\n[Skip](#anchor)\n~~~\nafter\n"
    assert "[Skip](#anchor)" not in strip_code(text)


def test_strip_code_removes_inline_code():
    text = "Use `[fake](#bad)` and ([real](#good))."
    stripped = strip_code(text)
    assert "[fake](#bad)" not in stripped
    assert "[real](#good)" in stripped


def test_strip_code_keeps_unmatched_inline_backtick():
    text = "Use `using method:\n[real](#good)\n"
    stripped = strip_code(text)
    assert "[real](#good)" in stripped


def test_extract_markdown_links_returns_text_and_url():
    text = "See [Routing](/docs/{{version}}/routing).\n"
    links = extract_markdown_links(text)
    assert len(links) == 1
    assert links[0].text == "Routing"
    assert links[0].url == "/docs/{{version}}/routing"


def test_extract_markdown_links_ignores_links_inside_code_block():
    text = "```\n[Skip](/docs/skip)\n```\n[Keep](/docs/keep)\n"
    links = extract_markdown_links(text)
    assert [link.url for link in links] == ["/docs/keep"]


def test_extract_markdown_links_strips_title_suffix():
    text = '[Title](/docs/keep "Optional title")\n'
    links = extract_markdown_links(text)
    assert links[0].url == "/docs/keep"


def test_extract_markdown_links_keeps_spaces_inside_placeholder():
    text = "[T](/docs/{{ version }}/routing)\n"
    links = extract_markdown_links(text)
    assert links[0].url == "/docs/{{ version }}/routing"


def test_extract_internal_markdown_links_filters_external_urls():
    text = (
        "[Internal](/docs/keep)\n"
        "[Anchor](#section)\n"
        "[Placeholder]({{version}}/placeholder)\n"
        "[Spaced]({{ version }}/spaced)\n"
        "[External](https://example.com)\n"
    )
    urls = [link.url for link in extract_internal_markdown_links(text)]
    assert urls == [
        "/docs/keep",
        "#section",
        "{{version}}/placeholder",
        "{{ version }}/spaced",
    ]


def test_is_internal_docs_link_recognizes_known_prefixes():
    assert is_internal_docs_link("/docs/abc")
    assert is_internal_docs_link("#anchor")
    assert is_internal_docs_link("{{version}}/path")
    assert is_internal_docs_link("{{ version }}/path")
    assert not is_internal_docs_link("https://example.com")


def test_extract_version_from_path_handles_versioned_path():
    assert (
        extract_version_from_path(
            ".github/docs-updater/source/version-12.x/routing.md"
        )
        == "12.x"
    )
    assert (
        extract_version_from_path("versioned_docs/version-master/routing.md")
        == "master"
    )
    assert extract_version_from_path("tools/foo.py") is None


def test_replace_version_placeholders_normalizes_spacing_and_value():
    assert (
        replace_version_placeholders(
            "/docs/{{version}}/x and /docs/{{ version }}/y", "12.x"
        )
        == "/docs/12.x/x and /docs/12.x/y"
    )


def test_replace_version_placeholders_with_empty_version_drops_token():
    assert replace_version_placeholders("/docs/{{version}}/x", "") == "/docs//x"
