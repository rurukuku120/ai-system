# VFX Feedback Agent

Nexon 마비노기 이터니티 VFX 작업물 피드백 에이전트.

## 역할

VFX 작업물 스크린샷을 입력받아 가독성 기준으로 평가하고, 결과를 JSON으로 저장 + Notion에 등록.

## 파일 구성

| 파일 | 설명 |
|------|------|
| `runner.py` | 실행 진입점 (GitHub Actions에서 호출) |
| `prompt.md` | 평가 시스템 프롬프트 |
| `rules.md` | 채점 루브릭 |
| `schema.json` | 출력 JSON 스키마 |
| `submit.sh` | 로컬 수동 실행 스크립트 |
| `workflow.md` | 자동화 워크플로우 설명 |

## 입출력

- **입력**: `inbox/` 폴더의 이미지 파일 (파일명 형식: `작업명_작업자_스킬유형.png`)
- **출력**: `projects/nexon/mabinogi-eternity/evaluations/results/YYYY-MM-DD_작업명.json`

## 실행 방법

```bash
# GitHub Actions 자동 실행: inbox/에 이미지 push 시 트리거
# 로컬 수동 실행:
ANTHROPIC_API_KEY=... NOTION_TOKEN=... python agents/vfx-feedback/runner.py
```

## 환경 변수

| 변수 | 필수 | 설명 |
|------|------|------|
| `ANTHROPIC_API_KEY` | 필수 | Anthropic API 키 |
| `NOTION_TOKEN` | 필수 | Notion PAT |
| `NOTION_DB_ID` | 선택 | Notion 데이터베이스 ID |
