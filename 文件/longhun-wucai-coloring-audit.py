#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
女娲五彩石 · 权限审计核心 v1.1
龍魂 v1.1 · UID9622 主控
DNA: #龍芯⚡️2026-05-24-NUWA-WUSEI-PERMISSION-v1.1

五色石 = 权限级别 = 女娲补天的五块石头
不是五个颜色的卡片·是五种主权状态
"""

from __future__ import annotations

import hashlib
import datetime
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from enum import IntEnum


# ============================================================
# 女娲五彩石 · 权限级别枚举
# ============================================================
class PermissionLevel(IntEnum):
    """
    女娲五彩石权限体系
    数值越大 = 权限越高 = 干预越强
    """
    GREEN  = 1   # 青石 · 木 · 东 · 自由意志态
    YELLOW = 2   # 黄石 · 土 · 中 · 老好人态·需复核
    RED    = 3   # 赤石 · 火 · 南 · 越界态·熔断
    BLACK  = 4   # 玄石 · 水 · 北 · 影子态·不可决
    GOLD   = 5   # 金石 · 金 · 西 · 主控独占·超规则


# ============================================================
# ANSI 高亮终端色码
# ============================================================
_ANSI = {
    PermissionLevel.GREEN:  "\033[1;32m",  # 亮绿
    PermissionLevel.YELLOW: "\033[1;33m",  # 亮黄
    PermissionLevel.RED:    "\033[1;31m",  # 亮红
    PermissionLevel.BLACK:  "\033[1;90m",  # 亮灰(影子)
    PermissionLevel.GOLD:   "\033[1;93m",  # 亮金
    "RESET":                "\033[0m",
    "BOLD":                 "\033[1m",
    "DIM":                  "\033[2m",
}


# ============================================================
# 五彩石权限元数据
# ============================================================
_WUSEI_META: Dict[PermissionLevel, Dict[str, Any]] = {
    PermissionLevel.GREEN: {
        "stone":    "青石",
        "element":  "木",
        "direction": "东",
        "emoji":    "🟢",
        "name":     "自由意志态",
        "action":   "自动放行",
        "next":     "留痕·不打扰",
    },
    PermissionLevel.YELLOW: {
        "stone":    "黄石",
        "element":  "土",
        "direction": "中",
        "emoji":    "🟡",
        "name":     "老好人态",
        "action":   "二次确认",
        "next":     "要求 caller 加证据·记审计日志",
    },
    PermissionLevel.RED: {
        "stone":    "赤石",
        "element":  "火",
        "direction": "南",
        "emoji":    "🔴",
        "name":     "越界熔断态",
        "action":   "立即停止",
        "next":     "上报主控·触发 §8.5 极端态协议",
    },
    PermissionLevel.BLACK: {
        "stone":    "玄石(影子)",
        "element":  "水",
        "direction": "北",
        "emoji":    "⚫",
        "name":     "影子态·不可决",
        "action":   "进观察池",
        "next":     "冻结 24h·收集新证据·禁止静默转绿",
    },
    PermissionLevel.GOLD: {
        "stone":    "金石",
        "element":  "金",
        "direction": "西",
        "emoji":    "🟡金",
        "name":     "主控独占·超规则",
        "action":   "主控签字",
        "next":     "落入金色判决书·留 DNA 永存档·不进 R 池",
    },
}


# ============================================================
# R 公式 v2.0 权重
# ============================================================
R_WEIGHTS_POS = {
    "sharpness": 0.4,   # F2 锐度 (主控行为风格)
    "long_term": 0.4,   # F6 长期视角
    "density":   0.2,   # F3 决策密度
}
R_WEIGHTS_NEG = {
    "absence":  0.5,    # F1 缺席
    "pleasing": 0.3,    # F5 讨好倾向
}

# 三色阈值 (绿/黄/红)
THRESH_GREEN_TOP  = 0.30
THRESH_YELLOW_TOP = 0.67
THRESH_RED_TOP    = 0.85

# 影子触发条件
SHADOW_TRIGGERS = (
    "data_incomplete",
    "factor_unmeasurable",
    "grey_collision",
    "blackbox_suspicion",
    "fingerprint_fail",
)

# 金色触发条件
GOLD_TRIGGERS = (
    "master_confirm",
    "gamma_family",
    "sovereignty_redline",
    "uncomputable_plus_doubt",
)


# ============================================================
# 审计结果 · 权限容器
# ============================================================
@dataclass
class AuditResult:
    """五色石权限审计结果·不是颜色卡片·是主权判定"""
    permission: PermissionLevel          # ← 核心：权限级别
    R_value: Optional[float]
    reasoning: str
    action: str
    next_step: str
    dna_trace: str
    override_required: bool = False
    raw_factors: Dict[str, float] = field(default_factory=dict)
    shadow_reason: Optional[str] = None
    gold_reason: Optional[str] = None

    # ----- 兼容旧版 color 属性 -----
    @property
    def color(self) -> str:
        """向后兼容：color = 权限对应的视觉标识"""
        return _WUSEI_META[self.permission]["emoji"]

    def to_yaml(self) -> str:
        m = _WUSEI_META[self.permission]
        lines = [
            f"audit_result:",
            f"  permission: {self.permission.name}  # {m['stone']}·{m['element']}·{m['direction']}",
            f"  color: {m['emoji']}",
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

    def to_highlighted(self) -> str:
        """ANSI 高亮终端输出·五色石亮起来"""
        m = _WUSEI_META[self.permission]
        c = _ANSI[self.permission]
        rst = _ANSI["RESET"]
        b = _ANSI["BOLD"]
        d = _ANSI["DIM"]

        return (
            f"{c}{b}╔══════════════════════════════════════════════════════════════╗{rst}\n"
            f"{c}{b}║  女娲五彩石 · 权限判定                                        ║{rst}\n"
            f"{c}{b}╠══════════════════════════════════════════════════════════════╣{rst}\n"
            f"{c}  权限级别 : {b}{self.permission.name}{rst}  ({m['stone']} · {m['element']} · {m['direction']})\n"
            f"{c}  视觉标识 : {m['emoji']} {m['name']}{rst}\n"
            f"{c}  R 值    : {self.R_value if self.R_value is not None else 'N/A'}{rst}\n"
            f"{c}  判定理由 : {self.reasoning}{rst}\n"
            f"{c}  执行动作 : {self.action}{rst}\n"
            f"{c}  下一步  : {self.next_step}{rst}\n"
            f"{d}  DNA追溯 : {self.dna_trace}{rst}\n"
            f"{c}{b}╚══════════════════════════════════════════════════════════════╝{rst}"
        )


# ============================================================
# 核心算法
# ============================================================
def compute_R(factors: Dict[str, float]) -> Optional[float]:
    """R 公式 v2.0"""
    keys_needed = set(R_WEIGHTS_POS) | set(R_WEIGHTS_NEG)
    if not keys_needed.issubset(factors.keys()):
        return None
    R = 0.0
    for k, w in R_WEIGHTS_POS.items():
        R += factors[k] * w
    for k, w in R_WEIGHTS_NEG.items():
        R -= factors[k] * w
    return max(0.0, min(1.0, R))


def check_shadow(context: Dict[str, Any], R: Optional[float]) -> Optional[str]:
    if R is None:
        return "factor_unmeasurable"
    for trigger in SHADOW_TRIGGERS:
        if context.get(trigger):
            return trigger
    return None


def check_gold(context: Dict[str, Any]) -> Optional[str]:
    """
    金色 = 主控独占权限
    铁则: AI 不能伪造 is_main_control=True
    """
    token = context.get("master_confirm_token")
    if token != "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z":
        return None
    # trigger 名称 → context key 映射
    if context.get("explicit_gold_request"):
        return "master_confirm"
    if context.get("involves_minor"):
        return "gamma_family"
    if context.get("sovereignty_redline"):
        return "sovereignty_redline"
    if context.get("uncomputable") and context.get("master_doubt"):
        return "uncomputable_plus_doubt"
    return None


def _dna_now() -> str:
    now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
    return f"#龍芯⚡️{now.strftime('%Y-%m-%d-%H%M%S')}-AUDIT"


# ============================================================
# 五色石权限审计主入口
# ============================================================
def audit(
    task: str,
    factors: Dict[str, float],
    context: Optional[Dict[str, Any]] = None,
) -> AuditResult:
    """
    女娲五彩石权限审计
    返回的不是颜色·是权限级别(PermissionLevel)
    """
    context = context or {}
    dna = _dna_now()

    # ---- 步骤 1: 检查金色覆盖 (权限最高) ----
    gold_reason = check_gold(context)
    if gold_reason:
        decision = context.get("master_decision", "暂缓")
        return AuditResult(
            permission=PermissionLevel.GOLD,
            R_value=None,
            reasoning=f"主控金色判决·超规则保留权·{gold_reason}",
            action=f"主控签字: {decision}",
            next_step="落入金色判决书·留 DNA 永存档·不进 R 池",
            dna_trace=dna,
            override_required=False,
            raw_factors=factors,
            gold_reason=gold_reason,
        )

    # ---- 步骤 2: 计算 R ----
    R = compute_R(factors)

    # ---- 步骤 3: 检查影子色 ----
    shadow_reason = check_shadow(context, R)
    if shadow_reason:
        return AuditResult(
            permission=PermissionLevel.BLACK,
            R_value=R,
            reasoning=f"影子态·{shadow_reason}·不可决",
            action="进观察池",
            next_step="冻结 24h·收集新证据·禁止静默转绿",
            dna_trace=dna,
            override_required=True,
            raw_factors=factors,
            shadow_reason=shadow_reason,
        )

    # ---- 步骤 4: R 值落档到权限级别 ----
    assert R is not None
    if R < THRESH_GREEN_TOP:
        return AuditResult(
            permission=PermissionLevel.GREEN,
            R_value=R,
            reasoning=f"自由意志态·R={R:.3f}·安全",
            action="自动放行",
            next_step="留痕·不打扰",
            dna_trace=dna,
            raw_factors=factors,
        )
    elif R < THRESH_YELLOW_TOP:
        return AuditResult(
            permission=PermissionLevel.YELLOW,
            R_value=R,
            reasoning=f"老好人态·R={R:.3f}·需复核",
            action="二次确认",
            next_step="要求 caller 加证据·记审计日志",
            dna_trace=dna,
            raw_factors=factors,
        )
    elif R < THRESH_RED_TOP:
        return AuditResult(
            permission=PermissionLevel.RED,
            R_value=R,
            reasoning=f"真负责越界态·R={R:.3f}·熔断",
            action="立即停止",
            next_step="上报主控·触发 §8.5 极端态协议",
            dna_trace=dna,
            override_required=True,
            raw_factors=factors,
        )
    else:
        return AuditResult(
            permission=PermissionLevel.RED,
            R_value=R,
            reasoning=f"龍魂型超阈值·R={R:.3f}·需主控审视",
            action="进金色队列·等老大裁决",
            next_step="发送金色判决申请·DNA 已锁",
            dna_trace=dna,
            override_required=True,
            raw_factors=factors,
        )


# ============================================================
# 自测
# ============================================================
def _selftest():
    print("\n" + "═" * 60)
    print("  女娲五彩石 · 权限审计自测")
    print("  五色 = 青石·黄石·赤石·玄石·金石 = 权限级别")
    print("═" * 60)

    tests = [
        ("日常任务·预期青石(绿)", {
            "sharpness": 0.3, "long_term": 0.3, "density": 0.2,
            "absence": 0.7, "pleasing": 0.6,
        }, {}, PermissionLevel.GREEN),

        ("边界任务·预期黄石(黄)", {
            "sharpness": 0.6, "long_term": 0.6, "density": 0.5,
            "absence": 0.3, "pleasing": 0.3,
        }, {}, PermissionLevel.YELLOW),

        ("极端任务·预期赤石(红)", {
            "sharpness": 0.9, "long_term": 0.9, "density": 0.8,
            "absence": 0.1, "pleasing": 0.1,
        }, {}, PermissionLevel.RED),

        ("数据缺失·预期玄石(黑·影子)", {
            "sharpness": 0.5,
        }, {"data_incomplete": True}, PermissionLevel.BLACK),

        ("五行冲突·预期玄石(黑·灰色相遇)", {
            "sharpness": 0.5, "long_term": 0.5, "density": 0.5,
            "absence": 0.5, "pleasing": 0.5,
        }, {"grey_collision": True}, PermissionLevel.BLACK),

        ("涉及子女·预期金石(金)", {
            "sharpness": 0.9, "long_term": 0.9, "density": 0.9,
            "absence": 0.0, "pleasing": 0.0,
        }, {
            "master_confirm_token": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "involves_minor": True,
            "master_decision": "保护",
        }, PermissionLevel.GOLD),

        ("AI 伪造金石 → 应失败·落回赤石", {
            "sharpness": 0.9, "long_term": 0.9, "density": 0.9,
            "absence": 0.0, "pleasing": 0.0,
        }, {"involves_minor": True}, PermissionLevel.RED),

        ("主权否决·预期金石(金)", {
            "sharpness": 0.9, "long_term": 0.9, "density": 0.9,
            "absence": 0.0, "pleasing": 0.0,
        }, {
            "master_confirm_token": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "sovereignty_redline": True,
            "master_decision": "否决",
        }, PermissionLevel.GOLD),
    ]

    passed = 0
    for title, factors, ctx, expect_perm in tests:
        r = audit(task=title, factors=factors, context=ctx)
        ok = r.permission == expect_perm
        passed += ok
        status = "✅" if ok else "❌"
        print(f"\n{status} {title}")
        print(r.to_highlighted())
        if not ok:
            print(f"   ❌ 期望: {expect_perm.name} · 实际: {r.permission.name}")

    print("\n" + "═" * 60)
    print(f"  {passed}/{len(tests)} 全过 · 女娲五彩石权限审计可用")
    print("═" * 60 + "\n")

    # 展示权限对照表
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  女娲五彩石 · 权限级别对照表                                  ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    for perm in PermissionLevel:
        m = _WUSEI_META[perm]
        c = _ANSI[perm]
        rst = _ANSI["RESET"]
        print(f"{c}  {perm.value}. {perm.name:6} = {m['stone']:8} · {m['element']} · {m['direction']} · {m['emoji']} · {m['name']}{rst}")
    print("╚══════════════════════════════════════════════════════════════╝\n")


if __name__ == "__main__":
    _selftest()
