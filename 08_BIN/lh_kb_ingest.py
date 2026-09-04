#!/usr/bin/env python3
# DNA: #龍芯⚡️2026-08-30-KB-INGEST-v1.1-STORY-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · 知识库入库管线 v1.1（story_factory 产出入库 + md 通用知识库生成）
──────────────────────────────────────────────
链路: 源(story_factory jsonl) → L1 合规(自有源) → L3 三保闸(质量/主权)
     → L4 ASI 七闸验证 → 入库 train_merged.jsonl + 生成 md 通用知识库

md 知识库（通用版·人可读）:
    11_DATA/knowledge_base/<域>/<id>.md  — 单条 markdown 知识卡
    11_DATA/knowledge_base/INDEX.md      — 索引(全量重建·含多域)

v1.1 工程审查修复(2026-08-30 P04鲁班 · 吸收 P00/P15/P77/main 意见):
  - 幂等键 → 内容指纹(公共模块)；DNA 日期动态化(不再硬编码 2026-08-30)
  - id 全局唯一(内容哈希) → md 卡永不覆盖旧卡
  - md 卡/索引只写 feed_result['passed'](与 train_merged 实际入库一致·main观察)
  - dry-run 不落盘 11_DATA(不写 md 卡/INDEX)
  - INDEX.md 全量重建(含八卦路由等所有域) · 新增 --category 入参
  - --domain 白名单清洗(防路径逃逸·P77 #6)
  - 路径基于 __file__ 推导项目根

⚠️ 并发约束(P01 #3)：本脚本与 lh_kb_daemon.py 为同一写路径（train_merged append + md 卡），
   当前无 fcntl.flock 排它锁；请勿与 daemon 并发手动运行，避免 TOCTOU 双写窗口。
   双写对账方案(lh_kb_reconcile 规划中)：train_merged 内容指纹去重 + train vs md 对账，见决策清单。

用法:
    python3 08_BIN/lh_kb_ingest.py [--limit N] [--dry-run] [--domain story] [--category growth]
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

from lh_kb_common import (SYSTEM_PROMPT, atomic_append_jsonl, content_fingerprint,
                          gen_dna, gen_id, now_utc, quota_report, read_jsonl,
                          rebuild_index, sanitize_domain)

_ROOT = Path(_BIN).parent

STORY_DIR = _ROOT / "08_BIN" / "story_factory" / "output"
KB_ROOT = _ROOT / "11_DATA" / "knowledge_base"
TRAIN_MERGED = _ROOT / "11_DATA" / "bootstrap" / "train_merged.jsonl"


def collect_story_sources() -> list:
    """收集 story_factory 所有产出 jsonl（跨文件内容指纹去重）"""
    files = sorted(STORY_DIR.glob("distill_stage*.jsonl")) + \
            [STORY_DIR / "distill_final.jsonl", STORY_DIR / "distill_merged_so_far.jsonl"]
    records, seen = [], set()
    for f in files:
        if not f.exists():
            continue
        for line in read_jsonl(f):  # read_jsonl 内部已容错坏行
            msgs = line.get("messages", [])
            if not msgs:
                continue
            fp = hashlib.sha256(json.dumps(msgs, ensure_ascii=False).encode()).hexdigest()
            if fp in seen:
                continue
            seen.add(fp)
            records.append({"messages": msgs, "_src": f.name})
    return records


def to_train_record(rec: dict, domain: str, idx: int) -> dict:
    """补全训练格式：metadata 四字段 + DNA + 全局唯一 id(内容哈希)"""
    msgs = rec["messages"]
    user = next((m.get("content", "") for m in msgs if m.get("role") == "user"), "")
    assis = next((m.get("content", "") for m in msgs if m.get("role") == "assistant"), "")
    content_for_dna = f"{user}{assis}"
    meta = {
        "source": "story_factory",
        "source_url": f"file://{rec['_src']}",
        "license": "MulanPSL-2.0",  # 自有产出·工程层许可
        "dna": gen_dna(content_for_dna, "STORY"),
        "domain": domain,
        "kb_ts": now_utc(),
    }
    return {
        "id": gen_id("story", content_for_dna),
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assis},
        ],
        "metadata": meta,
    }


