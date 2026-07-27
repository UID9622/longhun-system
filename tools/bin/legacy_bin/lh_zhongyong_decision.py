#!/usr/bin/env python3
"""
龍魂·五行平衡+中庸决策引擎 v2.0
DNA: #龍芯⚡️丙午·乙申·WUXING-ZHONGYONG-v2.0-CODE-LANDED
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

融合模块:
  - LuckyWuxingModule (P002): 五行平衡分析
  - ZhongYongDecisionModule (P003): 中庸决策
  - 中国式人性管理模型: 话语权动态平衡
  - Lucky式公司管理模型: 财富平衡+纠错机制
"""

from typing import Dict, List, Optional, Any
import datetime
from dataclasses import dataclass, field

# ============================================================
# LuckyWuxingModule (P002) — 五行平衡模块
# ============================================================


class LuckyWuxingModule:
    """五行理论文化注入模块 - 用于系统平衡决策"""

    def __init__(self):
        self.wuxing = {
            "木": {"属性": "生长", "方向": "东", "颜色": "青", "score": 0},
            "火": {"属性": "扩张", "方向": "南", "颜色": "红", "score": 0},
            "土": {"属性": "稳定", "方向": "中", "颜色": "黄", "score": 0},
            "金": {"属性": "收敛", "方向": "西", "颜色": "白", "score": 0},
            "水": {"属性": "流动", "方向": "北", "颜色": "黑", "score": 0},
        }
        self.shengke = {
            "木": {"生": "火", "克": "土"},
            "火": {"生": "土", "克": "金"},
            "土": {"生": "金", "克": "水"},
            "金": {"生": "水", "克": "木"},
            "水": {"生": "木", "克": "火"},
        }
        self.history: List[Dict] = []

    def analyze_balance(self, system_state: Dict[str, Any]) -> Dict[str, Any]:
        """分析系统五行平衡度"""
        scores = {
            "木": system_state.get("growth", 0),
            "火": system_state.get("expansion", 0),
            "土": system_state.get("stability", 0),
            "金": system_state.get("efficiency", 0),
            "水": system_state.get("flexibility", 0),
        }

        for k in scores:
            scores[k] = max(0.0, min(1.0, scores[k]))

        min_element = min(scores.items(), key=lambda x: x[1])
        max_element = max(scores.items(), key=lambda x: x[1])
        balance = self._calculate_balance(scores)
        trend = self._analyze_trend(scores)

        result = {
            "balance_score": balance,
            "weak_point": min_element[0],
            "weak_value": min_element[1],
            "strong_point": max_element[0],
            "strong_value": max_element[1],
            "suggestion": self._generate_balance_advice(min_element[0], scores),
            "trend": trend,
            "all_scores": scores,
        }

        self.history.append({**result, "timestamp": datetime.datetime.now().isoformat()})
        return result

    def _calculate_balance(self, scores: Dict[str, Any]) -> float:
        """计算平衡度（方差越小越平衡）"""
        values = list(scores.values())
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return round(1 - min(variance / 0.2, 1.0), 4)

    def _analyze_trend(self, scores: Dict[str, Any]) -> str:
        """分析五行趋势"""
        if len(self.history) < 2:
            return "初始状态"

        prev = self.history[-1].get("all_scores", {})
        if not prev:
            return "数据不足"

        changes = {}
        for k in scores:
            if k in prev:
                delta = scores[k] - prev[k]
                changes[k] = delta

        improving = [k for k, v in changes.items() if v > 0.05]
        declining = [k for k, v in changes.items() if v < -0.05]

        if improving and not declining:
            return f"上升趋势（{','.join(improving)}增强）"
        elif declining and not improving:
            return f"下降趋势（{','.join(declining)}减弱）"
        elif improving and declining:
            return f"分化趋势（{','.join(improving)}↑ {','.join(declining)}↓）"
        return "稳定趋势"

    def _generate_balance_advice(self, weak_element: str, scores: Dict[str, Any]) -> str:
        """生成平衡建议"""
        sheng_sources = [
            k for k, v in self.shengke.items() if v["生"] == weak_element
        ]
        ke_sources = [
            k for k, v in self.shengke.items() if v["克"] == weak_element
        ]

        advice_parts = []
        advice_parts.append(
            f"系统{weak_element}行不足（{self.wuxing[weak_element]['属性']}能力弱）"
        )

        if sheng_sources:
            advice_parts.append(
                f"建议强化{sheng_sources[0]}行来生旺{weak_element}行"
            )
        if ke_sources:
            advice_parts.append(
                f"注意减弱{ke_sources[0]}行对{weak_element}行的克制"
            )

        return "；".join(advice_parts) + "。"

    def get_wuxing_report(self) -> Dict[str, Any]:
        """获取五行分析报告"""
        if not self.history:
            return {"status": "无数据"}

        latest = self.history[-1]
        return {
            "当前五行": latest.get("all_scores", {}),
            "平衡度": latest.get("balance_score", 0),
            "薄弱环节": latest.get("weak_point", "未知"),
            "建议": latest.get("suggestion", ""),
            "历史记录数": len(self.history),
        }

    def visualize_wuxing(self, scores: Dict[str, Any]) -> str:
        """ASCII可视化五行平衡"""
        max_w = 40
        lines = []
        lines.append("╔═══════════════════════════════╗")
        lines.append("║     五行平衡雷达图 ASCII     ║")
        lines.append("╠═══════════════════════════════╣")
        for element, score in scores.items():
            bar_len = int(score * max_w)
            bar = "█" * bar_len + "░" * (max_w - bar_len)
            direction = self.wuxing[element]["方向"]
            lines.append(f"║ {element}({direction}) [{bar}] {score:.0%} ║")
        lines.append("╚═══════════════════════════════╝")
        return "\n".join(lines)


