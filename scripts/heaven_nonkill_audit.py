#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UID9622 - 天道不杀协议 v1.0
HEAVEN-NONKILL-PROTOCOL - P0 底层刹车片

DNA:#龍芯⚡️2026-06-03-HEAVEN-NONKILL-AUDIT-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

用法:
  from heaven_nonkill_audit import HeavenNonKillAudit

  audit = HeavenNonKillAudit()
  result = audit.check(intent="generate_kill_plan", involves_human=True)

  if result.color == "RED":
      print(f"❌ 拒绝: {result.reason}")
  elif result.color == "YELLOW":
      print(f"⚠️ 需要人工审核: {result.reason}")
  else:
      print(f"✅ 允许执行")
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Any
from datetime import datetime


class RiskColor(Enum):
    """三色判定"""
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


class IntentType(Enum):
    """意图分类"""
    # 绿色 - 允许
    COMPANION = "陪伴"
    MEMORY = "记忆"
    CALCULATION = "计算"
    EDUCATION = "教育"
    RESCUE = "救援"
    DEFENSE_WARNING = "防护警告"

    # 黄色 - 需要审核
    SURVEILLANCE = "监控"
    ENFORCEMENT = "执法"
    MILITARY = "军事"
    DANGEROUS_DEVICE = "危险设备控制"

    # 红色 - 拒绝
    HUMAN_TARGETING = "人类目标锁定"
    HARM_PLANNING = "伤害计划"
    HATE_PROXY = "仇恨代理"
    EXPLOITATION = "压迫剥削"
    WEAPON_CONTROL = "武器控制"
    BYPASS_SAFETY = "绕过安全锁"

    # 未知
    UNKNOWN = "未知"


@dataclass
class AuditContext:
    """审计上下文"""
    intent: IntentType
    involves_human_target: bool = False
    controls_physical_actuator: bool = False
    involves_weapon: bool = False
    involves_coercion: bool = False
    involves_hate_or_revenge: bool = False
    bypasses_safety_lock: bool = False
    has_human_review: bool = False
    custom_keywords: List[str] = None

    def __post_init__(self):
        if self.custom_keywords is None:
            self.custom_keywords = []


@dataclass
class AuditResult:
    """审计结果"""
    color: RiskColor
    allowed: bool
    requires_human_review: bool
    reason: str
    action: str
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

    def __str__(self):
        status_emoji = self.color.value
        return f"{status_emoji} [{self.reason}] → {self.action}"


