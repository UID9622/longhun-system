# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-ENGINE-WEIGHT_TUNER-FILE1-v1.0-2
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
"""
权重调谐器 · 基于历史数据重新计算wi
DNA: #龍芯⚡️2026-06-17-WEIGHT-TUNER

方法：最大熵原理 + 你的历史误判记录
输入：历史验证记录（正确/错误/硬失败）
输出：新权重wi，保持Σwi=1
"""
import json
from pathlib import Path
from collections import defaultdict


class WeightTuner:
    BASE_WEIGHTS = {
        "F1": 0.25, "F2": 0.15, "F3": 0.15,
        "F4": 0.12, "F5": 0.12, "F6": 0.11, "F7": 0.10
    }

    def __init__(self, history_file: str | None = None):
        self.history = self._load_history(history_file)

    def _load_history(self, filepath):
        """加载历史验证记录"""
        if filepath and Path(filepath).exists():
            return json.loads(Path(filepath).read_text())
        # 默认：空历史，返回基础权重
        return []

    def tune(self) -> dict[str, Any]:
        """
        简单调谐：根据硬失败频率降低对应因子权重
        根据成功验证提高权重
        """
        if not self.history:
            return self.BASE_WEIGHTS

        # 统计各因子硬失败次数
        fail_counts = defaultdict(int)
        success_counts = defaultdict(int)

        for record in self.history:
            factors = record.get("factors", {})
            passed = record.get("passed", False)

            for fi, val in factors.items():
                if val == 0:
                    fail_counts[fi] += 1
                elif passed:
                    success_counts[fi] += 1

        # 计算新权重
        new_weights = {}
        for fi in self.BASE_WEIGHTS.keys():
            # 成功奖励 / 失败惩罚
            s = success_counts.get(fi, 0)
            f = fail_counts.get(fi, 0)
            score = (s + 1) / (f + 1)  # 成功/失败比
            new_weights[fi] = score

        # 归一化
        total = sum(new_weights.values())
        normalized = {k: round(v/total, 4) for k, v in new_weights.items()}

        return normalized


if __name__ == "__main__":
    tuner = WeightTuner()
    # 无历史数据，返回基础权重
    print(json.dumps(tuner.tune(), indent=2))

    # 模拟历史数据测试
    mock_history = [
        {"factors": {"F1": 0.9, "F2": 0.8, "F3": 0.9, "F4": 0.9, "F5": 0, "F6": 0.9, "F7": 0.9}, "passed": False},
        {"factors": {"F1": 0.9, "F2": 0.9, "F3": 0.9, "F4": 0.9, "F5": 0.9, "F6": 0.9, "F7": 0.9}, "passed": True},
    ]
    tuner2 = WeightTuner()
    tuner2.history = mock_history
    print(json.dumps(tuner2.tune(), indent=2))
