# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 架构归一方案 v1.0

> DNA: `#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-ARCH-NORMALIZATION-v1.0-9A3F2D1E`
> 决策人: UID9622
> 执行人: CodeBuddy
> 原则: 不删除文件，只移动/归档/标注副本关系
> 审计: 🟢 三色通过

---

## 一、现状诊断

| 问题 | 严重度 | 数据 |
|------|--------|------|
| CNSH内核碎片化 | 🔴严重 | 7个目录含CNSH相关代码（cnsh-core/cnsh/cnsh-terminal/cnsh-runtime-v1/cnsh-core.backup/cnsh_terminal_v5.0/cnsh-editor/cnsh_editor） |
| 引擎多份副本 | 🔴严重 | 30个引擎文件，11组有副本冗余（最多5份同文件） |
| Web操作台重复 | 🔴严重 | web/与portal/几乎完全对称（相同HTML文件） |
| 技能定义分叉 | 🟡中等 | 02_SKILLS/(13文件) vs 01_技能库/(64文件) vs skills/ (13+子目录) |
| 技能备份冗余 | 🟡中等 | skills.backup/ 与 skills/ 重复 |
| 监控重复 | 🟡中等 | monitoring/ vs monitoring.backup/ 重复 |
| 根目录散落 | 🟡中等 | 60+ .md/.py/.sh/.json 文件散落根目录 |
| brain数据膨胀 | 🟡中等 | brain/ 含108,744文件，部分来自外部导入 |
| 归档未整理 | 🟢低 | _archive/ (1,515文件) + _quarantine/ (20文件) |

---

## 二、归一架构（目标状态）

