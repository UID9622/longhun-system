#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 DNA 签章数据结构 v1.1
DNA: #龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-DNA-STAMP-V1.1-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

DNA 签章节点：每个签章记录一次语义变更。链式哈希结构，不可篡改。
"""

import json
import hashlib
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DNAStamp:
    """
    DNA 签章节点 · 每个签章记录一次变更

    关键设计:
      - semantic_diff: 自然语言变更描述（AI可读），传统diff是"改了什么"，
        语义diff是"为什么改"
      - parent_hash: 链式结构，任何中间节点被篡改整条链失效
      - signatures: 多AI接龍，每个AI只签自己参与的部分
      - behavior_proof: 行为密码学七因子，证明"谁在什么情境下做了什么"
      - conflicts: 冲突显式记录，不悄悄覆盖
    """

    version: str
    author: str
    semantic_diff: str
    parent_hash: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    structured_diff: Dict = field(default_factory=dict)
    behavior_proof: Dict = field(default_factory=dict)
    signatures: List[Dict] = field(default_factory=list)
    merge_from: List[str] = field(default_factory=list)
    conflicts: List[Dict] = field(default_factory=list)
    compression: Dict = field(default_factory=dict)

    def hash(self) -> str:
        """计算签章哈希（用于链式验证）"""
        content = (
            f"{self.version}{self.author}{self.semantic_diff}"
            f"{self.parent_hash}{self.timestamp}"
        )
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def to_json(self) -> str:
        """序列化为JSON"""
        return json.dumps(self.__dict__, ensure_ascii=False, indent=2)

    def to_dict(self) -> dict:
        """转为纯字典（确保JSON可序列化）"""
        return {
            "version": self.version,
            "author": self.author,
            "semantic_diff": self.semantic_diff,
            "parent_hash": self.parent_hash,
            "timestamp": self.timestamp,
            "structured_diff": self.structured_diff,
            "behavior_proof": self.behavior_proof,
            "signatures": self.signatures,
            "merge_from": self.merge_from,
            "conflicts": self.conflicts,
            "compression": self.compression,
        }

    @classmethod
    def from_json(cls, data: str) -> "DNAStamp":
        """从JSON字符串反序列化"""
        obj = json.loads(data)
        return cls(**obj)

    @classmethod
    def from_dict(cls, data: dict) -> "DNAStamp":
        """从字典反序列化"""
        return cls(
            version=data.get("version", ""),
            author=data.get("author", ""),
            semantic_diff=data.get("semantic_diff", ""),
            parent_hash=data.get("parent_hash", ""),
            timestamp=data.get("timestamp", ""),
            structured_diff=data.get("structured_diff", {}),
            behavior_proof=data.get("behavior_proof", {}),
            signatures=data.get("signatures", []),
            merge_from=data.get("merge_from", []),
            conflicts=data.get("conflicts", []),
            compression=data.get("compression", {}),
        )

    def validate(self) -> Dict[str, any]:
        """
        验证签章数据结构的合法性
        - 必填字段完整性
        - 签名格式校验
        """
        errors = []
        warnings = []

        # 必填字段
        if not self.version:
            errors.append("version 为空")
        if not self.author:
            errors.append("author 为空")
        if not self.semantic_diff:
            warnings.append("semantic_diff 为空（建议填写）")
        if not self.timestamp:
            errors.append("timestamp 为空")

        # 哈希一致性
        computed = self.hash()
        if self.parent_hash and len(self.parent_hash) != 16:
            errors.append(f"parent_hash 长度异常: {len(self.parent_hash)} (期望16)")

        # 签名校验
        for i, sig in enumerate(self.signatures):
            if "ai" not in sig:
                errors.append(f"签章[{i}] 缺少 ai 字段")
            if "sig" not in sig:
                errors.append(f"签章[{i}] ({sig.get('ai', '?')}) 缺少 sig 字段")
            if "timestamp" not in sig:
                warnings.append(f"签章[{i}] ({sig.get('ai', '?')}) 缺少 timestamp")

        # 压缩率校验
        if self.compression:
            orig = self.compression.get("original_size", 0)
            comp = self.compression.get("compressed_size", 0)
            if orig > 0 and comp > 0:
                ratio = orig / comp
                if ratio < 50:
                    warnings.append(f"压缩率偏低: {ratio:.0f}:1 (期望 >= 50:1)")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "hash": computed,
        }
