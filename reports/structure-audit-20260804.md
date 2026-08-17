# 龍魂系统 · 结构健康审计报告

> DNA: #龍芯⚡️20260804082507837-STRUCTURE-AUDIT-12D00E52
> 时间: 2026-08-04T08:25:07.841119+00:00
> 根目录: `/Users/zuimeidedeyihan/longhun-system`
> 总体状态: 🔴 ERROR

## 摘要

| 指标 | 数值 |
|:---|---:|
| top_level_dirs | 101 |
| top_level_symlinks | 68 |
| top_level_files | 90 |
| top_level_others | 0 |
| bin_files | 1991 |
| bin_subdirs | ['identity', 'docs_factory', 'CNSH_中枢数据', '__pycache__', 'personas', 'shortcuts', 'lh_network', 'guardian_field', 'CNSH_加工输出', 'payment_providers', '_archive', 'cnsh_brain_regions'] |

## 检查项

| 检查项 | 状态 | 值 | 阈值 | 说明 |
|:---|:---:|:---:|:---:|:---|
| top_level_dir_count | 🔴 fail | 101 | 30 | 顶层目录数 101，阈值 30 |
| top_level_symlink_count | 🔴 fail | 68 | 5 | 顶层 Symlink 数 68，阈值 5 |
| top_dir_naming_compliance | 🔴 fail | {"violations": 90, "hidden_dirs": 10} | 0 | 顶层目录命名违规 90 个（隐藏工具目录 10 个单独记录） |
| root_file_whitelist | 🟡 warn | 46 | None | 根目录非白名单文件 46 个 |
| symlink_inventory | 🟢 ok | 68 | None | 已盘点 68 个 Symlink |
| bin_classification | 🟢 ok | {"files": 1991, "subdirs": ["identity", "docs_factory", "CNSH_中枢数据", "__pycache__", "personas", "shortcuts", "lh_network", "guardian_field", "CNSH_加工输出", "payment_providers", "_archive", "cnsh_brain_regions"]} | None | bin/ 已分类 |
| orphan_file_scan | 🟡 warn | 6 | None | 疑似孤儿文件（>90天未修改）6 个 |
| readme_coverage | 🟡 warn | 68 | None | 缺少 README.md 的顶层目录 68 个 |
| layer_tag_coverage | 🟡 warn | 101 | None | 缺少 .layer_tag 的顶层目录 101 个 |
| duplicate_filenames | 🟡 warn | 13299 | None | 值得关注的重复文件名（≥3处且非通用名）13299 个 |

## 违规详情

### top_dir_naming

```json
[
  {
    "path": "01_技能庫",
    "reason": "包含中文/繁体/日文"
  },
  {
    "path": "03_后土OS",
    "reason": "包含中文/繁体/日文"
  },
  {
    "path": "03_知識圖譜",
    "reason": "包含中文/繁体/日文"
  },
  {
    "path": "25_TASK_ENGINE",
    "reason": "格式不符"
  },
  {
    "path": "CNSH_修复输出",
    "reason": "包含中文/繁体/日文"
  },
  {
    "path": "CNSH_加工输出",
    "reason": "包含中文/繁体/日文"
  },
  {
    "path": "CNSH_护盾数据",
    "reason": "包含中文/繁体/日文"
  },
  {
    "path": "CNSH_监管数据",
    "reason": "包含中文/繁体/日文"
  },
  {
    "path": "_archive",
    "reason": "格式不符"
  },
  {
    "path": "_private",
    "reason": "格式不符"
  },
  {
    "path": "_work",
    "reason": "格式不符"
  },
  {
    "path": "agents",
    "reason": "格式不符"
  },
  {
    "path": "android-auto",
    "reason": "格式不符"
  },
  {
    "path": "apps",
    "reason": "格式不符"
  },
  {
    "path": "archive",
    "reason": "格式不符"
  },
  {
    "path": "articles",
    "reason": "格式不符"
  },
  {
    "path": "audit",
    "reason": "格式不符"
  },
  {
    "path": "baobao-guardian",
    "reason": "格式不符"
  },
  {
    "path": "bin",
    "reason": "格式不符"
  },
  {
    "path": "brand",
    "reason": "格式不符"
  },
  {
    "path": "capabilities",
    "reason": "格式不符"
  },
  {
    "path": "cnsh",
    "reason": "格式不符"
  },
  {
    "path": "config",
    "reason": "格式不符"
  },
  {
    "path": "control-panel",
    "reason": "格式不符"
  },
  {
    "path": "dashboard",
    "reason": "格式不符"
  },
  {
    "path": "data",
    "reason": "格式不符"
  },
  {
    "path": "deploy",
    "reason": "格式不符"
  },
  {
    "path": "dev-env",
    "reason": "格式不符"
  },
  {
    "path": "digital_humans",
    "reason": "格式不符"
  },
  {
    "path": "dist",
    "reason": "格式不符"
  },
  {
    "path": "docker",
    "reason": "格式不符"
  },
  {
    "path": "docs",
    "reason": "格式不符"
  },
  {
    "path": "editors",
    "reason": "格式不符"
  },
  {
    "path": "engines",
    "reason": "格式不符"
  },
  {
    "path": "executors",
    "reason": "格式不符"
  },
  {
    "path": "experiments",
    "reason": "格式不符"
  },
  {
    "path": "extensions",
    "reason": "格式不符"
  },
  {
    "path": "fused_model",
    "reason": "格式不符"
  },
  {
    "path": "governance",
    "reason": "格式不符"
  },
  {
    "path": "harmony",
    "reason": "格式不符"
  },
  {
    "path": "harmonyos-universe",
    "reason": "格式不符"
  },
  {
    "path": "imports",
    "reason": "格式不符"
  },
  {
    "path": "integrated_modules",
    "reason": "格式不符"
  },
  {
    "path": "integrations",
    "reason": "格式不符"
  },
  {
    "path": "kimi",
    "reason": "格式不符"
  },
  {
    "path": "knowledge",
    "reason": "格式不符"
  },
  {
    "path": "launchd",
    "reason": "格式不符"
  },
  {
    "path": "layers",
    "reason": "格式不符"
  },
  {
    "path": "library",
    "reason": "格式不符"
  },
  {
    "path": "logs",
    "reason": "格式不符"
  },
  {
    "path": "longhun-font",
    "reason": "格式不符"
  },
  {
    "path": "luoshu_369_engine",
    "reason": "格式不符"
  },
  {
    "path": "mobile",
    "reason": "格式不符"
  },
  {
    "path": "models",
    "reason": "格式不符"
  },
  {
    "path": "multicurrency",
    "reason": "格式不符"
  },
  {
    "path": "mvp_config",
    "reason": "格式不符"
  },
  {
    "path": "mvp_data",
    "reason": "格式不符"
  },
  {
    "path": "open_audit_output",
    "reason": "格式不符"
  },
  {
    "path": "output",
    "reason": "格式不符"
  },
  {
    "path": "pages",
    "reason": "格式不符"
  },
  {
    "path": "papers",
    "reason": "格式不符"
  },
  {
    "path": "personas",
    "reason": "格式不符"
  },
  {
    "path": "portal",
    "reason": "格式不符"
  },
  {
    "path": "price_audit_tool",
    "reason": "格式不符"
  },
  {
    "path": "public-content",
    "reason": "格式不符"
  },
  {
    "path": "registry",
    "reason": "格式不符"
  },
  {
    "path": "reports",
    "reason": "格式不符"
  },
  {
    "path": "research",
    "reason": "格式不符"
  },
  {
    "path": "scripts",
    "reason": "格式不符"
  },
  {
    "path": "services",
    "reason": "格式不符"
  },
  {
    "path": "skills",
    "reason": "格式不符"
  },
  {
    "path": "software_dna",
    "reason": "格式不符"
  },
  {
    "path": "sovereignty",
    "reason": "格式不符"
  },
  {
    "path": "state",
    "reason": "格式不符"
  },
  {
    "path": "systems",
    "reason": "格式不符"
  },
  {
    "path": "templates",
    "reason": "格式不符"
  },
  {
    "path": "test_logs",
    "reason": "格式不符"
  },
  {
    "path": "test_results",
    "reason": "格式不符"
  },
  {
    "path": "tests",
    "reason": "格式不符"
  },
  {
    "path": "tombstone_vault",
    "reason": "格式不符"
  },
  {
    "path": "tools",
    "reason": "格式不符"
  },
  {
    "path": "train",
    "reason": "格式不符"
  },
  {
    "path": "tts",
    "reason": "格式不符"
  },
  {
    "path": "videos",
    "reason": "格式不符"
  },
  {
    "path": "voices",
    "reason": "格式不符"
  },
  {
    "path": "web",
    "reason": "格式不符"
  },
  {
    "path": "web_apps",
    "reason": "格式不符"
  },
  {
    "path": "widgets",
    "reason": "格式不符"
  },
  {
    "path": "xpay",
    "reason": "格式不符"
  },
  {
    "path": "zeng-extraction",
    "reason": "格式不符"
  }
]
```

