#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-ADAPTER-LOONGSON-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
"""
龍魂·龍芯适配器 · 中科院龍芯3A5000/3A6000
LoongArch · 完全自主指令集架构 · LA464 微架构
"""

import platform
from dataclasses import dataclass


@dataclass
class LoongsonConfig:
    """龍芯优化配置"""
    arch: str = "loongarch64"
    march_flags: str = "-march=loongarch64"
    abi: str = "lp64d"  # LP64 + double float
    binaries: str = "loong64"


class LoongsonAdapter:
    """龍芯适配器"""

    def __init__(self):
        self.config = LoongsonConfig()

    def get_compile_flags(self) -> str:
        return f"{self.config.march_flags} -mabi={self.config.abi}"

    def get_docker_base_image(self) -> str:
        return "loongson/loongnix-server:latest"

    def is_supported(self) -> bool:
        return platform.machine() in ("loongarch64", "loongarch32")

    def __repr__(self):
        return f"LoongsonAdapter(arch={self.config.arch}, abi={self.config.abi})"
