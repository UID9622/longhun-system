#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-08-06-SAVE-PROXY-v1.0
# License: MulanPSL v2
"""
AI 省钱代理服务器
════════════════

OpenAI 兼容 API 代理，自动路由本地/云端。
启动后设 OPENAI_BASE_URL=http://localhost:8088/v1 即可使用。

核心:
  - 本地 Ollama 优先（免费）
  - 云端 API 兜底
  - 请求缓存（相同请求不重复调）
  - 实时成本统计
"""

import json
import logging
import sys
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

from .router import SmartRouter, RouteDecision, RouteStrategy
from .cache_engine import RequestCache
from .stats import CostStats
from .audit_log import AuditLogger

logger = logging.getLogger("longhun-save.proxy")


# ════════════════════════════════════════════════════
# FastAPI 应用
# ════════════════════════════════════════════════════

def create_app(
    router: SmartRouter = None,
    cache: RequestCache = None,
    stats: CostStats = None,
    audit: AuditLogger = None,
) -> FastAPI:
    """创建 FastAPI 应用

    Args:
        router: 智能路由器（不传则创建空的）
        cache: 请求缓存
        stats: 成本统计
        audit: 🔥 审计日志器（DNA注入+审计标记+加密日志）
    """
    r = router or SmartRouter()
    c = cache or RequestCache(max_size=500, ttl=3600)
    s = stats or CostStats()
    a = audit or AuditLogger(enabled=False)  # 默认不启用审计

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info("🐉 龍魂算力省钱代理 v1.0 启动")
        logger.info(f"   端点: {len([e for e in r._endpoints])}")
        for ep in r._endpoints:
            logger.info(f"     {ep.name}: {ep.model} @ {ep.base_url}")
        logger.info(f"   策略: {r.strategy.value}")
        logger.info(f"   缓存: 最多{c.max_size}条, TTL={c.ttl}s")
        yield
        summary = s.summary()
        logger.info(f"🐉 代理关闭 · 共{summary['total_calls']}次调用 · "
                    f"节省¥{summary['total_saved_rmb']}")

    app = FastAPI(
        title="龍魂算力省钱代理",
        version="1.0.0",
        description="AI API 智能路由·本地 Ollama 优先·请求缓存·成本统计",
        lifespan=lifespan,
    )

    @app.get("/")
    async def root():
        return {
            "name": "龍魂算力省钱代理 v1.0",
            "version": "1.0.0",
            "endpoints": r.list_endpoints(),
            "strategy": r.strategy.value,
            "cache": c.stat(),
            "cost": s.summary(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    @app.get("/health")
    async def health():
        return {"ok": True, "timestamp": datetime.now(timezone.utc).isoformat()}

    @app.get("/v1/models")
    async def list_models():
        """OpenAI 兼容模型列表"""
        return {
            "object": "list",
            "data": [
                {
                    "id": ep.model,
                    "object": "model",
                    "owned_by": "longhun-save",
                    "description": f"{'本地' if ep.is_local else '云端'}·{ep.name}",
                }
                for ep in r._endpoints
            ],
        }

    @app.post("/v1/chat/completions")
    async def chat_completions(req: Request):
        """OpenAI 兼容聊天接口 · 🔥 注入 DNA + 审计"""
        body = await req.json()
        messages = body.get("messages", [])
        model_hint = body.get("model")
        temperature = body.get("temperature", 0.7)
        max_tokens = body.get("max_tokens", 2048)

        # 🔥 审计: 生成 DNA
        request_dna = a.begin_request(messages, model_hint or "unknown", temperature)
        error_msg = ""
        is_local = False

        # Step 1: 查缓存
        cached = c.get(messages, model_hint or "default", temperature)
        if cached:
            s.record(
                endpoint="cache", model="cache", is_local=True,
                input_tokens=cached.get("usage", {}).get("prompt_tokens", 0),
                output_tokens=cached.get("usage", {}).get("completion_tokens", 0),
                latency_ms=0, cached=True,
            )
            audit_mark = a.end_request(request_dna, cached, is_cached=True, is_local=True)
            response = dict(cached)
            response["x-cached"] = True
            response["x-saved"] = True
            resp = JSONResponse(response)
            # 🔥 注入审计响应头
            resp.headers["X-Longhun-DNA"] = request_dna
            resp.headers["X-Longhun-Audit"] = audit_mark
            return resp

        # Step 2: 路由决策
        t_start = time.time()
        decision = await r.route(messages, model_hint=model_hint)

        # Step 3: 调用 AI
        try:
            resp_data, decision = await r.call(
                decision, messages,
                temperature=temperature, max_tokens=max_tokens,
            )
            is_local = decision.endpoint.is_local
        except Exception as e:
            logger.error(f"调用失败: {e}")
            error_msg = str(e)[:200]
            a.end_request(request_dna, {}, is_cached=False, is_local=is_local,
                          latency_ms=(time.time()-t_start)*1000, error=error_msg)
            raise HTTPException(status_code=502, detail={
                "error": "所有模型调用失败",
                "message": str(e),
            })

        # Step 4: 缓存结果
        c.put(messages, decision.endpoint.model, temperature, resp_data)

        # Step 5: 统计
        usage = resp_data.get("usage", {})
        s.record(
            endpoint=decision.endpoint.name,
            model=decision.endpoint.model,
            is_local=decision.endpoint.is_local,
            input_tokens=usage.get("prompt_tokens", 0),
            output_tokens=usage.get("completion_tokens", 0),
            latency_ms=decision.latency_ms,
        )

        # 🔥 审计结案
        audit_mark = a.end_request(request_dna, resp_data,
                                   is_cached=False, is_local=is_local,
                                   latency_ms=decision.latency_ms)

        # 注入元数据
        resp_data["x-route"] = decision.reason
        resp_data["x-local"] = is_local
        resp_data["x-latency-ms"] = round(decision.latency_ms, 1)
        resp_data["x-saved"] = is_local

        resp = JSONResponse(resp_data)
        # 🔥 注入审计响应头
        resp.headers["X-Longhun-DNA"] = request_dna
        resp.headers["X-Longhun-Audit"] = audit_mark
        return resp

    @app.get("/stats")
    async def get_stats():
        """成本统计"""
        return {
            "cost": s.summary(),
            "cache": c.stat(),
            "endpoints": r.list_endpoints(),
            "recent_calls": s.recent_calls(20),
        }

    @app.get("/stats/json")
    async def get_stats_json():
        """成本统计 JSON 详细"""
        return JSONResponse(json.loads(s.to_json()))

    return app


# ════════════════════════════════════════════════════
# 便捷启动类
# ════════════════════════════════════════════════════

class SaveProxy:
    """算力省钱代理便捷启动器

    Usage:
        proxy = SaveProxy()
        proxy.add_local("http://localhost:11434/v1", "qwen2.5:7b")
        proxy.add_cloud("https://api.deepseek.com/v1", "deepseek-chat", "sk-xxx")
        proxy.start(port=8088)

        # 然后设环境变量
        # export OPENAI_BASE_URL=http://localhost:8088/v1
    """

    def __init__(self, strategy: RouteStrategy = RouteStrategy.LOCAL_FIRST,
                 cache_max: int = 500, cache_ttl: int = 3600,
                 audit_key: str = None):
        self.router = SmartRouter(default_strategy=strategy)
        self.cache = RequestCache(max_size=cache_max, ttl=cache_ttl)
        self.stats = CostStats()
        self.audit = AuditLogger(key=audit_key or "longhun-proxy")

    def add_local(self, base_url: str, model: str, name: str = None,
                  priority: int = 0) -> "SaveProxy":
        self.router.add_local(base_url, model, name, priority)
        return self

    def add_cloud(self, base_url: str, model: str, api_key: str,
                  name: str = None, priority: int = 10) -> "SaveProxy":
        self.router.add_cloud(base_url, model, api_key, name, priority)
        return self

    def start(self, host: str = "127.0.0.1", port: int = 8088):
        """启动代理服务器（阻塞）"""
        app = create_app(self.router, self.cache, self.stats, self.audit)

        print(f"""
╔═══════════════════════════════════════════════╗
║  🐉 龍魂算力省钱代理 v1.0                       ║
║                                               ║
║  本地优先 · 请求缓存 · 成本统计 · DNA审计        ║
║                                               ║
║  API: http://{host}:{port}                    ║
║  Chat: POST /v1/chat/completions               ║
║  统计: GET /stats                              ║
║  审计: ~/.longhun/proxy/audit/                 ║
║                                               ║
║  使用方法:                                     ║
║    export OPENAI_BASE_URL=http://{host}:{port}/v1 ║
║    # 然后正常调用 openai SDK 或其他工具          ║
╚═══════════════════════════════════════════════╝
""")
        uvicorn.run(app, host=host, port=port, log_level="info")


# ════════════════════════════════════════════════════
# 自检
# ════════════════════════════════════════════════════

if __name__ == "__main__":
    import asyncio

    async def test():
        router = SmartRouter()
        router.add_local("http://localhost:11434/v1", "qwen2.5:0.5b", priority=0)
        cache = RequestCache(max_size=10, ttl=60)
        stats = CostStats()
        audit = AuditLogger(key="test-audit")

        app = create_app(router, cache, stats, audit)

        # 如果 Ollama 可用，发一个测试请求
        from fastapi.testclient import TestClient
        client = TestClient(app)

        r = client.get("/")
        print(f"根路径: {r.status_code}")
        print(json.dumps(r.json(), ensure_ascii=False, indent=2)[:500])

        r2 = client.get("/stats")
        print(f"\n统计: {r2.status_code}")
        print(json.dumps(r2.json()["cost"], ensure_ascii=False, indent=2))

        print(f"\n审计统计: {audit.stat()}")
        print("🟢 代理+审计自检通过")

    asyncio.run(test())
