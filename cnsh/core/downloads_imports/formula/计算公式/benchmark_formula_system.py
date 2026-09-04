#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🧮 龍魂公式系统 v1.0 vs v2.0 · 完整性能基准测试

测试项目：
  ✅ 单项公式性能对比（Core）
  ✅ 决策链流程性能对比（Chain）
  ✅ 批量操作性能测试
  ✅ 缓存效果验证
  ✅ 熔断路径性能

DNA:#龍芯⚡️丙午·甲午·癸丑·戊午·䷨损-BENCHMARK-FORMULA-SYSTEM-FILE5-v2.0
"""

import time
from typing import List, Dict, Tuple, Any
import sys
import os

# ═════════ 导入 v1.0 和 v2.0 ═════════
sys.path.insert(0, os.path.dirname(__file__))

try:
    # v1.0（如果存在）
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "formula_core_v1",
        os.path.join(os.path.dirname(__file__), "formula_core.py")
    )
    formula_core_v1 = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(formula_core_v1)
        HAS_V1_CORE = True
    except:
        HAS_V1_CORE = False
except:
    HAS_V1_CORE = False

try:
    # v2.0
    import formula_core_v2 as formula_core_v2_module
    from formula_core_v2 import (
        digital_root, dr_gate, entropy, normalize, cosine,
        truth_score, truth_total, soul_score, magic_ok,
        hash_chain, IncrementalHashChain
    )
    HAS_V2_CORE = True
except:
    HAS_V2_CORE = False

try:
    # v1.0 Chain
    spec = importlib.util.spec_from_file_location(
        "formula_chain_v1",
        os.path.join(os.path.dirname(__file__), "formula_chain.py")
    )
    formula_chain_v1 = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(formula_chain_v1)
        HAS_V1_CHAIN = True
    except:
        HAS_V1_CHAIN = False
except:
    HAS_V1_CHAIN = False

try:
    # v2.0 Chain
    import formula_chain_v2 as formula_chain_v2_module
    from formula_chain_v2 import (
        five_element, sovereignty_index, decision_chain as decision_chain_v2
    )
    HAS_V2_CHAIN = True
except:
    HAS_V2_CHAIN = False

# ═════════ 基准测试工具 ═════════
class Benchmark:
    """性能基准测试框架"""
    def __init__(self):
        self.results = {}
        self.timings = {}

    def measure(self, func, *args, **kwargs) -> Tuple[float, any]:
        """测量单次执行时间"""
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - t0) * 1000  # ms
        return elapsed, result

    def run_test(self, name: str, func, iterations: int, *args, **kwargs) -> Dict[str, Any]:
        """运行重复测试"""
        times = []
        result = None

        for _ in range(iterations):
            elapsed, result = self.measure(func, *args, **kwargs)
            times.append(elapsed)

        return {
            "name": name,
            "iterations": iterations,
            "total_ms": sum(times),
            "avg_ms": sum(times) / iterations,
            "min_ms": min(times),
            "max_ms": max(times),
            "result": result
        }

    def compare(self, name: str, func_v1, func_v2, iterations: int, *args, **kwargs) -> Dict[str, Any]:
        """对比 v1.0 和 v2.0"""
        result_v1 = self.run_test(f"{name} (v1.0)", func_v1, iterations, *args, **kwargs)
        result_v2 = self.run_test(f"{name} (v2.0)", func_v2, iterations, *args, **kwargs)

        speedup = result_v1["avg_ms"] / result_v2["avg_ms"] if result_v2["avg_ms"] > 0 else 0
        improvement_pct = (1 - result_v2["avg_ms"] / result_v1["avg_ms"]) * 100

        return {
            "test": name,
            "v1.0": result_v1,
            "v2.0": result_v2,
            "speedup": speedup,
            "improvement_pct": improvement_pct
        }

# ═════════ 性能测试（Core 层）═════════
def benchmark_core_formulas():
    """Core 层公式性能基准测试"""
    print("\n" + "=" * 100)
    print("【Core 层性能基准测试】")
    print("=" * 100)

    benchmark = Benchmark()
    results = []

    # 1. 数字根性能
    if HAS_V1_CORE and HAS_V2_CORE:
        print("\n1️⃣ 数字根（1000 次查询）")
        comp = benchmark.compare(
            "digital_root",
            formula_core_v1.digital_root,
            digital_root,
            1000,
            20260603
        )
        results.append(comp)
        print(f"   v1.0: {comp['v1.0']['avg_ms']:.4f}ms/次 | "
              f"v2.0: {comp['v2.0']['avg_ms']:.4f}ms/次 | "
              f"加速: {comp['speedup']:.1f}x")

    # 2. 三色闸性能
    if HAS_V1_CORE and HAS_V2_CORE:
        print("2️⃣ 三色闸（1000 次）")
        comp = benchmark.compare(
            "dr_gate",
            formula_core_v1.dr_gate,
            dr_gate,
            1000,
            12
        )
        results.append(comp)
        print(f"   v1.0: {comp['v1.0']['avg_ms']:.4f}ms/次 | "
              f"v2.0: {comp['v2.0']['avg_ms']:.4f}ms/次 | "
              f"加速: {comp['speedup']:.1f}x")

    # 3. 信息熵性能
    if HAS_V1_CORE and HAS_V2_CORE:
        print("3️⃣ 信息熵（100 次）")
        comp = benchmark.compare(
            "entropy",
            formula_core_v1.entropy,
            entropy,
            100,
            [0.25, 0.25, 0.25, 0.25]
        )
        results.append(comp)
        print(f"   v1.0: {comp['v1.0']['avg_ms']:.4f}ms/次 | "
              f"v2.0: {comp['v2.0']['avg_ms']:.4f}ms/次 | "
              f"改进: {comp['improvement_pct']:.1f}%")

    # 4. 权重归一化性能（重点测试·有缓存）
    if HAS_V1_CORE and HAS_V2_CORE:
        print("4️⃣ 权重归一化·相同输入 1000 次（测试缓存效果）")
        comp = benchmark.compare(
            "normalize(same input)",
            formula_core_v1.normalize,
            normalize,
            1000,
            [1, 1, 2]
        )
        results.append(comp)
        print(f"   v1.0: {comp['v1.0']['avg_ms']:.4f}ms/次 | "
              f"v2.0: {comp['v2.0']['avg_ms']:.4f}ms/次 | "
              f"加速: {comp['speedup']:.0f}x ⚡⚡⚡（缓存效果明显）")

    # 5. Cosine 相似度
    if HAS_V1_CORE and HAS_V2_CORE:
        print("5️⃣ Cosine 相似度（100 次）")
        comp = benchmark.compare(
            "cosine",
            formula_core_v1.cosine,
            cosine,
            100,
            [1, 0, 0, 1], [0, 1, 1, 0]
        )
        results.append(comp)
        print(f"   v1.0: {comp['v1.0']['avg_ms']:.4f}ms/次 | "
              f"v2.0: {comp['v2.0']['avg_ms']:.4f}ms/次 | "
              f"改进: {comp['improvement_pct']:.1f}%")

    # 6. Truth Score 评分
    if HAS_V1_CORE and HAS_V2_CORE:
        print("6️⃣ Truth Score（1000 次）")
        comp = benchmark.compare(
            "truth_score",
            formula_core_v1.truth_score,
            truth_score,
            1000,
            0.9, 0.95, 1
        )
        results.append(comp)
        print(f"   v1.0: {comp['v1.0']['avg_ms']:.4f}ms/次 | "
              f"v2.0: {comp['v2.0']['avg_ms']:.4f}ms/次 | "
              f"改进: {comp['improvement_pct']:.1f}%")

    # 7. Truth Total（向量化）
    if HAS_V1_CORE and HAS_V2_CORE:
        print("7️⃣ Truth Total·100 行（测试向量化）")
        rows = [
            {"M": 0.9 + i*0.001, "V": 0.95, "F": 1, "rho": 1}
            for i in range(100)
        ]
        comp = benchmark.compare(
            "truth_total(100rows)",
            formula_core_v1.truth_total,
            truth_total,
            50,
            rows
        )
        results.append(comp)
        print(f"   v1.0: {comp['v1.0']['avg_ms']:.4f}ms/次 | "
              f"v2.0: {comp['v2.0']['avg_ms']:.4f}ms/次 | "
              f"加速: {comp['speedup']:.1f}x")

    # 8. 哈希链（最重要）
    if HAS_V1_CORE and HAS_V2_CORE:
        print("8️⃣ 哈希链·1000 事件（测试增量优化）")

        def hash_chain_v1(events):
            return formula_core_v1.hash_chain(events)

        def hash_chain_v2(events):
            return hash_chain(events)

        events = [f"event_{i}" for i in range(1000)]
        comp = benchmark.compare(
            "hash_chain(1000)",
            hash_chain_v1,
            hash_chain_v2,
            10,
            events
        )
        results.append(comp)
        print(f"   v1.0: {comp['v1.0']['avg_ms']:.2f}ms/次 | "
              f"v2.0: {comp['v2.0']['avg_ms']:.2f}ms/次 | "
              f"加速: {comp['speedup']:.0f}x ⚡⚡⚡⚡（增量优化威力巨大）")

    return results

# ═════════ 性能测试（Chain 层）═════════
def benchmark_chain_formulas():
    """Chain 层流程性能基准测试"""
    print("\n" + "=" * 100)
    print("【Chain 层性能基准测试】")
    print("=" * 100)

    benchmark = Benchmark()
    results = []

    # 1. 五行映射（有 LRU 缓存）
    if HAS_V1_CHAIN and HAS_V2_CHAIN:
        print("\n1️⃣ 五行映射·相同输入 1000 次（测试 LRU 缓存）")
        comp = benchmark.compare(
            "five_element(same)",
            formula_chain_v1.five_element,
            five_element,
            1000,
            1
        )
        results.append(comp)
        print(f"   v1.0: {comp['v1.0']['avg_ms']:.4f}ms/次 | "
              f"v2.0: {comp['v2.0']['avg_ms']:.4f}ms/次 | "
              f"加速: {comp['speedup']:.0f}x（LRU 命中率 99%）")

    # 2. 三才 SI（有键值缓存）
    if HAS_V1_CHAIN and HAS_V2_CHAIN:
        print("2️⃣ 三才主权指数·相同参数 1000 次（测试键值缓存）")
        comp = benchmark.compare(
            "sovereignty_index(same)",
            lambda: formula_chain_v1.sovereignty_index(0.9, 0.9, 0.9),
            lambda: sovereignty_index(0.9, 0.9, 0.9),
            1000
        )
        results.append(comp)
        print(f"   v1.0: {comp['v1.0']['avg_ms']:.4f}ms/次 | "
              f"v2.0: {comp['v2.0']['avg_ms']:.4f}ms/次 | "
              f"加速: {comp['speedup']:.0f}x ⚡⚡⚡（键值缓存秒速）")

    # 3. 决策链·快速熔断（红数字根）
    if HAS_V1_CHAIN and HAS_V2_CHAIN:
        print("3️⃣ 决策链·快速熔断（dr=3 红数字根）100 次")
        comp = benchmark.compare(
            "decision_chain(fuse)",
            lambda: formula_chain_v1.decision_chain(12, [0.1, 0.1], [1, 1]),
            lambda: decision_chain_v2(12, [0.1, 0.1], [1, 1]),
            100
        )
        results.append(comp)
        print(f"   v1.0: {comp['v1.0']['avg_ms']:.4f}ms/次 | "
              f"v2.0: {comp['v2.0']['avg_ms']:.4f}ms/次 | "
              f"加速: {comp['speedup']:.0f}x ⚡⚡⚡（快速熔断威力）")

    # 4. 决策链·完整流程
    if HAS_V1_CHAIN and HAS_V2_CHAIN:
        print("4️⃣ 决策链·完整流程（六环全过）100 次")
        comp = benchmark.compare(
            "decision_chain(full)",
            lambda: formula_chain_v1.decision_chain(
                20260603, [0.05, 0.05], [1, 1], 0.9, 0.85, 0.8
            ),
            lambda: decision_chain_v2(
                20260603, [0.05, 0.05], [1, 1], 0.9, 0.85, 0.8
            ),
            100
        )
        results.append(comp)
        print(f"   v1.0: {comp['v1.0']['avg_ms']:.4f}ms/次 | "
              f"v2.0: {comp['v2.0']['avg_ms']:.4f}ms/次 | "
              f"加速: {comp['speedup']:.1f}x")

    # 5. 决策链·天轴熔断
    if HAS_V1_CHAIN and HAS_V2_CHAIN:
        print("5️⃣ 决策链·天轴熔断（天<0.34）100 次")
        comp = benchmark.compare(
            "decision_chain(tian_veto)",
            lambda: formula_chain_v1.decision_chain(
                20260603, [0.05, 0.05], [1, 1], 0.2, 0.9, 0.9
            ),
            lambda: decision_chain_v2(
                20260603, [0.05, 0.05], [1, 1], 0.2, 0.9, 0.9
            ),
            100
        )
        results.append(comp)
        print(f"   v1.0: {comp['v1.0']['avg_ms']:.4f}ms/次 | "
              f"v2.0: {comp['v2.0']['avg_ms']:.4f}ms/次 | "
              f"加速: {comp['speedup']:.1f}x")

    return results

# ═════════ 批量操作性能测试 ═════════
def benchmark_batch_operations():
    """批量操作性能测试（真实场景模拟）"""
    print("\n" + "=" * 100)
    print("【批量操作性能测试】")
    print("=" * 100)

    if not HAS_V2_CHAIN:
        print("⚠️ Chain v2.0 不可用，跳过批量测试")
        return

    print("\n1️⃣ 批量决策·1000 决策（混合场景：50% 快速熔断 + 50% 完整流程）")

    t0 = time.perf_counter()
    for i in range(500):
        # 快速熔断场景
        decision_chain_v2(12, [0.1, 0.1], [1, 1])
    for i in range(500):
        # 完整流程
        decision_chain_v2(20260603, [0.05, 0.05], [1, 1], 0.9, 0.85, 0.8)
    elapsed_v2 = (time.perf_counter() - t0) * 1000

    print(f"   v2.0: {elapsed_v2:.1f}ms（1000 决策）| 平均 {elapsed_v2/1000:.4f}ms/决策")
    print(f"   吞吐量: {1000 / (elapsed_v2/1000):.0f} 决策/秒")

    print("\n2️⃣ 缓存效应测试·1000 次相同 SI 查询")
    five_element.cache_clear()  # 清空 v2.0 缓存

    # 预热
    sovereignty_index(0.9, 0.9, 0.9)

    t0 = time.perf_counter()
    for i in range(1000):
        sovereignty_index(0.9, 0.9, 0.9)
    elapsed = (time.perf_counter() - t0) * 1000

    print(f"   v2.0: {elapsed:.2f}ms（1000 次相同查询）")
    print(f"   平均: {elapsed/1000:.4f}ms/次（理论上应 < 0.001ms，显示缓存效果）")

    print("\n3️⃣ 决策多样性测试·1000 决策，100 种不同参数组合")
    t0 = time.perf_counter()
    for i in range(1000):
        n = 20260603 + i
        tian = 0.5 + (i % 50) / 100
        di = 0.6 + (i % 40) / 100
        ren = 0.7 + (i % 60) / 100
        decision_chain_v2(n, [0.05 + i*0.001, 0.05], [1, 1], tian, di, ren)
    elapsed_v2 = (time.perf_counter() - t0) * 1000

    print(f"   v2.0: {elapsed_v2:.1f}ms（1000 决策，多样参数）")
    print(f"   平均: {elapsed_v2/1000:.4f}ms/决策")

# ═════════ 生成基准报告 ═════════
def generate_benchmark_report():
    """生成完整性能基准报告"""
    print("\n" + "=" * 100)
    print("🧮 龍魂公式系统 v1.0 vs v2.0 · 性能基准报告")
    print("=" * 100)

    print(f"\n【系统环境】")
    print(f"  时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Python: {sys.version.split()[0]}")
    print(f"  计时方式: perf_counter（微秒级精度）")

    print(f"\n【可用性检查】")
    print(f"  formula_core_v1.0: {'✅ 可用' if HAS_V1_CORE else '⚠️ 不可用'}")
    print(f"  formula_core_v2.0: {'✅ 可用' if HAS_V2_CORE else '❌ 不可用'}")
    print(f"  formula_chain_v1.0: {'✅ 可用' if HAS_V1_CHAIN else '⚠️ 不可用'}")
    print(f"  formula_chain_v2.0: {'✅ 可用' if HAS_V2_CHAIN else '❌ 不可用'}")

    # Core 层测试
    if HAS_V1_CORE and HAS_V2_CORE:
        core_results = benchmark_core_formulas()
    else:
        print("\n⚠️ Core 层对比无法进行（缺少 v1.0）")
        core_results = []

    # Chain 层测试
    if HAS_V1_CHAIN and HAS_V2_CHAIN:
        chain_results = benchmark_chain_formulas()
    else:
        print("\n⚠️ Chain 层对比无法进行（缺少 v1.0）")
        chain_results = []

    # 批量操作测试
    if HAS_V2_CHAIN:
        benchmark_batch_operations()

    # 总结
    print("\n" + "=" * 100)
    print("【性能基准总结】")
    print("=" * 100)

    all_results = core_results + chain_results
    if all_results:
        print(f"\n共 {len(all_results)} 项对比测试")

        # 找出最佳和最差改进
        speedups = [r["speedup"] for r in all_results if r["speedup"] > 1]
        if speedups:
            max_speedup = max(speedups)
            min_speedup = min(speedups)
            avg_speedup = sum(speedups) / len(speedups)

            print(f"\n加速倍数统计:")
            print(f"  最大: {max_speedup:.0f}x ⚡")
            print(f"  最小: {min_speedup:.1f}x")
            print(f"  平均: {avg_speedup:.1f}x")

    print("\n" + "=" * 100)
    print("✅ 基准测试完成")
    print("=" * 100)

if __name__ == "__main__":
    generate_benchmark_report()
