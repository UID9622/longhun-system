#!/usr/bin/env python3
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
龍魂公式系統 - 基準測試引擎
Benchmark Engine for Longhun Formula System

DNA: #龍芯⚡️2026-06-19-LONGHUN-BENCHMARK-v5.1
功能：Core層8項 + Chain層5項 + 批量測試3項 = 16個測試場景
"""

import time
import hashlib
import statistics
from typing import Callable, Dict, List, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class TestCategory(Enum):
    CORE = "Core層"
    CHAIN = "Chain層"
    BATCH = "批量測試"


@dataclass
class BenchmarkResult:
    """單項測試結果"""
    name: str
    category: TestCategory
    version: str  # "v1.0" or "v2.0"
    iterations: int
    total_time_ms: float
    avg_time_ms: float
    min_time_ms: float
    max_time_ms: float
    throughput_per_sec: float
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def ops_per_sec(self) -> float:
        """每秒操作數"""
        if self.avg_time_ms > 0:
            return 1000.0 / self.avg_time_ms
        return 0.0


class Timer:
    """高精度計時器 (微秒級)"""

    def __init__(self):
        self._start = 0.0
        self._end = 0.0

    def start(self):
        self._start = time.perf_counter()

    def stop(self) -> float:
        self._end = time.perf_counter()
        return (self._end - self._start) * 1000.0  # 轉為毫秒

    @property
    def elapsed_ms(self) -> float:
        return (self._end - self._start) * 1000.0


def run_benchmark(
    name: str,
    category: TestCategory,
    version: str,
    func: Callable,
    setup: Callable = None,
    iterations: int = 1000,
    warmup: int = 100,
    metadata: Dict[str, Any] = None
) -> BenchmarkResult:
    """
    執行基準測試

    Args:
        name: 測試名稱
        category: 測試分類
        version: 版本標記 (v1.0 / v2.0)
        func: 被測函數 (無參數)
        setup: 每次迭代前的設置函數
        iterations: 迭代次數
        warmup: 預熱次數
        metadata: 額外元數據
    """
    timer = Timer()
    times = []

    # 預熱階段 (排除 JIT / 緩存干擾)
    for _ in range(warmup):
        if setup:
            setup()
        func()

    # 正式測試
    for _ in range(iterations):
        if setup:
            setup()
        timer.start()
        func()
        times.append(timer.stop())

    total_time = sum(times)
    avg_time = statistics.mean(times)
    min_time = min(times)
    max_time = max(times)
    throughput = (iterations / total_time) * 1000.0 if total_time > 0 else 0.0

    return BenchmarkResult(
        name=name,
        category=category,
        version=version,
        iterations=iterations,
        total_time_ms=total_time,
        avg_time_ms=avg_time,
        min_time_ms=min_time,
        max_time_ms=max_time,
        throughput_per_sec=throughput,
        metadata=metadata or {}
    )


# ═══════════════════════════════════════════════════════════
# Core層 測試函數 (8項)
# ═══════════════════════════════════════════════════════════

def test_digital_root_v1(number: int = 20260603) -> int:
    """數字根 v1.0 - 基礎實現"""
    n = abs(number)
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


def test_digital_root_v2(number: int = 20260603) -> int:
    """數字根 v2.0 - 優化實現 (含審計模擬)"""
    n = abs(number)
    if n == 0:
        result = 0
    else:
        result = 1 + (n - 1) % 9
    # 模擬審計開銷 (DNA簽章 + 性能計時)
    _ = f"#龍芯⚡️dr-{hashlib.md5(str(number).encode()).hexdigest()[:8]}"
    return result


def test_tricolor_gate_v1(si: int = 5) -> str:
    """三色閘 v1.0 - 基礎實現"""
    colors = ["紅", "綠", "藍"]
    return colors[si % 3]


def test_tricolor_gate_v2(si: int = 5) -> str:
    """三色閘 v2.0 - 含審計實現"""
    colors = ["紅", "綠", "藍"]
    result = colors[si % 3]
    # 模擬審計開銷
    _ = f"#龍芯⚡️tg-{hashlib.md5(str(si).encode()).hexdigest()[:8]}"
    _ = time.perf_counter()  # 性能計時記錄
    return result


def test_weight_basic_v1(weights: List[float] = None) -> float:
    """權重計算 v1.0 - 基礎實現"""
    if weights is None:
        weights = [0.1, 0.15, 0.2, 0.25, 0.3]
    return sum(weights) / len(weights)


def test_weight_basic_v2(weights: List[float] = None) -> float:
    """權重計算 v2.0 - 含審計實現"""
    if weights is None:
        weights = [0.1, 0.15, 0.2, 0.25, 0.3]
    result = sum(weights) / len(weights)
    # 模擬審計開銷
    _ = f"#龍芯⚡️wb-{hashlib.md5(str(weights).encode()).hexdigest()[:8]}"
    return result


def test_weight_cached_v1(weights: List[float] = None) -> float:
    """權重(重複查詢) v1.0 - 無緩存"""
    if weights is None:
        weights = [0.1, 0.15]
    return sum(weights) / len(weights)


_weight_cache = {}


def test_weight_cached_v2(weights: List[float] = None) -> float:
    """權重(重複查詢) v2.0 - 有緩存"""
    if weights is None:
        weights = [0.1, 0.15]
    cache_key = tuple(weights)
    if cache_key in _weight_cache:
        return _weight_cache[cache_key]
    result = sum(weights) / len(weights)
    _weight_cache[cache_key] = result
    # 模擬審計開銷
    _ = f"#龍芯⚡️wc-{hashlib.md5(str(weights).encode()).hexdigest()[:8]}"
    return result


def test_si_index_v1(si: int = 5, max_val: int = 9) -> int:
    """SI索引 v1.0"""
    return si % max_val


def test_si_index_v2(si: int = 5, max_val: int = 9) -> int:
    """SI索引 v2.0 - 含審計"""
    result = si % max_val
    _ = f"#龍芯⚡️si-{hashlib.md5(str(si).encode()).hexdigest()[:8]}"
    return result


def test_number_pool_v1() -> int:
    """號碼池 v1.0"""
    pool = list(range(1, 50))
    return pool[0]


def test_number_pool_v2() -> int:
    """號碼池 v2.0 - 含審計"""
    pool = list(range(1, 50))
    result = pool[0]
    _ = f"#龍芯⚡️np-{hashlib.md5(str(pool[0]).encode()).hexdigest()[:8]}"
    return result


def test_formula_lookup_v1() -> str:
    """公式查找 v1.0"""
    formulas = {"dr": "digital_root", "tg": "tricolor_gate"}
    return formulas.get("dr")


def test_formula_lookup_v2() -> str:
    """公式查找 v2.0 - 含審計"""
    formulas = {"dr": "digital_root", "tg": "tricolor_gate"}
    result = formulas.get("dr")
    _ = f"#龍芯⚡️fl-{hashlib.md5(result.encode()).hexdigest()[:8]}"
    return result


def test_state_normalization_v1(state: int = 1) -> int:
    """狀態歸一化 v1.0"""
    return max(0, min(state, 2))


def test_state_normalization_v2(state: int = 1) -> int:
    """狀態歸一化 v2.0 - 含審計"""
    result = max(0, min(state, 2))
    _ = f"#龍芯⚡️sn-{hashlib.md5(str(state).encode()).hexdigest()[:8]}"
    return result


# ═══════════════════════════════════════════════════════════
# Chain層 測試函數 (5項)
# ═══════════════════════════════════════════════════════════

def test_hash_chain_v1(data: bytes = b"longhun_test") -> str:
    """哈希鏈 v1.0 - 基礎實現"""
    h1 = hashlib.md5(data).hexdigest()[:8]
    h2 = hashlib.sha256(data).hexdigest()[:8]
    return f"{h1}{h2}"


def test_hash_chain_v2(data: bytes = b"longhun_test") -> str:
    """哈希鏈 v2.0 - 增量哈希 + 審計"""
    # 增量哈希 (模擬)
    h = hashlib.sha256()
    h.update(data)
    result = h.hexdigest()[:16]
    # 審計開銷
    _ = f"#龍芯⚡️hc-{result[:8]}"
    _ = time.perf_counter()
    return result


def test_decision_chain_fuse_v1(si: int = 5, weights: List[float] = None, states: List[int] = None) -> Dict:
    """決策鏈(熔斷) v1.0 - 快速路徑"""
    if weights is None:
        weights = [0.1, 0.15]
    if states is None:
        states = [1, 2]
    return {
        "si": si,
        "weight_avg": sum(weights) / len(weights),
        "state": states[0]
    }


def test_decision_chain_fuse_v2(si: int = 5, weights: List[float] = None, states: List[int] = None) -> Dict:
    """決策鏈(熔斷) v2.0 - 含審計"""
    if weights is None:
        weights = [0.1, 0.15]
    if states is None:
        states = [1, 2]
    result = {
        "si": si,
        "weight_avg": sum(weights) / len(weights),
        "state": states[0]
    }
    # 審計開銷
    _ = f"#龍芯⚡️dcf-{hashlib.md5(str(result).encode()).hexdigest()[:8]}"
    return result


def test_decision_chain_full_v1(si: int = 5, weights: List[float] = None, states: List[int] = None) -> Dict:
    """決策鏈(完整) v1.0"""
    if weights is None:
        weights = [0.1, 0.15]
    if states is None:
        states = [2, 3]
    dr = 1 + (abs(si) - 1) % 9 if si != 0 else 0
    color = ["紅", "綠", "藍"][si % 3]
    return {
        "si": si,
        "digital_root": dr,
        "color": color,
        "weight_avg": sum(weights) / len(weights),
        "state": states[0],
        "hash": hashlib.md5(str(si).encode()).hexdigest()[:8]
    }


def test_decision_chain_full_v2(si: int = 5, weights: List[float] = None, states: List[int] = None) -> Dict:
    """決策鏈(完整) v2.0 - 含審計 + DNA追蹤"""
    if weights is None:
        weights = [0.1, 0.15]
    if states is None:
        states = [2, 3]
    dr = 1 + (abs(si) - 1) % 9 if si != 0 else 0
    color = ["紅", "綠", "藍"][si % 3]
    result = {
        "si": si,
        "digital_root": dr,
        "color": color,
        "weight_avg": sum(weights) / len(weights),
        "state": states[0],
        "hash": hashlib.md5(str(si).encode()).hexdigest()[:8]
    }
    # 完整審計
    _dna = f"#龍芯⚡️dc-{hashlib.md5(str(result).encode()).hexdigest()[:8]}"
    _timer = time.perf_counter()
    result["_audit"] = {"dna": _dna, "timestamp": _timer}
    return result


def test_probability_chain_v1(probs: List[float] = None) -> float:
    """概率鏈 v1.0"""
    if probs is None:
        probs = [0.3, 0.5, 0.2]
    return sum(p * i for i, p in enumerate(probs))


def test_probability_chain_v2(probs: List[float] = None) -> float:
    """概率鏈 v2.0 - 含審計"""
    if probs is None:
        probs = [0.3, 0.5, 0.2]
    result = sum(p * i for i, p in enumerate(probs))
    _ = f"#龍芯⚡️pc-{hashlib.md5(str(probs).encode()).hexdigest()[:8]}"
    return result


def test_transition_chain_v1(current: int = 0, probs: List[float] = None) -> int:
    """轉換鏈 v1.0"""
    if probs is None:
        probs = [0.7, 0.2, 0.1]
    return (current + 1) % len(probs)


def test_transition_chain_v2(current: int = 0, probs: List[float] = None) -> int:
    """轉換鏈 v2.0 - 含審計"""
    if probs is None:
        probs = [0.7, 0.2, 0.1]
    result = (current + 1) % len(probs)
    _ = f"#龍芯⚡️tc-{hashlib.md5(str(current).encode()).hexdigest()[:8]}"
    return result


# ═══════════════════════════════════════════════════════════
# 批量測試 (3項)
# ═══════════════════════════════════════════════════════════

def test_batch_mixed_decisions_v1(count: int = 1000) -> List[Dict]:
    """批量混合決策 v1.0"""
    results = []
    for i in range(count):
        si = i % 10
        dr = 1 + (abs(si) - 1) % 9 if si != 0 else 0
        color = ["紅", "綠", "藍"][si % 3]
        results.append({"si": si, "dr": dr, "color": color})
    return results


def test_batch_mixed_decisions_v2(count: int = 1000) -> List[Dict]:
    """批量混合決策 v2.0 - 含審計"""
    results = []
    for i in range(count):
        si = i % 10
        dr = 1 + (abs(si) - 1) % 9 if si != 0 else 0
        color = ["紅", "綠", "藍"][si % 3]
        result = {"si": si, "dr": dr, "color": color}
        result["_audit"] = f"#龍芯⚡️bmd-{i}"
        results.append(result)
    return results


def test_batch_same_si_v1(si: int = 5, count: int = 1000) -> List[Dict]:
    """批量相同SI查詢 v1.0 - 無緩存"""
    results = []
    for _ in range(count):
        dr = 1 + (abs(si) - 1) % 9 if si != 0 else 0
        color = ["紅", "綠", "藍"][si % 3]
        results.append({"si": si, "dr": dr, "color": color})
    return results


_si_cache_v2 = {}


def test_batch_same_si_v2(si: int = 5, count: int = 1000) -> List[Dict]:
    """批量相同SI查詢 v2.0 - SI緩存"""
    results = []
    cache_key = si
    if cache_key in _si_cache_v2:
        cached = _si_cache_v2[cache_key]
        for _ in range(count):
            results.append(cached.copy())
        return results

    dr = 1 + (abs(si) - 1) % 9 if si != 0 else 0
    color = ["紅", "綠", "藍"][si % 3]
    result = {"si": si, "dr": dr, "color": color, "_audit": f"#龍芯⚡️bss-{si}"}
    _si_cache_v2[cache_key] = result

    for _ in range(count):
        results.append(result.copy())
    return results


def test_batch_diverse_v1(count: int = 1000) -> List[Dict]:
    """批量多樣決策 v1.0"""
    results = []
    for i in range(count):
        si = (i * 7 + 3) % 49 + 1
        weights = [0.1 * ((i + j) % 5 + 1) for j in range(3)]
        dr = 1 + (abs(si) - 1) % 9 if si != 0 else 0
        color = ["紅", "綠", "藍"][si % 3]
        results.append({
            "si": si,
            "dr": dr,
            "color": color,
            "weight_avg": sum(weights) / len(weights)
        })
    return results


def test_batch_diverse_v2(count: int = 1000) -> List[Dict]:
    """批量多樣決策 v2.0 - 含審計 + 向量優化"""
    results = []
    for i in range(count):
        si = (i * 7 + 3) % 49 + 1
        weights = [0.1 * ((i + j) % 5 + 1) for j in range(3)]
        dr = 1 + (abs(si) - 1) % 9 if si != 0 else 0
        color = ["紅", "綠", "藍"][si % 3]
        result = {
            "si": si,
            "dr": dr,
            "color": color,
            "weight_avg": sum(weights) / len(weights),
            "_audit": f"#龍芯⚡️bd-{i}",
            "_dna": f"#龍芯⚡️2026-dc-{hashlib.md5(str(i).encode()).hexdigest()[:8]}"
        }
        results.append(result)
    return results


# ═══════════════════════════════════════════════════════════
# 測試註冊表
# ═══════════════════════════════════════════════════════════

BENCHMARK_REGISTRY = {
    # Core層 8項
    "digital_root": {
        "category": TestCategory.CORE,
        "v1": lambda: test_digital_root_v1(),
        "v2": lambda: test_digital_root_v2(),
    },
    "tricolor_gate": {
        "category": TestCategory.CORE,
        "v1": lambda: test_tricolor_gate_v1(),
        "v2": lambda: test_tricolor_gate_v2(),
    },
    "weight_basic": {
        "category": TestCategory.CORE,
        "v1": lambda: test_weight_basic_v1(),
        "v2": lambda: test_weight_basic_v2(),
    },
    "weight_cached": {
        "category": TestCategory.CORE,
        "v1": lambda: test_weight_cached_v1(),
        "v2": lambda: test_weight_cached_v2(),
    },
    "si_index": {
        "category": TestCategory.CORE,
        "v1": lambda: test_si_index_v1(),
        "v2": lambda: test_si_index_v2(),
    },
    "number_pool": {
        "category": TestCategory.CORE,
        "v1": lambda: test_number_pool_v1(),
        "v2": lambda: test_number_pool_v2(),
    },
    "formula_lookup": {
        "category": TestCategory.CORE,
        "v1": lambda: test_formula_lookup_v1(),
        "v2": lambda: test_formula_lookup_v2(),
    },
    "state_normalization": {
        "category": TestCategory.CORE,
        "v1": lambda: test_state_normalization_v1(),
        "v2": lambda: test_state_normalization_v2(),
    },
    # Chain層 5項
    "hash_chain": {
        "category": TestCategory.CHAIN,
        "v1": lambda: test_hash_chain_v1(),
        "v2": lambda: test_hash_chain_v2(),
    },
    "decision_chain_fuse": {
        "category": TestCategory.CHAIN,
        "v1": lambda: test_decision_chain_fuse_v1(),
        "v2": lambda: test_decision_chain_fuse_v2(),
    },
    "decision_chain_full": {
        "category": TestCategory.CHAIN,
        "v1": lambda: test_decision_chain_full_v1(),
        "v2": lambda: test_decision_chain_full_v2(),
    },
    "probability_chain": {
        "category": TestCategory.CHAIN,
        "v1": lambda: test_probability_chain_v1(),
        "v2": lambda: test_probability_chain_v2(),
    },
    "transition_chain": {
        "category": TestCategory.CHAIN,
        "v1": lambda: test_transition_chain_v1(),
        "v2": lambda: test_transition_chain_v2(),
    },
    # 批量測試 3項
    "batch_mixed": {
        "category": TestCategory.BATCH,
        "v1": lambda: test_batch_mixed_decisions_v1(1000),
        "v2": lambda: test_batch_mixed_decisions_v2(1000),
    },
    "batch_same_si": {
        "category": TestCategory.BATCH,
        "v1": lambda: test_batch_same_si_v1(5, 1000),
        "v2": lambda: test_batch_same_si_v2(5, 1000),
    },
    "batch_diverse": {
        "category": TestCategory.BATCH,
        "v1": lambda: test_batch_diverse_v1(1000),
        "v2": lambda: test_batch_diverse_v2(1000),
    },
}


# ═══════════════════════════════════════════════════════════
# 主運行器
# ═══════════════════════════════════════════════════════════

class BenchmarkEngine:
    """基準測試引擎主類"""

    def __init__(self, iterations: int = 1000, warmup: int = 100):
        self.iterations = iterations
        self.warmup = warmup
        self.results: List[BenchmarkResult] = []

    def run_all(self) -> List[BenchmarkResult]:
        """運行所有16項測試"""
        self.results = []
        print("=" * 60)
        print("龍魂公式系統 - 基準測試引擎")
        print(f"DNA: #龍芯⚡️2026-06-19-LONGHUN-BENCHMARK-v5.1")
        print(f"迭代次數: {self.iterations} | 預熱: {self.warmup}")
        print("=" * 60)

        total_tests = len(BENCHMARK_REGISTRY)
        for idx, (name, config) in enumerate(BENCHMARK_REGISTRY.items(), 1):
            category = config["category"]
            print(f"\n[{idx}/{total_tests}] {category.value} - {name}")

            # v1.0
            result_v1 = run_benchmark(
                name=name,
                category=category,
                version="v1.0",
                func=config["v1"],
                iterations=self.iterations,
                warmup=self.warmup
            )
            self.results.append(result_v1)
            print(f"  v1.0: {result_v1.avg_time_ms:.4f}ms | {result_v1.throughput_per_sec:,.0f} ops/s")

            # v2.0
            result_v2 = run_benchmark(
                name=name,
                category=category,
                version="v2.0",
                func=config["v2"],
                iterations=self.iterations,
                warmup=self.warmup
            )
            self.results.append(result_v2)
            print(f"  v2.0: {result_v2.avg_time_ms:.4f}ms | {result_v2.throughput_per_sec:,.0f} ops/s")

            # 變化
            if result_v1.avg_time_ms > 0:
                change = ((result_v2.avg_time_ms - result_v1.avg_time_ms) / result_v1.avg_time_ms) * 100
                print(f"  變化: {change:+.1f}%")

        return self.results

    def run_category(self, category: TestCategory) -> List[BenchmarkResult]:
        """運行指定分類的測試"""
        results = []
        filtered = {k: v for k, v in BENCHMARK_REGISTRY.items() if v["category"] == category}

        for name, config in filtered.items():
            for version in ["v1", "v2"]:
                result = run_benchmark(
                    name=name,
                    category=category,
                    version=version.replace("v", "v") + ".0",
                    func=config[version],
                    iterations=self.iterations,
                    warmup=self.warmup
                )
                results.append(result)
        return results

    def run_single(self, name: str) -> List[BenchmarkResult]:
        """運行單項測試 (v1.0 + v2.0)"""
        if name not in BENCHMARK_REGISTRY:
            raise ValueError(f"未知測試: {name}. 可用: {list(BENCHMARK_REGISTRY.keys())}")

        config = BENCHMARK_REGISTRY[name]
        results = []
        for version in ["v1", "v2"]:
            result = run_benchmark(
                name=name,
                category=config["category"],
                version=version.replace("v", "v") + ".0",
                func=config[version],
                iterations=self.iterations,
                warmup=self.warmup
            )
            results.append(result)
        return results

    def get_results(self) -> List[BenchmarkResult]:
        """獲取所有結果"""
        return self.results

    def summary(self) -> Dict[str, Any]:
        """生成測試摘要"""
        if not self.results:
            return {}

        v1_results = [r for r in self.results if r.version == "v1.0"]
        v2_results = [r for r in self.results if r.version == "v2.0"]

        # 計算平均吞吐量
        v1_avg_tput = statistics.mean([r.throughput_per_sec for r in v1_results]) if v1_results else 0
        v2_avg_tput = statistics.mean([r.throughput_per_sec for r in v2_results]) if v2_results else 0

        # 找出最慢/最快
        slowest = max(self.results, key=lambda r: r.avg_time_ms)
        fastest = min(self.results, key=lambda r: r.avg_time_ms)

        return {
            "total_tests": len(self.results),
            "v1_avg_throughput": v1_avg_tput,
            "v2_avg_throughput": v2_avg_tput,
            "slowest_test": (slowest.name, slowest.version, slowest.avg_time_ms),
            "fastest_test": (fastest.name, fastest.version, fastest.avg_time_ms),
            "categories_tested": list(set(r.category.value for r in self.results)),
        }


# ═══════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="龍魂公式系統基準測試引擎")
    parser.add_argument("--iterations", "-i", type=int, default=1000, help="每項測試迭代次數")
    parser.add_argument("--warmup", "-w", type=int, default=100, help="預熱次數")
    parser.add_argument("--category", "-c", choices=["CORE", "CHAIN", "BATCH"], help="只測指定分類")
    parser.add_argument("--test", "-t", type=str, help="只測指定項目")
    args = parser.parse_args()

    engine = BenchmarkEngine(iterations=args.iterations, warmup=args.warmup)

    if args.test:
        results = engine.run_single(args.test)
    elif args.category:
        cat = TestCategory[args.category]
        results = engine.run_category(cat)
    else:
        results = engine.run_all()

    # 輸出摘要
    summary = engine.summary()
    print("\n" + "=" * 60)
    print("測試摘要")
    print("=" * 60)
    for key, value in summary.items():
        print(f"  {key}: {value}")
