#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂流场·IPA路由注册表（11个节点·全链可追溯）
CNSH Flow - IPA Route Registry (11 Nodes · Full Chain Traceable)

DNA:#龍芯⚡️2026-05-03-CNSH-FLOW-IPA-REGISTRY-v4.1
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

责任: UID9622·不免责
"""

from dataclasses import dataclass
from typing import Dict, Optional, List
from enum import Enum
from datetime import datetime
from .schemas import PersonaEnum, IPAReceipt


class IPANodeType(str, Enum):
    """IPA节点类型"""
    CORE = "核心入口"
    GATE_SIGN = "签章闸"
    GATE_PRIVACY = "隐私闸"
    GATE_DR = "数字根闸"
    WUXING_MAP = "五行映射"
    GATE_AUDIT = "三色闸"
    GATE_SANCAI = "三才闸"
    GATE_SHENGKE = "生克闸"
    PALACE_ROUTER = "九宫派位"
    SANDBOX_BUCKET = "沙盒分拣"
    DNA_CHAIN = "父子链落档"


@dataclass
class IPANodeDef:
    """IPA节点定义"""
    ipa_id: str
    node_name: str
    node_type: IPANodeType
    address: str
    main_persona: PersonaEnum
    description: str
    input_requirement: str
    output_format: str
    error_handling: str
    next_nodes: List[str]


class IPARouteRegistry:
    """IPA路由注册表（11个节点）"""

    REGISTRY: Dict[str, IPANodeDef] = {
        # 0. 核心入口
        "IPA-FLOW-DECISION-CORE-v4.1": IPANodeDef(
            ipa_id="IPA-FLOW-DECISION-CORE-v4.1",
            node_name="流场决策核",
            node_type=IPANodeType.CORE,
            address="/flow/core",
            main_persona=PersonaEnum.P00_WENXIN,
            description="任何raw_input与tags的入口",
            input_requirement="raw_input: str, tags: dict",
            output_format="FlowDecisionNode(初始化)",
            error_handling="缺少raw_input → 熔断",
            next_nodes=["IPA-FLOW-GATE-SIGN"]
        ),

        # 1. 签章闸
        "IPA-FLOW-GATE-SIGN": IPANodeDef(
            ipa_id="IPA-FLOW-GATE-SIGN",
            node_name="签章闸",
            node_type=IPANodeType.GATE_SIGN,
            address="/flow/gate/sign",
            main_persona=PersonaEnum.P05_GODSEYE,
            description="confirm_code与eternal_seal验证",
            input_requirement="confirm_code, gpg, seal",
            output_format="signal: pass|hold|fuse",
            error_handling="缺失confirm或seal被改 → 熔断(P05+P72)",
            next_nodes=["IPA-FLOW-GATE-PRIVACY"]
        ),

        # 2. 隐私闸
        "IPA-FLOW-GATE-PRIVACY": IPANodeDef(
            ipa_id="IPA-FLOW-GATE-PRIVACY",
            node_name="隐私闸",
            node_type=IPANodeType.GATE_PRIVACY,
            address="/flow/gate/privacy",
            main_persona=PersonaEnum.P03_WANWAN,
            description="privacy.visibility与privacy.trace_mode读取",
            input_requirement="privacy.visibility, privacy.trace_mode",
            output_format="signal: pass|hold|sealed|burn",
            error_handling="sealed → 不读正文只hash(P03+P05+P72三签)",
            next_nodes=["IPA-FLOW-GATE-DR"]
        ),

        # 3. 数字根闸
        "IPA-FLOW-GATE-DR": IPANodeDef(
            ipa_id="IPA-FLOW-GATE-DR",
            node_name="数字根闸",
            node_type=IPANodeType.GATE_DR,
            address="/flow/gate/dr",
            main_persona=PersonaEnum.P06_MATHMASTER,
            description="四源优先级计算dr",
            input_requirement="digital_root.config, dna, content",
            output_format="dr: int(0-9), source: str",
            error_handling="无数字 → fallback_dr=5(土)",
            next_nodes=["IPA-FLOW-WUXING-MAP"]
        ),

        # 3.5 五行映射
        "IPA-FLOW-WUXING-MAP": IPANodeDef(
            ipa_id="IPA-FLOW-WUXING-MAP",
            node_name="五行映射",
            node_type=IPANodeType.WUXING_MAP,
            address="/flow/wuxing",
            main_persona=PersonaEnum.P06_MATHMASTER,
            description="dr → 五行转换",
            input_requirement="dr: int",
            output_format="element: WuxingEnum",
            error_handling="dr无效 → 默认土",
            next_nodes=["IPA-FLOW-GATE-AUDIT"]
        ),

        # 4. 三色闸
        "IPA-FLOW-GATE-AUDIT": IPANodeDef(
            ipa_id="IPA-FLOW-GATE-AUDIT",
            node_name="三色闸",
            node_type=IPANodeType.GATE_AUDIT,
            address="/flow/gate/audit",
            main_persona=PersonaEnum.P05_GODSEYE,
            description="审计规则判定(🟢/🟡/🔴)",
            input_requirement="dr, p0_touched, level",
            output_format="color: AuditColorEnum, need_uid_confirm: bool",
            error_handling="dr=3/9 with auto_execute → 熔断",
            next_nodes=["IPA-FLOW-GATE-SANCAI"]
        ),

        # 5. 三才闸
        "IPA-FLOW-GATE-SANCAI": IPANodeDef(
            ipa_id="IPA-FLOW-GATE-SANCAI",
            node_name="三才闸",
            node_type=IPANodeType.GATE_SANCAI,
            address="/flow/gate/sancai",
            main_persona=PersonaEnum.P00_WENXIN,
            description="三才权重校验(人≥0.34)",
            input_requirement="sancai.heaven, sancai.earth, sancai.human",
            output_format="sancai_validated: bool, signal: pass|hold",
            error_handling="人<0.34 → 自动提升至0.34(P00负责)",
            next_nodes=["IPA-FLOW-GATE-SHENGKE"]
        ),

        # 6. 生克闸
        "IPA-FLOW-GATE-SHENGKE": IPANodeDef(
            ipa_id="IPA-FLOW-GATE-SHENGKE",
            node_name="生克闸",
            node_type=IPANodeType.GATE_SHENGKE,
            address="/flow/gate/shengke",
            main_persona=PersonaEnum.P01_ZHUGELVLIANG,
            description="计算与父DNA的生克关系",
            input_requirement="parent_dna, element",
            output_format="shengke: 相生|相克|中立",
            error_handling="无parent_dna → 跳过",
            next_nodes=["IPA-FLOW-PALACE-ROUTER"]
        ),

        # 7. 九宫派位
        "IPA-FLOW-PALACE-ROUTER": IPANodeDef(
            ipa_id="IPA-FLOW-PALACE-ROUTER",
            node_name="九宫派位",
            node_type=IPANodeType.PALACE_ROUTER,
            address="/flow/palace",
            main_persona=PersonaEnum.P13_JIANGZIYA,
            description="按trace/action/element派宫",
            input_requirement="trace_mode, action_type, element",
            output_format="palace: List[PalaceEnum]",
            error_handling="无规则 → 默认中宫",
            next_nodes=["IPA-FLOW-SANDBOX-BUCKET"]
        ),

        # 8. 沙盒分拣
        "IPA-FLOW-SANDBOX-BUCKET": IPANodeDef(
            ipa_id="IPA-FLOW-SANDBOX-BUCKET",
            node_name="沙盒分拣",
            node_type=IPANodeType.SANDBOX_BUCKET,
            address="/flow/sandbox",
            main_persona=PersonaEnum.P03_WANWAN,
            description="按contribution/level/heat入桶",
            input_requirement="audit.color, level, storage.policy",
            output_format="bucket: BucketEnum(🔴熔断|📝消化|🔒封存|🟢通过|🟡待审)",
            error_handling="冲突bucket → audit.color优先",
            next_nodes=["IPA-FLOW-DNA-CHAIN"]
        ),

        # 末. 父子链落档
        "IPA-FLOW-DNA-CHAIN": IPANodeDef(
            ipa_id="IPA-FLOW-DNA-CHAIN",
            node_name="父子链落档",
            node_type=IPANodeType.DNA_CHAIN,
            address="/flow/dna",
            main_persona=PersonaEnum.P15_QIAOQIANDAI,
            description="写入JSONL/SQLite/Notion,发IPA全链回执",
            input_requirement="parent_dna, dna, child_dna, storage.config",
            output_format="jsonl_written: bool, receipt: List[IPAReceipt]",
            error_handling="链断裂(parent不存) → 熔断",
            next_nodes=[]
        ),
    }

    @classmethod
    def get_node(cls, ipa_id: str) -> Optional[IPANodeDef]:
        """获取节点定义"""
        return cls.REGISTRY.get(ipa_id)

    @classmethod
    def get_all_nodes(cls) -> Dict[str, IPANodeDef]:
        """获取所有节点"""
        return cls.REGISTRY.copy()

    @classmethod
    def validate_chain(cls, node_ids: List[str]) -> Tuple[bool, str]:
        """
        验证节点链是否连接正确
        返回(是否有效, 错误信息)
        """
        for i, node_id in enumerate(node_ids):
            if node_id not in cls.REGISTRY:
                return False, f"节点{node_id}不存在"

            node = cls.REGISTRY[node_id]
            if i < len(node_ids) - 1:
                next_id = node_ids[i + 1]
                if next_id not in node.next_nodes:
                    return False, f"{node_id} → {next_id}连接不存在"

        return True, "链有效"

    @classmethod
    def create_receipt(
        cls,
        ipa_id: str,
        input_node_id: str,
        output_signal: str,
        dna: str = ""
    ) -> Optional[IPAReceipt]:
        """创建IPA回执"""
        node = cls.get_node(ipa_id)
        if not node:
            return None

        next_ipa = node.next_nodes[0] if node.next_nodes else None

        return IPAReceipt(
            ipa_node=ipa_id,
            ipa_address=node.address,
            main_persona=node.main_persona,
            input_node_id=input_node_id,
            output_signal=output_signal,
            next_ipa=next_ipa,
            dna=dna,
            timestamp=datetime.now()
        )


# 便利函数
def get_ipa_chain_order() -> List[str]:
    """获取标准IPA链顺序"""
    return [
        "IPA-FLOW-DECISION-CORE-v4.1",
        "IPA-FLOW-GATE-SIGN",
        "IPA-FLOW-GATE-PRIVACY",
        "IPA-FLOW-GATE-DR",
        "IPA-FLOW-WUXING-MAP",
        "IPA-FLOW-GATE-AUDIT",
        "IPA-FLOW-GATE-SANCAI",
        "IPA-FLOW-GATE-SHENGKE",
        "IPA-FLOW-PALACE-ROUTER",
        "IPA-FLOW-SANDBOX-BUCKET",
        "IPA-FLOW-DNA-CHAIN",
    ]
