"""
Unreal Python: 텍스처 임포트
UnrealEditor-Cmd.exe -ExecutePythonScript 로 실행됨.

환경변수로 파라미터 전달:
  VFX_SYNC_TEXTURE_FILES  — 임포트할 파일 경로 (세미콜론 구분)
  VFX_SYNC_DEST_PATH      — 언리얼 대상 경로 (예: /Game/Material/FX/Effect)
"""

import os
import sys

import unreal


def import_textures(file_paths: list[str], destination_path: str) -> list[dict]:
    """텍스처 파일을 언리얼 프로젝트로 임포트."""
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    results = []

    tasks = []
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"[스킵] 파일 없음: {file_path}")
            results.append({"file": file_path, "status": "skipped", "reason": "not_found"})
            continue

        task = unreal.AssetImportTask()
        task.filename = file_path
        task.destination_path = destination_path
        task.destination_name = os.path.splitext(os.path.basename(file_path))[0]
        task.replace_existing = True
        task.automated = True
        task.save = True
        tasks.append(task)

    if tasks:
        asset_tools.import_asset_tasks(tasks)

    for task in tasks:
        imported = task.get_objects()
        status = "success" if imported else "failed"
        asset_path = imported[0].get_path_name() if imported else ""
        print(f"[{status.upper()}] {os.path.basename(task.filename)} → {asset_path}")
        results.append({
            "file": task.filename,
            "status": status,
            "asset_path": asset_path,
        })

    return results


def main():
    files_str = os.environ.get("VFX_SYNC_TEXTURE_FILES", "")
    dest_path = os.environ.get("VFX_SYNC_DEST_PATH", "/Game/Material/FX/Effect")

    if not files_str:
        print("[오류] VFX_SYNC_TEXTURE_FILES 환경변수가 비어있음")
        return

    file_paths = [f.strip() for f in files_str.split(";") if f.strip()]
    print(f"[시작] 텍스처 임포트 {len(file_paths)}개 → {dest_path}")

    results = import_textures(file_paths, dest_path)

    success = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "failed")
    print(f"[완료] 성공: {success}, 실패: {failed}")


main()
