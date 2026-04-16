# ai-system

> 자동 생성됨 — 2026-04-16 23:45
> `scripts/update_readme.py`가 갱신합니다. 직접 편집하지 마세요.

Nexon VFX팀의 AI 도구 및 에이전트 관리 저장소.

---

## 폴더 구조

| 폴더 | 설명 |
|------|------|
| `agents/` | 에이전트 정의 및 실행 스크립트 |
| `common/` | 전체 에이전트 공통 기반 (규칙/형식/프로토콜/스키마) |
| `config/` | 환경별 설정 (dev / staging / prod) |
| `docs/` | 대시보드 및 문서 |
| `hooks/` | Claude Code 훅 (dispatcher, registry) |
| `inbox/` | VFX 작업물 피드백 요청 이미지 투입 폴더 |
| `logs/` | 세션 로그 |
| `memory/` | 에이전트 학습 결과 누적 |
| `models/` | LLM별 개별 지침 (claude / gemini / gpt) |
| `monitoring/` | 실행 로그, 오류 추적, 성능 지표 |
| `projects/` | 프로젝트별 결과물 저장 |
| `scripts/` | 유틸리티 스크립트 |
| `security/` | 접근 권한, API 키 관리 기준 |
| `sync/` | 외부 시스템 연동 (Notion / GitHub) |
| `.claude/commands/` | 슬래시 커맨드 정의 |
| `.github/workflows/` | 자동화 워크플로우 |

---

## 에이전트

| 폴더 | 이름 | 역할 |
|------|------|------|
| `agents/asset-parser/` | Unreal Asset Parser Agent | UE5 `.uasset` 바이너리 파일을 파싱하여 구조화된 데이터를 추출하는 에이전트. 에디터 없이 독립 실 |
| `agents/dashboard-builder/` | Dashboard Builder Agent | `results/` JSON과 `agents/status.json`을 읽어 `docs/index.html`  |
| `agents/notion-writer/` | Notion Writer Agent | 구조화된 데이터(JSON)를 받아 Notion 데이터베이스에 페이지를 생성하는 범용 쓰기 에이전트. VFX  |
| `agents/session-logger/` | Claude Session Logger Agent | Claude Code 세션 종료 시 대화 내용을 마크다운으로 변환하고 GitHub에 자동으로 푸시하는 에이전 |
| `agents/vfx-evaluator/` | VFX Evaluator Agent | VFX 스크린샷을 입력받아 가독성 기준으로 평가하고, 결과를 JSON으로 저장 + Notion에 등록. |
| `agents/vfx-sync/` | VFX Sync Agent | 라이브 프로젝트의 VFX XML/Texture 파일 변경을 감지하여: - **XML** → Unreal Vi |

→ 상세: [`agents/README.md`](agents/README.md)

---

## 슬래시 커맨드

| 커맨드 | 설명 |
|--------|------|
| `/dashboard-build` | VFX 평가 결과 + 에이전트 상태를 읽어 docs/index.html 대시보드를 재생성합니다. |
| `/session-logger` | 현재 세션의 대화 내용을 마크다운으로 변환하고 GitHub에 푸시합니다. |
| `/vfx-eval` | inbox/ 폴더에 있는 VFX 스크린샷 이미지를 평가하라. |
| `/vfx-sync` | 라이브(마비노기) VFX 리소스를 감지하여 언리얼(이터니티)에 자동 동기화하라. |

---

## GitHub Actions 워크플로우

| 파일 | 이름 |
|------|------|
| `sync-skills.yml` | Sync Notion Skills |
| `vfx-eval.yml` | VFX Evaluation Agent |

