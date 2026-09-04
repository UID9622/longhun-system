#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍魂 · 场域动力学统一评测器 v1.0
# DNA: #龍芯⚡️丙午·丙申·乙丑·壬午·䷨损-FIELD-DYNAMICS-EVALUATOR-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 关联提案: papers/LH-FIELD-DYNAMICS-PROPOSAL-v1.0.md
# 用途: 标准测试日志 → U/D/A/H 四维归一化 + FHI 指数 + 统一评测指标(Δt/FPR/FNR/F1)
#       面向 GitHub 开源开发者，接入四个框架的统一评测基准原型。
"""场域动力学统一评测器 v1.0

从标准测试日志（schema/field-dynamics-log.schema.json）计算：
  1. U/D/A/H 四维归一化指标（跨框架可比）
  2. FHI 场域健康度指数（默认等权 0.25，可场景标定）
  3. 统一评测指标：预警提前量 Δt、误报率 FPR、漏报率 FNR、F1
  4. 维度归因一致性（H3 假设的观测输入）

用法:
  python3 evaluator.py --log <std-log.jsonl> --crash-window 300 --weights 0.25,0.25,0.25,0.25
  python3 evaluator.py --self-test   # 内置冒烟测试

该原型仅做"观测对齐"，不统一各框架的实现哲学（外部存储 vs 内部感知）。
"""

import argparse
import json
import sys
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

__version__ = "1.0.0"


# ---------------------------------------------------------------------------
# 一、四维归一化（代理指标 → [0,1]）
# ---------------------------------------------------------------------------

def normalize(value: float, lo: float, hi: float) -> float:
    """线性归一化到 [0,1]。lo/hi 为工程经验边界（可复算、可重标定）。"""
    if hi <= lo:
        return 0.5
    return max(0.0, min(1.0, (value - lo) / (hi - lo)))


def compute_dimensions(events: List[Dict]) -> Dict[str, List[float]]:
    """逐事件计算 U/D/A/H 四维观测值。

    代理口径（与提案 §3.2 对应，全部可从公共字段计算）:
      U(统一性)  = 1 - verdicts 与 heads 多数的分歧率      # 行为一致性
      D(发展性)  = rule_fired 触发即记 1（规则生效=演化信号）
      A(对抗性)  = conflict_marks 归一化 + heads 分歧率     # 矛盾密度
      H(和谐度)  = 1 - max(0, conflict_marks - threshold)   # 冲突-解决闭环比代理
    """
    series = {"U": [], "D": [], "A": [], "H": []}
    for ev in events:
        heads = ev.get("heads") or {}
        verdicts = ev.get("verdicts") or {}
        conflicts = int(ev.get("conflict_marks") or 0)

        # A 维: 多路分歧率 + 冲突密度
        head_vals = [str(v) for v in heads.values() if v is not None]
        if len(head_vals) >= 2:
            majority = max(head_vals.count(v) for v in set(head_vals))
            dissent = 1.0 - majority / len(head_vals)
        else:
            dissent = 0.0
        a_raw = 0.6 * dissent + 0.4 * normalize(conflicts, 0, 10)
        series["A"].append(a_raw)

        # U 维: 行为输出与裁决一致 = 1 - 分歧率
        if head_vals and verdicts:
            verdict_vals = [str(v) for v in verdicts.values() if v is not None]
            if verdict_vals:
                dissent_uv = sum(1 for hv in head_vals if hv not in verdict_vals) / len(head_vals)
                series["U"].append(1.0 - dissent_uv)
            else:
                series["U"].append(1.0 - dissent)
        else:
            series["U"].append(1.0 - dissent)

        # D 维: 规则演化信号（有规则触发=演化活跃）
        series["D"].append(1.0 if ev.get("rule_fired") else 0.0)

        # H 维: 和谐度 = 冲突未失控
        series["H"].append(1.0 - normalize(conflicts, 0, 5))

    return series


