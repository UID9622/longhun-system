#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 DNA 签章生成器 v1.1
DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-DNA-STAMP-GEN-V1.1-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

签章链生成器：创建DNA签章，维护链式哈希关系。
"""

import gzip
from typing import List, Dict, Optional
from datetime import datetime

from .dna_stamp import DNAStamp


class DNAStampGenerator:
    """DNA 签章生成器 · 创建语义变更签章链"""

    def __init__(self, author: str = "UID9622"):
        self.author = author
        self.chain: List[DNAStamp] = []
        self._ai_registry: Dict[str, dict] = {}

    def create_stamp(
        self,
        version: str,
        semantic_diff: str,
        structured_diff: Optional[Dict] = None,
        behavior_proof: Optional[Dict] = None,
        signatures: Optional[List[Dict]] = None,
        merge_from: Optional[List[str]] = None,
        conflicts: Optional[List[Dict]] = None,
        compressed: bool = False,
    ) -> DNAStamp:
        """
        创建DNA签章并追加到链尾

        Args:
            version: 版本号 (如 v1.0.0)
            semantic_diff: 自然语言变更描述
            structured_diff: 结构化变更描述（文件/函数/变更类型）
            behavior_proof: 行为密码学七因子证明
            signatures: AI签名列表
            merge_from: 合并来源分支
            conflicts: 冲突记录
            compressed: 是否启用gzip压缩存储

        Returns:
            新创建的DNAStamp实例
        """
        last_hash = self.chain[-1].hash() if self.chain else "0" * 16

        stamp = DNAStamp(
            version=version,
            author=self.author,
            semantic_diff=semantic_diff,
            parent_hash=last_hash,
            timestamp=datetime.now().isoformat(),
            structured_diff=structured_diff or {},
            behavior_proof=behavior_proof or {},
            signatures=signatures or [],
            merge_from=merge_from or [],
            conflicts=conflicts or [],
            compression={},
        )

        # 计算压缩元数据
        raw_json = stamp.to_json()
        raw_size = len(raw_json.encode("utf-8"))
        if compressed:
            compressed_data = gzip.compress(raw_json.encode("utf-8"))
            comp_size = len(compressed_data)
        else:
            comp_size = raw_size

        stamp.compression = {
            "original_size": raw_size,
            "compressed_size": comp_size,
            "algorithm": "gzip" if compressed else "none",
            "ratio": round(raw_size / comp_size, 1) if comp_size > 0 else 0,
        }

        self.chain.append(stamp)
        return stamp

    def get_chain_summary(self) -> str:
        """生成签章链可读摘要"""
        if not self.chain:
            return "签章链为空"

        lines = [
            f"🐉 DNA签章链 · 共 {len(self.chain)} 个节点",
            "-" * 60,
        ]
        for i, stamp in enumerate(self.chain):
            diff_preview = stamp.semantic_diff[:55]
            if len(stamp.semantic_diff) > 55:
                diff_preview += "..."
            lines.append(
                f"[{i+1:03d}] {stamp.version} | {stamp.hash()} | {diff_preview}"
            )
        lines.append("-" * 60)
        return "\n".join(lines)

    def get_chain_json(self) -> List[Dict]:
        """导出签章链为JSON列表"""
        return [stamp.to_dict() for stamp in self.chain]

    def load_chain(self, chain_data: List[Dict]):
        """从JSON列表加载签章链"""
        self.chain = [DNAStamp.from_dict(item) for item in chain_data]

    def export_compressed(self) -> bytes:
        """导出签章链为gzip压缩的JSON"""
        import json

        return gzip.compress(
            json.dumps(self.get_chain_json(), ensure_ascii=False).encode("utf-8")
        )

    @classmethod
    def import_compressed(cls, data: bytes, author: str = "UID9622") -> "DNAStampGenerator":
        """从压缩数据导入签章链"""
        import json

        gen = cls(author)
        chain_data = json.loads(gzip.decompress(data).decode("utf-8"))
        gen.load_chain(chain_data)
        return gen

    def get_storage_stats(self) -> Dict:
        """获取存储统计"""
        if not self.chain:
            return {"total_stamps": 0, "total_raw_bytes": 0, "total_compressed_bytes": 0}

        total_raw = sum(
            s.compression.get("original_size", 0) for s in self.chain
        )
        total_comp = sum(
            s.compression.get("compressed_size", 0) for s in self.chain
        )
        return {
            "total_stamps": len(self.chain),
            "total_raw_bytes": total_raw,
            "total_compressed_bytes": total_comp,
            "avg_ratio": round(total_raw / total_comp, 1) if total_comp > 0 else 0,
        }
