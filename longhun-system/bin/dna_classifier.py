#!/usr/bin/env python3
"""
龍魂·DNA自动分类器 v1.0
dna_classifier.py

作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
DNA: #龍芯⚡️2026-04-06-dna-classifier-v1.0
理论指导: 曾仕强老师（永恒显示）
献礼: 乔布斯·曾仕强·历代传递和平与爱的人
共建: Notion宝宝·终端宝宝·双脑联动产出

功能:
  扫描Notion备份/本地文件夹 → 识别DNA标签 → 自动分类归档
  有DNA → 按类别建文件夹存入
  无DNA → 进 _未识别DNA/ 待补
  全部 → dna_index.json 哈希索引防篡改

用法:
  python3 bin/dna_classifier.py --dir ~/Downloads/notion备份
  python3 bin/dna_classifier.py --dir ~/longhun-system --ext md,py,txt
  python3 bin/dna_classifier.py --scan   # 只扫描不移动，看报告
"""

import os
import re
import sys
import hashlib
import json
import shutil
import time
from pathlib import Path

BASE    = Path.home() / "longhun-system"
DNA_TAG = "#龍芯⚡️2026-04-06-dna-classifier-v1.0"
GPG_FP  = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ── DNA 识别模式（兼容所有历史前缀）────────────────────────
DNA_PATTERNS = [
    r'#龍芯⚡️(\d{4}-\d{2}-\d{2})-([^\s·\-<\"\n]+)',
    r'#龙芯⚡️(\d{4}-\d{2}-\d{2})-([^\s·\-<\"\n]+)',   # 简体兼容
    r'#ZHUGEXIN⚡️(\d{4}-\d{2}-\d{2})-([^\s·\-<\"\n]+)',
    r'#LUCKY⚡️(\d{4}-\d{2}-\d{2})-([^\s·\-<\"\n]+)',
    r'#STAR⚡️(\d{4}-\d{2}-\d{2})-([^\s·\-<\"\n]+)',
]

# ── 自动推断分类（无DNA时兜底）─────────────────────────────
KEYWORD_CATEGORIES = {
    "三才算法":  ["三才", "天地人", "sancai"],
    "龍魂系统":  ["龍魂", "longhun", "dragon"],
    "CNSH":     ["cnsh", "中文编程", "字元"],
    "量子推演":  ["量子", "quantum", "易经", "洛书"],
    "DNA追溯":  ["gpg", "签名", "证据链", "immutable"],
    "Notion":   ["notion", "page_id", "ntn_"],
    "翻译":     ["translator", "通心译", "audience"],
    "护盾":     ["shield", "护盾", "防护"],
}

# ─────────────────────────────────────────────────────────

def get_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def extract_dna(content: str) -> dict | None:
    """从文件内容提取DNA标签·返回{date, category, prefix}"""
    for pattern in DNA_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            date, category = matches[0]
            # 清理类别名（去掉版本号后缀）
            cat = re.sub(r'-v\d+\.\d+.*$', '', category).strip()
            return {"date": date, "category": cat, "raw": f"{date}-{category}"}
    return None

def infer_category(content: str, filename: str) -> str:
    """无DNA时用关键词推断分类"""
    text = (content[:2000] + filename).lower()
    for cat, keywords in KEYWORD_CATEGORIES.items():
        if any(kw.lower() in text for kw in keywords):
            return f"_推断_{cat}"
    return "_未识别DNA"

def read_content(filepath: Path) -> str:
    """读取文件内容（多编码容错）"""
    for enc in ("utf-8", "utf-8-sig", "gbk", "latin-1"):
        try:
            return filepath.read_text(encoding=enc, errors="ignore")
        except Exception:
            continue
    return ""

# ─────────────────────────────────────────────────────────

