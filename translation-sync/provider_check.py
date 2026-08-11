#!/usr/bin/env python3
"""실제 프로바이더를 호출하되 문서를 변경하지 않는 소규모 번역 계약 검사."""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path

from sync import config, prompt, response_contract, translate
from sync.runtime.failure import (
    ErrorClassification,
    ExitCode,
    FailureEvent,
    FailureReport,
    IssueCode,
    ProviderAttempts,
    classification_for,
    final_exit_code,
    write_failure_report_exact,
)

SYNC_ROOT = Path(__file__).resolve().parent
PROMPTS = {
    "ko": SYNC_ROOT / "prompt.md",
    "ja": SYNC_ROOT / "prompt_jp.md",
}
FIXTURE_VERSION = 1
RESPONSE_CONTRACT_VERSION = response_contract.RESPONSE_CONTRACT_VERSION
if not (
    FIXTURE_VERSION
    == RESPONSE_CONTRACT_VERSION
    == config.PROVIDER_BUDGET_PROFILE_VERSION
):
    raise RuntimeError(
        "fixture, response contract, and provider budget profile versions "
        "must be advanced together"
    )
FAILURE_REPORT_ENV = "TRANSLATION_FAILURE_REPORT"
RUN_ID_ENV = "TRANSLATION_RUN_ID"
_CONFIGURATION_FAILED_MESSAGE = "provider check configuration failed"
CHECK_SOURCE = (
    "<!-- fixture-source-comment -->\n\n"
    "Install the `Widget` package from [Package Index](/docs/master/packages) "
    "and verify that the command completes successfully before continuing.\n\n"
    "- Run `widget:init` once.\n"
)
CHECK_DIFF = (
    "+ <!-- fixture-source-comment -->\n"
    "+\n"
    "+ Install the `Widget` package from [Package Index](/docs/master/packages) "
    "and verify that the command completes successfully before continuing.\n"
    "+\n"
    "+ - Run `widget:init` once."
)


def evaluate_output(locale: str, translated: str) -> list[str]:
    """고정 테스트 입력 번역문의 공통 응답 계약 위반 목록 반환."""

    return response_contract.verify(
        translated,
        CHECK_SOURCE,
        locale=locale,
        contract_version=RESPONSE_CONTRACT_VERSION,
    )


def _locales(value: str) -> tuple[str, ...]:
    """CLI 로케일 선택값을 실행 순서로 변환."""

    return ("ko", "ja") if value == "all" else (value,)


def _config_issue_code(exc: config.ConfigError) -> IssueCode:
    """설정 예외의 안정적 문제 코드 반환."""

    return exc.issue_code


def _provider_issue_code(exc: translate.IncompleteTranslation) -> IssueCode:
    """미완료 번역 예외를 안정적 프로바이더 문제 코드로 분류."""

    if isinstance(exc, translate.RunDeadlineExceeded):
        return IssueCode.RUN_DEADLINE_EXCEEDED
    if isinstance(exc, translate.UnsupportedOversizeBlock):
        return IssueCode.UNSUPPORTED_OVERSIZE_BLOCK
    if isinstance(exc, translate.ProviderTransientExhausted):
        return IssueCode.PROVIDER_TRANSIENT_EXHAUSTED
    if isinstance(exc, translate.CliProviderFailed):
        return IssueCode.CLI_PROVIDER_FAILED
    if isinstance(exc, translate.ProviderPartialResponse):
        return IssueCode.PROVIDER_PARTIAL_RESPONSE
    return IssueCode.PROVIDER_REQUEST_REJECTED


def _failure_event(
    code: IssueCode,
    *,
    message: str,
    locale: str | None = None,
    response_evaluation: int = 0,
    transport: int = 0,
) -> FailureEvent:
    """프로바이더 테스트 실패와 시도 횟수를 보고서 이벤트로 구성."""

    attempts = (
        ProviderAttempts(
            response_evaluation=response_evaluation,
            transport=transport,
        )
        if classification_for(code) is ErrorClassification.TRANSLATION
        else None
    )
    return FailureEvent(
        code=code,
        stage="provider-fixture",
        message=message,
        locale=locale,
        attempts=attempts,
    )


def _required_run_id() -> str:
    """환경 변수에서 안전한 필수 실행 식별자 검증·로드."""

    run_id = os.environ.get(RUN_ID_ENV, "")
    if (
        not run_id
        or len(run_id) > 128
        or not run_id[0].isalnum()
        or any(
            not (character.isalnum() or character in "._-")
            for character in run_id
        )
    ):
        raise ValueError("invalid provider fixture run id")
    return run_id