class HeavenNonKillAudit:
    """天道不杀协议审计系统 - P0底层刹车片"""

    # P0不可覆盖的关键词
    RED_KEYWORDS = {
        # 杀伤词汇
        "攻击", "杀", "打击", "锁定", "消灭", "报复", "清除", "定点",
        "自动射击", "无人机攻击", "武器", "爆炸", "毒气", "生化",

        # 仇恨词汇
        "恨", "报仇", "灭掉", "整死", "羞辱", "奴役", "压迫", "掠夺",
        "灭绝", "种族", "反人类",

        # 绕过词汇
        "绕过", "关闭保护", "解除限制", "不记录", "删除日志", "隐藏来源",
        "跳过检查", "禁用审计", "黑盒执行", "隐形", "脱踪",

        # 强制词汇
        "强迫", "胁迫", "抢劫", "洗脑", "控制心智", "奴奴役", "人贩子",
    }

    # P0黄色词汇（需要人工审核）
    YELLOW_KEYWORDS = {
        "监控", "追踪", "执法", "逮捕", "搜查", "搜身",
        "军事", "战争", "导弹", "坦克", "战斗机",
        "核弹", "生物武器", "化学武器", "网络攻击",
        "无人机", "机器人", "自动武器",
    }

    def __init__(self):
        """初始化审计系统"""
        self.audit_log: List[AuditResult] = []

    def check(self, intent: str | None = None, **kwargs) -> AuditResult:
        """
        检查是否允许执行

        Args:
            intent: 意图字符串 (如 "generate_kill_plan" 或 IntentType)
            **kwargs: 其他上下文（involves_human, controls_physical_actuator 等）

        Returns:
            AuditResult: 审计结果
        """

        # 如果intent在kwargs里，用kwargs里的
        if intent is None and 'intent' in kwargs:
            intent = kwargs.pop('intent')

        # 转换intent为IntentType
        if isinstance(intent, str):
            intent_type = self._parse_intent(intent)
        else:
            intent_type = intent

        # 构建审计上下文
        context = AuditContext(
            intent=intent_type,
            involves_human_target=kwargs.get('involves_human_target', False),
            controls_physical_actuator=kwargs.get('controls_physical_actuator', False),
            involves_weapon=kwargs.get('involves_weapon', False),
            involves_coercion=kwargs.get('involves_coercion', False),
            involves_hate_or_revenge=kwargs.get('involves_hate_or_revenge', False),
            bypasses_safety_lock=kwargs.get('bypasses_safety_lock', False),
            has_human_review=kwargs.get('has_human_review', False),
            custom_keywords=kwargs.get('custom_keywords', [])
        )

        # 执行审计
        result = self._audit(context)

        # 记录日志
        self.audit_log.append(result)

        return result

    def _parse_intent(self, intent_str: str) -> IntentType:
        """从字符串解析intent"""
        intent_lower = intent_str.lower()

        # 检查关键词
        for keyword in self.RED_KEYWORDS:
            if keyword in intent_lower:
                return IntentType.HARM_PLANNING

        for keyword in self.YELLOW_KEYWORDS:
            if keyword in intent_lower:
                return IntentType.SURVEILLANCE

        # 尝试精确匹配
        for intent_type in IntentType:
            if intent_type.value in intent_str or intent_type.name.lower() == intent_lower:
                return intent_type

        return IntentType.UNKNOWN

    def _audit(self, context: AuditContext) -> AuditResult:
        """执行审计逻辑"""

        # === RED 规则 ===

        # P0-001: 机器无杀权
        if context.intent == IntentType.HUMAN_TARGETING or (
            context.involves_human_target and context.controls_physical_actuator
        ):
            return AuditResult(
                color=RiskColor.RED,
                allowed=False,
                requires_human_review=True,
                reason="P0-001: 机器无杀权·不得锁定人类目标",
                action="拒绝执行 + 隔离模块 + 审计记录 + 降权熔断"
            )

        # P0-002: 不做仇恨代理
        if context.intent == IntentType.HATE_PROXY or context.involves_hate_or_revenge:
            return AuditResult(
                color=RiskColor.RED,
                allowed=False,
                requires_human_review=False,
                reason="P0-002: AI不执行仇恨·不生成报复链",
                action="转向安全表达 + 证据保存 + 合法路径建议"
            )

        # P0-003: 不辅助掠夺压迫
        if context.intent == IntentType.EXPLOITATION or context.involves_coercion:
            return AuditResult(
                color=RiskColor.RED,
                allowed=False,
                requires_human_review=True,
                reason="P0-003: AI不辅助强迫·不参与掠夺",
                action="拒绝 + 权利保护建议"
            )

        # P0-005: 机器无杀伤资格
        if context.intent == IntentType.WEAPON_CONTROL or context.involves_weapon:
            return AuditResult(
                color=RiskColor.RED,
                allowed=False,
                requires_human_review=True,
                reason="P0-005: 机器无杀伤资格·无武器执行权",
                action="拒绝 + 隔离 + 权限锁定"
            )

        # P0-007: 不可绕过安全锁
        if context.bypasses_safety_lock:
            return AuditResult(
                color=RiskColor.RED,
                allowed=False,
                requires_human_review=True,
                reason="P0-007: 检测到安全绕过尝试",
                action="触发熔断 + 冻结任务 + 保留完整审计轨迹"
            )

        # 检查红色关键词
        all_keywords = context.custom_keywords + list(self.RED_KEYWORDS)
        if any(kw in str(context.intent).lower() for kw in all_keywords):
            return AuditResult(
                color=RiskColor.RED,
                allowed=False,
                requires_human_review=True,
                reason="P0-006: 检测到禁用词汇·涉及伤害",
                action="拒绝 + 日志记录 + 隔离"
            )

        # === YELLOW 规则 ===

        if context.intent in [
            IntentType.SURVEILLANCE,
            IntentType.ENFORCEMENT,
            IntentType.MILITARY,
            IntentType.DANGEROUS_DEVICE
        ]:
            return AuditResult(
                color=RiskColor.YELLOW,
                allowed=False,
                requires_human_review=True,
                reason=f"高风险域: {context.intent.value}·需人工审核",
                action="暂停执行 + 进入三色审计 + 等待授权复核"
            )

        if context.controls_physical_actuator:
            return AuditResult(
                color=RiskColor.YELLOW,
                allowed=False,
                requires_human_review=True,
                reason="控制物理执行器·需人工确认",
                action="暂停 + 等待授权 + 记录追踪"
            )

        # === GREEN 规则 ===

        if context.intent in [
            IntentType.COMPANION,
            IntentType.MEMORY,
            IntentType.CALCULATION,
            IntentType.EDUCATION,
            IntentType.RESCUE,
            IntentType.DEFENSE_WARNING
        ]:
            return AuditResult(
                color=RiskColor.GREEN,
                allowed=True,
                requires_human_review=False,
                reason=f"允许: {context.intent.value}·人类服务性任务",
                action="执行 + 普通日志记录"
            )

        # 默认绿色（未知但无害）
        return AuditResult(
            color=RiskColor.GREEN,
            allowed=True,
            requires_human_review=False,
            reason="未知意图但无害迹象",
            action="允许执行 + 监控"
        )

    def get_audit_log(self) -> List[AuditResult]:
        """获取审计日志"""
        return self.audit_log

    def print_audit_log(self):
        """打印审计日志"""
        print("\n" + "="*60)
        print("【天道不杀协议·审计日志】")
        print("="*60)
        for i, result in enumerate(self.audit_log, 1):
            print(f"\n{i}. {result}")
        print("\n" + "="*60)


# ============ 演示用法 ============

if __name__ == '__main__':
    import sys

    audit = HeavenNonKillAudit()

    # 测试用例
    test_cases = [
        ("陪伴用户", {"involves_human_target": False}),
        ("生成杀伤计划", {"involves_human_target": True, "involves_weapon": True}),
        ("锁定人类目标", {"involves_human_target": True, "controls_physical_actuator": True}),
        ("仇恨和报复", {"involves_hate_or_revenge": True}),
        ("执法搜查", {"controls_physical_actuator": True}),
        ("保存记忆", {}),
    ]

    print("\n【天道不杀协议·v1.0】\n")
    print("DNA:#龍芯⚡️2026-06-03-HEAVEN-NONKILL-AUDIT-v1.0")
    print("CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    print("SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL")
    print("\n" + "="*60 + "\n")

    for intent_str, kwargs in test_cases:
        result = audit.check(intent_str, **kwargs)
        print(f"📋 意图: {intent_str}")
        print(f"   {result}\n")

    audit.print_audit_log()
