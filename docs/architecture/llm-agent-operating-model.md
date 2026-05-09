# Multi LLM Agent Operating Model

`ai-system`은 특정 LLM 하나의 프롬프트 저장소가 아니라, 여러 LLM 도구가 같은 에이전트 계약과 실행 구조를 공유하는 운영 시스템이다.

## 계층

```text
AGENTS.md
  ├─ CLAUDE.md
  ├─ GEMINI.md
  └─ models/
      ├─ claude/README.md
      ├─ gemini/README.md
      └─ gpt/README.md

agents/<agent-id>/
  ├─ agent.yaml
  ├─ runner.py
  └─ model-specific notes
```

## 역할

| 항목 | 역할 |
|---|---|
| `AGENTS.md` | 공통 원본 지침 |
| `CLAUDE.md` | Claude Code가 찾기 쉬운 wrapper |
| `GEMINI.md` | Gemini가 찾기 쉬운 wrapper |
| `models/*` | 모델별 차이만 기록 |
| `agent.yaml` | 에이전트 계약 |
| `runner.py` | 실제 실행 코드 |
| `monitoring/health_check.py` | 계약과 실행 파일 상태 점검 |

## 원칙

- 공통 규칙을 여러 파일에 복사하지 않는다.
- 사람이 읽는 문서와 기계가 읽는 manifest를 분리한다.
- 에이전트는 작은 업무 단위로 나누고 입력/출력/환경변수를 명시한다.
- health check와 README 생성은 스크립트로 반복 가능하게 둔다.
