#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UID9622 · 诸葛鑫（龍芯北辰）
DNA追溯码: #龍芯⚡️2026-04-02-CS知识库拉取-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）
献礼: 新中国成立77周年（1949-2026）· 丙午马年

职责：从Notion计算机科学知识库拉取所有卡片，缓存到本地JSON
数据库ID: 3367125a9c9f808a9692f0c6752e92fa
"""

import json, os, sys, urllib.request, urllib.error

NOTION_API = "https://api.notion.com/v1"
DB_ID = "3367125a9c9f808a9692f0c6752e92fa"
CACHE_FILE = os.path.expanduser("~/longhun-system/bin/cs_cards_cache.json")


def get_notion_token():
    token = os.environ.get("NOTION_TOKEN")
    if token:
        return token
    for path in [
        os.path.expanduser("~/longhun-system/.env"),
        os.path.expanduser("~/.env"),
    ]:
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("NOTION_TOKEN="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def notion_request(method, path, body=None):
    token = get_notion_token()
    if not token:
        raise RuntimeError("NOTION_TOKEN 未配置")
    url = NOTION_API + path
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def fetch_block_text(block_id):
    """递归提取页面所有文字内容"""
    lines = []
    try:
        result = notion_request("GET", f"/blocks/{block_id}/children")
        for block in result.get("results", []):
            btype = block.get("type", "")
            content = block.get(btype, {})
            rich = content.get("rich_text", [])
            text = "".join(t.get("plain_text", "") for t in rich)
            if text.strip():
                lines.append(text.strip())
            # 递归子块（heading里有内容时）
            if block.get("has_children"):
                lines.extend(fetch_block_text(block["id"]))
    except Exception as e:
        lines.append(f"[内容拉取失败: {e}]")
    return lines


def fetch_all_cards():
    """查询数据库，拉取所有卡片"""
    print("🔄 查询计算机科学知识库...")
    result = notion_request("POST", f"/databases/{DB_ID}/query", {
        "page_size": 50
    })
    pages = result.get("results", [])
    print(f"🟢 找到 {len(pages)} 张卡片")

    cards = []
    for page in pages:
        # 取标题
        props = page.get("properties", {})
        title = ""
        for key in ["名称", "Name", "题目", "标题"]:
            if key in props:
                rich = props[key].get("title", [])
                title = "".join(t.get("plain_text", "") for t in rich)
                if title:
                    break

        if not title:
            # 兜底：取任何title类型的字段
            for v in props.values():
                if v.get("type") == "title":
                    rich = v.get("title", [])
                    title = "".join(t.get("plain_text", "") for t in rich)
                    if title:
                        break

        page_id = page["id"]
        print(f"  📄 拉取: {title or page_id}")

        # 拉取页面正文
        content_lines = fetch_block_text(page_id)
        content = "\n".join(content_lines)

        # 提取关键词（用于匹配用户问题）
        keywords = extract_keywords(title)

        cards.append({
            "id": page_id,
            "title": title,
            "keywords": keywords,
            "content": content[:3000],  # 最多3000字
        })

    return cards


def extract_keywords(title: str) -> list:
    """从标题提取关键词，用于问题匹配"""
    kw_map = {
        "进程": ["进程", "线程", "协程", "process", "thread"],
        "TCP": ["TCP", "握手", "挥手", "三次握手", "四次挥手", "连接"],
        "ACID": ["ACID", "事务", "原子性", "一致性", "隔离", "持久性", "数据库"],
        "大O": ["大O", "复杂度", "时间复杂度", "空间复杂度", "算法", "O(n)"],
        "堆": ["堆", "栈", "内存", "指针", "引用", "heap", "stack"],
    }
    result = []
    for key, words in kw_map.items():
        if any(k in title for k in [key] + words):
            result.extend(words)
    # 去重
    return list(dict.fromkeys(result))


def save_cache(cards):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)
    size = os.path.getsize(CACHE_FILE)
    print(f"🟢 缓存已写入: {CACHE_FILE} ({size} bytes)")


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []


def find_relevant_card(user_text: str, cards: list) -> dict | None:
    """根据用户问题找最相关的卡片"""
    text_lower = user_text.lower()
    best = None
    best_score = 0
    for card in cards:
        score = 0
        for kw in card.get("keywords", []):
            if kw.lower() in text_lower:
                score += 1
        # 标题直接出现加分
        if card["title"] and card["title"].lower() in text_lower:
            score += 3
        if score > best_score:
            best_score = score
            best = card
    return best if best_score > 0 else None


if __name__ == "__main__":
    try:
        cards = fetch_all_cards()
        save_cache(cards)
        print(f"\n✅ 共拉取 {len(cards)} 张卡片")
        for c in cards:
            print(f"  • {c['title']} ({len(c['content'])} 字) 关键词: {c['keywords'][:3]}")
    except Exception as e:
        print(f"🔴 拉取失败: {e}")
        sys.exit(1)