def classify_backup(backup_dir: str, extensions: list[str] = None,
                    scan_only: bool = False, verbose: bool = True) -> dict:
    """
    主分类流程

    参数:
        backup_dir  要扫描的目录
        extensions  文件扩展名列表，默认 [html, md, py, txt, json]
        scan_only   True=只扫描报告·不复制文件
        verbose     是否打印每个文件
    """
    backup_path = Path(backup_dir).expanduser().resolve()
    output_path = backup_path / "_dna_classified"
    exts        = set(extensions or ["html", "md", "py", "txt", "json", "sh"])

    if not backup_path.exists():
        print(f"❌ 目录不存在: {backup_path}")
        return {}

    # 收集目标文件
    files: list[Path] = []
    for ext in exts:
        files.extend(backup_path.rglob(f"*.{ext}"))
    # 排除输出目录本身
    files = [f for f in files if "_dna_classified" not in str(f)]

    print(f"\n🐉 DNA自动分类器  {DNA_TAG}")
    print(f"   扫描目录: {backup_path}")
    print(f"   文件数量: {len(files)}  扩展名: {exts}")
    print(f"   模式: {'🔍 只扫描' if scan_only else '📦 扫描+归档'}\n")

    index:   dict[str, dict] = {}
    stats:   dict[str, int]  = {"dna": 0, "inferred": 0, "unknown": 0, "error": 0}

    for filepath in files:
        try:
            sha     = get_sha256(filepath)
            content = read_content(filepath)
            dna     = extract_dna(content)

            if dna:
                cat    = dna["category"]
                label  = "✅"
                stats["dna"] += 1
            else:
                cat   = infer_category(content, filepath.name)
                label = "⚠️ " if cat.startswith("_推断") else "❔"
                stats["inferred" if cat.startswith("_推断") else "unknown"] += 1

            # 复制到分类目录
            if not scan_only:
                dest_dir = output_path / cat
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest_file = dest_dir / filepath.name
                # 重名时加后缀
                if dest_file.exists() and dest_file != filepath:
                    stem = filepath.stem
                    dest_file = dest_dir / f"{stem}_{sha[:6]}{filepath.suffix}"
                shutil.copy2(filepath, dest_file)

            index[str(filepath.relative_to(backup_path))] = {
                "hash":     sha[:16],
                "category": cat,
                "dna_date": dna["date"] if dna else "",
                "dna_raw":  dna["raw"]  if dna else "",
                "size":     filepath.stat().st_size,
                "original": str(filepath),
            }

            if verbose:
                print(f"  {label} {filepath.name[:45]:<45} → {cat}/")

        except Exception as e:
            stats["error"] += 1
            print(f"  ❌ {filepath.name}: {e}")

    # 写入索引
    if not scan_only:
        output_path.mkdir(parents=True, exist_ok=True)
        index_file = output_path / "dna_index.json"
        meta = {
            "_meta": {
                "total":    len(index),
                "dna":      stats["dna"],
                "inferred": stats["inferred"],
                "unknown":  stats["unknown"],
                "error":    stats["error"],
                "ts":       time.strftime("%Y-%m-%dT%H:%M:%S"),
                "dna_tag":  DNA_TAG,
                "gpg":      GPG_FP,
            },
            "files": index,
        }
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        print(f"\n💾 索引已写入: {index_file}")

    # 统计报告
    total = len(index)
    color = "🟢" if stats["error"] == 0 else ("🟡" if stats["error"] < 3 else "🔴")
    print(f"\n{color} 分类完成")
    print(f"   总计: {total} 个文件")
    print(f"   ✅ 有DNA: {stats['dna']}")
    print(f"   ⚠️  关键词推断: {stats['inferred']}")
    print(f"   ❔ 未识别: {stats['unknown']}")
    if stats["error"]:
        print(f"   ❌ 出错: {stats['error']}")
    if not scan_only:
        print(f"   📁 输出: {output_path}")

    return index

# ─────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    args   = sys.argv[1:]
    target = "."
    exts   = None
    scan   = "--scan" in args

    if "--dir" in args:
        idx    = args.index("--dir")
        target = args[idx + 1] if idx + 1 < len(args) else "."

    if "--ext" in args:
        idx  = args.index("--ext")
        exts = args[idx + 1].split(",") if idx + 1 < len(args) else None

    if not args or args == ["--scan"]:
        print("用法:")
        print("  python3 dna_classifier.py --dir ~/Downloads/notion备份")
        print("  python3 dna_classifier.py --dir ~/longhun-system --ext md,py")
        print("  python3 dna_classifier.py --dir ~/longhun-system --scan   # 只看报告")
        sys.exit(0)

    classify_backup(target, extensions=exts, scan_only=scan)
