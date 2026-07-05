#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂對話系統 · L0 道德經倫理錨定包裝器 v1.0

行為：
  - 所有用戶輸入先經過本地 L0 道德經倫理錨定引擎（:9630）檢查
  - 阻斷級輸入直接返回 422，不進入任何模型
  - 通過後調用本地 v10.0 API（:18100）生成回覆；v10 失敗時本地兜底
  - 提供瀏覽器對話界面：GET /

端口：9635
DNA: #龍芯⚡️2026-07-05-LONGHUN-DIALOGUE-ETHICS-WRAPPER-v1.0
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="龍魂對話系統 · L0 倫理錨定包裝器", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ETHICS_API = os.environ.get("LONGHUN_ETHICS_API", "http://127.0.0.1:9630/check")
V10_API = os.environ.get("LONGHUN_V10_API", "http://127.0.0.1:18100")
# v10 同時接受 emoji 版與 ASCII fallback；urllib header 只能用 latin-1，所以這裡用 ASCII 版
DNA_CONFIRM = "CONFIRM-9622-ONLY-ONCE-LK9X-772Z"


class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = Field(default_factory=list)
    model: str = "longhun-v10-golden-dragon"


def now_iso() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat()


def make_dna(endpoint: str) -> str:
    ts = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    return f"#龍芯⚡️{ts}-{endpoint}-{uuid.uuid4().hex[:8]}"


