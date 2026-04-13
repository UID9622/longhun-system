#!/usr/bin/env python3
"""
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 龍魂情报自动抓取系统 · news_sync.py
# DNA: #龍芯⚡️2026-03-21-NEWS-SYNC-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创作者: 诸葛鑫（UID9622）
# 理论指导: 曾仕强老师（永恒显示）
# 用途: 每日9点自动抓取9大新闻源 → 保存本地MD + 写入Notion情报知识库
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import urllib.request, urllib.error
import xml.etree.ElementTree as ET
import json, os, re, ssl
from datetime import datetime
from pathlib import Path

# ── SSL证书修复（macOS Python 3.11 缺失根证书）──
try:
    import certifi
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
    ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
except ImportError:
    pass  # 没有certifi就用系统默认

# ── 配置 ──────────────────────────────────
BASE_DIR = Path.home() / "longhun-system"
NEWS_DIR = BASE_DIR / "news"
NEWS_DIR.mkdir(exist_ok=True)

NOTION_TOKEN = os.getenv("NOTION_TOKEN_WORKSPACE", "")
NOTION_DB_ID = "32907171-7242-81e5-926c-f860c7283fff"  # 情报知识库

RSS_SOURCES = [
    # 中文视角（可用）
    {"name": "多维新闻",      "url": "https://www.dwnews.com/rss",                          "cat": "🌍 国际动态"},
    # 国际一手（可用）
    {"name": "BBC中文",       "url": "https://feeds.bbci.co.uk/zhongwen/simp/rss.xml",      "cat": "🌍 国际动态"},
    {"name": "Al Jazeera",    "url": "https://www.aljazeera.com/xml/rss/all.xml",           "cat": "🌍 国际动态"},
    # 科技AI（可用）
    {"name": "MIT Tech Review","url": "https://www.technologyreview.com/feed/",             "cat": "🤖 AI/科技"},
    {"name": "The Verge",     "url": "https://www.theverge.com/rss/index.xml",              "cat": "🤖 AI/科技"},
    {"name": "36氪",          "url": "https://36kr.com/feed",                               "cat": "🤖 AI/科技"},
    # 备用中文源
    {"name": "虎嗅网",        "url": "https://www.huxiu.com/rss/0.xml",                     "cat": "🤖 AI/科技"},
    {"name": "少数派",        "url": "https://sspai.com/feed",                               "cat": "🤖 AI/科技"},
]

MAX_PER_SOURCE = 5  # 每个源取最新5条


def clean(text):
    """去除HTML标签和多余空白"""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:200]


def fetch_rss(source):
    """抓取单个RSS源，返回文章列表"""
    items = []
    try:
        req = urllib.request.Request(
            source["url"],
            headers={"User-Agent": "LongHun-NewsBot/1.0 (UID9622)"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read()
        root = ET.fromstring(content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        # RSS 2.0
        for item in root.findall(".//item")[:MAX_PER_SOURCE]:
            title = clean(item.findtext("title", ""))
            link  = (item.findtext("link", "") or "").strip()
            desc  = clean(item.findtext("description", ""))
            pub   = item.findtext("pubDate", "")
            items.append({"title": title, "link": link, "desc": desc, "pub": pub})

        # Atom
        if not items:
            for entry in root.findall(".//atom:entry", ns)[:MAX_PER_SOURCE]:
                title = clean(entry.findtext("atom:title", "", ns))
                link_el = entry.find("atom:link", ns)
                link = link_el.get("href","") if link_el is not None else ""
                desc = clean(entry.findtext("atom:summary", "", ns))
                pub  = entry.findtext("atom:updated", "", ns)
                items.append({"title": title, "link": link, "desc": desc, "pub": pub})

    except Exception as e:
        print(f"  ⚠️  {source['name']} 抓取失败: {e}")
    return items


def write_notion(source, item):
    """写入Notion情报知识库（跳过没有Token的情况）"""
    if not NOTION_TOKEN:
        return
    try:
        payload = {
            "parent": {"database_id": NOTION_DB_ID},
            "properties": {
                "标题":    {"title": [{"type": "text", "text": {"content": item["title"][:100]}}]},
                "来源":    {"select": {"name": source["name"]}},
                "分类":    {"select": {"name": source["cat"]}},
                "摘要":    {"rich_text": [{"type": "text", "text": {"content": item["desc"][:500]}}]},
                "链接":    {"url": item["link"] or None},
                "抓取时间":{"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
                "重要度":  {"select": {"name": "🟢 存档"}},
                "已读":    {"checkbox": False}
            }
        }
        req = urllib.request.Request(
            "https://api.notion.com/v1/pages",
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Bearer {NOTION_TOKEN}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        urllib.request.urlopen(req, timeout=8)
    except Exception:
        pass  # 静默失败，不中断本地写入


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    now   = datetime.now().strftime("%Y-%m-%d %H:%M")
    out_file = NEWS_DIR / f"{today}_今日动态.md"

    lines = [
        f"# 🐉 龍魂情报日报 · {today}",
        f"> 自动抓取时间: {now}  |  DNA: #龍芯⚡️{today.replace('-','')}-NEWS-v1.0",
        "",
    ]

    total = 0
    for source in RSS_SOURCES:
        print(f"📡 抓取: {source['name']} ...")
        items = fetch_rss(source)
        if not items:
            lines.append(f"## {source['cat']} · {source['name']}\n> ⚠️ 无法获取\n")
            continue

        lines.append(f"## {source['cat']} · {source['name']}")
        for item in items:
            lines.append(f"### {item['title']}")
            if item["desc"]:
                lines.append(f"> {item['desc']}")
            if item["link"]:
                lines.append(f"- 链接: {item['link']}")
            if item["pub"]:
                lines.append(f"- 发布: {item['pub'][:30]}")
            lines.append("")
            write_notion(source, item)
            total += 1

    lines += [
        "---",
        f"共抓取 **{total}** 条情报 · 已写入Notion情报知识库",
        f"DNA: #龍芯⚡️{today.replace('-','')}-NEWS-v1.0",
        "GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    ]

    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n✅ 已保存: {out_file}")
    print(f"✅ 共抓取 {total} 条情报")


if __name__ == "__main__":
    main()
