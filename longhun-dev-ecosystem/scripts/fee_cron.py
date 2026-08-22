# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · 月费定时任务
DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-DEV-FEE-CRON-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

用法:
  python3 scripts/fee_cron.py --cron-freeze     # 每月1日执行·冻结超期开发者
  python3 scripts/fee_cron.py --stats           # 查看公开统计
  python3 scripts/fee_cron.py --export fee-records --token xxx --format csv
  python3 scripts/fee_cron.py --export contributions --token xxx
  python3 scripts/fee_cron.py --export code-dna --token xxx
  python3 scripts/fee_cron.py --export developers --token xxx

crontab:
  0 0 1 * * cd /opt/longhun-dev-ecosystem && /usr/bin/python3 scripts/fee_cron.py --cron-freeze >> logs/fee_cron.log 2>&1
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.models import SessionLocal  # noqa: E402
from backend.monthly_fee import (  # noqa: E402
    freeze_expired_developers,
    get_public_fee_stats,
    export_fee_records,
    export_contributions,
    export_code_dna,
    export_developers,
)


def main():
    parser = argparse.ArgumentParser(description="龍魂生态 · 月费定时任务")
    parser.add_argument("--cron-freeze", action="store_true", help="冻结超期开发者（每月1日）")
    parser.add_argument("--stats", action="store_true", help="查看公开统计")
    parser.add_argument("--export", choices=["fee-records", "contributions", "code-dna", "developers"], help="导出数据")
    parser.add_argument("--token", default="", help="管理员Token（导出用）")
    parser.add_argument("--format", default="csv", choices=["csv", "json"], help="导出格式")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        if args.cron_freeze:
            result = freeze_expired_developers(db)
            print(f"✅ 冻结任务完成: {result}")
        elif args.stats:
            print(get_public_fee_stats(db))
        elif args.export:
            exporters = {
                "fee-records": export_fee_records,
                "contributions": export_contributions,
                "code-dna": export_code_dna,
                "developers": export_developers,
            }
            result = exporters[args.export](db, args.token, args.format)
            if not result["success"]:
                print(f"❌ {result['error']}")
                sys.exit(1)
            print(result["content"])
        else:
            parser.print_help()
    finally:
        db.close()


if __name__ == "__main__":
    main()
