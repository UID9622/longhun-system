#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐲 龍魂记忆编辑器 · Notion 同步工具 v3.1
DNA: #龍芯⚡️2026-08-05-NOTION-SYNC-UID9622
创建者: 诸葛鑫（UID9622）
协议: MulanPSL v2

用法:
    python3 sync_to_notion.py                    # 同步所有记忆到 Notion
    python3 sync_to_notion.py --since 2026-08-01 # 同步指定日期之后的记忆

环境变量:
    NOTION_TOKEN        Notion Integration Token
    NOTION_MEMORY_DB_ID Notion 数据库 ID

依赖: pip install requests
许可: MulanPSL v2
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

MEMORY_DIR = Path.home() / "Desktop" / "龍魂系统·本地知识库" / "記憶"
INDEX_PATH = MEMORY_DIR / "index.json"

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "").strip()
NOTION_DATABASE_ID = os.environ.get("NOTION_MEMORY_DB_ID", "").strip()

CATEGORY_EMOJI = {
    "atomic_facts": "🔬",
    "scene_memory": "🎬",
    "global_overview": "🌍",
    "chat_history": "💬",
}

# Notion API 数据库必须字段（按 README 建议）
REQUIRED_DB_PROPERTIES = {
    "Name": "title",
    "Category": "select",
    "Tags": "multi_select",
    "DNA": "rich_text",
    "Digital Root": "number",
    "Date": "date",
}


def check_notion_ready():
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        print("⚠️ Notion 未配置，请设置环境变量 NOTION_TOKEN 和 NOTION_MEMORY_DB_ID")
        print("   export NOTION_TOKEN='你的 integration token'")
        print("   export NOTION_MEMORY_DB_ID='你的 database id'")
        return False
    if requests is None:
        print("⚠️ requests 未安装，请运行: pip install requests")
        return False
    return True


def load_index():
    if not INDEX_PATH.exists():
        return []
    try:
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def notion_headers():
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }


def query_existing(dna: str):
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    payload = {"filter": {"property": "DNA", "rich_text": {"equals": dna}}}
    try:
        resp = requests.post(url, headers=notion_headers(), json=payload, timeout=30)
        if resp.status_code == 200:
            return resp.json().get("results", [])
        print(f"  ⚠️  查询 Notion 失败 ({resp.status_code}): {resp.text[:120]}")
    except requests.RequestException as e:
        print(f"  ⚠️  查询 Notion 失败: {e}")
    return []


def create_page(entry: dict):
    category = entry.get("category", "atomic_facts")
    emoji = CATEGORY_EMOJI.get(category, "❓")
    title_text = entry.get("preview", "记忆")[:80]
    tags = [t for t in entry.get("tags", [])[:10] if t]
    dna = entry.get("dna", "")
    date_str = entry.get("date", "")
    digital_root = entry.get("digital_root", 0)
    if not isinstance(digital_root, (int, float)):
        digital_root = 0

    properties = {
        "Name": {"title": [{"text": {"content": f"{emoji} {title_text}"}}]},
        "Category": {"select": {"name": category}},
        "Tags": {"multi_select": [{"name": t} for t in tags]},
        "DNA": {"rich_text": [{"text": {"content": dna}}]},
        "Digital Root": {"number": digital_root},
    }
    if date_str:
        properties["Date"] = {"date": {"start": date_str}}

    children = []
    content_preview = entry.get("preview", "")
    if content_preview:
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": content_preview}}]
            },
        })
    file_name = entry.get("file", "")
    if file_name:
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": f"本地文件: {file_name}"}}]
            },
        })

    body = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "icon": {"emoji": emoji},
        "properties": properties,
        "children": children,
    }

    try:
        resp = requests.post(
            "https://api.notion.com/v1/pages",
            headers=notion_headers(),
            json=body,
            timeout=30,
        )
        if resp.status_code == 200:
            return True, resp.json().get("url", "")
        return False, resp.text
    except requests.RequestException as e:
        return False, str(e)


def sync_to_notion(since_date=None, dry_run=False, limit=None):
    if not check_notion_ready():
        return

    index = load_index()
    if not index:
        print("📭 没有记忆索引，请先保存记忆")
        return

    filtered = [
        e for e in index
        if (not since_date or e.get("date", "") >= since_date)
        and e.get("preview", "").strip()
    ]
    if limit:
        filtered = filtered[:limit]

    if not filtered:
        print(f"📭 没有 {since_date or '任何'} 之后的记忆需要同步")
        return

    print(f"🚀 准备同步 {len(filtered)} 条记忆到 Notion...")
    if dry_run:
        print("🔍 [Dry Run] 不会实际写入")
        for e in filtered:
            category = e.get("category", "atomic_facts")
            emoji = CATEGORY_EMOJI.get(category, "❓")
            print(f"  - {emoji} [{category}] {e.get('preview', '')[:60]} | DNA: {e.get('dna', '')}")
        return

    success = 0
    failed = 0
    skipped = 0
    for i, entry in enumerate(filtered, 1):
        preview = entry.get("preview", "")[:50]
        print(f"  [{i}/{len(filtered)}] {preview}...", end=" ")

        dna = entry.get("dna", "")
        if not dna:
            skipped += 1
            print("⏭️  缺少 DNA")
            continue

        if query_existing(dna):
            skipped += 1
            print("⏭️  已存在")
            continue

        ok, err = create_page(entry)
        if ok:
            success += 1
            print(f"✅ {err}")
        else:
            failed += 1
            print(f"❌ ({err[:120]})")

        # Notion API 限速：每秒约 3 次请求
        if i < len(filtered):
            time.sleep(0.35)

    print(f"\n📊 同步完成：成功 {success} 条，失败 {failed} 条，跳过 {skipped} 条")


def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂记忆编辑器 · Notion 同步工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 sync_to_notion.py                    # 同步全部记忆
  python3 sync_to_notion.py --since 2026-08-01 # 同步指定日期之后的记忆
  python3 sync_to_notion.py --dry-run          # 模拟运行，不写入
  python3 sync_to_notion.py --limit 10         # 只同步最近 10 条
        """,
    )
    parser.add_argument("--since", default=None, help="只同步该日期之后的记忆，格式: YYYY-MM-DD")
    parser.add_argument("--dry-run", action="store_true", help="模拟运行，不实际写入 Notion")
    parser.add_argument("--limit", type=int, default=None, help="最多同步条数")
    args = parser.parse_args()

    if args.since and not __import__('re').match(r"^\d{4}-\d{2}-\d{2}$", args.since):
        print("❌ --since 日期格式错误，应为 YYYY-MM-DD")
        sys.exit(1)

    if args.limit is not None and args.limit <= 0:
        print("❌ --limit 必须大于 0")
        sys.exit(1)

    sync_to_notion(args.since, args.dry_run, args.limit)


if __name__ == "__main__":
    main()
