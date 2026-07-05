# -*- coding: utf-8 -*-
# #龍芯⚡️2026-07-03-ENGINE-LOCAL_SECURE_GATEWAY-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂本地安全网关（轻量版）

仅暴露 /api/secure/*，接收来自 DeepSeek 执行器的加密请求，
解密后调用本地模型路由或简单派发，然后把响应加密返回。

监听：127.0.0.1:9622
DNA: #龍芯⚡️20260628-LOCAL-SECURE-GATEWAY-v1.0
"""

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from sovereignty.portal import model_router
from sovereignty.portal.longhun_crypto import (
    LonghunCryptoError,
    NonceCache,
    make_envelope,
    open_envelope,
)

app = FastAPI(title="龍魂本地安全网关", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

LONGHUN_EXECUTOR_SECRET = os.getenv("LONGHUN_EXECUTOR_SECRET", "")
_NONCE_CACHE = NonceCache()
LOG_DIR = Path.home() / "cnsh" / "logs"


def _dna(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = uuid.uuid4().hex[:12].upper()
    return f"#龍芯⚡️{ts}-{prefix}-{h}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _log(entry: Dict[str, Any]):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    path = LOG_DIR / f"longhun_secure_{datetime.now(timezone.utc).strftime('%Y%m%d')}.jsonl"
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


@app.get("/api/secure/health")
def secure_health():
    return {
        "状态": "ok",
        "channel": "secure",
        "secret_configured": bool(LONGHUN_EXECUTOR_SECRET),
        "dna": _dna("SECURE-HEALTH"),
    }


@app.post("/api/secure/execute")
async def secure_execute(request: Request):
    dna = _dna("SECURE-EXECUTE")
    client_host = request.client.host if request.client else "unknown"

    if not LONGHUN_EXECUTOR_SECRET:
        _log({"ts": _now(), "dna": dna, "event": "secret_missing", "tricolor": "🔴"})
        raise HTTPException(status_code=503, detail="执行器密钥未配置")

    try:
        envelope = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="请求体不是有效 JSON")

    try:
        plain = open_envelope(envelope, LONGHUN_EXECUTOR_SECRET, _NONCE_CACHE, ttl=300)
    except LonghunCryptoError as e:
        _log({
            "ts": _now(), "dna": dna, "event": "envelope_verify_failed",
            "client": client_host, "error": str(e), "tricolor": "🔴",
        })
        raise HTTPException(status_code=403, detail=f"信封校验失败: {e}")

    route = plain.get("route", "")
    payload = plain.get("payload", {})
    meta = plain.get("meta", {})

    result = {}
    tricolor = "🟢"

    try:
        if route == "echo":
            result = {"echo": payload}
        elif route == "chat":
            chat_req = model_router.ChatRequest(**payload)
            result = model_router.chat(chat_req)
        elif route == "models":
            result = model_router.list_models()
        else:
            raise ValueError(f"未知 route: {route}")
    except Exception as e:
        tricolor = "🔴"
        result = {"error": str(e)}

    _log({
        "ts": _now(), "dna": dna, "event": "secure_execute",
        "client": client_host, "route": route,
        "executor_dna": meta.get("executor_dna"),
        "tricolor": tricolor,
    })

    response_payload = {
        "status": "ok" if tricolor == "🟢" else "error",
        "route": route,
        "result": result,
        "dna": dna,
        "ts": _now(),
    }
    return make_envelope(response_payload, LONGHUN_EXECUTOR_SECRET)


if __name__ == "__main__":
    print(f"""
╔════════════════════════════════════════════════════════╗
║  龍魂本地安全网关 v1.0                                  ║
║  监听: 127.0.0.1:9623                                  ║
║  仅接受来自 DeepSeek 执行器的加密请求                   ║
║  DNA: #龍芯⚡️20260628-LOCAL-SECURE-GATEWAY-v1.0        ║
╚════════════════════════════════════════════════════════╝
""")
    uvicorn.run(app, host="127.0.0.1", port=9623, log_level="info")
