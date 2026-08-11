"""공급자 검사의 동작과 경계 조건 검증."""

import hashlib
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import provider_check


class ProviderCheckTests(unittest.TestCase):
    """공급자 검사의 동작과 경계 조건 테스트 모음."""

    def setUp(self) -> None:
        """테스트 사전 상태 구성."""

        self.failure_directory = tempfile.TemporaryDirectory()
        self.failure_report = (
            Path(self.failure_directory.name) / "fixture-failure.json"
        )
        self.environment = patch.dict(
            os.environ,
            {
                provider_check.RUN_ID_ENV: "fixture-run-1",
                provider_check.FAILURE_REPORT_ENV: str(self.failure_report),
            },
            clear=True,
        )
        self.environment.start()

    def tearDown(self) -> None:
        """테스트 사후 상태 정리."""

        self.environment.stop()
        self.failure_directory.cleanup()

    @staticmethod
    def _valid_translation(locale: str = "ko") -> str:
        """응답 계약을 만족하는 로케일별 픽스처 번역문 반환."""

        body = {
            "ko": (
                "`Widget` 패키지를 [Package Index](/docs/master/packages)에서 "
                "설치하고, 계속하기 전에 명령이 성공적으로 완료되는지 "
                "확인합니다."
            ),
            "ja": (
                "[Package Index](/docs/master/packages) から `Widget` パッケージを"
                "インストールし、続行する前にコマンドが正常に完了することを"
                "確認します。"
            ),
        }[locale]
        list_body = {
            "ko": "- `widget:init`을 한 번 실행합니다.",
            "ja": "- `widget:init` を一度実行します。",
        }[locale]
        return (
            "<!-- fixture-source-comment -->\n\n"
            "<!-- Install the `Widget` package from [Package Index]"
            "(/docs/master/packages) and verify that the command completes "
            "successfully before continuing. -->\n"
            f"{body}\n\n"
            "<!-- - Run `widget:init` once. -->\n"
            f"{list_body}\n"
        )

    def test_fixture_version_one_uses_the_specified_source_bytes(self):
        """픽스처·응답 계약·예산 프로필 버전과 명세 원문 바이트 검증."""

        self.assertEqual(provider_check.FIXTURE_VERSION, 1)
        self.assertEqual(provider_check.RESPONSE_CONTRACT_VERSION, 1)
        self.assertEqual(
            provider_check.config.PROVIDER_BUDGET_PROFILE_VERSION,
            1,
        )
        self.assertEqual(
            provider_check.CHECK_SOURCE,
            "<!-- fixture-source-comment -->\n\n"
            "Install the `Widget` package from [Package Index]"
            "(/docs/master/packages) and verify that the command completes "
            "successfully before continuing.\n\n"
            "- Run `widget:init` once.\n",
        )

    def test_accepts_structurally_valid_korean_markdown(self):
        """구조와 언어 계약을 만족하는 한국어 Markdown 허용 검증."""

        translated = self._valid_translation()

        self.assertEqual(provider_check.evaluate_output("ko", translated), [])

    def test_rejects_cli_wrapper_text(self):
        """번역문 앞의 CLI 설명 문구 거부 검증."""

        translated = (
            "Here is the translation:\n\n"
            + self._valid_translation()
        )

        self.assertTrue(provider_check.evaluate_output("ko", translated))

    def test_accepts_structurally_valid_japanese_markdown(self):
        """구조와 언어 계약을 만족하는 일본어 Markdown 허용 검증."""

        translated = self._valid_translation("ja")

        self.assertEqual(provider_check.evaluate_output("ja", translated), [])

    def test_retries_a_completed_response_that_fails_the_contract(self):
        """계약을 위반한 완료 응답을 피드백과 함께 한 번 재시도하는지 검증."""

        cfg = provider_check.config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "test-model",
            },
        )
        invalid = self._valid_translation().replace("`widget:init`", "widget:init")
        valid = self._valid_translation()
        stdout = io.StringIO()

        with redirect_stdout(stdout), patch.object(
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
        self.assertNotIn(valid, stdout.getvalue())
        self.assertIn("fixture_version=1", stdout.getvalue())
        self.assertIn("response_contract_version=1", stdout.getvalue())
        self.assertIn("budget_profile_version=1", stdout.getvalue())
        self.assertRegex(stdout.getvalue(), r"config_sha256=[0-9a-f]{64}")
        self.assertIn("status=passed", stdout.getvalue())

    def test_passes_the_shared_run_deadline_to_every_fixture_request(self):
        """모든 픽스처 요청에 같은 실행 기한을 전달하는지 검증."""

        cfg = provider_check.config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "test-model",
            },
        )
        with patch.object(
            provider_check.sys,
            "argv",
            ["provider_check.py", "--locale", "ko"],
        ), patch.object(
            provider_check.config,
            "load_config",
            return_value=cfg,
        ), patch.object(
            provider_check.config,
            "required_run_deadline",
            return_value=1234.5,
        ), patch.object(
            provider_check.prompt,
            "load_prompt",
            return_value="prompt",
        ), patch.object(
            provider_check.translate,
            "translate_request",
            return_value=self._valid_translation(),
        ) as provider, patch.object(
            provider_check.translate,
            "require_run_deadline",
        ) as deadline_check:
            exit_code = provider_check.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(provider.call_count, 1)
        self.assertEqual(provider.call_args.kwargs["deadline"], 1234.5)
        deadline_check.assert_called_once_with(1234.5)

    def test_stops_after_two_invalid_completed_responses(self):
        """계약 위반 완료 응답을 두 번 받은 뒤 검사 중단 검증."""

        stderr = io.StringIO()
        cfg = provider_check.config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "test-model",
            },
        )
        invalid = self._valid_translation().replace("`widget:init`", "widget:init")

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
        self.assertRegex(
            stderr.getvalue(),
            r"^ko provider check failed: response contract violations=\d+\n$",
        )

    def test_common_contract_rejects_trailing_wrapper_text(self):
        """공통 계약이 번역문 뒤의 설명 문구를 거부하는지 검증."""

        translated = self._valid_translation() + "\nTranslation complete.\n"

        self.assertTrue(provider_check.evaluate_output("ko", translated))

    def test_common_contract_rejects_modified_source_authored_comment(self):
        """공통 계약이 변경된 원문 작성 주석을 거부하는지 검증."""

        translated = self._valid_translation().replace(
            "<!-- fixture-source-comment -->",
            "<!-- changed-source-comment -->",
        )

        self.assertIn(
            "provider source comment mismatch",
            provider_check.evaluate_output("ko", translated),
        )

    def test_common_contract_rejects_modified_inline_code(self):
        """공통 계약이 변경된 인라인 코드를 거부하는지 검증."""

        translated = self._valid_translation().replace(
            "`widget:init`", "`widget:changed`"
        )

        self.assertIn(
            "provider inline code mismatch",
            provider_check.evaluate_output("ko", translated),
        )

    def test_success_outputs_only_versioned_metadata(self):
        """성공 로그에 버전이 명시된 비민감 메타데이터만 남는지 검증."""

        stdout = io.StringIO()
        stderr = io.StringIO()
        cfg = provider_check.config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "test-model",
                "TRANSLATION_REASONING_EFFORT": "low",
            },
        )
        prompt_text = "prompt"
        prompt_hash = hashlib.sha256(
            provider_check.translate.effective_prompt(prompt_text).encode()
        ).hexdigest()
        config_hash = provider_check.config.provider_config_sha256(cfg)
        translated = self._valid_translation()

        with redirect_stdout(stdout), redirect_stderr(stderr), patch.object(
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
            return_value=prompt_text,
        ), patch.object(
            provider_check.translate,
            "translate_request",
            return_value=translated,
        ):
            exit_code = provider_check.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(
            stdout.getvalue(),
            "provider=cli model=test-model model_profile=test-model "
            "reasoning=low locale=ko "
            f"prompt_sha256={prompt_hash} fixture_version=1 "
            "response_contract_version=1 budget_profile_version=1 "
            f"config_sha256={config_hash} status=passed\n",
        )
        self.assertNotIn(translated, stdout.getvalue())

    def test_failure_never_outputs_provider_response_or_transport_detail(self):
        """실패 로그에서 공급자 응답과 전송 세부 정보가 숨겨지는지 검증."""

        response_marker = "PRIVATE_PROVIDER_RESPONSE_BODY"
        for side_effect in (
            self._valid_translation() + f"\n{response_marker}\n",
            provider_check.translate.IncompleteTranslation(response_marker),
            RuntimeError(response_marker),
        ):
            with self.subTest(side_effect=type(side_effect).__name__):
                if self.failure_report.exists():
                    self.failure_report.unlink()
                stdout = io.StringIO()
                stderr = io.StringIO()
                cfg = provider_check.config.Config(
                    provider="cli",
                    values={
                        "TRANSLATION_PROVIDER": "cli",
                        "TRANSLATION_MODEL": "test-model",
                    },
                )
                with redirect_stdout(stdout), redirect_stderr(stderr), patch.object(
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
                    side_effect=(
                        side_effect
                        if isinstance(side_effect, BaseException)
                        else None
                    ),
                    return_value=(
                        side_effect if isinstance(side_effect, str) else None
                    ),
                ):
                    exit_code = provider_check.main()

                self.assertEqual(
                    exit_code,
                    2 if isinstance(side_effect, RuntimeError) else 1,
                )
                self.assertNotIn(response_marker, stdout.getvalue())
                self.assertNotIn(response_marker, stderr.getvalue())

    def test_contract_failure_writes_canonical_report_with_exact_run_and_attempts(self):
        """계약 실패 보고서에 실행 ID와 정확한 시도 횟수가 기록되는지 검증."""

        cfg = provider_check.config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "test-model",
            },
        )
        invalid = self._valid_translation().replace("`widget:init`", "widget:init")

        def respond(*_args, attempt_counter, **_kwargs):
            """전송 시도 횟수를 기록하고 계약 위반 응답 반환."""

            attempt_counter.record_transport()
            return invalid

        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp) / "fixture-failure.json"
            with patch.dict(
                os.environ,
                {provider_check.FAILURE_REPORT_ENV: str(report_path)},
            ), patch.object(
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
                side_effect=respond,
            ):
                exit_code = provider_check.main()

            report_bytes = report_path.read_bytes()
            report = json.loads(report_bytes)

        self.assertEqual(exit_code, 1)
        self.assertEqual(report["run_id"], "fixture-run-1")
        self.assertEqual(report["code"], "FIXTURE_CONTRACT_FAILED")
        self.assertEqual(
            report["attempts"],
            {"response_evaluation": 2, "transport": 2},
        )
        self.assertTrue(report_bytes.endswith(b"\n"))
        self.assertNotIn(invalid.encode(), report_bytes)

    def test_transport_failure_report_uses_stable_code_without_exception_body(self):
        """전송 실패 보고서의 예외 본문 제외와 안정된 코드 사용 검증."""

        marker = "PRIVATE_PROVIDER_EXCEPTION_BODY"
        cfg = provider_check.config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "test-model",
            },
        )

        def fail(*_args, attempt_counter, **_kwargs):
            """테스트용 대체 동작."""

            for _ in range(3):
                attempt_counter.record_transport()
            raise provider_check.translate.ProviderTransientExhausted(marker)

        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp) / "fixture-failure.json"
            with patch.dict(
                os.environ,
                {provider_check.FAILURE_REPORT_ENV: str(report_path)},
            ), patch.object(
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
                return_value="prompt",
            ), patch.object(
                provider_check.translate,
                "translate_request",
                side_effect=fail,
            ):
                exit_code = provider_check.main()

            report_bytes = report_path.read_bytes()
            report = json.loads(report_bytes)

        self.assertEqual(exit_code, 1)
        self.assertEqual(report["code"], "PROVIDER_TRANSIENT_EXHAUSTED")
        self.assertEqual(
            report["attempts"],
            {"response_evaluation": 0, "transport": 3},
        )
        self.assertNotIn(marker.encode(), report_bytes)

    def test_run_deadline_failure_report_has_zero_unstarted_attempts(self):
        """호출 전 기한 초과 보고서의 시작되지 않은 시도 횟수가 0인지 검증."""

        cfg = provider_check.config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "test-model",
            },
        )
        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp) / "fixture-failure.json"
            with patch.dict(
                os.environ,
                {provider_check.FAILURE_REPORT_ENV: str(report_path)},
            ), patch.object(
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
                side_effect=provider_check.translate.RunDeadlineExceeded(
                    "PRIVATE_DEADLINE_DETAIL"
                ),
            ):
                exit_code = provider_check.main()

            report = json.loads(report_path.read_bytes())

        self.assertEqual(exit_code, 1)
        self.assertEqual(report["code"], "RUN_DEADLINE_EXCEEDED")
        self.assertEqual(
            report["attempts"],
            {"response_evaluation": 0, "transport": 0},
        )

    def test_configuration_failure_report_maps_code_without_config_detail(self):
        """설정 실패의 민감한 세부 정보 제외와 안정된 코드 매핑 검증."""

        marker = "PRIVATE_CONFIG_DETAIL"
        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp) / "fixture-failure.json"
            with patch.dict(
                os.environ,
                {provider_check.FAILURE_REPORT_ENV: str(report_path)},
            ), patch.object(
                provider_check.sys,
                "argv",
                ["provider_check.py", "--locale", "ko"],
            ), patch.object(
                provider_check.config,
                "load_config",
                side_effect=provider_check.config.ConfigError(
                    "missing env for provider 'openai': OPENAI_API_KEY, " + marker,
                    provider_check.IssueCode.PROVIDER_CREDENTIAL_MISSING,
                ),
            ):
                exit_code = provider_check.main()

            report_bytes = report_path.read_bytes()
            report = json.loads(report_bytes)

        self.assertEqual(exit_code, 1)
        self.assertEqual(report["code"], "PROVIDER_CREDENTIAL_MISSING")
        self.assertIsNone(report["attempts"])
        self.assertNotIn(marker.encode(), report_bytes)

    def test_failure_report_is_no_replace(self):
        """기존 실패 보고서를 교체하지 않는지 검증."""

        cfg = provider_check.config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "test-model",
            },
        )
        stderr = io.StringIO()
        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp) / "fixture-failure.json"
            report_path.write_bytes(b"existing-report\n")
            with redirect_stderr(stderr), patch.dict(
                os.environ,
                {provider_check.FAILURE_REPORT_ENV: str(report_path)},
            ), patch.object(
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
                side_effect=OSError("PRIVATE_PROMPT_ERROR"),
            ):
                exit_code = provider_check.main()

            self.assertEqual(report_path.read_bytes(), b"existing-report\n")

        self.assertEqual(exit_code, 2)
        self.assertIn("REPORT_WRITE_FAILED", stderr.getvalue())
        self.assertNotIn("PRIVATE_PROMPT_ERROR", stderr.getvalue())

    def test_missing_or_invalid_run_id_fails_before_provider_configuration(self):
        """누락되거나 잘못된 실행 ID가 공급자 설정보다 먼저 거부되는지 검증."""

        for run_id in (None, "-invalid", "x" * 129):
            with self.subTest(run_id=run_id):
                environment = {}
                if run_id is not None:
                    environment[provider_check.RUN_ID_ENV] = run_id
                with patch.dict(os.environ, environment, clear=True), patch.object(
                    provider_check.sys,
                    "argv",
                    ["provider_check.py", "--locale", "ko"],
                ), patch.object(
                    provider_check.config,
                    "load_config",
                    side_effect=AssertionError("configuration must not be read"),
                ):
                    exit_code = provider_check.main()

                self.assertEqual(exit_code, 1)

    def test_missing_failure_report_target_fails_before_provider_configuration(self):
        """누락된 실패 보고서 경로가 공급자 설정보다 먼저 거부되는지 검증."""

        with patch.dict(
            os.environ,
            {provider_check.RUN_ID_ENV: "fixture-run-1"},
            clear=True,
        ), patch.object(
            provider_check.sys,
            "argv",
            ["provider_check.py", "--locale", "ko"],
        ), patch.object(
            provider_check.config,
            "load_config",
            side_effect=AssertionError("configuration must not be read"),
        ):
            exit_code = provider_check.main()

        self.assertEqual(exit_code, 2)

    def test_success_fails_if_failure_report_target_appears_during_fixture(self):
        """픽스처 실행 중 실패 보고서 경로가 선점되면 성공을 거부하는지 검증."""

        cfg = provider_check.config.Config(
            provider="cli",
            values={
                "TRANSLATION_PROVIDER": "cli",
                "TRANSLATION_MODEL": "test-model",
            },
        )

        def respond(*_args, **_kwargs):
            """유효한 응답을 반환하기 전에 보고서 경로를 선점."""

            self.failure_report.write_bytes(b"raced-report\n")
            return self._valid_translation()

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
            side_effect=respond,
        ):
            exit_code = provider_check.main()

        self.assertEqual(exit_code, 2)
        self.assertEqual(self.failure_report.read_bytes(), b"raced-report\n")

    def test_prompt_error_is_reported_as_configuration_failure(self):
        """프롬프트 형식 오류가 설정 실패로 보고되는지 검증."""

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

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            stderr.getvalue(),
            "provider check configuration failed\n",
        )

    def test_prompt_read_failure_is_reported_as_configuration_failure(self):
        """프롬프트 읽기 오류가 설정 실패로 보고되는지 검증."""

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

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            stderr.getvalue(),
            "provider check configuration failed\n",
        )


if __name__ == "__main__":
    unittest.main()
