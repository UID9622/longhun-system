#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂三色审计引擎 v1.0
DNA: #龍芯⚡️2026-08-25-TRICOLOR-AUDIT-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
五维评分：安全漏洞(30) + 归属主权(25) + 运行状态(20) + 数据完整性(15) + 合规性(10)
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any


class 三色(Enum):
    绿 = "🟢"
    黄 = "🟡"
    红 = "🔴"


@dataclass
class 审计结果:
    等级: 三色
    分数: int
    问题列表: List[str]
    建议措施: List[str]
    是否阻断: bool
    详细数据: Dict[str, Any] = field(default_factory=dict)


class TricolorAudit:
    def __init__(self):
        self.审计规则 = {
            "安全漏洞":   {"权重": 30, "红线阈值": 1},
            "归属主权":   {"权重": 25, "红线阈值": 1},
            "运行状态":   {"权重": 20, "红线阈值": 3},
            "数据完整性": {"权重": 15, "红线阈值": 1},
            "合规性":     {"权重": 10, "红线阈值": 2},
        }

    def audit(self, target_data: Dict[str, Any]) -> 审计结果:
        问题列表: List[str] = []
        建议措施: List[str] = []
        红线触发 = False

        安全问题  = target_data.get("安全问题", [])
        异常次数  = target_data.get("异常次数", 0)
        dna_valid = target_data.get("dna_valid", True)
        配置完整  = target_data.get("配置完整", True)

        # 安全漏洞维度
        if len(安全问题) >= self.审计规则["安全漏洞"]["红线阈值"]:
            红线触发 = True
            问题列表.append(f"🔴 安全红线：发现 {len(安全问题)} 个漏洞")
            建议措施.append("立即修复或触发死门熔断")
        elif 安全问题:
            问题列表.append(f"🟡 安全警告：发现 {len(安全问题)} 个潜在风险")

        # 归属主权维度
        if not dna_valid:
            红线触发 = True
            问题列表.append("🔴 归属红线：DNA链验证失败")
            建议措施.append("立即追溯DNA链，执行 verify_chain()")

        # 运行状态维度
        if 异常次数 >= self.审计规则["运行状态"]["红线阈值"]:
            问题列表.append(f"🟡 运行警告：异常 {异常次数} 次（阈值3次）")
            建议措施.append("检查服务日志，考虑触发杜门隔离")

        # 数据完整性维度
        if not 配置完整:
            问题列表.append("🟡 数据警告：配置不完整")
            建议措施.append("检查 doorkeeper_config.yml")

        # 评分计算
        base_score = 100
        for 问题 in 问题列表:
            if 问题.startswith("🔴"):
                base_score -= 30
            elif 问题.startswith("🟡"):
                base_score -= 10
        分数 = max(0, base_score)

        if 红线触发 or 分数 < 60:
            return 审计结果(三色.红, 分数, 问题列表, 建议措施, True, target_data)
        elif 分数 < 80:
            return 审计结果(三色.黄, 分数, 问题列表, 建议措施, False, target_data)
        else:
            return 审计结果(三色.绿, 分数, 问题列表, 建议措施, False, target_data)

    def quick_audit(self, service_name: str, port_alive: bool, error_count: int) -> 三色:
        """快速审计（用于心跳检测中的轻量评估）"""
        if not port_alive or error_count > 5:
            return 三色.红
        elif error_count > 2:
            return 三色.黄
        return 三色.绿


# 全局审计引擎单例
audit_engine = TricolorAudit()
