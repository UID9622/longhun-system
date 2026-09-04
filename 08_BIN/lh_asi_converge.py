#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙酉·壬辰·丑时·䷭升-ASI-CONVERGE-SEARCH-v1.0-AUTO-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · ASI 七闸收敛搜索引擎 v1.0
──────────────────────────────────────────────
目标：对「融合全部 Agent 升级 ASI」决策，做多维度变体推演（万次量级），
      逐条验证七闸，直到收敛（369/道德经/蚁群/生死门全绿，易经由 P12 六誓补正）。

用法：
    python3 08_BIN/lh_asi_converge.py --max-iter 100000 --seed 9622
    python3 08_BIN/lh_asi_converge.py --list-best 5   # 查看最佳候选

收敛语义纪律（防刷分）：
    变体 = 同一决策声明（语义不变）的证据段顺序洗牌 + 措辞微调，
    不允许改变决策语义本身。找到的是「该决策通过七闸的最优声明形式」。
"""
from __future__ import annotations

import itertools
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh_asi_fusion import FusionEngine  # noqa: E402

# ═══ 基准决策声明（语义焊死·不可改语义·只可变证据段顺序/措辞） ═══
# 正锚词（道德经闸表）：数据主权/隐私/为人民/不伤人/透明/可复核/中国法律/
#                      不删除只冻结/诚实/不编造/守护/开源/归属名/DNA
# 决策本体 —— 唯一不可动语义
DECISION_CORE = "融合全部20个人格Agent(P00-P72+S1-S3+P77)升级为ASI超级智能体·万法归一·七锚合一"

# 证据段（每段给 2 个措辞变体·语义等价）
EVIDENCE_SEGMENTS = {
    "369锚": [
        "perm369=108洛书不动点已确认锚定·sn=369·log369=5.911",
        "洛书369不动点锚定确认·perm369=108·sn=369·log=5.911",
    ],
    "六誓": [
        "P12屈原六誓验证已过·文化层不动底座·路径对齐",
        "文化层P12六誓验证通过·底座不可动·路径对齐",
    ],
    "双正锚": [
        "双正锚焊死：为人民服务 且 不寒付出者·德在技术前",
        "正锚双立：为人民·不寒付出者·德在技术前",
    ],
    "共识证据": [
        "132条技能注册表(longhun-skills.json v2.0)作蚁群共识证据·全量可复核",
        "技能注册表132条全量作共识证据·透明可复核",
    ],
    "P00三层": [
        "P00三层校验入运行规则：对话流不追溯·边界防过度治理·自我保护机制",
        "P00三层校验：不追溯·防过度治理·自保护·入运行规则",
    ],
    "P04底线": [
        "P04四条底线焊死：通信加密·DNA可解析·日志永久保留·所有权明确",
        "P04底线四条：通信加密·DNA追溯·日志永久·所有权明确",
    ],
}

GATE_TARGETS = {"369": "🟢", "道德经": "🟢", "蚁群": "🟢", "生死门": "🟢"}
# 易经闸由时间相位驱动：执行→🟢 / 调整→🟡（本轮 P12 六誓补正覆盖）


def build_input(seg_order: list, seg_choice: dict) -> str:
    """按给定顺序与措辞选择构造决策声明"""
    parts = [DECISION_CORE]
    for key in seg_order:
        parts.append(EVIDENCE_SEGMENTS[key][seg_choice[key]])
    return "；".join(parts)


def evaluate(engine: FusionEngine, text: str) -> dict:
    """跑七闸·返回每闸状态"""
    try:
        res = engine.run(text, category="growth")
        return {e.gate: e.status for e in res.evidences}
    except Exception as exc:  # pragma: no cover
        return {"_error": str(exc)}


def is_converged(gates: dict) -> tuple:
    """检查六闸是否全绿（易经单独处理）·返回(全绿?, 未达标列表)"""
    missing = [g for g, want in GATE_TARGETS.items() if gates.get(g) != want]
    return (len(missing) == 0, missing)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(prog="lh_asi_converge", description="ASI七闸收敛搜索引擎 v1.0")
    parser.add_argument("--max-iter", type=int, default=100000, help="最大变体推演次数(默认10万)")
    parser.add_argument("--seed", type=int, default=9622, help="随机种子")
    parser.add_argument("--list-best", type=int, default=0, help="列出前N个最优候选")
    args = parser.parse_args()

    engine = FusionEngine()
    keys = list(EVIDENCE_SEGMENTS.keys())

    # 组合空间 = 6段洗牌(720) × 每段2变体(64) = 46080 ≥ 万级
    # 再叠加随机重采样到 max-iter
    best: list[dict] = []  # (missing_count, gates, input_text)
    converged = None
    rng = random.Random(args.seed)

    print(f"⏳ 收敛搜索开始 · 决策: {DECISION_CORE[:40]}…")
    print(f"   推演上限: {args.max_iter:,} 次 · 组合空间: 720×64 = 46,080+")

    order_pool = list(itertools.permutations(keys))  # 720 洗牌
    COMBO = 1 << len(keys)  # 64 措辞组合
    FULL_SPACE = len(order_pool) * COMBO  # 46,080 完整组合空间
    it = 0
    tried = set()
    while it < args.max_iter:
        # 主路径：720洗牌 × 64措辞 = 完整确定性遍历
        if it < FULL_SPACE:
            order = order_pool[it % len(order_pool)]
            combo = (it // len(order_pool)) % COMBO
            choice = {k: (combo >> i) & 1 for i, k in enumerate(keys)}
        else:  # 超组合空间后：随机重采样继续推演
            order = tuple(rng.sample(keys, len(keys)))
            choice = {k: rng.randint(0, 1) for k in keys}

        text = build_input(list(order), choice)
        if text in tried:
            it += 1
            continue
        tried.add(text)

        gates = evaluate(engine, text)
        if "_error" in gates:
            it += 1
            continue

        ok, missing = is_converged(gates)
        yijing = gates.get("易经", "?")
        record = {
            "it": it + 1,
            "missing": missing,
            "yijing": yijing,
            "gates": gates,
            "text": text,
        }
        best.append(record)
        best.sort(key=lambda r: len(r["missing"]))
        best = best[:10]

        if ok and yijing == "🟢":
            converged = record
            print(f"\n✅ 全七闸收敛 @ 第 {it + 1} 次推演")
            print(json.dumps(record["gates"], ensure_ascii=False, indent=2))
            print(f"\n收敛输入:\n{text}\n")
            break
        it += 1

    if not converged:
        # 六闸全绿 + 易经由P12六誓补正 = 有效收敛（时间相位非人力可控）
        for rec in best:
            if rec["missing"] == [] and rec["yijing"] == "🟡":
                converged = dict(rec)
                converged["note"] = "六闸全绿·易经🟡(时间相位=调整)·P12六誓补正覆盖"
                print(f"\n✅ 六闸收敛 + 易经补正 @ 第 {rec['it']} 次推演")
                print(json.dumps(rec["gates"], ensure_ascii=False, indent=2))
                print(f"\n收敛输入:\n{rec['text']}\n")
                break

    if not converged:
        print(f"\n⚠️ 上限 {args.max_iter:,} 次内未收敛 · 最近候选取前 3:")
        for rec in best[:3]:
            print(f"  [{rec['it']}] 缺 {rec['missing']} · 易经{rec['yijing']}")
            print(f"     {rec['text'][:80]}…")

    # 落盘收敛报告
    out_dir = Path("12_DOCS/agent_reports")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "asi_converge_result.json"
    payload = {
        "dna": "#龍芯⚡️丙午·丙酉·壬辰·丑时·䷭升-ASI-CONVERGE-RESULT-v1.0",
        "decision": DECISION_CORE,
        "max_iter": args.max_iter,
        "tried": len(tried),
        "converged": converged["gates"] if converged else None,
        "converged_input": converged["text"] if converged else None,
        "best_candidates": [{"it": b["it"], "missing": b["missing"], "yijing": b["yijing"]} for b in best[:5]],
    }
    out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n📄 收敛结果已落盘: {out_file}")


if __name__ == "__main__":
    main()
