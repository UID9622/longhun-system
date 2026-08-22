#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""🐉 P02 张衡 · 数学引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·甲寅·申时·䷼中孚-P02-MATH-ENGINE-v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

职责: 数字根验证 · 河图洛书权重校准 · 五行矩阵评分 · DNA链完整性校验
自产自销: P01推演→P02数学校准→P06验证→P04落地→回流案例库
IPA路由: IPA-L7-PER-KNOW-007 → 回调 calibrated_weights + dr_chain + wuxing_matrix

三引擎:
  - digital_root_engine.py: 数字根计算 + 数字根链校验 + 洛书369不动点
  - hetu_luoshu_calibrator.py: 河图洛书权重校准 + 中五不动点 + 矩阵变换
  - wuxing_matrix.py: 五行矩阵评分 + 生克动态 + WBI/GRS/SBC诊断
"""
# P02 数学引擎统一入口
from .digital_root_engine import DigitalRootEngine, DRConfig as DigitalRootConfig, DRChain, dr_range, DRLevel
from .hetu_luoshu_calibrator import HetuLuoshuCalibrator, CalibrationConfig, WeightCalibration, 中五不动点, 河图矩阵, 洛书矩阵
from .wuxing_matrix import WuxingMatrix, MatrixConfig, MatrixScore, 五行常量

__all__ = [
    # 数字根
    "DigitalRootEngine", "DigitalRootConfig", "DRChain", "dr_range", "DRLevel",
    # 河图洛书
    "HetuLuoshuCalibrator", "CalibrationConfig", "WeightCalibration", "中五不动点", "河图矩阵", "洛书矩阵",
    # 五行矩阵
    "WuxingMatrix", "MatrixConfig", "MatrixScore", "五行常量",
]

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·申时·䷔噬嗑-CONFIRM-SEAL-__init__-B3444E35
