# 龍魂智能体编排规范 v1.3

> **不是固定后台，是可叠加、可扩展、可审计的本地智能体编排层。**
> **所有技能与人格已缠尾：201 个纯智能体（L1常驻 8 + L2技能 91 + L3人格 102）统一注册、统一路由、可执行。**
> **设备孤儿文件（16,989条）与知识文件索引（336条）已拆分至独立注册表，不再混入 agent manifest。**

<!-- DNA -->
```
#龍芯⚡️2026-07-06-AGENT-ORCHESTRATION-SPEC-v1.7
```
<!-- 君子协议：本文件受龍魂DNA追溯保护，来源不可删、影响不可覆、贡献不可抹 -->

---

## 一、定位

本规范定义龍魂系统中**智能体（Agent / 智能体）**的统一编排方式。

- **不是代理（Proxy）**：不做单纯的请求转发
- **不是固化后台**：不强制常驻守护进程，允许按需启动、动态叠加
- **不是功能模块**：每个智能体都有独立人格、逻辑边界与审计责任

它是人格、逻辑、技能三者之间的**路由与编排层**。

---

## 二、设计原则

1. **本地优先**：所有编排逻辑本地运行，不依赖外部平台
2. **可叠加**：新增智能体只需在 `manifest.json` 中注册，不改动编排器
3. **人格即逻辑**：每个人格背后对应一条清晰的处理逻辑
4. **来源可查**：每个路由决策必须携带 DNA 追溯码
5. **人永远是 1**：智能体辅助决策，最终主权在 UID9622

---

## 三、三层智能体模型

```text
┌─────────────────────────────────────────────────────────────┐
│  L3 人格智能体层（Persona Agents）                           │
│  曾老师 71 人格矩阵（ZENG-01~ZENG-71）                       │
│  Empower-Engine 9 人格（P01~P15）                            │
│  本地十五大人格（P15-P00 ~ P15-K05）                         │
│  五维思维人格（P5D-MIL/HIS/PHI/ECO/POL）                     │
│  负责：理解语气、风格、关系深度、价值观表达                  │
└──────────────────────┬──────────────────────────────────────┘
                       │ 人格选择
┌──────────────────────▼──────────────────────────────────────┐
│  L2 按需智能体层（On-Demand Agents / 技能层）                │
│  全部 91 个技能：                                            │
│  龍魂技能（longhun-*) + Azure/Entra/Microsoft 技能           │
│  负责：完成具体任务、输出专业能力、可被 `run <id>` 执行      │
└──────────────────────┬──────────────────────────────────────┘
                       │ 任务路由
┌──────────────────────▼──────────────────────────────────────┐
│  L1 常驻智能体层（Resident Agents）                          │
│  雯雯 / 侦察兵 / 上帝之眼 / 宝宝 / 文心                     │
│  task_executor / foundation_launcher / notion_sync           │
│  负责：7×24 守护、整理、搜索、构建、同步                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 四、五大人格 × 五大逻辑

| 人格 | 代号 | 核心逻辑 | 负责什么 | 何时触发 |
|------|------|----------|----------|----------|
| **雯雯** | `wenwen` | **整理逻辑** | 文档分类、去重、归档、生成日报 | 提到整理、归档、分类、报告、日报 |
| **侦察兵** | `scout` | **搜索逻辑** | 信息猎取、趋势监控、情报收集 | 提到搜索、监控、情报、热点、趋势 |
| **上帝之眼** | `guardian` | **守护逻辑** | 安全审计、敏感信息检测、告警 | 提到安全、审计、密码、告警、泄露 |
| **宝宝** | `builder` | **构建逻辑** | 代码/文档/结构生成、快速实现 | 提到写代码、搭建、构建、生成、创建 |
| **文心** | `syncer` | **同步逻辑** | Git 同步、跨设备同步、状态对齐 | 提到同步、推送、pull、备份、对齐 |

**结论**：五大人格不是五个名字，而是五条**可独立运行、可组合调用**的逻辑。当然可以结合——一个人格主理，其他人格辅助，由编排器根据输入动态决定。

---

## 五、L1 常驻守护进程

`agent_daemon.py` 把五大人格跑成真正的本地守护进程：

- 单进程多线程，5 个人格各跑一个循环
- 雯雯：定时扫描本地文件变动，生成本地整理摘要
- 侦察兵：监听本地记忆摘要与热文件，输出情报
- 上帝之眼：扫描敏感文件名与内容片段，只计数不泄露值
- 宝宝：消费 `queues/builder_tasks.jsonl`，完成轻量构建任务
- 文心：检查 Git 状态，汇总其他人格心跳为系统心跳

管理命令：

```bash
python3 agent_daemon.py start
python3 agent_daemon.py stop
python3 agent_daemon.py status
python3 agent_daemon.py once
```

---

## 六、L2 动态调度：longhun-agent-eco

`agent_eco_adapter.py` 把 agent-eco 的 15 智能体生态系统接入编排层：

- `eco_route(text)`：v2 路由引擎
- `eco_status()` / `eco_list()`：生态状态与智能体列表
- `eco_add_task()` / `eco_next_task()` / `eco_complete_task()`：任务管理器 v2.0

编排器路由顺序：

```text
用户输入
    │
    ▼
