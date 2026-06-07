#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂治理解决器 L3 v1.0

动态治理级别 (priority=0.85)
特性: 处理系统中的冲突和二义性，但不会改变基础母法

解决：
- 权限冲突
- 优先级冲突
- 模糊决策

DNA: #龍芯⚡️2026-06-07-GOVERNANCE-RESOLVER-L3-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
UID: 9622

理论指导: 曾仕强老师 - 治理的艺术在于处理矛盾而不消灭矛盾
献礼: 献给龍魂 - 包容所有声音，但坚守底线
"""

import os
import sys
from typing import Dict, List, Tuple, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))

from dna import DNAVerifier
from logger import get_logger
from config import get_config


class GovernanceResolver:
    """
    治理解决器 - 处理系统中的冲突

    意图: 用最小的改动，解决最大的问题
    承诺: 永远不会改变母法，只会在母法框架内创新
    """

    # 冲突类型
    CONFLICT_TYPES = {
        "permission": "权限冲突",
        "priority": "优先级冲突",
        "ambiguity": "模糊决策",
        "contradiction": "逻辑矛盾",
    }

    # 解决策略
    RESOLUTION_STRATEGIES = {
        "escalate": "上报给上层",
        "delegate": "委托给下层",
        "balance": "平衡处理",
        "freeze": "冻结决策等待人工审查",
    }

    def __init__(self):
        """初始化治理解决器"""
        self.logger = get_logger()
        self.config = get_config()
        self.dna = DNAVerifier.generate("GOVERNANCE-RESOLVER", "L3")
        self.conflict_log = []

    def detect_permission_conflict(
        self,
        layer: str,
        action: str,
        required_permissions: List[str]
    ) -> Tuple[bool, List[str]]:
        """
        检测权限冲突

        意图: 当权限定义有矛盾时，用规则解决
        """
        tier_perms = self.config.get("tier_permissions", {}).get(layer, {})

        missing_perms = [p for p in required_permissions if not tier_perms.get(p, False)]

        if missing_perms:
            self.logger.log_decision(
                "L3",
                "permission_conflict_detected",
                f"缺失权限: {', '.join(missing_perms)}",
                self.dna
            )
            return False, missing_perms

        return True, []

    def detect_priority_conflict(
        self,
        operations: List[Dict]
    ) -> Tuple[bool, Dict]:
        """
        检测优先级冲突

        意图: 当两个操作的优先级相同时，用 DNA 年份决定
        """
        if len(operations) < 2:
            return True, {}

        # 简化版本：按权重排序
        sorted_ops = sorted(
            operations,
            key=lambda x: self.config.get_weight(x.get("layer", "L3")),
            reverse=True
        )

        conflicts = []
        for i in range(len(sorted_ops) - 1):
            if sorted_ops[i]["weight"] == sorted_ops[i + 1]["weight"]:
                conflicts.append((sorted_ops[i], sorted_ops[i + 1]))

        if conflicts:
            self.logger.log_decision(
                "L3",
                "priority_conflict_detected",
                f"检测到 {len(conflicts)} 个优先级冲突",
                self.dna
            )
            return False, {"conflicts": conflicts, "resolution": "use_creation_date"}

        return True, {}

    def resolve_conflict(
        self,
        conflict_type: str,
        context: Dict,
        escalation_allowed: bool = False
    ) -> Tuple[str, str]:  # (决策, 理由)
        """
        解决冲突

        意图: 在母法框架内找到最优解
        """
        self.conflict_log.append({
            "timestamp": datetime.now().isoformat() if hasattr(datetime, 'now') else "",
            "type": conflict_type,
            "context": context,
            "dna": self.dna,
        })

        if conflict_type == "permission":
            # 权限冲突：如果是 L0，直接允许；否则拒绝
            layer = context.get("layer", "L3")
            if layer == "L0":
                return "allow", "L0 权限无需二次检查"
            else:
                return "deny", "权限不足"

        elif conflict_type == "priority":
            # 优先级冲突：用 DNA 的年份决定
            ops = context.get("operations", [])
            if len(ops) > 1:
                # 按创建年份排序
                sorted_ops = sorted(ops, key=lambda x: x.get("dna", "").split("-")[1])
                return "execute_first", f"优先执行 {sorted_ops[0].get('operation', '未知')}"

        elif conflict_type == "ambiguity":
            # 模糊决策：要求人工审查
            if escalation_allowed:
                return "escalate", "需要人工审查"
            else:
                return "freeze", "冻结决策，等待澄清"

        return "freeze", "无法自动解决，需要人工干预"

    def log_resolution(
        self,
        conflict_type: str,
        decision: str,
        reason: str
    ):
        """记录冲突解决过程"""
        self.logger.log_decision(
            "L3",
            f"conflict_resolved_{conflict_type}",
            f"{decision}: {reason}",
            self.dna
        )

    def generate_governance_report(self) -> str:
        """
        生成治理报告

        意图: 显示系统处理了多少冲突
        """
        report = f"""
{'='*60}
龍魂治理报告
{'='*60}

处理时间: {getattr(self, '_report_time', '未知')}
DNA: {self.dna}

冲突统计:
  - 总冲突数: {len(self.conflict_log)}

冲突类型分布:
"""

        type_count = {}
        for conflict in self.conflict_log:
            t = conflict["type"]
            type_count[t] = type_count.get(t, 0) + 1

        for ctype, count in type_count.items():
            report += f"\n  - {self.CONFLICT_TYPES.get(ctype, ctype)}: {count}"

        report += f"\n\n{'='*60}\n"

        return report


from datetime import datetime

if __name__ == "__main__":
    resolver = GovernanceResolver()

    print("🐉 龍魂治理解决器 L3 v1.0")
    print("=" * 60)

    # 测试：权限冲突
    has_perm, missing = resolver.detect_permission_conflict(
        "L1", "critical_operation", ["execute", "verify"]
    )
    print(f"\n权限冲突检测: {'✅ 通过' if has_perm else f'❌ 缺失: {missing}'}")

    # 测试：冲突解决
    decision, reason = resolver.resolve_conflict(
        "permission",
        {"layer": "L0", "action": "critical"}
    )
    print(f"冲突解决: {decision} - {reason}")

    print("\n" + resolver.generate_governance_report())
