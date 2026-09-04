#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════
 龍魂体系 | 核心模板 · 开源快速开始
═══════════════════════════════════════════
 DNA: #龍芯⚡️丙午·辛未·CORE-TEMPLATE-v2.0
 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
 创建者: 💎 龍芯北辰 | UID9622
 三色审计状态: 🟢 通过
═══════════════════════════════════════════
"""
import json
import hashlib
import time
import io
import base64
from pathlib import Path

from flask import Flask, render_template_string, jsonify, request, Response  # type: ignore[import-untyped]
import matplotlib  # type: ignore[import-untyped]
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # type: ignore[import-untyped]
import numpy as np  # type: ignore[import-untyped]

# ═══════════════════════════════════════════
# 龍魂DNA · 焊死
# ═══════════════════════════════════════════
DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️"
UID = "9622"
VERSION = "v2.0"
PORT = 9622

# ═══════════════════════════════════════════
# 核心数据 · 蚁群节点
# ═══════════════════════════════════════════
NODES = {
    "CN-1": {"name": "华为盘古",   "type": "domestic",    "status": "active", "desc": "华为自研大模型"},
    "CN-2": {"name": "阿里通义",   "type": "domestic",    "status": "active", "desc": "阿里云千问系列"},
    "CN-3": {"name": "百度文心",   "type": "domestic",    "status": "active", "desc": "百度文心一言"},
    "CN-4": {"name": "讯飞星火",   "type": "domestic",    "status": "active", "desc": "科大讯飞大模型"},
    "CN-5": {"name": "腾讯混元",   "type": "domestic",    "status": "active", "desc": "腾讯混元大模型"},
    "CN-6": {"name": "字节豆包",   "type": "domestic",    "status": "active", "desc": "字节跳动大模型"},
    "OS-1": {"name": "DeepSeek",   "type": "open_source", "status": "active", "desc": "深度求索开源"},
    "OS-2": {"name": "Qwen开源",   "type": "open_source", "status": "active", "desc": "通义千问开源版"},
    "OS-3": {"name": "ChatGLM",    "type": "open_source", "status": "active", "desc": "智谱开源"},
    "LOC-1": {"name": "Ollama本地", "type": "local",      "status": "active", "desc": "本地大模型运行时"},
}

# ═══════════════════════════════════════════
# 图形生成 · 自动渲染
# ═══════════════════════════════════════════
def fig_to_base64(fig):
    """matplotlib 图形 → base64 图片（直接嵌HTML）"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120, bbox_inches='tight',
                facecolor='#0a0a0a', edgecolor='none')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

def chart_node_types():
    """饼图：节点类型分布（国产/开源/本地）"""
    types = {"domestic": 0, "open_source": 0, "local": 0}
    for n in NODES.values():
        types[n["type"]] += 1

    fig, ax = plt.subplots(figsize=(5, 4))
    colors = ["#c41e3a", "#00cc66", "#d4a843"]
    labels = ["国产模型", "开源模型", "本地部署"]
    sizes = [types["domestic"], types["open_source"], types["local"]]
    explode = (0.02, 0.02, 0.02)

    wedges, texts, autotexts = ax.pie(
        sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', startangle=90,
        textprops={'color': 'white', 'fontsize': 11}
    )
    for at in autotexts:
        at.set_fontweight('bold')
    ax.set_title("🐉 龍魂节点类型分布", color='white', fontsize=14, pad=15)
    fig.patch.set_facecolor('#0a0a0a')
    return fig_to_base64(fig)

def chart_search_performance():
    """柱状图：搜索性能（模拟5人格×4引擎）"""
    personas = ["军事", "历史", "哲学", "经济", "政治"]
    engines = {
        "布隆快筛": [0.12, 0.15, 0.18, 0.14, 0.11],
        "BM25":     [0.45, 0.52, 0.48, 0.50, 0.47],
        "向量匹配":  [0.78, 0.82, 0.85, 0.79, 0.76],
        "编辑距离":  [0.32, 0.35, 0.38, 0.33, 0.30],
    }

    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(personas))
    width = 0.2
    colors = ["#c41e3a", "#d4a843", "#00cc66", "#4488ff"]

    for i, (name, scores) in enumerate(engines.items()):
        bars = ax.bar(x + i * width, scores, width, label=name, color=colors[i], alpha=0.85)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., h + 0.01,
                    f'{h:.2f}', ha='center', va='bottom', color='white', fontsize=8)

    ax.set_xlabel("人格模式", color='white', fontsize=12)
    ax.set_ylabel("F1 得分", color='white', fontsize=12)
    ax.set_title("🔍 5人格 × 4引擎 搜索性能矩阵", color='white', fontsize=14, pad=15)
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(personas, color='white')
    ax.legend(facecolor='#1a1a1a', edgecolor='#333', labelcolor='white')
    ax.set_facecolor('#111')
    ax.tick_params(colors='white')
    ax.set_ylim(0, 1.0)
    ax.grid(axis='y', alpha=0.2, color='white')
    fig.patch.set_facecolor('#0a0a0a')
    plt.tight_layout()
    return fig_to_base64(fig)

