#!/usr/bin/env python3
"""
Notion 页面浏览器 · 终端快速入口
DNA: #龍芯⚡️2026-03-31-NOTION-BROWSE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: 💎 龍芯北辰｜UID9622
理论指导: 曾仕强老师（永恒显示）
"""

import os, sys, json, subprocess
from pathlib import Path
import requests

# ── 读取 token ────────────────────────────────────────────
def load_token():
    env = Path.home() / "longhun-system" / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line.startswith("NOTION_TOKEN=") and not line.startswith("NOTION_TOKEN_"):
                v = line.split("=", 1)[1].strip("'\"")
                # 只保留 ASCII 可打印字符
                return "".join(c for c in v if 32 <= ord(c) < 127)
    return os.environ.get("NOTION_TOKEN", "")

TOKEN = load_token()
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def notion_request(method, path, body=None):
    url = f"https://api.notion.com/v1{path}"
    try:
        resp = requests.request(method, url, headers=HEADERS, json=body, timeout=10)
        return resp.json()
    except Exception as e:
        print(f"🔴 Notion API 错误: {e}")
        return {}

def get_title(page):
    props = page.get("properties", {})
    for v in props.values():
        if v.get("type") == "title":
            t = v.get("title", [])
            if t:
                return t[0].get("plain_text", "")
    return "(无标题)"

def get_pages(query=""):
    body = {"filter": {"value": "page", "property": "object"}, "page_size": 50}
    if query:
        body["query"] = query
    d = notion_request("POST", "/search", body)
    return d.get("results", [])

def open_url(url):
    subprocess.Popen(["open", url])

def page_url(page_id):
    return f"https://notion.so/{page_id.replace('-','')}"

# ══════════════════════════════════════════════════════════
# 主界面
# ══════════════════════════════════════════════════════════

def main():
    if not TOKEN:
        print("🔴 NOTION_TOKEN 未配置")
        sys.exit(1)

    # 命令行参数：直接搜索
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  📖 龍魂 Notion 页面浏览器")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    pages = get_pages(query)
    if not pages:
        print("  没有找到页面")
        return

    if query:
        print(f"  搜索「{query}」，找到 {len(pages)} 个结果\n")
    else:
        print(f"  共 {len(pages)} 个页面，输入编号打开，s=搜索，q=退出\n")

    for i, p in enumerate(pages, 1):
        title = get_title(p)
        print(f"  {i:2d}. {title[:55]}")

    print()

    while True:
        try:
            cmd = input("  ❯ ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if cmd.lower() == "q" or not cmd:
            break

        if cmd.lower().startswith("s "):
            # 重新搜索
            kw = cmd[2:].strip()
            pages = get_pages(kw)
            print(f"\n  搜索「{kw}」，找到 {len(pages)} 个\n")
            for i, p in enumerate(pages, 1):
                title = get_title(p)
                print(f"  {i:2d}. {title[:55]}")
            print()
            continue

        if cmd.isdigit():
            idx = int(cmd) - 1
            if 0 <= idx < len(pages):
                p = pages[idx]
                title = get_title(p)
                url = page_url(p["id"])
                print(f"  🔗 打开: {title[:40]}")
                open_url(url)
            else:
                print(f"  编号超范围，1-{len(pages)}")
            continue

        # 当做搜索词
        pages = get_pages(cmd)
        print(f"\n  搜索「{cmd}」，找到 {len(pages)} 个\n")
        for i, p in enumerate(pages, 1):
            title = get_title(p)
            print(f"  {i:2d}. {title[:55]}")
        print()

if __name__ == "__main__":
    main()
