# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · LU 认知压缩与全文还原引擎
Longhun LU Compression & Restoration Engine

DNA:#龍芯⚡️2026-06-30-LONGHUN-LU-COMPRESS-FILE1-v1.0

LU（Long-form → Unified token）是 UID9622 首创的认知压缩符号：
  把长文本（对话、论文、技能、记忆）压成一个短码 + 一句摘要 + 一个 DNA，
  需要时通过短码或 DNA 还原文本，并返回完整的压缩-还原血缘链。

核心能力：
  1. 压缩：输入任意长文本 → 输出 LU 短码、DNA、认知卡片、骨架、关键词。
  2. 还原：输入 LU 短码或 DNA → 返回原始全文 + 卡片 + 操作血缘。
  3. 检索：关键词/语义搜索已压缩记忆。
  4. 接入：语义闸、DNA 主权、知识图谱、视觉卡片。

数据原则：
  - 原始文本 append-only，永不删除。
  - 错误/失败记录也保留，只打标签。
  - 所有压缩/还原操作写入 lineage 血缘日志。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import secrets
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------- 路径 ----------
HOME = Path.home()
LU_ROOT = HOME / ".longhun" / "lu_memory"
LU_DB_PATH = LU_ROOT / "lu_memory.db"
LU_FULLTEXT_DIR = LU_ROOT / "fulltexts"
KG_DB_PATH = HOME / "longhun-system" / "brain" / "unified_kg.db"
CARDS_DIR = LU_ROOT / "cards"

DNA_PREFIX = "#龍芯⚡️"
LU_PREFIX = "LU"

# ---------- 停用词 ----------
STOPWORDS = set(
    "的 了 和 是 在 我 有 就 不 人 都 一 一个 上 也 很 到 说 要 去 你 会 着 没有 看 好 自己 这 那 我们 可以 这个 这些 为 之 与 而 及 以 于 被 把 给 让 向 从 对 将 等 吗 呢 吧 啊 哦 嗯".split()
    + "the a an is are was were be been have has had do does did will would could should may might must can shall".split()
)


# ---------- 通用工具 ----------
def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _dna(event_type: str, seed: str = "") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = hashlib.sha256(f"{event_type}|{seed}|{ts}".encode("utf-8")).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{ts}-{event_type}-{h}"


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _short_hash(text: str, length: int = 6) -> str:
    return _content_hash(text)[:length].upper()


def _safe_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, default=str)


def _extract_topic_slug(text: str, title: str = "") -> str:
    """从标题或正文提取 2-4 个字的主题词，用于 LU 短码可读部分。"""
    source = (title or text).strip()
    # 优先取标题里的中文词
    terms = re.findall(r"[\u4e00-\u9fff]{2,8}", source)
    terms = [t for t in terms if t not in STOPWORDS and len(t) >= 2]
    if terms:
        return terms[0][:4]
    #  fallback：英文单词
    en_terms = re.findall(r"[A-Za-z][A-Za-z0-9_]{2,20}", source)
    if en_terms:
        return en_terms[0][:12]
    return "记忆"


def _generate_lu_code(text: str, title: str = "") -> str:
    """生成 LU 短码：/LU-<日期>-<主题词>-<内容哈希4位>。"""
    date = datetime.now(timezone.utc).strftime("%y%m%d")
    topic = _extract_topic_slug(text, title)
    topic = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9_-]", "", topic)[:8]
    h = _short_hash(text, 4)
    return f"/{LU_PREFIX}-{date}-{topic}-{h}"


