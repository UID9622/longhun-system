#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-ADAPTER-APPLE-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
"""
龍魂·Apple Silicon适配器 · M1/M2/M3 系列
ARMv8.5+ · 统一内存架构(UMA) · Neural Engine · 本地开发主力
"""

import os
import platform
import subprocess
import sys
from dataclasses import dataclass


@dataclass
class AppleSiliconConfig:
    """Apple Silicon配置"""
    arch: str = "arm64"
    chip_model: str = ""
    memory_gb: int = 0
    neural_engine: bool = True  # M系列都有 Neural Engine
    gpu_cores: int = 0
    unified_memory: bool = True


class AppleSiliconAdapter:
    """Apple Silicon适配器 · M1/M2/M3本地开发"""

    def __init__(self):
        self.config = AppleSiliconConfig()
        self._detect_chip()

    def _detect_chip(self):
        """通过 sysctl 检测具体型号"""
        try:
            brand = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True, text=True
            ).stdout.strip()
            self.config.chip_model = brand
            
            # 内存
            mem = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True, text=True
            ).stdout.strip()
            if mem:
                self.config.memory_gb = int(mem) // (1024**3)
            
            # GPU 核心
            gpu = subprocess.run(
                ["sysctl", "-n", "hw.perflevel0.logicalcpu"],
                capture_output=True, text=True
            ).stdout.strip()
            if gpu:
                self.config.gpu_cores = int(gpu)
        except Exception:
            pass

    def get_compile_flags(self) -> str:
        return "-march=armv8.5-a+fp16+rcpc+dotprod+i8mm+bf16"

    def get_docker_base_image(self) -> str:
        return "arm64v8/python:3.12-slim"

    def is_supported(self) -> bool:
        return sys.platform == "darwin" and platform.machine() == "arm64"

    def is_development(self) -> bool:
        """是否为本地开发环境"""
        return self.is_supported()

    def __repr__(self):
        return (f"AppleSiliconAdapter({self.config.chip_model}, "
                f"{self.config.memory_gb}GB, "
                f"NE={self.config.neural_engine})")
