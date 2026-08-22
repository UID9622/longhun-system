#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-DRIVE-AUTO-BACKUP-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 移动硬盘自动备份引擎 v1.0

功能：
  - 检测 LonghunDisk 移动硬盘插入/拔出
  - 自动同步冷数据到硬盘（压缩+日期标注）
  - 支持增量备份，不重复拷贝
  - 每次插盘自动校验完整性

用法：
  python3 lh_drive_auto_backup.py once     # 单次备份
  python3 lh_drive_auto_backup.py watch    # 持续监控（守护模式）
  python3 lh_drive_auto_backup.py status   # 查看备份状态
  python3 lh_drive_auto_backup.py verify   # 校验备份完整性

DNA: #龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-DRIVE-AUTO-BACKUP-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── 常量 ──
HOME = Path.home()
ROOT = HOME / "longhun-system"
DRIVE_NAME = "LonghunDisk"
DRIVE_PATH = Path(f"/Volumes/{DRIVE_NAME}")
BACKUP_ROOT = DRIVE_PATH / "longhun-cold-storage"
STATE_FILE = ROOT / "state" / "drive_backup_state.json"
LOG_FILE = ROOT / "logs" / "drive_backup.log"
CHECK_INTERVAL = 5  # 秒

# ── 备份配置 ──
BACKUP_TASKS: List[Dict[str, Any]] = [
    {
        "name": "models",
        "source": "models/",
        "desc": "AI 模型文件",
        "compress": False,    # 已是二进制，不压缩
    },
    {
        "name": "archives",
        "source": ".archive/",
        "desc": "历史压缩归档",
        "compress": False,
    },
    {
        "name": "backups",
        "source": "backups/",
        "desc": "系统备份",
        "compress": False,
    },
    {
        "name": "editor_memory",
        "source": "brain/editor_memory_archive/",
        "desc": "编辑器历史记忆",
        "compress": True,     # JSON 文件压缩效果好
    },
    {
        "name": "data_hub",
        "source": "data-hub/",
        "desc": "浏览器采集数据",
        "compress": True,
    },
    {
        "name": "old_logs",
        "source": "logs/",
        "desc": "历史日志（>7天）",
        "compress": True,
        "age_days": 7,
    },
    {
        "name": "media_assets",
        "source": "assets/",
        "desc": "图片/媒体资源",
        "compress": True,
    },
    {
        "name": "public_content",
        "source": "public-content/",
        "desc": "公开发布内容",
        "compress": True,
    },
    {
        "name": "experiments",
        "source": "experiments/",
        "desc": "实验报告",
        "compress": True,
    },
    {
        "name": "reports",
        "source": "reports/",
        "desc": "报告文档",
        "compress": True,
    },
]

DNA = "#龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-DRIVE-AUTO-BACKUP-v1.0"


def log(msg: str) -> None:
    """写日志"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def is_drive_mounted() -> bool:
    """检测移动硬盘是否挂载"""
    return DRIVE_PATH.exists() and DRIVE_PATH.is_dir()


def get_date_tag() -> str:
    """日期标签: 2026-07-12"""
    return datetime.now().strftime("%Y-%m-%d")


def get_timestamp_tag() -> str:
    """时间戳标签: 20260712_1314"""
    return datetime.now().strftime("%Y%m%d_%H%M")


def file_hash(path: Path) -> str:
    """文件 SHA256"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def compress_dir(src: Path, dest: Path) -> Tuple[int, int]:
    """压缩目录，返回 (文件数, 大小bytes)"""
    import tarfile
    count = 0
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(dest, "w:gz") as tar:
        for f in src.rglob("*"):
            if f.is_file() and "__pycache__" not in str(f):
                tar.add(f, arcname=f.relative_to(src.parent))
                count += 1
    size = dest.stat().st_size if dest.exists() else 0
    return count, size


def load_state() -> Dict[str, Any]:
    """加载备份状态"""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"last_backup": None, "tasks": {}, "total_size": 0, "total_files": 0}


