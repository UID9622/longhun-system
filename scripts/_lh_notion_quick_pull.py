# DNA: #龍芯⚡️丙午·乙未·乙丑·井-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""龍魂 Notion 快速拉取器 · 极简版 · 无冗余依赖"""
import re, requests, time, pathlib

HOME = pathlib.Path.home()
SECRETS = HOME / ".longhun" / "secrets.env"
OUT_DIR = HOME / ".longhun" / "notion_pages" / "targeted_pull"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_token():
    m = re.search(r'export\s+NOTION_TOKEN=["\']([^"\']+)["\']', SECRETS.read_text())
    if m: return m.group(1)
    raise RuntimeError("No token")

def safe_fn(name):
    name = re.sub(r'[\x00-\x1f\x7f-\x9f]', '_', name.strip().replace("/", "_")[:60])
    return name or "untitled"

def rtm(rt): 
    return "".join(x.get("plain_text", "") for x in rt)

def pull_page(pid, ptitle, h):
    fpath = OUT_DIR / f"{safe_fn(ptitle)}_{pid[:8]}.md"
    if fpath.exists():
        print(f"    SKIP: {ptitle[:30]}", flush=True)
        return
    r = requests.get(
        f"https://api.notion.com/v1/blocks/{pid}/children?page_size=100",
        headers=h, timeout=20
    )
    if r.status_code != 200:
        print(f"    FAIL: {ptitle[:30]} ({r.status_code})", flush=True)
        return
    blocks = []
    for b in r.json().get("results", []):
        bt = b.get("type", "")
        bd = b.get(bt, {})
        txt = rtm(bd.get("rich_text", []))
        if bt == "paragraph": blocks.append(txt)
        elif bt == "heading_1": blocks.append(f"# {txt}")
        elif bt == "heading_2": blocks.append(f"## {txt}")
        elif bt == "heading_3": blocks.append(f"### {txt}")
        elif bt == "bulleted_list_item": blocks.append(f"- {txt}")
        elif bt == "numbered_list_item": blocks.append(f"1. {txt}")
        elif bt == "to_do":
            c = "x" if bd.get("checked") else " "
            blocks.append(f"- [{c}] {txt}")
        elif bt == "code": blocks.append(f"```\n{txt}\n```")
        elif bt == "divider": blocks.append("---")
        elif bt == "quote": blocks.append(f"> {txt}")
        elif bt == "child_page":
            blocks.append(f"> 📄 子页面: {b.get('child_page', {}).get('title', '')}")
        elif bt == "child_database":
            blocks.append(f"> 🗃️ 子数据库: {b.get('child_database', {}).get('title', '')}")
    fpath.write_text(
        f"# {ptitle}\n\n- Notion: https://www.notion.so/{pid.replace('-', '')}\n\n---\n\n" + "\n\n".join(blocks),
        encoding="utf-8"
    )
    print(f"    OK: {ptitle[:30]} ({len(blocks)}块)", flush=True)

def pull_db(db_id, h):
    nid = f"{db_id[0:8]}-{db_id[8:12]}-{db_id[12:16]}-{db_id[16:20]}-{db_id[20:32]}"
    r = requests.get(f"https://api.notion.com/v1/databases/{nid}", headers=h, timeout=15)
    if r.status_code != 200:
        print(f"DB {db_id[:8]}: SKIP ({r.status_code})", flush=True)
        return
    d = r.json()
    dbtitle = rtm(d.get("title", []))
    
    body = {"page_size": 50}
    pages = []
    while True:
        r2 = requests.post(
            f"https://api.notion.com/v1/databases/{nid}/query",
            headers={**h, "Content-Type": "application/json"},
            json=body, timeout=30
        )
        if r2.status_code != 200: break
        dd = r2.json()
        for p in dd.get("results", []):
            props = p.get("properties", {})
            pt = ""
            for k, v in props.items():
                if v.get("type") == "title":
                    pt = rtm(v.get("title", []))
                    break
            pages.append((p["id"], pt or "无标题"))
        if not dd.get("has_more"): break
        body["start_cursor"] = dd["next_cursor"]
        time.sleep(0.3)
    
    print(f"DB [{dbtitle[:40]}]: {len(pages)}页", flush=True)
    for i, (pid, ptitle) in enumerate(pages):
        print(f"  [{i+1}/{len(pages)}]", end=" ", flush=True)
        pull_page(pid, ptitle, h)
        time.sleep(0.2)
    print(f"✅ DB {dbtitle[:30]} 完成\n", flush=True)

def pull_page_direct(page_id, h):
    """拉取单个页面（非数据库）"""
    nid = f"{page_id[0:8]}-{page_id[8:12]}-{page_id[12:16]}-{page_id[16:20]}-{page_id[20:32]}"
    r = requests.get(f"https://api.notion.com/v1/pages/{nid}", headers=h, timeout=15)
    if r.status_code != 200:
        print(f"PAGE {page_id[:8]}: SKIP ({r.status_code})", flush=True)
        return
    d = r.json()
    props = d.get("properties", {})
    title = ""
    for k, v in props.items():
        if v.get("type") == "title":
            title = rtm(v.get("title", []))
            break
    print(f"PAGE [{title[:40]}]", flush=True)
    pull_page(nid, title, h)
    print(f"✅ PAGE {title[:30]} 完成\n", flush=True)

def main():
    token = load_token()
    h = {"Authorization": f"Bearer {token}", "Notion-Version": "2022-06-28"}
    
    # URL1 & URL2: Databases
    for db_id in ["baf3b574023e49c987eee620a811e70d", "3367125a9c9f808a9692f0c6752e92fa"]:
        pull_db(db_id, h)
    
    # URL3 & URL4: Pages
    for page_id in ["f545874667f4438e8bc76d7a76182b9e", "3debae713c554137abafdc3dc3874cc6"]:
        pull_page_direct(page_id, h)
    
    print("=" * 50)
    md_files = list(OUT_DIR.glob("*.md"))
    print(f"总计: {len(md_files)} 个markdown文件")
    print(f"目录: {OUT_DIR}")
    print("✅ 全部完成")

if __name__ == "__main__":
    main()
