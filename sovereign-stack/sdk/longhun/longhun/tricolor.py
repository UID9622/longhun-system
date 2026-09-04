"""
🐉 三色审计 v1.0
🟢 绿色：通过·可用·正常
🟡 黄色：待审·降级·需人工确认
🔴 红色：拒绝·熔断·触发告警
审计日志落 sqlite（~/.longhun/audit.db）· append-only

DNA: #龍芯⚡️2026-08-31-LONGHUN-TRICOLOR-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from .dna import generate_dna

DB_PATH = Path.home() / ".longhun" / "audit.db"


def _init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            module TEXT,
            event TEXT,
            color TEXT CHECK(color IN ('🟢','🟡','🔴')),
            detail TEXT,
            dna TEXT
        );
    """)
    conn.commit()
    conn.close()


def tricolor_status(status_code: int, has_data: bool = True) -> str:
    """三色判定：2xx且有数据=🟢 / 4xx=🟡 / 5xx=🔴"""
    if status_code < 300 and has_data:
        return "🟢"
    if status_code < 500:
        return "🟡"
    return "🔴"


def audit(module: str, event: str, color: str, detail: dict = None) -> str:
    """记录一条审计日志 · 返回该条 DNA"""
    _init_db()
    dna = generate_dna(f"AUDIT-{module}")
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(
        "INSERT INTO audit_log (timestamp, module, event, color, detail, dna) "
        "VALUES (?,?,?,?,?,?)",
        (datetime.now().isoformat(), module, event, color,
         json.dumps(detail or {}, ensure_ascii=False), dna),
    )
    conn.commit()
    conn.close()
    if color == "🔴":
        print(f"🔴 [AUDIT-ALERT] {module} | {event} | {detail}")
    return dna


def summary(module: str = None) -> dict:
    """审计汇总（按颜色计数）"""
    _init_db()
    conn = sqlite3.connect(str(DB_PATH))
    where, params = ("WHERE module=?", (module,)) if module else ("", ())
    rows = conn.execute(
        f"SELECT color, COUNT(*) FROM audit_log {where} GROUP BY color", params
    ).fetchall()
    conn.close()
    counts = {"🟢": 0, "🟡": 0, "🔴": 0}
    for color, cnt in rows:
        counts[color] = cnt
    return counts


_init_db()
