# 龍魂·国密DNA加密引擎

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技术文档 · 未经同行评审（如适用）
> 版本：v2.0
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
> **DNA:** `#龍芯⚡️2026-07-04-MEMORY-DNA-IMPORT-08-v2.0` · **ParentDNA:** `#龍芯⚡️2026-07-03-IP-ASSET-MATRIX-v2.0`
> **CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` · **SEAL:** `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL` · **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> **作者:** UID9622 / Lucky·诸葛鑫 · **来源:** `/Users/zuimeidedeyihan/Downloads/Kimi_Agent_龍魂IP资产清单 (2)/guomi_crypto_engine.md` · **归档:** `/Users/zuimeidedeyihan/longhun-system/docs/private-shared-imports/memory-dna/guomi_crypto_engine.md`
> **迁移时间:** 2026-07-04T14:29:42.393203+08:00

# 龍魂·国密DNA加密引擎

# 龍魂·国密DNA加密引擎

> **DNA追溯码**: `#龍芯⚡️2026-07-04-GUOMI-CRYPTO-v3.0`  
> **三色审计标准**: 🔴 红(禁止) / 🟡 黄(审查) / 🟢 绿(通过)  
> **版本**: v3.0 | **最后更新**: 2026-07-04

---

## 目录

1. [系统概述](#1-系统概述)
2. [国密算法核心实现](#2-国密算法核心实现)
3. [DNA追溯码系统](#3-dna追溯码系统)
4. [文件加密器](#4-文件加密器)
5. [密钥管理方案](#5-密钥管理方案)
6. [三色审计系统](#6-三色审计系统)
7. [使用示例](#7-使用示例)
8. [单元测试结果](#8-单元测试结果)

---

## 1. 系统概述

龍魂·国密DNA加密引擎是专为龍魂系统设计的全类型数据加密解决方案，基于中国国家密码管理局发布的三大国密算法标准（SM2/SM3/SM4），实现对图片、文本、个人信息、指纹、配方等全类型数据的加密保护，并嵌入DNA追溯码供检测部门做三色审计验证。

### 核心特性

| 特性 | 说明 |
|------|------|
| **SM3哈希** | 256位摘要，数据完整性验证 |
| **SM4对称加密** | 128位分组加密，支持ECB/CBC模式 |
| **SM2非对称加密** | 椭圆曲线加密/数字签名 |
| **DNA追溯码** | 国密标准追溯标识，格式 `#龍芯⚡️YYYY-MM-DD-MODULE-vX.X` |
| **LSB数字水印** | 图片最低有效位水印嵌入 |
| **三色审计** | 红(禁止)/黄(审查)/绿(通过) |

### 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    龍魂·国密DNA加密引擎                       │
├─────────────┬─────────────┬─────────────┬─────────────────┤
│   SM3哈希    │  SM4对称加密  │ SM2非对称加密 │  DNA追溯码系统   │
│  (数据摘要)  │ (文件加密)   │ (签名/加密)  │ (数字水印)       │
├─────────────┴─────────────┴─────────────┴─────────────────┤
│                     文件加密器层                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │
│  │ 图片加密器 │ │ 文本加密器 │ │ 个人信息加密│ │  配方加密器    │ │
│  │ JPG/PNG  │ │ TXT/DOC  │ │ 银行卡/指纹 │ │  成分/阈值    │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    密钥管理与审计系统                         │
│              企业私钥 ◄──► 检测部门公钥                       │
│              会话密钥管理 + 三色审计验证                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 国密算法核心实现

### 2.1 SM3 密码杂凑算法

SM3是中国国家密码管理局发布的密码杂凑算法，输出256位（32字节）摘要，用于数据完整性验证。

```python
# 使用示例
from longhun_crypto_engine import SM3, sm3_hash

# 方式1: 增量式哈希
sm3 = SM3()
sm3.update(b"Hello")
sm3.update(b" World")
digest = sm3.hexdigest()  # 64字符十六进制字符串

# 方式2: 便捷函数
hash_result = sm3_hash(b"data to hash")  # "66c7f0f4..."
```

**技术参数**:
- 输出长度: 256位 (32字节 / 64 hex字符)
- 块大小: 512位 (64字节)
- 填充方式: Merkle-Damgård + 附加长度

### 2.2 SM4 分组密码算法

SM4是中国国家密码管理局发布的分组密码算法，使用128位密钥和128位分组。

```python
from longhun_crypto_engine import SM4Cipher

key = b'0123456789abcdef'  # 16字节密钥
iv = b'fedcba9876543210'    # 16字节IV (CBC模式)

cipher = SM4Cipher(key)

# ECB模式
encrypted = cipher.encrypt(b"plaintext")
decrypted = cipher.decrypt(encrypted)

# CBC模式 (推荐)
encrypted = cipher.encrypt_cbc(b"plaintext", iv)
decrypted = cipher.decrypt_cbc(encrypted, iv)
```

**技术参数**:
- 密钥长度: 128位 (16字节)
- 分组大小: 128位 (16字节)
- 轮数: 32轮
- 填充: PKCS7
- 模式: ECB / CBC

### 2.3 SM2 椭圆曲线公钥密码算法

SM2是基于椭圆曲线的非对称加密算法，支持加密/解密和数字签名/验证。

```python
from longhun_crypto_engine import SM2Cipher

# 生成密钥对
sk, pk = SM2Cipher.generate_keypair()  # sk: 32字节, pk: 64字节

# 加密
sm2_enc = SM2Cipher(public_key=pk)
ciphertext = sm2_enc.encrypt(b"secret message")

# 解密
sm2_dec = SM2Cipher(private_key=sk)
plaintext = sm2_dec.decrypt(ciphertext)

# 签名
sm2_sign = SM2Cipher(private_key=sk)
r, s = sm2_sign.sign(b"message to sign")

# 验签
sm2_verify = SM2Cipher(public_key=pk)
assert sm2_verify.verify(b"message to sign", (r, s))
```

**技术参数**:
- 曲线: SM2曲线 (sm2p256v1)
- 私钥长度: 256位 (32字节)
- 公钥长度: 512位 (64字节未压缩)
- 密文格式: C1 || C3 || C2 (65 + 32 + len(M) 字节)
- 签名格式: (r, s) 两个256位整数

**SM2曲线参数** (通过OpenSSL验证):
```
p  = FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a  = FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b  = 28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
n  = FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
Gx = 32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Gy = BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
```

---

## 3. DNA追溯码系统

### 3.1 DNA追溯码格式

```
#龍芯⚡️YYYY-MM-DD-MODULE-vX.X[|BASE64_EXTRA_DATA]
```

**示例**:
```
#龍芯⚡️2026-07-04-GUOMI-CRYPTO-v3.0
#龍芯⚡️2026-07-04-IMG-ENCRYPT-v3.0|eyJvd25lciI6ICJ1c2VyMSJ9
```

### 3.2 模块代码对照表

| 模块键 | 代码 | 用途 |
|--------|------|------|
| `guomi_crypto` | `GUOMI-CRYPTO` | 国密引擎核心 |
| `image_encrypt` | `IMG-ENCRYPT` | 图片加密 |
| `text_encrypt` | `TXT-ENCRYPT` | 文本加密 |
| `personal_info` | `PINFO-ENCRYPT` | 个人信息加密 |
| `fingerprint` | `FINGERPRINT` | 指纹数据加密 |
| `formula` | `FORMULA` | 配方数据加密 |
| `audit` | `AUDIT-VERIFY` | 审计验证 |

### 3.3 数字水印嵌入

**LSB水印**: 将DNA码嵌入图片的RGB通道最低有效位

```python
from longhun_crypto_engine import WatermarkEmbedder

# 嵌入水印
watermarked_image = WatermarkEmbedder.embed_lsb(image_bytes, dna_code)

# 提取水印
extracted_dna = WatermarkEmbedder.extract_lsb(watermarked_image)
```

**元数据水印**: 将DNA信息嵌入PNG的tEXt块

```python
# 嵌入元数据
metadata = {"dna_code": dna_code, "sm3_hash": hash_value, "owner": "user1"}
marked_image = WatermarkEmbedder.embed_metadata(image_bytes, metadata)

# 提取元数据
extracted_meta = WatermarkEmbedder.extract_metadata(marked_image)
```

---

## 4. 文件加密器

### 4.1 图片加密器 (ImageEncryptor)

支持JPG/PNG图片的SM4-CBC加密 + DNA追溯码嵌入。

```python
from longhun_crypto_engine import ImageEncryptor, LongHunCryptoEngine
import io
from PIL import Image

# 创建测试图片
img = Image.new('RGB', (100, 100), color='blue')
buf = io.BytesIO()
img.save(buf, format='PNG')
img_data = buf.getvalue()

# 加密
engine = LongHunCryptoEngine()
encryptor = ImageEncryptor(engine)
sm4_key = os.urandom(16)
result = encryptor.encrypt(img_data, sm4_key, owner_id="user_001")

print(result["dna_code"])      # DNA追溯码
print(result["orig_hash"])     # 原始图片SM3摘要
print(result["ciphertext"])    # 加密后的密文(hex)

# 解密
decrypted = encryptor.decrypt(result["ciphertext"], result["sm4_key"], result["iv"])
assert decrypted == img_data

# LSB水印
watermarked = encryptor.embed_dna_watermark(img_data, result["dna_code"])
extracted = encryptor.extract_dna_watermark(watermarked)
print(extracted)  # 提取的DNA码
```

### 4.2 文本加密器 (TextEncryptor)

支持文本的SM4加密 + DNA头尾标记。

```python
from longhun_crypto_engine import TextEncryptor

encryptor = TextEncryptor()
sm4_key = os.urandom(16)

# 加密
text = "这是龍魂系统的敏感文本数据！"
result = encryptor.encrypt(text, sm4_key)

print(result["encrypted_package"])
# 输出格式:
# ===龍魂DNA头===#龍芯⚡️2026-07-04-TXT-ENCRYPT-v3.0===龍魂DNA头===
# IV:base64_iv
# DATA:base64_ciphertext
# ===龍魂DNA尾===sm3_hash===龍魂DNA尾===

# 解密
decrypted = encryptor.decrypt(result["encrypted_package"], result["sm4_key"])
print(decrypted)  # "这是龍魂系统的敏感文本数据！"

# 验证DNA标记
verify = encryptor.verify_dna(result["encrypted_package"])
print(verify)  # {"has_header": true, "has_footer": true, ...}
```

### 4.3 个人信息加密器 (PersonalInfoEncryptor)

支持银行卡、手机号、身份证号、指纹等敏感信息的SM2公钥加密 + DNA哈希。

```python
from longhun_crypto_engine import PersonalInfoEncryptor, SM2Cipher

# 生成SM2密钥对
sk, pk = SM2Cipher.generate_keypair()

encryptor = PersonalInfoEncryptor()

# 加密单个字段
result = encryptor.encrypt_field('bank_card', '6222021234567890123', pk)
print(result["mask"])       # 6222***********0123 (脱敏显示)
print(result["dna_code"])   # DNA追溯码
print(result["encrypted"])  # SM2加密后的密文(base64)

# 解密
plaintext = encryptor.decrypt_field(result["encrypted"], sk)
print(plaintext)  # 6222021234567890123

# 加密完整个人信息
person = {
    'name': '张三',
    'phone': '13800138000',
    'id_card': '110101199001011234',
    'bank_card': '6222021234567890123',
}
full_result = encryptor.encrypt_person(person, pk)
print(full_result["master_dna"])  # 主DNA追溯码
print(full_result["field_count"])  # 4
```

**支持的字段类型**:

| 类型 | 名称 | 脱敏示例 |
|------|------|----------|
| `bank_card` | 银行卡号 | 6222***********0123 |
| `phone` | 手机号 | 138****8000 |
| `id_card` | 身份证号 | 1101********1234 |
| `address` | 地址 | 北* |
| `name` | 姓名 | 张* |
| `fingerprint` | 指纹特征 | [生物特征] |

### 4.4 配方加密器 (FormulaEncryptor)

支持配方数据的SM4加密 + 成分阈值DNA + 合规检查。

```python
from longhun_crypto_engine import FormulaEncryptor

encryptor = FormulaEncryptor()

formula = {
    "name": "产品配方A",
    "ingredients": [
        {"name": "活性成分X", "ratio": 30.5},
        {"name": "活性成分Y", "ratio": 45.2},
        {"name": "纯净水", "ratio": 24.3},
    ]
}

# 设定合规阈值
compliance = {
    "max_活性成分X": 35.0,  # 活性成分X不超过35%
    "max_活性成分Y": 50.0,  # 活性成分Y不超过50%
}

sm4_key = os.urandom(16)
result = encryptor.encrypt_formula(formula, sm4_key, compliance)

print(result["compliance"]["status"])   # "pass" 或 "fail"
print(result["compliance"]["audit_color"])  # "green" 或 "red"
print(result["dna_code"])  # 包含成分摘要的DNA码

# 解密
decrypted = encryptor.decrypt_formula(
    result["ciphertext"], result["sm4_key"], result["iv"]
)
print(decrypted)  # 原始配方数据
```

---

## 5. 密钥管理方案

### 5.1 密钥体系

```
┌────────────────────────────────────────────────────┐
│                    龍魂密钥体系                      │
├────────────────────┬───────────────────────────────┤
│    企业密钥对       │      检测部门公钥              │
│  (签名DNA追溯码)   │     (验证DNA签名)             │
├────────────────────┼───────────────────────────────┤
│  SM2私钥 (企业保存) │   SM2公钥 (检测部门持有)       │
│  keystore/         │   通过安全通道分发              │
│  enterprise_sk.pem │                               │
├────────────────────┴───────────────────────────────┤
│              会话密钥 (SM4对称密钥)                   │
│       每次加密生成，加密后安全传输给授权方              │
└────────────────────────────────────────────────────┘
```

### 5.2 使用示例

```python
from longhun_crypto_engine import KeyManager

# 初始化密钥管理器
km = KeyManager(keystore_dir="./keystore")

# 生成/加载企业密钥对
sk, pk = km.load_enterprise_keypair()

# 设置检测部门公钥
inspector_pk = b'...'  # 检测部门提供的公钥
km.set_inspector_public_key(inspector_pk)

# 生成会话密钥
session_key = km.generate_session_key("session_001")

# 签名DNA码
dna_code = "#龍芯⚡️2026-07-04-GUOMI-CRYPTO-v3.0"
signature = km.sign_dna(dna_code)

# 验证DNA签名 (检测部门)
is_valid = km.verify_dna_signature(dna_code, signature)
```

---

## 6. 三色审计系统

### 6.1 审计标准

| 颜色 | 级别 | 含义 | 处理动作 |
|------|------|------|----------|
| 🔴 红色 | 3 | 禁止/高风险 | 立即阻止并上报 |
| 🟡 黄色 | 2 | 审查/中风险 | 需要人工审查 |
| 🟢 绿色 | 1 | 通过/低风险 | 正常通行 |

### 6.2 审计流程

```python
from longhun_crypto_engine import AuditSystem

audit = AuditSystem()

# 1. 验证数据完整性
result = audit.verify_data_integrity(data_bytes, stored_sm3_hash)
# {"match": true, "audit_color": "green", ...}

# 2. 验证DNA追溯码
result = audit.verify_dna_trace(dna_code, expected_module="GUOMI-CRYPTO")
# {"status": "pass", "audit_color": "green", ...}

# 3. 完整审计加密包
package = {
    "dna_code": dna_code,
    "orig_hash": hash_value,
    "ciphertext": ciphertext,
    ...
}
audit_result = audit.audit_encrypted_package(package, inspector_id="INSPECTOR_001")
# {
#     "audit_color": "green",
#     "audit_label": "🟢 绿色 - 通过",
#     "checks": [...],
#     "audit_dna": "AUDIT[green]:INSPECTOR_001:20260704120000:abcd1234"
# }
```

---

## 7. 使用示例

### 7.1 快速入门

```python
from longhun_crypto_engine import (
    LongHunCryptoEngine, KeyManager,
    ImageEncryptor, TextEncryptor,
    PersonalInfoEncryptor, FormulaEncryptor,
    SM2Cipher, SM3, SM4Cipher
)

# 1. 初始化引擎和密钥管理
engine = LongHunCryptoEngine()
km = KeyManager("./keystore")
km.load_enterprise_keypair()

# 2. SM4加密文本
text = "机密数据需要加密保护"
sm4_key = km.generate_session_key()
txt_enc = TextEncryptor(engine)
result = txt_enc.encrypt(text, sm4_key)
print(f"DNA码: {result['dna_code']}")
print(f"加密包: {result['encrypted_package'][:100]}...")

# 3. 解密验证
decrypted = txt_enc.decrypt(result["encrypted_package"], result["sm4_key"])
print(f"解密: {decrypted}")

# 4. SM2加密敏感信息
sk, pk = SM2Cipher.generate_keypair()
pii_enc = PersonalInfoEncryptor(engine)
pii_result = pii_enc.encrypt_field('phone', '13800138000', pk)
print(f"加密手机号: {pii_result['mask']}")

# 5. 签名DNA
dna_sig = km.sign_dna(result["dna_code"])
print(f"DNA签名: {dna_sig[:50]}...")
```

### 7.2 完整工作流

```python
import os
from longhun_crypto_engine import *

# Step 1: 初始化
engine = LongHunCryptoEngine()
km = KeyManager("./keystore")
km.load_enterprise_keypair()

# Step 2: 加密多种数据
data_to_encrypt = {
    "配方数据": {"name": "配方A", "ingredients": [...]},
    "个人信息": {"name": "张三", "phone": "13800138000"},
    "敏感文本": "机密配方成分比例...",
}

# Step 3: 为每种数据生成DNA追溯码
for data_type, data in data_to_encrypt.items():
    dna = engine.generate_dna_code(data_type, {"content": str(data)[:50]})
    print(f"[{data_type}] DNA: {dna}")

# Step 4: 签名所有DNA码
for dna in dna_codes:
    sig = km.sign_dna(dna)
    print(f"签名: {sig[:40]}...")

# Step 5: 检测部门审计
audit = AuditSystem(engine)
for package in encrypted_packages:
    result = audit.audit_encrypted_package(package, "INSPECTOR_001")
    color = result["audit_color"]
    print(f"审计结果: {result['audit_label']}")
```

---

## 8. 单元测试结果

```
============================================================
龍魂·国密DNA加密引擎 - 单元测试
DNA追溯码: #龍芯⚡️2026-07-04-GUOMI-CRYPTO-v3.0
============================================================

📦 SM3 哈希测试
  ✅ SM3基础测试('abc')
  ✅ SM3长数据测试

📦 SM4 对称加密测试
  ✅ SM4-ECB加解密
  ✅ SM4-CBC加解密
  ✅ SM4大文件加密(10KB)

📦 SM2 非对称加密/签名测试
  ✅ SM2密钥对生成
  ✅ SM2加解密
  ✅ SM2签名验签
  ✅ SM2多消息签名

📦 DNA追溯码测试
  ✅ DNA追溯码生成
  ✅ DNA追溯码解析
  ✅ DNA审计标记生成

📦 图片加密器测试
  ✅ 图片加密+DNA生成
  ✅ 图片解密验证

📦 文本加密器测试
  ✅ 文本加密+DNA
  ✅ 文本解密验证
  ✅ 文本DNA标记验证

📦 个人信息加密器测试
  ✅ 个人信息字段加密
  ✅ 个人信息字段解密
  ✅ 完整个人信息加密

📦 配方加密器测试
  ✅ 配方加密+合规检查
  ✅ 配方解密验证

📦 密钥管理测试
  ✅ 密钥管理生成/加载

📦 审计系统测试
  ✅ 审计-完整性验证
  ✅ 审计-DNA追溯验证

📦 集成测试
  ✅ 完整工作流集成

============================================================
总计: 26 | ✅ 通过: 26 | ❌ 失败: 0
============================================================
```

---

## 附录: 文件清单

| 文件 | 说明 |
|------|------|
| `longhun_crypto_engine.py` | 完整加密引擎源码 (可直接运行) |
| `keystore/enterprise_sk.pem` | 企业私钥 (自动生成的SM2私钥) |
| `keystore/enterprise_pk.pem` | 企业公钥 (对应私钥的公钥) |

## 附录: 运行方式

```bash
# 运行单元测试
python longhun_crypto_engine.py

# 作为模块导入
from longhun_crypto_engine import LongHunCryptoEngine
engine = LongHunCryptoEngine()
```

## 附录: 依赖要求

- Python 3.8+
- 标准库: os, sys, struct, copy, binascii, base64, json, time, random, hashlib, io, re
- 可选: Pillow (图片处理，JPG/PNG加密需要)

---

*龍魂系统 · 国密DNA加密引擎 v3.0*  
*DNA追溯码: #龍芯⚡️2026-07-04-GUOMI-CRYPTO-v3.0*

---

## 🐉 ROOT_CARD

```yaml
ROOT_CARD:
  系统: UID9622 龍魂系统
  模块: 龍魂·国密DNA加密引擎
  版本: v2.0
  DNA: "#龍芯⚡️2026-07-04-MEMORY-DNA-IMPORT-08-v2.0"
  ParentDNA: "#龍芯⚡️2026-07-03-IP-ASSET-MATRIX-v2.0"
  CONFIRM: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  SEAL: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
  GPG: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  作者: "UID9622 / Lucky·诸葛鑫"
  归档路径: "/Users/zuimeidedeyihan/longhun-system/docs/private-shared-imports/memory-dna/guomi_crypto_engine.md"
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
