#!/usr/bin/env python3
#龍芯⚡️2026-07-07-PERSONA-REPORT-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
📊 龍魂人格内阁评估报表 · Persona Assessment Report

> DNA: #龍芯⚡️2026-07-07-PERSONA-REPORT-v1.0
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 作用: 读取 persona_registry.json → 计算多维度评估 → 输出结构化报表
> 
> 输出目标:
>   1. portal/data/persona_report.json   — 官网静态加载
>   2. --json 标准输出                   — 飞书机器人 API 调用
>   3. --console 终端彩色报表            — 本地命令行查看

用法:
    python3 bin/lh_persona_report.py                    # 默认：生成报表并写入 portal data
    python3 bin/lh_persona_report.py --console           # 终端彩色报表
    python3 bin/lh_persona_report.py --json              # JSON 标准输出
    python3 bin/lh_persona_report.py --summary P01       # 单个人格详情
    python3 bin/lh_persona_report.py --feishu-card       # 飞书卡片 JSON 格式
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "persona" / "persona_registry.json"
PORTAL_DATA = ROOT / "L5_服务层" / "services" / "portal" / "portal" / "data" / "persona_report.json"
DNA = "#龍芯⚡️2026-07-07-PERSONA-REPORT-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def load_registry():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_assessment(persona: Dict[str, Any]) -> Dict[str, Any]:
    """
    单个人格多维度评估
    
    评分维度:
      - 活跃度 (0-30): 基于总执行次数 + 周/月调用
      - 成功率 (0-25): success_rate * 25
      - 信任度 (0-20): L1=5, L2=10, L3=15, L4=18, L5=20
      - 贡献值 (0-15): help_count + test_contribution_count
      - 稳定性 (0-10): 无熔断=10, 每次熔断-5, 每次警告-2
    """
    # 活跃度评分
    executions = persona.get("executions", 0) or 0
    weekly = persona.get("weekly_call_count", 0) or 0
    monthly = persona.get("monthly_call_count", 0) or 0
    activity_score = min(30, (executions / 10) + weekly * 3 + monthly * 1)
    
    # 成功率评分
    success_rate = persona.get("success_rate", 0.8) or 0.8
    success_score = min(25, success_rate * 25)
    
    # 信任度评分
    trust_map = {"L1": 5, "L2": 10, "L3": 15, "L4": 18, "L5": 20}
    trust_score = trust_map.get(persona.get("trust_level", "L3"), 10)
    
    # 贡献值评分
    help_count = persona.get("help_count", 0) or 0
    test_count = persona.get("test_contribution_count", 0) or 0
    contribution_score = min(15, help_count * 0.5 + test_count * 0.3)
    
    # 稳定性评分
    warnings = persona.get("warning_count", 0) or 0
    fuses = persona.get("fuse_count", 0) or 0
    stability_score = max(0, 10 - fuses * 5 - warnings * 2)
    
    total = round(activity_score + success_score + trust_score + contribution_score + stability_score, 1)
    
    # 等级判定
    if total >= 85:
        grade = "S"
        grade_label = "卓越"
    elif total >= 70:
        grade = "A"
        grade_label = "优秀"
    elif total >= 55:
        grade = "B"
        grade_label = "良好"
    elif total >= 40:
        grade = "C"
        grade_label = "一般"
    else:
        grade = "D"
        grade_label = "待激活"
    
    # 活跃度标签
    if activity_score >= 25:
        activity_label = "🔥 高频"
    elif activity_score >= 15:
        activity_label = "✅ 正常"
    elif activity_score >= 5:
        activity_label = "⚠️ 低频"
    else:
        activity_label = "❌ 休眠"
    
    # 风险评估
    risk = "🟢 无风险"
    if fuses > 0:
        risk = "🔴 曾熔断"
    elif warnings >= 3:
        risk = "🟡 需关注"
    elif warnings > 0:
        risk = "🟡 轻微预警"
    
    # 七维覆盖
    coverage = persona.get("seven_dim_coverage", [])
    
    # LU溯源
    lu_origin = persona.get("_lu_origin", None)
    
    return {
        "code": persona.get("code"),
        "name": persona.get("name"),
        "name_en": persona.get("name_en", ""),
        "role": persona.get("role", ""),
        "ip_group": persona.get("ip_group", "unknown"),
        "status": persona.get("status", "inactive"),
        "motto": persona.get("motto", ""),
        "triggers": persona.get("triggers", []),
        # 原始数据
        "executions": executions,
        "weekly_calls": weekly,
        "monthly_calls": monthly,
        "success_rate": round(success_rate * 100, 1),
        "trust_level": persona.get("trust_level", "L3"),
        "help_count": help_count,
        "test_contributions": test_count,
        "warnings": warnings,
        "fuses": fuses,
        # 评分
        "scores": {
            "activity": round(activity_score, 1),
            "success": round(success_score, 1),
            "trust": round(trust_score, 1),
            "contribution": round(contribution_score, 1),
            "stability": round(stability_score, 1),
            "total": total,
        },
        "grade": grade,
        "grade_label": grade_label,
        "activity_label": activity_label,
        "risk": risk,
        "seven_dim_coverage": coverage,
        "lu_origin": {
            "name": lu_origin.get("lu_persona_name", "") if lu_origin else "",
            "source": lu_origin.get("lu_source", "") if lu_origin else "",
            "sync_date": lu_origin.get("lu_sync_date", "") if lu_origin else "",
        } if lu_origin else None,
        "priority": persona.get("priority", 3),
        "mode": persona.get("mode", "sequential"),
        "last_active": persona.get("last_active_at"),
    }


