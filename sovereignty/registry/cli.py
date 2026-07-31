# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 UID9622 主权注册 CLI
用法：
    lh sovereign register "姓名" "身份证" "110101..." ["设备指纹"] ["GPG公钥路径"]
    lh sovereign verify UID9622-XXXXXX "签名"
    lh sovereign identity UID9622-XXXXXX
    lh sovereign list
    lh sovereign card UID9622-XXXXXX

DNA: #龍芯⚡️20260628-SOVEREIGN-CLI-v1.0
"""

import os
import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from registry import register_sovereign_identity, verify_identity, get_identity, list_identities
from card import generate_card_png


def cmd_register(args):
    gpg_key = ""
    if args.gpg_key_file:
        gpg_key = Path(args.gpg_key_file).read_text(encoding="utf-8")
    result = register_sovereign_identity(
        name=args.name,
        id_type=args.id_type,
        id_number=args.id_number,
        device_fingerprint=args.device_fingerprint or "",
        gpg_public_key=gpg_key,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "success" else 1


def cmd_verify(args):
    result = verify_identity(args.uid, args.signature)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "verified" else 1


def cmd_identity(args):
    record = get_identity(args.uid)
    if not record:
        print(json.dumps({"status": "not_found"}, ensure_ascii=False))
        return 1
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


def cmd_list(args):
    records = list_identities(limit=args.limit)
    print(json.dumps(records, ensure_ascii=False, indent=2))
    print(f"\n📊 共 {len(records)} 条记录")
    return 0


def cmd_card(args):
    result = generate_card_png(args.uid)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "success" else 1


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="lh sovereign", description="龍魂 UID9622 主权注册 CLI")
    sub = parser.add_subparsers(dest="cmd")

    p_reg = sub.add_parser("register", help="注册主权身份")
    p_reg.add_argument("name")
    p_reg.add_argument("id_type")
    p_reg.add_argument("id_number")
    p_reg.add_argument("--device", dest="device_fingerprint", default="")
    p_reg.add_argument("--gpg", dest="gpg_key_file", default=None)

    p_ver = sub.add_parser("verify", help="验证主权身份")
    p_ver.add_argument("uid")
    p_ver.add_argument("signature")

    p_id = sub.add_parser("identity", help="查看主权身份详情")
    p_id.add_argument("uid")

    p_list = sub.add_parser("list", help="列出主权身份")
    p_list.add_argument("--limit", type=int, default=100)

    p_card = sub.add_parser("card", help="生成身份卡")
    p_card.add_argument("uid")

    args = parser.parse_args(argv)

    if args.cmd == "register":
        return cmd_register(args)
    if args.cmd == "verify":
        return cmd_verify(args)
    if args.cmd == "identity":
        return cmd_identity(args)
    if args.cmd == "list":
        return cmd_list(args)
    if args.cmd == "card":
        return cmd_card(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
