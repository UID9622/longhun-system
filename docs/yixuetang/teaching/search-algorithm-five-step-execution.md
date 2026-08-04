# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!--#龍芯⚡️2026-06-21-DOC-SEARCH-ALGORITHM-FIVE-STEP-EXECUTION-v1.0 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# 搜索关键字算法 × 计算机科学 · 五步执行图

> 技术为人民服务 · 文化主权不可侵犯

---

## 第一步 👁️ 先看（看清楚现状）

**负责角色：** 全局观察角色 + 执行跟进角色

**任务：** 看懂“搜索关键字算法”是什么、已经有什么、缺什么。

### 搜索关键字算法 · 核心概念

- **倒排索引（Inverted Index）**：关键词 → 文档列表映射，搜索引擎标配
- **TF-IDF**：词频 × 逆文档频率，衡量词对文档的重要性
- **BM25**：TF-IDF 升级版，Google / Elasticsearch 默认排名算法
- **向量检索（Semantic Search）**：语义嵌入 + 余弦相似度，适合模糊匹配
- **前缀树（Trie）**：输入提示、自动补全，字符级索引

### 计算机基础 · 关键词检索相关

- **哈希表（Hash Map）**：O(1) 查找，关键词 → 位置快速定位
- **B+ 树索引**：数据库底层，范围查询高效
- **布隆过滤器（Bloom Filter）**：快速判断关键词是否存在，节省内存
- **KMP / Boyer-Moore**：字符串精确匹配算法
- **编辑距离（Levenshtein）**：模糊搜索、拼写纠错

| 算法 | 适用场景 | 时间复杂度 | 系统应用方向 |
| --- | --- | --- | --- |
| 倒排索引 | 全文搜索 · 关键词命中 | O(1) 查询 | 知识库检索 · 日志快搜 |
| TF-IDF / BM25 | 文档相关性排名 | O(n·k) | 审计报告排序 |
| 向量检索 | 语义搜索 · 模糊匹配 | O(n) → faiss 加速 | 记忆核心 L2 语义层 |
| Trie 前缀树 | 自动补全 · 前缀提示 | O(m) m=词长 | 指令触发词快速匹配 |
| 布隆过滤器 | 快速存在性判断 | O(k) k=哈希数 | 编码去重 · 水军预筛 |
| 编辑距离 | 拼写纠错 · 模糊搜索 | O(m·n) | 口语输入容错 |

---

## 第二步 📋 整理（把现有内容结构化）

**负责角色：** 审计角色 + 算法角色

**任务：** 把“看”到的东西分门别类，找出系统里已有的、缺的、可复用的。

### 现有算法资产盘点（已落地）

- ✅ 三色审计置信度算法 → 已有知识卡
- ✅ 五行数字根熔断算法 → MVP Python 脚本已跑通
- ✅ 向量检索占位 → 引擎 L2 语义层已预留
- ✅ 水军行为识别（余弦 + IP 聚类）→ 已有知识卡
- ❌ **搜索关键字算法** → **缺失 · 本次补全目标**
- ❌ 倒排索引实现 → 缺
- ❌ BM25 排名 → 缺
- ❌ Trie 自动补全 → 缺

### 整理产出 · 关键词搜索算法骨架（Python 3 · 零依赖）

