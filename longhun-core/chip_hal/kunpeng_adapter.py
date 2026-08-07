#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-ADAPTER-KUNPENG-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
"""
龍魂·鲲鹏适配器 · 华为鲲鹏920系列
ARMv8.2+ · 内置Da Vinci加速器 · 国密SM3/SM4硬件加速

编译标志: -march=armv8.2-a+fp16+rcpc+dotprod+sm3+sm4
优化: 鲲鹏加速库 KAE (Kunpeng Accelerator Engine)
"""

import os
import platform
from dataclasses import dataclass
from typing import Optional


@dataclass
class KunpengConfig:
    """鲲鹏优化配置"""
    arch: str = "armv8.2-a"
    march_flags: str = "-march=armv8.2-a+fp16+rcpc+dotprod"
    crypto_flags: str = "+sm3+sm4+aes+sha2"
    simd_flags: str = "+asimd"
    lib_paths: list = None
    kae_enabled: bool = False

    def __post_init__(self):
        if self.lib_paths is None:
            self.lib_paths = [
                "/usr/local/kunpeng/lib",
                "/opt/kunpeng/lib",
                "/usr/lib64",
            ]


class KunpengAdapter:
    """鲲鹏适配器 · 编译优化 + 加速库检测"""

    def __init__(self):
        self.config = KunpengConfig()
        self._detect_kae()

    def _detect_kae(self):
        """检测鲲鹏加速引擎 KAE"""
        kae_paths = [
            "/usr/local/lib/libkae.so",
            "/usr/lib64/libkae.so",
            "/opt/kunpeng/lib/libkae.so",
        ]
        for path in kae_paths:
            if os.path.exists(path):
                self.config.kae_enabled = True
                return

    def get_compile_flags(self) -> str:
        """获取最佳编译标志"""
        flags = self.config.march_flags + self.config.crypto_flags + self.config.simd_flags
        return flags

    def get_env_vars(self) -> dict:
        """获取环境变量"""
        env = {}
        env["LD_LIBRARY_PATH"] = ":".join(
            p for p in self.config.lib_paths if os.path.exists(p)
        )
        if self.config.kae_enabled:
            env["KAE_ENABLED"] = "1"
        return env

    def is_supported(self) -> bool:
        """当前环境是否为鲲鹏"""
        machine = platform.machine()
        return machine in ("aarch64", "arm64")

    def get_docker_base_image(self) -> str:
        """推荐 Docker 基础镜像"""
        return "arm64v8/python:3.12-slim"

    def __repr__(self):
        return f"KunpengAdapter(kae={self.config.kae_enabled}, march={self.config.march_flags})"
