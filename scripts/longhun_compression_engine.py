#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# #龍芯⚡️20260624010825160-AUTO-DNA-EADCC922 自动注入·分层治理自愈引擎 · 来源可查
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂认知压缩引擎 · LongHun Compression Engine

把大量信息（技能文档、上下文对话、记忆链）压缩成可召回的"认知粒子"：
  - 编号：短码 / 哈希前缀
  - 语义核心：一句话摘要 + 关键词
  - 向量：本地 TF-IDF 语义向量
  - DNA：龍魂追溯码

解决老大说的：
  - "几百万字压缩成几个字"
  - "几百个字就是向量"
  - "一个技能压缩成一个编号"

DNA: #龍芯⚡️2026-06-24-LONGHUN-COMPRESSION-ENGINE-v1.0
# STATUS: ⚠️ DEPRECATED · 压缩能力已整合进 engines/lh_fixed_point_memory_archive.py
# 保留原因: 历史压缩算法参考，新代码请使用 MemoryArchive.compress()
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import pickle
import re
import sqlite3
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

HOME = pathlib.Path.home()
ROOT = HOME / "longhun-system"
DB_DIR = ROOT / "brain"
DB_PATH = DB_DIR / "compression_registry.db"
VECTOR_CACHE_PATH = DB_DIR / "compression_vectors.npz"
VECTORIZER_PATH = DB_DIR / "compression_vectorizer.pkl"

DNA = "#龍芯⚡️2026-06-24-LONGHUN-COMPRESSION-ENGINE-v1.0"

