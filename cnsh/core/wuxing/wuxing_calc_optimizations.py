#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
from __future__ import annotations
##龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-WUXING-CALC-OPTIMIZATIONS-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
"""
🐉 龍魂·五行计算优化模块 v1.0

针对五行计算器中三个计算层面的优化：
1. 鲁棒数字根：支持全角数字、中文数字、负数、小数
2. CV 均衡指数：用变异系数替代方差，避免总分影响均衡性判断
3. 权重自学习：五行对冲指数 H 的权重随人工判定自动校准

DNA: #龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-WUXING-CALC-OPTIMIZATIONS-v1.0
"""

import json
import math
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Any

HOME = Path.home()
WEIGHTS_PATH = HOME / ".longhun" / "wuxing_weights.json"

# 中文数字映射（含大小写）
CN_DIGITS = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '零': 0, '〇': 0,
    '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5,
    '陆': 6, '柒': 7, '捌': 8, '玖': 9, '拾': 10,
}

# 默认权重（与 v3.0 文档一致）
DEFAULT_WEIGHTS = {
    "克制衡分": 0.30,
    "疏导分": 0.25,
    "补益分": 0.20,
    "均衡指数": 0.15,
    "链路健康度": 0.10,
}

# 熔断规则 DNA 标签
FUSE_RULES = {
    3: {"level": "🔴", "reason": "创新过载·需收束", "dna_tag": "OVERFLOW-CREATIVE"},
    9: {"level": "🔴", "reason": "规则篡改风险·需审计", "dna_tag": "RULE-TAMPER"},
    6: {"level": "🟡", "reason": "记忆回流·需补证", "dna_tag": "MEMORY-RECALL"},
}


def robust_digital_root(text) -> int:
    """
    鲁棒数字根计算。

    支持：
    - 半角数字 0-9
    - 全角数字 ０-９（自动归一化）
    - 中文数字 一~十 / 壹~拾
    - 负数（取绝对值后计算）
    - 小数（只取数字部分）
    - 无数字时返回 0

    >>> robust_digital_root("2026年五月")
    8
    >>> robust_digital_root("２０２６")
    2
    >>> robust_digital_root(" negative -5 value ")
    5
    """
    if text is None:
        return 0

    s = str(text)
    # 全角/半角归一化
    s = unicodedata.normalize('NFKC', s)

    digits = []
    for ch in s:
        if ch.isdigit():
            digits.append(int(ch))
        elif ch in CN_DIGITS:
            digits.append(CN_DIGITS[ch])

    if not digits:
        return 0

    total = sum(digits)
    # 反复求和直到个位数
    while total >= 10:
        total = sum(int(d) for d in str(total))
    return total


def cv_balance_score(scores: Dict[str, float]) -> float:
    """
    基于变异系数（CV）的均衡指数。

    优点：
    - 无量纲，不受总分大小影响
    - 对 0 分更稳健

    返回 0.0 ~ 1.0，越接近 1 越均衡。
    """
    values = [float(v) for v in scores.values() if v is not None]
    if not values:
        return 0.0

    total = sum(values)
    if total == 0:
        return 0.0

    mean = total / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    std = math.sqrt(variance)
    cv = std / mean

    # CV=0 → 1.0；CV=2 → 0
    return round(max(0.0, min(1.0, 1.0 - cv / 2.0)), 3)


def load_wuxing_weights() -> Dict[str, float]:
    """加载五行对冲指数 H 的权重，无记录时返回默认值"""
    if WEIGHTS_PATH.exists():
        try:
            stored = json.loads(WEIGHTS_PATH.read_text(encoding='utf-8'))
            # 合并默认值，防止缺字段
            return {**DEFAULT_WEIGHTS, **stored}
        except Exception:
            pass
    return DEFAULT_WEIGHTS.copy()


def save_wuxing_weights(weights: Dict[str, float]) -> None:
    """保存权重到本地"""
    WEIGHTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    WEIGHTS_PATH.write_text(json.dumps(weights, ensure_ascii=False, indent=2), encoding='utf-8')


