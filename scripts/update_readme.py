#!/usr/bin/env python3
"""Generate the root README from the current repository structure."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
README_PATH = REPO_ROOT / "README.md"
AGENTS_DIR = REPO_ROOT / "agents"


INSTRUCTION_FILES = [
    ("AGENTS.md", "공통 원본 지침"),
    ("CLAUDE.md", "Claude Code용 진입점"),
    ("GEMINI.md", "Gemini용 진입점"),
    ("models/", "모델별 부록"),
]


FOLDER_DESCRIPTIONS = {
    ".claude": "Claude Code 설정과 슬래시 커맨드",
    ".github": "GitHub Actions 워크플로우",
    "agents": "업무 단위 에이전트와 템플릿",
    "common": "공통 규칙, 프로토콜, 스키마, 테스트 케이스",
    "config": "환경별 설정",
    "docs": "운영 문서와 아키텍처",
    "hooks": "자동화 hook, scheduler, trigger 중앙 관제",
    "memory": "장기 메모리와 운영 노트",
    "models": "모델별 부록",
    "monitoring": "상태 점검",
    "projects": "프로젝트별 산출물",
    "scripts": "관리 스크립트",
    "security": "보안 기준",
    "skills": "AI와 CLI가 재사용하는 skill",
    "sync": "외부 시스템 동기화",
    "wiki": "AI가 읽고 사람이 관리하는 지식 베이스",
}


def read_manifest_value(path: Path, key: str) -> str:
    if not path.exists():
        return ""
    prefix = f"{key}:"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return ""


def collect_agents() -> list[dict[str, str]]:
    agents = []
    for entry in sorted(AGENTS_DIR.iterdir()):
        if not entry.is_dir() or entry.name.startswith((".", "_")):
            continue
        manifest = entry / "agent.yaml"
        if not manifest.exists():
            continue
        agents.append(
            {
                "id": read_manifest_value(manifest, "id") or entry.name,
                "name": read_manifest_value(manifest, "name") or entry.name,
                "description": read_manifest_value(manifest, "description") or "-",
                "entrypoint": read_manifest_value(manifest, "entrypoint") or "-",
            }
        )
    return agents


def collect_folders() -> list[dict[str, str]]:
    folders = []
    for entry in sorted(REPO_ROOT.iterdir(), key=lambda p: p.name.lower()):
        if not entry.is_dir() or entry.name == ".git":
            continue
        folders.append(
            {
                "name": entry.name,
                "description": FOLDER_DESCRIPTIONS.get(entry.name, "-"),
            }
        )
    return folders


def render() -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    instructions = [
        {
            "file": file,
            "role": role,
            "status": "yes" if (REPO_ROOT / file).exists() else "-",
        }
        for file, role in INSTRUCTION_FILES
    ]
    folders = collect_folders()
    agents = collect_agents()

    instruction_rows = "".join(
        f"| `{item['file']}` | {item['role']} | {item['status']} |\n"
        for item in instructions
    )
    folder_rows = "".join(
        f"| `{item['name']}/` | {item['description']} |\n"
        for item in folders
    )
    agent_rows = "".join(
        f"| `{item['id']}` | {item['name']} | `{item['entrypoint']}` | {item['description']} |\n"
        for item in agents
    )
    if not agent_rows:
        agent_rows = "| - | - | - | 아직 등록된 에이전트가 없습니다. |\n"

    return f"""# ai-system

> 자동 생성됨 - {now}
> `scripts/update_readme.py`가 갱신합니다.

Claude, Codex/GPT, Gemini가 같은 에이전트 구조를 읽고 실행할 수 있도록 설계한 운영 저장소다.

## 지침 체계

| 파일 | 역할 | 상태 |
|---|---|---|
{instruction_rows}
설계 기준: [`docs/architecture/llm-agent-operating-model.md`](docs/architecture/llm-agent-operating-model.md)

## 폴더 구조

| 폴더 | 설명 |
|---|---|
{folder_rows}
## 에이전트

| ID | 이름 | 진입점 | 설명 |
|---|---|---|---|
{agent_rows}
## 기본 명령

```powershell
python monitoring/health_check.py
python scripts/update_readme.py
```
"""


def main() -> None:
    README_PATH.write_text(render(), encoding="utf-8")
    print("[update_readme] README.md generated")


if __name__ == "__main__":
    main()
