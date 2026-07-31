# 🎯 龍魂技能去重与收口清单

> DNA: #龍芯⚡️2026-07-06-SKILLS-DEDUP-MANIFEST-v1.0
> 操作者: CodeBuddy

---

## 技能目录结构

| 目录 | 性质 | 文件数 | 说明 |
|------|------|--------|------|
| `01_技能庫/` | ⭐权威定义 | 5 | 5 个核心技能的正规定义 |
| `skills/` | 🟢运行态 | 75+ | 14 个子目录 + 顶层脚本，当前活跃 |
| `skills.backup/` | 🟡历史分支 | 32 | **全部文件与 skills/ 不同**，独立演化分支 |
| `01_技能库/` | 📦归档导入 | — | Kimi Agent 的下载/导入遗留物 |
| `skill-standards.integrated/` | 📋标准文档 | 4 | 集成/标准化报告文档 |

---

## 01_技能庫/ — 5 个核心技能（权威定义）

| 文件 | 技能名 | 状态 |
|------|--------|------|
| `code-audit.md` | 代码审计 | 🟢 |
| `dna-gen.md` | DNA 追溯码生成 | 🟢 |
| `kimi-webbridge.md` | Kimi WebBridge | 🟢 |
| `on-identity.md` | 身份核验 | 🟢 |
| `on-translate.md` | 通心译 | 🟢 |

---

## skills/ — 14 个子技能目录（运行态）

| 子目录 | 说明 |
|--------|------|
| `cnsh-aligner/` | CNSH 对齐器 |
| `core/` | 核心引擎 |
| `html-skills/` | HTML 技能 (skill-1~5) |
| `py-skills/` | Python 技能 (skill-6~10) |
| `longhun-ai-lexicon/` | AI 词典 |
| `longhun-audit-integrated/` | 审计集成 |
| `longhun-cross-platform/` | 跨平台 |
| `longhun-kg-paper-index/` | 知识图谱论文索引 |
| `longhun-shield/` | 龍魂护盾 |
| `longhun-tags/` | 标签系统 |
| `longhun-tongxinyi-v2/` | 通心意译 v2 |
| `warehouse-audit/` | 仓库审计 |
| `wucai_coloring/` | 五色着色 |
| `screenshots/` | 截图 |

---

## skills.backup/ — 历史分支（全部 32 文件与 skills/ 不同）

| 项目 | 说明 |
|------|------|
| `html-skills/` (10) | 5 个 HTML 技能 × 规格+实现 |
| `py-skills/` (10) | 5 个 Python 技能 × 规格+实现 |
| 顶层 .py (8) | phase5~7、api、init、fill 等 |
| 顶层 .json (4) | 性能报告 |
| `INTEGRATION.md` | 集成文档（旧版） |
| `README.md` | 说明（旧版） |

---

## 建议操作

1. ✅ `01_技能庫/` 为技能定义的唯一权威源
2. ✅ `skills/` 为技能运行时的唯一权威源
3. 🟡 `skills.backup/` 为独立分支 → 统一到 `_archive/` 或标记为 `skills-v1-legacy/`
4. 🟡 `01_技能库/downloads-imports/` → 归档到 `_archive/`
5. 🟡 `skill-standards.integrated/` → 归档到 `docs/` 或合并到 `01_技能庫/`

---

## 权威路由

```
技能定义 → 01_技能庫/*.md
技能实现 → skills/<skill-name>/
历史版本 → skills.backup/ (待归档)
导入残留 → 01_技能库/downloads-imports/ (待归档)
标准文档 → skill-standards.integrated/ (待归档)
```
