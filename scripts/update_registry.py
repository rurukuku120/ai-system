#!/usr/bin/env python3
"""
Agent Registry Updater
agents/ 하위 에이전트를 스캔해서 agents/README.md를 자동 갱신.
새 에이전트 추가 시 수동 또는 훅으로 실행.
"""

import re
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent
AGENTS_DIR = REPO_ROOT / "agents"
REGISTRY_PATH = AGENTS_DIR / "README.md"


def parse_agent(claude_md: Path) -> dict:
    """CLAUDE.md에서 이름, 역할, 슬래시 커맨드 추출."""
    text = claude_md.read_text(encoding="utf-8")
    lines = text.splitlines()

    # 이름: 첫 번째 # 헤딩
    name = ""
    for line in lines:
        if line.startswith("# "):
            name = line[2:].strip()
            break

    # 역할: ## 역할 바로 아래 첫 번째 비어있지 않은 줄
    role = ""
    in_role = False
    for line in lines:
        if re.match(r"^## 역할", line):
            in_role = True
            continue
        if in_role:
            if line.startswith("##"):
                break
            if line.strip():
                role = line.strip()
                break

    # 슬래시 커맨드: CLAUDE.md 내 `/커맨드명` 패턴 탐색
    commands = re.findall(r"`(/[\w-]+)`", text)
    command = commands[0] if commands else "-"

    # 트리거: Stop 훅 여부
    trigger = "Stop 훅 (자동)" if "Stop" in text else "수동"

    return {
        "dir": claude_md.parent.name,
        "name": name or claude_md.parent.name,
        "role": role or "-",
        "command": command,
        "trigger": trigger,
    }


def build_registry(agents: list[dict]) -> str:
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "# Agent Registry",
        "",
        f"> 마지막 갱신: {updated_at}  ",
        "> `scripts/update_registry.py` 로 자동 생성됨.",
        "",
        "---",
        "",
        "## 에이전트 목록",
        "",
        "| 에이전트 | 역할 | 슬래시 커맨드 | 트리거 |",
        "|---|---|---|---|",
    ]

    for a in agents:
        dir_link = f"[{a['name']}](./{a['dir']}/CLAUDE.md)"
        lines.append(f"| {dir_link} | {a['role']} | `{a['command']}` | {a['trigger']} |")

    lines += [
        "",
        "---",
        "",
        "## 에이전트 상세",
        "",
    ]

    for a in agents:
        lines += [
            f"### {a['name']}",
            "",
            f"- **폴더:** `agents/{a['dir']}/`",
            f"- **역할:** {a['role']}",
            f"- **커맨드:** `{a['command']}`",
            f"- **트리거:** {a['trigger']}",
            f"- **상세:** [{a['dir']}/CLAUDE.md](./{a['dir']}/CLAUDE.md)",
            "",
        ]

    lines += [
        "---",
        "",
        "## 새 에이전트 추가 방법",
        "",
        "1. `agents/[에이전트명]/` 폴더 생성",
        "2. `CLAUDE.md` 작성 — `## 역할` 섹션 필수",
        "3. `runner.py` 구현",
        "4. `.claude/commands/[에이전트명].md` 슬래시 커맨드 등록",
        "5. `python scripts/update_registry.py` 실행 (또는 자동 갱신)",
    ]

    return "\n".join(lines) + "\n"


def main():
    claude_mds = sorted(AGENTS_DIR.glob("*/CLAUDE.md"))

    if not claude_mds:
        print("[registry] 에이전트 없음.")
        return

    agents = [parse_agent(p) for p in claude_mds]
    content = build_registry(agents)
    REGISTRY_PATH.write_text(content, encoding="utf-8")

    print(f"[registry] {len(agents)}개 에이전트 등록 완료 → agents/README.md")
    for a in agents:
        print(f"  - {a['name']} ({a['dir']})")


if __name__ == "__main__":
    main()
