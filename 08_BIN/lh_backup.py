#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════
# lh_backup.py — 龍魂状态一键备份（任务C 生态补全）
# DNA: #龍芯⚡️2026-09-03-ECOSYSTEM-BACKUP-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）· 龍芯北辰
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用法: python3 08_BIN/lh_backup.py [--keep 7] [--list] [--info <文件>]
#   默认: 备份 ~/.longhun/ → ~/backups/longhun/longhun-<UTCts>.tar.gz
#   --keep N   仅保留最近 N 份（默认 7）
#   --list     列出全部备份
#   --info     查看指定备份内容清单
# 铁律: 零三方依赖(stdlib tarfile) · 备份内不落密钥明文到日志
# ═══════════════════════════════════════════════════════════
"""龍魂状态备份引擎。tar.gz 打包 ~/.longhun（图谱快照/耻辱墙/治理状态等）。"""
import argparse
import json
import os
import shutil
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

SRC = Path.home() / ".longhun"
BACKUP_ROOT = Path.home() / "backups" / "longhun"
MANIFEST = BACKUP_ROOT / "manifest.json"
KEEP_DEFAULT = 7


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _manifest_read() -> dict:
    if MANIFEST.is_file():
        try:
            return json.loads(MANIFEST.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"created_by": "诸葛鑫 | UID9622 · 龍芯北辰", "backups": []}


def _manifest_write(m: dict):
    MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_backup(keep: int = KEEP_DEFAULT, quiet: bool = False) -> int:
    if not SRC.is_dir():
        print(f"❌ 源目录不存在: {SRC}")
        return 1
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    ts = _ts()
    target = BACKUP_ROOT / f"longhun-{ts}.tar.gz"

    def _filter(ti: tarfile.TarInfo):
        ti.name = "longhun/" + ti.name.lstrip("/")
        return ti

    try:
        with tarfile.open(target, "w:gz") as tf:
            tf.add(SRC, arcname="longhun", filter=_filter)
    except Exception as e:  # noqa: BLE001
        print(f"❌ 备份失败: {e}")
        return 1
    size = target.stat().st_size
    if not quiet:
        print(f"\n  💾 龍魂状态备份完成")
        print(f"     源   {SRC}")
        print(f"     档   {target} ({size/1024:.1f} KB)")
    m = _manifest_read()
    m["backups"].append({"file": target.name, "ts": ts, "size": size,
                         "src": str(SRC)})
    # 只保留最近 keep 份 + manifest
    m["backups"] = m["backups"][-keep:]
    # 清理磁盘旧档
    keep_files = {b["file"] for b in m["backups"]}
    for f in sorted(BACKUP_ROOT.glob("longhun-*.tar.gz")):
        if f.name not in keep_files:
            f.unlink(missing_ok=True)
    _manifest_write(m)
    if not quiet:
        print(f"     保留最近 {keep} 份 · 共 {len(m['backups'])} 份在册")
    return 0


def cmd_list():
    m = _manifest_read()
    if not m["backups"]:
        print("  （无备份记录）")
        return 0
    print(f"\n  💾 龍魂状态备份清单 · {BACKUP_ROOT}")
    for b in reversed(m["backups"]):
        print(f"     · {b['ts']}  {b['file']}  ({b['size']/1024:.1f} KB)")
    return 0


def cmd_info(name: str):
    p = BACKUP_ROOT / name
    if not p.is_file():
        print(f"❌ 备份不存在: {p}")
        return 1
    with tarfile.open(p, "r:gz") as tf:
        entries = [m for m in tf.getmembers() if m.isfile()]
    print(f"\n  📦 {name} · {len(entries)} 个文件 · 顶层目录:")
    tops = {}
    for e in entries:
        parts = e.name.split("/")
        tops[parts[1] if len(parts) > 1 else e.name] = tops.get(
            parts[1] if len(parts) > 1 else e.name, 0) + 1
    for k, v in sorted(tops.items()):
        print(f"     · {k}: {v} 文件")
    return 0


def main():
    ap = argparse.ArgumentParser(description="💾 龍魂状态一键备份 (lh backup)")
    ap.add_argument("--keep", type=int, default=KEEP_DEFAULT, help="保留最近 N 份(默认 7)")
    ap.add_argument("--list", action="store_true", help="列出全部备份")
    ap.add_argument("--info", metavar="FILE", default="", help="查看指定备份内容")
    ap.add_argument("--quiet", "-q", action="store_true", help="静默模式")
    args = ap.parse_args()
    if args.list:
        return cmd_list()
    if args.info:
        return cmd_info(args.info)
    return cmd_backup(keep=max(1, args.keep), quiet=args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
