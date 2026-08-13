#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·丁巳·未时·䷐随-LOAD-TEST-v1.0-b2e8f4a1
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·HTTP压力测试工具 v1.0 — Load Test / Stress Test
并发请求·延迟分布·QPS统计·实时进度

用法:
    lh load-test                                    # 默认localhost:8761, 10并发, 30s
    lh load-test --concurrency 100 --duration 60s   # 100并发60秒
    lh load-test --endpoint http://localhost:8080/verify --concurrency 50
    lh load-test --method POST --body '{"test":1}'  # POST请求
    python3 bin/lh_load_test.py --url http://localhost:8761/ --concurrency 100 --duration 60s
"""

import os
import sys
import time
import json
import argparse
import threading
import statistics
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

# HTTP客户端 - 优先 urllib (标准库零依赖)
try:
    import urllib.request
    import urllib.error
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False

try:
    import http.client
    HAS_HTTP_CLIENT = True
except ImportError:
    HAS_HTTP_CLIENT = False


class LoadTester:
    """HTTP压力测试器"""

    def __init__(self, url: str, method: str = "GET", headers: Dict = None,
                 body: str = None, timeout: float = 30):
        self.url = url
        self.method = method.upper()
        self.headers = headers or {"User-Agent": "LongHun-LoadTest/1.0"}
        self.body = body.encode("utf-8") if body else None
        self.timeout = timeout

        # 统计
        self.lock = threading.Lock()
        self.total_requests = 0
        self.success_requests = 0
        self.error_requests = 0
        self.latencies: List[float] = []
        self.status_codes: Dict[int, int] = {}
        self.errors: Dict[str, int] = {}
        self.start_time = 0.0
        self.stop_flag = False

    def _make_request(self) -> Tuple[bool, float, int, str]:
        """单次HTTP请求"""
        t0 = time.perf_counter()
        try:
            req = urllib.request.Request(self.url, data=self.body, headers=self.headers, method=self.method)
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                status = resp.status
                resp.read()  # 消费响应体
            t1 = time.perf_counter()
            return True, t1 - t0, status, ""
        except urllib.error.HTTPError as e:
            t1 = time.perf_counter()
            return False, t1 - t0, e.code, f"HTTP {e.code}"
        except Exception as e:
            t1 = time.perf_counter()
            return False, t1 - t0, 0, str(type(e).__name__)

    def _worker(self):
        """工作线程"""
        while not self.stop_flag:
            ok, latency, status, err = self._make_request()
            with self.lock:
                self.total_requests += 1
                self.latencies.append(latency)
                if ok:
                    self.success_requests += 1
                    self.status_codes[status] = self.status_codes.get(status, 0) + 1
                else:
                    self.error_requests += 1
                    self.errors[err] = self.errors.get(err, 0) + 1

    def _progress_reporter(self):
        """进度报告线程"""
        while not self.stop_flag:
            time.sleep(2)
            with self.lock:
                elapsed = time.perf_counter() - self.start_time
                qps = self.total_requests / elapsed if elapsed > 0 else 0
                if self.latencies:
                    recent = self.latencies[-min(100, len(self.latencies)):]
                    avg_lat = statistics.mean(recent) * 1000 if recent else 0
                else:
                    avg_lat = 0
            print(f"\r⏳ 已运行 {elapsed:.0f}s | 请求: {self.total_requests} | QPS: {qps:.1f} | 平均: {avg_lat:.0f}ms | 错误: {self.error_requests}", end="")

    def run(self, concurrency: int, duration: float) -> Dict[str, Any]:
        """运行压测"""
        print(f"\n🐉 龍魂·压力测试")
        print(f"  目标: {self.method} {self.url}")
        print(f"  并发: {concurrency}  |  时长: {duration}s")
        print(f"  超时: {self.timeout}s")
        print()

        self.start_time = time.perf_counter()

        # 启动进度线程
        reporter = threading.Thread(target=self._progress_reporter, daemon=True)
        reporter.start()

        # 启动工作线程
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(self._worker) for _ in range(concurrency)]

            # 等待时长
            time.sleep(duration)
            self.stop_flag = True

            # 等待全部完成
            for f in futures:
                try:
                    f.result(timeout=5)
                except Exception:
                    pass

        elapsed = time.perf_counter() - self.start_time

        # 统计
        with self.lock:
            total = self.total_requests
            success = self.success_requests
            errors = self.error_requests
            lats = sorted(self.latencies) if self.latencies else [0]

        # 延迟分布
        def percentile(data, p):
            if not data:
                return 0
            k = (len(data) - 1) * p / 100
            f = int(k)
            c = f + 1 if f + 1 < len(data) else f
            return data[f] * (c - k) + data[c] * (k - f) if f != c else data[f]

        avg_lat = statistics.mean(lats) * 1000 if lats else 0
        min_lat = min(lats) * 1000 if lats else 0
        max_lat = max(lats) * 1000 if lats else 0
        p50 = percentile(lats, 50) * 1000
        p90 = percentile(lats, 90) * 1000
        p95 = percentile(lats, 95) * 1000
        p99 = percentile(lats, 99) * 1000
        qps = total / elapsed if elapsed > 0 else 0
        error_rate = (errors / total * 100) if total > 0 else 0

        result = {
            "timestamp": datetime.now().isoformat(),
            "config": {
                "url": self.url,
                "method": self.method,
                "concurrency": concurrency,
                "duration_s": round(duration, 1),
                "actual_elapsed_s": round(elapsed, 2),
            },
            "results": {
                "total_requests": total,
                "success": success,
                "errors": errors,
                "error_rate_pct": round(error_rate, 2),
                "qps": round(qps, 1),
                "latency": {
                    "avg_ms": round(avg_lat, 1),
                    "min_ms": round(min_lat, 1),
                    "max_ms": round(max_lat, 1),
                    "p50_ms": round(p50, 1),
                    "p90_ms": round(p90, 1),
                    "p95_ms": round(p95, 1),
                    "p99_ms": round(p99, 1),
                },
                "status_codes": self.status_codes,
                "errors_detail": self.errors,
            },
        }

        # 输出报告
        self._print_report(result)
        return result

    def _print_report(self, result: Dict):
        r = result["results"]
        print("\n\n")
        print("═" * 50)
        print("📊 压测结果报告")
        print("═" * 50)
        print(f"  总请求数: {r['total_requests']}")
        print(f"  成功: {r['success']}  |  失败: {r['errors']}  |  错误率: {r['error_rate_pct']}%")
        print(f"  QPS: {r['qps']} req/s")
        print()
        print("  延迟分布:")
        print(f"    平均: {r['latency']['avg_ms']} ms")
        print(f"    最小: {r['latency']['min_ms']} ms")
        print(f"    最大: {r['latency']['max_ms']} ms")
        print(f"    P50: {r['latency']['p50_ms']} ms")
        print(f"    P90: {r['latency']['p90_ms']} ms")
        print(f"    P95: {r['latency']['p95_ms']} ms")
        print(f"    P99: {r['latency']['p99_ms']} ms")
        if r.get("status_codes"):
            print(f"  HTTP状态: {r['status_codes']}")
        if r.get("errors_detail"):
            print(f"  错误详情: {r['errors_detail']}")

        # 判定
        if r["error_rate_pct"] > 5:
            print(f"\n  🔴 错误率过高 ({r['error_rate_pct']}%)，需排查！")
        elif r["latency"]["p99_ms"] > 500:
            print(f"\n  🟡 P99延迟 {r['latency']['p99_ms']}ms 偏高，建议优化")
        elif r["latency"]["p95_ms"] > 200:
            print(f"\n  🟡 P95延迟 {r['latency']['p95_ms']}ms 略高")
        else:
            print(f"\n  🟢 性能表现正常")


def quick_local_bench(target: str = "http://localhost:8761/", concurrency: int = 10, duration: float = 10) -> Dict:
    """快速本地自检 - 轻量"""
    tester = LoadTester(target, timeout=10)
    return tester.run(concurrency=concurrency, duration=duration)


def main():
    parser = argparse.ArgumentParser(description="龍魂HTTP压力测试工具")
    parser.add_argument("--url", "--endpoint", dest="url",
                        default="http://localhost:8761/",
                        help="目标URL (默认: http://localhost:8761/)")
    parser.add_argument("--method", "-X", default="GET", help="HTTP方法 (默认: GET)")
    parser.add_argument("--concurrency", "-c", type=int, default=10, help="并发数 (默认: 10)")
    parser.add_argument("--duration", "-d", type=str, default="30s", help="持续时间 (默认: 30s)")
    parser.add_argument("--body", dest="body", help="请求体 (POST等)")
    parser.add_argument("--header", "-H", dest="headers", action="append",
                        help="自定义Header (可重复)")
    parser.add_argument("--timeout", type=float, default=30, help="请求超时秒数")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    # 解析时长
    duration_str = args.duration.lower().replace("s", "")
    duration = float(duration_str)

    # 解析Headers
    headers = {
        "User-Agent": "LongHun-LoadTest/1.0",
        "Accept": "application/json, text/plain, */*",
    }
    if args.headers:
        for h in args.headers:
            if ":" in h:
                k, v = h.split(":", 1)
                headers[k.strip()] = v.strip()

    tester = LoadTester(
        url=args.url,
        method=args.method,
        headers=headers,
        body=args.body,
        timeout=args.timeout,
    )
    result = tester.run(concurrency=args.concurrency, duration=duration)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0 if result["results"]["error_rate_pct"] < 5 else 1


if __name__ == "__main__":
    sys.exit(main())
