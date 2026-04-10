# AI System

> **언어 설정:** 항상 한국어로 응답한다.

Nexon VFX팀의 AI 도구 및 평가 시스템 관리 저장소.

## 프로젝트 구조

```
agents/                              # 에이전트 정의 (핵심)
├── vfx-evaluator/                   # VFX 가독성 평가 에이전트
│   ├── CLAUDE.md                    # 에이전트 역할 및 사용법
│   ├── runner.py                    # 실행 진입점
│   ├── prompt.md                    # 평가 시스템 프롬프트
│   ├── rules.md                     # 채점 루브릭
│   └── schema.json                  # 출력 JSON 스키마
└── asset-parser/                    # UE5 에셋 파서 에이전트
    ├── CLAUDE.md                    # 에이전트 역할 및 사용법
    └── tools/                       # 파서 툴 구현체

inbox/                               # 평가 대상 이미지 투입 폴더
projects/
└── nexon/
    └── mabinogi-eternity/
        └── evaluations/
            └── results/             # 평가 결과 JSON 저장 위치

scripts/
└── generate_dashboard.py            # 대시보드 생성 유틸리티
```

## 커스텀 명령어

- `/vfx-eval` — VFX 가독성 평가 파이프라인 실행

## 새 에이전트 추가 방법

1. `agents/[에이전트명]/` 폴더 생성
2. `CLAUDE.md` — 역할, 입출력, 실행 방법 정의
3. `runner.py` — 실행 로직 구현
4. `.claude/commands/[에이전트명].md` — 슬래시 커맨드 등록
