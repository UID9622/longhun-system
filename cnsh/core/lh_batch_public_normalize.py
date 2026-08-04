#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂公开内容批量规范化
DNA: #龍芯⚡️2026-06-29-LONGHUN-BATCH-PUBLIC-NORMALIZE-v1.0

扫描全机公开内容，把需要规范化的文件先备份再原地修改：
- 简化字 '龍' → 繁体 '龍'
- DNA 前缀统一为 #龍芯⚡️

用法：
    python3 batch_public_normalize.py <目录>
"""
import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from cnsh_unified import 公开内容, 文字规范, DNA工具

PUBLIC_EXTENSIONS = {".md", ".txt", ".json", ".html", ".css", ".js", ".cnsh", ".yaml", ".yml", ".xml", ".toml"}


def 批量规范化(目标目录: Path, dry_run: bool = False):
    目标目录 = Path(目标目录)
    备份根 = Path.home() / ".龍魂" / "backups" / "public-content-unify" / datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    if not dry_run:
        备份根.mkdir(parents=True, exist_ok=True)

    计数 = 0
    改动 = 0
    跳过 = 0
    失败 = 0

    print(f"\n🐉 批量规范化公开内容\n")
    print(f"目标目录: {目标目录}")
    print(f"模式: {'预览' if dry_run else '实际执行'}")
    print(f"备份目录: {备份根}\n")

    for 路径 in 目标目录.rglob("*"):
        if not 路径.is_file():
            continue
        if 路径.suffix.lower() not in PUBLIC_EXTENSIONS:
            continue
        计数 += 1

        try:
            文本 = 路径.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            失败 += 1
            print(f"❌ 读取失败 {路径}: {e}")
            continue

        新文本 = DNA工具.规范化(文字规范.繁体龍(文本))
        if 新文本 == 文本:
            跳过 += 1
            continue

        if dry_run:
            改动 += 1
            if 改动 <= 20:
                print(f"[预览] 将规范化: {路径}")
            continue

        try:
            # 备份原文件
            try:
                相对 = 路径.relative_to(目标目录)
            except ValueError:
                相对 = 路径.relative_to(Path("/"))
            备份路径 = 备份根 / 相对
            备份路径.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(路径, 备份路径)

            # 原地写入
            路径.write_text(新文本, encoding="utf-8")
            改动 += 1
            if 改动 <= 20:
                print(f"✅ 已规范化: {路径}")
        except Exception as e:
            失败 += 1
            print(f"❌ 失败 {路径}: {e}")

    print(f"\n扫描文件: {计数}")
    print(f"改动: {改动}，跳过: {跳过}，失败: {失败}\n")


def 主函数():
    parser = argparse.ArgumentParser(description="龍魂公开内容批量规范化")
    parser.add_argument("目录", help="要规范化的根目录")
    parser.add_argument("--dry-run", action="store_true", help="仅预览不修改")
    args = parser.parse_args()
    批量规范化(Path(args.目录), dry_run=args.dry_run)


if __name__ == "__main__":
    主函数()
