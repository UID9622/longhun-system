#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-PUBLIC-CONSOLE-v1.0-a3b7f1c9
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 公开操作台 v1.0
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-PUBLIC-CONSOLE-v1.0-a3b7f1c9

设计原则:
  - 所有人可见：无需登录即可查看系统状态/操作历史
  - 所有操作留痕：任何修改（人工或AI）都生成DNA签名，写入审计链
  - AI可操作：AI代理自动执行任务，记录"谁做了什么事"
  - 实时数据：直接从审计链和状态库读取，无缓存

用法:
  lh console start              # 启动公开控制台服务 (port 8778)
  lh console status             # 查看当前公开状态
  lh console operate --action set --key x --value y   # 执行可审计操作
  lh console log                # 查看最新审计日志
  curl http://localhost:8778/api/state    # API: 获取状态
  curl http://localhost:8778/api/audit    # API: 审计日志
  open http://localhost:8778              # 浏览器: 公开面板
"""

import os
import sys
import json
import time
import hashlib
import sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from contextlib import contextmanager

# 北京时区
CST = timezone(timedelta(hours=8))

def cst_now() -> str:
    return datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S CST")

def cst_iso() -> str:
    return datetime.now(CST).isoformat()

# ============================================================
# 配置
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
AUDIT_DB = DATA_DIR / "public_audit.db"
STATE_FILE = DATA_DIR / "public_state.json"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
DNA_SALT = "龍魂⚡️UID9622"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# 检查依赖
_HAS_FASTAPI = False
try:
    from fastapi import FastAPI, HTTPException, Request, Query
    from fastapi.responses import JSONResponse, HTMLResponse
    import uvicorn
    _HAS_FASTAPI = True
except ImportError:
    pass

# ============================================================
# DNA生成器
# ============================================================

# 干支表（用于DNA生成）
_TIANGAN = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
_DIZHI = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

def _current_ganzhi() -> str:
    """生成当前日期的干支四柱"""
    now = datetime.now(CST)
    # 简化：用当前日期计算日干支
    base = datetime(2026, 2, 14, tzinfo=CST)  # 丙午年春节
    days = (now - base).days
    gz_idx = days % 60
    yg = _TIANGAN[gz_idx % 10]
    yd = _DIZHI[gz_idx % 12]
    # 时柱（简化：取小时对应地支）
    h = now.hour
    hz_idx = (h + 1) // 2 % 12
    hg = _TIANGAN[(gz_idx % 10 + hz_idx) % 10]
    hd = _DIZHI[hz_idx]
    return f"{yg}{yd}"

_GZ_CACHE = _current_ganzhi()

def generate_dna(prefix: str = "OP") -> str:
    """生成操作DNA追溯码"""
    ts = datetime.now(CST).strftime("%Y%m%d%H%M%S%f")
    unique = hashlib.md5(f"{ts}{DNA_SALT}{time.time()}".encode()).hexdigest()[:8]
    return f"#龍芯⚡️{_GZ_CACHE}-{prefix}-{unique}"

# ============================================================
# 审计链存储 (SQLite)
# ============================================================

@contextmanager
def get_db():
    conn = sqlite3.connect(str(AUDIT_DB))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                actor TEXT NOT NULL DEFAULT 'unknown',
                action TEXT NOT NULL,
                target TEXT DEFAULT '',
                data TEXT DEFAULT '{}',
                dna TEXT NOT NULL,
                signature TEXT DEFAULT '',
                result TEXT DEFAULT ''
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS state (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL,
                updated_by TEXT NOT NULL DEFAULT 'system',
                dna TEXT NOT NULL DEFAULT ''
            )
        ''')
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit(timestamp DESC)
        ''')
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit(actor)
        ''')
        conn.commit()

init_db()

# ============================================================
# 审计日志
# ============================================================

def log_audit(actor: str, action: str, target: str = "",
              data: Dict = None, dna: str = None, result: str = "") -> Dict:
    """写入审计日志"""
    if dna is None:
        dna = generate_dna(action.upper())
    timestamp = cst_iso()
    data_str = json.dumps(data or {}, ensure_ascii=False)
    with get_db() as conn:
        conn.execute(
            "INSERT INTO audit (timestamp, actor, action, target, data, dna, result) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (timestamp, actor, action, target, data_str, dna, result)
        )
        conn.commit()
    return {
        "timestamp": timestamp,
        "actor": actor,
        "action": action,
        "target": target,
        "data": data,
        "dna": dna,
        "result": result
    }

def get_latest_audit(limit: int = 50, actor: str = None,
                     action: str = None) -> List[Dict]:
    """获取最新审计日志"""
    query = "SELECT * FROM audit"
    params = []
    conditions = []
    if actor:
        conditions.append("actor = ?")
        params.append(actor)
    if action:
        conditions.append("action = ?")
        params.append(action)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    with get_db() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]

def get_audit_stats() -> Dict:
    """审计统计"""
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM audit").fetchone()[0]
        by_actor = {}
        for row in conn.execute(
            "SELECT actor, COUNT(*) as cnt FROM audit GROUP BY actor ORDER BY cnt DESC LIMIT 10"
        ).fetchall():
            by_actor[row["actor"]] = row["cnt"]
        by_action = {}
        for row in conn.execute(
            "SELECT action, COUNT(*) as cnt FROM audit GROUP BY action ORDER BY cnt DESC LIMIT 10"
        ).fetchall():
            by_action[row["action"]] = row["cnt"]
    return {"total_operations": total, "top_actors": by_actor, "top_actions": by_action}

# ============================================================
# 状态管理
# ============================================================

def set_state(key: str, value: str, actor: str = "system") -> Dict:
    """设置系统状态（自动记录审计）"""
    dna = generate_dna("STATE")
    with get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO state (key, value, updated_at, updated_by, dna) VALUES (?, ?, ?, ?, ?)",
            (key, value, cst_now(), actor, dna)
        )
        conn.commit()
    log_audit(actor=actor, action="set_state", target=key,
              data={"value": value}, dna=dna, result="ok")
    return {"key": key, "value": value, "dna": dna}

def get_state(key: str = None) -> Dict:
    """获取状态"""
    with get_db() as conn:
        if key:
            row = conn.execute("SELECT * FROM state WHERE key = ?", (key,)).fetchone()
            if row:
                return {
                    "key": row["key"],
                    "value": json.loads(row["value"]) if row["value"].startswith("{") else row["value"],
                    "updated_at": row["updated_at"],
                    "updated_by": row["updated_by"],
                    "dna": row["dna"]
                }
            return {}
        rows = conn.execute("SELECT * FROM state ORDER BY key").fetchall()
        result = {}
        for row in rows:
            try:
                result[row["key"]] = json.loads(row["value"]) if row["value"].startswith("{") else row["value"]
            except (json.JSONDecodeError, AttributeError):
                result[row["key"]] = row["value"]
        return result

def delete_state(key: str, actor: str = "system") -> Dict:
    """冻结状态（不物理删除，标记为frozen）"""
    dna = generate_dna("FREEZE")
    val = get_state(key)
    if not val:
        return {"error": f"Key '{key}' not found"}
    set_state(f"_frozen_{key}", json.dumps(val), actor)
    with get_db() as conn:
        conn.execute("DELETE FROM state WHERE key = ?", (key,))
        conn.commit()
    log_audit(actor=actor, action="freeze_state", target=key,
              data={"frozen_value": val}, dna=dna, result="frozen")
    return {"status": "frozen", "key": key, "dna": dna}

# ============================================================
# 系统健康（无需fastapi）
# ============================================================

def get_system_health() -> Dict:
    """系统基础健康信息"""
    import subprocess
    info = {
        "timestamp": cst_iso(),
        "hostname": os.uname().nodename,
        "python": sys.version.split()[0],
        "audit_db": str(AUDIT_DB),
        "audit_db_exists": AUDIT_DB.exists(),
    }
    # 磁盘
    try:
        import shutil
        usage = shutil.disk_usage(str(ROOT))
        info["disk"] = {"total_gb": round(usage.total / 1073741824, 1),
                        "used_gb": round(usage.used / 1073741824, 1),
                        "free_gb": round(usage.free / 1073741824, 1),
                        "percent": round(usage.used / usage.total * 100, 1)}
    except Exception:
        pass
    # OLLAMA
    try:
        import urllib.request
        req = urllib.request.Request("http://localhost:11434/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=3) as resp:
            info["ollama"] = "online"
    except Exception:
        info["ollama"] = "offline"
    return info


# ============================================================
# FastAPI 应用（仅在有fastapi时加载）
# ============================================================

if _HAS_FASTAPI:
    app = FastAPI(
        title="龍魂 · 公开操作台",
        description="透明可审计的公开控制面板，所有操作留痕·DNA可追溯",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url=None,
    )

    @app.get("/api/health")
    async def api_health():
        """健康检查"""
        return {
            "status": "ok",
            "service": "longhun-public-console",
            "version": "1.0.0",
            "timestamp": cst_iso(),
            "dna": generate_dna("HEALTH")
        }

    @app.get("/api/state")
    async def api_get_state():
        """获取当前所有公开状态"""
        return {
            "state": get_state(),
            "timestamp": cst_iso(),
            "dna": generate_dna("STATE")
        }

    @app.get("/api/state/{key}")
    async def api_get_state_key(key: str):
        """获取指定状态值"""
        val = get_state(key)
        if not val:
            raise HTTPException(status_code=404, detail=f"Key '{key}' not found")
        return val

    @app.get("/api/audit")
    async def api_get_audit(
        limit: int = Query(50, ge=1, le=500),
        actor: str = Query(None),
        action: str = Query(None)
    ):
        """获取最新审计日志"""
        logs = get_latest_audit(limit=limit, actor=actor, action=action)
        return {
            "logs": logs,
            "count": len(logs),
            "stats": get_audit_stats(),
            "timestamp": cst_iso()
        }

    @app.get("/api/system")
    async def api_system():
        """系统健康信息"""
        return get_system_health()

    # ---- 操作API ----
    from pydantic import BaseModel

    class OperationRequest(BaseModel):
        action: str = ""
        target: str = ""
        data: Dict = {}
        actor: str = "anonymous"

    @app.post("/api/operate")
    async def api_operate(req: OperationRequest):
        """执行可审计操作（带DNA留痕）"""
        dna = generate_dna(req.action.upper() if req.action else "OP")
        result_text = "recorded"

        if req.action == "set_state":
            value = req.data.get("value", req.data.get("val", ""))
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            set_result = set_state(req.target, str(value), req.actor)
            result_text = "ok"
        elif req.action == "freeze_state":
            del_result = delete_state(req.target, req.actor)
            result_text = "frozen"
        elif req.action == "log":
            # 纯日志操作，不改变状态
            result_text = "logged"
        else:
            result_text = "recorded"

        log = log_audit(
            actor=req.actor,
            action=req.action,
            target=req.target,
            data=req.data,
            dna=dna,
            result=result_text
        )
        return {"status": result_text, "operation": log}

    # ---- 公开 HTML 面板 ----
    @app.get("/", response_class=HTMLResponse)
    async def public_dashboard():
        return _DASHBOARD_HTML


# ============================================================
# 内嵌仪表盘 HTML
# ============================================================

_DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🐉 龍魂 · 公开操作台</title>
<style>
:root {
  --bg: #0a0a0f; --card-bg: #12121a; --border: #1e1e2e;
  --text: #c9d1d9; --title: #f0f6fc; --gold: #ffd60a;
  --green: #2ea043; --blue: #1f6feb; --red: #da3633; --orange: #d29922;
  --dna: #e6b422;
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: -apple-system, "PingFang SC", "Noto Sans SC", sans-serif;
  background: var(--bg); color: var(--text); min-height: 100vh;
  padding: 20px 24px;
}
.header {
  text-align: center; margin-bottom: 28px;
  padding-bottom: 16px; border-bottom: 1px solid var(--border);
}
.header h1 { color: var(--gold); font-size: 1.6em; }
.header p { color: #8b949e; font-size: 0.85em; margin-top: 4px; }
.grid { display: flex; gap: 20px; flex-wrap: wrap; }
.grid > div { flex: 1; min-width: 340px; }
.card {
  background: var(--card-bg); border-radius: 10px;
  border: 1px solid var(--border); padding: 18px; margin-bottom: 16px;
}
.card h2 { color: var(--title); font-size: 1.05em; margin-bottom: 12px; }
.state-item { display: flex; justify-content: space-between; align-items: center;
  padding: 8px 0; border-bottom: 1px solid rgba(48,54,61,0.4); font-size: 0.88em; }
.state-item:last-child { border-bottom: none; }
.state-key { color: var(--blue); font-weight: 600; min-width: 120px; }
.state-val { color: var(--gold); text-align: right; word-break: break-all; }
.log-entry { padding: 8px 0; border-bottom: 1px solid rgba(48,54,61,0.4); font-size: 0.82em; }
.log-entry:last-child { border-bottom: none; }
.badge { display: inline-block; padding: 1px 8px; border-radius: 10px; font-size: 0.75em; margin-right: 4px; }
.badge-op { background: var(--green); color: #fff; }
.badge-state { background: var(--blue); color: #fff; }
.badge-ai { background: var(--orange); color: #fff; }
.badge-freeze { background: var(--red); color: #fff; }
.dna-text { color: var(--dna); font-family: "SF Mono","Fira Code",monospace; font-size: 0.82em; }
.time-text { color: #8b949e; font-size: 0.78em; }
.actions { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }
.actions input {
  padding: 6px 10px; border-radius: 6px; border: 1px solid var(--border);
  background: var(--bg); color: var(--text); font-size: 0.82em; outline: none;
}
.actions input:focus { border-color: var(--blue); }
.actions button {
  padding: 6px 14px; border-radius: 6px; border: none; cursor: pointer;
  font-size: 0.82em; font-weight: 600; transition: opacity 0.15s;
}
.actions button:hover { opacity: 0.85; }
.btn-log { background: var(--blue); color: #fff; }
.btn-state { background: var(--green); color: #fff; }
.btn-freeze { background: var(--red); color: #fff; }
.btn-refresh { background: #30363d; color: var(--text); }
.stats-grid { display: flex; gap: 12px; margin-bottom: 12px; }
.stat-box { flex: 1; text-align: center; padding: 10px; background: var(--bg);
  border-radius: 8px; border: 1px solid var(--border); }
.stat-num { font-size: 1.4em; font-weight: 700; color: var(--gold); }
.stat-label { font-size: 0.75em; color: #8b949e; margin-top: 2px; }
.footer { text-align: center; margin-top: 16px; font-size: 0.75em; color: #484f58; }
pre { background: var(--bg); padding: 10px; border-radius: 6px; overflow-x: auto;
  font-size: 0.8em; border: 1px solid var(--border); }
</style>
</head>
<body>
<div class="header">
  <h1>🐉 龍魂 · 公开操作台</h1>
  <p>所有人可见 · 所有操作留痕 · AI操作带DNA追溯</p>
</div>
<div class="grid">
  <div>
    <div class="card">
      <h2>📊 系统状态</h2>
      <div id="state">加载中…</div>
    </div>
    <div class="card">
      <h2>⚡ 执行操作</h2>
      <div class="actions">
        <input id="actorIn" placeholder="操作者" value="public" style="width:100px;">
        <input id="targetIn" placeholder="目标key" style="width:140px;">
        <input id="valueIn" placeholder="值" style="width:160px;">
      </div>
      <div class="actions" style="margin-top:6px;">
        <button class="btn-state" onclick="doOp('set_state')">set_state</button>
        <button class="btn-freeze" onclick="doOp('freeze_state')">freeze</button>
        <button class="btn-log" onclick="doOp('log')">仅记录</button>
        <span id="opResult" style="font-size:0.82em;color:var(--orange);"></span>
      </div>
    </div>
  </div>
  <div>
    <div class="card">
      <h2>📋 审计统计</h2>
      <div id="stats"><div class="stats-grid"><div class="stat-box"><div class="stat-num">—</div><div class="stat-label">总操作</div></div></div></div>
    </div>
    <div class="card">
      <h2>📋 最新操作 <button class="btn-refresh" onclick="fetchData()" style="float:right;padding:2px 10px;font-size:0.75em;">刷新</button></h2>
      <div id="logs">加载中…</div>
      <div style="margin-top:8px;">
        <button class="btn-refresh" onclick="filterLogs('AI')" style="font-size:0.75em;margin-right:4px;">只看AI</button>
        <button class="btn-refresh" onclick="filterLogs('')" style="font-size:0.75em;">全部</button>
      </div>
    </div>
  </div>
</div>
<div id="jsonView" style="display:none;margin-top:12px;">
  <div class="card"><h2>📄 详情</h2><pre id="jsonContent" style="max-height:300px;"></pre></div>
</div>
<div class="footer">
  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
  龍魂系统 · UID9622 · 2026 |
  <a href="/api/docs" style="color:var(--blue);">API文档</a> |
  <a href="/api/state" style="color:var(--blue);">状态JSON</a> |
  <a href="/api/audit" style="color:var(--blue);">审计JSON</a>
</div>
<script>
let currentFilter = '';
async function fetchData() {
  try {
    const s = await (await fetch('/api/state')).json();
    const keys = Object.entries(s.state||{});
    document.getElementById('state').innerHTML = keys.length
      ? keys.map(([k,v]) => `<div class="state-item"><span class="state-key">${k}</span><span class="state-val">${typeof v==='string'?v:JSON.stringify(v)}</span></div>`).join('')
      : '<div style="color:#8b949e;font-size:0.85em;">暂无公开状态</div>';

    const url = currentFilter ? `/api/audit?limit=20&actor=${currentFilter}` : '/api/audit?limit=20';
    const a = await (await fetch(url)).json();
    document.getElementById('stats').innerHTML =
      `<div class="stats-grid"><div class="stat-box"><div class="stat-num">${a.stats?.total_operations||0}</div><div class="stat-label">总操作</div></div><div class="stat-box"><div class="stat-num">${a.count||0}</div><div class="stat-label">本次展示</div></div></div>`;
    document.getElementById('logs').innerHTML = (a.logs||[]).map(l => {
      let badge = 'badge-op';
      if (l.action.includes('state')) badge = 'badge-state';
      if (l.actor==='AI') badge = 'badge-ai';
      if (l.action.includes('freeze')) badge = 'badge-freeze';
      return `<div class="log-entry" style="cursor:pointer" onclick="showDetail('${l.dna}')"><span class="badge ${badge}">${l.action}</span> <b>${l.actor}</b> → ${l.target||'—'} <span class="dna-text">${l.dna}</span> <span class="time-text">${new Date(l.timestamp).toLocaleString('zh-CN')}</span></div>`;
    }).join('') || '<div style="color:#8b949e;font-size:0.85em;">暂无审计记录</div>';
  } catch(e) { console.error(e); }
}
function showDetail(dna) {
  fetch('/api/audit?limit=200').then(r => r.json()).then(a => {
    const entry = (a.logs||[]).find(l => l.dna===dna);
    if (entry) {
      document.getElementById('jsonContent').textContent = JSON.stringify(entry,null,2);
      document.getElementById('jsonView').style.display = 'block';
    }
  });
}
function filterLogs(actor) { currentFilter = actor; fetchData(); }
async function doOp(action) {
  const actor = document.getElementById('actorIn').value||'public';
  const target = document.getElementById('targetIn').value;
  const raw = document.getElementById('valueIn').value;
  let data = {};
  if (raw) {
    try { data = {value: JSON.parse(raw)}; } catch(e) { data = {value: raw}; }
  }
  const res = await fetch('/api/operate', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({action, target, data, actor})
  });
  const r = await res.json();
  document.getElementById('opResult').textContent = r.status + ' ' + (r.operation?.dna||'');
  setTimeout(fetchData, 300);
}
fetchData(); setInterval(fetchData, 10000);
</script>
</body>
</html>"""


