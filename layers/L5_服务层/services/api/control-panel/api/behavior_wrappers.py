#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# #龍芯⚡️2026-07-03-ENGINE-BEHAVIOR_WRAPPERS-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂公民画像引擎 Web 操作台封装
提供行为记录、亮灯控制、画像查询的统一接口
"""
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# 将技能脚本加入路径
SKILL_SCRIPTS = Path.home() / ".kimi-code" / "skills" / "longhun-behavior-engine" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

try:
    from 公民画像引擎 import 公民画像引擎
except Exception as e:
    raise ImportError(f"无法加载公民画像引擎: {e}") from e


def _引擎(用户ID: str) -> 公民画像引擎:
    return 公民画像引擎(用户ID)


def 获取画像(用户ID: str) -> Dict[str, Any]:
    """返回用户六大维度分数、亮灯设置与行为统计。"""
    return _引擎(用户ID).计算六大维度()


def 获取亮灯展示(用户ID: str) -> str:
    """返回用户选择对外展示的亮灯信息（文本）。"""
    return _引擎(用户ID).获取亮灯展示()


def 记录行为(
    用户ID: str,
    类型: str,
    名称: str,
    权重: Optional[float] = None,
    真实度: Optional[float] = None,
    连续天数: Optional[int] = None,
) -> Dict[str, Any]:
    """
    记录一条行为。
    类型: 环保 / 信誉 / 互动 / 服务 / 习惯
    """
    引擎 = _引擎(用户ID)
    类型 = 类型.strip()
    if 类型 == "环保":
        消息 = 引擎.记录环保行为(名称, 权重 or 1.0)
    elif 类型 == "信誉":
        消息 = 引擎.记录信誉行为(名称, 权重 or 2.0, 真实度 or 1.0)
    elif 类型 == "互动":
        消息 = 引擎.记录互动质量(名称, 权重 or 0.5, 真实度 or 0.8)
    elif 类型 == "服务":
        消息 = 引擎.记录服务行为(名称, 权重 or 5.0)
    elif 类型 == "习惯":
        消息 = 引擎.记录习惯(名称, 连续天数 or 1)
    else:
        raise ValueError(f"不支持的行为类型: {类型}，可选：环保/信誉/互动/服务/习惯")

    return {
        "状态": "success",
        "用户ID": 用户ID,
        "类型": 类型,
        "消息": 消息,
        "画像": 引擎.计算六大维度(),
    }


def 设置亮灯(用户ID: str, 维度: str, 开关: bool) -> Dict[str, Any]:
    """设置某维度是否对外亮灯。"""
    引擎 = _引擎(用户ID)
    消息 = 引擎.设置亮灯(维度, 开关)
    return {
        "状态": "success",
        "用户ID": 用户ID,
        "维度": 维度,
        "开关": 开关,
        "消息": 消息,
        "画像": 引擎.计算六大维度(),
    }
