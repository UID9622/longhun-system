# 龍魂系统 · 统一子系统收口总表 v3.0

> DNA: `#龍芯⚡️2026-07-06-MASTER-REGISTRY-SUBSYSTEMS-v3.3`
> 收口人: CodeBuddy
> 审计: 🟢 通过
> 原则: 一个仓库，一份总表，不可有未注册的子系统
>
> **关联文档:**
> - 归一架构: [`docs/ARCHITECTURE_NORMALIZATION_v1.0.md`](./docs/ARCHITECTURE_NORMALIZATION_v1.0.md)
> - 引擎去重: [`ENGINE_DEDUP_MANIFEST.md`](./ENGINE_DEDUP_MANIFEST.md)
> - 技能去重: [`SKILLS_DEDUP_MANIFEST.md`](./SKILLS_DEDUP_MANIFEST.md)
> - 插件主权: [`agents/CODEBUDDY_插件主权清单_v1.0.md`](./agents/CODEBUDDY_插件主权清单_v1.0.md)
> - 交接文档: [`L8_治理层/governance/HANDOVER_CODEBUDDY_龍魂神经网络实时总控_v2.0.md`](./L8_治理层/governance/HANDOVER_CODEBUDDY_龍魂神经网络实时总控_v2.0.md)
> - **v∞ 引擎归档（2026-07-06）**: 无限增长引擎/决策链/民主回复/权重算法/五行计算器v2-v3/流场压缩核 — 全部归档至权威目录
>
> **2026-07-06 架构归一操作:**
> - CNSH内核: 5个冗余目录→ `_archive/legacy/`（仅保留`cnsh-core/`为权威源）
> - 重复引擎: 权威引擎→ `L1_内核层/kernel/engines/`，副本已标注DUPLICATE_COPY
> - Web操作台: `web/` `portal/` `control-panel/` → `L5_服务层/services/`
> - 技能目录: `01_技能库/`(简中)→归档，`01_技能庫/`(正体)保留
> - 根目录: 143个散落文件→归入L1-L9层级目录，根目录仅保留24个核心文件
> - 归档统一: `_archive/` 集中管理所有废弃/备份/检疫内容
> - .gitignore: 新增 brain/voice-twin/train/outputs/.snapshots 规则
> - 引擎: 标记 8 个副本文件，确定 11 组权威源
> - 技能: 确认 skills.backup 为独立历史分支（全部 32 文件不同）
> - **v3.3 更新**: 五行映射全局对齐 — 数字根→五行统一为河图经典映射；IPA注册表wuxing_guard元数据修正；hetu_luoshu_dna.py新增数字根转五行函数

---

## 一、技能 (Skills) — 4 处，需收口为 1 处

### 1.1 `01_技能庫/`（权威源头）
| 技能 | 文件 | 用途 |
|------|------|------|
| code-audit | `code-audit.md` | 三色代码审计插件 |
| dna-gen | `dna-gen.md` | DNA 追溯码生成器 v2.0 |
| kimi-webbridge | `kimi-webbridge.md` | Kimi 浏览器桥接 |
| on-identity | `on-identity.md` | 身份核验（CONFIRM/SEAL/GPG） |
| on-translate | `on-translate.md` | 通心译·场景词典 |

### 1.2 `skills/`（开发/运行版本，与 01_技能庫 部分重合）
| 子目录 | 用途 |
|--------|------|
| `cnsh-aligner/` | CNSH 对齐器 |
| `core/` | 技能核心引擎 |
| `html-skills/` | HTML 技能 |
| `longhun-ai-lexicon/` | AI 词典 |
| `longhun-audit-integrated/` | 审计集成 |
| `longhun-cross-platform/` | 跨平台 |
| `longhun-kg-paper-index/` | 知识图谱论文索引 |
| `longhun-shield/` | 龍盾 |
| `longhun-tags/` | 标签系统 |
| `longhun-tongxinyi-v2/` | 通心意译 v2 |
| `py-skills/` | Python 技能 |
| `warehouse-audit/` | 仓库审计 |
| `wucai_coloring/` | 五色着色 |

