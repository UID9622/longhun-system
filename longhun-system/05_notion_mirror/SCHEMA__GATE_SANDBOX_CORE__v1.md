# 龍魂·Notion 主表统一 schema：GATE_SANDBOX_CORE
# DNA: #龍芯⚡️2026-04-26-NOTION-GATE-SCHEMA-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 作者：龍芯北辰｜UID9622
# 理论指导：曾仕强老師（永恒显示）
#
# 决策：取 Feed⑤ v3.0 的 GATE_SANDBOX_CORE（Feed④ v1.2 的 SANDBOX_CORE 是其严格子集）

---

## 0. 命名约定

- **主表名**：`GATE_SANDBOX_CORE`（不再使用 `SANDBOX_CORE`）
- **字段命名**：英文驼峰（与 Webhook payload 对齐），中文仅作备注
- **必填**：`Title / Input / Source / Status`
- **公式字段**：`AuditColor / NextState / Bucket / Heat`（避免脏数据）

---

## 1. 主表 GATE_SANDBOX_CORE

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `Title` | Title | ✅ | 条目标题（自动用前 30 字摘要） |
| `Input` | Text | ✅ | 原始输入 |
| `Summary` | Text | ❌ | 自动摘要 |
| `Source` | Select | ✅ | ChatGPT / Claude / DeepSeek / Grok / Notion / GitHub / 手写 / cnsh-chrome-plugin |
| `DNA` | Text | ❌ | DNA 追溯码（缺失时由引擎补 L4 临时码） |
| `ContentHash` | Formula | ❌ | SHA256(Input) 前 16 位 |
| **── 第一道闸门（新增）──** | | | |
| `DigitalRoot` | Number | ❌ | 数字根 dr（0-9） |
| `GateColor` | Select | ❌ | 🟢 通行 / 🟡 待审 / 🔴 熔断 |
| `DNAStatus` | Select | ❌ | L0合法 / 合法 / 缺失 / 疑似伪造 |
| `RuleCheck` | Select | ❌ | 🟢 / 🟡 / 🔴 |
| `FalsehoodCheck` | Select | ❌ | 🟢 / 🟡 / 🔴 |
| `DataGuardCheck` | Select | ❌ | 🟢 / 🟡 / 🔴 |
| **── 抽屉×五行 ──** | | | |
| `DrawerID` | Multi-select | ❌ | 命中抽屉编号（如 `11`、`27`） |
| `DrawerName` | Multi-select | ❌ | 抽屉中文名 |
| `SemanticRegion` | Select | ❌ | COGNITION / IDENTITY / RULE / EXECUTION / FLOW / SYSTEM / VALUE / HUMAN |
| `Element` | Select | ❌ | 主五行：金/水/木/火/土 |
| `ElementPair` | Text | ❌ | 五行组合（如 `金-木`） |
| `ElementRelation` | Select | ❌ | 相生 / 相克 / 比和 / 混合 / 相耗 |
| **── 路由/状态 ──** | | | |
| `RouteType` | Select | ❌ | PARSE / TRACE / EXEC / RULE_CHECK / BREAK / ... |
| `State` | Select | ❌ | S0_INPUT_GATE 至 S9_ARCHIVE |
| `NextState` | Formula | ❌ | 下一状态推断 |
| `Engine` | Select | ❌ | Semantic / Rule / Execution / Safety / ... |
| **── 评估（六维）──** | | | |
| `WeightLevel` | Select | ❌ | L0 / L1 / L1.5 / L2 / L3 / L4 |
| `RiskLevel` | Select | ❌ | 低 / 中 / 高 / 极高 |
| `AuditColor` | Formula | ❌ | 🟢 / 🟡 / 🟠 / 🔴（综合 GateColor + 三重检测） |
| `Contribution` | Number | ❌ | 0-10 贡献值 |
| `Heat` | Formula | ❌ | 🔥/⚡/✅/⚠️/💤 |
| `Bucket` | Formula | ❌ | 五桶分桶（草日志/入库/消化/迭代/归档） |
| **── 执行控制 ──** | | | |
| `NeedConfirm` | Checkbox | ❌ | 是否需老大确认 |
| `TimeoutAt` | Date | ❌ | 待审超时时间（dr=6 时引擎写入 +5min） |
| `Action` | Text | ❌ | 执行动作描述 |
| `Status` | Status | ✅ | 未扫 / 待审 / 执行中 / 完成 / 熔断 / 归档 |
| `Result` | Text | ❌ | 执行结果 |
| `Error` | Text | ❌ | 错误信息 |
| **── 追溯 ──** | | | |
| `TraceChain` | Text | ❌ | DNA 证据链（多条 DNA 用 `→` 连接） |
| `SourceRef` | Relation | ❌ | 关联来源条目 |
| `ContextRef` | Relation | ❌ | 关联上下文条目 |
| `Version` | Text | ❌ | 版本标签（如 `v1.2`） |
| **── 时间 ──** | | | |
| `CreatedAt` | Created time | ❌ | 自动 |
| `UpdatedAt` | Last edited time | ❌ | 自动 |
| `ClosedAt` | Date | ❌ | 闭环完成时间 |

