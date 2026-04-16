# VFX Sync Agent

라이브(마비노기) → 언리얼(이터니티) VFX 리소스 자동 동기화 에이전트.

## 역할

라이브 프로젝트의 VFX XML/Texture 파일 변경을 감지하여:
- **XML** → Unreal VirtuosTools Effect Import Tool로 Niagara 시스템 자동 생성
- **Texture(DDS)** → Real-ESRGAN 4K 업스케일 → 언리얼 지정 폴더에 자동 임포트

## 파일 구성

| 파일 | 설명 |
|------|------|
| `runner.py` | 메인 오케스트레이터 |
| `config.yaml` | 경로 및 설정 (수정 가능) |
| `watcher.py` | 파일 변경 감지 (스냅샷 비교) |
| `upscaler.py` | Real-ESRGAN 4K 업스케일 |
| `unreal_scripts/import_textures.py` | Unreal Python: 텍스처 임포트 |
| `unreal_scripts/import_effects.py` | Unreal Python: Effect Import Tool 호출 |
| `schema.json` | Sync 결과 JSON 스키마 |

## 입출력

- **입력**: 라이브 소스 디렉토리 (config.yaml에서 지정)
  - XML: `Z:/Mabinogi/dev/release/asset/data/gfx/fx/effect/*.xml`
  - Texture: `Z:/Mabinogi/dev/release/asset/data/material/fx/effect/*.dds`
- **출력**:
  - 업스케일된 텍스처 (PNG)
  - 언리얼 Niagara 시스템 / 텍스처 에셋
  - 결과 로그: `projects/nexon/mabinogi-eternity/sync/results/YYYY-MM-DD_sync.json`

## 실행 방법

```bash
# 초기 스냅샷 생성 (최초 1회)
python agents/vfx-sync/runner.py --init

# 변경 감지 + 자동 처리
python agents/vfx-sync/runner.py

# 변경 확인만 (실행 안 함)
python agents/vfx-sync/runner.py --dry-run

# XML만 처리
python agents/vfx-sync/runner.py --xml-only

# Texture만 처리
python agents/vfx-sync/runner.py --texture-only
```

슬래시 커맨드: `/vfx-sync`

## 환경 변수

| 변수 | 필수 | 설명 |
|------|------|------|
| `NOTION_TOKEN` | 선택 | Notion 결과 등록 시 필요 |

## 의존성

- Python: `pyyaml`, `torch` (CUDA), `spandrel`, `Pillow`, `numpy`
- 외부: `UnrealEditor-Cmd.exe` (UE 5.5.4)
- 모델: `RealESRGAN_x4plus.pth` (config.yaml의 model_path)
