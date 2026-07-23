#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂生态对齐测试 · 河图洛书 × 易经 × 七因子
DNA: #龍芯⚡️2026-07-05-ECOSYSTEM-ALIGNMENT-TEST-v1.0
"""

import json
import sys
from pathlib import Path

ECO_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ECO_DIR))

from hetu_luoshu_yijing_sevenfactor_bridge import (
    audit_with_ecosystem,
    digital_root,
    digital_root_invariant_check,
    seven_factor_to_bagua,
)


def test_digital_root():
    """测试数字根基本性质"""
    assert digital_root(37) == 1
    assert digital_root(369) == 9
    assert digital_root(15) == 6
    assert digital_root(45) == 9
    assert digital_root(0) == 0
    print("✅ 数字根测试通过")


def test_seven_factor_to_bagua():
    """测试七因子到八卦的映射"""
    factors = {"F1": 1.0, "F2": 0.9, "F3": 0.9, "F4": 0.95, "F5": 1.0, "F6": 0.88, "F7": 1.0}
    result = seven_factor_to_bagua(factors)
    assert "metrics" in result
    assert len(result["metrics"]) == 8
    assert result["upper_gua"] in "☰☷☳☴☵☲☶☱"
    assert result["lower_gua"] in "☰☷☳☴☵☲☶☱"
    print(f"✅ 七因子→八卦测试通过：{result['gua_combo']} ({result['upper_score']}, {result['lower_score']})")


def test_full_audit():
    """测试完整生态审计"""
    factors = {"F1": 1.0, "F2": 0.9, "F3": 0.9, "F4": 0.95, "F5": 1.0, "F6": 0.88, "F7": 1.0}
    result = audit_with_ecosystem(
        factors=factors,
        content="龍魂系统为人民服务",
        metadata={"uid": "UID9622", "persona": "P02"}
    )

    assert result["seven_factor"]["confidence"] > 0.85
    assert result["audit"]["color"] in {"🟢", "🟡", "🔴"}
    assert result["persona_route"]["upper_group"].endswith("组·创新突破")
    print(f"✅ 完整生态审计测试通过：置信度 {result['seven_factor']['confidence']}, 审计 {result['audit']['color']}")
    print(f"   卦象：{result['bagua']['gua_combo']}，数字根：{result['digital_root']['digital_root']}")


def test_hard_fail():
    """测试七因子硬失败"""
    factors = {"F1": 0.0, "F2": 0.9, "F3": 0.9, "F4": 0.95, "F5": 1.0, "F6": 0.88, "F7": 1.0}
    result = audit_with_ecosystem(factors=factors, content="测试")
    assert result["seven_factor"]["confidence"] == 0.0
    assert result["audit"]["color"] == "🔴"
    print("✅ 硬失败测试通过")


def test_luoshu_invariant():
    """测试河图洛书数字根红线"""
    # 8 维度指标之和为 15 时，dr=6，黄色待审
    result = digital_root_invariant_check(15)
    assert result["digital_root"] == 6
    assert result["color"] == "🟡"

    # 45 时，dr=9，红色熔断
    result = digital_root_invariant_check(45)
    assert result["digital_root"] == 9
    assert result["is_hard_fail"]
    print("✅ 河图洛书红线测试通过")


if __name__ == "__main__":
    print("\n🐉 龍魂生态对齐测试开始\n")
    test_digital_root()
    test_seven_factor_to_bagua()
    test_full_audit()
    test_hard_fail()
    test_luoshu_invariant()
    print("\n✅ 全部测试通过")
    print(f"\nDNA: #龍芯⚡️2026-07-05-ECOSYSTEM-ALIGNMENT-TEST-v1.0")
    print(f"CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
