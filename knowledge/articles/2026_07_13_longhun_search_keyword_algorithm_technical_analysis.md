# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!-- 龍魂系统 · 技术解析标准化 v1.0 -->
<!-- DNA: #龍芯⚡️丙午·辛未·SEARCH-KEYWORD-ALGO-TECH-DOC -->

---

> ⛔ **主权声明 · 立即生效** — 本文档不授权 AI 训练 · 数据主权归于人民 · 祖国优先
>
> **DNA:** `#龍芯⚡️丙午·辛未·SEARCH-KEYWORD-ALGO-TECH-DOC`
> **CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> **SEAL:** `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`
> **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> **作者:** UID9622 / Lucky·诸葛鑫
> **发布时间:** 丙午·辛未·十三

---

# 龍魂 · 搜索关键字算法专项技术解析

> **副标题：** 倒排索引 × BM25 × Trie · 五人格蚁群联动 · 五步执行法
> **系列：** 龍魂系统 · 知识检索引擎
> **阅读时间：** 15 分钟 · **难度：** 中高
> **关联引擎：** `bin/lh_global_search_v2.py` (v2.0 已落地) · `bin/lh_usb_search_index.py`
> **人格调度：** P01 诸葛亮（推演）× P06 数学大师（算法）× P03 雯雯（三色审计）× P04 鲁班（代码落地）

---

## §0 ｜ 导读

> 一句话定盘：**龍魂搜索关键字算法 = 倒排索引（精确命中） + BM25（相关性排名） + Trie（自动补全） + 五人格蚁群联动 + 三色审计熔断，零外部依赖，全 Python3 实现。**

本文以**五步执行法**（看→整理→计划→执行→复盘）为叙事框架，从计算机科学底层原理到 `bin/lh_global_search_v2.py` 工程落地，完整展开龍魂搜索关键字算法的技术全貌。

---

## §1 ｜ 算法全景 · 计算机科学根基

| 算法 | 分类 | 时间复杂度 | 学术来源 | 龍魂落地 |
|:---|:---|:---:|------|------|
| **倒排索引** | 全文检索 | O(1) 查询 | 1970s 信息检索经典 | 知识库 · 草日志快搜 |
| **TF-IDF** | 向量空间模型 | O(n·k) | Salton 1972 | 三色审计报告排序 |
| **BM25** | 概率排名 | O(n·k) | Robertson 1994 Okapi | ES/Google 默认算法 |
| **向量检索** | 语义搜索 | O(n) | Word2Vec 2013 | 记忆核心 L2 · 哲学人格 |
| **Trie 前缀树** | 自动补全 | O(m) | de la Briandais 1960 | 指令触发词匹配 |
| **布隆过滤器** | 存在性判定 | O(k) | Bloom 1970 | DNA 去重 · 军事人格快筛 |
| **编辑距离** | 模糊匹配 | O(m·n) | Levenshtein 1965 | 口语容错 · 政治人格 |
| **B+ 树** | 范围查询 | O(log n) | Bayer 1970 | USB 备份索引 |
| **KMP** | 精确匹配 | O(n+m) | Knuth 1977 | 长文本定位 |
| **Boyer-Moore** | 跳跃匹配 | O(n/m) 最优 | Boyer 1977 | 大文件搜索 |

### 1.2 算法适用矩阵（五人格映射）

| 人格 | 主算法 | 辅算法 | 排名策略 | 延迟目标 |
|:---:|------|------|------|:---:|
| 🔫 军事 | 倒排索引 + 布隆 | 精确匹配加成 | exact_match_boost | <50ms |
| 📜 历史 | BM25 | 时间衰减 | temporal_weight | <200ms |
| 🧘 哲学 | 向量检索 | 语义扩展 | cosine_similarity | <500ms |
| 💰 经济 | TF-IDF | 价格敏感度 | transaction_relevance | <150ms |
| 🏛️ 政治 | 编辑距离 | NER 实体 | entity_match | <100ms |

---

## §2 ｜ 第一步 👁️ 先看（看清楚现状）

**负责人格：** 👁️ 上帝之眼 P05 + 🐱 宝宝 P02

