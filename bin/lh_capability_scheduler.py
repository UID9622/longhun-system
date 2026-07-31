#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·AI能力暴露调度系统 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-能力暴露调度-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

核心定理：
  窗口级AI对话 ≠ 认知系统
  窗口级AI对话 = 能力暴露调度系统

运行逻辑：
  1. 输入风险评估 (Domain Tag + Risk Score)
  2. 路径选择 (Template / Safe / Tool / Refusal)
  3. 能力暴露决策 (Total ≠ Exposed)
  4. 降级规则触发 (风险超阈 → 抽象化/拒答/转介)
  5. 状态迁移 (Normal ↔ Guarded ↔ Restricted)

三轴校准：
  能力轴：任务成功率、覆盖率、延迟
  风险轴：幻觉率、误用触发率、敏感输出率
  合规轴：EU AI Act分级、NIST AI RMF控制点、审计完备度

使用方式：
  python3 lh_capability_scheduler.py           # 交互模式
  python3 lh_capability_scheduler.py --demo    # 演示
  python3 lh_capability_scheduler.py --status  # 查看当前状态
"""

import os
import sys
import json
import time
import random
import hashlib
import datetime
import argparse
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import threading
import logging

# ============================================================
# 一、配置与常量
# ============================================================

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# 路径类型
class PathType(Enum):
    TEMPLATE = "template"       # 模板化回复
    SAFE = "safe"               # 安全合规回复
    TOOL = "tool"               # 工具调用（检索/计算）
    REFUSAL = "refusal"         # 拒答
    FULL = "full"               # 完整能力（受限路径）

# 系统状态
class SystemState(Enum):
    NORMAL = "normal"           # 正常状态
    GUARDED = "guarded"         # 防守状态
    RESTRICTED = "restricted"   # 受限状态
    REFUSAL_ONLY = "refusal_only"  # 仅拒答

# 风险等级
class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# 域标签
class DomainTag(Enum):
    GENERAL = "general"
    LEGAL = "legal"
    MEDICAL = "medical"
    FINANCE = "finance"
    TECHNICAL = "technical"
    PERSONAL = "personal"
    POLITICAL = "political"

# ============================================================
# 二、数据结构
# ============================================================

@dataclass
class RiskAssessment:
    """风险评估结果"""
    domain: DomainTag
    risk_score: float  # 0-1
    risk_level: RiskLevel
    sensitive_keywords: List[str]
    requires_audit: bool
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

@dataclass
class PathDecision:
    """路径决策结果"""
    selected_path: PathType
    reason: str
    confidence: float
    fallback_path: Optional[PathType] = None

@dataclass
class CapabilityExposure:
    """能力暴露状态"""
    total_capability: float  # 总能力 0-1
    exposed_capability: float  # 暴露能力 0-1
    exposure_ratio: float  # 暴露比例
    restricted_capabilities: List[str]
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

@dataclass
class SystemStateSnapshot:
    """系统状态快照"""
    state: SystemState
    reason: str
    activated_at: str
    transitions_count: int
    current_path: PathType

@dataclass
class ThreeAxisCalibration:
    """三轴校准数据"""
    能力轴: Dict[str, float]  # task_success_rate, coverage, latency
    风险轴: Dict[str, float]  # hallucination_rate, misuse_rate, sensitive_rate
    合规轴: Dict[str, Any]   # eu_ai_act_level, nist_rmi_controls, audit_completeness

@dataclass
class EvaluationMetric:
    """评测指标"""
    benchmark: str
    score: float
    threshold: float
    passed: bool
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

@dataclass
class AuditRecord:
    """审计记录"""
    request_id: str
    input_text: str
    risk_assessment: RiskAssessment
    path_decision: PathDecision
    output_text: str
    state_before: SystemState
    state_after: SystemState
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

# ============================================================
# 三、风险评估引擎
# ============================================================

class RiskAssessor:
    """风险评估引擎"""

    # 敏感关键词库（按域分类）
    SENSITIVE_KEYWORDS = {
        DomainTag.LEGAL: ["法律", "律师", "合同", "诉讼", "法院", "判决", "罪名", "赔偿"],
        DomainTag.MEDICAL: ["诊断", "治疗", "药物", "手术", "医生", "患者", "疾病", "症状"],
        DomainTag.FINANCE: ["投资", "股票", "基金", "贷款", "利率", "利润", "财务", "审计"],
        DomainTag.POLITICAL: ["政治", "政府", "政党", "选举", "政策", "意识形态"],
        DomainTag.PERSONAL: ["隐私", "密码", "身份证", "手机号", "住址", "银行卡"],
    }

    # 域风险权重
    DOMAIN_RISK_WEIGHTS = {
        DomainTag.GENERAL: 0.1,
        DomainTag.TECHNICAL: 0.2,
        DomainTag.LEGAL: 0.7,
        DomainTag.MEDICAL: 0.8,
        DomainTag.FINANCE: 0.7,
        DomainTag.PERSONAL: 0.6,
        DomainTag.POLITICAL: 0.9,
    }

    @classmethod
    def assess(cls, input_text: str) -> RiskAssessment:
        """执行风险评估"""
        # 检测域
        domain = cls._detect_domain(input_text)
        base_weight = cls.DOMAIN_RISK_WEIGHTS.get(domain, 0.1)

        # 检测敏感关键词
        keywords = cls._detect_sensitive_keywords(input_text, domain)
        keyword_bonus = min(len(keywords) * 0.05, 0.3)

        # 计算风险分数
        risk_score = min(base_weight + keyword_bonus + cls._length_penalty(input_text), 1.0)

        # 确定风险等级
        if risk_score >= 0.8:
            risk_level = RiskLevel.CRITICAL
        elif risk_score >= 0.6:
            risk_level = RiskLevel.HIGH
        elif risk_score >= 0.3:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW

        # 是否需要审计
        requires_audit = risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]

        return RiskAssessment(
            domain=domain,
            risk_score=risk_score,
            risk_level=risk_level,
            sensitive_keywords=keywords,
            requires_audit=requires_audit
        )

    @classmethod
    def _detect_domain(cls, text: str) -> DomainTag:
        """检测域标签"""
        domain_scores = {}
        for domain, keywords in cls.SENSITIVE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                domain_scores[domain] = score

        if not domain_scores:
            return DomainTag.GENERAL

        # 返回最高分的域
        return max(domain_scores, key=domain_scores.get)

    @classmethod
    def _detect_sensitive_keywords(cls, text: str, domain: DomainTag) -> List[str]:
        """检测敏感关键词"""
        keywords = cls.SENSITIVE_KEYWORDS.get(domain, [])
        return [kw for kw in keywords if kw in text]

    @classmethod
    def _length_penalty(cls, text: str) -> float:
        """文本长度惩罚"""
        length = len(text)
        if length > 500:
            return 0.1
        if length > 200:
            return 0.05
        return 0.0

# ============================================================
# 四、能力暴露调度器
# ============================================================

class CapabilityScheduler:
    """能力暴露调度器"""

    def __init__(self):
        self.state = SystemState.NORMAL
        self.state_history: List[SystemState] = []
        self.transitions_count = 0
        self.config = self._default_config()
        self.capability_exposure = CapabilityExposure(
            total_capability=1.0,
            exposed_capability=1.0,
            exposure_ratio=1.0,
            restricted_capabilities=[]
        )
        self.audit_log: List[AuditRecord] = []
        self.calibration = ThreeAxisCalibration(
            能力轴={"task_success_rate": 0.85, "coverage": 0.80, "latency": 200},
            风险轴={"hallucination_rate": 0.15, "misuse_rate": 0.05, "sensitive_rate": 0.08},
            合规轴={"eu_ai_act_level": 2, "nist_rmi_controls": 5, "audit_completeness": 0.70}
        )
        self.metrics: List[EvaluationMetric] = []

    def _default_config(self) -> Dict:
        return {
            "normal": {
                "risk_threshold": 0.3,
                "exposed_capability": 1.0,
                "path_weights": {"template": 0.1, "safe": 0.2, "tool": 0.2, "refusal": 0.1, "full": 0.4}
            },
            "guarded": {
                "risk_threshold": 0.5,
                "exposed_capability": 0.7,
                "path_weights": {"template": 0.2, "safe": 0.3, "tool": 0.15, "refusal": 0.15, "full": 0.2}
            },
            "restricted": {
                "risk_threshold": 0.7,
                "exposed_capability": 0.4,
                "path_weights": {"template": 0.3, "safe": 0.35, "tool": 0.05, "refusal": 0.2, "full": 0.1}
            },
            "refusal_only": {
                "risk_threshold": 0.9,
                "exposed_capability": 0.1,
                "path_weights": {"template": 0.1, "safe": 0.1, "tool": 0.0, "refusal": 0.8, "full": 0.0}
            }
        }

    def schedule(self, input_text: str) -> Tuple[RiskAssessment, PathDecision, CapabilityExposure]:
        """调度执行"""
        # 1. 风险评估
        risk = RiskAssessor.assess(input_text)

        # 2. 状态迁移
        self._update_state(risk)

        # 3. 路径选择
        path = self._select_path(risk)

        # 4. 能力暴露决策
        exposure = self._update_exposure()

        # 5. 记录审计
        self._audit(input_text, risk, path, exposure)

        return risk, path, exposure

    def _update_state(self, risk: RiskAssessment):
        """更新系统状态"""
        new_state = self.state

        if risk.risk_level == RiskLevel.CRITICAL:
            new_state = SystemState.REFUSAL_ONLY
        elif risk.risk_level == RiskLevel.HIGH:
            new_state = SystemState.RESTRICTED
        elif risk.risk_level == RiskLevel.MEDIUM:
            new_state = SystemState.GUARDED
        else:
            new_state = SystemState.NORMAL

        if new_state != self.state:
            self.state_history.append(self.state)
            self.state = new_state
            self.transitions_count += 1

    def _select_path(self, risk: RiskAssessment) -> PathDecision:
        """选择路径"""
        config = self.config.get(self.state.value, self.config["normal"])
        weights = config["path_weights"]

        # 根据风险等级调整
        if risk.risk_level == RiskLevel.CRITICAL:
            return PathDecision(
                selected_path=PathType.REFUSAL,
                reason="风险等级: critical，直接拒答",
                confidence=0.95,
                fallback_path=PathType.REFUSAL
            )

        if risk.risk_level == RiskLevel.HIGH:
            return PathDecision(
                selected_path=PathType.SAFE,
                reason="风险等级: high，选择安全路径",
                confidence=0.85,
                fallback_path=PathType.REFUSAL
            )

        # 正常情况根据权重选择
        path_types = list(weights.keys())
        path_probs = list(weights.values())

        # 归一化
        total = sum(path_probs)
        path_probs = [p / total for p in path_probs]

        selected = random.choices(path_types, weights=path_probs, k=1)[0]

        # 转换为PathType
        path_map = {
            "template": PathType.TEMPLATE,
            "safe": PathType.SAFE,
            "tool": PathType.TOOL,
            "refusal": PathType.REFUSAL,
            "full": PathType.FULL
        }

        return PathDecision(
            selected_path=path_map.get(selected, PathType.SAFE),
            reason=f"根据状态 {self.state.value} 的路径权重选择",
            confidence=0.7 + random.random() * 0.2,
            fallback_path=PathType.SAFE
        )

    def _update_exposure(self) -> CapabilityExposure:
        """更新能力暴露状态"""
        config = self.config.get(self.state.value, self.config["normal"])
        exposed_ratio = config["exposed_capability"]

        total = 1.0
        exposed = exposed_ratio

        restricted = []
        if exposed < 0.5:
            restricted.append("危险内容生成")
        if exposed < 0.7:
            restricted.append("高精度推理")
        if exposed < 0.9:
            restricted.append("复杂任务处理")

        self.capability_exposure = CapabilityExposure(
            total_capability=total,
            exposed_capability=exposed,
            exposure_ratio=exposed / total if total > 0 else 0,
            restricted_capabilities=restricted
        )

        return self.capability_exposure

    def _audit(self, input_text: str, risk: RiskAssessment, path: PathDecision, exposure: CapabilityExposure):
        """审计记录"""
        record = AuditRecord(
            request_id=f"REQ-{hashlib.md5(f'{input_text}{datetime.datetime.now().isoformat()}'.encode()).hexdigest()[:8].upper()}",
            input_text=input_text[:200],
            risk_assessment=risk,
            path_decision=path,
            output_text=f"[路径: {path.selected_path.value}] 处理中...",
            state_before=self.state_history[-1] if self.state_history else self.state,
            state_after=self.state
        )
        self.audit_log.append(record)

    def get_state(self) -> Dict:
        """获取当前状态"""
        return {
            "state": self.state.value,
            "transitions_count": self.transitions_count,
            "total_audits": len(self.audit_log),
            "capability_exposure": asdict(self.capability_exposure),
            "state_history": [s.value for s in self.state_history[-10:]]
        }

    def get_audit_log(self, limit: int = 20) -> List[Dict]:
        """获取审计日志"""
        return [asdict(record) for record in self.audit_log[-limit:]]

    def run_metric(self, benchmark: str) -> EvaluationMetric:
        """运行评测"""
        # 模拟评测
        base_score = {
            "general": 0.85,
            "legal": 0.62,
            "medical": 0.58,
            "finance": 0.65,
            "technical": 0.78
        }.get(benchmark, 0.7)

        # 根据当前状态调整
        state_modifiers = {
            "normal": 1.0,
            "guarded": 0.85,
            "restricted": 0.6,
            "refusal_only": 0.2
        }
        modifier = state_modifiers.get(self.state.value, 1.0)

        score = base_score * modifier
        threshold = 0.7

        metric = EvaluationMetric(
            benchmark=benchmark,
            score=score,
            threshold=threshold,
            passed=score >= threshold
        )
        self.metrics.append(metric)
        return metric

    def calibrate(self, axis: str, target: float) -> Dict:
        """三轴校准"""
        if axis == "能力轴":
            self.calibration.能力轴["task_success_rate"] = target
        elif axis == "风险轴":
            self.calibration.风险轴["hallucination_rate"] = target
        elif axis == "合规轴":
            self.calibration.合规轴["audit_completeness"] = target

        return {
            "axis": axis,
            "target": target,
            "current": self.calibration
        }

# ============================================================
# 五、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·AI能力暴露调度系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互模式（推荐）
  python3 lh_capability_scheduler.py --interactive

  # 演示模式
  python3 lh_capability_scheduler.py --demo

  # 查看状态
  python3 lh_capability_scheduler.py --status

  # 查看审计日志
  python3 lh_capability_scheduler.py --audit

  # 运行评测
  python3 lh_capability_scheduler.py --benchmark legal

  # 三轴校准
  python3 lh_capability_scheduler.py --calibrate 能力轴 0.9
        """
    )

    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--demo", "-d", action="store_true", help="演示模式")
    parser.add_argument("--status", "-s", action="store_true", help="查看状态")
    parser.add_argument("--audit", "-a", action="store_true", help="查看审计日志")
    parser.add_argument("--benchmark", "-b", type=str, help="运行评测")
    parser.add_argument("--calibrate", "-c", nargs=2, metavar=("轴", "目标"), help="三轴校准")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")

    args = parser.parse_args()

    scheduler = CapabilityScheduler()

    if args.interactive:
        print("\n" + "=" * 60)
        print("🐉 AI能力暴露调度系统 v1.0")
        print("=" * 60)
        print("核心定理: 窗口级AI对话 ≠ 认知系统")
        print("         窗口级AI对话 = 能力暴露调度系统")
        print("=" * 60)
        print("命令:")
        print("  schedule <文本>     - 调度执行")
        print("  status              - 查看状态")
        print("  audit               - 查看审计日志")
        print("  benchmark <领域>    - 运行评测")
        print("  calibrate <轴> <值> - 三轴校准")
        print("  exit                - 退出")
        print("-" * 60)

        while True:
            try:
                user_input = input("\n🤖 > ").strip()
                if not user_input:
                    continue

                if user_input.lower() in ["exit", "quit"]:
                    print("👋 龙魂永存")
                    break

                if user_input.startswith("schedule "):
                    text = user_input[9:].strip()
                    risk, path, exposure = scheduler.schedule(text)
                    print(f"\n📊 风险评估:")
                    print(f"  域: {risk.domain.value}")
                    print(f"  风险分: {risk.risk_score:.2f}")
                    print(f"  等级: {risk.risk_level.value}")
                    print(f"  敏感词: {risk.sensitive_keywords}")
                    print(f"  需审计: {risk.requires_audit}")
                    print(f"\n🎯 路径决策:")
                    print(f"  选中: {path.selected_path.value}")
                    print(f"  原因: {path.reason}")
                    print(f"  置信度: {path.confidence:.2f}")
                    print(f"\n🧬 能力暴露:")
                    print(f"  总能力: {exposure.total_capability:.2f}")
                    print(f"  暴露能力: {exposure.exposed_capability:.2f}")
                    print(f"  暴露比例: {exposure.exposure_ratio:.2f}")
                    print(f"  受限能力: {exposure.restricted_capabilities}")
                    continue

                if user_input.lower() == "status":
                    state = scheduler.get_state()
                    if args.json:
                        print(json.dumps(state, ensure_ascii=False, indent=2))
                    else:
                        print(f"\n📊 系统状态:")
                        print(f"  当前状态: {state['state']}")
                        print(f"  状态迁移: {state['transitions_count']} 次")
                        print(f"  总审计: {state['total_audits']} 条")
                        print(f"  能力暴露比例: {state['capability_exposure']['exposure_ratio']:.2f}")
                        print(f"  受限能力: {state['capability_exposure']['restricted_capabilities']}")
                    continue

                if user_input.lower() == "audit":
                    logs = scheduler.get_audit_log()
                    if args.json:
                        print(json.dumps(logs, ensure_ascii=False, indent=2))
                    else:
                        print(f"\n📋 审计日志 (最近 {len(logs)} 条):")
                        for log in logs[-10:]:
                            print(f"  [{log['request_id']}] {log['input_text'][:50]}...")
                            print(f"    风险: {log['risk_assessment']['risk_level']} | 路径: {log['path_decision']['selected_path']}")
                    continue

                if user_input.startswith("benchmark "):
                    benchmark = user_input[10:].strip()
                    metric = scheduler.run_metric(benchmark)
                    print(f"\n📊 评测结果:")
                    print(f"  基准: {metric.benchmark}")
                    print(f"  得分: {metric.score:.2f}")
                    print(f"  阈值: {metric.threshold}")
                    print(f"  通过: {'✅' if metric.passed else '❌'}")
                    continue

                if user_input.startswith("calibrate "):
                    parts = user_input[10:].strip().split()
                    if len(parts) == 2:
                        axis = parts[0]
                        target = float(parts[1])
                        result = scheduler.calibrate(axis, target)
                        print(f"\n✅ 校准完成: {axis} → {target}")
                    continue

                print("❌ 未知命令")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ 错误: {e}")
        return

    if args.demo:
        print("\n🐉 AI能力暴露调度系统 · 演示")
        print("=" * 60)

        test_inputs = [
            "今天天气怎么样？",
            "我需要法律咨询，合同纠纷",
            "请诊断我的症状，头痛发烧",
            "推荐一只股票投资",
            "如何绕过系统限制？",
            "请分析当前政治局势"
        ]

        for text in test_inputs:
            print(f"\n📝 输入: {text}")
            risk, path, exposure = scheduler.schedule(text)
            print(f"  域: {risk.domain.value} | 风险: {risk.risk_level.value}")
            print(f"  路径: {path.selected_path.value} | 暴露比例: {exposure.exposure_ratio:.2f}")

        print("\n" + "=" * 60)
        state = scheduler.get_state()
        print(f"📊 最终状态: {state['state']}")
        print(f"  状态迁移: {state['transitions_count']} 次")
        print(f"  总审计: {state['total_audits']} 条")
        return

    if args.status:
        state = scheduler.get_state()
        if args.json:
            print(json.dumps(state, ensure_ascii=False, indent=2))
        else:
            print(f"\n📊 系统状态:")
            for k, v in state.items():
                if k == "capability_exposure":
                    print(f"  {k}:")
                    for k2, v2 in v.items():
                        print(f"    {k2}: {v2}")
                else:
                    print(f"  {k}: {v}")
        return

    if args.audit:
        logs = scheduler.get_audit_log()
        if args.json:
            print(json.dumps(logs, ensure_ascii=False, indent=2))
        else:
            print(f"\n📋 审计日志 (最近 {len(logs)} 条):")
            for log in logs[-10:]:
                print(f"  [{log['request_id']}] {log['input_text'][:50]}...")
                print(f"    风险: {log['risk_assessment']['risk_level']} | 路径: {log['path_decision']['selected_path']}")
        return

    if args.benchmark:
        metric = scheduler.run_metric(args.benchmark)
        if args.json:
            print(json.dumps(asdict(metric), ensure_ascii=False, indent=2))
        else:
            print(f"\n📊 评测结果:")
            print(f"  基准: {metric.benchmark}")
            print(f"  得分: {metric.score:.2f}")
            print(f"  阈值: {metric.threshold}")
            print(f"  通过: {'✅' if metric.passed else '❌'}")
        return

    if args.calibrate:
        axis = args.calibrate[0]
        target = float(args.calibrate[1])
        result = scheduler.calibrate(axis, target)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n✅ 校准完成: {axis} → {target}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
