# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-fe0203d9
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂 · 三才DNA无损压缩与内容指纹溯源框架 v2.0

本框架提供两种工作模式：

【模式A · 无损压缩】（默认）
  原始字节经 zlib 完整封存，三才指纹与 DNA 签章链作为可验证元数据。
  这是“真无损”的数据容器，自带主权锚定与完整性校验。

【模式B · 内容指纹与溯源】
  不压缩数据本体，仅生成天·地·人三才指纹 + DNA 签章链，
  用于文档完整性验证、代码审计、数据流水线监控、数字资产确权等场景。

DNA: #龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-SANCAI-DNA-COMPRESS-v2.0-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
协议: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

用法:
  # 无损压缩
  lh sancai-compress -c input.txt -o output.lhdc --sign

  # 解压
  lh sancai-compress -d output.lhdc -o restored.txt

  # 验证压缩包
  lh sancai-compress -v output.lhdc --verify-sig

  # 生成内容指纹
  lh sancai-compress --fingerprint input.txt --author UID9622

  # 用指纹验证文件完整性
  lh sancai-compress --verify-file input.txt --fingerprint-file input.txt.fingerprint.json

  # 三色审计
  lh sancai-compress --audit input.txt

  # 签章链
  lh sancai-compress --chain input.txt --chain-out chain.json
  lh sancai-compress --verify-chain chain.json
