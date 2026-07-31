# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 集思广益引擎

"集思广益"不是口号，是可执行、可追溯、可迭代的机制：
  - 集思：让意见有路可进，先归档，不判断对错。
  - 广益：系统按权重过滤、排序、标记，让对系统有益的意见自然浮现。

DNA:#龍芯⚡️2026-06-30-LONGHUN-COLLECTIVE-WISDOM-FILE1-v1.0
"""

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

HOME = Path.home()
CW_ROOT = HOME / ".longhun" / "collective_wisdom"
CW_DB = CW_ROOT / "collective_wisdom.db"
DNA_PREFIX = "#龍芯⚡️"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _dna(event: str, seed: str = "") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = hashlib.sha256(f"{event}|{seed}|{ts}".encode("utf-8")).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{ts}-{event}-{h}"


def _short_hash(text: str, length: int = 6) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length].upper()


def _safe_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, default=str)


def _load_module_safely(module_name: str, path: Path):
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


class CollectiveWisdomEngine:
    """
    集思广益引擎。
    """

    # 等级权重
    _LEVEL_WEIGHT = {"L0": 0.0, "L1": 0.5, "L2": 1.0, "L2-SP": 1.0, "L3": 2.0}

    def __init__(self, db_path: Path = CW_DB, founder: str = "UID9622") -> None:
        self.db_path = db_path
        self.founder = founder
        CW_ROOT.mkdir(parents=True, exist_ok=True)
        self._conn = self._init_db()
        self._gate = None
        self._dna_engine = None
        self._kg_conn = None
        self._lu_engine = None
        self._load_plugins()

    def _load_plugins(self) -> None:
        gate_path = HOME / "longhun-system" / "scripts" / "龍魂語義歸一化閘門.py"
        gate_mod = _load_module_safely("semantic_gate", gate_path)
        if gate_mod:
            try:
                self._gate = gate_mod.KnowledgeBaseGate()
            except Exception:
                pass

        dna_path = HOME / "longhun-system" / "scripts" / "龍魂DNA主權引擎.py"
        dna_mod = _load_module_safely("dna_sovereignty", dna_path)
        if dna_mod:
            try:
                self._dna_engine = dna_mod.DnaSovereigntyEngine()
            except Exception:
                pass

        kg_path = HOME / "longhun-system" / "brain" / "unified_kg.db"
        if kg_path.exists():
            try:
                self._kg_conn = sqlite3.connect(str(kg_path))
                self._kg_conn.execute("PRAGMA foreign_keys = ON")
            except Exception:
                self._kg_conn = None

        lu_path = HOME / "longhun-system" / "scripts" / "longhun_lu_compress.py"
        lu_mod = _load_module_safely("longhun_lu_compress", lu_path)
        if lu_mod:
            try:
                self._lu_engine = lu_mod.LonghunLuMemoryEngine()
            except Exception:
                self._lu_engine = None

    def _init_db(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_code TEXT UNIQUE NOT NULL,
                dna TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL,
                source TEXT DEFAULT 'user',
                submitter TEXT NOT NULL,
                level TEXT DEFAULT 'L0',
                status TEXT DEFAULT 'archived',
                weight REAL DEFAULT 0.0,
                mention_count INTEGER DEFAULT 1,
                verified_count INTEGER DEFAULT 0,
                gate_decision TEXT DEFAULT 'QUARANTINE',
                gate_dna TEXT,
                lu_code TEXT,
                kg_node_id TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ideas_code ON ideas(idea_code)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ideas_dna ON ideas(dna)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ideas_status ON ideas(status)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ideas_weight ON ideas(weight)")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS idea_mentions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_code TEXT NOT NULL,
                context TEXT,
                submitter TEXT,
                timestamp TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_mentions_code ON idea_mentions(idea_code)")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS idea_lineage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_code TEXT NOT NULL,
                dna TEXT NOT NULL,
                action TEXT NOT NULL,
                operator TEXT,
                detail TEXT,
                timestamp TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_lineage_code ON idea_lineage(idea_code)")

        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS ideas_fts USING fts5(
                idea_code, content UNINDEXED,
                tokenize='trigram'
            )
        """)
        conn.commit()
        return conn

    def _gate_check(self, content: str, submitter: str) -> Dict[str, Any]:
        if self._gate:
            try:
                return self._gate.evaluate(
                    content=content,
                    source="collective_wisdom",
                    operator=submitter,
                    metadata={"cw_idea": True},
                )
            except Exception:
                pass
        return {
            "ok": True,
            "decision": "ADMIT",
            "reason": "语义闸未加载，默认准入",
            "dna": _dna("CW-GATE-FALLBACK"),
        }

    def _log_lineage(self, idea_code: str, dna: str, action: str, operator: str, detail: str = "") -> None:
        self._conn.execute(
            "INSERT INTO idea_lineage(idea_code, dna, action, operator, detail, timestamp) VALUES(?,?,?,?,?,?)",
            (idea_code, dna, action, operator, detail, _now()),
        )
        self._conn.commit()

    def _record_contribution(self, dna: str, operator: str, value: int) -> None:
        if self._dna_engine:
            try:
                self._dna_engine.record_contribution(
                    dna_identity=dna,
                    category="collective_wisdom",
                    description=f"集思广益提交/互动",
                    value=value,
                    operator=operator,
                )
            except Exception:
                pass

    def _add_to_kg(self, record: Dict[str, Any]) -> Optional[str]:
        if not self._kg_conn:
            return None
        try:
            self._kg_conn.execute(
                "INSERT OR REPLACE INTO sources(id, name, description, record_count, last_synced_at) VALUES(?,?,?,?,?)",
                ("collective_wisdom", "集思广益", "Longhun Collective Wisdom", 0, _now()),
            )
            node_id = f"cw:{record['idea_code']}"
            self._kg_conn.execute(
                """INSERT OR REPLACE INTO nodes
                   (id, source, source_id, label, node_type, content, metadata, dna, created_at, updated_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (
                    node_id,
                    "collective_wisdom",
                    "collective_wisdom",
                    record["idea_code"],
                    "idea",
                    record["content"][:500],
                    _safe_json({
                        "submitter": record["submitter"],
                        "level": record["level"],
                        "status": record["status"],
                        "weight": record["weight"],
                    }),
                    record["dna"],
                    record["created_at"],
                    _now(),
                ),
            )
            self._kg_conn.commit()
            return node_id
        except Exception:
            return None

    def _compute_weight(self, level: str, submitter: str, mention_count: int, verified_count: int) -> float:
        level_bonus = self._LEVEL_WEIGHT.get(level, 0.0)
        adopted_history = self._conn.execute(
            "SELECT COUNT(*) FROM ideas WHERE submitter=? AND status='adopted'", (submitter,)
        ).fetchone()[0]
        history_bonus = min(adopted_history * 0.3, 3.0)
        mention_bonus = (mention_count - 1) * 0.2
        verified_bonus = verified_count * 1.0
        return 1.0 + level_bonus + history_bonus + mention_bonus + verified_bonus

    def submit(
        self,
        content: str,
        submitter: str = "UID9622",
        level: str = "L0",
        source: str = "user",
    ) -> Dict[str, Any]:
        """提交一条意见。先归档，不判断对错。"""
        content = content.strip()
        if not content:
            return {"ok": False, "code": "EMPTY", "message": "意见内容不能为空"}

        gate = self._gate_check(content, submitter)
        if gate.get("decision") == "REJECT":
            return {"ok": False, "code": "GATE_REJECTED", "message": f"🔴 语义闸熔断：{gate.get('reason')}"}

        date = datetime.now(timezone.utc).strftime("%y%m%d")
        topic = re.findall(r"[\u4e00-\u9fff]{2,8}", content)
        topic = topic[0][:4] if topic else "意见"
        idea_code = f"/CW-{date}-{topic}-{_short_hash(content, 4)}"
        dna = _dna("CW-IDEA", content)
        created_at = _now()

        record = {
            "idea_code": idea_code,
            "dna": dna,
            "content": content,
            "source": source,
            "submitter": submitter,
            "level": level,
            "status": "archived",
            "mention_count": 1,
            "verified_count": 0,
            "gate_decision": gate.get("decision", "QUARANTINE"),
            "gate_dna": gate.get("dna", ""),
            "lu_code": None,
            "created_at": created_at,
            "updated_at": created_at,
        }
        record["weight"] = self._compute_weight(level, submitter, 1, 0)

        # 压缩为 LU 记忆（可选）
        lu_code = None
        if self._lu_engine:
            try:
                lu_res = self._lu_engine.compress(
                    content,
                    title=f"集思广益：{idea_code}",
                    source="collective_wisdom",
                    operator=submitter,
                )
                if lu_res.get("ok"):
                    lu_code = lu_res["record"]["lu_code"]
                    record["lu_code"] = lu_code
            except Exception:
                pass

        try:
            self._conn.execute(
                """INSERT INTO ideas
                   (idea_code, dna, content, source, submitter, level, status, weight, mention_count, verified_count,
                    gate_decision, gate_dna, lu_code, created_at, updated_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    record["idea_code"],
                    record["dna"],
                    record["content"],
                    record["source"],
                    record["submitter"],
                    record["level"],
                    record["status"],
                    record["weight"],
                    record["mention_count"],
                    record["verified_count"],
                    record["gate_decision"],
                    record["gate_dna"],
                    record["lu_code"],
                    record["created_at"],
                    record["updated_at"],
                ),
            )
            self._conn.execute(
                "INSERT INTO ideas_fts(idea_code, content) VALUES(?,?)",
                (idea_code, content[:4000]),
            )
            self._conn.execute(
                "INSERT INTO idea_mentions(idea_code, context, submitter, timestamp) VALUES(?,?,?,?)",
                (idea_code, "首次提交", submitter, created_at),
            )
            self._conn.commit()
        except sqlite3.IntegrityError as e:
            return {"ok": False, "code": "DUPLICATE", "message": f"意见码已存在：{e}"}

        kg_node_id = self._add_to_kg(record)
        if kg_node_id:
            record["kg_node_id"] = kg_node_id
            self._conn.execute("UPDATE ideas SET kg_node_id=? WHERE idea_code=?", (kg_node_id, idea_code))
            self._conn.commit()

        self._log_lineage(idea_code, dna, "submit", submitter, f"level={level},gate={record['gate_decision']}")
        self._record_contribution(dna, submitter, 1)

        return {"ok": True, "code": "SUBMITTED", "message": f"🟢 意见已归档：{idea_code}", "record": record}

    def mention(self, idea_code: str, submitter: str = "UID9622", context: str = "") -> Dict[str, Any]:
        """再次提到某条意见，mention_count +1，权重重新计算。"""
        row = self._conn.execute("SELECT * FROM ideas WHERE idea_code=?", (idea_code,)).fetchone()
        if not row:
            return {"ok": False, "code": "NOT_FOUND", "message": f"未找到 {idea_code}"}
        rec = dict(row)

        self._conn.execute(
            "INSERT INTO idea_mentions(idea_code, context, submitter, timestamp) VALUES(?,?,?,?)",
            (idea_code, context or "再次提及", submitter, _now()),
        )
        new_count = rec["mention_count"] + 1
        new_weight = self._compute_weight(rec["level"], rec["submitter"], new_count, rec["verified_count"])
        self._conn.execute(
            "UPDATE ideas SET mention_count=?, weight=?, updated_at=? WHERE idea_code=?",
            (new_count, new_weight, _now(), idea_code),
        )
        self._conn.commit()
        self._log_lineage(idea_code, rec["dna"], "mention", submitter, f"count={new_count},weight={new_weight:.2f}")
        return {"ok": True, "code": "MENTIONED", "message": f"🟢 意见被再次提及，当前权重 {new_weight:.2f}", "record": self.get(idea_code)}

    def verify(self, idea_code: str, operator: str = "UID9622") -> Dict[str, Any]:
        """验证某条意见带来可验证改进，verified_count +1。"""
        row = self._conn.execute("SELECT * FROM ideas WHERE idea_code=?", (idea_code,)).fetchone()
        if not row:
            return {"ok": False, "code": "NOT_FOUND", "message": f"未找到 {idea_code}"}
        rec = dict(row)
        new_verified = rec["verified_count"] + 1
        new_weight = self._compute_weight(rec["level"], rec["submitter"], rec["mention_count"], new_verified)
        self._conn.execute(
            "UPDATE ideas SET verified_count=?, weight=?, updated_at=? WHERE idea_code=?",
            (new_verified, new_weight, _now(), idea_code),
        )
        self._conn.commit()
        self._log_lineage(idea_code, rec["dna"], "verify", operator, f"verified={new_verified},weight={new_weight:.2f}")
        return {"ok": True, "code": "VERIFIED", "message": f"🟢 意见已通过验证，当前权重 {new_weight:.2f}", "record": self.get(idea_code)}

    def set_status(self, idea_code: str, status: str, operator: str = "UID9622") -> Dict[str, Any]:
        """决策层设置状态：adopted / rejected / ignored / under_review。"""
        if status not in ("adopted", "rejected", "ignored", "under_review", "archived"):
            return {"ok": False, "code": "BAD_STATUS", "message": f"未知状态：{status}"}
        row = self._conn.execute("SELECT * FROM ideas WHERE idea_code=?", (idea_code,)).fetchone()
        if not row:
            return {"ok": False, "code": "NOT_FOUND", "message": f"未找到 {idea_code}"}
        rec = dict(row)
        self._conn.execute(
            "UPDATE ideas SET status=?, updated_at=? WHERE idea_code=?",
            (status, _now(), idea_code),
        )
        self._conn.commit()
        self._log_lineage(idea_code, rec["dna"], f"status:{status}", operator, "")
        return {"ok": True, "code": "STATUS_UPDATED", "message": f"🟢 意见状态已更新为 {status}", "record": self.get(idea_code)}

    def get(self, idea_code: str) -> Optional[Dict[str, Any]]:
        row = self._conn.execute("SELECT * FROM ideas WHERE idea_code=?", (idea_code,)).fetchone()
        if not row:
            return None
        rec = dict(row)
        rec["lineage"] = [
            dict(r) for r in self._conn.execute(
                "SELECT action, operator, detail, timestamp FROM idea_lineage WHERE idea_code=? ORDER BY timestamp DESC",
                (idea_code,),
            ).fetchall()
        ]
        rec["mentions"] = [
            dict(r) for r in self._conn.execute(
                "SELECT context, submitter, timestamp FROM idea_mentions WHERE idea_code=? ORDER BY timestamp DESC",
                (idea_code,),
            ).fetchall()
        ]
        return rec

    def list_ideas(
        self,
        status: Optional[str] = None,
        submitter: Optional[str] = None,
        sort_by: str = "weight",
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM ideas WHERE 1=1"
        params: List[Any] = []
        if status:
            sql += " AND status=?"
            params.append(status)
        if submitter:
            sql += " AND submitter=?"
            params.append(submitter)
        if sort_by == "weight":
            sql += " ORDER BY weight DESC, created_at DESC"
        elif sort_by == "newest":
            sql += " ORDER BY created_at DESC"
        elif sort_by == "mentions":
            sql += " ORDER BY mention_count DESC, weight DESC"
        else:
            sql += " ORDER BY created_at DESC"
        sql += " LIMIT ?"
        params.append(limit)
        rows = self._conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            rows = self._conn.execute(
                "SELECT idea_code FROM ideas_fts WHERE ideas_fts MATCH ? LIMIT ?",
                (query, limit),
            ).fetchall()
        except sqlite3.OperationalError:
            rows = []
        if rows:
            codes = [r["idea_code"] for r in rows]
            placeholders = ",".join("?" * len(codes))
            rows = self._conn.execute(
                f"SELECT * FROM ideas WHERE idea_code IN ({placeholders})",
                codes,
            ).fetchall()
            return [dict(r) for r in rows]
        # fallback LIKE
        rows = self._conn.execute(
            "SELECT * FROM ideas WHERE content LIKE ? ORDER BY weight DESC LIMIT ?",
            (f"%{query}%", limit),
        ).fetchall()
        return [dict(r) for r in rows]

    def top_ideas(self, limit: int = 10) -> List[Dict[str, Any]]:
        """按权重浮出的置顶意见。"""
        return self.list_ideas(status="archived", sort_by="weight", limit=limit)

    def stats(self) -> Dict[str, Any]:
        total = self._conn.execute("SELECT COUNT(*) FROM ideas").fetchone()[0]
        adopted = self._conn.execute("SELECT COUNT(*) FROM ideas WHERE status='adopted'").fetchone()[0]
        rejected = self._conn.execute("SELECT COUNT(*) FROM ideas WHERE status='rejected'").fetchone()[0]
        avg_weight = self._conn.execute("SELECT COALESCE(AVG(weight),0) FROM ideas").fetchone()[0]
        return {
            "total": total,
            "adopted": adopted,
            "rejected": rejected,
            "avg_weight": round(avg_weight, 2),
            "db_path": str(self.db_path),
            "dna": _dna("CW-STATS"),
        }

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None
        if self._kg_conn:
            self._kg_conn.close()
            self._kg_conn = None
        if self._lu_engine:
            self._lu_engine.close()
            self._lu_engine = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂集思广益引擎")
    parser.add_argument("--submit", "-s", type=str, help="提交一条意见")
    parser.add_argument("--submitter", default="UID9622", help="提交人")
    parser.add_argument("--level", default="L0", help="提交人等级")
    parser.add_argument("--source", default="cli", help="来源")
    parser.add_argument("--list", action="store_true", help="列出意见")
    parser.add_argument("--top", action="store_true", help="置顶意见")
    parser.add_argument("--search", type=str, help="搜索意见")
    parser.add_argument("--status", type=str, help="按状态过滤")
    parser.add_argument("--set-status", type=str, help="设置状态 adopted/rejected/ignored/under_review")
    parser.add_argument("--idea", type=str, help="目标意见码")
    parser.add_argument("--mention", action="store_true", help="提及某条意见")
    parser.add_argument("--verify", action="store_true", help="验证某条意见")
    parser.add_argument("--stats", action="store_true", help="统计")
    args = parser.parse_args()

    engine = CollectiveWisdomEngine()

    if args.submit:
        result = engine.submit(args.submit, args.submitter, args.level, args.source)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.mention and args.idea:
        result = engine.mention(args.idea, args.submitter)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.verify and args.idea:
        result = engine.verify(args.idea, args.submitter)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.set_status and args.idea:
        result = engine.set_status(args.idea, args.set_status, args.submitter)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.search:
        results = engine.search(args.search)
        print(json.dumps({"query": args.search, "results": results}, ensure_ascii=False, indent=2, default=str))
    elif args.top:
        results = engine.top_ideas()
        print(json.dumps(results, ensure_ascii=False, indent=2, default=str))
    elif args.list:
        results = engine.list_ideas(status=args.status)
        print(json.dumps(results, ensure_ascii=False, indent=2, default=str))
    elif args.stats:
        print(json.dumps(engine.stats(), ensure_ascii=False, indent=2, default=str))
    else:
        print(__doc__)
        print("\n当前统计：", json.dumps(engine.stats(), ensure_ascii=False, indent=2, default=str))

    engine.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
