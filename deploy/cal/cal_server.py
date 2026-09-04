#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cal_server.py - 龍魂 CAL 命令抽象层服务端 v1.3
# DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-CAL-SERVER-v1.3-AUTOROUTE
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 主权声明: 龍魂系统·数据主权归用户·token永不上云·D1永不触碰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 架构: 多端 -> nginx(443/wss) -> CAL(127.0.0.1:8765) -> [lh.py | Ollama | Notion | CodeBuddy]
# 安全: token 鉴权 + 命令白名单 + 列表传参(无shell) + 审计append-only + 只绑127.0.0.1

import asyncio
import hashlib
import hmac
import json
import logging
import os
import re
import subprocess
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Header, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("cal_server")

# ─── 常量 ───────────────────────────────────────────────
BASE_DIR = Path("/opt/longhun/cal")
TOKEN_FILE = BASE_DIR / ".cal_token"
AUDIT_LOG = BASE_DIR / "cal_audit.log"
LH = "/opt/longhun/lh.py"
WORKDIR = "/opt/longhun"
TIMEOUT = 120            # 单命令超时(秒)
MAX_OUTPUT = 50000       # 输出截断上限(字节)
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
# Mac 桥接隧道: Mac 上 ssh -R 8766:127.0.0.1:18765 root@鲲鹏
# 把鲲鹏 127.0.0.1:8766 反向映射到 Mac 的 cal_mac_bridge.py(18765)。
# Notion/CodeBuddy 走这里转发, token 永不上云。
BRIDGE_URL = "http://127.0.0.1:8766"
CST = timezone(timedelta(hours=8))
VERSION = "1.3"
DNA = "#龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-CAL-SERVER-v1.3-AUTOROUTE"

# ─── 白名单命令表（预定义·安全闸·对齐 lh.py 真实flag）──
COMMANDS = {
    "health":      ["L", ["python3", LH, "--health"]],
    "audit":       ["L", ["python3", LH, "--audit"]],
    "push":        ["L", ["python3", LH, "--push"]],
    "personas":    ["L", ["python3", LH, "--personas"]],
    "dashboard":   ["L", ["python3", LH, "--dashboard"]],
    "engine":      ["L", ["python3", LH, "--engine"]],
    "brain":       ["L", ["python3", LH, "--brain", "status"]],
    "hub":         ["L", ["python3", LH, "--hub", "status"]],
    "xuanji":      ["L", ["python3", LH, "--xuanji"]],
    "ping_local":  ["L", ["python3", "-c", "import socket; [print(f'{p}: {\"OK\" if socket.socket().connect_ex((\"127.0.0.1\", p))==0 else \"DEAD\"}') for p in [8765,8769,8771,8773,8970,8971,8972,9631]]"]],
    "disk":        ["S", "df -h / | tail -1 && echo '---MEM---' && free -m | head -2"],
    "uptime":      ["S", "uptime && echo '---LOAD---' && cat /proc/loadavg"],
}

# ─── 工具函数 ───────────────────────────────────────────
def now_str():
    return datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00")

def load_token() -> str:
    try:
        return TOKEN_FILE.read_text().strip()
    except OSError:
        # 文件不存在/读失败 → 视为无令牌（未初始化），由调用方决定放行或拒绝
        return ""

def check_token(given: str) -> bool:
    real = load_token()
    if not real or not given:
        return False
    return hmac.compare_digest(real.encode(), given.encode())

def audit(ip: str, cmd: str, exit_code: int, ok: bool, note: str = ""):
    entry = {
        "ts": now_str(), "ip": ip, "cmd": cmd[:200],
        "exit": exit_code, "ok": ok, "note": note[:200],
        "dna": DNA,
    }
    try:
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        # 审计写失败不允许崩主流程（否则审计本身成为攻击面）
        logger.warning("审计写入失败: %s", e)

