#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷇比-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# ============================================================
# 龍魂 · ANTENNA-8GATE 集成测试
# DNA：#龍芯⚡️丙午·癸未·壬戌·丙午·䷀乾为天-TEST-v5.0
# ============================================================

import sys, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'core'))
sys.path.insert(0, os.path.join(BASE, 'scheduler'))

import numpy as np
import time
from antenna_mesh import AntennaMesh, Bagua
from wuxing_scheduler import WuxingScheduler, WuxingTask, Wuxing


def test_antenna_mesh():
    print("=" * 60)
    print("测试1：蚁触神经网 · 八卦门控推理压缩")
    print("=" * 60)

    mesh = AntennaMesh(nodes_per_bagua=4, dim=128)
    print(f"网络规模：{len(mesh.nodes)} 节点")

    total_latency = 0

    for bagua in Bagua:
        x = np.random.randn(128)
        out, stats = mesh.inference(x, bagua)
        total_latency += stats['latency_ms']
        print(f"  {bagua.name}卦：延迟 {stats['latency_ms']:.3f}ms | "
              f"激活 {stats['nodes_active']}/{stats['nodes_total']} | "
              f"跳过率 {stats['skip_rate']*100:.1f}%")

    avg_latency = total_latency / 8
    print(f"\n平均延迟：{avg_latency:.3f} ms")
    print(f"总跳过率：{mesh._avg_skip_rate()*100:.1f}%")
    return True


def test_wuxing_scheduler():
    print("\n" + "=" * 60)
    print("测试2：五行调度器 · 肝心脾肺肾五线程")
    print("=" * 60)

    scheduler = WuxingScheduler()

    tasks = [
        ("安全扫描-P0", Wuxing.木, 0, np.random.randn(128)),
        ("日常对话-P1", Wuxing.火, 1, np.random.randn(128)),
        ("数据存储-P2", Wuxing.水, 2, np.random.randn(128)),
        ("格式转换-P1", Wuxing.土, 1, np.random.randn(128)),
        ("网络IO-P1", Wuxing.金, 1, np.random.randn(128)),
    ]

    for tid, wx, prio, payload in tasks:
        scheduler.submit(WuxingTask(tid, wx, prio, payload))
        print(f"  提交：{tid} → {wx.name} | 优先级P{prio}")

    time.sleep(0.5)
    report = scheduler.get_balance_report()
    print(f"\n五行平衡报告：")
    print(f"  平均健康度：{report['avg_health']}")
    print(f"  失衡度：{report['imbalance']}")
    print(f"  状态：{report['status']}")

    for wname, stats in report['organs'].items():
        print(f"  {wname}：处理{stats['processed']} | 丢弃{stats['dropped']} | "
              f"健康{stats['health']} | 能耗{stats['energy_j']:.2e}J")

    scheduler.stop_all()
    return True


def test_integration():
    print("\n" + "=" * 60)
    print("测试3：蚁触 + 五行 集成")
    print("=" * 60)

    mesh = AntennaMesh(nodes_per_bagua=4, dim=128)
    scheduler = WuxingScheduler()

    vec = np.random.randn(128)

    wx = Wuxing.火
    scheduler.submit(WuxingTask("integration-test", wx, 0, vec))

    out, stats = mesh.inference(vec, Bagua.乾)

    print(f"五行路由：{wx.name}")
    print(f"八卦目标：{Bagua.乾.name}")
    print(f"蚁触延迟：{stats['latency_ms']:.3f} ms")
    print(f"激活节点：{stats['nodes_active']}/{stats['nodes_total']}")

    scheduler.stop_all()
    return True


def benchmark():
    print("\n" + "=" * 60)
    print("测试4：性能基准")
    print("=" * 60)

    mesh = AntennaMesh(nodes_per_bagua=8, dim=512)

    n = 1000
    start = time.time()
    for i in range(n):
        x = np.random.randn(512)
        target = list(Bagua)[i % 8]
        mesh.inference(x, target)
    elapsed = time.time() - start

    print(f"批量推理：{n} 次")
    print(f"总时间：{elapsed:.3f} s")
    print(f"平均延迟：{elapsed/n*1000:.3f} ms")
    print(f"吞吐量：{n/elapsed:.1f} 次/秒")
    print(f"总跳过率：{mesh._avg_skip_rate()*100:.1f}%")

    return True


if __name__ == "__main__":
    print("龍魂 · ANTENNA-8GATE 集成测试启动")
    print("DNA：#龍芯⚡️丙午·癸未·壬戌·丙午·䷀乾为天-TEST-v5.0")
    print()

    results = []
    results.append(test_antenna_mesh())
    results.append(test_wuxing_scheduler())
    results.append(test_integration())
    results.append(benchmark())

    passed = sum(results)
    total = len(results)
    print(f"\n{'='*60}")
    print(f"结果：{passed}/{total} 通过")
    print(f"{'='*60}")
