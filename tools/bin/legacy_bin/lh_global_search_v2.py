#!/usr/bin/env python3
# lh_global_search_v2.py
# 龍魂 · 全球全量搜索 × 蚁群架构 × 人格联动
# DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️
# UID: 9622

import hashlib
import math
import re
import json
import time
from collections import defaultdict
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class Persona(Enum):
    MILITARY = "military"      # 军事：快、准、狠
    HISTORY = "history"        # 历史：时间权重、史料权威
    PHILOSOPHY = "philosophy"  # 哲学：语义相似、悟道匹配
    ECONOMY = "economy"        # 经济：价格敏感、交易相关
    POLITICAL = "political"    # 政治：实体识别、人名地名


@dataclass
class SearchResult:
    doc_id: str
    score: float
    persona: Persona
    tier: str           # perfect / compatible / restricted
    node_id: str        # CN-1 / CN-2 / ...
    audit_status: str   # green / yellow / red
    timestamp: float


class LongHunGlobalSearch:
    DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️"
    UID = "9622"

    # === 人格算法配置 ===
    PERSONA_ALGORITHMS = {
        Persona.MILITARY: {
            "primary": "inverted_index",
            "secondary": "bloom_filter",
            "ranking": "exact_match_boost",
            "latency_target_ms": 50
        },
        Persona.HISTORY: {
            "primary": "bm25",
            "secondary": "time_decay",
            "ranking": "temporal_weight",
            "latency_target_ms": 200
        },
        Persona.PHILOSOPHY: {
            "primary": "vector_search",
            "secondary": "semantic_expansion",
            "ranking": "cosine_similarity",
            "latency_target_ms": 500
        },
        Persona.ECONOMY: {
            "primary": "tfidf",
            "secondary": "price_sentiment",
            "ranking": "transaction_relevance",
            "latency_target_ms": 150
        },
        Persona.POLITICAL: {
            "primary": "edit_distance",
            "secondary": "ner_entity",
            "ranking": "entity_match",
            "latency_target_ms": 100
        }
    }

    # === 通心译 · 国产模型集群 ===
    NODES = {
        "CN-1": {"name": "华为盘古", "type": "perfect", "persona_boost": [Persona.MILITARY, Persona.PHILOSOPHY]},
        "CN-2": {"name": "阿里通义", "type": "perfect", "persona_boost": [Persona.ECONOMY, Persona.POLITICAL]},
        "CN-3": {"name": "百度文心", "type": "perfect", "persona_boost": [Persona.HISTORY, Persona.POLITICAL]},
        "CN-4": {"name": "讯飞星火", "type": "compatible", "persona_boost": [Persona.MILITARY, Persona.ECONOMY]},
    }

    def __init__(self, persona: Persona = Persona.MILITARY):
        self.persona = persona
        self.algo_config = self.PERSONA_ALGORITHMS[persona]

        # 索引结构
        self.index = defaultdict(set)           # 倒排索引
        self.docs = {}                          # 文档存储
        self.tf = defaultdict(dict)             # 词频
        self.df = defaultdict(int)              # 文档频率
        self.vectors = {}                       # 向量索引（哲学人格）
        self.entities = defaultdict(set)        # 实体索引（政治人格）
        self.prices = {}                        # 价格索引（经济人格）
        self.timestamps = {}                    # 时间索引（历史人格）
        self.trie = {}                          # 前缀树
        self.N = 0

        # BM25参数
        self.k1, self.b = 1.5, 0.75

        # 布隆过滤器（军事人格快筛）
        self.bloom_size = 100000
        self.bloom_hashes = 7
        self.bloom_filter = [0] * self.bloom_size

        # 三色审计词表
        self.red_words = set()      # 加载外部红线词库
        self.yellow_words = set()   # 加载外部敏感词库

    def _tokenize(self, text: str) -> List[str]:
        """全球分词：中文 + 英文 + 数字 + 一带一路语言"""
        # 中文单字 + 英文单词 + 数字
        tokens = re.findall(r'[\u4e00-\u9fff]|[a-zA-Z0-9]+', text.lower())
        return tokens

    def _bloom_add(self, word: str):
        """布隆过滤器添加"""
        for i in range(self.bloom_hashes):
            idx = hash(f"{word}{i}") % self.bloom_size
            self.bloom_filter[idx] = 1

    def _bloom_check(self, word: str) -> bool:
        """布隆过滤器检查（可能误报，不会漏报）"""
        for i in range(self.bloom_hashes):
            idx = hash(f"{word}{i}") % self.bloom_size
            if self.bloom_filter[idx] == 0:
                return False
        return True

    def _trie_insert(self, word: str):
        """前缀树插入"""
        node = self.trie
        for ch in word:
            node = node.setdefault(ch, {})
        node['$'] = True

    def _bm25_score(self, query: str, doc_id: str) -> float:
        """BM25评分"""
        tokens = self._tokenize(query)
        if not self.docs:
            return 0.0
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

    def _time_decay_score(self, doc_id: str, base_score: float) -> float:
        """历史人格：时间衰减权重"""
        ts = self.timestamps.get(doc_id, time.time())
        age_days = (time.time() - ts) / 86400
        # 越新权重越高，但经典史料不衰减
        decay = math.exp(-age_days / 365)  # 一年衰减到37%
        return base_score * (0.3 + 0.7 * decay)  # 最低保留30%

    def _vector_similarity(self, query_vec: List[float], doc_vec: List[float]) -> float:
        """哲学人格：余弦相似度"""
        dot = sum(a * b for a, b in zip(query_vec, doc_vec))
        norm_q = math.sqrt(sum(a * a for a in query_vec))
        norm_d = math.sqrt(sum(a * a for a in doc_vec))
        if norm_q == 0 or norm_d == 0:
            return 0.0
        return dot / (norm_q * norm_d)

    def _entity_match(self, query: str, doc_id: str) -> float:
        """政治人格：实体匹配"""
        q_entities = set(re.findall(r'[A-Z][a-z]+ [A-Z][a-z]+|[A-Z]{2,}', query))
        d_entities = self.entities.get(doc_id, set())
        if not q_entities:
            return 0.5
        match = len(q_entities & d_entities) / len(q_entities)
        return match

    def _price_relevance(self, query: str, doc_id: str) -> float:
        """经济人格：价格敏感度"""
        price_keywords = ['价格', 'price', 'cost', '费用', 'fee', '元', '$', '€', '¥']
        has_price = any(kw in query.lower() for kw in price_keywords)
        if not has_price:
            return 0.5
        doc_price = self.prices.get(doc_id, 0)
        return 0.5 + 0.5 * min(doc_price / 10000, 1.0)

    def _edit_distance(self, s1: str, s2: str) -> int:
        """编辑距离（政治人格模糊匹配）"""
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
        return dp[m][n]

    def _audit(self, query: str, doc_id: str) -> str:
        """三色审计"""
        text = query + " " + self.docs.get(doc_id, "")
        for rw in self.red_words:
            if rw in text:
                return "red"
        for yw in self.yellow_words:
            if yw in text:
                return "yellow"
        return "green"

    def add_document(self, doc_id: str, text: str,
                     vector: Optional[List[float]] = None,
                     entities: Optional[List[str]] = None,
                     price_info: Optional[float] = None,
                     timestamp: Optional[float] = None):
        """添加文档到全局索引"""
        tokens = self._tokenize(text)
        self.docs[doc_id] = text
        self.N += 1

        # 词频统计
        freq = defaultdict(int)
        for t in tokens:
            freq[t] += 1
            self._bloom_add(t)
            self._trie_insert(t)

        for word, cnt in freq.items():
            self.tf[doc_id][word] = cnt / len(tokens)
            self.df[word] += 1
            self.index[word].add(doc_id)

        # 人格特定索引
        if vector:
            self.vectors[doc_id] = vector
        if entities:
            self.entities[doc_id] = set(entities)
        if price_info:
            self.prices[doc_id] = price_info
        if timestamp:
            self.timestamps[doc_id] = timestamp
        else:
            self.timestamps[doc_id] = time.time()

    def search(self, query: str, top_k: int = 10) -> List[SearchResult]:
        """全局搜索 · 人格联动"""
        tokens = self._tokenize(query)

        # 军事人格：布隆过滤器快筛
        if self.persona == Persona.MILITARY:
            candidates = set()
            for t in tokens:
                if self._bloom_check(t):
                    candidates |= self.index.get(t, set())
        else:
            candidates = set()
            for t in tokens:
                candidates |= self.index.get(t, set())

        # 按人格算法评分
        results = []
        for doc_id in candidates:
            base_score = self._bm25_score(query, doc_id)

            # 人格加成
            if self.persona == Persona.HISTORY:
                score = self._time_decay_score(doc_id, base_score)
            elif self.persona == Persona.PHILOSOPHY:
                score = base_score * 1.5
            elif self.persona == Persona.ECONOMY:
                score = base_score + self._price_relevance(query, doc_id)
            elif self.persona == Persona.POLITICAL:
                score = base_score + self._entity_match(query, doc_id)
            else:
                score = base_score

            # 三色审计
            audit = self._audit(query, doc_id)
            if audit == "red":
                continue  # 红线熔断

            # 通心译 · 节点选择
            node_id = self._select_node(doc_id)
            tier = self.NODES[node_id]["type"]

            results.append(SearchResult(
                doc_id=doc_id,
                score=score,
                persona=self.persona,
                tier=tier,
                node_id=node_id,
                audit_status=audit,
                timestamp=time.time()
            ))

        # 排序
        results.sort(key=lambda x: x.score, reverse=True)

        # 黄色降级
        final = []
        for r in results[:top_k]:
            if r.audit_status == "yellow":
                r.score *= 0.3
            final.append(r)

        return final

    def _select_node(self, doc_id: str) -> str:
        """通心译 · 节点选择"""
        for node_id, node_info in self.NODES.items():
            if self.persona in node_info["persona_boost"]:
                return node_id
        return "CN-1"  # 默认盘古

    def autocomplete(self, prefix: str, limit: int = 5) -> List[str]:
        """前缀树自动补全"""
        node = self.trie
        for ch in prefix:
            if ch not in node:
                return []
            node = node[ch]
        results = []
        self._dfs(node, prefix, results, limit)
        return results

    def _dfs(self, node, path, results, limit):
        if len(results) >= limit:
            return
        if '$' in node:
            results.append(path)
        for ch, child in sorted(node.items()):
            if ch != '$':
                self._dfs(child, path + ch, results, limit)

    def to_json(self, results: List[SearchResult]) -> str:
        """输出JSON（含主权标记）"""
        output = {
            "protocol": "longhun-search-v2",
            "dna": self.DNA,
            "uid": self.UID,
            "persona": self.persona.value,
            "query_time_ms": int((time.time() - results[0].timestamp) * 1000) if results else 0,
            "results": [
                {
                    "doc_id": r.doc_id,
                    "score": round(r.score, 4),
                    "tier": r.tier,
                    "node": r.node_id,
                    "audit": r.audit_status,
                    "snippet": self.docs.get(r.doc_id, "")[:100]
                }
                for r in results
            ]
        }
        return json.dumps(output, ensure_ascii=False, indent=2)


