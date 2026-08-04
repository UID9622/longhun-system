#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂生态桥接模块 · 河图洛书 × 易经 × 七因子
DNA: #龍芯⚡️2026-07-05-HETU-LUOSHU-YIJING-7FACTOR-BRIDGE-v1.0
"""

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Dict, Union, Any

# 把 governance 目录加入路径，复用 SevenFactorVerifier
_GOV_DIR = Path(__file__).resolve().parent.parent / "governance"
if str(_GOV_DIR) not in sys.path:
    sys.path.insert(0, str(_GOV_DIR))

from f1_through_f7_verifier import (
    F1IdentityVerification,
    F2TemporalAnchor,
    F3RuleTrace,
    F4PersonaRouting,
    F5ProtectedVocabulary,
    F6StyleVector,
    F7MistakeLedger,
    SevenFactorVerifier,
    VerificationFactor,
)


# ═══════════════════════════════════════════════════════════════
# 河图洛书 · 数字根与不动点
# ═══════════════════════════════════════════════════════════════

def digital_root(n: int) -> int:
    """反复数字求和，n=0 返回 0"""
    if n == 0:
        return 0
    return 1 + ((n - 1) % 9)


def digital_root_invariant_check(value: Union[int, str]) -> Dict[str, Any]:
    """
    对任意整数或字符串计算数字根，输出三色动作。
    字符串会先被哈希成整数，再求数字根。
    """
    if isinstance(value, str):
        raw_int = int(hashlib.sha256(value.encode("utf-8")).hexdigest(), 16)
    else:
        raw_int = int(value)

    dr = digital_root(raw_int)

    if dr in {3, 9}:
        color, action, laozi = "🔴", "熔断", "第33章·知足者富；第40章·反者道之动"
    elif dr == 6:
        color, action, laozi = "🟡", "待审", "第44章·知足不辱，知止不殆"
    else:
        color, action, laozi = "🟢", "通行", "第16章·归根曰静，是谓复命"

    return {
        "input_type": "str" if isinstance(value, str) else "int",
        "digital_root": dr,
        "color": color,
        "action": action,
        "laozi": laozi,
        "is_hard_fail": dr in {3, 9},
    }


# ═══════════════════════════════════════════════════════════════
# 七因子 → 八卦 8 维度映射
# ═══════════════════════════════════════════════════════════════

SEVEN_FACTOR_TO_BAGUA = {
    # 七因子: (维度名, 八卦, 维度说明)
    "F1": ("defense", "☶ 艮", "身份验证 → 坚守防御度"),
    "F2": ("response", "☳ 震", "时间锚定 → 快速响应度"),
    "F3": ("risk_control", "☵ 坎", "规则追踪 → 风险管控度"),
    "F4": ("collaboration", "☱ 兑", "人格路由 → 协作联动度"),
    "F5": ("communication", "☲ 离", "保护词汇 → 传播表达度"),
    "F6": ("optimization", "☴ 巽", "风格向量 → 渗透优化度"),
    "F7": ("support", "☷ 坤", "错误日志 → 支持辅助度"),
}

BAGUA_SCORE_RANGES = [
    (90, "☰", "乾"),
    (80, "☱", "兑"),
    (70, "☲", "离"),
    (60, "☳", "震"),
    (50, "☴", "巽"),
    (40, "☵", "坎"),
    (30, "☶", "艮"),
    (0,  "☷", "坤"),
]


def score_to_gua(score: float) -> str:
    """0-100 分数映射到八卦符号"""
    for threshold, symbol, _ in BAGUA_SCORE_RANGES:
        if score >= threshold:
            return symbol
    return "☷"


def seven_factor_to_bagua(factors: Dict[str, float]) -> Dict[str, Any]:
    """
    把 F1-F7 因子映射到 64 卦审计所需的 8 维度指标。
    创新突破度由七因子综合置信度转换。
    """
    metrics = {}
    for f_key, (dim_name, _, desc) in SEVEN_FACTOR_TO_BAGUA.items():
        score = factors.get(f_key, 0.0) * 100
        metrics[dim_name] = round(score, 2)

    # 创新突破度：综合七因子几何平均 × 100
    geo_mean = math.exp(sum(math.log(max(v, 1e-9)) for v in factors.values()) / len(factors))
    metrics["innovation"] = round(geo_mean * 100, 2)

    # 上卦：创新 + 传播 + 协作
    upper_score = (
        metrics["innovation"] * 0.4 +
        metrics["communication"] * 0.3 +
        metrics["collaboration"] * 0.3
    )
    upper_gua = score_to_gua(upper_score)

    # 下卦：支持 + 风险 + 防御
    lower_score = (
        metrics["support"] * 0.3 +
        metrics["risk_control"] * 0.4 +
        metrics["defense"] * 0.3
    )
    lower_gua = score_to_gua(lower_score)

    combo = upper_gua + lower_gua

    return {
        "metrics": metrics,
        "upper_gua": upper_gua,
        "lower_gua": lower_gua,
        "gua_combo": combo,
        "upper_score": round(upper_score, 2),
        "lower_score": round(lower_score, 2),
    }


# ═══════════════════════════════════════════════════════════════
# 64 卦简表（关键卦象）
# ═══════════════════════════════════════════════════════════════

LIUSHISI_GUA = {
    "☰☰": {"name": "乾为天", "risk_level": "low", "suggestion": "创新势头强劲，保持前行"},
    "☰☷": {"name": "天地泰", "risk_level": "low", "suggestion": "天地交泰，系统通畅"},
    "☷☰": {"name": "天地否", "risk_level": "high", "suggestion": "天地不交，系统阻塞，需紧急干预"},
    "☵☰": {"name": "水天需", "risk_level": "medium", "suggestion": "险在前方，等待时机"},
    "☱☵": {"name": "泽水困", "risk_level": "high", "suggestion": "系统困顿，资源匮乏"},
    "☷☷": {"name": "坤为地", "risk_level": "medium", "suggestion": "系统稳固但缺乏动力"},
    "☰☵": {"name": "天水讼", "risk_level": "high", "suggestion": "争议风险，谨慎沟通"},
    "☵☷": {"name": "水地比", "risk_level": "low", "suggestion": "亲近互助，利于协作"},
    "☳☰": {"name": "雷天大壮", "risk_level": "medium", "suggestion": "力量充沛，但防过刚"},
    "☰☴": {"name": "天风姤", "risk_level": "medium", "suggestion": "不期而遇，留意变数"},
    "☲☰": {"name": "火天大有", "risk_level": "low", "suggestion": "光明盛大，收获在望"},
    "☰☶": {"name": "天山遁", "risk_level": "medium", "suggestion": "适时退避，保存实力"},
    "☱☰": {"name": "泽天夬", "risk_level": "medium", "suggestion": "果断决策，去旧迎新"},
    "☰☱": {"name": "天泽履", "risk_level": "low", "suggestion": "循礼而行，稳步前进"},
    "☴☷": {"name": "风地观", "risk_level": "medium", "suggestion": "观察形势，再做决断"},
    "☷☳": {"name": "地雷复", "risk_level": "low", "suggestion": "一阳来复，转机初现"},
}


def determine_audit_color(gua_info: Dict[str, Any], metrics: Dict[str, Any]) -> str:
    """根据卦象与指标判定三色"""
    risk_level = gua_info.get("risk_level", "medium")
    values = list(metrics.values())
    avg_score = sum(values) / len(values)
    min_score = min(values)

    if risk_level == "low" and avg_score >= 70 and min_score >= 50:
        return "🟢"
    elif risk_level == "high" or avg_score < 50 or min_score < 30:
        return "🔴"
    return "🟡"


# ═══════════════════════════════════════════════════════════════
# 人格路由
# ═══════════════════════════════════════════════════════════════

GUA_TO_PERSONA_GROUP = {
    "☰": "乾卦组·创新突破",
    "☷": "坤卦组·支持辅助",
    "☳": "震卦组·快速响应",
    "☴": "巽卦组·渗透优化",
    "☵": "坎卦组·风险管控",
    "☲": "离卦组·传播表达",
    "☶": "艮卦组·坚守防御",
    "☱": "兑卦组·协作联动",
}


def route_persona(upper_gua: str, lower_gua: str) -> Dict[str, Any]:
    return {
        "upper_group": GUA_TO_PERSONA_GROUP.get(upper_gua, "未知组"),
        "lower_group": GUA_TO_PERSONA_GROUP.get(lower_gua, "未知组"),
        "primary": "决策层 + " + GUA_TO_PERSONA_GROUP.get(upper_gua, "未知组"),
    }


# ═══════════════════════════════════════════════════════════════
# 完整生态审计入口
# ═══════════════════════════════════════════════════════════════

def audit_with_ecosystem(
    factors: Dict[str, float],
    content: str,
    metadata: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    龍魂生态完整审计：
    七因子 → 8 维度 → 64 卦 → 数字根红线 → 人格路由 → 道德经引用
    """
    metadata = metadata or {}

    # 1. 七因子置信度（复用已有验证器）
    verifier = SevenFactorVerifier()
    f_scores = {
        "F1": factors.get("F1", 0.0),
        "F2": factors.get("F2", 0.0),
        "F3": factors.get("F3", 0.0),
        "F4": factors.get("F4", 0.0),
        "F5": factors.get("F5", 0.0),
        "F6": factors.get("F6", 0.0),
        "F7": factors.get("F7", 0.0),
    }

    # 权重映射（字符串 key -> 枚举 key）
    weight_map = {
        "F1": VerificationFactor.F1_IDENTITY,
        "F2": VerificationFactor.F2_TEMPORAL,
        "F3": VerificationFactor.F3_RULE_TRACE,
        "F4": VerificationFactor.F4_PERSONA,
        "F5": VerificationFactor.F5_VOCABULARY,
        "F6": VerificationFactor.F6_STYLE,
        "F7": VerificationFactor.F7_MISTAKES,
    }

    # 硬失败检查
    hard_fail = any(v == 0 for v in f_scores.values())
    if hard_fail:
        confidence = 0.0
        passed = False
    else:
        confidence = math.prod(
            math.pow(v, SevenFactorVerifier.WEIGHTS[weight_map[k]])
            for k, v in f_scores.items()
        )
        passed = confidence >= verifier.DEFAULT_THRESHOLD

    # 2. 映射到八卦 8 维度
    bagua_result = seven_factor_to_bagua(f_scores)
    metrics = bagua_result["metrics"]
    combo = bagua_result["gua_combo"]
    gua_info = LIUSHISI_GUA.get(combo, {"name": "未收录卦象", "risk_level": "medium", "suggestion": "需补充卦辞"})

    # 3. 数字根红线：对 8 维度指标之和求数字根
    # 对应洛书"任意方向三数之和恒为 15"的哲学：系统状态数值必须先过 369 红线
    metrics_sum = int(round(sum(metrics.values())))
    dr_result = digital_root_invariant_check(metrics_sum)

    # 4. 综合三色：卦象结果 + 数字根红线
    color_from_gua = determine_audit_color(gua_info, metrics)
    final_color = "🔴" if dr_result["is_hard_fail"] else color_from_gua
    final_action = "熔断" if final_color == "🔴" else ("待审" if final_color == "🟡" else "通行")

    # 5. 人格路由
    persona_route = route_persona(bagua_result["upper_gua"], bagua_result["lower_gua"])

    return {
        "dna": "#龍芯⚡️2026-07-05-HETU-LUOSHU-YIJING-7FACTOR-BRIDGE-v1.0",
        "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        "seven_factor": {
            "scores": f_scores,
            "confidence": round(confidence, 4),
            "passed": passed,
            "hard_fail": hard_fail,
        },
        "bagua": bagua_result,
        "gua": gua_info,
        "digital_root": dr_result,
        "audit": {
            "color": final_color,
            "action": final_action,
            "laozi": dr_result["laozi"],
        },
        "persona_route": persona_route,
        "metadata": metadata,
    }


