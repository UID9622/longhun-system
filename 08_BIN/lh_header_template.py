#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂 · 文章抬头模板选择器 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
场景匹配→自动选择模板→生成抬头→附加ROOT_CARD

DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-HEADER-TEMPLATE-SELECTOR-v1.0-b3d8e1a5
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

用法:
  python3 bin/lh_header_template.py                  # 交互式
  python3 bin/lh_header_template.py --list           # 列出所有模板
  python3 bin/lh_header_template.py --template 2 --title "模块 v1.0"
  python3 bin/lh_header_template.py --template 3 --title "协议 v1.0" --skeleton
  python3 bin/lh_header_template.py --auto "这是一篇关于AI博弈论的研究"  # 自动匹配
"""

import sys
import os
import argparse
import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "bin"))

DNA = "#龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-HEADER-TEMPLATE-SELECTOR-v1.0-b3d8e1a5"
VERSION = "1.0.0"

# ============================================================
# 数字根 + 五行
# ============================================================

def digital_root(s: str) -> int:
    """计算字符串中数字各位的数字根"""
    digits = [int(c) for c in s if c.isdigit()]
    if not digits:
        return 0
    total = sum(digits)
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total

def wuxing_from_root(dr: int) -> str:
    """数字根→五行映射"""
    wm = {1: "水", 2: "火", 3: "木", 4: "金", 5: "土", 6: "水", 7: "火", 8: "木", 9: "金"}
    return wm.get(dr, "土")

# ============================================================
# 模板定义
# ============================================================

TEMPLATES = {
    1: {
        "name": "学术博弈论分析型",
        "emoji": "📊",
        "scenes": ["博弈论", "学术研究", "系统对比", "方法论论文", "理论推演", "建模", "分析", "论文", "研究", "因子", "权重"],
        "tricolor_default": "🟡",
        "tricolor_reason": "含分析性评分与前瞻推演，建议人工复核后引用",
        "personas": "P01诸葛亮·P06数学大师·P05上帝之眼",
        "executability": "⚠️ 文中模型为分析性建构，支付参数为标定推演，非实测数据",
        "header": """## 🏷️ AI输出类型声明

**输出者：** [AI名称]（AI协作 · UID9622定盘）
**输出类型：** 学术博弈论建模分析（概念推演 + 证据引证）
**可执行性：** {executability}
**依赖环境：** 无（纯文档）
**关键提示：** 所有事实性论断均带引用标记；模型参数在附录中公开，可复算、可质疑、可迭代
**三色审计：** {tricolor}（{tricolor_reason}）
**DNA签名：** {dna}
""",
        "skeleton_sections": [
            "## 摘要（TL;DR）\n\n[200-300字，覆盖问题、方法、结论]\n",
            "## 问题设定与分析方法\n\n[方法论声明、证据边界说明]\n",
            "## 理论框架\n\n[引用来源、概念定义]\n",
            "## 模型与求解\n\n[博弈矩阵、参数标定依据、求解结果]\n",
            "## 博弈矩阵可视化\n\n```mermaid\ngraph TD\n  A[玩家1] --> B[策略1]\n  A --> C[策略2]\n```\n",
            "## 敏感性分析\n\n[关键参数变化时均衡如何变化]\n",
            "## 与现有文献的对话\n\n[本文模型与已有研究的异同]\n",
            "## 结论\n\n[核心命题、限制条件]\n",
            "## 政策建议\n\n[从博弈均衡推导出的可操作建议]\n",
            "## 附录：模型参数与复算说明\n\n| 参数 | 值 | 标定依据 | 数据来源 |\n|:---|:---|:---|:---|\n",
            "## 参考文献\n\n",
        ],
    },
    2: {
        "name": "工程落地执行型",
        "emoji": "🔧",
        "scenes": ["代码", "脚本", "部署", "执行", "安装", "配置", "API", "开发", "工程", "交付", "工具"],
        "tricolor_default": "🟢",
        "tricolor_reason": "已通过本地测试，可部署",
        "personas": "P04鲁班·P14吕蒙·P15乔前辈",
        "executability": "✅ 所有代码块可直接运行，无需修改",
        "header": """## 🏷️ 执行声明

