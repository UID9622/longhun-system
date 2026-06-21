# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-ENGINE-STACK_RUNNER-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

#!/usr/bin/env python3
"""
六层堆栈运行器 · 逐层验证
DNA: #龍芯⚡️2026-06-17-STACK-RUNNER
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from l1_physical import PhysicalLayer
from l4_seven_factor import SevenFactorLayer


class CryptoStack:
    def __init__(self, uid="UID9622"):
        self.uid = uid
        self.l1 = PhysicalLayer()
        self.l4 = SevenFactorLayer(uid)
        self.results = {}

    def run(self, seven_factors: dict = None):
        """运行全栈验证"""
        # L1: 物理层
        self.results["L1"] = self.l1.export()

        # L4: 七因子层（如果提供因子）
        if seven_factors:
            self.results["L4"] = self.l4.compute(seven_factors)

        # 总评
        all_passed = all(
            r.get("passed", True) for r in self.results.values()
        )

        return {
            "stack": "龍魂祖传加密堆栈",
            "version": "v1.0-engineering",
            "uid": self.uid,
            "layers": self.results,
            "overall_passed": all_passed,
            "dna": "#龍芯⚡️2026-06-17-STACK-RUNNER"
        }


if __name__ == "__main__":
    stack = CryptoStack()
    # 测试：无七因子（只跑L1）
    print(json.dumps(stack.run(), indent=2, ensure_ascii=False))

    # 测试：带七因子
    factors = {f"F{i}": 0.92 for i in range(1, 8)}
    print(json.dumps(stack.run(factors), indent=2, ensure_ascii=False))
