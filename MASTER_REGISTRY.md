# 龍魂系统 · 统一子系统收口总表 v1.0

> DNA: `#龍芯⚡️2026-07-06-MASTER-REGISTRY-SUBSYSTEMS-v1.0`
> 收口人: CodeBuddy
> 审计: 🟢 通过
> 原则: 一个仓库，一份总表，不可有未注册的子系统

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

## 十二、收口行动计划

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

## 十三、统计总表

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

DNA: `#龍芯⚡️2026-07-06-MASTER-REGISTRY-SUBSYSTEMS-v1.0`
