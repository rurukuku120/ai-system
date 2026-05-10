# CLAUDE.md

이 저장소의 공통 지침은 `AGENTS.md`를 따른다.

Claude Code에서는 추가로 다음 위치를 참고한다.

- Claude 부록: `models/claude/README.md`
- 슬래시 커맨드: `.claude/commands/*.md`
- 에이전트별 Claude 지침: `agents/*/CLAUDE.md`

## Claude Code 규칙

- 항상 한국어로 응답한다.
- PowerShell 환경에서는 PowerShell 문법을 사용한다.
- 기존 사용자 변경을 임의로 되돌리지 않는다.
- 외부 아티팩트 생성은 명시 요청이 있을 때만 수행한다.

## 주요 명령어

```bash
# 에이전트 헬스체크
python monitoring/health_check.py

# 루트 README 갱신
python scripts/update_readme.py
```

## 배포된 프로젝트

- `projects/personal-fitness-app/` — Fly.io 배포 피트니스 앱 (https://personal-fitness-app.fly.dev)
