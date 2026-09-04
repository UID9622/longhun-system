#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════════════════════
# 龍魂体系 | 观澜引擎 M1 最小端点 v1.0
# ═══════════════════════════════════════════════════════════
# 一句话：观澜引擎 M1 里程碑 — 空壳端点，透传Ollama本地模型
#   未来 M2-M5 逐步加载 分析/预测/推荐/可视化 能力
# ═══════════════════════════════════════════════════════════
# DNA: #龍芯⚡️丙午·乙未·壬戌·丙午·䷕贲-觀-GUANLAN-M1-v1.0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════════
#
# 端点:
#   GET  /health                    — 健康检查 + Ollama连接状态
#   POST /chat                      — 透传到 Ollama :11434
#   POST /chat/stream               — 流式透传 (SSE)
#   GET  /status                    — 引擎状态 (M1标记)
#
# 请求格式:
#   {"query": "...", "persona_code": "...", "route_id": "...", "format": "v2"}
#
# M1 说明:
#   - 不加载任何分析模型
#   - 纯透传网关模式
#   - 预留 M2-M5 扩展接口
#   - 支持 8799 枢纽降级链接入
# ═══════════════════════════════════════════════════════════
"""

import sys
import os
import json
import time
import socket
import hashlib
import threading
from datetime import datetime, timezone, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from typing import Any, Dict, List, Optional, Tuple

# ── 项目路径 ──
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

# ═══════════════════════════════════════════════════════════
# 焊死常量
# ═══════════════════════════════════════════════════════════

PORT = 8770
HOST = "127.0.0.1"
VERSION = "M1-1.0.0"
DNA = "#龍芯⚡️丙午·乙未·壬戌·丙午·䷕贲-觀-GUANLAN-M1-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CST = timezone(timedelta(hours=8))

# ── M1 后端配置 ──
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "longhun-v3.7"
OLLAMA_TIMEOUT = 30

START_TIME = time.time()
AUDIT_LOCK = threading.Lock()
AUDIT_LOG: List[Dict[str, Any]] = []


def _audit(action: str, result: str, detail: str = "", color: str = "🟢") -> None:
    entry = {
        "time": datetime.now(CST).isoformat(),
        "action": action,
        "result": result,
        "detail": detail,
        "audit_mark": color,
        "dna": DNA,
    }
    with AUDIT_LOCK:
        AUDIT_LOG.append(entry)


def check_ollama() -> Tuple[bool, str]:
    """检查 Ollama 是否存活"""
    import urllib.request
    import urllib.error
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=2) as resp:
            if resp.status == 200:
                return (True, f"Ollama OK (HTTP 200)")
            return (False, f"Ollama HTTP {resp.status}")
    except Exception as e:
        return (False, f"Ollama unreachable: {e}")


# ═══════════════════════════════════════════════════════════
# HTTP 服务器
# ═══════════════════════════════════════════════════════════

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()


class GuanLanHandler(BaseHTTPRequestHandler):
    """观澜 M1 HTTP 处理器"""

    def _send_json(self, data: Dict[str, Any], status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("X-GuanLan", "M1-engines/guanlan")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw)

    def do_OPTIONS(self) -> None:
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-DNA-Token")
        self.end_headers()

    def do_GET(self) -> None:
        path = urlparse(self.path).path

        if path == "/health":
            ollama_ok, ollama_msg = check_ollama()
            self._send_json({
                "status": "ok",
                "service": "guanlan_engine",
                "milestone": "M1",
                "version": VERSION,
                "dna": DNA,
                "ollama": ollama_msg,
                "ollama_ok": ollama_ok,
                "uptime": time.time() - START_TIME,
                "audit_log_count": len(AUDIT_LOG),
            })

        elif path == "/status":
            self._send_json({
                "service": "guanlan_engine",
                "milestone": "M1",
                "version": VERSION,
                "capabilities": ["passthrough", "health", "audit"],
                "planned_milestones": {
                    "M2": "text_analysis",
                    "M3": "prediction",
                    "M4": "recommendation",
                    "M5": "visualization",
                },
                "dna": DNA,
                "confirm": CONFIRM,
            })

        else:
            self._send_json({"error": "not found", "path": path}, 404)

    def do_POST(self) -> None:
        path = urlparse(self.path).path

        if path == "/chat":
            try:
                payload = self._read_body()
            except json.JSONDecodeError:
                self._send_json({"error": "invalid json body"}, 400)
                return

            query = payload.get("query", "")
            if not query:
                self._send_json({"error": "missing 'query' field"}, 400)
                return

            # M1: 透传到 Ollama
            import urllib.request
            import urllib.error

            ollama_body = json.dumps({
                "model": OLLAMA_MODEL,
                "prompt": query,
                "stream": False,
            }).encode("utf-8")

            req = urllib.request.Request(
                OLLAMA_URL,
                data=ollama_body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            try:
                with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as resp:
                    raw = resp.read().decode("utf-8")
                    data = json.loads(raw)
                    answer = data.get("response", "") or data.get("text", "")
                    _audit("chat", "ok", f"query_hash={hashlib.sha256(query.encode()).hexdigest()[:16]}")
                    self._send_json({
                        "answer": answer,
                        "model": OLLAMA_MODEL,
                        "backend": "ollama_passthrough",
                        "milestone": "M1",
                        "dna": DNA,
                        "audit_mark": "🟢",
                    })
            except urllib.error.URLError as e:
                _audit("chat", "fail", f"Ollama error: {e.reason}", "🔴")
                self._send_json({
                    "answer": f"观澜M1: Ollama连接失败 ({e.reason})",
                    "backend": "none",
                    "milestone": "M1",
                    "dna": DNA,
                    "audit_mark": "🔴",
                }, 503)

        else:
            self._send_json({"error": "not found", "path": path}, 404)

    def log_message(self, format: str, *args: Any) -> None:
        pass


# ═══════════════════════════════════════════════════════════
# 主函数
# ═══════════════════════════════════════════════════════════

def main() -> None:
    print("═" * 56)
    print("🌊 观澜引擎 M1 最小端点 v1.0")
    print(f"🔗 http://{HOST}:{PORT}")
    print(f"🧬 {DNA}")
    print(f"📌 M1: 透传模式 (Passthrough)")
    print("═" * 56)

    # 启动 QuickCheck
    print("\n🔬 M1 QuickCheck:")
    ollama_ok, ollama_msg = check_ollama()
    print(f"    {'🟢' if ollama_ok else '🔴'} {ollama_msg}")

    server = ReusableHTTPServer((HOST, PORT), GuanLanHandler)
    print(f"\n🚀 监听 {HOST}:{PORT} ...\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 观澜 M1 关闭")
        server.shutdown()


if __name__ == "__main__":
    main()
