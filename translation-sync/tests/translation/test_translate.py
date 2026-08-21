"""`translate` 동작과 경계 조건 검증."""

import errno
import subprocess
import traceback
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

from sync import config, postprocess, response_contract, translate
from sync.runtime.failure import IssueCode
from sync.runtime.process import ProcessTreeCleanupError

REQUEST_BUDGET_ENV = {
    "TRANSLATION_CONTEXT_WINDOW_TOKENS": "200000",
    "TRANSLATION_RESERVED_OUTPUT_TOKENS": "200",
    "TRANSLATION_REQUEST_TIMEOUT_SECONDS": "60",
    "TRANSLATION_RUN_TIMEOUT_SECONDS": "600",
    "TRANSLATION_TOKENIZER_ENCODING": "o200k_base",
}
CLI_AUTH_ENV = {"CODEX_ACCESS_TOKEN": "test-codex-token"}


class TranslateRetryTests(unittest.TestCase):
    """`translate` 재시도 동작과 경계 조건 모음."""

    def setUp(self):
        """테스트 사전 상태 구성."""

        token_counter = patch.object(
            translate,
            "_count_tokens",
            side_effect=lambda text, _encoding: len(text.split()),
        )
        token_counter.start()
        self.addCleanup(token_counter.stop)

    def test_config_requires_complete_request_budget(self):
        """승인 profile 기본값이 없는 설정의 요청 예산 전체 항목 요구 검증."""

        with self.assertRaisesRegex(
            config.ConfigError,
            "INVALID_REQUEST_BUDGET.*TRANSLATION_CONTEXT_WINDOW_TOKENS",
        ):
            config.load_config(
                {
                    "TRANSLATION_PROVIDER": "cli",
                    "TRANSLATION_CLI_COMMAND": "codex exec",
                    "TRANSLATION_MODEL": "unverified-model",
                    **CLI_AUTH_ENV,
                }
            )

    def test_translation_request_uses_a_safe_dynamic_diff_fence(self):
        """번역 요청의 안전한 동적 `diff` 펜스 사용 검증."""

        diff_text = "+ Before.\n+ ````php\n+ echo true;\n+ ````"
        request = translate.TranslationRequest(
            source="Before.\n\n````php\necho true;\n````\n",
            existing_translation=None,
            diff_text=diff_text,
        )

        rendered = request.render()

        self.assertIn("`````diff\n" + diff_text + "\n`````", rendered)
        self.assertEqual(rendered.count("`````"), 2)

    def test_translation_request_preserves_payload_whitespace_and_eof_bytes(self):
        """번역 요청의 페이로드 공백과 EOF 바이트 보존 검증."""

        source = "Source hard break.  \n\n"
        existing = "기존 hard break.  \nEOF spaces  "
        diff_text = "+ Source hard break.  \n+ EOF spaces  "
        feedback = "contract issue  \n"
        request = translate.TranslationRequest(
            source=source,
            existing_translation=existing,
            diff_text=diff_text,
            verification_feedback=feedback,
        )

        rendered = request.render()

        self.assertIn(
            "## English Diff\n\n```diff\n"
            + diff_text
            + "\n```\n\n",
            rendered,
        )
        self.assertIn(
            "## English Source\n\n"
            + source
            + "\n## Existing Translation Context",
            rendered,
        )
        self.assertIn(
            "## Existing Translation Context\n\n"
            + existing
            + "\n\n## Previous Output Verification Failure",
            rendered,
        )
        self.assertIn(
            "## Previous Output Verification Failure\n\n"
            + feedback
            + "\n## Output",
            rendered,
        )

    def test_identity_test_config_has_no_api_credentials(self):
        """테스트용 `identity` 설정이 API 인증을 갖지 않는지 검증."""

        cfg = config.Config(
            provider="identity",
            values={"TRANSLATION_PROVIDER": "identity"},
        )

        self.assertEqual(cfg.provider, "identity")
        self.assertIsNone(cfg.request_budget())

    def test_provider_configuration_errors_carry_stable_issue_codes(self):
        """제공자 구성 오류의 안정적인 이슈 코드 유지 검증."""

        with self.assertRaises(config.ConfigError) as invalid_provider:
            config.load_config({"TRANSLATION_PROVIDER": "private-value"})
        self.assertEqual(
            invalid_provider.exception.issue_code,
            IssueCode.PROVIDER_SELECTION_INVALID,
        )

        with self.assertRaises(config.ConfigError) as missing_credential:
            config.load_config(
                {
                    "TRANSLATION_PROVIDER": "openai",
                    "TRANSLATION_MODEL": "model",
                }
            )
        self.assertEqual(
            missing_credential.exception.issue_code,
            IssueCode.PROVIDER_CREDENTIAL_MISSING,
        )

    def test_cli_provider_requires_an_explicit_model(self):
        """CLI 제공자의 명시적 모델 요구 검증."""

        with self.assertRaises(config.ConfigError):
            config.load_config(
                {
                    "TRANSLATION_PROVIDER": "cli",
                    "TRANSLATION_CLI_COMMAND": "codex exec",
                }
            )

    def test_cli_provider_requires_explicit_authentication(self):
        """CLI 제공자의 명시적 인증 요구 검증."""

        with self.assertRaises(config.ConfigError) as raised:
            config.load_config(
                {
                    "TRANSLATION_PROVIDER": "cli",
                    "TRANSLATION_CLI_COMMAND": "codex exec",
                    "TRANSLATION_MODEL": "gpt-5.6-luna",
                    "OPENAI_API_KEY": "not-cli-authentication",
                    **REQUEST_BUDGET_ENV,
                }
            )

        self.assertEqual(
            raised.exception.issue_code,
            IssueCode.PROVIDER_CREDENTIAL_MISSING,
        )

    def test_cli_config_rejects_multiple_authentication_modes(self):
        """CLI 설정의 여러 인증 모드 거부 검증."""

        with self.assertRaises(config.ConfigError) as raised:
            config.load_config(
                {
                    "TRANSLATION_PROVIDER": "cli",
                    "TRANSLATION_CLI_COMMAND": "codex exec",
                    "TRANSLATION_MODEL": "gpt-5.6-luna",
                    "CODEX_ACCESS_TOKEN": "access-token",
                    "CODEX_API_KEY": "api-key",
                    "CODEX_HOME": "/tmp/codex-home",
                    **REQUEST_BUDGET_ENV,
                }
            )

        self.assertEqual(
            raised.exception.issue_code,
            IssueCode.INVALID_RUNTIME_OPTION,
        )

    def test_cli_config_accepts_documented_exec_authentication_modes(self):
        """CLI 설정의 문서화된 실행 인증 모드 허용 검증."""

        for key, value in (
            ("CODEX_ACCESS_TOKEN", "test-codex-access-token"),
            ("CODEX_API_KEY", "test-codex-api-key"),
            ("CODEX_HOME", "/tmp/test-codex-home"),
        ):
            with self.subTest(key=key):
                cfg = config.load_config(
                    {
                        "TRANSLATION_PROVIDER": "cli",
                        "TRANSLATION_CLI_COMMAND": "codex exec",
                        "TRANSLATION_MODEL": "gpt-5.6-luna",
                        key: value,
                        **REQUEST_BUDGET_ENV,
                    }
                )

                self.assertEqual(cfg.get(key), value)

    def test_config_drops_unapproved_openai_compatible_endpoint_settings(self):
        """승인되지 않은 OpenAI 호환 엔드포인트 설정 제거 검증."""

        base = {
            "TRANSLATION_PROVIDER": "openai",
            "TRANSLATION_MODEL": "gpt-5.6-luna",
            "OPENAI_API_KEY": "key",
            **REQUEST_BUDGET_ENV,
        }
        cfg = config.load_config(
            {
                **base,
                "OPENAI_BASE_URL": "https://compatible.example/v1",
                "OPENAI_ORGANIZATION": "unapproved-organization",
                "OPENAI_ORG_ID": "unapproved-org-id",
                "OPENAI_PROJECT": "unapproved-project",
                "OPENAI_PROJECT_ID": "unapproved-project-id",
            }
        )

        for key in (
            "OPENAI_BASE_URL",
            "OPENAI_ORGANIZATION",
            "OPENAI_ORG_ID",
            "OPENAI_PROJECT",
            "OPENAI_PROJECT_ID",
        ):
            self.assertEqual(cfg.get(key), "")
        self.assertEqual(
            config.provider_config_sha256(cfg),
            config.provider_config_sha256(config.load_config(base)),
        )

    def test_provider_config_hash_binds_profiles_without_credentials(self):
        """자격 증명을 제외하고 프로필을 반영한 제공자 구성 해시 검증."""

        base = {
            "TRANSLATION_PROVIDER": "openai",
            "TRANSLATION_MODEL": "gpt-5.6-luna",
            **REQUEST_BUDGET_ENV,
        }
        first = config.load_config({**base, "OPENAI_API_KEY": "first-secret"})
        second = config.load_config({**base, "OPENAI_API_KEY": "second-secret"})

        digest = config.provider_config_sha256(first)

        self.assertEqual(len(digest), 64)
        self.assertEqual(digest, config.provider_config_sha256(second))
        self.assertNotIn("first-secret", digest)
        with patch.object(config, "PROVIDER_BUDGET_PROFILE_VERSION", 2):
            self.assertNotEqual(digest, config.provider_config_sha256(first))
        with patch.object(config, "PROVIDER_FRAMING_OVERHEAD_TOKENS", 64_000):
            self.assertNotEqual(digest, config.provider_config_sha256(first))

    def test_provider_config_hash_binds_cli_auth_mode_not_secret_location(self):
        """비밀 위치 대신 CLI 인증 모드를 반영한 제공자 구성 해시 검증."""

        base = {
            "TRANSLATION_PROVIDER": "cli",
            "TRANSLATION_CLI_COMMAND": "codex exec",
            "TRANSLATION_MODEL": "gpt-5.6-luna",
            **REQUEST_BUDGET_ENV,
        }
        first_home = config.load_config(
            {**base, "CODEX_HOME": "/private/first-codex-home"}
        )
        second_home = config.load_config(
            {**base, "CODEX_HOME": "/private/second-codex-home"}
        )
        token = config.load_config(
            {**base, "CODEX_ACCESS_TOKEN": "secret-token"}
        )
        timed_token = config.load_config(
            {
                **base,
                "CODEX_ACCESS_TOKEN": "secret-token",
                "TRANSLATION_CLI_TIMEOUT": "60",
            }
        )

        self.assertEqual(
            config.provider_config_sha256(first_home),
            config.provider_config_sha256(second_home),
        )
        self.assertNotEqual(
            config.provider_config_sha256(first_home),
            config.provider_config_sha256(token),
        )
        self.assertNotEqual(
            config.provider_config_sha256(token),
            config.provider_config_sha256(timed_token),
        )

    def test_cli_provider_rejects_relative_codex_home(self):
        """CLI 제공자의 상대 `CODEX_HOME` 경로 거부 검증."""

        with self.assertRaises(config.ConfigError) as raised:
            config.load_config(
                {
                    "TRANSLATION_PROVIDER": "cli",
                    "TRANSLATION_CLI_COMMAND": "codex exec",
                    "TRANSLATION_MODEL": "gpt-5.6-luna",
                    "CODEX_HOME": "relative/codex-home",
                    **REQUEST_BUDGET_ENV,
                }
            )

        self.assertEqual(
            raised.exception.issue_code,
            IssueCode.INVALID_RUNTIME_OPTION,
        )

    def test_cli_provider_rejects_command_options_and_wrappers(self):
        """CLI 제공자의 명령 옵션과 래퍼 거부 검증."""

        for command in (
            "codex exec --full-auto",
            "python codex exec",
            "codex --profile exec",
        ):
            with self.subTest(command=command):
                with self.assertRaises(config.ConfigError) as raised:
                    config.load_config(
                        {
                            "TRANSLATION_PROVIDER": "cli",
                            "TRANSLATION_CLI_COMMAND": command,
                            "TRANSLATION_MODEL": "gpt-5.6-luna",
                            **CLI_AUTH_ENV,
                            **REQUEST_BUDGET_ENV,
                        }
                    )
                self.assertEqual(
                    raised.exception.issue_code,
                    IssueCode.INVALID_RUNTIME_OPTION,
                )

    def test_config_binds_budget_to_verified_model_metadata(self):
        """검증된 모델 메타데이터에 요청 예산을 결합하는 설정 검증."""

        base_env = {
            "TRANSLATION_PROVIDER": "openai",
            "TRANSLATION_MODEL": "gpt-5.6-luna",
            "OPENAI_API_KEY": "test-openai-key",
            **REQUEST_BUDGET_ENV,
        }
        invalid_cases = (
            (
                {"TRANSLATION_MODEL": "unverified-model"},
                IssueCode.TOKENIZER_METADATA_UNAVAILABLE,
            ),
            (
                {"TRANSLATION_TOKENIZER_ENCODING": "cl100k_base"},
                IssueCode.TOKENIZER_METADATA_UNAVAILABLE,
            ),
            (
                {"TRANSLATION_CONTEXT_WINDOW_TOKENS": "1050001"},
                IssueCode.INVALID_REQUEST_BUDGET,
            ),
            (
                {
                    "TRANSLATION_CONTEXT_WINDOW_TOKENS": "200000",
                    "TRANSLATION_RESERVED_OUTPUT_TOKENS": "128001",
                },
                IssueCode.INVALID_REQUEST_BUDGET,
            ),
        )

        for override, issue_code in invalid_cases:
            with self.subTest(override=override):
                with self.assertRaises(config.ConfigError) as raised:
                    config.load_config({**base_env, **override})
                self.assertEqual(raised.exception.issue_code, issue_code)

    def test_config_preserves_provider_runtime_options(self):
        """설정의 제공자 런타임 옵션 보존 검증."""

        cfg = config.load_config(
            {
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_CLI_COMMAND": "codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                "TRANSLATION_REASONING_EFFORT": "low",
                "TRANSLATION_CLI_TIMEOUT": "60",
                **CLI_AUTH_ENV,
                **REQUEST_BUDGET_ENV,
            }
        )

        self.assertEqual(cfg.get("TRANSLATION_REASONING_EFFORT"), "low")
        self.assertEqual(cfg.get("TRANSLATION_CLI_TIMEOUT"), "60")

    def test_config_does_not_expose_a_retry_delay_override(self):
        """재시도 지연 재정의 옵션을 노출하지 않는 설정 검증."""

        cfg = config.load_config(
            {
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_CLI_COMMAND": "codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                "TRANSLATION_RETRY_DELAY": "0",
                **CLI_AUTH_ENV,
                **REQUEST_BUDGET_ENV,
            }
        )

        self.assertEqual(cfg.get("TRANSLATION_RETRY_DELAY"), "")

    def test_config_rejects_invalid_numeric_runtime_options(self):
        """설정의 잘못된 숫자형 런타임 옵션 거부 검증."""

        base_env = {
            "TRANSLATION_PROVIDER": "cli",
            "TRANSLATION_CLI_COMMAND": "codex exec",
            "TRANSLATION_MODEL": "gpt-5.6-luna",
            **CLI_AUTH_ENV,
            **REQUEST_BUDGET_ENV,
        }
        cases = (
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

    def test_config_rejects_invalid_request_budget_relationships(self):
        """설정의 잘못된 요청 예산 관계 거부 검증."""

        base_env = {
            "TRANSLATION_PROVIDER": "cli",
            "TRANSLATION_CLI_COMMAND": "codex exec",
            "TRANSLATION_MODEL": "gpt-5.6-luna",
            **CLI_AUTH_ENV,
            **REQUEST_BUDGET_ENV,
        }
        cases = (
            ("TRANSLATION_CONTEXT_WINDOW_TOKENS", "0"),
            ("TRANSLATION_RESERVED_OUTPUT_TOKENS", "0"),
            ("TRANSLATION_RESERVED_OUTPUT_TOKENS", "200000"),
            ("TRANSLATION_REQUEST_TIMEOUT_SECONDS", "601"),
        )

        for key, value in cases:
            with self.subTest(key=key, value=value):
                with self.assertRaisesRegex(
                    config.ConfigError,
                    "INVALID_REQUEST_BUDGET",
                ):
                    config.load_config({**base_env, key: value})

    def test_config_rejects_unknown_tokenizer_metadata(self):
        """설정의 알 수 없는 토크나이저 메타데이터 거부 검증."""

        with self.assertRaisesRegex(
            config.ConfigError,
            "TOKENIZER_METADATA_UNAVAILABLE.*not-a-tokenizer",
        ):
            config.load_config(
                {
                    "TRANSLATION_PROVIDER": "cli",
                    "TRANSLATION_CLI_COMMAND": "codex exec",
                    "TRANSLATION_MODEL": "gpt-5.6-luna",
                    **CLI_AUTH_ENV,
                    **REQUEST_BUDGET_ENV,
                    "TRANSLATION_TOKENIZER_ENCODING": "not-a-tokenizer",
                }
            )

    def test_config_calculates_run_deadline_from_budget(self):
        """설정의 실행 예산으로 절대 실행 기한 계산 검증."""

        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                **REQUEST_BUDGET_ENV,
            },
        )

        deadline = config.required_run_deadline(
            cfg,
            clock=lambda: 100.0,
        )

        self.assertEqual(deadline, 700.0)

    def test_annotation_format_is_locale_neutral(self):
        """주석 형식의 로캘 중립성 검증."""

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

    def test_atomic_request_over_budget_fails_before_provider_call(self):
        """원자적 요청의 예산 초과 시 제공자 호출 전 실패 검증."""

        request = translate.TranslationRequest(
            source="One indivisible paragraph that must stay atomic.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                "TRANSLATION_CONTEXT_WINDOW_TOKENS": "50",
                "TRANSLATION_RESERVED_OUTPUT_TOKENS": "10",
                "TRANSLATION_REQUEST_TIMEOUT_SECONDS": "10",
                "TRANSLATION_RUN_TIMEOUT_SECONDS": "20",
                "TRANSLATION_TOKENIZER_ENCODING": "o200k_base",
            },
        )

        with patch.object(
            translate,
            "_count_tokens",
            side_effect=lambda text, _encoding: len(text),
        ), patch.object(
            translate,
            "_translate_chunk",
            side_effect=AssertionError("provider must not run"),
        ) as provider:
            with self.assertRaisesRegex(
                translate.IncompleteTranslation,
                "UNSUPPORTED_OVERSIZE_BLOCK",
            ):
                translate.translate_request(
                    request,
                    cfg,
                    "prompt",
                    deadline=100.0,
                    clock=lambda: 0.0,
                )

        provider.assert_not_called()

    def test_request_budget_includes_utf8_upper_bound_and_framing_reserve(self):
        """요청 예산의 UTF-8 상한과 프레이밍 예비량 포함 검증."""

        instructions = "System"
        payload = "한글 payload"
        self.assertEqual(config.PROVIDER_BUDGET_PROFILE_VERSION, 1)
        self.assertEqual(translate.PROVIDER_FRAMING_OVERHEAD_TOKENS, 128_000)
        cfg = config.Config(
            provider="openai",
            values={
                "TRANSLATION_PROVIDER": "openai",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                **REQUEST_BUDGET_ENV,
            },
        )

        with patch.object(
            translate,
            "_count_tokens",
            side_effect=(100, 200),
        ):
            conservative_tokens = translate._validate_request_budget(
                instructions,
                payload,
                cfg,
            )

        self.assertEqual(
            conservative_tokens,
            max(300, len((instructions + payload).encode("utf-8")))
            + translate.PROVIDER_FRAMING_OVERHEAD_TOKENS,
        )

    def test_utf8_upper_bound_rejects_request_even_when_exact_count_is_small(self):
        """정확한 토큰 수가 작아도 UTF-8 상한으로 요청을 거부하는지 검증."""

        instructions = "I"
        payload = "한" * 100
        byte_upper_bound = len((instructions + payload).encode("utf-8"))
        reserved_output = 200
        cfg = config.Config(
            provider="openai",
            values={
                "TRANSLATION_PROVIDER": "openai",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                **REQUEST_BUDGET_ENV,
                "TRANSLATION_CONTEXT_WINDOW_TOKENS": str(
                    translate.PROVIDER_FRAMING_OVERHEAD_TOKENS
                    + byte_upper_bound
                    + reserved_output
                    - 1
                ),
                "TRANSLATION_RESERVED_OUTPUT_TOKENS": str(reserved_output),
            },
        )

        with patch.object(translate, "_count_tokens", return_value=1):
            with self.assertRaisesRegex(
                translate.UnsupportedOversizeBlock,
                "including provider framing",
            ):
                translate._validate_request_budget(instructions, payload, cfg)

    def test_budgeted_request_requires_injected_absolute_deadline(self):
        """예산이 지정된 요청의 주입된 절대 기한 요구 검증."""

        request = translate.TranslationRequest(
            source="Atomic source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                **REQUEST_BUDGET_ENV,
            },
        )

        with patch.object(
            translate,
            "_translate_chunk",
            side_effect=AssertionError("provider must not run"),
        ) as provider:
            with self.assertRaisesRegex(
                translate.IncompleteTranslation,
                "RUN_DEADLINE_EXCEEDED.*absolute deadline",
            ):
                translate.translate_request(request, cfg, "prompt")

        provider.assert_not_called()

    def test_live_request_rejects_direct_config_without_request_budget(self):
        """요청 예산이 없는 직접 설정을 실시간 요청에서 거부하는지 검증."""

        request = translate.TranslationRequest(
            source="Atomic source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="openai",
            values={
                "TRANSLATION_PROVIDER": "openai",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                "OPENAI_API_KEY": "test-openai-key",
            },
        )

        with patch.object(
            translate,
            "_translate_chunk",
            side_effect=AssertionError("provider must not run"),
        ) as provider:
            with self.assertRaises(config.ConfigError) as raised:
                translate.translate_request(
                    request,
                    cfg,
                    "prompt",
                    deadline=1000.0,
                    clock=lambda: 0.0,
                )

        self.assertEqual(
            raised.exception.issue_code,
            IssueCode.INVALID_REQUEST_BUDGET,
        )
        provider.assert_not_called()

    def test_live_request_rejects_non_finite_absolute_deadline(self):
        """실시간 요청의 유한하지 않은 절대 기한 거부 검증."""

        request = translate.TranslationRequest(
            source="Atomic source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="openai",
            values={
                "TRANSLATION_PROVIDER": "openai",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                "OPENAI_API_KEY": "test-openai-key",
                **REQUEST_BUDGET_ENV,
            },
        )

        with patch.object(
            translate,
            "_translate_chunk",
            side_effect=AssertionError("provider must not run"),
        ) as provider:
            for deadline in (float("nan"), float("inf")):
                with self.subTest(deadline=deadline):
                    with self.assertRaisesRegex(
                        translate.RunDeadlineExceeded,
                        "absolute deadline",
                    ):
                        translate.translate_request(
                            request,
                            cfg,
                            "prompt",
                            deadline=deadline,
                            clock=lambda: 0.0,
                        )

        provider.assert_not_called()

    def test_retries_transient_provider_failures_with_same_chunk(self):
        """같은 청크로 일시적 제공자 실패 재시도 검증."""

        calls: list[str] = []

        def flaky(chunk: str, _config: config.Config, _prompt: str) -> str:
            """청크를 기록하고 첫 두 호출에는 TimeoutError, 세 번째 호출에는 번역 결과 반환."""

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

    def test_transient_retries_use_the_fixed_five_minute_delay(self):
        """일시적 실패 재시도에 고정 5분 지연 사용 검증."""

        calls = 0
        sleeps: list[float] = []

        def flaky(_chunk: str, _config: config.Config, _prompt: str) -> str:
            """호출 횟수를 기록하고 첫 두 호출에는 TimeoutError, 세 번째 호출에는 번역 결과 반환."""

            nonlocal calls
            calls += 1
            if calls < 3:
                raise TimeoutError("temporary timeout")
            return "translated"

        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_RETRY_DELAY": "0",
            },
        )

        result = translate._with_retries(
            flaky,
            "same chunk",
            cfg,
            "prompt",
            sleep=sleeps.append,
        )

        self.assertEqual(result, "translated")
        self.assertEqual(sleeps, [300, 300])

    def test_provider_result_is_rejected_when_the_deadline_expires_during_call(self):
        """제공자 호출 중 기한이 만료된 결과의 거부 판정 검증."""

        now = 0.0

        def respond(_chunk: str, _config: config.Config, _prompt: str) -> str:
            """가상 시각을 기한으로 이동한 뒤 번역 결과 반환."""

            nonlocal now
            now = 10.0
            return "translated"

        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                **REQUEST_BUDGET_ENV,
                "TRANSLATION_REQUEST_TIMEOUT_SECONDS": "1",
            },
        )

        with self.assertRaisesRegex(
            translate.RunDeadlineExceeded,
            "deadline was exceeded",
        ):
            translate._with_retries(
                respond,
                "source",
                cfg,
                "prompt",
                deadline=10.0,
                clock=lambda: now,
            )

    def test_request_rejects_a_mismatched_response_contract_version(self):
        """요청의 불일치하는 응답 계약 버전 거부 검증."""

        request = translate.TranslationRequest(
            source="Source.\n",
            existing_translation=None,
            response_contract_version=2,
        )
        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

        with patch.object(
            translate,
            "translate_text",
            side_effect=AssertionError("provider must not run"),
        ) as provider:
            with self.assertRaisesRegex(
                translate.ProviderRequestRejected,
                "unsupported response contract version: 2",
            ):
                translate.translate_request(request, cfg, "prompt")

        provider.assert_not_called()

    def test_response_contract_rejects_an_unsupported_version(self):
        """지원하지 않는 응답 계약 버전 거부 검증."""

        with self.assertRaisesRegex(
            ValueError,
            "unsupported response contract version: 2",
        ):
            response_contract.verify(
                "Source.\n",
                "Source.\n",
                locale=None,
                contract_version=2,
            )

    def test_retry_does_not_wait_when_next_call_would_exceed_deadline(self):
        """다음 호출이 기한을 초과할 경우 대기하지 않는 재시도 검증."""

        calls = 0
        sleeps: list[float] = []
        now = 0.0

        def fail(_chunk: str, _config: config.Config, _prompt: str) -> str:
            """호출 횟수를 기록하고 항상 TimeoutError 발생."""

            nonlocal calls
            calls += 1
            raise TimeoutError("temporary timeout")

        def sleep(seconds: float) -> None:
            """대기 시간을 기록하고 가상 시각을 해당 시간만큼 증가."""

            nonlocal now
            sleeps.append(seconds)
            now += seconds

        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                **REQUEST_BUDGET_ENV,
                "TRANSLATION_REQUEST_TIMEOUT_SECONDS": "10",
            },
        )

        with self.assertRaisesRegex(
            translate.IncompleteTranslation,
            "RUN_DEADLINE_EXCEEDED",
        ):
            translate._with_retries(
                fail,
                "same chunk",
                cfg,
                "prompt",
                sleep=sleep,
                clock=lambda: now,
                deadline=14.0,
            )

        self.assertEqual(calls, 1)
        self.assertEqual(sleeps, [])

    def test_provider_call_does_not_start_without_full_request_time_remaining(self):
        """전체 요청 시간이 부족한 제공자 호출의 시작 방지 검증."""

        calls = 0

        def respond(_chunk: str, _config: config.Config, _prompt: str) -> str:
            """호출 횟수를 기록하고 번역 결과 반환."""

            nonlocal calls
            calls += 1
            return "translated"

        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                **REQUEST_BUDGET_ENV,
                "TRANSLATION_REQUEST_TIMEOUT_SECONDS": "10",
            },
        )

        with self.assertRaisesRegex(
            translate.IncompleteTranslation,
            "RUN_DEADLINE_EXCEEDED",
        ):
            translate._with_retries(
                respond,
                "source",
                cfg,
                "prompt",
                deadline=9.0,
                clock=lambda: 0.0,
            )

        self.assertEqual(calls, 0)

    def test_retries_cli_transport_failures(self):
        """CLI 전송 실패 재시도 검증."""

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
                    """첫 호출에 CLI 전송 오류를 발생시키고 두 번째 호출에 번역 결과 반환."""

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

    def test_records_each_physical_provider_attempt_across_retries(self):
        """재시도 과정의 실제 제공자 호출별 기록 검증."""

        calls = 0
        counter = translate.ProviderAttemptCounter()

        def respond(
            _chunk: str, _config: config.Config, _prompt: str
        ) -> str:
            """첫 두 호출에 TimeoutExpired를 발생시키고 세 번째 호출에 번역 결과 반환."""

            nonlocal calls
            calls += 1
            if calls < 3:
                raise subprocess.TimeoutExpired(cmd="provider", timeout=1)
            return "translated"

        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

        result = translate._with_retries(
            respond,
            "chunk",
            cfg,
            "prompt",
            sleep=lambda _: None,
            attempt_counter=counter,
        )

        self.assertEqual(result, "translated")
        self.assertEqual(counter.transport, 3)

    def test_raises_incomplete_translation_after_max_retries(self):
        """최대 재시도 후 불완전 번역 오류 발생 검증."""

        def always_fails(chunk: str, _config: config.Config, _prompt: str) -> str:
            """모든 호출에 TimeoutExpired 발생."""

            raise subprocess.TimeoutExpired(cmd="translate", timeout=1)

        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

        with self.assertRaises(translate.ProviderTransientExhausted):
            translate._with_retries(
                always_fails,
                "chunk",
                cfg,
                "prompt",
                sleep=lambda _: None,
            )

    def test_retries_blank_responses_until_nonblank_result(self):
        """비어 있지 않은 결과까지 빈 응답 재시도 검증."""

        responses = iter((" ", "\n", "translated"))
        sleeps: list[float] = []

        def respond(_chunk: str, _config: config.Config, _prompt: str) -> str:
            """응답 iterator에서 다음 값을 반환."""

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
        """빈 응답으로 시도 횟수 소진 시 오류 발생 검증."""

        calls = 0
        sleeps: list[float] = []

        def respond(_chunk: str, _config: config.Config, _prompt: str) -> str:
            """호출 횟수를 기록하고 빈 응답 반환."""

            nonlocal calls
            calls += 1
            return " "

        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

        with self.assertRaises(translate.ProviderTransientExhausted):
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
        """HTTP 429와 5xx 오류 재시도 검증."""

        class HttpError(Exception):
            """HTTP 오류."""

            def __init__(self, status_code: int):
                """HTTP 상태 코드로 오류 초기화."""

                super().__init__(f"HTTP {status_code}")
                self.status_code = status_code

        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
        for status_code in (429, 500, 502, 503, 504, 599):
            with self.subTest(status_code=status_code):
                calls = 0

                def respond(
                    _chunk: str, _config: config.Config, _prompt: str
                ) -> str:
                    """첫 호출에 지정한 HTTP 오류를 발생시키고 두 번째 호출에 번역 결과 반환."""

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
        """CLI HTTP 상태 메시지 기반 재시도 검증."""

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
                    """첫 호출에 CLI HTTP 오류를 발생시키고 두 번째 호출에 번역 결과 반환."""

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
        """CLI 사용법과 모델 오류 발생 시 즉시 중단 검증."""

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
                    """호출 횟수를 기록하고 CLI 사용법 또는 모델 오류 발생."""

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

    def test_nonretryable_http_errors_stop_immediately_without_response_detail(self):
        """재시도할 수 없는 HTTP 오류의 응답 상세 비공개와 즉시 중단 검증."""

        class HttpError(Exception):
            """HTTP 오류."""

            status_code = 400

        calls = 0

        def respond(_chunk: str, _config: config.Config, _prompt: str) -> str:
            """호출 횟수를 기록하고 재시도 불가 HTTP 400 오류 발생."""

            nonlocal calls
            calls += 1
            raise HttpError("bad request")

        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

        with self.assertRaisesRegex(
            translate.IncompleteTranslation,
            r"provider request failed \(http_status=400\)",
        ) as raised:
            translate._with_retries(
                respond,
                "chunk",
                cfg,
                "prompt",
                sleep=lambda _: None,
            )

        self.assertEqual(calls, 1)
        self.assertIsNone(raised.exception.__cause__)
        self.assertNotIn("bad request", str(raised.exception))

    def test_openai_request_uses_responses_and_returns_output_text(self):
        """OpenAI 요청의 Responses API 사용과 `output_text` 반환 검증."""

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
                **REQUEST_BUDGET_ENV,
            },
        )

        with patch("openai.OpenAI") as client_class:
            client_class.return_value.responses.create.return_value = SimpleNamespace(
                status="completed",
                output_text="translated Markdown",
            )

            out = translate.translate_request(
                request,
                cfg,
                "prompt",
                deadline=1000.0,
                clock=lambda: 0.0,
            )

        self.assertEqual(out, "translated Markdown")
        client_class.assert_called_once_with(
            api_key="key",
            base_url=translate.OPENAI_API_BASE_URL,
            organization="",
            project="",
            max_retries=0,
            timeout=60,
        )
        client_class.return_value.responses.create.assert_called_once_with(
            model="gpt-5.6-luna",
            instructions="prompt" + translate._ANNOTATION_FORMAT,
            input=request.render(),
            reasoning={"effort": "medium"},
            store=False,
            max_output_tokens=200,
        )

    def test_openai_incomplete_response_is_not_accepted(self):
        """OpenAI 미완료 응답 거부 검증."""

        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="openai",
            values={
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                "OPENAI_API_KEY": "key",
                **REQUEST_BUDGET_ENV,
            },
        )
        response = SimpleNamespace(
            status="incomplete",
            incomplete_details=SimpleNamespace(
                reason="PRIVATE_OPENAI_RESPONSE_DETAIL"
            ),
            output_text="PRIVATE_OPENAI_RESPONSE_BODY",
        )

        with patch("openai.OpenAI") as client_class:
            client_class.return_value.responses.create.return_value = response

            with self.assertRaisesRegex(
                translate.IncompleteTranslation,
                r"adapter=openai, status=incomplete",
            ) as raised:
                translate.translate_request(
                    request,
                    cfg,
                    "prompt",
                    deadline=1000.0,
                    clock=lambda: 0.0,
                )

        self.assertEqual(client_class.return_value.responses.create.call_count, 1)
        self.assertNotIn("PRIVATE_OPENAI", str(raised.exception))

    def test_split_chunks_keeps_anchor_with_following_heading(self):
        """`split_chunks`에서 앵커와 다음 제목을 함께 유지하는지 검증."""

        content = '<a name="intro"></a>\n\n## Introduction\n\nBody.\n'

        chunks = translate.split_chunks(content, max_lines=2)

        self.assertEqual(chunks, [content])

    def test_split_chunks_keeps_long_fenced_code_blocks_intact(self):
        """`split_chunks`에서 긴 펜스 코드 블록을 분할하지 않는지 검증."""

        content = "````markdown\n```php\necho 'ok';\n```\n````\n\nAfter.\n"

        chunks = translate.split_chunks(content, max_lines=2)

        self.assertEqual(chunks, [content])

    def test_split_chunks_does_not_split_an_atomic_owner_by_line_count(self):
        """`split_chunks`에서 원자적 소유자를 줄 수 기준으로 분할하지 않는지 검증."""

        content = ("Atomic owner line.\n" * 400) + "\nNext line.\n"

        chunks = translate.split_chunks(content, max_lines=2)

        self.assertEqual(chunks, [content])

    def test_translate_text_can_skip_internal_chunking(self):
        """`translate_text`의 내부 청크 분할 생략 지원 검증."""

        calls: list[str] = []

        def collect(chunk: str, _config: config.Config, _prompt: str) -> str:
            """호출 청크 수집."""

            calls.append(chunk)
            return chunk

        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                **REQUEST_BUDGET_ENV,
            },
        )

        with patch.object(translate, "_translate_chunk", side_effect=collect):
            out = translate.translate_text(
                "a\n\nb\n",
                cfg,
                "prompt",
                split=False,
                deadline=1000.0,
                clock=lambda: 0.0,
            )

        self.assertEqual(out, "a\n\nb\n")
        self.assertEqual(calls, ["a\n\nb\n"])

    def test_identity_request_returns_canonical_annotated_source_without_live_provider(self):
        """`identity` 요청에서 실시간 제공자 없이 표준 주석 원문 반환 검증."""

        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation="기존 번역입니다.",
            diff_text="+ Changed source.",
            version="13.x",
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

        self.assertEqual(out, "<!-- Changed source. -->\nChanged source.\n")
        self.assertEqual(
            response_contract.verify(out, request.source, locale=None),
            [],
        )

    def test_identity_request_uses_non_rendered_version_metadata(self):
        """`identity` 요청의 렌더링되지 않은 버전 메타데이터 사용 검증."""

        request = translate.TranslationRequest(
            source="Read the [guide](/docs/{{version}}/guide).\n",
            existing_translation=None,
            version="13.x",
        )
        cfg = config.Config(
            provider="identity",
            values={"TRANSLATION_PROVIDER": "identity"},
        )

        self.assertNotIn("13.x", request.render())
        out = translate.translate_request(request, cfg, "prompt")

        expected_source = request.source.replace("{{version}}", "13.x")
        self.assertIn("/docs/13.x/guide", out)
        self.assertEqual(
            response_contract.verify(out, expected_source, locale=None),
            [],
        )

    def test_identity_response_leaves_stale_link_normalization_to_postprocessing(self):
        """`identity` 응답의 오래된 링크 정규화를 후처리에 위임하는지 검증."""

        source = (
            "Read the [controller guide](controllers#actions-handled-by-resource-controller) "
            "for /docs/{{version}}.\n\n"
            "```text\n"
            "/docs/{{version}}\n"
            "```\n"
        )
        request = translate.TranslationRequest(
            source=source,
            existing_translation=None,
            version="10.x",
        )
        cfg = config.Config(
            provider="identity",
            values={"TRANSLATION_PROVIDER": "identity"},
        )

        out = translate.translate_request(request, cfg, "prompt")

        self.assertIn("for /docs/10.x.", out)
        self.assertIn("/docs/{{version}}\n```", out)
        self.assertEqual(
            response_contract.verify(
                out,
                response_contract.identity_source_view(source, "10.x"),
                locale=None,
            ),
            [],
        )
        normalized = postprocess.postprocess(out, "10.x", {})
        self.assertIn(
            "[controller guide](controllers#actions-handled-by-resource-controllers)",
            normalized,
        )
        self.assertIn(
            "<!-- Read the [controller guide](controllers#actions-handled-by-resource-controller) "
            "for /docs/10.x. -->",
            normalized,
        )

    def test_identity_response_preserves_full_replay_structure_contract(self):
        """`identity` 응답의 전체 `replay` 구조 계약 보존 검증."""

        source = (
            "<!-- source-authored -->\n\n"
            "# Heading\n\n"
            "Use `Widget` from [Package Index](/packages).\n\n"
            "- Run `widget:init`.\n\n"
            "> [!NOTE]\n"
            "> Keep this quoted body.\n\n"
            "| Name | Value |\n"
            "| --- | --- |\n"
            "| Widget | `enabled` |\n\n"
            "```php\n"
            "echo 'unchanged';\n"
            "```\n"
        )
        request = translate.TranslationRequest(
            source=source,
            existing_translation=None,
            version="13.x",
        )
        cfg = config.Config(
            provider="identity",
            values={"TRANSLATION_PROVIDER": "identity"},
        )

        out = translate.translate_request(request, cfg, "prompt")

        self.assertEqual(response_contract.verify(out, source, locale=None), [])
        self.assertNotIn("Translation Sync Input", out)
        self.assertIn("<!-- source-authored -->", out)
        self.assertIn("<!-- Use `Widget` from [Package Index](/packages). -->", out)
        self.assertIn(
            "<!-- | Name | Value | | --- | --- | | Widget | `enabled` | -->",
            out,
        )

    def test_identity_request_requires_version_metadata(self):
        """`identity` 요청의 버전 메타데이터 요구 검증."""

        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="identity",
            values={"TRANSLATION_PROVIDER": "identity"},
        )

        with self.assertRaisesRegex(
            translate.ProviderRequestRejected,
            "missing version metadata",
        ):
            translate.translate_request(request, cfg, "prompt")

    def test_cli_fixture_and_candidate_use_the_same_explicit_authentication(self):
        """CLI 픽스처와 후보의 동일한 명시적 인증 사용 검증."""

        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "CODEX_ACCESS_TOKEN": "selected-token",
            },
        )
        with TemporaryDirectory() as tmp, patch.dict(
            "os.environ",
            {
                "HOME": "/ambient/home",
                "CODEX_ACCESS_TOKEN": "ambient-token",
                "OPENAI_API_KEY": "ambient-openai-token",
            },
            clear=True,
        ):
            fixture_environment = translate._cli_environment(
                cfg,
                Path(tmp) / "fixture-home",
            )
            candidate_environment = translate._cli_environment(
                cfg,
                Path(tmp) / "candidate-home",
            )

        for environment in (fixture_environment, candidate_environment):
            self.assertEqual(
                environment["CODEX_ACCESS_TOKEN"],
                "selected-token",
            )
            self.assertNotIn("OPENAI_API_KEY", environment)
            self.assertNotEqual(environment["HOME"], "/ambient/home")
            self.assertEqual(
                environment["CODEX_HOME"],
                str(Path(environment["HOME"]) / ".codex"),
            )

    def test_cli_transport_uses_request_budget_timeout(self):
        """CLI 전송의 요청 예산 시간 제한 사용 검증."""

        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_CLI_COMMAND": "codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                **CLI_AUTH_ENV,
                **REQUEST_BUDGET_ENV,
                "TRANSLATION_REQUEST_TIMEOUT_SECONDS": "17",
            },
        )

        def run(command, **kwargs):
            """번역 결과 파일을 작성하고 완료된 프로세스 반환."""

            output_flag = command.index("--output-last-message")
            Path(command[output_flag + 1]).write_text(
                "translated", encoding="utf-8"
            )
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

        with patch.object(
            translate,
            "run_process_tree",
            side_effect=run,
        ) as process:
            translate._translate_cli("source", cfg, "prompt")

        self.assertEqual(process.call_args.kwargs["timeout"], 17)

    def test_cli_atomic_output_preserves_source_ending(self):
        """CLI 원자적 출력의 원문 끝 형식 보존 검증."""

        content = ("Source line.\n" * 399) + "\nFinal line.\n"
        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_CLI_COMMAND": "codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                **CLI_AUTH_ENV,
                **REQUEST_BUDGET_ENV,
            },
        )

        def run(command, **_kwargs):
            """줄바꿈 없는 번역 결과 파일을 작성하고 완료된 프로세스 반환."""

            output_flag = command.index("--output-last-message")
            Path(command[output_flag + 1]).write_text(
                "translated atomic owner", encoding="utf-8"
            )
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

        with patch.object(translate, "run_process_tree", side_effect=run):
            out = translate.translate_text(
                content,
                cfg,
                "prompt",
                deadline=1000.0,
                clock=lambda: 0.0,
            )

        self.assertEqual(
            out,
            "translated atomic owner\n",
        )

    def test_cli_usage_errors_stop_immediately_without_captured_output(self):
        """CLI 사용법 오류의 캡처 출력 비공개와 즉시 중단 검증."""

        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_CLI_COMMAND": "codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                **CLI_AUTH_ENV,
                **REQUEST_BUDGET_ENV,
            },
        )
        error = subprocess.CalledProcessError(
            2,
            ["codex", "exec"],
            stderr="unknown option --invalid",
        )

        with patch.object(
            translate,
            "run_process_tree",
            side_effect=error,
        ) as run:
            with self.assertRaisesRegex(
                translate.IncompleteTranslation,
                r"provider command failed \(exit_code=2\)",
            ) as raised:
                translate.translate_request(
                    request,
                    cfg,
                    "prompt",
                    deadline=1000.0,
                    clock=lambda: 0.0,
                )

        self.assertEqual(run.call_count, 1)
        self.assertNotIn("unknown option", str(raised.exception))

    def test_cli_error_diagnostics_do_not_render_captured_stderr(self):
        """CLI 오류 진단의 캡처된 표준 오류 비노출 검증."""

        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_CLI_COMMAND": "codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                "CODEX_ACCESS_TOKEN": "secret-token",
                **REQUEST_BUDGET_ENV,
            },
        )
        error = subprocess.CalledProcessError(
            1,
            ["codex", "exec"],
            output="PRIVATE_CLI_STDOUT secret-token",
            stderr="PRIVATE_CLI_STDERR secret-token",
        )

        with patch.dict(
            "os.environ",
            {"OPENAI_API_KEY": "secret-token"},
            clear=True,
        ), patch.object(translate, "run_process_tree", side_effect=error):
            with self.assertRaises(translate.IncompleteTranslation) as raised:
                translate.translate_request(
                    request,
                    cfg,
                    "prompt",
                    deadline=1000.0,
                    clock=lambda: 0.0,
                )

        self.assertNotIn("secret-token", str(raised.exception))
        self.assertNotIn("PRIVATE_CLI", str(raised.exception))
        rendered_traceback = "".join(
            traceback.format_exception(raised.exception)
        )
        self.assertNotIn("secret-token", rendered_traceback)
        self.assertNotIn("PRIVATE_CLI", rendered_traceback)
        self.assertEqual(
            str(raised.exception),
            "provider command failed (exit_code=1)",
        )

    def test_provider_error_message_never_depends_on_secret_replacement(self):
        """제공자 오류 메시지가 비밀값 치환에 의존하지 않는지 검증."""

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
        self.assertEqual(message, "provider command failed (exit_code=1)")

    def test_cli_rejects_codex_home_dotenv_before_process_start(self):
        """CLI 프로세스 시작 전 `CODEX_HOME`의 `.env` 거부 검증."""

        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation=None,
        )

        with TemporaryDirectory() as tmp:
            Path(tmp, ".env").write_text("UNRELATED_SECRET=value\n", encoding="utf-8")
            cfg = config.Config(
                provider="cli",
                values={
                    "TRANSLATION_CLI_COMMAND": "codex exec",
                    "TRANSLATION_MODEL": "gpt-5.6-luna",
                    "CODEX_HOME": tmp,
                    **REQUEST_BUDGET_ENV,
                },
            )
            with patch.dict(
                "os.environ",
                {"HOME": "/ambient/home"},
                clear=True,
            ), patch.object(
                translate,
                "run_process_tree",
                side_effect=AssertionError("process must not start"),
            ) as run:
                with self.assertRaisesRegex(
                    translate.IncompleteTranslation,
                    "provider request failed",
                ):
                    translate.translate_request(
                        request,
                        cfg,
                        "prompt",
                        deadline=1000.0,
                        clock=lambda: 0.0,
                    )

            run.assert_not_called()

    def test_cli_process_tree_failure_stops_without_retry(self):
        """CLI 프로세스 트리 실패 시 재시도 없이 중단 검증."""

        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_CLI_COMMAND": "codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                **CLI_AUTH_ENV,
                **REQUEST_BUDGET_ENV,
            },
        )

        with patch.object(
            translate,
            "run_process_tree",
            side_effect=ProcessTreeCleanupError("private cleanup detail"),
        ) as run:
            with self.assertRaisesRegex(
                translate.CliProviderFailed,
                "provider process isolation failed",
            ):
                translate.translate_request(
                    request,
                    cfg,
                    "prompt",
                    deadline=1000.0,
                    clock=lambda: 0.0,
                )

        self.assertEqual(run.call_count, 1)

    def test_missing_cli_command_stops_immediately(self):
        """누락된 CLI 명령 발견 시 즉시 중단 검증."""

        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_CLI_COMMAND": "/missing/codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                **CLI_AUTH_ENV,
                **REQUEST_BUDGET_ENV,
            },
        )

        with patch.object(
            translate,
            "run_process_tree",
            side_effect=FileNotFoundError("missing-codex not found"),
        ) as run:
            with self.assertRaisesRegex(
                translate.IncompleteTranslation,
                "provider command is unavailable",
            ):
                translate.translate_request(
                    request,
                    cfg,
                    "prompt",
                    deadline=1000.0,
                    clock=lambda: 0.0,
                )

        self.assertEqual(run.call_count, 1)

    def test_invalid_cli_executable_stops_immediately(self):
        """잘못된 CLI 실행 파일 발견 시 즉시 중단 검증."""

        request = translate.TranslationRequest(
            source="Changed source.\n",
            existing_translation=None,
        )
        cfg = config.Config(
            provider="cli",
            values={
                "TRANSLATION_CLI_COMMAND": "/invalid/codex exec",
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                **CLI_AUTH_ENV,
                **REQUEST_BUDGET_ENV,
            },
        )

        with patch.object(
            translate,
            "run_process_tree",
            side_effect=OSError(errno.ENOEXEC, "Exec format error"),
        ) as run:
            with self.assertRaisesRegex(
                translate.IncompleteTranslation,
                "provider request failed",
            ):
                translate.translate_request(
                    request,
                    cfg,
                    "prompt",
                    deadline=1000.0,
                    clock=lambda: 0.0,
                )

        self.assertEqual(run.call_count, 1)


    def test_sdk_transports_use_request_budget_timeout(self):
        """OpenAI API 전송의 요청 예산 시간 제한 사용 검증."""

        openai_config = config.Config(
            provider="openai",
            values={
                "TRANSLATION_MODEL": "gpt-5.6-luna",
                "OPENAI_API_KEY": "key",
                **REQUEST_BUDGET_ENV,
                "TRANSLATION_REQUEST_TIMEOUT_SECONDS": "17",
            },
        )
        with patch("openai.OpenAI") as openai_client:
            openai_client.return_value.responses.create.return_value = SimpleNamespace(
                status="completed",
                output_text="translated",
            )
            translate._translate_openai("source", openai_config, "prompt")

        openai_client.assert_called_once_with(
            api_key="key",
            base_url=translate.OPENAI_API_BASE_URL,
            organization="",
            project="",
            max_retries=0,
            timeout=17,
        )
        self.assertEqual(
            openai_client.return_value.responses.create.call_args.kwargs[
                "max_output_tokens"
            ],
            200,
        )

    def test_cli_request_returns_only_the_last_agent_message(self):
        """CLI 요청의 마지막 에이전트 메시지만 반환 검증."""

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
                **CLI_AUTH_ENV,
                **REQUEST_BUDGET_ENV,
            },
        )

        calls = []

        def run(command, **kwargs):
            """마지막 에이전트 메시지 파일을 작성하고 완료된 프로세스 반환."""

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
            "UNRELATED_SECRET": "must-not-leak",
        }
        with patch.dict("os.environ", parent_environment, clear=True), patch.object(
            translate,
            "run_process_tree",
            side_effect=run,
        ):
            out = translate.translate_request(
                request,
                cfg,
                "prompt",
                deadline=1000.0,
                clock=lambda: 0.0,
            )

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
        child_environment = kwargs["env"]
        child_home = Path(child_environment["HOME"])
        self.assertEqual(child_home, Path(kwargs["cwd"]) / "home")
        self.assertEqual(child_environment["USERPROFILE"], str(child_home))
        self.assertEqual(
            child_environment["CODEX_HOME"],
            str(child_home / ".codex"),
        )
        self.assertEqual(
            child_environment["XDG_CONFIG_HOME"],
            str(child_home / ".config"),
        )
        self.assertEqual(
            child_environment["XDG_CACHE_HOME"],
            str(child_home / ".cache"),
        )
        self.assertEqual(
            child_environment["CODEX_ACCESS_TOKEN"],
            "test-codex-token",
        )
        self.assertEqual(child_environment["PATH"], "/usr/bin")
        self.assertEqual(
            child_environment["HTTPS_PROXY"],
            "https://proxy.example",
        )
        self.assertEqual(child_environment["LANG"], "ko_KR.UTF-8")
        self.assertNotIn("OPENAI_API_KEY", child_environment)
        self.assertNotIn("UNRELATED_SECRET", child_environment)
        self.assertEqual(kwargs["timeout"], 60)

if __name__ == "__main__":
    unittest.main()
