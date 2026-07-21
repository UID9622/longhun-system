#!/usr/bin/env python3
"""龍魂·实时看板 API Server
DNA: #龍芯⚡️丙午·辛未·乙酉·申时·小畜-DASHBOARD-API-v1.0
端口: 19628
"""

import json, time, subprocess, threading
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse
import asyncio, os

app = FastAPI(title="龍魂·实时看板API", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

HTML_FILE = os.path.join(os.path.dirname(__file__), "lh_dashboard.html")

SSH_KEY = os.path.expanduser("~/.ssh/longhun_kunpeng_ed25519")
KP_HOST = "root@119.13.90.27"
SSH_BASE = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=8", KP_HOST]

# === 缓存 ===
_cache = {"mac": {}, "kp": {}, "ts": 0}
_lock = threading.Lock()

def _ssh(cmd: str) -> str:
    try:
        r = subprocess.run(SSH_BASE + [cmd], capture_output=True, text=True, timeout=12)
        return r.stdout.strip()
    except:
        return ""

def _run(cmd: list) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
        return r.stdout.strip()
    except:
        return ""

def _curl(url: str, is_kp: bool = False) -> str:
    if is_kp:
        return _ssh(f"curl -s --connect-timeout 5 {url}")
    try:
        r = subprocess.run(["curl", "-s", "--connect-timeout", "5", url], capture_output=True, text=True, timeout=8)
        return r.stdout.strip()
    except:
        return ""

# ====== 数据采集 ======

def collect_all():
    """采集所有实时数据"""
    data = {
        "ts": int(time.time()),
        "cst": datetime.now().strftime("%H:%M:%S"),
        "mac": collect_mac(),
        "kp": collect_kp(),
        "frp_status": check_frp(),
    }
    with _lock:
        _cache.update(data)
    return data

def collect_mac():
    d = {}
    # uptime
    out = _run(["uptime"])
    d["uptime"] = out
    # load
    try:
        import os
        l = os.getloadavg()
        d["load"] = {"1min": round(l[0],2), "5min": round(l[1],2), "15min": round(l[2],2)}
    except:
        d["load"] = {"1min":0,"5min":0,"15min":0}
    # disk
    out = _run(["df", "-h", "/"])
    lines = out.strip().split("\n")
    if len(lines) > 1:
        parts = lines[1].split()
        d["disk"] = {"total": parts[1], "used": parts[2], "avail": parts[3], "pct": parts[4]}
    # mem
    out = _run(["vm_stat"])
    d["mem_raw"] = out[:200]
    # services
    d["services"] = {}
    for name, url in [
        ("dashboard", "http://localhost:9627/health"),
        ("registry", "http://localhost:9623/health"),
        ("autoflow", "http://localhost:8766/health"),
        ("ollama_proxy", "http://localhost:11435/api/tags"),
    ]:
        r = _curl(url)
        d["services"][name] = "up" if r and "error" not in r.lower()[:30] else "down"
    # launchd tunnel
    out = _run(["launchctl", "list"])
    d["tunnel_guard"] = "up" if "longhun.kunpeng-tunnel" in out else "down"
    # frp_port_script
    try:
        body = subprocess.run(["cat", os.path.expanduser("~/.longhun/logs/frp_port_open.log")],
            capture_output=True, text=True, timeout=2).stdout
        lines_log = body.strip().split("\n")
        last = lines_log[-1] if lines_log else ""
        if "完成" in last:
            d["frp_port_script"] = "done"
        elif "還鎖著" in last:
            n = last.count("嘗試") if "嘗試" in last else 0
            d["frp_port_script"] = f"trying(#{n})"
        else:
            d["frp_port_script"] = "idle"
    except:
        d["frp_port_script"] = "unknown"
    return d

def collect_kp():
    d = {}
    # uptime
    d["uptime"] = _ssh("uptime")
    # load
    out = _ssh("cat /proc/loadavg")
    if out:
        parts = out.split()
        d["load"] = {"1min": round(float(parts[0]),2), "5min": round(float(parts[1]),2), "15min": round(float(parts[2]),2)}
    else:
        d["load"] = {"1min":0,"5min":0,"15min":0}
    # cpu
    out = _ssh("top -bn1 | grep 'Cpu'")
    idle = "100"
    if out:
        for token in out.split(","):
            if "id" in token:
                idle = token.strip().split()[0]
    d["cpu_idle"] = idle
    # mem
    out = _ssh("free -h | grep Mem")
    d["mem"] = out
    # disk
    out = _ssh("df -h / | tail -1")
    if out:
        parts = out.split()
        d["disk"] = {"total": parts[1], "used": parts[2], "avail": parts[3], "pct": parts[4]}
    # services
    d["services"] = {}
    for name, cmd in [
        ("frps", "systemctl is-active frps"),
        ("ollama", "curl -s --connect-timeout 3 http://localhost:11434/api/tags | grep -c models"),
        ("dashboard", "ss -tlnp | grep -c 9627"),
        ("registry", "ss -tlnp | grep -c 9623"),
        ("tunnel_in", "ss -tlnp | grep -c 19623"),
    ]:
        out = _ssh(cmd)
        d["services"][name] = "up" if out.strip() in ["active", "1", "4"] or (out.strip().isdigit() and int(out.strip()) > 0) else "down"
    # models
    out = _ssh("curl -s --connect-timeout 3 http://localhost:11434/api/tags 2>/dev/null")
    try:
        models = json.loads(out).get("models", [])
        d["models"] = [m["name"] for m in models]
    except:
        d["models"] = []
    # docker
    out = _ssh("docker ps --format '{{.Names}} {{.Status}}' 2>/dev/null")
    d["containers"] = out.split("\n") if out else []
    return d

def check_frp():
    """检查FRP连通状态"""
    # 鲲鹏上7000端口
    kp_7000 = _ssh("ss -tlnp | grep ':7000' | wc -l")
    # Mac上能否连鲲鹏7000
    try:
        r = subprocess.run(["nc", "-z", "-w", "5", "119.13.90.27", "7000"], capture_output=True, timeout=8)
        mac_to_7000 = r.returncode == 0
    except:
        mac_to_7000 = False
    return {
        "kp_port_7000": kp_7000.strip() if kp_7000 else "0",
        "mac_to_kp_7000": mac_to_7000,
        "ssh_tunnel": "active"
    }

# ====== API 端点 ======

@app.get("/")
def index():
    if os.path.exists(HTML_FILE):
        with open(HTML_FILE, 'r') as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1 style='color:gold;text-align:center;margin-top:100px'>🐉 龍魂大屏文件未找到</h1>")

@app.get("/api/health")
def health():
    return {"status": "龍魂·实时看板 v1.0", "dna": "#龍芯⚡️丙午·辛未·乙酉·申时·小畜-DASHBOARD-API-v1.0"}

@app.get("/api/status")
def status():
    return collect_all()

@app.get("/api/stream")
async def stream():
    """SSE 实时推送"""
    async def gen():
        while True:
            data = collect_all()
            yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
            await asyncio.sleep(2)
    return StreamingResponse(gen(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    print("🚀 龍魂·实时看板API 启动 :19628")
    uvicorn.run(app, host="0.0.0.0", port=19628, log_level="info")
