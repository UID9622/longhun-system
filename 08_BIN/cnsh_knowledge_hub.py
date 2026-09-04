#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🧠 CNSH 知识库中枢 (Knowledge Hub) v1.0

DNA: #龍芯⚡️丙午·丙酉·癸亥·巳时·䷫姤-CNSH-KNOWLEDGE-HUB-v1.0-UID9622

功能:
  - 本地 SQLite + FTS5 全文检索
  - 词频余弦相似度做轻量语义检索
  - DNA 追溯每条记忆
  - 与行为密码学指纹联动
  - 零依赖，纯 Python 标准库

设计原则:
  1. 本地优先：数据主权在本地/私有服务器
  2. 追加不覆盖：旧版本永久保留
  3. 可审计：每条记录带 DNA + 时间戳 + 来源
"""

import os
import re
import json
import hashlib
import sqlite3
import math
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict

# 尝试导入行为密码学；不存在则回退
_BC = None
try:
    sys_path = __import__("sys").path
    sys_path.insert(0, str(Path(__file__).resolve().parent.parent / "04_ENGINES" / "behavioral_crypto"))
    import seven_factor_model as _BC
except Exception:
    _BC = None


UID = "9622"
DNA_PREFIX = "#龍芯⚡️"
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
EMBEDDING_MODEL = os.environ.get("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text:latest")


def generate_dna(suffix: str = "") -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    rand = hashlib.sha256(f"{suffix}{timestamp}{UID}".encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{timestamp}-{suffix}-{rand}-{UID}"


def content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


@dataclass
class MemoryEntry:
    entry_id: str
    dna: str
    content_hash: str
    content: str
    category: str
    tags: List[str]
    source: str
    created_at: str
    updated_at: str
    bcm_fingerprint: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    embedding: Optional[List[float]] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["tags"] = json.dumps(self.tags, ensure_ascii=False)
        if self.metadata:
            d["metadata"] = json.dumps(self.metadata, ensure_ascii=False)
        return d


class KnowledgeHub:
    """知识库中枢：存储 + 检索"""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_dir = Path.home() / ".cnsh"
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(db_dir / "knowledge_hub.db")
        self.db_path = db_path
        self._init_db()

    def _check_embedding_model(self) -> bool:
        """检查 Ollama 中是否存在 embedding 模型"""
        try:
            req = urllib.request.Request(
                f"{OLLAMA_BASE_URL}/api/tags",
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m.get("name", "") for m in data.get("models", [])]
                return any(EMBEDDING_MODEL.split(":")[0] in m for m in models)
        except Exception:
            return False

    def _get_embedding(self, text: str) -> Optional[List[float]]:
        """调用本地 Ollama 生成向量，失败返回 None"""
        if not self._check_embedding_model():
            return None
        try:
            payload = json.dumps({
                "model": EMBEDDING_MODEL,
                "prompt": text[:2048],
            }).encode("utf-8")
            req = urllib.request.Request(
                f"{OLLAMA_BASE_URL}/api/embeddings",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("embedding")
        except Exception:
            return None

    @staticmethod
    def _cosine_similarity_vec(a: List[float], b: List[float]) -> float:
        if not a or not b or len(a) != len(b):
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS entries (
                    entry_id TEXT PRIMARY KEY,
                    dna TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT DEFAULT 'general',
                    tags TEXT DEFAULT '[]',
                    source TEXT DEFAULT 'unknown',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    bcm_fingerprint TEXT,
                    metadata TEXT DEFAULT '{}',
                    embedding TEXT
                );
                CREATE INDEX IF NOT EXISTS idx_entries_dna ON entries(dna);
                CREATE INDEX IF NOT EXISTS idx_entries_category ON entries(category);
                CREATE INDEX IF NOT EXISTS idx_entries_created ON entries(created_at);

                CREATE VIRTUAL TABLE IF NOT EXISTS entries_fts USING fts5(
                    content,
                    content_rowid=rowid,
                    tokenize='porter unicode61'
                );
            """)
            # Schema 迁移：老数据库没有 embedding 列时自动添加
            try:
                conn.execute("SELECT embedding FROM entries LIMIT 1")
            except sqlite3.OperationalError:
                conn.execute("ALTER TABLE entries ADD COLUMN embedding TEXT")
                print("🧠 已升级数据库：增加 embedding 列")

    def store(
        self,
        content: str,
        category: str = "general",
        tags: Optional[List[str]] = None,
        source: str = "unknown",
        dna: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryEntry:
        """存储一条记忆，返回带 DNA 的条目"""
        tags = tags or []
        metadata = metadata or {}
        entry_id = hashlib.sha256(f"{content}{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        dna = dna or generate_dna(f"KH-{category}")
        now = datetime.now().isoformat()

        # 行为密码学指纹
        bcm_fingerprint = None
        if _BC is not None:
            try:
                fp = _BC.quick_fingerprint({"content": content, "source": source, "uid": UID})
                bcm_fingerprint = fp.get("fingerprint")
            except Exception:
                pass

        # 生成向量（Ollama 本地 embedding，零费用）
        embedding = self._get_embedding(content)

        entry = MemoryEntry(
            entry_id=entry_id,
            dna=dna,
            content_hash=content_hash(content),
            content=content,
            category=category,
            tags=tags,
            source=source,
            created_at=now,
            updated_at=now,
            bcm_fingerprint=bcm_fingerprint,
            metadata=metadata,
            embedding=embedding,
        )

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO entries (entry_id, dna, content_hash, content, category, tags, source,
                                     created_at, updated_at, bcm_fingerprint, metadata, embedding)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entry.entry_id,
                    entry.dna,
                    entry.content_hash,
                    entry.content,
                    entry.category,
                    json.dumps(entry.tags, ensure_ascii=False),
                    entry.source,
                    entry.created_at,
                    entry.updated_at,
                    entry.bcm_fingerprint,
                    json.dumps(entry.metadata, ensure_ascii=False),
                    json.dumps(embedding) if embedding else None,
                ),
            )
            conn.execute(
                "INSERT INTO entries_fts (rowid, content) VALUES (last_insert_rowid(), ?)",
                (entry.content,),
            )
        return entry

    def retrieve(self, entry_id: Optional[str] = None, dna: Optional[str] = None) -> Optional[MemoryEntry]:
        """按 entry_id 或 DNA 检索单条记忆"""
        with sqlite3.connect(self.db_path) as conn:
            if entry_id:
                row = conn.execute(
                    "SELECT * FROM entries WHERE entry_id = ?", (entry_id,)
                ).fetchone()
            elif dna:
                row = conn.execute(
                    "SELECT * FROM entries WHERE dna = ? ORDER BY created_at DESC LIMIT 1", (dna,)
                ).fetchone()
            else:
                return None

            if not row:
                return None
            return self._row_to_entry(row)

    def search(self, query: str, top_k: int = 5, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """全文 + 语义 + 向量混合检索"""
        query_terms = self._tokenize(query)
        query_embedding = self._get_embedding(query)

        candidates = {}
        cols = None
        with sqlite3.connect(self.db_path) as conn:
            cols = [c[1] for c in conn.execute("PRAGMA table_info(entries)").fetchall()]

            # 1) FTS5 英文/数字检索
            try:
                sql = """
                    SELECT e.*, f.rank FROM entries e
                    JOIN (
                        SELECT rowid, rank FROM entries_fts WHERE entries_fts MATCH ?
                    ) f ON e.rowid = f.rowid
                """
                params = [query]
                if category:
                    sql += " AND e.category = ?"
                    params.append(category)
                sql += " ORDER BY f.rank LIMIT ?"
                params.append(top_k * 4)
                for row in conn.execute(sql, params).fetchall():
                    entry = self._row_to_entry(dict(zip(cols, row[:-1])))
                    candidates[entry.entry_id] = {"entry": entry, "fts_rank": row[-1]}
            except Exception:
                pass

            # 2) 中文 LIKE 兜底
            chinese_chars = re.findall(r"[\u4e00-\u9fff]", query)
            if chinese_chars:
                conditions = ["e.content LIKE ?" for _ in chinese_chars]
                params = [f"%{c}%" for c in chinese_chars]
                sql = f"SELECT e.* FROM entries e WHERE ({' OR '.join(conditions)})"
                if category:
                    sql += " AND e.category = ?"
                    params.append(category)
                sql += " LIMIT ?"
                params.append(top_k * 4)
                for row in conn.execute(sql, params).fetchall():
                    entry = self._row_to_entry(dict(zip(cols, row)))
                    if entry.entry_id not in candidates:
                        candidates[entry.entry_id] = {"entry": entry, "fts_rank": 0.0}

            # 3) 向量检索：加载最近有 embedding 的记录，与 query 向量做余弦相似
            if query_embedding:
                try:
                    vec_sql = "SELECT e.* FROM entries e WHERE e.embedding IS NOT NULL"
                    vec_params = []
                    if category:
                        vec_sql += " AND e.category = ?"
                        vec_params.append(category)
                    vec_sql += " ORDER BY e.created_at DESC LIMIT ?"
                    vec_params.append(top_k * 10)
                    for row in conn.execute(vec_sql, vec_params).fetchall():
                        entry = self._row_to_entry(dict(zip(cols, row)))
                        if entry.entry_id not in candidates:
                            candidates[entry.entry_id] = {"entry": entry, "fts_rank": 0.0}
                except Exception:
                    pass

        # 4) 多路相似度融合重排
        scored = []
        for item in candidates.values():
            entry = item["entry"]

            # 词频语义相似度
            text_score = self._cosine_similarity(query_terms, self._tokenize(entry.content))
            tag_score = self._cosine_similarity(query_terms, self._tokenize(" ".join(entry.tags)))
            lexical_score = text_score * 0.7 + tag_score * 0.3

            # 向量相似度
            vector_score = 0.0
            if query_embedding and entry.embedding:
                vector_score = self._cosine_similarity_vec(query_embedding, entry.embedding)

            # 融合：向量权重 0.6，词频权重 0.4
            if query_embedding and entry.embedding:
                final_score = vector_score * 0.6 + lexical_score * 0.4
            else:
                final_score = lexical_score

            scored.append({
                "entry": entry,
                "fts_rank": item["fts_rank"],
                "semantic_score": final_score,
                "vector_score": round(vector_score, 4),
                "lexical_score": round(lexical_score, 4),
            })

        scored.sort(key=lambda x: x["semantic_score"], reverse=True)
        return [
            {
                "entry_id": c["entry"].entry_id,
                "dna": c["entry"].dna,
                "content": c["entry"].content[:500],
                "category": c["entry"].category,
                "tags": c["entry"].tags,
                "source": c["entry"].source,
                "created_at": c["entry"].created_at,
                "bcm_fingerprint": c["entry"].bcm_fingerprint,
                "semantic_score": round(c["semantic_score"], 4),
                "vector_score": c["vector_score"],
                "lexical_score": c["lexical_score"],
            }
            for c in scored[:top_k]
        ]

    def list_categories(self) -> List[str]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT DISTINCT category FROM entries ORDER BY category"
            ).fetchall()
            return [r[0] for r in rows]

    def stats(self) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
            with_vec = conn.execute(
                "SELECT COUNT(*) FROM entries WHERE embedding IS NOT NULL"
            ).fetchone()[0]
            categories = conn.execute(
                "SELECT category, COUNT(*) FROM entries GROUP BY category"
            ).fetchall()
            latest = conn.execute(
                "SELECT created_at FROM entries ORDER BY created_at DESC LIMIT 1"
            ).fetchone()
        return {
            "total_entries": total,
            "entries_with_embedding": with_vec,
            "categories": {c: n for c, n in categories},
            "latest_entry_at": latest[0] if latest else None,
            "db_path": self.db_path,
        }

    def _row_to_entry(self, row) -> MemoryEntry:
        if isinstance(row, sqlite3.Row):
            row = dict(row)
        elif not isinstance(row, dict):
            # tuple from cursor.description
            return None
        emb_raw = row.get("embedding")
        embedding = None
        if emb_raw:
            try:
                embedding = json.loads(emb_raw)
            except Exception:
                embedding = None
        return MemoryEntry(
            entry_id=row["entry_id"],
            dna=row["dna"],
            content_hash=row["content_hash"],
            content=row["content"],
            category=row["category"],
            tags=json.loads(row["tags"]) if row["tags"] else [],
            source=row["source"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            bcm_fingerprint=row.get("bcm_fingerprint"),
            metadata=json.loads(row["metadata"]) if row.get("metadata") else {},
            embedding=embedding,
        )

    def _tokenize(self, text: str) -> Dict[str, int]:
        """简单中文/英文分词 + 词频"""
        text = text.lower()
        # 英文单词
        words = re.findall(r"[a-z0-9_]+", text)
        # 中文字符
        chars = re.findall(r"[\u4e00-\u9fff]", text)
        freq = {}
        for w in words:
            if len(w) > 1:
                freq[w] = freq.get(w, 0) + 1
        for c in chars:
            freq[c] = freq.get(c, 0) + 1
        return freq

    def _cosine_similarity(self, a: Dict[str, int], b: Dict[str, int]) -> float:
        if not a or not b:
            return 0.0
        keys = set(a.keys()) | set(b.keys())
        dot = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
        norm_a = math.sqrt(sum(v * v for v in a.values()))
        norm_b = math.sqrt(sum(v * v for v in b.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)


# ═══════════════════════════════════════════════════════
# CLI 测试
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys

    hub = KnowledgeHub()
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        e1 = hub.store(
            "龍魂系统基于行为密码学实现知行合一，所有创作都带 DNA 追溯。",
            category="philosophy",
            tags=["行为密码学", "DNA"],
            source="lh_agent_cosmos",
        )
        e2 = hub.store(
            "鲲鹏服务器负责跑算法和推理，本地负责编辑和发起请求。",
            category="architecture",
            tags=["鲲鹏", "算力"],
            source="user",
        )
        print("stored:", e1.entry_id, e1.dna)
        print("stored:", e2.entry_id, e2.dna)
        results = hub.search("鲲鹏 算力", top_k=3)
        print("search results:", json.dumps(results, ensure_ascii=False, indent=2))
        print("stats:", hub.stats())
    else:
        print("usage: python3 cnsh_knowledge_hub.py demo")
