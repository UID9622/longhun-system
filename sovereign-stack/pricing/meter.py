#!/usr/bin/env python3
"""
🐉 龍魂主权技术栈·按量计费计量器 v1.0
原则：透明·无隐性收费·随时可查·随时可停
DNA: #龍芯⚡️2026-08-31-METER-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: MulanPSL v2（工程实现层）
"""

import sqlite3
import yaml
import json
import time
from pathlib import Path
from datetime import datetime, date
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 配置路径基于本文件定位（兼容从任意目录启动）
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path.home() / ".longhun" / "meter.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# 加载定价规则
with open(BASE_DIR / "pricing_rules.yaml") as f:
    PRICING = yaml.safe_load(f)

with open(BASE_DIR / "free_tier.yaml") as f:
    FREE_TIER = yaml.safe_load(f)


def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS usage_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id TEXT NOT NULL,
            tier TEXT DEFAULT 'personal',
            resource_type TEXT NOT NULL,  -- 'api_call' | 'search' | 'storage'
            quantity REAL DEFAULT 1,
            timestamp TEXT NOT NULL,
            month TEXT NOT NULL,          -- 'YYYY-MM' 用于月度聚合
            dna TEXT                      -- DNA追溯码
        );
        CREATE TABLE IF NOT EXISTS accounts (
            account_id TEXT PRIMARY KEY,
            tier TEXT DEFAULT 'personal',
            balance REAL DEFAULT 0,       -- 预付余额（元）
            created_at TEXT,
            last_active TEXT,
            is_open_source INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS monthly_summary (
            account_id TEXT,
            month TEXT,
            api_calls INTEGER DEFAULT 0,
            search_queries INTEGER DEFAULT 0,
            storage_gb REAL DEFAULT 0,
            total_charge REAL DEFAULT 0,
            free_used INTEGER DEFAULT 0,  -- 是否使用了免费额度
            PRIMARY KEY (account_id, month)
        );
        CREATE INDEX IF NOT EXISTS idx_usage_account ON usage_log(account_id, month);
    """)
    conn.commit()
    conn.close()


def get_monthly_usage(account_id: str, month: str) -> dict:
    conn = sqlite3.connect(str(DB_PATH))
    row = conn.execute("""
        SELECT api_calls, search_queries, storage_gb
        FROM monthly_summary
        WHERE account_id=? AND month=?
    """, (account_id, month)).fetchone()
    conn.close()
    if row:
        return {"api_calls": row[0], "search_queries": row[1], "storage_gb": row[2]}
    return {"api_calls": 0, "search_queries": 0, "storage_gb": 0}


def get_tier_config(tier: str) -> dict:
    return PRICING["tiers"].get(tier, PRICING["tiers"]["personal"])


def calculate_charge(resource_type: str, quantity: float,
                     current_usage: dict, tier: str) -> dict:
    """计算本次使用费用（透明计算·无隐藏费）"""
    config = get_tier_config(tier)
    free_quota = config.get("free_quota", {})
    ppu = config.get("pay_as_you_go", {})

    type_map = {
        "api_call":    ("api_calls",    "api_call_unit"),
        "search":      ("search_queries", "search_query_unit"),
        "storage":     ("storage_gb",   "storage_gb_unit"),
    }

    usage_key, price_key = type_map.get(resource_type, ("api_calls", "api_call_unit"))
    current = current_usage.get(usage_key, 0)
    free_limit = free_quota.get(usage_key, 0)
    unit_price = ppu.get(price_key, 0)

    # 计算免费额度内的量
    free_remaining = max(0, free_limit - current)
    free_consumed = min(quantity, free_remaining)
    paid_quantity = max(0, quantity - free_consumed)

    charge = paid_quantity * unit_price

    return {
        "resource_type": resource_type,
        "quantity": quantity,
        "free_consumed": free_consumed,
        "paid_quantity": paid_quantity,
        "unit_price": unit_price,
        "charge": round(charge, 6),
        "free_remaining_after": max(0, free_remaining - free_consumed),
        "currency": "CNY",
        "transparent": True  # 计算过程完全透明
    }


def record_usage(account_id: str, resource_type: str,
                 quantity: float, tier: str = "personal") -> dict:
    """记录使用量并计算费用"""
    month = datetime.now().strftime("%Y-%m")
    current_usage = get_monthly_usage(account_id, month)
    charge_info = calculate_charge(resource_type, quantity, current_usage, tier)

    now = datetime.now().isoformat()
    dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-METER-{resource_type.upper()}-UID9622"

    conn = sqlite3.connect(str(DB_PATH))

    # 记录明细日志
    conn.execute("""
        INSERT INTO usage_log (account_id, tier, resource_type, quantity, timestamp, month, dna)
        VALUES (?,?,?,?,?,?,?)
    """, (account_id, tier, resource_type, quantity, now, month, dna))

    # 更新月度汇总
    type_col_map = {
        "api_call": "api_calls",
        "search":   "search_queries",
        "storage":  "storage_gb",
    }
    col = type_col_map.get(resource_type, "api_calls")
    conn.execute(f"""
        INSERT INTO monthly_summary (account_id, month, {col}, total_charge)
        VALUES (?,?,?,?)
        ON CONFLICT(account_id, month) DO UPDATE SET
            {col} = {col} + ?,
            total_charge = total_charge + ?
    """, (account_id, month, quantity, charge_info["charge"],
          quantity, charge_info["charge"]))

    # 如果有费用，从余额扣除
    if charge_info["charge"] > 0:
        conn.execute("""
            UPDATE accounts SET balance = balance - ?, last_active = ?
            WHERE account_id = ?
        """, (charge_info["charge"], now, account_id))

    conn.commit()
    conn.close()

    return {**charge_info, "dna": dna, "timestamp": now}


# ──────────────────────────────────────────
# REST API 端点
# ──────────────────────────────────────────

@app.route("/meter/record", methods=["POST"])
def record():
    """记录一次使用（由各服务调用）"""
    data = request.json or {}
    account_id    = data.get("account_id", "anonymous")
    resource_type = data.get("resource_type", "api_call")
    quantity      = float(data.get("quantity", 1))
    tier          = data.get("tier", "personal")
    result = record_usage(account_id, resource_type, quantity, tier)
    return jsonify(result)


@app.route("/meter/usage/<account_id>")
def usage(account_id):
    """查询当前月使用量（用户随时可查·透明）"""
    month = datetime.now().strftime("%Y-%m")
    current = get_monthly_usage(account_id, month)
    tier = request.args.get("tier", "personal")
    config = get_tier_config(tier)
    free_quota = config.get("free_quota", {})

    return jsonify({
        "account_id": account_id,
        "month": month,
        "tier": tier,
        "usage": current,
        "free_quota": free_quota,
        "free_remaining": {
            k: max(0, free_quota.get(k, 0) - current.get(k, 0))
            for k in free_quota
        },
        "note": "免费额度每月1日自动重置·无需申请",
        "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-USAGE-QUERY-UID9622"
    })


@app.route("/meter/bill/<account_id>")
def bill(account_id):
    """查询账单（透明·逐条可查）"""
    month = request.args.get("month", datetime.now().strftime("%Y-%m"))
    conn = sqlite3.connect(str(DB_PATH))
    summary = conn.execute("""
        SELECT api_calls, search_queries, storage_gb, total_charge
        FROM monthly_summary WHERE account_id=? AND month=?
    """, (account_id, month)).fetchone()
    details = conn.execute("""
        SELECT resource_type, quantity, timestamp, dna
        FROM usage_log WHERE account_id=? AND month=?
        ORDER BY timestamp DESC LIMIT 100
    """, (account_id, month)).fetchall()
    conn.close()

    return jsonify({
        "account_id": account_id,
        "month": month,
        "summary": dict(zip(
            ["api_calls", "search_queries", "storage_gb", "total_charge"],
            summary
        )) if summary else {},
        "details": [
            {"type": d[0], "qty": d[1], "time": d[2], "dna": d[3]}
            for d in details
        ],
        "transparency": "所有消费均有DNA追溯码·随时可查·随时可停·无隐藏费",
        "currency": "CNY"
    })


@app.route("/meter/topup", methods=["POST"])
def topup():
    """充值（预付·不欠费·不强制包月）"""
    data = request.json or {}
    account_id = data.get("account_id")
    amount     = float(data.get("amount", 0))
    if amount <= 0:
        return jsonify({"error": "充值金额必须大于0"}), 400
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        INSERT INTO accounts (account_id, balance, created_at)
        VALUES (?,?,?)
        ON CONFLICT(account_id) DO UPDATE SET balance = balance + ?
    """, (account_id, amount, datetime.now().isoformat(), amount))
    balance = conn.execute(
        "SELECT balance FROM accounts WHERE account_id=?",
        (account_id,)
    ).fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({
        "account_id": account_id,
        "topped_up": amount,
        "balance": balance,
        "currency": "CNY",
        "note": "预付余额·用多少扣多少·不强制消费",
        "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-TOPUP-UID9622"
    })


@app.route("/meter/health")
def health():
    return jsonify({"status": "healthy", "service": "longhun-meter", "version": "1.0"})


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=8897, debug=False)
