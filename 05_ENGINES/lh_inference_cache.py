#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂系统 · 推理缓存引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丙申·酉时·☰乾-INFERENCE-CACHE-v1.0-c8d4e2f1
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
补全: DL架构§11.10 推理缓存策略·高频查询去重·语义相似度匹配

功能:
  1. 精确缓存 - 完全相同的query直接返回缓存
  2. 语义缓存 - 相似度>0.85的query推测复用
  3. TTL策略 - 知识型长TTL(24h)·对话型短TTL(5min)
  4. LRU淘汰 - 内存上限自动淘汰最不常用条目
  5. 统计监控 - 命中率·节省token数·缓存大小
  6. 持久化 - SQLite落盘·重启不丢

架构:
  Query → 精确匹配 → 语义匹配(可选) → 模型推理 → 写入缓存 → 返回
"""

import os
import sys
import json
import time
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Tuple, List
from dataclasses import dataclass, field
from collections import OrderedDict

# ═══ 配置 ═══
BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DB = BASE_DIR / "data" / "inference_cache.db"
CACHE_DIR = Path.home() / ".longhun" / "cache"
MAX_MEMORY_ENTRIES = 1000      # 内存缓存上限
MAX_DB_ENTRIES = 10000         # 数据库缓存上限
KNOWLEDGE_TTL = 86400          # 知识型查询: 24小时
DIALOG_TTL = 300               # 对话型查询: 5分钟
SEMANTIC_THRESHOLD = 0.85      # 语义匹配阈值
EMBEDDING_DIM = 768            # 嵌入向量维度

# ═══ 数据模型 ═══
@dataclass
class CacheEntry:
    query: str
    response: str
    query_hash: str
    response_hash: str
    embedding: Optional[List[float]] = None
    category: str = "general"     # knowledge | dialog | creative | audit
    ttl: int = KNOWLEDGE_TTL
    created_at: float = field(default_factory=time.time)
    hit_count: int = 0
    tokens_saved: int = 0
    dna: str = ""

# ═══ 数据库初始化 ═══
def init_db():
    CACHE_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(CACHE_DB))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_hash TEXT UNIQUE NOT NULL,
            query TEXT NOT NULL,
            response TEXT NOT NULL,
            response_hash TEXT,
            category TEXT DEFAULT 'general',
            embedding BLOB,
            ttl INTEGER DEFAULT 86400,
            created_at REAL NOT NULL,
            hit_count INTEGER DEFAULT 0,
            tokens_saved INTEGER DEFAULT 0,
            dna TEXT DEFAULT ''
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_query_hash ON cache(query_hash)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON cache(category)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_created ON cache(created_at)")
    conn.commit()
    return conn

# ═══ 核心引擎 ═══
class InferenceCache:
    def __init__(self, enable_semantic: bool = True, max_memory: int = MAX_MEMORY_ENTRIES):
        self.conn = init_db()
        self.enable_semantic = enable_semantic
        self.max_memory = max_memory
        self.memory = OrderedDict()  # query_hash → CacheEntry (LRU)
        self.stats = {
            "hits": 0, "misses": 0, "semantic_hits": 0,
            "tokens_saved": 0, "total_queries": 0,
            "started_at": time.time(),
        }
        self.dna = "#龍芯⚡️{}-INFERENCE-CACHE-v1.0-{}".format(
            datetime.now().strftime("%Y-%m-%d"),
            hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        )
        self._load_recent()
    
    def _hash(self, text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()[:16]
    
    def _load_recent(self):
        """启动时加载最近使用的缓存到内存"""
        cursor = self.conn.execute(
            "SELECT query_hash, query, response, response_hash, category, embedding, ttl, created_at, hit_count, tokens_saved, dna "
            "FROM cache ORDER BY hit_count DESC LIMIT ?",
            (self.max_memory,)
        )
        for row in cursor:
            entry = CacheEntry(
                query=row[1], response=row[2], query_hash=row[0],
                response_hash=row[3], category=row[4],
                embedding=json.loads(row[5]) if row[5] else None,
                ttl=row[6], created_at=row[7], hit_count=row[8],
                tokens_saved=row[9], dna=row[10],
            )
            self.memory[entry.query_hash] = entry
    
    def get(self, query: str, category: str = "general") -> Optional[Tuple[str, dict]]:
        """
        查询缓存
        返回: (response, metadata) 或 None
        """
        self.stats["total_queries"] += 1
        qhash = self._hash(query)
        
        # 1. 精确匹配（内存）
        if qhash in self.memory:
            entry = self.memory[qhash]
            if not self._is_expired(entry):
                self._hit(entry)
                self.stats["hits"] += 1
                return entry.response, self._meta(entry, "exact")
            else:
                self._evict(entry)
        
        # 2. 精确匹配（数据库）
        cursor = self.conn.execute(
            "SELECT query,response,response_hash,category,embedding,ttl,created_at,hit_count,tokens_saved,dna FROM cache WHERE query_hash=?",
            (qhash,)
        )
        row = cursor.fetchone()
        if row:
            entry = CacheEntry(
                query=row[0], response=row[1], query_hash=qhash,
                response_hash=row[2], category=row[3],
                embedding=json.loads(row[4]) if row[4] else None,
                ttl=row[5], created_at=row[6], hit_count=row[7],
                tokens_saved=row[8], dna=row[9],
            )
            if not self._is_expired(entry):
                self._hit(entry)
                self.stats["hits"] += 1
                return entry.response, self._meta(entry, "exact_db")
            else:
                self._evict(entry)
        
        # 3. 语义匹配（可选）
        if self.enable_semantic:
            result = self._semantic_match(query, category)
            if result:
                entry, score = result
                self._hit(entry)
                self.stats["semantic_hits"] += 1
                meta = self._meta(entry, f"semantic({score:.2f})")
                meta["semantic_score"] = score
                return entry.response, meta
        
        self.stats["misses"] += 1
        return None
    
    def set(self, query: str, response: str, category: str = "general",
            embedding: Optional[List[float]] = None, ttl: Optional[int] = None):
        """
        写入缓存
        """
        qhash = self._hash(query)
        rhash = self._hash(response)
        tokens = max(len(response) // 4, 1)  # 粗略估算token数
        
        if ttl is None:
            ttl = KNOWLEDGE_TTL if category in ("knowledge", "audit", "code") else DIALOG_TTL
        
        entry = CacheEntry(
            query=query, response=response, query_hash=qhash,
            response_hash=rhash, embedding=embedding,
            category=category, ttl=ttl,
            tokens_saved=tokens, dna=self.dna,
        )
        
        # 写入数据库
        embedding_blob = json.dumps(embedding) if embedding else None
        self.conn.execute(
            """INSERT OR REPLACE INTO cache 
               (query_hash, query, response, response_hash, category, embedding, ttl, created_at, hit_count, tokens_saved, dna)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (qhash, query, response, rhash, category, embedding_blob, ttl, entry.created_at, 0, tokens, self.dna)
        )
        self.conn.commit()
        
        # 写入内存（LRU淘汰）
        self.memory[qhash] = entry
        self.memory.move_to_end(qhash)
        
        if len(self.memory) > self.max_memory:
            self.memory.popitem(last=False)
        
        # 定期清理
        if self.stats["total_queries"] % 100 == 0:
            self._purge_expired()
    
    def _hit(self, entry: CacheEntry):
        """记录命中"""
        entry.hit_count += 1
        self.stats["tokens_saved"] += entry.tokens_saved
        
        self.conn.execute(
            "UPDATE cache SET hit_count=hit_count+1 WHERE query_hash=?",
            (entry.query_hash,)
        )
        self.conn.commit()
        
        if entry.query_hash in self.memory:
            self.memory.move_to_end(entry.query_hash)
    
    def _evict(self, entry: CacheEntry):
        """淘汰过期条目"""
        if entry.query_hash in self.memory:
            del self.memory[entry.query_hash]
        self.conn.execute("DELETE FROM cache WHERE query_hash=?", (entry.query_hash,))
        self.conn.commit()
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        return (time.time() - entry.created_at) > entry.ttl
    
    def _semantic_match(self, query: str, category: str) -> Optional[Tuple[CacheEntry, float]]:
        """
        语义匹配 - 简化版使用关键词Jaccard相似度
        完整版接入embedding模型（Ollama/chroma）
        """
        query_words = set(query.lower().split())
        if len(query_words) < 3:
            return None
        
        best_entry = None
        best_score = 0.0
        
        # 只检查同category的缓存
        candidates = [e for e in self.memory.values() if e.category == category]
        if len(candidates) < 2:
            candidates = list(self.memory.values())[:20]  # 放宽到全部
        
        for entry in candidates:
            if self._is_expired(entry):
                continue
            entry_words = set(entry.query.lower().split())
            if not entry_words:
                continue
            
            intersection = query_words & entry_words
            union = query_words | entry_words
            score = len(intersection) / len(union) if union else 0
            
            if score > best_score:
                best_score = score
                best_entry = entry
        
        if best_entry and best_score >= SEMANTIC_THRESHOLD:
            return best_entry, best_score
        return None
    
    def _meta(self, entry: CacheEntry, hit_type: str) -> dict:
        return {
            "hit_type": hit_type,
            "cached_at": datetime.fromtimestamp(entry.created_at).isoformat(),
            "hit_count": entry.hit_count,
            "tokens_saved": entry.tokens_saved,
            "dna": entry.dna,
        }
    
    def _purge_expired(self):
        """清理过期条目"""
        now = time.time()
        expired = [
            h for h, e in self.memory.items()
            if (now - e.created_at) > e.ttl
        ]
        for h in expired:
            del self.memory[h]
        
        self.conn.execute(
            "DELETE FROM cache WHERE (created_at + ttl) < ?",
            (now,)
        )
        self.conn.commit()
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        total = self.stats["hits"] + self.stats["misses"]
        return {
            **self.stats,
            "hit_rate": f"{self.stats['hits']/max(total,1)*100:.1f}%",
            "semantic_hit_rate": f"{self.stats['semantic_hits']/max(total,1)*100:.1f}%",
            "memory_entries": len(self.memory),
            "uptime_hours": f"{(time.time()-self.stats['started_at'])/3600:.1f}",
            "total_tokens_saved": self.stats["tokens_saved"],
        }
    
    def clear(self, category: Optional[str] = None):
        """清空缓存"""
        if category:
            self.conn.execute("DELETE FROM cache WHERE category=?", (category,))
            self.memory = OrderedDict(
                (h, e) for h, e in self.memory.items() if e.category != category
            )
        else:
            self.conn.execute("DELETE FROM cache")
            self.memory.clear()
        self.conn.commit()
    
    def close(self):
        self.conn.close()

