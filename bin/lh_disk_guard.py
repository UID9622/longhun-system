#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 磁盘守护引擎 v1.0

功能：
  - 扫描 Downloads 大文件 → 自动归档到 LonghunDisk
  - 清理安全可删的系统/应用缓存
  - 磁盘低于阈值自动触发清理
  - 守护模式持续监控

用法：
  python3 lh_disk_guard.py scan     # 扫描并报告可清理项
  python3 lh_disk_guard.py clean    # 执行清理
  python3 lh_disk_guard.py watch    # 守护模式（自动监控）
  python3 lh_disk_guard.py status   # 查看清理统计

DNA: #龍芯⚡️2026-07-12-DISK-GUARD-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

# ── 常量 ──
HOME = Path.home()
ROOT = HOME / "longhun-system"
DOWNLOADS = HOME / "Downloads"
DRIVE_NAME = "LonghunDisk"
DRIVE_PATH = Path(f"/Volumes/{DRIVE_NAME}")
ARCHIVE_ROOT = DRIVE_PATH / "downloads_archive"
STATE_FILE = ROOT / "state" / "disk_guard_state.json"
LOG_FILE = ROOT / "logs" / "disk_guard.log"

# 磁盘阈值：剩余空间低于此值(GB)自动触发清理
FREE_SPACE_WARN_GB = 20
FREE_SPACE_CRITICAL_GB = 10

# Downloads 归档规则
ARCHIVE_MIN_SIZE_MB = 200       # 大于此大小的文件考虑归档
ARCHIVE_MIN_AGE_DAYS = 7        # 超过此天数未修改的考虑归档
ARCHIVE_EXTENSIONS = {           # 这些扩展名优先归档（安装包类）
    ".iso", ".dmg", ".pkg", ".tar.gz", ".tar.xz", ".tar.bz2",
    ".zip", ".7z", ".rar", ".app", ".mp4", ".mov", ".avi",
}

# 安全可清缓存列表（删了不影响系统和应用正常运行）
SAFE_CACHES: List[Tuple[str, str]] = [
    # (路径相对于 ~/Library/Caches/, 说明)
    ("kimi-desktop-updater", "Kimi 桌面更新缓存"),
    ("ms-playwright", "Playwright 浏览器缓存"),
    ("ms-playwright-mcp", "Playwright MCP 缓存"),
    ("Chromium", "Chromium 浏览器缓存"),
    ("Homebrew/downloads", "Homebrew 下载缓存"),
    ("node-gyp", "node-gyp 构建缓存"),
    ("typescript", "TypeScript 缓存"),
    ("pip-audit", "pip-audit 缓存"),
]

# 系统级安全可清缓存
SYSTEM_CACHES: List[Tuple[str, str]] = [
    ("/private/var/tmp/*", "系统临时文件（>7天）"),
]

CHECK_INTERVAL = 30  # 守护模式检测间隔(秒)

DNA = "#龍芯⚡️2026-07-12-DISK-GUARD-v1.0"


# ── 工具函数 ──
def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def fmt_size(bytes_val: int) -> str:
    """格式化文件大小"""
    mb = bytes_val / (1024 * 1024)
    if mb >= 1024:
        return f"{mb/1024:.1f} GB"
    return f"{mb:.1f} MB"


def get_free_space_gb() -> float:
    """获取系统盘剩余空间(GB)"""
    stat = os.statvfs("/")
    return (stat.f_bavail * stat.f_frsize) / (1024 ** 3)


def get_usage_percent() -> int:
    """获取磁盘使用率百分比"""
    stat = os.statvfs("/")
    return int((1 - stat.f_bavail / stat.f_blocks) * 100)


def is_drive_mounted() -> bool:
    return DRIVE_PATH.exists() and DRIVE_PATH.is_dir()


def get_date_tag() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def load_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {
        "total_cleaned_mb": 0,
        "total_archived_files": 0,
        "total_archived_mb": 0,
        "last_clean": None,
        "last_archive": None,
    }


