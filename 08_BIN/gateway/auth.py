#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙魂API网关 · 鉴权引擎
DNA: #龍芯⚡️2026-08-31-GATEWAY-AUTH-v1.2-UID9622
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

v1.2: 五锁融合 · 密钥 90 天轮换（rotate_key / get_keys_for_rotation）
"""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from db import get_db


def generate_api_key(owner: str, plan: str = "free") -> dict[str, str]:
    """生成新 API 密钥。key_secret 明文仅此一次返回，库中只存 SHA-256。"""
    key_id = f"lh_{secrets.token_hex(8)}"
    key_secret = secrets.token_hex(16)
    hashed = hashlib.sha256(key_secret.encode()).hexdigest()
    now = datetime.now(timezone.utc).isoformat()

    conn = get_db()
    conn.execute(
        "INSERT INTO api_keys (key_id, key_secret, owner, plan, created_at, active) VALUES (?, ?, ?, ?, ?, 1)",
        (key_id, hashed, owner, plan, now),
    )
    conn.execute(
        "INSERT INTO balances (key_id, balance, last_updated) VALUES (?, 0.0, ?)",
        (key_id, now),
    )
    conn.commit()
    conn.close()

    return {"key_id": key_id, "key_secret": key_secret}


def verify_api_key(key_id: str, key_secret: str) -> dict[str, Any] | None:
    """验证 API 密钥，返回密钥记录或 None。"""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM api_keys WHERE key_id = ? AND active = 1", (key_id,)
    ).fetchone()
    conn.close()

    if not row:
        return None

    hashed = hashlib.sha256(key_secret.encode()).hexdigest()
    if hashed != row["key_secret"]:
        return None

    if row["expires_at"]:
        now = datetime.now(timezone.utc).isoformat()
        if now > row["expires_at"]:
            return None

    return dict(row)


def get_api_key(key_id: str) -> dict[str, Any] | None:
    """按 key_id 取密钥记录（不校验 secret，供 HMAC 验签用）。"""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM api_keys WHERE key_id = ? AND active = 1", (key_id,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    if row["expires_at"]:
        now = datetime.now(timezone.utc).isoformat()
        if now > row["expires_at"]:
            return None
    return dict(row)


def get_plan(key_id: str) -> str:
    conn = get_db()
    row = conn.execute("SELECT plan FROM api_keys WHERE key_id = ?", (key_id,)).fetchone()
    conn.close()
    return row["plan"] if row else "free"


def set_plan(key_id: str, plan: str) -> None:
    conn = get_db()
    conn.execute("UPDATE api_keys SET plan = ? WHERE key_id = ?", (plan, key_id))
    conn.commit()
    conn.close()


# ─── 第五锁 · 密钥轮换（90 天） ───
def rotate_key(key_id: str) -> str | None:
    """轮换密钥：生成新 secret，库中更新哈希。返回新 secret（仅此一次明文）。"""
    new_secret = secrets.token_hex(32)
    hashed = hashlib.sha256(new_secret.encode()).hexdigest()
    now = datetime.now(timezone.utc).isoformat()

    conn = get_db()
    cur = conn.execute(
        "UPDATE api_keys SET key_secret = ?, last_rotated = ? WHERE key_id = ? AND active = 1",
        (hashed, now, key_id),
    )
    conn.commit()
    conn.close()
    return new_secret if cur.rowcount > 0 else None


def get_keys_for_rotation(max_age_days: int = 90) -> list[dict[str, Any]]:
    """返回需要轮换的密钥（超过 90 天未轮换 或 从未轮换且创建超 90 天）。"""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=max_age_days)).isoformat()
    conn = get_db()
    rows = conn.execute(
        "SELECT key_id, owner, plan, created_at, last_rotated FROM api_keys WHERE active = 1 "
        "AND (last_rotated IS NULL OR last_rotated < ?) AND created_at < ?",
        (cutoff, cutoff),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
