#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂审计状态汇总工具 v1.0
DNA: #龍芯⚡️2026-08-21-AUDIT-STATUS-v1.0
功能: 读取 audit_log.jsonl + test_log.jsonl，汇总七大维度三色状态
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
AUDIT_LOG = ROOT / "audit_log.jsonl"
TEST_LOG = ROOT / "test_log.jsonl"

# ────────────────────────────────────────────────
# 常量
# ────────────────────────────────────────────────

DIMENSIONS = [
    ("code",       "代码审计"),
    ("protocol",   "协议审计"),
    ("red_blue",   "红蓝对抗"),
    ("fix",        "修复优化"),
    ("success",    "成功标准"),
    ("experiment", "实验验证"),
    ("test",       "自测体系"),
]

COLOR = {
    "green":  "🟢 通过",
    "yellow": "🟡 待审",
    "red":    "🔴 拒绝",
    "none":   "⚪ 未审计",
}

# P0 熔断条件关键字
P0_KEYWORDS = [
    "remote_exploit", "rce", "forge_dna", "tamper_log",
    "bypass_defense", "protocol_critical", "confirm_invalid",
]


# ────────────────────────────────────────────────
# 数据加载
# ────────────────────────────────────────────────

def load_jsonl(path: Path) -> list:
    """load JSONL 文件，容错处理"""
    records = []
    if not path.exists():
        return records
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"  ⚠️  第 {i} 行 JSON 解析失败: {e}", file=sys.stderr)
    return records


# ────────────────────────────────────────────────
# 状态计算
# ────────────────────────────────────────────────

def compute_dim_status(records: list, dim_key: str) -> dict:
    """计算单一维度的三色状态"""
    relevant = [r for r in records if r.get("dimension") == dim_key]
    if not relevant:
        return {"color": "none", "green": 0, "yellow": 0, "red": 0, "total": 0,
                "p0": False, "last_dna": "", "last_time": ""}

    g = sum(1 for r in relevant if r.get("status") == "green")
    y = sum(1 for r in relevant if r.get("status") == "yellow")
    r = sum(1 for r in relevant if r.get("status") == "red")
    p0 = any(r.get("p0") or any(k in str(r).lower() for k in P0_KEYWORDS)
             for r in relevant)

    if r > 0 or p0:
        color = "red"
    elif y > 0:
        color = "yellow"
    else:
        color = "green"

    last = max(relevant, key=lambda x: x.get("timestamp", ""))
    return {
        "color": color, "green": g, "yellow": y, "red": r,
        "total": len(relevant), "p0": p0,
        "last_dna": last.get("dna", ""),
        "last_time": last.get("timestamp", ""),
    }


def compute_test_status(test_records: list) -> dict:
    """计算自测体系专属状态"""
    if not test_records:
        return {"color": "none", "passed": 0, "failed": 0, "total": 0,
                "coverage": 0.0, "last_dna": "", "last_time": ""}

    passed  = sum(1 for r in test_records if r.get("result") in ("pass", "passed", "green"))
    failed  = sum(1 for r in test_records if r.get("result") in ("fail", "failed", "red"))
    total   = len(test_records)
    coverage = sum(r.get("coverage", 0) for r in test_records) / total if total else 0

    color = "red" if failed > 0 else ("yellow" if coverage < 80 else "green")
    last = max(test_records, key=lambda x: x.get("timestamp", ""))
    return {
        "color": color, "passed": passed, "failed": failed, "total": total,
        "coverage": round(coverage, 1),
        "last_dna": last.get("dna", ""),
        "last_time": last.get("timestamp", ""),
    }


# ────────────────────────────────────────────────
# 输出
# ────────────────────────────────────────────────

def print_status(full: bool = False):
    audit_records = load_jsonl(AUDIT_LOG)
    test_records  = load_jsonl(TEST_LOG)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print()
    print("╔" + "═" * 63 + "╗")
    print("║  🐉 龍魂审计状态总览 v1.0" + " " * 36 + "║")
    print("╠" + "═" * 63 + "╣")
    print(f"║  生成时间: {now}" + " " * (49 - len(now)) + "║")
    print("║  数据源: audit_log.jsonl ({} 条) + test_log.jsonl ({} 条)  ║".format(
        len(audit_records), len(test_records))[:65] + "║")
    print("╠" + "═" * 63 + "╣")
    print("║  {:<10} {:<12} {:>4} {:>4} {:>4} {:>6}  ║".format(
        "维度KEY", "维度名", "🟢", "🟡", "🔴", "状态"))
    print("╠" + "═" * 63 + "╣")

    dim_results = {}
    overall_red = False
    overall_yellow = False
    p0_triggered = False

    for key, name in DIMENSIONS:
        if key == "test":
            s = compute_test_status(test_records)
            g_str = str(s["passed"])
            y_str = "-"
            r_str = str(s["failed"])
        else:
            s = compute_dim_status(audit_records, key)
            g_str = str(s["green"])
            y_str = str(s["yellow"])
            r_str = str(s["red"])

        color_label = COLOR[s["color"]]
        dim_results[key] = s

        if s["color"] == "red":
            overall_red = True
        elif s["color"] == "yellow":
            overall_yellow = True
        if s.get("p0"):
            p0_triggered = True

        print("║  {:<10} {:<12} {:>4} {:>4} {:>4}  {:<8}  ║".format(
            key, name, g_str, y_str, r_str, color_label))

    print("╠" + "═" * 63 + "╣")

    # 整体判定
    if overall_red or p0_triggered:
        overall = "🔴 拒绝"
    elif overall_yellow:
        overall = "🟡 待审"
    else:
        overall = "🟢 通过"

    print("║  综合判定: {:<52}║".format(overall))
    if p0_triggered:
        print("║  ⚠️  P0 熔断已触发！请立即处理。" + " " * 38 + "║")
    print("╚" + "═" * 63 + "╝")

    if full:
        print()
        print("📎 详细信息：")
        for key, name in DIMENSIONS:
            s = dim_results[key]
            print(f"  [{name}]")
            if s.get("last_time"):
                print(f"    最近操作: {s['last_time']}")
            if s.get("last_dna"):
                print(f"    DNA: {s['last_dna']}")
            if key == "test" and s.get("coverage") is not None:
                print(f"    覆盖率: {s['coverage']}%")
            print()


# ────────────────────────────────────────────────
# 入口
# ────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="龍魂审计状态汇总")
    parser.add_argument("--full", action="store_true", help="输出详细信息")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument(
        "--audit-log", default=str(AUDIT_LOG),
        help="指定 audit_log.jsonl 路径"
    )
    parser.add_argument(
        "--test-log", default=str(TEST_LOG),
        help="指定 test_log.jsonl 路径"
    )
    args = parser.parse_args()

    if args.audit_log != str(AUDIT_LOG):
        AUDIT_LOG = Path(args.audit_log)
    if args.test_log != str(TEST_LOG):
        TEST_LOG = Path(args.test_log)

    if args.json:
        audit_records = load_jsonl(AUDIT_LOG)
        test_records  = load_jsonl(TEST_LOG)
        result = {}
        for key, name in DIMENSIONS:
            if key == "test":
                result[key] = compute_test_status(test_records)
            else:
                result[key] = compute_dim_status(audit_records, key)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_status(full=args.full)
