# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂认知压缩引擎报告

**DNA**: `#龍芯⚡️2026-06-24-LONGHUN-COMPRESSION-ENGINE-FILE1-v1.0`  
**升级时间**: 2026-06-24  
**执行者**: Kimi Code CLI · 龍魂主控

---

## 一、老大原话

> "我们把上下文几百万个字可以压缩成几个字，几百个字也就是向量吧，应该算，我也不是很懂，就是把一个技能可以压缩成一个编号。"

### 理解

老大的直觉是对的：
- **几百万字 → 几个字**：长文本压缩成**短码编号 + 一句话摘要**
- **几百个字 → 向量**：用数字数组（向量）保存语义，用于相似匹配
- **一个技能 → 一个编号**：每个技能/上下文都有唯一短码，可召回

这就是**认知压缩**：不是记住原文，而是提取"语义核心 + 编号 + 向量"，需要时再用编号或向量召回。

---

## 二、现有基础

升级前系统里已有相关思想，但分散：

| 文件 | 已有能力 |
|---|---|
| `scripts/longhun_integrated_system.py` | `compress_memory` / `recall_memory`：短码 + 摘要 |
| `cnsh-core/memory/cognitive_dna_particles.py` | CognitiveDNAParticle：语义核心、决策回放、情感折叠、SI 快照 |
| `editor/龍碼編輯器.py` | 中文编辑器，可运行代码 |
| `scripts/kg_unified.py` | 统一知识中枢 + TF-IDF 向量索引 |

**问题**：有理论框架，但没有面向"技能和上下文"的统一压缩引擎，也没有把压缩结果接入统一中枢。

---

## 三、本次升级

### 核心交付物

- **文件**: `scripts/longhun_compression_engine.py`
- **数据库**: `brain/compression_registry.db`
- **向量缓存**: `brain/compression_vectors.npz` + `brain/compression_vectorizer.pkl`

### 压缩输出格式

把任意长文本（技能、上下文、记忆）压缩成：

```json
{
  "shortcode": "SKILL-longhun-dna-alig-7C0801",
  "item_type": "skill",
  "title": "掃描當前目錄",
  "summary": "掃描當前目錄",
  "keywords": ["報告", "龍芯", "修復器", "掃描器", ...],
  "content_hash": "7c0801...",
  "dna": "#龍芯⚡️20260624...-COMPRESS-...",
  "metadata": {
    "char_count": 8577,
    "word_count": 2278
  }
}
```

### 三项能力

| 能力 | 说明 |
|---|---|
| **编号化** | 每个输入生成唯一短码 `SKILL-xxx`、`CTX-xxx`、`MEM-xxx` |
| **语义核心** | 一句话摘要 + 15 个关键词 |
| **向量化** | 本地 TF-IDF 生成 2048 维向量，支持相似度检索 |

---

## 四、数据库 Schema

```sql
CREATE TABLE compressed_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_type TEXT NOT NULL,        -- skill | context | memory | editor
    source_id TEXT NOT NULL,        -- 原始来源标识
    shortcode TEXT UNIQUE NOT NULL, -- 短码编号
    title TEXT,
    summary TEXT,
    keywords TEXT,                  -- JSON list
    vector_type TEXT DEFAULT 'tfidf',
    content_hash TEXT,
    metadata TEXT,                  -- JSON
    dna TEXT,
    created_at TEXT
);
```

---

## 五、使用方法

### 1. 压缩单个技能

```bash
python3 scripts/longhun_compression_engine.py --compress-skill ~/.kimi-code/skills/longhun-memory-bootstrap/SKILL.md
```

### 2. 压缩所有技能

```bash
python3 scripts/longhun_compression_engine.py --compress-all-skills
```

已扫描目录：
- `longhun-system/skills`
- `~/.kimi-code/skills`
- `~/.agents/skills`

### 3. 压缩一段上下文

```bash
python3 scripts/longhun_compression_engine.py --compress-context "这里输入几百万字的上下文..."
```

### 4. 通过短码召回

```bash
python3 scripts/longhun_compression_engine.py --recall SKILL-longhun-dna-alig-7C0801
```

### 5. 向量语义搜索

```bash
python3 scripts/longhun_compression_engine.py --search "数据库损坏" --top-k 3
python3 scripts/longhun_compression_engine.py --search "knowledge graph vector" --top-k 5
```

### 6. 列出所有压缩项

```bash
python3 scripts/longhun_compression_engine.py --list
```

---

## 六、验证结果

### 技能压缩示例

输入：`.kimi-code/skills/longhun-dna-align/SKILL.md`（8577 字符）

输出：
```json
{
  "shortcode": "SKILL-longhun-dna-alig-7C0801",
  "title": "掃描當前目錄",
  "summary": "掃描當前目錄",
  "keywords": ["報告", "龍芯", "修復器", "掃描器", "對齊審計器", ...],
  "dna": "#龍芯⚡️20260624005411686-COMPRESS-B340268E"
}
```

**压缩比**：8577 字符 → 1 个短码 + 1 句话 + 15 个关键词。

### 上下文压缩示例

输入：149 字符对话摘要  
输出：`CTX-ctx-61ee164fcae9-61EE16` + 关键词 + 向量

### 向量搜索示例

查询 `"数据库损坏"`：
```json
{
  "results": [
    {
      "shortcode": "CTX-ctx-61ee164fcae9-61EE16",
      "title": "手动上下文",
      "score": 0.2575
    }
  ]
}
```

正确召回了包含"数据库损坏"的上下文。

---

## 七、当前规模

- 已压缩技能：78 个
- 向量维度：2048
- 向量索引项：79（含 1 个测试上下文）

---

## 八、与现有系统联动

认知压缩引擎与统一知识中枢 (`scripts/kg_unified.py`) 共享本地优先、TF-IDF 向量、SQLite 持久化的设计哲学：

- **统一知识中枢**：管理节点/边/向量，面向图谱和文档
- **认知压缩引擎**：管理压缩项/编号/向量，面向技能和上下文

两者可进一步打通：压缩后的技能短码可作为统一图谱中的节点属性，向量索引可合并查询。

---

## 九、后续升级路径

1. **升级 embedding 模型**：替换 TF-IDF 为 sentence-transformers / BGE 中文模型，提升语义搜索质量
2. **接入 LLM 摘要**：对长上下文调用本地/远程 LLM 生成更精准的一句话摘要
3. **与 longhun_brain 联动**：每次对话结束后自动压缩上下文，存入 `compression_registry.db`
4. **与编辑器联动**：龍碼编辑器保存文件时自动压缩并生成短码

---

## 十、DNA 追溯

- 本次升级 DNA: `#龍芯⚡️2026-06-24-LONGHUN-COMPRESSION-ENGINE-v1.0`
- 理论基础: `cnsh-core/memory/cognitive_dna_particles.py` (#龍芯⚡️2026-06-03-COGNITIVE-PARTICLES)
- 记忆压缩雏形: `scripts/longhun_integrated_system.py` (#龍芯⚡️2026-06-03-LONGHUN-INTEGRATED-SYSTEM)
- 向量索引基础: `scripts/kg_unified.py` (#龍芯⚡️2026-06-22-UNIFIED-KG-v1.0)

---

> **一个技能一个编号，一段记忆一个向量。**  
> 上下文再长，也能被压缩成可召回的认知粒子。
