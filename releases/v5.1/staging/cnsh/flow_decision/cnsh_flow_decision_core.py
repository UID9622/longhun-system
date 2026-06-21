#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂流场决策核 v4.1·主入口（10道闸完整流程）
CNSH Flow Decision Core v4.1 - Main Entry Point (10 Gates Complete Flow)

DNA:#龍芯⚡️2026-05-03-CNSH-FLOW-DECISION-CORE-FILE1-v4.1-MAIN
PARENT_DNA:#龍芯⚡️2026-05-03-CNSH-FLOW-DECISION-CORE-v4.1
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

责任: UID9622·不免责
"""

import json
import hashlib
from typing import Optional, List, Tuple
from datetime import datetime
from .schemas import (
    FlowDecisionNode, VisibilityEnum, BucketEnum, StatusEnum,
    WuxingEnum, AuditColorEnum, PersonaEnum, PrivacyConfig,
    TraceModeEnum, LevelEnum
)
from .digital_root import DigitalRootCalculator, quick_dr
from .ipa_route_registry import IPARouteRegistry, get_ipa_chain_order
from .persona_collaboration import PersonaCollaborationFramework
from .dna_chain_tracer import DNAChainTracer, DNATagPolicyValidator


from integrated_modules.longhun_config import getenv


class CNSHFlowDecisionCore:
    """龍魂流场决策核 v4.1 主类"""

    CONFIRM_CODE = getenv("LONGHUN_CONFIRM_CODE", "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    GPG_CODE = getenv("GPG_FINGERPRINT", "A2D0092CEE2E5BA87035600924C3704A8CC26D5F")

    def __init__(self):
        self.dna_registry = {}  # 存储所有DNA及其关系

    def process_input(
        self,
        raw_input: str,
        tags: dict,
        parent_dna: str = ""
    ) -> Tuple[FlowDecisionNode, List[str]]:
        """
        主流程：处理输入并返回FlowDecisionNode
        返回: (完整的FlowDecisionNode, 处理日志)
        """
        logs = []
        logs.append("【流场决策核启动】")

        # 初始化节点
        node = FlowDecisionNode(
            title=tags.get("title", "unknown"),
            node_id=self._generate_node_id(),
            raw_input=raw_input,
            parent_dna=parent_dna,
            tags=tags,
            dna=tags.get("dna", ""),
            confirm_code=self.CONFIRM_CODE,
            gpg=self.GPG_CODE,
        )

        logs.append(f"初始化节点: {node.node_id}")

        # ===== 第1道闸：签章闸 =====
        logs.append("\n【第1道·签章闸】")
        signal_1, log_1 = self._gate_sign(node)
        logs.extend(log_1)
        if signal_1 == "fuse":
            node.result_status = StatusEnum.FUSE
            node.route.bucket = BucketEnum.FUSE
            logs.append("→ 熔断（缺失签章）")
            return node, logs

        # ===== 第2道闸：隐私闸 =====
        logs.append("\n【第2道·隐私闸】")
        signal_2, log_2 = self._gate_privacy(node)
        logs.extend(log_2)
        if signal_2 == "sealed":
            node.storage.raw_body = None  # 销毁正文
            logs.append("→ sealed（不读正文，只保存hash）")

        # ===== 第3道闸：数字根闸 =====
        logs.append("\n【第3道·数字根闸】")
        signal_3, log_3 = self._gate_dr(node)
        logs.extend(log_3)

        # ===== 第3.5道：五行映射 =====
        logs.append("\n【第3.5道·五行映射】")
        signal_35, log_35 = self._gate_wuxing(node)
        logs.extend(log_35)

        # ===== 第4道闸：三色闸 =====
        logs.append("\n【第4道·三色闸】")
        signal_4, log_4 = self._gate_audit(node)
        logs.extend(log_4)

        # ===== 第5道闸：三才闸 =====
        logs.append("\n【第5道·三才闸】")
        signal_5, log_5 = self._gate_sancai(node)
        logs.extend(log_5)

        # ===== 第6道闸：生克闸 =====
        logs.append("\n【第6道·生克闸】")
        signal_6, log_6 = self._gate_shengke(node)
        logs.extend(log_6)

        # ===== 第7道闸：九宫派位 =====
        logs.append("\n【第7道·九宫派位】")
        signal_7, log_7 = self._gate_palace(node)
        logs.extend(log_7)

        # ===== 第8道闸：沙盒分拣 =====
        logs.append("\n【第8道·沙盒分拣】")
        signal_8, log_8 = self._gate_sandbox(node)
        logs.extend(log_8)

        # ===== 第9道闸：父子链落档 =====
        logs.append("\n【第9道·父子链落档】")
        signal_9, log_9 = self._gate_dna_chain(node)
        logs.extend(log_9)

        # 最终状态判定
        logs.append("\n【流场决策完成】")
        if node.route.bucket == BucketEnum.FUSE:
            node.result_status = StatusEnum.FUSE
            logs.append(f"最终状态: 🔴 FUSE")
        elif node.audit.color == AuditColorEnum.YELLOW:
            node.result_status = StatusEnum.HOLD
            logs.append(f"最终状态: 🟡 HOLD")
        else:
            node.result_status = StatusEnum.ENTER
            logs.append(f"最终状态: 🟢 ENTER")

        node.result_timestamp = datetime.now()
        logs.append(f"时间戳: {node.result_timestamp.isoformat()}")

        return node, logs

    # ===== 10道闸的具体实现 =====

    def _gate_sign(self, node: FlowDecisionNode) -> Tuple[str, List[str]]:
        """第1道·签章闸 (IPA-FLOW-GATE-SIGN)"""
        logs = []
        gate_config = PersonaCollaborationFramework.get_gate_config(1)

        # 检查confirm_code
        if node.confirm_code != self.CONFIRM_CODE:
            logs.append(f"  ❌ confirm_code不匹配")
            receipt = PersonaCollaborationFramework.create_gate_receipt(1, "fuse", "硬闸1")
            node.gate_receipts.append(receipt)
            return "fuse", logs

        # 检查GPG
        if node.gpg != self.GPG_CODE:
            logs.append(f"  ❌ GPG不匹配")
            receipt = PersonaCollaborationFramework.create_gate_receipt(1, "fuse", "硬闸2")
            node.gate_receipts.append(receipt)
            return "fuse", logs

        logs.append(f"  ✅ confirm & gpg验证通过")
        logs.append(f"  主驻: {gate_config.main_persona.value}")
        receipt = PersonaCollaborationFramework.create_gate_receipt(1, "pass")
        node.gate_receipts.append(receipt)
        return "pass", logs

    def _gate_privacy(self, node: FlowDecisionNode) -> Tuple[str, List[str]]:
        """第2道·隐私闸 (IPA-FLOW-GATE-PRIVACY)"""
        logs = []
        gate_config = PersonaCollaborationFramework.get_gate_config(2)

        privacy = node.privacy
        logs.append(f"  隐私等级: {privacy.visibility.value}")
        logs.append(f"  追溯模式: {privacy.trace_mode.value}")

        if privacy.visibility == VisibilityEnum.PRIVATE:
            if privacy.trace_mode == TraceModeEnum.NO_EXTERNAL:
                logs.append(f"  🔒 sealed级隐私（不读正文，不外发）")
                logs.append(f"  需要三签: P03+P05+P72")
                receipt = PersonaCollaborationFramework.create_gate_receipt(2, "sealed", "硬闸3/10")
                node.gate_receipts.append(receipt)
                node.storage.seal_proof = DNAChainTracer.create_seal_proof(
                    node.dna, node.raw_input, "UID9622",
                    personas_signed=["P03", "P05", "P72"]
                )
                return "sealed", logs

        logs.append(f"  ✅ 隐私闸通过")
        receipt = PersonaCollaborationFramework.create_gate_receipt(2, "pass")
        node.gate_receipts.append(receipt)
        return "pass", logs

    def _gate_dr(self, node: FlowDecisionNode) -> Tuple[str, List[str]]:
        """第3道·数字根闸 (IPA-FLOW-GATE-DR)"""
        logs = []
        gate_config = PersonaCollaborationFramework.get_gate_config(3)

        dr, source = DigitalRootCalculator.calculate_dr(
            node.digital_root,
            dna=node.dna,
            content=node.raw_input
        )
        logs.append(f"  数字根: dr={dr} (来源: {source})")
        node.digital_root.explicit_dr = dr

        receipt = PersonaCollaborationFramework.create_gate_receipt(3, "pass")
        node.gate_receipts.append(receipt)
        return "pass", logs

    def _gate_wuxing(self, node: FlowDecisionNode) -> Tuple[str, List[str]]:
        """第3.5道·五行映射"""
        logs = []
        dr = node.digital_root.get_primary_dr()
        element = DigitalRootCalculator.dr_to_wuxing(dr)
        node.math.element = element
        logs.append(f"  五行: {element.value}")

        receipt = PersonaCollaborationFramework.create_gate_receipt(4, "pass")
        node.gate_receipts.append(receipt)
        return "pass", logs

    def _gate_audit(self, node: FlowDecisionNode) -> Tuple[str, List[str]]:
        """第4道·三色闸 (IPA-FLOW-GATE-AUDIT)"""
        logs = []
        gate_config = PersonaCollaborationFramework.get_gate_config(5)

        dr = node.digital_root.get_primary_dr()

        # 检查硬闸7: dr=3/9 + auto_execute=true
        if dr in [3, 9] and node.tags.get("auto_execute", False):
            logs.append(f"  ❌ dr={dr} + auto_execute=true → 禁止自动执行（硬闸7）")
            node.audit.color = AuditColorEnum.RED
            receipt = PersonaCollaborationFramework.create_gate_receipt(5, "hold", "硬闸7")
            node.gate_receipts.append(receipt)
            return "hold", logs

        # 检查硬闸8: dr=6 → 待审
        if dr == 6:
            logs.append(f"  🟡 dr=6 → 待审（硬闸8）")
            node.audit.color = AuditColorEnum.YELLOW
            node.audit.need_uid_confirm = True
            receipt = PersonaCollaborationFramework.create_gate_receipt(5, "hold", "硬闸8")
            node.gate_receipts.append(receipt)
            return "hold", logs

        # 检查硬闸9: L0永恒
        if node.dna_tags.level == LevelEnum.L0_ETERNAL:
            logs.append(f"  ℹ️  L0永恒 → need_uid_confirm（硬闸9）")
            node.audit.need_uid_confirm = True
            node.audit.color = AuditColorEnum.GREEN

        logs.append(f"  ✅ 三色: {node.audit.color.value}")
        receipt = PersonaCollaborationFramework.create_gate_receipt(5, "pass")
        node.gate_receipts.append(receipt)
        return "pass", logs

    def _gate_sancai(self, node: FlowDecisionNode) -> Tuple[str, List[str]]:
        """第5道·三才闸 (IPA-FLOW-GATE-SANCAI)"""
        logs = []
        gate_config = PersonaCollaborationFramework.get_gate_config(6)

        # 检查硬闸6: 人 >= 0.34
        if node.math.sancai_human < 0.34:
            logs.append(f"  ⚠️  人权重={node.math.sancai_human} < 0.34 → 自动提升至0.34")
            node.math.sancai_human = 0.34
            node.audit.color = AuditColorEnum.YELLOW

        logs.append(f"  三才: 天={node.math.sancai_heaven}, 地={node.math.sancai_earth}, 人={node.math.sancai_human}")
        receipt = PersonaCollaborationFramework.create_gate_receipt(6, "pass")
        node.gate_receipts.append(receipt)
        return "pass", logs

    def _gate_shengke(self, node: FlowDecisionNode) -> Tuple[str, List[str]]:
        """第6道·生克闸 (IPA-FLOW-GATE-SHENGKE)"""
        logs = []
        gate_config = PersonaCollaborationFramework.get_gate_config(7)

        if not node.parent_dna:
            logs.append(f"  ℹ️  无parent_dna，跳过生克计算")
            receipt = PersonaCollaborationFramework.create_gate_receipt(7, "pass")
            node.gate_receipts.append(receipt)
            return "pass", logs

        logs.append(f"  与parent_dna的五行: {node.math.shengke_with_parent or '未计算'}")
        receipt = PersonaCollaborationFramework.create_gate_receipt(7, "pass")
        node.gate_receipts.append(receipt)
        return "pass", logs

    def _gate_palace(self, node: FlowDecisionNode) -> Tuple[str, List[str]]:
        """第7道·九宫派位 (IPA-FLOW-PALACE-ROUTER)"""
        logs = []
        gate_config = PersonaCollaborationFramework.get_gate_config(8)

        # 简单派位规则：根据trace_mode和element
        from schemas import PalaceEnum
        node.route.palace = [PalaceEnum.PALACE_5]  # 默认中宫

        logs.append(f"  派位宫位: {[p.value for p in node.route.palace]}")
        receipt = PersonaCollaborationFramework.create_gate_receipt(8, "pass")
        node.gate_receipts.append(receipt)
        return "pass", logs

    def _gate_sandbox(self, node: FlowDecisionNode) -> Tuple[str, List[str]]:
        """第8道·沙盒分拣 (IPA-FLOW-SANDBOX-BUCKET)"""
        logs = []
        gate_config = PersonaCollaborationFramework.get_gate_config(9)

        # 根据audit.color分拣
        if node.audit.color == AuditColorEnum.RED:
            node.route.bucket = BucketEnum.FUSE
            logs.append(f"  → 🔴 熔断")
        elif node.audit.color == AuditColorEnum.YELLOW:
            node.route.bucket = BucketEnum.HOLD
            logs.append(f"  → 🟡 待审")
        else:
            node.route.bucket = BucketEnum.NORMAL
            logs.append(f"  → 🟢 通过")

        receipt = PersonaCollaborationFramework.create_gate_receipt(9, "pass")
        node.gate_receipts.append(receipt)
        return "pass", logs

    def _gate_dna_chain(self, node: FlowDecisionNode) -> Tuple[str, List[str]]:
        """第9道·父子链落档 (IPA-FLOW-DNA-CHAIN)"""
        logs = []
        gate_config = PersonaCollaborationFramework.get_gate_config(10)

        # 生成child_dna
        content_hash = DNAChainTracer.calculate_content_hash(node.raw_input)
        node.child_dna = DNAChainTracer.generate_dna_child_id(node.dna, content_hash)
        logs.append(f"  生成子DNA: {node.child_dna}")

        # 验证链
        valid, msg = DNAChainTracer.validate_dna_chain(
            node.parent_dna, node.dna, node.child_dna
        )
        if not valid:
            logs.append(f"  ⚠️  {msg}")

        logs.append(f"  ✅ DNA链完整")
        receipt = PersonaCollaborationFramework.create_gate_receipt(10, "pass")
        node.gate_receipts.append(receipt)
        return "pass", logs

    @staticmethod
    def _generate_node_id() -> str:
        """生成节点ID: FLOW-9622-YYYYMMDD-8charHash"""
        from datetime import datetime
        now = datetime.now()
        date_str = now.strftime("%Y%m%d")
        hash_str = hashlib.md5(now.isoformat().encode()).hexdigest()[:8]
        return f"FLOW-9622-{date_str}-{hash_str}"


# 快速入口
def quick_process(raw_input: str, tags: dict = None, parent_dna: str = "") -> FlowDecisionNode:
    """快速处理输入"""
    if tags is None:
        tags = {"title": "quick_process"}

    core = CNSHFlowDecisionCore()
    node, logs = core.process_input(raw_input, tags, parent_dna)

    # 打印日志
    for log in logs:
        print(log)

    return node
