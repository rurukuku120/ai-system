#!/usr/bin/env python3
"""
notion_to_skill.py — Notion DB → .claude/commands/*.md 동기화 스크립트

Notion 스킬 DB의 각 페이지를 읽어 .claude/commands/{name}.md 파일로 동기화.

## Notion DB 필드 규약
| 필드명    | 타입       | 설명                                          |
|-----------|------------|-----------------------------------------------|
| Name      | title      | 커맨드 파일명 (예: vfx-eval → vfx-eval.md)    |
| Content   | rich_text  | .md 파일 본문 (마크다운)                       |
| Enabled   | checkbox   | false이면 동기화 대상에서 제외                 |

## 환경 변수
| 변수           | 필수 | 설명                              |
|----------------|------|-----------------------------------|
| NOTION_TOKEN   | 필수 | Notion PAT                        |
| SLACK_TOKEN    | 선택 | Slack Bot Token (알림 생략 가능)  |

## 사용법
  python sync/notion/notion_to_skill.py           # 실제 파일 쓰기
  python sync/notion/notion_to_skill.py --dry-run # 변경사항 미리보기
"""

import argparse
import os
import sys
from pathlib import Path

import requests

# ── 설정 ──────────────────────────────────────────────────────────────────────
REPO_ROOT      = Path(__file__).parent.parent.parent
COMMANDS_DIR   = REPO_ROOT / ".claude" / "commands"

NOTION_API_BASE  = os.environ.get("NOTION_API_BASE", "https://notion-pat-proxy.nexon.co.kr")
NOTION_VERSION   = "2022-06-28"
NOTION_DB_ID     = os.environ.get("NOTION_SKILL_DB_ID", "313dadb5-6b2f-8033-b8ad-000be9d352dd")

SLACK_CHANNEL_ID = "C08EC8WKY3D"  # #114_vfx유닛


# ── Notion API ─────────────────────────────────────────────────────────────────

def _notion_headers() -> dict:
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        raise EnvironmentError("NOTION_TOKEN 환경 변수가 설정되지 않았습니다.")
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def query_skill_db() -> list[dict]:
    """Notion DB에서 Enabled=true인 스킬 페이지 전체를 가져온다."""
    url = f"{NOTION_API_BASE}/v1/databases/{NOTION_DB_ID}/query"
    pages: list[dict] = []
    cursor = None

    while True:
        payload: dict = {"page_size": 100}
        if cursor:
            payload["start_cursor"] = cursor

        resp = requests.post(url, headers=_notion_headers(), json=payload, timeout=30)
        if not resp.ok:
            raise RuntimeError(f"Notion 쿼리 실패 {resp.status_code}: {resp.text[:400]}")

        data = resp.json()
        pages.extend(data.get("results", []))

        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")

    return pages


def _extract_plain_text(prop_value: dict) -> str:
    """Notion rich_text / title 프로퍼티에서 순수 텍스트 추출"""
    chunks = prop_value.get("rich_text") or prop_value.get("title") or []
    return "".join(c.get("plain_text", "") for c in chunks).strip()


def parse_page(page: dict) -> dict | None:
    """
    Notion 페이지 → {"name": str, "content": str} 변환.
    Enabled 필드가 false이면 None 반환.
    """
    props = page.get("properties", {})

    # Enabled 체크 (필드 없으면 기본 활성)
    enabled_prop = props.get("Enabled", {})
    if enabled_prop.get("type") == "checkbox" and not enabled_prop.get("checkbox", True):
        return None

    # Name (title 타입)
    name_prop = props.get("Name", {})
    name = _extract_plain_text(name_prop)
    if not name:
        return None

    # Content (rich_text 타입)
    content_prop = props.get("Content", {})
    content = _extract_plain_text(content_prop)

    return {"name": name, "content": content}


# ── 파일 동기화 ────────────────────────────────────────────────────────────────