"""

import argparse
import concurrent.futures
import multiprocessing
import hashlib
import json
import math
import os
import re
import struct
import subprocess
import sys
import zlib
from collections import Counter
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ============================================================
# 主权锚定（焊死）
# ============================================================

UID = "UID9622"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
DNA_ENGINE = "#龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-SANCAI-DNA-COMPRESS-v2.0"

# ============================================================
# 文件格式常量（无损压缩模式）
# ============================================================

MAGIC = b"LHDC"
VERSION = 2
HEADER_FMT = "!4sHHHII"
HEADER_SIZE = struct.calcsize(HEADER_FMT)
DEFAULT_CHUNK = 256 * 1024


# ============================================================
# DNA签章链
# ============================================================

@dataclass
class DNANode:
    """DNA签章链节点"""
    version: str
    author: str
    chunk_index: int
    original_offset: int
    chunk_size: int
    chunk_hash: str
    tian_hash: str
    di_hash: str
    ren_hash: str
    operation: str = "compress"
    parent_hash: str = ""
    current_hash: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    signatures: List[Dict[str, str]] = field(default_factory=list)
    note: str = ""

    def compute_hash(self) -> str:
        content = (
            f"{self.version}|{self.author}|{self.chunk_index}|"
            f"{self.original_offset}|{self.chunk_size}|{self.chunk_hash}|"
            f"{self.tian_hash}|{self.di_hash}|{self.ren_hash}|"
            f"{self.operation}|{self.parent_hash}|{self.timestamp}|{self.note}"
        )
        return hashlib.sha256(content.encode()).hexdigest()[:32]

    def finalize(self):
        if not self.current_hash:
            self.current_hash = self.compute_hash()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "author": self.author,
            "timestamp": self.timestamp,
            "chunk_index": self.chunk_index,
            "original_offset": self.original_offset,
            "chunk_size": self.chunk_size,
            "chunk_hash": self.chunk_hash,
            "tian_hash": self.tian_hash,
            "di_hash": self.di_hash,
            "ren_hash": self.ren_hash,
            "operation": self.operation,
            "parent_hash": self.parent_hash,
            "current_hash": self.current_hash,
            "signatures": self.signatures,
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DNANode":
        return cls(
            version=d["version"],
            author=d["author"],
            chunk_index=d.get("chunk_index", 0),
            original_offset=d.get("original_offset", 0),
            chunk_size=d.get("chunk_size", 0),
            chunk_hash=d.get("chunk_hash", ""),
            tian_hash=d.get("tian_hash", ""),
            di_hash=d.get("di_hash", ""),
            ren_hash=d.get("ren_hash", ""),
            operation=d.get("operation", "compress"),
            parent_hash=d.get("parent_hash", ""),
            current_hash=d.get("current_hash", ""),
            timestamp=d.get("timestamp", datetime.now().isoformat()),
            signatures=d.get("signatures", []),
            note=d.get("note", ""),
        )


class DNAChain:
    """DNA签章链"""

    def __init__(self):
        self.nodes: List[DNANode] = []

    def add(self, node: DNANode):
        node.finalize()
        if self.nodes:
            node.parent_hash = self.nodes[-1].current_hash
            node.current_hash = node.compute_hash()
        else:
            node.parent_hash = "0" * 32
            node.current_hash = node.compute_hash()
        self.nodes.append(node)
        return node

    def verify(self) -> Tuple[bool, str]:
        if not self.nodes:
            return False, "链为空"
        prev = "0" * 32
        for i, node in enumerate(self.nodes):
            if node.parent_hash != prev:
                return False, f"节点 {i} 父哈希断裂 (期望 {prev}, 实际 {node.parent_hash})"
            if node.compute_hash() != node.current_hash:
                return False, f"节点 {i} 当前哈希不匹配"
            prev = node.current_hash
        return True, f"链完整，共 {len(self.nodes)} 个节点"

    def to_dicts(self) -> List[Dict[str, Any]]:
        return [n.to_dict() for n in self.nodes]

    @classmethod
    def from_dicts(cls, ds: List[Dict[str, Any]]) -> "DNAChain":
        chain = cls()
        for d in ds:
            chain.nodes.append(DNANode.from_dict(d))
        return chain

    def to_chain_json(self) -> str:
        ok, msg = self.verify()
        return json.dumps(
            {
                "chain_length": len(self.nodes),
                "last_hash": self.nodes[-1].current_hash if self.nodes else "",
                "verification": msg,
                "nodes": self.to_dicts(),
            },
            ensure_ascii=False,
            indent=2,
        )


# ============================================================
# 三才特征提取器（v2.0 增强）
# ============================================================

class SancaiExtractor:
    """天·地·人 三才指纹提取器"""

    def __init__(self):
        self.tian_weight = 0.34
        self.di_weight = 0.33
        self.ren_weight = 0.33

    def _decode_text(self, data: bytes) -> str:
        return data.decode("utf-8", errors="ignore")

    def extract_tian(self, data: bytes) -> Dict[str, Any]:
        """天·语义特征：词频、熵、主题签名"""
        text = self._decode_text(data)
        words = re.findall(r"[\u4e00-\u9fa5a-zA-Z0-9]+", text)
        total_chars = max(len(text), 1)

        word_count = len(words)
        unique_words = len(set(w.lower() for w in words))

        char_freq = Counter(text)
        top_chars = dict(char_freq.most_common(10))
        chinese_ratio = sum(1 for c in text if "\u4e00" <= c <= "\u9fff") / total_chars

        # 香农熵：H = log2(N) - (1/N) * sum(c * log2(c))
        # 减少浮点除法次数
        acc = 0.0
        for count in char_freq.values():
            if count:
                acc += count * math.log2(count)
        entropy = math.log2(total_chars) - acc / total_chars

        semantic_content = f"{text[:1000]}|{word_count}|{unique_words}|{chinese_ratio:.4f}|{entropy:.4f}"
        semantic_hash = hashlib.sha256(semantic_content.encode()).hexdigest()

        return {
            "type": "天·语义",
            "word_count": word_count,
            "char_count": total_chars,
            "unique_words": unique_words,
            "unique_ratio": round(unique_words / max(word_count, 1), 6),
            "avg_word_len": round(sum(len(w) for w in words) / max(word_count, 1), 2),
            "chinese_ratio": round(chinese_ratio, 4),
            "entropy": round(entropy, 4),
            "top_chars": top_chars,
            "semantic_hash": semantic_hash[:16],
            "full_hash": semantic_hash,
        }

    def extract_di(self, data: bytes) -> Dict[str, Any]:
        """地·结构特征：句段、标点、格式骨架"""
        text = self._decode_text(data)
        sentences = [s.strip() for s in re.split(r"[。！？\n\r]+", text) if s.strip()]
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        lines = [l.strip() for l in text.split("\n") if l.strip()]

        punctuation = {
            "period": text.count("。"),
            "comma": text.count("，"),
            "exclamation": text.count("！"),
            "question": text.count("？"),
            "semicolon": text.count("；"),
            "colon": text.count("："),
            "quote": text.count("\"") + text.count("\""),
            "parentheses": text.count("(") + text.count(")"),
        }

        structure_content = (
            f"{len(sentences)}|{len(paragraphs)}|{len(lines)}|{len(data)}|"
            f"{text[:500]}|{json.dumps(punctuation, sort_keys=True)}"
        )
        structure_hash = hashlib.sha256(structure_content.encode()).hexdigest()

        return {
            "type": "地·结构",
            "byte_length": len(data),
            "sentence_count": len(sentences),
            "paragraph_count": len(paragraphs),
            "line_count": len(lines),
            "avg_sentence_len": round(sum(len(s) for s in sentences) / max(len(sentences), 1), 2),
            "punctuation": punctuation,
            "structure_hash": structure_hash[:16],
            "full_hash": structure_hash,
        }

    def extract_ren(self, data: bytes, author: Optional[str] = None) -> Dict[str, Any]:
        """人·行为特征：作者主权、操作轨迹、内容指纹"""
        text = self._decode_text(data)
        hostname = os.uname().nodename if hasattr(os, "uname") else "unknown"
        now = datetime.now().isoformat()

        # 直接在 bytes 上统计非 ASCII，避免对每个字符调 ord()
        non_ascii_bytes = sum(1 for b in data if b > 127)
        complexity = {
            "size_kb": round(len(data) / 1024, 4),
            "size_mb": round(len(data) / (1024 * 1024), 6),
            "lines": text.count("\n") + 1,
            "non_ascii_ratio": round(non_ascii_bytes / max(len(data), 1), 4),
        }

        behavior_content = f"{author or UID}|{hostname}|{now}|{len(data)}|{data[:256].hex()}"
        behavior_hash = hashlib.sha256(behavior_content.encode()).hexdigest()

        return {
            "type": "人·行为",
            "author": author or UID,
            "host": hostname,
            "timestamp": now,
            "dna": f"{DNA_ENGINE}-BEHAVIOR-{UID}",
            "complexity": complexity,
            "content_hash": hashlib.sha256(data).hexdigest()[:16],
            "head_sample": data[:64].hex(),
            "tail_sample": data[-64:].hex() if len(data) >= 64 else "",
            "behavior_hash": behavior_hash[:16],
            "full_hash": behavior_hash,
        }

    def extract_all(self, data: bytes, author: Optional[str] = None) -> Dict[str, Any]:
        return {
            "tian": self.extract_tian(data),
            "di": self.extract_di(data),
            "ren": self.extract_ren(data, author),
            "weights": {"天": self.tian_weight, "地": self.di_weight, "人": self.ren_weight},
            "data_hash": hashlib.sha256(data).hexdigest(),
            "data_size": len(data),
        }


# ============================================================
# 三色审计引擎
# ============================================================

class TricolorAuditEngine:
    """三色审计引擎"""

    @staticmethod
    def audit(data: bytes, features: Optional[Dict[str, Any]] = None, chain: Optional[DNAChain] = None) -> Dict[str, Any]:
        data_hash = hashlib.sha256(data).hexdigest()
        dimensions: Dict[str, float] = {}
        details: List[str] = []

        # 完整性
        if features and features.get("data_hash"):
            if features["data_hash"] == data_hash:
                dimensions["完整性"] = 100.0
                details.append("✅ 数据哈希匹配")
            else:
                dimensions["完整性"] = 0.0
                details.append("❌ 数据哈希不匹配，数据被篡改")
        else:
            dimensions["完整性"] = 50.0
            details.append("⚠️ 未提供指纹，完整性无法判定")

        # 语义丰富度
        if features and features.get("tian"):
            entropy = features["tian"].get("entropy", 0)
            score = min(100.0, entropy * 8)
            dimensions["语义丰富度"] = round(score, 2)
            details.append(f"{'✅' if score >= 60 else '🟡'} 语义熵 {entropy:.2f}")
        else:
            dimensions["语义丰富度"] = 0.0

        # 结构规范性
        if features and features.get("di"):
            di = features["di"]
            if di.get("sentence_count", 0) > 0 or di.get("line_count", 0) > 0:
                dimensions["结构规范性"] = 90.0
                details.append("✅ 结构骨架可识别")
            else:
                dimensions["结构规范性"] = 30.0
                details.append("🟡 结构信息较弱")
        else:
            dimensions["结构规范性"] = 0.0

        # 链完整性
        if chain and chain.nodes:
            valid, msg = chain.verify()
            if valid:
                dimensions["签章链完整性"] = 100.0
                details.append(f"✅ {msg}")
            else:
                dimensions["签章链完整性"] = 0.0
                details.append(f"❌ {msg}")
        else:
            dimensions["签章链完整性"] = 0.0
            details.append("⚠️ 无签章链")

        # 主权锚定
        if features and features.get("ren"):
            author = features["ren"].get("author", "")
            if UID in author:
                dimensions["主权锚定"] = 100.0
                details.append(f"✅ 主权锚定 {UID}")
            else:
                dimensions["主权锚定"] = 60.0
                details.append(f"🟡 作者 {author}")
        else:
            dimensions["主权锚定"] = 0.0

        R = sum(dimensions.values()) / len(dimensions) if dimensions else 50.0

        if R >= 85:
            tricolor = "🟢"
            status = "通过"
        elif R >= 60:
            tricolor = "🟡"
            status = "警告"
        else:
            tricolor = "🔴"
            status = "异常"

        return {
            "score": round(R, 2),
            "tricolor": tricolor,
            "status": status,
            "dimensions": dimensions,
            "details": details,
            "dna": f"{DNA_ENGINE}-AUDIT-{UID}",
            "timestamp": datetime.now().isoformat(),
        }


# ============================================================
# 并行工作函数（必须模块顶层，便于多进程 pickling）
# ============================================================

def _extract_chunk_features(args: Tuple[int, int, bytes, str]) -> Tuple[int, int, bytes, Dict[str, Any]]:
    """多进程工作函数：提取单个分块的三才特征

    返回: (chunk_index, original_offset, chunk_bytes, features)
    """
    idx, offset, chunk, author = args
    extractor = SancaiExtractor()
    features = extractor.extract_all(chunk, author)
    return idx, offset, chunk, features


# ============================================================
# 三才DNA引擎（v2.0 统一入口）
# ============================================================

class SancaiDNAEngine:
    """三才DNA无损压缩与内容指纹溯源引擎 v2.0"""

    def __init__(self, level: int = 6, chunk_size: int = DEFAULT_CHUNK, jobs: int = 0):
        if not 1 <= level <= 9:
            raise ValueError("压缩级别必须在 1-9 之间")
        self.level = level
        self.chunk_size = chunk_size
        self.jobs = jobs if jobs > 0 else max(1, os.cpu_count() or 1)
        self.extractor = SancaiExtractor()
        self.auditor = TricolorAuditEngine()

    # ── 无损压缩 ──

    def compress(self, data: bytes, author: str = UID, operation: str = "compress") -> bytes:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data 必须是 bytes 类型")

        original_crc32 = zlib.crc32(data) & 0xFFFFFFFF
        original_hash = hashlib.sha256(data).hexdigest()
        original_size = len(data)

        chain = DNAChain()
        chunk_count = max((original_size + self.chunk_size - 1) // self.chunk_size, 1)

        # 分块并行提取三才特征
        # 自动调大分块：保证每个 worker 大约处理 4 个块，降低调度开销
        effective_chunk_size = max(self.chunk_size, len(data) // (self.jobs * 4))
        effective_chunk_size = max(effective_chunk_size, 64 * 1024)  # 最小 64KB

        work_items = []
        for idx, offset in enumerate(range(0, len(data), effective_chunk_size)):
            chunk = data[offset:offset + effective_chunk_size]
            work_items.append((idx, offset, chunk, author))
        chunk_count = len(work_items)

        if self.jobs > 1 and chunk_count > 1:
            # macOS 默认 spawn 慢且对 <stdin> 不友好，优先用 fork
            try:
                ctx = multiprocessing.get_context("fork")
            except ValueError:
                ctx = multiprocessing.get_context("spawn")
            try:
                with concurrent.futures.ProcessPoolExecutor(max_workers=self.jobs, mp_context=ctx) as executor:
                    results = list(executor.map(_extract_chunk_features, work_items))
            except Exception:
                # 任何并行异常都回退到串行，保证可用性
                results = [_extract_chunk_features(item) for item in work_items]
        else:
            results = [_extract_chunk_features(item) for item in work_items]

        # 按 chunk_index 排序，确保 DNA 链顺序正确
        results.sort(key=lambda x: x[0])

        for idx, offset, chunk, features in results:
            node = DNANode(
                version="2.0.0",
                author=author,
                chunk_index=idx,
                original_offset=offset,
                chunk_size=len(chunk),
                chunk_hash=hashlib.sha256(chunk).hexdigest()[:32],
                tian_hash=features["tian"]["semantic_hash"],
                di_hash=features["di"]["structure_hash"],
                ren_hash=features["ren"]["behavior_hash"],
                operation=operation,
            )
            chain.add(node)

        payload = zlib.compress(data, self.level)

        metadata = {
            "magic": MAGIC.decode("ascii"),
            "version": VERSION,
            "level": self.level,
            "chunk_count": chunk_count,
            "chunk_size": effective_chunk_size,
            "original_size": original_size,
            "original_crc32": original_crc32,
            "original_hash": original_hash,
            "payload_size": len(payload),
            "hash_algorithm": "SHA256",
            "compression_engine": "zlib+三才DNA",
            "timestamp": datetime.now().isoformat(),
            "dna": f"{DNA_ENGINE}-{operation}-{UID}",
            "confirm": CONFIRM_CODE,
            "gpg": GPG_KEY,
            "tricolor": "🟢",
            "author": author,
        }

        package = {"metadata": metadata, "chain": chain.to_dicts()}
        meta_json = json.dumps(package, ensure_ascii=False).encode("utf-8")

        header = struct.pack(HEADER_FMT, MAGIC, VERSION, self.level, chunk_count, original_crc32, len(payload))
        return header + struct.pack("!I", len(meta_json)) + meta_json + payload

    def decompress(self, compressed: bytes) -> bytes:
        if len(compressed) < HEADER_SIZE + 4:
            raise ValueError("文件过小，不是有效的 LHDC 格式")

        header = compressed[:HEADER_SIZE]
        magic, version, level, chunk_count, original_crc32, payload_len = struct.unpack(HEADER_FMT, header)
        if magic != MAGIC:
            raise ValueError(f"无效的 Magic: {magic!r}")
        if version != VERSION:
            raise ValueError(f"不支持的版本: {version}")

        meta_len = struct.unpack("!I", compressed[HEADER_SIZE:HEADER_SIZE + 4])[0]
        meta_start = HEADER_SIZE + 4
        meta_end = meta_start + meta_len
        if meta_end > len(compressed):
            raise ValueError("元数据长度超出文件范围")

        package = json.loads(compressed[meta_start:meta_end].decode("utf-8"))
        payload = compressed[meta_end:meta_end + payload_len]
        if len(payload) != payload_len:
            raise ValueError("payload 长度不匹配")

        data = zlib.decompress(payload)

        if (zlib.crc32(data) & 0xFFFFFFFF) != original_crc32:
            raise ValueError("CRC32 校验失败，数据可能损坏")
        if hashlib.sha256(data).hexdigest() != package["metadata"]["original_hash"]:
            raise ValueError("SHA256 校验失败，数据可能损坏")

        return data

    def verify_package(self, compressed: bytes) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        try:
            header = compressed[:HEADER_SIZE]
            magic, version, level, chunk_count, original_crc32, payload_len = struct.unpack(HEADER_FMT, header)
            if magic != MAGIC:
                return False, "Magic 不匹配", None
            if version != VERSION:
                return False, f"版本不匹配: {version}", None

            meta_len = struct.unpack("!I", compressed[HEADER_SIZE:HEADER_SIZE + 4])[0]
            meta_end = HEADER_SIZE + 4 + meta_len
            package = json.loads(compressed[HEADER_SIZE + 4:meta_end].decode("utf-8"))

            chain = DNAChain.from_dicts(package["chain"])
            ok, msg = chain.verify()
            if not ok:
                return False, f"DNA链验证失败: {msg}", package

            payload = compressed[meta_end:meta_end + payload_len]
            if len(payload) != payload_len:
                return False, "payload 长度不匹配", package

            data = zlib.decompress(payload)
            if (zlib.crc32(data) & 0xFFFFFFFF) != original_crc32:
                return False, "CRC32 校验失败", package
            if hashlib.sha256(data).hexdigest() != package["metadata"]["original_hash"]:
                return False, "SHA256 校验失败", package

            return True, "三才DNA压缩包验证通过", package
        except Exception as e:
            return False, f"验证异常: {e}", None

    def package_info(self, compressed: bytes) -> Dict[str, Any]:
        ok, msg, package = self.verify_package(compressed)
        if not ok:
            raise ValueError(msg)
        meta = package["metadata"]
        chain = DNAChain.from_dicts(package["chain"])
        ratio = meta["original_size"] / max(len(compressed), 1)
        return {
            "magic": meta["magic"],
            "version": meta["version"],
            "level": meta["level"],
            "chunk_count": meta["chunk_count"],
            "original_size": meta["original_size"],
            "compressed_size": len(compressed),
            "payload_size": meta["payload_size"],
            "compression_ratio": round(ratio, 4),
            "original_hash": meta["original_hash"],
            "original_crc32": meta["original_crc32"],
            "timestamp": meta["timestamp"],
            "dna": meta["dna"],
            "confirm": meta["confirm"],
            "gpg": meta["gpg"],
            "tricolor": meta["tricolor"],
            "chain_status": chain.verify()[1],
        }

    # ── 内容指纹与溯源 ──

    def fingerprint(self, data: bytes, author: str = UID, operation: str = "fingerprint", note: str = "") -> Dict[str, Any]:
        features = self.extractor.extract_all(data, author)
        chain = DNAChain()
        node = DNANode(
            version="2.0.0",
            author=author,
            chunk_index=0,
            original_offset=0,
            chunk_size=len(data),
            chunk_hash=features["data_hash"][:32],
            tian_hash=features["tian"]["semantic_hash"],
            di_hash=features["di"]["structure_hash"],
            ren_hash=features["ren"]["behavior_hash"],
            operation=operation,
            note=note,
        )
        chain.add(node)

        return {
            "fingerprint": features,
            "chain": chain.to_dicts(),
            "dna": f"{DNA_ENGINE}-FINGERPRINT-{UID}",
            "confirm": CONFIRM_CODE,
            "gpg": GPG_KEY,
            "tricolor": "🟢",
            "timestamp": datetime.now().isoformat(),
        }

    def verify_fingerprint(self, data: bytes, fingerprint: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        current_hash = hashlib.sha256(data).hexdigest()
        stored_hash = fingerprint.get("fingerprint", {}).get("data_hash", "")

        if stored_hash and current_hash == stored_hash:
            return True, {"status": "✅ 数据完整", "hash_match": True, "tricolor": "🟢"}
        return False, {
            "status": "❌ 数据被篡改或指纹不匹配",
            "hash_match": False,
            "stored_hash": stored_hash[:16] if stored_hash else "",
            "current_hash": current_hash[:16],
            "tricolor": "🔴",
        }

    def audit(self, data: bytes, fingerprint: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        features = fingerprint.get("fingerprint") if fingerprint else None
        chain = None
        if fingerprint and fingerprint.get("chain"):
            chain = DNAChain.from_dicts(fingerprint["chain"])
        return self.auditor.audit(data, features, chain)

    def chain_from_fingerprint(self, fingerprint: Dict[str, Any]) -> DNAChain:
        if not fingerprint.get("chain"):
            raise ValueError("指纹中无签章链")
        return DNAChain.from_dicts(fingerprint["chain"])


# ============================================================
# GPG 签名辅助
# ============================================================

def gpg_sign_file(file_path: str, key_id: str = GPG_KEY) -> str:
    asc_path = file_path + ".asc"
    cmd = ["gpg", "--batch", "--yes", "--detach-sign", "--armor", "-u", key_id, "-o", asc_path, file_path]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return asc_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"GPG 签名失败: {e.stderr}") from e


def gpg_verify_file(file_path: str) -> Tuple[bool, str]:
    asc_path = file_path + ".asc"
    if not Path(asc_path).exists():
        return False, f"签名文件不存在: {asc_path}"
    cmd = ["gpg", "--verify", asc_path, file_path]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True, result.stderr or "签名有效"
    except subprocess.CalledProcessError as e:
        return False, e.stderr or "签名验证失败"


# ============================================================
# 命令行接口
# ============================================================

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 三才DNA无损压缩与内容指纹溯源框架 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
模式A · 无损压缩:
  lh sancai-compress -c input.txt -o output.lhdc --sign
  lh sancai-compress -d output.lhdc -o restored.txt
  lh sancai-compress -v output.lhdc --verify-sig
  lh sancai-compress --info output.lhdc

模式B · 内容指纹与溯源:
  lh sancai-compress --fingerprint input.txt --author UID9622
  lh sancai-compress --verify-file input.txt --fingerprint-file input.txt.fingerprint.json
  lh sancai-compress --audit input.txt
  lh sancai-compress --chain input.txt --chain-out chain.json
  lh sancai-compress --verify-chain chain.json
        """,
    )

    # 压缩模式
    parser.add_argument("-c", "--compress", metavar="FILE", help="压缩文件为 .lhdc")
    parser.add_argument("-d", "--decompress", metavar="FILE", help="解压 .lhdc 文件")
    parser.add_argument("-v", "--verify", metavar="FILE", help="验证 .lhdc 压缩包")
    parser.add_argument("--info", metavar="FILE", help="查看 .lhdc 压缩包信息")

    # 指纹模式
    parser.add_argument("--fingerprint", metavar="FILE", help="生成内容指纹 (.fingerprint.json)")
    parser.add_argument("--verify-file", metavar="FILE", help="用指纹验证文件完整性")
    parser.add_argument("--fingerprint-file", metavar="FILE", help="指纹文件路径")

    # 审计与链
    parser.add_argument("--audit", metavar="FILE", help="执行三色审计")
    parser.add_argument("--chain", metavar="FILE", help="生成 DNA 签章链")
    parser.add_argument("--chain-out", metavar="FILE", help="签章链输出路径")
    parser.add_argument("--verify-chain", metavar="FILE", help="验证签章链文件")

    # 通用
    parser.add_argument("-o", "--output", metavar="FILE", help="输出文件")
    parser.add_argument("-l", "--level", type=int, default=6, choices=range(1, 10), help="压缩级别 1-9 (默认6)")
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK, help=f"分块大小 (默认{DEFAULT_CHUNK})")
    parser.add_argument("-j", "--jobs", type=int, default=0, help="并行工作进程数，0=自动检测 CPU 核心数")
    parser.add_argument("--author", default=UID, help="作者标识")
    parser.add_argument("--sign", action="store_true", help="压缩后自动 GPG 签名")
    parser.add_argument("--verify-sig", action="store_true", help="同时验证 GPG 签名")
    parser.add_argument("--note", default="", help="签章链节点备注")

    args = parser.parse_args(argv)
    engine = SancaiDNAEngine(level=args.level, chunk_size=args.chunk_size, jobs=args.jobs)

    # ── 压缩模式 ──
    if args.compress:
        with open(args.compress, "rb") as f:
            data = f.read()
        compressed = engine.compress(data, author=args.author)
        output_path = args.output or args.compress + ".lhdc"
        with open(output_path, "wb") as f:
            f.write(compressed)

        info = engine.package_info(compressed)
        print(f"✅ 三才DNA压缩完成")
        print(f"   原始大小: {info['original_size']:,} bytes")
        print(f"   压缩大小: {info['compressed_size']:,} bytes")
        print(f"   压缩率:   {info['compression_ratio']:.2f}x")
        print(f"   分块数:   {info['chunk_count']}")
        print(f"   DNA链:    {info['chain_status']}")
        print(f"   DNA:      {info['dna']}")
        print(f"   输出:     {output_path}")

        if args.sign:
            asc_path = gpg_sign_file(output_path)
            print(f"   GPG签名:  {asc_path}")
        return 0

    if args.decompress:
        with open(args.decompress, "rb") as f:
            compressed = f.read()
        data = engine.decompress(compressed)
        output_path = args.output or args.decompress.replace(".lhdc", "_restored.bin")
        with open(output_path, "wb") as f:
            f.write(data)
        print(f"✅ 解压完成: {output_path} ({len(data):,} bytes)")
        return 0

    if args.verify:
        with open(args.verify, "rb") as f:
            compressed = f.read()
        ok, msg, _ = engine.verify_package(compressed)
        print(f"{'✅' if ok else '🔴'} {msg}")
        if args.verify_sig:
            sig_ok, sig_msg = gpg_verify_file(args.verify)
            print(f"{'✅' if sig_ok else '🔴'} GPG: {sig_msg}")
        return 0 if ok else 1

    if args.info:
        with open(args.info, "rb") as f:
            compressed = f.read()
        info = engine.package_info(compressed)
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return 0

    # ── 指纹模式 ──
    if args.fingerprint:
        with open(args.fingerprint, "rb") as f:
            data = f.read()
        result = engine.fingerprint(data, author=args.author, note=args.note)
        output_path = args.output or args.fingerprint + ".fingerprint.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✅ 三才指纹已生成: {output_path}")
        print(f"   数据哈希: {result['fingerprint']['data_hash'][:16]}...")
        print(f"   语义哈希: {result['fingerprint']['tian']['semantic_hash']}")
        print(f"   结构哈希: {result['fingerprint']['di']['structure_hash']}")
        print(f"   行为哈希: {result['fingerprint']['ren']['behavior_hash']}")
        print(f"   DNA:      {result['dna']}")
        return 0

    if args.verify_file:
        if not args.fingerprint_file:
            print("❌ 请指定 --fingerprint-file")
            return 1
        with open(args.verify_file, "rb") as f:
            data = f.read()
        with open(args.fingerprint_file, "r", encoding="utf-8") as f:
            fp = json.load(f)
        ok, result = engine.verify_fingerprint(data, fp)
        print(f"{result['status']}")
        print(f"   三色: {result['tricolor']}")
        if not ok:
            print(f"   存储哈希: {result.get('stored_hash', '')}")
            print(f"   当前哈希: {result.get('current_hash', '')}")
        return 0 if ok else 1

    # ── 审计与链 ──
    if args.audit:
        with open(args.audit, "rb") as f:
            data = f.read()
        fp = None
        fp_path = args.fingerprint_file or args.audit + ".fingerprint.json"
        if Path(fp_path).exists():
            with open(fp_path, "r", encoding="utf-8") as f:
                fp = json.load(f)
        report = engine.audit(data, fp)
        print(f"\n🔍 三色审计报告")
        print("=" * 40)
        print(f"  三色: {report['tricolor']}")
        print(f"  R值:  {report['score']}")
        print(f"  状态: {report['status']}")
        print(f"  DNA:  {report['dna']}")
        print("\n  各维度得分:")
        for dim, score in report["dimensions"].items():
            bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))
            print(f"    {dim}: {score:5.1f} {bar}")
        if report["details"]:
            print("\n  详情:")
            for detail in report["details"]:
                print(f"    {detail}")
        print("=" * 40)
        return 0

    if args.chain:
        with open(args.chain, "rb") as f:
            data = f.read()
        features = engine.extractor.extract_all(data, args.author)
        chain = DNAChain()
        node = DNANode(
            version="2.0.0",
            author=args.author,
            chunk_index=0,
            original_offset=0,
            chunk_size=len(data),
            chunk_hash=features["data_hash"][:32],
            tian_hash=features["tian"]["semantic_hash"],
            di_hash=features["di"]["structure_hash"],
            ren_hash=features["ren"]["behavior_hash"],
            operation="chain_init",
            note=args.note,
        )
        chain.add(node)
        output_path = args.chain_out or args.chain + ".chain.json"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(chain.to_chain_json())
        print(f"✅ DNA签章链已生成: {output_path}")
        print(f"   链长度: {len(chain.nodes)}")
        print(f"   最后哈希: {chain.nodes[-1].current_hash}")
        return 0

    if args.verify_chain:
        with open(args.verify_chain, "r", encoding="utf-8") as f:
            chain_data = json.load(f)
        nodes = chain_data.get("nodes", chain_data)
        chain = DNAChain.from_dicts(nodes)
        ok, msg = chain.verify()
        print(f"{'✅' if ok else '🔴'} {msg}")
        return 0 if ok else 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
