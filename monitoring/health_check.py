#!/usr/bin/env python3
"""Check agent manifests and entrypoints."""

from __future__ import annotations

import ast
import json
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / "agents"
STATUS_PATH = AGENTS_DIR / "status.json"
STATUS_MD_PATH = AGENTS_DIR / "STATUS.md"


def read_manifest(path: Path) -> dict[str, object]:
    data: dict[str, object] = {}
    stack: list[tuple[int, object]] = []
    current_list_key = ""

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if line.startswith("- ") and current_list_key:
            value = line[2:].strip()
            target = data.setdefault(current_list_key, [])
            if isinstance(target, list):
                if ":" in value:
                    key, item_value = value.split(":", 1)
                    target.append({key.strip(): item_value.strip().strip('"').strip("'")})
                else:
                    target.append(value.strip('"').strip("'"))
            continue

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not value:
            if indent == 0:
                data[key] = []
                current_list_key = key
            continue

        if indent == 0:
            data[key] = value.strip('"').strip("'")
            current_list_key = ""

    return data


def check_syntax(path: Path) -> bool | None:
    if not path.exists() or path.suffix != ".py":
        return None
    try:
        ast.parse(path.read_text(encoding="utf-8"))
        return True
    except SyntaxError:
        return False


def check_agent(agent_dir: Path) -> dict[str, object]:
    manifest_path = agent_dir / "agent.yaml"
    issues: list[str] = []

    if not manifest_path.exists():
        return {
            "id": agent_dir.name,
            "status": "warning",
            "issues": ["agent.yaml 없음"],
        }

    manifest = read_manifest(manifest_path)
    agent_id = str(manifest.get("id") or agent_dir.name)
    entrypoint = str(manifest.get("entrypoint") or "")
    entrypoint_path = REPO_ROOT / entrypoint if entrypoint else Path()

    for key in ["id", "name", "version", "entrypoint", "description"]:
        if not manifest.get(key):
            issues.append(f"{key} 없음")

    if entrypoint and not entrypoint_path.exists():
        issues.append(f"entrypoint 없음: {entrypoint}")

    syntax_ok = check_syntax(entrypoint_path) if entrypoint else None
    if syntax_ok is False:
        issues.append(f"Python 문법 오류: {entrypoint}")

    status = "healthy" if not issues else "error"

    return {
        "id": agent_id,
        "name": manifest.get("name", agent_id),
        "entrypoint": entrypoint,
        "status": status,
        "syntax_ok": syntax_ok,
        "issues": issues,
    }


def build_markdown(results: list[dict[str, object]]) -> str:
    healthy = sum(1 for item in results if item["status"] == "healthy")
    warning = sum(1 for item in results if item["status"] == "warning")
    error = sum(1 for item in results if item["status"] == "error")

    rows = ""
    for item in results:
        rows += (
            f"| {item['id']} | {item.get('name', '-')} | {item['status']} | "
            f"`{item.get('entrypoint', '-')}` | {item.get('syntax_ok', '-')} |\n"
        )

    details = ""
    for item in results:
        issues = item.get("issues", [])
        if issues:
            details += f"\n### {item['id']}\n\n"
            for issue in issues:
                details += f"- {issue}\n"

    issue_text = details or "\n없음\n"

    return f"""# Agent Status

> 마지막 점검: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## 요약

- 전체: {len(results)}
- 정상: {healthy}
- 경고: {warning}
- 오류: {error}

## 목록

| ID | 이름 | 상태 | 진입점 | 문법 |
|---|---|---|---|---|
{rows}
## 이슈
{issue_text}
"""


def main() -> None:
    results = [
        check_agent(path)
        for path in sorted(AGENTS_DIR.iterdir())
        if path.is_dir() and not path.name.startswith((".", "_"))
    ]
    payload = {
        "updated_at": datetime.now().isoformat(),
        "agents": results,
    }
    STATUS_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    STATUS_MD_PATH.write_text(build_markdown(results), encoding="utf-8")
    print(f"[health-check] checked {len(results)} agents")
    for item in results:
        print(f"  [{item['status']}] {item['id']}")


if __name__ == "__main__":
    main()
