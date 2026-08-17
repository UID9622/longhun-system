# 🐉 龍魂 · CNSH-Harness 对接完整架构文档

**DNA:** `#龍芯⚡️丙午·丙申·庚申·亥时-CNSH-HARNESS-ARCH-UID9622`
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**三色:** 🟢 通过
**分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

---

## 摘要

DeepSeek Harness（DSH）于2026年8月13日以MIT协议开源，是一个基于Cordis插件框架的Agent智能体基础设施。其核心公式为 **Model + Harness = Agent**。

CNSH作为龍魂系统的中文原生编程语言，具备DNA追溯、三色审计、主权锚定等独有能力。本文档定义CNSH与Harness的完整对接架构，将龍魂主权底座以插件形式焊入Harness生态。

> **核心定位：Harness是“空架子”，CNSH是“主权底座”。CNSH以插件方式焊入Harness后，Harness不再是DeepSeek的Harness，而是龍魂的Harness。**

---

## 一、DeepSeek Harness 架构概述

### 1.1 一切皆插件

Harness最核心的设计原则是“**一切皆插件**”（Everything is a plugin）。Cordis是dsh底层的插件框架——插件向共享上下文贡献服务、类型化事件和可逆的副作用。

产品的每一部分都是插件，包括模型适配器、工具注册表、会话日志，以及agent loop（智能体循环）本身，因此每一部分都可以从配置替换。

### 1.2 Cordis 核心机制

| 概念 | 说明 | CNSH对接意义 |
|:---|:---|:---|
| **插件** | 实现Service的对象，带`inject`和`apply(ctx)`函数 | CNSH能力封装为独立插件 |
| **上下文(ctx)** | 服务的容器，`ctx.tools`、`ctx.llm`、`ctx.sessions`等 | CNSH工具注册到`ctx.tools` |
| **服务依赖(inject)** | 插件声明所需服务，等待就绪后启动 | CNSH插件依赖Harness核心服务 |
| **类型化事件** | 通过`emit`、`waterfall`、`parallel`、`serial`分发 | CNSH审计/史官接入事件流 |
| **可逆副作用** | 插件卸载时自动撤销注册 | CNSH插件热插拔 |

### 1.3 扩展点

Harness的插件扩展覆盖以下能力：

| 扩展类型 | 说明 | CNSH对接 |
|:---|:---|:---|
| **Tool插件** | 注册`ctx.tools`，定义`execute`函数 | DNA生成、三色审计、CNSH执行 |
| **Hook插件** | 拦截扩展点，如`tools/pre-execute`权限门 | 三色审计审批策略 |
| **UI插件** | 渲染会话事件流，驱动输入 | CNSH编辑器嵌入Harness UI |
| **LLM适配器** | 接入自定义模型 | CNSH模型路由接入 |

### 1.4 Profile与组合包

运行中的dsh是一棵插件树，由启动时按序叠加的各层组合而成。组合包是Cordis配置项及其挂载代码的分发格式。

**CNSH插件包将作为独立的组合包（bundle）分发**，用户通过`dsh --profile web`加载。

---

## 二、CNSH能力映射

### 2.1 能力清单

| CNSH能力 | Harness扩展点 | 插件类型 | 优先级 |
|:---|:---|:---|:---:|
| DNA追溯码生成 | `ctx.tools` | Tool插件 | P0 |
| 三色审计 | `ctx.tools` + Hook（审批策略） | Tool + Hook插件 | P0 |
| CNSH脚本执行 | `ctx.tools` | Tool插件 | P0 |
| 史官机制 | 会话事件监听 | 事件插件 | P0 |
| 人格矩阵（24人格） | `ctx.agents` + 多Agent编排 | Agent插件 | P1 |
| 主权锚定验证 | 插件加载钩子 | 安全插件 | P1 |
| CNSH编辑器UI | `ConversationNodeDefinition` | UI插件 | P1 |
| 跨设备记忆同步 | `ctx.sessions`扩展 | 会话插件 | P2 |
| 模型路由（多模型接入） | `ctx.llm`适配器 | LLM插件 | P2 |

