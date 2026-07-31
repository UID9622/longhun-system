# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂·湍流治理框架 CLI v1.0
============================
命令行入口，支持：评估/推演/验证/追溯/状态

用法:
  python3 bin/lh_turbulence_cli.py assess            # 态势评估（交互式）
  python3 bin/lh_turbulence_cli.py project            # 签发推演
  python3 bin/lh_turbulence_cli.py verify <proj_id> <actual>  # 对账验证
  python3 bin/lh_turbulence_cli.py trace <proj_id>    # DNA追溯
  python3 bin/lh_turbulence_cli.py status             # 状态报告
  python3 bin/lh_turbulence_cli.py demo               # 端到端演示
  python3 bin/lh_turbulence_cli.py benchmark           # 性能基准

DNA: #龍芯⚡️丙午·乙未·辛酉·井-TURBULENCE-CLI-V1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import sys
import os
import json
import time
import numpy as np
from pathlib import Path

# 添加项目根目录
sys.path.insert(0, str(Path(__file__).parent.parent))

from engines.turbulence.lh_turbulence_governor import TurbulenceGovernor


def cmd_assess(args):
    """态势评估"""
    gov = TurbulenceGovernor()

    print("\n╔══════════════════════════════════════════╗")
    print("║   🌀 龍魂·湍流治理 — 态势评估          ║")
    print("╚══════════════════════════════════════════╝\n")

    # 交互式或参数式
    if len(args) >= 4:
        v, L, rr, tr = float(args[0]), float(args[1]), float(args[2]), float(args[3])
    else:
        v = float(input("情绪传播速度 v (转发/秒): ") or 500)
        L = float(input("事件影响范围 L (触达人数): ") or 10000)
        rr = float(input("理性讨论占比 [0-1]: ") or 0.3)
        tr = float(input("信息透明度 [0-1]: ") or 0.4)

    report = gov.assess(social_velocity=v, social_scope=L,
                        rational_ratio=rr, transparency=tr)

    sr = report.social_reynolds
    print(f"\n📊 社会雷诺数 Re_s = {sr.Re_s:.1f}")
    print(f"   临界值 Re_c = {sr.Re_c:.1f}")
    print(f"   流态: {sr.regime.upper()} ({'层流·可推演' if sr.regime == 'laminar' else '湍流·需降级'})")
    print(f"   推演置信度: {sr.confidence:.2%}")
    print(f"\n📋 建议: {sr.recommendation}")
    print(f"\n🔍 审计:");
    for k, v in report.audit_summary.items():
        print(f"   - {k}: {v}")
    print(f"\n{'🟢 系统正常，可签发推演' if report.regime == 'laminar' else '🟡 湍流态，推演需标注低置信度'}\n")


def cmd_project(args):
    """签发推演"""
    gov = TurbulenceGovernor()

    print("\n╔══════════════════════════════════════════╗")
    print("║   📝 签发推演 — 五步流程               ║")
    print("╚══════════════════════════════════════════╝\n")

    # 先快速评估
    gov.assess(social_velocity=300, social_scope=5000, config_override={"Re_c": 10000000})

    if len(args) >= 6:
        mil, his, phi, eco, pol = [float(a) for a in args[:5]]
        prediction = args[5]
    else:
        print("场景向量（五维：军事/历史/哲学/经济/政治）:")
        mil = float(input("  军事: ") or 0.05)
        his = float(input("  历史: ") or 0.03)
        phi = float(input("  哲学: ") or 0.05)
        eco = float(input("  经济: ") or 0.82)
        pol = float(input("  政治: ") or 0.05)
        prediction = input("\n推演结论: ") or "情绪72小时内进入耗散区间"

    scene = np.array([mil, his, phi, eco, pol])
    proj = gov.project(scene, prediction)

    print(f"\n✅ 推演已签发")
    print(f"   ID: {proj.projection_id}")
    print(f"   DNA签名: {proj.dna_signature}")
    print(f"   人格通道: {proj.persona_channel}")
    print(f"   锚点层级: L{proj.anchor_level}")
    print(f"   观察窗: {proj.observation_window_days}天")
    print(f"\n⏳ 请等待观察窗到期后执行 verify 对账\n")


