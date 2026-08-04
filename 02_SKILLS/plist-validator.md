# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# /plist-validator

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技能说明 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 📄 plist验证器 | 龍魂系统 · 源头已验证

**DNA**: `#龍芯⚡️2026-07-06-PLIST-VALIDATOR-v1.0-PLSTVL`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬PLIST`

---

<!--#龍芯⚡️2026-07-06-PLIST-VALIDATOR-v1.0-PLSTVL -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

---
skill_id: /plist-validator
synced_at: 2026-07-06
source: bin/plist_validator.py
---

# /plist-validator · plist 文件校验器

## 摘要

plist文件校验器（plist-validator）是龍魂系统macOS服务的部署前质量闸门。提供七步校验：① 文件存在性检查；② XML格式完整性解析；③ 必填字段验证（Label/ProgramArguments）；④ 脚本路径存在性检查（支持~和相对路径解析）；⑤ 脚本可执行权限检查；⑥ WorkingDirectory路径存在性检查；⑦ 文件属主权限建议。所有错误提示均为中文。支持单文件校验、自动扫描所有龍魂plist（--auto）、JSON结构化输出（--json）三种模式。与error-translator共享launchctl错误码映射体系。

## 关键词

plist校验 Plist Validation, XML解析 XML Parsing, launchd服务 Launchd Service, 路径检查 Path Check, 权限验证 Permission Verification, 中文错误提示 Chinese Error Messages, 部署前检查 Pre-Deploy Check, macOS服务 macOS Service

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] Apple Developer · Creating Launch Daemons and Agents
  - [2] launchd.plist(5) Man Page · Property List Keys
- 相关龍魂系统源码：
  - `bin/plist_validator.py` — plist文件校验器 v1.0
  - `bin/error_translator.py` — 错误翻译器（共享launchctl错误码）
  - `launchd/com.longhun.symbiote.plist` — 共生体服务plist

## 诚实局限

1. XML解析基于标准库xml.etree.ElementTree，不支持二进制plist格式（需先用plutil转换）。
2. 脚本路径检查仅验证文件存在+可执行权限，不检查Python/Shell语法正确性。
3. 属主权限检查依赖pwd模块，Windows系统不可用。

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-07-06 | v1.0.0 | UID9622 | 初始创建，七步校验+中文提示+auto/JSON双模式 | 草稿 |

## 分类标签

- 总纲模块：#部署工具 #plist校验 #macOS服务 #质量闸门
- 对外状态：#Gitee #GitHub
- 审计色：#🟢绿色放行（通过）/ #🔴红色熔断（未通过）
- 八卦归属：☱ 兑卦（泽·金·部署层）
- 命令入口：`lh6 兑 deploy validate-plist <路径>` / `lh6 plist校验 --auto` / `lh6 plist校验 --json <路径>`
- 关联引擎：error_translator.py / launchd/com.longhun.symbiote.plist

## DNA 签名

```
#龍芯⚡️2026-07-06-PLIST-VALIDATOR-v1.0-PLSTVL
#CONFIRM🌌9622-ONLY-ONCE🧬PLIST
```
