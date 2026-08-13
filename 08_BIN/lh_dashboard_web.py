#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂系统可视化仪表盘 v1.0
P4 · Web 监控 · 事件流 · 工作流 · 触发器 · 技能生态
DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-DASHBOARD-WEB-v1.0-UID9622
"""

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

HOME = Path.home()
LONGHUN_DIR = Path(os.environ.get("LONGHUN_DATA_DIR", str(HOME / ".longhun")))
PROJECT_DIR = Path(__file__).resolve().parent.parent
WEB_STATIC = PROJECT_DIR / "web" / "static"

BUS_SCRIPT = Path(__file__).resolve().parent / "lh_event_bus.py"
WF_RUN_DIR = LONGHUN_DIR / "workflow_runs"
TRIGGER_DIR = LONGHUN_DIR / "triggers"
TRIGGER_PID = TRIGGER_DIR / "trigger_daemon.pid"
AGENT_PID = LONGHUN_DIR / "agent_orchestrator" / "daemon.pid"
SKILL_INDEX = LONGHUN_DIR / "agent_orchestrator" / "skill_index.json"
TRIGGER_LOG = TRIGGER_DIR / "trigger_log.jsonl"

app = FastAPI(title="龍魂系统仪表盘", version="1.0")


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def load_json(path: Path) -> Any:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_jsonl(path: Path, limit: int = 20) -> List[dict]:
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    items = []
    for line in reversed(lines[-limit:]):
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return items


def is_running(pid_path: Path) -> bool:
    if not pid_path.exists():
        return False
    try:
        pid = int(pid_path.read_text().strip())
        os.kill(pid, 0)
        return True
    except Exception:
        return False


def query_event_bus() -> dict:
    db_path = LONGHUN_DIR / "event_bus" / "event_bus.db"
    if not db_path.exists():
        return {"total": 0, "status": {}, "subscriptions": {}}
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) FROM events GROUP BY status")
        status = dict(cursor.fetchall())
        cursor.execute("SELECT skill, COUNT(*) FROM subscriptions GROUP BY skill")
        subs = dict(cursor.fetchall())
        cursor.execute("SELECT id, topic, event_type, source, payload, status, timestamp FROM events ORDER BY id DESC LIMIT 10")
        recent = [
            {
                "id": r[0], "topic": r[1], "event_type": r[2], "source": r[3],
                "payload": r[4][:120] if r[4] else "", "status": r[5], "timestamp": r[6],
            }
            for r in cursor.fetchall()
        ]
        conn.close()
        return {"total": sum(status.values()), "status": status, "subscriptions": subs, "recent": recent}
    except Exception as e:
        return {"error": str(e)}


def query_workflows(limit: int = 10) -> List[dict]:
    if not WF_RUN_DIR.exists():
        return []
    files = sorted(WF_RUN_DIR.glob("*.json"), reverse=True)[:limit]
    return [load_json(f) for f in files]


def query_triggers() -> List[dict]:
    data = load_json(TRIGGER_DIR / "triggers.json")
    triggers = data.get("triggers", [])
    for t in triggers:
        t["daemon_running"] = False
    return triggers


def query_skill_stats() -> dict:
    index = load_json(SKILL_INDEX)
    skills = index.get("skills", [])
    scope_counts = {}
    for s in skills:
        scope_counts[s.get("scope", "unknown")] = scope_counts.get(s.get("scope", "unknown"), 0) + 1
    return {
        "total": len(skills),
        "scope_counts": scope_counts,
        "generated_at": index.get("generated_at", ""),
    }


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>🐉 龍魂系统仪表盘 v1.0</title>
<link rel="stylesheet" href="{css_url}">
<style>
  :root { --bg:#0d1117; --card:#161b22; --border:#30363d; --text:#c9d1d9; --gold:#d4a373; --green:#238636; --yellow:#f0883e; --red:#da3633; }
  body { margin:0; background:var(--bg); color:var(--text); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif; }
  .header { padding:24px; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center; }
  .header h1 { margin:0; font-size:24px; color:var(--gold); }
  .dna { font-family:monospace; font-size:12px; color:#8b949e; }
  .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:16px; padding:24px; }
  .card { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:16px; }
  .card h2 { margin:0 0 12px; font-size:16px; color:var(--gold); border-bottom:1px solid var(--border); padding-bottom:8px; }
  .metric { display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #21262d; }
  .metric:last-child { border-bottom:none; }
  .status-dot { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; }
  .green { background:var(--green); } .yellow { background:var(--yellow); } .red { background:var(--red); } .gray { background:#6e7681; }
  .payload { font-family:monospace; font-size:11px; color:#8b949e; word-break:break-all; }
  table { width:100%; border-collapse:collapse; font-size:13px; }
  th,td { text-align:left; padding:8px; border-bottom:1px solid #21262d; }
  th { color:var(--gold); }
  .refresh { position:fixed; bottom:24px; right:24px; background:var(--gold); color:#0d1117; border:none; padding:12px 20px; border-radius:24px; cursor:pointer; font-weight:bold; }
</style>
</head>
<body>
  <div class="header">
    <div>
      <h1>🐉 龍魂系统仪表盘 v1.0</h1>
      <div class="dna">#龍芯⚡️丙午·甲申·辛丑·坤卦-DASHBOARD-WEB-v1.0-UID9622</div>
    </div>
    <div id="clock"></div>
  </div>
  <div class="grid">
    <div class="card">
      <h2>📊 事件总线</h2>
      <div id="event-stats"></div>
    </div>
    <div class="card">
      <h2>🔥 最近事件</h2>
      <div id="event-list"></div>
    </div>
    <div class="card">
      <h2>🧬 技能生态</h2>
      <div id="skill-stats"></div>
    </div>
    <div class="card">
      <h2>🔄 工作流运行</h2>
      <div id="workflow-list"></div>
    </div>
    <div class="card">
      <h2>⏰ 触发器状态</h2>
      <div id="trigger-list"></div>
    </div>
    <div class="card">
      <h2>🤖 守护进程</h2>
      <div id="daemon-status"></div>
    </div>
  </div>
  <button class="refresh" onclick="loadAll()">🔄 刷新</button>
  <script>
    async function api(path) { return fetch(path).then(r=>r.json()); }
    function dot(cls) { return `<span class="status-dot ${cls}"></span>`; }
    async function loadAll() {
      const [stats, skills, workflows, triggers, daemons] = await Promise.all([
        api('/api/event-stats'), api('/api/skill-stats'),
        api('/api/workflows'), api('/api/triggers'), api('/api/daemons')
      ]);
      document.getElementById('event-stats').innerHTML = `
        <div class="metric"><span>总事件</span><strong>${stats.total || 0}</strong></div>
        <div class="metric"><span>pending</span><strong>${stats.status?.pending || 0}</strong></div>
        <div class="metric"><span>delivered</span><strong>${stats.status?.delivered || 0}</strong></div>
        <div class="metric"><span>订阅者</span><strong>${Object.keys(stats.subscriptions||{}).join(', ') || '无'}</strong></div>`;
      document.getElementById('event-list').innerHTML = (stats.recent||[]).map(e=>`
        <div class="metric">
          <div>#${e.id} ${e.topic}<br><span class="payload">${e.payload}</span></div>
          <span>${e.status}</span>
        </div>`).join('');
      document.getElementById('skill-stats').innerHTML = `
        <div class="metric"><span>技能总数</span><strong>${skills.total}</strong></div>
        ${Object.entries(skills.scope_counts||{}).map(([k,v])=>`<div class="metric"><span>${k}</span><strong>${v}</strong></div>`).join('')}
        <div class="metric"><span>索引时间</span><span>${skills.generated_at}</span></div>`;
      document.getElementById('workflow-list').innerHTML = workflows.map(w=>`
        <div class="metric">
          <div>${w.workflow} · ${w.run_id}<br><span class="payload">${w.status} · ${(w.steps||[]).length || 0} 步</span></div>
          <span>${w.started_at ? w.started_at.slice(11,16) : '-'}</span>
        </div>`).join('');
      document.getElementById('trigger-list').innerHTML = triggers.map(t=>`
        <div class="metric">
          <div>${t.id} [${t.type}]<br><span class="payload">${t.name}</span></div>
          <span>${t.enabled ? dot('green')+'启用' : dot('gray')+'禁用'}</span>
        </div>`).join('');
      document.getElementById('daemon-status').innerHTML = `
        <div class="metric"><span>Agent 编排器守护</span><span>${daemons.agent_orchestrator ? dot('green')+'运行中' : dot('gray')+'未运行'}</span></div>
        <div class="metric"><span>触发器守护</span><span>${daemons.trigger ? dot('green')+'运行中' : dot('gray')+'未运行'}</span></div>`;
      document.getElementById('clock').innerText = new Date().toLocaleString('zh-CN');
    }
    loadAll();
    setInterval(loadAll, 10000);
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def index():
    css_url = "/static/css/longhun-base.css" if (WEB_STATIC / "css" / "longhun-base.css").exists() else ""
    return HTML_TEMPLATE.replace("{css_url}", css_url)


@app.get("/api/event-stats")
def api_event_stats():
    return query_event_bus()


@app.get("/api/skill-stats")
def api_skill_stats():
    return query_skill_stats()


@app.get("/api/workflows")
def api_workflows(limit: int = 10):
    return query_workflows(limit)


@app.get("/api/triggers")
def api_triggers():
    return query_triggers()


@app.get("/api/daemons")
def api_daemons():
    return {
        "agent_orchestrator": is_running(AGENT_PID),
        "trigger": is_running(TRIGGER_PID),
    }


@app.get("/api/health")
def api_health():
    return {"status": "ok", "time": now_iso()}


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂系统可视化仪表盘 v1.0")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9600)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    if WEB_STATIC.exists():
        app.mount("/static", StaticFiles(directory=str(WEB_STATIC)), name="static")

    print(f"🐉 龍魂仪表盘启动: http://{args.host}:{args.port}")
    uvicorn.run("lh_dashboard_web:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
