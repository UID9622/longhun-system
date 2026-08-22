# DNA: #龍芯⚡️丙午·丙申·甲子·甲戌·䷍大有-CODE-补DNA-1c743d88
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""test_credibility.py — 可信度公式引擎测试（锚点3、锚点4）。"""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from longhun_trust.credibility import (
    ConfirmationState,
    FactRecord,
    SourceLevel,
    compute_credibility,
    freshness,
    needs_confirmation,
)


class TestFreshness:
    """F = clamp(1 - age_days/90, 0, 1)。"""

    def test_zero_age(self):
        assert freshness(0) == 1.0

    def test_half_decay(self):
        assert freshness(45) == pytest.approx(0.5)

    def test_full_decay(self):
        assert freshness(90) == pytest.approx(0.0)

    def test_beyond_90_clamped_to_zero(self):
        assert freshness(180) == 0.0

    def test_negative_age_clamped_to_one(self):
        assert freshness(-10) == 1.0

    def test_nan_raises_value_error(self):
        """Y1：NaN 输入绝不给满分，直接 raise ValueError。"""
        with pytest.raises(ValueError):
            freshness(float("nan"))

    def test_inf_raises_value_error(self):
        """Y1：inf/-inf 同样拒绝。"""
        with pytest.raises(ValueError):
            freshness(float("inf"))
        with pytest.raises(ValueError):
            freshness(float("-inf"))

    def test_compute_credibility_nan_raises(self):
        """Y1：compute_credibility 对 NaN age 同样 fail-closed。"""
        with pytest.raises(ValueError):
            compute_credibility(
                float("nan"), SourceLevel.FOUNDER, ConfirmationState.CONFIRMED
            )
        with pytest.raises(ValueError):
            compute_credibility(
                float("inf"), SourceLevel.FOUNDER, ConfirmationState.CONFIRMED
            )


class TestComputeCredibility:
    """锚点3：按公式实算。"""

    def test_anchor_founder_confirmed_fresh(self):
        assert compute_credibility(
            0, SourceLevel.FOUNDER, ConfirmationState.CONFIRMED
        ) == 1.0

    def test_anchor_founder_confirmed_45d(self):
        # F = 1 - 45/90 = 0.5 → 0.4×0.5 + 0.3×1.0 + 0.3×1.0 = 0.8
        assert compute_credibility(
            45, SourceLevel.FOUNDER, ConfirmationState.CONFIRMED
        ) == 0.8

    def test_unknown_disputed_old(self):
        # F=0 → 0.4×0 + 0.3×0.2 + 0.3×0 = 0.06
        assert compute_credibility(
            365, SourceLevel.UNKNOWN, ConfirmationState.DISPUTED
        ) == pytest.approx(0.06)

    def test_system_unconfirmed(self):
        # F=1 → 0.4 + 0.3×0.8 + 0.3×0.3 = 0.73
        assert compute_credibility(
            0, SourceLevel.SYSTEM, ConfirmationState.UNCONFIRMED
        ) == pytest.approx(0.73)

    def test_rounded_4_digits(self):
        score = compute_credibility(
            7, SourceLevel.COMMUNITY, ConfirmationState.UNCONFIRMED
        )
        assert score == round(score, 4)


class TestNeedsConfirmation:
    """锚点4：阈值 0.7。"""

    def test_below_threshold(self):
        assert needs_confirmation(0.69) is True

    def test_at_threshold(self):
        assert needs_confirmation(0.7) is False

    def test_above_threshold(self):
        assert needs_confirmation(1.0) is False


class TestFactRecord:
    def test_score_with_injected_now(self):
        now = datetime(2026, 8, 18, 12, 0, 0)
        rec = FactRecord(
            key="退伍年限",
            value=18,
            source=SourceLevel.FOUNDER,
            confirmation=ConfirmationState.CONFIRMED,
            recorded_at=now - timedelta(days=45),
        )
        assert rec.score(now=now) == 0.8

    def test_score_defaults_to_now(self):
        rec = FactRecord(
            key="k",
            value="v",
            source=SourceLevel.SYSTEM,
            confirmation=ConfirmationState.CONFIRMED,
            recorded_at=datetime.now(),
        )
        # 刚记录：F≈1 → 0.4+0.24+0.3=0.94
        assert rec.score() == pytest.approx(0.94, abs=1e-3)


class TestEnumValues:
    def test_source_level_values(self):
        assert SourceLevel.FOUNDER.value == 1.0
        assert SourceLevel.SYSTEM.value == 0.8
        assert SourceLevel.COMMUNITY.value == 0.5
        assert SourceLevel.UNKNOWN.value == 0.2

    def test_confirmation_state_values(self):
        assert ConfirmationState.CONFIRMED.value == 1.0
        assert ConfirmationState.UNCONFIRMED.value == 0.3
        assert ConfirmationState.DISPUTED.value == 0.0