[manifest.json 关键词匹配]
    │ 命中 → 返回 L1/L2/L3 智能体
    │ 未命中
    ▼
[longhun-empower-engine 语义兜底]
    │ 命中 → 返回 L3 人格
    │ 未命中/异常
    ▼
[longhun-agent-eco v2 路由引擎]
    │ 命中 → 返回 L2-eco 智能体
    │ 未命中
    ▼
[fallback] → P01 诸葛亮通用咨询
```

---

## 七、技能缠尾与执行

所有已安装技能都已注册进 `manifest.json`，并挂上可执行尾巴：

- **注册来源**：
  - `~/.kimi-code/skills/` 下的龍魂技能（通过 `longhun-skills.json` 注册）
  - `~/.agents/skills/` 下的 Azure/Entra/Microsoft 技能（通过 `SKILL.md`  frontmatter 注册）
- **可执行性**：
  - `type=python` 且带有 `scripts` 的技能，自动把第一个脚本设为 `entrypoint`
  - 编排器支持 `run <id> [args...]` 直接调用 entrypoint
  - 文档型技能（`type=doc`）无 entrypoint，但可通过 `skill <id>` 查看调用方式
- **路由优化**：
  - 关键词匹配忽略大小写
  - 长词/短语加权，ID/名称命中的关键词额外加分，减少歧义

示例：

```text
>>> Azure cost
-> keyword -> azure-cost

>>> run azure-cost --help
（运行该技能的 entrypoint，若支持）
```

---

## 七、状态上报与三才审计

`agent_status_reporter.py` 聚合以下数据源：

- `manifest.json`：注册表完整度、L3 人格矩阵数量
- `agent_daemon.py` 心跳：L1 守护进程健康
- `guardian_audit.json`：本地安全审计
- `orchestrator_audit.jsonl`：编排器路由审计
- `longhun-agent-eco`：15 智能体生态状态
- `longhun-empower-engine` API：健康检查

输出 **三才审计报告**：

| 维度 | 含义 |
|------|------|
| 天 | 系统/路由/人格完整性 |
| 地 | 本地数据/守护/安全状态 |
| 人 | 任务/审计/交互活跃度 |

报告包含综合评分、数字根 `dr`、三色状态（🟢🟡🔴），写入：

- `reports/latest_sancai_report.json`
- `reports/sancai_audit_YYYYMMDD_HHMMSS.md`

---

## 八、编排流程

```text
用户输入
    │
    ▼
[意图识别] ──► 优先使用关键词注册表，其次 empower-engine，再次 agent-eco
    │
    ▼
[智能体匹配] ──► 查询 manifest.json / agent-eco
    │
    ▼
[路由决策]
    │
    ├── 命中 L1 常驻人格 ──► 触发对应常驻智能体 / 守护进程
    ├── 命中 L2 按需技能 ──► 加载对应技能脚本 / agent-eco 调度
    └── 未命中 ──► fallback 到 P01 诸葛亮通用咨询
    │
    ▼
