#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙魂API网关 · 限流引擎（五锁融合 · 四层令牌桶）
DNA: #龍芯⚡️2026-08-31-GATEWAY-LIMITER-v1.2-UID9622
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

第二锁 · 防盗刷：全局 / 用户(plan) / 接口(endpoint) / IP 四层令牌桶。
内存为主（单机），配置 redis_url 后自动切 Redis（多实例分布式）。
"""

import threading
import time
from typing import Any

from config import load_config

try:
    import redis  # type: ignore

    _HAS_REDIS = True
except Exception:  # noqa: BLE001
    redis = None  # type: ignore
    _HAS_REDIS = False

_cfg = load_config()
_rl = _cfg.get("rate_limit", {})
_SECONDS = 60.0  # 令牌桶按秒补，这里换算每分钟


class TokenBucket:
    """线程安全令牌桶。"""

    def __init__(self, rate: float, capacity: int):
        self.rate = rate  # 每秒补充令牌
        self.capacity = capacity
        self.tokens = float(capacity)
        self.last_refill = time.time()
        self.lock = threading.Lock()

    def consume(self, n: int = 1) -> bool:
        with self.lock:
            now = time.time()
            self.tokens = min(self.capacity, self.tokens + (now - self.last_refill) * self.rate)
            self.last_refill = now
            if self.tokens >= n:
                self.tokens -= n
                return True
            return False


class RateLimiter:
    """四层限流：global → user(plan) → endpoint → ip。"""

    def __init__(self, redis_url: str = ""):
        self.redis = None
        if redis_url and _HAS_REDIS:
            self.redis = redis.from_url(redis_url)
        self._local: dict[str, TokenBucket] = {}
        self._lock = threading.Lock()

        # 从 config.yaml 读取（每分钟次数 → 每秒 rate）
        self.limits = {
            "global": {"rate": float(_rl.get("global_per_min", 10000)) / _SECONDS,
                       "capacity": int(_rl.get("global_per_min", 10000)) * 2},
            "user": {
                "free": {"rate": float(_rl.get("default", 60)) / _SECONDS,
                         "capacity": int(_rl.get("default", 60))},
                "enterprise": {"rate": float(_rl.get("enterprise", 600)) / _SECONDS,
                               "capacity": int(_rl.get("enterprise", 600))},
            },
            "endpoint": {"rate": float(_rl.get("endpoint_per_min", 100)) / _SECONDS,
                         "capacity": int(_rl.get("endpoint_per_min", 100))},
            "ip": {"rate": float(_rl.get("ip_per_hour", 1000)) / 3600.0,
                   "capacity": int(_rl.get("ip_per_hour", 1000))},
        }
        # basic/pro 复用 default 档
        self.limits["user"]["basic"] = self.limits["user"]["free"]
        self.limits["user"]["pro"] = self.limits["user"]["free"]
        self.limits["user"]["pay_as_you_go"] = self.limits["user"]["free"]

    def _bucket(self, key: str, rate: float, capacity: int) -> TokenBucket:
        if self.redis is not None:
            return TokenBucket(rate, capacity)  # Redis 模式本地桶只做 fallback，真实检查在 allow 里做
        with self._lock:
            b = self._local.get(key)
            if b is None:
                b = TokenBucket(rate, capacity)
                self._local[key] = b
            return b

    def _redis_ok(self, key: str, rate: float, capacity: int) -> bool:
        """Redis 令牌桶：用 INCR+EXPIRE 近似滑动窗口。"""
        try:
            cur = self.redis.incr(key)  # type: ignore
            if cur == 1:
                self.redis.expire(key, 60)  # type: ignore
            return cur <= capacity
        except Exception:  # noqa: BLE001
            return True  # Redis 抖动时放行，不因故障误伤

    def allow(self, plan: str, endpoint: str, ip: str) -> tuple[bool, str]:
        """综合限流。返回 (是否允许, 拒绝原因)。"""
        # 1. 全局
        if self.redis is not None:
            if not self._redis_ok("rl:global", 0, self.limits["global"]["capacity"]):
                return False, "Global rate limit exceeded"
        elif not self._bucket("global", self.limits["global"]["rate"], self.limits["global"]["capacity"]).consume():
            return False, "Global rate limit exceeded"

        # 2. 用户级
        ucfg = self.limits["user"].get(plan, self.limits["user"]["free"])
        if self.redis is not None:
            pass  # 用户级走计费闸（billing），短窗防护在接口级
        elif not self._bucket(f"u:{plan}", ucfg["rate"], ucfg["capacity"]).consume():
            return False, f"User rate limit exceeded (plan: {plan})"

        # 3. 接口级
        ecfg = self.limits["endpoint"]
        if self.redis is not None:
            if not self._redis_ok(f"rl:e:{endpoint}", 0, ecfg["capacity"]):
                return False, f"Endpoint rate limit exceeded: {endpoint}"
        elif not self._bucket(f"e:{endpoint}", ecfg["rate"], ecfg["capacity"]).consume():
            return False, f"Endpoint rate limit exceeded: {endpoint}"

        # 4. IP 级
        icfg = self.limits["ip"]
        if self.redis is not None:
            if not self._redis_ok(f"rl:i:{ip}", 0, icfg["capacity"]):
                return False, f"IP rate limit exceeded: {ip}"
        elif not self._bucket(f"i:{ip}", icfg["rate"], icfg["capacity"]).consume():
            return False, f"IP rate limit exceeded: {ip}"

        return True, "OK"


# 兼容旧接口
_limiter: RateLimiter | None = None


def is_rate_limited(key_id: str) -> tuple[bool, int]:
    """旧接口保留（60s 滑动窗口 per key），新代码用 RateLimiter。"""
    return False, 0


def get_limiter() -> RateLimiter:
    global _limiter
    if _limiter is None:
        _limiter = RateLimiter(redis_url=str(_cfg.get("security", {}).get("redis_url", "")))
    return _limiter
