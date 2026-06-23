import subprocess
import unittest
from unittest.mock import patch

from sync import config, translate


class TranslateRetryTests(unittest.TestCase):
    def test_annotation_format_is_locale_neutral(self):
        self.assertNotIn("한국어", translate._ANNOTATION_FORMAT)
        self.assertIn("translated paragraph", translate._ANNOTATION_FORMAT.lower())

    def test_retries_transient_provider_failures_with_same_chunk(self):
        calls: list[str] = []

        def flaky(chunk: str, _config: config.Config, _prompt: str) -> str:
            calls.append(chunk)
            if len(calls) < 3:
                raise TimeoutError("temporary timeout")
            return "translated"

        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

        result = translate._with_retries(
            flaky, "same chunk", cfg, "prompt", sleep=lambda _: None
        )

        self.assertEqual(result, "translated")
        self.assertEqual(calls, ["same chunk", "same chunk", "same chunk"])

    def test_raises_incomplete_translation_after_max_retries(self):
        def always_fails(chunk: str, _config: config.Config, _prompt: str) -> str:
            raise subprocess.TimeoutExpired(cmd="translate", timeout=1)

        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

        with self.assertRaises(translate.IncompleteTranslation):
            translate._with_retries(
                always_fails,
                "chunk",
                cfg,
                "prompt",
                sleep=lambda _: None,
            )

    def test_split_chunks_keeps_anchor_with_following_heading(self):
        content = '<a name="intro"></a>\n\n## Introduction\n\nBody.\n'

        chunks = translate.split_chunks(content, max_lines=2)

        self.assertEqual(chunks[0], '<a name="intro"></a>\n\n## Introduction\n\n')
        self.assertEqual(chunks[1], "Body.\n")

    def test_split_chunks_keeps_long_fenced_code_blocks_intact(self):
        content = "````markdown\n```php\necho 'ok';\n```\n````\n\nAfter.\n"

        chunks = translate.split_chunks(content, max_lines=2)

        self.assertEqual(chunks[0], "````markdown\n```php\necho 'ok';\n```\n````\n\n")
        self.assertEqual(chunks[1], "After.\n")

    def test_translate_text_can_skip_internal_chunking(self):
        calls: list[str] = []

        def collect(chunk: str, _config: config.Config, _prompt: str) -> str:
            calls.append(chunk)
            return chunk

        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

        with patch.object(translate, "_translate_chunk", side_effect=collect):
            out = translate.translate_text("a\n\nb\n", cfg, "prompt", split=False)

        self.assertEqual(out, "a\n\nb\n")
        self.assertEqual(calls, ["a\n\nb\n"])


if __name__ == "__main__":
    unittest.main()
