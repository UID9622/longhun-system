#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
🐉 龍魂 · 透明看板 v1.0
# 层级: L2_工具层
# DNA: #龍芯⚡️丙午·丙申·丁酉·甲辰·䷼中孚-TRANSPARENT-DASHBOARD-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# License: MulanPSL v2

核心原则: 永远没有黑箱操作，所有关键决策/状态/行为公开可查。
君子协议: 把系统所有关键数据直接暴露给用户，把承诺从口号变成可视化契约。

用法:
    python3 08_BIN/lh_transparent_dashboard.py              # 默认 127.0.0.1:8080
    python3 08_BIN/lh_transparent_dashboard.py --host 0.0.0.0 --port 8080
"""

import json
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "08_BIN"))

DNA = "#龍芯⚡️丙午·丙申·丁酉·甲辰·䷼中孚-TRANSPARENT-DASHBOARD-UID9622"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CST = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(CST).isoformat()


def _read_jsonl(path: Path, limit: int = 100) -> List[Dict[str, Any]]:
    """读取 JSONL 文件，返回最近 limit 条"""
    if not path.exists():
        return []
    entries = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except Exception:
                    continue
    except Exception:
        return []
    return entries[-limit:]


def _read_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _read_sqlite_counts(db_path: Path) -> Dict[str, Any]:
    """读取治理数据库统计"""
    if not db_path.exists():
        return {"available": False, "reason": "数据库不存在"}
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        counts = {}
        for table in ["governance_events", "shame_wall", "honor_wall", "agent_identities", "unauthorized_ai"]:
            try:
                cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
                counts[table] = cursor.fetchone()[0]
            except Exception as e:
                counts[table] = f"error: {e}"

        # 最近事件
        cursor = conn.execute(
            "SELECT timestamp, pain_point, action, actor, tricolor, duration_ms FROM governance_events ORDER BY id DESC LIMIT 50"
        )
        recent_events = [
            {"timestamp": ts, "pain_point": pp, "action": ac, "actor": actor, "tricolor": tc, "duration_ms": dur}
            for ts, pp, ac, actor, tc, dur in cursor
        ]

        # 最近耻辱墙
        cursor = conn.execute(
            "SELECT timestamp, pain_point, actor, reason FROM shame_wall ORDER BY id DESC LIMIT 20"
        )
        recent_shame = [
            {"timestamp": ts, "pain_point": pp, "actor": actor, "reason": reason}
            for ts, pp, actor, reason in cursor
        ]

        # 最近荣誉墙
        cursor = conn.execute(
            "SELECT timestamp, contributor, contribution FROM honor_wall ORDER BY id DESC LIMIT 20"
        )
        recent_honor = [
            {"timestamp": ts, "contributor": c, "contribution": contrib}
            for ts, c, contrib in cursor
        ]

        # 未授权AI
        cursor = conn.execute(
            "SELECT timestamp, tool_name, user, blocked FROM unauthorized_ai ORDER BY id DESC LIMIT 20"
        )
        recent_shadow = [
            {"timestamp": ts, "tool_name": tn, "user": u, "blocked": bool(b)}
            for ts, tn, u, b in cursor
        ]

        # Agent 身份绑定统计
        cursor = conn.execute("SELECT COUNT(*) FROM agent_identities WHERE binding_type='gpg'")
        gpg_bound = cursor.fetchone()[0]
        cursor = conn.execute("SELECT COUNT(*) FROM agent_identities")
        total_agents = cursor.fetchone()[0]

        conn.close()
        return {
            "available": True,
            "counts": counts,
            "recent_events": recent_events,
            "recent_shame": recent_shame,
            "recent_honor": recent_honor,
            "recent_shadow_ai": recent_shadow,
            "agent_bindings": {"total": total_agents, "gpg_bound": gpg_bound},
        }
    except Exception as e:
        return {"available": False, "reason": str(e)}


def collect_data() -> Dict[str, Any]:
    """采集所有可公开数据"""
    home = Path.home()
    longhun_home = home / ".longhun"

    # 治理数据库（如果存在）
    governance_db = PROJECT_ROOT / ".state" / "industry_governance" / "governance.sqlite"
    governance_data = _read_sqlite_counts(governance_db)

    # 史官记录
    historian_entries: List[Dict[str, Any]] = []
    audit_dir = longhun_home / "04_AUDIT"
    if audit_dir.exists():
        for f in sorted(audit_dir.glob("*.jsonl")):
            historian_entries.extend(_read_jsonl(f, limit=1000))
    historian_entries = sorted(
        historian_entries,
        key=lambda x: x.get("timestamp", x.get("ts", "")),
        reverse=True,
    )[:100]

    # 历史耻辱墙（JSONL 格式）
    legacy_shame = _read_jsonl(longhun_home / "08_STATE" / "shame_wall.jsonl", limit=50)

    # 系统状态
    system_state = _read_json(longhun_home / "08_STATE" / "status.json")

    # 知识图谱统计
    kg_data = _read_json(PROJECT_ROOT / "knowledge" / "graph" / "graph.json") or _read_json(
        longhun_home / "knowledge_graph" / "graph.json"
    )
    kg_stats = {"nodes": 0, "edges": 0}
    if kg_data:
        kg_stats = {
            "nodes": len(kg_data.get("nodes", [])),
            "edges": len(kg_data.get("edges", [])),
        }

    return {
        "dna": DNA,
        "timestamp": now_iso(),
        "version": "1.0",
        "governance": governance_data,
        "historian": historian_entries,
        "legacy_shame_wall": legacy_shame,
        "system_state": system_state,
        "knowledge_graph": kg_stats,
        "sources": {
            "governance_db": str(governance_db),
            "historian_dir": str(audit_dir) if audit_dir.exists() else None,
            "legacy_shame": str(longhun_home / "08_STATE" / "shame_wall.jsonl"),
        },
    }


# ============================================================
# Web 服务
# ============================================================

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # 类型检查时使用真实类型；运行时走下方 try/except
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse, JSONResponse
    from uvicorn import run
    HAS_FASTAPI = True
else:
    try:
        from fastapi import FastAPI
        from fastapi.responses import HTMLResponse, JSONResponse
        from uvicorn import run
        HAS_FASTAPI = True
    except Exception:
        HAS_FASTAPI = False

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐉 龍魂 · 透明看板</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: #0a0a14;
            color: #e0e0e0;
            padding: 40px 20px;
            line-height: 1.6;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header {
            border-bottom: 1px solid rgba(212,175,55,0.2);
            padding-bottom: 24px;
            margin-bottom: 40px;
        }
        .header h1 { color: #d4af37; font-size: 32px; margin-bottom: 8px; }
        .header .sub { color: rgba(255,255,255,0.5); font-size: 15px; }
        .header .dna { color: rgba(212,175,55,0.4); font-size: 12px; margin-top: 8px; font-family: monospace; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 12px;
            padding: 20px;
            transition: transform 0.2s;
        }
        .card:hover { transform: translateY(-2px); }
        .card .num { font-size: 36px; font-weight: 700; color: #d4af37; margin-bottom: 4px; }
        .card .label { font-size: 13px; color: rgba(255,255,255,0.4); }
        .section {
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.04);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
        }
        .section h2 { color: #d4af37; font-size: 18px; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
        .entry {
            padding: 10px 12px;
            border-bottom: 1px solid rgba(255,255,255,0.04);
            font-size: 13px;
            color: rgba(255,255,255,0.65);
            font-family: 'SF Mono', monospace;
        }
        .entry:last-child { border-bottom: none; }
        .entry .time { color: rgba(255,255,255,0.3); margin-right: 8px; }
        .entry .green { color: #22c55e; }
        .entry .yellow { color: #f59e0b; }
        .entry .red { color: #ef4444; }
        .empty { color: rgba(255,255,255,0.25); font-style: italic; }
        .footer {
            text-align: center;
            padding-top: 40px;
            border-top: 1px solid rgba(212,175,55,0.08);
            font-size: 12px;
            color: rgba(255,255,255,0.2);
        }
        .refresh {
            background: rgba(212,175,55,0.12);
            border: 1px solid rgba(212,175,55,0.25);
            color: #d4af37;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 16px;
        }
        .refresh:hover { background: rgba(212,175,55,0.22); }
        .badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            margin-left: 8px;
        }
        .badge-green { background: rgba(34,197,94,0.15); color: #22c55e; }
        .badge-yellow { background: rgba(245,158,11,0.15); color: #f59e0b; }
        .badge-red { background: rgba(239,68,68,0.15); color: #ef4444; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐉 龍魂 · 透明看板</h1>
            <div class="sub">永远没有黑箱操作 · 所有关键决策/状态/行为公开可查</div>
            <div class="dna">DNA: #龍芯⚡️丙午·丙申·丁酉·辰时-TRANSPARENT-DASHBOARD-UID9622</div>
        </div>

        <div class="grid" id="stats">
            <div class="card"><div class="num" id="eventCount">-</div><div class="label">📜 治理事件</div></div>
            <div class="card"><div class="num" id="shameCount">-</div><div class="label">🚫 耻辱墙</div></div>
            <div class="card"><div class="num" id="honorCount">-</div><div class="label">🏆 荣誉墙</div></div>
            <div class="card"><div class="num" id="agentCount">-</div><div class="label">🔗 Agent 绑定</div></div>
            <div class="card"><div class="num" id="shadowCount">-</div><div class="label">👤 影子AI检测</div></div>
            <div class="card"><div class="num" id="kgNodes">-</div><div class="label">📚 知识图谱节点</div></div>
        </div>

        <div class="section">
            <h2>📜 最近治理事件</h2>
            <div id="eventList"><div class="empty">加载中...</div></div>
        </div>

        <div class="section">
            <h2>🚫 耻辱墙</h2>
            <div id="shameList"><div class="empty">加载中...</div></div>
        </div>

        <div class="section">
            <h2>🏆 荣誉墙</h2>
            <div id="honorList"><div class="empty">加载中...</div></div>
        </div>

        <div class="section">
            <h2>👤 影子AI / 未授权工具检测</h2>
            <div id="shadowList"><div class="empty">加载中...</div></div>
        </div>

        <div class="section">
            <h2>📜 史官记录</h2>
            <div id="historianList"><div class="empty">加载中...</div></div>
        </div>

        <div class="footer">
            君子协议 · 龍魂系统给世界找回信任的底座协议 · 不容任何变动
            <br>
            <button class="refresh" onclick="loadData()">🔄 刷新数据</button>
        </div>
    </div>

    <script>
        function badge(color) {
            if (color === '🟢') return '<span class="badge badge-green">🟢 通过</span>';
            if (color === '🟡') return '<span class="badge badge-yellow">🟡 警告</span>';
            if (color === '🔴') return '<span class="badge badge-red">🔴 严重</span>';
            return '';
        }

        function loadData() {
            fetch('/api/data')
                .then(r => r.json())
                .then(data => {
                    const gov = data.governance || {};
                    const counts = gov.counts || {};
                    document.getElementById('eventCount').textContent = counts.governance_events ?? '-';
                    document.getElementById('shameCount').textContent = counts.shame_wall ?? '-';
                    document.getElementById('honorCount').textContent = counts.honor_wall ?? '-';
                    document.getElementById('agentCount').textContent = (gov.agent_bindings?.total ?? '-') + '/' + (gov.agent_bindings?.gpg_bound ?? '-');
                    document.getElementById('shadowCount').textContent = counts.unauthorized_ai ?? '-';
                    document.getElementById('kgNodes').textContent = data.knowledge_graph?.nodes ?? '-';

                    const render = (id, items, fn) => {
                        const el = document.getElementById(id);
                        if (!items || items.length === 0) {
                            el.innerHTML = '<div class="empty">暂无记录</div>';
                            return;
                        }
                        el.innerHTML = items.slice(0, 30).map(fn).join('');
                    };

                    render('eventList', gov.recent_events, e =>
                        `<div class="entry"><span class="time">${e.timestamp || ''}</span>[${e.pain_point}] ${e.action} · ${e.actor} ${badge(e.tricolor)} · ${e.duration_ms}ms</div>`
                    );

                    render('shameList', gov.recent_shame, e =>
                        `<div class="entry"><span class="red">🔴</span> <span class="time">${e.timestamp || ''}</span>${e.actor} · ${e.reason} · ${e.pain_point}</div>`
                    );

                    render('honorList', gov.recent_honor, e =>
                        `<div class="entry"><span class="green">🏆</span> <span class="time">${e.timestamp || ''}</span>${e.contributor} · ${e.contribution}</div>`
                    );

                    render('shadowList', gov.recent_shadow_ai, e =>
                        `<div class="entry"><span class="${e.blocked ? 'red' : 'green'}">${e.blocked ? '🔴 已阻断' : '🟢 已放行'}</span> <span class="time">${e.timestamp || ''}</span>${e.tool_name} · ${e.user}</div>`
                    );

                    render('historianList', data.historian, e =>
                        `<div class="entry"><span class="time">${e.timestamp || e.ts || ''}</span>${e.operation || e.action || '未知操作'}</div>`
                    );
                })
                .catch(err => {
                    console.error(err);
                });
        }
        loadData();
        setInterval(loadData, 10000);
    </script>
</body>
</html>
"""