# ═══════════════════════════════════════════════════════════════
# 演示
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🐉 龍魂生态桥接模块 v1.0\n")

    # 高信任场景
    good_factors = {
        "F1": 1.0, "F2": 0.9, "F3": 0.9,
        "F4": 0.95, "F5": 1.0, "F6": 0.88, "F7": 1.0
    }
    result = audit_with_ecosystem(
        factors=good_factors,
        content="龍魂系统为人民服务",
        metadata={"uid": "UID9622", "persona": "P02"}
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 数字根熔断场景
    print("\n--- 红线场景：数字根触发熔断 ---\n")
    fail_content = "x" * 999  # 任意长串，看数字根是否命中 {3,9}
    result2 = audit_with_ecosystem(
        factors=good_factors,
        content=fail_content,
        metadata={"scenario": "红线测试"}
    )
    print(f"内容哈希数字根: {result2['digital_root']['digital_root']}")
    print(f"最终审计: {result2['audit']['color']} {result2['audit']['action']}")

    # 七因子硬失败场景
    print("\n--- 硬失败场景：F1=0 ---\n")
    bad_factors = dict(good_factors)
    bad_factors["F1"] = 0.0
    result3 = audit_with_ecosystem(
        factors=bad_factors,
        content="测试硬失败",
        metadata={"scenario": "硬失败测试"}
    )
    print(f"七因子置信度: {result3['seven_factor']['confidence']}")
    print(f"最终审计: {result3['audit']['color']} {result3['audit']['action']}")
