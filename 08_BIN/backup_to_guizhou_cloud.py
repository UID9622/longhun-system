#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·庚申·丙寅·未时·䷐随-GZCLOUD-BACKUP-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🐉 龍魂 · 贵州云（iCloud 云上贵州）备份桥 v1.0

把鲲鹏 / 本地需要长期归档的数据，加密后背回到 iCloud 云上贵州目录。
数据主权：密钥在本地，云端只存密文 + DNA 索引。

用法:
  python3 08_BIN/backup_to_guizhou_cloud.py --scan
  python3 08_BIN/backup_to_guizhou_cloud.py --backup-kunpeng
  python3 08_BIN/backup_to_guizhou_cloud.py --backup-local ~/longhun-system
  python3 08_BIN/backup_to_guizhou_cloud.py --restore <manifest_id>
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

ICLOUD_BACKUP_DIR = Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs" / "龍魂系统备份"
LOCAL_INDEX_DIR = Path.home() / ".cnsh" / "backup_index"
KUNPENG_HOST = "119.13.90.27"
KUNPENG_USER = "root"
KUNPENG_KEY = Path.home() / ".ssh" / "longhun_kunpeng_ed25519"
CHUNK_SIZE = 256 * 1024 * 1024  # 256MB 分片


def generate_dna(tag: str) -> str:
    ts = datetime.now().strftime("%Y-%m-%d")
    h = hashlib.md5(f"{tag}{ts}{UID}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{tag}-{h}-{UID}"


def ensure_dirs():
    ICLOUD_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_INDEX_DIR.mkdir(parents=True, exist_ok=True)


def run_ssh(cmd: str, timeout: int = 60) -> Tuple[int, str, str]:
    """在鲲鹏上执行命令"""
    key = KUNPENG_KEY if KUNPENG_KEY.exists() else None
    if not key:
        return 1, "", f"鲲鹏私钥不存在: {KUNPENG_KEY}"
    full = ["ssh", "-i", str(key), "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=10",
            f"{KUNPENG_USER}@{KUNPENG_HOST}", cmd]
    r = subprocess.run(full, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def gpg_encrypt_file(src: Path, dst: Path) -> bool:
    """用 GPG 对称加密文件，密钥由用户本地口令派生"""
    try:
        subprocess.run(
            ["gpg", "--batch", "--yes", "--pinentry-mode", "loopback",
             "--symmetric", "--cipher-algo", "AES256", "--output", str(dst), str(src)],
            check=True, capture_output=True, text=True
        )
        return True
    except Exception as e:
        print(f"  ❌ 加密失败 {src}: {e}")
        return False


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def split_and_encrypt(src: Path, dst_dir: Path, manifest_id: str) -> List[Dict]:
    """把大文件分片并加密，返回分片清单"""
    chunks = []
    total_size = src.stat().st_size
    part_idx = 0
    with open(src, "rb") as f:
        while True:
            data = f.read(CHUNK_SIZE)
            if not data:
                break
            part_idx += 1
            part_plain = dst_dir / f"{manifest_id}_part{part_idx:04d}.bin"
            part_cipher = dst_dir / f"{manifest_id}_part{part_idx:04d}.bin.gpg"
            with open(part_plain, "wb") as pf:
                pf.write(data)
            if not gpg_encrypt_file(part_plain, part_cipher):
                part_plain.unlink(missing_ok=True)
                return []
            part_plain.unlink(missing_ok=True)
            chunks.append({
                "index": part_idx,
                "cipher": part_cipher.name,
                "size": part_cipher.stat().st_size,
                "sha256": sha256_file(part_cipher),
                "dna": generate_dna(f"CHUNK-{manifest_id}-{part_idx}")
            })
    return chunks


def scan_kunpeng_backups() -> List[Dict]:
    """扫描鲲鹏 /backup 下的大文件"""
    code, out, err = run_ssh("find /backup -type f -size +100M -printf '%s %p\\n' 2>/dev/null | sort -n", timeout=30)
    items = []
    if code != 0:
        print(f"⚠️ 扫描鲲鹏失败: {err}")
        return items
    for line in out.strip().splitlines():
        if not line.strip():
            continue
        size_str, path = line.split(" ", 1)
        items.append({
            "path": path,
            "size_bytes": int(size_str),
            "size_human": human_size(int(size_str)),
            "source": "kunpeng"
        })
    return items


def human_size(n: int) -> str:
    for unit in ["B", "K", "M", "G", "T"]:
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}P"


def backup_kunpeng_to_icloud(paths: Optional[List[str]] = None, keep_source: bool = False):
    """把鲲鹏指定路径备份到 iCloud 贵州云"""
    ensure_dirs()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    manifest_id = f"KUNPENG_{timestamp}"
    work_dir = LOCAL_INDEX_DIR / manifest_id
    work_dir.mkdir(parents=True, exist_ok=True)
    cloud_dir = ICLOUD_BACKUP_DIR / manifest_id
    cloud_dir.mkdir(parents=True, exist_ok=True)

    items = []
    if paths:
        for p in paths:
            code, out, err = run_ssh(f"test -f {p} && echo exists || echo missing", timeout=10)
            if out.strip() == "exists":
                code2, out2, _ = run_ssh(f"stat -c %s {p}", timeout=10)
                items.append({"path": p, "size_bytes": int(out2.strip()), "source": "kunpeng"})
            else:
                print(f"⚠️ 鲲鹏上不存在: {p}")
    else:
        items = scan_kunpeng_backups()

    if not items:
        print("🎉 没有需要备份的项目")
        return

    manifest = {
        "manifest_id": manifest_id,
        "dna": generate_dna("GZCLOUD-BACKUP"),
        "confirm": CONFIRM,
        "created_at": datetime.now().isoformat(),
        "source_host": KUNPENG_HOST,
        "backup_type": "kunpeng_to_guizhou_icloud",
        "items": []
    }

    print(f"📦 开始备份 {len(items)} 个项目到 iCloud 云上贵州...")
    for item in items:
        print(f"  🔄 {item['path']} ({human_size(item['size_bytes'])})")
        local_raw = work_dir / Path(item["path"]).name

        # 用 scp 拉到本地
        key_opt = f"-i {KUNPENG_KEY}" if KUNPENG_KEY.exists() else ""
        scp_cmd = f"scp {key_opt} -o StrictHostKeyChecking=no -o ConnectTimeout=10 {KUNPENG_USER}@{KUNPENG_HOST}:{item['path']} {local_raw}"
        r = subprocess.run(scp_cmd, shell=True, capture_output=True, text=True, timeout=3600)
        if r.returncode != 0:
            print(f"    ❌ scp 失败: {r.stderr}")
            continue

        sha_plain = sha256_file(local_raw)
        # 分片加密
        chunks = split_and_encrypt(local_raw, cloud_dir, manifest_id)
        if not chunks:
            print(f"    ❌ 分片加密失败")
            continue

        # 删除本地明文副本
        local_raw.unlink(missing_ok=True)

        entry = {
            "source_path": item["path"],
            "source_host": KUNPENG_HOST,
            "sha256_plain": sha_plain,
            "size_bytes": item["size_bytes"],
            "chunks": chunks,
            "dna": generate_dna(f"BACKUP-{Path(item['path']).name}")
        }
        manifest["items"].append(entry)
        print(f"    ✅ 已备份 {len(chunks)} 个分片")

        if not keep_source:
            print(f"    🗑️  删除鲲鹏源文件...")
            run_ssh(f"rm -f {item['path']}", timeout=10)

    # 保存清单并签章
    manifest_path = cloud_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    asc_path = cloud_dir / "manifest.json.asc"
    subprocess.run(
        ["gpg", "--batch", "--yes", "--pinentry-mode", "loopback",
         "--armor", "--detach-sign", "--default-key", GPG_KEY,
         "--output", str(asc_path), str(manifest_path)],
        check=True, capture_output=True, text=True
    )

    # 本地保留索引
    index_path = LOCAL_INDEX_DIR / f"{manifest_id}.json"
    shutil.copy2(manifest_path, index_path)

    print(f"\n✅ 备份完成: {cloud_dir}")
    print(f"🧬 DNA: {manifest['dna']}")
    print(f"🔐 清单签名: {asc_path}")


def backup_local_to_icloud(src_dir: str, label: str = "longhun-system"):
    """把本地目录打包加密后备份到 iCloud 贵州云"""
    ensure_dirs()
    src = Path(src_dir).resolve()
    if not src.exists():
        print(f"❌ 源目录不存在: {src}")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    manifest_id = f"LOCAL_{label}_{timestamp}"
    work_dir = LOCAL_INDEX_DIR / manifest_id
    work_dir.mkdir(parents=True, exist_ok=True)
    cloud_dir = ICLOUD_BACKUP_DIR / manifest_id
    cloud_dir.mkdir(parents=True, exist_ok=True)

    tar_name = f"{label}_{timestamp}.tar.gz"
    tar_path = work_dir / tar_name

    print(f"📦 打包本地目录: {src}")
    subprocess.run(
        ["tar", "czf", str(tar_path), "-C", str(src.parent), str(src.name)],
        check=True
    )

    sha_plain = sha256_file(tar_path)
    chunks = split_and_encrypt(tar_path, cloud_dir, manifest_id)
    tar_path.unlink(missing_ok=True)

    manifest = {
        "manifest_id": manifest_id,
        "dna": generate_dna("GZCLOUD-LOCAL-BACKUP"),
        "confirm": CONFIRM,
        "created_at": datetime.now().isoformat(),
        "source_host": "localhost",
        "backup_type": "local_to_guizhou_icloud",
        "items": [{
            "source_path": str(src),
            "source_host": "localhost",
            "sha256_plain": sha_plain,
            "size_bytes": sum(c["size"] for c in chunks),
            "chunks": chunks,
            "dna": generate_dna(f"LOCAL-BACKUP-{label}")
        }]
    }

    manifest_path = cloud_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    asc_path = cloud_dir / "manifest.json.asc"
    subprocess.run(
        ["gpg", "--batch", "--yes", "--pinentry-mode", "loopback",
         "--armor", "--detach-sign", "--default-key", GPG_KEY,
         "--output", str(asc_path), str(manifest_path)],
        check=True, capture_output=True, text=True
    )

    index_path = LOCAL_INDEX_DIR / f"{manifest_id}.json"
    shutil.copy2(manifest_path, index_path)

    print(f"\n✅ 本地备份完成: {cloud_dir}")
    print(f"🧬 DNA: {manifest['dna']}")


def list_backups():
    ensure_dirs()
    print("🗂️  iCloud 云上贵州备份清单:\n")
    for d in sorted(ICLOUD_BACKUP_DIR.iterdir()):
        if d.is_dir() and (d / "manifest.json").exists():
            with open(d / "manifest.json", "r", encoding="utf-8") as f:
                m = json.load(f)
            items = len(m.get("items", []))
            size = sum(sum(c.get("size", 0) for c in i.get("chunks", [])) for i in m.get("items", []))
            print(f"  📁 {d.name}")
            print(f"     项目数: {items}  总大小: {human_size(size)}  DNA: {m.get('dna', 'N/A')[:40]}...")


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 贵州云备份桥")
    parser.add_argument("--scan", action="store_true", help="扫描鲲鹏可备份项目")
    parser.add_argument("--backup-kunpeng", action="store_true", help="备份鲲鹏 /backup 下大文件到 iCloud")
    parser.add_argument("--backup-local", metavar="DIR", help="备份本地目录到 iCloud")
    parser.add_argument("--label", default="longhun-system", help="本地备份标签")
    parser.add_argument("--paths", nargs="+", help="指定鲲鹏上要备份的文件路径")
    parser.add_argument("--keep-source", action="store_true", help="备份后保留鲲鹏源文件")
    parser.add_argument("--list", action="store_true", help="列出已备份清单")
    args = parser.parse_args()

    if args.scan:
        items = scan_kunpeng_backups()
        print(f"🔍 鲲鹏上发现 {len(items)} 个可备份项目:")
        for it in items:
            print(f"  {it['path']} ({it['size_human']})")
    elif args.backup_kunpeng:
        backup_kunpeng_to_icloud(paths=args.paths, keep_source=args.keep_source)
    elif args.backup_local:
        backup_local_to_icloud(args.backup_local, label=args.label)
    elif args.list:
        list_backups()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
