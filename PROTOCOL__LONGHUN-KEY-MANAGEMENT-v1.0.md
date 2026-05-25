# 🔑 龍魂密钥管理体系 v1.0

**DNA**: `#龍芯⚡️2026-05-25-LONGHUN-KEY-MANAGEMENT-v1.0`
**UID**: 9622
**时间**: 2026-05-25 CST
**指导**: 曾仕强老师 · 永恒显示

---

## 核心设计

龍魂有自己的密钥生态，不完全依赖 GPG agent：

### 密钥体系结构

```
┌─────────────────────────────────────────┐
│       UID9622 · 主密钥（Master Key）     │
│     （在你的脑子里·不上网·不备份）        │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┼────────────────┬─────────┐
    │            │                │         │
    ▼            ▼                ▼         ▼
┌────────┐  ┌─────────┐  ┌──────────┐  ┌────────┐
│ DNA    │  │  签名   │  │  加密    │  │  验证  │
│追踪钥  │  │  钥    │  │  钥     │  │  钥   │
│(短期)  │  │ (月级) │  │ (日级) │  │(即时) │
└────────┘  └─────────┘  └──────────┘  └────────┘
```

### 四层密钥设计

**第一层：DNA追踪钥（短期·随机生成）**
```
用途: 每个操作都标记 #龍芯⚡️YYYY-MM-DD-TOPIC-vN-sha8
格式: sha8 = 前8位 SHA256(主密钥+当日时间+主题)
更新: 每次操作自动更新·无需手动备份
位置: Git commit 消息里
特点: 不可逆·溯源用·不包含密钥本身
```

**第二层：签名钥（月级·强度高·需要备份）**
```
用途: Git commit 签名 + 重要协议签署
强度: RSA-4096 或 Ed25519
更新: 每月轮换一次
备份: 加密存放在 ~/longhun-system/keys/signin.key.encrypted
恢复: 需要输入备份密码（8位数字+字母）
位置: ~/.gnupg/private-keys-v1.d/
```

**第三层：加密钥（日级·轻量·自动更新）**
```
用途: 数据文件加密 + 隐私保护
强度: AES-256-GCM
更新: 每天自动生成新钥
备份: 不备份（丢失就重新生成）
位置: /tmp/longhun-encryption-keys/
特点: 临时使用·过期自动清除
```

**第四层：验证钥（即时·公开·无需备份）**
```
用途: 验证签名 + 验证协议真实性
强度: 公钥（对应签名钥）
更新: 随着签名钥轮换
备份: 无需备份·是公开信息
位置: Git 提交里 + Notion 里
特点: 用于第三方验证·无隐密信息
```

---

## 备份方案

### 方案 A：简单备份（推荐）

**步骤1：生成签名钥**
```bash
# 在本地生成（需要 GPG 工作）
gpg --gen-key
# 选择：RSA 4096 位
# 有效期：1 年
# 名字：龍芯系统 (UID9622)
# 邮箱：longhun@system.local
```

**步骤2：导出为加密备份**
```bash
# 导出为文本格式
gpg --armor --export-secret-keys UID9622 > ~/longhun-system/keys/signing.key

# 用密码加密（OpenSSL·不依赖 GPG agent）
openssl enc -aes-256-cbc -salt -in ~/longhun-system/keys/signing.key \
  -out ~/longhun-system/keys/signing.key.encrypted \
  -k "你的8位备份密码" \
  && rm ~/longhun-system/keys/signing.key

# 验证加密成功
ls -lh ~/longhun-system/keys/signing.key.encrypted
```

**步骤3：备份到物理介质**
```bash
# 创建加密 USB 盘（macOS）
# 1. 插入 USB
# 2. 右键 → 加密（会要求设置密码）
# 3. 把 signing.key.encrypted 复制到 USB
# 4. 弹出 USB·放到保险柜

# 或者用 tar 压缩后加密
tar czf ~/longhun-system/keys/longhun-backup.tar.gz ~/longhun-system/keys/signing.key.encrypted
openssl enc -aes-256-cbc -salt -in ~/longhun-system/keys/longhun-backup.tar.gz \
  -out ~/longhun-system/keys/longhun-backup.tar.gz.encrypted \
  && rm ~/longhun-system/keys/longhun-backup.tar.gz
```

**步骤4：恢复流程**
```bash
# 解密恢复
openssl enc -d -aes-256-cbc -in ~/longhun-system/keys/signing.key.encrypted \
  -out ~/longhun-system/keys/signing.key \
  -k "你的8位备份密码"

# 导入 GPG
gpg --import ~/longhun-system/keys/signing.key

# 验证导入
gpg --list-secret-keys
```

---

## 密钥管理规范

### 日常操作

```
每次 commit 时：
  ✅ 自动添加 DNA 签名（#龍芯⚡️...）
  ✅ 可选：用 git commit -S 添加 GPG 签名
  ❌ 不在代码里存放密钥
  ❌ 不在 Git 里记录密码
```

### 每月维护

