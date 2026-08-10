"""실행 실패 모델 동작과 경계 조건 검증."""

import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sync.runtime.failure import (
    REPORT_FILENAME,
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
    write_failure_report,
    write_failure_report_exact,
)


class FailureCodeTests(unittest.TestCase):
    """실패 코드 동작과 경계 조건 테스트 모음."""

    def test_every_stable_code_has_one_classification_and_exit_meaning(self) -> None:
        """모든 안정적 코드에 분류와 종료 의미가 하나씩 있는지 검증."""

        for code in IssueCode:
            with self.subTest(code=code):
                self.assertIsInstance(classification_for(code), ErrorClassification)
                self.assertIsInstance(exit_code_for(code), ExitCode)

        self.assertEqual(
            exit_code_for(IssueCode.NORMALIZED_NOOP),
            ExitCode.SUCCESS,
        )
        self.assertEqual(
            exit_code_for(IssueCode.SOURCE_STRUCTURE_MISMATCH),
            ExitCode.CONTROLLED_FAILURE,
        )
        self.assertEqual(
            exit_code_for(IssueCode.RUNNER_OPERATION_FAILED),
            ExitCode.INFRASTRUCTURE_FAILURE,
        )
        self.assertEqual(
            exit_code_for(IssueCode.ACTIVE_WORKTREE_MUTATED),
            ExitCode.ACTIVE_STATE_MUTATION,
        )

    def test_exit_priority_is_three_then_two_then_one(self) -> None:
        """종료 코드 우선순위가 3, 2, 1 순인지 검증."""

        failures = [
            FailureEvent(
                code=IssueCode.PROVIDER_SELECTION_INVALID,
                stage="config",
                message="provider is invalid",
            ),
            FailureEvent(
                code=IssueCode.RUNNER_OPERATION_FAILED,
                stage="runner",
                message="runner failed",
            ),
            FailureEvent(
                code=IssueCode.ACTIVE_WORKTREE_MUTATED,
                stage="cleanup",
                message="fingerprint changed",
            ),
            FailureEvent(
                code=IssueCode.ACTIVE_WORKTREE_MUTATED,
                stage="cleanup-second-check",
                message="fingerprint still changed",
            ),
        ]

        self.assertEqual(final_exit_code(failures), ExitCode.ACTIVE_STATE_MUTATION)
        self.assertIs(select_primary_failure(failures), failures[2])
        self.assertEqual(final_exit_code([]), ExitCode.SUCCESS)

    def test_non_failure_status_cannot_be_reported_as_a_failure(self) -> None:
        """실패가 아닌 상태를 실패로 보고할 수 없는지 검증."""

        with self.assertRaises(ValueError):
            FailureEvent(
                code=IssueCode.NORMALIZED_NOOP,
                stage="source",
                message="not an error",
            )

    def test_attempts_are_present_only_for_provider_failures(self) -> None:
        """제공자 실패에만 시도 횟수가 포함되는지 검증."""

        with self.assertRaises(ValueError):
            FailureEvent(
                code=IssueCode.CLI_PROVIDER_FAILED,
                stage="translation",
                message="provider failed",
            )
        with self.assertRaises(ValueError):
            FailureEvent(
                code=IssueCode.UNIT_TEST_FAILED,
                stage="unit-test",
                message="test failed",
                attempts=ProviderAttempts(response_evaluation=1, transport=1),
            )


