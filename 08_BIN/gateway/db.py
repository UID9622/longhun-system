#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙魂API网关 · 数据库层
DNA: #龍芯⚡️2026-08-31-GATEWAY-DB-v1.2-UID9622
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

仅存计量/审计元数据（调用次数/余额/订阅/审计），不存任何用户对话内容与请求原文（P0 数据主权）。
v1.2: 五锁融合 · audit_logs 表 + api_keys.last_rotated 列（旧库自动迁移）
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta, timezone

DB_PATH = Path(__file__).parent / "gateway.db"


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    """初始化数据库表。"""
    conn = get_db()
    conn.executescript(
        """
        -- API密钥表（v1.2 加 last_rotated，90天轮换用）
        CREATE TABLE IF NOT EXISTS api_keys (
            key_id TEXT PRIMARY KEY,
            key_secret TEXT NOT NULL,        -- SHA-256(key_secret)，明文只在注册时返回一次
            owner TEXT NOT NULL,
            plan TEXT DEFAULT 'free',
            created_at TEXT NOT NULL,
            expires_at TEXT,
            active INTEGER DEFAULT 1,
            metadata TEXT DEFAULT '{}',
            last_rotated TEXT
        );

        -- 调用日志表（只记计量，不记内容）
        CREATE TABLE IF NOT EXISTS call_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_id TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            calls INTEGER DEFAULT 1,
            cost REAL DEFAULT 0.0,
            timestamp TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_calls_key ON call_logs(key_id);
        CREATE INDEX IF NOT EXISTS idx_calls_time ON call_logs(timestamp);

        -- 余额表
        CREATE TABLE IF NOT EXISTS balances (
            key_id TEXT PRIMARY KEY,
            balance REAL DEFAULT 0.0,
            last_updated TEXT NOT NULL
        );

        -- 每日配额表
        CREATE TABLE IF NOT EXISTS daily_usage (
            key_id TEXT NOT NULL,
            date TEXT NOT NULL,
            calls INTEGER DEFAULT 0,
            PRIMARY KEY (key_id, date)
        );

        -- 订阅表
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_id TEXT NOT NULL,
            plan TEXT NOT NULL,
            started_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            auto_renew INTEGER DEFAULT 1
        );
        CREATE INDEX IF NOT EXISTS idx_sub_key ON subscriptions(key_id);

        -- 审计日志表（五锁·只存元数据，不存请求原文/headers，P0）
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_id TEXT,
            endpoint TEXT NOT NULL,
            method TEXT NOT NULL,
            ip TEXT,
            status_code INTEGER,
            response_time REAL,
            auth_mode TEXT,
            signature_valid INTEGER,
            rate_limited INTEGER DEFAULT 0,
            timestamp TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_audit_time ON audit_logs(timestamp);
        CREATE INDEX IF NOT EXISTS idx_audit_key ON audit_logs(key_id);
        """
    )
    conn.commit()

    # ─── 旧库迁移：api_keys 补 last_rotated 列（CREATE IF NOT EXISTS 不会加列） ───
    cols = [r[1] for r in conn.execute("PRAGMA table_info(api_keys)").fetchall()]
    if "last_rotated" not in cols:
        conn.execute("ALTER TABLE api_keys ADD COLUMN last_rotated TEXT")
        conn.commit()

    conn.close()


def prune_call_logs(days: int = 90) -> None:
    """清理 90 天前的调用日志（防无限增长）。"""
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    conn = get_db()
    conn.execute("DELETE FROM call_logs WHERE timestamp < ?", (cutoff,))
    conn.execute("DELETE FROM audit_logs WHERE timestamp < ?", (cutoff,))
    conn.commit()
    conn.close()


def write_audit(
    *,
    key_id: str,
    endpoint: str,
    method: str,
    ip: str,
    status_code: int,
    response_time: float,
    auth_mode: str = "",
    signature_valid: int = 0,
    rate_limited: int = 0,
) -> None:
    """写入审计日志（只记元数据，不记请求内容，P0）。"""
    conn = get_db()
    conn.execute(
        """
        INSERT INTO audit_logs
        (key_id, endpoint, method, ip, status_code, response_time, auth_mode, signature_valid, rate_limited, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            key_id or "",
            endpoint,
            method,
            ip or "",
            status_code,
            round(response_time, 4),
            auth_mode,
            signature_valid,
            rate_limited,
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    conn.commit()
    conn.close()
