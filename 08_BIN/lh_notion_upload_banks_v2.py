#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""龍魂·面试题库 Notion 快速直传 v2.0
DNA: #龍芯⚡️丙午·甲申·壬子·亥时·䷗复-INTERVIEW-BANKS-NOTION-UPLOAD-v2.0
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2
策略: 每文件创建页面 → 全文作为一个段落块的大文本 → 快速稳定
"""
import json, os, time, sys
import urllib.request, urllib.error

TOKEN = "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"
BANKS_DIR = "/Users/zuimeidedeyihan/_work/interview-question-banks"
NOTION = "https://api.notion.com/v1"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"}

def api(method, path, data=None):
    """Notion API call with timeout"""
    url = f"{NOTION}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e)}

def create_page(parent_id, title):
    return api("POST", "/pages", {
        "parent": {"page_id": parent_id},
        "properties": {"title": {"title": [{"text": {"content": title}}]}}
    })

def append_text(page_id, text):
    """Append text as a single paragraph block (2000 char per text element)"""
    blocks = []
    i = 0
    rich = []
    while i < len(text):
        chunk = text[i:i+1990]  # leave some margin
        rich.append({"type": "text", "text": {"content": chunk}})
        i += 1990
        if len(rich) >= 100:  # Notion limit: 100 text elements per block
            blocks.append({"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich}})
            rich = []
    if rich:
        blocks.append({"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich}})
    
    # Append in chunks of 100 blocks
    total = len(blocks)
    appended = 0
    for start in range(0, total, 100):
        chunk = blocks[start:start+100]
        r = api("PATCH", f"/blocks/{page_id}/children", {"children": chunk})
        if "error" in r:
            print(f" ⚠️ {r['error'][:80]}", end="")
            # Retry one by one
            for b in chunk:
                r2 = api("PATCH", f"/blocks/{page_id}/children", {"children": [b]})
                if "error" not in r2:
                    appended += 1
                time.sleep(0.1)
        else:
            appended += len(chunk)
        time.sleep(0.2)
    return appended

def main():
    print("🐉 龍魂·面试题库 Notion 快速直传 v2.0")
    
    # Find container page
    r = api("POST", "/search", {"query": "面试题库", "filter": {"property": "object", "value": "page"}})
    parent_id = None
    for p in r.get("results", []):
        for v in p.get("properties", {}).values():
            if isinstance(v, dict) and v.get("type") == "title":
                t = "".join([x.get("plain_text","") for x in v.get("title",[])])
                if "面试题库" in t:
                    parent_id = p["id"]
                    break
    if not parent_id:
        r2 = api("POST", "/search", {"page_size": 1})
        root = r2.get("results", [{}])[0]
        root_id = root.get("id", "")
        cont = create_page(root_id, "📚 面试题库")
        parent_id = cont.get("id", "")
        print(f"📁 创建容器: {parent_id[:8]}...")
    else:
        print(f"📁 找到容器: {parent_id[:8]}...")
    
    files = sorted([f for f in os.listdir(BANKS_DIR) if f.endswith(".md")])
    lang_map = {
        "js": "JavaScript", "ts": "TypeScript", "go": "Go", "sql": "SQL",
        "rust": "Rust", "java": "Java", "csharp": "C#", "shell": "Shell/Bash",
        "ruby": "Ruby", "php": "PHP", "swift": "Swift", "kotlin": "Kotlin"
    }
    
    ok = 0
    for fname in files:
        code = fname.split("-")[0]
        lang = lang_map.get(code, code.upper())
        fpath = os.path.join(BANKS_DIR, fname)
        
        with open(fpath, encoding="utf-8") as f:
            content = f.read()
        
        size_k = len(content) // 1024
        print(f"  📥 {lang:12s} ({size_k}K)...", end=" ", flush=True)
        
        page = create_page(parent_id, f"🐉 {lang} 全方位笔试题库 v1.0")
        pid = page.get("id")
        if not pid:
            print(f"❌ {page.get('error','?')[:60]}")
            continue
        
        print(f"page={pid[:8]}...", end=" ", flush=True)
        n = append_text(pid, content)
        print(f"✅ {n} blocks")
        ok += 1
        time.sleep(0.3)
    
    print(f"\n🎉 完成: {ok}/{len(files)}")
    print(f"📍 https://www.notion.so/{parent_id.replace('-','')}")

if __name__ == "__main__":
    main()