def to_md_card(rec: dict, out: Path) -> None:
    """生成 md 通用知识卡（role 按字段提取·无下标魔法数字）"""
    meta = rec["metadata"]
    user = next((m.get("content", "") for m in rec["messages"] if m.get("role") == "user"), "")
    assis = next((m.get("content", "") for m in rec["messages"] if m.get("role") == "assistant"), "")
    card = f"""# 知识卡 · {rec['id']}

> DNA: {meta['dna']}
> 来源: {meta['source']} ({meta.get('source_url', '')})
> 许可: {meta['license']} · 领域: {meta['domain']}
> 入库: {meta['kb_ts']}

## 提问

{user}

## 龍魂应答

{assis}
"""
    out.write_text(card, encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser(prog="lh_kb_ingest", description="知识库入库管线 v1.1")
    p.add_argument("--limit", type=int, default=0, help="限制入库条数(0=全部)")
    p.add_argument("--dry-run", action="store_true", help="只验证不入库(不写 11_DATA)")
    p.add_argument("--domain", default="story", help="领域标签(白名单清洗)")
    p.add_argument("--category", default="growth", help="ASI 七闸类别")
    args = p.parse_args()
    args.domain = sanitize_domain(args.domain)

    print(f"⏳ 收集 story_factory 产出…")
    sources = collect_story_sources()
    print(f"  收集 {len(sources)} 条（跨文件去重后）")
    if not sources:
        print("  🔴 无产出，终止")
        sys.exit(1)

    # L1 合规：自有源放行（source=story_factory·自有产出）
    print(f"✅ L1 合规闸: 自有源 story_factory 放行")

    # 炼化 → 训练格式
    limit = args.limit or len(sources)
    records = [to_train_record(s, args.domain, i) for i, s in enumerate(sources[:limit])]
    print(f"  炼化 {len(records)} 条 → 训练格式")

    # L3 三保闸
    print(f"⏳ L3 三保闸: 质量≥0.75 · 主权四字段 · SimHash去重")
    from lh_triple_guard import check
    result = check(records)
    passed = result["passed"]
    print(f"  ✅ 三保闸: 通过 {len(passed)} / {result['total']} · 拒绝 {len(result['rejected'])}")
    for r in result["rejected"][:8]:
        print(f"    🔴 {r.get('id')}: {r['reason']}")
    if len(result["rejected"]) > 8:
        print(f"    … 其余 {len(result['rejected']) - 8} 条略")
    if not passed:
        print("  🔴 无通过样本，终止")
        sys.exit(1)

    # L4 ASI 七闸验证
    print(f"⏳ L4 ASI 七闸验证…")
    from lh_asi_feed import feed
    feed_result = feed(passed, category=args.category, dry_run=args.dry_run)
    print(f"  {feed_result['status']} ASI七闸 · score={feed_result.get('score')} · passed={feed_result.get('passed_cnt')} held={feed_result.get('held_cnt')} · 幂等跳过={feed_result.get('dedup_skipped', 0)}")
    if feed_result["status"] != "🟢":
        print("  🔴 七闸未全绿，本次不入库（样本留 audit 审计日志）")
        sys.exit(2)

    # md 通用知识库：只写 feed_result['passed'](幂等后实际入库的 fresh·与 train_merged 同步)
    if args.dry_run:
        print(f"  [dry-run] 将写入 {len(feed_result['passed'])} 张知识卡 → {KB_ROOT}/{args.domain}/")
    else:
        dom_dir = KB_ROOT / args.domain
        dom_dir.mkdir(parents=True, exist_ok=True)
        written = 0
        for r in feed_result["passed"]:
            to_md_card(r, dom_dir / f"{r['id']}.md")
            written += 1
        print(f"✅ md 通用知识库: {KB_ROOT}/ 写入 {written} 条")
        rebuild_index(KB_ROOT)

    q = quota_report(TRAIN_MERGED)
    if not args.dry_run:
        print(f"✅ 入库完成: {TRAIN_MERGED}（累计 {q['total']} 条）")


if __name__ == "__main__":
    main()
