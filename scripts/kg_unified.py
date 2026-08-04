#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# #龍芯⚡️20260624010825160-AUTO-DNA-B1DF8BB0 自动注入·分层治理自愈引擎 · 来源可查
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂统一知识中枢 · Knowledge Graph + Vector + Database 联动引擎

功能：
  1. 把多个孤立数据源（graph_data.json、notion_pages.db、
     dragon_knowledge.db、brain memories）汇入统一 SQLite 图谱。
  2. 为节点生成本地 TF-IDF 向量，支持语义相似度检索。
  3. 对外提供统一查询接口：全文检索、向量检索、图谱扩展。

DNA: #龍芯⚡️2026-06-22-UNIFIED-KG-v1.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

HOME = pathlib.Path.home()
PROJECT_ROOT = HOME / "longhun-system"
UNIFIED_DB_DIR = PROJECT_ROOT / "brain"
UNIFIED_DB_PATH = UNIFIED_DB_DIR / "unified_kg.db"
VECTOR_CACHE_PATH = UNIFIED_DB_DIR / "unified_kg_vectors.npz"
VECTORIZER_PATH = UNIFIED_DB_DIR / "unified_kg_vectorizer.pkl"

GRAPH_DATA_PATH = PROJECT_ROOT / "03_知識圖譜" / "graph_data.json"
NOTION_DB_PATH = HOME / ".longhun" / "notion_pages" / "notion_pages.db"
DRAGON_KNOWLEDGE_DB = HOME / "_work" / "dragon_knowledge.db"
BRAIN_DB_PATH = PROJECT_ROOT / "brain" / "memories.db"

