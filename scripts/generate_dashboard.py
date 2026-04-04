#!/usr/bin/env python3
"""
VFX 피드백 대시보드 생성기
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


def escape_js(text):
    return str(text).replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def generate_html(results):
    # JSON 데이터를 JS에 임베드
    js_data = json.dumps(results, ensure_ascii=False)

    rows = ""
    for i, r in enumerate(results):
        scores = r.get("scores", {})
        overall = r.get("overall_score")
        rows += f"""
        <tr onclick="showDetail({i})" style="cursor:pointer">
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
  <title>VFX 피드백 대시보드</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #1a1a2e; color: #eee; margin: 0; padding: 24px; }}
    h1 {{ color: #fff; margin-bottom: 4px; }}
    .meta {{ color: #aaa; font-size: 14px; margin-bottom: 24px; }}
    .stats {{ display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }}
    .stat {{ background: #16213e; border-radius: 8px; padding: 16px 24px; }}
    .stat-value {{ font-size: 28px; font-weight: bold; color: #4fc3f7; }}
    .stat-label {{ font-size: 12px; color: #aaa; margin-top: 4px; }}
    table {{ width: 100%; border-collapse: collapse; background: #16213e; border-radius: 8px; overflow: hidden; }}
    th {{ background: #0f3460; color: #4fc3f7; padding: 12px 10px; text-align: center; font-size: 13px; }}
    td {{ padding: 10px; text-align: center; border-bottom: 1px solid #0f3460; font-size: 13px; }}
    tr:last-child td {{ border-bottom: none; }}
    tr:hover td {{ background: #1a4a7a; }}
    td:first-child {{ text-align: left; font-weight: bold; }}

    /* 모달 */
    .modal-overlay {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:100; align-items:center; justify-content:center; }}
    .modal-overlay.active {{ display:flex; }}
    .modal {{ background:#16213e; border-radius:12px; padding:28px; max-width:600px; width:90%; max-height:85vh; overflow-y:auto; position:relative; }}
    .modal-close {{ position:absolute; top:16px; right:16px; background:none; border:none; color:#aaa; font-size:22px; cursor:pointer; }}
    .modal-close:hover {{ color:#fff; }}
    .modal h2 {{ margin-top:0; color:#4fc3f7; }}
    .modal-section {{ margin-bottom:20px; }}
    .modal-section h3 {{ color:#ff9800; font-size:14px; margin-bottom:8px; border-bottom:1px solid #0f3460; padding-bottom:4px; }}
    .modal-section p {{ color:#ccc; font-size:14px; line-height:1.6; margin:0; }}
    .score-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin-bottom:20px; }}
    .score-item {{ background:#0f3460; border-radius:6px; padding:10px; text-align:center; }}
    .score-item .label {{ font-size:11px; color:#aaa; }}
    .score-item .value {{ font-size:20px; font-weight:bold; margin-top:2px; }}
    .tag {{ display:inline-block; background:#0f3460; border-radius:4px; padding:4px 8px; font-size:12px; margin:3px 2px; color:#ccc; }}
  </style>
</head>
<body>
  <h1>VFX 피드백 대시보드</h1>
  <p class="meta">Mabinogi Eternity — 행을 클릭하면 상세 내용을 볼 수 있어요</p>

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

  <!-- 상세 모달 -->
  <div class="modal-overlay" id="modal" onclick="closeModal(event)">
    <div class="modal">
      <button class="modal-close" onclick="document.getElementById('modal').classList.remove('active')">✕</button>
      <h2 id="modal-title"></h2>
      <div class="score-grid" id="modal-scores"></div>
      <div class="modal-section">
        <h3>요약</h3>
        <p id="modal-summary"></p>
      </div>
      <div class="modal-section">
        <h3>강점</h3>
        <div id="modal-strengths"></div>
      </div>
      <div class="modal-section">
        <h3>문제점</h3>
        <div id="modal-issues"></div>
      </div>
      <div class="modal-section">
        <h3>개선 액션</h3>
        <div id="modal-actions"></div>
      </div>
    </div>
  </div>

  <script>
    const data = {js_data};
    const scoreLabels = {{
      hit_timing: '히트타이밍', readability: '가독성', silhouette: '실루엣',
      visual_hierarchy: '시각계층', impact: '임팩트', combat_readability: '전투가독성'
    }};
    const scoreColors = v => v >= 4 ? '#4caf50' : v >= 3 ? '#ff9800' : '#f44336';

    function showDetail(i) {{
      const r = data[i];
      const scores = r.scores || {{}};
      document.getElementById('modal-title').textContent = r.task_name || '-';
      document.getElementById('modal-summary').textContent = r.summary || '-';

      document.getElementById('modal-scores').innerHTML =
        Object.entries(scoreLabels).map(([k, label]) => {{
          const v = scores[k];
          return `<div class="score-item">
            <div class="label">${{label}}</div>
            <div class="value" style="color:${{scoreColors(v)}}">${{v || '-'}}</div>
          </div>`;
        }}).join('') +
        `<div class="score-item">
          <div class="label">종합점수</div>
          <div class="value" style="color:${{scoreColors(r.overall_score)}};font-size:24px">${{r.overall_score || '-'}}</div>
        </div>`;

      document.getElementById('modal-strengths').innerHTML =
        (r.strengths || []).map(s => `<span class="tag">✓ ${{s}}</span>`).join('');
      document.getElementById('modal-issues').innerHTML =
        (r.issues || []).map(s => `<span class="tag">⚠ ${{s}}</span>`).join('');
      document.getElementById('modal-actions').innerHTML =
        (r.recommended_actions || []).map(s => `<span class="tag">→ ${{s}}</span>`).join('');

      document.getElementById('modal').classList.add('active');
    }}

    function closeModal(e) {{
      if (e.target.id === 'modal') document.getElementById('modal').classList.remove('active');
    }}
  </script>
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
