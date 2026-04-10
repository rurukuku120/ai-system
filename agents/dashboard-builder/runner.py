#!/usr/bin/env python3
"""
Dashboard Builder Agent
VFX 평가 결과 + 에이전트 상태를 읽어 docs/index.html 생성.
"""

import json
from pathlib import Path

AGENT_DIR   = Path(__file__).parent
REPO_ROOT   = AGENT_DIR.parent.parent
RESULTS_DIR = REPO_ROOT / "projects/nexon/mabinogi-eternity/evaluations/results"
STATUS_JSON = REPO_ROOT / "agents/status.json"
DOCS_DIR    = REPO_ROOT / "docs"


# ── 유틸 ──────────────────────────────────────────────────────────────────────

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
        "approved":        ("#4caf50", "승인"),
        "draft":           ("#888",    "검토중"),
        "revision_needed": ("#f44336", "수정필요"),
    }
    color, label = colors.get(status, ("#888", status or "-"))
    return f'<span style="background:{color};color:#fff;padding:2px 8px;border-radius:4px;font-size:12px">{label}</span>'


def render_score(val):
    if val is None:
        return "-"
    return f'<span style="color:{score_color(val)};font-weight:bold">{val}</span>'


# ── 데이터 로드 ───────────────────────────────────────────────────────────────

def load_vfx_results() -> list[dict]:
    results = []
    for f in sorted(RESULTS_DIR.glob("*.json"), reverse=True):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            data["_filename"] = f.name
            results.append(data)
        except Exception:
            continue
    return results


def load_agent_status() -> dict:
    try:
        return json.loads(STATUS_JSON.read_text(encoding="utf-8"))
    except Exception:
        return {"updated_at": "", "agents": []}


# ── HTML 생성 ─────────────────────────────────────────────────────────────────