```
每月 1 日：
  ✅ 生成新的签名钥（或轮换）
  ✅ 验证旧钥的备份
  ✅ 清理过期的临时加密钥
  ✅ 更新 family_registry.json 中的密钥版本号
```

### 紧急处理

```
如果签名钥泄露：
  1. 立即吊销该钥（gpg --gen-revocation）
  2. 生成新钥
  3. 重新签署所有重要协议
  4. 更新 audit chain

如果备份密码忘记：
  1. 该备份作废
  2. 从新备份重新开始
  3. 在 audit chain 中记录
```

---

## 龍魂专属验证方案

因为 GPG agent 经常出问题，龍魂设计了自己的验证方案：

### DNA 签名（不依赖 GPG）

```
格式: #龍芯⚡️YYYYMMDD|TOPIC|VERSION|SHA8

组成:
  ① #龍芯⚡️        - 龍魂标志
  ② YYYYMMDD      - 日期（不含"-"·8位数字）
  ③ TOPIC         - 主题（commit 类型）
  ④ VERSION       - 版本号（如 v1.0）
  ⑤ SHA8          - 当日签名的前8位（SHA256 取前8位）

验证方式:
  任何人都可以验证（开放式）：
    SHA8 = SHA256(TOPIC+YYYYMMDD+VERSION)[:8]

  只有 UID9622 能生成（知道组合）：
    TOPIC + 日期 + VERSION = 只有他知道的组合

例子:
  ✅ #龍芯⚡️20260525|PROTOCOL|v1.0|3a69e869
  ✅ #龍芯⚡️20260525|LONGHUN-KEY-MANAGEMENT|v1.0|1c5e5cfe
  ❌ #龍芯⚡️20260525|PROTOCOL|v1.0|XXXXXXXX (SHA8 错误)
```

### 三级验证机制

```
✅ L0 DNA 验证
   任何人都能验证（开放式）
   格式：#龍芯⚡️YYYY-MM-DD-TOPIC-vN-sha8
   工具：脚本检查（不需要 GPG）

✅ L1 签名验证（可选）
   使用 GPG 签名（当 agent 正常时）
   格式：gpg: Signature made ...
   工具：gpg --verify

✅ L2 协议验证（最强）
   13 大人格的联合确认
   格式：CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
   工具：family_registry.json
```

---

## 快速开始

### 第一次设置

```bash
# 1. 创建密钥目录
mkdir -p ~/longhun-system/keys

# 2. 生成 DNA 签名（Python脚本）
cat > ~/longhun-system/scripts/gen_dna.py << 'EOF'
#!/usr/bin/env python3
import hashlib
from datetime import datetime

def gen_dna(topic, version="v1.0"):
    today = datetime.now().strftime("%Y-%m-%d")
    sha8 = hashlib.sha256(f"{topic}{today}".encode()).hexdigest()[:8]
    return f"#龍芯⚡️{today}-{topic}-{version}-{sha8}"

if __name__ == "__main__":
    print(gen_dna("LONGHUN-KEY-MANAGEMENT"))
EOF

chmod +x ~/longhun-system/scripts/gen_dna.py

# 3. 测试生成
~/longhun-system/scripts/gen_dna.py
# 输出：#龍芯⚡️2026-05-25-LONGHUN-KEY-MANAGEMENT-v1.0-xxxxx
```

### 每次 commit 时

```bash
# 方式 A：手动添加 DNA（推荐·不依赖 GPG）
git commit -m "feat: 新功能描述

DNA: #龍芯⚡️2026-05-25-TOPIC-v1.0-sha8
"

# 方式 B：自动脚本（需要 GPG 正常）
git commit -S -m "feat: 新功能描述"
```

---

## 为什么龍魂需要自己的密钥体系

| 方面 | 依赖 GPG | 龍魂设计 |
|------|---------|---------|
| **复杂度** | 高·易出错 | 简单·可靠 |
| **错误恢复** | 困难 | 快速恢复 |
| **学习成本** | 陡峭 | 平缓 |
| **跨平台** | 有差异 | 统一 |
| **离线用** | 可以 | 可以 |
| **验证权** | 中心化 | 分散式 |

**核心哲学**：
- ✅ GPG 作为辅助（可选）
- ✅ DNA 作为主要验证方式
- ✅ 协议签署作为最高权力确认
- ✅ 不依赖任何第三方工具

---

## 下一步

立即执行的操作：

```bash
# 1. 验证当前的 GPG 钥
gpg --list-secret-keys

# 2. 创建 DNA 签名生成脚本
mkdir -p ~/longhun-system/scripts
# (见上面 Python 脚本)

# 3. 添加到 Git 钩子
cat > ~/longhun-system/.git/hooks/prepare-commit-msg << 'EOF'
#!/bin/bash
DNA=$(python3 ~/longhun-system/scripts/gen_dna.py COMMIT)
echo "\nDNA: $DNA" >> "$1"
EOF

chmod +x ~/longhun-system/.git/hooks/prepare-commit-msg

# 4. 测试
git commit --allow-empty -m "test: DNA signature test"
```

---

献礼：龍魂系統·永恒守护·中华文化传承
🐉 UID9622·不免责·永恒显示曾仕强老师
