# skills

AI와 CLI가 재사용할 수 있는 능력 단위를 둔다.

`skills/`는 agent가 수행할 수 있는 구체적인 절차, 프롬프트, 도구 사용법, 출력 형식을 관리한다. Notion에서 관리되는 skill은 `sync/notion/notion_to_skills.py`를 통해 이 폴더로 동기화한다.

## 구조

```text
skills/<skill-id>/
├── skill.yaml
└── SKILL.md
```

## 원칙

- `skill.yaml`은 기계가 읽는 skill 계약이다.
- `SKILL.md`는 AI와 사람이 함께 읽는 실행 지침이다.
- Notion이 원본인 skill은 `skill.yaml`의 `source.type`을 `notion`으로 둔다.
- 로컬에서 직접 관리하는 skill은 `source.type`을 `local`로 둔다.

## 동기화

```powershell
python sync/notion/notion_to_skills.py --dry-run
python sync/notion/notion_to_skills.py
```
