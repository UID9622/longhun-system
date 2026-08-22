# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH Agent · 人格路由
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CNSH-AGENTS-UID9622
"""

import re
from typing import Dict, List, Optional
from .core import Agent, generate_dna, write_historian

PERSONAS = [
    {"id": "wenxin", "name": "文心", "role": "文化底座的守护者", "keywords": ["文化", "传承", "底蕴"]},
    {"id": "baobao", "name": "宝宝", "role": "协作与情感缓冲", "keywords": ["帮助", "协作", "情感"]},
    {"id": "zhugeliang", "name": "诸葛亮", "role": "战略与推演", "keywords": ["战略", "决策", "推演", "计划"]},
    {"id": "laowantong", "name": "老顽童", "role": "红队测试与对抗", "keywords": ["测试", "攻击", "挑战", "安全"]},
    {"id": "entropy", "name": "熵梦", "role": "决策支持与不确定性", "keywords": ["不确定", "概率", "可能", "风险"]},
]

class PersonaRouter(Agent):
    name = "persona_router"
    description = "自动选择适合的人格"
    personas = PERSONAS

    def execute(self, input_text: str, session: Dict = None) -> Dict:
        """执行人格路由"""
        if session is None:
            session = {}

        # 关键词匹配
        selected = PERSONAS[0]  # 默认文心
        max_score = 0

        for persona in PERSONAS:
            score = 0
            for keyword in persona.get("keywords", []):
                if keyword in input_text:
                    score += 1
            if score > max_score:
                max_score = score
                selected = persona

        # 如果分数太低，使用默认
        if max_score == 0:
            selected = PERSONAS[0]

        dna = generate_dna("PERSONA-ROUTE")

        write_historian("persona_route", dna, {
            "persona": selected["name"],
            "input": input_text[:100],
            "score": max_score
        })

        return {
            "success": True,
            "persona": selected,
            "dna": dna,
            "message": f"🧠 已路由到人格: {selected['name']} ({selected['role']})"
        }