def generate_report() -> Dict[str, Any]:
    """生成完整的评估报表"""
    data = load_registry()
    personas_raw = data.get("personas", {})
    meta = data.get("_meta", {})
    
    # 计算每个人格评估
    assessments = []
    for code, persona in personas_raw.items():
        assessments.append(compute_assessment(persona))
    
    # 按总分降序
    assessments.sort(key=lambda x: x["scores"]["total"], reverse=True)
    
    # 统计
    total = len(assessments)
    active_count = sum(1 for a in assessments if a["status"] == "active")
    fused_count = sum(1 for a in assessments if a["status"] == "fused")
    inactive_count = sum(1 for a in assessments if a["status"] == "inactive")
    
    # 等级分布
    grade_dist = defaultdict(int)
    for a in assessments:
        grade_dist[a["grade"]] += 1
    
    # IP分组分布
    group_dist = defaultdict(lambda: {"count": 0, "avg_score": 0, "personas": []})
    for a in assessments:
        g = a["ip_group"]
        group_dist[g]["count"] += 1
        group_dist[g]["personas"].append(a["name"])
    
    for g in group_dist:
        scores = [a["scores"]["total"] for a in assessments if a["ip_group"] == g]
        group_dist[g]["avg_score"] = round(sum(scores) / len(scores), 1) if scores else 0
    
    # 信任等级分布
    trust_dist = defaultdict(int)
    for a in assessments:
        trust_dist[a["trust_level"]] += 1
    
    # 平均分
    avg_total = round(sum(a["scores"]["total"] for a in assessments) / total, 1) if total else 0
    
    # 系统健康度
    health_score = round(
        (avg_total * 0.4) +
        (active_count / max(total, 1) * 100 * 0.3) +
        ((1 - fused_count / max(total, 1)) * 100 * 0.3),
        1
    )
    
    # LU回流统计
    lu_count = sum(1 for a in assessments if a["lu_origin"])
    
    now = datetime.now().isoformat()
    
    report = {
        "_meta": {
            "report_dna": DNA,
            "confirm_code": CONFIRM,
            "generated_at": now,
            "registry_version": meta.get("version", "unknown"),
            "registry_dna": meta.get("DNA", ""),
            "gpg": meta.get("GPG", ""),
        },
        "summary": {
            "total_personas": total,
            "active": active_count,
            "inactive": inactive_count,
            "fused": fused_count,
            "average_score": avg_total,
            "system_health": health_score,
            "lu_origin_count": lu_count,
            "grade_distribution": dict(grade_dist),
            "trust_distribution": dict(trust_dist),
            "group_distribution": {k: {"count": v["count"], "avg_score": v["avg_score"]} for k, v in group_dist.items()},
        },
        "rankings": assessments,
        "top5": assessments[:5],
        "needs_attention": [
            a for a in assessments
            if a["grade"] in ("C", "D") or a["status"] == "fused" or a["risk"] != "🟢 无风险"
        ],
    }
    
    return report


