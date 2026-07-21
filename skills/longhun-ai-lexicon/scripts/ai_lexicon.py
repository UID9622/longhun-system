#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 行业话术 · 龍文语义映射词典查询工具
==========================================
DNA: #龍芯⚡️2026-06-29-LONGHUN-AI-LEXICON-CLI-v1.0

用法:
  python ai_lexicon.py search <关键词>     # 按英文/中文/CNSH 检索
  python ai_lexicon.py list [分类]         # 列出全部或某分类
  python ai_lexicon.py explain <术语>      # 打印单条详细解释
  python ai_lexicon.py random              # 随机抽一条学习
  python ai_lexicon.py stats               # 统计 hype 等级与分类
"""

import argparse
import json
import random
import sys
from pathlib import Path

DNA = "#龍芯⚡️2026-06-29-LONGHUN-AI-LEXICON-CLI-v1.0"
DICT_PATH = Path.home() / "longhun-system/knowledge/ai-buzzword-dictionary/ai_buzzword_dict.json"


def _load():
    if not DICT_PATH.exists():
        print(f"🔴 词典文件不存在: {DICT_PATH}")
        print("请先运行: python3 ~/longhun-system/cnsh-core/build_ai_lexicon.py")
        sys.exit(1)
    return json.loads(DICT_PATH.read_text(encoding="utf-8"))


def _print_entry(e, full=False):
    print(f"\n{'='*60}")
    print(f"  {e['term_en']}  ·  {e['term_cn']}  ·  {e['cnsh_name']}")
    print(f"  DNA: {e['dna']}")
    print(f"{'='*60}")
    print(f"  分类: {e['category']}")
    print(f"  Hype 等级: {e['hype_level']}/5  {e['hype_badge']}")
    print(f"  人话解释: {e['plain_explanation']}")
    print(f"  真实底座: {e['base_tech']}")
    print(f"  龍魂映射: {e['longwen_mapping']}")
    if full:
        print(f"  相关词: {', '.join(e['related_terms'])}")
        print(f"  例子: {e['example']}")


def cmd_search(args):
    entries = _load()
    kw = args.keyword.lower()
    results = [
        e for e in entries
        if kw in e["term_en"].lower()
        or kw in e["term_cn"].lower()
        or kw in e["cnsh_name"].lower()
        or any(kw in r.lower() for r in e["related_terms"])
    ]
    if not results:
        print(f"🔴 未找到与 '{args.keyword}' 相关的词条")
        return
    print(f"\n🟢 找到 {len(results)} 条相关词条:\n")
    for e in results:
        print(f"  {e['term_en']:24s} {e['term_cn']:18s} → {e['cnsh_name']}  [hype {e['hype_level']}/5]")
    if args.detail:
        for e in results:
            _print_entry(e, full=True)


def cmd_list(args):
    entries = _load()
    if args.category:
        entries = [e for e in entries if e["category"] == args.category]
    if not entries:
        print(f"🔴 分类 '{args.category}' 无词条")
        return
    print(f"\n🟢 共 {len(entries)} 条词条:\n")
    for e in entries:
        print(f"  [{e['category']}] {e['term_en']:24s} {e['term_cn']:18s} → {e['cnsh_name']}")


def cmd_explain(args):
    entries = _load()
    kw = args.term.lower()
    for e in entries:
        if e["term_en"].lower() == kw or e["term_cn"].lower() == kw or e["cnsh_name"].lower() == kw:
            _print_entry(e, full=True)
            return
    print(f"🔴 未找到 '{args.term}'，尝试用 search 模糊查找")


def cmd_random(args):
    entries = _load()
    e = random.choice(entries)
    _print_entry(e, full=True)


def cmd_stats(args):
    entries = _load()
    print(f"\n{'='*60}")
    print("  AI 话术词典统计")
    print(f"{'='*60}")
    print(f"  总词条: {len(entries)}")
    cats = {}
    hype = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for e in entries:
        cats[e["category"]] = cats.get(e["category"], 0) + 1
        hype[e["hype_level"]] = hype.get(e["hype_level"], 0) + 1
    print("\n  分类分布:")
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"    {c}: {n}")
    print("\n  Hype 等级分布:")
    for level, n in sorted(hype.items()):
        bar = "🔥" * level + "░" * (5 - level)
        print(f"    {level}/5 {bar}: {n}")


def main():
    parser = argparse.ArgumentParser(description="AI 行业话术 · 龍文语义映射词典")
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="按关键词检索")
    p_search.add_argument("keyword")
    p_search.add_argument("--detail", action="store_true", help="显示详情")

    p_list = sub.add_parser("list", help="列出词条")
    p_list.add_argument("category", nargs="?", help="按分类过滤")

    p_explain = sub.add_parser("explain", help="解释单个术语")
    p_explain.add_argument("term")

    sub.add_parser("random", help="随机抽一条")
    sub.add_parser("stats", help="统计")

    args = parser.parse_args()
    {
        "search": cmd_search,
        "list": cmd_list,
        "explain": cmd_explain,
        "random": cmd_random,
        "stats": cmd_stats,
    }[args.command](args)


if __name__ == "__main__":
    main()
