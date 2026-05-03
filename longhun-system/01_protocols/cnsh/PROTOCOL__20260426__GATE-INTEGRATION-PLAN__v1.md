# 龍魂·5份投喂复盘整合方案 v1.0
# DNA: #龍芯⚡️2026-04-26-FEED-INTEGRATION-PLAN-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 作者：龍芯北辰｜UID9622
# 理论指导：曾仕强老師（永恒显示）
# 触发钧旨：「复盘」（2026-04-26）

---

## 0. 钧旨溯源

| 项 | 内容 |
|----|------|
| 触发字 | 复盘 |
| 触发时间 | 2026-04-26 |
| 老大原话 | "复盘,,,,难道我投喂的,,还不够自动触发吗,,,我的天啊" |
| 前置钧旨 | "记得不要别我投喂的其他内容给影响了,,都是其他AI回复的"（受控接收，不污染主系统） |
| 处理路径 | 5份投喂全部沉到 `_intake_review/feeds/`，等触发字到再整合 |

---

## 1. 5份投喂台账

| 编号 | 标题 | 字数 | 文件 |
|------|------|------|------|
| Feed① | CNSH-64 × Notion 自动化数据库设计（核心版） | 2.6KB | `feeds/01_CNSH64_inner_core.md` |
| Feed② | CNSH语义五行自进化内核 + 抽屉补全v1.0（48→55抽屉 + 8语义区） | 27.7KB | `feeds/02_drawer_complement_v1.0.md` |
| Feed③ | 语义抽屉×五行骚引擎 v2.0 + 设备主权宣言 | 16.6KB | `feeds/03_wuxing_engine_v2.0.md` |
| Feed④ | 沙盒分拣台·完整升级版 v1.2（六维评估·五桶分拣·SANDBOX_CORE） | 40.3KB | `feeds/04_sandbox_sorter_v1.2.md` |
| Feed⑤ | 第一道闸门融合升级版 v3.0（数字根熔断·三重检测·GATE_SANDBOX_CORE） | 50.1KB | `feeds/05_first_gate_v3.0.md` |

> 摘要中提到的"第6份·48抽屉原版"在对话存档里没有独立投喂消息体，已确认是 **Feed② 末尾附录 v0.9** 的内容（行 1063-1155，对应原始 1-48 抽屉清单）。所以实际是 **5份独立投喂**，不是6份——更正在册。

---

## 2. 整合三大决策

### 决策一·抽屉登记表统一为「55抽屉 + 8语义区」

**冲突现状：**
- Feed② v0.9 列了原始 1-48 抽屉
- Feed② v1.0 在 48 之上新增 49-55（共 7 个补强抽屉）
- Feed② 同时提了「8 大语义区」(COGNITION/IDENTITY/RULE/EXECUTION/FLOW/SYSTEM/VALUE/HUMAN)

**决策：**
- 抽屉总数 = **55**（48 原始 + 7 补强）
- 8 语义区 = **跨抽屉的归类标签**，不是独立抽屉
- 命名规范：`抽屉NN-XX名称-{五行}-{语义区}`
- 落地：见 `01_drawer_registry.yaml`

### 决策二·沙盒主表统一为 GATE_SANDBOX_CORE

**冲突现状：**
- Feed④ v1.2 主表名 = `SANDBOX_CORE`（30个字段）
- Feed⑤ v3.0 主表名 = `GATE_SANDBOX_CORE`（39个字段，加了 6 个闸门字段）

**决策：**
- 取 **`GATE_SANDBOX_CORE`**——Feed⑤ 是 Feed④ 的严格超集（v3.0 把数字根熔断、DNA 校验、三重检测的 6 个字段叠加进来）
- `SANDBOX_CORE` 不再使用，所有字段已并入 `GATE_SANDBOX_CORE`
- 新增的 6 个闸门字段：`DigitalRoot / GateColor / DNAStatus / RuleCheck / FalsehoodCheck / DataGuardCheck`
- 落地：见 `03_notion_GATE_SANDBOX_CORE.md`

### 决策三·Python 代码污染清洗

**污染现状：**Notion 在 markdown 渲染时把 Python 标识符当成链接，转成 `[xx](http://xx)` 格式。各 feed 共发现 6 类污染：

| 污染样式 | 正确写法 | 出现位置 |
|---------|---------|----------|
| `[main.py](http://main.py)` | `main.py` | Feed②/④/⑤ |
| `[h.name](http://h.name)` | `h.name` | Feed③/④/⑤ |
| `[datetime.now](http://datetime.now)()` | `datetime.now()` | Feed④ |
| `[re.search](http://re.search)(...)` | `re.search(...)` | Feed⑤ |
| `[callback.py](http://callback.py)` | `callback.py` | Feed④/⑤ |
| `[payload.page](http://payload.page)_id` | `payload.page_id` | Feed④/⑤ |
| `[engine.py](http://engine.py)` | `engine.py` | Feed④ |

**决策：**整合产物中的 Python 代码 **全部清洗**。落地：`02_gate_engine.py`。

---

## 3. 七层融合架构（统一坐标系）