def run_command(cmd_id: str) -> dict:
    spec = COMMANDS.get(cmd_id)
    if not spec:
        return {"status": "denied", "output": f"❌ 未知命令: {cmd_id}（不在白名单）", "exit": -1}
    mode, argv = spec
    try:
        if mode == "L":
            p = subprocess.run(argv, capture_output=True, text=True,
                               timeout=TIMEOUT, cwd=WORKDIR)
            out = p.stdout + p.stderr
        else:
            p = subprocess.run(argv, shell=True, capture_output=True, text=True,
                               timeout=TIMEOUT, cwd=WORKDIR)
            out = p.stdout + p.stderr
        code = p.returncode
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "output": f"⏱️ 命令超时({TIMEOUT}s): {cmd_id}", "exit": -1}
    except Exception as e:
        return {"status": "error", "output": f"❌ 执行异常: {e}", "exit": -1}
    if len(out) > MAX_OUTPUT:
        out = out[:MAX_OUTPUT] + f"\n... [输出已截断 {MAX_OUTPUT}B]"
    return {"status": "ok" if code == 0 else "error",
            "output": out.strip() or "(无输出)", "exit": code}

def run_nl_text(text: str) -> dict:
    try:
        p = subprocess.run(["python3", LH, text], capture_output=True,
                           text=True, timeout=TIMEOUT, cwd=WORKDIR)
        out = p.stdout + p.stderr
        if len(out) > MAX_OUTPUT:
            out = out[:MAX_OUTPUT] + f"\n... [输出已截断 {MAX_OUTPUT}B]"
        return {"status": "ok" if p.returncode == 0 else "error",
                "output": out.strip() or "(无输出)", "exit": p.returncode}
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "output": f"⏱️ 命令超时({TIMEOUT}s)", "exit": -1}
    except Exception as e:
        return {"status": "error", "output": f"❌ 执行异常: {e}", "exit": -1}

# ─── AI / Notion 后端 ────────────────────────────────────
def ollama_generate(model: str, prompt: str, max_tokens: int = 512) -> dict:
    """调用本地 Ollama 龍魂模型。如果 Ollama 未启动返回友好提示。"""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": max_tokens}
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return {"status": "ok", "output": body.get("response", "(模型无返回)").strip(),
                    "model": model, "exit": 0}
    except urllib.error.HTTPError as e:
        return {"status": "error", "output": f"Ollama HTTP {e.code}: {e.read().decode('utf-8','ignore')[:200]}", "exit": e.code}
    except urllib.error.URLError as e:
        return {"status": "error", "output": f"🦙 Ollama 未就绪: {e.reason}\n请确认鲲鹏上 ollama serve 已启动（端口 11434）。", "exit": -1}
    except Exception as e:
        return {"status": "error", "output": f"调用 Ollama 异常: {e}", "exit": -1}

def bridge_call(path: str, payload: dict, timeout: int = 45) -> dict:
    """经反向隧道转发到 Mac 桥接（token 永不上云）。"""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{BRIDGE_URL}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body
    except urllib.error.URLError as e:
        return {"status": "error", "output": f"🔌 Mac 桥接隧道未连接: {e.reason}\n请在 Mac 上运行:\n  python3 ~/longhun-system/deploy/cal/cal_mac_bridge.py &\n  ssh -R 8766:127.0.0.1:18765 root@119.13.90.27", "exit": -1}
    except Exception as e:
        return {"status": "error", "output": f"🔌 桥接调用异常: {e}", "exit": -1}

def notion_search(query: str) -> dict:
    """Notion 搜索 → 转发 Mac 桥接。"""
    if not query:
        return {"status": "error", "output": "❌ 请输入搜索词", "exit": -1}
    return bridge_call("/api/notion/search", {"query": query[:200]})

def codebuddy_bridge(message: str) -> dict:
    """CodeBuddy AI 消息 → 转发 Mac 桥接（异步收信 + 我的回复）。"""
    return bridge_call("/api/codebuddy/message", {"message": message[:2000]})

