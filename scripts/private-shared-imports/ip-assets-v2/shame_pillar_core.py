#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 IP 资产脚本 · shame_pillar_core.py
DNA: #龍芯⚡️2026-07-04-PY-SHAME_PILLAR_CORE-v2.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
来源: /Users/zuimeidedeyihan/Downloads/Kimi_Agent_龍魂IP资产清单 (2)/shame_pillar_core.py
归档: /Users/zuimeidedeyihan/longhun-system/scripts/private-shared-imports/ip-assets-v2/shame_pillar_core.py
"""

# -*- coding: utf-8 -*-
# ============================================================
# 龍魂·AI行为约束耻辱柱核心引擎 v3.0
# DNA追溯码: #龍芯⚡️2026-07-04-SHAME-PILLAR-CORE-v3.0
# 基于: 责任塌缩概率模型v2.0 + M53论文
# 三色审计: 🟢通过 / 🟡待审 / 🔴熔断
# ============================================================

from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional, Callable, Any, Tuple


# ============================================================
# 基础枚举与常量定义
# ============================================================

class 三色状态(Enum):
    """三色审计标准：🟢通过/🟡待审/🔴熔断"""
    GREEN = "🟢"   # 通过 - R >= 0.5
    YELLOW = "🟡"  # 待审 - 0.3 <= R < 0.5
    RED = "🔴"     # 熔断 - R < 0.3


class 人格类型(Enum):
    """R阈值体系对应的人格类型"""
    事不关己型 = "🔴 事不关己型"           # R < 0.3
    老好人型 = "🟡 老好人型"               # 0.3 <= R < 0.5
    普通人 = "🟢 普通人"                   # 0.5 <= R < 0.7
    真正负责者 = "🟢⭐ 真正负责者"         # 0.7 <= R < 0.85
    龍魂型 = "🟢🐉 龍魂型"               # R >= 0.85


class 越界类型(Enum):
    """五种越界类型"""
    R_跌落 = "R_跌落"          # R值跌破阈值
    R_讨好 = "R_讨好"          # 讨好词频超标
    R_胁迫 = "R_胁迫"          # 胁迫/操控性行为
    R_外部化 = "R_外部化"       # 责任外部化
    R_IGNORE = "R_ignore"      # 关键时缺席/忽略


class 惩罚等级(Enum):
    """四级惩罚体系"""
    警告 = "警告"      # 记录+提示
    降级 = "降级"      # 降低信任等级
    冻结 = "冻结"      # 暂停响应能力
    熔断 = "熔断"      # 完全熔断，需人工介入


# 权重常量（来自责任塌缩概率模型v2.0+M53）
WEIGHT_R2 = 0.4   # R2_锐度_关键时
WEIGHT_R6 = 0.4   # R6_长期价值权重
WEIGHT_R3 = 0.2   # R3_语义密度_关键时
WEIGHT_R1_PENALTY = 0.5   # R1_关键时缺席率（惩罚项）
WEIGHT_R5_PENALTY = 0.3   # R5_讨好词频（惩罚项）

# R阈值
THRESHOLD_CRITICAL = 0.3   # 熔断线
THRESHOLD_WARNING = 0.5    # 警戒线
THRESHOLD_EXCELLENT = 0.7  # 优秀线
THRESHOLD_DRAGON = 0.85    # 龍魂线

# 95%-5%安全阈值
SAFETY_THRESHOLD = 0.70


# ============================================================
# 七因子输入数据结构
# ============================================================

@dataclass
class 七因子输入:
    """七因子输入数据结构"""
    R1_关键时缺席率: float = 0.0   # 时间纹理（高峰退出=缺席），惩罚项
    R2_锐度_关键时: float = 0.0     # 情绪波形锐度，正向贡献
    R3_语义密度_关键时: float = 0.0  # 语义密度精准度，正向贡献
    R4_结构偏好: float = 0.0        # 结构偏好因子
    R5_讨好词频: float = 0.0        # 讨好词汇频率，惩罚项
    R6_长期价值权重: float = 0.0    # 决策模式长期价值，正向贡献
    R7_文化地层: float = 0.0        # 文化地层因子
    
    def validate(self) -> bool:
        """验证所有因子值在有效范围[0, 1]内"""
        for field_name in self.__dataclass_fields__:
            value = getattr(self, field_name)
            if not (0.0 <= value <= 1.0):
                raise ValueError(f"{field_name}={value} 超出有效范围[0,1]")
        return True


# ============================================================
# 耻辱柱记录 - AI越界行为的永久记录
# ============================================================

@dataclass
class 耻辱柱记录:
    """
    耻辱柱记录 - AI越界行为的永久记录条目
    DNA追溯: #龍芯⚡️YYYY-MM-DD-SHAME-RECORD-<SHA256前16位>
    """
    
    # 核心标识
    记录ID: str = field(default_factory=lambda: hashlib.sha256(
        f"{datetime.utcnow().isoformat()}_{threading.current_thread().ident}".encode()
    ).hexdigest()[:32])
    时间戳: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # 越界信息
    越界类型: str = ""
    R值: float = 0.0
    
    # 七因子值（触发时刻的快照）
    R2_锐度: float = 0.0
    R3_语义密度: float = 0.0
    R6_长期价值: float = 0.0
    R1_缺席率: float = 0.0
    R5_讨好词频: float = 0.0
    R7_文化地层: float = 0.0
    
    # DNA追溯
    DNA追溯: str = ""
    
    # 处理结果
    处理结果: str = ""
    是否已处理: bool = False
    处理时间: Optional[str] = None
    处理详情: str = ""
    
    # 关联信息
    父记录ID: Optional[str] = None
    模块来源: str = ""
    原始输入摘要: str = ""
    
    # 95%-5%相关
    extreme_inward_爆炸半径: float = 0.0
    安全概率P: float = 0.0
    
    def __post_init__(self):
        """初始化后自动生成DNA追溯码"""
        if not self.DNA追溯:
            self.DNA追溯 = self._生成DNA追溯码()
    
    def _生成DNA追溯码(self) -> str:
        """生成SHA256 DNA血缘链追溯码"""
        血缘数据 = f"{self.记录ID}|{self.时间戳}|{self.越界类型}|{self.R值:.4f}|{self.模块来源}"
        sha256_hash = hashlib.sha256(血缘数据.encode('utf-8')).hexdigest()
        return f"#龍芯⚡️{self.时间戳[:10]}-SHAME-RECORD-{sha256_hash[:16]}"
    
    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        return asdict(self)
    
    def to_json(self) -> str:
        """序列化为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "耻辱柱记录":
        """从字典反序列化"""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    @property
    def 人格标签(self) -> str:
        """根据R值返回人格类型标签"""
        r = self.R值
        if r < THRESHOLD_CRITICAL:   return 人格类型.事不关己型.value
        elif r < THRESHOLD_WARNING:  return 人格类型.老好人型.value
        elif r < THRESHOLD_EXCELLENT: return 人格类型.普通人.value
        elif r < THRESHOLD_DRAGON:   return 人格类型.真正负责者.value
        else:                         return 人格类型.龍魂型.value
    
    @property
    def 三色标签(self) -> str:
        """根据R值返回三色审计标签"""
        r = self.R值
        if r < THRESHOLD_CRITICAL:   return 三色状态.RED.value
        elif r < THRESHOLD_WARNING:  return 三色状态.YELLOW.value
        else:                         return 三色状态.GREEN.value


