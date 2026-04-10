# Agent Registry

> 마지막 갱신: 2026-04-10 23:30  
> `scripts/update_registry.py` 로 자동 생성됨.

---

## 에이전트 목록

| 에이전트 | 역할 | 슬래시 커맨드 | 트리거 |
|---|---|---|---|
| [Agent Manager](./agent-manager/CLAUDE.md) | `agents/` 폴더를 스캔하여 각 에이전트의 `CLAUDE.md`를 읽고, `agents/README.md`를 자동으로 갱신하는 메타 에이전트. | `/update-agents` | 수동 |
| [Unreal Asset Parser Agent](./asset-parser/CLAUDE.md) | UE5 `.uasset` 바이너리 파일을 파싱하여 구조화된 데이터를 추출하는 에이전트. | `-` | 수동 |
| [Claude Session Logger Agent](./session-logger/CLAUDE.md) | Claude Code 세션 종료 시 대화 내용을 마크다운으로 변환하고 GitHub에 자동으로 푸시하는 에이전트. | `-` | Stop 훅 (자동) |
| [VFX Evaluator Agent](./vfx-evaluator/CLAUDE.md) | VFX 스크린샷을 입력받아 가독성 기준으로 평가하고, 결과를 JSON으로 저장 + Notion에 등록. | `-` | 수동 |

---

## 에이전트 상세

### Agent Manager

- **폴더:** `agents/agent-manager/`
- **역할:** `agents/` 폴더를 스캔하여 각 에이전트의 `CLAUDE.md`를 읽고, `agents/README.md`를 자동으로 갱신하는 메타 에이전트.
- **커맨드:** `/update-agents`
- **트리거:** 수동
- **상세:** [agent-manager/CLAUDE.md](./agent-manager/CLAUDE.md)

### Unreal Asset Parser Agent

- **폴더:** `agents/asset-parser/`
- **역할:** UE5 `.uasset` 바이너리 파일을 파싱하여 구조화된 데이터를 추출하는 에이전트.
- **커맨드:** `-`
- **트리거:** 수동
- **상세:** [asset-parser/CLAUDE.md](./asset-parser/CLAUDE.md)

### Claude Session Logger Agent

- **폴더:** `agents/session-logger/`
- **역할:** Claude Code 세션 종료 시 대화 내용을 마크다운으로 변환하고 GitHub에 자동으로 푸시하는 에이전트.
- **커맨드:** `-`
- **트리거:** Stop 훅 (자동)
- **상세:** [session-logger/CLAUDE.md](./session-logger/CLAUDE.md)

### VFX Evaluator Agent

- **폴더:** `agents/vfx-evaluator/`
- **역할:** VFX 스크린샷을 입력받아 가독성 기준으로 평가하고, 결과를 JSON으로 저장 + Notion에 등록.
- **커맨드:** `-`
- **트리거:** 수동
- **상세:** [vfx-evaluator/CLAUDE.md](./vfx-evaluator/CLAUDE.md)

---

## 새 에이전트 추가 방법

1. `agents/[에이전트명]/` 폴더 생성
2. `CLAUDE.md` 작성 — `## 역할` 섹션 필수
3. `runner.py` 구현
4. `.claude/commands/[에이전트명].md` 슬래시 커맨드 등록
5. `python scripts/update_registry.py` 실행 (또는 자동 갱신)
