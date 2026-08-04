# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# /audit-plugin

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技能说明 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 📄 审计插件 | 龍魂系统 · 源头已验证

**DNA**: `#龍芯⚡️2026-07-06-AUDIT-PLUGIN-v1.0-5A3F8C1D`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬B4-PLUGIN`

---

<!--#龍芯⚡️2026-07-06-AUDIT-PLUGIN-v1.0-5A3F8C1D -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

---
skill_id: /audit-plugin
synced_at: 2026-07-06
source: bin/audit_plugin_base.py
---

# /audit-plugin · B4审计插件基类

## 摘要

B4审计插件基类（audit-plugin）是龍魂系统可插拔审计架构的核心基础设施。为所有B4审计命令提供统一插件基类（AuditPlugin ABC），支持动态注册/发现审计插件，内置三色审计（🟢🟡🔴）报告生成器。预注册DNA追溯验证（DNAVerifierPlugin）和CNSH命名规范审计（NamingConventionPlugin）两个内置插件。还提供B3快捷命令注册表（ShortcutRegistry），打通A4与B3边界。哲学锚为河图洛书中五不动点→四象审计→八卦分类。铁律：所有B4审计操作只读，不可修改系统状态。

## 关键词

可插拔审计 Pluggable Audit, 审计基类 AuditPlugin ABC, 三色报告 Three-Color Report, 插件注册表 Plugin Registry, DNA验证 DNA Verification, 命名规范 Naming Convention, B4审计层 B4 Audit Layer, 只读操作 Read-Only Operation

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] 知识矩阵总纲 v3.0 · 第肆章·三色审计 (#UID9622⚡️2026-06-16-KNOWLEDGE-MATRIX-MASTER-v3.0)
  - [2] CNSH命令与变量命名规范 v2.0 · 命名空间前缀规则
- 相关龍魂系统源码：
  - `bin/audit_plugin_base.py` — B4审计插件基类 v1.0
  - `bin/hetu_luoshu_dna.py` — 河图洛书DNA引擎（数字根联动）

## 诚实局限

1. 内置DNA验证器仅检查繁体龍/全角下划线/DNA格式等表面级合规，不检查语义正确性。
2. 命名规范审计基于正则匹配，对复杂嵌套结构的识别有遗漏风险。
3. 插件注册表为内存态，未持久化到磁盘，进程重启后需重新注册。

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-07-06 | v1.0.0 | UID9622 | 初始创建，内置DNA+命名两大审计插件 | 草稿 |

## 分类标签

- 总纲模块：#审计引擎 #可插拔架构 #B4审计层 #三色报告
- 对外状态：#Gitee #GitHub
- 审计色：#🟢绿色放行
- 八卦归属：☳ 震卦（雷·木·审计层）
- 命令入口：`lh6 审计插件 list` / `lh6 审计插件 dna <文件>` / `lh6 审计插件 naming <文件>`
- 关联引擎：hetu_luoshu_dna.py / code-audit.md

## DNA 签名

```
#龍芯⚡️2026-07-06-AUDIT-PLUGIN-v1.0-5A3F8C1D
#CONFIRM🌌9622-ONLY-ONCE🧬B4-PLUGIN
```
