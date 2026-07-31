#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·相册整理脚本
DNA: #龍芯⚡️丙午·癸未·丁未-ORGANIZE-PHOTOS-v1.0
功能：按拍摄日期（EXIF）整理照片/视频到 年/年-月 目录，自动去重
"""

import argparse
import hashlib
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# 支持的媒体扩展名
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".gif", ".heic", ".webp"}
VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".m4v", ".3gp"}
MEDIA_EXTS = IMAGE_EXTS | VIDEO_EXTS


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _exif_date(path: Path) -> Optional[datetime]:
    """从 EXIF 读取拍摄时间"""
    if not HAS_PIL:
        return None
    try:
        with Image.open(path) as img:
            exif = img._getexif()
            if not exif:
                return None
            exif_data = {TAGS.get(k, k): v for k, v in exif.items()}
            date_str = exif_data.get("DateTimeOriginal") or exif_data.get("DateTime")
            if date_str:
                return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    return None


def _file_creation_date(path: Path) -> datetime:
    """回退：用文件修改时间"""
    mtime = path.stat().st_mtime
    return datetime.fromtimestamp(mtime)


def _resolve_date(path: Path) -> Tuple[datetime, str]:
    d = _exif_date(path)
    if d:
        return d, "EXIF"
    return _file_creation_date(path), "文件时间"


def organize(
    src: Path,
    dest: Path,
    dry_run: bool = False,
    move: bool = False,
) -> dict:
    stats = {"scanned": 0, "copied": 0, "skipped": 0, "errors": 0, "duplicates": 0}
    seen_hashes: set[str] = set()

    for path in src.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in MEDIA_EXTS:
            continue

        stats["scanned"] += 1
        try:
            file_hash = _sha256(path)
            if file_hash in seen_hashes:
                stats["duplicates"] += 1
                print(f"🔄 重复跳过: {path}")
                continue
            seen_hashes.add(file_hash)

            date, source = _resolve_date(path)
            target_dir = dest / f"{date.year}" / f"{date.year}-{date.month:02d}"
            target_path = target_dir / path.name

            # 处理重名
            counter = 1
            stem = target_path.stem
            suffix = target_path.suffix
            while target_path.exists():
                target_path = target_dir / f"{stem}_{counter:03d}{suffix}"
                counter += 1

            action = "移动" if move else "复制"
            if dry_run:
                print(f"[DRY-RUN] {action}: {path} -> {target_path}  ({source})")
            else:
                target_dir.mkdir(parents=True, exist_ok=True)
                if move:
                    shutil.move(str(path), str(target_path))
                else:
                    shutil.copy2(str(path), str(target_path))
                print(f"✅ {action}完成: {target_path.name}  ({source})")
            stats["copied"] += 1

        except Exception as e:
            stats["errors"] += 1
            print(f"❌ 错误: {path} -> {e}")

    return stats


def main():
    parser = argparse.ArgumentParser(description="龍魂相册整理器：按日期整理照片/视频")
    parser.add_argument("src", type=Path, help="源相册目录")
    parser.add_argument("dest", type=Path, help="目标整理目录")
    parser.add_argument("--dry-run", action="store_true", help="只预览，不真正操作")
    parser.add_argument("--move", action="store_true", help="移动而非复制")
    parser.add_argument("--include-video", action="store_true", default=True, help="包含视频")
    args = parser.parse_args()

    if not args.src.exists():
        print(f"❌ 源目录不存在: {args.src}")
        sys.exit(1)

    if not args.include_video:
        global MEDIA_EXTS
        MEDIA_EXTS = IMAGE_EXTS

    print(f"\n🐉 龍魂相册整理器启动")
    print(f"   源目录: {args.src}")
    print(f"   目标目录: {args.dest}")
    print(f"   模式: {'预览' if args.dry_run else '移动' if args.move else '复制'}")
    print(f"   Pillow: {'可用' if HAS_PIL else '不可用，使用文件修改时间'}")
    print()

    stats = organize(args.src, args.dest, dry_run=args.dry_run, move=args.move)

    print(f"\n📊 整理完成")
    print(f"   扫描: {stats['scanned']}")
    print(f"   处理: {stats['copied']}")
    print(f"   重复: {stats['duplicates']}")
    print(f"   错误: {stats['errors']}")
    print(f"\n🧬 DNA: #龍芯⚡️丙午·癸未·丁未-ORGANIZE-PHOTOS-v1.0")


if __name__ == "__main__":
    main()
