#!/usr/bin/env python3
"""
VFX Evaluation Agent
GitHub Actions에서 자동 실행되는 VFX 가독성 평가 에이전트.

inbox/ 폴더의 이미지를 감지 → Gemini API 평가 → JSON 저장 → Notion 등록
"""

import os
import re
import json
from datetime import date
from pathlib import Path

import anthropic
import base64
import requests

# ── 경로 설정 ──────────────────────────────────────────────
REPO_ROOT   = Path(__file__).parent.parent
INBOX_DIR   = REPO_ROOT / "inbox"
RESULTS_DIR = REPO_ROOT / "projects/nexon/mabinogi-eternity/evaluations/results"
PROMPT_FILE = REPO_ROOT / "projects/nexon/mabinogi-eternity/evaluations/vfx-eval-prompt.md"
RULES_FILE  = REPO_ROOT / "projects/nexon/mabinogi-eternity/evaluations/vfx-readability-rules.md"
SCHEMA_FILE = REPO_ROOT / "projects/nexon/mabinogi-eternity/evaluations/vfx-eval-schema.json"

# ── 환경 변수 ──────────────────────────────────────────────
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
NOTION_TOKEN      = os.environ["NOTION_TOKEN"]
NOTION_DB_ID   = os.environ.get("NOTION_DB_ID", "5a0a9702-8478-433b-a9ce-7dd3273ed9db")

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


def find_new_images() -> list[Path]:
    """inbox/ 에서 처리되지 않은 이미지 파일 탐색"""
    return [
        f for f in INBOX_DIR.iterdir()
        if f.suffix.lower() in IMAGE_EXTENSIONS
        and f.parent.name != "processed"
    ]


def load_metadata(image_path: Path) -> dict:
    """
    메타데이터 로드 순서:
    1. 같은 이름의 .txt 파일 (key: value 형식)
    2. 파일명 파싱: 작업명_작업자_스킬유형.png
    """
    meta = {}

    txt_file = image_path.with_suffix(".txt")
    if txt_file.exists():
        for line in txt_file.read_text(encoding="utf-8").splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                meta[key.strip()] = val.strip()

    parts = image_path.stem.split("_")
    if not meta.get("작업명") and parts:
        meta["작업명"] = parts[0]
    if not meta.get("작업자") and len(parts) > 1:
        meta["작업자"] = parts[1]
    if not meta.get("스킬유형") and len(parts) > 2:
        meta["스킬유형"] = "_".join(parts[2:])

    return meta


def evaluate_image(image_path: Path, meta: dict) -> dict:
    """Anthropic API를 통해 VFX 이미지 평가"""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    system_prompt = "\n\n".join([
        PROMPT_FILE.read_text(encoding="utf-8"),
        "## 채점 루브릭\n" + RULES_FILE.read_text(encoding="utf-8"),
        "## 출력 형식\n반드시 JSON만 출력. 마크다운 코드블록 없이.\n"
        + SCHEMA_FILE.read_text(encoding="utf-8"),
    ])

    media_type_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp"}
    media_type = media_type_map.get(image_path.suffix.lower(), "image/png")
    image_b64 = base64.standard_b64encode(image_path.read_bytes()).decode()

    user_text = (
        f"이 VFX 스크린샷을 평가하라.\n"
        f"작업명: {meta.get('작업명', '미확인')}\n"
        f"작업자: {meta.get('작업자', '미확인')}\n"
        f"스킬유형: {meta.get('스킬유형', '미확인')}"
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_b64}},
                {"type": "text", "text": user_text},
            ],
        }],
    )

    text = response.content[0].text.strip()
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def save_result(result: dict, meta: dict) -> Path:
    """평가 결과를 JSON 파일로 저장"""
    today = date.today().strftime("%Y-%m-%d")
    task_name = result.get("task_name") or meta.get("작업명", "미확인")
    safe_name = re.sub(r'[\\/:*?"<>|]', "_", task_name)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / f"{today}_{safe_name}.json"
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def register_to_notion(result: dict, meta: dict) -> None:
    """Notion 데이터베이스에 평가 결과 등록"""
    def rich(text: str):
        return [{"type": "text", "text": {"content": str(text)[:2000]}}]

    scores = result.get("scores", {})

    properties = {
        "작업명":             {"title": rich(result.get("task_name", "미확인"))},
        "평가일":             {"date": {"start": date.today().strftime("%Y-%m-%d")}},
        "작업자":             {"rich_text": rich(meta.get("작업자", "미확인"))},
        "스킬유형":           {"select": {"name": meta.get("스킬유형", "기타")}},
        "hit_timing":         {"number": scores.get("hit_timing")},
        "readability":        {"number": scores.get("readability")},
        "silhouette":         {"number": scores.get("silhouette")},
        "visual_hierarchy":   {"number": scores.get("visual_hierarchy")},
        "impact":             {"number": scores.get("impact")},
        "combat_readability": {"number": scores.get("combat_readability")},
        "overall_score":      {"number": result.get("overall_score")},
        "강점":               {"rich_text": rich("\n".join(result.get("strengths", [])))},
        "문제점":             {"rich_text": rich("\n".join(result.get("issues", [])))},
        "개선액션":           {"rich_text": rich("\n".join(result.get("recommended_actions", [])))},
        "요약":               {"rich_text": rich(result.get("summary", ""))},
        "승인상태":           {"select": {"name": result.get("approval_status", "draft")}},
    }

    resp = requests.post(
        "https://notion-pat-proxy.nexon.co.kr/v1/pages",
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2025-09-03",
        },
        json={"parent": {"database_id": NOTION_DB_ID}, "properties": properties},
    )
    resp.raise_for_status()


def archive_image(image_path: Path) -> None:
    """처리 완료된 이미지를 inbox/processed/ 로 이동"""
    processed_dir = INBOX_DIR / "processed"
    processed_dir.mkdir(exist_ok=True)

    image_path.rename(processed_dir / image_path.name)

    txt_file = image_path.with_suffix(".txt")
    if txt_file.exists():
        txt_file.rename(processed_dir / txt_file.name)


def main():
    images = find_new_images()

    if not images:
        print("inbox/에 새 이미지 없음. 종료.")
        return

    for image_path in images:
        print(f"\n[시작] {image_path.name}")
        try:
            meta = load_metadata(image_path)
            print(f"  메타: {meta}")

            result = evaluate_image(image_path, meta)
            print(f"  평가 완료 - overall_score: {result.get('overall_score')}")

            output_path = save_result(result, meta)
            print(f"  저장: {output_path.name}")

            register_to_notion(result, meta)
            print("  Notion 등록 완료")

            archive_image(image_path)
            print("  아카이브 이동 완료")

        except Exception as e:
            print(f"  [오류] {image_path.name}: {e}")
            raise


if __name__ == "__main__":
    main()