**关键文件**:
- `longhun_skill_auto_completion_engine.py` — 技能自动完成引擎
- `longhun_standard_calculation_framework.py` — 标准计算框架
- `longhun-skills.json` — 技能注册表
- `registry.py` — 注册器
- `api.py` — API 层

### 1.3 `skills.backup/`（skills/ 的子集备份，内容重复）
仅含 `__init__.py`, `api.py`, `html-skills/`, `py-skills/` 等子集。**建议归档或删除**。

### 1.4 `skill-standards.integrated/`（标准文档）
- `LONGHUN-10SKILL-UNIFIED-STANDARD-v1.0.md`
- `LONGHUN-10SKILL-COMPLETE-INTEGRATION-FINAL.md`
- `LONGHUN-5SKILL-COMPLETE-STANDARD-v1.0.md`

### ⚠️ 技能收口建议
- `01_技能庫/` = 权威源头（5 个核心技能定义）
- `skills/` = 运行版本（含更多子技能+引擎+API）
- `skills.backup/` = 冗余 → **归档**
- `skill-standards.integrated/` = 标准文档 → 保留

---

## 二、引擎 (Engines) — 44 个引擎文件，按位置分类

### 2.1 引擎目录（独立子系统）

| 路径 | 引擎数 | 说明 |
|------|--------|------|
| `龍魂洛书369引擎/` | 7 子模块 | 启动器.py + core/ethics/journey/network/quantum/sovereignty/wuxing — 369数学体系核心 |
| `法律引擎/` | 2 | legal_engine.py + api_server.py — 法律条文检索引擎 |
| `engine/` | 2 | dao_ethics_anchor.py + memory/ |
| `engines/` | 1 | audit_engine.py |
| `cnsh-core/engines/` | 1 | audit_engine.py（与 engines/ 重复?） |

### 2.2 CNSH 体系引擎

| 路径 | 文件 | 用途 |
|------|------|------|
| `cnsh-core/rules/` | `rule_engine.py` | 规则引擎 |
| `cnsh-core/governance/` | `layered_governance_engine.py` | 分层治理引擎 |
| `cnsh-core/constitution/` | `longhun_weight_engine.py` | 权重引擎 |
| `cnsh-core/grammar/` | `cnsh_grammar_engine.py` | CNSH 语法引擎 |
| `cnsh-core/` | `m04_yijing_engine.py` | 易经引擎 |
| `cnsh-core/` | `people_behavior_engine.py` | 人员行为引擎 |
| `cnsh-core/scheduler/` | `heaven_duty_engine.py` | 天责调度引擎 |
| `cnsh-editor/` | `cnsh_editor_engine_v2.0.py` | 编辑器引擎 v2.0 |
| `cnsh-editor/` | `cnsh_translator_engine_v2.0.py` | 转译器引擎 v2.0 |
| `cnsh-editor/core/` | `cnsh_editor_engine_v2.0.py` | 编辑器引擎（重复?） |
| `cnsh-runtime-v1/` | `CNSH_代码审计引擎.py` | 代码审计引擎 |
| `cnsh-runtime-v1/` | `CNSH_流场可视化引擎.py` | 流场可视化引擎 |
| `cnsh-terminal/engines/` | `cnsh_editor_engine_v2.0.py` | 编辑器引擎（三份?） |
| `cnsh-terminal/engines/` | `cnsh_translator_engine_v2.0.py` | 转译器引擎（三份?） |
| `cnsh/` | `DNA授权执行引擎.py` | DNA 授权执行引擎 |
| `cnsh.integrated/` | `DNA授权执行引擎.py` | DNA 授权执行（集成本版） |
| `cnsh/reactor/` | `金融交易引擎.py` | 金融交易 |
| `cnsh/reactor/` | `图像识别引擎.py` | 图像识别 |
| `cnsh/reactor/` | `文字识别引擎.py` | 文字识别 |
| `cnsh/reactor/` | `语音识别引擎.py` | 语音识别 |
| `cnsh/research/` | `光刻机瓶颈推演引擎.py` | 光刻机推演 |

