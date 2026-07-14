#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂能力展示官网 · 本地 Web 服务
DNA:#龍芯⚡️2026-06-28-LONGHUN-CAPABILITY-WEB-FILE1-v1.0

提供能力清单展示、规则覆盖状态、训练状态监控。
"""
import json
import os
import sys
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import Config
from registry import CapabilityRegistry
from train_pipeline import TrainPipeline


WEB_ROOT = Config.project_root / "web"
PORT = 8844


class CapabilityHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_ROOT), **kwargs)

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/api/registry":
            self._send_json(CapabilityRegistry().data)
        elif self.path == "/api/stats":
            self._send_json(CapabilityRegistry().get_stats())
        elif self.path == "/api/train/status":
            self._send_json(TrainPipeline().status())
        else:
            super().do_GET()

    def _send_json(self, data):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    server = HTTPServer(("127.0.0.1", PORT), CapabilityHandler)
    print(f"🐉 龍魂能力展示官网已启动: http://127.0.0.1:{PORT}/")
    print(f"   DNA: #龍芯⚡️2026-06-28-LONGHUN-CAPABILITY-WEB-v1.0")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止")


if __name__ == "__main__":
    main()