# 中文停用词
STOPWORDS = set(
    "的 了 和 是 在 我 有 就 不 人 都 一 一个 上 也 很 到 说 要 去 你 会 着 没有 看 好 自己 这 那 我们 可以 这个 这些 为 之 与 而 及 以 于 被 把 给 让 向 从 对 将 等 吗 呢 吧 啊 哦 嗯".split()
    + "the a an is are was were be been have has had do does did will would could should may might must can shall".split()
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _dna(prefix: str, seed: str = "") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = hashlib.sha256(f"{prefix}|{seed}|{ts}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{prefix}-{h}"


def _safe_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, default=str)


def init_db() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS compressed_items (
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
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_type ON compressed_items(item_type)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_shortcode ON compressed_items(shortcode)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_source ON compressed_items(source_id)")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS compression_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            item_type TEXT,
            shortcode TEXT,
            details TEXT,
            dna TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    return conn


def _log(conn: sqlite3.Connection, action: str, item_type: str, shortcode: str, details: str = "") -> None:
    conn.execute(
        "INSERT INTO compression_log(action, item_type, shortcode, details, dna, timestamp) VALUES(?,?,?,?,?,?)",
        (action, item_type, shortcode, details, _dna(action, shortcode), _now()),
    )
    conn.commit()


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _extract_chinese_terms(text: str, top_k: int = 12) -> List[Tuple[str, int]]:
    """提取中文词组并按频率排序。"""
    # 2-6 字中文词
    terms: Dict[str, int] = {}
    for m in re.finditer(r"[\u4e00-\u9fff]{2,8}", text):
        term = m.group(0)
        if len(term) >= 2 and len(term) <= 8 and term not in STOPWORDS:
            terms[term] = terms.get(term, 0) + 1
    # 过滤单字和过短的
    return sorted(terms.items(), key=lambda x: x[1], reverse=True)[:top_k]


def _extract_english_terms(text: str, top_k: int = 8) -> List[Tuple[str, int]]:
    """提取英文术语（驼峰、下划线、连续大写单词）。"""
    terms: Dict[str, int] = {}
    for m in re.finditer(r"[A-Za-z][A-Za-z0-9_]{1,30}", text):
        term = m.group(0).lower()
        if term not in STOPWORDS and len(term) > 2:
            terms[term] = terms.get(term, 0) + 1
    return sorted(terms.items(), key=lambda x: x[1], reverse=True)[:top_k]


def _generate_summary(text: str, title: str = "", max_len: int = 120) -> str:
    """生成一句话摘要。"""
    # 优先取标题
    if title:
        return title[:max_len]

    # 尝试取 Markdown 第一段非空文本
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines[:10]:
        # 跳过标题、代码块标记、链接
        if line.startswith("#") or line.startswith("```") or line.startswith("["):
            continue
        # 取中文/英文混合的有效句子
        cleaned = re.sub(r"\[.*?\]\(.*?\)", "", line)
        cleaned = cleaned.strip("*->· ")
        if len(cleaned) > 10:
            return cleaned[:max_len]

    # fallback：关键词拼接
    terms = _extract_chinese_terms(text, top_k=5)
    if terms:
        return "关于" + "、".join([t[0] for t in terms[:5]]) + "的内容"
    return text[:max_len].replace("\n", " ")


def _generate_shortcode(item_type: str, source_id: str, content_hash: str) -> str:
    """生成短码编号。"""
    prefix = {
        "skill": "SKILL",
        "context": "CTX",
        "memory": "MEM",
        "editor": "EDIT",
    }.get(item_type, "ITEM")
    # 来源路径取最后一段
    name = pathlib.Path(source_id).stem if "/" in source_id or "\\" in source_id else source_id
    name = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9_-]", "", name)[:16]
    h = content_hash[:6].upper()
    return f"{prefix}-{name}-{h}".replace("--", "-")


def compress_text(
    conn: sqlite3.Connection,
    text: str,
    item_type: str,
    source_id: str,
    title: str = "",
) -> Dict[str, Any]:
    """把任意长文本压缩成编号+语义核心+向量。"""
    if not text or len(text.strip()) < 10:
        raise ValueError("文本过短，无法压缩")

    content_hash = _content_hash(text)
    shortcode = _generate_shortcode(item_type, source_id, content_hash)

    # 摘要
    summary = _generate_summary(text, title)

    # 关键词
    cn_terms = _extract_chinese_terms(text)
    en_terms = _extract_english_terms(text)
    keywords = [t[0] for t in cn_terms] + [t[0] for t in en_terms]
    keywords = list(dict.fromkeys(keywords))[:15]  # 去重，最多15个

    # 元数据
    metadata = {
        "char_count": len(text),
        "word_count": len(re.findall(r"[\u4e00-\u9fff]", text)),
        "compressed_at": _now(),
    }

    dna = _dna("COMPRESS", content_hash)

    # 保存到数据库
    conn.execute(
        """INSERT OR REPLACE INTO compressed_items
           (item_type, source_id, shortcode, title, summary, keywords, vector_type, content_hash, metadata, dna, created_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (
            item_type,
            source_id,
            shortcode,
            title or summary[:40],
            summary,
            _safe_json(keywords),
            "tfidf",
            content_hash,
            _safe_json(metadata),
            dna,
            _now(),
        ),
    )
    conn.commit()
    _log(conn, "compress", item_type, shortcode, f"chars={len(text)}, keywords={len(keywords)}")

    return {
        "shortcode": shortcode,
        "item_type": item_type,
        "source_id": source_id,
        "title": title or summary[:40],
        "summary": summary,
        "keywords": keywords,
        "content_hash": content_hash,
        "dna": dna,
        "metadata": metadata,
    }


def compress_skill(conn: sqlite3.Connection, skill_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """压缩一个技能文件（SKILL.md 或 .py）。"""
    if not skill_path.exists():
        return None

    text = skill_path.read_text(encoding="utf-8")
    title = skill_path.stem
    source_id = str(skill_path)

    # SKILL.md 用所在目录名作为来源标识
    if skill_path.name == "SKILL.md":
        source_id = skill_path.parent.name
        title = skill_path.parent.name
        # 尝试从 SKILL.md 提取标题
        m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        if m:
            title = m.group(1).strip()

    return compress_text(conn, text, "skill", source_id, title)


def compress_context(conn: sqlite3.Connection, text: str, title: str = "") -> Dict[str, Any]:
    """压缩一段上下文/对话。"""
    return compress_text(conn, text, "context", f"ctx-{_content_hash(text)}", title)


def build_vector_index(conn: sqlite3.Connection) -> Tuple[int, int]:
    """为所有压缩项生成 TF-IDF 向量。"""
    rows = conn.execute(
        "SELECT id, title, summary, keywords FROM compressed_items"
    ).fetchall()

    if not rows:
        return 0, 0

    ids = []
    texts = []
    for rid, title, summary, keywords in rows:
        kw_list = json.loads(keywords or "[]")
        text_parts = [title or "", summary or ""] + kw_list
        texts.append(" ".join(text_parts))
        ids.append(rid)

    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(2, 4),
        max_features=2048,
    )
    X = vectorizer.fit_transform(texts)

    np.savez(
        VECTOR_CACHE_PATH,
        ids=np.array(ids, dtype=np.int64),
        matrix=X.toarray().astype(np.float32),
    )
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    _log(conn, "build_index", "all", "INDEX", f"items={len(ids)}, dim={X.shape[1]}")
    return len(ids), X.shape[1]


def search_similar(conn: sqlite3.Connection, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """用向量语义搜索压缩项。"""
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
        rid = int(ids[idx])
        row = conn.execute(
            "SELECT item_type, shortcode, title, summary, keywords, dna FROM compressed_items WHERE id=?",
            (rid,),
        ).fetchone()
        if row:
            results.append({
                "item_type": row[0],
                "shortcode": row[1],
                "title": row[2],
                "summary": row[3],
                "keywords": json.loads(row[4] or "[]"),
                "dna": row[5],
                "score": round(float(sims[idx]), 4),
            })
    return results


def recall_by_shortcode(conn: sqlite3.Connection, shortcode: str) -> Optional[Dict[str, Any]]:
    """通过短码召回压缩项。"""
    row = conn.execute(
        "SELECT item_type, source_id, shortcode, title, summary, keywords, metadata, dna, created_at FROM compressed_items WHERE shortcode=?",
        (shortcode,),
    ).fetchone()
    if not row:
        return None
    return {
        "item_type": row[0],
        "source_id": row[1],
        "shortcode": row[2],
        "title": row[3],
        "summary": row[4],
        "keywords": json.loads(row[5] or "[]"),
        "metadata": json.loads(row[6] or "{}"),
        "dna": row[7],
        "created_at": row[8],
    }


def list_items(conn: sqlite3.Connection, item_type: Optional[str] = None) -> List[Dict[str, Any]]:
    sql = "SELECT item_type, shortcode, title, summary, keywords, dna FROM compressed_items"
    params = ()
    if item_type:
        sql += " WHERE item_type=?"
        params = (item_type,)
    sql += " ORDER BY created_at DESC"
    rows = conn.execute(sql, params).fetchall()
    return [
        {
            "item_type": r[0],
            "shortcode": r[1],
            "title": r[2],
            "summary": r[3],
            "keywords": json.loads(r[4] or "[]"),
            "dna": r[5],
        }
        for r in rows
    ]


def compress_all_skills(conn: sqlite3.Connection) -> int:
    """扫描并压缩所有技能文件。"""
    count = 0
    skill_roots = [
        ROOT / "skills",
        HOME / ".kimi-code" / "skills",
        HOME / ".agents" / "skills",
    ]

    for root in skill_roots:
        if not root.exists():
            continue
        for skill_md in root.rglob("SKILL.md"):
            try:
                compress_skill(conn, skill_md)
                count += 1
            except Exception as e:
                print(f"⚠️ 压缩失败 {skill_md}: {e}")

    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="龍魂认知压缩引擎")
    parser.add_argument("--compress-skill", type=str, help="压缩单个技能文件路径")
    parser.add_argument("--compress-context", type=str, help="压缩上下文文本")
    parser.add_argument("--compress-all-skills", action="store_true", help="压缩所有技能")
    parser.add_argument("--recall", type=str, help="通过短码召回")
    parser.add_argument("--search", type=str, help="语义搜索")
    parser.add_argument("--list", action="store_true", help="列出所有压缩项")
    parser.add_argument("--index", action="store_true", help="重建向量索引")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    conn = init_db()

    if args.compress_skill:
        result = compress_skill(conn, pathlib.Path(args.compress_skill))
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("文件不存在")

    if args.compress_context:
        result = compress_context(conn, args.compress_context, "手动上下文")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    if args.compress_all_skills:
        print("🐉 开始压缩所有技能...")
        n = compress_all_skills(conn)
        print(f"压缩完成: {n} 个技能")
        n_idx, dim = build_vector_index(conn)
        print(f"向量索引: {n_idx} 项, 维度 {dim}")

    if args.index:
        n, dim = build_vector_index(conn)
        print(f"向量索引: {n} 项, 维度 {dim}")

    if args.recall:
        result = recall_by_shortcode(conn, args.recall)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"短码 {args.recall} 未找到")

    if args.search:
        results = search_similar(conn, args.search, args.top_k)
        print(json.dumps({"query": args.search, "results": results}, ensure_ascii=False, indent=2))

    if args.list:
        items = list_items(conn)
        print(json.dumps(items, ensure_ascii=False, indent=2))

    if not any([
        args.compress_skill, args.compress_context, args.compress_all_skills,
        args.recall, args.search, args.list, args.index,
    ]):
        print(__doc__)
        print(f"\n当前压缩项数: {conn.execute('SELECT COUNT(*) FROM compressed_items').fetchone()[0]}")

    conn.close()


if __name__ == "__main__":
    main()