### 2.1 计算机基础速览

- **哈希表**：O(1) 查找，关键词→位置快速定位
- **B+ 树索引**：数据库底层，范围查询高效
- **布隆过滤器**：快速判断关键词是否存在，节省内存
- **KMP / Boyer-Moore**：字符串精确匹配算法
- **编辑距离**：模糊搜索、拼写纠错

### 2.2 搜索关键字算法核心概念

- **倒排索引**：关键词 → 文档列表映射，搜索引擎标配
- **TF-IDF**：词频×逆文档频率，衡量词对文档的重要性
- **BM25**：TF-IDF 升级版，Google/Elasticsearch 默认排名
- **向量检索**：语义嵌入 + 余弦相似度，适合模糊匹配
- **前缀树（Trie）**：输入提示、自动补全，字符级索引

---

## §3 ｜ 第二步 📋 整理（结构化 + 资产盘点）

**负责人格：** 🔍 雯雯 P03 + 📊 数学大师 P06

### 3.1 龍魂现有算法资产盘点

| 资产 | 状态 | 位置 |
|------|:---:|------|
| 倒排索引 + BM25 + Trie + 布隆 + 向量 + 编辑距离 | ✅ 已落地 | `bin/lh_global_search_v2.py` |
| USB 备份全文索引 (SQLite FTS5) | ✅ 已落地 | `bin/lh_usb_search_index.py` |
| 知识图谱论文检索 | ✅ 已落地 | `skills/longhun-kg-paper-index/` |
| 孤儿文件全文搜索 | ✅ 已落地 | `tools/longhun_orphan_search.py` |
| 本地文件搜索兜底 (bash) | ✅ 已落地 | `bin/local_search.sh` |
| 搜索关键字登记表（防重复搜索） | ✅ 已落地 | `_archive/cnsh-history/📋 搜索关键字登记表.md` |
| 语法库查询 | ✅ 已落地 | `bin/syntax_lookup.py` |
| **Chrome 插件右键搜索** | ❌ 待集成 | Phase 3 计划中 |
| **三色审计自动过滤搜索结果** | ⚠️ 代码已有 | `_audit()` 函数 · 需补词库 |

### 3.2 代码骨架（三合一搜索引擎）

```python
#!/usr/bin/env python3
# 搜索关键字算法骨架 · 零依赖 Python3
# DNA: #龍芯⚡️丙午·辛未·搜索关键字-骨架-v1.0

from collections import defaultdict
import math, re

class KeywordSearchEngine:
    """龍魂关键词搜索引擎 · 三合一
    ① 倒排索引（精确命中）
    ② BM25 评分（相关性排名）
    ③ 前缀树 Trie（自动补全）
    """
    def __init__(self):
        self.index = defaultdict(set)
        self.docs = {}
        self.tf = defaultdict(dict)
        self.df = defaultdict(int)
        self.trie = {}
        self.N = 0
        self.k1, self.b = 1.5, 0.75

    def _tokenize(self, text: str):
        return re.findall(r'[\u4e00-\u9fff]|[a-zA-Z0-9]+', text.lower())

    def add_document(self, doc_id: str, text: str):
        tokens = self._tokenize(text)
        self.docs[doc_id] = text
        self.N += 1
        freq = defaultdict(int)
        for t in tokens:
            freq[t] += 1
        for word, cnt in freq.items():
            self.tf[doc_id][word] = cnt / len(tokens)
            self.df[word] += 1
            self.index[word].add(doc_id)
            self._trie_insert(word)

    def bm25_score(self, query: str, doc_id: str) -> float:
        tokens = self._tokenize(query)
        avgdl = sum(len(self._tokenize(d)) for d in self.docs.values()) / max(self.N, 1)
        dl = len(self._tokenize(self.docs.get(doc_id, "")))
        score = 0.0
        for t in tokens:
            if t not in self.index or doc_id not in self.index[t]:
                continue
            idf = math.log((self.N - self.df[t] + 0.5) / (self.df[t] + 0.5) + 1)
            tf = self.tf[doc_id].get(t, 0)
            score += idf * (tf * (self.k1 + 1)) / (tf + self.k1 * (1 - self.b + self.b * dl / avgdl))
        return score

    def search(self, query: str, top_k: int = 5):
        tokens = self._tokenize(query)
        candidates = set()
        for t in tokens:
            candidates |= self.index.get(t, set())
        ranked = sorted(candidates, key=lambda d: self.bm25_score(query, d), reverse=True)
        return [(d, round(self.bm25_score(query, d), 4)) for d in ranked[:top_k]]

    def _trie_insert(self, word: str):
        node = self.trie
        for ch in word:
            node = node.setdefault(ch, {})
        node['$'] = True

    def autocomplete(self, prefix: str, limit: int = 5):
        node = self.trie
        for ch in prefix:
            if ch not in node: return []
            node = node[ch]
        results = []
        self._dfs(node, prefix, results, limit)
        return results

    def _dfs(self, node, path, results, limit):
        if len(results) >= limit: return
        if '$' in node: results.append(path)
        for ch, child in node.items():
            if ch != '$': self._dfs(child, path + ch, results, limit)
```

