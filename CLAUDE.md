# AI System

Nexon VFX팀의 AI 도구 및 평가 시스템 관리 저장소.

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

## 커스텀 명령어

- `/vfx-eval` — VFX 가독성 평가 파이프라인 실행
