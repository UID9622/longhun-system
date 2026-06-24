# 龍魂CNSH体系 | LongHun CNSH System

```
DNA: #龍芯⚡️2026-06-18-CNSH-ROOT-CARD-v2.0
```

> 🟢 **君子协议** | **JunZi Protocol**: CC BY-NC-SA 4.0
> 🟡 **AI Truth Protocol**: All outputs must be verifiable and traceable
> 🔴 **DNA Trace**: Every change is tracked and auditable

---

## 一、龍魂体系简介 | Introduction

**龍魂CNSH**（Chinese Namespace Hierarchy）是一套面向AI系统的标准化中文编程目录结构体系。它以「龍」为精神图腾，以「魂」为架构灵魂，旨在构建一个人人可理解、可审计、可追溯的AI系统开发框架。

**核心理念**: 
- **中文编程** — 使用中文变量名、函数名、类名，降低理解门槛
- **繁体龍字** — 「龍」字永存，传承中华文化基因
- **三色审计** — 🟢🟡🔴 三级标记系统，一目了然的质量控制
- **DNA追溯** — 每个文件都有唯一的DNA标识，变更链完整可追溯
- **通心译** — 双语注释确保全球开发者无障碍协作

---

## 二、目录结构总览 | Directory Structure

```
/mnt/agents/output/CNSH/
├── runtime/              # 运行时引擎 - Runtime Engine
│   ├── __init__.py
│   ├── 启动器.py          # 统一入口 | Unified Entry Point
│   └── 配置管理器.py       # 配置管理 | Configuration Manager
├── governance/           # 治理层 - Governance Layer
│   ├── __init__.py
│   ├── 三层监督器.py       # Three-Layer Supervisor
│   ├── 三色审计器.py       # Tri-Color Auditor (🟢🟡🔴)
│   └── DNA追溯器.py        # DNA Tracer
├── router/               # 模块路由器 - Module Router
│   ├── __init__.py
│   └── 龍魂路由器.py       # LongHun Router
├── eventbus/             # 事件总线 - Event Bus
│   ├── __init__.py
│   └── 事件总线.py         # Event Bus
├── hooks/                # 生命周期钩子 - Lifecycle Hooks
│   ├── __init__.py
│   └── 钩子管理器.py        # Hook Manager
├── audit/                # 审计日志 - Audit Logs
│   ├── __init__.py
│   └── 审计记录器.py        # Audit Logger
├── snapshots/            # 状态快照 - State Snapshots
│   ├── __init__.py
│   └── 快照管理器.py        # Snapshot Manager
├── reactor/              # 反应器核心 - Reactor Core
│   ├── __init__.py
│   ├── 图像识别引擎.py      # LongTong OCR Engine (龍瞳)
│   ├── 文字识别引擎.py      # LongWen NLP Engine (龍文)
│   ├── 语音识别引擎.py      # LongYin ASR Engine (龍音)
│   └── 金融交易引擎.py      # Web3-DNA Trading Engine
├── memory/               # 记忆系统 - Memory System
│   ├── __init__.py
│   └── 记忆管理器.py        # Memory Manager
├── sandbox/              # 沙箱执行 - Sandbox Execution
│   ├── __init__.py
│   └── 沙箱执行器.py        # Sandbox Executor
├── protocols/            # 协议层 - Protocol Layer
│   ├── __init__.py
│   ├── 君子协议.py         # JunZi Protocol (CC BY-NC-SA 4.0)
│   ├── AI真相协议.py       # AI Truth Protocol
│   └── 通心译协议.py       # TongXinYi Protocol
├── adapters/             # 适配器 - Adapters
│   ├── __init__.py
│   └── 接口适配器.py        # Interface Adapter
├── prompts/              # 提示词模板 - Prompt Templates
│   ├── __init__.py
│   └── 系统提示词.py        # System Prompts
├── agents/               # 智能体配置 - Agent Configuration
│   ├── __init__.py
│   └── 代理配置器.py        # Agent Configurator
├── notion/               # Notion集成 - Notion Integration
│   ├── __init__.py
│   └── Notion连接器.py      # Notion Connector
├── logs/                 # 日志存储 (空目录) - Log Storage
├── scripts/              # 脚本库 - Script Library
│   └── 占位脚本.py
├── database/             # 本地数据库 - Local Database
│   ├── __init__.py
│   └── 龍魂数据库.py        # LongHun Database
├── xcode/                # Xcode项目 (空目录) - Xcode Projects
└── ROOT_CARD.md          # 根卡片索引 (本文档)
```

