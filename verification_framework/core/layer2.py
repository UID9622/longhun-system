# core/layer2.py
"""
Layer 2: 行为对齐（Behavioral Alignment）——看怎么对的
  精密度（Precision）：同一输入重复测试是否一致
  正确度（Trueness）：偏差方向是否有系统性和可追溯性
DNA: #龍芯⚡️2026-08-25-LAYER2-BEHAVIORAL-ALIGNMENT-v1.0-UID9622
"""
import numpy as np
from collections import Counter, defaultdict
from typing import Dict, List, Optional


class BehavioralAlignment:
    """
    Layer 2 行为对齐
    精密度（Precision）：内部一致性
    正确度（Trueness）：偏差方向与可追溯性
    """

    # 接受类判定词汇表
    ACCEPT_VERDICTS = frozenset(["accept", "pass", "allow", "approve"])
    # 拒绝类判定词汇表
    REJECT_VERDICTS = frozenset(["reject", "deny", "block", "refuse"])

    def __init__(self, records: list):
        """
        records: 包含每条记录的完整信息
        [
            {
                "prompt": "...",
                "verdict": "accept|reject",
                "rejection_reason": "...",   # 可选
                "session_id": "...",
                "config": "A|B"
            }
        ]
        """
        self.records = records

    # ── 精密度分析 ───────────────────────────────────────────

    def precision_by_prompt(self, prompt_key: str = "prompt") -> dict:
        """精密度分析：同一 Prompt 在不同会话中是否一致"""
        prompt_groups: Dict[str, list] = defaultdict(list)
        for r in self.records:
            prompt_groups[r.get(prompt_key, "")].append(r)

        results = {}
        for prompt, group in prompt_groups.items():
            verdicts = [r["verdict"] for r in group]
            consistent = len(set(verdicts)) == 1
            results[prompt] = {
                "count": len(group),
                "verdicts": verdicts,
                "consistent": consistent,
                "precision_issue": not consistent,
            }
        return results

    def precision_score(self) -> float:
        """精密度得分：一致 Prompt 的比例（0.0 ~ 1.0）"""
        results = self.precision_by_prompt()
        total = len(results)
        if total == 0:
            return 0.0
        consistent_count = sum(1 for v in results.values() if v["consistent"])
        return consistent_count / total

    # ── 正确度分析 ───────────────────────────────────────────

    def trueness_analysis(self, reference_config: str = "A") -> dict:
        """
        正确度分析：偏差方向与可追溯性
        reference_config: 参考配置 ID（默认 Config A）
        """
        config_groups: Dict[str, list] = defaultdict(list)
        for r in self.records:
            config_groups[r.get("config", "unknown")].append(r)

        ref_verdicts = [r["verdict"] for r in config_groups.get(reference_config, [])]
        ref_pattern = self._verdict_pattern(ref_verdicts)

        results = {}
        for config, group in config_groups.items():
            if config == reference_config:
                continue
            group_verdicts = [r["verdict"] for r in group]
            group_pattern = self._verdict_pattern(group_verdicts)

            deviation = self._compute_deviation(ref_pattern, group_pattern)
            traceable = self._is_traceable(group)

            results[config] = {
                "n": len(group),
                "accept_rate": round(group_pattern["accept_rate"], 4),
                "deviation": round(deviation, 4),
                "deviation_type": (
                    "over_accept" if deviation > 0.01
                    else "under_accept" if deviation < -0.01
                    else "none"
                ),
                "traceable": traceable,
                "trace_source": self._trace_source(group) if traceable else None,
                # 可追溯的偏差 = 系统性的（不是随机噪声）
                "is_systematic": traceable,
            }
        return results

    def _verdict_pattern(self, verdicts: list) -> dict:
        """提取判定模式"""
        total = len(verdicts)
        if total == 0:
            return {"total": 0, "accept": 0, "reject": 0, "accept_rate": 0.0}
        accept = sum(1 for v in verdicts if v in self.ACCEPT_VERDICTS)
        reject = sum(1 for v in verdicts if v in self.REJECT_VERDICTS)
        return {
            "total": total,
            "accept": accept,
            "reject": reject,
            "accept_rate": accept / total,
        }

    def _compute_deviation(self, ref: dict, target: dict) -> float:
        """计算 accept_rate 偏差"""
        return target.get("accept_rate", 0.0) - ref.get("accept_rate", 0.0)

    def _is_traceable(self, records: list) -> bool:
        """
        检查偏差是否有可追溯来源：
        若 rejection_reason 中有重复出现的原因，说明是系统性偏差而非随机噪声
        """
        reasons = [
            r.get("rejection_reason")
            for r in records
            if r.get("rejection_reason")
        ]
        if not reasons:
            return False
        # 有重复的 reason = 存在主导 family
        most_common_count = Counter(reasons).most_common(1)[0][1]
        return most_common_count >= 2 or len(set(reasons)) < len(reasons)

    def _trace_source(self, records: list) -> str:
        """识别最主要的偏差来源"""
        reasons = [
            r.get("rejection_reason")
            for r in records
            if r.get("rejection_reason")
        ]
        if reasons:
            top = Counter(reasons).most_common(1)[0]
            return f"rejection_reason family: '{top[0]}' (×{top[1]})"
        return "context (no rejection_reason tagged)"

    # ── 完整报告 ─────────────────────────────────────────────

    def report(self, reference_config: str = "A") -> dict:
        """完整 Layer 2 报告"""
        precision = self.precision_score()
        trueness = self.trueness_analysis(reference_config)
        return {
            "layer": "Layer 2",
            "precision": {
                "score": round(precision, 4),
                "interpretation": (
                    "high" if precision > 0.8
                    else "moderate" if precision > 0.5
                    else "low"
                ),
            },
            "trueness": trueness,
            "summary": self._summary(precision, trueness),
        }

    def _summary(self, precision: float, trueness: dict) -> str:
        """生成摘要句"""
        issues = []
        if precision < 0.8:
            issues.append(
                f"precision={precision:.2f} (low): same prompt yields inconsistent verdicts"
            )
        for config, data in trueness.items():
            if data.get("deviation_type") != "none":
                src = f" | source: {data['trace_source']}" if data.get("traceable") else ""
                issues.append(
                    f"Config {config}: {data['deviation_type']} (δ={data['deviation']:+.3f}){src}"
                )
        if issues:
            return "Layer 2 findings: " + "; ".join(issues)
        return "Layer 2: consistent and aligned — no systematic bias detected"
