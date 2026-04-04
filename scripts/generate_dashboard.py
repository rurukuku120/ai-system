#!/usr/bin/env python3
"""
VFX 평가 결과 대시보드 생성기
results/ 폴더의 JSON 파일을 읽어 docs/index.html 생성
"""

import json
from pathlib import Path

REPO_ROOT   = Path(__file__).parent.parent
RESULTS_DIR = REPO_ROOT / "projects/nexon/mabinogi-eternity/evaluations/results"
DOCS_DIR    = REPO_ROOT / "docs"


def score_color(score):
    if score is None:
        return "#888"
    if score >= 4:
        return "#4caf50"
    if score >= 3:
        return "#ff9800"
    return "#f44336"


def status_badge(status):
    colors = {
        "approved": ("#4caf50", "승인"),
        "draft": ("#888", "검토중"),
        "revision_needed": ("#f44336", "수정필요"),
    }
    color, label = colors.get(status, ("#888", status or "-"))
    return f'<span style="background:{color};color:#fff;padding:2px 8px;border-radius:4px;font-size:12px">{label}</span>'


def load_results():
    results = []
    for f in sorted(RESULTS_DIR.glob("*.json"), reverse=True):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            data["_filename"] = f.name
            results.append(data)
        except Exception:
            continue
    return results


def render_score(val):
    if val is None:
        return "-"
    color = score_color(val)
    return f'<span style="color:{color};font-weight:bold">{val}</span>'


def generate_html(results):
    rows = ""
    for r in results:
        scores = r.get("scores", {})
        overall = r.get("overall_score")
        rows += f"""
        <tr>
            <td>{r.get("task_name", "-")}</td>
            <td>{r.get("_filename", "")[:10]}</td>
            <td>{render_score(scores.get("hit_timing"))}</td>
            <td>{render_score(scores.get("readability"))}</td>
            <td>{render_score(scores.get("silhouette"))}</td>
            <td>{render_score(scores.get("visual_hierarchy"))}</td>
            <td>{render_score(scores.get("impact"))}</td>
            <td>{render_score(scores.get("combat_readability"))}</td>
            <td style="font-size:16px;font-weight:bold;color:{score_color(overall)}">{overall or "-"}</td>
            <td>{status_badge(r.get("approval_status"))}</td>
        </tr>
        """

    count = len(results)
    avg = round(sum(r.get("overall_score", 0) for r in results if r.get("overall_score")) / count, 2) if count else 0

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VFX 평가 결과 대시보드</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #1a1a2e; color: #eee; margin: 0; padding: 24px; }}
    h1 {{ color: #fff; margin-bottom: 4px; }}
    .meta {{ color: #aaa; font-size: 14px; margin-bottom: 24px; }}
    .stats {{ display: flex; gap: 16px; margin-bottom: 24px; }}
    .stat {{ background: #16213e; border-radius: 8px; padding: 16px 24px; }}
    .stat-value {{ font-size: 28px; font-weight: bold; color: #4fc3f7; }}
    .stat-label {{ font-size: 12px; color: #aaa; margin-top: 4px; }}
    table {{ width: 100%; border-collapse: collapse; background: #16213e; border-radius: 8px; overflow: hidden; }}
    th {{ background: #0f3460; color: #4fc3f7; padding: 12px 10px; text-align: center; font-size: 13px; }}
    td {{ padding: 10px; text-align: center; border-bottom: 1px solid #0f3460; font-size: 13px; }}
    tr:last-child td {{ border-bottom: none; }}
    tr:hover td {{ background: #0f3460; }}
    td:first-child {{ text-align: left; font-weight: bold; }}
  </style>
</head>
<body>
  <h1>VFX 평가 결과 대시보드</h1>
  <p class="meta">Mabinogi Eternity — 자동 생성</p>

  <div class="stats">
    <div class="stat">
      <div class="stat-value">{count}</div>
      <div class="stat-label">총 평가 수</div>
    </div>
    <div class="stat">
      <div class="stat-value">{avg}</div>
      <div class="stat-label">평균 점수</div>
    </div>
  </div>

  <table>
    <thead>
      <tr>
        <th>작업명</th><th>날짜</th>
        <th>히트타이밍</th><th>가독성</th><th>실루엣</th>
        <th>시각계층</th><th>임팩트</th><th>전투가독성</th>
        <th>종합</th><th>상태</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</body>
</html>"""


def main():
    DOCS_DIR.mkdir(exist_ok=True)
    results = load_results()
    html = generate_html(results)
    output = DOCS_DIR / "index.html"
    output.write_text(html, encoding="utf-8")
    print(f"대시보드 생성 완료: {output} ({len(results)}개 결과)")


if __name__ == "__main__":
    main()
