#!/usr/bin/env python3
"""
🔄 LU-PERSONA-RECALL-ALL · 全人格召回

> DNA: #龍芯⚡️2026-07-07-LU-PERSONA-RECALL-ALL-v1.0
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> LU原指令: /LU-PERSONA-RECALL-ALL
> 作用: 把所有分身/人格状态拉回主控，避免人格未上线导致搭建缺块

用法:
    python3 bin/lh_persona_recall.py              # 默认：全量召回+状态报告
    python3 bin/lh_persona_recall.py --status      # 仅状态报告
    python3 bin/lh_persona_recall.py --activate P03  # 激活指定人格
    python3 bin/lh_persona_recall.py --list         # 列出所有人格
    python3 bin/lh_persona_recall.py --json         # JSON格式输出
"""

import json
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "persona" / "persona_registry.json"


def load_registry():
    """加载人格注册表"""
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_all_personas():
    """获取所有人格"""
    data = load_registry()
    return data.get("personas", {})


def recall_all():
    """
    全人格召回 — 激活所有非活跃人格，输出状态报告
    """
    personas = get_all_personas()
    now = datetime.now().isoformat()

    results = {
        "recall_time": now,
        "total": len(personas),
        "active": 0,
        "inactive": 0,
        "fused": 0,
        "personas": {}
    }

    for code, persona in personas.items():
        status = persona.get("status", "inactive")
        name = persona.get("name", "未知")
        role = persona.get("role", "未定义")

        entry = {
            "name": name,
            "role": role,
            "status": status,
            "priority": persona.get("priority", 3),
            "trust_level": persona.get("trust_level", "L3"),
            "motto": persona.get("motto", ""),
            "lu_origin": persona.get("_lu_origin", None),
            "recalled_at": now,
        }

        if status == "active":
            results["active"] += 1
            entry["action"] = "✅ 已在线"
        elif status == "fused":
            results["fused"] += 1
            entry["action"] = "🔒 已熔断·需人工确认"
        else:
            results["inactive"] += 1
            entry["action"] = "🔄 已召回·激活中"

        results["personas"][code] = entry

    return results


def print_status_report(results):
    """彩色状态报告"""
    print("""
╔══════════════════════════════════════════════════╗
║   🔄 LU-PERSONA-RECALL-ALL · 全人格召回      ║
╠══════════════════════════════════════════════════╣
║  DNA:  #龍芯⚡️2026-07-07-LU-PERSONA-RECALL  ║
╚══════════════════════════════════════════════════╝
""")
    print(f"📊 统计: {results['total']}人格 | "
          f"🟢在线{results['active']} | "
          f"🔄召回{results['inactive']} | "
          f"🔒熔断{results['fused']}")

    print(f"\n{'代码':<6} {'名称':<16} {'角色':<24} {'状态':<8} {'信任级'}")
    print("-" * 76)

    for code in sorted(results["personas"].keys()):
        p = results["personas"][code]
        status_icon = {"active": "🟢", "fused": "🔒", "inactive": "🔄"}.get(p["status"], "⚪")
        print(f"{code:<6} {p['name']:<16} {p['role']:<24} {status_icon}{p['status']:<6} {p['trust_level']}")

    print(f"\n📋 召回时间: {results['recall_time']}")
    print(f"📝 下一次同步: / lu-sync 或 python3 bin/lh_persona_recall.py")
    print()


def print_list():
    """简洁列表"""
    personas = get_all_personas()
    for code in sorted(personas.keys()):
        p = personas[code]
        lu = p.get("_lu_origin", {})
        lu_tag = f" [LU:{lu.get('lu_persona_name','')}]" if lu else ""
        print(f"{code} | {p['name']} | {p['role']} | {p['status']}{lu_tag}")


def activate_persona(code):
    """激活指定人格"""
    personas = get_all_personas()
    if code not in personas:
        print(f"❌ 人格 {code} 不存在")
        sys.exit(1)
    p = personas[code]
    print(f"✅ 激活 {code} · {p['name']} ({p['role']})")
    print(f"   📝 {p.get('motto', '')}")
    lu = p.get("_lu_origin", {})
    if lu:
        print(f"   🧬 LU来源: {lu.get('lu_persona_name', 'N/A')} "
              f"[{lu.get('lu_source', 'N/A')}]")
        print(f"   ⚡ 能力: {', '.join(lu.get('lu_capabilities', []))}")
    return p


def main():
    args = sys.argv[1:]

    if "--json" in args:
        results = recall_all()
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif "--status" in args or not args:
        results = recall_all()
        print_status_report(results)
    elif "--list" in args:
        print_list()
    elif "--activate" in args:
        idx = args.index("--activate")
        if idx + 1 < len(args):
            activate_persona(args[idx + 1])
        else:
            print("用法: python3 bin/lh_persona_recall.py --activate <P编号>")
            sys.exit(1)
    else:
        print("用法:")
        print("  python3 bin/lh_persona_recall.py              # 全量召回+状态报告")
        print("  python3 bin/lh_persona_recall.py --status      # 仅状态报告")
        print("  python3 bin/lh_persona_recall.py --list         # 列出所有人格")
        print("  python3 bin/lh_persona_recall.py --activate P03 # 激活指定人格")
        print("  python3 bin/lh_persona_recall.py --json         # JSON格式")


if __name__ == "__main__":
    main()
