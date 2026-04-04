# AI System - Claude Code Agent Instructions

## 이미지가 전달되면 자동 실행

사용자가 이미지를 전달하고 별도 지시가 없으면, **VFX 가독성 평가 파이프라인을 자동으로 실행**하라.

### 자동 실행 순서

1. **평가 실행**
   - `projects/nexon/mabinogi-eternity/evaluations/vfx-eval-prompt.md` 프롬프트 기준으로 평가
   - `projects/nexon/mabinogi-eternity/evaluations/vfx-readability-rules.md` 루브릭 적용
   - `projects/nexon/mabinogi-eternity/evaluations/vfx-eval-schema.json` 형식으로 JSON 출력

2. **파일 저장**
   - 경로: `projects/nexon/mabinogi-eternity/evaluations/results/YYYY-MM-DD_작업명.json`
   - 날짜는 오늘 날짜 자동 사용
   - 작업명은 이미지 내용 기반으로 추론 (또는 사용자가 제공한 경우 그대로 사용)

3. **Git 커밋 & 푸시**
   ```bash
   git pull origin main --rebase
   git add <파일경로>
   git commit -m "Add VFX evaluation: <작업명>"
   git push origin main
   ```

4. **Notion 등록**
   - 데이터베이스 ID: `5a0a9702-8473-433b-a9ce-7dd3273ed9db`
   - 모든 점수, 요약, 강점, 문제점, 개선액션 자동 등록
   - 승인상태 기본값: `draft`

### 사용자가 추가 정보를 제공한 경우

이미지와 함께 아래 정보를 주면 그대로 사용:
- **작업명** — JSON 파일명과 Notion 작업명에 사용
- **작업자** — Notion 작업자 필드에 사용
- **스킬 유형** — Notion 스킬유형 필드에 사용 (히트이펙트 / AOE / 버프 / 보스패턴 / 기타)

정보가 없으면 이미지에서 추론하거나 기본값 사용.

### 팀원 사용 시

작업자 이름이 없으면 Notion 등록 전에 "작업자 이름을 알려주세요"라고 물어본다.

---

## 프로젝트 구조

```
projects/
└── nexon/
    └── mabinogi-eternity/
        └── evaluations/
            ├── vfx-eval-prompt.md       # 평가 시스템 프롬프트
            ├── vfx-eval-schema.json     # 출력 JSON 스키마
            ├── vfx-readability-rules.md # 채점 루브릭
            └── results/                 # 평가 결과 저장 위치
```
