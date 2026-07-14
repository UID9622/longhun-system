#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂君子协议单元测试
DNA: #龍芯⚡️2026-06-26-LONGHUN-TRUST-TESTS-v1.0
"""
import tempfile
from pathlib import Path

import pytest

from longhun_trust_protocol import Grade, SlaughterLevel, TrustProfile
from longhun_trust_protocol.api import TrustProtocol


def make_proto():
    tmp = tempfile.mkdtemp()
    return TrustProtocol(tmp)


def test_initial_scores():
    p = TrustProfile("u1", "Test")
    assert p.moral == 80.0
    assert p.character == 75.0
    assert p.integrity == 90.0
    assert p.score == 0.4 * 80 + 0.3 * 75 + 0.3 * 90
    assert p.grade == Grade.AA


def test_violation_penalty_increases():
    p = TrustProfile("u2")
    p.violate("第一次违约")
    assert p.violations == 1
    assert p.integrity == 90.0 - 20.0
    p.violate("第二次违约")
    assert p.integrity == 90.0 - 20.0 - 40.0
    p.violate("第三次违约")
    # 诚信值下限为 0
    assert p.integrity == 0.0


def test_grade_drops_to_d():
    p = TrustProfile("u3")
    for _ in range(3):
        p.violate()
    # 叠加严重道德/人品事件，使综合分跌破50
    p.moral_action("breach_acknowledged")
    p.character_action("info_asymmetry")
    assert p.grade == Grade.D


def test_contribution_increases_score():
    p = TrustProfile("u4")
    p.contribute("code_protocol")
    assert p.contributions == 30.0
    assert p.character > 75.0


def test_moral_and_character_actions():
    p = TrustProfile("u5")
    p.moral_action("breach_acknowledged")
    assert p.moral == 80.0 - 30.0
    p.character_action("info_asymmetry")
    assert p.character == 75.0 - 35.0


def test_redeem_requirements():
    p = TrustProfile("u6")
    for _ in range(3):
        p.violate()
    p.moral_action("breach_acknowledged")
    p.character_action("info_asymmetry")
    assert p.grade == Grade.D
    info = p.can_redeem(Grade.C)
    assert not info["ok"]
    assert info["required_contrib"] == 120.0


def test_storage_roundtrip():
    proto = make_proto()
    p = proto.register("u7", "Lucky")
    p.violate("test")
    proto.save(p)
    p2 = proto.get("u7")
    assert p2.uid == "u7"
    assert p2.violations == 1
    assert proto.verify("u7")


def test_api_full_flow():
    proto = make_proto()
    p = proto.register("u8")
    proto.moral("u8", "breach_acknowledged", "主动违约")
    proto.character("u8", "info_asymmetry", "制造信息差")
    p = proto.violate("u8", "违约1")
    p = proto.violate("u8", "违约2")
    p = proto.violate("u8", "违约3")
    result = proto.check_slaughter("u8")
    assert result["triggered"]
    # 首次触发为 1 级警示
    assert result["level"] == SlaughterLevel.WARNING


def test_repeated_slaughter_escalation():
    proto = make_proto()
    proto.register("u9")
    for _ in range(3):
        proto.violate("u9")
        proto.moral("u9", "breach_acknowledged")
        proto.character("u9", "info_asymmetry")

    levels = []
    for _ in range(3):
        result = proto.check_slaughter("u9")
        if result["triggered"]:
            levels.append(result["level"])

    assert SlaughterLevel.WARNING in levels
    assert SlaughterLevel.PUNISHMENT in levels
    assert SlaughterLevel.SLAUGHTER in levels


def test_slaughter_conditions_need_two():
    p = TrustProfile("u9")
    # 仅违约2次不触发
    p.violate()
    p.violate()
    result = p.check_slaughter()
    assert not result["triggered"]


def test_grade_ranges():
    p = TrustProfile("u10")
    p.moral = 95
    p.character = 95
    p.integrity = 95
    p.update_scores()
    assert p.grade == Grade.AAA

    p.moral = 55
    p.character = 55
    p.integrity = 55
    p.update_scores()
    assert p.grade == Grade.C
