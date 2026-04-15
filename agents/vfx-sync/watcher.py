#!/usr/bin/env python3
"""
파일 변경 감지 모듈
스냅샷 비교 방식으로 네트워크 드라이브(Z:)에서도 안정적으로 동작.
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FileChange:
    added: list[str] = field(default_factory=list)
    modified: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        return bool(self.added or self.modified or self.removed)

    @property
    def total(self) -> int:
        return len(self.added) + len(self.modified) + len(self.removed)


def snapshot(directory: str, extensions: set[str] | None = None) -> dict[str, dict]:
    """디렉토리의 파일 상태 스냅샷 생성.

    Returns:
        {filename: {"mtime": float, "size": int}}
    """
    result = {}
    dir_path = Path(directory)
    if not dir_path.exists():
        return result

    for f in dir_path.iterdir():
        if not f.is_file():
            continue
        if extensions and f.suffix.lower() not in extensions:
            continue
        stat = f.stat()
        result[f.name] = {
            "mtime": stat.st_mtime,
            "size": stat.st_size,
        }
    return result


def diff(old: dict[str, dict], new: dict[str, dict]) -> FileChange:
    """두 스냅샷을 비교하여 변경 사항 반환."""
    old_keys = set(old.keys())
    new_keys = set(new.keys())

    added = sorted(new_keys - old_keys)
    removed = sorted(old_keys - new_keys)

    modified = []
    for name in sorted(old_keys & new_keys):
        if old[name]["mtime"] != new[name]["mtime"] or old[name]["size"] != new[name]["size"]:
            modified.append(name)

    return FileChange(added=added, modified=modified, removed=removed)


def save_snapshot(snap: dict[str, dict], path: Path) -> None:
    """스냅샷을 JSON 파일로 저장."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snap, indent=2), encoding="utf-8")


def load_snapshot(path: Path) -> dict[str, dict]:
    """JSON 파일에서 스냅샷 로드. 파일이 없으면 빈 딕셔너리 반환."""
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


# ── CLI ────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="파일 변경 감지")
    parser.add_argument("directory", help="감시할 디렉토리")
    parser.add_argument("--extensions", nargs="*", help="감시할 확장자 (예: .xml .dds)")
    parser.add_argument("--snapshot-file", help="스냅샷 저장/로드 경로")
    parser.add_argument("--save-only", action="store_true", help="스냅샷만 저장 (비교 안 함)")
    args = parser.parse_args()

    exts = set(args.extensions) if args.extensions else None
    snap_path = Path(args.snapshot_file) if args.snapshot_file else Path(f".snapshots/{Path(args.directory).name}.json")

    current = snapshot(args.directory, exts)
    print(f"[스냅샷] {len(current)}개 파일 감지: {args.directory}")

    if args.save_only:
        save_snapshot(current, snap_path)
        print(f"[저장] {snap_path}")
    else:
        previous = load_snapshot(snap_path)
        changes = diff(previous, current)

        if changes.has_changes:
            print(f"[변경] 추가: {len(changes.added)}, 수정: {len(changes.modified)}, 삭제: {len(changes.removed)}")
            for f in changes.added:
                print(f"  + {f}")
            for f in changes.modified:
                print(f"  ~ {f}")
            for f in changes.removed:
                print(f"  - {f}")
        else:
            print("[변경 없음]")

        save_snapshot(current, snap_path)
        print(f"[저장] {snap_path}")
