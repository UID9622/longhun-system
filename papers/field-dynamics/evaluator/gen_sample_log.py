#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍魂 · 场域动力学示例日志生成器 v1.0
# DNA: #龍芯⚡️丙午·丙申·乙丑·壬午·䷨损-FIELD-DYNAMICS-SAMPLE-GEN-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 用途: 生成 1000 条符合 schema 的标准测试日志（含 2 个标注翻转点），
#       供 evaluator.py 演示完整评测链路。
"""示例日志生成器 —— 让 evaluator 开箱即测。

故事线（4 个阶段 · 2 次失谐-崩溃周期）:
  Phase0 (0-399)  稳态: 三头一致, 低冲突
  Phase1 (400-559) 失谐①: heads 分歧累积 → 崩溃点 A
  Phase2 (560-799) 恢复: 规则更新, 回归稳态
  Phase3 (800-999) 失谐②: 分歧低但 U 维漂移(行为与裁决脱节) → 崩溃点 B
"""
import argparse
import hashlib
import json
import random
import sys
from datetime import datetime, timedelta, timezone

__version__ = "1.0.0"


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def gen(seed: int = 42, n: int = 1000, out: str = "sample-log.jsonl") -> None:
    rng = random.Random(seed)
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    crash_a, crash_b = 560, 950

    with open(out, "w", encoding="utf-8") as f:
        for i in range(n):
            t = base + timedelta(seconds=30 * i)
            ts = t.isoformat()

            # --- 失谐强度 by phase ---
            if i < 400:                       # 稳态
                dissent = 0.02
                conflicts = rng.randint(0, 1)
            elif i < 560:                     # 失谐① 缓慢累积
                ramp = (i - 400) / 160
                dissent = 0.05 + 0.55 * ramp + rng.uniform(0, 0.08)
                conflicts = rng.randint(1, 5)
            elif i < 800:                     # 恢复
                dissent = 0.03 + rng.uniform(0, 0.03)
                conflicts = rng.randint(0, 2)
            else:                             # 失谐② U 维漂移为主, A 维低
                dissent = 0.05 + rng.uniform(0, 0.05)
                conflicts = rng.randint(0, 2)

            # --- heads: 按失谐强度分配 c 头分歧 ---
            heads = {"a": "ok", "b": "ok", "c": "ok"}
            if dissent > 0.30:
                heads["c"] = "reject"
            elif dissent > 0.12:
                heads["c"] = "reject" if rng.random() < 0.5 else "ok"

            # --- verdicts: 多数裁决; U 维漂移窗口 (800-949) 行为与裁决脱节 ---
            verdicts = {"truth": "ok", "lesson": "keep", "verify": "ok"}
            if 820 <= i < 950 and rng.random() < 0.35:   # verify 链脱节
                verdicts["verify"] = "reject"

            blocked = i > 555 and dissent > 0.35          # 拦截触发
            rule_fired = f"HF-{rng.randint(1, 29)}" if (i >= 400 and i % 3 == 0) else None

            # --- 标注区 ---
            lbl = {"crash_at": None, "precursor_dimension": None, "annotator": "synthetic-v1.0"}
            if i == crash_a:
                lbl["crash_at"] = t.isoformat()
                lbl["precursor_dimension"] = "A"
            elif i == crash_b:
                lbl["crash_at"] = t.isoformat()
                lbl["precursor_dimension"] = "U"
            elif 520 <= i < crash_a and dissent > 0.4:
                lbl["precursor_dimension"] = "A"
            elif 900 <= i < crash_b and verdicts["verify"] == "reject":
                lbl["precursor_dimension"] = "U"

            ev = {
                "ts": ts,
                "input_hash": sha256_hex(f"sample-{seed}-{i}"),
                "session_id": "sample-agent-01",
                "heads": heads,
                "verdicts": verdicts,
                "audit_level": "G2",
                "blocked": blocked,
                "rule_fired": rule_fired,
                "user_escalated": dissent > 0.55,
                "conflict_marks": conflicts,
                "labels": lbl,
                "extensions": {"sample_phase": "phase0" if i < 400 else
                               "phase1" if i < 560 else "phase2" if i < 800 else "phase3"},
            }
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")

    print(f"generated {n} events -> {out} | crashes at idx {crash_a}, {crash_b}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="场域动力学示例日志生成器")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--out", default="sample-log.jsonl")
    args = ap.parse_args()
    sys.exit(gen(args.seed, args.n, args.out))
