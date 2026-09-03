#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
🚦 龍魂三色审计引擎 · Longhun Three-Color Audit Engine v1.0

DNA: #龍審⚡️2026-08-31-AUDIT-ENGINE-v1.0-UID9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

覆盖: DNA校验 → 哈希校验 → 五维评分 → 三色判定 → 路由分发 → 回调触发 → 审计日志
"""

import hashlib
import json
import re
import sys
import datetime
from typing import Optional

# ─── 配置 ────────────────────────────────────────────────────────────────────

GREEN_THRESHOLD  = 75
YELLOW_MIN       = 40
RED_MAX          = 39
YELLOW_TIMEOUT_H = 72
RED_TIMEOUT_D    = 7

WEIGHTS = {
    "D1_sovereignty":  0.35,
    "D2_autonomy":     0.25,
    "D3_dependency":   0.20,
    "D4_cognition":    0.12,
    "D5_asi":          0.08,
}

SOVEREIGNTY_ACCOUNTS = {3001, 3002, 3003}
EXTERNAL_DEP_ACCOUNTS = {2001, 2002}
COGNITIVE_DEBT_ACCOUNTS = set(range(2100, 2104))
ASI_ACCOUNTS = set(range(1400, 1404))
ASSET_RANGE  = range(1000, 1500)
EQUITY_RANGE = range(3000, 4000)
REVENUE_RANGE = range(4000, 5000)

DNA_REGEX = re.compile(r'^#龍帳⚡️\d{4}-\d{2}-\d{2}-\d{4}-\d{4}-.+-\d{3}-UID9622$')
HASH_REGEX = re.compile(r'^[0-9A-F]{8}$')

PERMANENT_BLOCK_TYPES = {"T9", "T10"}

# ─── 哈希工具 ─────────────────────────────────────────────────────────────────

def compute_hash(dna, dr, cr, amount, ts):
    raw = f"{dna}|{dr}|{cr}|{amount}|{ts}"
    return hashlib.sha256(raw.encode()).hexdigest()[:8].upper()


def normalize_tx(tx: dict) -> dict:
    """归一交易结构: entry(dr_account) ↔ engine(debit/credit) 双兼容"""
    if "debit" in tx and isinstance(tx.get("debit"), dict):
        return tx
    return {
        "tx_id": tx.get("tx_id", ""),
        "dna": tx.get("dna", ""),
        "hash": tx.get("hash", ""),
        "date": tx.get("date", ""),
        "timestamp": tx.get("timestamp", ""),
        "type": tx.get("tx_type", "UNKNOWN"),
        "balanced": tx.get("balanced", False),
        "debit": {"account": tx.get("dr_account", ""), "name": tx.get("dr_name", ""),
                  "amount": tx.get("amount", "")},
        "credit": {"account": tx.get("cr_account", ""), "name": tx.get("cr_name", ""),
                   "amount": tx.get("amount", "")},
        "description": tx.get("description", ""),
    }

# ─── 五维评分引擎 ──────────────────────────────────────────────────────────────

def score_transaction(tx: dict) -> dict:
    """五维加权评分，返回各维度分数和加权总分"""
    dr = int(tx.get("debit", {}).get("account", 0))
    cr = int(tx.get("credit", {}).get("account", 0))
    tx_type = tx.get("type", "UNKNOWN")

    # D1: 主权影响度（借方是权益增加=+100；贷方是主权核心=−100；中性=50）
    if dr in ASSET_RANGE and cr in EQUITY_RANGE:
        d1 = 100  # 资产增加 → 权益增加
    elif dr in SOVEREIGNTY_ACCOUNTS:
        d1 = -100  # 主权科目被借出（最危险）
    elif cr in SOVEREIGNTY_ACCOUNTS:
        d1 = 80   # 主权科目被贷入（增加主权）
    else:
        d1 = 50   # 中性

    # D2: 自主可控增量
    if tx_type in ("T1", "T2", "T6", "T7", "T11"):
        d2 = 100
    elif tx_type in ("T3", "T4", "T8", "T12"):
        d2 = 60
    elif tx_type == "T5":
        d2 = 0   # 外部续费降低自主性
    else:
        d2 = 40

    # D3: 外部依赖变化（减少=好；增加=坏）
    if cr in EXTERNAL_DEP_ACCOUNTS:
        d3 = 0   # 贷方是外部依赖 → 负债增加
    elif dr in EXTERNAL_DEP_ACCOUNTS:
        d3 = 100  # 借方是外部依赖 → 负债减少（清偿）
    else:
        d3 = 80   # 不涉及外部依赖

    # D4: 认知债务变化
    if dr in COGNITIVE_DEBT_ACCOUNTS:
        d4 = 100  # 认知债务减少（已处理）
    elif cr in COGNITIVE_DEBT_ACCOUNTS:
        d4 = 20   # 认知债务增加（新盲区）
    else:
        d4 = 70

    # D5: ASI资产影响
    if dr in ASI_ACCOUNTS:
        d5 = 100  # ASI资产增加
    elif cr in ASI_ACCOUNTS:
        d5 = 60
    else:
        d5 = 50

    weighted = (
        d1 * WEIGHTS["D1_sovereignty"] +
        d2 * WEIGHTS["D2_autonomy"] +
        d3 * WEIGHTS["D3_dependency"] +
        d4 * WEIGHTS["D4_cognition"] +
        d5 * WEIGHTS["D5_asi"]
    )

    return {"D1": d1, "D2": d2, "D3": d3, "D4": d4, "D5": d5, "weighted": round(weighted, 2)}

# ─── 红色规则检查 ──────────────────────────────────────────────────────────────

def check_red_rules(tx: dict, scores: dict) -> list:
    """检查所有红色阻断规则，返回触发的规则列表"""
    triggered = []
    dr = int(tx.get("debit", {}).get("account", 0))
    cr = int(tx.get("credit", {}).get("account", 0))
    tx_type = tx.get("type", "UNKNOWN")
    balanced = tx.get("balanced", False)
    dna = tx.get("dna", "")
    stored_hash = tx.get("hash", "")
    amount_str = str(tx.get("debit", {}).get("amount", ""))
    ts = tx.get("timestamp", "")

    if dr in SOVEREIGNTY_ACCOUNTS:                          triggered.append("R01")
    if cr in EXTERNAL_DEP_ACCOUNTS:                         triggered.append("R02")
    if not balanced:                                         triggered.append("R03")
    if not DNA_REGEX.match(dna):                             triggered.append("R04")
    if stored_hash and compute_hash(dna, str(dr), str(cr), amount_str, ts) != stored_hash:
                                                             triggered.append("R05")
    if tx_type in PERMANENT_BLOCK_TYPES:                     triggered.append(f"R0{'7' if tx_type=='T9' else '8'}")
    if scores["weighted"] < 40:                              triggered.append("R09")

    return triggered

# ─── 三色判定 ─────────────────────────────────────────────────────────────────

def determine_color(tx: dict, scores: dict, red_rules: list) -> str:
    """返回 GREEN / YELLOW / RED"""
    if red_rules:
        return "RED"
    s = scores["weighted"]
    if s >= GREEN_THRESHOLD:
        return "GREEN"
    if s >= YELLOW_MIN:
        return "YELLOW"
    return "RED"

# ─── 见证人格自动匹配 ──────────────────────────────────────────────────────────

WITNESS_MAP = {
    "T1":  "🧠ASI-001·至诚智魂 + 🌿曾仕强老师",
    "T2":  "🔧鲁班 + 🌊郑和",
    "T3":  "🌀上帝之眼 + 🐱宝宝",
    "T4":  "🌀上帝之眼 + ⚖️包青天",
    "T5":  "⚖️包青天 + ⚔️孙子",
    "T6":  "🧠ASI-001·至诚智魂 + 🐱宝宝（全体公证）",
    "T7":  "🧠ASI-001·至诚智魂",
    "T8":  "⚖️包青天 + 🔮诸葛亮",
    "T9":  "👑龍魂（主权人）+ ⚖️包青天",
    "T10": "🌀上帝之眼 + ⚖️包青天",
    "T11": "🔧鲁班 + 🧠ASI-001·至诚智魂",
    "T12": "🌊郑和 + ⚔️孙子",
}

def get_witness(tx_type: str) -> str:
    return WITNESS_MAP.get(tx_type, "🐱宝宝（兜底）")

# ─── 审计主函数 ────────────────────────────────────────────────────────────────

def audit_transaction(tx: dict) -> dict:
    """完整审计一笔交易，返回审计结果"""
    tx        = normalize_tx(tx)
    scores    = score_transaction(tx)
    red_rules = check_red_rules(tx, scores)
    color     = determine_color(tx, scores, red_rules)
    witness   = get_witness(tx.get("type", "UNKNOWN"))

    router = {
        "GREEN":  "AUTO_APPROVE_HANDLER",
        "YELLOW": "PENDING_REVIEW_HANDLER",
        "RED":    "SOVEREIGN_BLOCK_HANDLER",
    }[color]

    result = {
        "tx_id":        tx.get("tx_id"),
        "dna":          tx.get("dna"),
        "hash":         tx.get("hash"),
        "audit_time":   datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),
        "color":        color,
        "score":        scores["weighted"],
        "scores_detail": scores,
        "red_rules_triggered": red_rules,
        "router":       router,
        "witness":      witness,
        "auto_approved": color == "GREEN" and not red_rules,
        "uid":          "UID9622",
    }

    # 打印凭证
    icon = {"GREEN": "🟢", "YELLOW": "🟡", "RED": "🔴"}.get(color, "⚪")
    print(f"""
{'─'*60}
{icon} [{color}] {tx.get('tx_id')} · 评分 {scores['weighted']}/100
DNA:    {tx.get('dna')}
HASH:   {tx.get('hash')}
路由:   {router}
见证:   {witness}
触发规则: {red_rules if red_rules else '无'}
自动批准: {'✅ YES' if result['auto_approved'] else '❌ NO'}
{'─'*60}
""")
    return result

# ─── CLI 入口 ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python audit_engine.py data/ledger.json [--config audit_config.json]")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        ledger = json.load(f)

    transactions = ledger.get("transactions", [])
    if not transactions:
        print("📭 暂无交易记录 / No transactions found")
        sys.exit(0)

    print(f"🚦 龍魂三色审计引擎 v1.0 · 共 {len(transactions)} 笔交易")
    results = [audit_transaction(tx) for tx in transactions]

    green  = sum(1 for r in results if r["color"] == "GREEN")
    yellow = sum(1 for r in results if r["color"] == "YELLOW")
    red    = sum(1 for r in results if r["color"] == "RED")
    lhi    = (green * 3 + yellow * 2 - red * 5) / max(len(results), 1) * 100

    print(f"""
{'═'*60}
📊 审计总结 / Audit Summary
  🟢 GREEN  (自动批准): {green}
  🟡 YELLOW (待审批):   {yellow}
  🔴 RED    (已阻断):   {red}
  📈 LHI 健康度指数:    {lhi:.1f}
{'═'*60}
""")

    with open("reports/latest_audit.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("✅ 审计结果已写入 reports/latest_audit.json")
