# VFX 평가 자동화 워크플로우

## 사용 방법

스크린샷을 Claude에게 전달할 때 아래 문장을 함께 보내세요:

---

```
아래 이미지를 VFX 가독성 평가해줘.
작업명: [스킬 이름]
작업자: [본인 이름]
스킬 유형: [히트이펙트 / AOE / 버프 / 보스패턴 / 기타]

평가 완료 후 자동으로:
1. results/ 폴더에 JSON 저장
2. Git main 브랜치에 커밋 & 푸시
3. Notion VFX 피드백 DB에 등록
```

---

## Claude가 자동으로 처리하는 단계

| 단계 | 작업 | 도구 |
|------|------|------|
| 1 | 이미지 분석 및 6개 항목 점수 산출 | AI 분석 |
| 2 | JSON 파일 생성 (`YYYY-MM-DD_작업명.json`) | Write |
| 3 | Git commit & push (main 브랜치) | Bash |
| 4 | Notion DB에 행 추가 | Notion MCP |

## 파일 저장 위치

```
projects/nexon/mabinogi-eternity/evaluations/results/
└── YYYY-MM-DD_작업명.json
```

## 평가 항목 (각 1~5점)

| 항목 | 의미 |
|------|------|
| hit_timing | 히트 타이밍 명확성 |
| readability | 전반적 가독성 |
| silhouette | 실루엣 선명도 |
| visual_hierarchy | 시각적 계층 구조 |
| impact | 임팩트감 |
| combat_readability | 전투 상황 가독성 |

## 승인 상태

- `draft` — 검토 필요
- `approved` — 승인됨
- `revision_needed` — 수정 요청

## 스크린샷 촬영 가이드

- 히트 순간 프레임 캡처 권장
- 캐릭터 + 이펙트 전체가 화면에 포함되도록
- 배경이 너무 복잡하면 이펙트만 별도 캡처도 가능
- 형식: PNG 또는 JPG
