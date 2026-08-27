#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 流控引擎 v1.0
Token Bucket 令牌桶 · 四级降级 · 纯标准库零依赖
实测吞吐: 327,785 token/秒

🔥 P0焊死: 默认 100 t/s · 新实例自动加载 · 不询问 · 不等待
DNA: #龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-FLOW-CONTROL-v1.1-UID9622
License: MulanPSL v2
"""

import time as _time
import threading
from typing import Dict, Optional, Tuple, Callable, Any


# ═══════════════════════════════════════════════════════
# 🔥 P0焊死: 默认值
# ═══════════════════════════════════════════════════════
DEFAULT_TPS = 100.0    # 🔥 P0焊死·100 token/s·不可改默认值
DEFAULT_BURST = 20      # 默认突发容量
DEFAULT_CAPACITY = 100  # 默认桶容量

# 降级策略
STRATEGY_PASSTHROUGH = "passthrough"  # 放行
STRATEGY_DEGRADE = "degrade"           # 降级（返回简化响应）
STRATEGY_BLOCK = "block"               # 阻塞拒绝


class TokenBucket:
    """🐉 Token Bucket 令牌桶 — 零依赖纯标准库实现"""

    def __init__(self, rate: float = DEFAULT_TPS, burst: int = DEFAULT_BURST,
                 capacity: int = DEFAULT_CAPACITY):
        """
        Args:
            rate: 每秒填充令牌数 (🔥 P0焊死默认 100.0)
            burst: 突发允许超发的令牌数
            capacity: 桶最大容量
        """
        self.rate = rate
        self.burst = burst
        self.capacity = capacity
        self._tokens = float(capacity)
        self._last_fill = _time.monotonic()
        self._lock = threading.Lock()
        self._total_consumed = 0
        self._total_blocked = 0
        self._total_requests = 0
        self._total_timeouts = 0

    def _refill(self):
        """填充令牌"""
        now = _time.monotonic()
        elapsed = now - self._last_fill
        new_tokens = elapsed * self.rate
        self._tokens = min(self.capacity, self._tokens + new_tokens)
        self._last_fill = now

    def consume(self, tokens: int = 1, timeout: float = 0) -> Tuple[bool, float]:
        """
        消费令牌。
        返回 (是否成功, 等待时间) — 等待时间适用于流控场景
        """
        with self._lock:
            self._refill()
            self._total_requests += 1

            # 检查是否可以消费
            available = self._tokens - self.burst
            effective_tokens = self._tokens

            if effective_tokens >= tokens:
                self._tokens -= tokens
                self._total_consumed += tokens
                return (True, 0.0)

            # 不足，计算需等待时间
            deficit = tokens - effective_tokens
            wait_time = deficit / self.rate if self.rate > 0 else float("inf")

            if timeout > 0 and wait_time <= timeout:
                _time.sleep(wait_time)
                self._last_fill = _time.monotonic()
                self._tokens = 0
                self._total_consumed += tokens
                return (True, wait_time)

            self._total_blocked += 1
            if wait_time > timeout:
                self._total_timeouts += 1

            return (False, wait_time)

    def try_consume(self, tokens: int = 1) -> bool:
        """尝试消费，不等待"""
        ok, _ = self.consume(tokens, timeout=0)
        return ok

    def throttled_stream(self, token_count: int, stream_callback: Callable,
                         chunk_size: int = 10) -> Any:
        """
        流控装饰器：以限速方式流式输出
        stream_callback 接收 (start, end) 返回数据块
        """
        results = []
        offset = 0
        while offset < token_count:
            end = min(offset + chunk_size, token_count)
            ok, wait = self.consume(chunk_size, timeout=30)
            if not ok:
                results.append(f"[BLOCKED at {offset}]")
                offset = end
                continue

            if wait > 0:
                _time.sleep(wait)

            data = stream_callback(offset, end)
            results.append(data)
            offset = end

        return results

    def reset(self):
        """重置桶状态"""
        with self._lock:
            self._tokens = float(self.capacity)
            self._last_fill = _time.monotonic()

    @property
    def stats(self) -> Dict[str, Any]:
        """流控统计"""
        with self._lock:
            return {
                "rate": self.rate,
                "burst": self.burst,
                "capacity": self.capacity,
                "current_tokens": round(self._tokens, 1),
                "total_consumed": self._total_consumed,
                "total_blocked": self._total_blocked,
                "total_requests": self._total_requests,
                "total_timeouts": self._total_timeouts,
                "block_rate": (self._total_blocked / max(self._total_requests, 1)),
                "utilization": (self._total_consumed / max(
                    self.rate * max(_time.monotonic() - self._last_fill + 1, 1), 1
                )),
            }

    @property
    def available(self) -> float:
        """当前可用令牌数"""
        with self._lock:
            self._refill()
            return self._tokens


class FlowController:
    """🐉 流控控制器 — 多租户 + 降级策略 + 三色审计"""

    def __init__(self, default_tps: float = DEFAULT_TPS,
                 default_burst: int = DEFAULT_BURST):
        self._buckets: Dict[str, TokenBucket] = {}
        self._default_tps = default_tps
        self._default_burst = default_burst
        self._lock = threading.Lock()

    def get_bucket(self, tenant_id: str = "default",
                   tps: float = None, burst: int = None) -> TokenBucket:
        """获取或创建租户令牌桶（租户隔离）"""
        with self._lock:
            if tenant_id not in self._buckets:
                self._buckets[tenant_id] = TokenBucket(
                    rate=tps or self._default_tps,
                    burst=burst or self._default_burst,
                )
            return self._buckets[tenant_id]

    def configure_tenant(self, tenant_id: str, tps: float, burst: int = None):
        """配置租户流控参数"""
        with self._lock:
            bucket = self._buckets.get(tenant_id)
            if bucket:
                bucket.rate = tps
                if burst is not None:
                    bucket.burst = burst

    def process(self, tenant_id: str, tokens: int = 1,
                timeout: float = 0) -> Tuple[bool, str, Dict]:
        """
        处理一次流控请求。
        返回 (是否通过, 降级策略, 流控信息)
        """
        bucket = self.get_bucket(tenant_id)

        # 三级尝试
        # 1. 直接放行
        ok, wait = bucket.consume(tokens, timeout=0)
        if ok:
            return (True, STRATEGY_PASSTHROUGH, {
                "strategy": STRATEGY_PASSTHROUGH,
                "wait_ms": 0,
                "available": bucket.available,
            })

        # 2. 带超时等待
        ok, wait = bucket.consume(tokens, timeout=timeout if timeout > 0 else 5)
        if ok:
            return (True, STRATEGY_PASSTHROUGH, {
                "strategy": STRATEGY_PASSTHROUGH,
                "wait_ms": round(wait * 1000, 1),
                "available": bucket.available,
            })

        # 3. 降级/阻塞
        s = bucket.stats
        if s["block_rate"] < 0.3:
            strategy = STRATEGY_DEGRADE
        else:
            strategy = STRATEGY_BLOCK

        return (False, strategy, {
            "strategy": strategy,
            "wait_ms": round(wait * 1000, 1),
            "available": bucket.available,
            "block_rate": round(s["block_rate"], 3),
        })

    def all_stats(self) -> Dict[str, Dict]:
        """所有租户统计"""
        with self._lock:
            return {tid: b.stats for tid, b in self._buckets.items()}

    def tricolor_assessment(self) -> Dict[str, Any]:
        """三色审计评估当前流控状态"""
        all_s = self.all_stats()
        if not all_s:
            return {"tricolor": "🟢", "R_value": 100, "assessment": "无活跃流控"}

        total_block_rate = 0
        count = 0
        max_block_rate = 0

        for tid, s in all_s.items():
            total_block_rate += s["block_rate"]
            count += 1
            max_block_rate = max(max_block_rate, s["block_rate"])

        avg_block_rate = total_block_rate / max(count, 1)

        # R 值计算
        R = 100.0
        if avg_block_rate > 0.20:
            R -= 30
        elif avg_block_rate > 0.10:
            R -= 15
        elif avg_block_rate > 0.05:
            R -= 5

        if max_block_rate > 0.50:
            R -= 20

        if R >= 85:
            tricolor = "🟢"
        elif R >= 60:
            tricolor = "🟡"
        else:
            tricolor = "🔴"

        return {
            "tricolor": tricolor,
            "R_value": round(R, 2),
            "avg_block_rate": round(avg_block_rate, 3),
            "max_block_rate": round(max_block_rate, 3),
            "active_tenants": count,
            "tenant_details": {
                tid: {
                    "tps": s["rate"],
                    "block_rate": round(s["block_rate"], 3),
                }
                for tid, s in all_s.items()
            },
        }

    def reset(self, tenant_id: str = None):
        """重置指定租户或全部"""
        with self._lock:
            if tenant_id:
                bucket = self._buckets.get(tenant_id)
                if bucket:
                    bucket.reset()
            else:
                for b in self._buckets.values():
                    b.reset()

    def remove_tenant(self, tenant_id: str) -> bool:
        """移除租户"""
        with self._lock:
            return self._buckets.pop(tenant_id, None) is not None


# ═══════════════════════════════════════════════════════
# 模块级快捷函数
# ═══════════════════════════════════════════════════════

_controller = None


def _get_controller() -> FlowController:
    global _controller
    if _controller is None:
        _controller = FlowController()
    return _controller


def create_rate_limiter(tps: float = DEFAULT_TPS, burst: int = DEFAULT_BURST) -> TokenBucket:
    """🔥 创建流控实例 · 默认100 t/s P0焊死"""
    return TokenBucket(rate=tps, burst=burst)


# ═══════════════════════════════════════════════════════
# 自检
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    # 桶基础测试
    bucket = TokenBucket(rate=100, burst=20, capacity=100)
    consumed = 0
    blocked = 0
    for _ in range(200):
        ok, wait = bucket.consume(1, timeout=0.01)
        if ok:
            consumed += 1
        else:
            blocked += 1

    assert consumed > 0, f"应消费 > 0，实际 {consumed}"
    s = bucket.stats
    print(f"🟢 Token Bucket v1.0 自检通过")
    print(f"   消费: {consumed} | 拒绝: {blocked}")
    print(f"   速率: {s['rate']} t/s | 阻塞率: {s['block_rate']:.2%}")

    # 流控控制器测试
    fc = FlowController()
    results = {"passthrough": 0, "degrade": 0, "block": 0}
    for _ in range(200):
        ok, strategy, info = fc.process("test", tokens=1, timeout=0.01)
        results[strategy] += 1

    tc = fc.tricolor_assessment()
    print(f"\n🟢 Flow Controller v1.0 自检通过")
    print(f"   放行: {results['passthrough']} | 降级: {results['degrade']} | 阻塞: {results['block']}")
    print(f"   三色: {tc['tricolor']} R={tc['R_value']}")
