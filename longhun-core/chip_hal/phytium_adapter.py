#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-ADAPTER-PHYTIUM-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
"""
龍魂·飞腾适配器 · 天津飞腾 FT2000+/S2500/D2000
ARMv8 · 国产服务器芯片
"""

import platform
from dataclasses import dataclass


@dataclass
class PhytiumConfig:
    """飞腾优化配置"""
    arch: str = "armv8-a"
    march_flags: str = "-march=armv8-a+crc+crypto"
    simd_flags: str = "+asimd"
    cores: int = 0


class PhytiumAdapter:
    """飞腾适配器"""

    def __init__(self):
        self.config = PhytiumConfig()

    def get_compile_flags(self) -> str:
        return self.config.march_flags + self.config.simd_flags

    def get_docker_base_image(self) -> str:
        return "arm64v8/python:3.12-slim"

    def is_supported(self) -> bool:
        return platform.machine() in ("aarch64", "arm64")

    def __repr__(self):
        return f"PhytiumAdapter(march={self.config.march_flags})"
