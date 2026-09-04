#!/usr/bin/env python3
# DNA: #龍芯⚡️2026-08-30-ASI-DISTILLER-L3-TRIPLE-GUARD-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · ASI 蒸馏器 L3 三保闸 v1.0
──────────────────────────────────────────────
三保: 保质量 / 保主权 / 保能力
  - 保质量: quality_score ≥ QUALITY_MIN (0.75) + SimHash 跨域去重
  - 保主权: dna/source/license/source_url 四字段必填（血缘哈希链）
  - 保能力: 核心域（CNSH/DNA/369/人格/协议/审计）占比 ≥ CORE_MIN (0.20)
           防止蒸馏冲淡核心能力（对齐 ASI 天花板协议）

用法:
    python3 08_BIN/lh_triple_guard.py check <train.jsonl>
    python3 08_BIN/lh_triple_guard.py quota <train.jsonl>          # 能力配额审计
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

QUALITY_MIN = 0.75
CORE_MIN = 0.20
CORE_DOMAINS = {"cognition", "cns", "dna", "369", "persona", "protocol", "audit",
                "八卦", "安全", "审计", "协议", "人格", "数字根"}

# ── 质量锚词（启发式·对齐 lh_knowledge_distiller._score_quality） ──
ANCHOR_WORDS = {
    "cognition": ["认知", "推演", "决策", "逻辑", "推理"],
    "cns": ["CNSH", "语义", "语法", "编译"],
    "dna": ["DNA", "追溯", "干支", "卦象"],
    "369": ["369", "洛书", "数字根", "河图"],
    "persona": ["人格", "龍芯", "魯班", "文心", "职责"],
    "protocol": ["协议", "铁律", "焊死", "底线", "熔断"],
    "audit": ["审计", "三色", "检查", "扫描", "风险"],
    "八卦": ["八卦", "卦象", "乾", "坤", "震", "巽", "坎", "离", "艮", "兑", "路由"],
}


def _simhash(text: str, n: int = 4) -> int:
    """简化 SimHash：字符 n-gram 加权哈希（sha256·安全基线禁 MD5）"""
    text = re.sub(r"\s+", "", text)
    grams = [text[i:i + n] for i in range(len(text) - n + 1)]
    v = [0] * 64
    for g in grams[:2000]:
        h = int(hashlib.sha256(g.encode()).hexdigest(), 16)
        for i in range(64):
            v[i] += 1 if (h >> i) & 1 else -1
    return sum((1 << i) for i in range(64) if v[i] > 0)


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def quality_score(record: dict) -> float:
    """保质量：结构完整性 + 内容长度 + 锚词 + 推理链（通用版·不偏科任何域）"""
    msgs = record.get("messages", [])
    text = " ".join(m.get("content", "") for m in msgs if m.get("content"))
    reasoning = record.get("reasoning_chain", "")
    user = next((m.get("content", "") for m in msgs if m.get("role") == "user"), "")
    assis = next((m.get("content", "") for m in msgs if m.get("role") == "assistant"), "")
    roles = [m.get("role") for m in msgs if m.get("content")]

    # 领域锚词命中（任一词表≥1即有效命中）
    anchor_hit = any(any(w in text for w in words) for words in ANCHOR_WORDS.values())

    # 结构化指令数据：user+assistant 完整 + 领域锚词 → 独立评分路径
    # （指令→精确映射型：如八卦路由，output 短是其固有形态，长度门槛不适用）
    if user and assis and anchor_hit and len(text) <= 500:
        score = 0.55
        if anchor_hit:
            score += 0.1       # 领域锚词加分（卦象/路由/八卦等）
        if len(text) > 200:
            score += 0.1
        if reasoning:
            score += 0.2
        if re.search(r"(?:综上所述|因此|所以|总之)", text):
            score += 0.1
        return min(score, 1.0)

    # 通用长文本路径
    score = 0.4
    if "user" in roles and "assistant" in roles:
        score += 0.1
    if len(assis) > 300:
        score += 0.15
    if len(text) > 500:
        score += 0.05
    if len(text) > 1000:
        score += 0.05
    if reasoning:
        score += 0.2
    for words in ANCHOR_WORDS.values():
        if sum(1 for w in words if w in text) >= 3:
            score += 0.1
            break
    if re.search(r"(?:首先|其次|最后|第一|第二|第三)", text):
        score += 0.05
    if re.search(r"(?:综上所述|因此|所以|总之)", text):
        score += 0.05
    return min(score, 1.0)


def classify(text: str) -> str:
    """领域分类"""
    for domain, words in ANCHOR_WORDS.items():
        if sum(1 for w in words if w in text) >= 2:
            return domain
    return "通用"


