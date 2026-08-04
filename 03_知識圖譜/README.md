# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 03_知识图谱

**路径**：`03_知识图谱`

## 状态

🟡 本 README 由 `bin/generate_module_readmes.py` 自动生成，用于提高仓库透明度。
具体用法请结合源码与实际场景调整。

## 功能概述

该模块包含 2 个文件，主要提供 `03_知识图谱` 相关能力。

## 入口脚本

- `generate_downloads_inbox.py`：扫描 `~/Downloads` 顶层，生成 `downloads_inbox_manifest.json`、`downloads_inbox_index.md`，并同步更新 `graph_data.json` 与 `graph_index.md`。
- `migrate_downloads_inbox.py`：读取清单，按类别将非图片/DMG 交付物复制到主干对应目录，并更新清单、图谱与索引页。
- `compress_downloads_imports.py`：对 `downloads-imports` 与 `_archive` 导入区执行内容级去重硬链接，生成压缩报告。
- `build_cnsh_editor_module.py`：构建统一的 `cnsh-editor/` 模块，整合编辑器引擎/UI/关键字/平台编辑器/文档，并清理冗余副本。
- `generate_claude_sessions_inventory.py`：扫描 `~/Library/Application Support/Claude/local-agent-mode-sessions`，整理技能、功能模块、会话、输入输出、审计备份等元数据，生成 `claude_sessions_manifest.json`、`claude_sessions_index.md`，并同步追加到 `graph_data.json` 与 `graph_index.md`。

## 新增文件

- `downloads_inbox_manifest.json`：Downloads 顶层交付物的结构化清单（含状态、建议归宿、DNA、迁移目标）。
- `downloads_inbox_index.md`：人工可读索引页，含统计、分类、迁移状态、压缩与合并结果。
- `downloads_migration.log`：最近一次迁移的执行日志。
- `downloads_compression_report.json` / `downloads_compression.log`：导入区去重硬链接的报告与日志。
- `cnsh_editor_build_report.md`：`cnsh-editor/` 统一编辑器模块构建报告。
- `claude_sessions_manifest.json`：Claude 本地代理会话目录的结构化盘点（技能、模块、会话、输入输出、审计备份）。
- `claude_sessions_index.md`：人工可读索引页，含统计、技能清单、会话清单、模块/HTML 工具、自动化建议。
- `graph_data.json`：知识图谱数据，已追加 `downloads/inbox`、`cnsh-editor`、`claude-local-sessions` 等节点。
- `graph_index.md`：由 `graph_data.json` 自动重生成的索引页。

## 接口说明

- 若该模块提供 API，请在源码中查找 `api/`、`router/`、`main.py` 等入口。
- 若为脚本工具，可直接调用上述入口脚本。

## 统一知识中枢（新增）

本模块的静态图谱 `graph_data.json` 已接入龍魂统一知识中枢：

- **核心脚本**: `scripts/kg_unified.py`
- **统一数据库**: `brain/unified_kg.db`
- **向量索引**: `brain/unified_kg_vectors.npz` + `brain/unified_kg_vectorizer.pkl`
- **API 接口**: `sovereignty/portal/knowledge_api.py`

统一中枢已把以下数据源汇入同一套节点/边/向量体系：
- `03_知識圖譜/graph_data.json`（本模块）
- `~/.longhun/notion_pages/notion_pages.db`
- `~/_work/dragon_knowledge.db`
- `brain/memories.db`

对外提供统一检索能力：
- `GET /api/unified/search?q=...` — 全文 + 向量语义检索
- `GET /api/unified/graph?node_id=...` — 统一图谱扩展
- `GET /api/unified/vector?q=...` — 纯向量检索
- `GET /api/unified/stats` — 中枢统计

详见升级报告：`docs/unified-knowledge/知识图谱-向量-数据库联动升级报告_v1.0.md`

## 注意事项

- 运行前请确认依赖已安装。
- 建议先阅读源码注释，了解每个脚本的副作用。

**DNA**:#龍芯⚡️2026-06-17-MOD_03_-README-FILE1_EE3F-v1.0