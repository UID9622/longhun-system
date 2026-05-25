#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·Web3-DNA 64卦审计算法 v1.0
64-Gua Audit Algorithm: 8-Dimensional Risk Assessment

DNA: #龍芯⚡️2026-05-25-WEB3-DNA-64GUA-AUDIT-v1.0
UID: 9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

基于易经64卦的8维度审计体系：
1. 创新度 (Innovation) - 是否引入新的可能性
2. 支持度 (Support) - 生态支持力度
3. 响应度 (Responsiveness) - 对市场反馈的快速响应
4. 渗透度 (Penetration) - 风险渗透程度
5. 风控度 (Risk Control) - 风险控制力度
6. 传播度 (Dissemination) - 信息传播范围与速度
7. 防御度 (Defense) - 防守机制的完整性
8. 协作度 (Collaboration) - 与其他系统的协作能力

每个维度 0-100 分，最终汇总到一个"卦象"
8维度组合 = 256 种可能的卦象配置
三维投影到八卦（乾坤艮兑震巽坎离）

本地计算·永不外送·纯数学·零ML依赖

理论指导: 曾仕强老师（永恒显示）
献礼: 龍魂系统·永恒守护·中华文化传承
"""

import hashlib
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import math


# ════════════════════════════════════════════════════════
# 第一步：八卦与64卦定义
# ════════════════════════════════════════════════════════

class BaGua(Enum):
    """八卦"""
    QIAN = "乾"  # 天
    KUN = "坤"   # 地
    GEN = "艮"   # 山
    DUI = "兑"   # 泽
    ZHEN = "震"  # 雷
    XUN = "巽"   # 风
    KAN = "坎"   # 水
    LI = "离"    # 火


@dataclass
class AuditDimension:
    """审计维度（8个）"""
    name: str              # 维度名称
    code: str              # 维度代码：I/S/R/P/RC/D/DF/C
    value: int             # 0-100
    weight: float          # 权重（总和=1.0）
    description: str       # 描述

    def __repr__(self):
        return f"{self.name}({self.code}): {self.value}/100"


@dataclass
class GuaAuditResult:
    """64卦审计结果"""
    gua_name: str                           # 卦名（如"天火同人"）
    gua_hex: str                            # 卦象（6条线）
    primary_bagua: BaGua                    # 主卦（上）
    secondary_bagua: BaGua                  # 副卦（下）
    dimensions: Dict[str, AuditDimension]  # 8维度
    overall_score: float                    # 总体审计分数 0-100
    risk_level: str                         # 风险等级：LOW/MEDIUM/HIGH/CRITICAL
    dna: str                                # 追溯码
    timestamp: str                          # 时间戳
    audit_items: List[str] = field(default_factory=list)  # 审计项目清单

    def dimension_summary(self) -> Dict[str, int]:
        """维度摘要"""
        return {name: dim.value for name, dim in self.dimensions.items()}


# ════════════════════════════════════════════════════════
# 第二步：8维度评分引擎
# ════════════════════════════════════════════════════════

class Gua64AuditEngine:
    """64卦审计引擎"""

    # 八卦对应的属性（用于维度到卦象的映射）
    BAGUA_MAP = {
        BaGua.QIAN: {"name": "天", "direction": "上", "element": "金"},
        BaGua.KUN: {"name": "地", "direction": "下", "element": "土"},
        BaGua.GEN: {"name": "山", "direction": "北东", "element": "土"},
        BaGua.DUI: {"name": "泽", "direction": "西", "element": "金"},
        BaGua.ZHEN: {"name": "雷", "direction": "东", "element": "木"},
        BaGua.XUN: {"name": "风", "direction": "东南", "element": "木"},
        BaGua.KAN: {"name": "水", "direction": "北", "element": "水"},
        BaGua.LI: {"name": "火", "direction": "南", "element": "火"},
    }

    # 卦名映射（64卦简化版，取常用的）
    GUAS = {
        "乾为天": (BaGua.QIAN, BaGua.QIAN),
        "坤为地": (BaGua.KUN, BaGua.KUN),
        "天火同人": (BaGua.QIAN, BaGua.LI),
        "风雷益": (BaGua.XUN, BaGua.ZHEN),
        "雷风恒": (BaGua.ZHEN, BaGua.XUN),
        "水火既济": (BaGua.KAN, BaGua.LI),
        "火水未济": (BaGua.LI, BaGua.KAN),
    }

    def __init__(self):
        self.audit_history: List[GuaAuditResult] = []

    @staticmethod
    def calculate_digital_root(text: str) -> int:
        """计算数字根"""
        total = sum(ord(c) for c in text)
        while total >= 10:
            total = sum(int(d) for d in str(total))
        return total if total > 0 else 9

    @staticmethod
    def score_dimension(
        dimension_name: str,
        base_score: float,
        context_factor: float = 1.0
    ) -> int:
        """
        评分单个维度
        base_score: 基础分数（0-100）
        context_factor: 上下文因子（调整系数）
        """
        final_score = base_score * context_factor
        return max(0, min(100, int(final_score)))

    def audit_transaction(
        self,
        transaction_data: Dict[str, Any],
        context_data: Dict[str, Any] = None
    ) -> GuaAuditResult:
        """
        审计一笔交易的8个维度
        """
        # 获取交易的关键信息
        tx_id = transaction_data.get("tx_id", "unknown")
        tx_amount = transaction_data.get("amount", 0)
        tx_type = transaction_data.get("type", "unknown")

        # 计算上下文因子
        context_factor = 1.0
        if context_data:
            risk_level_context = context_data.get("risk_level", "medium")
            context_factor = {"low": 0.8, "medium": 1.0, "high": 1.2}.get(risk_level_context, 1.0)

        # 1. 创新度 (Innovation) - 交易是否涉及新的资产类型或机制
        innovation_score = self.score_dimension(
            "Innovation",
            50 + (hash(tx_type) % 30),  # 基于tx_type的哈希值
            context_factor
        )

        # 2. 支持度 (Support) - 生态中对该交易类型的支持程度
        support_score = self.score_dimension(
            "Support",
            70 if tx_type in ["payment", "transfer"] else 50,
            context_factor
        )

        # 3. 响应度 (Responsiveness) - 系统对该交易的快速处理能力
        responsiveness_score = self.score_dimension(
            "Responsiveness",
            75,  # 系统默认快速响应
            context_factor
        )

        # 4. 渗透度 (Penetration) - 该交易对风险的渗透程度（低于50%为好）
        penetration_score = self.score_dimension(
            "Penetration",
            20 if tx_amount < 10000 else 60,  # 大额交易风险更高
            context_factor
        )

        # 5. 风控度 (Risk Control) - 风险控制机制的完整性
        risk_control_score = self.score_dimension(
            "Risk Control",
            80,  # 内置风控机制强度
            context_factor
        )

        # 6. 传播度 (Dissemination) - 信息传播范围
        dissemination_score = self.score_dimension(
            "Dissemination",
            40,  # 区块链原生的广播特性
            context_factor
        )

        # 7. 防御度 (Defense) - 防守机制的完整性
        defense_score = self.score_dimension(
            "Defense",
            85,  # 多层签名、时间锁等防守机制
            context_factor
        )

        # 8. 协作度 (Collaboration) - 与其他系统的协作能力
        collaboration_score = self.score_dimension(
            "Collaboration",
            60,  # 跨链/跨平台的兼容性
            context_factor
        )

        # 创建维度对象
        dimensions = {
            "Innovation": AuditDimension("创新度", "I", innovation_score, 0.125, "新颖性与创新"),
            "Support": AuditDimension("支持度", "S", support_score, 0.125, "生态支持力度"),
            "Responsiveness": AuditDimension("响应度", "R", responsiveness_score, 0.125, "快速响应能力"),
            "Penetration": AuditDimension("渗透度", "P", penetration_score, 0.125, "风险渗透程度"),
            "Risk_Control": AuditDimension("风控度", "RC", risk_control_score, 0.125, "风险控制力度"),
            "Dissemination": AuditDimension("传播度", "D", dissemination_score, 0.125, "信息传播范围"),
            "Defense": AuditDimension("防御度", "DF", defense_score, 0.125, "防守机制完整性"),
            "Collaboration": AuditDimension("协作度", "C", collaboration_score, 0.125, "协作互操作能力"),
        }

        # 计算总体评分（8维度的加权平均，权重都是0.125）
        overall_score = sum(dim.value * dim.weight for dim in dimensions.values())

        # 判定风险等级
        if overall_score >= 80:
            risk_level = "LOW"
        elif overall_score >= 60:
            risk_level = "MEDIUM"
        elif overall_score >= 40:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"

        # 映射到八卦（简化版：取score高低映射）
        if overall_score >= 75:
            primary = BaGua.QIAN  # 乾为天
            secondary = BaGua.QIAN
            gua_name = "乾为天"
        elif overall_score >= 60:
            primary = BaGua.LI    # 离为火
            secondary = BaGua.ZHEN  # 雷
            gua_name = "火雷噬嗑"
        elif overall_score >= 40:
            primary = BaGua.KAN   # 坎为水
            secondary = BaGua.LI
            gua_name = "水火既济"
        else:
            primary = BaGua.KUN   # 坤为地
            secondary = BaGua.KUN
            gua_name = "坤为地"

        # 生成卦象（6条线的二进制表示）
        gua_hex = format(int(overall_score) % 64, '06b')  # 64卦周期

        # 生成DNA
        dna_hash = hashlib.sha256(
            f"{tx_id}{overall_score}{gua_name}".encode()
        ).hexdigest()[:8]
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d-%H:%M')}-64GUA-AUDIT-{dna_hash}"

        result = GuaAuditResult(
            gua_name=gua_name,
            gua_hex=gua_hex,
            primary_bagua=primary,
            secondary_bagua=secondary,
            dimensions=dimensions,
            overall_score=round(overall_score, 2),
            risk_level=risk_level,
            dna=dna,
            timestamp=datetime.now().isoformat(),
            audit_items=[
                f"交易ID: {tx_id}",
                f"交易类型: {tx_type}",
                f"交易金额: {tx_amount}",
                f"总体审计分数: {overall_score:.2f}/100",
                f"风险等级: {risk_level}",
                f"卦象: {gua_name} ({gua_hex})",
            ]
        )

        self.audit_history.append(result)
        return result

    def export_audit_report(self, result: GuaAuditResult) -> str:
        """导出审计报告为Markdown"""
        report = f"# 📊 64卦审计报告\n\n"
        report += f"**时间**: {result.timestamp}\n"
        report += f"**DNA**: {result.dna}\n\n"

        report += f"## 卦象\n\n"
        report += f"- **主卦**: {result.primary_bagua.value}\n"
        report += f"- **副卦**: {result.secondary_bagua.value}\n"
        report += f"- **卦名**: {result.gua_name}\n"
        report += f"- **卦象**: `{result.gua_hex}`\n\n"

        report += f"## 审计分数\n\n"
        report += f"**总体评分**: {result.overall_score}/100\n"
        report += f"**风险等级**: {result.risk_level}\n\n"

        report += f"## 8维度评分\n\n"
        report += f"| 维度 | 代码 | 分数 | 权重 |\n"
        report += f"|------|------|-------|-------|\n"
        for dim in result.dimensions.values():
            report += f"| {dim.name} | {dim.code} | {dim.value}/100 | {dim.weight:.3f} |\n"

        report += f"\n## 审计项目\n\n"
        for item in result.audit_items:
            report += f"- {item}\n"

        return report


# ════════════════════════════════════════════════════════
# 测试与演示
# ════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("📊 龍魂 Web3-DNA 64卦审计算法 v1.0")
    print(f"   DNA: #龍芯⚡️2026-05-25-WEB3-DNA-64GUA-AUDIT-v1.0")
    print("=" * 60 + "\n")

    engine = Gua64AuditEngine()

    # 测试交易
    test_transactions = [
        {
            "tx_id": "tx-001",
            "type": "payment",
            "amount": 5000,
            "description": "标准支付交易"
        },
        {
            "tx_id": "tx-002",
            "type": "asset_creation",
            "amount": 50000,
            "description": "新型资产创建"
        },
        {
            "tx_id": "tx-003",
            "type": "transfer",
            "amount": 100000,
            "description": "大额转账"
        },
    ]

    print("📍 测试: 64卦交易审计\n")
    for tx in test_transactions:
        result = engine.audit_transaction(tx)
        print(f"交易: {tx['tx_id']} - {tx['description']}")
        print(f"  卦名: {result.gua_name}")
        print(f"  评分: {result.overall_score}/100")
        print(f"  风险: {result.risk_level}")
        print(f"  DNA: {result.dna}\n")

    print("=" * 60)
    print("✅ 64卦审计算法初始化完成")
    print("=" * 60 + "\n")
    print("🐉 龍魂 Web3-DNA · 64卦审计门 · UID9622不免责")
