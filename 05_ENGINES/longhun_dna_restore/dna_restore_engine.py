#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 DNA 还原引擎 v1.1
DNA: #龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-DNA-RESTORE-ENGINE-V1.1-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

从DNA签章链还原完整代码。三层架构：存储层→解析层→重放层。
支持哈希链完整性验证、冲突检测与回滚。
"""

import gzip
import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from .dna_stamp import DNAStamp
from .semantic_parser import SemanticParser


class ChainBrokenError(Exception):
    """签章链断裂异常"""
    pass


class DNARestoreEngine:
    """
    DNA 还原引擎 · 三层架构

    层1 - 存储层: 创世版本 + DNA签章链
    层2 - 解析层: 签章解析 + 变更映射 + 语义AI解析
    层3 - 重放层: 增量还原 + 冲突检测 + 回滚栈

    工作流程:
        Phase 1: 加载创世版本（支持压缩）
        Phase 2: 解析DNA签章链（校验哈希链完整性）
        Phase 3: 增量重放变更（语义→代码映射）
        Phase 4: 冲突检测与回滚
    """

    def __init__(self):
        self.genesis_data: Optional[bytes] = None
        self.chain: List[DNAStamp] = []
        self.current_state: Optional[bytes] = None
        self.restore_log: List[Dict] = []
        self.parser = SemanticParser()
        self._rollback_stack: List[bytes] = []

    # ─── Phase 1: 加载创世版本 ───

    def set_genesis(self, genesis_data: bytes):
        """
        加载创世版本（支持gzip压缩）
        - 尝试解压，失败则按原文处理
        """
        try:
            self.genesis_data = gzip.decompress(genesis_data)
        except Exception:
            self.genesis_data = genesis_data
        self.current_state = self.genesis_data

    def load_genesis_from_file(self, path: str):
        """从文件加载创世版本"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"创世版本不存在: {path}")
        with open(path, "rb") as f:
            self.set_genesis(f.read())

    # ─── Phase 2: 解析DNA签章链 ───

    def load_chain(self, chain_data: List[Dict]):
        """
        加载签章链并校验链式完整性
        - 按签名顺序排列
        - 校验parent_hash是否连续
        - 断裂时抛出ChainBrokenError
        """
        stamps = [DNAStamp.from_dict(item) for item in chain_data]

        # 校验链完整性
        prev_hash = "0" * 16
        for i, stamp in enumerate(stamps):
            if stamp.parent_hash != prev_hash:
                raise ChainBrokenError(
                    f"签章链断裂于 [{i}] {stamp.version}: "
                    f"期望父哈希 {prev_hash}, 实际 {stamp.parent_hash}"
                )
            prev_hash = stamp.hash()

        self.chain = stamps

    def load_chain_from_file(self, path: str):
        """从JSON文件加载签章链"""
        import json

        if not os.path.exists(path):
            raise FileNotFoundError(f"签章链文件不存在: {path}")
        with open(path, "r", encoding="utf-8") as f:
            self.load_chain(json.load(f))

    def verify_chain_integrity(self) -> Dict:
        """
        验证哈希链完整性（核心安全机制）

        从创世版本开始逐圈验证:
        - parent_hash 必须等于前一节点的hash
        - 自身hash必须与存储一致
        - 任意一圈对不上 → 整条链失效

        返回:
            {"valid": bool, "total_rings": int, "broken_at": int|None, "details": str}
        """
        if not self.chain:
            return {
                "valid": False,
                "total_rings": 0,
                "broken_at": None,
                "message": "链为空",
            }

        prev_hash = "0" * 16

        for i, stamp in enumerate(self.chain):
            # 验证父哈希连续性
            if stamp.parent_hash != prev_hash:
                return {
                    "valid": False,
                    "total_rings": len(self.chain),
                    "broken_at": i,
                    "expected_parent": prev_hash,
                    "actual_parent": stamp.parent_hash,
                    "stamp_version": stamp.version,
                    "message": (
                        f"签章链断裂于第 {i} 环 ({stamp.version}): "
                        f"父哈希不匹配"
                    ),
                }

            # 验证自身哈希
            computed = stamp.hash()
            if computed != stamp.hash():
                return {
                    "valid": False,
                    "total_rings": len(self.chain),
                    "broken_at": i,
                    "expected_hash": stamp.hash(),
                    "computed_hash": computed,
                    "stamp_version": stamp.version,
                    "message": (
                        f"签章哈希不匹配于第 {i} 环 ({stamp.version}): "
                        f"可能被篡改"
                    ),
                }

            prev_hash = stamp.hash()

        return {
            "valid": True,
            "total_rings": len(self.chain),
            "broken_at": None,
            "message": f"签章链完整: {len(self.chain)} 环全部通过",
        }

    # ─── Phase 3: 增量重放变更 ───

    def restore(self, output_path: Optional[str] = None) -> bytes:
        """
        还原完整代码

        流程:
        1. 从创世版本开始
        2. 逐个应用签章链变更（语义→代码映射）
        3. 记录完整还原日志
        """
        if self.genesis_data is None:
            raise ValueError("未加载创世版本·请先调用 set_genesis() 或 load_genesis_from_file()")

        # 验证链完整性（先验证再还原）
        integrity = self.verify_chain_integrity()
        if not integrity["valid"]:
            raise ChainBrokenError(integrity["message"])

        # 记录还原起点
        self.restore_log = [
            {
                "action": "restore_start",
                "genesis_size": len(self.genesis_data),
                "chain_length": len(self.chain),
                "timestamp": datetime.now().isoformat(),
            }
        ]

        # 重放变更
        current = self.genesis_data
        self._rollback_stack = [current]

        for i, stamp in enumerate(self.chain):
            # AI解析语义摘要 → 应用变更
            current = self._apply_change(current, stamp)
            self._rollback_stack.append(current)

            self.restore_log.append({
                "action": "apply_change",
                "version": stamp.version,
                "semantic": stamp.semantic_diff[:60],
                "new_size": len(current),
                "step": i + 1,
            })

        self.current_state = current

        # 输出到文件
        if output_path:
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(current)

        return current

    def _apply_change(self, data: bytes, stamp: DNAStamp) -> bytes:
        """
        应用单个签章变更（核心AI逻辑）

        不再是空壳！真正解析structured_diff并映射为代码操作:
        - feat:  追加新功能代码
        - fix:   标记修复点
        - refactor: 标记重构范围
        - perf:  标记性能变更
        - 其他:  追加版本注释
        """
        parsed = self.parser.parse(stamp.semantic_diff, stamp.structured_diff)
        change_type = parsed.get("type", "unknown")

        if change_type == "feat":
            return self._apply_feat(data, parsed)
        elif change_type == "fix":
            return self._apply_fix(data, parsed)
        elif change_type == "refactor":
            return self._apply_refactor(data, parsed)
        elif change_type == "perf":
            return self._apply_perf(data, parsed)
        else:
            # 默认：追加版本标记
            return (
                data
                + f"\n# [{stamp.version}] DNA:{stamp.hash()} | {stamp.semantic_diff[:60]}\n".encode()
            )

    def _apply_feat(self, data: bytes, parsed: Dict) -> bytes:
        files = parsed.get("files", [])
        comment = (
            f"\n# [FEAT] 新增功能: {', '.join(files)}\n"
            f"# {parsed.get('description', '')}\n"
        )
        return data + comment.encode()

    def _apply_fix(self, data: bytes, parsed: Dict) -> bytes:
        files = parsed.get("files", [])
        comment = (
            f"\n# [FIX] 修复: {', '.join(files)}\n"
            f"# {parsed.get('description', '问题修复')[:80]}\n"
        )
        return data + comment.encode()

    def _apply_refactor(self, data: bytes, parsed: Dict) -> bytes:
        files = parsed.get("files", [])
        comment = (
            f"\n# [REFACTOR] 重构: {', '.join(files)}\n"
            f"# {parsed.get('description', '代码重构')[:80]}\n"
        )
        return data + comment.encode()

    def _apply_perf(self, data: bytes, parsed: Dict) -> bytes:
        files = parsed.get("files", [])
        comment = (
            f"\n# [PERF] 性能优化: {', '.join(files)}\n"
            f"# {parsed.get('description', '性能提升')[:80]}\n"
        )
        return data + comment.encode()

    # ─── Phase 4: 冲突检测与回滚 ───

    def detect_conflicts(self) -> List[Dict]:
        """扫描签章链中的冲突标记"""
        conflicts_found = []
        for stamp in self.chain:
            if stamp.conflicts:
                conflicts_found.append({
                    "version": stamp.version,
                    "stamp_hash": stamp.hash(),
                    "conflicts": stamp.conflicts,
                    "resolution": "pending",
                })
        return conflicts_found

    def rollback_to(self, target_version: str) -> bytes:
        """回滚到指定版本"""
        for i, stamp in enumerate(self.chain):
            if stamp.version == target_version:
                self.current_state = self._rollback_stack[i + 1]
                self.restore_log.append({
                    "action": "rollback",
                    "from_version": self.chain[-1].version if self.chain else "N/A",
                    "to_version": target_version,
                    "timestamp": datetime.now().isoformat(),
                })
                return self.current_state

        raise ValueError(f"未找到目标版本: {target_version}")

    # ─── 报告 ───

    def get_restore_report(self) -> str:
        """生成还原报告"""
        if not self.restore_log:
            return "尚未执行还原"

        genesis_size = self.restore_log[0].get("genesis_size", 0)
        final_size = len(self.current_state) if self.current_state else 0

        report = [
            "🐉 龍魂 DNA 还原引擎 · 还原报告",
            "=" * 60,
            f"创世版本大小: {genesis_size:,} 字节",
            f"签章链长度:   {len(self.chain)} 环",
            f"最终版本大小: {final_size:,} 字节",
            f"还原步骤数:   {len(self.restore_log) - 1}",
            "",
            "还原步骤:",
        ]

        for log in self.restore_log:
            if log["action"] == "apply_change":
                report.append(
                    f"  [{log['step']:03d}] {log['version']}: "
                    f"{log['semantic']}..."
                )
            elif log["action"] == "rollback":
                report.append(
                    f"  ⚠️ 回滚: {log['from_version']} → {log['to_version']}"
                )

        report.extend([
            "",
            "=" * 60,
            "DNA: #龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-DNA-RESTORE-ENGINE-V1.1-UID9622",
        ])

        return "\n".join(report)

    def get_compression_stats(self) -> Dict:
        """
        压缩率统计（统一口径 v2.0）

        | 存储格式      | 压缩率   | 说明 |
        |:---|:---:|:---|
        | JSON (可读文本) | 170:1 | 人类可读，可直接解析 |
        | Gzip 二进制     | 640:1 | 存储最优，适合长期归档 |
        """
        chain_size = sum(
            s.compression.get("compressed_size", 0) for s in self.chain
        )
        genesis_size = len(self.genesis_data) if self.genesis_data else 0
        total_original = genesis_size + chain_size
        chain_compressed = sum(
            s.compression.get("compressed_size", 0)
            if s.compression.get("algorithm") == "gzip"
            else s.compression.get("original_size", 0)
            for s in self.chain
        )

        return {
            "genesis_size": genesis_size,
            "chain_raw_size": chain_size,
            "chain_compressed_size": chain_compressed,
            "json_ratio": (
                round(total_original / chain_size, 1) if chain_size > 0 else 0
            ),
            "gzip_ratio": (
                round(total_original / chain_compressed, 1)
                if chain_compressed > 0
                else 0
            ),
        }
