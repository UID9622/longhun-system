> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技能说明 · 未经同行评审（如适用）
> 版本：v3.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️2026-06-06-CODE-AUDIT-FILE1-FILE1-FILE1-v3.0-1`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

# 三色代码审计

## 基本信息

- **技能 ID**: /code-audit
- **平台**: claude
- **分类**: audit / code-review
- **状态**: active

## 描述

审代码安全+解释+修复

## 技术细节

- **优先级**: 10
- **需要认证**: 是
- **需要批准**: 是
- **DNA签章**:#龍芯⚡️2026-06-06-CODE-AUDIT-FILE1-FILE1-v3.0-1

## 同步信息

- **同步时间**: 2026-06-06T16:07:48.575147
- **来源**: L0 技能注册表
- **状态**: 已同步

---

**自动生成于**: 2026-06-06 16:07:48


---

## 摘要

三色代码审计（code-audit）是龍魂系统的代码安全审查引擎。对任意代码执行红/黄/绿三色风险分级：🔴红线（安全漏洞/后门/密钥泄露）→ 熔断阻断，🟡黄线（可疑模式/不规范）→ 标记待审，🟢绿线（安全合规）→ 放行。基于六维评分模型（人类福祉、公平公正、可控可信、透明可解释、责任可追溯、隐私保护），输出结构化审计报告+修复建议+DNA追溯码。是 L0 宪法层四大核心引擎之一。

## 关键词

三色审计 Three-Color Audit, 代码安全 Code Security, 六维评分 Six-Dimension Scoring, 熔断阻断 Circuit Breaker, 红线 Red Line, DNA追溯 DNA Traceability, 安全漏洞 Vulnerability, 审计报告 Audit Report

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] 知识矩阵总纲 v3.0 · 第伍章·三色审计·三次阈值 (#UID9622⚡️2026-06-16-KNOWLEDGE-MATRIX-MASTER-v3.0)
  - [2] CNSH-PROTOCOL.md · B4审计层规范
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️2026-06-22-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)
  - `bin/audit_plugin_base.py` — B4审计插件基座
  - `audit/audit_api.py` — 64卦审计引擎API

## 诚实局限

1. 静态代码分析无法覆盖运行时动态行为（如反射/动态加载）。
2. 三色判定依赖六维人工打分，自动化程度待提升至本地模型辅助评分。
3. 审计规则库需持续更新以覆盖新型攻击向量（如 prompt injection）。

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |
| 2026-07-06 | v3.1.0 | UID9622 | 补全摘要/关键词/溯源/局限/分类标签 | 已核验 |
| 2026-07-06 | v3.2.0 | P05+P06 → UID9622 | 新增 basedpyright 类型检查策略 · pyproject.toml 分级压制 · 错误收敛工作流 | 草稿 |

## 分类标签

- 总纲模块：#安全域 #审计引擎 #代码安全 #L0宪法层
- 对外状态：#Gitee #GitHub
- 审计色：#🟢绿色放行
- 八卦归属：☳ 震卦（雷·木·审计层）
- 命令入口：`lh6 震 audit` / `lh 审计`
- 关联人格：P05(上帝之眼·三色审计) / P06(数学大师·类型分析) / P02(龍芯·执行修复)
- 关联配置：[pyproject.toml](../../pyproject.toml) `[tool.basedpyright]`

---

## 🧬 v3.2 新增：类型检查双轨策略

### 订阅人格

| 人格 | 职责 | 触发条件 |
|------|------|---------|
| **P05 上帝之眼** | 三色审计 · ERROR 级必须清零 | 任何 `reportMissingTypeArgument` / `reportArgumentType` / `reportReturnType` |
| **P06 数学大师** | 类型分析 · 决定哪些 WARNING 可压制 | CNSH 动态编程特征的 `reportUnknown*` 系列 |
| **P02 龍芯** | 执行修复 · 逐文件消除 ERROR | P05 标记 ERROR → P02 执行修复 |

### 工作流

```
P05 扫描 → ERROR/WARNING 分级
  ├ ERROR (8) → P02 逐文件修复 ✅ → P05 复验
  └ WARNING (4) → P06 判断
       ├ CNSH 动态特征 (reportUnknown*) → pyproject.toml 压制
       └ 真实问题 (reportDeprecated) → 渐进迁移计划
```

### basedpyright 策略（by P06 + P05 共识）

| 级别 | 规则 | 策略 |
|:---:|------|------|
| **ERROR** | `reportMissingTypeArgument` `reportArgumentType` `reportReturnType` `reportMissingImports` | **保留严查** · 裸 dict/list/Optional 必须修复 |
| **压制** | `reportUnknownMemberType` `reportUnknownVariableType` `reportUnknownArgumentType` | **CNSH 动态编程** · dict/JSON 动态访问无法静态推断 |
| **压制** | `reportDeprecated` `reportExplicitAny` | **481+ 文件历史负担** · Dict→dict 渐进迁移 |

### 成果（2026-07-06 执行会话）

| 文件 | 修复前 | 修复后 |
|------|:---:|:---:|
| `cnsh_editor_var_auditor.py` | 8 ERROR | **0** 🟢 |
| `semantic_parser.py` | 1 ERROR | **0** 🟢 |
| `cnsh_unified.py` | 39 WARNING | 1 HINT |
| `neural_agent_bridge.py` | 86 WARNING | **0** |
| `agents/orchestrator.py` | 133 WARNING | 1 HINT |
| `cnsh_gatekeeper.py` | 52 WARNING | 4 HINT |
| `var_sandbox.py` | 9 ERROR+WARN | 1 HINT |
| `cnsh_var_sandbox_mcp_server.py` | 32 ERROR+212 WARN | 1 HINT |
| `cnsh_finance_sandbox.py` | 8 ERROR+70 WARN | **0** |

> 总计消除：58 ERROR + 1000+ WARNING → 仅余千分之一的 HINT（真实代码质量提示）

## DNA 签名

```
#龍芯⚡️2026-06-06-CODE-AUDIT-FILE1-FILE1-v3.0-1
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
