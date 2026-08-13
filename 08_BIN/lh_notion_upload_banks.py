#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""龍魂·面试题库 Notion 直传引擎 v1.0
DNA: #龍芯⚡️丙午·甲申·壬子·亥时·䷗复-INTERVIEW-BANKS-NOTION-UPLOAD-v1.0
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2
"""
import json, os, re, time, sys
import urllib.request, urllib.error

TOKEN = "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"
NOTION_API = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}
PAGE_SIZE = 2000  # Notion text block limit
BANKS_DIR = "/Users/zuimeidedeyihan/_work/interview-question-banks"
PARENT_PAGE_ID = None  # Will create new top-level page as container

def notion(method, path, data=None):
    """Call Notion API"""
    url = f"{NOTION_API}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": str(e.code), "body": e.read().decode()[:500]}

def split_blocks(text, max_len=PAGE_SIZE):
    """Split long text into Notion-friendly blocks"""
    blocks = []
    # Split by paragraphs first
    paragraphs = text.split("\n\n")
    current = ""
    for para in paragraphs:
        if len(current) + len(para) + 2 > max_len:
            if current:
                blocks.append(current.strip())
            current = para
        else:
            current = current + "\n\n" + para if current else para
    if current:
        blocks.append(current.strip())
    return blocks

def text_block(content):
    """Create a paragraph block"""
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": content[:PAGE_SIZE]}}]
        }
    }

def heading_block(content, level=1):
    """Create a heading block"""
    return {
        "object": "block",
        "type": f"heading_{level}",
        f"heading_{level}": {
            "rich_text": [{"type": "text", "text": {"content": content[:500]}}]
        }
    }

def divider_block():
    return {"object": "block", "type": "divider", "divider": {}}

def code_block(content, language="plain text"):
    """Create a code block"""
    return {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": content[:PAGE_SIZE]}}],
            "language": language
        }
    }

def parse_markdown_to_blocks(md_text):
    """Parse markdown text to Notion blocks"""
    blocks = []
    lines = md_text.split("\n")
    i = 0
    code_buffer = ""
    in_code = False
    code_lang = "plain text"
    
    while i < len(lines):
        line = lines[i]
        
        # Code fence detection
        if line.strip().startswith("```"):
            if in_code:
                # End code block
                if code_buffer.strip():
                    blocks.append(code_block(code_buffer.strip()[:PAGE_SIZE], code_lang))
                code_buffer = ""
                in_code = False
            else:
                in_code = True
                code_lang = line.strip()[3:].strip() or "plain text"
            i += 1
            continue
        
        if in_code:
            code_buffer += line + "\n"
            i += 1
            continue
        
        # Headings
        if line.startswith("#### "):
            blocks.append(heading_block(line[5:], 3))
        elif line.startswith("### "):
            blocks.append(heading_block(line[4:], 2))
        elif line.startswith("## "):
            blocks.append(heading_block(line[3:], 2))
        elif line.startswith("# "):
            blocks.append(heading_block(line[2:], 1))
        elif line.strip() == "---":
            blocks.append(divider_block())
        elif line.strip().startswith("|") and "|" in line:
            # Table row - keep as text paragraph
            blocks.append(text_block(line[:PAGE_SIZE]))
        elif line.strip():
            blocks.append(text_block(line[:PAGE_SIZE]))
        else:
            blocks.append(text_block(""))
        
        i += 1
    
    # Flush remaining code
    if code_buffer.strip():
        blocks.append(code_block(code_buffer.strip()[:PAGE_SIZE], code_lang))
    
    return blocks

def create_page(parent_id, title):
    """Create a simple Notion page under parent"""
    data = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {
                "type": "title",
                "title": [{"type": "text", "text": {"content": title}}]
            }
        }
    }
    return notion("POST", "/pages", data)

def append_blocks(page_id, blocks, chunk_size=100):
    """Append blocks to page in chunks (Notion limit: 100 blocks per call)"""
    total = len(blocks)
    appended = 0
    for start in range(0, total, chunk_size):
        chunk = blocks[start:start + chunk_size]
        result = notion("PATCH", f"/blocks/{page_id}/children", {"children": chunk})
        if "error" in result:
            print(f"  ⚠️ Block append error at {start}: {result['error']}")
            # Try one by one
            for b in chunk:
                r = notion("PATCH", f"/blocks/{page_id}/children", {"children": [b]})
                if "error" in r:
                    print(f"    ❌ Single block fail")
                else:
                    appended += 1
            time.sleep(0.5)
        else:
            appended += len(chunk)
        time.sleep(0.3)
    return appended

def main():
    print("🐉 龍魂·面试题库 Notion 直传引擎")
    print("=" * 60)
    
    # Step 1: Find or create container page
    print("\n📁 查找/创建「面试题库」容器页...")
    
    # Search for existing interview banks page
    search_result = notion("POST", "/search", {
        "query": "面试题库",
        "filter": {"property": "object", "value": "page"}
    })
    
    parent_id = None
    if "results" in search_result and search_result["results"]:
        for r in search_result["results"]:
            title = ""
            props = r.get("properties", {})
            for k, v in props.items():
                if isinstance(v, dict) and v.get("type") == "title":
                    title = "".join([t.get("plain_text", "") for t in v.get("title", [])])
            if "面试题库" in title:
                parent_id = r["id"]
                print(f"  ✅ 找到已有容器: {title} ({parent_id[:8]}...)")
                break
    
    if not parent_id:
        # Need to create under a known page - search for any accessible page
        print("  未找到，创建新容器...")
        # Use the workspace root - search for a known parent
        search_all = notion("POST", "/search", {"page_size": 1})
        if "results" in search_all and search_all["results"]:
            root_page = search_all["results"][0]
            root_id = root_page.get("parent", {}).get("page_id") or root_page.get("id")
            if root_page.get("parent", {}).get("type") != "workspace":
                root_id = root_page["id"]
            # Create the container
            cont = create_page(root_id, "📚 面试题库")
            if "id" in cont:
                parent_id = cont["id"]
                print(f"  ✅ 已创建容器: {parent_id[:8]}...")
            else:
                print(f"  ❌ 创建失败: {cont}")
                return
        else:
            print("  ❌ 无法获取根页面")
            return
    
    # Step 2: Process each bank file
    files = sorted([f for f in os.listdir(BANKS_DIR) if f.endswith(".md")])
    print(f"\n📚 待同步: {len(files)} 份题库\n")
    
    results = []
    for filename in files:
        filepath = os.path.join(BANKS_DIR, filename)
        name = filename.replace("-interview-question-bank-v1.0.md", "").upper()
        lang_map = {
            "JS": "JavaScript", "TS": "TypeScript", "GO": "Go",
            "SQL": "SQL", "RUST": "Rust", "JAVA": "Java",
            "CSHARP": "C#", "SHELL": "Shell/Bash", "RUBY": "Ruby",
            "PHP": "PHP", "SWIFT": "Swift", "KOTLIN": "Kotlin"
        }
        display_name = lang_map.get(name, name)
        
        print(f"  📥 {display_name} ({filename}) ...", end=" ", flush=True)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        file_size = len(content)
        
        # Create page with summary (first 500 chars as description)
        # Extract first meaningful paragraph
        summary = ""
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and not stripped.startswith(">") \
               and not stripped.startswith("---") and len(stripped) > 30:
                summary = stripped[:200]
                break
        
        page_title = f"🐉 {display_name} 笔试题库 | {summary[:60]}"
        page = create_page(parent_id, page_title[:100])  # Notion title limit ~100 chars
        
        if "error" in page:
            print(f"❌ 创建页面失败: {page['error']}")
            results.append({"file": filename, "status": "failed", "error": str(page)})
            continue
        
        page_id = page["id"]
        print(f"页面已创建 {page_id[:8]}...", end=" ", flush=True)
        
        # Parse markdown to blocks
        blocks = parse_markdown_to_blocks(content)
        
        # Also add the full raw content as a single detailed section (for search)
        # Actually parse_markdown_to_blocks already handles it
        
        # Append blocks
        appended = append_blocks(page_id, blocks, chunk_size=80)
        print(f"✅ {appended}/{len(blocks)} 块")
        
        results.append({
            "file": filename,
            "display_name": display_name,
            "page_id": page_id,
            "blocks": len(blocks),
            "appended": appended,
            "status": "ok"
        })
        
        # Also create a direct content page with the full raw markdown for reference
        print(f"    📎 创建完整内容页...", end=" ", flush=True)
        full_page = create_page(page_id, "📄 完整题库内容")
        if "id" in full_page:
            full_id = full_page["id"]
            # Split raw content into chunks and append
            content_blocks = []
            for i in range(0, len(content), PAGE_SIZE):
                chunk_text = content[i:i + PAGE_SIZE]
                content_blocks.append(text_block(chunk_text))
            full_appended = append_blocks(full_id, content_blocks, chunk_size=50)
            print(f"✅ {full_appended} 块")
        
        time.sleep(0.5)
    
    # Step 3: Summary
    print("\n" + "=" * 60)
    ok_count = sum(1 for r in results if r["status"] == "ok")
    print(f"🎉 同步完成: {ok_count}/{len(results)} 成功")
    print(f"\n📍 Notion 容器页: https://www.notion.so/{parent_id.replace('-', '')}")
    
    # Save results
    output = {
        "parent_id": parent_id,
        "notion_url": f"https://www.notion.so/{parent_id.replace('-', '')}",
        "results": results,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "dna": "#龍芯⚡️丙午·甲申·壬子·亥时·䷗复-INTERVIEW-BANKS-NOTION-SYNC-v1.0"
    }
    outpath = "/Users/zuimeidedeyihan/longhun-system/logs/notion_banks_sync_result.json"
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"📝 结果已保存: {outpath}")

if __name__ == "__main__":
    main()
