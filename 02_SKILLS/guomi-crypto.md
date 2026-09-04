# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# /guomi-crypto

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技能说明 · 国密三引擎加密技能
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-GUOMI-CRYPTO-SKILL-v1.0`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

skill_id: /guomi-crypto
synced_at: 2026-07-06
source: 原世界身份定位总纲 v9.0 §4（Notion）
---

# /guomi-crypto · 国密三引擎

## 摘要

国密加密引擎是龍魂系统的密码学保护层。采用国家密码管理局发布的商用密码标准（GM/T系列），包含三大核心引擎：SM2 非对称签名引擎（数字签名+密钥交换，256位椭圆曲线）、SM3 哈希摘要引擎（数据完整性校验，256位输出）、SM4 对称加密引擎（数据加密/解密，128位分组32轮迭代）。三引擎协同保护七因子身份数据：SM2 保护 F1/F2、SM3 保护 F3/F7、SM4 保护 F4/F5/F6。与 AES-256-GCM 形成国密+国际双轨加密体系。

## 一句话定义

> 龍魂系统的加密工具箱——SM2 盖电子印章、SM3 给文件打指纹、SM4 锁住敏感数据。

## 关键词

国密 National Secret Algorithm, SM2 SM3 SM4, 非对称加密 Asymmetric Encryption, 哈希摘要 Hash Digest, 对称加密 Symmetric Encryption, GM/T标准, 数字签名 Digital Signature, PBKDF2, 椭圆曲线 Elliptic Curve

## 三大引擎

### SM2 非对称签名引擎

**标准**：GM/T 0003-2012
**类型**：非对称加密/数字签名
**安全强度**：256位椭圆曲线（相当于 RSA-3072）

**曲线参数**：
```
y² = x³ + ax + b (mod p)
p = FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a = FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
n = FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
```

**核心功能**：
- 生成 SM2 密钥对（私钥32字节 + 公钥65字节）
- 使用私钥对数据进行数字签名
- 使用公钥验证签名
- 为 DNA 追溯码生成数字签名（核心操作）

**签名流程**：
```
数据 → SM3哈希 → SM2私钥签名 → 签名值（r+s）
```

**验证流程**：
```
数据 → SM3哈希 → SM2公钥验证 → True/False
```

### SM3 哈希摘要引擎

**标准**：GM/T 0004-2012
**类型**：密码学哈希函数
**安全强度**：256位输出，抗碰撞

**算法参数**：
```
输出长度：256位（32字节）
分组长度：512位（64字节）
字长度：32位
迭代次数：64轮
填充方式：Merkle-Damgard 结构
```

**核心功能**：
- 计算任意数据的 SM3 哈希值
- 为 DNA 追溯码生成验证摘要
- 构建哈希链（Hash Chain）实现不可篡改
- 验证七因子向量的哈希值

**哈希链构建**：
```
区块N = SM3(数据N的哈希 + 前一区块的组合哈希)
→ 每个节点包含前一个节点的哈希
→ 链式结构，任一节点被改则整链断裂
```

### SM4 对称加密引擎

**标准**：GM/T 0002-2012
**类型**：分组对称加密
**安全强度**：128位分组，32轮迭代

**算法参数**：
```
分组长度：128位（16字节）
密钥长度：128位（16字节）
迭代次数：32轮
结构：非平衡 Feistel 网络
支持模式：ECB、CBC、CFB、OFB、CTR、GCM
```

**核心功能**：
- SM4-CBC 模式加密/解密数据
- SM4-GCM 模式认证加密（AEAD）
- 从口令派生密钥（PBKDF2-HMAC-SHA256）
- 加密七因子敏感中间数据

**密钥派生**：
```
口令 + 盐值 + 100000次迭代 → PBKDF2-HMAC-SHA256 → 16字节密钥
```

## 三引擎与七因子映射

| 国密算法 | 保护因子 | 保护方式 | 技术实现 |
|------|:---:|------|------|
| SM2 | F1-身份DNA | 数字签名验证身份绑定 | 用私钥签名DNA追溯码 |
| SM2 | F2-时间锚点 | 签名时间戳防篡改 | 对时间戳进行数字签名 |
| SM3 | F3-规则轨迹 | 哈希链保证完整性 | 规则日志的哈希链 |
| SM4 | F4-人格路径 | 加密存储人格基线 | 人格向量加密存储 |
| SM4 | F5-受保护词汇 | 加密存储私人词典 | 词典加密存储 |
| SM4 | F6-风格向量 | 加密存储风格基线 | 风格向量加密存储 |
| SM3 | F7-错误账本 | 哈希保证修订历史完整 | 修订记录的哈希链 |

## 完整加密流程

```
用户提交内容制品 C
  → 七因子引擎计算 Σ(C) = (F1..F7)
    → SM3 先计算内容哈希
      → SM2 使用私钥签名
        → SM4 加密敏感因子数据（F4/F5/F6）
          → SM3 计算DNA追溯码哈希
            → DNA追溯系统生成完整DNA（DNA + SM3 + SIG）
              → 三色审计引擎五类检测器并行运行
                → 返回最终结果（含DNA+审计标签）
