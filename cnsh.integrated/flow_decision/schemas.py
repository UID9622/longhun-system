#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂流场决策核 v4.1·数据结构定义
CNSH Flow Decision Core v4.1 - Schema Definitions

DNA: #龍芯⚡️2026-05-03-CNSH-FLOW-DECISION-CORE-v4.1-SCHEMAS
PARENT_DNA: #龍芯⚡️2026-05-03-CNSH-FLOW-DECISION-CORE-v4.1
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

责任: UID9622·不免责
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal, Any
from enum import Enum
from datetime import datetime


# ============================================================================
# 枚举类型定义
# ============================================================================

class VisibilityEnum(str, Enum):
    """可见性枚举"""
    PUBLIC = "public"
    INTERNAL = "internal"
    PRIVATE = "private"


class TraceModeEnum(str, Enum):
    """追溯模式枚举"""
    CHAIN = "chain"
    LOCAL_ONLY = "local_only"
    NO_EXTERNAL = "no_external"


class WuxingEnum(str, Enum):
    """五行枚举"""
    METAL = "金"
    WOOD = "木"
    WATER = "水"
    FIRE = "火"
    EARTH = "土"


class PalaceEnum(str, Enum):
    """九宫枚举"""
    PALACE_1 = "1坎"
    PALACE_2 = "2坤"
    PALACE_3 = "3震"
    PALACE_4 = "4巽"
    PALACE_5 = "5中"
    PALACE_6 = "6乾"
    PALACE_7 = "7兑"
    PALACE_8 = "8艮"
    PALACE_9 = "9离"


class BucketEnum(str, Enum):
    """沙盒分拣桶"""
    FUSE = "🔴熔断"
    BURN = "📝内部消化"
    SEALED = "🔒封存隐私"
    NORMAL = "🟢通过"
    HOLD = "🟡待审"


class AuditColorEnum(str, Enum):
    """三色审计"""
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


class LevelEnum(str, Enum):
    """数据层级"""
    L0_ETERNAL = "L0永恒"
    L1_CENTURY = "L1百年"
    L3_DAILY = "L3日常"
    L5_TEMP = "L5临时"


class StatusEnum(str, Enum):
    """最终状态"""
    ENTER = "enter"
    HOLD = "hold"
    FUSE = "fuse"


class PersonaEnum(str, Enum):
    """人格编号"""
    P00_WENXIN = "P00"
    P01_ZHUGELVLIANG = "P01"
    P03_WANWAN = "P03"
    P05_GODSEYE = "P05"
    P06_MATHMASTER = "P06"
    P13_JIANGZIYA = "P13"
    P14_LVMENG = "P14"
    P15_QIAOQIANDAI = "P15"
    P72_LONGSHIELD = "P72"


# ============================================================================
# 主数据类定义（38字段）
# ============================================================================

@dataclass
class PrivacyConfig:
    """隐私配置"""
    visibility: VisibilityEnum
    trace_mode: TraceModeEnum
    raw_body_allowed: bool = False


@dataclass
class MathConfig:
    """数学配置（五行、三才、生克）"""
    element: WuxingEnum = field(default=WuxingEnum.EARTH)
    sancai_heaven: float = 0.35  # 天
    sancai_earth: float = 0.15   # 地
    sancai_human: float = 0.50   # 人（必须≥0.34）
    shengke_with_parent: Optional[str] = None  # 与父DNA的生克关系


@dataclass
class DigitalRootConfig:
    """数字根配置（四源优先级）"""
    explicit_dr: Optional[int] = None      # 显式给定（优先级1）
    dna_digits: Optional[int] = None       # DNA字符串提取（优先级2）
    content_hash_dr: Optional[int] = None  # 内容hash（优先级3）
    raw_digits_dr: Optional[int] = None    # 原文数字（优先级4）
    fallback_dr: int = 5                   # 默认土（优先级5）

    def get_primary_dr(self) -> int:
        """按四源优先级返回最终dr"""
        if self.explicit_dr is not None:
            return self.explicit_dr
        if self.dna_digits is not None:
            return self.dna_digits
        if self.content_hash_dr is not None:
            return self.content_hash_dr
        if self.raw_digits_dr is not None:
            return self.raw_digits_dr
        return self.fallback_dr


@dataclass
class AuditConfig:
    """审计配置"""
    color: AuditColorEnum
    need_uid_confirm: bool = False
    reason: str = ""


@dataclass
class RouteConfig:
    """路由配置"""
    palace: List[PalaceEnum]
    bucket: BucketEnum
    main_persona: PersonaEnum
    assist_persona: Optional[List[PersonaEnum]] = None


@dataclass
class StorageConfig:
    """存储配置"""
    notion: bool = True
    jsonl: bool = True
    sqlite: bool = True
    destroy_proof: Optional[str] = None  # burn时生成sha256
    seal_proof: Optional[str] = None     # sealed时生成sha256


