#!/usr/bin/env python3
"""
🐉 龍魂引擎 · Web通道适配器
=============================
官网/Web Widget → HTTP API → 统一 Message → 引擎内核 → JSON响应

同时提供静态 Web Widget 前端页面。

启动:
  python3 引擎/channels/web_adapter.py
  端口: 9639 (默认)

DNA: #龍芯⚡️丙午·乙未·甲子·申时·需-WEB-ADAPTER-v1.0
"""

from __future__ import annotations
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from 引擎.message import Message, Response, Channel, AuditLevel
from 引擎.engine_core import LonghunEngine

CST = timezone(timedelta(hours=8))
DNA = "#龍芯⚡️丙午·乙未·甲子·申时·需-WEB-ADAPTER-v1.0"
WEB_BOT_PORT = int(os.getenv("WEB_BOT_PORT", "9639"))

engine = LonghunEngine(safe_mode=True)

app = FastAPI(
    title="龍魂引擎 · Web通道",
    description="官网Widget / 公开API / WebSocket",
    version="2.0.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# ═══════════════════════════════════════════════
# REST API
# ═══════════════════════════════════════════════

@app.get("/health")
def health():
    return {
        "status": "ok",
        "channel": "web",
        "dna": DNA,
        "engine": engine.get_health(),
    }


@app.get("/api/query")
def api_query(q: str = ""):
    """统一查询接口"""
    if not q:
        return {"error": "请提供 q 参数"}
    msg = Message(channel=Channel.WEB, content=q)
    response = engine.process(msg)
    return {"response": response.to_dict()}


@app.post("/api/query")
async def api_query_post(request: Request):
    """POST 查询"""
    body = await request.json()
    text = body.get("text", body.get("q", ""))
    if not text:
        return {"error": "请提供 text 或 q 参数"}
    msg = Message(channel=Channel.WEB, content=text)
    response = engine.process(msg)
    return {"response": response.to_dict()}


@app.get("/api/capabilities")
def api_capabilities():
    caps = []
    for cap in engine.registry.list_all():
        caps.append({
            "name": cap.name,
            "display": cap.display_name,
            "description": cap.description,
            "keywords": cap.keywords,
            "examples": cap.examples,
            "persona": cap.persona,
        })
    return {"dna": DNA, "capabilities": caps, "total": len(caps)}


# ═══════════════════════════════════════════════
# Web Widget 前端
# ═══════════════════════════════════════════════

@app.get("/", response_class=HTMLResponse)
def widget_page():
    """龍魂 Web Widget 前端"""
    return HTMLResponse(WIDGET_HTML)


WIDGET_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🐉 龍魂引擎</title>
<style>
:root {
  --bg: #0a0a0f;
  --surface: #131320;
  --border: #2a2a3a;
  --text: #e0e0e0;
  --text-dim: #808090;
  --accent: #c9a84c;
  --accent-glow: #f0d060;
  --red: #e05555;
  --green: #55b855;
  --yellow: #c9a84c;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
  height: 100vh;
  display: flex;
  flex-direction: column;
}
.header {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.header h1 { font-size: 18px; color: var(--accent); }
.header .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green); }
.header .status { font-size: 12px; color: var(--text-dim); }
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.msg {
  max-width: 85%;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  word-break: break-word;
}
.msg.user {
  align-self: flex-end;
  background: var(--accent);
  color: #1a1a2e;
}
.msg.bot {
  align-self: flex-start;
  background: var(--surface);
  border: 1px solid var(--border);
}
.msg.bot .dna {
  font-size: 10px;
  color: var(--text-dim);
  margin-top: 6px;
  font-family: monospace;
}
.msg.red { border-left: 3px solid var(--red); }
.msg.yellow { border-left: 3px solid var(--yellow); }
.input-area {
  background: var(--surface);
  border-top: 1px solid var(--border);
  padding: 12px 20px;
  display: flex;
  gap: 10px;
}
.input-area input {
  flex: 1;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  color: var(--text);
  font-size: 14px;
  outline: none;
}
.input-area input:focus { border-color: var(--accent); }
.input-area button {
  background: var(--accent);
  color: #1a1a2e;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}
.input-area button:hover { background: var(--accent-glow); }
.input-area button:disabled { opacity: 0.5; cursor: not-allowed; }
.typing { color: var(--text-dim); font-size: 12px; padding: 0 20px 8px; }
.suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 8px 20px;
}
.suggestions span {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 4px 12px;
  font-size: 12px;
  cursor: pointer;
  color: var(--text-dim);
}
.suggestions span:hover { border-color: var(--accent); color: var(--text); }
@media (max-width: 600px) {
  .msg { max-width: 95%; }
}
</style>
</head>
<body>
<div class="header">
  <div class="dot"></div>
  <h1>🐉 龍魂引擎</h1>
  <span class="status" id="status">就绪</span>
