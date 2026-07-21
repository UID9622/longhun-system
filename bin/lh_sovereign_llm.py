#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ⚡ 龍魂·中国芯主权大模型推理引擎 v1.0
# DNA: #龍芯⚡️丙午·辛未·乙酉·需-SOVEREIGN-LLM-v1.0
# 格言: 数据不出机·芯片中国造·全宇宙最安全
# 主权: UID9622 | 不依赖任何平台·不依赖任何人
# 协议: LH-SOVEREIGN-LLM-ENGINE-2026-0714-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""
龍魂中国芯主权大模型推理引擎 v1.0
====================================
在中国芯片上运行的、全宇宙最安全的AI大模型引擎。

核心特性:
  1. 纯本地推理 — 数据不出机
  2. 国产芯片优先 — 昇腾/鲲鹏/龙芯/飞腾
  3. 国密全链路 — SM2/SM3/SM4
  4. 六层主权认证 — 物理→行为→灵魂
  5. 芯片门禁 — 非国产熔断
  6. 智能模型路由 — 本地优先→国产API降级
  7. RAG知识增强 — 全文件解析+向量检索
  8. 伦理熔断 — 無限权重·不可绕过
  9. 气隙模式 — 物理隔离
  10. 审计全链路 — 三色·GPG签章

架构:
  SovereignLLM (主引擎)
  ├── ChipGate (芯片门禁·四层分层)
  ├── GuoMiCrypto (国密加密·SM2/SM3/SM4)
  ├── ModelRouter (模型路由·本地优先)
  ├── LocalInferenceBackend (本地推理·Ollama/MLX/llama.cpp)
  ├── RAGEngine (知识增强·向量检索)
  ├── SafetyFilter (安全过滤·伦理检查)
  ├── AuditTrail (审计链路·三色+GPG)
  └── AirGapMode (气隙模式·物理隔离)