DNA = "#龍芯⚡️2026-06-22-UNIFIED-KG-v1.0"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _dna(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = hashlib.sha256(f"{prefix}|{ts}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{prefix}-{h}"


def _safe_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, default=str)


def init_db(db_path: pathlib.Path = UNIFIED_DB_PATH) -> sqlite3.Connection:
    UNIFIED_DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            record_count INTEGER DEFAULT 0,
            last_synced_at TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS nodes (
            id TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            source_id TEXT NOT NULL,
            label TEXT NOT NULL,
            node_type TEXT NOT NULL,
            content TEXT,
            metadata TEXT,
            dna TEXT,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY (source) REFERENCES sources(id)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_nodes_source ON nodes(source)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_nodes_type ON nodes(node_type)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_nodes_label ON nodes(label)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_nodes_content ON nodes(content)")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS edges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_node TEXT NOT NULL,
            target_node TEXT NOT NULL,
            relation TEXT NOT NULL,
            weight REAL DEFAULT 1.0,
            metadata TEXT,
            dna TEXT,
            FOREIGN KEY (source_node) REFERENCES nodes(id),
            FOREIGN KEY (target_node) REFERENCES nodes(id)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_node)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_node)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_pair ON edges(source_node, target_node)")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS node_vectors (
            node_id TEXT PRIMARY KEY,
            vector BLOB,
            vector_type TEXT DEFAULT 'tfidf',
            generated_at TEXT,
            FOREIGN KEY (node_id) REFERENCES nodes(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS sync_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            action TEXT,
            count INTEGER,
            dna TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    return conn


def _clear_source(conn: sqlite3.Connection, source: str) -> None:
    conn.execute("DELETE FROM node_vectors WHERE node_id IN (SELECT id FROM nodes WHERE source=?)", (source,))
    conn.execute("DELETE FROM edges WHERE source_node IN (SELECT id FROM nodes WHERE source=?)", (source,))
    conn.execute("DELETE FROM edges WHERE target_node IN (SELECT id FROM nodes WHERE source=?)", (source,))
    conn.execute("DELETE FROM nodes WHERE source=?", (source,))


def _register_source(conn: sqlite3.Connection, source_id: str, name: str, description: str, count: int) -> None:
    conn.execute(
        """INSERT OR REPLACE INTO sources(id, name, description, record_count, last_synced_at)
           VALUES(?,?,?,?,?)""",
        (source_id, name, description, count, _now()),
    )


def _log_sync(conn: sqlite3.Connection, source: str, action: str, count: int) -> None:
    conn.execute(
        "INSERT INTO sync_log(source, action, count, dna, timestamp) VALUES(?,?,?,?,?)",
        (source, action, count, _dna(action), _now()),
    )


def sync_graph_data(conn: sqlite3.Connection, path: pathlib.Path = GRAPH_DATA_PATH) -> int:
    source = "graph_data"
    _clear_source(conn, source)
    _register_source(conn, source, "项目文件知识图谱", "03_KNOWLEDGE_GRAPH/graph_data.json", 0)
    if not path.exists():
        return 0

    data = json.loads(path.read_text(encoding="utf-8"))
    nodes = data.get("nodes", {})
    edges = data.get("edges", [])
    ts = _now()

    for nid, n in nodes.items():
        label = n.get("label") or nid
        content = "\n".join(filter(None, [
            n.get("description", ""),
            " ".join(n.get("related_nodes", [])),
        ]))
        metadata = {k: v for k, v in n.items() if k not in ("node_id", "label", "type", "description", "related_nodes")}
        conn.execute(
            """INSERT INTO nodes(id, source, source_id, label, node_type, content, metadata, dna, created_at, updated_at)
               VALUES(?,?,?,?,?,?,?,?,?,?)""",
            (
                f"{source}:{nid}",
                source,
                nid,
                label,
                n.get("type", "unknown"),
                content,
                _safe_json(metadata),
                n.get("dna") or _dna("GRAPH-NODE"),
                ts,
                ts,
            ),
        )

    node_id_set = set(nodes.keys())
    edge_count = 0
    for e in edges:
        src = e.get("source")
        tgt = e.get("target")
        if src not in node_id_set or tgt not in node_id_set:
            continue
        conn.execute(
            """INSERT INTO edges(source_node, target_node, relation, weight, metadata, dna)
               VALUES(?,?,?,?,?,?)""",
            (
                f"{source}:{src}",
                f"{source}:{tgt}",
                e.get("relationship", "related"),
                e.get("strength", 1.0),
                _safe_json(e),
                _dna("GRAPH-EDGE"),
            ),
        )
        edge_count += 1

    conn.execute("UPDATE sources SET record_count=? WHERE id=?", (len(nodes), source))
    _log_sync(conn, source, "sync_nodes", len(nodes))
    _log_sync(conn, source, "sync_edges", edge_count)
    conn.commit()
    return len(nodes)


def sync_notion_pages(conn: sqlite3.Connection, db_path: pathlib.Path = NOTION_DB_PATH) -> int:
    source = "notion_pages"
    _clear_source(conn, source)
    _register_source(conn, source, "Notion 页面与知识图谱", str(db_path), 0)
    if not db_path.exists():
        return 0

    src_conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    src_conn.row_factory = sqlite3.Row
    ts = _now()

    # pages -> nodes
    rows = src_conn.execute(
        """SELECT id, title, category, subcategory, notion_url, local_md_path,
                  word_count, block_count, phase, dna, created, modified
           FROM pages WHERE status='done'"""
    ).fetchall()

    page_count = 0
    for r in rows:
        pid = r["id"]
        title = r["title"] or "未命名"
        content = ""
        if r["local_md_path"] and pathlib.Path(r["local_md_path"]).exists():
            try:
                content = pathlib.Path(r["local_md_path"]).read_text(encoding="utf-8")[:4000]
            except Exception:
                pass
        metadata = {
            "category": r["category"],
            "subcategory": r["subcategory"],
            "word_count": r["word_count"],
            "block_count": r["block_count"],
            "phase": r["phase"],
            "notion_url": r["notion_url"],
            "local_md_path": r["local_md_path"],
            "created": r["created"],
            "modified": r["modified"],
        }
        conn.execute(
            """INSERT INTO nodes(id, source, source_id, label, node_type, content, metadata, dna, created_at, updated_at)
               VALUES(?,?,?,?,?,?,?,?,?,?)""",
            (
                f"{source}:page:{pid}",
                source,
                pid,
                title,
                "page",
                content,
                _safe_json(metadata),
                r["dna"] or _dna("NOTION-PAGE"),
                r["created"] or ts,
                r["modified"] or ts,
            ),
        )
        page_count += 1

    # entities -> nodes
    entity_rows = src_conn.execute(
        "SELECT id, name, type, tongxin_zh, first_seen_page_id, first_seen_at, occurrence_count FROM entities"
    ).fetchall()

    entity_id_map: Dict[int, str] = {}
    for r in entity_rows:
        eid = r["id"]
        name = r["name"]
        etype = r["type"]
        local_id = f"entity:{eid}"
        global_id = f"{source}:{local_id}"
        entity_id_map[eid] = global_id
        content = f"{name} ({etype})"
        if r["tongxin_zh"]:
            content += f" 通心译：{r['tongxin_zh']}"
        metadata = {
            "tongxin_zh": r["tongxin_zh"],
            "first_seen_page_id": r["first_seen_page_id"],
            "first_seen_at": r["first_seen_at"],
            "occurrence_count": r["occurrence_count"],
        }
        conn.execute(
            """INSERT INTO nodes(id, source, source_id, label, node_type, content, metadata, dna, created_at, updated_at)
               VALUES(?,?,?,?,?,?,?,?,?,?)""",
            (
                global_id,
                source,
                local_id,
                name,
                etype,
                content,
                _safe_json(metadata),
                _dna("NOTION-ENTITY"),
                r["first_seen_at"] or ts,
                ts,
            ),
        )

    # relations -> edges
    rel_rows = src_conn.execute(
        "SELECT source_id, target_id, relation_type, page_id, context, weight FROM relations"
    ).fetchall()

    rel_count = 0
    for r in rel_rows:
        sid = entity_id_map.get(r["source_id"])
        tid = entity_id_map.get(r["target_id"])
        if not sid or not tid:
            continue
        conn.execute(
            """INSERT INTO edges(source_node, target_node, relation, weight, metadata, dna)
               VALUES(?,?,?,?,?,?)""",
            (
                sid,
                tid,
                r["relation_type"],
                r["weight"] or 1.0,
                _safe_json({"page_id": r["page_id"], "context": r["context"]}),
                _dna("NOTION-REL"),
            ),
        )
        rel_count += 1

    # entity -> page edges
    occ_rows = src_conn.execute(
        "SELECT entity_id, page_id FROM entity_occurrences"
    ).fetchall()
    occ_added: set[Any] = set()
    for r in occ_rows:
        eid = entity_id_map.get(r["entity_id"])
        pid = f"{source}:page:{r['page_id']}"
        if not eid:
            continue
        key = (eid, pid)
        if key in occ_added:
            continue
        occ_added.add(key)
        conn.execute(
            """INSERT INTO edges(source_node, target_node, relation, weight, metadata, dna)
               VALUES(?,?,?,?,?,?)""",
            (eid, pid, "appears_in", 0.8, "{}", _dna("NOTION-OCC")),
        )

    total_nodes = page_count + len(entity_id_map)
    conn.execute("UPDATE sources SET record_count=? WHERE id=?", (total_nodes, source))
    _log_sync(conn, source, "sync_pages", page_count)
    _log_sync(conn, source, "sync_entities", len(entity_id_map))
    _log_sync(conn, source, "sync_relations", rel_count)
    conn.commit()
    src_conn.close()
    return total_nodes


def sync_dragon_knowledge(conn: sqlite3.Connection, db_path: pathlib.Path = DRAGON_KNOWLEDGE_DB) -> int:
    source = "dragon_knowledge"
    _clear_source(conn, source)
    _register_source(conn, source, "代码收割知识库", str(db_path), 0)
    if not db_path.exists():
        return 0

    src_conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    src_conn.row_factory = sqlite3.Row
    ts = _now()

    rows = src_conn.execute(
        """SELECT code_id, file_name, file_path, file_extension, source_language,
                  theory_guide, source_url_or_path, author, dna_code, cnsh_version,
                  content_raw, content_hash, created_at
           FROM harvested_code"""
    ).fetchall()

    count = 0
    author_nodes: Dict[str, str] = {}
    lang_nodes: Dict[str, str] = {}

    for r in rows:
        cid = r["code_id"]
        label = (r["file_name"] or "unnamed").split("/")[-1]
        content = (r["content_raw"] or "")[:4000]
        metadata = {
            "file_path": r["file_path"],
            "file_extension": r["file_extension"],
            "source_language": r["source_language"],
            "theory_guide": r["theory_guide"],
            "source_url_or_path": r["source_url_or_path"],
            "author": r["author"],
            "cnsh_version": r["cnsh_version"],
            "content_hash": r["content_hash"],
        }
        global_id = f"{source}:{cid}"
        conn.execute(
            """INSERT INTO nodes(id, source, source_id, label, node_type, content, metadata, dna, created_at, updated_at)
               VALUES(?,?,?,?,?,?,?,?,?,?)""",
            (
                global_id,
                source,
                cid,
                label,
                "code",
                content,
                _safe_json(metadata),
                r["dna_code"] or _dna("CODE"),
                r["created_at"] or ts,
                ts,
            ),
        )
        count += 1

        # author edges
        author = r["author"]
        if author:
            if author not in author_nodes:
                aid = f"{source}:author:{author}"
                author_nodes[author] = aid
                conn.execute(
                    """INSERT INTO nodes(id, source, source_id, label, node_type, content, metadata, dna, created_at, updated_at)
                       VALUES(?,?,?,?,?,?,?,?,?,?)""",
                    (aid, source, f"author:{author}", author, "author", f"作者：{author}", "{}", _dna("AUTHOR"), ts, ts),
                )
            conn.execute(
                """INSERT INTO edges(source_node, target_node, relation, weight, metadata, dna)
                   VALUES(?,?,?,?,?,?)""",
                (global_id, author_nodes[author], "authored_by", 1.0, "{}", _dna("CODE-AUTHOR")),
            )

        # language edges
        lang = r["source_language"] or (r["file_extension"] or "").lstrip(".")
        if lang:
            if lang not in lang_nodes:
                lid = f"{source}:lang:{lang}"
                lang_nodes[lang] = lid
                conn.execute(
                    """INSERT INTO nodes(id, source, source_id, label, node_type, content, metadata, dna, created_at, updated_at)
                       VALUES(?,?,?,?,?,?,?,?,?,?)""",
                    (lid, source, f"lang:{lang}", lang, "language", f"语言：{lang}", "{}", _dna("LANG"), ts, ts),
                )
            conn.execute(
                """INSERT INTO edges(source_node, target_node, relation, weight, metadata, dna)
                   VALUES(?,?,?,?,?,?)""",
                (global_id, lang_nodes[lang], "written_in", 0.9, "{}", _dna("CODE-LANG")),
            )

    conn.execute("UPDATE sources SET record_count=? WHERE id=?", (count, source))
    _log_sync(conn, source, "sync_code", count)
    conn.commit()
    src_conn.close()
    return count


def sync_brain_memories(conn: sqlite3.Connection, db_path: pathlib.Path = BRAIN_DB_PATH) -> int:
    source = "brain_memories"
    _clear_source(conn, source)
    _register_source(conn, source, "龍魂脑干记忆链", str(db_path), 0)
    if not db_path.exists():
        return 0

    src_conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    src_conn.row_factory = sqlite3.Row
    ts = _now()

    rows = src_conn.execute(
        """SELECT id, dna, content, wuxing, persona, dr, tricolor, tags, source, created_at
           FROM memories"""
    ).fetchall()

    count = 0
    for r in rows:
        mid = str(r["id"])
        content = r["content"] or ""
        label = content[:40] + "..." if len(content) > 40 else content
        metadata = {
            "wuxing": r["wuxing"],
            "persona": r["persona"],
            "dr": r["dr"],
            "tricolor": r["tricolor"],
            "tags": r["tags"],
            "source": r["source"],
        }
        conn.execute(
            """INSERT INTO nodes(id, source, source_id, label, node_type, content, metadata, dna, created_at, updated_at)
               VALUES(?,?,?,?,?,?,?,?,?,?)""",
            (
                f"{source}:{mid}",
                source,
                mid,
                label,
                "memory",
                content,
                _safe_json(metadata),
                r["dna"] or _dna("MEMORY"),
                r["created_at"] or ts,
                ts,
            ),
        )
        count += 1

    conn.execute("UPDATE sources SET record_count=? WHERE id=?", (count, source))
    _log_sync(conn, source, "sync_memories", count)
    conn.commit()
    src_conn.close()
    return count


def build_vector_index(conn: sqlite3.Connection) -> Tuple[int, int]:
    """为所有有 content 的节点生成 TF-IDF 向量。"""
    rows = conn.execute(
        "SELECT id, content FROM nodes WHERE content IS NOT NULL AND length(content) > 10"
    ).fetchall()

    if not rows:
        return 0, 0

    ids = [r[0] for r in rows]
    texts = [r[1] for r in rows]

    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(2, 4),
        max_features=4096,
        stop_words=None,
    )
    X = vectorizer.fit_transform(texts)

    # 保存到表
    conn.execute("DELETE FROM node_vectors")
    for nid, vec in zip(ids, X):
        arr = vec.toarray().astype(np.float32).flatten()
        conn.execute(
            "INSERT OR REPLACE INTO node_vectors(node_id, vector, vector_type, generated_at) VALUES(?,?,?,?)",
            (nid, arr.tobytes(), "tfidf", _now()),
        )

    # 保存 vectorizer + 矩阵缓存，便于快速查询
    np.savez(
        VECTOR_CACHE_PATH,
        ids=np.array(ids, dtype=object),
        matrix=X.toarray().astype(np.float32),
    )
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    _log_sync(conn, "unified_kg", "build_vector_index", len(ids))
    conn.commit()
    return len(ids), X.shape[1]