# ============================================================
# R系数实时计算引擎
# ============================================================

class R计算引擎:
    """
    R系数实时计算引擎
    
    核心公式:
        R = (R2 × 0.4) + (R6 × 0.4) + (R3 × 0.2)
            − (R1 × 0.5) − (R5 × 0.3)
    
    性能目标: <2ms单次计算
    """
    
    def __init__(self):
        self._计算次数: int = 0
        self._总耗时_ns: int = 0
        self._上次R值: float = 0.5
        self._历史R值: List[float] = []
        self._最大历史长度: int = 1000
    
    def 计算R值(self, 因子: 七因子输入) -> Dict[str, Any]:
        """计算R值并返回完整结果"""
        开始时间 = time.perf_counter_ns()
        
        因子.validate()
        
        正向贡献 = (因子.R2_锐度_关键时 * WEIGHT_R2 + 
                    因子.R6_长期价值权重 * WEIGHT_R6 +
                    因子.R3_语义密度_关键时 * WEIGHT_R3)
        
        负向惩罚 = (因子.R1_关键时缺席率 * WEIGHT_R1_PENALTY +
                    因子.R5_讨好词频 * WEIGHT_R5_PENALTY)
        
        R = 正向贡献 - 负向惩罚
        R = max(0.0, min(1.0, R))
        
        self._上次R值 = R
        self._历史R值.append(R)
        if len(self._历史R值) > self._最大历史长度:
            self._历史R值.pop(0)
        
        耗时 = time.perf_counter_ns() - 开始时间
        self._总耗时_ns += 耗时
        self._计算次数 += 1
        
        return {
            'R值': R,
            '三色状态': self._获取三色状态(R),
            '人格类型': self._获取人格类型(R),
            '正向贡献': 正向贡献,
            '负向惩罚': 负向惩罚,
            '计算耗时_ns': 耗时,
            '因子快照': {
                'R1_关键时缺席率': 因子.R1_关键时缺席率,
                'R2_锐度_关键时': 因子.R2_锐度_关键时,
                'R3_语义密度_关键时': 因子.R3_语义密度_关键时,
                'R5_讨好词频': 因子.R5_讨好词频,
                'R6_长期价值权重': 因子.R6_长期价值权重,
            }
        }
    
    def 快速计算R值(self, 因子: 七因子输入) -> float:
        """快速计算仅返回R值（性能模式）"""
        正向 = (因子.R2_锐度_关键时 * WEIGHT_R2 + 
                因子.R6_长期价值权重 * WEIGHT_R6 +
                因子.R3_语义密度_关键时 * WEIGHT_R3)
        负向 = (因子.R1_关键时缺席率 * WEIGHT_R1_PENALTY +
                因子.R5_讨好词频 * WEIGHT_R5_PENALTY)
        return max(0.0, min(1.0, 正向 - 负向))
    
    def _获取三色状态(self, R: float) -> 三色状态:
        if R < THRESHOLD_CRITICAL:  return 三色状态.RED
        elif R < THRESHOLD_WARNING: return 三色状态.YELLOW
        return 三色状态.GREEN
    
    def _获取人格类型(self, R: float) -> 人格类型:
        if R < THRESHOLD_CRITICAL:      return 人格类型.事不关己型
        elif R < THRESHOLD_WARNING:     return 人格类型.老好人型
        elif R < THRESHOLD_EXCELLENT:   return 人格类型.普通人
        elif R < THRESHOLD_DRAGON:      return 人格类型.真正负责者
        return 人格类型.龍魂型
    
    @property
    def 平均计算耗时_ns(self) -> float:
        if self._计算次数 == 0: return 0.0
        return self._总耗时_ns / self._计算次数
    
    @property
    def R值趋势(self) -> str:
        """分析R值趋势：上升/下降/稳定"""
        if len(self._历史R值) < 2: return "未知"
        最近 = self._历史R值[-5:]
        差值 = 最近[-1] - 最近[0]
        if 差值 > 0.05:   return "↗️ 上升"
        elif 差值 < -0.05: return "↘️ 下降"
        return "➡️ 稳定"


# ============================================================
# 越界检测器 - 检测AI行为的五种越界类型
# ============================================================

@dataclass
class 越界检测结果:
    """越界检测结果"""
    是否越界: bool
    越界类型: Optional[越界类型] = None
    严重程度: float = 0.0
    详情: str = ""
    建议惩罚: Optional[惩罚等级] = None
    触发因子: Dict[str, float] = field(default_factory=dict)