**输出者：** [AI名称]（AI协作 · UID9622定盘）
**输出类型：** 工程落地包（可执行代码 + 部署脚本）
**可执行性：** {executability}
**依赖环境：** Python 3.8+ / [其他]
**关键提示：** 执行前请备份现有配置；所有敏感信息使用 `.env` 管理
**三色审计：** {tricolor}（{tricolor_reason}）
**DNA签名：** {dna}
""",
        "skeleton_sections": [
            "## 📦 交付物清单\n\n| 文件 | 类型 | 说明 |\n|:---|:---|:---|\n",
            "## 📂 文件树\n\n```\n~\n```\n",
            "## 🚀 执行命令\n\n```bash\n# 待补充\n```\n",
            "## ✅ 验收清单\n\n- [ ] 文件已创建到指定路径\n- [ ] 命令可正常运行\n- [ ] 测试通过\n",
            "## 🔴 一票否决\n\n- 未执行却说已执行 → L3熔断\n- 无测试却说已通过 → L3熔断\n",
        ],
    },
    3: {
        "name": "协议/原则声明型",
        "emoji": "📜",
        "scenes": ["协议", "规则", "宪法", "条款", "政策", "声明", "隐私", "治理"],
        "tricolor_default": "🟢",
        "tricolor_reason": "已通过主权审计",
        "personas": "P12屈原·P13姜子牙·P15乔前辈·P05上帝之眼",
        "executability": "⏳ N/A（治理文档，非可执行代码）",
        "header": """## 🏷️ 协议声明

**发布者：** UID9622 · 诸葛鑫
**协议类型：** [P0-ETERNAL / P1-CORE / P2-SUPPLEMENT]
**生效时间：** {today}
**生效范围：** 全球 / 龍魂系统所有项目
**可修改性：** [❌ 不可修改 / ⚠️ 需双签确认 / ✅ 可迭代]
**三色审计：** {tricolor}（{tricolor_reason}）
**DNA签名：** {dna}
""",
        "skeleton_sections": [
            "## 📜 条款正文\n\n### 第一条：[条款名称]\n\n[条款内容]\n",
            "## 🔐 签章\n\n**DNA：** ...\n**CONFIRM：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z\n**GPG：** A2D0092CEE2E5BA87035600924C3704A8CC26D5F\n",
            "## 📋 修改记录\n\n| 版本 | 日期 | 修改内容 | 修改人 |\n|:---|:---|:---|:---|\n| v1.0 | {today} | 初始发布 | UID9622 |\n",
        ],
    },
    4: {
        "name": "人格对话/协作记录型",
        "emoji": "💬",
        "scenes": ["对话", "协作", "讨论", "推演", "决策", "辅导", "人格"],
        "tricolor_default": "🟢",
        "tricolor_reason": "已完成协作",
        "personas": "全部人格（按场景路由）",
        "executability": "⏳ 对话记录，非可执行代码",
        "header": """## 🏷️ 协作声明

**参与者：** 用户（UID9622） + [人格名称]（[人格ID]）
**协作类型：** 战略推演 / 工程实现 / 知识整理 / 决策咨询
**输出类型：** 对话记录 + 结构化结论
**三色审计：** {tricolor}（{tricolor_reason}）
**DNA签名：** {dna}
""",
        "skeleton_sections": [
            "## 🎯 目标\n\n[本次协作要解决什么问题]\n",
            "## 💬 对话记录\n\n**用户 >** [内容]\n\n**[人格名称] >** [内容]\n",
            "## 📋 结论\n\n[协作达成的结论]\n",
            "## 🔗 关联\n\n- 关联DNA：\n- 关联任务：\n- 关联人格：\n",
        ],
    },
    5: {
        "name": "复盘/总结型",
        "emoji": "📝",
        "scenes": ["复盘", "总结", "回顾", "记错", "月报", "周报", "错误", "改进"],
        "tricolor_default": "🟡",
        "tricolor_reason": "含主观判断，建议复核",
        "personas": "P03雯雯·P05上帝之眼·P09孙思邈",
        "executability": "⏳ 复盘文档，非可执行代码",
        "header": """## 🏷️ 复盘声明

