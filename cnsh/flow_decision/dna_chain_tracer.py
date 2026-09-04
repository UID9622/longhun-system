#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂流场·DNA父子链追踪（多标签+四源数字根+销毁封存证明）
CNSH Flow - DNA Chain Tracer (Multi-Tags + Four-Source DR + Destroy/Seal Proof)

DNA:#龍芯⚡️2026-05-03-CNSH-FLOW-DNA-CHAIN-FILE1-v4.1
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

责任: UID9622·不免责
"""

import hashlib
import json
from dataclasses import dataclass, asdict
from typing import Optional, List, Tuple, Any
from datetime import datetime
from .schemas import DNATagPolicy, LevelEnum, VisibilityEnum, TraceModeEnum


@dataclass
class DNAProof:
    """DNA证明记录"""
    dna: str
    proof_type: str  # "burn" | "sealed"
    content_hash: str  # SHA256
    operator: str
    timestamp: datetime
    personas_signed: List[str] = None


class DNAChainTracer:
    """DNA父子链追踪器（IPA-FLOW-DNA-CHAIN）"""

    @staticmethod
    def generate_dna_child_id(parent_dna: str, content_hash: str) -> str:
        """
        生成子DNA ID
        格式: parent_dna + "-CHILD-" + hash8
        例:#龍芯⚡️2026-05-03-XXX-v4.1-CHILD-A1B2C3D4
        """
        combined = f"{parent_dna}${content_hash}".encode('utf-8')
        h = hashlib.sha256(combined).hexdigest()
        child_id = f"{parent_dna}-CHILD-{h[:8]}"
        return child_id

    @staticmethod
    def calculate_content_hash(content: str) -> str:
        """计算内容SHA256哈希"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    @staticmethod
    def create_burn_proof(
        dna: str,
        content: str,
        operator: str
    ) -> str:
        """
        生成销毁证明
        格式: burn_proof:sha256:[hash]+[timestamp]+[operator]
        """
        content_hash = DNAChainTracer.calculate_content_hash(content)
        timestamp = datetime.now().isoformat()
        proof = f"burn_proof:sha256:{content_hash}+{timestamp}+{operator}"
        return proof

    @staticmethod
    def create_seal_proof(
        dna: str,
        content: str,
        operator: str,
        personas_signed: List[str] = None
    ) -> str:
        """
        生成封存证明
        格式: seal_proof:sha256:[hash]+[timestamp]+[operator]+[P03,P05,P72]
        """
        if personas_signed is None:
            personas_signed = []
        content_hash = DNAChainTracer.calculate_content_hash(content)
        timestamp = datetime.now().isoformat()
        personas_str = ",".join(personas_signed) if personas_signed else "unsigned"
        proof = f"seal_proof:sha256:{content_hash}+{timestamp}+{operator}+{personas_str}"
        return proof

    @staticmethod
    def validate_dna_chain(
        parent_dna: str,
        current_dna: str,
        child_dna: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        验证DNA链完整性
        返回(是否有效, 错误/成功消息)
        """
        # 验证current_dna存在
        if not current_dna:
            return False, "当前DNA不能为空"

        # 验证parent_dna链接有效（如果不是首条）
        if parent_dna and not parent_dna.startswith("#龍芯"):
            return False, "parent_dna格式无效"

        # 验证child_dna格式（如果存在）
        if child_dna:
            if not child_dna.endswith("-CHILD-") and "-CHILD-" not in child_dna:
                return False, "child_dna格式无效（缺少-CHILD-标记）"

        return True, "链有效"

    @staticmethod
    def trace_to_ancestor(
        dna_registry: dict[str, Any],
        current_dna: str,
        max_depth: int = 10
    ) -> List[str]:
        """
        追踪DNA到祖先
        返回从祖父到当前的DNA列表
        """
        chain = [current_dna]
        depth = 0

        while depth < max_depth:
            # 从registry查找parent_dna
            if current_dna not in dna_registry:
                break

            parent = dna_registry[current_dna].get("parent_dna")
            if not parent:
                break

            chain.insert(0, parent)
            current_dna = parent
            depth += 1

        return chain

    @staticmethod
    def trace_to_descendants(
        dna_registry: dict[str, Any],
        current_dna: str,
        max_depth: int = 10
    ) -> List[str]:
        """
        追踪DNA到后代
        返回从当前到最新后代的DNA列表
        """
        chain = [current_dna]
        depth = 0

        while depth < max_depth:
            # 找child_dna
            found_child = None
            for dna, record in dna_registry.items():
                if record.get("parent_dna") == current_dna:
                    found_child = dna
                    break

            if not found_child:
                break

            chain.append(found_child)
            current_dna = found_child
            depth += 1

        return chain

    @staticmethod
    def build_full_lineage(
        dna_registry: dict[str, Any],
        target_dna: str
    ) -> dict[str, Any]:
        """
        构建完整DNA谱系
        返回: {
            "grandparent": "...",
            "parent": "...",
            "self": "...",
            "child": "...",
            "descendant_chain": [...]
        }
        """
        ancestors = DNAChainTracer.trace_to_ancestor(dna_registry, target_dna)
        descendants = DNAChainTracer.trace_to_descendants(dna_registry, target_dna)

        result = {
            "full_ancestry": ancestors,
            "full_descendancy": descendants,
            "grandparent": ancestors[0] if len(ancestors) >= 2 else None,
            "parent": ancestors[-2] if len(ancestors) >= 2 else None,
            "self": target_dna,
            "child": descendants[1] if len(descendants) >= 2 else None,
        }

        return result


class DNATagPolicyValidator:
    """DNA多标签策略验证器"""

    @staticmethod
    def validate_dna_tags(policy: DNATagPolicy) -> Tuple[bool, List[str]]:
        """
        验证DNA多标签策略
        返回(是否有效, 错误列表)
        """
        errors = []

        # 验证必填字段
        if not policy.operator:
            errors.append("operator字段不能为空")

        if policy.level == LevelEnum.L0_ETERNAL and not policy.p0_touched:
            errors.append("L0级数据必须标记p0_touched=True")

        # 验证sealed逻辑
        if policy.visibility == VisibilityEnum.PRIVATE and policy.trace_mode == TraceModeEnum.NO_EXTERNAL:
            # private + no_external 的组合是合理的
            pass

        return len(errors) == 0, errors

    @staticmethod
    def auto_set_tags_by_content(
        content: str,
        tags: dict[str, Any]
    ) -> DNATagPolicy:
        """
        根据内容自动设置DNA标签
        例：检测到token -> visibility=PRIVATE
        """
        policy = DNATagPolicy(
            visibility=tags.get("visibility", VisibilityEnum.INTERNAL),
            trace_mode=tags.get("trace_mode", TraceModeEnum.CHAIN),
            operator=tags.get("operator", "UID9622"),
            p0_touched=tags.get("p0_touched", False),
            level=tags.get("level", LevelEnum.L3_DAILY),
            parent_dna=tags.get("parent_dna", ""),
        )

        # 检测敏感内容
        sensitive_keywords = ["token", "key", "secret", "password", "private_key", "api_key"]
        for kw in sensitive_keywords:
            if kw.lower() in content.lower():
                policy.visibility = VisibilityEnum.PRIVATE
                policy.trace_mode = TraceModeEnum.NO_EXTERNAL
                break

        return policy
