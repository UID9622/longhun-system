# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
---
title: 龍魂系统 · 目录地图 v1.0
dna: "#龍芯⚡️丙午·丙申·庚戌·䷙大畜-DIRECTORY-MAP-v1.0-UID9622"
layer: core-idea
creator: 诸葛鑫（UID9622）
license: CC BY-NC-SA 4.0
status: draft
effective_date: 2026-08-04
---

# 龍魂系统 · 目录地图 v1.0

> DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-DIRECTORY-MAP-v1.0-UID9622
> LAYER: core-idea
> 用途：快速定位任何文件应该放在哪里
> 关联文档：`docs/SYSTEM_STRUCTURE_AUDIT_v1.0.md`

---

## 快速决策表

| 我要放什么 | 放到哪里 | 当前对应路径 |
|:---|:---|:---|
| 协议、治理文档、白皮书 | `01_PROTOCOLS/` | `01_protocols/` |
| 技能定义、投喂存档 | `02_SKILLS/` | `01_技能庫/` |
| 架构分层实现 | `03_LAYERS/` | `layers/` |
| 引擎核心代码 | `04_ENGINES/` | `engines/` |
| API/后端/集成服务 | `05_SERVICES/` | `services/` |
| 终端应用 | `06_APPS/` | `apps/` |
| Web 门户页面 | `07_PORTAL/` | `portal/` |
| CLI 命令脚本 | `08_BIN/` | `bin/` |
| 可复用 SDK/库 | `09_LIBS/` | （待拆分） |
| 知识图谱、数据集 | `10_DATA/` | `data/`、`knowledge-graph/` |
| 文章、教程 | `11_ARTICLES/` | `articles/` |
| 技术文档、架构说明 | `12_DOCS/` | `docs/` |
| 单元/集成/性能测试 | `13_TESTS/` | `tests/`、`benchmarks/` |
| Docker/systemd/nginx 配置 | `14_DEPLOY/` | `deploy/`、`docker/` |
| 活跃实验项目 | `15_LABS/` | `archive/experiments/` |
| 历史归档（只读） | `16_ARCHIVE/` | `archive/` |
| 审计日志、报告 | `17_AUDIT/` | `audit/` |
| 运行时日志 | `18_LOGS/` | `logs/` |
| 字体、图片、音频 | `19_ASSETS/` | `fonts/`、`portal/assets/` |
| 编辑器、工具配置 | `20_CONFIG/` | `.vscode/`、`.devcontainer/` |
| 私密资料（不纳入版本控制） | `21_PRIVATE/` | `_private/` |
| 临时工作区 | `22_WORK/` | `_work/` |
| 第三方集成 | `23_INTEGRATIONS/` | `integrations/` |
| Android 相关 | `24_ANDROID/` | `android-auto/` |
| 宝宝守护 | `25_BAOBAO/` | `baobao-guardian/` |
| 任务引擎 | `26_TASK_ENGINE/` | `25_TASK_ENGINE/` |

---

## 目标目录详解

### 00_META/ — 项目元数据与入口

| 文件 | 用途 |
|:---|:---|
| `README.md` | 人类入口：介绍、快速启动、链接 |
| `AGENTS.md` | AI 操作手册：规则、铁律、命令 |
| `LICENSE` | 分层双许可证声明 |
| `CHANGELOG.md` | 版本变更日志 |
| `ROADMAP.md` | 路线图 |
| `CONTRIBUTING.md` | 贡献指南 |
| `CODE_OF_CONDUCT.md` | 社区行为准则 |

---

### 01_PROTOCOLS/ — 协议·治理·白皮书

**核心思想层（CC BY-NC-SA 4.0）**

| 子目录 | 用途 |
|:---|:---|
| `constitution/` | 系统宪法、根本规则 |
| `governance/` | 治理模型、决策流程 |
| `audit/` | 审计协议、方法论 |
| `cnsh/` | CNSH 语言规范 |
| `privacy/` | 隐私政策、数据主权 |
| `security/` | 安全策略 |
| `archive/` | 已废止协议 |

**当前映射**：`01_protocols/`

---

### 02_SKILLS/ — 技能库

**核心思想层 + 工程实现层混合**

| 子目录 | 用途 |
|:---|:---|
| `active/` | 当前激活的技能定义 |
| `archive/` | 历史技能 |
| `registry.json` | 技能注册表 |

**当前映射**：`01_技能庫/`

---

### 03_LAYERS/ — 架构分层

**工程实现层（MulanPSL v2）**

