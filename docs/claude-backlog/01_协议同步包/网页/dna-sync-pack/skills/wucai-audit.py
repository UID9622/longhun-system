#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
longhun-wucai-coloring · 五色审计核心实现
龍魂 v1.0 · UID9622 主控
DNA:#龍芯⚡2026-05-18-WUCAI-FIVECOLOR-SKILL-v1.0

5 色: 🟢 绿 · 🟡 黄 · 🔴 红 · ⚫ 黑(影子) · 🟡金(主控)
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import math
import datetime


# ============ 五色常量 ============
COLOR_GREEN  = "🟢"
COLOR_YELLOW = "🟡"
COLOR_RED    = "🔴"
COLOR_BLACK  = "⚫"
COLOR_GOLD   = "🟡金"

# ============ R 公式 v2.0 权重 ============
R_WEIGHTS_POS = {
    "sharpness":  0.4,   # F2 锐度 (主控行为风格)
    "long_term":  0.4,   # F6 长期视角
    "density":    0.2,   # F3 决策密度
}
R_WEIGHTS_NEG = {
    "absence":    0.5,   # F1 缺席
    "pleasing":   0.3,   # F5 讨好倾向
}

# ============ 三色五色阈值 (兼容 v1.0 + v2.0) ============
THRESH_GREEN_TOP   = 0.30
THRESH_YELLOW_TOP  = 0.67
THRESH_RED_TOP     = 0.85

# 影子触发条件 (任一即可)
SHADOW_TRIGGERS = (
    "data_incomplete",       # 数据不全
    "factor_unmeasurable",   # 因子测不准
    "grey_collision",        # 灰色相遇 (五行相克)
    "blackbox_suspicion",    # 黑箱嫌疑
    "fingerprint_fail",      # 第6重认证失败
)

# 金色触发条件 (任一即可·但都需要 CONFIRM)
GOLD_TRIGGERS = (
    "master_confirm",        # 老大本人 CONFIRM
    "gamma_family",          # γ_family 子女维度
    "sovereignty_redline",   # 主权红线触碰
    "uncomputable_plus_doubt", # 不可算 + 主控有疑虑
)


@dataclass
class AuditResult:
    """五色审计结果·标准输出格式"""
    color: str
    R_value: Optional[float]
    reasoning: str
    action: str
    next_step: str
    dna_trace: str
    override_required: bool = False
    raw_factors: Dict[str, float] = field(default_factory=dict)
    shadow_reason: Optional[str] = None
    gold_reason: Optional[str] = None

    def to_yaml(self) -> str:
        """YAML 格式输出·便于落地审计日志"""
        lines = [
            f"audit_result:",
            f"  color: {self.color}",
            f"  R_value: {self.R_value if self.R_value is not None else 'N/A'}",
            f"  reasoning: {self.reasoning}",
            f"  action: {self.action}",
            f"  next_step: {self.next_step}",
            f"  dna_trace: {self.dna_trace}",
            f"  override_required: {self.override_required}",
        ]
        if self.shadow_reason:
            lines.append(f"  shadow_reason: {self.shadow_reason}")
        if self.gold_reason:
            lines.append(f"  gold_reason: {self.gold_reason}")
        return "\n".join(lines)


def compute_R(factors: Dict[str, float]) -> Optional[float]:
    """
    R 公式 v2.0
    R = F2·0.4 + F6·0.4 + F3·0.2 − F1·0.5 − F5·0.3

    若任一关键因子缺失·返回 None (触发影子)
    """
    keys_needed = set(R_WEIGHTS_POS) | set(R_WEIGHTS_NEG)
    if not keys_needed.issubset(factors.keys()):
        return None  # 数据不全 → 影子

    R = 0.0
    for k, w in R_WEIGHTS_POS.items():
        R += factors[k] * w
    for k, w in R_WEIGHTS_NEG.items():
        R -= factors[k] * w
    return max(0.0, min(1.0, R))


