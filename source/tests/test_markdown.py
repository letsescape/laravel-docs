from utils.markdown import sanitize_markdown_for_mdx


class TestSanitizeMarkdownForMdx:
    def test_wraps_style_block_with_template_literal(self):
        source = "<style>\n.badge { color: red; }\n</style>\n"
        result = sanitize_markdown_for_mdx(source)
        assert result == "<style>{`\n.badge { color: red; }\n`}</style>\n"

    def test_self_closes_img_tag(self):
        source = '<img src="https://example.com/a.png">\n'
        result = sanitize_markdown_for_mdx(source)
        assert result == '<img src="https://example.com/a.png" />\n'

    def test_does_not_change_fenced_code_content(self):
        source = (
            "```blade\n"
            "<style>\n"
            ".x { color: red; }\n"
            "</style>\n"
            '<img src="https://example.com/a.png">\n'
            "```\n"
        )
        result = sanitize_markdown_for_mdx(source)
        assert result == source

    def test_does_not_change_inline_code_content(self):
        source = 'Use `<img src="https://example.com/a.png">` in the example.\n'
        result = sanitize_markdown_for_mdx(source)
        assert result == source

    def test_keeps_already_wrapped_style_unchanged(self):
        source = "<style>{`\n.badge { color: red; }\n`}</style>\n"
        result = sanitize_markdown_for_mdx(source)
        assert result == source
