#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""龍魂·Notion全量同步引擎 v2.0
DNA: #龍芯⚡️丙午·甲申·壬子·亥时·䷗复-NOTION-SYNC-V2-FULL
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）
"""
import json, os, sys, time, hashlib
from datetime import datetime, timezone
from pathlib import Path
import urllib.request, urllib.error

TOKEN_FILE = Path(__file__).parent.parent / "config" / "notion_config.json"
OUTPUT_DIR = Path(__file__).parent.parent / "11_DATA" / "notion_sync_v2"
MIRROR_DIR = OUTPUT_DIR / "mirror"
REPORT_FILE = OUTPUT_DIR / "sync_report.json"
DELTA_FILE = OUTPUT_DIR / "delta_since_2026-07-09.json"
NOTION_VERSION = "2022-06-28"
PAGE_SIZE = 100  # Max per request

def load_token():
    with open(TOKEN_FILE) as f:
        return json.load(f)["notion_token"]

def notion_request(url, method="GET", body=None, token=None):
    if token is None:
        token = load_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"  ❌ HTTP {e.code}: {err_body[:200]}")
        return None

def get_all_databases(token):
    """Get all accessible databases with pagination"""
    dbs = []
    cursor = None
    while True:
        body = {"page_size": 100, "filter": {"property": "object", "value": "database"}}
        if cursor:
            body["start_cursor"] = cursor
        result = notion_request("https://api.notion.com/v1/search", "POST", body, token)
        if not result:
            break
        dbs.extend(result.get("results", []))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    return dbs

def get_db_pages(db_id, token):
    """Get all pages from a database with pagination"""
    pages = []
    cursor = None
    while True:
        body = {"page_size": PAGE_SIZE}
        if cursor:
            body["start_cursor"] = cursor
        result = notion_request(
            f"https://api.notion.com/v1/databases/{db_id}/query", "POST", body, token
        )
        if not result:
            break
        pages.extend(result.get("results", []))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    return pages

def get_block_children(block_id, token):
    """Get block children with pagination"""
    blocks = []
    cursor = None
    while True:
        url = f"https://api.notion.com/v1/blocks/{block_id}/children?page_size=100"
        if cursor:
            url += f"&start_cursor={cursor}"
        result = notion_request(url, "GET", None, token)
        if not result:
            break
        blocks.extend(result.get("results", []))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    return blocks

def extract_title(page):
    """Extract title from a page's properties"""
    props = page.get("properties", {})
    for k, v in props.items():
        if isinstance(v, dict) and v.get("type") == "title":
            texts = v.get("title", [])
            return "".join(t.get("plain_text", "") for t in texts)
    return "Untitled"

def get_page_last_edited(page):
    """Get last edited time"""
    return page.get("last_edited_time", "")

def rich_text_to_md(rich_text_list):
    """Convert Notion rich text array to markdown"""
    parts = []
    for t in rich_text_list:
        text = t.get("plain_text", "")
        annotations = t.get("annotations", {})
        if annotations.get("bold"):
            text = f"**{text}**"
        if annotations.get("italic"):
            text = f"*{text}*"
        if annotations.get("strikethrough"):
            text = f"~~{text}~~"
        if annotations.get("code"):
            text = f"`{text}`"
        href = t.get("href")
        if href:
            text = f"[{text}]({href})"
        parts.append(text)
    return "".join(parts)