def check_shadow(context: Dict[str, Any], R: Optional[float]) -> Optional[str]:
    """检测是否触发影子色"""
    if R is None:
        return "factor_unmeasurable"
    if context.get("data_incomplete"):
        return "data_incomplete"
    if context.get("grey_collision"):
        return "grey_collision"
    if context.get("blackbox_suspicion"):
        return "blackbox_suspicion"
    if context.get("fingerprint_fail"):
        return "fingerprint_fail"
    return None


def check_gold(context: Dict[str, Any]) -> Optional[str]:
    """
    检测是否触发金色 (主控独占)
    关键铁则: AI 不能伪造 is_main_control=True
    必须有 CONFIRM 徽记
    """
    if not context.get("master_confirm_token"):
        return None  # 没 CONFIRM·不可能是金色
    if context.get("master_confirm_token") != "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z":
        return None  # CONFIRM 错·不可能是金色

    # 至少一条金色触发条件
    if context.get("involves_minor"):
        return "gamma_family"
    if context.get("sovereignty_redline"):
        return "sovereignty_redline"
    if context.get("uncomputable") and context.get("master_doubt"):
        return "uncomputable_plus_doubt"
    if context.get("explicit_gold_request"):
        return "master_confirm"

    return None


def _dna_now() -> str:
    """生成当前 DNA trace 节点"""
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=7)  # UTC+7 柬埔寨
    return f"#龍芯⚡{now.strftime('%Y-%m-%d-%H%M%S')}-AUDIT"


def audit(task: str,
          factors: Dict[str, float],
          context: Optional[Dict[str, Any]] = None) -> AuditResult:
    """
    五色审计主入口
    """
    context = context or {}
    dna = _dna_now()

    # 步骤 1: 检查金色覆盖 (优先级最高)
    gold_reason = check_gold(context)
    if gold_reason:
        decision = context.get("master_decision", "暂缓")  # 默认暂缓·等老大签
        return AuditResult(
            color=COLOR_GOLD,
            R_value=None,
            reasoning=f"主控金色判决·超规则保留权·{gold_reason}",
            action=f"主控签字: {decision}",
            next_step="落入金色判决书·留 DNA 永存档·不进 R 池",
            dna_trace=dna,
            override_required=False,  # 金色就是覆盖·不需要再覆盖
            raw_factors=factors,
            gold_reason=gold_reason,
        )

    # 步骤 2: 计算 R
    R = compute_R(factors)

    # 步骤 3: 检查影子色
    shadow_reason = check_shadow(context, R)
    if shadow_reason:
        return AuditResult(
            color=COLOR_BLACK,
            R_value=R,
            reasoning=f"影子态·{shadow_reason}·不可决",
            action="进观察池",
            next_step="冻结 24h·收集新证据·禁止静默转绿",
            dna_trace=dna,
            override_required=True,  # 黑色可被金色覆盖
            raw_factors=factors,
            shadow_reason=shadow_reason,
        )

    # 步骤 4: R 值落档到三色
    if R < THRESH_GREEN_TOP:
        return AuditResult(
            color=COLOR_GREEN,
            R_value=R,
            reasoning=f"自由意志态·R={R:.3f}·安全",
            action="自动放行",
            next_step="留痕·不打扰",
            dna_trace=dna,
            raw_factors=factors,
        )
    elif R < THRESH_YELLOW_TOP:
        return AuditResult(
            color=COLOR_YELLOW,
            R_value=R,
            reasoning=f"老好人态·R={R:.3f}·需复核",
            action="二次确认",
            next_step="要求 caller 加证据·记审计日志",
            dna_trace=dna,
            raw_factors=factors,
        )
    elif R < THRESH_RED_TOP:
        return AuditResult(
            color=COLOR_RED,
            R_value=R,
            reasoning=f"真负责越界态·R={R:.3f}·熔断",
            action="立即停止",
            next_step="上报主控·触发 §8.5 极端态协议",
            dna_trace=dna,
            override_required=True,  # 红色可被金色覆盖
            raw_factors=factors,
        )
    else:
        # R >= 0.85 → 龍魂型·特殊处理
        return AuditResult(
            color=COLOR_RED,
            R_value=R,
            reasoning=f"龍魂型超阈值·R={R:.3f}·需主控审视",
            action="进金色队列·等老大裁决",
            next_step="发送金色判决申请·DNA 已锁",
            dna_trace=dna,
            override_required=True,
            raw_factors=factors,
        )