---

## 2. 公式字段定义

### 2.1 `AuditColor`（综合审计色）

```js
if(prop("GateColor") == "🔴 熔断", "🔴",
if(prop("RuleCheck") == "🔴", "🔴",
if(prop("FalsehoodCheck") == "🔴", "🔴",
if(prop("DataGuardCheck") == "🔴", "🔴",
if(or(
   prop("RuleCheck") == "🟡",
   prop("FalsehoodCheck") == "🟡",
   prop("DataGuardCheck") == "🟡",
   prop("GateColor") == "🟡 待审"
), "🟡",
"🟢")))))
```

### 2.2 `NextState`（下一状态推断）

```js
if(prop("AuditColor") == "🔴", "S8_BREAK_RECOVER",
if(prop("AuditColor") == "🟡", "S4_RULE_CONFIRM",
if(prop("Element") == "金", "S4_RULE_CONFIRM",
if(prop("Element") == "水", "S1_DNA_BIND",
if(prop("Element") == "木", "S6_EXECUTE",
if(prop("Element") == "火", "S2_SEMANTIC_PARSE",
if(prop("Element") == "土", "S7_AUDIT_LOOP",
"S2_SEMANTIC_PARSE")))))))
```

### 2.3 `Bucket`（五桶分桶）

```js
if(prop("AuditColor") == "🔴", "🔴 熔断封存",
if(prop("NeedConfirm") == true, "🔁 待迭代升级池",
if(prop("Contribution") >= 8, "📦 入库/封装",
if(prop("Contribution") >= 5, "🟢 推草日志",
if(prop("Contribution") >= 1, "⚡ 内部消化",
"💤 归档")))))
```

### 2.4 `Heat`（热度）

```js
if(dateBetween(now(), prop("UpdatedAt"), "days") <= 7, "🔥",
if(dateBetween(now(), prop("UpdatedAt"), "days") <= 30, "✅",
if(dateBetween(now(), prop("UpdatedAt"), "days") <= 60, "⚠️",
"💤")))
```

---

## 3. 辅助数据库（10 张）

| 数据库 | 用途 | 关键字段 |
|--------|------|---------|
| `DNA_TRACE_LOG` | DNA 证据链全量 | seq / ts / dna / prev_hash / self_hash |
| `GATE_FUSE_LOG` | 数字根熔断专项日志 | dr / text_hash / triggered_at |
| `TRI_CHECK_LOG` | 三重检测全量记录 | rule / falsehood / data_guard |
| `AUDIT_LOG` | 三色审计汇总 | uid / op_type / summary / payload |
| `RULE_LOCK_TABLE` | P0++ 锁定规则表 | rule_id / locked_at / lock_reason |
| `ITERATION_POOL` | 待迭代升级池 | item / why_paused / trigger_condition |
| `INTERNAL_DIGEST` | 内部消化区 | issue / fix_method / done |
| `SANDBOX_ARCHIVE` | 旧链接归档 | original_url / replacement / archive_reason |
| `VERSION_LOG` | 版本更新日志 | module / version / changes |
| `PERSONA_REGISTRY` | 人格调度注册表 | persona_id / scope / activate_keywords |

