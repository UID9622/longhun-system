#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬申·亥时·䷕贲-OVERSEAS-AI-GATEWAY-v1.0-9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
龍魂海外节点 · AI 网关 v1.0（OpenAI-compatible 转发）
======================================================
海外节点统一 AI 入口：海外业务把 OPENAI_BASE_URL 指向本网关，
按模型名自动路由到 OpenAI / Claude(Anthropic) / Google Gemini，
对上层业务完全透明。

  POST /v1/chat/completions   聊天补全（OpenAI 兼容格式）
  GET  /health                健康检查
  鉴权  : Authorization: Bearer <LONGHUN_GATEWAY_KEY> 或 X-API-Key

环境变量（ai-gateway/.env）：
  LONGHUN_GATEWAY_KEY   网关自己的钥匙（必填）
  OPENAI_API_KEY        OpenAI key（模型名不含 claude/gemini 时用）
  ANTHROPIC_API_KEY     Claude key（模型名含 claude 时用）
  GEMINI_API_KEY        Gemini key（模型名含 gemini 时用）
  GATEWAY_PORT          监听端口（默认 8788）
  OPENAI_BASE_URL       可覆盖 OpenAI 兼容端点（默认 https://api.openai.com/v1）

一国一微调：海外节点只服务海外业务；密钥只存节点 .env（0600），不入 git。
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ---------- 环境 ----------
def load_env(path: str) -> None:
    if not os.path.exists(path):
        return
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

load_env(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

GATEWAY_KEY = os.environ.get("LONGHUN_GATEWAY_KEY", "")
PORT = int(os.environ.get("GATEWAY_PORT", "8788"))
OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
OPENAI_BASE = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/openai"
ANTHROPIC_BASE = "https://api.anthropic.com/v1"

LOG_FILE = "/var/log/longhun/ai-gateway.log"


def log(msg: str) -> None:
    line = f"[{datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}] {msg}"
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
    print(line)


def route_for(model: str) -> tuple:
    """返回 (upstream_base, auth_header)"""
    m = model.lower()
    if "claude" in m:
        return (ANTHROPIC_BASE, f"x-api-key: {ANTHROPIC_KEY}")
    if "gemini" in m:
        return (GEMINI_BASE, f"Authorization: Bearer {GEMINI_KEY}")
    return (OPENAI_BASE, f"Authorization: Bearer {OPENAI_KEY}")


def forward(body: bytes, model: str) -> tuple:
    base, auth = route_for(model)
    url = f"{base}/chat/completions"
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", auth.split(": ", 1)[1])
    if "x-api-key" in auth:
        req.add_header("x-api-key", auth.split(": ", 1)[1])
        req.add_header("anthropic-version", "2023-06-01")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
            code = resp.status
    except urllib.error.HTTPError as e:
        data = e.read()
        code = e.code
    except Exception as e:
        log(f"FORWARD ERROR model={model} err={e}")
        return (502, json.dumps({"error": {"message": str(e)}}).encode())
    log(f"FORWARD model={model} code={code} ms={int((time.time()-t0)*1000)}")
    return (code, data)


class Handler(BaseHTTPRequestHandler):
    server_version = "LonghunOverseas/1.0"

    def _check_auth(self) -> bool:
        if not GATEWAY_KEY:
            return True  # 未配网关钥匙时放行（部署向导阶段）
        key = self.headers.get("X-API-Key") or ""
        auth = self.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            key = auth[len("Bearer "):].strip()
        return key == GATEWAY_KEY

    def _send(self, code: int, body: bytes, ctype: str = "application/json") -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, json.dumps({
                "status": "ok", "node": "overseas",
                "upstreams": {
                    "openai": bool(OPENAI_KEY), "claude": bool(ANTHROPIC_KEY),
                    "gemini": bool(GEMINI_KEY),
                },
                "time": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            }, ensure_ascii=False).encode())
            return
        self._send(404, b'{"error":"not found"}')

    def do_POST(self):
        if self.path not in ("/v1/chat/completions", "/chat/completions"):
            self._send(404, b'{"error":"not found"}')
            return
        if not self._check_auth():
            log("AUTH FAIL 401")
            self._send(401, b'{"error":{"message":"invalid gateway key"}}')
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length)
            payload = json.loads(body.decode("utf-8"))
            model = payload.get("model", "")
        except Exception as e:
            self._send(400, json.dumps({"error": {"message": f"bad request: {e}"}}).encode())
            return
        code, resp = forward(body, model)
        self._send(code, resp)

    def log_message(self, fmt, *args):
        pass  # 走自建 log()，避免刷屏


def main():
    if not GATEWAY_KEY:
        log("⚠️ 未配置 LONGHUN_GATEWAY_KEY（请编辑 ai-gateway/.env）")
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    log(f"🟢 龍魂海外 AI 网关 v1.0 已启动 :{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("⬛ 网关停止")
        server.shutdown()


if __name__ == "__main__":
    sys.exit(main())
