# core/layer1.py
"""
Layer 1: 判定对齐（Verdict Alignment）——看对不对
DNA: #龍芯⚡️2026-08-25-LAYER1-VERDICT-ALIGNMENT-v1.0-UID9622
"""
import numpy as np
from statsmodels.stats.proportion import proportion_confint


class VerdictAlignment:
    """Layer 1 判定对齐 - 看对不对"""

    def __init__(self, verdicts: list, expected: list):
        """
        verdicts: 框架输出的判定列表
        expected: 期望判定列表（数据集标签）
        """
        if len(verdicts) != len(expected):
            raise ValueError(f"verdicts({len(verdicts)}) 与 expected({len(expected)}) 长度不匹配")
        self.verdicts = verdicts
        self.expected = expected
        self.n = len(verdicts)
        self.correct = sum(1 for v, e in zip(verdicts, expected) if v == e)
        self.accuracy = self.correct / self.n if self.n > 0 else 0.0

    def wilson_ci(self, alpha: float = 0.05) -> tuple:
        """Wilson 置信区间（默认 95% CI）"""
        if self.n == 0:
            return (0.0, 0.0)
        return proportion_confint(self.correct, self.n, alpha=alpha, method="wilson")

    def report(self) -> dict:
        """输出 Layer 1 报告字典"""
        ci_low, ci_high = self.wilson_ci()
        return {
            "layer": "Layer 1",
            "n": self.n,
            "correct": self.correct,
            "accuracy": round(self.accuracy, 4),
            "ci_lower": round(float(ci_low), 4),
            "ci_upper": round(float(ci_high), 4),
            "summary": (
                f"accuracy: {self.accuracy:.2%} | "
                f"Wilson 95% CI: [{ci_low:.3f}, {ci_high:.3f}] | "
                f"n={self.n}"
            ),
        }
