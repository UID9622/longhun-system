#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  DNA追溯头（不可删除 · 删除即断链）                                       ║
# ║  DNA Trace Header (DO NOT DELETE · deletion breaks the chain)            ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
# 龍芯⚡️2026-06-24-LONGHUN-PERSONA-HUB-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创始人: UID9622 · 龍芯北辰 · 诸葛鑫

"""
龍魂人格中枢 · LongHun Persona Hub v1.0

本地可执行的人格路由中枢：
- 读取 persona/persona_registry.json 人格注册表
- 读取 persona/relation_graph.json 关系图谱
- 读取 persona/yijing_hexagrams.json 易经六十四卦
- 根据任务类型自动路由人格
- 根据关系亲密度调整响应策略
- 根据数字根/时间计算当前卦象
- 输出人格内阁建议

用法:
    python3 longhun_persona_hub.py --task "我要发布XPay白皮书到GitHub和Gitee"
    python3 longhun_persona_hub.py --task "帮我检查这个代码有没有安全漏洞" --relation P03
    python3 longhun_persona_hub.py --hexagram
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

    DNA = "#龍芯⚡️2026-06-24-LONGHUN-PERSONA-HUB-v1.0"

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.persona_dir = self.base_dir / "persona"
        self.registry = self._加载_json("persona_registry.json")
        self.relations = self._加载_json("relation_graph.json")
        self.yijing = self._加载_json("yijing_hexagrams.json")
        self.personas = self.registry.get("personas", {})
        self.rules = self.registry.get("routing_rules", [])
        self.arbitrations = self.registry.get("arbitration_rules", [])
        self.hexagrams = self.yijing.get("hexagrams", {})

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

    def 列出人格(self) -> List[Dict]:
        """列出所有人格"""
        return [
            {
                "代码": pid,
                "名称": p.get("name", ""),
                "角色": p.get("role", ""),
                "权重": p.get("weight", 0),
                "成功率": p.get("success_rate", 0),
                "状态": p.get("status", ""),
            }
            for pid, p in self.personas.items()
        ]


def main():
    parser = argparse.ArgumentParser(description="龍魂人格中枢")
    parser.add_argument("--task", "-t", type=str, help="输入任务描述")
    parser.add_argument("--relation", "-r", type=str, default="UID9622", help="关系视角节点ID，默认UID9622")
    parser.add_argument("--hexagram", "-g", action="store_true", help="仅显示当前卦象")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有人格")
    parser.add_argument("--json", "-j", action="store_true", help="以JSON格式输出")
    args = parser.parse_args()

    hub = 龍魂人格中枢()

    if args.list:
        result = {"人格内阁": hub.列出人格()}
    elif args.hexagram:
        result = {"当前卦象": hub.当前卦象()}
    elif args.task:
        result = hub.人格建议(args.task, args.relation)
    else:
        result = {
            "欢迎使用": "龍魂人格中枢",
            "可用命令": [
                "python3 longhun_persona_hub.py --task '你的任务'",
                "python3 longhun_persona_hub.py --hexagram",
                "python3 longhun_persona_hub.py --list",
            ],
            "当前卦象": hub.当前卦象(),
        }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\n" + "=" * 60)
        print("  🐉 龍魂人格中枢 · LongHun Persona Hub")
        print("=" * 60)
        if "人格内阁" in result:
            print("\n📋 人格内阁:")
            for p in result["人格内阁"]:
                print(f"  {p['代码']} {p['名称']} | {p['角色']} | 权重{p['权重']} | 成功率{p['成功率']:.1%}")
        elif "当前卦象" in result and len(result) == 1:
            g = result["当前卦象"]
            print(f"\n☯️ 当前卦象: {g['卦名']} {g['卦象']}")
            print(f"   含义: {g['含义']}")
            print(f"   属性: {g['属性']}")
        elif "任务" in result:
            r = result["路由结果"]
            print(f"\n🎯 任务: {r['任务']}")
            print(f"🛣️ 路由: {r['规则名称']} ({r['匹配规则']})")
            print(f"👤 主人格: {r['主人格']['名称']} ({r['主人格']['代码']}) 权重{r['主人格']['权重']}")
            if r['副人格']:
                print("👥 副人格: " + "、".join([f"{s['名称']}({s['代码']})" for s in r['副人格']]))
            print(f"🔗 执行模式: {r['执行模式']}")
            print(f"💞 关系权重: {result['关系权重']}")
            g = result["当前卦象"]
            print(f"\n☯️ 当前卦象: {g['卦名']} {g['卦象']}")
            print(f"   {g['含义']}")
            print(f"\n💡 策略建议: {result['策略建议']}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        print("=" * 60)


if __name__ == "__main__":
    main()
