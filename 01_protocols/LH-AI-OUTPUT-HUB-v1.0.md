# 🐉 龍魂·AI产出归集Hub v1.0 · 使用指南

DNA: #龍芯⚡️丙午·丙申·戊午·亥时·䷗复-AI-OUTPUT-HUB-V1.0-GUIDE
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层·非商业·署名·相同方式共享）

---

## 一句话说清楚

> 不管你用 CodeBuddy / Claude / Kimi / Grok 哪个AI工具，
> 产出的文件全部自动归集到 `~/ai-outputs/`，一个命令搜遍所有。

---

## 目录结构

```
~/ai-outputs/
├── codebuddy/     ← CodeBuddy 产出
├── claude/        ← Claude Code 产出  
├── kimi/          ← Kimi Code 产出
├── grok/          ← Grok 产出
├── copilot/       ← Copilot 产出
├── _shared/       ← 跨工具共享区
└── _index/        ← 自动索引（JSON）
    ├── master_index.json   ← 全量索引
    └── stats.json          ← 统计数据
```

## 快速命令

| 命令 | 干什么 |
|:---|:---|
| `lh ai-report` | 查看归集总览报告 |
| `lh ai-find 关键词` | 跨工具搜索所有产出 |
| `lh ai-find 关键词 --tool kimi` | 只搜 Kimi 的产出 |
| `lh ai-scan ~/某目录 --tool kimi` | 把某目录归集到 Kimi 区 |
| `lh ai-index` | 重建索引 |
| `ai-to kimi 文件.md` | 快速归集单个文件 |
| `ai-open` | Finder 打开归集目录 |

## 符号链接（已自动配置）

| 工具 | 默认输出 | → 统一Hub |
|:---|:---|:---|
| Claude Code | `~/.claude/downloads/` | → `~/ai-outputs/claude/` |
| CodeBuddy | `~/.codebuddy/output/` | → `~/ai-outputs/codebuddy/` |
| Kimi Code | 直接写 workspace，用完 `ai-to` 归集 | → `~/ai-outputs/kimi/` |
| Grok | 同上 | → `~/ai-outputs/grok/` |

## 工作流示例

```bash
# 用 Kimi 生成了一段代码 → 存到 ~/Downloads/test.py
ai-to kimi ~/Downloads/test.py

# 用 Claude 写了一份分析报告 → 保存后归集
ai-to claude ~/longhun-system/output/report.md

# 搜一下之前谁写过"华云道"相关内容
lh ai-find "华云道"

# 看看所有工具的产出统计
lh ai-report
```

## 索引引擎技术细节

- **引擎**: `bin/lh_ai_indexer.py`（530行·纯Python·零依赖）
- **索引格式**: JSON（`_index/master_index.json`）
- **支持类型**: .md .py .js .ts .html .json .sh 等所有文本文件
- **去重策略**: 文件名 + 内容哈希（SHA-256前16位）
- **搜索权重**: 标题匹配(10) > 文件名(8) > DNA(7) > 标签(5) > 路径(3)
- **增量更新**: 5分钟内不重复扫描

## 当前状态

> 首次扫描: **23,092 文件 · 453.6 MB** 已入索引
