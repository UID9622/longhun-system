#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂通心译后端 · 8777 端口
鸿蒙/手机设备直连翻译引擎
DNA:#龍芯⚡️丙午·丙申·乙卯·辰时·需-TONGXINYI-BACKEND-v1.0
"""

import json
import sys
import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer

# 加载通心译闸门
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "L5_服务层" / "services" / "api" / "control-panel"))
os.chdir(str(ROOT / "L5_服务层" / "services" / "api" / "control-panel"))

from tongxinyi_gate import TongxinyiGate

gate = TongxinyiGate()

class TongxinyiHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[通心译:8777] {self.address_string()} - {format % args}")

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def _send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path == "/health" or self.path == "/api/health":
            self._send_json(200, {
                "status": "ok",
                "service": "longhun-tongxinyi",
                "version": "v1.0",
                "dna": "#龍芯⚡️丙午·丙申·乙卯·辰时·需-TONGXINYI-BACKEND-v1.0",
                "endpoints": ["/api/translate", "/api/cnsh/clipboard-translate", "/health"]
            })
            return
        self._send_json(404, {"error": "not found"})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            data = json.loads(body) if body else {}
        except:
            self._send_json(400, {"error": "无效JSON"})
            return

        if self.path in ("/api/translate", "/api/tongxinyi/translate"):
            text = data.get("text", data.get("q", ""))
            if not text:
                self._send_json(400, {"error": "缺少 text 参数"})
                return
            result = gate.translate(text)
            self._send_json(200, result)
            return

        if self.path == "/api/cnsh/clipboard-translate":
            text = data.get("text", "")
            if not text:
                self._send_json(400, {"error": "缺少 text 参数"})
                return
            result = gate.translate(text)
            self._send_json(200, {
                "original": text,
                "translation": result.get("L5_适配输出", {}).get("five_part_receipt", {}).get("理解", "未解析"),
                "dna": result.get("dna"),
                "audit": result.get("L4_三色审计", {}).get("color"),
                "wuxing": result.get("L2_意图骨架", {}).get("wuxing", {}).get("dominant"),
            })
            return

        self._send_json(404, {"error": "未知端点", "path": self.path})


if __name__ == "__main__":
    PORT = 8777
    HOST = "0.0.0.0"
    server = HTTPServer((HOST, PORT), TongxinyiHandler)
    print(f"🐉 龍魂通心译后端已启动: http://0.0.0.0:{PORT}")
    print(f"   设备入口: http://192.168.1.34:{PORT}")
    print(f"   端点: /api/translate | /api/cnsh/clipboard-translate | /health")
    print(f"   DNA:#龍芯⚡️丙午·丙申·乙卯·辰时·需-TONGXINYI-BACKEND-v1.0")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[通心译:8777] 已停止")
