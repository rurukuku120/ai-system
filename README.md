# ai-system

멀티 에이전트 통합 관리 시스템.
에이전트 정의, LLM별 지침, 자동화 워크플로우, 학습 메모리, Notion 동기화를 통합 관리한다.

## 구조 개요

| 폴더 | 역할 |
|------|------|
| common/ | 전체 시스템 공통 기반 (규칙/형식/프로토콜) |
| models/ | LLM별 개별 지침 |
| use-cases/ | 프롬프트/에이전트/워크플로우 정의 |
| projects/ | 회사/프로젝트별 전용 지침 |
| memory/ | 에이전트 학습 누적 |
| sync/ | Notion/GitHub 연동 |
| evals/ | 시스템 평가 |
| config/ | 환경별 설정 |
| security/ | 접근 권한/민감 정보 |
| monitoring/ | 로그/성능 지표 |
| docs/ | 온보딩/운영 가이드 |
