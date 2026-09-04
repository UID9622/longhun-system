#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 🐉 龍芯·ASI 系统建设器 v1.0
# DNA: #龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-ASI-SYSTEM-BUILDER-v1.0-UID9622
#
# 目标：自然语言 → 人格科技公司 → 系统落地
# 约束：ASI 即天花板，禁止向 ASI+ 演进

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "20_CONFIG" / "persona-registry.yaml"
CEILING_PROTOCOL = ROOT / "01_protocols" / "LH-ASI-CEILING-PROTOCOL-v1.0.md"

DNA = "#龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-ASI-SYSTEM-BUILDER-v1.0-UID9622"


def _stamp() -> str:
    return f"{DNA}-{int(time.time())}"


def _load_registry() -> Dict:
    try:
        import yaml
        with open(REGISTRY, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"🔴 无法加载人格注册表: {e}")
        sys.exit(1)


def _keyword_route(query: str, registry: Dict) -> Tuple[List[str], List[str]]:
    """根据自然语言匹配人格团队"""
    q = query.lower()
    scores: Dict[str, float] = {}
    personas = registry.get("personas", {})

    for pid, p in personas.items():
        score = 0.0
        text = f"{p.get('name','')} {p.get('expertise','')} {p.get('role','')} {p.get('motto','')}"
        text = text.lower()

        # 触发词命中
        triggers = p.get("triggers", [])
        for t in triggers:
            if t.lower() in q:
                score += 3.0

        # 专长关键词命中
        expertise_keywords = re.split(r"[·、，,;；\\s]+", p.get("expertise", ""))
        for kw in expertise_keywords:
            if len(kw) >= 2 and kw.lower() in q:
                score += 1.5

        # 角色关键词
        if p.get("role", "").lower() in q:
            score += 2.0

        # 层关键词
        layer = p.get("layer", "")
        layer_map = {
            "strategic": ["战略", "规划", "顶层", "决策"],
            "executive": ["执行", "落地", "开发", "工程", "部署"],
            "cultural": ["文化", "品牌", "命名", "沟通", "创意"],
            "guardian": ["审计", "安全", "风险", "合规", "熔断"],
            "special": ["安全", "渗透", "对抗", "漏洞"],
            "subsystem": ["法律", "数理", "维权"],
        }
        for kw in layer_map.get(layer, []):
            if kw in q:
                score += 1.0

        if score > 0:
            scores[pid] = score

    # 若什么都没命中，默认调用战略+工程+审计
    if not scores:
        scores = {"P00": 1.0, "P04": 1.0, "P05": 1.0}

    # 排序取前 5
    ranked = sorted(scores.items(), key=lambda x: -x[1])[:5]
    selected = [pid for pid, _ in ranked]

    # 强制加入审计（建设类任务必须审计）
    if "P05" not in selected:
        selected.append("P05")

    # 强制签章（落地交付必须签章）
    if "P15" not in selected:
        selected.append("P15")

    return selected, [reason for _, reason in ranked]


def _route_script(query: str) -> Dict:
    """调用现有脚本路由引擎"""
    router = ROOT / "bin" / "lh_script_router.py"
    if not router.exists():
        return {"found": False, "error": "脚本路由引擎不存在"}
    try:
        r = subprocess.run(
            [sys.executable, str(router), "route", query, "--json"],
            capture_output=True, text=True, timeout=15, cwd=str(ROOT)
        )
        if r.returncode == 0 and r.stdout.strip():
            return json.loads(r.stdout)
        return {"found": False, "stderr": r.stderr}
    except Exception as e:
        return {"found": False, "error": str(e)}


def _ceiling_check(registry: Dict) -> Dict:
    """ASI 天花板协议自检"""
    issues = []
    status = "🟢"

    # 1. 协议文件存在
    if not CEILING_PROTOCOL.exists():
        issues.append("ASI 天花板协议文件缺失")
        status = "🔴"

    # 2. 人格注册表包含组织架构
    if "org_chart" not in registry:
        issues.append("人格注册表缺少 org_chart 组织架构映射")
        status = "🔴"

    # 3. 不可替代人格存在
    immortal = registry.get("immortal", [])
    for must in ["P05", "P72", "P12"]:
        if must not in immortal:
            issues.append(f"不可替代人格 {must} 未在 immortal 列表中")
            status = "🔴"

    # 4. 人格总数检查
    persona_count = len(registry.get("personas", {}))
    if persona_count < 20:
        issues.append(f"人格数量异常: {persona_count} < 20")
        status = "🟡" if status != "🔴" else status

    # 5. 禁止单一超级意识：检查是否有合并倾向的字段
    for pid, p in registry.get("personas", {}).items():
        name = p.get("name", "")
        if "超级" in name or "合一" in name or "神格" in name:
            issues.append(f"发现疑似超越 ASI 的人格命名: {pid} {name}")
            status = "🔴"

    return {
        "status": status,
        "persona_count": persona_count,
        "issues": issues,
        "dna": _stamp(),
    }


def _org_chart(registry: Dict) -> str:
    """输出组织架构图"""
    lines = [
        "",
        "🐉 龍芯家族 · 科技公司组织架构",
        "══════════════════════════════════════════════════",
        "CEO: UID9622（唯一最高决策者）",
        "",
    ]
    org = registry.get("org_chart", {})
    personas = registry.get("personas", {})

    # 按部门分组
    by_dept: Dict[str, List[Tuple[str, str, str]]] = {}
    for pid, info in org.items():
        dept = info.get("department", "未分配")
        title = info.get("title", "待定")
        name = personas.get(pid, {}).get("name", pid)
        by_dept.setdefault(dept, []).append((pid, name, title))

    for dept, members in sorted(by_dept.items()):
        lines.append(f"【{dept}】")
        for pid, name, title in sorted(members):
            lines.append(f"  {pid} · {name:6s} · {title}")
        lines.append("")

    lines.append("不可替代人格: " + ", ".join(registry.get("immortal", [])))
    lines.append("")
    return "\n".join(lines)