```
longhun-system/
│
├── 📜 L0_宪法层/                      ← 不可变·系统根
│   ├── CONSTITUTION.md                (系统宪法)
│   ├── AGENTS.md                      (AI操作手册)
│   ├── CNSH-PROTOCOL.md               (CNSH语言规范)
│   ├── CNSH-SEMANTIC.md               (CNSH语义规范)
│   ├── ATTRIBUTION.md                 (署名规范)
│   ├── STANDARD.md                    (编码标准)
│   └── README.md                      (项目入口)
│
├── 🧠 L1_内核层/                      ← CNSH编译器+核心引擎
│   └── kernel/
│       ├── compiler/                  ← (cnsh-core/cnsh-v2.1/) CNSH编译器
│       ├── engines/                   ← 所有权威引擎唯一存放处
│       │   ├── audit_engine.py        ← 审计引擎 (⭐权威)
│       │   ├── cnsh_editor_engine.py  ← 编辑器引擎 (⭐权威)
│       │   ├── cnsh_translator_engine.py ← 转译器引擎 (⭐权威)
│       │   ├── yijing_engine.py       ← 易经引擎 (⭐权威)
│       │   ├── governance_engine.py   ← 分层治理引擎
│       │   ├── rule_engine.py         ← 规则引擎
│       │   ├── dna_engine.py          ← DNA授权引擎
│       │   ├── redline_engine.py      ← 红线引擎
│       │   └── symlinks/             ← 其他位置的符号链接
│       ├── grammar/                   ← CNSH语法
│       ├── governance/                ← 分层治理
│       ├── rules/                     ← 规则引擎
│       ├── constitution/              ← 权重引擎
│       └── api/                       ← 统一API
│
├── 🛡️ L2_技能层/                      ← 技能权威定义+引擎
│   └── skills/
│       ├── definitions/               ← (02_SKILLS/) 13个权威技能定义
│       ├── engines/                   ← 技能引擎
│       │   ├── skill_extension.py
│       │   ├── bagua_router.py
│       │   ├── wuxing_guard.py
│       │   ├── sovereign_privacy.py
│       │   ├── semantic_parser.py
│       │   ├── audit_plugin_base.py
│       │   ├── error_translator.py
│       │   └── plist_validator.py
│       ├── standards/                 ← (skill-standards.integrated/) 技能标准文档
│       └── runtime/                   ← 运行时技能（原skills/子目录）
│
├── 🤖 L3_智能体层/                    ← Agent编排+执行
│   └── agents/
│       ├── orchestrator.py
│       ├── manifest.json
│       ├── daemon/
│       ├── adapters/
│       └── tasks/
│
├── ⚡ L4_执行层/                      ← CLI+运行时+调度
│   └── executors/
│       ├── bin/                       ← 命令注册表+CLI工具
│       ├── runtime/                   ← 执行运行时
│       ├── scheduler/                 ← 调度器
│       └── launcher/                  ← 启动脚本
│
├── 🌐 L5_服务层/                      ← Web/API/Portal
│   └── services/
│       ├── api/                       ← (control-panel/) API服务 :9622
│       ├── dashboard/                 ← (web/) 操作台
│       ├── portal/                    ← (portal/) 对外官网
│       └── neural/                    ← 3D神经网络可视化
│
├── 🔌 L6_集成层/                      ← 外部集成+桥接
│   └── integrations/
│       ├── mcp/                       ← MCP Server
│       ├── deepseek/                  ← DeepSeek
│       ├── notion/                    ← Notion同步
│       ├── wechat/                    ← 微信公众号
│       ├── bridges/                   ← API桥接
│       └── internal/                  ← 内部集成模块
│
├── 💾 L7_数据层/                      ← 数据存储+知识库
│   └── data/
│       ├── knowledge-graph/           ← (03_KNOWLEDGE_GRAPH/)
│       ├── brain/                     ← 第二大脑
│       ├── memory/                    ← 记忆宇宙
│       ├── capabilities/              ← 能力注册表
│       ├── protocols/                 ← (01_protocols/)
│       ├── rules/                     ← (02_rules/)
│       └── compiler/                  ← (03_compiler/)
│
├── 📊 L8_治理层/                      ← 审计+日志+报告
│   └── governance/
│       ├── audit/                     ← 审计子系统
│       ├── logs/                      ← 执行记录+决策日志
│       ├── reports/                   ← 系统报告
│       └── tech-docs/                 ← (06_技術文檔/)
│
├── 🎨 L9_子系统/                      ← 独立功能子系统
│   └── subsystems/
│       ├── baobao-guardian/           ← 宝宝守护者
│       ├── xpay/                      ← 支付系统
│       ├── persona/                   ← 人格系统
│       ├── font-engine/               ← (longhun-font/)
│       ├── voice/                     ← (voice-dna/ + voice-twin/)
│       ├── chrome-extension/          ← 浏览器扩展
│       ├── law-engine/                ← (法律引擎/)
│       ├── luoshu-engine/             ← (龍魂洛书369引擎/)
│       ├── forensics/                 ← (龍魂取证内核/)
│       ├── rules-engine/              ← (rules-engine-v2.5/)
│       ├── memory-universe/           ← 记忆宇宙
│       ├── wuxing-visual/             ← 五行可视化
│       ├── android-auto/              ← 安卓自动化
│       ├── csdn-sync/                 ← CSDN同步
│       └── cnsh-editor/               ← CNSH编辑器
│
├── 📦 _archive/                       ← 归档层（所有废弃/备份/历史）
│   ├── legacy/
│   │   ├── cnsh-core.backup/
│   │   ├── cnsh-runtime-v1/
│   │   └── cnsh-terminal.backup/
│   ├── deprecated/
│   │   ├── 01_技能库/                  ← (简中分叉，已合并到skills/definitions/)
│   │   ├── skills.backup/
│   │   ├── monitoring.backup/
│   │   └── second-brain/               ← (与brain重复)
│   ├── quarantine/                    ← (_quarantine/)
│   └── reports/                       ← (_archived_reports/)
│
├── 📄 根目录（仅保留入口文件）
│   ├── .gitignore
│   ├── pyproject.toml
│   ├── requirements-base.txt
│   └── lh → executors/bin/lh          ← (符号链接)
│
└── 🔧 config/                         ← 系统配置
```

---

## 三、迁移映射表

### 3.1 CNSH内核归一 (norm2)

| 源路径 | 目标 | 操作 |
|--------|------|------|
| `cnsh-core/` | `L1_内核层/kernel/` | 🏠 保留为主权威源 |
| `cnsh/` | `_archive/legacy/cnsh-legacy/` | 📦 归档（旧版内核） |
| `cnsh-terminal/` | `_archive/legacy/cnsh-terminal-legacy/` | 📦 归档（终端旧版） |
| `cnsh-runtime-v1/` | `_archive/legacy/cnsh-runtime-v1/` | 📦 归档（v1运行时） |
| `cnsh-core.backup/` | `_archive/legacy/cnsh-core.backup/` | 📦 归档（已备份） |
| `cnsh_terminal_v5.0/` | `_archive/legacy/cnsh_terminal_v5.0/` | 📦 归档（与cnsh-terminal重复） |
| `cnsh_editor/` | `_archive/legacy/cnsh_editor/` | 📦 归档（与cnsh-editor重复） |

### 3.2 引擎收敛 (norm3)

