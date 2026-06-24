#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XPay 主权网关单元测试
DNA:#龍芯⚡️2026-06-17-XPAY-TESTS-v2.0
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from xpay.src.core import SovereignGateway


def test_cny_pay():
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "xpay_test.db"
        gw = SovereignGateway(db_path=db)

        result = gw.pay(amount=100.0, currency="CNY", recipient="UID1001", memo="测试")
        assert result["success"] is True
        assert result["currency"] == "CNY"
        assert result["fees"]["processing"] == 0.0
        assert result["fees"]["dna"] == 0.001
        assert result["dna_signature"].startswith("#龍芯⚡️")

        tx = gw.query(result["tx_id"])
        assert tx is not None
        assert tx["recipient_id"] == "UID1001"
        print("✅ CNY 支付测试通过")


def test_usd_pay():
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "xpay_test.db"
        gw = SovereignGateway(db_path=db)

        result = gw.pay(amount=100.0, currency="USD", recipient="UID1002")
        assert result["success"] is True
        assert result["fees"]["processing"] == 0.5
        assert result["fees"]["dna"] == 0.01
        print("✅ USD 支付测试通过")


def test_unsupported_currency():
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "xpay_test.db"
        gw = SovereignGateway(db_path=db)

        result = gw.pay(amount=10.0, currency="BTC", recipient="UID1003")
        assert result["success"] is False
        assert "不支持的币种" in result["error"]
        print("✅ 不支持的币种测试通过")


def test_stats():
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "xpay_test.db"
        gw = SovereignGateway(db_path=db)
        gw.pay(10.0, "CNY", "UID1001")
        gw.pay(20.0, "CNY", "UID1002")
        stats = gw.stats()
        assert stats["transaction_count"] == 2
        assert stats["total_volume"] == 30.0
        print("✅ 统计测试通过")


if __name__ == "__main__":
    test_cny_pay()
    test_usd_pay()
    test_unsupported_currency()
    test_stats()
    print("\n🐉 所有 XPay 主权网关测试通过")
