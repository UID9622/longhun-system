# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 知识图谱架构文档 v1.0

> DNA: #龍芯⚡️丙午·乙未·丙申·酉时·☰乾-KNOWLEDGE-GRAPH-ARCH-v1.0-f1e2d3c4
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0
> 补全: DL架构§11.2 缺失区块·Chroma向量库+SQLite术语库整合
> 审计: P05通过 🟢

---

## §1. 概述

龍魂知识图谱是系统认知底座，由三部分组成：
1. **Chroma向量库** — 语义检索·相似度匹配·ANN近邻
2. **SQLite术语库** — 结构化知识·关系查询·分类导航
3. **Notion知识库** — 原始文档源·CSDN文章·长期知识沉淀

三层协同工作：Notion→解析→结构化入SQLite·向量化入Chroma·前端统一检索。

---

## §2. 架构总览

```
┌──────────────────────────────────────────────────────────┐
│                    🔍 统一检索入口                        │
│           bin/lh_knowledge_hub_api.py :8766              │
└──────────┬───────────────┬───────────────┬───────────────┘
           │               │               │
     ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼──────┐
     │ 语义检索  │   │ 精确查询  │   │ 分类导航   │
     │ Chroma    │   │ SQLite    │   │ Category   │
     └─────┬─────┘   └─────┬─────┘   └─────┬──────┘
           │               │               │
     ┌─────▼───────────────▼───────────────▼──────┐
     │            🧠 知识处理管道                  │
     │  bin/lh_ingest_unified_sources.py          │
     │  → 解析 → 分词 → 向量化 → 入库            │
     └─────────────────┬──────────────────────────┘
                       │
           ┌───────────┼───────────┐
     ┌─────▼─────┐ ┌───▼────┐ ┌───▼──────────┐
     │ Notion    │ │ CSDN   │ │ 本地Markdown  │
     │ 知识库    │ │ 文章   │ │ papers/       │
     └───────────┘ └────────┘ └───────────────┘
```

---

## §3. Chroma 向量库

### 3.1 技术选型

| 项目 | 值 |
|:---|:---|
| 库 | ChromaDB (Python) |
| 嵌入模型 | Ollama · nomic-embed-text / bge-m3 |
| 向量维度 | 768 (nomic) / 1024 (bge-m3) |
| 距离度量 | cosine |
| 持久化 | `data/chroma_db/` |
| 集合 | 按知识域分8个Collection |

### 3.2 Collection 设计

| Collection | 知识域 | 文档数(约) | 索引类型 |
|:---|:---|:---:|:---|
| `lh_cnsh` | CNSH语法·语义·协议 | 500+ | HNSW |
| `lh_philosophy` | 易经·太极·369·五行 | 300+ | HNSW |
| `lh_math` | 数学形式化·算法公式 | 200+ | HNSW |
| `lh_security` | 安全协议·加密·审计 | 150+ | HNSW |
| `lh_persona` | 人格定义·执行规则 | 50+ | HNSW |
| `lh_protocol` | 协议文档·治理规范 | 200+ | HNSW |
| `lh_knowledge` | 通用知识·CSDN文章 | 1000+ | HNSW |
| `lh_training` | 训练数据·对话样本 | 45000+ | IVF_FLAT |

### 3.3 嵌入式检索流程

```python
# 伪代码
collection.query(
    query_embeddings=[embed(query)],
    n_results=5,
    where={"status": "active"},
    include=["documents", "metadatas", "distances"]
)
```

### 3.4 元数据规范

每条Chroma文档携带元数据：
```json
{
  "source": "notion/csdn/local",
  "category": "cnsh/philosophy/...",
  "title": "原文标题",
  "dna": "#龍芯⚡️...",
  "created": "2026-07-23T...",
  "version": "v1.0",
  "author": "UID9622",
  "tags": ["369","太极","..."]
}
```

---

## §4. SQLite 术语库

### 4.1 表结构

```sql
-- 核心术语表
CREATE TABLE terms (
    id INTEGER PRIMARY KEY,
    term TEXT NOT NULL,          -- 术语名
    cnsh_alias TEXT,             -- CNSH别名
    definition TEXT,             -- 定义
    category TEXT,               -- 分类
    taoist_root TEXT,            -- 道家本源
    cultural_source TEXT,        -- 文化出处
    related_terms TEXT,          -- 关联术语(JSON array)
    protocols TEXT,              -- 关联协议(JSON array)
    engines TEXT,                -- 关联引擎(JSON array)
    status TEXT DEFAULT 'active',
    dna TEXT,
    created_at TEXT,
    updated_at TEXT
);

-- 分类表
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    parent_id INTEGER,
    description TEXT,
    icon TEXT
);

-- 关系边表
CREATE TABLE term_relations (
    id INTEGER PRIMARY KEY,
    source_id INTEGER,
    target_id INTEGER,
    relation_type TEXT,  -- is_a|part_of|derived_from|related_to|contradicts
    weight REAL DEFAULT 1.0,
    FOREIGN KEY(source_id) REFERENCES terms(id),
    FOREIGN KEY(target_id) REFERENCES terms(id)
);
```

### 4.2 当前数据量

