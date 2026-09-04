#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
龍魂监管操作捕获中间件
DNA: #龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-REGULATORY-MIDDLEWARE-v1.0

FastAPI 中间件，自动捕获所有 API 操作并写入操作日志。
"""

import time
import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .regulatory_db import log_operation
from .regulatory_service import event_bus

# 不需要记录的路径前缀
SKIP_PATHS = {
    "/api/regulatory/operations/live",
    "/api/regulatory/ws",
    "/api/ws",
    "/api/docs",
    "/api/redoc",
    "/api/openapi.json",
    "/api/system/health",
}


class RegulatoryOperationMiddleware(BaseHTTPMiddleware):
    """自动捕获所有非监管 API 操作。"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # 检查是否需要跳过
        path = request.url.path
        if path in SKIP_PATHS or path.startswith("/api/regulatory"):
            return await call_next(request)
        
        # 获取操作信息
        method = request.method
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent", "")
        
        # 尝试获取用户信息
        operator_uid = "anonymous"
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            try:
                from .auth import decode_jwt
                payload = decode_jwt(auth_header.replace("Bearer ", ""))
                if payload and payload.get("uid"):
                    operator_uid = payload["uid"]
            except Exception:
                pass
        elif "X-Regulatory-Key" in request.headers:
            operator_uid = "REGULATOR"
        
        # 提取请求体（不记录敏感数据）
        body_summary = ""
        if method in ("POST", "PUT", "PATCH"):
            try:
                body = await request.body()
                if body and len(body) < 1024:
                    body_summary = body.decode('utf-8', errors='ignore')[:200]
                elif body:
                    body_summary = f"[{len(body)} bytes]"
            except Exception:
                body_summary = "[无法读取]"
        
        # 执行请求
        response = await call_next(request)
        
        # 计算耗时
        duration_ms = round((time.time() - start_time) * 1000, 2)
        
        # 记录操作
        log_operation(
            op_type=f"api_{method.lower()}",
            source="api_gateway",
            target=path,
            detail=f"{method} {path} → {response.status_code} ({duration_ms}ms)" + 
                    (f" | {body_summary[:100]}" if body_summary else ""),
            operator_uid=operator_uid,
            operator_ip=client_ip,
        )
        
        # 推送到事件总线
        try:
            import asyncio
            loop = asyncio.get_event_loop()
            if loop.is_running():
                event = {
                    "type": "api_call",
                    "method": method,
                    "path": path,
                    "status": response.status_code,
                    "duration_ms": duration_ms,
                    "operator_uid": operator_uid,
                }
                asyncio.run_coroutine_threadsafe(event_bus.publish(event), loop)
        except Exception:
            pass
        
        return response
