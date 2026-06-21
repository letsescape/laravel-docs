import subprocess
import unittest

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


if __name__ == "__main__":
    unittest.main()
