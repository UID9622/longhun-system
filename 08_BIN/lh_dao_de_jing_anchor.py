#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·癸未·未时·䷚颐-DAO-DE-JING-ANCHOR-V0.1-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 父技能: .codebuddy/skills/longhun-dao-de-jing（补入口·entry_valid False→True）
# 说明: 道德经锚点检索 v0.1（MVP=原文锚检索·只读既有校验数据·不造原文）
#   数据源: 11_DATA/daodejing_deep_valid.jsonl（337 对话对·龍魂大白话解读 v5.0·deep_valid）
#   覆盖度(实机): 80/81 章·缺第 27 章 → 缺章如实提示·不补造（防空壳）
#   索引口径: 每个样例按全文中首现「第N章/出自第N章」归位（近似映射·如实注）
#   愿景字段「算法锚点/十维联动」不在本 v0.1 范围内 → 如实标（防空壳）
# 用法:
#   python3 bin/lh_dao_de_jing_anchor.py --chapter 5      # 第5章原文锚+解读
#   python3 bin/lh_dao_de_jing_anchor.py --search 上善若水  # 关键词检索(取前3)
#   python3 bin/lh_dao_de_jing_anchor.py --stats           # 覆盖统计
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "11_DATA" / "daodejing_deep_valid.jsonl"

CH_RE = re.compile(r"第\s*(\d{1,2})\s*章|出自第\s*(\d{1,2})")


def _extract_ch(text):
    for m in CH_RE.finditer(text):
        n = int(m.group(1) or m.group(2))
        if 1 <= n <= 81:
            return n
    return None


def _clean(s):
    return re.sub(r"\s+", " ", s).strip()


def load_index():
    """{chapter: [{'quote':..,'excerpt':..,'n':行数}]}·每样例归首现章(近似)"""
    idx = {}
    orphan = 0
    if not DATA.exists():
        print(f"❌ 数据缺失: {DATA}")
        sys.exit(1)
    for line_no, line in enumerate(DATA.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        msgs = obj.get("messages", []) or []
        if not msgs:
            continue
        user_buf, asst_buf = [], []
        for m in msgs:
            c = _clean(m.get("content", ""))
            if not c:
                continue
            if m.get("role") == "user":
                user_buf.append(c)
            elif m.get("role") == "assistant":
                asst_buf.append(c)
        all_text = " ".join(user_buf + asst_buf)
        ch = _extract_ch(all_text)
        if not ch:
            orphan += 1
            continue
        quote = user_buf[0][:120] if user_buf else all_text[:120]
        excerpt = asst_buf[0][:260] if asst_buf else ""
        idx.setdefault(ch, []).append(
            {"quote": quote, "excerpt": excerpt, "src": line_no}
        )
    return idx, orphan


def cmd_stats(idx, orphan):
    covered = sorted(idx.keys())
    missing = [c for c in range(1, 82) if c not in idx]
    total = sum(len(v) for v in idx.values())
    print(f"道德经锚索引 v0.1 · 数据 {DATA.name}")
    print(f"总样例(归位): {total} · 覆盖章 {len(covered)}/81 · 无章孤儿 {orphan}")
    print(f"缺章: {missing}")
    print("索引口径: 每样例按首现章号归位(近似映射) · 解读均来自既有 deep_valid 数据(非本引擎生成·不造原文)")


def cmd_chapter(idx, ch):
    rows = idx.get(ch)
    print(f"《道德经》第 {ch} 章 锚点检索")
    if not rows:
        print(f"   ⚠️ 第 {ch} 章无解读样例(数据缺口·如实标·不补造)")
        return
    for r in rows[:2]:
        print(f"   ── 样例(数据第{r['src']}行) ──")
        print(f"   原文锚: {r['quote']}")
        if r["excerpt"]:
            print(f"   龍魂解读(截断260字): {r['excerpt']}")
    print(f"   (该章共 {len(rows)} 条样例)")


def cmd_search(idx, kw):
    hits = []
    for ch, rows in idx.items():
        for r in rows:
            if kw in r["quote"] or kw in r["excerpt"]:
                hits.append((ch, r))
    print(f"检索「{kw}」· 命中 {len(hits)} 条(取前3)")
    for ch, r in hits[:3]:
        print(f"   ── 第{ch}章(数据第{r['src']}行) ──")
        print(f"   {r['quote'][:90]}")
        if r["excerpt"]:
            print(f"   → {r['excerpt'][:150]}")
    if not hits:
        print("   ⚠️ 无命中·换关键词或换数据源(本索引只覆盖既有 337 样例)")


def main():
    ap = argparse.ArgumentParser(description="龍魂·道德经锚点检索 v0.1(只读既有校验数据·不造原文)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--chapter", type=int, help="按章号 1-81 锚点检索")
    g.add_argument("--search", type=str, help="关键词/引文片段检索")
    g.add_argument("--stats", action="store_true", help="覆盖统计")
    args = ap.parse_args()
    idx, orphan = load_index()
    if args.stats:
        cmd_stats(idx, orphan)
    elif args.chapter:
        if not 1 <= args.chapter <= 81:
            print("章号须 1-81")
            sys.exit(1)
        cmd_chapter(idx, args.chapter)
    elif args.search:
        cmd_search(idx, args.search)
    else:
        ap.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