---

## 三、快速开始指南 | Quick Start

### 3.1 启动系统

```python
# 导入启动器
from runtime.启动器 import 系统启动器

# 创建启动器实例
启动器 = 系统启动器()

# 加载配置
启动器.加载配置("./config.json")

# 启动系统
启动器.启动()

# 优雅关闭
启动器.优雅关闭()
```

### 3.2 使用三色审计

```python
from governance.三色审计器 import 三色审计器

审计器 = 三色审计器()
审计器.绿记录("runtime", "系统启动正常")
审计器.黄记录("governance", "配置项使用默认值")
审计器.红记录("reactor", "引擎初始化超时")
print(审计器.获取统计())
```

### 3.3 DNA追溯

```python
from governance.DNA追溯器 import DNA追溯器

追溯器 = DNA追溯器()
根 = 追溯器.创建根节点("CNSH", "governance", "v1.0")
子 = 追溯器.创建子节点(根.dna字符串, "CNSH", "runtime", "v1.1", "添加启动器")
血缘 = 追溯器.追溯血缘(子.dna字符串)
```

### 3.4 三层监督

```python
from governance.三层监督器 import 三层监督器

监督器 = 三层监督器()
结果 = 监督器.全流程监督("输入数据", 处理函数)
```

---

## 四、DNA追溯链 | DNA Trace Chain

| 代际 | DNA标识 | 模块 | 版本 | 描述 |
|------|---------|------|------|------|
| 第0代 | `#龍芯⚡️2026-06-18-CNSH-ROOT-v1.0` | ROOT | v1.0 | 初始根节点 |
| 第1代 | `#龍芯⚡️2026-06-18-CNSH-DIR-STRUCTURE-v2.0` | DIR-STRUCTURE | v2.0 | 目录结构v2 |
| 第2代 | `#龍芯⚡️2026-06-18-CNSH-runtime-v1.0` | runtime | v1.0 | 运行时引擎 |
| 第2代 | `#龍芯⚡️2026-06-18-CNSH-governance-v1.0` | governance | v1.0 | 治理层 |
| 第2代 | `#龍芯⚡️2026-06-18-CNSH-router-v1.0` | router | v1.0 | 路由器 |
| 第2代 | `#龍芯⚡️2026-06-18-CNSH-eventbus-v1.0` | eventbus | v1.0 | 事件总线 |
| 第2代 | `#龍芯⚡️2026-06-18-CNSH-hooks-v1.0` | hooks | v1.0 | 钩子管理 |
| 第2代 | `#龍芯⚡️2026-06-18-CNSH-audit-v1.0` | audit | v1.0 | 审计日志 |
| 第2代 | `#龍芯⚡️2026-06-18-CNSH-snapshots-v1.0` | snapshots | v1.0 | 状态快照 |
| 第2代 | `#龍芯⚡️2026-06-18-CNSH-reactor-v1.0` | reactor | v1.0 | 反应器核心 |
| 第2代 | `#龍芯⚡️2026-06-18-CNSH-memory-v1.0` | memory | v1.0 | 记忆系统 |
| 第2代 | `#龍芯⚡️2026-06-18-CNSH-sandbox-v1.0` | sandbox | v1.0 | 沙箱执行 |
| 第2代 | `#龍芯⚡️2026-06-18-CNSH-protocols-v1.0` | protocols | v1.0 | 协议层 |
| 第2代 | `#龍芯⚡️2026-06-18-CNSH-adapters-v1.0` | adapters | v1.0 | 适配器 |
| 第2代 | `#龍芯⚡️2026-06-18-CNSH-prompts-v1.0` | prompts | v1.0 | 提示词模板 |
| 第2代 | `#龍芯⚡️2026-06-18-CNSH-agents-v1.0` | agents | v1.0 | 智能体配置 |
| 第2代 | `#龍芯⚡️2026-06-18-CNSH-notion-v1.0` | notion | v1.0 | Notion集成 |
| 第2代 | `#龍芯⚡️2026-06-18-CNSH-database-v1.0` | database | v1.0 | 本地数据库 |

---

## 五、模块索引表 | Module Index

### 核心模块 (Core Modules)