# ============================================================
# 启动服务
# ============================================================

def start_server(host: str = "0.0.0.0", port: int = 8778):
    """启动公开操作台服务"""
    if not _HAS_FASTAPI:
        print("❌ 需要安装 fastapi uvicorn: pip install fastapi uvicorn")
        sys.exit(1)

    log_audit(actor="system", action="console_start", target=f"{host}:{port}")

    print(f"""
🐉 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  龍魂 · 公开操作台 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  地址:     http://{host}:{port}
  状态API:  /api/state
  审计API:  /api/audit
  操作API:  /api/operate (POST)
  系统API:  /api/system
  面板:     /
  API文档:  /api/docs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  确认码:   {CONFIRM_CODE}
  DNA:      {generate_dna("START")}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    uvicorn.run(app, host=host, port=port, log_level="info")


# ============================================================
# CLI
# ============================================================

def print_state():
    """CLI: 打印当前状态"""
    state = get_state()
    if not state:
        print("📊 暂无公开状态")
        return
    print("📊 当前状态:")
    for k, v in state.items():
        print(f"  {k}: {v}")

def print_audit(limit: int = 20):
    """CLI: 打印审计日志"""
    logs = get_latest_audit(limit)
    if not logs:
        print("📋 暂无审计日志")
        return
    print(f"📋 最新 {len(logs)} 条审计日志:")
    for log in logs:
        print(f"  [{log['timestamp'][:19]}] {log['actor']:10s} | {log['action']:15s} | {log['target'] or '-':20s} | DNA:{log['dna']}")

def do_operate(action: str, target: str, value: str, actor: str = "cli"):
    """CLI: 执行操作"""
    data = {}
    if value:
        try:
            data = {"value": json.loads(value)}
        except json.JSONDecodeError:
            data = {"value": value}
    result = log_audit(actor=actor, action=action, target=target, data=data)
    if action == "set_state":
        set_state(target, value, actor)
        print(f"✅ state.{target} = {value}")
    print(f"DNA: {result['dna']}")


def main():
    import argparse
    ap = argparse.ArgumentParser(description="龍魂公开操作台 v1.0")
    ap.add_argument("action", nargs="?", default="start", choices=["start","status","log","operate"],
                    help="start=启动服务 / status=查看状态 / log=查看日志 / operate=执行操作")
    ap.add_argument("--host", default="0.0.0.0", help="监听地址")
    ap.add_argument("--port", type=int, default=8778, help="监听端口")
    ap.add_argument("--limit", type=int, default=30, help="日志条数 (log)")
    ap.add_argument("--op", "--action", dest="op_action", default=None, help="操作动作 (operate)")
    ap.add_argument("--key", "--target", dest="target", default="", help="目标key (operate)")
    ap.add_argument("--value", dest="value", default="", help="值 (operate)")
    ap.add_argument("--actor", default="cli", help="操作者标识")
    args = ap.parse_args()

    if args.action == "status":
        print_state()
        return
    if args.action == "log":
        print_audit(args.limit)
        return
    if args.action == "operate":
        if not args.op_action:
            print("❌ 需要 --op 参数 (set_state/freeze_state/log)")
            return
        do_operate(args.op_action, args.target, args.value, args.actor)
        return
    # 默认：启动服务
    start_server(args.host, args.port)


if __name__ == "__main__":
    main()
