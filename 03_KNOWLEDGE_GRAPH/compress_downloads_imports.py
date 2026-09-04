#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-COMPRESS_DOWNLOADS_I-5B9BDEE6
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
Downloads 导入区去重压缩脚本
对迁移进主干的 downloads-imports / _archive 目录进行内容级去重：
  - 相同文件（size + md5）只保留一份物理存储
  - 其余副本用硬链接指向同一 inode
  - 保留目录结构，不删除任何文件

执行：
  cd /Users/zuimeidedeyihan/longhun-system/03_知識圖譜
  python3 compress_downloads_imports.py
"""

import hashlib
import json
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path("/Users/zuimeidedeyihan/longhun-system")
REPORT = PROJECT_ROOT / "03_知識圖譜" / "downloads_compression_report.json"
LOG = PROJECT_ROOT / "03_知識圖譜" / "downloads_compression.log"

TARGETS = [
    "cnsh-terminal/downloads-imports",
    "01_技能库/downloads-imports",
    "cnsh-core/downloads-imports",
    "01_protocols/downloads-imports",
    "audit/downloads-imports",
    "baobao-guardian/downloads-imports",
    "agents/downloads-imports",
    "_archive/agent-sessions",
    "_archive/downloads-inbox",
    "_archive/notion-exports",
    "_archive/papers",
    "_archive/evidence",
    "_archive/media",
]

NOISE = {".DS_Store", "Thumbs.db"}


def collect_files():
    files = []
    for rel in TARGETS:
        root = PROJECT_ROOT / rel
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file() and p.name not in NOISE:
                try:
                    st = p.stat()
                    files.append({"path": p, "size": st.st_size, "ino": st.st_ino, "dev": st.st_dev})
                except Exception:
                    pass
    return files


def md5_file(p: Path) -> str:
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def hardlink_dupes():
    files = collect_files()
    # group by size first
    by_size = defaultdict(list)
    for f in files:
        by_size[f["size"]].append(f)

    saved = 0
    linked = 0
    groups = 0
    log_lines = []

    for size, group in by_size.items():
        if size == 0 or len(group) < 2:
            continue
        # compute md5 for candidates
        by_hash = defaultdict(list)
        for f in group:
            h = md5_file(f["path"])
            by_hash[h].append(f)
        for h, hgroup in by_hash.items():
            if len(hgroup) < 2:
                continue
            # pick canonical: prefer shortest path, then lexicographically first
            hgroup.sort(key=lambda x: (len(str(x["path"])), str(x["path"])))
            canonical = hgroup[0]
            c_ino = canonical["ino"]
            c_dev = canonical["dev"]
            for dup in hgroup[1:]:
                # already same inode => already hardlinked
                if dup["ino"] == c_ino and dup["dev"] == c_dev:
                    continue
                dup_path = dup["path"]
                canon_path = canonical["path"]
                try:
                    # atomic replace with hardlink
                    tmp = dup_path.with_name(dup_path.name + ".longhun-tmp")
                    os.link(canon_path, tmp)
                    os.replace(tmp, dup_path)
                    saved += size
                    linked += 1
                    log_lines.append(f"LINK {dup_path} -> {canon_path}")
                except Exception as e:
                    log_lines.append(f"FAIL {dup_path}: {e}")
            groups += 1

    report = {
        "timestamp": datetime.now().isoformat(),
        "targets": TARGETS,
        "scanned_files": len(files),
        "duplicate_groups": groups,
        "hardlinks_created": linked,
        "bytes_saved": saved,
        "human_saved": human_size(saved),
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    LOG.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    return report


def human_size(n):
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.2f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024
    return f"{n:.2f} TB"


if __name__ == "__main__":
    report = hardlink_dupes()
    print(f"扫描 {report['scanned_files']} 个文件，发现 {report['duplicate_groups']} 组重复")
    print(f"创建 {report['hardlinks_created']} 个硬链接，节省 {report['human_saved']}")
    print(f"报告：{REPORT}\n日志：{LOG}")

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·申时·䷵归妹-CONFIRM-SEAL-compress_downloads_i-A81F6367
