#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·己未·乙亥时·䷒临-API-GATEWAY-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# SPDX-License-Identifier: MulanPSL-2.0
"""
🐉 龍魂 · API网关 v1.0
端口: 8970 (仅绑定 127.0.0.1, 外部唯一入口为 nginx 443)
契约:
  GET /health       → {"status":"ok","service":"api-gateway","dna":...}
  GET /auth/verify  → 验 X-Dragon-DNA 格式: ^#龍芯⚡️ 开头且长度≥20 → 200, 否则 401
                      (供 nginx auth_request 子请求使用; 🟡 HMAC 验签待真机部署密钥后启用)
  其余路径          → 无 X-Dragon-DNA 头 → 403 {"error":"P0协议要求: 缺少DNA追溯码"}
"""

import re
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from lh_audit import CONFIRM, Historian, generate_dna, require_dna

SERVICE = "api-gateway"
DNA_RE = re.compile(r"^#龍芯⚡️")  # DNA 格式前缀


def _normalize_dna(raw: str) -> str:
    """HTTP 头按 latin-1 解码, 中文 DNA 会成 mojibake;
    还原 UTF-8 字节后再做格式校验, 保证真机 curl/浏览器直发也能通过。"""
    try:
        return raw.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return raw

app = FastAPI(title="龍魂API网关", version="1.0.0")


@app.middleware("http")
async def p0_audit_middleware(request: Request, call_next):
    """每请求审计落链; /health 与 /auth/verify 免 DNA 头 (契约豁免)。"""
    path = request.url.path
    if path in ("/health", "/auth/verify"):
        return await call_next(request)
    dna = require_dna(request.headers, SERVICE, path)
    if not dna:
        return JSONResponse(status_code=403,
                            content={"error": "P0协议要求: 缺少DNA追溯码"})
    response = await call_next(request)
    Historian.record("api_request", dna, {
        "path": path,
        "method": request.method,
        "status": response.status_code,
        "client_ip": request.headers.get("x-real-ip")
                     or (request.client.host if request.client else ""),
    }, service=SERVICE)
    return response


@app.get("/health")
async def health():
    return {"status": "ok", "service": SERVICE, "dna": generate_dna("HEALTH")}


@app.get("/auth/verify")
async def auth_verify(request: Request):
    """nginx auth_request 鉴权端点。
    本期校验 DNA 格式与长度; 🟡 HMAC 验签待真机部署共享密钥后启用(修正5)。
    auth_request 只认 2xx=放行 / 401|403=拒绝。
    """
    dna = _normalize_dna(request.headers.get("x-dragon-dna", ""))
    if DNA_RE.match(dna) and len(dna) >= 20:
        return JSONResponse(status_code=200, content={"auth": "ok"})
    Historian.record("auth_reject", dna or "<missing>",
                     {"reason": "dna_format"}, service=SERVICE)
    return JSONResponse(status_code=401, content={"error": "DNA格式校验失败"})


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(request: Request, path: str):
    dna = request.headers.get("x-dragon-dna", "")
    client_ip = request.headers.get("x-real-ip") or \
        (request.client.host if request.client else "")
    return {
        "dna": generate_dna("API"),
        "request_dna": dna,
        "path": path,
        "method": request.method,
        "client_ip": client_ip,
        "timestamp": datetime.now().isoformat(),
        "confirm": CONFIRM,
        "message": "API网关处理完成",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8970)
