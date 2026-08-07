#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-ADAPTER-ASCEND-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
"""
龍魂·昇腾适配器 · 华为昇腾310/910系列
CANN计算架构 · NPU AI推理加速
"""

import os
from dataclasses import dataclass, field
from typing import List, Optional
try:
    from .ascend_npu import AscendNpuDetector, NpuStatus
except ImportError:
    from chip_hal.ascend_npu import AscendNpuDetector, NpuStatus


@dataclass
class AscendConfig:
    """昇腾优化配置"""
    ascend_home: str = "/usr/local/Ascend"
    npu_type: str = ""
    chip_count: int = 0
    total_memory_mb: int = 0
    toolkit_version: str = ""
    env_sourced: bool = False
    cann_paths: List[str] = field(default_factory=list)


class AscendAdapter:
    """昇腾适配器 · CANN 环境管理 + PyTorch适配"""

    def __init__(self):
        self.config = AscendConfig()
        self.npu_detector = AscendNpuDetector()
        self.npu_status: Optional[NpuStatus] = None
        self._init_status()

    def _init_status(self):
        self.npu_status = self.npu_detector.detect()
        if self.npu_status.available:
            self.config.npu_type = self.npu_status.npu_type.value
            self.config.chip_count = self.npu_status.chip_count
            self.config.total_memory_mb = self.npu_status.total_memory_mb
            self.config.toolkit_version = self.npu_status.driver_version
            self._discover_cann_paths()

    def _discover_cann_paths(self):
        """发现 CANN 安装路径"""
        ascend_home = self.config.ascend_home
        if os.path.isdir(ascend_home):
            for item in os.listdir(ascend_home):
                full = os.path.join(ascend_home, item)
                if os.path.isdir(full):
                    self.config.cann_paths.append(full)

    def source_env(self) -> dict:
        """生成 CANN 环境变量（不实际 source，返回 dict 供后续使用）"""
        env = {}
        ascend_home = self.config.ascend_home
        
        if not os.path.isdir(ascend_home):
            return env
        
        env["ASCEND_HOME"] = ascend_home
        env["LD_LIBRARY_PATH"] = os.pathsep.join([
            f"{ascend_home}/driver/lib64",
            f"{ascend_home}/nnae/latest/lib64",
        ])
        env["PATH"] = os.pathsep.join([
            f"{ascend_home}/toolkit/latest/compiler/ccec_compiler/bin",
            f"{ascend_home}/toolkit/latest/compiler/bin",
            os.environ.get("PATH", ""),
        ])
        env["PYTHONPATH"] = os.pathsep.join([
            f"{ascend_home}/nnae/latest/opp/op_impl/built-in/ai_core/tbe",
            os.environ.get("PYTHONPATH", ""),
        ])
        
        self.config.env_sourced = True
        return env

    def get_docker_base_image(self) -> str:
        """推荐 Docker 基础镜像"""
        return "ascendhub/ascend-pytorch:latest"  # 华为昇腾官方镜像

    def get_torch_device(self) -> str:
        """获取 PyTorch 设备字符串"""
        if self.npu_status and self.npu_status.torch_npu_available:
            return "npu:0"
        return "cpu"

    def is_supported(self) -> bool:
        return self.npu_status is not None and self.npu_status.available

    def __repr__(self):
        return (f"AscendAdapter(type={self.config.npu_type}, "
                f"chips={self.config.chip_count}, "
                f"mem={self.config.total_memory_mb}MB)")
