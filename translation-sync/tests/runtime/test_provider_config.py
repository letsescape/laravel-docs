"""번역 제공자 설정과 요청 예산 검증."""

import unittest
from unittest import mock

from sync.runtime import config
from sync.runtime.failure import IssueCode


REQUEST_BUDGET_ENV = {
    "TRANSLATION_CONTEXT_WINDOW_TOKENS": "200000",
    "TRANSLATION_RESERVED_OUTPUT_TOKENS": "200",
    "TRANSLATION_REQUEST_TIMEOUT_SECONDS": "60",
    "TRANSLATION_RUN_TIMEOUT_SECONDS": "600",
    "TRANSLATION_WORKFLOW_TIMEOUT_SECONDS": "900",
    "TRANSLATION_TOKENIZER_ENCODING": "o200k_base",
}


def openai_environment() -> dict[str, str]:
    """검증 가능한 OpenAI 테스트 환경."""

    return {
        "TRANSLATION_PROVIDER": "openai",
        "TRANSLATION_MODEL": "gpt-5.6-luna",
        "OPENAI_API_KEY": "test-openai-key",
        **REQUEST_BUDGET_ENV,
    }


def cli_environment() -> dict[str, str]:
    """검증 가능한 CLI 테스트 환경."""

    return {
        "TRANSLATION_PROVIDER": "cli",
        "TRANSLATION_CLI_COMMAND": "codex exec",
        "TRANSLATION_MODEL": "gpt-5.6-luna",
        "CODEX_ACCESS_TOKEN": "test-codex-token",
        **REQUEST_BUDGET_ENV,
    }


class ProviderSelectionTests(unittest.TestCase):
    """번역 제공자 선택과 필수 인증 설정 검증."""

    def test_reports_stable_codes_for_provider_and_credential_errors(self):
        """잘못된 제공자와 누락된 인증 정보의 안정적 오류 코드 검증."""

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
                    "TRANSLATION_MODEL": "gpt-5.6-luna",
                }
            )
        self.assertEqual(
            missing_credential.exception.issue_code,
            IssueCode.PROVIDER_CREDENTIAL_MISSING,
        )

    def test_limits_identity_provider_to_replay(self):
        """``identity`` 제공자의 재실행 외 사용 거부 검증."""

        with self.assertRaises(config.ConfigError) as raised:
            config.load_config({"TRANSLATION_PROVIDER": "identity"})
        self.assertEqual(
            raised.exception.issue_code,
            IssueCode.REPLAY_PROVIDER_FORBIDDEN,
        )

        loaded = config.load_config(
            {
                "TRANSLATION_PROVIDER": "identity",
                "TRANSLATION_REPLAY": "1",
            }
        )
        self.assertEqual(loaded.provider, "identity")
        self.assertIsNone(loaded.request_budget())

    def test_seals_a_copy_of_validated_values(self):
        """원본 매핑 변경과 직접 수정에서 설정값 보호 검증."""

        values = {"TRANSLATION_MODEL": "gpt-5.6-luna"}
        loaded = config.Config(provider="identity", values=values)

        values["TRANSLATION_MODEL"] = "changed"

        self.assertEqual(loaded.get("TRANSLATION_MODEL"), "gpt-5.6-luna")
        with self.assertRaises(TypeError):
            loaded.values["TRANSLATION_MODEL"] = "changed"  # type: ignore[index]