def _extract_skeleton(content: str) -> Dict[str, Any]:
    """提取问题/方案/关键点/下一步/背景骨架（兼容 LU 指令体系）。"""
    lines = [l.strip() for l in content.splitlines() if l.strip()]
    skeleton = {
        "problem": "",
        "solution": "",
        "key_points": [],
        "next_action": "",
        "context": "",
    }
    section = "context"
    for line in lines[:200]:  # 限制扫描行数，避免超大文本
        lower = line.lower()
        if any(kw in line for kw in ["问题", "Problem", "Issue", "错误", "痛点"]):
            section = "problem"
            continue
        if any(kw in line for kw in ["方案", "Solution", "解决", "方法", "策略"]):
            section = "solution"
            continue
        if any(kw in line for kw in ["下一步", "Next", "Action", "TODO", "待办"]):
            section = "next_action"
            continue
        if line.startswith(("-", "*", "•", "1.", "2.", "3.", "4.", "5.")) and section in ("solution", "context"):
            cleaned = re.sub(r"^[-*•\d\.\s]+", "", line)
            if len(cleaned) > 4:
                skeleton["key_points"].append(cleaned)
            continue
        if section == "problem":
            skeleton["problem"] += line + "\n"
        elif section == "solution":
            skeleton["solution"] += line + "\n"
        elif section == "next_action":
            skeleton["next_action"] += line + "\n"
        else:
            skeleton["context"] += line + "\n"

    for key in ("problem", "solution", "next_action", "context"):
        skeleton[key] = skeleton[key].strip()[:500]
    skeleton["key_points"] = skeleton["key_points"][:8]
    return skeleton


def _generate_summary(text: str, title: str = "", max_len: int = 120) -> str:
    if title:
        return title[:max_len]
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines[:10]:
        if line.startswith(("#", "```", "[", "-", "*")):
            continue
        cleaned = re.sub(r"\[.*?\]\(.*?\)", "", line).strip("*-· ")
        if len(cleaned) > 10:
            return cleaned[:max_len]
    terms = _extract_chinese_terms(text, top_k=5)
    if terms:
        return "关于" + "、".join([t[0] for t in terms[:5]]) + "的内容"
    return text[:max_len].replace("\n", " ")


def _extract_chinese_terms(text: str, top_k: int = 12) -> List[Tuple[str, int]]:
    terms: Dict[str, int] = {}
    for m in re.finditer(r"[\u4e00-\u9fff]{2,8}", text):
        term = m.group(0)
        if len(term) >= 2 and term not in STOPWORDS:
            terms[term] = terms.get(term, 0) + 1
    return sorted(terms.items(), key=lambda x: x[1], reverse=True)[:top_k]


def _extract_english_terms(text: str, top_k: int = 8) -> List[Tuple[str, int]]:
    terms: Dict[str, int] = {}
    for m in re.finditer(r"[A-Za-z][A-Za-z0-9_]{1,30}", text):
        term = m.group(0).lower()
        if term not in STOPWORDS and len(term) > 2:
            terms[term] = terms.get(term, 0) + 1
    return sorted(terms.items(), key=lambda x: x[1], reverse=True)[:top_k]


def _extract_keywords(text: str) -> List[str]:
    cn = _extract_chinese_terms(text)
    en = _extract_english_terms(text)
    keywords = [t[0] for t in cn] + [t[0] for t in en]
    return list(dict.fromkeys(keywords))[:15]


def _generate_card(record: Dict[str, Any]) -> str:
    """生成 Markdown 认知压缩卡。"""
    sk = record.get("skeleton", {})
    one_liner = record.get("summary", "")[:100]
    key_points = sk.get("key_points", [])
    return f"""【LU 认知压缩卡】

**标题**: {record.get('title') or one_liner}
**来源**: {record.get('source', 'manual')}
**LU 短码**: `{record.get('lu_code', '-')}`
**DNA**: `{record.get('dna', '-')}`
**时间**: {record.get('created_at', '-')}
**操作人**: {record.get('operator', 'UID9622')}
**状态**: {record.get('status', 'active')}

---

## 一｜一句话压缩
{one_liner}

## 二｜核心骨架
- **背景**：{sk.get('context') or '（暂无）'}
- **问题**：{sk.get('problem') or '（暂无）'}
- **方案**：{sk.get('solution') or '（暂无）'}
- **下一步**：{sk.get('next_action') or '（暂无）'}

## 三｜关键点
{chr(10).join(f'- {p}' for p in key_points) or '- （暂无）'}

## 四｜元数据
- 原始长度：{record.get('char_count', 0)} 字符
- 关键词：{', '.join(record.get('keywords', []))}
- 语义闸判定：{record.get('gate_decision', 'QUARANTINE')}
- 压缩模式：{record.get('mode', 'balanced')}

---
*LU = Long-form → Unified token · UID9622 首创*
"""


