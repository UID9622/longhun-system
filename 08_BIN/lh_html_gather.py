#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-02-HTML-GATHER-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 功能: HTML 资产归集引擎 —— 全设备 HTML 归集到 web_apps/html_assets/ + 生成 INDEX.json 供数字人创作检索
# 原则: 复制不移动(不破坏原路径引用) · 黑名单跳过 · 按顶层目录分组 · 重名加短哈希

import os
import shutil
import hashlib
import json
import time

ROOT = os.path.expanduser("~/longhun-system")
DST = os.path.join(ROOT, "web_apps", "html_assets")

# 黑名单(目录名含任意项即跳过)
BLACK = ("html_assets", ".venv", "node_modules", "11_DATA", "_work", "dist", "models",
         "archive", "backup", "WASTE", "__pycache__", "glyph-backup")
SKIP_TOP = ("_archive", ".venv_tts", "rust")  # 顶层目录级跳过


def main():
    os.makedirs(DST, exist_ok=True)
    index = []
    count = 0
    skipped = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # 剪枝黑名单目录
        dirnames[:] = [d for d in dirnames
                       if not any(b in d for b in BLACK) and not d.startswith(".")]
        rel = os.path.relpath(dirpath, ROOT)
        parts = rel.split(os.sep)
        if parts and parts[0] in SKIP_TOP:
            dirnames[:] = []
            continue
        top = parts[0] if parts and parts[0] != "." else "root"
        for fn in filenames:
            if not fn.lower().endswith(".html"):
                continue
            src = os.path.join(dirpath, fn)
            dest_dir = os.path.join(DST, top)
            os.makedirs(dest_dir, exist_ok=True)
            dest = os.path.join(dest_dir, fn)
            if os.path.exists(dest):
                h = hashlib.md5(src.encode("utf-8")).hexdigest()[:6]
                dest = os.path.join(dest_dir, f"{os.path.splitext(fn)[0]}_{h}.html")
            try:
                shutil.copy2(src, dest)
            except OSError:
                skipped += 1
                continue
            st = os.stat(src)
            index.append({
                "src": os.path.relpath(src, ROOT),
                "dest": os.path.relpath(dest, ROOT),
                "size": st.st_size,
                "mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime)),
                "group": top,
            })
            count += 1

    index.sort(key=lambda x: x["src"])
    with open(os.path.join(DST, "INDEX.json"), "w", encoding="utf-8") as f:
        json.dump({"total": count, "skipped": skipped,
                   "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "items": index}, f, ensure_ascii=False, indent=1)

    # 按 group 统计
    groups = {}
    for item in index:
        groups[item["group"]] = groups.get(item["group"], 0) + 1
    print(f"归集完成: {count} 个 HTML → web_apps/html_assets/ (跳过 {skipped})")
    for g, n in sorted(groups.items(), key=lambda x: -x[1]):
        print(f"  {g}: {n}")


if __name__ == "__main__":
    main()
