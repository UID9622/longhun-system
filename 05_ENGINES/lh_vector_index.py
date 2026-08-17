#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 向量索引引擎 (Vector Index Engine)
DNA: #龍芯⚡️丙午·丙申·壬戌·巳时-VECTOR-INDEX-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
License: MulanPSL v2

功能: 文件语义向量索引。鲲鹏 ARM64 优化：
      - 优先本地 Ollama 嵌入 (/api/embeddings)
      - 次选 sentence-transformers
      - 无模型时自动降级为关键词倒排 + 标题语义
      - 纯 Python/numpy，不依赖 faiss-gpu
"""

import hashlib
import json
import math
import os
import re
import sqlite3
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import requests
    HAS_REQUESTS = True
except Exception:
    HAS_REQUESTS = False
    requests = None  # type: ignore

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / ".state" / "vector_index"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "vectors.sqlite"

DNA_PREFIX = "#龍芯⚡️"
ENGINE_DNA = f"{DNA_PREFIX}丙午·丙申·壬戌·巳时-VECTOR-INDEX-UID9622"
UID = "UID9622"
CST = timezone(timedelta(hours=8))

OLLAMA_URL = os.environ.get("LH_OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("LH_OLLAMA_EMBED_MODEL", "nomic-embed-text")


def now_iso() -> str:
    return datetime.now(CST).isoformat()


def _init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS vectors (
            file_id TEXT PRIMARY KEY,
            file_path TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            embedding BLOB,
            keywords TEXT,
            title TEXT,
            summary TEXT,
            mtime REAL,
            indexed_at TEXT
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_path ON vectors(file_path)"
    )
    conn.commit()
    return conn


class EmbeddingProvider:
    """嵌入提供者，支持 Ollama / sentence-transformers / 关键词降级"""

    def __init__(self):
        self.mode: str = "keyword"
        self.model: Any = None
        self._check_ollama()
        if self.mode == "keyword":
            self._check_sentence_transformers()

    def _check_ollama(self):
        try:
            if HAS_REQUESTS:
                r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
                if r.status_code == 200:
                    self.mode = "ollama"
                    return
            else:
                import urllib.request
                import urllib.error
                req = urllib.request.Request(f"{OLLAMA_URL}/api/tags", method="GET")
                with urllib.request.urlopen(req, timeout=2) as resp:
                    if resp.status == 200:
                        self.mode = "ollama"
                        return
        except Exception:
            pass

    def _check_sentence_transformers(self):
        try:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.mode = "sentence_transformers"
        except Exception:
            self.mode = "keyword"

    def embed(self, text: str) -> Optional[List[float]]:
        if self.mode == "ollama":
            return self._ollama_embed(text)
        if self.mode == "sentence_transformers" and self.model is not None:
            return self.model.encode(text).tolist()
        return None

    def _ollama_embed(self, text: str) -> Optional[List[float]]:
        try:
            payload = json.dumps({"model": OLLAMA_MODEL, "prompt": text[:2048]}, ensure_ascii=False).encode("utf-8")
            if HAS_REQUESTS:
                r = requests.post(
                    f"{OLLAMA_URL}/api/embeddings",
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30,
                )
                if r.status_code == 200:
                    return r.json().get("embedding")
            else:
                import urllib.request
                req = urllib.request.Request(
                    f"{OLLAMA_URL}/api/embeddings",
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    return json.loads(resp.read().decode("utf-8")).get("embedding")
        except Exception:
            pass
        return None


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _extract_keywords(text: str, topk: int = 20) -> List[str]:
    """轻量中文关键词提取（无需 jieba 也能跑）"""
    try:
        import jieba

        words = [w.strip() for w in jieba.cut(text) if len(w.strip()) > 1]
        freq: Dict[str, int] = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        return [w for w, _ in sorted(freq.items(), key=lambda x: -x[1])[:topk]]
    except Exception:
        # 纯 Python fallback：2-4 字 ngram
        text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", " ", text)
        tokens = text.split()
        ngrams: Dict[str, int] = {}
        for t in tokens:
            for n in (2, 3, 4):
                for i in range(len(t) - n + 1):
                    ng = t[i : i + n]
                    ngrams[ng] = ngrams.get(ng, 0) + 1
        return [w for w, _ in sorted(ngrams.items(), key=lambda x: -x[1])[:topk]]


def _file_hash(path: Path) -> str:
    h = hashlib.sha256()
    try:
        h.update(path.read_bytes())
    except Exception:
        pass
    return h.hexdigest()[:16]


def _summarize(text: str, max_len: int = 200) -> str:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return ""
    summary = lines[0][:max_len]
    if len(summary) < max_len and len(lines) > 1:
        summary += " " + lines[1][: max_len - len(summary)]
    return summary


class VectorIndex:
    """向量索引主类"""

    def __init__(self):
        self.conn = _init_db()
        self.provider = EmbeddingProvider()

    def index_file(self, path: Path, force: bool = False) -> Dict[str, Any]:
        path = path.resolve()
        file_id = hashlib.sha256(str(path).encode()).hexdigest()[:16]
        content_hash = _file_hash(path)

        cursor = self.conn.execute(
            "SELECT content_hash FROM vectors WHERE file_id=?", (file_id,)
        )
        row = cursor.fetchone()
        if row and row[0] == content_hash and not force:
            return {"status": "unchanged", "file_id": file_id, "path": str(path)}

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            return {"status": "error", "error": str(e), "path": str(path)}

        title = path.name
        summary = _summarize(text)
        keywords = _extract_keywords(text)
        embedding = self.provider.embed(text[:3000])

        self.conn.execute(
            """
            INSERT OR REPLACE INTO vectors
            (file_id, file_path, content_hash, embedding, keywords, title, summary, mtime, indexed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                file_id,
                str(path),
                content_hash,
                json.dumps(embedding, ensure_ascii=False) if embedding else None,
                json.dumps(keywords, ensure_ascii=False),
                title,
                summary,
                path.stat().st_mtime if path.exists() else 0,
                now_iso(),
            ),
        )
        self.conn.commit()

        return {
            "status": "indexed",
            "file_id": file_id,
            "path": str(path),
            "mode": self.provider.mode,
            "embedding_dim": len(embedding) if embedding else 0,
            "keywords": keywords[:5],
        }

    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """语义搜索 + 关键词搜索混合"""
        query_emb = self.provider.embed(query[:500])
        cursor = self.conn.execute(
            "SELECT file_id, file_path, embedding, keywords, title, summary FROM vectors"
        )
        results: List[Dict[str, Any]] = []
        query_keywords = set(_extract_keywords(query, topk=10))

        for row in cursor:
            file_id, file_path, emb_json, kw_json, title, summary = row
            score = 0.0
            reasons: List[str] = []

            # 语义分
            if query_emb and emb_json:
                emb = json.loads(emb_json)
                sim = _cosine_similarity(query_emb, emb)
                score += sim * 0.6
                if sim > 0.5:
                    reasons.append(f"semantic:{sim:.2f}")

            # 关键词分
            if kw_json:
                kws = set(json.loads(kw_json))
                overlap = len(query_keywords & kws)
                if overlap:
                    score += min(overlap * 0.1, 0.4)
                    reasons.append(f"keyword:{overlap}")

            # 标题命中奖励
            if query.lower() in title.lower():
                score += 0.15
                reasons.append("title")

            if score > 0.05:
                results.append(
                    {
                        "file_id": file_id,
                        "path": file_path,
                        "title": title,
                        "summary": summary,
                        "score": round(score, 4),
                        "reasons": reasons,
                    }
                )

        results.sort(key=lambda x: -x["score"])
        return results[:top_k]

    def index_directory(
        self, root: Path, pattern: str = "*.md", force: bool = False
    ) -> Dict[str, Any]:
        root = root.resolve()
        files = [p for p in root.rglob(pattern) if p.is_file() and ".git" not in p.parts]
        stats = {"total": len(files), "indexed": 0, "unchanged": 0, "errors": 0}
        for p in files:
            r = self.index_file(p, force=force)
            if r["status"] == "indexed":
                stats["indexed"] += 1
            elif r["status"] == "unchanged":
                stats["unchanged"] += 1
            else:
                stats["errors"] += 1
        return stats

    def stats(self) -> Dict[str, Any]:
        cursor = self.conn.execute("SELECT COUNT(*) FROM vectors")
        count = cursor.fetchone()[0]
        return {
            "db_path": str(DB_PATH),
            "total_files": count,
            "embedding_mode": self.provider.mode,
            "ollama_url": OLLAMA_URL,
            "ollama_model": OLLAMA_MODEL,
            "dna": ENGINE_DNA,
        }


