#!/usr/bin/env python3
"""
DNA-Calendar → Notion 天罗地网同步器
本地DNA时空胶囊 → Notion数据库双链备份

Author: 诸葛鑫 (UID9622)
DNA: #LONGHUN⚡️2026-03-23-TIANLUODIWANG-v1.1
"""

import os
import json
import sys
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

NOTION_VERSION = "2022-06-28"


class DNANotionSync:
    def __init__(self):
        self.token = os.getenv("NOTION_TOKEN")
        self.db_id = os.getenv("NOTION_DATABASE_ID", "8f5b4ac0baed40d392e6fca1ff3901de")
        self.cnsh  = os.getenv("CNSH_API_URL", "http://127.0.0.1:9622")
        self.user  = os.getenv("USER_ID", "UID9622")

        if not self.token:
            print("❌ 未找到 NOTION_TOKEN")
            sys.exit(1)

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type":  "application/json",
            "Notion-Version": NOTION_VERSION,
        }

    # ── 辅助：Notion REST 调用 ────────────────────────────────

    def _post(self, path: str, body: dict = None) -> dict:
        url = f"https://api.notion.com/v1{path}"
        r = requests.post(url, headers=self.headers, json=body or {}, timeout=15)
        r.raise_for_status()
        return r.json()

    def _get(self, path: str) -> dict:
        url = f"https://api.notion.com/v1{path}"
        r = requests.get(url, headers=self.headers, timeout=15)
        r.raise_for_status()
        return r.json()

    # ── 获取本地事件 ──────────────────────────────────────────

    def fetch_local(self) -> list:
        try:
            r = requests.get(
                f"{self.cnsh}/calendar/events/{self.user}?limit=1000", timeout=10
            )
            r.raise_for_status()
            return r.json().get("events", [])
        except Exception as e:
            print(f"❌ CNSH-64 API连接失败: {e}")
            return []

    # ── 查询Notion已有DNA码 ───────────────────────────────────

    def fetch_notion_existing(self) -> dict:
        existing = {}
        try:
            cursor = None
            while True:
                body = {
                    "filter": {
                        "property": "DNA追溯码",
                        "rich_text": {"is_not_empty": True}
                    },
                    "page_size": 100,
                }
                if cursor:
                    body["start_cursor"] = cursor

                resp = self._post(f"/databases/{self.db_id}/query", body)

                for page in resp.get("results", []):
                    props = page.get("properties", {})
                    arr = props.get("DNA追溯码", {}).get("rich_text", [])
                    if arr:
                        dna = arr[0]["text"]["content"]
                        existing[dna] = page["id"]

                if not resp.get("has_more"):
                    break
                cursor = resp.get("next_cursor")

        except Exception as e:
            print(f"⚠️ 查询Notion已有记录失败: {e}")

        return existing

    # ── 创建单条Notion页面 ────────────────────────────────────

    def push_event(self, event: dict) -> bool:
        try:
            ts = event.get("timestamp") or 0
            dt = datetime.fromtimestamp(ts) if ts else datetime.now()
            # Notion日期：不带时区偏移的本地时间字符串
            date_str = dt.strftime("%Y-%m-%dT%H:%M:%S")

            mood = event.get("mood") or "平静"
            if mood not in ["平静","开心","激动","专注","疲惫","忧虑"]:
                mood = "平静"

            temp = event.get("wx_temp")
            desc = event.get("wx_desc", "") or ""
            wx_text = f"{temp}°C {desc}".strip() if temp else desc

            city = event.get("geo_city", "") or ""
            lat  = event.get("geo_lat") or 0.0
            lng  = event.get("geo_lng") or 0.0
            if lat and lng:
                loc_text = f"{city} ({lat:.4f}, {lng:.4f})".strip()
            else:
                loc_text = city

            try:
                tags = json.loads(event.get("tags", "[]") or "[]")
            except Exception:
                tags = []

            valid_tags = {"工作","重要","生活","系统","里程碑","DNA"}
            tag_props = [{"name": t} for t in tags if t in valid_tags]

            notes = (event.get("notes") or "")[:2000]

            properties = {
                "标题": {
                    "title": [{"text": {"content": event.get("title", "(无标题)")}}]
                },
                "DNA追溯码": {
                    "rich_text": [{"text": {"content": event.get("dna_trace", "")}}]
                },
                "时间戳": {
                    "date": {"start": date_str}
                },
                "心情": {
                    "select": {"name": mood}
                },
                "事件哈希": {
                    "rich_text": [{"text": {"content": (event.get("event_hash") or "")[:16]}}]
                },
                "前一哈希": {
                    "rich_text": [{"text": {"content": (event.get("prev_hash") or "")[:16]}}]
                },
                "同步状态": {
                    "select": {"name": "已同步"}
                },
            }

            if wx_text:
                properties["天气"] = {"rich_text": [{"text": {"content": wx_text}}]}
            if loc_text:
                properties["位置"] = {"rich_text": [{"text": {"content": loc_text}}]}
            if notes:
                properties["备注"] = {"rich_text": [{"text": {"content": notes}}]}
            if tag_props:
                properties["标签"] = {"multi_select": tag_props}

            self._post("/pages", {
                "parent": {"database_id": self.db_id},
                "properties": properties,
            })
            return True

        except Exception as e:
            print(f"   ❌ 写入失败 [{event.get('title')}]: {e}")
            return False

    # ── 主同步 ────────────────────────────────────────────────

    def sync(self, dry_run: bool = False) -> dict:
        line = "═" * 52
        print(line)
        print("🔄  龍魂天罗地网同步器 · 启动")
        print(f"📡  CNSH-64: {self.cnsh}")
        print(f"📓  Notion DB: {self.db_id[:8]}...{self.db_id[-4:]}")
        print(f"👤  用户: {self.user}")
        print(line)

        local = self.fetch_local()
        if not local:
            print("⚠️  本地没有事件，同步结束")
            return {"synced": 0, "skipped": 0, "failed": 0}

        print(f"📦  本地时空胶囊: {len(local)} 个")

        existing = self.fetch_notion_existing()
        print(f"☁️   Notion已有: {len(existing)} 个")

        to_sync = [e for e in local if e.get("dna_trace") not in existing]
        print(f"🆕  待同步: {len(to_sync)} 个\n")

        if dry_run:
            for e in to_sync:
                print(f"  [DRY] {e.get('title')} → {e.get('dna_trace')}")
            return {"dry_run_count": len(to_sync)}

        synced = failed = 0
        for i, event in enumerate(to_sync, 1):
            ok = self.push_event(event)
            if ok:
                synced += 1
                short = (event.get("dna_trace") or "")[-12:]
                print(f"  ✅ [{i}/{len(to_sync)}] {event.get('title')} · ...{short}")
            else:
                failed += 1

        print(f"\n{line}")
        print(f"🎉  新增 {synced} 个 | 已有 {len(existing)} 个 | 失败 {failed} 个")
        if synced > 0:
            print(f"🔒  DNA链已建立天罗地网双链备份")
        print(line)

        return {"synced": synced, "skipped": len(existing), "failed": failed}


if __name__ == "__main__":
    dry = "--dry" in sys.argv
    syncer = DNANotionSync()
    result = syncer.sync(dry_run=dry)
    sys.exit(0 if result.get("failed", 0) == 0 else 1)
