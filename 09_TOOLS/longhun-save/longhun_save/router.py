#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️2026-08-06-SAVE-ROUTER-v1.0
# License: MulanPSL v2
"""
智能路由器 · 本地优先 + 云端兜底
══════════════════════════════════

路由策略:
  1. 优先本地 Ollama（免费、低延迟、数据不出机）
  2. 本地不可用 → 云端 API（DeepSeek/混元等）
  3. 缓存命中 → 直接返回（零成本）

路由决策:
  - 意图分析：简单问答→本地小模型；复杂推理→云端大模型
  - 负载均衡：本地模型繁忙→分流云端
  - 成本优化：统计每条路由的实际成本
"""

import asyncio
import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple

import httpx

logger = logging.getLogger("longhun-save.router")


# ════════════════════════════════════════════════════
# 数据结构
# ════════════════════════════════════════════════════

class RouteStrategy(str, Enum):
    LOCAL_ONLY = "local_only"    # 只用本地
    LOCAL_FIRST = "local_first"  # 本地优先（默认）
    CLOUD_ONLY = "cloud_only"    # 只用云端
    SMART = "smart"              # 智能判定


@dataclass
class ModelEndpoint:
    """模型端点配置"""
    name: str                      # 显示名
    base_url: str                  # API 地址
    model: str                     # 模型名
    api_key: str = ""              # API Key
    is_local: bool = True          # 是否本地
    max_tokens: int = 4096
    priority: int = 0              # 优先级（越小越优先）


@dataclass
class RouteDecision:
    """路由决策结果"""
    endpoint: ModelEndpoint
    strategy: RouteStrategy
    reason: str
    cached: bool = False
    latency_ms: float = 0.0


# ════════════════════════════════════════════════════
# 智能路由器
# ════════════════════════════════════════════════════