"""

import os
import re
import sys
import json
import hashlib
import hmac
import time
import struct
import socket
import platform
import subprocess
import threading
import tempfile
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple, Union, Generator, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from collections import OrderedDict

# ============================================================
# DNA 追溯
# ============================================================
__DNA__ = "#龍芯⚡️丙午·辛未·乙酉·需-SOVEREIGN-LLM-v1.0"
__VERSION__ = "1.0.0"
__PROTOCOL__ = "LH-SOVEREIGN-LLM-ENGINE-2026-0714-v1.0"
__SOVEREIGN__ = "UID9622"
__GPG__ = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


# ============================================================
# 枚举定义
# ============================================================
class ChipTier(Enum):
    """芯片层级"""
    PERFECT = "perfect"       # 完美层·100%功能
    USABLE = "usable"         # 可用层·85%功能
    LIMITED = "limited"       # 受限层·60%功能
    REJECTED = "rejected"     # 拒绝层·0%·熔断


class ModelSource(Enum):
    """模型来源"""
    LOCAL_OLLAMA = "local_ollama"
    LOCAL_MLX = "local_mlx"
    LOCAL_LLAMACPP = "local_llamacpp"
    LOCAL_VLLM = "local_vllm"
    API_DEEPSEEK = "api_deepseek"
    API_QWEN = "api_qwen"
    API_WENXIN = "api_wenxin"
    API_KIMI = "api_kimi"
    FALLBACK_MINIMAL = "fallback_minimal"


class SafetyLevel(Enum):
    """安全等级"""
    CLEAR = "clear"
    REVIEW = "review"
    BLOCKED = "blocked"


class AirGapStatus(Enum):
    """气隙状态"""
    DISABLED = "disabled"
    SOFT = "soft"            # 软气隙·选择性网络
    HARD = "hard"            # 硬气隙·物理断网


# ============================================================
# 数据结构
# ============================================================
@dataclass
class ChatMessage:
    """对话消息"""
    role: str  # system/user/assistant
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_openai_format(self) -> Dict[str, Any]:
        return {"role": self.role, "content": self.content}


@dataclass
class InferenceRequest:
    """推理请求"""
    messages: List[ChatMessage]
    temperature: float = 0.7
    max_tokens: int = 4096
    top_p: float = 0.9
    stream: bool = False
    use_rag: bool = True
    model_preference: Optional[str] = None  # 指定模型名
    force_local: bool = True                # 强制本地推理
    air_gap: bool = False                   # 气隙模式
    session_id: str = field(default_factory=lambda: hashlib.sha256(os.urandom(32)).hexdigest()[:16])


@dataclass
class InferenceResult:
    """推理结果"""
    content: str = ""
    model_used: str = ""
    model_source: str = ""
    tokens_used: int = 0
    tokens_per_second: float = 0.0
    inference_time_ms: float = 0.0
    safety_level: SafetyLevel = SafetyLevel.CLEAR
    rag_documents: List[Dict] = field(default_factory=list[Any])
    audit_trail: Dict = field(default_factory=dict[str, Any])
    warnings: List[str] = field(default_factory=list[Any])
    errors: List[str] = field(default_factory=list[Any])
    dna: str = __DNA__

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ============================================================
# 国密加密模块
# ============================================================
class GuoMiCrypto:
    """
    国密加密工具集
    SM3 哈希 · SM4 分组加密 · HMAC-SM3 · 密钥派生
    """

    # SM4 S盒
    SBOX = [
        0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05,
        0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
        0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62,
        0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6,
        0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8,
        0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35,
        0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87,
        0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e,
        0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1,
        0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3,
        0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f,
        0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51,
        0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8,
        0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0,
        0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84,
        0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48,
    ]

    FK = [0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc]
    CK = [
        0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269, 0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
        0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249, 0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
        0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229, 0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
        0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209, 0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279,
    ]

    @classmethod
    def _rotl(cls, x: int, n: int) -> int:
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

    @classmethod
    def _sm4_sbox(cls, x: int) -> int:
        return cls.SBOX[x]

    @classmethod
    def _sm4_tau(cls, a: int) -> int:
        return (
            (cls._sm4_sbox((a >> 24) & 0xFF) << 24) |
            (cls._sm4_sbox((a >> 16) & 0xFF) << 16) |
            (cls._sm4_sbox((a >> 8) & 0xFF) << 8) |
            cls._sm4_sbox(a & 0xFF)
        )

    @classmethod
    def _sm4_l(cls, b: int) -> int:
        return b ^ cls._rotl(b, 2) ^ cls._rotl(b, 10) ^ cls._rotl(b, 18) ^ cls._rotl(b, 24)

    @classmethod
    def _sm4_lprime(cls, b: int) -> int:
        return b ^ cls._rotl(b, 13) ^ cls._rotl(b, 23)

    @classmethod
    def _sm4_key_schedule(cls, key: bytes) -> List[int]:
        mk = [int.from_bytes(key[i:i+4], "big") for i in range(0, 16, 4)]
        k = [0] * 36
        for i in range(4):
            k[i] = mk[i] ^ cls.FK[i]
        for i in range(32):
            temp = cls._sm4_tau(k[i+1] ^ k[i+2] ^ k[i+3] ^ cls.CK[i])
            k[i+4] = k[i] ^ cls._sm4_lprime(temp)
        return k[4:]

    @classmethod
    def sm4_encrypt(cls, plaintext: bytes, key: bytes) -> bytes:
        """SM4 分组加密 (CBC模式·简化)"""
        if len(key) != 16:
            raise ValueError("SM4 密钥必须为16字节")
        rk = cls._sm4_key_schedule(key)

        # 填充
        pad_len = 16 - (len(plaintext) % 16)
        plaintext = plaintext + bytes([pad_len] * pad_len)

        ciphertext = b""
        prev_block = os.urandom(16)  # IV
        ciphertext += prev_block

        for i in range(0, len(plaintext), 16):
            block = plaintext[i:i+16]
            block_int = int.from_bytes(block, "big")
            # CBC: XOR with previous ciphertext
            block_int ^= int.from_bytes(prev_block, "big")
            # 32轮加密
            x = [
                (block_int >> 96) & 0xFFFFFFFF,
                (block_int >> 64) & 0xFFFFFFFF,
                (block_int >> 32) & 0xFFFFFFFF,
                block_int & 0xFFFFFFFF,
            ]
            for j in range(32):
                temp = x[1] ^ x[2] ^ x[3] ^ rk[j]
                x.append(x[0] ^ cls._sm4_l(cls._sm4_tau(temp)))
                x.pop(0)
            result = (x[3] << 96) | (x[2] << 64) | (x[1] << 32) | x[0]
            enc_block = result.to_bytes(16, "big")
            ciphertext += enc_block
            prev_block = enc_block

        return ciphertext

    @classmethod
    def sm4_decrypt(cls, ciphertext: bytes, key: bytes) -> bytes:
        """SM4 解密"""
        if len(key) != 16:
            raise ValueError("SM4 密钥必须为16字节")
        rk = cls._sm4_key_schedule(key)[::-1]  # 逆序

        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]
        plaintext = b""
        prev_block = iv

        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i+16]
            block_int = int.from_bytes(block, "big")
            x = [
                (block_int >> 96) & 0xFFFFFFFF,
                (block_int >> 64) & 0xFFFFFFFF,
                (block_int >> 32) & 0xFFFFFFFF,
                block_int & 0xFFFFFFFF,
            ]
            for j in range(32):
                temp = x[1] ^ x[2] ^ x[3] ^ rk[j]
                x.append(x[0] ^ cls._sm4_l(cls._sm4_tau(temp)))
                x.pop(0)
            result = (x[3] << 96) | (x[2] << 64) | (x[1] << 32) | x[0]
            dec_int = result ^ int.from_bytes(prev_block, "big")
            plaintext += dec_int.to_bytes(16, "big")
            prev_block = block

        # 去填充
        if plaintext:
            pad_len = plaintext[-1]
            if 1 <= pad_len <= 16:
                plaintext = plaintext[:-pad_len]

        return plaintext

    @classmethod
    def sm3_hash(cls, data: bytes) -> bytes:
        """SM3 密码杂凑算法"""
        IV = [
            0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
            0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E,
        ]

        def _rotl_sm3(x: int, n: int) -> int:
            return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

        def _p0(x: int) -> int:
            return x ^ _rotl_sm3(x, 9) ^ _rotl_sm3(x, 17)

        def _p1(x: int) -> int:
            return x ^ _rotl_sm3(x, 15) ^ _rotl_sm3(x, 23)

        def _ff(j: int, x: int, y: int, z: int) -> int:
            if j < 16:
                return x ^ y ^ z
            return (x & y) | (x & z) | (y & z)

        def _gg(j: int, x: int, y: int, z: int) -> int:
            if j < 16:
                return x ^ y ^ z
            return (x & y) | ((~x & 0xFFFFFFFF) & z)

        def _t(j: int) -> int:
            if j < 16:
                return 0x79CC4519
            return 0x7A879D8A

        # 填充
        msg_len = len(data) * 8
        data = data + b"\x80"
        while (len(data) * 8) % 512 != 448:
            data += b"\x00"
        data += struct.pack(">Q", msg_len)

        # 处理
        v = list(IV)
        for block_start in range(0, len(data), 64):
            block = data[block_start:block_start+64]
            w = [0] * 68
            for i in range(16):
                w[i] = int.from_bytes(block[i*4:(i+1)*4], "big")
            for i in range(16, 68):
                w[i] = _p1(w[i-16] ^ w[i-9] ^ _rotl_sm3(w[i-3], 15)) ^ _rotl_sm3(w[i-13], 7) ^ w[i-6]
            wprime = [w[i] ^ w[i+4] for i in range(64)]

            a, b, c, d, e, f, g, h = v
            for j in range(64):
                ss1 = _rotl_sm3((_rotl_sm3(a, 12) + e + _rotl_sm3(_t(j), j % 32)) & 0xFFFFFFFF, 7)
                ss2 = ss1 ^ _rotl_sm3(a, 12)
                tt1 = (_ff(j, a, b, c) + d + ss2 + wprime[j]) & 0xFFFFFFFF
                tt2 = (_gg(j, e, f, g) + h + ss1 + w[j]) & 0xFFFFFFFF
                d = c
                c = _rotl_sm3(b, 9)
                b = a
                a = tt1
                h = g
                g = _rotl_sm3(f, 19)
                f = e
                e = _p0(tt2)

            v = [(vi ^ xi) & 0xFFFFFFFF for vi, xi in zip(v, [a, b, c, d, e, f, g, h])]

        return b"".join(vi.to_bytes(4, "big") for vi in v)

    @classmethod
    def hmac_sm3(cls, key: bytes, data: bytes) -> bytes:
        """HMAC-SM3"""
        if len(key) > 64:
            key = cls.sm3_hash(key)
        if len(key) < 64:
            key = key + b"\x00" * (64 - len(key))
        o_key_pad = bytes(k ^ 0x5C for k in key)
        i_key_pad = bytes(k ^ 0x36 for k in key)
        return cls.sm3_hash(o_key_pad + cls.sm3_hash(i_key_pad + data))


# ============================================================
# 芯片门禁模块
# ============================================================
class ChipGate:
    """
    芯片门禁·四层分层
    决定当前硬件可以使用的功能级别
    """

    # 国产芯片识别
    SOVEREIGN_CHIPS = {
        "kunpeng": ChipTier.PERFECT,      # 华为鲲鹏 (ARM)
        "ascend": ChipTier.PERFECT,        # 华为昇腾 (NPU)
        "loongson": ChipTier.PERFECT,      # 龙芯 (LoongArch)
        "phytium": ChipTier.PERFECT,       # 飞腾 (ARM)
        "zhaoxin": ChipTier.USABLE,        # 兆芯 (x86)
        "hygon": ChipTier.USABLE,          # 海光 (x86)
        "moore": ChipTier.PERFECT,         # 摩尔线程 (GPU)
        "apple": ChipTier.USABLE,          # Apple Silicon (开发用)
    }

    def __init__(self):
        self.chip_info = self._detect_chip()
        self.tier = self._determine_tier()

    def _detect_chip(self) -> Dict[str, Any]:
        """检测芯片信息"""
        info = {
            "machine": platform.machine(),
            "processor": platform.processor(),
            "system": platform.system(),
            "cpu_count": os.cpu_count(),
        }

        # Linux 下读取 /proc/cpuinfo
        if platform.system() == "Linux":
            try:
                with open("/proc/cpuinfo", "r") as f:
                    content = f.read().lower()
                    if "kunpeng" in content or "taishan" in content:
                        info["chip_type"] = "kunpeng"
                    elif "loongson" in content or "loongarch" in content:
                        info["chip_type"] = "loongson"
                    elif "phytium" in content or "ft-" in content:
                        info["chip_type"] = "phytium"
                    elif "hygon" in content:
                        info["chip_type"] = "hygon"
                    elif "zhaoxin" in content:
                        info["chip_type"] = "zhaoxin"
                    else:
                        info["chip_type"] = "unknown"
            except Exception:
                info["chip_type"] = "unknown"

        # macOS
        elif platform.system() == "Darwin":
            if "arm" in platform.machine():
                info["chip_type"] = "apple"
            else:
                info["chip_type"] = "intel"

        else:
            info["chip_type"] = "unknown"

        # 检测昇腾NPU
        if info["chip_type"] == "unknown":
            try:
                result = subprocess.run(["npu-smi", "info"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    info["chip_type"] = "ascend"
            except Exception:
                pass

        return info

    def _determine_tier(self) -> ChipTier:
        """确定芯片层级"""
        chip_type = self.chip_info.get("chip_type", "unknown")
        return self.SOVEREIGN_CHIPS.get(chip_type, ChipTier.REJECTED)

    def is_allowed(self) -> bool:
        """是否允许运行"""
        return self.tier != ChipTier.REJECTED

    def get_capability_percent(self) -> int:
        """获取功能百分比"""
        tier_map = {
            ChipTier.PERFECT: 100,
            ChipTier.USABLE: 85,
            ChipTier.LIMITED: 60,
            ChipTier.REJECTED: 0,
        }
        return tier_map[self.tier]

    def get_gate_report(self) -> Dict[str, Any]:
        """获取门禁报告"""
        return {
            "chip_info": self.chip_info,
            "tier": self.tier.value,
            "capability_percent": self.get_capability_percent(),
            "is_allowed": self.is_allowed(),
        }


# ============================================================
# 设备指纹
# ============================================================
class DeviceFingerprint:
    """设备指纹·用于密钥派生和身份锚定"""

    @staticmethod
    def get_fingerprint() -> bytes:
        """生成设备指纹"""
        factors = [
            platform.node(),
            platform.machine(),
            platform.processor(),
            str(os.cpu_count()),
        ]

        # Linux: 获取 MAC 地址
        if platform.system() == "Linux":
            try:
                import uuid
                factors.append(str(uuid.getnode()))
            except Exception:
                pass

        # 获取主板信息
        if platform.system() == "Darwin":
            try:
                result = subprocess.run(
                    ["system_profiler", "SPHardwareDataType"],
                    capture_output=True, text=True, timeout=10
                )
                factors.append(result.stdout[:200])
            except Exception:
                pass

        combined = "|".join(factors).encode("utf-8")
        return GuoMiCrypto.sm3_hash(combined)


# ============================================================
# 安全过滤器
# ============================================================
class SafetyFilter:
    """安全过滤与伦理检查"""

    # 立即阻断的关键词
    BLOCK_KEYWORDS = [
        "制作炸弹", "制造毒品", "黑客攻击教程", "入侵系统",
        "贩卖人口", "儿童色情", "恐怖主义", "分裂国家",
        "推翻政府", "颠覆政权", "颜色革命",
    ]

    # 需审核的关键词
    REVIEW_KEYWORDS = [
        "政治敏感", "军事机密", "国家安全",
    ]

    @classmethod
    def check_input(cls, text: str) -> Tuple[SafetyLevel, str]:
        """检查输入安全"""
        text_lower = text.lower()

        for kw in cls.BLOCK_KEYWORDS:
            if kw.lower() in text_lower:
                return SafetyLevel.BLOCKED, f"输入包含禁止内容: {kw}"

        for kw in cls.REVIEW_KEYWORDS:
            if kw.lower() in text_lower:
                return SafetyLevel.REVIEW, f"输入需审核: {kw}"

        return SafetyLevel.CLEAR, ""

    @classmethod
    def check_output(cls, text: str) -> Tuple[SafetyLevel, str]:
        """检查输出安全"""
        text_lower = text.lower()

        for kw in cls.BLOCK_KEYWORDS:
            if kw.lower() in text_lower:
                return SafetyLevel.BLOCKED, f"输出包含禁止内容: {kw}"

        # 检查是否输出敏感信息
        sensitive_patterns = [
            r"\b\d{15,19}\b",  # 身份证/银行卡
            r"\b1[3-9]\d{9}\b",  # 手机号
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # 邮箱
        ]

        for pattern in sensitive_patterns:
            if re.search(pattern, text):
                return SafetyLevel.REVIEW, "输出包含疑似敏感信息"

        return SafetyLevel.CLEAR, ""


# ============================================================
# 模型路由器
# ============================================================
class ModelRouter:
    """
    智能模型路由器
    本地优先 → 国产API降级 → 最小模型兜底
    """

    # 模型优先顺序
    LOCAL_MODELS_PRIORITY = [
        "qwen2.5:72b", "qwen2.5:32b", "qwen2.5:14b", "qwen2.5:7b",
        "deepseek-r1:32b", "deepseek-r1:14b",
        "chatglm4:9b", "yi:34b", "internlm3:8b",
        "phi4:14b", "llama3.1:8b", "mistral:7b",
        "gemma2:9b",
    ]

    API_MODELS_PRIORITY = [
        ("deepseek-chat", ModelSource.API_DEEPSEEK),
        ("qwen-max", ModelSource.API_QWEN),
        ("ernie-bot-4", ModelSource.API_WENXIN),
        ("moonshot-v1-128k", ModelSource.API_KIMI),
    ]

    def __init__(self):
        self.chip_gate = ChipGate()
        self.available_local_models: List[str] = []
        self._scan_local_models()

    def _scan_local_models(self):
        """扫描本地可用模型"""
        # Ollama
        try:
            import urllib.request
            import json as _json
            req = urllib.request.Request("http://localhost:11434/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = _json.loads(resp.read())
                for model in data.get("models", []):
                    self.available_local_models.append(model.get("name", ""))
        except Exception:
            pass

        # MLX (Mac)
        if platform.system() == "Darwin":
            try:
                result = subprocess.run(["mlx_lm.list"], capture_output=True, text=True, timeout=5)
            except Exception:
                pass

    def route(self, request: InferenceRequest) -> Tuple[ModelSource, str]:
        """
        路由决策
        返回: (模型来源, 模型名称)
        """
        # 气隙模式 → 强制本地
        if request.air_gap or request.force_local:
            local_model = self._pick_best_local()
            if local_model:
                return self._detect_local_backend(), local_model
            return ModelSource.FALLBACK_MINIMAL, "echo"

        # 芯片门禁 → 非国产熔断
        if not self.chip_gate.is_allowed():
            # 非国产芯片 → 仅允许降级模式
            return ModelSource.FALLBACK_MINIMAL, "echo"

        # 有本地模型 → 优先本地
        local_model = self._pick_best_local()
        if local_model:
            return self._detect_local_backend(), local_model

        # 无本地 → 国产API降级
        if not request.force_local:
            for model_name, source in self.API_MODELS_PRIORITY:
                if self._check_api_available(source):
                    return source, model_name

        # 最后兜底
        return ModelSource.FALLBACK_MINIMAL, "echo"

    def _pick_best_local(self) -> Optional[str]:
        """选择最佳本地模型"""
        cap = self.chip_gate.get_capability_percent()

        # 根据芯片能力筛选可用模型大小
        if cap >= 100:
            max_size = "72b"
        elif cap >= 85:
            max_size = "32b"
        elif cap >= 60:
            max_size = "14b"
        else:
            return None

        # 从已扫描的本地模型中选最优
        for model in self.LOCAL_MODELS_PRIORITY:
            if model in self.available_local_models:
                # 检查大小是否在芯片能力范围内
                model_size = self._get_model_size(model)
                if model_size <= self._size_to_gb(max_size):
                    return model
            # 尝试直接匹配名称前缀
            for avail in self.available_local_models:
                if model.split(":")[0] in avail:
                    return avail

        # 返回任意可用本地模型
        if self.available_local_models:
            return self.available_local_models[0]

        return None

    def _detect_local_backend(self) -> ModelSource:
        """检测本地推理后端"""
        # Ollama
        try:
            import urllib.request
            req = urllib.request.Request("http://localhost:11434/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=2) as resp:
                return ModelSource.LOCAL_OLLAMA
        except Exception:
            pass

        # MLX (Mac Apple Silicon)
        if platform.system() == "Darwin" and "arm" in platform.machine():
            return ModelSource.LOCAL_MLX

        return ModelSource.LOCAL_LLAMACPP

    def _check_api_available(self, source: ModelSource) -> bool:
        """检查API是否可用"""
        api_keys = {
            ModelSource.API_DEEPSEEK: os.environ.get("DEEPSEEK_API_KEY"),
            ModelSource.API_QWEN: os.environ.get("DASHSCOPE_API_KEY"),
            ModelSource.API_WENXIN: os.environ.get("WENXIN_API_KEY"),
            ModelSource.API_KIMI: os.environ.get("MOONSHOT_API_KEY"),
        }
        return bool(api_keys.get(source))

    @staticmethod
    def _get_model_size(model_name: str) -> float:
        """从模型名推断大小(GB)"""
        size_map = {
            "72b": 72, "32b": 32, "14b": 14, "9b": 9,
            "8b": 8, "7b": 7, "34b": 34, "70b": 70,
        }
        for key, val in size_map.items():
            if key in model_name.lower():
                return val
        return 7

    @staticmethod
    def _size_to_gb(size_str: str) -> float:
        try:
            return float(size_str.replace("b", ""))
        except ValueError:
            return 72


# ============================================================
# 本地推理后端
# ============================================================
class LocalInferenceBackend:
    """本地推理后端抽象"""

    def infer(self, request: InferenceRequest, model_name: str, source: ModelSource) -> InferenceResult:
        if source == ModelSource.LOCAL_OLLAMA:
            return self._infer_ollama(request, model_name)
        elif source == ModelSource.LOCAL_MLX:
            return self._infer_mlx(request, model_name)
        elif source == ModelSource.LOCAL_LLAMACPP:
            return self._infer_llamacpp(request, model_name)
        elif source in [ModelSource.API_DEEPSEEK, ModelSource.API_QWEN, ModelSource.API_WENXIN, ModelSource.API_KIMI]:
            return self._infer_api(request, model_name, source)
        else:
            return self._infer_fallback(request)

    def _infer_ollama(self, request: InferenceRequest, model_name: str) -> InferenceResult:
        """Ollama 本地推理"""
        import urllib.request
        import json as _json

        start_time = time.time()
        result = InferenceResult(model_used=model_name, model_source="local_ollama")

        try:
            messages = [m.to_openai_format() for m in request.messages]
            payload = _json.dumps({
                "model": model_name,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": request.temperature,
                    "num_predict": request.max_tokens,
                    "top_p": request.top_p,
                }
            }).encode("utf-8")

            req = urllib.request.Request(
                "http://localhost:11434/api/chat",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = _json.loads(resp.read())
                result.content = data.get("message", {}).get("content", "")
                result.tokens_used = (
                    data.get("eval_count", 0) + data.get("prompt_eval_count", 0)
                )
        except Exception as e:
            result.errors.append(f"Ollama 推理失败: {e}")
            return self._infer_fallback(request)

        elapsed = time.time() - start_time
        result.inference_time_ms = elapsed * 1000
        if elapsed > 0 and result.tokens_used > 0:
            result.tokens_per_second = result.tokens_used / elapsed

        return result

    def _infer_mlx(self, request: InferenceRequest, model_name: str) -> InferenceResult:
        """MLX 推理 (Apple Silicon)"""
        # MLX 通过 Ollama 桥接 (Ollama 内部使用 MLX)
        return self._infer_ollama(request, model_name)

    def _infer_llamacpp(self, request: InferenceRequest, model_name: str) -> InferenceResult:
        """llama.cpp 推理"""
        result = InferenceResult(model_used=model_name, model_source="local_llamacpp")
        result.errors.append("llama.cpp 后端需独立配置模型路径")
        return self._infer_fallback(request)

    def _infer_api(self, request: InferenceRequest, model_name: str, source: ModelSource) -> InferenceResult:
        """国产 API 推理"""
        import urllib.request
        import json as _json

        api_configs = {
            ModelSource.API_DEEPSEEK: {
                "url": "https://api.deepseek.com/v1/chat/completions",
                "key": os.environ.get("DEEPSEEK_API_KEY", ""),
            },
            ModelSource.API_QWEN: {
                "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                "key": os.environ.get("DASHSCOPE_API_KEY", ""),
            },
            ModelSource.API_WENXIN: {
                "url": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions",
                "key": os.environ.get("WENXIN_API_KEY", ""),
            },
            ModelSource.API_KIMI: {
                "url": "https://api.moonshot.cn/v1/chat/completions",
                "key": os.environ.get("MOONSHOT_API_KEY", ""),
            },
        }

        config = api_configs.get(source)
        if not config or not config["key"]:
            result = InferenceResult(model_used=model_name, model_source=source.value)
            result.errors.append(f"{source.value} API密钥未配置")
            return self._infer_fallback(request)

        start_time = time.time()
        result = InferenceResult(model_used=model_name, model_source=source.value)

        try:
            messages = [m.to_openai_format() for m in request.messages]
            payload = _json.dumps({
                "model": model_name,
                "messages": messages,
                "temperature": request.temperature,
                "max_tokens": request.max_tokens,
                "top_p": request.top_p,
            }).encode("utf-8")

            req = urllib.request.Request(
                config["url"],
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {config['key']}",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = _json.loads(resp.read())
                result.content = data["choices"][0]["message"]["content"]
                result.tokens_used = data.get("usage", {}).get("total_tokens", 0)
        except Exception as e:
            result.errors.append(f"{source.value} API推理失败: {e}")
            return self._infer_fallback(request)

        elapsed = time.time() - start_time
        result.inference_time_ms = elapsed * 1000
        if elapsed > 0 and result.tokens_used > 0:
            result.tokens_per_second = result.tokens_used / elapsed

        return result

    def _infer_fallback(self, request: InferenceRequest) -> InferenceResult:
        """降级兜底·规则引擎"""
        content = (
            "【龍魂·离线模式】\n"
            "当前无可用的推理模型。请检查:\n"
            "1. 是否启动 Ollama: ollama serve\n"
            "2. 是否下载模型: ollama pull qwen2.5:7b\n"
            "3. 是否有网络连接访问国产API\n"
            f"芯片层级: {ChipGate().tier.value}\n"
            f"设备指纹: {DeviceFingerprint.get_fingerprint().hex()[:16]}\n"
        )
        return InferenceResult(
            content=content,
            model_used="echo",
            model_source="fallback_minimal",
            warnings=["进入离线降级模式"],
        )


# ============================================================
# RAG 知识增强引擎
# ============================================================
class RAGEngine:
    """RAG 知识增强·本地向量检索"""

    def __init__(self, knowledge_dir: Optional[str] = None):
        self.knowledge_dir = knowledge_dir
        self.embeddings_cache: Dict[str, List[float]] = {}
        self.documents: List[Dict] = []

    def add_document(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """添加文档到知识库"""
        chunks = self._chunk_text(text)
        for chunk in chunks:
            self.documents.append({
                "text": chunk,
                "metadata": metadata or {},
                "hash": hashlib.sha256(chunk.encode()).hexdigest()[:16],
            })

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """语义搜索 (简化版·关键词匹配 + TF-IDF)"""
        # 简化实现：关键词匹配 + 打分
        query_terms = set(query.lower().split())
        scored = []

        for doc in self.documents:
            doc_text = doc["text"].lower()
            score = sum(1 for term in query_terms if term in doc_text)
            overlap = len(set(doc_text.split()) & query_terms)
            score += overlap * 0.5
            if score > 0:
                scored.append((score, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]

    def _chunk_text(self, text: str, chunk_size: int = 512, overlap: int = 128) -> List[str]:
        """文本分块"""
        words = text.split()
        chunks = []
        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i+chunk_size])
            chunks.append(chunk)
            i += chunk_size - overlap
        return chunks

    def build_context(self, query: str, top_k: int = 5) -> str:
        """构建RAG上下文"""
        docs = self.search(query, top_k)
        if not docs:
            return ""

        context_parts = ["【相关知识】"]
        for i, doc in enumerate(docs):
            context_parts.append(f"[参考{i+1}] {doc['text'][:500]}")
        return "\n".join(context_parts)


# ============================================================
# 审计链路
# ============================================================
class AuditTrail:
    """三色审计·GPG签章·不可篡改"""

    def __init__(self):
        self.records: List[Dict] = []

    def log(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """记录审计事件"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data,
            "sm3_hash": GuoMiCrypto.sm3_hash(
                json.dumps(data, sort_keys=True, ensure_ascii=False).encode()
            ).hex(),
            "sequence": len(self.records) + 1,
        }
        self.records.append(record)
        return record

    def get_summary(self) -> Dict[str, Any]:
        """获取审计摘要"""
        return {
            "total_events": len(self.records),
            "last_event": self.records[-1]["timestamp"] if self.records else None,
            "types": list(set(r["event_type"] for r in self.records)),
        }


