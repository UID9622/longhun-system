# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·数字根引擎测试 v1.0
DNA: #龍芯⚡️2026-07-30-数字根引擎-测试-v1.0
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bin.lh_digital_root import 数字根引擎, 计算数字根

pass_count = 0
fail_count = 0


def assert_eq(desc: str, actual, expected):
    global pass_count, fail_count
    if actual == expected:
        print(f"  ✅ {desc}: {actual}")
        pass_count += 1
    else:
        print(f"  ❌ {desc}: 期望 {expected}, 实际 {actual}")
        fail_count += 1


def assert_true(desc: str, value):
    global pass_count, fail_count
    if value:
        print(f"  ✅ {desc}")
        pass_count += 1
    else:
        print(f"  ❌ {desc}: 期望 True, 实际 {value}")
        fail_count += 1


def test_基本计算():
    print("\n── 基本计算 ──")
    assert_eq("纯数字9622", 数字根引擎.计算("9622"), 1)       # 9+6+2+2=19→10→1
    assert_eq("纯数字2026", 数字根引擎.计算("2026"), 1)       # 2+0+2+6=10→1
    assert_eq("含文本'订单123'", 数字根引擎.计算("订单123"), 6)  # 1+2+3=6
    assert_eq("含文本'5622号'", 数字根引擎.计算("5622号"), 6)  # 5+6+2+2=15→6
    assert_eq("无数字文本'abc'", 数字根引擎.计算("abc"), 0)
    assert_eq("空字符串", 数字根引擎.计算(""), 0)
    assert_eq("数字0", 数字根引擎.计算("0"), 0)
    assert_eq("整数输入123", 数字根引擎.计算(123), 6)          # 1+2+3=6
    assert_eq("369熔断数字", 数字根引擎.计算(369), 9)          # 3+6+9=18→9


def test_大数字():
    print("\n── 大数字 ──")
    assert_eq("9999999999(10个9)", 数字根引擎.计算("9999999999"), 9)  # 90→9
    assert_eq("1234567890", 数字根引擎.计算("1234567890"), 9)  # 45→9
    assert_eq("20260730(今天日期)", 数字根引擎.计算("20260730"), 2)  # 2+0+2+6+0+7+3+0=20→2


def test_带五行():
    print("\n── 带五行信息 ──")
    r1 = 数字根引擎.带五行("9622")
    assert_eq("9622→数字根1", r1["数字根"], 1)
    assert_eq("9622→五行水", r1["五行"], "水")
    assert_eq("9622→🟢", r1["三色审计"], "🟢")

    r3 = 数字根引擎.带五行("369")
    assert_eq("369→数字根9🔴", r3["数字根"], 9)
    assert_eq("369→熔断🔴", r3["三色审计"], "🔴")

    r6 = 数字根引擎.带五行("123")
    assert_eq("123→数字根6🟡", r6["数字根"], 6)
    assert_eq("123→待审🟡", r6["三色审计"], "🟡")


def test_熔断数字根():
    print("\n── 熔断数字根(3,9) 🔴 ──")
    assert_eq("3熔断", 数字根引擎.三色审计表.get(3), "🔴")
    assert_eq("9熔断", 数字根引擎.三色审计表.get(9), "🔴")
    assert_eq("39熔断(3+9=12→3)", 数字根引擎.三色审计表.get(数字根引擎.计算("39")), "🔴")


def test_映射表完整性():
    print("\n── 映射表完整性 ──")
    for i in range(10):
        五行 = 数字根引擎.五行映射表.get(i)
        assert_true(f"数字根{i}有五行映射", 五行 is not None)
    assert_eq("映射表共10项", len(数字根引擎.五行映射表), 10)


def test_批量计算():
    print("\n── 批量计算 ──")
    结果 = 数字根引擎.批量计算(["123", "456", "789", "2026", ""])
    assert_eq("批量5项", 结果, [6, 6, 6, 1, 0])


def test_验证功能():
    print("\n── 验证功能 ──")
    assert_true("9622→1正确", 数字根引擎.验证("9622", 1))
    assert_true("123→6不正确应为5", not 数字根引擎.验证("123", 5))
    assert_eq("实际上123→6", 数字根引擎.计算("123"), 6)


def test_数字根五行全映射():
    print("\n── 完整数字根→五行映射 ──")
    期望映射 = {0:"土", 1:"水", 2:"火", 3:"木", 4:"金", 5:"土", 6:"水", 7:"火", 8:"木", 9:"金"}
    for dr, wx in 期望映射.items():
        assert_eq(f"dr{dr}→{wx}", 数字根引擎.五行映射表[dr], wx)


def test_与流场压缩核对接():
    print("\n── 流场压缩核对接(模拟 lh_wuxing_core 链路) ──")
    # 模拟五行计算器调用数字根引擎的完整链路
    test_inputs = ["20260730", "9622", "369", "测试无数字"]
    for inp in test_inputs:
        r = 数字根引擎.带五行(inp)
        assert_true(f"{inp}→dr={r['数字根']},wx={r['五行']},audit={r['三色审计']}",
                    r["数字根"] in range(10))


if __name__ == "__main__":
    print("=" * 60)
    print("🐉 数字根引擎 v1.0 测试")
    print("=" * 60)

    test_基本计算()
    test_大数字()
    test_带五行()
    test_熔断数字根()
    test_映射表完整性()
    test_批量计算()
    test_验证功能()
    test_数字根五行全映射()
    test_与流场压缩核对接()

    print("\n" + "=" * 60)
    total = pass_count + fail_count
    print(f"  {total} 项 · ✅ {pass_count} 通过 · ❌ {fail_count} 失败")
    print("=" * 60)
    sys.exit(0 if fail_count == 0 else 1)
