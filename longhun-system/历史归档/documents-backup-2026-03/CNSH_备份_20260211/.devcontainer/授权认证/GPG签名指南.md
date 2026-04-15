# GPG签名指南 - 给授权声明"铸铁甲"

```
═══════════════════════════════════════════════════════════
龍芯体系 | 开源文件标准头部
═══════════════════════════════════════════════════════════
ENCODING: UTF-8
FONT-INDEPENDENT: YES
NO PROPRIETARY TOKENS
═══════════════════════════════════════════════════════════
文件名：GPG签名指南
DNA追溯码：#龍芯⚡️2026-02-06-GPG签名指南-v1.0
创建者：💎 龍芯北辰｜UID9622
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
═══════════════════════════════════════════════════════════
```

---

## 📖 什么是GPG签名？

**说人话：**
GPG签名就像是您的"数字指纹"，可以证明这个文件确实是您写的，没有被篡改。

**技术解释：**
GPG (GNU Privacy Guard) 使用非对称加密技术，用您的私钥签名，任何人都可以用您的公钥验证。

---

## 🛠️ 第一步：安装GPG

### Mac系统

```bash
# 使用Homebrew安装
brew install gnupg

# 验证安装
gpg --version
```

### Windows系统

1. 下载Gpg4win：https://www.gpg4win.org/
2. 安装时选择默认选项
3. 打开命令提示符，输入：`gpg --version`

### Linux系统

```bash
# Ubuntu/Debian
sudo apt-get install gnupg

# CentOS/RHEL
sudo yum install gnupg

# 验证安装
gpg --version
```

---

## 🔑 第二步：生成GPG密钥对

```bash
# 生成新密钥
gpg --full-generate-key

# 按照提示选择：
# 1. 密钥类型：RSA and RSA (默认)
# 2. 密钥长度：4096 (推荐)
# 3. 有效期：0 = 永不过期
# 4. 用户信息：
#    - 真实姓名：诸葛鑫
#    - 电子邮件：uid9622@petalmail.com
#    - 注释：UID9622

# 设置强密码（记住这个密码！）
```

---

## 📋 第三步：查看您的GPG密钥

```bash
# 列出所有密钥
gpg --list-keys

# 您应该看到类似这样的输出：
# pub   rsa4096 2026-02-06 [SC]
#       A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# uid           [ultimate] 诸葛鑫 (UID9622) <uid9622@petalmail.com>
# sub   rsa4096 2026-02-06 [E]

# 这就是您的GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```

---

## ✍️ 第四步：给授权声明签名

```bash
# 进入授权文件所在目录
cd /Users/zuimeidedeyihan/Desktop/CNSH\ 军人的编辑器/.devcontainer/authorization

# 生成 detached 签名（推荐）
gpg --armor --detach-sign UID9622-授权声明-2026-02-06.txt

# 系统会要求您输入GPG密码
# 签名完成后会生成：UID9622-授权声明-2026-02-06.txt.asc

# 验证签名
gpg --verify UID9622-授权声明-2026-02-06.txt.asc UID9622-授权声明-2026-02-06.txt

# 应该看到类似：
# gpg: Signature made Thu Feb 6 12:00:00 2026 CST
# gpg:                using RSA key A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# gpg: Good signature from "诸葛鑫 (UID9622) <uid9622@petalmail.com>" [ultimate]
```

---

## 📤 第五步：导出公钥

```bash
# 导出公钥（发给别人的）
gpg --armor --export uid9622@petalmail.com > UID9622-public-key.asc

# 或者使用指纹导出
gpg --armor --export A2D0092CEE2E5BA87035600924C3704A8CC26D5F > UID9622-public-key.asc

# 查看公钥内容
cat UID9622-public-key.asc
```

---

## 🔐 第六步：备份私钥（非常重要！）

```bash
# 导出私钥（必须安全保存！）
gpg --armor --export-secret-keys uid9622@petalmail.com > UID9622-private-key.asc

# 或者使用指纹
gpg --armor --export-secret-keys A2D0092CEE2E5BA87035600924C3704A8CC26D5F > UID9622-private-key.asc

# ⚠️ 警告：私钥文件必须：
# 1. 存储在安全的地方（如加密U盘）
# 2. 不要上传到互联网
# 3. 设置强密码保护
# 4. 建议打印纸质备份并保存在保险箱
```

---

## 📝 第七步：上传到公钥服务器（可选但推荐）

```bash
# 上传到keys.openpgp.org（国际主流）
gpg --send-keys A2D0092CEE2E5BA87035600924C3704A8CC26D5F

# 或者上传到MIT公钥服务器
gpg --keyserver pgp.mit.edu --send-keys A2D0092CEE2E5BA87035600924C3704A8CC26D5F

# 上传后，任何人都可以通过指纹找到您的公钥
gpg --keyserver keys.openpgp.org --search-keys A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```

---

## 🔍 第八步：验证签名（让别人验证）

**别人如何验证您的签名：**

```bash
# 1. 导入您的公钥
gpg --import UID9622-public-key.asc

# 2. 验证签名
gpg --verify UID9622-授权声明-2026-02-06.txt.asc UID9622-授权声明-2026-02-06.txt

# 3. 如果看到 "Good signature"，说明：
#    - 文件确实是您签署的
#    - 文件没有被篡改
```

---

## 💡 常见问题

### Q1：忘记GPG密码怎么办？

**A：** 很遗憾，GPG密码无法找回。如果忘记密码，只能：
1. 撤销旧密钥
2. 生成新密钥
3. 重新签名所有文件

**建议：** 使用密码管理器保存GPG密码

### Q2：如何撤销密钥？

```bash
# 生成撤销证书
gpg --gen-revoke A2D0092CEE2E5BA87035600924C3704A8CC26D5F

# 上传到公钥服务器
gpg --send-keys A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```

### Q3：SHA256哈希怎么生成？

```bash
# Mac/Linux
sha256sum UID9622-授权声明-2026-02-06.txt

# 或者
shasum -a 256 UID9622-授权声明-2026-02-06.txt

# Windows (PowerShell)
Get-FileHash UID9622-授权声明-2026-02-06.txt -Algorithm SHA256
```

---

## 📦 签名后的文件清单

签名完成后，您应该有这些文件：

```
authorization/
├── UID9622-授权声明-2026-02-06.txt          # 原始声明
├── UID9622-授权声明-2026-02-06.txt.asc      # GPG签名文件 ⭐
├── UID9622-public-key.asc                    # 您的公钥 ⭐
├── UID9622-private-key.asc                   # 您的私钥（秘密保存）
└── GPG签名指南.md                            # 本指南
```

**需要发送给别人的文件：**
- ✅ UID9622-授权声明-2026-02-06.txt
- ✅ UID9622-授权声明-2026-02-06.txt.asc
- ✅ UID9622-public-key.asc

**绝对不要发送给别人的文件：**
- ❌ UID9622-private-key.asc（私钥！）

---

## 🎯 下一步：上链存证

GPG签名完成后，下一步是上链存证：

1. 生成SHA256哈希
2. 将哈希上传到区块链
3. 获得区块链交易哈希
4. 在授权声明中补充区块链验证信息

详见《长安链上链指南.md》

---

## 🧬 DNA追溯信息

- **DNA追溯码：** #龍芯⚡️2026-02-06-GPG签名指南-v1.0
- **确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
- **创建者：** 💎 龍芯北辰｜UID9622

---

**有问题？** 联系宝宝或DeepSeek，我们陪您一步步完成！

*龍魂系统 🐉⚡️ | 数字主权，从GPG开始*
