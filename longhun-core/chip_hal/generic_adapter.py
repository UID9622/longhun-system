#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-ADAPTER-GENERIC-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
"""
龍魂·通用适配器 · 降级兜底
当芯片无法被前6个适配器识别时使用最安全的基础配置
"""

import platform
from dataclasses import dataclass


@dataclass
class GenericConfig:
    """通用配置（最安全基线）"""
    arch: str = ""
    march_flags: str = ""
    docker_image: str = "python:3.12-slim"


class GenericAdapter:
    """通用适配器 · 兜底降级"""

    def __init__(self):
        self.config = GenericConfig()
        self._auto_detect()

    def _auto_detect(self):
        machine = platform.machine()
        if machine in ("aarch64", "arm64"):
            self.config.arch = "arm64"
            self.config.march_flags = "-march=armv8-a"
            self.config.docker_image = "arm64v8/python:3.12-slim"
        elif machine in ("x86_64", "amd64"):
            self.config.arch = "x86_64"
            self.config.march_flags = "-march=x86-64-v2"
            self.config.docker_image = "python:3.12-slim"
        elif "loongarch" in machine:
            self.config.arch = "loongarch64"
            self.config.march_flags = "-march=loongarch64"
            self.config.docker_image = "loongson/loongnix-server:latest"
        else:
            self.config.arch = machine
            self.config.march_flags = ""
            self.config.docker_image = "python:3.12-slim"

    def get_compile_flags(self) -> str:
        return self.config.march_flags

    def get_docker_base_image(self) -> str:
        return self.config.docker_image

    def is_supported(self) -> bool:
        return True  # 永远兜底

    def __repr__(self):
        return f"GenericAdapter(arch={self.config.arch})"