| 子目录 | 职责 | 当前映射 |
|:---|:---|:---|
| `L0_hardware/` | 物理层、设备层 | `L0_物理层` |
| `L1_kernel/` | 内核、身份、安全底座 | `L1_内核层` + `L1_身份层` |
| `L2_capability/` | 技能、主权、能力编排 | `L2_技能层` + `L2_主权层` |
| `L3_data/` | 数据存储、schema、流 | `L3_数据层` |
| `L4_semantic/` | 语义、翻译、知识表示 | `L3_语义层` |
| `L5_service/` | 服务编排、API、集成 | `L5_服务层` |
| `L6_memory/` | 记忆、同步、状态 | `L6_记忆层` + `L6_同步层` |
| `L7_expression/` | 表达、交互、前端 | `L7_表达层` |
| `L8_governance/` | 治理、审计、决策 | `L8_治理层` + `03_后土OS/` |
| `L9_subsystems/` | 子系统、独立应用 | `L9_子系统` |

---

### 04_ENGINES/ — 引擎

| 子目录 | 用途 |
|:---|:---|
| `core/` | 核心引擎 |
| `audit/` | 审计引擎 |
| `ant_colony/` | 蚁群算法引擎 |
| `avatar/` | 数字人引擎 |
| `guanlan/` | 观澜引擎 |
| `legacy/` | 废弃引擎（兼容期） |

**当前映射**：`engines/`（需清理 `legacy_runtime`、`__pycache__`）

---

### 05_SERVICES/ — 服务

| 子目录 | 用途 |
|:---|:---|
| `api/` | REST/WebSocket API |
| `portal/` | 门户后端 |
| `integrations/` | 第三方集成后端 |
| `legacy/` | 遗留后端（兼容期） |

**当前映射**：`services/`

---

### 06_APPS/ — 终端应用

| 子目录 | 用途 |
|:---|:---|
| `homeowner-toolkit/` | 业主工具包 |

**当前映射**：`apps/`

---

### 07_PORTAL/ — Web 门户

| 子目录 | 用途 |
|:---|:---|
| `dashboard/` | 仪表盘 |
| `ai-hub/` | AI Hub |
| `audit-battle-hub/` | 审计对抗中枢 |
| `civil-audit/` | 民生审计 |
| `dna-generator/` | DNA 生成器 |
| `warp-lab/` | 曲速引擎 |
| ... | 其他门户 |

**当前映射**：`portal/`

---

### 08_BIN/ — 命令工具

| 子目录 | 用途 |
|:---|:---|
| `core/` | 系统核心命令 |
| `skills/` | 技能命令 |
| `audit/` | 审计命令 |
| `deploy/` | 部署命令 |
| `dev/` | 开发调试命令 |
| `data/` | 数据命令 |
| `legacy/` | 废弃命令（兼容期） |

**当前映射**：`bin/`（2,003 个文件需分类）

---

### 09_LIBS/ — SDK/库

| 子目录 | 用途 |
|:---|:---|
| `cnsh/` | CNSH 运行时库 |

**当前状态**：待从 `engines/`、`services/` 中拆分。

---

### 10_DATA/ — 数据资产

| 子目录 | 用途 |
|:---|:---|
| `knowledge-graph/` | 知识图谱 |
| `memory/` | 记忆数据 |
| `registry/` | 注册表数据 |

**当前映射**：`data/`、`knowledge-graph/`

---

### 11_ARTICLES/ — 文章与教程

| 子目录 | 用途 |
|:---|:---|
| `zh/` | 中文文章 |
| `en/` | 英文文章 |
| `csdn/` | CSDN 同步版 |
| `arxiv/` | 学术论文 |

**当前映射**：`articles/`、`arxiv/`

---

### 12_DOCS/ — 技术文档

| 子目录 | 用途 |
|:---|:---|
| `architecture/` | 架构文档 |
| `api/` | API 文档 |
| `development/` | 开发者文档 |
| `faq/` | FAQ |
| `glossary/` | 术语表 |
| `tech/` | 技术细节 |

**当前映射**：`docs/`

---

### 13_TESTS/ — 测试

| 子目录 | 用途 |
|:---|:---|
| `unit/` | 单元测试 |
| `integration/` | 集成测试 |
| `benchmark/` | 性能测试 |

**当前映射**：`tests/`、`benchmarks/`

---

### 14_DEPLOY/ — 部署配置

| 子目录 | 用途 |
|:---|:---|
| `docker/` | Docker 配置 |
| `systemd/` | Systemd 服务 |
| `nginx/` | Nginx 配置 |
| `scripts/` | 部署脚本 |