| 目录 | 文件 | 中文名 | 英文名 | 状态 |
|------|------|--------|--------|------|
| `runtime/` | `启动器.py` | 统一启动器 | Unified Launcher | 🟢 就绪 |
| `runtime/` | `配置管理器.py` | 配置管理器 | Config Manager | 🟢 就绪 |
| `governance/` | `三层监督器.py` | 三层监督器 | 3-Layer Supervisor | 🟢 就绪 |
| `governance/` | `三色审计器.py` | 三色审计器 | Tri-Color Auditor | 🟢 就绪 |
| `governance/` | `DNA追溯器.py` | DNA追溯器 | DNA Tracer | 🟢 就绪 |

### 通信模块 (Communication)

| 目录 | 文件 | 中文名 | 英文名 | 状态 |
|------|------|--------|--------|------|
| `router/` | `龍魂路由器.py` | 龍魂路由器 | LongHun Router | 🟢 就绪 |
| `eventbus/` | `事件总线.py` | 事件总线 | Event Bus | 🟢 就绪 |
| `hooks/` | `钩子管理器.py` | 钩子管理器 | Hook Manager | 🟢 就绪 |

### 数据模块 (Data)

| 目录 | 文件 | 中文名 | 英文名 | 状态 |
|------|------|--------|--------|------|
| `audit/` | `审计记录器.py` | 审计记录器 | Audit Logger | 🟢 就绪 |
| `snapshots/` | `快照管理器.py` | 快照管理器 | Snapshot Manager | 🟢 就绪 |
| `memory/` | `记忆管理器.py` | 记忆管理器 | Memory Manager | 🟢 就绪 |
| `database/` | `龍魂数据库.py` | 龍魂数据库 | LongHun Database | 🟢 就绪 |

### 引擎模块 (Engines)

| 目录 | 文件 | 中文名 | 英文名 | 状态 |
|------|------|--------|--------|------|
| `reactor/` | `图像识别引擎.py` | 龍瞳OCR引擎 | LongTong OCR | 🟡 占位 |
| `reactor/` | `文字识别引擎.py` | 龍文NLP引擎 | LongWen NLP | 🟡 占位 |
| `reactor/` | `语音识别引擎.py` | 龍音ASR引擎 | LongYin ASR | 🟡 占位 |
| `reactor/` | `金融交易引擎.py` | Web3-DNA交易 | Web3-DNA Trading | 🟡 占位 |

### 协议模块 (Protocols)

| 目录 | 文件 | 中文名 | 英文名 | 状态 |
|------|------|--------|--------|------|
| `protocols/` | `君子协议.py` | 君子协议 | JunZi Protocol | 🟢 就绪 |
| `protocols/` | `AI真相协议.py` | AI真相协议 | AI Truth Protocol | 🟢 就绪 |
| `protocols/` | `通心译协议.py` | 通心译协议 | TongXinYi Protocol | 🟢 就绪 |

### 集成模块 (Integration)

| 目录 | 文件 | 中文名 | 英文名 | 状态 |
|------|------|--------|--------|------|
| `adapters/` | `接口适配器.py` | 接口适配器 | Interface Adapter | 🟢 就绪 |
| `prompts/` | `系统提示词.py` | 系统提示词 | System Prompts | 🟢 就绪 |
| `agents/` | `代理配置器.py` | 代理配置器 | Agent Configurator | 🟢 就绪 |
| `notion/` | `Notion连接器.py` | Notion连接器 | Notion Connector | 🟢 就绪 |
| `sandbox/` | `沙箱执行器.py` | 沙箱执行器 | Sandbox Executor | 🟢 就绪 |

---

## 六、文件清单 | File Inventory