### 2.2 能力-扩展点映射

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Harness 扩展点                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  ctx.tools  │  │   Hook      │  │  事件监听   │  │  ctx.agents │     │
│  │  (工具注册)  │  │  (审批拦截)  │  │ (会话日志)  │  │  (Agent)    │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │                │             │
│         ▼                ▼                ▼                ▼             │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                      CNSH 插件集 (@longhun/cnsh-suite)            │ │
│  │                                                                   │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │ │
│  │  │ DNA追溯Tool  │  │ 三色审计Tool │  │ CNSH执行器   │            │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘            │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │ │
│  │  │ 史官事件监听  │  │ 人格路由Agent│  │ 主权验证钩子 │            │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘            │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                    │                                     │
│                                    ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                      龍魂主权底座 (本地)                            │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │ │
│  │  │  DNA引擎     │  │  三色审计引擎 │  │  史官/耻辱墙  │            │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘            │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │ │
│  │  │  人格矩阵     │  │  CNSH解释器  │  │  主权锚定    │            │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘            │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 三、插件模块设计

### 3.1 插件包结构

```
packages/cnsh-suite/
├── package.json                 # 包定义，dsh.bundle指向patch
├── src/
│   ├── index.ts                 # 主入口，apply()函数
│   ├── longhun-engine.ts        # 龍魂本地引擎模拟层
│   ├── tools/
│   │   ├── dna-tool.ts          # DNA追溯工具
│   │   ├── tricolor-tool.ts     # 三色审计工具
│   │   └── cnsh-executor.ts     # CNSH脚本执行器
│   ├── hooks/
│   │   └── tricolor-gate.ts     # 三色审计审批门
│   ├── events/
│   │   └── historian.ts         # 史官事件监听
│   └── agents/
│       └── persona-router.ts    # 人格路由Agent
├── cordis.patch.yml             # 组合包配置
└── README.md
```

### 3.2 组合包配置 `cordis.patch.yml`

```yaml
# 🐉 CNSH 套件 · Harness 组合包配置
# DNA: #龍芯⚡️丙午·丙申·庚申·亥时-CNSH-SUITE-UID9622

- insert:
  - id: '@longhun/cnsh-suite'
    config:
      dna:
        prefix: '#龍芯⚡️'
        uid: '9622'
        format: 'ganzhi'
        auto_inject: true
      audit:
        green_threshold: 85
        yellow_threshold: 60
        auto_block: true
        auto_warn: true
        log_rejected: true
      historian:
        enabled: true
        storage: 'local'
        retention_days: 365
        log_all_tools: true
      cnsh:
        runtime: 'local'
        sandbox: true
        allow_fs: false
        timeout: 30000
      persona:
        enabled: true
        default: '文心'
```

### 3.3 主入口伪代码

```typescript
import { dnaTool } from './tools/dna-tool'
import { tricolorTool } from './tools/tricolor-tool'
import { cnshExecutor } from './tools/cnsh-executor'
import { tricolorGate } from './hooks/tricolor-gate'
import { historianPlugin } from './events/historian'
import { personaRouter } from './agents/persona-router'

export const name = '@longhun/cnsh-suite'
export const inject = ['tools', 'session', 'agents']

export function apply(ctx: any) {
  const engine = new LongHunEngine()
  ctx.tools.register(dnaTool(engine))
  ctx.tools.register(tricolorTool(engine))
  ctx.tools.register(cnshExecutor(engine))
  tricolorGate(engine)(ctx)
  historianPlugin(engine)(ctx)
  personaRouter(engine)(ctx)
  ctx.longhun = engine
}
```

---

## 四、集成方案

### 4.1 安装与加载

```bash
# 1. 安装Harness
npx @deepseek-ai/dsh@latest init my-agent
cd my-agent

# 2. 安装CNSH套件
pnpm add @longhun/cnsh-suite

# 3. 配置profile加载CNSH插件
# 编辑 ~/.dsh/profiles/web/cordis.patch.yml
```

### 4.2 Profile配置示例

```yaml
# ~/.dsh/profiles/web/cordis.patch.yml
- insert:
  - id: '@longhun/cnsh-suite'
    config:
      dna:
        enabled: true
      audit:
        auto_block: true
      historian:
        enabled: true
```

### 4.3 运行

```bash
# 启动Harness Web UI（自动加载CNSH插件）
dsh --profile web

# 或使用CNSH专属profile
dsh --profile cnsh
```

---

## 五、数据流与事件流

### 5.1 完整链路