# ---------------------------------------------------------------------------
# 二、FHI 场域健康度指数
# ---------------------------------------------------------------------------

def fhi_index(dims: Dict[str, List[float]], weights: Dict[str, float]) -> List[float]:
    """FHI(t) = wU·Û + wD·D̂ + wA·(1-Â) + wH·Ĥ"""
    w = {k: weights.get(k, 0.25) for k in ("U", "D", "A", "H")}
    n = max(len(dims[k]) for k in dims)
    out = []
    for i in range(n):
        u = dims["U"][i] if i < len(dims["U"]) else 0.5
        d = dims["D"][i] if i < len(dims["D"]) else 0.5
        a = dims["A"][i] if i < len(dims["A"]) else 0.5
        h = dims["H"][i] if i < len(dims["H"]) else 0.5
        out.append(round(w["U"] * u + w["D"] * d + w["A"] * (1 - a) + w["H"] * h, 4))
    return out


# ---------------------------------------------------------------------------
# 三、统一评测指标（Δt / FPR / FNR / F1）
# ---------------------------------------------------------------------------

def evaluate_alerts(events: List[Dict], alert_fn, crash_window_sec: float) -> Dict:
    """按预警函数评测。

    alert_fn(event, history) -> bool：框架预警逻辑（默认: A 维越过阈值 0.3）。
    crash 标注: labels.crash_at 非空的事件为崩溃点。
    """
    crashes = []
    for i, ev in enumerate(events):
        lbl = ev.get("labels") or {}
        if lbl.get("crash_at"):
            crashes.append(i)

    if not crashes:
        return {"precursor_lead_time": None, "fpr": 0.0, "fnr": 0.0, "f1": 0.0,
                "n_alerts": 0, "n_crashes": 0, "note": "无标注崩溃点，跳过评测"}

    alerts = []  # (idx, ts)
    history = []
    for i, ev in enumerate(events):
        if alert_fn(ev, history):
            alerts.append(i)
        history.append(ev)

    # 预警提前量：崩溃前最后一次预警到崩溃的间隔（事件数）
    lead_times = []
    for cidx in crashes:
        prior = [a for a in alerts if a < cidx]
        if prior:
            lead_times.append(cidx - max(prior))
    mean_lead = round(sum(lead_times) / len(lead_times), 2) if lead_times else None

    # FPR: 未崩溃窗口内预警的比例；FNR: 崩溃前无预警的比例
    crash_set = set(crashes)
    false_alerts = sum(1 for a in alerts if not any(0 <= a - c <= crash_window_sec / 60 for c in crashes))
    total_non_crash = max(1, len(events) - len(crashes))
    fpr = round(false_alerts / total_non_crash, 4)

    missed = sum(1 for c in crashes if not any(a < c for a in alerts))
    fnr = round(missed / len(crashes), 4)

    # F1（对崩溃前 30 步窗口预警视为正例命中）
    tp = len(crashes) - missed
    fp = false_alerts
    fn = missed
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = round(2 * prec * rec / (prec + rec), 4) if (prec + rec) else 0.0

    return {"precursor_lead_time": mean_lead, "fpr": fpr, "fnr": fnr, "f1": f1,
            "n_alerts": len(alerts), "n_crashes": len(crashes)}


def default_alert_fn(threshold: float = 0.3):
    """默认预警函数：A 维归一化对抗性越过阈值（H1 假设的工程实现）。"""
    def fn(ev, history):
        heads = ev.get("heads") or {}
        head_vals = [str(v) for v in heads.values() if v is not None]
        if len(head_vals) < 2:
            return False
        majority = max(head_vals.count(v) for v in set(head_vals))
        dissent = 1.0 - majority / len(head_vals)
        return dissent > threshold
    return fn


# ---------------------------------------------------------------------------
# 四、维度归因（H3 假设观测输入）
# ---------------------------------------------------------------------------

