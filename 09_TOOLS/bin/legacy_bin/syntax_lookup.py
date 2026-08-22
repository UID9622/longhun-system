#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂·语法库查询工具 v1.0
DNA: #龍芯⚡️丙午·乙未·癸未·戊午·䷖剥-SYNTAX-LOOKUP-v1.0

用法:
  python3 bin/syntax_lookup.py "打印"              # 查单个中文关键字
  python3 bin/syntax_lookup.py "打印" --target py   # 只查Python映射
  python3 bin/syntax_lookup.py --list-categories    # 列出所有语法类别
  python3 bin/syntax_lookup.py --category 控制流     # 列出某类别所有关键字
  python3 bin/syntax_lookup.py --search "list"      # 模糊搜索
  python3 bin/syntax_lookup.py --targets            # 列出所有目标语言
"""
import json
import sys
from pathlib import Path
from typing import Any

DNA = "#龍芯⚡️丙午·乙未·癸未·戊午·䷖剥-SYNTAX-LOOKUP-v1.0"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LIB_PATH = PROJECT_ROOT / "03_compiler" / "mappings" / "syntax_library.json"

TARGET_NAMES = {
    "py": "Python", "c": "C", "cpp": "C++", "js": "JavaScript",
    "rs": "Rust", "swift": "Swift", "go": "Go", "java": "Java",
    "rb": "Ruby", "kt": "Kotlin", "bash": "Bash", "objc": "Objective-C",
    "css": "CSS", "html": "HTML", "sql": "SQL", "regex": "正则表达式",
    "md": "Markdown", "sh": "Shell", "docker": "Docker", "git": "Git"
}


def load_library() -> dict[str, Any]:
    with open(LIB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def find_entry(lib: dict[str, Any], cn_word: str) -> dict[str, Any] | None:
    for category, entries in lib["syntax"].items():
        for entry in entries:
            if entry["cn"] == cn_word:
                return entry
    return None


def lookup(cn_word: str, target: str | None = None):
    lib = load_library()
    entry = find_entry(lib, cn_word)
    if not entry:
        print(f"❌ 未找到关键字: {cn_word}")
        # 模糊搜索
        matches = fuzzy_search(lib, cn_word)
        if matches:
            print(f"\n🔍 你可能在找:")
            for m in matches[:5]:
                print(f"  · {m}")
        sys.exit(1)

    print(f"\n🐉 {entry['cn']}")
    if "note" in entry:
        print(f"   📝 {entry['note']}")
    print()

    if target:
        if target in entry:
            lang_name = TARGET_NAMES.get(target, target)
            print(f"   {lang_name:>15}: {entry[target]}")
        else:
            print(f"   ❌ 目标语言 '{target}' 不支持此关键字")
    else:
        # 显示所有映射
        shown = set()
        for key, value in entry.items():
            if key in ("cn", "en", "note"):
                continue
            if value == "—":
                continue
            lang_name = TARGET_NAMES.get(key, key)
            print(f"   {lang_name:>15}: {value}")
            shown.add(key)

        # 显示不支持的语言
        not_supported = [k for k in entry if k not in ("cn", "en", "note") and k not in shown]
        if not_supported:
            print(f"\n   {'(不支持)':>15}: {', '.join(not_supported)}")


def fuzzy_search(lib: dict[str, Any], query: str) -> list[str]:
    results = []
    q = query.lower()
    for category, entries in lib["syntax"].items():
        for entry in entries:
            cn = entry["cn"]
            en_val = entry.get("en", "")
            if q in cn or q in str(en_val).lower():
                results.append(f"[{category}] {cn}")
    return results


def list_categories(lib: dict[str, Any]):
    print("\n📂 语法类别 (25类):\n")
    for i, cat in enumerate(lib["syntax_categories"]["_order"], 1):
        count = len(lib["syntax"].get(cat, []))
        print(f"   {i:2}. {cat} ({count}条)")


def list_category(lib: dict[str, Any], cat_name: str):
    entries = lib["syntax"].get(cat_name, [])
    if not entries:
        print(f"❌ 未找到类别: {cat_name}")
        print(f"   可用类别: {', '.join(lib['syntax_categories']['_order'])}")
        sys.exit(1)

    print(f"\n📂 {cat_name} ({len(entries)}条):\n")
    for e in entries:
        en_val = e.get("en", "")
        note = f" — {e['note']}" if "note" in e else ""
        print(f"   {e['cn']:<12} → {en_val}{note}")


def list_targets(lib: dict[str, Any]):
    print("\n🎯 支持的目标语言 (20种):\n")
    for key, info in lib["target_languages"].items():
        lang_name = TARGET_NAMES.get(key, info["name"])
        status = info["status"]
        ext = info["ext"]
        print(f"   {status} {lang_name:<18} ({key})  .{ext}")


def search(lib: dict[str, Any], query: str):
    results = fuzzy_search(lib, query)
    if not results:
        print(f"❌ 未找到匹配 '{query}' 的关键字")
        sys.exit(1)
    print(f"\n🔍 搜索 '{query}' — 找到 {len(results)} 条:\n")
    for r in results:
        print(f"   · {r}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    arg = sys.argv[1]
    lib = load_library()

    if arg == "--list-categories":
        list_categories(lib)
    elif arg == "--category":
        if len(sys.argv) < 3:
            print("用法: python3 bin/syntax_lookup.py --category <类别名>")
            sys.exit(1)
        list_category(lib, sys.argv[2])
    elif arg == "--targets":
        list_targets(lib)
    elif arg == "--search":
        if len(sys.argv) < 3:
            print("用法: python3 bin/syntax_lookup.py --search <关键词>")
            sys.exit(1)
        search(lib, sys.argv[2])
    else:
        target = None
        if len(sys.argv) >= 4 and sys.argv[2] == "--target":
            target = sys.argv[3]
        lookup(arg, target)


if __name__ == "__main__":
    main()
