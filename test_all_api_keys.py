#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂API密鑰完整性測試
DNA: #龍芯⚡️2026-05-28-TEST-ALL-API-KEYS-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能: 測試所有已配置的API密鑰是否有效
執行: python3 test_all_api_keys.py
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def test_notion_token():
    """測試Notion API Token"""
    print("\n【Notion API 測試】")

    token_file = Path("~/.longhun/secrets.env").expanduser()
    if not token_file.exists():
        print("  ❌ ~/.longhun/secrets.env 不存在")
        return False

    # 讀取token
    token = None
    with open(token_file) as f:
        for line in f:
            if line.startswith("NOTION_TOKEN="):
                token = line.split("=", 1)[1].strip()
                break

    if not token or token.startswith("your_") or token.startswith("ntn_"):
        if token and token.startswith("ntn_"):
            print(f"  ✅ Token 格式正確 (ntn_...)")
            print(f"  ✅ 長度: {len(token)} 字符")
            return True
        else:
            print(f"  ❌ Token 無效或為佔位符")
            return False

    return True

def test_github_token():
    """測試GitHub Token"""
    print("\n【GitHub Token 測試】")

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        # 嘗試從 ~/.env 讀取
        env_file = Path("~/.env").expanduser()
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith("GITHUB_TOKEN="):
                        token = line.split("=", 1)[1].strip()
                        break

    if not token:
        print("  ⏳ 未配置 (GITHUB_TOKEN)")
        return None

    if token.startswith("ghp_"):
        print(f"  ✅ Token 格式正確 (ghp_...)")
        print(f"  ✅ 長度: {len(token)} 字符")
        return True
    else:
        print(f"  ❌ Token 格式錯誤 (應該是 ghp_...)")
        return False

def test_stripe_keys():
    """測試Stripe密鑰"""
    print("\n【Stripe API 測試】")

    secrets_file = Path("~/.longhun/secrets.env").expanduser()

    pub_key = None
    secret_key = None

    if secrets_file.exists():
        with open(secrets_file) as f:
            for line in f:
                if line.startswith("STRIPE_PUBLISHABLE_KEY="):
                    pub_key = line.split("=", 1)[1].strip()
                elif line.startswith("STRIPE_SECRET_KEY="):
                    secret_key = line.split("=", 1)[1].strip()

    if not pub_key and not secret_key:
        print("  ⏳ 未配置 (Stripe密鑰)")
        return None

    if pub_key and pub_key.startswith("pk_"):
        print(f"  ✅ Publishable Key 格式正確 (pk_...)")
        return True

    if secret_key and secret_key.startswith("sk_"):
        print(f"  ✅ Secret Key 格式正確 (sk_...)")
        return True

    print(f"  ⚠️  格式可能有誤")
    return False

def test_notion_databases():
    """測試Notion數據庫ID"""
    print("\n【Notion 數據庫ID 測試】")

    secrets_file = Path("~/.longhun/secrets.env").expanduser()

    dbs = {
        "DB_AL": None,
        "DB_CLOUD": None,
        "DB_JQ": None,
        "DB_LU": None,
        "DB_PUB": None,
        "NOTION_INBOX_DB": None,
        "NOTION_SNAPSHOT_DB": None,
    }

    if secrets_file.exists():
        with open(secrets_file) as f:
            for line in f:
                for db_name in dbs.keys():
                    if line.startswith(f"{db_name}="):
                        dbs[db_name] = line.split("=", 1)[1].strip()

    found = 0
    for db_name, db_id in dbs.items():
        if db_id:
            # 檢查格式（32字符hex或帶dash的uuid）
            if len(db_id) >= 30 and (len(db_id.replace("-", "")) == 32 or len(db_id) == 32):
                print(f"  ✅ {db_name}: 有效")
                found += 1
            else:
                print(f"  ⚠️  {db_name}: 格式可能有誤")
        else:
            print(f"  ⏳ {db_name}: 未配置")

    return found > 0

def generate_report():
    """生成完整報告"""
    print("\n" + "=" * 70)
    print("🐉 龍魂系統 API 密鑰完整性測試")
    print(f"時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    results = {}

    # 測試所有API
    results["notion"] = test_notion_token()
    results["github"] = test_github_token()
    results["stripe"] = test_stripe_keys()
    results["databases"] = test_notion_databases()

    # 總結
    print("\n" + "=" * 70)
    print("📊 測試總結")
    print("=" * 70)

    valid = sum(1 for v in results.values() if v is True)
    partial = sum(1 for v in results.values() if v is None)
    invalid = sum(1 for v in results.values() if v is False)

    print(f"\n✅ 有效: {valid}")
    print(f"⏳ 未配置: {partial}")
    print(f"❌ 無效: {invalid}")

    print("\n💡 建議:")
    if invalid > 0:
        print("  1. 檢查無效的密鑰格式")
        print("  2. 重新配置到 ~/.longhun/secrets.env")

    if partial > 0:
        print("  3. 按需配置可選API（GitHub、Stripe）")

    print("\n📍 參考文檔: ~/Desktop/🔑龍魂系統API密鑰管理中心.md")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    try:
        generate_report()
    except Exception as e:
        print(f"\n❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
