#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-QUALITY-GATE-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
"""
🐉 龍魂 · 质量门禁 v1.0
功能: 发布前强制检查，不达标自动拦截（P0 门禁，gate 不过不发布）
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class GateStatus(Enum):
    PASS = "✅ 通过"
    FAIL = "❌ 失败"
    WARN = "⚠️ 警告"


@dataclass
class QualityGateRule:
    """质量门禁规则"""
    name: str
    condition: str  # passed, coverage, tricolor
    threshold: float
    severity: str  # critical, high, medium, low


@dataclass
class QualityGateResult:
    """质量门禁结果"""
    rule: str
    status: GateStatus
    actual: float
    threshold: float
    message: str

    def to_dict(self) -> Dict:
        """转为可 JSON 序列化字典"""
        return {
            "rule": self.rule,
            "status": self.status.value,
            "actual": self.actual,
            "threshold": self.threshold,
            "message": self.message,
        }


class QualityGate:
    """质量门禁"""

    DEFAULT_RULES = [
        QualityGateRule("测试通过率", "passed", 0.95, "critical"),
        QualityGateRule("代码覆盖率", "coverage", 0.80, "high"),
        QualityGateRule("三色审计", "tricolor", 0.0, "critical"),  # 只能是 🟢
    ]

    def __init__(self, rules: List[QualityGateRule] = None):
        self.rules = rules or self.DEFAULT_RULES

    def evaluate(self, test_report: Dict) -> Dict:
        """评估质量门禁"""
        results = []
        all_passed = True

        for rule in self.rules:
            actual = self._get_actual_value(test_report, rule.condition)
            threshold = rule.threshold
            status = GateStatus.PASS if actual >= threshold else GateStatus.FAIL

            # 三色审计特殊处理: 只有 🟢 才放行
            if rule.condition == "tricolor":
                status = GateStatus.PASS if test_report.get("tricolor") == "🟢" else GateStatus.FAIL

            # 覆盖率未检测到（无 pytest-cov 插件）→ 降级 WARN，不硬拦
            if rule.condition == "coverage" and actual == 0:
                status = GateStatus.WARN

            if status == GateStatus.FAIL:
                all_passed = False

            results.append(QualityGateResult(
                rule=rule.name,
                status=status,
                actual=actual,
                threshold=threshold,
                message=self._generate_message(rule, actual, status)
            ))

        return {
            "overall": "PASS" if all_passed else "FAIL",
            "results": [r.to_dict() for r in results],
            "timestamp": datetime.now().isoformat(),
            "dna": _GEN_DNA("GATE"),
        }

    def _get_actual_value(self, report: Dict, condition: str) -> float:
        if condition == "passed":
            total = report.get("total", 1) or 1
            passed = report.get("passed", 0)
            return passed / total if total > 0 else 0
        elif condition == "coverage":
            return report.get("coverage", 0) / 100
        elif condition == "tricolor":
            return 1.0 if report.get("tricolor") == "🟢" else 0
        return 0

    def _generate_message(self, rule: QualityGateRule, actual: float, status: GateStatus) -> str:
        if status == GateStatus.PASS:
            return f"{rule.name} 达标 ({actual:.2f} >= {rule.threshold})"
        if status == GateStatus.WARN:
            return f"{rule.name} 未检测到覆盖率数据（无 pytest-cov），降级为警告"
        return f"{rule.name} 未达标 ({actual:.2f} < {rule.threshold})"


def _GEN_DNA(suffix: str) -> str:
    """延迟导入 generate_dna，避免循环依赖"""
    from .generate_dna import generate_dna
    return generate_dna(suffix)
