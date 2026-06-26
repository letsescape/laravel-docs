import difflib
import unittest

from sync import diff, patch, verify


def _segments(old_en: str, new_en: str) -> list[patch.Segment]:
    """Build segments the way the pipeline does: real unified diff -> hunks."""
    diff_text = "\n".join(
        difflib.unified_diff(old_en.splitlines(), new_en.splitlines(), lineterm="")
    )
    hunks = diff._parse_unified_diff(diff_text)  # noqa: SLF001
    return patch.segments_from_hunks(hunks, new_en)


# Two code blocks. Only the first changes Exception -> Throwable; the second
# keeps an identical `use Exception;` line to prove changes stay block-scoped.
_OLD_EN = (
    '<a name="retry"></a>\n'
    "## Retrying Requests\n"
    "\n"
    "First paragraph describing the retry callback.\n"
    "\n"
    "```php\n"
    "use Exception;\n"
    "use App\\Support\\Helper;\n"
    "\n"
    "$response = retry(function (Exception $e) {\n"
    "    return true;\n"
    "});\n"
    "```\n"
    "\n"
    "Second paragraph that must stay untouched.\n"
    "\n"
    "```php\n"
    "use Exception;\n"
    "\n"
    "$other = keep(Exception::class);\n"
    "```\n"
)
_NEW_EN = _OLD_EN.replace(
    "use Exception;\nuse App\\Support\\Helper;\n\n$response = retry(function (Exception $e) {",
    "use Throwable;\nuse App\\Support\\Helper;\n\n$response = retry(function (Throwable $e) {",
)


class CodeBlockPatchTests(unittest.TestCase):
    def test_interior_change_becomes_code_block_segment(self):
        segments = _segments(_OLD_EN, _NEW_EN)
        code = [s for s in segments if s.code_block is not None]
        self.assertEqual(len(code), 1)
        self.assertEqual(code[0].code_block.block_index, 0)
        self.assertFalse(code[0].needs_translation)

    def test_applies_change_scoped_to_the_right_block(self):
        # Translation still carries the old code; only block 0 should change.
        result = patch.apply_segments(_OLD_EN, _segments(_OLD_EN, _NEW_EN), [])
        self.assertIn("$response = retry(function (Throwable $e) {", result)
        # Block 1 is left alone, so its identical lines survive verbatim.
        self.assertIn("$other = keep(Exception::class);", result)
        self.assertEqual(result.count("use Exception;"), 1)
        # The locale code blocks now match English (what verification checks).
        self.assertEqual(
            verify._normalized_fenced_code_blocks(result),  # noqa: SLF001
            verify._normalized_fenced_code_blocks(_NEW_EN),  # noqa: SLF001
        )

    def test_canonicalizes_block_when_translation_already_updated_and_reordered(self):
        # The real failure: the translation already has Throwable but with its
        # imports in a different order than English. The patch must not raise,
        # and must restore the English block so verification passes.
        already = _NEW_EN.replace(
            "use Throwable;\nuse App\\Support\\Helper;",
            "use App\\Support\\Helper;\nuse Throwable;",
        )
        segments = _segments(_OLD_EN, _NEW_EN)
        result = patch.apply_segments(already, segments, [])
        self.assertEqual(
            verify._normalized_fenced_code_blocks(result),  # noqa: SLF001
            verify._normalized_fenced_code_blocks(_NEW_EN),  # noqa: SLF001
        )
        # Idempotent: re-applying changes nothing further.
        self.assertEqual(patch.apply_segments(result, segments, []), result)

    def test_pure_code_line_insertion_is_applied(self):
        old = (
            "Intro paragraph.\n"
            "\n"
            "```php\n"
            "use Throwable;\n"
            "$response = run();\n"
            "```\n"
        )
        new = old.replace(
            "use Throwable;\n$response = run();",
            "use Throwable;\n$debug = config('app.debug');\n$response = run();",
        )
        result = patch.apply_segments(old, _segments(old, new), [])
        self.assertIn("$debug = config('app.debug');", result)
        self.assertEqual(
            verify._normalized_fenced_code_blocks(result),  # noqa: SLF001
            verify._normalized_fenced_code_blocks(new),  # noqa: SLF001
        )

    def test_pure_code_line_deletion_is_applied(self):
        old = (
            "Intro paragraph.\n"
            "\n"
            "```php\n"
            "use Throwable;\n"
            "$debug = config('app.debug');\n"
            "$response = run();\n"
            "```\n"
        )
        new = old.replace("use Throwable;\n$debug = config('app.debug');\n", "use Throwable;\n")
        result = patch.apply_segments(old, _segments(old, new), [])
        self.assertNotIn("$debug = config('app.debug');", result)
        self.assertEqual(
            verify._normalized_fenced_code_blocks(result),  # noqa: SLF001
            verify._normalized_fenced_code_blocks(new),  # noqa: SLF001
        )

    def test_diverged_block_is_left_untouched_not_corrupted(self):
        # If the indexed block holds none of the changed markers, leave it be.
        diverged = _OLD_EN.replace(
            "use Exception;\n"
            "use App\\Support\\Helper;\n"
            "\n"
            "$response = retry(function (Exception $e) {\n"
            "    return true;\n"
            "});",
            "echo 'totally unrelated block';",
        )
        result = patch.apply_segments(diverged, _segments(_OLD_EN, _NEW_EN), [])
        self.assertIn("echo 'totally unrelated block';", result)

    def test_replaces_paragraph_between_nearest_raw_contexts_when_old_comment_is_gone(self):
        old = (
            "## PHP Versions\n\n"
            "The default PHP version is PHP 8.4.\n\n"
            "```yaml\n"
            "context: ./vendor/laravel/sail/runtimes/8.4\n"
            "```\n"
        )
        new = old.replace("PHP 8.4.", "PHP 8.5.")
        existing = (
            "```yaml\n"
            "unrelated: true\n"
            "```\n\n"
            "<!-- ## PHP Versions -->\n"
            "## PHP Versions\n\n"
            "<!-- The default PHP version is PHP 8.5. -->\n"
            "기본 PHP 버전은 PHP 8.5입니다.\n\n"
            "```yaml\n"
            "context: ./vendor/laravel/sail/runtimes/8.4\n"
            "```\n"
        )
        translated = (
            "<!-- The default PHP version is PHP 8.5. -->\n"
            "기본 PHP 버전은 PHP 8.5입니다.\n"
        )

        segments = _segments(old, new)
        self.assertIn("기본 PHP 버전", patch.existing_context(existing, segments[0]))
        self.assertEqual(
            patch.apply_segments(existing, segments, [translated]),
            existing,
        )

    def test_replaces_existing_inserted_anchor_section_instead_of_duplicating_it(self):
        old = (
            '<a name="next"></a>\n'
            "## Next\n"
        )
        new = (
            '<a name="inserted"></a>\n'
            "#### Inserted\n\n"
            "Inserted paragraph.\n\n"
            "```php\n"
            "example();\n"
            "```\n\n"
            '<a name="next"></a>\n'
            "## Next\n"
        )
        existing = (
            '<a name="inserted"></a>\n'
            "<!-- #### Inserted -->\n"
            "#### Inserted\n\n"
            "<!-- Inserted paragraph. -->\n"
            "삽입된 문단입니다.\n\n"
            "```php\n"
            "example();\n"
            "```\n\n"
            '<a name="next"></a>\n'
            "<!-- ## Next -->\n"
            "## Next\n"
        )
        translated = (
            '<a name="inserted"></a>\n'
            "<!-- #### Inserted -->\n"
            "#### Inserted\n\n"
            "<!-- Inserted paragraph. -->\n"
            "삽입된 문단입니다.\n\n"
            "```php\n"
            "example();\n"
            "```\n"
        )

        result = patch.apply_segments(existing, _segments(old, new), [translated])

        self.assertEqual(result.count('<a name="inserted"></a>'), 1)
        self.assertEqual(
            verify._normalized_fenced_code_blocks(result),  # noqa: SLF001
            verify._normalized_fenced_code_blocks(new),  # noqa: SLF001
        )
        self.assertEqual(result, existing)


