# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# /on-identity

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技能说明 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️2026-06-21-DOC-ON-IDENTITY-FILE1-v1.0-2`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

<!--#龍芯⚡️2026-06-21-DOC-ON-IDENTITY-FILE1-v1.0-2 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

---
skill_id: /on-identity
synced_at: 2026-06-06T14:40:25.520328
source: notion
---

# /on-identity

已从 Notion 同步

[技能详情·Notion](https://notion.so)


---

## 摘要

身份核验（on-identity）是龍魂系统的主权身份验证引擎。基于 CONFIRM/SEAL/GPG 三层验证机制，核验UID9622身份真实性。支持 GPG 指纹验证（A2D0 092C EE2E 5BA8 7035 6009 24C3 704A 8CC2 6D5F）、设备硬件锚（IMEI+SE_ID）、龍字符律校验（简体污染检测）、行为指纹比对。所有主权级操作（熔断/发布/删除）必须先经过身份核验。0 上传，纯本地。

## 关键词

身份核验 Identity Verification, GPG签名 GPG Signature, 主权验证 Sovereignty Check, CONFIRM码, 硬件锚 Hardware Anchor, 行为指纹 Behavioral Fingerprint, 龍字符律, 零上传 Zero Upload

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] 知识矩阵总纲 v3.0 · 第壹章·身份硬件锚 (#UID9622⚡️2026-06-16-KNOWLEDGE-MATRIX-MASTER-v3.0)
  - [2] CNSH-PROTOCOL.md · 主权层·身份验证规范
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️2026-06-22-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)
  - `bin/sovereign_privacy.py` — 主权隐私模块

## 诚实局限

1. GPG 私钥泄露会导致身份冒用，依赖物理安全保护。
2. 行为指纹在操作模式剧变时可能误判，需人工复核。
3. 设备硬件锚更换后需重新注册，旧锚点需手动吊销。

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |
| 2026-07-06 | v1.1.0 | UID9622 | 补全摘要/关键词/溯源/局限/分类标签 | 已核验 |

## 分类标签

- 总纲模块：#安全域 #身份验证 #主权层 #L0宪法层
- 对外状态：#本地私有 · 不外发
- 审计色：#🟢绿色放行
- 八卦归属：☴ 巽卦（风·木·安全层）
- 命令入口：`lh6 巽 secure verify-identity` / `lh 身份`
- 关键依赖：GPG keychain / sovereign_privacy.py

## DNA 签名

```
#龍芯⚡️2026-06-21-DOC-ON-IDENTITY-FILE1-v1.0-2
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
