#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·乙酉·NOTION-CAPACITY-SCAN
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·Notion 容量扫描器 (只读·归档前置侦察)
用途: 定位吃 workspace 容量的「上传型 image 块」，按库/行排序。
     只读，不下载、不改数据。结果写本地归档目录(独立于 longhun-system)。
DNA: #龍芯⚡️丙午·辛未·乙酉·NOTION-CAPACITY-SCAN
"""
import os, sys, json, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = Path("/Users/zuimeidedeyihan/UID9622-Notion-Archive")
ARCHIVE.mkdir(parents=True, exist_ok=True)

TOKEN = ""
secrets = ROOT.parent / ".longhun" / "secrets.env"
if secrets.exists():
    for line in secrets.read_text(encoding="utf-8").splitlines():
        if line.startswith("export NOTION_TOKEN="):
            TOKEN = line.split("=", 1)[1].strip().strip('"')
if not TOKEN:
    TOKEN = os.getenv("NOTION_TOKEN", "")

API = "https://api.notion.com/v1"
HDR = {"Authorization": f"Bearer {TOKEN}", "Notion-Version": "2022-06-28",
       "Content-Type": "application/json"}


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method, headers=HDR)
    for i in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                time.sleep(0.34)  # 稳定限速 ≤3 req/s，避免 429 退避
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 2 ** (i + 1)
                time.sleep(wait)
                continue
            if i == 4:
                raise
            time.sleep(1.2 * (i + 1))
        except Exception:
            if i == 4:
                raise
            time.sleep(1.2 * (i + 1))


def query_rows(db_id, cap=500):
    rows, cursor, n = [], None, 0
    while n < cap:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        d = call("POST", f"/databases/{db_id}/query", body)
        rows.extend(d.get("results", []))
        n = len(rows)
        if d.get("has_more"):
            cursor = d["next_cursor"]
        else:
            break
    return rows


def get_blocks(page_id, cap=200):
    blocks, cursor, n = [], None, 0
    while n < cap:
        path = f"/blocks/{page_id}/children?page_size=100"
        if cursor:
            path += f"&start_cursor={cursor}"
        d = call("GET", path)
        blocks.extend(d.get("results", []))
        n = len(blocks)
        if d.get("has_more"):
            cursor = d["next_cursor"]
        else:
            break
    return blocks


def _txt(arr):
    return "".join(t.get("plain_text", "") for t in arr if isinstance(t, dict))


def title_of(row):
    props = row.get("properties", {})
    # 优先已知标题键
    for k in ("title", "Name", "名称"):
        p = props.get(k)
        if isinstance(p, dict):
            if p.get("type") == "title" and p.get("title"):
                return _txt(p["title"])
            if p.get("type") == "rich_text" and p.get("rich_text"):
                return _txt(p["rich_text"])
    # 兜底: 扫任意 title/rich_text 属性
    for p in props.values():
        if isinstance(p, dict) and p.get("type") in ("title", "rich_text"):
            arr = p.get("title") or p.get("rich_text") or []
            t = _txt(arr)
            if t:
                return t
    return "(无标题)"


TARGETS = {
    "龍魂快照库·Snapshots": "3677125a-9c9f-81ce-846c-db15c69e08ae",
    "📸 Snapshots-数据快照": "126b192b-22d6-4021-b0da-6d89cf9fbd29",
    "资产库·Assets": "3677125a-9c9f-8138-865b-d13628126e24",
    "🐉 跨平台AI对话总归档": "1959c7d5-76ff-4a86-adbe-31238a9c2843",
    "💬 对话归档库": "23505ecb-76fa-49d3-946b-2c024a5230f8",
}


def main():
    report = {"scanned_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "databases": []}
    completed = []

    def save():
        report["databases"] = completed + ([current] if "current" in dir() and current else [])
        (ARCHIVE / "scan_report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"🔍 容量扫描启动 · 目标库 {len(TARGETS)} 个\n", flush=True)
    for name, db_id in TARGETS.items():
        print(f"▸ 扫描 [{name}] …", flush=True)
        try:
            rows = query_rows(db_id)
        except Exception as e:
            print(f"  ⚠️ 查询失败: {e}", flush=True)
            continue
        current = {"name": name, "id": db_id, "row_count": len(rows),
                   "total_images": 0, "file_images": 0, "ext_images": 0, "heavy_rows_top": []}
        heavy = []
        for ri, row in enumerate(rows, 1):
            rid = row["id"]
            rt = title_of(row)
            try:
                blocks = get_blocks(rid)
            except Exception:
                blocks = []
            fim = sum(1 for b in blocks if b.get("type") == "image" and isinstance(b.get("image"), dict) and b["image"].get("type") == "file")
            eim = sum(1 for b in blocks if b.get("type") == "image" and isinstance(b.get("image"), dict) and b["image"].get("type") == "external")
            current["total_images"] += fim + eim
            current["file_images"] += fim
            current["ext_images"] += eim
            if fim + eim > 0:
                heavy.append({"id": rid, "title": rt[:50], "file_images": fim, "ext_images": eim})
            if ri % 20 == 0:
                current["heavy_rows_top"] = sorted(heavy, key=lambda x: -x["file_images"])[:15]
                save()
                print(f"   …{ri}/{len(rows)} 行 | 累计上传图={current['file_images']}", flush=True)
        current["heavy_rows_top"] = sorted(heavy, key=lambda x: -x["file_images"])[:15]
        current["all_image_rows"] = heavy  # 全量含图行(供归档脚本直接消费)
        completed.append(current)
        del current
        save()
        print(f"  ✅ {name}: 行={len(rows)} | 上传图(file)={completed[-1]['file_images']} | 外链图={completed[-1]['ext_images']}", flush=True)

    print("\n" + "=" * 60, flush=True)
    print("📊 容量排序 (按上传型图片数 降序):", flush=True)
    for db in sorted(completed, key=lambda x: -x.get("file_images", 0)):
        print(f"  {db.get('file_images',0):5d} 上传图 | {db['name']} | 行={db.get('row_count',0)}", flush=True)
    print(f"\n💾 报告 → {ARCHIVE / 'scan_report.json'}", flush=True)


if __name__ == "__main__":
    main()
