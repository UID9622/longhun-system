#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·乙亥·巳时·䷝离-BENCHMARK-v1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 协议配套: docs/对外接口协议-v1.0.md
"""
🐉 龍魂性能基准 v1.0 — lh benchmark [--iterations 1000] [--json]

测试:
  1. bazi 排盘   迭代 N 次（标准四柱算法·口径同薄壳 core.bazi）
  2. flow 流场   迭代 N 次（数字根压缩·口径同薄壳 core.flow）
  3. 网关 QPS    GET http://127.0.0.1:9622/health 串行 N 次（网关未启动 → skipped）

输出: 平均/最大/最小耗时(ms) + QPS（每项独立统计）。
"""

import argparse
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACK = ROOT / "packaging" / "longhun_cli"
sys.path.insert(0, str(PACK))
from longhun_cli.core import bazi, flow  # noqa: E402

GATEWAY_HEALTH = "http://127.0.0.1:9622/health"


def _node_id(text: str) -> str:
    return f"BENCH-9622-{hashlib.sha256(text.encode()).hexdigest()[:8].upper()}"


def _stats(times: list[float]) -> dict:
    n = len(times)
    total = sum(times)
    avg = total / n if n else 0.0
    return {
        "iterations": n,
        "avg_ms": round(avg, 3),
        "max_ms": round(max(times, default=0.0), 3),
        "min_ms": round(min(times, default=0.0), 3),
        "qps": round(n / total, 1) if total else 0.0,
    }


def bench_bazi(n: int) -> dict:
    times: list[float] = []
    for i in range(n):
        t0 = time.perf_counter()
        bazi("1990-01-01", "08:00")
        times.append((time.perf_counter() - t0) * 1000)
    return {"name": "bazi 排盘", **_stats(times)}


def bench_flow(n: int) -> dict:
    times: list[float] = []
    for _ in range(n):
        t0 = time.perf_counter()
        flow("龙魂对外首发")
        times.append((time.perf_counter() - t0) * 1000)
    return {"name": "flow 流场", **_stats(times)}


def bench_gateway(n: int) -> dict:
    times: list[float] = []
    try:
        with urllib.request.urlopen(GATEWAY_HEALTH, timeout=3) as r:
            r.read()
    except Exception:  # noqa: BLE001
        return {"name": "网关 QPS", "iterations": 0, "avg_ms": 0.0,
                "max_ms": 0.0, "min_ms": 0.0, "qps": 0.0,
                "skipped": "网关未启动（lh api --daemon 可启动）"}
    for _ in range(n):
        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(GATEWAY_HEALTH, timeout=5) as r:
                r.read()
        except Exception:  # noqa: BLE001
            continue
        times.append((time.perf_counter() - t0) * 1000)
    if not times:
        return {"name": "网关 QPS", "iterations": 0, "avg_ms": 0.0,
                "max_ms": 0.0, "min_ms": 0.0, "qps": 0.0, "skipped": "全部请求失败"}
    return {"name": "网关 QPS", **_stats(times)}


def main() -> None:
    ap = argparse.ArgumentParser(prog="lh benchmark", description="龍魂性能基准")
    ap.add_argument("--iterations", type=int, default=1000, help="每项迭代次数 (默认 1000)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    n = max(1, min(args.iterations, 20000))

    tests = [bench_bazi(n), bench_flow(n), bench_gateway(min(n, 200))]
    total_t = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    node = _node_id(json.dumps(tests))
    data = {
        "status": "ok",
        "node_id": node,
        "iterations": n,
        "tests": tests,
        "timestamp": total_t,
    }
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print("⚡ 龍魂性能基准")
        for t in tests:
            if t.get("skipped"):
                print(f"  {t['name']}: {t['skipped']}")
            else:
                print(f"  {t['name']}: avg={t['avg_ms']}ms max={t['max_ms']}ms "
                      f"min={t['min_ms']}ms qps={t['qps']}")


if __name__ == "__main__":
    main()