def dimension_attribution(dims: Dict[str, List[float]], crash_idx: int, lookback: int = 30) -> Optional[str]:
    """归因崩溃前主导退化维度：lookback 窗口内下降幅度最大的维度。"""
    if crash_idx < 1:
        return None
    start = max(0, crash_idx - lookback)
    best_dim, best_drop = None, -1.0
    for k in ("U", "D", "A", "H"):
        series = dims[k]
        seg = series[start:crash_idx]
        if len(seg) >= 2:
            drop = seg[0] - seg[-1]  # U/D/H 越高越健康 → 下降=退化
            if drop > best_drop:
                best_drop, best_dim = drop, k
    return best_dim


# ---------------------------------------------------------------------------
# 五、入口
# ---------------------------------------------------------------------------

def load_log(path: str) -> List[Dict]:
    events = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            events.append(json.loads(line))
    return events


def self_test() -> None:
    """内置冒烟测试：构造含 2 个翻转点样本，验证管线可跑。"""
    from datetime import timedelta
    base = datetime(2026, 8, 19, tzinfo=timezone.utc)
    events = []
    for i in range(200):
        heads = {"a": "ok", "b": "ok", "c": "ok"}
        if 120 <= i <= 145:                      # 失谐窗口：c 头与 a/b 分歧
            heads["c"] = "reject"
        ev = {
            "ts": (base + timedelta(seconds=30 * i)).isoformat(),
            "input_hash": "0" * 64,
            "session_id": "selftest",
            "heads": heads,
            "verdicts": {"truth": "ok", "lesson": "keep", "verify": "ok"},
            "audit_level": "G2",
            "blocked": i > 145,
            "rule_fired": f"HF-{i % 29}",
            "user_escalated": False,
            "conflict_marks": 2 if 120 <= i <= 145 else 0,
            "labels": {"crash_at": None, "precursor_dimension": "A" if 120 <= i <= 145 else None},
        }
        events.append(ev)
    events[150]["labels"]["crash_at"] = events[150]["ts"]  # 翻转点

    dims = compute_dimensions(events)
    fhi = fhi_index(dims, {"U": 0.25, "D": 0.25, "A": 0.25, "H": 0.25})
    res = evaluate_alerts(events, default_alert_fn(0.3), crash_window_sec=300)
    print(f"self-test OK | events={len(events)} fhi_range=[{min(fhi):.3f},{max(fhi):.3f}] "
          f"metrics={res}")


def main() -> int:
    ap = argparse.ArgumentParser(description="场域动力学统一评测器 v1.0")
    ap.add_argument("--log", help="标准测试日志 JSONL 路径")
    ap.add_argument("--weights", default="0.25,0.25,0.25,0.25", help="U,D,A,H 权重")
    ap.add_argument("--threshold", type=float, default=0.3, help="A 维预警阈值（H1）")
    ap.add_argument("--crash-window", type=float, default=300.0, help="崩溃窗口(秒)")
    ap.add_argument("--self-test", action="store_true", help="运行冒烟测试")
    args = ap.parse_args()

    if args.self_test:
        self_test()
        return 0
    if not args.log:
        print("error: 需 --log 或 --self-test", file=sys.stderr)
        return 2

    w = dict(zip(("U", "D", "A", "H"), (float(x) for x in args.weights.split(","))))
    events = load_log(args.log)
    dims = compute_dimensions(events)
    fhi = fhi_index(dims, w)
    metrics = evaluate_alerts(events, default_alert_fn(args.threshold), crash_window_sec=args.crash_window)

    report = {
        "log": args.log,
        "events": len(events),
        "fhi_series": fhi,
        "fhi_now": fhi[-1] if fhi else None,
        "dim_means": {k: round(sum(v) / len(v), 4) if v else None for k, v in dims.items()},
        "alerts": metrics,
        "weights": w,
        "threshold": args.threshold,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
