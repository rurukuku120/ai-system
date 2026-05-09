# AI System Agent Instructions

이 저장소는 Claude, Codex/GPT, Gemini 등 여러 LLM 도구가 같은 에이전트 구조를 이해하고 실행하기 위한 공통 운영 시스템이다.

## 언어

- 항상 한국어로 응답한다.
- 코드, 파일명, 명령어, API 이름은 원문을 유지한다.

## 운영 원칙

- `AGENTS.md`가 공통 원본 지침이다.
- `CLAUDE.md`, `GEMINI.md`는 각 도구가 발견하기 쉬운 얇은 진입점이다.
- 모델별 차이는 `models/<model>/README.md`에만 기록한다.
- 실제 업무 단위는 `agents/<agent-id>/`에 둔다.
- 재사용 가능한 능력과 절차는 `skills/<skill-id>/`에 둔다.
- AI가 참조할 도메인 지식과 운영 지식은 `wiki/`에 둔다.
- 에이전트의 기계 판독 가능한 계약은 `agent.yaml`에 둔다.
- 실행 가능한 동작은 `runner.py`에 둔다.
- 외부 아티팩트 생성은 사용자 명시 요청 또는 에이전트 계약이 있을 때만 수행한다.
- 자동 생성 파일은 생성 스크립트로 갱신한다.
- 자동화 트리거, hook, scheduler의 원본과 목록은 `hooks/`에서 확인 가능해야 한다.

## 기본 구조

```text
AGENTS.md              공통 원본 지침
CLAUDE.md              Claude Code용 진입점
GEMINI.md              Gemini용 진입점
models/                모델별 부록
agents/                업무 단위 에이전트
skills/                재사용 가능한 skill과 CLI 동기화 산출물
wiki/                  AI가 읽고 사람이 관리하는 지식 베이스
common/                공통 규칙, 프로토콜, 스키마, 테스트 케이스
monitoring/            상태 점검
hooks/                 자동화 hook, scheduler, trigger 중앙 관제
scripts/               관리 스크립트
docs/                  운영 문서
sync/                  외부 시스템 연동
```

## 에이전트 계약

각 에이전트는 다음 구성을 기본으로 한다.

```text
agents/<agent-id>/
├── agent.yaml
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
├── runner.py
└── schema.json
```

최소 필수 파일은 `agent.yaml`과 실행 가능한 `entrypoint`다. 모델별 지침 파일은 필요한 경우에만 추가한다.

## 새 에이전트 추가 순서

1. `agents/_template/`를 복사해 `agents/<agent-id>/`를 만든다.
2. `agent.yaml`의 `id`, `name`, `entrypoint`, `triggers`, `inputs`, `outputs`, `env`, `health`를 채운다.
3. `runner.py`에 실제 실행 로직을 작성한다.
4. 필요하면 `.claude/commands/<agent-id>.md`를 추가한다.
5. `python monitoring/health_check.py`로 상태를 확인한다.
6. `python scripts/update_readme.py`로 루트 README를 갱신한다.

## 검증

- 에이전트 manifest 형식: `common/schemas/agent.schema.json`
- skill manifest 형식: `common/schemas/skill.schema.json`
- 예시 manifest: `common/schemas/agent.example.yaml`
- 운영 모델 문서: `docs/architecture/llm-agent-operating-model.md`
