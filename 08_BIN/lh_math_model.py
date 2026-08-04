#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️2026-07-25-MATH-MODEL-CLI-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════
# 龍魂 · 数学建模 CLI v1.0
# ═══════════════════════════════════════════
# DNA: #龍芯⚡️2026-07-25-MATH-MODEL-CLI-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# ═══════════════════════════════════════════
# 用法:
#   python3 bin/lh_math_model.py selftest            # 全部公式自检
#   python3 bin/lh_math_model.py dr 20260603         # 数字根+三色闸
#   python3 bin/lh_math_model.py si 0.9 0.8 0.7      # 三才主权指数
#   python3 bin/lh_math_model.py soul                # SOUL七维评分示例
#   python3 bin/lh_math_model.py chain               # 治理决策链演示
#   python3 bin/lh_math_model.py eval --id xxx --tian 0.9 --di 0.8 --ren 0.7  # 评估输入
# ═══════════════════════════════════════════
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from engines.lh_math_formula_core import (
    AuditColor,
    SOUL_WEIGHTS,
    compress_ratio,
    cosine,
    digital_root,
    dr_gate,
    element_of,
    entropy,
    hash_chain,
    magic_ok,
    normalize,
    selftest,
    soul_score,
    sovereignty_index,
)
from engines.lh_governance_decision_chain import (
    GovernanceDecisionChain,
    GovernanceInput,
    RiskFactor,
)


def cmd_selftest():
    report = selftest()
    print("=" * 64)
    print("🧮 龍魂数学公式算法核心 v2.0 · 自检报告")
    print("=" * 64)
    for line in report["details"]:
        print(line)
    print("=" * 64)
    print(f"{report['status']} 全部 {report['passed']} 组公式通过自检")
    print("=" * 64)


def cmd_dr(n: int):
    dr = digital_root(n)
    gate = dr_gate(n)
    elem = element_of(n)
    print(f"数字: {n}")
    print(f"数字根: {dr}")
    print(f"五行: {elem}")
    print(f"三色闸: {gate.value}")


def cmd_si(tian: float, di: float, ren: float):
    result = sovereignty_index(tian, di, ren)
    print(f"三才主权指数: {result['SI']}")
    print(f"有效分: {result['score']}")
    print(f"三色: {result['color'].value}")
    if result["veto"]:
        print(f"熔断原因: {result['reason']}")


def cmd_soul():
    # 示例评分
    example = {
        "技术": 0.85,
        "语言": 0.90,
        "文化": 0.88,
        "数据": 0.82,
        "决策": 0.79,
        "知识": 0.80,
        "身份": 1.0,  # 身份永不衰减
    }
    score = soul_score(example)
    print("SOUL 七维评分示例:")
    for dim, val in example.items():
        weight = SOUL_WEIGHTS[dim]
        print(f"  {dim}: {val:.2f} × {weight:.2f} = {val * weight:.4f}")
    print(f"总分: {score:.4f}")


def cmd_chain():
    from engines.lh_governance_decision_chain import demo
    demo()


def cmd_eval(args):
    chain = GovernanceDecisionChain()
    inp = GovernanceInput(
        identifier=args.id,
        tian=args.tian,
        di=args.di,
        ren=args.ren,
        risk_factors=[
            RiskFactor(name=f"风险{i+1}", weight=1.0, risk=r)
            for i, r in enumerate(args.risk or [])
        ],
    )
    result = chain.evaluate(inp)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_entropy(probs: List[float]):
    h = entropy(probs)
    print(f"概率分布: {probs}")
    print(f"香农熵: {h:.4f} bit")


def cmd_cosine(a: List[float], b: List[float]):
    score = cosine(a, b)
    print(f"向量 A: {a}")
    print(f"向量 B: {b}")
    print(f"余弦相似度: {score:.4f}")


def main():
    p = argparse.ArgumentParser(
        description="龍魂数学建模 CLI v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s selftest
  %(prog)s dr 20260603
  %(prog)s si 0.9 0.8 0.7
  %(prog)s soul
  %(prog)s chain
  %(prog)s eval --id api-gateway --tian 0.9 --di 0.8 --ren 0.7 --risk 0.1 --risk 0.2
        """,
    )
    sp = p.add_subparsers(dest="cmd", help="子命令")

    # selftest
    sp.add_parser("selftest", help="全部公式自检")

    # dr
    dr_p = sp.add_parser("dr", help="数字根+三色闸")
    dr_p.add_argument("n", type=int, help="整数")

    # si
    si_p = sp.add_parser("si", help="三才主权指数")
    si_p.add_argument("tian", type=float, help="天维评分 0~1")
    si_p.add_argument("di", type=float, help="地维评分 0~1")
    si_p.add_argument("ren", type=float, help="人维评分 0~1")

    # soul
    sp.add_parser("soul", help="SOUL七维评分示例")

    # chain
    sp.add_parser("chain", help="治理决策链演示")

    # eval
    eval_p = sp.add_parser("eval", help="评估一个输入的治理链")
    eval_p.add_argument("--id", required=True, help="输入标识")
    eval_p.add_argument("--tian", type=float, required=True, help="天维评分")
    eval_p.add_argument("--di", type=float, required=True, help="地维评分")
    eval_p.add_argument("--ren", type=float, required=True, help="人维评分")
    eval_p.add_argument("--risk", type=float, action="append", help="风险值（可多次）")

    # entropy
    ent_p = sp.add_parser("entropy", help="计算香农熵")
    ent_p.add_argument("probs", type=float, nargs="+", help="概率分布（和不必为1，会自动归一）")

    # cosine
    cos_p = sp.add_parser("cosine", help="计算余弦相似度")
    cos_p.add_argument("a", type=float, nargs="+", help="向量A")
    cos_p.add_argument("b", type=float, nargs="+", help="向量B")

    args = p.parse_args()

    if args.cmd == "selftest":
        cmd_selftest()
    elif args.cmd == "dr":
        cmd_dr(args.n)
    elif args.cmd == "si":
        cmd_si(args.tian, args.di, args.ren)
    elif args.cmd == "soul":
        cmd_soul()
    elif args.cmd == "chain":
        cmd_chain()
    elif args.cmd == "eval":
        cmd_eval(args)
    elif args.cmd == "entropy":
        probs = normalize(args.probs)
        cmd_entropy(probs)
    elif args.cmd == "cosine":
        if len(args.a) != len(args.b):
            print("错误：两个向量长度必须相同")
            sys.exit(1)
        cmd_cosine(args.a, args.b)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
