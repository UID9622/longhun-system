"""
龍魂9622·notion_sync.py v2.0
DNA(v∞): #龍芯⚡️丙午·丁酉·辛巳-LONGHUN-EXT-NOTION-SYNC-v2.0-9f2e8d4c
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
功能: 把Chrome里抓到的内容·回写Notion记错本
"""
import os
from datetime import datetime
import httpx
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path.home() / "longhun-engine" / ".env")
except ImportError:
    pass

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
ERRATA_DB_ID = os.getenv("ERRATA_DB_ID", "")

HEADERS = lambda: {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

async def push_errata(text: str, source_url: str = "", source_title: str = "") -> dict:
    """上报记错本到 Notion 数据库"""
    if not NOTION_TOKEN:
        raise ValueError("未配置 NOTION_TOKEN")
    if not ERRATA_DB_ID:
        raise ValueError("未配置 ERRATA_DB_ID")

    payload = {
        "parent": {"database_id": ERRATA_DB_ID},
        "properties": {
            "标题": {"title": [{"text": {"content": text[:80]}}]},
            "原文": {"rich_text": [{"text": {"content": text[:1900]}}]},
            "来源URL": {"url": source_url or None},
            "来源标题": {"rich_text": [{"text": {"content": source_title[:200]}}]},
            "时间": {"date": {"start": datetime.now().isoformat()}},
        }
    }

    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.post(
            "https://api.notion.com/v1/pages",
            headers=HEADERS(),
            json=payload
        )
        r.raise_for_status()
        d = r.json()
        return {"id": d.get("id"), "url": d.get("url")}


async def push_dna_log(dna: str, content: str, page_type: str = "通用") -> dict:
    """DNA 日志写入 Notion"""
    if not NOTION_TOKEN:
        raise ValueError("未配置 NOTION_TOKEN")

    log_db = os.getenv("DNA_LOG_DB_ID", "")
    if not log_db:
        raise ValueError("未配置 DNA_LOG_DB_ID")

    payload = {
        "parent": {"database_id": log_db},
        "properties": {
            "DNA": {"title": [{"text": {"content": dna}}]},
            "内容摘要": {"rich_text": [{"text": {"content": content[:500]}}]},
            "类型": {"select": {"name": page_type}},
            "时间": {"date": {"start": datetime.now().isoformat()}},
        }
    }

    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.post(
            "https://api.notion.com/v1/pages",
            headers=HEADERS(),
            json=payload
        )
        r.raise_for_status()
        d = r.json()
        return {"id": d.get("id"), "url": d.get("url")}
