import errno
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

from sync import config, translate


class TranslateRetryTests(unittest.TestCase):
    def test_translation_request_uses_a_safe_dynamic_diff_fence(self):
        diff_text = "+ Before.\n+ ````php\n+ echo true;\n+ ````"
        request = translate.TranslationRequest(
            source="Before.\n\n````php\necho true;\n````\n",
            existing_translation=None,
            diff_text=diff_text,
        )

        rendered = request.render()

        self.assertIn("`````diff\n" + diff_text + "\n`````", rendered)
        self.assertEqual(rendered.count("`````"), 2)

    def test_identity_provider_requires_replay_mode(self):
        with self.assertRaises(config.ConfigError):
            config.load_config({"TRANSLATION_PROVIDER": "identity"})

        cfg = config.load_config(
            {
                "TRANSLATION_PROVIDER": "identity",
                "TRANSLATION_REPLAY": "1",
            }
        )

        self.assertEqual(cfg.provider, "identity")

    def test_cli_provider_requires_an_explicit_model(self):
        with self.assertRaises(config.ConfigError):
            config.load_config(
                {
                    "TRANSLATION_PROVIDER": "cli",
                    "TRANSLATION_CLI_COMMAND": "codex exec",
                }
            )

    def test_config_preserves_provider_runtime_options(self):
        cfg = config.load_config(
            {
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_CLI_COMMAND": "codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                "TRANSLATION_REASONING_EFFORT": "low",
                "TRANSLATION_CLI_TIMEOUT": "60",
                "TRANSLATION_RETRY_DELAY": "0",
            }
        )

        self.assertEqual(cfg.get("TRANSLATION_REASONING_EFFORT"), "low")
        self.assertEqual(cfg.get("TRANSLATION_CLI_TIMEOUT"), "60")
        self.assertEqual(cfg.get("TRANSLATION_RETRY_DELAY"), "0")

    def test_config_rejects_invalid_numeric_runtime_options(self):
        base_env = {
            "TRANSLATION_PROVIDER": "cli",
            "TRANSLATION_CLI_COMMAND": "codex exec",
            "TRANSLATION_MODEL": "gpt-5.6-luna",
        }
        cases = (
            (
                "TRANSLATION_RETRY_DELAY",
                "later",
                "TRANSLATION_RETRY_DELAY must be an integer >= 0",
            ),
            (
                "TRANSLATION_RETRY_DELAY",
                "-1",
                "TRANSLATION_RETRY_DELAY must be an integer >= 0",
            ),
            (
                "TRANSLATION_CLI_TIMEOUT",
                "later",
                "TRANSLATION_CLI_TIMEOUT must be an integer > 0",
            ),
            (
                "TRANSLATION_CLI_TIMEOUT",
                "0",
                "TRANSLATION_CLI_TIMEOUT must be an integer > 0",
            ),
        )

        for key, value, message in cases:
            with self.subTest(key=key, value=value):
                with self.assertRaisesRegex(config.ConfigError, message):
                    config.load_config({**base_env, key: value})

    def test_annotation_format_is_locale_neutral(self):
        self.assertNotIn("한국어", translate._ANNOTATION_FORMAT)
        self.assertNotIn("Translated Section Title", translate._ANNOTATION_FORMAT)
        self.assertIn("# Section Title", translate._ANNOTATION_FORMAT)
        self.assertIn("translated paragraph", translate._ANNOTATION_FORMAT.lower())
        self.assertIn(
            "Do not add English source comments to blockquoted prose",
            translate._ANNOTATION_FORMAT,
        )
        self.assertIn(
            "lists made entirely of inline-code identifiers",
            translate._ANNOTATION_FORMAT,
        )
        self.assertIn(
            "including its complete Markdown marker",
            translate._ANNOTATION_FORMAT,
        )
        self.assertIn(
            "escape literal `-->` as `--&gt;`",
            translate._ANNOTATION_FORMAT,
        )

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

    def test_retries_cli_transport_failures(self):
        details = (
            "stream disconnected before completion",
            "error sending request for url",
            "Could not resolve host: api.example.test",
            "temporary failure in name resolution",
            "dns error: failed to lookup address information",
            "request timeout",
            "operation timeout",
            "connection timeout",
            "timeout",
            "context deadline exceeded",
        )
        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

        for detail in details:
            with self.subTest(detail=detail):
                calls = 0

                def respond(
                    _chunk: str, _config: config.Config, _prompt: str
                ) -> str:
                    nonlocal calls
                    calls += 1
                    if calls == 1:
                        raise subprocess.CalledProcessError(
                            1, ["luna"], stderr=detail
                        )
                    return "translated"

                result = translate._with_retries(
                    respond,
                    "chunk",
                    cfg,
                    "prompt",
                    sleep=lambda _: None,
                )

                self.assertEqual(result, "translated")
                self.assertEqual(calls, 2)

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

    def test_retries_blank_responses_until_nonblank_result(self):
        responses = iter((" ", "\n", "translated"))
        sleeps: list[float] = []

        def respond(_chunk: str, _config: config.Config, _prompt: str) -> str:
            return next(responses)

        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

        result = translate._with_retries(
            respond,
            "chunk",
            cfg,
            "prompt",
            sleep=sleeps.append,
        )

        self.assertEqual(result, "translated")
        self.assertEqual(len(sleeps), 2)

    def test_blank_responses_exhaust_attempts(self):
        calls = 0
        sleeps: list[float] = []

        def respond(_chunk: str, _config: config.Config, _prompt: str) -> str:
            nonlocal calls
            calls += 1
            return " "

        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

        with self.assertRaises(translate.IncompleteTranslation):
            translate._with_retries(
                respond,
                "chunk",
                cfg,
                "prompt",
                sleep=sleeps.append,
            )

        self.assertEqual(calls, translate.MAX_ATTEMPTS)
        self.assertEqual(len(sleeps), translate.MAX_ATTEMPTS - 1)

    def test_retries_http_429_and_5xx_errors(self):
        class HttpError(Exception):
            def __init__(self, status_code: int):
                super().__init__(f"HTTP {status_code}")
                self.status_code = status_code

        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
        for status_code in (429, 500, 502, 503, 504, 599):
            with self.subTest(status_code=status_code):
                calls = 0

                def respond(
                    _chunk: str, _config: config.Config, _prompt: str
                ) -> str:
                    nonlocal calls
                    calls += 1
                    if calls == 1:
                        raise HttpError(status_code)
                    return "translated"

                result = translate._with_retries(
                    respond,
                    "chunk",
                    cfg,
                    "prompt",
                    sleep=lambda _: None,
                )

                self.assertEqual(result, "translated")
                self.assertEqual(calls, 2)

    def test_retries_cli_http_status_messages(self):
        details = (
            "Error: 503 Service Unavailable",
            "API error: 502 Bad Gateway",
            "upstream returned 500 Internal Server Error",
            "codex exited: 429 Too Many Requests",
        )
        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

        for detail in details:
            with self.subTest(detail=detail):
                calls = 0

                def respond(
                    _chunk: str, _config: config.Config, _prompt: str
                ) -> str:
                    nonlocal calls
                    calls += 1
                    if calls == 1:
                        raise subprocess.CalledProcessError(
                            1, ["codex"], stderr=detail
                        )
                    return "translated"

                result = translate._with_retries(
                    respond,
                    "chunk",
                    cfg,
                    "prompt",
                    sleep=lambda _: None,
                )

                self.assertEqual(result, "translated")
                self.assertEqual(calls, 2)

    def test_cli_usage_and_model_errors_stop_immediately(self):
        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
        for detail in (
            "invalid model: gpt-500",
            "unexpected argument '--connection-mode'",
        ):
            with self.subTest(detail=detail):
                calls = 0

                def respond(
                    _chunk: str, _config: config.Config, _prompt: str
                ) -> str:
                    nonlocal calls
                    calls += 1
                    raise subprocess.CalledProcessError(
                        2, ["codex"], stderr=detail
                    )

                with self.assertRaises(translate.IncompleteTranslation):
                    translate._with_retries(
                        respond,
                        "chunk",
                        cfg,
                        "prompt",
                        sleep=lambda _: None,
                    )

                self.assertEqual(calls, 1)

    def test_nonretryable_http_errors_stop_immediately(self):
        class HttpError(Exception):
            status_code = 400

        calls = 0

        def respond(_chunk: str, _config: config.Config, _prompt: str) -> str:
            nonlocal calls
            calls += 1
            raise HttpError("bad request")

        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

        with self.assertRaisesRegex(
            translate.IncompleteTranslation,
            "bad request",
        ) as raised:
            translate._with_retries(
                respond,
                "chunk",
                cfg,
                "prompt",
                sleep=lambda _: None,
            )

        self.assertEqual(calls, 1)
        self.assertIsInstance(raised.exception.__cause__, HttpError)

    def test_azure_request_uses_chat_completions(self):
        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation="기존 번역입니다.",
        )
        response = SimpleNamespace(
            choices=[
                SimpleNamespace(
                    finish_reason="stop",
                    message=SimpleNamespace(content="translated"),
                )
            ]
        )
        cfg = config.Config(
            provider="azure",
            values={
                "TRANSLATION_MODEL": "model",
                "TRANSLATION_REASONING_EFFORT": "medium",
                "AZURE_OPENAI_API_KEY": "key",
                "AZURE_OPENAI_API_VERSION": "version",
                "AZURE_OPENAI_ENDPOINT": "endpoint",
            },
        )

        with patch("openai.AzureOpenAI") as client_class:
            client_class.return_value.chat.completions.create.return_value = response

            result = translate.translate_request(request, cfg, "prompt")

        self.assertEqual(result, "translated")
        client_class.assert_called_once_with(
            api_key="key",
            api_version="version",
            azure_endpoint="endpoint",
            max_retries=0,
        )
        client_class.return_value.chat.completions.create.assert_called_once_with(
            model="model",
            reasoning_effort="medium",
            messages=[
                {
                    "role": "system",
                    "content": "prompt" + translate._ANNOTATION_FORMAT,
                },
                {"role": "user", "content": request.render()},
            ],
        )

    def test_openai_request_uses_responses_and_returns_output_text(self):
        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation="기존 번역입니다.",
        )
        cfg = config.Config(
            provider="openai",
            values={
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                "TRANSLATION_REASONING_EFFORT": "medium",
                "OPENAI_API_KEY": "key",
            },
        )

        with patch("openai.OpenAI") as client_class:
            client_class.return_value.responses.create.return_value = SimpleNamespace(
                status="completed",
                output_text="translated Markdown",
            )

            out = translate.translate_request(request, cfg, "prompt")

        self.assertEqual(out, "translated Markdown")
        client_class.assert_called_once_with(api_key="key", max_retries=0)
        client_class.return_value.responses.create.assert_called_once_with(
            model="gpt-5.6-luna",
            instructions="prompt" + translate._ANNOTATION_FORMAT,
            input=request.render(),
            reasoning={"effort": "medium"},
            store=False,
        )

    def test_openai_incomplete_response_is_not_accepted(self):
        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="openai",
            values={
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                "OPENAI_API_KEY": "key",
            },
        )
        response = SimpleNamespace(
            status="incomplete",
            incomplete_details=SimpleNamespace(reason="max_output_tokens"),
            output_text="partial Markdown",
        )

        with patch("openai.OpenAI") as client_class:
            client_class.return_value.responses.create.return_value = response

            with self.assertRaisesRegex(
                translate.IncompleteTranslation,
                "incomplete.*max_output_tokens",
            ):
                translate.translate_request(request, cfg, "prompt")

        self.assertEqual(client_class.return_value.responses.create.call_count, 1)

    def test_azure_truncated_response_is_not_accepted(self):
        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="azure",
            values={
                "TRANSLATION_MODEL": "model",
                "AZURE_OPENAI_API_KEY": "key",
                "AZURE_OPENAI_API_VERSION": "version",
                "AZURE_OPENAI_ENDPOINT": "endpoint",
            },
        )
        response = SimpleNamespace(
            choices=[
                SimpleNamespace(
                    finish_reason="length",
                    message=SimpleNamespace(content="partial Markdown"),
                )
            ]
        )

        with patch("openai.AzureOpenAI") as client_class:
            client_class.return_value.chat.completions.create.return_value = response

            with self.assertRaisesRegex(
                translate.IncompleteTranslation,
                "finish_reason.*length",
            ):
                translate.translate_request(request, cfg, "prompt")

        self.assertEqual(
            client_class.return_value.chat.completions.create.call_count,
            1,
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

    def test_identity_request_returns_source_without_live_provider(self):
        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation="기존 번역입니다.",
            diff_text="+ Changed source.",
        )
        cfg = config.Config(
            provider="identity",
            values={"TRANSLATION_PROVIDER": "identity"},
        )

        with patch.object(
            translate,
            "translate_text",
            side_effect=AssertionError("live provider should not run"),
        ):
            out = translate.translate_request(request, cfg, "prompt")

        self.assertEqual(out, "Changed source.\n")

    def test_cli_request_returns_only_the_last_agent_message(self):
        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_CLI_COMMAND": "codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                "TRANSLATION_REASONING_EFFORT": "medium",
            },
        )

        calls = []

        def run(command, **kwargs):
            calls.append((command, kwargs))
            output_flag = command.index("--output-last-message")
            Path(command[output_flag + 1]).write_text(
                "translated Markdown", encoding="utf-8"
            )
            return subprocess.CompletedProcess(
                command,
                0,
                stdout="formatted agent progress",
                stderr="",
            )

        parent_environment = {
            "PATH": "/usr/bin",
            "HOME": "/tmp/home",
            "CODEX_HOME": "/tmp/codex-home",
            "CODEX_ACCESS_TOKEN": "allowed-codex-token",
            "OPENAI_API_KEY": "allowed-openai-key",
            "HTTPS_PROXY": "https://proxy.example",
            "LANG": "ko_KR.UTF-8",
            "AZURE_OPENAI_API_KEY": "must-not-leak",
            "UNRELATED_SECRET": "must-not-leak",
        }
        with patch.dict("os.environ", parent_environment, clear=True), patch(
            "subprocess.run", side_effect=run
        ):
            out = translate.translate_request(request, cfg, "prompt")

        self.assertEqual(out, "translated Markdown")
        self.assertEqual(len(calls), 1)
        command, kwargs = calls[0]
        self.assertEqual(command[:2], ["codex", "exec"])
        self.assertIn("--ignore-user-config", command)
        self.assertIn("--ignore-rules", command)
        self.assertIn("--ephemeral", command)
        for feature in (
            "apps",
            "browser_use",
            "browser_use_external",
            "browser_use_full_cdp_access",
            "computer_use",
            "hooks",
            "image_generation",
            "in_app_browser",
            "multi_agent",
            "plugins",
            "plugin_sharing",
            "remote_plugin",
            "shell_snapshot",
            "shell_tool",
            "tool_suggest",
            "unified_exec",
            "workspace_dependencies",
        ):
            self.assertIn(("--disable", feature), zip(command, command[1:]))
        self.assertIn("--strict-config", command)
        self.assertEqual(command[command.index("--model") + 1], "gpt-5.6-luna")
        self.assertEqual(
            command[command.index("-c") + 1],
            'model_reasoning_effort="medium"',
        )
        self.assertIn("project_doc_max_bytes=0", command)
        self.assertIn('web_search="disabled"', command)
        self.assertIn('shell_environment_policy.inherit="none"', command)
        self.assertIn("allow_login_shell=false", command)
        self.assertEqual(command[command.index("--sandbox") + 1], "read-only")
        self.assertEqual(command[-1], "prompt" + translate._ANNOTATION_FORMAT)
        self.assertEqual(
            kwargs["input"],
            request.render(),
        )
        self.assertEqual(kwargs["cwd"], str(Path(command[-2]).parent))
        self.assertTrue(kwargs["check"])
        self.assertEqual(
            kwargs["env"],
            {
                "PATH": "/usr/bin",
                "HOME": "/tmp/home",
                "CODEX_HOME": "/tmp/codex-home",
                "CODEX_ACCESS_TOKEN": "allowed-codex-token",
                "OPENAI_API_KEY": "allowed-openai-key",
                "HTTPS_PROXY": "https://proxy.example",
                "LANG": "ko_KR.UTF-8",
            },
        )

    def test_cli_chunk_outputs_preserve_source_boundaries(self):
        content = ("Source line.\n" * 399) + "\nFinal line.\n"
        outputs = iter(("first translated chunk", "second translated chunk"))
        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_CLI_COMMAND": "codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
            },
        )

        def run(command, **_kwargs):
            output_flag = command.index("--output-last-message")
            Path(command[output_flag + 1]).write_text(
                next(outputs), encoding="utf-8"
            )
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

        with patch("subprocess.run", side_effect=run):
            out = translate.translate_text(content, cfg, "prompt")

        self.assertEqual(
            out,
            "first translated chunk\n\nsecond translated chunk\n",
        )

    def test_cli_usage_errors_stop_immediately_with_diagnostics(self):
        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_CLI_COMMAND": "codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                "TRANSLATION_RETRY_DELAY": "0",
            },
        )
        error = subprocess.CalledProcessError(
            2,
            ["codex", "exec"],
            stderr="unknown option --invalid",
        )

        with patch("subprocess.run", side_effect=error) as run:
            with self.assertRaisesRegex(
                translate.IncompleteTranslation,
                "unknown option --invalid",
            ):
                translate.translate_request(request, cfg, "prompt")

        self.assertEqual(run.call_count, 1)

    def test_cli_error_diagnostics_redact_allowed_credentials(self):
        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_CLI_COMMAND": "codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                "TRANSLATION_RETRY_DELAY": "0",
            },
        )
        error = subprocess.CalledProcessError(
            1,
            ["codex", "exec"],
            stderr="authentication failed for secret-token",
        )

        with patch.dict(
            "os.environ",
            {"OPENAI_API_KEY": "secret-token"},
            clear=True,
        ), patch("subprocess.run", side_effect=error):
            with self.assertRaises(translate.IncompleteTranslation) as raised:
                translate.translate_request(request, cfg, "prompt")

        self.assertNotIn("secret-token", str(raised.exception))
        self.assertIn("[REDACTED:OPENAI_API_KEY]", str(raised.exception))

    def test_cli_error_diagnostics_redact_trimmed_credentials(self):
        error = subprocess.CalledProcessError(
            1,
            ["codex", "exec"],
            stderr="authentication failed for secret-token",
        )

        with patch.dict(
            "os.environ",
            {"OPENAI_API_KEY": "  secret-token\n"},
            clear=True,
        ):
            message = translate._provider_error_message(error)

        self.assertNotIn("secret-token", message)
        self.assertIn("[REDACTED:OPENAI_API_KEY]", message)

    def test_cli_rejects_codex_home_dotenv_before_process_start(self):
        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_CLI_COMMAND": "codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
            },
        )

        with TemporaryDirectory() as tmp:
            Path(tmp, ".env").write_text("UNRELATED_SECRET=value\n", encoding="utf-8")
            with patch.dict(
                "os.environ",
                {"HOME": tmp, "CODEX_HOME": tmp},
                clear=True,
            ), patch(
                "subprocess.run",
                side_effect=AssertionError("process must not start"),
            ) as run:
                with self.assertRaisesRegex(
                    translate.IncompleteTranslation,
                    r"CODEX_HOME/\.env.*environment allowlist",
                ):
                    translate.translate_request(request, cfg, "prompt")

            run.assert_not_called()

    def test_missing_cli_command_stops_immediately(self):
        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_CLI_COMMAND": "missing-codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                "TRANSLATION_RETRY_DELAY": "0",
            },
        )

        with patch(
            "subprocess.run",
            side_effect=FileNotFoundError("missing-codex not found"),
        ) as run:
            with self.assertRaisesRegex(
                translate.IncompleteTranslation,
                "missing-codex not found",
            ):
                translate.translate_request(request, cfg, "prompt")

        self.assertEqual(run.call_count, 1)

    def test_invalid_cli_executable_stops_immediately(self):
        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_CLI_COMMAND": "invalid-codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                "TRANSLATION_RETRY_DELAY": "0",
            },
        )

        with patch(
            "subprocess.run",
            side_effect=OSError(errno.ENOEXEC, "Exec format error"),
        ) as run:
            with self.assertRaisesRegex(
                translate.IncompleteTranslation,
                "Exec format error",
            ):
                translate.translate_request(request, cfg, "prompt")

        self.assertEqual(run.call_count, 1)


if __name__ == "__main__":
    unittest.main()