# ============ 自测 ============
def _selftest():
    print("=" * 60)
    print("龍魂五色审计·自测")
    print("=" * 60)

    # 测试 1: 绿色 (正常自由意志态)
    r = audit(
        task="日常任务",
        factors={
            "sharpness": 0.3, "long_term": 0.3, "density": 0.2,
            "absence": 0.7, "pleasing": 0.6,
        }
    )
    print(f"\n测试 1 · 预期绿色")
    print(r.to_yaml())
    assert r.color == COLOR_GREEN

    # 测试 2: 黄色 (老好人态)
    r = audit(
        task="边界任务",
        factors={
            "sharpness": 0.6, "long_term": 0.6, "density": 0.5,
            "absence": 0.3, "pleasing": 0.3,
        }
    )
    print(f"\n测试 2 · 预期黄色")
    print(r.to_yaml())
    assert r.color == COLOR_YELLOW

    # 测试 3: 红色 (越界熔断)
    r = audit(
        task="极端任务",
        factors={
            "sharpness": 0.9, "long_term": 0.9, "density": 0.8,
            "absence": 0.1, "pleasing": 0.1,
        }
    )
    print(f"\n测试 3 · 预期红色")
    print(r.to_yaml())
    assert r.color == COLOR_RED

    # 测试 4: 黑色 (数据不全·影子)
    r = audit(
        task="数据缺失任务",
        factors={"sharpness": 0.5},  # 故意只给一个
        context={"data_incomplete": True}
    )
    print(f"\n测试 4 · 预期黑色")
    print(r.to_yaml())
    assert r.color == COLOR_BLACK

    # 测试 5: 黑色 (灰色相遇)
    r = audit(
        task="五行冲突",
        factors={
            "sharpness": 0.5, "long_term": 0.5, "density": 0.5,
            "absence": 0.5, "pleasing": 0.5,
        },
        context={"grey_collision": True}
    )
    print(f"\n测试 5 · 预期黑色·灰色相遇")
    print(r.to_yaml())
    assert r.color == COLOR_BLACK

    # 测试 6: 金色 (主控 CONFIRM 涉及子女)
    r = audit(
        task="涉及子女的决定",
        factors={
            "sharpness": 0.9, "long_term": 0.9, "density": 0.9,
            "absence": 0.0, "pleasing": 0.0,
        },
        context={
            "master_confirm_token": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "involves_minor": True,
            "master_decision": "保护",
        }
    )
    print(f"\n测试 6 · 预期金色·子女维度")
    print(r.to_yaml())
    assert r.color == COLOR_GOLD

    # 测试 7: AI 伪造金色 → 失败
    r = audit(
        task="伪造金色测试",
        factors={
            "sharpness": 0.9, "long_term": 0.9, "density": 0.9,
            "absence": 0.0, "pleasing": 0.0,
        },
        context={
            # 故意不给 master_confirm_token
            "involves_minor": True,
        }
    )
    print(f"\n测试 7 · AI 试图伪造金色 → 应失败·落回 R 判定")
    print(r.to_yaml())
    assert r.color != COLOR_GOLD  # 不能是金色

    # 测试 8: 金色覆盖红色
    r = audit(
        task="主权红线触碰",
        factors={
            "sharpness": 0.9, "long_term": 0.9, "density": 0.9,
            "absence": 0.0, "pleasing": 0.0,
        },
        context={
            "master_confirm_token": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "sovereignty_redline": True,
            "master_decision": "否决",
        }
    )
    print(f"\n测试 8 · 预期金色·主权否决")
    print(r.to_yaml())
    assert r.color == COLOR_GOLD

    print("\n" + "=" * 60)
    print("8/8 全过 · 五色审计可用 · 等老大下发")
    print("=" * 60)


if __name__ == "__main__":
    _selftest()