# ─── 说人话 · 自动路由（v1.3）────────────────────────────
# 规则: 关键词判定, 不调模型(省算力·可预测·零黑箱)。
# 优先级: 显式前缀 > Notion搜 > lh系统命令 > 转AI > 兜底龍魂模型。
# 透明: 返回 (目标model, 清洗后文本), 前端 meta 展示实际路由。

# 中文指令 → 白名单命令别名（对齐 COMMANDS，避免中文被当NL丢给lh.py扑空）
LH_ALIAS = {
    # 特异性高的排前面, health 的"状态"兜底放最后（避免吞"端口状态/磁盘状态"）
    "ping_local":["端口", "ping"],
    "disk":      ["磁盘", "内存", "存储", "disk", "df"],
    "xuanji":    ["璇玑", "推演", "xuanji"],
    "brain":     ["中枢", "brain"],
    "hub":       ["归集", "hub"],
    "engine":    ["引擎", "engine"],
    "dashboard": ["仪表盘", "dashboard"],
    "personas":  ["人格", "persona", "personas"],
    "push":      ["推送", "一键", "push"],
    "audit":     ["审计", "安全", "audit"],
    "uptime":    ["负载", "运行", "uptime", "load"],
    "health":    ["健康", "体检", "状态", "status", "health"],
}

def lh_alias(text: str):
    """中文指令 → 白名单 cmd_id；映射不到返回 None。"""
    t = text.lower()
    for cmd, kws in LH_ALIAS.items():
        if any(k in t for k in kws):
            return cmd
    return None

def auto_route(text: str):
    t = text.strip()
    low = t.lower()
    # 0) 显式前缀: /notion 词  /lh 命令  /ai 消息  → 强制直达
    for prefix, target in (("/notion", "notion"), ("/搜索", "notion"), ("/lh", "lh"),
                           ("/命令", "lh"), ("/ai", "codebuddy"), ("/cb", "codebuddy")):
        if t.startswith(prefix):
            rest = t[len(prefix):].strip()
            return target, rest
    # 1) Notion 搜索意图（且不是系统状态类）
    if re.search(r"(搜索|搜一下|搜|查资料|知识库|notion|百科)", low) \
            and not re.search(r"(健康|体检|审计|复盘|推送|状态|负载|端口|盘点)", low):
        return "notion", t
    # 2) 转给 CodeBuddy AI（"告诉AI"整体匹配, 避免误伤"告诉我磁盘"）
    if re.search(r"(转给|告诉AI|问问AI|交给AI|让AI|@ai|@codebuddy)", low, re.IGNORECASE):
        return "codebuddy", t
    # 3) lh 系统命令词
    if re.search(r"(健康|体检|审计|复盘|推送|人格|引擎|磁盘|负载|端口|盘点|状态|status|health|audit|push|disk|uptime)", low):
        return "lh", t
    # 4) 兜底: 龍魂模型对话
    return "longhun", t

# ─── FastAPI ────────────────────────────────────────────
app = FastAPI(title="龍魂 CAL", version=VERSION)

