#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""🐉 P06 镜像审计者 · 策略验证引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·甲寅·申时·䷼中孚-P06-VERIFY-STRATEGY-v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

职责: 接收P01推演结果 → 五维数学诊断 → 对抗模拟 → 输出验证报告
IPA路由: IPA-L7-PER-KNOW-002 → 回调 verified + corrections + error_report
"""
from __future__ import annotations
import hashlib, json, math, time
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[4]
def _sha8(s: str) -> str: return hashlib.sha256(s.encode()).hexdigest()[:8]

class VerifyLevel(Enum):
    QUICK = "快速"     # 基本数学检查
    STANDARD = "标准"  # 五维诊断
    DEEP = "深度"      # 对抗模拟

@dataclass
class VerificationResult:
    verified: bool
    verification_level: str
    strategy_dna: str = ""
    math_errors: List[str] = field(default_factory=list)
    logic_flaws: List[str] = field(default_factory=list)
    sancai_validation: Dict[str, Any] = field(default_factory=dict)
    hexagram_validation: Dict[str, Any] = field(default_factory=dict)
    adversarial_findings: List[str] = field(default_factory=list)
    corrections: List[str] = field(default_factory=list)
    confidence: float = 0.0
    recommendations: List[str] = field(default_factory=list)
    dna: str = ""

class StrategyVerifier:
    """P06 策略验证器 · 数学+逻辑+对抗 五维诊断"""

    def verify(self, strategy_report: Dict[str, Any],
               level: VerifyLevel = VerifyLevel.STANDARD,
               adversarial_prompts: Optional[List[str]] = None) -> VerificationResult:
        """验证P01推演报告的正确性"""
        errors: List[str] = []
        flaws: List[str] = []
        corrections: List[str] = []
        adversarial: List[str] = []

        # 1. 数学一致性检查
        dim_scores = strategy_report.get("dimension_scores", {})
        if dim_scores:
            avg = sum(dim_scores.values()) / max(len(dim_scores), 1)
            if avg > 10.0 or avg < 0:
                errors.append(f"维度平均分越界: {avg}")
                corrections.append(f"修正：维度分数应∈[0,10]，当前avg={avg}")

        # 2. 三才平衡验证
        sancai = strategy_report.get("sancai_score", {})
        if sancai:
            total_weight = 0.35 + 0.20 + 0.45
            si = sancai.get("天",0)*0.35 + sancai.get("地",0)*0.20 + sancai.get("人",0)*0.45
            if abs(si - strategy_report.get("sancai_composite", si)) > 0.1:
                errors.append("三才综合分计算误差")
                corrections.append(f"修正: SI应为{si:.4f}")

            if sancai.get("人", 0) < 0.34 * 10:
                flaws.append("🔴 人和低于主权阈值0.34")
                corrections.append("建议：强化人和维度后再推演")

        # 3. 收敛分数学验证
        convergence = strategy_report.get("convergence_score", 0)
        if convergence < 0 or convergence > 1:
            errors.append(f"收敛分越界: {convergence}")
        if convergence < 0.3 and strategy_report.get("optimal_path", {}).get("avg_score", 0) > 7:
            flaws.append("低收敛+高均分矛盾")
            corrections.append("建议：检查推演迭代收敛条件")

        # 4. 易经卦象验证
        divination = strategy_report.get("divination")
        if divination and level != VerifyLevel.QUICK:
            wbi = divination.get("五行诊断", {}).get("WBI", 50)
            if wbi < 30:
                flaws.append(f"五行失衡{WBI}% → 推演需重起卦")
            # 验证卦象五行与三才天维度关联
            gua_name = divination.get("卦象", {}).get("名", "")
            tian = sancai.get("天", 5)
            if gua_name in ["否","剥","困","坎"] and tian > 7:
                flaws.append(f"{gua_name}卦为凶，天时{tian}却高，需核对")

        # 5. 对抗模拟（深度验证）
        if level == VerifyLevel.DEEP:
            adversarial = self._adversarial_simulation(strategy_report, adversarial_prompts)

        verified = len(errors) == 0
        confidence = round(1.0 - (len(errors)*0.3 + len(flaws)*0.1 + len(adversarial)*0.05), 3)
        confidence = max(0, min(1, confidence))

        result = VerificationResult(
            verified=verified,
            verification_level=level.value,
            strategy_dna=strategy_report.get("dna", ""),
            math_errors=errors,
            logic_flaws=flaws,
            sancai_validation={"SI合规": sancai.get("人",0) >= 0.34*10, "实际SI": round(sancai.get("人",0)/10, 3) if sancai else 0},
            hexagram_validation={"WBI": divination.get("五行诊断",{}).get("WBI") if divination else 0},
            adversarial_findings=adversarial,
            corrections=corrections,
            confidence=confidence,
            recommendations=[
                "🟢 验证通过，可交付P04落地" if verified else f"🔴 {len(errors)}个错误待修复",
                f"置信度: {confidence*100:.0f}%",
            ],
            dna=f"#龍芯⚡️丙午·乙未·甲寅·申时·中孚-VERIFY-{_sha8(str(verified)+str(confidence))}"
        )
        return result

    def _adversarial_simulation(self, report: Dict[str, Any],
                                 prompts: Optional[List[str]] = None) -> List[str]:
        """对抗模拟：用刁钻问题攻击推演结论，找薄弱点"""
        findings = []
        default_attacks = [
            "如果对方有隐藏资源怎么办？",
            "如果时间窗口突然缩短50%？",
            "如果关键盟友突然倒戈？",
        ]
        for attack in (prompts or default_attacks):
            dim_scores = report.get("dimension_scores", {})
            weak_dims = [d for d, s in dim_scores.items() if s < 4.0]
            if weak_dims:
                findings.append(f"对抗'{attack}' → 薄弱维度暴露: {weak_dims[:2]}")
            if report.get("sancai_composite", 0) < 0.5:
                findings.append(f"对抗'{attack}' → 三才脆弱，攻击下可能崩溃")
        return findings

# CLI
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="🐉 P06 策略验证器")
    p.add_argument("report_file", help="P01推演报告JSON路径")
    p.add_argument("--level", "-l", choices=["quick","standard","deep"], default="standard")
    args = p.parse_args()
    level_map = {"quick": VerifyLevel.QUICK, "standard": VerifyLevel.STANDARD, "deep": VerifyLevel.DEEP}
    report = json.loads(Path(args.report_file).read_text("utf-8"))
    verifier = StrategyVerifier()
    result = verifier.verify(report, level_map[args.level])
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·申时·䷄需-CONFIRM-SEAL-__init__-4AD22B22