def generate_feishu_card(report: Dict[str, Any], query: str = "") -> Dict[str, Any]:
    """
    生成飞书卡片消息格式
    
    支持查询:
      - 空/"全部": 返回总览卡片
      - "P01"/"诸葛亮": 返回单个人格详情
      - "top5": 返回 Top5
      - "健康度": 返回系统健康度
    """
    s = report["summary"]
    rankings = report["rankings"]
    
    # 单个人格查询
    if query and query not in ("全部", "top5", "健康度", "总览"):
        target = None
        for r in rankings:
            if r["code"].upper() == query.upper() or r["name"] == query:
                target = r
                break
        if target:
            sc = target["scores"]
            lu = target["lu_origin"]
            return {
                "msg_type": "interactive",
                "card": {
                    "header": {
                        "title": {"tag": "plain_text", "content": f"🧬 {target['code']} · {target['name']}"},
                        "template": "blue"
                    },
                    "elements": [
                        {"tag": "div", "text": {"tag": "lark_md", "content": f"**角色**: {target['role']}\n**格言**: {target['motto']}\n**状态**: {target['status']} | **等级**: {target['trust_level']}\n**分组**: {target['ip_group']}"}},
                        {"tag": "hr"},
                        {"tag": "div", "text": {"tag": "lark_md", "content": f"📊 **总分**: {sc['total']}/100 · **{target['grade']}级** ({target['grade_label']})\n🔹 活跃度: {sc['activity']}/30\n🔹 成功率: {sc['success']}/25 ({target['success_rate']}%)\n🔹 信任度: {sc['trust']}/20\n🔹 贡献值: {sc['contribution']}/15\n🔹 稳定性: {sc['stability']}/10"}},
                        {"tag": "hr"},
                        {"tag": "div", "text": {"tag": "lark_md", "content": f"📈 总执行: {target['executions']} | 周: {target['weekly_calls']} | 月: {target['monthly_calls']}\n🎯 触发词: {', '.join(target['triggers'][:5])}\n⚠️ 风险: {target['risk']}"}},
                    ] + ([
                        {"tag": "hr"},
                        {"tag": "div", "text": {"tag": "lark_md", "content": f"🧬 **LU溯源**: {lu['name']} | {lu['source']}"}},
                    ] if lu else []),
                    "footer": {
                        "DNA": DNA,
                        "generated_at": report["_meta"]["generated_at"],
                    }
                }
            }
        return {"msg_type": "text", "content": {"text": f"未找到人格: {query}\n可用: P01-P18, P72, P77 或 诸葛亮/张衡/墨子/红客 等"}}
    
    # Top5
    if query == "top5":
        top5 = report["top5"]
        lines = []
        for i, r in enumerate(top5):
            sc = r["scores"]
            lines.append(f"{'🥇🥈🥉🏅🏅'[i]} **{r['code']} {r['name']}** — {sc['total']}分 ({r['grade']}级)")
        return {
            "msg_type": "interactive",
            "card": {
                "header": {"title": {"tag": "plain_text", "content": "🏆 人格内阁 Top5"}, "template": "orange"},
                "elements": [
                    {"tag": "div", "text": {"tag": "lark_md", "content": "\n".join(lines)}},
                    {"tag": "hr"},
                    {"tag": "div", "text": {"tag": "lark_md", "content": f"系统平均分: **{s['average_score']}** | 系统健康度: **{s['system_health']}**"}},
                ]
            }
        }
    
    # 健康度
    if query == "健康度":
        return {
            "msg_type": "interactive",
            "card": {
                "header": {"title": {"tag": "plain_text", "content": "💚 系统健康度报告"}, "template": "green"},
                "elements": [
                    {"tag": "div", "text": {"tag": "lark_md", "content": f"**系统健康度**: {s['system_health']}/100\n**平均分**: {s['average_score']}\n**在线人格**: {s['active']}/{s['total_personas']}\n**熔断**: {s['fused']}\n**LU回流**: {s['lu_origin_count']}"}},
                    {"tag": "hr"},
                    {"tag": "div", "text": {"tag": "lark_md", "content": f"📊 等级分布: " + " | ".join(f"{k}级×{v}" for k, v in sorted(s['grade_distribution'].items()))}},
                    {"tag": "div", "text": {"tag": "lark_md", "content": f"🛡️ 信任分布: " + " | ".join(f"{k}×{v}" for k, v in sorted(s['trust_distribution'].items()))}},
                ]
            }
        }
    
    # 默认总览
    top3 = rankings[:3]
    top3_lines = []
    for r in top3:
        sc = r["scores"]
        top3_lines.append(f"**{r['code']} {r['name']}** — {sc['total']}分 ({r['grade']}级)")
    
    needs = report["needs_attention"]
    needs_text = "✅ 无" if not needs else ", ".join(f"{n['code']} {n['name']}({n['risk']})" for n in needs[:5])
    
    return {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"tag": "plain_text", "content": "🧬 龍魂人格内阁·评估总览"}, "template": "blue"},
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": f"📊 **{s['total_personas']}人格** | 在线{s['active']} | 平均{s['average_score']}分\n💚 健康度: **{s['system_health']}** | LU回流: {s['lu_origin_count']}"}},
                {"tag": "hr"},
                {"tag": "div", "text": {"tag": "lark_md", "content": "🏆 **Top3**:\n" + "\n".join(top3_lines)}},
                {"tag": "hr"},
                {"tag": "div", "text": {"tag": "lark_md", "content": f"⚠️ **需关注**: {needs_text}\n📊 等级分布: " + " | ".join(f"{k}×{v}" for k, v in sorted(s['grade_distribution'].items()))}},
                {"tag": "hr"},
                {"tag": "div", "text": {"tag": "lark_md", "content": "📋 发送指令查询详情:\n`人格 P01` / `人格 top5` / `人格 健康度` / `人格 全部`"}},
            ]
        }
    }


