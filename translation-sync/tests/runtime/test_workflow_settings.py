"""버전 관리되는 워크플로 설정의 형식 계약 검증."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from sync.runtime.settings import SettingsError, load_workflow_settings


def _valid_settings() -> dict[str, object]:
    """테스트용 최소 유효 워크플로 설정 생성.

    Returns:
        필수 필드를 모두 포함한 유효한 설정 문서.
    """

    return {
        "schema_version": 1,
        "workflow_timeout_seconds": 3600,
        "unit_test_command": ["uv", "run", "python", "-m", "unittest"],
        "replay_command": ["uv", "run", "python", "replay.py"],
        "provider_fixture_command": ["uv", "run", "python", "provider_check.py"],
        "candidate_setup_commands": [["npm", "ci"]],
        "sync_core_command": ["uv", "run", "python", "main.py"],
        "site_validation_commands": [
            ["npm", "run", "test:markdown-links"],
            ["npm", "run", "build"],
        ],
        "path_validation_command": [
            "uv",
            "run",
            "python",
            "validate_generated_changes.py",
        ],
        "deploy_workflow": "deploy.yml",
    }


class WorkflowSettingsTests(unittest.TestCase):
    """워크플로 JSON 설정의 로딩과 거부 경계 검증."""

    def _write(self, root: Path, value: object) -> Path:
        """임시 workflow.json 기록.

        Args:
            root: 설정 파일을 기록할 임시 디렉터리.
            value: JSON으로 직렬화할 설정 문서.

        Returns:
            기록을 마친 설정 파일 경로.
        """

        path = root / "workflow.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_loads_commands_as_immutable_argv(self) -> None:
        """명령 배열의 불변 argv 로딩."""

        with tempfile.TemporaryDirectory() as tmp:
            settings = load_workflow_settings(
                self._write(Path(tmp), _valid_settings())
            )

        self.assertEqual(settings.workflow_timeout_seconds, 3600)
        self.assertEqual(settings.unit_test_command[0], "uv")
        self.assertIsInstance(settings.unit_test_command, tuple)
        self.assertEqual(settings.candidate_setup_commands, (("npm", "ci"),))
        self.assertEqual(len(settings.site_validation_commands), 2)
        self.assertEqual(settings.deploy_workflow, "deploy.yml")

    def test_rejects_missing_or_empty_required_command(self) -> None:
        """필수 명령 누락과 빈 배열 거부."""

        for key, value in (
            ("unit_test_command", None),
            ("candidate_setup_commands", []),
            ("sync_core_command", []),
            ("site_validation_commands", []),
        ):
            with self.subTest(key=key), tempfile.TemporaryDirectory() as tmp:
                document = _valid_settings()
                if value is None:
                    document.pop(key)
                else:
                    document[key] = value
                path = self._write(Path(tmp), document)

                with self.assertRaisesRegex(SettingsError, key):
                    load_workflow_settings(path)

    def test_rejects_invalid_candidate_setup_argv(self) -> None:
        """candidate 준비 명령의 잘못된 argv 거부."""

        with tempfile.TemporaryDirectory() as tmp:
            document = _valid_settings()
            document["candidate_setup_commands"] = [["npm", ""]]
            path = self._write(Path(tmp), document)

            with self.assertRaisesRegex(
                SettingsError,
                r"candidate_setup_commands\[0\]",
            ):
                load_workflow_settings(path)

    def test_rejects_shell_like_or_non_string_argv(self) -> None:
        """shell 문자열과 문자열이 아닌 argv 요소 거부."""

        invalid_commands = (
            "uv run python main.py",
            ["uv", ""],
            ["uv", 3],
            ["uv", "run\0python"],
        )
        for command in invalid_commands:
            with self.subTest(command=command), tempfile.TemporaryDirectory() as tmp:
                document = _valid_settings()
                document["sync_core_command"] = command
                path = self._write(Path(tmp), document)

                with self.assertRaisesRegex(SettingsError, "sync_core_command"):
                    load_workflow_settings(path)

    def test_rejects_unknown_fields_and_nonpositive_timeout(self) -> None:
        """알 수 없는 필드와 양수가 아닌 timeout 거부."""

        cases = (
            {**_valid_settings(), "unexpected": True},
            {**_valid_settings(), "workflow_timeout_seconds": 0},
            {**_valid_settings(), "workflow_timeout_seconds": True},
        )
        for document in cases:
            with self.subTest(document=document), tempfile.TemporaryDirectory() as tmp:
                path = self._write(Path(tmp), document)
                with self.assertRaises(SettingsError):
                    load_workflow_settings(path)

    def test_rejects_unsafe_deploy_workflow_name(self) -> None:
        """안전한 basename이 아닌 배포 workflow 이름 거부."""

        for name in ("../deploy.yml", "/deploy.yml", "deploy.yaml", "a/b.yml"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                document = _valid_settings()
                document["deploy_workflow"] = name
                path = self._write(Path(tmp), document)

                with self.assertRaisesRegex(SettingsError, "deploy_workflow"):
                    load_workflow_settings(path)


if __name__ == "__main__":
    unittest.main()
