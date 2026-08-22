#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 AI 网关 · 流控模块 v1.0
DNA: #龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-FLOW-CONTROL-UID9622

功能:
- Token Bucket 限流算法
- 支持流式输出 (SSE / WebSocket)
- 配置化 (速率/突发/场景)
- 监控指标暴露
- 三色审计对接
- 降级策略 (流控失败时的兜底)
"""

import time
import json
import threading
import logging
from typing import Optional, Dict, Any, Callable, Generator
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum
import hashlib

# ============================================================
# 日志配置
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('longhun.flow_control')


# ============================================================
# 主权锚定
# ============================================================

class SovereignAnchor:
    UID = "9622"
    DNA_PREFIX = "#龍芯⚡️"
    GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

    @classmethod
    def generate_dna(cls, suffix: str = "") -> str:
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        rand = hashlib.md5(f"{suffix}{time.time()}".encode()).hexdigest()[:8].upper()
        return f"{cls.DNA_PREFIX}{timestamp}-{suffix}-{rand}-{cls.UID}"


# ============================================================
# Token Bucket 核心算法
# ============================================================

class TokenBucket:
    """
    Token Bucket 限流器
    - 每秒填充 tokens_per_second 个 token
    - burst_size 为最大突发容量
    - 线程安全
    """

    def __init__(self, tokens_per_second: float = 100.0, burst_size: int = 20):
        self.tokens_per_second = tokens_per_second
        self.burst_size = burst_size
        self._tokens = burst_size
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self):
        """填充 token"""
        now = time.monotonic()
        elapsed = now - self._last_refill
        new_tokens = elapsed * self.tokens_per_second
        if new_tokens > 0:
            self._tokens = min(self.burst_size, self._tokens + new_tokens)
            self._last_refill = now

    def consume(self, tokens: int = 1) -> bool:
        """
        消费 token，返回是否成功
        """
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

    def wait_and_consume(self, tokens: int = 1, timeout: float = None) -> bool:
        """
        等待直到有足够 token，或超时
        """
        start = time.monotonic()
        while True:
            if self.consume(tokens):
                return True
            if timeout is not None and (time.monotonic() - start) > timeout:
                return False
            time.sleep(0.001)  # 1ms 轮询

    def get_available(self) -> float:
        """获取当前可用 token 数"""
        with self._lock:
            self._refill()
            return self._tokens

    def get_stats(self) -> Dict:
        """获取统计信息"""
        with self._lock:
            self._refill()
            return {
                "tokens_per_second": self.tokens_per_second,
                "burst_size": self.burst_size,
                "available_tokens": round(self._tokens, 2),
                "utilization": round(1 - (self._tokens / self.burst_size), 4)
            }


# ============================================================
# 场景配置
# ============================================================

@dataclass
class RateLimitConfig:
    """流控配置"""
    enabled: bool = True
    tokens_per_second: float = 100.0
    burst_size: int = 20
    timeout: Optional[float] = 5.0
    fallback_action: str = "block"  # block | passthrough | degrade
    audit_logging: bool = True
    tricolor_check: bool = True

    def to_dict(self) -> Dict:
        return {
            "enabled": self.enabled,
            "tokens_per_second": self.tokens_per_second,
            "burst_size": self.burst_size,
            "timeout": self.timeout,
            "fallback_action": self.fallback_action,
            "audit_logging": self.audit_logging,
            "tricolor_check": self.tricolor_check
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'RateLimitConfig':
        return cls(
            enabled=data.get("enabled", True),
            tokens_per_second=data.get("tokens_per_second", 100.0),
            burst_size=data.get("burst_size", 20),
            timeout=data.get("timeout", 5.0),
            fallback_action=data.get("fallback_action", "block"),
            audit_logging=data.get("audit_logging", True),
            tricolor_check=data.get("tricolor_check", True)
        )


# ============================================================
# 默认配置
# ============================================================

SCENE_CONFIGS = {
    "local": RateLimitConfig(
        tokens_per_second=100.0,
        burst_size=20,
        timeout=3.0,
        fallback_action="passthrough"
    ),
    "cloud": RateLimitConfig(
        tokens_per_second=50.0,
        burst_size=10,
        timeout=5.0,
        fallback_action="block"
    ),
    "hybrid": RateLimitConfig(
        tokens_per_second=80.0,
        burst_size=15,
        timeout=4.0,
        fallback_action="degrade"
    ),
    "critical": RateLimitConfig(
        tokens_per_second=200.0,
        burst_size=30,
        timeout=2.0,
        fallback_action="passthrough"
    ),
    "test": RateLimitConfig(
        tokens_per_second=1000.0,
        burst_size=100,
        timeout=1.0,
        fallback_action="passthrough"
    ),
}


# ============================================================
# 流控插件
# ============================================================

class RateLimiterPlugin:
    """
    龍魂流控插件
    - 支持流式输出的限流
    - 支持多租户隔离
    - 支持动态配置更新
    - 支持三色审计对接
    """

    def __init__(self, config: Optional[RateLimitConfig] = None):
        self.config = config or RateLimitConfig()
        self._buckets: Dict[str, TokenBucket] = {}
        self._stats = defaultdict(lambda: {
            "total_tokens": 0,
            "consumed_tokens": 0,
            "blocked": 0,
            "timeouts": 0,
            "last_activity": 0
        })
        self._lock = threading.Lock()
        self.dna = SovereignAnchor.generate_dna("FLOW-CONTROL")
        self._audit_log = []

    def _get_bucket(self, session_id: str) -> TokenBucket:
        """获取或创建 session 对应的 bucket"""
        with self._lock:
            if session_id not in self._buckets:
                self._buckets[session_id] = TokenBucket(
                    tokens_per_second=self.config.tokens_per_second,
                    burst_size=self.config.burst_size
                )
            return self._buckets[session_id]

    def _update_stats(self, session_id: str, consumed: int, success: bool):
        """更新统计"""
        stats = self._stats[session_id]
        stats["total_tokens"] += consumed
        if success:
            stats["consumed_tokens"] += consumed
        else:
            stats["blocked"] += 1
        stats["last_activity"] = time.time()

    def _audit(self, session_id: str, action: str, result: str, detail: str = ""):
        """审计日志"""
        if not self.config.audit_logging:
            return
        entry = {
            "timestamp": time.time(),
            "dna": SovereignAnchor.generate_dna("AUDIT"),
            "session_id": session_id,
            "action": action,
            "result": result,
            "detail": detail
        }
        self._audit_log.append(entry)
        # 同步到史官模块
        logger.info(f"📋 审计: {session_id} | {action} | {result}")

    def check(self, session_id: str, tokens: int = 1) -> bool:
        """
        检查是否允许通过（非阻塞）
        """
        if not self.config.enabled:
            return True

        bucket = self._get_bucket(session_id)
        success = bucket.consume(tokens)
        self._update_stats(session_id, tokens, success)

        if not success:
            self._audit(session_id, "check", "blocked", f"tokens={tokens}")
        else:
            self._audit(session_id, "check", "allowed", f"tokens={tokens}")

        return success

    def wait_and_check(self, session_id: str, tokens: int = 1) -> bool:
        """
        等待直到允许通过（阻塞）
        """
        if not self.config.enabled:
            return True

        bucket = self._get_bucket(session_id)
        success = bucket.wait_and_consume(tokens, timeout=self.config.timeout)
        self._update_stats(session_id, tokens, success)

        if not success:
            self._audit(session_id, "wait", "timeout", f"tokens={tokens}, timeout={self.config.timeout}")
            # 降级处理
            if self.config.fallback_action == "passthrough":
                logger.warning(f"⚠️ 流控超时，降级放行: {session_id}")
                return True
            elif self.config.fallback_action == "degrade":
                logger.warning(f"⚠️ 流控超时，降级限速: {session_id}")
                # 降级：强制降低速率到一半
                bucket.tokens_per_second = self.config.tokens_per_second * 0.5
                return bucket.wait_and_consume(tokens, timeout=self.config.timeout)
        else:
            self._audit(session_id, "wait", "allowed", f"tokens={tokens}")

        return success

    def process_stream(self, session_id: str, chunk_generator: Generator) -> Generator:
        """
        流式处理装饰器
        对生成器的每个 chunk 进行限流
        """
        if not self.config.enabled:
            for chunk in chunk_generator:
                yield chunk
            return

        bucket = self._get_bucket(session_id)
        for chunk in chunk_generator:
            chunk_len = len(chunk) if isinstance(chunk, (str, bytes)) else 1
            if not bucket.wait_and_consume(chunk_len, timeout=self.config.timeout):
                self._audit(session_id, "stream", "blocked", f"chunk_len={chunk_len}")
                if self.config.fallback_action == "block":
                    # 阻断流
                    break
                elif self.config.fallback_action == "passthrough":
                    # 降级放行
                    pass
            else:
                self._update_stats(session_id, chunk_len, True)
                self._audit(session_id, "stream", "allowed", f"chunk_len={chunk_len}")
            yield chunk

    def get_stats(self, session_id: Optional[str] = None) -> Dict:
        """获取统计信息"""
        if session_id:
            bucket = self._buckets.get(session_id)
            stats = self._stats[session_id]
            return {
                "session_id": session_id,
                "bucket": bucket.get_stats() if bucket else None,
                "stats": dict(stats),
                "config": self.config.to_dict()
            }

        # 汇总所有 session
        total_stats = {
            "sessions": len(self._buckets),
            "total_tokens": 0,
            "consumed_tokens": 0,
            "blocked": 0,
            "timeouts": 0,
            "config": self.config.to_dict()
        }
        for sid, stats in self._stats.items():
            total_stats["total_tokens"] += stats["total_tokens"]
            total_stats["consumed_tokens"] += stats["consumed_tokens"]
            total_stats["blocked"] += stats["blocked"]
            total_stats["timeouts"] += stats["timeouts"]
        return total_stats

    def get_audit_log(self, limit: int = 100) -> list:
        """获取审计日志"""
        return self._audit_log[-limit:]

    def update_config(self, config: RateLimitConfig):
        """动态更新配置"""
        self.config = config
        # 清空 bucket 重新创建（新的速率）
        with self._lock:
            self._buckets.clear()
        logger.info(f"✅ 流控配置已更新: {config.to_dict()}")


# ============================================================
# 三色审计对接
# ============================================================

class TricolorAudit:
    """三色审计·流控维度"""

    @staticmethod
    def audit_flow_control(plugin: RateLimiterPlugin) -> Dict:
        """
        对流控模块进行三色审计
        """
        stats = plugin.get_stats()
        config = plugin.config

        # 计算 R 值
        R = 100.0

        # 检查阻塞率
        total = stats.get("total_tokens", 1)
        blocked = stats.get("blocked", 0)
        block_rate = blocked / max(total, 1)

        if block_rate > 0.1:
            R -= 20  # 阻塞率 > 10%
        elif block_rate > 0.05:
            R -= 10  # 阻塞率 > 5%

        # 检查超时率
        timeouts = stats.get("timeouts", 0)
        timeout_rate = timeouts / max(total, 1)
        if timeout_rate > 0.05:
            R -= 15

        # 检查配置合理性
        if config.tokens_per_second < 10:
            R -= 10  # 速率太低

        # 判定三色
        if R >= 85:
            tricolor = "🟢"
            status = "通过"
        elif R >= 60:
            tricolor = "🟡"
            status = "警告"
        else:
            tricolor = "🔴"
            status = "异常"

        return {
            "tricolor": tricolor,
            "status": status,
            "R_value": round(R, 2),
            "stats": stats,
            "dna": SovereignAnchor.generate_dna("TRICOLOR-AUDIT"),
            "timestamp": time.time()
        }


# ============================================================
# 使用示例
# ============================================================

def demo():
    """演示流控模块"""

    print("\n🐉 龍魂流控模块 v1.0 演示")
    print("=" * 60)

    # 1. 创建插件
    config = RateLimitConfig(
        tokens_per_second=10.0,
        burst_size=5,
        timeout=2.0
    )
    plugin = RateLimiterPlugin(config)

    print(f"🧬 DNA: {plugin.dna}")

    # 2. 模拟请求
    session_id = "demo-user-001"
    print(f"\n📌 模拟请求 (session: {session_id})")

    for i in range(20):
        success = plugin.wait_and_check(session_id, tokens=1)
        status = "✅" if success else "❌"
        print(f"  请求 {i+1}: {status} (可用token: {plugin._get_bucket(session_id).get_available():.2f})")
        if i == 10:
            print("  ... 继续")

    # 3. 查看统计
    print("\n📊 统计信息:")
    stats = plugin.get_stats(session_id)
    print(f"  总token: {stats['stats']['total_tokens']}")
    print(f"  已消费: {stats['stats']['consumed_tokens']}")
    print(f"  阻塞: {stats['stats']['blocked']}")

    # 4. 三色审计
    print("\n🔍 三色审计:")
    audit = TricolorAudit.audit_flow_control(plugin)
    print(f"  三色: {audit['tricolor']}")
    print(f"  R值: {audit['R_value']}")
    print(f"  状态: {audit['status']}")

    # 5. 审计日志
    print("\n📋 审计日志 (最近3条):")
    for entry in plugin.get_audit_log(3):
        print(f"  {entry}")

    print("\n" + "=" * 60)
    print("✅ 演示完成")


if __name__ == "__main__":
    demo()
