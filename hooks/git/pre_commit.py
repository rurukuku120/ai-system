#!/usr/bin/env python3
"""Pre-commit automation for ai-system."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def run(args: list[str]) -> None:
    subprocess.run(args, cwd=REPO_ROOT, check=True)


def main() -> int:
    python = sys.executable
    tasks = [
        [python, "scripts/update_readme.py"],
        [python, "monitoring/health_check.py"],
    ]

    try:
        for task in tasks:
            run(task)
        run(["git", "add", "README.md", "agents/STATUS.md", "agents/status.json"])
    except subprocess.CalledProcessError as exc:
        print(f"[pre-commit] failed: {' '.join(exc.cmd)}", file=sys.stderr)
        return exc.returncode or 1

    print("[pre-commit] README and agent status updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
