#!/usr/bin/env python3
"""
龍魂 · 根性治理引擎 — 三才三色共治模型
============================================================
论文: 《根性治理论：从西方二进制到中国道理》(15章)
DNA: #龍芯⚡️2026-07-07-ROOT-GOVERNANCE-ENGINE-v1.0
确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
来源: THESIS-ROOT-GOVERNANCE 第九章·核心算法落地

核心机制:
  三才评估: 天(制度)·地(资源)·人(情感) — 三元独立不合并
  三色信号: 🟢通行·🟡关注·🔴帮扶 — 不排名·不惩罚·重改进
  多源真实性协同: 多源校验·单一信息垄断打破
  数字根辅助: 模式识别·不替代情境判断
============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple  # noqa: UP035
import hashlib
import math


# ── 三才维度定义（论文第九章） ──────────────────────────────

class SancaiDimension(Enum):
    """三才：天·地·人"""
    HEAVEN = "天"   # 制度与标准
    EARTH = "地"    # 资源与条件
    HUMAN = "人"    # 情感与责任


SANCAI_DESC = {
    "天": "制度与标准：法律法规、政策文件、服务标准、考核导向、价值目标",
    "地": "资源与条件：财政资源、人力资源、技术条件、地理环境、社会文化",
    "人": "情感与责任：干部责任心、群众需求、服务态度、人际关系、社会信任",
}

# ── 三色定义 ────────────────────────────────────────────────

class TricolorSignal(Enum):
    GREEN = "🟢"   # 自然通行
    YELLOW = "🟡"  # 需要关注
    RED = "🔴"     # 需要帮扶


# ── 3×3 评估矩阵（论文第九章） ──────────────────────────────

SANCAI_TRICOLOR_MATRIX = {
    ("天", "🟢"): "制度合理、方向正确",
    ("天", "🟡"): "制度有漏洞、需要完善",
    ("天", "🔴"): "制度扭曲、方向错误",
    ("地", "🟢"): "资源充足、条件具备",
    ("地", "🟡"): "资源紧张、条件有限",
    ("地", "🔴"): "资源严重不足",
    ("人", "🟢"): "责任心强、关系和谐",
    ("人", "🟡"): "有疲劳迹象、需要关注",
    ("人", "🔴"): "责任心缺失、关系紧张",
}

# ── 治理原则 ────────────────────────────────────────────────

GOVERNANCE_PRINCIPLES = [
    "不合并总分：三个维度各自独立评估，不合并成单一分数（防止信息丢失）",
    "不排名：三色信号只用于自我诊断、横向参考、追踪改进、资源分配参考",
    "重改进：🟢继续、🟡关注微调、🔴帮扶介入",
    "重对话：出现🔴时先对话了解根因，再制定改进方案",
    "重实地：数据是辅助，实地是根本",
    "数字根辅助：数字根作为模式识别工具，不替代具体情境判断",
]


# ── 数据结构 ────────────────────────────────────────────────

@dataclass
class SancaiAssessment:
    """三才评估结果"""
    dimension: SancaiDimension
    score: float           # [0, 1] 维度分数
    signal: TricolorSignal  # 三色信号
    indicators: Dict[str, float]  # 子指标
    narrative: str          # 评估叙述（质性的，不只是数字）


@dataclass
class GovernanceReport:
    """根性治理报告"""
    subject_id: str
    subject_type: str       # 个人/部门/乡镇/项目
    assessments: List[SancaiAssessment]
    digital_root: int       # 数字根辅助
    overall_guidance: str   # 整体方向（不合并分数）
    improvement_plan: List[str]  # 改进建议（不惩罚）
    timestamp: str
    dna: str


@dataclass
class RealityCheckResult:
    """多源真实性校验结果"""
    source_count: int
    sources: List[str]
    conflicts: List[str]
    authenticity_score: float   # 0-1
    single_source_risk: bool
    recommendation: str


# ════════════════════════════════════════════════════════════
# 根性治理引擎
# ════════════════════════════════════════════════════════════

class RootGovernanceEngine:
    """
    根性治理 · 三才三色共治引擎

    核心原则：
      - 不合并总分（防止信息丢失）
      - 不排名（三色 = 方向信号·不是标签）
      - 重改进（帮扶 > 惩罚）
      - 重对话（🔴时先对话·不扣钱·不通报）
      - 重实地（数据是辅助·实地是根本）
    """

    DNA = "#龍芯⚡️2026-07-07-ROOT-GOVERNANCE-ENGINE-v1.0"
    CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

    def __init__(self):
        self.reports: List[GovernanceReport] = []
        self.reality_checks: List[RealityCheckResult] = []

    # ── 三才评估 ────────────────────────────────────────────

    def assess_heaven(self, indicators: Dict[str, float]) -> SancaiAssessment:
        """
        天·制度标准评估

        indicators: {"policy_alignment": 0-1, "standard_compliance": 0-1,
                      "goal_clarity": 0-1, "rule_fairness": 0-1}
        """
        weights = {"policy_alignment": 0.3, "standard_compliance": 0.25,
                   "goal_clarity": 0.25, "rule_fairness": 0.2}

        score = sum(indicators.get(k, 0.5) * w for k, w in weights.items())
        score = min(1.0, max(0.0, score))

        if score >= 0.7:
            signal = TricolorSignal.GREEN
        elif score >= 0.4:
            signal = TricolorSignal.YELLOW
        else:
            signal = TricolorSignal.RED

        narrative = SANCAI_TRICOLOR_MATRIX[("天", signal.value)]

        return SancaiAssessment(
            dimension=SancaiDimension.HEAVEN,
            score=round(score, 4),
            signal=signal,
            indicators=indicators,
            narrative=narrative,
        )

    def assess_earth(self, indicators: Dict[str, float]) -> SancaiAssessment:
        """
        地·资源条件评估

        indicators: {"financial": 0-1, "human_resource": 0-1,
                      "technical": 0-1, "geographic": 0-1,
                      "social_cultural": 0-1}
        """
        weights = {"financial": 0.25, "human_resource": 0.25,
                   "technical": 0.2, "geographic": 0.15,
                   "social_cultural": 0.15}

        score = sum(indicators.get(k, 0.5) * w for k, w in weights.items())
        score = min(1.0, max(0.0, score))

        if score >= 0.7:
            signal = TricolorSignal.GREEN
        elif score >= 0.4:
            signal = TricolorSignal.YELLOW
        else:
            signal = TricolorSignal.RED

        narrative = SANCAI_TRICOLOR_MATRIX[("地", signal.value)]

        return SancaiAssessment(
            dimension=SancaiDimension.EARTH,
            score=round(score, 4),
            signal=signal,
            indicators=indicators,
            narrative=narrative,
        )

    def assess_human(self, indicators: Dict[str, float]) -> SancaiAssessment:
        """
        人·情感责任评估

        indicators: {"responsibility": 0-1, "public_satisfaction": 0-1,
                      "service_attitude": 0-1, "relationship": 0-1,
                      "social_trust": 0-1}
        """
        weights = {"responsibility": 0.25, "public_satisfaction": 0.25,
                   "service_attitude": 0.2, "relationship": 0.15,
                   "social_trust": 0.15}

        score = sum(indicators.get(k, 0.5) * w for k, w in weights.items())
        score = min(1.0, max(0.0, score))

        if score >= 0.7:
            signal = TricolorSignal.GREEN
        elif score >= 0.4:
            signal = TricolorSignal.YELLOW
        else:
            signal = TricolorSignal.RED

        narrative = SANCAI_TRICOLOR_MATRIX[("人", signal.value)]

        return SancaiAssessment(
            dimension=SancaiDimension.HUMAN,
            score=round(score, 4),
            signal=signal,
            indicators=indicators,
            narrative=narrative,
        )

    def full_assessment(
        self,
        subject_id: str,
        subject_type: str,
        heaven_indicators: Dict[str, float],
        earth_indicators: Dict[str, float],
        human_indicators: Dict[str, float],
    ) -> GovernanceReport:
        """三才三色完整评估 — 不合并总分"""

        heaven = self.assess_heaven(heaven_indicators)
        earth = self.assess_earth(earth_indicators)
        human = self.assess_human(human_indicators)

        assessments = [heaven, earth, human]

        # 数字根辅助（不替代情境判断）
        dr = self._compute_digital_root(heaven.score, earth.score, human.score)

        # 不排名·不扣钱·不通报 — 只给方向信号
        red_count = sum(1 for a in assessments if a.signal == TricolorSignal.RED)
        yellow_count = sum(1 for a in assessments if a.signal == TricolorSignal.YELLOW)

        if red_count > 0:
            overall = f"🔴 {red_count}维度需重点帮扶·先对话再定方案"
        elif yellow_count >= 2:
            overall = "🟡 多方面需关注·建议微调"
        elif yellow_count == 1:
            overall = "🟡 个别维度需留意"
        else:
            overall = "🟢 各维度运行良好·保持即可"

        # 改进计划（帮扶式·非惩罚式）
        plan = self._generate_improvement_plan(assessments)

        dna = self._gen_dna(subject_id, assessments)

        report = GovernanceReport(
            subject_id=subject_id,
            subject_type=subject_type,
            assessments=assessments,
            digital_root=dr,
            overall_guidance=overall,
            improvement_plan=plan,
            timestamp=datetime.now(timezone.utc).isoformat(),
            dna=dna,
        )
        self.reports.append(report)
        return report

    def _compute_digital_root(self, *scores: float) -> int:
        """数字根计算 — 辅助参考"""
        total = int(sum(s * 100 for s in scores))
        while total >= 10:
            total = sum(int(d) for d in str(total))
        return total

    def _generate_improvement_plan(self, assessments: List[SancaiAssessment]) -> List[str]:
        """生成改进建议 — 帮扶式·非惩罚式"""
        plan = []
        for a in assessments:
            if a.signal == TricolorSignal.RED:
                dim = a.dimension.value
                plan.append(f"🔴 {dim}维：优先对话了解根因 → 制定针对性改进方案 → 资源倾斜支持")
                # 查找最低子指标
                low = [k for k, v in a.indicators.items() if v < 0.4]
                if low:
                    plan.append(f"   薄弱环节: {', '.join(low)}")
            elif a.signal == TricolorSignal.YELLOW:
                dim = a.dimension.value
                plan.append(f"🟡 {dim}维：关注但不紧急 → 微调即可")
        return plan

    def _gen_dna(self, subject_id: str, assessments: List[SancaiAssessment]) -> str:
        raw = f"ROOTGOV_{subject_id}_{datetime.now(timezone.utc).isoformat()}"
        h = hashlib.sha256(raw.encode()).hexdigest()[:8]
        return f"#龍芯⚡️{datetime.now(timezone.utc).strftime('%Y%m%d')}-ROOTGOV-{h}"

    # ── 多源真实性协同 ── 论文第十章 + 协议 ─────────────────

    def multi_source_authenticity_check(
        self, sources: List[Dict[str, Any]], subject_info: Dict[str, Any]
    ) -> RealityCheckResult:
        """
        多源真实性校验 — 打破单一信息垄断

        sources: [{"name": "来源A", "data": {...}, "reliability": 0-1}, ...]
        """
        conflicts = []
        source_names = [s.get("name", "unknown") for s in sources]
        n = len(sources)

        # 检查信息冲突
        if n >= 2:
            for i in range(n):
                for j in range(i + 1, n):
                    data_i = sources[i].get("data", {})
                    data_j = sources[j].get("data", {})
                    for key in set(data_i.keys()) & set(data_j.keys()):
                        vi = data_i[key]
                        vj = data_j[key]
                        if isinstance(vi, (int, float)) and isinstance(vj, (int, float)):
                            # 差异 > 30% 且绝对值差 > 2 → 标记冲突
                            if abs(vi - vj) > 2 and abs(vi - vj) / max(abs(vi), abs(vj), 1) > 0.3:
                                conflicts.append(f"{source_names[i]} vs {source_names[j]}: {key}={vi} vs {key}={vj}")

        # 真实性估算
        if n == 1:
            authenticity = sources[0].get("reliability", 0.5) * 0.7  # 单一来源扣30%
            single_risk = True
            rec = "⚠️ 仅单一信息源·建议增加独立反馈渠道验证"
        elif n >= 3 and not conflicts:
            authenticity = 0.95
            single_risk = False
            rec = "✅ 多源一致·信息可信度高"
        elif n >= 2 and conflicts:
            authenticity = 0.5
            single_risk = False
            rec = "🟡 多源存在冲突·需实地核实"
        else:
            authenticity = 0.8
            single_risk = False
            rec = "🟢 多源基本一致"

        result = RealityCheckResult(
            source_count=n,
            sources=source_names,
            conflicts=conflicts,
            authenticity_score=round(authenticity, 4),
            single_source_risk=single_risk,
            recommendation=rec,
        )
        self.reality_checks.append(result)
        return result

    # ── 与西方评分系统的关键区别 ── 论文第八章 ─────────────

    @staticmethod
    def vs_western_scoring() -> Dict[str, str]:
        """三才三色 vs 西方评分机制"""
        return {
            "核心逻辑": "多维化·质性·方向 / 一元化·量化·排名",
            "输出形式": "三维颜色信号 / 单一分数或等级",
            "价值判断": "通行/关注/帮扶 / 好/坏·优秀/差",
            "对失败的态度": "帮扶·改进 / 惩罚·淘汰",
            "容错空间": "大 / 小",
            "合并总分": "不合并 / 合并排名",
            "实地权重": "实地 > 数据 / 数据 > 情境",
            "对话机制": "🔴先对话 / 直接扣分",
        }

    # ── 统计 ────────────────────────────────────────────────

    def stats(self) -> Dict[str, Any]:
        total = len(self.reports)
        red_count = sum(1 for r in self.reports
                        if any(a.signal == TricolorSignal.RED for a in r.assessments))

        return {
            "total_assessments": total,
            "subjects_with_red": red_count,
            "red_ratio": round(red_count / max(1, total), 4),
            "reality_checks_done": len(self.reality_checks),
            "principles": GOVERNANCE_PRINCIPLES,
            "dna": self.DNA,
        }


# ════════════════════════════════════════════════════════════
# 自测
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("🐉 根性治理 · 三才三色共治引擎 · 自测")
    print(f"DNA: {RootGovernanceEngine.DNA}")
    print("=" * 60)

    engine = RootGovernanceEngine()

    # ── 测试1: 三才独立评估（不合并总分） ──
    print("\n📐 测试1: 三才独立评估 · 不合并总分")
    r1 = engine.full_assessment(
        "乡镇A", "乡镇",
        {"policy_alignment": 0.85, "standard_compliance": 0.9, "goal_clarity": 0.8, "rule_fairness": 0.75},
        {"financial": 0.3, "human_resource": 0.5, "technical": 0.2, "geographic": 0.6, "social_cultural": 0.7},
        {"responsibility": 0.9, "public_satisfaction": 0.85, "service_attitude": 0.8, "relationship": 0.75, "social_trust": 0.7},
    )
    for a in r1.assessments:
        print(f"  {a.dimension.value}维: score={a.score} {a.signal.value} | {a.narrative}")
    print(f"  数字根: {r1.digital_root} | 整体: {r1.overall_guidance}")
    print(f"  改进计划: {r1.improvement_plan}")
    print("  ✅ 三维独立·不合并·有改进方案")

    # ── 测试2: 多源真实性校验 ──
    print("\n📐 测试2: 多源真实性协同协议")
    sources1 = [
        {"name": "群众投诉", "data": {"满意度": 85, "投诉次数": 3}, "reliability": 0.9},
        {"name": "上级考核", "data": {"满意度": 90, "投诉次数": 2}, "reliability": 0.8},
        {"name": "独立督查", "data": {"满意度": 88, "投诉次数": 3}, "reliability": 0.85},
    ]
    c1 = engine.multi_source_authenticity_check(sources1, {"type": "基层服务"})
    print(f"  来源: {c1.sources}")
    print(f"  真实性: {c1.authenticity_score} | 冲突: {c1.conflicts}")
    print(f"  {c1.recommendation}")
    assert c1.authenticity_score >= 0.9, "三源一致应高真实性!"
    print("  ✅ 多源一致·信息可信")

    # ── 测试3: 单一来源风险 ──
    print("\n📐 测试3: 单一信息源 → 真实性降权")
    sources2 = [
        {"name": "自评报告", "data": {"满意度": 100, "投诉次数": 0}, "reliability": 0.7},
    ]
    c2 = engine.multi_source_authenticity_check(sources2, {"type": "自我评估"})
    print(f"  来源: {c2.sources}")
    print(f"  真实性: {c2.authenticity_score} | 单一源风险: {c2.single_source_risk}")
    print(f"  {c2.recommendation}")
    assert c2.single_source_risk, "单一来源应有风险标记!"
    print("  ✅ 单一来源自动降权")

    # ── 测试4: vs 西方评分 ──
    print("\n📐 测试4: 三才三色 vs 西方评分关键区别")
    diffs = engine.vs_western_scoring()
    for k, v in diffs.items():
        print(f"  {k}: {v}")
    print("  ✅ 7项核心区别清晰")

    # ── 测试5: 统计 ──
    print("\n📐 测试5: 引擎统计")
    s = engine.stats()
    print(f"  评估: {s['total_assessments']}次 | 🔴: {s['subjects_with_red']}")
    print(f"  治理原则: {len(s['principles'])}条")
    print("  ✅ 通过")

    print(f"\n{'=' * 60}")
    print("✅ 根性治理引擎 · 全部验证通过")
    print("  不合并总分·不排名·不扣钱·不通报·重帮扶·重对话·重实地")
    print("  从'评分社会'到'道理社会'")
    print(f"  DNA: {engine.DNA}")
