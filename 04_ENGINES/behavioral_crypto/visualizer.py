#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·行為密碼學可視化器 v2.0
DNA: #龍芯⚡️丙午·甲申·丁酉·丙午·䷳艮-VISUALIZER-V2.0-UID9622
License: MulanPSL v2

ASCII終端渲染 + HTML報告生成
"""

import json
from typing import Dict, List

from .seven_factor_model import FACTOR_DEFINITIONS
from .experiment_runner import ATTACK_LEVELS


class Visualizer:
    """可視化工具箱"""
    
    # ── ASCII 終端渲染 ──
    
    @staticmethod
    def render_radar(factor_scores: Dict[str, float], width: int = 60) -> str:
        """ASCII 七因子雷達圖"""
        factor_order = list(FACTOR_DEFINITIONS.keys())
        names = [FACTOR_DEFINITIONS[f]["name"] for f in factor_order]
        max_name_len = max(len(n) for n in names)
        
        lines = ["┌" + "─" * (width - 2) + "┐"]
        lines.append("│  🎯 七因子行為指紋雷達" + " " * (width - 20) + "│")
        lines.append("├" + "─" * (width - 2) + "┤")
        
        for f_id, name in zip(factor_order, names):
            score = factor_scores.get(f_id, 0)
            bar_len = int(score * (width - max_name_len - 12))
            bar = "█" * bar_len + "░" * max(0, (width - max_name_len - 12) - bar_len)
            icon = FACTOR_DEFINITIONS[f_id]["icon"]
            
            if score > 0.7:
                status = "🟢"
            elif score > 0.3:
                status = "🟡"
            else:
                status = "🔴"
            
            lines.append(f"│ {icon} {name:{max_name_len}s} {status} {bar} {score:.2f} │")
        
        lines.append("└" + "─" * (width - 2) + "┘")
        return "\n".join(lines)
    
    @staticmethod
    def render_comparison(original: Dict, attacked: Dict, attack_level: str) -> str:
        """渲染原始 vs 攻擊後對比"""
        lines = []
        lines.append("═" * 70)
        lines.append(f"  ⚔️ 攻擊等級: {ATTACK_LEVELS[attack_level]['color']} {attack_level} - {ATTACK_LEVELS[attack_level]['name']}")
        lines.append("─" * 70)
        lines.append(f"  {'因子':12s} {'原始':>8s} {'攻擊後':>8s} {'保留率':>8s} {'狀態'}")
        lines.append("─" * 70)
        
        for orig_f, att_f in zip(original.get("factors", []), attacked.get("factors", [])):
            f_id = orig_f["id"]
            orig_score = orig_f["raw"]
            att_score = att_f["raw"]
            retention = att_score / max(orig_score, 0.001)
            retention = min(1.0, retention)
            
            if retention > 0.8:
                status = "🟢 穩固"
            elif retention > 0.4:
                status = "🟡 受損"
            else:
                status = "🔴 崩潰"
            
            lines.append(f"  {FACTOR_DEFINITIONS[f_id]['icon']} {FACTOR_DEFINITIONS[f_id]['name']:8s} {orig_score:8.3f} {att_score:8.3f} {retention:7.1%} {status}")
        
        lines.append("─" * 70)
        lines.append(f"  綜合保留率: {attacked.get('composite_score', 0) / max(original.get('composite_score', 0.001), 0.001):.1%}")
        lines.append("═" * 70)
        return "\n".join(lines)
    
    @staticmethod
    def render_summary(summary: Dict) -> str:
        """渲染實驗總結"""
        lines = []
        lines.append("=" * 70)
        lines.append("  📊 龍魂·行為密碼學實驗報告")
        lines.append("=" * 70)
        lines.append(f"  實驗ID: {summary.get('experiment_id', 'N/A')}")
        lines.append(f"  測試文檔: {summary.get('total_documents', 0)} 篇")
        lines.append(f"  總測試次數: {summary.get('total_results', 0)}")
        lines.append(f"  總體平均保留率: {summary.get('overall_avg_retention', 0):.1%}")
        lines.append("─" * 70)
        
        by_level = summary.get("by_level", {})
        for level in ["L0", "L1", "L2", "L3", "L4"]:
            data = by_level.get(level, {})
            if not data:
                continue
            passed = "✅" if data.get("passed") else "⚠️"
            color = ATTACK_LEVELS[level]["color"]
            lines.append(
                f"  {color} {level} {data.get('name', ''):10s} | "
                f"實測: {data.get('avg_retention', 0):.1%} | "
                f"理論: {data.get('theoretical', 0):.1%} | {passed}"
            )
        
        lines.append("─" * 70)
        lines.append("  🏆 因子抗攻擊排名（平均保留率）:")
        for i, f in enumerate(summary.get("factor_ranking", [])):
            bar = "█" * int(f["avg_retention"] * 25)
            lines.append(f"  {i+1}. {f['icon']} {f['name']:8s} [{bar:25s}] {f['avg_retention']:.1%}")
        
        lines.append("=" * 70)
        return "\n".join(lines)
    
    # ── HTML 報告生成 ──
    
    @staticmethod
    def _html_radar_svg(factor_scores: Dict[str, float], size: int = 300) -> str:
        """生成 SVG 雷達圖"""
        factor_order = list(FACTOR_DEFINITIONS.keys())
        n = len(factor_order)
        cx, cy = size / 2, size / 2
        r = size / 2 - 30
        
        paths = []
        labels = []
        
        for i, f_id in enumerate(factor_order):
            angle = -90 + i * (360 / n)  # 從頂部開始
            rad = angle * 3.14159 / 180
            score = factor_scores.get(f_id, 0)
            
            # 數據點
            x = cx + r * score * math.cos(rad) if 'math' in dir() else cx + r * score * (0.707 if angle == 45 else -0.707 if angle == -45 else 0)
            
            # 標籤位置（在圓外）
            lx = cx + (r + 25) * (0.707 if abs(angle % 90) == 45 else (1 if angle % 360 < 180 else -1) if angle % 180 == 0 else 0)
            ly = cy + (r + 25) * (-1 if angle <= 0 else 1) if angle % 180 == 90 else 0
            
            name = FACTOR_DEFINITIONS[f_id]["name"]
            labels.append(
                f'<text x="{lx}" y="{ly}" text-anchor="middle" '
                f'dominant-baseline="middle" font-size="11" fill="#d4a843">{name}</text>'
            )
        
        return f"""
        <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" class="radar-chart">
          <defs>
            <radialGradient id="radarGrad" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#d4a843" stop-opacity="0.3"/>
              <stop offset="100%" stop-color="#d4a843" stop-opacity="0.05"/>
            </radialGradient>
          </defs>
          <!-- 網格 -->
          {"".join(f'<circle cx="{cx}" cy="{cy}" r="{r * (i+1)/5}" fill="none" stroke="#2a2a3a" stroke-width="0.5"/>' for i in range(5))}
          <!-- 軸 -->
          {"".join(labels)}
        </svg>"""
    
    @staticmethod
    def generate_html_report(summary: Dict, results: List[Dict]) -> str:
        """生成完整 HTML 實驗報告"""
        import math as _math
        global math
        math = _math
        
        by_level = summary.get("by_level", {})
        by_corpus = summary.get("by_corpus", {})
        factor_ranking = summary.get("factor_ranking", [])
        
        # 構建因子平均值用於雷達圖
        factor_avgs = {}
        if factor_ranking:
            factor_avgs = {f["id"]: f["avg_retention"] for f in factor_ranking}
        
        # 生成級別行
        level_rows = ""
        for level in ["L0", "L1", "L2", "L3", "L4"]:
            data = by_level.get(level, {})
            if not data:
                continue
            avg = data.get("avg_retention", 0)
            theo = data.get("theoretical", 0)
            passed = data.get("passed", False)
            color = ATTACK_LEVELS[level]["color"]
            bar_len = int(avg * 200)
            level_rows += f"""
            <tr>
              <td>{color} {level}</td>
              <td>{data.get('name', '')}</td>
              <td>{data.get('sample_count', 0)}</td>
              <td>
                <div class="retention-bar">
                  <div class="retention-fill {'green' if avg > 0.6 else 'yellow' if avg > 0.3 else 'red'}" 
                       style="width:{int(avg * 100)}%"></div>
                </div>
              </td>
              <td class="{'text-green' if avg > 0.6 else 'text-yellow' if avg > 0.3 else 'text-red'}">
                {avg:.1%}
              </td>
              <td>{theo:.1%}</td>
              <td class="{'text-green' if passed else 'text-yellow'}">{'✅ 通過' if passed else '⚠️ 低於預期'}</td>
            </tr>"""
        
        # 生成語料類型行
        corpus_rows = ""
        for corp_type, data in sorted(by_corpus.items()):
            avg = data.get("avg_retention", 0)
            bar_len = int(avg * 200)
            corpus_rows += f"""
            <tr>
              <td>{data.get('icon', '📄')} {data.get('name', corp_type)}</td>
              <td>{data.get('sample_count', 0)}</td>
              <td>
                <div class="retention-bar">
                  <div class="retention-fill {'green' if avg > 0.6 else 'yellow' if avg > 0.3 else 'red'}" 
                       style="width:{int(avg * 100)}%"></div>
                </div>
              </td>
              <td class="{'text-green' if avg > 0.6 else 'text-yellow' if avg > 0.3 else 'text-red'}">
                {avg:.1%}
              </td>
            </tr>"""
        
        # 生成因子排名
        factor_rows = ""
        for i, f in enumerate(factor_ranking):
            avg = f["avg_retention"]
            bar_color = "green" if avg > 0.7 else "yellow" if avg > 0.4 else "red"
            factor_rows += f"""
            <tr>
              <td>{i+1}</td>
              <td>{f['icon']} {f['name']}</td>
              <td>{f['forge_difficulty']:.0%}</td>
              <td>
                <div class="retention-bar">
                  <div class="retention-fill {bar_color}" style="width:{int(avg * 100)}%"></div>
                </div>
              </td>
              <td class="{'text-green' if avg > 0.7 else 'text-yellow' if avg > 0.4 else 'text-red'}">
                {avg:.1%}
              </td>
            </tr>"""
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🐉 龍魂·行為密碼學實驗報告 v2.0</title>
<style>
  :root {{
    --bg-primary: #0a0a14;
    --bg-card: #12122a;
    --bg-card-hover: #1a1a35;
    --text-primary: #e0e0e0;
    --text-secondary: #a0a0b0;
    --gold: #d4a843;
    --gold-light: #e8c96a;
    --gold-dark: #9a7a2a;
    --red: #e74c3c;
    --yellow: #f39c12;
    --green: #2ecc71;
    --blue: #3498db;
    --border: #2a2a3a;
    --radius: 8px;
    --shadow: 0 4px 24px rgba(0,0,0,0.3);
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.6;
    min-height: 100vh;
  }}

  /* ── 背景動畫 ── */
  .bg-grid {{
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
      linear-gradient(rgba(212,168,67,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(212,168,67,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
    z-index: 0;
    pointer-events: none;
  }}

  /* ── 容器 ── */
  .container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    position: relative;
    z-index: 1;
  }}

  /* ── 頭部 ── */
  .header {{
    text-align: center;
    padding: 40px 20px 30px;
    border-bottom: 2px solid var(--gold);
    margin-bottom: 30px;
  }}
  .header h1 {{
    font-size: 2.2em;
    color: var(--gold);
    margin-bottom: 8px;
    text-shadow: 0 0 30px rgba(212,168,67,0.3);
  }}
  .header .subtitle {{
    color: var(--text-secondary);
    font-size: 0.95em;
  }}
  .header .dna-line {{
    font-family: monospace;
    font-size: 0.75em;
    color: var(--gold-dark);
    margin-top: 8px;
    word-break: break-all;
  }}

  /* ── 統計卡片行 ── */
  .stats-row {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 30px;
  }}
  .stat-card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
    text-align: center;
    transition: all 0.3s;
  }}
  .stat-card:hover {{
    background: var(--bg-card-hover);
    border-color: var(--gold);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(212,168,67,0.1);
  }}
  .stat-card .stat-icon {{ font-size: 2em; margin-bottom: 8px; }}
  .stat-card .stat-value {{
    font-size: 2em;
    font-weight: bold;
    color: var(--gold);
  }}
  .stat-card .stat-label {{
    color: var(--text-secondary);
    font-size: 0.85em;
    margin-top: 4px;
  }}

  /* ── 面板 ── */
  .panel {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    margin-bottom: 24px;
    overflow: hidden;
  }}
  .panel-header {{
    padding: 16px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .panel-header h2 {{
    color: var(--gold);
    font-size: 1.2em;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .panel-body {{ padding: 20px; }}

  /* ── 表格 ── */
  table {{
    width: 100%;
    border-collapse: collapse;
  }}
  th, td {{
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid var(--border);
    font-size: 0.9em;
  }}
  th {{
    color: var(--gold);
    font-weight: 600;
    background: rgba(212,168,67,0.05);
    position: sticky;
    top: 0;
  }}
  tr:hover td {{ background: rgba(212,168,67,0.03); }}

  /* ── 保留率條 ── */
  .retention-bar {{
    width: 100%;
    height: 20px;
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    overflow: hidden;
  }}
  .retention-fill {{
    height: 100%;
    border-radius: 10px;
    transition: width 0.6s ease;
    min-width: 2px;
  }}
  .retention-fill.green {{ background: linear-gradient(90deg, #27ae60, var(--green)); }}
  .retention-fill.yellow {{ background: linear-gradient(90deg, #e67e22, var(--yellow)); }}
  .retention-fill.red {{ background: linear-gradient(90deg, #c0392b, var(--red)); }}

  .text-green {{ color: var(--green); font-weight: bold; }}
  .text-yellow {{ color: var(--yellow); font-weight: bold; }}
  .text-red {{ color: var(--red); font-weight: bold; }}

  /* ── 兩欄佈局 ── */
  .two-col {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }}
  @media (max-width: 768px) {{
    .two-col {{ grid-template-columns: 1fr; }}
    .stats-row {{ grid-template-columns: repeat(2, 1fr); }}
  }}

  /* ── 雷達圖容器 ── */
  .radar-container {{
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    min-height: 320px;
  }}
  .radar-chart circle {{ transition: all 0.5s; }}

  /* ── 因子卡網格 ── */
  .factor-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 12px;
  }}
  .factor-card {{
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 16px;
    display: flex;
    align-items: center;
    gap: 14px;
    transition: all 0.3s;
  }}
  .factor-card:hover {{
    border-color: var(--gold);
    background: rgba(212,168,67,0.05);
  }}
  .factor-card .fc-icon {{ font-size: 1.8em; }}
  .factor-card .fc-info {{ flex: 1; }}
  .factor-card .fc-name {{
    font-weight: 600;
    color: var(--gold-light);
    font-size: 0.95em;
  }}
  .factor-card .fc-desc {{
    color: var(--text-secondary);
    font-size: 0.78em;
    margin-top: 4px;
  }}
  .factor-card .fc-score {{
    font-size: 1.3em;
    font-weight: bold;
  }}

  /* ── 頁腳 ── */
  .footer {{
    text-align: center;
    padding: 30px 20px;
    border-top: 1px solid var(--border);
    margin-top: 40px;
    color: var(--text-secondary);
    font-size: 0.8em;
  }}
  .footer .sig {{
    color: var(--gold);
    font-family: monospace;
    font-size: 0.85em;
  }}

  /* ── 狀態指示器 ── */
  .status-dot {{
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 6px;
  }}
  .status-dot.green {{ background: var(--green); box-shadow: 0 0 8px var(--green); }}
  .status-dot.yellow {{ background: var(--yellow); box-shadow: 0 0 8px var(--yellow); }}
  .status-dot.red {{ background: var(--red); box-shadow: 0 0 8px var(--red); }}

  /* ── Badge ── */
  .badge {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 0.75em;
    font-weight: 600;
  }}
  .badge.green {{ background: rgba(46,204,113,0.15); color: var(--green); }}
  .badge.yellow {{ background: rgba(243,156,18,0.15); color: var(--yellow); }}
  .badge.red {{ background: rgba(231,76,60,0.15); color: var(--red); }}
  .badge.gold {{ background: rgba(212,168,67,0.15); color: var(--gold); }}
</style>
</head>
<body>
<div class="bg-grid"></div>

<div class="container">
  <!-- 頭部 -->
  <div class="header">
    <h1>🐉 龍魂·行為密碼學實驗報告</h1>
    <div class="subtitle">七因子來源追溯框架 · 五級攻擊模擬 · 抗偽造能力驗證</div>
    <div class="dna-line">
      DNA: #龍芯⚡️丙午·甲申·丁酉·丙午·䷳艮-BCM-EXPERIMENT-V2.0-UID9622
      <br>確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
      <br>實驗ID: {summary.get('experiment_id', 'N/A')} | 生成時間: {summary.get('experiment_id', '')[:13] or '自動'}
    </div>
  </div>

  <!-- 統計卡片 -->
  <div class="stats-row">
    <div class="stat-card">
      <div class="stat-icon">📊</div>
      <div class="stat-value">{summary.get('total_results', 0)}</div>
      <div class="stat-label">總測試次數</div>
    </div>
    <div class="stat-card">
      <div class="stat-icon">📄</div>
      <div class="stat-value">{summary.get('total_documents', 0)}</div>
      <div class="stat-label">測試文檔</div>
    </div>
    <div class="stat-card">
      <div class="stat-icon">🛡️</div>
      <div class="stat-value">{summary.get('overall_avg_retention', 0):.1%}</div>
      <div class="stat-label">總體保留率</div>
    </div>
    <div class="stat-card">
      <div class="stat-icon">📐</div>
      <div class="stat-value">7</div>
      <div class="stat-label">行為因子</div>
    </div>
    <div class="stat-card">
      <div class="stat-icon">⚔️</div>
      <div class="stat-value">{summary.get('attack_levels', 5)}</div>
      <div class="stat-label">攻擊級別</div>
    </div>
  </div>

  <!-- 攻擊級別結果 -->
  <div class="panel">
    <div class="panel-header">
      <h2><span>⚔️</span> 五級攻擊模擬結果</h2>
      <span class="badge gold">自動化測試</span>
    </div>
    <div class="panel-body">
      <div style="overflow-x: auto;">
        <table>
          <thead>
            <tr>
              <th>級別</th>
              <th>攻擊名稱</th>
              <th>樣本數</th>
              <th>保留率可視化</th>
              <th>實測保留率</th>
              <th>理論值</th>
              <th>判定</th>
            </tr>
          </thead>
          <tbody>{level_rows}
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- 雙欄：因子排名 + 語料分析 -->
  <div class="two-col">
    <!-- 因子抗攻擊排名 -->
    <div class="panel">
      <div class="panel-header">
        <h2><span>🏆</span> 因子抗攻擊排名</h2>
      </div>
      <div class="panel-body">
        <table>
          <thead>
            <tr><th>#</th><th>因子</th><th>偽造難度</th><th>保留率</th><th>實測</th></tr>
          </thead>
          <tbody>{factor_rows}
          </tbody>
        </table>
      </div>
    </div>

    <!-- 語料類型分析 -->
    <div class="panel">
      <div class="panel-header">
        <h2><span>📂</span> 語料類型分析</h2>
      </div>
      <div class="panel-body">
        <table>
          <thead>
            <tr><th>類型</th><th>樣本數</th><th>保留率</th><th>平均</th></tr>
          </thead>
          <tbody>{corpus_rows}
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- 七因子詳情 -->
  <div class="panel">
    <div class="panel-header">
      <h2><span>🔬</span> 七因子行為指紋詳情</h2>
      <span class="badge gold">不可偽造</span>
    </div>
    <div class="panel-body">
      <div class="factor-grid">
""" + "\n".join(f"""
        <div class="factor-card">
          <div class="fc-icon">{FACTOR_DEFINITIONS[f_id]['icon']}</div>
          <div class="fc-info">
            <div class="fc-name">{FACTOR_DEFINITIONS[f_id]['name']} <small style="color:var(--text-secondary)">({FACTOR_DEFINITIONS[f_id]['name_en']})</small></div>
            <div class="fc-desc">{FACTOR_DEFINITIONS[f_id]['description']}</div>
          </div>
          <div class="fc-score text-{"green" if factor_avgs.get(f_id,0) > 0.7 else "yellow" if factor_avgs.get(f_id,0) > 0.4 else "red"}">
            {factor_avgs.get(f_id, 0):.1%}
          </div>
        </div>""" for f_id in FACTOR_DEFINITIONS) + """
      </div>
    </div>
  </div>

  <!-- 主權聲明 -->
  <div class="panel" style="border-color: var(--gold);">
    <div class="panel-header" style="border-color: var(--gold);">
      <h2><span>🏛️</span> 主權驗證與技術規範</h2>
    </div>
    <div class="panel-body">
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px;">
        <div style="background: rgba(212,168,67,0.05); padding: 16px; border-radius: var(--radius);">
          <div style="color: var(--gold); font-weight: bold; margin-bottom: 8px;">🔐 加密標準</div>
          <div style="color: var(--text-secondary); font-size: 0.85em;">
            SM3 國密哈希（內容簽名）<br>
            SM4 國密對稱加密（數據保護）<br>
            SHA3-256（Merkle樹根）<br>
            最低要求: AES-256 / SM4
          </div>
        </div>
        <div style="background: rgba(212,168,67,0.05); padding: 16px; border-radius: var(--radius);">
          <div style="color: var(--gold); font-weight: bold; margin-bottom: 8px;">⚖️ 法律管轄</div>
          <div style="color: var(--text-secondary); font-size: 0.85em;">
            中華人民共和國法律為唯一準繩<br>
            數據不出境·境內存儲處理<br>
            符合《數據安全法》《個人信息保護法》
          </div>
        </div>
        <div style="background: rgba(212,168,67,0.05); padding: 16px; border-radius: var(--radius);">
          <div style="color: var(--gold); font-weight: bold; margin-bottom: 8px;">📜 許可證</div>
          <div style="color: var(--text-secondary); font-size: 0.85em;">
            思想層: CC BY-NC-SA 4.0<br>
            工程層: MulanPSL v2（允許商業使用）<br>
            GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
          </div>
        </div>
        <div style="background: rgba(212,168,67,0.05); padding: 16px; border-radius: var(--radius);">
          <div style="color: var(--gold); font-weight: bold; margin-bottom: 8px;">🛡️ 安全等級</div>
          <div style="color: var(--text-secondary); font-size: 0.85em;">
            等保2.0 三級等效<br>
            數據分級: D1-D4<br>
            熔斷級別: L0-L3<br>
            審計: 🟢🟡🔴 三色標記
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 頁腳 -->
  <div class="footer">
    <div class="sig">
      DNA: #龍芯⚡️丙午·甲申·丁酉·丙午·䷳艮-BCM-V2.0-UID9622
    </div>
    <div>
      創建者: 诸葛鑫 (UID9622) · GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
    </div>
    <div style="margin-top: 8px;">
      工程層 License: MulanPSL v2 · 思想層 License: CC BY-NC-SA 4.0
    </div>
    <div style="margin-top: 4px;">
      中華人民共和國 · 🇨🇳 · 數據主權不可讓渡
    </div>
  </div>
</div>

</body>
</html>"""
        
        return html


# ============================================================
# 命令行入口
# ============================================================
if __name__ == "__main__":
    import sys
    import math
    
    # 演示數據
    demo_scores = {
        "f1_identity_dna": 0.92,
        "f2_time_anchor": 0.88,
        "f3_content_hash": 1.0,
        "f4_style_vector": 0.76,
        "f5_protected_vocab": 0.65,
        "f6_longterm_style": 0.82,
        "f7_error_ledger": 0.91,
    }
    
    viz = Visualizer()
    
    if "--radar" in sys.argv:
        print(viz.render_radar(demo_scores))
    elif "--comparison" in sys.argv:
        orig = {
            "factors": [
                {"id": fid, "raw": demo_scores[fid]} 
                for fid in FACTOR_DEFINITIONS
            ],
            "composite_score": 0.85,
        }
        attacked = {
            "factors": [
                {"id": fid, "raw": demo_scores[fid] * 0.45} 
                for fid in FACTOR_DEFINITIONS
            ],
            "composite_score": 0.38,
        }
        print(viz.render_comparison(orig, attacked, "L3"))
    else:
        print("🐉 龍魂·行為密碼學可視化器 v2.0")
        print(viz.render_radar(demo_scores))
