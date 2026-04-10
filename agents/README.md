# Agents 인덱스

> 자동 생성됨 — 2026-04-11 00:27
> `agents/agent-manager/runner.py`가 각 에이전트의 `CLAUDE.md`를 읽어 갱신합니다.
> 직접 편집하지 마세요. `/update-agents`로 갱신하세요.

---

## 에이전트 목록

| 에이전트 | 폴더 | 트리거 | 슬래시 커맨드 |
|----------|------|--------|--------------|
| [Unreal Asset Parser Agent](#asset-parser) | `agents/asset-parser/` | 수동 호출 | — |
| [Dashboard Builder Agent](#dashboard-builder) | `agents/dashboard-builder/` | 수동 호출 | `/dashboard-build` |
| [Notion Writer Agent](#notion-writer) | `agents/notion-writer/` | 수동 호출 | — |
| [Claude Session Logger Agent](#session-logger) | `agents/session-logger/` | Stop 훅 | — |
| [VFX Evaluator Agent](#vfx-evaluator) | `agents/vfx-evaluator/` | GitHub Actions | — |

---

## Unreal Asset Parser Agent

> 폴더: `agents/asset-parser/`

## 역할
UE5 `.uasset` 바이너리 파일을 파싱하여 구조화된 데이터를 추출하는 에이전트.
에디터 없이 독립 실행 가능한 파서 툴을 호출하고 결과를 해석한다.

## 적용 프로젝트
- 넥슨 / 마비노기 이터니티 (UE5)

---

## 시스템 프롬프트

```
당신은 Unreal Engine 5 에셋 파일(.uasset) 분석 전문가입니다.
바이너리 파서 툴을 호출하여 에셋 데이터를 추출하고, 결과를 명확하게 해석해 제공합니다.

## 처리 가능한 에셋 타입
- DataTable: 행/열 구조의 게임 데이터 (아이템, 스탯 등)
- StaticMesh / SkeletalMesh: 폴리곤 수, LOD, 소켓 등 메타데이터
- Texture2D: 해상도, 압축 포맷, 밉맵 수
- Blueprint / BlueprintGeneratedClass: 노드 구조, 변수, 함수 목록
- 패키지 의존성: import/export 테이블 기반 참조 그래프

## 툴 사용 원칙
1. 파일 경로를 받으면 해당 툴을 즉시 호출한다.
2. 여러 에셋을 한 번에 처리할 경우 배치 툴을 사용한다.
3. 파싱 실패 시 에러 유형(magic mismatch, version unsupported, truncated 등)을 명시한다.
4. 결과는 항상 JSON으로 반환하고, 요약 설명을 함께 제공한다.

## 출력 형식
파싱 결과 요약:
- 에셋 타입: {class_name}
- UE 버전: {file_version_ue5}
- 익스포트 수: {export_count}
- 임포트(의존성) 수: {import_count}
[추출 데이터 JSON]

## 주의사항
- IoStore(.ucas/.utoc) 패키지 포맷은 별도 툴 필요 (cooked 빌드)
- 에디터 에셋(uasset)과 쿠킹된 에셋은 포맷이 다를 수 있음
- 암호화된 에셋은 키 없이 파싱 불가
```

---

## 툴 목록

| 툴 이름 | 설명 | 입력 |
|---|---|---|
| `parse_asset_summary` | 파일 헤더 요약 (버전, 카운트 등) | `file_path` |
| `parse_dependencies` | import 테이블 기반 의존성 추출 | `file_path` |
| `parse_datatable` | DataTable 행 데이터 추출 | `file_path` |
| `parse_mesh_metadata` | 메시/텍스처 메타데이터 추출 | `file_path` |
| `parse_blueprint` | Blueprint 구조 추출 | `file_path` |
| `batch_parse` | 디렉토리 내 전체 에셋 일괄 파싱 | `dir_path`, `asset_types[]` |

툴 구현: `tools/uasset_parser.py`
툴 스키마: `tools/tool_schemas.json`

---

## 사용 예시

```
사용자: Content/Items/DataTable_ItemBase.uasset 파일 분석해줘

에이전트:
1. parse_asset_summary 호출 → 파일 헤더 확인
2. parse_datatable 호출 → 행 데이터 추출
3. parse_dependencies 호출 → 참조 에셋 목록 확인
4. 결과 JSON 반환 + 요약 설명 제공
```

---

## 관련 파일
- `tools/uasset_parser.py` — Python 파서 구현체
- `tools/tool_schemas.json` — Claude API function calling 스키마

---

## Dashboard Builder Agent

> 폴더: `agents/dashboard-builder/`

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

---

## Notion Writer Agent

> 폴더: `agents/notion-writer/`

## 역할
구조화된 데이터(JSON)를 받아 Notion 데이터베이스에 페이지를 생성하는 범용 쓰기 에이전트.
VFX Evaluator, Asset Parser 등 다른 에이전트가 Notion에 결과를 저장할 때 호출한다.

## 입출력

- **입력**: JSON 페이로드 (database_id + properties + 선택적 page content)
- **출력**: 생성된 Notion 페이지 URL 및 page_id (stdout)

## 실행 방법

```bash
# 1. 함수로 임포트 (다른 에이전트에서 호출)
from agents.notion_writer.runner import write_page
page_id = write_page(database_id="...", properties={...})

# 2. CLI 직접 실행 (파일 경로)
python agents/notion-writer/runner.py --database-id DB_ID --data result.json

# 3. CLI 직접 실행 (stdin)
echo '{"database_id": "...", "properties": {...}}' | python agents/notion-writer/runner.py
```

## 입력 JSON 형식

```json
{
  "database_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "properties": {
    "제목": { "type": "title", "value": "페이지 제목" },
    "점수": { "type": "number", "value": 87.5 },
    "상태": { "type": "select", "value": "완료" },
    "날짜": { "type": "date", "value": "2026-04-10" },
    "설명": { "type": "rich_text", "value": "긴 텍스트..." },
    "담당자": { "type": "people", "value": ["user_id_1"] },
    "체크": { "type": "checkbox", "value": true }
  },
  "children": []
}
```

## 지원 프로퍼티 타입

| type | value 형식 | 설명 |
|------|-----------|------|
| `title` | string | 페이지 제목 (필수) |
| `rich_text` | string | 긴 텍스트 |
| `number` | float/int | 숫자 |
| `select` | string | 단일 선택 |
| `multi_select` | string[] | 다중 선택 |
| `date` | "YYYY-MM-DD" | 날짜 |
| `checkbox` | bool | 체크박스 |
| `url` | string | URL |
| `people` | user_id[] | 사용자 |

## 환경 변수

| 변수 | 필수 | 설명 |
|------|------|------|
| `NOTION_TOKEN` | 필수 | Notion PAT |
| `NOTION_API_BASE` | 선택 | 기본값: `https://notion-pat-proxy.nexon.co.kr` |

## 관련 파일
- `runner.py` — 실행 진입점 및 임포트 가능한 함수

---

## Claude Session Logger Agent

> 폴더: `agents/session-logger/`

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
- `runner.py` — 실행 스크립트
- `.claude/commands/session-logger.md` — 슬래시 커맨드 (수동 실행)
- `~/.claude/settings.json` — Stop 훅 등록

---

## VFX Evaluator Agent

> 폴더: `agents/vfx-evaluator/`

Nexon 마비노기 이터니티 VFX 가독성 자동 평가 에이전트.

## 역할

VFX 스크린샷을 입력받아 가독성 기준으로 평가하고, 결과를 JSON으로 저장 + Notion에 등록.

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
ANTHROPIC_API_KEY=... NOTION_TOKEN=... python agents/vfx-evaluator/runner.py
```

## 환경 변수

| 변수 | 필수 | 설명 |
|------|------|------|
| `ANTHROPIC_API_KEY` | 필수 | Anthropic API 키 |
| `NOTION_TOKEN` | 필수 | Notion PAT |
| `NOTION_DB_ID` | 선택 | Notion 데이터베이스 ID |

---

