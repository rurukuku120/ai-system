#!/usr/bin/env python3
"""
AI System Setup
새 컴퓨터에서 레포 클론 후 한 번 실행.
hooks/registry.json을 읽어 ~/.claude/settings.json에 훅을 자동 등록한다.

사용법:
    python scripts/setup.py
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DISPATCHER = REPO_ROOT / "hooks" / "dispatcher.py"
REGISTRY_PATH = REPO_ROOT / "hooks" / "registry.json"
SETTINGS_PATH = Path.home() / ".claude" / "settings.json"

# registry 키 → Claude Code 이벤트 이름
EVENT_MAP = {
    "stop": "Stop",
    "pre_tool_use": "PreToolUse",
    "post_tool_use": "PostToolUse",
    "notification": "Notification",
}


def main():
    # registry 읽기
    try:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[setup] registry.json 읽기 실패: {e}")
        sys.exit(1)

    # settings.json 읽기 (없으면 빈 dict)
    if SETTINGS_PATH.exists():
        try:
            settings = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        except Exception:
            settings = {}
    else:
        settings = {}

    hooks = settings.setdefault("hooks", {})

    # dispatcher 경로 (슬래시 통일)
    dispatcher_path = str(DISPATCHER).replace("\\", "/")

    changed = False
    for reg_key, claude_event in EVENT_MAP.items():
        entries = registry.get(reg_key, [])
        enabled = [e for e in entries if e.get("enabled", True)]
        if not enabled:
            continue

        command = f"python {dispatcher_path} {reg_key}"

        # 이미 등록된 경우 건너뜀
        existing = hooks.get(claude_event, [])
        already = any(
            h.get("command") == command
            for entry in existing
            for h in entry.get("hooks", [])
        )

        if already:
            print(f"[setup] 이미 등록됨: {claude_event}")
            continue

        hooks[claude_event] = [
            {
                "matcher": "",
                "hooks": [{"type": "command", "command": command}]
            }
        ]
        print(f"[setup] 등록: {claude_event} → dispatcher.py {reg_key}")
        changed = True

    if changed:
        SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
        SETTINGS_PATH.write_text(
            json.dumps(settings, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"[setup] 저장 완료: {SETTINGS_PATH}")
    else:
        print("[setup] 변경 사항 없음.")


if __name__ == "__main__":
    main()
