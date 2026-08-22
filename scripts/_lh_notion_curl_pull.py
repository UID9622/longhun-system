#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷯井-FIX_DNA-v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
"""龍魂 Notion 拉取器 · curl版 · 绕过requests库问题"""
import subprocess, json, pathlib, time, re, sys

HOME = pathlib.Path.home()
SECRETS = HOME / ".longhun" / "secrets.env"
OUT_DIR = HOME / ".longhun" / "notion_pages" / "targeted_pull"
TRAIN_CORPUS = HOME / "longhun-system" / "models" / "longhun-v1.0" / "notion_targeted_corpus.md"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TOKEN = re.search(r'export\s+NOTION_TOKEN=["\']([^"\']+)["\']', SECRETS.read_text()).group(1)

def curl(method, url, data=None):
    """用curl调用Notion API"""
    cmd = ['curl', '-s', '--max-time', '15',
           '-H', f'Authorization: Bearer {TOKEN}',
           '-H', 'Notion-Version: 2022-06-28']
    if method == 'POST':
        cmd.extend(['-H', 'Content-Type: application/json', '-d', data])
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return {}
    try:
        return json.loads(r.stdout)
    except:
        return {}

def safe_fn(name):
    n = re.sub(r'[\x00-\x1f\x7f-\x9f]', '_', name.strip().replace("/", "_")[:60])
    return n or "untitled"

def rtm(rt): return "".join(x.get("plain_text", "") for x in rt)

all_md = []

def pull_db(db_id):
    nid = f"{db_id[0:8]}-{db_id[8:12]}-{db_id[12:16]}-{db_id[16:20]}-{db_id[20:32]}"
    d = curl('GET', f"https://api.notion.com/v1/databases/{nid}")
    dbtitle = rtm(d.get('title', [])); print(f"\nDB: {dbtitle[:50]}", flush=True)
    
    cursor = None; pages = []
    while True:
        body = json.dumps({"page_size": 50, "start_cursor": cursor} if cursor else {"page_size": 50})
        dd = curl('POST', f"https://api.notion.com/v1/databases/{nid}/query", body)
        if not dd: break
        for p in dd.get('results', []):
            props = p.get('properties', {}); pt = ""
            for v in props.values():
                if v.get('type') == 'title': pt = rtm(v.get('title', [])); break
            pages.append((p['id'], pt or '无标题'))
        if not dd.get('has_more'): break
        cursor = dd['next_cursor']; time.sleep(0.35)
    
    print(f"  {len(pages)}条", flush=True)
    for i, (pid, pt) in enumerate(pages):
        fpath = OUT_DIR / f"{safe_fn(pt)}_{pid[:8]}.md"
        if fpath.exists(): print(f"  [{i+1}/{len(pages)}] SKIP {pt[:30]}", flush=True); all_md.append(fpath.read_text()); continue
        bd = curl('GET', f"https://api.notion.com/v1/blocks/{pid}/children?page_size=100")
        if not bd: print(f"  [{i+1}/{len(pages)}] FAIL {pt[:30]}", flush=True); continue
        blocks = []
        for b in bd.get('results', []):
            bt = b.get('type', ''); bb = b.get(bt, {}); txt = rtm(bb.get('rich_text', []))
            if bt == 'paragraph': blocks.append(txt)
            elif bt in ('heading_1','heading_2','heading_3'): blocks.append(f"{'#'*int(bt[-1])} {txt}")
            elif bt == 'bulleted_list_item': blocks.append(f"- {txt}")
            elif bt == 'numbered_list_item': blocks.append(f"1. {txt}")
            elif bt == 'to_do': c = 'x' if bb.get('checked') else ' '; blocks.append(f"- [{c}] {txt}")
            elif bt == 'code': blocks.append(f"```\n{txt}\n```")
            elif bt == 'divider': blocks.append('---')
            elif bt == 'quote': blocks.append(f"> {txt}")
            elif bt == 'child_page': blocks.append(f"> 📄 子页面: {b.get('child_page',{}).get('title','')}")
            elif bt == 'child_database': blocks.append(f"> 🗃️ 子数据库: {b.get('child_database',{}).get('title','')}")
        md = f"# {pt}\n\n- Notion: https://www.notion.so/{pid.replace('-','')}\n\n---\n\n" + "\n\n".join(blocks)
        fpath.write_text(md, encoding='utf-8')
        all_md.append(md)
        print(f"  [{i+1}/{len(pages)}] OK {pt[:30]} ({len(blocks)}块)", flush=True)
        time.sleep(0.25)

