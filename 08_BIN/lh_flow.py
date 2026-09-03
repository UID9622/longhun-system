#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·乙亥·巳时·䷝离-FLOW-CLI-v1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🌀 龍魂流场 CLI v1.0 — lh flow "<文本>" [--json]

与对外薄壳 longhun_cli.core 同口径（对外接口协议-v1.0.md §4）：
数字根(digital root) + 五行 + 八卦 + 审计色 + action → 标准 Node JSON。
"""

import argparse
import hashlib
import json
import sys
import time

WUXING_BY_DR = {1: "水", 2: "火", 3: "木", 4: "金", 5: "土", 6: "水", 7: "火", 8: "木", 9: "金"}
GUA_BY_DR = {1: "乾", 2: "兑", 3: "离", 4: "震", 5: "巽", 6: "坎", 7: "艮", 8: "坤", 9: "离"}
ACTION_ENTER = {1, 2, 3, 4}


def digital_root(value) -> int:
    s = str(value) if isinstance(value, (int, float)) else str(value)
    total = sum(ord(ch) for ch in s)
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total if total > 0 else 0


def flow(text: str) -> dict:
    dr = digital_root(text)
    return {
        "node_id": f"FLOW-9622-{hashlib.sha256(text.encode('utf-8')).hexdigest()[:8].upper()}",
        "digital_root": dr,
        "element": WUXING_BY_DR.get(dr % 10, "土"),
        "gua": GUA_BY_DR.get(dr % 9 or 9, "离"),
        "audit": "🟢" if dr in (1, 2, 3, 4, 5) else "🟡",
        "action": "enter" if dr in ACTION_ENTER else "stay",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }


def main() -> None:
    ap = argparse.ArgumentParser(prog="lh flow", description="龍魂流场计算")
    ap.add_argument("text", nargs="?", default="龍魂")
    ap.add_argument("--json", action="store_true", help="JSON 可解析输出")
    args = ap.parse_args()

    node = flow(args.text)
    if args.json:
        print(json.dumps(node, ensure_ascii=False, indent=2))
    else:
        print(f"🌀 流场 | {args.text}")
        print(f"  数字根: {node['digital_root']} · 五行: {node['element']} · 八卦: {node['gua']}")
        print(f"  审计: {node['audit']} · 行为: {node['action']}")
        print(f"  节点: {node['node_id']}")


if __name__ == "__main__":
    main()
