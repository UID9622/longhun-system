#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·己酉·亥时·䷾既济-LH-API-NORM-TEST-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
lh_api._norm 路径归一单元测试（v1.0 · 2026-09-05）

背景: v2.3 ADS 融合时现场抓到 bug——_norm 未剥 query，带 `?confirm=` 的
请求归一后 path 仍含 query，导致 _serve_self 的 seg 失配返回 404。
修复: _norm 先 urlparse 剥 query 再 unquote（路由判定只认路径·query 由端点自取）。
本测试将「query 不混入路由判定」焊为回归用例，防后续扩路由复踩。
"""
import sys
import unittest
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import lh_api  # noqa: E402


def norm(raw: str) -> str:
    """_norm 不依赖实例状态 → 免构造 Handler 直接 unbound 调用。"""
    h = object.__new__(lh_api.Handler)
    return lh_api.Handler._norm(h, raw)


class TestNormPathClean(unittest.TestCase):
    """无 query 场景：归一只剥 /api[/v1] 前缀 + 尾部斜杠。"""

    def test_plain_v1(self):
        self.assertEqual(norm("/v1/lh"), "/v1/lh")

    def test_api_prefix_stripped(self):
        self.assertEqual(norm("/api/v1/lh"), "/lh")

    def test_self_health_api_v1(self):
        self.assertEqual(norm("/api/v1/self/health"), "/self/health")

    def test_self_bare_becomes_health(self):
        # _serve_self 里空 seg 回落 health（在网关分支层·_norm 只管前缀）
        self.assertEqual(norm("/v1/self"), "/v1/self")

    def test_trailing_slash(self):
        self.assertEqual(norm("/v1/topo/"), "/v1/topo")

    def test_root(self):
        self.assertEqual(norm("/"), "/")


class TestNormQueryStripped(unittest.TestCase):
    """v2.3 bug 回归：query 必须被剥离，不得混入路由判定。"""

    def test_query_simple(self):
        self.assertEqual(norm("/v1/self/health?confirm=x"), "/v1/self/health")

    def test_query_confirm_code(self):
        # 真实确认码（%23# + emoji 百分号编码）不得污染 path
        self.assertEqual(
            norm("/v1/self/health?confirm=%23CONFIRM%F0%9F%8C%8C9622-ONLY-ONCE%F0%9F%A7%ACLK9X-772Z"),
            "/v1/self/health")

    def test_query_memorial(self):
        self.assertEqual(norm("/memorial/verify?code=1"), "/memorial/verify")

    def test_query_api_prefix(self):
        self.assertEqual(norm("/api/v1/judge/shamewall?refresh=1"), "/judge/shamewall")


if __name__ == "__main__":
    unittest.main(verbosity=2)
