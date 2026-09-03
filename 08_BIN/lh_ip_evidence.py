#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·丁丑·戌时·䷒临-IP-EVIDENCE-ENGINE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·IP链上存证引擎 v1.0
批量 SHA-256 哈希固化 + Merkle 根生成，为 IPFS/区块链上链提供统一证据账本。

用法:
  python3 bin/lh_ip_evidence.py build            # 生成证据账本
  python3 bin/lh_ip_evidence.py verify           # 复算校验账本未被篡改
  python3 bin/lh_ip_evidence.py show             # 显示根哈希与统计
"""
import hashlib
import json
import os
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE_DIR = os.path.join(ROOT, "12_DOCS", "evidence")
LEDGER = os.path.join(EVIDENCE_DIR, "UID9622_IP_HASH_LEDGER.json")
ROOT_FILE = os.path.join(EVIDENCE_DIR, "MERKLE_ROOT.txt")

# 存证范围：原创资产（排除原始下载/参考资料目录）
# skip_dirs=None 表示只扫该目录顶层（协议层均为单层归档，避免子目录整理副本重复）
SCAN_DIRS = [
    ("articles", ["*.md"], []),
    ("papers", ["*.md"], ["downloads_archive", "_kimi_raw", "behavioral_crypto_deploy"]),
    ("01_protocols", ["*.md"], None),
]
OWNER = "诸葛鑫 | UID9622 · 龍芯北辰"
DNA = "#龍芯⚡️丙午·丙申·丁丑·戌时·䷒临-IP-EVIDENCE-ENGINE-v1.0-UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_files():
    items = []
    for base, patterns, skip_dirs in SCAN_DIRS:
        base_path = os.path.join(ROOT, base)
        if not os.path.isdir(base_path):
            continue
        if skip_dirs is None:
            # 只扫顶层
            for fn in os.listdir(base_path):
                full = os.path.join(base_path, fn)
                if not os.path.isfile(full):
                    continue
                if fn.endswith(".asc") or fn.endswith(".glyph-backup"):
                    continue
                if any(fn.endswith(p.replace("*", "")) for p in patterns):
                    items.append((os.path.relpath(full, ROOT), full))
            continue
        for dirpath, dirnames, filenames in os.walk(base_path):
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]
            for fn in filenames:
                if fn.endswith(".asc") or fn.endswith(".glyph-backup"):
                    continue
                if any(fn.endswith(p.replace("*", "")) for p in patterns):
                    full = os.path.join(dirpath, fn)
                    rel = os.path.relpath(full, ROOT)
                    items.append((rel, full))
    return sorted(items)


def build():
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    items = scan_files()
    entries = []
    for rel, full in items:
        entries.append({
            "path": rel,
            "sha256": sha256_file(full),
            "bytes": os.path.getsize(full),
            "mtime": datetime.fromtimestamp(os.path.getmtime(full)).isoformat(timespec="seconds"),
        })
    # Merkle 根：全部条目按 path 排序后拼接哈希再取根
    joined = "".join(e["sha256"] for e in entries).encode()
    merkle_root = hashlib.sha256(joined).hexdigest()
    ledger = {
        "dna": DNA,
        "owner": OWNER,
        "confirm": CONFIRM,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total_files": len(entries),
        "merkle_root": merkle_root,
        "entries": entries,
    }
    with open(LEDGER, "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
    with open(ROOT_FILE, "w", encoding="utf-8") as f:
        f.write(f"UID9622 IP Evidence Merkle Root v1.0\n")
        f.write(f"owner: {OWNER}\n")
        f.write(f"dna: {DNA}\n")
        f.write(f"generated_at: {ledger['generated_at']}\n")
        f.write(f"total_files: {len(entries)}\n")
        f.write(f"merkle_root: {merkle_root}\n")
        f.write(f"confirm: {CONFIRM}\n")
    print(f"LEDGER-OK files={len(entries)} root={merkle_root}")


def verify():
    if not os.path.exists(LEDGER):
        print("ERROR: ledger missing, run build first")
        sys.exit(1)
    with open(LEDGER, "r", encoding="utf-8") as f:
        ledger = json.load(f)
    bad = 0
    for e in ledger["entries"]:
        full = os.path.join(ROOT, e["path"])
        if not os.path.exists(full):
            print(f"MISSING {e['path']}")
            bad += 1
            continue
        cur = sha256_file(full)
        if cur != e["sha256"]:
            print(f"TAMPERED {e['path']}")
            bad += 1
    joined = "".join(e["sha256"] for e in ledger["entries"]).encode()
    root = hashlib.sha256(joined).hexdigest()
    status = "OK" if root == ledger["merkle_root"] and bad == 0 else "FAIL"
    print(f"VERIFY-{status} files={len(ledger['entries'])} root={root}")
    sys.exit(0 if status == "OK" else 1)


def show():
    if not os.path.exists(ROOT_FILE):
        print("ERROR: root file missing, run build first")
        sys.exit(1)
    with open(ROOT_FILE, "r", encoding="utf-8") as f:
        print(f.read(), end="")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    {"build": build, "verify": verify, "show": show}.get(cmd, build)()