### 2.3 独立脚本/子系统引擎

| 路径 | 文件 | 用途 |
|------|------|------|
| `audit/` | `gua_audit_engine.py` | 卦象审计引擎 |
| `scripts/` | `復盤引擎.py` | 复盘引擎 |
| `scripts/` | `龍魂DNA主權引擎.py` | DNA 主权引擎 |
| `scripts/` | `龍魂语气引擎.py` | 语气引擎 |
| `scripts/` | `longhun_compression_engine.py` | 压缩引擎（scripts 版） |
| `scripts/persona/` | `longhun_persona_engine.py` | 人格引擎 |
| `scripts/yijing_algorithm/` | `yijing_engine.py` | 易经算法引擎 |
| `scripts/private-shared-imports/ip-assets-v2/` | `longhun_crypto_engine.py` | 加密引擎 |
| `scripts/private-shared-imports/ip-assets-v2/` | `tri_color_audit_engine.py` | 三色审计引擎 |
| `persona/` | `compression_engine.py` | 压缩引擎（persona 版） |
| `systems/v3/` | `五行融合决策引擎_v3.0.py` | 五行决策引擎 v3 |
| `longhun-font/engines/` | 4 个 `cnsh_font_engine*.py` | 字体引擎（4 份） |
| `skills/` | `longhun_skill_auto_completion_engine.py` | 技能自动完成引擎（skills 版） |
| `skills/core/` | `longhun_skill_auto_completion_engine.py` | 技能引擎（core 版） |
| `skills/` | `longhun-skill-auto-completion-engine.py` | 技能引擎（连字符版） |
| `skill-standards.integrated/` | `longhun-skill-auto-completion-engine.py` | 技能引擎（standard 版） |
| `integrated-modules/kimi_agent/` | `cnsh_core_engine.py` | CNSH 核心引擎 |
| `integrated-modules/skills.integrated/` | `longhun_skill_auto_completion_engine.py` | 技能引擎（integrated 版） |

### ⚠️ 引擎收口建议
- 同一引擎存在 **3-4 份拷贝**（如 cnsh_editor_engine、cnsh_translator_engine、skill_auto_completion_engine）
- 需建立**唯一权威源**，其余改为 import 引用或符号链接
- 优先级：`cnsh-core/` > `cnsh/` > `cnsh.integrated/` > `cnsh-terminal/engines/`

---

## 三、执行器 (Executors)

### 3.1 `executors/` 目录
| 子目录 | 用途 |
|--------|------|
| `task/` | 通用任务执行器 |
| `mvp/` | MVP 执行器 |
| `kimi-agent-v2/` | Kimi Agent v2 执行器 |
| `kfpp/` | KFPP 执行器 |
| `runtime/` | 运行时执行器 |

### 3.2 `bin/` 中的执行器
| 文件 | 用途 |
|------|------|
| `longhun_mvp_executor_v2.0.py` | MVP 执行器 v2.0 |
| `longhun_foundation_launcher_v2.0.py` | 基础启动器 |
| `persona_scheduler.py` | 人格调度器 |

### 3.3 `.codebuddy/agents/龙魂执行器.md`
Agent 定义：~/龙魂系统 的代理执行器。

---

## 四、Agents (代理人)

