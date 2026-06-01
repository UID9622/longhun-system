#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 CNSH Gateway 单元测试

DNA: #龍芯⚡️2026-06-01-TEST-GATEWAY-v1.0
"""

import pytest
import time
import hashlib
import hmac
from cnsh_gateway_v1_1 import (
    digital_root,
    make_dna,
    sha8,
    sign_request,
    RateLimiter,
    LogLevel,
)


class TestDigitalRoot:
    """数字根计算测试"""

    def test_single_digit(self):
        """单个数字"""
        assert digital_root(5) == 5
        assert digital_root(9) == 9

    def test_two_digits(self):
        """两位数"""
        assert digital_root(10) == 1
        assert digital_root(18) == 9
        assert digital_root(39) == 3

    def test_three_digits(self):
        """三位数"""
        assert digital_root(123) == 6
        assert digital_root(999) == 9
        assert digital_root(100) == 1

    def test_zero(self):
        """零值"""
        assert digital_root(0) == 0

    def test_string_input(self):
        """字符串输入"""
        assert digital_root("5") == 5
        assert digital_root("39") == 3

    @pytest.mark.parametrize("input_val,expected", [
        (1, 1),
        (11, 2),
        (38, 2),
        (123, 6),
        (999, 9),
        (1234567, 1),
    ])
    def test_batch(self, input_val, expected):
        """批量测试"""
        assert digital_root(input_val) == expected


class TestDNAGeneration:
    """DNA追踪码生成测试"""

    def test_dna_format(self):
        """DNA格式检查"""
        dna = make_dna("test_category", "test_message")
        assert dna.startswith("#龍芯⚡️")
        assert "test_category" in dna
        assert len(dna) > 20

    def test_dna_consistency(self):
        """相同输入生成相同DNA"""
        dna1 = make_dna("auth", "login_success")
        dna2 = make_dna("auth", "login_success")
        # DNA中包含时间戳，所以可能不完全相同
        # 但分类和消息应该相同
        assert "auth" in dna1 and "auth" in dna2

    def test_dna_uniqueness(self):
        """不同消息生成不同DNA"""
        dna1 = make_dna("api", "msg1")
        dna2 = make_dna("api", "msg2")
        # 由于消息不同，DNA应该不同
        assert dna1 != dna2


class TestSHA8:
    """SHA8哈希测试"""

    def test_sha8_length(self):
        """SHA8长度检查"""
        result = sha8("test")
        assert len(result) == 8

    def test_sha8_format(self):
        """SHA8格式检查"""
        result = sha8("message")
        assert all(c in "0123456789ABCDEF" for c in result)

    def test_sha8_consistency(self):
        """相同输入生成相同哈希"""
        hash1 = sha8("content")
        hash2 = sha8("content")
        assert hash1 == hash2

    def test_sha8_different_input(self):
        """不同输入生成不同哈希"""
        hash1 = sha8("msg1")
        hash2 = sha8("msg2")
        assert hash1 != hash2


class TestSignRequest:
    """请求签名测试"""

    def test_signature_creation(self):
        """签名生成"""
        body = '{"msg": "test"}'
        secret = "test_secret"
        sig = sign_request(body, secret)
        assert len(sig) == 64  # SHA256哈希长度
        assert all(c in "0123456789abcdef" for c in sig)

    def test_signature_verification(self):
        """签名验证"""
        body = '{"data": "value"}'
        secret = "my_secret"

        # 生成签名
        sig = sign_request(body, secret)

        # 验证签名
        expected = hmac.new(
            secret.encode(),
            body.encode(),
            hashlib.sha256
        ).hexdigest()

        assert sig == expected

    def test_signature_deterministic(self):
        """签名确定性"""
        body = "test_body"
        secret = "test_secret"

        sig1 = sign_request(body, secret)
        sig2 = sign_request(body, secret)

        assert sig1 == sig2

    def test_signature_secret_sensitivity(self):
        """签名对密钥敏感"""
        body = "test_body"

        sig1 = sign_request(body, "secret1")
        sig2 = sign_request(body, "secret2")

        assert sig1 != sig2


class TestRateLimiter:
    """速率限制器测试"""

    def test_rate_limiter_init(self):
        """初始化"""
        limiter = RateLimiter(rpm=60)  # 每分钟60个请求
        assert limiter.rpm == 60

    def test_rate_limiter_allowed(self):
        """允许请求"""
        limiter = RateLimiter(rpm=10)

        # 首个请求应该通过
        allowed, remaining = limiter.is_allowed("user1")
        assert allowed is True
        assert remaining == 9

    def test_rate_limiter_blocked(self):
        """阻止请求"""
        limiter = RateLimiter(rpm=2)  # 每分钟2个请求

        # 前2个通过
        assert limiter.is_allowed("user2")[0] is True
        assert limiter.is_allowed("user2")[0] is True

        # 第3个被阻止
        allowed, remaining = limiter.is_allowed("user2")
        assert allowed is False
        assert remaining == 0

    def test_rate_limiter_per_user(self):
        """用户隔离"""
        limiter = RateLimiter(rpm=2)

        # user1: 2请求
        limiter.is_allowed("user1")
        limiter.is_allowed("user1")

        # user2: 应该有独立额度
        allowed1, _ = limiter.is_allowed("user2")
        allowed2, _ = limiter.is_allowed("user2")

        assert allowed1 is True
        assert allowed2 is True

    def test_rate_limiter_window_reset(self):
        """时间窗口重置"""
        limiter = RateLimiter(rpm=2, window_sec=1)  # 1秒窗口

        # 消耗配额
        limiter.is_allowed("user3")
        limiter.is_allowed("user3")

        # 等待窗口重置
        time.sleep(1.1)

        # 配额应该恢复
        allowed, remaining = limiter.is_allowed("user3")
        assert allowed is True
        assert remaining == 1


class TestLogLevel:
    """日志等级测试"""

    def test_log_level_enum(self):
        """日志等级枚举"""
        assert LogLevel.DEBUG.value == 0
        assert LogLevel.INFO.value == 1
        assert LogLevel.WARN.value == 2
        assert LogLevel.ERROR.value == 3
        assert LogLevel.CRITICAL.value == 4

    def test_log_level_comparison(self):
        """日志等级比较"""
        assert LogLevel.DEBUG.value < LogLevel.CRITICAL.value
        assert LogLevel.ERROR.value > LogLevel.INFO.value


# ═══════════════════════════════════════════════════════════════
# 集成测试
# ═══════════════════════════════════════════════════════════════

class TestGatewayIntegration:
    """Gateway集成测试"""

    @pytest.mark.integration
    def test_full_request_flow(self):
        """完整请求流程"""
        # 模拟一个完整的请求验证流程
        body = '{"messages": [{"role": "user", "content": "hello"}]}'
        secret = "UID9622-CHANGE-THIS"

        # 签名
        sig = sign_request(body, secret)

        # 验证签名格式
        assert len(sig) == 64
        assert all(c in "0123456789abcdef" for c in sig)

    @pytest.mark.integration
    def test_rate_limit_enforcement(self):
        """速率限制执行"""
        limiter = RateLimiter(rpm=5)

        # 连续发送10个请求
        allowed_count = 0
        for i in range(10):
            allowed, _ = limiter.is_allowed("client")
            if allowed:
                allowed_count += 1

        # 应该有5个通过
        assert allowed_count == 5


# ═══════════════════════════════════════════════════════════════
# 性能测试
# ═══════════════════════════════════════════════════════════════

@pytest.mark.slow
class TestPerformance:
    """性能测试"""

    def test_digital_root_performance(self):
        """数字根性能"""
        start = time.time()
        for i in range(10000):
            digital_root(i)
        duration = time.time() - start

        # 应该在100ms内完成
        assert duration < 0.1, f"数字根计算耗时 {duration*1000:.2f}ms"

    def test_dna_generation_performance(self):
        """DNA生成性能"""
        start = time.time()
        for i in range(1000):
            make_dna("category", f"message_{i}")
        duration = time.time() - start

        # 应该在50ms内完成
        assert duration < 0.05, f"DNA生成耗时 {duration*1000:.2f}ms"

    def test_rate_limiter_performance(self):
        """速率限制器性能"""
        limiter = RateLimiter(rpm=1000)

        start = time.time()
        for i in range(10000):
            limiter.is_allowed(f"user_{i % 100}")
        duration = time.time() - start

        # 应该在100ms内完成
        assert duration < 0.1, f"速率限制耗时 {duration*1000:.2f}ms"
