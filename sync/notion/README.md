# sync/notion

Notion 연동 코드를 둔다.

외부 페이지 생성은 사용자 명시 요청 또는 에이전트 계약이 있을 때만 수행한다.

## Notion skills 동기화

Notion에서 관리하는 skill을 CLI에서도 사용할 수 있도록 `skills/` 폴더로 동기화한다.

현재 기본 원본은 `skills.source.json`에 기록한다.

```powershell
python sync/notion/notion_to_skills.py --dry-run
python sync/notion/notion_to_skills.py
```

## 환경 변수

| 변수 | 설명 |
|---|---|
| `NOTION_TOKEN` | Notion API token |
| `NOTION_SKILLS_DATABASE_ID` | skill 데이터베이스 ID, 선택 |
| `NOTION_SKILLS_DATABASE_URL` | skill 데이터베이스 URL, 선택 |

`skills.source.json`에 기본 database URL과 ID가 있으면 `NOTION_TOKEN`만으로 실행할 수 있다.

## 필터 후보

스크린샷 기준으로 확인된 후보 속성은 `유형`, `제목`, `생성자`, `태그`다. `AI Skill` 행만 동기화하려면 다음 조건이 후보지만, 실제 DB schema 접근 검증 후 `skills.source.json`에 확정한다.

```powershell
python sync/notion/notion_to_skills.py --filter-property "유형" --filter-type select --filter-equals "AI Skill"
```

지원하는 필터 타입은 `select`, `multi_select`, `status`, `rich_text`, `title`이다.

초기 구현은 Notion 데이터베이스의 다음 속성 이름을 기대한다.

| Notion property | 용도 |
|---|---|
| `제목` | skill 이름 후보 |
| `Slug` | 로컬 폴더 이름 |
| `Description` | skill 설명 |
| `Tags` | 태그 |
