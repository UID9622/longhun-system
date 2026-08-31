#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙魂API网关 · 套餐定义
DNA: #龍芯⚡️2026-08-31-GATEWAY-PLANS-v1.0-UID9622
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from auth import set_plan
from db import get_db

PLANS: dict[str, dict[str, Any]] = {
    "free": {
        "name": "免费版",
        "price": 0,
        "daily_calls": 100,
        "kb_access": "basic",
        "priority": False,
        "sla": False,
        "description": "试用体验",
    },
    "pay_as_you_go": {
        "name": "按量付费",
        "price": 0,
        "daily_calls": None,
        "kb_access": "basic",
        "priority": False,
        "sla": False,
        "description": "阶梯计费 0.05/0.04/0.03 元每调用",
    },
    "basic": {
        "name": "基础版",
        "price": 99,
        "monthly_calls": 3000,
        "kb_access": "basic",
        "priority": False,
        "sla": False,
        "description": "适合个人开发者",
    },
    "pro": {
        "name": "专业版",
        "price": 299,
        "monthly_calls": 15000,
        "kb_access": "all",
        "priority": True,
        "sla": False,
        "description": "适合小团队",
    },
    "enterprise": {
        "name": "企业版",
        "price": 999,
        "monthly_calls": None,
        "kb_access": "all",
        "priority": True,
        "sla": True,
        "description": "无限调用 + 私有部署支持",
    },
}


def get_plan_info(plan_name: str) -> dict[str, Any]:
    return PLANS.get(plan_name, PLANS["free"])


def create_subscription(key_id: str, plan_name: str, auto_renew: int = 1) -> dict[str, Any]:
    """创建订阅（30 天）。新订阅自动停用旧订阅并切换套餐。"""
    plan = PLANS.get(plan_name)
    if not plan or plan_name in ("free", "pay_as_you_go"):
        return {"error": "无效订阅套餐"}

    now = datetime.now(timezone.utc)
    expires = now + timedelta(days=30)

    conn = get_db()
    conn.execute(
        "UPDATE subscriptions SET auto_renew = 0 WHERE key_id = ? AND expires_at > ?",
        (key_id, now.isoformat()),
    )
    conn.execute(
        "INSERT INTO subscriptions (key_id, plan, started_at, expires_at, auto_renew) VALUES (?, ?, ?, ?, ?)",
        (key_id, plan_name, now.isoformat(), expires.isoformat(), auto_renew),
    )
    conn.commit()
    conn.close()

    set_plan(key_id, plan_name)

    return {
        "key_id": key_id,
        "plan": plan_name,
        "started_at": now.isoformat(),
        "expires_at": expires.isoformat(),
        "price": plan["price"],
    }


def get_subscription(key_id: str) -> dict[str, Any] | None:
    """返回当前有效订阅（未过期），无则 None。时间用 Python 比较，避免 ISO 格式与 SQLite datetime() 不一致。"""
    now = datetime.now(timezone.utc).isoformat()
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM subscriptions WHERE key_id = ? ORDER BY started_at DESC LIMIT 1",
        (key_id,),
    ).fetchone()
    conn.close()
    if not row or row["expires_at"] <= now:
        return None
    return dict(row)


def get_remaining_calls(key_id: str) -> int:
    """订阅制剩余调用次数；无限返回 -1；无订阅/用完返回 0。"""
    sub = get_subscription(key_id)
    if not sub:
        return 0
    plan = PLANS.get(sub["plan"])
    if not plan:
        return 0

    monthly_calls = plan.get("monthly_calls")
    if monthly_calls is None:
        return -1

    conn = get_db()
    row = conn.execute(
        "SELECT SUM(calls) AS total FROM call_logs WHERE key_id = ? AND timestamp > ?",
        (key_id, sub["started_at"]),
    ).fetchone()
    conn.close()

    used = row["total"] if row and row["total"] else 0
    return max(0, int(monthly_calls - used))