### 4.1 `agents/` 目录（运行时代理）
| 文件 | 用途 |
|------|------|
| `orchestrator.py` | 编排器（核心） |
| `task_executor_live_v1.py` | 任务执行器 v1 |
| `agent_daemon.py` | 代理守护进程 |
| `agent_eco_adapter.py` | 生态适配器 |
| `agent_status_reporter.py` | 状态报告器 |
| `longhun_foundation_launcher_auto.py` | 基础自动启动 |
| `longhun_notion_sync_auto.py` | Notion 自动同步 |
| `xpay_core_auto.py` | XPay 核心自动 |
| `manifest.json` | 代理清单 |
| `daemon.pid` / `daemon_state.json` | 守护进程状态 |

### 4.2 `.codebuddy/agents/龙魂执行器.md`
CodeBuddy 环境的 Agent 定义文件。

---

## 五、内核 (Kernels)

| 路径 | 说明 |
|------|------|
| `core/` | 龍魂心法·容错内核 v1.0 |
| `core-services/` | calendar 服务 |
| `cnsh-core/` | CNSH v2.1 编译器内核 + 语法引擎 + 规则引擎 + 治理引擎 + 易经引擎 + 统一 API |
| `cnsh.integrated/` | 集成运行时（含 agent/adapter/audit/governance/router/sandbox 等子模块） |
| `cnsh/` | 红线引擎 + DNA 授权引擎 + reactor（图像/语音/文字/金融） |
| `龍魂取证内核/` | 取证工具（5 文件：取证内核.py + 技能内核.py + 技能收集器.py + start 脚本） |

---

## 六、编译器 (Compilers)

### 6.1 正式编译器
| 路径 | 说明 |
|------|------|
| `cnsh-core/cnsh-v2.1/` | CNSH v2.1 编译器（lexer/parser/compiler） |
| `cnsh-core/cnsh_unified.py` | 统一 API（DNA工具/数学工具/审计工具） |
| `03_compiler/` | 编译注册表（COMPILE-REGISTRY.local.jsonl） |

### 6.2 编辑器（含编译功能）
| 路径 | 说明 |
|------|------|
| `cnsh_editor/` | engine.py + \_\_init\_\_.py |
| `cnsh-editor/` | 含 cnsh_editor_engine_v2.0.py + cnsh_translator_engine_v2.0.py |
| `integrated-modules/cnsh_editor_api/` | 编辑器 API 服务（含 Dockerfile） |

---

## 七、Web 前端（3 个并行的操作台）

| 目录 | 文件数 | 说明 |
|------|--------|------|
| `web/` | 130 | Web 操作台 v4.0 + 3D 神经网络 v1/v2 |
| `portal/` | 131 | 对外官网 longhun888.com + P0 控制面板 29 个 |
| `control-panel/` | 19 | 操作台 API（端口 9622）+ Skill 调度 |
| `desktop/` | 5 | macOS 桌面主开关 |

**说明**: `web/` 和 `portal/` 结构高度对称，似乎前者是本地开发版，后者是生产版。

---

## 八、集成层 (Integrations & Bridges)

### 8.1 `integrations/` (155 文件)
| 子模块 | 说明 |
|--------|------|
| `mcp/` | CNSH MCP Server（13 工具）+ v4 MCP Server |
| `deepseek/` | DeepSeek API 客户端 |
| `fish_audio/` | Fish Audio TTS |
| `notion/` | Notion MVP 集成 + 哲学体系同步 |
| `wechat_public_account/` | 微信公众号全套系统（含小程序） |

### 8.2 `integrated-modules/` (77 文件)
| 子模块 | 说明 |
|--------|------|
| `kimi_agent/` | Kimi Agent 核心引擎 |
| `shame_pillar/` | 耻辱柱系统（50KB 核心 + 熔断协议 + 六誓引擎） |
| `skills.integrated/` | 10 技能集成标准 |
| `cnsh_editor_api/` | CNSH 编辑器 API |
| `gateway/` | Claude-Kimi 协作网关 |
| `monitoring/` | 移动端监控文档 |
| `sync/` | Brain-Notion 同步 |
| `protocols/` | CNSH v2.0 协议 + 保护 |
| `longhun_config/` | 主权环境配置 |
| `longhun_logging/` | 日志/版本/追踪系统 |

