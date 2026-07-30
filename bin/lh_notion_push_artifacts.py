#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·产物推送至 Notion
DNA: #龍芯⚡️丙午·癸未·丁未-NOTION-PUSH-ARTIFACTS-v1.0
功能：把最新产物清单推送到指定 Notion 页面，保持信息不断裂。
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import requests

DNA = "#龍芯⚡️丙午·癸未·丁未-NOTION-PUSH-ARTIFACTS-v1.0"


def load_token() -> str:
    env_path = Path.home() / ".cnsh" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            m = re.match(r"NOTION_TOKEN\s*=\s*['\"]?([^'\"\s]+)['\"]?", line)
            if m:
                return m.group(1)
    token = os.getenv("NOTION_TOKEN")
    if token:
        return token
    print("❌ 未找到 NOTION_TOKEN")
    sys.exit(1)


def extract_page_id(url_or_id: str) -> str:
    m = re.search(r"([a-f0-9]{32})", url_or_id)
    if m:
        return m.group(1)
    return url_or_id.strip().replace("-", "")


def push_artifacts(page_id: str, artifacts: list, token: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"

    children = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": f"🐉 龍魂产物更新 · {datetime.now().strftime('%Y-%m-%d %H:%M')}"}}]
            },
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": f"DNA: {DNA}"}}]
            },
        },
    ]

    for item in artifacts:
        children.append({
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": item}}]
            },
        })

    resp = requests.patch(url, headers=headers, json={"children": children})
    if resp.status_code == 200:
        print(f"✅ 已推送到 Notion 页面 {page_id}")
        return True
    else:
        print(f"❌ 推送失败: {resp.status_code} {resp.text}")
        return False


def main():
    parser = argparse.ArgumentParser(description="推送龍魂产物到 Notion")
    parser.add_argument("page", help="Notion 页面 URL 或页面 ID")
    args = parser.parse_args()

    page_id = extract_page_id(args.page)
    token = load_token()

    artifacts = [
        "产物统一规范 SOP: 01_protocols/LH-ARTIFACT-CREATION-SOP-v1.0.md",
        "自然语言路由器: engines/lh_natural_router.py",
        "自动意图引擎: engines/lh_auto_intent.py",
        "剪贴板守护进程: engines/lh_clipboard_daemon.py",
        "关键字文件整理器: scripts/organize_by_keywords.py",
        "相册整理器: scripts/organize_photos.py",
        "Mac 身体翻译官: bin/lh_mac_translator.py",
        "AGENTS.md / STATE.md 已更新并签名",
        "鲲鹏同步: /opt/longhun-system 已更新",
    ]

    push_artifacts(page_id, artifacts, token)


if __name__ == "__main__":
    main()