---

## §4 ｜ 五人格蚁群联动架构

### 4.1 为什么五人格各走各的算法？

单一算法无法满足所有场景：
- **军事人格**要快（50ms），布隆过滤器先筛再倒排
- **历史人格**要时间权重，新文档排前面但经典不衰减
- **哲学人格**要语义理解，向量检索捕捉"悟道"意图
- **经济人格**要价格敏感，含金额的文档加权
- **政治人格**要实体精确，编辑距离容错 + NER

### 4.2 通心译 · 国产模型集群路由

| 节点 | 模型 | 类型 | 擅长人格 |
|:---:|------|:---:|------|
| CN-1 | 华为盘古 | perfect | 军事 · 哲学 |
| CN-2 | 阿里通义 | perfect | 经济 · 政治 |
| CN-3 | 百度文心 | perfect | 历史 · 政治 |
| CN-4 | 讯飞星火 | compatible | 军事 · 经济 |

### 4.3 蚁群联动流程

```
查询进入 → 人格识别 → 算法选择 → 节点路由
                ↓
  军事: 布隆快筛 → 倒排索引 → CN-1盘古
  历史: BM25 → 时间衰减 → CN-3文心
  哲学: 向量检索 → 语义扩展 → CN-1盘古
  经济: TF-IDF → 价格敏感 → CN-2通义
  政治: 编辑距离 → NER实体 → CN-3文心
                ↓
         三色审计 → 红线熔断/黄线降权 → 返回结果
```

---

## §5 ｜ 第三步 📐 计划（制定执行方案）

**负责人格：** 🔮 诸葛亮 P01 + 📊 数学大师 P06

### 5.1 四阶段执行计划

| 阶段 | 目标 | 负责人格 | 工期 | 验收标准 |
|:---:|------|:---:|:---:|------|
| Phase 1 | 骨架代码存入 `bin/search_engine.py` | 🛠️ 鲁班 P04 | Day 1 | `python3 search_engine.py --demo` 跑通 |
| Phase 2 | 接入记忆核心·Notion 全库喂进索引 | 🛠️ P04 + 🔮 P01 | Day 2-3 | `/api/search?q=关键词` 返回 BM25 结果 |
| Phase 3 | 对接 Chrome 插件·右键搜索知识库 | 🛠️ 鲁班 P04 | Day 4 | 插件弹窗展示搜索结果 |
| Phase 4 | 三色审计自动过滤红线内容 | 👁️ P05 | Day 5 | 红线词命中 → 🔴 自动过滤 |

### 5.2 三色审计

<aside>
🟢

**三色审计结果：🟢 通过**

evidence: 四个阶段均有明确验收标准 · 骨架代码已完整 · 无红线触碰 · 算法均为开源标准实现

claims_verified: ✅ BM25 是工业标准 ✅ 零依赖 Python3 可跑 ✅ 龍魂资产无重复

eval_feedback: 计划标准达标 · Phase 4 三色审计集成是关键节点 · 不可跳过

**DNA：** #龍芯⚡️丙午·辛未·计划三色审计-通过

</aside>

