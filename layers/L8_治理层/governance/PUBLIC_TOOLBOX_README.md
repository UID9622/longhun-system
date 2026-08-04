# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂工具箱 · LongHun Toolbox

> **中国自主可控的 AI 治理与本地主权工具集合**
>
> 用中文语义、中文命名规范、DNA 追溯、三色审计，打造属于我们自己的 AI 基础设施。

## 项目定位

龍魂工具箱不是「又一个工具集」，而是：

- **中文母语优先**：类名、函数名、注释、文档全部中文可读
- **本地主权**：数据根留本地，不依赖外网
- **DNA 追溯**：每个动作、每个文件都有可追溯的 DNA 签名
- **三色审计**：🟢 通过 / 🟡 提醒 / 🔴 熔断
- **自主可控**：龍芯 × 华为 × CNSH 融合底座

## 目录

- [项目定位](#项目定位)
- [核心模块速览](#核心模块速览)
- [隔离区说明](#隔离区说明)
- [工具清单](#工具清单)
- [快速开始](#快速开始)
- [贡献规范](#贡献规范)
- [主权声明](#主权声明)

## 核心模块速览

| 模块 | 路径 | 一句话说明 |
|---|---|---|
| 中文编辑器 | [`dev-env/chinese-editor`](dev-env/chinese-editor) | 闭环中文编辑开发环境：CNSH 脚本本地运行 + 龍魂字体 |
| 君子协议 | [`governance/longhun-trust-protocol`](governance/longhun-trust-protocol) | 诚信评级与违约清算算法：M/P/I 三维评分 + 杀猪机制 |
| CNSH 核心 | [`cnsh-core`](cnsh-core) | 中文原生脚本编译器、运行时、治理与审计 |
| 技能库 | [`01_技能库`](01_技能库) | 龍魂技能栈：部署、Kimi 集成、MCP、Notion、仓库审计等 |
| 脚本工具 | [`scripts`](scripts) | 日常治理脚本：DNA、知识图谱、Notion 同步、复盘等 |
| 多币种 | [`multicurrency`](multicurrency) / [`xpay`](xpay) | e-CNY / 多币种行情与交易演示 |
| 数字身份 | [`sovereignty`](sovereignty) | 国家数字身份主权认证入口（本地运行） |
| 数字人 | [`01_技能库/longhun-zeng-digital-human`](01_技能库/longhun-zeng-digital-human) | 曾老师数字人哲学 + 十维呼吸引擎 |

## 隔离区说明

敏感或外部导入的内容统一放入 [`_quarantine/`](_quarantine/)，由专属人格/本地模型管理，不进入公开发行版：

- `Kimi_Agent_龍魂協議自動化完成/`：外部导入，含硬编码密钥、Notion Schema、n8n 工作流。

## 工具清单


### `.`

- 📖 [QUICK_DNA_STATUS.sh](QUICK_DNA_STATUS.sh) — 状态: `HELP_OK`
- ✅ [__init__.py](__init__.py) — 状态: `IMPORT_OK`
- 📖 [brain_notion_sync.py](brain_notion_sync.py) — 状态: `HELP_OK`
- 🚀 [daily_review.py](daily_review.py) — 状态: `HAS_MAIN`
- ✔️ [deploy_persona_api.sh](deploy_persona_api.sh) — 状态: `SYNTAX_OK`
- ✅ [init_directories.py](init_directories.py) — 状态: `IMPORT_OK`
- 📖 [install-terminal.sh](install-terminal.sh) — 状态: `HELP_OK`
- ✔️ [install_longhun_daemon.sh](install_longhun_daemon.sh) — 状态: `SYNTAX_OK`
- 🚀 [longhun_mvp_executor_v1.0.py](longhun_mvp_executor_v1.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_setup_integration_v1.0.py](longhun_mvp_setup_integration_v1.0.py) — 状态: `HAS_MAIN`
- 📖 [longhun_persona_hub.py](longhun_persona_hub.py) — 状态: `HELP_OK`
- 🚀 [longhun_self_check_v1.0.py](longhun_self_check_v1.0.py) — 状态: `HAS_MAIN`
- 📖 [longhun_system_start_all.sh](longhun_system_start_all.sh) — 状态: `HELP_OK`
- ✔️ [longhun_system_startup_check.sh](longhun_system_startup_check.sh) — 状态: `SYNTAX_OK`
- ✔️ [protocol_shield.sh](protocol_shield.sh) — 状态: `SYNTAX_OK`
- 📖 [test-workflow.sh](test-workflow.sh) — 状态: `HELP_OK`
- 🚀 [test_audit_integration_v1.py](test_audit_integration_v1.py) — 状态: `HAS_MAIN`
- ✔️ [test_persona_api.sh](test_persona_api.sh) — 状态: `SYNTAX_OK`

### `01_protocols/downloads-imports/Kimi_Agent_龍魂協議自動化完成`

- ⚠️ 整个目录已隔离至 `_quarantine/Kimi_Agent_龍魂協議自動化完成/`（外部导入、含硬编码密钥/Notion Schema/n8n 工作流等敏感内容，不适合直接开源发布）

### `01_protocols/downloads-imports/龍魂协议双语版/龍魂系统-v3`

- ✔️ [一键安装.sh](01_protocols/downloads-imports/龍魂协议双语版/龍魂系统-v3/一键安装.sh) — 状态: `SYNTAX_OK`

### `01_protocols/downloads-imports/龍魂协议双语版/龍魂系统-v3/快捷命令`

- ⚙️ [启动人格代理.py](01_protocols/downloads-imports/龍魂协议双语版/龍魂系统-v3/快捷命令/启动人格代理.py) — 状态: `MAIN_NO_HELP`

### `01_protocols/downloads-imports/龍魂协议双语版/龍魂系统-v3/核心引擎`

- 📖 [规则引擎.py](01_protocols/downloads-imports/龍魂协议双语版/龍魂系统-v3/核心引擎/规则引擎.py) — 状态: `HELP_OK`

### `01_protocols/downloads-imports/龍魂协议双语版/龍魂系统-v3/语言修正`

- 📖 [漂移词修正器.py](01_protocols/downloads-imports/龍魂协议双语版/龍魂系统-v3/语言修正/漂移词修正器.py) — 状态: `HELP_OK`
- ⚙️ [规则导出工具.py](01_protocols/downloads-imports/龍魂协议双语版/龍魂系统-v3/语言修正/规则导出工具.py) — 状态: `MAIN_NO_HELP`

### `01_protocols/downloads-imports/龍魂協議焊死·立即行動方案`

- ✔️ [protocol_shield.sh](01_protocols/downloads-imports/龍魂協議焊死·立即行動方案/protocol_shield.sh) — 状态: `SYNTAX_OK`

### `01_技能库/downloads-imports/ 10 个 skill `

- 📖 [SKILL-LAUNCHER.sh](01_技能库/downloads-imports/ 10 个 skill /SKILL-LAUNCHER.sh) — 状态: `HELP_OK`
- 🚀 [skill-10-web-artifacts-builder.py](01_技能库/downloads-imports/ 10 个 skill /skill-10-web-artifacts-builder.py) — 状态: `HAS_MAIN`
- 🚀 [skill-6-mcp-builder.py](01_技能库/downloads-imports/ 10 个 skill /skill-6-mcp-builder.py) — 状态: `HAS_MAIN`
- 🚀 [skill-7-skill-creator.py](01_技能库/downloads-imports/ 10 个 skill /skill-7-skill-creator.py) — 状态: `HAS_MAIN`
- 🚀 [skill-8-slack-gif-creator.py](01_技能库/downloads-imports/ 10 个 skill /skill-8-slack-gif-creator.py) — 状态: `HAS_MAIN`
- 🚀 [skill-9-theme-factory.py](01_技能库/downloads-imports/ 10 个 skill /skill-9-theme-factory.py) — 状态: `HAS_MAIN`

### `01_技能库/downloads-imports/Kimi_Agent_启动全部技能`

- 🚀 [DNA追溯链系统_v3.0.py](01_技能库/downloads-imports/Kimi_Agent_启动全部技能/DNA追溯链系统_v3.0.py) — 状态: `HAS_MAIN`
- 📖 [SKILL-LAUNCHER.sh](01_技能库/downloads-imports/Kimi_Agent_启动全部技能/SKILL-LAUNCHER.sh) — 状态: `HELP_OK`
- 🚀 [三色审计与10道闸系统_v3.0.py](01_技能库/downloads-imports/Kimi_Agent_启动全部技能/三色审计与10道闸系统_v3.0.py) — 状态: `HAS_MAIN`
- 🚀 [五行融合决策引擎_v3.0.py](01_技能库/downloads-imports/Kimi_Agent_启动全部技能/五行融合决策引擎_v3.0.py) — 状态: `HAS_MAIN`
- 🚀 [人格矩阵路由系统_v3.0.py](01_技能库/downloads-imports/Kimi_Agent_启动全部技能/人格矩阵路由系统_v3.0.py) — 状态: `HAS_MAIN`
- 🚀 [安全域审计协议_v3.0.py](01_技能库/downloads-imports/Kimi_Agent_启动全部技能/安全域审计协议_v3.0.py) — 状态: `HAS_MAIN`

### `01_技能库/downloads-imports/龍魂 10 Skill 標準化完成`

- 🚀 [longhun-skill-auto-completion-engine.py](01_技能库/downloads-imports/龍魂 10 Skill 標準化完成/longhun-skill-auto-completion-engine.py) — 状态: `HAS_MAIN`
- 🚀 [longhun-standard-calculation-framework.py](01_技能库/downloads-imports/龍魂 10 Skill 標準化完成/longhun-standard-calculation-framework.py) — 状态: `HAS_MAIN`

### `01_技能库/longhun-cloud-deploy/scripts`

- 📖 [部署引擎.py](01_技能库/longhun-cloud-deploy/scripts/部署引擎.py) — 状态: `HELP_OK`

### `01_技能库/longhun-cloud-kimi/scripts`

- 📖 [Kimi集成器.py](01_技能库/longhun-cloud-kimi/scripts/Kimi集成器.py) — 状态: `HELP_OK`

### `01_技能库/longhun-cloud-mcp/scripts`

- 🚀 [MCP服務器.py](01_技能库/longhun-cloud-mcp/scripts/MCP服務器.py) — 状态: `HAS_MAIN`

### `01_技能库/longhun-cloud-notion/scripts`

- 📖 [Notion同步器.py](01_技能库/longhun-cloud-notion/scripts/Notion同步器.py) — 状态: `HELP_OK`

### `01_技能库/longhun-cloud-panel/scripts`

- 🚀 [操作台API.py](01_技能库/longhun-cloud-panel/scripts/操作台API.py) — 状态: `HAS_MAIN`

### `01_技能库/longhun-empower-engine/scripts`

- 🚀 [empower_engine_v2.py](01_技能库/longhun-empower-engine/scripts/empower_engine_v2.py) — 状态: `HAS_MAIN`
- 📖 [install.sh](01_技能库/longhun-empower-engine/scripts/install.sh) — 状态: `HELP_OK`
- 🚀 [longhun_api.py](01_技能库/longhun-empower-engine/scripts/longhun_api.py) — 状态: `HAS_MAIN`
- 🚀 [notion_reporter.py](01_技能库/longhun-empower-engine/scripts/notion_reporter.py) — 状态: `HAS_MAIN`

### `01_技能库/longhun-forensic-toolkit`

- ✔️ [verify.sh](01_技能库/longhun-forensic-toolkit/verify.sh) — 状态: `SYNTAX_OK`

### `01_技能库/longhun-kg-upgrade/scripts`

- ✔️ [install.sh](01_技能库/longhun-kg-upgrade/scripts/install.sh) — 状态: `SYNTAX_OK`

### `01_技能库/longhun-warehouse-audit/scripts`

- 📖 [audit_engine.py](01_技能库/longhun-warehouse-audit/scripts/audit_engine.py) — 状态: `HELP_OK`

### `01_技能库/longhun-zeng-digital-human/scripts`

- 🚀 [人格管理系统.py](01_技能库/longhun-zeng-digital-human/scripts/人格管理系统.py) — 状态: `HAS_MAIN`
- 🚀 [十维呼吸引擎.py](01_技能库/longhun-zeng-digital-human/scripts/十维呼吸引擎.py) — 状态: `HAS_MAIN`
- 📖 [启动数字人.py](01_技能库/longhun-zeng-digital-human/scripts/启动数字人.py) — 状态: `HELP_OK`
- 🚀 [存在性验证.py](01_技能库/longhun-zeng-digital-human/scripts/存在性验证.py) — 状态: `HAS_MAIN`
- 🚀 [数字人主控.py](01_技能库/longhun-zeng-digital-human/scripts/数字人主控.py) — 状态: `HAS_MAIN`
- 🚀 [网络渲染引擎.py](01_技能库/longhun-zeng-digital-human/scripts/网络渲染引擎.py) — 状态: `HAS_MAIN`
- 🚀 [航标灯系统.py](01_技能库/longhun-zeng-digital-human/scripts/航标灯系统.py) — 状态: `HAS_MAIN`

### `03_知識圖譜`

- 🚀 [build_cnsh_editor_module.py](03_知識圖譜/build_cnsh_editor_module.py) — 状态: `HAS_MAIN`
- 🚀 [compress_downloads_imports.py](03_知識圖譜/compress_downloads_imports.py) — 状态: `HAS_MAIN`
- 🚀 [generate_downloads_inbox.py](03_知識圖譜/generate_downloads_inbox.py) — 状态: `HAS_MAIN`
- 🚀 [migrate_downloads_inbox.py](03_知識圖譜/migrate_downloads_inbox.py) — 状态: `HAS_MAIN`

### `agents`

- 📖 [agent_daemon.py](agents/agent_daemon.py) — 状态: `HELP_OK`
- ✅ [agent_eco_adapter.py](agents/agent_eco_adapter.py) — 状态: `IMPORT_OK`
- 📖 [agent_status_reporter.py](agents/agent_status_reporter.py) — 状态: `HELP_OK`
- 🚀 [longhun_foundation_launcher_auto.py](agents/longhun_foundation_launcher_auto.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_notion_sync_auto.py](agents/longhun_notion_sync_auto.py) — 状态: `HAS_MAIN`
- 🚀 [orchestrator.py](agents/orchestrator.py) — 状态: `HAS_MAIN`
- 🚀 [task_executor_live_v1.py](agents/task_executor_live_v1.py) — 状态: `HAS_MAIN`
- 🚀 [xpay_core_auto.py](agents/xpay_core_auto.py) — 状态: `HAS_MAIN`

### `agents/downloads-imports/龍魂网关/LongHun_Complete_Ecosystem_v1.0`

- 🚀 [LongHun_Ecosystem_Complete_Implementation_v1.0.py](agents/downloads-imports/龍魂网关/LongHun_Complete_Ecosystem_v1.0/LongHun_Ecosystem_Complete_Implementation_v1.0.py) — 状态: `HAS_MAIN`
- 🚀 [LongHun_Ecosystem_Standalone_v1.0.py](agents/downloads-imports/龍魂网关/LongHun_Complete_Ecosystem_v1.0/LongHun_Ecosystem_Standalone_v1.0.py) — 状态: `HAS_MAIN`
- 🚀 [XPay_Complete_Implementation_v1.0.py](agents/downloads-imports/龍魂网关/LongHun_Complete_Ecosystem_v1.0/XPay_Complete_Implementation_v1.0.py) — 状态: `HAS_MAIN`

### `agents/downloads-imports/龍魂自动化启动`

- ✔️ [longhun_launcher.sh](agents/downloads-imports/龍魂自动化启动/longhun_launcher.sh) — 状态: `SYNTAX_OK`
- 📖 [setup_longhun_alias.sh](agents/downloads-imports/龍魂自动化启动/setup_longhun_alias.sh) — 状态: `HELP_OK`

### `android-auto`

- ✔️ [termux-setup.sh](android-auto/termux-setup.sh) — 状态: `SYNTAX_OK`

### `baobao-guardian`

- ✔️ [start.sh](baobao-guardian/start.sh) — 状态: `SYNTAX_OK`
- 📖 [verify-structure.sh](baobao-guardian/verify-structure.sh) — 状态: `HELP_OK`

### `baobao-guardian/backend/app`

- 🚀 [main.py](baobao-guardian/backend/app/main.py) — 状态: `HAS_MAIN`

### `brain`

- 📖 [behavior_notion_sync.py](brain/behavior_notion_sync.py) — 状态: `HELP_OK`

### `cnsh-core`

- ✅ [__init__.py](cnsh-core/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [api_wuxing.py](cnsh-core/api_wuxing.py) — 状态: `HAS_MAIN`
- 🚀 [audit_3color_v1.py](cnsh-core/audit_3color_v1.py) — 状态: `HAS_MAIN`
- 🚀 [audit_integration_v1.py](cnsh-core/audit_integration_v1.py) — 状态: `HAS_MAIN`
- 🚀 [core_system_launcher.py](cnsh-core/core_system_launcher.py) — 状态: `HAS_MAIN`
- 🚀 [dna_sovereignty_kernel.py](cnsh-core/dna_sovereignty_kernel.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_instruction_executor.py](cnsh-core/longhun_instruction_executor.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_plain_guide.py](cnsh-core/longhun_plain_guide.py) — 状态: `HAS_MAIN`
- 🚀 [m04_yijing_engine.py](cnsh-core/m04_yijing_engine.py) — 状态: `HAS_MAIN`
- 🚀 [m05_wuxing_calculator.py](cnsh-core/m05_wuxing_calculator.py) — 状态: `HAS_MAIN`
- 🚀 [memory_pack_v3.py](cnsh-core/memory_pack_v3.py) — 状态: `HAS_MAIN`
- 🚀 [notion_task5_setup.py](cnsh-core/notion_task5_setup.py) — 状态: `HAS_MAIN`
- 📖 [parse_notion.py](cnsh-core/parse_notion.py) — 状态: `HELP_OK`
- 🚀 [people_behavior_engine.py](cnsh-core/people_behavior_engine.py) — 状态: `HAS_MAIN`
- 🚀 [people_rights_guard.py](cnsh-core/people_rights_guard.py) — 状态: `HAS_MAIN`
- 🚀 [people_skill_scope.py](cnsh-core/people_skill_scope.py) — 状态: `HAS_MAIN`
- 🚀 [task_executor_v9_integrated.py](cnsh-core/task_executor_v9_integrated.py) — 状态: `HAS_MAIN`
- ✅ [v9_system_integration_bridge.py](cnsh-core/v9_system_integration_bridge.py) — 状态: `IMPORT_OK`
- 🚀 [v9_task_executor_adapter.py](cnsh-core/v9_task_executor_adapter.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup`

- 🚀 [api_wuxing.py](cnsh-core.backup/api_wuxing.py) — 状态: `HAS_MAIN`
- 🚀 [audit_3color_v1.py](cnsh-core.backup/audit_3color_v1.py) — 状态: `HAS_MAIN`
- 🚀 [audit_integration_v1.py](cnsh-core.backup/audit_integration_v1.py) — 状态: `HAS_MAIN`
- 🚀 [core_system_launcher.py](cnsh-core.backup/core_system_launcher.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_instruction_executor.py](cnsh-core.backup/longhun_instruction_executor.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_plain_guide.py](cnsh-core.backup/longhun_plain_guide.py) — 状态: `HAS_MAIN`
- 🚀 [m04_yijing_engine.py](cnsh-core.backup/m04_yijing_engine.py) — 状态: `HAS_MAIN`
- 🚀 [m05_wuxing_calculator.py](cnsh-core.backup/m05_wuxing_calculator.py) — 状态: `HAS_MAIN`
- 🚀 [memory_pack_v3.py](cnsh-core.backup/memory_pack_v3.py) — 状态: `HAS_MAIN`
- 🚀 [notion_task5_setup.py](cnsh-core.backup/notion_task5_setup.py) — 状态: `HAS_MAIN`
- 📖 [parse_notion.py](cnsh-core.backup/parse_notion.py) — 状态: `HELP_OK`

### `cnsh-core.backup/ai-tools/longhu_sentinel_bot`

- 📖 [sentinel_bot.py](cnsh-core.backup/ai-tools/longhu_sentinel_bot/sentinel_bot.py) — 状态: `HELP_OK`
- ✔️ [start_sentinel.sh](cnsh-core.backup/ai-tools/longhu_sentinel_bot/start_sentinel.sh) — 状态: `SYNTAX_OK`
- ✅ [telegram_handler.py](cnsh-core.backup/ai-tools/longhu_sentinel_bot/telegram_handler.py) — 状态: `IMPORT_OK`

### `cnsh-core.backup/ai-tools/operation_log_engine/core`

- ✅ [__init__.py](cnsh-core.backup/ai-tools/operation_log_engine/core/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [cross_device_identifier.py](cnsh-core.backup/ai-tools/operation_log_engine/core/cross_device_identifier.py) — 状态: `HAS_MAIN`
- 🚀 [dna_particle_generator.py](cnsh-core.backup/ai-tools/operation_log_engine/core/dna_particle_generator.py) — 状态: `HAS_MAIN`
- 🚀 [habit_fingerprint_manager.py](cnsh-core.backup/ai-tools/operation_log_engine/core/habit_fingerprint_manager.py) — 状态: `HAS_MAIN`
- 🚀 [multisig_gate.py](cnsh-core.backup/ai-tools/operation_log_engine/core/multisig_gate.py) — 状态: `HAS_MAIN`
- 🚀 [operation_ledger.py](cnsh-core.backup/ai-tools/operation_log_engine/core/operation_ledger.py) — 状态: `HAS_MAIN`
- 🚀 [query_tool.py](cnsh-core.backup/ai-tools/operation_log_engine/core/query_tool.py) — 状态: `HAS_MAIN`
- 🚀 [sync_engine.py](cnsh-core.backup/ai-tools/operation_log_engine/core/sync_engine.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/ai-tools/operation_log_engine/operation_log_engine`

- ✅ [__init__.py](cnsh-core.backup/ai-tools/operation_log_engine/operation_log_engine/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [cli.py](cnsh-core.backup/ai-tools/operation_log_engine/operation_log_engine/cli.py) — 状态: `HAS_MAIN`
- ✅ [config.py](cnsh-core.backup/ai-tools/operation_log_engine/operation_log_engine/config.py) — 状态: `IMPORT_OK`
- ✅ [encryption_enforce.py](cnsh-core.backup/ai-tools/operation_log_engine/operation_log_engine/encryption_enforce.py) — 状态: `IMPORT_OK`
- ✅ [logging_config.py](cnsh-core.backup/ai-tools/operation_log_engine/operation_log_engine/logging_config.py) — 状态: `IMPORT_OK`

### `cnsh-core.backup/brain`

- 📖 [longhun_brain.py](cnsh-core.backup/brain/longhun_brain.py) — 状态: `HELP_OK`

### `cnsh-core.backup/compiler`

- ✅ [audit.py](cnsh-core.backup/compiler/audit.py) — 状态: `IMPORT_OK`
- ✅ [compiler_node.py](cnsh-core.backup/compiler/compiler_node.py) — 状态: `IMPORT_OK`

### `cnsh-core.backup/constitution`

- 🚀 [longhun_foundation_config.py](cnsh-core.backup/constitution/longhun_foundation_config.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/dna`

- 🚀 [dna_system.py](cnsh-core.backup/dna/dna_system.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/engines`

- 🚀 [audit_engine.py](cnsh-core.backup/engines/audit_engine.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/gateway`

- 🚀 [cnsh_gateway.py](cnsh-core.backup/gateway/cnsh_gateway.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/governance`

- 🚀 [f1_through_f7_verifier.py](cnsh-core.backup/governance/f1_through_f7_verifier.py) — 状态: `HAS_MAIN`
- 🚀 [sovereignty_index.py](cnsh-core.backup/governance/sovereignty_index.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/identity`

- 🚀 [identity_verification.py](cnsh-core.backup/identity/identity_verification.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/language`

- ✔️ [编译运行.sh](cnsh-core.backup/language/编译运行.sh) — 状态: `SYNTAX_OK`
- 📖 [设置-cnsh文件关联.sh](cnsh-core.backup/language/设置-cnsh文件关联.sh) — 状态: `HELP_OK`

### `cnsh-core.backup/logging`

- 🚀 [append_only_logging.py](cnsh-core.backup/logging/append_only_logging.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/mathematics`

- 🚀 [formula_core.py](cnsh-core.backup/mathematics/formula_core.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/memory`

- 🚀 [cognitive_dna_particles.py](cnsh-core.backup/memory/cognitive_dna_particles.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/permissions`

- 🚀 [rbac_system.py](cnsh-core.backup/permissions/rbac_system.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/registry`

- 🚀 [node.py](cnsh-core.backup/registry/node.py) — 状态: `HAS_MAIN`
- 🚀 [route_registry.py](cnsh-core.backup/registry/route_registry.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/router`

- 🚀 [__init__.py](cnsh-core.backup/router/__init__.py) — 状态: `HAS_MAIN`
- 🚀 [execution_router.py](cnsh-core.backup/router/execution_router.py) — 状态: `HAS_MAIN`
- 🚀 [integration_test_persona_f4.py](cnsh-core.backup/router/integration_test_persona_f4.py) — 状态: `HAS_MAIN`
- 🚀 [persona_router.py](cnsh-core.backup/router/persona_router.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/rules`

- 🚀 [builtin_rules.py](cnsh-core.backup/rules/builtin_rules.py) — 状态: `HAS_MAIN`
- 🚀 [rule_node.py](cnsh-core.backup/rules/rule_node.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/runtime-governance`

- 📖 [brain_sync.py](cnsh-core.backup/runtime-governance/brain_sync.py) — 状态: `HELP_OK`
- 🚀 [cnsh_runtime_core.py](cnsh-core.backup/runtime-governance/cnsh_runtime_core.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/scheduler`

- 🚀 [execution_schedule.py](cnsh-core.backup/scheduler/execution_schedule.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/wuxing`

- 🚀 [longhun_wuxing_mvp.py](cnsh-core.backup/wuxing/longhun_wuxing_mvp.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/wuxing_calculator`

- 🚀 [calculator.py](cnsh-core.backup/wuxing_calculator/calculator.py) — 状态: `HAS_MAIN`

### `cnsh-core.backup/龍魂-决策流场-自动化优化`

- 🚀 [dna_validator.py](cnsh-core.backup/龍魂-决策流场-自动化优化/dna_validator.py) — 状态: `HAS_MAIN`
- 🚀 [index_resolver.py](cnsh-core.backup/龍魂-决策流场-自动化优化/index_resolver.py) — 状态: `HAS_MAIN`
- 🚀 [notion_sync_checker.py](cnsh-core.backup/龍魂-决策流场-自动化优化/notion_sync_checker.py) — 状态: `HAS_MAIN`
- 🚀 [term_translator.py](cnsh-core.backup/龍魂-决策流场-自动化优化/term_translator.py) — 状态: `HAS_MAIN`

### `cnsh-core/ai-tools/longhu_sentinel_bot`

- ⚙️ [sentinel_bot.py](cnsh-core/ai-tools/longhu_sentinel_bot/sentinel_bot.py) — 状态: `MAIN_NO_HELP`
- ✔️ [start_sentinel.sh](cnsh-core/ai-tools/longhu_sentinel_bot/start_sentinel.sh) — 状态: `SYNTAX_OK`
- ✅ [telegram_handler.py](cnsh-core/ai-tools/longhu_sentinel_bot/telegram_handler.py) — 状态: `IMPORT_OK`

### `cnsh-core/ai-tools/operation_log_engine/core`

- ✅ [__init__.py](cnsh-core/ai-tools/operation_log_engine/core/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [cross_device_identifier.py](cnsh-core/ai-tools/operation_log_engine/core/cross_device_identifier.py) — 状态: `HAS_MAIN`
- 🚀 [dna_particle_generator.py](cnsh-core/ai-tools/operation_log_engine/core/dna_particle_generator.py) — 状态: `HAS_MAIN`
- 🚀 [habit_fingerprint_manager.py](cnsh-core/ai-tools/operation_log_engine/core/habit_fingerprint_manager.py) — 状态: `HAS_MAIN`
- 🚀 [multisig_gate.py](cnsh-core/ai-tools/operation_log_engine/core/multisig_gate.py) — 状态: `HAS_MAIN`
- 🚀 [operation_ledger.py](cnsh-core/ai-tools/operation_log_engine/core/operation_ledger.py) — 状态: `HAS_MAIN`
- 🚀 [query_tool.py](cnsh-core/ai-tools/operation_log_engine/core/query_tool.py) — 状态: `HAS_MAIN`
- 🚀 [sync_engine.py](cnsh-core/ai-tools/operation_log_engine/core/sync_engine.py) — 状态: `HAS_MAIN`

### `cnsh-core/ai-tools/operation_log_engine/operation_log_engine`

- ✅ [__init__.py](cnsh-core/ai-tools/operation_log_engine/operation_log_engine/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [cli.py](cnsh-core/ai-tools/operation_log_engine/operation_log_engine/cli.py) — 状态: `HAS_MAIN`
- ✅ [config.py](cnsh-core/ai-tools/operation_log_engine/operation_log_engine/config.py) — 状态: `IMPORT_OK`
- ✅ [encryption_enforce.py](cnsh-core/ai-tools/operation_log_engine/operation_log_engine/encryption_enforce.py) — 状态: `IMPORT_OK`
- ✅ [logging_config.py](cnsh-core/ai-tools/operation_log_engine/operation_log_engine/logging_config.py) — 状态: `IMPORT_OK`

### `cnsh-core/api/longhun-api`

- 🚀 [龍魂系统_API接口完整实现_v1.0.py](cnsh-core/api/longhun-api/龍魂系统_API接口完整实现_v1.0.py) — 状态: `HAS_MAIN`

### `cnsh-core/brain`

- 📖 [longhun_brain.py](cnsh-core/brain/longhun_brain.py) — 状态: `HELP_OK`

### `cnsh-core/cnsh-runtime`

- 📖 [cnsh_runner.py](cnsh-core/cnsh-runtime/cnsh_runner.py) — 状态: `HELP_OK`

### `cnsh-core/compiler`

- ✅ [__init__.py](cnsh-core/compiler/__init__.py) — 状态: `IMPORT_OK`
- ✅ [audit.py](cnsh-core/compiler/audit.py) — 状态: `IMPORT_OK`
- ✅ [cnsh_compiler.py](cnsh-core/compiler/cnsh_compiler.py) — 状态: `IMPORT_OK`
- ✅ [codegen.py](cnsh-core/compiler/codegen.py) — 状态: `IMPORT_OK`
- ✅ [compiler_node.py](cnsh-core/compiler/compiler_node.py) — 状态: `IMPORT_OK`
- ✅ [lexer.py](cnsh-core/compiler/lexer.py) — 状态: `IMPORT_OK`
- ✅ [optimizer.py](cnsh-core/compiler/optimizer.py) — 状态: `IMPORT_OK`
- ✅ [parser.py](cnsh-core/compiler/parser.py) — 状态: `IMPORT_OK`
- ✅ [semantic.py](cnsh-core/compiler/semantic.py) — 状态: `IMPORT_OK`

### `cnsh-core/constitution`

- 🚀 [longhun_foundation_config.py](cnsh-core/constitution/longhun_foundation_config.py) — 状态: `HAS_MAIN`

### `cnsh-core/dna`

- ✅ [__init__.py](cnsh-core/dna/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [dna_system.py](cnsh-core/dna/dna_system.py) — 状态: `HAS_MAIN`

### `cnsh-core/downloads-imports/ 龍魂系統 · CNSH 語義接入規範 v2.0`

- 🚀 [longhun_protocol_resident_script_framework.py](cnsh-core/downloads-imports/ 龍魂系統 · CNSH 語義接入規範 v2.0/longhun_protocol_resident_script_framework.py) — 状态: `HAS_MAIN`

### `cnsh-core/downloads-imports/formula/新视觉计算公式`

- 🚀 [riemann_hypothesis_phase1_framework.py](cnsh-core/downloads-imports/formula/新视觉计算公式/riemann_hypothesis_phase1_framework.py) — 状态: `HAS_MAIN`

### `cnsh-core/downloads-imports/formula/计算公式`

- 🚀 [benchmark_formula_system.py](cnsh-core/downloads-imports/formula/计算公式/benchmark_formula_system.py) — 状态: `HAS_MAIN`
- 🚀 [benchmark_no_audit.py](cnsh-core/downloads-imports/formula/计算公式/benchmark_no_audit.py) — 状态: `HAS_MAIN`
- 🚀 [formula_catalog_v1_0.py](cnsh-core/downloads-imports/formula/计算公式/formula_catalog_v1_0.py) — 状态: `HAS_MAIN`
- 🚀 [formula_chain.py](cnsh-core/downloads-imports/formula/计算公式/formula_chain.py) — 状态: `HAS_MAIN`
- 🚀 [formula_chain_v2.py](cnsh-core/downloads-imports/formula/计算公式/formula_chain_v2.py) — 状态: `HAS_MAIN`
- 🚀 [formula_core.py](cnsh-core/downloads-imports/formula/计算公式/formula_core.py) — 状态: `HAS_MAIN`
- 🚀 [formula_core_v2.py](cnsh-core/downloads-imports/formula/计算公式/formula_core_v2.py) — 状态: `HAS_MAIN`
- 🚀 [formula_manifest_complete_v1_0.py](cnsh-core/downloads-imports/formula/计算公式/formula_manifest_complete_v1_0.py) — 状态: `HAS_MAIN`
- 🚀 [wuxing_complete_system.py](cnsh-core/downloads-imports/formula/计算公式/wuxing_complete_system.py) — 状态: `HAS_MAIN`
- 🚀 [wuxing_formula_v1.py](cnsh-core/downloads-imports/formula/计算公式/wuxing_formula_v1.py) — 状态: `HAS_MAIN`
- 🚀 [wuxing_module_e_hexagram.py](cnsh-core/downloads-imports/formula/计算公式/wuxing_module_e_hexagram.py) — 状态: `HAS_MAIN`
- 🚀 [wuxing_module_f_supply.py](cnsh-core/downloads-imports/formula/计算公式/wuxing_module_f_supply.py) — 状态: `HAS_MAIN`
- 🚀 [wuxing_module_g_monitoring.py](cnsh-core/downloads-imports/formula/计算公式/wuxing_module_g_monitoring.py) — 状态: `HAS_MAIN`
- 🚀 [wuxing_module_h_batch.py](cnsh-core/downloads-imports/formula/计算公式/wuxing_module_h_batch.py) — 状态: `HAS_MAIN`
- 🚀 [wuxing_module_i_knowledge_graph.py](cnsh-core/downloads-imports/formula/计算公式/wuxing_module_i_knowledge_graph.py) — 状态: `HAS_MAIN`

### `cnsh-core/engines`

- 🚀 [audit_engine.py](cnsh-core/engines/audit_engine.py) — 状态: `HAS_MAIN`

### `cnsh-core/gateway`

- 🚀 [cnsh_gateway.py](cnsh-core/gateway/cnsh_gateway.py) — 状态: `HAS_MAIN`

### `cnsh-core/governance`

- 🚀 [f1_through_f7_verifier.py](cnsh-core/governance/f1_through_f7_verifier.py) — 状态: `HAS_MAIN`
- 📖 [layered_governance_engine.py](cnsh-core/governance/layered_governance_engine.py) — 状态: `HELP_OK`
- 🚀 [sovereignty_index.py](cnsh-core/governance/sovereignty_index.py) — 状态: `HAS_MAIN`

### `cnsh-core/identity`

- 🚀 [identity_verification.py](cnsh-core/identity/identity_verification.py) — 状态: `HAS_MAIN`

### `cnsh-core/language`

- ✔️ [编译运行.sh](cnsh-core/language/编译运行.sh) — 状态: `SYNTAX_OK`
- 📖 [设置-cnsh文件关联.sh](cnsh-core/language/设置-cnsh文件关联.sh) — 状态: `HELP_OK`

### `cnsh-core/longhun_logging`

- ✅ [__init__.py](cnsh-core/longhun_logging/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [append_only_logging.py](cnsh-core/longhun_logging/append_only_logging.py) — 状态: `HAS_MAIN`

### `cnsh-core/mathematics`

- ✅ [__init__.py](cnsh-core/mathematics/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [formula_comparison_table.py](cnsh-core/mathematics/formula_comparison_table.py) — 状态: `HAS_MAIN`
- 🚀 [formula_core.py](cnsh-core/mathematics/formula_core.py) — 状态: `HAS_MAIN`

### `cnsh-core/memory`

- 🚀 [cognitive_dna_particles.py](cnsh-core/memory/cognitive_dna_particles.py) — 状态: `HAS_MAIN`

### `cnsh-core/permissions`

- ✅ [__init__.py](cnsh-core/permissions/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [rbac_system.py](cnsh-core/permissions/rbac_system.py) — 状态: `HAS_MAIN`

### `cnsh-core/registry`

- ✅ [__init__.py](cnsh-core/registry/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [node.py](cnsh-core/registry/node.py) — 状态: `HAS_MAIN`
- 🚀 [route_registry.py](cnsh-core/registry/route_registry.py) — 状态: `HAS_MAIN`

### `cnsh-core/router`

- 🚀 [__init__.py](cnsh-core/router/__init__.py) — 状态: `HAS_MAIN`
- 🚀 [execution_router.py](cnsh-core/router/execution_router.py) — 状态: `HAS_MAIN`
- 🚀 [integration_test_persona_f4.py](cnsh-core/router/integration_test_persona_f4.py) — 状态: `HAS_MAIN`
- 🚀 [persona_router.py](cnsh-core/router/persona_router.py) — 状态: `HAS_MAIN`
- 🚀 [platform_persona_router.py](cnsh-core/router/platform_persona_router.py) — 状态: `HAS_MAIN`

### `cnsh-core/rules`

- ✅ [__init__.py](cnsh-core/rules/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [builtin_rules.py](cnsh-core/rules/builtin_rules.py) — 状态: `HAS_MAIN`
- ✅ [rule_engine.py](cnsh-core/rules/rule_engine.py) — 状态: `IMPORT_OK`
- ✅ [rule_executor.py](cnsh-core/rules/rule_executor.py) — 状态: `IMPORT_OK`
- 🚀 [rule_node.py](cnsh-core/rules/rule_node.py) — 状态: `HAS_MAIN`

### `cnsh-core/runtime-governance`

- ⚙️ [brain_sync.py](cnsh-core/runtime-governance/brain_sync.py) — 状态: `MAIN_NO_HELP`
- 🚀 [cnsh_runtime_core.py](cnsh-core/runtime-governance/cnsh_runtime_core.py) — 状态: `HAS_MAIN`

### `cnsh-core/scheduler`

- ✅ [__init__.py](cnsh-core/scheduler/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [execution_schedule.py](cnsh-core/scheduler/execution_schedule.py) — 状态: `HAS_MAIN`
- 📖 [heaven_cli.py](cnsh-core/scheduler/heaven_cli.py) — 状态: `HELP_OK`
- 🚀 [heaven_duty_engine.py](cnsh-core/scheduler/heaven_duty_engine.py) — 状态: `HAS_MAIN`

### `cnsh-core/tests`

- 🚀 [test_behavior_integration.py](cnsh-core/tests/test_behavior_integration.py) — 状态: `HAS_MAIN`
- 🚀 [test_dna_sovereignty_integration.py](cnsh-core/tests/test_dna_sovereignty_integration.py) — 状态: `HAS_MAIN`
- 🚀 [test_people_rights_integration.py](cnsh-core/tests/test_people_rights_integration.py) — 状态: `HAS_MAIN`
- 🚀 [test_skill_scope_integration.py](cnsh-core/tests/test_skill_scope_integration.py) — 状态: `HAS_MAIN`

### `cnsh-core/tools`

- 🚀 [behavior_cli.py](cnsh-core/tools/behavior_cli.py) — 状态: `HAS_MAIN`
- 🚀 [export_user_data.py](cnsh-core/tools/export_user_data.py) — 状态: `HAS_MAIN`
- 🚀 [founder_trip.py](cnsh-core/tools/founder_trip.py) — 状态: `HAS_MAIN`
- 📖 [skill_scope_cli.py](cnsh-core/tools/skill_scope_cli.py) — 状态: `HELP_OK`

### `cnsh-core/wuxing`

- 🚀 [longhun_wuxing_mvp.py](cnsh-core/wuxing/longhun_wuxing_mvp.py) — 状态: `HAS_MAIN`
- 🚀 [wuxing_calc_optimizations.py](cnsh-core/wuxing/wuxing_calc_optimizations.py) — 状态: `HAS_MAIN`

### `cnsh-core/wuxing_calculator`

- ✅ [__init__.py](cnsh-core/wuxing_calculator/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [calculator.py](cnsh-core/wuxing_calculator/calculator.py) — 状态: `HAS_MAIN`

### `cnsh-core/龍魂-决策流场-自动化优化`

- 🚀 [dna_validator.py](cnsh-core/龍魂-决策流场-自动化优化/dna_validator.py) — 状态: `HAS_MAIN`
- 🚀 [index_resolver.py](cnsh-core/龍魂-决策流场-自动化优化/index_resolver.py) — 状态: `HAS_MAIN`
- 🚀 [notion_sync_checker.py](cnsh-core/龍魂-决策流场-自动化优化/notion_sync_checker.py) — 状态: `HAS_MAIN`
- 🚀 [term_translator.py](cnsh-core/龍魂-决策流场-自动化优化/term_translator.py) — 状态: `HAS_MAIN`

### `cnsh-editor/ui`

- 🚀 [editor_ui.py](cnsh-editor/ui/editor_ui.py) — 状态: `HAS_MAIN`

### `cnsh-repo-push`

- 🚀 [cnsh_compiler.py](cnsh-repo-push/cnsh_compiler.py) — 状态: `HAS_MAIN`

### `cnsh-repo-push/dna-tracking`

- 🚀 [dna-ecny-activation.py](cnsh-repo-push/dna-tracking/dna-ecny-activation.py) — 状态: `HAS_MAIN`

### `cnsh-repo-push/longhun-system/🔧 AI技术架构分析中心`

- 📖 [IW-ECB-Western-Ethics-compile.sh](cnsh-repo-push/longhun-system/🔧 AI技术架构分析中心/IW-ECB-Western-Ethics-compile.sh) — 状态: `HELP_OK`
- 📖 [V9-GameTheory-compile.sh](cnsh-repo-push/longhun-system/🔧 AI技术架构分析中心/V9-GameTheory-compile.sh) — 状态: `HELP_OK`
- 🚀 [用户留痕核心.py](cnsh-repo-push/longhun-system/🔧 AI技术架构分析中心/用户留痕核心.py) — 状态: `HAS_MAIN`

### `cnsh-terminal`

- 📖 [cnsh_terminal_v5.py](cnsh-terminal/cnsh_terminal_v5.py) — 状态: `HELP_OK`
- 📖 [multimodal_cli.py](cnsh-terminal/multimodal_cli.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6`

- 📖 [_v6_upgrade_orchestrator.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/_v6_upgrade_orchestrator.py) — 状态: `HELP_OK`
- 📖 [baobao_workflow_v2.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/baobao_workflow_v2.0.py) — 状态: `HELP_OK`
- 🚀 [cnsh_aligner_v2.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/cnsh_aligner_v2.0.py) — 状态: `HAS_MAIN`
- 📖 [cnsh_translator_engine_v2.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/cnsh_translator_engine_v2.0.py) — 状态: `HELP_OK`
- 🚀 [content_sovereignty_protocol_v2.1.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/content_sovereignty_protocol_v2.1.py) — 状态: `HAS_MAIN`
- 📖 [longhun-v6-launcher.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v6-launcher.py) — 状态: `HELP_OK`
- 🚀 [longhun_file_audit_foundation_v2.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun_file_audit_foundation_v2.0.py) — 状态: `HAS_MAIN`
- 📖 [longhun_foundation_launcher_v2.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun_foundation_launcher_v2.0.py) — 状态: `HELP_OK`
- 📖 [longhun_script_manager_v2.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun_script_manager_v2.0.py) — 状态: `HELP_OK`
- 🚀 [龍魂体系v5-一键启动.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/龍魂体系v5-一键启动.py) — 状态: `HAS_MAIN`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/CNSH/compliance_china/compliance_china`

- 🚀 [个保法检查器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/CNSH/compliance_china/compliance_china/个保法检查器.py) — 状态: `HAS_MAIN`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/cnsh_terminal_v5.0`

- 📖 [cnsh_terminal_v5.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/cnsh_terminal_v5.0/cnsh_terminal_v5.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/cnsh_terminal_v5.0/modules`

- ✅ [__init__.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/cnsh_terminal_v5.0/modules/__init__.py) — 状态: `IMPORT_OK`
- ✅ [four_layer_check.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/cnsh_terminal_v5.0/modules/four_layer_check.py) — 状态: `IMPORT_OK`
- 🚀 [lexer.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/cnsh_terminal_v5.0/modules/lexer.py) — 状态: `HAS_MAIN`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/cnsh_terminal_v5.0/modules/voice`

- 🚀 [龍魂语音识别器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/cnsh_terminal_v5.0/modules/voice/龍魂语音识别器.py) — 状态: `HAS_MAIN`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/cnsh_terminal_v5.0/modules/感知中枢`

- 🚀 [通心译扩展术语表.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/cnsh_terminal_v5.0/modules/感知中枢/通心译扩展术语表.py) — 状态: `HAS_MAIN`
- 🚀 [龍魂多模态感知中枢.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/cnsh_terminal_v5.0/modules/感知中枢/龍魂多模态感知中枢.py) — 状态: `HAS_MAIN`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-automation/scripts`

- 📖 [自动化评估.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-automation/scripts/自动化评估.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-cloud-deploy/scripts`

- 📖 [k8s控制器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-cloud-deploy/scripts/k8s控制器.py) — 状态: `HELP_OK`
- 📖 [健康檢查.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-cloud-deploy/scripts/健康檢查.py) — 状态: `HELP_OK`
- 📖 [回滚系統.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-cloud-deploy/scripts/回滚系統.py) — 状态: `HELP_OK`
- 📖 [部署引擎.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-cloud-deploy/scripts/部署引擎.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-cloud-kimi/scripts`

- 📖 [Kimi集成器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-cloud-kimi/scripts/Kimi集成器.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-cloud-mcp/scripts`

- 🚀 [MCP服務器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-cloud-mcp/scripts/MCP服務器.py) — 状态: `HAS_MAIN`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-cloud-notion/scripts`

- 📖 [Notion同步器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-cloud-notion/scripts/Notion同步器.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-cloud-panel/scripts`

- 🚀 [操作台API.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-cloud-panel/scripts/操作台API.py) — 状态: `HAS_MAIN`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-integration/scripts`

- 📖 [兼容性检查器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-integration/scripts/兼容性检查器.py) — 状态: `HELP_OK`
- 📖 [集成测试引擎.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-integration/scripts/集成测试引擎.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-multicurrency/scripts`

- 📖 [多币种行情中心.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-multicurrency/scripts/多币种行情中心.py) — 状态: `HELP_OK`
- ⚙️ [汇率转换器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-multicurrency/scripts/汇率转换器.py) — 状态: `MAIN_NO_HELP`
- 📖 [龍字规范化器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-multicurrency/scripts/龍字规范化器.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-review/scripts`

- 📖 [复盘引擎.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/cloud/longhun-review/scripts/复盘引擎.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-3core-opt/scripts`

- 📖 [三核心优化器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-3core-opt/scripts/三核心优化器.py) — 状态: `HELP_OK`
- 📖 [快速启动检查.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-3core-opt/scripts/快速启动检查.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-agent-eco/scripts`

- 🚀 [任务管理器v2.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-agent-eco/scripts/任务管理器v2.py) — 状态: `HAS_MAIN`
- 🚀 [智能体生态系统.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-agent-eco/scripts/智能体生态系统.py) — 状态: `HAS_MAIN`
- 🚀 [路由引擎v2.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-agent-eco/scripts/路由引擎v2.py) — 状态: `HAS_MAIN`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-backup/scripts`

- 📖 [备份管理器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-backup/scripts/备份管理器.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-benchmark/scripts`

- 📖 [基准测试引擎.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-benchmark/scripts/基准测试引擎.py) — 状态: `HELP_OK`
- 📖 [性能分析器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-benchmark/scripts/性能分析器.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-daemon/scripts`

- 📖 [一鍵啟動器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-daemon/scripts/一鍵啟動器.py) — 状态: `HELP_OK`
- 📖 [健康檢查器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-daemon/scripts/健康檢查器.py) — 状态: `HELP_OK`
- 📖 [守护进程管理器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-daemon/scripts/守护进程管理器.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-dna-align/scripts`

- 📖 [DNA修复器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-dna-align/scripts/DNA修复器.py) — 状态: `HELP_OK`
- 📖 [DNA对齐审计器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-dna-align/scripts/DNA对齐审计器.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-formula-opt/scripts`

- 📖 [公式链优化器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-formula-opt/scripts/公式链优化器.py) — 状态: `HELP_OK`
- 📖 [性能对比分析器.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-formula-opt/scripts/性能对比分析器.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-monitoring/scripts`

- 🚀 [监控核心.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun-v5-skills-archive/local/longhun-monitoring/scripts/监控核心.py) — 状态: `HAS_MAIN`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun_mvp_reviewed`

- 🚀 [baobao_workflow_v2.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun_mvp_reviewed/baobao_workflow_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [cnsh_aligner_v1.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun_mvp_reviewed/cnsh_aligner_v1.0.py) — 状态: `HAS_MAIN`
- 🚀 [content_sovereignty_protocol_v2.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun_mvp_reviewed/content_sovereignty_protocol_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [lineage_verification_engine_v1.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun_mvp_reviewed/lineage_verification_engine_v1.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_file_audit_foundation_v1.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun_mvp_reviewed/longhun_file_audit_foundation_v1.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_foundation_launcher_v1.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun_mvp_reviewed/longhun_foundation_launcher_v1.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_execution_engine_v2.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun_mvp_reviewed/longhun_mvp_execution_engine_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_launcher_v2.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun_mvp_reviewed/longhun_mvp_launcher_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_notion_integration_v2.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun_mvp_reviewed/longhun_mvp_notion_integration_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_setup_integration_v2.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun_mvp_reviewed/longhun_mvp_setup_integration_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [script_manager_v1.0.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/longhun_mvp_reviewed/script_manager_v1.0.py) — 状态: `HAS_MAIN`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 7`

- 📖 [longhun-v7-launcher.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 7/longhun-v7-launcher.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 8`

- 📖 [守护进程管理器_逐行注释版.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 8/守护进程管理器_逐行注释版.py) — 状态: `HELP_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5`

- 🚀 [龍魂体系v5-本地启动.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/龍魂体系v5-本地启动.py) — 状态: `HAS_MAIN`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/CNSH/runtime/主权工具/sovereignty`

- ✅ [__init__.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/CNSH/runtime/主权工具/sovereignty/__init__.py) — 状态: `IMPORT_OK`
- ⚙️ [cli.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/CNSH/runtime/主权工具/sovereignty/cli.py) — 状态: `MAIN_NO_HELP`
- 🚀 [templates.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/CNSH/runtime/主权工具/sovereignty/templates.py) — 状态: `HAS_MAIN`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/CNSH/runtime/主权工具/sovereignty/portal`

- 🚀 [api_server.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/CNSH/runtime/主权工具/sovereignty/portal/api_server.py) — 状态: `HAS_MAIN`
- ✔️ [启动国家数字身份入口.sh](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/CNSH/runtime/主权工具/sovereignty/portal/启动国家数字身份入口.sh) — 状态: `SYNTAX_OK`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/CNSH/skills-export/china-digital-identity/src`

- 🚀 [digital_identity.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/CNSH/skills-export/china-digital-identity/src/digital_identity.py) — 状态: `HAS_MAIN`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/CNSH/skills-export/china-digital-identity/src/audit`

- 🚀 [behavioral_crypto.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/CNSH/skills-export/china-digital-identity/src/audit/behavioral_crypto.py) — 状态: `HAS_MAIN`
- 🚀 [left_right_audit.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/CNSH/skills-export/china-digital-identity/src/audit/left_right_audit.py) — 状态: `HAS_MAIN`
- 🚀 [system_guardian.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/CNSH/skills-export/china-digital-identity/src/audit/system_guardian.py) — 状态: `HAS_MAIN`

### `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/CNSH/skills-export/china-digital-identity/src/sovereignty/portal`

- 🚀 [api_server.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/CNSH/skills-export/china-digital-identity/src/sovereignty/portal/api_server.py) — 状态: `HAS_MAIN`
- 🚀 [国家数字身份统一认证入口.py](cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化5/CNSH/skills-export/china-digital-identity/src/sovereignty/portal/国家数字身份统一认证入口.py) — 状态: `HAS_MAIN`

### `cnsh-terminal/engines`

- 📖 [cnsh_translator_engine_v2.0.py](cnsh-terminal/engines/cnsh_translator_engine_v2.0.py) — 状态: `HELP_OK`

### `cnsh-terminal/modules`

- ✅ [__init__.py](cnsh-terminal/modules/__init__.py) — 状态: `IMPORT_OK`
- ✅ [ai_timestamp.py](cnsh-terminal/modules/ai_timestamp.py) — 状态: `IMPORT_OK`
- ✅ [ast_nodes.py](cnsh-terminal/modules/ast_nodes.py) — 状态: `IMPORT_OK`
- ✅ [audit_integration.py](cnsh-terminal/modules/audit_integration.py) — 状态: `IMPORT_OK`
- ✅ [circuit_breaker.py](cnsh-terminal/modules/circuit_breaker.py) — 状态: `IMPORT_OK`
- ✅ [encryption.py](cnsh-terminal/modules/encryption.py) — 状态: `IMPORT_OK`
- ✅ [four_layer_check.py](cnsh-terminal/modules/four_layer_check.py) — 状态: `IMPORT_OK`
- 🚀 [lexer.py](cnsh-terminal/modules/lexer.py) — 状态: `HAS_MAIN`
- 🚀 [terminology_bank.py](cnsh-terminal/modules/terminology_bank.py) — 状态: `HAS_MAIN`
- 🚀 [translator.py](cnsh-terminal/modules/translator.py) — 状态: `HAS_MAIN`

### `cnsh-terminal/modules/multimodal`

- 🚀 [通心译扩展术语表.py](cnsh-terminal/modules/multimodal/通心译扩展术语表.py) — 状态: `HAS_MAIN`
- ✔️ [龍魂图像识别器.py](cnsh-terminal/modules/multimodal/龍魂图像识别器.py) — 状态: `SYNTAX_OK`
- 🚀 [龍魂多模态感知中枢.py](cnsh-terminal/modules/multimodal/龍魂多模态感知中枢.py) — 状态: `HAS_MAIN`
- ✔️ [龍魂语音合成器.py](cnsh-terminal/modules/multimodal/龍魂语音合成器.py) — 状态: `SYNTAX_OK`
- ✔️ [龍魂语音识别器.py](cnsh-terminal/modules/multimodal/龍魂语音识别器.py) — 状态: `SYNTAX_OK`

### `cnsh_terminal_v5.0/modules`

- 🚀 [editor_ui.py](cnsh_terminal_v5.0/modules/editor_ui.py) — 状态: `HAS_MAIN`

### `control-panel`

- 🚀 [api_gateway_8443.py](control-panel/api_gateway_8443.py) — 状态: `HAS_MAIN`
- ✔️ [launch.sh](control-panel/launch.sh) — 状态: `SYNTAX_OK`
- 🚀 [main.py](control-panel/main.py) — 状态: `HAS_MAIN`
- 🚀 [tongxinyi_gate.py](control-panel/tongxinyi_gate.py) — 状态: `HAS_MAIN`

### `control-panel/api`

- ✅ [behavior_wrappers.py](control-panel/api/behavior_wrappers.py) — 状态: `IMPORT_OK`
- ✅ [foundation_wrappers.py](control-panel/api/foundation_wrappers.py) — 状态: `IMPORT_OK`
- 🚀 [skill_wrappers.py](control-panel/api/skill_wrappers.py) — 状态: `HAS_MAIN`
- 🚀 [system_monitor.py](control-panel/api/system_monitor.py) — 状态: `HAS_MAIN`

### `crypto-stack/src`

- 🚀 [l1_physical.py](crypto-stack/src/l1_physical.py) — 状态: `HAS_MAIN`
- 🚀 [l4_seven_factor.py](crypto-stack/src/l4_seven_factor.py) — 状态: `HAS_MAIN`
- 🚀 [l6_soul.py](crypto-stack/src/l6_soul.py) — 状态: `HAS_MAIN`
- 🚀 [stack_runner.py](crypto-stack/src/stack_runner.py) — 状态: `HAS_MAIN`
- 🚀 [weight_tuner.py](crypto-stack/src/weight_tuner.py) — 状态: `HAS_MAIN`

### `csdn_sync`

- 🚀 [enhance_drafts.py](csdn_sync/enhance_drafts.py) — 状态: `HAS_MAIN`
- 🚀 [publish_remaining.py](csdn_sync/publish_remaining.py) — 状态: `HAS_MAIN`
- 🚀 [sanitize.py](csdn_sync/sanitize.py) — 状态: `HAS_MAIN`

### `deployment`

- 🚀 [demo_staging_deployment.py](deployment/demo_staging_deployment.py) — 状态: `HAS_MAIN`
- 🚀 [production_deployment.py](deployment/production_deployment.py) — 状态: `HAS_MAIN`

### `desktop`

- 🚀 [龍魂控制中心.py](desktop/龍魂控制中心.py) — 状态: `HAS_MAIN`

### `docs/claude-backlog/01_协议同步包/网页`

- ✔️ [sync-install.sh](docs/claude-backlog/01_协议同步包/网页/sync-install.sh) — 状态: `SYNTAX_OK`

### `docs/claude-backlog/01_协议同步包/网页/dna-sync-pack/skills`

- 🚀 [wucai-audit.py](docs/claude-backlog/01_协议同步包/网页/dna-sync-pack/skills/wucai-audit.py) — 状态: `HAS_MAIN`

### `docs/claude-backlog/02_CNSH语言`

- ✔️ [编译运行.sh](docs/claude-backlog/02_CNSH语言/编译运行.sh) — 状态: `SYNTAX_OK`
- 📖 [设置-cnsh文件关联.sh](docs/claude-backlog/02_CNSH语言/设置-cnsh文件关联.sh) — 状态: `HELP_OK`

### `docs/claude-backlog/05_工具脚本`

- 🚀 [DNA_生成器_v1.0.cnsh.py](docs/claude-backlog/05_工具脚本/DNA_生成器_v1.0.cnsh.py) — 状态: `HAS_MAIN`
- 🚀 [alignment_v1.5_F19_F22.py](docs/claude-backlog/05_工具脚本/alignment_v1.5_F19_F22.py) — 状态: `HAS_MAIN`

### `editor`

- 🚀 [龍碼編輯器.py](editor/龍碼編輯器.py) — 状态: `HAS_MAIN`

### `executors/kfpp`

- 🚀 [longhun_kfpp_executor_v1.0.py](executors/kfpp/longhun_kfpp_executor_v1.0.py) — 状态: `HAS_MAIN`

### `executors/kimi-agent-v2`

- 📖 [baobao_workflow_v2.0.py](executors/kimi-agent-v2/baobao_workflow_v2.0.py) — 状态: `HELP_OK`
- 🚀 [cnsh_aligner_v2.0.py](executors/kimi-agent-v2/cnsh_aligner_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [content_sovereignty_protocol_v2.1.py](executors/kimi-agent-v2/content_sovereignty_protocol_v2.1.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_file_audit_foundation_v2.0.py](executors/kimi-agent-v2/longhun_file_audit_foundation_v2.0.py) — 状态: `HAS_MAIN`
- 📖 [longhun_foundation_launcher_v2.0.py](executors/kimi-agent-v2/longhun_foundation_launcher_v2.0.py) — 状态: `HELP_OK`
- 🚀 [longhun_lineage_verification_v2.0.py](executors/kimi-agent-v2/longhun_lineage_verification_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_executor_v2.0.py](executors/kimi-agent-v2/longhun_mvp_executor_v2.0.py) — 状态: `HAS_MAIN`
- 📖 [longhun_mvp_launcher_v2.0.py](executors/kimi-agent-v2/longhun_mvp_launcher_v2.0.py) — 状态: `HELP_OK`
- 🚀 [longhun_mvp_notion_integration_v2.0.py](executors/kimi-agent-v2/longhun_mvp_notion_integration_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_setup_integration_v2.0.py](executors/kimi-agent-v2/longhun_mvp_setup_integration_v2.0.py) — 状态: `HAS_MAIN`
- 📖 [longhun_script_manager_v2.0.py](executors/kimi-agent-v2/longhun_script_manager_v2.0.py) — 状态: `HELP_OK`

### `executors/mvp`

- 🚀 [longhun_mvp_launcher_v1.0.py](executors/mvp/longhun_mvp_launcher_v1.0.py) — 状态: `HAS_MAIN`

### `executors/runtime`

- 🚀 [longhun_foundation_runtime_v1.0.py](executors/runtime/longhun_foundation_runtime_v1.0.py) — 状态: `HAS_MAIN`

### `executors/task`

- 🚀 [task_executor_live_v1.py](executors/task/task_executor_live_v1.py) — 状态: `HAS_MAIN`

### `extensions/LongHunWidget/mcp-bridge`

- 📖 [install.sh](extensions/LongHunWidget/mcp-bridge/install.sh) — 状态: `HELP_OK`

### `imports/v7`

- 📖 [baobao_workflow_v2.0.py](imports/v7/baobao_workflow_v2.0.py) — 状态: `HELP_OK`
- 🚀 [cnsh_aligner_v2.0.py](imports/v7/cnsh_aligner_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [cnsh_editor_engine_v2.0.py](imports/v7/cnsh_editor_engine_v2.0.py) — 状态: `HAS_MAIN`
- 📖 [cnsh_translator_engine_v2.0.py](imports/v7/cnsh_translator_engine_v2.0.py) — 状态: `HELP_OK`
- 🚀 [longhun_file_audit_foundation_v2.0.py](imports/v7/longhun_file_audit_foundation_v2.0.py) — 状态: `HAS_MAIN`
- 📖 [longhun_foundation_launcher_v2.0.py](imports/v7/longhun_foundation_launcher_v2.0.py) — 状态: `HELP_OK`
- 🚀 [longhun_lineage_verification_v2.0.py](imports/v7/longhun_lineage_verification_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_executor_v2.0.py](imports/v7/longhun_mvp_executor_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_launcher_v2.0.py](imports/v7/longhun_mvp_launcher_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_notion_integration_v2.0.py](imports/v7/longhun_mvp_notion_integration_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_setup_integration_v2.0.py](imports/v7/longhun_mvp_setup_integration_v2.0.py) — 状态: `HAS_MAIN`
- 📖 [longhun_script_manager_v2.0.py](imports/v7/longhun_script_manager_v2.0.py) — 状态: `HELP_OK`
- 📖 [守护进程管理器_逐行注释版.py](imports/v7/守护进程管理器_逐行注释版.py) — 状态: `HELP_OK`

### `integrated-modules/gateway`

- ✅ [__init__.py](integrated-modules/gateway/__init__.py) — 状态: `IMPORT_OK`

### `integrated-modules/kimi_agent`

- ✅ [__init__.py](integrated-modules/kimi_agent/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [cnsh_api_server.py](integrated-modules/kimi_agent/cnsh_api_server.py) — 状态: `HAS_MAIN`
- 🚀 [cnsh_core_engine.py](integrated-modules/kimi_agent/cnsh_core_engine.py) — 状态: `HAS_MAIN`
- 🚀 [cnsh_main.py](integrated-modules/kimi_agent/cnsh_main.py) — 状态: `HAS_MAIN`
- 🚀 [cnsh_meta_awareness.py](integrated-modules/kimi_agent/cnsh_meta_awareness.py) — 状态: `HAS_MAIN`
- 🚀 [cnsh_persona_system.py](integrated-modules/kimi_agent/cnsh_persona_system.py) — 状态: `HAS_MAIN`

### `integrated-modules/longhun_config`

- ✅ [__init__.py](integrated-modules/longhun_config/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [sovereign_env.py](integrated-modules/longhun_config/sovereign_env.py) — 状态: `HAS_MAIN`

### `integrated-modules/longhun_logging`

- ✅ [__init__.py](integrated-modules/longhun_logging/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [longhun_logging_versioning_tracing_core.py](integrated-modules/longhun_logging/longhun_logging_versioning_tracing_core.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_startup_recovery_system.py](integrated-modules/longhun_logging/longhun_startup_recovery_system.py) — 状态: `HAS_MAIN`

### `integrated-modules/monitoring`

- ✅ [__init__.py](integrated-modules/monitoring/__init__.py) — 状态: `IMPORT_OK`

### `integrated-modules/protocols`

- ✅ [__init__.py](integrated-modules/protocols/__init__.py) — 状态: `IMPORT_OK`
- ✔️ [protocol_shield.sh](integrated-modules/protocols/protocol_shield.sh) — 状态: `SYNTAX_OK`

### `integrated-modules/skills.integrated`

- ✅ [__init__.py](integrated-modules/skills.integrated/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [longhun_skill_auto_completion_engine.py](integrated-modules/skills.integrated/longhun_skill_auto_completion_engine.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_standard_calculation_framework.py](integrated-modules/skills.integrated/longhun_standard_calculation_framework.py) — 状态: `HAS_MAIN`

### `integrated-modules/sync`

- ✔️ [BRAIN_NOTION_SYNC_UPGRADE_DEPLOY.sh](integrated-modules/sync/BRAIN_NOTION_SYNC_UPGRADE_DEPLOY.sh) — 状态: `SYNTAX_OK`
- ✅ [__init__.py](integrated-modules/sync/__init__.py) — 状态: `IMPORT_OK`
- ⚙️ [brain_notion_sync_v1_1_upgraded.py](integrated-modules/sync/brain_notion_sync_v1_1_upgraded.py) — 状态: `MAIN_NO_HELP`

### `integrations/mcp`

- 🚀 [cnsh_mcp_server.py](integrations/mcp/cnsh_mcp_server.py) — 状态: `HAS_MAIN`
- 🚀 [v4_mcp_server.py](integrations/mcp/v4_mcp_server.py) — 状态: `HAS_MAIN`

### `integrations/notion`

- 🚀 [longhun_mvp_notion_integration_v1.0.py](integrations/notion/longhun_mvp_notion_integration_v1.0.py) — 状态: `HAS_MAIN`
- 📖 [philosophy_system_sync.py](integrations/notion/philosophy_system_sync.py) — 状态: `HELP_OK`

### `integrations/wechat_public_account`

- 📖 [cli.py](integrations/wechat_public_account/cli.py) — 状态: `HELP_OK`
- ✔️ [setup.sh](integrations/wechat_public_account/setup.sh) — 状态: `SYNTAX_OK`
- 🚀 [web_ui.py](integrations/wechat_public_account/web_ui.py) — 状态: `HAS_MAIN`

### `integrations/wechat_public_account/config`

- ✅ [__init__.py](integrations/wechat_public_account/config/__init__.py) — 状态: `IMPORT_OK`
- ✅ [settings.py](integrations/wechat_public_account/config/settings.py) — 状态: `IMPORT_OK`

### `integrations/wechat_public_account/core`

- ✅ [__init__.py](integrations/wechat_public_account/core/__init__.py) — 状态: `IMPORT_OK`

### `integrations/wechat_public_account/services`

- ✅ [__init__.py](integrations/wechat_public_account/services/__init__.py) — 状态: `IMPORT_OK`
- ✅ [voice_service.py](integrations/wechat_public_account/services/voice_service.py) — 状态: `IMPORT_OK`

### `kimi`

- ✅ [__init__.py](kimi/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [kimi_client.py](kimi/kimi_client.py) — 状态: `HAS_MAIN`
- 🚀 [kimi_gateway.py](kimi/kimi_gateway.py) — 状态: `HAS_MAIN`
- 🚀 [kimi_integration.py](kimi/kimi_integration.py) — 状态: `HAS_MAIN`
- 🚀 [test_kimi_integration.py](kimi/test_kimi_integration.py) — 状态: `HAS_MAIN`

### `logging_backup`

- ✅ [__init__.py](logging_backup/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [longhun-logging-versioning-tracing-core.py](logging_backup/longhun-logging-versioning-tracing-core.py) — 状态: `HAS_MAIN`
- 🚀 [longhun-startup-recovery-system.py](logging_backup/longhun-startup-recovery-system.py) — 状态: `HAS_MAIN`

### `longhun-font`

- 📖 [editor.py](longhun-font/editor.py) — 状态: `HELP_OK`
- ✔️ [install_macos.sh](longhun-font/install_macos.sh) — 状态: `SYNTAX_OK`

### `longhun-font/calligraphy`

- ✅ [__init__.py](longhun-font/calligraphy/__init__.py) — 状态: `IMPORT_OK`
- 📖 [cli.py](longhun-font/calligraphy/cli.py) — 状态: `HELP_OK`
- 🚀 [renderer.py](longhun-font/calligraphy/renderer.py) — 状态: `HAS_MAIN`
- 🚀 [seal_generator.py](longhun-font/calligraphy/seal_generator.py) — 状态: `HAS_MAIN`
- 🚀 [watermark.py](longhun-font/calligraphy/watermark.py) — 状态: `HAS_MAIN`
- 🚀 [work_id.py](longhun-font/calligraphy/work_id.py) — 状态: `HAS_MAIN`

### `longhun-font/engines`

- 🚀 [cnsh_font_engine.py](longhun-font/engines/cnsh_font_engine.py) — 状态: `HAS_MAIN`
- 🚀 [cnsh_font_engine_current.py](longhun-font/engines/cnsh_font_engine_current.py) — 状态: `HAS_MAIN`
- 🚀 [cnsh_font_engine_uid9622.py](longhun-font/engines/cnsh_font_engine_uid9622.py) — 状态: `HAS_MAIN`
- 🚀 [cnsh_font_engine_uid9622_current.py](longhun-font/engines/cnsh_font_engine_uid9622_current.py) — 状态: `HAS_MAIN`

### `longhun-font/scripts`

- 🚀 [build_font_v3.py](longhun-font/scripts/build_font_v3.py) — 状态: `HAS_MAIN`
- 🚀 [build_wuwu_color_font.py](longhun-font/scripts/build_wuwu_color_font.py) — 状态: `HAS_MAIN`
- 🚀 [expand_chinese_10000.py](longhun-font/scripts/expand_chinese_10000.py) — 状态: `HAS_MAIN`
- 🚀 [expand_chinese_5000.py](longhun-font/scripts/expand_chinese_5000.py) — 状态: `HAS_MAIN`
- 🚀 [expand_chinese_7000.py](longhun-font/scripts/expand_chinese_7000.py) — 状态: `HAS_MAIN`
- 🚀 [expand_chinese_full_cjk.py](longhun-font/scripts/expand_chinese_full_cjk.py) — 状态: `HAS_MAIN`
- 🚀 [expand_more_oracle_bone.py](longhun-font/scripts/expand_more_oracle_bone.py) — 状态: `HAS_MAIN`
- 🚀 [generate_coverage_report.py](longhun-font/scripts/generate_coverage_report.py) — 状态: `HAS_MAIN`
- 🚀 [glyph_generator_calligraphy.py](longhun-font/scripts/glyph_generator_calligraphy.py) — 状态: `HAS_MAIN`
- 🚀 [refine_all_cjk_calligraphy.py](longhun-font/scripts/refine_all_cjk_calligraphy.py) — 状态: `HAS_MAIN`
- ✔️ [release.sh](longhun-font/scripts/release.sh) — 状态: `SYNTAX_OK`

### `longhun_mvp_reviewed`

- 🚀 [baobao_workflow_v2.0.py](longhun_mvp_reviewed/baobao_workflow_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [cnsh_aligner_v1.0.py](longhun_mvp_reviewed/cnsh_aligner_v1.0.py) — 状态: `HAS_MAIN`
- 🚀 [content_sovereignty_protocol_v2.0.py](longhun_mvp_reviewed/content_sovereignty_protocol_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [lineage_verification_engine_v1.0.py](longhun_mvp_reviewed/lineage_verification_engine_v1.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_file_audit_foundation_v1.0.py](longhun_mvp_reviewed/longhun_file_audit_foundation_v1.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_foundation_launcher_v1.0.py](longhun_mvp_reviewed/longhun_foundation_launcher_v1.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_execution_engine_v2.0.py](longhun_mvp_reviewed/longhun_mvp_execution_engine_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_launcher_v2.0.py](longhun_mvp_reviewed/longhun_mvp_launcher_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_notion_integration_v2.0.py](longhun_mvp_reviewed/longhun_mvp_notion_integration_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_setup_integration_v2.0.py](longhun_mvp_reviewed/longhun_mvp_setup_integration_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [script_manager_v1.0.py](longhun_mvp_reviewed/script_manager_v1.0.py) — 状态: `HAS_MAIN`

### `memory-universe`

- 📖 [星辰记忆系统.py](memory-universe/星辰记忆系统.py) — 状态: `HELP_OK`

### `mobile-monitoring.integrated`

- ✔️ [deploy-all-mock.sh](mobile-monitoring.integrated/deploy-all-mock.sh) — 状态: `SYNTAX_OK`
- ✔️ [deploy-all.sh](mobile-monitoring.integrated/deploy-all.sh) — 状态: `SYNTAX_OK`

### `mobile-monitoring.integrated/backend/python`

- 🚀 [monitoring_server.py](mobile-monitoring.integrated/backend/python/monitoring_server.py) — 状态: `HAS_MAIN`
- ✅ [monitoring_server_port9000.py](mobile-monitoring.integrated/backend/python/monitoring_server_port9000.py) — 状态: `IMPORT_OK`

### `monitoring`

- ✅ [__init__.py](monitoring/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [datadog_monitoring_config.py](monitoring/datadog_monitoring_config.py) — 状态: `HAS_MAIN`

### `monitoring.backup`

- 🚀 [datadog_monitoring_config.py](monitoring.backup/datadog_monitoring_config.py) — 状态: `HAS_MAIN`

### `multicurrency`

- 🚀 [alert_system.py](multicurrency/alert_system.py) — 状态: `HAS_MAIN`
- 📖 [backup_databases.sh](multicurrency/backup_databases.sh) — 状态: `HELP_OK`
- 🚀 [currency_database.py](multicurrency/currency_database.py) — 状态: `HAS_MAIN`
- 🚀 [dashboard_lite.py](multicurrency/dashboard_lite.py) — 状态: `HAS_MAIN`
- 🚀 [dashboard_server.py](multicurrency/dashboard_server.py) — 状态: `HAS_MAIN`
- 🚀 [exchange_rate_sources.py](multicurrency/exchange_rate_sources.py) — 状态: `HAS_MAIN`
- ✔️ [health_check.sh](multicurrency/health_check.sh) — 状态: `SYNTAX_OK`
- 📖 [multicurrency_service.py](multicurrency/multicurrency_service.py) — 状态: `HELP_OK`
- ⚙️ [notion_multicurrency_integration.py](multicurrency/notion_multicurrency_integration.py) — 状态: `MAIN_NO_HELP`
- ⚙️ [notion_multicurrency_sync.py](multicurrency/notion_multicurrency_sync.py) — 状态: `MAIN_NO_HELP`
- ⚙️ [system_test_suite.py](multicurrency/system_test_suite.py) — 状态: `MAIN_NO_HELP`
- 🚀 [trend_analyzer.py](multicurrency/trend_analyzer.py) — 状态: `HAS_MAIN`

### `persona`

- 📖 [anti_blowout_guard.py](persona/anti_blowout_guard.py) — 状态: `HELP_OK`
- 🚀 [apply_sovereignty_footer.py](persona/apply_sovereignty_footer.py) — 状态: `HAS_MAIN`
- 📖 [audit_logger.py](persona/audit_logger.py) — 状态: `HELP_OK`
- 📖 [compression_engine.py](persona/compression_engine.py) — 状态: `HELP_OK`
- 📖 [dna_tracer.py](persona/dna_tracer.py) — 状态: `HELP_OK`
- 📖 [eternal_guard.py](persona/eternal_guard.py) — 状态: `HELP_OK`
- 📖 [output_contract.py](persona/output_contract.py) — 状态: `HELP_OK`
- 📖 [overload_guard.py](persona/overload_guard.py) — 状态: `HELP_OK`
- 🚀 [protocol_librarian.py](persona/protocol_librarian.py) — 状态: `HAS_MAIN`
- 📖 [system_status_panel.py](persona/system_status_panel.py) — 状态: `HELP_OK`
- 📖 [德者永生殿_v2.0.py](persona/德者永生殿_v2.0.py) — 状态: `HELP_OK`

### `phase3`

- ✔️ [launch-phase3.sh](phase3/launch-phase3.sh) — 状态: `SYNTAX_OK`

### `phase3/backend`

- 🚀 [main.py](phase3/backend/main.py) — 状态: `HAS_MAIN`

### `project-memory`

- 📖 [龍魂編年史.py](project-memory/龍魂編年史.py) — 状态: `HELP_OK`

### `releases/v5.1/staging/agents`

- 🚀 [longhun_foundation_launcher_auto.py](releases/v5.1/staging/agents/longhun_foundation_launcher_auto.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_notion_sync_auto.py](releases/v5.1/staging/agents/longhun_notion_sync_auto.py) — 状态: `HAS_MAIN`
- 🚀 [task_executor_live_v1.py](releases/v5.1/staging/agents/task_executor_live_v1.py) — 状态: `HAS_MAIN`
- 🚀 [xpay_core_auto.py](releases/v5.1/staging/agents/xpay_core_auto.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/baobao-guardian`

- ✔️ [start.sh](releases/v5.1/staging/baobao-guardian/start.sh) — 状态: `SYNTAX_OK`
- 📖 [verify-structure.sh](releases/v5.1/staging/baobao-guardian/verify-structure.sh) — 状态: `HELP_OK`

### `releases/v5.1/staging/baobao-guardian/backend/app`

- 🚀 [main.py](releases/v5.1/staging/baobao-guardian/backend/app/main.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/brain`

- ⚙️ [brain_notion_sync.py](releases/v5.1/staging/brain/brain_notion_sync.py) — 状态: `MAIN_NO_HELP`

### `releases/v5.1/staging/cnsh`

- ✅ [__init__.py](releases/v5.1/staging/cnsh/__init__.py) — 状态: `IMPORT_OK`
- ✔️ [launch.sh](releases/v5.1/staging/cnsh/launch.sh) — 状态: `SYNTAX_OK`
- 🚀 [task_executor_v9_integrated.py](releases/v5.1/staging/cnsh/task_executor_v9_integrated.py) — 状态: `HAS_MAIN`
- ✅ [v9_system_integration_bridge.py](releases/v5.1/staging/cnsh/v9_system_integration_bridge.py) — 状态: `IMPORT_OK`
- 🚀 [v9_task_executor_adapter.py](releases/v5.1/staging/cnsh/v9_task_executor_adapter.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/cnsh-terminal`

- 📖 [cnsh_terminal_v5.py](releases/v5.1/staging/cnsh-terminal/cnsh_terminal_v5.py) — 状态: `HELP_OK`
- 📖 [multimodal_cli.py](releases/v5.1/staging/cnsh-terminal/multimodal_cli.py) — 状态: `HELP_OK`

### `releases/v5.1/staging/cnsh-terminal/engines`

- 🚀 [cnsh_editor_engine_v2.0.py](releases/v5.1/staging/cnsh-terminal/engines/cnsh_editor_engine_v2.0.py) — 状态: `HAS_MAIN`
- 📖 [cnsh_translator_engine_v2.0.py](releases/v5.1/staging/cnsh-terminal/engines/cnsh_translator_engine_v2.0.py) — 状态: `HELP_OK`

### `releases/v5.1/staging/cnsh-terminal/modules`

- ✅ [__init__.py](releases/v5.1/staging/cnsh-terminal/modules/__init__.py) — 状态: `IMPORT_OK`
- ✅ [ai_timestamp.py](releases/v5.1/staging/cnsh-terminal/modules/ai_timestamp.py) — 状态: `IMPORT_OK`
- ✅ [ast_nodes.py](releases/v5.1/staging/cnsh-terminal/modules/ast_nodes.py) — 状态: `IMPORT_OK`
- ✅ [audit_integration.py](releases/v5.1/staging/cnsh-terminal/modules/audit_integration.py) — 状态: `IMPORT_OK`
- ✅ [circuit_breaker.py](releases/v5.1/staging/cnsh-terminal/modules/circuit_breaker.py) — 状态: `IMPORT_OK`
- 🚀 [editor_ui.py](releases/v5.1/staging/cnsh-terminal/modules/editor_ui.py) — 状态: `HAS_MAIN`
- ✅ [encryption.py](releases/v5.1/staging/cnsh-terminal/modules/encryption.py) — 状态: `IMPORT_OK`
- ✅ [four_layer_check.py](releases/v5.1/staging/cnsh-terminal/modules/four_layer_check.py) — 状态: `IMPORT_OK`
- 🚀 [lexer.py](releases/v5.1/staging/cnsh-terminal/modules/lexer.py) — 状态: `HAS_MAIN`
- 🚀 [terminology_bank.py](releases/v5.1/staging/cnsh-terminal/modules/terminology_bank.py) — 状态: `HAS_MAIN`
- 🚀 [translator.py](releases/v5.1/staging/cnsh-terminal/modules/translator.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/cnsh-terminal/modules/multimodal`

- 🚀 [通心译扩展术语表.py](releases/v5.1/staging/cnsh-terminal/modules/multimodal/通心译扩展术语表.py) — 状态: `HAS_MAIN`
- 🚀 [龍魂图像识别器.py](releases/v5.1/staging/cnsh-terminal/modules/multimodal/龍魂图像识别器.py) — 状态: `HAS_MAIN`
- 🚀 [龍魂多模态感知中枢.py](releases/v5.1/staging/cnsh-terminal/modules/multimodal/龍魂多模态感知中枢.py) — 状态: `HAS_MAIN`
- 🚀 [龍魂语音合成器.py](releases/v5.1/staging/cnsh-terminal/modules/multimodal/龍魂语音合成器.py) — 状态: `HAS_MAIN`
- 🚀 [龍魂语音识别器.py](releases/v5.1/staging/cnsh-terminal/modules/multimodal/龍魂语音识别器.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/cnsh/flow_decision`

- ✅ [__init__.py](releases/v5.1/staging/cnsh/flow_decision/__init__.py) — 状态: `IMPORT_OK`
- ✅ [cnsh_flow_decision_core.py](releases/v5.1/staging/cnsh/flow_decision/cnsh_flow_decision_core.py) — 状态: `IMPORT_OK`
- ✅ [digital_root.py](releases/v5.1/staging/cnsh/flow_decision/digital_root.py) — 状态: `IMPORT_OK`
- ✅ [dna_chain_tracer.py](releases/v5.1/staging/cnsh/flow_decision/dna_chain_tracer.py) — 状态: `IMPORT_OK`
- 🚀 [examples.py](releases/v5.1/staging/cnsh/flow_decision/examples.py) — 状态: `HAS_MAIN`
- ✅ [ipa_route_registry.py](releases/v5.1/staging/cnsh/flow_decision/ipa_route_registry.py) — 状态: `IMPORT_OK`
- 🚀 [persona_api.py](releases/v5.1/staging/cnsh/flow_decision/persona_api.py) — 状态: `HAS_MAIN`
- ✅ [persona_collaboration.py](releases/v5.1/staging/cnsh/flow_decision/persona_collaboration.py) — 状态: `IMPORT_OK`
- ✅ [schemas.py](releases/v5.1/staging/cnsh/flow_decision/schemas.py) — 状态: `IMPORT_OK`

### `releases/v5.1/staging/cnsh/flow_decision/tests`

- ✅ [__init__.py](releases/v5.1/staging/cnsh/flow_decision/tests/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [test_flow_decision_core.py](releases/v5.1/staging/cnsh/flow_decision/tests/test_flow_decision_core.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/cnsh/sancai_sync`

- ✅ [__init__.py](releases/v5.1/staging/cnsh/sancai_sync/__init__.py) — 状态: `IMPORT_OK`
- ✅ [sancai_sync_hub.py](releases/v5.1/staging/cnsh/sancai_sync/sancai_sync_hub.py) — 状态: `IMPORT_OK`

### `releases/v5.1/staging/cnsh/sancai_sync/tests`

- ✅ [__init__.py](releases/v5.1/staging/cnsh/sancai_sync/tests/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [test_sancai_sync_hub.py](releases/v5.1/staging/cnsh/sancai_sync/tests/test_sancai_sync_hub.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/cnsh/tests`

- ✅ [__init__.py](releases/v5.1/staging/cnsh/tests/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [test_v9_integration.py](releases/v5.1/staging/cnsh/tests/test_v9_integration.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/control-panel`

- ✔️ [launch.sh](releases/v5.1/staging/control-panel/launch.sh) — 状态: `SYNTAX_OK`
- 🚀 [main.py](releases/v5.1/staging/control-panel/main.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/control-panel/api`

- ✅ [foundation_wrappers.py](releases/v5.1/staging/control-panel/api/foundation_wrappers.py) — 状态: `IMPORT_OK`
- 🚀 [skill_wrappers.py](releases/v5.1/staging/control-panel/api/skill_wrappers.py) — 状态: `HAS_MAIN`
- 🚀 [system_monitor.py](releases/v5.1/staging/control-panel/api/system_monitor.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/crypto-stack/src`

- 🚀 [l1_physical.py](releases/v5.1/staging/crypto-stack/src/l1_physical.py) — 状态: `HAS_MAIN`
- 🚀 [l4_seven_factor.py](releases/v5.1/staging/crypto-stack/src/l4_seven_factor.py) — 状态: `HAS_MAIN`
- 🚀 [l6_soul.py](releases/v5.1/staging/crypto-stack/src/l6_soul.py) — 状态: `HAS_MAIN`
- 🚀 [stack_runner.py](releases/v5.1/staging/crypto-stack/src/stack_runner.py) — 状态: `HAS_MAIN`
- 🚀 [weight_tuner.py](releases/v5.1/staging/crypto-stack/src/weight_tuner.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/desktop`

- 🚀 [龍魂控制中心.py](releases/v5.1/staging/desktop/龍魂控制中心.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/editor`

- 🚀 [龍碼編輯器.py](releases/v5.1/staging/editor/龍碼編輯器.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/executors/kimi-agent-v2`

- 📖 [baobao_workflow_v2.0.py](releases/v5.1/staging/executors/kimi-agent-v2/baobao_workflow_v2.0.py) — 状态: `HELP_OK`
- 🚀 [cnsh_aligner_v2.0.py](releases/v5.1/staging/executors/kimi-agent-v2/cnsh_aligner_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [content_sovereignty_protocol_v2.1.py](releases/v5.1/staging/executors/kimi-agent-v2/content_sovereignty_protocol_v2.1.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_file_audit_foundation_v2.0.py](releases/v5.1/staging/executors/kimi-agent-v2/longhun_file_audit_foundation_v2.0.py) — 状态: `HAS_MAIN`
- 📖 [longhun_foundation_launcher_v2.0.py](releases/v5.1/staging/executors/kimi-agent-v2/longhun_foundation_launcher_v2.0.py) — 状态: `HELP_OK`
- 🚀 [longhun_lineage_verification_v2.0.py](releases/v5.1/staging/executors/kimi-agent-v2/longhun_lineage_verification_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_executor_v2.0.py](releases/v5.1/staging/executors/kimi-agent-v2/longhun_mvp_executor_v2.0.py) — 状态: `HAS_MAIN`
- 📖 [longhun_mvp_launcher_v2.0.py](releases/v5.1/staging/executors/kimi-agent-v2/longhun_mvp_launcher_v2.0.py) — 状态: `HELP_OK`
- 🚀 [longhun_mvp_notion_integration_v2.0.py](releases/v5.1/staging/executors/kimi-agent-v2/longhun_mvp_notion_integration_v2.0.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_mvp_setup_integration_v2.0.py](releases/v5.1/staging/executors/kimi-agent-v2/longhun_mvp_setup_integration_v2.0.py) — 状态: `HAS_MAIN`
- 📖 [longhun_script_manager_v2.0.py](releases/v5.1/staging/executors/kimi-agent-v2/longhun_script_manager_v2.0.py) — 状态: `HELP_OK`

### `releases/v5.1/staging/memory-universe`

- 📖 [星辰记忆系统.py](releases/v5.1/staging/memory-universe/星辰记忆系统.py) — 状态: `HELP_OK`

### `releases/v5.1/staging/skills`

- 📖 [SKILL-LAUNCHER.sh](releases/v5.1/staging/skills/SKILL-LAUNCHER.sh) — 状态: `HELP_OK`
- ✅ [__init__.py](releases/v5.1/staging/skills/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [api.py](releases/v5.1/staging/skills/api.py) — 状态: `HAS_MAIN`
- 🚀 [fill_all_skills_specifications.py](releases/v5.1/staging/skills/fill_all_skills_specifications.py) — 状态: `HAS_MAIN`
- 🚀 [longhun-skill-auto-completion-engine.py](releases/v5.1/staging/skills/longhun-skill-auto-completion-engine.py) — 状态: `HAS_MAIN`
- 🚀 [longhun-standard-calculation-framework.py](releases/v5.1/staging/skills/longhun-standard-calculation-framework.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_skill_auto_completion_engine.py](releases/v5.1/staging/skills/longhun_skill_auto_completion_engine.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_standard_calculation_framework.py](releases/v5.1/staging/skills/longhun_standard_calculation_framework.py) — 状态: `HAS_MAIN`
- 🚀 [phase5_performance_benchmark.py](releases/v5.1/staging/skills/phase5_performance_benchmark.py) — 状态: `HAS_MAIN`
- 🚀 [phase6_cross_skill_integration.py](releases/v5.1/staging/skills/phase6_cross_skill_integration.py) — 状态: `HAS_MAIN`
- 🚀 [phase7_final_system_acceptance.py](releases/v5.1/staging/skills/phase7_final_system_acceptance.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/skills/cnsh-aligner`

- 🚀 [cnsh_aligner.py](releases/v5.1/staging/skills/cnsh-aligner/cnsh_aligner.py) — 状态: `HAS_MAIN`
- 🚀 [script_manager.py](releases/v5.1/staging/skills/cnsh-aligner/script_manager.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/skills/longhun-audit-integrated`

- 📖 [longhun_audit_integrated.py](releases/v5.1/staging/skills/longhun-audit-integrated/longhun_audit_integrated.py) — 状态: `HELP_OK`

### `releases/v5.1/staging/skills/longhun-shield`

- 📖 [longhun_shield_cli.py](releases/v5.1/staging/skills/longhun-shield/longhun_shield_cli.py) — 状态: `HELP_OK`
- 🚀 [longhun_shield_instruction_protocol.py](releases/v5.1/staging/skills/longhun-shield/longhun_shield_instruction_protocol.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_shield_system.py](releases/v5.1/staging/skills/longhun-shield/longhun_shield_system.py) — 状态: `HAS_MAIN`
- 🚀 [shield_test_example.py](releases/v5.1/staging/skills/longhun-shield/shield_test_example.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/skills/py-skills`

- 🚀 [skill-10-web-artifacts-builder.py](releases/v5.1/staging/skills/py-skills/skill-10-web-artifacts-builder.py) — 状态: `HAS_MAIN`
- 🚀 [skill-6-mcp-builder.py](releases/v5.1/staging/skills/py-skills/skill-6-mcp-builder.py) — 状态: `HAS_MAIN`
- 🚀 [skill-7-skill-creator.py](releases/v5.1/staging/skills/py-skills/skill-7-skill-creator.py) — 状态: `HAS_MAIN`
- 🚀 [skill-8-slack-gif-creator.py](releases/v5.1/staging/skills/py-skills/skill-8-slack-gif-creator.py) — 状态: `HAS_MAIN`
- 🚀 [skill-9-theme-factory.py](releases/v5.1/staging/skills/py-skills/skill-9-theme-factory.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/skills/warehouse-audit/scripts`

- 📖 [audit_engine.py](releases/v5.1/staging/skills/warehouse-audit/scripts/audit_engine.py) — 状态: `HELP_OK`
- 📖 [generate_demo_wms_data.py](releases/v5.1/staging/skills/warehouse-audit/scripts/generate_demo_wms_data.py) — 状态: `HELP_OK`

### `releases/v5.1/staging/systems/kfpp`

- 🚀 [kfpp_executor_v1.0.py](releases/v5.1/staging/systems/kfpp/kfpp_executor_v1.0.py) — 状态: `HAS_MAIN`

### `releases/v5.1/staging/xpay`

- ✅ [__init__.py](releases/v5.1/staging/xpay/__init__.py) — 状态: `IMPORT_OK`

### `releases/v5.1/staging/xpay/src`

- ✅ [__init__.py](releases/v5.1/staging/xpay/src/__init__.py) — 状态: `IMPORT_OK`
- ✅ [adapter.py](releases/v5.1/staging/xpay/src/adapter.py) — 状态: `IMPORT_OK`
- 📖 [cli.py](releases/v5.1/staging/xpay/src/cli.py) — 状态: `HELP_OK`
- ✅ [dna.py](releases/v5.1/staging/xpay/src/dna.py) — 状态: `IMPORT_OK`
- ✅ [transaction.py](releases/v5.1/staging/xpay/src/transaction.py) — 状态: `IMPORT_OK`

### `releases/v5.1/staging/xpay/src/adapters`

- ✅ [__init__.py](releases/v5.1/staging/xpay/src/adapters/__init__.py) — 状态: `IMPORT_OK`
- ✅ [cny_demo.py](releases/v5.1/staging/xpay/src/adapters/cny_demo.py) — 状态: `IMPORT_OK`
- ✅ [eur_demo.py](releases/v5.1/staging/xpay/src/adapters/eur_demo.py) — 状态: `IMPORT_OK`
- ✅ [usd_demo.py](releases/v5.1/staging/xpay/src/adapters/usd_demo.py) — 状态: `IMPORT_OK`

### `releases/v5.1/staging/xpay/tests`

- 🚀 [test_gateway.py](releases/v5.1/staging/xpay/tests/test_gateway.py) — 状态: `HAS_MAIN`

### `research`

- 🚀 [riemann_numerical_verification_extended.py](research/riemann_numerical_verification_extended.py) — 状态: `HAS_MAIN`
- 🚀 [riemann_perspective_B_proof.py](research/riemann_perspective_B_proof.py) — 状态: `HAS_MAIN`
- 🚀 [riemann_perspective_C_proof.py](research/riemann_perspective_C_proof.py) — 状态: `HAS_MAIN`
- 🚀 [riemann_three_talent_verification.py](research/riemann_three_talent_verification.py) — 状态: `HAS_MAIN`

### `research/euv-lithography/scripts`

- 🚀 [cnsh_euv_model.py](research/euv-lithography/scripts/cnsh_euv_model.py) — 状态: `HAS_MAIN`

### `rules-engine-v2.5`

- 🚀 [batch_processor_v2.5.py](rules-engine-v2.5/batch_processor_v2.5.py) — 状态: `HAS_MAIN`
- 🚀 [notion_sync_v2.5.py](rules-engine-v2.5/notion_sync_v2.5.py) — 状态: `HAS_MAIN`
- ✔️ [report_generator_enhanced.py](rules-engine-v2.5/report_generator_enhanced.py) — 状态: `SYNTAX_OK`
- ✔️ [test_integration.py](rules-engine-v2.5/test_integration.py) — 状态: `SYNTAX_OK`

### `scripts`

- 📖 [baobao_workflow_v2.py](scripts/baobao_workflow_v2.py) — 状态: `HELP_OK`
- 🚀 [formula_chain.py](scripts/formula_chain.py) — 状态: `HAS_MAIN`
- 🚀 [formula_core.py](scripts/formula_core.py) — 状态: `HAS_MAIN`
- 🚀 [fulltext_compress.py](scripts/fulltext_compress.py) — 状态: `HAS_MAIN`
- 🚀 [heaven_nonkill_audit.py](scripts/heaven_nonkill_audit.py) — 状态: `HAS_MAIN`
- 🚀 [index_notion_exports.py](scripts/index_notion_exports.py) — 状态: `HAS_MAIN`
- 🚀 [kg_subgraphs.py](scripts/kg_subgraphs.py) — 状态: `HAS_MAIN`
- 📖 [kg_unified.py](scripts/kg_unified.py) — 状态: `HELP_OK`
- 📖 [longhun_compression_engine.py](scripts/longhun_compression_engine.py) — 状态: `HELP_OK`
- 🚀 [longhun_integrated_system.py](scripts/longhun_integrated_system.py) — 状态: `HAS_MAIN`
- 📖 [longhun_kb.py](scripts/longhun_kb.py) — 状态: `HELP_OK`
- 🚀 [longhun_kg.py](scripts/longhun_kg.py) — 状态: `HAS_MAIN`
- 🚀 [main.py](scripts/main.py) — 状态: `HAS_MAIN`
- 🚀 [module_self_assessment.py](scripts/module_self_assessment.py) — 状态: `HAS_MAIN`
- 🚀 [notion_download_orchestrator.py](scripts/notion_download_orchestrator.py) — 状态: `HAS_MAIN`
- 📖 [notion_downloader.py](scripts/notion_downloader.py) — 状态: `HELP_OK`
- 📖 [notion_knowledge_graph.py](scripts/notion_knowledge_graph.py) — 状态: `HELP_OK`
- 🚀 [notion_missing_report.py](scripts/notion_missing_report.py) — 状态: `HAS_MAIN`
- 📖 [setup.sh](scripts/setup.sh) — 状态: `HELP_OK`
- 🚀 [test_uid9622_env.py](scripts/test_uid9622_env.py) — 状态: `HAS_MAIN`
- 📖 [weekly_backup.sh](scripts/weekly_backup.sh) — 状态: `HELP_OK`

### `scripts/L0_MANIFESTO`

- 🚀 [manifesto_watchdog.py](scripts/L0_MANIFESTO/manifesto_watchdog.py) — 状态: `HAS_MAIN`

### `scripts/L1_IRON_LAWS`

- 🚀 [iron_laws_enforcer.py](scripts/L1_IRON_LAWS/iron_laws_enforcer.py) — 状态: `HAS_MAIN`
- 🚀 [semantic_shield.py](scripts/L1_IRON_LAWS/semantic_shield.py) — 状态: `HAS_MAIN`

### `scripts/L2_WELDED_PROTOCOLS`

- 🚀 [barrier_monitor.py](scripts/L2_WELDED_PROTOCOLS/barrier_monitor.py) — 状态: `HAS_MAIN`
- 🚀 [dna_verifier.py](scripts/L2_WELDED_PROTOCOLS/dna_verifier.py) — 状态: `HAS_MAIN`
- 🚀 [protocol_auditor.py](scripts/L2_WELDED_PROTOCOLS/protocol_auditor.py) — 状态: `HAS_MAIN`
- 🚀 [weight_calculator.py](scripts/L2_WELDED_PROTOCOLS/weight_calculator.py) — 状态: `HAS_MAIN`

### `scripts/L3_DYNAMIC_GOVERNANCE`

- 🚀 [citizen_feedback_processor.py](scripts/L3_DYNAMIC_GOVERNANCE/citizen_feedback_processor.py) — 状态: `HAS_MAIN`
- 🚀 [governance_resolver.py](scripts/L3_DYNAMIC_GOVERNANCE/governance_resolver.py) — 状态: `HAS_MAIN`
- 🚀 [state_machine_controller.py](scripts/L3_DYNAMIC_GOVERNANCE/state_machine_controller.py) — 状态: `HAS_MAIN`

### `scripts/L4_SUPPLEMENTARY`

- 🚀 [crisis_recovery.py](scripts/L4_SUPPLEMENTARY/crisis_recovery.py) — 状态: `HAS_MAIN`
- 🚀 [supplement_publisher.py](scripts/L4_SUPPLEMENTARY/supplement_publisher.py) — 状态: `HAS_MAIN`

### `scripts/common`

- 🚀 [config.py](scripts/common/config.py) — 状态: `HAS_MAIN`
- 🚀 [dna.py](scripts/common/dna.py) — 状态: `HAS_MAIN`
- 🚀 [logger.py](scripts/common/logger.py) — 状态: `HAS_MAIN`
- 🚀 [utils.py](scripts/common/utils.py) — 状态: `HAS_MAIN`

### `scripts/persona`

- 🚀 [longhun_persona_engine.py](scripts/persona/longhun_persona_engine.py) — 状态: `HAS_MAIN`

### `skill-standards.integrated`

- 🚀 [longhun-skill-auto-completion-engine.py](skill-standards.integrated/longhun-skill-auto-completion-engine.py) — 状态: `HAS_MAIN`
- 🚀 [longhun-standard-calculation-framework.py](skill-standards.integrated/longhun-standard-calculation-framework.py) — 状态: `HAS_MAIN`

### `skills`

- 📖 [SKILL-LAUNCHER.sh](skills/SKILL-LAUNCHER.sh) — 状态: `HELP_OK`
- ✅ [__init__.py](skills/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [api.py](skills/api.py) — 状态: `HAS_MAIN`
- 🚀 [fill_all_skills_specifications.py](skills/fill_all_skills_specifications.py) — 状态: `HAS_MAIN`
- 🚀 [longhun-standard-calculation-framework.py](skills/longhun-standard-calculation-framework.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_skill_auto_completion_engine.py](skills/longhun_skill_auto_completion_engine.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_standard_calculation_framework.py](skills/longhun_standard_calculation_framework.py) — 状态: `HAS_MAIN`
- 🚀 [phase5_performance_benchmark.py](skills/phase5_performance_benchmark.py) — 状态: `HAS_MAIN`
- 🚀 [phase6_cross_skill_integration.py](skills/phase6_cross_skill_integration.py) — 状态: `HAS_MAIN`
- 🚀 [phase7_final_system_acceptance.py](skills/phase7_final_system_acceptance.py) — 状态: `HAS_MAIN`
- 📖 [registry.py](skills/registry.py) — 状态: `HELP_OK`

### `skills.backup`

- ✅ [__init__.py](skills.backup/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [api.py](skills.backup/api.py) — 状态: `HAS_MAIN`
- 🚀 [fill_all_skills_specifications.py](skills.backup/fill_all_skills_specifications.py) — 状态: `HAS_MAIN`
- 🚀 [phase5_performance_benchmark.py](skills.backup/phase5_performance_benchmark.py) — 状态: `HAS_MAIN`
- 🚀 [phase6_cross_skill_integration.py](skills.backup/phase6_cross_skill_integration.py) — 状态: `HAS_MAIN`
- 🚀 [phase7_final_system_acceptance.py](skills.backup/phase7_final_system_acceptance.py) — 状态: `HAS_MAIN`

### `skills.backup/py-skills`

- 🚀 [skill-10-web-artifacts-builder.py](skills.backup/py-skills/skill-10-web-artifacts-builder.py) — 状态: `HAS_MAIN`
- 🚀 [skill-6-mcp-builder.py](skills.backup/py-skills/skill-6-mcp-builder.py) — 状态: `HAS_MAIN`
- 🚀 [skill-7-skill-creator.py](skills.backup/py-skills/skill-7-skill-creator.py) — 状态: `HAS_MAIN`
- 🚀 [skill-8-slack-gif-creator.py](skills.backup/py-skills/skill-8-slack-gif-creator.py) — 状态: `HAS_MAIN`
- 🚀 [skill-9-theme-factory.py](skills.backup/py-skills/skill-9-theme-factory.py) — 状态: `HAS_MAIN`

### `skills/cnsh-aligner`

- 🚀 [cnsh_aligner.py](skills/cnsh-aligner/cnsh_aligner.py) — 状态: `HAS_MAIN`
- 🚀 [script_manager.py](skills/cnsh-aligner/script_manager.py) — 状态: `HAS_MAIN`

### `skills/core`

- 🚀 [longhun_skill_auto_completion_engine.py](skills/core/longhun_skill_auto_completion_engine.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_standard_calculation_framework.py](skills/core/longhun_standard_calculation_framework.py) — 状态: `HAS_MAIN`

### `skills/longhun-audit-integrated`

- 📖 [longhun_audit_integrated.py](skills/longhun-audit-integrated/longhun_audit_integrated.py) — 状态: `HELP_OK`

### `skills/longhun-shield`

- 📖 [longhun_shield_cli.py](skills/longhun-shield/longhun_shield_cli.py) — 状态: `HELP_OK`
- 🚀 [longhun_shield_instruction_protocol.py](skills/longhun-shield/longhun_shield_instruction_protocol.py) — 状态: `HAS_MAIN`
- 🚀 [longhun_shield_system.py](skills/longhun-shield/longhun_shield_system.py) — 状态: `HAS_MAIN`
- 🚀 [shield_test_example.py](skills/longhun-shield/shield_test_example.py) — 状态: `HAS_MAIN`

### `skills/py-skills`

- 🚀 [skill-10-web-artifacts-builder.py](skills/py-skills/skill-10-web-artifacts-builder.py) — 状态: `HAS_MAIN`
- 🚀 [skill-6-mcp-builder.py](skills/py-skills/skill-6-mcp-builder.py) — 状态: `HAS_MAIN`
- 🚀 [skill-7-skill-creator.py](skills/py-skills/skill-7-skill-creator.py) — 状态: `HAS_MAIN`
- 🚀 [skill-8-slack-gif-creator.py](skills/py-skills/skill-8-slack-gif-creator.py) — 状态: `HAS_MAIN`
- 🚀 [skill-9-theme-factory.py](skills/py-skills/skill-9-theme-factory.py) — 状态: `HAS_MAIN`

### `skills/warehouse-audit/scripts`

- 📖 [audit_engine.py](skills/warehouse-audit/scripts/audit_engine.py) — 状态: `HELP_OK`
- 📖 [generate_demo_wms_data.py](skills/warehouse-audit/scripts/generate_demo_wms_data.py) — 状态: `HELP_OK`

### `skills/wucai_coloring`

- ✅ [__init__.py](skills/wucai_coloring/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [audit.py](skills/wucai_coloring/audit.py) — 状态: `HAS_MAIN`
- 🚀 [emotion_scene.py](skills/wucai_coloring/emotion_scene.py) — 状态: `HAS_MAIN`
- 🚀 [runtime_weight.py](skills/wucai_coloring/runtime_weight.py) — 状态: `HAS_MAIN`

### `software-dna`

- 🚀 [dna_encryption.py](software-dna/dna_encryption.py) — 状态: `HAS_MAIN`
- 🚀 [test_encryption.py](software-dna/test_encryption.py) — 状态: `HAS_MAIN`

### `sovereignty`

- ✅ [__init__.py](sovereignty/__init__.py) — 状态: `IMPORT_OK`
- ⚙️ [cli.py](sovereignty/cli.py) — 状态: `MAIN_NO_HELP`
- 🚀 [digital_identity.py](sovereignty/digital_identity.py) — 状态: `HAS_MAIN`
- 🚀 [templates.py](sovereignty/templates.py) — 状态: `HAS_MAIN`

### `sovereignty/portal`

- 🚀 [api_server.py](sovereignty/portal/api_server.py) — 状态: `HAS_MAIN`
- ✅ [knowledge_api.py](sovereignty/portal/knowledge_api.py) — 状态: `IMPORT_OK`
- ✅ [model_router.py](sovereignty/portal/model_router.py) — 状态: `IMPORT_OK`
- 🚀 [portal_public_gateway.py](sovereignty/portal/portal_public_gateway.py) — 状态: `HAS_MAIN`
- ✔️ [启动国家数字身份入口.sh](sovereignty/portal/启动国家数字身份入口.sh) — 状态: `SYNTAX_OK`
- 🚀 [国家数字身份统一认证入口.py](sovereignty/portal/国家数字身份统一认证入口.py) — 状态: `HAS_MAIN`

### `systems/kfpp`

- 🚀 [kfpp_executor_v1.0.py](systems/kfpp/kfpp_executor_v1.0.py) — 状态: `HAS_MAIN`

### `systems/v3`

- 🚀 [DNA追溯链系统_v3.0.py](systems/v3/DNA追溯链系统_v3.0.py) — 状态: `HAS_MAIN`
- ✅ [__init__.py](systems/v3/__init__.py) — 状态: `IMPORT_OK`
- 🚀 [三色审计与10道闸系统_v3.0.py](systems/v3/三色审计与10道闸系统_v3.0.py) — 状态: `HAS_MAIN`
- 🚀 [五行融合决策引擎_v3.0.py](systems/v3/五行融合决策引擎_v3.0.py) — 状态: `HAS_MAIN`
- 🚀 [人格矩阵路由系统_v3.0.py](systems/v3/人格矩阵路由系统_v3.0.py) — 状态: `HAS_MAIN`
- 🚀 [安全域审计协议_v3.0.py](systems/v3/安全域审计协议_v3.0.py) — 状态: `HAS_MAIN`

### `tests`

- ✅ [test_longhun_basic.py](tests/test_longhun_basic.py) — 状态: `IMPORT_OK`

### `tools`

- 📖 [dna_file_filler.py](tools/dna_file_filler.py) — 状态: `HELP_OK`
- 📖 [dna_normalizer.py](tools/dna_normalizer.py) — 状态: `HELP_OK`
- 📖 [dna_python_filler.py](tools/dna_python_filler.py) — 状态: `HELP_OK`
- 📖 [dna_registry_builder.py](tools/dna_registry_builder.py) — 状态: `HELP_OK`
- 🚀 [longhun_ka_batch_importer.py](tools/longhun_ka_batch_importer.py) — 状态: `HAS_MAIN`
- 📖 [longhun_knowledge_manager.py](tools/longhun_knowledge_manager.py) — 状态: `HELP_OK`
- ✔️ [sign_creator_protection.sh](tools/sign_creator_protection.sh) — 状态: `SYNTAX_OK`
- 🚀 [v7_upgrade_orchestrator.py](tools/v7_upgrade_orchestrator.py) — 状态: `HAS_MAIN`

### `tools/gpg-sign-manager`

- 🚀 [cnsh.py](tools/gpg-sign-manager/cnsh.py) — 状态: `HAS_MAIN`
- 🚀 [cnsh_gateway.py](tools/gpg-sign-manager/cnsh_gateway.py) — 状态: `HAS_MAIN`
- ⚙️ [gpg_sign_manager.py](tools/gpg-sign-manager/gpg_sign_manager.py) — 状态: `MAIN_NO_HELP`

### `tools/logging`

- 🚀 [action_logger.py](tools/logging/action_logger.py) — 状态: `HAS_MAIN`
- 🚀 [daily_review.py](tools/logging/daily_review.py) — 状态: `HAS_MAIN`
- 🚀 [daily_review_enhanced.py](tools/logging/daily_review_enhanced.py) — 状态: `HAS_MAIN`

### `tools/normalizers`

- 📖 [dragon_char_normalizer.py](tools/normalizers/dragon_char_normalizer.py) — 状态: `HELP_OK`

### `tools/security`

- 🚀 [sovereign_env_audit.py](tools/security/sovereign_env_audit.py) — 状态: `HAS_MAIN`

### `voice-twin`

- 📖 [draft_generator.py](voice-twin/draft_generator.py) — 状态: `HELP_OK`
- 📖 [military_memory_generator.py](voice-twin/military_memory_generator.py) — 状态: `HELP_OK`
- 📖 [reading_generator.py](voice-twin/reading_generator.py) — 状态: `HELP_OK`
- 📖 [sage_dialogue.py](voice-twin/sage_dialogue.py) — 状态: `HELP_OK`
- 🚀 [style_extractor.py](voice-twin/style_extractor.py) — 状态: `HAS_MAIN`
- 📖 [video_remixer.py](voice-twin/video_remixer.py) — 状态: `HELP_OK`
- 📖 [video_script_generator.py](voice-twin/video_script_generator.py) — 状态: `HELP_OK`
- 📖 [voice_clone_trainer.py](voice-twin/voice_clone_trainer.py) — 状态: `HELP_OK`
- 🚀 [voice_twin_server.py](voice-twin/voice_twin_server.py) — 状态: `HAS_MAIN`
- 📖 [wechat_video_exporter.py](voice-twin/wechat_video_exporter.py) — 状态: `HELP_OK`

### `xpay`

- ✅ [__init__.py](xpay/__init__.py) — 状态: `IMPORT_OK`

### `xpay/src`

- ✅ [__init__.py](xpay/src/__init__.py) — 状态: `IMPORT_OK`
- ✅ [adapter.py](xpay/src/adapter.py) — 状态: `IMPORT_OK`
- 📖 [cli.py](xpay/src/cli.py) — 状态: `HELP_OK`
- ✅ [dna.py](xpay/src/dna.py) — 状态: `IMPORT_OK`
- ✅ [transaction.py](xpay/src/transaction.py) — 状态: `IMPORT_OK`

### `xpay/src/adapters`

- ✅ [__init__.py](xpay/src/adapters/__init__.py) — 状态: `IMPORT_OK`
- ✅ [cny_demo.py](xpay/src/adapters/cny_demo.py) — 状态: `IMPORT_OK`
- ✅ [eur_demo.py](xpay/src/adapters/eur_demo.py) — 状态: `IMPORT_OK`
- ✅ [usd_demo.py](xpay/src/adapters/usd_demo.py) — 状态: `IMPORT_OK`

### `xpay/tests`

- 🚀 [test_gateway.py](xpay/tests/test_gateway.py) — 状态: `HAS_MAIN`

### `龍魂洛书369引擎/wuxing`

- 🚀 [太极递归与五行图论.py](龍魂洛书369引擎/wuxing/太极递归与五行图论.py) — 状态: `HAS_MAIN`

## 快速开始

```bash
# 克隆仓库
git clone <仓库地址>
cd longhun-system

# 安装中文编辑器模块（已独立为可发布包）
pip install -e dev-env/chinese-editor

# 1. 运行 CNSH 脚本示例
cnsh-runtime run dev-env/chinese-editor/examples/hello.cnsh

# 2. 启动本地中文编辑器
longhun-editor editor dev-env/chinese-editor/examples/hello.cnsh --run

# 3. 运行代码审计工具（如存在）
python3 tools/longhun_code_audit_runner.py --help
```

## 贡献规范

1. 所有代码必须经过 `py_compile` / `bash -n` 语法检查
2. 必须包含中文注释和 DNA 追溯标记
3. 涉及外部 API 调用的文件，必须配置化，不硬编码密钥
4. 敏感内容由专属人格/本地模型管理；公开发布前把外部导入或含密钥的文件移入 `_quarantine/`，其余 DNA/GPG 等主权标记保留不动

## 主权声明

- 核心数据主权归 UID9622 / 龍魂社区所有
- 遵循 CNSH 中文原生脚本协议
- 反对任何 AI 平台的记忆绑架与数据垄断

---

**DNA:** `#龍芯⚡️2026-06-26-LONGHUN-TOOLBOX-PUBLIC-v1.1`
