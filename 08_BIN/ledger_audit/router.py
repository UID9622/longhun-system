#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
🚦 龍魂路由分发器 · Longhun Audit Router v1.0

DNA: #龍審⚡️2026-08-31-AUDIT-ROUTER-v1.0-UID9622
根据三色审计结果，路由到对应处理器并触发回调
"""

import json
import sys
import datetime
from audit_engine import audit_transaction
from integrations import on_green_commit, on_yellow_pending, on_red_block


def auto_approve_handler(tx, result):
    """🟢 GREEN: 自动批准处理器 → Notion写入 + GitHub同步"""
    print(f"  ✅ AUTO_APPROVE: {tx['tx_id']} → Notion写入 + GitHub同步")
    on_green_commit(tx, result)
    trigger_callback("on_green_commit", tx, result)


def pending_review_handler(tx, result):
    """🟡 YELLOW: 等待审批处理器（72h窗口）→ 宝宝接管"""
    print(f"  ⏳ PENDING_REVIEW: {tx['tx_id']} → 宝宝接管，72h倒计时")
    on_yellow_pending(tx, result)
    trigger_callback("on_yellow_pending", tx, result)


def sovereign_block_handler(tx, result):
    """🔴 RED: 主权阻断处理器 → 交易冻结 + 主权人警报 + incidents归档"""
    print(f"  🚫 SOVEREIGN_BLOCK: {tx['tx_id']} → 交易冻结，主权人警报")
    on_red_block(tx, result)
    trigger_callback("on_red_block", tx, result)


def trigger_callback(event: str, tx: dict, result: dict):
    """回调触发器 - 记录回调事件"""
    ts = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
    callback = {
        "callback_id": f"CB-{tx.get('date', 'UNKNOWN')}-{tx.get('tx_id', 'UNKNOWN')}",
        "event": event,
        "timestamp": ts,
        "tx_dna": tx.get("dna"),
        "tx_hash": tx.get("hash"),
        "audit_result": result,
        "uid": "UID9622"
    }
    print(f"  📡 CALLBACK: {event} fired at {ts}")
    return callback


ROUTER_MAP = {
    "AUTO_APPROVE_HANDLER":    auto_approve_handler,
    "PENDING_REVIEW_HANDLER":  pending_review_handler,
    "SOVEREIGN_BLOCK_HANDLER": sovereign_block_handler,
}


def route(tx: dict):
    result = audit_transaction(tx)
    handler = ROUTER_MAP.get(result["router"])
    if handler:
        handler(tx, result)
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python router.py data/ledger.json")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        ledger = json.load(f)

    for tx in ledger.get("transactions", []):
        route(tx)
