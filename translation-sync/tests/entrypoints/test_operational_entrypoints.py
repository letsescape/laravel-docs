"""운영 진입점의 단계 위임과 credential 경계 검증."""

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


def workflow_run_script(step_name: str) -> str:
    """지정한 Actions 단계의 shell script 추출."""

    workflow = read_repository_file(".github/workflows/sync-translation.yml")
    step = workflow.split(f"      - name: {step_name}\n", 1)[1]
    step = step.split("\n      - name:", 1)[0]
    body = step.split("        run: |\n", 1)[1]
    return "\n".join(line[10:] if line else "" for line in body.splitlines())


class OperationalEntrypointTests(unittest.TestCase):
    """Actions·Makefile·Docker 운영 진입점 테스트 모음."""

    def test_sync_package_preserves_flat_module_imports(self) -> None:
        """기존 flat module import가 canonical package와 같은 객체인지 검증."""

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

    def test_actions_uses_only_the_sealed_workflow_phases(self) -> None:
        """번역 Actions가 봉인된 세 워크플로 phase만 호출하는지 검증."""

        workflow = read_repository_file(".github/workflows/sync-translation.yml")

        prepare = workflow.index("python workflow.py \"${args[@]}\"")
        publish = workflow.index("python workflow.py publish")
        deploy = workflow.index("python workflow.py deploy")
        self.assertLess(prepare, publish)
        self.assertLess(publish, deploy)
        self.assertIn("@openai/codex@latest", workflow)
        self.assertIn("codex --version", workflow)
        self.assertIn("uses: actions/checkout@v6", workflow)
        self.assertIn("uses: astral-sh/setup-uv@v9", workflow)
        self.assertIn("uses: actions/setup-node@v6", workflow)
        self.assertIn("uses: actions/upload-artifact@v7", workflow)
        self.assertNotRegex(workflow, r"uses: [^\n]+@[0-9a-f]{40}")
        self.assertIn("persist-credentials: false", workflow)

        for bypass in (
            "python main.py",
            "python replay.py",
            "python provider_check.py",
            "python validate_generated_changes.py",
            "git add -A",
            "git commit",
            "git push",
            "gh workflow run",
        ):
            self.assertNotIn(bypass, workflow)

        publish_step_start = workflow.index(
            "- name: Publish verified tree with compare-and-swap"
        )
        deploy_step_start = workflow.index(
            "- name: Trigger and verify production deployment"
        )
        prepare_step = workflow[
            workflow.index("- name: Prepare verified publication") : publish_step_start
        ]
        self.assertNotIn("GH_TOKEN", prepare_step)
        self.assertIn('--repository "$GITHUB_REPOSITORY"', prepare_step)
        for required_setting in (
            "TRANSLATION_MODEL_PROFILE",
            "TRANSLATION_CONTEXT_WINDOW_TOKENS",
            "TRANSLATION_RESERVED_OUTPUT_TOKENS",
            "TRANSLATION_REQUEST_TIMEOUT_SECONDS",
            "TRANSLATION_RUN_TIMEOUT_SECONDS",
            "TRANSLATION_TOKENIZER_ENCODING",
        ):
            self.assertIn(required_setting, prepare_step)
        for credential_setting in (
            "OPENAI_API_KEY",
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_API_VERSION",
            "AZURE_OPENAI_ENDPOINT",
            "CODEX_ACCESS_TOKEN",
            "CODEX_API_KEY",
            "CODEX_HOME",
        ):
            self.assertIn(credential_setting, prepare_step)
        self.assertIn("TRANSLATION_WORKFLOW_TIMEOUT_SECONDS: '7200'", prepare_step)
        self.assertNotIn("TRANSLATION_RETRY_DELAY", workflow)
        for unsupported_openai_setting in (
            "OPENAI_BASE_URL",
            "OPENAI_ORGANIZATION",
            "OPENAI_PROJECT",
        ):
            self.assertNotIn(unsupported_openai_setting, workflow)
        publish_step = workflow[publish_step_start:deploy_step_start]
        self.assertIn("GH_TOKEN", publish_step)
        for secret in (
            "OPENAI_API_KEY",
            "AZURE_OPENAI_API_KEY",
            "CODEX_ACCESS_TOKEN",
            "CODEX_API_KEY",
        ):
            self.assertNotIn(secret, publish_step)
        deploy_step = workflow[deploy_step_start:]
        self.assertNotIn('--repository "$GITHUB_REPOSITORY"', deploy_step)
        for secret in (
            "OPENAI_API_KEY",
            "AZURE_OPENAI_API_KEY",
            "CODEX_ACCESS_TOKEN",
            "CODEX_API_KEY",
        ):
            self.assertNotIn(secret, deploy_step)

    def test_actions_uploads_only_explicit_redacted_evidence(self) -> None:
        """Actions artifact가 허용된 redacted evidence로 제한되는지 검증."""

        workflow = read_repository_file(".github/workflows/sync-translation.yml")
        upload = workflow[workflow.index("- name: Upload redacted workflow evidence") :]

        self.assertIn("if: ${{ always() }}", upload)
        self.assertIn("translation-sync-failure.json", upload)
        self.assertIn("translation-sync-fixture-evidence.txt", upload)
        self.assertNotIn(".translation-sync-preparation-key", upload)
        self.assertNotIn("translation-sync-prepared.json", upload)
        self.assertNotIn("translation-sync-replay.json", upload)
        self.assertNotIn("translation-candidate-", upload)

    def test_deploy_workflow_validates_exact_main_commit(self) -> None:
        """배포 워크플로가 main의 정확한 commit과 correlation을 검증하는지 확인."""

        workflow = read_repository_file(".github/workflows/deploy.yml")

        self.assertIn("expected_commit:", workflow)
        self.assertIn("correlation_id:", workflow)
        self.assertIn("ACTUAL_COMMIT: ${{ github.sha }}", workflow)
        self.assertIn("[!A-Za-z0-9]*|*[!A-Za-z0-9._-]*", workflow)
        self.assertIn("[ \"${#EXPECTED_COMMIT}\" -ne 40 ]", workflow)
        self.assertIn("[ \"${#EXPECTED_COMMIT}\" -ne 64 ]", workflow)
        self.assertIn('[ "$ACTUAL_COMMIT" != "$EXPECTED_COMMIT" ]', workflow)
        self.assertIn("uses: actions/checkout@v6", workflow)
        self.assertIn("uses: actions/setup-node@v6", workflow)
        self.assertIn("uses: actions/configure-pages@v6", workflow)
        self.assertIn("uses: actions/upload-pages-artifact@v5", workflow)
        self.assertIn("uses: actions/deploy-pages@v5", workflow)
        self.assertNotRegex(workflow, r"uses: [^\n]+@[0-9a-f]{40}")

    def test_make_operational_targets_delegate_to_workflow_cli(self) -> None:
        """Make 운영 target이 credential을 분리해 workflow CLI에 위임하는지 검증."""

        makefile = read_repository_file("Makefile")

        self.assertIn("translation-prepare:", makefile)
        self.assertIn("python workflow.py \"$$@\"", makefile)
        self.assertIn("python workflow.py publish", makefile)
        self.assertIn("python workflow.py deploy", makefile)
        prepare_target = makefile[
            makefile.index("translation-prepare:") : makefile.index(
                "translation-publish:"
            )
        ]
        deploy_target = makefile[
            makefile.index("translation-deploy:") : makefile.index(
                "translation-run:"
            )
        ]
        self.assertIn('--repository "$$REPOSITORY"', prepare_target)
        self.assertNotIn('--repository "$$REPOSITORY"', deploy_target)
        self.assertIn("TRANSLATION_PUSH_ENV_KEYS),-u", prepare_target)
        self.assertIn("TRANSLATION_PROVIDER_ENV_KEYS),-u", makefile)
        self.assertNotIn("python main.py", makefile)
        self.assertIn("translation-replay-diagnostic:", makefile)
        self.assertIn("translation-provider-diagnostic:", makefile)
        self.assertIn("translation-path-diagnostic:", makefile)

    def test_translation_container_uses_the_same_workflow_cli(self) -> None:
        """번역 컨테이너가 read-only 저장소에서 같은 workflow CLI를 쓰는지 검증."""

        dockerfile = read_repository_file("Dockerfile.translate")
        compose = read_repository_file("docker-compose.yml")
        dockerignore = read_repository_file(".dockerignore")

        self.assertIn("FROM node:24-", dockerfile)
        self.assertIn("uv python install 3.14", dockerfile)
        self.assertIn("ca-certificates gh git", dockerfile)
        self.assertIn("@openai/codex@latest", dockerfile)
        self.assertIn("codex --version", dockerfile)
        self.assertIn("--registry=https://registry.npmjs.org", dockerfile)
        self.assertIn('"/workspace/translation-sync/workflow.py"', dockerfile)
        self.assertNotIn("main.py", dockerfile)
        self.assertNotIn("COPY .", dockerfile)
        self.assertNotIn("COPY translation-sync", dockerfile)

        self.assertIn("source: .", compose)
        self.assertIn("target: /workspace", compose)
        self.assertIn("read_only: true", compose)
        self.assertIn("target: /artifacts", compose)
        self.assertIn("source: translation-sync-artifacts", compose)
        self.assertIn("UV_PROJECT_ENVIRONMENT=/home/app/.venv", dockerfile)
        self.assertIn("target: /home/app/.venv", compose)
        for active_output_mount in (
            "./i18n:/workspace/i18n",
            "./versioned_docs:/workspace/versioned_docs",
            "./versioned_sidebars:/workspace/versioned_sidebars",
        ):
            self.assertNotIn(active_output_mount, compose)

        ignored = set(dockerignore.splitlines())
        self.assertIn(".env", ignored)
        self.assertIn(".env.*", ignored)
        self.assertIn("!.env.example", ignored)


class TranslationWorkflowTests(unittest.TestCase):
    """번역 워크플로 shell 경계 조건 테스트 모음."""

    def test_prepare_step_preserves_nonzero_workflow_status(self) -> None:
        """Actions 준비 단계가 비정상 워크플로 종료 코드를 보존하는지 검증."""

        script = workflow_run_script("Prepare verified publication")
        harness = 'uv() { return "$PREPARE_STATUS"; }\n' + script

        with tempfile.TemporaryDirectory() as tmp:
            for status in (2, 3):
                with self.subTest(status=status):
                    env = os.environ.copy()
                    env.update(
                        {
                            "TRANSLATION_ARTIFACT_ROOT": str(Path(tmp) / "artifacts"),
                            "TRANSLATION_PUSH_ENDPOINT": (
                                "https://github.com/owner/repository.git"
                            ),
                            "TARGET_BRANCH": "main",
                            "GITHUB_REPOSITORY": "owner/repository",
                            "INPUT_VERSION": "",
                            "INPUT_DOC": "",
                            "PREPARE_STATUS": str(status),
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


if __name__ == "__main__":
    unittest.main()