# ═══ 装饰器 ═══
def cached(category: str = "general", ttl: Optional[int] = None):
    """推理缓存装饰器"""
    def decorator(func):
        cache = InferenceCache()
        def wrapper(*args, **kwargs):
            # 从参数构造query
            query_parts = []
            for a in args:
                if isinstance(a, str):
                    query_parts.append(a)
            for k, v in sorted(kwargs.items()):
                query_parts.append(f"{k}={v}")
            query = " | ".join(query_parts)
            
            # 查缓存
            result = cache.get(query, category)
            if result:
                return result[0]
            
            # 执行推理
            response = func(*args, **kwargs)
            cache.set(query, response, category=category, ttl=ttl)
            return response
        return wrapper
    return decorator

# ═══ CLI ═══
def main():
    if len(sys.argv) < 2:
        print("🐉 推理缓存引擎 CLI")
        print("  python3 engines/lh_inference_cache.py stats   查看统计")
        print("  python3 engines/lh_inference_cache.py clear   清空缓存")
        print("  python3 engines/lh_inference_cache.py list    列出前20条")
        return
    
    cache = InferenceCache()
    cmd = sys.argv[1]
    
    if cmd == "stats":
        stats = cache.get_stats()
        print("\n🐉 缓存统计")
        print("─" * 40)
        for k, v in stats.items():
            print(f"  {k}: {v}")
    
    elif cmd == "clear":
        cat = sys.argv[2] if len(sys.argv) > 2 else None
        cache.clear(cat)
        print(f"✅ 已清空缓存{' (category='+cat+')' if cat else ''}")
    
    elif cmd == "list":
        print("\n🐉 缓存条目 (最近20条)")
        print("─" * 80)
        for h, e in list(cache.memory.items())[:20]:
            age = time.time() - e.created_at
            print(f"  {e.query_hash[:8]} | {e.category:<12} | 命中{e.hit_count:>3} | {age:.0f}s前")
    
    cache.close()

if __name__ == "__main__":
    main()
