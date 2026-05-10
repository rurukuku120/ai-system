# ai-system

> 자동 생성됨 - 2026-05-10 20:46
> `scripts/update_readme.py`가 갱신합니다.

Claude, Codex/GPT, Gemini가 같은 에이전트 구조를 읽고 실행할 수 있도록 설계한 운영 저장소다.

## 지침 체계

| 파일 | 역할 | 상태 |
|---|---|---|
| `AGENTS.md` | 공통 원본 지침 | yes |
| `CLAUDE.md` | Claude Code용 진입점 | yes |
| `GEMINI.md` | Gemini용 진입점 | yes |
| `models/` | 모델별 부록 | yes |

설계 기준: [`docs/architecture/llm-agent-operating-model.md`](docs/architecture/llm-agent-operating-model.md)

## 폴더 구조

| 폴더 | 설명 |
|---|---|
| `.claude/` | Claude Code 설정과 슬래시 커맨드 |
| `.github/` | GitHub Actions 워크플로우 |
| `agents/` | 업무 단위 에이전트와 템플릿 |
| `common/` | 공통 규칙, 프로토콜, 스키마, 테스트 케이스 |
| `config/` | 환경별 설정 |
| `docs/` | 운영 문서와 아키텍처 |
| `hooks/` | 자동화 hook, scheduler, trigger 중앙 관제 |
| `memory/` | 장기 메모리와 운영 노트 |
| `models/` | 모델별 부록 |
| `monitoring/` | 상태 점검 |
| `projects/` | 프로젝트별 산출물 |
| `scripts/` | 관리 스크립트 |
| `security/` | 보안 기준 |
| `skills/` | AI와 CLI가 재사용하는 skill |
| `sync/` | 외부 시스템 동기화 |
| `wiki/` | AI가 읽고 사람이 관리하는 지식 베이스 |

## 에이전트

| ID | 이름 | 진입점 | 설명 |
|---|---|---|---|
| - | - | - | 아직 등록된 에이전트가 없습니다. |

## 기본 명령

```powershell
python monitoring/health_check.py
python scripts/update_readme.py
```
