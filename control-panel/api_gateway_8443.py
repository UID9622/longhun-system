#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🐉 龍魂 API 网关 · 8443 端口
为 v5 一键启动器提供统一的云端 API 入口
DNA:#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-API-GATEWAY-8443-v1.0
"""

import json
import http.client
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 9622


class GatewayHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # 简化日志输出
        print(f"[API-GW:8443] {self.address_string()} - {format % args}")

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {
                "status": "ok",
                "gateway": "longhun-v5-api-gateway",
                "dna": "#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-API-GATEWAY-8443-v1.0",
                "upstream": f"http://{TARGET_HOST}:{TARGET_PORT}"
            })
            return
        self._proxy("GET")

    def do_HEAD(self):
        if self.path == "/health":
            self._send_json(200, {"status": "ok"})
            return
        self._proxy("HEAD")

    def do_POST(self):
        self._proxy("POST")

    def do_PUT(self):
        self._proxy("PUT")

    def do_DELETE(self):
        self._proxy("DELETE")

    def _send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _proxy(self, method):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else None

            # 转发到 9622
            conn = http.client.HTTPConnection(TARGET_HOST, TARGET_PORT, timeout=10)
            headers = {k: v for k, v in self.headers.items() if k.lower() not in ("host",)}
            conn.request(method, self.path, body=body, headers=headers)
            resp = conn.getresponse()

            self.send_response(resp.status)
            for k, v in resp.getheaders():
                if k.lower() not in ("transfer-encoding", "content-length"):
                    self.send_header(k, v)
            self.send_header("Content-Length", str(resp.length or 0))
            self.end_headers()
            self.wfile.write(resp.read())
            conn.close()
        except Exception as e:
            self._send_json(502, {"error": "upstream failed", "detail": str(e)})


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8443), GatewayHandler)
    print("🐉 龍魂 API 网关已启动: http://0.0.0.0:8443")
    print(f"   上游: http://{TARGET_HOST}:{TARGET_PORT}")
    print("   DNA:#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-API-GATEWAY-8443-v1.0")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[API-GW:8443] 已停止")
