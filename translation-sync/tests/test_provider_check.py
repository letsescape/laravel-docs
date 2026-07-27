import io
import unittest
from contextlib import redirect_stderr
from unittest.mock import patch

import provider_check


class ProviderCheckTests(unittest.TestCase):
    @staticmethod
    def _valid_translation(locale: str = "ko") -> str:
        body = {
            "ko": "[atomic locks](#atomic-locks) API를 `Cache::lock`과 함께 사용합니다.",
            "ja": "[atomic locks](#atomic-locks) API を `Cache::lock` とともに使用します。",
        }[locale]
        return (
            '<a name="cache-locks"></a>\n'
            "<!-- ## Cache Locks -->\n"
            "## Cache Locks\n\n"
            "<!-- Use the [atomic locks](#atomic-locks) API with `Cache::lock`. -->\n"
            f"{body}\n\n"
            "```php\n"
            "$lock = Cache::lock('foo', 10);\n"
            "```\n"
        )

    def test_accepts_structurally_valid_korean_markdown(self):
        translated = self._valid_translation()

        self.assertEqual(provider_check.evaluate_output("ko", translated), [])

    def test_rejects_cli_wrapper_text(self):
        translated = (
            "Here is the translation:\n\n"
            + self._valid_translation()
        )

        self.assertIn(
            "unexpected provider response prefix",
            provider_check.evaluate_output("ko", translated),
        )

    def test_accepts_structurally_valid_japanese_markdown(self):
        translated = self._valid_translation("ja")

        self.assertEqual(provider_check.evaluate_output("ja", translated), [])

    def test_retries_a_completed_response_that_fails_the_contract(self):
        cfg = provider_check.config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "test-model",
            },
        )
        invalid = self._valid_translation().replace("`Cache::lock`", "Cache::lock")
        valid = self._valid_translation()

        with patch.object(
            provider_check.sys,
            "argv",
            ["provider_check.py", "--locale", "ko"],
        ), patch.object(
            provider_check.config,
            "load_config",
            return_value=cfg,
        ), patch.object(
            provider_check.prompt,
            "load_prompt",
            return_value="prompt",
        ), patch.object(
            provider_check.translate,
            "translate_request",
            side_effect=[invalid, valid],
        ) as provider:
            exit_code = provider_check.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(provider.call_count, 2)
        retry_request = provider.call_args_list[1].args[0]
        self.assertIn(
            "provider inline code mismatch",
            retry_request.verification_feedback or "",
        )

    def test_stops_after_two_invalid_completed_responses(self):
        stderr = io.StringIO()
        cfg = provider_check.config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "test-model",
            },
        )
        invalid = self._valid_translation().replace("`Cache::lock`", "Cache::lock")

        with redirect_stderr(stderr), patch.object(
            provider_check.sys,
            "argv",
            ["provider_check.py", "--locale", "ko"],
        ), patch.object(
            provider_check.config,
            "load_config",
            return_value=cfg,
        ), patch.object(
            provider_check.prompt,
            "load_prompt",
            return_value="prompt",
        ), patch.object(
            provider_check.translate,
            "translate_request",
            return_value=invalid,
        ) as provider:
            exit_code = provider_check.main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            provider.call_count,
            provider_check.translate.MAX_COMPLETED_RESPONSE_ATTEMPTS,
        )
        self.assertIn("provider inline code mismatch", stderr.getvalue())

    def test_rejects_trailing_wrapper_text(self):
        translated = self._valid_translation() + "\nTranslation complete.\n"

        self.assertIn(
            "unexpected provider response shape",
            provider_check.evaluate_output("ko", translated),
        )

    def test_rejects_misordered_original_comments(self):
        translated = self._valid_translation().replace(
            "<!-- ## Cache Locks -->\n## Cache Locks\n\n"
            "<!-- Use the [atomic locks](#atomic-locks) API with `Cache::lock`. -->",
            "<!-- Use the [atomic locks](#atomic-locks) API with `Cache::lock`. -->\n"
            "## Cache Locks\n\n<!-- ## Cache Locks -->",
        )

        self.assertIn(
            "unexpected provider response shape",
            provider_check.evaluate_output("ko", translated),
        )

    def test_rejects_modified_fenced_code(self):
        translated = self._valid_translation().replace(
            "$lock = Cache::lock('foo', 10);",
            "$lock = Cache::lock('bar', 10);",
        )

        self.assertIn(
            "code block mismatch",
            provider_check.evaluate_output("ko", translated),
        )

    def test_rejects_paragraph_changed_to_markdown_structure(self):
        body = "[atomic locks](#atomic-locks) API를 `Cache::lock`과 함께 사용합니다."
        for marker in ("- ", "1. ", "> ", "| ", "<div>"):
            with self.subTest(marker=marker):
                translated = self._valid_translation().replace(body, marker + body)

                self.assertIn(
                    "unexpected provider response shape",
                    provider_check.evaluate_output("ko", translated),
                )

    def test_rejects_extra_paragraph_line(self):
        body = "[atomic locks](#atomic-locks) API를 `Cache::lock`과 함께 사용합니다."
        translated = self._valid_translation().replace(
            body,
            body + "\n원문에 없는 설명입니다.",
        )

        self.assertIn(
            "unexpected provider response shape",
            provider_check.evaluate_output("ko", translated),
        )

    def test_rejects_paragraph_indented_as_a_code_block(self):
        body = "[atomic locks](#atomic-locks) API를 `Cache::lock`과 함께 사용합니다."
        translated = self._valid_translation().replace(body, "    " + body)

        self.assertIn(
            "provider paragraph indentation mismatch",
            provider_check.evaluate_output("ko", translated),
        )

    def test_rejects_english_source_echo_with_one_target_character(self):
        body = "[atomic locks](#atomic-locks) API를 `Cache::lock`과 함께 사용합니다."
        translated = self._valid_translation().replace(
            body,
            "Use the [atomic locks](#atomic-locks) API with `Cache::lock`. 한",
        )

        self.assertIn(
            "unexpected provider response shape",
            provider_check.evaluate_output("ko", translated),
        )

    def test_rejects_near_english_echo_with_one_target_character(self):
        body = "[atomic locks](#atomic-locks) API를 `Cache::lock`과 함께 사용합니다."
        translated = self._valid_translation().replace(
            body,
            "Use the [atomic locks](#atomic-locks) APIs with `Cache::lock`. 한",
        )

        self.assertIn(
            "unexpected provider response shape",
            provider_check.evaluate_output("ko", translated),
        )

    def test_rejects_japanese_body_with_only_incidental_korean_text(self):
        body = "[atomic locks](#atomic-locks) API를 `Cache::lock`과 함께 사용합니다."
        translated = self._valid_translation().replace(
            body,
            "[atomic locks](#atomic-locks) APIを`Cache::lock`とともに使用します。한글문",
        )

        self.assertIn(
            "unexpected provider response shape",
            provider_check.evaluate_output("ko", translated),
        )

    def test_prompt_error_is_reported_as_configuration_failure(self):
        stderr = io.StringIO()
        cfg = provider_check.config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "test-model",
            },
        )

        with redirect_stderr(stderr), patch.object(
            provider_check.sys,
            "argv",
            ["provider_check.py", "--locale", "ko"],
        ), patch.object(
            provider_check.config,
            "load_config",
            return_value=cfg,
        ), patch.object(
            provider_check.prompt,
            "load_prompt",
            side_effect=provider_check.prompt.PromptError(
                "missing prompt file: prompt.md"
            ),
        ), patch.object(
            provider_check.translate,
            "translate_request",
            side_effect=AssertionError("provider should not be called"),
        ):
            exit_code = provider_check.main()

        self.assertEqual(exit_code, 2)
        self.assertEqual(
            stderr.getvalue(),
            "provider check configuration failed: "
            "missing prompt file: prompt.md\n",
        )

    def test_prompt_read_failure_is_reported_as_configuration_failure(self):
        stderr = io.StringIO()
        cfg = provider_check.config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "test-model",
            },
        )

        with redirect_stderr(stderr), patch.object(
            provider_check.sys,
            "argv",
            ["provider_check.py", "--locale", "ja"],
        ), patch.object(
            provider_check.config,
            "load_config",
            return_value=cfg,
        ), patch.object(
            provider_check.prompt,
            "load_prompt",
            side_effect=OSError("prompt is unreadable"),
        ), patch.object(
            provider_check.translate,
            "translate_request",
            side_effect=AssertionError("provider should not be called"),
        ):
            exit_code = provider_check.main()

        self.assertEqual(exit_code, 2)
        self.assertEqual(
            stderr.getvalue(),
            "provider check configuration failed: prompt is unreadable\n",
        )


if __name__ == "__main__":
    unittest.main()
