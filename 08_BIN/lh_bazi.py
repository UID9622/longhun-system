#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·乙亥·巳时·䷝离-BAZI-CLI-v1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: AGPL-3.0-or-later
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🌀 龍魂八字排盘 CLI v1.0 — lh bazi [--date YYYY-MM-DD] [--time HH:MM] [--json]

与对外薄壳 longhun_cli.core.bazi 同口径（标准排盘算法·零依赖）。
"""

import argparse
import hashlib
import json
import sys
import time
from datetime import date, datetime

TIANGAN = "甲乙丙丁戊己庚辛壬癸"
DIZHI = "子丑寅卯辰巳午未申酉戌亥"
STEM_WUXING = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火",
    "戊": "土", "己": "土", "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}
BRANCH_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水",
}
TIGAN_OFFSET = {0: 2, 1: 4, 2: 6, 3: 8, 4: 0, 5: 2, 6: 4, 7: 6, 8: 8, 9: 0}
SHUTUN_OFFSET = {0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 0, 6: 2, 7: 4, 8: 6, 9: 8}
DAY_EPOCH = (1900, 1, 1)
DAY_EPOCH_BRANCH = 10
PILLAR_WEIGHT = {
    "year": {"stem": 1.0, "branch": 0.8},
    "month": {"stem": 1.5, "branch": 1.2},
    "day": {"stem": 2.0, "branch": 1.6},
    "hour": {"stem": 1.2, "branch": 1.0},
}
WUXING_BY_DR = {1: "水", 2: "火", 3: "木", 4: "金", 5: "土", 6: "水", 7: "火", 8: "木", 9: "金"}
GUA_BY_DR = {1: "乾", 2: "兑", 3: "离", 4: "震", 5: "巽", 6: "坎", 7: "艮", 8: "坤", 9: "离"}
ACTION_ENTER = {1, 2, 3, 4}


def digital_root(value) -> int:
    total = sum(ord(ch) for ch in str(value))
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total if total > 0 else 0


def bazi(date_str: str | None = None, time_str: str | None = None) -> dict:
    """公历日期/时间 → 干支四柱 + 五行强度 + 文化主权节点。"""
    now = datetime.now()
    try:
        if date_str:
            y, m, d = (int(x) for x in date_str.split("-"))
        else:
            y, m, d = now.year, now.month, now.day
        if time_str:
            hh, mm = (int(x) for x in time_str.split(":"))
        else:
            hh, mm = now.hour, now.minute
        date(y, m, d)
    except Exception as e:
        return {"status": "error", "error": f"日期格式错误（应为 YYYY-MM-DD / HH:MM）: {e}"}

    yg, yz = (y - 4) % 10, (y - 4) % 12
    ystem, ybranch = TIANGAN[yg], DIZHI[yz]
    mz = (m + 1) % 12
    mg = (TIGAN_OFFSET[yg] + m - 1) % 10
    mstem, mbranch = TIANGAN[mg], DIZHI[mz]
    days = (date(y, m, d) - date(*DAY_EPOCH)).days
    dg, dz = days % 10, (days + 10) % 12
    dstem, dbranch = TIANGAN[dg], DIZHI[dz]
    hz = ((hh + 1) // 2) % 12
    hg = (SHUTUN_OFFSET[dg] + hz) % 10
    hstem, hbranch = TIANGAN[hg], DIZHI[hz]

    pillars = {
        "year": {"stem": ystem, "branch": ybranch},
        "month": {"stem": mstem, "branch": mbranch},
        "day": {"stem": dstem, "branch": dbranch},
        "hour": {"stem": hstem, "branch": hbranch},
    }
    bazi_str = " ".join(f"{p['stem']}{p['branch']}" for p in pillars.values())

    score: dict = {}
    for key, p in pillars.items():
        w = PILLAR_WEIGHT[key]
        for part, char in (("stem", p["stem"]), ("branch", p["branch"])):
            el = (STEM_WUXING if part == "stem" else BRANCH_WUXING)[char]
            score[el] = score.get(el, 0.0) + w[part]
    dominant = max(score, key=score.get)
    weakest = min(score, key=score.get)

    dr = digital_root(bazi_str)
    return {
        "status": "ok",
        "node_id": f"BAZI-9622-{hashlib.sha256(bazi_str.encode('utf-8')).hexdigest()[:8].upper()}",
        "date": f"{y}-{m:02d}-{d:02d}",
        "time": f"{hh:02d}:{mm:02d}",
        "bazi": bazi_str,
        "pillars": {k: f"{v['stem']}{v['branch']}" for k, v in pillars.items()},
        "wuxing_score": {k: round(v, 2) for k, v in sorted(score.items(), key=lambda x: -x[1])},
        "dominant": dominant,
        "weakest": weakest,
        "digital_root": dr,
        "element": WUXING_BY_DR.get(dr % 10, "土"),
        "gua": GUA_BY_DR.get(dr % 9 or 9, "离"),
        "audit": "🟢" if dr in (1, 2, 3, 4, 5) else "🟡",
        "action": "enter" if dr in ACTION_ENTER else "stay",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }


def main() -> None:
    ap = argparse.ArgumentParser(prog="lh bazi", description="龍魂八字排盘")
    ap.add_argument("--date", default=None, help="出生日期 YYYY-MM-DD（默认今天）")
    ap.add_argument("--time", default=None, help="出生时间 HH:MM（默认当前时刻）")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    node = bazi(args.date, args.time)
    if node.get("status") == "error":
        print(node["error"], file=sys.stderr)
        sys.exit(1)
    if args.json:
        print(json.dumps(node, ensure_ascii=False, indent=2))
    else:
        print(f"🌀 八字 | {node['date']} {node['time']}")
        print(f"  四柱: {node['bazi']}")
        print(f"  五行: 主导{node['dominant']} · 弱势{node['weakest']}")
        print(f"  节点: {node['node_id']} · 审计: {node['audit']}")


if __name__ == "__main__":
    main()
