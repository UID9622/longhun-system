# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂智能体编排层

> **不是固化后台，是可叠加、可扩展、可审计的本地智能体编排系统。**

---

## 快速开始

```bash
cd /Users/zuimeidedeyihan/longhun-system/agents

# 交互式路由测试
python3 orchestrator.py

# 一次性查看三才审计报告
python3 agent_status_reporter.py

# L1 守护进程管理
python3 agent_daemon.py start      # 启动
python3 agent_daemon.py stop       # 停止
python3 agent_daemon.py status     # 状态
python3 agent_daemon.py once       # 手动跑一轮（调试用）
```

---

## 核心文件

| 文件 | 作用 |
|---|---|
| `AGENT_ORCHESTRATION_SPEC.md` | 正式架构规范：三层模型、五大人格×五大逻辑、扩展机制 |
| `manifest.json` | **纯智能体注册表**（201条：L1常驻8 + L2技能91 + L3人格102） |
| `device_orphan_registry.json` | 设备孤儿文件注册表（16,989条，非Agent，仅设备溯源） |
| `knowledge_file_registry.json` | 知识文件注册表（336条，非Agent，仅知识库索引） |
| `orchestrator.py` | 编排器核心：读取注册表、关键词匹配、语义兜底、写审计日志 |
| `agent_daemon.py` | L1 常驻五大人格守护进程（雯雯/侦察兵/上帝之眼/宝宝/文心） |
| `agent_eco_adapter.py` | `longhun-agent-eco` 动态调度适配器 |
| `agent_status_reporter.py` | 智能体状态上报 + 三才审计报告生成 |
| `task_executor_live_v1.py` | 实时任务执行智能体 |
| `longhun_foundation_launcher_auto.py` | 基础服务启动智能体 |
| `longhun_notion_sync_auto.py` | Notion 同步智能体 |
| `xpay_core_auto.py` | 支付核心智能体 |

---

## 三层模型（已缠尾）

```text
L3 人格智能体  ──►  曾老师 71 人格矩阵（ZENG-01~ZENG-71）
                   + Empower-Engine 9 人格（P01~P15）
                   + 本地十五大人格（P15-P00 ~ P15-K05）
                   + 五维思维人格（P5D-MIL/HIS/PHI/ECO/POL）
                   + 共 102 人格
L2 按需智能体  ──►  全部 91 个技能（龍魂技能 + Azure/Entra/Microsoft 技能）
L1 常驻智能体  ──►  雯雯 / 侦察兵 / 上帝之眼 / 宝宝 / 文心
                   / task_executor / foundation_launcher / notion_sync
                   + 共 8 常驻
```

> **缠尾**：所有 `.kimi-code/skills/` 与 `.agents/skills/` 下的技能、以及 `cnsh/flow_decision/persona_api.py` 中的十五大人格，都已注册进 `manifest.json`，不再是死文档。

---

## 五大人格 × 五大逻辑

| 人格 | 逻辑 | 触发场景 |
|---|---|---|
| 雯雯 | 整理逻辑 | 归档、分类、去重、日报 |
| 侦察兵 | 搜索逻辑 | 搜索、监控、情报、趋势 |
| 上帝之眼 | 守护逻辑 | 安全、审计、敏感信息、告警 |
| 宝宝 | 构建逻辑 | 写代码、搭建、生成、创建 |
| 文心 | 同步逻辑 | 同步、Git、备份、对齐 |

五大人格本身就是五条逻辑，可以组合调用：主理 + 辅助。

---

## 编排器交互命令

进入 `python3 orchestrator.py` 后可输入：

| 命令 | 说明 |
|---|---|
| `list` | 列出全部 201 个已注册智能体 |
| `skill <id>` | 查看某个技能/智能体的详情与调用方式 |
| `run <id> [args...]` | 直接运行技能的 entrypoint 脚本 |
| `daemon-status` | 查看 L1 守护进程状态 |
| `start-daemon` / `stop-daemon` | 启动/停止守护进程 |
| `report` | 生成三才审计报告 |
| `eco-status` | 查看 agent-eco 15 智能体生态状态 |
| `eco-route <文本>` | 用 agent-eco v2 路由引擎单独路由 |
| `q` | 退出 |

示例：

```
>>> Azure cost
>>> skill azure-cost
>>> run longhun-agent-eco report
>>> 数字身份
>>> report
```

---

## 如何新增智能体

1. 编辑 `manifest.json`，追加一条记录
2. 将脚本/技能放到 `agents/` 或对应技能目录
3. 不需要修改 `orchestrator.py`

示例：

```json
{
  "id": "my-agent",
  "name": "我的智能体",
  "layer": "L2",
  "type": "on-demand",
  "logic": "某逻辑",
  "keywords": ["关键词1", "关键词2"],
  "persona_code": "P-MY",
  "entrypoint": "my_agent.py",
  "description": "...",
  "dna": "#龍芯⚡️..."
}
```

---

## 设计原则

- **本地优先**：不依赖外部平台
- **可叠加**：持续迭代，新智能体即插即用
- **人格即逻辑**：每个人格对应清晰处理逻辑
- **来源可查**：每次路由都带 DNA 追溯码
- **人永远是 1**：最终决策权在 UID9622

---

## DNA

- **编排器 DNA**：`#龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-AGENT-ORCHESTRATOR-v1.1`
- **注册表 DNA**：`#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-AGENT-MANIFEST-v1.10-CLEAN`
- **规范 DNA**：`#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-AGENT-ORCHESTRATION-SPEC-v1.7`
- **守护进程 DNA**：`#龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-LONGHUN-AGENT-DAEMON-v1.0`
- **eco 适配器 DNA**：`#龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-LONGHUN-AGENT-ECO-ADAPTER-v1.0`
- **状态报告 DNA**：`#龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-LONGHUN-AGENT-STATUS-REPORTER-v1.0`
