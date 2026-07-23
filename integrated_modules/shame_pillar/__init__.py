#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · AI行为约束耻辱柱模块
DNA: #龍芯⚡️2026-07-04-SHAME-PILLAR-MODULE-v1.0

本模块提供基于责任塌缩概率模型的 AI 行为约束引擎，包括：
- 耻辱柱核心引擎（R 值计算、越界检测、惩罚执行）
- 六誓引擎（6 条数学不变式检查）
- 权限-R 阈值分级
- 极端态熔断协议

入口：
    from shame_pillar.shame_pillar_core import 耻辱柱核心引擎, 七因子输入
    引擎 = 耻辱柱核心引擎()
    结果 = 引擎.处理(七因子输入(...))

命令行自检：
    python3 -m shame_pillar.shame_pillar_core
"""

from .shame_pillar_core import (
    七因子输入,
    三色状态,
    人格类型,
    越界类型,
    惩罚等级,
    耻辱柱核心引擎,
)

__all__ = [
    "七因子输入",
    "三色状态",
    "人格类型",
    "越界类型",
    "惩罚等级",
    "耻辱柱核心引擎",
]
