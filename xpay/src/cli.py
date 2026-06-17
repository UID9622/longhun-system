#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XPay 主權網關 CLI 演示
DNA: #龍芯⚡️2026-06-17-XPAY-CLI-v2.0
"""
import argparse
import json
import sys
from pathlib import Path

# 確保能從項目根目錄導入
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from xpay.src.core import SovereignGateway


def main():
    parser = argparse.ArgumentParser(description="龍魂主權支付網關 v2.0")
    sub = parser.add_subparsers(dest="command", required=True)

    # currencies
    sub.add_parser("currencies", help="列出支持的幣種與主權信息")

    # pay
    pay_parser = sub.add_parser("pay", help="發起一筆演示支付")
    pay_parser.add_argument("amount", type=float, help="金額")
    pay_parser.add_argument("currency", help="幣種代碼，例如 CNY")
    pay_parser.add_argument("recipient", help="收款方 UID")
    pay_parser.add_argument("--sender", default="UID9622", help="付款方 UID")
    pay_parser.add_argument("--memo", default="", help="備註")

    # query
    query_parser = sub.add_parser("query", help="查詢交易")
    query_parser.add_argument("tx_id", help="交易 ID")

    # stats
    sub.add_parser("stats", help="交易統計")

    # migrate
    sub.add_parser("migrate", help="從舊版 transactions.json 遷移數據")

    args = parser.parse_args()

    gateway = SovereignGateway()

    if args.command == "currencies":
        print("支持的幣種：")
        for code in gateway.supported_currencies():
            info = gateway.sovereign_info(code)
            print(f"\n  {info.currency_code} · {info.issuer}")
            print(f"    國家: {info.country_code}")
            print(f"    點對點: {'✅' if info.p2p_capable else '⏳'}")
            print(f"    可追蹤: {'✅' if info.traceable else '⏳'}")
            print(f"    不可篡改: {'✅' if info.immutable else '⏳'}")
            print(f"    DNA 審計: {info.audit_score}/12")
            print(f"    狀態: {info.status}")

    elif args.command == "pay":
        result = gateway.pay(
            amount=args.amount,
            currency=args.currency,
            recipient=args.recipient,
            sender=args.sender,
            memo=args.memo
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == "query":
        tx = gateway.query(args.tx_id)
        if tx:
            print(json.dumps(tx, indent=2, ensure_ascii=False))
        else:
            print(f"❌ 找不到交易：{args.tx_id}")

    elif args.command == "stats":
        print(json.dumps(gateway.stats(), indent=2, ensure_ascii=False))

    elif args.command == "migrate":
        legacy = Path.home() / ".龍魂" / "xpay" / "transactions.json"
        result = gateway.migrate_legacy(legacy)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("遷移後統計：")
        print(json.dumps(gateway.stats(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
