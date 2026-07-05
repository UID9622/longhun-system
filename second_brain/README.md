<!-- #龍芯⚡️2026-06-29-SECOND-BRAIN-README-v1.0 -->

# 🧠 龍魂第二大脑

把 Obsidian vault（`~/Obsidian/龍魂系統`）同步进 `~/longhun-system`，让 Kimi 可以本地查询、追溯、调用。

## 核心文件

| 文件 | 作用 |
|---|---|
| `config.py` | 路径、DNA 前缀、集合名 |
| `importer.py` | 解析 Markdown / frontmatter / wiki-link / 标签 |
| `indexer.py` | SQLite + Chroma 向量索引 |
| `sync.py` | 全量同步 orchestrator |
| `embed_backfill.py` | 为已入库 chunks 补向量 |
| `api.py` | FastAPI 本地后台 |

## 常用命令

```bash
# 结构同步（不生成向量，秒级）
.venv_longhun_math/bin/python scripts/sync_second_brain.py --no-embed

# 向量补全（首次运行较慢，后台跑）
.venv_longhun_math/bin/python scripts/index_second_brain_embeddings.py

# 启动本地 API
bash scripts/run_second_brain_api.sh

# 查询
curl -s -X POST http://127.0.0.1:8787/query \
  -H 'Content-Type: application/json' \
  -d '{"q":"AGENT","top_k":5}'
```

## 数据位置

- SQLite：`second_brain/data/second_brain.db`
- Chroma：`second_brain/data/chroma/`
- 审计日志：`audit/second_brain_sync.jsonl`

## CNSH 双视角

每条笔记入库后自带 `{M::, CNSH::}` 卡片与 DNA 追溯码，满足龍魂三色审计。