### 8.3 `bridges/`
- `deepseek_bridge.py` — DeepSeek API 本地桥接

---

## 九、监控 (Monitoring) — 3 处

| 目录 | 文件数 | 说明 |
|------|--------|------|
| `monitoring/` | 8 | 生产监控（Datadog + Prometheus + Grafana） |
| `monitoring.backup/` | 5 | 监控备份（与 monitoring/ 重复） |
| `mobile-monitoring.integrated/` | 36 | 移动端监控完整方案（前后端 SDK + 仪表板） |

---

## 十、其他独立子系统

| 目录 | 说明 |
|------|------|
| `baobao-guardian/` | 宝宝守护者（前后端分离，端口独立） |
| `xpay/` | 支付系统（含激励模型、多币种） |
| `chrome_extension/` | 浏览器扩展（background.js + popup） |
| `software_dna/` | 软件 DNA 加密/签名（10 子目录） |
| `software-dna/` | 软件 DNA v2（加密 + 扫描 + 测试） |
| `persona/` | 人格系统（25 文件：压缩引擎/审计日志/DNA追踪/洛书易经/德者永生殿） |
| `systems/` | 系统集合（agent-os/database/kfpp/metaverse/p0-foundation/v3） |
| `龍魂洛书369引擎/` | 369 数学体系（7 子模块） |
| `法律引擎/` | 法律条文检索引擎（API 服务器 + laws.json） |
| `龍魂取证内核/` | 取证工具集 |
| `longhun-font/` | 自主字体引擎（含 4 个 font_engine） |
| `wuxing-visual/` | 五行可视化 |
| `zeng-extraction/` | 曾提取（十维呼吸 + 网络渲染引擎） |
| `cnsh-terminal/` | CNSH 终端 v5.0（含多模态 CLI） |
| `cnsh_terminal_v5.0/` | CNSH 终端（另一个目录?） |
| `voice-dna/` | 声纹 DNA |
| `voice-twin/` | 声音孪生 |
| `rules-engine-v2.5/` | 规则引擎 v2.5（Notion 同步 + 批量处理） |
| `memory-universe/` | 记忆宇宙 |
| `second_brain/` | 第二大脑 |
| `second-brain/` | 第二大脑（另一个?） |

---

## 十一、入口点汇总

### 11.1 主要启动入口
| 文件 | 说明 |
|------|------|
| `龍魂体系v5-一键启动.py` | v5 一键启动（根目录） |
| `bin/longhun-launcher.py` | 统一启动器 |
| `bin/lh` | 快捷命令 |
| `control-panel/main.py` | 操作台后端（:9622） |
| `tools/longhun_neural_network_server.py` | 神经网络总控（:9627） |

### 11.2 其他 main.py 入口
- `phase3/backend/main.py`
- `scripts/main.py`
- `integrated-modules/cnsh_editor_api/main.py`
- `notion_absorb/main.py`
- `baobao-guardian/backend/app/main.py`

---

## 十二、治理协议 (Governance Protocols)

### 12.1 已激活协议

| 协议 | 文件 | 用途 | 状态 |
|------|------|------|------|
| KFPP | `L8_治理层/governance/KFPP_ACTIVATION_PROCLAMATION.md` | 知识流动纯净度协议 | 🟢 活跃 |
| **CLAP** | `L8_治理层/governance/CAPITAL_LOVE_AUDIT_PROTOCOL.md` | **资本愛之审计协议 v1.0** | 🟢 活跃 |

### 12.2 CLAP 资本愛之审计引擎

| 文件 | 用途 |
|------|------|
| `audit/capital_love_audit.py` | 资本愛之审计执行引擎 · 七维矩阵评分 · 四级准入判定 |
| `audit/reports/` | 季度审计报告输出目录 |
| `~/.longhun/audit/capital_love_audit.jsonl` | 追加式审计日志 |
| `~/.longhun/audit/capital_banned.json` | 永久禁入名单 |

