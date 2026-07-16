#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三才流场MCP引擎v4.0 - 状态容器

天场·地场·人场三位一体状态容器
洛书九宫 · 五色审计 · 五大人格 · 龍盾脉冲

DNA: #龍芯⚡️2026-06-09-三才流场-FlowFieldState-v4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅
"""

from __future__ import annotations

import time
import hashlib
import json
from enum import Enum, auto
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Callable, Any, Tuple
from datetime import datetime
from collections import deque
import threading


class 审计色码(Enum):
    """三色审计状态枚举"""
    绿色 = "🟢"  # 正常/平衡
    黄色 = "🟡"  # 警告/相克
    红色 = "🔴"  # 危险/熔断


class 人格状态(Enum):
    """五大人格运行状态枚举"""
    待机 = "待机"
    激活 = "激活"
    熔断 = "熔断"
    降级 = "降级"
    守护 = "守护"


class 审计维度(Enum):
    """天场审计五维度"""
    平衡 = "平衡"
    相克 = "相克"
    三才 = "三才"
    置信 = "置信"
    整体 = "整体"


@dataclass
class 龍盾脉冲结构:
    """龍盾脉冲数据结构 - 宫格5不动点锚定"""
    心跳时间戳: float = field(default_factory=time.time)
    稳定指数: float = 1.0  # 0.0-1.0
    上次校正: Optional[float] = None
    不动点锚: int = 5  # 宫格5为永恒不动点
    校正次数: int = 0
    脉冲序列: deque = field(default_factory=lambda: deque(maxlen=64))

    def 到字典(self) -> Dict[str, Any]:
        return {
            "heartbeat": self.心跳时间戳,
            "stability": self.稳定指数,
            "lastCorrection": self.上次校正,
            "anchor": self.不动点锚,
            "correctionCount": self.校正次数,
            "pulseSequence": list(self.脉冲序列)
        }


@dataclass
class 人格状态结构:
    """单个人格完整状态"""
    名称: str
    标识: str
    状态: 人格状态 = 人格状态.待机
    激活时间: Optional[float] = None
    累计激活时长: float = 0.0
    处理任务数: int = 0
    版本: str = "4.0"
    元数据: Dict[str, Any] = field(default_factory=dict)

    def 到字典(self) -> Dict[str, Any]:
        return {
            "name": self.名称,
            "id": self.标识,
            "status": self.状态.value,
            "activatedAt": self.激活时间,
            "totalActiveTime": self.累计激活时长,
            "tasksProcessed": self.处理任务数,
            "version": self.版本,
            "metadata": self.元数据
        }


class 流场状态:
    """
    三才流场MCP引擎v4.0 - 核心状态容器

    管理天场（审计）、地场（密度）、人场（人格）、龍盾（脉冲）
    四重状态空间，事件驱动，量子观测兼容
    """

    # ═══════════════════════════════════════════════
    #  类常量
    # ═══════════════════════════════════════════════

    洛书九宫映射: Dict[int, str] = {
        1: "坎·北", 2: "坤·西南", 3: "震·东",
        4: "巽·东南", 5: "中宫·不动", 6: "干·西北",
        7: "兑·西", 8: "艮·东北", 9: "离·南"
    }

    五行属性: Dict[int, str] = {
        1: "水", 2: "土", 3: "木", 4: "木",
        5: "土", 6: "金", 7: "金", 8: "土", 9: "火"
    }

    事件类型定义: Tuple[str, ...] = (
        "densityChange",           # 密度变化
        "audit:red",               # 红色审计警报
        "audit:orange",            # 黄色审计警告
        "audit:green",             # 绿色审计正常
        "syncer:degraded",         # 同步官降级
        "syncer:recovered",        # 同步官恢复
        "persona:activated",       # 人格激活
        "persona:fused",           # 人格融合
        "dragon:correction",       # 龍盾校正
        "dragon:heartbeat",        # 龍盾心跳
        "field:resonance",         # 流场共振
        "field:collapse",          # 流场坍缩
    )

    def __init__(self, 设备标识: str = "UID9622"):
        """
        初始化三才流场完整状态容器

        Args:
            设备标识: 设备唯一标识，默认UID9622
        """
        self._设备标识 = 设备标识
        self._初始化时间 = time.time()
        self._锁 = threading.RLock()
        self._事件监听器: Dict[str, List[Callable]] = {ev: [] for ev in self.事件类型定义}
        self._历史记录: deque = deque(maxlen=1024)
        self._版本 = "4.0.0"

        # ═════════════════════════════════════════
        #  天场（auditField）- 三色审计
        # ═════════════════════════════════════════
        self._审计天场: Dict[str, 审计色码] = {
            审计维度.平衡.value: 审计色码.绿色,
            审计维度.相克.value: 审计色码.绿色,
            审计维度.三才.value: 审计色码.绿色,
            审计维度.置信.value: 审计色码.绿色,
            审计维度.整体.value: 审计色码.绿色,
        }
        self._审计历史: deque = deque(maxlen=256)
        self._审计频率: int = 1  # 每秒审计次数
        self._审计计数器: int = 0

        # ═════════════════════════════════════════
        #  地场（merkleDensity）- 洛书九宫密度
        # ═════════════════════════════════════════
        self._九宫密度: Dict[int, float] = {
            1: 0.5, 2: 0.5, 3: 0.5,
            4: 0.5, 5: 1.0, 6: 0.5,  # 宫格5=1.0不动点
            7: 0.5, 8: 0.5, 9: 0.5,
        }
        self._密度历史: Dict[int, deque] = {
            i: deque(maxlen=128) for i in range(1, 10)
        }
        self._密度趋势: Dict[int, float] = {i: 0.0 for i in range(1, 10)}
        self._merkle根哈希: str = self._计算初始_merkle根()

        # ═════════════════════════════════════════
        #  人场（personas）- 五大人格状态
        # ═════════════════════════════════════════
        self._人格集: Dict[str, 人格状态结构] = {
            "wenwen": 人格状态结构(
                名称="雯雯P03·技术整理师",
                标识="wenwen",
                元数据={"职责": "归档·整理·索引", "宫格": "2", "五行": "土"}
            ),
            "p72": 人格状态结构(
                名称="宝宝P72·龍盾",
                标识="p72",
                状态=人格状态.守护,  # 始终激活
                激活时间=time.time(),
                元数据={
                    "职责": "熔断守门·宫格5不动点锚",
                    "宫格": "5",
                    "五行": "土",
                    "始终激活": True,
                    "不动点锚定": True
                }
            ),
            "scout": 人格状态结构(
                名称="侦察兵",
                标识="scout",
                元数据={"职责": "信息收集·外部感知", "宫格": "3", "五行": "木"}
            ),
            "architect": 人格状态结构(
                名称="架构师",
                标识="architect",
                元数据={"职责": "系统设计·逻辑构建", "宫格": "6", "五行": "金"}
            ),
            "syncer": 人格状态结构(
                名称="同步官",
                标识="syncer",
                元数据={"职责": "状态同步·一致性维护", "宫格": "1", "五行": "水"}
            ),
        }
        self._当前主导人格: Optional[str] = None
        self._人格融合模式: bool = False
        self._融合人格列表: List[str] = []

        # ═════════════════════════════════════════
        #  龍盾脉冲（dragonPulse）- 不动点锚定
        # ═════════════════════════════════════════
        self._龍盾脉冲 = 龍盾脉冲结构()
        self._龍盾脉冲.脉冲序列.append({
            "ts": time.time(),
            "stability": 1.0,
            "event": "init"
        })

        # ═════════════════════════════════════════
        #  五层设备映射
        # ═════════════════════════════════════════
        self._五层目录: Dict[str, str] = {
            "L0": "~/longhun-lu/",       # 干·主权层
            "L1": "~/longhun-jq/",       # 离·继承层
            "L2": "~/longhun-al/",       # 震·战友层
            "L3": "~/longhun-pub/",      # 巽·公开层
            "L4": "~/longhun-cloud/",    # 坎·云端层
        }
        self._五层数据库: Dict[str, str] = {
            "L0": "DB_LU",      # 老大个人·M4 Mac
            "L1": "DB_JQ",      # 佳琪UID9622-JQ001
            "L2": "DB_AL",      # 核心战友
            "L3": "DB_PUB",     # 公开发布
            "L4": "DB_CLOUD",   # 云端备份
        }

        # ═════════════════════════════════════════
        #  系统统计
        # ═════════════════════════════════════════
        self._状态变更次数: int = 0
        self._密度更新次数: int = 0
        self._审计次数: int = 0
        self._脉冲次数: int = 0

    # ═══════════════════════════════════════════════
    #  属性访问器（只读）
    # ═══════════════════════════════════════════════

    @property
    def 九宫密度(self) -> Dict[int, float]:
        """获取九宫密度快照（深拷贝）"""
        with self._锁:
            return dict(self._九宫密度)

    @property
    def 审计天场(self) -> Dict[str, str]:
        """获取天场审计色码快照"""
        with self._锁:
            return {k: v.value for k, v in self._审计天场.items()}

    @property
    def 龍盾脉冲状态(self) -> Dict[str, Any]:
        """获取龍盾脉冲状态"""
        with self._锁:
            return self._龍盾脉冲.到字典()

    @property
    def merkle根哈希(self) -> str:
        """获取当前Merkle根哈希"""
        with self._锁:
            return self._merkle根哈希

    @property
    def 当前主导人格(self) -> Optional[str]:
        """获取当前主导人格标识"""
        with self._锁:
            return self._当前主导人格

    @property
    def 系统版本(self) -> str:
        """获取系统版本"""
        return self._版本

    # ═══════════════════════════════════════════════
    #  地场操作 - Merkle密度九宫格
    # ═══════════════════════════════════════════════

    def 更新密度(self, 宫格: int, 新密度: float) -> Dict[str, Any]:
        """
        更新指定宫格密度，触发densityChange事件

        Args:
            宫格: 1-9的宫格编号
            新密度: 0.0-1.0之间的密度值

        Returns:
            变更记录字典

        Raises:
            ValueError: 宫格或密度值非法
        """
        if not 1 <= 宫格 <= 9:
            raise ValueError(f"宫格必须在1-9之间，收到: {宫格}")
        if not 0.0 <= 新密度 <= 1.0:
            raise ValueError(f"密度必须在0.0-1.0之间，收到: {新密度}")
        if 宫格 == 5:
            raise ValueError("宫格5为不动点，禁止直接修改密度（恒=1.0）")

        with self._锁:
            旧密度 = self._九宫密度[宫格]
            self._九宫密度[宫格] = 新密度
            self._密度更新次数 += 1

            # 记录密度历史
            self._密度历史[宫格].append({
                "ts": time.time(),
                "old": 旧密度,
                "new": 新密度,
                "delta": 新密度 - 旧密度
            })

            # 计算密度趋势（简单移动平均斜率）
            历史列表 = list(self._密度历史[宫格])
            if len(历史列表) >= 2:
                最新 = 历史列表[-1]["new"]
                最早 = 历史列表[0]["new"]
                时长 = 历史列表[-1]["ts"] - 历史列表[0]["ts"]
                if 时长 > 0:
                    self._密度趋势[宫格] = (最新 - 最早) / 时长

            # 重新计算Merkle根
            旧哈希 = self._merkle根哈希
            self._merkle根哈希 = self._计算_merkle根()

            # 构建变更记录
            变更记录 = {
                "type": "densityChange",
                "宫格": 宫格,
                "方位": self.洛书九宫映射[宫格],
                "五行": self.五行属性[宫格],
                "旧密度": 旧密度,
                "新密度": 新密度,
                "变化量": round(新密度 - 旧密度, 6),
                "趋势": round(self._密度趋势[宫格], 6),
                "旧哈希": 旧哈希,
                "新哈希": self._merkle根哈希,
                "时间戳": time.time()
            }

            self._记录历史(变更记录)
            self._状态变更次数 += 1

            # 触发事件
            self._触发事件("densityChange", 变更记录)

            return 变更记录

    def 批量更新密度(self, 密度映射: Dict[int, float]) -> List[Dict[str, Any]]:
        """
        批量更新多个宫格密度

        Args:
            密度映射: {宫格: 新密度} 字典

        Returns:
            变更记录列表
        """
        结果 = []
        for 宫格, 密度 in sorted(密度映射.items()):
            try:
                记录 = self.更新密度(宫格, 密度)
                结果.append(记录)
            except ValueError as e:
                结果.append({"type": "error", "宫格": 宫格, "error": str(e)})
        return 结果

    def 获取密度趋势(self, 宫格: Optional[int] = None) -> Dict[str, float]:
        """
        获取密度趋势分析

        Args:
            宫格: 指定宫格或None获取全部

        Returns:
            趋势字典
        """
        with self._锁:
            if 宫格 is not None:
                return {宫格: self._密度趋势.get(宫格, 0.0)}
            return dict(self._密度趋势)

    def 获取密度热力图(self) -> Dict[int, Dict[str, Any]]:
        """
        获取九宫密度完整热力图

        Returns:
            每个宫格的详细状态字典
        """
        with self._锁:
            热力图 = {}
            for 宫格 in range(1, 10):
                历史列表 = list(self._密度历史[宫格])
                热力图[宫格] = {
                    "宫格": 宫格,
                    "方位": self.洛书九宫映射[宫格],
                    "五行": self.五行属性[宫格],
                    "当前密度": self._九宫密度[宫格],
                    "趋势": round(self._密度趋势[宫格], 6),
                    "历史点数": len(历史列表),
                    "平均值": round(sum(h["new"] for h in 历史列表) / len(历史列表), 6) if 历史列表 else self._九宫密度[宫格],
                    "最小值": round(min(h["new"] for h in 历史列表), 6) if 历史列表 else self._九宫密度[宫格],
                    "最大值": round(max(h["new"] for h in 历史列表), 6) if 历史列表 else self._九宫密度[宫格],
                    "是否不动点": 宫格 == 5,
                }
            return 热力图

    # ═══════════════════════════════════════════════
    #  天场操作 - 三色审计
    # ═══════════════════════════════════════════════

    def 审计(self, 审计类型: str, 色码: str) -> Dict[str, Any]:
        """
        更新天场审计色

        Args:
            审计类型: "平衡"|"相克"|"三才"|"置信"|"整体"
            色码: "🟢"|"🟡"|"🔴"

        Returns:
            审计记录
        """
        if 审计类型 not in [d.value for d in 审计维度]:
            raise ValueError(f"未知审计维度: {审计类型}")

        try:
            新色码 = {"🟢": 审计色码.绿色, "🟡": 审计色码.黄色, "🔴": 审计色码.红色}[色码]
        except KeyError:
            raise ValueError(f"非法色码: {色码}，必须是🟢/🟡/🔴")

        with self._锁:
            旧色码 = self._审计天场[审计类型]
            self._审计天场[审计类型] = 新色码
            self._审计次数 += 1
            self._审计计数器 += 1

            记录 = {
                "type": "audit",
                "审计类型": 审计类型,
                "旧色码": 旧色码.value,
                "新色码": 新色码.value,
                "时间戳": time.time(),
                "累计审计": self._审计次数
            }

            self._审计历史.append(记录)
            self._记录历史(记录)
            self._状态变更次数 += 1

            # 根据色码触发对应事件
            if 新色码 == 审计色码.红色:
                self._触发事件("audit:red", {**记录, "severity": "critical"})
            elif 新色码 == 审计色码.黄色:
                self._触发事件("audit:orange", {**记录, "severity": "warning"})
            else:
                self._触发事件("audit:green", {**记录, "severity": "normal"})

            return 记录

    def 批量审计(self, 审计映射: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        批量更新多个审计维度

        Args:
            审计映射: {审计类型: 色码} 字典

        Returns:
            审计记录列表
        """
        结果 = []
        for 类型, 色 in 审计映射.items():
            try:
                记录 = self.审计(类型, 色)
                结果.append(记录)
            except ValueError as e:
                结果.append({"type": "error", "审计类型": 类型, "error": str(e)})
        return 结果

    def 获取整体审计色(self) -> str:
        """
        计算整体审计色（取最严重的）

        Returns:
            🟢|🟡|🔴
        """
        with self._锁:
            色优先级 = {审计色码.红色: 2, 审计色码.黄色: 1, 审计色码.绿色: 0}
            最严重 = max(self._审计天场.values(), key=lambda c: 色优先级[c])
            return 最严重.value

    def 获取审计摘要(self) -> Dict[str, Any]:
        """获取审计场完整摘要"""
        with self._锁:
            return {
                "当前审计": self.审计天场,
                "整体色": self.获取整体审计色(),
                "总审计次数": self._审计次数,
                "审计频率": self._审计频率,
            }

    # ═══════════════════════════════════════════════
    #  人场操作 - 五大人格
    # ═══════════════════════════════════════════════

    def 激活人格(self, 人格标识: str) -> Dict[str, Any]:
        """
        激活指定人格

        Args:
            人格标识: wenwen|p72|scout|architect|syncer

        Returns:
            激活记录
        """
        if 人格标识 not in self._人格集:
            raise ValueError(f"未知人格: {人格标识}")

        with self._锁:
            人格 = self._人格集[人格标识]

            # p72始终激活，不允许修改
            if 人格标识 == "p72":
                return {
                    "type": "persona:guard",
                    "人格": 人格标识,
                    "状态": "始终守护",
                    "不可变更": True,
                    "时间戳": time.time()
                }

            旧状态 = 人格.状态
            人格.状态 = 人格状态.激活
            人格.激活时间 = time.time()
            self._当前主导人格 = 人格标识

            记录 = {
                "type": "persona:activated",
                "人格": 人格标识,
                "名称": 人格.名称,
                "旧状态": 旧状态.value,
                "新状态": 人格状态.激活.value,
                "时间戳": time.time()
            }

            self._记录历史(记录)
            self._触发事件("persona:activated", 记录)
            self._状态变更次数 += 1

            return 记录

    def 人格熔断(self, 人格标识: str, 原因: str = "") -> Dict[str, Any]:
        """
        对指定人格执行熔断

        Args:
            人格标识: 人格标识符
            原因: 熔断原因

        Returns:
            熔断记录
        """
        if 人格标识 not in self._人格集:
            raise ValueError(f"未知人格: {人格标识}")

        with self._锁:
            人格 = self._人格集[人格标识]
            旧状态 = 人格.状态
            人格.状态 = 人格状态.熔断

            记录 = {
                "type": "persona:fused",
                "人格": 人格标识,
                "名称": 人格.名称,
                "旧状态": 旧状态.value,
                "新状态": 人格状态.熔断.value,
                "原因": 原因,
                "时间戳": time.time()
            }

            self._记录历史(记录)
            self._状态变更次数 += 1

            return 记录

    def 人格降级(self, 人格标识: str, 原因: str = "") -> Dict[str, Any]:
        """将人格降级处理"""
        if 人格标识 not in self._人格集:
            raise ValueError(f"未知人格: {人格标识}")

        with self._锁:
            人格 = self._人格集[人格标识]
            旧状态 = 人格.状态
            人格.状态 = 人格状态.降级

            记录 = {
                "type": "persona:degraded",
                "人格": 人格标识,
                "旧状态": 旧状态.value,
                "新状态": 人格状态.降级.value,
                "原因": 原因,
                "时间戳": time.time()
            }

            if 人格标识 == "syncer":
                self._触发事件("syncer:degraded", 记录)

            self._记录历史(记录)
            self._状态变更次数 += 1

            return 记录

    def 人格恢复(self, 人格标识: str) -> Dict[str, Any]:
        """恢复人格到待机状态"""
        if 人格标识 not in self._人格集:
            raise ValueError(f"未知人格: {人格标识}")

        with self._锁:
            人格 = self._人格集[人格标识]

            if 人格标识 == "p72":
                return {"type": "persona:guard", "状态": "p72不可变更"}

            旧状态 = 人格.状态
            人格.状态 = 人格状态.待机
            人格.激活时间 = None

            if self._当前主导人格 == 人格标识:
                self._当前主导人格 = None

            记录 = {
                "type": "persona:recovered",
                "人格": 人格标识,
                "旧状态": 旧状态.value,
                "新状态": 人格状态.待机.value,
                "时间戳": time.time()
            }

            self._记录历史(记录)
            self._状态变更次数 += 1

            return 记录

    def 获取人格状态(self, 人格标识: Optional[str] = None) -> Dict[str, Any]:
        """
        获取人格状态

        Args:
            人格标识: 指定人格或None获取全部

        Returns:
            人格状态字典
        """
        with self._锁:
            if 人格标识:
                if 人格标识 not in self._人格集:
                    raise ValueError(f"未知人格: {人格标识}")
                return self._人格集[人格标识].到字典()
            return {k: v.到字典() for k, v in self._人格集.items()}

    # ═══════════════════════════════════════════════
    #  龍盾脉冲操作
    # ═══════════════════════════════════════════════

    def 脉冲(self, 状态数据: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        更新龍盾脉冲心跳

        Args:
            状态数据: 可选的附加状态数据

        Returns:
            脉冲记录
        """
        with self._锁:
            now = time.time()
            self._龍盾脉冲.心跳时间戳 = now
            self._脉冲次数 += 1

            # 检查宫格5密度（不动点校验）
            宫格5密度 = self._九宫密度[5]
            需要校正 = abs(宫格5密度 - 1.0) > 1e-9

            脉冲记录 = {
                "ts": now,
                "stability": self._龍盾脉冲.稳定指数,
                "density5": 宫格5密度,
                "sequence": self._脉冲次数
            }

            if 状态数据:
                脉冲记录["data"] = 状态数据

            if 需要校正:
                脉冲记录["correction"] = True
                脉冲记录["oldDensity5"] = 宫格5密度
                self._九宫密度[5] = 1.0  # 强制修复不动点
                self._龍盾脉冲.稳定指数 = max(0.0, self._龍盾脉冲.稳定指数 - 0.05)
                self._龍盾脉冲.上次校正 = now
                self._龍盾脉冲.校正次数 += 1
                self._merkle根哈希 = self._计算_merkle根()

                校正记录 = {
                    "type": "dragon:correction",
                    "不动点": 5,
                    "旧密度": 宫格5密度,
                    "新密度": 1.0,
                    "稳定指数": self._龍盾脉冲.稳定指数,
                    "校正次数": self._龍盾脉冲.校正次数,
                    "时间戳": now
                }
                self._记录历史(校正记录)
                self._触发事件("dragon:correction", 校正记录)
            else:
                # 正常心跳，缓慢恢复稳定
                self._龍盾脉冲.稳定指数 = min(1.0, self._龍盾脉冲.稳定指数 + 0.001)

            self._龍盾脉冲.脉冲序列.append(脉冲记录)

            self._触发事件("dragon:heartbeat", {
                "type": "dragon:heartbeat",
                "sequence": self._脉冲次数,
                "stability": self._龍盾脉冲.稳定指数,
                "时间戳": now
            })

            return {
                "type": "pulse",
                "心跳": now,
                "稳定指数": self._龍盾脉冲.稳定指数,
                "序列号": self._脉冲次数,
                "校正": 需要校正,
                "校正次数": self._龍盾脉冲.校正次数,
                "不动点": 5,
                "不动点密度": self._九宫密度[5]
            }

    def 龍盾校正(self) -> Dict[str, Any]:
        """
        手动触发龍盾校正 - 校验并修复所有不动点

        Returns:
            校正结果
        """
        with self._锁:
            校正结果 = {
                "type": "dragon:correction",
                "校正项": [],
                "时间戳": time.time()
            }

            # 宫格5为唯一不动点
            if abs(self._九宫密度[5] - 1.0) > 1e-9:
                旧值 = self._九宫密度[5]
                self._九宫密度[5] = 1.0
                校正结果["校正项"].append({
                    "宫格": 5,
                    "旧值": 旧值,
                    "新值": 1.0,
                    "类型": "不动点修复"
                })

            # 检查其他宫格是否在合法范围
            for 宫格 in range(1, 10):
                if 宫格 == 5:
                    continue
                密度 = self._九宫密度[宫格]
                if 密度 < 0.0 or 密度 > 1.0:
                    旧值 = 密度
                    新值 = max(0.0, min(1.0, 密度))
                    self._九宫密度[宫格] = 新值
                    校正结果["校正项"].append({
                        "宫格": 宫格,
                        "旧值": 旧值,
                        "新值": 新值,
                        "类型": "越界修复"
                    })

            if 校正结果["校正项"]:
                self._龍盾脉冲.上次校正 = time.time()
                self._龍盾脉冲.校正次数 += 1
                self._merkle根哈希 = self._计算_merkle根()

            return 校正结果

    # ═══════════════════════════════════════════════
    #  Merkle根哈希计算
    # ═══════════════════════════════════════════════

    def _计算初始_merkle根(self) -> str:
        """计算初始Merkle根"""
        return self._计算_merkle根()

    def _计算_merkle根(self) -> str:
        """
        计算九宫格密度的Merkle根哈希

        使用二叉Merkle树结构，宫格5为根节点左子树的核心
        """
        # 将所有宫格密度值转换为字符串并哈希
        叶节点 = []
        for 宫格 in range(1, 10):
            数据 = f"{宫格}:{self._九宫密度[宫格]:.10f}:{self.五行属性[宫格]}"
            叶哈希 = hashlib.sha256(数据.encode("utf-8")).hexdigest()
            叶节点.append(叶哈希)

        # 层级合并（Merkle树）
        def 合并层(节点列表: List[str]) -> List[str]:
            if len(节点列表) <= 1:
                return 节点列表
            上一层 = []
            for i in range(0, len(节点列表) - 1, 2):
                合并 = hashlib.sha256(
                    (节点列表[i] + 节点列表[i + 1]).encode("utf-8")
                ).hexdigest()
                上一层.append(合并)
            if len(节点列表) % 2 == 1:
                上一层.append(节点列表[-1])  # 奇数复制最后一个
            return 上一层

        当前层 = 叶节点[:]
        while len(当前层) > 1:
            当前层 = 合并层(当前层)

        return 当前层[0] if 当前层 else ""

    def 计算_merkle根(self) -> str:
        """公开方法：重新计算并返回Merkle根"""
        with self._锁:
            self._merkle根哈希 = self._计算_merkle根()
            return self._merkle根哈希

    # ═══════════════════════════════════════════════
    #  事件系统
    # ═══════════════════════════════════════════════

    def 注册监听器(self, 事件类型: str, 回调: Callable) -> None:
        """
        注册事件监听器

        Args:
            事件类型: 事件类型字符串
            回调: 回调函数(数据)
        """
        if 事件类型 not in self._事件监听器:
            self._事件监听器[事件类型] = []
        self._事件监听器[事件类型].append(回调)

    def 注销监听器(self, 事件类型: str, 回调: Callable) -> None:
        """注销事件监听器"""
        if 事件类型 in self._事件监听器:
            if 回调 in self._事件监听器[事件类型]:
                self._事件监听器[事件类型].remove(回调)

    def _触发事件(self, 事件类型: str, 数据: Dict[str, Any]) -> None:
        """内部：触发事件到所有监听器"""
        for 回调 in self._事件监听器.get(事件类型, []):
            try:
                回调(数据)
            except Exception as e:
                # 事件处理不应中断主流程
                print(f"[事件错误] {事件类型}: {e}")

    # ═══════════════════════════════════════════════
    #  历史记录
    # ═══════════════════════════════════════════════

    def _记录历史(self, 记录: Dict[str, Any]) -> None:
        """内部：记录到历史"""
        记录["_seq"] = self._状态变更次数
        self._历史记录.append(记录)

    def 获取历史(self, 数量: int = 100) -> List[Dict[str, Any]]:
        """
        获取最近历史记录

        Args:
            数量: 返回记录数量

        Returns:
            历史记录列表
        """
        with self._锁:
            return list(self._历史记录)[-数量:]

    # ═══════════════════════════════════════════════
    #  五行融合指数
    # ═══════════════════════════════════════════════

    def 计算五行平衡指数(self) -> Dict[str, Any]:
        """
        计算五行平衡指数（公式A）

        基于九宫格密度，按五行属性分组计算平衡度
        公式: 平衡指数 = 1 - (五行方差之和 / 5)

        Returns:
            五行平衡分析结果
        """
        with self._锁:
            五行分组: Dict[str, List[float]] = {"金": [], "木": [], "水": [], "火": [], "土": []}

            for 宫格 in range(1, 10):
                五行 = self.五行属性[宫格]
                五行分组[五行].append(self._九宫密度[宫格])

            五行均值 = {}
            五行方差 = {}

            for 五行, 值列表 in 五行分组.items():
                if 值列表:
                    均值 = sum(值列表) / len(值列表)
                    方差 = sum((v - 均值) ** 2 for v in 值列表) / len(值列表)
                    五行均值[五行] = 均值
                    五行方差[五行] = 方差

            总方差 = sum(五行方差.values())
            平衡指数 = max(0.0, 1.0 - 总方差 / 5.0)

            # 检查五行相克预警
            相克预警 = []
            相克关系 = [("金", "木"), ("木", "土"), ("土", "水"), ("水", "火"), ("火", "金")]
            for a, b in 相克关系:
                if a in 五行均值 and b in 五行均值:
                    差 = abs(五行均值[a] - 五行均值[b])
                    if 差 > 0.3:
                        相克预警.append(f"{a}克{b}: 偏差={差:.3f}")

            return {
                "五行均值": {k: round(v, 4) for k, v in 五行均值.items()},
                "五行方差": {k: round(v, 6) for k, v in 五行方差.items()},
                "总方差": round(总方差, 6),
                "平衡指数": round(平衡指数, 4),
                "平衡等级": "平衡" if 平衡指数 > 0.8 else "轻微失衡" if 平衡指数 > 0.5 else "严重失衡",
                "相克预警": 相克预警,
                "不动点贡献": {
                    "宫格5": {"密度": self._九宫密度[5], "五行": "土"}
                }
            }

    # ═══════════════════════════════════════════════
    #  流场摘要
    # ═══════════════════════════════════════════════

    def 获取流场摘要(self) -> Dict[str, Any]:
        """
        获取完整流场状态摘要（JSON可序列化）

        Returns:
            完整的状态摘要字典
        """
        with self._锁:
            now = time.time()
            运行时长 = now - self._初始化时间

            # 计算系统健康度
            整体审计色 = self.获取整体审计色()
            审计健康 = {"🟢": 1.0, "🟡": 0.5, "🔴": 0.0}[整体审计色]
            稳定健康 = self._龍盾脉冲.稳定指数

            # 密度均值（不含不动点）
            动态密度 = [self._九宫密度[i] for i in range(1, 10) if i != 5]
            密度均值 = sum(动态密度) / len(动态密度) if 动态密度 else 0.5

            系统健康度 = (审计健康 + 稳定健康 + 密度均值) / 3.0

            return {
                "meta": {
                    "version": self._版本,
                    "deviceId": self._设备标识,
                    "initializedAt": self._初始化时间,
                    "uptime": round(运行时长, 3),
                    "timestamp": now,
                },
                "天场": {
                    "auditField": self.审计天场,
                    "overall": 整体审计色,
                    "totalAudits": self._审计次数,
                    "auditFrequency": self._审计频率,
                },
                "地场": {
                    "merkleDensity": dict(self._九宫密度),
                    "merkleRoot": self._merkle根哈希,
                    "trends": dict(self._密度趋势),
                    "densityUpdates": self._密度更新次数,
                },
                "人场": {
                    "personas": {k: v.到字典() for k, v in self._人格集.items()},
                    "dominant": self._当前主导人格,
                    "fusionMode": self._人格融合模式,
                    "fusionList": self._融合人格列表,
                },
                "龍盾": self._龍盾脉冲.到字典(),
                "五行": self.计算五行平衡指数(),
                "五层": {
                    "directories": dict(self._五层目录),
                    "databases": dict(self._五层数据库),
                },
                "系统": {
                    "healthScore": round(系统健康度, 4),
                    "totalChanges": self._状态变更次数,
                    "historySize": len(self._历史记录),
                }
            }

    def 导出_json(self, 文件路径: Optional[str] = None) -> str:
        """
        导出流场状态为JSON字符串

        Args:
            文件路径: 可选的保存路径

        Returns:
            JSON字符串
        """
        摘要 = self.获取流场摘要()
        json字符串 = json.dumps(摘要, ensure_ascii=False, indent=2, default=str)

        if 文件路径:
            with open(文件路径, "w", encoding="utf-8") as f:
                f.write(json字符串)

        return json字符串

    def __repr__(self) -> str:
        审计色 = self.获取整体审计色()
        return (
            f"流场状态(v{self._版本} | "
            f"天场{审计色} | "
            f"地场根{self._merkle根哈希[:8]}... | "
            f"人场主导:{self._当前主导人格 or '无'} | "
            f"龍盾稳{self._龍盾脉冲.稳定指数:.3f})"
        )

    def __str__(self) -> str:
        return self.__repr__()


# ═══════════════════════════════════════════════
#  工厂函数与快捷入口
# ═══════════════════════════════════════════════

def 创建流场状态(设备标识: str = "UID9622") -> 流场状态:
    """工厂函数：创建新的流场状态实例"""
    return 流场状态(设备标识=设备标识)


def 流场自检测() -> Dict[str, Any]:
    """系统自检：验证流场状态完整性"""
    结果 = {
        "测试": "流场状态自检",
        "时间": time.time(),
        "项目": []
    }

    try:
        流场 = 创建流场状态()

        # 测试1: 初始状态
        密度 = 流场.九宫密度
        assert 密度[5] == 1.0, "宫格5不动点失败"
        assert all(密度[i] == 0.5 for i in [1, 2, 3, 4, 6, 7, 8, 9]), "初始密度不一致"
        结果["项目"].append({"name": "初始状态", "status": "通过"})

        # 测试2: 密度更新
        流场.更新密度(1, 0.8)
        assert 流场.九宫密度[1] == 0.8, "密度更新失败"
        结果["项目"].append({"name": "密度更新", "status": "通过"})

        # 测试3: 不动点保护
        try:
            流场.更新密度(5, 0.5)
            结果["项目"].append({"name": "不动点保护", "status": "失败-未触发异常"})
        except ValueError:
            结果["项目"].append({"name": "不动点保护", "status": "通过"})

        # 测试4: 审计更新
        流场.审计("整体", "🟡")
        assert 流场.获取整体审计色() == "🟡", "审计更新失败"
        结果["项目"].append({"name": "审计更新", "status": "通过"})

        # 测试5: 脉冲
        脉冲结果 = 流场.脉冲()
        assert 脉冲结果["稳定指数"] > 0, "脉冲失败"
        结果["项目"].append({"name": "龍盾脉冲", "status": "通过"})

        # 测试6: 人格激活
        流场.激活人格("wenwen")
        assert 流场.当前主导人格 == "wenwen", "人格激活失败"
        结果["项目"].append({"name": "人格激活", "status": "通过"})

        # 测试7: Merkle根
        根 = 流场.计算_merkle根()
        assert len(根) == 64, "Merkle根格式错误"
        结果["项目"].append({"name": "Merkle根", "status": "通过"})

        # 测试8: 流场摘要
        摘要 = 流场.获取流场摘要()
        assert "天场" in 摘要 and "地场" in 摘要 and "人场" in 摘要, "摘要不完整"
        结果["项目"].append({"name": "流场摘要", "status": "通过"})

        # 测试9: 五行平衡
        五行 = 流场.计算五行平衡指数()
        assert "平衡指数" in 五行, "五行平衡计算失败"
        结果["项目"].append({"name": "五行平衡", "status": "通过"})

        # 测试10: JSON序列化
        json字符串 = 流场.导出_json()
        import json
        解析 = json.loads(json字符串)
        assert "meta" in 解析, "JSON序列化失败"
        结果["项目"].append({"name": "JSON序列化", "status": "通过"})

        结果["总结果"] = "全部通过"

    except Exception as e:
        结果["总结果"] = f"失败: {str(e)}"
        结果["项目"].append({"name": "异常", "status": str(e)})

    return 结果


# ═══════════════════════════════════════════════
#  命令行入口
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("三才流场MCP引擎v4.0 - 状态容器")
    print("=" * 60)
    print()

    # 运行自检
    print("[1/2] 执行系统自检...")
    自检结果 = 流场自检测()
    for 项目 in 自检结果["项目"]:
        状态 = "✅" if 项目["status"] == "通过" else "❌"
        print(f"  {状态} {项目['name']}")
    print(f"\n  总结果: {自检结果['总结果']}")
    print()

    # 演示完整功能
    print("[2/2] 演示流场状态...")
    流场 = 创建流场状态()

    # 模拟一些操作
    流场.更新密度(1, 0.75)
    流场.更新密度(3, 0.9)
    流场.更新密度(9, 0.3)
    流场.审计("平衡", "🟡")
    流场.激活人格("scout")
    流场.脉冲()

    # 打印摘要
    摘要 = 流场.获取流场摘要()
    print(f"\n  系统版本: {摘要['meta']['version']}")
    print(f"  设备标识: {摘要['meta']['deviceId']}")
    print(f"  系统健康: {摘要['系统']['healthScore']}")
    print(f"  天场审计: {摘要['天场']['overall']}")
    print(f"  主导人格: {摘要['人场']['dominant']}")
    print(f"  龍盾稳定: {摘要['龍盾']['stability']}")
    print(f"  Merkle根: {摘要['地场']['merkleRoot'][:16]}...")
    print(f"  五行平衡: {摘要['五行']['平衡指数']} ({摘要['五行']['平衡等级']})")
    print(f"\n  五层设备:")
    for 层, 目录 in 摘要['五层']['directories'].items():
        print(f"    {层} → {目录}")

    print(f"\n{'=' * 60}")
    print(f"DNA: #龍芯⚡️2026-06-09-三才流场-FlowFieldState-v4.0")
    print(f"{'=' * 60}")