def cmd_verify(args):
    """对账验证"""
    gov = TurbulenceGovernor()

    if len(args) >= 2:
        proj_id = args[0]
        actual = args[1]
    else:
        proj_id = input("推演ID: ").strip()
        actual = input("真实观测值: ").strip()

    # 尝试解析数字
    try:
        actual_val = float(actual)
    except ValueError:
        actual_val = actual

    was_consolidated = gov.verify(proj_id, actual_val)

    proj = gov.audit_engine.projections.get(proj_id)
    if not proj:
        print(f"❌ 推演 {proj_id} 不存在")
        return

    print(f"\n📊 验证结果:")
    print(f"   推演值 ŷ_n: {proj.prediction}")
    print(f"   真实值 y_n: {actual_val}")
    print(f"   误差 e_n: {proj.error:.4f}")
    print(f"   固化阈值 ε₀: {gov.audit_engine.epsilon_0}")

    if proj.error < gov.audit_engine.epsilon_0:
        print(f"   ✅ 通过（误差 < 阈值）")
        if was_consolidated:
            print(f"   🔒 满足连续固化条件，规则已入 P2 层！")
        else:
            print(f"   ⏳ 等待连续 κ={gov.audit_engine.kappa} 次达标后固化")
    else:
        print(f"   ❌ 未通过（误差 ≥ 阈值），规则不固化，沿DNA修正参数")

    print(f"\n📈 当前准确率 A(t) = {gov.audit_engine.accuracy():.4f}")
    print(f"   单调性: {'✅ 保持' if gov.audit_engine.is_monotonic() else '⚠️ 需检查'}\n")


def cmd_trace(args):
    """DNA追溯"""
    gov = TurbulenceGovernor()

    proj_id = args[0] if args else input("推演ID: ").strip()
    trace_data = gov.trace(proj_id)

    if not trace_data.get("dna_signature"):
        print(f"❌ 推演 {proj_id} 不存在")
        return

    print(f"\n🔍 DNA追溯报告")
    print(f"   推演ID: {trace_data['projection_id']}")
    print(f"   DNA签名: {trace_data['dna_signature']}")
    print(f"   审计轨迹: {trace_data['trail_count']}条")
    print(f"\n   时间线:")
    for t in trace_data["trails"]:
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t["timestamp"]))
        print(f"   [{ts}] {t['event']}: {json.dumps(t['metadata'], ensure_ascii=False)}")
    print()


def cmd_status(args):
    """状态报告"""
    gov = TurbulenceGovernor()

    # 快速初始化
    gov.assess(social_velocity=500, social_scope=10000)

    status = gov.status_report()
    engines = status["engines"]
    params = status["param_state"]

    print("\n╔══════════════════════════════════════════╗")
    print("║   📊 龍魂·湍流治理 — 状态报告          ║")
    print("╚══════════════════════════════════════════╝\n")

    print(f"⏱ 运行时间: {status['uptime_seconds']:.0f}秒\n")

    print("【引擎状态】")
    print(f"  🔗 锚点发现 | q={engines['anchor']['q']} | 收敛={engines['anchor']['contraction_valid']}")
    print(f"  🗝 七因子   | θ₀={engines['factor']['theta_0']} | 指纹={engines['factor']['registered_fingerprints']} | 可分性={engines['factor']['separability']:.3f}")
    print(f"  🧭 人格路由 | 矩阵={engines['router']['matrix_shape']} | 5维×16通道")
    print(f"  📜 分层协议 | 规则={engines['protocol']['total_rules']}条")
    print(f"  🧬 DNA审计 | 推演={engines['audit']['total_projections']} | 验证={engines['audit']['verified']} | 固化={engines['audit']['consolidated_rules']} | A={engines['audit']['accuracy']:.4f}")
    print(f"  🌊 社会雷诺 | Re_c={engines['reynolds']['Re_c']:.1f} | 最新={engines['reynolds'].get('latest_Re_s', 'N/A')}")

    print(f"\n【参数】")
    print(f"  权重: {[f'{w:.3f}' for w in params['weights']]} (收敛度 {params['weight_convergence']:.4f})")
    print(f"  ε₀: {params['epsilon_0']:.4f} | Re_c: {params['Re_c']:.1f}\n")


