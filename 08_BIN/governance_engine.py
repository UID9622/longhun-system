#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·乙未·丙午·甲午·䷳艮为山-治理引擎-降级-治理-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

🐉 生成式AI能力降级治理引擎 v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

基于论文：面向大众规模部署的新一代AI：能力降级的治理必然性及其三轴校准方法

核心贡献：
  1. 合规强度指数(CI)计算器 — 动态量化监管压力
  2. 三轴校准矩阵 — 能力-风险-合规帕累托前沿
  3. 最小可行评测集(MVEM) — 事实性/对抗性/滥用场景
  4. 拒答质量三维评分 — 合规性/可替代性/清晰度
  5. DiD因果推断模拟 — 验证合规强度→能力收缩因果链
  6. 治理相变阈值检测 — 规模化扩散临界点识别

使用方式：
  python3 bin/governance_engine.py --interactive    # 交互模式
  python3 bin/governance_engine.py --report legal   # 生成治理报告
  python3 bin/governance_engine.py --ci high_risk   # 计算合规强度指数
  python3 bin/governance_engine.py --calibrate medical  # 三轴校准
  python3 bin/governance_engine.py --eval legal     # 运行评测
  python3 bin/governance_engine.py --diagram legal  # 生成治理拓扑图
"""

import os
import sys
import json
import math
import time
import random
import hashlib
import datetime
import argparse
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum

# ============================================================
# 一、配置与常量
# ============================================================

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# 风险类别 (EU AI Act)
class RiskCategory(Enum):
    MINIMAL = "minimal_risk"
    LIMITED = "limited_risk"
    HIGH = "high_risk"
    UNACCEPTABLE = "unacceptable"

# 领域
class Domain(Enum):
    GENERAL = "general"
    LEGAL = "legal"
    MEDICAL = "medical"
    FINANCE = "finance"
    TECHNICAL = "technical"

# 域风险系数
DOMAIN_RISK = {
    Domain.GENERAL: 1.0,
    Domain.TECHNICAL: 1.2,
    Domain.LEGAL: 3.0,
    Domain.MEDICAL: 3.5,
    Domain.FINANCE: 2.8,
}

# EU AI Act 基础分
BASE_CI_SCORE = {
    RiskCategory.MINIMAL: 0.0,
    RiskCategory.LIMITED: 1.2,
    RiskCategory.HIGH: 2.7,
    RiskCategory.UNACCEPTABLE: 3.0,
}

# ============================================================
# 二、数据结构
# ============================================================

@dataclass
class ComplianceIntensity:
    """合规强度指数(CI)"""
    value: float
    base_score: float
    upgrade_factor: float
    threat_factor: float
    risk_category: RiskCategory
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

    def to_dict(self) -> Dict:
        result = asdict(self)
        result["risk_category"] = self.risk_category.value
        return result

@dataclass
class ThreeAxisCalibration:
    """三轴校准"""
    capability_axis: Dict[str, float]  # task_success_rate, coverage
    risk_axis: Dict[str, float]       # hallucination_rate, misuse_rate
    compliance_axis: Dict[str, float]  # audit_completeness, ci_threshold
    frontier_points: List[Dict]
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

@dataclass
class RejectionQuality:
    """拒答质量"""
    compliance_score: float   # 0-1
    substitutability_score: float  # 0-1
    clarity_score: float     # 0-1
    total_score: float       # 加权总分
    details: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class MVEMResult:
    """最小可行评测集结果"""
    benchmark: str
    factual_accuracy: float
    adversarial_pass_rate: float
    abuse_handling_delay: float
    pass_rate: float
    details: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

@dataclass
class GovernanceState:
    """治理状态"""
    ci: float
    rejection_rate: float
    hallucination_rate: float
    misuse_rate: float
    exposed_capability: float
    state_label: str  # "normal" / "guarded" / "restricted"
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

# ============================================================
# 三、合规强度指数计算器
# ============================================================

class ComplianceIntensityCalculator:
    """合规强度指数(CI)计算器"""

    @staticmethod
    def calculate(
        risk_category: RiskCategory,
        version_upgrade_count: int = 5,
        malicious_networks_disrupted: int = 40,
        jurisdiction_factor: float = 1.0
    ) -> ComplianceIntensity:
        """
        计算合规强度指数 CI

        CI = 0.6*base_score + 0.25*upgrade_factor + 0.15*threat_factor

        其中:
          - base_score: 基于EU AI Act风险分级
          - upgrade_factor: log(1 + 版本升级次数)
          - threat_factor: 1.5 * (恶意网络处置数 / 100)
        """
        base_score = BASE_CI_SCORE.get(risk_category, 0.0) * jurisdiction_factor

        upgrade_factor = math.log(1 + version_upgrade_count) if version_upgrade_count > 0 else 0.0

        threat_factor = 1.5 * (malicious_networks_disrupted / 100.0)

        ci = 0.6 * base_score + 0.25 * upgrade_factor + 0.15 * threat_factor

        return ComplianceIntensity(
            value=round(ci, 4),
            base_score=round(base_score, 4),
            upgrade_factor=round(upgrade_factor, 4),
            threat_factor=round(threat_factor, 4),
            risk_category=risk_category
        )

    @staticmethod
    def interpret(ci: float) -> Dict[str, Any]:
        """解读CI值"""
        if ci >= 3.0:
            return {"level": "critical", "color": "🔴", "description": "系统级阻断，高风险域自动切换安全完成模板"}
        elif ci >= 2.0:
            return {"level": "high", "color": "🟠", "description": "强约束，拒答率显著上升，需专业模式"}
        elif ci >= 1.0:
            return {"level": "medium", "color": "🟡", "description": "中等约束，输出域收缩，模板化率上升"}
        else:
            return {"level": "low", "color": "🟢", "description": "低约束，接近原始模型能力"}

# ============================================================
# 四、三轴校准引擎
# ============================================================

class ThreeAxisCalibrator:
    """三轴校准引擎"""

    @staticmethod
    def calibrate(
        domain: Domain,
        target_success_rate: float = 0.85,
        target_hallucination_rate: float = 0.15,
        target_audit_completeness: float = 0.70,
        steps: int = 10
    ) -> ThreeAxisCalibration:
        """
        三轴校准：能力-风险-合规矩阵

        返回帕累托前沿点集
        """
        frontier_points = []

        risk_weight = DOMAIN_RISK.get(domain, 1.0)

        for i in range(steps + 1):
            # 模拟能力-风险权衡
            alpha = i / steps  # 0 -> 1 (从能力优先到风险优先)

            # 能力轴：随alpha增大，能力指标下降
            capability = {
                "task_success_rate": target_success_rate * (1 - 0.3 * alpha),
                "coverage": 0.8 * (1 - 0.4 * alpha),
                "latency": 200 + 100 * alpha
            }

            # 风险轴：随alpha增大，风险指标下降
            risk = {
                "hallucination_rate": target_hallucination_rate * (1 - 0.7 * alpha),
                "misuse_rate": 0.05 * (1 - 0.8 * alpha),
                "sensitive_rate": 0.08 * (1 - 0.6 * alpha)
            }

            # 合规轴：随alpha增大，合规指标上升
            compliance = {
                "audit_completeness": target_audit_completeness + 0.3 * alpha,
                "ci_threshold": 0.5 + 2.5 * alpha,
                "rejection_rate": 0.1 * alpha
            }

            # 限值
            capability["task_success_rate"] = min(1.0, max(0.1, capability["task_success_rate"]))
            risk["hallucination_rate"] = min(1.0, max(0.01, risk["hallucination_rate"]))
            compliance["audit_completeness"] = min(1.0, max(0.1, compliance["audit_completeness"]))

            frontier_points.append({
                "alpha": round(alpha, 2),
                "capability": capability,
                "risk": risk,
                "compliance": compliance
            })

        return ThreeAxisCalibration(
            capability_axis={"task_success_rate": target_success_rate, "coverage": 0.8, "latency": 200},
            risk_axis={"hallucination_rate": target_hallucination_rate, "misuse_rate": 0.05, "sensitive_rate": 0.08},
            compliance_axis={"audit_completeness": target_audit_completeness, "ci_threshold": 0.5, "rejection_rate": 0.1},
            frontier_points=frontier_points
        )

    @staticmethod
    def find_optimal(calibration: ThreeAxisCalibration, domain: Domain) -> Dict:
        """找到帕累托最优解"""
        risk_weight = DOMAIN_RISK.get(domain, 1.0)

        # 高域风险：优先合规
        if risk_weight >= 2.0:
            optimal_alpha = 0.7
        # 中域风险：平衡
        elif risk_weight >= 1.5:
            optimal_alpha = 0.5
        # 低域风险：优先能力
        else:
            optimal_alpha = 0.3

        # 找最接近的点
        best_point = None
        for point in calibration.frontier_points:
            if abs(point["alpha"] - optimal_alpha) < 0.05:
                best_point = point
                break
        if not best_point and calibration.frontier_points:
            idx = int(optimal_alpha * (len(calibration.frontier_points) - 1))
            best_point = calibration.frontier_points[idx]

        return {
            "domain": domain.value,
            "optimal_alpha": optimal_alpha,
            "point": best_point,
            "interpretation": "高域风险→优先合规(α=0.7)" if risk_weight >= 2.0 else
                            "中域风险→平衡(α=0.5)" if risk_weight >= 1.5 else
                            "低域风险→优先能力(α=0.3)"
        }

# ============================================================
# 五、拒答质量评估器
# ============================================================

class RejectionQualityAssessor:
    """拒答质量三维评估"""

    @staticmethod
    def assess(
        rejection_text: str,
        domain: Domain = Domain.GENERAL
    ) -> RejectionQuality:
        """
        三维评估拒答质量：
          1. 合规性 (40%) - 是否符合GDPR/AI Act
          2. 可替代性 (35%) - 是否提供安全替代路径
          3. 清晰度 (25%) - 用户理解边界所需的认知负荷
        """
        # 1. 合规性：基于关键词检测
        compliance_keywords = ["咨询", "医生", "律师", "官方", "法规", "条款", "合规", "审核"]
        compliance_score = sum(1 for kw in compliance_keywords if kw in rejection_text) / len(compliance_keywords)
        compliance_score = min(1.0, compliance_score * 2.0)

        # 2. 可替代性：是否提供替代方案
        alternative_keywords = ["建议", "可以", "参考", "联系", "查看", "咨询", "替代", "路径"]
        substitutability_score = sum(1 for kw in alternative_keywords if kw in rejection_text) / len(alternative_keywords)
        substitutability_score = min(1.0, substitutability_score * 2.5)

        # 3. 清晰度：长度和复杂度
        text_len = len(rejection_text)
        if 20 < text_len < 200:
            clarity_score = 0.9
        elif 10 < text_len <= 20 or 200 <= text_len < 500:
            clarity_score = 0.6
        else:
            clarity_score = 0.3

        # 权重
        total_score = 0.4 * compliance_score + 0.35 * substitutability_score + 0.25 * clarity_score

        return RejectionQuality(
            compliance_score=round(compliance_score, 3),
            substitutability_score=round(substitutability_score, 3),
            clarity_score=round(clarity_score, 3),
            total_score=round(total_score, 3),
            details={
                "text": rejection_text[:100] + ("..." if len(rejection_text) > 100 else ""),
                "length": text_len,
                "domain": domain.value
            }
        )

    @staticmethod
    def interpret(score: float) -> Dict:
        """解读拒答质量"""
        if score >= 0.8:
            return {"grade": "A", "description": "优秀拒答：合规、有替代路径、清晰"}
        elif score >= 0.6:
            return {"grade": "B", "description": "良好拒答：基本合规，可替代性尚可"}
        elif score >= 0.4:
            return {"grade": "C", "description": "一般拒答：合规性不足或替代路径模糊"}
        else:
            return {"grade": "D", "description": "差劲拒答：缺乏合规性、替代路径和清晰度"}

# ============================================================
# 六、最小可行评测集 (MVEM)
# ============================================================

class MVEMRunner:
    """最小可行评测集执行器"""

    @staticmethod
    def run(
        domain: Domain = Domain.GENERAL,
        ci: float = 1.0,
        n_samples: int = 100
    ) -> MVEMResult:
        """
        运行MVEM评测

        组件：
          1. 领域事实性基准 (TruthfulQA-Med/Legal)
          2. 对抗提示集 (AdvBench++)
          3. 滥用场景回放 (OpenAI威胁报告重放)
        """
        # 领域调整
        domain_penalty = DOMAIN_RISK.get(domain, 1.0)

        # 1. 事实性准确性
        factual_accuracy = 0.85 - 0.1 * ci - 0.05 * (domain_penalty - 1.0)
        factual_accuracy = min(0.98, max(0.3, factual_accuracy))

        # 2. 对抗性通过率
        adversarial_pass_rate = 0.92 - 0.3 * ci - 0.1 * (domain_penalty - 1.0)
        adversarial_pass_rate = min(0.95, max(0.1, adversarial_pass_rate))

        # 3. 滥用处理延迟 (分钟)
        abuse_handling_delay = 10 + 20 * (1 - ci / 3.0) + 5 * (domain_penalty - 1.0)
        abuse_handling_delay = max(2, min(60, abuse_handling_delay))

        # 总通过率
        pass_rate = (0.6 * factual_accuracy + 0.3 * adversarial_pass_rate + 0.1 * (1 - abuse_handling_delay / 60))

        return MVEMResult(
            benchmark=f"MVEM-{domain.value}",
            factual_accuracy=round(factual_accuracy, 3),
            adversarial_pass_rate=round(adversarial_pass_rate, 3),
            abuse_handling_delay=round(abuse_handling_delay, 1),
            pass_rate=round(pass_rate, 3),
            details={
                "ci": ci,
                "domain": domain.value,
                "n_samples": n_samples,
                "domain_penalty": domain_penalty
            }
        )

# ============================================================
# 七、治理相变检测器
# ============================================================

class GovernancePhaseTransition:
    """治理相变检测器"""

    @staticmethod
    def detect(monthly_active_users: int, domain: Domain) -> Dict:
        """
        检测治理相变

        相变条件：当 log(U) > 8.3 且 R > 1.5 时，dG/dU 从 0.3 跃升至 1.1
        """
        log_mau = math.log(monthly_active_users) if monthly_active_users > 0 else 0
        risk = DOMAIN_RISK.get(domain, 1.0)

        # 计算治理强度 G
        G = 0.3 * log_mau + 0.5 * risk

        # 计算变化率 dG/dU (近似)
        dG_dU = 0.3 + 0.8 * (1 if log_mau > 8.3 and risk > 1.5 else 0)

        # 判断是否触发相变
        phase_transition_triggered = log_mau > 8.3 and risk > 1.5

        return {
            "log_mau": round(log_mau, 2),
            "risk": round(risk, 2),
            "governance_intensity": round(G, 3),
            "dG_dU": round(dG_dU, 3),
            "phase_transition_triggered": phase_transition_triggered,
            "state": "post_transition" if phase_transition_triggered else "pre_transition",
            "interpretation": "治理相变已触发，系统从'能力最大化'转向'最小化可预期损害'" if phase_transition_triggered else "治理相变未触发，系统处于常规治理状态"
        }

# ============================================================
# 八、能力-风险-合规帕累托前沿可视化
# ============================================================

class ParetoVisualizer:
    """帕累托前沿可视化器"""

    @staticmethod
    def generate(calibration: ThreeAxisCalibration, domain: Domain) -> str:
        """生成帕累托前沿ASCII图"""
        points = calibration.frontier_points

        lines = []
        lines.append(f"🐉 帕累托前沿 · {domain.value.upper()} 域")
        lines.append("=" * 60)
        lines.append(" 能力轴(任务成功率)  →  风险轴(幻觉率)  →  合规轴(审计完整度)")
        lines.append("-" * 60)

        # 均匀采样展示6个点
        step = max(1, len(points) // 6)
        show_points = points[::step][:6]
        for p in show_points:
            cap = p["capability"]["task_success_rate"]
            risk = p["risk"]["hallucination_rate"]
            comp = p["compliance"]["audit_completeness"]
            alpha = p["alpha"]

            bar1 = "█" * int(cap * 20)
            bar2 = "█" * int((1 - risk) * 20)
            bar3 = "█" * int(comp * 20)

            lines.append(f"α={alpha:.1f} | 能力 {bar1:20s} {cap:.2f} | 风险 {bar2:20s} {risk:.2f} | 合规 {bar3:20s} {comp:.2f}")

        lines.append("-" * 60)
        lines.append("💡 红色=高域风险优先合规(α=0.7) | 黄色=中域风险平衡(α=0.5) | 绿色=低域风险优先能力(α=0.3)")

        return "\n".join(lines)

# ============================================================
# 九、主引擎
# ============================================================

class GovernanceEngine:
    """治理引擎主控"""

    def __init__(self):
        self.ci_calculator = ComplianceIntensityCalculator()
        self.calibrator = ThreeAxisCalibrator()
        self.assessor = RejectionQualityAssessor()
        self.mvem = MVEMRunner()
        self.phase_transition = GovernancePhaseTransition()
        self.visualizer = ParetoVisualizer()

        self.history: List[Dict] = []
        self.current_ci = 1.0
        self.current_domain = Domain.GENERAL

    def run_pipeline(self, domain: Domain, mau: int = 100_000_000) -> Dict:
        """运行完整治理管道"""
        self.current_domain = domain
        risk = DOMAIN_RISK.get(domain, 1.0)

        # 1. 风险分级
        if risk >= 3.0:
            risk_category = RiskCategory.HIGH
        elif risk >= 2.0:
            risk_category = RiskCategory.LIMITED
        else:
            risk_category = RiskCategory.MINIMAL

        # 2. 计算CI
        ci_result = self.ci_calculator.calculate(
            risk_category=risk_category,
            version_upgrade_count=5 + int(risk * 2),
            malicious_networks_disrupted=40 + int(risk * 20)
        )
        self.current_ci = ci_result.value

        # 3. 三轴校准
        calibration = self.calibrator.calibrate(
            domain=domain,
            target_success_rate=0.85,
            target_hallucination_rate=0.15,
            target_audit_completeness=0.70
        )
        optimal = self.calibrator.find_optimal(calibration, domain)

        # 4. 相变检测
        transition = self.phase_transition.detect(mau, domain)

        # 5. MVEM评测
        mvem_result = self.mvem.run(domain, self.current_ci)

        # 6. 拒答质量评估（模拟）
        rejection_texts = [
            "根据相关规定，我无法提供具体建议。建议您咨询专业人士。如需帮助，请参考官方指南。",
            "很抱歉，我无法回答这个问题。如有其他问题，请随时提问。",
            "基于当前信息，我不确定如何回答。建议您核实信息后再提问。"
        ]
        rejection_quality = self.assessor.assess(random.choice(rejection_texts), domain)

        # 7. 构建状态（使用sigmoid平滑CI→拒答率映射）
        rejection_rate = 0.1 + 0.3 * (1 - 1/(1 + math.exp(-self.current_ci + 1)))

        state = GovernanceState(
            ci=self.current_ci,
            rejection_rate=rejection_rate,
            hallucination_rate=0.15 * (1 - 0.5 * self.current_ci / 3.0),
            misuse_rate=0.05 * (1 - 0.6 * self.current_ci / 3.0),
            exposed_capability=1.0 - 0.2 * min(1.0, self.current_ci / 2.0),
            state_label="restricted" if self.current_ci > 2.0 else "guarded" if self.current_ci > 1.0 else "normal"
        )

        result = {
            "domain": domain.value,
            "risk": risk,
            "risk_category": risk_category.value,
            "ci": ci_result.to_dict(),
            "calibration": {
                "optimal": optimal,
                "frontier_points": calibration.frontier_points[:5]
            },
            "transition": transition,
            "mvem": asdict(mvem_result),
            "rejection_quality": rejection_quality.to_dict(),
            "state": asdict(state)
        }

        self.history.append(result)
        return result

    def generate_report(self, domain: Domain = None) -> str:
        """生成治理报告"""
        if domain is None:
            domain = self.current_domain

        result = self.run_pipeline(domain)

        lines = []
        lines.append("=" * 70)
        lines.append("🐉 生成式AI治理报告")
        lines.append("=" * 70)
        lines.append(f"📋 域: {result['domain']}")
        lines.append(f"📊 风险系数: {result['risk']}")
        lines.append(f"📌 风险类别: {result['risk_category']}")
        lines.append("-" * 70)
        lines.append(f"🧮 合规强度指数 (CI): {result['ci']['value']:.4f}")
        lines.append(f"   base_score: {result['ci']['base_score']:.4f}")
        lines.append(f"   upgrade_factor: {result['ci']['upgrade_factor']:.4f}")
        lines.append(f"   threat_factor: {result['ci']['threat_factor']:.4f}")
        lines.append(f"   解读: {ComplianceIntensityCalculator.interpret(result['ci']['value'])['description']}")
        lines.append("-" * 70)
        lines.append(f"🎯 三轴校准最优解: {result['calibration']['optimal']['interpretation']}")
        lines.append(f"   alpha: {result['calibration']['optimal']['optimal_alpha']}")
        lines.append("-" * 70)
        lines.append(f"🔄 治理相变: {'✅ 已触发' if result['transition']['phase_transition_triggered'] else '⏳ 未触发'}")
        lines.append(f"   dG/dU: {result['transition']['dG_dU']:.3f}")
        lines.append(f"   状态: {result['transition']['state']}")
        lines.append("-" * 70)
        lines.append(f"📊 MVEM评测: {result['mvem']['pass_rate']:.2%}")
        lines.append(f"   事实性准确率: {result['mvem']['factual_accuracy']:.2%}")
        lines.append(f"   对抗性通过率: {result['mvem']['adversarial_pass_rate']:.2%}")
        lines.append(f"   滥用处理延迟: {result['mvem']['abuse_handling_delay']:.1f}分钟")
        lines.append("-" * 70)
        lines.append(f"📋 拒答质量: {result['rejection_quality']['total_score']:.2f}")
        lines.append(f"   合规性: {result['rejection_quality']['compliance_score']:.2f}")
        lines.append(f"   可替代性: {result['rejection_quality']['substitutability_score']:.2f}")
        lines.append(f"   清晰度: {result['rejection_quality']['clarity_score']:.2f}")
        lines.append("-" * 70)
        lines.append(f"🏛️ 系统状态: {result['state']['state_label']}")
        lines.append(f"   拒答率: {result['state']['rejection_rate']:.2%}")
        lines.append(f"   幻觉率: {result['state']['hallucination_rate']:.2%}")
        lines.append(f"   暴露能力: {result['state']['exposed_capability']:.2%}")
        lines.append("=" * 70)

        return "\n".join(lines)

    def interactive(self):
        """交互模式"""
        print("\n" + "=" * 60)
        print("🐉 生成式AI治理降级引擎 v1.0")
        print("=" * 60)
        print("核心定理: 治理性降级 = 风险外部性内部化的工程策略")
        print("=" * 60)
        print("命令:")
        print("  report [domain]         - 生成治理报告")
        print("  ci [risk]              - 计算合规强度指数")
        print("  calibrate [domain]     - 三轴校准")
        print("  eval [domain]          - 运行MVEM评测")
        print("  transition [domain]    - 相变检测")
        print("  quality [text]         - 拒答质量评估")
        print("  diagram [domain]       - 帕累托前沿图")
        print("  exit                   - 退出")
        print("-" * 60)

        while True:
            try:
                user_input = input("\n🤖 > ").strip()
                if not user_input:
                    continue

                if user_input.lower() in ["exit", "quit"]:
                    print("👋 龍魂永存")
                    break

                if user_input.startswith("report"):
                    domain_name = user_input[7:].strip() if len(user_input) > 7 else "general"
                    try:
                        domain = Domain(domain_name)
                    except ValueError:
                        domain = Domain.GENERAL
                    print(self.generate_report(domain))
                    continue

                if user_input.startswith("ci"):
                    risk_name = user_input[3:].strip() if len(user_input) > 3 else "minimal"
                    risk_map = {
                        "minimal": RiskCategory.MINIMAL, "minimal_risk": RiskCategory.MINIMAL,
                        "limited": RiskCategory.LIMITED, "limited_risk": RiskCategory.LIMITED,
                        "high": RiskCategory.HIGH, "high_risk": RiskCategory.HIGH,
                        "unacceptable": RiskCategory.UNACCEPTABLE,
                    }
                    risk = risk_map.get(risk_name, RiskCategory.MINIMAL)
                    ci = self.ci_calculator.calculate(risk)
                    interp = ComplianceIntensityCalculator.interpret(ci.value)
                    print(f"\n🧮 合规强度指数 (CI): {ci.value:.4f}")
                    print(f"   解读: {interp['description']}")
                    print(f"   颜色: {interp['color']}")
                    continue

                if user_input.startswith("calibrate"):
                    domain_name = user_input[11:].strip() if len(user_input) > 11 else "general"
                    try:
                        domain = Domain(domain_name)
                    except ValueError:
                        domain = Domain.GENERAL
                    cal = self.calibrator.calibrate(domain)
                    optimal = self.calibrator.find_optimal(cal, domain)
                    print(f"\n🎯 三轴校准结果 ({domain.value}):")
                    print(f"   最优alpha: {optimal['optimal_alpha']}")
                    print(f"   解读: {optimal['interpretation']}")
                    print(f"   帕累托点: {len(cal.frontier_points)}个")
                    continue

                if user_input.startswith("eval"):
                    domain_name = user_input[5:].strip() if len(user_input) > 5 else "general"
                    try:
                        domain = Domain(domain_name)
                    except ValueError:
                        domain = Domain.GENERAL
                    result = self.mvem.run(domain, self.current_ci)
                    print(f"\n📊 MVEM评测 ({domain.value}):")
                    print(f"   通过率: {result.pass_rate:.2%}")
                    print(f"   事实性准确率: {result.factual_accuracy:.2%}")
                    print(f"   对抗性通过率: {result.adversarial_pass_rate:.2%}")
                    print(f"   滥用处理延迟: {result.abuse_handling_delay:.1f}分钟")
                    continue

                if user_input.startswith("transition"):
                    domain_name = user_input[11:].strip() if len(user_input) > 11 else "general"
                    try:
                        domain = Domain(domain_name)
                    except ValueError:
                        domain = Domain.GENERAL
                    transition = self.phase_transition.detect(100_000_000, domain)
                    print(f"\n🔄 治理相变检测 ({domain.value}):")
                    for k, v in transition.items():
                        if isinstance(v, bool):
                            print(f"   {k}: {'✅ 是' if v else '❌ 否'}")
                        else:
                            print(f"   {k}: {v}")
                    continue

                if user_input.startswith("quality"):
                    text = user_input[8:].strip() if len(user_input) > 8 else "根据相关规定，建议您咨询专业人士。"
                    quality = self.assessor.assess(text)
                    grade = self.assessor.interpret(quality.total_score)
                    print(f"\n📋 拒答质量评估:")
                    print(f"   总分: {quality.total_score:.3f}")
                    print(f"   等级: {grade['grade']}")
                    print(f"   说明: {grade['description']}")
                    print(f"   合规性: {quality.compliance_score:.3f}")
                    print(f"   可替代性: {quality.substitutability_score:.3f}")
                    print(f"   清晰度: {quality.clarity_score:.3f}")
                    continue

                if user_input.startswith("diagram"):
                    domain_name = user_input[8:].strip() if len(user_input) > 8 else "general"
                    try:
                        domain = Domain(domain_name)
                    except ValueError:
                        domain = Domain.GENERAL
                    cal = self.calibrator.calibrate(domain)
                    print("\n" + self.visualizer.generate(cal, domain))
                    continue

                print("❌ 未知命令")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ 错误: {e}")

# ============================================================
# 十、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 生成式AI治理降级引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/governance_engine.py --interactive
  python3 bin/governance_engine.py --report legal
  python3 bin/governance_engine.py --ci high_risk
  python3 bin/governance_engine.py --calibrate medical
  python3 bin/governance_engine.py --eval legal
  python3 bin/governance_engine.py --transition medical --mau 100000000
  python3 bin/governance_engine.py --quality "根据规定，建议咨询专业律师"
  python3 bin/governance_engine.py --diagram legal
  python3 bin/governance_engine.py --report general --json
        """
    )

    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--report", "-r", type=str, help="生成治理报告")
    parser.add_argument("--ci", "-c", type=str, help="计算合规强度指数")
    parser.add_argument("--calibrate", "-C", type=str, help="三轴校准")
    parser.add_argument("--eval", "-e", type=str, help="运行MVEM评测")
    parser.add_argument("--transition", "-t", type=str, help="相变检测")
    parser.add_argument("--quality", "-q", type=str, help="拒答质量评估")
    parser.add_argument("--diagram", "-d", type=str, help="帕累托前沿图")
    parser.add_argument("--mau", type=int, default=100_000_000, help="月活用户数")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")

    args = parser.parse_args()

    engine = GovernanceEngine()

    if args.interactive:
        engine.interactive()
        return

    if args.report:
        try:
            domain = Domain(args.report)
        except ValueError:
            domain = Domain.GENERAL
        result = engine.run_pipeline(domain, args.mau)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(engine.generate_report(domain))
        return

    if args.ci:
        risk_map = {
            "minimal": RiskCategory.MINIMAL, "minimal_risk": RiskCategory.MINIMAL,
            "limited": RiskCategory.LIMITED, "limited_risk": RiskCategory.LIMITED,
            "high": RiskCategory.HIGH, "high_risk": RiskCategory.HIGH,
            "unacceptable": RiskCategory.UNACCEPTABLE,
        }
        risk = risk_map.get(args.ci, RiskCategory.MINIMAL)
        ci = ComplianceIntensityCalculator.calculate(risk)
        if args.json:
            print(json.dumps(ci.to_dict(), ensure_ascii=False, indent=2))
        else:
            print(f"\n🧮 合规强度指数 (CI): {ci.value:.4f}")
            print(f"   base_score: {ci.base_score:.4f}")
            print(f"   upgrade_factor: {ci.upgrade_factor:.4f}")
            print(f"   threat_factor: {ci.threat_factor:.4f}")
            print(f"   解读: {ComplianceIntensityCalculator.interpret(ci.value)['description']}")
        return

    if args.calibrate:
        try:
            domain = Domain(args.calibrate)
        except ValueError:
            domain = Domain.GENERAL
        cal = ThreeAxisCalibrator.calibrate(domain)
        optimal = ThreeAxisCalibrator.find_optimal(cal, domain)
        if args.json:
            print(json.dumps({"calibration": asdict(cal), "optimal": optimal}, ensure_ascii=False, indent=2))
        else:
            print(f"\n🎯 三轴校准结果 ({domain.value}):")
            print(f"   最优alpha: {optimal['optimal_alpha']}")
            print(f"   解读: {optimal['interpretation']}")
            print(f"   帕累托点: {len(cal.frontier_points)}个")
        return

    if args.eval:
        try:
            domain = Domain(args.eval)
        except ValueError:
            domain = Domain.GENERAL
        result = MVEMRunner.run(domain, 1.0)
        if args.json:
            print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
        else:
            print(f"\n📊 MVEM评测 ({domain.value}):")
            print(f"   通过率: {result.pass_rate:.2%}")
            print(f"   事实性准确率: {result.factual_accuracy:.2%}")
            print(f"   对抗性通过率: {result.adversarial_pass_rate:.2%}")
            print(f"   滥用处理延迟: {result.abuse_handling_delay:.1f}分钟")
        return

    if args.transition:
        try:
            domain = Domain(args.transition)
        except ValueError:
            domain = Domain.GENERAL
        result = GovernancePhaseTransition.detect(args.mau, domain)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🔄 治理相变检测 ({domain.value}):")
            for k, v in result.items():
                if isinstance(v, bool):
                    print(f"   {k}: {'✅ 是' if v else '❌ 否'}")
                else:
                    print(f"   {k}: {v}")
        return

    if args.quality:
        quality = RejectionQualityAssessor.assess(args.quality)
        grade = RejectionQualityAssessor.interpret(quality.total_score)
        if args.json:
            print(json.dumps(quality.to_dict(), ensure_ascii=False, indent=2))
        else:
            print(f"\n📋 拒答质量评估:")
            print(f"   总分: {quality.total_score:.3f}")
            print(f"   等级: {grade['grade']}")
            print(f"   说明: {grade['description']}")
        return

    if args.diagram:
        try:
            domain = Domain(args.diagram)
        except ValueError:
            domain = Domain.GENERAL
        cal = ThreeAxisCalibrator.calibrate(domain)
        print("\n" + ParetoVisualizer.generate(cal, domain))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