class FailureReportTests(unittest.TestCase):
    """실패 보고서 생성과 기록의 경계 조건 테스트 모음."""

    def _events(self) -> list[FailureEvent]:
        """테스트용 실패 이벤트 구성."""

        return [
            FailureEvent(
                code=IssueCode.SOURCE_STRUCTURE_MISMATCH,
                stage="verification",
                message="heading order differs",
                version="12.x",
                locale="ko",
                document="documentation/12.x/ko/routing.md",
                plan_id="plan-2",
                structural_address="section:2/heading:1",
            ),
            FailureEvent(
                code=IssueCode.RUNNER_OPERATION_FAILED,
                stage="cleanup",
                message="cleanup failed",
            ),
        ]

    def test_report_uses_highest_exit_priority_for_top_level_fields(self) -> None:
        """보고서 최상위 필드에 가장 높은 종료 우선순위를 사용하는지 검증."""

        report = FailureReport.build(
            run_id="run-20260802-1",
            failures=self._events(),
            manifest_digest="a" * 64,
            base_head="b" * 40,
            candidate_debug_path="runs/run-20260802-1/candidate",
        )
        data = report.to_mapping()

        self.assertEqual(data["stage"], "cleanup")
        self.assertEqual(data["classification"], "X")
        self.assertEqual(data["code"], "RUNNER_OPERATION_FAILED")
        self.assertEqual(data["exit_code"], 2)
        self.assertIsNone(data["version"])
        self.assertEqual(
            [item["code"] for item in data["issues"]],
            ["RUNNER_OPERATION_FAILED", "SOURCE_STRUCTURE_MISMATCH"],
        )

    def test_canonical_bytes_are_recursive_sorted_compact_utf8_with_one_lf(
        self,
    ) -> None:
        """정규 바이트의 재귀 정렬·압축 UTF-8·단일 줄바꿈 형식 검증."""

        first, second = self._events()
        kwargs = {
            "run_id": "실행-1",
            "manifest_digest": "a" * 64,
            "base_head": "b" * 40,
        }
        report_a = FailureReport.build(failures=[first, second], **kwargs)
        report_b = FailureReport.build(failures=[second, first], **kwargs)

        # 인프라 문제의 우선순위가 유일하게 가장 높으므로 낮은 우선순위의 탐지 순서가 바뀌어도 정규 바이트는 바뀌지 않음.
        self.assertEqual(report_a.to_bytes(), report_b.to_bytes())
        self.assertTrue(report_a.to_bytes().endswith(b"\n"))
        self.assertFalse(report_a.to_bytes().endswith(b"\n\n"))
        self.assertNotIn(b": ", report_a.to_bytes())
        self.assertEqual(
            report_a.to_bytes(),
            (
                json.dumps(
                    report_a.to_mapping(),
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                + "\n"
            ).encode("utf-8"),
        )

    def test_messages_are_short_and_redact_secrets_bodies_and_absolute_paths(
        self,
    ) -> None:
        """메시지 길이 제한과 비밀·본문·절대 경로 가림 검증."""

        event = FailureEvent(
            code=IssueCode.CLI_PROVIDER_FAILED,
            stage="translation",
            message=(
                "Authorization: Bearer secret-token API_KEY=super-secret "
                "sk-live-secretvalue /Users/person/private/request.json\n"
                + "QUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVo="
                * 4
            ),
            attempts=ProviderAttempts(response_evaluation=1, transport=1),
        )
        report = FailureReport.build(run_id="run-1", failures=[event])
        payload = report.to_bytes().decode("utf-8")

        for secret in (
            "secret-token",
            "super-secret",
            "sk-live-secretvalue",
            "/Users/person",
            "QUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVo",
        ):
            self.assertNotIn(secret, payload)
        issue_message = report.to_mapping()["issues"][0]["message"]
        self.assertLessEqual(len(issue_message), 240)
        self.assertNotIn("\n", issue_message)

    def test_single_segment_absolute_path_is_redacted_but_docs_link_is_preserved(
        self,
    ) -> None:
        """단일 구간 절대 경로는 가리고 문서 링크는 보존하는지 검증."""

        event = FailureEvent(
            code=IssueCode.RUNNER_OPERATION_FAILED,
            stage="runner",
            message=("temporary root /tmp failed while checking /docs/master/routing"),
        )

        message = event.message

        self.assertNotIn("/tmp", message)
        self.assertIn("<redacted-path>", message)
        self.assertIn("/docs/master/routing", message)

    def test_context_paths_must_be_repository_or_artifact_relative(self) -> None:
        """문맥 경로가 저장소 또는 산출물 기준 상대 경로인지 검증."""

        for field, path in (
            ("document", "/Users/person/repo/file.md"),
            ("document", "../outside.md"),
            ("document", "documentation/./routing.md"),
            ("candidate_debug_path", "/tmp/candidate"),
            ("candidate_debug_path", "runs/../candidate"),
            ("candidate_debug_path", "runs//candidate"),
        ):
            with self.subTest(field=field, path=path):
                event_kwargs = {field: path} if field == "document" else {}
                event = FailureEvent(
                    code=IssueCode.SOURCE_STRUCTURE_MISMATCH,
                    stage="verification",
                    message="mismatch",
                    **event_kwargs,
                )
                report_kwargs = {field: path} if field == "candidate_debug_path" else {}
                with self.assertRaises(ValueError):
                    FailureReport.build(
                        run_id="run-1",
                        failures=[event],
                        **report_kwargs,
                    )

    def test_write_is_no_replace_and_uses_redacted_stderr_fallback(self) -> None:
        """보고서 기록의 무교체 동작과 가려진 표준 오류 대체 출력 검증."""

        report = FailureReport.build(
            run_id="run-1",
            failures=[
                FailureEvent(
                    code=IssueCode.RUNNER_OPERATION_FAILED,
                    stage="runner",
                    message="failed",
                )
            ],
        )
        with tempfile.TemporaryDirectory() as tmp:
            artifact_root = Path(tmp).resolve()
            stderr = io.StringIO()

            written = write_failure_report(
                report,
                artifact_root=artifact_root,
                stderr=stderr,
            )
            self.assertEqual(written, artifact_root / REPORT_FILENAME)
            self.assertEqual(written.read_bytes(), report.to_bytes())
            self.assertEqual(stderr.getvalue(), "")

            second = write_failure_report(
                report,
                artifact_root=artifact_root,
                stderr=stderr,
            )
            self.assertIsNone(second)
            self.assertEqual(
                stderr.getvalue(),
                "REPORT_WRITE_FAILED: failure report could not be written\n",
            )
            self.assertEqual(written.read_bytes(), report.to_bytes())

    def test_missing_artifact_root_does_not_get_created(self) -> None:
        """존재하지 않는 산출물 루트를 생성하지 않는지 검증."""

        report = FailureReport.build(
            run_id="run-1",
            failures=[
                FailureEvent(
                    code=IssueCode.RUNNER_OPERATION_FAILED,
                    stage="runner",
                    message="failed",
                )
            ],
        )
        with tempfile.TemporaryDirectory() as tmp:
            artifact_root = Path(tmp).resolve() / "missing"
            stderr = io.StringIO()

            self.assertIsNone(
                write_failure_report(
                    report,
                    artifact_root=artifact_root,
                    stderr=stderr,
                )
            )
            self.assertFalse(artifact_root.exists())
            self.assertEqual(
                stderr.getvalue(),
                "REPORT_WRITE_FAILED: failure report could not be written\n",
            )

    def test_exact_path_writer_is_no_replace_and_does_not_create_parent(self) -> None:
        """정확한 경로 기록기의 무교체 동작과 상위 디렉터리 미생성 검증."""

        report = FailureReport.build(
            run_id="run-1",
            failures=[
                FailureEvent(
                    code=IssueCode.RUNNER_OPERATION_FAILED,
                    stage="runner",
                    message="failed",
                )
            ],
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            target = root / "replay-failure.json"
            stderr = io.StringIO()

            self.assertEqual(
                write_failure_report_exact(
                    report,
                    target=target,
                    stderr=stderr,
                ),
                target,
            )
            self.assertEqual(target.read_bytes(), report.to_bytes())

            self.assertIsNone(
                write_failure_report_exact(
                    report,
                    target=target,
                    stderr=stderr,
                )
            )
            self.assertEqual(target.read_bytes(), report.to_bytes())

            missing_target = root / "missing" / "failure.json"
            self.assertIsNone(
                write_failure_report_exact(
                    report,
                    target=missing_target,
                    stderr=stderr,
                )
            )
            self.assertFalse(missing_target.parent.exists())
            self.assertEqual(
                stderr.getvalue(),
                "REPORT_WRITE_FAILED: failure report could not be written\n" * 2,
            )

    def test_exact_path_writer_rejects_symlink_and_non_directory_ancestors(
        self,
    ) -> None:
        """정확한 경로 기록기의 심볼릭 링크와 디렉터리가 아닌 상위 경로 거부 검증."""

        report = FailureReport.build(
            run_id="run-1",
            failures=[
                FailureEvent(
                    code=IssueCode.RUNNER_OPERATION_FAILED,
                    stage="runner",
                    message="failed",
                )
            ],
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            external = root / "external"
            external.mkdir()
            symlink = root / "linked"
            symlink.symlink_to(external, target_is_directory=True)
            regular = root / "regular"
            regular.write_text("keep\n", encoding="utf-8")
            linked_target = external / "existing.json"
            linked_target.write_text("keep target\n", encoding="utf-8")
            target_symlink = root / "failure-link.json"
            target_symlink.symlink_to(linked_target)

            for target in (
                symlink / "failure.json",
                regular / "failure.json",
                target_symlink,
            ):
                with self.subTest(target=target):
                    stderr = io.StringIO()
                    self.assertIsNone(
                        write_failure_report_exact(
                            report,
                            target=target,
                            stderr=stderr,
                        )
                    )
                    self.assertEqual(
                        stderr.getvalue(),
                        "REPORT_WRITE_FAILED: failure report could not be written\n",
                    )

            self.assertEqual(
                linked_target.read_text(encoding="utf-8"),
                "keep target\n",
            )
            self.assertTrue(target_symlink.is_symlink())
            self.assertEqual(list(external.iterdir()), [linked_target])
            self.assertEqual(regular.read_text(encoding="utf-8"), "keep\n")

    def test_partial_write_leaves_no_final_or_temporary_file(self) -> None:
        """부분 기록 실패 시 최종 파일과 임시 파일을 남기지 않는지 검증."""

        report = FailureReport.build(
            run_id="run-1",
            failures=[
                FailureEvent(
                    code=IssueCode.RUNNER_OPERATION_FAILED,
                    stage="runner",
                    message="failed",
                )
            ],
        )
        real_write = os.write
        calls = 0

        def fail_after_partial_write(descriptor, contents):
            """부분 기록 뒤 실패하는 테스트 대체 동작."""

            nonlocal calls
            calls += 1
            if calls == 1:
                partial = max(1, len(contents) // 2)
                return real_write(descriptor, contents[:partial])
            raise OSError("simulated partial write failure")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            target = root / "failure.json"
            stderr = io.StringIO()

            with patch(
                "sync.runtime.failure.os.write",
                side_effect=fail_after_partial_write,
            ):
                self.assertIsNone(
                    write_failure_report_exact(
                        report,
                        target=target,
                        stderr=stderr,
                    )
                )

            self.assertFalse(target.exists())
            self.assertEqual(list(root.iterdir()), [])
            self.assertEqual(
                stderr.getvalue(),
                "REPORT_WRITE_FAILED: failure report could not be written\n",
            )

    def test_directory_fsync_failure_removes_published_report_and_temporary_file(
        self,
    ) -> None:
        """디렉터리 동기화 실패 시 게시된 보고서와 임시 파일 제거 검증."""

        report = FailureReport.build(
            run_id="run-1",
            failures=[
                FailureEvent(
                    code=IssueCode.RUNNER_OPERATION_FAILED,
                    stage="runner",
                    message="failed",
                )
            ],
        )
        real_fsync = os.fsync
        calls = 0

        def fail_directory_fsync(descriptor):
            """디렉터리 동기화만 실패시키는 테스트 대체 동작."""

            nonlocal calls
            calls += 1
            if calls == 1:
                return real_fsync(descriptor)
            raise OSError("simulated directory fsync failure")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            target = root / "failure.json"
            stderr = io.StringIO()

            with patch(
                "sync.runtime.failure.os.fsync",
                side_effect=fail_directory_fsync,
            ):
                self.assertIsNone(
                    write_failure_report_exact(
                        report,
                        target=target,
                        stderr=stderr,
                    )
                )

            self.assertFalse(target.exists())
            self.assertEqual(list(root.iterdir()), [])
            self.assertEqual(
                stderr.getvalue(),
                "REPORT_WRITE_FAILED: failure report could not be written\n",
            )


if __name__ == "__main__":
    unittest.main()
