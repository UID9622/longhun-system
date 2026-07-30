#!/usr/bin/env python3
#龍芯⚡️2026-07-25-EVOLUTION-CLI-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂 · 自适应进化中枢 CLI v1.0
DNA: #龍芯⚡️2026-07-25-EVOLUTION-CLI-v1.0

用法:
  python3 bin/lh_evolution.py status       全局状态
  python3 bin/lh_evolution.py selftest     自检
  python3 bin/lh_evolution.py trigger      阈值检查
  python3 bin/lh_evolution.py puzzle       全景拼图报告
  python3 bin/lh_evolution.py jump <内容>  记录跳跃碎片
  python3 bin/lh_evolution.py repeat <内容>  检测重复指令
  python3 bin/lh_evolution.py demo         完整演示
"""

import json, sys, os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engines.lh_adaptive_evolution import (
    AdaptiveEvolutionHub, selftest as engine_selftest
)

hub = AdaptiveEvolutionHub()


def cmd_status():
    print(json.dumps(hub.global_status(), ensure_ascii=False, indent=2))


def cmd_selftest():
    print("🧬 龍魂·自适应进化中枢 自检")
    print("═" * 50)
    results = engine_selftest()
    all_ok = True
    for name, result in results.items():
        ok = result == "OK"
        if not ok: all_ok = False
        print(f"  {'🟢' if ok else '🔴'} {name}: {result}")
    print("═" * 50)
    print(f"  结论: {'🟢 全部通过' if all_ok else '🔴 存在问题'}")


def cmd_trigger():
    print("⚡ 阈值触发器检查")
    print("═" * 50)
    r = hub.check_thresholds()
    for d in r["dimensions"]:
        icon = "🔴" if d["level"] == "triggered" else ("🟡" if d["level"] == "warning" else "🟢")
        bar = "█" * min(int(d["ratio"] * 20), 20)
        print(f"  {icon} {d['dimension']:12s} {d['current']:4d}/{d['threshold']:4d}  [{bar}{' '*(20-len(bar))}] {d['ratio']:.0%}")

    if r["should_upgrade"]:
        print(f"\n🔴 系统已达阈值！触发维度: {', '.join(r['triggered'])}")
        print("   自动升级流程:")
        for s in r["upgrade_plan"]["steps"]:
            print(f"     {s['step']}. {s['action']} → {s['cmd']}")
    elif r["warning"]:
        print(f"\n🟡 接近阈值: {', '.join(r['warning'])}")
    else:
        print("\n🟢 所有维度正常")


def cmd_puzzle():
    print("🧩 跳跃思维全景拼图报告")
    print("═" * 50)
    r = hub.puzzle_report()
    print(f"  总碎片: {r['total']}  |  孤立: {r['isolated']}  |  链接: {r['linked']}")
    print(f"  可合龙: {r['assemblable']}  |  已合龙: {r['merged']}")
    if r["clusters"]:
        print(f"\n  发现 {len(r['clusters'])} 个可合龙集群:")
        for c in r["clusters"]:
            print(f"\n  📦 {c['id']} ({c['size']}碎片)")
            print(f"     模块: {', '.join(c['modules'])}")
            print(f"     标签: {', '.join(c['tags'])}")
            for frag in c["fragments"][:5]:
                print(f"     · {frag['content'][:60]}")
            print(f"     💡 {c['suggestion'][:120]}")
    else:
        print("\n  暂无可合龙集群。继续跳跃，系统自动拼图。")


def cmd_jump(content: str, tags: str = "", module: str = "general"):
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    frag = hub.record_jump(content, tag_list, module)
    print(f"🧩 碎片已记录: {frag.fragment_id}")
    print(f"   内容: {frag.content[:60]}")
    print(f"   模块: {frag.module}  |  标签: {frag.tags}")
    print(f"   状态: {frag.status.value}  |  关联: {frag.linked_to}")


def cmd_repeat(content: str, context: str = "cli"):
    r = hub.detect_repeat(content, context)
    if r["is_repeat"]:
        print(f"🔔 重复检测: {r['repeat_type']}")
        print(f"   {r['alert']}")
        if r.get("suggestion"):
            print(f"   📋 {r['suggestion']}")
    else:
        print("🟢 全新指令，已记录。")


def cmd_demo():
    """完整功能演示。"""
    print("╔══════════════════════════════════════╗")
    print("║  🧬 龍魂·自适应进化中枢 v1.0 演示     ║")
    print("╚══════════════════════════════════════╝")

    print("\n── 1. 重复指令检测 ──")
    hub.detect_repeat("帮我写一个登录页面", "codebuddy-chat")
    r = hub.detect_repeat("帮我写一个登录页面，要带验证码", "codebuddy-chat")
    print(f"   首次→记录；二次相似→{'优化' if r.get('repeat_type') == 'optimized' else '未知'}")

    print("\n── 2. 跳跃思维记录 ──")
    hub.record_jump("新增自适应进化中枢", ["系统", "进化", "infra"], "infra")
    hub.record_jump("门户需要实时数据面板", ["门户", "dashboard"], "portal")
    hub.record_jump("进化中枢需要仪表盘展示进化状态", ["门户", "进化", "dashboard"], "portal")
    print("   已记录3个跳跃碎片")

    print("\n── 3. 阈值触发 ──")
    r = hub.check_thresholds()
    triggered = r.get("triggered", [])
    print(f"   检查4维度 → 触发: {triggered} → {'🔴需升级' if r['should_upgrade'] else '🟢正常'}")

    print("\n── 4. 全景拼图 ──")
    pr = hub.puzzle_report()
    print(f"   总碎片: {pr['total']}  |  可合龙集群: {len(pr['clusters'])}")
    for c in pr["clusters"]:
        print(f"     {c['id']}: {c['size']}碎片 → {c['suggestion'][:80]}")

    print("\n── 5. 全局状态 ──")
    gs = hub.global_status()
    print(f"   重复事件: {gs['repeats']['total']}  |  碎片: {gs['puzzles']['total']}")
    print(f"   阈值触发: {gs['thresholds']['triggered']}  |  防剽窃: {'熔断' if gs['guard']['melted'] else '安全'}")

    print("\n╔══════════════════════════════════════╗")
    print("║  🟢 演示完成·五大模块全部运行          ║")
    print("╚══════════════════════════════════════╝")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        cmd_selftest()
    elif args[0] == "status":
        cmd_status()
    elif args[0] == "selftest":
        cmd_selftest()
    elif args[0] == "trigger":
        cmd_trigger()
    elif args[0] == "puzzle":
        cmd_puzzle()
    elif args[0] == "demo":
        cmd_demo()
    elif args[0] == "jump" and len(args) >= 2:
        tags = args[2] if len(args) >= 3 else ""
        module = args[3] if len(args) >= 4 else "general"
        cmd_jump(args[1], tags, module)
    elif args[0] == "repeat" and len(args) >= 2:
        context = args[2] if len(args) >= 3 else "cli"
        cmd_repeat(args[1], context)
    else:
        print(__doc__)
        print("可用命令: status selftest trigger puzzle demo jump repeat")
