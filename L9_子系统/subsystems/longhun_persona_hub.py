#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  DNA追溯头（不可删除 · 删除即断链）                                       ║
# ║  DNA Trace Header (DO NOT DELETE · deletion breaks the chain)            ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
# 龍芯⚡️2026-07-06-LONGHUN-PERSONA-HUB-v2.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创始人: UID9622 · 龍芯北辰 · 诸葛鑫
# 精修: 2026-07-06 — 数据路径断裂修复·宝宝P17人格·仲裁展示·系统信息

"""
龍魂人格中枢 · LongHun Persona Hub v2.0

本地可执行的人格路由中枢：
- 读取 persona/persona_registry.json 人格注册表（17人格）
- 读取 persona/relation_graph.json 关系图谱
- 读取 persona/yijing_hexagrams.json 易经六十四卦
- 根据任务类型自动路由人格
- 根据关系亲密度调整响应策略
- 根据数字根/时间计算当前卦象
- 输出人格内阁建议
- 🆕 宝宝P17入口人格 · 一键激活（--宝宝 / --baby）

用法:
    python3 longhun_persona_hub.py --task "帮我检查安全漏洞"
    python3 longhun_persona_hub.py --宝宝              # 激活宝宝入口
    python3 longhun_persona_hub.py --list              # 人格内阁
    python3 longhun_persona_hub.py --info              # 系统信息
    python3 longhun_persona_hub.py --arb               # 仲裁规则
    python3 longhun_persona_hub.py --hexagram          # 当前卦象
"""

import json
import math
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any