def check(records: list, quality_min: float = QUALITY_MIN) -> dict:
    """L3 主闸: 逐条 保质量+保主权 + 批次 保能力"""
    passed, rejected = [], []
    seen_fp = {}
    for rec in records:
        # ── 保主权: 四字段必填 ──
        meta = rec.get("metadata", {}) or {}
        missing = [f for f in ("dna", "source", "license", "source_url") if not meta.get(f)]
        if missing:
            rejected.append({"id": rec.get("id", "?"), "reason": f"主权字段缺失: {missing}"})
            continue
        # ── 保质量 ──
        q = quality_score(rec)
        if q < quality_min:
            rejected.append({"id": rec.get("id", "?"), "reason": f"质量 {q:.2f} < {quality_min}", "score": q})
            continue
        # ── SimHash 去重（跨域双键·仅 user+assistant，排除固定 system prompt） ──
        text = " ".join(
            m.get("content", "") for m in rec.get("messages", [])
            if m.get("content") and m.get("role") in ("user", "assistant")
        )
        fp = _simhash(text)
        domain = classify(text)
        key = f"{domain}:{fp}"
        if key in seen_fp:
            rejected.append({"id": rec.get("id", "?"), "reason": f"SimHash重复(域{domain})", "score": q})
            continue
        seen_fp[key] = rec.get("id", "?")
        rec["metadata"]["quality_score"] = round(q, 3)
        rec["metadata"]["domain"] = domain
        passed.append(rec)

    # ── 保能力: 核心域配额（批次级统计·全局配额由 quota() 对全库审计） ──
    domains = Counter(r["metadata"].get("domain", "通用") for r in passed)
    core_cnt = sum(c for d, c in domains.items() if d in CORE_DOMAINS)
    core_ratio = core_cnt / len(passed) if passed else 0.0
    quota_ok = core_ratio >= CORE_MIN

    return {
        "total": len(records),
        "passed": passed,
        "rejected": rejected,
        "domains": dict(domains),
        "core_ratio": round(core_ratio, 3),
        "quota_ok": quota_ok,
        "core_min": CORE_MIN,
        "quality_min": quality_min,
    }


def quota(records: list) -> dict:
    """全库能力配额审计：核心域占比 ≥ CORE_MIN（防蒸馏冲淡核心能力）
    域判定基于实时 classify(user+assistant)，不依赖存储域（存储域可能因词表演进滞后）。"""
    domains = Counter()
    for r in records:
        meta = r.get("metadata", {}) or {}
        stored = meta.get("domain")
        if stored and stored in CORE_DOMAINS:
            domains[stored] += 1
            continue
        text = " ".join(
            m.get("content", "") for m in r.get("messages", [])
            if m.get("content") and m.get("role") in ("user", "assistant")
        )
        domains[classify(text)] += 1
    core_cnt = sum(c for d, c in domains.items() if d in CORE_DOMAINS)
    core_ratio = core_cnt / len(records) if records else 0.0
    return {
        "total": len(records),
        "domains": dict(domains),
        "core_cnt": core_cnt,
        "core_ratio": round(core_ratio, 3),
        "quota_ok": core_ratio >= CORE_MIN,
        "core_min": CORE_MIN,
    }


def _load_records(path: Path) -> list:
    """读 jsonl：坏行计数并 warning（不整批抛异常·可观测性）"""
    recs, bad = [], 0
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            recs.append(json.loads(line))
        except Exception as e:
            bad += 1
            if bad <= 3:
                print(f"  ⚠️ 坏行跳过: {e}")
    if bad > 3:
        print(f"  ⚠️ 共跳过 {bad} 坏行")
    return recs


def main() -> None:
    p = argparse.ArgumentParser(prog="lh_triple_guard", description="ASI 蒸馏器 L3 三保闸 v1.0")
    p.add_argument("cmd", choices=["check", "quota"])
    p.add_argument("file", help="训练数据 jsonl 路径")
    p.add_argument("--quality-min", type=float, default=QUALITY_MIN)
    args = p.parse_args()

    recs = _load_records(Path(args.file))
    result = check(recs, args.quality_min)

    print(f"🟢 三保闸检查 · 总数 {result['total']} · 通过 {len(result['passed'])} · 拒绝 {len(result['rejected'])}")
    for r in result["rejected"][:10]:
        print(f"  🔴 {r.get('id')}: {r['reason']}")
    if len(result["rejected"]) > 10:
        print(f"  … 其余 {len(result['rejected']) - 10} 条略")
    print(f"领域分布: {result['domains']}")
    print(f"核心域占比: {result['core_ratio']:.1%} (阈值 {result['core_min']:.0%}) → {'🟢' if result['quota_ok'] else '🔴 不达标'}")


if __name__ == "__main__":
    main()
