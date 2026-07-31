# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧮 龍魂公式系统性能基准测试 · 无审计模式

对比：
  ✅ 有审计（默认）vs 无审计（本测试）
  ✅ 展现优化的真实效果
  ✅ 验证增量哈希·缓存·向量化·熔断的性能收益

DNA:#龍芯⚡️2026-06-08-BENCHMARK-NO-AUDIT-FILE5-v2.0
"""

import time
from typing import Dict, Tuple, Any
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

# ═════════ 导入并禁用审计 ═════════
try:
    from formula_core_v2 import (
        digital_root, dr_gate, entropy, normalize, cosine,
        truth_score, truth_total, soul_score, magic_ok,
        hash_chain, IncrementalHashChain,
        set_config, _audit
    )
    # 关键：禁用审计
    set_config("enable_audit_log", False)
    set_config("dna_mode", "off")
    HAS_V2_CORE = True
except Exception as e:
    print(f"❌ 导入失败: {e}")
    HAS_V2_CORE = False

try:
    from formula_chain_v2 import (
        five_element, sovereignty_index, decision_chain as decision_chain_v2,
        set_chain_config
    )
    set_chain_config("enable_audit", False)
    HAS_V2_CHAIN = True
except Exception as e:
    print(f"❌ Chain 导入失败: {e}")
    HAS_V2_CHAIN = False

# 同时导入 v1.0 用于对比
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "formula_core_v1",
        os.path.join(os.path.dirname(__file__), "formula_core.py")
    )
    formula_core_v1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(formula_core_v1)
    HAS_V1_CORE = True
except:
    HAS_V1_CORE = False

try:
    spec = importlib.util.spec_from_file_location(
        "formula_chain_v1",
        os.path.join(os.path.dirname(__file__), "formula_chain.py")
    )
    formula_chain_v1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(formula_chain_v1)
    HAS_V1_CHAIN = True
except:
    HAS_V1_CHAIN = False

# ═════════ 性能测试工具 ═════════
class NoAuditBenchmark:
    """无审计模式的基准测试"""

    def measure(self, func, *args, **kwargs) -> Tuple[float, any]:
        """高精度计时"""
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - t0) * 1000  # ms
        return elapsed, result

    def run_test(self, name: str, func, iterations: int, *args, **kwargs) -> Dict[str, Any]:
        """运行多次测试"""
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
        }

    def compare(self, name: str, func_v1, func_v2, iterations: int, *args, **kwargs) -> Dict[str, Any]:
        """对比 v1.0 和 v2.0"""
        result_v1 = self.run_test(f"{name} (v1.0)", func_v1, iterations, *args, **kwargs)
        result_v2 = self.run_test(f"{name} (v2.0)", func_v2, iterations, *args, **kwargs)

        speedup = result_v1["avg_ms"] / result_v2["avg_ms"] if result_v2["avg_ms"] > 0 else 0
        improvement = (1 - result_v2["avg_ms"] / result_v1["avg_ms"]) * 100

        return {
            "test": name,
            "v1.0_avg": result_v1["avg_ms"],
            "v2.0_avg": result_v2["avg_ms"],
            "speedup": speedup,
            "improvement_pct": improvement,
            "v1.0_total": result_v1["total_ms"],
            "v2.0_total": result_v2["total_ms"],
        }

# ═════════ 核心层测试（无审计） ═════════
def benchmark_core_no_audit():
    """Core 层·无审计模式"""
    print("\n" + "=" * 100)
    print("【Core 层性能基准测试·无审计模式】")
    print("=" * 100)

    benchmark = NoAuditBenchmark()
    results = []

    if not (HAS_V1_CORE and HAS_V2_CORE):
        print("⚠️ 无法进行 Core 层测试")
        return results

    # 1. 数字根（1000x）
    print("\n1️⃣ 数字根（1000 次）")
    comp = benchmark.compare(
        "digital_root",
        formula_core_v1.digital_root,
        digital_root,
        1000,
        20260603
    )
    results.append(comp)
    print(f"   v1.0: {comp['v1.0_avg']:.4f}ms | v2.0: {comp['v2.0_avg']:.4f}ms | 加速: {comp['speedup']:.2f}x")

    # 2. 三色闸（1000x）
    print("2️⃣ 三色闸（1000 次）")
    comp = benchmark.compare(
        "dr_gate",
        formula_core_v1.dr_gate,
        dr_gate,
        1000,
        12
    )
    results.append(comp)
    print(f"   v1.0: {comp['v1.0_avg']:.4f}ms | v2.0: {comp['v2.0_avg']:.4f}ms | 加速: {comp['speedup']:.2f}x")

    # 3. 信息熵（100x）
    print("3️⃣ 信息熵（100 次）")
    comp = benchmark.compare(
        "entropy",
        formula_core_v1.entropy,
        entropy,
        100,
        [0.25, 0.25, 0.25, 0.25]
    )
    results.append(comp)
    print(f"   v1.0: {comp['v1.0_avg']:.4f}ms | v2.0: {comp['v2.0_avg']:.4f}ms | 加速: {comp['speedup']:.2f}x")

    # 4. 权重归一化·重复查询（最重点）
    print("4️⃣ 权重归一化·相同输入 1000 次（LRU 缓存）")
    comp = benchmark.compare(
        "normalize(same)",
        formula_core_v1.normalize,
        normalize,
        1000,
        [1, 1, 2]
    )
    results.append(comp)
    speedup_str = f"{comp['speedup']:.0f}x ⚡⚡⚡" if comp['speedup'] > 10 else f"{comp['speedup']:.1f}x"
    print(f"   v1.0: {comp['v1.0_avg']:.4f}ms | v2.0: {comp['v2.0_avg']:.4f}ms | 加速: {speedup_str}")

    # 5. Cosine 相似度（100x）
    print("5️⃣ Cosine 相似度（100 次）")
    comp = benchmark.compare(
        "cosine",
        formula_core_v1.cosine,
        cosine,
        100,
        [1, 0, 0, 1], [0, 1, 1, 0]
    )
    results.append(comp)
    print(f"   v1.0: {comp['v1.0_avg']:.4f}ms | v2.0: {comp['v2.0_avg']:.4f}ms | 改进: {comp['improvement_pct']:.1f}%")

    # 6. Truth Total（100 行·向量化测试）
    print("6️⃣ Truth Total（100 行）")
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
    speedup_str = f"{comp['speedup']:.1f}x ⚡" if comp['speedup'] > 1.5 else f"{comp['speedup']:.2f}x"
    print(f"   v1.0: {comp['v1.0_avg']:.4f}ms | v2.0: {comp['v2.0_avg']:.4f}ms | 加速: {speedup_str}")

    # 7. 哈希链·1000 事件（最重点）
    print("7️⃣ 哈希链·1000 事件（增量优化·O(n²)→O(n)）")
    events = [f"event_{i}" for i in range(1000)]
    comp = benchmark.compare(
        "hash_chain(1000)",
        formula_core_v1.hash_chain,
        hash_chain,
        10,
        events
    )
    results.append(comp)
    speedup_str = f"{comp['speedup']:.0f}x ⚡⚡⚡⚡" if comp['speedup'] > 100 else f"{comp['speedup']:.1f}x"
    print(f"   v1.0: {comp['v1.0_total']:.2f}ms 总 | v2.0: {comp['v2.0_total']:.2f}ms 总 | 加速: {speedup_str}")

    # 8. 洛书守恒（无优化·基线）
    print("8️⃣ 洛书守恒（基线·无优化）")
    comp = benchmark.compare(
        "magic_ok",
        formula_core_v1.magic_ok,
        magic_ok,
        1000
    )
    results.append(comp)
    print(f"   v1.0: {comp['v1.0_avg']:.6f}ms | v2.0: {comp['v2.0_avg']:.6f}ms | 性能: 持平")

    return results

# ═════════ Chain 层测试（无审计） ═════════
def benchmark_chain_no_audit():
    """Chain 层·无审计模式"""
    print("\n" + "=" * 100)
    print("【Chain 层性能基准测试·无审计模式】")
    print("=" * 100)

    benchmark = NoAuditBenchmark()
    results = []

    if not (HAS_V1_CHAIN and HAS_V2_CHAIN):
        print("⚠️ 无法进行 Chain 层测试")
        return results

    # 1. 五行映射（1000x 相同）
    print("\n1️⃣ 五行映射·相同输入 1000 次（LRU 缓存）")
    comp = benchmark.compare(
        "five_element(same)",
        formula_chain_v1.five_element,
        five_element,
        1000,
        1
    )
    results.append(comp)
    speedup_str = f"{comp['speedup']:.0f}x ⚡" if comp['speedup'] > 10 else f"{comp['speedup']:.1f}x"
    print(f"   v1.0: {comp['v1.0_avg']:.4f}ms | v2.0: {comp['v2.0_avg']:.4f}ms | 加速: {speedup_str}")

    # 2. SI 计算（1000x 相同）
    print("2️⃣ 三才 SI·相同参数 1000 次（键值缓存）")
    comp = benchmark.compare(
        "sovereignty_index(same)",
        lambda: formula_chain_v1.sovereignty_index(0.9, 0.9, 0.9),
        lambda: sovereignty_index(0.9, 0.9, 0.9),
        1000
    )
    results.append(comp)
    speedup_str = f"{comp['speedup']:.0f}x ⚡⚡⚡" if comp['speedup'] > 100 else f"{comp['speedup']:.1f}x"
    print(f"   v1.0: {comp['v1.0_avg']:.4f}ms | v2.0: {comp['v2.0_avg']:.4f}ms | 加速: {speedup_str}")

    # 3. 决策链·快速熔断（100x）
    print("3️⃣ 决策链·快速熔断（dr=3 红数字根）")
    comp = benchmark.compare(
        "decision_chain(fuse)",
        lambda: formula_chain_v1.decision_chain(12, [0.1, 0.1], [1, 1]),
        lambda: decision_chain_v2(12, [0.1, 0.1], [1, 1]),
        100
    )
    results.append(comp)
    speedup_str = f"{comp['speedup']:.0f}x ⚡⚡⚡" if comp['speedup'] > 100 else f"{comp['speedup']:.1f}x"
    print(f"   v1.0: {comp['v1.0_avg']:.4f}ms | v2.0: {comp['v2.0_avg']:.4f}ms | 加速: {speedup_str}")

    # 4. 决策链·完整流程（100x）
    print("4️⃣ 决策链·完整流程（六环全过）")
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
    speedup_str = f"{comp['speedup']:.1f}x ⚡" if comp['speedup'] > 1.2 else f"{comp['speedup']:.2f}x"
    print(f"   v1.0: {comp['v1.0_avg']:.4f}ms | v2.0: {comp['v2.0_avg']:.4f}ms | 加速: {speedup_str}")

    # 5. 决策链·天轴熔断（100x）
    print("5️⃣ 决策链·天轴熔断（天<0.34）")
    comp = benchmark.compare(
        "decision_chain(veto)",
        lambda: formula_chain_v1.decision_chain(
            20260603, [0.05, 0.05], [1, 1], 0.2, 0.9, 0.9
        ),
        lambda: decision_chain_v2(
            20260603, [0.05, 0.05], [1, 1], 0.2, 0.9, 0.9
        ),
        100
    )
    results.append(comp)
    speedup_str = f"{comp['speedup']:.1f}x ⚡" if comp['speedup'] > 1.2 else f"{comp['speedup']:.2f}x"
    print(f"   v1.0: {comp['v1.0_avg']:.4f}ms | v2.0: {comp['v2.0_avg']:.4f}ms | 加速: {speedup_str}")

    return results

# ═════════ 批量操作测试 ═════════
def benchmark_batch_no_audit():
    """批量操作·无审计"""
    print("\n" + "=" * 100)
    print("【批量操作性能测试·无审计模式】")
    print("=" * 100)

    if not HAS_V2_CHAIN:
        print("⚠️ 无法进行批量测试")
        return

    print("\n1️⃣ 批量决策·1000 决策（混合：50% 熔断 + 50% 完整）")
    t0 = time.perf_counter()
    for i in range(500):
        decision_chain_v2(12, [0.1, 0.1], [1, 1])
    for i in range(500):
        decision_chain_v2(20260603, [0.05, 0.05], [1, 1], 0.9, 0.85, 0.8)
    elapsed = (time.perf_counter() - t0) * 1000

    print(f"   耗时: {elapsed:.2f}ms（1000 决策）")
    print(f"   平均: {elapsed/1000:.4f}ms/决策")
    print(f"   吞吐量: {1000/(elapsed/1000):.0f} 决策/秒 ⚡")

    print("\n2️⃣ 相同 SI 查询·1000 次（测试键值缓存效果）")
    five_element.cache_clear()
    sovereignty_index(0.9, 0.9, 0.9)  # 预热

    t0 = time.perf_counter()
    for i in range(1000):
        sovereignty_index(0.9, 0.9, 0.9)
    elapsed = (time.perf_counter() - t0) * 1000

    print(f"   耗时: {elapsed:.2f}ms（1000 次）")
    print(f"   平均: {elapsed/1000:.6f}ms/次")
    print(f"   吞吐量: {1000/(elapsed/1000):.0f} 次/秒 ⚡⚡⚡")

# ═════════ 主程序 ═════════
def main():
    """执行完整基准测试"""
    print("\n" + "=" * 100)
    print("🧮 龍魂公式系统性能基准测试·无审计模式")
    print("=" * 100)

    print(f"\n【配置】")
    print(f"  enable_audit_log: False")
    print(f"  dna_mode: off")
    print(f"  计时精度: perf_counter（微秒）")

    # Core 层
    core_results = benchmark_core_no_audit()

    # Chain 层
    chain_results = benchmark_chain_no_audit()

    # 批量
    benchmark_batch_no_audit()

    # 总结
    print("\n" + "=" * 100)
    print("【性能总结】")
    print("=" * 100)

    all_results = core_results + chain_results
    if all_results:
        speedups = [r["speedup"] for r in all_results if r["speedup"] > 0]
        print(f"\n{len(all_results)} 项对比·加速倍数统计:")
        print(f"  最大: {max(speedups):.0f}x ⚡")
        print(f"  最小: {min(speedups):.2f}x")
        print(f"  平均: {sum(speedups)/len(speedups):.1f}x")

        # 列出加速最明显的项
        print("\n【最高加速项目】")
        top_3 = sorted(all_results, key=lambda x: x["speedup"], reverse=True)[:3]
        for i, r in enumerate(top_3, 1):
            print(f"  {i}. {r['test']}: {r['speedup']:.0f}x")

    print("\n" + "=" * 100)
    print("✅ 无审计模式基准测试完成")
    print("=" * 100)

if __name__ == "__main__":
    main()