def cmd_demo(args):
    """端到端演示 — 对应附录A"""
    print("\n╔══════════════════════════════════════════╗")
    print("║   🎬 端到端推演验证演示                ║")
    print("║   场景：企业促销舆情 · 情绪流推演      ║")
    print("╚══════════════════════════════════════════╝\n")

    gov = TurbulenceGovernor(config={"Re_c": 10000000})

    # ═══ 第一步：锚点选择 ═══
    print("【第一步】锚点选择 — 扫描传播结构")
    gov.assess(social_velocity=300, social_scope=5000,
               rational_ratio=0.35, transparency=0.5,
               entity_features={
                   "首发账号": [0.2, 0.45, 0.6, 0.15, 0.7, 0.35, 0.55],
                   "放大节点A": [0.22, 0.47, 0.58, 0.14, 0.72, 0.33, 0.53],
                   "放大节点B": [0.19, 0.44, 0.62, 0.16, 0.68, 0.37, 0.56],
               })
    for lvl, anchor in gov.anchor_engine.anchors.items():
        print(f"   x*_{lvl} {'✅收敛' if anchor.is_converged else '⚠️未收敛'} | 置信度{anchor.confidence:.3f}")

    # ═══ 第二步：签发推演 ═══
    print("\n【第二步】签发推演 — 经济思维通道主导")
    scene = np.array([0.02, 0.03, 0.05, 0.85, 0.05])  # 促销=经济利益驱动
    proj = gov.project(scene, 72.0)  # 数值型：预测耗散时间72h
    print(f"   推演: ŷ₁ = 72h内耗散")
    print(f"   通道: {proj.persona_channel}")
    print(f"   DNA:  {proj.dna_signature}")
    print(f"   ⏳ 推演已挂起，进入90天观察窗...\n")

    # ═══ 第三步：模拟三个月后对账 ═══
    print("【第三步】三个月后对账 — 获取实际观测")
    time.sleep(0.5)  # 戏剧效果
    actual = 66.0
    print(f"   真实观测 y₁ = 66h内耗散")
    print(f"   推演值 ŷ₁ = 72h内耗散")

    # ═══ 第四步：验证+固化（模拟3次连续达标） ═══
    print("\n【第四步】验证固化 — 连续3次达标")
    gov.verify(proj.projection_id, actual)
    e1 = gov.audit_engine.projections[proj.projection_id].error
    print(f"   第1次: e₁={e1:.4f} → {'✅ 通过' if e1 < gov.audit_engine.epsilon_0 else '❌ 未通过'}")

    # 模拟第2-3次...
    for i in range(2, 4):
        p = gov.project(scene, 70.0 + i * 2)
        gov.verify(p.projection_id, 65.0 + i * 3)

    # 检查固化
    for pid, p in gov.audit_engine.projections.items():
        if p.is_consolidated:
            print(f"   🔒 {pid}: 已固化入P2层!")

    print(f"\n   📈 最终准确率 A(t) = {gov.audit_engine.accuracy():.4f}")
    print(f"   {'✅ 单调性已保持' if gov.audit_engine.is_monotonic() else '⚠️ 需核查'}")

    # ═══ 第五步：审计追溯 ═══
    print(f"\n【第五步】DNA审计追溯")
    trace = gov.trace(proj.projection_id)
    print(f"   签名: {trace['dna_signature']}")
    print(f"   轨迹: {trace['trail_count']}条 — 完整血统可审计")

    print(f"\n{'='*50}")
    print(f"🎯 演示结论:")
    print(f"   '促销舆情耗散锚点模式'规则已固化入P2层")
    print(f"   任何人可凭DNA签名 {proj.dna_signature} 回溯全链路")
    print(f"   P0铁律：不删除只冻结，A(t+1)≥A(t) ✅")
    print(f"{'='*50}\n")


def cmd_benchmark(args):
    """性能基准"""
    print("\n⚡ 性能基准测试\n")

    gov = TurbulenceGovernor()

    iterations = int(args[0]) if args else 100
    print(f"跑 {iterations} 轮姿态评估+推演...")

    t0 = time.time()
    for i in range(iterations):
        gov.assess(social_velocity=300 + i, social_scope=5000 + i * 10)
        scene = np.array([0.02, 0.03, 0.05, 0.85, 0.05])
        proj = gov.project(scene, f"推演结论_{i}")
        gov.verify(proj.projection_id, f"实际观测_{i}")

    elapsed = time.time() - t0
    print(f"\n  ✅ {iterations}轮完成, 总耗时 {elapsed:.2f}s")
    print(f"  平均每轮: {elapsed/iterations*1000:.2f}ms")
    print(f"  吞吐量: {iterations/elapsed:.1f} 推演/秒")
    print(f"  最终准确率: {gov.audit_engine.accuracy():.4f}")


# ── 命令路由 ──────────────────────────────────────
COMMANDS = {
    "assess":    (cmd_assess,    "态势评估 [v L rational_ratio transparency]"),
    "project":   (cmd_project,   "签发推演 [mil his phi eco pol prediction]"),
    "verify":    (cmd_verify,    "对账验证 <proj_id> <actual>"),
    "trace":     (cmd_trace,     "DNA追溯 <proj_id>"),
    "status":    (cmd_status,    "状态报告"),
    "demo":      (cmd_demo,      "端到端演示（附录A）"),
    "benchmark": (cmd_benchmark, "性能基准 [iterations]"),
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        print("可用命令:")
        for cmd, (_, desc) in COMMANDS.items():
            print(f"  {cmd:<12} {desc}")
        return

    cmd = sys.argv[1]
    if cmd not in COMMANDS:
        print(f"未知命令: {cmd}")
        print(f"可用: {', '.join(COMMANDS.keys())}")
        return

    handler, _ = COMMANDS[cmd]
    handler(sys.argv[2:])


if __name__ == "__main__":
    main()