def print_console(report: Dict[str, Any]):
    """终端彩色输出"""
    s = report["summary"]
    rankings = report["rankings"]
    
    print(f"""
╔══════════════════════════════════════════════════════╗
║   🧬 龍魂人格内阁 · 评估报表                      ║
╠══════════════════════════════════════════════════════╣
║  DNA: {DNA}  ║
║  确认: {CONFIRM} ║
╚══════════════════════════════════════════════════════╝
""")
    print(f"📊 系统总览:")
    print(f"   人格总数: {s['total_personas']} | 在线: {s['active']} | 休眠: {s['inactive']} | 熔断: {s['fused']}")
    print(f"   平均分: {s['average_score']}/100 | 健康度: {s['system_health']}/100")
    print(f"   LU回流: {s['lu_origin_count']}人格")
    print(f"   等级分布: " + " | ".join(f"{k}级×{v}" for k, v in sorted(s['grade_distribution'].items())))
    print(f"   信任分布: " + " | ".join(f"{k}×{v}" for k, v in sorted(s['trust_distribution'].items())))
    
    print(f"\n{'排名':<4} {'代码':<6} {'名称':<14} {'角色':<22} {'总分':<6} {'等级':<4} {'活跃度':<8}")
    print("-" * 78)
    for i, r in enumerate(rankings):
        sc = r["scores"]
        print(f"#{i+1:<3} {r['code']:<6} {r['name']:<14} {r['role']:<22} {sc['total']:<6} {r['grade']:<4} {r['activity_label']:<8}")
    
    print(f"\n🏆 Top5:")
    for i, r in enumerate(report["top5"]):
        sc = r["scores"]
        print(f"   {'🥇🥈🥉🏅🏅'[i]} {r['code']} {r['name']} — {sc['total']}分 ({r['grade']}级) — {r['motto']}")
    
    needs = report["needs_attention"]
    if needs:
        print(f"\n⚠️ 需关注的人格:")
        for r in needs:
            print(f"   ⚠️ {r['code']} {r['name']} — {r['grade']}级 — {r['risk']}")
    
    print(f"\n📋 生成时间: {report['_meta']['generated_at']}")
    print(f"📝 注册表版本: {report['_meta']['registry_version']}")
    print()


