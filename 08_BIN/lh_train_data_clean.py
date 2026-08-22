#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·甲子·庚午·䷙大畜-训练数据清洗-v1.0-7f3a
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·训练数据清洗引擎 v1.0
--------------------------------
背景: 量化 LoRA 训练 Best Val 2.2987，train loss 波动巨大(2.42→3.29)。
      根因 = 数据噪声: 6984 条中 502 条 <100字、52 条 >2000字、Top10 来源占 57%。
规则(UID9622 定):
  1. 过滤输出 <150 字 或 >1500 字 的样本
  2. 按来源去重，每个来源最多 100 条
  3. 长段落(>=600字且多段)按语义段落切分，切分段拼合到 150~800 字
  4. 重新生成 train/valid (95/5)
用法:
  python3 bin/lh_train_data_clean.py            # 清洗 docs/notion_full_export/data
  python3 bin/lh_train_data_clean.py --dry-run  # 只统计不写盘
"""
import argparse
import json
import random
import shutil
import sys
import time
from collections import Counter, OrderedDict
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT / "docs" / "notion_full_export" / "data"
TRAIN = DATA_DIR / "train.jsonl"
VALID = DATA_DIR / "valid.jsonl"
OUT_TRAIN = DATA_DIR / "train.jsonl"
OUT_VALID = DATA_DIR / "valid.jsonl"
BACKUP_DIR = DATA_DIR / "backup_clean_v1"

MIN_LEN, MAX_LEN = 150, 1500          # 规则1
MAX_PER_SOURCE = 100                   # 规则2
SPLIT_THRESHOLD = 600                  # >=600 且多段才切分（规则3）
SEG_MIN, SEG_MAX = 150, 800            # 切分段落目标长度区间
VALID_RATIO = 0.05                     # 规则4


def get_output(row: dict) -> str:
    msgs = row.get("messages") or []
    for m in reversed(msgs):
        if m.get("role") in ("assistant", "model"):
            return (m.get("content") or "").strip()
    return (msgs[-1].get("content") or "").strip() if msgs else ""


def get_input(row: dict) -> str:
    msgs = row.get("messages") or []
    parts = [m.get("content", "") for m in msgs[:-1] if m.get("role") in ("user", "system")]
    return "".join(parts)


def split_paragraphs(text: str):
    """按空行/换行切语义段，再按句号兜底，返回段落列表"""
    segs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if len(segs) < 2:
        segs = [p.strip() for p in text.split("\n") if p.strip()]
    if len(segs) < 2:
        # 单段长文: 按中文句号切成短句再合并
        sentences = [s for s in text.replace("。", "。\n").split("\n") if s.strip()]
        return sentences
    return segs


def merge_to_window(segs, lo=SEG_MIN, hi=SEG_MAX):
    """贪心拼合段落到 [lo, hi] 区间，太长丢弃"""
    merged = []
    buf = ""
    for s in segs:
        if len(buf) + len(s) <= hi:
            buf += s
        else:
            if len(buf) >= lo:
                merged.append(buf)
            # 单段超 hi 直接丢弃（信息密度低/截断风险）
            if len(s) > hi:
                buf = ""
            else:
                buf = s
    if buf and len(buf) >= lo:
        merged.append(buf)
    return merged


def clean_rows(rows):
    stats = Counter()
    kept = []
    for r in rows:
        out = get_output(r)
        n = len(out)
        src = r.get("source", "(空)")
        if n < MIN_LEN:
            stats["过滤:输出<150字"] += 1
            continue
        if n > MAX_LEN:
            stats["过滤:输出>1500字"] += 1
            continue
        stats["通过:主过滤"] += 1
        # 规则3: 长样本切分
        if n >= SPLIT_THRESHOLD:
            segs = split_paragraphs(out)
            if len(segs) >= 2:
                pieces = merge_to_window(segs)
                if len(pieces) >= 2:
                    stats["切分:长样本"] += 1
                    for i, p in enumerate(pieces):
                        nr = dict(r)
                        nr["messages"] = list(r.get("messages") or [])
                        # 替换最后一条 assistant 内容
                        for j in range(len(nr["messages"]) - 1, -1, -1):
                            if nr["messages"][j].get("role") in ("assistant", "model"):
                                nr["messages"][j] = dict(nr["messages"][j], content=p)
                                break
                        else:
                            nr["messages"].append({"role": "assistant", "content": p})
                        nr["_seg"] = f"{i + 1}/{len(pieces)}"
                        kept.append(nr)
                    continue
        kept.append(r)
    # 规则2: 每个来源最多 MAX_PER_SOURCE 条
    random.shuffle(kept)
    per_src = OrderedDict()
    for r in kept:
        src = r.get("source", "(空)")
        if per_src.get(src, 0) < MAX_PER_SOURCE:
            per_src[src] = per_src.get(src, 0) + 1
            stats["通过:来源cap"] += 1
    capped = []
    seen = Counter()
    for r in kept:
        src = r.get("source", "(空)")
        if seen[src] < MAX_PER_SOURCE:
            seen[src] += 1
            capped.append(r)
    stats["最终保留"] = len(capped)
    return capped, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    random.seed(args.seed)

    if not TRAIN.exists():
        print(f"[ERR] 找不到 {TRAIN}"); sys.exit(1)

    rows = []
    with open(TRAIN, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    vrows = []
    if VALID.exists():
        with open(VALID, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    vrows.append(json.loads(line))

    t0 = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] 清洗开始 | train={len(rows)} valid={len(vrows)}")
    print(f"  规则: 输出 {MIN_LEN}~{MAX_LEN}字 | 每来源≤{MAX_PER_SOURCE} | 长样本≥{SPLIT_THRESHOLD}字切分")

    clean_train, st = clean_rows(rows)
    clean_valid, sv = clean_rows(vrows)
    print(f"\n--- train 清洗统计 ({time.time()-t0:.1f}s) ---")
    for k, v in st.most_common():
        print(f"  {k}: {v}")
    print(f"\n--- valid 清洗统计 ---")
    for k, v in sv.most_common():
        print(f"  {k}: {v}")

    # 规则4: 合并重新划分 95/5
    all_rows = clean_train + clean_valid
    random.shuffle(all_rows)
    n_valid = max(1, int(len(all_rows) * VALID_RATIO))
    new_train, new_valid = all_rows[n_valid:], all_rows[:n_valid]
    src_cnt = Counter(r.get("source", "(空)") for r in new_train)
    print(f"\n--- 重新划分 ---")
    print(f"  train: {len(new_train)} 条 (来自 {len(src_cnt)} 来源)")
    print(f"  valid: {len(new_valid)} 条")
    print(f"  新 train Top5 来源:")
    for name, c in src_cnt.most_common(5):
        print(f"    {name[:60]}: {c}")

    if args.dry_run:
        print("\n[dry-run] 不写盘，以上为预览。")
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    for src in (TRAIN, VALID):
        if src.exists():
            dst = BACKUP_DIR / f"{src.name}.bak"
            shutil.copy2(src, dst)
    with open(OUT_TRAIN, "w", encoding="utf-8") as f:
        for r in new_train:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(OUT_VALID, "w", encoding="utf-8") as f:
        for r in new_valid:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\n✅ 已写入: {OUT_TRAIN} ({len(new_train)}行) / {OUT_VALID} ({len(new_valid)}行)")
    print(f"   原文件备份: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
