#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
📈 龍魂健康度指数计算器 · Longhun Health Index (LHI) Calculator v1.0

DNA: #龍審⚡️2026-08-31-LHI-CALCULATOR-v1.0-UID9622
LHI = (绿色×3 + 黄色已批准×2 - 红色阻断×5) / 总交易数 × 100
"""

import json
import sys

LEVELS = [
    (90, "🟢 卓越（高度主权自治）"),
    (70, "🟢 健康"),
    (50, "🟡 警戒（外部依赖偏高）"),
    (30, "🔴 危险（主权风险累积）"),
    (0,  "🔴 紧急（需立即主权人介入）"),
]


def classify_lhi(lhi: float) -> str:
    for threshold, label in LEVELS:
        if lhi >= threshold:
            return label
    return LEVELS[-1][1]


def calculate_lhi(audit_results: list) -> dict:
    total  = len(audit_results)
    green  = sum(1 for r in audit_results if r.get("color") == "GREEN")
    yellow = sum(1 for r in audit_results if r.get("color") == "YELLOW" and r.get("auto_approved"))
    red    = sum(1 for r in audit_results if r.get("color") == "RED")

    lhi = (green * 3 + yellow * 2 - red * 5) / max(total, 1) * 100
    lhi = max(0, min(100, lhi))  # clamp 0-100

    return {
        "lhi": round(lhi, 1),
        "level": classify_lhi(lhi),
        "breakdown": {"total": total, "green": green, "yellow_approved": yellow, "red": red},
    }


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "reports/latest_audit.json"
    with open(src, encoding="utf-8") as f:
        data = json.load(f)
    result = calculate_lhi(data if isinstance(data, list) else data.get("transactions", []))
    print(f"\n📈 LHI = {result['lhi']}  →  {result['level']}")
    print(json.dumps(result, ensure_ascii=False, indent=2))