if HAS_FASTAPI:
    app = FastAPI(title="龍魂透明看板", version="1.0")

    @app.get("/", response_class=HTMLResponse)
    def dashboard():
        return HTMLResponse(content=HTML_TEMPLATE)

    @app.get("/api/data")
    def api_data():
        return JSONResponse(content=collect_data())

    @app.get("/api/health")
    def health():
        return {"status": "ok", "dna": DNA, "timestamp": now_iso()}


def cli():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂透明看板")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址 (默认 127.0.0.1，可设为 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8080, help="监听端口")
    args = parser.parse_args()

    if not HAS_FASTAPI:
        print("❌ 需要 fastapi + uvicorn，请安装: pip install fastapi uvicorn")
        sys.exit(1)

    print(f"🐉 透明看板启动: http://{args.host}:{args.port}")
    print(f"   DNA: {DNA}")
    print(f"   君子协议: 永远没有黑箱操作")
    if args.host == "0.0.0.0":
        print("🟡 警告: 当前监听 0.0.0.0，数据对网络内所有设备可见")
    run(app, host=args.host, port=args.port, log_level="warning")


if __name__ == "__main__":
    cli()

# ⛓️ 龍魂DNA接龍链 ──────────────────────────────
# DNA:V1|丙午·丙申·癸亥·辰时·䷗复|P04鲁班|创建|透明看板落地-君子协议可视化契约|bhash:132a221a|chash:bcc11926|←GENESIS
# DNA:V2|丙午·丙申·癸亥·辰时·䷗复|P04鲁班|修改|透明看板+双语路由封装|bhash:7cae84b4|chash:0de3b17d|←bcc11926
# ⛓️ 龍魂DNA接龍末端 ──────────────────────────────
