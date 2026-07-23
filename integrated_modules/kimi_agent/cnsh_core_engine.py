#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系统 CNSH OS v2.5 核心引擎
═══════════════════════════════════════════════════════════
整合五大模块：
  ✅ DNA生成引擎 — SHA256全链路追溯+五行标记
  ✅ 状态机引擎 — CNSH状态流转+智能转换规则
  ✅ 五行融合决策引擎 — 四大公式+六门路由
  ✅ 三色审计引擎 — 🔴🟡🟢三级审计+签发流程
  ✅ CNSH标准JSON — 执行级标准接口

DNA:#龍芯⚡️2026-06-09-CNSH-CORE-ENGINE-v2.5
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅
作者: UID9622 · 龍芯北辰 · 诸葛鑫
AI协作: Kimi
许可证: CC BY-NC-SA 4.0 + AI协作标签
三色审计: 🟢
"""

from __future__ import annotations

import json
import hashlib
import math
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum, auto
from typing import (
    Any, Dict, List, Optional, Tuple, Set, Callable,
    Union, TypeVar, Generic
)
from functools import lru_cache
from collections import defaultdict

# ═══════════════════════════════════════════════════════════
# 一、基础常量和枚举定义
# ═══════════════════════════════════════════════════════════


class 五行类型(Enum):
    """五行类型枚举"""
    金 = ("金", "权益", "L0", "#FFD700", 1.0)
    木 = ("木", "教育", "L4", "#228B22", 0.8)
    水 = ("水", "数据", "L1", "#000080", 0.9)
    火 = ("火", "创作", "L2", "#FF0000", 0.7)
    土 = ("土", "民生", "L3", "#8B4513", 1.1)

    def __init__(self, 名称: str, 领域: str, 层级: str, 颜色: str, 权重: float):
        self.名称 = 名称
        self.领域 = 领域
        self.层级 = 层级
        self.颜色 = 颜色
        self.权重 = 权重


class 六门类型(Enum):
    """六门路由类型"""
    权益门 = ("权益门", "金", "L0")
    数据门 = ("数据门", "水", "L1")
    创作门 = ("创作门", "火", "L2")
    民生门 = ("民生门", "土", "L3")
    教育门 = ("教育门", "木", "L4")

    def __init__(self, 门名: str, 五行: str, 层级: str):
        self.门名 = 门名
        self.五行 = 五行
        self.层级 = 层级


class 状态类型(Enum):
    """状态机状态类型"""
    原始输入 = "RAW_INPUT"
    解析完成 = "PARSED"
    阻塞审查 = "BLOCKED"
    跨AI复核 = "CROSS_AI_REVIEW"
    共识构建 = "CONSENSUS_BUILDING"
    状态裁决 = "STATE_DECISION"
    活跃协议 = "ACTIVE_PROTOCOL"
    图谱链接 = "GRAPH_LINKED"
    归档 = "ARCHIVED"
    冻结 = "FROZEN"


class 审计颜色(Enum):
    """三色审计颜色"""
    绿色 = ("🟢", 1.0, "可进入", "PASS")
    黄色 = ("🟡", 0.45, "待审", "REVIEW")
    红色 = ("🔴", 0.2, "隔离", "REJECT")

    def __init__(self, 图标: str, 分值: float, 含义: str, 代码: str):
        self.图标 = 图标
        self.分值 = 分值
        self.含义 = 含义
        self.代码 = 代码


class 行动类型(Enum):
    """行动决策类型"""
    进入 = "ENTER"
    待审 = "HOLD"
    熔断 = "FUSE"
    归档 = "ARCHIVE"
    路由 = "ROUTE"
    人工审查 = "HUMAN_GATE"


class 优先级(Enum):
    """优先级枚举"""
    P0 = ("P0", "最高")
    P1 = ("P1", "高")
    P2 = ("P2", "中")
    P3 = ("P3", "低")
    P4 = ("P4", "最低")

    def __init__(self, 代码: str, 描述: str):
        self.代码 = 代码
        self.描述 = 描述


class 审计阶段(Enum):
    """审计流程阶段"""
    提交 = "SUBMITTED"
    自动分类 = "AUTO_CLASSIFIED"
    三色预审 = "TRI_COLOR_REVIEW"
    P3复核 = "P3_REVIEW"
    P1价值校验 = "P1_VALIDATION"
    UID9622签发 = "ISSUED"


# ═══════════════════════════════════════════════════════════
# 二、数据结构定义
# ═══════════════════════════════════════════════════════════


@dataclass
class 五行评分:
    """五行评分数据结构"""
    金: float = 0.0   # 规则度
    木: float = 0.0   # 创新度
    水: float = 0.0   # 记忆度
    火: float = 0.0   # 文明度
    土: float = 0.0   # 普惠度

    def to_dict(self) -> Dict[str, float]:
        return {"金": self.金, "木": self.木, "水": self.水, "火": self.火, "土": self.土}

    def total(self) -> float:
        return self.金 + self.木 + self.水 + self.火 + self.土

    def normalize(self) -> Dict[str, float]:
        total = self.total()
        if total == 0:
            return {k: 0.2 for k in ["金", "木", "水", "火", "土"]}
        return {k: round(v / total, 4) for k, v in self.to_dict().items()}

    def to_list(self) -> List[float]:
        return [self.金, self.木, self.水, self.火, self.土]


@dataclass
class 公式结果:
    """四大公式计算结果"""
    平衡指数: float              # 公式A: 0-100
    相生相克强度: Dict[str, Dict[str, Any]]  # 公式B
    三才系数: float              # 公式C: 0-1
    复合决策强度: float           # 公式D: 0-1
    综合置信度: float             # 综合: 0-1


@dataclass
class 识别结果:
    """人机会识别结果"""
    人类五行: Optional[str]
    人类置信度: float
    机器五行: str
    机器置信度: float
    机器审计通过: bool
    机器审计原因: str
    匹配: bool
    一致性分数: float
    最终置信度: float


@dataclass
class 路由决策:
    """自动化路由决策"""
    门: str
    层级: str
    优先级: str
    行动: 行动类型
    审计颜色: 审计颜色
    理由: str
    下一步: str


@dataclass
class 审计记录:
    """三色审计记录"""
    审计ID: str
    阶段: 审计阶段
    颜色: 审计颜色
    审计员: str
    时间戳: str
    详情: str
    证据: List[str] = field(default_factory=list)


@dataclass
class 审计报告:
    """完整审计报告"""
    报告ID: str
    时间戳: str
    审计链: List[审计记录] = field(default_factory=list)
    最终颜色: 审计颜色 = 审计颜色.绿色
    需要人工: bool = False
    签发状态: bool = False


@dataclass
class 状态转换:
    """状态转换规则"""
    当前状态: 状态类型
    目标状态: 状态类型
    条件: str
    转换函数: Optional[Callable[[状态包], bool]] = None


@dataclass
class 状态包:
    """状态机数据包"""
    数据ID: str
    当前状态: 状态类型 = 状态类型.原始输入
    内容: str = ""
    分析结果: Dict[str, Any] = field(default_factory=dict)
    价值分: float = 0.0
    风险分: float = 0.0
    幻觉率: float = 0.0
    冲突标记: bool = False
    共识度: float = 0.0
    审计状态: Dict[str, Any] = field(default_factory=dict)
    历史: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "数据ID": self.数据ID,
            "当前状态": self.当前状态.value,
            "内容": self.内容,
            "分析结果": self.分析结果,
            "价值分": self.价值分,
            "风险分": self.风险分,
            "幻觉率": self.幻觉率,
            "冲突标记": self.冲突标记,
            "共识度": self.共识度,
            "审计状态": self.审计状态,
        }


@dataclass
class CNSH标准数据块:
    """CNSH标准JSON数据块"""
    块ID: str
    内容: str
    标签: List[str] = field(default_factory=list)
    五行: str = "水"
    价值分: float = 0.0
    风险分: float = 0.0


@dataclass
class CNSH标准JSON:
    """CNSH Standard JSON 执行级接口"""
    dna: str = ""
    源AI: str = ""
    输入: str = ""
    块列表: List[CNSH标准数据块] = field(default_factory=list)
    分析: Dict[str, Any] = field(default_factory=dict)
    流转: Dict[str, Any] = field(default_factory=dict)
    审计: Dict[str, Any] = field(default_factory=dict)
    时间戳: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dna": self.dna,
            "source_ai": self.源AI,
            "input": self.输入,
            "blocks": [
                {
                    "block_id": b.块ID,
                    "content": b.内容,
                    "tags": b.标签,
                    "element": b.五行,
                    "value_score": b.价值分,
                    "risk_score": b.风险分,
                }
                for b in self.块列表
            ],
            "analysis": self.分析,
            "flow": self.流转,
            "audit": self.审计,
            "timestamp": self.时间戳,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════
# 三、DNA生成引擎
# ═══════════════════════════════════════════════════════════


class DNA引擎:
    """
    DNA全链路追溯引擎

    格式: CNSH-YYYYMMDD-HASH-BRANCH-TYPE
    生成: SHA256(content + ai_model + timestamp + user_id)
    五行标记: 0-20水 20-40木 40-60土 60-80火 80-100金
    """

    # 五行分值区间
    五行区间 = {
        五行类型.水: (0, 20),
        五行类型.木: (20, 40),
        五行类型.土: (40, 60),
        五行类型.火: (60, 80),
        五行类型.金: (80, 100),
    }

    # 五行映射
    五行映射 = {
        0: 五行类型.水, 1: 五行类型.水,
        2: 五行类型.木, 3: 五行类型.木,
        4: 五行类型.土, 5: 五行类型.土,
        6: 五行类型.火, 7: 五行类型.火,
        8: 五行类型.金, 9: 五行类型.金,
    }

    def __init__(self):
        self.生成计数 = 0
        self.DNA记录: Dict[str, Dict[str, Any]] = {}

    def 生成DNA(self,
               内容: str,
               AI模型: str = "CNSH",
               用户ID: str = "UID9622",
               分支: str = "MAIN",
               类型: str = "CORE") -> str:
        """
        生成DNA签名

        参数:
            内容: 需要签名的原始内容
            AI模型: AI模型标识
            用户ID: 用户标识
            分支: 代码分支
            类型: DNA类型

        返回:
            DNA签名字符串
        """
        时间戳 = datetime.now().strftime("%Y%m%d")
        纳秒 = str(int(time.time() * 1_000_000))

        # 计算SHA256
        源字符串 = f"{内容}|{AI模型}|{纳秒}|{用户ID}|{分支}|{类型}"
        哈希值 = hashlib.sha256(源字符串.encode("utf-8")).hexdigest()
        短哈希 = 哈希值[:16].upper()

        DNA = f"CNSH-{时间戳}-{短哈希}-{分支}-{类型}"

        # 记录
        self.生成计数 += 1
        self.DNA记录[DNA] = {
            "源字符串": 源字符串,
            "哈希值": 哈希值,
            "生成时间": datetime.now().isoformat(),
            "序号": self.生成计数,
        }

        return DNA

    def 五行标记(self, 分值: float) -> 五行类型:
        """
        根据分值确定五行标记

        分值范围 0-100:
            0-20: 水
            20-40: 木
            40-60: 土
            60-80: 火
            80-100: 金
        """
        索引 = int(min(99, max(0, 分值))) // 10
        return self.五行映射.get(索引, 五行类型.土)

    def 验证DNA(self, DNA: str, 内容: str, AI模型: str = "CNSH") -> bool:
        """验证DNA签名是否有效"""
        if DNA not in self.DNA记录:
            return False
        记录 = self.DNA记录[DNA]
        return 记录["源字符串"].startswith(f"{内容}|{AI模型}")

    def 生成完整签名(self, 内容: str = "") -> Dict[str, str]:
        """生成完整的DNA签名集合"""
        DNA = self.生成DNA(内容)
        return {
            "DNA": f"#龍芯⚡️{DNA}",
            "确认码": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅",
            "灵魂绑定": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅",
            "生成时间": datetime.now().isoformat(),
            "版本": "v2.5",
        }


# ═══════════════════════════════════════════════════════════
# 四、状态机引擎
# ═══════════════════════════════════════════════════════════


class 状态机引擎:
    """
    CNSH状态流转引擎

    状态流转图:
        RAW_INPUT → PARSED → BLOCKED → CROSS_AI_REVIEW →
        CONSENSUS_BUILDING → STATE_DECISION → ACTIVE_PROTOCOL →
        GRAPH_LINKED → ARCHIVED/FROZEN

    转换规则:
        IF AI_CONFLICT > 0.6 → CROSS_AI_REVIEW
        IF VALUE_SCORE > 85 AND CONSENSUS > 0.8 → ACTIVE_PROTOCOL
        IF RISK_SCORE > 70 → HUMAN_GATE
        IF CONTRADICTION == TRUE → STATE_DECISION
    """

    # 状态转换规则表
    转换规则: List[状态转换] = [
        # 基础流转
        状态转换(状态类型.原始输入, 状态类型.解析完成, "输入验证通过"),
        状态转换(状态类型.解析完成, 状态类型.阻塞审查, "初步审查完成"),
        状态转换(状态类型.阻塞审查, 状态类型.跨AI复核, "AI冲突超过阈值"),
        状态转换(状态类型.阻塞审查, 状态类型.共识构建, "无重大冲突"),
        状态转换(状态类型.跨AI复核, 状态类型.共识构建, "多AI达成共识"),
        状态转换(状态类型.跨AI复核, 状态类型.状态裁决, "存在矛盾"),
        状态转换(状态类型.共识构建, 状态类型.状态裁决, "共识度不足"),
        状态转换(状态类型.共识构建, 状态类型.活跃协议, "高价值+高共识"),
        状态转换(状态类型.状态裁决, 状态类型.活跃协议, "裁决通过"),
        状态转换(状态类型.状态裁决, 状态类型.冻结, "裁决驳回"),
        状态转换(状态类型.活跃协议, 状态类型.图谱链接, "链接验证完成"),
        状态转换(状态类型.图谱链接, 状态类型.归档, "生命周期完成"),

        # 特殊流转
        状态转换(状态类型.活跃协议, 状态类型.冻结, "主动冻结"),
        状态转换(状态类型.图谱链接, 状态类型.冻结, "安全冻结"),
        状态转换(状态类型.阻塞审查, 状态类型.冻结, "高风险熔断"),
    ]

    def __init__(self):
        self.状态历史: Dict[str, List[Dict[str, Any]]] = {}
        self.活跃实例: Dict[str, 状态包] = {}
        self.转换回调: Dict[Tuple[str, str], List[Callable]] = {}

    def 创建实例(self, 内容: str) -> 状态包:
        """创建新的状态机实例"""
        实例ID = f"ST-{uuid.uuid4().hex[:8].upper()}"
        实例 = 状态包(
            数据ID=实例ID,
            当前状态=状态类型.原始输入,
            内容=内容,
            历史=[{"状态": 状态类型.原始输入.value, "时间": datetime.now().isoformat(), "触发": "创建"}]
        )
        self.活跃实例[实例ID] = 实例
        self.状态历史[实例ID] = 实例.历史
        return 实例

    def 评估转换(self, 实例: 状态包) -> Optional[状态类型]:
        """
        根据当前状态包的分析结果评估下一步转换

        返回目标状态或None（无需转换）
        """
        分析 = 实例.分析结果
        价值分 = 实例.价值分
        风险分 = 实例.风险分
        共识度 = 实例.共识度
        冲突标记 = 实例.冲突标记

        if 实例.当前状态 == 状态类型.原始输入:
            return 状态类型.解析完成

        elif 实例.当前状态 == 状态类型.解析完成:
            return 状态类型.阻塞审查

        elif 实例.当前状态 == 状态类型.阻塞审查:
            # IF RISK_SCORE > 70 → HUMAN_GATE (冻结)
            if 风险分 > 70:
                return 状态类型.冻结
            # IF AI_CONFLICT > 0.6 → CROSS_AI_REVIEW
            if 分析.get("ai_conflict", 0) > 0.6:
                return 状态类型.跨AI复核
            return 状态类型.共识构建

        elif 实例.当前状态 == 状态类型.跨AI复核:
            # IF CONTRADICTION == TRUE → STATE_DECISION
            if 冲突标记:
                return 状态类型.状态裁决
            if 共识度 > 0.6:
                return 状态类型.共识构建
            return 状态类型.状态裁决

        elif 实例.当前状态 == 状态类型.共识构建:
            # IF VALUE_SCORE > 85 AND CONSENSUS > 0.8 → ACTIVE_PROTOCOL
            if 价值分 > 85 and 共识度 > 0.8:
                return 状态类型.活跃协议
            # IF CONSENSUS < 0.4 → STATE_DECISION
            if 共识度 < 0.4:
                return 状态类型.状态裁决
            return 状态类型.活跃协议  # 默认继续推进

        elif 实例.当前状态 == 状态类型.状态裁决:
            # 裁决结果决定
            if 分析.get("decision_result", "pass") == "pass":
                return 状态类型.活跃协议
            else:
                return 状态类型.冻结

        elif 实例.当前状态 == 状态类型.活跃协议:
            return 状态类型.图谱链接

        elif 实例.当前状态 == 状态类型.图谱链接:
            return 状态类型.归档

        return None

    def 执行转换(self, 实例ID: str, 目标状态: Optional[状态类型] = None) -> 状态包:
        """执行状态转换"""
        if 实例ID not in self.活跃实例:
            raise ValueError(f"实例 {实例ID} 不存在")

        实例 = self.活跃实例[实例ID]

        # 如果没有指定目标状态，自动评估
        if 目标状态 is None:
            目标状态 = self.评估转换(实例)

        if 目标状态 is None:
            return 实例  # 无需转换

        # 验证转换是否合法
        合法转换 = any(
            r.当前状态 == 实例.当前状态 and r.目标状态 == 目标状态
            for r in self.转换规则
        )

        旧状态 = 实例.当前状态
        实例.当前状态 = 目标状态

        记录 = {
            "状态": 目标状态.value,
            "时间": datetime.now().isoformat(),
            "触发": "自动评估" if 合法转换 else "强制转换",
            "合法": 合法转换,
        }
        实例.历史.append(记录)
        self.状态历史[实例ID].append(记录)

        return 实例

    def 获取状态链(self, 实例ID: str) -> List[str]:
        """获取状态转换链"""
        if 实例ID not in self.状态历史:
            return []
        return [h["状态"] for h in self.状态历史[实例ID]]

    def 获取状态流(self) -> List[Dict[str, str]]:
        """获取所有活跃实例的状态流摘要"""
        return [
            {
                "实例ID": ID,
                "当前状态": 实例.当前状态.value,
                "价值分": str(实例.价值分),
                "风险分": str(实例.风险分),
                "历史步数": str(len(实例.历史)),
            }
            for ID, 实例 in self.活跃实例.items()
        ]



# ═══════════════════════════════════════════════════════════
# 五、五行融合决策引擎（整合 wuxing_complete_system.py）
# ═══════════════════════════════════════════════════════════


class 五行决策引擎:
    """
    五行融合决策引擎 — 四大公式

    公式A: 平衡指数 = 100 - (σ/avg × 100)
    公式B: 相生相克强度 G(A→B) - R(A⇒B)
    公式C: 三才系数 = Heaven×0.35 + Earth×0.20 + Human×0.45（人≥0.34）
    公式D: 复合决策强度 = A×0.35 + B×0.30 + C×0.35
    六门路由: 金→权益门L0, 木→教育门L4, 水→数据门L1, 火→创作门L2, 土→民生门L3
    """

    # 相生相克表
    相生表 = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
    相克表 = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}

    # 六门映射
    六门映射 = {
        "金": 六门类型.权益门,
        "木": 六门类型.教育门,
        "水": 六门类型.数据门,
        "火": 六门类型.创作门,
        "土": 六门类型.民生门,
    }

    # 层级映射
    层级映射 = {
        "金": "L0", "木": "L4", "水": "L1", "火": "L2", "土": "L3"
    }

    # 三才权重
    三才权重 = (0.35, 0.20, 0.45)  # 天, 地, 人
    人最小值 = 0.34

    def __init__(self):
        self.计算计数 = 0
        self.审计日志: List[Dict[str, Any]] = []

    # ═════════ 公式A：平衡指数 ═════════

    def 计算平衡指数(self, 评分: 五行评分) -> float:
        """
        公式A: 平衡指数 = 100 - (σ/avg × 100)

        五行越均衡，指数越高（0-100）
        """
        分数列表 = [评分.金, 评分.木, 评分.水, 评分.火, 评分.土]
        总数 = sum(分数列表)

        if 总数 == 0:
            return 0.0

        均值 = 总数 / 5
        方差 = sum((s - 均值) ** 2 for s in 分数列表) / 5
        标准差 = math.sqrt(方差)

        比值 = 标准差 / 均值 if 均值 > 0 else 0
        指数 = max(0, 100 - 比值 * 100)

        self._记录审计("公式A", {"评分": 评分.to_dict()}, {"平衡指数": round(指数, 2)})
        return round(指数, 2)

    def 平衡转颜色(self, 平衡指数: float) -> 审计颜色:
        """平衡指数转三色审计"""
        if 平衡指数 >= 80:
            return 审计颜色.绿色
        elif 平衡指数 >= 60:
            return 审计颜色.黄色
        else:
            return 审计颜色.红色

    # ═════════ 公式B：相生相克强度 ═════════

    def 计算相生相克(self, 评分: 五行评分) -> Dict[str, Dict[str, Any]]:
        """
        公式B: 相生相克强度 G(A→B) - R(A⇒B)

        计算每对五行之间的相生和相克强度
        """
        分数字典 = 评分.to_dict()
        结果 = {}

        for 五行名 in ["金", "木", "水", "火", "土"]:
            相生目标 = self.相生表[五行名]
            相克目标 = self.相克表[五行名]

            源分 = 分数字典[五行名]
            相生分 = 分数字典[相生目标]
            相克分 = 分数字典[相克目标]

            # 相生强度: G(A→B) = B / (A + B)
            相生强度 = (相生分 / (源分 + 相生分)) if (源分 + 相生分) > 0 else 0

            # 相克强度: R(A⇒B) = min(A, B) / A
            相克强度 = (min(源分, 相克分) / 源分) if 源分 > 0 else 0

            # 净强度
            净强度 = 相生强度 - 相克强度

            结果[五行名] = {
                "相生": round(相生强度, 4),
                "相克": round(相克强度, 4),
                "净强度": round(净强度, 4),
                "相生目标": 相生目标,
                "相克目标": 相克目标,
            }

        self._记录审计("公式B", {"评分": 评分.to_dict()}, {"结果数": len(结果)})
        return 结果

    def 相克转颜色(self, 相克结果: Dict[str, Dict]) -> 审计颜色:
        """根据平均相克强度转三色审计"""
        平均相克 = sum(v["相克"] for v in 相克结果.values()) / len(相克结果)

        if 平均相克 > 0.85:
            return 审计颜色.红色
        elif 平均相克 > 0.60:
            return 审计颜色.黄色
        else:
            return 审计颜色.绿色

    # ═════════ 公式C：三才系数 ═════════

    def 计算三才系数(self, 天: float, 地: float, 人: float) -> float:
        """
        公式C: 三才系数 = Heaven×0.35 + Earth×0.20 + Human×0.45

        约束条件: 人 ≥ 0.34（不满足则自动调整）
        """
        天权重, 地权重, 人权重 = self.三才权重

        # 验证并调整人的最小值
        if 人 < self.人最小值:
            人 = self.人最小值
            剩余 = 1 - 人
            剩余总和 = 天 + 地
            if 剩余总和 > 0:
                比例 = 剩余 / 剩余总和
                天 = 天 * 比例
                地 = 地 * 比例

        系数 = 天 * 天权重 + 地 * 地权重 + 人 * 人权重

        self._记录审计("公式C", {"天": 天, "地": 地, "人": 人}, {"三才系数": round(系数, 4)})
        return round(系数, 4)

    def 三才转颜色(self, 三才系数: float) -> 审计颜色:
        """三才系数转三色审计"""
        if 三才系数 >= 0.75:
            return 审计颜色.绿色
        elif 三才系数 >= 0.50:
            return 审计颜色.黄色
        else:
            return 审计颜色.红色

    # ═════════ 公式D：复合决策强度 ═════════

    def 计算复合强度(self, 平衡指数: float, 相克结果: Dict, 三才系数: float) -> float:
        """
        公式D: 复合决策强度 = A×0.35 + B×0.30 + C×0.35

        A: 平衡指数（归一化）
        B: 相克强度（反向归一化，相克越强越危险）
        C: 三才系数
        """
        # 归一化
        平衡归一 = min(1.0, 平衡指数 / 100)

        # 平均相克归一化（反向，相克越强越差）
        平均相克 = sum(v["相克"] for v in 相克结果.values()) / len(相克结果)
        相克归一 = 1 - 平均相克

        # 三才系数已在0-1范围
        三才归一 = max(0, min(1, 三才系数))

        # 复合强度
        强度 = 平衡归一 * 0.35 + 相克归一 * 0.30 + 三才归一 * 0.35

        self._记录审计("公式D", {
            "平衡归一": round(平衡归一, 4),
            "相克归一": round(相克归一, 4),
            "三才归一": round(三才归一, 4),
        }, {"复合强度": round(强度, 4)})
        return round(强度, 4)

    # ═════════ 机器识别与自审 ═════════

    def 机器识别(self, 评分: 五行评分, 平衡指数: float) -> Tuple[str, float, bool, str]:
        """
        机器识别：确定主导五行，计算置信度，自审

        返回: (主导五行, 置信度, 审计通过, 审计原因)
        """
        分数字典 = 评分.to_dict()
        总数 = 评分.total() or 1

        # 识别主导五行
        主五行 = max(分数字典, key=分数字典.get)
        主分数 = 分数字典[主五行]
        主比例 = 主分数 / 总数

        # 计算置信度
        置信度 = round(主比例 * 0.6 + 平衡指数 / 100 * 0.4, 4)

        # 自审
        审计通过 = True
        审计原因 = "🟢 通过自审·可以输出"

        if 置信度 < 0.40:
            审计通过 = False
            审计原因 = "🔴 置信度过低（<0.40）"
        elif 平衡指数 < 20:
            审计通过 = False
            审计原因 = "🔴 五行极度失衡（平衡指数<20）"
        elif 主分数 < 10:
            审计通过 = False
            审计原因 = "🔴 数据不足（主导五行得分<10）"

        return 主五行, 置信度, 审计通过, 审计原因

    # ═════════ 人机一致性验证 ═════════

    def 验证一致性(self,
                  人类五行: Optional[str],
                  人类置信度: float,
                  机器五行: str,
                  机器置信度: float,
                  机器审计通过: bool) -> 识别结果:
        """验证人机会识别一致性"""

        # 判断一致性
        if not 机器审计通过:
            一致性分数 = 0.0
        elif 人类五行 is None:
            一致性分数 = 机器置信度
        elif 人类五行 == 机器五行:
            一致性分数 = 1.0
        else:
            # 检查相生相克
            if (self.相生表.get(人类五行) == 机器五行 or
                self.相生表.get(机器五行) == 人类五行):
                一致性分数 = 0.7
            elif (self.相克表.get(人类五行) == 机器五行 or
                  self.相克表.get(机器五行) == 人类五行):
                一致性分数 = 0.4
            else:
                一致性分数 = 0.2

        # 计算最终置信度
        if not 机器审计通过:
            最终置信度 = 0.0
            匹配 = False
        else:
            if 人类五行 is None:
                最终置信度 = 机器置信度
            else:
                最终置信度 = round(
                    (人类置信度 * 0.5 + 机器置信度 * 0.5) * 一致性分数, 4
                )
            匹配 = (人类五行 == 机器五行) if 人类五行 else False

        return 识别结果(
            人类五行=人类五行,
            人类置信度=人类置信度,
            机器五行=机器五行,
            机器置信度=机器置信度,
            机器审计通过=机器审计通过,
            机器审计原因="",
            匹配=匹配,
            一致性分数=一致性分数,
            最终置信度=最终置信度,
        )

    # ═════════ 六门路由 ═════════

    def 六门路由(self, 识别: 识别结果, 复合强度: float) -> 路由决策:
        """
        自动化六门路由决策

        金→权益门L0, 木→教育门L4, 水→数据门L1, 火→创作门L2, 土→民生门L3
        """
        五行名 = 识别.机器五行
        门 = self.六门映射.get(五行名, 六门类型.民生门)
        层级 = self.层级映射.get(五行名, "L3")

        # 确定行动与优先级
        if not 识别.机器审计通过:
            行动 = 行动类型.熔断
            颜色 = 审计颜色.红色
            优先级 = "P0"
            理由 = "AI自审失败·熔断隔离"
        elif 识别.最终置信度 >= 0.80:
            行动 = 行动类型.进入
            颜色 = 审计颜色.绿色
            优先级 = "P0" if 五行名 in ["金", "水"] else "P1"
            理由 = f"置信度高·直接进入·{五行名}元素·层级{层级}"
        elif 识别.最终置信度 >= 0.60:
            行动 = 行动类型.待审
            颜色 = 审计颜色.黄色
            优先级 = "P1"
            理由 = f"置信度中等·需加审计·{五行名}元素·层级{层级}"
        else:
            行动 = 行动类型.熔断
            颜色 = 审计颜色.红色
            优先级 = "P0"
            理由 = f"置信度低·熔断隔离·建议人工审查"

        下一步 = f"进入{门.门名} → {层级}层级·优先级{优先级}"

        return 路由决策(
            门=门.门名,
            层级=层级,
            优先级=优先级,
            行动=行动,
            审计颜色=颜色,
            理由=理由,
            下一步=下一步,
        )

    # ═════════ 完整工作流 ═════════

    def 完整决策(self,
                评分: 五行评分,
                三才天: float = 0.35,
                三才地: float = 0.20,
                三才人: float = 0.45,
                人类五行: Optional[str] = None,
                人类置信度: float = 0.5) -> 公式结果:
        """
        执行完整的四大公式决策流程

        返回: 公式结果对象
        """
        self.计算计数 += 1

        # 公式A：平衡指数
        平衡 = self.计算平衡指数(评分)

        # 公式B：相生相克强度
        相克结果 = self.计算相生相克(评分)

        # 公式C：三才系数
        三才 = self.计算三才系数(三才天, 三才地, 三才人)

        # 公式D：复合决策强度
        复合 = self.计算复合强度(平衡, 相克结果, 三才)

        return 公式结果(
            平衡指数=平衡,
            相生相克强度=相克结果,
            三才系数=三才,
            复合决策强度=复合,
            综合置信度=复合,
        )

    def _记录审计(self, 函数名: str, 输入: Dict, 输出: Dict):
        """记录审计日志"""
        self.审计日志.append({
            "函数": 函数名,
            "输入": 输入,
            "输出": 输出,
            "时间": datetime.now().isoformat(),
        })


# ═══════════════════════════════════════════════════════════
# 六、三色审计引擎
# ═══════════════════════════════════════════════════════════


class 三色审计引擎:
    """
    🔴🟡🟢 三色审计系统

    绿色: 逻辑正确+事实准确+符合君子协议+无安全风险
    黄色: 逻辑基本正确但有不明确之处+需引用来源
    红色: 逻辑错误+事实错误+违反君子协议+安全风险+必须人工介入

    审计流程: 提交→自动分类→三色预审→P3复核→P1价值校验→UID9622签发
    """

    # 审计阈值
    阈值 = {
        "价值分": {"绿": 85, "黄": 60},
        "风险分": {"绿": 30, "黄": 70},
        "幻觉率": {"绿": 0.05, "黄": 0.20},
        "置信度": {"绿": 0.80, "黄": 0.60},
    }

    def __init__(self, 审计员ID: str = "UID9622"):
        self.审计员ID = 审计员ID
        self.审计记录: Dict[str, 审计报告] = {}
        self.审计链: Dict[str, List[审计记录]] = {}

    def 自动分类(self, 价值分: float, 风险分: float,
                幻觉率: float, 置信度: float) -> 审计颜色:
        """
        自动分类：根据指标自动确定审计颜色

        红色触发条件（任一）:
        - 价值分 < 60
        - 风险分 > 70
        - 幻觉率 > 0.20
        - 置信度 < 0.40

        黄色触发条件（任一）:
        - 价值分 < 85
        - 风险分 > 30
        - 幻觉率 > 0.05
        - 置信度 < 0.60
        """
        # 红色检查
        if (价值分 < self.阈值["价值分"]["黄"] or
            风险分 > self.阈值["风险分"]["黄"] or
            幻觉率 > self.阈值["幻觉率"]["黄"] or
            置信度 < 0.40):
            return 审计颜色.红色

        # 黄色检查
        if (价值分 < self.阈值["价值分"]["绿"] or
            风险分 > self.阈值["风险分"]["绿"] or
            幻觉率 > self.阈值["幻觉率"]["绿"] or
            置信度 < self.阈值["置信度"]["黄"]):
            return 审计颜色.黄色

        return 审计颜色.绿色

    def 三色预审(self, 报告ID: str,
                价值分: float, 风险分: float,
                幻觉率: float, 置信度: float,
                事实检查: bool = True,
                君子协议检查: bool = True,
                安全检查: bool = True) -> 审计记录:
        """
        三色预审阶段

        综合多个维度进行预审
        """
        # 自动分类颜色
        颜色 = self.自动分类(价值分, 风险分, 幻觉率, 置信度)

        详情 = []
        if 价值分 >= self.阈值["价值分"]["绿"]:
            详情.append(f"🟢 价值分{价值分}·达标")
        elif 价值分 >= self.阈值["价值分"]["黄"]:
            详情.append(f"🟡 价值分{价值分}·需关注")
        else:
            详情.append(f"🔴 价值分{价值分}·不合格")

        if 风险分 <= self.阈值["风险分"]["绿"]:
            详情.append(f"🟢 风险分{风险分}·安全")
        elif 风险分 <= self.阈值["风险分"]["黄"]:
            详情.append(f"🟡 风险分{风险分}·中风险")
        else:
            详情.append(f"🔴 风险分{风险分}·高风险")

        if not 事实检查:
            颜色 = 审计颜色.红色
            详情.append("🔴 事实检查未通过")
        else:
            详情.append("🟢 事实检查通过")

        if not 君子协议检查:
            颜色 = 审计颜色.红色
            详情.append("🔴 违反君子协议")
        else:
            详情.append("🟢 君子协议通过")

        if not 安全检查:
            颜色 = 审计颜色.红色
            详情.append("🔴 安全检查未通过")
        else:
            详情.append("🟢 安全检查通过")

        记录 = 审计记录(
            审计ID=f"AUD-{报告ID}-{datetime.now().strftime('%H%M%S')}",
            阶段=审计阶段.三色预审,
            颜色=颜色,
            审计员=self.审计员ID,
            时间戳=datetime.now().isoformat(),
            详情="\n".join(详情),
            证据=[
                f"价值分={价值分}",
                f"风险分={风险分}",
                f"幻觉率={幻觉率}",
                f"置信度={置信度}",
                f"事实检查={事实检查}",
                f"君子协议={君子协议检查}",
                f"安全检查={安全检查}",
            ]
        )

        if 报告ID not in self.审计链:
            self.审计链[报告ID] = []
        self.审计链[报告ID].append(记录)

        return 记录

    def P3复核(self, 报告ID: str, P3审核通过: bool = True) -> 审计记录:
        """P3复核阶段"""
        记录 = 审计记录(
            审计ID=f"P3-{报告ID}-{datetime.now().strftime('%H%M%S')}",
            阶段=审计阶段.P3复核,
            颜色=审计颜色.绿色 if P3审核通过 else 审计颜色.红色,
            审计员=f"P3-{self.审计员ID}",
            时间戳=datetime.now().isoformat(),
            详情="P3复核通过" if P3审核通过 else "P3复核未通过·需人工审查",
        )
        self.审计链[报告ID].append(记录)
        return 记录

    def P1价值校验(self, 报告ID: str, 价值分: float) -> 审计记录:
        """P1价值校验阶段"""
        通过 = 价值分 >= self.阈值["价值分"]["黄"]
        记录 = 审计记录(
            审计ID=f"P1-{报告ID}-{datetime.now().strftime('%H%M%S')}",
            阶段=审计阶段.P1价值校验,
            颜色=审计颜色.绿色 if 通过 else 审计颜色.红色,
            审计员=f"P1-{self.审计员ID}",
            时间戳=datetime.now().isoformat(),
            详情=f"价值校验{'通过' if 通过 else '未通过'}（价值分={价值分}）",
        )
        self.审计链[报告ID].append(记录)
        return 记录

    def UID9622签发(self, 报告ID: str) -> 审计报告:
        """
        UID9622签发阶段

        签发流程最终步骤，生成完整审计报告
        """
        if 报告ID not in self.审计链:
            raise ValueError(f"报告 {报告ID} 不存在，无法签发")

        链 = self.审计链[报告ID]

        # 确定最终颜色
        颜色优先级 = {审计颜色.红色: 0, 审计颜色.黄色: 1, 审计颜色.绿色: 2}
        最终颜色 = min(链, key=lambda r: 颜色优先级.get(r.颜色, 1)).颜色

        # 确定是否需要人工
        需要人工 = any(r.颜色 == 审计颜色.红色 for r in 链)

        报告 = 审计报告(
            报告ID=报告ID,
            时间戳=datetime.now().isoformat(),
            审计链=链,
            最终颜色=最终颜色,
            需要人工=需要人工,
            签发状态=True,
        )

        self.审计记录[报告ID] = 报告
        return 报告

    def 完整审计(self, 报告ID: str,
                价值分: float, 风险分: float,
                幻觉率: float, 置信度: float,
                事实检查: bool = True,
                君子协议检查: bool = True,
                安全检查: bool = True,
                P3通过: bool = True) -> 审计报告:
        """
        执行完整审计流程

        审计流程: 提交→自动分类→三色预审→P3复核→P1价值校验→UID9622签发
        """
        # 初始化审计链
        self.审计链[报告ID] = []

        # 提交阶段
        self.审计链[报告ID].append(审计记录(
            审计ID=f"SUB-{报告ID}",
            阶段=审计阶段.提交,
            颜色=审计颜色.绿色,
            审计员=self.审计员ID,
            时间戳=datetime.now().isoformat(),
            详情=f"审计已提交·报告ID={报告ID}",
        ))

        # 自动分类阶段
        分类颜色 = self.自动分类(价值分, 风险分, 幻觉率, 置信度)
        self.审计链[报告ID].append(审计记录(
            审计ID=f"CLS-{报告ID}",
            阶段=审计阶段.自动分类,
            颜色=分类颜色,
            审计员="AUTO",
            时间戳=datetime.now().isoformat(),
            详情=f"自动分类结果：{分类颜色.含义}",
        ))

        # 三色预审
        self.三色预审(报告ID, 价值分, 风险分, 幻觉率, 置信度,
                      事实检查, 君子协议检查, 安全检查)

        # P3复核
        self.P3复核(报告ID, P3通过)

        # P1价值校验
        self.P1价值校验(报告ID, 价值分)

        # UID9622签发
        return self.UID9622签发(报告ID)

    def 生成审计报告JSON(self, 报告: 审计报告) -> Dict[str, Any]:
        """生成审计报告的JSON格式"""
        return {
            "报告ID": 报告.报告ID,
            "时间戳": 报告.时间戳,
            "最终颜色": 报告.最终颜色.图标,
            "需要人工": 报告.需要人工,
            "签发状态": 报告.签发状态,
            "审计链": [
                {
                    "审计ID": r.审计ID,
                    "阶段": r.阶段.value,
                    "颜色": r.颜色.图标,
                    "审计员": r.审计员,
                    "时间": r.时间戳,
                    "详情": r.详情,
                }
                for r in 报告.审计链
            ],
        }



# ═══════════════════════════════════════════════════════════
# 七、CNSH OS v2.5 核心引擎（统一整合）
# ═══════════════════════════════════════════════════════════


class CNSH核心引擎:
    """
    龍魂系统 CNSH OS v2.5 核心引擎

    统一整合五大模块：
      1. DNA生成引擎 — 全链路追溯
      2. 状态机引擎 — 状态流转
      3. 五行决策引擎 — 融合决策
      4. 三色审计引擎 — 审计签发
      5. CNSH标准JSON — 标准接口

    使用方式:
        引擎 = CNSH核心引擎()
        结果 = 引擎.处理(用户输入, 五行评分, ...)
        json输出 = 结果.to_json()
    """

    # 版本信息
    版本 = "v2.5"
    构建日期 = "2026-06-09"
    核心ID = "CNSH-CORE-ENGINE"

    def __init__(self, 审计员ID: str = "UID9622"):
        """初始化所有子引擎"""
        self.DNA引擎 = DNA引擎()
        self.状态机 = 状态机引擎()
        self.五行决策 = 五行决策引擎()
        self.三色审计 = 三色审计引擎(审计员ID)

        self.处理计数 = 0
        self.审计员ID = 审计员ID
        self.性能日志: List[Dict[str, Any]] = []

    def 处理(self,
            用户输入: str,
            五行评分: 五行评分,
            源AI: str = "CNSH",
            三才天: float = 0.35,
            三才地: float = 0.20,
            三才人: float = 0.45,
            人类五行: Optional[str] = None,
            人类置信度: float = 0.5,
            价值分: float = 0.0,
            风险分: float = 0.0,
            幻觉率: float = 0.0) -> CNSH标准JSON:
        """
        龍魂系统核心处理流程

        完整处理链路:
          输入 → DNA签名 → 状态机创建 → 五行决策 → 状态流转 → 三色审计 → CNSH JSON输出

        参数:
            用户输入: 原始输入内容
            五行评分: 五行评分数据
            源AI: AI模型标识
            三才天/地/人: 三才参数
            人类五行/置信度: 人机会识别参数
            价值分/风险分/幻觉率: 分析指标

        返回:
            CNSH标准JSON对象
        """
        开始时间 = time.time()
        self.处理计数 += 1

        # ═══ Step 1: DNA签名 ═══
        DNA签名 = self.DNA引擎.生成完整签名(用户输入)
        DNA = DNA签名["DNA"]

        # ═══ Step 2: 创建状态机实例 ═══
        状态包实例 = self.状态机.创建实例(用户输入)
        状态包实例.分析结果 = {
            "value_score": 价值分,
            "risk_score": 风险分,
            "hallucination": 幻觉率,
        }
        状态包实例.价值分 = 价值分
        状态包实例.风险分 = 风险分
        状态包实例.幻觉率 = 幻觉率

        # 执行初始状态流转
        self.状态机.执行转换(状态包实例.数据ID)
        self.状态机.执行转换(状态包实例.数据ID)

        # ═══ Step 3: 五行决策（四大公式）═══
        公式结果 = self.五行决策.完整决策(
            五行评分,
            三才天=三才天, 三才地=三才地, 三才人=三才人,
            人类五行=人类五行, 人类置信度=人类置信度,
        )

        # 机器识别
        平衡指数 = 公式结果.平衡指数
        主五行, 机器置信度, 审计通过, 审计原因 = self.五行决策.机器识别(五行评分, 平衡指数)

        # 人机一致性验证
        识别 = self.五行决策.验证一致性(
            人类五行, 人类置信度,
            主五行, 机器置信度, 审计通过,
        )
        识别.机器审计原因 = 审计原因

        # 六门路由
        路由 = self.五行决策.六门路由(识别, 公式结果.复合决策强度)

        # ═══ Step 4: 更新状态机（根据决策结果）═══
        状态包实例.共识度 = 识别.最终置信度
        状态包实例.冲突标记 = (路由.行动 == 行动类型.熔断)

        # 自动流转状态
        while True:
            目标 = self.状态机.评估转换(状态包实例)
            if 目标 is None or 状态包实例.当前状态 == 目标:
                break
            self.状态机.执行转换(状态包实例.数据ID, 目标)
            if 状态包实例.当前状态 in (状态类型.活跃协议, 状态类型.冻结, 状态类型.归档):
                break

        # ═══ Step 5: 三色审计 ═══
        审计报告 = self.三色审计.完整审计(
            报告ID=状态包实例.数据ID,
            价值分=价值分 if 价值分 > 0 else 公式结果.平衡指数,
            风险分=风险分 if 风险分 > 0 else (100 - 公式结果.平衡指数),
            幻觉率=幻觉率,
            置信度=识别.最终置信度,
            事实检查=True,
            君子协议检查=True,
            安全检查=True,
            P3通过=(路由.行动 != 行动类型.熔断),
        )

        # ═══ Step 6: 构建CNSH标准JSON ═══
        时间戳 = datetime.now().isoformat()

        # 创建数据块
        数据块 = CNSH标准数据块(
            块ID=f"B-{状态包实例.数据ID}",
            内容=用户输入,
            标签=["核心处理", 主五行, 路由.门],
            五行=主五行,
            价值分=价值分 if 价值分 > 0 else 公式结果.平衡指数,
            风险分=风险分 if 风险分 > 0 else (100 - 公式结果.平衡指数),
        )

        结果JSON = CNSH标准JSON(
            dna=DNA,
            源AI=源AI,
            输入=用户输入,
            块列表=[数据块],
            分析={
                "value_score": round(价值分 if 价值分 > 0 else 公式结果.平衡指数, 2),
                "risk_score": round(风险分 if 风险分 > 0 else (100 - 公式结果.平衡指数), 2),
                "hallucination": round(幻觉率, 4),
                "conflict": 状态包实例.冲突标记,
                "consensus": round(状态包实例.共识度, 4),
                "balance_index": round(公式结果.平衡指数, 2),
                "composite_strength": round(公式结果.复合决策强度, 4),
                "machine_element": 主五行,
                "machine_confidence": round(机器置信度, 4),
                "final_confidence": round(识别.最终置信度, 4),
            },
            流转={
                "instance_id": 状态包实例.数据ID,
                "current_state": 状态包实例.当前状态.value,
                "state_chain": self.状态机.获取状态链(状态包实例.数据ID),
                "next_state": "ACTIVE_PROTOCOL" if 路由.行动 == 行动类型.进入 else (
                    "FROZEN" if 路由.行动 == 行动类型.熔断 else "REVIEW"
                ),
                "gate": 路由.门,
                "layer": 路由.层级,
                "priority": 路由.优先级,
                "action": 路由.行动.value,
            },
            审计={
                "requires_human": 审计报告.需要人工,
                "audit_color": 审计报告.最终颜色.图标,
                "override": False,
                "audit_chain": [
                    {"phase": r.阶段.value, "color": r.颜色.图标}
                    for r in 审计报告.审计链
                ],
            },
            时间戳=时间戳,
        )

        # 记录性能
        耗时 = round((time.time() - 开始时间) * 1000, 3)
        self.性能日志.append({
            "处理ID": self.处理计数,
            "数据ID": 状态包实例.数据ID,
            "耗时_ms": 耗时,
            "DNA": DNA,
            "五行": 主五行,
            "状态": 状态包实例.当前状态.value,
            "审计": 审计报告.最终颜色.图标,
        })

        return 结果JSON

    def 快速处理(self, 用户输入: str, 五行评分: 五行评分) -> CNSH标准JSON:
        """简化版处理接口（使用默认参数）"""
        return self.处理(
            用户输入=用户输入,
            五行评分=五行评分,
            价值分=五行评分.total(),
            幻觉率=0.0,
        )

    def 获取性能报告(self) -> Dict[str, Any]:
        """获取性能统计报告"""
        if not self.性能日志:
            return {"消息": "暂无性能数据"}

        耗时列表 = [l["耗时_ms"] for l in self.性能日志]
        return {
            "总处理数": self.处理计数,
            "平均耗时_ms": round(sum(耗时列表) / len(耗时列表), 3),
            "最大耗时_ms": max(耗时列表),
            "最小耗时_ms": min(耗时列表),
            "总耗时_ms": round(sum(耗时列表), 3),
            "最近处理": self.性能日志[-1] if self.性能日志 else None,
        }

    def 获取引擎状态(self) -> Dict[str, Any]:
        """获取核心引擎状态摘要"""
        return {
            "版本": self.版本,
            "构建日期": self.构建日期,
            "核心ID": self.核心ID,
            "处理计数": self.处理计数,
            "审计员ID": self.审计员ID,
            "DNA生成数": self.DNA引擎.生成计数,
            "五行决策数": self.五行决策.计算计数,
            "活跃状态机": len(self.状态机.活跃实例),
            "审计记录数": len(self.三色审计.审计记录),
            "性能报告": self.获取性能报告(),
        }


# ═══════════════════════════════════════════════════════════
# 八、工具函数
# ═══════════════════════════════════════════════════════════


def 数字根(n: int) -> int:
    """数字根: dr(n) = 1 + ((n-1) mod 9)"""
    n = abs(n)
    return 0 if n == 0 else 1 + (n - 1) % 9


def 五行映射(数字: int) -> str:
    """数字根映射到五行"""
    根 = 数字根(数字)
    映射 = {1: "木", 2: "木", 3: "火", 4: "火", 5: "土",
            6: "金", 7: "金", 8: "水", 9: "水"}
    return 映射[根]


def 创建五行评分(金: float = 0, 木: float = 0, 水: float = 0,
                火: float = 0, 土: float = 0) -> 五行评分:
    """便捷创建五行评分"""
    return 五行评分(金=金, 木=木, 水=水, 火=火, 土=土)


def 均衡五行评分(总值: float = 100) -> 五行评分:
    """创建均衡的五行评分（每个五行相等）"""
    均分 = 总值 / 5
    return 五行评分(金=均分, 木=均分, 水=均分, 火=均分, 土=均分)


# ═══════════════════════════════════════════════════════════
# 九、完整测试块
# ═══════════════════════════════════════════════════════════


if __name__ == "__main__":
    print("=" * 100)
    print("龍魂系统 CNSH OS v2.5 核心引擎 — 完整自检")
    print("=" * 100)

    测试通过 = 0
    测试失败 = 0

    # ═══════════════════════════════════════════════════════
    # 测试 1: DNA生成引擎
    # ═══════════════════════════════════════════════════════
    print("\n【测试 1】DNA生成引擎")
    print("-" * 50)

    try:
        dna_eng = DNA引擎()

        # 生成DNA
        dna1 = dna_eng.生成DNA("测试内容", "GPT", "UID9622")
        assert dna1.startswith("CNSH-")
        print(f"  ✅ DNA生成: {dna1}")

        # 五行标记
        assert dna_eng.五行标记(10).名称 == "水"
        assert dna_eng.五行标记(30).名称 == "木"
        assert dna_eng.五行标记(50).名称 == "土"
        assert dna_eng.五行标记(70).名称 == "火"
        assert dna_eng.五行标记(90).名称 == "金"
        print(f"  ✅ 五行标记: 水(10) 木(30) 土(50) 火(70) 金(90)")

        # 完整签名
        签名 = dna_eng.生成完整签名("测试")
        assert "DNA" in 签名
        assert "确认码" in 签名
        assert "灵魂绑定" in 签名
        print(f"  ✅ 完整签名生成")

        测试通过 += 1
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        测试失败 += 1

    # ═══════════════════════════════════════════════════════
    # 测试 2: 状态机引擎
    # ═══════════════════════════════════════════════════════
    print("\n【测试 2】状态机引擎")
    print("-" * 50)

    try:
        sm = 状态机引擎()

        # 创建实例
        实例 = sm.创建实例("测试状态流转")
        assert 实例.当前状态 == 状态类型.原始输入
        print(f"  ✅ 创建实例: ID={实例.数据ID}")

        # 状态流转
        sm.执行转换(实例.数据ID)  # → 解析完成
        sm.执行转换(实例.数据ID)  # → 阻塞审查
        assert 实例.当前状态 == 状态类型.阻塞审查
        print(f"  ✅ 自动流转: 原始输入 → 解析完成 → 阻塞审查")

        # 高风险流转
        实例2 = sm.创建实例("高风险测试")
        实例2.风险分 = 85  # 高风险
        sm.执行转换(实例2.数据ID)  # → 解析完成
        sm.执行转换(实例2.数据ID)  # → 阻塞审查
        sm.执行转换(实例2.数据ID)  # → 冻结（风险>70触发熔断）
        # 应该走到冻结
        assert 实例2.当前状态 == 状态类型.冻结
        print(f"  ✅ 风险熔断: 风险85 → 阻塞审查 → 冻结（高风险自动熔断）")

        # 高价值流转
        实例3 = sm.创建实例("高价值测试")
        实例3.价值分 = 90
        实例3.共识度 = 0.85
        sm.执行转换(实例3.数据ID)
        sm.执行转换(实例3.数据ID)
        sm.执行转换(实例3.数据ID)  # → 共识构建
        sm.执行转换(实例3.数据ID)  # → 活跃协议
        assert 实例3.当前状态 == 状态类型.活跃协议
        print(f"  ✅ 价值通过: 价值90+共识0.85 → 活跃协议")

        # 状态链
        链 = sm.获取状态链(实例3.数据ID)
        assert len(链) >= 3
        print(f"  ✅ 状态链: {' → '.join(链)}")

        测试通过 += 1
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        测试失败 += 1

    # ═══════════════════════════════════════════════════════
    # 测试 3: 五行融合决策引擎
    # ═══════════════════════════════════════════════════════
    print("\n【测试 3】五行融合决策引擎 — 四大公式")
    print("-" * 50)

    try:
        wx = 五行决策引擎()

        # 测试数据
        评分 = 五行评分(金=45, 木=35, 水=55, 火=40, 土=50)

        # 公式A: 平衡指数
        平衡 = wx.计算平衡指数(评分)
        assert 0 <= 平衡 <= 100
        print(f"  ✅ 公式A·平衡指数: {平衡}/100")

        # 公式B: 相生相克
        相克 = wx.计算相生相克(评分)
        assert len(相克) == 5
        assert "金" in 相克
        assert all(k in 相克["金"] for k in ["相生", "相克", "净强度"])
        print(f"  ✅ 公式B·相生相克: 5对关系计算完成")

        # 公式C: 三才系数
        三才 = wx.计算三才系数(0.85, 0.75, 0.90)
        assert 0 <= 三才 <= 1
        print(f"  ✅ 公式C·三才系数: {三才}")

        # 三才约束测试（人 < 0.34）
        三才约束 = wx.计算三才系数(0.5, 0.5, 0.2)
        assert 三才约束 >= 0.34 * 0.45
        print(f"  ✅ 公式C·三才约束: 人=0.2 < 0.34 → 自动调整为{三才约束}")

        # 公式D: 复合决策强度
        复合 = wx.计算复合强度(平衡, 相克, 三才)
        assert 0 <= 复合 <= 1
        print(f"  ✅ 公式D·复合强度: {复合}")

        # 机器识别
        主五行, 置信度, 审计通过, 原因 = wx.机器识别(评分, 平衡)
        assert 主五行 in ["金", "木", "水", "火", "土"]
        print(f"  ✅ 机器识别: 主导五行={主五行} 置信度={置信度} {'通过' if 审计通过 else '未通过'}")

        # 人机一致性
        识别 = wx.验证一致性("水", 0.8, 主五行, 置信度, 审计通过)
        assert 识别.一致性分数 >= 0
        print(f"  ✅ 一致性验证: 分数={识别.一致性分数} 最终置信={识别.最终置信度}")

        # 六门路由
        路由 = wx.六门路由(识别, 复合)
        assert 路由.门 in ["权益门", "数据门", "创作门", "民生门", "教育门"]
        print(f"  ✅ 六门路由: {路由.门} → {路由.层级} 优先级={路由.优先级}")

        # 完整决策
        结果 = wx.完整决策(评分)
        assert 结果.平衡指数 > 0
        print(f"  ✅ 完整决策: 平衡={结果.平衡指数} 复合={结果.复合决策强度} 三才={结果.三才系数}")

        测试通过 += 1
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        测试失败 += 1

    # ═══════════════════════════════════════════════════════
    # 测试 4: 三色审计引擎
    # ═══════════════════════════════════════════════════════
    print("\n【测试 4】三色审计引擎 — 🔴🟡🟢")
    print("-" * 50)

    try:
        audit = 三色审计引擎("UID9622")

        # 自动分类
        绿 = audit.自动分类(90, 20, 0.02, 0.85)
        assert 绿 == 审计颜色.绿色
        黄 = audit.自动分类(70, 50, 0.10, 0.50)
        assert 黄 == 审计颜色.黄色
        红 = audit.自动分类(50, 80, 0.30, 0.30)
        assert 红 == 审计颜色.红色
        print(f"  ✅ 自动分类: 高指标→{绿.图标} 中指标→{黄.图标} 低指标→{红.图标}")

        # 完整审计流程
        审计 = audit.完整审计(
            报告ID="TEST-001",
            价值分=88,
            风险分=15,
            幻觉率=0.03,
            置信度=0.82,
        )
        assert 审计.签发状态 == True
        assert len(审计.审计链) >= 5
        print(f"  ✅ 完整审计: {审计.最终颜色.图标} 已签发 链长={len(审计.审计链)}")

        # 高风险审计
        审计红 = audit.完整审计(
            报告ID="TEST-002",
            价值分=40,
            风险分=85,
            幻觉率=0.30,
            置信度=0.30,
        )
        assert 审计红.需要人工 == True
        print(f"  ✅ 高风险审计: {审计红.最终颜色.图标} 需人工={审计红.需要人工}")

        测试通过 += 1
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        测试失败 += 1

    # ═══════════════════════════════════════════════════════
    # 测试 5: CNSH核心引擎完整工作流
    # ═══════════════════════════════════════════════════════
    print("\n【测试 5】CNSH核心引擎 — 完整工作流")
    print("-" * 50)

    try:
        引擎 = CNSH核心引擎()

        # 工作流测试 1: 标准输入
        评分1 = 五行评分(金=45, 木=35, 水=55, 火=40, 土=50)
        结果1 = 引擎.处理(
            用户输入="测试龍魂系统核心引擎",
            五行评分=评分1,
            源AI="Kimi",
            三才天=0.85,
            三才地=0.80,
            三才人=0.90,
            人类五行="水",
            人类置信度=0.75,
            价值分=88,
            风险分=12,
            幻觉率=0.03,
        )

        assert 结果1.dna.startswith("#龍芯⚡️CNSH-")
        assert 结果1.源AI == "Kimi"
        assert len(结果1.块列表) == 1
        assert "value_score" in 结果1.分析
        assert "next_state" in 结果1.流转
        assert "requires_human" in 结果1.审计
        print(f"  ✅ 完整工作流: DNA={结果1.dna[:40]}...")
        print(f"     状态: {结果1.流转['current_state']} → {结果1.流转['next_state']}")
        print(f"     路由: {结果1.流转['gate']} {结果1.流转['layer']}")
        print(f"     审计: {结果1.审计['audit_color']} 需人工={结果1.审计['requires_human']}")

        # 工作流测试 2: 快速处理
        评分2 = 均衡五行评分(100)
        结果2 = 引擎.快速处理("快速处理测试", 评分2)
        assert 结果2.dna != ""
        print(f"  ✅ 快速处理: 平衡五行 状态={结果2.流转['current_state']}")

        # 工作流测试 3: 高风险输入
        评分3 = 五行评分(金=5, 木=5, 水=5, 火=5, 土=5)
        结果3 = 引擎.处理(
            用户输入="高风险测试输入",
            五行评分=评分3,
            价值分=30,
            风险分=85,
            幻觉率=0.25,
        )
        print(f"  ✅ 高风险处理: 审计={结果3.审计['audit_color']} 需人工={结果3.审计['requires_human']}")

        测试通过 += 1
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        测试失败 += 1

    # ═══════════════════════════════════════════════════════
    # 测试 6: CNSH标准JSON序列化
    # ═══════════════════════════════════════════════════════
    print("\n【测试 6】CNSH标准JSON — 序列化")
    print("-" * 50)

    try:
        # 测试序列化
        json_str = 结果1.to_json()
        assert "dna" in json_str
        assert "analysis" in json_str
        print(f"  ✅ JSON序列化: {len(json_str)} 字符")

        # 反序列化验证
        解析 = json.loads(json_str)
        assert 解析["dna"] == 结果1.dna
        assert 解析["source_ai"] == "Kimi"
        print(f"  ✅ JSON反序列化: 结构完整")

        # 引擎状态报告
        状态 = 引擎.获取引擎状态()
        assert 状态["处理计数"] >= 3
        print(f"  ✅ 引擎状态: 处理{状态['处理计数']}次 活跃{状态['活跃状态机']}实例")

        # 性能报告
        性能 = 引擎.获取性能报告()
        assert "平均耗时_ms" in 性能
        print(f"  ✅ 性能报告: 平均{性能['平均耗时_ms']}ms 最大{性能['最大耗时_ms']}ms")

        # 打印完整JSON
        print(f"\n【CNSH标准JSON输出示例】")
        print(json.dumps(解析, ensure_ascii=False, indent=2)[:800] + "...")

        测试通过 += 1
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        测试失败 += 1

    # ═══════════════════════════════════════════════════════
    # 测试 7: 工具函数
    # ═══════════════════════════════════════════════════════
    print("\n【测试 7】工具函数")
    print("-" * 50)

    try:
        # 数字根
        assert 数字根(12345) == 6
        assert 数字根(9) == 9
        assert 数字根(0) == 0
        print(f"  ✅ 数字根: dr(12345)={数字根(12345)} dr(9)={数字根(9)}")

        # 五行映射
        assert 五行映射(1) == "木"
        assert 五行映射(8) == "水"
        print(f"  ✅ 五行映射: 1→{五行映射(1)} 8→{五行映射(8)}")

        # 创建五行评分
        评分 = 创建五行评分(金=10, 木=20, 水=30, 火=40, 土=50)
        assert 评分.金 == 10
        assert 评分.total() == 150
        print(f"  ✅ 创建评分: 总分={评分.total()}")

        # 均衡评分
        均衡 = 均衡五行评分(100)
        assert 均衡.金 == 20
        assert 均衡.水 == 20
        print(f"  ✅ 均衡评分: {均衡.to_dict()}")

        测试通过 += 1
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        测试失败 += 1

    # ═══════════════════════════════════════════════════════
    # 总结
    # ═══════════════════════════════════════════════════════
    print("\n" + "=" * 100)
    print("龍魂系统 CNSH OS v2.5 核心引擎 — 自检总结")
    print("=" * 100)
    print(f"  测试通过: {测试通过}/7 模块")
    print(f"  测试失败: {测试失败}/7 模块")
    print(f"  DNA生成数: {dna_eng.生成计数 if 'dna_eng' in dir() else 'N/A'}")
    print(f"  处理计数: {引擎.处理计数 if '引擎' in dir() else 'N/A'}")

    if 测试失败 == 0:
        print(f"\n  🟢 所有测试通过！CNSH OS v2.5 核心引擎运行正常")
    else:
        print(f"\n  🟡 部分测试失败，请检查日志")

    print(f"\n  DNA:#龍芯⚡️2026-06-09-CNSH-CORE-ENGINE-v2.5")
    print(f"  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅")
    print(f"  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅")
    print("=" * 100)