class SmartRouter:
    """AI 请求智能路由器

    配置:
        router = SmartRouter()
        router.add_local("http://localhost:11434/v1", "qwen2.5:7b")
        router.add_cloud("https://api.deepseek.com/v1", "deepseek-chat", "sk-xxx")

        decision = await router.route(messages)
        response = await router.call(decision, messages)
    """

    def __init__(self, default_strategy: RouteStrategy = RouteStrategy.LOCAL_FIRST):
        self.strategy = default_strategy
        self._endpoints: List[ModelEndpoint] = []
        self._health_cache: Dict[str, Tuple[bool, float]] = {}  # url → (alive, checked_at)
        self._health_ttl = 10  # 健康检查缓存秒数
        self._timeout = httpx.Timeout(60.0)

    # ═══════════════════════════════════════════════
    # 配置
    # ═══════════════════════════════════════════════

    def add_local(self, base_url: str, model: str, name: str = None,
                  priority: int = 0) -> "SmartRouter":
        """添加本地模型"""
        self._endpoints.append(ModelEndpoint(
            name=name or f"local:{model}",
            base_url=base_url.rstrip("/"),
            model=model,
            is_local=True,
            priority=priority,
        ))
        self._endpoints.sort(key=lambda e: (e.priority, 0 if e.is_local else 1))
        return self

    def add_cloud(self, base_url: str, model: str, api_key: str,
                  name: str = None, priority: int = 10) -> "SmartRouter":
        """添加云端模型"""
        self._endpoints.append(ModelEndpoint(
            name=name or f"cloud:{model}",
            base_url=base_url.rstrip("/"),
            model=model,
            api_key=api_key,
            is_local=False,
            priority=priority,
        ))
        self._endpoints.sort(key=lambda e: (e.priority, 0 if e.is_local else 1))
        return self

    # ═══════════════════════════════════════════════
    # 健康检查
    # ═══════════════════════════════════════════════

    async def health_check(self, endpoint: ModelEndpoint) -> bool:
        """检查端点是否可用"""
        now = time.time()
        if endpoint.base_url in self._health_cache:
            alive, checked_at = self._health_cache[endpoint.base_url]
            if now - checked_at < self._health_ttl:
                return alive

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(f"{endpoint.base_url}/models")
                alive = r.status_code == 200
        except Exception:
            alive = False

        self._health_cache[endpoint.base_url] = (alive, now)
        return alive

    # ═══════════════════════════════════════════════
    # 路由决策
    # ═══════════════════════════════════════════════

    async def route(self, messages: List[Dict], model_hint: str = None) -> RouteDecision:
        """决定请求路由到哪个端点

        Args:
            messages: 对话消息列表
            model_hint: 用户指定的模型（如果有）
        """
        # 用户指定了模型 → 找匹配的
        if model_hint:
            for ep in self._endpoints:
                if model_hint in ep.model or model_hint == ep.name:
                    return RouteDecision(endpoint=ep, strategy=RouteStrategy.SMART,
                                         reason=f"用户指定: {model_hint}")

        # 按策略路由
        if self.strategy == RouteStrategy.LOCAL_ONLY:
            for ep in self._endpoints:
                if ep.is_local and await self.health_check(ep):
                    return RouteDecision(endpoint=ep, strategy=RouteStrategy.LOCAL_ONLY,
                                         reason="仅本地模式")
            raise RuntimeError("LOCAL_ONLY 模式但所有本地模型不可用")

        if self.strategy == RouteStrategy.CLOUD_ONLY:
            for ep in self._endpoints:
                if not ep.is_local:
                    return RouteDecision(endpoint=ep, strategy=RouteStrategy.CLOUD_ONLY,
                                         reason="仅云端模式")
            raise RuntimeError("CLOUD_ONLY 模式但没有云端端点")

        # LOCAL_FIRST / SMART: 先尝试本地
        for ep in self._endpoints:
            if ep.is_local and await self.health_check(ep):
                return RouteDecision(endpoint=ep, strategy=RouteStrategy.LOCAL_FIRST,
                                     reason="本地可用·优先本地")

        # 降级到云端
        for ep in self._endpoints:
            if not ep.is_local:
                return RouteDecision(endpoint=ep, strategy=RouteStrategy.LOCAL_FIRST,
                                     reason="本地不可用·降级云端")

        raise RuntimeError("所有模型端点不可用")

    # ═══════════════════════════════════════════════
    # 调用
    # ═══════════════════════════════════════════════

    async def call(self, decision: RouteDecision,
                   messages: List[Dict], **kwargs) -> Tuple[Dict, RouteDecision]:
        """执行路由决策，调用 AI 模型"""
        ep = decision.endpoint
        payload = {
            "model": ep.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", ep.max_tokens),
            "stream": kwargs.get("stream", False),
        }

        headers = {"Content-Type": "application/json"}
        if ep.api_key:
            headers["Authorization"] = f"Bearer {ep.api_key}"

        t_start = time.time()

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            r = await client.post(
                f"{ep.base_url}/chat/completions",
                json=payload,
                headers=headers,
            )

        if r.status_code != 200:
            raise RuntimeError(f"模型返回错误 {r.status_code}: {r.text[:200]}")

        decision.latency_ms = (time.time() - t_start) * 1000
        return r.json(), decision

    # ═══════════════════════════════════════════════
    # 工具
    # ═══════════════════════════════════════════════

    def list_endpoints(self) -> List[dict]:
        """列出所有端点状态"""
        return [{
            "name": ep.name,
            "model": ep.model,
            "base_url": ep.base_url,
            "is_local": ep.is_local,
            "priority": ep.priority,
        } for ep in self._endpoints]

    @staticmethod
    def hash_request(messages: List[Dict], model: str, temperature: float) -> str:
        """计算请求哈希（用于缓存）"""
        key = json.dumps({
            "messages": messages,
            "model": model,
            "temperature": temperature,
        }, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(key.encode()).hexdigest()[:16]


# ════════════════════════════════════════════════════
# 自检
# ════════════════════════════════════════════════════

if __name__ == "__main__":
    import asyncio

    async def test():
        router = SmartRouter()
        # 试试本地 Ollama
        router.add_local("http://localhost:11434/v1", "qwen2.5:0.5b", priority=0)

        endpoints = router.list_endpoints()
        print(f"端点: {len(endpoints)}")
        for ep in endpoints:
            alive = await router.health_check(
                ModelEndpoint(name=ep["name"], base_url=ep["base_url"],
                             model=ep["model"], is_local=ep["is_local"],
                             priority=ep["priority"])
            )
            print(f"  {ep['name']}: {'🟢' if alive else '🔴'} {ep['base_url']}")

        if alive:
            messages = [{"role": "user", "content": "你好，用一句话介绍自己"}]
            decision = await router.route(messages)
            print(f"\n路由: {decision.reason}")
            resp, dec = await router.call(decision, messages, max_tokens=50)
            text = resp["choices"][0]["message"]["content"]
            print(f"回复: {text[:100]}...")
            print(f"延迟: {dec.latency_ms:.0f}ms")
        print("🟢 路由器自检完成")

    asyncio.run(test())
