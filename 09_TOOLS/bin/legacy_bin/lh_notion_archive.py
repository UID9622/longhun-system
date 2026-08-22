#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·Notion 截图归档器 (打包落本地 + Notion 归档)
前置: lh_notion_capacity_scan.py 产出的 scan_report.json
策略(用户选定): 先打包落本地 → 再在 Notion 归档(archived:true, 可恢复)
  · 只处理「含上传型图片(file)的行」——这是吃容量的大头；纯文本行不动。
  · 外链图(ext)不占容量，仅记入清单，可选下载。
  · 安全闸: 默认 DRY_RUN(只打印计划)；设 ARCHIVE_GO=1 才真下载+归档。
DNA: #龍芯⚡️丙午·辛未·乙酉·壬午·䷨损-NOTION-ARCHIVE
"""
import os, sys, json, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = Path("/Users/zuimeidedeyihan/UID9622-Notion-Archive")
REPORT = ARCHIVE / "scan_report.json"
GO = os.getenv("ARCHIVE_GO") == "1"          # 安全闸
DOWNLOAD_EXT = os.getenv("DOWNLOAD_EXT") == "1"  # 是否也下载外链图

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
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2 ** (i + 1)); continue
            if i == 4: raise
            time.sleep(1.2 * (i + 1))
        except Exception:
            if i == 4: raise
            time.sleep(1.2 * (i + 1))


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


def download(url, dest: Path):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type", "")
    ext = ".bin"
    if "png" in ctype: ext = ".png"
    elif "jpeg" in ctype or "jpg" in ctype: ext = ".jpg"
    elif "gif" in ctype: ext = ".gif"
    elif "webp" in ctype: ext = ".webp"
    elif "pdf" in ctype: ext = ".pdf"
    dest = dest.with_suffix(ext) if dest.suffix == "" else dest
    dest.write_bytes(data)
    return ext, len(data)


def safe_name(s, max=40):
    bad = '/\\:*?"<>|'
    return "".join(c if c not in bad else "_" for c in (s or "untitled")).strip()[:max] or "untitled"


def main():
    if not REPORT.exists():
        print("❌ 找不到 scan_report.json，先跑 lh_notion_capacity_scan.py"); sys.exit(1)
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    print(f"{'🟢 实跑模式(ARCHIVE_GO=1)' if GO else '🟡 演练模式 DRY_RUN'} · 下载外链图={'是' if DOWNLOAD_EXT else '否'}")
    print(f"报告时间: {report.get('scanned_at')}\n")

    manifest = {"archived_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "databases": []}
    total_img = 0
    total_bytes = 0
    for db in report.get("databases", []):
        name = db["name"]
        db_safe = safe_name(name, 30)
        rows = db.get("all_image_rows", [])
        print(f"▸ {name} · 含图行 {len(rows)}", flush=True)
        db_manifest = {"name": name, "id": db["id"], "rows": []}
        for row in rows:
            rid = row["id"]
            rtitle = row.get("title", "")
            folder = ARCHIVE / db_safe / safe_name(rtitle, 30) + "_" + rid[:8]
            folder.mkdir(parents=True, exist_ok=True)
            # 重新拉块拿图片 URL(扫描只记了计数)
            try:
                blocks = get_blocks(rid)
            except Exception as e:
                print(f"   ⚠️ 拉块失败 {rid}: {e}", flush=True)
                continue
            imgs = [b for b in blocks if b.get("type") == "image" and isinstance(b.get("image"), dict)]
            row_rec = {"id": rid, "title": rtitle, "images": [], "archived": False}
            for i, b in enumerate(imgs, 1):
                im = b["image"]
                itype = im.get("type")
                if itype == "file":
                    url = im.get("file", {}).get("url")
                    tag = "file"
                else:
                    url = im.get("external", {}).get("url")
                    tag = "ext"
                if not url:
                    continue
                if tag == "ext" and not DOWNLOAD_EXT:
                    row_rec["images"].append({"n": i, "type": tag, "url": url, "local": None})
                    continue
                dest = folder / f"img_{i:03d}"
                if GO:
                    try:
                        ext, sz = download(url, dest)
                        total_bytes += sz
                        row_rec["images"].append({"n": i, "type": tag, "local": f"{dest.name}{ext}", "bytes": sz})
                        total_img += 1
                    except Exception as e:
                        row_rec["images"].append({"n": i, "type": tag, "url": url, "error": str(e)})
                else:
                    row_rec["images"].append({"n": i, "type": tag, "url": url[:80] + "…", "local": f"{dest.name}.<ext>"})
                    total_img += 1
            # 归档
            if GO and row_rec["images"]:
                try:
                    call("PATCH", f"/pages/{rid}", {"archived": True})
                    row_rec["archived"] = True
                    print(f"   📦 {rtitle[:30]} | 图 {len(row_rec['images'])} | 已归档", flush=True)
                except Exception as e:
                    print(f"   ⚠️ 归档失败 {rid}: {e}", flush=True)
            else:
                print(f"   📦 {rtitle[:30]} | 图 {len(row_rec['images'])} | {'将归档' if GO else '演练'}", flush=True)
            db_manifest["rows"].append(row_rec)
        manifest["databases"].append(db_manifest)

    (ARCHIVE / "archive_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{'='*60}")
    print(f"📊 处理图片(预估/实际): {total_img} 张 | 下载体积: {total_bytes/1024/1024:.1f} MB")
    print(f"🗂️ 本地归档: {ARCHIVE}")
    print(f"📝 清单: {ARCHIVE / 'archive_manifest.json'}")
    if not GO:
        print("\n⚠️ 当前为演练(DRY_RUN)。确认无误后运行: ARCHIVE_GO=1 python3 bin/lh_notion_archive.py")


if __name__ == "__main__":
    main()
