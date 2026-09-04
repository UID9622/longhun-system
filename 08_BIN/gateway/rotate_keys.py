#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙魂API网关 · 密钥自动轮换（第五锁）
DNA: #龍芯⚡️2026-08-31-GATEWAY-KEY-ROTATION-v1.0-UID9622
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

用法:
  python3 rotate_keys.py --check     # 只列出需要轮换的密钥
  python3 rotate_keys.py --rotate    # 轮换并打印新 secret（仅此一次）
  python3 rotate_keys.py --dry-run   # 演练不落库

配合 cron（每日 03:00）:
  0 3 * * * cd /path/gateway && python3 rotate_keys.py --rotate >> rotation.log 2>&1
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from auth import get_keys_for_rotation, rotate_key  # noqa: E402
from config import load_config  # noqa: E402


def main() -> None:
    cfg = load_config()
    max_days = int(cfg.get("key_rotation", {}).get("max_age_days", 90))

    parser = argparse.ArgumentParser(description="龙魂API网关 密钥轮换")
    parser.add_argument("--check", action="store_true", help="列出需要轮换的密钥")
    parser.add_argument("--rotate", action="store_true", help="轮换到期密钥并输出新 secret")
    parser.add_argument("--dry-run", action="store_true", help="演练，不落库")
    args = parser.parse_args()

    due = get_keys_for_rotation(max_age_days=max_days)
    now = datetime.now(timezone.utc).isoformat()

    if not due:
        print(f"[OK] {now} 无到期密钥（{max_days} 天窗口）")
        return

    if args.check or args.dry_run:
        print(f"[INFO] {now} 待轮换 {len(due)} 个密钥:")
        for k in due:
            print(f"  - {k['key_id']} | {k['owner']} | plan={k['plan']} | created={k['created_at'][:10]} | last={k['last_rotated'][:10] if k['last_rotated'] else 'never'}")
        return

    if args.rotate:
        print(f"[ROTATE] {now} 轮换 {len(due)} 个密钥:")
        for k in due:
            new_secret = rotate_key(k["key_id"])
            print(f"  ✅ {k['key_id']} 新 secret: {new_secret}")
            print(f"     ⚠️ 此 secret 仅本次输出，请通知 {k['owner']} 更新客户端")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