**当前映射**：`docker/`、`deploy/`

---

### 15_LABS/ — 活跃实验

| 子目录 | 用途 |
|:---|:---|
| `forensic-kernel/` | 取证内核 |
| `memory-universe/` | 记忆宇宙 |
| `ops-console/` | 运维控制台 |
| `rag-indexes/` | RAG 索引 |

**当前映射**：`archive/experiments/` 中活跃项目

---

### 16_ARCHIVE/ — 历史归档（只读）

| 子目录 | 用途 |
|:---|:---|
| `backups/` | 备份 |
| `experiments-frozen/` | 已冻结实验 |
| `legacy/` | 遗留代码 |
| `records/` | 执行记录、决策日志、系统报告 |

**当前映射**：`archive/`、`_archive/`、各类历史 Symlink

---

### 17_AUDIT/ — 审计数据

| 子目录 | 用途 |
|:---|:---|
| `logs/` | 审计日志 |
| `reports/` | 审计报告 |
| `ethics/` | 伦理快照 |
| `backups/` | 审计备份 |

**当前映射**：`audit/`

---

### 18_LOGS/ — 运行时日志

| 子目录 | 用途 |
|:---|:---|
| `services/` | 服务日志 |
| `tasks/` | 任务日志 |
| `archive/` | 日志归档 |

**当前映射**：`logs/`

---

### 19_ASSETS/ — 静态资产

| 子目录 | 用途 |
|:---|:---|
| `fonts/` | 字体 |
| `images/` | 图片 |
| `sounds/` | 音频 |

**当前映射**：`fonts/`、`portal/*/assets/`

---

### 20_CONFIG/ — 配置文件

| 子目录 | 用途 |
|:---|:---|
| `vscode/` | VS Code 配置 |
| `devcontainer/` | Dev Container 配置 |
| `bandit/` | Bandit 配置 |
| `git-hooks/` | Git Hooks |

**当前映射**：`.vscode/`、`.devcontainer/`、`.bandit.yaml`、`.githooks/`

---

### 21_PRIVATE/ — 私密资料

> ⚠️ 不纳入版本控制。

| 子目录 | 用途 |
|:---|:---|
| `id-documents/` | 身份资料 |
| `vault/` | 密钥保险库 |
| `keys/` | 密钥资料 |

**当前映射**：`_private/`

---

### 22_WORK/ — 临时工作区

> 中间产物、临时文件、待处理数据。

**当前映射**：`_work/`

---

### 23_INTEGRATIONS/ — 第三方集成

| 子目录 | 用途 |
|:---|:---|
| `mcp/` | MCP Server |
| `wechat/` | 微信集成 |
| `android-auto/` | Android Auto |

**当前映射**：`integrations/`、`android-auto/`

---

### 24_ANDROID/ — Android 相关

**当前映射**：`android-auto/`

---

### 25_BAOBAO/ — 宝宝守护

**当前映射**：`baobao-guardian/`

---

### 26_TASK_ENGINE/ — 任务引擎

**当前映射**：`25_TASK_ENGINE/`

---

## 附录 · 当前 → 目标路径映射速查

| 当前路径 | 目标路径 | 优先级 |
|:---|:---|:---:|
| `01_protocols/` | `01_PROTOCOLS/` | P0 |
| `01_技能庫/` | `02_SKILLS/` | P0 |
| `layers/` | `03_LAYERS/` | P0 |
| `engines/` | `04_ENGINES/` | P0 |
| `services/` | `05_SERVICES/` | P0 |
| `apps/` | `06_APPS/` | P1 |
| `portal/` | `07_PORTAL/` | P0 |
| `bin/` | `08_BIN/` | P0 |
| `articles/` | `11_ARTICLES/` | P1 |
| `docs/` | `12_DOCS/` | P0 |
| `tests/` | `13_TESTS/` | P1 |
| `docker/`、`deploy/` | `14_DEPLOY/` | P1 |
| `archive/experiments/` 活跃项 | `15_LABS/` | P2 |
| `archive/` | `16_ARCHIVE/` | P1 |
| `audit/` | `17_AUDIT/` | P1 |
| `logs/` | `18_LOGS/` | P2 |
| `_private/` | `21_PRIVATE/` | P0 |
| `_work/` | `22_WORK/` | P1 |
| `baobao-guardian/` | `25_BAOBAO/` | P2 |
| `25_TASK_ENGINE/` | `26_TASK_ENGINE/` | P1 |

---

> 🐉 **知道东西在哪里，比知道东西是什么更重要。**
>
> 本文件适用 CC BY-NC-SA 4.0。
