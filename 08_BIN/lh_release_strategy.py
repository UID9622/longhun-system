#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-RELEASE-CLI-UID9622
# 创建者: 诸葛鑫（UID9622）
"""🐉 龍魂 · 发布策略 CLI: python3 08_BIN/lh_release_strategy.py --run canary"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from factory.release_strategy import ReleaseStrategy  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 发布策略 CLI")
    parser.add_argument("--run", default="canary", help="策略: canary|gray|full|rollback")
    parser.add_argument("--list", action="store_true", help="列出可用策略")
    args = parser.parse_args()

    if args.list:
        print("可用发布策略:")
        for name in ReleaseStrategy.STRATEGIES:
            cfg = ReleaseStrategy.STRATEGIES[name]
            print(f"  - {name}: {cfg.percentage}% 流量, 观察 {cfg.canary_duration}s")
        return

    strategy = ReleaseStrategy(args.run)
    result = strategy.execute()
    print(f"🚀 发布策略: {result['strategy']} | 状态: {result['status']}")
    for s in result.get('steps', []):
        print(f"  - {s['step']}: {s['status']}")
    print(f"  DNA: {result['dna']}")


if __name__ == "__main__":
    main()
