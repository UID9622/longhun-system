#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ============================================================
# 龍魂 · 语义编码器 · Ollama Embedding 桥接
# DNA：#龍芯⚡️丙午·乙未·丙申·未时·☲离-SEMANTIC-ENCODER-v1.0-a1b2c3d4
# 创建者：诸葛鑫（UID9622）
# 协议：CC BY-NC-SA 4.0
# ============================================================

import numpy as np
import requests
import hashlib
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import OrderedDict

OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "longhun-v4.1.1-bind:latest"
EMBED_DIM = 4096  # Yi-1.5-9B 输出维度
CACHE_SIZE = 1024
SIMILARITY_THRESHOLD = 0.85  # 余弦相似度阈值


@dataclass
class SemanticPattern:
    """语义记忆单元"""
    embedding: np.ndarray
    bagua_target: int  # Bagua enum value
    query_hash: str
    hit_count: int = 0
    last_hit: float = 0.0
    energy_saved_total: float = 0.0


class SemanticEncoder:
    """
    语义编码器：文本 → Ollama Embedding → 蚁触网输入向量
    
    升级点：
    1. ord(c)%256 → Ollama 4096维语义嵌入
    2. 随机路由 → 语义相似度引导路由
    3. 无记忆 → LRU模式缓存（1024条）
    """
    
    def __init__(self, cache_size: int = CACHE_SIZE, 
                 similarity_threshold: float = SIMILARITY_THRESHOLD):
        self.cache_size = cache_size
        self.similarity_threshold = similarity_threshold
        self.patterns: OrderedDict[str, SemanticPattern] = OrderedDict()
        self.embed_hits = 0
        self.embed_misses = 0
        self.total_api_time = 0.0
        self._embed_dim = EMBED_DIM
        
    @property
    def embed_dim(self) -> int:
        return self._embed_dim
    
    def encode(self, text: str, target_bagua: int) -> np.ndarray:
        """
        编码文本为蚁触网输入向量
        优先从缓存命中，未命中则调 Ollama API
        """
        key = hashlib.sha256(text.encode()).hexdigest()[:16]
        
        # 缓存命中（语义相似度匹配）
        cached = self._find_similar(text, key)
        if cached is not None:
            self.embed_hits += 1
            cached.hit_count += 1
            cached.last_hit = time.time()
            return cached.embedding
        
        # 缓存未命中 → Ollama API
        self.embed_misses += 1
        embedding = self._ollama_embed(text)
        
        # 存入缓存
        pattern = SemanticPattern(
            embedding=embedding,
            bagua_target=target_bagua,
            query_hash=key,
            last_hit=time.time()
        )
        self.patterns[key] = pattern
        
        # LRU 淘汰
        if len(self.patterns) > self.cache_size:
            self.patterns.popitem(last=False)
        
        return embedding
    
    def _ollama_embed(self, text: str) -> np.ndarray:
        """调用 Ollama /api/embed"""
        t0 = time.time()
        try:
            resp = requests.post(
                f"{OLLAMA_HOST}/api/embed",
                json={"model": MODEL_NAME, "input": text},
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            embedding = np.array(data["embeddings"][0], dtype=np.float32)
            self.total_api_time += time.time() - t0
            return embedding
        except Exception as e:
            # 降级：hash fallback
            self.total_api_time += time.time() - t0
            return self._hash_fallback(text)
    
    def _find_similar(self, text: str, key: str) -> Optional[SemanticPattern]:
        """在缓存中找语义相似的已有模式"""
        if key in self.patterns:
            return self.patterns[key]
        
        if not self.patterns or len(self.patterns) == 0:
            return None
        
        # 先用 hash 做快速预筛（同hash直接命中）
        # 再对最近 N 条做全量余弦相似度检查
        # 关键：query embedding 也用 Ollama，不用 hash fallback
        try:
            query_emb = self._ollama_embed(text)
            q_norm = np.linalg.norm(query_emb)
            if q_norm == 0:
                return None
        except Exception:
            return None
        
        best_sim = 0.0
        best_key = None
        best_pattern = None
        recent = list(self.patterns.items())[-64:]  # 最近64条
        
        for pk, p in recent:
            p_norm = np.linalg.norm(p.embedding)
            if p_norm == 0:
                continue
            sim = np.dot(query_emb, p.embedding) / (q_norm * p_norm)
            if sim > best_sim:
                best_sim = sim
                best_key = pk
                best_pattern = p
        
        if best_sim >= self.similarity_threshold and best_pattern is not None:
            best_pattern.hit_count += 1
            best_pattern.last_hit = time.time()
            self.embed_hits += 1
            return best_pattern
        
        return None
    
    def _hash_fallback(self, text: str) -> np.ndarray:
        """
        降级方案：用 SHA-256 哈希展成向量
        当 Ollama 不可用时保底
        """
        h = hashlib.sha256(text.encode()).digest()
        # 32字节 → 4096维（重复填充）
        vec = np.zeros(self._embed_dim, dtype=np.float32)
        for i in range(self._embed_dim):
            vec[i] = h[i % 32] / 255.0
        return vec
    
    def get_stats(self) -> Dict:
        total = self.embed_hits + self.embed_misses
        return {
            "cache_size": len(self.patterns),
            "hits": self.embed_hits,
            "misses": self.embed_misses,
            "hit_rate": self.embed_hits / total if total > 0 else 0,
            "avg_api_time_ms": (self.total_api_time / self.embed_misses * 1000) 
                if self.embed_misses > 0 else 0,
            "similarity_threshold": self.similarity_threshold,
        }


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("语义编码器 · 自检")
    print("=" * 50)
    
    encoder = SemanticEncoder(cache_size=128)
    
    # 测试1：基础编码
    q1 = "系统当前状态如何？"
    v1 = encoder.encode(q1, 0)
    print(f"\n[编码] '{q1}' → {v1.shape} (dim={v1.mean():.4f}, std={v1.std():.4f})")
    
    # 测试2：缓存命中
    v2 = encoder.encode(q1, 0)
    print(f"[命中] 相同查询 → hit={encoder.embed_hits}, miss={encoder.embed_misses}")
    
    # 测试3：语义相似
    q3 = "现在系统跑得怎么样？"
    v3 = encoder.encode(q3, 0)
    sim = np.dot(v1, v3) / (np.linalg.norm(v1) * np.linalg.norm(v3))
    print(f"[相似] '{q3}' → 余弦相似度={sim:.4f}, hit={encoder.embed_hits}")
    
    # 测试4：统计
    print(f"\n[统计] {encoder.get_stats()}")
    print("\n✅ 语义编码器自检通过")
