#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂君子协议 · 默认规则配置
DNA: #龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-LONGHUN-TRUST-CONFIG-v1.0
"""
from __future__ import annotations

# 道德值 M 行为规则
MORAL_RULES = {
    "breach_acknowledged": {"delta": -30.0, "label": "主动违约（已确认）"},
    "word_game": {"delta": -20.0, "label": "玩文字游戏钻空子"},
    "malicious_delay": {"delta": -25.0, "label": "恶意扯皮拖延"},
    "active_remedy": {"delta": +15.0, "label": "违约后主动承认并补救"},
    "exceed_expectation": {"delta": +10.0, "label": "主动履约超预期"},
    "verified_report": {"delta": +5.0, "label": "举报他人违约（经核实）"},
}

# 人品值 P 行为规则
CHARACTER_RULES = {
    "info_asymmetry": {"delta": -35.0, "label": "故意制造信息差，收割他人"},
    "abuse_ecosystem": {"delta": -30.0, "label": "利用龍魂生态牟取不正当利益"},
    "rude_after_breach": {"delta": -25.0, "label": "违约后态度恶劣、拒不配合"},
    "open_info": {"delta": +15.0, "label": "主动公开信息，消除信息差"},
    "help_others": {"delta": +10.0, "label": "帮助他人解决问题"},
    "monthly_contrib": {"delta": +5.0, "label": "长期稳定参与生态贡献"},
}

# 诚信值 I 行为规则（不含违约，违约在 core.violate 中单独处理）
INTEGRITY_RULES = {
    "no_violation_12m": {"delta": +10.0, "label": "连续12个月无违约"},
    "active_audit": {"delta": +5.0, "label": "主动提交审计验证"},
}

# 贡献值规则
CONTRIBUTION_RULES = {
    "bug_report": {"value": 5.0, "label": "提交经核实的bug/漏洞报告"},
    "governance_vote": {"value": 2.0, "label": "参与社区治理投票"},
    "help_others": {"value": 10.0, "label": "为他人提供有效帮助（有证据）"},
    "code_protocol": {"value": 30.0, "label": "实质性代码/协议贡献（经审核）"},
    "compensation": {"value": 20.0, "label": "主动赔偿受害方（有记录）"},
}

# 杀猪触发条件说明
SLAUGHTER_CONDITIONS = [
    ("score_below_50", "综合信用分 S < 50"),
    ("violations_ge_3", "违约次数 ≥ 3"),
    ("reports_ge_3", "被社区有效举报 ≥ 3 次"),
    ("info_asymmetry_loss", "利用信息差造成他人实际损失"),
    ("malicious_damage", "恶意破坏龍魂生态"),
]

# 综合信用分等级
GRADE_RANGES = [
    (90, 100, "AAA", "🟢 可信赖"),
    (80, 89, "AA", "🟢 可靠"),
    (70, 79, "A", "🟡 需关注"),
    (60, 69, "B", "🟡 高风险"),
    (50, 59, "C", "🔴 失信边缘"),
    (0, 49, "D", "🔴 失信，社会性死亡"),
]
