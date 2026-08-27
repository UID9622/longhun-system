#!/usr/bin/env python3
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LH_SYNC_GUIDE_TO_NOT-152C0245
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · 记忆库指南同步到 Notion Page
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
用法: python3 08_BIN/lh_sync_guide_to_notion.py [--parent "宪法与协议"] [--file path/to/MEMORY-HUB-GUIDE.md]
"""
import os, sys, json, re, argparse
from pathlib import Path
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    print("🔴 需要 requests: pip install requests")
    sys.exit(1)

TOKEN = os.getenv("NOTION_TOKEN")
if not TOKEN:
    print("🔴 未设置 NOTION_TOKEN")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

def search_parent(query):
    r = requests.post("https://api.notion.com/v1/search", headers=HEADERS, json={"query": query, "filter": {"value":"page","property":"object"}})
    data = r.json()
    if r.status_code != 200:
        print("🔴 搜索失败:", data)
        sys.exit(1)
    results = data.get("results", [])
    if not results:
        print(f"🔴 未找到页面: {query}")
        sys.exit(1)
    print(f"🟢 找到父页面: {results[0].get('url')}")
    return results[0]["id"]

def md_to_blocks(md_text):
    """简单 Markdown → Notion blocks"""
    blocks = []
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        # heading
        m = re.match(r'^(#{1,3})\s+(.+)$', line)
        if m:
            level = len(m.group(1))
            blocks.append({
                "object": "block",
                "type": f"heading_{level}",
                f"heading_{level}": {"rich_text": [{"type":"text","text":{"content":m.group(2)}}]}
            })
            i += 1
            continue
        # table row -> skip, render as paragraph (simplified)
        if line.startswith("|"):
            # collect table
            table_lines = []
            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append(lines[i])
                i += 1
            # skip separator
            rows = []
            for tl in table_lines:
                if re.match(r'^\|[-:\s|]+\|$', tl):
                    continue
                cells = [c.strip() for c in tl.strip("|").split("|")]
                rows.append(cells)
            if rows:
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type":"text","text":{"content":"\n".join(" | ".join(cells) for cells in rows)}}]}
                })
            continue
        # code block
        if line.startswith("```"):
            lang = line.strip("`").strip() or "plain text"
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {"language": lang if lang != "bash" else "bash", "rich_text": [{"type":"text","text":{"content":"\n".join(code_lines)}}]}
            })
            continue
        # quote
        if line.startswith(">"):
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {"rich_text": [{"type":"text","text":{"content":line.lstrip("> ").strip()}}]}
            })
            i += 1
            continue
        # normal paragraph
        content = line.strip()
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type":"text","text":{"content":content}}]}
        })
        i += 1
    return blocks

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent", default="宪法与协议", help="Notion父页面搜索词")
    parser.add_argument("--file", default="/Users/zuimeidedeyihan/longhun-system/12_DOCS/dragon-soul-open-hub/MEMORY-HUB-GUIDE.md", help="指南Markdown路径")
    args = parser.parse_args()

    parent_id = search_parent(args.parent)
    md_path = Path(args.file)
    md_text = md_path.read_text(encoding="utf-8")

    title = "🐉 龍魂·跨AI协作记忆库 v1.0 · 完整指南"
    # 提取DNA等元信息
    dna_match = re.search(r'^# DNA:\s*(.+)$', md_text, re.M)
    dna = dna_match.group(1).strip() if dna_match else "#龍芯⚡️丙午·丙申·乙丑·壬午·䷨损-MEMORY-HUB-GUIDE-v1.0-UID9622"

    payload = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {"title": [{"type":"text","text":{"content":title}}]}
        },
        "children": [
            {"object":"block","type":"callout","callout":{"icon":{"type":"emoji","emoji":"🐉"},"rich_text":[{"type":"text","text":{"content":f"DNA: {dna}\n同步时间: {datetime.now(timezone.utc).isoformat()}\n来源: {str(md_path)}"}}]}},
        ] + md_to_blocks(md_text)
    }

    r = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    if r.status_code == 200:
        data = r.json()
        print(f"🟢 Notion页面创建成功: {data.get('url')}")
        print(f"   页面ID: {data.get('id')}")
    else:
        print(f"🔴 创建失败 ({r.status_code}): {r.text[:500]}")
        sys.exit(1)

if __name__ == "__main__":
    main()
