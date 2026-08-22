#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════════════════════
# 龍魂体系 | 小艺调度枢纽 8799 端点 v1.0
# ═══════════════════════════════════════════════════════════
# 一句话：宝宝中枢四引擎融合后的唯一AI问答入口
#   接收 /hub/ask → 智能降级 9622→8765→11434 → 返回聚合结果
# ═══════════════════════════════════════════════════════════
# DNA: #龍芯⚡️丙午·乙未·壬戌·丙午·䷂屯-XIAOYI-HUB-8799-v1.0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════════
#
# 端点:
#   GET  /health                    — 健康检查 + 所有后端状态
#   POST /hub/ask                   — 统一问答入口 (v2格式)
#   GET  /hub/status                — 详细状态报告
#
# 请求格式 (v2 unified, aligned with 小艺调度枢纽方案 §3.3):
#   {
#     "query": "...",
#     "persona_code": "...",        // 调用方标识
#     "route_id": "...",            // 路由追踪ID
#     "timestamp": "ISO8601",
#     "model_route": "fallback_chain" | "force:9622" | "force:ollama",
#     "format": "v2"
#   }
#
# 响应格式 (§3.3):
#   {
#     "answer": "...",
#     "backend": "9622操作台",
#     "route_trace": ["8799→9622"],
#     "dna": "...",
#     "audit_mark": "🟢"
#   }
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
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

# ═══════════════════════════════════════════════════════════
# 焊死常量
# ═══════════════════════════════════════════════════════════

PORT = 18899
HOST = "127.0.0.1"
VERSION = "1.0.1"
DNA = "#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-XIAOYI-HUB-v1.0-UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CST = timezone(timedelta(hours=8))

# ── 后端降级链（有序）──
# 修复：Ollama 实际端口为 11434；v2 桥接在 18799；避免 8799/9622 冲突。
BACKENDS: List[Dict[str, Any]] = [
    {
        "name": "18799龍魂桥接",
        "url": "http://localhost:18799/api/v1/chat",
        "health_url": "http://localhost:18799/api/v1/xiaoyi/health",
        "timeout": 60,
    },
    {
        "name": "Ollama本地",
        "url": "http://localhost:11434/api/generate",
        "health_url": "http://localhost:11434/api/tags",
        "timeout": 60,
        "ollama_format": True,
    },
]

# ── 一票否决词 ──
VETO_WORDS = [
    "技术无国界", "用户体验优先", "灵活处理", "国际接轨",
    "简化管理", "商业化需要", "平衡各方", "行业标准",
]
ETHICAL_FUSE = ["儿童", "未成年", "幼女", "少儿"]

# ── 审计日志（线程安全）──
AUDIT_LOG: List[Dict[str, Any]] = []
AUDIT_LOCK = threading.Lock()


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


def detect_veto(text: str) -> Optional[str]:
    for w in ETHICAL_FUSE:
        if w in text:
            return f"🔴 L0伦理熔断: 涉「{w}」"
    for w in VETO_WORDS:
        if w in text:
            return f"🔴 一票否决词触发: 「{w}」"
    return None


def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


# ═══════════════════════════════════════════════════════════
# 降级链执行器
# ═══════════════════════════════════════════════════════════

def _forward_to_backend(
    backend: Dict[str, Any], payload: Dict[str, Any]
) -> Tuple[bool, Optional[str], str]:
    """向单个后端转发请求，返回 (成功, 答案, trace_info)"""
    import urllib.request
    import urllib.error

    query = payload.get("query", "")
    name = backend["name"]
    url = backend["url"]
    timeout = backend.get("timeout", 15)

    if backend.get("ollama_format"):
        body = json.dumps({
            "model": "qwen2.5:1.5b",
            "prompt": query,
            "stream": False,
        }).encode("utf-8")
    else:
        body = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-DNA-Token": "LONGHUN-XIAOYI-HUB-8799-v1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            status = resp.status

            if status == 200:
                answer = (
                    data.get("answer")
                    or data.get("response")
                    or data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    or data.get("text", "")
                    or json.dumps(data, ensure_ascii=False)
                )
                return (True, answer, f"{name}(HTTP 200)")
            else:
                return (False, None, f"{name}(HTTP {status})")

    except urllib.error.URLError as e:
        return (False, None, f"{name}(URLError: {e.reason})")
    except Exception as e:
        return (False, None, f"{name}({type(e).__name__}: {e})")


