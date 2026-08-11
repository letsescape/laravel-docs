"""버전 관리되는 번역 워크플로 argv 설정의 로딩 및 검증.

JSON 문서의 명령 배열을 shell 해석 없는 불변 argv와 공통 실행 설정으로 변환.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class SettingsError(ValueError):
    """워크플로 설정 형식 또는 값의 계약 위반 오류."""

    pass


@dataclass(frozen=True, slots=True)
class WorkflowSettings:
    """검증을 마친 워크플로 명령과 공통 timeout 설정.

    Attributes:
        workflow_timeout_seconds: 워크플로 전체에 허용할 실행 시간.
        unit_test_command: Python 단위 테스트 명령.
        replay_command: 결정론적 replay 검증 명령.
        provider_fixture_command: 번역 provider fixture 검증 명령.
        candidate_setup_commands: 검증 후보 작업공간 준비 명령 목록.
        sync_core_command: 번역 동기화 핵심 명령.
        site_validation_commands: 사이트 산출물 검증 명령 목록.
        path_validation_command: 생성된 변경 경로 검증 명령.
        deploy_workflow: 후속 배포에 사용할 GitHub Actions workflow 파일명.
    """

    workflow_timeout_seconds: int
    unit_test_command: tuple[str, ...]
    replay_command: tuple[str, ...]
    provider_fixture_command: tuple[str, ...]
    candidate_setup_commands: tuple[tuple[str, ...], ...]
    sync_core_command: tuple[str, ...]
    site_validation_commands: tuple[tuple[str, ...], ...]
    path_validation_command: tuple[str, ...]
    deploy_workflow: str


_FIELDS = {
    "schema_version",
    "workflow_timeout_seconds",
    "unit_test_command",
    "replay_command",
    "provider_fixture_command",
    "candidate_setup_commands",
    "sync_core_command",
    "site_validation_commands",
    "path_validation_command",
    "deploy_workflow",
}
_WORKFLOW_NAME_RE = re.compile(r"^[A-Za-z0-9._-]+\.yml$")


def _argv(value: Any, *, field: str) -> tuple[str, ...]:
    """JSON 배열을 shell 해석 없는 불변 argv로 변환.

    Args:
        value: argv로 변환할 JSON 값.
        field: 오류 메시지에 사용할 설정 필드명.

    Returns:
        검증을 마친 불변 argv.

    Raises:
        SettingsError: 값이 비어 있거나 유효한 문자열 배열이 아닌 경우.
    """

    if not isinstance(value, list) or not value:
        raise SettingsError(f"{field} must be a non-empty argv array")
    if any(
        not isinstance(argument, str) or not argument or "\0" in argument
        for argument in value
    ):
        raise SettingsError(f"{field} contains an invalid argv value")
    return tuple(value)


def load_workflow_settings(path: Path) -> WorkflowSettings:
    """JSON 설정 파일에서 워크플로 설정 로딩 및 검증.

    Args:
        path: 읽을 워크플로 설정 파일 경로.

    Returns:
        검증을 마친 워크플로 설정.

    Raises:
        SettingsError: 파일을 읽을 수 없거나 설정 계약을 위반한 경우.
    """

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SettingsError("workflow settings cannot be read") from exc
    if not isinstance(value, dict):
        raise SettingsError("workflow settings must be a JSON object")
    unknown = set(value) - _FIELDS
    missing = _FIELDS - set(value)
    if unknown:
        raise SettingsError(f"unknown workflow settings: {sorted(unknown)!r}")
    if missing:
        raise SettingsError(f"missing workflow settings: {sorted(missing)!r}")
    if value["schema_version"] != 1 or isinstance(value["schema_version"], bool):
        raise SettingsError("schema_version must be integer 1")

    timeout = value["workflow_timeout_seconds"]
    if isinstance(timeout, bool) or not isinstance(timeout, int) or timeout <= 0:
        raise SettingsError("workflow_timeout_seconds must be a positive integer")

    setup_value = value["candidate_setup_commands"]
    if not isinstance(setup_value, list) or not setup_value:
        raise SettingsError("candidate_setup_commands must be a non-empty array")
    setup_commands = tuple(
        _argv(command, field=f"candidate_setup_commands[{index}]")
        for index, command in enumerate(setup_value)
    )

    site_value = value["site_validation_commands"]
    if not isinstance(site_value, list) or not site_value:
        raise SettingsError("site_validation_commands must be a non-empty array")
    site_commands = tuple(
        _argv(command, field=f"site_validation_commands[{index}]")
        for index, command in enumerate(site_value)
    )

    deploy_workflow = value["deploy_workflow"]
    if not isinstance(deploy_workflow, str) or not _WORKFLOW_NAME_RE.fullmatch(
        deploy_workflow
    ):
        raise SettingsError("deploy_workflow must be a basename ending in .yml")

    return WorkflowSettings(
        workflow_timeout_seconds=timeout,
        unit_test_command=_argv(
            value["unit_test_command"], field="unit_test_command"
        ),
        replay_command=_argv(value["replay_command"], field="replay_command"),
        provider_fixture_command=_argv(
            value["provider_fixture_command"], field="provider_fixture_command"
        ),
        candidate_setup_commands=setup_commands,
        sync_core_command=_argv(
            value["sync_core_command"], field="sync_core_command"
        ),
        site_validation_commands=site_commands,
        path_validation_command=_argv(
            value["path_validation_command"], field="path_validation_command"
        ),
        deploy_workflow=deploy_workflow,
    )
