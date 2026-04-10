"""
Agent Manager — agents/ 폴더를 스캔하여 README.md를 자동 갱신한다.
"""

import os
import re
from pathlib import Path
from datetime import datetime

AGENTS_DIR = Path(__file__).parent.parent
README_PATH = AGENTS_DIR / "README.md"
SKIP_DIRS = {"agent-manager"}


def parse_claude_md(path: Path) -> dict:
    """CLAUDE.md에서 핵심 정보를 추출한다."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # 첫 번째 H1을 이름으로 사용
    name = next((l.lstrip("# ").strip() for l in lines if l.startswith("# ")), path.parent.name)

    # ## 역할 섹션 추출
    role = ""
    in_role = False
    for line in lines:
        if re.match(r"^##\s+역할", line):
            in_role = True
            continue
        if in_role:
            if line.startswith("##"):
                break
            if line.strip():
                role += line.strip() + " "
    role = role.strip()

    # 트리거 힌트 추출 (훅, Actions, 수동 키워드)
    trigger = "수동 호출"
    text_lower = text.lower()
    hints = []
    if "github actions" in text_lower:
        hints.append("GitHub Actions")
    if "stop 훅" in text_lower or "stop hook" in text_lower:
        hints.append("Stop 훅")
    if "posttooluse" in text_lower:
        hints.append("PostToolUse 훅")
    if hints:
        trigger = " / ".join(hints)

    # 슬래시 커맨드 추출
    slash = ""
    m = re.search(r"`(/[\w-]+)`", text)
    if m:
        slash = m.group(1)

    return {
        "name": name,
        "folder": f"agents/{path.parent.name}/",
        "role": role or "(역할 미정의)",
        "trigger": trigger,
        "slash": slash,
    }


def collect_agents() -> list[dict]:
    agents = []
    for entry in sorted(AGENTS_DIR.iterdir()):
        if not entry.is_dir() or entry.name in SKIP_DIRS:
            continue
        claude_md = entry / "CLAUDE.md"
        if claude_md.exists():
            agents.append(parse_claude_md(claude_md))
    return agents


def render_readme(agents: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 요약 테이블
    table_rows = ""
    for a in agents:
        slash_col = f"`{a['slash']}`" if a["slash"] else "—"
        table_rows += f"| [{a['name']}](#{a['folder'].split('/')[1]}) | `{a['folder']}` | {a['trigger']} | {slash_col} |\n"

    # 상세 섹션
    detail_sections = ""
    for a in agents:
        agent_dir = a["folder"].split("/")[1]
        claude_md_path = AGENTS_DIR / agent_dir / "CLAUDE.md"
        raw = claude_md_path.read_text(encoding="utf-8")

        # H1 제거 (이미 섹션 헤더로 사용)
        raw = re.sub(r"^#\s+.+\n?", "", raw, count=1)
        detail_sections += f"## {a['name']}\n\n> 폴더: `{a['folder']}`\n\n{raw.strip()}\n\n---\n\n"

    return f"""# Agents 인덱스

> 자동 생성됨 — {now}
> `agents/agent-manager/runner.py`가 각 에이전트의 `CLAUDE.md`를 읽어 갱신합니다.
> 직접 편집하지 마세요. `/update-agents`로 갱신하세요.

---

## 에이전트 목록

| 에이전트 | 폴더 | 트리거 | 슬래시 커맨드 |
|----------|------|--------|--------------|
{table_rows}
---

{detail_sections}"""


def main():
    agents = collect_agents()
    content = render_readme(agents)
    README_PATH.write_text(content, encoding="utf-8")
    print(f"[agent-manager] README.md 갱신 완료 — 에이전트 {len(agents)}개")
    for a in agents:
        print(f"  • {a['name']} ({a['folder']})")


if __name__ == "__main__":
    main()