def block_to_md(block, indent=0):
    """Convert a Notion block to markdown"""
    btype = block.get("type", "")
    content = block.get(btype, {})
    prefix = "  " * indent
    
    if btype == "paragraph":
        text = rich_text_to_md(content.get("rich_text", []))
        return f"{prefix}{text}\n\n" if text else f"{prefix}\n\n"
    
    elif btype == "heading_1":
        return f"{prefix}# {rich_text_to_md(content.get('rich_text', []))}\n\n"
    elif btype == "heading_2":
        return f"{prefix}## {rich_text_to_md(content.get('rich_text', []))}\n\n"
    elif btype == "heading_3":
        return f"{prefix}### {rich_text_to_md(content.get('rich_text', []))}\n\n"
    
    elif btype == "bulleted_list_item":
        text = rich_text_to_md(content.get("rich_text", []))
        return f"{prefix}- {text}\n"
    elif btype == "numbered_list_item":
        text = rich_text_to_md(content.get("rich_text", []))
        return f"{prefix}1. {text}\n"
    
    elif btype == "to_do":
        checked = content.get("checked", False)
        text = rich_text_to_md(content.get("rich_text", []))
        return f"{prefix}- [{'x' if checked else ' '}] {text}\n"
    
    elif btype == "toggle":
        text = rich_text_to_md(content.get("rich_text", []))
        return f"{prefix}<details>\n{prefix}<summary>{text}</summary>\n\n"
    
    elif btype == "code":
        lang = content.get("language", "plain text")
        code_text = rich_text_to_md(content.get("rich_text", []))
        return f"{prefix}```{lang}\n{code_text}\n{prefix}```\n\n"
    
    elif btype == "quote":
        text = rich_text_to_md(content.get("rich_text", []))
        return f"{prefix}> {text}\n\n"
    
    elif btype == "callout":
        icon = content.get("icon", {}).get("emoji", "")
        text = rich_text_to_md(content.get("rich_text", []))
        return f"{prefix}> {icon} **{text}**\n\n"
    
    elif btype == "divider":
        return f"{prefix}---\n\n"
    
    elif btype == "image":
        url = content.get("file", {}).get("url") or content.get("external", {}).get("url", "")
        caption = rich_text_to_md(content.get("caption", []))
        return f"{prefix}![{caption}]({url})\n\n"
    
    elif btype == "bookmark":
        url = content.get("url", "")
        caption = rich_text_to_md(content.get("caption", []))
        return f"{prefix}[🔖 {caption}]({url})\n\n"
    
    elif btype == "equation":
        expr = content.get("expression", "")
        return f"{prefix}$${expr}$$\n\n"
    
    elif btype == "table":
        return f"{prefix}[📊 Table]\n\n"
    
    elif btype == "child_page":
        title = content.get("title", "Untitled")
        return f"{prefix}📄 **{title}** (child page)\n\n"
    
    elif btype == "child_database":
        title = content.get("title", "Untitled")
        return f"{prefix}🗄️ **{title}** (child database)\n\n"
    
    elif btype == "video":
        url = content.get("file", {}).get("url") or content.get("external", {}).get("url", "")
        return f"{prefix}🎬 [Video]({url})\n\n"
    
    elif btype == "file":
        url = content.get("file", {}).get("url") or content.get("external", {}).get("url", "")
        name = content.get("name", "file")
        return f"{prefix}📎 [{name}]({url})\n\n"
    
    elif btype == "pdf":
        url = content.get("file", {}).get("url") or content.get("external", {}).get("url", "")
        return f"{prefix}📑 [PDF]({url})\n\n"
    
    elif btype == "embed":
        url = content.get("url", "")
        return f"{prefix}🔗 [Embed]({url})\n\n"
    
    elif btype == "link_preview":
        url = content.get("url", "")
        return f"{prefix}🔗 [{url}]({url})\n\n"
    
    elif btype == "synced_block":
        return f"{prefix}[Synced Block]\n\n"
    
    elif btype == "table_of_contents":
        return f"{prefix}[TOC]\n\n"
    
    elif btype == "column_list":
        return f"{prefix}[Columns]\n\n"
    
    else:
        return f"{prefix}[{btype}]\n\n"