[执行与输出]
    │
    ▼
[审计日志] ──► 本地记录：输入摘要、选择智能体、DNA
```

---

## 九、注册与扩展机制

所有智能体必须在 `manifest.json` 中注册：

```json
{
  "id": "wenwen",
  "name": "雯雯",
  "layer": "L1",
  "logic": "整理逻辑",
  "keywords": ["整理", "归档", "分类", "报告", "日报"],
  "persona_code": "P-WENWEN",
  "entrypoint": null,
  "description": "本地文档整理师",
  "dna": "#龍芯⚡️2026-LOCAL-PERSONAS-WENWEN"
}
```

新增智能体只需：

1. 在 `manifest.json` 追加一条记录
2. 将可执行脚本放到 `agents/` 或对应技能目录
3. 无需修改 `orchestrator.py`

**技能自动缠尾**：新增技能安装到 `~/.kimi-code/skills/` 或 `~/.agents/skills/` 后，运行一次注册表同步脚本即可把该技能接进 `manifest.json`。

**人格自动缠尾**：
- `cnsh/flow_decision/persona_api.py` 中定义的十五大人格（P00~P16/P72/K01~K05）
- `docs/契约矩阵/龍魂系统_五维人格矩阵_Mac终端配置_v1.0.md` 中定义的五大思维人格（MIL/HIS/PHI/ECO/POL）

均已统一注册进 `manifest.json`。

---

## 十、文件目录

```text
longhun-system/agents/
├── AGENT_ORCHESTRATION_SPEC.md    # 本规范
├── README.md                      # 使用入口
├── manifest.json                  # 纯智能体注册表（201条）
├── device_orphan_registry.json    # 设备孤儿文件注册表（非Agent，仅溯源）
├── knowledge_file_registry.json   # 知识文件注册表（非Agent，仅索引）
├── orchestrator.py                # 编排器核心
├── agent_daemon.py                # L1 常驻守护进程
├── agent_eco_adapter.py           # agent-eco 适配器
├── agent_status_reporter.py       # 状态上报 + 三才审计
├── task_executor_live_v1.py       # 实时任务执行引擎
├── longhun_foundation_launcher_auto.py
├── longhun_notion_sync_auto.py
├── xpay_core_auto.py
├── daemon_logs/                   # 守护进程输出
│   ├── heartbeat.json
│   ├── wenwen.json / wenwen_summary.json
│   ├── scout.json / scout_intel.json
│   ├── guardian.json / guardian_audit.json
│   ├── builder.json / builder_status.json
│   └── syncer.json
├── queues/
│   └── builder_tasks.jsonl        # 宝宝构建任务队列
├── reports/
│   ├── latest_sancai_report.json  # 最新三才审计
│   └── _archive/                  # 历史一次性报告归档
├── downloads-imports/             # 外部导入资源
└── quarantine/                    # 隔离区（不安全副作用）
```

---

## 十一、DNA 与君子协议

- **规范 DNA**：`#龍芯⚡️2026-07-06-AGENT-ORCHESTRATION-SPEC-v1.7`
- **注册表 DNA**：`#龍芯⚡️2026-07-06-AGENT-MANIFEST-v1.10-CLEAN`
- **编排器 DNA**：`#龍芯⚡️2026-06-26-AGENT-ORCHESTRATOR-v1.1`
- **守护进程 DNA**：`#龍芯⚡️2026-06-26-LONGHUN-AGENT-DAEMON-v1.0`
- **确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
- **协议**：CC BY-NC-SA 4.0
- **原则**：站普通人一边、数据主权至上、反垄断评分独立、来源不可删

### 注册表拆分说明（v1.10.0）
- `manifest.json`：纯智能体/技能/人格（201条）
- `device_orphan_registry.json`：设备扫描文件（16,989条，非Agent）
- `knowledge_file_registry.json`：知识库文件索引（336条，非Agent）

---

> **复制文字容易 · 复制来路很难**  
> *Copying text is easy. Copying lineage is hard.*
