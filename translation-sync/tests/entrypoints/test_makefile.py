"""초기화와 명시적 번역 실행의 Makefile 경계 검증."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


class MakefileEntrypointTests(unittest.TestCase):
    """외부 명령을 대체하고 실제 Make target을 실행하는 회귀 검사."""

    def run_make(self, target: str, **variables: str) -> list[dict]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copyfile(REPOSITORY_ROOT / "Makefile", root / "Makefile")
            shutil.copyfile(
                REPOSITORY_ROOT / "docker-compose.yml", root / "docker-compose.yml"
            )
            (root / ".env").write_text("OPENAI_API_KEY=fixture-only\n", encoding="utf-8")
            commands = root / "commands.jsonl"
            binaries = root / "bin"
            binaries.mkdir()
            fixture = f"#!{sys.executable}\n" + """\
import json
import os
import sys
from pathlib import Path

command = Path(sys.argv[0]).name
args = sys.argv[1:]
with Path(os.environ["MAKEFILE_TEST_COMMAND_LOG"]).open("a", encoding="utf-8") as log:
    log.write(json.dumps({"command": command, "args": args}) + "\\n")

if command == "docker":
    allowed = (
        args in (
            ["compose", "version"], ["info"],
            ["compose", "up", "-d", "build"], ["compose", "build", "translate"],
        )
        or (args[:2] == ["run", "--rm"] and "node:24-alpine" in args)
        or (args[:2] == ["compose", "run"] and "translate" in args)
    )
    if not allowed:
        raise SystemExit(97)
elif command == "curl":
    output = Path(args[args.index("-o") + 1])
    output.write_text("Behavioral guidelines to reduce common LLM coding mistakes\\n", encoding="utf-8")
elif command == "specify":
    sys.stdin.readline()
"""
            for command in ("docker", "curl", "specify"):
                executable = binaries / command
                executable.write_text(fixture, encoding="utf-8")
                executable.chmod(0o755)

            mktemp = binaries / "mktemp"
            mktemp.write_text(
                f"#!{sys.executable}\n"
                "import os, tempfile\n"
                "fd, path = tempfile.mkstemp(dir=os.environ['MAKEFILE_TEST_ROOT'])\n"
                "os.close(fd)\nprint(path)\n",
                encoding="utf-8",
            )
            mktemp.chmod(0o755)

            environment = {
                key: os.environ[key]
                for key in ("LANG", "LC_ALL", "TMPDIR", "SYSTEMROOT")
                if key in os.environ
            }
            environment.update(
                {
                    "PATH": str(binaries)
                    + os.pathsep
                    + os.environ.get("PATH", os.defpath),
                    "MAKEFILE_TEST_COMMAND_LOG": str(commands),
                    "MAKEFILE_TEST_ROOT": str(root),
                    "OPENAI_API_KEY": "fixture-only",
                }
            )
            result = subprocess.run(
                [
                    "make",
                    "--no-print-directory",
                    target,
                    *[f"{key}={value}" for key, value in variables.items()],
                ],
                cwd=root,
                env=environment,
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return [json.loads(line) for line in commands.read_text().splitlines()]

    def assert_initialization_only(self, calls: list[dict]) -> None:
        docker_calls = [call["args"] for call in calls if call["command"] == "docker"]
        self.assertEqual(docker_calls[:2], [["compose", "version"], ["info"]])
        self.assertEqual(len(docker_calls), 4)
        self.assertEqual(docker_calls[2], ["compose", "up", "-d", "build"])
        self.assertEqual(docker_calls[3][:2], ["run", "--rm"])
        self.assertIn("node:24-alpine", docker_calls[3])
        self.assertIn("npm install", docker_calls[3][-1])

    def test_init_prepares_dependencies_without_starting_translation(self) -> None:
        calls = self.run_make("init")
        self.assert_initialization_only(calls)
        self.assertEqual({call["command"] for call in calls}, {"docker"})

    def test_dev_runs_setup_targets_without_starting_translation(self) -> None:
        calls = self.run_make("dev")
        self.assert_initialization_only(calls)
        self.assertEqual(
            [call["command"] for call in calls],
            ["docker", "docker", "docker", "docker", "curl", "specify"],
        )
        self.assertEqual(
            calls[-1]["args"],
            ["init", "--here", "--ai", "claude", "--script", "sh"],
        )

    @unittest.skipUnless(shutil.which("docker"), "Docker is not installed")
    def test_compose_requires_translation_profile_for_default_startup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copyfile(
                REPOSITORY_ROOT / "docker-compose.yml", root / "docker-compose.yml"
            )
            (root / ".env").touch()
            environment = {"PATH": os.environ.get("PATH", os.defpath)}
            version = subprocess.run(
                ["docker", "compose", "version"], env=environment,
                capture_output=True, timeout=15, check=False,
            )
            if version.returncode:
                self.skipTest("Docker Compose is not installed")
            for profile, expected in (
                ([], ["build"]),
                (["--profile", "translation"], ["build", "translate"]),
            ):
                with self.subTest(profile=profile):
                    result = subprocess.run(
                        ["docker", "compose", *profile, "config", "--services"],
                        cwd=root,
                        env=environment,
                        capture_output=True,
                        text=True,
                        timeout=15,
                        check=False,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(sorted(result.stdout.splitlines()), expected)

    def test_translate_explicitly_builds_and_runs_the_selected_document(self) -> None:
        calls = self.run_make("translate", VERSION="13.x", DOC="collections.md")
        self.assertEqual([call["command"] for call in calls], ["docker", "docker"])
        self.assertEqual(calls[0]["args"], ["compose", "build", "translate"])
        run = calls[1]["args"]
        self.assertEqual(run[:2], ["compose", "run"])
        self.assertIn("--no-deps", run)
        self.assertEqual(
            run[-5:], ["translate", "--version", "13.x", "--doc", "collections.md"]
        )
        self.assertIn("TRANSLATION_PROVIDER=openai", run)
        self.assertIn("OPENAI_API_KEY", run)


if __name__ == "__main__":
    unittest.main()
