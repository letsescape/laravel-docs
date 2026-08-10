"""replay 동작과 경계 조건 검증."""

import base64
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import replay
from sync.runtime.candidate import SYNC_FAILURE_REPORT_FILENAME
from sync.runtime.settings import WorkflowSettings


def _manifest_bytes() -> bytes:
    """두 version을 가리키는 정규 manifest byte 생성."""

    return (
        '{"schema_version":1,"entries":['
        '{"version":"master","repository":"https://github.com/laravel/docs.git",'
        '"object_format":"sha1","commit":"' + "a" * 40 + '"},'
        '{"version":"13.x","repository":"https://github.com/laravel/docs.git",'
        '"object_format":"sha1","commit":"' + "b" * 40 + '"}]}'
        "\n"
    ).encode("utf-8")


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """테스트 저장소에서 Git 명령 실행."""

    return subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )


def _init_repo(root: Path, main_source: str) -> None:
    """Replay 입력으로 사용할 최소 Git 저장소 초기화."""

    (root / "translation-sync").mkdir()
    (root / "translation-sync/main.py").write_text(main_source, encoding="utf-8")
    (root / "tracked.txt").write_text("original\n", encoding="utf-8")
    (root / "deleted.txt").write_text("delete me\n", encoding="utf-8")
    (root / "versions.json").write_text(
        '["master","13.x"]\n',
        encoding="utf-8",
    )
    _git(root, "init", "--quiet")
    _git(root, "config", "user.name", "Replay Tests")
    _git(root, "config", "user.email", "replay-tests@localhost")
    _git(root, "add", "-A")
    _git(root, "commit", "--quiet", "-m", "fixture")


def _replay_workflow_settings(
    *,
    workflow_timeout_seconds: int = 3600,
    setup_commands: tuple[tuple[str, ...], ...] | None = None,
    sync_core_command: tuple[str, ...] | None = None,
    site_commands: tuple[tuple[str, ...], ...] | None = None,
    path_command: tuple[str, ...] | None = None,
) -> WorkflowSettings:
    """Replay 테스트에 필요한 최소 워크플로 설정 구성."""

    no_op = (sys.executable, "-c", "raise SystemExit(0)")
    return WorkflowSettings(
        workflow_timeout_seconds=workflow_timeout_seconds,
        unit_test_command=no_op,
        replay_command=no_op,
        provider_fixture_command=no_op,
        candidate_setup_commands=setup_commands or (no_op,),
        sync_core_command=sync_core_command
        or (sys.executable, "translation-sync/main.py"),
        site_validation_commands=site_commands
        or (no_op, no_op, no_op, no_op),
        path_validation_command=path_command or no_op,
        deploy_workflow="deploy.yml",
    )


class TranslationReplayTests(unittest.TestCase):
    """번역 replay 동작과 경계 조건 테스트 모음."""

    def setUp(self) -> None:
        """테스트 사전 상태 구성."""

        manifest_environment = patch.dict(
            os.environ,
            {
                replay.MANIFEST_ENV: "",
                replay.FAILURE_REPORT_ENV: "",
                replay.RUN_ID_ENV: "",
                "TRANSLATION_WORKFLOW_DEADLINE_MONOTONIC": str(
                    time.monotonic() + 3600
                ),
            },
        )
        manifest_environment.start()
        self.addCleanup(manifest_environment.stop)
        manifest_resolver = patch.object(
            replay.upstream,
            "resolve_manifest",
            return_value=_manifest_bytes(),
        )
        self.resolve_manifest = manifest_resolver.start()
        self.addCleanup(manifest_resolver.stop)
        workflow_settings = patch.object(
            replay,
            "load_workflow_settings",
            return_value=_replay_workflow_settings(),
        )
        self.load_workflow_settings = workflow_settings.start()
        self.addCleanup(workflow_settings.stop)

    def test_invalid_or_expired_workflow_deadline_is_rejected_before_setup(
        self,
    ) -> None:
        """잘못되거나 만료된 공통 기한이 sandbox 준비 전에 거부되는지 검증."""

        for deadline, expected in (
            ("not-a-number", replay.EXIT_SYNC_FAILED),
            ("nan", replay.EXIT_SYNC_FAILED),
            (str(time.monotonic() - 1), replay.EXIT_REPLAY_ERROR),
        ):
            with self.subTest(deadline=deadline), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / "repo"
                root.mkdir()
                _init_repo(root, "raise SystemExit(0)\n")
                sandboxes = Path(tmp) / "sandboxes"
                self.resolve_manifest.reset_mock()

                with patch.dict(
                    os.environ,
                    {"TRANSLATION_WORKFLOW_DEADLINE_MONOTONIC": deadline},
                ):
                    result = replay.run_replay(
                        repo_root=root,
                        sandbox_parent=sandboxes,
                    )

                self.assertEqual(result, expected)
                self.assertFalse(sandboxes.exists())
                self.resolve_manifest.assert_not_called()

    def test_setup_interrupt_preserves_signal_convention(self) -> None:
        """준비 중 interrupt가 일반 종료 코드로 변환되지 않는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"

            with patch.object(
                replay,
                "load_versions",
                side_effect=KeyboardInterrupt,
            ):
                with self.assertRaises(KeyboardInterrupt):
                    replay.run_replay(
                        repo_root=root,
                        sandbox_parent=sandboxes,
                    )

            self.assertFalse(sandboxes.exists())

    def test_command_error_does_not_include_arguments_or_stderr_paths(self) -> None:
        """하위 명령 오류가 인자와 stderr 경로를 노출하지 않는지 검증."""

        exposed_path = "/artifact/translation-replay-secret/private-output"
        error = subprocess.CalledProcessError(
            1,
            ["git", "status", exposed_path],
            stderr=exposed_path.encode(),
        )

        with patch.object(replay, "_PROCESS_RUNNER", side_effect=error):
            with self.assertRaises(replay.ReplayError) as raised:
                replay._command(  # noqa: SLF001
                    ["git", "status", exposed_path],
                    cwd=Path("."),
                )

        self.assertNotIn(exposed_path, str(raised.exception))

    def test_all_replay_subprocesses_use_the_same_remaining_deadline(self) -> None:
        """모든 replay 하위 프로세스가 같은 절대 기한을 공유하는지 검증."""

        main_source = """\
import os
import time

