# 龍魂 × DeepSeek Harness 融合协议 v1.0

> DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷏豫-HARNESS-FUSION-v1.0-7d3f1a2b
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0（核心思想层）
> 上位: LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md · LH-SYNTAX-SPEC-v3.0.md
> 三色: 🟢 调研实证 + 映射对齐 🟡 代码落地逐项待实测 🔴 无
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

---

## 〇、一句话结论

**DeepSeek Harness 把「模型是大脑、执行是神经系统」拆成了可组合的插件矩阵；龍魂体系天生就是多 Agent 编排体，缺的不是理念，是「统一插件契约 + 时空可逆的执行内核 + 全量轨迹回放」。本协议把 Harness 的 Cordis 插件哲学吸收为龍魂的工程规范，不改龙魂 DNA。**

---

## 一、Harness 是什么（学习笔记·2026-08-13 发布）

| 项 | 内容 |
|:---|:---|
| 发布时间 | 2026-08-13 · DeepSeek 官方 · v0.1 开发者预览版 |
| 开源 | MIT 协议 |
| 定位 | 开源智能体运行框架 |
| 核心公式 | **Model + Harness = Agent**（模型=大脑，Harness=神经系统） |
| 生态 | 社区插件增长迅速 · 热插拔 · Jani 组件替换 |

### 1.1 四大核心设计理念

1. **一切皆插件（Everything is a Plugin）**：模型/工具/会话/沙箱/存储/循环/调度/UI 全部由插件组合，开发者不改 Harness 源码，靠配置选/换/扩能力。
2. **Cordis 插件系统**（底层基座）：
   - **时间可组合性**：组件卸载时，其产生的所有副作用（事件监听/文件句柄/内存分配）被**完整逆转**，干净回滚。
   - **空间可组合性**：组件依赖声明式表达，运行时响应式管理，插件灵活协作。
   - 四大核心对象：**Context**（上下文容器）· **Fiber**（调度单元）· **Reflect**（反射/内省）· **Registry**（注册表）。
3. **可追溯性**：append-only 会话日志，模型看到的一切（系统提示/思维链/工具调用/子 Agent 调度）完整记录，Trajectory 视图可恢复/分叉/检索/回放。
4. **四种运行模式**：标准模式 · PTC（程序化工具调用）· 极简模式 · 创造模式。

### 1.2 插件契约（核心抽象）

```
Plugin = {
  id, name, version,        // 身份
  dependencies: [...],      // 声明式依赖（空间可组合）
  onLoad(ctx) -> disposer,  // 装载：返回"逆转函数"（时间可组合）
  onUnload(),               // 卸载：副作用逆转
  provides: [...],          // 提供能力
  subscribes: [...],        // 订阅事件
}
```

**时空可组合性 = 两个铁律**：
- 时间：`onLoad` 必须返回 disposer，卸载时逐个调用 disposer 逆转副作用 → **零残留**。
- 空间：`dependencies` 声明式表达，Cordis 运行时解析依赖图、按序装载。

### 1.3 事件分发（EventBus）

Cordis 事件总线支持**四种分发模式**：
| 模式 | 语义 |
|:---|:---|
| emit | 广播（所有订阅者各收一份） |
| waterfall | 瀑布（前一个结果传给下一个，管道） |
| parallel | 并行（同时跑，等全部） |
| serial | 串行（排队依次跑） |

---

## 二、龍魂现状盘点（融合前的家底）

| 龍魂已有 | 位置 | 与 Harness 对齐度 |
|:---|:---|:---|
| 事件总线 LCB v1.0 | `08_BIN/lh_event_bus.py` | 🟡 只有"广播+订阅"，**无 waterfall/parallel/serial** |
| AI 互通总线 | `bin/lh_bus.py` | 🟡 人话封装，底层复用 LCB |
| 插件基座 | `bin/lh_cnsh_plugin.py` | 🟡 单插件（CNSH 贴入），无统一契约 |
| 人格编排 | `bin/lh_persona_team.py` | 🟢 多 Agent 小队（PMO/代码/PR/安全） |
| 智能体编排 | `05_ENGINES/longhun_agents/run.py` | 🟢 GrandOrchestrator 三层（蚁群+人格+黑板） |
| AI 网关 | `bin/lh_ai_gateway.py` | 🟡 多模型（混元/DeepSeek/Kimi/Claude）但非插件式 adapter |
| 审计日志 | `audit_log.jsonl` / LCB 事件表 | 🟢 append-only 已有 |
| 调度 | `bin/lh_capability_scheduler.py` | 🟢 能力调度 |
| 语义路由 | `.codebuddy/cnsh_semantic_protocol.md` | 🟢 语义路由已有 |
| 熔断 | 四级熔断体系 | 🟢 已有（L0-L3） |
| 轨迹回放 | 无 | 🔴 **缺失** |

**结论：龍魂已有「多 Agent + 事件总线 + 调度 + 审计」的神经系统骨架，缺的是 Harness 的「统一插件契约 + 时空可逆内核 + Trajectory 回放」三个工程件。**

---

## 三、融合映射表（Harness → 龍魂）

