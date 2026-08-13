#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙戌·乙丑·卯时·䷯井-TRUST-PROTOCOL-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂君子协议 · 诚信评级与违约清算 v1.0

量化道德值 M、人品值 P、诚信值 I，综合信用分 S = 0.4M + 0.3P + 0.3I。
违约上链递增惩罚（20/40/60...），贡献可赎回；三级清算：警示/惩戒/永久标记。

用法:
    python3 08_BIN/lh_trust_protocol.py register <uid> [--name NAME]
    python3 08_BIN/lh_trust_protocol.py contribute <uid> <type> [--desc DESC]
    python3 08_BIN/lh_trust_protocol.py violate <uid> [--desc DESC] [--evidence EVIDENCE]
    python3 08_BIN/lh_trust_protocol.py moral <uid> good|bad [--desc DESC]
    python3 08_BIN/lh_trust_protocol.py character <uid> good|bad [--desc DESC]
    python3 08_BIN/lh_trust_protocol.py query <uid>
    python3 08_BIN/lh_trust_protocol.py audit <uid>
    python3 08_BIN/lh_trust_protocol.py list
    python3 08_BIN/lh_trust_protocol.py rules
    python3 08_BIN/lh_trust_protocol.py version

协议: CC BY-NC-SA 4.0 (思想层) · MulanPSL v2 (工程层)
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.longhun_core.dna_trace import generate_dna

CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
ZERO_PROTOCOL_DNA = "#龍芯⚡️2026-07-03-ZERO-PROTOCOL-WORLD-PEOPLE-SUPREME-v1.0"

DATA_DIR = Path.home() / ".longhun" / "trust_protocol"
DATA_FILE = DATA_DIR / "ledger.json"

DEFAULT_SCORES = {"M": 100.0, "P": 100.0, "I": 100.0}
CONTRIBUTION_TYPES = {
    "code": {"M": 2, "P": 1, "I": 3},
    "doc": {"M": 3, "P": 2, "I": 1},
    "review": {"M": 2, "P": 3, "I": 2},
    "test": {"M": 1, "P": 1, "I": 3},
    "community": {"M": 3, "P": 3, "I": 1},
}


def _load_ledger() -> Dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        return {"version": "1.0", "entries": [], "people": {}}
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"version": "1.0", "entries": [], "people": {}}


