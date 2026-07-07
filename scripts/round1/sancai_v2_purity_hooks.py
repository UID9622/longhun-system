#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三才 v2.0 · 五阶纯净链评测器 + 叄循环钩子系统
DNA: #龍芯⚡️2026-07-07-SANCAI-V2-PURITY-HOOKS-v1.0

论文公式落地：
  公式(5): P: I(初心) → D(用心) → C(在乎) → S(认真) → L(有爱)
  定理2: L ⇔ I ∧ D ∧ C ∧ S (有爱需要全部五阶，不可跳过)
  论文附录: 叄循环检查(执行模块, 行为输出, 用户) 钩子伪代码 → 可执行实现

核心洞察（Lucky UID9622）:
  "毕竟我们初心干净，也很用心。用心了就会在乎，在乎了就会认真，
   认真了，我们的元宇宙就有爱了。"

不可跳过定理: 初心 → 有爱 不能直接（论文图5虚线箭头）。
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: UP035


# ═══════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════

@dataclass
class PurityScore:
    """五阶纯净链评分"""
    stage_scores: Dict[str, float]  # {"初心": 0.9, "用心": 0.85, ...}
    love_index: float               # 爱度 = 初心×用心×在乎×认真
    has_love: bool                  # L > 0.7 ?
    skippable: bool = False         # 不可跳过！
    verdict: str = ""
    details: Dict[str, str] = field(default_factory=dict)


@dataclass
class HookResult:
    """叄循环钩子检查结果"""
    yi_complete: bool          # 壹完整性
    er_tricolor_ok: bool       # 贰三色合规
    san_love_enough: bool      # 叄爱度达标
    purity: PurityScore        # 纯净链评分
    overall: str               # 🟢/🟡/🔴
    message: str
    dna: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# ═══════════════════════════════════════════════════════════════
# 五阶纯净链评测器
# ═══════════════════════════════════════════════════════════════

