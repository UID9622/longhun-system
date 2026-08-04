#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-

# DNA: #龍芯⚡️2026-06-24-LONGHUN-CLEAN-DUPLICATES-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""
清理 Downloads/Kimi_Agent_* 中的重复脚本副本
保留每个文件最新版本，将旧副本移动到废纸篓目录（可手动确认后删除）

用法:
    python3 clean-kimi-download-duplicates.py --dry-run
    python3 clean-kimi-download-duplicates.py --execute
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime


DNA = "#龍芯⚡️2026-06-24-LONGHUN-CLEAN-DUPLICATES-v1.0"


def main():
    parser = argparse.ArgumentParser(description="清理 Kimi_Agent 重复下载副本")
    parser.add_argument("--execute", action="store_true", help="真正执行移动（默认仅预览）")
    parser.add_argument("--base", default=str(Path.home() / "Downloads"), help="下载目录")
    args = parser.parse_args()

    base = Path(args.base)
    kimi_dirs = sorted(
        [d for d in base.iterdir() if d.is_dir() and d.name.startswith("Kimi_Agent_")],
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )

    if not kimi_dirs:
        print("未发现 Downloads/Kimi_Agent_* 目录")
        return

    print(f"🐉 龍魂重复副本清理工具 · {DNA}")
    print(f"   扫描到 {len(kimi_dirs)} 个 Kimi_Agent 目录")
    print(f"   保留策略：按目录修改时间，只保留每个文件的最新版本")
    print("")

    # 收集所有文件（相对于 Kimi_Agent 根目录的相对路径）
    files_by_relpath = defaultdict(list)
    for d in kimi_dirs:
        for f in d.rglob("*"):
            if f.is_file() and f.stat().st_size > 0:
                rel = f.relative_to(d)
                rel_str = str(rel)
                # 跳过系统文件和缓存
                if ".DS_Store" in rel_str or "__pycache__" in rel_str or rel_str.endswith(".pyc"):
                    continue
                files_by_relpath[rel_str].append((d, f))

    trash_dir = base / f"Kimi_Agent_重复副本回收站_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    moved = 0
    moved_bytes = 0

    for name, entries in sorted(files_by_relpath.items()):
        if len(entries) <= 1:
            continue
        # 按目录修改时间排序，最新的保留
        entries.sort(key=lambda x: x[0].stat().st_mtime, reverse=True)
        keep_dir, keep_file = entries[0]
        duplicates = entries[1:]
        print(f"📁 {name}")
        print(f"   ✅ 保留: {keep_file} (来自 {keep_dir.name})")
        for dup_dir, dup_file in duplicates:
            rel = dup_file.relative_to(base)
            target = trash_dir / rel
            print(f"   🗑️  移动: {dup_file} -> {target}")
            if args.execute:
                try:
                    if not dup_file.exists():
                        print(f"   ⚠️  源文件已不存在，跳过")
                        continue
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(dup_file), str(target))
                    moved += 1
                    moved_bytes += target.stat().st_size
                except Exception as e:
                    print(f"   ⚠️  移动失败: {e}")
        print("")

    # 清理空目录
    empty_removed = 0
    if args.execute:
        for d in sorted(kimi_dirs, reverse=True):
            try:
                # 只删除空的 Kimi_Agent 子目录
                for sub in list(d.rglob("*")):
                    if sub.is_dir() and not any(sub.iterdir()):
                        sub.rmdir()
                if d.exists() and not any(d.iterdir()):
                    d.rmdir()
                    empty_removed += 1
            except Exception as e:
                print(f"   ⚠️ 无法删除空目录 {d}: {e}")

    print("=" * 60)
    print(f"统计: 发现重复文件 {moved} 个，约 {moved_bytes / 1024 / 1024:.1f} MB")
    if args.execute:
        print(f"       已移动到回收站: {trash_dir}")
        print(f"       已删除空目录: {empty_removed} 个")
        print("       请检查回收站，确认无误后可手动删除")
    else:
        print("       以上为预览，未真正移动。加 --execute 执行")
    print("=" * 60)


if __name__ == "__main__":
    main()
