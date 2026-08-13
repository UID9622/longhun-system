#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 AI 网关 · 流控模块 v1.1
Token Bucket + RateLimiterPlugin — 可配置·可审计·可降级

DNA: #龍芯⚡️丙午·丙申·丁巳·恒卦-FLOW-CONTROL-v1.1
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

v1.1 修复（Kimi实测验证·2026-08-11）:
  - Bug 1: wait_and_check() 缺 timeout 参数 → 已修复
  - Bug 2: 超时路径不统计 timeouts → 已修复
  - 增强: LRU会话管理·审计采样·降级恢复·租户解析

设计:
  - 纯标准库零依赖（可选 PyYAML 读配置）
  - Token Bucket 60行可审计实现
  - 多场景预设（default/chat/stream/batch/admin）
  - 三色审计自动上报
  - 降级: passthrough(放行) / degrade(半速) / block(拒绝)
  - DNA 由 lh_time_engine 算法生成（禁止手写干支）
"""

import hashlib
import json
import logging
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger("lh_flow_control")

# ─── 尝试导入时间引擎 ──────────────────────────────────
try:
    from bin.lh_time_engine import get_output_stamp
    def _build_dna() -> str:
        try:
            stamp = get_output_stamp()
            h = hashlib.sha256(stamp.encode()).hexdigest()[:8].upper()
            return f"{stamp.split(']')[0]}]-FLOW-CONTROL-{h}"
        except Exception:
            pass
        return _build_dna_fallback()
except ImportError:
    def _build_dna() -> str:
        return _build_dna_fallback()

def _build_dna_fallback() -> str:
    """降级：时间戳DNA（非手写干支）"""
    ts = time.strftime("%Y%m%d%H%M%S", time.localtime())
    h = hashlib.sha256(f"flow_control_{ts}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-FLOW-CONTROL-{h}"


# ═══════════════════════════════════════════════════════
# 枚举
# ═══════════════════════════════════════════════════════

class AuditMark(Enum):
    GREEN = "🟢"      # 通过
    YELLOW = "🟡"    # 待核
    RED = "🔴"       # 红线

class FallbackAction(Enum):
    PASSTHROUGH = "passthrough"  # 超时放行
    DEGRADE = "degrade"          # 降级半速
    BLOCK = "block"              # 直接拒绝


# ═══════════════════════════════════════════════════════
# 令牌桶
# ═══════════════════════════════════════════════════════

class TokenBucket:
    """标准令牌桶算法 — 线程安全"""

    def __init__(self, tokens_per_second: float, burst_size: int = 20):
        self.tokens_per_second = tokens_per_second
        self.burst_size = burst_size
        self.capacity = float(burst_size)
        self._tokens = float(burst_size)
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()
        self.created_at = time.time()
        self.last_access = time.time()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.tokens_per_second)
        self._last_refill = now

    def consume(self, tokens: int = 1) -> bool:
        """尝试消费，返回是否成功"""
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                self.last_access = time.time()
                return True
            self.last_access = time.time()
            return False

    def wait_and_consume(self, tokens: int = 1, timeout: float = 5.0) -> bool:
        """阻塞等待直到消费成功或超时"""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.consume(tokens):
                return True
            # 计算需要等待的时间
            with self._lock:
                needed = tokens - self._tokens
                wait_time = needed / self.tokens_per_second if self.tokens_per_second > 0 else 0.1
                wait_time = min(wait_time, 0.05)  # 最多等50ms一轮
            time.sleep(wait_time)
        # 最后一次尝试
        return self.consume(tokens)

    @property
    def available_tokens(self) -> float:
        with self._lock:
            self._refill()
            return max(0.0, self._tokens)


# ═══════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════

@dataclass
class RateLimitConfig:
    """流控配置
    
    🔥 P0焊死: tokens_per_second 默认值 = 100.0（不可修改默认值）
       触发条件: 任何新网关实例初始化
       行为: 自动加载，不询问、不等待
       例外: 无（覆盖需显式传入参数）
       DNA: #龍芯⚡️丙午·丙申·丁巳·恒卦-FLOW-CONTROL-v1.1-UID9622
    """
    enabled: bool = True
    tokens_per_second: float = 100.0       # 🔥 P0焊死·默认100 token/s·不询问不等待
    burst_size: int = 20                    # 突发容量
    timeout: float = 5.0                    # 默认超时(秒)
    fallback_action: FallbackAction = FallbackAction.PASSTHROUGH
    audit_sample_rate: float = 0.01         # allowed事件采样率(1%)
    max_sessions: int = 10000               # LRU上限
    degrade_duration: float = 60.0          # 降级恢复时间(秒)
    degrade_rate_multiplier: float = 0.5    # 降级速率乘数


# 场景预设
SCENE_CONFIGS: Dict[str, RateLimitConfig] = {
    "default": RateLimitConfig(
        tokens_per_second=100.0,
        burst_size=20,
        timeout=5.0,
        fallback_action=FallbackAction.PASSTHROUGH,
    ),
    "stream": RateLimitConfig(
        tokens_per_second=100.0,
        burst_size=30,
        timeout=3.0,
        fallback_action=FallbackAction.PASSTHROUGH,
    ),
    "chat": RateLimitConfig(
        tokens_per_second=50.0,
        burst_size=15,
        timeout=10.0,
        fallback_action=FallbackAction.PASSTHROUGH,
    ),
    "batch": RateLimitConfig(
        tokens_per_second=200.0,
        burst_size=50,
        timeout=30.0,
        fallback_action=FallbackAction.DEGRADE,
    ),
    "admin": RateLimitConfig(
        tokens_per_second=500.0,
        burst_size=100,
        timeout=5.0,
        fallback_action=FallbackAction.PASSTHROUGH,
    ),
}


# ═══════════════════════════════════════════════════════
# 审计
# ═══════════════════════════════════════════════════════

class TricolorAudit:
    """三色审计日志"""

    def __init__(self, log_path: Optional[Path] = None):
        self.log_path = log_path or (Path(__file__).resolve().parent.parent / "logs" / "flow_control_audit.jsonl")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def log(self, session_id: str, event_type: str, result: str,
            detail: str = "", dna: str = "") -> None:
        """追加审计日志"""
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
            "session_id": session_id,
            "event": event_type,
            "result": result,
            "detail": detail,
            "dna": dna or _build_dna(),
        }
        with self._lock:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ═══════════════════════════════════════════════════════
# 流控插件（核心）
# ═══════════════════════════════════════════════════════

class RateLimiterPlugin:
    """
    龍魂流控插件 v1.1

    使用:
        plugin = RateLimiterPlugin(RateLimitConfig(tokens_per_second=100))
        plugin.check_and_consume("session_001", tokens=1)  # 非阻塞
        plugin.wait_and_check("session_001", tokens=1, timeout=2.0)  # 阻塞
    """

    def __init__(self, config: Optional[RateLimitConfig] = None, scene: str = "default"):
        self.config = config or SCENE_CONFIGS.get(scene, SCENE_CONFIGS["default"])
        self.scene = scene
        self._buckets: OrderedDict[str, TokenBucket] = OrderedDict()
        self._stats: Dict[str, Dict[str, int]] = {}
        self._lock = threading.Lock()
        self._auditor = TricolorAudit()
        self._degraded_buckets: Dict[str, Tuple[float, float]] = {}  # bucket_id -> (degrade_time, original_rate)

    # ── 桶管理 ──────────────────────────────────────

    def _get_bucket(self, session_id: str) -> TokenBucket:
        """获取或创建令牌桶（LRU淘汰）"""
        with self._lock:
            if session_id in self._buckets:
                # 移到末尾（最近使用）
                self._buckets.move_to_end(session_id)
                return self._buckets[session_id]

            # LRU淘汰
            while len(self._buckets) >= self.config.max_sessions:
                self._buckets.popitem(last=False)

            bucket = TokenBucket(
                tokens_per_second=self.config.tokens_per_second,
                burst_size=self.config.burst_size,
            )
            self._buckets[session_id] = bucket
            self._stats[session_id] = {"allowed": 0, "blocked": 0, "timeouts": 0, "total_tokens": 0}
            return bucket

    # ── 租户配置解析 ────────────────────────────────

    def resolve_tenant_config(self, session_id: str,
                               tenants: Optional[Dict[str, RateLimitConfig]] = None) -> RateLimitConfig:
        """按session_id前缀匹配租户配置，优先级 tenants > scenes > default"""
        if tenants:
            for prefix, cfg in sorted(tenants.items(), key=lambda x: -len(x[0])):
                if session_id.startswith(prefix):
                    return cfg
        return self.config

    # ── 统计 ────────────────────────────────────────

    def _update_stats(self, session_id: str, tokens: int, success: bool) -> None:
        with self._lock:
            if session_id not in self._stats:
                self._stats[session_id] = {"allowed": 0, "blocked": 0, "timeouts": 0, "total_tokens": 0}
            stats = self._stats[session_id]
            stats["total_tokens"] += tokens
            if success:
                stats["allowed"] += 1
            else:
                stats["blocked"] += 1

    # ── 审计 ────────────────────────────────────────

    def _audit(self, session_id: str, event_type: str, result: str, detail: str = "") -> None:
        """审计日志：allowed采样(1%)，blocked/timeout 100%落盘"""
        if result == "allowed":
            if hash(f"{session_id}{time.time()}") % 100 >= self.config.audit_sample_rate * 100:
                return
        self._audit.log(session_id, event_type, result, detail)

    # ── 非阻塞检查 ──────────────────────────────────

    def check_and_consume(self, session_id: str, tokens: int = 1) -> bool:
        """非阻塞：立即尝试消费，返回成功/失败"""
        if not self.config.enabled:
            return True
        bucket = self._get_bucket(session_id)
        success = bucket.consume(tokens)
        self._update_stats(session_id, tokens, success)
        if success:
            self._auditor.log(session_id, "check", "allowed", f"tokens={tokens}")
        else:
            self._auditor.log(session_id, "check", "blocked", f"tokens={tokens}")
            logger.warning(f"🚫 流控拒绝: {session_id} (tokens={tokens})")
        return success

    # ── 阻塞等待（v1.1修复：timeout参数+timeouts统计） ─

    def wait_and_check(self, session_id: str, tokens: int = 1,
                       timeout: Optional[float] = None) -> bool:
        """
        阻塞等待直到通过或超时。
        timeout=None 时使用 config.timeout。
        """
        if not self.config.enabled:
            return True
        eff_timeout = self.config.timeout if timeout is None else timeout
        bucket = self._get_bucket(session_id)

        # 检查是否在降级恢复中
        if session_id in self._degraded_buckets:
            degraded_at, original_rate = self._degraded_buckets[session_id]
            if time.time() - degraded_at < self.config.degrade_duration:
                pass  # 仍在降级中，使用降级速率
            else:
                # 恢复原始速率
                bucket.tokens_per_second = original_rate
                del self._degraded_buckets[session_id]
                logger.info(f"🔄 流控恢复: {session_id} → {original_rate} t/s")
                self._auditor.log(session_id, "recover", "allowed",
                            f"restored_rate={original_rate}")

        success = bucket.wait_and_consume(tokens, timeout=eff_timeout)
        self._update_stats(session_id, tokens, success)

        if not success:
            # v1.1修复：超时路径计入 stats["timeouts"]
            with self._lock:
                if session_id in self._stats:
                    self._stats[session_id]["timeouts"] += 1
            self._auditor.log(session_id, "wait", "timeout",
                        f"tokens={tokens}, timeout={eff_timeout}")

            if self.config.fallback_action == FallbackAction.PASSTHROUGH:
                logger.warning(f"⚠️ 流控超时，降级放行: {session_id}")
                return True
            elif self.config.fallback_action == FallbackAction.DEGRADE:
                logger.warning(f"⚠️ 流控超时，降级限速: {session_id}")
                original_rate = bucket.tokens_per_second
                bucket.tokens_per_second = self.config.tokens_per_second * self.config.degrade_rate_multiplier
                self._degraded_buckets[session_id] = (time.time(), original_rate)
                # 降级后重试用更长超时（如5s），确保有机会获得token
                degrade_timeout = max(eff_timeout, 5.0)
                return bucket.wait_and_consume(tokens, timeout=degrade_timeout)
            else:  # BLOCK
                return False
        else:
            self._auditor.log(session_id, "wait", "allowed", f"tokens={tokens}")
        return success

    # ── 配置管理 ────────────────────────────────────

    def update_config(self, new_config: RateLimitConfig) -> None:
        """热更新配置（保留在途会话状态）"""
        old_tps = self.config.tokens_per_second
        self.config = new_config
        with self._lock:
            for sid, bucket in self._buckets.items():
                if bucket.tokens_per_second == old_tps:
                    bucket.tokens_per_second = new_config.tokens_per_second
                    bucket.burst_size = new_config.burst_size
                    bucket.capacity = float(new_config.burst_size)
        logger.info(f"🔄 流控配置已更新: {new_config.tokens_per_second} t/s")

    # ── 查询 ────────────────────────────────────────

    def get_stats(self, session_id: Optional[str] = None) -> Dict:
        """获取统计信息"""
        with self._lock:
            if session_id:
                return dict(self._stats.get(session_id, {}))
            total = {"allowed": 0, "blocked": 0, "timeouts": 0, "total_tokens": 0, "active_sessions": len(self._buckets)}
            for ss in self._stats.values():
                for k in ("allowed", "blocked", "timeouts", "total_tokens"):
                    total[k] += ss.get(k, 0)
            return total

    def get_metrics(self) -> str:
        """Prometheus 格式指标"""
        stats = self.get_stats()
        lines = [
            "# HELP longhun_flow_requests_total 流控请求总数",
            "# TYPE longhun_flow_requests_total counter",
            f"longhun_flow_requests_total{{result=\"allowed\"}} {stats['allowed']}",
            f"longhun_flow_requests_total{{result=\"blocked\"}} {stats['blocked']}",
            f"longhun_flow_requests_total{{result=\"timeout\"}} {stats['timeouts']}",
            "# HELP longhun_flow_tokens_total 流控令牌消耗总量",
            "# TYPE longhun_flow_tokens_total counter",
            f"longhun_flow_tokens_total {stats['total_tokens']}",
            "# HELP longhun_flow_active_sessions 活跃会话数",
            "# TYPE longhun_flow_active_sessions gauge",
            f"longhun_flow_active_sessions {stats['active_sessions']}",
        ]
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════
# 流式输出包装器
# ═══════════════════════════════════════════════════════

def process_stream(generator, plugin: RateLimiterPlugin, session_id: str,
                   chunk_token_ratio: float = 1.0) -> str:
    """
    对流式生成器施加流控。

    Args:
        generator: 流式chunk生成器 (yield str)
        plugin: RateLimiterPlugin实例
        session_id: 会话ID
        chunk_token_ratio: 每个字符≈多少token（默认1.0，即1字符=1token）

    Yields:
        限速后的chunk
    """
    for chunk in generator:
        # 估算chunk的token数
        estimated_tokens = max(1, int(len(chunk) * chunk_token_ratio))
        # 阻塞等待令牌
        if not plugin.wait_and_check(session_id, tokens=estimated_tokens):
            logger.error(f"🚫 流式输出被阻断: {session_id}")
            break
        yield chunk


def create_plugin(tokens_per_second: float = 100.0,
                  burst_size: int = 20,
                  fallback: str = "passthrough",
                  scene: str = "default") -> RateLimiterPlugin:
    """
    快捷创建流控插件。

    🔥 P0焊死·铁律: 默认值 tokens_per_second=100 不可修改。
       新网关实例默认加载 100 t/s，自动开，不询问，不等待。
       覆盖需显式传参。例外: 无。
       DNA: #龍芯⚡️丙午·丙申·丁巳·恒卦-FLOW-CONTROL-v1.1-UID9622

    Args:
        tokens_per_second: 每秒令牌数（默认100·P0焊死）
        burst_size: 突发容量
        fallback: passthrough/degrade/block
        scene: 场景名（覆盖默认配置）
    """
    config = RateLimitConfig(
        tokens_per_second=tokens_per_second,
        burst_size=burst_size,
        fallback_action=FallbackAction(fallback),
    )
    return RateLimiterPlugin(config=config, scene=scene)


# ═══════════════════════════════════════════════════════
# 演示 & 自测
# ═══════════════════════════════════════════════════════

def demo():
    """快速演示"""
    plugin = create_plugin(tokens_per_second=10, burst_size=20)
    session = "demo_session"

    print("=" * 60)
    print("🐉 龍魂流控模块 v1.1 演示")
    print(f"   配置: 10 token/s, burst=20, fallback=passthrough")
    print(f"   DNA: {_build_dna()}")
    print("=" * 60)

    # 突发测试：前20请求应全通过
    print("\n📊 突发测试（前20请求）:")
    passed = sum(1 for i in range(20) if plugin.check_and_consume(session))
    print(f"   通过: {passed}/20")

    # 超限测试
    print("\n📊 超限测试（无等待，立即消费）:")
    results = [plugin.check_and_consume(session) for _ in range(5)]
    print(f"   通过: {sum(1 for r in results if r)}/5")

    # 等待测试
    print("\n📊 等待测试（timeout=2s）:")
    ok = plugin.wait_and_check(session, tokens=1, timeout=2.0)
    print(f"   结果: {'✅ 通过' if ok else '❌ 超时/拒绝'}")

    # 统计
    stats = plugin.get_stats(session)
    print(f"\n📊 会话统计:")
    print(f"   放行: {stats['allowed']}  拒绝: {stats['blocked']}  超时: {stats['timeouts']}  令牌: {stats['total_tokens']}")

    # 全局统计
    global_stats = plugin.get_stats()
    print(f"\n📊 全局统计:")
    print(f"   活跃会话: {global_stats['active_sessions']}")
    print(f"   总放行: {global_stats['allowed']}  总拒绝: {global_stats['blocked']}  总超时: {global_stats['timeouts']}")

    # Prometheus指标
    print(f"\n📊 Prometheus指标:")
    print(plugin.get_metrics())

    print("\n✅ 演示完成 🟢")


if __name__ == "__main__":
    demo()
