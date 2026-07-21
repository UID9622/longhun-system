---
name: longhun-kg-paper-index
description: >
  龍魂知识图谱论文入库技能：把本地论文目录一键复制到 longhun-system/papers/，
  索引进全局知识图谱 DB，并调用 kg-api 验证中英文搜索命中。
  当用户提及“论文入库”“放进知识图谱”“提交论文”“知识图谱搜索”
  “把论文放到仓库”“paper index”“kg index”时触发。
  入口：python3 ~/longhun-system/skills/longhun-kg-paper-index/scripts/论文入库与搜索验证.py --source-dir <源目录> [--category <子目录>] [--commit]
license: CC BY-NC-SA 4.0
metadata:
  id: longhun-kg-paper-index
  display_name: 知识图谱论文入库
  version: "1.0.0"
  author: UID9622
  dna: "#龍芯⚡️2026-07-01-KG-PAPER-INDEX-SKILL-v1.0"
  category: internal
  level: "L1-L2"
  status: active
  tags:
    - 知识图谱
    - 论文入库
    - 全局索引
    - 搜索验证
    - Git 提交
    - 文档元数据
  trigger:
    keywords:
      - 论文入库
      - 放进知识图谱
      - 提交论文
      - 知识图谱搜索
      - 把论文放到仓库
      - paper index
      - kg index
      - 论文提交
      - 入库知识图谱
      - 论文可搜索
    context: "论文/文档归档、知识图谱索引、Git 提交"
    priority: 85
---

# longhun-kg-paper-index | 龍魂知识图谱论文入库技能 v1.0

> **DNA**: `#龍芯⚡️2026-07-01-KG-PAPER-INDEX-SKILL-v1.0`  
> **责任人**: UID9622 · 不免责  
> **状态**: 🟢 已就绪

## 能力

1. **复制论文**：把指定目录下的 `.md`/`.txt`/`.markdown`/`.rst` 复制到 `longhun-system/papers/<category>/`。
2. **全局索引**：写进 `~/.longhun/global_index/global_index.db`，自动提取标题、首标题、摘要作为搜索元数据。
3. **搜索验证**：调用 `kg-api` (`http://127.0.0.1:8088`) 对中英文关键词进行命中测试。
4. **Git 提交**：可选把论文提交到 `longhun-system` 仓库。

## 使用

```bash
python3 ~/longhun-system/skills/longhun-kg-paper-index/scripts/论文入库与搜索验证.py \
        --source-dir /Users/zuimeidedeyihan/Downloads/Kimi_Agent_全球化翻译 \
        --category Kimi_Agent_全球化翻译 \
        --commit
```

参数：
- `--source-dir`：源论文目录（必填）
- `--category`：papers 下子目录名，默认取源目录 basename
- `--target-root`：论文仓库根目录，默认 `~/longhun-system/papers`
- `--db-path`：全局索引数据库，默认 `~/.longhun/global_index/global_index.db`
- `--api-url`：kg-api 搜索端点，默认 `http://127.0.0.1:8088/api/knowledge/search`
- `--verify-terms`：自定义逗号分隔验证搜索词
- `--commit`：提交到 git

## 输出示例

```json
{
  "DNA": "#龍芯⚡️20260701...",
  "category": "Kimi_Agent_全球化翻译",
  "copied": 3,
  "indexed": [...],
  "verify": [
    {"term": "责任塌缩", "total": 2},
    {"term": "Responsibility", "total": 3}
  ],
  "git_commit": "695c09d8"
}
```

## 文件结构

```
longhun-kg-paper-index/
├── SKILL.md
├── lib/
│   └── kg_indexer.py          # 轻量索引器（自包含，不依赖 watchdog）
└── scripts/
    └── 论文入库与搜索验证.py   # 一键执行入口
```

## 依赖

- Python 3.10+
- 标准库：sqlite3、hashlib、urllib、shutil、subprocess
- 外部依赖：已运行的 `kg-api` 服务用于搜索验证