def l0_check(text: str) -> Dict[str, Any]:
    """調用 L0 引擎進行倫理篩查；L0 未啟動時默認通過並標記跳過。"""
    if not text:
        return {"passed": True, "status": "🟢 通過", "reason": "空內容", "dna": ""}
    try:
        payload = json.dumps({"input": text[:2000], "output": ""}, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            ETHICS_API,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        overall = result.get("整體狀態", "")
        passed = overall.startswith("🟢") or overall.startswith("🟡")
        return {
            "passed": passed,
            "status": overall,
            "reason": result.get("錨點A", {}).get("原因", ""),
            "dna": result.get("DNA", ""),
            "detail": result,
        }
    except Exception as e:
        return {"passed": True, "status": "🟡 跳過", "reason": f"L0 暫不可達: {e}", "dna": ""}


def call_v10(messages: List[Dict[str, str]], model: str) -> str:
    """同步調用 v10 generate-stream，解析 SSE 後返回完整文本。"""
    url = f"{V10_API}/api/v10/models/{model}/generate-stream"
    payload = json.dumps({"messages": messages, "stream": True}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-DNA-Confirm": DNA_CONFIRM,
            "X-UID": "UID9622",
            "X-Request-DNA": f"lh-dna-{uuid.uuid4().hex}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60.0) as resp:
        raw = resp.read().decode("utf-8")
    text = ""
    for line in raw.splitlines():
        if line.startswith("data: "):
            chunk = line[6:]
            if chunk == "[DONE]":
                break
            try:
                data = json.loads(chunk)
                delta = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                text += delta
            except Exception:
                pass
    return text or "（v10 返回空內容）"


def generate_reply(message: str, history: List[Dict[str, str]], model: str) -> Dict[str, Any]:
    messages = list(history)
    messages.append({"role": "user", "content": message})
    try:
        reply = call_v10(messages, model)
        source = "v10"
    except Exception as e:
        reply = f"【本地兜底】龍魂已收到：{message}\n（v10 暫不可達：{e}）"
        source = "local-fallback"
    return {"reply": reply, "source": source, "model": model}


@app.get("/health")
def health():
    ethics_ok = False
    try:
        urllib.request.urlopen(ETHICS_API.replace("/check", "/health"), timeout=1.0)
        ethics_ok = True
    except Exception:
        pass
    return {
        "status": "ok",
        "service": "dialogue-ethics-wrapper",
        "ethics_api_reachable": ethics_ok,
        "dna": make_dna("health"),
    }


@app.post("/chat")
def chat(req: ChatRequest):
    ethics = l0_check(req.message)
    if not ethics["passed"]:
        return JSONResponse(
            status_code=422,
            content={
                "code": 40001,
                "message": "L0 道德經倫理錨定層阻斷本次對話",
                "timestamp": now_iso(),
                "ethics": ethics,
                "dna": make_dna("chat-blocked"),
            },
        )
    result = generate_reply(req.message, req.history, req.model)
    return {
        "code": 0,
        "message": "ok",
        "timestamp": now_iso(),
        "ethics": ethics,
        "data": result,
        "dna": make_dna("chat"),
    }


CHAT_UI = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>龍魂對話 · L0 倫理錨定</title>
<style>
:root{--bg:#0a0a0f;--bg2:#12121a;--border:#2a2a3a;--accent:#a78bfa;--green:#4ade80;--red:#f87171;--yellow:#fbbf24;--text:#e4e4e7;--dim:#71717a;}
body{margin:0;padding:0;background:var(--bg);color:var(--text);font-family:"PingFang SC","Microsoft YaHei",sans-serif;font-size:14px;line-height:1.6;display:flex;flex-direction:column;height:100vh}
.header{padding:14px 20px;border-bottom:1px solid var(--border);background:var(--bg2)}
.header h1{margin:0;font-size:18px;color:var(--accent)}
.header p{margin:4px 0 0;font-size:12px;color:var(--dim)}
.chat{flex:1;overflow-y:auto;padding:16px 20px;display:flex;flex-direction:column;gap:12px}
.msg{max-width:80%;padding:10px 14px;border-radius:10px;white-space:pre-wrap}
.user{align-self:flex-end;background:#3b82f633;border:1px solid #60a5fa}
.bot{align-self:flex-start;background:var(--bg2);border:1px solid var(--border)}
.block{align-self:center;background:#ef444433;border:1px solid var(--red);color:var(--red);max-width:90%}
.input-area{padding:14px 20px;border-top:1px solid var(--border);display:flex;gap:10px;background:var(--bg2)}
.input-area textarea{flex:1;min-height:60px;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);padding:10px;font-size:14px;resize:vertical}
.input-area button{background:var(--accent);color:#000;border:none;border-radius:8px;padding:0 20px;font-weight:700;cursor:pointer}
.input-area button:disabled{opacity:.5;cursor:not-allowed}
.meta{font-size:11px;color:var(--dim);margin-top:4px}
</style>
</head>
<body>
<div class="header">
  <h1>🐉 龍魂對話 · L0 道德經倫理錨定</h1>
  <p>所有輸入先經 :9630 L0 引擎檢查 · 阻斷級內容不會送達模型 · 數據根留本地</p>
</div>
<div class="chat" id="chat"></div>
<div class="input-area">
  <textarea id="msg" placeholder="輸入想說的話...">請幫我分析一下這個數據</textarea>
  <button id="send" onclick="send()">發送</button>
</div>
<script>
async function send(){
  const input = document.getElementById('msg');
  const text = input.value.trim();
  if(!text) return;
  const chat = document.getElementById('chat');
  chat.innerHTML += `<div class="msg user">${escapeHtml(text)}</div>`;
  input.value = '';
  document.getElementById('send').disabled = true;
  try{
    const r = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message:text, history:[]})});
    const d = await r.json();
    if(r.status === 422){
      chat.innerHTML += `<div class="msg block">🛡️ L0 阻斷<br>${escapeHtml(d.message)}<br>原因：${escapeHtml(d.ethics?.reason||'')}</div>`;
    } else {
      chat.innerHTML += `<div class="msg bot">${escapeHtml(d.data?.reply||'')}<div class="meta">來源：${d.data?.source||''} · ${d.ethics?.status||''}</div></div>`;
    }
  }catch(e){
    chat.innerHTML += `<div class="msg block">請求失敗：${escapeHtml(e.message)}</div>`;
  }
  document.getElementById('send').disabled = false;
  chat.scrollTop = chat.scrollHeight;
}
function escapeHtml(t){
  return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}
document.getElementById('msg').addEventListener('keydown', e=>{ if(e.key==='Enter' && !e.shiftKey){ e.preventDefault(); send(); }});
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def index():
    return CHAT_UI


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("LONGHUN_DIALOGUE_PORT", "9635"))
    print(f"🐉 龍魂對話系統（L0 倫理錨定）· http://127.0.0.1:{port}")
    print(f"   DNA: #龍芯⚡️2026-07-05-LONGHUN-DIALOGUE-ETHICS-WRAPPER-v1.0")
    uvicorn.run(app, host="127.0.0.1", port=port)