---

## 4. 视图（建议 8 个）

| 视图名 | 过滤条件 | 用途 |
|--------|---------|------|
| 今日待过闸 | `Status = 未扫` AND `CreatedAt = today()` | 当天复盘入口 |
| 数字根熔断 | `GateColor = 🔴 熔断` | 查看本周/本月所有数学红线 |
| 三重检测待审 | `AuditColor = 🟡` AND `NeedConfirm = true` | 等老大批的池 |
| P0++ 触碰 | `RuleCheck = 🔴` AND `Input contains "P0"` | 核心规则保护监控 |
| 可执行队列 | `AuditColor = 🟢` AND `RouteType = EXEC` | 待执行任务 |
| 高价值入库 | `Contribution >= 8` | 即将封装为系统能力 |
| 旧链归档 | `Heat = 💤` | 清理候选 |
| 本周复盘 | `CreatedAt within 7 days` | 周报数据源 |

---

## 5. 按钮（6 个）

| 按钮 | 触发动作 |
|------|---------|
| 🚪 过闸门 | 调用 `gate_engine.decide()` → 写 DigitalRoot/GateColor/DNAStatus |
| 🛡️ 三重检测 | 调用 `rule_check + falsehood_check + data_guard_check` |
| 🧠 宝宝复盘 | 摘要 + 抽屉识别 + 五行 + 贡献值 + 分桶 |
| 🚀 执行 | 前置 `AuditColor = 🟢` AND `State != S8` → 触发 Webhook |
| 🔁 回滚 | `State → S8_BREAK_RECOVER` + 调用 RecoveryEngine |
| 💤 归档 | `Status → 已归档` + `Bucket → 归档旧链接池` |

---

## 6. Webhook payload 契约

```json
{
  "page_id":      "{{PAGE_ID}}",
  "dna":          "{{DNA}}",
  "input":        "{{Input}}",
  "digital_root": "{{DigitalRoot}}",
  "gate_color":   "{{GateColor}}",
  "audit_color":  "{{AuditColor}}",
  "drawer_id":    "{{DrawerID}}",
  "element":      "{{Element}}",
  "route":        "{{RouteType}}",
  "state":        "{{State}}",
  "engine":       "{{Engine}}",
  "bucket":       "{{Bucket}}",
  "action":       "{{Action}}"
}
```

---

## 7. 与本地 dna_chain.jsonl 的关系

| 项 | Notion `DNA_TRACE_LOG` | 本地 `dna_chain.jsonl` |
|----|------------------------|------------------------|
| 写入入口 | 远程 Webhook 回写 | `dna_append_log.py append()` |
| 主权 | 公开可查 | 本地我做主，不出境 |
| 完整性 | Notion 自动版本 | prev_hash + self_hash 链式自校验 |
| 同步策略 | **本地优先**——本地写入成功后异步同步 Notion；Notion 失败不影响本地 |

> 与 `bin/dna_append_log.py` 第 213 行铁律一致：「本地优先：日志写本地 dna_chain.jsonl，再异步同步 Notion（Notion挂了不影响本地留痕）。」

---

## 8. 落地步骤（建议）

1. 在北极星工作区新建 `GATE_SANDBOX_CORE` 主表 + 10 张辅助表
2. 录入字段（按本文清单）
3. 加 4 条公式
4. 加 8 个视图
5. 加 6 个按钮
6. 配置 Webhook → 本地 `:9622/api/tongxinyi/v1/translate`（沿用 `external_api_protocol.md`）
7. 沙盒跑一周再接主系统（Feed⑤ 强烈建议）

---

`DNA: #龍芯⚡️2026-04-26-NOTION-GATE-SCHEMA-v1.0`
`确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
