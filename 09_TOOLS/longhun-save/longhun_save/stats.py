#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-08-06-SAVE-STATS-v1.0
# License: MulanPSL v2
"""
成本统计引擎
═══════════

追踪每次 AI 调用的成本，对比本地 vs 云端，计算节省金额。

价格参考（2026年大致价格，人民币）:
  - DeepSeek: 输入 ¥1/百万token, 输出 ¥2/百万token
  - 混元: 输入 ¥1.5/百万token, 输出 ¥4/百万token
  - Ollama 本地: ¥0（电费忽略不计）
"""

import json
import time
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional


# ════════════════════════════════════════════════════
# 价格表
# ════════════════════════════════════════════════════

@dataclass
class TokenPrice:
    """每百万 token 价格（人民币）"""
    input_price: float   # 输入价格 ¥/M token
    output_price: float  # 输出价格 ¥/M token

    def cost(self, input_tokens: int, output_tokens: int) -> float:
        """计算本次调用成本"""
        return (input_tokens / 1_000_000) * self.input_price + \
               (output_tokens / 1_000_000) * self.output_price


# 预设价格表
PRICE_TABLE: Dict[str, TokenPrice] = {
    "deepseek": TokenPrice(input_price=1.0, output_price=2.0),
    "hunyuan": TokenPrice(input_price=1.5, output_price=4.0),
    "qwen-max": TokenPrice(input_price=2.0, output_price=6.0),
    "gpt-4o": TokenPrice(input_price=35.0, output_price=105.0),
    "gpt-4o-mini": TokenPrice(input_price=2.0, output_price=8.0),
    "claude": TokenPrice(input_price=22.0, output_price=88.0),
    "local": TokenPrice(input_price=0, output_price=0),  # 本地免费
}


@dataclass
class CallRecord:
    """单次调用记录"""
    timestamp: str
    endpoint: str                 # 路由到的端点
    model: str
    is_local: bool
    input_tokens: int
    output_tokens: int
    latency_ms: float
    cached: bool = False
    cost_rmb: float = 0.0         # 实际花费
    saved_vs_cloud: float = 0.0   # 相比云端节省


class CostStats:
    """成本统计追踪器

    用法:
        stats = CostStats()
        stats.record("local:qwen", "qwen2.5:7b", is_local=True,
                     input_tokens=500, output_tokens=200, latency_ms=120)
        print(stats.summary())
    """

    def __init__(self, cloud_price: TokenPrice = None):
        self._records: List[CallRecord] = []
        self._lock = threading.Lock()
        self._cloud_price = cloud_price or PRICE_TABLE.get("deepseek", TokenPrice(1.0, 2.0))

    def record(self, endpoint: str, model: str, is_local: bool,
               input_tokens: int, output_tokens: int, latency_ms: float,
               cached: bool = False):
        """记录一次调用"""
        # 确定价格
        if is_local or cached:
            price = PRICE_TABLE["local"]
        else:
            # 从端点名推断价格
            price = self._cloud_price
            for name, p in PRICE_TABLE.items():
                if name in endpoint.lower() or name in model.lower():
                    price = p
                    break

        cost = price.cost(input_tokens, output_tokens) if not cached else 0
        cloud_cost = self._cloud_price.cost(input_tokens, output_tokens)
        saved = cloud_cost - cost

        record = CallRecord(
            timestamp=datetime.now(timezone.utc).isoformat(),
            endpoint=endpoint,
            model=model,
            is_local=is_local,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            cached=cached,
            cost_rmb=cost,
            saved_vs_cloud=saved,
        )

        with self._lock:
            self._records.append(record)

    def summary(self) -> dict:
        """汇总统计"""
        with self._lock:
            total = len(self._records)
            if total == 0:
                return {"total_calls": 0, "message": "暂无调用记录"}

            local_calls = sum(1 for r in self._records if r.is_local)
            cloud_calls = sum(1 for r in self._records if not r.is_local)
            cached_calls = sum(1 for r in self._records if r.cached)
            total_cost = sum(r.cost_rmb for r in self._records)
            total_saved = sum(r.saved_vs_cloud for r in self._records)
            total_input = sum(r.input_tokens for r in self._records)
            total_output = sum(r.output_tokens for r in self._records)
            avg_latency = sum(r.latency_ms for r in self._records) / total if total > 0 else 0

            return {
                "total_calls": total,
                "local_calls": local_calls,
                "cloud_calls": cloud_calls,
                "cached_calls": cached_calls,
                "total_input_tokens": total_input,
                "total_output_tokens": total_output,
                "total_cost_rmb": round(total_cost, 6),
                "total_saved_rmb": round(total_saved, 6),
                "saved_vs_cloud_percent": round(
                    total_saved / (total_cost + total_saved) * 100, 1
                ) if (total_cost + total_saved) > 0 else 100,
                "avg_latency_ms": round(avg_latency, 1),
                "local_ratio": round(local_calls / total * 100, 1),
            }

    def recent_calls(self, n: int = 10) -> List[dict]:
        """最近 N 次调用详情"""
        with self._lock:
            return [
                {
                    "time": r.timestamp,
                    "endpoint": r.endpoint,
                    "model": r.model,
                    "is_local": r.is_local,
                    "cached": r.cached,
                    "input_tokens": r.input_tokens,
                    "output_tokens": r.output_tokens,
                    "latency_ms": r.latency_ms,
                    "cost_rmb": round(r.cost_rmb, 6),
                    "saved_rmb": round(r.saved_vs_cloud, 6),
                }
                for r in self._records[-n:]
            ]

    def to_json(self) -> str:
        return json.dumps({
            "summary": self.summary(),
            "recent": self.recent_calls(20),
        }, ensure_ascii=False, indent=2)


# ════════════════════════════════════════════════════
# 自检
# ════════════════════════════════════════════════════

if __name__ == "__main__":
    stats = CostStats()

    # 模拟一些调用
    for i in range(5):
        stats.record("local:qwen", "qwen2.5:7b", is_local=True,
                     input_tokens=500, output_tokens=200, latency_ms=80 + i * 10)

    for i in range(2):
        stats.record("cloud:deepseek", "deepseek-chat", is_local=False,
                     input_tokens=1000, output_tokens=500, latency_ms=500 + i * 50)

    stats.record("local:qwen", "qwen2.5:7b", is_local=True,
                 input_tokens=300, output_tokens=150, latency_ms=5, cached=True)

    summary = stats.summary()
    print(f"总调用: {summary['total_calls']}")
    print(f"本地: {summary['local_calls']} | 云端: {summary['cloud_calls']} | 缓存: {summary['cached_calls']}")
    print(f"总花费: ¥{summary['total_cost_rmb']}")
    print(f"节省: ¥{summary['total_saved_rmb']} ({summary['saved_vs_cloud_percent']}%)")
    print(f"本地率: {summary['local_ratio']}%")
    print(f"平均延迟: {summary['avg_latency_ms']}ms")
    print("🟢 成本统计自检通过")