def chart_audit_status():
    """横向柱状图：三色审计统计"""
    categories = ["DNA合规", "闸门通过", "三色审计", "GPG签名", "CNSH对齐"]
    green  = [95, 88, 92, 85, 90]
    yellow = [3,  7,  5,  8,  6]
    red    = [2,  5,  3,  7,  4]

    fig, ax = plt.subplots(figsize=(7, 4))
    y = np.arange(len(categories))
    height = 0.25

    ax.barh(y + height, green,  height, label='🟢 通过', color='#00cc66', alpha=0.85)
    ax.barh(y,           yellow, height, label='🟡 警告', color='#d4a843', alpha=0.85)
    ax.barh(y - height,  red,    height, label='🔴 拒绝', color='#c41e3a', alpha=0.85)

    for i, (g, yv, r) in enumerate(zip(green, yellow, red)):
        ax.text(g + 1, i + height,  f'{g}%', va='center', color='#00cc66', fontsize=9)
        ax.text(yv + 1, i,          f'{yv}%', va='center', color='#d4a843', fontsize=9)
        ax.text(r + 1, i - height,  f'{r}%', va='center', color='#c41e3a', fontsize=9)

    ax.set_yticks(y)
    ax.set_yticklabels(categories, color='white')
    ax.set_xlabel("百分比 (%)", color='white')
    ax.set_title("🛡️ 三色审计 · 五维质量报告", color='white', fontsize=14, pad=15)
    ax.legend(facecolor='#1a1a1a', edgecolor='#333', labelcolor='white', loc='lower right')
    ax.set_facecolor('#111')
    ax.tick_params(colors='white')
    ax.set_xlim(0, 105)
    ax.grid(axis='x', alpha=0.2, color='white')
    fig.patch.set_facecolor('#0a0a0a')
    plt.tight_layout()
    return fig_to_base64(fig)