deadline = float(os.environ["TRANSLATION_WORKFLOW_DEADLINE_MONOTONIC"])
raise SystemExit(0 if deadline > time.monotonic() else 9)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"
            deadline = time.monotonic() + 60
            observed_timeouts: list[float | None] = []
            real_run = replay._PROCESS_RUNNER  # noqa: SLF001

            def observe_timeout(*args: object, **kwargs: object):
                """전달된 timeout을 기록하고 실제 하위 명령 실행."""

                observed_timeouts.append(kwargs.get("timeout"))
                return real_run(*args, **kwargs)

            with patch.dict(
                os.environ,
                {"TRANSLATION_WORKFLOW_DEADLINE_MONOTONIC": str(deadline)},
            ), patch.object(
                replay,
                "_PROCESS_RUNNER",
                side_effect=observe_timeout,
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_OK)
            self.assertTrue(observed_timeouts)
            self.assertTrue(
                all(
                    timeout is not None and 0 < timeout <= 60
                    for timeout in observed_timeouts
                )
            )

    def test_standalone_replay_starts_one_deadline_from_workflow_settings(self) -> None:
        """독립 replay가 워크플로 설정에서 기한을 한 번만 시작하는지 검증."""

        main_source = """\
import os
import time

deadline = float(os.environ["TRANSLATION_WORKFLOW_DEADLINE_MONOTONIC"])
raise SystemExit(0 if deadline > time.monotonic() else 9)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"

            with patch.dict(os.environ, {}, clear=False):
                os.environ.pop(replay.WORKFLOW_DEADLINE_ENV, None)
                with patch.object(
                    replay,
                    "load_workflow_settings",
                    return_value=_replay_workflow_settings(
                        workflow_timeout_seconds=60
                    ),
                ) as load_settings:
                    result = replay.run_replay(
                        repo_root=root,
                        sandbox_parent=sandboxes,
                    )

            self.assertEqual(result, replay.EXIT_OK)
            load_settings.assert_called_once_with(
                root.resolve() / "translation-sync/workflow.json"
            )

    def test_selector_is_canonical_utf8_json_and_allows_nested_documents(self) -> None:
        """중첩 문서 selector가 정규 UTF-8 JSON으로 생성되는지 검증."""

        selector = replay.normalize_selector(
            version="13.x",
            doc="guides/cafe\u0301.md",
            supported_versions=["master", "13.x"],
        )

        self.assertEqual(
            selector,
            '{"document":"guides/café.md","version":"13.x"}\n'.encode(),
        )

    def test_empty_selector_is_canonical_json_with_null_values(self) -> None:
        """빈 selector가 null 값을 가진 정규 JSON인지 검증."""

        self.assertEqual(
            replay.normalize_selector(
                version=None,
                doc=None,
                supported_versions=["master", "13.x"],
            ),
            b'{"document":null,"version":null}\n',
        )

    def test_cli_accepts_external_artifact_root(self) -> None:
        """CLI가 저장소 외부 artifact root를 전달하는지 검증."""

        with patch.object(
            replay.sys,
            "argv",
            ["replay.py", "--artifact-root", "/tmp/replay-artifacts"],
        ):
            args = replay._parse_args()  # noqa: SLF001

        self.assertEqual(args.artifact_root, Path("/tmp/replay-artifacts"))

    def test_selector_rejects_noncanonical_or_unsafe_paths(self) -> None:
        """비정규 또는 저장소 탈출 가능성이 있는 문서 selector 거부 검증."""

        for document in (
            "",
            "/guide.md",
            "guides//guide.md",
            "guides/./guide.md",
            "guides/../guide.md",
            "guides\\guide.md",
            "guide.md\0ignored",
            "guide.txt",
        ):
            with self.subTest(document=document), self.assertRaises(
                replay.ReplayInputError
            ):
                replay.normalize_selector(
                    version="13.x",
                    doc=document,
                    supported_versions=["master", "13.x"],
                )

        with self.assertRaises(replay.ReplayInputError):
            replay.normalize_selector(
                version=None,
                doc="guide.md",
                supported_versions=["master", "13.x"],
            )
        with self.assertRaises(replay.ReplayInputError):
            replay.normalize_selector(
                version="12.x",
                doc=None,
                supported_versions=["master", "13.x"],
            )

        for version, document in ((13, None), ("13.x", 13)):
            with self.subTest(
                version=version,
                document=document,
            ), self.assertRaises(replay.ReplayInputError):
                replay.normalize_selector(
                    version=version,  # type: ignore[arg-type]
                    doc=document,  # type: ignore[arg-type]
                    supported_versions=["master", "13.x"],
                )

    def test_unsafe_selector_is_rejected_before_manifest_resolution(self) -> None:
        """안전하지 않은 selector가 manifest 해석보다 먼저 거부되는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"
            sandboxes.mkdir()
            report_path = sandboxes / "failure.json"

            with patch.dict(
                os.environ,
                {
                    replay.FAILURE_REPORT_ENV: str(report_path),
                    replay.RUN_ID_ENV: "run-invalid-selector",
                },
            ):
                result = replay.run_replay(
                    repo_root=root,
                    version="13.x",
                    doc="guides/../secrets.md",
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.resolve_manifest.assert_not_called()
            self.assertEqual(
                json.loads(report_path.read_bytes())["code"],
                "INVALID_SELECTOR",
            )
            self.assertEqual(
                [path.name for path in sandboxes.iterdir()],
                ["failure.json"],
            )

    def test_both_replay_processes_receive_the_same_manifest_and_selector(self) -> None:
        """두 replay pass가 동일한 manifest와 selector를 받는지 검증."""

        main_source = """\
import hashlib
import os
from pathlib import Path

root = Path(__file__).resolve().parent.parent
manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"])
manifest_bytes = manifest.read_bytes()
selector = os.environ["TRANSLATION_SELECTOR_JSON"].encode("utf-8")
contract = (
    hashlib.sha256(manifest_bytes).hexdigest(),
    os.environ["TRANSLATION_UPSTREAM_MANIFEST_DIGEST"],
    selector,
    os.environ["TRANSLATION_SELECTOR_DIGEST"],
)
expected = (
    contract[0] == contract[1]
    and hashlib.sha256(selector).hexdigest() == contract[3]
    and selector == b'{"document":"guides/caf\\xc3\\xa9.md","version":"13.x"}\\n'
    and manifest.stat().st_mode & 0o222 == 0
)
record = root / ".git/replay-contract"
serialized = repr(contract)
if record.exists():
    expected = expected and record.read_text(encoding="utf-8") == serialized
else:
    record.write_text(serialized, encoding="utf-8")
raise SystemExit(0 if expected else 9)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(
                repo_root=root,
                version="13.x",
                doc="guides/cafe\u0301.md",
                sandbox_parent=sandboxes,
            )

            self.assertEqual(result, replay.EXIT_OK)
            self.assertEqual(list(sandboxes.iterdir()), [])

    def test_both_passes_run_full_candidate_pipeline_in_order(self) -> None:
        """두 pass가 전체 candidate pipeline을 정의된 순서로 실행하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(99)\n")
            artifact_root = Path(tmp) / "artifacts"
            artifact_root.mkdir()
            stage_log = artifact_root / "stage.log"

            def stage_command(label: str, body: str = "") -> tuple[str, ...]:
                """Candidate 단계 명령을 실행 순서에 기록."""

                script = (
                    "from pathlib import Path; "
                    f"log = Path({str(stage_log)!r}); "
                    f"log.write_text(log.read_text() + {label!r} + '\\n' "
                    "if log.exists() else "
                    f"{label!r} + '\\n', encoding='utf-8'); "
                    + body
                )
                return (sys.executable, "-c", script)

            settings = _replay_workflow_settings(
                setup_commands=(stage_command("setup"),),
                sync_core_command=stage_command(
                    "sync",
                    "document = Path('tracked.txt'); "
                    "current = document.read_text(encoding='utf-8'); "
                    "assert current in {'original\\n', 'candidate\\n'}; "
                    "document.write_text('candidate\\n', encoding='utf-8') "
                    "if current == 'original\\n' else None",
                ),
                site_commands=tuple(
                    stage_command(f"site-{index}") for index in range(1, 5)
                ),
                path_command=stage_command("path"),
            )
            committed_trees: list[tuple[str, str]] = []

            def record_verified_commit(
                sandbox: Path,
                *,
                verified_tree: str,
                parent_commit: str,
            ) -> str:
                """첫 pass의 봉인된 tree 연결을 실행 순서에 기록."""

                commit = real_commit(
                    sandbox,
                    verified_tree=verified_tree,
                    parent_commit=parent_commit,
                )
                committed_tree = _git(
                    sandbox,
                    "rev-parse",
                    f"{commit}^{{tree}}",
                ).stdout.strip()
                committed_trees.append((verified_tree, committed_tree))
                return commit

            real_commit = replay._commit_verified_candidate  # noqa: SLF001
            with patch.object(
                replay,
                "load_workflow_settings",
                return_value=settings,
            ) as load_settings, patch.object(
                replay,
                "_commit_verified_candidate",
                side_effect=record_verified_commit,
            ):
                result = replay.run_replay(
                    repo_root=root,
                    artifact_root=artifact_root,
                )

            self.assertEqual(result, replay.EXIT_OK)
            self.assertEqual(
                stage_log.read_text(encoding="utf-8").splitlines(),
                [
                    "setup",
                    "sync",
                    "site-1",
                    "site-2",
                    "site-3",
                    "site-4",
                    "path",
                    "setup",
                    "sync",
                    "site-1",
                    "site-2",
                    "site-3",
                    "site-4",
                    "path",
                ],
            )
            self.assertEqual(len(committed_trees), 1)
            self.assertEqual(committed_trees[0][0], committed_trees[0][1])
            load_settings.assert_called_once_with(
                root.resolve() / "translation-sync/workflow.json"
            )
            self.assertFalse(
                any(path.is_dir() for path in artifact_root.iterdir())
            )

    def test_candidate_validator_mutation_stops_before_second_pass(self) -> None:
        """Validator가 candidate를 변경하면 두 번째 pass 전에 중단되는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(99)\n")
            artifact_root = Path(tmp) / "artifacts"
            artifact_root.mkdir()
            report_path = artifact_root / "replay-failure.json"
            stage_log = artifact_root / "stage.log"

            def stage_command(label: str, body: str = "") -> tuple[str, ...]:
                """Candidate 단계 명령을 기록하고 선택적으로 tree 변경."""

                return (
                    sys.executable,
                    "-c",
                    "from pathlib import Path; "
                    f"log = Path({str(stage_log)!r}); "
                    f"log.write_text(log.read_text() + {label!r} + '\\n' "
                    "if log.exists() else "
                    f"{label!r} + '\\n', encoding='utf-8'); "
                    + body,
                )

            settings = _replay_workflow_settings(
                setup_commands=(stage_command("setup"),),
                sync_core_command=stage_command(
                    "sync",
                    "Path('tracked.txt').write_text('candidate\\n')",
                ),
                site_commands=(
                    stage_command(
                        "site-1",
                        "Path('tracked.txt').write_text('validator mutation\\n')",
                    ),
                    stage_command("site-2"),
                    stage_command("site-3"),
                    stage_command("site-4"),
                ),
                path_command=stage_command("path"),
            )

            with patch.dict(
                os.environ,
                {
                    replay.FAILURE_REPORT_ENV: str(report_path),
                    replay.RUN_ID_ENV: "run-candidate-mutation",
                },
            ), patch.object(
                replay,
                "load_workflow_settings",
                return_value=settings,
            ):
                result = replay.run_replay(
                    repo_root=root,
                    artifact_root=artifact_root,
                )

            report = json.loads(report_path.read_bytes())
            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertEqual(report["code"], "CANDIDATE_SOURCE_MUTATED")
            self.assertEqual(
                stage_log.read_text(encoding="utf-8").splitlines(),
                ["setup", "sync", "site-1"],
            )
            self.assertTrue(report["candidate_debug_path"])

    def test_manifest_change_after_first_process_prevents_second_process(self) -> None:
        """첫 pass 뒤 manifest 변경이 두 번째 pass를 차단하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            call_log = Path(tmp) / "manifest-mutation-calls"
            main_source = f"""\
import os
from pathlib import Path

manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"])
call_log = Path({str(call_log)!r})
calls = call_log.read_text(encoding="utf-8") if call_log.exists() else ""
call_log.write_text(calls + "sync\\n", encoding="utf-8")
manifest.chmod(0o600)
manifest.write_text("changed\\n", encoding="utf-8")
raise SystemExit(0)
"""
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertEqual(
                call_log.read_text(encoding="utf-8").splitlines(),
                ["sync"],
            )
            self.assertEqual(
                len(
                    list(
                        sandboxes.glob(
                            "replay-pass-1/translation-candidate-*"
                        )
                    )
                ),
                1,
            )

    def test_missing_external_manifest_is_exported_only_after_sandbox_replay(
        self,
    ) -> None:
        """새 외부 manifest가 sandbox replay 성공 뒤에만 생성되는지 검증."""

        digest = hashlib.sha256(_manifest_bytes()).hexdigest()
        main_source = f"""\
import hashlib
import os
from pathlib import Path

root = Path(__file__).resolve().parent.parent
manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"]).resolve()
checks = [
    manifest.is_relative_to(root),
    hashlib.sha256(manifest.read_bytes()).hexdigest() == {digest!r},
    os.environ["TRANSLATION_UPSTREAM_MANIFEST_DIGEST"] == {digest!r},
    manifest.stat().st_mode & 0o222 == 0,
]
raise SystemExit(0 if all(checks) else 9)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"
            external_manifest = Path(tmp) / "outputs/upstream-refs.json"

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(external_manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_OK)
            self.assertEqual(
                external_manifest.read_bytes(),
                _manifest_bytes(),
            )
            self.assertEqual(list(sandboxes.iterdir()), [])

    def test_success_exports_canonical_machine_readable_replay_state(self) -> None:
        """성공 시 기계 판독 가능한 정규 replay 상태를 내보내는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "artifacts/sandboxes"
            state_output = Path(tmp) / "artifacts/replay-state.json"

            result = replay.run_replay(
                repo_root=root,
                version="13.x",
                doc="guides/cafe\u0301.md",
                sandbox_parent=sandboxes,
                state_output=state_output,
            )

            raw_state = state_output.read_bytes()
            state = json.loads(raw_state)
            manifest = base64.b64decode(
                state["manifest_base64"],
                validate=True,
            )
            selector = base64.b64decode(
                state["selector_base64"],
                validate=True,
            )
            self.assertEqual(result, replay.EXIT_OK)
            self.assertEqual(
                tuple(state),
                (
                    "schema_version",
                    "manifest_base64",
                    "manifest_digest",
                    "selector_base64",
                    "selector_digest",
                ),
            )
            self.assertEqual(manifest, _manifest_bytes())
            self.assertEqual(
                state["manifest_digest"],
                hashlib.sha256(manifest).hexdigest(),
            )
            self.assertEqual(
                selector,
                '{"document":"guides/café.md","version":"13.x"}\n'.encode(),
            )
            self.assertEqual(
                state["selector_digest"],
                hashlib.sha256(selector).hexdigest(),
            )
            self.assertEqual(
                raw_state,
                (json.dumps(state, separators=(",", ":")) + "\n").encode(),
            )
            self.assertEqual(list(sandboxes.iterdir()), [])

    def test_replay_state_output_is_no_replace_and_validated_before_setup(self) -> None:
        """Replay 상태 경로가 준비 전에 검증되고 기존 파일을 보존하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"
            state_output = Path(tmp) / "replay-state.json"
            state_output.write_text("keep\n", encoding="utf-8")

            result = replay.run_replay(
                repo_root=root,
                sandbox_parent=sandboxes,
                state_output=state_output,
            )

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertEqual(state_output.read_text(encoding="utf-8"), "keep\n")
            self.assertFalse(sandboxes.exists())
            self.resolve_manifest.assert_not_called()

    def test_replay_state_output_inside_active_repository_is_rejected(self) -> None:
        """Active 저장소 내부의 replay 상태 경로 거부 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"
            state_output = root / "replay-state.json"

            result = replay.run_replay(
                repo_root=root,
                sandbox_parent=sandboxes,
                state_output=state_output,
            )

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertFalse(state_output.exists())
            self.assertFalse(sandboxes.exists())
            self.resolve_manifest.assert_not_called()

    def test_existing_external_manifest_is_staged_as_read_only_input(self) -> None:
        """기존 외부 manifest가 읽기 전용 snapshot으로 전달되는지 검증."""

        digest = hashlib.sha256(_manifest_bytes()).hexdigest()
        main_source = f"""\
import hashlib
import os
from pathlib import Path

root = Path(__file__).resolve().parent.parent
manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"]).resolve()
checks = [
    manifest.is_relative_to(root),
    hashlib.sha256(manifest.read_bytes()).hexdigest() == {digest!r},
    os.environ["TRANSLATION_UPSTREAM_MANIFEST_DIGEST"] == {digest!r},
    manifest.stat().st_mode & 0o222 == 0,
]
raise SystemExit(0 if all(checks) else 9)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"
            external_manifest = Path(tmp) / "upstream-refs.json"
            external_manifest.write_bytes(_manifest_bytes())

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(external_manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_OK)
            self.assertEqual(
                external_manifest.read_bytes(),
                _manifest_bytes(),
            )
            self.assertEqual(list(sandboxes.iterdir()), [])

    def test_manifest_destination_inside_active_repository_is_rejected(self) -> None:
        """Active 저장소 내부의 manifest 대상 경로 거부 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"
            manifest = root / "generated/upstream-refs.json"

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertFalse(manifest.exists())
            self.assertFalse(sandboxes.exists())
            self.assertEqual(_git(root, "status", "--porcelain").stdout, "")

    def test_case_alias_inside_active_repository_is_rejected(self) -> None:
        """대소문자 alias로 저장소 내부를 가리키는 manifest 경로 거부 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(
                root,
                """\
import os
from pathlib import Path

manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"])
if not manifest.exists():
    manifest.write_text("generated\\n", encoding="utf-8")
""",
            )
            alias = root.with_name(root.name.upper())
            try:
                same_repository = alias.samefile(root)
            except OSError:
                same_repository = False
            if not same_repository:
                self.skipTest("filesystem is case-sensitive")
            sandboxes = Path(tmp) / "sandboxes"
            manifest = alias / "upstream-refs.json"

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertFalse(root.joinpath("upstream-refs.json").exists())
            self.assertFalse(sandboxes.exists())

    def test_manifest_ancestor_created_as_active_repo_symlink_is_rejected(
        self,
    ) -> None:
        """Manifest 상위 경로가 저장소 symlink로 교체되는 경쟁 조건 거부 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            late_parent = Path(tmp) / "outputs/late"
            late_parent.parent.mkdir()
            main_source = f"""\
import os
from pathlib import Path

manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"])
if not manifest.exists():
    manifest.write_text("generated\\n", encoding="utf-8")
late_parent = Path({str(late_parent)!r})
if not late_parent.exists():
    late_parent.symlink_to(Path({str(root)!r}), target_is_directory=True)
"""
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"
            manifest = late_parent / "upstream-refs.json"

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertFalse(root.joinpath("upstream-refs.json").exists())

    def test_symlink_manifest_target_is_rejected(self) -> None:
        """Symlink manifest 대상 거부 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"
            target = Path(tmp) / "actual-refs.json"
            target.write_text("pinned\n", encoding="utf-8")
            manifest = Path(tmp) / "upstream-refs.json"
            manifest.symlink_to(target)

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertTrue(manifest.is_symlink())
            self.assertEqual(target.read_text(encoding="utf-8"), "pinned\n")
            self.assertFalse(sandboxes.exists())

    def test_non_regular_manifest_target_is_rejected_before_replay(self) -> None:
        """일반 파일이 아닌 manifest 대상을 replay 전에 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"
            manifest = Path(tmp) / "upstream-refs.json"
            manifest.mkdir()

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertTrue(manifest.is_dir())
            self.assertFalse(sandboxes.exists())

    def test_manifest_created_during_replay_is_never_overwritten(self) -> None:
        """Replay 도중 다른 프로세스가 만든 manifest를 덮어쓰지 않는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            external_manifest = Path(tmp) / "upstream-refs.json"
            main_source = f"""\
import os
from pathlib import Path

manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"])
if not manifest.exists():
    manifest.write_text("generated\\n", encoding="utf-8")
external = Path({str(external_manifest)!r})
if not external.exists():
    external.write_text("created concurrently\\n", encoding="utf-8")
"""
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(external_manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertEqual(
                external_manifest.read_text(encoding="utf-8"),
                "created concurrently\n",
            )
            self.assertEqual(list(sandboxes.iterdir()), [])

    def test_failed_replay_does_not_export_generated_manifest(self) -> None:
        """실패한 replay가 새 manifest를 외부로 내보내지 않는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(9)\n")
            sandboxes = Path(tmp) / "sandboxes"
            external_manifest = Path(tmp) / "upstream-refs.json"
            state_output = Path(tmp) / "replay-state.json"

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(external_manifest)},
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                    state_output=state_output,
                )

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertFalse(external_manifest.exists())
            self.assertFalse(state_output.exists())
            self.assertEqual(
                len(
                    list(
                        sandboxes.glob(
                            "replay-pass-1/translation-candidate-*"
                        )
                    )
                ),
                1,
            )

    def test_existing_manifest_is_snapshotted_before_replay_setup(self) -> None:
        """기존 manifest가 replay 준비 전에 단일 snapshot으로 고정되는지 검증."""

        digest = hashlib.sha256(_manifest_bytes()).hexdigest()
        main_source = f"""\
import hashlib
import os
from pathlib import Path

manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"])
raise SystemExit(
    0 if hashlib.sha256(manifest.read_bytes()).hexdigest() == {digest!r} else 9
)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"
            external_manifest = Path(tmp) / "upstream-refs.json"
            external_manifest.write_bytes(_manifest_bytes())
            replacement = Path(tmp) / "replacement.json"
            replacement.write_text("replacement\n", encoding="utf-8")
            original_create_sandbox = replay._create_sandbox  # noqa: SLF001

            def replace_after_sandbox(
                source: Path, sandbox_parent: Path | None
            ) -> Path:
                """Manifest snapshot 뒤 외부 원본을 다른 byte로 교체."""

                sandbox = original_create_sandbox(source, sandbox_parent)
                external_manifest.unlink()
                external_manifest.symlink_to(replacement)
                return sandbox

            with patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(external_manifest)},
            ), patch.object(
                replay,
                "_create_sandbox",
                side_effect=replace_after_sandbox,
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_OK)
            self.assertTrue(external_manifest.is_symlink())
            self.assertEqual(
                replacement.read_text(encoding="utf-8"),
                "replacement\n",
            )

    def test_manifest_is_not_published_until_complete(self) -> None:
        """Manifest가 완전한 byte를 기록한 뒤에만 공개되는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "sandbox-manifest.json"
            source.write_text("generated\n", encoding="utf-8")
            destination = Path(tmp) / "published/manifest.json"
            observed: list[bool] = []
            real_fsync = os.fsync

            def observe_publication(descriptor: int) -> None:
                """Manifest 공개 시점의 대상 파일 내용을 관찰."""

                observed.append(destination.exists())
                real_fsync(descriptor)

            with patch.object(replay.os, "fsync", side_effect=observe_publication):
                replay._export_manifest(source, destination)  # noqa: SLF001

            self.assertEqual(observed, [False])
            self.assertEqual(
                destination.read_text(encoding="utf-8"),
                "generated\n",
            )

    def test_interrupted_manifest_export_leaves_no_destination(self) -> None:
        """Manifest export 중 interrupt가 대상 파일을 남기지 않는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "sandbox-manifest.json"
            source.write_text("generated\n", encoding="utf-8")
            destination = Path(tmp) / "published/manifest.json"

            with patch.object(replay.os, "fsync", side_effect=KeyboardInterrupt):
                with self.assertRaises(KeyboardInterrupt):
                    replay._export_manifest(source, destination)  # noqa: SLF001

            self.assertFalse(destination.exists())
            self.assertEqual(list(destination.parent.iterdir()), [])

    def test_failed_export_does_not_delete_concurrent_destination(self) -> None:
        """Export 실패 정리가 경쟁 프로세스의 대상 파일을 삭제하지 않는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "sandbox-manifest.json"
            source.write_text("generated\n", encoding="utf-8")
            destination = Path(tmp) / "published/manifest.json"
            moved = Path(tmp) / "opened-manifest.json"

            def replace_and_fail(_descriptor: int) -> None:
                """경쟁 대상 파일을 만든 뒤 manifest 연결을 실패시킴."""

                if destination.exists():
                    destination.rename(moved)
                destination.write_text("concurrent\n", encoding="utf-8")
                raise OSError("injected write failure")

            with patch.object(replay.os, "fsync", side_effect=replace_and_fail):
                with self.assertRaises(OSError):
                    replay._export_manifest(source, destination)  # noqa: SLF001

            self.assertEqual(
                destination.read_text(encoding="utf-8"),
                "concurrent\n",
            )
            self.assertEqual(list(destination.parent.iterdir()), [destination])

    def test_cleanup_failure_prevents_manifest_export(self) -> None:
        """Sandbox 정리 실패가 manifest export를 차단하는지 검증."""

        main_source = """\
import os
from pathlib import Path

manifest = Path(os.environ["TRANSLATION_UPSTREAM_MANIFEST"])
if not manifest.exists():
    manifest.write_text("generated\\n", encoding="utf-8")
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"
            external_manifest = Path(tmp) / "upstream-refs.json"
            state_output = Path(tmp) / "replay-state.json"
            stdout = io.StringIO()
            stderr = io.StringIO()

            def fail_cleanup(path: Path) -> None:
                """Replay sandbox 제거에서 정리 오류 발생."""

                raise OSError(f"injected cleanup failure: {path}")

            with redirect_stdout(stdout), redirect_stderr(stderr), patch.dict(
                os.environ,
                {"TRANSLATION_UPSTREAM_MANIFEST": str(external_manifest)},
            ), patch.object(
                replay.shutil,
                "rmtree",
                side_effect=fail_cleanup,
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                    state_output=state_output,
                )

            preserved = list(sandboxes.iterdir())
            output = stdout.getvalue() + stderr.getvalue()
            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertFalse(external_manifest.exists())
            self.assertFalse(state_output.exists())
            self.assertTrue(
                any(f"sandbox={path.name}" in output for path in preserved)
            )
            self.assertTrue(
                all(str(path) not in output for path in preserved)
            )
            self.assertNotIn(str(sandboxes), output)

    def test_success_replays_current_worktree_with_filters_and_removes_sandbox(self) -> None:
        """현재 worktree와 선택자를 replay한 뒤 sandbox를 제거하는지 검증."""

        main_source = """\