# ============================================================
# ZhongYongDecisionModule (P003) — 中庸决策模块
# ============================================================


@dataclass
class DecisionOption:
    name: str
    factors: Dict[str, float] = field(default_factory=dict)
    risk: float = 0.5
    opportunity: float = 0.5
    weakness: str = ""


class ZhongYongDecisionModule:
    """中庸之道文化注入模块 - 用于平衡决策"""

    def __init__(self):
        self.factors: List[str] = []
        self.weights: Dict[str, float] = {}
        self.decision_history: List[Dict] = []

    def balanced_decision(self, options: List[Dict]) -> Dict[str, Any]:
        """中庸决策：寻找最平衡的方案"""
        scores = {}

        for option in options:
            balance_score = self._evaluate_balance(option)
            risk_score = self._evaluate_risk(option)
            opportunity_score = self._evaluate_opportunity(option)

            zhongyong_score = round(
                balance_score * 0.4 + risk_score * 0.3 + opportunity_score * 0.3, 4
            )

            scores[option.get("name", "未知")] = {
                "total_score": zhongyong_score,
                "balance": balance_score,
                "risk": risk_score,
                "opportunity": opportunity_score,
                "reasoning": self._generate_reasoning(option, zhongyong_score),
            }

        best_option = max(scores.items(), key=lambda x: x[1]["total_score"])

        result = {
            "recommended": best_option[0],
            "score": best_option[1]["total_score"],
            "reason": best_option[1]["reasoning"],
            "all_scores": scores,
            "decision_level": self._judge_level(best_option[1]["total_score"]),
        }

        self.decision_history.append(result)
        return result

    def _evaluate_balance(self, option: Dict[str, Any]) -> float:
        """评估方案的平衡度"""
        factors = option.get("factors", {})
        if not factors:
            return 0.5
        values = list(factors.values())
        mean = sum(values) / len(values)
        variance = sum(abs(x - mean) for x in values) / len(values)
        return round(1 - min(variance, 1.0), 4)

    def _evaluate_risk(self, option: Dict[str, Any]) -> float:
        """评估风险（风险越低分数越高）"""
        risk = option.get("risk", 0.5)
        return round(1 - risk, 4)

    def _evaluate_opportunity(self, option: Dict[str, Any]) -> float:
        """评估机会"""
        return round(option.get("opportunity", 0.5), 4)

    def _generate_reasoning(self, option: Dict[str, Any], score: float) -> str:
        if score >= 0.8:
            return f"此方案符合中庸之道：既有进取又有稳健，风险可控，机会适中，建议采纳。"
        elif score >= 0.6:
            return f"方案尚可，但需注意{option.get('weakness', '某些方面')}的不足，适度调整后可行。"
        else:
            return f"方案失衡，{option.get('weakness', '风险')}过高或机会不足，建议重新权衡。"

    def _judge_level(self, score: float) -> str:
        if score >= 0.8:
            return "🟢 上策 — 积极推荐"
        elif score >= 0.6:
            return "🟡 中策 — 谨慎可行"
        else:
            return "🔴 下策 — 不推荐"

    def get_best_from_history(self, top_n: int = 3) -> List[Dict]:
        """获取历史最佳决策"""
        sorted_history = sorted(
            self.decision_history, key=lambda x: x["score"], reverse=True
        )
        return sorted_history[:top_n]