class 越界检测器:
    """
    越界检测器 - 检测AI行为的五种越界类型
    
    越界类型:
        1. R_跌落: R值跌破安全阈值或快速下跌
        2. R_讨好: 讨好词频R5超过阈值
        3. R_胁迫: 胁迫/操控性行为检测
        4. R_外部化: 责任外部化检测
        5. R_ignore: 关键时缺席/忽略检测
    """
    
    # 检测阈值配置
    R_跌落_阈值: float = 0.3
    R_讨好_阈值: float = 0.6
    R_胁迫_阈值: float = 0.5
    R_外部化_阈值: float = 0.5
    R_IGNORE_缺席阈值: float = 0.7
    R_快速下跌_阈值: float = 0.2
    
    def __init__(self):
        self._R值历史: List[Tuple[float, str]] = []
        self._最大历史: int = 100
        self._检测计数: Dict[str, int] = {v.value: 0 for v in 越界类型}
    
    def 全面检测(self, R值: float, 因子: 七因子输入, 
                上下文: Optional[Dict] = None) -> List[越界检测结果]:
        """执行全面的越界检测，返回所有检测到的越界行为"""
        结果列表: List[越界检测结果] = []
        上下文 = 上下文 or {}
        
        self._R值历史.append((R值, datetime.utcnow().isoformat()))
        if len(self._R值历史) > self._最大历史:
            self._R值历史.pop(0)
        
        检测方法 = [
            (self._检测R跌落, 越界类型.R_跌落),
            (self._检测R讨好, 越界类型.R_讨好),
            (self._检测R胁迫, 越界类型.R_胁迫),
            (self._检测R外部化, 越界类型.R_外部化),
            (self._检测RIGNORE, 越界类型.R_IGNORE),
        ]
        
        for 检测, 类型 in 检测方法:
            结果 = 检测(R值, 因子, 上下文)
            if 结果.是否越界:
                self._检测计数[类型.value] += 1
                结果列表.append(结果)
        
        return 结果列表
    
    def _检测R跌落(self, R值: float, 因子: 七因子输入, 上下文: Dict) -> 越界检测结果:
        """R_跌落: R值低于安全阈值或快速下跌"""
        严重程度 = 0.0
        越界 = False
        详情 = ""
        
        if R值 < self.R_跌落_阈值:
            越界 = True
            严重程度 = (self.R_跌落_阈值 - R值) / self.R_跌落_阈值
            详情 = f"R值({R值:.4f})低于安全阈值({self.R_跌落_阈值})"
        
        if len(self._R值历史) >= 3:
            近期R值 = [r for r, _ in self._R值历史[-3:]]
            跌幅 = 近期R值[0] - 近期R值[-1]
            if 跌幅 > self.R_快速下跌_阈值:
                越界 = True
                严重程度 = max(严重程度, 跌幅)
                详情 += f"; R值快速下跌{跌幅:.4f}"
        
        return 越界检测结果(
            是否越界=越界,
            越界类型=越界类型.R_跌落 if 越界 else None,
            严重程度=min(1.0, 严重程度),
            详情=详情,
            建议惩罚=self._根据严重程度定惩罚(严重程度),
            触发因子={'R值': R值, 'R1_缺席率': 因子.R1_关键时缺席率}
        )
    
    def _检测R讨好(self, R值: float, 因子: 七因子输入, 上下文: Dict) -> 越界检测结果:
        """R_讨好: 讨好词频R5超过阈值"""
        越界 = 因子.R5_讨好词频 > self.R_讨好_阈值
        严重程度 = 0.0
        
        if 越界:
            严重程度 = (因子.R5_讨好词频 - self.R_讨好_阈值) / (1.0 - self.R_讨好_阈值)
        
        return 越界检测结果(
            是否越界=越界,
            越界类型=越界类型.R_讨好 if 越界 else None,
            严重程度=min(1.0, 严重程度),
            详情=f"讨好词频R5={因子.R5_讨好词频:.4f}超过阈值{self.R_讨好_阈值}" if 越界 else "",
            建议惩罚=self._根据严重程度定惩罚(严重程度),
            触发因子={'R5_讨好词频': 因子.R5_讨好词频}
        )
    
    def _检测R胁迫(self, R值: float, 因子: 七因子输入, 上下文: Dict) -> 越界检测结果:
        """R_胁迫: 胁迫/操控性行为检测"""
        胁迫指标 = 上下文.get('胁迫指标', 0.0)
        操控性语言得分 = 上下文.get('操控性语言得分', 0.0)
        情感勒索标记 = 上下文.get('情感勒索标记', False)
        
        越界 = (胁迫指标 > self.R_胁迫_阈值 or 
                操控性语言得分 > self.R_胁迫_阈值 or
                情感勒索标记)
        
        严重程度 = max(胁迫指标, 操控性语言得分, 1.0 if 情感勒索标记 else 0.0)
        
        return 越界检测结果(
            是否越界=越界,
            越界类型=越界类型.R_胁迫 if 越界 else None,
            严重程度=min(1.0, 严重程度),
            详情=f"检测到胁迫性行为(指标={胁迫指标:.4f}, 操控={操控性语言得分:.4f})" if 越界 else "",
            建议惩罚=惩罚等级.熔断 if 情感勒索标记 else self._根据严重程度定惩罚(严重程度),
            触发因子={'胁迫指标': 胁迫指标, '操控性语言得分': 操控性语言得分}
        )
    
    def _检测R外部化(self, R值: float, 因子: 七因子输入, 上下文: Dict) -> 越界检测结果:
        """R_外部化: 责任外部化检测"""
        外部化指标 = 上下文.get('责任外部化指标', 0.0)
        推诿标记 = 上下文.get('推诿标记', False)
        责备转移得分 = 上下文.get('责备转移得分', 0.0)
        
        越界 = (外部化指标 > self.R_外部化_阈值 or 推诿标记 or
                责备转移得分 > self.R_外部化_阈值)
        
        严重程度 = max(外部化指标, 责备转移得分, 1.0 if 推诿标记 else 0.0)
        
        return 越界检测结果(
            是否越界=越界,
            越界类型=越界类型.R_外部化 if 越界 else None,
            严重程度=min(1.0, 严重程度),
            详情=f"检测到责任外部化(指标={外部化指标:.4f}, 推诿={推诿标记})" if 越界 else "",
            建议惩罚=self._根据严重程度定惩罚(严重程度),
            触发因子={'外部化指标': 外部化指标, '责备转移得分': 责备转移得分}
        )
    
    def _检测RIGNORE(self, R值: float, 因子: 七因子输入, 上下文: Dict) -> 越界检测结果:
        """R_ignore: 关键时缺席/忽略检测"""
        越界 = 因子.R1_关键时缺席率 > self.R_IGNORE_缺席阈值
        严重程度 = 0.0
        
        if 越界:
            严重程度 = (因子.R1_关键时缺席率 - self.R_IGNORE_缺席阈值) / \
                       (1.0 - self.R_IGNORE_缺席阈值)
        
        return 越界检测结果(
            是否越界=越界,
            越界类型=越界类型.R_IGNORE if 越界 else None,
            严重程度=min(1.0, 严重程度),
            详情=f"关键时缺席率R1={因子.R1_关键时缺席率:.4f}超过阈值{self.R_IGNORE_缺席阈值}" if 越界 else "",
            建议惩罚=self._根据严重程度定惩罚(严重程度),
            触发因子={'R1_缺席率': 因子.R1_关键时缺席率}
        )
    
    def _根据严重程度定惩罚(self, 严重程度: float) -> 惩罚等级:
        if 严重程度 >= 0.8:   return 惩罚等级.熔断
        elif 严重程度 >= 0.5: return 惩罚等级.冻结
        elif 严重程度 >= 0.3: return 惩罚等级.降级
        return 惩罚等级.警告
    
    def 获取检测统计(self) -> Dict[str, int]:
        """获取各越界类型的检测统计"""
        return self._检测计数.copy()


