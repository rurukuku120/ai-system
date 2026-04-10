# /session-logger

현재 세션의 대화 내용을 마크다운으로 변환하고 GitHub에 푸시합니다.

## 사용법

```
/session-logger
```

## 동작

1. 현재 세션 JSONL 파일 탐색
2. 대화 내용을 마크다운으로 변환
3. `logs/sessions/` 에 저장
4. git commit & push

## 관련 에이전트

`agents/session-logger/` — 에이전트 정의 및 runner.py