INDEX_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>龍魂 CAL · 跨端统一入口</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0b0d12;color:#e8e6e1;font-family:-apple-system,"PingFang SC",sans-serif;min-height:100vh;display:flex;flex-direction:column}
header{padding:18px 20px;border-bottom:1px solid #2a2d36;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
header h1{font-size:20px;letter-spacing:1px}
header .dna{color:#8b8f9a;font-size:11px;flex:1;text-align:right;word-break:break-all}
main{flex:1;padding:16px 20px;max-width:960px;width:100%;margin:0 auto}
.token-bar{display:flex;gap:8px;margin-bottom:14px}
input[type=password],input[type=text],select{background:#15181f;border:1px solid #2a2d36;border-radius:8px;color:#e8e6e1;padding:10px 12px;font-size:14px}
input[type=text],input[type=password]{flex:1}
select{min-width:130px;color:#e8e6e1}
option{background:#15181f;color:#e8e6e1}
button{background:#c9a227;border:none;color:#0b0d12;font-weight:700;padding:10px 16px;border-radius:8px;cursor:pointer;font-size:14px}
button:hover{background:#e0b73c}
.btn-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin-bottom:14px}
.btn-grid button{background:#1c2029;color:#e8e6e1;border:1px solid #2a2d36;padding:12px 8px;font-size:13px}
.btn-grid button:hover{background:#2a2f3a;border-color:#c9a227}
.nl-bar{display:flex;gap:8px;margin-bottom:14px}
#out{background:#0d0f14;border:1px solid #2a2d36;border-radius:8px;padding:14px;font-family:ui-monospace,Menlo,monospace;font-size:12px;white-space:pre-wrap;word-break:break-all;min-height:200px;max-height:60vh;overflow:auto;color:#a5e6a0}
#out .err{color:#ff7b72}
#meta{color:#8b8f9a;font-size:11px;margin-top:8px}
.model-hint{color:#8b8f9a;font-size:12px;margin-bottom:8px}
.adv{margin-bottom:14px;border:1px solid #2a2d36;border-radius:8px;padding:8px 12px}
.adv summary{cursor:pointer;color:#8b8f9a;font-size:12px;user-select:none}
.adv summary:hover{color:#c9a227}
.adv .adv-inner{display:flex;gap:8px;align-items:center;margin-top:8px;flex-wrap:wrap}
footer{padding:12px 20px;border-top:1px solid #2a2d36;color:#5a5e68;font-size:11px;text-align:center}
</style>
</head>
<body>
<header>
  <h1>龍魂 CAL</h1>
  <span style="color:#8b8f9a;font-size:12px">跨端统一入口 · 浏览器/手机/平板</span>
  <div class="dna" id="hdna"></div>
</header>
<main>
  <div class="token-bar">
    <input type="password" id="token" placeholder="输入访问令牌（存在本机浏览器·不传服务器存储）">
    <button onclick="saveToken()">记住</button>
  </div>
  <div class="btn-grid" id="btns"></div>
  <div class="nl-bar">
    <input type="text" id="nl" placeholder="直接说人话，自动路由：搜龍魂 / 健康检查 / 复盘 / 告诉AI帮我看看 ... 回车发送" onkeydown="if(event.key==='Enter')runNL()">
    <button onclick="runNL()">发送</button>
  </div>
  <details class="adv">
    <summary>⚙️ 高级选项 · 当前：🤖 自动路由（说人话即可，不用选）</summary>
    <div class="adv-inner">
      <select id="model">
        <option value="auto">🤖 自动路由（推荐）</option>
        <option value="longhun">🐉 龍魂模型 (Ollama)</option>
        <option value="longhun-judge">⚖️ 龍魂 judge</option>
        <option value="notion">📝 Notion 引擎</option>
        <option value="codebuddy">🧑‍✈️ CodeBuddy AI</option>
        <option value="lh">🛠️ lh.py 命令</option>
      </select>
      <div class="model-hint" style="margin:0">手动选了就走指定引擎；显式前缀直达：/notion 词 · /lh 命令 · /ai 消息。所有路径都记审计、可回查。</div>
    </div>
  </details>
  <pre id="out">连接状态：等待指令…</pre>
  <div id="meta"></div>
</main>
<footer>龍魂系统 · 数据主权归 UID9622 · 命令白名单 · 审计可追溯</footer>
<script>
const BTNS=[["health","🏥 健康检查"],["audit","🛡️ 安全审计"],["personas","👥 人格列表"],["dashboard","📊 人格仪表盘"],["engine","⚙️ 引擎能力"],["brain","🧠 统一中枢"],["hub","📦 AI归集Hub"],["xuanji","🔮 璇玑推演"],["disk","💾 磁盘内存"],["uptime","⏱️ 负载运行"],["ping_local","🏓 本地端口"],["push","🚀 一键推送"]];
const tkEl=document.getElementById('token'),outEl=document.getElementById('out');
function renderBtns(){document.getElementById('btns').innerHTML=BTNS.map(b=>'<button onclick="run(\''+b[0]+'\')">'+b[1]+'</button>').join('')}
function saveToken(){localStorage.setItem('cal_token',tkEl.value.trim());showMeta('令牌已记住（本机浏览器）')}
function getTok(){return localStorage.getItem('cal_token')||tkEl.value.trim()}
async function run(id){outEl.textContent='⏳ 执行中: '+id+' …';showMeta('');try{
 const r=await fetch('/api/run',{method:'POST',headers:{'Content-Type':'application/json','X-CAL-Token':getTok()},body:JSON.stringify({cmd:id})});
 const d=await r.json();print(d);
}catch(e){outEl.textContent='❌ 连接失败: '+e;}}
async function runNL(){const t=document.getElementById('nl').value.trim();if(!t)return;const m=document.getElementById('model').value;outEl.textContent='⏳ '+(m==='auto'?'🤖 自动路由':m)+': '+t+' …';try{
 const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json','X-CAL-Token':getTok()},body:JSON.stringify({model:m,message:t,max_tokens:512})});
 const d=await r.json();print(d);
}catch(e){outEl.textContent='❌ 连接失败: '+e;}}
function print(d){outEl.className='';if(d.status==='ok'){outEl.textContent=d.output}else{outEl.className='err';outEl.textContent=(d.output||d.detail||'未知错误')}
 showMeta('状态:'+(d.status||'-')+' · 退出码:'+(d.exit??'-')+' · 模型:'+(d.model||'-')+' · 时间:'+(d.ts||'-'))}
function showMeta(s){document.getElementById('meta').textContent=s}
function init(){renderBtns();const s=localStorage.getItem('cal_token');if(s){tkEl.value=s}const h=document.querySelector('.dna');if(h)h.textContent='#龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-CAL-WEB-v1.3'}
init();
</script>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return INDEX_HTML

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "龍魂 CAL", "version": VERSION,
            "ts": now_str(), "dna": DNA}

@app.post("/api/chat")
async def api_chat(req: Request, x_cal_token: str = Header(default="")):
    if not check_token(x_cal_token):
        audit(req.client.host if req.client else "?", "chat", -1, False, "token拒绝")
        raise HTTPException(status_code=401, detail="🔴 令牌无效·拒绝访问")
    try:
        body = await req.json()
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(status_code=400, detail="JSON格式错误")
    model = str(body.get("model", "auto")).strip() or "auto"
    message = str(body.get("message", "")).strip()[:2000]
    max_tokens = min(int(body.get("max_tokens", 512)), 2048)
    ip = req.client.host if req.client else "?"
    if not message:
        return {"status": "error", "output": "❌ 空输入", "exit": -1, "ts": now_str(), "dna": DNA}

    # 说人话 · 自动路由: 不指定模型时按关键词判断
    if model == "auto":
        model, message = auto_route(message)
        if not message:
            return {"status": "error", "output": "❌ 自动路由后指令为空（试试 /notion 词 /lh 命令 /ai 消息）",
                    "exit": -1, "ts": now_str(), "dna": DNA}

    if model in ("longhun", "longhun-v1.0", "qwen2.5"):
        res = ollama_generate(model + ":latest" if ":" not in model else model, message, max_tokens)
    elif model == "longhun-judge":
        res = ollama_generate("longhun-judge:latest", message, max_tokens)
    elif model == "notion":
        res = notion_search(message)
        res["model"] = "notion"
    elif model == "codebuddy":
        res = codebuddy_bridge(message)
        res["model"] = "codebuddy"
    elif model == "lh":
        cmd = lh_alias(message)
        if cmd:
            res = run_command(cmd)
            res["model"] = "lh:" + cmd       # 透明: 显示实际落到的白名单命令
        else:
            res = run_nl_text(message)
            res["model"] = "lh:nl"
    else:
        res = {"status": "error", "output": f"❌ 未知模型/引擎: {model}", "exit": -1}

    audit(ip, f"chat:{model}:{message[:50]}", res.get("exit", -1), res["status"] == "ok")
    res.update({"ts": now_str(), "dna": DNA})
    return res

@app.post("/api/run")
async def api_run(req: Request, x_cal_token: str = Header(default="")):
    if not check_token(x_cal_token):
        audit(req.client.host if req.client else "?", "-", -1, False, "token拒绝")
        raise HTTPException(status_code=401, detail="🔴 令牌无效·拒绝访问")
    try:
        body = await req.json()
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(status_code=400, detail="JSON格式错误")
    ip = req.client.host if req.client else "?"
    if "cmd" in body and isinstance(body["cmd"], str):
        cmd = body["cmd"].strip()
        if cmd not in COMMANDS:
            audit(ip, cmd, -1, False, "白名单拒绝")
            return {"status": "denied", "output": f"❌ 不在白名单: {cmd}", "exit": -1, "ts": now_str(), "dna": DNA}
        res = run_command(cmd)
        audit(ip, cmd, res["exit"], res["status"] == "ok")
        res.update({"ts": now_str(), "dna": DNA})
        return res
    if "text" in body and isinstance(body["text"], str):
        text = body["text"].strip()[:200]
        if not text:
            return {"status": "error", "output": "❌ 空输入", "exit": -1, "ts": now_str(), "dna": DNA}
        res = run_nl_text(text)
        audit(ip, "NL:" + text, res["exit"], res["status"] == "ok")
        res.update({"ts": now_str(), "dna": DNA})
        return res
    return {"status": "error", "output": "❌ 需要 cmd 或 text 字段", "exit": -1, "ts": now_str(), "dna": DNA}

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    authed = False
    try:
        while True:
            data = await ws.receive_text()
            try:
                obj = json.loads(data)
            except json.JSONDecodeError:
                await ws.send_text(json.dumps({"status": "error", "output": "JSON格式错误"}))
                continue
            if not authed:
                if obj.get("token") and check_token(obj["token"]):
                    authed = True
                    await ws.send_text(json.dumps({"status": "ok", "output": "✅ 认证通过·龍魂CAL已连接", "ts": now_str(), "dna": DNA}))
                else:
                    await ws.send_text(json.dumps({"status": "error", "output": "🔴 令牌无效"}))
                continue
            if "cmd" in obj and obj["cmd"] in COMMANDS:
                res = run_command(obj["cmd"])
                res.update({"ts": now_str(), "dna": DNA})
                await ws.send_text(json.dumps(res, ensure_ascii=False))
            elif "text" in obj:
                res = run_nl_text(str(obj["text"])[:200])
                res.update({"ts": now_str(), "dna": DNA})
                await ws.send_text(json.dumps(res, ensure_ascii=False))
            else:
                await ws.send_text(json.dumps({"status": "denied", "output": "❌ 不在白名单"}))
    except WebSocketDisconnect:
        pass  # 客户端正常断开
    except Exception as e:
        # 其余异常: 记日志后断开（WebSocketDisconnect 已单独捕获）
        logger.warning("WS连接异常: %s", e)

if __name__ == "__main__":
    os.makedirs(BASE_DIR, exist_ok=True)
    if not TOKEN_FILE.exists():
        subprocess.run(["openssl", "rand", "-hex", "24"],
                       stdout=open(TOKEN_FILE, "w"))
        os.chmod(TOKEN_FILE, 0o600)
        logger.info("已生成新令牌 → %s", TOKEN_FILE)
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="warning")