### CLAP 核心原则
- 🔴 没有爱的资本 → 永久禁入
- 🟡 进来的资本 → 只配当服务商
- 🟢 主权不可让渡 · 中国法律唯一管辖权
- 🛡️ 得罪少数人 · 造福14亿人

### 12.3 v∞ 算法与协议家族（2026-07-06 归档）

| 文档 | 路径 | 用途 | 状态 |
|------|------|------|------|
| **INFINITE_GROWTH_ENGINE** | `L8_治理层/governance/INFINITE_GROWTH_ENGINE_v∞.md` | v∞无限智能增长引擎·四层循环+失控防护 | 🟡 待人审 |
| **IPA-DICT-101-111** | `01_protocols/IPA-DICT-101-111-决策链.md` | 循环触发·五行流转·11条决策链 | 🟢 通过 |
| **Democratic Reply** | `L2_技能层/skills/democratic-reply-calculator.md` | 民主回复计算函数·六维检查矩阵 | 🟢 通过 |
| **Weight Algo v3.1** | `L8_治理层/governance/tech-docs/LONGHUN-WEIGHT-ALGO-v3.1.md` | 龍魂权重算法·三层次解构·形式化证明 | 🟢 通过 |
| **Wuxing v2.0-v3.0** | `cnsh-core/wuxing/WUXING-CALCULATOR-v2.0-v3.0.md` | 五行计算器·四大指令·六门路由·对冲指数H | 🟢 通过 |
| **FLOW-CORE v3.0** | `cnsh-core/CNSH-FLOW-CORE-v3.0.md` | 流场压缩核·任意输入→流场节点 | 🟢 通过 |

**算法家族关系图：**
```
INFINITE_GROWTH_ENGINE (v∞ 主引擎)
  ├── IPA-DICT-101-111 (决策链协议)
  │     └── Democratic Reply (民主回复中间件)
  ├── LONGHUN-WEIGHT-ALGO v3.1 (数学基础)
  │     └── WUXING-CALCULATOR v2.0-v3.0 (五行计算)
  └── CNSH-FLOW-CORE v3.0 (流场压缩核·统一出口)
```

| 关联对 | 对接方式 |
|--------|----------|
| 决策链 ↔ 无限引擎 | 四层循环（微观/宏观/进化/超越）→ 引擎四层优化器 |
| 权重算法 ↔ 五行计算器 | 数字根→五行映射 + 对冲指数H → 天道系统分级 |
| 流场压缩核 ↔ 五行计算器 | 入口宇宙六门路由 + 生成节点统一格式 |
| 民主回复 ↔ 权重算法 | 六维检查中的权重与权重算法的太极公式共用数学根 |

---

### 12.4 铁律总目录·本地归档（2026-07-06）

| 文档 | 路径 | 用途 | 状态 |
|------|------|------|------|
| **P0 铁律总目录** | `L8_治理层/governance/IRON-LAWS/P0_ETERNAL_IRON_LAW_DIRECTORY.md` | 35 条主律+子律完整目录·九钻石伦理·六主权出口 | 🟢 已归档 |

原始来源：Notion P0 永恒页（UID9622 亲自焊接·v1.0-v3.5 版本日志完整）

---

### 12.5 本地 API 服务状态（2026-07-06 盘点）

| 服务 | 端口 | 状态 | 说明 |
|------|------|------|------|
| **Ollama** | :11434 | 🟢 在线 | 15 个模型已加载（qwen2.5:7b/14b/72b, cnsh-reactor v2.6, longhun-9622, Qwen3-8B, dolphin-mixtral 46.7B, chuxinzhiyi 72.7B, deepseek-v3.1:671b-cloud, deepseek-coder:6.7b 等） |
| **DeepSeek 中继桥** | :8788 | 🟢 在线 | bridge=deepseek, ollama_fallback 已就绪 |
| **主服务** | :9622 | 🟡 在线 | 服务在跑但无 /health 端点（返回 404） |
| **操作台** | :9625 | 🟢 在线 | 龍魂腦幹 v1.0 |
| **FAISS** | :8081 | 🔴 未启动 | 向量检索服务 |
| **Shield** | :8765 | 🔴 未启动 | 安全护盾服务 |

