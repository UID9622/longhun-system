#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_NOTION_QUICK_SCAN-v1.0-18c7397a
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""快速 Notion 扫描 v2 - 修复版"""
import json, os, subprocess, sys, time
from pathlib import Path

HOME = Path.home()
TOKEN = os.environ.get("NOTION_TOKEN", "")
if not TOKEN:
    sys.path.insert(0, str(HOME / "longhun-system" / "bin"))
    from lh_secrets_loader import load_all
    load_all(export_to_os=True)
    TOKEN = os.environ.get("NOTION_TOKEN", "")

OUT = HOME / "longhun-system" / "data" / "notion_scan" / "scan_raw.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

def api(endpoint, method="GET", payload=None):
    """Simple direct curl API call"""
    url = f"https://api.notion.com/v1{endpoint}"
    cmd = [
        "curl", "-s", "-S", "--max-time", "30",
        "-H", f"Authorization: Bearer {TOKEN}",
        "-H", "Notion-Version: 2022-06-28",
        "-H", "Content-Type: application/json",
    ]
    if method != "GET":
        cmd.extend(["-X", method])
    if payload:
        cmd.extend(["-d", json.dumps(payload, ensure_ascii=False)])
    cmd.extend(["-w", r"\nHTTP_CODE:%{http_code}", url])
    
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=35)
        out = proc.stdout.decode("utf-8", errors="replace")
        marker = "HTTP_CODE:"
        if marker not in out:
            print(f"  DEBUG api fail: {out[:200]}", file=sys.stderr, flush=True)
            return None
        body, code = out.rsplit(marker, 1)
        code = int(code.strip())
        body = body.strip()
        if code >= 400:
            if code == 429:
                time.sleep(3)
                return api(endpoint, method, payload)
            print(f"  API {code}: {body[:150]}", file=sys.stderr, flush=True)
            return None
        if not body:
            return {}
        return json.loads(body)
    except Exception as e:
        print(f"  API exception: {e}", file=sys.stderr, flush=True)
        return None

print("🐉 Scanning Notion...", flush=True)

# Step 1: Search all
all_results = []
cursor = None
page_num = 1
while True:
    payload = {"page_size": 100}
    if cursor:
        payload["start_cursor"] = cursor
    resp = api("/search", "POST", payload)
    if resp is None:
        print(f"  Search failed at page {page_num}", flush=True)
        break
    batch = resp.get("results", [])
    all_results.extend(batch)
    print(f"  Search p{page_num}: +{len(batch)} → total {len(all_results)}", flush=True)
    if not resp.get("has_more"):
        break
    cursor = resp.get("next_cursor")
    page_num += 1
    time.sleep(0.3)

print(f"\n📊 Found: {len(all_results)} items total", flush=True)

# Classify
dbs = [r for r in all_results if r.get("object") == "database"]
pages = [r for r in all_results if r.get("object") == "page"]
print(f"   DBs: {len(dbs)}, Pages: {len(pages)}", flush=True)

# Step 2: Read each DB
def ext_title(obj):
    for pv in (obj.get("properties") or {}).values():
        if isinstance(pv, dict) and pv.get("type") == "title":
            return "".join(t.get("plain_text","") for t in pv.get("title",[]))
    return "未命名"

db_details = []
for i, db in enumerate(dbs):
    db_id = db["id"].replace("-", "")
    db_title = ext_title(db)
    print(f"\n📁 DB {i+1}/{len(dbs)}: {db_title} ({db_id[:12]}...)", flush=True)
    
    # Read entries
    entries = []
    cursor2 = None
    while True:
        qp = {"page_size": 100}
        if cursor2:
            qp["start_cursor"] = cursor2
        qr = api(f"/databases/{db_id}/query", "POST", qp)
        if qr is None:
            break
        batch2 = qr.get("results", [])
        entries.extend(batch2)
        if not qr.get("has_more"):
            break
        cursor2 = qr.get("next_cursor")
        time.sleep(0.33)
    
    db_details.append({
        "id": db_id,
        "title": db_title,
        "url": db.get("url", ""),
        "entry_count": len(entries),
        "entries": [{
            "id": e.get("id",""),
            "title": ext_title(e),
            "url": e.get("url",""),
            "last_edited": e.get("last_edited_time",""),
        } for e in entries],
    })
    print(f"   → {len(entries)} entries", flush=True)

# Step 3: Page summaries
page_summaries = []
for p in pages:
    page_summaries.append({
        "id": p.get("id","").replace("-",""),
        "title": ext_title(p),
        "url": p.get("url",""),
        "last_edited": p.get("last_edited_time",""),
        "parent_type": p.get("parent",{}).get("type",""),
        "parent_db": p.get("parent",{}).get("database_id","").replace("-",""),
        "archived": p.get("archived", False),
    })

result = {
    "scan_time": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    "dna": f"#龍芯⚡️{time.strftime('%Y%m%d-%H%M%S')}-NOTION-SCAN-v2",
    "summary": {
        "total_items": len(all_results),
        "databases": len(dbs),
        "pages": len(pages),
        "db_entries": sum(d["entry_count"] for d in db_details),
    },
    "database_details": db_details,
    "page_summaries": page_summaries,
}

OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2))
print(f"\n{'='*50}")
print(f"✅ 扫描完成!")
print(f"  数据库: {len(dbs)} 个")
print(f"  独立页面: {len(pages)} 个")  
print(f"  数据库条目: {sum(d['entry_count'] for d in db_details)} 条")
print(f"  保存至: {OUT}")
print(f"{'='*50}")
