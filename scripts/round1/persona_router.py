#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人格矩阵路由器
DNA: #龍芯⚡️2026-07-05-ROUND1-PERSONA-ROUTER-v1.0
"""

import json
from pathlib import Path
from typing import Dict, List

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "round1"


class PersonaRouter:
    def __init__(self, registry_path: Path = None):
        self.registry_path = registry_path or (DATA_DIR / "persona_registry.json")
        with open(self.registry_path, "r", encoding="utf-8") as f:
            self.registry = json.load(f)

    def route(self, state_code: int, scene_tags: List[str], priority: str = "normal") -> Dict:
        """
        根据64卦状态码+场景标签选择执行人格。
        匹配规则：状态码命中人格 hexagrams 列表 → 命中；再按场景标签加分。
        """
        best_persona = None
        best_score = -1

        for name, info in self.registry.items():
            score = 0
            if state_code in info.get("hexagrams", []):
                score += 2
            for tag in scene_tags:
                if tag in info.get("scenes", []):
                    score += 1
                if tag in info.get("strengths", []):
                    score += 1

            if priority == "high" and "最终决策" in info.get("role", ""):
                score += 1

            if score > best_score:
                best_score = score
                best_persona = name

        # 兜底：若都没命中，选君子
        if best_persona is None or best_score == 0:
            best_persona = "君子"

        selected = self.registry[best_persona]
        fallback = selected.get("fallback", "龍芯")

        # 置信度简单按 score 映射
        confidence = min(0.95, 0.6 + best_score * 0.1)

        return {
            "selected_persona": best_persona,
            "persona_id": selected["id"],
            "role": selected["role"],
            "confidence": round(confidence, 2),
            "fallback": fallback,
            "score": best_score
        }


if __name__ == "__main__":
    router = PersonaRouter()
    tests = [
        (1, ["主权", "决策"]),
        (44, ["知足", "不争"]),
        (20, ["审计", "验证"]),
        (6, ["争议"])
    ]
    for code, tags in tests:
        print(f"state={code}, tags={tags} →", router.route(code, tags))