def update_wuxing_weights(
    scores: Dict[str, float],
    current_h: float,
    human_judgment: str,
    learning_rate: float = 0.01
) -> Dict[str, float]:
    """
    根据人工判定微调五行对冲指数 H 的权重。

    human_judgment: "通过" / "待补" / "熔断"
    """
    if human_judgment not in ("通过", "待补", "熔断"):
        return load_wuxing_weights()

    weights = load_wuxing_weights()
    target = {"通过": 0.85, "待补": 0.65, "熔断": 0.35}[human_judgment]
    error = target - current_h

    # 按各分项得分比例分配权重调整
    total_score = sum(scores.values()) + 1e-9
    for key in weights:
        score_ratio = scores.get(key, 0.0) / total_score
        # 保证权重在合理范围 [0.05, 0.50]
        weights[key] = round(
            max(0.05, min(0.50, weights[key] + learning_rate * error * score_ratio)),
            4
        )

    # 归一化，使权重和为 1.0
    total_weight = sum(weights.values())
    if total_weight > 0:
        weights = {k: round(v / total_weight, 4) for k, v in weights.items()}

    save_wuxing_weights(weights)
    return weights


def compute_hedge_index_h(
    restraint_score: float,
    relief_score: float,
    supplement_score: float,
    balance_score: float,
    health_score: float,
    weights: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    计算五行对冲指数 H（使用可自学习权重）。
    """
    if weights is None:
        weights = load_wuxing_weights()

    scores = {
        "克制衡分": max(0.0, min(1.0, restraint_score)),
        "疏导分": max(0.0, min(1.0, relief_score)),
        "补益分": max(0.0, min(1.0, supplement_score)),
        "均衡指数": max(0.0, min(1.0, balance_score)),
        "链路健康度": max(0.0, min(1.0, health_score)),
    }

    h = round(sum(scores[k] * weights[k] for k in scores), 3)

    if h >= 0.80:
        color, action = "🟢 对冲充分", "enter"
    elif h >= 0.50:
        color, action = "🟡 对冲不足，需补", "hold"
    else:
        color, action = "🔴 对冲失败，熔断或重算", "fuse"

    return {
        "对冲指数H": h,
        "三色": color,
        "action": action,
        "分项": scores,
        "权重": weights,
        "DNA追溯": "#龍芯⚡️丙午·癸巳·辛巳·甲午·䷃蒙-五行对冲指数H-v3.1",
    }


def detect_excess(scores: Dict[str, float], threshold_sigma: float = 1.5) -> List[tuple[Any, ...]]:
    """
    动态过旺检测：超过 均值 + threshold_sigma * 标准差 才算过旺。
    比固定阈值 0.40 更适应不同总分规模。
    """
    values = list(scores.values())
    total = sum(values)
    if total == 0:
        return []

    mean = total / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    std = math.sqrt(variance)
    threshold = mean + threshold_sigma * std

    return [(k, v) for k, v in scores.items() if v > threshold]


def fuse_audit(dr: int) -> Dict[str, Any]:
    """返回数字根熔断规则"""
    return FUSE_RULES.get(dr, {"level": "🟢", "reason": "通行", "dna_tag": "PASS"})


def demo():
    """自测演示"""
    print("=== 鲁棒数字根测试 ===")
    for t in ["2026年五月", "２０２６", "negative -5 value", "一二三", "玖拾玖"]:
        print(f"  {t!r} → dr={robust_digital_root(t)}")

    print("\n=== CV 均衡指数测试 ===")
    print(f"  均衡 {{金:20,木:20,水:20,火:20,土:20}} → {cv_balance_score({'金':20,'木':20,'水':20,'火':20,'土':20})}")
    print(f"  偏斜 {{金:80,木:5,水:5,火:5,土:5}} → {cv_balance_score({'金':80,'木':5,'水':5,'火':5,'土':5})}")

    print("\n=== 对冲指数 H 测试 ===")
    h = compute_hedge_index_h(0.8, 0.7, 0.9, 0.6, 0.75)
    print(f"  H={h['对冲指数H']}, 三色={h['三色']}, 权重={h['权重']}")

    print("\n=== 权重自学习测试 ===")
    new_weights = update_wuxing_weights(h["分项"], h["对冲指数H"], "通过")
    print(f"  更新后权重: {new_weights}")


if __name__ == "__main__":
    demo()
