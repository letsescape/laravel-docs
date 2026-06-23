import unittest

from sync import verify


class VerifyContentTests(unittest.TestCase):
    def test_detects_link_url_changed_even_when_original_comment_contains_url(self):
        source = "See [Routing](routing.md#basic-routing)."
        translated = """<!-- See [Routing](routing.md#basic-routing). -->
[라우팅](routing.md#기본-라우팅)을 참고하세요.
"""

        self.assertIn("link target mismatch", verify.verify(translated, source=source))

    def test_allows_translated_link_text_when_url_is_preserved(self):
        source = "See [Routing](routing.md#basic-routing)."
        translated = """<!-- See [Routing](routing.md#basic-routing). -->
[라우팅](routing.md#basic-routing)을 참고하세요.
"""

        self.assertNotIn("link target mismatch", verify.verify(translated, source=source))

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

    def test_detects_heading_level_mismatch(self):
        source = "# Title\n\n## Install\n"
        translated = """<!-- # Title -->
# 제목 (Title)

<!-- ## Install -->
### 설치 (Install)
"""

        self.assertIn("heading mismatch", verify.verify(translated, source=source))

    def test_does_not_treat_later_horizontal_rule_as_front_matter(self):
        source = "Intro.\n\n---\n\nDetails.\n"
        translated = """<!-- Intro. -->
소개입니다.

---

상세입니다.
"""

        self.assertIn("missing original comment", verify.verify(translated, source=source))


if __name__ == "__main__":
    unittest.main()