| Harness 概念 | 龍魂落点 | 融合动作 |
|:---|:---|:---|
| Plugin 契约 | `lh_cnsh_plugin.py` → 升级为通用插件基座 | 统一 `id/name/version/deps/onLoad/onUnload/provides/subscribes` |
| 时空可组合性 | 龍魂熔断 + 任务回滚 | 新增副作用注册表（EffectScope），onLoad 注册 disposer，熔断时全量逆转 |
| Context | 会话上下文（`lh capture` / 统一记忆 8771） | 插件内共享 Context 对象 |
| Registry | `20_CONFIG/persona-duty-matrix.json` / 命令总目 | 插件注册表对齐 Command Index |
| EventBus 四种分发 | `08_BIN/lh_event_bus.py` | **新增 waterfall/parallel/serial 三种分发模式** |
| Trajectory | `audit_log.jsonl` | 新增轨迹视图：可恢复/分叉/回放 |
| 四种运行模式 | 人格路由 | 标准=常态 · PTC=`lh.py` 命令直达 · 极简=低算力 · 创造=创意爆发(P11) |
| Model Adapter | `lh_ai_gateway.py` | 封装为统一 adapter 接口（Ollama/混元/DeepSeek/Kimi） |
| Jani 热替换 | 龍魂引擎热更新 | 插件 onUnload+onLoad 原子替换 |

---

## 四、落地规范（龍魂工程实现细则）

### 4.1 插件契约（龍魂版）

```python
# 每个龍魂插件文件头声明（沿用语法规范）
PLUGIN_META = {
    "id": "lh.skill.deben-audit",       # 命名空间: lh.<类别>.<名>
    "name": "德本审计引擎",
    "version": "1.0.0",
    "dependencies": ["lh.core.time", "lh.core.dna"],  # 空间可组合
    "provides": ["audit.deben"],         # 对外能力
    "subscribes": ["skill.execution"],   # 订阅事件
    "license": "MulanPSL v2",
}

def onLoad(ctx):
    # 注册副作用（事件监听/文件句柄/内存），返回 disposer 列表
    effects = []
    effects.append(ctx.subscribe("skill.execution", handler))  # 自动登记
    effects.append(open_log_handle())
    return effects  # 卸载时按逆序调用 → 时间可组合

def onUnload(ctx):
    # 显式清理（可选，disposer 优先）
    pass
```

### 4.2 EffectScope 副作用注册表（时间可组合落地）

- 位置：`bin/lh_effect_scope.py`
- 核心：`scope = EffectScope(); scope.register(disposer); scope.reverse_all()`
- 触发时机：插件卸载 · L1/L2 熔断 · 任务失败回滚
- 铁律：**onLoad 不返回 disposer 的插件 = 不合格插件（P05 🔴）**

### 4.3 四种事件分发模式

`lh_event_bus.py` 的 `publish` 增加 `--dispatch emit|waterfall|parallel|serial`：
- emit：现有广播
- waterfall：订阅者按 priority 排队，前一个输出注入后一个输入
- parallel：并发执行（线程池），全部完成返回
- serial：排队串行

### 4.4 Trajectory 轨迹视图

- 数据源：LCB 事件表（append-only 已有）+ 会话快照
- 新增 `lh trajectory` 命令：`show <dna>` / `fork <dna>` / `replay <dna>`
- 对应审计追溯 + 会话恢复

### 4.5 四种运行模式（龍魂映射）

| Harness 模式 | 龍魂对应 | 触发 |
|:---|:---|:---|
| 标准 | 常态人格路由 | 默认 |
| PTC | `lh.py` 子命令直达 | 明确指令/脚本 |
| 极简 | 低算力模式（流控 100 t/s） | 资源紧张 |
| 创造 | P11 李白创意链路 | 创意/脑暴指令 |

---

## 五、落地清单（本次执行）

| # | 交付物 | 路径 | 状态 |
|:---:|:---|:---|:---:|
| 1 | 本融合协议 | `01_protocols/LH-HARNESS-FUSION-v1.0.md` | 🟢 |
| 2 | EffectScope 副作用注册表 | `bin/lh_effect_scope.py` | 待建 |
| 3 | 插件契约基座升级 | `bin/lh_plugin_kit.py` | 待建 |
| 4 | 事件总线四种分发 | `08_BIN/lh_event_bus.py` + `--dispatch` | 待建 |
| 5 | 轨迹视图 | `bin/lh_trajectory.py` | 待建 |
| 6 | AI 网关 adapter 接口 | `bin/lh_ai_gateway.py` 对齐 | 待建 |

---

## 六、审计与验收

- GATE-03 语义闸：融合不引入 Harness 专有名词污染龍魂语义路由（保持 `lh.*` 命名空间）
- GATE-05 伦理闸：插件契约不采集用户数据 · 副作用注册表是"本地回滚"非"云上传"
- GATE-09 DNA 闸：所有新文件头三行 + DNA 追溯码
- GATE-11 签名闸：交付前 `python3 bin/lh_gpg_sign.py sign .`
- 三色审计：代码落地后逐项实测，未实测不标 🟢

---

## 七、版本记录

| 版本 | 日期 | 内容 |
|:---|:---|:---|
| v1.0 | 2026-08-18 | 初版：Harness 学习笔记 + 龍魂映射 + 落地规范 |

---

> 本协议为思想层文档（CC BY-NC-SA 4.0），配套代码按 MulanPSL v2（工程层）。
> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
