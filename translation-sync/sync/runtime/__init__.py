"""번역 워크플로의 실행 설정, 기한 및 실패 계약."""

from .failure import (
    ErrorClassification,
    ExitCode,
    FailureEvent,
    FailureReport,
    IssueCode,
    ProviderAttempts,
    classification_for,
    exit_code_for,
    final_exit_code,
    select_primary_failure,
)

__all__ = [
    "ErrorClassification",
    "ExitCode",
    "FailureEvent",
    "FailureReport",
    "IssueCode",
    "ProviderAttempts",
    "classification_for",
    "exit_code_for",
    "final_exit_code",
    "select_primary_failure",
]
