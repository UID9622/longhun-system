#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-08-06-LONGHUN-MEMORY-v1.0-SDK
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龙魂·记忆压缩+国密加密 SDK v1.0

给开发者的对话记忆工具包：
  - 智能压缩：保留关键信息，压缩冗余上下文
  - SM4 加密：国密对称加密，保护记忆数据
  - SM3 追溯链：哈希链保证数据完整性，防篡改可追溯
  - DNA 溯源：每条记忆绑定唯一追溯码
  - 三色审计：🟢通过·🟡待核·🔴红线

用法:
    from longhun_memory import MemoryVault

    vault = MemoryVault(key="your-secret-key")
    
    # 压缩 + 加密
    blob = vault.seal([
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！有什么可以帮你？"},
    ])
    
    # 解密 + 校验
    result = vault.unseal(blob)
"""

from .vault import MemoryVault, UnsealResult
from .sm_crypto import SM3, SM4, SM3HashChain
from .dna import DNA, dna_now
from .audit import AuditMark, ThreeColorAudit

__version__ = "1.0.0"
__all__ = [
    "MemoryVault", "UnsealResult",
    "SM3", "SM4", "SM3HashChain",
    "DNA", "dna_now",
    "AuditMark", "ThreeColorAudit",
]
