#!/usr/bin/env python3
"""
update_readme.py — 루트 README.md 자동 생성 스크립트

다음 항목을 스캔하여 루트 README.md를 갱신한다:
- agents/          에이전트 목록 (CLAUDE.md 파싱)
- .claude/commands/ 슬래시 커맨드 목록
- .github/workflows/ 워크플로우 목록
"""

import re
from datetime import datetime
from pathlib import Path

REPO_ROOT     = Path(__file__).parent.parent
AGENTS_DIR    = REPO_ROOT / "agents"
COMMANDS_DIR  = REPO_ROOT / ".claude" / "commands"
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"
README_PATH   = REPO_ROOT / "README.md"

SKIP_AGENTS = {"agent-manager"}


def collect_agents() -> list[dict]:
    agents = []
    for entry in sorted(AGENTS_DIR.iterdir()):
        if not entry.is_dir() or entry.name in SKIP_AGENTS:
            continue
        claude_md = entry / "CLAUDE.md"
        if not claude_md.exists():
            continue

        text = claude_md.read_text(encoding="utf-8")
        lines = text.splitlines()

        name = next((l.lstrip("# ").strip() for l in lines if l.startswith("# ")), entry.name)

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

        agents.append({
            "folder": entry.name,
            "name": name,
            "role": role.strip() or "—",
        })
    return agents


def collect_commands() -> list[dict]:
    commands = []
    for f in sorted(COMMANDS_DIR.glob("*.md")):
        first_line = f.read_text(encoding="utf-8").splitlines()
        desc = next((l.strip() for l in first_line if l.strip() and not l.startswith("#")), "—")
        desc = desc[:60] + ("…" if len(desc) > 60 else "")
        commands.append({"name": f"/{f.stem}", "desc": desc})
    return commands


def collect_workflows() -> list[dict]:
    workflows = []
    for f in sorted(WORKFLOWS_DIR.glob("*.yml")):
        text = f.read_text(encoding="utf-8")
        m = re.search(r"^name:\s*(.+)", text, re.MULTILINE)
        name = m.group(1).strip() if m else f.stem
        workflows.append({"file": f.name, "name": name})
    return workflows


# 폴더별 설명 사전 — 새 폴더 추가 시 여기에만 추가하면 됨
FOLDER_DESCRIPTIONS: dict[str, str] = {
    "agents":     "에이전트 정의 및 실행 스크립트",
    "common":     "전체 에이전트 공통 기반 (규칙/형식/프로토콜/스키마)",
    "config":     "환경별 설정 (dev / staging / prod)",
    "docs":       "대시보드 및 문서",
    "hooks":      "Claude Code 훅 (dispatcher, registry)",
    "inbox":      "VFX 작업물 피드백 요청 이미지 투입 폴더",
    "logs":       "세션 로그",
    "memory":     "에이전트 학습 결과 누적",
    "models":     "LLM별 개별 지침 (claude / gemini / gpt)",
    "monitoring": "실행 로그, 오류 추적, 성능 지표",
    "projects":   "프로젝트별 결과물 저장",
    "scripts":    "유틸리티 스크립트",
    "security":   "접근 권한, API 키 관리 기준",
    "sync":       "외부 시스템 연동 (Notion / GitHub)",
    ".claude":    "Claude Code 설정 및 슬래시 커맨드 정의",
    ".github":    "GitHub Actions 워크플로우",
}

SKIP_FOLDERS = {".git", "__pycache__"}


def collect_folders() -> list[dict]:
    """루트 폴더를 스캔하여 존재하는 폴더 목록 반환 (숨김 폴더 포함)"""
    folders = []
    for entry in sorted(REPO_ROOT.iterdir(), key=lambda p: p.name.lower()):
        if not entry.is_dir() or entry.name in SKIP_FOLDERS:
            continue
        desc = FOLDER_DESCRIPTIONS.get(entry.name, "—")
        folders.append({"name": entry.name, "desc": desc})
    return folders


def render(agents: list[dict], commands: list[dict], workflows: list[dict], folders: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    agent_rows = "".join(
        f"| `agents/{a['folder']}/` | {a['name']} | {a['role'][:60]} |\n"
        for a in agents
    )

    command_rows = "".join(
        f"| `{c['name']}` | {c['desc']} |\n"
        for c in commands
    )

    workflow_rows = "".join(
        f"| `{w['file']}` | {w['name']} |\n"
        for w in workflows
    )

    folder_rows = "".join(
        f"| `{f['name']}/` | {f['desc']} |\n"
        for f in folders
    )

    return f"""# ai-system

> 자동 생성됨 — {now}
> `scripts/update_readme.py`가 갱신합니다. 직접 편집하지 마세요.

Nexon VFX팀의 AI 도구 및 에이전트 관리 저장소.

---

## 폴더 구조

| 폴더 | 설명 |
|------|------|
{folder_rows}

---

## 에이전트

| 폴더 | 이름 | 역할 |
|------|------|------|
{agent_rows}
→ 상세: [`agents/README.md`](agents/README.md)

---

## 슬래시 커맨드

| 커맨드 | 설명 |
|--------|------|
{command_rows}
---

## GitHub Actions 워크플로우

| 파일 | 이름 |
|------|------|
{workflow_rows}
"""


def main():
    agents    = collect_agents()
    commands  = collect_commands()
    workflows = collect_workflows()
    folders   = collect_folders()
    content   = render(agents, commands, workflows, folders)
    README_PATH.write_text(content, encoding="utf-8")
    print(f"[update_readme] README.md 갱신 완료 - 에이전트 {len(agents)}개, 커맨드 {len(commands)}개, 워크플로우 {len(workflows)}개")


if __name__ == "__main__":
    main()
