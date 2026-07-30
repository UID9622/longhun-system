#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·乙酉·NOTION-EXPLORE-READONLY
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·Notion 只读勘探器
用途: 枚举 integration 可见的所有页面/数据库，统计类型与规模，
     为「容量清理 / 截图归档」提供决策依据。只读，不改任何数据。
DNA: #龍芯⚡️丙午·辛未·乙酉·NOTION-EXPLORE-READONLY
"""
import os, sys, json, time
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# 从主权 secrets.env 读 token
secrets = ROOT.parent / ".longhun" / "secrets.env"
TOKEN = ""
if secrets.exists():
    for line in secrets.read_text(encoding="utf-8").splitlines():
        if line.startswith("export NOTION_TOKEN="):
            TOKEN = line.split("=", 1)[1].strip().strip('"')
if not TOKEN:
    TOKEN = os.getenv("NOTION_TOKEN", "")
if not TOKEN:
    print("❌ 未找到 NOTION_TOKEN"); sys.exit(1)

API = "https://api.notion.com/v1"
HDR = {"Authorization": f"Bearer {TOKEN}", "Notion-Version": "2022-06-28",
       "Content-Type": "application/json"}


def call(method, path, body=None):
    url = API + path
    data = json.dumps(body).encode() if body is not None else None
    req = Request(url, data=data, method=method, headers=HDR)
    for _ in range(3):
        try:
            with urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            err = e
            time.sleep(1.5)
    raise err


def search_all():
    out, cursor = [], None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        d = call("POST", "/search", body)
        out.extend(d.get("results", []))
        if d.get("has_more"):
            cursor = d["next_cursor"]
        else:
            break
        if len(out) > 5000:
            break
    return out


def main():
    print("🔍 枚举 integration 可见对象 (只读)…")
    results = search_all()
    pages = [r for r in results if r.get("object") == "page"]
    dbs = [r for r in results if r.get("object") == "database"]

    print(f"\n可见对象总数: {len(results)} | 页面: {len(pages)} | 数据库: {len(dbs)}\n")

    print("═" * 72)
    print("📚 数据库一览 (integration 可见)")
    print("═" * 72)
    db_rows = []
    for db in dbs:
        did = db["id"]
        title = "".join(t.get("plain_text", "") for t in db.get("title", [])) or "(无标题)"
        # 行数
        try:
            q = call("POST", f"/databases/{did}/query", {"page_size": 100})
            n = len(q.get("results", []))
            has_more = q.get("has_more")
            while has_more and n < 5000:
                q = call("POST", f"/databases/{did}/query",
                         {"page_size": 100, "start_cursor": q["next_cursor"]})
                n += len(q.get("results", []))
                has_more = q.get("has_more")
        except Exception as e:
            n = f"err:{e}"
        db_rows.append((title, did, n))
        print(f"  • {title[:40]:40s} | 行数={n} | {did}")

    print("\n═" * 72)
    print("📄 顶层页面一览 (前 60，按最后编辑时间倒序)")
    print("═" * 72)
    pages_sorted = sorted(pages, key=lambda p: p.get("last_edited_time", ""), reverse=True)
    for p in pages_sorted[:60]:
        pid = p["id"]
        title = "(无标题)"
        if p.get("properties", {}).get("title"):
            title = "".join(t.get("plain_text", "") for t in p["properties"]["title"])
        elif p.get("properties", {}).get("Name"):
            title = "".join(t.get("plain_text", "") for t in p["properties"]["Name"])
        le = p.get("last_edited_time", "")[:10]
        print(f"  • {le} | {title[:46]:46s} | {pid}")

    if len(pages) > 60:
        print(f"  … 其余 {len(pages)-60} 个页面未列出")

    # 输出 JSON 供后续脚本复用
    out_path = ROOT / "L7_数据层" / "notion_prompt_library" / "_explore_cache.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({
        "scanned_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "totals": {"pages": len(pages), "databases": len(dbs), "all": len(results)},
        "databases": [{"title": t, "id": i, "rows": n} for t, i, n in db_rows],
        "pages": [{"id": p["id"],
                   "title": "".join(t.get("plain_text","") for t in
                       (p.get("properties",{}).get("title") or p.get("properties",{}).get("Name") or [])),
                   "last_edited": p.get("last_edited_time","")} for p in pages_sorted],
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n💾 勘探缓存 → {out_path}")


if __name__ == "__main__":
    main()
