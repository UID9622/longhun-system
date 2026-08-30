# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂审计链 · 汇兑模块 v1.0
DNA: #龍芯⚡️2026-08-23-CONVERTER-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

设计原则:
  · 任意币 → eCNY，一次调用搞定
  · 汇率快照自动存证到 SQLite（审计需要）
  · DNA 追溯码绑定每笔转换
"""

import sqlite3, os
from datetime import datetime
from rate_fetcher import get_rate_to_cny
from dna_utils import generate_dna, now_iso

DB_PATH = os.path.join(os.path.dirname(__file__), "db", "ledger.db")

def _init_db():
    """初始化 SQLite 数据库（自动建表）"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS conversions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            dna         TEXT UNIQUE,
            user_id     TEXT,
            from_amount REAL,
            from_curr   TEXT,
            ecny_amount REAL,
            rate        REAL,
            rate_source TEXT,
            is_fallback INTEGER,
            created_at  TEXT
        );
        CREATE TABLE IF NOT EXISTS payments (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            dna         TEXT UNIQUE,
            user_id     TEXT,
            ecny_amount REAL,
            type        TEXT,
            status      TEXT DEFAULT 'pending',
            settle_dna  TEXT,
            created_at  TEXT
        );
        CREATE TABLE IF NOT EXISTS audit_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            dna         TEXT UNIQUE,
            caller_id   TEXT,
            endpoint    TEXT,
            ecny_charged REAL,
            tri_color   TEXT,
            created_at  TEXT
        );
    """)
    conn.commit()
    conn.close()

_init_db()  # 启动时自动初始化

class CurrencyConverter:
    """
    核心汇兑器：任意币 → eCNY
    """

    def convert(self, amount: float, from_currency: str,
                user_id: str = "anonymous") -> dict:
        """
        转换任意货币到 eCNY，记录账本，返回完整结果
        """
        from_currency = from_currency.upper()

        # 获取汇率
        rate_info = get_rate_to_cny(from_currency)
        rate      = rate_info["rate"]
        ecny_amt  = round(amount * rate, 4)

        # 生成 DNA
        dna = generate_dna("CONVERT", {
            "amount": amount,
            "from": from_currency,
            "ecny": ecny_amt,
            "user": user_id,
        })

        # 存证到 SQLite
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT OR IGNORE INTO conversions "
            "(dna, user_id, from_amount, from_curr, ecny_amount, rate, "
            "rate_source, is_fallback, created_at) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            (dna, user_id, amount, from_currency, ecny_amt,
             rate, rate_info["source"],
             1 if rate_info["is_fallback"] else 0,
             now_iso())
        )
        conn.commit()
        conn.close()

        return {
            "original":  {"amount": amount, "currency": from_currency},
            "converted": {"amount": ecny_amt, "currency": "eCNY"},
            "rate":       rate,
            "rate_source": rate_info["source"],
            "is_fallback": rate_info["is_fallback"],
            "rate_snapshot_at": rate_info["timestamp"],
            "dna":        dna,
            "tri_color":  "🟡" if rate_info["is_fallback"] else "🟢",
        }
