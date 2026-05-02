from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_package_scripts_do_not_call_github_automation_or_python():
    package = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
    scripts = package["scripts"]

    offenders = {
        name: command
        for name, command in scripts.items()
        if ".github/" in command or command.startswith("python") or " python" in command
    }

    assert offenders == {}
