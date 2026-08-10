"""워크플로 실행 동작과 경계 조건 검증."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
import subprocess
from pathlib import Path
from unittest import mock

from sync.runtime.base import ApprovedPublicationBase
from sync.runtime.base import RepositoryStateError
from sync.runtime.candidate import (
    SYNC_FAILURE_REPORT_FILENAME,
    CandidateFailure,
    CandidateResult,
)
from sync.runtime.config import load_config, provider_config_sha256
from sync.runtime.failure import ExitCode, FailureEvent, FailureReport, IssueCode
from sync.runtime.publication import PreparedPublication
from sync.runtime.process import ProcessTreeLeak
from sync.runtime.settings import WorkflowSettings
from sync.runtime.unit_test import (
    ApprovedBaseUnitTestFailure,
    ApprovedBaseUnitTestProof,
    ApprovedBaseUnitTestResult,
)
from sync.runtime.workflow import (
    PREPARED_STATE_FILENAME,
    PrepareRequest,
    ReplaySnapshot,
    WorkflowHooks,
    WorkflowPreparer,
    WorkflowStageError,
    _prepare_git_environment,
    _run_stage_command,
    _stage_environment,
    _validate_fixture_evidence,
    _write_no_replace,
)


HEAD = "a" * 40
BASE_TREE = "b" * 40
VERIFIED_TREE = "c" * 40
COMMIT = "d" * 40
FINGERPRINT = "e" * 64
MANIFEST = b'{"schema_version":1,"entries":[]}\n'
SELECTOR = b'{"document":null,"version":null}\n'


class MutableClock:
    """값을 변경할 수 있는 테스트 시계."""

    def __init__(self, value: float = 100.0) -> None:
        """현재 시각 초기화."""

        self.value = value

    def __call__(self) -> float:
        """현재 시각 반환."""

        return self.value


def settings(*, timeout: int = 1000) -> WorkflowSettings:
    """테스트용 워크플로 설정 구성."""

    return WorkflowSettings(
        workflow_timeout_seconds=timeout,
        unit_test_command=("unit", "test"),
        replay_command=("replay",),
        provider_fixture_command=("fixture",),
        candidate_setup_commands=(("npm", "ci"),),
        sync_core_command=("sync",),
        site_validation_commands=(("site-1",), ("site-2",)),
        path_validation_command=("paths",),
        deploy_workflow="deploy.yml",
    )


def environment(
    *,
    run_timeout: int = 100,
    workflow_timeout: int = 1000,
) -> dict[str, str]:
    """테스트용 실행 환경 구성."""

    return {
        "PATH": "/bin:/usr/bin",
        "LANG": "C.UTF-8",
        "TRANSLATION_PROVIDER": "openai",
        "TRANSLATION_MODEL": "gpt-5.6",
        "TRANSLATION_CONTEXT_WINDOW_TOKENS": "1000",
        "TRANSLATION_RESERVED_OUTPUT_TOKENS": "100",
        "TRANSLATION_REQUEST_TIMEOUT_SECONDS": "10",
        "TRANSLATION_RUN_TIMEOUT_SECONDS": str(run_timeout),
        "TRANSLATION_WORKFLOW_TIMEOUT_SECONDS": str(workflow_timeout),
        "TRANSLATION_TOKENIZER_ENCODING": "o200k_base",
        "OPENAI_API_KEY": "must-not-be-serialized",
        "AZURE_OPENAI_API_KEY": "must-not-reach-openai-children",
        "CODEX_ACCESS_TOKEN": "must-not-reach-openai-children",
        "GH_TOKEN": "must-not-reach-pre-publication-children",
        "HOME": "/must/not/reach/candidate",
        "TRANSLATION_PRIVATE_TOKEN": "must-not-reach-any-child",
    }


def fixture_evidence() -> bytes:
    """테스트용 제공자 픽스처 증거 구성."""

    config_digest = provider_config_sha256(load_config(environment()))
    shared = (
        "provider=openai model=gpt-5.6 model_profile=gpt-5.6 "
        "reasoning=medium"
    )
    versions = (
        "fixture_version=1 response_contract_version=1 "
        "budget_profile_version=1"
    )
    return (
        f"{shared} locale=ko prompt_sha256={'1' * 64} {versions} "
        f"config_sha256={config_digest} status=passed\n"
        f"{shared} locale=ja prompt_sha256={'2' * 64} {versions} "
        f"config_sha256={config_digest} status=passed\n"
    ).encode("utf-8")


def approved_base() -> ApprovedPublicationBase:
    """테스트용 승인 기준본 구성."""

    return ApprovedPublicationBase(
        head=HEAD,
        tree=BASE_TREE,
        remote_ref="refs/heads/main",
        remote_oid=HEAD,
        active_fingerprint=FINGERPRINT,
    )


def unit_success() -> ApprovedBaseUnitTestResult:
    """테스트용 단위 테스트 성공 결과 구성."""

    return ApprovedBaseUnitTestResult(
        proof=ApprovedBaseUnitTestProof(
            base_commit=HEAD,
            base_tree=BASE_TREE,
            argv_digest="f" * 64,
        )
    )


def replay_snapshot() -> ReplaySnapshot:
    """테스트용 재실행 스냅샷 구성."""

    return ReplaySnapshot(
        manifest=MANIFEST,
        manifest_digest=hashlib.sha256(MANIFEST).hexdigest(),
        selector=SELECTOR,
        selector_digest=hashlib.sha256(SELECTOR).hexdigest(),
    )


class WorkflowPreparerTests(unittest.TestCase):
    """워크플로 준비기 동작과 경계 조건 테스트 모음."""

    def setUp(self) -> None:
        """테스트 사전 상태 구성."""

        self.temporary = tempfile.TemporaryDirectory()
        root = Path(self.temporary.name)
        self.repo = root / "repo"
        self.artifacts = root / "artifacts"
        self.repo.mkdir()
        self.artifacts.mkdir()
        self.clock = MutableClock()
        self.events: list[str] = []
        self.fixture_environment: dict[str, str] | None = None
        self.candidate_environment: dict[str, str] | None = None

    def tearDown(self) -> None:
        """테스트 사후 상태 정리."""

        self.temporary.cleanup()

    def request(self) -> PrepareRequest:
        """테스트용 준비 요청 구성."""

        return PrepareRequest(
            repository=self.repo,
            artifact_root=self.artifacts,
            push_endpoint="https://github.com/example/repository.git",
            deploy_repository="example/repository",
            branch="main",
            commit_message="docs: synchronize translations",
        )

    def hooks(self) -> WorkflowHooks:
        """호출 순서를 기록하는 워크플로 훅 구성."""

        def capture(request: PrepareRequest, remaining):
            """승인 기준본 캡처."""

            self.events.append("base")
            self.assertGreater(remaining(), 0)
            return approved_base()

        def unit(request: PrepareRequest, base, argv, remaining):
            """단위 테스트 실행."""

            self.events.append("unit")
            self.assertEqual(argv, ("unit", "test"))
            self.assertEqual(base.head, HEAD)
            return unit_success()

        def replay(request, argv, output_path, stage_environment, remaining):
            """재실행 수행."""

            self.events.append("replay")
            self.assertEqual(argv, ("replay",))
            self.assertNotIn("GH_TOKEN", stage_environment)
            self.assertNotIn("HOME", stage_environment)
            self.assertNotIn("TRANSLATION_PRIVATE_TOKEN", stage_environment)
            self.assertEqual(
                stage_environment["TRANSLATION_WORKFLOW_DEADLINE_MONOTONIC"],
                "1100",
            )
            return replay_snapshot()

        def fixture(request, argv, stage_environment, remaining):
            """제공자 픽스처 실행."""

            self.events.append("fixture")
            self.fixture_environment = dict(stage_environment)
            self.assertNotIn("GH_TOKEN", stage_environment)
            self.assertEqual(stage_environment["HOME"], os.devnull)
            self.assertEqual(stage_environment["XDG_CONFIG_HOME"], os.devnull)
            self.assertNotIn("TRANSLATION_PRIVATE_TOKEN", stage_environment)
            self.assertNotIn("AZURE_OPENAI_API_KEY", stage_environment)
            self.assertNotIn("CODEX_ACCESS_TOKEN", stage_environment)
            return fixture_evidence()

        def candidate(
            request,
            base,
            setup_argvs,
            sync_argv,
            site_argvs,
            path_argv,
            stage_environment,
            remaining,
        ):
            """후보 실행."""

            self.events.append("candidate")
            self.candidate_environment = dict(stage_environment)
            self.assertEqual(base.head, HEAD)
            self.assertEqual(setup_argvs, (("npm", "ci"),))
            self.assertEqual(stage_environment["HOME"], os.devnull)
            self.assertEqual(stage_environment["XDG_CONFIG_HOME"], os.devnull)
            self.assertNotIn("AZURE_OPENAI_API_KEY", stage_environment)
            self.assertNotIn("CODEX_ACCESS_TOKEN", stage_environment)
            self.assertEqual(sync_argv, ("sync",))
            self.assertEqual(site_argvs, (("site-1",), ("site-2",)))
            self.assertEqual(path_argv, ("paths",))
            manifest_path = Path(stage_environment["TRANSLATION_UPSTREAM_MANIFEST"])
            self.assertEqual(manifest_path.read_bytes(), MANIFEST)
            (self.artifacts / "candidate-1").mkdir()
            return CandidateResult(
                sandbox=self.artifacts / "candidate-1",
                base_commit=HEAD,
                verified_tree=VERIFIED_TREE,
                has_changes=True,
            )

        def publication(request, base, candidate, preparation_key, remaining):
            """게시 준비."""

            self.events.append("publication-prepare")
            self.assertEqual(candidate.verified_tree, VERIFIED_TREE)
            self.assertEqual(len(preparation_key), 32)
            return PreparedPublication(
                base_head=HEAD,
                base_tree=BASE_TREE,
                remote_ref="refs/heads/main",
                verified_tree=VERIFIED_TREE,
                commit_oid=COMMIT,
                seal="9" * 64,
            )

        def fingerprint(request, remaining):
            """활성 저장소 지문 조회."""

            self.events.append("fingerprint")
            return FINGERPRINT

        return WorkflowHooks(
            capture_base=capture,
            run_unit_tests=unit,
            run_replay=replay,
            run_provider_fixture=fixture,
            build_candidate=candidate,
            prepare_publication=publication,
            read_active_fingerprint=fingerprint,
        )

    def preparer(self, hooks: WorkflowHooks | None = None) -> WorkflowPreparer:
        """테스트용 워크플로 준비기 구성."""

        return WorkflowPreparer(
            settings=settings(),
            environment=environment(),
            hooks=hooks or self.hooks(),
            clock=self.clock,
            run_id_factory=lambda: "run-1",
            preparation_key_factory=lambda: b"k" * 32,
        )

    def test_prepare_runs_exact_order_and_writes_canonical_state(self) -> None:
        """준비 단계를 정확한 순서로 실행하고 정규 상태를 기록하는지 검증."""

        outcome = self.preparer().prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.SUCCESS)
        self.assertEqual(
            self.events,
            [
                "base",
                "unit",
                "replay",
                "fixture",
                "candidate",
                "publication-prepare",
                "fingerprint",
                "fingerprint",
            ],
        )
        self.assertEqual(
            self.fixture_environment["TRANSLATION_RUN_DEADLINE_MONOTONIC"],
            "200",
        )
        self.assertEqual(
            self.fixture_environment["TRANSLATION_RUN_DEADLINE_MONOTONIC"],
            self.candidate_environment["TRANSLATION_RUN_DEADLINE_MONOTONIC"],
        )
        self.assertEqual(
            self.fixture_environment["TRANSLATION_SELECTOR_JSON"],
            SELECTOR.decode("utf-8"),
        )
        self.assertEqual(
            self.fixture_environment["TRANSLATION_UPSTREAM_MANIFEST_DIGEST"],
            hashlib.sha256(MANIFEST).hexdigest(),
        )
        self.assertEqual(
            self.fixture_environment["OPENAI_API_KEY"],
            self.candidate_environment["OPENAI_API_KEY"],
        )
        self.assertEqual(
            {
                key
                for key in self.fixture_environment
                if key.endswith("API_KEY") or key.endswith("ACCESS_TOKEN")
            },
            {"OPENAI_API_KEY"},
        )

        state_bytes = (self.artifacts / PREPARED_STATE_FILENAME).read_bytes()
        self.assertNotIn(b"must-not-be-serialized", state_bytes)
        state = json.loads(state_bytes)
        self.assertEqual(state["base"]["head"], HEAD)
        self.assertEqual(state["candidate"]["verified_tree"], VERIFIED_TREE)
        self.assertEqual(state["publication"]["commit_oid"], COMMIT)
        self.assertEqual(state["candidate"]["path"], "candidate-1")
        self.assertEqual(state["deploy_repository"], "example/repository")
        self.assertEqual(state["deploy_host"], "github.com")
        self.assertEqual(
            state["fixture"]["evidence_digest"],
            hashlib.sha256(fixture_evidence()).hexdigest(),
        )
        self.assertEqual(
            (self.artifacts / state["fixture"]["evidence_file"]).read_bytes(),
            fixture_evidence(),
        )
        self.assertEqual(
            state_bytes,
            (
                json.dumps(
                    state,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                + "\n"
            ).encode(),
        )

    def test_run_deadline_is_created_immediately_before_fixture(self) -> None:
        """실행 기한을 제공자 픽스처 직전에 생성하는지 검증."""

        hooks = self.hooks()
        original_replay = hooks.run_replay

        def replay(*args, **kwargs):
            """재실행 후 현재 시각 전진."""

            result = original_replay(*args, **kwargs)
            self.clock.value = 450.0
            return result

        hooks = WorkflowHooks(
            capture_base=hooks.capture_base,
            run_unit_tests=hooks.run_unit_tests,
            run_replay=replay,
            run_provider_fixture=hooks.run_provider_fixture,
            build_candidate=hooks.build_candidate,
            prepare_publication=hooks.prepare_publication,
            read_active_fingerprint=hooks.read_active_fingerprint,
        )

        outcome = self.preparer(hooks).prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.SUCCESS)
        self.assertEqual(
            self.fixture_environment["TRANSLATION_RUN_DEADLINE_MONOTONIC"],
            "550",
        )
        self.assertEqual(
            self.fixture_environment["TRANSLATION_WORKFLOW_DEADLINE_MONOTONIC"],
            "1100",
        )

    def test_unit_failure_is_fail_fast_and_writes_report(self) -> None:
        """단위 테스트 실패 시 즉시 중단하고 보고서를 기록하는지 검증."""

        hooks = self.hooks()

        def failed_unit(*args, **kwargs):
            """단위 테스트 실패 결과 반환."""

            self.events.append("unit")
            return ApprovedBaseUnitTestResult(
                failure=ApprovedBaseUnitTestFailure(
                    stage="unit-test",
                    issue_code=IssueCode.UNIT_TEST_FAILED,
                    returncode=1,
                )
            )

        hooks = WorkflowHooks(
            capture_base=hooks.capture_base,
            run_unit_tests=failed_unit,
            run_replay=hooks.run_replay,
            run_provider_fixture=hooks.run_provider_fixture,
            build_candidate=hooks.build_candidate,
            prepare_publication=hooks.prepare_publication,
            read_active_fingerprint=hooks.read_active_fingerprint,
        )

        outcome = self.preparer(hooks).prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.CONTROLLED_FAILURE)
        self.assertEqual(self.events, ["base", "unit", "fingerprint"])
        report = json.loads(outcome.report_path.read_bytes())
        self.assertEqual(report["code"], "UNIT_TEST_FAILED")
        self.assertFalse((self.artifacts / PREPARED_STATE_FILENAME).exists())

    def test_fixture_failure_stops_before_candidate(self) -> None:
        """제공자 픽스처 실패 시 후보 실행 전에 중단하는지 검증."""

        hooks = self.hooks()

        def fixture(*args, **kwargs):
            """제공자 픽스처 실패 결과 반환."""

            self.events.append("fixture")
            raise WorkflowStageError(
                stage="provider-fixture",
                code=IssueCode.FIXTURE_CONTRACT_FAILED,
                message="fixture response contract failed",
            )

        hooks = WorkflowHooks(
            capture_base=hooks.capture_base,
            run_unit_tests=hooks.run_unit_tests,
            run_replay=hooks.run_replay,
            run_provider_fixture=fixture,
            build_candidate=hooks.build_candidate,
            prepare_publication=hooks.prepare_publication,
            read_active_fingerprint=hooks.read_active_fingerprint,
        )

        outcome = self.preparer(hooks).prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.CONTROLLED_FAILURE)
        self.assertEqual(
            self.events,
            ["base", "unit", "replay", "fixture", "fingerprint"],
        )
        report = json.loads(outcome.report_path.read_bytes())
        self.assertEqual(report["code"], "FIXTURE_CONTRACT_FAILED")

    def test_invalid_fixture_success_evidence_stops_before_candidate(self) -> None:
        """잘못된 픽스처 성공 증거에서 후보 실행 전에 중단하는지 검증."""

        hooks = self.hooks()

        def fixture(*args, **kwargs):
            """잘못된 픽스처 성공 증거 반환."""

            self.events.append("fixture")
            return b"provider output that is not canonical evidence\n"

        hooks = WorkflowHooks(
            capture_base=hooks.capture_base,
            run_unit_tests=hooks.run_unit_tests,
            run_replay=hooks.run_replay,
            run_provider_fixture=fixture,
            build_candidate=hooks.build_candidate,
            prepare_publication=hooks.prepare_publication,
            read_active_fingerprint=hooks.read_active_fingerprint,
        )

        outcome = self.preparer(hooks).prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.CONTROLLED_FAILURE)
        self.assertEqual(
            self.events,
            ["base", "unit", "replay", "fixture", "fingerprint"],
        )
        report = json.loads(outcome.report_path.read_bytes())
        self.assertEqual(report["code"], "FIXTURE_CONTRACT_FAILED")

    def test_fixture_evidence_is_exactly_bound_to_live_config(self) -> None:
        """픽스처 증거가 실제 제공자 설정에 정확히 결합되는지 검증."""

        config = load_config(environment())
        evidence = fixture_evidence()

        self.assertEqual(
            _validate_fixture_evidence(evidence, config),
            evidence,
        )
        mismatches = (
            (b"provider=openai", b"provider=cli"),
            (b"model=gpt-5.6", b"model=gpt-5.6-sol"),
            (b"reasoning=medium", b"reasoning=low"),
            (b"config_sha256=", b"config_sha256=0"),
        )
        for original, replacement in mismatches:
            with self.subTest(field=original):
                altered = evidence.replace(original, replacement)
                with self.assertRaises(WorkflowStageError) as caught:
                    _validate_fixture_evidence(altered, config)
                self.assertEqual(
                    caught.exception.code,
                    IssueCode.FIXTURE_CONTRACT_FAILED,
                )

    def test_replay_selector_mismatch_stops_before_live_fixture(self) -> None:
        """재실행 선택자 불일치 시 실제 제공자 픽스처 전에 중단하는지 검증."""

        hooks = self.hooks()
        mismatched = b'{"document":null,"version":"master"}\n'

        def replay(*args, **kwargs):
            """선택자가 다른 재실행 스냅샷 반환."""

            self.events.append("replay")
            return ReplaySnapshot(
                manifest=MANIFEST,
                manifest_digest=hashlib.sha256(MANIFEST).hexdigest(),
                selector=mismatched,
                selector_digest=hashlib.sha256(mismatched).hexdigest(),
            )

        hooks = WorkflowHooks(
            capture_base=hooks.capture_base,
            run_unit_tests=hooks.run_unit_tests,
            run_replay=replay,
            run_provider_fixture=hooks.run_provider_fixture,
            build_candidate=hooks.build_candidate,
            prepare_publication=hooks.prepare_publication,
            read_active_fingerprint=hooks.read_active_fingerprint,
        )

        outcome = self.preparer(hooks).prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.CONTROLLED_FAILURE)
        self.assertEqual(self.events, ["base", "unit", "replay", "fingerprint"])
        report = json.loads(outcome.report_path.read_bytes())
        self.assertEqual(report["code"], "INVALID_SELECTOR")

    def test_invalid_live_selector_stops_before_base_capture(self) -> None:
        """잘못된 실제 선택자에서 기준본 캡처 전에 중단하는지 검증."""

        request = self.request()
        request = PrepareRequest(
            repository=request.repository,
            artifact_root=request.artifact_root,
            push_endpoint=request.push_endpoint,
            deploy_repository=request.deploy_repository,
            branch=request.branch,
            commit_message=request.commit_message,
            version=None,
            document="guide.md",
        )

        outcome = self.preparer().prepare(request)

        self.assertEqual(outcome.exit_code, ExitCode.CONTROLLED_FAILURE)
        self.assertEqual(self.events, [])
        report = json.loads(outcome.report_path.read_bytes())
        self.assertEqual(report["code"], "INVALID_SELECTOR")

    def test_candidate_failure_never_prepares_publication(self) -> None:
        """후보 실패 시 게시를 준비하지 않는지 검증."""

        hooks = self.hooks()

        def candidate(*args, **kwargs):
            """후보 실패 결과 반환."""

            self.events.append("candidate")
            (self.artifacts / "candidate-failed").mkdir()
            return CandidateResult(
                sandbox=self.artifacts / "candidate-failed",
                base_commit=HEAD,
                failure=CandidateFailure(
                    stage="site-validation",
                    issue_code=IssueCode.SITE_VALIDATION_FAILED,
                    returncode=1,
                ),
            )

        hooks = WorkflowHooks(
            capture_base=hooks.capture_base,
            run_unit_tests=hooks.run_unit_tests,
            run_replay=hooks.run_replay,
            run_provider_fixture=hooks.run_provider_fixture,
            build_candidate=candidate,
            prepare_publication=hooks.prepare_publication,
            read_active_fingerprint=hooks.read_active_fingerprint,
        )

        outcome = self.preparer(hooks).prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.CONTROLLED_FAILURE)
        self.assertNotIn("publication-prepare", self.events)
        report = json.loads(outcome.report_path.read_bytes())
        self.assertEqual(report["candidate_debug_path"], "candidate-failed")

    def test_generic_candidate_failure_consumes_stable_child_report(self) -> None:
        """일반 후보 실패가 안정적 하위 작업 보고서를 사용하는지 검증."""

        hooks = self.hooks()

        def candidate(
            request,
            base,
            setup_argvs,
            sync_argv,
            site_argvs,
            path_argv,
            stage_environment,
            remaining,
        ):
            """하위 작업 보고서를 포함한 후보 실패 결과 반환."""

            self.events.append("candidate")
            sandbox = self.artifacts / "candidate-child-failed"
            sandbox.mkdir()
            child_report = FailureReport.build(
                run_id="run-1",
                failures=(
                    FailureEvent(
                        code=IssueCode.OUTPUT_STATE_MISMATCH,
                        stage="path-validation",
                        message="generated states did not match",
                        version="12.x",
                        locale="ko",
                        document="docs/example.md",
                        plan_id="plan-1",
                        structural_address="section:example",
                    ),
                    FailureEvent(
                        code=IssueCode.RESIDUAL_PATTERN,
                        stage="path-validation",
                        message="one source phrase remains",
                        structural_address="section:second",
                    ),
                ),
                manifest_digest=hashlib.sha256(MANIFEST).hexdigest(),
                base_head=HEAD,
                candidate_debug_path="candidate-child-failed",
            )
            report_path = self.artifacts / SYNC_FAILURE_REPORT_FILENAME
            report_path.write_bytes(child_report.to_bytes())
            return CandidateResult(
                sandbox=sandbox,
                base_commit=HEAD,
                failure=CandidateFailure(
                    stage="path-validation",
                    issue_code=None,
                    returncode=1,
                    report_path=report_path,
                ),
            )

        hooks = WorkflowHooks(
            capture_base=hooks.capture_base,
            run_unit_tests=hooks.run_unit_tests,
            run_replay=hooks.run_replay,
            run_provider_fixture=hooks.run_provider_fixture,
            build_candidate=candidate,
            prepare_publication=hooks.prepare_publication,
            read_active_fingerprint=hooks.read_active_fingerprint,
        )

        outcome = self.preparer(hooks).prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.CONTROLLED_FAILURE)
        report = json.loads(outcome.report_path.read_bytes())
        self.assertEqual(report["code"], "OUTPUT_STATE_MISMATCH")
        self.assertEqual(report["version"], "12.x")
        self.assertEqual(report["locale"], "ko")
        self.assertEqual(report["document"], "docs/example.md")
        self.assertEqual(report["plan_id"], "plan-1")
        self.assertEqual(report["structural_address"], "section:example")
        self.assertEqual(
            {issue["code"] for issue in report["issues"]},
            {"OUTPUT_STATE_MISMATCH", "RESIDUAL_PATTERN"},
        )
        self.assertEqual(
            report["manifest_digest"],
            hashlib.sha256(MANIFEST).hexdigest(),
        )
        self.assertEqual(report["base_head"], HEAD)

    def test_noncanonical_child_failure_report_is_infrastructure(self) -> None:
        """비정규 하위 작업 실패 보고서를 인프라 실패로 판정하는지 검증."""

        hooks = self.hooks()

        def candidate(*args, **kwargs):
            """비정규 보고서를 포함한 후보 실패 결과 반환."""

            self.events.append("candidate")
            sandbox = self.artifacts / "candidate-invalid-report"
            sandbox.mkdir()
            child_report = FailureReport.build(
                run_id="run-1",
                failures=(
                    FailureEvent(
                        code=IssueCode.OUTPUT_STATE_MISMATCH,
                        stage="path-validation",
                        message="generated states did not match",
                    ),
                ),
            )
            report_path = self.artifacts / SYNC_FAILURE_REPORT_FILENAME
            report_path.write_text(
                json.dumps(child_report.to_mapping(), indent=2) + "\n",
                encoding="utf-8",
            )
            return CandidateResult(
                sandbox=sandbox,
                base_commit=HEAD,
                failure=CandidateFailure(
                    stage="path-validation",
                    issue_code=None,
                    returncode=1,
                    report_path=report_path,
                ),
            )

        hooks = WorkflowHooks(
            capture_base=hooks.capture_base,
            run_unit_tests=hooks.run_unit_tests,
            run_replay=hooks.run_replay,
            run_provider_fixture=hooks.run_provider_fixture,
            build_candidate=candidate,
            prepare_publication=hooks.prepare_publication,
            read_active_fingerprint=hooks.read_active_fingerprint,
        )

        outcome = self.preparer(hooks).prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.INFRASTRUCTURE_FAILURE)
        report = json.loads(outcome.report_path.read_bytes())
        self.assertEqual(report["code"], "RUNNER_OPERATION_FAILED")

    def test_missing_candidate_child_report_is_infrastructure(self) -> None:
        """후보 하위 작업 보고서 누락을 인프라 실패로 판정하는지 검증."""

        hooks = self.hooks()

        def candidate(*args, **kwargs):
            """보고서가 누락된 후보 실패 결과 반환."""

            self.events.append("candidate")
            sandbox = self.artifacts / "candidate-no-report"
            sandbox.mkdir()
            return CandidateResult(
                sandbox=sandbox,
                base_commit=HEAD,
                failure=CandidateFailure(
                    stage="sync-core",
                    issue_code=None,
                    returncode=1,
                    report_path=self.artifacts / SYNC_FAILURE_REPORT_FILENAME,
                ),
            )

        hooks = WorkflowHooks(
            capture_base=hooks.capture_base,
            run_unit_tests=hooks.run_unit_tests,
            run_replay=hooks.run_replay,
            run_provider_fixture=hooks.run_provider_fixture,
            build_candidate=candidate,
            prepare_publication=hooks.prepare_publication,
            read_active_fingerprint=hooks.read_active_fingerprint,
        )

        outcome = self.preparer(hooks).prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.INFRASTRUCTURE_FAILURE)
        report = json.loads(outcome.report_path.read_bytes())
        self.assertEqual(report["code"], "RUNNER_OPERATION_FAILED")

    def test_final_active_mutation_has_highest_exit_and_blocks_state(self) -> None:
        """최종 활성 저장소 변경이 최우선 종료 코드를 사용하고 상태 기록을 차단하는지 검증."""

        hooks = self.hooks()

        def fingerprint(*args, **kwargs):
            """마지막 조회에서 변경된 활성 저장소 지문 반환."""

            self.events.append("fingerprint")
            return "0" * 64

        hooks = WorkflowHooks(
            capture_base=hooks.capture_base,
            run_unit_tests=hooks.run_unit_tests,
            run_replay=hooks.run_replay,
            run_provider_fixture=hooks.run_provider_fixture,
            build_candidate=hooks.build_candidate,
            prepare_publication=hooks.prepare_publication,
            read_active_fingerprint=fingerprint,
        )

        outcome = self.preparer(hooks).prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.ACTIVE_STATE_MUTATION)
        self.assertFalse((self.artifacts / PREPARED_STATE_FILENAME).exists())
        report = json.loads(outcome.report_path.read_bytes())
        self.assertEqual(report["code"], "ACTIVE_WORKTREE_MUTATED")

    def test_state_write_failure_still_rechecks_final_fingerprint(self) -> None:
        """상태 기록 실패에도 최종 활성 저장소 지문을 다시 확인하는지 검증."""

        hooks = self.hooks()
        fingerprints = iter((FINGERPRINT, "0" * 64))

        def fingerprint(*args, **kwargs):
            """활성 저장소 지문 조회 횟수 기록."""

            self.events.append("fingerprint")
            return next(fingerprints)

        hooks = WorkflowHooks(
            capture_base=hooks.capture_base,
            run_unit_tests=hooks.run_unit_tests,
            run_replay=hooks.run_replay,
            run_provider_fixture=hooks.run_provider_fixture,
            build_candidate=hooks.build_candidate,
            prepare_publication=hooks.prepare_publication,
            read_active_fingerprint=fingerprint,
        )

        def write(path: Path, contents: bytes) -> Path:
            """준비 상태 파일 기록만 실패."""

            if path.name == PREPARED_STATE_FILENAME:
                raise OSError("state write failed")
            return _write_no_replace(path, contents)

        with mock.patch(
            "sync.runtime.workflow._write_no_replace",
            side_effect=write,
        ):
            outcome = self.preparer(hooks).prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.ACTIVE_STATE_MUTATION)
        self.assertEqual(self.events[-2:], ["fingerprint", "fingerprint"])
        report = json.loads(outcome.report_path.read_bytes())
        self.assertEqual(report["code"], "ACTIVE_WORKTREE_MUTATED")
        self.assertEqual(
            {issue["code"] for issue in report["issues"]},
            {"ACTIVE_WORKTREE_MUTATED", "RUNNER_OPERATION_FAILED"},
        )

    def test_mutation_after_prepared_state_write_still_fails_run(self) -> None:
        """준비 상태 기록 후 활성 저장소가 변경돼도 실행이 실패하는지 검증."""

        hooks = self.hooks()
        fingerprints = iter((FINGERPRINT, "0" * 64))

        def fingerprint(*args, **kwargs):
            """마지막 조회에서 변경된 활성 저장소 지문 반환."""

            self.events.append("fingerprint")
            return next(fingerprints)

        hooks = WorkflowHooks(
            capture_base=hooks.capture_base,
            run_unit_tests=hooks.run_unit_tests,
            run_replay=hooks.run_replay,
            run_provider_fixture=hooks.run_provider_fixture,
            build_candidate=hooks.build_candidate,
            prepare_publication=hooks.prepare_publication,
            read_active_fingerprint=fingerprint,
        )

        outcome = self.preparer(hooks).prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.ACTIVE_STATE_MUTATION)
        self.assertTrue((self.artifacts / PREPARED_STATE_FILENAME).is_file())
        report = json.loads(outcome.report_path.read_bytes())
        self.assertEqual(report["code"], "ACTIVE_WORKTREE_MUTATED")

    def test_final_fingerprint_deadline_is_infrastructure(self) -> None:
        """최종 지문 조회의 기한 초과를 인프라 실패로 판정하는지 검증."""

        hooks = self.hooks()

        def fingerprint(*args, **kwargs):
            """최종 활성 저장소 지문 조회에서 기한 초과 발생."""

            self.events.append("fingerprint")
            raise RepositoryStateError(IssueCode.WORKFLOW_DEADLINE_EXCEEDED)

        hooks = WorkflowHooks(
            capture_base=hooks.capture_base,
            run_unit_tests=hooks.run_unit_tests,
            run_replay=hooks.run_replay,
            run_provider_fixture=hooks.run_provider_fixture,
            build_candidate=hooks.build_candidate,
            prepare_publication=hooks.prepare_publication,
            read_active_fingerprint=fingerprint,
        )

        outcome = self.preparer(hooks).prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.INFRASTRUCTURE_FAILURE)
        report = json.loads(outcome.report_path.read_bytes())
        self.assertEqual(report["code"], "WORKFLOW_DEADLINE_EXCEEDED")

    def test_deadline_expiring_during_final_fingerprint_is_failure(self) -> None:
        """최종 지문 조회 중 기한 만료를 실패로 판정하는지 검증."""

        hooks = self.hooks()

        def fingerprint(*args, **kwargs):
            """최종 지문 조회 중 워크플로 기한 소진."""

            self.events.append("fingerprint")
            self.clock.value = 1101.0
            return FINGERPRINT

        hooks = WorkflowHooks(
            capture_base=hooks.capture_base,
            run_unit_tests=hooks.run_unit_tests,
            run_replay=hooks.run_replay,
            run_provider_fixture=hooks.run_provider_fixture,
            build_candidate=hooks.build_candidate,
            prepare_publication=hooks.prepare_publication,
            read_active_fingerprint=fingerprint,
        )

        outcome = self.preparer(hooks).prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.INFRASTRUCTURE_FAILURE)
        report = json.loads(outcome.report_path.read_bytes())
        self.assertEqual(report["code"], "WORKFLOW_DEADLINE_EXCEEDED")

    def test_final_fingerprint_io_error_is_infrastructure_not_mutation(self) -> None:
        """최종 지문 입출력 오류를 저장소 변경이 아닌 인프라 실패로 판정하는지 검증."""

        hooks = self.hooks()

        def fingerprint(*args, **kwargs):
            """최종 활성 저장소 지문 조회에서 입출력 오류 발생."""

            self.events.append("fingerprint")
            raise OSError("fingerprint unavailable")

        hooks = WorkflowHooks(
            capture_base=hooks.capture_base,
            run_unit_tests=hooks.run_unit_tests,
            run_replay=hooks.run_replay,
            run_provider_fixture=hooks.run_provider_fixture,
            build_candidate=hooks.build_candidate,
            prepare_publication=hooks.prepare_publication,
            read_active_fingerprint=fingerprint,
        )

        outcome = self.preparer(hooks).prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.INFRASTRUCTURE_FAILURE)
        report = json.loads(outcome.report_path.read_bytes())
        self.assertEqual(report["code"], "RUNNER_OPERATION_FAILED")

    def test_existing_prepared_state_fails_before_any_stage(self) -> None:
        """기존 준비 상태 파일이 있으면 모든 단계 전에 실패하는지 검증."""

        (self.artifacts / PREPARED_STATE_FILENAME).write_text("owned\n")

        outcome = self.preparer().prepare(self.request())

        self.assertEqual(outcome.exit_code, ExitCode.CONTROLLED_FAILURE)
        self.assertEqual(self.events, [])
        self.assertEqual(
            (self.artifacts / PREPARED_STATE_FILENAME).read_text(),
            "owned\n",
        )

    def test_artifact_root_inside_repository_is_rejected(self) -> None:
        """저장소 내부의 산출물 루트 거부 검증."""

        inside = self.repo / "artifacts"
        inside.mkdir()
        request = PrepareRequest(
            repository=self.repo,
            artifact_root=inside,
            push_endpoint="https://github.com/example/repository.git",
            deploy_repository="example/repository",
            branch="main",
            commit_message="docs: synchronize translations",
        )

        outcome = self.preparer().prepare(request)

        self.assertEqual(outcome.exit_code, ExitCode.CONTROLLED_FAILURE)
        self.assertEqual(self.events, [])

    def test_artifact_root_ancestor_of_repository_is_rejected(self) -> None:
        """저장소의 상위 경로인 산출물 루트 거부 검증."""

        request = PrepareRequest(
            repository=self.repo,
            artifact_root=self.repo.parent,
            push_endpoint="https://github.com/example/repository.git",
            deploy_repository="example/repository",
            branch="main",
            commit_message="docs: synchronize translations",
        )

        outcome = self.preparer().prepare(request)

        self.assertEqual(outcome.exit_code, ExitCode.CONTROLLED_FAILURE)
        self.assertIsNone(outcome.report_path)
        self.assertEqual(self.events, [])

    def test_push_endpoint_must_match_sealed_deploy_repository(self) -> None:
        """푸시 엔드포인트와 봉인된 배포 저장소의 일치 요구 검증."""

        request = PrepareRequest(
            repository=self.repo,
            artifact_root=self.artifacts,
            push_endpoint="https://github.com/other/repository.git",
            deploy_repository="example/repository",
            branch="main",
            commit_message="docs: synchronize translations",
        )

        outcome = self.preparer().prepare(request)

        self.assertEqual(outcome.exit_code, ExitCode.CONTROLLED_FAILURE)
        self.assertEqual(self.events, [])
        report = json.loads(outcome.report_path.read_bytes())
        self.assertEqual(report["code"], "INVALID_RUNTIME_OPTION")

    def test_push_endpoint_credentials_are_rejected_before_base_capture(self) -> None:
        """자격 증명을 포함한 푸시 엔드포인트를 기준본 캡처 전에 거부하는지 검증."""

        request = PrepareRequest(
            repository=self.repo,
            artifact_root=self.artifacts,
            push_endpoint=(
                "https://user:credential@github.com/example/repository.git"
            ),
            deploy_repository="example/repository",
            branch="main",
            commit_message="docs: synchronize translations",
        )

        outcome = self.preparer().prepare(request)

        self.assertEqual(outcome.exit_code, ExitCode.CONTROLLED_FAILURE)
        self.assertEqual(self.events, [])
        report = outcome.report_path.read_bytes()
        self.assertNotIn(b"credential", report)
        self.assertEqual(json.loads(report)["code"], "INVALID_RUNTIME_OPTION")

    def test_publication_prepare_environment_omits_credentials(self) -> None:
        """게시 준비 환경에서 자격 증명을 제외하는지 검증."""

        prepared = _prepare_git_environment(
            {
                "PATH": "/bin",
                "LANG": "C.UTF-8",
                "HOME": "/host-home",
                "HTTP_PROXY": "http://proxy.invalid",
                "OPENAI_API_KEY": "secret",
                "GH_TOKEN": "secret",
                "TRANSLATION_PRIVATE_TOKEN": "secret",
            }
        )

        self.assertEqual(prepared["PATH"], "/bin")
        self.assertEqual(prepared["GIT_AUTHOR_NAME"], "translation-sync")
        self.assertNotIn("HOME", prepared)
        self.assertNotIn("HTTP_PROXY", prepared)
        self.assertFalse(any("TOKEN" in key or "API_KEY" in key for key in prepared))

    def test_live_environment_keeps_only_selected_provider_auth(self) -> None:
        """실제 제공자 환경에 선택한 제공자 인증만 유지하는지 검증."""

        source = environment()
        source.update(
            {
                "AZURE_OPENAI_API_VERSION": "2026-01-01",
                "AZURE_OPENAI_ENDPOINT": "https://azure.example",
                "CODEX_API_KEY": "codex-api-key",
                "CODEX_HOME": "/explicit/codex-home",
            }
        )
        credential_keys = {
            "OPENAI_API_KEY",
            "AZURE_OPENAI_API_KEY",
            "CODEX_ACCESS_TOKEN",
            "CODEX_API_KEY",
            "CODEX_HOME",
        }
        cli_source = {
            **source,
            "TRANSLATION_PROVIDER": "cli",
            "TRANSLATION_CLI_COMMAND": "codex exec",
        }
        cli_source.pop("CODEX_API_KEY")
        cli_source.pop("CODEX_HOME")
        cases = (
            (
                source,
                {"OPENAI_API_KEY"},
            ),
            (
                {
                    **source,
                    "TRANSLATION_PROVIDER": "azure",
                    "TRANSLATION_MODEL": "deployment-name",
                    "TRANSLATION_MODEL_PROFILE": "gpt-5.6",
                },
                {"AZURE_OPENAI_API_KEY"},
            ),
            (
                cli_source,
                {"CODEX_ACCESS_TOKEN"},
            ),
        )

        for case_environment, expected_credentials in cases:
            with self.subTest(provider=case_environment["TRANSLATION_PROVIDER"]):
                config = load_config(case_environment)
                staged = _stage_environment(
                    case_environment,
                    validated_values=config.values,
                )
                self.assertEqual(
                    credential_keys.intersection(staged),
                    expected_credentials,
                )

    def test_fixture_process_timeout_uses_run_deadline_code(self) -> None:
        """픽스처 프로세스 기한 초과에 실행 기한 코드를 사용하는지 검증."""

        with mock.patch(
            "sync.runtime.workflow.run_process_tree",
            side_effect=subprocess.TimeoutExpired(("fixture",), 1),
        ):
            with self.assertRaises(WorkflowStageError) as caught:
                _run_stage_command(
                    ("fixture",),
                    cwd=self.repo,
                    environment={"PATH": "/bin"},
                    remaining_seconds=lambda: 1,
                    stage="provider-fixture",
                    deadline_code=IssueCode.RUN_DEADLINE_EXCEEDED,
                )

        self.assertEqual(caught.exception.stage, "provider-fixture")
        self.assertEqual(caught.exception.code, IssueCode.RUN_DEADLINE_EXCEEDED)

    def test_child_process_tree_leak_is_runner_failure(self) -> None:
        """하위 프로세스 트리 누수의 실행기 실패 판정 검증."""

        with mock.patch(
            "sync.runtime.workflow.run_process_tree",
            side_effect=ProcessTreeLeak("descendant survived"),
        ):
            with self.assertRaises(WorkflowStageError) as caught:
                _run_stage_command(
                    ("replay",),
                    cwd=self.repo,
                    environment={"PATH": "/bin"},
                    remaining_seconds=lambda: 1,
                    stage="replay",
                )

        self.assertEqual(caught.exception.stage, "replay")
        self.assertEqual(caught.exception.code, IssueCode.RUNNER_OPERATION_FAILED)


if __name__ == "__main__":
    unittest.main()