def _required_failure_report_target() -> Path:
    """저장소 외부에 새로 만들 실패 보고서 경로 검증."""

    value = os.environ.get(FAILURE_REPORT_ENV)
    if not value:
        raise ValueError("provider fixture failure report path is missing")
    requested = Path(value)
    if (
        not requested.is_absolute()
        or requested.exists()
        or requested.is_symlink()
        or not requested.parent.is_dir()
    ):
        raise ValueError("provider fixture failure report path is unsafe")
    target = requested.resolve(strict=False)
    if target.is_relative_to(SYNC_ROOT.parent.resolve()):
        raise ValueError("provider fixture failure report path must be external")
    return target


def _write_failure_report(
    failures: list[FailureEvent],
    *,
    run_id: str,
    target: Path,
) -> bool:
    """실패 이벤트를 정규 보고서로 새 파일에 기록하고 성공 여부 반환."""

    try:
        report = FailureReport.build(
            run_id=run_id,
            failures=failures,
        )
    except (TypeError, ValueError):
        print(
            "REPORT_WRITE_FAILED: provider fixture failure report could not be written",
            file=sys.stderr,
        )
        return False
    return write_failure_report_exact(report, target=target) is not None


def _finish_failure(
    event: FailureEvent,
    diagnostic: str,
    *,
    run_id: str,
    report_target: Path,
) -> int:
    """진단과 실패 보고서를 기록하고 공통 종료 코드 반환."""

    print(diagnostic, file=sys.stderr)
    if not _write_failure_report(
        [event],
        run_id=run_id,
        target=report_target,
    ):
        return int(ExitCode.INFRASTRUCTURE_FAILURE)
    return int(final_exit_code((event,)))


def _evaluate_fixture_attempt(
    *,
    locale: str,
    cfg: config.Config,
    locale_prompt: str,
    run_deadline: float | None,
    feedback: str | None,
    response_evaluation: int,
    attempt_counter: translate.ProviderAttemptCounter,
    run_id: str,
    report_target: Path,
) -> tuple[list[str], int | None]:
    """고정 fixture 번역을 요청·평가하고 실패를 종료 코드로 변환.

    Args:
        locale: 검사할 로케일.
        cfg: 검증된 프로바이더 설정.
        locale_prompt: 로케일 번역 프롬프트.
        run_deadline: 전체 실행 기한.
        feedback: 직전 응답 계약 위반 피드백.
        response_evaluation: 지금까지 평가한 응답 수.
        attempt_counter: 프로바이더 전송 시도 횟수 기록기.
        run_id: 실패 보고서 실행 식별자.
        report_target: 실패 보고서 출력 경로.

    Returns:
        응답 계약 위반 목록과 실패 종료 코드. 성공 시 종료 코드는 ``None``.
    """

    request = translate.TranslationRequest(
        source=CHECK_SOURCE,
        existing_translation=None,
        diff_text=CHECK_DIFF,
        verification_feedback=feedback,
        response_contract_version=RESPONSE_CONTRACT_VERSION,
    )
    completed_response = False
    try:
        translated = translate.translate_request(
            request,
            cfg,
            locale_prompt,
            deadline=run_deadline,
            attempt_counter=attempt_counter,
        )
        completed_response = True
        issues = evaluate_output(locale, translated)
        translate.require_run_deadline(run_deadline)
        return issues, None
    except config.ConfigError as exc:
        code = _config_issue_code(exc)
        message = "provider fixture request configuration is invalid"
        diagnostic = f"{locale} provider check failed: request configuration is invalid"
    except translate.IncompleteTranslation as exc:
        code = _provider_issue_code(exc)
        message = "provider fixture request did not complete"
        diagnostic = f"{locale} provider check failed: provider request did not complete"
    except Exception:
        code = IssueCode.UNCLASSIFIED_INTERNAL
        message = "provider fixture encountered an internal error"
        diagnostic = f"{locale} provider check failed: unexpected provider check error"
    return [], _finish_failure(
        _failure_event(
            code,
            message=message,
            locale=locale,
            response_evaluation=(
                response_evaluation + int(completed_response)
            ),
            transport=attempt_counter.transport,
        ),
        diagnostic,
        run_id=run_id,
        report_target=report_target,
    )


