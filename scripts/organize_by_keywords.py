#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·关键字文件分类整理器
DNA: #龍芯⚡️丙午·癸未·丁未-ORGANIZE-BY-KEYWORDS-v1.0
功能：按用户自定义规则（关键字+扩展名）自动整理文件到分类目录
说明：本脚本本地运行，规则由用户自己配置，不联网、不上传。
"""

import argparse
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def load_config(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def is_excluded(file_path: Path, exclude_patterns: List[str]) -> bool:
    """检查文件路径是否匹配排除规则（支持正则）"""
    path_str = str(file_path)
    for pattern in exclude_patterns:
        try:
            if re.search(pattern, path_str, re.IGNORECASE):
                return True
        except re.error:
            if pattern in path_str:
                return True
    return False


def match_rule(file_path: Path, rule: dict) -> bool:
    """匹配单条规则：先匹配关键字，再匹配扩展名"""
    path_str_lower = str(file_path).lower()
    name_lower = file_path.name.lower()

    keywords = rule.get("keywords", [])
    exts = rule.get("exts", [])

    # 关键字匹配：路径或文件名包含任一关键字
    keyword_hit = False
    for kw in keywords:
        if kw.lower() in path_str_lower:
            keyword_hit = True
            break

    # 扩展名匹配
    ext_hit = False
    for ext in exts:
        ext_clean = ext.lower()
        if not ext_clean.startswith("."):
            ext_clean = "." + ext_clean
        if name_lower.endswith(ext_clean):
            ext_hit = True
            break

    # 规则逻辑：有关键字时，关键字命中即可；无关键字时，按扩展名匹配
    if keywords and exts:
        return keyword_hit or ext_hit
    if keywords:
        return keyword_hit
    if exts:
        return ext_hit
    return False


def decide_category(file_path: Path, rules: List[dict], default_name: str = "其他") -> str:
    """按规则顺序匹配，返回分类名"""
    for rule in rules:
        if match_rule(file_path, rule):
            return rule.get("name", "未命名")
    return default_name


def ensure_unique(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem = dest.stem
    suffix = dest.suffix
    counter = 1
    while True:
        new_dest = dest.with_name(f"{stem}_{counter:03d}{suffix}")
        if not new_dest.exists():
            return new_dest
        counter += 1


def _build_target_index(dest_dir: Path) -> set:
    """建立目标目录已有文件的 (相对分类/文件名, 大小) 索引，用于断点续传"""
    index = set()
    if not dest_dir.exists():
        return index
    for f in dest_dir.rglob("*"):
        if not f.is_file():
            continue
        try:
            rel = f.relative_to(dest_dir)
            index.add((str(rel), f.stat().st_size))
        except Exception:
            continue
    return index


def organize(config: dict, resume: bool = False) -> dict:
    source_dirs = [Path(p).expanduser().resolve() for p in config.get("source_dirs", [])]
    dest_dir = Path(config.get("dest_dir", "~/Desktop/整理后")).expanduser().resolve()
    rules = config.get("rules", [])
    exclude_patterns = config.get("exclude_paths", [])
    mode = config.get("mode", "copy")  # copy 或 move
    dry_run = config.get("dry_run", True)
    default_category = config.get("default_category", "其他")

    stats = {"scanned": 0, "organized": 0, "excluded": 0, "errors": 0, "skipped_existing": 0}
    plan: List[Dict] = []

    target_index = _build_target_index(dest_dir) if resume and not dry_run else set()

    for src in source_dirs:
        if not src.exists():
            print(f"⚠️ 源目录不存在，跳过: {src}")
            continue
        for file_path in src.rglob("*"):
            if not file_path.is_file():
                continue
            stats["scanned"] += 1

            if is_excluded(file_path, exclude_patterns):
                stats["excluded"] += 1
                continue

            category = decide_category(file_path, rules, default_category)
            target_dir = dest_dir / category
            target_path = target_dir / file_path.name

            # 断点续传：目标已有同名同大小文件则跳过
            if resume and not dry_run:
                rel_key = str((target_path.relative_to(dest_dir)))
                file_size = file_path.stat().st_size
                if (rel_key, file_size) in target_index:
                    stats["skipped_existing"] += 1
                    continue

            target_path = ensure_unique(target_path)

            plan.append({
                "src": file_path,
                "dst": target_path,
                "category": category,
            })

    # 执行
    if not dry_run:
        dest_dir.mkdir(parents=True, exist_ok=True)

    for item in plan:
        try:
            if dry_run:
                print(f"[DRY-RUN] [{item['category']}] {item['src']} -> {item['dst']}")
            else:
                item["dst"].parent.mkdir(parents=True, exist_ok=True)
                if mode == "move":
                    shutil.move(str(item["src"]), str(item["dst"]))
                else:
                    shutil.copy2(str(item["src"]), str(item["dst"]))
                print(f"✅ [{item['category']}] {item['dst'].name}")
            stats["organized"] += 1
        except Exception as e:
            stats["errors"] += 1
            print(f"❌ 错误: {item['src']} -> {e}")

    return stats


def main():
    parser = argparse.ArgumentParser(description="龍魂关键字文件分类整理器")
    parser.add_argument("--config", type=Path, required=True, help="规则配置文件路径")
    parser.add_argument("--execute", action="store_true", help="真正执行（默认 dry-run）")
    parser.add_argument("--resume", action="store_true", help="断点续传：跳过目标已存在的同名同大小文件")
    args = parser.parse_args()

    if not args.config.exists():
        print(f"❌ 配置文件不存在: {args.config}")
        sys.exit(1)

    config = load_config(args.config)
    if args.execute:
        config["dry_run"] = False
    else:
        config["dry_run"] = True

    mode = config.get("mode", "copy")
    dry_run = config["dry_run"]

    print("🐉 龍魂关键字文件分类整理器")
    print(f"   模式: {'预览' if dry_run else '执行'}")
    print(f"   操作: {'复制' if mode == 'copy' else '移动'}")
    print(f"   断点续传: {'是' if args.resume else '否'}")
    print(f"   目标: {Path(config.get('dest_dir', '~/Desktop/整理后')).expanduser().resolve()}")
    print()

    stats = organize(config, resume=args.resume)

    print(f"\n📊 统计")
    print(f"   扫描: {stats['scanned']}")
    print(f"   整理: {stats['organized']}")
    print(f"   跳过（已存在）: {stats['skipped_existing']}")
    print(f"   排除: {stats['excluded']}")
    print(f"   错误: {stats['errors']}")
    print(f"\n🧬 DNA: #龍芯⚡️丙午·癸未·丁未-ORGANIZE-BY-KEYWORDS-v1.0")


if __name__ == "__main__":
    main()
