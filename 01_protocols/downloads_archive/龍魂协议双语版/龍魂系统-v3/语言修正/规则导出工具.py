# P0焊死: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
╔══════════════════════════════════════════════════════════════╗
║  龍魂·规则导出工具 v1.0                                      ║
║  DNA: #龍芯⚡️丙午·癸巳·癸卯·戊午·䷚颐-EXTRACT-RULES-v1.0                   ║
╚══════════════════════════════════════════════════════════════╝

alias 打包 指向这里。
功能：
  - 把当前账本（rules_ledger.jsonl）导出为结构化 JSON
  - 汇总每人的规则命中统计
  - 生成人类可读的规则报告

用法：
  python3 cnsh/extract_rules_to_json.py                    # 导出到 data/rules_export.json
  python3 cnsh/extract_rules_to_json.py --out my.json      # 指定输出文件
  python3 cnsh/extract_rules_to_json.py --summary          # 只显示摘要
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from longhun_rules_engine_v2 import ScoreEngine, Rules, tricolor_gate, CONFIG
except ImportError:
    print("⚠️  找不到 longhun_rules_engine_v2.py")
    sys.exit(1)


def extract_rules_to_json(output_path: str | None = None, summary_only: bool = False) -> dict[str, Any]:
    """
    从账本提取规则命中数据·导出为 JSON。
    """
    engine = ScoreEngine()

    now = datetime.now().isoformat()

    # ── 汇总每人数据 ──
    persons_data = {}
    for evt in engine.history:
        p = evt.person
        if p not in persons_data:
            persons_data[p] = {
                "person": p,
                "score": engine.scores.get(p, 100),
                "tricolor": tricolor_gate(engine.scores.get(p, 100))[0],
                "status": tricolor_gate(engine.scores.get(p, 100))[1],
                "total_events": 0,
                "mistakes": 0,
                "owned": 0,
                "not_owned": 0,
                "stood_up": 0,
                "threats": 0,
                "compensated": 0,
                "events": [],
            }

        d = persons_data[p]
        d["total_events"] += 1
        if evt.mistake:
            d["mistakes"] += 1
            if evt.owned:
                d["owned"] += 1
            else:
                d["not_owned"] += 1
            if evt.stood_up:
                d["stood_up"] += 1
        if evt.threat:
            d["threats"] += 1
        if evt.compensated:
            d["compensated"] += 1

        if not summary_only:
            d["events"].append({
                "event_id": evt.event_id,
                "action": evt.action,
                "timestamp": evt.timestamp,
                "dna": evt.dna,
                "chain_hash": evt.chain_hash,
                "flags": {
                    "mistake": evt.mistake,
                    "owned": evt.owned,
                    "stood_up": evt.stood_up,
                    "threat": evt.threat,
                    "compensated": evt.compensated,
                },
            })

    # ── 规则定义 ──
    rules_def = {
        "R1": Rules.R1_CAN_BE_BAD,
        "R2": Rules.R2_TAKE_IT,
        "R3": Rules.R3_CAN_FIX,
        "R4": Rules.R4_FIGHT,
        "R5": Rules.R5_COMPENSATE,
        "R6": Rules.R6_REPEAT_OFFENDER,
    }

    # ── 最终结构 ──
    export = {
        "meta": {
            "generated_at": now,
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d-%H%M%S')}-RULES-EXPORT-v1.0",
            "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "gpg": CONFIG["gpg"],
            "ledger_path": CONFIG["ledger_path"],
            "total_events": len(engine.history),
            "total_persons": len(persons_data),
        },
        "rules": rules_def,
        "persons": list(persons_data.values()),
        "integrity": {
            "verified": engine.verify_integrity()[0],
            "message": engine.verify_integrity()[1],
        },
    }

    return export


def main():
    parser = argparse.ArgumentParser(description="龍魂·规则导出工具")
    parser.add_argument("--out", default=None, help="输出 JSON 文件路径")
    parser.add_argument("--summary", action="store_true", help="只输出摘要（不含事件列表）")
    args = parser.parse_args()

    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  龍魂·规则导出 v1.0                                         ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    data = extract_rules_to_json(summary_only=args.summary)

    # 默认输出路径
    out_path = args.out or os.path.expanduser("~/.cnsh/data/rules_export.json")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"📊 汇总：")
    print(f"   总事件数：{data['meta']['total_events']}")
    print(f"   总人数：{data['meta']['total_persons']}")
    print(f"   账本完整性：{'✅' if data['integrity']['verified'] else '🔴'} {data['integrity']['message']}")
    print()

    for p in data["persons"]:
        print(f"   {p['tricolor']} {p['person']:8}  分={p['score']:3d}  "
              f"事件={p['total_events']}  错={p['mistakes']}  "
              f"扛={p['owned']}  甩={p['not_owned']}  威胁={p['threats']}")

    print()
    print(f"✅ 已导出到：{out_path}")
    print(f"🔖 DNA：{data['meta']['dna']}")


if __name__ == "__main__":
    main()