</div>
<div class="suggestions" id="suggestions">
  <span onclick="sendQuick('系统状态')">系统状态</span>
  <span onclick="sendQuick('人格 top5')">人格排行</span>
  <span onclick="sendQuick('安全检查')">安全检查</span>
  <span onclick="sendQuick('算一下 369')">五行演算</span>
  <span onclick="sendQuick('帮助')">帮助</span>
</div>
<div class="messages" id="messages">
  <div class="msg bot">
    🐉 你好，我是龍魂引擎。<br/>
    输入「帮助」查看我能做什么。
  </div>
</div>
<div class="typing" id="typing"></div>
<div class="input-area">
  <input id="input" placeholder="输入你的问题..." onkeydown="if(event.key==='Enter')send()" autofocus>
  <button onclick="send()">发送</button>
</div>
<script>
const API = '/api/query';
const msgs = document.getElementById('messages');
const input = document.getElementById('input');
const typing = document.getElementById('typing');
const status = document.getElementById('status');

async function send() {
  const text = input.value.trim();
  if (!text) return;
  input.value = '';
  input.disabled = true;

  addMsg(text, 'user');
  typing.textContent = '🐉 思考中...';
  status.textContent = '处理中';

  try {
    const resp = await fetch(API + '?q=' + encodeURIComponent(text));
    const data = await resp.json();
    const r = data.response;
    let cls = r.audit_level === 'red' ? 'red' : r.audit_level === 'yellow' ? 'yellow' : '';
    let content = r.content || '(空)';
    if (r.title) content = '**' + r.title + '**\n' + content;
    addMsg(content, 'bot', cls, r.dna_trace);
    status.textContent = r.success ? '就绪' : '错误';
  } catch(e) {
    addMsg('连接失败: ' + e, 'bot', 'red');
    status.textContent = '离线';
  }

  input.disabled = false;
  input.focus();
  typing.textContent = '';
}

function sendQuick(text) {
  input.value = text;
  send();
}

function addMsg(text, role, cls, dna) {
  const div = document.createElement('div');
  div.className = 'msg ' + role + (cls ? ' ' + cls : '');
  div.innerHTML = text.replace(/\n/g, '<br/>');
  if (dna) div.innerHTML += '<div class="dna">🧬 ' + dna + '</div>';
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

input.focus();
</script>
</body>
</html>"""


# ─── 启动 ───
if __name__ == "__main__":
    import uvicorn
    print(f"""
╔══════════════════════════════════════════════════════╗
║   🐉 龍魂引擎 · Web通道 v2.0                       ║
╠══════════════════════════════════════════════════════╣
║  DNA:    {DNA}
║  端口:   {WEB_BOT_PORT}
║  引擎:   统一内核 · {len(engine.registry.list_all())} 项能力
╚══════════════════════════════════════════════════════╝
📡 端点:
   GET  /                   — Web Widget 前端
   GET  /api/query?q=...    — HTTP 查询
   POST /api/query          — POST 查询
   GET  /api/capabilities   — 能力清单
   GET  /health             — 健康检查

🌐 浏览器打开: http://localhost:{WEB_BOT_PORT}/
""")
    uvicorn.run(app, host="127.0.0.1", port=WEB_BOT_PORT, log_level="info")
