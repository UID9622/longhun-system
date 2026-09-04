# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-24cb3e64
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
import sys; sys.path.insert(0,"/tmp")
from flow_control_v11 import *
import unittest, time

class TestRateLimiter(unittest.TestCase):

    def test_basic_limit(self):
        """测试基础限流"""
        config = RateLimitConfig(tokens_per_second=10, burst_size=5)
        plugin = RateLimiterPlugin(config)
        session = "test-001"

        # 前5个应该通过
        for i in range(5):
            self.assertTrue(plugin.check(session))

        # 第6个应该被阻塞
        self.assertFalse(plugin.check(session))

    def test_wait_and_check(self):
        """测试等待限流"""
        config = RateLimitConfig(tokens_per_second=10, burst_size=5)
        plugin = RateLimiterPlugin(config)
        session = "test-002"

        # 消耗完 token
        for i in range(5):
            plugin.check(session)

        # 等待限流应该等待
        start = time.time()
        success = plugin.wait_and_check(session, tokens=1, timeout=2.0)
        elapsed = time.time() - start

        # 应该等待至少 0.1 秒
        self.assertTrue(success)
        self.assertGreater(elapsed, 0.05)

    def test_stream_limiting(self):
        """测试流式限流"""
        config = RateLimitConfig(tokens_per_second=10, burst_size=5)
        plugin = RateLimiterPlugin(config)
        session = "test-003"

        def gen():
            for i in range(20):
                yield f"chunk-{i}"

        chunks = []
        for chunk in plugin.process_stream(session, gen()):
            chunks.append(chunk)

        # 可能因为限流被截断
        self.assertLessEqual(len(chunks), 15)  # 20个chunk，但速率限制

    def test_fallback_degrade(self):
        """测试降级策略"""
        config = RateLimitConfig(
            tokens_per_second=10,
            burst_size=5,
            fallback_action="degrade"
        )
        plugin = RateLimiterPlugin(config)
        session = "test-004"

        # 消耗完token
        for i in range(5):
            plugin.check(session)

        # 降级后应该仍然能通过（虽然变慢）
        success = plugin.wait_and_check(session, tokens=1, timeout=3.0)
        self.assertTrue(success)