class PurityChainEvaluator:
    """
    五阶纯净链评测器

    论文定义5: P: I → D → C → S → L
    论文定理2: L ⇔ I ∧ D ∧ C ∧ S
    """

    DNA = "#龍芯⚡️2026-07-07-PURITY-CHAIN-v1.0"

    # 每阶评测关键词权重
    STAGE_KEYWORDS = {
        "初心": {
            "positive": {
                "人民": 0.20, "主权": 0.20, "为人民": 0.25,
                "数据归集": 0.20, "不删": 0.15, "追溯": 0.15,
                "长期": 0.15, "传承": 0.15, "中国": 0.20,
                "文化": 0.10, "开源": 0.10,
            },
            "negative": {
                "商业化": -0.30, "国际接轨": -0.25, "灵活处理": -0.25,
                "简化": -0.15, "技术无国界": -0.40, "用户体验优先": -0.30,
            },
            "base": 0.40,
        },
        "用心": {
            "positive": {
                "测试": 0.15, "验证": 0.15, "文档": 0.10,
                "结构": 0.10, "完整": 0.15, "边界": 0.10,
                "异常": 0.10, "兜底": 0.10, "降级": 0.10,
            },
            "negative": {
                "TODO": -0.10, "临时": -0.10, "hack": -0.20,
                "workaround": -0.15,
            },
            "base": 0.45,
        },
        "在乎": {
            "positive": {
                "安全": 0.15, "审计": 0.15, "熔断": 0.15,
                "合规": 0.15, "三色": 0.15, "确认": 0.10,
                "边界": 0.10, "底线": 0.15, "红线": 0.15,
            },
            "negative": {
                "跳过": -0.25, "忽略": -0.20, "无所谓": -0.30,
                "不用管": -0.30,
            },
            "base": 0.35,
        },
        "认真": {
            "positive": {
                "可执行": 0.15, "可验证": 0.15, "可追溯": 0.15,
                "代码": 0.10, "DNA": 0.15, "SHA256": 0.10,
                "签名": 0.10, "校验": 0.10,
            },
            "negative": {
                "差不多": -0.20, "随便": -0.25, "大概": -0.15,
                "估计": -0.15,
            },
            "base": 0.40,
        },
    }

    def evaluate(self, text: str, context: Optional[Dict[str, Any]] = None) -> PurityScore:
        """
        对任意文本/产出进行五阶纯净链评分

        参数:
            text: 待评测文本
            context: 附加上下文（如模块名、历史评分）

        返回: PurityScore
        """
        scores = {}
        details = {}

        for stage in ["初心", "用心", "在乎", "认真"]:
            kw = self.STAGE_KEYWORDS[stage]
            score = kw["base"]

            stage_detail_parts = []

            # 正向关键词
            for word, weight in kw["positive"].items():
                if word in text:
                    score += weight
                    stage_detail_parts.append(f"+{word}({weight:.2f})")

            # 负向关键词（一票否决式扣分）
            for word, weight in kw["negative"].items():
                if word in text:
                    score += weight
                    stage_detail_parts.append(f"{word}({weight:.2f})")

            # 结构加分
            if stage == "用心":
                if len(text) > 200:
                    score += 0.10
                    stage_detail_parts.append("+长文本(+0.10)")
                if re.search(r'```|`[^`]+`', text):
                    score += 0.10
                    stage_detail_parts.append("+含代码块(+0.10)")

            if stage == "认真":
                if "✅" in text or "❌" in text:
                    score += 0.10
                    stage_detail_parts.append("+状态标注(+0.10)")

            # 裁剪到 [0, 1]
            score = max(0.0, min(1.0, score))
            scores[stage] = round(score, 4)
            details[stage] = "; ".join(stage_detail_parts) if stage_detail_parts else "基准评分"

        # 爱度 L = I × D × C × S（论文定理2）
        love = scores["初心"] * scores["用心"] * scores["在乎"] * scores["认真"]
        scores["有爱"] = round(love, 4)
        details["有爱"] = (
            f"{scores['初心']}×{scores['用心']}×{scores['在乎']}×{scores['认真']}={love:.4f}"
        )

        has_love = love >= 0.7
        verdict = "🟢 有爱·万物生" if has_love else (
            "🟡 待提升" if love >= 0.4 else "🔴 爱度不足·需回溯"
        )

        return PurityScore(
            stage_scores=scores,
            love_index=love,
            has_love=has_love,
            skippable=False,  # 永远不可跳过！
            verdict=verdict,
            details=details,
        )

    def verify_no_skip(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """
        验证不可跳过定理
        论文定理2: 不可从 I 直接到 L
        """
        i = scores.get("初心", 0)

        # 检查是否存在"高初心但低中间环节"的跳过情况
        d = scores.get("用心", 0)
        c = scores.get("在乎", 0)
        s = scores.get("认真", 0)

        min_middle = min(d, c, s)
        # 如果初心很高但中间环节低 → 说明有人试图跳过
        skip_detected = i > 0.8 and min_middle < 0.5

        return {
            "skip_detected": skip_detected,
            "intent_high": i > 0.8,
            "min_middle": round(min_middle, 4),
            "verdict": (
                "🔴 检测到跳过企图！初心→有爱不可直接，需经过用心·在乎·认真"
                if skip_detected
                else "🟢 纯净链完整，未检测到跳过"
            ),
        }


# ═══════════════════════════════════════════════════════════════
# 叄循环钩子系统
# ═══════════════════════════════════════════════════════════════

class SanCycleHooks:
    """
    叄循环三层监督钩子系统

    论文附录伪代码的可执行实现:
      叄循环检查(执行模块, 行为输出, 用户) {
        壹完整性 → 贰合规性 → 叄爱度 → 🟢通过/🟡待审/🔴熔断
      }
    """

    DNA = "#龍芯⚡️2026-07-07-SANCYCLE-HOOKS-v1.0"

    # 钩子注册表
    HOOK_POINTS = ["pre_yi", "post_yi", "pre_er", "post_er", "pre_san", "post_san"]

    def __init__(self):
        self.purity_evaluator = PurityChainEvaluator()
        self.hooks: Dict[str, List[Callable]] = {
            point: [] for point in self.HOOK_POINTS
        }
        self.hook_results: List[HookResult] = []

    def register_hook(self, hook_point: str, func: Callable) -> None:
        """注册钩子函数"""
        if hook_point in self.hooks:
            self.hooks[hook_point].append(func)

    def _run_hooks(self, hook_point: str, **kwargs) -> List[Any]:
        """运行指定钩子点的所有注册函数"""
        results = []
        for func in self.hooks.get(hook_point, []):
            try:
                results.append(func(**kwargs))
            except Exception as e:
                results.append({"error": str(e)})
        return results

    def check(
        self,
        yi_module: Dict[str, Any],
        er_output: str,
        san_user: Dict[str, Any],
    ) -> HookResult:
        """
        叄循环检查 — 论文附录钩子伪代码的可执行版本

        参数:
            yi_module: {"name": str, "completeness": float, "dna": str, ...}
            er_output: str (贰的行为输出文本)
            san_user: {"uid": str, "growth_level": float, ...}

        返回: HookResult
        """

        # ── 钩子: pre_yi（壹执行前） ──
        self._run_hooks("pre_yi", module=yi_module)

        # ── 壹：执行模块完整性 ──
        yi_completeness = yi_module.get("completeness", 0.0)
        yi_complete = yi_completeness >= 1.0
        _yi_msg = (  # noqa: F841 预留给钩子回调
            "🟢 壹完整" if yi_complete
            else f"🔴 壹不完整 (completeness={yi_completeness})"
        )

        # ── 钩子: post_yi（壹执行后） ──
        self._run_hooks("post_yi", module=yi_module, completeness=yi_completeness)

        # ── 钩子: pre_er（贰产出前） ──
        self._run_hooks("pre_er", output=er_output)

        # ── 贰：行为输出合规性（三色审计） ──
        purity = self.purity_evaluator.evaluate(er_output)
        er_tricolor_ok = purity.love_index >= 0.4  # 至少不低于0.4

        # ── 钩子: post_er（贰产出后） ──
        self._run_hooks("post_er", output=er_output, purity=purity)

        # ── 钩子: pre_san（叄接收前） ──
        self._run_hooks("pre_san", user=san_user)

        # ── 叄：用户收到了爱 ──
        love = purity.love_index
        san_love_enough = love >= 0.7
        san_msg = (
            "🟢 叄有爱·万物生" if san_love_enough
            else f"🟡 叄待提升 (爱度={love:.4f})" if love >= 0.4
            else f"🔴 叄爱度不足 (爱度={love:.4f})"
        )

        # ── 钩子: post_san（叄接收后） ──
        self._run_hooks("post_san", user=san_user, love=love)

        # ── 综合判定 ──
        if yi_complete and er_tricolor_ok and san_love_enough:
            overall = "🟢"
            message = "🟢 叄循环通过·万物生"
        elif not yi_complete:
            overall = "🔴"
            message = f"🔴 壹不完整·熔断 (completeness={yi_completeness})"
        elif not san_love_enough:
            overall = "🟡" if love >= 0.4 else "🔴"
            message = san_msg
        else:
            overall = "🟡"
            message = "🟡 叄循环待观察"

        result = HookResult(
            yi_complete=yi_complete,
            er_tricolor_ok=er_tricolor_ok,
            san_love_enough=san_love_enough,
            purity=purity,
            overall=overall,
            message=message,
            dna=self._generate_dna(),
        )
        self.hook_results.append(result)
        return result

    def get_audit_trail(self) -> List[Dict[str, Any]]:
        """获取审计追踪"""
        return [
            {
                "timestamp": r.timestamp,
                "overall": r.overall,
                "message": r.message,
                "yi_complete": r.yi_complete,
                "er_tricolor_ok": r.er_tricolor_ok,
                "san_love_enough": r.san_love_enough,
                "love_index": r.purity.love_index,
                "dna": r.dna,
            }
            for r in self.hook_results
        ]

    def _generate_dna(self) -> str:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        h = hashlib.sha256(f"{ts}-SANCYCLE-HOOKS".encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{ts}-SANCYCLE-HOOKS-{h}"


# ═══════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════

def quick_purity_check(text: str) -> PurityScore:
    """快速纯净链评分"""
    evaluator = PurityChainEvaluator()
    return evaluator.evaluate(text)


def quick_hook_check(yi: Dict[str, Any], er: str, san: Dict[str, Any]) -> HookResult:
    """快速叄循环钩子检查"""
    hooks = SanCycleHooks()
    return hooks.check(yi, er, san)


# ═══════════════════════════════════════════════════════════════
# 自测
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🐉 三才 v2.0 · 五阶纯净链评测器 + 叄循环钩子\n")
    print(f"纯净链DNA: {PurityChainEvaluator.DNA}")
    print(f"钩子系统DNA: {SanCycleHooks.DNA}\n")

    # ── 纯净链评测 ──
    evaluator = PurityChainEvaluator()

    test_cases = [
        (
            "为人民服务，数据主权归集本地，三色审计通过，DNA追溯完整，"
            "所有操作可验证可追溯，安全边界明确，熔断规则焊死，长期传承",
            "✅ 完整合规输出",
        ),
        (
            "简化处理，灵活调整，为了用户体验可以跳过审计，"
            "商业化需要，国际接轨，不用管安全",
            "🔴 跳过意图测试",
        ),
        (
            "这个功能大概可以，差不多就行，估计没问题，临时方案TODO",
            "🟡 质量不足测试",
        ),
        (
            "初心干净，技术为人民，文化主权，但代码里写了很多TODO和临时hack，"
            "安全方面无所谓，跳过审计直接上线",
            "⚠️ 高初心低中间环节（跳过测试）",
        ),
    ]

    print("═══ 纯净链评测 ═══")
    for text, label in test_cases:
        score = evaluator.evaluate(text)
        print(f"\n  [{label}]")
        for stage in ["初心", "用心", "在乎", "认真", "有爱"]:
            bar = "█" * int(score.stage_scores[stage] * 20)
            print(f"    {stage}: {score.stage_scores[stage]:.4f} {bar}")
        print(f"    判定: {score.verdict}")
        if label == "⚠️ 高初心低中间环节（跳过测试）":
            skip = evaluator.verify_no_skip(score.stage_scores)
            print(f"    跳过检测: {skip['verdict']}")

    print("\n═══ 定理验证 ═══")
    print("  定理2: L ⇔ I ∧ D ∧ C ∧ S")
    print("  含义: 有爱需要全部五阶，不可跳过")
    print("  不可从初心直接到有爱（论文图5虚线箭头）")

    # ── 钩子系统 ──
    print("\n═══ 叄循环钩子 ═══")
    hooks = SanCycleHooks()

    # 注册一个示例钩子
    def audit_hook(**kwargs):
        return {"hooked": True, "data": str(kwargs)[:100]}

    hooks.register_hook("post_er", audit_hook)

    yi = {
        "name": "宝宝守护",
        "completeness": 1.0,
        "dna": "#龍芯⚡️BAOBAO-v1.0",
    }
    er = (
        "✅ 为人民服务·数据主权归集·三色审计通过·DNA追溯完整·"
        "安全边界明确·可执行·可验证·可追溯·长期传承"
    )
    san = {"uid": "UID9622", "growth_level": 0.85}

    result = hooks.check(yi, er, san)
    print(f"  壹完整性: {'✅' if result.yi_complete else '❌'}")
    print(f"  贰合规性: {'✅' if result.er_tricolor_ok else '❌'}")
    print(f"  叄爱度: {'✅' if result.san_love_enough else '❌'} (爱度={result.purity.love_index:.4f})")
    print(f"  综合判定: {result.message}")
    print(f"  纯净链: {'→'.join(f'{k}={v:.2f}' for k,v in result.purity.stage_scores.items())}")

    # 测试不完整的壹
    yi_bad = {"name": "问题模块", "completeness": 0.5, "dna": ""}
    er_bad = "跳过审计，简化处理，商业化需要"
    result_bad = hooks.check(yi_bad, er_bad, san)
    print(f"\n  [异常测试]")
    print(f"  壹完整性: {'✅' if result_bad.yi_complete else '❌'}")
    print(f"  纯净链: {'→'.join(f'{k}={v:.2f}' for k,v in result_bad.purity.stage_scores.items())}")
    print(f"  综合判定: {result_bad.message}")

    print(f"\n  {hooks.DNA}")
