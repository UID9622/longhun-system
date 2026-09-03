#!/usr/bin/env python3
"""
🐉 龍魂·个人开发者免费配额管理器
原则：个人开发者不应该有门槛，代码应该普惠所有人
DNA: #龍芯⚡️2026-08-31-FREE-TIER-MANAGER-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: MulanPSL v2（工程实现层）
"""

import sqlite3
import yaml
import json
from datetime import datetime, date
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = Path.home() / ".longhun" / "quota.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# 配置路径基于本文件定位：优先本目录 free_tier_config.yaml，回退 ../pricing/free_tier.yaml
_BASE = Path(__file__).resolve().parent
_CANDIDATES = [_BASE / "free_tier_config.yaml", _BASE.parent / "pricing" / "free_tier.yaml"]
_CFG = next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[0])
with open(_CFG) as f:
    FREE_CONFIG = yaml.safe_load(f)


def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS developer_accounts (
            phone TEXT PRIMARY KEY,
            nickname TEXT,
            tier TEXT DEFAULT 'personal',
            is_open_source INTEGER DEFAULT 0,
            open_source_repo TEXT,
            registered_at TEXT,
            last_active TEXT
        );
        CREATE TABLE IF NOT EXISTS monthly_quota (
            phone TEXT,
            month TEXT,
            api_calls_used INTEGER DEFAULT 0,
            search_used INTEGER DEFAULT 0,
            storage_used_gb REAL DEFAULT 0,
            PRIMARY KEY (phone, month)
        );
    """)
    conn.commit()
    conn.close()


def register(phone: str, nickname: str = "开发者",
             open_source_repo: str = None) -> dict:
    """注册开发者账号（无需信用卡·无需身份证）"""
    conn = sqlite3.connect(str(DB_PATH))
    tier = "open_source" if open_source_repo else "personal"
    conn.execute("""
        INSERT OR IGNORE INTO developer_accounts
        (phone, nickname, tier, is_open_source, open_source_repo, registered_at)
        VALUES (?,?,?,?,?,?)
    """, (phone, nickname, tier, bool(open_source_repo),
          open_source_repo, datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return {
        "phone": phone,
        "nickname": nickname,
        "tier": tier,
        "welcome": "🎉 欢迎！个人开发者每月享受免费额度，永不收费。",
        "free_quota": FREE_CONFIG["monthly_reset"],
        "no_credit_card": FREE_CONFIG["no_credit_card"],
        "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-DEV-REGISTER-UID9622"
    }


def check_quota(phone: str, resource: str, needed: float = 1) -> dict:
    """检查是否还有免费额度"""
    month = datetime.now().strftime("%Y-%m")
    conn = sqlite3.connect(str(DB_PATH))

    # 获取账户信息
    account = conn.execute(
        "SELECT tier FROM developer_accounts WHERE phone=?", (phone,)
    ).fetchone()
    tier = account[0] if account else "personal"

    # 开源项目无限免费
    if tier == "open_source":
        conn.close()
        return {"allowed": True, "reason": "开源项目·无限免费", "tier": tier}

    # 获取本月使用量
    usage = conn.execute("""
        SELECT api_calls_used, search_used, storage_used_gb
        FROM monthly_quota WHERE phone=? AND month=?
    """, (phone, month)).fetchone()
    conn.close()

    col_map = {
        "api_call": ("api_calls_used", "api_calls"),
        "search":   ("search_used",    "search_queries"),
        "storage":  ("storage_used_gb","storage_gb"),
    }

    _, quota_key = col_map.get(resource, ("api_calls_used", "api_calls"))
    limit = FREE_CONFIG["monthly_reset"].get(quota_key, 0)
    used = (usage[list(col_map.keys()).index(resource)] if usage else 0)

    remaining = limit - used
    allowed = remaining >= needed

    return {
        "allowed": allowed,
        "used": used,
        "limit": limit,
        "remaining": max(0, remaining),
        "reset_date": f"{datetime.now().strftime('%Y-%m')}-{FREE_CONFIG['monthly_reset']['reset_day']:02d}",
        "reason": "免费额度充足" if allowed else f"本月免费额度已用完·可充值继续使用或等下月重置",
        "cost_if_overage": "¥0.0001/次" if resource == "api_call" else "¥0.001/次",
        "tier": tier
    }


@app.route("/quota/register", methods=["POST"])
def api_register():
    data = request.json or {}
    result = register(
        data.get("phone", ""),
        data.get("nickname", "开发者"),
        data.get("open_source_repo")
    )
    return jsonify(result)


@app.route("/quota/check/<phone>/<resource>")
def api_check(phone, resource):
    return jsonify(check_quota(phone, resource))


@app.route("/quota/status/<phone>")
def api_status(phone):
    month = datetime.now().strftime("%Y-%m")
    conn = sqlite3.connect(str(DB_PATH))
    account = conn.execute(
        "SELECT * FROM developer_accounts WHERE phone=?", (phone,)
    ).fetchone()
    usage = conn.execute(
        "SELECT * FROM monthly_quota WHERE phone=? AND month=?",
        (phone, month)
    ).fetchone()
    conn.close()

    if not account:
        return jsonify({"error": "账号不存在·请先注册"}), 404

    free = FREE_CONFIG["monthly_reset"]
    used_api    = usage[2] if usage else 0
    used_search = usage[3] if usage else 0
    used_storage= usage[4] if usage else 0

    return jsonify({
        "account": {"tier": account[2], "nickname": account[1]},
        "month": month,
        "usage": {
            "api_calls":   {"used": used_api,     "free": free["api_calls"],     "remaining": max(0, free["api_calls"]     - used_api)},
            "search":      {"used": used_search,  "free": free["search_queries"],"remaining": max(0, free["search_queries"]- used_search)},
            "storage_gb":  {"used": used_storage, "free": free["storage_gb"],    "remaining": max(0, free["storage_gb"]    - used_storage)},
        },
        "reset_date": f"每月{free['reset_day']}日自动重置",
        "philosophy": "代码应该普惠所有人·个人开发者不应该有门槛",
        "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-QUOTA-STATUS-UID9622"
    })


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=8895, debug=False)
