#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创始人行程报备

DNA:#龍芯⚡️2026-06-21-FOUNDER-TRIP-v1.0

用法:
  python founder_trip.py 北京
  python founder_trip.py --list

你说一声，系统随行。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dna_sovereignty_kernel import PeopleSovereigntyGuard


def main():
    guard = PeopleSovereigntyGuard()

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("🐉 创始人行程报备")
        print("  python founder_trip.py <地点>   # 报备将去哪里")
        print("  python founder_trip.py --list   # 查看已报备行程")
        return

    if sys.argv[1] == "--list":
        if not guard.founder_trips:
            print("暂无报备行程")
            return
        for where, when in guard.founder_trips.items():
            print(f"  {where}: {when}")
        return

    where = sys.argv[1]
    print(guard.founder_going_to(where))


if __name__ == "__main__":
    main()