class RequestBudgetTests(unittest.TestCase):
    """토크나이저·토큰·제한 시간 예산 제약 검증."""

    def test_requires_budget_without_approved_profile_defaults(self):
        """승인 profile이 없는 모델의 불완전한 요청 예산 거부 검증."""

        environment = cli_environment()
        environment["TRANSLATION_MODEL"] = "unverified-model"
        del environment["TRANSLATION_CONTEXT_WINDOW_TOKENS"]

        with self.assertRaisesRegex(
            config.ConfigError,
            "INVALID_REQUEST_BUDGET.*TRANSLATION_CONTEXT_WINDOW_TOKENS",
        ):
            config.load_config(environment)

    def test_defaults_budget_from_approved_model_profile(self):
        """미설정 예산을 승인 profile 파생 기본값으로 채우는지 검증."""

        environment = openai_environment()
        for key in REQUEST_BUDGET_ENV:
            del environment[key]

        loaded = config.load_config(environment)
        budget = loaded.request_budget()

        self.assertIsNotNone(budget)
        assert budget is not None
        self.assertEqual(budget.context_window_tokens, 1_050_000)
        self.assertEqual(budget.reserved_output_tokens, 128_000)
        self.assertEqual(budget.request_timeout_seconds, 600)
        self.assertEqual(budget.run_timeout_seconds, 1800)
        self.assertEqual(budget.workflow_timeout_seconds, 7200)
        self.assertEqual(budget.tokenizer_encoding, "o200k_base")
        self.assertEqual(
            loaded.get("TRANSLATION_CONTEXT_WINDOW_TOKENS"), "1050000"
        )

    def test_environment_budget_overrides_profile_defaults(self):
        """명시된 env 예산 값이 profile 기본값보다 우선하는지 검증."""

        environment = openai_environment()
        for key in REQUEST_BUDGET_ENV:
            del environment[key]
        environment["TRANSLATION_CONTEXT_WINDOW_TOKENS"] = "500000"

        budget = config.load_config(environment).request_budget()

        self.assertIsNotNone(budget)
        assert budget is not None
        self.assertEqual(budget.context_window_tokens, 500_000)
        self.assertEqual(budget.reserved_output_tokens, 128_000)
        self.assertEqual(budget.tokenizer_encoding, "o200k_base")

    def test_exposes_reserved_output_and_maximum_input(self):
        """검증된 예산에서 최대 입력 토큰 수 계산 검증."""

        budget = config.load_config(openai_environment()).request_budget()

        self.assertIsNotNone(budget)
        assert budget is not None
        self.assertEqual(budget.reserved_output_tokens, 200)
        self.assertEqual(budget.max_input_tokens, 199800)

    def test_binds_budget_to_approved_model_metadata(self):
        """승인되지 않은 모델·토크나이저·상한 조합 거부 검증."""

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
                    config.load_config({**openai_environment(), **override})
                self.assertEqual(raised.exception.issue_code, issue_code)

    def test_requires_azure_deployment_model_profile(self):
        """Azure 배포 이름과 승인 모델 프로필의 명시적 연결 검증."""

        environment = {
            "TRANSLATION_PROVIDER": "azure",
            "TRANSLATION_MODEL": "deployment-name",
            "AZURE_OPENAI_API_KEY": "test-azure-key",
            "AZURE_OPENAI_API_VERSION": "2026-01-01",
            "AZURE_OPENAI_ENDPOINT": "https://azure.example.test",
            **REQUEST_BUDGET_ENV,
        }
        with self.assertRaises(config.ConfigError) as missing_profile:
            config.load_config(environment)
        self.assertEqual(
            missing_profile.exception.issue_code,
            IssueCode.TOKENIZER_METADATA_UNAVAILABLE,
        )

        loaded = config.load_config(
            {**environment, "TRANSLATION_MODEL_PROFILE": "gpt-5.6-luna"}
        )
        self.assertEqual(loaded.get("TRANSLATION_MODEL"), "deployment-name")
        self.assertEqual(
            loaded.get("TRANSLATION_MODEL_PROFILE"),
            "gpt-5.6-luna",
        )

    def test_rejects_invalid_budget_relationships(self):
        """0 이하 값과 역전된 토큰·제한 시간 관계 거부 검증."""

        cases = (
            ("TRANSLATION_CONTEXT_WINDOW_TOKENS", "0"),
            ("TRANSLATION_RESERVED_OUTPUT_TOKENS", "0"),
            ("TRANSLATION_RESERVED_OUTPUT_TOKENS", "200000"),
            ("TRANSLATION_REQUEST_TIMEOUT_SECONDS", "601"),
            ("TRANSLATION_RUN_TIMEOUT_SECONDS", "901"),
        )

        for key, value in cases:
            with self.subTest(key=key, value=value):
                with self.assertRaisesRegex(
                    config.ConfigError,
                    "INVALID_REQUEST_BUDGET",
                ):
                    config.load_config({**cli_environment(), key: value})

    def test_rejects_unknown_tokenizer(self):
        """tiktoken에 없는 인코딩 이름 거부 검증."""

        with self.assertRaisesRegex(
            config.ConfigError,
            "TOKENIZER_METADATA_UNAVAILABLE.*not-a-tokenizer",
        ):
            config.load_config(
                {
                    **cli_environment(),
                    "TRANSLATION_TOKENIZER_ENCODING": "not-a-tokenizer",
                }
            )


