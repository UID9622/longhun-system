"""
dare/store.py — 四敢品质 SQLite 持久层
表: dare_actions | shield_logs
"""
import os, sqlite3, uuid, time
from typing import List, Dict, Optional

DB_PATH = os.path.expanduser("~/.longhun/dna_calendar.db")

# ── 建表 ──────────────────────────────────────────────────────────

def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_dare_tables():
    """确保 dare_actions / shield_logs 表存在"""
    conn = _get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS dare_actions (
            id          TEXT PRIMARY KEY,
            user_id     TEXT NOT NULL DEFAULT 'uid9622',
            action_type TEXT NOT NULL,
            weight      REAL DEFAULT 1.0,
            context     TEXT,
            dna_trace   TEXT,
            timestamp   INTEGER DEFAULT (strftime('%s','now'))
        );
        CREATE INDEX IF NOT EXISTS idx_dare_user
            ON dare_actions(user_id, action_type);

        CREATE TABLE IF NOT EXISTS shield_logs (
            id        TEXT PRIMARY KEY,
            dna_trace TEXT NOT NULL,
            layer     TEXT NOT NULL,
            action    TEXT NOT NULL,
            result    TEXT NOT NULL,
            timestamp INTEGER DEFAULT (strftime('%s','now'))
        );
        CREATE INDEX IF NOT EXISTS idx_shield_dna
            ON shield_logs(dna_trace);
    """)
    conn.commit()
    conn.close()

# ── dare_actions CRUD ─────────────────────────────────────────────

def record_action(action_type: str, weight: float = 1.0,
                  context: str = "", dna_trace: str = "",
                  user_id: str = "uid9622") -> str:
    """写入一条四敢行为记录，返回 action_id"""
    conn = _get_conn()
    aid = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO dare_actions(id, user_id, action_type, weight, context, dna_trace) "
        "VALUES (?,?,?,?,?,?)",
        (aid, user_id, action_type, weight, context, dna_trace)
    )
    conn.commit()
    conn.close()
    return aid

def get_actions(user_id: str = "uid9622",
                action_type: Optional[str] = None,
                limit: int = 200) -> List[Dict]:
    conn = _get_conn()
    if action_type:
        rows = conn.execute(
            "SELECT * FROM dare_actions WHERE user_id=? AND action_type=? "
            "ORDER BY timestamp DESC LIMIT ?",
            (user_id, action_type, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM dare_actions WHERE user_id=? "
            "ORDER BY timestamp DESC LIMIT ?",
            (user_id, limit)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ── shield_logs CRUD ──────────────────────────────────────────────

def write_shield_log(dna_trace: str, layer: str,
                     action: str, result: str) -> str:
    conn = _get_conn()
    lid = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO shield_logs(id, dna_trace, layer, action, result) VALUES (?,?,?,?,?)",
        (lid, dna_trace, layer, action, result)
    )
    conn.commit()
    conn.close()
    return lid

def get_shield_logs(dna_trace: str) -> List[Dict]:
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM shield_logs WHERE dna_trace=? ORDER BY timestamp DESC",
        (dna_trace,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