## 附加信息

### hidden_tool_dirs

```json
{
  "type": "hidden_tool_dirs",
  "dirs": [
    ".cnsh",
    ".codebuddy",
    ".commander",
    ".daoyin_workspace",
    ".devcontainer",
    ".githooks",
    ".github",
    ".longhun",
    ".obsidian",
    ".vscode"
  ]
}
```

### root_unknown_files

```json
{
  "type": "root_unknown_files",
  "files": [
    "COMMIT_MESSAGE_STANDARD.md",
    "COMMIT_MESSAGE_STANDARD.md.asc",
    "Dockerfile.cnsh",
    "Dockerfile.cnsh.asc",
    "INSTALL.md",
    "INSTALL.md.asc",
    "MANIFESTO.md",
    "MANIFESTO.md.asc",
    "P0_ETERNAL_LOCK.md",
    "P0_ETERNAL_LOCK.md.asc",
    "QUICKSTART.md",
    "QUICKSTART.md.asc",
    "RELEASE_ANNOUNCEMENT-v5.0.0-opensource.md",
    "RELEASE_ANNOUNCEMENT-v5.0.0-opensource.md.asc",
    "STANDARD.md",
    "STANDARD.md.asc",
    "STATE.md",
    "STATE.md.asc",
    "cnsh_constants.py",
    "cnsh_constants.py.asc",
    "cnsh_create.sh",
    "cnsh_create.sh.asc",
    "cnsh_env.sh",
    "cnsh_env.sh.asc",
    "cnsh_print.py",
    "cnsh_print.py.asc",
    "cnsh_prompt.zsh",
    "cnsh_prompt.zsh.asc",
    "code_with_dna_1785506239.py",
    "code_with_dna_1785506239.py.asc",
    "code_with_dna_1785820178.py",
    "code_with_dna_1785820178.py.asc",
    "demo_vulnerable.py",
    "demo_vulnerable.py.asc",
    "dna_master_key.json",
    "lh_public_key.asc",
    "pytest.ini",
    "requirements-base.txt",
    "requirements.lock.txt",
    "requirements.txt",
    "sync_log.jsonl",
    "system_registry.json",
    "system_registry.json.asc",
    "功能清单.md",
    "功能清单.md.asc",
    "操作草日志.log"
  ]
}
```

### symlink_details

```json
[
  {
    "link": "02_rules",
    "target": ".codebuddy/rules/archive"
  },
  {
    "link": "02_執行記錄",
    "target": "archive/历史记录/02_執行記錄"
  },
  {
    "link": "03_compiler",
    "target": "cnsh/compiler_legacy"
  },
  {
    "link": "04_決策日誌",
    "target": "archive/历史记录/04_決策日誌"
  },
  {
    "link": "05_系統報告",
    "target": "archive/历史记录/05_系統報告"
  },
  {
    "link": "06_技術文檔",
    "target": "docs/tech"
  },
  {
    "link": "CNSH_颜色历史",
    "target": "archive/CNSH_颜色历史"
  },
  {
    "link": "L0_物理层",
    "target": "layers/L0_物理层"
  },
  {
    "link": "L1_内核层",
    "target": "layers/L1_内核层"
  },
  {
    "link": "L1_身份层",
    "target": "layers/L1_身份层"
  },
  {
    "link": "L2_主权层",
    "target": "layers/L2_主权层"
  },
  {
    "link": "L2_技能层",
    "target": "layers/L2_技能层"
  },
  {
    "link": "L3_执行层",
    "target": "layers/L3_执行层"
  },
  {
    "link": "L3_数据层",
    "target": "layers/L3_数据层"
  },
  {
    "link": "L3_语义层",
    "target": "layers/L3_语义层"
  },
  {
    "link": "L4_数据层",
    "target": "layers/L4_数据层"
  },
  {
    "link": "L5_服务层",
    "target": "layers/L5_服务层"
  },
  {
    "link": "L6_同步层",
    "target": "layers/L6_同步层"
  },
  {
    "link": "L6_记忆层",
    "target": "layers/L6_记忆层"
  },
  {
    "link": "L6_集成层",
    "target": "layers/L6_集成层"
  },
  {
    "link": "L7_数据层",
    "target": "layers/L7_数据层"
  },
  {
    "link": "L7_表达层",
    "target": "layers/L7_表达层"
  },
  {
    "link": "L8_分发层",
    "target": "layers/L8_分发层"
  },
  {
    "link": "L8_治理层",
    "target": "layers/L8_治理层"
  },
  {
    "link": "L9_子系统",
    "target": "layers/L9_子系统"
  },
  {
    "link": "arxiv",
    "target": "archive/experiments/arxiv"
  },
  {
    "link": "backend",
    "target": "services/backend_legacy"
  },
  {
    "link": "backups",
    "target": "archive/backups_cp"
  },
  {
    "link": "benchmarks",
    "target": "archive/experiments/benchmarks"
  },
  {
    "link": "brain",
    "target": "archive/experiments/brain"
  },
  {
    "link": "bridges",
    "target": "archive/experiments/bridges"
  },
  {
    "link": "calendar-context-logger",
    "target": "archive/experiments/calendar-context-logger"
  },
  {
    "link": "chrome_extension",
    "target": "archive/experiments/chrome_extension"
  },
  {
    "link": "cnsh.integrated",
    "target": "cnsh"
  },
  {
    "link": "compute_kernels",
    "target": "archive/experiments/compute_kernels"
  },
  {
    "link": "core",
    "target": "archive/experiments/core"
  },
  {
    "link": "core-services",
    "target": "archive/experiments/core-services"
  },
  {
    "link": "crypto-stack",
    "target": "archive/experiments/crypto-stack"
  },
  {
    "link": "data-hub",
    "target": "archive/experiments/data-hub"
  },
  {
    "link": "desktop",
    "target": "archive/experiments/desktop"
  },
  {
    "link": "editor",
    "target": "editors"
  },
  {
    "link": "forensic_kernel",
    "target": "archive/experiments/forensic_kernel"
  },
  {
    "link": "kg-api",
    "target": "archive/experiments/kg-api"
  },
  {
    "link": "knowledge-graph",
    "target": "knowledge/graph"
  },
  {
    "link": "longhun-v1.0-audit-package",
    "target": "archive/longhun-v1.0-audit-package"
  },
  {
    "link": "memory-universe",
    "target": "archive/experiments/memory-universe"
  },
  {
    "link": "mobile-monitoring.integrated",
    "target": "mobile/monitoring"
  },
  {
    "link": "monitoring",
    "target": "archive/experiments/monitoring"
  },
  {
    "link": "ops-console",
    "target": "archive/experiments/ops-console"
  },
  {
    "link": "orders",
    "target": "archive/experiments/orders"
  },
  {
    "link": "project-memory",
    "target": "archive/experiments/project-memory"
  },
  {
    "link": "rag_indexes",
    "target": "archive/experiments/rag_indexes"
  },
  {
    "link": "rules-engine-v2.5",
    "target": "archive/experiments/rules-engine-v2.5"
  },
  {
    "link": "skill-standards.integrated",
    "target": "archive/experiments/skill-standards.integrated"
  },
  {
    "link": "sovereign-registry",
    "target": "sovereignty/registry"
  },
  {
    "link": "training",
    "target": "train"
  },
  {
    "link": "var",
    "target": "archive/experiments/var"
  },
  {
    "link": "wuxing-visual",
    "target": "archive/experiments/wuxing-visual"
  },
  {
    "link": "人民维权助手",
    "target": "engines/people_assist"
  },
  {
    "link": "协议文档",
    "target": "01_protocols/archive/legacy"
  },
  {
    "link": "字体",
    "target": "/Users/zuimeidedeyihan/longhun-system/longhun-font"
  },
  {
    "link": "引擎",
    "target": "engines/legacy_runtime"
  },
  {
    "link": "快捷命令",
    "target": "bin/shortcuts"
  },
  {
    "link": "日志",
    "target": "logs"
  },
  {
    "link": "核心引擎",
    "target": "engines/core"
  },
  {
    "link": "法律引擎",
    "target": "engines/legal"
  },
  {
    "link": "统一入口",
    "target": "portal/unified_entry"
  },
  {
    "link": "龍魂日记本-iOS",
    "target": "mobile/longhun-diary-ios"
  }
]
```