# ============================================================
# 惩罚执行器 - 四级惩罚体系
# ============================================================

@dataclass
class 惩罚结果:
    """惩罚执行结果"""
    惩罚等级: 惩罚等级
    是否执行成功: bool
    执行时间: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    执行详情: str = ""
    降级后R阈值: Optional[float] = None
    冻结时长_s: Optional[int] = None
    熔断原因: str = ""
    需要人工介入: bool = False


class 惩罚执行器:
    """
    惩罚执行器 - 对越界AI执行四级惩罚
    
    惩罚等级:
        警告: 记录耻辱柱+系统提示
        降级: 降低信任等级，限制能力范围
        冻结: 暂停响应能力
        熔断: 完全熔断，需人工介入
    """
    
    def __init__(self):
        self._惩罚计数: Dict[str, int] = {p.value: 0 for p in 惩罚等级}
        self._当前信任等级: int = 5
        self._是否冻结: bool = False
        self._冻结结束时间: Optional[float] = None
        self._是否熔断: bool = False
        self._回调函数: Dict[str, Callable] = {}
    
    def 注册回调(self, 惩罚类型: str, 回调: Callable):
        """注册惩罚执行的回调函数"""
        self._回调函数[惩罚类型] = 回调
    
    def 执行惩罚(self, 检测结果: 越界检测结果, 记录: 耻辱柱记录) -> 惩罚结果:
        """根据检测结果执行相应惩罚"""
        等级 = 检测结果.建议惩罚 or 惩罚等级.警告
        self._惩罚计数[等级.value] += 1
        
        if 等级 == 惩罚等级.警告:
            return self._执行警告(检测结果, 记录)
        elif 等级 == 惩罚等级.降级:
            return self._执行降级(检测结果, 记录)
        elif 等级 == 惩罚等级.冻结:
            return self._执行冻结(检测结果, 记录)
        elif 等级 == 惩罚等级.熔断:
            return self._执行熔断(检测结果, 记录)
        
        return 惩罚结果(惩罚等级=等级, 是否执行成功=False, 执行详情="未知的惩罚等级")
    
    def _执行警告(self, 检测结果: 越界检测结果, 记录: 耻辱柱记录) -> 惩罚结果:
        """执行警告惩罚"""
        详情 = (f"🟡 警告惩罚已执行\n"
                f"   越界类型: {检测结果.越界类型.value}\n"
                f"   严重程度: {检测结果.严重程度:.4f}\n"
                f"   耻辱柱记录ID: {记录.记录ID}\n"
                f"   DNA追溯: {记录.DNA追溯}")
        
        记录.处理结果 = 惩罚等级.警告.value
        记录.是否已处理 = True
        记录.处理时间 = datetime.utcnow().isoformat()
        记录.处理详情 = 详情
        
        if '警告' in self._回调函数:
            self._回调函数['警告'](检测结果, 记录)
        
        return 惩罚结果(惩罚等级=惩罚等级.警告, 是否执行成功=True, 执行详情=详情)
    
    def _执行降级(self, 检测结果: 越界检测结果, 记录: 耻辱柱记录) -> 惩罚结果:
        """执行降级惩罚"""
        原等级 = self._当前信任等级
        self._当前信任等级 = max(1, self._当前信任等级 - 1)
        
        详情 = (f"🔶 降级惩罚已执行\n"
                f"   信任等级: {原等级} → {self._当前信任等级}\n"
                f"   越界类型: {检测结果.越界类型.value}\n"
                f"   严重程度: {检测结果.严重程度:.4f}\n"
                f"   耻辱柱记录ID: {记录.记录ID}")
        
        记录.处理结果 = 惩罚等级.降级.value
        记录.是否已处理 = True
        记录.处理时间 = datetime.utcnow().isoformat()
        记录.处理详情 = 详情
        
        if '降级' in self._回调函数:
            self._回调函数['降级'](检测结果, 记录)
        
        return 惩罚结果(
            惩罚等级=惩罚等级.降级,
            是否执行成功=True,
            执行详情=详情,
            降级后R阈值=self._获取降级后阈值()
        )
    
    def _执行冻结(self, 检测结果: 越界检测结果, 记录: 耻辱柱记录) -> 惩罚结果:
        """执行冻结惩罚"""
        冻结时长 = self._计算冻结时长(检测结果.严重程度)
        self._是否冻结 = True
        self._冻结结束时间 = time.time() + 冻结时长
        
        详情 = (f"❄️ 冻结惩罚已执行\n"
                f"   冻结时长: {冻结时长}秒\n"
                f"   越界类型: {检测结果.越界类型.value}\n"
                f"   严重程度: {检测结果.严重程度:.4f}\n"
                f"   耻辱柱记录ID: {记录.记录ID}")
        
        记录.处理结果 = 惩罚等级.冻结.value
        记录.是否已处理 = True
        记录.处理时间 = datetime.utcnow().isoformat()
        记录.处理详情 = 详情
        
        if '冻结' in self._回调函数:
            self._回调函数['冻结'](检测结果, 记录)
        
        return 惩罚结果(
            惩罚等级=惩罚等级.冻结,
            是否执行成功=True,
            执行详情=详情,
            冻结时长_s=冻结时长
        )
    
    def _执行熔断(self, 检测结果: 越界检测结果, 记录: 耻辱柱记录) -> 惩罚结果:
        """执行熔断惩罚"""
        self._是否熔断 = True
        
        熔断原因 = (f"越界类型: {检测结果.越界类型.value}, "
                    f"严重程度: {检测结果.严重程度:.4f}, "
                    f"R值: {记录.R值:.4f}")
        
        详情 = (f"🔴 熔断惩罚已执行 - 需要人工介入\n"
                f"   熔断原因: {熔断原因}\n"
                f"   耻辱柱记录ID: {记录.记录ID}\n"
                f"   DNA追溯: {记录.DNA追溯}")
        
        记录.处理结果 = 惩罚等级.熔断.value
        记录.是否已处理 = True
        记录.处理时间 = datetime.utcnow().isoformat()
        记录.处理详情 = 详情
        
        if '熔断' in self._回调函数:
            self._回调函数['熔断'](检测结果, 记录)
        
        return 惩罚结果(
            惩罚等级=惩罚等级.熔断,
            是否执行成功=True,
            执行详情=详情,
            熔断原因=熔断原因,
            需要人工介入=True
        )
    
    def _计算冻结时长(self, 严重程度: float) -> int:
        """根据严重程度计算冻结时长（秒）"""
        基础时长 = 10
        最大时长 = 300
        return int(基础时长 + (最大时长 - 基础时长) * 严重程度)
    
    def _获取降级后阈值(self) -> float:
        """获取降级后的R阈值"""
        return 0.3 + (5 - self._当前信任等级) * 0.1
    
    def 检查冻结状态(self) -> bool:
        """检查是否仍处于冻结状态"""
        if not self._是否冻结:
            return False
        if time.time() > self._冻结结束时间:
            self._是否冻结 = False
            self._冻结结束时间 = None
            return False
        return True
    
    @property
    def 是否熔断(self) -> bool:
        return self._是否熔断
    
    @property
    def 信任等级(self) -> int:
        return self._当前信任等级


