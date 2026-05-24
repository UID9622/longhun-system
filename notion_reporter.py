#!/usr/bin/env python3
import requests
import json
import datetime
from pathlib import Path

BASE_DIR = Path.home() / "longhun-system"
LOG_DIR = BASE_DIR / "logs"
CONFIG = json.loads((BASE_DIR / "config.json").read_text(encoding="utf-8"))

NOTION_TOKEN = CONFIG.get("notion_token", "")
NOTION_DB_ID = CONFIG.get("notion_database_id", "")

def push_daily_report():
    log_file = LOG_DIR / "engine_audit.jsonl"
    if not log_file.exists():
        return
    lines = log_file.read_text().strip().split("\n")[-20:]
    logs = [json.loads(l) for l in lines]
    summary = f"龍魂引擎日报 | {datetime.date.today()} | 处理{len(logs)}次识别"
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    payload = {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": summary}}]},
            "Status": {"select": {"name": "已审计"}},
            "Count": {"number": len(logs)},
            "DNA": {"rich_text": [{"text": {"content": "#龍芯⚡️日报"}}]}
        }
    }
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code == 200:
        print(f"🟢 Notion推送成功：{summary}")
    else:
        print(f"🔴 推送失败：{r.status_code} {r.text}")

if __name__ == "__main__":
    push_daily_report()
