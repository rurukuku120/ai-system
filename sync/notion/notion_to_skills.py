#!/usr/bin/env python3
"""Sync Notion skill pages into local CLI-readable skill folders."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"
SOURCE_CONFIG = Path(__file__).with_name("skills.source.json")
NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9가-힣_-]+", "-", value.strip()).strip("-").lower()
    slug = re.sub(r"-+", "-", slug)
    return slug or "untitled-skill"


def normalize_notion_id(value: str) -> str:
    return value.replace("-", "").strip()


def database_id_from_url(url: str) -> str:
    parsed = urlparse(url)
    path_parts = [part for part in parsed.path.split("/") if part]
    if not path_parts:
        return ""

    candidate = path_parts[-1]
    match = re.search(r"([0-9a-fA-F]{32})$", candidate.replace("-", ""))
    return match.group(1) if match else ""


def load_source_config() -> dict:
    if not SOURCE_CONFIG.exists():
        return {}
    return json.loads(SOURCE_CONFIG.read_text(encoding="utf-8"))


def notion_request(method: str, path: str, token: str, payload: dict | None = None) -> dict:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = Request(
        f"{NOTION_API}{path}",
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        message = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Notion API error {exc.code}: {message}") from exc


def plain_text(items: list[dict]) -> str:
    return "".join(item.get("plain_text", "") for item in items)


def property_text(properties: dict, name: str) -> str:
    prop = properties.get(name, {})
    prop_type = prop.get("type")
    if prop_type == "title":
        return plain_text(prop.get("title", []))
    if prop_type == "rich_text":
        return plain_text(prop.get("rich_text", []))
    if prop_type == "url":
        return prop.get("url") or ""
    if prop_type == "select":
        selected = prop.get("select")
        return selected.get("name", "") if selected else ""
    return ""


def property_tags(properties: dict, name: str) -> list[str]:
    prop = properties.get(name, {})
    if prop.get("type") != "multi_select":
        return []
    return [item.get("name", "") for item in prop.get("multi_select", []) if item.get("name")]


def block_to_markdown(block: dict) -> str:
    block_type = block.get("type")
    data = block.get(block_type, {})

    if block_type == "paragraph":
        text = plain_text(data.get("rich_text", []))
        return f"{text}\n" if text else ""
    if block_type == "heading_1":
        return f"# {plain_text(data.get('rich_text', []))}\n"
    if block_type == "heading_2":
        return f"## {plain_text(data.get('rich_text', []))}\n"
    if block_type == "heading_3":
        return f"### {plain_text(data.get('rich_text', []))}\n"
    if block_type == "bulleted_list_item":
        return f"- {plain_text(data.get('rich_text', []))}\n"
    if block_type == "numbered_list_item":
        return f"1. {plain_text(data.get('rich_text', []))}\n"
    if block_type == "to_do":
        checked = "x" if data.get("checked") else " "
        return f"- [{checked}] {plain_text(data.get('rich_text', []))}\n"
    if block_type == "code":
        language = data.get("language", "")
        text = plain_text(data.get("rich_text", []))
        return f"```{language}\n{text}\n```\n"
    if block_type == "quote":
        text = plain_text(data.get("rich_text", []))
        return f"> {text}\n"
    return ""


def fetch_page_markdown(page_id: str, token: str) -> str:
    blocks: list[dict] = []
    cursor = None
    while True:
        suffix = f"&start_cursor={cursor}" if cursor else ""
        payload = notion_request("GET", f"/blocks/{page_id}/children?page_size=100{suffix}", token)
        blocks.extend(payload.get("results", []))
        if not payload.get("has_more"):
            break
        cursor = payload.get("next_cursor")

    markdown = "\n".join(part for block in blocks if (part := block_to_markdown(block).rstrip()))
    return markdown.strip() + "\n" if markdown.strip() else ""


def build_database_filter(property_name: str, property_type: str, equals: str) -> dict | None:
    if not property_name or not equals:
        return None

    if property_type == "select":
        return {"property": property_name, "select": {"equals": equals}}
    if property_type == "multi_select":
        return {"property": property_name, "multi_select": {"contains": equals}}
    if property_type == "status":
        return {"property": property_name, "status": {"equals": equals}}
    if property_type == "rich_text":
        return {"property": property_name, "rich_text": {"equals": equals}}
    if property_type == "title":
        return {"property": property_name, "title": {"equals": equals}}

    raise ValueError(f"Unsupported filter property type: {property_type}")


def query_database(database_id: str, token: str, database_filter: dict | None = None) -> list[dict]:
    pages: list[dict] = []
    cursor = None
    while True:
        payload: dict = {"page_size": 100}
        if database_filter:
            payload["filter"] = database_filter
        if cursor:
            payload["start_cursor"] = cursor
        response = notion_request("POST", f"/databases/{database_id}/query", token, payload)
        pages.extend(response.get("results", []))
        if not response.get("has_more"):
            break
        cursor = response.get("next_cursor")
    return pages


def render_manifest(skill: dict) -> str:
    tags = "\n".join(f"  - {tag}" for tag in skill["tags"]) or "  []"
    return f"""id: {skill['id']}