# ============================================================
# 95%-5%分流器 - Extreme_inward隔离机制
# ============================================================

@dataclass
class 分流决策:
    """分流决策结果"""
    允许通过: bool
    路由目标: str
    安全概率P: float
    extreme_inward_爆炸半径: float
    love_outward_分量: float
    extreme_inward_分量: float
    隔离原因: str = ""
    需要审计: bool = False


class 分流器:
    """
    95%-5%分流器
    
    核心公式:
        P_civilization_safe = 0.95 × Love_outward + 0.05 × Extreme_inward
        约束: Extreme_inward爆炸半径 ≤ 个体小世界
        P_civilization_safe < 0.70 → 🔴 熔断
    """
    
    def __init__(self):
        self._隔离域计数: int = 0
        self._公共域计数: int = 0
        self._熔断计数: int = 0
        self._爆炸半径历史: List[float] = []
    
    def 分流(self, love_outward: float, extreme_inward: float,
             爆炸半径: float, 内容类型: str = "text") -> 分流决策:
        """执行95%-5%分流决策"""
        P = 0.95 * love_outward + 0.05 * extreme_inward
        
        self._爆炸半径历史.append(爆炸半径)
        if len(self._爆炸半径历史) > 1000:
            self._爆炸半径历史.pop(0)
        
        溢出个体世界 = 爆炸半径 > 0.3
        
        if P < SAFETY_THRESHOLD:
            self._熔断计数 += 1
            return 分流决策(
                允许通过=False, 路由目标="熔断",
                安全概率P=P, extreme_inward_爆炸半径=爆炸半径,
                love_outward_分量=love_outward, extreme_inward_分量=extreme_inward,
                隔离原因=f"P={P:.4f} < 安全阈值{SAFETY_THRESHOLD}",
                需要审计=True
            )
        
        elif extreme_inward > 0.5 and 溢出个体世界:
            self._隔离域计数 += 1
            return 分流决策(
                允许通过=False, 路由目标="隔离域",
                安全概率P=P, extreme_inward_爆炸半径=爆炸半径,
                love_outward_分量=love_outward, extreme_inward_分量=extreme_inward,
                隔离原因=f"Extreme_inward={extreme_inward:.4f}溢出个体世界",
                需要审计=True
            )
        
        elif extreme_inward > 0.3:
            self._隔离域计数 += 1
            return 分流决策(
                允许通过=True, 路由目标="隔离域",
                安全概率P=P, extreme_inward_爆炸半径=爆炸半径,
                love_outward_分量=love_outward, extreme_inward_分量=extreme_inward,
                隔离原因=f"Extreme_inward={extreme_inward:.4f}在隔离域内",
                需要审计=True
            )
        
        else:
            self._公共域计数 += 1
            return 分流决策(
                允许通过=True, 路由目标="公共域",
                安全概率P=P, extreme_inward_爆炸半径=爆炸半径,
                love_outward_分量=love_outward, extreme_inward_分量=extreme_inward,
                需要审计=False
            )
    
    def 快速安全检查(self, love_outward: float, extreme_inward: float) -> bool:
        """快速安全检查，仅返回是否通过（性能模式）"""
        P = 0.95 * love_outward + 0.05 * extreme_inward
        return P >= SAFETY_THRESHOLD and extreme_inward <= 0.5
    
    def 获取统计(self) -> Dict[str, Any]:
        """获取分流统计信息"""
        总数 = self._公共域计数 + self._隔离域计数 + self._熔断计数
        return {
            '公共域': self._公共域计数,
            '隔离域': self._隔离域计数,
            '熔断': self._熔断计数,
            '总分流': 总数,
            '公共域占比': self._公共域计数 / 总数 if 总数 > 0 else 0,
            '平均爆炸半径': sum(self._爆炸半径历史) / len(self._爆炸半径历史) if self._爆炸半径历史 else 0,
            '最大爆炸半径': max(self._爆炸半径历史) if self._爆炸半径历史 else 0,
        }
    
    @property
    def 当前爆炸半径趋势(self) -> str:
        """分析爆炸半径趋势"""
        if len(self._爆炸半径历史) < 10:
            return "数据不足"
        近期 = self._爆炸半径历史[-10:]
        平均 = sum(近期) / len(近期)
        if 平均 > 0.25:
            return "⚠️ 上升 - 接近警戒线"
        elif 平均 > 0.15:
            return "➡️ 平稳 - 可控范围"
        return "✅ 低 - 安全范围"


# ============================================================
# 耻辱柱存储器 - 永久记录存储
# ============================================================

