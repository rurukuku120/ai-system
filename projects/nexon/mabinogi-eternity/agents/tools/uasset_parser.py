#!/usr/bin/env python3
"""
UE5 .uasset Binary Parser
Unreal Engine 5 에셋 파일 바이너리 파서.

지원 추출 데이터:
- 파일 헤더 요약 (버전, 이름/임포트/익스포트 카운트)
- 의존성 그래프 (import table)
- DataTable 행 데이터
- 메시/텍스처 메타데이터
- Blueprint 구조 (변수, 함수 목록)

사용법:
    python uasset_parser.py summary   <file.uasset>
    python uasset_parser.py deps      <file.uasset>
    python uasset_parser.py datatable <file.uasset>
    python uasset_parser.py mesh      <file.uasset>
    python uasset_parser.py blueprint <file.uasset>
    python uasset_parser.py batch     <directory> [--types datatable,mesh]
"""

import struct
import json
import sys
import os
from pathlib import Path
from typing import Optional

# UE 패키지 매직 넘버
UE_PACKAGE_MAGIC = 0x9E2A83C1

# UE5 버전 상수
VER_UE5_LARGE_WORLD_COORDINATES = 1000
VER_UE5_ADD_SOFTOBJECTPATH_LIST = 518


# ---------------------------------------------------------------------------
# Binary Reader
# ---------------------------------------------------------------------------

class BinaryReader:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def remaining(self) -> int:
        return len(self.data) - self.pos

    def seek(self, pos: int):
        self.pos = pos

    def tell(self) -> int:
        return self.pos

    def read_bytes(self, n: int) -> bytes:
        if self.pos + n > len(self.data):
            raise ValueError(f"Unexpected EOF at offset {self.pos} (need {n} bytes)")
        val = self.data[self.pos:self.pos + n]
        self.pos += n
        return val

    def read_int8(self) -> int:
        return struct.unpack_from('<b', self.read_bytes(1))[0]

    def read_uint8(self) -> int:
        return struct.unpack_from('<B', self.read_bytes(1))[0]

    def read_int32(self) -> int:
        return struct.unpack_from('<i', self.read_bytes(4))[0]

    def read_uint32(self) -> int:
        return struct.unpack_from('<I', self.read_bytes(4))[0]

    def read_int64(self) -> int:
        return struct.unpack_from('<q', self.read_bytes(8))[0]

    def read_uint64(self) -> int:
        return struct.unpack_from('<Q', self.read_bytes(8))[0]

    def read_float(self) -> float:
        return struct.unpack_from('<f', self.read_bytes(4))[0]

    def read_double(self) -> float:
        return struct.unpack_from('<d', self.read_bytes(8))[0]

    def read_bool32(self) -> bool:
        return self.read_uint32() != 0

    def read_fstring(self) -> str:
        length = self.read_int32()
        if length == 0:
            return ""
        if length < 0:
            # UTF-16 LE
            byte_len = (-length) * 2
            raw = self.read_bytes(byte_len)
            return raw.decode('utf-16-le', errors='replace').rstrip('\x00')
        else:
            raw = self.read_bytes(length)
            return raw.decode('utf-8', errors='replace').rstrip('\x00')

    def read_guid(self) -> str:
        a = self.read_uint32()
        b = self.read_uint32()
        c = self.read_uint32()
        d = self.read_uint32()
        return f"{a:08X}-{b:08X}-{c:08X}-{d:08X}"


# ---------------------------------------------------------------------------
# UAsset Parser Core
# ---------------------------------------------------------------------------

