#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·丁巳·未时·䷐随-SYSTEM-BENCHMARK-v1.0-a3f7c2d1
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·系统性能基准测试 v1.0 — System Performance Benchmark
CPU/内存/磁盘/网络 四维基准·实机跑分·历史对比

用法:
    lh benchmark                  # 默认全项基准测试
    lh benchmark --quick          # 快速基准（仅CPU+内存）
    lh benchmark --compare        # 对比历史基线
    lh benchmark --json           # JSON结构化输出
    python3 bin/lh_system_benchmark.py   # 直接运行
"""

import os
import sys
import time
import json
import platform
import argparse
import subprocess
import hashlib
import statistics
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

# 路径
BENCHMARK_BASELINE = Path(__file__).parent.parent / "data" / "benchmark_baseline.json"
WORKSPACE = Path(__file__).parent.parent


def get_system_info() -> Dict[str, str]:
    """获取系统基本信息"""
    info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }
    # macOS 详细
    if platform.system() == "Darwin":
        try:
            r = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"],
                             capture_output=True, text=True, timeout=5)
            info["cpu_model"] = r.stdout.strip()
        except Exception:
            info["cpu_model"] = "unknown"
        try:
            r = subprocess.run(["sysctl", "-n", "hw.memsize"],
                             capture_output=True, text=True, timeout=5)
            mem_bytes = int(r.stdout.strip())
            info["total_memory"] = f"{mem_bytes / (1024**3):.1f} GB"
        except Exception:
            info["total_memory"] = "unknown"
    elif platform.system() == "Linux":
        try:
            r = subprocess.run(["lscpu"], capture_output=True, text=True, timeout=5)
            for line in r.stdout.split("\n"):
                if "Model name" in line:
                    info["cpu_model"] = line.split(":")[1].strip()
                    break
        except Exception:
            info["cpu_model"] = "unknown"
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if "MemTotal" in line:
                        kb = int(line.split()[1])
                        info["total_memory"] = f"{kb / (1024**2):.1f} GB"
                        break
        except Exception:
            info["total_memory"] = "unknown"
    return info


# ═══════════════════════════════════════════════════════════
# CPU 基准
# ═══════════════════════════════════════════════════════════

def bench_cpu_single() -> Dict[str, Any]:
    """单核CPU性能 — 素数筛+浮点运算"""
    import math
    n = 10_000_000
    # 素数筛
    t0 = time.perf_counter()
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.isqrt(n)) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    primes_count = sum(sieve)
    t1 = time.perf_counter()
    sieve_time = t1 - t0

    # 浮点运算
    t0 = time.perf_counter()
    result = 0.0
    for i in range(5_000_000):
        result += math.sin(i * 0.001) * math.cos(i * 0.0001)
        result += math.sqrt(abs(result)) * 0.5
    t1 = time.perf_counter()
    float_time = t1 - t0

    return {
        "sieve_n": n,
        "primes_found": primes_count,
        "sieve_time_s": round(sieve_time, 3),
        "float_ops": 5_000_000,
        "float_time_s": round(float_time, 3),
        "cpu_single_score": round(100 / (sieve_time + float_time), 0),
    }


def _sieve_worker_multi(n: int) -> int:
    """独立函数，用于多进程/多线程素数筛"""
    import math
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.isqrt(n)) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return sum(sieve)


def bench_cpu_multi() -> Dict[str, Any]:
    """多核CPU性能 — ThreadPoolExecutor（macOS兼容）"""
    from concurrent.futures import ThreadPoolExecutor
    n_per_worker = 2_000_000
    workers = os.cpu_count() or 4

    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        results = list(ex.map(_sieve_worker_multi, [n_per_worker] * workers))
    t1 = time.perf_counter()
    multi_time = t1 - t0

    return {
        "workers": workers,
        "n_per_worker": n_per_worker,
        "multi_time_s": round(multi_time, 3),
        "total_primes": sum(results),
        "cpu_multi_score": round(1000 / multi_time, 0),
        "parallel_efficiency": round(100 / multi_time / workers, 1),
    }


# ═══════════════════════════════════════════════════════════
# 内存基准
# ═══════════════════════════════════════════════════════════

def bench_memory() -> Dict[str, Any]:
    """内存读写性能"""
    size = 50_000_000  # 50M 个整数 ≈ 400MB

    # 顺序写
    t0 = time.perf_counter()
    arr = list(range(size))
    t1 = time.perf_counter()
    write_time = t1 - t0

    # 顺序读
    t0 = time.perf_counter()
    s = sum(arr)
    t1 = time.perf_counter()
    read_time = t1 - t0

    # 随机访问
    import random
    random.seed(9622)
    indices = [random.randint(0, size - 1) for _ in range(1_000_000)]
    t0 = time.perf_counter()
    s2 = sum(arr[i] for i in indices)
    t1 = time.perf_counter()
    random_time = t1 - t0

    mem_mb = size * 28 / (1024 * 1024)  # Python int ≈ 28 bytes
    return {
        "allocated_mb": round(mem_mb, 1),
        "write_mb_s": round(mem_mb / write_time, 1),
        "read_mb_s": round(mem_mb / read_time, 1),
        "random_mb_s": round(1_000_000 * 28 / (1024 * 1024) / random_time, 1),
        "write_time_s": round(write_time, 3),
        "read_time_s": round(read_time, 3),
        "random_time_s": round(random_time, 3),
    }


# ═══════════════════════════════════════════════════════════
# 磁盘基准
# ═══════════════════════════════════════════════════════════

def bench_disk() -> Dict[str, Any]:
    """磁盘IO性能"""
    test_file = WORKSPACE / "_work" / "benchmark_test.bin"
    os.makedirs(test_file.parent, exist_ok=True)
    size_mb = 200
    chunk = b"X" * (1024 * 1024)  # 1MB

    try:
        # 顺序写
        t0 = time.perf_counter()
        with open(test_file, "wb") as f:
            for _ in range(size_mb):
                f.write(chunk)
        t1 = time.perf_counter()
        write_time = t1 - t0
        write_speed = size_mb / write_time if write_time > 0 else 0

        # 顺序读
        t0 = time.perf_counter()
        with open(test_file, "rb") as f:
            while f.read(1024 * 1024):
                pass
        t1 = time.perf_counter()
        read_time = t1 - t0
        read_speed = size_mb / read_time if read_time > 0 else 0

        # 随机读
        import random
        random.seed(9622)
        t0 = time.perf_counter()
        with open(test_file, "rb") as f:
            for _ in range(1000):
                offset = random.randint(0, size_mb - 1)
                f.seek(offset * 1024 * 1024)
                f.read(4096)
        t1 = time.perf_counter()
        random_read_time = t1 - t0
    finally:
        if test_file.exists():
            test_file.unlink()

    return {
        "size_mb": size_mb,
        "write_mb_s": round(write_speed, 1),
        "read_mb_s": round(read_speed, 1),
        "write_time_s": round(write_time, 3),
        "read_time_s": round(read_time, 3),
        "random_read_1k_ops": 1000,
        "random_read_time_s": round(random_read_time, 3),
    }


# ═══════════════════════════════════════════════════════════
# 网络基准
# ═══════════════════════════════════════════════════════════

def bench_network() -> Dict[str, Any]:
    """网络延迟测试"""
    targets = [
        ("鲲鹏", "119.13.90.27"),
        ("百度", "www.baidu.com"),
        ("阿里", "www.aliyun.com"),
        ("GitHub", "github.com"),
    ]
    results = {}
    for name, host in targets:
        try:
            if platform.system() == "Darwin":
                cmd = ["ping", "-c", "5", "-t", "3", host]
            else:
                cmd = ["ping", "-c", "5", "-W", "3", host]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            # 提取延迟
            latencies = []
            for line in r.stdout.split("\n"):
                if "time=" in line:
                    try:
                        ms = float(line.split("time=")[1].split()[0])
                        latencies.append(ms)
                    except (ValueError, IndexError):
                        pass
            if latencies:
                results[name] = {
                    "avg_ms": round(statistics.mean(latencies), 2),
                    "min_ms": round(min(latencies), 2),
                    "max_ms": round(max(latencies), 2),
                    "loss_pct": 0 if "0.0%" in r.stdout else None,
                }
            else:
                results[name] = {"error": "无法解析延迟", "raw": r.stdout[:200]}
        except subprocess.TimeoutExpired:
            results[name] = {"error": "超时"}
        except Exception as e:
            results[name] = {"error": str(e)}

    # 本地HTTP响应测试（如有服务在跑）
    local_ports = [8761, 8771, 9631, 8080]
    http_results = {}
    for port in local_ports:
        try:
            t0 = time.perf_counter()
            r = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code};%{time_total}",
                 f"http://localhost:{port}/"],
                capture_output=True, text=True, timeout=5
            )
            t1 = time.perf_counter()
            if r.returncode == 0:
                parts = r.stdout.strip().split(";")
                if len(parts) >= 2:
                    http_results[f"localhost:{port}"] = {
                        "status": parts[0],
                        "response_s": round(float(parts[1]), 3),
                    }
        except Exception:
            pass

    return {"ping": results, "http": http_results}


# ═══════════════════════════════════════════════════════════
# 综合得分
# ═══════════════════════════════════════════════════════════

def compute_score(cpu_single, cpu_multi, memory, disk, network) -> Dict[str, Any]:
    """计算综合性能得分"""
    scores = {}

    # CPU得分（归一化到 100 为基准）
    cpu_s = cpu_single.get("cpu_single_score", 0)
    cpu_m = cpu_multi.get("cpu_multi_score", 0)
    scores["cpu_single"] = round(cpu_s, 0)
    scores["cpu_multi"] = round(cpu_m, 0)
    scores["cpu_overall"] = round(cpu_s * 0.3 + cpu_m * 0.7, 0)

    # 内存得分
    read_speed = memory.get("read_mb_s", 0)
    scores["memory_read_mb_s"] = round(read_speed, 0)
    scores["memory_score"] = round(min(read_speed / 50, 200), 0)  # 50MB/s = 100分

    # 磁盘得分
    disk_read = disk.get("read_mb_s", 0)
    disk_write = disk.get("write_mb_s", 0)
    scores["disk_read_mb_s"] = round(disk_read, 0)
    scores["disk_write_mb_s"] = round(disk_write, 0)
    scores["disk_score"] = round(min((disk_read + disk_write) / 2 / 5, 200), 0)  # 500MB/s = 100分

    # 网络得分
    net_ping = network.get("ping", {})
    avg_lats = []
    for v in net_ping.values():
        if isinstance(v, dict) and "avg_ms" in v:
            avg_lats.append(v["avg_ms"])
    if avg_lats:
        avg_ping = statistics.mean(avg_lats)
        scores["network_avg_ping_ms"] = round(avg_ping, 1)
        scores["network_score"] = round(max(100 - avg_ping, 5), 0)
    else:
        scores["network_score"] = 0

    # 综合得分（加权）
    weights = {"cpu": 0.35, "memory": 0.25, "disk": 0.25, "network": 0.15}
    overall = (
        scores.get("cpu_overall", 0) * weights["cpu"]
        + scores.get("memory_score", 0) * weights["memory"]
        + scores.get("disk_score", 0) * weights["disk"]
        + scores.get("network_score", 0) * weights["network"]
    )
    scores["overall_score"] = round(overall, 0)

    # 等级
    if overall >= 150:
        scores["grade"] = "🏆 S"
    elif overall >= 120:
        scores["grade"] = "🟢 A"
    elif overall >= 90:
        scores["grade"] = "🟡 B"
    elif overall >= 60:
        scores["grade"] = "🟠 C"
    else:
        scores["grade"] = "🔴 D"

    return scores


# ═══════════════════════════════════════════════════════════
# 历史对比
# ═══════════════════════════════════════════════════════════

def save_baseline(result: Dict[str, Any]):
    """保存基准测试结果"""
    BENCHMARK_BASELINE.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if BENCHMARK_BASELINE.exists():
        try:
            existing = json.loads(BENCHMARK_BASELINE.read_text())
        except Exception:
            pass

    timestamp = datetime.now().isoformat()
    # 保留最近5次
    history = existing.get("history", [])
    history.append({"timestamp": timestamp, "scores": result.get("scores", {})})
    if len(history) > 5:
        history = history[-5:]

    existing["history"] = history
    existing["latest"] = {"timestamp": timestamp, "scores": result.get("scores", {})}
    BENCHMARK_BASELINE.write_text(json.dumps(existing, ensure_ascii=False, indent=2))


def load_baseline() -> Optional[Dict[str, Any]]:
    """加载历史基线"""
    if not BENCHMARK_BASELINE.exists():
        return None
    try:
        return json.loads(BENCHMARK_BASELINE.read_text())
    except Exception:
        return None


def compare_baseline(current: Dict[str, Any]) -> str:
    """对比历史基线"""
    baseline = load_baseline()
    if not baseline or not baseline.get("history"):
        return "📭 无历史基线，这是第一次跑。结果已保存。"

    prev = baseline["history"][-1]["scores"]
    curr = current.get("scores", {})

    lines = ["📊 与上次基线对比:", ""]
    metrics = [
        ("cpu_overall", "CPU综合"),
        ("memory_score", "内存"),
        ("disk_score", "磁盘"),
        ("network_score", "网络"),
        ("overall_score", "综合得分"),
    ]
    for key, label in metrics:
        pv = prev.get(key, 0)
        cv = curr.get(key, 0)
        if pv == 0:
            lines.append(f"  {label}: {cv} (新增)")
        else:
            diff = cv - pv
            icon = "📈" if diff > 0 else ("📉" if diff < 0 else "➡️")
            pct = (diff / pv) * 100
            lines.append(f"  {icon} {label}: {pv} → {cv} ({diff:+.0f}, {pct:+.1f}%)")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# 主运行函数
# ═══════════════════════════════════════════════════════════

def run_benchmark(quick: bool = False, compare: bool = False, json_out: bool = False) -> Dict[str, Any]:
    """运行基准测试"""
    print("🐉 龍魂·系统性能基准测试 v1.0")
    print("=" * 50)
    print()

    result = {
        "timestamp": datetime.now().isoformat(),
        "system_info": get_system_info(),
    }

    # CPU
    print("🧠 CPU基准测试...")
    cpu_single = bench_cpu_single()
    cpu_multi = bench_cpu_multi()
    result["cpu"] = {"single": cpu_single, "multi": cpu_multi}

    # 内存
    if not quick:
        print("💾 内存基准测试...")
        memory = bench_memory()
        result["memory"] = memory

        # 磁盘
        print("💿 磁盘基准测试...")
        disk = bench_disk()
        result["disk"] = disk

        # 网络
        print("🌐 网络基准测试...")
        network = bench_network()
        result["network"] = network
    else:
        memory = {"read_mb_s": 0, "write_mb_s": 0, "random_mb_s": 0}
        disk = {"read_mb_s": 0, "write_mb_s": 0}
        network = {"ping": {}, "http": {}}

    # 综合得分
    scores = compute_score(cpu_single, cpu_multi, memory, disk, network)
    result["scores"] = scores

    # 保存基线
    save_baseline(result)

    # 输出
    if not json_out:
        print()
        print("═" * 50)
        print("📊 基准测试结果")
        print("═" * 50)
        print(f"  系统: {result['system_info'].get('os')} / {result['system_info'].get('cpu_model', 'unk')}")
        print(f"  CPU单核: {scores['cpu_single']} 分  |  多核: {scores['cpu_multi']} 分")
        print(f"  综合CPU: {scores['cpu_overall']} 分")
        if not quick:
            print(f"  内存读取: {scores['memory_read_mb_s']} MB/s")
            print(f"  磁盘读取: {scores['disk_read_mb_s']} MB/s  |  写入: {scores['disk_write_mb_s']} MB/s")
            print(f"  网络延迟: {scores['network_avg_ping_ms']} ms")
            # HTTP服务
            for svc, info in network.get("http", {}).items():
                print(f"  HTTP {svc}: {info.get('response_s', '?')}s (状态{info.get('status', '?')})")
        print(f"  ────────────────────")
        print(f"  🏆 综合得分: {scores['overall_score']} 分 / 等级: {scores['grade']}")
        print()

        if compare:
            print(compare_baseline(result))

    if json_out:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    return result


def main():
    parser = argparse.ArgumentParser(description="龍魂系统性能基准测试")
    parser.add_argument("--quick", action="store_true", help="仅CPU+内存快速测试")
    parser.add_argument("--compare", action="store_true", help="对比历史基线")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    run_benchmark(quick=args.quick, compare=args.compare, json_out=args.json)


if __name__ == "__main__":
    main()
