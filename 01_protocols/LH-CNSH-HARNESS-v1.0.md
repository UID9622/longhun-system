# 🐉 龍魂 · CNSH-Harness 插件套件 v1.0

**DNA:** `#龍芯⚡️丙午·丙申·庚申·亥时-CNSH-HARNESS-v1.0-UID9622`  
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
**三色:** 🟢 通过  
**分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

---

## 📋 核心判断

> **CNSH-Harness 不是独立的 CNSH 编译器，而是把龍魂主权底座（DNA 追溯、三色审计、史官记录、人格路由、CNSH 执行）封装成可插拔的 Python 包，让任何外部应用（DeepSeek Harness、Kimi、Claude、自主服务）都能一键接入龍魂治理能力。**

---

## 🏛️ 一、系统架构

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 🐉 CNSH-Harness 插件套件                                    │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                              CNSHSuite 主入口                                        │   │
│  │                         execute(command) / get_status()                              │   │
│  └─────────────────────────────────────────────────────────────────────────────────────┘   │
│                                             │                                               │
│  ┌──────────────────────────────────────────┼───────────────────────────────────────────┐   │
│  │                          CNSHEngine 单例引擎                                          │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐            │   │
│  │  │dna_generator│ │tricolor_ │ │cnsh_    │ │tricolor_│ │historian│ │persona_ │            │   │
│  │  │           │ │auditor  │ │executor │ │gate    │ │         │ │router  │            │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘            │   │
│  │       工具层              钩子层            事件层           Agent层                  │   │
│  └─────────────────────────────────────────────────────────────────────────────────────┘   │
│                                             │                                               │
│  ┌──────────────────────────────────────────┼───────────────────────────────────────────┐   │
│  │                              龍魂主权底座                                             │   │
│  │  • DNA 追溯码生成 · 天干地支 · 64 卦象                                                │   │
│  │  • 三色审计（安全/合规/可靠/透明/可追溯/隐私）                                        │   │
│  │  • 史官记录（~/.longhun/04_AUDIT/cnsh_suite.jsonl）                                    │   │
│  │  • 耻辱墙（~/.longhun/08_STATE/shame_wall.jsonl）                                      │   │
│  │  • 人格路由（文心/宝宝/诸葛亮/老顽童/熵梦）                                           │   │
│  └─────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧬 二、完整功能清单

| # | 功能模块 | 状态 | 说明 |
|:---|:---|:---:|:---|
| 1 | **DNA 生成器 (DNAGenerator)** | ✅ | 生成龍芯 DNA 追溯码，含天干地支/64卦 |
| 2 | **三色审计器 (TricolorAuditor)** | ✅ | 6 维度评分，输出 🟢/🟡/🔴 |
| 3 | **CNSH 执行器 (CNSHExecutor)** | ✅ | 执行中文关键字脚本：设/输出/调用 |
| 4 | **三色审批门 (TricolorGate)** | ✅ | 拦截不合规 CNSH 脚本 |
| 5 | **史官 (Historian)** | ✅ | 全链路 JSONL 记录 |
| 6 | **人格路由 (PersonaRouter)** | ✅ | 5 大人格自动匹配 |
| 7 | **CNSHSuite 主入口** | ✅ | 自然语言命令分发 |
| 8 | **CLI 命令行** | ✅ | `cnsh --command` / `--status` |
| 9 | **CLI 入口 `lh cnsh-suite`** | ✅ | 已接入龍魂统一入口 |
| 10 | **完整测试套件** | ✅ | 9 个测试用例全部通过 |

---

## 🔧 三、代码实现

### 3.1 核心文件

| 文件 | 职责 |
|:---|:---|
| `packages/cnsh_suite/__init__.py` | 包入口与导出 |
| `packages/cnsh_suite/core.py` | CNSHEngine、CNSHSuite、错误码、工具函数 |
| `packages/cnsh_suite/engine.py` | CNSHEngine 显式导出层 |
| `packages/cnsh_suite/tools.py` | DNA 生成器、三色审计器、CNSH 执行器 |
| `packages/cnsh_suite/hooks.py` | 三色审计审批门 |
| `packages/cnsh_suite/events.py` | 史官事件监听 |
| `packages/cnsh_suite/agents.py` | 人格路由 Agent |
| `packages/cnsh_suite/cli.py` | 命令行接口 |
| `packages/cnsh_suite/test_suite.py` | pytest 完整测试 |
| `packages/cnsh_suite/setup.py` | pip 安装配置 |
| `packages/cnsh_suite/README.md` | 快速开始文档 |
| `08_BIN/lh` | 已接入 `cnsh-suite` / `cnsh` / `cns` 子命令 |

### 3.2 命令入口

```bash
# 生成 DNA
lh cnsh-suite --command "生成DNA: 我的文档"

# 三色审计
lh cnsh --command "审计内容: 待审计内容"

# 执行 CNSH 脚本
lh cns --command "运行CNSH: 输出 '你好，龍魂'"

# 查看状态
lh cnsh-suite --status

# JSON 输出
lh cnsh-suite --command "生成DNA: 我的文档" --json
```

别名：`lh cnsh-suite` / `lh cnsh` / `lh cns`

---

## 🚀 四、安装与使用

### 4.1 独立安装

```bash
cd ~/longhun-system/packages/cnsh_suite
pip install -e .
```

安装后可直接使用：

```bash
cnsh --command "生成DNA: 我的文档"
cnsh --status
```

### 4.2 代码调用