def cli():
    import argparse

    parser = argparse.ArgumentParser(description="龍魂向量索引引擎")
    sub = parser.add_subparsers(dest="cmd")

    p_index = sub.add_parser("index", help="索引文件或目录")
    p_index.add_argument("target", help="目标文件/目录")
    p_index.add_argument("--pattern", default="*.md", help="通配符")
    p_index.add_argument("--force", action="store_true", help="强制重建")

    p_search = sub.add_parser("search", help="语义搜索")
    p_search.add_argument("query", help="查询语句")
    p_search.add_argument("--top", type=int, default=10, help="返回数量")

    p_stats = sub.add_parser("stats", help="索引统计")

    args = parser.parse_args()
    idx = VectorIndex()

    if args.cmd == "index":
        target = Path(args.target)
        if target.is_file():
            print(json.dumps(idx.index_file(target, force=args.force), ensure_ascii=False, indent=2))
        else:
            print(json.dumps(idx.index_directory(target, pattern=args.pattern, force=args.force), ensure_ascii=False, indent=2))
    elif args.cmd == "search":
        print(json.dumps(idx.search(args.query, top_k=args.top), ensure_ascii=False, indent=2))
    elif args.cmd == "stats":
        print(json.dumps(idx.stats(), ensure_ascii=False, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