def _load_module_safely(module_name: str, path: Path):
    """安全加载项目内模块，失败返回 None。"""
    try:
        if str(path.parent) not in sys.path:
            sys.path.insert(0, str(path.parent))
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, str(path))
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    except Exception:
        pass
    return None


# ---------- 引擎 ----------
class LonghunLuMemoryEngine:
    """LU 认知压缩 / 还原 / 检索 / 图谱接入引擎。"""

    def __init__(
        self,
        db_path: Path = LU_DB_PATH,
        founder: str = "UID9622",
    ) -> None:
        self.db_path = db_path
        self.founder = founder
        self.fulltext_dir = LU_FULLTEXT_DIR
        self.cards_dir = CARDS_DIR
        self.fulltext_dir.mkdir(parents=True, exist_ok=True)
        self.cards_dir.mkdir(parents=True, exist_ok=True)
        self._conn = self._init_db()
        self._gate = None
        self._dna_engine = None
        self._kg_conn = None
        self._load_plugins()

    def _load_plugins(self) -> None:
        # 语义闸
        gate_path = HOME / "longhun-system" / "scripts" / "龍魂語義歸一化閘門.py"
        gate_mod = _load_module_safely("semantic_gate", gate_path)
        if gate_mod:
            try:
                self._gate = gate_mod.KnowledgeBaseGate()
            except Exception:
                pass
        # DNA 主权引擎
        dna_path = HOME / "longhun-system" / "scripts" / "龍魂DNA主權引擎.py"
        dna_mod = _load_module_safely("dna_sovereignty", dna_path)
        if dna_mod:
            try:
                self._dna_engine = dna_mod.DnaSovereigntyEngine()
            except Exception:
                pass
        # 知识图谱库
        if KG_DB_PATH.exists():
            try:
                self._kg_conn = sqlite3.connect(str(KG_DB_PATH))
                self._kg_conn.execute("PRAGMA foreign_keys = ON")
            except Exception:
                self._kg_conn = None

    def _init_db(self) -> sqlite3.Connection:
        LU_ROOT.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS lu_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lu_code TEXT UNIQUE NOT NULL,
                dna TEXT UNIQUE NOT NULL,
                title TEXT,
                summary TEXT,
                keywords TEXT,
                skeleton TEXT,
                content_hash TEXT NOT NULL,
                fulltext_path TEXT NOT NULL,
                char_count INTEGER DEFAULT 0,
                word_count INTEGER DEFAULT 0,
                mode TEXT DEFAULT 'balanced',
                source TEXT DEFAULT 'manual',
                operator TEXT DEFAULT 'UID9622',
                status TEXT DEFAULT 'active',
                gate_decision TEXT DEFAULT 'QUARANTINE',
                gate_dna TEXT,
                kg_node_id TEXT,
                card_path TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_lu_code ON lu_records(lu_code)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_dna ON lu_records(dna)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_status ON lu_records(status)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_source ON lu_records(source)")
        # 迁移：老数据库可能没有这两个字段
        try:
            conn.execute("ALTER TABLE lu_records ADD COLUMN kg_node_id TEXT")
        except sqlite3.OperationalError:
            pass
        try:
            conn.execute("ALTER TABLE lu_records ADD COLUMN card_path TEXT")
        except sqlite3.OperationalError:
            pass

        conn.execute("""
            CREATE TABLE IF NOT EXISTS lu_lineage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lu_code TEXT NOT NULL,
                dna TEXT NOT NULL,
                action TEXT NOT NULL,
                operator TEXT,
                detail TEXT,
                timestamp TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_lineage_code ON lu_lineage(lu_code)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_lineage_dna ON lu_lineage(dna)")

        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS lu_fts USING fts5(
                lu_code, title, summary, keywords, content UNINDEXED,
                tokenize='trigram'
            )
        """)
        conn.commit()
        return conn

    def _write_fulltext(self, lu_code: str, text: str) -> Path:
        safe = re.sub(r"[^\w\-]", "_", lu_code.replace("/", ""))[:80]
        path = self.fulltext_dir / f"{safe}.txt"
        path.write_text(text, encoding="utf-8")
        return path

    def _read_fulltext(self, path: Path) -> str:
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8", errors="replace")

    def _log_lineage(self, lu_code: str, dna: str, action: str, operator: str, detail: str = "") -> None:
        self._conn.execute(
            "INSERT INTO lu_lineage(lu_code, dna, action, operator, detail, timestamp) VALUES(?,?,?,?,?,?)",
            (lu_code, dna, action, operator, detail, _now()),
        )
        self._conn.commit()

    def _gate_check(self, text: str, operator: str, metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if self._gate:
            try:
                return self._gate.evaluate(
                    content=text,
                    source="lu_compression",
                    operator=operator,
                    metadata=metadata,
                )
            except Exception:
                pass
        return {
            "ok": True,
            "decision": "ADMIT",
            "reason": "语义闸未加载，默认准入",
            "dna": _dna("LU-GATE-FALLBACK"),
        }

    def _record_contribution(self, dna: str, operator: str, char_count: int) -> None:
        if self._dna_engine:
            try:
                self._dna_engine.record_contribution(
                    dna_identity=dna,
                    category="lu_memory_compression",
                    description=f"LU 压缩 {char_count} 字符",
                    value=char_count,
                    operator=operator,
                )
            except Exception:
                pass

    def _add_to_kg(self, record: Dict[str, Any]) -> Optional[str]:
        if not self._kg_conn:
            return None
        try:
            # 注册来源
            self._kg_conn.execute(
                "INSERT OR REPLACE INTO sources(id, name, description, record_count, last_synced_at) VALUES(?,?,?,?,?)",
                ("lu_memory", "LU 认知压缩记忆", "Longhun LU Compression Memory", 0, _now()),
            )
            node_id = f"lu:{record['lu_code']}"
            content_preview = record.get("summary", "") + "\n" + " ".join(record.get("keywords", []))
            self._kg_conn.execute(
                """INSERT OR REPLACE INTO nodes
                   (id, source, source_id, label, node_type, content, metadata, dna, created_at, updated_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (
                    node_id,
                    "lu_memory",
                    record["lu_code"],
                    record.get("title") or record.get("summary", "")[:40],
                    "lu_memory",
                    content_preview,
                    _safe_json({
                        "lu_code": record["lu_code"],
                        "keywords": record.get("keywords", []),
                        "mode": record.get("mode"),
                        "gate_decision": record.get("gate_decision"),
                    }),
                    record["dna"],
                    record.get("created_at", _now()),
                    _now(),
                ),
            )
            # 关键词边
            for kw in record.get("keywords", [])[:10]:
                kw_id = f"lu_kw:{kw}"
                self._kg_conn.execute(
                    "INSERT OR REPLACE INTO nodes(id, source, source_id, label, node_type, content, metadata, dna, created_at, updated_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (kw_id, "lu_memory", f"kw:{kw}", kw, "keyword", f"关键词：{kw}", "{}", record["dna"], _now(), _now()),
                )
                self._kg_conn.execute(
                    "INSERT OR REPLACE INTO edges(source_node, target_node, relation, weight, metadata, dna) VALUES(?,?,?,?,?,?)",
                    (node_id, kw_id, "has_keyword", 1.0, "{}", _dna("LU-EDGE")),
                )
            self._kg_conn.commit()
            return node_id
        except Exception:
            return None

    def compress(
        self,
        text: str,
        title: str = "",
        source: str = "manual",
        operator: str = "UID9622",
        mode: str = "balanced",
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """压缩一段长文本，返回 LU 短码、DNA、卡片。"""
        if not text or len(text.strip()) < 10:
            return {"ok": False, "code": "TEXT_TOO_SHORT", "message": "文本过短，无法压缩"}

        # 1. 语义闸
        gate_result = self._gate_check(text, operator, {"mode": mode, "source": source})
        if gate_result.get("decision") == "REJECT":
            # 仍记录到失败/隔离表，但不上架
            fail_dna = _dna("LU-REJECTED", _content_hash(text))
            self._log_lineage("REJECTED", fail_dna, "compress_rejected", operator, gate_result.get("reason", ""))
            return {
                "ok": False,
                "code": "GATE_REJECTED",
                "message": f"🔴 语义闸熔断：{gate_result.get('reason')}",
                "gate": gate_result,
            }

        # 2. 生成短码与 DNA
        lu_code = _generate_lu_code(text, title)
        content_hash = _content_hash(text)
        dna = _dna("LU-COMPRESS", content_hash)
        created_at = _now()

        # 3. 摘要与骨架
        summary = _generate_summary(text, title)
        keywords = _extract_keywords(text)
        skeleton = _extract_skeleton(text)
        char_count = len(text)
        word_count = len(re.findall(r"[\u4e00-\u9fff]", text))

        # 4. 持久化全文
        fulltext_path = self._write_fulltext(lu_code, text)

        # 5. 构建记录
        record: Dict[str, Any] = {
            "lu_code": lu_code,
            "dna": dna,
            "title": title or summary[:40],
            "summary": summary,
            "keywords": keywords,
            "skeleton": skeleton,
            "content_hash": content_hash,
            "fulltext_path": str(fulltext_path),
            "char_count": char_count,
            "word_count": word_count,
            "mode": mode,
            "source": source,
            "operator": operator,
            "status": "active",
            "gate_decision": gate_result.get("decision", "QUARANTINE"),
            "gate_dna": gate_result.get("dna", ""),
            "tags": list(tags or []),
            "created_at": created_at,
            "updated_at": created_at,
        }

        # 6. 写入数据库
        try:
            self._conn.execute(
                """INSERT INTO lu_records
                   (lu_code, dna, title, summary, keywords, skeleton, content_hash, fulltext_path,
                    char_count, word_count, mode, source, operator, status, gate_decision, gate_dna,
                    kg_node_id, card_path, created_at, updated_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    record["lu_code"],
                    record["dna"],
                    record["title"],
                    record["summary"],
                    _safe_json(record["keywords"]),
                    _safe_json(record["skeleton"]),
                    record["content_hash"],
                    record["fulltext_path"],
                    record["char_count"],
                    record["word_count"],
                    record["mode"],
                    record["source"],
                    record["operator"],
                    record["status"],
                    record["gate_decision"],
                    record["gate_dna"],
                    None,
                    None,
                    record["created_at"],
                    record["updated_at"],
                ),
            )
            self._conn.execute(
                "INSERT INTO lu_fts(lu_code, title, summary, keywords, content) VALUES(?,?,?,?,?)",
                (lu_code, record["title"], summary, " ".join(keywords), text[:8000]),
            )
            self._conn.commit()
        except sqlite3.IntegrityError as e:
            return {"ok": False, "code": "DUPLICATE", "message": f"LU 短码或 DNA 已存在：{e}"}

        # 7. 血缘 / DNA 贡献 / 图谱
        self._log_lineage(lu_code, dna, "compress", operator, f"chars={char_count},gate={record['gate_decision']}")
        self._record_contribution(dna, operator, char_count)
        kg_node_id = self._add_to_kg(record)
        record["kg_node_id"] = kg_node_id
        if kg_node_id:
            self._conn.execute("UPDATE lu_records SET kg_node_id=? WHERE lu_code=?", (kg_node_id, lu_code))
            self._conn.commit()

        # 8. 认知卡片：Markdown + 视觉卡片
        record["card"] = _generate_card(record)
        try:
            card_path = self.generate_visual_card(lu_code)
            if card_path:
                record["card_path"] = str(card_path)
                self._conn.execute("UPDATE lu_records SET card_path=? WHERE lu_code=?", (str(card_path), lu_code))
                self._conn.commit()
        except Exception:
            pass

        return {"ok": True, "code": "COMPRESSED", "message": f"🟢 已压缩为 {lu_code}", "record": record}

    def recall(self, handle: str, operator: str = "UID9622") -> Dict[str, Any]:
        """通过 LU 短码或 DNA 还原全文与血缘。"""
        handle = handle.strip()
        row = None
        if handle.startswith("/LU-"):
            row = self._conn.execute(
                "SELECT * FROM lu_records WHERE lu_code=?", (handle,)
            ).fetchone()
        if not row and handle.startswith(DNA_PREFIX):
            row = self._conn.execute(
                "SELECT * FROM lu_records WHERE dna=?", (handle,)
            ).fetchone()
        # 模糊匹配短码
        if not row:
            row = self._conn.execute(
                "SELECT * FROM lu_records WHERE lu_code LIKE ? ORDER BY created_at DESC LIMIT 1",
                (f"%{handle}%",),
            ).fetchone()

        if not row:
            return {"ok": False, "code": "NOT_FOUND", "message": f"未找到 {handle} 对应的 LU 记忆"}

        record = dict(row)
        record["keywords"] = json.loads(record.get("keywords") or "[]")
        record["skeleton"] = json.loads(record.get("skeleton") or "{}")
        record["fulltext"] = self._read_fulltext(Path(record["fulltext_path"]))
        record["card"] = _generate_card(record)

        # 血缘
        lineage = self._conn.execute(
            "SELECT action, operator, detail, timestamp FROM lu_lineage WHERE lu_code=? ORDER BY timestamp DESC LIMIT 50",
            (record["lu_code"],),
        ).fetchall()
        record["lineage"] = [dict(r) for r in lineage]

        self._log_lineage(record["lu_code"], record["dna"], "recall", operator, f"handle={handle}")
        return {"ok": True, "code": "RECALLED", "message": f"🟢 已还原 {record['lu_code']}", "record": record}

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """关键词搜索（FTS5）。"""
        try:
            rows = self._conn.execute(
                """SELECT r.lu_code, r.dna, r.title, r.summary, r.keywords, r.status, r.created_at,
                          snippet(lu_fts, 1, '**', '**', '…', 40) AS snippet
                   FROM lu_fts
                   JOIN lu_records r ON r.lu_code = lu_fts.lu_code
                   WHERE lu_fts MATCH ?
                   ORDER BY rank
                   LIMIT ?""",
                (query, limit),
            ).fetchall()
        except sqlite3.OperationalError:
            rows = []
        if not rows:
            # fallback LIKE
            rows = self._conn.execute(
                """SELECT lu_code, dna, title, summary, keywords, status, created_at, '' AS snippet
                   FROM lu_records
                   WHERE title LIKE ? OR summary LIKE ? OR keywords LIKE ?
                   ORDER BY created_at DESC LIMIT ?""",
                (f"%{query}%", f"%{query}%", f"%{query}%", limit),
            ).fetchall()
        return [dict(r) for r in rows]

    def search_semantic(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """基于 TF-IDF 字符 n-gram 的语义相似度搜索（中文 fallback）。"""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
        except Exception:
            # 没有 sklearn 时退化到关键词搜索
            return self.search(query, limit=limit)

        rows = self._conn.execute(
            "SELECT lu_code, dna, title, summary, keywords, fulltext_path, status, created_at "
            "FROM lu_records WHERE status='active'"
        ).fetchall()
        if not rows:
            return []

        records = [dict(r) for r in rows]

        def _doc(rec: Dict[str, Any]) -> str:
            try:
                kw = json.loads(rec.get("keywords") or "[]")
            except Exception:
                kw = []
            text = self._read_fulltext(Path(rec["fulltext_path"]))
            parts = [
                rec.get("title") or "",
                rec.get("summary") or "",
                " ".join(kw),
                text[:800],
            ]
            return " ".join(p for p in parts if p)

        corpus = [_doc(r) for r in records]
        try:
            vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
            X = vectorizer.fit_transform(corpus)
            q_vec = vectorizer.transform([query])
            scores = cosine_similarity(q_vec, X).flatten()
        except Exception:
            return self.search(query, limit=limit)

        indexed = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        results = []
        for idx, score in indexed[:limit]:
            if score <= 0:
                continue
            rec = records[idx]
            rec["semantic_score"] = round(float(score), 4)
            results.append(rec)
        return results

    def list_recent(self, limit: int = 20, status: Optional[str] = None) -> List[Dict[str, Any]]:
        sql = "SELECT lu_code, dna, title, summary, keywords, status, created_at FROM lu_records"
        params: Tuple[Any, ...] = ()
        if status:
            sql += " WHERE status=?"
            params = (status,)
        sql += " ORDER BY created_at DESC LIMIT ?"
        params += (limit,)
        rows = self._conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def generate_visual_card(self, lu_code: str, output_path: Optional[Path] = None) -> Optional[Path]:
        """生成视觉知识卡片（依赖 longhun_kb.render_card）。"""
        try:
            kb_path = HOME / "longhun-system" / "scripts" / "longhun_kb.py"
            kb_mod = _load_module_safely("longhun_kb", kb_path)
            if not kb_mod or not hasattr(kb_mod, "render_card"):
                return None

            row = self._conn.execute(
                "SELECT lu_code, title, summary, dna, fulltext_path FROM lu_records WHERE lu_code=?", (lu_code,)
            ).fetchone()
            if not row:
                return None
            record = dict(row)
            text = self._read_fulltext(Path(record["fulltext_path"]))
            excerpt = text[:300].replace("#", "").replace("\n", " ")
            out = output_path or self.cards_dir / f"{lu_code.replace('/', '')}.png"
            page_id = record["lu_code"].replace("/", "")
            kb_mod.render_card(
                page_id=page_id,
                title=record["title"] or record["summary"] or "LU记忆",
                category="LU压缩记忆",
                dna=record["dna"],
                excerpt=excerpt,
                output_path=out,
                calligraphy=False,
            )
            return out
        except Exception:
            return None

    def stats(self) -> Dict[str, Any]:
        total = self._conn.execute("SELECT COUNT(*) FROM lu_records").fetchone()[0]
        active = self._conn.execute("SELECT COUNT(*) FROM lu_records WHERE status='active'").fetchone()[0]
        chars = self._conn.execute("SELECT COALESCE(SUM(char_count),0) FROM lu_records").fetchone()[0]
        lineage = self._conn.execute("SELECT COUNT(*) FROM lu_lineage").fetchone()[0]
        return {
            "total_records": total,
            "active_records": active,
            "total_chars": chars,
            "lineage_events": lineage,
            "db_path": str(self.db_path),
            "dna": _dna("LU-STATS"),
        }

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None
        if self._kg_conn:
            self._kg_conn.close()
            self._kg_conn = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


# ---------- 命令行 ----------
def main() -> None:
    parser = argparse.ArgumentParser(description="龍魂 LU 认知压缩与还原引擎")
    parser.add_argument("--compress", "-c", type=str, help="要压缩的文本（或文件路径，前缀 file:）")
    parser.add_argument("--title", "-t", type=str, default="", help="标题")
    parser.add_argument("--source", "-s", type=str, default="cli", help="来源标识")
    parser.add_argument("--mode", "-m", type=str, default="balanced", help="压缩模式")
    parser.add_argument("--recall", "-r", type=str, help="LU 短码或 DNA 还原")
    parser.add_argument("--search", type=str, help="关键词搜索（FTS5）")
    parser.add_argument("--semantic", type=str, help="语义搜索（TF-IDF 字符 n-gram）")
    parser.add_argument("--list", action="store_true", help="列出最近压缩")
    parser.add_argument("--stats", action="store_true", help="统计")
    parser.add_argument("--card", type=str, help="为指定 LU 短码生成视觉卡片")
    args = parser.parse_args()

    engine = LonghunLuMemoryEngine()

    if args.compress:
        text = args.compress
        if text.startswith("file:"):
            path = Path(text[5:])
            text = path.read_text(encoding="utf-8", errors="replace")
        result = engine.compress(text, title=args.title, source=args.source, mode=args.mode)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        if result.get("ok") and result.get("record"):
            print("\n" + result["record"].get("card", ""))

    elif args.recall:
        result = engine.recall(args.recall)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

    elif args.search:
        results = engine.search(args.search)
        print(json.dumps({"query": args.search, "results": results}, ensure_ascii=False, indent=2, default=str))

    elif args.semantic:
        results = engine.search_semantic(args.semantic)
        print(json.dumps({"query": args.semantic, "results": results}, ensure_ascii=False, indent=2, default=str))

    elif args.list:
        results = engine.list_recent()
        print(json.dumps(results, ensure_ascii=False, indent=2, default=str))

    elif args.stats:
        print(json.dumps(engine.stats(), ensure_ascii=False, indent=2, default=str))

    elif args.card:
        path = engine.generate_visual_card(args.card)
        print(json.dumps({"ok": bool(path), "path": str(path)}, ensure_ascii=False, indent=2, default=str))

    else:
        print(__doc__)
        print("\n当前统计：", json.dumps(engine.stats(), ensure_ascii=False, indent=2, default=str))

    engine.close()


if __name__ == "__main__":
    main()
