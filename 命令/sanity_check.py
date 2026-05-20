#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龲魂 sanity · region_consistency_check + 可选全链路
DNA: #龲芯⚡2026-05-20-SANITY-REGION-v1.0
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills"))

from region_sovereignty import (  # noqa: E402
    region_consistency_check,
    region_lock_check,
    DNA_TAG,
)


def main() -> int:
    print("=" * 60)
    print("sanity_check · region_consistency_check")
    print("DNA:", DNA_TAG)
    print("=" * 60)

    r = region_lock_check()
    print(r.acknowledgment)
    if r.warnings:
        for w in r.warnings:
            print("  🟡", w)
    if r.violations:
        for v in r.violations:
            print("  🔴", v)

    log_dir = ROOT / "logs"
    ok, parts = region_consistency_check(log_dir=log_dir)
    labels = {
        "tz_match": "时区 UTC+8",
        "charset_match": "UTF-8",
        "date_format_match": "ISO8601+08",
        "locale_match": "zh-CN",
        "jsonl_tz_hint": "jsonl 时戳 +08",
    }
    for k, v in parts.items():
        mark = "✓" if v else "✗"
        print(f"  [{mark}] {labels.get(k, k)}")
    print("=" * 60)
    if ok and r.ok:
        print("PASS · 8/8 region sanity")
        return 0
    print("FAIL · 见上")
    return 1


if __name__ == "__main__":
    sys.exit(main())
