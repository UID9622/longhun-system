#!/usr/bin/env python3
# DNA: #龍芯⚡️2026-08-30-KB-INGEST-CORE-v1.1-ANTENNA-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · 核心域知识入库 v1.1（天线八门训练数据 → 平衡核心域配额）
──────────────────────────────────────────────
源: 01_protocols/ANTENNA-8GATE/training_data/training_data.jsonl (69条·八卦路由)
格式: instruction/input/output → messages 训练格式
链路: L1 合规(自有) → L3 三保闸 → L4 ASI 七闸 → 入库 + md 知识卡

v1.1 工程审查修复(2026-08-30 P04鲁班 · 吸收 P00/P15 意见):
  - 幂等键 → 内容指纹；DNA 日期动态化(不再硬编码 2026-08-30)
  - id 全局唯一(内容哈希)·md 卡复用 to_md_card(role 按字段提取·无下标魔法数字)
  - md 卡只写 feed_result['passed'](与 train_merged 同步)·dry-run 不落盘 11_DATA
  - INDEX 全量重建(八卦路由纳入) · 新增 --category 入参
  - 路径基于 __file__ 推导项目根

用法:
    python3 08_BIN/lh_kb_ingest_core.py [--dry-run] [--category growth]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

_BIN = str(Path(__file__).resolve().parent)
if _BIN not in sys.path:
    sys.path.insert(0, _BIN)

from lh_kb_common import (SYSTEM_PROMPT, gen_dna, gen_id, now_utc, quota_report,
                          read_jsonl, rebuild_index)

_ROOT = Path(_BIN).parent

SRC = _ROOT / "01_protocols" / "ANTENNA-8GATE" / "training_data" / "training_data.jsonl"
KB_DOMAIN = "八卦路由"
KB_ROOT = _ROOT / "11_DATA" / "knowledge_base"
TRAIN_MERGED = _ROOT / "11_DATA" / "bootstrap" / "train_merged.jsonl"


def main() -> None:
    p = argparse.ArgumentParser(prog="lh_kb_ingest_core", description="核心域知识入库 v1.1")
    p.add_argument("--dry-run", action="store_true", help="只验证不入库(不写 11_DATA)")
    p.add_argument("--category", default="growth", help="ASI 七闸类别")
    args = p.parse_args()

    recs = []
    seen = set()
    for d in read_jsonl(SRC):
        instr = (d.get("instruction", "") + (d.get("input") or "")).strip()
        out = d.get("output", "").strip()
        if not instr or not out:
            continue
        fp = hashlib.sha256((instr + out).encode()).hexdigest()
        if fp in seen:
            continue
        seen.add(fp)
        meta = {
            "source": "antenna-8gate-training",
            "source_url": f"file://{SRC}",
            "license": "MulanPSL-2.0",
            "dna": gen_dna(instr + out, "CORE"),
            "domain": KB_DOMAIN,
            "kb_ts": now_utc(),
        }
        recs.append({
            "id": gen_id("core", instr + out),
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": instr},
                {"role": "assistant", "content": out},
            ],
            "metadata": meta,
        })

    print(f"⏳ 天线八门核心数据: 收集 {len(recs)} 条")
    if not recs:
        print("  🔴 无数据，终止")
        sys.exit(1)

    from lh_triple_guard import check
    result = check(recs)
    passed = result["passed"]
    print(f"✅ L3 三保闸: 通过 {len(passed)} / {result['total']} · 拒绝 {len(result['rejected'])}")
    for r in result["rejected"][:5]:
        print(f"    🔴 {r.get('id')}: {r['reason']}")
    if not passed:
        print("  🔴 无通过样本，终止")
        sys.exit(1)

    from lh_asi_feed import feed
    feed_result = feed(passed, category=args.category, dry_run=args.dry_run)
    print(f"✅ L4 ASI 七闸: {feed_result['status']} · passed={feed_result.get('passed_cnt')} held={feed_result.get('held_cnt')} · 幂等跳过={feed_result.get('dedup_skipped', 0)}")
    if feed_result["status"] != "🟢":
        print("  🔴 七闸未过，终止")
        sys.exit(2)

    # md 知识卡：只写 feed_result['passed']·dry-run 不落盘
    if args.dry_run:
        print(f"  [dry-run] 将写入 {len(feed_result['passed'])} 张知识卡 → {KB_ROOT}/{KB_DOMAIN}/")
    else:
        from lh_kb_ingest import to_md_card
        dom_dir = KB_ROOT / KB_DOMAIN
        dom_dir.mkdir(parents=True, exist_ok=True)
        for r in feed_result["passed"]:
            to_md_card(r, dom_dir / f"{r['id']}.md")
        print(f"✅ md 知识库: 写入 {len(feed_result['passed'])} 条 → {dom_dir}")
        rebuild_index(KB_ROOT)

    quota_report(TRAIN_MERGED)


if __name__ == "__main__":
    main()