def sync_skills(dry_run: bool = False) -> dict:
    """
    Notion DB → .claude/commands/ 동기화.

    Returns:
        {"created": [...], "updated": [...], "skipped": [...], "errors": [...]}
    """
    pages = query_skill_db()
    print(f"Notion에서 {len(pages)}개 페이지 읽음")

    COMMANDS_DIR.mkdir(parents=True, exist_ok=True)

    created: list[str] = []
    updated: list[str] = []
    skipped: list[str] = []
    errors:  list[str] = []

    for page in pages:
        try:
            parsed = parse_page(page)
            if parsed is None:
                skipped.append(page.get("id", "unknown"))
                continue

            name    = parsed["name"]
            content = parsed["content"]
            target  = COMMANDS_DIR / f"{name}.md"

            if not content:
                print(f"  [스킵] {name}.md — Content 비어 있음")
                skipped.append(name)
                continue

            if target.exists():
                existing = target.read_text(encoding="utf-8")
                if existing == content:
                    print(f"  [변경없음] {name}.md")
                    skipped.append(name)
                    continue
                status = "updated"
            else:
                status = "created"

            if dry_run:
                print(f"  [dry-run] {status}: {name}.md")
                print(f"    --- 미리보기 (앞 200자) ---")
                print(f"    {content[:200]!r}")
            else:
                target.write_text(content, encoding="utf-8")
                print(f"  [{status}] {name}.md")

            (created if status == "created" else updated).append(name)

        except Exception as exc:
            err_msg = f"{page.get('id', 'unknown')}: {exc}"
            print(f"  [오류] {err_msg}", file=sys.stderr)
            errors.append(err_msg)

    return {"created": created, "updated": updated, "skipped": skipped, "errors": errors}


# ── Slack 알림 ─────────────────────────────────────────────────────────────────

def send_slack_notification(result: dict, dry_run: bool = False) -> None:
    """동기화 결과를 Slack #114_vfx유닛 채널에 전송."""
    token = os.environ.get("SLACK_TOKEN")
    if not token:
        print("SLACK_TOKEN 없음 — Slack 알림 건너뜀")
        return

    created = result["created"]
    updated = result["updated"]
    errors  = result["errors"]

    if dry_run:
        print("dry-run 모드 — Slack 알림 건너뜀")
        return

    status_emoji = ":white_check_mark:" if not errors else ":warning:"
    lines = [f"{status_emoji} *Notion → Skill 동기화 완료*"]

    if created:
        lines.append(f"• 신규: {', '.join(f'`{n}`' for n in created)}")
    if updated:
        lines.append(f"• 업데이트: {', '.join(f'`{n}`' for n in updated)}")
    if not created and not updated:
        lines.append("• 변경사항 없음")
    if errors:
        lines.append(f"• 오류 {len(errors)}건:\n" + "\n".join(f"  - {e}" for e in errors))

    message = "\n".join(lines)

    resp = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"channel": SLACK_CHANNEL_ID, "text": message},
        timeout=15,
    )

    data = resp.json()
    if data.get("ok"):
        print(f"Slack 알림 전송 완료 (ts={data.get('ts')})")
    else:
        print(f"Slack 알림 실패: {data.get('error')}", file=sys.stderr)


# ── 진입점 ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Notion 스킬 DB → .claude/commands/ 동기화")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="파일을 실제로 쓰지 않고 변경사항만 출력"
    )
    args = parser.parse_args()

    print(f"{'[DRY-RUN] ' if args.dry_run else ''}동기화 시작 — DB: {NOTION_DB_ID}")

    result = sync_skills(dry_run=args.dry_run)

    print(
        f"\n완료: 신규 {len(result['created'])}개 / "
        f"업데이트 {len(result['updated'])}개 / "
        f"변경없음 {len(result['skipped'])}개 / "
        f"오류 {len(result['errors'])}개"
    )

    send_slack_notification(result, dry_run=args.dry_run)

    if result["errors"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
