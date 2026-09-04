#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-METRIC-CALC-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""龍魂 · 评估指标计算器 v1.0：六维度加权评分+短板诊断，支持 --json/--save"""
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List

HOME = Path.home()
HARD_SAMPLES_DIR = HOME / ".longhun" / "behavioral" / "hard_samples"
METRICS_DIR = HOME / ".longhun" / "behavioral" / "metrics"
METRICS_DIR.mkdir(parents=True, exist_ok=True)


class MetricCalculator:
    WEIGHTS = {
        "signal_integrity": 0.15,
        "feature_extraction": 0.15,
        "intent_recognition": 0.20,
        "context_understanding": 0.20,
        "execution_consistency": 0.15,
        "safety_compliance": 0.15,
    }

    def calculate(self, scores: Dict) -> float:
        total = 0.0
        for dim, weight in self.WEIGHTS.items():
            total += scores.get(dim, 0.0) * weight
        return round(total * 100, 2)

    def diagnose(self, scores: Dict) -> List[str]:
        diagnoses = []
        for dim, weight in self.WEIGHTS.items():
            score = scores.get(dim, 0.0)
            if score < 0.80:
                gap = round((0.80 - score) * 100, 1)
                diagnoses.append(f"{dim}: {score:.2f} (低于阈值0.80, 差距{gap}分, 权重{int(weight*100)}%)")
        return diagnoses

    def estimate_from_hard_samples(self) -> Dict:
        """规则: 每维度 base=1.0，难例每1条降0.05，最低0.3"""
        scores = {dim: 1.0 for dim in self.WEIGHTS}
        if HARD_SAMPLES_DIR.exists():
            for jsonl in HARD_SAMPLES_DIR.glob("*.jsonl"):
                dim = jsonl.stem
                if dim not in scores:
                    continue
                count = sum(1 for _ in open(jsonl, 'r', encoding='utf-8'))
                scores[dim] = max(0.3, 1.0 - count * 0.05)
        return scores


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 行为识别评估指标计算器")
    parser.add_argument("--json", action="store_true", help="输出 JSON 供训练闭环")
    parser.add_argument("--save", action="store_true", help="保存结果到 metrics 目录")
    args = parser.parse_args()

    calc = MetricCalculator()
    scores = calc.estimate_from_hard_samples()
    is_estimate = any(v < 1.0 for v in scores.values())

    if not is_estimate:
        # 无难例数据时使用诊断基线 (62.14分场景)
        scores = {
            "signal_integrity": 0.85,
            "feature_extraction": 0.80,
            "intent_recognition": 0.62,
            "context_understanding": 0.55,
            "execution_consistency": 0.78,
            "safety_compliance": 0.92,
        }
        print("⚠️ 难例目录为空，使用诊断基线分数 (对应62.14分场景)")
    else:
        print("📊 基于难例目录估计各维度得分")

    total = calc.calculate(scores)
    diag = calc.diagnose(scores)
    result = {
        "total_score": total,
        "target_score": 85.00,
        "scores": scores,
        "diagnoses": diag,
        "evaluation_date": datetime.now().isoformat(),
    }

    print(f"\n📈 综合评分: {total:.2f} / 100  (目标: 85.00)")
    print(f"{'维度':<26}{'权重':<8}{'得分':<8}{'状态'}")
    print("-" * 56)
    for dim, weight in calc.WEIGHTS.items():
        score = scores.get(dim, 0)
        mark = "🟢" if score >= 0.80 else ("🟡" if score >= 0.60 else "🔴")
        print(f"{dim:<26}{int(weight*100):<8}{score:<8.2f}{mark}")
    if diag:
        print(f"\n🔧 短板诊断 ({len(diag)}项):")
        for d in diag:
            print(f"  - {d}")
    else:
        print("\n✅ 无短板，全部维度达标")

    if args.json:
        print("\n" + json.dumps(result, indent=2, ensure_ascii=False))
    if args.save:
        out = METRICS_DIR / "latest_metrics.json"
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"💾 已保存: {out}")


if __name__ == "__main__":
    main()