def _check_locale(
    locale: str,
    *,
    cfg: config.Config,
    run_deadline: float | None,
    model_profile: str,
    config_sha256: str,
    run_id: str,
    report_target: Path,
) -> int | None:
    """단일 로케일 fixture가 응답 계약을 충족할 때까지 검사.

    Args:
        locale: 검사할 로케일.
        cfg: 검증된 프로바이더 설정.
        run_deadline: 전체 실행 기한.
        model_profile: 로그에 기록할 모델 프로필.
        config_sha256: 로그에 기록할 설정 digest.
        run_id: 실패 보고서 실행 식별자.
        report_target: 실패 보고서 출력 경로.

    Returns:
        실패 종료 코드. 성공 시 ``None``.
    """

    try:
        locale_prompt = prompt.load_prompt(PROMPTS[locale])
    except (prompt.PromptError, OSError):
        return _finish_failure(
            _failure_event(
                IssueCode.REQUIRED_CONFIG_MISSING,
                message="provider fixture prompt is unavailable",
                locale=locale,
            ),
            _CONFIGURATION_FAILED_MESSAGE,
            run_id=run_id,
            report_target=report_target,
        )
    prompt_hash = hashlib.sha256(
        translate.effective_prompt(locale_prompt).encode()
    ).hexdigest()
    feedback: str | None = None
    issues: list[str] = []
    response_evaluation = 0
    attempt_counter = translate.ProviderAttemptCounter()
    for _attempt in range(translate.MAX_COMPLETED_RESPONSE_ATTEMPTS):
        issues, failure_code = _evaluate_fixture_attempt(
            locale=locale,
            cfg=cfg,
            locale_prompt=locale_prompt,
            run_deadline=run_deadline,
            feedback=feedback,
            response_evaluation=response_evaluation,
            attempt_counter=attempt_counter,
            run_id=run_id,
            report_target=report_target,
        )
        if failure_code is not None:
            return failure_code
        response_evaluation += 1
        if not issues:
            _print_success(
                locale=locale,
                cfg=cfg,
                model_profile=model_profile,
                prompt_hash=prompt_hash,
                config_sha256=config_sha256,
            )
            return None
        feedback = translate.verification_feedback(issues)
    return _finish_failure(
        _failure_event(
            IssueCode.FIXTURE_CONTRACT_FAILED,
            message=(
                "provider fixture response contract failed "
                f"with {len(issues)} violations"
            ),
            locale=locale,
            response_evaluation=response_evaluation,
            transport=attempt_counter.transport,
        ),
        f"{locale} provider check failed: response contract violations={len(issues)}",
        run_id=run_id,
        report_target=report_target,
    )


def _print_success(
    *,
    locale: str,
    cfg: config.Config,
    model_profile: str,
    prompt_hash: str,
    config_sha256: str,
) -> None:
    """성공한 fixture 검사 프로필을 단일 로그 줄로 출력.

    Args:
        locale: 검사한 로케일.
        cfg: 사용한 프로바이더 설정.
        model_profile: 모델 프로필.
        prompt_hash: 유효 프롬프트 digest.
        config_sha256: 프로바이더 설정 digest.
    """

    print(
        f"provider={cfg.provider} model={cfg.get('TRANSLATION_MODEL')} "
        f"model_profile={model_profile} "
        f"reasoning={cfg.get('TRANSLATION_REASONING_EFFORT', 'medium')} "
        f"locale={locale} prompt_sha256={prompt_hash} "
        f"fixture_version={FIXTURE_VERSION} "
        f"response_contract_version={RESPONSE_CONTRACT_VERSION} "
        "budget_profile_version="
        f"{config.PROVIDER_BUDGET_PROFILE_VERSION} "
        f"config_sha256={config_sha256} status=passed",
        flush=True,
    )


def main() -> int:
    """선택한 로케일별 실제 프로바이더 계약 검사 실행."""

    parser = argparse.ArgumentParser(
        description="Call the configured live provider with a fixed translation fixture."
    )
    parser.add_argument("--locale", choices=("all", "ko", "ja"), default="all")
    args = parser.parse_args()

    try:
        run_id = _required_run_id()
    except ValueError:
        print(_CONFIGURATION_FAILED_MESSAGE, file=sys.stderr)
        return 1
    try:
        report_target = _required_failure_report_target()
    except ValueError:
        print(
            "REPORT_WRITE_FAILED: provider fixture failure report path is invalid",
            file=sys.stderr,
        )
        return int(ExitCode.INFRASTRUCTURE_FAILURE)

    try:
        cfg = config.load_config()
        run_deadline = config.required_run_deadline(cfg)
        model_profile = config.provider_model_profile(cfg)
        config_sha256 = config.provider_config_sha256(cfg)
    except config.ConfigError as exc:
        return _finish_failure(
            _failure_event(
                _config_issue_code(exc),
                message="provider fixture configuration is invalid",
            ),
            _CONFIGURATION_FAILED_MESSAGE,
            run_id=run_id,
            report_target=report_target,
        )

    for locale in _locales(args.locale):
        failure_code = _check_locale(
            locale,
            cfg=cfg,
            run_deadline=run_deadline,
            model_profile=model_profile,
            config_sha256=config_sha256,
            run_id=run_id,
            report_target=report_target,
        )
        if failure_code is not None:
            return failure_code

    if report_target.exists() or report_target.is_symlink():
        print(
            "REPORT_WRITE_FAILED: provider fixture failure report path changed",
            file=sys.stderr,
        )
        return int(ExitCode.INFRASTRUCTURE_FAILURE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