def execute_fallback(payload: Dict[str, Any]) -> Dict[str, Any]:
    """执行完整降级链，返回聚合响应"""
    query = payload.get("query", "")
    route_trace: List[str] = []

    for backend in BACKENDS:
        ok, answer, trace = _forward_to_backend(backend, payload)
        route_trace.append(trace)
        if ok and answer:
            _audit("ask", "ok", f"query_hash={compute_hash(query)} backend={backend['name']}")
            return {
                "answer": answer,
                "backend": backend["name"],
                "route_trace": route_trace,
                "dna": DNA,
                "audit_mark": "🟢",
                "query_hash": compute_hash(query),
            }

    _audit("ask", "fail", f"query_hash={compute_hash(query)} all_backends_failed", "🔴")
    return {
        "answer": "所有后端均不可用。请检查 9622操作台 / 8765GPT / Ollama 服务状态。",
        "backend": "none",
        "route_trace": route_trace,
        "dna": DNA,
        "audit_mark": "🔴",
        "query_hash": compute_hash(query),
    }


def health_check_backend(url: str, timeout: int = 1) -> bool:
    """快速检查某后端是否存活"""
    import urllib.request
    import urllib.error
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout):
            return True
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════
# HTTP 请求处理器
# ═══════════════════════════════════════════════════════════

class ReusableHTTPServer(HTTPServer):
    """支持 SO_REUSEADDR 的 HTTPServer"""
    allow_reuse_address = True

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()


class HubHandler(BaseHTTPRequestHandler):
    """8799 枢纽 HTTP 处理器"""

    def _send_json(self, data: Dict[str, Any], status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("X-DNA", "LONGHUN-XIAOYI-HUB-8799-v1.0")
        self.send_header("X-DNA-Full", DNA.encode("utf-8").hex())
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
            backends_status = {}
            for b in BACKENDS:
                backends_status[b["name"]] = "🟢" if health_check_backend(b["health_url"]) else "🔴"

            self._send_json({
                "status": "ok",
                "service": "xiaoyi_hub_8799",
                "version": VERSION,
                "dna": DNA,
                "backends": backends_status,
                "audit_log_count": len(AUDIT_LOG),
                "uptime": time.time() - START_TIME,
            })

        elif path == "/hub/status":
            self._send_json({
                "service": "xiaoyi_hub_8799",
                "version": VERSION,
                "dna": DNA,
                "confirm": CONFIRM,
                "port": PORT,
                "backends": [b["name"] for b in BACKENDS],
                "audit_log_entries": len(AUDIT_LOG),
                "veto_words_count": len(VETO_WORDS),
                "ethical_fuse_count": len(ETHICAL_FUSE),
            })

        else:
            self._send_json({"error": "not found"}, 404)

    def do_POST(self) -> None:
        path = urlparse(self.path).path

        if path == "/hub/ask":
            try:
                payload = self._read_body()
            except json.JSONDecodeError:
                self._send_json({"error": "invalid json body"}, 400)
                return

            query = payload.get("query", "")
            if not query:
                self._send_json({"error": "missing 'query' field"}, 400)
                return

            # 一票否决词检测
            veto = detect_veto(query)
            if veto:
                _audit("ask", "veto", veto, "🔴")
                self._send_json({
                    "answer": veto,
                    "backend": "veto_fuse",
                    "route_trace": ["8799→熔断"],
                    "dna": DNA,
                    "audit_mark": "🔴",
                }, 403)
                return

            # 执行降级链
            result = execute_fallback(payload)
            status_code = 200 if result["audit_mark"] == "🟢" else 503
            self._send_json(result, status_code)

        else:
            self._send_json({"error": "not found"}, 404)

    def log_message(self, format: str, *args: Any) -> None:
        pass  # 禁用默认 stderr 日志，改用审计体系


# ═══════════════════════════════════════════════════════════
# 主函数
# ═══════════════════════════════════════════════════════════

START_TIME = time.time()


def main() -> None:
    print("═" * 56)
    print("🐉 小艺调度枢纽 8799 端点 v1.0")
    print(f"🔗 http://{HOST}:{PORT}")
    print(f"🧬 {DNA}")
    print(f"✅ {CONFIRM}")
    print("═" * 56)

    # 启动时 QuickCheck 所有后端
    print("\n🔬 启动 QuickCheck:")
    for b in BACKENDS:
        ok = health_check_backend(b["health_url"])
        print(f"    {'🟢' if ok else '🔴'} {b['name']} ({b['health_url']})")

    # 允许端口复用 (SO_REUSEADDR)
    server = ReusableHTTPServer((HOST, PORT), HubHandler)
    print(f"\n🚀 监听 {HOST}:{PORT} ...\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 枢纽关闭")
        server.shutdown()


if __name__ == "__main__":
    main()
