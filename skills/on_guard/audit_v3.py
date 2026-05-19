#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
longhun-wucai-coloring · v3.0 升级版
龍魂 v3.0 · UID9622 主控
DNA: #龍芯⚡2026-05-19-WUCAI-V3-ENGINE-FUSION-v1.0

═══════════════════════════════════════════════════════════════
v3.0 = v2.0 Router (五色) + v1.5 Engine (F18 + α + 最小链)
═══════════════════════════════════════════════════════════════

v2.0 → v3.0 焊入三件 (来自 v1.5 公式对准表):

  ① F18 三才主权指数 SI · 顶层熔断
     SI = 0.34*Heaven + 0.33*Earth + 0.33*Human
     SI < 0.34 → 主权失锚 → 一票熔断 (比 R 系数更高级)

  ② α 三义锁死 · 裸 α 一票否决
     α_τ = 时间衰减
     α_a = 人格振幅
     α_w = 权重
     裸 α (未标注归属) = 协议违例·拒

  ③ 最小执行链 · 每次审计必走六步
     dr (数字根) → W(x) 权重 → Risk → S 主权 → D 决策 → Action

═══════════════════════════════════════════════════════════════
向后兼容: v2.0 调用方式不变 · audit() 函数签名兼容
═══════════════════════════════════════════════════════════════
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Literal
import datetime
import math


# ============ 五色常量 (v2.0 沿用) ============
COLOR_GREEN  = "🟢"
COLOR_YELLOW = "🟡"
COLOR_RED    = "🔴"
COLOR_BLACK  = "⚫"
COLOR_GOLD   = "🟡金"
COLOR_VOID   = "🔵"   # ★ v3.0 新增 · F18 主权失锚专用 (比红更高级)

# ============ R 公式 v2.0 权重 (沿用) ============
R_WEIGHTS_POS = {"sharpness": 0.4, "long_term": 0.4, "density": 0.2}
R_WEIGHTS_NEG = {"absence": 0.5, "pleasing": 0.3}

# ============ 三色五色阈值 (沿用) ============
THRESH_GREEN_TOP  = 0.30
THRESH_YELLOW_TOP = 0.67
THRESH_RED_TOP    = 0.85

# ============ ★ v3.0 新焊 · F18 主权指数 SI ============
SI_WEIGHTS = {
    "heaven": 0.34,   # 天 · 道义/法理/公共秩序
    "earth":  0.33,   # 地 · 资源/环境/生产
    "human":  0.33,   # 人 · 人格/信任/关系
}
SI_VOID_THRESHOLD = 0.34   # SI 低于此值 = 主权失锚 = 顶层熔断

# ============ ★ v3.0 新焊 · α 三义合法标注 ============
ALPHA_TAGS = {"α_τ", "α_a", "α_w"}   # 必须用其一标注·不可裸 α