@dataclass
class DNATagPolicy:
    """DNA多标签策略"""
    visibility: VisibilityEnum
    trace_mode: TraceModeEnum
    operator: str
    p0_touched: bool
    level: LevelEnum
    parent_dna: str = ""
    child_dna: Optional[str] = None


@dataclass
class IPAReceipt:
    """IPA节点回执"""
    ipa_node: str
    ipa_address: str
    main_persona: PersonaEnum
    input_node_id: str
    output_signal: Literal["pass", "hold", "fuse"]
    next_ipa: Optional[str] = None
    dna: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class GateReceipt:
    """闸口回执"""
    gate_name: str
    gate_number: int
    main_persona: PersonaEnum
    assist_personas: List[PersonaEnum] = field(default_factory=list)
    hard_rule_triggered: str = ""
    signal: Literal["pass", "hold", "fuse"] = "pass"
    ipa_receipt: Optional[IPAReceipt] = None


@dataclass
class FlowDecisionNode:
    """流场决策节点 - 完整38字段定义"""

    # ===== 核心身份字段 (5) =====
    title: str
    node_id: str  # 格式: FLOW-9622-YYYYMMDD-8charHash
    confirm_code: str = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    gpg: str = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    dna: str = ""

    # ===== 链接字段 (2) =====
    parent_dna: str = ""
    child_dna: Optional[str] = None

    # ===== 隐私与追溯 (2) =====
    privacy: PrivacyConfig = field(default_factory=lambda: PrivacyConfig(
        visibility=VisibilityEnum.INTERNAL,
        trace_mode=TraceModeEnum.CHAIN
    ))
    dna_tags: DNATagPolicy = field(default_factory=lambda: DNATagPolicy(
        visibility=VisibilityEnum.INTERNAL,
        trace_mode=TraceModeEnum.CHAIN,
        operator="",
        p0_touched=False,
        level=LevelEnum.L3_DAILY
    ))

    # ===== 数学层（五行、三才、生克） (3) =====
    math: MathConfig = field(default_factory=MathConfig)
    digital_root: DigitalRootConfig = field(default_factory=DigitalRootConfig)

    # ===== 审计层 (2) =====
    audit: AuditConfig = field(default_factory=lambda: AuditConfig(
        color=AuditColorEnum.GREEN
    ))
    gate_receipts: List[GateReceipt] = field(default_factory=list)

    # ===== 路由与派位 (2) =====
    route: RouteConfig = field(default_factory=lambda: RouteConfig(
        palace=[PalaceEnum.PALACE_5],
        bucket=BucketEnum.NORMAL,
        main_persona=PersonaEnum.P00_WENXIN
    ))
    ipa_chain: List[IPAReceipt] = field(default_factory=list)

    # ===== 存储配置 (1) =====
    storage: StorageConfig = field(default_factory=StorageConfig)

    # ===== 结果与操作 (3) =====
    result_status: StatusEnum = StatusEnum.ENTER
    result_operator: str = "UID9622"
    result_timestamp: datetime = field(default_factory=datetime.now)

    # ===== 内容与元数据 (4) =====
    raw_input: str = ""
    raw_body: Optional[str] = None
    content_hash: str = ""
    tags: Dict[str, Any] = field(default_factory=dict)

    # ===== 备注与回溯 (2) =====
    remarks: str = ""
    trace_info: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# 工具函数
# ============================================================================

def validate_sancai_human(value: float) -> bool:
    """验证人才权重 ≥ 0.34"""
    return value >= 0.34


def dr_to_wuxing(dr: int) -> WuxingEnum:
    """数字根转五行"""
    mapping = {
        1: WuxingEnum.WATER,
        2: WuxingEnum.WOOD,
        3: WuxingEnum.WOOD,
        4: WuxingEnum.FIRE,
        5: WuxingEnum.FIRE,
        6: WuxingEnum.EARTH,
        7: WuxingEnum.METAL,
        8: WuxingEnum.METAL,
        9: WuxingEnum.WATER,
        0: WuxingEnum.EARTH,
    }
    return mapping.get(dr % 10, WuxingEnum.EARTH)


def palette_to_color(palace: PalaceEnum) -> AuditColorEnum:
    """九宫到三色的快速映射（示例）"""
    # 坎(1) 坤(2) = 水/地 → 🟢
    # 震(3) 巽(4) = 木 → 🟢
    # 乾(6) 兑(7) = 金 → 🟢
    # 艮(8) 离(9) = 山/火 → 🟢
    # 中(5) = 待审 → 🟡
    if palace == PalaceEnum.PALACE_5:
        return AuditColorEnum.YELLOW
    return AuditColorEnum.GREEN
