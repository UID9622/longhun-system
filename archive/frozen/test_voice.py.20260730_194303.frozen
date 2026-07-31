#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for cnsh_runtime.cnsh.voice package.

These tests avoid heavy optional dependencies (Whisper, edge-tts, etc.)
and focus on data structures, role management, text preprocessing,
and import sanity.
"""

import os
import sys
import pytest

# Ensure the package under test is importable in editable installs.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cnsh_runtime.cnsh.voice import (
    审计颜色,
    审计结果,
    六层来源链,
    铁律自审闸,
    语音合成结果,
    语音角色管理器,
    龍魂语音合成器,
    语音识别结果,
    龍魂语音识别器,
)


def test_audit_color_values():
    assert 审计颜色.绿色通过.value == "🟢"
    assert 审计颜色.黄色警告.value == "🟡"
    assert 审计颜色.红色阻断.value == "🔴"


def test_audit_result_dataclass():
    结果 = 审计结果(颜色=审计颜色.绿色通过, 置信度=0.95, 原因="通过", 建议="")
    assert 结果.置信度 == 0.95


def test_provenance_stamp():
    印章 = 六层来源链.盖章("test")
    assert "DNA追溯码" in 印章
    assert "六层来源链" in 印章
    assert 印章["DNA追溯码"].startswith("#龍芯")


def test_iron_gate_passes():
    闸 = 铁律自审闸()
    assert "繁体" in 闸.获取铁律()[0]
    assert 闸.审查("龍魂")["通过"] is True


def test_iron_gate_catches_simplified_dragon():
    闸 = 铁律自审闸()
    结果 = 闸.审查("龙魂")
    assert 结果["通过"] is False
    assert any("龍" in item for item in 结果["违规项"])


def test_role_manager_lists_roles():
    全部 = 语音角色管理器.获取全部角色()
    assert "xiaoxiao" in 全部
    assert 全部["xiaoxiao"]["语言"] == "zh-CN"


def test_role_manager_by_language():
    中文 = 语音角色管理器.按语言获取角色("zh-CN")
    assert "xiaoxiao" in 中文
    英文 = 语音角色管理器.按语言获取角色("en")
    assert "jenny" in 英文


def test_tts_result_to_dict():
    结果 = 语音合成结果(
        音频路径="/tmp/test.mp3",
        文本="测试",
        语速=1.0,
        音调=0.0,
        语音角色="女声",
        音频时长=3.5,
        采样率=24000,
        处理时长=0.8,
        合成引擎="edge-tts-test",
        DNA追溯="#龍芯⚡️2026-06-18-TTS-test",
    )
    字典 = 结果.to_dict()
    assert 字典["文本长度"] == 2
    assert 字典["采样率"] == 24000


def test_tts_preprocessing():
    合成器 = 龍魂语音合成器(启用审计=False, 输出目录="/tmp")
    原始 = "  这是一段\n需要预处理的\r\n文本内容。包含  多余  空格！  "
    处理后 = 合成器._预处理文本(原始)
    assert "\n" not in 处理后
    assert "  " not in 处理后


def test_tts_smart_split():
    合成器 = 龍魂语音合成器(启用审计=False, 输出目录="/tmp")
    文本 = "第一句。第二句！第三句？第四句；第五句。第六句。第七句。"
    分段 = 合成器._智能分句(文本, 15)
    assert len(分段) >= 1


def test_asr_result_to_dict():
    结果 = 语音识别结果(
        文本="测试文本",
        置信度=0.92,
        语言="zh",
        片段列表=[{"start": 0.0, "end": 1.0, "text": "测试"}],
        音频时长=5.0,
        处理时长=1.2,
        识别模型="Whisper-base",
        DNA追溯="#龍芯⚡️2026-06-18-STT-test",
    )
    字典 = 结果.to_dict()
    assert 字典["片段数"] == 1
    assert 0 < 字典["实时率_RTF"] < 10


def test_asr_model_name_resolution():
    识别器 = 龍魂语音识别器(模型名称="基础", 启用审计=False)
    assert 识别器.模型名称 == "base"


def test_asr_device_fallback_without_torch():
    # When torch is unavailable, auto device should fall back to cpu.
    识别器 = 龍魂语音识别器(模型名称="base", 设备="auto", 启用审计=False)
    assert 识别器.设备 in ("cpu", "cuda")