> 需要启动的服务：`FAISS (:8081)` `Shield (:8765)`

---

## 十三、收口行动计划

### 🔴 高优先级（重复/冲突）
| 问题 | 建议 |
|------|------|
| `skills.backup/` 与 `skills/` 重复 | 归档 `skills.backup/` |
| `monitoring.backup/` 与 `monitoring/` 重复 | 归档 `monitoring.backup/` |
| `cnsh_editor_engine_v2.0.py` × 3 份 | 保留 `cnsh-core/`，其余 import |
| `cnsh_translator_engine_v2.0.py` × 3 份 | 同上 |
| `longhun_skill_auto_completion_engine.py` × 4 份 | 同上 |
| `cnsh_font_engine*.py` × 4 份 | 保留最新，其余归档 |
| `audit_engine.py` × 2 (`engines/` vs `cnsh-core/engines/`) | 确认为同一文件或合并 |
| `DNA授权执行引擎.py` × 2 (`cnsh/` vs `cnsh.integrated/`) | 统一到 `cnsh/` |
| `longhun_compression_engine.py` × 2 (`scripts/` vs `persona/`) | 保留一个 |
| `software_dna/` vs `software-dna/` | 合并为单目录 |

### 🟡 中优先级（聚合）
| 问题 | 建议 |
|------|------|
| `web/` vs `portal/` 对称但分立 | 明确谁是生产版 |
| `cnsh-terminal/` vs `cnsh_terminal_v5.0/` | 保留一个 |
| `second_brain/` vs `second-brain/` | 保留一个 |
| 引擎散落在 30+ 个路径 | 统一 import 路径 |

### 🟢 低优先级（文档）
| 问题 | 建议 |
|------|------|
| 根目录 66 个报告 .md | 归档到 `05_系統報告/` |
| 429 个未跟踪新文件 | 分批审计后 add |

---

## 十四、统计总表

| 类别 | 权威位置 | 副本/冗余数 | 状态 |
|------|---------|------------|------|
| 技能定义 | `01_技能庫/` (5) → `skills/` (13+) | 1 份备份冗余 | 🟡 |
| 引擎 | `cnsh-core/` (8) + 散落 (36+) | 5-6 份多重重名 | 🔴 |
| 执行器 | `executors/` (5 子目录) + `bin/` (3) | — | 🟢 |
| Agent | `agents/` (10) + `.codebuddy/agents/` (1) | — | 🟢 |
| 内核 | 5 个独立内核目录 | — | 🟢 |
| 编译器 | `cnsh-core/cnsh-v2.1/` | — | 🟢 |
| 编辑器 | 3 个目录 | 有交叉 | 🟡 |
| Web 前端 | 3 个操作台 | web↔portal 对称 | 🟡 |
| 集成 | `integrations/` + `integrated-modules/` | — | 🟢 |
| 监控 | 3 处 | 1 份备份冗余 | 🟡 |
| 独立子系统 | 19 个 | — | 🟢 |

---

DNA: `#龍芯⚡️2026-07-06-MASTER-REGISTRY-SUBSYSTEMS-v3.3`

> v3.1 更新：新增 v∞ 算法协议家族（6 个文档）归档注册
> v3.2 更新：新增铁律总目录本地归档 + 修复 .codebuddy/agents 断链 + 本地 API 状态盘点
> v3.3 更新：五行映射全局对齐 — 数字根→五行统一为河图经典映射；IPA注册表修正；hetu_luoshu_dna.py 新增数字根转五行()

