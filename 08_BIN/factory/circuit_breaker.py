#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-CIRCUIT-BREAKER-UID9622
# 创建者: 诸葛鑫（UID9622）
"""
🐉 龍魂 · 四级熔断引擎 v1.0（v2.0 补全区块·对齐系统 L0/L1/L2/L3 熔断）
功能: 连续失败自动熔断 + 告警升级 + 冻结留档 + 恢复条件

级别:
  L0/∞ 伦理 — 涉童/伪造DNA/背叛人民 → 全系统冻结，不可恢复
  L1 数据   — 敏感字段泄露/明文密码 → 拒绝+MELTDOWN，人工+GPG恢复
  L2 人格   — 越权/身份伪装          → 禁用该职能，重设恢复
  L3 行为   — 连续失败N次/数字根不符 → 锁定当前任务，自动恢复
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List

from .generate_dna import generate_dna


class BreakerLevel(Enum):
    L0 = "∞/L0"
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"


@dataclass
class BreakerRule:
    """熔断规则"""
    level: BreakerLevel
    threshold: int          # 连续失败触发次数
    cooldown_seconds: int   # 冷却时间
    auto_recover: bool      # 是否自动恢复
    recover_condition: str  # 恢复条件描述


class CircuitBreaker:
    """四级熔断器"""

    DEFAULT_RULES = {
        BreakerLevel.L3: BreakerRule(BreakerLevel.L3, 3, 300, True, "数字根复算通过/连续3次成功"),
        BreakerLevel.L2: BreakerRule(BreakerLevel.L2, 2, 1800, False, "人格重设+审计通过"),
        BreakerLevel.L1: BreakerRule(BreakerLevel.L1, 1, 0, False, "UID9622人工+GPG签章"),
        BreakerLevel.L0: BreakerRule(BreakerLevel.L0, 1, -1, False, "不可恢复（永久）"),
    }

    def __init__(self, rules: Dict[BreakerLevel, BreakerRule] = None):
        self.rules = rules or self.DEFAULT_RULES
        self.fail_counts: Dict[str, int] = {}
        self.tripped_at: Dict[str, datetime] = {}
        self.events: List[Dict] = []

    def register_failure(self, key: str, level: BreakerLevel = BreakerLevel.L3) -> Dict:
        """记录一次失败，达到阈值即熔断"""
        dna = generate_dna(f"BREAK-{level.value.replace('/', '')}")
        rule = self.rules[level]
        self.fail_counts[key] = self.fail_counts.get(key, 0) + 1
        count = self.fail_counts[key]

        event = {
            "dna": dna,
            "key": key,
            "level": level.value,
            "count": count,
            "threshold": rule.threshold,
            "tripped": count >= rule.threshold,
            "timestamp": datetime.now().isoformat(),
        }
        self.events.append(event)

        if count >= rule.threshold:
            self.tripped_at[key] = datetime.now()
            event["action"] = "TRIP"
            if not rule.auto_recover:
                event["recover"] = rule.recover_condition

        return event

    def is_tripped(self, key: str, level: BreakerLevel = BreakerLevel.L3) -> bool:
        """检查是否处于熔断状态（含冷却恢复逻辑）"""
        rule = self.rules[level]
        if rule.cooldown_seconds < 0:  # L0 永久
            return key in self.tripped_at
        tripped_at = self.tripped_at.get(key)
        if not tripped_at:
            return False
        if not rule.auto_recover:
            return True  # L1/L2 需人工
        # L3 冷却期后自动复位
        return datetime.now() - tripped_at < timedelta(seconds=rule.cooldown_seconds)

    def reset(self, key: str) -> None:
        """人工/条件恢复后重置"""
        self.fail_counts.pop(key, None)
        self.tripped_at.pop(key, None)

    def status(self) -> Dict:
        """熔断器总状态"""
        return {
            "dna": generate_dna("BREAK-STATUS"),
            "tripped_keys": {k: v.value for k, v in self.tripped_at.items()},
            "event_count": len(self.events),
            "timestamp": datetime.now().isoformat(),
        }