| 引擎名 | 权威源 | 副本 | 操作 |
|--------|--------|------|------|
| audit_engine | `L1_内核层/kernel/engines/audit_engine.py` | 4份副本 | 📋副本标注 + 待废弃 |
| cnsh_editor_engine | `L1_内核层/kernel/engines/cnsh_editor_engine.py` | 4份副本 | 📋副本标注 |
| cnsh_translator_engine | `L1_内核层/kernel/engines/cnsh_translator_engine.py` | 4份副本 | 📋副本标注 |
| skill_auto_completion | `L2_技能层/skills/engines/skill_auto_completion.py` | 3份副本 | 📋副本标注 |
| yijing_engine | `L1_内核层/kernel/engines/yijing_engine.py` | 1份副本 | 📋副本标注 |

### 3.3 Web归一 (norm4)

| 源 | 目标 | 操作 |
|----|------|------|
| `web/` | `L5_服务层/services/dashboard/` | 🏠 保留为开发版操作台 |
| `portal/` | `L5_服务层/services/portal/` | 🏠 保留为生产版官网 |
| `control-panel/` | `L5_服务层/services/api/` | 🏠 保留为API服务 |
| `desktop/` | `L5_服务层/services/desktop/` | 🏠 保留 |

### 3.4 技能归一 (norm5)

| 源 | 目标 | 操作 |
|----|------|------|
| `02_SKILLS/` (13文件) | `L2_技能层/skills/definitions/` | 🏠 保留为权威定义 |
| `01_技能库/` (64文件) | `_archive/deprecated/01_技能库/` | 📦 归档（简中分叉） |
| `skills/` (运行时) | `L2_技能层/skills/runtime/` | 🏠 保留为运行时 |
| `skills.backup/` | `_archive/deprecated/skills.backup/` | 📦 归档 |
| `skill-standards.integrated/` | `L2_技能层/skills/standards/` | 🏠 保留 |

### 3.5 根目录清理 (norm6)

| 分类 | 文件数 | 目标 |
|------|--------|------|
| 宪法文件 | ~8 | 保留在根目录 |
| 启动/入口文件 | ~10 | → `executors/launcher/` |
| 系统报告 | ~15 | → `governance/reports/` |
| 独立脚本 (.py) | ~12 | → 对应子系统 |
| 治理文档 | ~10 | → `governance/` |
| 临时/测试文件 | ~8 | → `_archive/` |

### 3.6 归档收敛 (norm7)

| 源 | 操作 |
|----|------|
| `_archive/` (1,515文件) | 保持，添加README说明 |
| `_quarantine/` (20文件) | 移入 `_archive/quarantine/` |
| `_backup/` (105文件) | 移入 `_archive/backups/` |
| `backups/` (21文件) | 移入 `_archive/backups/system/` |
| `_archived_reports/` (94文件) | 移入 `_archive/reports/` |
| `_audit/` (32文件) | 移入 `_archive/audit/` |
| `_private/` (28文件) | 不动（私有数据） |

### 3.7 其他归一 (norm8)

| 源 | 目标 | 操作 |
|----|------|------|
| `monitoring.backup/` | `_archive/deprecated/monitoring.backup/` | 📦 归档 |
| `second_brain/` | → 与 `brain/` 比对后归档 | 📦 归档 |
| `second-brain/` | → 同上 | 📦 归档 |
| `software_dna/` + `software-dna/` | 合并保留一个 | 🔀 合并 |
| `cnsh-terminal/` + `cnsh_terminal_v5.0/` | 保留v5.0，其余归档 | 📦 归档旧版 |
| `CNSH_监管数据/` | `data/regulatory/` | 📁 归类 |
| `CNSH_修复输出/` | `_archive/CNSH_修复输出/` | 📦 归档 |
| `CNSH-整理版/` | `_archive/CNSH-整理版/` | 📦 归档 |
| 根目录60+散落文件 | 按分类归入对应目录 | 📁 归类 |

---

## 四、执行顺序（防踩踏）

```
norm1 ✅ 制定归一架构文档        ← 当前
norm2 ⏳ CNSH内核归一（7→1）
norm3 ⏳ 重复引擎收敛（标注副本）
norm4 ⏳ Web/Portal整理
norm5 ⏳ 技能目录归一
norm6 ⏳ 根目录清理
norm7 ⏳ 归档收敛
norm8 ⏳ .gitignore + MASTER_REGISTRY 更新 + 全链路验证
```

## 五、不变量保障

- ❌ 不执行 `rm -rf`（龍魂铁律）
- ✅ 所有操作使用 `mv` (移动) + 符号链接
- ✅ 每个移动操作绑定DNA
- ✅ 完成后运行 `lh6 审计` 验证

---

DNA: `#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-ARCH-NORMALIZATION-v1.0-9A3F2D1E`
