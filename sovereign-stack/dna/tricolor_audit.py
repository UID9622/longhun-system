#!/usr/bin/env python3
"""
🐉 龍魂三色审计引擎
🟢 绿色：通过·可用·正常
🟡 黄色：待审·降级·需人工确认
🔴 红色：拒绝·熔断·触发告警
DNA: #龍芯⚡️2026-08-31-TRICOLOR-AUDIT-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: MulanPSL v2（工程实现层）
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / ".longhun" / "audit.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def init_audit_db():
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
        CREATE INDEX IF NOT EXISTS idx_audit_color  ON audit_log(color);
        CREATE INDEX IF NOT EXISTS idx_audit_module ON audit_log(module);
    """)
    conn.commit()
    conn.close()


def audit(module: str, event: str, color: str, detail: dict = None):
    """记录一条审计日志"""
    conn = sqlite3.connect(str(DB_PATH))
    dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-AUDIT-{module.upper()}-UID9622"
    conn.execute("""
        INSERT INTO audit_log (timestamp, module, event, color, detail, dna)
        VALUES (?,?,?,?,?,?)
    """, (datetime.now().isoformat(), module, event, color,
          json.dumps(detail or {}, ensure_ascii=False), dna))
    conn.commit()
    conn.close()

    # 🔴 红色立即打印告警
    if color == "🔴":
        print(f"🔴 [AUDIT-ALERT] {module} | {event} | {detail}")

    return dna


def get_audit_summary(module: str = None, last_n: int = 100) -> dict:
    conn = sqlite3.connect(str(DB_PATH))
    where = "WHERE module=?" if module else ""
    params = (module,) if module else ()
    rows = conn.execute(f"""
        SELECT color, COUNT(*) as cnt
        FROM audit_log {where}
        GROUP BY color
    """, params).fetchall()
    recent = conn.execute(f"""
        SELECT timestamp, module, event, color, detail
        FROM audit_log {where}
        ORDER BY id DESC LIMIT ?
    """, (*params, last_n)).fetchall()
    conn.close()

    counts = {r[0]: r[1] for r in rows}
    return {
        "summary": {
            "🟢": counts.get("🟢", 0),
            "🟡": counts.get("🟡", 0),
            "🔴": counts.get("🔴", 0)
        },
        "recent": [
            {"time": r[0], "module": r[1], "event": r[2],
             "color": r[3], "detail": r[4]}
            for r in recent
        ]
    }


init_audit_db()
