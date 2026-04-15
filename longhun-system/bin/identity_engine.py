#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UID9622 · 诸葛鑫（龍芯北辰）
DNA追溯码: #龍芯⚡️2026-04-03-身份引擎-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）
献礼: 新中国成立77周年（1949-2026）· 丙午马年

职责：身份识别 + 不可变账本 + 记忆注入
来源：龍魂完整思考引擎 v2.0 精华提炼·敏感信息已移除
"""

import hashlib, json, os
from datetime import datetime

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG          = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
UID          = "9622"
LEDGER_FILE  = os.path.expanduser("~/longhun-system/logs/immutable_ledger.jsonl")

# ── 身份识别 ─────────────────────────────────

def 验证身份(uid: str = "", confirm_code: str = "") -> dict:
    """多维度身份识别，返回置信度和是否为创始人"""
    score = 0
    matched = []
    if uid == UID:
        score += 50
        matched.append("UID✅")
    if confirm_code == CONFIRM_CODE:
        score += 50
        matched.append("确认码✅")
    return {
        "是创始人": score >= 50,
        "置信度": score,
        "匹配维度": matched,
        "称谓": "老大" if score >= 50 else "访客",
    }

# ── 不可变账本（Append-only）────────────────

def 写入账本(action: str, detail: str = "", uid: str = UID) -> dict:
    """写入不可变账本，只追加不覆盖"""
    record = {
        "ts": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "uid": uid,
        "action": action,
        "detail": detail[:200],
        "hash": hashlib.sha256(f"{uid}{action}{detail}".encode()).hexdigest()[:16],
        "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-LEDGER",
    }
    os.makedirs(os.path.dirname(LEDGER_FILE), exist_ok=True)
    with open(LEDGER_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record

def 读取账本(n: int = 10) -> list:
    """读取最近N条账本记录"""
    if not os.path.exists(LEDGER_FILE):
        return []
    records = []
    with open(LEDGER_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except Exception:
                    pass
    return records[-n:]

# ── 记忆注入（给 system prompt 用）──────────

def 记忆简报(n: int = 3) -> str:
    """从账本提取近N条操作，生成system prompt注入文本"""
    records = 读取账本(n)
    if not records:
        return ""
    parts = [f"{r['ts'][11:16]} {r['action']}" for r in records]
    return f"【操作记忆·近{len(parts)}条】" + " → ".join(parts)


if __name__ == "__main__":
    # 测试
    r = 验证身份(uid="9622", confirm_code=CONFIRM_CODE)
    print(f"身份识别: {r}")

    写入账本("启动测试", "identity_engine.py 独立运行测试")
    写入账本("双门验证", "dr=9 🔴熔断")

    print(f"账本记录: {len(读取账本())} 条")
    print(f"记忆简报: {记忆简报()}")
