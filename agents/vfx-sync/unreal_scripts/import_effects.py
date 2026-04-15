"""
Unreal Python: Effect Import Tool (VirtuosTools) 호출
UnrealEditor-Cmd.exe -ExecutePythonScript 로 실행됨.

환경변수로 파라미터 전달:
  VFX_SYNC_XML_FILES       — 임포트할 XML 파일 경로 (세미콜론 구분)
  VFX_SYNC_XML_SOURCE_DIR  — XML 소스 디렉토리 (단일 파일 대신 디렉토리 모드)
  VFX_SYNC_TEXTURE_DIR     — 텍스처 디렉토리 (언리얼 내 경로)
  VFX_SYNC_FX_DEST         — Niagara 출력 디렉토리 (언리얼 내 경로)
"""

import os

import unreal


def import_effects_directory(source_dir: str, texture_dir: str, dest_dir: str) -> bool:
    """VirtuosEffectToolUI를 설정하고 ImportFile 호출."""
    try:
        tool_ui = unreal.VirtuosEffectToolUI()
        tool_ui.set_editor_property("source_directory", unreal.DirectoryPath(source_dir))
        tool_ui.set_editor_property("texture_directory", unreal.DirectoryPath(texture_dir))
        tool_ui.set_editor_property("destination_directory", unreal.DirectoryPath(dest_dir))
        tool_ui.set_editor_property("b_import_single_file", False)
        tool_ui.set_editor_property("b_recursive_source_directory", True)
        tool_ui.set_editor_property("b_enable_asset_auto_save", True)

        # static 함수 호출
        unreal.VirtuosEffectToolWindow.import_file(tool_ui)
        print(f"[성공] Effect Import 완료: {source_dir} → {dest_dir}")
        return True

    except AttributeError as e:
        print(f"[경고] VirtuosEffectToolUI 직접 호출 실패: {e}")
        print("[시도] Factory 방식으로 폴백...")
        return import_effects_factory(source_dir, texture_dir, dest_dir)

    except Exception as e:
        print(f"[오류] Effect Import 실패: {e}")
        return False


def import_effects_single(xml_path: str, texture_dir: str, dest_dir: str) -> bool:
    """단일 XML 파일 임포트."""
    try:
        tool_ui = unreal.VirtuosEffectToolUI()
        tool_ui.set_editor_property("b_import_single_file", True)
        tool_ui.set_editor_property("source_file", unreal.FilePath(xml_path))
        tool_ui.set_editor_property("texture_directory", unreal.DirectoryPath(texture_dir))
        tool_ui.set_editor_property("destination_directory", unreal.DirectoryPath(dest_dir))
        tool_ui.set_editor_property("b_enable_asset_auto_save", True)

        unreal.VirtuosEffectToolWindow.import_file(tool_ui)
        print(f"[성공] {os.path.basename(xml_path)} → {dest_dir}")
        return True

    except AttributeError:
        return import_effects_factory_single(xml_path, texture_dir, dest_dir)

    except Exception as e:
        print(f"[오류] {os.path.basename(xml_path)}: {e}")
        return False


def import_effects_factory(source_dir: str, texture_dir: str, dest_dir: str) -> bool:
    """Factory + AssetTools 방식 폴백."""
    try:
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        factory = unreal.VirtuosMabinogiNiagaraFactory()

        for f in os.listdir(source_dir):
            if not f.lower().endswith(".xml"):
                continue
            xml_path = os.path.join(source_dir, f)
            task = unreal.AssetImportTask()
            task.filename = xml_path
            task.destination_path = dest_dir
            task.factory = factory
            task.automated = True
            task.replace_existing = True
            task.save = True
            asset_tools.import_asset_tasks([task])

            imported = task.get_objects()
            status = "성공" if imported else "실패"
            print(f"  [{status}] {f}")

        return True

    except Exception as e:
        print(f"[오류] Factory 폴백 실패: {e}")
        return False


def import_effects_factory_single(xml_path: str, texture_dir: str, dest_dir: str) -> bool:
    """단일 파일 Factory 폴백."""
    try:
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        factory = unreal.VirtuosMabinogiNiagaraFactory()

        task = unreal.AssetImportTask()
        task.filename = xml_path
        task.destination_path = dest_dir
        task.factory = factory
        task.automated = True
        task.replace_existing = True
        task.save = True
        asset_tools.import_asset_tasks([task])

        imported = task.get_objects()
        status = "성공" if imported else "실패"
        print(f"  [{status}] {os.path.basename(xml_path)}")
        return bool(imported)

    except Exception as e:
        print(f"[오류] {os.path.basename(xml_path)}: {e}")
        return False


def main():
    xml_files_str = os.environ.get("VFX_SYNC_XML_FILES", "")
    source_dir = os.environ.get("VFX_SYNC_XML_SOURCE_DIR", "")
    texture_dir = os.environ.get("VFX_SYNC_TEXTURE_DIR", "")
    dest_dir = os.environ.get("VFX_SYNC_FX_DEST", "/Game/FX/Effect")

    if not texture_dir:
        print("[경고] VFX_SYNC_TEXTURE_DIR 미설정, 기본값 사용")

    if source_dir:
        print(f"[시작] Effect Import (디렉토리): {source_dir}")
        import_effects_directory(source_dir, texture_dir, dest_dir)

    elif xml_files_str:
        file_paths = [f.strip() for f in xml_files_str.split(";") if f.strip()]
        print(f"[시작] Effect Import {len(file_paths)}개 파일")
        success = 0
        for xml_path in file_paths:
            if import_effects_single(xml_path, texture_dir, dest_dir):
                success += 1
        print(f"[완료] 성공: {success}/{len(file_paths)}")

    else:
        print("[오류] VFX_SYNC_XML_FILES 또는 VFX_SYNC_XML_SOURCE_DIR 필요")


main()
