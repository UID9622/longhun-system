#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 文章同步到桌面「文章」文件夹 v1.0
DNA: #龍芯⚡️2026-07-04-ARTICLE-SYNC-TO-DESKTOP-v1.0

功能：
- 把 longhun-system 里新写的文章，同步到桌面「文章」文件夹，方便查找。
- 自动按日期前缀命名，支持分类目录（原文 / CSDN发布版 / 微信公众号发布版）。
- 自动更新「文章索引.md」。

用法：
    python3 sync_article_to_desktop.py \
        --source ~/longhun-system/docs/华为_eNSP_安装完全指南_人民标准版_v3.0.md \
        --category 原文

    python3 sync_article_to_desktop.py \
        --source ~/longhun-system/outputs/csdn_华为_eNSP_安装完全指南_人民标准版_v3.0.md \
        --category CSDN发布版
"""

import argparse
import re
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

DNA = "#龍芯⚡️2026-07-04-ARTICLE-SYNC-TO-DESKTOP-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def extract_title(file_path: Path) -> str:
    """尝试从 Markdown 第一行提取标题。"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    return line.lstrip("# ").strip()
    except Exception:
        pass
    return file_path.stem


def decide_dest_filename(source: Path) -> str:
    """
    如果文件名已有 YYYY-MM-DD- 或 YYYY-MM-DD_ 前缀，直接保留；
    否则按文件修改时间加上日期前缀。
    """
    name = source.name
    if re.match(r"^\d{4}-\d{2}-\d{2}[-_]", name):
        return name
    mtime = datetime.fromtimestamp(source.stat().st_mtime, tz=timezone(timedelta(hours=8)))
    date_prefix = mtime.strftime("%Y-%m-%d-")
    return date_prefix + name


def normalize_dest_filename(source: Path, category: str) -> str:
    """
    统一命名格式：
    - 原文：YYYY-MM-DD-标题.md
    - CSDN发布版：YYYY-MM-DD-标题-CSDN发布版.md
    - 微信公众号发布版：YYYY-MM-DD-标题-微信公众号发布版.md
    """
    name = decide_dest_filename(source)
    stem = Path(name).stem
    suffix = Path(name).suffix

    if category == "CSDN发布版":
        # 去掉常见前缀/后缀
        stem = re.sub(r"^csdn_?", "", stem, flags=re.IGNORECASE)
        stem = re.sub(r"-?CSDN发布版$", "", stem, flags=re.IGNORECASE)
        stem = re.sub(r"_?CSDN$", "", stem, flags=re.IGNORECASE)
        return f"{stem}-CSDN发布版{suffix}"

    if category == "微信公众号发布版":
        stem = re.sub(r"^(wechat|wx)_?", "", stem, flags=re.IGNORECASE)
        stem = re.sub(r"-?微信公众号发布版$", "", stem, flags=re.IGNORECASE)
        return f"{stem}-微信公众号发布版{suffix}"

    return name


def update_index(article_root: Path, source: Path, dest: Path, category: str):
    index_path = article_root / "文章索引.md"
    title = extract_title(dest)
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")

    # 索引链接：原文直接写文件名，其他分类写「分类/文件名」
    if dest.parent == article_root:
        link = dest.name
    else:
        link = f"{dest.parent.name}/{dest.name}"

    entry = f"| {now} | {category} | [{title}]({link}) | `{source}` |\n"

    if not index_path.exists():
        header = """# 龍魂文章索引

> 本索引由 `sync_article_to_desktop.py` 自动维护。
> 桌面「文章」文件夹是龍魂系统文章的本地快捷入口，原文仍保留在 longhun-system 中。

| 同步时间 | 分类 | 文章标题 | 系统原文路径 |
|---------|------|---------|-------------|
"""
        index_path.write_text(header, encoding="utf-8")

    with open(index_path, "a", encoding="utf-8") as f:
        f.write(entry)


def main():
    parser = argparse.ArgumentParser(description="龍魂 · 文章同步到桌面「文章」文件夹")
    parser.add_argument("--source", required=True, help="源文章路径（Markdown）")
    parser.add_argument(
        "--target-dir",
        default="~/Desktop/文章",
        help="桌面文章文件夹路径（默认：~/Desktop/文章）",
    )
    parser.add_argument(
        "--category",
        default="原文",
        choices=["原文", "CSDN发布版", "微信公众号发布版"],
        help="文章分类子目录",
    )
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    article_root = Path(args.target_dir).expanduser().resolve()
    # 「原文」默认放在文章根目录，其他分类放在对应子文件夹
    if args.category == "原文":
        category_dir = article_root
    else:
        category_dir = article_root / args.category
        category_dir.mkdir(parents=True, exist_ok=True)

    dest_filename = normalize_dest_filename(source, args.category)
    dest = category_dir / dest_filename

    shutil.copy2(source, dest)
    update_index(article_root, source, dest, args.category)

    print("=" * 60)
    print("龍魂 · 文章同步完成")
    print("=" * 60)
    print(f"源文件: {source}")
    print(f"目标:   {dest}")
    print(f"分类:   {args.category}")
    print(f"索引:   {article_root / '文章索引.md'}")
    print(f"DNA:    {DNA}")
    print(f"CONFIRM:{CONFIRM}")
    print("=" * 60)


if __name__ == "__main__":
    main()
