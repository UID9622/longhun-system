#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂低算力内核 · 基准测试脚本
复现实测数据 · 纯标准库 · 零网络依赖

DNA: #龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-BENCHMARK-UID9622
License: MulanPSL v2

运行: python3 tools/benchmark_lowpower.py
"""

import sys
import os
import time as _time
import json
import hashlib
import platform
from datetime import datetime

# 添加 core/ 到路径
_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent not in sys.path:
    sys.path.insert(0, _parent)

from core.longhun_core import (
    DNAEngine, TricolorAudit, YearRingChain,
    DigitalRoot, compute_root,
    create_rate_limiter,
)


DIVIDER = "═" * 60


def measure(label, count, fn):
    """运行基准测试并返回统计"""
    # 预热
    for _ in range(min(100, count // 10)):
        fn()

    t0 = _time.perf_counter()
    for _ in range(count):
        fn()
    t1 = _time.perf_counter()

    elapsed = t1 - t0
    rate = count / elapsed if elapsed > 0 else 0

    return {
        "label": label,
        "count": count,
        "elapsed_s": round(elapsed, 4),
        "rate_per_sec": round(rate, 0),
        "us_per_op": round(elapsed / count * 1_000_000, 2) if count > 0 else 0,
    }


def main():
    print(DIVIDER)
    print("🐉 龍魂低算力内核 · 实测报告")
    print("治大国若烹小鲜。——《道德经》第60章")
    print(DIVIDER)
    print(f"平台:  {platform.platform()}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"时间:  {datetime.now().isoformat()}")
    print(f"DNA:   #龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-BENCH-UID9622")
    print(DIVIDER)
    print()

    results = []

    # === 1. DNA 签发吞吐 ===
    engine = DNAEngine()
    r = measure("DNA签发吞吐", 50000, lambda: engine.stamp(module="B", action="T"))
    results.append(r)
    print(f"📊 {r['label']}: {r['rate_per_sec']:,.0f} 条/秒 ({r['elapsed_s']}s · {r['us_per_op']}μs/条)")

    # === 2. 年轮链落笔 ===
    chain = YearRingChain(name="bench")
    counter = [0]
    def write_one():
        chain.write({"id": f"b{counter[0]}", "val": counter[0]})
        counter[0] += 1
    r = measure("年轮链落笔", 15000, write_one)
    results.append(r)
    print(f"📊 {r['label']}: {r['rate_per_sec']:,.0f} 条/秒 ({r['elapsed_s']}s · {r['us_per_op']}μs/条)")

    # === 3. 流控token吞吐 ===
    bucket = create_rate_limiter(tps=9999999, burst=9999999)
    r = measure("流控token吞吐", 500000, lambda: bucket.try_consume(1))
    results.append(r)
    print(f"📊 {r['label']}: {r['rate_per_sec']:,.0f} token/秒 ({r['elapsed_s']}s · {r['us_per_op']}μs/条)")

    # === 4. 审计批量 ===
    auditor = TricolorAudit()
    data = {"阻塞率": 0.02, "耗时_ms": 120, "错误率": 0.005}
    r = measure("审计批量评估", 50000, lambda: auditor.quick_eval(data))
    results.append(r)
    print(f"📊 {r['label']}: {r['rate_per_sec']:,.0f} 条/秒 ({r['elapsed_s']}s · {r['us_per_op']}μs/条)")

    # === 5. 数字根计算 ===
    nums = list(range(50000))
    idx = [0]
    def root_one():
        compute_root(nums[idx[0] % len(nums)])
        idx[0] += 1
    r = measure("数字根计算", 100000, root_one)
    results.append(r)
    print(f"📊 {r['label']}: {r['rate_per_sec']:,.0f} 次/秒 ({r['elapsed_s']}s · {r['us_per_op']}μs/条)")

    # === 6. 内存估算 ===
    print()
    print(DIVIDER)
    print("📊 内存实测")
    print(DIVIDER)

    import sys as _sys

    # 空审计器
    auditor2 = TricolorAudit()
    auditor_size = _sys.getsizeof(auditor2) + sum(
        _sys.getsizeof(ch) for ch in auditor2._checkers
    )
    print(f"  内核增量内存:      ~{auditor_size} bytes (~0 MB)")
    print(f"  年轮链 15000 条:    ~{_sys.getsizeof(chain.chain)} bytes (列表引用)")
    print(f"  流控桶对象:         ~{_sys.getsizeof(bucket)} bytes")

    # 模拟 50000 条审计记录的内存
    records_5w = []
    for i in range(50000):
        records_5w.append({"tricolor": "🟢", "R": 90.5, "ts": i, "dna": "x" * 20})
    mem_5w = _sys.getsizeof(records_5w) + sum(_sys.getsizeof(r) for r in records_5w[:100]) * 500
    print(f"  5万条审计记录:      ~{mem_5w / 1024 / 1024:.1f} MB (估算)")

    # === 7. 总结 ===
    print()
    print(DIVIDER)
    print("📊 总结")
    print(DIVIDER)

    summary = {
        "timestamp": datetime.now().isoformat(),
        "platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "dna": "#龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-BENCH-UID9622",
        "results": results,
        "network_dependency": "零（纯标准库·断网可跑）",
        "source_code_size": "~10KB (压缩后)",
        "license": "工程层 MulanPSL v2 · 思想层 CC BY-NC-SA 4.0",
    }

    for r in results:
        print(f"  {r['label']}: {r['rate_per_sec']:,.0f} 次/秒")

    print()
    print("🟢 大厂告诉你：算力=智能。龍魂告诉你：你随时可以验证我说的话。")
    print(DIVIDER)

    # 保存结果
    report_path = os.path.join(os.path.dirname(__file__), "benchmark_result.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"\n📄 结果已保存: {report_path}")


if __name__ == "__main__":
    main()
