#!/usr/bin/env python3
"""
Agent Health Check
agents/ 하위 에이전트 상태를 점검하고 STATUS.md + status.json 생성.
"""

import json
import subprocess
import ast
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent
AGENTS_DIR = REPO_ROOT / "agents"
STATUS_MD = AGENTS_DIR / "STATUS.md"
STATUS_JSON = AGENTS_DIR / "status.json"


def check_agent(agent_dir: Path) -> dict:
    """에이전트 폴더를 점검하고 상태 반환."""
    name = agent_dir.name
    issues = []

    # 필수 파일 존재 여부
    has_claude_md = (agent_dir / "CLAUDE.md").exists()
    has_runner = (agent_dir / "runner.py").exists()

    if not has_claude_md:
        issues.append("CLAUDE.md 없음")
    if not has_runner:
        issues.append("runner.py 없음")

    # runner.py 문법 검사
    syntax_ok = None
    if has_runner:
        try:
            source = (agent_dir / "runner.py").read_text(encoding="utf-8")
            ast.parse(source)
            syntax_ok = True
        except SyntaxError as e:
            syntax_ok = False
            issues.append(f"문법 오류: {e.msg} (line {e.lineno})")

    # 마지막 git 커밋 시간
    last_commit = get_last_commit(agent_dir)

    # 상태 결정
    if not has_claude_md or not has_runner:
        status = "error"
        icon = "❌"
    elif syntax_ok is False:
        status = "error"
        icon = "❌"
    elif issues:
        status = "warning"
        icon = "⚠️"
    else:
        status = "healthy"
        icon = "✅"

    return {
        "name": name,
        "status": status,
        "icon": icon,
        "has_claude_md": has_claude_md,
        "has_runner": has_runner,
        "syntax_ok": syntax_ok,
        "last_commit": last_commit,
        "issues": issues,
    }


def get_last_commit(path: Path) -> str:
    """해당 경로의 마지막 git 커밋 시간 반환."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ci", "--", str(path)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=5,
        )
        raw = result.stdout.strip()
        if raw:
            # "2026-04-10 23:30:00 +0900" → "2026-04-10 23:30"
            return raw[:16]
        return "-"
    except Exception:
        return "-"


def build_status_md(results: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = len(results)
    healthy = sum(1 for r in results if r["status"] == "healthy")
    warning = sum(1 for r in results if r["status"] == "warning")
    error = sum(1 for r in results if r["status"] == "error")

    lines = [
        "# Agent Status",
        "",
        f"> 마지막 점검: {now}  ",
        "> `scripts/health_check.py` 로 자동 생성됨.",
        "",
        "---",
        "",
        "## 요약",
        "",
        f"- 전체: **{total}개**",
        f"- ✅ 정상: **{healthy}개**",
        f"- ⚠️ 경고: **{warning}개**",
        f"- ❌ 오류: **{error}개**",
        "",
        "---",
        "",
        "## 상태 목록",
        "",
        "| 에이전트 | 상태 | CLAUDE.md | runner.py | 문법 | 마지막 커밋 |",
        "|---|---|---|---|---|---|",
    ]

    for r in results:
        claude_md = "✅" if r["has_claude_md"] else "❌"
        runner = "✅" if r["has_runner"] else "❌"
        syntax = "✅" if r["syntax_ok"] else ("❌" if r["syntax_ok"] is False else "-")
        lines.append(
            f"| {r['name']} | {r['icon']} {r['status']} | {claude_md} | {runner} | {syntax} | {r['last_commit']} |"
        )

    # 이슈가 있는 에이전트 상세
    issues_list = [r for r in results if r["issues"]]
    if issues_list:
        lines += [
            "",
            "---",
            "",
            "## 이슈",
            "",
        ]
        for r in issues_list:
            lines.append(f"### {r['name']}")
            lines.append("")
            for issue in r["issues"]:
                lines.append(f"- {issue}")
            lines.append("")

    return "\n".join(lines) + "\n"


def main():
    agent_dirs = sorted([d for d in AGENTS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")])

    if not agent_dirs:
        print("[health-check] 에이전트 없음.")
        return

    results = [check_agent(d) for d in agent_dirs]

    # STATUS.md 저장
    STATUS_MD.write_text(build_status_md(results), encoding="utf-8")

    # status.json 저장
    STATUS_JSON.write_text(
        json.dumps(
            {
                "updated_at": datetime.now().isoformat(),
                "agents": results,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # 결과 출력
    print(f"[health-check] {len(results)}개 에이전트 점검 완료")
    for r in results:
        print(f"  [{r['status']}] {r['name']}")
        for issue in r["issues"]:
            print(f"      ! {issue}")


if __name__ == "__main__":
    main()
