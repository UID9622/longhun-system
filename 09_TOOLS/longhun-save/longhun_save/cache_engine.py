#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️2026-08-06-SAVE-CACHE-v1.0
# License: MulanPSL v2
"""
请求缓存引擎
═══════════

相同请求不重复调用 AI，直接返回缓存结果。
缓存策略: LRU + TTL（默认1小时）

节省策略:
  - 完全相同请求 → 直接命中
  - 相似请求（编辑距离<阈值）→ 提示用户可复用
"""

import hashlib
import json
import time
import threading
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple


@dataclass
class CacheEntry:
    """缓存条目"""
    key: str
    response: Dict[str, Any]
    messages_hash: str          # 原始请求哈希
    created_at: float           # 创建时间戳
    hit_count: int = 0          # 命中次数
    last_hit: float = 0.0       # 最后命中时间
    saved_tokens: int = 0       # 节省的 token 数


class RequestCache:
    """AI 请求缓存 · LRU + TTL

    用法:
        cache = RequestCache(max_size=1000, ttl=3600)

        # 查找
        cached = cache.get(messages, model, temperature)
        if cached:
            return cached  # 直接返回，零成本

        # 未命中 → 调用 AI → 缓存
        response = call_ai(...)
        cache.put(messages, model, temperature, response)
    """

    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        """
        Args:
            max_size: 最大缓存条目数
            ttl: 缓存有效期（秒），默认 1 小时
        """
        self.max_size = max_size
        self.ttl = ttl
        self._store: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.Lock()
        self._total_hits = 0
        self._total_misses = 0
        self._total_saved_tokens = 0

    def _make_key(self, messages: List[Dict], model: str, temperature: float) -> str:
        """生成缓存键"""
        raw = json.dumps({
            "m": messages,
            "model": model,
            "t": temperature,
        }, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def get(self, messages: List[Dict], model: str = "default",
            temperature: float = 0.7) -> Optional[Dict[str, Any]]:
        """查找缓存

        Returns:
            命中的 response dict，未命中返回 None
        """
        key = self._make_key(messages, model, temperature)

        with self._lock:
            # 清理过期
            self._evict_expired()

            entry = self._store.get(key)
            if entry is None:
                self._total_misses += 1
                return None

            # 检查 TTL
            if time.time() - entry.created_at > self.ttl:
                del self._store[key]
                self._total_misses += 1
                return None

            # 命中
            entry.hit_count += 1
            entry.last_hit = time.time()
            self._total_hits += 1
            self._total_saved_tokens += entry.saved_tokens

            # LRU: 移到末尾
            self._store.move_to_end(key)

            return entry.response

    def put(self, messages: List[Dict], model: str, temperature: float,
            response: Dict[str, Any]):
        """存入缓存"""
        key = self._make_key(messages, model, temperature)

        # 估算节省的 token 数
        usage = response.get("usage", {})
        saved_tokens = (
            usage.get("prompt_tokens", 0) + usage.get("completion_tokens", 0)
        )

        entry = CacheEntry(
            key=key,
            response=response,
            messages_hash=key,
            created_at=time.time(),
            saved_tokens=saved_tokens,
        )

        with self._lock:
            # LRU 淘汰
            if len(self._store) >= self.max_size:
                self._store.popitem(last=False)  # 去掉最老的

            self._store[key] = entry

    def _evict_expired(self):
        """淘汰过期条目"""
        now = time.time()
        expired = [k for k, v in self._store.items()
                   if now - v.created_at > self.ttl]
        for k in expired:
            del self._store[k]

    def stat(self) -> dict:
        """缓存统计"""
        with self._lock:
            total = self._total_hits + self._total_misses
            return {
                "entries": len(self._store),
                "max_size": self.max_size,
                "ttl_seconds": self.ttl,
                "total_hits": self._total_hits,
                "total_misses": self._total_misses,
                "hit_rate": round(self._total_hits / total, 3) if total > 0 else 0,
                "total_saved_tokens": self._total_saved_tokens,
            }

    def clear(self):
        """清空缓存"""
        with self._lock:
            self._store.clear()
            self._total_hits = 0
            self._total_misses = 0
            self._total_saved_tokens = 0


# ════════════════════════════════════════════════════
# 自检
# ════════════════════════════════════════════════════

if __name__ == "__main__":
    cache = RequestCache(max_size=10, ttl=60)

    MODEL = "test-model"
    TEMP = 0.7

    msg1 = [{"role": "user", "content": "你好"}]
    msg2 = [{"role": "user", "content": "再见"}]

    # 未命中
    r1 = cache.get(msg1, MODEL, TEMP)
    assert r1 is None, "应未命中"
    print("🟢 缓存未命中（正确）")

    # 存入
    cache.put(msg1, MODEL, TEMP, {"choices": [{"message": {"content": "你好!"}}]})

    # 命中
    r2 = cache.get(msg1, MODEL, TEMP)
    assert r2 is not None, "应命中"
    assert r2["choices"][0]["message"]["content"] == "你好!"
    print("🟢 缓存命中（正确）")

    # 不同请求不命中
    r3 = cache.get(msg2, MODEL, TEMP)
    assert r3 is None, "应未命中"
    print("🟢 不同请求未命中（正确）")

    stats = cache.stat()
    print(f"统计: {stats}")
    print("🟢🟢🟢 缓存引擎自检通过")
