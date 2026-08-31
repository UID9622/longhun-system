#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙魂API网关 · 计量引擎
DNA: #龍芯⚡️2026-08-31-GATEWAY-METER-v1.0-UID9622
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

from datetime import date, datetime, timezone
from typing import Any

from db import get_db


def get_daily_usage(key_id: str) -> int:
    """今日调用次数。"""
    today = date.today().isoformat()
    conn = get_db()
    row = conn.execute(
        "SELECT calls FROM daily_usage WHERE key_id = ? AND date = ?",
        (key_id, today),
    ).fetchone()
    conn.close()
    return row["calls"] if row else 0


def increment_daily_usage(key_id: str, increment: int = 1) -> int:
    """增加今日调用计数，返回最新值。"""
    today = date.today().isoformat()
    conn = get_db()
    conn.execute(
        """
        INSERT INTO daily_usage (key_id, date, calls)
        VALUES (?, ?, ?)
        ON CONFLICT(key_id, date) DO UPDATE SET calls = calls + excluded.calls
        """,
        (key_id, today, increment),
    )
    conn.commit()
    row = conn.execute(
        "SELECT calls FROM daily_usage WHERE key_id = ? AND date = ?",
        (key_id, today),
    ).fetchone()
    conn.close()
    return row["calls"] if row else 0


def deduct_balance(key_id: str, amount: float) -> bool:
    """扣减余额，余额不足返回 False。"""
    conn = get_db()
    row = conn.execute("SELECT balance FROM balances WHERE key_id = ?", (key_id,)).fetchone()
    if not row or row["balance"] < amount:
        conn.close()
        return False
    conn.execute(
        "UPDATE balances SET balance = balance - ?, last_updated = ? WHERE key_id = ?",
        (amount, datetime.now(timezone.utc).isoformat(), key_id),
    )
    conn.commit()
    conn.close()
    return True


def add_balance(key_id: str, amount: float) -> None:
    """增加余额（充值）。"""
    conn = get_db()
    conn.execute(
        """
        INSERT INTO balances (key_id, balance, last_updated)
        VALUES (?, ?, ?)
        ON CONFLICT(key_id) DO UPDATE SET balance = balance + excluded.balance
        """,
        (key_id, amount, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()


def get_balance(key_id: str) -> float:
    conn = get_db()
    row = conn.execute("SELECT balance FROM balances WHERE key_id = ?", (key_id,)).fetchone()
    conn.close()
    return row["balance"] if row else 0.0


def log_call(key_id: str, endpoint: str, cost: float = 0.0, calls: int = 1) -> None:
    """记录调用日志（只记计量，不记内容）。"""
    conn = get_db()
    conn.execute(
        "INSERT INTO call_logs (key_id, endpoint, calls, cost, timestamp) VALUES (?, ?, ?, ?, ?)",
        (key_id, endpoint, calls, cost, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()
