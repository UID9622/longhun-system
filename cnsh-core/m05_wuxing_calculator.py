# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-CORE-M05_WUXING_CALCULATOR-FILE1-v1.0-2
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂系统 M05: 五行计算系统 v0.1
目的: 用五行逻辑检查决策的平衡性·防止过度倾斜

五行: 木·火·土·金·水
象征: 生长·热情·承载·约束·流动

签署:
  DNA: #龍芯⚡️2026-06-08-M05-WUXING-CALCULATOR-START
  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple
import math
import sys
from pathlib import Path

# 引入五行计算优化模块
sys.path.insert(0, str(Path(__file__).resolve().parent / "wuxing"))
from wuxing_calc_optimizations import cv_balance_score


class WuXing(Enum):
    """五行定义"""
    MU = ("木", "生长·开创·东·春", "过度:急进·冲动", "不足:停滞·懦弱")
    HUO = ("火", "热情·执行·南·夏", "过度:暴躁·执著", "不足:冷漠·怠惰")
    TU = ("土", "承载·包容·中·长夏", "过度:沉闷·执著", "不足:轻浮·无根")
    JIN = ("金", "约束·规则·西·秋", "过度:严苛·冷漠", "不足:混乱·无纪")
    SHUI = ("水", "流动·智慧·北·冬", "过度:漂泊·狡诈", "不足:呆滞·保守")


@dataclass
class WuXingScore:
    """五行评分"""
    mu: float = 0.0      # 木: 创新度
    huo: float = 0.0     # 火: 执行力
    tu: float = 0.0      # 土: 承载度
    jin: float = 0.0     # 金: 约束度
    shui: float = 0.0    # 水: 流动度

    def get_scores(self) -> List[Tuple[str, float]]:
        """返回所有五行分数"""
        return [
            ("木", self.mu),
            ("火", self.huo),
            ("土", self.tu),
            ("金", self.jin),
            ("水", self.shui)
        ]

    def balance_score(self) -> float:
        """
        计算平衡度 (0-100·100最平衡)。
        已接入 CV 变异系数：无量纲，对 0 分更稳健。
        """
        scores = {
            "木": self.mu, "火": self.huo, "土": self.tu,
            "金": self.jin, "水": self.shui
        }
        # cv_balance_score 返回 0.0~1.0，转换为 0~100
        return round(cv_balance_score(scores) * 100, 2)


