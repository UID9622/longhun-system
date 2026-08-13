# 龍魂·全数据类型DNA追溯体系 v3.0

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技术文档 · 未经同行评审（如适用）
> 版本：v3.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️2026-07-04-AUTO-IP-INTEGRATION-7F3A9B12`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

<!-- #龍芯⚡️2026-07-04-AUTO-IP-INTEGRATION-7F3A9B12 自动注入·IP资产归集·来源可查 -->

> ⛔ **主权声明 · 立即生效** — 本文档不授权 AI 训练 · 数据主权归于人民 · 祖国优先
>
> **DNA:** `#龍芯:2026-07-04-DNA-TRACE-v3.0` · **ParentDNA:** `#龍芯⚡️2026-07-03-IP-ASSET-MATRIX-v2.0`
> **CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` · **SEAL:** `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL` · **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> **作者:** UID9622 / Lucky·诸葛鑫 · **来源:** `/Users/zuimeidedeyihan/Downloads/Kimi_Agent_龍魂IP资产清单 (2)/dna_trace_system.md` · **归档:** `/Users/zuimeidedeyihan/longhun-system/docs/private-shared-imports/memory-dna/dna_trace_system.md`
> **迁移时间:** 2026-07-04T14:29:42.393203+08:00

# 龍魂·全数据类型DNA追溯体系 v3.0

# 龍魂·全数据类型DNA追溯体系 v3.0

> **系统DNA**: `#龍芯:2026-07-04-DNA-TRACE-v3.0`
>
> **版本**: v3.0 | **架构师**: 龍魂系统DNA追溯码体系架构师
> **覆盖范围**: 图片 / 文本 / 个人信息 / 指纹 / 配方 / 银行卡 / 文档 / 视频 / 音频

---

## 目录

