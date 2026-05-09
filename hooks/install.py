#!/usr/bin/env python3
"""Install local automation hooks declared by hooks/ sources."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
GIT_HOOKS_DIR = REPO_ROOT / ".git" / "hooks"
PRE_COMMIT_SOURCE = REPO_ROOT / "hooks" / "git" / "pre-commit"
PRE_COMMIT_TARGET = GIT_HOOKS_DIR / "pre-commit"


def install_git_hook(source: Path, target: Path) -> None:
    if not source.exists():
        raise SystemExit(f"[hooks/install] hook source not found: {source}")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    target.chmod(target.stat().st_mode | 0o111)
    print(f"[hooks/install] installed {target}")


def main() -> None:
    if not (REPO_ROOT / ".git").exists():
        raise SystemExit("[hooks/install] .git directory not found")

    install_git_hook(PRE_COMMIT_SOURCE, PRE_COMMIT_TARGET)


if __name__ == "__main__":
    main()