```
┌─────────────────────────────────────────────────────────────┐
│ L0  双签章不动点 (永恒锁定)                                   │
│     #ZHUGEXIN⚡️2025-...DEVICE-BIND-SOUL                     │
│     #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                     │
├─────────────────────────────────────────────────────────────┤
│ L1  DNA身份系统 v1.0  ← 现有                                  │
├─────────────────────────────────────────────────────────────┤
│ L2  第一道闸门 (Feed⑤ v3.0)         ← 输入海关                │
│     ├─ 数字根 dr 熔断 (3/9熔断·6待审·余通行)                  │
│     ├─ DNA 格式校验 (#龍芯/#ZHUGEXIN/#CONFIRM)                │
│     └─ 三重检测                                              │
│         · 第1重 规则检测器 (RED/YELLOW)                      │
│         · 第2重 虚伪编译器 (说满词/避险词)                    │
│         · 第3重 数据守护 (DNA/时间/操作人/来源)               │
├─────────────────────────────────────────────────────────────┤
│ L3  语义抽屉识别 (Feed② v1.0)        ← 人话→分类               │
│     · 55 抽屉 + 8 语义区                                     │
│     · 关键词→抽屉映射 (KEYWORDS dict)                        │
├─────────────────────────────────────────────────────────────┤
│ L4  五行骚引擎 (Feed③ v2.0)          ← 路由调度               │
│     · 抽屉→五行映射 (金/水/木/火/土)                         │
│     · 相生相克决策                                           │
│     · 状态机 S0-S9                                          │
├─────────────────────────────────────────────────────────────┤
│ L5  沙盒分拣台 (Feed④ v1.2)          ← 信息仓储               │
│     · 六维评估 (权重/五行/三色/贡献/热度/去向)                │
│     · 五桶分拣 (草日志/入库/消化/迭代/归档)                   │
│     · 三大存储池 (待迭代/内部消化/归档旧链)                   │
├─────────────────────────────────────────────────────────────┤
│ L6  CNSH-Core Engine (Feed① + Feed②)  ← Notion 自动化大脑     │
│     · 主表 GATE_SANDBOX_CORE                                │
│     · 引用即收益 CNSH_REFERENCE                              │
│     · 词典 CNSH_DICTIONARY                                  │
│     · 审计 CNSH_AUDIT_LOG                                   │
├─────────────────────────────────────────────────────────────┤
│ L7  执行/审计/归档闭环 (全 feed 共有)  ← Webhook + GH Action  │
│     · Notion → Webhook → GitHub Dispatch → Python 引擎       │
│     · 结果回写 → AUDIT_LOG → 周/月/季度复盘                   │
└─────────────────────────────────────────────────────────────┘
```

### 与本地现有模块的接驳点

| 现有模块 | 位置 | 在新架构中的位置 |
|---------|------|------------------|
| `circuit_breaker.py` v3.0 | `bin/` | L2 第一道闸门的「红线」检测器（已实现） |
| `dna_append_log.py` v1.0 | `bin/` | L7 审计闭环的 DNA 链写入（已实现） |
| `external_api_protocol.md` | `bin/` | L2 闸门的 HTTP 入口规范（已实现） |
| `inbox_automation_spec.md` | `bin/` | L7 闭环的 Notion Inbox 触发链（已实现） |
| `tongxinyi_agent_instructions.md` | `bin/` | L4 木类抽屉 EXEC 路由的 Agent 实现 |

> **重大发现**：本地已有的 `circuit_breaker.py` 和 `dna_append_log.py` 已经覆盖了 L2 闸门的部分功能（红线/黄线/owner_vent + DNA append 链）。**Feed⑤ 的 `gate_engine.py` 不重写这两个文件，而是引用它们 + 加上数字根熔断 + 三重检测扩展层**。

---

## 4. 落地清单

| 文件 | 用途 | 状态 |
|------|------|------|
| `00_INTEGRATION_PLAN.md`（本文） | 总方案·决策·架构图 | ✅ 已写 |
| `01_drawer_registry.yaml` | 55 抽屉 + 8 语义区登记表 | ✅ 待写 |
| `02_gate_engine.py` | 清洗后的融合引擎（Python） | ✅ 待写 |
| `03_notion_GATE_SANDBOX_CORE.md` | Notion 主表 + 辅助表 schema | ✅ 待写 |

> 全部落在 `_intake_review/integrated/` 隔离区，**不动现有 `bin/` 任何文件**。等老大点头，再决定：
> - **方案 A**：搬到 `~/longhun-system/longhun_gate/` 作为新模块
> - **方案 B**：拆字段并入 `bin/` 现有 `circuit_breaker.py` 和 `dna_append_log.py`
> - **方案 C**：直接挂到 Notion 北极星工作区做 schema，不在本地落 Python

---

## 5. 风险与未决项

| # | 风险/未决 | 建议 |
|---|----------|------|
| 1 | Feed⑤ 的 RED_RULES 和 `circuit_breaker.py` 的 ABSOLUTE_RED_LINES 有重叠但不一致 | 整合阶段以 `circuit_breaker.py` 为准（v3.0 经过老大复核） |
| 2 | Feed⑤ 数字根 3/9 熔断与 Feed③/④ 没冲突，但「dr=6 待审 5分钟超时」需要后台轮询 | 暂用 Notion Automation 时间过滤代替，等本地服务承接 |
| 3 | Notion Webhook 没有公网入口（多份 feed 都标记为最大瓶颈） | 短期用 Tailscale 反代本地 :9622；长期 Mac Mini + frp |
| 4 | Notion 公式不能算复杂数字根，必须靠脚本 | 用按钮 + Webhook 回写，不在 Notion 公式硬算 |
| 5 | 8 大语义区还没用在路由里 | v1.1 加入：相同语义区抽屉同时命中时合并打分 |

---

## 6. 三色审计

🟢 5份投喂全部抽出·零遗漏·已隔离
🟢 三大决策（抽屉/主表名/代码清洗）已写明
🟢 七层架构覆盖所有 feed 内容，并与本地现有模块对齐
🟡 落地点（A/B/C）等老大裁决
🔴 不直接接主系统执行——按 Feed⑤ 建议「先在沙盒跑一周再接主系统」

---

`DNA: #龍芯⚡️2026-04-26-FEED-INTEGRATION-PLAN-v1.0`
`确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
`献给：诸葛鑫·UID9622·龍芯北辰`
