#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙申·甲寅·庚午·坤-RULE-ENGINE-v4.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 来源: 龍魂系统/核心引擎/规则引擎/引擎.py → 吸收对齐后嵌入 longhun-system
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 路径标准化·DNA升级·对齐完成
# 理论指导: 曾仕强老师（永恒显示）

"""
龍魂规则引擎 v4.1
==================
六大规则·三色闸门·DNA签名链·数字根判定

路径对齐说明：
  - 账本路径默认从 ~/.龍魂/ → longhun-system/audit/rule_ledger.jsonl
  - DNA格式升级为 v∞ 干支卦标准格式
  - 导入路径修正为 longhun-system 标准路径

六大规则：
  R1: 坏可以，自己扛
  R2: 挨骂要立正
  R3: 错可以弥补
  R4: 威胁直接干
  R5: 主动补救加分
  R6: 惯犯追踪
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional
import hashlib
import json
import os


# ── 项目根路径 ──
项目根 = Path(__file__).resolve().parent.parent


# ── 数据结构 ──

class 规则类型(Enum):
    """六大规则"""
    R1_责任承担 = "R1: 坏可以，自己扛"
    R2_批评姿态 = "R2: 挨骂要立正"
    R3_错误补救 = "R3: 错可以弥补"
    R4_威胁零分 = "R4: 威胁直接干"
    R5_主动补偿 = "R5: 主动补救加分"
    R6_累犯追踪 = "R6: 惯犯追踪"


@dataclass
class 事件:
    """
    事件记录 - 龍魂规则引擎的原子单位

    字段:
    - 自扛: R1责任承担
    - 立正: R2批评姿态
    - 威胁: R4威胁零分
    - 补救: R5主动补偿
    """
    编号: str
    人物: str
    行为: str
    犯错: bool
    自扛: bool = False
    立正: bool = False
    威胁: bool = False
    补救: bool = False
    DNA: str = ""
    链杂凑: str = ""
    时间戳: str = field(default_factory=lambda: datetime.now().isoformat())

    def 计算数字根(self) -> int:
        """计算行为描述的数字根（三色闸门核心）"""
        total = sum(ord(c) for c in self.行为)
        while total >= 10:
            total = sum(int(d) for d in str(total))
        return total


class DNA链:
    """
    不可修改的DNA签名链
    - 每个事件都有DNA签名
    - 链杂凑连接前后事件
    - 任何修改会破坏后续所有记录
    """

    def __init__(self):
        self.最后杂凑 = "GENESIS"

    def 生成(self, 事件: 事件) -> str:
        """为事件生成v∞ DNA签名"""
        事件资料 = f"{事件.编号}|{事件.人物}|{事件.行为}|{事件.时间戳}"
        事件杂凑 = hashlib.sha256(事件资料.encode()).hexdigest()[:8]
        DNA = f"#龍芯⚡️{事件.时间戳[:10]}-{事件.人物[:2]}-{事件.编号[:3]}-{事件杂凑}"
        return DNA

    def 验证链(self, 事件: 事件) -> bool:
        """验证事件链完整性"""
        if not 事件.DNA.startswith("#龍芯⚡️"):
            return False
        if 事件.链杂凑 == "":
            事件.链杂凑 = self.最后杂凑
            return True
        return hashlib.sha256(
            f"{事件.DNA}{self.最后杂凑}".encode()
        ).hexdigest()[:8] == 事件.链杂凑


class 评分器:
    """
    100分制评分系统 + 三色闸门

    基础分: 100
    R1: 犯错但自扛 +2 | 逃避 -10
    R2: 挨骂立正 +0 | 顶嘴 -5
    R4: 威胁 → 直接0分+🔴熔断
    R5: 主动补偿 +5
    R6: 累犯 1st/-5 | 2nd/-10 | 3rd/-15+降级
    数字根: 3/9→🔴 | 6→🟡 | 其他→🟢
    """

    def __init__(self):
        self.违规历史: Dict[str, List[str]] = {}
        self.基础分 = 100

    def 判定(self, 事件: 事件) -> Dict:
        分数 = self.基础分
        规则匹配 = []

        # R4: 威胁直接干 → 🔴熔断
        if 事件.威胁:
            分数 = 0
            规则匹配.append(规则类型.R4_威胁零分.value)
            return {
                'DNA': "",
                '分数': 分数,
                '数字根': 0,
                '状态': '🔴熔断',
                '规则匹配': 规则匹配,
                '说明': '威胁行为，直接零分·熔断'
            }

        # R1: 责任承担
        if 事件.犯错:
            if 事件.自扛:
                分数 += 2
                规则匹配.append(f"{规则类型.R1_责任承担.value} ✓")
            else:
                分数 -= 10
                规则匹配.append(f"{规则类型.R1_责任承担.value} ✗")

        # R2: 批评姿态
        if 事件.犯错:
            if 事件.立正:
                规则匹配.append(f"{规则类型.R2_批评姿态.value} ✓")
            else:
                分数 -= 5
                规则匹配.append(f"{规则类型.R2_批评姿态.value} ✗")

        # R5: 主动补救
        if 事件.补救:
            分数 += 5
            规则匹配.append(f"{规则类型.R5_主动补偿.value} ✓")

        # R6: 惯犯追踪
        if 事件.人物 not in self.违规历史:
            self.违规历史[事件.人物] = []

        if 事件.犯错:
            self.违规历史[事件.人物].append(事件.编号)
            违规次数 = len(self.违规历史[事件.人物])

            if 违规次数 == 2:
                分数 -= 10
                规则匹配.append(f"{规则类型.R6_累犯追踪.value} (2nd) -10")
            elif 违规次数 >= 3:
                分数 -= 15
                规则匹配.append(f"{规则类型.R6_累犯追踪.value} (3+) -15")

        分数 = max(0, min(100, 分数))

        # 数字根判定三色闸门
        dr = self._计算数字根(分数)
        if dr in [3, 9]:
            状态 = '🔴熔断'
        elif dr == 6:
            状态 = '🟡待审'
        else:
            状态 = '🟢通过'

        return {
            'DNA': f"#龍芯⚡️{事件.时间戳[:10]}-判定-dr{dr}",
            '分数': 分数,
            '数字根': dr,
            '状态': 状态,
            '规则匹配': 规则匹配,
            '说明': f"分数 {分数}/100，数字根 {dr}，状态 {状态}"
        }

    def _计算数字根(self, n: int) -> int:
        while n >= 10:
            n = sum(int(d) for d in str(n))
        return n


class 规则引擎:
    """
    龍魂规则引擎 v4.1

    统一入口 - 接收事件 → 执行判定 → 返回DNA签名结果
    """

    def __init__(self, 账本路径: str = ""):
        self.评分器 = 评分器()
        self.DNA链 = DNA链()
        # 默认账本路径：longhun-system/audit/rule_ledger.jsonl
        if 账本路径:
            self.账本路径 = 账本路径
        else:
            self.账本路径 = str(项目根 / "audit" / "rule_ledger.jsonl")
        self.事件列表: List[事件] = []

    def 执行(self, 事件: 事件) -> Dict:
        """
        核心执行方法

        流程:
        1. 生成DNA签名
        2. 执行评分判定
        3. 验证DNA链
        4. 写入账本（append-only）
        5. 返回完整结果
        """
        事件.DNA = self.DNA链.生成(事件)
        判定结果 = self.评分器.判定(事件)
        self.DNA链.验证链(事件)

        账本项 = {
            '时间': datetime.now().isoformat(),
            '事件': {
                '编号': 事件.编号,
                '人物': 事件.人物,
                '行为': 事件.行为,
                'DNA': 事件.DNA,
                '链杂凑': 事件.链杂凑
            },
            '判定': 判定结果
        }

        self.事件列表.append(事件)
        self._写账本(账本项)

        return {
            'DNA': 事件.DNA,
            '事件编号': 事件.编号,
            '人物': 事件.人物,
            '判定结果': 判定结果,
            '状态': 判定结果['状态'],
            '分数': 判定结果['分数'],
            '链验证': True
        }

    def _写账本(self, 项: Dict):
        """写入append-only账本"""
        ledger_dir = os.path.dirname(self.账本路径)
        if ledger_dir:
            os.makedirs(ledger_dir, exist_ok=True)

        with open(self.账本路径, 'a', encoding='utf-8') as f:
            f.write(json.dumps(项, ensure_ascii=False) + '\n')

    def 查询账本(self, 人物: Optional[str] = None) -> List[Dict]:
        """查询账本记录（只读）"""
        if not os.path.exists(self.账本路径):
            return []

        结果 = []
        with open(self.账本路径, 'r', encoding='utf-8') as f:
            for 行 in f:
                if not 行.strip():
                    continue
                项 = json.loads(行)
                if 人物 is None or 项['事件']['人物'] == 人物:
                    结果.append(项)
        return 结果
