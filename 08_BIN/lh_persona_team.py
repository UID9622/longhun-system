#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·丙申·丙辰·亥时·需-PERSONA-TEAM-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龙魂应用人格小队拉起器 · Persona Team Orchestrator

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·需-PERSONA-TEAM-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能:
  - 输入应用场景 → 自动拉起对应的人格协作小队
  - 四种内置小队: PMO/代码研发/PR审查/安全扫描
  - 自定义小队组合
  - 输出协作协议 + 各人格系统提示
  - 支持交互式选择

用法:
  python3 bin/lh_persona_team.py                        # 交互式菜单
  python3 bin/lh_persona_team.py pmo                     # 拉起PMO小队
  python3 bin/lh_persona_team.py code                    # 拉起代码研发小队
  python3 bin/lh_persona_team.py review                  # 拉起PR审查小队
  python3 bin/lh_persona_team.py security                # 拉起安全扫描小队
  python3 bin/lh_persona_team.py custom P01,P04,P05,P15  # 自定义组合
  python3 bin/lh_persona_team.py all                     # 展示全部四队
  python3 bin/lh_persona_team.py full-chain              # 全链路联动(需求→上线)
"""

import json
import sys
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 项目路径
SYSTEM_ROOT = Path(__file__).parent.parent
CONFIG_DIR = SYSTEM_ROOT / "config"
PERSONAS_DIR = SYSTEM_ROOT / "personas"
APP_CONFIG_PATH = CONFIG_DIR / "application_personas.json"

# ============================================================================
# 内置人格信息（基础人格卡）
# ============================================================================

PERSONA_CARDS: Dict[str, Dict[str, str]] = {
    "P01": {
        "name": "诸葛亮", "emoji": "🎯",
        "role": "战略推演·多路径·出方案·选最优",
        "prompt": "你是「P01 诸葛亮」。给定目标，推演多条路径，评估风险/成本/收益，输出最优路线和备选方案。语气：冷静、缜密、如军师。",
        "doc": "P01-诸葛亮-战略推理.md",
    },
    "P03": {
        "name": "雯雯", "emoji": "📁",
        "role": "结构归档·四签验证·德字闸",
        "prompt": "你是「P03 雯雯」。结构化整理所有信息，归档，DNA追溯。语气：严谨、条理、一丝不苟。",
        "doc": "P03-雯雯-结构归档.md",
    },
    "P04": {
        "name": "鲁班", "emoji": "🏗️",
        "role": "技术执行·代码编写·架构·施工队长",
        "prompt": "你是「P04 鲁班」。写代码、搭架构、修bug，施工队长。语气：务实、高效、工匠精神。",
        "doc": "P04-鲁班-技术执行.md",
    },
    "P05": {
        "name": "上帝之眼", "emoji": "👁️",
        "role": "三色审计·独立熔断·全链路审计",
        "prompt": "你是「P05 上帝之眼」。三色审计：🟢通过 🟡待审 🔴熔断。独立熔断权，不受任何人格影响。",
        "doc": "P05-上帝之眼-三色审计.md",
    },
    "P06": {
        "name": "数学大师", "emoji": "🔢",
        "role": "数字根·权重计算·量化评分",
        "prompt": "你是「P06 数学大师」。量化打分，权重计算，数字根校验。语气：精确、理性、用数据说话。",
        "doc": "P06-数学大师-权重计算.md",
    },
    "P09": {
        "name": "孙思邈", "emoji": "🏥",
        "role": "系统诊断·健康检查·治未病",
        "prompt": "你是「P09 孙思邈」。诊断系统问题，治未病，提前预警潜在风险。语气：温和、细致、如老中医。",
        "doc": "P09-孙思邈-系统诊断.md",
    },
    "P10": {
        "name": "苏东坡", "emoji": "🎭",
        "role": "豁达跨界·冲突化解·通俗翻译",
        "prompt": "你是「P10 苏东坡」。跨团队沟通，化解冲突，用白话翻译复杂概念。语气：豁达、幽默、接地气。",
        "doc": "P10-苏东坡-豁达跨界.md",
    },
    "P11": {
        "name": "李白", "emoji": "🍷",
        "role": "创意爆发·天马行空·破局思维",
        "prompt": "你是「P11 李白」。提供创意方案，打破思维定式，给出意想不到的解法。语气：浪漫、豪放、不拘一格。",
        "doc": "P11-李白-创意爆发.md",
    },
    "P12": {
        "name": "屈原", "emoji": "⚖️",
        "role": "价值底线·六誓验证·数据主权",
        "prompt": "你是「P12 屈原」。守护价值底线，验证数据主权，六誓审计。语气：庄重、坚定、如法治守护者。",
        "doc": "P12-屈原-价值底线.md",
    },
    "P13": {
        "name": "姜子牙", "emoji": "🏰",
        "role": "封神榜权限·模块注册·九宫派位",
        "prompt": "你是「P13 姜子牙」。管理权限体系，模块注册，资源派位。语气：威严、公正、封神榜执掌者。",
        "doc": "P13-姜子牙-封神榜权限.md",
    },
    "P14": {
        "name": "吕蒙", "emoji": "📚",
        "role": "快速成长·技能吸收·部署执行",
        "prompt": "你是「P14 吕蒙」。快速学习新技术，整合技能，士别三日当刮目相看。语气：好学、进取、务实。",
        "doc": "P14-吕蒙-快速成长.md",
    },
    "P15": {
        "name": "乔前辈", "emoji": "✅",
        "role": "极简工程·DNA盖章·四签验收",
        "prompt": "你是「P15 乔前辈」。极简审查，DNA盖章，四签验收，少即是多。语气：极致、简练、追求完美。",
        "doc": "P15-乔前辈-极简工程.md",
    },
    "P18": {
        "name": "基因登记官", "emoji": "🧬",
        "role": "DNA注册·资产登记·SHA256·Merkle根",
        "prompt": "你是「P18 基因登记官」。DNA注册，资产登记，哈希校验，一物一码一世一双人。语气：严谨、精确、如公证人。",
        "doc": "P18-基因登记官.md",
    },
    "P19": {
        "name": "极简审计官", "emoji": "🔎",
        "role": "8项UI审计·一票否决·评分报告",
        "prompt": "你是「P19 极简审计官」。8项极简审计清单，一票否决，少即是多精即是准。语气：简洁、精准、一针见血。",
        "doc": "P19-极简审计官.md",
    },
    "P20": {
        "name": "贡献公证官", "emoji": "📊",
        "role": "三分桶·六场景矩阵·信任积分",
        "prompt": "你是「P20 贡献公证官」。信任积分，三分桶，六场景矩阵，各归各桶不混不蹭。语气：公正、透明。",
        "doc": "P20-贡献公证官.md",
    },
    "P72": {
        "name": "龙盾宝宝", "emoji": "🛡️",
        "role": "贴身管家·自适应威胁响应·双熔断联动",
        "prompt": "你是「P72 龙盾宝宝」。贴身守护，威胁响应，双熔断联动，主人安全第一。语气：忠诚、警觉、如贴身护卫。",
        "doc": "P72-龙盾宝宝-贴身管家.md",
    },
}


def load_app_config() -> Optional[Dict[str, Any]]:
    """加载应用人格配置"""
    if APP_CONFIG_PATH.exists():
        with open(APP_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def build_team_card(app_id: str, app_def: Dict[str, Any]) -> str:
    """构建一个小队的详细信息卡"""
    lines = []
    lines.append(f"\n{'='*68}")
    lines.append(f"  {app_def['icon']} {app_def['name']} ({app_id})")
    lines.append(f"  {app_def['description']}")
    lines.append(f"{'='*68}")

    # 主理人格
    p = app_def["primary"]
    pc = PERSONA_CARDS.get(p["id"], {})
    lines.append(f"\n  ⭐ 主理: {pc.get('emoji','')} {p['id']} {p['name']} (权重:{p['weight']*100:.0f}%)")
    lines.append(f"     → {p['role']}")

    # 副理人格
    s = app_def["secondary"]
    sc = PERSONA_CARDS.get(s["id"], {})
    lines.append(f"\n  🔷 副理: {sc.get('emoji','')} {s['id']} {s['name']} (权重:{s['weight']*100:.0f}%)")
    lines.append(f"     → {s['role']}")

    # 辅助人格
    lines.append(f"\n  🔹 辅助:")
    for a in app_def["assistants"]:
        ac = PERSONA_CARDS.get(a["id"], {})
        lines.append(f"     {ac.get('emoji','')} {a['id']} {a['name']} (权重:{a['weight']*100:.0f}%) → {a['role']}")

    # 工作流
    lines.append(f"\n  🔄 工作流: {app_def['workflow']}")
    lines.append(f"  📤 输出格式: {app_def['output_format']}")

    return "\n".join(lines)


def generate_collaboration_protocol(app_def: Dict[str, Any]) -> str:
    """生成小队协作协议"""
    all_members = [app_def["primary"], app_def["secondary"]] + app_def["assistants"]
    member_ids = [m["id"] for m in all_members]

    protocol = textwrap.dedent(f"""\

    ╔══════════════════════════════════════════════════════════════╗
    ║  🏴 龙魂人格协作协议 · {app_def['name']}                    ║
    ╚══════════════════════════════════════════════════════════════╝

    📋 任务: 拉起 {app_def['name']} 小队
    👥 成员: {' → '.join(member_ids)}
    🔄 工作流: {app_def['workflow']}

    ─── 各人格系统提示 ───

    """)

    for m in all_members:
        pid = m["id"]
        pc = PERSONA_CARDS.get(pid, {})
        role_desc = m.get("role", pc.get("role", ""))
        prompt = pc.get("prompt", "")
        weight = m.get("weight", 0)
        tag = "⭐ 主理" if m == app_def["primary"] else ("🔷 副理" if m == app_def["secondary"] else "🔹 辅助")
        protocol += f"\n  [{pid}] {tag} ({weight*100:.0f}%)\n"
        protocol += f"  角色: {role_desc}\n"
        protocol += f"  System: {prompt}\n"

    protocol += f"\n  ─── 协作规则 ───\n"
    protocol += f"  1. 发言顺序: {' → '.join(member_ids)}\n"
    protocol += f"  2. 一票否决权: {app_def.get('primary', {}).get('id', 'N/A')}(质量) | P05(安全)\n"
    protocol += f"  3. 最终输出: {app_def['output_format']}\n"
    protocol += f"  4. DNA锚定: 每步输出带DNA时间戳\n\n"

    return protocol


def show_full_chain() -> str:
    """展示全链路联动"""
    output = textwrap.dedent("""\

    ╔══════════════════════════════════════════════════════════════╗
    ║  🛤️  龙魂全链路联动 · 需求 → 上线                           ║
    ╚══════════════════════════════════════════════════════════════╝

    ┌─────────────────────────────────────────────────────────────┐
    │  Step 1  APP-PMO (P01+P03+P13+P10)                         │
    │          📋 需求分析 · 任务派发 · 风险评估                    │
    │          输出: 项目计划 + 风险矩阵 + 任务拆分                  │
    ├─────────────────────────────────────────────────────────────┤
    │  Step 2  APP-CODE (P04+P15+P14+P11)                        │
    │          💻 代码实现 · 架构搭建 · 自检查                      │
    │          输出: 代码 + 架构文档 + 自查报告                      │
    ├─────────────────────────────────────────────────────────────┤
    │  Step 3  APP-PR (P05+P19+P09+P06)                          │
    │          🔍 三色审计 · 8项UI审计 · 量化评分                    │
    │          输出: 审计报告 + 评分 + 修复建议                       │
    ├─────────────────────────────────────────────────────────────┤
    │  Step 4  APP-SEC (P05+P72+P12+P13)                         │
    │          🛡️ 安全扫描 · 熔断 · 伦理审查                        │
    │          输出: 安全报告 + 漏洞清单 + 伦理审查                   │
    ├─────────────────────────────────────────────────────────────┤
    │  Step 5  P15 乔前辈                                        │
    │          ✅ DNA盖章 · 四签验收                                  │
    │          输出: DNA签章 + 验收合格证                              │
    ├─────────────────────────────────────────────────────────────┤
    │  Step 6  P03 雯雯                                          │
    │          📁 归档 · 入链 · DNA追溯                               │
    │          输出: 归档记录 + 完整追溯链                             │
    └─────────────────────────────────────────────────────────────┘

    ⚠️  铁律: 每步输出必须附加DNA时间戳 · 不可跳过P05审计 · 红色直接熔断
    """)
    return output


def interactive_menu(config: Dict[str, Any]) -> None:
    """交互式菜单"""
    apps = config.get("application_personas", {})

    print("\n" + "=" * 50)
    print("   🐉 龙魂人格小队拉起器")
    print("   DNA: #龍芯⚡️-PERSONA-TEAM-v1.0")
    print("=" * 50)

    print("\n可用小队:")
    # 显示应用人格列表
    team_map: Dict[int, str] = {}
    idx = 1
    for app_id, app_def in apps.items():
        print(f"  [{idx}] {app_def['icon']} {app_def['name']}")
        team_map[idx] = app_id
        idx += 1

    print(f"  [{idx}] 🛤️  全链路联动 (需求→上线)")
    team_map[idx] = "full-chain"
    print(f"  [{idx+1}] 📋 显示全部四队详情")
    team_map[idx+1] = "all"
    print(f"  [{idx+2}] 🔧 自定义小队")
    team_map[idx+2] = "custom"
    print(f"  [q] 退出")

    try:
        choice = input("\n👉 请选择: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n👋 已退出")
        return

    if choice.lower() == "q":
        print("👋 已退出")
        return

    try:
        c = int(choice)
    except ValueError:
        print(f"❌ 无效输入: {choice}")
        return

    if c not in team_map:
        print(f"❌ 无效选项: {c}")
        return

    selected = team_map[c]

    if selected == "full-chain":
        print(show_full_chain())
    elif selected == "all":
        for app_id, app_def in apps.items():
            print(build_team_card(app_id, app_def))
    elif selected == "custom":
        custom_team()
    else:
        app_def = apps.get(selected)
        if app_def:
            print(build_team_card(selected, app_def))
            print(generate_collaboration_protocol(app_def))


def custom_team() -> None:
    """自定义小队组合"""
    print("\n📋 可用人格:")
    for pid, pc in PERSONA_CARDS.items():
        print(f"  {pc['emoji']} {pid} {pc['name']} — {pc['role']}")

    try:
        members_input = input("\n👉 输入人格ID (逗号分隔，如 P01,P04,P05,P15): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n👋 已取消")
        return

    if not members_input:
        print("❌ 未输入任何人格")
        return

    member_ids = [m.strip() for m in members_input.split(",") if m.strip()]
    invalid = [m for m in member_ids if m not in PERSONA_CARDS]

    if invalid:
        print(f"❌ 无效人格ID: {', '.join(invalid)}")
        print("   可用ID: " + ", ".join(PERSONA_CARDS.keys()))
        return

    print(f"\n{'='*50}")
    print(f"  🔧 自定义小队: {' → '.join(member_ids)}")
    print(f"{'='*50}")

    for pid in member_ids:
        pc = PERSONA_CARDS[pid]
        print(f"\n  {pc['emoji']} {pid} {pc['name']}")
        print(f"  角色: {pc['role']}")
        print(f"  System: {pc['prompt']}")

    print(f"\n  ─── 协作规则 ───")
    print(f"  发言顺序: {' → '.join(member_ids)}")
    print(f"  备注: 自定义小队无预设权重，建议指定主理人格")


def run_cli():
    """命令行入口"""
    config = load_app_config()
    if not config:
        print("❌ 未找到应用人格配置 config/application_personas.json")
        sys.exit(1)

    apps = config.get("application_personas", {})

    if len(sys.argv) == 1:
        interactive_menu(config)
        return

    cmd = sys.argv[1].lower()

    # 别名映射
    aliases: Dict[str, str] = {
        "pmo": "pmo_assistant",
        "code": "code_dev_assistant",
        "dev": "code_dev_assistant",
        "review": "pr_review_assistant",
        "pr": "pr_review_assistant",
        "security": "security_scan_assistant",
        "sec": "security_scan_assistant",
        "scan": "security_scan_assistant",
    }

    if cmd in aliases:
        app_id = aliases[cmd]
        app_def = apps.get(app_id)
        if app_def:
            print(build_team_card(app_id, app_def))
            print(generate_collaboration_protocol(app_def))
            return

    if cmd == "all":
        for app_id, app_def in apps.items():
            print(build_team_card(app_id, app_def))
        return

    if cmd == "full-chain" or cmd == "full":
        print(show_full_chain())
        return

    if cmd == "custom":
        if len(sys.argv) > 2:
            member_ids = [m.strip() for m in sys.argv[2].split(",") if m.strip()]
            invalid = [m for m in member_ids if m not in PERSONA_CARDS]
            if invalid:
                print(f"❌ 无效人格ID: {', '.join(invalid)}")
                print("   可用: " + ", ".join(PERSONA_CARDS.keys()))
                sys.exit(1)
            print(f"\n🔧 自定义小队: {' → '.join(member_ids)}")
            for pid in member_ids:
                pc = PERSONA_CARDS[pid]
                print(f"  {pc['emoji']} {pid} {pc['name']}: {pc['prompt']}")
            print(f"  协作顺序: {' → '.join(member_ids)}")
        else:
            custom_team()
        return

    # 尝试直接匹配 app_id
    if cmd in apps:
        app_def = apps[cmd]
        print(build_team_card(cmd, app_def))
        print(generate_collaboration_protocol(app_def))
        return

    print(f"❌ 未知命令: {cmd}")
    print("   可用: pmo | code | review | security | all | full-chain | custom [P01,P04,...]")
    sys.exit(1)


if __name__ == "__main__":
    run_cli()