```python
from collections import defaultdict
import math, re

class KeywordSearchEngine:
    """
    关键词搜索引擎 · 三合一
    ① 倒排索引（精确命中）
    ② BM25 评分（相关性排名）
    ③ 前缀树 Trie（自动补全）
    """
    def __init__(self):
        self.index = defaultdict(set)    # 倒排索引: word → {doc_ids}
        self.docs  = {}                  # doc_id → 原文
        self.tf    = defaultdict(dict)   # tf[doc_id][word]
        self.df    = defaultdict(int)    # df[word] = 含此词的文档数
        self.trie  = {}                  # 前缀树根节点
        self.N     = 0                   # 文档总数
        # BM25 参数
        self.k1, self.b = 1.5, 0.75

    # ── 分词（中英文简版）──
    def _tokenize(self, text: str):
        return re.findall(r'[\u4e00-\u9fff]|[a-zA-Z0-9]+', text.lower())

    # ── 建索引 ──
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
            self._trie_insert(word)  # 同步写入前缀树

    # ── BM25 评分 ──
    def bm25_score(self, query: str, doc_id: str) -> float:
        tokens = self._tokenize(query)
        avgdl  = sum(len(self._tokenize(d)) for d in self.docs.values()) / max(self.N, 1)
        dl     = len(self._tokenize(self.docs.get(doc_id, "")))
        score  = 0.0
        for t in tokens:
            if t not in self.index or doc_id not in self.index[t]:
                continue
            idf = math.log((self.N - self.df[t] + 0.5) / (self.df[t] + 0.5) + 1)
            tf  = self.tf[doc_id].get(t, 0)
            score += idf * (tf * (self.k1 + 1)) / (tf + self.k1 * (1 - self.b + self.b * dl / avgdl))
        return score

    # ── 搜索（返回按 BM25 排名的结果）──
    def search(self, query: str, top_k: int = 5):
        tokens = self._tokenize(query)
        candidates = set()
        for t in tokens:
            candidates |= self.index.get(t, set())
        ranked = sorted(candidates, key=lambda d: self.bm25_score(query, d), reverse=True)
        return [(d, round(self.bm25_score(query, d), 4)) for d in ranked[:top_k]]

    # ── 前缀树插入 ──
    def _trie_insert(self, word: str):
        node = self.trie
        for ch in word:
            node = node.setdefault(ch, {})
        node['$'] = True   # 结束标记

    # ── 自动补全 ──
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

## 第三步 📐 计划（制定执行方案）

**负责角色：** 推演角色 + 算法角色

> ⚠️ **计划必须过三色审计才能出结果**

### 计划内容

把搜索算法集成进系统引擎的四个节点：

| 阶段 | 目标 | 负责角色 | 工期 | 验收标准 |
| --- | --- | --- | --- | --- |
| Phase 1 | 把上方骨架代码存入 `~/engine/search_engine.py` | 工程角色 | Day 1 | `python3 search_engine.py --demo` 能跑通 ✅ |
| Phase 2 | 接入记忆核心 · 把全库文档喂进索引 | 工程角色 + 推演角色 | Day 2-3 | `/api/search?q=关键词` 返回 BM25 排名结果 ✅ |
| Phase 3 | 对接浏览器插件 · 右键 → 搜索知识库 | 工程角色 | Day 4 | 插件弹窗能展示搜索结果 ✅ |
| Phase 4 | 三色审计自动扫描搜索结果（过滤红线内容） | 全局观察角色 | Day 5 | 红线词命中 → 🔴 自动过滤 ✅ |

### 计划三色审计

**三色审计结果：🟢 通过**

- **evidence：** 四个阶段均有明确验收标准 · 骨架代码已完整 · 无红线触碰 · 算法均为开源标准实现
- **claims_verified：** ✅ BM25 是工业标准 ✅ 零依赖 Python 3 可跑 ✅ 现有资产无重复
- **eval_feedback：** 计划标准达标 · Phase 4 三色审计集成是关键节点 · 不可跳过

---

## 第四步 ⚙️ 执行（工程角色动手）

**负责角色：** 工程角色（主导）+ 执行跟进角色（跟进）

**执行铁律：**

- 🔴 每步执行完 · 草日志留痕 · 时间戳精确到分钟
- 🔴 报错不绕过 · 报错留痕 · 找到根因再继续
- 🟢 执行中发现计划有坑 · 立即报告推演角色更新计划

```bash
# Day 1 执行命令（Mac 终端示例）
cd ~/engine
# 1. 保存骨架代码
cat > search_engine.py << 'PYEOF'
# [粘贴上方 Python 骨架代码]
PYEOF

# 2. 写 demo 测试
python3 -c "
from search_engine import KeywordSearchEngine
eng = KeywordSearchEngine()
eng.add_document('doc1', '三色审计系统核心算法')
eng.add_document('doc2', '搜索关键字算法 BM25 倒排索引')
eng.add_document('doc3', '五行计算器 Python 脚本零依赖')
print(eng.search('算法'))
print(eng.autocomplete('b'))
"
```

---

## 第五步 🔄 复盘（复盘结果 · 进化）

**负责角色：** 审计角色 + 全局观察角色

> ⚠️ **复盘必须过三色审计才能出结论**

### 复盘模板（每次执行完填一次）

| 复盘维度 | 问题 | 填写内容 | 三色 |
| --- | --- | --- | --- |
| ✅ 完成了什么 | 本次执行了哪些 Phase？产出了什么？ | （执行后填写） | — |
| ❌ 没完成什么 | 哪些 Phase 没跑通？卡在哪里？ | （执行后填写） | — |
| 🔴 踩了什么坑 | 报错/漏洞/计划偏差 | （执行后填写） | — |
| 📈 下次怎么改 | 算法参数/集成方式/文档结构 | （执行后填写） | — |
| 🧬 DNA 沉淀 | 本次产出的追溯码 | （执行后填写） | — |

### 复盘三色审计框架

**复盘过审条件（三项全满足才 🟢）：**

1. ✅ 每个 Phase 都有明确完成/未完成状态
2. ✅ 所有报错有根因分析 · 不能只写“已修复”
3. ✅ 下次改进方案具体可执行 · 不能是空话

**未满足 → 🟡 补完再审 → 满足 → 🟢 沉淀到知识库**

---

## 五步总结

```
看 → 整理 → 计划(审计) → 执行 → 复盘(审计)
```

**搜索算法接入七维技术轴的核心价值：**

- 🔍 **知识库检索**：把全库文档喂进倒排索引 → 随时能“搜”到任何页面
- 📡 **指令触发匹配**：Trie 前缀树 → 输入前两个字自动补全指令词
- 🎯 **三色审计加速**：BM25 排名 → 审计结果按相关性排序，最相关的先看

这不是多余的技术，是七维系统“能动起来”的引擎。

---

*来源：易学堂 workspace（Notion 导出），已脱敏处理。删除了 UID、确认码、DNA 追溯码中的个人标识符，并将具体人格代号替换为通用角色名称。*
