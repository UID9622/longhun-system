# -*- coding: utf-8 -*-
"""SQLite 审计链 · chain_hash · append-only（§5/§8）"""
from __future__ import annotations

import json
import sqlite3
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .chain_hash import particle_dict_fingerprint, set_particle_chain
from .particle import CNSH_DNA_Particle

_GENESIS = "0" * 64


def _connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), isolation_level=None)  # autocommit for append-only clarity
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def init_db(db_path: Path) -> None:
    conn = _connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS dna_particle_audit (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              dna_id TEXT NOT NULL UNIQUE,
              payload_json TEXT NOT NULL,
              prev_hash TEXT NOT NULL,
              self_hash TEXT NOT NULL,
              created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_dna_particle_self_hash
            ON dna_particle_audit(self_hash);
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS dna_particle_triggers (
              trigger_word TEXT NOT NULL,
              dna_id TEXT NOT NULL,
              PRIMARY KEY (trigger_word, dna_id)
            );
            """
        )
    finally:
        conn.close()


def _last_hash(conn: sqlite3.Connection) -> str:
    row = conn.execute(
        "SELECT self_hash FROM dna_particle_audit ORDER BY id DESC LIMIT 1;"
    ).fetchone()
    return row[0] if row else _GENESIS


def append_particle(
    particle: CNSH_DNA_Particle,
    *,
    db_path: Optional[Path] = None,
) -> CNSH_DNA_Particle:
    """
    仅 INSERT：写入带 prev/self chain_hash 的粒子（篡改检测用）。
    会就地更新 `particle.chain`。
    """
    path = db_path or default_db_path()
    init_db(path)
    prev = _GENESIS
    conn = _connect(path)
    try:
        prev = _last_hash(conn)
        p2 = set_particle_chain(particle, prev_hash=prev)
        payload = json.dumps(
            p2.to_dict()["CNSH_DNA_PARTICLE"],
            ensure_ascii=False,
            separators=(",", ":"),
        )
        conn.execute("BEGIN IMMEDIATE;")
        conn.execute(
            """
            INSERT INTO dna_particle_audit (dna_id, payload_json, prev_hash, self_hash)
            VALUES (?, ?, ?, ?);
            """,
            (p2.dna_id, payload, p2.chain.prev_hash, p2.chain.self_hash),
        )
        for w in p2.restore_hint.trigger_words:
            wn = w.strip()
            if not wn:
                continue
            conn.execute(
                """
                INSERT OR IGNORE INTO dna_particle_triggers (trigger_word, dna_id)
                VALUES (?, ?);
                """,
                (wn.lower(), p2.dna_id),
            )
        conn.execute("COMMIT;")
        return p2
    except Exception:
        conn.execute("ROLLBACK;")
        raise
    finally:
        conn.close()


def fetch_particle_dict(dna_id: str, *, db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    path = db_path or default_db_path()
    if not path.exists():
        return None
    conn = _connect(path)
    try:
        row = conn.execute(
            "SELECT payload_json, prev_hash, self_hash FROM dna_particle_audit WHERE dna_id = ?;",
            (dna_id,),
        ).fetchone()
        if not row:
            return None
        body = json.loads(row[0])
        body.setdefault("chain", {})
        body["chain"]["_prev_hash"] = row[1]
        body["chain"]["_self_hash"] = row[2]
        return body
    finally:
        conn.close()


def find_dna_ids_by_trigger(trigger: str, *, db_path: Optional[Path] = None) -> List[str]:
    path = db_path or default_db_path()
    if not path.exists():
        return []
    conn = _connect(path)
    try:
        cur = conn.execute(
            "SELECT dna_id FROM dna_particle_triggers WHERE trigger_word = ? ORDER BY dna_id;",
            (trigger.strip().lower(),),
        )
        return [r[0] for r in cur.fetchall()]
    finally:
        conn.close()


def verify_chain(db_path: Optional[Path] = None) -> Tuple[bool, List[str]]:
    """全表顺序校验：每条 prev 等于上条 self；首条 prev 须为 GENESIS。"""
    path = db_path or default_db_path()
    errors: List[str] = []
    if not path.exists():
        return True, []
    conn = _connect(path)
    try:
        rows = conn.execute(
            "SELECT dna_id, payload_json, prev_hash, self_hash FROM dna_particle_audit ORDER BY id ASC;"
        ).fetchall()
        expected_prev = _GENESIS
        for dna_id, payload_json, prev_hash, self_hash in rows:
            if prev_hash != expected_prev:
                errors.append(
                    f"{dna_id}: prev_hash 断裂 expected={expected_prev[:16]}… got={prev_hash[:16]}…"
                )
            body = json.loads(payload_json)
            calc = particle_dict_fingerprint(body)
            if calc != self_hash:
                errors.append(f"{dna_id}: self_hash 不匹配")
            expected_prev = self_hash
        return len(errors) == 0, errors
    finally:
        conn.close()


def default_db_path() -> Path:
    return Path(__file__).resolve().parent.parent.parent / "data" / "dna_particle_audit.sqlite3"