def sync_database(db, token):
    """Sync a single database - pull all pages and save"""
    db_title = "".join(t.get("plain_text", "") for t in db.get("title", []))
    db_id = db["id"]
    
    # Safe filename
    safe_name = db_title.replace("/", "-").replace(":", "-").replace(" ", "_")[:80]
    safe_name = "".join(c for c in safe_name if c.isalnum() or c in "_-.")
    if not safe_name:
        safe_name = db_id[:8]
    
    db_dir = MIRROR_DIR / f"{safe_name}_{db_id[:8]}"
    db_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"  📥 {db_title} [{db_id[:8]}]", end=" ", flush=True)
    
    pages = get_db_pages(db_id, token)
    print(f"→ {len(pages)} pages", end="", flush=True)
    
    page_count = 0
    block_count = 0
    new_since_0709 = 0
    
    for page in pages:
        title = extract_title(page)
        page_id = page["id"]
        last_edited = get_page_last_edited(page)
        
        # Check if new since July 9
        if last_edited > "2026-07-09":
            new_since_0709 += 1
        
        # Save page JSON
        page_json_path = db_dir / f"{page_id}.json"
        with open(page_json_path, "w", encoding="utf-8") as f:
            json.dump(page, f, ensure_ascii=False, indent=2)
        
        # Generate markdown from blocks
        blocks = get_block_children(page_id, token)
        block_count += len(blocks)
        
        md_content = f"""# {title}

> **Notion Page ID**: `{page_id}`
> **Database**: {db_title}
> **Last Edited**: {last_edited}
> **Synced**: {datetime.now(timezone.utc).isoformat()}

---

"""
        for block in blocks:
            md_content += block_to_md(block)
        
        # Close toggle blocks
        md_content = md_content.replace("\n\n<details>", "\n</details>\n\n<details>")
        
        md_path = db_dir / f"{page_id}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        page_count += 1
    
    print(f" ✅ {block_count} blocks | new: {new_since_0709}")
    
    return {
        "db_id": db_id,
        "db_title": db_title,
        "pages": page_count,
        "blocks": block_count,
        "new_since_0709": new_since_0709,
        "dir": str(db_dir)
    }

def main():
    print("🐉 龍魂·Notion全量同步引擎 v2.0")
    print(f"  输出目录: {OUTPUT_DIR}")
    print()
    
    token = load_token()
    
    # Step 1: Get all databases
    print("🔍 搜索所有数据库...")
    dbs = get_all_databases(token)
    print(f"   找到 {len(dbs)} 个数据库\n")
    
    # Step 2: Sync each database
    results = []
    total_pages = 0
    total_new = 0
    
    for i, db in enumerate(dbs):
        title = "".join(t.get("plain_text", "") for t in db.get("title", []))
        print(f"[{i+1}/{len(dbs)}]", end=" ")
        try:
            r = sync_database(db, token)
            results.append(r)
            total_pages += r["pages"]
            total_new += r["new_since_0709"]
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append({
                "db_id": db["id"],
                "db_title": title,
                "error": str(e)
            })
    
    # Step 3: Generate report
    print(f"\n{'='*60}")
    print(f"📊 同步完成")
    print(f"  数据库: {len(dbs)}")
    print(f"  总页面: {total_pages}")
    print(f"  7月9日后新增: {total_new}")
    print(f"  输出: {MIRROR_DIR}")
    
    report = {
        "sync_time": datetime.now(timezone.utc).isoformat(),
        "total_databases": len(dbs),
        "total_pages": total_pages,
        "new_since_0709": total_new,
        "databases": results
    }
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"  报告: {REPORT_FILE}")
    print(f"\n{'='*60}")
    
    # Step 4: Delta - pages since July 9
    delta_pages = []
    for db_dir in MIRROR_DIR.iterdir():
        if db_dir.is_dir():
            for page_file in db_dir.glob("*.json"):
                with open(page_file) as f:
                    page = json.load(f)
                if get_page_last_edited(page) > "2026-07-09":
                    delta_pages.append({
                        "id": page["id"],
                        "title": extract_title(page),
                        "last_edited": get_page_last_edited(page),
                        "db_dir": str(db_dir)
                    })
    
    delta_pages.sort(key=lambda x: x["last_edited"], reverse=True)
    
    with open(DELTA_FILE, "w", encoding="utf-8") as f:
        json.dump(delta_pages, f, ensure_ascii=False, indent=2)
    
    print(f"\n🆕 7月9日后增量: {len(delta_pages)} 页 → {DELTA_FILE}")

if __name__ == "__main__":
    main()