import os
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
checks = [
    os.environ.get("TRANSLATION_PROVIDER") == "identity",
    os.environ.get("TRANSLATION_REPLAY") == "1",
    "OPENAI_API_KEY" not in os.environ,
    "GH_TOKEN" not in os.environ,
    "SSH_AUTH_SOCK" not in os.environ,
    "PWD" not in os.environ,
    sys.argv[1:] == ["--version", "13.x", "--doc", "collections.md"],
    (root / "tracked.txt").read_text(encoding="utf-8") == "modified\\n",
    not (root / "deleted.txt").exists(),
    (root / "untracked.txt").read_text(encoding="utf-8") == "new\\n",
    subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout == "",
    subprocess.run(
        ["git", "remote"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout == "",
    subprocess.run(
        ["git", "for-each-ref", "--format=%(refname)", "refs/remotes/"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout == "",
    not (root / ".git/objects/info/alternates").exists(),
]
raise SystemExit(0 if all(checks) else 9)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            (root / "tracked.txt").write_text("modified\n", encoding="utf-8")
            (root / "deleted.txt").unlink()
            (root / "untracked.txt").write_text("new\n", encoding="utf-8")
            before = replay._worktree_fingerprint(root)  # noqa: SLF001
            sandboxes = Path(tmp) / "sandboxes"

            with patch.dict(
                os.environ,
                {
                    "OPENAI_API_KEY": "must-not-leak",
                    "GH_TOKEN": "must-not-leak",
                    "SSH_AUTH_SOCK": "/must/not/leak",
                },
            ):
                result = replay.run_replay(
                    repo_root=root,
                    version="13.x",
                    doc="collections.md",
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_OK)
            self.assertEqual(list(sandboxes.iterdir()), [])
            self.assertEqual(replay._worktree_fingerprint(root), before)  # noqa: SLF001

    def test_failed_sync_preserves_sandbox(self) -> None:
        """동기화 실패 시 디버깅용 sandbox를 보존하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(9)\n")
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            preserved = list(
                sandboxes.glob("replay-pass-1/translation-candidate-*")
            )
            self.assertEqual(len(preserved), 1)
            self.assertEqual(
                _git(preserved[0], "status", "--porcelain").stdout,
                "",
            )

    def test_supported_child_exit_code_is_preserved(self) -> None:
        """지원하는 하위 프로세스 종료 코드가 replay 결과에 보존되는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, f"raise SystemExit({replay.EXIT_REPLAY_ERROR})\n")
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertEqual(
                len(
                    list(
                        sandboxes.glob(
                            "replay-pass-1/translation-candidate-*"
                        )
                    )
                ),
                1,
            )

    def test_failed_replay_reports_only_a_relative_sandbox_identifier(self) -> None:
        """실패 로그가 sandbox의 상대 식별자만 노출하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(1)\n")
            sandboxes = Path(tmp) / "sandboxes"
            stdout = io.StringIO()
            stderr = io.StringIO()

            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            preserved = next(
                sandboxes.glob("replay-pass-1/translation-candidate-*")
            )
            relative = preserved.relative_to(sandboxes).as_posix()
            output = stdout.getvalue() + stderr.getvalue()
            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertIn(f"sandbox={relative}", output)
            self.assertNotIn(str(preserved), output)
            self.assertNotIn(str(sandboxes), output)

    def test_sandbox_operation_error_does_not_expose_artifact_path(self) -> None:
        """Sandbox 작업 오류가 외부 artifact 절대 경로를 숨기는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"
            stdout = io.StringIO()
            stderr = io.StringIO()

            def fail_with_artifact_path(_source: Path, sandbox: Path) -> None:
                """비공개 artifact 경로를 포함한 sandbox 작업 오류 발생."""

                raise OSError(f"failed to write {sandbox / 'private-output'}")

            with redirect_stdout(stdout), redirect_stderr(stderr), patch.object(
                replay,
                "_overlay_worktree",
                side_effect=fail_with_artifact_path,
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            preserved = next(sandboxes.iterdir())
            output = stdout.getvalue() + stderr.getvalue()
            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertIn(f"sandbox={preserved.name}", output)
            self.assertNotIn(str(preserved), output)
            self.assertNotIn(str(sandboxes), output)

    def test_sandbox_clone_error_does_not_expose_artifact_path(self) -> None:
        """Sandbox clone 오류가 외부 artifact 절대 경로를 숨기는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"
            stderr = io.StringIO()
            real_command = replay._command  # noqa: SLF001

            def fail_clone(
                args: list[str],
                *,
                cwd: Path,
                input_data: bytes | None = None,
            ) -> subprocess.CompletedProcess[bytes]:
                """비공개 artifact 경로를 포함한 clone 오류 발생."""

                if args[:2] == ["git", "clone"]:
                    raise replay.ReplayError(f"command failed: {' '.join(args)}")
                return real_command(args, cwd=cwd, input_data=input_data)

            with redirect_stderr(stderr), patch.object(
                replay,
                "_command",
                side_effect=fail_clone,
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandboxes,
                )

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertEqual(list(sandboxes.iterdir()), [])
            self.assertNotIn(str(sandboxes), stderr.getvalue())
            self.assertNotIn("translation-replay-", stderr.getvalue())

    def test_active_worktree_status_change_is_reported_and_preserves_sandbox(self) -> None:
        """Replay 도중 active worktree 변경을 감지하고 sandbox를 보존하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            (root / "tracked.txt").write_text("dirty before replay\n", encoding="utf-8")
            sandboxes = Path(tmp) / "sandboxes"

            def modify_active_worktree(
                _sandbox: Path,
                *,
                version: str | None,
                doc: str | None,
                manifest_digest: str,
                selector: bytes,
            ) -> int:
                """동기화 성공 직전에 active worktree 내용 변경."""

                self.assertIsNone(version)
                self.assertIsNone(doc)
                self.assertTrue(manifest_digest)
                self.assertTrue(selector)
                (root / "tracked.txt").write_text("changed during replay\n", encoding="utf-8")
                return replay.EXIT_REPLAY_ERROR

            with patch.object(
                replay, "_execute_sync", side_effect=modify_active_worktree
            ) as execute_sync:
                result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_WORKTREE_CHANGED)
            self.assertEqual(len(list(sandboxes.iterdir())), 1)
            execute_sync.assert_called_once()

    def test_active_index_content_change_is_reported(self) -> None:
        """상태 문자열이 같아도 active index 내용 변경을 감지하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            (root / "tracked.txt").write_text("staged before\n", encoding="utf-8")
            _git(root, "add", "tracked.txt")
            (root / "tracked.txt").write_text("worktree\n", encoding="utf-8")
            sandboxes = Path(tmp) / "sandboxes"

            def modify_active_index(
                _sandbox: Path,
                *,
                version: str | None,
                doc: str | None,
                manifest_digest: str,
                selector: bytes,
            ) -> int:
                """동기화 성공 직전에 active index의 blob 교체."""

                self.assertIsNone(version)
                self.assertIsNone(doc)
                self.assertTrue(manifest_digest)
                self.assertTrue(selector)
                (root / "tracked.txt").write_text("staged after\n", encoding="utf-8")
                _git(root, "add", "tracked.txt")
                (root / "tracked.txt").write_text("worktree\n", encoding="utf-8")
                return 0

            with patch.object(
                replay, "_execute_sync", side_effect=modify_active_index
            ):
                result = replay.run_replay(
                    repo_root=root, sandbox_parent=sandboxes
                )

            self.assertEqual(result, replay.EXIT_WORKTREE_CHANGED)
            self.assertEqual(len(list(sandboxes.iterdir())), 1)

    def test_active_clean_commit_is_reported(self) -> None:
        """깨끗한 상태를 유지한 active HEAD 변경도 감지하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"

            def commit_active_worktree(
                _sandbox: Path,
                *,
                version: str | None,
                doc: str | None,
                manifest_digest: str,
                selector: bytes,
            ) -> int:
                """동기화 성공 직전에 active 저장소에 새 commit 생성."""

                self.assertIsNone(version)
                self.assertIsNone(doc)
                self.assertTrue(manifest_digest)
                self.assertTrue(selector)
                (root / "tracked.txt").write_text(
                    "committed during replay\n", encoding="utf-8"
                )
                _git(root, "add", "tracked.txt")
                _git(root, "commit", "--quiet", "-m", "concurrent commit")
                return 0

            with patch.object(
                replay, "_execute_sync", side_effect=commit_active_worktree
            ):
                result = replay.run_replay(
                    repo_root=root, sandbox_parent=sandboxes
                )

            self.assertEqual(result, replay.EXIT_WORKTREE_CHANGED)
            self.assertEqual(len(list(sandboxes.iterdir())), 1)

    def test_interrupt_while_verifying_active_worktree_preserves_signal(self) -> None:
        """Active worktree 검증 중 interrupt의 signal 규약 보존 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"

            with patch.object(
                replay,
                "_execute_sync",
                return_value=0,
            ), patch.object(
                replay,
                "_worktree_fingerprint",
                side_effect=[b"before", KeyboardInterrupt],
            ):
                with self.assertRaises(KeyboardInterrupt):
                    replay.run_replay(
                        repo_root=root,
                        sandbox_parent=sandboxes,
                    )

            self.assertEqual(len(list(sandboxes.iterdir())), 1)

    def test_sync_interrupt_verifies_active_worktree_then_preserves_signal(self) -> None:
        """동기화 interrupt 뒤 active worktree를 재검증하고 signal을 보존하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"
            real_fingerprint = replay._worktree_fingerprint  # noqa: SLF001
            fingerprint_calls = 0

            def record_fingerprint(repo: Path) -> bytes:
                """Worktree 지문 호출 횟수를 기록하고 두 번째 호출에서 interrupt 발생."""

                nonlocal fingerprint_calls
                fingerprint_calls += 1
                return real_fingerprint(repo)

            with patch.object(
                replay,
                "_execute_sync",
                side_effect=KeyboardInterrupt,
            ), patch.object(
                replay,
                "_worktree_fingerprint",
                side_effect=record_fingerprint,
            ):
                with self.assertRaises(KeyboardInterrupt):
                    replay.run_replay(
                        repo_root=root,
                        sandbox_parent=sandboxes,
                    )

            self.assertGreaterEqual(fingerprint_calls, 2)
            self.assertEqual(len(list(sandboxes.iterdir())), 1)

    def test_git_environment_ignores_global_and_system_config(self) -> None:
        """Replay Git 환경이 전역·시스템 설정을 읽지 않는지 검증."""

        env = replay._git_environment()  # noqa: SLF001

        self.assertEqual(env["GIT_CONFIG_GLOBAL"], os.devnull)
        self.assertEqual(env["GIT_CONFIG_SYSTEM"], os.devnull)
        self.assertEqual(env["XDG_CONFIG_HOME"], env["HOME"])

    def test_git_environment_does_not_reuse_predictable_home_ignore_file(self) -> None:
        """Replay Git 환경이 예측 가능한 HOME ignore 파일을 재사용하지 않는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            hidden = root / "untracked.secret"
            hidden.write_text("must be replayed\n", encoding="utf-8")
            predictable_home = Path(tmp) / "translation-replay-git-home"
            ignore = predictable_home / ".config/git/ignore"
            ignore.parent.mkdir(parents=True)
            ignore.write_text("*.secret\n", encoding="utf-8")

            with patch.object(replay.tempfile, "gettempdir", return_value=tmp):
                output = replay._git(  # noqa: SLF001
                    root,
                    "ls-files",
                    "--others",
                    "--exclude-standard",
                    "-z",
                ).stdout

            self.assertIn(b"untracked.secret\0", output)

    def test_untracked_file_mode_is_part_of_worktree_fingerprint(self) -> None:
        """미추적 파일 권한이 worktree 지문에 포함되는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            script = root / "script.sh"
            script.write_text("#!/bin/sh\n", encoding="utf-8")
            script.chmod(0o644)
            before = replay._worktree_fingerprint(root)  # noqa: SLF001

            script.chmod(0o755)

            self.assertNotEqual(
                replay._worktree_fingerprint(root),  # noqa: SLF001
                before,
            )

    def test_non_head_refs_are_part_of_active_repository_fingerprint(self) -> None:
        """HEAD 외 Git refs도 active 저장소 지문에 포함되는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            _git(root, "update-ref", "refs/test/guarded", "HEAD")
            before = replay._worktree_fingerprint(root)  # noqa: SLF001

            _git(root, "update-ref", "-d", "refs/test/guarded")

            self.assertNotEqual(
                replay._worktree_fingerprint(root),  # noqa: SLF001
                before,
            )

    def test_tmpdir_inside_active_repository_is_rejected_cleanly(self) -> None:
        """Active 저장소 내부의 기본 임시 경로를 부작용 없이 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandbox_parent = root / "tmp"
            sandbox_parent.mkdir()
            stderr = io.StringIO()

            with redirect_stderr(stderr), patch.object(
                replay.tempfile,
                "gettempdir",
                return_value=str(sandbox_parent),
            ):
                result = replay.run_replay(repo_root=root)

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertEqual(list(sandbox_parent.iterdir()), [])
            self.assertEqual(_git(root, "status", "--porcelain").stdout, "")
            self.assertNotIn(str(sandbox_parent), stderr.getvalue())
            self.assertIn(
                "temporary directory is inside active repository",
                stderr.getvalue(),
            )

    def test_tmpdir_inside_repository_is_rejected_with_explicit_sandbox_parent(
        self,
    ) -> None:
        """명시한 sandbox 상위 경로가 저장소 내부이면 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            temp_parent = root / "tmp"
            temp_parent.mkdir()
            sandbox_parent = Path(tmp) / "sandboxes"

            with patch.object(
                replay.tempfile,
                "gettempdir",
                return_value=str(temp_parent),
            ):
                result = replay.run_replay(
                    repo_root=root,
                    sandbox_parent=sandbox_parent,
                )

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertEqual(list(temp_parent.iterdir()), [])
            self.assertFalse(sandbox_parent.exists())

    def test_untracked_symlink_is_rejected_without_following_it(self) -> None:
        """미추적 symlink를 따라가지 않고 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            external = Path(tmp) / "external.txt"
            external.write_text("outside\n", encoding="utf-8")
            (root / "external-link").symlink_to(external)
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertEqual(external.read_text(encoding="utf-8"), "outside\n")
            self.assertEqual(len(list(sandboxes.iterdir())), 1)

    def test_tracked_symlink_is_rejected_without_following_it(self) -> None:
        """변경된 추적 symlink를 따라가지 않고 거부하는지 검증."""

        main_source = """\
from pathlib import Path

root = Path(__file__).resolve().parent.parent
(root / "tracked.txt").write_text("changed\\n", encoding="utf-8")
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            external = Path(tmp) / "external.txt"
            external.write_text("outside\n", encoding="utf-8")
            (root / "tracked.txt").unlink()
            (root / "tracked.txt").symlink_to(external)
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertEqual(external.read_text(encoding="utf-8"), "outside\n")
            self.assertFalse(sandboxes.exists())

    def test_unchanged_tracked_symlink_is_allowed(self) -> None:
        """저장소 내부를 가리키는 변경 없는 추적 symlink 허용 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            (root / "target.txt").write_text("inside\n", encoding="utf-8")
            (root / "tracked-link").symlink_to("target.txt")
            _git(root, "add", "target.txt", "tracked-link")
            _git(root, "commit", "--quiet", "-m", "add tracked link")
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_OK)
            self.assertEqual(list(sandboxes.iterdir()), [])

    def test_unchanged_external_tracked_symlink_is_rejected(self) -> None:
        """저장소 외부를 가리키는 변경 없는 추적 symlink 거부 검증."""

        main_source = """\
from pathlib import Path

root = Path(__file__).resolve().parent.parent
(root / "external-link").write_text("escaped\\n", encoding="utf-8")
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            external = Path(tmp) / "external.txt"
            external.write_text("outside\n", encoding="utf-8")
            (root / "external-link").symlink_to(external)
            _git(root, "add", "external-link")
            _git(root, "commit", "--quiet", "-m", "add external link")
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertEqual(external.read_text(encoding="utf-8"), "outside\n")
            self.assertFalse(sandboxes.exists())

    def test_tracked_symlink_cannot_leave_and_reenter_repository(self) -> None:
        """외부를 경유해 저장소로 돌아오는 추적 symlink 거부 검증."""

        main_source = """\
from pathlib import Path

root = Path(__file__).resolve().parent.parent
(root / "external-hop").write_text("escaped\\n", encoding="utf-8")
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            target = root / "target.txt"
            target.write_text("inside\n", encoding="utf-8")
            outside = Path(tmp) / "outside"
            outside.mkdir()
            (outside / "back-inside").symlink_to(target)
            (root / "external-hop").symlink_to("../outside/back-inside")
            _git(root, "add", "target.txt", "external-hop")
            _git(root, "commit", "--quiet", "-m", "add external hop")
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertEqual(target.read_text(encoding="utf-8"), "inside\n")
            self.assertFalse(sandboxes.exists())

    def test_second_sync_must_leave_first_sync_result_unchanged(self) -> None:
        """두 번째 동기화가 첫 verified tree를 변경하면 실패하는지 검증."""

        main_source = """\
from pathlib import Path

root = Path(__file__).resolve().parent.parent
document = root / "tracked.txt"
current = document.read_text(encoding="utf-8")
document.write_text(
    "first\\n" if current == "original\\n" else "second\\n",
    encoding="utf-8",
)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            sandboxes = Path(tmp) / "sandboxes"

            result = replay.run_replay(repo_root=root, sandbox_parent=sandboxes)

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertEqual(
                len(
                    list(
                        sandboxes.glob(
                            "replay-pass-*/translation-candidate-*"
                        )
                    )
                ),
                2,
            )

    def test_sandbox_is_removed_when_setup_fails(self) -> None:
        """Sandbox 준비 실패 시 불완전 sandbox를 제거하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"

            with patch.object(
                replay,
                "_command",
                side_effect=replay.ReplayError("fixture failure"),
            ):
                with self.assertRaises(replay.ReplayError):
                    replay._create_sandbox(root, sandboxes)  # noqa: SLF001

            self.assertFalse(sandboxes.exists())

    def test_sandbox_is_removed_when_setup_is_interrupted(self) -> None:
        """Sandbox 준비 interrupt 시 불완전 sandbox를 제거하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            sandboxes = Path(tmp) / "sandboxes"

            with patch.object(
                replay,
                "_command",
                side_effect=KeyboardInterrupt,
            ):
                with self.assertRaises(KeyboardInterrupt):
                    replay._create_sandbox(root, sandboxes)  # noqa: SLF001

            self.assertFalse(sandboxes.exists())

    def test_child_stable_failure_is_preserved_in_replay_report(self) -> None:
        """첫 pass 하위 작업의 안정적인 실패 증거가 replay 보고서에 보존되는지 검증."""

        main_source = """\
import json
import os
from pathlib import Path

payload = {
    "schema_version": 1,
    "run_id": os.environ["TRANSLATION_RUN_ID"],
    "manifest_digest": os.environ["TRANSLATION_UPSTREAM_MANIFEST_DIGEST"],
    "base_head": None,
    "stage": "verification",
    "classification": "V",
    "code": "SOURCE_STRUCTURE_MISMATCH",
    "exit_code": 1,
    "published_commit": None,
    "version": "13.x",
    "locale": "ko",
    "document": "documentation/13.x/ko/routing.md",
    "plan_id": None,
    "structural_address": "section:1",
    "attempts": None,
    "issues": [{
        "code": "SOURCE_STRUCTURE_MISMATCH",
        "structural_address": "section:1",
        "message": "heading order differs",
    }],
    "candidate_debug_path": None,
}
Path(os.environ["TRANSLATION_FAILURE_REPORT"]).write_text(
    json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    + "\\n",
    encoding="utf-8",
)
raise SystemExit(1)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            artifact_root = Path(tmp) / "artifacts"
            artifact_root.mkdir()
            report_path = artifact_root / "replay-failure.json"

            with patch.dict(
                os.environ,
                {
                    replay.FAILURE_REPORT_ENV: str(report_path),
                    replay.RUN_ID_ENV: "run-parent-child",
                },
            ):
                result = replay.run_replay(
                    repo_root=root,
                    version="13.x",
                    artifact_root=artifact_root,
                )

            report = json.loads(report_path.read_bytes())
            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertEqual(report["run_id"], "run-parent-child")
            self.assertEqual(report["code"], "SOURCE_STRUCTURE_MISMATCH")
            self.assertEqual(report["stage"], "verification")
            self.assertEqual(report["exit_code"], replay.EXIT_SYNC_FAILED)
            self.assertEqual(report["locale"], "ko")
            self.assertEqual(
                report["document"],
                "documentation/13.x/ko/routing.md",
            )

    def test_second_pass_child_stable_failure_is_preserved(self) -> None:
        """두 번째 pass 하위 작업의 안정적인 실패 증거 보존 검증."""

        main_source = """\
import json
import os
from pathlib import Path

document = Path("tracked.txt")
if document.read_text(encoding="utf-8") == "original\\n":
    document.write_text("candidate\\n", encoding="utf-8")
    raise SystemExit(0)

payload = {
    "schema_version": 1,
    "run_id": os.environ["TRANSLATION_RUN_ID"],
    "stage": "verification",
    "classification": "V",
    "code": "SOURCE_STRUCTURE_MISMATCH",
    "exit_code": 1,
    "version": "13.x",
    "locale": "ko",
    "document": "documentation/13.x/ko/routing.md",
    "plan_id": None,
    "structural_address": "section:2",
    "attempts": None,
    "issues": [{
        "code": "SOURCE_STRUCTURE_MISMATCH",
        "structural_address": "section:2",
        "message": "second pass structure differs",
    }],
}
Path(os.environ["TRANSLATION_FAILURE_REPORT"]).write_text(
    json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    + "\\n",
    encoding="utf-8",
)
raise SystemExit(1)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            artifact_root = Path(tmp) / "artifacts"
            artifact_root.mkdir()
            report_path = artifact_root / "replay-failure.json"

            with patch.dict(
                os.environ,
                {
                    replay.FAILURE_REPORT_ENV: str(report_path),
                    replay.RUN_ID_ENV: "run-second-child",
                },
            ):
                result = replay.run_replay(
                    repo_root=root,
                    artifact_root=artifact_root,
                )

            report = json.loads(report_path.read_bytes())
            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertEqual(report["run_id"], "run-second-child")
            self.assertEqual(report["code"], "SOURCE_STRUCTURE_MISMATCH")
            self.assertEqual(report["stage"], "verification")
            self.assertTrue(
                report["candidate_debug_path"].startswith(
                    "replay-pass-2/translation-candidate-"
                )
            )
            self.assertFalse(
                (
                    artifact_root
                    / "replay-pass-1"
                    / SYNC_FAILURE_REPORT_FILENAME
                ).exists()
            )
            self.assertTrue(
                (
                    artifact_root
                    / "replay-pass-2"
                    / SYNC_FAILURE_REPORT_FILENAME
                ).is_file()
            )

    def test_replay_passes_use_distinct_child_report_paths_and_shared_run_id(
        self,
    ) -> None:
        """두 pass가 별도 보고서 경로와 같은 실행 ID를 사용하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            artifact_root = Path(tmp) / "artifacts"
            record = Path(tmp) / "child-report-contract"
            main_source = f"""\
import os
from pathlib import Path

record = Path({str(record)!r})
line = os.environ["TRANSLATION_RUN_ID"] + "|" + os.environ["TRANSLATION_FAILURE_REPORT"]
lines = record.read_text(encoding="utf-8").splitlines() if record.exists() else []
expected = (
    "API_KEY" not in os.environ
    and "OPENAI_API_KEY" not in os.environ
    and line not in lines
)
record.write_text("\\n".join([*lines, line]) + "\\n", encoding="utf-8")
raise SystemExit(0 if expected else 9)
"""
            root.mkdir()
            _init_repo(root, main_source)
            artifact_root.mkdir()

            with patch.dict(
                os.environ,
                {
                    "API_KEY": "must-not-leak",
                    "OPENAI_API_KEY": "must-not-leak",
                    replay.RUN_ID_ENV: "run-parent-distinct",
                },
            ):
                result = replay.run_replay(
                    repo_root=root,
                    artifact_root=artifact_root,
                )

            self.assertEqual(result, replay.EXIT_OK)
            lines = record.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            run_ids = [line.split("|", 1)[0] for line in lines]
            report_paths = [Path(line.split("|", 1)[1]) for line in lines]
            self.assertEqual(run_ids, ["run-parent-distinct"] * 2)
            self.assertEqual(len(set(report_paths)), 2)
            self.assertEqual(
                [path.parent.name for path in report_paths],
                ["replay-pass-1", "replay-pass-2"],
            )

    def test_nonconvergent_replay_writes_canonical_failure_report(self) -> None:
        """비수렴 replay가 정규 실패 보고서를 기록하는지 검증."""

        main_source = """\
from pathlib import Path

root = Path(__file__).resolve().parent.parent
document = root / "tracked.txt"
current = document.read_text(encoding="utf-8")
document.write_text(
    "first\\n" if current == "original\\n" else "second\\n",
    encoding="utf-8",
)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, main_source)
            artifact_root = Path(tmp) / "artifacts"
            artifact_root.mkdir()
            report_path = artifact_root / "replay-failure.json"
            base_head = _git(root, "rev-parse", "HEAD").stdout.strip()

            with patch.dict(
                os.environ,
                {
                    replay.FAILURE_REPORT_ENV: str(report_path),
                    replay.RUN_ID_ENV: "run-parent-1",
                },
            ):
                result = replay.run_replay(
                    repo_root=root,
                    artifact_root=artifact_root,
                )

            raw_report = report_path.read_bytes()
            report = json.loads(raw_report)
            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertEqual(report["run_id"], "run-parent-1")
            self.assertEqual(report["code"], "REPLAY_NON_CONVERGENT")
            self.assertEqual(report["classification"], "V")
            self.assertEqual(report["exit_code"], replay.EXIT_SYNC_FAILED)
            self.assertEqual(report["base_head"], base_head)
            self.assertEqual(
                report["manifest_digest"],
                hashlib.sha256(_manifest_bytes()).hexdigest(),
            )
            self.assertTrue(
                report["candidate_debug_path"].startswith(
                    "replay-pass-2/translation-candidate-"
                )
            )
            self.assertEqual(
                raw_report,
                (
                    json.dumps(report, separators=(",", ":"), sort_keys=True)
                    + "\n"
                ).encode(),
            )

    def test_expired_deadline_writes_infrastructure_failure_report(self) -> None:
        """만료된 기한이 인프라 실패 보고서로 기록되는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            artifact_root = Path(tmp) / "artifacts"
            artifact_root.mkdir()
            report_path = artifact_root / "replay-failure.json"

            with patch.dict(
                os.environ,
                {
                    replay.FAILURE_REPORT_ENV: str(report_path),
                    replay.RUN_ID_ENV: "run-parent-2",
                    replay.WORKFLOW_DEADLINE_ENV: str(time.monotonic() - 1),
                },
            ):
                result = replay.run_replay(
                    repo_root=root,
                    artifact_root=artifact_root,
                )

            report = json.loads(report_path.read_bytes())
            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertEqual(report["code"], "WORKFLOW_DEADLINE_EXCEEDED")
            self.assertEqual(report["classification"], "X")
            self.assertEqual(report["exit_code"], replay.EXIT_REPLAY_ERROR)
            self.assertIsNone(report["manifest_digest"])
            self.assertIsNone(report["candidate_debug_path"])

    def test_active_worktree_mutation_report_has_exit_three(self) -> None:
        """Active worktree 변경 보고서의 종료 코드가 3인지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            artifact_root = Path(tmp) / "artifacts"
            artifact_root.mkdir()
            report_path = artifact_root / "replay-failure.json"

            def mutate_active_repo(
                _sandbox: Path,
                **_kwargs: object,
            ) -> int:
                """Replay 도중 active 저장소 파일 변경."""

                (root / "tracked.txt").write_text("changed\n", encoding="utf-8")
                return replay.EXIT_OK

            with patch.dict(
                os.environ,
                {
                    replay.FAILURE_REPORT_ENV: str(report_path),
                    replay.RUN_ID_ENV: "run-parent-3",
                },
            ), patch.object(
                replay,
                "_execute_sync",
                side_effect=mutate_active_repo,
            ):
                result = replay.run_replay(
                    repo_root=root,
                    artifact_root=artifact_root,
                )

            report = json.loads(report_path.read_bytes())
            self.assertEqual(result, replay.EXIT_WORKTREE_CHANGED)
            self.assertEqual(report["code"], "ACTIVE_WORKTREE_MUTATED")
            self.assertEqual(report["exit_code"], replay.EXIT_WORKTREE_CHANGED)
            self.assertTrue(report["candidate_debug_path"])

    def test_signal_does_not_write_or_replace_failure_report(self) -> None:
        """Interrupt가 실패 보고서를 생성하거나 교체하지 않는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            artifact_root = Path(tmp) / "artifacts"
            artifact_root.mkdir()
            report_path = artifact_root / "replay-failure.json"

            with patch.dict(
                os.environ,
                {
                    replay.FAILURE_REPORT_ENV: str(report_path),
                    replay.RUN_ID_ENV: "run-parent-4",
                },
            ), patch.object(
                replay,
                "_execute_sync",
                side_effect=KeyboardInterrupt,
            ):
                with self.assertRaises(KeyboardInterrupt):
                    replay.run_replay(
                        repo_root=root,
                        artifact_root=artifact_root,
                    )

            self.assertFalse(report_path.exists())

    def test_existing_failure_report_is_never_replaced(self) -> None:
        """기존 replay 실패 보고서를 절대 교체하지 않는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(1)\n")
            artifact_root = Path(tmp) / "artifacts"
            artifact_root.mkdir()
            report_path = artifact_root / "replay-failure.json"
            report_path.write_text("keep\n", encoding="utf-8")
            stderr = io.StringIO()

            with patch.dict(
                os.environ,
                {
                    replay.FAILURE_REPORT_ENV: str(report_path),
                    replay.RUN_ID_ENV: "run-parent-5",
                },
            ), redirect_stderr(stderr):
                result = replay.run_replay(
                    repo_root=root,
                    artifact_root=artifact_root,
                )

            self.assertEqual(result, replay.EXIT_REPLAY_ERROR)
            self.assertEqual(report_path.read_text(encoding="utf-8"), "keep\n")
            self.assertIn("REPORT_WRITE_FAILED", stderr.getvalue())

    def test_failure_report_outside_explicit_artifact_root_is_not_written(
        self,
    ) -> None:
        """명시한 artifact root 밖의 실패 보고서 경로를 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            artifact_root = Path(tmp) / "artifacts"
            artifact_root.mkdir()
            report_path = Path(tmp) / "outside-failure.json"
            stderr = io.StringIO()

            with patch.dict(
                os.environ,
                {
                    replay.FAILURE_REPORT_ENV: str(report_path),
                    replay.RUN_ID_ENV: "run-parent-outside",
                },
            ), redirect_stderr(stderr):
                result = replay.run_replay(
                    repo_root=root,
                    artifact_root=artifact_root,
                )

            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertFalse(report_path.exists())
            self.assertIn("REPORT_WRITE_FAILED", stderr.getvalue())

    def test_failure_report_cannot_alias_success_state_output(self) -> None:
        """실패 보고서와 성공 상태 출력이 같은 경로를 공유하지 못하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            _init_repo(root, "raise SystemExit(0)\n")
            artifact_root = Path(tmp) / "artifacts"
            artifact_root.mkdir()
            shared_output = artifact_root / "shared.json"

            with patch.dict(
                os.environ,
                {
                    replay.FAILURE_REPORT_ENV: str(shared_output),
                    replay.RUN_ID_ENV: "run-parent-shared-output",
                },
            ):
                result = replay.run_replay(
                    repo_root=root,
                    artifact_root=artifact_root,
                    state_output=shared_output,
                )

            report = json.loads(shared_output.read_bytes())
            self.assertEqual(result, replay.EXIT_SYNC_FAILED)
            self.assertEqual(report["code"], "REPLAY_PATH_UNSAFE")
            self.assertEqual(report["exit_code"], replay.EXIT_SYNC_FAILED)
            self.assertNotIn("manifest_base64", report)


if __name__ == "__main__":
    unittest.main()
