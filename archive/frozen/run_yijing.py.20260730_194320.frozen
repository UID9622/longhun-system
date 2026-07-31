#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
易经推演 · 执行入口
用法：python3 run_yijing.py "你的问题"

DNA: #龍芯⚡️2026-06-29-YIJING-RUN-v1.0
"""
import sys
import time
from yijing_engine import complete_divination, print_cultural_dna


def main():
    question = sys.argv[1] if len(sys.argv) > 1 else "UID9622 龍魂系统当前局势与未来走势如何？"
    timestamp = time.time()

    print_cultural_dna()
    result = complete_divination(question, timestamp)

    print("=" * 64)
    print("🐉 易经64卦推演报告")
    print("=" * 64)
    print(f"问：{result['question']}")
    print(f"时间戳：{result['timestamp']}")
    print(f"节气权重：{result['solar_weight']}")
    print()

    original = result["hexagrams"]["original"]
    mutual = result["hexagrams"]["mutual"]
    changed = result["hexagrams"]["changed"]

    print(f"本卦：{original['name']}卦（ID={original['id']}）")
    print(f"  卦辞：{original['interpretation']['gua_ci']}")
    print(f"  彖：{original['interpretation']['interpretation']}")
    print()
    print(f"互卦：{mutual['name']}卦（ID={mutual['id']}）")
    print(f"  卦辞：{mutual['interpretation']['gua_ci']}")
    print()
    print(f"变卦：{changed['name']}卦（ID={changed['id']}）")
    print(f"  卦辞：{changed['interpretation']['gua_ci']}")
    print()

    wx = result["wuxing"]
    print(f"五行流转：{wx['original_element']} → {wx['changed_element']} | {wx['trend']}")
    print()

    judgment = result["judgment"]
    print(f"太极三才综合判断：{judgment['judgment']}")
    print(f"  天道：{judgment['details']['tian_dao']['score']} | {judgment['details']['tian_dao']['text'][:40]}...")
    print(f"  地道：{judgment['details']['di_dao']['score']} | {judgment['details']['di_dao']['text']}")
    print(f"  人道：{judgment['details']['ren_dao']['score']} | 变爻 {len(judgment['details']['ren_dao']['changes'])} 根")
    for ch in judgment["details"]["ren_dao"]["changes"]:
        flag = "吉" if ch["is_auspicious"] else "慎"
        print(f"    第{ch['position']}爻 [{flag}]：{ch['text']}")
    print()
    print(f"行动建议：{judgment['advice']}")
    print(f"综合评分：{judgment['score']}")
    print("=" * 64)
    print(f"DNA：#龍芯⚡️2026-06-29-YIJING-RUN-v1.0")
    print("=" * 64)


if __name__ == "__main__":
    main()
