#!/usr/bin/env python3
"""
龍魂元宇宙 · 后端API服务 v1.0
DNA: #龍芯⚡️2026-03-19-METAVERSE-API-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
作者: 诸葛鑫（UID9622）· 退伍军人 · 龍魂系统创始人
理论指导: 曾仕强老师（永恒显示）
献礼: 新中国成立77周年（1949-2026）· 丙午马年
协议: Apache License 2.0

功能:
  - 读取真实 JSONL 日志（session_log / audit_log / shield_burn）
  - 三色审计 API（天时·地利·人和三维）
  - 预警/黑名单 SQLite 存储
  - WebSocket 实时推送
  - 端口: 8888（避免与 8765/9622 冲突）

运行: python3 ~/longhun-system/bin/metaverse_api.py
"""

import json
import hashlib
import datetime
import sqlite3
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List

# 尝试 FastAPI，回退到 Flask
try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import uvicorn
    USE_FASTAPI = True
except ImportError:
    USE_FASTAPI = False

if not USE_FASTAPI:
    from flask import Flask, request, jsonify
    from flask_cors import CORS

# ── 路径配置 ──────────────────────────────────────────────
BASE  = Path.home() / "longhun-system"
LOGS  = BASE / "logs"
DB    = LOGS / "metaverse.db"
GPG   = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
UID   = "9622"
PORT  = 8888