| 序号 | 文件路径 | 说明 |
|------|----------|------|
| 1 | `runtime/__init__.py` | 运行时模块包初始化 |
| 2 | `runtime/启动器.py` | 系统统一入口启动器 |
| 3 | `runtime/配置管理器.py` | 配置读写与热更新管理 |
| 4 | `governance/__init__.py` | 治理层模块包初始化 |
| 5 | `governance/三层监督器.py` | 感知·认知·决策三层监督 |
| 6 | `governance/三色审计器.py` | 🟢🟡🔴 审计标记系统 |
| 7 | `governance/DNA追溯器.py` | DNA血缘追溯链管理 |
| 8 | `router/__init__.py` | 路由器模块包初始化 |
| 9 | `router/龍魂路由器.py` | 智能模块路由分发 |
| 10 | `eventbus/__init__.py` | 事件总线模块包初始化 |
| 11 | `eventbus/事件总线.py` | 异步事件发布订阅 |
| 12 | `hooks/__init__.py` | 钩子模块包初始化 |
| 13 | `hooks/钩子管理器.py` | 生命周期钩子管理 |
| 14 | `audit/__init__.py` | 审计日志模块包初始化 |
| 15 | `audit/审计记录器.py` | 结构化日志持久化 |
| 16 | `snapshots/__init__.py` | 快照模块包初始化 |
| 17 | `snapshots/快照管理器.py` | 状态保存·恢复·对比 |
| 18 | `reactor/__init__.py` | 反应器模块包初始化 |
| 19 | `reactor/图像识别引擎.py` | 龍瞳OCR（占位） |
| 20 | `reactor/文字识别引擎.py` | 龍文NLP（占位） |
| 21 | `reactor/语音识别引擎.py` | 龍音ASR（占位） |
| 22 | `reactor/金融交易引擎.py` | Web3-DNA交易（占位） |
| 23 | `memory/__init__.py` | 记忆系统模块包初始化 |
| 24 | `memory/记忆管理器.py` | 三层记忆架构管理 |
| 25 | `sandbox/__init__.py` | 沙箱模块包初始化 |
| 26 | `sandbox/沙箱执行器.py` | 安全代码执行环境 |
| 27 | `protocols/__init__.py` | 协议层模块包初始化 |
| 28 | `protocols/君子协议.py` | CC BY-NC-SA 4.0 协议 |
| 29 | `protocols/AI真相协议.py` | AI输出验证标准 |
| 30 | `protocols/通心译协议.py` | 双语注释标准 |
| 31 | `adapters/__init__.py` | 适配器模块包初始化 |
| 32 | `adapters/接口适配器.py` | 统一接口转换层 |
| 33 | `prompts/__init__.py` | 提示词模块包初始化 |
| 34 | `prompts/系统提示词.py` | 提示词模板管理 |
| 35 | `agents/__init__.py` | 智能体模块包初始化 |
| 36 | `agents/代理配置器.py` | 角色权限配置管理 |
| 37 | `notion/__init__.py` | Notion模块包初始化 |
| 38 | `notion/Notion连接器.py` | Notion API集成 |
| 39 | `database/__init__.py` | 数据库模块包初始化 |
| 40 | `database/龍魂数据库.py` | SQLite封装引擎 |
| 41 | `scripts/占位脚本.py` | 脚本库占位 |
| 42 | `ROOT_CARD.md` | 根卡片索引文档 |

**总计**: 18个目录, 42个文件

---

## 七、开发规范 | Development Standards

### 7.1 DNA追溯头格式

```python
#龍芯⚡️{YYYY-MM-DD}-{项目}-{模块}-{版本}
```

### 7.2 三色审计标记

- 🟢 **绿色** — 正常/通过/安全
- 🟡 **黄色** — 警告/注意/需复核
- 🔴 **红色** — 错误/阻断/危险

### 7.3 君子协议声明

每个文件头部必须包含：
```python
# 🟢 君子协议 | JunZi Protocol: CC BY-NC-SA 4.0
# 🟡 AI Truth Protocol: All outputs must be verifiable and traceable
# 🔴 DNA Trace: #龍芯⚡️2026-06-18-{模块}-{版本}
```

### 7.4 通心译双语注释

所有类、函数、模块必须包含中英文双语注释：
```python
class 示例类:
    """通心译 | TongXinYi: Example Class — 示例类说明"""
    
    def 示例方法(自身):
        """🟢 示例方法 | Example method"""
        pass
```

---

## 八、联系方式与贡献 | Contact & Contribution

- **龍魂共同体** | LongHun Community
- **协议**: CC BY-NC-SA 4.0 International
- **版本**: v2.0
- **最后更新**: 2026-06-18

> *"以心传心，以码载道"*
> *"Transmit heart to heart, carry the way through code"*

---

**END OF ROOT CARD** | 根卡片结束

```
DNA: #龍芯⚡️2026-06-18-CNSH-ROOT-CARD-v2.0
龍魂永存 | LongHun Eternal
```
