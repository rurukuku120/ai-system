#!/usr/bin/env python3
"""
VFX Sync Agent
라이브(마비노기) VFX 리소스 변경 감지 → 4K 업스케일 + 언리얼 임포트 자동화.

파이프라인:
  A. XML 변경 → UnrealEditor-Cmd.exe → Effect Import Tool
  B. DDS 변경 → Real-ESRGAN 4K 업스케일 → UnrealEditor-Cmd.exe → 텍스처 임포트
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml

# ── 경로 설정 ──────────────────────────────────────────────
AGENT_DIR = Path(__file__).parent
REPO_ROOT = AGENT_DIR.parent.parent
CONFIG_PATH = AGENT_DIR / "config.yaml"
UNREAL_SCRIPTS_DIR = AGENT_DIR / "unreal_scripts"
RESULTS_DIR = REPO_ROOT / "projects/nexon/mabinogi-eternity/sync/results"

sys.path.insert(0, str(AGENT_DIR))
from watcher import FileChange, diff, load_snapshot, save_snapshot, snapshot  # noqa: E402
from upscaler import upscale_batch  # noqa: E402


def load_config(config_path: Path | None = None) -> dict:
    """config.yaml 로드."""
    path = config_path or CONFIG_PATH
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def get_snapshot_dir(config: dict) -> Path:
    """스냅샷 저장 디렉토리."""
    custom = config["paths"].get("snapshot_dir", "")
    if custom:
        return Path(custom)
    return AGENT_DIR / ".snapshots"


def detect_changes(config: dict) -> tuple[FileChange, FileChange]:
    """XML과 Texture 변경 사항 감지."""
    snap_dir = get_snapshot_dir(config)

    # XML 스냅샷
    xml_dir = config["paths"]["source_xml"]
    xml_snap_path = snap_dir / "xml_snapshot.json"
    xml_old = load_snapshot(xml_snap_path)
    xml_new = snapshot(xml_dir, {".xml"})
    xml_changes = diff(xml_old, xml_new)

    # Texture 스냅샷
    tex_dir = config["paths"]["source_texture"]
    tex_snap_path = snap_dir / "texture_snapshot.json"
    tex_old = load_snapshot(tex_snap_path)
    tex_new = snapshot(tex_dir, {".dds"})
    tex_changes = diff(tex_old, tex_new)

    return xml_changes, tex_changes


def save_snapshots(config: dict) -> None:
    """현재 상태를 스냅샷으로 저장."""
    snap_dir = get_snapshot_dir(config)

    xml_dir = config["paths"]["source_xml"]
    xml_new = snapshot(xml_dir, {".xml"})
    save_snapshot(xml_new, snap_dir / "xml_snapshot.json")

    tex_dir = config["paths"]["source_texture"]
    tex_new = snapshot(tex_dir, {".dds"})
    save_snapshot(tex_new, snap_dir / "texture_snapshot.json")


def run_unreal_script(config: dict, script_name: str, env_vars: dict) -> bool:
    """UnrealEditor-Cmd.exe로 Python 스크립트 헤드리스 실행."""
    editor_cmd = config["paths"]["unreal_editor_cmd"]
    project = config["paths"]["unreal_project"]
    flags = config["unreal"]["headless_flags"]
    timeout = config["unreal"]["timeout_seconds"]

    script_path = UNREAL_SCRIPTS_DIR / script_name

    cmd = f'"{editor_cmd}" "{project}" -ExecutePythonScript="{script_path}" {flags}'

    env = os.environ.copy()
    env.update(env_vars)

    print(f"  [Unreal] 실행: {script_name}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        # Unreal 로그에서 LogPython 라인 추출
        for line in result.stdout.splitlines():
            if "LogPython" in line and "Display" not in line.split("LogPython")[0]:
                print(f"    {line.split('LogPython:')[-1].strip()}" if "LogPython:" in line else f"    {line}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  [타임아웃] {timeout}초 초과")
        return False
    except Exception as e:
        print(f"  [오류] Unreal 실행 실패: {e}")
        return False


def process_xml_changes(config: dict, changes: FileChange) -> list[dict]:
    """XML 변경 → Effect Import Tool."""
    results = []
    changed_files = changes.added + changes.modified
    if not changed_files:
        return results

    xml_dir = config["paths"]["source_xml"]
    fx_dest = config["paths"].get("unreal_fx_dest", "")
    texture_dest = config["paths"].get("unreal_texture_dest", "")

    if not fx_dest:
        print("  [스킵] unreal_fx_dest 미설정")
        return results

    # 세미콜론 구분 파일 목록
    full_paths = [str(Path(xml_dir) / f) for f in changed_files]
    env_vars = {
        "VFX_SYNC_XML_FILES": ";".join(full_paths),
        "VFX_SYNC_TEXTURE_DIR": texture_dest,
        "VFX_SYNC_FX_DEST": fx_dest,
    }

    success = run_unreal_script(config, "import_effects.py", env_vars)
    for f in changed_files:
        results.append({
            "type": "xml",
            "file": f,
            "action": "import_effect",
            "status": "submitted" if success else "failed",
        })

    return results


def process_texture_changes(config: dict, changes: FileChange) -> list[dict]:
    """DDS 변경 → 4K 업스케일 → 텍스처 임포트."""
    results = []
    changed_files = changes.added + changes.modified
    if not changed_files:
        return results

    tex_dir = Path(config["paths"]["source_texture"])
    upscale_output = config["paths"].get("upscale_output", "")
    texture_dest = config["paths"].get("unreal_texture_dest", "")
    model_path = config["paths"]["model_path"]
    scale = config["upscale"]["scale"]
    fmt = config["upscale"]["format"]

    if not upscale_output:
        print("  [스킵] upscale_output 미설정")
        return results

    output_dir = Path(upscale_output)

    # 1. 업스케일
    print(f"\n[업스케일] {len(changed_files)}개 텍스처")
    upscale_results = upscale_batch(
        changed_files, tex_dir, output_dir, model_path, scale, fmt,
    )

    # 2. 언리얼 임포트
    if texture_dest:
        upscaled_files = [
            r["dst"] for r in upscale_results
            if r.get("status") != "error" and "dst" in r
        ]
        if upscaled_files:
            env_vars = {
                "VFX_SYNC_TEXTURE_FILES": ";".join(upscaled_files),
                "VFX_SYNC_DEST_PATH": texture_dest,
            }
            run_unreal_script(config, "import_textures.py", env_vars)

    for r in upscale_results:
        results.append({
            "type": "texture",
            "file": Path(r.get("src", "")).name,
            "action": "upscale_and_import",
            "status": "error" if "error" in r else "success",
            "detail": r,
        })

    return results


def save_results(results: list[dict]) -> Path:
    """동기화 결과를 JSON으로 저장."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_path = RESULTS_DIR / f"{timestamp}_sync.json"

    report = {
        "timestamp": datetime.now().isoformat(),
        "total": len(results),
        "success": sum(1 for r in results if r.get("status") in ("success", "submitted")),
        "failed": sum(1 for r in results if r.get("status") in ("failed", "error")),
        "items": results,
    }

    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def main():
    import argparse

    parser = argparse.ArgumentParser(description="VFX Sync Agent")
    parser.add_argument("--config", help="설정 파일 경로 (기본: config.yaml)")
    parser.add_argument("--dry-run", action="store_true", help="변경 감지만 하고 실행하지 않음")
    parser.add_argument("--init", action="store_true", help="초기 스냅샷 저장 (비교 없이)")
    parser.add_argument("--xml-only", action="store_true", help="XML만 처리")
    parser.add_argument("--texture-only", action="store_true", help="Texture만 처리")
    args = parser.parse_args()

    config_path = Path(args.config) if args.config else None
    config = load_config(config_path)
    print("=" * 60)
    print("[VFX Sync Agent] 시작")
    print(f"  XML 소스:     {config['paths']['source_xml']}")
    print(f"  Texture 소스: {config['paths']['source_texture']}")
    print("=" * 60)

    # 초기 스냅샷 모드
    if args.init:
        save_snapshots(config)
        print("[초기화] 스냅샷 저장 완료")
        return

    # 변경 감지
    xml_changes, tex_changes = detect_changes(config)

    process_xml = not args.texture_only
    process_tex = not args.xml_only

    if process_xml:
        if xml_changes.has_changes:
            print(f"\n[XML] 변경 감지: +{len(xml_changes.added)} ~{len(xml_changes.modified)} -{len(xml_changes.removed)}")
            for f in xml_changes.added:
                print(f"  + {f}")
            for f in xml_changes.modified:
                print(f"  ~ {f}")
        else:
            print("\n[XML] 변경 없음")

    if process_tex:
        if tex_changes.has_changes:
            print(f"\n[Texture] 변경 감지: +{len(tex_changes.added)} ~{len(tex_changes.modified)} -{len(tex_changes.removed)}")
            for f in tex_changes.added:
                print(f"  + {f}")
            for f in tex_changes.modified:
                print(f"  ~ {f}")
        else:
            print("\n[Texture] 변경 없음")

    if not xml_changes.has_changes and not tex_changes.has_changes:
        print("\n[완료] 변경 사항 없음")
        return

    if args.dry_run:
        print("\n[Dry Run] 실제 처리 건너뜀")
        save_snapshots(config)
        return

    # 처리
    all_results = []

    if process_xml and xml_changes.has_changes:
        print(f"\n{'='*60}")
        print("[Pipeline A] XML → Effect Import")
        xml_results = process_xml_changes(config, xml_changes)
        all_results.extend(xml_results)

    if process_tex and tex_changes.has_changes:
        print(f"\n{'='*60}")
        print("[Pipeline B] Texture → 4K Upscale → Import")
        tex_results = process_texture_changes(config, tex_changes)
        all_results.extend(tex_results)

    # 결과 저장
    if all_results:
        output_path = save_results(all_results)
        print(f"\n[결과] {output_path}")

    # 스냅샷 업데이트
    save_snapshots(config)

    # 요약
    success = sum(1 for r in all_results if r.get("status") in ("success", "submitted"))
    failed = sum(1 for r in all_results if r.get("status") in ("failed", "error"))
    print(f"\n{'='*60}")
    print(f"[완료] 총 {len(all_results)}건 -성공: {success}, 실패: {failed}")
    print("=" * 60)


if __name__ == "__main__":
    main()
