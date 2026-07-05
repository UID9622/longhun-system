# -*- coding: utf-8 -*-
"""#龍芯⚡️2026-06-29-SECOND-BRAIN-INDEXER-v1.0
SQLite + Chroma 向量索引
"""
import os
import re
import sqlite3
import hashlib
from pathlib import Path
from typing import List, Dict, Optional

import chromadb

from . import config
from .models import Note, Chunk
from .tfidf_embedder import TfidfSvdEmbedder


class SecondBrainIndex:
    def __init__(self, skip_embeddings: bool = False):
        os.makedirs(config.DATA_DIR, exist_ok=True)
        self.db_path = config.DB_PATH
        self.chroma_dir = config.CHROMA_DIR
        self._tfidf_cache = config.DATA_DIR / "tfidf_svd.pkl"
        self._skip_embeddings = skip_embeddings
        self._init_sqlite()
        self._init_chroma()
        self._embedding = None
        if not skip_embeddings:
            self._load_embedding_model()

    def _init_sqlite(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                note_id TEXT PRIMARY KEY,
                path TEXT UNIQUE,
                title TEXT,
                content_hash TEXT,
                created TEXT,
                modified TEXT,
                tags TEXT,
                links TEXT,
                aliases TEXT,
                metadata TEXT,
                dna TEXT,
                audit TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id TEXT PRIMARY KEY,
                note_id TEXT,
                seq INTEGER,
                text TEXT,
                FOREIGN KEY (note_id) REFERENCES notes(note_id) ON DELETE CASCADE
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS edges (
                source TEXT,
                target TEXT,
                type TEXT,
                weight REAL,
                PRIMARY KEY (source, target, type)
            )
        ''')
        self.conn.commit()

    def _init_chroma(self):
        self.client = chromadb.PersistentClient(path=str(self.chroma_dir))
        self.collection = self.client.get_or_create_collection(
            name=config.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

    def _load_embedding_model(self):
        # 默认使用本地 TF-IDF+SVD，避免网络/下载阻塞
        # 如需 sentence-transformers，请设置环境变量 SECOND_BRAIN_USE_ST=1
        if os.environ.get("SECOND_BRAIN_USE_ST") == "1":
            try:
                from sentence_transformers import SentenceTransformer
                self._embedding = SentenceTransformer(config.EMB_MODEL)
                print("✅ sentence-transformers 嵌入模型已加载")
                return
            except Exception as e:
                print(f"🟡 sentence-transformers 加载失败，启用本地 TF-IDF+SVD 降级: {e}")
        self._embedding = TfidfSvdEmbedder(cache_path=self._tfidf_cache)
        print("✅ 本地 TF-IDF+SVD 嵌入器已就绪")

    def _is_tfidf(self) -> bool:
        return isinstance(self._embedding, TfidfSvdEmbedder)

    def fit_tfidf(self) -> Dict:
        """用 SQLite 中全部 chunks 训练本地 TF-IDF+SVD，并写入 Chroma。"""
        if not self._is_tfidf():
            return {"status": "not_tfidf"}
        rows = self.conn.execute('''
            SELECT c.chunk_id, c.note_id, c.seq, c.text, n.title, n.path
            FROM chunks c JOIN notes n ON c.note_id = n.note_id
            ORDER BY c.note_id, c.seq
        ''').fetchall()
        texts = [r["text"] for r in rows]
        if not texts:
            return {"status": "no_chunks"}
        print(f"🧠 训练本地 TF-IDF+SVD 嵌入，样本数 {len(texts)}...")
        self._embedding.fit(texts)
        embeddings = self._embedding.transform(texts)
        if embeddings is None:
            return {"status": "fit_failed"}
        # 批量写入/覆盖 Chroma
        batch = 256
        for i in range(0, len(rows), batch):
            b = rows[i:i + batch]
            e = embeddings[i:i + batch]
            self.collection.upsert(
                ids=[r["chunk_id"] for r in b],
                embeddings=e,
                documents=[r["text"] for r in b],
                metadatas=[{
                    "note_id": r["note_id"],
                    "title": r["title"],
                    "path": r["path"],
                    "seq": r["seq"],
                } for r in b]
            )
        return {"status": "ok", "chunks": len(rows), "dim": len(embeddings[0])}

    def embed(self, texts: List[str]) -> Optional[List[List[float]]]:
        if self._embedding is None:
            return None
        try:
            if self._is_tfidf():
                return self._embedding.transform(texts)
            # sentence-transformers
            return [v.tolist() for v in self._embedding.encode(texts)]
        except Exception as e:
            print(f"🟡 embedding 失败: {e}")
            return None

    @staticmethod
    def _chunks_from_text(text: str, max_len: int = 600) -> List[str]:
        # 按二级标题切分，若块仍过大再按段落切
        parts = re.split(r"\n(?=##\s+)", text)
        out = []
        for part in parts:
            part = part.strip()
            if not part:
                continue
            if len(part) <= max_len:
                out.append(part)
                continue
            # 段落切分
            paras = re.split(r"\n\s*\n", part)
            buf = ""
            for para in paras:
                if len(buf) + len(para) > max_len and buf:
                    out.append(buf.strip())
                    buf = para
                else:
                    buf += "\n\n" + para if buf else para
            if buf.strip():
                out.append(buf.strip())
        return out

    def note_exists_and_unchanged(self, note: Note) -> bool:
        row = self.conn.execute(
            "SELECT content_hash FROM notes WHERE note_id=?", (note.note_id,)
        ).fetchone()
        return row is not None and row["content_hash"] == note.content_hash

    def delete_note(self, note_id: str):
        # 删除 SQLite chunks + Chroma chunks
        chunk_rows = self.conn.execute(
            "SELECT chunk_id FROM chunks WHERE note_id=?", (note_id,)
        ).fetchall()
        chunk_ids = [r["chunk_id"] for r in chunk_rows]
        if chunk_ids:
            try:
                self.collection.delete(ids=chunk_ids)
            except Exception as e:
                print(f"🟡 chroma delete {note_id}: {e}")
        self.conn.execute("DELETE FROM edges WHERE source=? OR target=?", (note_id, note_id))
        self.conn.execute("DELETE FROM chunks WHERE note_id=?", (note_id,))
        self.conn.execute("DELETE FROM notes WHERE note_id=?", (note_id,))
        self.conn.commit()

    def index_note(self, note: Note):
        if self.note_exists_and_unchanged(note):
            return False  # 无变化

        # 先删除旧数据
        self.delete_note(note.note_id)

        c = self.conn.cursor()
        c.execute('''
            INSERT INTO notes
            (note_id, path, title, content_hash, created, modified, tags, links, aliases, metadata, dna, audit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            note.note_id,
            note.path,
            note.title,
            note.content_hash,
            note.created,
            note.modified,
            ",".join(note.tags),
            ",".join(note.links),
            ",".join(note.aliases),
            str(note.metadata),
            note.dna,
            note.audit,
        ))

        texts = self._chunks_from_text(note.content)
        chunks: List[Chunk] = []
        for seq, text in enumerate(texts):
            cid = f"{note.note_id}-c{seq}"
            chunks.append(Chunk(chunk_id=cid, note_id=note.note_id, text=text, seq=seq))
            c.execute('''
                INSERT INTO chunks (chunk_id, note_id, seq, text) VALUES (?, ?, ?, ?)
            ''', (cid, note.note_id, seq, text))

        if chunks and self._embedding:
            embeddings = self.embed([ch.text for ch in chunks])
            if embeddings:
                self.collection.add(
                    ids=[ch.chunk_id for ch in chunks],
                    embeddings=embeddings,
                    documents=[ch.text for ch in chunks],
                    metadatas=[{
                        "note_id": note.note_id,
                        "title": note.title,
                        "path": note.path,
                        "seq": ch.seq,
                    } for ch in chunks]
                )
        self.conn.commit()
        return True

    def index_edges(self, note: Note, link_id_map: Dict[str, str]):
        c = self.conn.cursor()
        for link in note.links:
            target = link_id_map.get(link)
            if target:
                c.execute('''
                    INSERT OR REPLACE INTO edges (source, target, type, weight)
                    VALUES (?, ?, ?, ?)
                ''', (note.note_id, target, "wiki_link", 1.0))
        self.conn.commit()

    def get_note(self, note_id: str) -> Optional[Dict]:
        row = self.conn.execute("SELECT * FROM notes WHERE note_id=?", (note_id,)).fetchone()
        return dict(row) if row else None

    def get_all_note_ids(self) -> List[str]:
        return [r["note_id"] for r in self.conn.execute("SELECT note_id FROM notes")]

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        if self._embedding:
            emb = self.embed([query])
            if emb:
                results = self.collection.query(
                    query_embeddings=emb,
                    n_results=min(top_k * 3, 30),
                    include=["documents", "metadatas", "distances"]
                )
                out = []
                ids = results.get("ids", [[]])[0]
                docs = results.get("documents", [[]])[0]
                metas = results.get("metadatas", [[]])[0]
                dists = results.get("distances", [[]])[0]
                for cid, doc, meta, dist in zip(ids, docs, metas, dists):
                    note = self.get_note(meta["note_id"])
                    if note:
                        out.append({
                            "chunk_id": cid,
                            "note": note,
                            "snippet": doc[:300],
                            "distance": dist,
                        })
                return out
        # fallback: 关键词匹配标题/标签
        like = f"%{query}%"
        rows = self.conn.execute(
            "SELECT * FROM notes WHERE title LIKE ? OR tags LIKE ? LIMIT ?",
            (like, like, top_k * 3)
        ).fetchall()
        return [{"note": dict(r), "snippet": "", "distance": 0.0} for r in rows]

    def graph(self, note_id: str) -> List[Dict]:
        rows = self.conn.execute('''
            SELECT * FROM edges WHERE source=? OR target=?
        ''', (note_id, note_id)).fetchall()
        out = []
        for r in rows:
            other = r["target"] if r["source"] == note_id else r["source"]
            note = self.get_note(other)
            if note:
                out.append({"edge": dict(r), "note": note})
        return out

    def stats(self) -> Dict:
        counts = self.conn.execute('''
            SELECT COUNT(*) FROM notes
        ''').fetchone()[0]
        chunks = self.conn.execute('''
            SELECT COUNT(*) FROM chunks
        ''').fetchone()[0]
        edges = self.conn.execute('''
            SELECT COUNT(*) FROM edges
        ''').fetchone()[0]
        audit_counts = self.conn.execute('''
            SELECT audit, COUNT(*) FROM notes GROUP BY audit
        ''').fetchall()
        return {
            "notes": counts,
            "chunks": chunks,
            "edges": edges,
            "audit": {r["audit"]: r["COUNT(*)"] for r in audit_counts},
        }
