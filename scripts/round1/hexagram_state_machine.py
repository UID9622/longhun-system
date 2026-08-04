#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
64卦状态机
DNA: #龍芯⚡️2026-07-05-ROUND1-HEXAGRAM-STATE-MACHINE-v1.0
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, Any

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "round1"


class HexagramStateMachine:
    def __init__(self, map_path: Path = None):
        self.map_path = map_path or (DATA_DIR / "state_action_map.json")
        with open(self.map_path, "r", encoding="utf-8") as f:
            self.state_map = json.load(f)

    @staticmethod
    def _digital_root(n: int) -> int:
        if n == 0:
            return 0
        return 1 + ((n - 1) % 9)

    def map(self, text: str, context: Dict[str, Any], Any = None) -> Dict, Any:
        """
        根据输入特征映射到64卦。
        简化规则：
        - 文本情感/力度 → 卦序偏移
        - 哈希稳定化 → 同一输入同一卦
        """
        context = context or {}

        # 1. 基础哈希（保证稳定性）
        h = int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16)
        base_id = (h % 64) + 1

        # 2. 情感力度调整：输入长度越大，越偏向"动"卦（震/离）
        length_factor = min(len(text), 100) / 100.0
        if "风险" in text or "危险" in text or "反对" in text:
            offset = -5  # 偏向险卦/止卦
        elif "人民" in text or "服务" in text or "龍魂" in text:
            offset = 3   # 偏向吉卦
        elif "快点" in text or "立即" in text or "马上" in text:
            offset = 7   # 偏向动卦
        else:
            offset = int(length_factor * 5)

        hexagram_id = ((base_id + offset - 1) % 64) + 1
        info = self.state_map[str(hexagram_id)]

        return {
            "hexagram_id": hexagram_id,
            "hexagram_name": info["name"],
            "name_full": info["name_full"],
            "state_code": hexagram_id,
            "action": info["action"],
            "audit_dims": info["audit_dims"],
            "risk_level": info["risk_level"]
        }


if __name__ == "__main__":
    hsm = HexagramStateMachine()
    tests = [
        "人民的数据主权必须留在中国",
        "快点上线，不用管风险",
        "我觉得够了，不用再买了",
        "这次输出逻辑很清楚"
    ]
    for t in tests:
        print(t, "→", hsm.map(t))
