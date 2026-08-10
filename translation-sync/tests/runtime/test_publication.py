"""publication 동작과 경계 조건 검증."""

from __future__ import annotations

import json
import math
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sync.runtime.failure import IssueCode
from sync.runtime.process import ProcessTreeCleanupError
from sync.runtime.publication import (
    PreparedPublication,
    PublicationBase,
    PublicationError,
    Publisher,
    build_cas_push_argv,
)


_TARGET_REF = "refs/heads/main"
_PREPARATION_KEY = b"p" * 32


def _git(repo: Path, *args: str) -> str:
    """테스트 저장소에서 Git 명령 실행 후 stdout 반환."""

    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _init_repositories(root: Path) -> tuple[Path, Path, Path, str, str]:
    """active·bare remote·candidate 저장소와 기준 식별자 생성."""

    active = root / "active"
    remote = root / "remote.git"
    candidate = root / "candidate"

    active.mkdir()
    _git(active, "init", "--quiet", "--initial-branch=main")
    _git(active, "config", "user.name", "Publication Tests")
    _git(active, "config", "user.email", "publication-tests@localhost")
    (active / "tracked.txt").write_text("approved\n", encoding="utf-8")
    _git(active, "add", "tracked.txt")
    _git(active, "commit", "--quiet", "-m", "approved base")

    remote.mkdir()
    _git(remote, "init", "--quiet", "--bare")
    _git(remote, "symbolic-ref", "HEAD", _TARGET_REF)
    _git(active, "remote", "add", "publish", str(remote))
    _git(active, "push", "--quiet", "publish", f"HEAD:{_TARGET_REF}")

    subprocess.run(
        ["git", "clone", "--quiet", str(remote), str(candidate)],
        check=True,
        capture_output=True,
        text=True,
    )
    _git(candidate, "config", "user.name", "Publication Tests")
    _git(candidate, "config", "user.email", "publication-tests@localhost")
    _git(candidate, "remote", "rename", "origin", "publish")

    base_head = _git(active, "rev-parse", "HEAD")
    base_tree = _git(active, "rev-parse", "HEAD^{tree}")
    return active, remote, candidate, base_head, base_tree


def _repository_state(repo: Path) -> tuple[str, str, str, str]:
    """HEAD·branch·index tree·worktree 상태 snapshot 반환."""

    return (
        _git(repo, "rev-parse", "HEAD"),
        _git(repo, "symbolic-ref", "HEAD"),
        _git(repo, "write-tree"),
        _git(repo, "status", "--porcelain=v1", "--untracked-files=all"),
    )


def _remote_oid(remote: Path) -> str:
    """bare remote의 main ref 객체 ID 조회."""

    return _git(remote, "rev-parse", _TARGET_REF)


def _ref_exists(repo: Path, ref: str) -> bool:
    """저장소에 정확한 ref가 존재하는지 판별."""

    return (
        subprocess.run(
            ["git", "show-ref", "--verify", "--quiet", ref],
            cwd=repo,
            check=False,
        ).returncode
        == 0
    )


def _is_push_argv(value: object) -> bool:
    """기록된 argv가 Git push 명령인지 판별."""

    return (
        isinstance(value, (tuple, list))
        and len(value) > 1
        and value[1] == "push"
    )


def _environment(**extra: str) -> dict[str, str]:
    """격리 Git 테스트 identity와 최소 환경 구성."""

    return {
        "PATH": os.environ["PATH"],
        "LANG": "C",
        "GIT_AUTHOR_NAME": "Translation Sync Tests",
        "GIT_AUTHOR_EMAIL": "translation-sync-tests@localhost",
        "GIT_COMMITTER_NAME": "Translation Sync Tests",
        "GIT_COMMITTER_EMAIL": "translation-sync-tests@localhost",
        **extra,
    }