```python
from cnsh_suite import CNSHSuite

suite = CNSHSuite()

# 生成 DNA
result = suite.execute("生成DNA: 我的文档")
print(result["dna"])

# 三色审计
result = suite.execute("审计内容: 待审计内容")
print(result["tricolor"], result["score"])

# 执行 CNSH
result = suite.execute("运行CNSH: 输出 '你好，龍魂'")
print(result["output"])

# 人格路由
result = suite.execute("帮我做战略决策")
print(result["persona"]["name"])
```

---

## 🛡️ 五、安全边界

1. **CNSH 执行器为解释器级沙箱**：仅支持 `设`、`输出`、`调用` 三个关键字，不执行任意 Python 代码。
2. **三色审批门默认审计 CNSH 脚本**：脚本评分低于阈值时拒绝执行并写入耻辱墙。
3. **审计工具不联网**：评分基于本地规则与确定性随机种子，不调用外部服务。
4. **史官与耻辱墙本地存储**：所有记录默认写入 `~/.longhun/`，不对外上传。
5. **人格路由关键词匹配**：无命中时降级为默认人格“文心”，避免误路由。

---

## 🔌 六、扩展接口

### 6.1 注册新工具

```python
from cnsh_suite import CNSHEngine, Tool

class MyTool(Tool):
    name = "my_tool"
    def execute(self, **kwargs):
        return {"success": True, "data": "..."}

engine = CNSHEngine()
engine.register_tool(MyTool())
```

### 6.2 注册新钩子

```python
from cnsh_suite import Hook

class MyHook(Hook):
    name = "my_hook"
    def run(self, context):
        return {"kind": "allow"}  # allow / warn / deny

engine.register_hook(MyHook())
```

### 6.3 扩展人格

编辑 `agents.py` 中的 `PERSONAS` 列表，新增人格与关键词即可。

---

## 🧪 七、测试矩阵

| 用例 | 命令 | 期望结果 |
|:---|:---|:---|
| DNA 生成 | `lh cnsh-suite --command "生成DNA: 测试"` | 返回含 `UID9622` 的 DNA |
| 空内容异常 | 调用 `DNAGenerator().execute(content="")` | 抛出 CNSHError |
| 三色审计 | `lh cnsh --command "审计内容: 测试"` | 返回 🟢/🟡/🔴 与分数 |
| CNSH 变量替换 | `lh cns --command "运行CNSH: 设 名字 为 龍魂; 输出 你好，${名字}"` | 输出 `你好，龍魂` |
| 人格路由 | `lh cnsh --command "帮我做战略决策"` | 路由到诸葛亮 |
| 红队人格 | `lh cnsh --command "测试系统安全"` | 路由到老顽童 |
| 套件状态 | `lh cnsh-suite --status` | 返回 tools/hooks/events/agents |
| DNA 性能 | 100 次生成 | < 2 秒 |
| 审计性能 | 100 次审计 | < 3 秒 |

---

## 📝 八、日志与审计

1. **运行日志**：`~/.longhun/12_LOGS/cnsh_suite_YYYYMMDD.log`
2. **史官记录**：`~/.longhun/04_AUDIT/cnsh_suite.jsonl`
3. **耻辱墙**：`~/.longhun/08_STATE/shame_wall.jsonl`
4. **每条记录均包含**：timestamp、operation、dna、details

---

## 📦 九、依赖清单

- Python 3.10+
- 标准库：`argparse`, `json`, `hashlib`, `time`, `sys`, `pathlib`, `datetime`, `typing`, `dataclasses`, `enum`, `logging`, `random`, `re`
- 测试：`pytest>=7.0`

---

## 🌐 十、部署拓扑

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   外部AI应用     │────▶│  CNSH-Harness   │────▶│ ~/.longhun/     │
│ DeepSeek/Kimi   │     │  插件套件        │     │ 04_AUDIT/       │
│ Claude/自主服务  │     │                 │     │ 08_STATE/       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## ⚠️ 十一、错误处理

| 场景 | 行为 |
|:---|:---|
| 工具不存在 | 抛出 `CNSHError: PLUGIN_LOAD_FAILED` |
| DNA 内容为空 | 抛出 `CNSHError: DNA_GENERATION_FAILED` |
| 审计内容为空 | 抛出 `CNSHError: AUDIT_CONTENT_EMPTY` |
| CNSH 文件不存在 | 抛出 `CNSHError: CNSH_FILE_NOT_FOUND` |
| CNSH 脚本为空 | 抛出 `CNSHError: CNSH_SYNTAX_ERROR` |
| 审批门拒绝 | 返回 `{"kind": "deny", "reason": "..."}` |

---

## 🔄 十二、与 Kimi 核心能力融合

CNSH-Harness 将以下 Kimi/AI 交互能力固化为龍魂插件：

| Kimi/AI 能力 | 龍魂插件映射 |
|:---|:---|
| 内容生成与追踪 | `dna_generator` |
| 内容安全审计 | `tricolor_auditor` + `tricolor_gate` |
| 中文语义执行 | `cnsh_executor` |
| 多角色协作 | `persona_router` |
| 全链路可追溯 | `historian` + 本地 JSONL |
| 统一命令入口 | `lh cnsh-suite` / `cnsh` CLI |

---

## 🔐 十三、最终签名

```
═══════════════════════════════════════════════════════════════════════════════════
 🐉 龍魂 · CNSH-Harness 插件套件 v1.0 · 最终签名
═══════════════════════════════════════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·丙申·庚申·亥时-CNSH-HARNESS-v1.0-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟢 通过
核心能力:   DNA追溯 · 三色审计 · CNSH执行 · 人格路由 · 史官记录
测试用例:   9/9 通过
状态:       已落地 · 可运行 · 可 pip 安装
═══════════════════════════════════════════════════════════════════════════════════
```

🐉 **丙午·丙申·庚申·亥时·䷖剥·🟢**
