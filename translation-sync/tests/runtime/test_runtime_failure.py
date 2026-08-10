"""runtime failure 동작과 경계 조건 검증."""

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
    """실패 code 동작과 경계 조건 테스트 모음."""

    def test_every_stable_code_has_one_classification_and_exit_meaning(self) -> None:
        """`every_stable_code` 관련 경계 조건 검증."""

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
        """`exit_priority`의 three 이후 two 이후 one 판정 검증."""

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
        """`non_failure_status_cannot_be_reported_as_a_failure` 시나리오 검증."""

        with self.assertRaises(ValueError):
            FailureEvent(
                code=IssueCode.NORMALIZED_NOOP,
                stage="source",
                message="not an error",
            )

    def test_attempts_are_present_only_for_provider_failures(self) -> None:
        """`attempts_are_present_only_for_provider_failures` 시나리오 검증."""

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
    """실패 보고서 동작과 경계 조건 테스트 모음."""

    def _events(self) -> list[FailureEvent]:
        """events 처리."""

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
        """`report`의 highest exit priority 대상 top level fields 사용 검증."""

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
        """`canonical_bytes_are` 관련 경계 조건 검증."""

        first, second = self._events()
        kwargs = {
            "run_id": "실행-1",
            "manifest_digest": "a" * 64,
            "base_head": "b" * 40,
        }
        report_a = FailureReport.build(failures=[first, second], **kwargs)
        report_b = FailureReport.build(failures=[second, first], **kwargs)

        # The infrastructure issue has the unique highest priority, so changing
        # lower-priority detection order must not change canonical bytes.
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
        """`messages_are_short` 관련 경계 조건 검증."""

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
        """`single_segment_absolute`의 상태 판정 경계 검증."""

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
        """`context_paths_must_be_repository_or_artifact_relative` 시나리오 검증."""

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
        """`write`의 no replace 및 uses redacted stderr fallback 판정 검증."""

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
        """`missing_artifact_root`의 않음 get created 동작 검증."""

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
        """`exact_path_writer`의 no replace 및 않음 create parent 판정 검증."""

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
        """`exact_path_writer`의 symlink 및 non 디렉터리 ancestors 거부 검증."""

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
        """`partial_write_leaves_no_final_or_temporary_file` 시나리오 검증."""

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
            """테스트용 after partial write 대체 동작."""

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
        """`directory_fsync_failure`의 published 보고서 및 temporary 파일 제거 검증."""

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
            """테스트용 디렉터리 fsync 대체 동작."""

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