def _publisher(
    *,
    candidate: Path,
    remote: Path,
    base_head: str,
    base_tree: str,
    expected_fingerprint: str = "active-v1",
    read_active_fingerprint=lambda _timeout: "active-v1",
    remaining_seconds=lambda: 30.0,
) -> Publisher:
    """고정 테스트 기준본으로 Publisher fixture 생성."""

    return Publisher(
        candidate_repo=candidate,
        push_endpoint=str(remote),
        base=PublicationBase(
            head=base_head,
            tree=base_tree,
            remote_ref=_TARGET_REF,
            active_fingerprint=expected_fingerprint,
        ),
        read_active_fingerprint=read_active_fingerprint,
        remaining_seconds=remaining_seconds,
        prepare_environment=_environment(),
        preparation_key=_PREPARATION_KEY,
    )


def _create_competing_commit(root: Path, remote: Path) -> tuple[Path, str]:
    """원격 브랜치를 선점할 경쟁 commit 생성."""

    competitor = root / "competitor"
    subprocess.run(
        ["git", "clone", "--quiet", str(remote), str(competitor)],
        check=True,
        capture_output=True,
        text=True,
    )
    _git(competitor, "config", "user.name", "Publication Tests")
    _git(competitor, "config", "user.email", "publication-tests@localhost")
    (competitor / "competing.txt").write_text("advanced\n", encoding="utf-8")
    _git(competitor, "add", "competing.txt")
    _git(competitor, "commit", "--quiet", "-m", "competing publication")
    return competitor, _git(competitor, "rev-parse", "HEAD")


