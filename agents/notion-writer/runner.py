#!/usr/bin/env python3
"""
Notion Writer Agent
구조화된 JSON 데이터를 받아 Notion 데이터베이스에 페이지를 생성하는 범용 에이전트.

사용법:
  # 임포트
  from agents.notion_writer.runner import write_page

  # CLI (파일)
  python agents/notion-writer/runner.py --database-id DB_ID --data result.json

  # CLI (stdin)
  echo '{"database_id": "...", "properties": {...}}' | python agents/notion-writer/runner.py
"""

import argparse
import json
import os
import sys
from typing import Any

import requests

NOTION_TOKEN   = os.environ.get("NOTION_TOKEN", "")
NOTION_API_BASE = os.environ.get("NOTION_API_BASE", "https://notion-pat-proxy.nexon.co.kr")
NOTION_VERSION = "2022-06-28"


# ── 프로퍼티 변환 ──────────────────────────────────────────────

def _rich(text: str) -> list[dict]:
    return [{"type": "text", "text": {"content": str(text)[:2000]}}]


def _build_property(prop_type: str, value: Any) -> dict:
    """type + value → Notion API 프로퍼티 포맷으로 변환"""
    if prop_type == "title":
        return {"title": _rich(value)}
    if prop_type == "rich_text":
        return {"rich_text": _rich(value)}
    if prop_type == "number":
        return {"number": float(value) if value is not None else None}
    if prop_type == "select":
        return {"select": {"name": str(value)}}
    if prop_type == "multi_select":
        items = value if isinstance(value, list) else [value]
        return {"multi_select": [{"name": str(v)} for v in items]}
    if prop_type == "date":
        return {"date": {"start": str(value)}}
    if prop_type == "checkbox":
        return {"checkbox": bool(value)}
    if prop_type == "url":
        return {"url": str(value)}
    if prop_type == "people":
        ids = value if isinstance(value, list) else [value]
        return {"people": [{"object": "user", "id": uid} for uid in ids]}
    raise ValueError(f"지원하지 않는 프로퍼티 타입: {prop_type}")


def build_properties(props_input: dict) -> dict:
    """
    입력 형식:
      {"제목": {"type": "title", "value": "..."},
       "점수": {"type": "number", "value": 87.5}, ...}

    출력: Notion API properties 포맷
    """
    result = {}
    for key, spec in props_input.items():
        prop_type = spec.get("type")
        value     = spec.get("value")
        if value is None and prop_type not in ("checkbox",):
            continue  # None 값은 건너뜀 (선택 필드)
        result[key] = _build_property(prop_type, value)
    return result


# ── Notion API 호출 ──────────────────────────────────────────────

def write_page(
    database_id: str,
    properties: dict,
    children: list | None = None,
    *,
    token: str | None = None,
) -> dict:
    """
    Notion 데이터베이스에 페이지를 생성한다.

    Args:
        database_id: Notion 데이터베이스 ID
        properties: build_properties() 결과 또는 raw Notion API 형식
        children: 페이지 본문 블록 (선택)
        token: NOTION_TOKEN 환경 변수 대신 직접 전달 시 사용

    Returns:
        {"page_id": "...", "url": "https://notion.so/..."}
    """
    api_token = token or NOTION_TOKEN
    if not api_token:
        raise EnvironmentError("NOTION_TOKEN 환경 변수가 설정되지 않았습니다.")

    payload: dict[str, Any] = {
        "parent": {"database_id": database_id},
        "properties": properties,
    }
    if children:
        payload["children"] = children

    resp = requests.post(
        f"{NOTION_API_BASE}/v1/pages",
        headers={
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION,
        },
        json=payload,
        timeout=30,
    )

    if not resp.ok:
        raise RuntimeError(
            f"Notion API 오류 {resp.status_code}: {resp.text[:500]}"
        )

    data = resp.json()
    page_id = data.get("id", "")
    url = data.get("url", f"https://www.notion.so/{page_id.replace('-', '')}")
    return {"page_id": page_id, "url": url}


def write_page_from_payload(payload: dict, token: str | None = None) -> dict:
    """
    CLAUDE.md 입력 형식(type+value 구조)을 파싱하여 write_page 호출.

    Args:
        payload: {"database_id": "...", "properties": {"키": {"type": "...", "value": ...}}, "children": [...]}
    """
    database_id = payload.get("database_id")
    if not database_id:
        raise ValueError("payload에 database_id가 없습니다.")

    raw_props = payload.get("properties", {})
    children  = payload.get("children")

    properties = build_properties(raw_props)
    return write_page(database_id, properties, children, token=token)


# ── CLI 진입점 ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Notion 페이지 생성 에이전트")
    parser.add_argument("--database-id", help="Notion 데이터베이스 ID (payload 내 database_id 대신 사용)")
    parser.add_argument("--data", help="입력 JSON 파일 경로 (없으면 stdin)")
    args = parser.parse_args()

    # 입력 읽기
    if args.data:
        with open(args.data, encoding="utf-8") as f:
            payload = json.load(f)
    else:
        payload = json.load(sys.stdin)

    # CLI 인수로 database_id 오버라이드
    if args.database_id:
        payload["database_id"] = args.database_id

    result = write_page_from_payload(payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