class CliConfigurationTests(unittest.TestCase):
    """Codex CLI 명령과 인증 격리 설정 검증."""

    def test_requires_options_free_codex_exec_command(self):
        """옵션이나 래퍼가 포함된 CLI 명령 거부 검증."""

        for command in (
            "codex exec --full-auto",
            "python codex exec",
            "codex --profile exec",
        ):
            with self.subTest(command=command):
                with self.assertRaises(config.ConfigError) as raised:
                    config.load_config(
                        {
                            **cli_environment(),
                            "TRANSLATION_CLI_COMMAND": command,
                        }
                    )
                self.assertEqual(
                    raised.exception.issue_code,
                    IssueCode.INVALID_RUNTIME_OPTION,
                )

    def test_requires_exactly_one_explicit_authentication_mode(self):
        """누락되거나 중복된 CLI 인증 방식 거부 검증."""

        missing = cli_environment()
        del missing["CODEX_ACCESS_TOKEN"]
        with self.assertRaises(config.ConfigError) as missing_auth:
            config.load_config(missing)
        self.assertEqual(
            missing_auth.exception.issue_code,
            IssueCode.PROVIDER_CREDENTIAL_MISSING,
        )

        with self.assertRaises(config.ConfigError) as duplicate_auth:
            config.load_config(
                {
                    **cli_environment(),
                    "CODEX_API_KEY": "second-token",
                }
            )
        self.assertEqual(
            duplicate_auth.exception.issue_code,
            IssueCode.INVALID_RUNTIME_OPTION,
        )

    def test_accepts_each_documented_authentication_mode(self):
        """토큰 또는 절대 경로 ``CODEX_HOME`` 인증 방식 허용 검증."""

        for key, value in (
            ("CODEX_ACCESS_TOKEN", "test-access-token"),
            ("CODEX_API_KEY", "test-api-key"),
            ("CODEX_HOME", "/tmp/test-codex-home"),
        ):
            with self.subTest(key=key):
                environment = cli_environment()
                del environment["CODEX_ACCESS_TOKEN"]
                loaded = config.load_config({**environment, key: value})
                self.assertEqual(loaded.get(key), value)

    def test_rejects_relative_codex_home(self):
        """상대 경로 ``CODEX_HOME`` 거부 검증."""

        environment = cli_environment()
        del environment["CODEX_ACCESS_TOKEN"]

        with self.assertRaises(config.ConfigError) as raised:
            config.load_config(
                {**environment, "CODEX_HOME": "relative/codex-home"}
            )
        self.assertEqual(
            raised.exception.issue_code,
            IssueCode.INVALID_RUNTIME_OPTION,
        )

    def test_preserves_only_approved_runtime_options(self):
        """추론 수준과 CLI 제한 시간만 선택적 실행 설정으로 보존하는지 검증."""

        loaded = config.load_config(
            {
                **cli_environment(),
                "TRANSLATION_REASONING_EFFORT": "low",
                "TRANSLATION_CLI_TIMEOUT": "60",
                "TRANSLATION_RETRY_DELAY": "0",
            }
        )

        self.assertEqual(loaded.get("TRANSLATION_REASONING_EFFORT"), "low")
        self.assertEqual(loaded.get("TRANSLATION_CLI_TIMEOUT"), "60")
        self.assertEqual(loaded.get("TRANSLATION_RETRY_DELAY"), "")

    def test_rejects_nonpositive_cli_timeout(self):
        """정수가 아니거나 양수가 아닌 CLI 제한 시간 거부 검증."""

        for value in ("later", "0"):
            with self.subTest(value=value):
                with self.assertRaisesRegex(
                    config.ConfigError,
                    "TRANSLATION_CLI_TIMEOUT must be an integer > 0",
                ):
                    config.load_config(
                        {
                            **cli_environment(),
                            "TRANSLATION_CLI_TIMEOUT": value,
                        }
                    )


