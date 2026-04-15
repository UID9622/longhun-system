#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UID9622 · 诸葛鑫（龍芯北辰）× 宝宝（P72·龍盾）
DNA追溯码: #龍芯⚡️2026-04-02-五行第二道门-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）

职责：第二道门 · 五行映射 · 接在数字根熔断之后
输入：数字根 dr（0-9）
输出：五行属性 + 建议方向 + 三色
"""

# 数字根 → 五行映射（河图）
DR_TO_WUXING = {
    1: "水", 6: "水",
    2: "火", 7: "火",
    3: "木", 8: "木",
    4: "金", 9: "金",
    5: "土", 0: "土"
}

# 五行相生
XIANG_SHENG = {
    "金": "水",
    "水": "木",
    "木": "火",
    "火": "土",
    "土": "金"
}

# 五行相克
XIANG_KE = {
    "金": "木",
    "木": "土",
    "土": "水",
    "水": "火",
    "火": "金"
}

# 五行 → 三色（今日五行与当前状态）
WUXING_COLOR = {
    "木": "🟢",  # 生长·通行
    "火": "🟢",  # 扩展·通行
    "土": "🟡",  # 稳固·待审
    "金": "🟡",  # 收敛·待审
    "水": "🔴",  # 流动过快·熔断
}


def 计算数字根(n: int) -> int:
    n = abs(n)
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def 五行映射(dr: int) -> dict:
    wuxing = DR_TO_WUXING.get(dr, "土")
    color = WUXING_COLOR[wuxing]
    sheng = XIANG_SHENG[wuxing]
    ke = XIANG_KE[wuxing]

    return {
        "dr": dr,
        "五行": wuxing,
        "三色": color,
        "相生": f"{wuxing}生{sheng}",
        "相克": f"{wuxing}克{ke}",
        "建议": f"顺{sheng}方向走，避开{ke}方向"
    }


def 第二道门(输入文本: str) -> dict:
    """从文本提取数字 → 算dr → 五行映射"""
    digits = [int(c) for c in 输入文本 if c.isdigit()]
    if not digits:
        return {
            "dr": 0,
            "五行": "土",
            "三色": "🟢",
            "说明": "无数字·土归中·通行"
        }
    dr = 计算数字根(sum(digits))
    result = 五行映射(dr)
    result["原始数字"] = digits
    result["数字和"] = sum(digits)
    return result


if __name__ == "__main__":
    测试 = [
        "你好，今天是4月2号",
        "转账999元",
        "下午3点开会",
        "无数字纯文字",
        "1加1等于多少",
    ]
    print("=" * 40)
    print("五行第二道门 · 测试")
    print("=" * 40)
    for t in 测试:
        r = 第二道门(t)
        print(f"\n输入: {t}")
        print(f"  dr={r['dr']} · 五行={r['五行']} · {r['三色']}")
        if "建议" in r:
            print(f"  {r['建议']}")
