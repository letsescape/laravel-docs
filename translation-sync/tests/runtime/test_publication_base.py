"""게시 기준본 동작과 경계 조건 검증."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sync.runtime.base import (
    RepositoryStateError,
    active_repository_fingerprint,
    capture_publication_base,
    read_remote_ref_oid,
)
from sync.runtime.failure import IssueCode
from sync.runtime.process import ProcessTreeCleanupError


def _git(repo: Path, *args: str) -> str:
    """Git 명령 실행."""

    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _repositories(root: Path) -> tuple[Path, Path, str]:
    """테스트용 활성·원격 저장소 초기화."""

    active = root / "active"
    remote = root / "remote.git"
    active.mkdir()
    _git(active, "init", "--quiet", "--initial-branch=main")
    _git(active, "config", "user.name", "Base Tests")
    _git(active, "config", "user.email", "base-tests@localhost")
    (active / "tracked.txt").write_text("approved\n", encoding="utf-8")
    _git(active, "add", "tracked.txt")
    _git(active, "commit", "--quiet", "-m", "approved")
    remote.mkdir()
    _git(remote, "init", "--quiet", "--bare")
    _git(remote, "symbolic-ref", "HEAD", "refs/heads/main")
    _git(active, "remote", "add", "origin", str(remote))
    _git(active, "push", "--quiet", "origin", "HEAD:refs/heads/main")
    return active, remote, _git(active, "rev-parse", "HEAD")


class PublicationBaseTests(unittest.TestCase):
    """게시 기준본 동작과 경계 조건 테스트 모음."""

    def test_process_tree_failure_is_a_runner_failure(self) -> None:
        """프로세스 트리 실패의 실행기 실패 판정 검증."""

        with tempfile.TemporaryDirectory() as tmp, patch(
            "sync.runtime.base.run_process_tree",
            side_effect=ProcessTreeCleanupError("private cleanup detail"),
        ):
            with self.assertRaises(RepositoryStateError) as caught:
                read_remote_ref_oid(
                    Path(tmp),
                    remote="origin",
                    remote_ref="refs/heads/main",
                    remaining_seconds=lambda: 17.5,
                )

        self.assertEqual(
            caught.exception.code,
            IssueCode.RUNNER_OPERATION_FAILED,
        )

    def test_git_subprocess_receives_only_read_only_environment(self) -> None:
        """Git 하위 프로세스에 읽기 전용 환경만 전달하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            source_environment = {
                "PATH": "/safe/bin",
                "LANG": "ko_KR.UTF-8",
                "LANGUAGE": "ko_KR:en",
                "LC_CTYPE": "ko_KR.UTF-8",
                "HTTPS_PROXY": "https://proxy.example",
                "http_proxy": "http://proxy.example",
                "NO_PROXY": "localhost",
                "SSL_CERT_FILE": "/certs/ca.pem",
                "SSL_CERT_DIR": "/certs",
                "CURL_CA_BUNDLE": "/certs/curl.pem",
                "GIT_SSL_CAINFO": "/certs/git.pem",
                "GIT_SSL_CAPATH": "/certs/git",
                "SYSTEMROOT": "C:\\Windows",
                "TMPDIR": "/safe/tmp",
                "HOME": "/private/home",
                "XDG_CONFIG_HOME": "/private/xdg",
                "GIT_CONFIG_GLOBAL": "/private/gitconfig",
                "GIT_CONFIG_SYSTEM": "/private/system-gitconfig",
                "GIT_CONFIG_COUNT": "9",
                "GIT_CONFIG_KEY_0": "credential.helper",
                "GIT_CONFIG_VALUE_0": "credential-helper",
                "GIT_ASKPASS": "/private/askpass",
                "SSH_AUTH_SOCK": "/private/agent.sock",
                "OPENAI_API_KEY": "provider-secret",
                "AZURE_OPENAI_API_KEY": "azure-secret",
                "CODEX_API_KEY": "codex-secret",
                "GH_TOKEN": "gh-secret",
                "GITHUB_TOKEN": "github-secret",
                "UNRELATED_SECRET": "other-secret",
            }
            observed: dict[str, object] = {}

            def fake_run(*args: object, **kwargs: object):
                """Git 실행 인수 기록용 대체 동작."""

                observed.update(kwargs)
                return subprocess.CompletedProcess(
                    args=args[0],
                    returncode=0,
                    stdout=(b"a" * 40) + b"\trefs/heads/main\n",
                    stderr=b"",
                )

            with (
                patch.dict("os.environ", source_environment, clear=True),
                patch("sync.runtime.base.run_process_tree", side_effect=fake_run),
            ):
                oid = read_remote_ref_oid(
                    repo,
                    remote="origin",
                    remote_ref="refs/heads/main",
                    remaining_seconds=lambda: 17.5,
                )

            self.assertEqual(oid, "a" * 40)
            environment = observed["env"]
            assert isinstance(environment, dict)
            for name in (
                "PATH",
                "LANG",
                "LANGUAGE",
                "LC_CTYPE",
                "HTTPS_PROXY",
                "http_proxy",
                "NO_PROXY",
                "SSL_CERT_FILE",
                "SSL_CERT_DIR",
                "CURL_CA_BUNDLE",
                "GIT_SSL_CAINFO",
                "GIT_SSL_CAPATH",
                "SYSTEMROOT",
                "TMPDIR",
            ):
                self.assertEqual(environment[name], source_environment[name])
            for name in (
                "OPENAI_API_KEY",
                "AZURE_OPENAI_API_KEY",
                "CODEX_API_KEY",
                "GH_TOKEN",
                "GITHUB_TOKEN",
                "UNRELATED_SECRET",
                "SSH_AUTH_SOCK",
            ):
                self.assertNotIn(name, environment)
            self.assertEqual(environment["HOME"], "/dev/null")
            self.assertEqual(environment["XDG_CONFIG_HOME"], "/dev/null")
            self.assertEqual(environment["GIT_CONFIG_GLOBAL"], "/dev/null")
            self.assertEqual(environment["GIT_CONFIG_SYSTEM"], "/dev/null")
            self.assertEqual(environment["GIT_CONFIG_NOSYSTEM"], "1")
            self.assertEqual(environment["GIT_CONFIG_COUNT"], "1")
            self.assertEqual(environment["GIT_CONFIG_KEY_0"], "credential.helper")
            self.assertEqual(environment["GIT_CONFIG_VALUE_0"], "")
            self.assertEqual(environment["GIT_ASKPASS"], "/dev/null")
            self.assertEqual(environment["SSH_ASKPASS"], "/dev/null")
            self.assertEqual(environment["GIT_OPTIONAL_LOCKS"], "0")
            self.assertEqual(environment["GIT_TERMINAL_PROMPT"], "0")
            self.assertEqual(observed["timeout"], 17.5)
            self.assertIs(observed["shell"], False)
            self.assertIs(observed["stdin"], subprocess.DEVNULL)

    def test_captures_clean_branch_and_exact_remote_ref(self) -> None:
        """깨끗한 브랜치와 정확한 원격 참조를 캡처하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            active, _, head = _repositories(Path(tmp))

            base = capture_publication_base(
                active,
                remote="origin",
                branch="main",
                remaining_seconds=lambda: 30.0,
            )

            self.assertEqual(base.head, head)
            self.assertEqual(base.tree, _git(active, "rev-parse", "HEAD^{tree}"))
            self.assertEqual(base.remote_ref, "refs/heads/main")
            self.assertEqual(base.remote_oid, head)
            self.assertEqual(
                base.active_fingerprint,
                active_repository_fingerprint(
                    active,
                    remaining_seconds=lambda: 30.0,
                ),
            )

    def test_rejects_tracked_or_index_changes(self) -> None:
        """추적 파일 또는 인덱스 변경 거부 검증."""

        for mutation in ("worktree", "index"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                active, _, _ = _repositories(Path(tmp))
                (active / "tracked.txt").write_text("dirty\n", encoding="utf-8")
                if mutation == "index":
                    _git(active, "add", "tracked.txt")

                with self.assertRaises(RepositoryStateError) as caught:
                    capture_publication_base(
                        active,
                        remote="origin",
                        branch="main",
                        remaining_seconds=lambda: 30.0,
                    )

                self.assertEqual(
                    caught.exception.code,
                    IssueCode.DIRTY_PUBLICATION_BASE,
                )

    def test_rejects_nonignored_untracked_file_in_owned_path(self) -> None:
        """소유 경로의 무시되지 않은 미추적 파일 거부 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            active, _, _ = _repositories(Path(tmp))
            path = active / "versioned_docs/version-13.x/untracked.md"
            path.parent.mkdir(parents=True)
            path.write_text("untracked\n", encoding="utf-8")

            with self.assertRaises(RepositoryStateError) as caught:
                capture_publication_base(
                    active,
                    remote="origin",
                    branch="main",
                    remaining_seconds=lambda: 30.0,
                )

            self.assertEqual(caught.exception.code, IssueCode.DIRTY_PUBLICATION_BASE)

    def test_unrelated_untracked_is_allowed_but_covered_by_fingerprint(self) -> None:
        """관련 없는 미추적 파일은 허용하되 지문에 포함하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            active, _, _ = _repositories(Path(tmp))
            unrelated = active / "notes.tmp"
            unrelated.write_text("one\n", encoding="utf-8")
            base = capture_publication_base(
                active,
                remote="origin",
                branch="main",
                remaining_seconds=lambda: 30.0,
            )

            unrelated.write_text("two\n", encoding="utf-8")

            self.assertNotEqual(
                base.active_fingerprint,
                active_repository_fingerprint(
                    active,
                    remaining_seconds=lambda: 30.0,
                ),
            )

    def test_rejects_detached_head_and_remote_race(self) -> None:
        """분리된 HEAD와 원격 갱신 경쟁 거부 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            active, remote, head = _repositories(root)
            _git(active, "checkout", "--detach", "--quiet", head)
            with self.assertRaises(RepositoryStateError) as detached:
                capture_publication_base(
                    active,
                    remote="origin",
                    branch="main",
                    remaining_seconds=lambda: 30.0,
                )
            self.assertEqual(detached.exception.code, IssueCode.NON_BRANCH_REF)

            _git(active, "checkout", "--quiet", "main")
            competitor = root / "competitor"
            subprocess.run(
                ["git", "clone", "--quiet", str(remote), str(competitor)],
                check=True,
            )
            _git(competitor, "config", "user.name", "Base Tests")
            _git(competitor, "config", "user.email", "base-tests@localhost")
            (competitor / "advance.txt").write_text("advance\n", encoding="utf-8")
            _git(competitor, "add", "advance.txt")
            _git(competitor, "commit", "--quiet", "-m", "advance")
            _git(competitor, "push", "--quiet", "origin", "HEAD:refs/heads/main")

            with self.assertRaises(RepositoryStateError) as advanced:
                capture_publication_base(
                    active,
                    remote="origin",
                    branch="main",
                    remaining_seconds=lambda: 30.0,
                )
            self.assertEqual(
                advanced.exception.code,
                IssueCode.PUBLICATION_BASE_CHANGED,
            )


if __name__ == "__main__":
    unittest.main()