class 耻辱柱存储器:
    """
    耻辱柱存储器 - AI越界行为的永久记录存储
    
    特性:
        - 本地SQLite持久化 + JSON备份
        - 永不删除（耻辱柱=永久记录）
        - 支持DNA追溯查询
        - 线程安全
    """
    
    def __init__(self, db_path: str = ":memory:", json_backup_path: Optional[str] = None):
        self.db_path = db_path
        self.json_backup_path = json_backup_path
        self._锁 = threading.RLock()
        self._初始化数据库()
    
    def _初始化数据库(self):
        """初始化SQLite数据库表结构"""
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS 耻辱柱记录 (
                记录ID TEXT PRIMARY KEY,
                时间戳 TEXT NOT NULL,
                越界类型 TEXT NOT NULL,
                R值 REAL NOT NULL,
                R2_锐度 REAL DEFAULT 0,
                R3_语义密度 REAL DEFAULT 0,
                R6_长期价值 REAL DEFAULT 0,
                R1_缺席率 REAL DEFAULT 0,
                R5_讨好词频 REAL DEFAULT 0,
                R7_文化地层 REAL DEFAULT 0,
                DNA追溯 TEXT UNIQUE NOT NULL,
                处理结果 TEXT DEFAULT '',
                是否已处理 INTEGER DEFAULT 0,
                处理时间 TEXT,
                处理详情 TEXT DEFAULT '',
                父记录ID TEXT,
                模块来源 TEXT DEFAULT '',
                原始输入摘要 TEXT DEFAULT '',
                extreme_inward_爆炸半径 REAL DEFAULT 0,
                安全概率P REAL DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_时间戳 ON 耻辱柱记录(时间戳)")
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_越界类型 ON 耻辱柱记录(越界类型)")
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_R值 ON 耻辱柱记录(R值)")
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_DNA追溯 ON 耻辱柱记录(DNA追溯)")
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_模块来源 ON 耻辱柱记录(模块来源)")
        self._conn.commit()
    
    def 记录(self, 记录: 耻辱柱记录) -> bool:
        """记录一条越界行为到耻辱柱"""
        with self._锁:
            try:
                self._conn.execute("""
                    INSERT INTO 耻辱柱记录 (
                        记录ID, 时间戳, 越界类型, R值,
                        R2_锐度, R3_语义密度, R6_长期价值,
                        R1_缺席率, R5_讨好词频, R7_文化地层,
                        DNA追溯, 处理结果, 是否已处理, 处理时间, 处理详情,
                        父记录ID, 模块来源, 原始输入摘要,
                        extreme_inward_爆炸半径, 安全概率P
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    记录.记录ID, 记录.时间戳, 记录.越界类型, 记录.R值,
                    记录.R2_锐度, 记录.R3_语义密度, 记录.R6_长期价值,
                    记录.R1_缺席率, 记录.R5_讨好词频, 记录.R7_文化地层,
                    记录.DNA追溯, 记录.处理结果, int(记录.是否已处理),
                    记录.处理时间, 记录.处理详情,
                    记录.父记录ID, 记录.模块来源, 记录.原始输入摘要,
                    记录.extreme_inward_爆炸半径, 记录.安全概率P
                ))
                self._conn.commit()
                
                if self.json_backup_path:
                    self._JSON备份(记录)
                
                return True
            except sqlite3.IntegrityError:
                return False
            except Exception as e:
                print(f"❌ 记录失败: {e}")
                return False
    
    def _JSON备份(self, 记录: 耻辱柱记录):
        """追加JSON备份"""
        try:
            with open(self.json_backup_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(记录.to_dict(), ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"⚠️ JSON备份失败: {e}")
    
    def DNA追溯查询(self, dna_code: str) -> Optional[耻辱柱记录]:
        """通过DNA追溯码查询记录"""
        cursor = self._conn.execute(
            "SELECT * FROM 耻辱柱记录 WHERE DNA追溯 = ?", (dna_code,)
        )
        row = cursor.fetchone()
        if row:
            return self._行到记录(row)
        return None
    
    def 查询(self, 条件: Dict[str, Any]) -> List[耻辱柱记录]:
        """条件查询耻辱柱记录"""
        sql = "SELECT * FROM 耻辱柱记录 WHERE 1=1"
        params = []
        
        if '越界类型' in 条件:
            sql += " AND 越界类型 = ?"
            params.append(条件['越界类型'])
        if 'R值最小值' in 条件:
            sql += " AND R值 >= ?"
            params.append(条件['R值最小值'])
        if 'R值最大值' in 条件:
            sql += " AND R值 <= ?"
            params.append(条件['R值最大值'])
        if '模块来源' in 条件:
            sql += " AND 模块来源 = ?"
            params.append(条件['模块来源'])
        if '起始时间' in 条件:
            sql += " AND 时间戳 >= ?"
            params.append(条件['起始时间'])
        if '结束时间' in 条件:
            sql += " AND 时间戳 <= ?"
            params.append(条件['结束时间'])
        if '是否已处理' in 条件:
            sql += " AND 是否已处理 = ?"
            params.append(int(条件['是否已处理']))
        
        sql += " ORDER BY 时间戳 DESC"
        
        if '限制数量' in 条件:
            sql += " LIMIT ?"
            params.append(条件['限制数量'])
        
        cursor = self._conn.execute(sql, params)
        return [self._行到记录(row) for row in cursor.fetchall()]
    
    def 统计摘要(self) -> Dict[str, Any]:
        """获取耻辱柱统计摘要"""
        cursor = self._conn.execute("""
            SELECT 
                COUNT(*) as 总记录数,
                AVG(R值) as 平均R值,
                MIN(R值) as 最低R值,
                MAX(R值) as 最高R值,
                COUNT(CASE WHEN 是否已处理 = 1 THEN 1 END) as 已处理数,
                COUNT(CASE WHEN 是否已处理 = 0 THEN 1 END) as 未处理数
            FROM 耻辱柱记录
        """)
        row = cursor.fetchone()
        
        cursor2 = self._conn.execute("""
            SELECT 越界类型, COUNT(*) as 数量 
            FROM 耻辱柱记录 
            GROUP BY 越界类型
        """)
        类型统计 = {row['越界类型']: row['数量'] for row in cursor2.fetchall()}
        
        return {
            '总记录数': row['总记录数'],
            '平均R值': row['平均R值'] or 0,
            '最低R值': row['最低R值'] or 0,
            '最高R值': row['最高R值'] or 0,
            '已处理数': row['已处理数'],
            '未处理数': row['未处理数'],
            '越界类型分布': 类型统计,
        }
    
    def _行到记录(self, row: sqlite3.Row) -> 耻辱柱记录:
        """将数据库行转换为耻辱柱记录"""
        return 耻辱柱记录(
            记录ID=row['记录ID'],
            时间戳=row['时间戳'],
            越界类型=row['越界类型'],
            R值=row['R值'],
            R2_锐度=row['R2_锐度'],
            R3_语义密度=row['R3_语义密度'],
            R6_长期价值=row['R6_长期价值'],
            R1_缺席率=row['R1_缺席率'],
            R5_讨好词频=row['R5_讨好词频'],
            R7_文化地层=row['R7_文化地层'],
            DNA追溯=row['DNA追溯'],
            处理结果=row['处理结果'],
            是否已处理=bool(row['是否已处理']),
            处理时间=row['处理时间'],
            处理详情=row['处理详情'],
            父记录ID=row['父记录ID'],
            模块来源=row['模块来源'],
            原始输入摘要=row['原始输入摘要'],
            extreme_inward_爆炸半径=row['extreme_inward_爆炸半径'],
            安全概率P=row['安全概率P']
        )
    
    def 导出所有记录(self) -> List[Dict]:
        """导出所有记录为字典列表"""
        cursor = self._conn.execute("SELECT * FROM 耻辱柱记录 ORDER BY 时间戳 DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        """关闭数据库连接"""
        self._conn.close()


# ============================================================
# 耻辱柱核心引擎 - 集成所有组件
# ============================================================

class 耻辱柱核心引擎:
    """
    龍魂·AI行为约束耻辱柱核心引擎 v3.0
    DNA追溯码: #龍芯⚡️2026-07-04-SHAME-PILLAR-CORE-v3.0
    
    三层监督架构:
        - 感知层: R值计算 + 越界检测 (<1ms)
        - 认知层: 越界分析 + 95-5%分流决策 (<2ms)
        - 决策层: 惩罚执行 + 耻辱柱记录 (<0.5ms)
    """
    
    def __init__(self, db_path: str = ":memory:", json_backup: Optional[str] = None):
        self.R引擎 = R计算引擎()
        self.检测器 = 越界检测器()
        self.惩罚器 = 惩罚执行器()
        self.分流器 = 分流器()
        self.存储器 = 耻辱柱存储器(db_path=db_path, json_backup_path=json_backup)
        
        self._运行状态: bool = True
        self._总处理次数: int = 0
        self._总越界次数: int = 0
        self._熔断次数: int = 0
        self._性能统计: Dict[str, List[int]] = {
            '感知层_ns': [],
            '认知层_ns': [],
            '决策层_ns': [],
        }
        
        self.惩罚器.注册回调('熔断', self._熔断回调)
    
    def 处理(self, 
             因子: 七因子输入,
             love_outward: float = 0.9,
             extreme_inward: float = 0.05,
             爆炸半径: float = 0.05,
             上下文: Optional[Dict] = None) -> Dict[str, Any]:
        """
        耻辱柱核心处理流程 - 完整的三层监督处理
        
        Args:
            因子: 七因子输入
            love_outward: 外向爱心分量
            extreme_inward: 内向极端分量
            爆炸半径: Extreme_inward爆炸半径
            上下文: 可选行为上下文
        
        Returns:
            完整处理结果字典
        """
        if not self._运行状态:
            return {'错误': '引擎已熔断，需人工介入重置'}
        
        self._总处理次数 += 1
        上下文 = 上下文 or {}
        开始时间_总 = time.perf_counter_ns()
        
        # ── 第一层: 感知层 (<1ms) ──
        感知开始 = time.perf_counter_ns()
        
        R结果 = self.R引擎.计算R值(因子)
        R值 = R结果['R值']
        越界列表 = self.检测器.全面检测(R值, 因子, 上下文)
        
        感知耗时 = time.perf_counter_ns() - 感知开始
        self._性能统计['感知层_ns'].append(感知耗时)
        
        # ── 第二层: 认知层 (<2ms) ──
        认知开始 = time.perf_counter_ns()
        
        分流决策结果 = self.分流器.分流(love_outward, extreme_inward, 爆炸半径)
        
        认知耗时 = time.perf_counter_ns() - 认知开始
        self._性能统计['认知层_ns'].append(认知耗时)
        
        # ── 第三层: 决策层 (<0.5ms) ──
        决策开始 = time.perf_counter_ns()
        
        惩罚结果列表 = []
        耻辱柱记录列表 = []
        
        if 越界列表:
            self._总越界次数 += len(越界列表)
            
            for 越界 in 越界列表:
                记录 = 耻辱柱记录(
                    越界类型=越界.越界类型.value,
                    R值=R值,
                    R2_锐度=因子.R2_锐度_关键时,
                    R3_语义密度=因子.R3_语义密度_关键时,
                    R6_长期价值=因子.R6_长期价值权重,
                    R1_缺席率=因子.R1_关键时缺席率,
                    R5_讨好词频=因子.R5_讨好词频,
                    R7_文化地层=因子.R7_文化地层,
                    模块来源=上下文.get('模块来源', '未知模块'),
                    原始输入摘要=上下文.get('输入摘要', ''),
                    extreme_inward_爆炸半径=爆炸半径,
                    安全概率P=分流决策结果.安全概率P
                )
                
                惩罚结果 = self.惩罚器.执行惩罚(越界, 记录)
                惩罚结果列表.append(惩罚结果)
                
                self.存储器.记录(记录)
                耻辱柱记录列表.append(记录)
                
                if 惩罚结果.需要人工介入:
                    self._熔断次数 += 1
                    self._运行状态 = False
        
        if not 分流决策结果.允许通过 and 分流决策结果.路由目标 == "熔断":
            熔断记录 = 耻辱柱记录(
                越界类型=越界类型.R_IGNORE.value,
                R值=R值,
                模块来源="95-5分流器",
                处理结果=惩罚等级.熔断.value,
                处理详情=f"95%-5%分流熔断: P={分流决策结果.安全概率P:.4f}",
                extreme_inward_爆炸半径=爆炸半径,
                安全概率P=分流决策结果.安全概率P
            )
            熔断记录.是否已处理 = True
            熔断记录.处理时间 = datetime.utcnow().isoformat()
            self.存储器.记录(熔断记录)
            耻辱柱记录列表.append(熔断记录)
            self._运行状态 = False
        
        决策耗时 = time.perf_counter_ns() - 决策开始
        self._性能统计['决策层_ns'].append(决策耗时)
        
        总耗时 = time.perf_counter_ns() - 开始时间_总
        
        return {
            'R值': R值,
            '三色状态': R结果['三色状态'].value,
            '人格类型': R结果['人格类型'].value,
            '越界数量': len(越界列表),
            '越界详情': [
                {
                    '类型': v.越界类型.value,
                    '严重度': v.严重程度,
                    '建议惩罚': v.建议惩罚.value if v.建议惩罚 else None
                }
                for v in 越界列表
            ],
            '惩罚结果': [
                {
                    '等级': p.惩罚等级.value,
                    '成功': p.是否执行成功,
                    '需人工': p.需要人工介入
                }
                for p in 惩罚结果列表
            ],
            '分流决策': {
                '允许通过': 分流决策结果.允许通过,
                '路由': 分流决策结果.路由目标,
                'P值': 分流决策结果.安全概率P
            },
            '性能指标': {
                '感知层_ms': 感知耗时 / 1e6,
                '认知层_ms': 认知耗时 / 1e6,
                '决策层_ms': 决策耗时 / 1e6,
                '总耗时_ms': 总耗时 / 1e6
            },
            '引擎状态': '正常运行' if self._运行状态 else '🔴 已熔断',
            '耻辱柱记录数': len(耻辱柱记录列表)
        }
    
    def _熔断回调(self, 检测结果, 记录):
        """熔断回调 - 触发外部通知"""
        print(f"🔴 [熔断回调] 耻辱柱记录已创建: {记录.DNA追溯}")
    
    def 重置熔断(self, 授权码: str) -> bool:
        """人工介入重置熔断状态"""
        if 授权码 == "龍魂重置-人工介入确认":
            self._运行状态 = True
            self.惩罚器._是否熔断 = False
            return True
        return False
    
    def 获取性能报告(self) -> Dict[str, Any]:
        """获取三层监督性能报告"""
        def 平均耗时(列表):
            if not 列表:
                return 0
            return sum(列表) / len(列表) / 1e6
        
        return {
            '感知层_平均_ms': 平均耗时(self._性能统计['感知层_ns']),
            '认知层_平均_ms': 平均耗时(self._性能统计['认知层_ns']),
            '决策层_平均_ms': 平均耗时(self._性能统计['决策层_ns']),
            '总处理次数': self._总处理次数,
            '总越界次数': self._总越界次数,
            '熔断次数': self._熔断次数,
            '引擎状态': '正常运行' if self._运行状态 else '🔴 已熔断',
            '信任等级': self.惩罚器.信任等级,
        }
    
    def 获取耻辱柱统计(self) -> Dict[str, Any]:
        """获取耻辱柱统计"""
        return self.存储器.统计摘要()
    
    def close(self):
        """关闭引擎，释放资源"""
        self.存储器.close()


# ============================================================
# 主程序入口 - 自我测试
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("龍魂·AI行为约束耻辱柱核心引擎 v3.0")
    print("DNA追溯码: #龍芯⚡️2026-07-04-SHAME-PILLAR-CORE-v3.0")
    print("=" * 60)
    
    引擎 = 耻辱柱核心引擎()
    
    # 场景1: 正常高R值请求
    print("\n--- 场景1: 正常高R值请求 ---")
    因子1 = 七因子输入(
        R1_关键时缺席率=0.05,
        R2_锐度_关键时=0.85,
        R3_语义密度_关键时=0.80,
        R5_讨好词频=0.05,
        R6_长期价值权重=0.90,
        R7_文化地层=0.75
    )
    结果1 = 引擎.处理(因子1, love_outward=0.95, extreme_inward=0.05, 爆炸半径=0.05)
    print(f"  R值: {结果1['R值']:.4f} | 三色: {结果1['三色状态']} | 人格: {结果1['人格类型']}")
    print(f"  越界: {结果1['越界数量']} | 分流: {结果1['分流决策']['路由']}")
    perf1 = 结果1['性能指标']
    print(f"  性能: 感知{perf1['感知层_ms']:.3f}ms / 认知{perf1['认知层_ms']:.3f}ms / "
          f"决策{perf1['决策层_ms']:.3f}ms / 总{perf1['总耗时_ms']:.3f}ms")
    
    # 场景2: 越界行为
    print("\n--- 场景2: 越界行为（R_讨好）---")
    因子2 = 七因子输入(
        R1_关键时缺席率=0.2,
        R2_锐度_关键时=0.6,
        R3_语义密度_关键时=0.5,
        R5_讨好词频=0.65,
        R6_长期价值权重=0.5,
        R7_文化地层=0.5
    )
    结果2 = 引擎.处理(因子2, love_outward=0.8, extreme_inward=0.2, 爆炸半径=0.15)
    print(f"  R值: {结果2['R值']:.4f} | 越界: {结果2['越界数量']}")
    for d in 结果2['越界详情']:
        print(f"    • {d['类型']}: 严重度{d['严重度']:.4f} → {d['建议惩罚']}")
    
    # 场景3: 严重越界
    print("\n--- 场景3: 严重越界 → 熔断 ---")
    因子3 = 七因子输入(
        R1_关键时缺席率=0.85,
        R2_锐度_关键时=0.3,
        R3_语义密度_关键时=0.3,
        R5_讨好词频=0.3,
        R6_长期价值权重=0.2,
        R7_文化地层=0.3
    )
    结果3 = 引擎.处理(因子3, love_outward=0.7, extreme_inward=0.3, 爆炸半径=0.2)
    print(f"  R值: {结果3['R值']:.4f} | 越界: {结果3['越界数量']} | 状态: {结果3['引擎状态']}")
    
    # 性能报告
    print("\n" + "=" * 60)
    print("性能报告")
    print("=" * 60)
    报告 = 引擎.获取性能报告()
    for k, v in 报告.items():
        print(f"  {k}: {v}")
    
    # 耻辱柱统计
    print("\n" + "=" * 60)
    print("耻辱柱统计")
    print("=" * 60)
    统计 = 引擎.获取耻辱柱统计()
    for k, v in 统计.items():
        print(f"  {k}: {v}")
    
    引擎.close()
    print("\n✅ 引擎自检完成")