def print_summary(code: str, report: Dict[str, Any]):
    """打印单个人格详情"""
    rankings = report["rankings"]
    target = None
    for r in rankings:
        if r["code"].upper() == code.upper():
            target = r
            break
    
    if not target:
        print(f"❌ 人格 {code} 不存在")
        sys.exit(1)
    
    sc = target["scores"]
    lu = target["lu_origin"]
    
    print(f"""
╔══════════════════════════════════════════════════════╗
║   {target['code']} · {target['name']} ({target['name_en']})
╠══════════════════════════════════════════════════════╣
║   {target['motto']}
╚══════════════════════════════════════════════════════╝
""")
    print(f"📋 基本信息:")
    print(f"   角色: {target['role']}")
    print(f"   分组: {target['ip_group']} | 模式: {target['mode']} | 优先级: {target['priority']}")
    print(f"   状态: {target['status']} | 信任等级: {target['trust_level']}")
    print(f"   触发词: {', '.join(target['triggers'])}")
    
    print(f"\n📊 评估得分:")
    print(f"   总分: {sc['total']}/100 · {target['grade']}级 ({target['grade_label']})")
    print(f"   活跃度: {sc['activity']}/30 | 成功率: {sc['success']}/25 ({target['success_rate']}%)")
    print(f"   信任度: {sc['trust']}/20 | 贡献值: {sc['contribution']}/15 | 稳定性: {sc['stability']}/10")
    
    print(f"\n📈 调用数据:")
    print(f"   总执行: {target['executions']} | 本周: {target['weekly_calls']} | 本月: {target['monthly_calls']}")
    print(f"   帮助次数: {target['help_count']} | 测试贡献: {target['test_contributions']}")
    print(f"   警告: {target['warnings']} | 熔断: {target['fuses']}")
    
    print(f"\n🎯 状态:")
    print(f"   活跃度: {target['activity_label']} | 风险: {target['risk']}")
    
    if lu:
        print(f"\n🧬 LU溯源:")
        print(f"   源头人格: {lu['name']}")
        print(f"   来源: {lu['source']}")
        print(f"   同步日期: {lu['sync_date']}")
    
    if target["seven_dim_coverage"]:
        print(f"\n🌈 七维覆盖: {', '.join(target['seven_dim_coverage'])}")
    
    print()


def main():
    report = generate_report()
    args = sys.argv[1:]
    
    if "--console" in args:
        print_console(report)
    elif "--json" in args:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif "--summary" in args:
        idx = args.index("--summary")
        if idx + 1 < len(args):
            print_summary(args[idx + 1], report)
        else:
            print("用法: python3 bin/lh_persona_report.py --summary <P编号或名称>")
            sys.exit(1)
    elif "--feishu-card" in args:
        query = ""
        idx = args.index("--feishu-card")
        if idx + 1 < len(args) and not args[idx + 1].startswith("--"):
            query = args[idx + 1]
        card = generate_feishu_card(report, query)
        print(json.dumps(card, ensure_ascii=False, indent=2))
    else:
        # 默认：生成报表并写入 portal data
        print_console(report)
        PORTAL_DATA.parent.mkdir(parents=True, exist_ok=True)
        with open(PORTAL_DATA, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"✅ 报表已写入: {PORTAL_DATA}")
        print(f"   （官网 {PORTAL_DATA.parent.name}/persona_report.json 可直接加载）")


if __name__ == "__main__":
    main()
