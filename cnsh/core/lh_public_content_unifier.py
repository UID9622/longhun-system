#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂公开内容统一器
DNA: #龍芯⚡️2026-06-29-PUBLIC-CONTENT-UNIFIER-v1.0

把设备上对外公开的内容（README、文档、网页、示例脚本）统一成 CNSH 语法规范：
- 龍 字统一为繁体
- DNA 格式前缀统一为 #龍芯⚡️
- 配置键统一为 CNSH 中文键（可选）

用法：
    python3 public_content_unifier.py 扫描 <目录>
    python3 public_content_unifier.py 规范化 <目录> --output <输出目录>
"""
import argparse
import json
from pathlib import Path
from typing import List

from cnsh_unified import 公开内容, 文字规范, DNA工具


PUBLIC_EXTENSIONS = {".md", ".txt", ".json", ".html", ".css", ".js", ".cnsh", ".yaml", ".yml"}


def 扫描公开目录(目录: Path) -> List[dict]:
    结果 = []
    for 路径 in Path(目录).rglob("*"):
        if 路径.is_file() and 路径.suffix.lower() in PUBLIC_EXTENSIONS:
            结果.append(公开内容.扫描文件(路径))
    return 结果


def 打印扫描报告(结果: List[dict]):
    问题文件 = [r for r in 结果 if r["简化字"] or r["dna数量"] > 0]
    print(f"\n📂 扫描文件数: {len(结果)}")
    print(f"⚠️ 需要关注的文件: {len(问题文件)}\n")
    for r in 问题文件[:20]:
        标记 = []
        if r["简化字"]:
            标记.append(f"简化字:{r['简化字']}")
        if r["dna数量"] > 0:
            标记.append(f"DNA:{r['dna数量']}条")
        print(f"  • {r['路径']}  {' / '.join(标记)}")
    if len(问题文件) > 20:
        print(f"  ... 还有 {len(问题文件) - 20} 个文件")
    print()


def 规范化目录(输入目录: Path, 输出目录: Path):
    输出目录 = Path(输出目录)
    输出目录.mkdir(parents=True, exist_ok=True)
    计数 = 0
    for 路径 in Path(输入目录).rglob("*"):
        if 路径.is_file() and 路径.suffix.lower() in PUBLIC_EXTENSIONS:
            相对 = 路径.relative_to(输入目录)
            目标 = 输出目录 / 相对
            目标.parent.mkdir(parents=True, exist_ok=True)
            公开内容.规范化文件(路径, 目标)
            计数 += 1
    print(f"\n✅ 已规范化 {计数} 个文件到: {输出目录}\n")


def 主函数():
    parser = argparse.ArgumentParser(description="龍魂公开内容统一器")
    subparsers = parser.add_subparsers(dest="命令")

    scan_parser = subparsers.add_parser("扫描", help="扫描目录中的公开内容问题")
    scan_parser.add_argument("目录", help="要扫描的目录")

    norm_parser = subparsers.add_parser("规范化", help="规范化目录并输出到新位置")
    norm_parser.add_argument("目录", help="要规范化的目录")
    norm_parser.add_argument("--output", "-o", required=True, help="输出目录")

    args = parser.parse_args()
    if not args.命令:
        parser.print_help()
        return

    if args.命令 == "扫描":
        结果 = 扫描公开目录(Path(args.目录))
        打印扫描报告(结果)
    elif args.命令 == "规范化":
        规范化目录(Path(args.目录), Path(args.output))


if __name__ == "__main__":
    主函数()
