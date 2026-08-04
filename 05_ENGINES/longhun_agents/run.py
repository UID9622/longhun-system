#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2
"""
🐲 龍魂·多智能体统一入口 v2.0
DNA: #龍芯⚡️2026-08-04-MULTI-AGENT-ENTRY-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

用法:
  python3 run.py --demo                  # 演示模式
  python3 run.py --task "审计系统安全"     # 单任务执行
  python3 run.py --file doc.md            # 分析文件
  python3 run.py --status                 # 查看所有Agent状态
  python3 run.py --boot                   # 启动所有Agent
  python3 run.py --mode audit --task "..." # 指定执行模式
  python3 run.py --self-test              # 自检模式

模式:
  full      - 全量链式执行
  audit     - 审计模式（守护层全量）
  quick     - 快速模式（最多3个Agent）
  deploy    - 部署模式（P14+P77+P05）
  teaching  - 教学模式（P02+P08+P11）
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

# 路径处理
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "05_ENGINES"))

from engines.longhun_agents import GrandOrchestrator
from engines.longhun_agents.core.chunker import DocumentChunker, ChunkMethod


def print_banner():
    print(f"""
╔══════════════════════════════════════════════════════╗
║  🐲 龍魂·多智能体统一协作框架 v2.0                        ║
║  DNA: #龍芯⚡️2026-08-04-MULTI-AGENT-ENTRY-UID9622    ║
║  三层架构: 蚁群 + 人格矩阵(24) + 黑板主编                  ║
╚══════════════════════════════════════════════════════╝
""")


def print_status(orchestrator: GrandOrchestrator):
    """打印完整状态"""
    status = orchestrator.status_all()
    print(f"\n{'='*60}")
    print(f"📊 龍魂·系统状态")
    print(f"{'='*60}")
    print(f"  Agent总数: {len(status['agents'])}")
    print(f"  已启动: {'✅' if status['booted'] else '❌'}")
    print(f"  蚁群引擎: {'✅' if status['ant_colony'] else '⚠️ 未启用'}")
    print(f"  黑板: {'✅' if status['blackboard'] else '⚠️ 未启用'}")
    print(f"  执行次数: {status['execution_count']}")

    print(f"\n按层分组:")
    layers = orchestrator.status_by_layer()
    for layer, agents in layers.items():
        print(f"  [{layer:12s}] {', '.join(agents)}")

    print(f"\n各Agent状态:")
    for pid, info in sorted(status['agents'].items()):
        state_icon = {"IDLE":"🟢","THINKING":"🟣","ACTING":"🟡","ERROR":"🔴","DONE":"⚫","MELTDOWN":"💀"}
        icon = state_icon.get(info.get('state', '?'), '❓')
        print(f"  {icon} {pid:5s} {info['name']:10s} | {info['layer']:12s} | tasks={info['tasks']}")


def main():
    parser = argparse.ArgumentParser(
        description="🐲 龍魂·多智能体统一协作框架",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 run.py --demo                    # 演示
  python3 run.py --task "审计代码安全"       # 自动路由执行
  python3 run.py --mode audit --task "..."  # 指定模式
  python3 run.py --status                  # 查看状态
  python3 run.py --self-test               # 自检
        """
    )

    parser.add_argument("--demo", action="store_true", help="演示模式")
    parser.add_argument("--self-test", action="store_true", help="自检模式")
    parser.add_argument("--status", action="store_true", help="查看所有Agent状态")
    parser.add_argument("--boot", action="store_true", help="启动所有Agent")
    parser.add_argument("--task", "-t", help="任务描述")
    parser.add_argument("--file", "-f", help="分析文件路径")
    parser.add_argument("--mode", "-m", default="auto",
                        choices=["auto","full","audit","quick","deploy","teaching"],
                        help="执行模式 (默认: auto)")
    parser.add_argument("--agents", "-a", nargs="+",
                        help="指定Agent列表 (如: --agents P05 P06 P12)")
    parser.add_argument("--report", action="store_true", help="输出最终报告")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    # 初始化总编排器
    print_banner()
    orchestrator = GrandOrchestrator(enable_ant_colony=True, enable_blackboard=True)

    # ── 演示模式 ──
    if args.demo:
        orchestrator.demo()
        return

    # ── 自检模式 ──
    if args.self_test:
        run_self_test(orchestrator)
        return

    # ── 状态查询 ──
    if args.status:
        orchestrator.boot()
        print_status(orchestrator)
        return

    # ── 启动所有Agent ──
    if args.boot:
        result = orchestrator.boot()
        print(f"\n✅ 启动完成: {sum(1 for v in result.values() if v)}/{len(result)}")
        print_status(orchestrator)
        return

    # ── 任务执行 ──
    task = args.task
    if args.file:
        fp = Path(args.file)
        if not fp.exists():
            print(f"❌ 文件不存在: {fp}")
            return
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        # 如果是长文件，先分块再汇总
        chunker = DocumentChunker()
        chunks = chunker.chunk(content[:50000], ChunkMethod.HYBRID)
        print(f"📄 文件: {fp.name} → {len(chunks)} 块")
        task = f"分析以下文档内容：{chunks[0].content[:500]}" if chunks else "空文件"
    elif task:
        print(f"📝 任务: {task[:150]}")
    else:
        print("❌ 请指定 --task 或 --file 或 --demo")
        return

    # 执行
    result = orchestrator.run(task, mode=args.mode, agents=args.agents)

    # 输出
    if args.json:
        print(json.dumps(result, ensure_ascii=False, default=str, indent=2))
    else:
        agent_results = result.get("agent_results", {})
        print(f"\n{'='*60}")
        print(f"📋 执行结果 (模式: {result.get('mode', '?')} | 耗时: {result.get('orchestrator',{}).get('elapsed_sec', 0):.1f}s)")
        print(f"{'='*60}")

        for pid, r in agent_results.items():
            status = r.get("status", "?")
            icon = "✅" if status == "ok" else "❌"
            persona = r.get("persona", pid)
            name = r.get("name", pid)
            print(f"  {icon} {persona} ({name}): {status}")
            if status == "error":
                print(f"     └─ {r.get('error', '未知错误')}")

        print(f"\n路由链: {' → '.join(result.get('chain', []))}")

    # 输出报告
    if args.report:
        report = orchestrator.get_final_report()
        if report:
            print(f"\n{'='*60}")
            print(f"📄 最终报告")
            print(f"{'='*60}\n")
            print(report[:3000])
        else:
            print("\n⚠️ 报告未生成")

    # 打印时间戳
    stamp = orchestrator._agents.get("P06")
    if stamp:
        t = stamp.act("time")
        print(f"\n🐉 {datetime.now().strftime('%Y年%m月%d日 %H:%M')} · 🟢")