class PatchTests(unittest.TestCase):
    def test_blocks_parse_indented_multiline_comments_with_closing_content(self):
        blocks = patch._blocks(  # noqa: SLF001
            "  <!--\n"
            "First line.\n"
            "Second line. -->\n"
            "번역입니다.\n"
        )

        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].comment, "First line. Second line.")


class AdmonitionMarkerTests(unittest.TestCase):
    def test_apply_does_not_duplicate_admonition_marker(self):
        # A NOTE body line changes. The marker line stays as context, so the
        # body is translated alone; the model often re-emits the `> [!NOTE]`
        # marker in its output. Applying that block after the retained marker
        # must not leave two consecutive markers.
        old = (
            "The basic workflow paragraph.\n\n"
            "> [!NOTE]\n"
            "> Vector search requires a PostgreSQL database.\n\n"
            '<a name="generating-embeddings"></a>\n'
            "### Generating Embeddings\n"
        )
        new = old.replace(
            "> Vector search requires a PostgreSQL database.",
            "> Vector search requires the AI SDK and PostgreSQL or MongoDB.",
        )
        existing = (
            "<!-- The basic workflow paragraph. -->\n"
            "기본 워크플로 문단입니다.\n\n"
            "> [!NOTE]\n"
            "> 벡터 검색은 PostgreSQL 데이터베이스가 필요합니다.\n\n"
            '<a name="generating-embeddings"></a>\n'
            "<!-- ### Generating Embeddings -->\n"
            "### Generating Embeddings\n"
        )
        translated = (
            "> [!NOTE]\n"
            "> <!-- Vector search requires the AI SDK and PostgreSQL or MongoDB. -->\n"
            "> 벡터 검색에는 AI SDK가 필요하며 PostgreSQL 또는 MongoDB를 지원합니다.\n"
        )

        result = patch.apply_segments(existing, _segments(old, new), [translated])

        self.assertNotIn("> [!NOTE]\n> [!NOTE]", result)
        self.assertEqual(result.count("> [!NOTE]"), 1)


if __name__ == "__main__":
    unittest.main()