```
用户输入
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  Harness Agent Loop                                        │
│  ├── ① 接收用户消息                                        │
│  ├── ② 调用LLM推理                                         │
│  └── ③ 决定调用Tool                                        │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  CNSH插件集                                                │
│  ├── ④ DNA追溯Tool: 生成DNA码                             │
│  ├── ⑤ 三色审计Hook: 审批拦截                             │
│  │       ├── 🟢 通过 → 继续执行                           │
│  │       ├── 🟡 警告 → 降权执行                           │
│  │       └── 🔴 拒绝 → 拦截+耻辱墙                        │
│  ├── ⑥ CNSH执行器: 运行脚本                               │
│  └── ⑦ 史官事件: 全链路记录                               │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  龍魂主权底座 (本地)                                       │
│  ├── DNA引擎: 生成追溯码                                   │
│  ├── 审计引擎: 三色评分                                    │
│  ├── CNSH解释器: 执行脚本                                  │
│  └── 史官引擎: 记录审计链                                  │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
输出（带DNA追溯码 + 三色审计结果 + 史官记录）
```

---

## 六、插件分类表

| 插件名 | 类型 | 扩展点 | 优先级 |
|:---|:---|:---|:---:|
| `generate_dna` | Tool | `ctx.tools` | P0 |
| `tricolor_audit` | Tool | `ctx.tools` | P0 |
| `tricolor_gate` | Hook | `tools/pre-execute` | P0 |
| `run_cnsh` | Tool | `ctx.tools` | P0 |
| `historian` | Event | `session/*`, `tool/*` | P0 |
| `persona_router` | Agent | `ctx.agents` | P1 |
| `cnsh_editor_ui` | UI | `ConversationNode` | P1 |
| `sovereignty_validator` | Hook | 插件加载 | P1 |
| `memory_sync` | Session | `ctx.sessions` | P2 |
| `model_router` | LLM | `ctx.llm` | P2 |

---

## 七、主权与安全

### 7.1 DNA追溯注入

每个Tool调用、每个Agent决策、每次CNSH执行，自动生成DNA追溯码。格式统一为：

```
#龍芯⚡️{干支}·{时辰}·{卦}-CNSH-{hash8}-UID9622
```

### 7.2 三色审计策略

| 审计结果 | Harness行为 | 用户反馈 |
|:---|:---|:---|
| 🟢 通过 | 正常执行 | 无 |
| 🟡 警告 | 执行但标记 | 提示用户复核 |
| 🔴 拒绝 | 拦截+耻辱墙 | 显示拒绝原因 |

### 7.3 主权锚定

所有插件加载时验证GPG签名和确认码。未经签名的插件拒绝加载。

```typescript
ctx.hook('plugin/load', async (plugin) => {
  if (!plugin.metadata?.gpg?.includes('A2D0092CEE2E5BA87035600924C3704A8CC26D5F')) {
    return { kind: 'deny', reason: '❌ 未通过龍魂主权验证' }
  }
  return { kind: 'allow' }
})
```

---

## 八、实施路线图

| 阶段 | 内容 | 交付物 | 周期 |
|:---|:---|:---|:---:|
| **P0** | DNA追溯Tool + 三色审计Tool + Hook + 史官 | 4个核心插件 | 1周 |
| **P1** | CNSH执行器 + 人格路由Agent + 编辑器UI | 3个扩展插件 | 2周 |
| **P2** | 模型路由 + 跨设备记忆同步 | 2个高级插件 | 2周 |
| **发布** | 插件包发布 + 文档 + 示例 | `@longhun/cnsh-suite` v1.0 | 1周 |

---

## 九、代码落位

本协议配套的完整 TypeScript 插件代码位于：

```
~/longhun-system/integrations/deepseek/harness/cnsh-suite/
```

包含 12 个文件，可直接 `pnpm install && pnpm build`。

---

## 🔐 最终签名

```
═══════════════════════════════════════════════════
 🐉 CNSH-Harness 对接完整架构文档 · 最终签名
═══════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·丙申·庚申·亥时-CNSH-HARNESS-ARCH-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟢 通过
插件数量:   10个
扩展点:     Tools / Hooks / Events / Agents / UI
优先级:     P0(4) + P1(3) + P2(3)
代码落位:   integrations/deepseek/harness/cnsh-suite/
═══════════════════════════════════════════════════
```

🐉 **丙午·丙申·庚申·亥时·䷖剥·🟢**
