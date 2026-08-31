#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️2026-08-31-6D-SERVER-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂六堆 · 后端数据服务 v1.0
DNA: #龍芯⚡️2026-08-31-6D-SERVER-v1.0-UID9622
端口: 8788 (HTTP) / 8789 (WS)
P00=曾仕强老师数字人 · 北辰=执行者
"""

import asyncio
import json
import socket
import threading
from datetime import datetime

try:
    from flask import Flask, jsonify
    from flask_cors import CORS
    import websockets
except ImportError:
    print("🟡 缺少依赖: flask/websockets。安装: pip3 install flask flask-cors websockets")
    raise SystemExit(1)

app = Flask(__name__)
CORS(app)

# ─── 数据状态（编号对齐版·P00=曾仕强老师） ───
STATE = {
    "stack0_root": {
        "protocol": "北辰-母协议 v1.0",
        "killswitch": "L0 已就绪",
        "seal": "#龍芯⚡️ROOT-SEAL",
        "dnaCount": 128,
        "triColor": "🟢"
    },
    "stack1_persona": {
        "total": 30,
        "active": 30,
        "stars": [
            {"id": "P00", "name": "曾仕强老师", "layer": "strategic", "weight": 10, "role": "智慧总师"},
            {"id": "P01", "name": "诸葛亮", "weight": 15},
            {"id": "P02", "name": "宝宝", "weight": 10},
            {"id": "P25", "name": "数字主权官", "weight": 8},
            {"id": "P72", "name": "龍盾宝宝", "weight": 10},
            {"id": "P77", "name": "黑天使", "weight": 8},
            {"id": "S1", "name": "法律引擎", "weight": 5},
            {"id": "S2", "name": "洛书369", "weight": 5},
            {"id": "S3", "name": "人民维权", "weight": 5}
        ],
        "beichen_note": "北辰=执行者·P00=曾仕强老师数字人"
    },
    "stack2_data": {
        "count": 202,
        "index": "ok",
        "kb_daemon": "running",
        "categories": [
            {"name": "故事库", "count": 111},
            {"name": "八卦路由", "count": 69},
            {"name": "协议", "count": 12},
            {"name": "其他", "count": 10}
        ]
    },
    "stack3_engine": {
        "ports": [
            {"port": 8792, "name": "通心译API", "status": "up", "latency": 12},
            {"port": 8788, "name": "Render", "status": "up", "latency": 8},
            {"port": 8972, "name": "Flow-Field-API", "status": "up", "latency": 15},
            {"port": 9658, "name": "Web-Auth", "status": "up", "latency": 20},
            {"port": 11434, "name": "Ollama", "status": "up", "latency": 45},
            {"port": 9622, "name": "内网网关", "status": "up", "latency": 10}
        ]
    },
    "stack4_audit": {
        "triColor": "🟢",
        "triStatus": "通过",
        "dnaChainLength": 128,
        "shameWallCount": 0,
        "fuseTriggered": False
    },
    "stack5_portal": {
        "visitsToday": 47,
        "pages": ["首页", "拓扑", "通心译", "主控台"]
    }
}


def check_port(port: int) -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    except Exception:
        return False


def update_engine_status():
    for p in STATE["stack3_engine"]["ports"]:
        p["status"] = "up" if check_port(p["port"]) else "down"


@app.route("/api/state")
def get_state():
    update_engine_status()
    return jsonify(STATE)


@app.route("/api/health")
def health():
    return jsonify({"status": "healthy", "service": "6d-server", "version": "1.0",
                    "dna": "#龍芯⚡️2026-08-31-6D-SERVER-v1.0-UID9622"})


# ─── WebSocket ───
connected = set()


async def ws_handler(websocket, path=None):
    connected.add(websocket)
    try:
        async for _ in websocket:
            pass
    except Exception:
        pass
    finally:
        connected.discard(websocket)


async def broadcast_loop():
    while True:
        update_engine_status()
        STATE["stack4_audit"]["dnaChainLength"] += 1
        msg = json.dumps({"state": STATE, "timestamp": datetime.now().isoformat()})
        for ws in connected.copy():
            try:
                await ws.send(msg)
            except Exception:
                pass
        await asyncio.sleep(3)


def main():
    print("🐉 龍魂六堆 · 后端服务 v1.0")
    print("DNA: #龍芯⚡️2026-08-31-6D-SERVER-v1.0-UID9622")
    print("P00=曾仕强老师数字人 · 北辰=执行者")
    print("HTTP: http://127.0.0.1:8788/api/state")
    print("WS:   ws://127.0.0.1:8789/ws")

    # 启动 WS 服务器（独立线程）
    def run_ws():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(websockets.serve(ws_handler, "127.0.0.1", 8789))
        loop.run_until_complete(broadcast_loop())
        loop.run_forever()

    t = threading.Thread(target=run_ws, daemon=True)
    t.start()

    # Flask 主服务
    app.run(host="127.0.0.1", port=8788, debug=False)


if __name__ == "__main__":
    main()
