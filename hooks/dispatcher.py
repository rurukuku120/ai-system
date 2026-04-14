#!/usr/bin/env python3
"""
Claude Hook Dispatcher
registry.json에 등록된 훅을 이벤트 타입에 맞게 순서대로 실행한다.

사용법:
    python dispatcher.py <event>
    echo '{"session_id": "..."}' | python dispatcher.py stop
"""

import json
import sys
import subprocess
from pathlib import Path

HOOKS_DIR = Path(__file__).parent
REGISTRY_PATH = HOOKS_DIR / "registry.json"


def main():
    if len(sys.argv) < 2:
        print("[dispatcher] 이벤트 인수 없음. 예: dispatcher.py stop", file=sys.stderr)
        sys.exit(1)

    event = sys.argv[1]
    stdin_data = sys.stdin.read()

    try:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[dispatcher] registry.json 읽기 실패: {e}", file=sys.stderr)
        sys.exit(1)

    hooks = registry.get(event, [])
    enabled = [h for h in hooks if h.get("enabled", True)]

    if not enabled:
        sys.exit(0)

    for hook in enabled:
        script = HOOKS_DIR / hook["script"]
        if not script.exists():
            print(f"[dispatcher] 스크립트 없음: {script}", file=sys.stderr)
            continue

        try:
            result = subprocess.run(
                [sys.executable, str(script)],
                input=stdin_data,
                text=True,
                capture_output=True,
            )
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, end="", file=sys.stderr)
        except Exception as e:
            print(f"[dispatcher] 실행 오류 ({hook['id']}): {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
