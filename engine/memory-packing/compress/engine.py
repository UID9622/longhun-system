#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗜️ 智能压缩引擎 · Smart Compression Engine
DNA: #龍芯⚡️2026-05-22-COMPRESS-ENGINE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

智能压缩引擎特性：
1. 多算法自适应选择（zlib/lzma/bz2）
2. 内容类型感知（文本/二进制/图片）
3. 压缩比优先 vs 速度优先
4. 分块压缩支持大文件
5. 完整性校验（SHA256）
"""

import hashlib
import zlib
import lzma
import bz2
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Tuple, Dict, Any


class CompressionLevel(Enum):
    """压缩级别"""
    NONE = 0        # 不压缩
    FAST = 1        # 快速压缩（牺牲压缩比）
    BALANCED = 5    # 平衡（默认）
    BEST = 9        # 最佳压缩（牺牲速度）


class CompressionAlgo(Enum):
    """压缩算法"""
    NONE = "none"       # 不压缩
    ZLIB = "zlib"       # zlib (deflate)
    LZMA = "lzma"       # LZMA (xz)
    BZ2 = "bz2"         # bzip2
    AUTO = "auto"       # 自动选择


@dataclass
class CompressionResult:
    """压缩结果"""
    original_size: int
    compressed_size: int
    algorithm: str
    level: int
    checksum: str           # 原始数据的SHA256
    compressed_checksum: str  # 压缩后数据的SHA256
    ratio: float            # 压缩比 (compressed/original)
    time_ms: float          # 压缩耗时（毫秒）
    data: bytes             # 压缩后的数据

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_size": self.original_size,
            "compressed_size": self.compressed_size,
            "algorithm": self.algorithm,
            "level": self.level,
            "checksum": self.checksum,
            "compressed_checksum": self.compressed_checksum,
            "ratio": self.ratio,
            "time_ms": self.time_ms,
        }


class CompressionEngine:
    """
    智能压缩引擎

    根据内容类型和用户偏好自动选择最优压缩策略
    """

    # 已经压缩的文件类型（不需要再压缩）
    PRECOMPRESSED_TYPES = {
        'image/png', 'image/jpeg', 'image/gif', 'image/webp',
        'video/mp4', 'video/webm',
        'audio/mp3', 'audio/aac', 'audio/ogg',
        'application/zip', 'application/gzip', 'application/x-rar-compressed',
        'application/pdf',
    }

    # 文本类型（压缩效果好）
    TEXT_TYPES = {
        'text/plain', 'text/html', 'text/css', 'text/javascript',
        'text/markdown', 'text/x-python', 'application/json',
        'application/xml', 'application/javascript',
    }

    def __init__(self, default_level: CompressionLevel = CompressionLevel.BALANCED):
        self.default_level = default_level
        self.stats = {
            "total_compressed": 0,
            "total_original": 0,
            "total_saved": 0,
        }

    def select_algorithm(self, data: bytes, content_type: str) -> CompressionAlgo:
        """
        根据内容类型和数据特征选择最优算法

        策略：
        - 已压缩格式 → NONE
        - 小文件(<1KB) → ZLIB（快速）
        - 文本类型 → LZMA（高压缩比）
        - 大文件(>1MB) → LZMA
        - 其他 → ZLIB
        """
        # 已压缩格式不再压缩
        if content_type in self.PRECOMPRESSED_TYPES:
            return CompressionAlgo.NONE

        size = len(data)

        # 小文件用快速算法
        if size < 1024:
            return CompressionAlgo.ZLIB

        # 文本类型用高压缩比算法
        if content_type in self.TEXT_TYPES:
            return CompressionAlgo.LZMA

        # 大文件用高压缩比算法
        if size > 1024 * 1024:
            return CompressionAlgo.LZMA

        # 默认用 zlib
        return CompressionAlgo.ZLIB

    def compress(self,
                 data: bytes,
                 content_type: str = "application/octet-stream",
                 algorithm: CompressionAlgo = CompressionAlgo.AUTO,
                 level: Optional[CompressionLevel] = None) -> CompressionResult:
        """
        压缩数据

        Args:
            data: 原始数据
            content_type: MIME类型
            algorithm: 压缩算法（AUTO自动选择）
            level: 压缩级别

        Returns:
            压缩结果
        """
        import time
        start = time.time()

        original_size = len(data)
        original_checksum = hashlib.sha256(data).hexdigest()

        if level is None:
            level = self.default_level

        # 自动选择算法
        if algorithm == CompressionAlgo.AUTO:
            algorithm = self.select_algorithm(data, content_type)

        # 执行压缩
        if algorithm == CompressionAlgo.NONE:
            compressed = data
        elif algorithm == CompressionAlgo.ZLIB:
            compressed = zlib.compress(data, level.value)
        elif algorithm == CompressionAlgo.LZMA:
            compressed = lzma.compress(data, preset=level.value)
        elif algorithm == CompressionAlgo.BZ2:
            compressed = bz2.compress(data, compresslevel=level.value)
        else:
            compressed = data

        compressed_size = len(compressed)
        compressed_checksum = hashlib.sha256(compressed).hexdigest()
        elapsed = (time.time() - start) * 1000

        # 如果压缩后更大，保留原数据
        if compressed_size >= original_size and algorithm != CompressionAlgo.NONE:
            compressed = data
            compressed_size = original_size
            compressed_checksum = original_checksum
            algorithm = CompressionAlgo.NONE

        ratio = compressed_size / original_size if original_size > 0 else 1.0

        # 更新统计
        self.stats["total_compressed"] += compressed_size
        self.stats["total_original"] += original_size
        self.stats["total_saved"] += (original_size - compressed_size)

        return CompressionResult(
            original_size=original_size,
            compressed_size=compressed_size,
            algorithm=algorithm.value,
            level=level.value,
            checksum=original_checksum,
            compressed_checksum=compressed_checksum,
            ratio=ratio,
            time_ms=elapsed,
            data=compressed
        )

    def decompress(self,
                   data: bytes,
                   algorithm: str,
                   expected_checksum: Optional[str] = None) -> Tuple[bytes, bool]:
        """
        解压数据

        Args:
            data: 压缩数据
            algorithm: 压缩算法名称
            expected_checksum: 期望的原始数据SHA256（用于校验）

        Returns:
            (解压后的数据, 校验是否通过)
        """
        if algorithm == "none":
            decompressed = data
        elif algorithm == "zlib":
            decompressed = zlib.decompress(data)
        elif algorithm == "lzma":
            decompressed = lzma.decompress(data)
        elif algorithm == "bz2":
            decompressed = bz2.decompress(data)
        else:
            raise ValueError(f"不支持的算法: {algorithm}")

        # 校验
        if expected_checksum:
            actual = hashlib.sha256(decompressed).hexdigest()
            return decompressed, actual == expected_checksum

        return decompressed, True

    def get_stats(self) -> Dict[str, Any]:
        """获取压缩统计"""
        total_orig = self.stats["total_original"]
        total_comp = self.stats["total_compressed"]
        return {
            "total_original_bytes": total_orig,
            "total_compressed_bytes": total_comp,
            "total_saved_bytes": self.stats["total_saved"],
            "overall_ratio": total_comp / total_orig if total_orig > 0 else 1.0,
            "savings_percent": (1 - total_comp / total_orig) * 100 if total_orig > 0 else 0,
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-COMPRESS-STATS"
        }


# 全局实例
_engine: Optional[CompressionEngine] = None


def get_engine() -> CompressionEngine:
    """获取全局压缩引擎"""
    global _engine
    if _engine is None:
        _engine = CompressionEngine()
    return _engine


def compress(data: bytes,
             content_type: str = "application/octet-stream",
             level: CompressionLevel = CompressionLevel.BALANCED) -> CompressionResult:
    """便捷压缩函数"""
    return get_engine().compress(data, content_type, level=level)


def decompress(data: bytes,
               algorithm: str,
               checksum: Optional[str] = None) -> Tuple[bytes, bool]:
    """便捷解压函数"""
    return get_engine().decompress(data, algorithm, checksum)


if __name__ == "__main__":
    # 测试
    print("🗜️ 智能压缩引擎测试")
    print("=" * 60)

    engine = CompressionEngine()

    # 测试文本压缩
    text = "龍魂系统是我一年心血的结晶。" * 100
    text_bytes = text.encode('utf-8')
    print(f"原始文本: {len(text_bytes)} 字节")

    result = engine.compress(text_bytes, "text/plain")
    print(f"压缩后: {result.compressed_size} 字节")
    print(f"算法: {result.algorithm}")
    print(f"压缩比: {result.ratio:.2%}")
    print(f"节省: {(1 - result.ratio) * 100:.1f}%")
    print(f"耗时: {result.time_ms:.2f}ms")
    print()

    # 解压验证
    decompressed, ok = engine.decompress(
        result.data, result.algorithm, result.checksum
    )
    print(f"解压验证: {'✅ 通过' if ok else '❌ 失败'}")
    print(f"解压后大小: {len(decompressed)} 字节")
    print()

    # 测试不同内容类型
    print("📊 不同内容类型测试:")
    test_cases = [
        ("text/plain", "龍魂龍魂龍魂" * 500),
        ("application/json", '{"key": "value", "array": [1,2,3]}' * 100),
        ("text/markdown", "# 标题\n\n段落内容" * 200),
    ]

    for content_type, content in test_cases:
        data = content.encode('utf-8')
        result = engine.compress(data, content_type)
        print(f"  {content_type}: {len(data)}→{result.compressed_size} ({result.algorithm}, {result.ratio:.1%})")

    print()
    print("📈 总体统计:")
    stats = engine.get_stats()
    print(f"  总原始: {stats['total_original_bytes']} 字节")
    print(f"  总压缩: {stats['total_compressed_bytes']} 字节")
    print(f"  总节省: {stats['total_saved_bytes']} 字节 ({stats['savings_percent']:.1f}%)")
