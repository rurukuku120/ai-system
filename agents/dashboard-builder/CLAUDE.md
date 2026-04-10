# Dashboard Builder Agent

## 역할
`results/` JSON과 `agents/status.json`을 읽어 `docs/index.html` 대시보드를 생성하는 에이전트.

## 트리거
- VFX 평가 완료 후 자동 실행 (vfx-evaluator runner에서 호출)
- 수동: `python agents/dashboard-builder/runner.py`
- 슬래시 커맨드: `/dashboard-build`

## 입출력

- **입력**
  - `projects/nexon/mabinogi-eternity/evaluations/results/*.json` — VFX 평가 결과
  - `agents/status.json` — 에이전트 헬스체크 상태
- **출력**
  - `docs/index.html` — GitHub Pages 대시보드

## 관련 파일
- `runner.py` — 실행 스크립트
- `scripts/generate_dashboard.py` — 레거시 (runner.py로 대체됨)