def pull_page(page_id, label=""):
    nid = f"{page_id[0:8]}-{page_id[8:12]}-{page_id[12:16]}-{page_id[16:20]}-{page_id[20:32]}"
    d = curl('GET', f"https://api.notion.com/v1/pages/{nid}")
    if not d: print(f"\n{label}PAGE: FAIL", flush=True); return
    props = d.get('properties', {}); title = ""
    for v in props.values():
        if v.get('type') == 'title': title = rtm(v.get('title', [])); break
    title = title or '无标题'; print(f"\n{label}PAGE: {title[:50]}", flush=True)
    
    fpath = OUT_DIR / f"{safe_fn(title)}_{page_id[:8]}.md"
    if fpath.exists(): print(f"  SKIP", flush=True); all_md.append(fpath.read_text()); return
    
    bd = curl('GET', f"https://api.notion.com/v1/blocks/{nid}/children?page_size=100")
    if not bd: print(f"  FAIL", flush=True); return
    blocks = []
    for b in bd.get('results', []):
        bt = b.get('type', ''); bb = b.get(bt, {}); txt = rtm(bb.get('rich_text', []))
        if bt == 'paragraph': blocks.append(txt)
        elif bt in ('heading_1','heading_2','heading_3'): blocks.append(f"{'#'*int(bt[-1])} {txt}")
        elif bt == 'bulleted_list_item': blocks.append(f"- {txt}")
        elif bt == 'numbered_list_item': blocks.append(f"1. {txt}")
        elif bt == 'to_do': c = 'x' if bb.get('checked') else ' '; blocks.append(f"- [{c}] {txt}")
        elif bt == 'code': blocks.append(f"```\n{txt}\n```")
        elif bt == 'divider': blocks.append('---')
        elif bt == 'quote': blocks.append(f"> {txt}")
        elif bt == 'child_page': blocks.append(f"> 📄 子页面: {b.get('child_page',{}).get('title','')}")
        elif bt == 'child_database': blocks.append(f"> 🗃️ 子数据库: {b.get('child_database',{}).get('title','')}")
    md = f"# {title}\n\n- Notion: https://www.notion.so/{page_id}\n\n---\n\n" + "\n\n".join(blocks)
    fpath.write_text(md, encoding='utf-8')
    all_md.append(md)
    print(f"  OK ({len(blocks)}块)", flush=True)

def main():
    print("🐉 龍魂 Notion 拉取 (curl版)", flush=True)
    
    # URL1: DB
    pull_db("baf3b574023e49c987eee620a811e70d")
    # URL2: DB
    pull_db("3367125a9c9f808a9692f0c6752e92fa")
    # URL3: PAGE
    pull_page("f545874667f4438e8bc76d7a76182b9e", "URL3 ")
    # URL4: PAGE
    pull_page("3debae713c554137abafdc3dc3874cc6", "URL4 ")
    
    # 训练语料
    TRAIN_CORPUS.parent.mkdir(parents=True, exist_ok=True)
    corpus = f"# 龍魂 Notion 训练语料\n\n拉取时间: {time.strftime('%Y-%m-%d %H:%M')}\n目标: 4\n确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z\n\n---\n\n" + "\n\n---\n\n".join(all_md)
    TRAIN_CORPUS.write_text(corpus, encoding='utf-8')
    
    md_files = list(OUT_DIR.glob("*.md"))
    size_kb = TRAIN_CORPUS.stat().st_size / 1024
    print(f"\n{'='*50}")
    print(f"📊 总计: {len(md_files)} 文件 · 语料 {size_kb:.1f} KB")
    print(f"📁 页面: {OUT_DIR}")
    print(f"📚 语料: {TRAIN_CORPUS}")
    print(f"✅ 完成")

if __name__ == "__main__":
    main()