name: {skill['name']}
version: 0.1.0
description: {json.dumps(skill['description'], ensure_ascii=False)}
source:
  type: notion
  id: {skill['source_id']}
  url: {skill['url']}
inputs: []
outputs: []
tags:
{tags}
updated_at: {skill['updated_at']}
"""


def render_skill_md(skill: dict) -> str:
    body = skill["body"].strip()
    if not body:
        body = "## 목적\n\n아직 내용이 없습니다.\n"
    return f"""# {skill['name']}

> Notion에서 동기화됨: {skill['url']}

{body}
"""


def page_to_skill(page: dict, token: str) -> dict:
    properties = page.get("properties", {})
    name = property_text(properties, "Name") or property_text(properties, "제목") or property_text(properties, "이름") or "Untitled Skill"
    slug = property_text(properties, "Slug") or property_text(properties, "slug") or slugify(name)
    description = property_text(properties, "Description") or property_text(properties, "설명")
    tags = property_tags(properties, "Tags") or property_tags(properties, "태그")
    page_id = page["id"]

    return {
        "id": slugify(slug),
        "name": name,
        "description": description or name,
        "tags": tags,
        "source_id": page_id,
        "url": page.get("url", ""),
        "body": fetch_page_markdown(page_id, token),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def write_skill(skill: dict, dry_run: bool) -> None:
    skill_dir = SKILLS_DIR / skill["id"]
    manifest_path = skill_dir / "skill.yaml"
    skill_path = skill_dir / "SKILL.md"

    if dry_run:
        print(f"[dry-run] would write {manifest_path}")
        print(f"[dry-run] would write {skill_path}")
        return

    skill_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(render_manifest(skill), encoding="utf-8")
    skill_path.write_text(render_skill_md(skill), encoding="utf-8")
    print(f"[sync] wrote {skill_dir}")


def main() -> int:
    source_config = load_source_config()

    parser = argparse.ArgumentParser(description="Sync Notion skills into local skills/")
    parser.add_argument(
        "--database-id",
        default=os.environ.get("NOTION_SKILLS_DATABASE_ID", source_config.get("database_id", "")),
    )
    parser.add_argument(
        "--database-url",
        default=os.environ.get("NOTION_SKILLS_DATABASE_URL", source_config.get("database_url", "")),
    )
    source_filter = source_config.get("filter", {})
    parser.add_argument("--filter-property", default=os.environ.get("NOTION_SKILLS_FILTER_PROPERTY", source_filter.get("property", "")))
    parser.add_argument("--filter-type", default=os.environ.get("NOTION_SKILLS_FILTER_TYPE", source_filter.get("type", "select")))
    parser.add_argument("--filter-equals", default=os.environ.get("NOTION_SKILLS_FILTER_EQUALS", source_filter.get("equals", "")))
    parser.add_argument("--token", default=os.environ.get("NOTION_TOKEN", ""))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    database_id = normalize_notion_id(args.database_id) or database_id_from_url(args.database_url)

    if not args.token:
        print("[notion-to-skills] NOTION_TOKEN is required", file=sys.stderr)
        return 2
    if not database_id:
        print("[notion-to-skills] NOTION_SKILLS_DATABASE_ID, NOTION_SKILLS_DATABASE_URL, --database-id, or --database-url is required", file=sys.stderr)
        return 2

    database_filter = build_database_filter(args.filter_property, args.filter_type, args.filter_equals)
    if database_filter:
        print(f"[notion-to-skills] filter: {args.filter_property} {args.filter_type} == {args.filter_equals}")

    pages = query_database(database_id, args.token, database_filter)
    print(f"[notion-to-skills] fetched {len(pages)} pages")
    for page in pages:
        write_skill(page_to_skill(page, args.token), args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