**复盘者：** UID9622 + [AI名称]
**复盘范围：** [时间范围] / [项目范围]
**复盘类型：** 项目复盘 / 月度总结 / 错误回顾 / 知识整理
**三色审计：** {tricolor}（{tricolor_reason}）
**DNA签名：** {dna}
""",
        "skeleton_sections": [
            "## 📊 概览\n\n- 时间范围：[开始] ~ [结束]\n- 总任务数：[N]\n- 已完成：[N]\n",
            "## ✅ 已完成事项\n\n1.\n",
            "## ⚠️ 问题与错误\n\n| 问题 | 原因 | 解决方案 | 防再犯机制 |\n|:---|:---|:---|:---|\n",
            "## 📝 记错本条目\n\n> 如有错误，按记错本格式记录\n",
            "## 🎯 下一步行动\n\n1.\n",
        ],
    },
    6: {
        "name": "快速笔记/想法型",
        "emoji": "💡",
        "scenes": ["灵感", "想法", "笔记", "待整理", "临时", "备忘", "记录"],
        "tricolor_default": "🟡",
        "tricolor_reason": "未整理，需后续复核",
        "personas": "P11李白·P03雯雯",
        "executability": "⏳ 临时笔记，非可执行代码",
        "header": """## 🏷️ 笔记声明

**记录者：** UID9622 / [AI名称]
**记录时间：** {today_full}
**笔记类型：** 灵感 / 待整理 / 临时记录
**三色审计：** {tricolor}（{tricolor_reason}）
**DNA签名：** {dna}
""",
        "skeleton_sections": [
            "## 📝 内容\n\n[快速记录的内容]\n",
            "## 🔗 关联\n\n- 关联项目：\n- 关联人格：\n",
            "## 📋 待办\n\n- [ ] \n",
        ],
    },
}


def generate_root_card(tricolor: str, template_id: int, dna_str: str) -> str:
    """生成 ROOT_CARD"""
    dr = digital_root(dna_str)
    wx = wuxing_from_root(dr)
    type_map = {1: "academic-analysis", 2: "engineering", 3: "protocol-declaration",
                4: "persona-collab", 5: "review", 6: "quicknote"}
    return f"""## 📋 ROOT_CARD

【ROOT_CARD｜数学根审计】
Root: dr={dr}
Wuxing: {wx}
TriColor: {tricolor}
Type: {type_map.get(template_id, 'unknown')}
DNA: {dna_str}
"""


def generate_footer() -> str:
    return """## 协议声明

DNA: {dna_str}
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""


def auto_match(content: str) -> int:
    """根据内容关键词自动匹配模板（加权）"""
    # 高权重关键词 — 强信号，匹配到即+5
    PRIMARY_KW = {
        1: ["博弈论", "学术研究", "方法论", "系统对比"],
        2: ["部署", "安装", "交付", "脚本"],
        3: ["协议", "宪法", "条款", "政策"],
        4: ["对话", "协作", "人格", "讨论"],
        5: ["复盘", "总结", "回顾", "记错", "月报", "周报"],
        6: ["灵感", "笔记", "备忘", "想法", "快速记录"],
    }
    scores = {tid: 0 for tid in TEMPLATES}
    content_lower = content.lower()
    for tid, tmpl in TEMPLATES.items():
        # 高权重关键词 (+5)
        for kw in PRIMARY_KW.get(tid, []):
            if kw.lower() in content_lower:
                scores[tid] += 5
        # 普通关键词 (+1)
        for kw in tmpl["scenes"]:
            if kw.lower() in content_lower:
                scores[tid] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else 1


def interactive_select() -> int:
    """交互式选择模板"""
    print("""
╔══════════════════════════════════════════════════════╗
║  🐉 龍魂 · 文章抬头模板选择器 v{VERSION}           ║
╠══════════════════════════════════════════════════════╣
""".format(VERSION=VERSION))
    for tid in sorted(TEMPLATES):
        tmpl = TEMPLATES[tid]
        print(f"║  [{tid}] {tmpl['emoji']} {tmpl['name']}")
        print(f"║      适用: {', '.join(tmpl['scenes'][:4])}")
        print(f"║      三色: {tmpl['tricolor_default']} 默认")
        print(f"║      人格: {tmpl['personas'][:40]}")
        print(f"║")
    print("╚══════════════════════════════════════════════════════╝")
    while True:
        try:
            choice = input("\n选择模板 [1-6] 或输入场景描述自动匹配: ").strip()
            tid = int(choice)
            if 1 <= tid <= 6:
                return tid
        except ValueError:
            if choice:
                tid = auto_match(choice)
                tmpl = TEMPLATES[tid]
                print(f"  自动匹配 → 模板{tid}: {tmpl['emoji']} {tmpl['name']}")
                confirm = input("  确认? [Y/n]: ").strip().lower()
                if confirm in ("", "y", "yes"):
                    return tid
                continue
        print("  输入 1-6 或一段场景描述")