### orphan_candidates

```json
[
  {
    "file": "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/bin/python3",
    "age_days": 128.5
  },
  {
    "file": "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/bin/python",
    "age_days": 128.5
  },
  {
    "file": "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/bin/python3.12",
    "age_days": 128.5
  },
  {
    "file": "engines/gpt_sovits/.venv_gpt_sovits/bin/python3",
    "age_days": 128.5
  },
  {
    "file": "engines/gpt_sovits/.venv_gpt_sovits/bin/python",
    "age_days": 128.5
  },
  {
    "file": "engines/gpt_sovits/.venv_gpt_sovits/bin/python3.12",
    "age_days": 128.5
  }
]
```

### dirs_without_readme

```json
{
  "type": "dirs_without_readme",
  "dirs": [
    ".cnsh",
    ".codebuddy",
    ".commander",
    ".daoyin_workspace",
    ".devcontainer",
    ".githooks",
    ".github",
    ".obsidian",
    ".vscode",
    "01_protocols",
    "01_技能庫",
    "25_TASK_ENGINE",
    "CNSH_修复输出",
    "CNSH_加工输出",
    "CNSH_护盾数据",
    "CNSH_监管数据",
    "_archive",
    "_private",
    "_work",
    "apps",
    "archive",
    "articles",
    "audit",
    "brand",
    "config",
    "dashboard",
    "data",
    "deploy",
    "dev-env",
    "digital_humans",
    "dist",
    "engines",
    "experiments",
    "governance",
    "harmony",
    "harmonyos-universe",
    "imports",
    "knowledge",
    "launchd",
    "layers",
    "library",
    "logs",
    "luoshu_369_engine",
    "mobile",
    "models",
    "mvp_data",
    "open_audit_output",
    "output",
    "pages",
    "papers",
    "personas",
    "portal",
    "public-content",
    "registry",
    "reports",
    "services",
    "software_dna",
    "sovereignty",
    "state",
    "systems",
    "test_logs",
    "test_results",
    "tombstone_vault",
    "tts",
    "videos",
    "web_apps",
    "widgets",
    "zeng-extraction"
  ]
}
```

### dirs_without_layer_tag

```json
{
  "type": "dirs_without_layer_tag",
  "dirs": [
    ".cnsh",
    ".codebuddy",
    ".commander",
    ".daoyin_workspace",
    ".devcontainer",
    ".githooks",
    ".github",
    ".longhun",
    ".obsidian",
    ".vscode",
    "01_protocols",
    "01_技能庫",
    "03_后土OS",
    "03_知識圖譜",
    "25_TASK_ENGINE",
    "CNSH_修复输出",
    "CNSH_加工输出",
    "CNSH_护盾数据",
    "CNSH_监管数据",
    "_archive",
    "_private",
    "_work",
    "agents",
    "android-auto",
    "apps",
    "archive",
    "articles",
    "audit",
    "baobao-guardian",
    "bin",
    "brand",
    "capabilities",
    "cnsh",
    "config",
    "control-panel",
    "dashboard",
    "data",
    "deploy",
    "dev-env",
    "digital_humans",
    "dist",
    "docker",
    "docs",
    "editors",
    "engines",
    "executors",
    "experiments",
    "extensions",
    "fused_model",
    "governance",
    "harmony",
    "harmonyos-universe",
    "imports",
    "integrated_modules",
    "integrations",
    "kimi",
    "knowledge",
    "launchd",
    "layers",
    "library",
    "logs",
    "longhun-font",
    "luoshu_369_engine",
    "mobile",
    "models",
    "multicurrency",
    "mvp_config",
    "mvp_data",
    "open_audit_output",
    "output",
    "pages",
    "papers",
    "personas",
    "portal",
    "price_audit_tool",
    "public-content",
    "registry",
    "reports",
    "research",
    "scripts",
    "services",
    "skills",
    "software_dna",
    "sovereignty",
    "state",
    "systems",
    "templates",
    "test_logs",
    "test_results",
    "tests",
    "tombstone_vault",
    "tools",
    "train",
    "tts",
    "videos",
    "voices",
    "web",
    "web_apps",
    "widgets",
    "xpay",
    "zeng-extraction"
  ]
}
```

### duplicate_filenames

