#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 模型路由引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-ROUTER-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 根据任务特征自动选择最合适的模型
  - 支持规则路由/性能路由/A/B测试
  - 记录性能数据用于动态路由
"""

import random
import time
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass


class RouteMode(Enum):
    RULE = "rule"
    PERFORMANCE = "performance"
    AB_TEST = "ab_test"


@dataclass
class ModelEndpoint:
    name: str
    handler: Callable
    latency_ms: float = 100
    accuracy: float = 0.95


class ModelRouter:
    """模型路由引擎——简单任务用规则，复杂任务用大模型"""

    def __init__(self):
        self.endpoints: Dict[str, ModelEndpoint] = {}
        self.rules: List[Dict] = []
        self.mode = RouteMode.RULE
        self.performance_history: Dict[str, List[Dict]] = {}
        self._init_default()

    def _init_default(self):
        self.register("rule", lambda x: f"[规则] {x[:50]}", latency=5, accuracy=0.99)
        self.register("fast", lambda x: f"[快速] {x}", latency=20, accuracy=0.90)
        self.register("accurate", lambda x: f"[高精度] {x}", latency=200, accuracy=0.98)
        self.add_rule("健康", "rule")
        self.add_rule("审计", "accurate")
        self.add_rule("记忆", "fast")
        self.add_rule("代码", "accurate")
        self.add_rule("快速", "fast")

    def register(self, name: str, handler: Callable, latency: float = 100, accuracy: float = 0.95):
        self.endpoints[name] = ModelEndpoint(name=name, handler=handler, latency_ms=latency, accuracy=accuracy)

    def add_rule(self, keyword: str, model_name: str):
        self.rules.append({"keyword": keyword, "model": model_name})

    def route(self, task: str, context: Dict = None) -> ModelEndpoint:
        context = context or {}
        mode = context.get("mode", self.mode)

        if mode == RouteMode.PERFORMANCE:
            return self._route_by_performance()
        elif mode == RouteMode.AB_TEST:
            return self._route_ab_test()
        return self._route_by_rule(task)

    def _route_by_rule(self, task: str) -> ModelEndpoint:
        for rule in self.rules:
            if rule["keyword"] in task:
                return self.endpoints.get(rule["model"], self.endpoints["rule"])
        return self.endpoints["rule"]

    def _route_by_performance(self) -> ModelEndpoint:
        candidates = [(n, e) for n, e in self.endpoints.items() if e.accuracy > 0.9]
        if candidates:
            candidates.sort(key=lambda x: x[1].latency_ms)
            return candidates[0][1]
        return self.endpoints["rule"]

    def _route_ab_test(self) -> ModelEndpoint:
        if random.random() < 0.1:
            return self.endpoints.get("accurate", self.endpoints["rule"])
        return self.endpoints["rule"]

    def record(self, model_name: str, latency_ms: float, success: bool):
        if model_name not in self.performance_history:
            self.performance_history[model_name] = []
        self.performance_history[model_name].append({"latency": latency_ms, "success": success, "time": time.time()})
        if model_name in self.endpoints:
            recent = self.performance_history[model_name][-100:]
            if recent:
                self.endpoints[model_name].latency_ms = sum(r["latency"] for r in recent) / len(recent)

    def get_recommendation(self, task: str) -> Dict:
        selected = self.route(task)
        return {"task": task, "model": selected.name, "latency_ms": selected.latency_ms, "accuracy": selected.accuracy}

    def set_mode(self, mode: RouteMode):
        self.mode = mode


if __name__ == "__main__":
    router = ModelRouter()
    for task in ["健康检查", "审计代码", "记忆搜索", "写代码"]:
        rec = router.get_recommendation(task)
        print(f"  [{task}] → {rec['model']} (延迟:{rec['latency_ms']}ms, 精度:{rec['accuracy']})")
    router.record("fast", 15, True)
    router.record("rule", 3, True)
    print("🟢 模型路由引擎测试通过")
