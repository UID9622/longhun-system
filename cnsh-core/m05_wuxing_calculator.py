#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂系統 M05: 五行計算系統 v0.1
目的: 用五行邏輯檢查決策的平衡性·防止過度傾斜

五行: 木·火·土·金·水
象徵: 生長·熱情·承載·約束·流動

簽署:
  DNA: #龍芯⚡️2026-06-08-M05-WUXING-CALCULATOR-START
  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple
import math


class WuXing(Enum):
    """五行定義"""
    MU = ("木", "生長·開創·東·春", "過度:急進·衝動", "不足:停滯·懦弱")
    HUO = ("火", "熱情·執行·南·夏", "過度:暴躁·執著", "不足:冷漠·怠惰")
    TU = ("土", "承載·包容·中·長夏", "過度:沉悶·執著", "不足:輕浮·無根")
    JIN = ("金", "約束·規則·西·秋", "過度:嚴苛·冷漠", "不足:混亂·無紀")
    SHUI = ("水", "流動·智慧·北·冬", "過度:漂泊·狡詐", "不足:呆滯·保守")


@dataclass
class WuXingScore:
    """五行評分"""
    mu: float = 0.0      # 木: 創新度
    huo: float = 0.0     # 火: 執行力
    tu: float = 0.0      # 土: 承載度
    jin: float = 0.0     # 金: 約束度
    shui: float = 0.0    # 水: 流動度

    def get_scores(self) -> List[Tuple[str, float]]:
        """返回所有五行分數"""
        return [
            ("木", self.mu),
            ("火", self.huo),
            ("土", self.tu),
            ("金", self.jin),
            ("水", self.shui)
        ]

    def balance_score(self) -> float:
        """計算平衡度 (0-100·100最平衡)"""
        scores = [self.mu, self.huo, self.tu, self.jin, self.shui]
        mean = sum(scores) / len(scores)

        # 方差越小·平衡度越高
        variance = sum((s - mean) ** 2 for s in scores) / len(scores)
        std_dev = math.sqrt(variance)

        # 轉換為 0-100 的平衡指數
        # std_dev 越小·平衡指數越高
        balance = max(0, 100 - std_dev * 10)
        return min(100, balance)


