# Agent Manager

## 역할
`agents/` 폴더를 스캔하여 각 에이전트의 `CLAUDE.md`를 읽고, `agents/README.md`를 자동으로 갱신하는 메타 에이전트.

## 적용 범위
- 이 저장소 전역
- 새 에이전트 추가 시 `/update-agents` 슬래시 커맨드로 수동 트리거

## 동작 흐름

```
/update-agents 실행
  └─ runner.py
       ├─ agents/ 폴더 스캔
       ├─ 각 에이전트의 CLAUDE.md 파싱 (이름, 역할, 트리거, 슬래시 커맨드)
       └─ agents/README.md 자동 생성
```

## 실행 방법

```bash
python agents/agent-manager/runner.py
```

또는 슬래시 커맨드:
```
/update-agents
```

## 관련 파일
- `runner.py` — 실행 스크립트
- `agents/README.md` — 자동 생성되는 에이전트 인덱스 (직접 편집 금지)