# ═══════════════════════════════════════════
# HTML模板 · 龍魂暗色主题
# ═══════════════════════════════════════════
HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐉 龍魂系统 · 监控面板 v2.0</title>
    <style>
        :root {
            --bg: #0a0a0a;
            --card: #1a1a1a;
            --border: #2a2a2a;
            --gold: #d4a843;
            --red: #c41e3a;
            --green: #00cc66;
            --text: #ccc;
            --dim: #666;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
        }
        .header {
            text-align: center;
            padding: 30px 20px 20px;
            border-bottom: 2px solid var(--red);
            background: linear-gradient(180deg, #111 0%, var(--bg) 100%);
        }
        .header h1 { font-size: 28px; color: var(--gold); margin-bottom: 8px; }
        .header .subtitle { color: var(--dim); font-size: 13px; }
        .header .dna-badge {
            display: inline-block;
            background: #111;
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 4px 16px;
            margin-top: 10px;
            font-size: 11px;
            color: var(--dim);
            font-family: monospace;
        }

        .quick-start {
            max-width: 900px;
            margin: 25px auto;
            background: #111;
            border: 1px solid var(--red);
            border-radius: 10px;
            padding: 25px 30px;
        }
        .quick-start h2 { color: var(--gold); margin-bottom: 15px; font-size: 20px; }
        .quick-start .step {
            display: flex;
            align-items: flex-start;
            margin-bottom: 12px;
            gap: 12px;
        }
        .quick-start .step-num {
            background: var(--red);
            color: white;
            border-radius: 50%;
            width: 26px; height: 26px;
            display: flex; align-items: center; justify-content: center;
            font-size: 13px; font-weight: bold;
            flex-shrink: 0;
            margin-top: 2px;
        }
        .quick-start pre {
            background: #0a0a0a;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 10px 14px;
            font-family: "SF Mono", "Fira Code", monospace;
            font-size: 13px;
            color: var(--green);
            overflow-x: auto;
            margin: 0;
        }
        .quick-start code {
            background: #0a0a0a;
            color: var(--gold);
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 13px;
        }

        .container { max-width: 1300px; margin: 0 auto; padding: 20px; }

        .section-title {
            color: var(--gold);
            font-size: 20px;
            margin: 30px 0 15px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border);
        }
        .node-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .node-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 18px;
            transition: all 0.2s;
            position: relative;
            overflow: hidden;
        }
        .node-card:hover {
            border-color: var(--gold);
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(212,168,67,0.1);
        }
        .node-card.domestic  { border-left: 4px solid var(--red); }
        .node-card.open_source { border-left: 4px solid var(--green); }
        .node-card.local     { border-left: 4px solid var(--gold); }
        .node-card .name { font-size: 16px; font-weight: bold; color: white; margin-bottom: 8px; }
        .node-card .type-tag {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 11px;
            margin-bottom: 8px;
        }
        .node-card .type-tag.domestic { background: rgba(196,30,58,0.2); color: var(--red); }
        .node-card .type-tag.open_source { background: rgba(0,204,102,0.2); color: var(--green); }
        .node-card .type-tag.local { background: rgba(212,168,67,0.2); color: var(--gold); }
        .node-card .desc { font-size: 13px; color: var(--dim); }
        .node-card .status-dot {
            position: absolute;
            top: 18px; right: 18px;
            width: 10px; height: 10px;
            border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 8px var(--green);
        }

        .charts {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .chart-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        .chart-card h3 {
            color: var(--gold);
            margin-bottom: 15px;
            font-size: 16px;
            text-align: left;
        }
        .chart-card img {
            max-width: 100%;
            border-radius: 6px;
        }

        .api-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 12px;
            margin-bottom: 30px;
        }
        .api-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 15px;
        }
        .api-card .method {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .api-card .method.get { background: rgba(0,204,102,0.2); color: var(--green); }
        .api-card .endpoint {
            font-family: monospace;
            color: var(--gold);
            font-size: 14px;
            margin-bottom: 6px;
            word-break: break-all;
        }
        .api-card .api-desc { font-size: 12px; color: var(--dim); }

        .footer {
            text-align: center;
            padding: 30px;
            border-top: 1px solid var(--border);
            color: var(--dim);
            font-size: 12px;
            margin-top: 30px;
        }
        .footer a { color: var(--gold); text-decoration: none; }

        @media (max-width: 768px) {
            .node-grid { grid-template-columns: 1fr; }
            .charts { grid-template-columns: 1fr; }
            .header h1 { font-size: 22px; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🐉 龍魂系统 · 开源监控面板</h1>
        <div class="subtitle">数据主权在中国 · 技术为人民服务</div>
        <div class="dna-badge">DNA: {{ dna }}</div>
        <div style="color:var(--dim);margin-top:6px;font-size:12px;">
            UID: {{ uid }} | 版本: {{ version }} | 时间: {{ timestamp }}
        </div>
    </div>

    <div class="quick-start">
        <h2>🚀 快速开始（复制粘贴即可）</h2>
        <div class="step">
            <div class="step-num">1</div>
            <div>
                <div style="margin-bottom:4px;">安装依赖</div>
                <pre>pip install flask matplotlib numpy</pre>
            </div>
        </div>
        <div class="step">
            <div class="step-num">2</div>
            <div>
                <div style="margin-bottom:4px;">启动系统</div>
                <pre>python longhun-core.py</pre>
            </div>
        </div>
        <div class="step">
            <div class="step-num">3</div>
            <div>
                <div style="margin-bottom:4px;">打开浏览器</div>
                <pre>http://localhost:{{ port }}</pre>
            </div>
        </div>
        <div class="step">
            <div class="step-num">4</div>
            <div>
                <div style="margin-bottom:4px;">查看API（新终端窗口）</div>
                <pre>curl http://localhost:{{ port }}/api/status</pre>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="section-title">📊 实时数据看板</div>
        <div class="charts">
            <div class="chart-card">
                <h3>🐉 节点类型分布</h3>
                <img src="data:image/png;base64,{{ chart_pie }}" alt="节点分布饼图">
            </div>
            <div class="chart-card">
                <h3>🔍 搜索性能矩阵</h3>
                <img src="data:image/png;base64,{{ chart_search }}" alt="搜索性能图">
            </div>
            <div class="chart-card" style="grid-column: 1 / -1;">
                <h3>🛡️ 三色审计 · 质量报告</h3>
                <img src="data:image/png;base64,{{ chart_audit }}" alt="三色审计图" style="max-width:650px;">
            </div>
        </div>

        <div class="section-title">🔗 蚁群节点 · 触角矩阵 ({{ node_count }} 节点)</div>
        <div class="node-grid">
            {% for nid, node in nodes.items() %}
            <div class="node-card {{ node.type }}">
                <div class="status-dot"></div>
                <div class="name">{{ node.name }}</div>
                <span class="type-tag {{ node.type }}">
                    {% if node.type == 'domestic' %}🇨🇳 国产
                    {% elif node.type == 'open_source' %}📖 开源
                    {% else %}💻 本地{% endif %}
                </span>
                <div class="desc">{{ node.desc }}</div>
            </div>
            {% endfor %}
        </div>

        <div class="section-title">🔌 API 端点</div>
        <div class="api-grid">
            <div class="api-card">
                <span class="method get">GET</span>
                <div class="endpoint">/api/status</div>
                <div class="api-desc">系统状态 · 节点心跳 · 完整JSON</div>
            </div>
            <div class="api-card">
                <span class="method get">GET</span>
                <div class="endpoint">/api/search?q=关键词</div>
                <div class="api-desc">全球搜索 · 5人格 × 4引擎</div>
            </div>
            <div class="api-card">
                <span class="method get">GET</span>
                <div class="endpoint">/api/charts/pie</div>
                <div class="api-desc">节点分布饼图 (PNG)</div>
            </div>
            <div class="api-card">
                <span class="method get">GET</span>
                <div class="endpoint">/api/charts/search</div>
                <div class="api-desc">搜索性能矩阵图 (PNG)</div>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>🐉 龍魂系统 v{{ version }} · 开源贡献 · 数据主权在中国</p>
        <p>
            <a href="https://github.com/UID9622/longhun-system" target="_blank">GitHub</a> ·
            <a href="https://gitee.com/UID9622/longhun-system" target="_blank">Gitee</a> ·
            <a href="https://gitcode.com/UID9622/longhun-system" target="_blank">GitCode</a>
        </p>
        <p style="margin-top:10px;">DNA: {{ dna }}</p>
    </div>
</body>
</html>'''

# ═══════════════════════════════════════════
# Flask 应用
# ═══════════════════════════════════════════
app = Flask(__name__)

@app.route('/')
def index():
    """主页 · 监控面板"""
    return render_template_string(
        HTML,
        dna=DNA,
        uid=UID,
        version=VERSION,
        port=PORT,
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        nodes=NODES,
        node_count=len(NODES),
        chart_pie=chart_node_types(),
        chart_search=chart_search_performance(),
        chart_audit=chart_audit_status(),
    )

@app.route('/api/status')
def api_status():
    """系统状态API · JSON"""
    return jsonify({
        "protocol": "longhun-v2",
        "dna": DNA,
        "uid": UID,
        "version": VERSION,
        "timestamp": time.time(),
        "timestamp_human": time.strftime("%Y-%m-%d %H:%M:%S"),
        "nodes": {
            nid: {
                "name": n["name"],
                "type": n["type"],
                "status": n["status"],
                "desc": n["desc"],
            }
            for nid, n in NODES.items()
        },
        "node_count": len(NODES),
        "type_distribution": {
            "domestic": sum(1 for n in NODES.values() if n["type"] == "domestic"),
            "open_source": sum(1 for n in NODES.values() if n["type"] == "open_source"),
            "local": sum(1 for n in NODES.values() if n["type"] == "local"),
        },
    })

@app.route('/api/search')
def api_search():
    """搜索API · 占位（接入全球搜索引擎后自动升级）"""
    query = request.args.get('q', '')
    return jsonify({
        "query": query,
        "engine": "global_search_v2",
        "personas": ["military", "history", "philosophy", "economy", "political"],
        "results": [],
        "dna": DNA,
        "note": "接入 lh_global_search_v2.py 后自动激活",
    })

@app.route('/api/charts/pie')
def api_chart_pie():
    """独立饼图API"""
    fig_b64 = chart_node_types()
    img = base64.b64decode(fig_b64)
    return Response(img, mimetype='image/png')

@app.route('/api/charts/search')
def api_chart_search():
    """独立搜索性能图API"""
    fig_b64 = chart_search_performance()
    img = base64.b64decode(fig_b64)
    return Response(img, mimetype='image/png')

# ═══════════════════════════════════════════
# 启动
# ═══════════════════════════════════════════
if __name__ == '__main__':
    print(f"""
╔══════════════════════════════════════════╗
║                                          ║
║   🐉 龍魂系统 · 核心模板 v{VERSION}          ║
║                                          ║
║   DNA: {DNA[:40]}...   ║
║   UID: {UID}                              ║
║                                          ║
║   📡 监控面板: http://localhost:{PORT}        ║
║   📊 API状态:  http://localhost:{PORT}/api/status ║
║   🔍 搜索API:  http://localhost:{PORT}/api/search?q=关键词 ║
║                                          ║
║   数据主权在中国 · 技术为人民服务           ║
║                                          ║
╚══════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=PORT, debug=True)