def _save_ledger(ledger: Dict[str, Any]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")


def _chain_hash(ledger: Dict[str, Any]) -> str:
    payload = json.dumps(ledger, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _compute_score(person: Dict[str, Any]) -> Dict[str, Any]:
    M = DEFAULT_SCORES["M"]
    P = DEFAULT_SCORES["P"]
    I = DEFAULT_SCORES["I"]
    violations = 0
    for ev in person.get("events", []):
        if ev["type"] == "violate":
            violations += 1
            penalty = 20 * violations
            I -= penalty
        elif ev["type"] == "contribute":
            deltas = CONTRIBUTION_TYPES.get(ev["subtype"], {"M": 1, "P": 1, "I": 1})
            M += deltas["M"]
            P += deltas["P"]
            I += deltas["I"]
        elif ev["type"] == "moral":
            delta = 5 if ev["subtype"] == "good" else -8
            M += delta
        elif ev["type"] == "character":
            delta = 5 if ev["subtype"] == "good" else -8
            P += delta
    M = max(0, min(200, M))
    P = max(0, min(200, P))
    I = max(0, min(200, I))
    S = round(0.4 * M + 0.3 * P + 0.3 * I, 2)
    level = "🟢 正常"
    if S < 40:
        level = "🔴 永久标记"
    elif S < 60:
        level = "🟠 惩戒"
    elif S < 80:
        level = "🟡 警示"
    return {"M": round(M, 1), "P": round(P, 1), "I": round(I, 1), "S": S, "level": level, "violations": violations}


def _add_event(ledger: Dict[str, Any], uid: str, event_type: str, subtype: str = "", desc: str = "", evidence: str = ""):
    if uid not in ledger["people"]:
        print(f"❌ UID 未注册: {uid}", file=sys.stderr)
        sys.exit(2)
    entry = {
        "time": datetime.now().isoformat(),
        "uid": uid,
        "type": event_type,
        "subtype": subtype,
        "desc": desc,
        "evidence": evidence,
    }
    ledger["entries"].append(entry)
    ledger["people"][uid].setdefault("events", []).append(entry)
    ledger["chain_hash"] = _chain_hash(ledger)
    _save_ledger(ledger)


def cmd_register(args: argparse.Namespace):
    ledger = _load_ledger()
    if args.uid in ledger["people"]:
        print(f"⚠️ UID 已存在: {args.uid}")
        return
    ledger["people"][args.uid] = {
        "name": args.name or args.uid,
        "registered_at": datetime.now().isoformat(),
        "events": [],
    }
    ledger["chain_hash"] = _chain_hash(ledger)
    _save_ledger(ledger)
    print(f"✅ 已注册: {args.uid} ({args.name or args.uid})")


def cmd_contribute(args: argparse.Namespace):
    ledger = _load_ledger()
    _add_event(ledger, args.uid, "contribute", subtype=args.type, desc=args.desc)
    score = _compute_score(ledger["people"][args.uid])
    print(f"✅ 贡献已记录: {args.uid} -> {args.type}")
    print(f"   当前信用分 S={score['S']} ({score['level']})")


def cmd_violate(args: argparse.Namespace):
    ledger = _load_ledger()
    _add_event(ledger, args.uid, "violate", desc=args.desc, evidence=args.evidence)
    score = _compute_score(ledger["people"][args.uid])
    print(f"🔴 违约已记录: {args.uid}")
    print(f"   当前信用分 S={score['S']} ({score['level']})")


def cmd_moral(args: argparse.Namespace):
    ledger = _load_ledger()
    _add_event(ledger, args.uid, "moral", subtype=args.action, desc=args.desc)
    score = _compute_score(ledger["people"][args.uid])
    print(f"✅ 道德事件已记录: {args.uid} -> {args.action}")
    print(f"   M={score['M']}, S={score['S']}")


def cmd_character(args: argparse.Namespace):
    ledger = _load_ledger()
    _add_event(ledger, args.uid, "character", subtype=args.action, desc=args.desc)
    score = _compute_score(ledger["people"][args.uid])
    print(f"✅ 人品事件已记录: {args.uid} -> {args.action}")
    print(f"   P={score['P']}, S={score['S']}")


def cmd_query(args: argparse.Namespace):
    ledger = _load_ledger()
    p = ledger["people"].get(args.uid)
    if not p:
        print(f"❌ UID 不存在: {args.uid}", file=sys.stderr)
        sys.exit(2)
    score = _compute_score(p)
    print(f"🐉 UID: {args.uid} ({p.get('name', args.uid)})")
    print(f"   道德值 M={score['M']}")
    print(f"   人品值 P={score['P']}")
    print(f"   诚信值 I={score['I']}")
    print(f"   综合分 S={score['S']} {score['level']}")
    print(f"   违约次数: {score['violations']}")
    print(f"   注册时间: {p.get('registered_at', '-')}")


def cmd_audit(args: argparse.Namespace):
    ledger = _load_ledger()
    p = ledger["people"].get(args.uid)
    if not p:
        print(f"❌ UID 不存在: {args.uid}", file=sys.stderr)
        sys.exit(2)
    score = _compute_score(p)
    report = {
        "dna": generate_dna("TRUST-AUDIT", "UID9622"),
        "confirm": CONFIRM_MARK,
        "zero_protocol": ZERO_PROTOCOL_DNA,
        "uid": args.uid,
        "name": p.get("name", args.uid),
        "score": score,
        "events": p.get("events", []),
        "chain_hash": ledger.get("chain_hash", ""),
        "data_file": str(DATA_FILE),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


def cmd_list(args: argparse.Namespace):
    ledger = _load_ledger()
    if not ledger["people"]:
        print("📭 暂无记录")
        return
    print("🐉 君子协议注册列表\n")
    print(f"{'UID':<20} {'名称':<16} {'S':<8} {'等级':<12} {'违约'}")
    print("-" * 60)
    for uid, p in sorted(ledger["people"].items()):
        score = _compute_score(p)
        print(f"{uid:<20} {p.get('name', uid):<16} {score['S']:<8} {score['level']:<12} {score['violations']}")


def cmd_rules(args: argparse.Namespace):
    print("🐉 龍魂君子协议 · 计算规则\n")
    print("综合信用分 S = 0.4×M + 0.3×P + 0.3×I")
    print("违约惩罚: 第 n 次违约扣 20×n 分（诚信值 I）")
    print("贡献加分: 按类型 code/doc/review/test/community 增加 M/P/I")
    print("道德/人品 good +5, bad -8")
    print("三级清算: S<80 警示, S<60 惩戒, S<40 永久标记")
    print(f"零号协议: {ZERO_PROTOCOL_DNA}")


def cmd_version(args: argparse.Namespace):
    print("龍魂君子协议 v1.0 · DNA: #龍芯⚡️2026-07-05-LONGHUN-TRUST-PROTOCOL-v5.2-a4c7e1d2")


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂君子协议 · 诚信评级")
    sub = parser.add_subparsers(dest="command", help="子命令")

    p_reg = sub.add_parser("register", help="注册新主体")
    p_reg.add_argument("uid")
    p_reg.add_argument("--name", default="")

    p_con = sub.add_parser("contribute", help="记录贡献")
    p_con.add_argument("uid")
    p_con.add_argument("type", choices=list(CONTRIBUTION_TYPES.keys()))
    p_con.add_argument("--desc", default="")

    p_vio = sub.add_parser("violate", help="记录违约")
    p_vio.add_argument("uid")
    p_vio.add_argument("--desc", default="")
    p_vio.add_argument("--evidence", default="")

    p_moral = sub.add_parser("moral", help="记录道德事件")
    p_moral.add_argument("uid")
    p_moral.add_argument("action", choices=["good", "bad"])
    p_moral.add_argument("--desc", default="")

    p_char = sub.add_parser("character", help="记录人品事件")
    p_char.add_argument("uid")
    p_char.add_argument("action", choices=["good", "bad"])
    p_char.add_argument("--desc", default="")

    sub.add_parser("query", help="查询信用分").add_argument("uid")
    sub.add_parser("audit", help="输出完整审计 JSON").add_argument("uid")
    sub.add_parser("list", help="列出所有主体")
    sub.add_parser("rules", help="显示计算规则")
    sub.add_parser("version", help="显示版本")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(2)

    globals()[f"cmd_{args.command}"](args)


if __name__ == "__main__":
    main()