def generate(template_id: int, title: str, skeleton: bool = False, output: str = None) -> str:
    """生成指定模板的抬头"""
    tmpl = TEMPLATES[template_id]
    today = datetime.datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    today_full = today.strftime("%Y-%m-%d %H:%M")
    dna_str = f"#龍芯⚡️{today_str}-{title.replace(' ', '-').replace('/', '-')}"

    title_line = f"# 🐉 {title}\n"

    header = tmpl["header"].format(
        today=today_str,
        today_full=today_full,
        tricolor=tmpl["tricolor_default"],
        tricolor_reason=tmpl["tricolor_reason"],
        dna=dna_str,
        executability=tmpl["executability"],
    )

    # 生成 root_card
    root_card = generate_root_card(tmpl["tricolor_default"], template_id, dna_str)

    result = title_line + header
    if skeleton:
        result += "\n" + "\n".join(tmpl["skeleton_sections"])
    else:
        result += "\n[正文内容在此填入...]\n"

    result += "\n" + generate_footer().format(dna_str=dna_str) + "\n"
    result += "\n" + root_card + "\n"
    result += f"\n---\n*Generated by 龍魂 Header Template Selector v{VERSION} | 2026-08-02*\n"

    if output:
        out_path = Path(output)
        if not out_path.is_absolute():
            out_path = PROJECT_ROOT / output
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(result, encoding="utf-8")
        print(f"✅ 已生成: {out_path}")
        print(f"   模板: [{template_id}] {tmpl['emoji']} {tmpl['name']}")
        print(f"   三色: {tmpl['tricolor_default']} | DNA: {dna_str}")

    return result


def list_templates():
    """列出所有模板"""
    print(f"\n🐉 龍魂 · 文章抬头模板 v{VERSION}")
    print("=" * 56)
    for tid in sorted(TEMPLATES):
        tmpl = TEMPLATES[tid]
        print(f"\n[{tid}] {tmpl['emoji']} {tmpl['name']}")
        print(f"    三色默认: {tmpl['tricolor_default']}")
        print(f"    关联人格: {tmpl['personas']}")
        print(f"    适用场景: {', '.join(tmpl['scenes'])}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description=f"🐉 龍魂 · 文章抬头模板选择器 v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                                      # 交互式选择
  %(prog)s --list                               # 列出所有模板
  %(prog)s --template 2 --title "模块v1.0"       # 生成工程模板抬头
  %(prog)s --template 3 --title "协议v1.0" --skeleton  # 含完整骨架
  %(prog)s --auto "博弈论分析AI系统"             # 自动匹配+生成
  %(prog)s --template 5 --title "复盘v1.0" -o docs/review.md  # 输出到文件
        """,
    )
    parser.add_argument("--list", action="store_true", help="列出所有模板")
    parser.add_argument("--template", "-t", type=int, choices=range(1, 7), help="指定模板编号 (1-6)")
    parser.add_argument("--title", type=str, default="未命名文档", help="文章标题")
    parser.add_argument("--skeleton", action="store_true", help="生成完整骨架（含空区块）")
    parser.add_argument("--auto", "-a", type=str, help="自动匹配（提供一段描述或标题）")
    parser.add_argument("--output", "-o", type=str, help="输出文件路径（相对于项目根目录）")

    args = parser.parse_args()

    # --list
    if args.list:
        list_templates()
        return

    # --auto
    if args.auto:
        tid = auto_match(args.auto)
        tmpl = TEMPLATES[tid]
        print(f"自动匹配 → 模板{tid}: {tmpl['emoji']} {tmpl['name']}")
        title = args.title if args.title != "未命名文档" else args.auto[:40]
        print(generate(tid, title, skeleton=args.skeleton, output=args.output))
        return

    # 指定模板
    if args.template:
        print(generate(args.template, args.title, skeleton=args.skeleton, output=args.output))
        return

    # 交互式
    try:
        tid = interactive_select()
        title = input(f"文章标题 [{TEMPLATES[tid]['name']}]: ").strip()
        if not title:
            title = f"{TEMPLATES[tid]['name']}-{datetime.datetime.now().strftime('%Y%m%d')}"
        skeleton = input("生成完整骨架（含空区块）? [y/N]: ").strip().lower()
        output = input("输出文件（留空=打印到屏幕）: ").strip()
        print()
        if output:
            generate(tid, title, skeleton=(skeleton in ("y", "yes")), output=output)
        else:
            print(generate(tid, title, skeleton=(skeleton in ("y", "yes"))))
    except (KeyboardInterrupt, EOFError):
        print("\n👋 已取消")
        sys.exit(0)


if __name__ == "__main__":
    main()
