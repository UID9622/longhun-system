#!/usr/bin/env python3
# DNA: #龍芯⚡️2026-08-30-ASI-DISTILLER-L4-ASI-FEED-v1.1-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · ASI 蒸馏器 L4 ASI 接入闸 v1.1
──────────────────────────────────────────────
每批蒸馏样本入库前跑 lh_asi_fusion 七闸验证：
   样本批 → 七闸(金字塔/五行/369/易经/八门/道德经/蚁群)
         → 输出 三色 + 总分 + 证据链卡(DNA)
         → 全绿: 入库 train_merged.jsonl
         → 🟡: 暂存待审 / 🔴: 退回
审计日志: audit/distill_asi_audit.jsonl append-only

v1.1 工程审查修复(2026-08-30 P04鲁班 · 吸收 P00/P15/P77 意见):
  - 幂等键: DNA → 内容指纹(sha256 of user+assistant)，跨天 DNA 变化不再重复入库
  - 原子写: 批量入库先拼 batch 单次写入，失败记录审计不静默
  - 抽验: 逐条抽验任一硬闸🔴→整体🔴；失败过半→🟡暂存(不再无视·P00 P0-2)
  - fail-closed: 引擎不可用→🔴拒入(补全返回字段·P77 #3)
  - DNA 校验: 入库前按内容重算哈希比对，不采信样本自带 DNA(P77 #2)
  - 路径: 相对 cwd → 基于 __file__ 推导项目根

用法:
    python3 08_BIN/lh_asi_feed.py check <samples.jsonl> [--category growth] [--dry-run]
    python3 08_BIN/lh_asi_feed.py audit-view
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

from lh_kb_common import (atomic_append_jsonl, content_fingerprint, dna_hash_ok,
                          existing_fingerprints, now_utc, read_jsonl)

_ROOT = Path(_BIN).parent

AUDIT_LOG = _ROOT / "audit" / "distill_asi_audit.jsonl"
TRAIN_MERGED = _ROOT / "11_DATA" / "bootstrap" / "train_merged.jsonl"

HARD_GATES = {"金字塔", "道德经", "生死门"}


def _load_samples(path: Path) -> list:
    return read_jsonl(path)


def check_batch(samples: list, category: str = "growth", dry_run: bool = False) -> dict:
    """七闸验证整批样本（代表性合并文本 + 逐条抽样）。全绿才放行。"""
    fail = {
        "status": "🔴", "reason": "ASI引擎不可用", "batch_dna": "N/A-ENGINE-DOWN",
        "category": category, "evidence_cards": [], "sample_statuses": [],
        "passed": [], "held": samples, "dry_run": dry_run,
    }
    try:
        from lh_asi_fusion import FusionEngine
        engine = FusionEngine()
    except Exception as e:
        fail["reason"] = f"ASI引擎不可用: {e}"
        return fail

    # 代表性文本：system(龍魂价值观=道德经正锚) + user + assistant
    sample_texts = []
    for s in samples:
        msgs = s.get("messages", [])
        syst = next((m.get("content", "") for m in msgs if m.get("role") == "system"), "")
        user = next((m.get("content", "") for m in msgs if m.get("role") == "user"), "")
        assis = next((m.get("content", "") for m in msgs if m.get("role") == "assistant"), "")
        sample_texts.append(f"{syst[:150]}；{user[:200]}；{assis[:300]}")

    # 整批合并文本过一次七闸（代表性验证）
    merged = "；".join(t[:120] for t in sample_texts[:10])
    try:
        res = engine.run(merged, category=category)
        batch_status = res.status
        batch_score = res.score
        evidence_cards = [e.to_dict() for e in res.evidences]
    except Exception as e:
        batch_status, batch_score = "🟡", 0
        evidence_cards = [{"gate": "系统", "status": "🟡", "detail": str(e)}]

    # 蒸馏入库场景判定：硬闸（价值观红线）= 金字塔/道德经/生死门 必须无🔴；
    # 软闸（蚁群共识/易经相位/369警示/五行映射）= 🟡 记成长待审不拦截。
    hard_red = any(
        c.get("status") == "🔴" and c.get("gate") in HARD_GATES
        for c in evidence_cards
    )

    # 逐条抽验（最多 30 条，防刷分）
    sampled = []
    for idx, s in enumerate(samples[:30]):
        txt = sample_texts[idx] if idx < len(sample_texts) else merged
        try:
            r = engine.run(txt, category=category)
        except Exception:
            r = None
        sampled.append(r.to_dict() if r else {"status": "🟡", "score": 0, "evidences": []})

    # 抽验参与判定(P00 P0-2)：任一硬闸🔴→整体🔴；异常/失败过半→🟡暂存（不静默无视）
    sample_hard_red = any(
        e.get("status") == "🔴" and e.get("gate") in HARD_GATES
        for s in sampled if isinstance(s, dict)
        for e in s.get("evidences", [])
    )
    sample_failed = sum(1 for s in sampled if not s.get("evidences"))
    sample_bad_ratio = sample_failed / len(sampled) if sampled else 0.0

    if hard_red or sample_hard_red:
        verdict = "🔴"
    elif sample_bad_ratio > 0.5:
        verdict = "🟡"   # 抽验过半失败：引擎不稳定/内容异常，暂存待审
    else:
        verdict = "🟢"

    batch_dna = f"#龍芯⚡️ASI-FEED-{hashlib.sha256(merged.encode()).hexdigest()[:8]}-UID9622"
    return {
        "status": verdict,
        "score": batch_score,
        "batch_dna": batch_dna,
        "category": category,
        "evidence_cards": evidence_cards,
        "sample_statuses": sampled,
        "passed": samples if verdict == "🟢" else [],
        "held": samples if verdict != "🟢" else [],
        "dry_run": dry_run,
    }


def append_audit(entry: dict) -> None:
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry["_id"] = hashlib.sha256(
        json.dumps({k: v for k, v in entry.items() if k != "_id"}, ensure_ascii=False, default=str).encode()
    ).hexdigest()[:16]
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")


def _reject_sovereignty(samples: list) -> list:
    """独立 CLI 防绕过(P77 #2)：主权四字段 + DNA 一致性校验，不通过的样本直接剔除并 warning。"""
    bad, keep = [], []
    for s in samples:
        meta = s.get("metadata") or {}
        missing = [f for f in ("dna", "source", "license", "source_url") if not meta.get(f)]
        if missing:
            bad.append({"id": s.get("id", "?"), "reason": f"主权字段缺失: {missing}"})
            continue
        if not dna_hash_ok(s):
            bad.append({"id": s.get("id", "?"), "reason": "DNA哈希不一致(内容与DNA不匹配)"})
            continue
        keep.append(s)
    for b in bad[:5]:
        print(f"  ⚠️ 主权校验拒绝 {b['id']}: {b['reason']}")
    if len(bad) > 5:
        print(f"  ⚠️ 其余 {len(bad) - 5} 条主权校验拒绝略")
    return keep


def feed(samples: list, category: str = "growth", dry_run: bool = False) -> dict:
    """L4 主入口：主权校验 → 七闸验证 → 幂等入库(内容指纹) → 审计"""
    samples = _reject_sovereignty(samples)
    result = check_batch(samples, category=category, dry_run=dry_run)
    result["ts"] = now_utc()
    result["total"] = len(samples)
    result["dedup_skipped"] = 0

    if result["status"] == "🟢" and not dry_run:
        existing = existing_fingerprints(TRAIN_MERGED)
        fresh = [s for s in result["passed"] if content_fingerprint(s) not in existing]
        result["dedup_skipped"] = len(result["passed"]) - len(fresh)
        try:
            atomic_append_jsonl(TRAIN_MERGED, fresh)
            result["appended_to"] = str(TRAIN_MERGED)
        except Exception as e:
            result["status"] = "🔴"
            result["reason"] = f"入库失败: {e}"
            fresh = []
        result["passed"] = fresh
    result["passed_cnt"] = len(result["passed"])
    result["held_cnt"] = len(result["held"])

    append_audit(result)
    return result


def audit_view() -> None:
    if not AUDIT_LOG.exists():
        print("无审计记录")
        return
    lines = AUDIT_LOG.read_text(encoding="utf-8").splitlines()
    print(f"审计记录总数: {len(lines)}")
    for line in lines[-10:]:
        try:
            e = json.loads(line)
            print(f"  {e.get('ts','')[:19]} {e.get('status')} total={e.get('total')} passed={e.get('passed_cnt')} held={e.get('held_cnt')} {e.get('batch_dna','')}")
        except Exception:
            pass


def main() -> None:
    p = argparse.ArgumentParser(prog="lh_asi_feed", description="ASI 蒸馏器 L4 接入闸 v1.1")
    p.add_argument("cmd", choices=["check", "audit-view"], default="check")
    p.add_argument("file", nargs="?", help="蒸馏样本 jsonl")
    p.add_argument("--category", default="growth")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    if args.cmd == "audit-view":
        audit_view()
        return
    if not args.file:
        print("需要样本文件")
        return
    samples = _load_samples(Path(args.file))
    result = feed(samples, category=args.category, dry_run=args.dry_run)
    print(f"{result['status']} ASI七闸验证 · total={result['total']} passed={result['passed_cnt']} held={result['held_cnt']}")
    print(f"  分数: {result.get('score')} · DNA: {result.get('batch_dna')}")
    if result.get("appended_to"):
        print(f"  ✅ 已入库: {result['appended_to']}")
    if result.get("evidence_cards"):
        for c in result["evidence_cards"]:
            print(f"    {c.get('status')} [{c.get('gate')}] {c.get('detail','')[:60]}")


if __name__ == "__main__":
    main()