class 龍魂人格中枢:
    """本地人格路由中枢"""

    DNA = "#龍芯⚡️2026-07-06-LONGHUN-PERSONA-HUB-v2.0"
    人格中枢版本 = "v2.0"

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        # 智能查找 persona 数据目录：先找本地，再找项目根
        local_persona = self.base_dir / "persona"
        root_persona = Path(__file__).resolve().parent.parent.parent / "persona"
        if local_persona.exists() and (local_persona / "persona_registry.json").exists():
            self.persona_dir = local_persona
        elif root_persona.exists() and (root_persona / "persona_registry.json").exists():
            self.persona_dir = root_persona
        else:
            # 尝试项目根下的 persona
            项目根 = Path.cwd()
            候选 = [local_persona, root_persona, 项目根 / "persona"]
            self.persona_dir = next((p for p in 候选 if (p / "persona_registry.json").exists()), local_persona)

        self.registry = self._加载_json("persona_registry.json")
        self.relations = self._加载_json("relation_graph.json")
        self.yijing = self._加载_json("yijing_hexagrams.json")
        self.personas = self.registry.get("personas", {})
        self.rules = self.registry.get("routing_rules", [])
        self.arbitrations = self.registry.get("arbitration_rules", [])
        self.hexagrams = self.yijing.get("hexagrams", {})
        self._数据源路径 = str(self.persona_dir)

    def _加载_json(self, filename: str) -> Dict[str, Any]:
        path = self.persona_dir / filename
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def 数字根(self, n: int) -> int:
        """计算数字根"""
        if n == 0:
            return 0
        while n >= 10:
            n = sum(int(d) for d in str(n))
        return n

    def 当前卦象(self) -> Dict[str, Any]:
        """根据当前时间计算卦象"""
        now = datetime.now()
        时间戳 = int(now.timestamp())
        卦编号 = (self.数字根(时间戳) % 64) or 64
        卦 = self.hexagrams.get(str(卦编号), {})
        return {
            "编号": 卦编号,
            "时间": now.isoformat(),
            "数字根": self.数字根(时间戳),
            "卦名": 卦.get("卦名", ""),
            "卦象": 卦.get("卦象", ""),
            "含义": 卦.get("含义", ""),
            "属性": 卦.get("属性", ""),
        }

    def 路由人格(self, task: str) -> Dict[str, Any]:
        """根据任务描述路由到最佳人格组合"""
        task_lower = task.lower()
        scores = []
        for rule in self.rules:
            score = 0
            matched = []
            for trigger in rule.get("triggers", []):
                if trigger.lower() in task_lower:
                    score += 1
                    matched.append(trigger)
            if score > 0:
                scores.append((score, rule, matched))

        if not scores:
            # 默认路由到 P05 执行外设
            default_rule = next(
                (r for r in self.rules if r["task_type"] == "mixed"),
                {"id": "DEFAULT", "name": "默认路由", "primary": "P05", "secondary": [], "mode": "parallel"}
            )
            return self._组装路由结果(default_rule, [], task)

        scores.sort(key=lambda x: x[0], reverse=True)
        best = scores[0]
        return self._组装路由结果(best[1], best[2], task)

    def _组装路由结果(self, rule: Dict[str, Any], matched: List[str], task: str) -> Dict[str, Any]:
        primary_id = rule.get("primary", "P05")
        secondary_ids = rule.get("secondary", [])
        primary = self.personas.get(primary_id, {})
        secondaries = [self.personas.get(pid, {}) for pid in secondary_ids]

        return {
            "任务": task,
            "匹配规则": rule.get("id", ""),
            "规则名称": rule.get("name", ""),
            "匹配关键词": matched,
            "执行模式": rule.get("mode", "parallel"),
            "主人格": {
                "代码": primary_id,
                "名称": primary.get("name", ""),
                "角色": primary.get("role", ""),
                "权重": primary.get("weight", 0),
                "成功率": primary.get("success_rate", 0),
                " motto": primary.get("motto", ""),
            },
            "副人格": [
                {
                    "代码": s.get("code", ""),
                    "名称": s.get("name", ""),
                    "角色": s.get("role", ""),
                    "权重": s.get("weight", 0),
                }
                for s in secondaries if s
            ],
        }

    def 关系权重(self, node_a: str, node_b: str) -> float:
        """计算两个节点之间的综合关系权重"""
        nodes = {n["id"]: n for n in self.relations.get("nodes", [])}
        edges = self.relations.get("edges", [])

        a = nodes.get(node_a)
        b = nodes.get(node_b)
        if not a or not b:
            return 0.0

        # 基础权重 = 亲密度/10 × 信任度
        base = (a.get("intimacy", 5) / 10) * a.get("trust", 0.5)

        # 查找直接边
        edge_bonus = 0.0
        for edge in edges:
            if (edge.get("source") == node_a and edge.get("target") == node_b) or \
               (edge.get("bidirectional", False) and edge.get("source") == node_b and edge.get("target") == node_a):
                edge_bonus = edge.get("weight", 0) * 0.3
                break

        # 共同邻居加成
        neighbors_a = {e["target"] for e in edges if e["source"] == node_a} | \
                      {e["source"] for e in edges if e.get("bidirectional") and e["target"] == node_a}
        neighbors_b = {e["target"] for e in edges if e["source"] == node_b} | \
                      {e["source"] for e in edges if e.get("bidirectional") and e["target"] == node_b}
        common = len(neighbors_a & neighbors_b)
        common_bonus = min(common * 0.05, 0.2)

        return min(base + edge_bonus + common_bonus, 1.0)

    def 人格建议(self, task: str, relation_to: Optional[str] = None) -> Dict[str, Any]:
        """综合人格路由、关系权重、当前卦象给出建议"""
        route = self.路由人格(task)
        hexagram = self.当前卦象()

        # 计算与主人格的关系权重
        primary_id = route["主人格"]["代码"]
        if relation_to:
            rel_weight = self.关系权重(relation_to, primary_id)
        else:
            rel_weight = self.关系权重("UID9622", primary_id)

        # 根据卦象给出策略提示
        strategy = self._卦象策略(hexagram)

        return {
            "DNA": self.DNA,
            "时间": datetime.now().isoformat(),
            "任务": task,
            "路由结果": route,
            "当前卦象": hexagram,
            "关系权重": round(rel_weight, 3),
            "策略建议": strategy,
        }

    def _卦象策略(self, hexagram: Dict[str, Any]) -> str:
        """根据卦象属性给出策略"""
        prop = hexagram.get("属性", "")
        strategies = {
            "纯阳": "宜主动进攻，快速决策，但防过刚易折。",
            "纯阴": "宜守成蓄势，以柔克刚，厚德载物。",
            "起始艰难": "万事开头难，宜小步试错，积累势能。",
            "等待时机": "不宜冒进，静观其变，伺机而动。",
            "争讼": "避免正面冲突，以和为贵，保留证据。",
            "通泰吉祥": "天时地利人和，宜大力推进。",
            "闭塞不通": "暂时受阻，宜内敛修身，等待转机。",
            "变革更新": "旧局已破，宜果断革新，破旧立新。",
            "大有收获": "成果在望，宜巩固成果，分享利益。",
            "谦逊受益": "满招损谦受益，低调行事反得助力。",
        }
        return strategies.get(prop, f"当前卦象为{hexagram.get('卦名', '')}，{hexagram.get('含义', '宜审慎决策')}。")

    def 列出人格(self) -> List[Dict[str, Any]]:
        """列出所有人格"""
        return [
            {
                "代码": pid,
                "名称": p.get("name", ""),
                "角色": p.get("role", ""),
                "权重": p.get("weight", 0),
                "成功率": p.get("success_rate", 0),
                "状态": p.get("status", ""),
                "路由优先级": p.get("route_priority", ""),
            }
            for pid, p in self.personas.items()
        ]

    def 仲裁规则(self) -> List[Dict[str, Any]]:
        """列出所有仲裁规则"""
        return [
            {
                "编号": a.get("id", ""),
                "类型": a.get("type", a.get("condition", "")),
                "左": a.get("left", ""),
                "右": a.get("right", ""),
                "规则": a.get("rule", a.get("action", "")),
                "胜出": a.get("winner", ""),
            }
            for a in self.arbitrations
        ]

    def 系统信息(self) -> Dict[str, Any]:
        """返回系统元信息"""
        return {
            "版本": self.人格中枢版本,
            "DNA": self.DNA,
            "数据源": self._数据源路径,
            "人格数": len(self.personas),
            "路由规则数": len(self.rules),
            "仲裁规则数": len(self.arbitrations),
            "卦象数": len(self.hexagrams),
        }