class PublicationTests(unittest.TestCase):
    """publication 동작과 경계 조건 테스트 모음."""

    def test_builds_explicit_commit_to_ref_cas_push_argv(self) -> None:
        """explicit 커밋 후 ref cas push argv 생성 검증."""

        base = "a" * 40
        commit = "b" * 40

        self.assertEqual(
            build_cas_push_argv(
                push_endpoint="https://github.com/example/repository.git",
                remote_ref=_TARGET_REF,
                base_head=base,
                commit_oid=commit,
            ),
            (
                "git",
                "push",
                "--no-verify",
                "--no-follow-tags",
                f"--force-with-lease={_TARGET_REF}:{base}",
                "https://github.com/example/repository.git",
                f"{commit}:{_TARGET_REF}",
            ),
        )

    def test_creates_detached_verified_commit_and_publishes_without_local_mutation(
        self,
    ) -> None:
        """detached verified 커밋 및 publishes 제외 local mutation 생성 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            active, remote, candidate, base_head, base_tree = _init_repositories(
                Path(tmp)
            )
            (candidate / "tracked.txt").write_text("candidate\n", encoding="utf-8")
            _git(candidate, "add", "tracked.txt")
            verified_tree = _git(candidate, "write-tree")
            active_before = _repository_state(active)
            candidate_before = _repository_state(candidate)
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )

            real_run = subprocess.run
            publication_calls: list[dict[str, object]] = []

            def run_with_recording(*args: object, **kwargs: object):
                """with recording 실행."""

                publication_calls.append(kwargs.copy())
                return real_run(*args, **kwargs)

            with patch(
                "sync.runtime.publication.run_process_tree",
                side_effect=run_with_recording,
            ):
                prepared = publisher.prepare(
                    verified_tree=verified_tree,
                    commit_message="docs: publish translations",
                )
                result = publisher.publish(
                    prepared,
                    push_environment=_environment(),
                )

            self.assertIsNotNone(prepared.commit_oid)
            assert prepared.commit_oid is not None
            self.assertEqual(
                _git(candidate, "rev-parse", f"{prepared.commit_oid}^{{tree}}"),
                verified_tree,
            )
            self.assertEqual(
                _git(candidate, "show", "-s", "--format=%P", prepared.commit_oid),
                base_head,
            )
            self.assertEqual(_repository_state(active), active_before)
            self.assertEqual(_repository_state(candidate), candidate_before)

            self.assertTrue(result.pushed)
            self.assertEqual(result.published_oid, prepared.commit_oid)
            self.assertEqual(_remote_oid(remote), prepared.commit_oid)
            self.assertEqual(_repository_state(active), active_before)
            self.assertEqual(_repository_state(candidate), candidate_before)
            self.assertTrue(publication_calls)
            self.assertTrue(
                all(
                    isinstance(call.get("timeout"), (int, float))
                    and not isinstance(call["timeout"], bool)
                    and math.isfinite(float(call["timeout"]))
                    and float(call["timeout"]) > 0
                    and float(call["timeout"]) <= 30.0
                    for call in publication_calls
                )
            )

    def test_no_change_rechecks_base_and_skips_commit_and_push(self) -> None:
        """`no_change_rechecks_base_and_skips_commit_and_push` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            active, remote, candidate, base_head, base_tree = _init_repositories(
                Path(tmp)
            )
            active_before = _repository_state(active)
            candidate_before = _repository_state(candidate)
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )

            prepared = publisher.prepare(
                verified_tree=base_tree,
                commit_message="docs: publish translations",
            )
            result = publisher.publish(
                prepared,
                push_environment=_environment(),
            )

            self.assertIsNone(prepared.commit_oid)
            self.assertFalse(result.pushed)
            self.assertEqual(result.published_oid, base_head)
            self.assertEqual(_remote_oid(remote), base_head)
            self.assertEqual(_repository_state(active), active_before)
            self.assertEqual(_repository_state(candidate), candidate_before)

    def test_serialized_preparation_is_revalidated_by_a_new_publisher(self) -> None:
        """`serialized_preparation`의 revalidated by 신규 publisher 판정 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            _, remote, candidate, base_head, base_tree = _init_repositories(Path(tmp))
            (candidate / "tracked.txt").write_text("candidate\n", encoding="utf-8")
            _git(candidate, "add", "tracked.txt")
            preparer = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )
            prepared = preparer.prepare(
                verified_tree=_git(candidate, "write-tree"),
                commit_message="docs: publish translations",
            )
            restored = PreparedPublication.from_mapping(
                json.loads(json.dumps(prepared.to_mapping()))
            )
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )

            result = publisher.publish(
                restored,
                push_environment=_environment(),
            )

            self.assertTrue(result.pushed)
            self.assertEqual(result.published_oid, prepared.commit_oid)
            self.assertEqual(_remote_oid(remote), prepared.commit_oid)

    def test_prepare_uses_explicit_identity_without_candidate_user_config(self) -> None:
        """`prepare`의 explicit identity 제외 candidate user 설정 사용 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            _, remote, candidate, base_head, base_tree = _init_repositories(Path(tmp))
            _git(candidate, "config", "--unset-all", "user.name")
            _git(candidate, "config", "--unset-all", "user.email")
            (candidate / "tracked.txt").write_text("candidate\n", encoding="utf-8")
            _git(candidate, "add", "tracked.txt")
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )

            prepared = publisher.prepare(
                verified_tree=_git(candidate, "write-tree"),
                commit_message="docs: publish translations",
            )

            self.assertIsNotNone(prepared.commit_oid)
            assert prepared.commit_oid is not None
            self.assertEqual(
                _git(candidate, "show", "-s", "--format=%an", prepared.commit_oid),
                "Translation Sync Tests",
            )

    def test_active_fingerprint_change_blocks_publication(self) -> None:
        """`active_fingerprint_change`의 publication 차단 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            _, remote, candidate, base_head, base_tree = _init_repositories(Path(tmp))
            (candidate / "tracked.txt").write_text("candidate\n", encoding="utf-8")
            _git(candidate, "add", "tracked.txt")
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
                read_active_fingerprint=lambda _timeout: "active-v2",
            )
            prepared = publisher.prepare(
                verified_tree=_git(candidate, "write-tree"),
                commit_message="docs: publish translations",
            )

            with self.assertRaises(PublicationError) as caught:
                publisher.publish(prepared, push_environment=_environment())

            self.assertEqual(caught.exception.code, IssueCode.PUBLICATION_BASE_CHANGED)
            self.assertEqual(_remote_oid(remote), base_head)

    def test_remote_ref_change_blocks_publication_before_push(self) -> None:
        """`remote_ref_change`의 push 전 publication 차단 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, remote, candidate, base_head, base_tree = _init_repositories(root)
            (candidate / "tracked.txt").write_text("candidate\n", encoding="utf-8")
            _git(candidate, "add", "tracked.txt")
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )
            prepared = publisher.prepare(
                verified_tree=_git(candidate, "write-tree"),
                commit_message="docs: publish translations",
            )
            competitor, competing_oid = _create_competing_commit(root, remote)
            _git(competitor, "push", "--quiet", "origin", f"HEAD:{_TARGET_REF}")

            with self.assertRaises(PublicationError) as caught:
                publisher.publish(prepared, push_environment=_environment())

            self.assertEqual(caught.exception.code, IssueCode.PUBLICATION_BASE_CHANGED)
            self.assertEqual(_remote_oid(remote), competing_oid)

    def test_force_with_lease_closes_race_after_remote_ref_recheck(self) -> None:
        """`force_with_lease_closes_race_after_remote_ref_recheck` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, remote, candidate, base_head, base_tree = _init_repositories(root)
            (candidate / "tracked.txt").write_text("candidate\n", encoding="utf-8")
            _git(candidate, "add", "tracked.txt")
            competitor, competing_oid = _create_competing_commit(root, remote)

            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )
            prepared = publisher.prepare(
                verified_tree=_git(candidate, "write-tree"),
                commit_message="docs: publish translations",
            )
            real_remote_oid = publisher._remote_oid
            reads = 0

            def read_then_advance_remote(
                repo: Path,
                environment: dict[str, str],
            ) -> str:
                """then advance 원격 읽기."""

                nonlocal reads
                observed = real_remote_oid(repo, environment)
                reads += 1
                if reads == 1:
                    _git(
                        competitor,
                        "push",
                        "--quiet",
                        "origin",
                        f"HEAD:{_TARGET_REF}",
                    )
                return observed

            with patch.object(
                publisher,
                "_remote_oid",
                side_effect=read_then_advance_remote,
            ):
                with self.assertRaises(PublicationError) as caught:
                    publisher.publish(prepared, push_environment=_environment())

            self.assertEqual(caught.exception.code, IssueCode.PUBLICATION_BASE_CHANGED)
            self.assertIsNone(caught.exception.published_commit)
            self.assertEqual(_remote_oid(remote), competing_oid)

    def test_candidate_push_configuration_cannot_add_refs_or_redirect_endpoint(
        self,
    ) -> None:
        """`candidate_push_configuration` 관련 경계 조건 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, remote, candidate, base_head, base_tree = _init_repositories(root)
            redirected = root / "redirected.git"
            redirected.mkdir()
            _git(redirected, "init", "--quiet", "--bare")
            _git(redirected, "symbolic-ref", "HEAD", _TARGET_REF)
            _git(candidate, "tag", "-a", "base-tag", "-m", "base tag", base_head)
            _git(candidate, "config", "push.followTags", "true")
            _git(candidate, "config", "remote.publish.pushurl", str(redirected))
            _git(
                candidate,
                "config",
                f"url.{redirected}.pushInsteadOf",
                str(remote),
            )
            (candidate / "tracked.txt").write_text("candidate\n", encoding="utf-8")
            _git(candidate, "add", "tracked.txt")
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )
            prepared = publisher.prepare(
                verified_tree=_git(candidate, "write-tree"),
                commit_message="docs: publish translations",
            )

            result = publisher.publish(
                prepared,
                push_environment=_environment(),
            )

            self.assertTrue(result.pushed)
            self.assertEqual(_remote_oid(remote), prepared.commit_oid)
            self.assertFalse(_ref_exists(remote, "refs/tags/base-tag"))
            self.assertFalse(_ref_exists(redirected, _TARGET_REF))

    def test_commit_tree_mismatch_is_rejected_before_publication(self) -> None:
        """`commit_tree_mismatch`의 publication 전 rejected 판정 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            _, remote, candidate, base_head, base_tree = _init_repositories(Path(tmp))
            (candidate / "tracked.txt").write_text("candidate\n", encoding="utf-8")
            _git(candidate, "add", "tracked.txt")
            verified_tree = _git(candidate, "write-tree")
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )
            real_tree_oid = publisher._tree_oid
            calls = 0

            def substitute_commit_tree(
                repo: Path,
                object_oid: str,
                *,
                environment: dict[str, str],
            ) -> str:
                """substitute 커밋 tree 처리."""

                nonlocal calls
                calls += 1
                resolved = real_tree_oid(
                    repo,
                    object_oid,
                    environment=environment,
                )
                if calls == 3:
                    return base_tree
                return resolved

            with patch.object(
                publisher,
                "_tree_oid",
                side_effect=substitute_commit_tree,
            ):
                with self.assertRaises(PublicationError) as caught:
                    publisher.prepare(
                        verified_tree=verified_tree,
                        commit_message="docs: publish translations",
                    )

            self.assertEqual(caught.exception.code, IssueCode.VERIFIED_TREE_MISMATCH)
            self.assertEqual(_remote_oid(remote), base_head)

    def test_push_failure_does_not_expose_stderr_or_environment_values(self) -> None:
        """`push_failure`의 않음 expose stderr 또는 환경 values 동작 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            _, remote, candidate, base_head, base_tree = _init_repositories(Path(tmp))
            (candidate / "tracked.txt").write_text("candidate\n", encoding="utf-8")
            _git(candidate, "add", "tracked.txt")
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )
            prepared = publisher.prepare(
                verified_tree=_git(candidate, "write-tree"),
                commit_message="docs: publish translations",
            )
            failed = subprocess.CompletedProcess(
                args=["git", "push"],
                returncode=1,
                stdout=b"",
                stderr=b"api_key=DO_NOT_EXPOSE provider response body",
            )

            real_run = subprocess.run

            def fail_only_push(*args: object, **kwargs: object):
                """테스트용 only push 대체 동작."""

                argv = args[0]
                if _is_push_argv(argv):
                    return failed
                return real_run(*args, **kwargs)

            push_environment = _environment(TEST_PUSH_TOKEN="DO_NOT_EXPOSE")
            with patch(
                "sync.runtime.publication.run_process_tree",
                side_effect=fail_only_push,
            ) as run:
                with self.assertRaises(PublicationError) as caught:
                    publisher.publish(
                        prepared,
                        push_environment=push_environment,
                    )

            rendered = str(caught.exception)
            self.assertEqual(caught.exception.code, IssueCode.RUNNER_OPERATION_FAILED)
            self.assertNotIn("DO_NOT_EXPOSE", rendered)
            self.assertNotIn("provider response body", rendered)
            push_call = next(
                call
                for call in run.call_args_list
                if call.args[0][1] == "push"
            )
            self.assertEqual(
                push_call.kwargs["env"]["TEST_PUSH_TOKEN"],
                "DO_NOT_EXPOSE",
            )
            self.assertGreater(float(push_call.kwargs["timeout"]), 0)
            clone_call = next(
                call
                for call in run.call_args_list
                if call.args[0][1] == "clone"
            )
            self.assertNotIn("TEST_PUSH_TOKEN", clone_call.kwargs["env"])

    def test_unissued_prepared_value_cannot_bypass_tree_and_parent_checks(self) -> None:
        """`unissued_prepared_value` 관련 경계 조건 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            _, remote, candidate, base_head, base_tree = _init_repositories(Path(tmp))
            (candidate / "tracked.txt").write_text("candidate\n", encoding="utf-8")
            _git(candidate, "add", "tracked.txt")
            verified_tree = _git(candidate, "write-tree")
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )
            forged_commit = subprocess.run(
                ["git", "commit-tree", verified_tree, "-p", base_head],
                cwd=candidate,
                env=_environment(),
                input="forged candidate\n",
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            forged = PreparedPublication(
                base_head=base_head,
                base_tree=base_tree,
                remote_ref=_TARGET_REF,
                verified_tree=verified_tree,
                commit_oid=forged_commit,
                seal="0" * 64,
            )

            self.assertEqual(
                _git(candidate, "rev-parse", f"{forged_commit}^{{tree}}"),
                verified_tree,
            )
            self.assertEqual(
                _git(candidate, "show", "-s", "--format=%P", forged_commit),
                base_head,
            )

            with self.assertRaises(PublicationError) as caught:
                publisher.publish(forged, push_environment=_environment())

            self.assertEqual(caught.exception.code, IssueCode.VERIFIED_TREE_MISMATCH)
            self.assertEqual(_remote_oid(remote), base_head)

    def test_expired_deadline_starts_no_git_subprocess(self) -> None:
        """`expired_deadline_starts_no_git_subprocess` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            _, remote, candidate, base_head, base_tree = _init_repositories(Path(tmp))
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
                remaining_seconds=lambda: 0.0,
            )

            with patch("sync.runtime.publication.run_process_tree") as run:
                with self.assertRaises(PublicationError) as caught:
                    publisher.prepare(
                        verified_tree=base_tree,
                        commit_message="docs: publish translations",
                    )

            self.assertEqual(
                caught.exception.code,
                IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            )
            run.assert_not_called()

    def test_push_timeout_is_a_workflow_deadline_failure(self) -> None:
        """`push_timeout`의 워크플로 기한 실패 판정 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            _, remote, candidate, base_head, base_tree = _init_repositories(Path(tmp))
            (candidate / "tracked.txt").write_text("candidate\n", encoding="utf-8")
            _git(candidate, "add", "tracked.txt")
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )
            prepared = publisher.prepare(
                verified_tree=_git(candidate, "write-tree"),
                commit_message="docs: publish translations",
            )

            real_run = subprocess.run

            def timeout_only_push(*args: object, **kwargs: object):
                """timeout only push 처리."""

                argv = args[0]
                if _is_push_argv(argv):
                    raise subprocess.TimeoutExpired(["git", "push"], 15)
                return real_run(*args, **kwargs)

            with patch(
                "sync.runtime.publication.run_process_tree",
                side_effect=timeout_only_push,
            ):
                with self.assertRaises(PublicationError) as caught:
                    publisher.publish(
                        prepared,
                        push_environment=_environment(),
                    )

            self.assertEqual(
                caught.exception.code,
                IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            )
            self.assertIsNone(caught.exception.published_commit)
            self.assertIsNone(caught.exception.__cause__)

    def test_timeout_after_server_update_reports_published_commit(self) -> None:
        """`timeout_after_server_update_reports_published_commit` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            _, remote, candidate, base_head, base_tree = _init_repositories(Path(tmp))
            (candidate / "tracked.txt").write_text("candidate\n", encoding="utf-8")
            _git(candidate, "add", "tracked.txt")
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )
            prepared = publisher.prepare(
                verified_tree=_git(candidate, "write-tree"),
                commit_message="docs: publish translations",
            )
            real_run = subprocess.run

            def publish_then_timeout(*args: object, **kwargs: object):
                """publish then timeout 처리."""

                argv = args[0]
                if _is_push_argv(argv):
                    completed = real_run(*args, **kwargs)
                    self.assertEqual(completed.returncode, 0)
                    raise subprocess.TimeoutExpired(argv, kwargs["timeout"])
                return real_run(*args, **kwargs)

            with patch(
                "sync.runtime.publication.run_process_tree",
                side_effect=publish_then_timeout,
            ):
                with self.assertRaises(PublicationError) as caught:
                    publisher.publish(prepared, push_environment=_environment())

            self.assertEqual(
                caught.exception.code,
                IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            )
            self.assertEqual(caught.exception.published_commit, prepared.commit_oid)
            self.assertEqual(_remote_oid(remote), prepared.commit_oid)

    def test_cleanup_error_after_server_update_reports_published_commit(self) -> None:
        """`cleanup_error_after_server_update`의 published 커밋 보고 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            _, remote, candidate, base_head, base_tree = _init_repositories(Path(tmp))
            (candidate / "tracked.txt").write_text("candidate\n", encoding="utf-8")
            _git(candidate, "add", "tracked.txt")
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )
            prepared = publisher.prepare(
                verified_tree=_git(candidate, "write-tree"),
                commit_message="docs: publish translations",
            )
            real_run = subprocess.run

            def publish_then_fail_cleanup(*args: object, **kwargs: object):
                """publish then fail cleanup 처리."""

                argv = args[0]
                if _is_push_argv(argv):
                    completed = real_run(*args, **kwargs)
                    self.assertEqual(completed.returncode, 0)
                    raise ProcessTreeCleanupError("private cleanup detail")
                return real_run(*args, **kwargs)

            with patch(
                "sync.runtime.publication.run_process_tree",
                side_effect=publish_then_fail_cleanup,
            ):
                with self.assertRaises(PublicationError) as caught:
                    publisher.publish(prepared, push_environment=_environment())

            self.assertEqual(
                caught.exception.code,
                IssueCode.RUNNER_OPERATION_FAILED,
            )
            self.assertEqual(caught.exception.published_commit, prepared.commit_oid)
            self.assertEqual(_remote_oid(remote), prepared.commit_oid)
            self.assertNotIn("private", str(caught.exception))

    def test_nonzero_after_server_update_reports_published_commit(self) -> None:
        """`nonzero_after_server_update_reports_published_commit` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            _, remote, candidate, base_head, base_tree = _init_repositories(Path(tmp))
            (candidate / "tracked.txt").write_text("candidate\n", encoding="utf-8")
            _git(candidate, "add", "tracked.txt")
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )
            prepared = publisher.prepare(
                verified_tree=_git(candidate, "write-tree"),
                commit_message="docs: publish translations",
            )
            real_run = subprocess.run

            def publish_then_report_failure(*args: object, **kwargs: object):
                """publish then 보고서 실패 처리."""

                argv = args[0]
                if _is_push_argv(argv):
                    completed = real_run(*args, **kwargs)
                    self.assertEqual(completed.returncode, 0)
                    return subprocess.CompletedProcess(
                        argv,
                        1,
                        stdout=b"",
                        stderr=b"sensitive transport details",
                    )
                return real_run(*args, **kwargs)

            with patch(
                "sync.runtime.publication.run_process_tree",
                side_effect=publish_then_report_failure,
            ):
                with self.assertRaises(PublicationError) as caught:
                    publisher.publish(prepared, push_environment=_environment())

            self.assertEqual(caught.exception.code, IssueCode.RUNNER_OPERATION_FAILED)
            self.assertEqual(caught.exception.published_commit, prepared.commit_oid)
            self.assertNotIn("sensitive", str(caught.exception))
            self.assertEqual(_remote_oid(remote), prepared.commit_oid)

    def test_temporary_directory_creation_failure_is_a_runner_failure(self) -> None:
        """`temporary_directory_creation_failure`의 runner 실패 판정 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            _, remote, candidate, base_head, base_tree = _init_repositories(Path(tmp))
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )
            prepared = publisher.prepare(
                verified_tree=base_tree,
                commit_message="docs: publish translations",
            )

            with patch(
                "sync.runtime.publication.tempfile.TemporaryDirectory",
                side_effect=OSError("sensitive temporary path"),
            ):
                with self.assertRaises(PublicationError) as caught:
                    publisher.publish(prepared, push_environment=_environment())

            self.assertEqual(caught.exception.code, IssueCode.RUNNER_OPERATION_FAILED)
            self.assertIsNone(caught.exception.published_commit)
            self.assertNotIn("sensitive", str(caught.exception))

    def test_cleanup_failure_after_success_preserves_published_commit(self) -> None:
        """`cleanup_failure_after_success`의 published 커밋 보존 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            _, remote, candidate, base_head, base_tree = _init_repositories(Path(tmp))
            (candidate / "tracked.txt").write_text("candidate\n", encoding="utf-8")
            _git(candidate, "add", "tracked.txt")
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )
            prepared = publisher.prepare(
                verified_tree=_git(candidate, "write-tree"),
                commit_message="docs: publish translations",
            )
            real_temporary_directory = tempfile.TemporaryDirectory

            class CleanupFailure:
                """cleanup 실패 정보."""

                def __init__(self, *args: object, **kwargs: object) -> None:
                    """cleanup 실패 초기화."""

                    self._temporary = real_temporary_directory(*args, **kwargs)
                    self.name = self._temporary.name

                def cleanup(self) -> None:
                    """정리."""

                    self._temporary.cleanup()
                    raise OSError("sensitive cleanup path")

            with patch(
                "sync.runtime.publication.tempfile.TemporaryDirectory",
                CleanupFailure,
            ):
                with self.assertRaises(PublicationError) as caught:
                    publisher.publish(prepared, push_environment=_environment())

            self.assertEqual(caught.exception.code, IssueCode.RUNNER_OPERATION_FAILED)
            self.assertEqual(caught.exception.published_commit, prepared.commit_oid)
            self.assertEqual(_remote_oid(remote), prepared.commit_oid)
            self.assertNotIn("sensitive", str(caught.exception))

    def test_cleanup_failure_preserves_prior_published_failure_state(self) -> None:
        """`cleanup_failure`의 prior published 실패 상태 보존 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            _, remote, candidate, base_head, base_tree = _init_repositories(Path(tmp))
            (candidate / "tracked.txt").write_text("candidate\n", encoding="utf-8")
            _git(candidate, "add", "tracked.txt")
            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
            )
            prepared = publisher.prepare(
                verified_tree=_git(candidate, "write-tree"),
                commit_message="docs: publish translations",
            )
            real_run = subprocess.run
            real_temporary_directory = tempfile.TemporaryDirectory

            def publish_then_timeout(*args: object, **kwargs: object):
                """publish then timeout 처리."""

                argv = args[0]
                if _is_push_argv(argv):
                    completed = real_run(*args, **kwargs)
                    self.assertEqual(completed.returncode, 0)
                    raise subprocess.TimeoutExpired(argv, kwargs["timeout"])
                return real_run(*args, **kwargs)

            class CleanupFailure:
                """cleanup 실패 정보."""

                def __init__(self, *args: object, **kwargs: object) -> None:
                    """cleanup 실패 초기화."""

                    self._temporary = real_temporary_directory(*args, **kwargs)
                    self.name = self._temporary.name

                def cleanup(self) -> None:
                    """정리."""

                    self._temporary.cleanup()
                    raise OSError("sensitive cleanup path")

            with (
                patch(
                    "sync.runtime.publication.run_process_tree",
                    side_effect=publish_then_timeout,
                ),
                patch(
                    "sync.runtime.publication.tempfile.TemporaryDirectory",
                    CleanupFailure,
                ),
            ):
                with self.assertRaises(PublicationError) as caught:
                    publisher.publish(prepared, push_environment=_environment())

            self.assertEqual(caught.exception.code, IssueCode.RUNNER_OPERATION_FAILED)
            self.assertEqual(caught.exception.published_commit, prepared.commit_oid)
            self.assertEqual(_remote_oid(remote), prepared.commit_oid)
            self.assertNotIn("sensitive", str(caught.exception))

    def test_no_change_rechecks_deadline_after_state_readers(self) -> None:
        """`no_change_rechecks_deadline_after_state_readers` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            _, remote, candidate, base_head, base_tree = _init_repositories(Path(tmp))
            remaining = [30.0]

            def exhaust_deadline(_timeout: float) -> str:
                """exhaust 기한 처리."""

                remaining[0] = 0.0
                return "active-v1"

            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
                read_active_fingerprint=exhaust_deadline,
                remaining_seconds=lambda: remaining[0],
            )
            prepared = publisher.prepare(
                verified_tree=base_tree,
                commit_message="docs: publish translations",
            )

            with self.assertRaises(PublicationError) as caught:
                publisher.publish(prepared, push_environment=_environment())

            self.assertEqual(
                caught.exception.code,
                IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
            )

    def test_state_reader_failure_does_not_chain_sensitive_exception_text(self) -> None:
        """`state_reader_failure`의 않음 chain sensitive exception text 동작 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            _, remote, candidate, base_head, base_tree = _init_repositories(Path(tmp))

            def fail_with_sensitive_text(_timeout: float) -> str:
                """테스트용 with sensitive text 대체 동작."""

                raise RuntimeError("api_key=DO_NOT_EXPOSE")

            publisher = _publisher(
                candidate=candidate,
                remote=remote,
                base_head=base_head,
                base_tree=base_tree,
                read_active_fingerprint=fail_with_sensitive_text,
            )
            prepared = publisher.prepare(
                verified_tree=base_tree,
                commit_message="docs: publish translations",
            )

            with self.assertRaises(PublicationError) as caught:
                publisher.publish(prepared, push_environment=_environment())

            self.assertEqual(caught.exception.code, IssueCode.RUNNER_OPERATION_FAILED)
            self.assertNotIn("DO_NOT_EXPOSE", str(caught.exception))
            self.assertIsNone(caught.exception.__cause__)


if __name__ == "__main__":
    unittest.main()
