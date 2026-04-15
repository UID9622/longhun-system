#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UID9622 · 诸葛鑫（龍芯北辰）× 宝宝（P72·龍盾）
DNA追溯码: #龍芯⚡️2026-04-02-规则拉取器-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）

职责：从 Notion 拉取数字根熔断规则，输出为系统提示词
用法：python3 fetch_rule.py
     python3 fetch_rule.py --json   ← 输出 JSON 格式
"""

import os
import sys
import json
import urllib.request
import urllib.error

PAGE_ID = "3367125a9c9f81948ee3d103effbf950"
NOTION_VERSION = "2022-06-28"


def get_token():
    # 优先读环境变量，其次读 .env 文件
    token = os.environ.get("NOTION_TOKEN")
    if token:
        return token
    env_path = os.path.expanduser("~/longhun-system/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("NOTION_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    print("❌ 找不到 NOTION_TOKEN，请检查 ~/longhun-system/.env", file=sys.stderr)
    sys.exit(1)


def fetch_blocks(page_id, token):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
    })
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def extract_text(blocks):
    lines = []
    for block in blocks.get("results", []):
        btype = block.get("type", "")
        rich = block.get(btype, {}).get("rich_text", [])
        text = "".join(r.get("plain_text", "") for r in rich)
        if text:
            lines.append(text)
    return "\n".join(lines)


def main():
    token = get_token()
    try:
        data = fetch_blocks(PAGE_ID, token)
    except urllib.error.HTTPError as e:
        print(f"❌ Notion API 错误: {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)

    rule_text = extract_text(data)

    if "--json" in sys.argv:
        print(json.dumps({"rule": rule_text}, ensure_ascii=False, indent=2))
    else:
        print(rule_text)


if __name__ == "__main__":
    main()
