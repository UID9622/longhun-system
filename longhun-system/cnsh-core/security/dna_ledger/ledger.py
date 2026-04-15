"""
DNA 追溯链 · Append-Only Ledger
Author: 诸葛鑫 (UID9622)
DNA: #ZHUGEXIN⚡️2026-03-23-DNA-LEDGER-v1.0

每个系统行为产生一条不可篡改记录。
链式结构: DNA(n) = SHA256(DNA(n-1) || timestamp || event || decision)
"""

import hashlib
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, List


@dataclass
class DNARecord:
    record_id:     str
    timestamp:     str
    event_hash:    str
    composite_state: str
    action:        str
    risk_score:    float
    audit_color:   str
    prev_hash:     str
    this_hash:     str
    dna_trace:     str
    user_id:       str
    metadata:      str  # JSON string


def generate_dna_trace(event: str, state: str, action: str, ts: str) -> str:
    """生成 DNA 追溯码"""
    date = ts[:10]
    raw  = f"{event}|{state}|{action}|{ts}"
    h8   = hashlib.sha256(raw.encode()).hexdigest()[:8].upper()
    return f"#LONGHUN⚡️{date}-{action.upper()}-{h8}"


def compute_hash(prev_hash: str, timestamp: str, event: str, decision: str) -> str:
    raw = f"{prev_hash}||{timestamp}||{event}||{decision}"
    return hashlib.sha256(raw.encode()).hexdigest()


class DNALedger:
    """
    不可篡改的 DNA 行为账本。
    存储：SQLite（本地，不上云）
    """

    GENESIS_HASH = "0" * 64  # 创世哈希

    def __init__(self, db_path: str = "~/.longhun/cnsh_ledger.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dna_records (
                    record_id      TEXT PRIMARY KEY,
                    timestamp      TEXT NOT NULL,
                    event_hash     TEXT NOT NULL,
                    composite_state TEXT NOT NULL,
                    action         TEXT NOT NULL,
                    risk_score     REAL NOT NULL,
                    audit_color    TEXT NOT NULL,
                    prev_hash      TEXT NOT NULL,
                    this_hash      TEXT NOT NULL,
                    dna_trace      TEXT NOT NULL,
                    user_id        TEXT NOT NULL,
                    metadata       TEXT DEFAULT '{}'
                )
            """)
            conn.commit()

    def _last_hash(self) -> str:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT this_hash FROM dna_records ORDER BY timestamp DESC LIMIT 1"
            ).fetchone()
        return row[0] if row else self.GENESIS_HASH

    def append(
        self,
        event_content: str,
        composite_state: str,
        action: str,
        risk_score: float,
        audit_color: str,
        user_id: str,
        metadata: dict = None,
    ) -> DNARecord:
        ts         = datetime.utcnow().isoformat()
        prev_hash  = self._last_hash()
        event_hash = hashlib.sha256(event_content.encode()).hexdigest()
        this_hash  = compute_hash(prev_hash, ts, event_hash, action)
        dna_trace  = generate_dna_trace(event_content, composite_state, action, ts)
        record_id  = hashlib.md5(f"{ts}{event_hash}".encode()).hexdigest()

        record = DNARecord(
            record_id       = record_id,
            timestamp       = ts,
            event_hash      = event_hash,
            composite_state = composite_state,
            action          = action,
            risk_score      = risk_score,
            audit_color     = audit_color,
            prev_hash       = prev_hash,
            this_hash       = this_hash,
            dna_trace       = dna_trace,
            user_id         = user_id,
            metadata        = json.dumps(metadata or {}),
        )

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO dna_records VALUES
                   (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    record.record_id, record.timestamp, record.event_hash,
                    record.composite_state, record.action, record.risk_score,
                    record.audit_color, record.prev_hash, record.this_hash,
                    record.dna_trace, record.user_id, record.metadata,
                ),
            )
            conn.commit()

        return record

    def verify_integrity(self) -> bool:
        """验证账本链式完整性"""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT prev_hash, this_hash, timestamp, event_hash, action FROM dna_records ORDER BY timestamp ASC"
            ).fetchall()

        if not rows:
            return True

        expected_prev = self.GENESIS_HASH
        for row in rows:
            prev_hash, this_hash, ts, event_hash, action = row
            if prev_hash != expected_prev:
                return False
            recomputed = compute_hash(prev_hash, ts, event_hash, action)
            if recomputed != this_hash:
                return False
            expected_prev = this_hash

        return True

    def query(self, user_id: Optional[str] = None, limit: int = 50) -> List[dict]:
        with sqlite3.connect(self.db_path) as conn:
            if user_id:
                rows = conn.execute(
                    "SELECT * FROM dna_records WHERE user_id=? ORDER BY timestamp DESC LIMIT ?",
                    (user_id, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM dna_records ORDER BY timestamp DESC LIMIT ?",
                    (limit,),
                ).fetchall()

        cols = [
            "record_id", "timestamp", "event_hash", "composite_state",
            "action", "risk_score", "audit_color", "prev_hash", "this_hash",
            "dna_trace", "user_id", "metadata",
        ]
        return [dict(zip(cols, r)) for r in rows]
