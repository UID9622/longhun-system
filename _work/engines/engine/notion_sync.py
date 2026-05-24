#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notion 回写 · 记错本 / 审计日志
DNA: #龍芯⚡️2026-04-19-NOTION-SYNC-v1.0

需要 Notion Integration Token（Settings→Connections→Develop）
和 记错本 data_source_id
"""
import os
import httpx

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/longhun-system/engine/.env"))
except ImportError:
    pass

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
ERRATA_DB = os.getenv("ERRATA_DB_ID", "")
NOTION_VERSION = os.getenv("NOTION_VERSION", "2022-06-28")


async def push_errata(text: str, source_url: str = "", source_title: str = ""):
    """推送一条记错本条目"""
    if not NOTION_TOKEN:
        return {"error": "未配置 NOTION_TOKEN", "id": None, "url": None}
    if not ERRATA_DB:
        return {"error": "未配置 ERRATA_DB_ID", "id": None, "url": None}

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    # 注意：Notion 2026 新 API 用 data_source_id，旧的用 database_id
    # 这里给出两种兼容格式
    payload = {
        "parent": {"data_source_id": ERRATA_DB},
        "properties": {
            "标题": {"title": [{"text": {"content": text[:80]}}]},
            "来源URL": {"url": source_url or None},
            "来源标题": {"rich_text": [{"text": {"content": source_title[:200]}}]},
            "原文": {"rich_text": [{"text": {"content": text[:1900]}}]},
        },
    }
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=payload,
            )
            d = r.json()
            if d.get("object") == "error":
                # 降级到 database_id
                payload["parent"] = {"database_id": ERRATA_DB}
                r = await c.post(
                    "https://api.notion.com/v1/pages",
                    headers=headers,
                    json=payload,
                )
                d = r.json()
            return {
                "id": d.get("id"),
                "url": d.get("url"),
                "error": d.get("message") if d.get("object") == "error" else None,
            }
    except Exception as e:
        return {"error": str(e), "id": None, "url": None}


async def search_notion(query: str, limit: int = 10):
    """搜索 Notion 工作区"""
    if not NOTION_TOKEN:
        return {"error": "未配置 NOTION_TOKEN", "results": []}
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(
                "https://api.notion.com/v1/search",
                headers=headers,
                json={"query": query, "page_size": limit},
            )
            d = r.json()
            return {"results": d.get("results", [])[:limit]}
    except Exception as e:
        return {"error": str(e), "results": []}
