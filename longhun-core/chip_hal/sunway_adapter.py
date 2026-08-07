#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-ADAPTER-SUNWAY-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
"""
龍魂·申威适配器 · 无锡超级计算中心 SW26010/SW1621
Sunway64 · 超算级别 · 神威·太湖之光同源
"""

import platform
from dataclasses import dataclass


@dataclass
class SunwayConfig:
    """申威优化配置"""
    arch: str = "sw26010"
    march_flags: str = "-march=sw26010"
    simd_flags: str = "+simd"


class SunwayAdapter:
    """申威适配器"""

    def __init__(self):
        self.config = SunwayConfig()

    def get_compile_flags(self) -> str:
        return self.config.march_flags + self.config.simd_flags

    def get_docker_base_image(self) -> str:
        return "swr.cn-east-2.myhuaweicloud.com/swamd/swamd:latest"

    def is_supported(self) -> bool:
        return platform.machine() in ("sw_64", "sunway")

    def __repr__(self):
        return f"SunwayAdapter(arch={self.config.arch})"