class ProviderEvidenceTests(unittest.TestCase):
    """제공자 설정 증거 해시와 실행 기한 검증."""

    def test_hash_excludes_credentials_and_binds_profile_versions(self):
        """해시의 인증값 제외와 모델·예산 프로필 변경 반영 검증."""

        first = config.load_config(openai_environment())
        second = config.load_config(
            {**openai_environment(), "OPENAI_API_KEY": "rotated-secret"}
        )
        digest = config.provider_config_sha256(first)

        self.assertEqual(len(digest), 64)
        self.assertEqual(digest, config.provider_config_sha256(second))
        self.assertNotIn("test-openai-key", digest)
        with mock.patch.object(
            config,
            "PROVIDER_BUDGET_PROFILE_VERSION",
            2,
        ):
            self.assertNotEqual(digest, config.provider_config_sha256(first))

    def test_hash_binds_cli_auth_mode_without_secret_location(self):
        """해시에서 CLI 인증 종류는 구분하고 ``CODEX_HOME`` 위치는 제외하는지 검증."""

        base = cli_environment()
        del base["CODEX_ACCESS_TOKEN"]
        first_home = config.load_config(
            {**base, "CODEX_HOME": "/private/first-codex-home"}
        )
        second_home = config.load_config(
            {**base, "CODEX_HOME": "/private/second-codex-home"}
        )
        token = config.load_config(
            {**base, "CODEX_ACCESS_TOKEN": "secret-token"}
        )

        self.assertEqual(
            config.provider_config_sha256(first_home),
            config.provider_config_sha256(second_home),
        )
        self.assertNotEqual(
            config.provider_config_sha256(first_home),
            config.provider_config_sha256(token),
        )

    def test_hash_binds_azure_endpoint_without_api_key(self):
        """해시의 Azure 엔드포인트 변경 반영과 API 키 교체 제외 검증."""

        base = {
            "TRANSLATION_PROVIDER": "azure",
            "TRANSLATION_MODEL": "deployment",
            "TRANSLATION_MODEL_PROFILE": "gpt-5.6-luna",
            "AZURE_OPENAI_API_VERSION": "2026-01-01",
            **REQUEST_BUDGET_ENV,
        }
        first = config.load_config(
            {
                **base,
                "AZURE_OPENAI_ENDPOINT": "https://first.openai.azure.com",
                "AZURE_OPENAI_API_KEY": "first-secret",
            }
        )
        rotated_key = config.load_config(
            {
                **base,
                "AZURE_OPENAI_ENDPOINT": "https://first.openai.azure.com",
                "AZURE_OPENAI_API_KEY": "second-secret",
            }
        )
        changed_endpoint = config.load_config(
            {
                **base,
                "AZURE_OPENAI_ENDPOINT": "https://second.openai.azure.com",
                "AZURE_OPENAI_API_KEY": "first-secret",
            }
        )

        self.assertEqual(
            config.provider_config_sha256(first),
            config.provider_config_sha256(rotated_key),
        )
        self.assertNotEqual(
            config.provider_config_sha256(first),
            config.provider_config_sha256(changed_endpoint),
        )

    def test_reads_one_shared_absolute_run_deadline(self):
        """상위 워크플로 기한 안의 유효한 절대 실행 기한 로드 검증."""

        loaded = config.load_config(cli_environment())

        deadline = config.required_run_deadline(
            loaded,
            {
                config.WORKFLOW_DEADLINE_ENV: "1000.0",
                config.RUN_DEADLINE_ENV: "700.0",
            },
            clock=lambda: 100.0,
        )

        self.assertEqual(deadline, 700.0)

    def test_rejects_missing_expired_or_reset_run_deadline(self):
        """누락·만료·상위 기한 초과 실행 기한 거부 검증."""

        loaded = config.load_config(cli_environment())
        cases = (
            {},
            {
                config.WORKFLOW_DEADLINE_ENV: "1000.0",
                config.RUN_DEADLINE_ENV: "99.0",
            },
            {
                config.WORKFLOW_DEADLINE_ENV: "800.0",
                config.RUN_DEADLINE_ENV: "900.0",
            },
            {
                config.WORKFLOW_DEADLINE_ENV: "1000.0",
                config.RUN_DEADLINE_ENV: "701.0",
            },
        )

        for environment in cases:
            with self.subTest(environment=environment):
                with self.assertRaises(config.ConfigError) as raised:
                    config.required_run_deadline(
                        loaded,
                        environment,
                        clock=lambda: 100.0,
                    )
                self.assertEqual(
                    raised.exception.issue_code,
                    IssueCode.INVALID_RUNTIME_OPTION,
                )


if __name__ == "__main__":
    unittest.main()
