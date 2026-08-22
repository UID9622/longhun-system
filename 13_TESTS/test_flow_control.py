#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
龍魂流控模块 v1.1 测试套件
4 测试用例 — 对应协议 v1.1 验收标准

DNA: #龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-FLOW-CONTROL-TEST-v1.1
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2

v1.1 修复验证:
  - Bug 1: wait_and_check() 缺 timeout 参数 → 已修复（test_wait_and_check）
  - Bug 2: 超时路径不统计 timeouts → 已修复（test_timeout_stats）
"""

import sys
import time
import unittest
from pathlib import Path

# 确保引擎路径可导入
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "engines"))

from engines.lh_flow_control import (
    TokenBucket,
    RateLimitConfig,
    RateLimiterPlugin,
    FallbackAction,
    create_plugin,
)


class TestTokenBucket(unittest.TestCase):
    """令牌桶基础测试"""

    def test_consume_within_burst(self):
        """突发内消费全部通过"""
        bucket = TokenBucket(tokens_per_second=10, burst_size=20)
        passed = sum(1 for _ in range(20) if bucket.consume())
        self.assertEqual(passed, 20, "突发的20个请求应全部通过")

    def test_consume_beyond_burst(self):
        """超出突发后拒绝"""
        bucket = TokenBucket(tokens_per_second=10, burst_size=5)
        # 消耗完突发
        for _ in range(5):
            bucket.consume()
        # 第6个应立即失败
        self.assertFalse(bucket.consume(), "超出burst后应立即拒绝")

    def test_refill_over_time(self):
        """令牌随时间的补充"""
        bucket = TokenBucket(tokens_per_second=100, burst_size=10)
        # 消耗完
        for _ in range(10):
            bucket.consume()
        self.assertFalse(bucket.consume())
        # 等待0.02秒（100 tps = 2 tokens/0.02s）
        time.sleep(0.02)
        self.assertTrue(bucket.consume(), "0.02s后应有至少1个token")

    def test_wait_and_consume_timeout(self):
        """等待消费超时"""
        bucket = TokenBucket(tokens_per_second=10, burst_size=5)
        for _ in range(5):
            bucket.consume()
        # 请求50个token，0.1s内不可能补充到
        start = time.monotonic()
        result = bucket.wait_and_consume(tokens=50, timeout=0.1)
        elapsed = time.monotonic() - start
        self.assertFalse(result, "请求大量token在小超时内应失败")
        self.assertLess(elapsed, 0.3, "超时控制应生效")


class TestRateLimiterPlugin(unittest.TestCase):
    """RateLimiterPlugin 集成测试"""

    def setUp(self):
        self.plugin = create_plugin(tokens_per_second=10, burst_size=20)

    def test_basic_limit(self):
        """基础流控：突发通过，超限拒绝"""
        session = "test_basic"
        # 突发20请求全通过
        passed = sum(1 for _ in range(20) if self.plugin.check_and_consume(session))
        self.assertEqual(passed, 20)
        # 第21个拒绝
        self.assertFalse(self.plugin.check_and_consume(session))

    def test_stream_limiting(self):
        """流式限速：逐token消费"""
        session = "test_stream"
        # 连续快速消费，检验速率
        passed = sum(1 for _ in range(10) if self.plugin.check_and_consume(session, tokens=2))
        # 10 * 2 = 20 tokens，burst=20 全部通过
        self.assertEqual(passed, 10)

    def test_wait_and_check(self):
        """v1.1 核心修复：wait_and_check 带 timeout 参数"""
        session = "test_wait"
        # 消耗完突发
        for _ in range(20):
            self.plugin.check_and_consume(session)

        # wait_and_check(timeout=2.0) — v1.0会报TypeError，v1.1应正常工作
        start = time.monotonic()
        ok = self.plugin.wait_and_check(session, tokens=1, timeout=2.0)
        elapsed = time.monotonic() - start
        self.assertTrue(ok, "passthrough模式应放行")
        # 如果立即放行（passthrough），耗时应该很短
        if elapsed > 2.5:
            self.fail(f"超时控制失效: elapsed={elapsed:.2f}s")

    def test_fallback_degrade(self):
        """v1.1 降级测试"""
        config = RateLimitConfig(
            tokens_per_second=1,  # 极低速率
            burst_size=1,
            timeout=0.1,
            fallback_action=FallbackAction.DEGRADE,
        )
        plugin = RateLimiterPlugin(config=config)
        session = "test_degrade"
        # 消耗完唯一的burst
        plugin.check_and_consume(session)
        # wait_and_check 应触发degrade
        ok = plugin.wait_and_check(session, tokens=1, timeout=0.1)
        self.assertTrue(ok, "degrade模式应降级放行")

    def test_timeout_stats(self):
        """v1.1 修复：timeouts 统计正确"""
        config = RateLimitConfig(
            tokens_per_second=1,
            burst_size=1,
            timeout=0.05,
            fallback_action=FallbackAction.BLOCK,  # block模式，不允许passthrough
        )
        plugin = RateLimiterPlugin(config=config)
        session = "test_timeout_stats"
        # 消耗掉唯一token
        plugin.check_and_consume(session)
        # 立即尝试消费，应触发超时
        plugin.wait_and_check(session, tokens=1, timeout=0.05)

        stats = plugin.get_stats(session)
        self.assertGreater(stats.get("timeouts", 0), 0,
                           f"timeouts应为>0，但实际是{stats.get('timeouts', 'N/A')}")

    def test_multi_session_isolation(self):
        """多会话隔离"""
        p1 = self.plugin.check_and_consume("session_a", tokens=10)
        p2 = self.plugin.check_and_consume("session_b", tokens=10)
        self.assertTrue(p1 and p2, "两个独立会话不互相影响")
        stats_a = self.plugin.get_stats("session_a")
        stats_b = self.plugin.get_stats("session_b")
        self.assertEqual(stats_a["total_tokens"], 10)
        self.assertEqual(stats_b["total_tokens"], 10)

    def test_lru_eviction(self):
        """LRU 淘汰"""
        config = RateLimitConfig(
            tokens_per_second=100,
            burst_size=100,
            max_sessions=5,
        )
        plugin = RateLimiterPlugin(config=config)
        # 创建10个会话
        for i in range(10):
            plugin.check_and_consume(f"session_{i}")
        stats = plugin.get_stats()
        self.assertLessEqual(stats["active_sessions"], 5,
                             f"LRU应限制在5以内，但实际有{stats['active_sessions']}")

    def test_update_config(self):
        """热更新配置"""
        old_stats = self.plugin.get_stats()
        self.plugin.update_config(RateLimitConfig(tokens_per_second=200, burst_size=50))
        self.assertEqual(self.plugin.config.tokens_per_second, 200)
        # 已在途的会话bucket速率应更新
        session = "test_config_update"
        self.plugin.check_and_consume(session, tokens=1)
        new_stats = self.plugin.get_stats(session)
        self.assertGreaterEqual(new_stats["total_tokens"], 1)

    def test_metrics_output(self):
        """Prometheus 指标输出"""
        self.plugin.check_and_consume("test_metrics")
        metrics = self.plugin.get_metrics()
        self.assertIn("longhun_flow_requests_total", metrics)
        self.assertIn("longhun_flow_tokens_total", metrics)
        self.assertIn("longhun_flow_active_sessions", metrics)

    def test_disabled(self):
        """禁用时全放行"""
        config = RateLimitConfig(enabled=False)
        plugin = RateLimiterPlugin(config=config)
        for i in range(100):
            self.assertTrue(plugin.check_and_consume("any"), f"禁用时应全部放行 (第{i}次)")


if __name__ == "__main__":
    # 用 unittest 运行，但更友好的输出
    print("=" * 60)
    print("🐉 龍魂流控 v1.1 测试套件")
    print("=" * 60)
    result = unittest.main(verbosity=2, exit=False)
    passed = result.result.testsRun - len(result.result.failures) - len(result.result.errors)
    total = result.result.testsRun
    print(f"\n{'='*60}")
    print(f"📊 结果: {passed}/{total} 通过"
          f"  🟢" if passed == total else f"  🔴 {len(result.result.failures) + len(result.result.errors)} 失败")
    print(f"{'='*60}")
    sys.exit(0 if result.result.wasSuccessful() else 1)