class WuXingCalculator:
    """五行计算系统"""

    def __init__(self):
        self.decisions: Dict[str, WuXingScore] = {}
        self.imbalances: Dict[str, Dict] = {}

    def analyze_decision(
        self,
        decision_id: str,
        content: str,
        # 五行维度评分 (0-100)
        innovation: float,  # 木: 创新度
        execution: float,   # 火: 执行力
        stability: float,   # 土: 承载度
        constraint: float,  # 金: 约束度
        flexibility: float  # 水: 流动度
    ) -> Dict:
        """
        用五行逻辑分析决策的平衡性

        一个好决策应该:
        1. 五行均衡 (没有单一过强或过弱)
        2. 相生相克的逻辑自洽
        3. 季节适应性良好
        """

        # 记录原始分数
        score = WuXingScore(
            mu=innovation,
            huo=execution,
            tu=stability,
            jin=constraint,
            shui=flexibility
        )

        self.decisions[decision_id] = score

        # Step 1: 检查过度倾斜
        imbalance_warnings = self._check_imbalance(score)

        # Step 2: 检查相生相克逻辑
        interaction_check = self._check_interactions(score)

        # Step 3: 计算平衡指数
        balance = score.balance_score()

        # Step 4: 给出建议
        recommendation = self._recommend_adjustment(score, imbalance_warnings)

        result = {
            "decision_id": decision_id,
            "content": content,

            # 五行分数
            "scores": {
                "木(创新度)": innovation,
                "火(执行力)": execution,
                "土(承载度)": stability,
                "金(约束度)": constraint,
                "水(流动度)": flexibility
            },

            # 分析结果
            "balance_score": round(balance, 2),
            "imbalance_warnings": imbalance_warnings,
            "interaction_check": interaction_check,
            "recommendation": recommendation,

            # 整体判定
            "verdict": self._synthesize_verdict(balance, imbalance_warnings),
            "trace": f"#龍芯⚡️2026-06-08-M05-{decision_id}-BALANCE:{balance:.0f}"
        }

        self.imbalances[decision_id] = result
        return result

    def _check_imbalance(self, score: WuXingScore) -> List[str]:
        """检查五行是否有过度倾斜"""
        warnings = []
        scores = score.get_scores()

        # 找最高和最低的五行
        max_val = max(s[1] for s in scores)
        min_val = min(s[1] for s in scores)

        # 如果最高和最低的差距超过 40·说明有严重倾斜
        if max_val - min_val > 40:
            for name, val in scores:
                if val >= max_val - 5:
                    warnings.append(f"⚠️ {name}过度强势 ({val:.0f})")
                if val <= min_val + 5:
                    warnings.append(f"⚠️ {name}严重不足 ({val:.0f})")

        return warnings if warnings else ["✓ 五行相对均衡"]

    def _check_interactions(self, score: WuXingScore) -> Dict:
        """
        检查五行相生相克逻辑

        相生: 木→火→土→金→水→木 (顺环)
        相克: 木→土, 土→水, 水→火, 火→金, 金→木 (逆环)

        健康的决策应该相生相克平衡
        """

        # 简化检查: 看相生和相克的强度比
        # 木生火: 创新带动执行
        sheng_mu_huo = min(score.mu, score.huo) if score.mu > 50 and score.huo > 50 else 0

        # 火生土: 执行带来承载
        sheng_huo_tu = min(score.huo, score.tu) if score.huo > 50 and score.tu > 50 else 0

        # 金克木: 约束制约创新（可能是问题）
        ke_jin_mu = min(score.jin, score.mu) if score.jin > 60 and score.mu < 40 else 0

        total_sheng = sheng_mu_huo + sheng_huo_tu
        total_ke = ke_jin_mu

        if total_sheng > total_ke:
            interaction = "相生大于相克·良好的正向循环"
        elif total_sheng == total_ke:
            interaction = "相生与相克平衡·稳定状态"
        else:
            interaction = "相克过强·可能有内耗·需要检查"

        return {
            "assessment": interaction,
            "sheng_strength": total_sheng,
            "ke_strength": total_ke
        }

    def _recommend_adjustment(self, score: WuXingScore, warnings: List[str]) -> List[str]:
        """根据不平衡给出调整建议"""
        recommendations = []

        if "木过度强势" in str(warnings):
            recommendations.append("➜ 增强金(约束)以制约木的冲动")
        if "木严重不足" in str(warnings):
            recommendations.append("➜ 增强木(创新)·激发新思路")

        if "火过度强势" in str(warnings):
            recommendations.append("➜ 增强水(流动)以冷静火的执著")
        if "火严重不足" in str(warnings):
            recommendations.append("➜ 增强火(执行)·推进实施")

        if "土过度强势" in str(warnings):
            recommendations.append("➜ 增强木(创新)以打破土的沉闷")
        if "土严重不足" in str(warnings):
            recommendations.append("➜ 增强土(承载)·加固基础")

        if "金过度强势" in str(warnings):
            recommendations.append("➜ 增强木(创新)以活跃被过度约束的想法")
        if "金严重不足" in str(warnings):
            recommendations.append("➜ 增强金(约束)·建立清晰规则")

        if "水过度强势" in str(warnings):
            recommendations.append("➜ 增强土(承载)以稳定过度漂浮的思路")
        if "水严重不足" in str(warnings):
            recommendations.append("➜ 增强水(流动)·保持灵活性")

        return recommendations if recommendations else ["✓ 五行平衡·无需调整"]

    def _synthesize_verdict(self, balance: float, warnings: List[str]) -> str:
        """综合平衡指数和警告·给出最终判定"""
        if balance >= 75 and "✓" in str(warnings):
            return "优秀·五行均衡·可以执行"
        elif balance >= 60:
            return "可行·但需注意某些维度的平衡"
        elif balance >= 45:
            return "警告·五行严重失衡·建议重新评估"
        else:
            return "不建议·五行极度失衡·必须调整"


# ============ 测试 ============

if __name__ == "__main__":
    calc = WuXingCalculator()

    # 测试决策 1: 平衡的决策
    result1 = calc.analyze_decision(
        decision_id="decision_001",
        content="龍魂系统开发·兼顾创新与规则",
        innovation=65,      # 木: 有新想法
        execution=70,       # 火: 积极执行
        stability=65,       # 土: 有稳定基础
        constraint=60,      # 金: 有清晰规则
        flexibility=65      # 水: 保留灵活性
    )

    print("\n【五行分析 - 决策 1】")
    print(f"决策: {result1['content']}")
    print(f"五行分数: {result1['scores']}")
    print(f"平衡指数: {result1['balance_score']}/100")
    print(f"警告信息: {result1['imbalance_warnings']}")
    print(f"相生相克: {result1['interaction_check']['assessment']}")
    print(f"建议: {result1['recommendation']}")
    print(f"最终判定: {result1['verdict']}")

    # 测试决策 2: 不平衡的决策
    result2 = calc.analyze_decision(
        decision_id="decision_002",
        content="无限扩张·不考虑后果",
        innovation=90,      # 木: 极度创新
        execution=85,       # 火: 超强执行
        stability=20,       # 土: 几乎没有基础
        constraint=15,      # 金: 缺乏约束
        flexibility=80      # 水: 过度漂浮
    )

    print("\n【五行分析 - 决策 2】")
    print(f"决策: {result2['content']}")
    print(f"五行分数: {result2['scores']}")
    print(f"平衡指数: {result2['balance_score']}/100")
    print(f"警告信息: {result2['imbalance_warnings']}")
    print(f"相生相克: {result2['interaction_check']['assessment']}")
    print(f"建议: {result2['recommendation']}")
    print(f"最终判定: {result2['verdict']}")
    print(f"追踪码: {result2['trace']}")