class UAssetParser:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'rb') as f:
            self.data = f.read()

        self.r = BinaryReader(self.data)
        self.summary: dict = {}
        self.names: list[str] = []
        self.imports: list[dict] = []
        self.exports: list[dict] = []
        self._parsed_header = False
        self._parsed_names = False
        self._parsed_imports = False
        self._parsed_exports = False

    # ------------------------------------------------------------------
    # Header Parsing
    # ------------------------------------------------------------------

    def parse_header(self) -> dict:
        if self._parsed_header:
            return self.summary

        r = self.r
        r.seek(0)

        magic = r.read_uint32()
        if magic != UE_PACKAGE_MAGIC:
            raise ValueError(
                f"Not a valid .uasset file. Magic: 0x{magic:08X} "
                f"(expected 0x{UE_PACKAGE_MAGIC:08X})"
            )

        legacy_file_version = r.read_int32()   # 음수값 (-6, -7, -8 등)
        r.read_int32()                          # LegacyUE3Version (항상 864)

        file_version_ue4 = r.read_int32()
        file_version_ue5 = 0

        # UE5: legacy_file_version <= -8 이면 UE5 버전 필드 존재
        if legacy_file_version <= -8:
            file_version_ue5 = r.read_int32()

        r.read_int32()  # FileVersionLicenseeUE

        # CustomVersions 배열
        custom_ver_count = r.read_int32()
        custom_versions = []
        for _ in range(custom_ver_count):
            guid = r.read_guid()
            ver = r.read_int32()
            custom_versions.append({"guid": guid, "version": ver})

        total_header_size = r.read_int32()
        package_name = r.read_fstring()
        package_flags = r.read_uint32()

        name_count = r.read_int32()
        name_offset = r.read_int32()

        # UE5: SoftObjectPaths
        soft_object_paths_count = 0
        soft_object_paths_offset = 0
        if file_version_ue5 >= VER_UE5_ADD_SOFTOBJECTPATH_LIST:
            soft_object_paths_count = r.read_int32()
            soft_object_paths_offset = r.read_int32()

        # GatherableTextData (legacy_file_version >= -7)
        gatherable_text_count = 0
        gatherable_text_offset = 0
        if legacy_file_version >= -7:
            gatherable_text_count = r.read_int32()
            gatherable_text_offset = r.read_int32()

        export_count = r.read_int32()
        export_offset = r.read_int32()
        import_count = r.read_int32()
        import_offset = r.read_int32()
        depends_offset = r.read_int32()

        self.summary = {
            "file": str(self.file_path),
            "file_size_bytes": len(self.data),
            "magic": f"0x{magic:08X}",
            "legacy_file_version": legacy_file_version,
            "file_version_ue4": file_version_ue4,
            "file_version_ue5": file_version_ue5,
            "package_name": package_name,
            "package_flags": f"0x{package_flags:08X}",
            "total_header_size": total_header_size,
            "name_count": name_count,
            "name_offset": name_offset,
            "export_count": export_count,
            "export_offset": export_offset,
            "import_count": import_count,
            "import_offset": import_offset,
            "custom_version_count": custom_ver_count,
        }
        self._parsed_header = True
        return self.summary

    # ------------------------------------------------------------------
    # Name Table
    # ------------------------------------------------------------------

    def _parse_names(self):
        if self._parsed_names:
            return
        self.parse_header()

        r = self.r
        r.seek(self.summary["name_offset"])

        self.names = []
        for _ in range(self.summary["name_count"]):
            name = r.read_fstring()
            r.read_uint32()  # NonCasePreservingHash
            r.read_uint32()  # CasePreservingHash
            self.names.append(name)

        self._parsed_names = True

    def _read_fname(self) -> str:
        idx = self.r.read_int32()
        number = self.r.read_int32()
        if 0 <= idx < len(self.names):
            base = self.names[idx]
            return f"{base}_{number - 1}" if number > 0 else base
        return f"<name:{idx}>"

    def _resolve_index(self, index: int) -> str:
        """임포트/익스포트 인덱스를 이름으로 변환"""
        if index < 0:
            imp_idx = -index - 1
            if 0 <= imp_idx < len(self.imports):
                return self.imports[imp_idx].get("object_name", f"<import:{imp_idx}>")
        elif index > 0:
            exp_idx = index - 1
            if 0 <= exp_idx < len(self.exports):
                return self.exports[exp_idx].get("object_name", f"<export:{exp_idx}>")
        return "None"

    # ------------------------------------------------------------------
    # Import Table
    # ------------------------------------------------------------------

    def _parse_imports(self):
        if self._parsed_imports:
            return
        self._parse_names()

        r = self.r
        r.seek(self.summary["import_offset"])

        self.imports = []
        for _ in range(self.summary["import_count"]):
            class_package = self._read_fname()
            class_name = self._read_fname()
            outer_index = r.read_int32()
            object_name = self._read_fname()
            # UE5: optional package name field
            package_name = self._read_fname()

            self.imports.append({
                "class_package": class_package,
                "class_name": class_name,
                "outer_index": outer_index,
                "object_name": object_name,
                "package_name": package_name,
            })

        self._parsed_imports = True

    # ------------------------------------------------------------------
    # Export Table
    # ------------------------------------------------------------------

    def _parse_exports(self):
        if self._parsed_exports:
            return
        self._parse_imports()

        r = self.r
        r.seek(self.summary["export_offset"])

        self.exports = []
        for _ in range(self.summary["export_count"]):
            class_index = r.read_int32()
            super_index = r.read_int32()
            template_index = r.read_int32()
            outer_index = r.read_int32()
            object_name = self._read_fname()
            object_flags = r.read_uint32()
            serial_size = r.read_int64()
            serial_offset = r.read_int64()
            is_forced_export = r.read_bool32()
            is_not_for_client = r.read_bool32()
            is_not_for_server = r.read_bool32()
            package_guid = r.read_guid()
            package_flags = r.read_uint32()
            is_not_always_loaded_for_editor_game = r.read_bool32()
            is_asset = r.read_bool32()
            generate_public_hash = r.read_bool32()

            # FirstExportDependency (int32 x 4)
            r.read_int32()
            r.read_int32()
            r.read_int32()
            r.read_int32()

            self.exports.append({
                "class_index": class_index,
                "object_name": object_name,
                "object_flags": f"0x{object_flags:08X}",
                "serial_size": serial_size,
                "serial_offset": serial_offset,
                "is_asset": is_asset,
            })

        self._parsed_exports = True

    # ------------------------------------------------------------------
    # Public API: parse_asset_summary
    # ------------------------------------------------------------------

    def parse_asset_summary(self) -> dict:
        """파일 헤더 요약 반환"""
        summary = self.parse_header()
        self._parse_exports()

        # 루트 에셋 클래스 추론
        root_class = "Unknown"
        if self.exports and self.imports:
            first_export = self.exports[0]
            cls_idx = first_export["class_index"]
            if cls_idx < 0:
                imp = self.imports[-cls_idx - 1]
                root_class = imp.get("class_name", "Unknown")

        return {
            **summary,
            "root_class": root_class,
            "exports": [
                {"name": e["object_name"], "class_index": e["class_index"],
                 "size": e["serial_size"]}
                for e in self.exports
            ],
        }

    # ------------------------------------------------------------------
    # Public API: parse_dependencies
    # ------------------------------------------------------------------

    def parse_dependencies(self) -> dict:
        """import 테이블 기반 의존성 추출"""
        self._parse_imports()

        categorized = {
            "textures": [],
            "meshes": [],
            "materials": [],
            "blueprints": [],
            "sounds": [],
            "animations": [],
            "particles": [],
            "other": [],
        }

        texture_classes = {"Texture2D", "TextureCube", "Texture2DArray",
                           "TextureRenderTarget2D", "VolumeTexture"}
        mesh_classes = {"StaticMesh", "SkeletalMesh"}
        material_classes = {"Material", "MaterialInstance",
                            "MaterialInstanceConstant", "MaterialInstanceDynamic"}
        blueprint_classes = {"Blueprint", "BlueprintGeneratedClass",
                             "AnimBlueprint", "AnimBlueprintGeneratedClass"}
        sound_classes = {"SoundWave", "SoundCue", "SoundBase"}
        anim_classes = {"AnimSequence", "AnimMontage", "BlendSpace",
                        "BlendSpace1D", "AnimComposite"}
        particle_classes = {"ParticleSystem", "NiagaraSystem", "NiagaraEmitter"}

        for imp in self.imports:
            cls = imp["class_name"]
            entry = {
                "name": imp["object_name"],
                "package": imp["package_name"] or imp["class_package"],
                "class": cls,
            }
            if cls in texture_classes:
                categorized["textures"].append(entry)
            elif cls in mesh_classes:
                categorized["meshes"].append(entry)
            elif cls in material_classes:
                categorized["materials"].append(entry)
            elif cls in blueprint_classes:
                categorized["blueprints"].append(entry)
            elif cls in sound_classes:
                categorized["sounds"].append(entry)
            elif cls in anim_classes:
                categorized["animations"].append(entry)
            elif cls in particle_classes:
                categorized["particles"].append(entry)
            else:
                categorized["other"].append(entry)

        return {
            "file": str(self.file_path),
            "total_imports": len(self.imports),
            "summary": {k: len(v) for k, v in categorized.items()},
            "dependencies": categorized,
        }

    # ------------------------------------------------------------------
    # Public API: parse_datatable
    # ------------------------------------------------------------------

    def parse_datatable(self) -> dict:
        """
        DataTable 에셋의 행 데이터 파싱.
        DataTable은 export 직렬화 데이터에서 FDataTableRowMap을 읽어야 하나,
        바이너리 포맷이 row struct 타입에 따라 달라지므로
        현재는 이름 테이블 + export 메타만 반환하고 raw offset을 제공.
        완전한 행 파싱은 row struct 스키마가 필요.
        """
        self._parse_exports()

        datatable_exports = [
            e for e in self.exports
            if "DataTable" in e["object_name"] or e["class_index"] < 0
        ]

        rows_hint = []
        # 이름 테이블에서 RowName 후보 탐색 (휴리스틱)
        for name in self.names:
            if name and not name.startswith("/Script") and "." not in name:
                if len(name) > 1 and not name[0].isdigit():
                    rows_hint.append(name)

        return {
            "file": str(self.file_path),
            "note": (
                "DataTable 행 데이터의 완전한 파싱은 RowStruct 스키마가 필요합니다. "
                "row_name_hints는 이름 테이블 휴리스틱 결과입니다."
            ),
            "datatable_exports": datatable_exports,
            "row_name_hints": rows_hint[:100],  # 최대 100개
            "raw_export_offsets": [
                {"name": e["object_name"], "offset": e["serial_offset"],
                 "size": e["serial_size"]}
                for e in self.exports
            ],
        }

    # ------------------------------------------------------------------
    # Public API: parse_mesh_metadata
    # ------------------------------------------------------------------

    def parse_mesh_metadata(self) -> dict:
        """메시/텍스처 메타데이터 추출 (이름 + 의존성 기반)"""
        self._parse_exports()
        deps = self.parse_dependencies()

        mesh_exports = []
        for exp in self.exports:
            name = exp["object_name"]
            if any(kw in name for kw in ("LOD", "Mesh", "Texture", "Material")):
                mesh_exports.append({
                    "name": name,
                    "serial_size": exp["serial_size"],
                    "serial_offset": exp["serial_offset"],
                })

        return {
            "file": str(self.file_path),
            "referenced_textures": deps["dependencies"]["textures"],
            "referenced_meshes": deps["dependencies"]["meshes"],
            "referenced_materials": deps["dependencies"]["materials"],
            "mesh_related_exports": mesh_exports,
            "total_export_size_bytes": sum(
                e["serial_size"] for e in self.exports
            ),
        }

    # ------------------------------------------------------------------
    # Public API: parse_blueprint
    # ------------------------------------------------------------------

    def parse_blueprint(self) -> dict:
        """Blueprint 구조 추출 (이름 테이블 기반 휴리스틱)"""
        self._parse_exports()
        self._parse_imports()

        # Blueprint 관련 임포트
        bp_imports = [
            imp for imp in self.imports
            if "Blueprint" in imp["class_name"] or
               "Blueprint" in imp["object_name"]
        ]

        # 이름 테이블에서 변수/함수 후보 추출
        variable_hints = []
        function_hints = []
        for name in self.names:
            if not name or name.startswith("/"):
                continue
            # 함수: 대문자로 시작하는 동사형
            if name.startswith(("On", "Get", "Set", "Is", "Has",
                                 "Can", "Do", "Try", "Update", "Init",
                                 "Spawn", "Destroy", "Apply")):
                function_hints.append(name)
            # 변수: 소문자 시작 또는 b접두사 (bool 패턴)
            elif name.startswith("b") and len(name) > 1 and name[1].isupper():
                variable_hints.append({"name": name, "type_hint": "bool"})
            elif name and name[0].islower() and "_" not in name:
                variable_hints.append({"name": name, "type_hint": "unknown"})

        return {
            "file": str(self.file_path),
            "note": (
                "Blueprint 노드 그래프의 완전한 파싱은 UE5 직렬화 포맷 구현이 필요합니다. "
                "현재는 이름 테이블 기반 휴리스틱을 제공합니다."
            ),
            "blueprint_imports": bp_imports,
            "exports": [
                {"name": e["object_name"], "size": e["serial_size"]}
                for e in self.exports
            ],
            "function_hints": function_hints[:50],
            "variable_hints": variable_hints[:50],
        }


