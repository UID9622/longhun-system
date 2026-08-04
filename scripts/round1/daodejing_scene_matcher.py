#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
道德经场景匹配器
DNA: #龍芯⚡️2026-07-05-ROUND1-DAODEJING-SCENE-MATCHER-v1.0
"""

import json
from pathlib import Path
from typing import Dict, List, Any

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "round1"


class DaodejingSceneMatcher:
    def __init__(self, map_path: Path = None):
        self.map_path = map_path or (DATA_DIR / "daodejing_scene_map.json")
        with open(self.map_path, "r", encoding="utf-8") as f:
            self.scene_map = json.load(f)

    def match(self, text: str) -> Dict[str, Any]:
        """对用户输入进行关键词扫描，返回最匹配的道德经章节"""
        text = text.lower()
        best_chapter = None
        best_score = 0
        best_keyword = ""

        for chapter, info in self.scene_map.items():
            for kw in info.get("keywords", []):
                if kw in text:
                    score = len(kw)
                    if score > best_score:
                        best_score = score
                        best_chapter = chapter
                        best_keyword = kw

        if best_chapter:
            info = self.scene_map[best_chapter]
            return {
                "chapter": int(best_chapter),
                "scene": info["scene"],
                "golden_sentence": info["golden_sentence"],
                "matched_keyword": best_keyword,
                "tags": info["tags"],
                "matched": True
            }

        # 默认返回第 81 章：真实、不争
        return {
            "chapter": 81,
            "scene": "真实/不争",
            "golden_sentence": "信言不美，美言不信",
            "matched_keyword": "",
            "tags": ["真实", "不争"],
            "matched": False
        }


if __name__ == "__main__":
    matcher = DaodejingSceneMatcher()
    tests = [
        "我觉得够了，不用再买了",
        "要怎么才能守住本心",
        "人民的数据主权必须留在中国",
        "这次输出逻辑很清楚",
        "快点上线，不用管风险"
    ]
    for t in tests:
        print(t, "→", matcher.match(t))
