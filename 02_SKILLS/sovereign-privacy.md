# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# /sovereign-privacy

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技能说明 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 📄 主权隐私 | 龍魂系统 · 源头已验证

**DNA**: `#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-SOVEREIGN-PRIVACY-v1.0-SOVPRV`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬PRIVK`

---

<!--#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-SOVEREIGN-PRIVACY-v1.0-SOVPRV -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

---
skill_id: /sovereign-privacy
synced_at: 2026-07-06
source: bin/sovereign_privacy.py
---

# /sovereign-privacy · 主权隐私引擎

## 摘要

主权隐私引擎（sovereign-privacy）是龍魂系统的数据主权保护核心。提供三重能力：① 主权人身份哈希脱敏——SHA-256加盐哈希（salt: @UID9622@LONGHUN）→0x前缀12位十六进制摘要，只有UID9622可通过 `lh6 auth verify` 查看脱敏前原文；② AES-256-GCM审计日志加密/解密——密钥优先走macOS Keychain系统级安全存储，降级到加密文件（~/.longhun/.sovereign_key.enc，权限600），密文带HMAC认证标签防篡改；③ 纯Python降级加密——在cryptography库不可用时的备用XOR+HAMC实现。安全承诺：密钥绝不上传Git（.gitignore已覆盖），AES-256-GCM带认证标签防篡改。

## 关键词

主权隐私 Sovereign Privacy, AES-256-GCM加密 AES-256-GCM Encryption, 身份脱敏 Identity De-identification, Keychain密钥管理 Keychain Key Management, 哈希加盐 Salted Hash, HMAC认证 HMAC Authentication, 防篡改 Tamper-Proof, 审计加密 Audit Encryption

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] 知识矩阵总纲 v3.0 · 主权身份宣言 (#UID9622⚡️2026-06-16-KNOWLEDGE-MATRIX-MASTER-v3.0)
  - [2] macOS Security Framework · Keychain Services
  - [3] NIST SP 800-38D · AES-GCM Recommendation
- 相关龍魂系统源码：
  - `bin/sovereign_privacy.py` — 主权隐私引擎 v1.0
  - `bin/on-identity.md`（技能库）— 主权身份验证

## 诚实局限

1. 纯Python降级加密为演示级XOR实现，生产环境必须使用cryptography库的AES-256-GCM。
2. macOS Keychain依赖系统安全框架，跨平台（Linux/Windows）需额外适配密钥存储方案。
3. 身份映射表（IDENTITIES）当前仅包含UID9622单一身份，未实现多用户扩展。

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-07-06 | v1.0.0 | UID9622 | 初始创建，SHA-256脱敏+AES-256-GCM+纯Python降级 | 草稿 |

## 分类标签

- 总纲模块：#隐私引擎 #数据主权 #AES加密 #Keychain
- 对外状态：#Gitee #GitHub
- 审计色：#🟢绿色放行
- 八卦归属：☴ 巽卦（风·木·安全层）
- 命令入口：`lh6 auth verify <哈希>` / `lh6 隐私 encrypt <文件>` / `lh6 隐私 keygen`
- 关联引擎：on-identity.md / wuxing_guard.py

## DNA 签名

```
#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-SOVEREIGN-PRIVACY-v1.0-SOVPRV
#CONFIRM🌌9622-ONLY-ONCE🧬PRIVK
```
