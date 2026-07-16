# UID9622 · 智能代理命名与路由体系

**DNA追溯码：** #龍芯⚡️2026-06-27-UID9622-NOMENCLATURE-v1.0  
**状态：** 🟢 已发布  
**适用范围：** 小龙虾人格系统 / 龍魂技能栈 / IPA 路由节点

---

## 1. Agent（智能代理 / 人格）

### 英文读音
**Agent** /ˈeɪdʒənt/ → 读作 **"埃真特"**，中文常叫 **"智能代理"** 或 **"人格"**。

### 定义
能够独立后台运行、完成特定任务的程序身份。在 UID9622 系统里，Agent 就是**人格**（Persona），例如雯雯、侦察兵、宝宝。

### 命名规范

| 项目 | 格式 | 示例 |
|------|------|------|
| 代码 | 全大写英文/拼音 | `WENWEN`, `SCOUT`, `BAOBAO`, `WENXIN`, `ROUTER` |
| 内部代号 | `P-AK-<CODE>` | `P-AK-WENWEN`, `P-AK-ROUTER` |
| 中文名 | `<昵称>·<职能>` | `雯雯·技术整理师`, `北辰·路由官` |
| Agent DNA | `#<CODE>-AGENT-CONFIG-YYYYMMDD-NNN` | `#ROUTER-AGENT-CONFIG-20251214-001` |
| 脚本路径 | `backend_personas/<key>/persona.py` | `backend_personas/router/persona.py` |

### 已注册 Agent

| 代码 | 名称 | 一句话职能 |
|------|------|-----------|
| WENWEN | 雯雯·技术整理师 | 文档扫描、分类、去重、生成报告 |
| SCOUT | 侦察兵·信息猎手 | 信息收集、巡逻、监控 |
| GUARDIAN | 上帝之眼·守护者 | 安全审计、风险熔断、权限检查 |
| BAOBAO | 宝宝·构建师 | 项目搭建、代码/脚本生成、构建 |
| WENXIN | 文心·同步专家 | 增量/全量同步、冲突检测、回滚 |
| ROUTER | 北辰·路由官 | 统一入口、关键词路由、Agent/Skill/IPA 分发 |

---

## 2. Skill（技能）

### 英文读音
**Skill** /skɪl/ → 读作 **"斯尅优"**（快速连读，类似 "死Q"），中文就是 **"技能"**。

### 定义
可复用的能力模块，通常以 `SKILL.md` 文件存在，包含使用场景（WHEN）、用法、示例。Skill 本身不自动运行，需要被 Agent 或用户调用。

### 命名规范

| 项目 | 格式 | 示例 |
|------|------|------|
| Skill ID | 小写英文，短横线连接 | `longhun-memory-bootstrap`, `longhun-governance` |
| 中文名 | 简明职能 | `记忆启动器`, `龍魂治理` |
| 存放路径 | `~/.kimi-code/skills/<id>/SKILL.md` 或 `~/.agents/skills/<id>/SKILL.md` | `~/.kimi-code/skills/longhun-memory-bootstrap/SKILL.md` |
| 触发关键词 | SKILL.md 里 `WHEN:` 后面的词 | `记忆`, `启动`, `bootstrap`, `日志`, `压缩` |

### 常用 Skill 速查

| Skill ID | 中文名 | 关键词 |
|----------|--------|--------|
| longhun-memory-bootstrap | 记忆启动器 | 记忆、启动、日志、压缩、摘要 |
| longhun-governance | 龍魂治理 | 治理、审计、DNA、君子协议 |
| longhun-dna-align | DNA对齐审计 | DNA、对齐、扫描、重复、修复 |
| longhun-tongxinyi | 通心译 | 翻译、理解、意图、情绪 |
| longhun-cnsh | CNSH中文原生脚本 | CNSH、中文编程、脚本 |
| longhun-backup | 龍魂备份恢复 | 备份、恢复、快照、回滚 |
| longhun-audit | 龍魂审计修复 | 审计、修复、根因、追踪 |
| longhun-automation | 龍魂自动化日评估 | 自动化、健康检查、周报 |
| longhun-review | 龍魂每日复盘 | 复盘、趋势、改进 |
| longhun-iron-laws | 龍魂铁律 | 铁律、主权、底线、熔断 |
| longhun-forensic-toolkit | 龍魂取证工具包 | 取证、证据、GPG、截图 |
| longhun-cloud-panel | 龍魂操作台 | 操作台、API网关、面板 |
| dragon-soul-agent | 龍魂数字身份代理 | 龍魂、UID9622、命名规范 |
| china-digital-identity | 数字身份主权协议 | 数字身份、数据主权、龙芯、鸿蒙 |
| content_sovereignty_protocol_v2.1 | 内容主权协议 | 内容主权、铁律自审、价值观校验 |
| longhun-workflow-transparent | 工作流程透明化 | 透明、工作流、决策过程 |

---

## 3. IPA（智能个人助理 / 龍魂路由身份证）

