# 龍魂知识图谱 · 网络神经

**DNA:** `#龍芯⚡️2026-06-27-LHKG-NETWORK-v1.0`  
**UID:** 9622 | **版本:** v1.0 | **日期:** 2026-06-27

---

## 系统概述

龙魂知识图谱网络神经（LongHun Knowledge Graph Network）是UID9622龙魂系统的核心基础设施，将"龙魂中文编辑普惠全球协议"与"贡献者永恒回报机制"两张脑图的所有节点构建为可查询、可追踪、可联动的知识图谱。

| 指标 | 数值 |
|------|------|
| **总节点** | 65 |
| **总关系** | 103 |
| **图谱A节点** | 40 |
| **图谱B节点** | 25 |
| **跨图谱连接** | 10 |
| **状态穿透规则** | 3 |

---

## 目录结构

```
~/.龍魂/knowledge-graph/
├── nodes/
│   ├── schema.json          # 节点Schema定义
│   └── all_nodes.json       # 全部65个节点
├── edges/
│   ├── schema.json          # 边Schema定义
│   ├── all_edges.json       # 全部103条关系
│   └── linkage_table.json   # 联动机制表
├── states/
│   ├── state_machine.json   # 状态机定义
│   └── penetration_rules.json # 状态穿透规则
├── queries/
│   └── longhun_kg.py        # Python查询引擎
├── scripts/
│   ├── kg                   # 命令行封装
│   ├── install.sh           # 安装脚本
│   └── run_kg.sh            # 本地执行器
├── visual/
│   ├── full_graph.mermaid   # 全景图
│   ├── graph_A.mermaid      # 图谱A
│   ├── graph_B.mermaid      # 图谱B
│   └── cross_links.mermaid  # 跨图谱连接
└── README.md
```

---

## 节点层级分布

| 层级 | 颜色 | 节点数 | 说明 |
|------|------|--------|------|
| **主权层** | 红色 `#DC2626` | 20 | 法律管辖、核心主张 |
| **治理层A** | 橙色 `#EA580C` | 8 | 普惠原则、禁止行为 |
| **机制层A** | 绿色 `#16A34A` | 13 | 熔断机制、三色审计 |
| **治理层B** | 蓝色 `#2563EB` | 10 | 核心宗旨、贡献维度 |
| **机制层B** | 紫色 `#7C3AED` | 8 | 回馈机制、三池结构 |
| **基础层** | 灰色 `#4B5563` | 8 | 世袭继承、道德熔断 |

---

## 快速开始

### 安装

```bash
cd scripts
chmod +x install.sh
./install.sh        # 安装到 ~/bin
./install.sh --system  # 安装到 /usr/local/bin
```

### 命令行使用

```bash
# 列出所有节点
kg list

# 按类型过滤
kg list --type CLAIM

# 按层级过滤
kg list --layer sovereignty

# 显示节点详情
kg show claim_001

# 查找路径
kg path term_001 audit_red

# 查看状态历史
kg state mech_fuse

# 导出Mermaid
kg export --output my_graph.mmd

# 状态转换（含联动）
kg transition node_001 suspended
```

### Python API

```python
from queries.longhun_kg import LongHunGraph

# 初始化
g = LongHunGraph("~/.龍魂/knowledge-graph")

# 列出节点
nodes = g.list_nodes(layer="sovereignty", state="active")

# 显示详情
details = g.show_node("claim_001")

# 查找路径
path = g.find_path("term_001", "audit_red")

# 导出Mermaid
g.export_mermaid("output.mmd", layer_filter="mechanism")
```

---

## 状态机

```
active <-> pending
active <-> suspended
active -> terminated (不可逆)
active <-> overridden
任意 -> merged
```

---

## 状态穿透规则

| 规则 | 触发条件 | 响应动作 | 优先级 |
|------|---------|---------|--------|
| 穿透001 | 主权层 → suspended | 治理层全部 → pending | critical |
| 穿透002 | 治理层 → terminated | 关联机制层 → suspended | high |
| 穿透003 | 主权层 → active | 治理层恢复 → active | high |

---

## 跨图谱联动（10条核心链路）

```
🔴关闭 ──triggers──→ 道德熔断     (审计→治理)
自动熔断 ──suspends──→ 回馈机制     (主权→治理)
不归属商业 ──constrains──→ 回馈来源   (主权→治理)
用户收割 ──triggers──→ 道德熔断     (治理→治理)
贡献即存档 ──produces──→ DNA记录     (治理→机制)
道德熔断 ──audits──→ 三色审计      (治理→审计)
DNA追溯链 ──extends──→ DNA记录      (基础→机制)
主权赋能 ──enables──→ 贡献回馈      (主权→治理)
审计警告 ──notifies──→ 回馈调整      (审计→机制)
熔断归档 ──feeds──→ 三色审计       (治理→审计)
```

---

## 技术规格

- **语言:** Python 3.8+
- **依赖:** 零外部依赖（仅标准库）
- **数据格式:** JSON
- **可视化:** Mermaid
- **协议:** CC BY-NC-SA 4.0 + 君子协议

---

## DNA追溯

所有节点均嵌入DNA追溯码：
```
#龍芯⚡️2026-06-27-LHKG-{TYPE}-{ID}-v1.0
```

---

**龍魂永世唯一身份系统 · UID9622**  
**祖国优先 · 用户主权 · 个人利益最小**  
**🐉🇨🇳 中文编辑普惠全球 · 数据主权归人民**