def save_state(state: Dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


# ── 下载文件扫描与归档 ──
def scan_downloads() -> List[Dict[str, Any]]:
    """扫描 Downloads 中可归档的大文件"""
    candidates = []
    now = time.time()

    if not DOWNLOADS.exists():
        return candidates

    for f in DOWNLOADS.rglob("*"):
        if not f.is_file():
            continue
        # 跳过隐藏文件
        if f.name.startswith("."):
            continue
        # 跳过符号链接
        if f.is_symlink():
            continue
        # 跳过 .DS_Store 等系统文件
        if f.name == ".DS_Store":
            continue

        try:
            stat = f.stat()
        except (OSError, PermissionError):
            continue

        size_mb = stat.st_size / (1024 * 1024)
        age_days = (now - stat.st_mtime) / 86400
        ext = f.suffix.lower()

        # 归档条件（AND 逻辑组合）：
        #   条件A: 大文件 (>200MB) → 无条件归档候选
        #   条件B: 安装包类型 且 超过7天 → 归档候选
        #   不满足任一条件的忽略
        is_large = size_mb >= ARCHIVE_MIN_SIZE_MB
        is_installer = ext in ARCHIVE_EXTENSIONS
        is_old = age_days >= ARCHIVE_MIN_AGE_DAYS

        if not (is_large or (is_installer and is_old)):
            continue

        # 决定归档原因
        reasons = []
        priority = 0

        if is_large:
            reasons.append(f"大文件 ({fmt_size(stat.st_size)})")
            priority += 3

        if is_installer:
            reasons.append(f"安装包类型 ({ext})")
            priority += 2

        if is_old:
            reasons.append(f"已 {age_days:.0f} 天未修改")
            priority += 1

        candidates.append({
            "path": str(f),
            "name": f.name,
            "size_mb": round(size_mb, 1),
            "size_bytes": stat.st_size,
            "age_days": round(age_days, 1),
            "reasons": reasons,
            "priority": priority,
        })

    # 按优先级排序
    candidates.sort(key=lambda x: (-x["priority"], -x["size_mb"]))
    return candidates


def archive_downloads(candidates: List[Dict[str, Any]], dry_run: bool = False) -> Dict[str, Any]:
    """将可归档的下载文件移动到 LonghunDisk"""
    if not is_drive_mounted():
        msg = "LonghunDisk 未挂载，无法归档"
        log(f"  ⚠️  {msg}")
        return {"error": "drive_not_mounted", "msg": msg}

    if not candidates:
        return {"archived": 0, "size_mb": 0}

    date_tag = get_date_tag()
    dest_dir = ARCHIVE_ROOT / date_tag
    dest_dir.mkdir(parents=True, exist_ok=True)

    archived = 0
    total_size_mb = 0
    failed = []

    for item in candidates:
        src = Path(item["path"])
        dest = dest_dir / src.name

        if dry_run:
            archived += 1
            total_size_mb += item["size_mb"]
            log(f"  [DRY-RUN] {src.name} → {dest}")
            continue

        try:
            # 避免覆盖：如果存在同名文件，加序号
            if dest.exists():
                stem, ext = os.path.splitext(src.name)
                counter = 1
                while dest.exists():
                    dest = dest_dir / f"{stem}_{counter}{ext}"
                    counter += 1

            shutil.move(str(src), str(dest))
            archived += 1
            total_size_mb += item["size_mb"]
            log(f"  📦 {src.name} ({item['size_mb']:.1f} MB) → LonghunDisk")
        except Exception as e:
            failed.append({"file": src.name, "error": str(e)})
            log(f"  ❌ {src.name}: {e}")

    result = {
        "archived": archived,
        "size_mb": round(total_size_mb, 1),
        "dest": str(dest_dir),
        "failed": failed,
    }

    # 更新状态
    state = load_state()
    state["last_archive"] = get_date_tag()
    state["total_archived_files"] = state.get("total_archived_files", 0) + archived
    state["total_archived_mb"] = state.get("total_archived_mb", 0) + total_size_mb
    state["total_cleaned_mb"] = state.get("total_cleaned_mb", 0) + total_size_mb
    save_state(state)

    return result


# ── 缓存清理 ──
def scan_caches() -> List[Dict[str, Any]]:
    """扫描可安全清理的缓存"""
    candidates = []
    cache_base = HOME / "Library" / "Caches"

    for rel_path, desc in SAFE_CACHES:
        full_path = cache_base / rel_path
        if not full_path.exists():
            continue

        try:
            total_size = sum(
                f.stat().st_size
                for f in full_path.rglob("*")
                if f.is_file()
            )
        except (OSError, PermissionError):
            continue

        if total_size > 0:
            candidates.append({
                "path": str(full_path),
                "desc": desc,
                "size_mb": round(total_size / (1024 * 1024), 1),
                "size_bytes": total_size,
            })

    candidates.sort(key=lambda x: -x["size_mb"])
    return candidates


def clean_caches(candidates: List[Dict[str, Any]], dry_run: bool = False) -> Dict[str, Any]:
    """清理缓存目录"""
    cleaned = 0
    total_size_mb = 0
    failed = []

    for item in candidates:
        path = Path(item["path"])

        if dry_run:
            cleaned += 1
            total_size_mb += item["size_mb"]
            log(f"  [DRY-RUN] 清理 {path.name} ({item['size_mb']:.1f} MB) - {item['desc']}")
            continue

        try:
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
                # 重建空目录以防应用需要
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.unlink(missing_ok=True)

            cleaned += 1
            total_size_mb += item["size_mb"]
            log(f"  🧹 {path.name} ({item['size_mb']:.1f} MB) - {item['desc']}")
        except Exception as e:
            failed.append({"path": str(path), "error": str(e)})
            log(f"  ❌ {path.name}: {e}")

    # 额外清理 pip/npm 缓存（用各自命令）
    if not dry_run:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "cache", "purge"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                log("  🧹 pip 缓存已清理")
        except Exception:
            pass

        try:
            result = subprocess.run(
                ["npm", "cache", "clean", "--force"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                log("  🧹 npm 缓存已清理")
        except Exception:
            pass

    result = {
        "cleaned": cleaned,
        "size_mb": round(total_size_mb, 1),
        "failed": failed,
    }

    state = load_state()
    state["last_clean"] = get_date_tag()
    state["total_cleaned_mb"] = state.get("total_cleaned_mb", 0) + total_size_mb
    save_state(state)

    return result


# ── 系统临时文件清理 ──
def clean_system_tmp() -> float:
    """清理 /private/var/tmp 中超过7天的文件，返回释放的MB数"""
    tmp_dir = Path("/private/var/tmp")
    if not tmp_dir.exists():
        return 0

    cutoff = time.time() - 7 * 86400
    freed = 0

    try:
        for item in tmp_dir.iterdir():
            try:
                stat = item.stat()
                if stat.st_mtime < cutoff:
                    if item.is_dir():
                        size = sum(
                            f.stat().st_size
                            for f in item.rglob("*")
                            if f.is_file()
                        )
                        shutil.rmtree(item, ignore_errors=True)
                    else:
                        size = stat.st_size
                        item.unlink(missing_ok=True)
                    freed += size
            except (OSError, PermissionError):
                continue
    except Exception:
        pass

    freed_mb = freed / (1024 * 1024)
    if freed_mb > 0:
        log(f"  🧹 系统临时文件: {freed_mb:.1f} MB")
    return freed_mb


# ── 主操作 ──
def cmd_scan(json_output: bool = False) -> None:
    """扫描模式：报告可清理项"""
    print("🔍 龍魂磁盘扫描...")
    print(f"   磁盘使用率: {get_usage_percent()}%")
    print(f"   剩余空间: {get_free_space_gb():.1f} GB")
    print()

    # 下载文件
    dl_candidates = scan_downloads()
    print(f"📂 Downloads 可归档文件: {len(dl_candidates)} 个")
    if dl_candidates:
        total_dl_mb = sum(c["size_mb"] for c in dl_candidates)
        print(f"   可释放: {total_dl_mb:.1f} MB")
        for c in dl_candidates[:10]:
            print(f"   • {c['name']} ({c['size_mb']:.1f} MB, {c['age_days']:.0f}天) - {', '.join(c['reasons'])}")
        if len(dl_candidates) > 10:
            print(f"   ... 还有 {len(dl_candidates) - 10} 个")
    else:
        print("   暂无")

    print()

    # 缓存
    cache_candidates = scan_caches()
    print(f"🗑 可清理缓存: {len(cache_candidates)} 项")
    if cache_candidates:
        total_cache_mb = sum(c["size_mb"] for c in cache_candidates)
        print(f"   可释放: {total_cache_mb:.1f} MB")
        for c in cache_candidates:
            print(f"   • {c['desc']}: {c['size_mb']:.1f} MB")
    else:
        print("   暂无")

    total_free = sum(c["size_mb"] for c in dl_candidates) + sum(c["size_mb"] for c in cache_candidates)
    print(f"\n📊 共计可释放: {total_free:.1f} MB (~{total_free/1024:.1f} GB)")

    drive_status = "🟢 已挂载" if is_drive_mounted() else "⚪ 未挂载"
    print(f"💾 LonghunDisk: {drive_status}")

    if json_output:
        output = {
            "disk_usage_percent": get_usage_percent(),
            "free_space_gb": round(get_free_space_gb(), 1),
            "drive_mounted": is_drive_mounted(),
            "downloads_candidates": dl_candidates,
            "cache_candidates": cache_candidates,
            "total_freeable_mb": round(total_free, 1),
        }
        print(f"\n--- JSON ---\n{json.dumps(output, ensure_ascii=False, indent=2)}")


def cmd_clean(dry_run: bool = False) -> Dict[str, Any]:
    """清理模式：执行所有清理"""
    label = "[试运行] " if dry_run else ""
    log(f"🧹 龍魂磁盘清理开始 {label}")

    free_before = get_free_space_gb()
    log(f"   清理前剩余: {free_before:.1f} GB")

    result: Dict[str, Any] = {
        "timestamp": get_date_tag(),
        "free_before_gb": round(free_before, 1),
        "dry_run": dry_run,
    }

    # 1. 清理缓存
    cache_candidates = scan_caches()
    if cache_candidates:
        cache_result = clean_caches(cache_candidates, dry_run=dry_run)
        result["caches"] = cache_result

    # 2. 归档下载（需要 LonghunDisk）
    if is_drive_mounted():
        dl_candidates = scan_downloads()
        if dl_candidates:
            archive_result = archive_downloads(dl_candidates, dry_run=dry_run)
            result["downloads"] = archive_result
    else:
        log("   ⚠️  LonghunDisk 未挂载，跳过下载归档")
        dl_candidates = scan_downloads()
        if dl_candidates:
            total_dl_mb = sum(c["size_mb"] for c in dl_candidates)
            log(f"   📋 有 {len(dl_candidates)} 个文件({total_dl_mb:.1f} MB)待归档, 请插入硬盘")
            result["downloads"] = {"skipped": len(dl_candidates), "size_mb": round(total_dl_mb, 1)}

    # 3. 系统临时文件
    if not dry_run:
        tmp_freed = clean_system_tmp()
        result["tmp_freed_mb"] = round(tmp_freed, 1)

    free_after = get_free_space_gb()
    freed = free_after - free_before
    log(f"   清理后剩余: {free_after:.1f} GB (释放 {freed:.1f} GB)")
    log(f"🧹 清理完成")

    result["free_after_gb"] = round(free_after, 1)
    result["freed_gb"] = round(freed, 1)

    return result


def cmd_status() -> None:
    """查看清理统计"""
    state = load_state()
    free = get_free_space_gb()

    print("🐉 龍魂磁盘守护状态")
    print(f"   磁盘使用率: {get_usage_percent()}%")
    print(f"   剩余空间: {free:.1f} GB")
    print(f"   LonghunDisk: {'🟢 已挂载' if is_drive_mounted() else '⚪ 未挂载'}")
    print()
    print(f"   累计缓存清理: {state.get('total_cleaned_mb', 0):.1f} MB")
    print(f"   累计下载归档: {state.get('total_archived_files', 0)} 文件, {state.get('total_archived_mb', 0):.1f} MB")
    print(f"   上次缓存清理: {state.get('last_clean', '从未')}")
    print(f"   上次下载归档: {state.get('last_archive', '从未')}")


def watch_loop() -> None:
    """守护模式：持续监控磁盘空间"""
    log("👁 龍魂磁盘守护启动...")
    log(f"   警告阈值: {FREE_SPACE_WARN_GB} GB")
    log(f"   紧急阈值: {FREE_SPACE_CRITICAL_GB} GB")

    last_clean_date = None
    was_mounted = is_drive_mounted()

    while True:
        free = get_free_space_gb()
        is_mounted = is_drive_mounted()
        today = get_date_tag()

        # 硬盘插入时触发归档
        if is_mounted and not was_mounted:
            log(f"💾 LonghunDisk 已插入，触发下载归档...")
            dl_candidates = scan_downloads()
            if dl_candidates:
                archive_downloads(dl_candidates)
            last_clean_date = today  # 今天已经处理过了

        was_mounted = is_mounted

        # 磁盘空间不足时触发清理
        if free < FREE_SPACE_CRITICAL_GB and last_clean_date != today:
            log(f"🚨 磁盘紧急: {free:.1f} GB < {FREE_SPACE_CRITICAL_GB} GB, 自动清理...")
            cmd_clean()
            last_clean_date = today

        elif free < FREE_SPACE_WARN_GB and last_clean_date != today:
            log(f"⚠️  磁盘不足: {free:.1f} GB < {FREE_SPACE_WARN_GB} GB, 自动清理...")
            cmd_clean()
            last_clean_date = today

        # 每天重置
        if last_clean_date and last_clean_date != today:
            last_clean_date = None

        time.sleep(CHECK_INTERVAL)


def main() -> None:
    parser = argparse.ArgumentParser(description="🐉 龍魂磁盘守护引擎")
    parser.add_argument("action", nargs="?", default="scan",
                        choices=["scan", "clean", "watch", "status"])
    parser.add_argument("--dry-run", action="store_true",
                        help="试运行，不实际删除/移动文件")
    parser.add_argument("--json", action="store_true",
                        help="以JSON格式输出扫描结果")
    args = parser.parse_args()

    if args.action == "scan":
        cmd_scan(json_output=args.json)
    elif args.action == "clean":
        result = cmd_clean(dry_run=args.dry_run)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.action == "watch":
        watch_loop()
    elif args.action == "status":
        cmd_status()


if __name__ == "__main__":
    main()
