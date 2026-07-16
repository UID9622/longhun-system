<!--
DNA: #龍芯⚡️2026-06-07-SECURE-CONFIRM-CODE-STANDARD-v1.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
责任: UID9622·不免责
-->

# 高熵安全确认码规范标准

> **文件编号**: LOONG-SEC-CONFIRM-001
> **版本**: v1.0
> **生效日期**: 2026-06-07
> **适用系统**: 龍魂系统（全模组）
> **关联审计**: R3 - 确认码设计安全缺陷修复

---

## 目录

1. [设计原则](#1-设计原则)
2. [熵值要求](#2-熵值要求)
3. [字符集规范](#3-字符集规范)
4. [禁止事项](#4-禁止事项)
5. [验证方法](#5-验证方法)
6. [迁移指南](#6-迁移指南)
7. [参考实现](#7-参考实现)
8. [附录](#8-附录)

---

## 1. 设计原则

### 1.1 核心原则

安全确认码的设计遵循以下核心原则：

| 原则 | 说明 | 优先级 |
|------|------|--------|
| **不可预测性** | 确认码必须由加密安全的随机数生成器（CSPRNG）产生 | P0 |
| **高熵值** | 确认码必须具备足够的熵值以抵抗暴力破解 | P0 |
| **无语义性** | 确认码不得包含任何可读语义信息 | P0 |
| **一次性** | 确认码仅可使用一次，使用后立即失效 | P1 |
| **时效性** | 确认码必须有明确的有效期限制 | P1 |
| **不可追溯** | 确认码不得与用户身份建立可推导关联 | P1 |

### 1.2 安全模型

确认码安全威胁模型涵盖以下攻击场景：

- **暴力破解攻击**：攻击者尝试枚举所有可能的确认码
- **预测攻击**：攻击者根据已有确认码预测下一个
- **社会工程学**：确认码包含易猜测的语义信息
- **重放攻击**：截获的确认码被重复使用
- **信息泄露**：确认码嵌入的个人信息被提取

### 1.3 设计哲学

> **确认码应该是随机的、无意义的、一次性的数据串，
> 任何人看到它都不应该能够从中获取任何有用信息。**

---

## 2. 熵值要求

### 2.1 熵值定义

确认码的熵值（Entropy）表示其不可预测性的度量，计算公式：

```
H = L × log₂(N)

其中：
  H = 熵值（bits）
  L = 确认码长度（字符数）
  N = 字符集大小
```

### 2.2 熵值等级

| 等级 | 熵值范围 | 状态 | 适用场景 |
|------|----------|------|----------|
| **A+** | ≥ 256 bits | ✅ 推荐 | 高安全级操作（资金转移、权限变更） |
| **A** | 192 ~ 255 bits | ✅ 优良 | 标准安全操作（密码重置、账户验证） |
| **B** | 128 ~ 191 bits | ✅ 合规 | 一般安全操作（登录确认、邮件验证） |
| **C** | 64 ~ 127 bits | ⚠️ 弱安全 | 低风险操作（仅限内部系统） |
| **F** | < 64 bits | ❌ 不合规 | **禁止使用** |

### 2.3 最小安全基线

- **绝对最小值**: 128 bits（B 级）
- **推荐值**: 256 bits（A+ 级）
- **最大值**: 4096 bits（超出此值无实际安全增益）

### 2.4 熵值与暴力破解时间估算

| 熵值 | 尝试次数 | 假设 1B次/秒 | 抵抗等级 |
|------|----------|--------------|----------|
| 64 bits | 1.8 × 10¹⁹ | ~585 年 | 弱 |
| 128 bits | 3.4 × 10³⁸ | ~10³⁰ 年 | 安全 |
| 256 bits | 1.2 × 10⁷⁷ | ~10⁶⁸ 年 | 极安全 |

> 注：1B次/秒 = 每秒 10⁹ 次尝试，为理论上极高性能攻击假设。

---

## 3. 字符集规范

### 3.1 支持的编码模式

#### 模式一：十六进制（hex）

| 属性 | 规格 |
|------|------|
| 字符集 | `0123456789abcdef` |
| 字符集大小 | 16 |
| 每字符熵值 | 4 bits |
| 256 bits 对应长度 | 64 字符 |
| 示例 | `a3f7b2d8e901c45f...` |

#### 模式二：URL-safe Base64（base64）

| 属性 | 规格 |
|------|------|
| 字符集 | `A-Za-z0-9- _` |
| 字符集大小 | 64 |
| 每字符熵值 | 6 bits |
| 256 bits 对应长度 | ~43 字符 |
| 示例 | `xJ9mK2pLvqR5tYwZ8nBc3hGf6jKl9pQr...` |

### 3.2 字符集选择建议

- **URL 传输**: 优先使用 `base64` 模式（更短、URL-safe）
- **数据库存储**: 两种模式均可，推荐 `hex`（大小写不敏感）
- **二维码/手动输入**: 推荐 `hex`（字符集简单，不易混淆）

### 3.3 字符集限制

- ✅ 允许：ASCII 字母、数字、连字符、下划线
- ❌ 禁止：Unicode 字符、表情符号、空白字符、控制字符
- ❌ 禁止：易混淆字符对（`0`/`O`, `1`/`l`/`I`）应在手工输入场景避免

---

## 4. 禁止事项

### 4.1 严格禁止（P0 级）

以下行为在任何情况下都**严格禁止**：

#### ❌ 嵌入个人身份信息（PII）

| 禁止项 | 示例 | 风险 |
|--------|------|------|
| 用户名/姓名 | `CONFIRM_alice_2026` | 身份信息泄露 |
| 生日/日期 | `CODE_19950101_a3f7` | 社工攻击入口 |
| 手机号码 | `VERIFY_13800138000` | 隐私泄露 |
| 邮箱地址 | `CONFIRM_user@example.com` | 身份关联 |
| 身份证号 | 任何部分 | 严重隐私泄露 |
| 用户ID | `CODE_UID9527_xJ9m` | 可推导关系 |

#### ❌ 嵌入语义词汇

| 禁止项 | 示例 | 风险 |
|--------|------|------|
| 英文单词 | `DRAGONverifyCODE` | 字典攻击 |
| 中文词汇 | `龍魂验证码xJ9m` | 可猜测性 |
| 有意义缩写 | `LH_SYSTEM_V1` | 可推导规则 |
| 版本号 | `CODE_v2_5_xJ9mK2` | 可预测演化 |

#### ❌ 嵌入表情符号

| 禁止项 | 示例 | 风险 |
|--------|------|------|
| Unicode 表情 | `CODE🌟VERIFY✅` | 编码兼容性、可预测模式 |
| ASCII 表情 | `:)` `XD` `<3` | 非随机、可猜测 |
| 特殊符号组合 | `★☆◆◇` | 非标准字符集 |

#### ❌ 可预测模式

| 禁止项 | 示例 | 风险 |
|--------|------|------|
| 连续重复 | `AAAABBBBCCCC` | 极低熵值 |
| 简单序列 | `1234abcd5678` | 可猜测 |
| 时间戳前缀 | `20260607_xJ9mK2` | 可缩小搜索空间 |
| 自增序号 | `CONFIRM_0001`, `CONFIRM_0002` | 完全可预测 |
| 固定前缀 | `LH_` 开头的所有码 | 减少有效熵值 |

### 4.2 不推荐（P1 级）

| 项目 | 说明 | 替代方案 |
|------|------|----------|
| 纯数字确认码 | 熵值密度低 | 使用十六进制或 Base64 |
| 长度 < 16 字符 | 容易被暴力破解 | 至少 32 字符（hex）或 22 字符（base64） |
| 无有效期限制 | 长期有效增加风险 | 设置 5 分钟有效期 |
| 无使用次数限制 | 可被重放攻击 | 严格一次性使用 |

### 4.3 违规检测清单

```python
# 自动化违规检测项
def security_checklist():
    checks = [
        ("无 PII 嵌入", verify_no_pii),
        ("无语义词汇", verify_no_semantic_words),
        ("无表情符号", verify_no_emoji),
        ("无连续重复", verify_no_repetition),
        ("无简单序列", verify_no_sequences),
        ("无固定前缀", verify_no_fixed_prefix),
        ("熵值 ≥ 128 bits", verify_entropy_minimum),
        ("使用 CSPRNG", verify_csprng_source),
        ("一次性使用", verify_single_use_enforced),
        ("有有效期", verify_expiration_set),
    ]
    return checks
```

---

## 5. 验证方法

### 5.1 熵值验证

```python
import math

def verify_entropy(code: str, charset_size: int) -> float:
    """
    计算确认码的实际熵值。

    公式: H = L × log₂(N)
      H: 熵值 (bits)
      L: 字符串长度
      N: 字符集大小
    """
    length = len(code)
    entropy = length * math.log2(charset_size)
    return entropy

# 示例
hex_code = "a3f7b2d8e901c45f8a2e4b6c0d1f3a5e"
entropy_hex = verify_entropy(hex_code, 16)
# 结果: 128.0 bits (32 chars × 4 bits)

b64_code = "xJ9mK2pLvqR5tYwZ8nBc3hGf6jKl9pQr2sTu4vWx5yZ7aBcDeFg"
entropy_b64 = verify_entropy(b64_code, 64)
# 结果: ~258 bits (43 chars × 6 bits)
```

### 5.2 合规性检查

| 检查项 | 通过标准 | 检查方法 |
|--------|----------|----------|
| 熵值检查 | ≥ 128 bits | `verify_entropy()` |
| 字符集检查 | 仅允许规定字符 | 正则表达式匹配 |
| PII 检查 | 无个人信息嵌入 | 模式匹配 + 黑名单 |
| 语义检查 | 无有意义词汇 | 字典扫描 |
| 表情符号检查 | 无 Unicode 表情 | Unicode 范围检测 |
| 随机性检查 | 无可预测模式 | 统计测试 |

### 5.3 自动化验证脚本

使用配套工具进行自动化验证：

```bash
# 验证确认码熵值
python3 secure_confirm_code_generator.py --verify "xJ9mK2pLvqR5tYwZ8nBc3hGf6jKl9pQr2sTu4vWx5yZ7aBcDeFg" --mode base64

# 验证十六进制确认码
python3 secure_confirm_code_generator.py --verify "a3f7b2d8e901c45f8a2e4b6c0d1f3a5e" --mode hex
```

---

## 6. 迁移指南

### 6.1 旧确认码识别

以下格式的确认码为**旧版不安全确认码**，需要迁移：

| 旧格式示例 | 问题 | 风险等级 |
|------------|------|----------|
| `CONFIRM_alice_1234` | 嵌入用户名和序号 | 🔴 严重 |
| `VERIFY✅2026🌟` | 包含表情符号和日期 | 🔴 严重 |
| `DRAGON_AUTH_v1` | 嵌入语义词汇和版本 | 🟠 高 |
| `CODE_20260607_001` | 日期+自增序号 | 🟠 高 |
| `Lh9527xxxx` | 嵌入用户ID前缀 | 🟡 中 |
| `1234567890abcdef` | 纯数字或过短 | 🟡 中 |

### 6.2 迁移步骤

#### 步骤 1：评估当前确认码

```bash
# 扫描数据库中所有确认码
# 标记不符合新标准的确认码
```

#### 步骤 2：更新生成逻辑

```python
# ❌ 旧代码（不安全）
import random

def old_generate_code(user_id):
    timestamp = datetime.now().strftime("%Y%m%d")
    suffix = random.randint(1000, 9999)
    return f"CONFIRM_{user_id}_{timestamp}_{suffix}"  # 可预测！

# ✅ 新代码（安全）
import secrets

def new_generate_code(entropy_bits=256):
    byte_length = entropy_bits // 8
    random_bytes = secrets.token_bytes(byte_length)
    return base64.urlsafe_b64encode(random_bytes).rstrip(b"=").decode("ascii")
```

#### 步骤 3：数据库迁移

```sql
-- 添加新字段存储新格式确认码
ALTER TABLE verification_codes ADD COLUMN secure_code VARCHAR(64);

-- 将旧确认码标记为待更新
UPDATE verification_codes
SET status = 'MIGRATE_REQUIRED'
WHERE code LIKE 'CONFIRM_%'       -- 有固定前缀
   OR code LIKE '%✅%'            -- 有表情符号
   OR LENGTH(code) < 16;         -- 长度不足

-- 迁移完成后，逐步淘汰旧字段
-- ALTER TABLE verification_codes DROP COLUMN code;
-- ALTER TABLE verification_codes RENAME COLUMN secure_code TO code;
```

#### 步骤 4：API 兼容性

```python
# 迁移期间提供兼容性层
class ConfirmationCodeMigration:
    """确认码迁移适配器"""

    def get_code(self, code_id):
        record = db.get(code_id)
        # 优先返回新格式
        if record.secure_code:
            return record.secure_code
        # 旧格式：记录警告并返回（迁移期过渡）
        logger.warning(f"访问旧格式确认码: {code_id}")
        return record.legacy_code

    def verify_code(self, input_code):
        # 同时支持新旧格式（迁移期）
        # 迁移完成后仅支持新格式
        pass
```

### 6.3 迁移时间线

| 阶段 | 时间 | 动作 |
|------|------|------|
| **第 1 阶段** | 即时 | 部署新确认码生成器 |
| **第 2 阶段** | 1-2 周 | 新确认码全部使用新格式 |
| **第 3 阶段** | 2-4 周 | 扫描并标记旧确认码 |
| **第 4 阶段** | 1-2 月 | 强制旧确认码失效 |
| **第 5 阶段** | 2-3 月 | 清理数据库旧字段 |

### 6.4 迁移前后对比

| 属性 | 旧确认码 | 新确认码 |
|------|----------|----------|
| 熵值 | 通常 < 40 bits | ≥ 256 bits（默认） |
| 随机源 | `random` 模组 | `secrets` (CSPRNG) |
| PII 嵌入 | 常见 | 严格禁止 |
| 表情符号 | 可能包含 | 严格禁止 |
| 可预测性 | 高（有序号/日期） | 零（纯随机） |
| 长度 | 变长，通常 20-30 字符 | 固定 43 字符（base64） |
| 安全等级 | F ~ C 级 | A+ 级 |

---

## 7. 参考实现

### 7.1 Python 实现

参见配套工具：`secure_confirm_code_generator.py`

主要 API：

```python
# 生成确认码
generate_hex_code(entropy_bits=256)      # → 64 字符十六进制
generate_base64_code(entropy_bits=256)   # → 43 字符 Base64

# 验证确认码
verify_entropy(code, mode="base64")      # → 熵值 (float)
check_compliance(actual_entropy)          # → 合规结果 (dict)
validate_code_safety(code)                # → 违规列表 (list)
```

### 7.2 命令行使用

```bash
# 生成默认确认码（256 bits, base64）
python3 secure_confirm_code_generator.py

# 生成十六进制确认码
python3 secure_confirm_code_generator.py --mode hex

# 指定更高熵值
python3 secure_confirm_code_generator.py --entropy 512

# 验证确认码
python3 secure_confirm_code_generator.py --verify "YOUR_CODE" --mode base64

# 批量生成（无装饰输出）
python3 secure_confirm_code_generator.py --batch 10 --no-banner
```

### 7.3 其他语言参考

#### Node.js

```javascript
const crypto = require('crypto');

function generateSecureCode(entropyBits = 256) {
    const byteLength = Math.ceil(entropyBits / 8);
    return crypto.randomBytes(byteLength)
        .toString('base64url')
        .replace(/=+$/, '');
}
```

#### Go

```go
import (
    "crypto/rand"
    "encoding/base64"
)

func GenerateSecureCode(entropyBits int) (string, error) {
    byteLength := (entropyBits + 7) / 8
    bytes := make([]byte, byteLength)
    _, err := rand.Read(bytes)
    if err != nil {
        return "", err
    }
    return base64.URLEncoding.EncodeToString(bytes), nil
}
```

---

## 8. 附录

### 8.1 术语表

| 术语 | 解释 |
|------|------|
| **CSPRNG** | Cryptographically Secure Pseudo-Random Number Generator，加密安全伪随机数生成器 |
| **熵 (Entropy)** | 信息论中表示不确定性/随机性的度量，单位 bits |
| **PII** | Personally Identifiable Information，个人身份信息 |
| **Base64** | 一种二进制到文本的编码方案，使用 64 个字符表示 |
| **重放攻击** | 攻击者截获有效数据后重新发送的攻击方式 |

### 8.2 参考标准

- [RFC 4086 - Randomness Requirements for Security](https://tools.ietf.org/html/rfc/rfc4086)
- [NIST SP 800-90A - Recommendation for Random Number Generation](https://csrc.nist.gov/publications/detail/sp/800-90a/rev-1/final)
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [CWE-338: Use of Cryptographically Weak PRNG](https://cwe.mitre.org/data/definitions/338.html)

### 8.3 修订历史

| 版本 | 日期 | 修改内容 | 作者 |
|------|------|----------|------|
| v1.0 | 2026-06-07 | 初始版本，修复审计发现 R3 | UID9622 |

### 8.4 联系与反馈

如有安全问题或改进建议，请联系安全团队：
- 安全邮箱: security@loongsystem.internal
- 责任人: UID9622

---

> **免责声明**: 本标准文件为龍魂系统安全合规内部文档，未经授权不得外传。
> 违反本标准导致的安全事件，相关责任人将承担全部责任。