def build_vfx_rows(results: list[dict]) -> str:
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
        </tr>"""
    return rows


def build_agent_cards(agents: list[dict]) -> str:
    status_color = {"healthy": "#4caf50", "warning": "#ff9800", "error": "#f44336"}
    status_label = {"healthy": "정상", "warning": "경고", "error": "오류"}

    cards = ""
    for a in agents:
        color = status_color.get(a["status"], "#555")
        label = status_label.get(a["status"], a["status"])
        claude_md_color = "#4fc3f7" if a["has_claude_md"] else "#f44336"
        claude_md_bg    = "#0f3460" if a["has_claude_md"] else "#3a0000"
        runner_color    = "#4fc3f7" if a["has_runner"] else "#f44336"
        runner_bg       = "#0f3460" if a["has_runner"] else "#3a0000"
        syntax_ok       = a.get("syntax_ok")
        syntax_color    = "#4fc3f7" if syntax_ok else ("#f44336" if syntax_ok is False else "#666")
        syntax_bg       = "#0f3460" if syntax_ok else ("#3a0000" if syntax_ok is False else "#222")
        issues_html     = "".join(f'<div style="font-size:12px;color:#f44336;margin-top:6px">! {i}</div>' for i in a.get("issues", []))

        cards += f"""
        <div style="background:#16213e;border-radius:10px;padding:20px;border-left:4px solid {color}">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <span style="font-weight:bold;font-size:15px;">{a["name"]}</span>
            <span style="color:{color};font-size:13px;font-weight:bold;">● {label}</span>
          </div>
          <div style="font-size:12px;color:#aaa;margin-bottom:8px;">마지막 커밋: {a.get("last_commit", "-")}</div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;">
            <span style="font-size:11px;padding:3px 8px;border-radius:4px;background:{claude_md_bg};color:{claude_md_color}">CLAUDE.md</span>
            <span style="font-size:11px;padding:3px 8px;border-radius:4px;background:{runner_bg};color:{runner_color}">runner.py</span>
            <span style="font-size:11px;padding:3px 8px;border-radius:4px;background:{syntax_bg};color:{syntax_color}">문법</span>
          </div>
          {issues_html}
        </div>"""
    return cards


def generate_html(results: list[dict], agent_status: dict) -> str:
    count = len(results)
    avg   = round(sum(r.get("overall_score", 0) for r in results if r.get("overall_score")) / count, 2) if count else 0

    agents        = agent_status.get("agents", [])
    updated_at    = (agent_status.get("updated_at") or "")[:16].replace("T", " ")
    total         = len(agents)
    healthy_count = sum(1 for a in agents if a["status"] == "healthy")
    warning_count = sum(1 for a in agents if a["status"] == "warning")
    error_count   = sum(1 for a in agents if a["status"] == "error")

    vfx_rows     = build_vfx_rows(results)
    agent_cards  = build_agent_cards(agents)
    js_data      = json.dumps(results, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI System Dashboard</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #1a1a2e; color: #eee; margin: 0; padding: 24px; }}
    h1, h2 {{ color: #fff; margin-bottom: 4px; }}
    h2 {{ margin-top: 48px; }}
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
    .agent-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; margin-top: 8px; }}
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
    <div class="stat"><div class="stat-value">{count}</div><div class="stat-label">총 평가 수</div></div>
    <div class="stat"><div class="stat-value">{avg}</div><div class="stat-label">평균 점수</div></div>
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
    <tbody>{vfx_rows}</tbody>
  </table>

  <h2>Agent 현황</h2>
  <p class="meta">마지막 점검: {updated_at}</p>
  <div class="stats">
    <div class="stat"><div class="stat-value">{total}</div><div class="stat-label">전체 에이전트</div></div>
    <div class="stat"><div class="stat-value" style="color:#4caf50">{healthy_count}</div><div class="stat-label">정상</div></div>
    <div class="stat"><div class="stat-value" style="color:#ff9800">{warning_count}</div><div class="stat-label">경고</div></div>
    <div class="stat"><div class="stat-value" style="color:#f44336">{error_count}</div><div class="stat-label">오류</div></div>
  </div>
  <div class="agent-grid">{agent_cards}</div>

  <!-- 상세 모달 -->
  <div class="modal-overlay" id="modal" onclick="closeModal(event)">
    <div class="modal">
      <button class="modal-close" onclick="document.getElementById('modal').classList.remove('active')">✕</button>
      <h2 id="modal-title"></h2>
      <div class="score-grid" id="modal-scores"></div>
      <div class="modal-section"><h3>요약</h3><p id="modal-summary"></p></div>
      <div class="modal-section"><h3>강점</h3><div id="modal-strengths"></div></div>
      <div class="modal-section"><h3>문제점</h3><div id="modal-issues"></div></div>
      <div class="modal-section"><h3>개선 액션</h3><div id="modal-actions"></div></div>
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
          return `<div class="score-item"><div class="label">${{label}}</div><div class="value" style="color:${{scoreColors(v)}}">${{v || '-'}}</div></div>`;
        }}).join('') +
        `<div class="score-item"><div class="label">종합점수</div><div class="value" style="color:${{scoreColors(r.overall_score)}};font-size:24px">${{r.overall_score || '-'}}</div></div>`;
      document.getElementById('modal-strengths').innerHTML = (r.strengths || []).map(s => `<span class="tag">✓ ${{s}}</span>`).join('');
      document.getElementById('modal-issues').innerHTML = (r.issues || []).map(s => `<span class="tag">⚠ ${{s}}</span>`).join('');
      document.getElementById('modal-actions').innerHTML = (r.recommended_actions || []).map(s => `<span class="tag">→ ${{s}}</span>`).join('');
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
    results      = load_vfx_results()
    agent_status = load_agent_status()
    html         = generate_html(results, agent_status)
    output       = DOCS_DIR / "index.html"
    output.write_text(html, encoding="utf-8")
    print(f"[dashboard-builder] 완료: {len(results)}개 VFX, {len(agent_status.get('agents', []))}개 에이전트")


if __name__ == "__main__":
    main()