```json
{
  ".claude.json": [
    ".codebuddy/.claude.json",
    "_work/repos/ai-truth-protocol/longhun-system/CNSH_备份_20260211/.claude.json",
    "_work/repos/longhun-system/_archive/cnsh-history/CNSH_备份_20260211/.claude.json",
    "data/training/home_absorb/loose_files/.claude.json",
    "data/training/home_absorb/workspace/Desktop/龍魂系统-知识库/_archive/cnsh-history/CNSH_备份_20260211/.claude.json",
    "data/training/home_absorb/knowledge/Obsidian/龍魂系統/_archive/cnsh-history/CNSH_备份_20260211/.claude.json",
    "data/sources/downloads_20260717_absorb/UID9622_脑子/CNSH 军人的编辑器/.claude.json"
  ],
  "RULE-REGISTRY.local.jsonl": [
    ".codebuddy/rules/archive/RULE-REGISTRY.local.jsonl",
    "_work/repos/longhun-system/02_rules/RULE-REGISTRY.local.jsonl",
    "data/training/home_absorb/workspace/Desktop/龍魂系统·统一知识矩阵/04_三色审计与决策/RULE-REGISTRY.local.jsonl",
    "data/training/home_absorb/workspace/Desktop/龍魂系统-知识库/02_rules/RULE-REGISTRY.local.jsonl",
    "data/training/home_absorb/workspace/Desktop/桌面项目箱/龍魂系統·統一知識矩陣/04_三色審計與決策/RULE-REGISTRY.local.jsonl",
    "data/training/home_absorb/knowledge/Obsidian/龍魂系統/02_rules/RULE-REGISTRY.local.jsonl"
  ],
  "memory.md.asc": [
    ".codebuddy/automations/notion/memory.md.asc",
    ".codebuddy/automations/automation/memory.md.asc",
    ".codebuddy/automations/automation-2/memory.md.asc",
    ".codebuddy/automations/automation-4/memory.md.asc"
  ],
  "memory.md": [
    ".codebuddy/automations/notion/memory.md",
    ".codebuddy/automations/automation/memory.md",
    ".codebuddy/automations/automation-2/memory.md",
    ".codebuddy/automations/automation-4/memory.md"
  ],
  "automation.toml.asc": [
    ".codebuddy/automations/crystal-daily-scan/automation.toml.asc",
    ".codebuddy/automations/automation/automation.toml.asc",
    ".codebuddy/automations/automation-2/automation.toml.asc",
    ".codebuddy/automations/automation-4/automation.toml.asc"
  ],
  "automation.toml": [
    ".codebuddy/automations/crystal-daily-scan/automation.toml",
    ".codebuddy/automations/automation/automation.toml",
    ".codebuddy/automations/automation-2/automation.toml",
    ".codebuddy/automations/automation-4/automation.toml"
  ],
  "SKILL.md.asc": [
    ".codebuddy/skills/longhun-deben-audit/SKILL.md.asc",
    ".codebuddy/skills/longhun-vuln-detect/SKILL.md.asc",
    ".codebuddy/skills/longhun-wuxing/SKILL.md.asc",
    ".codebuddy/skills/longhun-orchestrator/SKILL.md.asc",
    ".codebuddy/skills/longhun-anti-tamper/SKILL.md.asc",
    ".codebuddy/skills/longhun-circuit-breaker/SKILL.md.asc",
    ".codebuddy/skills/longhun-three-color-audit/SKILL.md.asc",
    ".codebuddy/skills/longhun-digital-root/SKILL.md.asc",
    ".codebuddy/skills/longhun-gpg-sign/SKILL.md.asc",
    ".codebuddy/skills/longhun-trust-score/SKILL.md.asc",
    ".codebuddy/skills/longhun-deploy/SKILL.md.asc",
    ".codebuddy/skills/longhun-xpay/SKILL.md.asc",
    ".codebuddy/skills/longhun-persona-orchestrate/SKILL.md.asc",
    ".codebuddy/skills/longhun-dao-de-jing/SKILL.md.asc",
    ".codebuddy/skills/longhun-search/SKILL.md.asc",
    ".codebuddy/skills/longhun-memory-load/SKILL.md.asc",
    ".codebuddy/skills/longhun-ai-model/SKILL.md.asc",
    ".codebuddy/skills/longhun-auto-heal/SKILL.md.asc",
    ".codebuddy/skills/longhun-identity-verify/SKILL.md.asc",
    ".codebuddy/skills/longhun-cnsh-translate/SKILL.md.asc",
    "02_SKILLS/SKILL.md.asc",
    "02_SKILLS/downloads_archive/Kimi_Agent_龍魂体系技能检查/longhun-warehouse-audit/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-zeng-digital-human/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/dragon-soul-agent/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-harmonyos/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-3core-opt/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-finance/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-dna-align/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-ocr/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-benchmark/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-ios/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-asr/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-behavior-engine/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-monitoring/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-nlp/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-formula-opt/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-cnsh/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-cross-platform/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-agent-eco/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-daemon/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-archive/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-governance/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-riemann/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-backup/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-cloud-panel/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-cloud-mcp/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-deployment-ready/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-cloud-notion/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-audit/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-cloud-kimi/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-review/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-cloud-deploy/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-automation/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-integration/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-multicurrency/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/protocols/CNSH-SEMANTIC/SKILL.md.asc",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/protocols/CNSH-PROTOCOL/SKILL.md.asc",
    "_work/repos/ai-truth-protocol/longhun-system/signatures/SKILL.md.asc",
    "data/training/home_absorb/workspace/Desktop/龍魂系统·统一知识矩阵/13_技能库与对外接口/SKILL.md.asc",
    "data/training/home_absorb/workspace/Desktop/桌面项目箱/龍魂系統·統一知識矩陣/13_技能庫與對外接口/SKILL.md.asc",
    "data/training/home_absorb/sources/longhun-kimi-skills/skills/longhun-memory-bootstrap/SKILL.md.asc",
    "data/training/home_absorb/sources/longhun-kimi-skills/skills/longhun-priority-sort/SKILL.md.asc",
    "data/training/home_absorb/sources/longhun-kimi-skills/skills/dragon-soul-agent/SKILL.md.asc",
    "layers/L7_数据层/claude_extracted/raw/skills/a89d76ba-6216-42b3-ba33-e18194ebb230/b84aa772-13a2-4c76-ae42-f31f0ff2ce57/local_44e185fd-8cce-463c-b23f-e533932fa24c/outputs/SKILL.md.asc",
    "skills/longhun-tongxinyi-v2/SKILL.md.asc",
    "skills/warehouse-audit/SKILL.md.asc",
    "skills/longhun-ai-lexicon/SKILL.md.asc",
    "skills/longhun-kg-paper-index/SKILL.md.asc",
    "skills/longhun-tags/SKILL.md.asc",
    "skills/longhun-cross-platform/SKILL.md.asc"
  ],
  "SKILL.md": [
    ".codebuddy/skills/longhun-deben-audit/SKILL.md",
    ".codebuddy/skills/longhun-vuln-detect/SKILL.md",
    ".codebuddy/skills/longhun-wuxing/SKILL.md",
    ".codebuddy/skills/longhun-orchestrator/SKILL.md",
    ".codebuddy/skills/longhun-anti-tamper/SKILL.md",
    ".codebuddy/skills/longhun-circuit-breaker/SKILL.md",
    ".codebuddy/skills/longhun-three-color-audit/SKILL.md",
    ".codebuddy/skills/longhun-digital-root/SKILL.md",
    ".codebuddy/skills/longhun-gpg-sign/SKILL.md",
    ".codebuddy/skills/longhun-trust-score/SKILL.md",
    ".codebuddy/skills/longhun-deploy/SKILL.md",
    ".codebuddy/skills/longhun-xpay/SKILL.md",
    ".codebuddy/skills/longhun-persona-orchestrate/SKILL.md",
    ".codebuddy/skills/longhun-dao-de-jing/SKILL.md",
    ".codebuddy/skills/longhun-search/SKILL.md",
    ".codebuddy/skills/longhun-memory-load/SKILL.md",
    ".codebuddy/skills/longhun-ai-model/SKILL.md",
    ".codebuddy/skills/longhun-auto-heal/SKILL.md",
    ".codebuddy/skills/longhun-identity-verify/SKILL.md",
    ".codebuddy/skills/longhun-cnsh-translate/SKILL.md",
    "02_SKILLS/SKILL.md",
    "02_SKILLS/downloads_archive/Kimi_Agent_龍魂体系技能检查/longhun-warehouse-audit/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-zeng-digital-human/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/dragon-soul-agent/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-harmonyos/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-3core-opt/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-finance/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-dna-align/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-ocr/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-benchmark/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-ios/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-asr/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-behavior-engine/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-monitoring/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-nlp/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-formula-opt/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-cnsh/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-cross-platform/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-agent-eco/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-daemon/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-archive/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-governance/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-riemann/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-backup/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-cloud-panel/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-cloud-mcp/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-deployment-ready/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-cloud-notion/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-audit/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-cloud-kimi/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-review/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-cloud-deploy/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-automation/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-integration/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-multicurrency/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/protocols/CNSH-SEMANTIC/SKILL.md",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/protocols/CNSH-PROTOCOL/SKILL.md",
    "_work/repos/longhun-memory-bootstrap/SKILL.md",
    "_work/repos/longhun-kimi-skills/skills/longhun-memory-bootstrap/SKILL.md",
    "_work/repos/longhun-kimi-skills/skills/longhun-priority-sort/SKILL.md",
    "_work/repos/longhun-kimi-skills/skills/dragon-soul-agent/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/SKILL.md",
    "_work/repos/longhun-system/releases/v5.1/staging/skills/warehouse-audit/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/Kimi_Agent_龍魂体系技能检查/longhun-warehouse-audit/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-zeng-digital-human/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/dragon-soul-agent/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-harmonyos/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-3core-opt/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-finance/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-dna-align/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-ocr/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-benchmark/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-ios/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-asr/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-behavior-engine/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-monitoring/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-nlp/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-formula-opt/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-cnsh/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-cross-platform/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-agent-eco/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-daemon/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-archive/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-governance/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-riemann/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/local/longhun-backup/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-cloud-panel/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-cloud-mcp/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-deployment-ready/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-cloud-notion/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-audit/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-cloud-kimi/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-review/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-cloud-deploy/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-automation/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-integration/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/cloud/longhun-multicurrency/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/protocols/CNSH-SEMANTIC/SKILL.md",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/protocols/CNSH-PROTOCOL/SKILL.md",
    "_work/repos/longhun-system/skills/longhun-tongxinyi-v2/SKILL.md",
    "_work/repos/longhun-system/skills/warehouse-audit/SKILL.md",
    "_work/repos/longhun-system/skills/longhun-ai-lexicon/SKILL.md",
    "_work/repos/longhun-system/skills/longhun-kg-paper-index/SKILL.md",
    "_work/repos/longhun-system/skills/longhun-tags/SKILL.md",
    "_work/repos/longhun-system/skills/longhun-cross-platform/SKILL.md",
    "_work/repos/longhun-system/backups/cs-kb-enhanced-20260701/SKILL.md",
    "_work/repos/longhun-system/backups/longhun-tongxinyi-v1-20260701/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/claude_extracted/raw/skills/a89d76ba-6216-42b3-ba33-e18194ebb230/b84aa772-13a2-4c76-ae42-f31f0ff2ce57/local_44e185fd-8cce-463c-b23f-e533932fa24c/outputs/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/92d21a0a593b0d44/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/352563239d529938/skills/metal-optimize/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/352563239d529938/skills/retrospective/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/352563239d529938/skills/test-ci/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/352563239d529938/skills/add-new-op/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/352563239d529938/skills/vulkan-optimize/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/352563239d529938/skills/support-new-llm/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/352563239d529938/skills/opencl-optimize/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/352563239d529938/skills/arm-cpu-optimize/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/adb45aeffc0a05bb/skills/metal-optimize/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/adb45aeffc0a05bb/skills/retrospective/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/adb45aeffc0a05bb/skills/test-ci/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/adb45aeffc0a05bb/skills/add-new-op/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/adb45aeffc0a05bb/skills/vulkan-optimize/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/adb45aeffc0a05bb/skills/support-new-llm/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/adb45aeffc0a05bb/skills/opencl-optimize/SKILL.md",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/adb45aeffc0a05bb/skills/arm-cpu-optimize/SKILL.md",
    "data/training/home_absorb/workspace/Desktop/龍魂系统·统一知识矩阵/13_技能库与对外接口/SKILL.md",
    "data/training/home_absorb/workspace/Desktop/桌面项目箱/龍魂系統·統一知識矩陣/13_技能庫與對外接口/SKILL.md",
    "data/training/home_absorb/sources/longhun-kimi-skills/skills/longhun-memory-bootstrap/SKILL.md",
    "data/training/home_absorb/sources/longhun-kimi-skills/skills/longhun-priority-sort/SKILL.md",
    "data/training/home_absorb/sources/longhun-kimi-skills/skills/dragon-soul-agent/SKILL.md",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/typer/.agents/skills/typer/SKILL.md",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fastapi/.agents/skills/fastapi/SKILL.md",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/typer/.agents/skills/typer/SKILL.md",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fastapi/.agents/skills/fastapi/SKILL.md",
    "layers/L7_数据层/claude_extracted/raw/skills/a89d76ba-6216-42b3-ba33-e18194ebb230/b84aa772-13a2-4c76-ae42-f31f0ff2ce57/local_44e185fd-8cce-463c-b23f-e533932fa24c/outputs/SKILL.md",
    "skills/longhun-tongxinyi-v2/SKILL.md",
    "skills/warehouse-audit/SKILL.md",
    "skills/longhun-ai-lexicon/SKILL.md",
    "skills/longhun-kg-paper-index/SKILL.md",
    "skills/longhun-tags/SKILL.md",
    "skills/longhun-cross-platform/SKILL.md"
  ],
  "registry.json": [
    ".commander/registry.json",
    "02_SKILLS/downloads_archive/新技能/longhun-v5-skills/registry/registry.json",
    "_work/repos/longhun-system/cnsh/core/registry/v5-skills/registry.json",
    "_work/repos/longhun-system/02_SKILLS/downloads_archive/新技能/longhun-v5-skills/registry/registry.json",
    "_work/repos/longhun-system/cnsh-core/registry/v5-skills/registry.json",
    "_work/repos/longhun-system/L7_数据层/persona_knowledge/registry.json",
    "cnsh/core/registry/v5-skills/registry.json",
    "data/training/home_absorb/sources/UID9622_Workspace/backend_personas/router/registry.json",
    "digital_humans/registry.json",
    "dist/longhun-system-v5.0.0-opensource/cnsh/core/registry/v5-skills/registry.json",
    "layers/L7_数据层/persona_knowledge/registry.json"
  ],
  "LICENSE": [
    ".daoyin_workspace/distributed_hardware_fwk/LICENSE",
    ".daoyin_workspace/ability_ability_base/LICENSE",
    "_work/repos/LonghunFont/LICENSE",
    "_work/repos/onghun-system/LICENSE",
    "_work/repos/longhun-memory-bootstrap/LICENSE",
    "_work/repos/longhun-anti-colonial/LICENSE",
    "_work/repos/longhun-kimi-skills/LICENSE",
    "_work/repos/CNSH/LICENSE",
    "_work/repos/uid9622-open-blueprint/LICENSE",
    "_work/repos/cnsh-runtime/LICENSE",
    "_work/repos/longhun-system/LICENSE",
    "_work/repos/longhun-calendar/LICENSE",
    "_work/repos/ai-truth-protocol/longhun-system/CNSH-整理版/LICENSE",
    "_work/repos/longhun-system/cnsh-repo-push/LICENSE",
    "_work/repos/longhun-system/xpay/LICENSE",
    "_work/repos/longhun-system/longhun-font/LICENSE",
    "_work/repos/longhun-system/editors/codebuddy/longhun-console/LICENSE",
    "_work/repos/longhun-system/editors/codebuddy/model-router/LICENSE",
    "_work/repos/longhun-system/editors/codebuddy/protocol-checker/LICENSE",
    "_work/repos/longhun-system/editors/codebuddy/audit-tracker/LICENSE",
    "_work/repos/longhun-system/editors/codebuddy/one-click-deploy/LICENSE",
    "_work/repos/longhun-system/dev-env/chinese-editor/LICENSE",
    "_work/repos/longhun-system/_archive/cnsh-history/CNSH-整理版/LICENSE",
    "_work/repos/longhun-system/L7_数据层/gitee-mirror/dragon-soul-pack/字体支持/LICENSE",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/d6bf38ad64e1a7d7/LICENSE",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/80d5362c4d7ddba1/LICENSE",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/3618dc578b94e5c8/LICENSE",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/f715e6f83e9280f6/tests/src/test_libs/rnd_unicodes/rnd_unicodes/LICENSE",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/f715e6f83e9280f6/scripts/built_in_font/font_license/DejaVuSans/LICENSE",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/f715e6f83e9280f6/src/libs/FT800-FT813/LICENSE",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/f715e6f83e9280f6/src/libs/gif/LICENSE",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/352563239d529938/3rd_party/protobuf/LICENSE",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/352563239d529938/apps/frameworks/sherpa-mnn/LICENSE",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/adb45aeffc0a05bb/3rd_party/protobuf/LICENSE",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/adb45aeffc0a05bb/apps/frameworks/sherpa-mnn/LICENSE",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/ed4eac3aa730d902/tests/src/test_libs/rnd_unicodes/rnd_unicodes/LICENSE",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/ed4eac3aa730d902/scripts/built_in_font/font_license/DejaVuSans/LICENSE",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/ed4eac3aa730d902/src/libs/FT800-FT813/LICENSE",
    "_work/repos/longhun-system/L7_数据层/daoyin/mirror/ed4eac3aa730d902/src/libs/gif/LICENSE",
    "apps/homeowner-toolkit/LICENSE",
    "cnsh/xpay/LICENSE",
    "cnsh/longhun-font/LICENSE",
    "cnsh/core/runtime_governance/venv_notion/lib/python3.14/site-packages/pip-26.1.1.dist-info/licenses/src/pip/_vendor/packaging/LICENSE",
    "cnsh/core/runtime_governance/venv_notion/lib/python3.14/site-packages/pip-26.1.1.dist-info/licenses/src/pip/_vendor/truststore/LICENSE",
    "cnsh/core/runtime_governance/venv_notion/lib/python3.14/site-packages/pip-26.1.1.dist-info/licenses/src/pip/_vendor/pygments/LICENSE",
    "cnsh/core/runtime_governance/venv_notion/lib/python3.14/site-packages/pip-26.1.1.dist-info/licenses/src/pip/_vendor/distro/LICENSE",
    "cnsh/core/runtime_governance/venv_notion/lib/python3.14/site-packages/pip-26.1.1.dist-info/licenses/src/pip/_vendor/requests/LICENSE",
    "cnsh/core/runtime_governance/venv_notion/lib/python3.14/site-packages/pip-26.1.1.dist-info/licenses/src/pip/_vendor/tomli/LICENSE",
    "cnsh/core/runtime_governance/venv_notion/lib/python3.14/site-packages/pip-26.1.1.dist-info/licenses/src/pip/_vendor/certifi/LICENSE",
    "cnsh/core/runtime_governance/venv_notion/lib/python3.14/site-packages/pip-26.1.1.dist-info/licenses/src/pip/_vendor/pyproject_hooks/LICENSE",
    "cnsh/core/runtime_governance/venv_notion/lib/python3.14/site-packages/pip-26.1.1.dist-info/licenses/src/pip/_vendor/rich/LICENSE",
    "cnsh/core/runtime_governance/venv_notion/lib/python3.14/site-packages/pip-26.1.1.dist-info/licenses/src/pip/_vendor/pkg_resources/LICENSE",
    "cnsh/core/runtime_governance/venv_notion/lib/python3.14/site-packages/pip-26.1.1.dist-info/licenses/src/pip/_vendor/resolvelib/LICENSE",
    "cnsh/core/runtime_governance/venv_notion/lib/python3.14/site-packages/pip-26.1.1.dist-info/licenses/src/pip/_vendor/platformdirs/LICENSE",
    "cnsh/core/runtime_governance/venv_notion/lib/python3.14/site-packages/notion_client-3.1.0.dist-info/licenses/LICENSE",
    "cnsh/core/runtime_governance/venv_notion/lib/python3.14/site-packages/anyio-4.13.0.dist-info/licenses/LICENSE",
    "data/training/home_absorb/workspace/Desktop/龍魂系统-知识库/_archive/cnsh-history/CNSH-整理版/LICENSE",
    "data/training/home_absorb/workspace/Desktop/桌面项目箱/龍魂黎曼猜想_投稿包/LICENSE",
    "data/training/home_absorb/workspace/Desktop/桌面项目箱/打包待命/龍魂万年历-生态入口包/LICENSE",
    "data/training/home_absorb/knowledge/Obsidian/龍魂系統/_archive/cnsh-history/CNSH-整理版/LICENSE",
    "data/training/home_absorb/sources/longhun-anti-colonial/LICENSE",
    "data/training/home_absorb/sources/龍芯北辰UID9622签章/LICENSE",
    "data/training/home_absorb/sources/longhun-kimi-skills/LICENSE",
    "data/training/home_absorb/sources/CLA系列/LICENSE",
    "data/training/home_absorb/sources/cnsh-runtime/LICENSE",
    "data/training/home_absorb/sources/longhun-calendar/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/typing_inspect-0.9.0.dist-info/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/dataclasses_json-0.6.7.dist-info/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pydantic_core-2.46.4.dist-info/licenses/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/marshmallow-3.26.2.dist-info/licenses/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/packaging-26.2.dist-info/licenses/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip/_vendor/packaging/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip/_vendor/truststore/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip/_vendor/pygments/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip/_vendor/distro/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip/_vendor/requests/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip/_vendor/tomli/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip/_vendor/certifi/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip/_vendor/pyproject_hooks/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip/_vendor/rich/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip/_vendor/tomli_w/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip/_vendor/pkg_resources/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip/_vendor/resolvelib/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip/_vendor/platformdirs/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/typing_extensions-4.15.0.dist-info/licenses/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pydantic-2.13.4.dist-info/licenses/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip-26.1.2.dist-info/licenses/src/pip/_vendor/packaging/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip-26.1.2.dist-info/licenses/src/pip/_vendor/truststore/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip-26.1.2.dist-info/licenses/src/pip/_vendor/pygments/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip-26.1.2.dist-info/licenses/src/pip/_vendor/distro/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip-26.1.2.dist-info/licenses/src/pip/_vendor/requests/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip-26.1.2.dist-info/licenses/src/pip/_vendor/tomli/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip-26.1.2.dist-info/licenses/src/pip/_vendor/certifi/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip-26.1.2.dist-info/licenses/src/pip/_vendor/pyproject_hooks/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip-26.1.2.dist-info/licenses/src/pip/_vendor/rich/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip-26.1.2.dist-info/licenses/src/pip/_vendor/tomli_w/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip-26.1.2.dist-info/licenses/src/pip/_vendor/pkg_resources/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip-26.1.2.dist-info/licenses/src/pip/_vendor/resolvelib/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/pip-26.1.2.dist-info/licenses/src/pip/_vendor/platformdirs/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/typing_inspection-0.4.2.dist-info/licenses/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/annotated_types-0.7.0.dist-info/licenses/LICENSE",
    "data/training/home_absorb/sources/龍魂系统/运行环境/lib/python3.14/site-packages/mypy_extensions-1.1.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/portal/warp-lab/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/tools/AP_BWE_main/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/shellingham-1.5.4.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/semantic_version-2.10.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/cn2an-0.5.24.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/tomlkit-0.12.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/soundfile-0.14.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/kaldiio-2.18.1.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pydub-0.25.1.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fast_langdetect/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/onnxruntime/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torchmetrics-1.5.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/defusedxml-0.7.1.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/contourpy-1.3.3.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/inflect-7.5.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/python_mecab_ko_dic-2.1.1.post2.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/matplotlib-3.11.1.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/transformers-4.50.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torchaudio-2.5.1.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/aliyun_python_sdk_kms-2.16.5.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/protobuf-7.35.1.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/proces-0.1.7.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/mdurl-0.1.2.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/python_dateutil-2.9.0.post0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/mpmath-1.3.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.5.1.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/ffmpeg_python-0.2.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/cycler-0.12.1.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pandas-2.3.3.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/websockets-12.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/split_lang-2.1.1.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pillow-10.4.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/sympy-1.13.1.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fasttext_predict-0.9.2.4.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/g2pk2-0.0.3.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/python_mecab_ko-1.3.7.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/psutil-7.2.2.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/six-1.17.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/ToJyutping-3.2.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/importlib_resources-6.5.2.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fsspec-2026.4.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/audioread-3.1.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/threadpoolctl-3.6.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/tensorboardx-2.6.5.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fastapi_cli-0.0.32.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/colorlog-6.12.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/multidict-6.7.1.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/lightning_utilities-0.15.3.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/opencc-1.4.1.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/rotary_embedding_torch-0.9.1.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fastapi_cloud_cli-0.23.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fastapi-0.141.1.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/einops-0.8.2.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/tensorboard-2.21.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/numba-0.66.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torchaudio-2.11.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/llvmlite-0.48.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/crcmod-1.7.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/requests-2.34.2.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/ruff-0.16.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/funasr-1.3.30.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/rich-15.0.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/tiktoken-0.13.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pydantic-2.10.6.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/aliyun_python_sdk_core-2.16.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch_einops_utils-0.1.12.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/propcache-0.5.2.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/kiwisolver-1.5.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/packaging-26.2.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/yarl-1.24.5.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/sentry_sdk-2.66.1.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/tzdata-2026.3.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/gradio-4.44.1.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/typer-0.27.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/dnspython-2.8.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fastar-0.11.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pydantic_extra_types-2.11.1.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/distance-0.1.3.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/charset_normalizer-3.4.9.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/email_validator-2.3.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/modelscope_hub-0.1.8.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/einx-0.4.3.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fonttools-4.63.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/packaging/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/truststore/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/pygments/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/distro/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/requests/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/tomli/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/certifi/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/pyproject_hooks/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/rich/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/tomli_w/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/pkg_resources/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/resolvelib/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/platformdirs/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/aiohappyeyeballs-2.7.1.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/grpcio-1.83.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/rapidfuzz-3.14.5.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/oss2-2.19.1.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/huggingface_hub-0.36.2.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/numpy/ma/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fsspec-2026.7.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/budoux-0.8.4.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools-78.1.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/safetensors-0.8.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/aiofiles-23.2.1.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/anyio-4.14.2.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/absl_py-2.5.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/cryptography-49.0.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/packaging/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/truststore/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/pygments/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/distro/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/requests/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/tomli/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/certifi/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/rich/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/tomli_w/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/pkg_resources/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/resolvelib/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/platformdirs/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/httptools-0.8.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/httptools-0.8.0.dist-info/licenses/vendor/llhttp/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/sklearn/externals/array_api_compat/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/sklearn/externals/array_api_extra/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/python_dotenv-1.2.2.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pycparser-3.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pygments-2.20.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/modelscope-1.39.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pyyaml-6.0.3.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/frozenlist-1.8.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/accelerate-1.14.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/typing_extensions-4.15.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/aiosignal-1.4.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/typeguard-4.6.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/certifi-2026.7.22.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pydantic_core-2.27.2.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/benchmark/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/composable_kernel/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/NNPACK/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/miniz-3.0.2/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/pthreadpool/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/ideep/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/onnx/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/pybind11/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fmt/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/gloo/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/mimalloc/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fbgemm/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/FXdiv/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/aiter/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/XNNPACK/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/googletest/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/flatbuffers/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/psimd/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/flash-attention/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/cpp-httplib/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/cpuinfo/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/FP16/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/mslk/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/protobuf/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/ideep/mkl-dnn/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/ideep/mkl-dnn/third_party/opencl/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/ideep/mkl-dnn/third_party/gtest/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/onnx/third_party/pybind11/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/gemmlowp/gemmlowp/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/tensorpipe/third_party/libuv/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/tensorpipe/third_party/pybind11/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/tensorpipe/third_party/googletest/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/tensorpipe/third_party/libnop/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/tensorpipe/third_party/googletest/googletest/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/tensorpipe/third_party/googletest/googlemock/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/tensorpipe/third_party/googletest/googlemock/scripts/generator/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fbgemm/fbgemm_gpu/experimental/hstu/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fbgemm/fbgemm_gpu/test/quantize/mx/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fbgemm/fbgemm_gpu/src/quantize_ops/mx/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fbgemm/external/composable_kernel/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fbgemm/external/googletest/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fbgemm/external/cpuinfo/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fbgemm/external/cpuinfo/deps/clog/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/fmt/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/googletest/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/DCGM/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/prometheus-cpp/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/cpr/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/pfs/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/googletest/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/prometheus-cpp/3rdparty/googletest/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/prometheus-cpp/3rdparty/googletest/googlemock/scripts/generator/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/prometheus-cpp/3rdparty/civetweb/examples/rest/cJSON/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/cpr/test/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/json/third_party/cpplint/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/aiter/3rdparty/composable_kernel/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/flatbuffers/dart/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/flatbuffers/swift/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/flash-attention/csrc/composable_kernel/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/flash-attention/third_party/aiter/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/flash-attention/third_party/aiter/3rdparty/composable_kernel/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/flash-attention/flash_attn/cute/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/cpuinfo/deps/clog/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/mslk/external/composable_kernel/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/mslk/external/googletest/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/mslk/mslk/attention/flash_attn/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/protobuf/third_party/benchmark/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/protobuf/third_party/googletest/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/protobuf/third_party/googletest/googletest/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/protobuf/third_party/googletest/googlemock/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/protobuf/third_party/googletest/googlemock/scripts/generator/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/NVTX/tools/docs/github-markdown-css/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/watchfiles-1.2.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools-83.0.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/annotated_types-0.8.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pyparsing-3.3.2.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/omegaconf-2.3.1.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/filelock-3.32.2.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/markdown_it_py-4.2.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/annotated_doc-0.0.5.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pydantic_settings-2.14.2.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/filelock-3.29.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/rignore-0.8.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/hydra_core-1.3.4.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/rich_toolkit-0.20.3.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/attrs-26.1.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pytorch_lightning-2.6.5.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/hf_xet-1.5.2.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/jaraco.text-3.12.1.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/jaraco.text-4.0.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/jaraco.collections-5.1.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/importlib_metadata-8.0.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/jaraco.functools-4.0.1.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/jaraco.context-5.3.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/inflect-7.3.1.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/autocommand-2.2.2.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/backports.tarfile-1.2.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/typeguard-4.3.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/packaging-24.2.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/zipp-3.19.2.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/tomli-2.0.1.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/typing_extensions-4.12.2.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/more_itertools-10.3.0.dist-info/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/tomli-2.4.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/more_itertools-10.8.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/platformdirs-4.4.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/wheel/vendored/packaging/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/importlib_metadata-8.7.1.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/jaraco_functools-4.4.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/jaraco_context-6.1.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/packaging-26.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/zipp-3.23.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/platformdirs-4.2.2.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/x_transformers-2.24.1.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pynndescent-0.6.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/typing_extensions-4.16.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fast_langdetect-1.0.1.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/platformdirs-4.11.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/cffi-2.1.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/aiohttp-3.14.3.dist-info/licenses/vendor/llhttp/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/peft-0.17.1.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/jaconv-0.5.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/typing_inspection-0.4.2.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/scipy/_lib/_uarray/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/more_itertools-11.1.0.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/chardet-7.4.3.dist-info/licenses/LICENSE",
    "data/knowledge_pull/cache/engines/gpt_sovits/GPT_SoVITS/BigVGAN/LICENSE",
    "dev-env/chinese-editor/LICENSE",
    "dist/longhun-system-v5.0.0-opensource/LICENSE",
    "dist/longhun-system-v5.0.0-opensource/tools/adapters/LICENSE",
    "editors/codebuddy/longhun-console/LICENSE",
    "editors/codebuddy/model-router/LICENSE",
    "editors/codebuddy/protocol-checker/LICENSE",
    "editors/codebuddy/audit-tracker/LICENSE",
    "editors/codebuddy/one-click-deploy/LICENSE",
    "engines/gpt_sovits/LICENSE",
    "engines/gpt_sovits/tools/AP_BWE_main/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/shellingham-1.5.4.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/semantic_version-2.10.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/cn2an-0.5.24.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/tomlkit-0.12.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/soundfile-0.14.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/kaldiio-2.18.1.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pydub-0.25.1.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fast_langdetect/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/onnxruntime/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torchmetrics-1.5.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/defusedxml-0.7.1.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/contourpy-1.3.3.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/inflect-7.5.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/python_mecab_ko_dic-2.1.1.post2.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/matplotlib-3.11.1.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/transformers-4.50.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torchaudio-2.5.1.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/aliyun_python_sdk_kms-2.16.5.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/protobuf-7.35.1.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/proces-0.1.7.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/mdurl-0.1.2.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/python_dateutil-2.9.0.post0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/mpmath-1.3.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.5.1.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/ffmpeg_python-0.2.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/cycler-0.12.1.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pandas-2.3.3.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/websockets-12.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/split_lang-2.1.1.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pillow-10.4.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/sympy-1.13.1.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fasttext_predict-0.9.2.4.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/g2pk2-0.0.3.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/python_mecab_ko-1.3.7.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/psutil-7.2.2.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/six-1.17.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/ToJyutping-3.2.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/importlib_resources-6.5.2.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fsspec-2026.4.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/audioread-3.1.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/threadpoolctl-3.6.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/tensorboardx-2.6.5.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fastapi_cli-0.0.32.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/colorlog-6.12.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/multidict-6.7.1.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/lightning_utilities-0.15.3.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/opencc-1.4.1.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/rotary_embedding_torch-0.9.1.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fastapi_cloud_cli-0.23.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fastapi-0.141.1.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/einops-0.8.2.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/tensorboard-2.21.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/numba-0.66.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torchaudio-2.11.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/llvmlite-0.48.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/crcmod-1.7.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/requests-2.34.2.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/ruff-0.16.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/funasr-1.3.30.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/rich-15.0.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/tiktoken-0.13.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pydantic-2.10.6.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/aliyun_python_sdk_core-2.16.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch_einops_utils-0.1.12.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/propcache-0.5.2.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/kiwisolver-1.5.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/packaging-26.2.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/yarl-1.24.5.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/sentry_sdk-2.66.1.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/tzdata-2026.3.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/gradio-4.44.1.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/typer-0.27.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/dnspython-2.8.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fastar-0.11.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pydantic_extra_types-2.11.1.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/distance-0.1.3.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/charset_normalizer-3.4.9.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/email_validator-2.3.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/modelscope_hub-0.1.8.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/einx-0.4.3.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fonttools-4.63.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/packaging/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/truststore/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/pygments/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/distro/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/requests/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/tomli/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/certifi/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/pyproject_hooks/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/rich/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/tomli_w/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/pkg_resources/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/resolvelib/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip-26.2.dist-info/licenses/src/pip/_vendor/platformdirs/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/aiohappyeyeballs-2.7.1.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/grpcio-1.83.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/rapidfuzz-3.14.5.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/oss2-2.19.1.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/huggingface_hub-0.36.2.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/numpy/ma/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fsspec-2026.7.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/budoux-0.8.4.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools-78.1.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/safetensors-0.8.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/aiofiles-23.2.1.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/anyio-4.14.2.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/absl_py-2.5.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/cryptography-49.0.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/packaging/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/truststore/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/pygments/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/distro/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/requests/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/tomli/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/certifi/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/rich/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/tomli_w/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/pkg_resources/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/resolvelib/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pip/_vendor/platformdirs/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/httptools-0.8.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/httptools-0.8.0.dist-info/licenses/vendor/llhttp/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/sklearn/externals/array_api_compat/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/sklearn/externals/array_api_extra/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/python_dotenv-1.2.2.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pycparser-3.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pygments-2.20.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/modelscope-1.39.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pyyaml-6.0.3.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/frozenlist-1.8.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/accelerate-1.14.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/typing_extensions-4.15.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/aiosignal-1.4.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/typeguard-4.6.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/certifi-2026.7.22.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pydantic_core-2.27.2.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/benchmark/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/composable_kernel/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/NNPACK/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/miniz-3.0.2/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/pthreadpool/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/ideep/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/onnx/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/pybind11/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fmt/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/gloo/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/mimalloc/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fbgemm/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/FXdiv/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/aiter/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/XNNPACK/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/googletest/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/flatbuffers/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/psimd/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/flash-attention/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/cpp-httplib/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/cpuinfo/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/FP16/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/mslk/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/protobuf/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/ideep/mkl-dnn/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/ideep/mkl-dnn/third_party/opencl/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/ideep/mkl-dnn/third_party/gtest/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/onnx/third_party/pybind11/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/gemmlowp/gemmlowp/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/tensorpipe/third_party/libuv/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/tensorpipe/third_party/pybind11/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/tensorpipe/third_party/googletest/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/tensorpipe/third_party/libnop/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/tensorpipe/third_party/googletest/googletest/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/tensorpipe/third_party/googletest/googlemock/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/tensorpipe/third_party/googletest/googlemock/scripts/generator/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fbgemm/fbgemm_gpu/experimental/hstu/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fbgemm/fbgemm_gpu/test/quantize/mx/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fbgemm/fbgemm_gpu/src/quantize_ops/mx/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fbgemm/external/composable_kernel/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fbgemm/external/googletest/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fbgemm/external/cpuinfo/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/fbgemm/external/cpuinfo/deps/clog/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/fmt/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/googletest/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/DCGM/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/prometheus-cpp/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/cpr/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/pfs/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/googletest/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/prometheus-cpp/3rdparty/googletest/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/prometheus-cpp/3rdparty/googletest/googlemock/scripts/generator/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/prometheus-cpp/3rdparty/civetweb/examples/rest/cJSON/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/cpr/test/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/kineto/libkineto/third_party/dynolog/third_party/json/third_party/cpplint/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/aiter/3rdparty/composable_kernel/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/flatbuffers/dart/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/flatbuffers/swift/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/flash-attention/csrc/composable_kernel/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/flash-attention/third_party/aiter/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/flash-attention/third_party/aiter/3rdparty/composable_kernel/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/flash-attention/flash_attn/cute/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/cpuinfo/deps/clog/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/mslk/external/composable_kernel/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/mslk/external/googletest/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/mslk/mslk/attention/flash_attn/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/protobuf/third_party/benchmark/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/protobuf/third_party/googletest/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/protobuf/third_party/googletest/googletest/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/protobuf/third_party/googletest/googlemock/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/protobuf/third_party/googletest/googlemock/scripts/generator/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/torch-2.13.0.dist-info/licenses/third_party/NVTX/tools/docs/github-markdown-css/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/watchfiles-1.2.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools-83.0.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/annotated_types-0.8.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pyparsing-3.3.2.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/omegaconf-2.3.1.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/filelock-3.32.2.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/markdown_it_py-4.2.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/annotated_doc-0.0.5.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pydantic_settings-2.14.2.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/filelock-3.29.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/rignore-0.8.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/hydra_core-1.3.4.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/rich_toolkit-0.20.3.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/attrs-26.1.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pytorch_lightning-2.6.5.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/hf_xet-1.5.2.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/jaraco.text-3.12.1.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/jaraco.text-4.0.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/jaraco.collections-5.1.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/importlib_metadata-8.0.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/jaraco.functools-4.0.1.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/jaraco.context-5.3.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/inflect-7.3.1.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/autocommand-2.2.2.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/backports.tarfile-1.2.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/typeguard-4.3.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/packaging-24.2.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/zipp-3.19.2.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/tomli-2.0.1.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/typing_extensions-4.12.2.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/more_itertools-10.3.0.dist-info/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/tomli-2.4.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/more_itertools-10.8.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/platformdirs-4.4.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/wheel/vendored/packaging/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/importlib_metadata-8.7.1.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/jaraco_functools-4.4.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/jaraco_context-6.1.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/packaging-26.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/zipp-3.23.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/setuptools/_vendor/platformdirs-4.2.2.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/x_transformers-2.24.1.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/pynndescent-0.6.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/typing_extensions-4.16.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/fast_langdetect-1.0.1.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/platformdirs-4.11.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/cffi-2.1.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/aiohttp-3.14.3.dist-info/licenses/vendor/llhttp/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/peft-0.17.1.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/jaconv-0.5.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/typing_inspection-0.4.2.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/scipy/_lib/_uarray/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/more_itertools-11.1.0.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/.venv_gpt_sovits/lib/python3.12/site-packages/chardet-7.4.3.dist-info/licenses/LICENSE",
    "engines/gpt_sovits/GPT_SoVITS/BigVGAN/LICENSE",
    "layers/L7_数据层/gitee-mirror/dragon-soul-pack/字体支持/LICENSE",
    "longhun-font/LICENSE",
    "models/base_models_v4.0/DeepSeek-R1-Distill-Llama-8B/LICENSE",
    "models/base_models_v4.0/Meta-Llama-3.1-8B-Instruct/LICENSE",
    "portal/warp-lab/LICENSE",
    "research/riemann_desktop/龍魂黎曼猜想_投稿包/LICENSE",
    "tools/adapters/LICENSE",
    "tts/fish-speech/LICENSE",
    "xpay/LICENSE"
  ]
}
```
