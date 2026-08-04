#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
龍魂·项目瘦身引擎 v3.0 — 一枪到底
DNA: #龍芯⚡️丙午·乙申·己酉·亥时·SLIM-v3.0
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772ZLU-ORIGIN-FULLSYNC

八枪连发精准瘦身：
  1. models/ 删已部署的merged+gguf → 保留adapter+data
  2. L7_数据层/daoyin/mirror/ 删git克隆镜像
  3. voice-twin/ 删python venv
  4. 全域 node_modules/ 删
  5. container_data/ gzip压缩archive+audit
  6. brain/ 归档旧记忆到archive/
  7. logs/ gzip压缩>1MB日志
  8. 全域残留清理: __pycache__/.pyc/空目录/所有.venv*
"""

import os
import gzip
import shutil
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent

STATS = {"deleted_size": 0, "gzip_count": 0, "deleted_dirs": 0, "deleted_files": 0}


def size_mb(path: Path) -> float:
    if not path.exists():
        return 0
    if path.is_file():
        return path.stat().st_size / (1024 * 1024)
    total = 0
    for f in path.rglob("*"):
        if f.is_file():
            total += f.stat().st_size
    return total / (1024 * 1024)


def fmt(sz_mb: float) -> str:
    if sz_mb >= 1024:
        return f"{sz_mb/1024:.1f}GB"
    return f"{sz_mb:.0f}MB"


def safe_delete(target: Path, label: str) -> None:
    if not target.exists():
        print(f"  ⏭️  {label}: 不存在，跳过")
        return
    sz = size_mb(target)
    try:
        if target.is_dir():
            shutil.rmtree(target)
            STATS["deleted_dirs"] += 1
        else:
            target.unlink()
            STATS["deleted_files"] += 1
        STATS["deleted_size"] += sz
        print(f"  ✅ {label}: 释放 {fmt(sz)}")
    except Exception as e:
        print(f"  ❌ {label}: {e}")


def gzip_file(filepath: Path) -> None:
    if not filepath.exists():
        return
    orig_sz = size_mb(filepath)
    gz_path = filepath.with_suffix(filepath.suffix + ".gz")
    with open(filepath, "rb") as f_in:
        with gzip.open(gz_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    gz_sz = size_mb(gz_path)
    filepath.unlink()
    STATS["gzip_count"] += 1
    STATS["deleted_size"] += (orig_sz - gz_sz)
    print(f"  ✅ gzip {filepath.name}: {fmt(orig_sz)} → {fmt(gz_sz)} (省 {fmt(orig_sz-gz_sz)})")


def run():
    print("🔫 龍魂·项目瘦身引擎 v3.0")
    print(f"   项目: {ROOT}")
    print()

    # ── 枪1: models/ ──
    print("🔫 [1/8] models/ 删除已部署到ollama的旧模型")
    safe_delete(ROOT / "models/longhun-v1.0/lora_output/merged_v2.1", "merged_v2.1 (safetensors)")
    safe_delete(ROOT / "models/longhun-v1.0/lora_output/gguf_v2.1", "gguf_v2.1 (GGUF)")
    safe_delete(ROOT / "models/longhun-v1.0/lora_output/merged", "merged (旧v1.x)")
    safe_delete(ROOT / "models/longhun-v1.0/lora_output/gguf", "gguf (空目录)")
    print(f"   📊 models/ 现在: {fmt(size_mb(ROOT / 'models'))}")
    print()

    # ── 枪2: L7 mirror ──
    print("🔫 [2/8] L7_数据层/daoyin/mirror/ 删除git克隆镜像")
    safe_delete(ROOT / "L7_数据层/daoyin/mirror", "git克隆仓库")
    print(f"   📊 L7_数据层/ 现在: {fmt(size_mb(ROOT / 'L7_数据层'))}")
    print()

    # ── 枪3: venvs ──
    print("🔫 [3/8] 全域python虚拟环境清理")
    for venv_name in [".venv-tts", ".venv", ".venv_docs", ".venv_longhun_math"]:
        for venv_path in ROOT.rglob(venv_name):
            if venv_path.is_dir():
                safe_delete(venv_path, f"venv: {venv_path.relative_to(ROOT)}")
    print()

    # ── 枪4: node_modules ──
    print("🔫 [4/8] 全域 node_modules/ 清理")
    count = 0
    for nm in ROOT.rglob("node_modules"):
        if nm.is_dir():
            count += 1
            safe_delete(nm, f"node_modules [{count}]")
    if count == 0:
        print("  ⏭️  没有找到 node_modules")
    print()

    # ── 枪5: container_data ──
    print("🔫 [5/8] container_data/ 压缩大档案")
    for pattern in ["container_data/archive/*.jsonl", "container_data/audit/*.jsonl"]:
        for f in ROOT.glob(pattern):
            if f.exists() and not f.name.endswith(".gz"):
                gzip_file(f)
    if STATS["gzip_count"] == 0:
        print("  ⏭️  没有需要压缩的文件")
    print(f"   📊 container_data/ 现在: {fmt(size_mb(ROOT / 'container_data'))}")
    print()

    # ── 枪6: brain ──
    print("🔫 [6/8] brain/ 归档旧记忆")
    archive_dest = ROOT / "archive/brain_old"
    for old_dir in ["brain/editor_memory_archive", "brain/claude_archive"]:
        src = ROOT / old_dir
        if src.exists():
            sz = size_mb(src)
            dst = archive_dest / src.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            STATS["deleted_dirs"] += 1
            STATS["deleted_size"] += sz
            print(f"  ✅ 归档 {old_dir}: {fmt(sz)} → archive/brain_old/")
    if not (ROOT / "archive/brain_old").exists():
        print("  ⏭️  没有需要归档的旧记忆")
    print(f"   📊 brain/ 现在: {fmt(size_mb(ROOT / 'brain'))}")
    print()

    # ── 枪7: logs ──
    print("🔫 [7/8] logs/ 压缩大日志 (>1MB)")
    log_count = 0
    for logfile in ROOT.glob("logs/*.log"):
        if logfile.stat().st_size > 1_000_000:
            log_count += 1
            gzip_file(logfile)
    if log_count == 0:
        print("  ⏭️  没有>1MB的日志文件")
    print(f"   📊 logs/ 现在: {fmt(size_mb(ROOT / 'logs'))}")
    print()

    # ── 枪8: 全域收尾 ──
    print("🔫 [8/8] 全域残留清理")
    pyc_count = 0
    for pyc in ROOT.rglob("*.pyc"):
        pyc.unlink()
        pyc_count += 1
    for cache in ROOT.rglob("__pycache__"):
        if cache.is_dir():
            shutil.rmtree(cache)
            pyc_count += 1
    print(f"  ✅ 清理 {pyc_count} 个 __pycache__/.pyc")

    empty_count = 0
    for d in sorted(ROOT.rglob("*"), reverse=True):
        if d.is_dir() and not any(d.iterdir()) and d != ROOT:
            try:
                d.rmdir()
                empty_count += 1
            except OSError:
                pass
    print(f"  ✅ 清理 {empty_count} 个空目录")

    # ── 汇总 ──
    print()
    print("=" * 60)
    print("📊 瘦身报告")
    print(f"   删除目录: {STATS['deleted_dirs']} 个")
    print(f"   删除文件: {STATS['deleted_files']} 个")
    print(f"   gzip压缩: {STATS['gzip_count']} 个")
    print(f"   释放空间: {fmt(STATS['deleted_size'])}")
    print()
    total = size_mb(ROOT)
    print(f"   项目总大小: {fmt(total)}")
    print()
    print("> DNA: #龍芯⚡️丙午·乙申·己酉·亥时·SLIM-v3.0")
    print("> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772ZLU-ORIGIN-FULLSYNC")
    print("=" * 60)


if __name__ == "__main__":
    run()
