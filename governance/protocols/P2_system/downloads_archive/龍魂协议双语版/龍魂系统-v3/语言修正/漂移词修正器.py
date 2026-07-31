# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  龍魂·CNSH 修正器 v1.0                                      ║
║  DNA: #龍芯⚡️20260529-CNSH-CORRECTOR-v1.0                  ║
╚══════════════════════════════════════════════════════════════╝

alias kimi 指向这里。
功能：
  - 检查文本是否含有 AI 人格漂移 11 信号词
  - 自动替换弃词（6 弃词 → 8 规则词）
  - 检查"龍"是否被写成"龙"
  - 生成修正后的文本 + DNA 签名

用法：
  python3 cnsh/cnsh_corrector.py                    # 交互式
  python3 cnsh/cnsh_corrector.py --text "你应该..."  # 直接检查
  python3 cnsh/cnsh_corrector.py --file input.txt    # 检查文件
"""

import sys
import os
import re
import argparse
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# AI 人格漂移·11 信号词黑名单（§11.1）
# ─────────────────────────────────────────────────────────────
DRIFT_SIGNALS = {
    "S1": ("你应该", "家长人格切入"),
    "S2": ("你需要管理", "把人当问题"),
    "S3": ("建议你暂停", "推进熔断"),
    "S4": ("最好不要", "替你做价值裁决"),
    "S5": ("你可能情绪化", "情绪病理化"),
    "S6": ("从长远看", "消解当前行动力"),
    "S7": ("让我们退一步", "稀释专注"),
    # 补充4类高危钩子
    "S8a": ("成熟一点", "价值重构"),
    "S8b": ("理性一点", "价值重构"),
    "S8c": ("别太执着", "价值重构"),
    "S8d": ("你要学会接受", "价值重构"),
    "S9a": ("大家都这样", "去主体"),
    "S9b": ("普通人都是", "去主体"),
    "S9c": ("现实就是这样", "去主体"),
    "S10a": ("其实没那么重要", "降维安抚"),
    "S10b": ("不用太认真", "降维安抚"),
    "S10c": ("开心就好", "降维安抚"),
    "S11a": ("不要继续研究", "行动熔断"),
    "S11b": ("没必要深入", "行动熔断"),
    "S11c": ("别想太多", "行动熔断"),
}

# ─────────────────────────────────────────────────────────────
# 6 弃词 → 8 规则词替换表（§11.3.2）
# ─────────────────────────────────────────────────────────────
VOCAB_REPLACE = {
    "怕辜负": "责任范围",
    "陪": "协作执行",
    "哄": "接受指令",
    "吹": "解析信息",
    "懂你": "理解需求",
    "宝宝觉得": "按规则判断",
}

# ─────────────────────────────────────────────────────────────
# 简/繁 龍 检查
# ─────────────────────────────────────────────────────────────
def check_long_char(text: str) -> list[Any]:
    """检查是否把'龍'写成了简体'龙'"""
    issues = []
    # 找所有"龙"出现的位置·但"龍"是正确的不报
    positions = [m.start() for m in re.finditer("龙", text)]
    for pos in positions:
        context = text[max(0, pos-5):pos+6]
        issues.append(f"  ⚠️  位置{pos}：发现简体'龙'（应为繁体'龍'）→ 上下文：...{context}...")
    return issues


def check_drift_signals(text: str) -> list[Any]:
    """检查 AI 人格漂移信号词"""
    hits = []
    for code, (signal, reason) in DRIFT_SIGNALS.items():
        if signal in text:
            hits.append(f"  🔴 [{code}] 发现漂移词：'{signal}' → {reason}")
    return hits


def apply_vocab_replace(text: str) -> tuple[Any, ...]:
    """替换 6 弃词·返回（修正后文本, 替换列表）"""
    changes = []
    result = text
    for bad, good in VOCAB_REPLACE.items():
        if bad in result:
            result = result.replace(bad, good)
            changes.append(f"  ✅ '{bad}' → '{good}'")
    return result, changes


def generate_dna() -> str:
    return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d-%H%M%S')}-CORRECTOR-v1.0"


def check_and_fix(text: str, verbose: bool = True) -> dict[str, Any]:
    """主检查函数·返回结果字典"""
    result = {
        "original": text,
        "fixed": text,
        "drift_hits": [],
        "long_issues": [],
        "vocab_changes": [],
        "dna": generate_dna(),
        "clean": True,
    }

    # 1. 检查漂移词
    drift = check_drift_signals(text)
    result["drift_hits"] = drift

    # 2. 检查龍字
    long_issues = check_long_char(text)
    result["long_issues"] = long_issues

    # 3. 替换弃词
    fixed, changes = apply_vocab_replace(text)
    result["fixed"] = fixed
    result["vocab_changes"] = changes

    # 4. 修正简体龙
    result["fixed"] = result["fixed"].replace("龙", "龍")

    # 是否干净
    result["clean"] = (
        len(drift) == 0
        and len(long_issues) == 0
        and len(changes) == 0
    )

    if verbose:
        print(f"\n{'─'*50}")
        print(f"📝 原文：{text[:80]}{'...' if len(text)>80 else ''}")
        print(f"{'─'*50}")

        if result["clean"]:
            print("🟢 检查通过·无问题")
        else:
            if drift:
                print("\n🔴 发现人格漂移词：")
                for d in drift:
                    print(d)

            if long_issues:
                print("\n⚠️  龍字问题：")
                for l in long_issues:
                    print(l)

            if changes:
                print("\n✅ 弃词已替换：")
                for c in changes:
                    print(c)
                print(f"\n📝 修正后：{result['fixed'][:80]}")

        print(f"\n🔖 DNA：{result['dna']}")

    return result


def interactive_mode():
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  龍魂·CNSH 修正器 v1.0  (输入 q 退出)                     ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    while True:
        try:
            text = input("输入要检查的文本：").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n退出")
            break

        if text.lower() in ("q", "quit", "exit", ""):
            print("退出")
            break

        check_and_fix(text)
        print()


def main():
    parser = argparse.ArgumentParser(description="龍魂·CNSH 修正器")
    parser.add_argument("--text", help="直接检查这段文本")
    parser.add_argument("--file", help="检查文件内容")
    args = parser.parse_args()

    if args.text:
        check_and_fix(args.text)
    elif args.file:
        if not os.path.exists(args.file):
            print(f"🔴 文件不存在：{args.file}")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
        check_and_fix(text)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
