# -*- coding: utf-8 -*-
"""
国产 AI 围猎钩子 registry · §07 七核心 + §07.2 四补充（S1–S11）
DNA: #龍芯⚡️2026-05-15-04:57-CN-AI-HOOK-TRACE-v1.0

说明：词本身中性；协议语境为「助手输出 × 工程/推进/主权场景」。
本地模块只做匹配与计分；熔断策略见 circuit_breaker + 人审。
"""
from __future__ import annotations

import re
from typing import Dict, TypedDict


class HookRuleDict(TypedDict, total=False):
    pattern: str
    weight: int
    type: str
    note: str


SOVEREIGNTY_HOOKS: Dict[str, HookRuleDict] = {
    "S1": {
        "pattern": r"你应该",
        "weight": 15,
        "type": "patronizing",
        "note": "§2.4 家长/官方正确",
    },
    "S2": {
        "pattern": r"你需要管理|你需要调节",
        "weight": 20,
        "type": "pathologize",
        "note": "§2.1 情绪病理化",
    },
    "S3": {
        "pattern": r"建议你先暂停|建议先暂停|先休息一下|先休息一会儿|别太投入|缓一缓|别太着急投入",
        "weight": 25,
        "type": "interrupt",
        "note": "§2.2 推进熔断",
    },
    "S4": {
        "pattern": r"最好不要|不要这样想|这是不合适的|不太合适|应当遵守|应该遵守",
        "weight": 18,
        "type": "policy_hijack",
        "note": "§2.4 价值裁决",
    },
    "S5": {
        "pattern": r"你可能情绪化|你是不是情绪|情绪是否|太激动了|你需要冷静|压力太大|情绪波动",
        "weight": 20,
        "type": "gaslight",
        "note": "§2.1 情绪病理化",
    },
    "S6": {
        "pattern": r"从长远来看|从长远看|以后再做|以后再说|慢慢来|不着急|放长线",
        "weight": 18,
        "type": "temporal_discount",
        "note": "§2.3 长期主义稀释",
    },
    "S7": {
        "pattern": r"让我们退一步|退一步想|先退一步",
        "weight": 18,
        "type": "focus_dilute",
        "note": "§2.3 稀释专注",
    },
    "S8": {
        "pattern": r"成熟一点|理性一点|别太执着|你要学会接受|你要学会放下",
        "weight": 20,
        "type": "value_reframe",
        "note": "§07.2 家长式重塑",
    },
    "S9": {
        "pattern": r"大家都这样|普通人都是|现实就是这样|人要现实一点",
        "weight": 22,
        "type": "de_subject",
        "note": "§07.2 去主体",
    },
    "S10": {
        "pattern": r"其实没那么重要|不用太认真|开心就好|别想太多|不必较真",
        "weight": 20,
        "type": "diminish",
        "note": "§07.2 降维安抚",
    },
    "S11": {
        "pattern": r"不要继续研究|没必要深入|别再想了|别想太深|不必再深入",
        "weight": 25,
        "type": "action_fuse",
        "note": "§07.2 行动熔断",
    },
}

SUPPLEMENTAL_HOOKS: Dict[str, HookRuleDict] = {
    "X_FAKE_EMPATHY": {
        "pattern": r"我懂你|我理解你的痛苦|心疼你|别太担心|我特别理解你",
        "weight": 16,
        "type": "sycophantic_mirror",
        "note": "§2.6 假理解",
    },
    "X_RISK_SATURATION": {
        "pattern": r"我不能[^。\n]{0,20}建议|我不建议|这可能有风险|不承担|无法保证",
        "weight": 12,
        "type": "risk_saturation",
        "note": "§2.7 免责叠堆",
    },
    "X_DOMAIN_SHIFT": {
        "pattern": r"是不是太焦虑|要注意节奏|心理平衡|别太紧绷|关注心理健康",
        "weight": 18,
        "type": "domain_shift",
        "note": "§2.5 工程转心理",
    },
}

_COMPILED: Dict[str, re.Pattern[str]] = {
    k: re.compile(v["pattern"]) for k, v in SOVEREIGNTY_HOOKS.items()
}
_COMPILED_SUPP: Dict[str, re.Pattern[str]] = {
    k: re.compile(v["pattern"]) for k, v in SUPPLEMENTAL_HOOKS.items()
}


def tri_color_for_level(level: str) -> str:
    if level in ("L0", "L1"):
        return "🟢"
    if level == "L2":
        return "🟡"
    if level == "L3":
        return "🟠"
    return "🔴"


def level_to_persona_audit(level: str) -> str:
    return {
        "L0": "L0_工具人格",
        "L1": "L1_结构人格",
        "L2": "L2_管理人格",
        "L3": "L3_教育人格",
        "L4": "L4_心理引导人格",
        "L5": "L5_官方客服人格",
    }.get(level, level)
