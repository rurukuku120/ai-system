# AI System

> **언어 설정:** 항상 한국어로 응답한다.

Nexon VFX팀의 AI 도구 및 평가 시스템 관리 저장소.

## 환경

- OS: Windows 11 Enterprise
- Shell: PowerShell 7.6 (bash alias가 아닌 pwsh 문법 사용)
- Python: 3.14
- Unreal Engine: 5 (마비노기 이터니티 프로젝트)
- PowerShell profile 경로: `$PROFILE` (pwsh 7 기준). PS 5.1 profile을 수정하지 말 것.

## 규칙

- UE5 Python API 사용 시 메서드를 추측하지 말 것. `dir()`, `help()`로 먼저 확인한 후 스크립트 작성.
- MCP 도구(Notion, Slack)가 실패하면 같은 호출을 반복하지 말고, 원인을 설명하고 수동 대안 제시.
- Notion 페이지, Slack 메시지 등 외부 아티팩트는 명시적 요청 없이 생성하지 말 것. 읽기/검색만 허용.

## 언리얼 연동 (MCP)

- `execute_python` — UE5 에디터에서 Python 코드 실행 (`unreal` 모듈 사용 가능)
- `healthcheck` — UE5 HTTP 서버 연결 상태 확인
- 사전 조건: UE5 에디터에서 HTTP 서버(`ue_http_server.py`)가 실행 중이어야 함
- UE5 Python API 사용 시 `dir()`, `help()`로 먼저 확인 후 스크립트 작성 (기존 규칙)

## 프로젝트 구조

```
agents/                              # 에이전트 정의 (핵심)
├── vfx-feedback/                    # VFX 작업물 피드백 에이전트
├── vfx-sync/                        # VFX 리소스 동기화 에이전트
├── dashboard-builder/               # 대시보드 생성 에이전트
├── notion-writer/                   # Notion 쓰기 에이전트
├── session-logger/                  # 세션 로그 에이전트
├── asset-parser/                    # UE5 에셋 파서 에이전트
└── agent-manager/                   # 에이전트 레지스트리 관리

inbox/                               # VFX 작업물 피드백 요청 이미지 투입 폴더
monitoring/
└── health_check.py                  # 에이전트 상태 점검

sync/
└── notion/
    └── notion_to_skill.py           # Notion → 슬래시 커맨드 동기화

scripts/
└── ue/                              # UE5 연동 스크립트
    ├── ue_mcp_server.py             # Claude Code ↔ UE5 MCP 서버
    ├── ue_http_server.py            # UE5 에디터 내 HTTP 서버
    └── ue_send.py                   # UE5 Remote Execution 유틸
```

## 커스텀 명령어

- `/vfx-eval` — VFX 작업물 피드백 파이프라인 실행

## 새 에이전트 추가 방법

1. `agents/[에이전트명]/` 폴더 생성
2. `CLAUDE.md` — 역할, 입출력, 실행 방법 정의
3. `runner.py` — 실행 로직 구현
4. `.claude/commands/[에이전트명].md` — 슬래시 커맨드 등록