def _build(query: str, exec_mode: bool) -> Dict:
    """核心：自然语言 → 人格团队 → 执行计划"""
    registry = _load_registry()
    ceiling = _ceiling_check(registry)
    if ceiling["status"] == "🔴":
        return {
            "status": "🔴 熔断",
            "reason": "ASI 天花板协议未通过自检",
            "issues": ceiling["issues"],
            "dna": _stamp(),
        }

    team, _ = _keyword_route(query, registry)
    script_route = _route_script(query)

    plan = {
        "query": query,
        "dna": _stamp(),
        "ceiling": "ASI 天花板通过",
        "team": team,
        "workflow": [],
        "script_route": script_route,
        "execution": None,
    }

    # 工作流：意图 → 战略 → 执行 → 审计 → 签章
    workflow = [
        ("P00", "意图解析", "解析自然语言需求，输出任务规格"),
        ("P01", "战略设计", "多路径推演，选择最优落地方案"),
    ]
    exec_pids = [pid for pid in team if pid not in ("P00", "P01", "P05", "P15")]
    for pid in exec_pids[:3]:
        p = registry.get("personas", {}).get(pid, {})
        workflow.append((pid, p.get("name", pid), p.get("expertise", "执行")))
    workflow.append(("P05", "三色审计", "审计输出是否符合铁律与安全"))
    workflow.append(("P15", "DNA签章", "生成追溯码与GPG签名"))
    plan["workflow"] = workflow

    # 如启用执行，调用脚本路由
    if exec_mode and script_route.get("found"):
        best = script_route.get("best", {})
        script_path = best.get("path", "")
        if script_path:
            cmd = [sys.executable, str(ROOT / script_path)]
            args = best.get("args", [])
            if args:
                cmd.extend(args)
            try:
                r = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=120, cwd=str(ROOT)
                )
                plan["execution"] = {
                    "cmd": " ".join(cmd),
                    "returncode": r.returncode,
                    "stdout": r.stdout[:1000],
                    "stderr": r.stderr[:500],
                }
            except Exception as e:
                plan["execution"] = {"error": str(e)}

    return plan


def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍芯·ASI 系统建设器 — 自然语言驱动系统落地",
        epilog="ASI 即天花板。禁止向 ASI+ 演进。"
    )
    parser.add_argument("query", nargs="?", help="自然语言需求，例如：为估值报告增加PDF导出")
    parser.add_argument("--ceiling-check", action="store_true", help="ASI 天花板协议自检")
    parser.add_argument("--org-chart", action="store_true", help="输出人格科技公司组织架构")
    parser.add_argument("--exec", action="store_true", help="在生成计划后尝试执行匹配脚本（默认仅规划）")
    parser.add_argument("--json", action="store_true", help="JSON 输出")

    args = parser.parse_args()

    registry = _load_registry()

    if args.ceiling_check:
        result = _ceiling_check(registry)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🐉 ASI 天花板协议自检")
            print(f"状态: {result['status']}")
            print(f"人格数: {result['persona_count']}")
            if result["issues"]:
                print("问题:")
                for issue in result["issues"]:
                    print(f"  · {issue}")
            else:
                print("✅ 无异常")
            print(f"DNA: {result['dna']}\n")
        return 0 if result["status"] != "🔴" else 1

    if args.org_chart:
        print(_org_chart(registry))
        return 0

    if not args.query:
        parser.print_help()
        return 0

    plan = _build(args.query, args.exec)

    if plan.get("status", "").startswith("🔴"):
        print(f"\n{plan['status']}")
        print(f"原因: {plan.get('reason')}")
        for issue in plan.get("issues", []):
            print(f"  · {issue}")
        print(f"DNA: {plan['dna']}\n")
        return 1

    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    print(f"\n🐉 龍芯·ASI 系统建设器")
    print(f"需求: {plan['query']}")
    print(f"DNA: {plan['dna']}")
    print(f"天花板检查: {plan['ceiling']}")
    print(f"\n调度人格团队: {', '.join(plan['team'])}")
    print("执行工作流:")
    for pid, name, desc in plan['workflow']:
        print(f"  [{pid}] {name}: {desc}")

    sr = plan.get("script_route", {})
    if sr.get("found"):
        best = sr.get("best", {})
        print(f"\n📦 脚本路由命中: {best.get('name', '未知')}")
        print(f"   路径: {best.get('path', 'N/A')}")
        print(f"   得分: {best.get('score', 0)}")
    else:
        print(f"\n🟡 脚本路由: 未命中强匹配脚本（可手动选择脚本执行）")

    if plan.get("execution"):
        ex = plan["execution"]
        print(f"\n⚙️ 实际执行:")
        print(f"   命令: {ex.get('cmd')}")
        print(f"   返回码: {ex.get('returncode')}")
        if ex.get("stdout"):
            print(f"   输出:\n{ex['stdout']}")
        if ex.get("stderr"):
            print(f"   错误:\n{ex['stderr']}")
    elif args.exec:
        print(f"\n🟡 --exec 已启用，但未命中可执行脚本")
    else:
        print(f"\n💡 这是规划模式。如需执行，请加 --exec")

    print("")
    return 0


if __name__ == "__main__":
    sys.exit(main())