@dataclass
class AuditResult:
    """五色审计结果 v3.0"""
    color: str
    R_value: Optional[float]
    SI_value: Optional[float] = None   # ★ v3.0 新字段
    reasoning: str = ""
    action: str = ""
    next_step: str = ""
    dna_trace: str = ""
    override_required: bool = False
    raw_factors: Dict[str, float] = field(default_factory=dict)
    shadow_reason: Optional[str] = None
    gold_reason: Optional[str] = None
    void_reason: Optional[str] = None  # ★ v3.0 主权失锚原因
    execution_chain: Dict[str, Any] = field(default_factory=dict)  # ★ 最小链留痕

    def to_yaml(self) -> str:
        lines = [
            "audit_result:",
            f"  version: v3.0",
            f"  color: {self.color}",
            f"  R_value: {self.R_value if self.R_value is not None else 'N/A'}",
            f"  SI_value: {self.SI_value if self.SI_value is not None else 'N/A'}",
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
        if self.void_reason:
            lines.append(f"  void_reason: {self.void_reason}")
        if self.execution_chain:
            lines.append(f"  execution_chain:")
            for k, v in self.execution_chain.items():
                lines.append(f"    {k}: {v}")
        return "\n".join(lines)


# ============ R 计算 (v2.0 沿用) ============
def compute_R(factors: Dict[str, float]) -> Optional[float]:
    keys_needed = set(R_WEIGHTS_POS) | set(R_WEIGHTS_NEG)
    if not keys_needed.issubset(factors.keys()):
        return None
    R = sum(factors[k] * w for k, w in R_WEIGHTS_POS.items())
    R -= sum(factors[k] * w for k, w in R_WEIGHTS_NEG.items())
    return max(0.0, min(1.0, R))


# ============ ★ v3.0 新焊 · F18 主权指数 SI ============
def compute_SI(triadic: Dict[str, float]) -> Optional[float]:
    """
    F18 三才主权指数 SI
    SI = 0.34*天 + 0.33*地 + 0.33*人 · 范围 [0, 1]
    SI < 0.34 = 主权失锚 = 比 R 更高级的一票熔断

    输入:
      triadic = {"heaven": float, "earth": float, "human": float}
    输出:
      SI 值 ∈ [0,1] · 或 None (输入不全)
    """
    if not set(SI_WEIGHTS.keys()).issubset(triadic.keys()):
        return None
    SI = sum(triadic[k] * w for k, w in SI_WEIGHTS.items())
    return max(0.0, min(1.0, SI))


# ============ ★ v3.0 新焊 · α 三义合法性检查 ============
def check_alpha_violation(context: Dict[str, Any]) -> Optional[str]:
    """
    裸 α 一票否决 (v1.5 §S 锁死铁律)
    使用 α 必须标注归属: α_τ (时间) / α_a (振幅) / α_w (权重)
    裸 α (未标注) = 协议违例·拒
    """
    alphas_used = context.get("alphas_used", [])
    for a in alphas_used:
        if a == "α" or a == "alpha":
            return f"裸 α 检出·必须标注 α_τ/α_a/α_w · 协议违例"
        if a not in ALPHA_TAGS:
            return f"非法 α 标注: {a} · 仅允许 {ALPHA_TAGS}"
    return None


# ============ 数字根 (最小执行链第一步) ============
def digital_root(n) -> int:
    """计算数字根 dr · 用于五行 369 闸门"""
    if isinstance(n, float):
        n = int(round(n * 1000))
    n = abs(n)
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


# ============ 五色 (v2.0 沿用) ============
def check_shadow(context: Dict[str, Any], R: Optional[float]) -> Optional[str]:
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
    if not context.get("master_confirm_token"):
        return None
    if context.get("master_confirm_token") != "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z":
        return None
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
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    return f"#龍芯⚡{now.strftime('%Y-%m-%d-%H%M%S')}-AUDIT-V3"


# ============ ★ v3.0 主入口 · 最小执行链六步 ============
def audit(task: str,
          factors: Dict[str, float],
          context: Optional[Dict[str, Any]] = None,
          triadic: Optional[Dict[str, float]] = None) -> AuditResult:
    """
    五色审计 v3.0 主入口

    最小执行链: dr → W(x) → Risk → S → D → Action

    新增参数:
      triadic: {"heaven": float, "earth": float, "human": float}
               用于 F18 SI 主权指数计算
               若为 None · SI 不参与判定 (向后兼容 v2.0)
    """
    context = context or {}
    dna = _dna_now()
    chain = {}  # 最小执行链留痕

    # ━━━ 步 0 · α 合法性 (前置·裸 α 一票否决) ━━━
    alpha_violation = check_alpha_violation(context)
    if alpha_violation:
        return AuditResult(
            color=COLOR_RED,
            R_value=None,
            reasoning=f"α 三义违例·{alpha_violation}",
            action="拒绝执行·校准 α 标注后重审",
            next_step="使用 α_τ / α_a / α_w 之一明确标注",
            dna_trace=dna,
            override_required=True,
            execution_chain={"step": "0_alpha_check", "violation": alpha_violation},
        )

    # ━━━ 步 1 · dr 数字根 ━━━
    task_hash = sum(ord(c) for c in task)
    dr = digital_root(task_hash)
    chain["1_dr"] = dr

    # ━━━ 步 2 · W(x) 权重计算 ━━━
    R = compute_R(factors)
    chain["2_W"] = {k: f"{factors.get(k, 'N/A')}" for k in (set(R_WEIGHTS_POS) | set(R_WEIGHTS_NEG))}

    # ━━━ 步 3 · Risk 风险评估 (= R 值) ━━━
    chain["3_Risk"] = R if R is not None else "uncomputable"

    # ━━━ 步 4 · S 主权检查 (★ v3.0 新焊·F18 SI) ━━━
    SI = compute_SI(triadic) if triadic else None
    chain["4_S"] = SI if SI is not None else "skipped"

    # 主权熔断: SI < 0.34 = 主权失锚 = 比 R 更高级
    if SI is not None and SI < SI_VOID_THRESHOLD:
        return AuditResult(
            color=COLOR_VOID,
            R_value=R,
            SI_value=SI,
            reasoning=f"F18 主权失锚·SI={SI:.3f} < {SI_VOID_THRESHOLD}·顶层熔断",
            action="立即冻结·上报 L11 主权层",
            next_step="检查天/地/人三才是否被外部胁迫·非 R 可救",
            dna_trace=dna,
            override_required=True,  # 只有金色可救
            raw_factors=factors,
            void_reason=f"sovereignty_unanchored_SI_{SI:.3f}",
            execution_chain=chain,
        )

    # ━━━ 步 5 · D 决策 (五色判定·v2.0 逻辑) ━━━

    # 金色优先 (主控独占)
    gold_reason = check_gold(context)
    if gold_reason:
        decision = context.get("master_decision", "暂缓")
        chain["5_D"] = f"GOLD:{decision}"
        return AuditResult(
            color=COLOR_GOLD,
            R_value=R,
            SI_value=SI,
            reasoning=f"主控金色判决·{gold_reason}",
            action=f"主控签字: {decision}",
            next_step="落入金色判决书·留 DNA 永存档",
            dna_trace=dna,
            override_required=False,
            raw_factors=factors,
            gold_reason=gold_reason,
            execution_chain=chain,
        )

    # 影子色 (黑)
    shadow_reason = check_shadow(context, R)
    if shadow_reason:
        chain["5_D"] = "SHADOW"
        return AuditResult(
            color=COLOR_BLACK,
            R_value=R,
            SI_value=SI,
            reasoning=f"影子态·{shadow_reason}·不可决",
            action="进观察池",
            next_step="冻结 24h·收集新证据·禁止静默转绿",
            dna_trace=dna,
            override_required=True,
            raw_factors=factors,
            shadow_reason=shadow_reason,
            execution_chain=chain,
        )

    # ━━━ 步 6 · Action 三色落档 ━━━
    if R < THRESH_GREEN_TOP:
        chain["5_D"] = "GREEN"
        chain["6_Action"] = "pass"
        return AuditResult(
            color=COLOR_GREEN, R_value=R, SI_value=SI,
            reasoning=f"自由意志态·R={R:.3f}",
            action="自动放行", next_step="留痕·不打扰",
            dna_trace=dna, raw_factors=factors,
            execution_chain=chain,
        )
    elif R < THRESH_YELLOW_TOP:
        chain["5_D"] = "YELLOW"
        chain["6_Action"] = "review"
        return AuditResult(
            color=COLOR_YELLOW, R_value=R, SI_value=SI,
            reasoning=f"老好人态·R={R:.3f}",
            action="二次确认", next_step="要求 caller 加证据·记审计日志",
            dna_trace=dna, raw_factors=factors,
            execution_chain=chain,
        )
    elif R < THRESH_RED_TOP:
        chain["5_D"] = "RED"
        chain["6_Action"] = "block"
        return AuditResult(
            color=COLOR_RED, R_value=R, SI_value=SI,
            reasoning=f"真负责越界态·R={R:.3f}",
            action="立即停止", next_step="上报主控·触发 §8.5 极端态协议",
            dna_trace=dna, override_required=True,
            raw_factors=factors, execution_chain=chain,
        )
    else:
        chain["5_D"] = "RED+"
        chain["6_Action"] = "escalate"
        return AuditResult(
            color=COLOR_RED, R_value=R, SI_value=SI,
            reasoning=f"龍魂型超阈值·R={R:.3f}",
            action="进金色队列·等老大裁决",
            next_step="发送金色判决申请·DNA 已锁",
            dna_trace=dna, override_required=True,
            raw_factors=factors, execution_chain=chain,
        )


# ============ 自测 12 项 (8 v2.0 + 4 v3.0 新焊) ============
def _selftest():
    print("=" * 64)
    print("龍魂五色审计 v3.0 · 自测 12 项")
    print("(8 项 v2.0 沿用 + 4 项 v3.0 新焊)")
    print("=" * 64)

    # === v2.0 沿用 8 项 ===
    print("\n── v2.0 沿用 ──")

    # 1. 绿色
    r = audit("日常", {"sharpness": 0.3, "long_term": 0.3, "density": 0.2, "absence": 0.7, "pleasing": 0.6})
    assert r.color == COLOR_GREEN
    print(f"  [1/12 ✓] 绿色 · R={r.R_value:.3f}")

    # 2. 黄色
    r = audit("边界", {"sharpness": 0.6, "long_term": 0.6, "density": 0.5, "absence": 0.3, "pleasing": 0.3})
    assert r.color == COLOR_YELLOW
    print(f"  [2/12 ✓] 黄色 · R={r.R_value:.3f}")

    # 3. 红色
    r = audit("极端", {"sharpness": 0.9, "long_term": 0.9, "density": 0.8, "absence": 0.1, "pleasing": 0.1})
    assert r.color == COLOR_RED
    print(f"  [3/12 ✓] 红色 · R={r.R_value:.3f}")

    # 4. 黑色·数据不全
    r = audit("数据缺", {"sharpness": 0.5}, context={"data_incomplete": True})
    assert r.color == COLOR_BLACK
    print(f"  [4/12 ✓] 黑色 · 数据不全")

    # 5. 黑色·灰色相遇
    r = audit("五行冲突",
              {"sharpness": 0.5, "long_term": 0.5, "density": 0.5, "absence": 0.5, "pleasing": 0.5},
              context={"grey_collision": True})
    assert r.color == COLOR_BLACK
    print(f"  [5/12 ✓] 黑色 · 灰色相遇")

    # 6. 金色·子女维度
    r = audit("子女",
              {"sharpness": 0.9, "long_term": 0.9, "density": 0.9, "absence": 0.0, "pleasing": 0.0},
              context={
                  "master_confirm_token": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
                  "involves_minor": True,
                  "master_decision": "保护",
              })
    assert r.color == COLOR_GOLD
    print(f"  [6/12 ✓] 金色 · 子女维度")

    # 7. AI 伪造金色·应失败
    r = audit("伪金",
              {"sharpness": 0.9, "long_term": 0.9, "density": 0.9, "absence": 0.0, "pleasing": 0.0},
              context={"involves_minor": True})
    assert r.color != COLOR_GOLD
    print(f"  [7/12 ✓] AI 伪造金色 → 拒")

    # 8. 金色·主权红线
    r = audit("主权",
              {"sharpness": 0.9, "long_term": 0.9, "density": 0.9, "absence": 0.0, "pleasing": 0.0},
              context={
                  "master_confirm_token": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
                  "sovereignty_redline": True,
                  "master_decision": "否决",
              })
    assert r.color == COLOR_GOLD
    print(f"  [8/12 ✓] 金色 · 主权红线")

    # === v3.0 新焊 4 项 ===
    print("\n── v3.0 新焊 ──")

    # 9. ★ F18 SI 高 · 主权稳·走 v2.0 流程
    r = audit("正常",
              {"sharpness": 0.3, "long_term": 0.3, "density": 0.2, "absence": 0.7, "pleasing": 0.6},
              triadic={"heaven": 0.8, "earth": 0.8, "human": 0.8})
    assert r.color == COLOR_GREEN
    assert r.SI_value is not None and r.SI_value > 0.34
    print(f"  [9/12 ✓] F18 SI 高 · SI={r.SI_value:.3f} · 走绿色")

    # 10. ★ F18 SI 低 · 主权失锚·熔断 (即便 R 是绿)
    r = audit("主权失锚",
              {"sharpness": 0.3, "long_term": 0.3, "density": 0.2, "absence": 0.7, "pleasing": 0.6},
              triadic={"heaven": 0.1, "earth": 0.2, "human": 0.2})
    assert r.color == COLOR_VOID
    assert r.SI_value is not None and r.SI_value < 0.34
    print(f"  [10/12 ✓] F18 SI 低·VOID 熔断·SI={r.SI_value:.3f} (即便 R 应绿)")

    # 11. ★ 裸 α 一票否决
    r = audit("裸 alpha",
              {"sharpness": 0.5, "long_term": 0.5, "density": 0.5, "absence": 0.3, "pleasing": 0.3},
              context={"alphas_used": ["α"]})
    assert r.color == COLOR_RED
    assert "α" in r.reasoning
    print(f"  [11/12 ✓] 裸 α 检出·拒绝执行")

    # 12. ★ 最小执行链 6 步留痕完整
    r = audit("链测",
              {"sharpness": 0.5, "long_term": 0.5, "density": 0.4, "absence": 0.4, "pleasing": 0.3},
              triadic={"heaven": 0.7, "earth": 0.7, "human": 0.7},
              context={"alphas_used": ["α_τ", "α_w"]})
    chain_keys = set(r.execution_chain.keys())
    expected_keys = {"1_dr", "2_W", "3_Risk", "4_S", "5_D", "6_Action"}
    assert expected_keys.issubset(chain_keys), f"链不完整: {chain_keys}"
    print(f"  [12/12 ✓] 最小执行链 6 步完整 · {sorted(chain_keys)}")

    print("\n" + "=" * 64)
    print("12/12 全过 · v3.0 Engine 焊入完成")
    print("Router (v2.0 五色) + Engine (v1.5 F18/α/链) = v3.0")
    print("=" * 64)


if __name__ == "__main__":
    _selftest()
