.PHONY: sync-skills sync-skills-dry

## Notion 스킬 DB → .claude/commands/ 동기화
sync-skills:
	python scripts/notion_to_skill.py

## 동기화 미리보기 (파일 변경 없음)
sync-skills-dry:
	python scripts/notion_to_skill.py --dry-run
