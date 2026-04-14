# Claude Session Logger Agent

## 역할
Claude Code 세션 종료 시 대화 내용을 마크다운으로 변환하고 GitHub에 자동으로 푸시하는 에이전트.

## 적용 범위
- 전역 (모든 프로젝트)
- Stop 훅으로 자동 트리거

---

## 동작 흐름

```
세션 종료
  └─ Stop 훅 실행
       └─ runner.py
            ├─ 1. stdin에서 session_id 추출
            ├─ 2. ~/.claude/projects/*/{session_id}.jsonl 탐색
            ├─ 3. JSONL → 마크다운 변환
            ├─ 4. logs/sessions/{date}_{session_id_short}.md 저장
            └─ 5. git commit & push
```

## 출력 파일 위치
```
ai-system/
└── logs/
    └── sessions/
        └── YYYY-MM-DD_XXXXXXXX.md
```

## 마크다운 형식
```markdown
# Session Log — YYYY-MM-DD HH:MM

**Session ID:** xxxxxxxx  
**Project:** /path/to/project  
**Model:** claude-sonnet-4-6  

---

## 대화

### User
...

### Assistant
...
```

## 관련 파일
- `hooks/stop/session-logger.py` — 실제 구현 (dispatcher 경유)
- `hooks/dispatcher.py` — 이벤트 라우터
- `hooks/registry.json` — 훅 활성화/순서 관리
- `scripts/setup.py` — 새 컴퓨터 초기 설정
- `.claude/commands/session-logger.md` — 슬래시 커맨드 (수동 실행)

> runner.py는 레거시. 실제 로직은 hooks/stop/session-logger.py에 있음.