def run_self_test(orchestrator: GrandOrchestrator):
    """完整自检"""
    print("🔧 龍魂·多智能体自检模式\n")

    # 1. 注册表完整性
    from engines.longhun_agents.agents.persona_agents import AGENT_REGISTRY, AGENT_META
    print(f"[1/5] 注册表完整性: {len(AGENT_REGISTRY)} Agent已注册")
    for pid, meta in sorted(AGENT_META.items()):
        icon = "✅" if pid in AGENT_REGISTRY else "❌"
        print(f"  {icon} {pid:5s} {meta['name']:10s} | {meta['layer']:12s} | {meta['motto']}")

    # 2. Agent启动
    print(f"\n[2/5] Agent启动测试:")
    boot_result = orchestrator.boot()
    ok = sum(1 for v in boot_result.values() if v)
    print(f"  成功: {ok}/{len(boot_result)}")

    # 3. 意图解析
    print(f"\n[3/5] 意图解析测试:")
    test_inputs = ["审计代码安全", "架构设计评估", "部署上线", "教我数学"]
    for inp in test_inputs:
        intent = orchestrator.parse_intent(inp)
        print(f"  '{inp}' → {intent['primary']} ({intent['intent']})")

    # 4. 快速执行
    print(f"\n[4/5] 快速执行测试:")
    result = orchestrator.run("自检: 确认所有Agent在线", mode="quick")
    agent_count = len(result.get("agent_results", {}))
    print(f"  参与Agent: {agent_count} → {'✅' if agent_count > 0 else '❌'}")

    # 5. 最终报告
    print(f"\n[5/5] 主编整合测试:")
    report = orchestrator.get_final_report()
    if report:
        print(f"  ✅ 报告已生成 ({len(report)}字符)")
    else:
        # 手动触发整合
        orchestrator._integrator.act("自检任务", agent_results=result.get("agent_results", {}))
        report = orchestrator.get_final_report()
        print(f"  {'✅' if report else '❌'} 报告{'已' if report else '未'}生成")

    print(f"\n{'='*50}")
    print(f"总计: {orchestrator._agents and len(orchestrator._agents) or 0} Agent可用")
    print(f"注册表: {len(AGENT_REGISTRY)} Agent（22核心+2扩展）")
    print(f"架构层: 6层（战略+执行+文化+守护+安全+子系统）")
    print(f"自检完成 ✅")
    print(f"\n🐉 {datetime.now().strftime('%Y年%m月%d日 %H:%M')} · 🟢")


if __name__ == "__main__":
    main()