def vector_search(conn: sqlite3.Connection, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
    if not VECTOR_CACHE_PATH.exists() or not VECTORIZER_PATH.exists():
        return []

    cache = np.load(VECTOR_CACHE_PATH, allow_pickle=True)
    ids = cache["ids"].tolist()
    matrix = cache["matrix"].astype(np.float32)

    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)

    q_vec = vectorizer.transform([query]).toarray().astype(np.float32)

    if q_vec.sum() == 0:
        return []

    sims = cosine_similarity(q_vec, matrix)[0]
    top_idx = np.argsort(sims)[::-1][:top_k]

    results = []
    for idx in top_idx:
        if sims[idx] <= 0:
            continue
        nid = ids[idx]
        row = conn.execute(
            "SELECT id, source, label, node_type, content, metadata FROM nodes WHERE id=?", (nid,)
        ).fetchone()
        if row:
            results.append({
                "id": row[0],
                "source": row[1],
                "label": row[2],
                "node_type": row[3],
                "content_preview": (row[4] or "")[:300],
                "metadata": json.loads(row[5] or "{}"),
                "score": round(float(sims[idx]), 4),
            })
    return results


def full_text_search(conn: sqlite3.Connection, query: str, top_k: int = 20) -> List[Dict[str, Any]]:
    pattern = f"%{query}%"
    rows = conn.execute(
        """SELECT id, source, label, node_type, content, metadata
           FROM nodes
           WHERE label LIKE ? OR content LIKE ? OR node_type LIKE ?
           LIMIT ?""",
        (pattern, pattern, pattern, top_k),
    ).fetchall()

    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "source": r[1],
            "label": r[2],
            "node_type": r[3],
            "content_preview": (r[4] or "")[:300],
            "metadata": json.loads(r[5] or "{}"),
        })
    return results


