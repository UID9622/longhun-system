#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三维可视化仪表盘生成器（中国古典青铜风格）
把 telemetry.db 里的运行痕迹、路由决策、多维评分渲染成可交互 HTML。
DNA: #龍芯⚡️2026-06-27-UID9622-DASHBOARD-v2.0
"""
import base64
import importlib.util
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .config import load_config, workspace_root
from .telemetry import _db_path


def _load_visual_engine():
    """动态加载龍魂视觉生成引擎，不破坏 core 包结构。"""
    root = workspace_root()
    visual_path = root / "backend_personas" / "baobao" / "visual_engine" / "generator.py"
    spec = importlib.util.spec_from_file_location("longhun_visual_engine", str(visual_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DIMENSIONS = ["health", "completion", "stability", "efficiency", "sovereignty"]
DIM_LABELS = {
    "health": "健康度",
    "completion": "完成度",
    "stability": "稳定性",
    "efficiency": "效率",
    "sovereignty": "主权合规",
}

# 青铜主题色板
PALETTE = {
    "ink_black": "#0a0908",       # 玄黑底
    "bronze_dark": "#1c1512",     # 青铜深褐
    "bronze": "#b87333",          # 青铜
    "bronze_glow": "#d4a055",     # 铜光
    "gold": "#f0c674",            # 金镶
    "jade": "#3c8d7d",            # 玉绿
    "cinnabar": "#c23a30",        # 朱砂
    "vermilion": "#e85d4f",       # 朱红亮
    "stone": "#8c8378",           # 石刻灰
    "text": "#f5f0e6",            # 宣纸白
    "grid": "#4a3b2a",            # 暗纹
}


def _generate_visual_assets(assets_dir: Path) -> Dict[str, Path]:
    """调用龍魂视觉生成引擎生成仪表盘专属纹样与印章。"""
    assets_dir.mkdir(parents=True, exist_ok=True)
    visual = _load_visual_engine()
    p = PALETTE
    files = {
        "meander_pattern.svg": visual.meander_svg(400, 400, stroke=p["bronze"], bg=p["ink_black"]),
        "dragon_seal.svg": visual.dragon_seal_svg(120, stroke=p["gold"], bg=p["ink_black"]),
        "bagua_ring.svg": visual.bagua_ring_svg(160, stroke=p["bronze"], bg=p["ink_black"]),
        "pan_chi.svg": visual.pan_chi_svg(200, stroke=p["gold"], bg=p["ink_black"]),
        "dragon_scale.svg": visual.dragon_scale_svg(200, 200, stroke=p["bronze"], bg=p["ink_black"]),
        "particle_totem.svg": visual.particle_totem_svg(200, stroke=p["gold"], bg=p["ink_black"]),
    }
    for name, svg in files.items():
        (assets_dir / name).write_text(svg, encoding="utf-8")
    (assets_dir / "palette.json").write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
    return {k: assets_dir / k for k in files}


def _pattern_svg_data(assets_dir: Path) -> str:
    """云雷纹（回纹）背景图案，使用视觉引擎生成的 SVG 做 base64 data URI。"""
    svg_path = assets_dir / "meander_pattern.svg"
    if not svg_path.exists():
        _generate_visual_assets(assets_dir)
    svg = svg_path.read_text(encoding="utf-8")
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"url('data:image/svg+xml;base64,{b64}')"


def _inline_svg(svg_path: Path) -> str:
    """读取 SVG 文件并返回内联 <svg>...</svg> 字符串。"""
    svg = svg_path.read_text(encoding="utf-8")
    m = re.search(r"(<svg\b[^>]*>.*</svg>)", svg, re.DOTALL)
    return m.group(1) if m else svg


def _seal_svg(assets_dir: Path) -> str:
    """顶部龙纹印章装饰 SVG（龍魂视觉生成引擎参数方程龙纹）。"""
    svg_path = assets_dir / "dragon_seal.svg"
    if not svg_path.exists():
        _generate_visual_assets(assets_dir)
    return _inline_svg(svg_path)


def _load_routes(limit: int = 100) -> List[Dict[str, Any]]:
    db = _db_path()
    if not db.exists():
        return []
    conn = sqlite3.connect(str(db), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM routes ORDER BY timestamp DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def _latest_scores_by_persona(runs: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """取每个人格最近一次运行的评分。"""
    latest = {}
    for r in runs:
        code = r.get("persona_code")
        if code in latest:
            continue
        scores = r.get("scores") or {}
        if not scores:
            continue
        latest[code] = {
            "name": r.get("persona_name", code),
            "started_at": r.get("started_at"),
            "overall": scores.get("overall", 0),
            "scores": scores,
            "status": r.get("status"),
        }
    return latest


def _build_3d_data(latest: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    x, y, z, text, colors = [], [], [], [], []
    color_map = {
        "success": PALETTE["jade"],
        "error": PALETTE["cinnabar"],
        "partial": PALETTE["gold"],
        "running": PALETTE["bronze_glow"],
    }
    for code, info in latest.items():
        for dim in DIMENSIONS:
            x.append(code)
            y.append(DIM_LABELS.get(dim, dim))
            score = info["scores"].get(dim, 0)
            z.append(score)
            text.append(f"{info['name']}<br>{DIM_LABELS.get(dim, dim)}: {score}")
            colors.append(color_map.get(info["status"], PALETTE["stone"]))
    return {"x": x, "y": y, "z": z, "text": text, "colors": colors}


def generate_html(output_path: Path = None) -> Path:
    from .telemetry import get_runs, get_summary

    cfg = load_config()
    if output_path is None:
        output_path = Path(cfg.get("data_dir", workspace_root() / "data")) / "dashboard" / "uid9622_dashboard.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary = get_summary()
    runs = get_runs(limit=300)
    routes = _load_routes(limit=60)
    latest = _latest_scores_by_persona(runs)
    plot_data = _build_3d_data(latest)

    total = summary.get("total_runs", 0)
    status_counts = summary.get("status_counts", {})
    success = status_counts.get("success", 0)
    error = status_counts.get("error", 0)
    success_rate = round(success / total * 100, 1) if total else 0.0
    top_route = (summary.get("top_routes") or [{"target_name": "无", "c": 0}])[0]

    recent_rows = []
    for r in summary.get("recent_runs", [])[:20]:
        scores = r.get("scores") or {}
        recent_rows.append({
            "timestamp": r.get("started_at", "")[:19].replace("T", " "),
            "persona": r.get("persona_code", ""),
            "status": r.get("status", ""),
            "duration_ms": r.get("duration_ms", 0),
            "overall": scores.get("overall", "-"),
        })

    route_rows = []
    for rt in routes[:20]:
        route_rows.append({
            "timestamp": rt.get("timestamp", "")[:19].replace("T", " "),
            "source": "ROUTER",
            "target_type": rt.get("target_type", ""),
            "target": rt.get("target_name", rt.get("target_code", "")),
            "score": rt.get("score", 0),
            "query": rt.get("query", "")[:60],
        })

    p = PALETTE
    assets_dir = output_path.parent / "assets"
    _generate_visual_assets(assets_dir)
    pattern = _pattern_svg_data(assets_dir)
    seal = _seal_svg(assets_dir)
    bagua_path = assets_dir / "bagua_ring.svg"
    pan_chi = _inline_svg(assets_dir / "pan_chi.svg")
    dragon_scale = _inline_svg(assets_dir / "dragon_scale.svg")
    particle_totem = _inline_svg(assets_dir / "particle_totem.svg")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>龙魂系统 · UID9622 专属运行与路由三维仪表盘</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
  :root {{
    --ink: {p['ink_black']};
    --bronze-dark: {p['bronze_dark']};
    --bronze: {p['bronze']};
    --bronze-glow: {p['bronze_glow']};
    --gold: {p['gold']};
    --jade: {p['jade']};
    --cinnabar: {p['cinnabar']};
    --vermilion: {p['vermilion']};
    --stone: {p['stone']};
    --text: {p['text']};
  }}
  body {{
    margin: 0;
    font-family: "STSong", "SimSun", "Noto Serif SC", "Songti SC", serif;
    background-color: var(--ink);
    background-image: {pattern};
    background-size: 200px 200px;
    color: var(--text);
  }}
  .container {{ max-width: 1480px; margin: 0 auto; padding: 28px; }}
  .banner {{
    text-align: center;
    padding: 18px 12px 10px;
    background: linear-gradient(180deg, rgba(184,115,51,0.18) 0%, rgba(10,9,8,0) 100%);
    border-bottom: 2px solid var(--bronze);
    margin-bottom: 24px;
  }}
  .banner svg {{ max-width: 220px; height: auto; margin-bottom: 8px; }}
  .banner .bagua-ring {{ width: 42px; height: 42px; vertical-align: middle; margin: 0 10px; opacity: 0.85; }}
  h1 {{
    margin: 0;
    font-size: 30px;
    letter-spacing: 4px;
    color: var(--gold);
    text-shadow: 0 0 10px rgba(240,198,116,0.25);
  }}
  .subtitle {{
    color: var(--stone);
    font-size: 13px;
    margin-top: 8px;
    letter-spacing: 1px;
  }}
  .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 18px; margin-bottom: 26px; }}
  .card {{
    background: rgba(28,21,18,0.82);
    border: 1px solid var(--bronze);
    border-radius: 6px;
    padding: 18px 16px;
    box-shadow: 0 0 14px rgba(184,115,51,0.18), inset 0 0 0 1px rgba(240,198,116,0.08);
  }}
  .card .label {{ font-size: 12px; color: var(--stone); text-transform: uppercase; letter-spacing: 1px; }}
  .card .value {{ font-size: 34px; font-weight: 700; margin-top: 8px; color: var(--text); }}
  .bronze {{ color: var(--bronze-glow) !important; }}
  .gold {{ color: var(--gold) !important; }}
  .jade {{ color: var(--jade) !important; }}
  .cinnabar {{ color: var(--cinnabar) !important; }}
  .section {{
    background: rgba(28,21,18,0.78);
    border: 1px solid rgba(184,115,51,0.55);
    border-radius: 8px;
    padding: 22px;
    margin-bottom: 26px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
  }}
  .section h2 {{
    margin: 0 0 16px;
    font-size: 20px;
    color: var(--gold);
    border-left: 4px solid var(--cinnabar);
    padding-left: 12px;
    letter-spacing: 2px;
  }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid rgba(184,115,51,0.3); }}
  th {{ color: var(--bronze-glow); font-weight: 600; }}
  tr:hover {{ background: rgba(184,115,51,0.08); }}
  .badge {{ display: inline-block; padding: 3px 9px; border-radius: 3px; font-size: 11px; font-weight: 600; }}
  .badge-success {{ background: rgba(60,141,125,0.18); color: var(--jade); border: 1px solid var(--jade); }}
  .badge-error {{ background: rgba(194,58,48,0.15); color: var(--vermilion); border: 1px solid var(--cinnabar); }}
  .badge-running {{ background: rgba(212,160,85,0.15); color: var(--gold); border: 1px solid var(--gold); }}
  footer {{ text-align: center; color: var(--stone); font-size: 12px; padding: 18px 0 8px; letter-spacing: 1px; }}
  .seal {{ display: inline-block; border: 1px solid var(--cinnabar); color: var(--cinnabar); padding: 2px 8px; border-radius: 2px; margin-left: 8px; }}
  .gallery {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 18px; }}
  .gallery-item {{ text-align: center; }}
  .gallery-item svg {{ width: 160px; height: 160px; border: 1px solid var(--bronze); border-radius: 6px; background: rgba(10,9,8,0.6); padding: 8px; box-shadow: 0 0 12px rgba(184,115,51,0.15); }}
  .gallery-item .label {{ margin-top: 8px; font-size: 12px; color: var(--stone); letter-spacing: 1px; }}
</style>
</head>
<body>
<div class="container">
  <div class="banner">
    {seal}
    <h1>🐉 龙魂系统 · UID9622 专属运行与路由三维仪表盘</h1>
    <div class="subtitle">
      青铜为骨 · 金镶为脉 · 玄黑为底 · 朱砂为印
      {_inline_svg(bagua_path)}
      呼叫宝宝，启动龙魂
      <span class="seal">DNA #龍芯⚡️2026-06-27-LONGHUN-SYSTEM-DASHBOARD-v2.0</span>
    </div>
    <div class="subtitle">生成时间: {datetime.now(timezone.utc).isoformat()}</div>
  </div>

  <div class="cards">
    <div class="card"><div class="label">总运行次数</div><div class="value bronze">{total}</div></div>
    <div class="card"><div class="label">成功率</div><div class="value {'jade' if success_rate >= 80 else 'gold' if success_rate >= 50 else 'cinnabar'}">{success_rate}%</div></div>
    <div class="card"><div class="label">活跃人格</div><div class="value gold">{len(latest)}</div></div>
    <div class="card"><div class="label">错误次数</div><div class="value {'cinnabar' if error else 'jade'}">{error}</div></div>
    <div class="card"><div class="label">最热路由目标</div><div class="value" style="font-size:17px; color: var(--gold);">{top_route.get('target_name','无')} ({top_route.get('c',0)})</div></div>
  </div>

  <div class="section">
    <h2>🧊 三维评分视图（人格 × 维度 × 分数）</h2>
    <div id="chart3d" style="width:100%; height:560px;"></div>
  </div>

  <div class="section">
    <h2>📋 最近运行记录</h2>
    <table>
      <tr><th>时间</th><th>人格</th><th>状态</th><th>耗时(ms)</th><th>综合评分</th></tr>
      {''.join(f"<tr><td>{r['timestamp']}</td><td>{r['persona']}</td><td><span class='badge badge-{'success' if r['status']=='success' else 'error' if r['status']=='error' else 'running'}'>{r['status']}</span></td><td>{r['duration_ms']}</td><td>{r['overall']}</td></tr>" for r in recent_rows)}
    </table>
  </div>

  <div class="section">
    <h2>🔗 最近路由决策痕迹</h2>
    <table>
      <tr><th>时间</th><th>目标类型</th><th>目标</th><th>匹配分</th><th>原始请求</th></tr>
      {''.join(f"<tr><td>{r['timestamp']}</td><td>{r['target_type']}</td><td>{r['target']}</td><td>{r['score']}</td><td>{r['query']}</td></tr>" for r in route_rows)}
    </table>
  </div>

  <div class="section">
    <h2>🎨 龍魂视觉资产（纯代码生成）</h2>
    <div class="gallery">
      <div class="gallery-item">{seal}<div class="label">龙纹印章</div></div>
      <div class="gallery-item">{_inline_svg(bagua_path)}<div class="label">八卦环</div></div>
      <div class="gallery-item">{pan_chi}<div class="label">蟠螭纹</div></div>
      <div class="gallery-item">{dragon_scale}<div class="label">龙鳞纹</div></div>
      <div class="gallery-item">{particle_totem}<div class="label">粒子图腾</div></div>
    </div>
  </div>

  <footer>
    🐉 龙魂系统 · UID9622 专属 · 数据根留本地 · 决策全程留痕 · 呼叫宝宝，启动龙魂
  </footer>
</div>

<script>
  var data = [{{
    type: 'scatter3d',
    mode: 'markers',
    x: {json.dumps(plot_data['x'], ensure_ascii=False)},
    y: {json.dumps(plot_data['y'], ensure_ascii=False)},
    z: {json.dumps(plot_data['z'], ensure_ascii=False)},
    text: {json.dumps(plot_data['text'], ensure_ascii=False)},
    marker: {{
      size: 11,
      color: {json.dumps(plot_data['colors'])},
      opacity: 0.9,
      line: {{ color: '#1c1512', width: 1 }}
    }},
    hovertemplate: '%%{{text}}<extra></extra>'
  }}];
  var layout = {{
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: {{ family: 'STSong, SimSun, Noto Serif SC, serif', color: '#f5f0e6' }},
    scene: {{
      xaxis: {{ title: '人格', backgroundcolor: '#1c1512', gridcolor: '#4a3b2a', tickfont: {{color:'#f5f0e6'}} }},
      yaxis: {{ title: '评估维度', backgroundcolor: '#1c1512', gridcolor: '#4a3b2a', tickfont: {{color:'#f5f0e6'}} }},
      zaxis: {{ title: '分数', backgroundcolor: '#1c1512', gridcolor: '#4a3b2a', range: [0, 100], tickfont: {{color:'#f5f0e6'}} }},
      camera: {{ eye: {{ x: 1.6, y: 1.6, z: 1.0 }} }}
    }},
    margin: {{ l: 0, r: 0, b: 0, t: 0 }}
  }};
  Plotly.newPlot('chart3d', data, layout, {{responsive: true}});
</script>
</body>
</html>"""
    output_path.write_text(html, encoding="utf-8")
    return output_path


def print_summary():
    from .telemetry import get_runs, get_summary
    summary = get_summary()
    print("\n# UID9622 运行汇总\n")
    print(f"总运行次数: {summary['total_runs']}")
    print(f"状态分布: {summary['status_counts']}")
    print(f"人格分布: {summary['persona_counts']}")
    print("\n最近运行:")
    for r in summary["recent_runs"][:10]:
        scores = r.get("scores") or {}
        print(f"  - {r['started_at'][:19]} | {r['persona_code']:<10} | {r['status']:<7} | overall={scores.get('overall','-'):<6} | duration={r['duration_ms']}ms")
