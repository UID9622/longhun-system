#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-ROLLBACK-CLI-UID9622
# 创建者: 诸葛鑫（UID9622）
"""🐉 龍魂 · 回滚 CLI: python3 08_BIN/lh_rollback.py --version v1.0.0"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from factory.rollback_pipeline import RollbackPipeline  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 回滚 CLI")
    parser.add_argument("--version", help="回滚到指定版本")
    parser.add_argument("--list", action="store_true", help="列出可回滚版本")
    parser.add_argument("--deploy-dir", default=str(Path.home() / ".longhun" / "factory" / "deploy"),
                        help="部署目录")
    args = parser.parse_args()

    pipeline = RollbackPipeline(Path(args.deploy_dir))

    if args.list:
        versions = pipeline.list_versions()
        if not versions:
            print("（暂无版本记录）")
            return
        for v in versions:
            print(f"  {v['version']} @ {v['timestamp']}")
        return

    if args.version:
        result = pipeline.rollback(args.version)
        print(f"⏪ 回滚: {result['status']}")
        if result.get('error'):
            print(f"  ❌ {result['error']}")
        else:
            print(f"  DNA: {result['dna']}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