```

## 三色审计引擎（五类检测器）

| 检测器 | 功能 |
|------|------|
| 配方合规检测器 | 检查加密算法配置是否合规 |
| 文本幻觉检测器 | 检测AI生成内容的幻觉 |
| 个人信息保护检测器 | 检测PII泄露 |
| 参数合规检测器 | 检查密码学参数是否符合国标 |
| DNA验证检测器 | 验证DNA追溯码的完整性 |

**审计判定**：
- 有红燈 → 总体红燈
- 无红燈有黄燈 → 总体黄燈
- 全部绿燈 → 总体绿燈

## 引擎映射（本地实现）

| 引擎 | 文件 | 说明 |
|------|------|------|
| 七因子验证器 | `cnsh-core/governance/f1_through_f7_verifier.py` | F1-F7 独立验证 |
| L4 七因子签名层 | `crypto-stack/src/l4_seven_factor.py` | 加权乘积置信度模型 |
| L6 灵魂层 | `crypto-stack/src/l6_soul.py` | 引用七因子 |
| 密码栈运行器 | `crypto-stack/src/stack_runner.py` | 调用七因子层 |
| 河图洛书桥接 | `cnsh-core/ecosystem/hetu_luoshu_yijing_sevenfactor_bridge.py` | 易经×七因子桥接 |

## 技术参数速查

| 参数 | 值 |
|------|------|
| SM2 密钥长度 | 私钥256位 / 公钥512位 |
| SM3 输出长度 | 256位（64个HEX字符） |
| SM4 密钥长度 | 128位（16字节） |
| SM4 分组长度 | 128位（16字节） |
| PBKDF2 迭代次数 | 100,000 |
| PBKDF2 哈希算法 | HMAC-SHA256 |
| 备选对称算法 | AES-256-GCM |
| 备选签名算法 | RSA-2048 |

## 引用与溯源

- 国密标准：GM/T 0002/0003/0004-2012
- Python库：`gmssl`（国密算法Python实现）
- 相关文件：
  - `02_SKILLS/identity-positioning.md` — 身份定位总纲
  - `02_SKILLS/dna-trace-engine.md` — DNA追溯引擎
  - `01_protocols/seven-factor-verification.md` — 七因子验证预言机协议
  - `crypto-stack/` — 密码学栈

## 诚实局限

1. `gmssl` 库为纯 Python 实现，性能远低于硬件 HSM/国密芯片。
2. SM2 椭圆曲线参数为公开标准，安全性依赖私钥保管。
3. SM4-CBC 模式不提供认证加密，需配合 HMAC 或升级到 SM4-GCM。
4. 三引擎当前独立运行，未实现完整的加密流程编排。

## 修改记录

| 日期 | 变更 | DNA |
|------|------|------|
| 2026-07-06 | 初始创建，整合国密三引擎 SM2/SM3/SM4 + 五类审计检测器 | `#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-GUOMI-CRYPTO-SKILL-v1.0` |

---

**三色审计**: 🟢 通过 | 🟡 gmssl纯Python性能待优化 | 🔴 0
