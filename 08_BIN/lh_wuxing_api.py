#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·五行计算器 HTTP API v1.0（最小闭环）
DNA: #龍芯⚡️2026-09-01-五行计算器API-v1.0-WELD-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

最小闭环 API：复用 lh_wuxing_core 内核，标准库零依赖（http.server）。
按需启动（python3 lh_wuxing_api.py [端口]），测完即停，不常驻。

路由:
  GET /health                                      健康检查
  GET /wuxing?pillars=甲子丙午庚申壬戌             四柱分析 JSON（对接表字段）
  GET /                                            服务说明
"""
import json
import sys
import os
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lh_wuxing_core import 龍魂五行计算器, _扁平节点, _解析四柱

DEFAULT_PORT = 8908


def _四柱_to_json(文本: str) -> dict:
    """解析四柱并返回扁平 JSON（协议§十对接表字段）"""
    字 = _解析四柱(文本)
    if not 字:
        raise ValueError("四柱须为8个字，如: 甲子丙午庚申壬戌")
    return _扁平节点(龍魂五行计算器(*字))


class 五行APIHandler(BaseHTTPRequestHandler):
    server_version = "LongHun-WuxingAPI/1.0"

    def _send(self, code: int, body: dict, ctype: str = "application/json; charset=utf-8"):
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self._send(204, {})

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/health":
            self._send(200, {"status": "ok", "engine": "v4.0", "api": "lh_wuxing_api/v1.0"})
            return
        if path == "/wuxing":
            qs = parse_qs(self.path.split("?", 1)[1] if "?" in self.path else "")
            pillars = (qs.get("pillars", [""])[0] or "").strip()
            if not pillars:
                self._send(400, {"error": "缺少参数 pillars，如 /wuxing?pillars=甲子丙午庚申壬戌"})
                return
            try:
                self._send(200, _四柱_to_json(pillars))
            except ValueError as e:
                self._send(400, {"error": str(e)})
            except Exception as e:  # pragma: no cover
                self._send(500, {"error": f"内部错误: {e}"})
            return
        self._send(200, {
            "service": "龍魂·五行计算器 HTTP API v1.0",
            "engine": "v4.0",
            "routes": {
                "/health": "健康检查",
                "/wuxing?pillars=甲子丙午庚申壬戌": "四柱分析 JSON（node_id/digital_root/element/audit/dna/action/对冲指数H/三色）",
            },
            "usage": "python3 lh_wuxing_api.py 8908",
        })

    def log_message(self, fmt, *args):  # 节能：静默访问日志
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    服务 = HTTPServer(("127.0.0.1", port), 五行APIHandler)
    print(f"🐉 五行计算器 API 已启动: http://127.0.0.1:{port}  (按需使用·Ctrl+C 停止)")
    try:
        服务.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止")
        服务.server_close()


if __name__ == "__main__":
    main()
