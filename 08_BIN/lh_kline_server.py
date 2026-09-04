#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 K线 数据服务 v1.0
DNA: #龍芯⚡️2026-08-31-KLINE-SERVER-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
端口: REST 8899 · WebSocket 8890
功能: 真实数据 REST API + WebSocket 实时推送（龍魂K线行情终端）
安全: 默认绑定 127.0.0.1（对外经 nginx 反代 /api/kline 同源）
"""

import json
import os
import threading
import time
import asyncio
from pathlib import Path

# 双模式导入（包导入 / 直接运行）
if __package__ in (None, ''):
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from lh_kline_fetcher import fetcher, DEFAULT_SYMBOLS
else:
    from .lh_kline_fetcher import fetcher, DEFAULT_SYMBOLS

try:
    from flask import Flask, request, jsonify, send_from_directory
    from flask_cors import CORS
    import websockets
except ImportError as e:
    raise ImportError(f"缺少依赖: {e} → pip3 install flask flask-cors websockets")

# 静态托管 10_PORTAL（kline.html + assets 单端口可用）
PORTAL_DIR = Path(__file__).resolve().parent.parent / "10_PORTAL"
app = Flask(__name__, static_folder=str(PORTAL_DIR), static_url_path="")
CORS(app)

PORT = int(os.environ.get("KLINE_PORT", "8899"))
WS_PORT = int(os.environ.get("KLINE_WS_PORT", "8890"))
HOST = "127.0.0.1"
# 对外经 nginx 反代（uid9622.cn/api/kline → 127.0.0.1:8899），此处不暴露公网


# ─── 静态页面（单端口托管） ───
@app.route("/")
def index():
    return send_from_directory(PORTAL_DIR, "kline.html")


@app.route("/kline.html")
def kline_page():
    return send_from_directory(PORTAL_DIR, "kline.html")


# ─── REST API ───
@app.route("/api/kline/symbols")
def get_symbols():
    return jsonify({
        "symbols": [
            {"id": sid, "name": info["name"], "exchange": info["exchange"]}
            for sid, info in DEFAULT_SYMBOLS.items()
        ]
    })


@app.route("/api/kline/data/<symbol>")
def get_kline_data(symbol):
    """指定标的K线（?days=30 最近N根）"""
    days = request.args.get("days", 60, type=int)
    data = fetcher.fetch(symbol)
    if not data or not data.get("data"):
        return jsonify({"error": "数据获取失败", "symbol": symbol}), 404
    limited = data["data"][-max(1, min(days, 500)):]
    return jsonify({
        "symbol": symbol,
        "name": DEFAULT_SYMBOLS.get(symbol, {}).get("name", symbol),
        "source": data.get("source", "unknown"),
        "last_updated": data.get("last_updated"),
        "count": len(limited),
        "data": limited,
    })


@app.route("/api/kline/all")
def get_all_kline():
    """全部标的概览（?days=1 收盘快照）"""
    days = request.args.get("days", 1, type=int)
    results = {}
    for symbol in DEFAULT_SYMBOLS:
        data = fetcher.fetch(symbol)
        if data and data.get("data"):
            results[symbol] = {
                "name": DEFAULT_SYMBOLS[symbol]["name"],
                "exchange": DEFAULT_SYMBOLS[symbol]["exchange"],
                "source": data.get("source"),
                "last_updated": data.get("last_updated"),
                "data": data["data"][-max(1, min(days, 500)):],
            }
    return jsonify({"count": len(results), "data": results})


@app.route("/api/kline/refresh")
def refresh():
    """强制刷新全部数据"""
    t0 = time.time()
    fetcher.fetch_all()
    return jsonify({"status": "refreshed", "elapsed_s": round(time.time() - t0, 2)})


@app.route("/api/kline/health")
def health():
    return jsonify({"status": "healthy", "service": "kline-server", "port": PORT})


# ─── WebSocket 推送 ───
connected: set = set()


async def ws_handler(websocket, path=None):
    connected.add(websocket)
    try:
        async for message in websocket:
            try:
                msg = json.loads(message)
                symbol = msg.get("symbol")
                if symbol:
                    data = fetcher.fetch(symbol)
                    if data:
                        await websocket.send(json.dumps({
                            "type": "kline", "symbol": symbol,
                            "data": data["data"][-30:],
                            "timestamp": time.time(),
                        }))
            except Exception:
                pass
    finally:
        connected.discard(websocket)


async def broadcast_loop():
    """每 60s 广播最新行情（增量·节约算力）"""
    while True:
        try:
            for symbol in DEFAULT_SYMBOLS:
                data = fetcher.fetch(symbol)
                if data and connected:
                    msg = json.dumps({
                        "type": "update", "symbol": symbol,
                        "data": data["data"][-5:], "timestamp": time.time(),
                    })
                    dead = []
                    for ws in connected:
                        try:
                            await ws.send(msg)
                        except Exception:
                            dead.append(ws)
                    for ws in dead:
                        connected.discard(ws)
            await asyncio.sleep(60)
        except Exception:
            await asyncio.sleep(5)


def run_flask():
    app.run(host=HOST, port=PORT, debug=False, threaded=True)


async def ws_main():
    """WebSocket 常驻：serve + 广播循环（同一事件循环）"""
    async with websockets.serve(ws_handler, HOST, WS_PORT, ping_interval=None):
        await asyncio.gather(broadcast_loop(), asyncio.Future())


if __name__ == "__main__":
    print("🐉 龍魂 K线 数据服务 v1.0")
    print("DNA: #龍芯⚡️2026-08-31-KLINE-SERVER-v1.0-UID9622")
    print("确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    print(f"REST:     http://{HOST}:{PORT}/api/kline/data/sh600036")
    print(f"Symbols:  http://{HOST}:{PORT}/api/kline/symbols")
    print(f"Health:   http://{HOST}:{PORT}/api/kline/health")
    print(f"WebSocket: ws://{HOST}:{WS_PORT}")
    print()
    threading.Thread(target=run_flask, daemon=True).start()
    try:
        asyncio.run(ws_main())
    except KeyboardInterrupt:
        print("已停止")