class WuXingCalculator:
    """五行計算系統"""

    def __init__(self):
        self.decisions: Dict[str, WuXingScore] = {}
        self.imbalances: Dict[str, Dict] = {}

    def analyze_decision(
        self,
        decision_id: str,
        content: str,
        # 五行維度評分 (0-100)
        innovation: float,  # 木: 創新度
        execution: float,   # 火: 執行力
        stability: float,   # 土: 承載度
        constraint: float,  # 金: 約束度
        flexibility: float  # 水: 流動度
    ) -> Dict:
        """
        用五行邏輯分析決策的平衡性

        一個好決策應該:
        1. 五行均衡 (沒有單一過強或過弱)
        2. 相生相剋的邏輯自洽
        3. 季節適應性良好
        """

        # 記錄原始分數
        score = WuXingScore(
            mu=innovation,
            huo=execution,
            tu=stability,
            jin=constraint,
            shui=flexibility
        )

        self.decisions[decision_id] = score

        # Step 1: 檢查過度傾斜
        imbalance_warnings = self._check_imbalance(score)

        # Step 2: 檢查相生相剋邏輯
        interaction_check = self._check_interactions(score)

        # Step 3: 計算平衡指數
        balance = score.balance_score()

        # Step 4: 給出建議
        recommendation = self._recommend_adjustment(score, imbalance_warnings)

        result = {
            "decision_id": decision_id,
            "content": content,

            # 五行分數
            "scores": {
                "木(創新度)": innovation,
                "火(執行力)": execution,
                "土(承載度)": stability,
                "金(約束度)": constraint,
                "水(流動度)": flexibility
            },

            # 分析結果
            "balance_score": round(balance, 2),
            "imbalance_warnings": imbalance_warnings,
            "interaction_check": interaction_check,
            "recommendation": recommendation,

            # 整體判定
            "verdict": self._synthesize_verdict(balance, imbalance_warnings),
            "trace": f"#龍芯⚡️2026-06-08-M05-{decision_id}-BALANCE:{balance:.0f}"
        }

        self.imbalances[decision_id] = result
        return result

    def _check_imbalance(self, score: WuXingScore) -> List[str]:
        """檢查五行是否有過度傾斜"""
        warnings = []
        scores = score.get_scores()

        # 找最高和最低的五行
        max_val = max(s[1] for s in scores)
        min_val = min(s[1] for s in scores)

        # 如果最高和最低的差距超過 40·說明有嚴重傾斜
        if max_val - min_val > 40:
            for name, val in scores:
                if val >= max_val - 5:
                    warnings.append(f"⚠️ {name}過度強勢 ({val:.0f})")
                if val <= min_val + 5:
                    warnings.append(f"⚠️ {name}嚴重不足 ({val:.0f})")

        return warnings if warnings else ["✓ 五行相對均衡"]

    def _check_interactions(self, score: WuXingScore) -> Dict:
        """
        檢查五行相生相剋邏輯

        相生: 木→火→土→金→水→木 (順環)
        相剋: 木→土, 土→水, 水→火, 火→金, 金→木 (逆環)

        健康的決策應該相生相剋平衡
        """

        # 簡化檢查: 看相生和相剋的强度比
        # 木生火: 創新帶動執行
        sheng_mu_huo = min(score.mu, score.huo) if score.mu > 50 and score.huo > 50 else 0

        # 火生土: 執行帶來承載
        sheng_huo_tu = min(score.huo, score.tu) if score.huo > 50 and score.tu > 50 else 0

        # 金克木: 約束制約創新（可能是問題）
        ke_jin_mu = min(score.jin, score.mu) if score.jin > 60 and score.mu < 40 else 0

        total_sheng = sheng_mu_huo + sheng_huo_tu
        total_ke = ke_jin_mu

        if total_sheng > total_ke:
            interaction = "相生大於相剋·良好的正向循環"
        elif total_sheng == total_ke:
            interaction = "相生與相剋平衡·穩定狀態"
        else:
            interaction = "相剋過強·可能有內耗·需要檢查"

        return {
            "assessment": interaction,
            "sheng_strength": total_sheng,
            "ke_strength": total_ke
        }

    def _recommend_adjustment(self, score: WuXingScore, warnings: List[str]) -> List[str]:
        """根據不平衡給出調整建議"""
        recommendations = []

        if "木過度強勢" in str(warnings):
            recommendations.append("➜ 增強金(約束)以制約木的衝動")
        if "木嚴重不足" in str(warnings):
            recommendations.append("➜ 增強木(創新)·激發新思路")

        if "火過度強勢" in str(warnings):
            recommendations.append("➜ 增強水(流動)以冷靜火的執著")
        if "火嚴重不足" in str(warnings):
            recommendations.append("➜ 增強火(執行)·推進實施")

        if "土過度強勢" in str(warnings):
            recommendations.append("➜ 增強木(創新)以打破土的沉悶")
        if "土嚴重不足" in str(warnings):
            recommendations.append("➜ 增強土(承載)·加固基礎")

        if "金過度強勢" in str(warnings):
            recommendations.append("➜ 增強木(創新)以活躍被過度約束的想法")
        if "金嚴重不足" in str(warnings):
            recommendations.append("➜ 增強金(約束)·建立清晰規則")

        if "水過度強勢" in str(warnings):
            recommendations.append("➜ 增強土(承載)以穩定過度漂浮的思路")
        if "水嚴重不足" in str(warnings):
            recommendations.append("➜ 增強水(流動)·保持靈活性")

        return recommendations if recommendations else ["✓ 五行平衡·無需調整"]

    def _synthesize_verdict(self, balance: float, warnings: List[str]) -> str:
        """綜合平衡指數和警告·給出最終判定"""
        if balance >= 75 and "✓" in str(warnings):
            return "優秀·五行均衡·可以執行"
        elif balance >= 60:
            return "可行·但需注意某些維度的平衡"
        elif balance >= 45:
            return "警告·五行嚴重失衡·建議重新評估"
        else:
            return "不建議·五行極度失衡·必須調整"


# ============ 測試 ============

if __name__ == "__main__":
    calc = WuXingCalculator()

    # 測試決策 1: 平衡的決策
    result1 = calc.analyze_decision(
        decision_id="decision_001",
        content="龍魂系統開發·兼顧創新與規則",
        innovation=65,      # 木: 有新想法
        execution=70,       # 火: 積極執行
        stability=65,       # 土: 有穩定基礎
        constraint=60,      # 金: 有清晰規則
        flexibility=65      # 水: 保留靈活性
    )

    print("\n【五行分析 - 決策 1】")
    print(f"決策: {result1['content']}")
    print(f"五行分數: {result1['scores']}")
    print(f"平衡指數: {result1['balance_score']}/100")
    print(f"警告信息: {result1['imbalance_warnings']}")
    print(f"相生相剋: {result1['interaction_check']['assessment']}")
    print(f"建議: {result1['recommendation']}")
    print(f"最終判定: {result1['verdict']}")

    # 測試決策 2: 不平衡的決策
    result2 = calc.analyze_decision(
        decision_id="decision_002",
        content="無限擴張·不考慮後果",
        innovation=90,      # 木: 極度創新
        execution=85,       # 火: 超強執行
        stability=20,       # 土: 幾乎沒有基礎
        constraint=15,      # 金: 缺乏約束
        flexibility=80      # 水: 過度漂浮
    )

    print("\n【五行分析 - 決策 2】")
    print(f"決策: {result2['content']}")
    print(f"五行分數: {result2['scores']}")
    print(f"平衡指數: {result2['balance_score']}/100")
    print(f"警告信息: {result2['imbalance_warnings']}")
    print(f"相生相剋: {result2['interaction_check']['assessment']}")
    print(f"建議: {result2['recommendation']}")
    print(f"最終判定: {result2['verdict']}")
    print(f"追蹤碼: {result2['trace']}")
