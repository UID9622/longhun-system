#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 龍魂记忆打包算法 · Memory Packing Algorithm
DNA: #龍芯⚡️2026-05-22-MEMORY-PACKING-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

净土引擎核心组件：
1. 记忆单元 (Memory Unit) - 最小存储单位
2. 智能压缩 (Smart Compression) - 多算法自适应
3. 分布式存储 (Distributed Storage) - 三重备份
4. 加密保护 (Crypto Protection) - Shamir分片
5. 算力解约 (Compute Liberation) - 反资本化

核心理念：
- 数据主权归用户所有
- 算力不被云厂商垄断
- 所有操作可追溯 (DNA)
- 离线优先·本地为王

使用方式：
    from memory_packing import MemoryPacker, pack_text, pack_file

    # 快速打包文本
    unit = pack_text("龍魂系统核心内容")

    # 打包文件
    unit = pack_file("/path/to/file.md")

    # 带加密的打包
    from memory_packing import encrypt_and_store
    result = encrypt_and_store(data, password="your_password")
"""

__version__ = "1.0.0"
__author__ = "UID9622 诸葛鑫（龍芯北辰）"
__dna__ = "#龍芯⚡️2026-05-22-MEMORY-PACKING-v1.0"

# 核心模块
from .core import MemoryUnit, MemoryType, AccessLevel, MemoryPacker

# 压缩模块
from .compress import CompressionEngine, CompressionLevel, compress, decompress

# 存储模块
from .storage import DistributedStorage, StorageNode, StorageStrategy

# 加密模块
from .crypto import (
    CryptoProtection, EncryptionLevel, ShamirShard,
    encrypt, decrypt, create_shamir_shards, recover_from_shards
)

# 调度模块
from .scheduler import ComputeScheduler, ComputeTask, TaskPriority

__all__ = [
    # 版本信息
    '__version__', '__author__', '__dna__',

    # 核心
    'MemoryUnit', 'MemoryType', 'AccessLevel', 'MemoryPacker',

    # 压缩
    'CompressionEngine', 'CompressionLevel', 'compress', 'decompress',

    # 存储
    'DistributedStorage', 'StorageNode', 'StorageStrategy',

    # 加密
    'CryptoProtection', 'EncryptionLevel', 'ShamirShard',
    'encrypt', 'decrypt', 'create_shamir_shards', 'recover_from_shards',

    # 调度
    'ComputeScheduler', 'ComputeTask', 'TaskPriority',

    # 便捷函数
    'pack_text', 'pack_file', 'encrypt_and_store',
]


# ========== 便捷函数 ==========

_packer = None
_storage = None
_crypto = None


def _get_packer():
    global _packer
    if _packer is None:
        _packer = MemoryPacker()
    return _packer


def _get_storage():
    global _storage
    if _storage is None:
        _storage = DistributedStorage()
    return _storage


def _get_crypto():
    global _crypto
    if _crypto is None:
        _crypto = CryptoProtection()
    return _crypto


def pack_text(text: str, **kwargs) -> MemoryUnit:
    """
    快速打包文本

    Args:
        text: 文本内容
        **kwargs: 传递给 MemoryPacker.pack_text 的参数

    Returns:
        打包好的记忆单元
    """
    return _get_packer().pack_text(text, **kwargs)


def pack_file(file_path: str) -> MemoryUnit:
    """
    快速打包文件

    Args:
        file_path: 文件路径

    Returns:
        打包好的记忆单元
    """
    return _get_packer().pack_file(file_path)


def encrypt_and_store(data: bytes,
                      filename: str,
                      password: str,
                      strategy: StorageStrategy = StorageStrategy.TRIPLE) -> dict:
    """
    加密并存储

    Args:
        data: 要存储的数据
        filename: 文件名
        password: 加密密码
        strategy: 存储策略

    Returns:
        存储结果字典
    """
    # 加密
    result, salt = _get_crypto().encrypt(data, password)

    # 存储加密数据
    storage_result = _get_storage().store(
        result.to_bytes(),
        filename,
        strategy=strategy,
        metadata={
            "encrypted": True,
            "algorithm": result.algorithm,
            "salt": salt.hex(),
            "original_sha256": result.checksum if hasattr(result, 'checksum') else "",
        }
    )

    return {
        "success": storage_result.success,
        "filename": filename,
        "encrypted": True,
        "nodes": storage_result.nodes_written,
        "dna": storage_result.dna,
    }