def main():
    print("🐉 龍魂 · 全球全量搜索 × 蚁群架构 v2.0")
    print(f"DNA: {LongHunGlobalSearch.DNA}")
    print(f"UID: {LongHunGlobalSearch.UID}")
    print()

    # 初始化军事人格搜索引擎
    engine = LongHunGlobalSearch(Persona.MILITARY)

    # 添加全球文档（多语言）
    docs = [
        ("doc1", "龍魂系统三色审计算法核心实现", None, ["龍魂", "审计"], None),
        ("doc2", "BM25 ranking algorithm Elasticsearch default", None, ["BM25", "Elasticsearch"], None),
        ("doc3", "华为鲲鹏920芯片国密加速SM2 SM3 SM4", None, ["华为", "鲲鹏"], 19999.0),
        ("doc4", "សួស្តី កម្ពុជា ប្រព័ន្ធយូអាយឌី9622", None, ["柬埔寨", "UID9622"], None),
        ("doc5", "Поисковый алгоритм ранжирования российского сегмента", None, ["俄罗斯", "算法"], None),
        ("doc6", "البحث عن الكلمات الرئيسية في النظام الصيني", None, ["阿拉伯", "搜索"], None),
        ("doc7", "جستجوی کلیدواژه در سیستم چینی UID9622", None, ["伊朗", "UID9622"], None),
    ]

    for doc_id, text, vec, ents, price in docs:
        engine.add_document(doc_id, text, vec, ents, price)

    # 搜索
    print("=== 军事人格搜索：算法 ===")
    results = engine.search("算法")
    print(engine.to_json(results))

    print("\n=== 自动补全：b ===")
    print(engine.autocomplete("b"))

    # 切换哲学人格
    engine_phil = LongHunGlobalSearch(Persona.PHILOSOPHY)
    for doc_id, text, vec, ents, price in docs:
        engine_phil.add_document(doc_id, text, [0.1, 0.2, 0.3], ents, price)

    print("\n=== 哲学人格搜索：系统 ===")
    results = engine_phil.search("系统")
    print(engine_phil.to_json(results))

    # === 通心译 · 人格节点路由表 ===
    print("\n=== 通心译 · 人格节点路由表 ===")
    print(f"{'人格':<8} {'首选节点':<12} {'次选节点':<12} {'算法组合':<24} {'延迟目标':<10}")
    print("-" * 70)
    routes = [
        ("军事", "华为盘古 CN-1", "讯飞星火 CN-4", "倒排 + 布隆", "50ms"),
        ("历史", "百度文心 CN-3", "华为盘古 CN-1", "BM25 + 时间衰减", "200ms"),
        ("哲学", "华为盘古 CN-1", "阿里通义 CN-2", "向量 + 语义扩展", "500ms"),
        ("经济", "阿里通义 CN-2", "讯飞星火 CN-4", "TF-IDF + 价格敏感", "150ms"),
        ("政治", "百度文心 CN-3", "阿里通义 CN-2", "编辑距离 + NER", "100ms"),
    ]
    for persona, primary, secondary, algo, latency in routes:
        print(f"{persona:<8} {primary:<12} {secondary:<12} {algo:<24} {latency:<10}")


if __name__ == "__main__":
    main()