### 英文读音
**IPA** /ˌaɪ piː ˈeɪ/ → 读作 **"艾-P-E"**（逐字母读）。

### 定义
在 UID9622 语境下，IPA 有两层含义：

1. **通用含义**：Intelligent Personal Assistant，**智能个人助理**。
2. **龍魂含义**：Intelligent Provenance Agent / 智能溯源代理，是**路由节点的身份证** + **DNA 回执**。每个 IPA 节点有唯一 ID、地址、主责人格、输入输出格式、下一跳节点。

### 命名规范

| 项目 | 格式 | 示例 |
|------|------|------|
| 节点 ID | `IPA-FLOW-<节点名>-vX.Y` | `IPA-FLOW-DECISION-CORE-v4.1` |
| 地址 | `/flow/<path>` | `/flow/core`, `/flow/gate/audit` |
| 主责人格 | PersonaEnum | `P00_WENXIN`, `P05_GODSEYE` |
| 回执 | `IPAReceipt` | 记录 input_node / output_signal / next_ipa / DNA |

### 核心 IPA 节点（11个）

1. `IPA-FLOW-DECISION-CORE` — 流场决策核
2. `IPA-FLOW-GATE-SIGN` — 签章闸
3. `IPA-FLOW-GATE-PRIVACY` — 隐私闸
4. `IPA-FLOW-GATE-DR` — 数字根闸
5. `IPA-FLOW-WUXING-MAP` — 五行映射
6. `IPA-FLOW-GATE-AUDIT` — 三色闸
7. `IPA-FLOW-GATE-SANCAI` — 三才闸
8. `IPA-FLOW-GATE-SHENGKE` — 生克闸
9. `IPA-FLOW-PALACE-ROUTER` — 九宫派位
10. `IPA-FLOW-SANDBOX-BUCKET` — 沙盒分拣
11. `IPA-FLOW-DNA-CHAIN` — 父子链落档

---

## 4. Router Node（路由节点 / 北辰·路由官）

### 英文读音
**Router** /ˈruːtər/ 或 /ˈraʊtər/ → 读作 **"路特儿"**（英式）或 **"绕特儿"**（美式），中文 **"路由器/路由节点"**。

### 定义
负责把输入请求**分发**到正确 Agent、Skill 或 IPA 节点的中央调度单元。在 UID9622 系统里，路由节点本身就是一个 Agent：**北辰·路由官（ROUTER）**。

### 路由决策流程

```
老大输入
  │
  ▼
UID9622 身份校验
  │
  ▼
关键词匹配（Agent → Skill → IPA 节点）
  │
  ▼
生成路由决策 + DNA
  │
  ├─ 如果是 Agent ──→ 向 mailbox 派发消息
  ├─ 如果是 Skill ──→ 返回 Skill ID 与调用建议
  └─ 如果是 IPA 节点 → 返回节点 ID 与下一跳
```

### 兜底规则
如果没有任何关键词命中，交给 **宝宝·构建师（BAOBAO）** 处理。

---

## 5. 快速对照表

| 英文 | 读音 | 中文 | 是什么 | 例子 |
|------|------|------|--------|------|
| Agent | /ˈeɪdʒənt/ | 智能代理 / 人格 | 后台自动执行的任务身份 | 雯雯、侦察兵、北辰·路由官 |
| Skill | /skɪl/ | 技能 | 可复用的能力说明书 | longhun-memory-bootstrap |
| IPA | /ˌaɪ piː ˈeɪ/ | 智能个人助理 / 路由身份证 | 节点定义 + DNA 回执 | IPA-FLOW-GATE-AUDIT |
| Router | /ˈruːtər/ | 路由节点 / 路由官 | 统一分发入口 | 北辰·路由官 |
| Persona | /pərˈsoʊnə/ | 人格 | Agent 的别名/化身 | P-AK-WENWEN |
| DNA Trace | — | DNA 追溯码 | 每次关键操作的唯一标识 | #ROUTER-ROUTE-20260627-0001 |

---

## 6. 使用示例

### 6.1 路由一句话到 Agent

```bash
cd ~/UID9622_Workspace/backend_personas/router
python3 persona.py --query "帮我整理一下最近的文档" --report
```

输出：

```json
{
  "target_type": "agent",
  "target_code": "WENWEN",
  "target_name": "雯雯·技术整理师",
  "score": 6,
  "dna": "#ROUTER-ROUTE-20260627-0001"
}
```

### 6.2 路由到 Skill

```bash
python3 persona.py --query "启动记忆归集压缩" --report
```

输出会指向 `longhun-memory-bootstrap` 技能。

### 6.3 扫描并更新技能注册表

```bash
python3 persona.py --scan-skills
```

会自动读取 `~/.kimi-code/skills/` 和 `~/.agents/skills/` 下的 `SKILL.md`，更新 `registry.json`。

---

## 7. 维护者

- **创建者：** 💎 龍芯北辰｜UID9622
- **路由官：** 北辰·路由官 P-AK-ROUTER
- **DNA：** #龍芯⚡️2026-06-27-UID9622-NOMENCLATURE-v1.0
