import unittest

from sync import verify


class VerifyContentTests(unittest.TestCase):
    def test_detects_link_url_changed_even_when_original_comment_contains_url(self):
        source = "See [Routing](routing.md#basic-routing)."
        translated = """<!-- See [Routing](routing.md#basic-routing). -->
[라우팅](routing.md#기본-라우팅)을 참고하세요.
"""

        self.assertIn("link target mismatch", verify.verify(translated, source=source))

    def test_detects_translated_link_text_even_when_url_is_preserved(self):
        source = "See [Routing](routing.md#basic-routing)."
        translated = """<!-- See [Routing](routing.md#basic-routing). -->
[라우팅](routing.md#basic-routing)을 참고하세요.
"""

        self.assertIn("link label mismatch", verify.verify(translated, source=source))

    def test_accepts_preserved_link_text_when_url_is_preserved(self):
        source = "See [Routing](routing.md#basic-routing)."
        translated = """<!-- See [Routing](routing.md#basic-routing). -->
[Routing](routing.md#basic-routing)을 참고하세요.
"""

        self.assertNotIn("link label mismatch", verify.verify(translated, source=source))

    def test_detects_swapped_link_labels_and_targets(self):
        source = (
            "Generate a [redirect HTTP response](responses#redirects) "
            "for a [named route](routing#named-routes)."
        )
        translated = """<!-- Generate a [redirect HTTP response](responses#redirects) for a [named route](routing#named-routes). -->
[redirect HTTP response](routing#named-routes)에 대한 [named route](responses#redirects)을 생성합니다.
"""

        self.assertIn("link pair mismatch", verify.verify(translated, source=source))

    def test_detects_missing_inline_code_from_translated_body(self):
        source = "Set `user_id` before saving."
        translated = """<!-- Set `user_id` before saving. -->
저장하기 전에 사용자 ID를 설정합니다.
"""

        self.assertIn("inline code mismatch", verify.verify(translated, source=source))

    def test_detects_code_block_content_changed(self):
        source = """```js
// Create a user
const user = {};
```
"""
        translated = """```js
// 사용자를 생성합니다
const user = {};
```
"""

        self.assertIn("code block mismatch", verify.verify(translated, source=source))

    def test_accepts_fenced_code_blocks_with_equivalent_trailing_newline(self):
        source = """```php
echo 'ok';
```
"""
        translated = """```php
echo 'ok';
```"""

        self.assertNotIn("code block mismatch", verify.verify(translated, source=source))

    def test_accepts_fenced_code_blocks_with_equivalent_trailing_spaces(self):
        source = "```php\nreturn true;    \n```\n"
        translated = "```php\nreturn true;\n```\n"

        self.assertNotIn("code block mismatch", verify.verify(translated, source=source))

    def test_accepts_long_fenced_code_blocks_with_inner_shorter_fence(self):
        source = "````markdown\n```php\necho 'ok';\n```\n````\n"
        translated = source

        self.assertNotIn("code block mismatch", verify.verify(translated, source=source))

    def test_detects_html_anchor_name_changed(self):
        source = '<a name="basic-routing"></a>\n\n# Routing\n'
        translated = """<!-- <a name="basic-routing"></a> -->
<a name="기본-라우팅"></a>

<!-- # Routing -->
# 라우팅 (Routing)
"""

        self.assertIn("anchor mismatch", verify.verify(translated, source=source))

    def test_ignores_translation_alias_anchors(self):
        source = '<a name="generating-migrations"></a>\n\n# Migrations\n'
        translated = """<!-- <a name="generating-migrations"></a> -->
<a name="generating-migrations"></a>
<a name="writing-migrations" data-translation-alias="true"></a>

<!-- # Migrations -->
# 마이그레이션 (Migrations)
"""

        self.assertNotIn("anchor mismatch", verify.verify(translated, source=source))

    def test_detects_missing_original_english_comment_for_heading_or_paragraph(self):
        source = "# Installation\n\nInstall Laravel with Composer.\n"
        translated = "# 설치 (Installation)\n\nComposer로 Laravel을 설치합니다.\n"

        self.assertIn("missing original comment", verify.verify(translated, source=source))
        self.assertEqual(
            verify.missing_original_comments(translated, source),
            ["# Installation", "Install Laravel with Composer."],
        )

    def test_accepts_escaped_js_comment_closer_inside_original_comment(self):
        source = "Use `DB::raw(/* ... */)` carefully."
        translated = """<!-- Use `DB::raw(/* ... *&#47;)` carefully. -->
`DB::raw(/* ... */)`를 신중하게 사용합니다.
"""

        self.assertNotIn("missing original comment", verify.verify(translated, source=source))

    def test_normalizes_known_stale_link_targets_before_comparing(self):
        source = "See [Agents](#agents-integration)."
        translated = """<!-- See [Agents](#agents-integration). -->
[Agents](#agent-integration)를 참고하세요.
"""

        self.assertNotIn("link target mismatch", verify.verify(translated, source=source))

    def test_normalizes_versioned_absolute_doc_links_to_relative_targets(self):
        source = "See [Cache](cache)."
        translated = """<!-- See [Cache](cache). -->
[Cache](/docs/12.x/cache)를 참고하세요.
"""

        self.assertNotIn("link target mismatch", verify.verify(translated, source=source))

    def test_detects_heading_level_mismatch(self):
        source = "# Title\n\n## Install\n"
        translated = """<!-- # Title -->
# 제목 (Title)

<!-- ## Install -->
### 설치 (Install)
"""

        self.assertIn("heading mismatch", verify.verify(translated, source=source))

    def test_detects_translated_heading_text(self):
        source = "# Title\n\n## Install\n"
        translated = """<!-- # Title -->
# Title

<!-- ## Install -->
## 설치 (Install)
"""

        self.assertIn("heading text mismatch", verify.verify(translated, source=source))

    def test_detects_translated_front_matter_title(self):
        source = "---\ntitle: Installation\n---\n\n# Installation\n"
        translated = "---\ntitle: 설치\n---\n\n<!-- # Installation -->\n# Installation\n"

        self.assertIn(
            "front matter title mismatch", verify.verify(translated, source=source)
        )

    def test_does_not_treat_later_horizontal_rule_as_front_matter(self):
        source = "Intro.\n\n---\n\nDetails.\n"
        translated = """<!-- Intro. -->
소개입니다.

---

상세입니다.
"""

        self.assertIn("missing original comment", verify.verify(translated, source=source))

    def test_detects_admonition_body_outside_blockquote(self):
        translated = """> [!NOTE]
<!-- Note body. -->
본문입니다.
"""

        self.assertIn("admonition body outside blockquote", verify.verify(translated))

    def test_detects_duplicated_admonition_marker(self):
        translated = """> [!NOTE]
> [!NOTE]
> <!-- Vector search requires the [AI SDK](/docs/13.x/ai-sdk). -->
> 벡터 검색에는 [AI SDK](/docs/13.x/ai-sdk)가 필요합니다.
"""

        self.assertIn("duplicate admonition marker", verify.verify(translated))

    def test_accepts_single_admonition_marker(self):
        translated = """> [!NOTE]
> <!-- Vector search requires the [AI SDK](/docs/13.x/ai-sdk). -->
> 벡터 검색에는 [AI SDK](/docs/13.x/ai-sdk)가 필요합니다.
"""

        self.assertNotIn("duplicate admonition marker", verify.verify(translated))

    def test_detects_list_markers_dropped_in_translation(self):
        source = """- [Using Eloquent](https://example.com/eloquent/) stores models.
- [Write queries](https://example.com/queries/) with the builder.
"""
        translated = """<!--
- [Using Eloquent](https://example.com/eloquent/) stores models.
- [Write queries](https://example.com/queries/) with the builder.
-->
[Using Eloquent](https://example.com/eloquent/) を使うとモデルを保存できます。

[Write queries](https://example.com/queries/) をビルダーで作成できます。
"""

        self.assertIn("list marker mismatch", verify.verify(translated, source=source))

    def test_accepts_preserved_list_markers(self):
        source = """- [Using Eloquent](https://example.com/eloquent/) stores models.
- [Write queries](https://example.com/queries/) with the builder.
"""
        translated = """<!--
- [Using Eloquent](https://example.com/eloquent/) stores models.
- [Write queries](https://example.com/queries/) with the builder.
-->
- [Using Eloquent](https://example.com/eloquent/) を使うとモデルを保存できます。
- [Write queries](https://example.com/queries/) をビルダーで作成できます。
"""

        self.assertNotIn("list marker mismatch", verify.verify(translated, source=source))

    def test_accepts_translation_that_expands_prose_into_a_list(self):
        source = "Supported serializers include: `A`, `B`, and `C`.\n"
        translated = """<!-- Supported serializers include: `A`, `B`, and `C`. -->
지원되는 직렬화 방식:

- `A`
- `B`
- `C`
"""

        self.assertNotIn("list marker mismatch", verify.verify(translated, source=source))


if __name__ == "__main__":
    unittest.main()
