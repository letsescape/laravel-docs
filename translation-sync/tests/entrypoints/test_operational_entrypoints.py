"""문서 동기화·번역 운영 진입점 검증."""

from __future__ import annotations

import importlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import sync


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def read_repository_file(relative: str) -> str:
    """저장소 상대 경로의 UTF-8 파일 내용 반환."""

    return (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")


def workflow_run_script(
    step_name: str,
    workflow_path: str = ".github/workflows/sync-translation.yml",
) -> str:
    """지정한 Actions 단계의 셸 스크립트 추출."""

    workflow = read_repository_file(workflow_path)
    step = workflow.split(f"      - name: {step_name}\n", 1)[1]
    step = step.split("\n      - name:", 1)[0]
    body = step.split("        run: |\n", 1)[1]
    return "\n".join(line[10:] if line else "" for line in body.splitlines())


def makefile_env_loader() -> str:
    """Makefile의 `.env` 로더 정의를 실행 가능한 셸 조각으로 추출."""

    makefile = read_repository_file("Makefile")
    body = makefile.split("define LOAD_TRANSLATION_ENV\n", 1)[1]
    body = body.split("\nendef", 1)[0]
    env_file = next(
        line.split(":=", 1)[1].strip()
        for line in makefile.splitlines()
        if line.startswith("TRANSLATION_ENV_FILE")
    )
    return (
        body.replace("$(TRANSLATION_ENV_FILE)", env_file)
        .replace("$$", "$")
        .replace("\\\n", "\n")
    )


class OperationalEntrypointTests(unittest.TestCase):
    """Actions·Makefile·Docker 운영 진입점 테스트 모음."""

    def test_env_file_loader_fills_unset_values_and_keeps_explicit_ones(self) -> None:
        """`.env`가 미설정 값만 채우고 명시적 환경 변수는 유지하는지 검증."""

        script = makefile_env_loader()
        self.assertIn(".env", script)
        environment = {
            key: value
            for key, value in os.environ.items()
            if not key.startswith(("GIT_", "TRANSLATION_", "OPENAI_"))
        }

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".env").write_text(
                "# comment\n"
                "\n"
                "TRANSLATION_PROVIDER=openai\n"
                'TRANSLATION_CLI_COMMAND="codex exec"\n'
                "OPENAI_API_KEY=from-file\n",
                encoding="utf-8",
            )
            probe = (
                script
                + "\nprintf '%s|%s|%s' "
                '"$TRANSLATION_PROVIDER" "$TRANSLATION_CLI_COMMAND" "$OPENAI_API_KEY"'
            )
            for explicit, expected in (
                ({}, "openai|codex exec|from-file"),
                ({"TRANSLATION_PROVIDER": "cli"}, "cli|codex exec|from-file"),
                ({"OPENAI_API_KEY": ""}, "openai|codex exec|"),
            ):
                with self.subTest(explicit=explicit):
                    result = subprocess.run(
                        ["bash", "-c", probe],
                        cwd=root,
                        env={**environment, **explicit},
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    self.assertEqual(result.stdout, expected)

    def test_compose_and_deploy_declare_the_expected_contracts(self) -> None:
        """Compose의 `.env` 경로와 배포 연계 조건을 검증."""

        compose = read_repository_file("docker-compose.yml")
        self.assertIn("env_file:\n      - path: .env", compose)

        deploy = read_repository_file(".github/workflows/deploy.yml")
        self.assertIn("workflows:\n      - Sync Documentation Translation", deploy)
        self.assertIn("github.event.workflow_run.conclusion == 'success'", deploy)
        self.assertIn("github.event.workflow_run.head_branch == 'main'", deploy)

    def test_sync_package_preserves_flat_module_imports(self) -> None:
        """기존 단일 계층 모듈 가져오기가 정규 패키지와 같은 객체인지 검증."""

        aliases = {
            "annotate": "sync.annotation.annotate",
            "config": "sync.runtime.config",
            "diff": "sync.source.diff",
            "patch": "sync.translation.patch",
            "postprocess": "sync.postprocessing.postprocess",
            "preprocess": "sync.preprocessing.preprocess",
            "prompt": "sync.translation.prompt",
            "repair": "sync.postprocessing.repair",
            "response_contract": "sync.verification.response_contract",
            "translate": "sync.translation.translate",
            "upstream": "sync.source.upstream",
            "verify": "sync.verification.verify",
        }

        self.assertEqual(set(sync.__all__), {*aliases, "sidebar"})
        for alias, canonical in aliases.items():
            with self.subTest(alias=alias):
                self.assertIs(
                    importlib.import_module(f"sync.{alias}"),
                    importlib.import_module(canonical),
                )
        self.assertIs(sync.sidebar, importlib.import_module("sync.sidebar"))

    def test_actions_runs_tests_then_python_sync_then_commit(self) -> None:
        """번역 Actions가 테스트·동기화 뒤 문서 커밋까지만 수행하는지 검증."""

        workflow = read_repository_file(".github/workflows/sync-translation.yml")

        tests = workflow.index("python -m unittest discover -s tests")
        sync_run = workflow.index('python main.py "${args[@]}"')
        commit = workflow.index("- name: Commit synchronized documents")
        self.assertLess(tests, sync_run)
        self.assertLess(sync_run, commit)
        self.assertIn("uses: actions/checkout@v6", workflow)
        self.assertIn("uses: astral-sh/setup-uv@v7", workflow)
        self.assertIn("permissions:\n  contents: write", workflow)
        self.assertIn("timeout-minutes: 360", workflow)
        self.assertIn("- name: Validate branch ref", workflow)
        # 자격 증명은 커밋 단계에만 주입한다.
        self.assertIn("persist-credentials: false", workflow)
        self.assertLess(workflow.index("persist-credentials: false"), commit)
        self.assertNotIn("${{ github.token }}", workflow[:commit])
        self.assertIn("OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}", workflow)
        self.assertNotRegex(workflow, r"uses: [^\n]+@[0-9a-f]{40}")

        for unrelated in (
            "setup-node",
            "npm ",
            "workflow.py",
            "replay.py",
            "provider_check.py",
            "validate_generated_changes.py",
            "upload-artifact",
            "GH_TOKEN",
            "publication",
            "deploy",
            "${{ vars.",
            "AZURE_OPENAI",
            "CODEX_",
        ):
            self.assertNotIn(unrelated, workflow)

    def test_deploy_workflow_is_independent_from_translation(self) -> None:
        """사이트 배포에 번역 실행 상관관계 입력이 남지 않는지 검증."""

        workflow = read_repository_file(".github/workflows/deploy.yml")

        self.assertIn("uses: actions/setup-node@v6", workflow)
        self.assertIn("uses: actions/deploy-pages@v5", workflow)
        self.assertIn("- name: Validate deployment branch", workflow)
        self.assertIn("REF_TYPE: ${{ github.ref_type }}", workflow)
        self.assertIn("REF_NAME: ${{ github.ref_name }}", workflow)
        self.assertNotIn("translation-deploy", workflow)
        self.assertNotIn("expected_commit", workflow)
        self.assertNotIn("correlation_id", workflow)

    def test_make_targets_run_main_directly(self) -> None:
        """Make의 번역 대상이 Python 진입점을 직접 호출하는지 검증."""

        makefile = read_repository_file("Makefile")

        self.assertIn("translation-run:", makefile)
        self.assertIn('python main.py "$$@"', makefile)
        self.assertIn("TRANSLATION_API_ENV_KEYS := OPENAI_API_KEY", makefile)
        self.assertIn('--user "$$(id -u):$$(id -g)"', makefile)
        self.assertIn("-e HOME=/tmp", makefile)
        self.assertIn("-e TRANSLATION_PROVIDER=openai", makefile)
        for unrelated in (
            "translation-prepare",
            "translation-publish",
            "translation-deploy",
            "translation-replay-diagnostic",
            "translation-provider-diagnostic",
            "translation-path-diagnostic",
            "workflow.py",
            "GH_TOKEN",
            "ARTIFACT_ROOT",
            "PUSH_ENDPOINT",
        ):
            self.assertNotIn(unrelated, makefile)

    def test_translation_container_is_python_only_and_writes_results(self) -> None:
        """번역 컨테이너가 Python으로 작업 트리의 문서를 직접 갱신하는지 검증."""

        dockerfile = read_repository_file("Dockerfile.translate")
        compose = read_repository_file("docker-compose.yml")

        self.assertIn("FROM ghcr.io/astral-sh/uv:python3.14-", dockerfile)
        self.assertIn("ca-certificates git", dockerfile)
        self.assertIn('"/workspace/translation-sync/main.py"', dockerfile)
        for unrelated in ("FROM node:", "npm ", "codex", " gh ", "workflow.py"):
            self.assertNotIn(unrelated, dockerfile)

        translate = compose.split("  translate:\n", 1)[1]
        self.assertIn("source: .", translate)
        self.assertIn("target: /workspace", translate)
        self.assertNotIn("read_only: true", translate)
        self.assertNotIn("/artifacts", translate)
        self.assertNotIn("translation-sync-artifacts", compose)


class TranslationWorkflowShellTests(unittest.TestCase):
    """번역 Actions 셸 경계 조건 테스트 모음."""

    def test_sync_step_preserves_nonzero_python_status(self) -> None:
        """동기화·번역 단계가 Python 종료 코드를 보존하는지 검증."""

        script = workflow_run_script("Run translation sync")
        harness = 'uv() { return "$SYNC_STATUS"; }\n' + script

        for status in (1, 2):
            with self.subTest(status=status):
                env = os.environ.copy()
                env.update(
                    {
                        "INPUT_VERSION": "",
                        "INPUT_DOC": "",
                        "SYNC_STATUS": str(status),
                    }
                )
                result = subprocess.run(
                    ["bash", "-e", "-c", harness],
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )

                self.assertEqual(result.returncode, status)

    def test_commit_step_records_documents_only_when_they_change(self) -> None:
        """커밋 단계가 변경이 있을 때만 문서를 커밋해 원격에 반영하는지 검증."""

        script = workflow_run_script("Commit synchronized documents")
        # 상위 Git 호출이 남긴 index·저장소 환경이 fixture 저장소로 새지 않도록 제거.
        environment = {
            key: value
            for key, value in os.environ.items()
            if not key.startswith(("GIT_", "GITHUB_"))
        }
        environment["GITHUB_REF_NAME"] = "main"
        environment["GITHUB_REPOSITORY"] = "owner/repository"
        environment["PUSH_TOKEN"] = "test-token"
        push_url = "https://x-access-token:test-token@github.com/owner/repository"
        git = ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com"]

        def run(arguments: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
            """fixture 저장소에서 Git 명령 실행."""

            return subprocess.run(
                arguments,
                cwd=cwd,
                env=environment,
                capture_output=True,
                text=True,
                check=True,
            )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            remote = root / "remote.git"
            work = root / "work"
            work.mkdir()
            run(["git", "init", "--bare", "--initial-branch=main", str(remote)], root)
            run([*git, "init", "--initial-branch=main", "."], work)
            for directory in ("i18n", "versioned_docs", "versioned_sidebars"):
                (work / directory).mkdir()
                (work / directory / "seed.md").write_text("seed\n", encoding="utf-8")
            run([*git, "add", "-A"], work)
            run([*git, "commit", "-m", "seed"], work)
            run([*git, "remote", "add", "origin", str(remote)], work)
            run([*git, "push", "origin", "main"], work)
            # 스크립트가 만드는 원격 URL을 fixture 저장소로 돌린다.
            run(
                [*git, "config", f"url.{remote}.insteadOf", push_url],
                work,
            )

            unchanged = subprocess.run(
                ["bash", "-e", "-c", script],
                cwd=work,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(unchanged.returncode, 0, unchanged.stderr)
            self.assertIn("No documentation changes to commit.", unchanged.stdout)

            (work / "versioned_docs" / "seed.md").write_text(
                "translated\n", encoding="utf-8"
            )
            changed = subprocess.run(
                ["bash", "-e", "-c", script],
                cwd=work,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(changed.returncode, 0, changed.stderr)

            published = run([*git, "log", "-1", "--format=%s", "main"], remote)
            self.assertEqual(published.stdout.strip(), "docs: synchronize translations")

    def test_deploy_step_accepts_only_the_main_branch(self) -> None:
        """수동 사이트 배포도 main branch에서만 진행되는지 검증."""

        script = workflow_run_script(
            "Validate deployment branch",
            ".github/workflows/deploy.yml",
        )
        cases = (
            ({"REF_TYPE": "branch", "REF_NAME": "main"}, 0),
            ({"REF_TYPE": "branch", "REF_NAME": "develop"}, 1),
            ({"REF_TYPE": "tag", "REF_NAME": "main"}, 1),
        )
        for environment, expected_status in cases:
            with self.subTest(environment=environment):
                result = subprocess.run(
                    ["bash", "-e", "-c", script],
                    env={**os.environ, **environment},
                    capture_output=True,
                    text=True,
                    check=False,
                )

                self.assertEqual(result.returncode, expected_status)


if __name__ == "__main__":
    unittest.main()