def graph_expand(conn: sqlite3.Connection, node_id: str, depth: int = 1) -> Dict[str, Any]:
    current = {node_id}
    node_set = {node_id}
    for _ in range(depth):
        nxt = set()
        placeholders = ",".join(["?"] * len(current))
        rows = conn.execute(
            f"SELECT source_node, target_node FROM edges WHERE source_node IN ({placeholders}) OR target_node IN ({placeholders})",
            list(current) + list(current),
        ).fetchall()
        for src, tgt in rows:
            nxt.add(src)
            nxt.add(tgt)
        current = nxt
        node_set |= nxt

    nodes = []
    for nid in node_set:
        row = conn.execute(
            "SELECT id, source, label, node_type, content, metadata FROM nodes WHERE id=?", (nid,)
        ).fetchone()
        if row:
            nodes.append({
                "id": row[0],
                "source": row[1],
                "label": row[2],
                "node_type": row[3],
                "content_preview": (row[4] or "")[:200],
                "metadata": json.loads(row[5] or "{}"),
            })

    placeholders = ",".join(["?"] * len(node_set))
    edges = []
    for row in conn.execute(
        f"SELECT source_node, target_node, relation, weight, metadata FROM edges WHERE source_node IN ({placeholders}) AND target_node IN ({placeholders})",
        list(node_set) + list(node_set),
    ).fetchall():
        edges.append({
            "source": row[0],
            "target": row[1],
            "relation": row[2],
            "weight": row[3],
            "metadata": json.loads(row[4] or "{}"),
        })

    return {"center": node_id, "depth": depth, "nodes": nodes, "edges": edges}


