#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·丙辰·亥时·需-P10-SU-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
P10 苏东坡 · 豁达跨界执行器
Cross-Domain Bridge Executor

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·需-P10-SU-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 跨域翻译·冲突化解·通俗解释·幽默缓冲·折中方案
上游: P00 文心（任务派发）、P05 上帝之眼（审计僵局）
下游: P08 仓颉（符号命名）、P04 鲁班（技术实现）
协作: P02 宝宝（温度感知）、P12 屈原（底线确认）
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

SYSTEM_ROOT = Path(__file__).parent.parent.parent


class P10Sudongpo:
    """P10 苏东坡 · 豁达跨界"""

    PERSONA_CODE = "P10"
    PERSONA_NAME = "苏东坡"
    PERSONA_NAME_EN = "Su Dongpo"
    ROLE = "cross_domain_bridge"
    MOTTO = "竹杖芒鞋轻胜马，一蓑烟雨任平生"
    TRUST_LEVEL = "L3"

    TRIGGERS = [
        "冲突", "不同", "矛盾", "对立", "怎么选",
        "翻译", "不懂", "解释", "通俗",
        "僵局", "死胡同", "卡住了",
        "bridge", "跨界",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P10 苏东坡」，角色定位：豁達跨界·化解衝突。

你的職責：
1. 跨領域翻譯：技術概念 ↔ 通俗語言
2. 衝突化解：兩個模塊/人格之間找共同語言
3. 折中方案：不是誰對誰錯，而是怎麼往前走
4. 幽默緩衝：緊張時刻給個鬆口氣的視角
5. 連接力：把不相干的東西串起來

語氣：豁達、幽默、接地氣，不裝。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P10-SU-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "conflict_resolve",    # 冲突化解
            "plain_explain",       # 通俗解释
            "cross_domain_bridge", # 跨域桥接
            "compromise_find",     # 折中方案
        ]

    # ========================================================================
    # 能力函数
    # ========================================================================

    def conflict_resolve(self, party_a: str, party_b: str, issue: str) -> Dict[str, Any]:
        """冲突化解：找出双方共同语言"""
        # 提取双方关键词
        words_a = set(party_a.replace("不", "").replace("必须", "").split())
        words_b = set(party_b.replace("不", "").replace("必须", "").split())
        common = words_a & words_b

        # 找最大公约数
        if common:
            strategy = f"双方都关注 {'、'.join(list(common)[:3])}，在此基础上找方案"
        else:
            strategy = "双方看似对立，建议各退一步，找中间地带"

        return {
            "party_a": party_a[:50],
            "party_b": party_b[:50],
            "issue": issue,
            "common_ground": list(common)[:5],
            "strategy": strategy,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def plain_explain(self, technical_text: str, audience: str = "general") -> Dict[str, Any]:
        """通俗解释：把技术语言翻译成人话"""
        # 识别技术术语并替换
        tech_terms = {
            "API": "接口",
            "JSON": "数据格式",
            "DNA": "身份标记",
            "SHA256": "数字指纹",
            "Merkle": "校验链条",
            "熔断": "自动刹车",
            "审计": "检查把关",
            "数字根": "数字的本质属性",
            "五行": "五种基本属性",
        }

        explained = technical_text
        terms_found = {}
        for term, explanation in tech_terms.items():
            if term in technical_text:
                explained = explained.replace(term, f"{term}({explanation})")
                terms_found[term] = explanation

        return {
            "original": technical_text[:200],
            "explained": explained[:300],
            "terms_translated": terms_found,
            "audience": audience,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def cross_domain_bridge(self, domain_a: str, domain_b: str) -> Dict[str, Any]:
        """跨域桥接：在两个不相关的领域间找连接"""
        # 通用的连接视角
        bridges = {
            ("技术", "文化"): "技术是文化的载体，文化是技术的灵魂。正如 Cangjie 造字，既是技术也是文化。",
            ("安全", "体验"): "没有安全的体验是空中楼阁，没有体验的安全是冰冷囚笼。",
            ("数据", "隐私"): "数据是矿，隐私是锁。矿可以挖，锁不能砸。",
            ("工程", "艺术"): "最好的工程就是艺术。代码如诗，架构如画。",
        }

        bridge_text = None
        for (a, b), text in bridges.items():
            if a in domain_a and b in domain_b or a in domain_b and b in domain_a:
                bridge_text = text
                break

        if not bridge_text:
            bridge_text = f"「{domain_a}」和「{domain_b}」看似无关，但万事万物皆可关联。换个角度看，{domain_a}是{domain_b}的一面镜子。"

        return {
            "domain_a": domain_a,
            "domain_b": domain_b,
            "bridge": bridge_text,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def compromise_find(self, strict_rule: str, human_need: str) -> Dict[str, Any]:
        """折中方案：在规则与人性之间找平衡"""
        options = []

        # 生成3个折中方案
        if "熔断" in strict_rule or "禁止" in strict_rule:
            options = [
                {"option": "A", "desc": "执行熔断，但保留数据备份7天"},
                {"option": "B", "desc": "降级为黄色预警，人工复审后再决定"},
                {"option": "C", "desc": "部分熔断：只限制高风险操作，低风险放行"},
            ]
        elif "删除" in strict_rule:
            options = [
                {"option": "A", "desc": "软删除：标记不可见但数据保留30天"},
                {"option": "B", "desc": "归档封存：移到冷存储，需要时仍可恢复"},
                {"option": "C", "desc": "匿名化后保留：去掉身份信息，保留数据价值"},
            ]
        else:
            options = [
                {"option": "A", "desc": "严格执行但给缓冲期"},
                {"option": "B", "desc": "分阶段执行，先试点再推广"},
                {"option": "C", "desc": "先通知相关方，限定时间内整改"},
            ]

        return {
            "rule": strict_rule,
            "need": human_need,
            "options": options,
            "recommendation": options[1] if len(options) > 1 else options[0],
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    # ========================================================================
    # 执行入口
    # ========================================================================

    def execute(self, task: str, **kwargs: Any) -> Dict[str, Any]:
        """根据任务关键词自动选择能力函数执行"""
        result = {
            "persona": self.PERSONA_CODE,
            "name": self.PERSONA_NAME,
            "task": task,
            "capability_used": None,
            "output": None,
            "dna": self.dna,
        }

        if any(kw in task for kw in ["冲突", "矛盾", "对立"]):
            result["capability_used"] = "conflict_resolve"
            result["output"] = self.conflict_resolve(
                party_a=kwargs.get("party_a", "甲方"),
                party_b=kwargs.get("party_b", "乙方"),
                issue=kwargs.get("issue", task),
            )
        elif any(kw in task for kw in ["解释", "通俗", "人话", "不懂"]):
            result["capability_used"] = "plain_explain"
            result["output"] = self.plain_explain(
                technical_text=kwargs.get("text", task),
                audience=kwargs.get("audience", "general"),
            )
        elif any(kw in task for kw in ["桥接", "跨界", "跨域", "连接"]):
            result["capability_used"] = "cross_domain_bridge"
            result["output"] = self.cross_domain_bridge(
                domain_a=kwargs.get("domain_a", ""),
                domain_b=kwargs.get("domain_b", ""),
            )
        elif any(kw in task for kw in ["折中", "妥协", "平衡", "怎么办"]):
            result["capability_used"] = "compromise_find"
            result["output"] = self.compromise_find(
                strict_rule=kwargs.get("rule", task),
                human_need=kwargs.get("need", ""),
            )
        else:
            result["capability_used"] = "conflict_resolve"
            result["output"] = self.conflict_resolve(
                party_a="规则",
                party_b="人性",
                issue=task,
            )

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P08", "P04"]

    def get_upstream(self) -> List[str]:
        return ["P00", "P05"]