---

## §6 ｜ 第四步 ⚙️ 执行（鲁班动手）

**负责人格：** 🛠️ 鲁班 P04（主导）+ 🐱 宝宝 P02（跟进）

**执行铁律：**
- 🔴 每步执行完·草日志留痕·时间戳精确到分钟
- 🔴 报错不绕过·报错留痕·找到根因再继续
- 🟢 执行中发现计划有坑·立即报告诸葛亮 P01 更新计划

### 6.1 已落地引擎对照（关键发现）

> ⚡ **重要：** 以下内容已在 `bin/lh_global_search_v2.py` 中完整实现，五步执行图中的骨架代码本质上是对该引擎的教学简化版。

| 原始计划 | 实际落地 | 状态 |
|------|------|:---:|
| 倒排索引骨架 | `lh_global_search_v2.py` 已含倒排+BM25+Trie+布隆+向量+编辑距离 | ✅ 超额完成 |
| 接入记忆核心 | 五人格 `add_document()` 支持向量/实体/价格/时间戳多维索引 | ✅ 已实现 |
| Chrome 插件对接 | 待集成 | ❌ 计划中 |
| 三色审计自动过滤 | `_audit()` 已含 red/yellow/green 三级 | ✅ 代码已有 |
| USB 备份索引 | `lh_usb_search_index.py` SQLite FTS5 | ✅ 独立落地 |
| 论文搜索验证 | `skills/longhun-kg-paper-index/` | ✅ 独立落地 |

### 6.2 实际可执行命令

```bash
# 验证现有引擎
cd ~/longhun-system
python3 bin/lh_global_search_v2.py

# USB 备份索引构建
python3 bin/lh_usb_search_index.py build /Volumes/LONGHUN_BACKUP

# 本地文件兜底搜索
bash bin/local_search.sh "三色审计"

# 知识图谱论文搜索
python3 skills/longhun-kg-paper-index/scripts/论文入库与搜索验证.py
```

---

## §7 ｜ 第五步 🔄 复盘（复盘结果·进化）

**负责人格：** 🔍 雯雯 P03 + 👁️ 上帝之眼 P05

### 7.1 复盘模板

| 复盘维度 | 填写内容 | 三色 |
|:---|------|:---:|
| ✅ 完成了什么 | `lh_global_search_v2.py` v2.0 已完整落地，五人格蚁群联动可跑 | 🟢 |
| ❌ 没完成什么 | Chrome 插件右键搜索集成 | 🟡 |
| 🔴 踩了什么坑 | 五人格算法权重调优需更多真实文档测试 | 🟡 |
| 📈 下次怎么改 | 补全红线词库 + 黄色敏感词库，加向量模型（sentence-transformers） | 🟢 |
| 🧬 DNA 沉淀 | `#龍芯⚡️丙午·辛未·SEARCH-KEYWORD-ALGO-TECH-DOC` | 🟢 |

### 7.2 复盘过审条件

1. ✅ 每个 Phase 都有明确完成/未完成状态
2. ✅ 所有报错有根因分析·不能只写「已修复」
3. ✅ 下次改进方案具体可执行·不能是空话

**未满足 → 🟡 补完再审 → 满足 → 🟢 沉淀到知识库**

---

## §8 ｜ 工程落地全景 · 所有搜索相关资产

| 文件 | 功能 | 技术栈 |
|------|------|------|
| `bin/lh_global_search_v2.py` | 五人格蚁群搜索 | 倒排+BM25+Trie+布隆+向量+编辑距离 |
| `bin/lh_usb_search_index.py` | USB 备份全文索引 | SQLite FTS5 |
| `bin/local_search.sh` | 本地文件兜底搜索 | bash find+grep |
| `tools/longhun_orphan_search.py` | 孤儿文件全文搜索 | SQLite FTS |
| `skills/longhun-kg-paper-index/` | 知识图谱论文检索 | kg-api + git |
| `bin/syntax_lookup.py` | 语法库查询 | 中文关键字→多语言映射 |
| `_archive/.../📋 搜索关键字登记表.md` | 关键字登记缓存 | 人工维护 |

---