# ---------------------------------------------------------------------------
# Batch Parser
# ---------------------------------------------------------------------------

def batch_parse(directory: str, asset_types: Optional[list] = None) -> dict:
    """디렉토리 내 .uasset 파일 일괄 파싱"""
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    uasset_files = list(dir_path.rglob("*.uasset"))
    results = []
    errors = []

    for f in uasset_files:
        try:
            parser = UAssetParser(str(f))
            summary = parser.parse_asset_summary()
            entry = {
                "file": str(f),
                "root_class": summary.get("root_class"),
                "import_count": summary.get("import_count"),
                "export_count": summary.get("export_count"),
                "file_size_bytes": summary.get("file_size_bytes"),
            }
            if asset_types:
                if summary.get("root_class") in asset_types:
                    results.append(entry)
            else:
                results.append(entry)
        except Exception as e:
            errors.append({"file": str(f), "error": str(e)})

    return {
        "directory": directory,
        "total_found": len(uasset_files),
        "total_parsed": len(results),
        "total_errors": len(errors),
        "results": results,
        "errors": errors,
    }


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    target = sys.argv[2]

    try:
        if command == "summary":
            parser = UAssetParser(target)
            result = parser.parse_asset_summary()

        elif command == "deps":
            parser = UAssetParser(target)
            result = parser.parse_dependencies()

        elif command == "datatable":
            parser = UAssetParser(target)
            result = parser.parse_datatable()

        elif command == "mesh":
            parser = UAssetParser(target)
            result = parser.parse_mesh_metadata()

        elif command == "blueprint":
            parser = UAssetParser(target)
            result = parser.parse_blueprint()

        elif command == "batch":
            types = None
            if "--types" in sys.argv:
                idx = sys.argv.index("--types")
                types = sys.argv[idx + 1].split(",")
            result = batch_parse(target, types)

        else:
            print(f"Unknown command: {command}", file=sys.stderr)
            sys.exit(1)

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except FileNotFoundError as e:
        print(json.dumps({"error": "file_not_found", "message": str(e)}))
        sys.exit(1)
    except ValueError as e:
        print(json.dumps({"error": "parse_error", "message": str(e)}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": "unexpected", "message": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
