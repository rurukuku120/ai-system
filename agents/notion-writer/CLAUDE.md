# Notion Writer Agent

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