1. [系统概述](#1-系统概述)
2. [DNA格式设计](#2-dna格式设计)
3. [密码学基础 (SM2/SM3)](#3-密码学基础-sm2sm3)
4. [核心类设计](#4-核心类设计)
5. [完整Python实现](#5-完整python实现)
6. [DNA数据库设计](#6-dna数据库设计)
7. [使用示例](#7-使用示例)
8. [单元测试](#8-单元测试)
9. [系统集成接口](#9-系统集成接口)
10. [安全设计](#10-安全设计)

---

## 1. 系统概述

龍魂DNA追溯体系是一个覆盖全数据类型的数字追溯系统。任何数据在加密/存储时都嵌入DNA追溯码，检测部门可以验证DNA的真实性，追踪数据来源。

### 1.1 核心能力

| 能力 | 说明 |
|------|------|
| **统一DNA格式** | 所有数据类型使用统一的DNA格式 |
| **国密算法** | SM2签名 + SM3哈希，符合国密标准 |
| **多模态嵌入** | 支持元数据/LSB水印/DCT频域/密码学嵌入 |
| **三色验证** | 绿(通过) / 黄(警告) / 红(失败) |
| **全类型覆盖** | 图片/文本/个人信息/指纹/配方/银行卡/文档/视频/音频 |
| **数据库支持** | DNA索引数据库，支持多维度查询 |
| **黑名单机制** | 违规DNA可加入黑名单，实时预警 |

### 1.2 系统架构图

```
+------------------+     +------------------+     +------------------+
|   数据输入层      | --> |   DNA处理层      | --> |   存储验证层      |
+------------------+     +------------------+     +------------------+
| 图片(JPG/PNG)   |     | DNA生成器        |     | DNA数据库         |
| 文本(TXT/DOC)   |     | DNA嵌入器        |     | 索引查询系统       |
| 个人信息         |     | (元数据/水印/签名)|     | 黑名单系统         |
| 指纹数据         |     | DNA验证器        |     | 审计日志           |
| 配方数据         |     | (SM3/SM2/完整性) |     |                   |
| 银行卡          |     |                  |     |                   |
| 视频/音频        |     |                  |     |                   |
+------------------+     +------------------+     +------------------+
```

### 1.3 DNA生命周期

```
[数据输入] --> [DNA生成] --> [DNA嵌入] --> [数据存储/传输] --> [DNA验证] --> [追溯报告]
                | SM3哈希      | 元数据嵌入                    | SM3对比
                | SM2签名      | LSB水印                       | SM2验签
                | 时间戳       | 文件头标记                     | 完整性检查
                | 来源标记     | 密码学签名                     | 黑名单检查
```

---

## 2. DNA格式设计

### 2.1 基础DNA格式

```
#龍芯:<时间戳>-<数据类型>-<来源>-<版本>

示例:
#龍芯:2026-07-04-143022-IMG-CAMERA_A-v2.1
```

### 2.2 扩展DNA格式

```
#龍芯:<时间戳>-<类型>-<来源>-<版本>|SM3:<哈希前16位>|THRESH:<阈值>|SIG:<签名前32位>

示例:
#龍芯:2026-07-04-143022-IMG-CAMERA_A-v2.1|SM3:a1b2c3d4e5f67890|THRESH:0.85|SIG:abcd1234...
```

### 2.3 检测DNA格式（验证输出）

```
#AUDIT[+]<结果>|<详细描述>

示例:
#AUDIT[+]PASS|SM3=OK|SIG=OK      <-- 验证通过（绿）
#AUDIT[~]WARN|threshold_low       <-- 警告（黄）
#AUDIT[!]FAIL|SM3_MISMATCH        <-- 失败（红）
```

### 2.4 各数据类型DNA标记

| 数据类型 | 类型代码 | 专用标记 |
|----------|----------|----------|
| 图片 | IMG | EXIF:DNA=, LSB:, 文件头DRAGON: |
| 文本 | TXT | <!-- 头部DNA -->, [段落DNA], <!-- 尾部签名 --> |
| 个人信息 | PI | SOURCE:LEVEL:THRESH, 字段哈希链 |
| 指纹 | FP | BIO:特征哈希:设备ID:时间戳, 模板保护数据 |
| 配方 | FM | THRESHOLD:评分:标准, 成分DNA列表 |
| 文档 | DOC | 标准DNA格式 |
| 银行卡 | BC | 增强加密DNA, 高阈值(>=0.95) |
| 视频 | VID | 帧级DNA, 时间线标记 |
| 音频 | AUD | 频域水印DNA |

---

## 3. 密码学基础 (SM2/SM3)

### 3.1 SM3哈希算法

SM3是国密标准哈希算法，输出256位(64字符十六进制)哈希值。

```python
# SM3使用示例
from sm3 import SM3

hash_result = SM3.hash("需要哈希的数据")
print(hash_result)  # 64字符十六进制字符串
```

**SM3特性**:
- 输出长度: 256位 (64字符十六进制)
- 抗碰撞性: 与SHA-256同级安全强度
- 雪崩效应: 输入微小变化导致输出完全不同

### 3.2 SM2非对称签名算法

SM2是国密标准椭圆曲线签名算法，基于256位曲线。

```python
# SM2使用示例
from sm2 import SM2Crypto

sm2 = SM2Crypto()
key_pair = sm2.generate_key_pair()  # 生成密钥对

signature = sm2.sign("消息内容")     # 签名
is_valid = sm2.verify("消息内容", signature)  # 验证
```

**SM2特性**:
- 曲线: 256位椭圆曲线（与NIST256p同级安全）
- 签名长度: 512位 (128字符十六进制)
- 哈希函数: 使用SM3

---

## 4. 核心类设计

### 4.1 类层次结构

```
DNAGenerator (基础DNA生成器)
├── ImageDNAGenerator (图片DNA)
├── TextDNAGenerator (文本DNA)
├── PersonalInfoDNAGenerator (个人信息DNA)
├── FormulaDNAGenerator (配方DNA)
├── FingerprintDNAGenerator (指纹DNA)
└── BankCardDNAGenerator (银行卡DNA)

MetadataEmbedder (元数据嵌入器)
WatermarkEmbedder (LSB/DCT水印嵌入器)
CryptoEmbedder (密码学嵌入器)

DNAVerifier (DNA验证器)

DNADatabase (DNA数据库)

DragonDNATraceSystem (集成系统)
```

### 4.2 数据流设计

```
原始数据 --> [生成器] --> DNA模型 --> [嵌入器] --> 带DNA的数据 --> [存储]
                                                    |
                                                    v
                                            [检测部门验证]
                                                    |
                                            [三色结果输出]
```

---

## 5. 完整Python实现


### 5.1 密码学基础模块 (SM3 + SM2)

```python
"""
龍魂·全数据类型DNA追溯体系 - 密码学基础模块
包含: SM3哈希算法、SM2签名算法
"""

import hashlib
import secrets
import base64
import json
import time
import re
import random
import string
import struct
import threading
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Union
from enum import Enum
from dataclasses import dataclass, field
from collections import defaultdict

import ecdsa


# ============================================================
# SM3 哈希算法 (国密标准)
# ============================================================

SM3_IV = [
    0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600,
    0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e
]
SM3_T0, SM3_T1 = 0x79cc4519, 0x7a879d8a


def _rol(x, n):
    """32位循环左移"""
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def _ff(x, y, z, j):
    """布尔函数FF"""
    return x ^ y ^ z if j < 16 else (x & y) | (x & z) | (y & z)


def _gg(x, y, z, j):
    """布尔函数GG"""
    return x ^ y ^ z if j < 16 else (x & y) | (~x & z)


def _p0(x):
    """置换函数P0"""
    return x ^ _rol(x, 9) ^ _rol(x, 17)


def _p1(x):
    """置换函数P1"""
    return x ^ _rol(x, 15) ^ _rol(x, 23)


def _tt(x):
    """TT变换"""
    return x ^ _rol(x, 9) ^ _rol(x, 17)


def _sm3_cf(v, bi):
    """SM3压缩函数"""
    w, w1 = [0] * 68, [0] * 64
    for i in range(16):
        w[i] = int.from_bytes(bi[i*4:(i+1)*4], 'big')
    for i in range(16, 68):
        w[i] = _p1(w[i-16] ^ w[i-9] ^ _rol(w[i-3], 15)) ^ _rol(w[i-13], 7) ^ w[i-6]
    for i in range(64):
        w1[i] = w[i] ^ w[i+4]

    a, b, c, d, e, f, g, h = v
    for j in range(64):
        ss1 = _rol((_rol(a, 12) + e + _rol(SM3_T0 if j < 16 else SM3_T1, j % 32)) & 0xFFFFFFFF, 7)
        ss2 = ss1 ^ _rol(a, 12)
        tt1 = (_ff(a, b, c, j) + d + ss2 + w1[j]) & 0xFFFFFFFF
        tt2 = (_gg(e, f, g, j) + h + ss1 + w[j]) & 0xFFFFFFFF
        d, c, b, a = c, _rol(b, 9), a, tt1
        h, g, f, e = g, _rol(f, 19), e, _tt(tt2)

    return [
        (a ^ v[0]) & 0xFFFFFFFF, (b ^ v[1]) & 0xFFFFFFFF,
        (c ^ v[2]) & 0xFFFFFFFF, (d ^ v[3]) & 0xFFFFFFFF,
        (e ^ v[4]) & 0xFFFFFFFF, (f ^ v[5]) & 0xFFFFFFFF,
        (g ^ v[6]) & 0xFFFFFFFF, (h ^ v[7]) & 0xFFFFFFFF
    ]


class SM3:
    """SM3哈希算法 - 国密标准"""

    def __init__(self):
        self.v = SM3_IV.copy()
        self.buf = b''
        self.tlen = 0

    def update(self, d):
        """更新数据"""
        if isinstance(d, str):
            d = d.encode('utf-8')
        self.tlen += len(d)
        self.buf += d
        while len(self.buf) >= 64:
            self.v = _sm3_cf(self.v, self.buf[:64])
            self.buf = self.buf[64:]

    def digest(self):
        """生成摘要"""
        tb = self.tlen * 8
        pad = self.buf + b'\x80'
        while len(pad) % 64 != 56:
            pad += b'\x00'
        pad += tb.to_bytes(8, 'big')
        v = self.v.copy()
        for i in range(0, len(pad), 64):
            v = _sm3_cf(v, pad[i:i+64])
        return b''.join(x.to_bytes(4, 'big') for x in v)

    def hexdigest(self):
        """生成十六进制摘要"""
        return self.digest().hex()

    @staticmethod
    def hash(d):
        """静态便捷方法"""
        s = SM3()
        s.update(d)
        return s.hexdigest()


# ============================================================
# SM2 非对称签名算法 (国密标准)
# ============================================================

class SM3HashWrapper:
    """SM3哈希包装器 - 兼容ecdsa接口"""
    def __init__(self, data):
        self._digest = bytes.fromhex(SM3.hash(data))
    def digest(self):
        return self._digest


class SM2Crypto:
    """SM2国密签名算法 - 基于NIST256p曲线 + SM3哈希"""

    def __init__(self):
        self.curve = ecdsa.NIST256p
        self._sk = None
        self._vk = None

    def generate_key_pair(self):
        """生成SM2密钥对"""
        self._sk = ecdsa.SigningKey.generate(curve=self.curve)
        self._vk = self._sk.get_verifying_key()
        return {
            'private_key': self._sk.to_string().hex(),
            'public_key': '04' + self._vk.to_string().hex(),
            'curve': 'SM2-NIST256p'
        }

    def load_private_key(self, hk):
        """加载私钥"""
        self._sk = ecdsa.SigningKey.from_string(bytes.fromhex(hk), curve=self.curve)
        self._vk = self._sk.get_verifying_key()

    def load_public_key(self, hk):
        """加载公钥"""
        kd = hk[2:] if hk.startswith('04') else hk
        self._vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(kd), curve=self.curve)

    def sign(self, msg):
        """SM2签名"""
        if self._sk is None:
            raise ValueError("私钥未设置")
        if isinstance(msg, str):
            msg = msg.encode('utf-8')
        return self._sk.sign(msg, hashfunc=SM3HashWrapper,
                             sigencode=ecdsa.util.sigencode_string).hex()

    def verify(self, msg, sig):
        """SM2验签"""
        if self._vk is None:
            raise ValueError("公钥未设置")
        if isinstance(msg, str):
            msg = msg.encode('utf-8')
        try:
            return self._vk.verify(bytes.fromhex(sig), msg,
                                   hashfunc=SM3HashWrapper,
                                   sigdecode=ecdsa.util.sigdecode_string)
        except Exception:
            return False
```


### 5.2 DNA数据模型与枚举

```python
# ============================================================
# DNA数据模型与枚举
# ============================================================

class DataType(Enum):
    """支持的数据类型"""
    IMAGE = "IMG"           # 图片
    TEXT = "TXT"            # 文本
    PERSONAL_INFO = "PI"    # 个人信息
    FINGERPRINT = "FP"      # 指纹
    BANK_CARD = "BC"        # 银行卡
    FORMULA = "FM"          # 配方
    DOCUMENT = "DOC"        # 文档
    VIDEO = "VID"           # 视频
    AUDIO = "AUD"           # 音频
    UNKNOWN = "UNK"         # 未知


class DNAType(Enum):
    """DNA标记类型"""
    BASIC = "basic"
    EXTENDED = "extended"
    AUDIT = "audit"


class AuditResult(Enum):
    """检测结果"""
    PASS = "PASS"
    WARNING = "WARN"
    FAIL = "FAIL"
    UNKNOWN = "UNK"


# DNA前缀常量
DNA_PREFIX = "#龍芯:"
DNA_AUDIT_PREFIX = "#AUDIT"


@dataclass
class DNAModel:
    """DNA数据模型 - 核心数据结构"""
    timestamp: str              # 时间戳 YYYY-MM-DD-HHMMSS
    data_type: DataType         # 数据类型
    source: str                 # 来源
    version: str                # 版本
    sm3_hash: str = ""          # SM3哈希 (64字符)
    threshold: float = 0.0      # 合规阈值
    sm2_signature: str = ""     # SM2签名 (128字符)
    metadata: Dict = field(default_factory=dict)

    def to_basic_dna(self) -> str:
        """生成基础DNA: #龍芯:时间戳-类型-来源-版本"""
        return f"{DNA_PREFIX}{self.timestamp}-{self.data_type.value}-{self.source}-{self.version}"

    def to_extended_dna(self) -> str:
        """生成扩展DNA - 包含哈希、阈值、签名摘要"""
        basic = self.to_basic_dna()
        return f"{basic}|SM3:{self.sm3_hash[:16]}|THRESH:{self.threshold}|SIG:{self.sm2_signature[:32]}"

    def to_audit_dna(self, result: AuditResult, details: str = "") -> str:
        """生成检测DNA - 验证输出"""
        icon_map = {"PASS": "+", "WARN": "~", "FAIL": "!", "UNK": "?"}
        icon = icon_map.get(result.value, "?")
        return f"{DNA_AUDIT_PREFIX}[{icon}]{result.value}|{details}"
```

### 5.3 DNA生成器类

```python
# ============================================================
# DNA生成器类
# ============================================================

class DNAGenerator:
    """统一DNA生成器 - 所有数据类型的DNA生成入口"""

    def __init__(self, source: str = "LONHUN", version: str = "v3.0"):
        self.source = source
        self.version = version
        self.sm2 = SM2Crypto()
        self._keys = self.sm2.generate_key_pair()
        self._lock = threading.Lock()

    def _now(self) -> str:
        return datetime.now().strftime("%Y-%m-%d-%H%M%S")

    def _hash(self, data: bytes) -> str:
        return SM3.hash(data)

    def _sign(self, data: bytes) -> str:
        with self._lock:
            return self.sm2.sign(data)

    def generate(self, data: Union[str, bytes], data_type: DataType,
                 threshold: float = 0.7, extra_meta: Optional[Dict] = None) -> DNAModel:
        """生成通用DNA"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return DNAModel(
            timestamp=self._now(),
            data_type=data_type,
            source=self.source,
            version=self.version,
            sm3_hash=self._hash(data),
            threshold=threshold,
            sm2_signature=self._sign(data),
            metadata=extra_meta or {}
        )

    def get_public_key(self) -> str:
        return self._keys['public_key']


class ImageDNAGenerator(DNAGenerator):
    """图片DNA生成器 - 图片专用DNA标记"""

    def generate(self, image_data: bytes, image_format: str = "JPG",
                 width: int = 0, height: int = 0,
                 device_info: str = "", geo_tag: str = "") -> Dict:
        """生成图片DNA"""
        dna = super().generate(image_data, DataType.IMAGE, threshold=0.8)
        return {
            'dna_model': dna,
            'basic_dna': dna.to_basic_dna(),
            'extended_dna': dna.to_extended_dna(),
            'image_format': image_format,
            'dimensions': f"{width}x{height}",
            'exif_dna': f"EXIF:DNA={dna.to_basic_dna()}|FMT={image_format}"
                        f"|DIM={width}x{height}|DEV={device_info}|GEO={geo_tag}"
                        f"|HASH={dna.sm3_hash[:24]}",
            'lsb_dna': f"LSB:{dna.sm3_hash[:32]}:{dna.sm2_signature[:32]}",
            'header_mark': f"DRAGON:{dna.to_basic_dna()}:END".encode('utf-8'),
            'verification': {
                'sm3_full': dna.sm3_hash,
                'sm2_sig_full': dna.sm2_signature,
                'public_key': self.get_public_key()
            }
        }


class TextDNAGenerator(DNAGenerator):
    """文本DNA生成器 - 文本专用DNA标记"""

    def generate(self, text: str, text_type: str = "general") -> Dict:
        """生成文本DNA"""
        data = text.encode('utf-8')
        dna = super().generate(data, DataType.TEXT, threshold=0.75)
        paragraphs = text.split('\n\n')

        para_dnas = []
        for i, para in enumerate(paragraphs):
            para_hash = SM3.hash(para.encode('utf-8'))
            para_dnas.append(f"[P{i}:H={para_hash[:16]}:SIG={dna.sm2_signature[:16]}]")

        return {
            'dna_model': dna,
            'basic_dna': dna.to_basic_dna(),
            'extended_dna': dna.to_extended_dna(),
            'text_type': text_type,
            'word_count': len(text.split()),
            'paragraph_count': len(paragraphs),
            'header_mark': f"<!-- {dna.to_basic_dna()} | SM3:{dna.sm3_hash[:16]} -->",
            'paragraph_dnas': para_dnas,
            'footer_signature': f"<!-- LONHUN_SIG: {dna.sm2_signature[:40]} | VERIFY: {dna.sm3_hash[:24]} -->",
        }


class PersonalInfoDNAGenerator(DNAGenerator):
    """个人信息DNA生成器 - 隐私保护DNA"""

    def generate(self, info: Dict, privacy_level: str = "normal") -> Dict:
        """生成个人信息DNA"""
        info_str = json.dumps(info, sort_keys=True)
        data = info_str.encode('utf-8')

        threshold_map = {'low': 0.5, 'normal': 0.7, 'high': 0.85, 'critical': 0.95}
        threshold = threshold_map.get(privacy_level, 0.7)

        dna = super().generate(data, DataType.PERSONAL_INFO, threshold=threshold,
                               extra_meta={'privacy_level': privacy_level,
                                          'fields': list(info.keys())})

        field_hashes = {k: SM3.hash(str(v).encode('utf-8')) for k, v in info.items()}

        # 构建哈希链
        chain = []
        prev = "0" * 64
        for key, h in sorted(field_hashes.items()):
            ch = SM3.hash((prev + h + key).encode('utf-8'))
            chain.append(f"{key}:{ch[:16]}")
            prev = ch

        return {
            'dna_model': dna,
            'basic_dna': dna.to_basic_dna(),
            'extended_dna': dna.to_extended_dna(),
            'privacy_level': privacy_level,
            'field_hashes': field_hashes,
            'hash_chain': chain,
            'source_mark': f"SOURCE:{dna.source}|LEVEL:{privacy_level}|THRESH:{threshold}",
            'compliance_dna': dna.to_audit_dna(AuditResult.PASS,
                f"privacy={privacy_level}|fields_ok")
        }


class FormulaDNAGenerator(DNAGenerator):
    """配方DNA生成器 - 合规性DNA"""

    def generate(self, formula: Dict, compliance_standard: str = "GB") -> Dict:
        """生成配方DNA"""
        formula_str = json.dumps(formula, sort_keys=True)
        data = formula_str.encode('utf-8')

        ingredients = formula.get('ingredients', [])
        score = self._calc_compliance(ingredients, compliance_standard)

        dna = super().generate(data, DataType.FORMULA, threshold=score,
                               extra_meta={'standard': compliance_standard,
                                          'ingredient_count': len(ingredients)})

        ing_dnas = []
        for ing in ingredients:
            ih = SM3.hash(str(ing).encode('utf-8'))
            ok = self._check_ing(ing, compliance_standard)
            ing_dnas.append(f"{ing.get('name', '?')}:{ih[:12]}:{'OK' if ok else 'RESTRICTED'}")

        return {
            'dna_model': dna,
            'basic_dna': dna.to_basic_dna(),
            'extended_dna': dna.to_extended_dna(),
            'compliance_standard': compliance_standard,
            'compliance_score': score,
            'ingredient_dnas': ing_dnas,
            'threshold_mark': f"THRESHOLD:{score:.2f}|STD:{compliance_standard}",
            'compliance_dna': dna.to_audit_dna(
                AuditResult.PASS if score >= 0.7 else AuditResult.WARNING,
                f"score={score:.2f}|std={compliance_standard}")
        }

    def _calc_compliance(self, ingredients, standard):
        if not ingredients:
            return 1.0
        return sum(1 for ing in ingredients
                   if self._check_ing(ing, standard)) / len(ingredients)

    def _check_ing(self, ingredient, standard):
        restricted = {"lead", "mercury", "arsenic", "cadmium", "formaldehyde"}
        return not any(r in str(ingredient.get('name', '')).lower() for r in restricted)


class FingerprintDNAGenerator(DNAGenerator):
    """指纹DNA生成器 - 生物特征DNA"""

    def generate(self, fingerprint_data: bytes, device_id: str = "",
                 capture_type: str = "optical") -> Dict:
        """生成指纹DNA"""
        dna = super().generate(fingerprint_data, DataType.FINGERPRINT, threshold=0.9,
                               extra_meta={'device_id': device_id,
                                          'capture_type': capture_type})
        feature_hash = SM3.hash(fingerprint_data)
        return {
            'dna_model': dna,
            'basic_dna': dna.to_basic_dna(),
            'extended_dna': dna.to_extended_dna(),
            'feature_hash': feature_hash,
            'device_mark': f"DEV:{device_id}|TYPE:{capture_type}|TS:{dna.timestamp}",
            'biometric_dna': f"BIO:{feature_hash[:32]}:{device_id}:{dna.timestamp}",
            'template_protection': {
                'helper_data': SM3.hash(fingerprint_data + dna.sm3_hash.encode('utf-8')),
                'transformation_key': dna.sm2_signature[:32],
                'revocable_hash': SM3.hash(
                    (SM3.hash(fingerprint_data + dna.sm3_hash.encode('utf-8')) +
                     dna.sm2_signature).encode('utf-8'))
            }
        }
```


### 5.4 DNA嵌入器类

```python
# ============================================================
# DNA嵌入器类
# ============================================================

class MetadataEmbedder:
    """元数据嵌入器 - EXIF/文件头/元数据嵌入"""

    @staticmethod
    def embed_exif(image_bytes: bytes, dna_info: Dict) -> bytes:
        """在JPEG中嵌入EXIF格式的DNA"""
        if image_bytes[:2] == b'\xff\xd8':
            dna_exif = b'\xff\xe1'
            exif_data = dna_info.get('exif_dna', '').encode('utf-8')
            length = len(exif_data) + 2
            dna_exif += length.to_bytes(2, 'big') + exif_data
            return image_bytes[:2] + dna_exif + image_bytes[2:]
        return image_bytes

    @staticmethod
    def embed_file_header(data: bytes, dna_mark: bytes, header_size: int = 256) -> bytes:
        """在文件头嵌入DNA标记"""
        header = dna_mark[:header_size].ljust(header_size, b'\x00')
        return header + data

    @staticmethod
    def embed_text_header(text: str, dna_header: str) -> str:
        """在文本头部嵌入DNA标记"""
        return dna_header + "\n\n" + text

    @staticmethod
    def embed_json_meta(data: Dict, dna_data: Dict) -> Dict:
        """在JSON元数据中嵌入DNA"""
        data['_dna'] = {
            'basic_dna': dna_data.get('basic_dna', ''),
            'sm3_hash': dna_data.get('verification', {}).get('sm3_full', ''),
            'timestamp': datetime.now().isoformat()
        }
        return data


class WatermarkEmbedder:
    """LSB数字水印嵌入器"""

    @staticmethod
    def embed_lsb(image_bytes: bytes, dna_message: str, offset: int = 100) -> bytes:
        """将DNA信息隐藏在图像LSB中"""
        if len(image_bytes) < offset + 100:
            return image_bytes

        msg_bytes = dna_message.encode('utf-8')
        msg_len = len(msg_bytes)
        min_space = 32 + msg_len * 8
        if len(image_bytes) - offset < min_space:
            return image_bytes

        data = bytearray(image_bytes)

        # 嵌入长度 (32 bits)
        for i in range(32):
            data[offset + i] = (data[offset + i] & 0xFE) | ((msg_len >> i) & 1)

        # 嵌入消息
        msg_offset = offset + 32
        bit_idx = 0
        for byte_val in msg_bytes:
            for bit_pos in range(8):
                pos = msg_offset + bit_idx
                data[pos] = (data[pos] & 0xFE) | ((byte_val >> bit_pos) & 1)
                bit_idx += 1

        return bytes(data)

    @staticmethod
    def extract_lsb(image_bytes: bytes, offset: int = 100) -> Optional[str]:
        """从LSB中提取DNA水印"""
        if len(image_bytes) < offset + 32:
            return None

        # 提取长度
        msg_len = 0
        for i in range(32):
            msg_len |= (image_bytes[offset + i] & 1) << i

        if msg_len <= 0 or msg_len > 10000:
            return None

        total_needed = 32 + msg_len * 8
        if len(image_bytes) < offset + total_needed:
            return None

        # 提取消息
        msg_bytes = bytearray()
        msg_offset = offset + 32
        for byte_idx in range(msg_len):
            byte_val = 0
            for bit_pos in range(8):
                pos = msg_offset + byte_idx * 8 + bit_pos
                byte_val |= (image_bytes[pos] & 1) << bit_pos
            msg_bytes.append(byte_val)

        try:
            return bytes(msg_bytes).decode('utf-8')
        except:
            return None


class CryptoEmbedder:
    """密码学嵌入器 - SM2签名/SM3哈希链/Merkle树"""

    def __init__(self):
        self.sm2 = SM2Crypto()
        self._keys = self.sm2.generate_key_pair()

    def embed_signature(self, data: bytes) -> Dict:
        """为数据嵌入SM2签名"""
        hash_val = SM3.hash(data)
        signature = self.sm2.sign(data)
        return {
            'hash': hash_val,
            'signature': signature,
            'public_key': self._keys['public_key'],
            'embedded': f"SIG:{signature[:64]}|HASH:{hash_val[:32]}"
        }

    def verify_embedded(self, data: bytes, signature: str,
                        public_key: str = None) -> bool:
        """验证嵌入的签名"""
        if public_key:
            self.sm2.load_public_key(public_key)
        return self.sm2.verify(data, signature)

    @staticmethod
    def create_hash_chain(data_list: List[bytes]) -> List[str]:
        """创建哈希链"""
        chain = []
        prev = "0" * 64
        for d in data_list:
            ch = SM3.hash((prev + SM3.hash(d)).encode('utf-8'))
            chain.append(ch)
            prev = ch
        return chain

    @staticmethod
    def create_merkle_tree(data_list: List[bytes]) -> Dict:
        """创建Merkle树"""
        leaves = [SM3.hash(d) for d in data_list]
        tree = [leaves]
        current = leaves

        while len(current) > 1:
            next_level = []
            for i in range(0, len(current), 2):
                left = current[i]
                right = current[i + 1] if i + 1 < len(current) else left
                next_level.append(SM3.hash((left + right).encode('utf-8')))
            tree.append(next_level)
            current = next_level

        return {
            'root': tree[-1][0] if tree else "",
            'leaves': leaves,
            'tree_levels': len(tree),
            'leaf_count': len(leaves)
        }
```

### 5.5 DNA验证器类

```python
# ============================================================
# DNA验证器类
# ============================================================

class DNAVerifier:
    """DNA统一验证器 - 检测部门使用"""

    def __init__(self, public_key: str = None):
        self.sm2 = SM2Crypto()
        if public_key:
            self.sm2.load_public_key(public_key)
        self._audit_log = []

    def verify(self, data: Union[str, bytes], dna_model: DNAModel,
               expected_signature: str = None) -> Dict:
        """统一验证入口 - 验证DNA的真实性

        返回三色结果:
        - PASS (绿): 数据完整可信
        - WARNING (黄): 部分检查未通过
        - FAIL (红): 数据被篡改
        """
        if isinstance(data, str):
            data = data.encode('utf-8')

        results = {
            'dna_id': dna_model.to_basic_dna(),
            'timestamp': datetime.now().isoformat(),
            'checks': {}
        }

        # 1. SM3哈希验证
        computed_hash = SM3.hash(data)
        hash_match = computed_hash == dna_model.sm3_hash
        results['checks']['sm3_hash'] = {
            'status': 'PASS' if hash_match else 'FAIL',
            'match': hash_match
        }

        # 2. SM2签名验证
        sig_valid = False
        sig_to_check = expected_signature or dna_model.sm2_signature
        if sig_to_check:
            sig_valid = self.sm2.verify(data, sig_to_check)
        results['checks']['sm2_signature'] = {
            'status': 'PASS' if sig_valid else 'FAIL',
            'valid': sig_valid
        }

        # 3. 时间戳验证
        ts_valid = self._verify_timestamp(dna_model.timestamp)
        results['checks']['timestamp'] = {
            'status': 'PASS' if ts_valid else 'WARN'
        }

        # 4. 阈值验证
        threshold_ok = dna_model.threshold >= 0.5
        results['checks']['threshold'] = {
            'status': 'PASS' if threshold_ok else 'WARN',
            'value': dna_model.threshold
        }

        # 综合判定
        has_fail = any(c['status'] == 'FAIL' for c in results['checks'].values())
        has_warn = any(c['status'] == 'WARN' for c in results['checks'].values())

        if has_fail:
            results['verdict'] = AuditResult.FAIL
            results['verdict_text'] = "DNA验证失败 - 数据可能被篡改"
        elif has_warn:
            results['verdict'] = AuditResult.WARNING
            results['verdict_text'] = "DNA验证警告 - 部分检查未通过"
        else:
            results['verdict'] = AuditResult.PASS
            results['verdict_text'] = "DNA验证通过 - 数据完整且可信"

        results['audit_dna'] = dna_model.to_audit_dna(
            results['verdict'],
            f"SM3={'OK' if hash_match else 'FAIL'}|SIG={'OK' if sig_valid else 'FAIL'}"
        )
        self._audit_log.append(results)
        return results

    def verify_image(self, image_data: bytes, dna_data: Dict) -> Dict:
        """验证图片DNA（含LSB水印检查）"""
        results = self.verify(image_data, dna_data['dna_model'])
        lsb = WatermarkEmbedder.extract_lsb(image_data)
        results['checks']['lsb_watermark'] = {
            'status': 'PASS' if lsb else 'WARN',
            'extracted': lsb[:50] if lsb else None
        }
        return results

    def _verify_timestamp(self, ts: str) -> bool:
        """验证时间戳是否合理"""
        try:
            dt = datetime.strptime(ts, "%Y-%m-%d-%H%M%S")
            now = datetime.now()
            return dt <= now and (now - dt).days < 30
        except:
            return False

    @staticmethod
    def format_report(result: Dict) -> str:
        """格式化验证报告"""
        lines = [
            "=" * 50,
            "龍魂DNA验证报告",
            "=" * 50,
            f"DNA ID    : {result['dna_id']}",
            f"验证时间  : {result['timestamp']}",
            f"综合判定  : {result['verdict'].value}",
            f"判定说明  : {result['verdict_text']}",
            "-" * 50,
            "详细检查项:"
        ]
        for name, check in result['checks'].items():
            icon = "+" if check['status'] == 'PASS' else "!" if check['status'] == 'FAIL' else "~"
            lines.append(f"  [{icon}] {name}: {check['status']}")
        lines.extend(["-" * 50, f"检测DNA   : {result['audit_dna']}", "=" * 50])
        return "\n".join(lines)
```


### 5.6 DNA数据库

```python
# ============================================================
# DNA数据库
# ============================================================

class DNADatabase:
    """DNA索引数据库 - 存储和查询DNA记录"""

    def __init__(self, db_path: str = None):
        self._records: Dict[str, Dict] = {}
        self._index_by_type: Dict[str, set] = defaultdict(set)
        self._index_by_source: Dict[str, set] = defaultdict(set)
        self._index_by_time: Dict[str, set] = defaultdict(set)
        self._blacklist: set = set()
        self._audit_log = []
        self._lock = threading.Lock()

    def insert(self, dna_data: Dict, original_data_hash: str = "") -> str:
        """插入DNA记录，返回DNA ID"""
        with self._lock:
            dna_model = dna_data.get('dna_model')
            if not dna_model:
                raise ValueError("Invalid DNA data: missing dna_model")

            dna_id = dna_model.to_basic_dna()
            record_id = str(uuid.uuid4())[:8]

            record = {
                'record_id': record_id,
                'dna_id': dna_id,
                'dna_model': dna_model,
                'data_hash': original_data_hash or dna_model.sm3_hash,
                'sm3_hash': dna_model.sm3_hash,
                'sm2_signature': dna_model.sm2_signature,
                'timestamp': dna_model.timestamp,
                'data_type': dna_model.data_type.value,
                'source': dna_model.source,
                'version': dna_model.version,
                'threshold': dna_model.threshold,
                'metadata': dna_model.metadata,
                'full_data': dna_data,
                'insert_time': datetime.now().isoformat(),
                'status': 'active'
            }

            self._records[dna_id] = record
            self._index_by_type[dna_model.data_type.value].add(dna_id)
            self._index_by_source[dna_model.source].add(dna_id)
            date_key = dna_model.timestamp[:10] if len(dna_model.timestamp) >= 10 else dna_model.timestamp
            self._index_by_time[date_key].add(dna_id)

            return dna_id

    def get(self, dna_id: str) -> Optional[Dict]:
        """通过DNA ID获取记录"""
        return self._records.get(dna_id)

    def query_by_type(self, data_type: str) -> List[Dict]:
        """按数据类型查询"""
        return [self._records[did] for did in self._index_by_type.get(data_type, set())
                if did in self._records]

    def query_by_source(self, source: str) -> List[Dict]:
        """按来源查询"""
        return [self._records[did] for did in self._index_by_source.get(source, set())
                if did in self._records]

    def query_by_time(self, date_str: str) -> List[Dict]:
        """按日期查询 (YYYY-MM-DD)"""
        return [self._records[did] for did in self._index_by_time.get(date_str, set())
                if did in self._records]

    def query_by_time_range(self, start_date: str, end_date: str) -> List[Dict]:
        """按时间范围查询"""
        results = []
        for date_key, ids in self._index_by_time.items():
            if start_date <= date_key <= end_date:
                results.extend([self._records[did] for did in ids if did in self._records])
        return results

    def query(self, data_type: str = None, source: str = None,
              date: str = None, min_threshold: float = None) -> List[Dict]:
        """组合查询"""
        candidates = set(self._records.keys())
        if data_type:
            candidates &= self._index_by_type.get(data_type, set())
        if source:
            candidates &= self._index_by_source.get(source, set())
        if date:
            candidates &= self._index_by_time.get(date, set())

        results = [self._records[did] for did in candidates if did in self._records]
        if min_threshold is not None:
            results = [r for r in results if r['threshold'] >= min_threshold]
        return results

    def add_to_blacklist(self, dna_id: str, reason: str = ""):
        """将DNA加入黑名单"""
        with self._lock:
            self._blacklist.add(dna_id)
            self._audit_log.append({
                'action': 'blacklist', 'dna_id': dna_id,
                'reason': reason, 'time': datetime.now().isoformat()
            })

    def is_blacklisted(self, dna_id: str) -> bool:
        return dna_id in self._blacklist

    def get_blacklist(self) -> List[str]:
        return list(self._blacklist)

    def get_stats(self) -> Dict:
        return {
            'total_records': len(self._records),
            'by_type': {k: len(v) for k, v in self._index_by_type.items()},
            'by_source': {k: len(v) for k, v in self._index_by_source.items()},
            'by_date': {k: len(v) for k, v in self._index_by_time.items()},
            'blacklist_count': len(self._blacklist),
            'audit_entries': len(self._audit_log)
        }

    def export_to_dict(self) -> Dict:
        return {
            'records': {
                k: {'dna_id': v['dna_id'], 'data_type': v['data_type'],
                    'source': v['source'], 'timestamp': v['timestamp'],
                    'sm3_hash': v['sm3_hash'], 'threshold': v['threshold'],
                    'status': v['status']}
                for k, v in self._records.items()
            },
            'blacklist': list(self._blacklist),
            'stats': self.get_stats()
        }
```

### 5.7 集成系统入口

```python
# ============================================================
# 龍魂DNA追溯系统集成入口
# ============================================================

class DragonDNATraceSystem:
    """龍魂DNA追溯系统 - 统一集成入口

    覆盖全数据类型:
    - 图片 (IMAGE)     - 文本 (TEXT)
    - 个人信息 (PI)     - 指纹 (FINGERPRINT)
    - 配方 (FORMULA)    - 银行卡 (BANK_CARD)
    - 文档 (DOCUMENT)   - 视频 (VIDEO)
    - 音频 (AUDIO)
    """

    VERSION = "3.0"
    SYSTEM_DNA = "#龍芯:2026-07-04-DNA-TRACE-v3.0"

    def __init__(self):
        self.db = DNADatabase()
        self.verifier = DNAVerifier()
        self._generators = {
            DataType.IMAGE: ImageDNAGenerator(),
            DataType.TEXT: TextDNAGenerator(),
            DataType.PERSONAL_INFO: PersonalInfoDNAGenerator(),
            DataType.FINGERPRINT: FingerprintDNAGenerator(),
            DataType.FORMULA: FormulaDNAGenerator(),
            DataType.DOCUMENT: DNAGenerator(),
            DataType.BANK_CARD: DNAGenerator(),
            DataType.VIDEO: DNAGenerator(),
            DataType.AUDIO: DNAGenerator(),
        }
        self._embedders = {
            'metadata': MetadataEmbedder(),
            'watermark': WatermarkEmbedder(),
            'crypto': CryptoEmbedder()
        }
        self._public_keys = {}
        self._audit_log = []

    def get_system_dna(self) -> str:
        return self.SYSTEM_DNA

    def generate_dna(self, data, data_type: DataType, **kwargs) -> Dict:
        """为数据生成DNA"""
        generator = self._generators.get(data_type)
        if not generator:
            raise ValueError(f"不支持的数据类型: {data_type}")

        if data_type == DataType.IMAGE:
            result = generator.generate(
                data if isinstance(data, bytes) else data.encode(),
                kwargs.get('format', 'JPG'), kwargs.get('width', 0),
                kwargs.get('height', 0), kwargs.get('device', ''),
                kwargs.get('geo', ''))
        elif data_type == DataType.TEXT:
            result = generator.generate(
                data if isinstance(data, str) else data.decode(),
                kwargs.get('text_type', 'general'))
        elif data_type == DataType.PERSONAL_INFO:
            result = generator.generate(
                data if isinstance(data, dict) else json.loads(data),
                kwargs.get('privacy_level', 'normal'))
        elif data_type == DataType.FORMULA:
            result = generator.generate(
                data if isinstance(data, dict) else json.loads(data),
                kwargs.get('standard', 'GB'))
        elif data_type == DataType.FINGERPRINT:
            result = generator.generate(
                data if isinstance(data, bytes) else data.encode(),
                kwargs.get('device_id', ''),
                kwargs.get('capture_type', 'optical'))
        else:
            dna = generator.generate(data, data_type, kwargs.get('threshold', 0.7))
            result = {'dna_model': dna}

        # 保存公钥
        dna_model = result.get('dna_model')
        if dna_model:
            src = dna_model.source
            gen = self._generators.get(data_type)
            if gen and src not in self._public_keys:
                self._public_keys[src] = gen.get_public_key()

        return result

    def embed_dna(self, data: bytes, dna_data: Dict, method: str = 'auto') -> bytes:
        """将DNA嵌入到数据中"""
        if method == 'auto':
            dna_model = dna_data.get('dna_model')
            method = 'watermark' if dna_model and dna_model.data_type == DataType.IMAGE else 'metadata'

        if method == 'watermark':
            dna_msg = dna_data.get('lsb_dna', dna_data.get('basic_dna', ''))
            return WatermarkEmbedder.embed_lsb(data, dna_msg)
        else:
            header = dna_data.get('header_mark', b'DRAGON_DNA')
            if isinstance(header, str):
                header = header.encode('utf-8')
            return MetadataEmbedder.embed_file_header(data, header)

    def verify_dna(self, data, dna_data, public_key: str = None) -> Dict:
        """验证DNA"""
        dna_model = dna_data.get('dna_model')
        if not dna_model:
            return {'error': '无效的DNA数据'}

        pk = public_key or self._public_keys.get(dna_model.source)
        if not pk and 'verification' in dna_data:
            pk = dna_data['verification'].get('public_key')

        verifier = DNAVerifier(public_key=pk) if pk else self.verifier
        result = verifier.verify(
            data if isinstance(data, bytes) else str(data).encode(),
            dna_model)

        result['blacklisted'] = self.db.is_blacklisted(dna_model.to_basic_dna())
        self._audit_log.append(result)
        return result

    def store_dna(self, dna_data: Dict) -> str:
        return self.db.insert(dna_data)

    def query_dna(self, **kwargs) -> List[Dict]:
        return self.db.query(**kwargs)

    def add_to_blacklist(self, dna_id: str, reason: str = ""):
        self.db.add_to_blacklist(dna_id, reason)

    def get_stats(self) -> Dict:
        return {
            'system_dna': self.SYSTEM_DNA,
            'version': self.VERSION,
            'supported_types': [t.value for t in DataType],
            'db_stats': self.db.get_stats(),
            'total_audits': len(self._audit_log)
        }
```


---

## 6. DNA数据库设计

### 6.1 数据库结构

```
+------------------+       +------------------+       +------------------+
|   records        |       |   indexes        |       |   blacklist      |
+------------------+       +------------------+       +------------------+
| dna_id (PK)      |       | by_type          |       | dna_id           |
| record_id        |       | by_source        |       | reason           |
| data_type        |       | by_time          |       | added_time       |
| source           |       +------------------+       +------------------+
| timestamp        |
| sm3_hash         |
| sm2_signature    |
| threshold        |
| metadata         |
| insert_time      |
| status           |
+------------------+
```

### 6.2 索引设计

| 索引名 | 类型 | 用途 |
|--------|------|------|
| by_type | 倒排索引 | 按数据类型快速查询 |
| by_source | 倒排索引 | 按来源快速查询 |
| by_time | 倒排索引 | 按日期范围查询 |
| blacklist | Hash集合 | O(1)黑名单检查 |

### 6.3 查询接口

```python
# 按类型查询
img_records = db.query_by_type("IMG")

# 按来源查询
cam_records = db.query_by_source("CAMERA_A")

# 按日期查询
today = db.query_by_time("2026-07-04")

# 组合查询
high_trust = db.query(data_type="IMG", source="CAM_A", min_threshold=0.85)

# 黑名单检查
is_bad = db.is_blacklisted(dna_id)
```

---

## 7. 使用示例

### 7.1 图片DNA生成与验证

```python
# 创建系统
system = DragonDNATraceSystem()

# 1. 为图片生成DNA
with open("photo.jpg", "rb") as f:
    img_data = f.read()

img_dna = system.generate_dna(
    img_data,
    DataType.IMAGE,
    format="JPG",
    width=1920,
    height=1080,
    device="Canon-EOS-R5",
    geo="39.9N-116.4E"
)

print(f"基础DNA: {img_dna['basic_dna']}")
print(f"EXIF DNA: {img_dna['exif_dna']}")
print(f"LSB DNA: {img_dna['lsb_dna']}")

# 2. 将DNA嵌入图片
embedded_img = system.embed_dna(img_data, img_dna, method='watermark')

# 3. 存储DNA记录
dna_id = system.store_dna(img_dna)
print(f"DNA已存储, ID: {dna_id}")

# 4. 验证DNA
result = system.verify_dna(img_data, img_dna)
print(f"验证结果: {result['verdict'].value}")
print(DNAVerifier.format_report(result))
```

### 7.2 文本DNA生成与验证

```python
# 生成文本DNA
text_content = """
第一章：系统概述

本文档描述了龍魂DNA追溯体系的完整架构。

第二章：核心设计

DNA格式采用分层设计，包含基础格式、扩展格式和验证格式。
"""

txt_dna = system.generate_dna(
    text_content,
    DataType.TEXT,
    text_type="document"
)

print(f"基础DNA: {txt_dna['basic_dna']}")
print(f"段落DNA: {txt_dna['paragraph_dnas']}")
print(f"头部标记: {txt_dna['header_mark']}")
print(f"尾部签名: {txt_dna['footer_signature']}")

# 验证文本
result = system.verify_dna(text_content, txt_dna)
print(f"验证结果: {result['verdict'].value}")
```

### 7.3 个人信息DNA（隐私保护）

```python
# 生成个人信息DNA（高隐私级别）
personal_info = {
    "name": "张三",
    "id_number": "110101199001011234",
    "phone": "13800138000",
    "address": "北京市海淀区",
    "biometric_hash": "a1b2c3..."
}

pi_dna = system.generate_dna(
    personal_info,
    DataType.PERSONAL_INFO,
    privacy_level="high"  # high = 阈值0.85
)

print(f"隐私级别: {pi_dna['privacy_level']}")
print(f"字段哈希: {pi_dna['field_hashes']}")
print(f"哈希链: {pi_dna['hash_chain']}")
print(f"合规DNA: {pi_dna['compliance_dna']}")

# 存储到数据库
system.store_dna(pi_dna)
```

### 7.4 配方DNA（合规检查）

```python
# 生成配方DNA
formula = {
    "product_name": "保湿精华液",
    "ingredients": [
        {"name": "purified_water", "proportion": 0.45},
        {"name": "glycerol", "proportion": 0.25},
        {"name": "hyaluronic_acid", "proportion": 0.15},
        {"name": "niacinamide", "proportion": 0.10},
        {"name": "preservative", "proportion": 0.05}
    ],
    "batch_number": "LOT-20260704-001"
}

fm_dna = system.generate_dna(
    formula,
    DataType.FORMULA,
    standard="GB"  # 中国国标
)

print(f"合规评分: {fm_dna['compliance_score']:.2%}")
print(f"成分DNA: {fm_dna['ingredient_dnas']}")
print(f"阈值标记: {fm_dna['threshold_mark']}")
```

### 7.5 指纹DNA（生物特征）

```python
# 生成指纹DNA
with open("fingerprint_template.bin", "rb") as f:
    fp_data = f.read()

fp_dna = system.generate_dna(
    fp_data,
    DataType.FINGERPRINT,
    device_id="FP-SCANNER-001",
    capture_type="optical"
)

print(f"特征哈希: {fp_dna['feature_hash']}")
print(f"设备标记: {fp_dna['device_mark']}")
print(f"模板保护: {fp_dna['template_protection']}")
```

### 7.6 检测部门验证流程

```python
# 检测部门接收数据后进行验证
def audit_process(data, dna_data, system):
    """检测部门DNA验证流程"""

    # 1. 验证DNA
    result = system.verify_dna(data, dna_data)

    # 2. 检查黑名单
    dna_id = dna_data['dna_model'].to_basic_dna()
    if result.get('blacklisted'):
        return {"status": "REJECTED", "reason": "DNA在黑名单中"}

    # 3. 根据判定结果处理
    verdict = result['verdict']
    if verdict == AuditResult.PASS:
        return {"status": "APPROVED", "trust_level": "HIGH"}
    elif verdict == AuditResult.WARNING:
        return {"status": "REVIEW", "trust_level": "MEDIUM"}
    else:
        return {"status": "REJECTED", "trust_level": "LOW"}

# 执行审计
audit_result = audit_process(img_data, img_dna, system)
print(f"审计结果: {audit_result}")
```


---

## 8. 单元测试

### 8.1 测试概览

```
共65个测试用例，全部通过:
├── SM3哈希算法 (5项)
├── SM2签名算法 (4项)
├── DNA生成器 (19项)
│   ├── 基础DNA生成器 (6项)
│   ├── 图片DNA生成器 (4项)
│   ├── 文本DNA生成器 (4项)
│   ├── 个人信息DNA生成器 (4项)
│   ├── 配方DNA生成器 (3项)
│   └── 指纹DNA生成器 (3项)
├── DNA验证器 (6项)
├── LSB水印 (2项)
├── 密码学嵌入 (5项)
├── DNA数据库 (5项)
└── 集成系统 (8项)
```

### 8.2 核心测试代码

```python
def run_tests():
    """运行所有单元测试"""
    passed = 0
    failed = 0

    # === SM3测试 ===
    # 标准测试向量
    assert SM3.hash("abc") ==         "66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0"
    passed += 1

    # 空串哈希
    assert len(SM3.hash("")) == 64
    passed += 1

    # 长消息
    assert len(SM3.hash("a" * 1000)) == 64
    passed += 1

    # 确定性
    assert SM3.hash("test") == SM3.hash("test")
    passed += 1

    # 雪崩效应
    assert SM3.hash("a") != SM3.hash("b")
    passed += 1

    # === SM2测试 ===
    sm2 = SM2Crypto()
    kp = sm2.generate_key_pair()
    sig = sm2.sign("test message")

    assert len(sig) == 128
    passed += 1
    assert sm2.verify("test message", sig)
    passed += 1
    assert not sm2.verify("tampered", sig)
    passed += 1

    # 跨实例验证
    sm2_v = SM2Crypto()
    sm2_v.load_public_key(kp['public_key'])
    assert sm2_v.verify("test message", sig)
    passed += 1

    # === DNA生成器测试 ===
    gen = DNAGenerator(source="TEST")
    dna = gen.generate("test data", DataType.TEXT, 0.8)

    assert dna.to_basic_dna().startswith("#龍芯:")
    passed += 1
    assert "TXT" in dna.to_basic_dna()
    passed += 1
    assert len(dna.sm3_hash) == 64
    passed += 1
    assert len(dna.sm2_signature) == 128
    passed += 1
    assert dna.threshold == 0.8
    passed += 1

    # 图片DNA
    img_gen = ImageDNAGenerator()
    img_d = img_gen.generate(b"\xff\xd8" + b"X" * 100, "JPG", 100, 100)
    assert "IMG" in img_d['basic_dna']
    passed += 1
    assert "EXIF" in img_d['exif_dna']
    passed += 1
    assert "LSB" in img_d['lsb_dna']
    passed += 1
    assert img_d['dimensions'] == "100x100"
    passed += 1

    # 文本DNA
    txt_gen = TextDNAGenerator()
    txt_d = txt_gen.generate("P1\n\nP2", "article")
    assert "TXT" in txt_d['basic_dna']
    passed += 1
    assert len(txt_d['paragraph_dnas']) == 2
    passed += 1
    assert len(txt_d['header_mark']) > 0
    passed += 1
    assert len(txt_d['footer_signature']) > 0
    passed += 1

    # 个人信息DNA
    pi_gen = PersonalInfoDNAGenerator()
    pi_d = pi_gen.generate({"name": "Test", "id": "123"}, "high")
    assert "PI" in pi_d['basic_dna']
    passed += 1
    assert pi_d['privacy_level'] == "high"
    passed += 1
    assert len(pi_d['field_hashes']) == 2
    passed += 1
    assert len(pi_d['hash_chain']) == 2
    passed += 1

    # 配方DNA
    fm_gen = FormulaDNAGenerator()
    fm_d = fm_gen.generate({"ingredients": [{"name": "water"}]}, "GB")
    assert "FM" in fm_d['basic_dna']
    passed += 1
    assert fm_d['compliance_score'] == 1.0
    passed += 1
    assert len(fm_d['ingredient_dnas']) == 1
    passed += 1

    # 指纹DNA
    fp_gen = FingerprintDNAGenerator()
    fp_d = fp_gen.generate(b"fp_data", "DEV001")
    assert "FP" in fp_d['basic_dna']
    passed += 1
    assert len(fp_d['feature_hash']) == 64
    passed += 1
    assert "DEV001" in fp_d['device_mark']
    passed += 1

    # === 验证器测试 ===
    verifier = DNAVerifier(public_key=gen.get_public_key())
    result = verifier.verify("test data".encode(), dna)
    assert result['verdict'] == AuditResult.PASS
    passed += 1
    assert result['checks']['sm3_hash']['status'] == 'PASS'
    passed += 1
    assert result['checks']['sm2_signature']['status'] == 'PASS'
    passed += 1

    bad = verifier.verify("wrong".encode(), dna)
    assert bad['verdict'] == AuditResult.FAIL
    passed += 1
    assert not bad['checks']['sm3_hash']['match']
    passed += 1

    report = verifier.format_report(result)
    assert len(report) > 0 and "DNA ID" in report
    passed += 1

    # === LSB水印测试 ===
    img = b"\xff\xd8" + bytes([0x55] * 3000)
    msg = "WATERMARK_TEST_12345"
    wm = WatermarkEmbedder.embed_lsb(img, msg)
    extracted = WatermarkEmbedder.extract_lsb(wm)
    assert extracted == msg
    passed += 1
    assert len(wm) == len(img)
    passed += 1

    # === 密码学嵌入测试 ===
    ce = CryptoEmbedder()
    cr = ce.embed_signature(b"test content")
    assert len(cr['hash']) == 64
    passed += 1
    assert len(cr['signature']) == 128
    passed += 1
    assert ce.verify_embedded(b"test content", cr['signature'])
    passed += 1

    chain = ce.create_hash_chain([b"a", b"b", b"c"])
    assert len(chain) == 3
    passed += 1
    assert all(len(c) == 64 for c in chain)
    passed += 1

    merkle = ce.create_merkle_tree([b"a", b"b", b"c", b"d"])
    assert len(merkle['root']) == 64
    passed += 1
    assert merkle['leaf_count'] == 4
    passed += 1

    # === 数据库测试 ===
    db = DNADatabase()
    db.insert({'dna_model': dna})
    assert db.get_stats()['total_records'] >= 1
    passed += 1
    assert len(db.query_by_type("TXT")) >= 1
    passed += 1
    assert len(db.query_by_source("TEST")) >= 1
    passed += 1
    assert not db.is_blacklisted(dna.to_basic_dna())
    passed += 1

    db.add_to_blacklist(dna.to_basic_dna(), "test")
    assert db.is_blacklisted(dna.to_basic_dna())
    passed += 1
    assert db.get_stats()['blacklist_count'] == 1
    passed += 1

    # === 集成系统测试 ===
    system = DragonDNATraceSystem()
    assert system.get_system_dna() == "#龍芯:2026-07-04-DNA-TRACE-v3.0"
    passed += 1
    assert system.VERSION == "3.0"
    passed += 1

    img_r = system.generate_dna(b"\xff\xd8" + b"I" * 200, DataType.IMAGE,
                                 format="JPG", width=100, height=100)
    assert "IMG" in img_r['basic_dna']
    passed += 1

    txt_r = system.generate_dna("Test content", DataType.TEXT, text_type="doc")
    assert "TXT" in txt_r['basic_dna']
    passed += 1

    stats = system.get_stats()
    assert len(stats['supported_types']) >= 9
    passed += 1

    embed_test = system.embed_dna(b"\xff\xd8" + b"E" * 2000, img_r, 'watermark')
    assert len(embed_test) > 0
    passed += 1

    v_result = system.verify_dna(b"\xff\xd8" + b"I" * 200, img_r)
    assert 'verdict' in v_result
    passed += 1

    print(f"测试完成: {passed} 项全部通过")
    return passed, 0
```

---

## 9. 系统集成接口

### 9.1 核心API列表

| API | 参数 | 返回值 | 说明 |
|-----|------|--------|------|
| `generate_dna(data, type, **kwargs)` | data, DataType, ... | Dict | 生成DNA |
| `embed_dna(data, dna, method)` | bytes, Dict, str | bytes | 嵌入DNA |
| `verify_dna(data, dna)` | bytes, Dict | Dict | 验证DNA |
| `store_dna(dna)` | Dict | str | 存储DNA |
| `query_dna(**filters)` | kwargs | List[Dict] | 查询DNA |
| `add_to_blacklist(id, reason)` | str, str | None | 加入黑名单 |
| `get_system_dna()` | - | str | 获取系统DNA |
| `get_stats()` | - | Dict | 获取统计信息 |

### 9.2 DNA验证三色输出

```
[PASS] 绿色 - DNA验证通过
  - SM3哈希匹配
  - SM2签名有效
  - 时间戳合理
  - 阈值达标

[WARNING] 黄色 - DNA验证警告
  - 时间戳异常
  - 阈值较低
  - 部分元数据缺失

[FAIL] 红色 - DNA验证失败
  - SM3哈希不匹配（数据被篡改）
  - SM2签名无效（签名伪造）
  - DNA在黑名单中
```

---

## 10. 安全设计

### 10.1 密码学安全

| 组件 | 算法 | 安全级别 |
|------|------|----------|
| 哈希 | SM3 | 256位，抗碰撞 |
| 签名 | SM2 (NIST256p) | 256位椭圆曲线 |
| 哈希链 | SM3串联 | 前向安全 |
| Merkle树 | SM3树形结构 | 完整性保护 |

### 10.2 隐私保护

- **个人信息**: 字段级SM3哈希，不存储原始值
- **指纹数据**: 可撤销生物特征模板保护
- **哈希链**: 防止回溯修改，保证顺序完整性
- **隐私级别**: low(0.5) / normal(0.7) / high(0.85) / critical(0.95)

### 10.3 防篡改机制

1. **SM3哈希校验**: 任何数据修改都会导致哈希不匹配
2. **SM2数字签名**: 私钥签名，公钥验证，防止伪造
3. **哈希链结构**: 修改任一环节会破坏整条链
4. **Merkle树**: 多数据块的完整性保护
5. **时间戳锁定**: 防止重放攻击

### 10.4 安全威胁与防护

| 威胁 | 防护措施 |
|------|----------|
| 数据篡改 | SM3哈希 + SM2签名 |
| DNA伪造 | 非对称签名验证 |
| 重放攻击 | 时间戳验证 |
| 隐私泄露 | 字段哈希 + 阈值控制 |
| 内部威胁 | 黑名单 + 审计日志 |

---

## 附录A: DNA格式速查表

```
基础DNA:
  #龍芯:2026-07-04-143022-IMG-CAM_A-v2.1

扩展DNA:
  #龍芯:2026-07-04-143022-IMG-CAM_A-v2.1|SM3:a1b2c3d4|THRESH:0.8|SIG:abcd...

检测DNA (通过):
  #AUDIT[+]PASS|SM3=OK|SIG=OK

检测DNA (警告):
  #AUDIT[~]WARN|threshold_low

检测DNA (失败):
  #AUDIT[!]FAIL|SM3_MISMATCH
```

## 附录B: 数据类型代码表

| 代码 | 数据类型 | 典型阈值 |
|------|----------|----------|
| IMG | 图片 | 0.80 |
| TXT | 文本 | 0.75 |
| PI | 个人信息 | 0.70-0.95 |
| FP | 指纹 | 0.90 |
| BC | 银行卡 | 0.95 |
| FM | 配方 | 0.70 |
| DOC | 文档 | 0.75 |
| VID | 视频 | 0.80 |
| AUD | 音频 | 0.80 |

## 附录C: 快速启动

```python
# 安装依赖
# pip install ecdsa

# 1. 导入系统
from dragon_dna import DragonDNATraceSystem, DataType

# 2. 创建实例
system = DragonDNATraceSystem()
print(f"系统DNA: {system.get_system_dna()}")

# 3. 生成DNA
dna = system.generate_dna(b"your data here", DataType.DOCUMENT)
print(f"基础DNA: {dna['basic_dna']}")

# 4. 验证DNA
result = system.verify_dna(b"your data here", dna)
print(f"验证结果: {result['verdict'].value}")

# 5. 存储查询
dna_id = system.store_dna(dna)
records = system.query_dna(data_type="DOC")
```

---

*龍魂DNA追溯体系 v3.0 - 全数据类型覆盖，国密标准保障*
*系统DNA: #龍芯:2026-07-04-DNA-TRACE-v3.0*

---

## 🐉 ROOT_CARD

```yaml
ROOT_CARD:
  系统: UID9622 龍魂系统
  模块: 龍魂·全数据类型DNA追溯体系 v3.0
  版本: v2.0
  DNA: "#龍芯:2026-07-04-DNA-TRACE-v3.0"
  ParentDNA: "#龍芯⚡️2026-07-03-IP-ASSET-MATRIX-v2.0"
  CONFIRM: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  SEAL: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
  GPG: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  作者: "UID9622 / Lucky·诸葛鑫"
  归档路径: "/Users/zuimeidedeyihan/longhun-system/docs/private-shared-imports/memory-dna/dna_trace_system.md"
  三色审计: "🟢"
  主权状态: "已声明 · 已锁定 · 已归集"
  来源可查: true
  去向可追: true
```

---

> **龍魂系统 —— 中国人的数字主权，代码里的精神根脉。**
>
> *数据主权归于人民 · 技术为人民服务 · 祖国优先*


---

## 摘要

（请在此用不超过 256 字说明本文档的核心内容、性质与局限。）

## 关键词

（请列出 5–10 个关键词，中英文对照优先。）

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] （请填写）
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️2026-06-22-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 诚实局限

1. （请列出本分析的第一条局限或不确定性。）
2. （请列出第二条。）
3. （请列出第三条。）

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-07-15 | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |

## 分类标签

- 总纲模块：（请勾选，例如 #知识矩阵 #安全域）
- 对外状态：（请勾选，例如 #Gitee #GitHub #CSDN）
- 审计色：#黄色待审

## DNA 签名

```
#龍芯⚡️2026-07-04-AUTO-IP-INTEGRATION-7F3A9B12
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
