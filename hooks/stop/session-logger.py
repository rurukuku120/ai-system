#!/usr/bin/env python3
"""
Session Logger Hook
세션 종료 시 JSONL 로그를 마크다운으로 변환하고 GitHub에 푸시.
dispatcher.py를 통해 Stop 이벤트에서 실행된다.
"""

import json
import sys
import os
import socket
import subprocess
from pathlib import Path
from datetime import datetime

# ── 설정 ──────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent.parent  # ai-system/
LOG_DIR = REPO_ROOT / "logs" / "sessions"
PROJECTS_DIR = Path.home() / ".claude" / "projects"


def find_jsonl(session_id: str) -> Path | None:
    """~/.claude/projects/ 하위에서 session_id에 해당하는 JSONL 파일 탐색."""
    for path in PROJECTS_DIR.rglob(f"{session_id}.jsonl"):
        return path
    return None


def parse_jsonl(jsonl_path: Path) -> dict:
    """JSONL 파일에서 대화 내용과 메타데이터 추출."""
    messages = []
    meta = {}

    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            entry_type = entry.get("type", "")

            if not meta and entry.get("cwd"):
                meta = {
                    "session_id": entry.get("sessionId", ""),
                    "cwd": entry.get("cwd", ""),
                    "version": entry.get("version", ""),
                    "timestamp": entry.get("timestamp", ""),
                    "git_branch": entry.get("gitBranch", ""),
                    "user_type": entry.get("userType", "external"),
                    "entrypoint": entry.get("entrypoint", "cli"),
                }

            if entry_type == "user":
                content = entry.get("message", {}).get("content", "")
                if isinstance(content, list):
                    text = " ".join(
                        c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"
                    )
                elif isinstance(content, str):
                    text = content
                else:
                    text = ""
                if text.strip():
                    messages.append({"role": "User", "text": text.strip()})

            elif entry_type == "assistant":
                content = entry.get("message", {}).get("content", [])
                if isinstance(content, list):
                    text = " ".join(
                        c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"
                    )
                elif isinstance(content, str):
                    text = content
                else:
                    text = ""
                if text.strip():
                    messages.append({"role": "Assistant", "text": text.strip()})

    return {"meta": meta, "messages": messages}


def get_github_account() -> str:
    """현재 로그인된 GitHub 계정명 반환."""
    try:
        result = subprocess.run(
            ["gh", "api", "user", "--jq", ".login"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() or "-"
    except Exception:
        try:
            result = subprocess.run(
                ["git", "config", "user.email"],
                capture_output=True, text=True, timeout=5
            )
            return result.stdout.strip() or "-"
        except Exception:
            return "-"


def to_markdown(data: dict, session_id: str) -> str:
    """파싱된 데이터를 마크다운으로 변환."""
    meta = data["meta"]
    messages = data["messages"]

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    session_short = session_id[:8]

    lines = [
        f"# Session Log — {now}",
        "",
        f"**Session ID:** {session_short}",
        f"**Computer:** {socket.gethostname()}",
        f"**GitHub:** {get_github_account()}",
        f"**Claude 계정 유형:** {meta.get('user_type', 'external')} ({meta.get('entrypoint', 'cli')})",
        f"**Project:** {meta.get('cwd', 'unknown')}",
        f"**Branch:** {meta.get('git_branch', '-')}",
        f"**Claude Code:** v{meta.get('version', 'unknown')}",
        "",
        "---",
        "",
        "## 대화",
        "",
    ]

    for msg in messages:
        lines.append(f"### {msg['role']}")
        lines.append("")
        lines.append(msg["text"])
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def git_push(log_path: Path) -> bool:
    """변경된 로그 파일을 git commit & push."""
    try:
        subprocess.run(["git", "add", str(log_path)], cwd=REPO_ROOT, check=True, capture_output=True)
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=REPO_ROOT,
            capture_output=True,
        )
        if result.returncode == 0:
            return True

        date_str = datetime.now().strftime("%Y-%m-%d")
        subprocess.run(
            ["git", "commit", "-m", f"chore: session log {date_str} [skip ci]"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
        )
        subprocess.run(["git", "push"], cwd=REPO_ROOT, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[session-logger] git 오류: {e}", file=sys.stderr)
        return False


def main():
    try:
        data = json.loads(sys.stdin.read())
        session_id = data.get("session_id", "")
    except Exception:
        session_id = ""

    if not session_id:
        print("[session-logger] session_id 없음, 종료.", file=sys.stderr)
        sys.exit(0)

    jsonl_path = find_jsonl(session_id)
    if not jsonl_path:
        print(f"[session-logger] JSONL 파일 없음: {session_id}", file=sys.stderr)
        sys.exit(0)

    parsed = parse_jsonl(jsonl_path)
    if not parsed["messages"]:
        print("[session-logger] 대화 내용 없음, 건너뜀.", file=sys.stderr)
        sys.exit(0)

    md_content = to_markdown(parsed, session_id)

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_path = LOG_DIR / f"{date_str}_{session_id[:8]}.md"
    log_path.write_text(md_content, encoding="utf-8")

    print(f"[session-logger] 로그 저장: {log_path.name}")

    if git_push(log_path):
        print("[session-logger] GitHub 푸시 완료.")


if __name__ == "__main__":
    main()
