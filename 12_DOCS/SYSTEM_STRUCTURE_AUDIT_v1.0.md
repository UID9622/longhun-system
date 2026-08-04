# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
---
title: 龍魂系统 · 系统结构审计与重组方案 v1.0
dna: "#龍芯⚡️丙午·丙申·庚戌·䷙大畜-SYSTEM-STRUCTURE-AUDIT-v1.0-UID9622"
layer: core-idea
creator: 诸葛鑫（UID9622）
license: CC BY-NC-SA 4.0
status: draft
review_cycle: 6个月
effective_date: 2026-08-04
auditor: P05
tags:
  - system-architecture
  - directory-structure
  - governance
  - automation
  - restructure
  - 龍魂
---

# 龍魂系统 · 系统结构审计与重组方案 v1.0

> DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SYSTEM-STRUCTURE-AUDIT-v1.0-UID9622
> LAYER: core-idea
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0
> 生效日期: 2026-08-04
> 审计色: 🟡 结构重组方案·待 P05 审议

---

## 目录

1. [执行摘要](#1-执行摘要)
2. [审计范围与方法](#2-审计范围与方法)
3. [当前结构现状](#3-当前结构现状)
4. [核心问题诊断](#4-核心问题诊断)
5. [重组目标与原则](#5-重组目标与原则)
6. [目标架构蓝图](#6-目标架构蓝图)
7. [目录命名规范](#7-目录命名规范)
8. [自动化治理规则](#8-自动化治理规则)
9. [迁移路线图](#9-迁移路线图)
10. [附录A · 当前目录完整清单](#附录a--当前目录完整清单)
11. [附录B · Symlink 清理清单](#附录b--symlink-清理清单)
12. [附录C · 推荐文件头模板](#附录c--推荐文件头模板)
13. [附录D · 自动化脚本规格](#附录d--自动化脚本规格)

---

## 1. 执行摘要

龍魂系统从"一人项目"成长为"生态底座"，当前文件系统已出现**结构熵增**迹象：顶层目录过多、中英文混用、符号链接泛滥、历史归档与活跃代码交织。本审计报告提出一套**分层、命名统一、自动化可治理**的重组方案，目标是让 AI Agent 和人类开发者都能在最短时间内定位任何文件，同时保持龍魂的文化主权与技术开放性。

**关键数字（截至 2026-08-04）**：

| 指标 | 数值 | 健康阈值 | 状态 |
|:---|:---:|:---:|:---:|
| 顶层目录数 | ~106 | ≤30 | 🔴 严重超标 |
| 顶层 Symlink 数 | ~25 | ≤5 | 🔴 过多 |
| `bin/` 文件数 | 2,003 | 建议按模块拆分 | 🟡 需要治理 |
| `01_protocols/` 子目录 | 24 | ≤15 | 🟡 偏多 |
| `layers/` 子目录 | 18 | 建议合并重复层 | 🟡 需要整理 |
| 文档入口文件 | 1 个 README | ≥3 个互补索引 | 🟡 不足 |

**核心建议**：
1. 将顶层目录压缩到 **30 个以内**。
2. 统一目录命名：**英文小写 + 数字前缀**，废止繁体中文目录名作为正式入口。
3. 清理或归档 **80% 的 Symlink**，只保留必要的向后兼容入口。
4. 为每个活跃目录生成 `README.md` 和 `.layer_tag`。
5. 部署自动化脚本：目录健康检查、命名合规校验、 orphan 文件扫描。

---

## 2. 审计范围与方法

### 2.1 审计范围

- 根目录 `/Users/zuimeidedeyihan/longhun-system/`
- 顶层目录、文件、符号链接
- 关键子系统：`01_protocols/`、`layers/`、`bin/`、`services/`、`engines/`、`portal/`、`docs/`、`audit/`
- 已存在索引：`.inventory.json`、`AGENTS.md`、`README.md`

### 2.2 审计方法

| 方法 | 工具/命令 | 输出 |
|:---|:---|:---|
| 目录枚举 | `find . -maxdepth 1 -type d` | 顶层目录清单 |
| Symlink 扫描 | `find . -maxdepth 1 -type l` | 符号链接清单 |
| 文件计数 | `ls bin/ \| wc -l` | 模块规模评估 |
| 协议分类 | `find 01_protocols -maxdepth 2 -type d` | 协议组织评估 |
| 结构一致性 | 人工审查 | 命名规范、重复层、语义冲突 |

---

## 3. 当前结构现状

### 3.1 顶层目录全景

当前根目录包含约 **106 个目录** 和 **25 个符号链接**，远超一个中型开源项目的合理规模。主要入口可分为以下几类：

#### 3.1.1 协议与治理（🏛️ 核心思想层）

| 目录 | 说明 | 问题 |
|:---|:---|:---|
| `01_protocols/` | 协议、白皮书、治理文档 | 子目录 24 个，部分命名不统一 |
| `01_技能庫/` | 技能投喂存档 | 繁体中文目录名，应改为 `01_skills/` |
| `02_rules/` → `.codebuddy/rules/archive` | 对齐规则 | Symlink，可保留但需明确 |
| `02_執行記錄/` → `archive/历史记录/02_執行記錄` | 执行记录 | Symlink + 繁体，应整合到 `archive/records/` |
| `04_決策日誌/` | 决策日志 | Symlink，应整合 |
| `05_系統報告/` | 系统报告 | Symlink，应整合 |
| `06_技術文檔/` → `docs/tech` | 技术文档 | Symlink，应移除 |

#### 3.1.2 架构分层（🔧 工程实现层）

| 目录 | 说明 | 问题 |
|:---|:---|:---|
| `layers/` | L0-L9 架构分层 | 存在重复层名：`L3_数据层`、`L4_数据层`、`L7_数据层` |
| `L1_内核层` → `layers/L1_内核层` | 重复入口 | Symlink，应移除 |
| `L9_子系统` → `layers/L9_子系统` | 重复入口 | Symlink，应移除 |
| `services/` | API、后端、集成 | 结构合理，需整理 `backend_legacy` |
| `engines/` | 引擎集合 | 包含 `legacy_runtime`、`__pycache__`，需清理 |
| `portal/` | Web 门户集合 | 子项目多，需统一入口 |
| `apps/` | 应用 | 当前只有 `homeowner-toolkit`，规模小 |

#### 3.1.3 数据与资产

| 目录 | 说明 | 问题 |
|:---|:---|:---|
| `data/` | 数据 | 需确认是否活跃 |
| `logs/` | 日志 | 活跃，但需轮转策略 |
| `audit/` | 审计数据 | 活跃，需索引 |
| `_work/` | 工作区 | 私有/临时，应明确标注 |
| `_private/` | 私密资料 | 不应纳入版本控制 |
| `_archive/` | 归档 | 合理，需索引 |
| `archive/` | 历史归档 | 内容庞杂，需二级分类 |

#### 3.1.4 实验与历史堆积

| 目录 | 说明 | 问题 |
|:---|:---|:---|
| `archive/experiments/` | 实验项目 | 大量实验目录堆积 |
| `forensic_kernel` → `archive/experiments/forensic_kernel` | 取证内核实验 | 实验项目不应在顶层 |
| `memory-universe` → `archive/experiments/memory-universe` | 记忆宇宙实验 | 同上 |
| `ops-console` → `archive/experiments/ops-console` | 运维控制台实验 | 同上 |
| `rag_indexes` → `archive/experiments/rag_indexes` | RAG 索引实验 | 同上 |
| `calendar-context-logger` → `archive/experiments/...` | 日历上下文日志实验 | 同上 |

### 3.2 `bin/` 目录规模

`bin/` 目录当前包含 **2,003 个文件**，是系统的命令中枢。存在的问题：

- 没有子目录分类，所有命令平铺。
- 命名风格不一致：`lh_*.py`、中文名、`_legacy`、`_v1`、`_v2` 等后缀混用。
- 部分脚本可能已废弃，但无明确标记。

**建议**：按功能域拆分为 `bin/core/`、`bin/skills/`、`bin/audit/`、`bin/deploy/`、`bin/legacy/` 等。

### 3.3 `layers/` 分层重复问题

`layers/` 子目录列表：

```
L0_物理层
L1_内核层
L1_身份层
L2_技能层
L2_主权层
L3_数据层
L3_语义层
L3_执行层
L4_数据层      ← 与 L3_数据层重复
L5_服务层
L6_集成层
L6_记忆层
L6_同步层
L7_表达层
L7_数据层      ← 再次出现数据层
L8_分发层
L8_治理层
L9_子系统
```

**问题**：
- "数据层"在 L3、L4、L7 三个层级出现，职责边界模糊。
- 单层出现多个子层（L1 有内核+身份，L2 有技能+主权），说明层级粒度不均。

**建议**：重新定义 L0-L9 每层单一职责，将重复概念合并或降维。

---

## 4. 核心问题诊断

### 4.1 问题一：顶层目录过多（🔴 严重）

**现象**：106 个顶层目录，远超认知负荷。

**影响**：
- 新加入的 AI Agent 无法快速理解系统边界。
- 查找文件依赖记忆而非规则。
- 自动化脚本难以稳定遍历。

**根因**：
- 历史演进中未做定期归档。
- 实验项目未在完成后迁移到 `archive/experiments/`。
- 过度使用 Symlink 作为快捷入口。

### 4.2 问题二：命名不统一（🔴 严重）

**现象**：中英文混用、繁简混用、数字前缀不一致。

| 反例 | 问题 |
|:---|:---|
| `01_protocols/` + `01_技能庫/` | 中英文目录同级，风格割裂 |
| `03_后土OS/` + `03_知識圖譜/` | 繁体、产品名、技术术语混用 |
| `L1_内核层` vs `layers/L1_内核层` | 同一内容两个入口 |
| `articles/` vs `06_技術文檔/` | 都是文档，分散多处 |

**建议**：顶层目录统一使用 `NN_english-name/` 格式；中文语义通过内部 `README.md` 解释。

### 4.3 问题三：Symlink 泛滥（🔴 严重）

**现象**：约 25 个顶层 Symlink，多数指向 `archive/experiments/` 或 `layers/`。

**影响**：
- 造成"文件在这里"的错觉。
- 某些工具（如 `ripgrep`、`find`）默认跟随 Symlink，导致重复扫描。
- 增加认知复杂度。

**建议**：
- 只保留 3-5 个必要的向后兼容 Symlink（如 `docs` → `docs/` 不存在的情况）。
- 其余全部移除，在迁移日志中记录旧路径映射。

### 4.4 问题四：`bin/` 未分类（🟡 中等）

**现象**：2,003 个命令平铺。

**影响**：
- 命令发现困难。
- 自动化补全、帮助生成复杂。
- 废弃命令与新命令混杂。

**建议**：按功能域拆分，并建立 `bin/README.md` 命令索引。

### 4.5 问题五：归档与活跃代码交织（🟡 中等）

**现象**：`archive/` 中既有历史备份，又有活跃实验；`engines/` 中 `legacy_runtime` 与核心引擎并列。

**影响**：
- 难以判断哪些代码仍在维护。
- 自动化部署可能误打包废弃代码。

**建议**：
- `archive/` 只做只读历史归档。
- 活跃实验放入 `labs/` 或 `experiments/`。
- 废弃代码明确标记为 `DEPRECATED`。

### 4.6 问题六：缺乏自动化结构治理（🟡 中等）

**现象**：没有针对目录结构的 CI 检查。

**影响**：
- 新文件随意存放。
- 命名违规难以发现。
- 孤儿文件、空目录、重复文件累积。

**建议**：部署 `scripts/structure-audit.py`，定期生成结构健康报告。

---

## 5. 重组目标与原则

### 5.1 重组目标

1. **30 个顶层目录以内**：将当前 106 个压缩到 30 个以内。
2. **命名统一**：全部使用 `NN_english-name/` 格式，废止繁体中文顶层目录名。
3. **Symlink 清理**：只保留 5 个以内必要的兼容入口。
4. **`bin/` 分类**：按功能域拆分子目录。
5. **`layers/` 归一**：每层单一职责，消除重复层名。
6. **自动化治理**：目录健康检查、命名合规校验、orphan 文件扫描纳入 CI。
7. **三个互补索引**：`README.md`（人类）、`docs/DIRECTORY_MAP.md`（结构）、`.inventory.json`（机器）。

### 5.2 重组原则

| 原则 | 说明 |
|:---|:---|
| **分层原则** | 思想层与工程层分离，归档与活跃分离 |
| **单一职责** | 每个目录只做一件事，不混合多类资产 |
| **命名稳定** | 目录名一旦确定不轻易变更，变更需走迁移流程 |
| **向后兼容** | 旧路径通过 6 个月过渡期 + 重定向脚本兼容 |
| **自动化优先** | 任何结构规则必须可被脚本检查 |
| **文化主权** | 中文语义保留在 README 与文档中，目录名使用英文以便国际化工具链 |

---

## 6. 目标架构蓝图

### 6.1 顶层目录（目标：26 个）

```
/Users/zuimeidedeyihan/longhun-system/
│
├── 00_META/                    # 项目元数据与入口
│   ├── README.md
│   ├── AGENTS.md
│   ├── LICENSE
│   ├── CHANGELOG.md
│   └── ROADMAP.md
│
├── 01_PROTOCOLS/               # 协议·治理·白皮书（核心思想层）
│   ├── constitution/
│   ├── governance/
│   ├── audit/
│   ├── cnsk/
│   ├── privacy/
│   └── archive/
│
├── 02_SKILLS/                  # 技能库（原 01_技能庫）
│   ├── active/
│   ├── archive/
│   └── registry.json
│
├── 03_LAYERS/                  # 架构分层（原 layers/）
│   ├── L0_hardware/
│   ├── L1_kernel/
│   ├── L2_capability/
│   ├── L3_data/
│   ├── L4_semantic/
│   ├── L5_service/
│   ├── L6_memory/
│   ├── L7_expression/
│   ├── L8_governance/
│   └── L9_subsystems/
│
├── 04_ENGINES/                 # 引擎（原 engines/，去 legacy）
│   ├── core/
│   ├── audit/
│   ├── ant_colony/
│   ├── avatar/
│   └── guanlan/
│
├── 05_SERVICES/                # 服务（原 services/）
│   ├── api/
│   ├── portal/
│   ├── integrations/
│   └── legacy/                 # 明确标记为 legacy
│
├── 06_APPS/                    # 终端应用（原 apps/）
│   └── homeowner-toolkit/
│
├── 07_PORTAL/                  # Web 门户（原 portal/）
│   ├── dashboard/
│   ├── ai-hub/
│   ├── audit-battle-hub/
│   └── ...
│
├── 08_BIN/                     # 命令工具（原 bin/ 分类）
│   ├── core/
│   ├── skills/
│   ├── audit/
│   ├── deploy/
│   ├── dev/
│   └── legacy/
│
├── 09_LIBS/                    # SDK/库（可 pip install 的模块）
│   └── cnsh/
│
├── 10_DATA/                    # 数据资产
│   ├── knowledge-graph/
│   ├── memory/
│   └── registry/
│
├── 11_ARTICLES/                # 文章与教程（原 articles/）
│   ├── zh/
│   ├── en/
│   └── csdn/
│
├── 12_DOCS/                    # 技术文档（原 docs/）
│   ├── architecture/
│   ├── api/
│   ├── development/
│   └── faq/
│
├── 13_TESTS/                   # 测试代码（统一入口）
│   ├── unit/
│   ├── integration/
│   └── benchmark/
│
├── 14_DEPLOY/                  # 部署配置
│   ├── docker/
│   ├── systemd/
│   ├── nginx/
│   └── scripts/
│
├── 15_LABS/                    # 活跃实验（从 archive/experiments 迁移）
│   ├── forensic-kernel/
│   ├── memory-universe/
│   └── ops-console/
│
├── 16_ARCHIVE/                 # 历史归档（只读）
│   ├── backups/
│   ├── experiments-frozen/
│   ├── legacy/
│   └── records/
│
├── 17_AUDIT/                   # 审计数据（原 audit/）
│   ├── logs/
│   ├── reports/
│   ├── ethics/
│   └── backups/
│
├── 18_LOGS/                    # 运行时日志
│   ├── services/
│   ├── tasks/
│   └── archive/
│
├── 19_ASSETS/                  # 静态资产
│   ├── fonts/
│   ├── images/
│   └── sounds/
│
├── 20_CONFIG/                  # 配置文件
│   ├── vscode/
│   ├── devcontainer/
│   ├── bandit/
│   └── git-hooks/
│
├── 21_PRIVATE/                 # 私密资料（不纳入版本控制）
│   └── README.md
│
├── 22_WORK/                    # 工作区（临时/中间产物）
│   └── README.md
│
├── 23_INTEGRATIONS/            # 第三方集成
│   ├── mcp/
│   ├── wechat/
│   └── android-auto/
│
├── 24_ANDROID/                 # Android 相关
│   └── auto/
│
├── 25_BAOBAO/                  # 宝宝守护（原 baobao-guardian/）
│   └── ...
│
├── 26_TASK_ENGINE/             # 任务引擎（原 25_TASK_ENGINE/）
│   └── ...
│
└── scripts/                    # 系统级脚本（跨目录）
    ├── structure-audit.py
    ├── license-audit.py
    └── onboarding.py
```

### 6.2 关键变更说明

| 原路径 | 目标路径 | 理由 |
|:---|:---|:---|
| `01_protocols/` | `01_PROTOCOLS/` | 统一大写，保留数字前缀 |
| `01_技能庫/` | `02_SKILLS/` | 废止繁体中文顶层名 |
| `03_后土OS/` | 移入 `03_LAYERS/L8_governance/` 或 `15_LABS/` | 按性质归类 |
| `03_知識圖譜/` | `10_DATA/knowledge-graph/` | 数据资产归位 |
| `layers/` | `03_LAYERS/` | 统一数字前缀 |
| `L1_内核层` 等 Symlink | 删除 | 直接访问 `03_LAYERS/` |
| `bin/` | `08_BIN/` | 分类子目录 |
| `services/` | `05_SERVICES/` | 统一数字前缀 |
| `engines/` | `04_ENGINES/` | 统一数字前缀 |
| `portal/` | `07_PORTAL/` | 统一数字前缀 |
| `articles/` | `11_ARTICLES/` | 统一数字前缀 |
| `docs/` | `12_DOCS/` | 统一数字前缀，注意与 `00_META/README.md` 互补 |
| `archive/` | `16_ARCHIVE/` | 明确只读归档 |
| `_work/` | `22_WORK/` | 去除下划线私有前缀，明确为工作区 |
| `_private/` | `21_PRIVATE/` | 明确为私密区，不纳入版本控制 |
| `android-auto/` | `24_ANDROID/` | 归类 |
| `baobao-guardian/` | `25_BAOBAO/` | 归类 |
| `25_TASK_ENGINE/` | `26_TASK_ENGINE/` | 调整数字前缀 |

### 6.3 `03_LAYERS/` 归一化方案

将重复层名合并，每层只保留一个核心职责：

| 新层级 | 职责 | 原目录映射 |
|:---|:---|:---|
| `L0_hardware/` | 物理层、设备层 | `L0_物理层` |
| `L1_kernel/` | 内核、身份、安全底座 | `L1_内核层` + `L1_身份层` |
| `L2_capability/` | 技能、主权、能力编排 | `L2_技能层` + `L2_主权层` |
| `L3_data/` | 数据存储、 schema、流 | `L3_数据层` |
| `L4_semantic/` | 语义、翻译、知识表示 | `L3_语义层` |
| `L5_service/` | 服务编排、API、集成 | `L5_服务层` |
| `L6_memory/` | 记忆、同步、状态 | `L6_记忆层` + `L6_同步层` |
| `L7_expression/` | 表达、交互、前端 | `L7_表达层` |
| `L8_governance/` | 治理、审计、决策 | `L8_治理层` + `03_后土OS/` |
| `L9_subsystems/` | 子系统、独立应用 | `L9_子系统` |

> 注：`L3_执行层`、`L4_数据层`、`L6_集成层`、`L7_数据层`、`L8_分发层` 按实际内容分别并入 `L3_data/`、`L5_service/`、`L6_memory/`、`L7_expression/`。

### 6.4 `08_BIN/` 分类方案

```
08_BIN/
├── core/           # 系统核心命令（启动、状态、健康、记忆）
├── skills/         # 技能相关命令
├── audit/          # 审计、检查、修复
├── deploy/         # 部署、发布、同步
├── dev/            # 开发、测试、调试
├── data/           # 数据导入、导出、迁移
├── legacy/         # 废弃命令，保留兼容
└── README.md       # 命令索引
```

---

## 7. 目录命名规范

### 7.1 顶层目录命名

格式：
```
NN_CATEGORY-NAME/
```

规则：
- `NN`：两位数字前缀，用于排序和快速识别。
- `CATEGORY-NAME`：英文小写，单词间用连字符 `-` 连接。
- 不使用下划线 `_` 作为单词分隔符（技术工具常将下划线视为单词边界）。
- 不使用中文、日文、繁体中文作为目录名。
- 不存放文件在根目录，根目录只保留入口文件。

### 7.2 子目录命名

- 使用英文小写 + 连字符。
- 技术子目录可使用下划线（如 `unit_tests/`）。
- 版本号建议放在目录内部文件命名中，而非目录名中。

### 7.3 文件命名

- 协议文件：`LH-<NAME>-v<MAJOR>.<MINOR>.md`
- 代码文件：`lh_<domain>_<action>.py`
- 配置文件：`<tool>.<ext>`，如 `pyproject.toml`
- 归档文件：`<YYYYMMDD>-<description>.<ext>`

### 7.4 禁止事项

| 禁止 | 示例 | 正确 |
|:---|:---|:---|
| 顶层中文目录 | `01_技能庫/` | `02_SKILLS/` |
| 顶层繁体目录 | `03_知識圖譜/` | `10_DATA/knowledge-graph/` |
| 产品名作为顶层 | `03_后土OS/` | `03_LAYERS/L8_governance/` |
| 无意义 Symlink | `core -> archive/experiments/core` | 删除 |
| 平铺所有命令 | `bin/` 2003 个文件 | `08_BIN/<domain>/` |

---

## 8. 自动化治理规则

### 8.1 目标

让系统结构成为"可检查、可修复、可追溯"的治理对象，而非依赖个人记忆。

### 8.2 自动化检查项

| 检查项 | 规则 | 触发时机 |
|:---|:---|:---|
| 顶层目录数量 | ≤30 | 每次 PR / 每周 |
| 顶层 Symlink 数量 | ≤5 | 每次 PR / 每周 |
| 目录命名合规 | `NN_english-name/` 格式 | 每次 PR |
| 文件头 LAYER 标签 | 所有 `.py` / `.md` 必须携带 | 每次 PR |
| `bin/` 文件分类 | 必须位于 `08_BIN/<domain>/` | 每次 PR |
| 孤儿文件扫描 | 90 天未修改且无引用的文件标 🟡 | 每周 |
| 重复文件名 | 同名文件在不同目录需说明理由 | 每周 |
| 归档目录只读 | `16_ARCHIVE/` 禁止写入新活跃代码 | 每次 PR |
| README 覆盖率 | 每个顶层目录必须有 `README.md` | 每次 PR |
| `.layer_tag` 文件 | 每个活跃目录必须有该文件 | 每次 PR |

### 8.3 `.layer_tag` 规范

每个活跃目录应包含 `.layer_tag` 文件，用于机器识别：

```yaml
# .layer_tag
name: 03_LAYERS
layer: engineering
owner: UID9622
status: active
review_cycle: 6months
last_reviewed: 2026-08-04
dna: "#龍芯⚡️丙午·丙申·庚戌·LAYERS-v1.0-UID9622"
description: "龍魂系统架构分层实现"
notes: "禁止在目录内混合思想层文档"
```

### 8.4 自动化脚本规格

#### 8.4.1 `scripts/structure-audit.py`

功能：扫描仓库结构健康度。

```bash
python3 scripts/structure-audit.py --format=json --output=reports/structure-audit.json
```

输出示例：

```json
{
  "dna": "#龍芯⚡️20260804-STRUCTURE-AUDIT-UID9622",
  "timestamp": "2026-08-04T16:00:00Z",
  "status": "warn",
  "top_level_dirs": 106,
  "top_level_symlinks": 25,
  "top_level_files": 48,
  "checks": [
    {
      "name": "top_level_dir_count",
      "status": "fail",
      "value": 106,
      "threshold": 30,
      "message": "顶层目录数 106，超出阈值 30"
    },
    {
      "name": "naming_compliance",
      "status": "fail",
      "violations": [
        "01_技能庫/",
        "03_后土OS/",
        "03_知識圖譜/"
      ]
    },
    {
      "name": "orphan_files",
      "status": "warn",
      "count": 23,
      "files": [
        "engines/lh_old_tool.py",
        "portal/chat-widget-v1.html"
      ]
    }
  ]
}
```

#### 8.4.2 `scripts/restructure-plan.py`

功能：生成重组执行计划。

```bash
python3 scripts/restructure-plan.py --dry-run --source=. --output=restructure-plan.json
python3 scripts/restructure-plan.py --apply --source=. --output=restructure-log.json
```

#### 8.4.3 `scripts/migrate-symlinks.py`

功能：分析 Symlink 影响，生成清理建议。

```bash
python3 scripts/migrate-symlinks.py --report
```

### 8.5 CI 集成

```yaml
# .github/workflows/structure-audit.yml
name: 龍魂系统结构审计
on: [push, pull_request]
jobs:
  structure-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: 结构健康检查
        run: python3 scripts/structure-audit.py --fail-on-error
      - name: 目录命名合规
        run: python3 scripts/validate-naming.py --strict
      - name: 生成结构报告
        run: python3 scripts/structure-audit.py --format=markdown --output=reports/structure-audit.md
```

---

## 9. 迁移路线图

### 9.1 阶段一：元数据与索引（第 1-2 周）

| 任务 | 负责人 | 产出 |
|:---|:---:|:---|
| 创建 `docs/SYSTEM_STRUCTURE_AUDIT_v1.0.md` | AI+P05 | 本文件 |
| 创建 `docs/DIRECTORY_MAP.md` | AI | 目录地图 |
| 更新 `README.md` 导航 | AI | 新增结构索引链接 |
| 为每个顶层目录创建 `README.md` | AI | 至少覆盖活跃目录 |
| 生成 `.layer_tag` 模板 | AI | 26 个目录模板 |

### 9.2 阶段二：安全清理（第 3-4 周）

| 任务 | 负责人 | 产出 |
|:---|:---:|:---|
| 扫描并列出所有 Symlink | `scripts/migrate-symlinks.py` | Symlink 影响报告 |
| 移除非必要 Symlink | AI+UID9622 | 清理日志 |
| 将实验项目移入 `15_LABS/` | AI | 实验目录规整 |
| 将历史归档移入 `16_ARCHIVE/` | AI | 归档目录规整 |
| 标记 `_private/` 为不纳入版本控制 | AI | `.gitignore` 更新 |

### 9.3 阶段三：目录重命名与合并（第 5-8 周）

| 任务 | 负责人 | 产出 |
|:---|:---:|:---|
| 重命名中文/繁体目录 | AI+脚本 | 目录重命名日志 |
| 合并 `layers/` 重复层 | AI+P05 | `03_LAYERS/` 归一化 |
| 拆分 `bin/` 到 `08_BIN/` | AI+脚本 | 命令分类完成 |
| 迁移 `services/`、`engines/`、`portal/` | AI | 新命名生效 |
| 更新所有硬编码路径 | AI+脚本 | 路径一致性检查通过 |

### 9.4 阶段四：自动化治理上线（第 9-10 周）

| 任务 | 负责人 | 产出 |
|:---|:---:|:---|
| 部署 `scripts/structure-audit.py` | AI | 审计脚本 |
| 部署 `scripts/validate-naming.py` | AI | 命名校验脚本 |
| 配置 GitHub Actions | AI | `.github/workflows/structure-audit.yml` |
| 首次全量结构审计 | CI | 结构健康报告 |
| 修复首次审计发现的违规 | AI | 违规清零 |

### 9.5 阶段五：稳定与文档化（第 11-12 周）

| 任务 | 负责人 | 产出 |
|:---|:---:|:---|
| 更新 `AGENTS.md` 结构规则 | AI | AI 操作手册新增目录规范 |
| 创建 `CONTRIBUTING.md` 目录规范 | AI | 贡献指南 |
| 培训/通知所有协作者 | UID9622 | 社区公告 |
| 归档本审计报告 | P05 | `01_PROTOCOLS/audit/` |

### 9.6 过渡期兼容策略

- **6 个月过渡期**：旧路径通过 Symlink 保留，但标记为 `DEPRECATED`。
- **过渡期脚本**：`scripts/compat-path.py` 可将旧路径映射到新路径。
- **过渡期日志**：每次访问旧路径时记录到 `logs/compat-path.log`。
- **过渡期结束**：删除所有兼容 Symlink，旧路径彻底失效。

---

## 附录A · 当前目录完整清单

> 以下清单基于 2026-08-04 快照，用于迁移前后对比。

### A.1 顶层目录（部分示例）

```
01_protocols/
01_技能庫/
02_rules -> .codebuddy/rules/archive
02_執行記錄 -> archive/历史记录/02_執行記錄
03_compiler -> cnsh/compiler_legacy
03_后土OS/
03_知識圖譜/
04_決策日誌 -> archive/历史记录/04_決策日誌
05_系統報告 -> archive/历史记录/05_系統報告
06_技術文檔 -> docs/tech
25_TASK_ENGINE/
agents/
android-auto/
apps/
archive/
articles/
audit/
baobao-guardian/
bin/
data/
docs/
engines/
fonts/
knowledge-graph -> knowledge/graph
layers/
logs/
portal/
services/
...
```

完整清单见 `reports/structure-audit-20260804.json`（由 `scripts/structure-audit.py` 生成）。

### A.2 当前目录分类统计

| 类别 | 数量 | 说明 |
|:---|:---:|:---|
| 协议/治理 | 7 | `01_protocols/`、`01_技能庫/`、`_rules/` 等 |
| 架构/代码 | 15 | `layers/`、`services/`、`engines/`、`bin/` 等 |
| 数据/日志 | 8 | `data/`、`logs/`、`audit/` 等 |
| 文档/文章 | 5 | `docs/`、`articles/` 等 |
| 应用/门户 | 6 | `apps/`、`portal/`、`baobao-guardian/` 等 |
| 归档/实验 | 20+ | `archive/`、指向 `archive/experiments/` 的 Symlink |
| 配置/工具 | 10+ | `.vscode/`、`.devcontainer/` 等 |
| 私有/工作区 | 3 | `_private/`、`_work/`、`_archive/` |
| 其他 | 30+ | 未明确分类的目录 |

---

## 附录B · Symlink 清理清单

### B.1 建议删除的 Symlink（21 个）

| Symlink | 目标 | 删除理由 |
|:---|:---|:---|
| `02_rules/` | `.codebuddy/rules/archive` | 应直接访问原始路径 |
| `02_執行記錄/` | `archive/历史记录/02_執行記錄` | 整合到 `16_ARCHIVE/records/` |
| `03_compiler/` | `cnsh/compiler_legacy` | 直接访问 `cnsh/compiler_legacy` 或移入 `16_ARCHIVE/` |
| `04_決策日誌/` | `archive/历史记录/04_決策日誌` | 整合到 `16_ARCHIVE/records/` |
| `05_系統報告/` | `archive/历史记录/05_系統報告` | 整合到 `16_ARCHIVE/reports/` |
| `06_技術文檔/` | `docs/tech` | 直接访问 `12_DOCS/tech/` |
| `L1_内核层/` | `layers/L1_内核层` | 直接访问 `03_LAYERS/L1_kernel/` |
| `L9_子系统/` | `layers/L9_子系统` | 直接访问 `03_LAYERS/L9_subsystems/` |
| `rag_indexes/` | `archive/experiments/rag_indexes` | 实验项目不应在顶层 |
| `calendar-context-logger/` | `archive/experiments/...` | 同上 |
| `skill-standards.integrated/` | `archive/experiments/...` | 同上 |
| `forensic_kernel/` | `archive/experiments/forensic_kernel` | 同上 |
| `memory-universe/` | `archive/experiments/memory-universe` | 同上 |
| `ops-console/` | `archive/experiments/ops-console` | 同上 |
| `core/` | `archive/experiments/core` | 同上 |
| `training/` | `train` | 直接访问 `train/` 或重命名 |
| `backend/` | `services/backend_legacy` | 直接访问目标路径 |
| `backups/` | `archive/backups_cp` | 整合到 `16_ARCHIVE/backups/` |
| `benchmarks/` | `archive/experiments/benchmarks` | 移入 `13_TESTS/benchmark/` |
| `arxiv/` | `archive/experiments/arxiv` | 移入 `11_ARTICLES/arxiv/` |
| `knowledge-graph/` | `knowledge/graph` | 目标路径也需合并 |

### B.2 建议保留的 Symlink（5 个）

| Symlink | 目标 | 保留理由 |
|:---|:---|:---|
| `docs/` → `12_DOCS/` | 过渡期兼容 | 大量旧文档引用 `docs/` |
| `README.md` | 主入口 | 这是文件，非目录 |
| `LICENSE` | 根级许可 | 必须保留 |
| `AGENTS.md` | 根级 AI 手册 | 必须保留 |
| `install.sh` | 根级安装脚本 | 必须保留 |

---

## 附录C · 推荐文件头模板

### C.1 目录 README 模板

```markdown
# <目录名>

> DNA: #龍芯⚡️<干支>-<目录名>-v1.0-UID9622
> LAYER: engineering | core-idea | mixed
> STATUS: active | draft | deprecated
> OWNER: UID9622
> REVIEW_CYCLE: 6months
> LAST_REVIEWED: 2026-08-04

## 职责

简要说明本目录存放什么、不存放什么。

## 子目录

| 子目录 | 说明 |
|:---|:---|
| `sub-a/` | ... |
| `sub-b/` | ... |

## 命名规范

- 文件命名：`lh_<domain>_<action>.py`
- 禁止：...

## 相关文档

- `../docs/...`
- `../01_PROTOCOLS/...`
```

### C.2 `.layer_tag` 模板

```yaml
name: <目录名>
layer: engineering
owner: UID9622
status: active
review_cycle: 6months
last_reviewed: 2026-08-04
dna: "#龍芯⚡️<干支>-<目录名>-v1.0-UID9622"
description: "<一句话描述>"
notes: "<注意事项>"
```

---

## 附录D · 自动化脚本规格

### D.1 `scripts/structure-audit.py`

**输入**：仓库根路径。
**输出**：JSON/Markdown 结构健康报告。
**检查项**：
- 顶层目录数量
- 顶层 Symlink 数量
- 目录命名合规性
- 孤儿文件
- 重复文件名
- README 覆盖率
- `.layer_tag` 覆盖率
- `bin/` 文件分类情况
- 归档目录写入检查

### D.2 `scripts/validate-naming.py`

**输入**：仓库根路径。
**输出**：违规列表。
**规则**：
- 顶层目录必须匹配 `^\d{2}_[a-z0-9-]+/$`
- 子目录必须匹配 `^[a-z0-9_-]+/$`
- 禁止中文、日文、繁体中文目录名
- 禁止无意义 Symlink

### D.3 `scripts/migrate-symlinks.py`

**输入**：仓库根路径。
**输出**：Symlink 影响报告 + 迁移建议。
**功能**：
- 列出所有 Symlink 及其目标
- 分析每个 Symlink 被引用的次数
- 生成删除/保留建议
- 生成兼容路径映射表

### D.4 `scripts/restructure-plan.py`

**输入**：仓库根路径 + 目标架构配置。
**输出**：迁移计划 JSON。
**模式**：
- `--dry-run`：预览迁移计划
- `--apply`：执行迁移
- `--compat`：生成兼容 Symlink

---

## 附录E · 修订历史

| 版本 | 日期 | 变更 | 修订人 |
|:---|:---|:---|:---|
| v1.0 | 2026-08-04 | 初始审计报告·目标架构蓝图·迁移路线图·自动化治理规则 | UID9622+AI |
| v2.0 | 2026-08-04 | 执行第一阶段重组：清理24个archive/experiments实验Symlink；完成10个核心目录编号化（bin→08_BIN、tools→09_TOOLS、portal→10_PORTAL、data→11_DATA、docs→12_DOCS、tests→13_TESTS、engines→05_ENGINES、services→04_SERVICES、layers→03_LAYERS、audit→07_AUDIT），旧路径全部保留Symlink兼容；新增scripts/compat-path.py兼容映射脚本；更新目录地图v2.0 | UID9622+AI |

---

> 🐉 **结构是主权的外化。目录名即法度，路径即秩序。**
>
> 本协议为龍魂系统核心思想层文件，适用 CC BY-NC-SA 4.0。
> 工程实现层自动化脚本适用 MulanPSL v2。