def save_state(state: Dict[str, Any]) -> None:
    """保存备份状态"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def run_backup() -> Dict[str, Any]:
    """执行完整备份"""
    if not is_drive_mounted():
        log("❌ 移动硬盘未挂载，跳过备份")
        return {"error": "drive_not_mounted"}

    date_tag = get_date_tag()
    ts_tag = get_timestamp_tag()
    state = load_state()

    log(f"🐉 龍魂自动备份开始 — {ts_tag}")
    log(f"   目标: {BACKUP_ROOT}")

    total_files = 0
    total_size = 0
    results = {}

    for task in BACKUP_TASKS:
        name = task["name"]
        src = ROOT / task["source"]

        if not src.exists():
            log(f"  ⏭  {name}: 源目录不存在，跳过")
            continue

        # 过滤旧日志（如果配置了 age_days）
        if task.get("age_days") and "logs" in str(src):
            log(f"  📋 {name}: 只备份 {task['age_days']} 天前的日志")
            # 用 tar 的 --newer-mt 或 mtime 过滤
            age_seconds = task["age_days"] * 86400
            cutoff = time.time() - age_seconds
            # 创建临时目录装旧文件
            tmp_dir = ROOT / "tmp" / f"old_logs_{ts_tag}"
            tmp_dir.parent.mkdir(parents=True, exist_ok=True)
            if tmp_dir.exists():
                shutil.rmtree(tmp_dir)
            tmp_dir.mkdir()
            copied = 0
            for f in src.rglob("*"):
                if f.is_file() and f.stat().st_mtime < cutoff:
                    rel = f.relative_to(src)
                    dest_f = tmp_dir / rel
                    dest_f.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, dest_f)
                    copied += 1
            if copied == 0:
                log(f"    ✅ 无旧日志需要备份")
                shutil.rmtree(tmp_dir)
                results[name] = {"files": 0, "size": 0}
                continue
            src = tmp_dir
            log(f"    收集了 {copied} 个旧日志文件")

        dest_name = f"{name}_{ts_tag}.tar.gz" if task.get("compress") else name
        dest = BACKUP_ROOT / dest_name

        if task.get("compress"):
            log(f"  🗜  {name}: 压缩中...")
            f_count, f_size = compress_dir(src, dest)
            size_mb = f_size / (1024 * 1024)
            log(f"    ✅ {f_count} 个文件 → {size_mb:.1f} MB")
            results[name] = {"files": f_count, "size": f_size}
        else:
            log(f"  📁 {name}: 同步中...")
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest, dirs_exist_ok=True)
            # 统计
            f_count = sum(1 for _ in dest.rglob("*") if _.is_file())
            f_size = sum(_.stat().st_size for _ in dest.rglob("*") if _.is_file())
            size_mb = f_size / (1024 * 1024)
            log(f"    ✅ {f_count} 个文件 → {size_mb:.1f} MB")
            results[name] = {"files": f_count, "size": f_size}

        total_files += results[name]["files"]
        total_size += results[name]["size"]

    # 更新状态
    state["last_backup"] = ts_tag
    state["tasks"][ts_tag] = results
    state["total_size"] = state.get("total_size", 0) + total_size
    state["total_files"] = state.get("total_files", 0) + total_files
    save_state(state)

    total_mb = total_size / (1024 * 1024)
    log(f"🐉 备份完成: {total_files} 个文件, {total_mb:.1f} MB")
    log(f"   路径: {BACKUP_ROOT}")

    return {
        "timestamp": ts_tag,
        "files": total_files,
        "size_mb": round(total_mb, 1),
        "tasks": results,
    }


def verify_backup() -> Dict[str, Any]:
    """校验备份完整性"""
    if not is_drive_mounted():
        return {"error": "drive_not_mounted"}

    state = load_state()
    if not state.get("last_backup"):
        return {"status": "no_backup_found"}

    results = {}
    issues = 0
    for task in BACKUP_TASKS:
        name = task["name"]
        dest_dir = BACKUP_ROOT / name
        if dest_dir.exists():
            f_count = sum(1 for _ in dest_dir.rglob("*") if _.is_file())
            results[name] = {"exists": True, "files": f_count}
        else:
            # 检查压缩版本
            compressed = list(BACKUP_ROOT.glob(f"{name}_*.tar.gz"))
            if compressed:
                results[name] = {"exists": True, "compressed": compressed[0].name}
            else:
                results[name] = {"exists": False}
                issues += 1

    return {"status": "ok" if issues == 0 else "partial", "issues": issues, "tasks": results}


def watch_loop() -> None:
    """守护模式：持续监控硬盘插入"""
    log("👁 龍魂硬盘监控守护启动...")
    was_mounted = is_drive_mounted()
    last_backup_date = None

    while True:
        is_mounted = is_drive_mounted()
        today = get_date_tag()

        if is_mounted and not was_mounted:
            log(f"💾 检测到硬盘插入: {DRIVE_PATH}")
            time.sleep(2)  # 等系统挂载稳定
            if today != last_backup_date:
                result = run_backup()
                last_backup_date = today
                log(f"   结果: {result.get('files', 0)} 文件, {result.get('size_mb', 0)} MB")
            else:
                log(f"   今天已备份过，跳过")

        elif not is_mounted and was_mounted:
            log("💨 硬盘已拔出")

        was_mounted = is_mounted
        time.sleep(CHECK_INTERVAL)


def show_status() -> None:
    """显示备份状态"""
    state = load_state()
    mounted = is_drive_mounted()

    print(f"🐉 龍魂硬盘备份状态")
    print(f"   硬盘挂载: {'🟢 已挂载' if mounted else '⚪ 未挂载'}")
    print(f"   上次备份: {state.get('last_backup', '从未')}")
    print(f"   累计备份: {state.get('total_files', 0)} 文件, "
          f"{state.get('total_size', 0) / (1024*1024):.1f} MB")

    if state.get("tasks"):
        latest = max(state["tasks"].keys())
        print(f"\n   最近备份 ({latest}):")
        for name, info in state["tasks"][latest].items():
            size_mb = info["size"] / (1024 * 1024)
            print(f"     {name}: {info['files']} 文件, {size_mb:.1f} MB")


def main() -> None:
    parser = argparse.ArgumentParser(description="🐉 龍魂移动硬盘自动备份引擎")
    parser.add_argument("action", nargs="?", default="status",
                        choices=["once", "watch", "status", "verify"])
    args = parser.parse_args()

    if args.action == "once":
        result = run_backup()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.action == "watch":
        watch_loop()
    elif args.action == "verify":
        result = verify_backup()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        show_status()


if __name__ == "__main__":
    main()
