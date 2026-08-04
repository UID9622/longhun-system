#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
价格审计 - 测试
DNA: #龍芯⚡️丙午·乙未·辛亥·巳时·☰乾-PRICE-AUDIT-TEST-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from detector import detect_price_anomaly, quick_check, check_with_groups


def test_quick_check():
    """基础：仅价格列表。"""
    result = quick_check([9.9, 10.0, 9.8, 12.0, 12.5])
    assert "error" not in result
    assert "composite_assessment" in result
    assert "iqr_analysis" in result
    print("✅ test_quick_check 通过")


def test_normal_prices():
    """无明显异常的价格。"""
    result = quick_check([100, 102, 101, 99, 100, 103, 98])
    score = result["composite_assessment"]["score"]
    # 正常价格应该低分
    assert score < 40, f"正常价格评分应<40, 实际{score}"
    print(f"✅ test_normal_prices 通过 (score={score})")


def test_suspicious_prices():
    """典型杀熟场景：新老用户价差。"""
    groups = {
        "新用户": [9.9, 10.0, 9.8, 10.0, 9.9],
        "老用户": [12.0, 12.5, 12.3, 12.8, 11.9]
    }
    all_prices = groups["新用户"] + groups["老用户"]
    result = detect_price_anomaly(all_prices, groups=groups)
    score = result["composite_assessment"]["score"]
    
    assert result["suspicious"] is True, "杀熟场景应标记为可疑"
    assert score >= 40, f"杀熟评分应>=40, 实际{score}"
    print(f"✅ test_suspicious_prices 通过 (score={score}, suspicious=True)")


def test_empty_prices():
    result = quick_check([])
    assert "error" in result
    print("✅ test_empty_prices 通过")


def test_single_price():
    """只有一个价格时不崩溃。"""
    result = quick_check([9.9])
    assert "error" not in result
    assert result["data_summary"]["total_records"] == 1
    print("✅ test_single_price 通过")


def test_group_detection():
    """分组检测逻辑。"""
    result = check_with_groups(
        [100, 100, 100, 200, 200, 200],
        {"组A": [100, 100, 100], "组B": [200, 200, 200]}
    )
    grp = result["group_analysis"]
    assert grp["suspicious"] is True
    assert grp["max_diff_pct"] > 90  # 差值100%
    print(f"✅ test_group_detection 通过 (diff={grp['max_diff_pct']}%)")


def test_timeseries():
    """时间序列异常检测。"""
    timeseries = [
        {"time": "t1", "price": 10},
        {"time": "t2", "price": 10},
        {"time": "t3", "price": 10},
        {"time": "t4", "price": 10},
        {"time": "t5", "price": 10},
        {"time": "t6", "price": 50},  # 突然暴涨
    ]
    all_prices = [d["price"] for d in timeseries]
    result = detect_price_anomaly(all_prices, timeseries=timeseries)
    ts = result["timeseries_analysis"]
    assert ts["anomalies_count"] > 0
    print(f"✅ test_timeseries 通过 (anomalies={ts['anomalies_count']})")


def test_iqr_extreme():
    """极端异常值检测。"""
    # 大部分在10-12，一个在100
    prices = [10, 10, 11, 10, 12, 11, 100]
    result = quick_check(prices)
    iqr = result["iqr_analysis"]
    assert iqr["outliers_count"] > 0
    # 100应该是极端异常
    outliers = iqr["outliers"]
    extreme = [o for o in outliers if o["price"] == 100]
    assert len(extreme) > 0
    assert extreme[0]["type"] == "极端异常"
    print(f"✅ test_iqr_extreme 通过 (outliers={iqr['outliers_count']})")


def test_composite_breakdown():
    """综合评分的分解应该合理。"""
    result = quick_check([9.9, 10.0, 12.0, 12.5])
    bd = result["composite_assessment"]["breakdown"]
    assert "iqr_score" in bd
    assert "group_diff_score" in bd
    assert "time_score" in bd
    assert "data_score" in bd
    # 数据充分度分应该非零
    assert bd["data_score"] > 0
    print(f"✅ test_composite_breakdown 通过")


if __name__ == "__main__":
    print("=" * 50)
    print("  价格审计检测引擎 · 测试套件")
    print("=" * 50)
    
    tests = [
        test_quick_check,
        test_normal_prices,
        test_suspicious_prices,
        test_empty_prices,
        test_single_price,
        test_group_detection,
        test_timeseries,
        test_iqr_extreme,
        test_composite_breakdown,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} 失败: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"  总计: {passed}通过 / {failed}失败 / {len(tests)}项")
    print(f"{'='*50}")
