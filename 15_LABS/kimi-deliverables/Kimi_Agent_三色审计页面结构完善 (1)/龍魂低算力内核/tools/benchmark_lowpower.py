# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-7b52c0f3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""🐉 低算力实测脚本 · 输出 reports/low-power-report.json
用法: python3 tools/benchmark_lowpower.py
"""
import sys, os, time, json, tracemalloc
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "core"))

def rss_mb():
    with open("/proc/self/status") as f:
        for l in f:
            if l.startswith("VmRSS"):
                return int(l.split()[1]) / 1024

def main():
    基线 = rss_mb()
    from longhun_core.dna_trace import 生成DNA
    from longhun_core.historian import 年轮链
    from longhun_core.flow_control import RateLimiterPlugin, RateLimitConfig
    载入后 = rss_mb()

    t0 = time.perf_counter()
    for _ in range(10000): 生成DNA("BENCH")
    dna_tps = 10000 / (time.perf_counter() - t0)

    链 = 年轮链()
    t0 = time.perf_counter()
    for i in range(10000): 链.落笔(f"bench-{i}", {"i": i})
    链_tps = 10000 / (time.perf_counter() - t0)
    验 = 链.验链()

    插件 = RateLimiterPlugin(RateLimitConfig(tokens_per_second=1e9, burst_size=10**8, audit_logging=False))
    def gen():
        for i in range(100000): yield f"token-{i} "
    t0 = time.perf_counter()
    n = sum(1 for _ in 插件.process_stream("bench", gen()))
    流_tps = n / (time.perf_counter() - t0)

    tracemalloc.start()
    链2 = 年轮链()
    for i in range(50000): 链2.落笔(f"peak-{i}")
    _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()

    报告 = {
        "测试时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "环境": {"Python": sys.version.split()[0], "平台": os.uname().machine + "/Linux"},
        "冷启动基线内存MB": round(基线, 1),
        "内核载入后内存MB": round(载入后, 1),
        "内核增量内存MB": round(载入后 - 基线, 1),
        "DNA生成吞吐_条每秒": round(dna_tps),
        "年轮链落笔吞吐_条每秒": round(链_tps),
        "流式token吞吐_token每秒": round(流_tps),
        "五万条年轮记录业务内存峰值MB": round(peak / 1048576, 1),
        "年轮链完整性": 验,
        "DNA": 生成DNA("LOW-POWER-BENCH"),
    }
    os.makedirs("reports", exist_ok=True)
    with open("reports/low-power-report.json", "w", encoding="utf-8") as f:
        json.dump(报告, f, ensure_ascii=False, indent=2)
    print(json.dumps(报告, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
