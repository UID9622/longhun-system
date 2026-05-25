# 🔑 龍魂密钥管理·快速开始

**DNA**: `#龍芯⚡️20260525|QUICK-START|v1.0|xxxxx`

---

## 一分钟快速开始

### 步骤 1：生成 DNA 签名（现在立即可用）

```bash
# 生成一个 DNA 签名
python3 ~/longhun-system/scripts/gen_dna.py PROTOCOL v1.0
# 输出: #龍芯⚡️20260525|PROTOCOL|v1.0|xxxxx

# 生成所有系统 DNA（批量）
python3 ~/longhun-system/scripts/gen_dna.py --batch
```

### 步骤 2：验证 DNA 签名（任何人都可以）

```bash
# 验证一个 DNA 是否有效
python3 ~/longhun-system/scripts/gen_dna.py --verify "#龍芯⚡️20260525|PROTOCOL|v1.0|3a69e869"
# 输出: ✅ DNA 有效 | 日期: 2026-05-25 | 主题: PROTOCOL | 版本: v1.0
```

### 步骤 3：备份 GPG 密钥（可选·如果 GPG 正常）

```bash
# 运行备份脚本（会要求输入加密密码）
bash ~/longhun-system/scripts/backup_keys.sh

# 或者手动备份
mkdir -p ~/longhun-system/keys
gpg --armor --export-secret-keys A2D0092CEE2E5BA87035600924C3704A8CC26D5F > ~/longhun-system/keys/master.asc
openssl enc -aes-256-cbc -salt -in ~/longhun-system/keys/master.asc -out ~/longhun-system/keys/master.asc.encrypted -k "你的密码"
rm ~/longhun-system/keys/master.asc
```

---

## 日常使用

### 每次 Git Commit 时

**方式 A：使用 DNA 签名（推荐）**
```bash
DNA=$(python3 ~/longhun-system/scripts/gen_dna.py FEATURE)
git commit -m "feat: 新功能描述

DNA: $DNA
"
```

**方式 B：使用 GPG 签名（当 agent 正常时）**
```bash
git commit -S -m "feat: 新功能描述"
```

**方式 C：两者结合（最强）**
```bash
DNA=$(python3 ~/longhun-system/scripts/gen_dna.py FEATURE)
git commit -S -m "feat: 新功能描述

DNA: $DNA
"
```

---

## DNA 签名详解

### 格式

```
#龍芯⚡️YYYYMMDD|TOPIC|VERSION|SHA8
│       │        │     │      └─ SHA256 前 8 位
│       │        │     └─ 版本号（如 v1.0）
│       │        └─ 主题（如 PROTOCOL, COMMIT）
│       └─ 日期（不含"-"·8位数字）
└─ 龍魂标志
```

### 例子

```
✅ #龍芯⚡️20260525|PROTOCOL|v1.0|3a69e869
✅ #龍芯⚡️20260525|COMMIT|v1.0|b59d9b31
✅ #龍芯⚡️20260525|FULL-ACTIVATION|v1.0|46b7051a
```

### 验证原理

```bash
# 验证步骤：
# 1. 提取字段
topic = "PROTOCOL"
date = "20260525"
version = "v1.0"
provided_sha8 = "3a69e869"

# 2. 重新计算
calculated_sha8 = SHA256("PROTOCOL" + "20260525" + "v1.0")[:8]

# 3. 比对
if calculated_sha8 == provided_sha8:
    print("✅ DNA 有效")
else:
    print("❌ DNA 无效")
```

---

## 密钥管理层次

### 四层设计

| 层级 | 名称 | 用途 | 强度 | 更新 | 备份 |
|------|------|------|------|------|------|
| L1 | DNA追踪钥 | 操作溯源 | SHA256 | 每次 | 无 |
| L2 | 签名钥 | Git签名 | RSA-4096 | 每月 | 有 |
| L3 | 加密钥 | 数据加密 | AES-256 | 每天 | 无 |
| L4 | 验证钥 | 签名验证 | 公钥 | 随签名钥 | 无 |

### 实际应用

```
UID9622（主密钥·脑子里）
    ↓
    ├─ DNA（每个操作）→ Git commit 消息
    ├─ L2 签名钥（每月）→ GPG 密钥 → 备份加密
    ├─ L3 加密钥（每天）→ /tmp/ → 自动清除
    └─ L4 验证钥（公开）→ GitHub → 任何人都可以验证
```