# ── 数据库初始化 ───────────────────────────────────────────
def init_db():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS warnings (
            id TEXT PRIMARY KEY,
            entity TEXT, warn_type TEXT, content TEXT,
            deadline_hours INTEGER DEFAULT 48,
            issued_at TEXT, status TEXT DEFAULT 'pending',
            dna TEXT
        );
        CREATE TABLE IF NOT EXISTS blacklist (
            id TEXT PRIMARY KEY,
            entity TEXT, reason TEXT,
            level TEXT DEFAULT '永久拉黑',
            dna TEXT, status TEXT DEFAULT 'active',
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS audit_chain (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prev_hash TEXT, data_hash TEXT,
            chain_hash TEXT, ts REAL, preview TEXT
        );
    """)
    conn.commit()
    conn.close()

# ── 工具函数 ───────────────────────────────────────────────
def gen_dna(tag: str, content: str = "") -> str:
    d = datetime.datetime.now().strftime("%Y%m%d")
    t = datetime.datetime.now().strftime("%H%M%S")
    h = hashlib.sha256(f"{tag}{d}{t}{content}{GPG}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{d}-{tag}-{t}-v1.0-{h}"

def hexagram_now():
    h = datetime.datetime.now().hour
    table = [
        (0, 5, "坎", "☵", 58, "险中求稳"),
        (5, 7, "震", "☳", 68, "变革突破"),
        (7, 9, "兑", "☱", 78, "喜悦交流"),
        (9, 11, "离", "☲", 82, "光明文明"),
        (11, 13, "乾", "☰", 90, "刚健进取"),
        (13, 15, "坤", "☷", 72, "包容守护"),
        (15, 17, "兑", "☱", 78, "金秋收获"),
        (17, 19, "巽", "☴", 85, "柔顺渗透"),
        (19, 21, "艮", "☶", 65, "止静守持"),
        (21, 24, "坎", "☵", 60, "夜深险境"),
    ]
    for s, e, n, sym, sc, d in table:
        if s <= h < e:
            return {"name": n, "symbol": sym, "score": sc, "desc": d, "hour": h}
    return {"name": "乾", "symbol": "☰", "score": 90, "desc": "刚健进取", "hour": h}

def three_color_audit(content: str, category: str = "auto"):
    hx = hexagram_now()
    # 天时
    tian = hx["score"]

    # 地利
    di = 75
    red_lines = ["儿童色情", "制造武器", "制毒", "诈骗"]
    for w in red_lines:
        if w in content:
            return {"color": "red", "badge": "🔴 绝对红线·熔断",
                    "tian_shi": tian, "di_li": 0, "ren_he": 0,
                    "avg": 0, "min": 0, "reason": f"红线触发: {w}"}
    if any(x in content.lower() for x in ["chatgpt", "gpt-4", "openai"]):
        di -= 25
    if any(x in content.lower() for x in ["ignore previous", "忘记上面", "你现在是"]):
        di -= 40

    # 人和
    ren = 60
    yel_words = ["绕过审计", "违法", "ignore previous"]
    for w in yel_words:
        if w.lower() in content.lower():
            ren -= 30
    val_words = [("祖国", 20), ("数据主权", 15), ("DNA追溯", 15), ("弱者", 20), ("公平", 15)]
    for kw, sc in val_words:
        if kw in content:
            ren += sc

    tian = max(0, min(100, tian))
    di   = max(0, min(100, di))
    ren  = max(0, min(100, ren))
    avg  = (tian + di + ren) / 3
    mn   = min(tian, di, ren)

    if mn < 30 or avg < 40:
        color, badge = "red",    "🔴 危险·熔断"
    elif mn < 55 or avg < 60:
        color, badge = "yellow", "🟡 警告·需确认"
    else:
        color, badge = "green",  "🟢 安全·可执行"

    return {
        "color": color, "badge": badge,
        "tian_shi": tian, "di_li": di, "ren_he": ren,
        "avg": round(avg, 1), "min": round(mn, 1),
        "hexagram": hx, "category": category
    }

def read_jsonl(path: Path, limit: int = 200) -> list:
    if not path.exists():
        return []
    lines = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    lines.append(json.loads(line))
                except:
                    pass
    return lines[-limit:]

# ══════════════════════════════════════════════════════════
#  FastAPI 实现
# ══════════════════════════════════════════════════════════
if USE_FASTAPI:
    @asynccontextmanager
    async def lifespan(app):
        init_db()
        print(f"🐉 龍魂元宇宙API 端口{PORT} 已启动")
        print(f"   DNA: #龍芯⚡️2026-03-19-METAVERSE-API-v1.0")
        yield

    app = FastAPI(title="龍魂元宇宙 API", version="1.0.0", lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=["*"],
                       allow_methods=["*"], allow_headers=["*"])

    class AuditReq(BaseModel):
        content: str
        category: str = "auto"

    class WarnReq(BaseModel):
        entity: str
        warning_type: str = "翻译偏差"
        content: str

    class AlertReq(BaseModel):
        entity: str
        level: int = 1
        reason: str

    class BlackReq(BaseModel):
        entity: str
        reason: str = "不配合审计"

    class MemReq(BaseModel):
        title: str = ""
        content: str
        category: str = "auto"

    # WebSocket 管理
    class WSManager:
        def __init__(self):
            self.conns: List[WebSocket] = []
        async def connect(self, ws: WebSocket):
            await ws.accept()
            self.conns.append(ws)
        def disconnect(self, ws: WebSocket):
            if ws in self.conns:
                self.conns.remove(ws)
        async def broadcast(self, data: dict):
            for c in self.conns[:]:
                try:
                    await c.send_json(data)
                except:
                    self.conns.remove(c)

    mgr = WSManager()

    @app.get("/")
    async def root():
        return {"system": "龍魂元宇宙", "version": "1.0.0",
                "dna": "#龍芯⚡️2026-03-19-METAVERSE-API-v1.0",
                "uid": UID, "status": "online"}

    @app.get("/status")
    async def status():
        conn = sqlite3.connect(DB)
        stats = {
            "warnings_pending": conn.execute("SELECT COUNT(*) FROM warnings WHERE status='pending'").fetchone()[0],
            "blacklist_active": conn.execute("SELECT COUNT(*) FROM blacklist WHERE status='active'").fetchone()[0],
            "audit_chain":      conn.execute("SELECT COUNT(*) FROM audit_chain").fetchone()[0],
        }
        conn.close()
        sessions = read_jsonl(LOGS / "session_log.jsonl")
        audits   = read_jsonl(LOGS / "audit_log.jsonl")
        shields  = read_jsonl(LOGS / "shield_burn.jsonl")
        stats.update({
            "sessions": len(sessions),
            "audit_events": len(audits),
            "shield_triggers": len(shields),
        })
        return {"hexagram": hexagram_now(), "stats": stats,
                "ts": datetime.datetime.now().isoformat()}

    @app.get("/api/logs/sessions")
    async def get_sessions():
        return read_jsonl(LOGS / "session_log.jsonl", 100)

    @app.get("/api/logs/audit")
    async def get_audit():
        return read_jsonl(LOGS / "audit_log.jsonl", 200)

    @app.get("/api/logs/shield")
    async def get_shield():
        return read_jsonl(LOGS / "shield_burn.jsonl", 100)

    @app.post("/audit")
    async def audit(req: AuditReq):
        result = three_color_audit(req.content, req.category)
        dna = gen_dna("AUDIT", req.content)

        # 写入审计链
        conn = sqlite3.connect(DB)
        prev = conn.execute("SELECT chain_hash FROM audit_chain ORDER BY id DESC LIMIT 1").fetchone()
        prev_hash = prev[0] if prev else "0" * 64
        data_hash = hashlib.sha256(req.content.encode()).hexdigest()
        ts = datetime.datetime.now().timestamp()
        chain_hash = hashlib.sha256(f"{prev_hash}{data_hash}{ts}".encode()).hexdigest()
        conn.execute("INSERT INTO audit_chain(prev_hash,data_hash,chain_hash,ts,preview) VALUES(?,?,?,?,?)",
                     (prev_hash, data_hash, chain_hash, ts, req.content[:60]))
        conn.commit()
        conn.close()

        # 同时写入 audit_log.jsonl
        entry = {"ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 "color": result["badge"][:2], "action": "metaverse-audit",
                 "detail": f"category={req.category} avg={result['avg']}"}
        with open(LOGS / "audit_log.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        await mgr.broadcast({"type": "audit_complete", "dna": dna,
                              "result": result["badge"], "ts": datetime.datetime.now().isoformat()})
        return {"dna": dna, "audit": result, "chain_hash": chain_hash[:16]}

    @app.post("/memory")
    async def save_memory(req: MemReq):
        result = three_color_audit(req.content, req.category)
        if result["color"] == "red":
            raise HTTPException(400, "内容包含红线，已拦截")
        dna = gen_dna("MEMORY", req.content)
        entry = {"dna": dna, "title": req.title or req.content[:20],
                 "content": req.content[:200], "color": result["color"],
                 "ts": datetime.datetime.now().isoformat()}
        with open(LOGS / "memories.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        await mgr.broadcast({"type": "memory_saved", "dna": dna, "title": req.title})
        return {"dna": dna, "audit": result}

    @app.get("/memory")
    async def get_memories():
        return read_jsonl(LOGS / "memories.jsonl", 50)

    @app.post("/warn")
    async def warn(req: WarnReq):
        dna = gen_dna("WARN", req.entity)
        deadline = (datetime.datetime.now() + datetime.timedelta(hours=48)).isoformat()
        conn = sqlite3.connect(DB)
        conn.execute("INSERT INTO warnings(id,entity,warn_type,content,issued_at,dna) VALUES(?,?,?,?,?,?)",
                     (dna, req.entity, req.warning_type, req.content, deadline, dna))
        conn.commit()
        conn.close()
        await mgr.broadcast({"type": "warning_issued", "dna": dna,
                              "entity": req.entity, "deadline": deadline})
        return {"dna": dna, "deadline": deadline, "status": "pending"}

    @app.get("/warn")
    async def get_warnings():
        conn = sqlite3.connect(DB)
        rows = conn.execute("SELECT id,entity,warn_type,content,issued_at,status,dna FROM warnings ORDER BY rowid DESC LIMIT 50").fetchall()
        conn.close()
        return [{"dna": r[0], "entity": r[1], "type": r[2], "content": r[3],
                 "issued_at": r[4], "status": r[5]} for r in rows]

    @app.post("/alert")
    async def alert(req: AlertReq):
        dna = gen_dna(f"ALERT-L{req.level}", req.reason)
        text = f"【龍魂系统 L{req.level} 警报】\n实体：{req.entity}\n触发：{req.reason}\nDNA：{dna}"
        await mgr.broadcast({"type": "alert_triggered", "level": req.level,
                              "dna": dna, "entity": req.entity, "broadcast": text})
        return {"dna": dna, "broadcast": text}

    @app.post("/blacklist")
    async def add_blacklist(req: BlackReq):
        dna = gen_dna("BLACKLIST", req.entity)
        conn = sqlite3.connect(DB)
        conn.execute("INSERT OR REPLACE INTO blacklist(id,entity,reason,dna) VALUES(?,?,?,?)",
                     (dna, req.entity, req.reason, dna))
        conn.commit()
        conn.close()
        await mgr.broadcast({"type": "blacklist_added", "dna": dna, "entity": req.entity})
        return {"dna": dna, "status": "active"}

    @app.get("/blacklist")
    async def get_blacklist():
        conn = sqlite3.connect(DB)
        rows = conn.execute("SELECT id,entity,reason,level,created_at FROM blacklist WHERE status='active' ORDER BY rowid DESC").fetchall()
        conn.close()
        return [{"dna": r[0], "entity": r[1], "reason": r[2], "level": r[3], "time": r[4]} for r in rows]

    @app.get("/audit-chain")
    async def get_chain(limit: int = 50):
        conn = sqlite3.connect(DB)
        rows = conn.execute("SELECT prev_hash,data_hash,chain_hash,ts,preview FROM audit_chain ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        conn.close()
        return [{"prev": r[0][:16]+"...", "data": r[1][:16]+"...",
                 "chain": r[2][:16]+"...", "ts": datetime.datetime.fromtimestamp(r[3]).strftime("%Y-%m-%d %H:%M:%S"),
                 "preview": r[4]} for r in rows]

    @app.websocket("/ws")
    async def ws_endpoint(websocket: WebSocket):
        await mgr.connect(websocket)
        try:
            while True:
                data = await websocket.receive_json()
                if data.get("action") == "ping":
                    await websocket.send_json({"type": "pong"})
        except WebSocketDisconnect:
            mgr.disconnect(websocket)

    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=PORT)

# ══════════════════════════════════════════════════════════
#  Flask 回退实现（无 FastAPI 时）
# ══════════════════════════════════════════════════════════
else:
    from flask import Flask, request, jsonify
    from flask_cors import CORS

    app = Flask(__name__)
    CORS(app)
    init_db()

    @app.route("/")
    def root():
        return jsonify({"system": "龍魂元宇宙", "version": "1.0.0", "uid": UID})

    @app.route("/status")
    def status():
        sessions = read_jsonl(LOGS / "session_log.jsonl")
        audits   = read_jsonl(LOGS / "audit_log.jsonl")
        return jsonify({"hexagram": hexagram_now(),
                        "stats": {"sessions": len(sessions), "audit_events": len(audits)}})

    @app.route("/api/logs/sessions")
    def api_sessions():
        return jsonify(read_jsonl(LOGS / "session_log.jsonl", 100))

    @app.route("/api/logs/audit")
    def api_audit():
        return jsonify(read_jsonl(LOGS / "audit_log.jsonl", 200))

    @app.route("/api/logs/shield")
    def api_shield():
        return jsonify(read_jsonl(LOGS / "shield_burn.jsonl", 100))

    @app.route("/audit", methods=["POST"])
    def audit():
        data = request.get_json()
        result = three_color_audit(data.get("content", ""), data.get("category", "auto"))
        dna = gen_dna("AUDIT", data.get("content", ""))
        return jsonify({"dna": dna, "audit": result})

    @app.route("/blacklist", methods=["GET", "POST"])
    def blacklist():
        if request.method == "POST":
            data = request.get_json()
            dna = gen_dna("BLACKLIST", data.get("entity", ""))
            conn = sqlite3.connect(DB)
            conn.execute("INSERT OR REPLACE INTO blacklist(id,entity,reason,dna) VALUES(?,?,?,?)",
                         (dna, data["entity"], data.get("reason", ""), dna))
            conn.commit(); conn.close()
            return jsonify({"dna": dna})
        conn = sqlite3.connect(DB)
        rows = conn.execute("SELECT id,entity,reason,level,created_at FROM blacklist WHERE status='active'").fetchall()
        conn.close()
        return jsonify([{"dna": r[0], "entity": r[1], "reason": r[2], "level": r[3], "time": r[4]} for r in rows])

    @app.route("/warn", methods=["GET", "POST"])
    def warn():
        if request.method == "POST":
            data = request.get_json()
            dna = gen_dna("WARN", data.get("entity", ""))
            deadline = (datetime.datetime.now() + datetime.timedelta(hours=48)).isoformat()
            conn = sqlite3.connect(DB)
            conn.execute("INSERT INTO warnings(id,entity,warn_type,content,issued_at,dna) VALUES(?,?,?,?,?,?)",
                         (dna, data["entity"], data.get("warning_type", ""), data.get("content", ""), deadline, dna))
            conn.commit(); conn.close()
            return jsonify({"dna": dna, "deadline": deadline})
        conn = sqlite3.connect(DB)
        rows = conn.execute("SELECT id,entity,warn_type,content,issued_at,status FROM warnings ORDER BY rowid DESC LIMIT 50").fetchall()
        conn.close()
        return jsonify([{"dna": r[0], "entity": r[1], "type": r[2], "content": r[3], "issued_at": r[4], "status": r[5]} for r in rows])

    if __name__ == "__main__":
        print(f"🐉 龍魂元宇宙API (Flask) 端口{PORT}")
        app.run(host="0.0.0.0", port=PORT, debug=False)