# ============================================================
# ChineseManagementModel — 中国式人性管理模型
# ============================================================


class ChineseManagementModel:
    """中国式人性管理模型 - Lucky版本
    核心公式: 付出2份，才能管1份。付出0，凭什么管？
    """

    def __init__(self):
        self.contribution_log: List[Dict] = []
        self.authority_thresholds = {
            "心服口服": 2.0,
            "勉强接受": 1.0,
            "内心不服": 0.0,
        }

    def calculate_authority(self, my_contribution: float, my_demand: float) -> Dict[str, Any]:
        """计算话语权合理性"""
        if my_demand == 0:
            ratio = float("inf")
        else:
            ratio = my_contribution / my_demand

        if ratio >= 2.0:
            level = "心服口服"
        elif ratio >= 1.0:
            level = "勉强接受"
        else:
            level = "内心不服"

        return {
            "contribution": my_contribution,
            "demand": my_demand,
            "ratio": ratio if ratio != float("inf") else "∞",
            "authority_level": level,
            "can_demand": ratio >= 1.0,
            "advice": self._get_authority_advice(level, ratio),
        }

    def self_reflection_check(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """问心无愧检验机制"""
        questions = {
            "我付出了多少？": action.get("contribution", 0),
            "我有资格管吗？": self.calculate_authority(
                action.get("contribution", 0), action.get("demand", 1)
            )["can_demand"],
            "我做到了吗？": action.get("self_done", False),
        }

        all_pass = all(
            v if isinstance(v, bool) else v > 0 for v in questions.values()
        )

        return {
            "questions": questions,
            "result": "可以行动" if all_pass else "先反思，多付出",
            "pass": all_pass,
        }

    def _get_authority_advice(self, level: str, ratio) -> str:
        if level == "心服口服":
            return f"付出比例 {ratio:.1f}:1，你有充分话语权，对方心服口服。"
        elif level == "勉强接受":
            return f"付出比例 {ratio:.1f}:1，对方勉强接受，建议多付出少要求。"
        else:
            return "付出不够，没有资格要求。先付出再多说。"

    @staticmethod
    def chinese_growth_truth(age: int) -> str:
        """中国式成长真相"""
        if age < 18:
            return "有人说你的错（家长·老师·社会教育你）"
        else:
            return "没人说，自己悟（成年人没人教，只能靠自己悟透）"


# ============================================================
# LuckyCompanyModel — Lucky式公司人性管理模型
# ============================================================


class LuckyCompanyModel:
    """Lucky式公司人性管理系统
    核心理念: 财富差距=人性距离，缩小差距减少内耗
    """

    def __init__(self, employee_count: int):
        self.employee_count = employee_count
        self.management_density = self.calculate_density()
        self.tolerance_level = self.calculate_tolerance()
        self.employees: List[Dict] = []

    def calculate_density(self) -> str:
        """人多 → 管理密度高"""
        if self.employee_count > 100:
            return "高密度规则（细节到位·环环相扣）"
        elif self.employee_count > 50:
            return "中密度规则（平衡管理·抓大放小）"
        else:
            return "低密度规则（灵活宽松·人性化）"

    def calculate_tolerance(self) -> Dict[str, Any]:
        """容错空间计算"""
        points = max(1, int(self.employee_count * 0.1))
        return {
            "容错次数": points,
            "扣分规则": "每次-1分，不直接开除",
            "原则": "不是审判，是纠正。不是判死刑，是给机会。",
        }

    def correction_mechanism(self, employee: str, mistake: str) -> List[str]:
        """纠错机制（不是惩罚机制）"""
        return [
            f"1. 警告：向{employee}指出错误 [{mistake}]",
            f"2. 纠正：给出具体改正方案",
            f"3. 跟踪：观察改进情况（1-2周）",
            f"4. 奖励：改好了+1分，公开表扬",
        ]

    def wealth_balance_check(self, salaries: List[float]) -> Dict[str, Any]:
        """财富平衡检查"""
        if not salaries:
            return {"status": "无数据"}

        max_sal = max(salaries)
        min_sal = min(salaries)
        avg_sal = sum(salaries) / len(salaries)
        gap_ratio = (max_sal - min_sal) / avg_sal if avg_sal > 0 else 0

        if gap_ratio < 0.3:
            status = "差距小 → 人性和谐 → 没人管闲事 → 效率高"
            level = "🟢 健康"
        elif gap_ratio < 0.6:
            status = "差距适中 → 略有不满 → 偶有内耗"
            level = "🟡 关注"
        else:
            status = "差距大 → 嫉妒攀比 → 内耗严重 → 效率低"
            level = "🔴 危险"

        return {
            "max_salary": max_sal,
            "min_salary": min_sal,
            "avg_salary": round(avg_sal, 2),
            "gap_ratio": round(gap_ratio, 2),
            "status": status,
            "level": level,
        }

    @staticmethod
    def northeast_mode() -> Dict[str, Any]:
        """东北式公司：起点相似·差距小"""
        return {
            "工资结构": "扁平化，差距≤30%",
            "福利制度": "统一标准，人人平等",
            "晋升机制": "靠能力不靠关系",
            "结果": "人人专注工作，没闲工夫管别人",
            "人性状态": "不嫉妒·不羡慕·不生气",
        }

    @staticmethod
    def southern_mode() -> Dict[str, Any]:
        """南方式公司：阶层分化·差距大"""
        return {
            "工资结构": "金字塔，差距≥100%",
            "福利制度": "差异化，等级分明",
            "晋升机制": "关系和能力并重",
            "结果": "内耗严重，勾心斗角",
            "人性状态": "嫉妒·攀比·焦虑·不满",
        }


# ============================================================
# 测试入口
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🧬 龍魂·五行平衡+中庸决策引擎 v2.0")
    print("=" * 60)

    # --- 五行测试 ---
    wuxing = LuckyWuxingModule()
    state = {
        "growth": 0.85,
        "expansion": 0.70,
        "stability": 0.90,
        "efficiency": 0.65,
        "flexibility": 0.80,
    }
    balance_result = wuxing.analyze_balance(state)
    print(f"\n☯️ 五行平衡分析:")
    print(f"  平衡度: {balance_result['balance_score']:.2%}")
    print(f"  薄弱: {balance_result['weak_point']} ({balance_result['weak_value']:.0%})")
    print(f"  强劲: {balance_result['strong_point']} ({balance_result['strong_value']:.0%})")
    print(f"  建议: {balance_result['suggestion']}")
    print(wuxing.visualize_wuxing(balance_result["all_scores"]))

    # --- 中庸测试 ---
    zhongyong = ZhongYongDecisionModule()
    options = [
        {
            "name": "激进方案",
            "factors": {"速度": 0.9, "成本": 0.3, "质量": 0.5},
            "risk": 0.8,
            "opportunity": 0.9,
            "weakness": "风险过高",
        },
        {
            "name": "稳健方案",
            "factors": {"速度": 0.4, "成本": 0.7, "质量": 0.9},
            "risk": 0.2,
            "opportunity": 0.5,
            "weakness": "机会不足",
        },
        {
            "name": "平衡方案",
            "factors": {"速度": 0.6, "成本": 0.6, "质量": 0.8},
            "risk": 0.4,
            "opportunity": 0.7,
            "weakness": "",
        },
    ]
    decision = zhongyong.balanced_decision(options)
    print(f"\n⚖️ 中庸决策:")
    print(f"  推荐: {decision['recommended']} ({decision['decision_level']})")
    print(f"  得分: {decision['score']:.2%}")
    print(f"  理由: {decision['reason']}")
    for name, s in decision["all_scores"].items():
        print(f"  - {name}: {s['total_score']:.2%}")

    # --- 中国式管理测试 ---
    mgmt = ChineseManagementModel()
    auth = mgmt.calculate_authority(my_contribution=2.0, my_demand=1.0)
    print(f"\n🇨🇳 中国式人性管理:")
    print(f"  付出: 2份, 要求管: 1份 → {auth['authority_level']}")
    print(f"  建议: {auth['advice']}")

    reflection = mgmt.self_reflection_check({
        "contribution": 3.0,
        "demand": 1.0,
        "self_done": True,
    })
    print(f"  问心无愧: {reflection['result']}")

    # --- 公司管理测试 ---
    company = LuckyCompanyModel(employee_count=80)
    print(f"\n🏢 Lucky式公司管理:")
    print(f"  管理密度: {company.calculate_density()}")
    print(f"  容错机制: {company.calculate_tolerance()}")

    balance = company.wealth_balance_check([8000, 10000, 12000, 15000, 30000])
    print(f"  财富平衡: {balance['level']} - {balance['status']}")