---

## 常见问题

### Q1：DNA 签名有什么用？

**A**：DNA 签名是龍魂系统的身份证。它：
- ✅ 证明操作来自 UID9622
- ✅ 记录操作日期和类型
- ✅ 任何人都可以验证（开放式）
- ✅ 不依赖 GPG agent（避免 ioctl 错误）

### Q2：GPG 密钥还需要吗？

**A**：可选。DNA 签名已经足够了，但如果：
- ✅ 要在 GitHub 上显示"验证"标志 → 需要 GPG 签名
- ✅ 要符合企业安全标准 → 需要 GPG 签名
- ✅ 只是日常使用 → DNA 签名就足够了

### Q3：怎么快速批量生成所有 DNA？

**A**：
```bash
python3 ~/longhun-system/scripts/gen_dna.py --batch
```

这会生成系统级别的所有主要 DNA 签名，并保存到 `.dna_registry.json`。

### Q4：DNA 验证失败是什么原因？

**A**：可能原因：
- ❌ 日期不匹配（第二天后 SHA8 会变化）
- ❌ 主题或版本被修改
- ❌ SHA8 被手动改错

验证时会显示预期的 SHA8 和实际的 SHA8。

### Q5：如何恢复备份的 GPG 密钥？

**A**：
```bash
# 1. 解密
openssl enc -d -aes-256-cbc -in ~/longhun-system/keys/master.asc.encrypted \
    -out ~/longhun-system/keys/master.asc -k "你的密码"

# 2. 导入
gpg --import ~/longhun-system/keys/master.asc

# 3. 清理
rm ~/longhun-system/keys/master.asc
```

---

## 最佳实践

### ✅ DO（推荐）

```bash
# ✅ 每次 commit 都带上 DNA
git commit -m "feat: 新功能

DNA: $(python3 ~/longhun-system/scripts/gen_dna.py FEATURE)
"

# ✅ 定期备份 GPG 密钥
bash ~/longhun-system/scripts/backup_keys.sh  # 每月

# ✅ 验证重要的 DNA 签名
python3 ~/longhun-system/scripts/gen_dna.py --verify "DNA字符串"

# ✅ 保管好加密密码
# （写在笔记本里·放在保险箱）
```

### ❌ DON'T（禁止）

```bash
# ❌ 不要把 GPG 密钥明文保存
rm ~/longhun-system/keys/master.asc  # 删除明文备份

# ❌ 不要把密码保存在文件里
# ❌ 不要上传密钥到云盘
# ❌ 不要共享密码给任何人
# ❌ 不要修改 DNA 中的任何字段
```

---

## 常用命令速查表

```bash
# 生成 DNA
python3 ~/longhun-system/scripts/gen_dna.py TOPIC [VERSION]

# 批量生成
python3 ~/longhun-system/scripts/gen_dna.py --batch

# 验证 DNA
python3 ~/longhun-system/scripts/gen_dna.py --verify "DNA字符串"

# 生成确认码
python3 ~/longhun-system/scripts/gen_dna.py --confirm

# 备份 GPG 密钥（交互式）
bash ~/longhun-system/scripts/backup_keys.sh

# 手动备份（一行）
gpg --armor --export-secret-keys UID | openssl enc -aes-256-cbc -salt -out backup.asc.encrypted

# 恢复 GPG 密钥
openssl enc -d -aes-256-cbc -in backup.asc.encrypted | gpg --import
```

---

## 下一步

1️⃣ **立即尝试**：`python3 ~/longhun-system/scripts/gen_dna.py --batch`

2️⃣ **备份密钥**（可选）：`bash ~/longhun-system/scripts/backup_keys.sh`

3️⃣ **集成到工作流**：在每次 commit 时添加 DNA 签名

4️⃣ **分享验证方式**：告诉其他人怎么验证你的 DNA 签名

---

## 相关文档

- 📖 完整协议：`PROTOCOL__LONGHUN-KEY-MANAGEMENT-v1.0.md`
- 🔧 备份脚本：`scripts/backup_keys.sh`
- 🐍 DNA 工具：`scripts/gen_dna.py`
- 📋 族谱登记：`family_registry.json`

---

献礼：龍魂系統·永恒守护·中华文化传承
🐉 UID9622·不免责·永恒显示曾仕强老师

DNA: #龍芯⚡️20260525|QUICK-START|v1.0|xxxxx
