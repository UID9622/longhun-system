# -*- coding: utf-8 -*-
# #龍芯⚡️2026-07-03-ENGINE-DEEPSEEK_EXECUTOR-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 DeepSeek 唯一监管加密执行者

职责：
1. 作为龍魂系统对外 API 的唯一入口。
2. 解密外部请求、校验调用者身份、HMAC、时间戳、防重放。
3. 可选地把动作描述送 DeepSeek API 做策略审查。
4. 把合法请求重新加密后转发给龍魂本地网关。
5. 将本地网关的加密响应解密后再加密返回给外部调用者。

监听：127.0.0.1:9453（由 Nginx 反代 /executor/ 到公网）
DNA: #龍芯⚡️20260628-DEEPSEEK-EXECUTOR-v1.0
"""

import hashlib
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import requests
import uvicorn
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from sovereignty.portal.longhun_crypto import (
    LonghunCryptoError,
    NonceCache,
    make_envelope,
    open_envelope,
)

app = FastAPI(title="龍魂 DeepSeek 执行器", version="1.0.0")

# ═══════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
LONGHUN_EXECUTOR_SECRET = os.getenv("LONGHUN_EXECUTOR_SECRET", "")
EXECUTOR_TOKEN = os.getenv("EXECUTOR_TOKEN", "")
LOCAL_GATEWAY_URL = os.getenv("LOCAL_GATEWAY_URL", "http://127.0.0.1:9623/api/secure/execute")
POLICY_CHECK = os.getenv("DEEPSEEK_POLICY_CHECK", "true").lower() in ("1", "true", "yes")
MAX_BODY_SIZE = int(os.getenv("EXECUTOR_MAX_BODY_SIZE", "1048576"))  # 1 MB

LOG_DIR = os.path.expanduser("~/cnsh/logs")
os.makedirs(LOG_DIR, exist_ok=True)

_NONCE_CACHE = NonceCache()


def _dna(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = uuid.uuid4().hex[:12].upper()
    return f"#龍芯⚡️{ts}-{prefix}-{h}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha8(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:8].upper()


def _log(entry: Dict[str, Any]):
    path = os.path.join(LOG_DIR, f"deepseek_executor_{datetime.now(timezone.utc).strftime('%Y%m%d')}.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _verify_caller_token(authorization: Optional[str]) -> bool:
    if not EXECUTOR_TOKEN:
        return False
    if not authorization:
        return False
    scheme, _, token = authorization.partition(" ")
    return scheme.lower() == "bearer" and token == EXECUTOR_TOKEN


def _policy_check(route: str, payload_summary: str, caller: str) -> bool:
    """把动作摘要送 DeepSeek API 做策略审查，返回是否允许。"""
    if not POLICY_CHECK:
        return True
    if not DEEPSEEK_API_KEY:
        # 未配置 Key 时直接允许，避免阻塞
        return True

    prompt = (
        "你是龍魂系统的安全策略审查员。请仅回答 ALLOW 或 DENY，不要解释。\n"
        f"调用者: {caller}\n"
        f"目标路由: {route}\n"
        f"请求摘要: {payload_summary[:200]}\n"
        "判断是否允许执行该操作。若涉及修改宪法、删除审计日志、伪造 DNA、泄露主权数据，请回答 DENY。"
    )
    try:
        r = requests.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 16,
                "temperature": 0.0,
            },
            timeout=15,
        )
        r.raise_for_status()
        answer = r.json()["choices"][0]["message"]["content"].strip().upper()
        return answer.startswith("ALLOW")
    except Exception:
        # 策略服务异常时，按拒绝处理（安全默认）
        return False


# ═══════════════════════════════════════════════════════
# 请求/响应模型
# ═══════════════════════════════════════════════════════
class ExecuteRequest(BaseModel):
    cipher: str = Field(..., description="加密后的请求体")
    hmac: str = Field(..., description="HMAC-SHA256(cipher|ts|nonce)")
    ts: int = Field(..., description="Unix 秒级时间戳")
    nonce: str = Field(..., description="一次性随机串")


class ExecuteResponse(BaseModel):
    cipher: str
    hmac: str
    ts: int
    nonce: str
    dna: str


# ═══════════════════════════════════════════════════════
# 端点
# ═══════════════════════════════════════════════════════
@app.get("/health")
def health():
    deepseek_online = False
    if DEEPSEEK_API_KEY:
        try:
            r = requests.get(
                f"{DEEPSEEK_BASE_URL}/models",
                headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
                timeout=8,
            )
            deepseek_online = r.status_code == 200
        except Exception:
            pass

    return {
        "status": "ok",
        "service": "longhun-deepseek-executor",
        "deepseek_api_online": deepseek_online,
        "policy_check_enabled": POLICY_CHECK,
        "local_gateway": LOCAL_GATEWAY_URL,
        "dna": _dna("EXECUTOR-HEALTH"),
    }


@app.post("/execute", response_model=ExecuteResponse)
def execute(
    body: ExecuteRequest,
    request: Request,
    authorization: Optional[str] = Header(None),
):
    dna = _dna("EXECUTE")
    caller_ip = request.client.host if request.client else "unknown"

    # 1. 调用者身份校验
    if not _verify_caller_token(authorization):
        _log({
            "ts": _now(), "dna": dna, "event": "auth_failed",
            "caller_ip": caller_ip, "tricolor": "🔴",
        })
        raise HTTPException(status_code=403, detail="调用者身份校验失败")

    # 2. 解密并校验外部信封
    try:
        external_payload = open_envelope(body.model_dump(), LONGHUN_EXECUTOR_SECRET, _NONCE_CACHE, ttl=300)
    except LonghunCryptoError as e:
        _log({
            "ts": _now(), "dna": dna, "event": "envelope_open_failed",
            "caller_ip": caller_ip, "error": str(e), "tricolor": "🔴",
        })
        raise HTTPException(status_code=403, detail=f"信封校验失败: {e}")

    route = external_payload.get("route", "")
    internal_payload = external_payload.get("payload", {})

    # 3. DeepSeek 策略审查
    summary = json.dumps(internal_payload, ensure_ascii=False)[:300]
    allowed = _policy_check(route, summary, caller_ip)
    if not allowed:
        _log({
            "ts": _now(), "dna": dna, "event": "policy_denied",
            "caller_ip": caller_ip, "route": route, "tricolor": "🔴",
        })
        raise HTTPException(status_code=403, detail="DeepSeek 策略审查拒绝执行")

    # 4. 重新加密并转发给本地网关
    local_request = {
        "route": route,
        "payload": internal_payload,
        "meta": {
            "caller_ip": caller_ip,
            "executor_dna": dna,
            "ts": _now(),
        },
    }
    local_envelope = make_envelope(local_request, LONGHUN_EXECUTOR_SECRET)

    try:
        r = requests.post(LOCAL_GATEWAY_URL, json=local_envelope, timeout=120)
        r.raise_for_status()
        local_response = r.json()
    except Exception as e:
        _log({
            "ts": _now(), "dna": dna, "event": "local_gateway_error",
            "caller_ip": caller_ip, "route": route, "error": str(e), "tricolor": "🔴",
        })
        raise HTTPException(status_code=502, detail=f"本地网关调用失败: {e}")

    # 5. 解密本地响应，再加密给外部调用者
    try:
        local_plain = open_envelope(local_response, LONGHUN_EXECUTOR_SECRET, _NONCE_CACHE, ttl=300)
    except LonghunCryptoError as e:
        _log({
            "ts": _now(), "dna": dna, "event": "local_response_decrypt_failed",
            "caller_ip": caller_ip, "route": route, "error": str(e), "tricolor": "🔴",
        })
        raise HTTPException(status_code=502, detail=f"本地响应解密失败: {e}")

    external_response_envelope = make_envelope(local_plain, LONGHUN_EXECUTOR_SECRET)

    _log({
        "ts": _now(), "dna": dna, "event": "execute_success",
        "caller_ip": caller_ip, "route": route,
        "tricolor": "🟢", "policy_checked": POLICY_CHECK,
    })

    return ExecuteResponse(
        cipher=external_response_envelope["cipher"],
        hmac=external_response_envelope["hmac"],
        ts=external_response_envelope["ts"],
        nonce=external_response_envelope["nonce"],
        dna=dna,
    )


@app.middleware("http")
async def size_limit(request: Request, call_next):
    if request.method in ("POST", "PUT"):
        content_length = int(request.headers.get("content-length", 0))
        if content_length > MAX_BODY_SIZE:
            return JSONResponse(status_code=413, content={"error": "请求体超过大小限制"})
    return await call_next(request)


if __name__ == "__main__":
    print(f"""
╔════════════════════════════════════════════════════════╗
║  龍魂 DeepSeek 唯一监管加密执行器 v1.0                  ║
║  监听: 127.0.0.1:9453                                  ║
║  本地网关: {LOCAL_GATEWAY_URL:<45} ║
║  策略审查: {'开启' if POLICY_CHECK else '关闭':<18}                  ║
║  DNA: #龍芯⚡️20260628-DEEPSEEK-EXECUTOR-v1.0           ║
╚════════════════════════════════════════════════════════╝
""")
    uvicorn.run(app, host="127.0.0.1", port=9453, log_level="info")
