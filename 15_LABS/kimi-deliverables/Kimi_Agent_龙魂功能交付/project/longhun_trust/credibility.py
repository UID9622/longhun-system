# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-844a6074
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""龍魂信任核心 · 可信度公式引擎。

公式：C = 0.4·F + 0.3·S + 0.3·K；F = clamp(1 - age_days/90, 0, 1)；
阈值 C < 0.7 → 待确认（必问）。
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

CREDIBILITY_THRESHOLD: float = 0.7
"""可信度阈值：低于该值必须向用户确认。"""

FRESHNESS_FULL_DAYS: float = 90.0
"""新鲜度线性衰减周期（天）：90 天衰减至 0。"""


class SourceLevel(Enum):
    """来源权重 S。"""

    FOUNDER = 1.0  # 创始人 L0
    SYSTEM = 0.8  # 系统核验过的外部数据
    COMMUNITY = 0.5
    UNKNOWN = 0.2


class ConfirmationState(Enum):
    """确认状态 K。"""

    CONFIRMED = 1.0
    UNCONFIRMED = 0.3
    DISPUTED = 0.0


def _clamp(value: float, low: float, high: float) -> float:
    """把 value 截断到 [low, high] 区间。"""
    return max(low, min(high, value))


def freshness(age_days: float) -> float:
    """计算新鲜度 F = clamp(1 - age_days/90, 0, 1)，90 天线性衰减至 0。

    :param age_days: 事实记录距今天数（负值 clamp 到 0，视为最新）。
    :return: 0..1 的新鲜度。
    :raises ValueError: age_days 为非有限值（nan/inf）——绝不给 NaN 输入算分。
    """
    age = float(age_days)
    if not math.isfinite(age):
        raise ValueError(f"age_days 必须是有限数值，收到 {age_days!r}")
    age = max(0.0, age)
    return _clamp(1.0 - age / FRESHNESS_FULL_DAYS, 0.0, 1.0)


def compute_credibility(
    age_days: float,
    source: SourceLevel,
    confirmation: ConfirmationState,
) -> float:
    """计算可信度 C = 0.4·F + 0.3·S + 0.3·K。

    :param age_days: 事实记录距今天数。
    :param source: 来源权重枚举。
    :param confirmation: 确认状态枚举。
    :return: 0..1 的可信度，round 4 位。
    """
    score = 0.4 * freshness(age_days) + 0.3 * source.value + 0.3 * confirmation.value
    return round(_clamp(score, 0.0, 1.0), 4)


def needs_confirmation(score: float) -> bool:
    """判断可信度是否需要用户确认：score < 0.7 → True。

    :param score: 可信度得分。
    :return: 是否需要确认。
    """
    return score < CREDIBILITY_THRESHOLD


@dataclass
class FactRecord:
    """事实记录：带来源与确认状态，可实时计算可信度。"""

    key: str
    value: Any
    source: SourceLevel
    confirmation: ConfirmationState
    recorded_at: datetime

    def score(self, now: datetime | None = None) -> float:
        """按记录时间计算当前可信度。

        :param now: 参考时间，默认 datetime.now()（可注入便于测试）。
        :return: 0..1 的可信度。
        """
        reference = now if now is not None else datetime.now()
        age_days = max(
            0.0, (reference - self.recorded_at).total_seconds() / 86400.0
        )
        return compute_credibility(age_days, self.source, self.confirmation)
