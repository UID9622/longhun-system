# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-ENGINE-L4_SEVEN_FACTOR-FILE1-v1.0-2
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
"""
L4 七因子签名层 · 直接复用 Behavioral Cryptography
DNA: #龍芯⚡️2026-06-17-L4-SEVEN-FACTOR
"""
import json
import math
from pathlib import Path


class SevenFactorLayer:
    WEIGHTS = {
        "F1": 0.25, "F2": 0.15, "F3": 0.15,
        "F4": 0.12, "F5": 0.12, "F6": 0.11, "F7": 0.10
    }
    THRESHOLD_STD = 0.85
    THRESHOLD_HIGH = 0.95

    def __init__(self, uid="UID9622"):
        self.uid = uid
        self.dna_file = Path(f"~/longhun-system/skills/skill-11-persona-dna/dna_{uid}.json").expanduser()

    def compute(self, factors: dict[str, Any]) -> dict[str, Any]:
        """
        factors = {"F1": 0.9, "F2": 0.8, ...}
        任一因子为0 → conf=0（硬失败）
        """
        conf = 1.0
        hard_fail = False
        fail_reason = None

        for key, weight in self.WEIGHTS.items():
            fi = factors.get(key, 0.0)
            if fi == 0:
                hard_fail = True
                fail_reason = f"{key}=0"
                conf = 0
                break
            conf *= math.pow(fi, weight)

        return {
            "layer": "L4",
            "confidence": round(conf, 4),
            "threshold": self.THRESHOLD_STD,
            "passed": conf >= self.THRESHOLD_STD and not hard_fail,
            "hard_fail": hard_fail,
            "fail_reason": fail_reason,
            "factors": factors
        }


if __name__ == "__main__":
    l4 = SevenFactorLayer()
    # 测试：全因子0.9
    test_factors = {f"F{i}": 0.9 for i in range(1, 8)}
    print(json.dumps(l4.compute(test_factors), indent=2))

    # 测试：F5=0（硬失败）
    test_fail = {f"F{i}": 0.9 for i in range(1, 8)}
    test_fail["F5"] = 0
    print(json.dumps(l4.compute(test_fail), indent=2))