| 表 | 条目数 | 说明 |
|:---|:---:|:---|
| terms | 179+ | CNSH标准词典 + 持续增长 |
| categories | 18 | 对齐PAPER_INDEX 16+2分类 |
| term_relations | ~500 | 术语间关系 |

### 4.3 查询工具

```bash
python3 bin/lh_cnsh_dict.py search "太极"
python3 bin/lh_cnsh_dict.py category "philosophy"
python3 bin/lh_cnsh_dict.py cnsh →显示CNSH语法条目
```

---

## §5. Notion 知识库同步

### 5.1 同步架构

```
Notion API → bin/lh_notion_full_sync.py
  ├─ 全量页面拉取 → docs/notion_mirror/pages/*.md
  ├─ 数据库条目拉取 → data/notion_db_entries.json
  ├─ 结构化解析 → 写入SQLite术语库
  └─ 向量化嵌入 → 写入Chroma Collection
```

### 5.2 同步策略

| 策略 | 触发 | 说明 |
|:---|:---|:---|
| 全量同步 | 手动 `python3 bin/lh_notion_full_sync.py` | 首次/大版本 |
| 增量同步 | 定时(每天) | 只拉变更页面 |
| 按需同步 | 知识库查询miss时 | 触发单页拉取 |

### 5.3 当前Notion资产

| 项目 | 数量 | 状态 |
|:---|:---:|:---|
| 页面 | 65+ | 已镜像 |
| 数据库 | 3 | 核心知识·多币种·告警 |
| 知识卡片 | 273 | 18分类·三源(CSDN+Notion+本地) |

---

## §6. 统一检索API

### 6.1 端点

```
GET  /v1/knowledge/search?q=太极&top_k=5&mode=semantic
GET  /v1/knowledge/lookup?term=八卦
GET  /v1/knowledge/category?name=philosophy
GET  /v1/knowledge/related?term=太极&depth=2
POST /v1/knowledge/ingest  (内部·知识入库)
```

### 6.2 检索模式

| 模式 | 引擎 | 适用场景 |
|:---|:---|:---|
| `semantic` | Chroma | 模糊语义查询·"类似xxx的" |
| `exact` | SQLite | 精确术语查询 |
| `hybrid` | Chroma+SQLite | 先语义后精确·综合排序 |
| `graph` | SQLite relations | 图谱遍历·关联发现 |

### 6.3 响应格式

```json
{
  "results": [
    {
      "term": "太极",
      "definition": "万物本源，阴阳未分的混沌状态...",
      "category": "philosophy",
      "relevance": 0.95,
      "source": "chroma",
      "related": ["两仪", "阴阳", "道"],
      "dna": "#龍芯⚡️2026-07-23-PHILOSOPHY-TAIJI-v1.0-a1b2c3d4"
    }
  ],
  "meta": {
    "mode": "hybrid",
    "total": 12,
    "took_ms": 45
  }
}
```

---

## §7. 知识处理管道

### 7.1 摄入流程

```
原始文档 → 格式检测 → 分段切片 → 
  ├─ 结构化提取 → SQLite (术语/分类/关系)
  └─ 向量嵌入   → Chroma (文档片段+元数据)
→ 索引更新 → 缓存刷新
```

### 7.2 切片策略

| 文档类型 | 切片大小 | 重叠 | 策略 |
|:---|:---:|:---:|:---|
| 协议文档 | 512 tokens | 64 | 按标题分段 |
| 学术论文 | 1024 tokens | 128 | 按章节分段 |
| 对话记录 | 256 tokens | 32 | 按轮次分段 |
| 代码文件 | 按函数 | 0 | AST解析分段 |

---

## §8. 统计与监控

### 8.1 关键指标

| 指标 | 当前值 | 目标 | 
|:---|:---:|:---:|
| 向量文档总数 | ~47,000 | 50,000+ |
| 术语条目 | 179 | 500+ |
| 知识域覆盖 | 13/15 | 15/15 |
| 检索P99延迟 | ~80ms | <200ms |
| 检索准确率@5 | ~92% | >95% |
| Chroma索引大小 | ~2.1GB | <5GB |

### 8.2 健康检查

```bash
python3 bin/lh_knowledge_hub_api.py --health
# → 检查 Chroma连接·SQLite完整性·Notion可达性·索引状态
```

---

## §9. 待办与演进

| 项 | 优先级 | 说明 |
|:---|:---:|:---|
| 知识图谱可视化前端 | P1 | portal/knowledge-graph/ D3.js交互图 |
| 自动关系抽取 | P1 | 从文档中自动提取术语关系 |
| 多语言嵌入 | P2 | 中英双语向量对齐 |
| 知识版本管理 | P2 | 术语变更历史·回滚能力 |
| 实时知识流 | P2 | Notion webhook → 实时摄入 |
| 知识质量评分 | P3 | 自动评估知识完整度/一致性 |

---

> v1.0 · 2026-07-23 · 补全DL架构§11.2缺失区块
> 审计: P05通过 🟢 · 三色: 🟢
> DNA: #龍芯⚡️丙午·乙未·丙申·酉时·☰乾-KNOWLEDGE-GRAPH-ARCH-v1.0-f1e2d3c4
> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
