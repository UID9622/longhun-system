# GPG 签名验证说明

**DNA追溯码**: #ZHUGEXIN⚡️20260201-CNSH-EDITOR-GPG-v1.0
**创始人**: Lucky·UID9622（诸葛鑫·龍芯北辰）
**GPG指纹**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

---

## 📌 关于 GPG 签名

本仓库代码的真实性通过 GPG 签名保护。

**GPG主密钥指纹**：
```
A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```

---

## ✅ 如何验证代码真实性

### 方法1：验证 GPG 签名文件

```bash
# 1. 导入作者公钥
gpg --keyserver keys.openpgp.org --recv-keys A2D0092CEE2E5BA87035600924C3704A8CC26D5F

# 2. 验证 README 签名
gpg --verify README.md.asc README.md

# 3. 验证 Git 提交签名
git log --show-signature
```

### 方法2：验证 DNA 追溯码

所有文件头部都包含 DNA 追溯码，格式：
```
#ZHUGEXIN⚡️YYYYMMDD-描述-版本号
```

追溯码说明：
- `ZHUGEXIN` = 诸葛鑫（创始人汉语拼音）
- `YYYYMMDD` = 创建日期（可对照 Git 提交时间戳验证）
- 描述 = 该文件用途
- 版本号 = 该版本号

---

## 🔐 签名状态

| 文件 | 签名状态 | 说明 |
|------|----------|------|
| README.md | ⏳ 待签名 | 需在本地由 UID9622 签名 |
| LICENSE | ⏳ 待签名 | 需在本地由 UID9622 签名 |
| Git commits | ⏳ 待配置 | 需本地配置 GPG 提交签名 |

---

## 📋 UID9622 本地签名操作（仅作者执行）

```bash
# 签名 README.md
gpg --detach-sign -a --default-key A2D0092CEE2E5BA87035600924C3704A8CC26D5F README.md
# 生成 README.md.asc

# 提交签名文件
git add README.md.asc
git commit -S -m "Add GPG signature for README.md"
git push

# 配置 Git 自动 GPG 签名
git config user.signingkey A2D0092CEE2E5BA87035600924C3704A8CC26D5F
git config commit.gpgsign true
```

---

## 🌐 公钥发布位置

作者公钥已发布至：
- `keys.openpgp.org`
- 可通过指纹 `A2D0092CEE2E5BA87035600924C3704A8CC26D5F` 查找

---

**#CONFIRM🌌9622-ONLY-ONCE🧬CNSH-EDITOR-772Z**