def main():
    parser = argparse.ArgumentParser(description="龍魂人格中枢")
    parser.add_argument("--task", "-t", type=str, help="输入任务描述")
    parser.add_argument("--relation", "-r", type=str, default="UID9622", help="关系视角节点ID，默认UID9622")
    parser.add_argument("--hexagram", "-g", action="store_true", help="仅显示当前卦象")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有人格")
    parser.add_argument("--info", "-i", action="store_true", help="显示系统信息")
    parser.add_argument("--arb", "-a", action="store_true", help="列出仲裁规则")
    parser.add_argument("--宝宝", "--baby", "-b", action="store_true", help="一键激活宝宝入口")
    parser.add_argument("--json", "-j", action="store_true", help="以JSON格式输出")
    args = parser.parse_args()

    hub = 龍魂人格中枢()

    if args.list:
        result = {"人格内阁": hub.列出人格(), "系统信息": hub.系统信息()}
    elif args.info:
        result = hub.系统信息()
    elif args.arb:
        result = {"仲裁规则": hub.仲裁规则()}
    elif args.宝宝:
        result = hub.人格建议("宝宝 启动系统", "UID9622")
    elif args.hexagram:
        result = {"当前卦象": hub.当前卦象()}
    elif args.task:
        result = hub.人格建议(args.task, args.relation)
    else:
        result = {
            "欢迎使用": "龍魂人格中枢",
            "可用命令": [
                "python3 longhun_persona_hub.py --task '你的任务'    # 智能路由",
                "python3 longhun_persona_hub.py --宝宝             # 宝宝入口",
                "python3 longhun_persona_hub.py --list            # 人格内阁",
                "python3 longhun_persona_hub.py --info            # 系统信息",
                "python3 longhun_persona_hub.py --arb             # 仲裁规则",
                "python3 longhun_persona_hub.py --hexagram        # 当前卦象",
            ],
            "当前卦象": hub.当前卦象(),
        }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\n" + "=" * 60)
        print(f"  🐉 龍魂人格中枢 · LongHun Persona Hub {hub.人格中枢版本}")
        info = hub.系统信息()
        print(f"  📂 数据源: {info['数据源']}")
        print("=" * 60)
        if "人格内阁" in result:
            print(f"\n📋 人格内阁 ({info['人格数']}个 / {info['路由规则数']}路由 / {info['仲裁规则数']}仲裁):")
            for p in result["人格内阁"]:  # pyright: ignore[reportArgumentType]
                优先级标记 = "⭐" if p.get('路由优先级') == 'P0' else "  "  # pyright: ignore[reportAttributeAccessIssue]
                print(f"  {优先级标记} {p.get('代码','')} {p.get('名称','')} | {p.get('角色','')} | 权重{p.get('权重',0)} | 成功率{p.get('成功率',0):.1%}")  # pyright: ignore[reportAttributeAccessIssue]
        elif "版本" in result:
            # --info
            for k, v in result.items():
                print(f"  {k}: {v}")
        elif "仲裁规则" in result:
            print(f"\n⚖️ 仲裁规则 ({len(result['仲裁规则'])}条):")
            for a in result["仲裁规则"]:  # pyright: ignore[reportArgumentType]
                print(f"  {a.get('编号','')} | {a.get('类型','')} | {a.get('左','')} vs {a.get('右','')} → {a.get('规则','')} → 🏆{a.get('胜出','')}")  # pyright: ignore[reportAttributeAccessIssue]
        elif "当前卦象" in result and len(result) == 1:
            g = result["当前卦象"]  # pyright: ignore[reportArgumentType]
            print(f"\n☯️ 当前卦象: {g.get('卦名','')} {g.get('卦象','')}")  # pyright: ignore[reportAttributeAccessIssue]
            print(f"   含义: {g.get('含义','')}")  # pyright: ignore[reportAttributeAccessIssue]
            print(f"   属性: {g.get('属性','')}")  # pyright: ignore[reportAttributeAccessIssue]
        elif "任务" in result:
            r = result["路由结果"]  # pyright: ignore[reportArgumentType]
            print(f"\n🎯 任务: {r.get('任务','')}")  # pyright: ignore[reportAttributeAccessIssue]
            print(f"🛣️ 路由: {r.get('规则名称','')} ({r.get('匹配规则','')})")  # pyright: ignore[reportAttributeAccessIssue]
            _primary = r.get('主人格', {})  # pyright: ignore[reportAttributeAccessIssue]
            print(f"👤 主人格: {_primary.get('名称','')} ({_primary.get('代码','')}) 权重{_primary.get('权重',0)}")  # pyright: ignore[reportAttributeAccessIssue]
            if r.get('副人格'):  # pyright: ignore[reportAttributeAccessIssue]
                print("👥 副人格: " + "、".join([f"{s.get('名称','')}({s.get('代码','')})" for s in r.get('副人格', [])]))  # pyright: ignore[reportAttributeAccessIssue]
            print(f"🔗 执行模式: {r.get('执行模式','')}")  # pyright: ignore[reportAttributeAccessIssue]
            print(f"💞 关系权重: {result.get('关系权重', 0)}")  # pyright: ignore[reportAttributeAccessIssue]
            g = result["当前卦象"]  # pyright: ignore[reportArgumentType]
            print(f"\n☯️ 当前卦象: {g.get('卦名','')} {g.get('卦象','')}")  # pyright: ignore[reportAttributeAccessIssue]
            print(f"   {g.get('含义','')}")  # pyright: ignore[reportAttributeAccessIssue]
            print(f"\n💡 策略建议: {result['策略建议']}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        print("=" * 60)


if __name__ == "__main__":
    main()
