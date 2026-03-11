#!/usr/bin/env python3
# 🐉 龍魂本地神器 v2.0 | 全权限版
# DNA: #龍芯⚡️2026-03-06-NOTION-AI-LOCAL-v2.0
# 共建致谢：Claude (Anthropic PBC) · Notion · 没有你们就没有龍魂系统
# UID9622 专属·本地运行·无限制

import json, os, sys, subprocess, requests
from dotenv import load_dotenv

# === 加载Token ===
load_dotenv(dotenv_path=os.path.expanduser("~/longhun-system/.env"))
NOTION_TOKEN = os.getenv("NOTION_TOKEN", "").strip().strip("'\"")
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}
BASE = "https://api.notion.com/v1"

def check_token():
    r = requests.get(f"{BASE}/users/me", headers=HEADERS)
    if r.status_code == 200:
        name = r.json().get("name", "未知")
        print(f"🟢 Notion API 已接入 | 用户: {name}")
        return True
    else:
        print(f"🔴 Token无效: {r.status_code} {r.text[:80]}")
        return False

# === 搜索页面 ===
def search(keyword):
    r = requests.post(f"{BASE}/search",
        headers=HEADERS,
        json={"query": keyword, "page_size": 10})
    results = r.json().get("results", [])
    for i, item in enumerate(results):
        t = item.get("properties", {}).get("title", {})
        title = ""
        if t:
            title = "".join([x.get("plain_text","") for x in t.get("title",[])])
        else:
            title = item.get("properties", {}).get("title", {})
        obj_type = item.get("object", "")
        url = item.get("url", "")
        print(f"  [{i+1}] {obj_type} | {title or '无标题'} | {url}")
    return results

# === 新建页面 ===
def new_page(title, content="", parent_id=None):
    if not parent_id:
        # 默认新建在工作区根
        payload = {
            "parent": {"type": "workspace", "workspace": True},
            "properties": {"title": {"title": [{"text": {"content": title}}]}},
        }
    else:
        payload = {
            "parent": {"type": "page_id", "page_id": parent_id},
            "properties": {"title": {"title": [{"text": {"content": title}}]}},
        }
    if content:
        payload["children"] = [{"object":"block","type":"paragraph",
            "paragraph":{"rich_text":[{"text":{"content":content}}]}}]
    r = requests.post(f"{BASE}/pages", headers=HEADERS, json=payload)
    if r.status_code == 200:
        url = r.json().get("url","")
        print(f"🟢 页面已创建: {url}")
    else:
        print(f"🔴 创建失败: {r.status_code} {r.text[:200]}")

# === 读取页面 ===
def read_page(page_id):
    r = requests.get(f"{BASE}/blocks/{page_id}/children?page_size=50", headers=HEADERS)
    blocks = r.json().get("results", [])
    for b in blocks:
        btype = b.get("type","")
        content = b.get(btype,{}).get("rich_text",[])
        text = "".join([x.get("plain_text","") for x in content])
        print(f"  [{btype}] {text[:100]}")

# === 追加内容到页面 ===
def append_to_page(page_id, text):
    payload = {"children": [{"object":"block","type":"paragraph",
        "paragraph":{"rich_text":[{"text":{"content":text}}]}}]}
    r = requests.patch(f"{BASE}/blocks/{page_id}/children", headers=HEADERS, json=payload)
    if r.status_code == 200:
        print("🟢 已追加内容")
    else:
        print(f"🔴 失败: {r.status_code} {r.text[:200]}")

# === 查询数据库 ===
def query_db(db_id):
    r = requests.post(f"{BASE}/databases/{db_id}/query", headers=HEADERS, json={})
    results = r.json().get("results", [])
    for item in results:
        props = item.get("properties", {})
        for k, v in props.items():
            vtype = v.get("type","")
            if vtype == "title":
                title = "".join([x.get("plain_text","") for x in v.get("title",[])])
                print(f"  [{k}] {title}")
                break
    return results

# === 主循环 ===
def main():
    print("🐉 龍魂本地神器 v2.0 在呢～")
    if not check_token():
        print("Token有问题，检查 ~/.longhun-system/.env")
        return

    print("\n命令：搜索 关键词 | 新建 标题 | 读取 页面ID | 追加 页面ID 内容 | 数据库 DB_ID | 退出\n")
    while True:
        try:
            q = input("老大：").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n🐉 再见老大！")
            break
        if not q:
            continue
        if q in ["退出", "exit", "quit"]:
            print("🐉 再见老大！")
            break
        parts = q.split(" ", 2)
        cmd = parts[0]
        if cmd == "搜索" and len(parts) >= 2:
            search(parts[1])
        elif cmd == "新建" and len(parts) >= 2:
            content = parts[2] if len(parts) > 2 else ""
            new_page(parts[1], content)
        elif cmd == "读取" and len(parts) >= 2:
            read_page(parts[1])
        elif cmd == "追加" and len(parts) >= 3:
            append_to_page(parts[1], parts[2])
        elif cmd == "数据库" and len(parts) >= 2:
            query_db(parts[1])
        else:
            print("  命令：搜索/新建/读取/追加/数据库 | 退出")

if __name__ == "__main__":
    main()