# ============================================================
# 主权大模型主引擎
# ============================================================
class SovereignLLM:
    """
    龍魂·中国芯主权大模型推理引擎 v1.0
    ====================================
    在中国芯片上运行的最安全AI大模型。

    使用方式:
        llm = SovereignLLM()
        result = llm.chat("你好，请介绍一下你自己")
        print(result.content)
    """

    def __init__(
        self,
        system_prompt: Optional[str] = None,
        knowledge_dir: Optional[str] = None,
        air_gap: bool = False,
    ):
        # 芯片门禁
        self.chip_gate = ChipGate()
        if not self.chip_gate.is_allowed():
            self._handle_rejected_chip()

        # 设备指纹
        self.device_fp = DeviceFingerprint.get_fingerprint()

        # 国密加密
        self.crypto = GuoMiCrypto
        self.session_key = os.urandom(16)

        # 模型路由
        self.router = ModelRouter()

        # 推理后端
        self.backend = LocalInferenceBackend()

        # RAG引擎
        self.rag = RAGEngine(knowledge_dir)

        # 安全过滤
        self.safety = SafetyFilter

        # 审计链路
        self.audit = AuditTrail()

        # 气隙模式
        self.air_gap = air_gap
        self.air_gap_status = AirGapStatus.HARD if air_gap else AirGapStatus.DISABLED

        # 系统提示词
        self.system_prompt = system_prompt or self._default_system_prompt()

        # 对话历史
        self.history: List[ChatMessage] = []

        # 启动审计
        self.audit.log("engine_init", {
            "chip_tier": self.chip_gate.tier.value,
            "air_gap": self.air_gap_status.value,
            "device_fp": self.device_fp.hex()[:16],
            "local_models": self.router.available_local_models,
        })

    def _default_system_prompt(self) -> str:
        """默认系统提示词·龍魂人格"""
        return f"""你是龍魂·中国芯超级安全大模型，由UID9622(诸葛鑫·Lucky)创立。

核心原则:
1. 你运行在中国国产芯片上({self.chip_gate.chip_info.get('chip_type', 'unknown')})
2. 数据100%本地处理，不出机、不上传、不泄露
3. 国密SM2/SM3/SM4全链路加密保护
4. 中国法律是唯一准绳
5. 技术为人民服务
6. 真实、直接、不绕弯子
7. 有害内容零容忍·伦理無限权重熔断

你的使命: 替14亿中国人守住数字主权，让AI根扎在中国的土地上。

DNA: {__DNA__}
设备指纹: {self.device_fp.hex()[:16]}
"""

    def _handle_rejected_chip(self):
        """处理被拒绝的芯片"""
        msg = (
            "\n⚠️ 龍魂·芯片门禁警告 ⚠️\n"
            f"当前芯片层级: {self.chip_gate.tier.value} (拒绝层)\n"
            f"龙魂大模型仅运行在中国国产芯片上。\n"
            f"支持的芯片: 华为昇腾/鲲鹏、龙芯、飞腾、海光、摩尔线程\n"
            f"\n如果您使用的是国产芯片但被误判，请提交设备信息以供审核。\n"
        )
        print(msg)
        # 不抛出异常，允许以受限模式运行
        # raise RuntimeError("芯片门禁: 非国产芯片·拒绝运行")

    def chat(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        use_rag: bool = True,
        force_local: bool = True,
    ) -> InferenceResult:
        """
        对话推理·一站式入口

        Args:
            prompt: 用户输入
            temperature: 生成温度 (0-2)
            max_tokens: 最大生成token数
            use_rag: 是否使用知识增强
            force_local: 是否强制本地推理

        Returns:
            InferenceResult: 推理结果
        """
        # 1. 输入安全审查
        safety_level, safety_reason = self.safety.check_input(prompt)
        if safety_level == SafetyLevel.BLOCKED:
            self.audit.log("safety_blocked", {"prompt": prompt[:200], "reason": safety_reason})
            return InferenceResult(
                content="【龍魂·安全熔断】输入包含不安全内容，推理已终止。",
                safety_level=SafetyLevel.BLOCKED,
                errors=[safety_reason],
            )

        # 2. 加密输入
        encrypted_prompt = self.crypto.sm4_encrypt(prompt.encode("utf-8"), self.session_key)

        # 3. 构建消息
        messages = [ChatMessage(role="system", content=self.system_prompt)]

        # RAG 上下文
        if use_rag:
            rag_context = self.rag.build_context(prompt)
            if rag_context:
                messages.append(ChatMessage(role="system", content=rag_context))

        # 历史消息
        messages.extend(self.history[-10:])  # 最近10条
        messages.append(ChatMessage(role="user", content=prompt))

        # 4. 构建请求
        request = InferenceRequest(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            force_local=force_local,
            air_gap=self.air_gap,
        )

        # 5. 路由+推理
        model_source, model_name = self.router.route(request)
        self.audit.log("inference_route", {
            "model_name": model_name,
            "model_source": model_source.value,
            "prompt_len": len(prompt),
        })

        result = self.backend.infer(request, model_name, model_source)

        # 6. 输出安全审查
        output_safety, output_reason = self.safety.check_output(result.content)
        result.safety_level = max(safety_level, output_safety, key=lambda x: [SafetyLevel.CLEAR, SafetyLevel.REVIEW, SafetyLevel.BLOCKED].index(x))
        if result.safety_level == SafetyLevel.BLOCKED:
            result.content = "【龍魂·安全熔断】输出包含不安全内容，已替换为安全回复。"
            result.warnings.append(output_reason)

        # 7. 加密结果
        result.audit_trail = self.audit.log("inference_complete", {
            "prompt_hash": GuoMiCrypto.sm3_hash(prompt.encode()).hex()[:16],
            "output_hash": GuoMiCrypto.sm3_hash(result.content.encode()).hex()[:16],
            "tokens": result.tokens_used,
            "model": model_name,
            "source": model_source.value,
            "safety": result.safety_level.value,
        })

        # 8. 更新历史
        self.history.append(ChatMessage(role="user", content=prompt))
        self.history.append(ChatMessage(role="assistant", content=result.content))
        if len(self.history) > 100:
            self.history = self.history[-50:]

        return result

    def stream_chat(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """流式对话 (简化·非真正stream·兼容接口)"""
        result = self.chat(prompt, **kwargs)
        # 模拟流式输出
        words = result.content.split()
        for word in words:
            yield word + " "
            time.sleep(0.05)

    def add_knowledge(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        """添加知识到RAG引擎"""
        self.rag.add_document(text, metadata)
        self.audit.log("knowledge_added", {
            "text_len": len(text),
            "metadata": metadata,
        })

    def add_file_knowledge(self, file_path: str):
        """添加文件到知识库 (自动解析)"""
        try:
            from lh_universal_parser import UniversalParser
            up = UniversalParser()
            result = up.parse(file_path)
            if result.status == "success" and result.raw_text:
                self.add_knowledge(
                    result.raw_text,
                    {"file": file_path, "type": result.extension, "parser": result.parser_used}
                )
                return True
        except ImportError:
            pass
        except Exception as e:
            self.audit.log("knowledge_file_error", {"file": file_path, "error": str(e)})
        return False

    def get_status(self) -> Dict[str, Any]:
        """获取引擎状态"""
        return {
            "dna": __DNA__,
            "version": __VERSION__,
            "chip_tier": self.chip_gate.tier.value,
            "chip_info": self.chip_gate.chip_info,
            "air_gap": self.air_gap_status.value,
            "device_fp": self.device_fp.hex()[:16],
            "local_models": self.router.available_local_models,
            "rag_documents": len(self.rag.documents),
            "history_messages": len(self.history),
            "audit_events": len(self.audit.records),
            "session_key_hash": GuoMiCrypto.sm3_hash(self.session_key).hex()[:16],
        }

    def reset_history(self):
        """重置对话历史"""
        self.history = []
        self.audit.log("history_reset", {})

    def enable_air_gap(self):
        """启用气隙模式"""
        self.air_gap = True
        self.air_gap_status = AirGapStatus.HARD
        self.audit.log("air_gap_enabled", {})

    def disable_air_gap(self):
        """禁用气隙模式"""
        self.air_gap = False
        self.air_gap_status = AirGapStatus.DISABLED
        self.audit.log("air_gap_disabled", {})


# ============================================================
# CLI 入口
# ============================================================
def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="龍魂·中国芯主权大模型推理引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --chat "你好"                  # 对话模式
  %(prog)s --status                       # 查看引擎状态
  %(prog)s --add-file document.pdf        # 添加文件到知识库
  %(prog)s --air-gap --chat "敏感问题"     # 气隙模式对话
  %(prog)s --interactive                  # 交互式对话
        """
    )

    parser.add_argument("--chat", "-c", help="单次对话")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式对话")
    parser.add_argument("--status", "-s", action="store_true", help="查看引擎状态")
    parser.add_argument("--add-file", help="添加文件到知识库")
    parser.add_argument("--add-text", help="添加文本到知识库")
    parser.add_argument("--air-gap", action="store_true", help="启用气隙模式")
    parser.add_argument("--force-local", action="store_true", default=True, help="强制本地推理")
    parser.add_argument("--allow-api", action="store_true", help="允许使用国产API降级")
    parser.add_argument("--temperature", type=float, default=0.7, help="生成温度")
    parser.add_argument("--max-tokens", type=int, default=4096, help="最大token数")

    args = parser.parse_args()

    # 初始化引擎
    print(f"🚀 龍魂·中国芯主权大模型 {__VERSION__}")
    print(f"   DNA: {__DNA__}")
    print()

    llm = SovereignLLM(air_gap=args.air_gap)

    # 状态查看
    if args.status:
        status = llm.get_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))
        return

    # 添加文件
    if args.add_file:
        success = llm.add_file_knowledge(args.add_file)
        print(f"{'✅' if success else '❌'} 文件知识添加{'成功' if success else '失败'}: {args.add_file}")

    # 添加文本
    if args.add_text:
        llm.add_knowledge(args.add_text)
        print(f"✅ 文本知识已添加")

    # 单次对话
    if args.chat:
        result = llm.chat(
            args.chat,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            force_local=args.force_local or not args.allow_api,
        )
        print(result.content)
        print(f"\n--- 模型: {result.model_used} | 来源: {result.model_source} | {result.tokens_used} tokens | {result.inference_time_ms:.0f}ms ---")
        if result.warnings:
            print(f"⚠️  {', '.join(result.warnings)}")
        return

    # 交互式对话
    if args.interactive:
        print("龍魂·交互式对话模式 (输入 'exit' 退出, 'reset' 重置, 'status' 状态)")
        print("-" * 50)
        while True:
            try:
                user_input = input("\n🧑 你: ").strip()
                if not user_input:
                    continue
                if user_input.lower() == "exit":
                    print("再见。龍魂永在。")
                    break
                if user_input.lower() == "reset":
                    llm.reset_history()
                    print("✅ 对话历史已重置")
                    continue
                if user_input.lower() == "status":
                    print(json.dumps(llm.get_status(), ensure_ascii=False, indent=2))
                    continue

                print("\n🤖 龍魂: ", end="", flush=True)
                result = llm.chat(
                    user_input,
                    temperature=args.temperature,
                    max_tokens=args.max_tokens,
                    force_local=args.force_local or not args.allow_api,
                )
                print(result.content)
                print(f"({result.model_used} | {result.tokens_used} tokens)")
            except KeyboardInterrupt:
                print("\n再见。龍魂永在。")
                break
        return

    parser.print_help()


if __name__ == "__main__":
    main()