def unified_search(
    conn: sqlite3.Connection,
    query: str,
    top_k: int = 10,
    use_vector: bool = True,
) -> Dict[str, Any]:
    ft = full_text_search(conn, query, top_k)
    vec = vector_search(conn, query, top_k) if use_vector else []

    seen = {r["id"] for r in ft}
    combined = list(ft)
    for r in vec:
        if r["id"] not in seen:
            r["source_type"] = "vector"
            combined.append(r)
        else:
            # 提升已有结果分数
            for item in combined:
                if item["id"] == r["id"]:
                    item["score"] = max(item.get("score", 0.0), r["score"])
                    break

    combined.sort(key=lambda x: x.get("score", 0.0), reverse=True)
    return {
        "dna": _dna("UNIFIED-SEARCH"),
        "timestamp": _now(),
        "query": query,
        "text_count": len(ft),
        "vector_count": len(vec),
        "results": combined[:top_k],
    }


def get_stats(conn: sqlite3.Connection) -> Dict[str, Any]:
    cur = conn.execute("SELECT id, name, description, record_count, last_synced_at FROM sources ORDER BY id")
    sources = [
        {"id": r[0], "name": r[1], "description": r[2], "record_count": r[3], "last_synced_at": r[4]}
        for r in cur.fetchall()
    ]
    node_count = conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
    edge_count = conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
    vector_count = conn.execute("SELECT COUNT(*) FROM node_vectors").fetchone()[0]
    type_dist = {r[0]: r[1] for r in conn.execute(
        "SELECT node_type, COUNT(*) FROM nodes GROUP BY node_type ORDER BY COUNT(*) DESC"
    ).fetchall()}
    return {
        "dna": _dna("STATS"),
        "timestamp": _now(),
        "sources": sources,
        "node_count": node_count,
        "edge_count": edge_count,
        "vector_count": vector_count,
        "type_distribution": type_dist,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="龍魂统一知识中枢")
    parser.add_argument("--sync", action="store_true", help="同步所有数据源")
    parser.add_argument("--index", action="store_true", help="重建向量索引")
    parser.add_argument("--search", type=str, help="统一检索")
    parser.add_argument("--vector-search", type=str, help="仅向量检索")
    parser.add_argument("--expand", type=str, help="图谱扩展：指定节点 ID")
    parser.add_argument("--depth", type=int, default=1, help="扩展深度")
    parser.add_argument("--stats", action="store_true", help="统计")
    parser.add_argument("--top-k", type=int, default=10)
    args = parser.parse_args()

    conn = init_db()

    if args.sync:
        print("🐉 开始同步统一知识中枢...")
        c1 = sync_graph_data(conn)
        c2 = sync_notion_pages(conn)
        c3 = sync_dragon_knowledge(conn)
        c4 = sync_brain_memories(conn)
        print(f"  graph_data: {c1} nodes")
        print(f"  notion_pages: {c2} nodes")
        print(f"  dragon_knowledge: {c3} nodes")
        print(f"  brain_memories: {c4} nodes")
        print("🧬 同步完成，准备重建向量索引...")
        n, dim = build_vector_index(conn)
        print(f"  向量索引：{n} 个节点，维度 {dim}")
        print(f"  数据库：{UNIFIED_DB_PATH}")

    if args.index:
        n, dim = build_vector_index(conn)
        print(f"向量索引完成：{n} 个节点，维度 {dim}")

    if args.search:
        res = unified_search(conn, args.search, args.top_k)
        print(json.dumps(res, ensure_ascii=False, indent=2))

    if args.vector_search:
        res = vector_search(conn, args.vector_search, args.top_k)
        print(json.dumps(res, ensure_ascii=False, indent=2))

    if args.expand:
        res = graph_expand(conn, args.expand, args.depth)
        print(json.dumps(res, ensure_ascii=False, indent=2))

    if args.stats:
        print(json.dumps(get_stats(conn), ensure_ascii=False, indent=2))

    if not any([args.sync, args.index, args.search, args.vector_search, args.expand, args.stats]):
        print(__doc__)
        print(f"当前统计：{json.dumps(get_stats(conn), ensure_ascii=False, indent=2)}")

    conn.close()


if __name__ == "__main__":
    main()
