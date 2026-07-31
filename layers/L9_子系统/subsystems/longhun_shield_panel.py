# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂护盾 Web 面板 — 实时攻击地图
DNA: #龍芯⚡️2026-06-29-LONGHUN-SHIELD-PANEL-v1.0
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect  # type: ignore[import-untyped]
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import-untyped]

from longhun_shield_cnsh import 龍魂护盾
from longhun_ai_output_guard import AI输出熔断器
from longhun_download_guard import 下载文件检测器, 下载隔离区

app = FastAPI(title="龍魂护盾 Web 面板")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8766", "http://127.0.0.1:8766"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-DNA-TRACE"],
)
护盾 = 龍魂护盾()
AI熔断器 = AI输出熔断器(护盾)
文件检测器 = 下载文件检测器(护盾)
隔离区 = 下载隔离区(Path(os.environ.get("LONGHUN_QUARANTINE_DIR", str(Path.home() / ".longhun" / "quarantine"))))
连接池: List[WebSocket] = []


def 广播到面板(事件: Dict[str, Any]):
    数据 = json.dumps(事件, ensure_ascii=False)
    存活 = []
    for ws in 连接池:
        try:
            asyncio.create_task(ws.send_text(数据))
            存活.append(ws)
        except Exception:
            pass
    连接池[:] = 存活


护盾.广播器.注册(广播到面板)


HTML_PAGE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>龍魂护盾 · 实时攻击地图</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 20px; background:#0b0f19; color:#e0e6ed; }
  h1 { color:#00d4aa; }
  .grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(280px,1fr)); gap:16px; margin: 20px 0; }
  .card { background:#151b29; border:1px solid #253046; border-radius:8px; padding:16px; }
  .card h3 { margin-top:0; color:#4fc3f7; }
  .log { height:320px; overflow:auto; background:#0d111d; border:1px solid #253046; border-radius:6px; padding:10px; font-family:monospace; font-size:13px; }
  .entry { margin-bottom:6px; border-bottom:1px solid #1c2538; padding-bottom:4px; }
  .entry .ts { color:#888; }
  .entry .dim { color:#ff9800; }
  .entry .id { color:#00d4aa; }
  .badge { display:inline-block; padding:2px 8px; border-radius:4px; font-size:12px; margin-left:8px; }
  .green { background:#1b5e20; }
  .red { background:#b71c1c; }
  .yellow { background:#f57f17; }
  button { background:#00d4aa; color:#000; border:none; padding:8px 16px; border-radius:4px; cursor:pointer; }
</style>
</head>
<body>
<h1>🛡️ 龍魂护盾 · 实时攻击地图</h1>
<div class="grid">
  <div class="card"><h3>系统状态</h3><div id="status">连接中...</div></div>
  <div class="card"><h3>观察名单数</h3><div id="watchlist">-</div></div>
  <div class="card"><h3>已封禁身份</h3><div id="blocked">-</div></div>
  <div class="card"><h3>操作</h3><button onclick="demo()">模拟一次攻击</button></div>
</div>
<div class="card">
  <h3>实时攻击日志</h3>
  <div id="log" class="log"></div>
</div>
<script>
const log = document.getElementById('log');
function addEntry(e) {
  const div = document.createElement('div');
  div.className = 'entry';
  let badge = '';
  if (e.类型 === 'threat_alert') badge = '<span class="badge red">威胁</span>';
  if (e.类型 === 'shame_wall_record') badge = '<span class="badge yellow">上链</span>';
  div.innerHTML = `<span class="ts">${new Date().toLocaleTimeString()}</span> ${badge} <span class="dim">${e.维度 || e.类型}</span> <span class="id">${e.攻击者标识 || ''}</span> ${e.等级 || ''} ${e.分数 || ''}`;
  log.prepend(div);
}
async function refreshStatus() {
  const r = await fetch('/api/status');
  const s = await r.json();
  const fuse = s.熔断器 || '未知';
  const fuseHtml = fuse === '完整' ? '<span class="green">✅ 主权完整</span>' : '<span class="red">❌ ' + fuse + '</span>';
  document.getElementById('status').innerHTML = `熔断器：${fuseHtml}<br>墙完整性：<b>${s.墙完整性 ? '✅ 正常' : (s.墙完整性 === false ? '❌ 异常' : '—')}</b><br>DNA：${s.dna}`;
  document.getElementById('watchlist').textContent = s.观察名单数 || '—';
  document.getElementById('blocked').textContent = (s.已封禁身份 || []).join(', ') || '无';
}
async function demo() {
  await fetch('/api/demo', {method: 'POST'});
}
const ws = new WebSocket(`ws://${location.host}/ws`);
ws.onmessage = ev => addEntry(JSON.parse(ev.data));
ws.onopen = () => { refreshStatus(); setInterval(refreshStatus, 3000); };
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def 首页():
    return HTMLResponse(HTML_PAGE)


@app.get("/api/status")
async def 状态():
    return 护盾.状态()


@app.get("/api/wall")
async def 耻辱墙记录(n: int = 50):
    if not 护盾.墙.路径.exists():
        return []
    记录 = []
    with open(护盾.墙.路径, "r", encoding="utf-8") as f:
        for line in f:
            记录.append(json.loads(line))
    return 记录[-n:]


@app.get("/api/watchlist")
async def 观察名单():
    return {
        k: {"分数": v["分数"], "事件数": len(v["事件"])}
        for k, v in 护盾.感知._观察名单.items()
    }


@app.post("/api/demo")
async def 模拟攻击():
    护盾.检查网络("attacker_9.9.9.9", {
        "path": "/api/search",
        "q": "1' UNION SELECT * FROM users--"
    })
    return {"ok": True}


@app.get("/api/fuse")
async def 熔断状态():
    return {
        "主权完整": not getattr(护盾, '_已熔断', False),
        "锚定": getattr(护盾.熔断器, '脱氧核糖核酸锚定', '') if hasattr(护盾, '熔断器') else ''
    }


@app.post("/api/ai-scan")
async def AI输出扫描(请求: Dict[str, Any]):
    来源 = 请求.get("来源", "unknown")
    内容 = 请求.get("内容", "")
    return AI熔断器.检查(来源, 内容)


@app.post("/api/download-event")
async def 浏览器下载事件(请求: Dict[str, Any]):
    """浏览器扩展上报下载完成事件，立即触发本地扫描。"""
    本地路径 = Path(请求.get("local_path", ""))
    文件名 = 请求.get("filename", 本地路径.name)
    来源网址 = 请求.get("url", "")
    if not 本地路径.exists():
        return {"通过": True, "原因": "文件尚未落地，等待目录看守处理", "路径": str(本地路径)}

    结果 = 文件检测器.检测(本地路径)
    if not 结果["通过"]:
        隔离路径 = 隔离区.隔离(本地路径, "BROWSER_DL")
        护盾.感知.上报("download", 文件名, {
            "原因": "浏览器下载文件可疑",
            "来源网址": 来源网址,
            "风险项": 结果.get("风险项", []),
        })
        return {**结果, "隔离路径": str(隔离路径), "路径": str(本地路径)}
    return {"通过": True, "原因": "干净", "路径": str(本地路径)}


@app.websocket("/ws")
async def 实时通道(ws: WebSocket):
    await ws.accept()
    连接池.append(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        if ws in 连接池:
            连接池.remove(ws)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("LONGHUN_PANEL_PORT", "8788"))
    uvicorn.run(app, host="127.0.0.1", port=port)
