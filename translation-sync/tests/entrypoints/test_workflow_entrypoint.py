"""workflow entrypoint 동작과 경계 조건 검증."""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import os
import tempfile
import time
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock

import workflow
from sync.runtime.failure import ExitCode
from sync.runtime.workflow import (
    DEPLOYED_STATE_FILENAME,
    FIXTURE_EVIDENCE_FILENAME,
    MANIFEST_FILENAME,
    PREPARATION_KEY_FILENAME,
    PREPARED_STATE_FILENAME,
    PUBLISHED_STATE_FILENAME,
    _canonical_json,
    _sealed_mapping,
)


HEAD = "a" * 40
TREE = "b" * 40
KEY = b"k" * 32
SELECTOR = b'{"document":null,"version":null}\n'
MANIFEST = b'{"schema_version":1,"entries":[]}\n'
FIXTURE_EVIDENCE = b"fixture-evidence\n"


class WorkflowEntrypointStateTests(unittest.TestCase):
    """워크플로 entrypoint 상태 동작과 경계 조건 테스트 모음."""

    def setUp(self) -> None:
        """테스트 사전 상태 구성."""

        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.candidate = self.root / "candidate"
        self.candidate.mkdir()
        key_path = self.root / PREPARATION_KEY_FILENAME
        key_path.write_bytes(KEY)
        key_path.chmod(0o600)
        (self.root / MANIFEST_FILENAME).write_bytes(MANIFEST)
        (self.root / FIXTURE_EVIDENCE_FILENAME).write_bytes(FIXTURE_EVIDENCE)

    def tearDown(self) -> None:
        """테스트 사후 상태 정리."""

        self.temporary.cleanup()

    def prepared_mapping(
        self,
        *,
        deadline: float | None = None,
    ) -> dict[str, object]:
        """prepared mapping 처리."""

        unsigned = {
            "schema_version": 1,
            "run_id": "run-1",
            "workflow_deadline_monotonic": (
                time.monotonic() + 1000 if deadline is None else deadline
            ),
            "branch": "main",
            "push_endpoint": "https://github.com/example/repository.git",
            "deploy_repository": "example/repository",
            "deploy_host": "github.com",
            "deploy_workflow": "deploy.yml",
            "base": {
                "head": HEAD,
                "tree": TREE,
                "remote_ref": "refs/heads/main",
                "remote_oid": HEAD,
                "active_fingerprint": "f" * 64,
            },
            "replay": {
                "manifest_file": MANIFEST_FILENAME,
                "manifest_digest": hashlib.sha256(MANIFEST).hexdigest(),
                "selector_base64": base64.b64encode(SELECTOR).decode("ascii"),
                "selector_digest": hashlib.sha256(SELECTOR).hexdigest(),
            },
            "fixture": {
                "evidence_file": FIXTURE_EVIDENCE_FILENAME,
                "evidence_digest": hashlib.sha256(FIXTURE_EVIDENCE).hexdigest(),
            },
            "candidate": {
                "path": "candidate",
                "base_commit": HEAD,
                "verified_tree": TREE,
                "has_changes": False,
            },
            "publication": {
                "base_head": HEAD,
                "base_tree": TREE,
                "remote_ref": "refs/heads/main",
                "verified_tree": TREE,
                "commit_oid": None,
                "seal": "9" * 64,
            },
        }
        return _sealed_mapping(unsigned, KEY)

    def write_prepared(self, value: dict[str, object] | None = None) -> None:
        """prepared 기록."""

        (self.root / PREPARED_STATE_FILENAME).write_bytes(
            _canonical_json(value or self.prepared_mapping())
        )

    def write_published(
        self,
        *,
        branch: str = "feature",
        deadline: float | None = None,
    ) -> None:
        """published 기록."""

        value = _sealed_mapping(
            {
                "schema_version": 1,
                "run_id": "run-1",
                "workflow_deadline_monotonic": (
                    time.monotonic() + 1000 if deadline is None else deadline
                ),
                "branch": branch,
                "push_endpoint": "https://github.com/example/repository.git",
                "deploy_repository": "example/repository",
                "deploy_host": "github.com",
                "deploy_workflow": "deploy.yml",
                "manifest_digest": hashlib.sha256(MANIFEST).hexdigest(),
                "active_fingerprint": "f" * 64,
                "base_commit": HEAD,
                "published_commit": HEAD,
                "remote_commit": HEAD,
                "has_changes": False,
            },
            KEY,
        )
        (self.root / PUBLISHED_STATE_FILENAME).write_bytes(_canonical_json(value))

    def test_prepared_state_seal_detects_canonical_tampering(self) -> None:
        """`prepared_state_seal`의 canonical tampering 감지 검증."""

        value = self.prepared_mapping()
        value["branch"] = "other"
        self.write_prepared(value)

        with self.assertRaises(workflow.EntrypointError) as caught:
            workflow._load_prepared_state(self.root)

        self.assertEqual(caught.exception.code.value, "VERIFIED_TREE_MISMATCH")

    def test_private_preparation_key_rejects_group_or_world_permissions(self) -> None:
        """`private_preparation_key`의 group 또는 world permissions 거부 검증."""

        self.write_prepared()
        (self.root / PREPARATION_KEY_FILENAME).chmod(0o644)

        with self.assertRaises(workflow.EntrypointError) as caught:
            workflow._load_prepared_state(self.root)

        self.assertEqual(caught.exception.code.value, "INVALID_RUNTIME_OPTION")

    def test_prepared_candidate_path_rejects_symlink_component(self) -> None:
        """`prepared_candidate_path`의 symlink component 거부 검증."""

        link = self.root / "candidate-link"
        link.symlink_to(self.candidate, target_is_directory=True)
        value = self.prepared_mapping()
        value.pop("state_seal")
        candidate = dict(value["candidate"])
        candidate["path"] = link.name
        value["candidate"] = candidate
        self.write_prepared(_sealed_mapping(value, KEY))

        with self.assertRaises(workflow.EntrypointError) as caught:
            workflow._load_prepared_state(self.root)

        self.assertEqual(caught.exception.code.value, "INVALID_RUNTIME_OPTION")

    def test_publish_https_requires_credentials_before_mutation(self) -> None:
        """`publish_https`의 mutation 전 credentials 요구 검증."""

        self.write_prepared()
        args = argparse.Namespace(artifact_root=self.root)

        with mock.patch.object(workflow, "_verify_active_repository") as verify:
            result = workflow.run_publish(
                args,
                environment={"PATH": "/bin:/usr/bin"},
            )

        self.assertEqual(result, ExitCode.CONTROLLED_FAILURE)
        verify.assert_called_once()
        self.assertFalse((self.root / PUBLISHED_STATE_FILENAME).exists())
        report = json.loads(
            (self.root / "translation-sync-failure.json").read_text()
        )
        self.assertEqual(report["code"], "PUBLICATION_CREDENTIAL_UNAVAILABLE")
        self.assertEqual(
            report["manifest_digest"],
            hashlib.sha256(MANIFEST).hexdigest(),
        )
        self.assertEqual(report["base_head"], HEAD)

    def test_prepublication_fingerprint_preserves_deadline_code(self) -> None:
        """`prepublication_fingerprint`의 기한 code 보존 검증."""

        self.write_prepared()
        args = argparse.Namespace(artifact_root=self.root)

        class FingerprintPublisher:
            """fingerprint publisher 객체."""

            def __init__(self, **kwargs):
                """fingerprint publisher 초기화."""

                self.read_fingerprint = kwargs["read_active_fingerprint"]

            def publish(self, prepared, *, push_environment):
                """publish 처리."""

                self.read_fingerprint(10.0)
                raise AssertionError("fingerprint deadline must stop publication")

        with (
            mock.patch.object(workflow, "Publisher", FingerprintPublisher),
            mock.patch.object(
                workflow,
                "active_repository_fingerprint",
                side_effect=workflow.RepositoryStateError(
                    workflow.IssueCode.WORKFLOW_DEADLINE_EXCEEDED
                ),
            ),
        ):
            result = workflow.run_publish(
                args,
                environment={
                    "PATH": "/bin:/usr/bin",
                    "GH_TOKEN": "push-token",
                },
            )

        self.assertEqual(result, ExitCode.INFRASTRUCTURE_FAILURE)
        report = json.loads(
            (self.root / "translation-sync-failure.json").read_text()
        )
        self.assertEqual(report["code"], "WORKFLOW_DEADLINE_EXCEEDED")
        self.assertIsNone(report["published_commit"])

    def test_final_fingerprint_io_error_is_runner_failure(self) -> None:
        """`final_fingerprint_io_error`의 runner 실패 판정 검증."""

        with mock.patch.object(
            workflow,
            "active_repository_fingerprint",
            side_effect=OSError("fingerprint read failed"),
        ):
            with self.assertRaises(workflow.EntrypointError) as caught:
                workflow._verify_active_repository(
                    expected_fingerprint="f" * 64,
                    deadline=workflow.WorkflowDeadline(
                        expires_at=time.monotonic() + 1000
                    ),
                    published_commit=HEAD,
                )

        self.assertEqual(
            caught.exception.code,
            workflow.IssueCode.RUNNER_OPERATION_FAILED,
        )
        self.assertEqual(caught.exception.published_commit, HEAD)

    def test_final_fingerprint_must_finish_before_deadline(self) -> None:
        """`final_fingerprint_must_finish_before_deadline` 시나리오 검증."""

        deadline = workflow.WorkflowDeadline(
            expires_at=100.0,
            _clock=lambda: 101.0,
        )
        with mock.patch.object(
            workflow,
            "active_repository_fingerprint",
            return_value="f" * 64,
        ):
            with self.assertRaises(workflow.EntrypointError) as caught:
                workflow._verify_active_repository(
                    expected_fingerprint="f" * 64,
                    deadline=deadline,
                    published_commit=HEAD,
                )

        self.assertEqual(
            caught.exception.code,
            workflow.IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
        )

    def test_askpass_helper_keeps_token_out_of_script(self) -> None:
        """`askpass_helper`의 token out of script 유지 검증."""

        token = "credential-value-that-must-not-enter-the-helper"

        with workflow._push_environment(
            "https://github.com/example/repository.git",
            {"PATH": "/bin:/usr/bin", "GH_TOKEN": token},
        ) as environment:
            helper = Path(environment["GIT_ASKPASS"])
            self.assertTrue(helper.is_file())
            self.assertNotIn(token.encode(), helper.read_bytes())
            self.assertNotIn("GH_TOKEN", environment)
            self.assertEqual(environment["TRANSLATION_SYNC_PUSH_TOKEN"], token)
            self.assertEqual(helper.stat().st_mode & 0o777, 0o700)

    def test_post_publication_state_write_failure_retains_commit_context(self) -> None:
        """post publication 상태 write 실패 retains 커밋 문맥 시나리오 검증."""

        self.write_prepared()
        args = argparse.Namespace(artifact_root=self.root)
        with (
            mock.patch.object(workflow, "Publisher") as publisher_type,
            mock.patch.object(
                workflow,
                "_verify_active_repository",
            ) as verify,
            mock.patch.object(
                workflow,
                "_write_no_replace",
                side_effect=OSError("state write failed"),
            ),
        ):
            publisher_type.return_value.publish.return_value = (
                workflow.PublicationResult(
                    published_oid=HEAD,
                    commit_oid=None,
                    pushed=False,
                )
            )
            result = workflow.run_publish(
                args,
                environment={
                    "PATH": "/bin:/usr/bin",
                    "GH_TOKEN": "push-token",
                },
            )

        self.assertEqual(result, ExitCode.INFRASTRUCTURE_FAILURE)
        verify.assert_called_once()
        report = json.loads(
            (self.root / "translation-sync-failure.json").read_text()
        )
        self.assertEqual(report["code"], "RUNNER_OPERATION_FAILED")
        self.assertEqual(report["published_commit"], HEAD)
        self.assertEqual(
            report["manifest_digest"],
            hashlib.sha256(MANIFEST).hexdigest(),
        )

    def test_push_cleanup_failure_retains_successful_publication_commit(self) -> None:
        """`push_cleanup_failure` 관련 경계 조건 검증."""

        self.write_prepared()
        args = argparse.Namespace(artifact_root=self.root)
        with (
            mock.patch.object(workflow, "Publisher") as publisher_type,
            mock.patch.object(workflow, "_verify_active_repository"),
            mock.patch.object(
                workflow.tempfile.TemporaryDirectory,
                "_rmtree",
                side_effect=OSError("cleanup failed"),
            ),
        ):
            publisher_type.return_value.publish.return_value = (
                workflow.PublicationResult(
                    published_oid=HEAD,
                    commit_oid=None,
                    pushed=False,
                )
            )
            result = workflow.run_publish(
                args,
                environment={
                    "PATH": "/bin:/usr/bin",
                    "GH_TOKEN": "push-token",
                },
            )

        self.assertEqual(result, ExitCode.INFRASTRUCTURE_FAILURE)
        report = json.loads(
            (self.root / "translation-sync-failure.json").read_text()
        )
        self.assertEqual(report["code"], "RUNNER_OPERATION_FAILED")
        self.assertEqual(report["published_commit"], HEAD)

    def test_push_cleanup_failure_preserves_publication_error_context(self) -> None:
        """`push_cleanup_failure`의 publication 오류 문맥 보존 검증."""

        self.write_prepared()
        args = argparse.Namespace(artifact_root=self.root)
        publication_error = workflow.PublicationError(
            workflow.IssueCode.PUBLICATION_BASE_CHANGED,
            published_commit=HEAD,
        )
        with (
            mock.patch.object(workflow, "Publisher") as publisher_type,
            mock.patch.object(workflow, "_verify_active_repository"),
            mock.patch.object(
                workflow.tempfile.TemporaryDirectory,
                "_rmtree",
                side_effect=OSError("cleanup failed"),
            ),
        ):
            publisher_type.return_value.publish.side_effect = publication_error
            result = workflow.run_publish(
                args,
                environment={
                    "PATH": "/bin:/usr/bin",
                    "GH_TOKEN": "push-token",
                },
            )

        self.assertEqual(result, ExitCode.INFRASTRUCTURE_FAILURE)
        report = json.loads(
            (self.root / "translation-sync-failure.json").read_text()
        )
        self.assertEqual(report["code"], "RUNNER_OPERATION_FAILED")
        self.assertEqual(
            {issue["code"] for issue in report["issues"]},
            {"PUBLICATION_BASE_CHANGED", "RUNNER_OPERATION_FAILED"},
        )
        self.assertEqual(report["published_commit"], HEAD)

    def test_deadline_after_publication_reports_published_commit(self) -> None:
        """`deadline_after_publication_reports_published_commit` 시나리오 검증."""

        self.write_prepared()
        args = argparse.Namespace(artifact_root=self.root)
        with (
            mock.patch.object(workflow, "Publisher") as publisher_type,
            mock.patch.object(
                workflow.WorkflowDeadline,
                "phase_remaining",
                side_effect=(
                    1000.0,
                    workflow.DeadlineExceeded(
                        workflow.IssueCode.WORKFLOW_DEADLINE_EXCEEDED
                    ),
                ),
            ),
        ):
            publisher_type.return_value.publish.return_value = (
                workflow.PublicationResult(
                    published_oid=HEAD,
                    commit_oid=None,
                    pushed=False,
                )
            )
            result = workflow.run_publish(
                args,
                environment={
                    "PATH": "/bin:/usr/bin",
                    "GH_TOKEN": "push-token",
                },
            )

        self.assertEqual(result, ExitCode.INFRASTRUCTURE_FAILURE)
        self.assertFalse((self.root / PUBLISHED_STATE_FILENAME).exists())
        report = json.loads(
            (self.root / "translation-sync-failure.json").read_text()
        )
        self.assertEqual(report["code"], "WORKFLOW_DEADLINE_EXCEEDED")
        self.assertEqual(report["published_commit"], HEAD)

    def test_expired_prepared_state_retains_failure_report_context(self) -> None:
        """`expired_prepared_state_retains_failure_report_context` 시나리오 검증."""

        self.write_prepared(
            self.prepared_mapping(deadline=time.monotonic() - 1)
        )
        args = argparse.Namespace(artifact_root=self.root)
        with (
            mock.patch.object(workflow, "Publisher") as publisher_type,
            mock.patch.object(workflow, "_verify_active_repository") as verify,
        ):
            result = workflow.run_publish(
                args,
                environment={
                    "PATH": "/bin:/usr/bin",
                    "GH_TOKEN": "push-token",
                },
            )

        self.assertEqual(result, ExitCode.INFRASTRUCTURE_FAILURE)
        publisher_type.assert_not_called()
        verify.assert_not_called()
        report = json.loads(
            (self.root / "translation-sync-failure.json").read_text()
        )
        self.assertEqual(report["code"], "WORKFLOW_DEADLINE_EXCEEDED")
        self.assertEqual(report["run_id"], "run-1")
        self.assertEqual(report["base_head"], HEAD)
        self.assertEqual(
            report["manifest_digest"],
            hashlib.sha256(MANIFEST).hexdigest(),
        )

    def test_final_mutation_outranks_publication_state_write_failure(self) -> None:
        """`final_mutation_outranks_publication_state_write_failure` 시나리오 검증."""

        self.write_prepared()
        args = argparse.Namespace(artifact_root=self.root)
        mutation = workflow.EntrypointError(
            workflow.IssueCode.ACTIVE_WORKTREE_MUTATED,
            stage="active-fingerprint",
            published_commit=HEAD,
        )
        with (
            mock.patch.object(workflow, "Publisher") as publisher_type,
            mock.patch.object(
                workflow,
                "_write_no_replace",
                side_effect=OSError("state write failed"),
            ),
            mock.patch.object(
                workflow,
                "_verify_active_repository",
                side_effect=mutation,
            ),
        ):
            publisher_type.return_value.publish.return_value = (
                workflow.PublicationResult(
                    published_oid=HEAD,
                    commit_oid=None,
                    pushed=False,
                )
            )
            result = workflow.run_publish(
                args,
                environment={
                    "PATH": "/bin:/usr/bin",
                    "GH_TOKEN": "push-token",
                },
            )

        self.assertEqual(result, ExitCode.ACTIVE_STATE_MUTATION)
        report = json.loads(
            (self.root / "translation-sync-failure.json").read_text()
        )
        self.assertEqual(report["code"], "ACTIVE_WORKTREE_MUTATED")
        self.assertEqual(
            {issue["code"] for issue in report["issues"]},
            {"ACTIVE_WORKTREE_MUTATED", "RUNNER_OPERATION_FAILED"},
        )
        self.assertEqual(report["published_commit"], HEAD)

    def test_non_main_deploy_is_a_separate_no_trigger_success_phase(self) -> None:
        """`non_main_deploy`의 separate no trigger success phase 판정 검증."""

        self.write_published(branch="feature/docs-sync")
        args = argparse.Namespace(
            artifact_root=self.root,
            repository="attacker/fork",
            correlation_prefix=None,
        )

        with (
            mock.patch.object(workflow, "_verify_active_repository") as verify,
            mock.patch.object(
                workflow,
                "DeploymentCoordinator",
            ) as coordinator_type,
        ):
            coordinator_type.return_value.deploy.return_value = (
                workflow.DeploymentResult(
                    branch="feature/docs-sync",
                    published_commit=HEAD,
                )
            )
            result = workflow.run_deploy(
                args,
                environment={
                    "PATH": "/bin:/usr/bin",
                    "GH_HOST": "attacker.example",
                },
            )

        self.assertEqual(result, ExitCode.SUCCESS)
        self.assertEqual(verify.call_count, 2)
        coordinator_kwargs = coordinator_type.call_args.kwargs
        self.assertEqual(coordinator_kwargs["repository"], "example/repository")
        self.assertEqual(
            coordinator_kwargs["runner"]._environment["GH_HOST"],
            "github.com",
        )
        deployed = json.loads((self.root / DEPLOYED_STATE_FILENAME).read_text())
        self.assertFalse(deployed["triggered"])
        self.assertEqual(deployed["published_commit"], HEAD)
        self.assertEqual(
            deployed["manifest_digest"],
            hashlib.sha256(MANIFEST).hexdigest(),
        )

    def test_expired_published_state_retains_commit_in_failure_report(self) -> None:
        """expired published 상태 retains 커밋 in 실패 보고서 시나리오 검증."""

        self.write_published(deadline=time.monotonic() - 1)
        args = argparse.Namespace(
            artifact_root=self.root,
            correlation_prefix=None,
        )
        with (
            mock.patch.object(
                workflow,
                "DeploymentCoordinator",
            ) as coordinator_type,
            mock.patch.object(workflow, "_verify_active_repository") as verify,
        ):
            result = workflow.run_deploy(
                args,
                environment={"PATH": "/bin:/usr/bin"},
            )

        self.assertEqual(result, ExitCode.INFRASTRUCTURE_FAILURE)
        coordinator_type.assert_not_called()
        verify.assert_not_called()
        report = json.loads(
            (self.root / "translation-sync-failure.json").read_text()
        )
        self.assertEqual(report["code"], "WORKFLOW_DEADLINE_EXCEEDED")
        self.assertEqual(report["run_id"], "run-1")
        self.assertEqual(report["base_head"], HEAD)
        self.assertEqual(report["published_commit"], HEAD)
        self.assertEqual(
            report["manifest_digest"],
            hashlib.sha256(MANIFEST).hexdigest(),
        )

    def test_final_mutation_outranks_deploy_failure(self) -> None:
        """`final_mutation_outranks_deploy_failure` 시나리오 검증."""

        self.write_published(branch="main")
        args = argparse.Namespace(
            artifact_root=self.root,
            correlation_prefix=None,
        )
        mutation = workflow.EntrypointError(
            workflow.IssueCode.ACTIVE_WORKTREE_MUTATED,
            stage="active-fingerprint",
            published_commit=HEAD,
        )
        with (
            mock.patch.object(
                workflow,
                "_verify_active_repository",
                side_effect=(None, mutation),
            ),
            mock.patch.object(
                workflow,
                "DeploymentCoordinator",
            ) as coordinator_type,
        ):
            coordinator_type.return_value.deploy.return_value = (
                workflow.DeploymentResult(
                    branch="main",
                    published_commit=HEAD,
                    correlation_id="sync-run",
                    issue_code=workflow.IssueCode.DEPLOY_TRIGGER_FAILED,
                    published_commit_retained=True,
                )
            )
            result = workflow.run_deploy(
                args,
                environment={"PATH": "/bin:/usr/bin"},
            )

        self.assertEqual(result, ExitCode.ACTIVE_STATE_MUTATION)
        report = json.loads(
            (self.root / "translation-sync-failure.json").read_text()
        )
        self.assertEqual(report["code"], "ACTIVE_WORKTREE_MUTATED")
        self.assertEqual(
            {issue["code"] for issue in report["issues"]},
            {"ACTIVE_WORKTREE_MUTATED", "DEPLOY_TRIGGER_FAILED"},
        )
        self.assertEqual(report["published_commit"], HEAD)

    def test_invalid_cli_options_use_controlled_failure_exit_code(self) -> None:
        """`invalid_cli_options_use_controlled_failure_exit_code` 시나리오 검증."""

        stderr = io.StringIO()
        with redirect_stderr(stderr):
            result = workflow.main(["prepare"], environment={})

        self.assertEqual(result, ExitCode.CONTROLLED_FAILURE)
        self.assertIn("REPORT_WRITE_FAILED", stderr.getvalue())

    def test_invalid_artifact_root_uses_fixed_stderr_fallback(self) -> None:
        """`invalid_artifact_root`의 fixed stderr fallback 사용 검증."""

        args = argparse.Namespace(
            artifact_root=self.root / "missing",
            push_endpoint="https://github.com/example/repository.git",
            repository="example/repository",
            branch="main",
            commit_message="docs: synchronize translations",
            version=None,
            doc=None,
        )
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            result = workflow.run_prepare(
                args,
                environment={},
                started_at=time.monotonic(),
            )

        self.assertEqual(result, ExitCode.CONTROLLED_FAILURE)
        self.assertEqual(
            stderr.getvalue(),
            "REPORT_WRITE_FAILED: failure report could not be written\n",
        )

    def test_artifact_root_cannot_be_repository_ancestor(self) -> None:
        """`artifact_root_cannot_be_repository_ancestor` 시나리오 검증."""

        repository = self.root / "active-repository"
        repository.mkdir()

        with mock.patch.object(workflow, "REPOSITORY_ROOT", repository):
            with self.assertRaises(workflow.EntrypointError) as caught:
                workflow._artifact_root(self.root)

        self.assertEqual(
            caught.exception.code,
            workflow.IssueCode.INVALID_RUNTIME_OPTION,
        )

    def test_invalid_prepared_state_does_not_invent_publish_run_id(self) -> None:
        """`invalid_prepared_state`의 않음 invent publish 실행 id 동작 검증."""

        (self.root / PREPARED_STATE_FILENAME).write_bytes(b"{}\n")
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            result = workflow.run_publish(
                argparse.Namespace(artifact_root=self.root),
                environment={},
            )

        self.assertEqual(result, ExitCode.CONTROLLED_FAILURE)
        self.assertFalse(
            (self.root / "translation-sync-failure.json").exists()
        )
        self.assertIn("REPORT_WRITE_FAILED", stderr.getvalue())

    def test_invalid_published_state_does_not_invent_deploy_run_id(self) -> None:
        """`invalid_published_state`의 않음 invent 배포 실행 id 동작 검증."""

        (self.root / PUBLISHED_STATE_FILENAME).write_bytes(b"{}\n")
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            result = workflow.run_deploy(
                argparse.Namespace(
                    artifact_root=self.root,
                    correlation_prefix=None,
                ),
                environment={},
            )

        self.assertEqual(result, ExitCode.CONTROLLED_FAILURE)
        self.assertFalse(
            (self.root / "translation-sync-failure.json").exists()
        )
        self.assertIn("REPORT_WRITE_FAILED", stderr.getvalue())

    def test_prepare_unexpected_configuration_error_writes_stable_report(self) -> None:
        """`prepare_unexpected_configuration_error`의 stable 보고서 기록 검증."""

        args = argparse.Namespace(
            artifact_root=self.root,
            push_endpoint="https://github.com/example/repository.git",
            repository="example/repository",
            branch="main",
            commit_message="docs: synchronize translations",
            version=None,
            doc=None,
        )
        with mock.patch.object(
            workflow,
            "load_workflow_settings",
            side_effect=RuntimeError("unexpected"),
        ):
            result = workflow.run_prepare(
                args,
                environment={"PATH": "/bin:/usr/bin"},
                started_at=time.monotonic(),
            )

        self.assertEqual(result, ExitCode.INFRASTRUCTURE_FAILURE)
        report = json.loads(
            (self.root / "translation-sync-failure.json").read_text()
        )
        self.assertEqual(report["code"], "UNCLASSIFIED_INTERNAL")


if __name__ == "__main__":
    unittest.main()