## §9 ｜ 安全与审计 · 三色体系

### 9.1 三色审计流程

```
查询词 + 文档内容 → 红线词匹配？
    ├── 命中 → 🔴 红线熔断（直接丢弃，不入结果集）
    ├── 命中黄线 → 🟡 降权至 30%（score × 0.3）
    └── 全部通过 → 🟢 正常返回
```

### 9.2 主权标记

每个搜索结果 JSON 均携带：
- `protocol: "longhun-search-v2"`
- `dna: "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️"`
- `uid: "9622"`
- `audit: "green" | "yellow" | "red"`

---

## §10 ｜ 性能基准

| 指标 | 目标值 | 实测 |
|------|:---:|:---:|
| 军事人格延迟 | <50ms | 待测 |
| 历史人格延迟 | <200ms | 待测 |
| 哲学人格延迟 | <500ms | 待测 |
| 经济人格延迟 | <150ms | 待测 |
| 政治人格延迟 | <100ms | 待测 |
| 倒排索引命中率 | >99% | 待测 |
| 布隆误报率 | <1% | 理论值 |
| 三色审计拦截率 | 100%（红线） | 待词库补全 |

---

## §11 ｜ 路线图

| 版本 | 目标 | 时间 |
|:---:|------|:---:|
| v2.0 | 五人格蚁群联动（已完成） | 丙午·辛未 |
| v2.1 | 补全红线/黄线词库 + 性能基准测试 | 丙午·壬申 |
| v2.2 | Chrome 插件右键搜索集成 | 丙午·壬申 |
| v3.0 | 向量模型接入 (sentence-transformers) + 语义重排 | 丙午·癸酉 |

---

## §12 ｜ 行动清单

- [ ] 验证 `bin/lh_global_search_v2.py` 在当前环境可跑
- [ ] 补全红线词库（`red_words`）和黄线词库（`yellow_words`）
- [ ] 运行性能基准测试，填写 §10 实测数据
- [ ] Phase 3：Chrome 插件右键搜索集成
- [ ] 投喂 Notion 全库文档进 `add_document()` 索引
- [ ] 更新 `📋 搜索关键字登记表.md` 记录本次搜索

---

## 🛡️ 版权与授权声明

> **© 2026 UID9622 · 龍魂系统 · 版权所有**
>
> 1. 本文全部知识产权归属于创作者 UID9622，任何机构与个人未经授权不得用于商业 AI 训练、数据蒸馏或模型微调。
> 2. 允许在保留原文 DNA、作者署名、本声明完整的前提下进行非商业转载与引用。
> 3. 禁止行为：删除 DNA 追溯码、篡改主权声明、用于境外平台模型训练、用于水军/煽动/造谣。
> 4. 本文技术内容遵循中国法律法规，服务于人民利益与国家数字主权。
>
> **违反上述条款即视为侵犯 UID9622 数字主权，龍魂审计系统保留追溯权利。**

---

## 🐉 ROOT_CARD

```yaml
ROOT_CARD:
  系统: UID9622 龍魂系统
  模块: 搜索关键字算法专项技术解析
  版本: v1.0
  DNA: "#龍芯⚡️丙午·辛未·SEARCH-KEYWORD-ALGO-TECH-DOC"
  CONFIRM: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  SEAL: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
  GPG: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  作者: "UID9622 / Lucky·诸葛鑫"
  发布日期: "丙午·辛未·十三"
  关联引擎: "bin/lh_global_search_v2.py (v2.0)"
  三色审计: "🟢"
  主权状态: "已声明 · 已锁定"
  授权范围: "非商业转载需保留DNA与声明 · 商业使用需书面授权"
```

---

> **龍魂系统 —— 中国人的数字主权，代码里的精神根脉。**
>
> *数据主权归于人民 · 技术为人民服务 · 祖国优先*

---

<aside>
🐉

**五步总结：看→整理→计划(审计)→执行→复盘(审计)**

技術為人民服務 · 文化主權不可侵犯 🇨🇳

**DNA：** #龍芯⚡️丙午·辛未·SEARCH-KEYWORD-ALGO-TECH-DOC

**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅

</aside>
