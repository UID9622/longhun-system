#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-ASCEND-NPU-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
"""
龍魂昇腾 NPU 加速路由 · 智能降级

检测昇腾硬件 → 尝试 torch_npu / CANN API → 若不可达则降级 CPU
不强制安装昇腾驱动，无驱动时静默降级，不影响系统运行。

用法:
    detector = AscendNpuDetector()
    result = detector.detect()
    
    route = compute_route({"prefer": "auto"})  # 自动选择 NPU/CPU 路径
"""

import os
import sys
import warnings
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from .chip_detect import detect_chip, ChipInfo, NpuType
except ImportError:
    from chip_hal.chip_detect import detect_chip, ChipInfo, NpuType


class ComputeTarget(Enum):
    """计算目标"""
    CPU = "cpu"
    NPU_ASCEND = "npu_ascend"
    NPU_KUNPENG = "npu_kunpeng"
    AUTO = "auto"


@dataclass
class NpuStatus:
    """NPU 状态"""
    available: bool = False
    npu_type: NpuType = NpuType.NONE
    driver_path: str = ""
    driver_version: str = ""
    toolkit_installed: bool = False
    torch_npu_available: bool = False
    chip_count: int = 0
    total_memory_mb: int = 0
    temperature_c: float = 0.0
    errors: list = field(default_factory=list)


class AscendNpuDetector:
    """
    昇腾 NPU 探测器。
    检测 CANN 驱动、toolkit、torch_npu 可用性，静默降级。
    """
    
    # 昇腾安装路径候选
    ASCEND_PATHS = [
        "/usr/local/Ascend",
        "/opt/ascend",
        os.path.expanduser("~/Ascend"),
    ]
    
    def __init__(self):
        self._status: Optional[NpuStatus] = None
    
    def detect(self) -> NpuStatus:
        """完整检测，结果缓存"""
        if self._status is not None:
            return self._status
        
        status = NpuStatus()
        
        # Step 1: 找驱动
        status.driver_path = self._find_driver_path()
        if not status.driver_path:
            self._status = status
            return status
        
        status.available = True
        status.driver_version = self._get_driver_version(status.driver_path)
        
        # Step 2: 判断 NPU 型号
        chip = detect_chip()
        status.npu_type = chip.npu_type
        
        # Step 3: 检查 toolkit
        status.toolkit_installed = self._check_toolkit(status.driver_path)
        
        # Step 4: 尝试导入 torch_npu
        status.torch_npu_available = self._try_import_torch_npu()
        
        # Step 5: 获取芯片数和内存
        status.chip_count, status.total_memory_mb = self._get_chip_info(
            status.driver_path
        )
        
        # Step 6: 温度
        status.temperature_c = self._get_temperature(status.driver_path)
        
        self._status = status
        return status
    
    def _find_driver_path(self) -> str:
        """查找 Ascend 驱动目录"""
        for base in self.ASCEND_PATHS:
            driver = os.path.join(base, "driver")
            if os.path.isdir(driver):
                return driver
        return ""
    
    def _get_driver_version(self, driver_path: str) -> str:
        """获取驱动版本"""
        version_cfg = os.path.join(driver_path, "version.cfg")
        try:
            if os.path.exists(version_cfg):
                with open(version_cfg) as f:
                    for line in f:
                        line = line.strip()
                        if "Version" in line:
                            return line.split("=")[-1].strip()
        except Exception:
            pass
        return "unknown"
    
    def _check_toolkit(self, driver_path: str) -> bool:
        """检查 CANN toolkit"""
        asc_home = os.path.dirname(driver_path)
        toolkit = os.path.join(asc_home, "nnae", "latest")
        return os.path.isdir(toolkit)
    
    def _try_import_torch_npu(self) -> bool:
        """尝试导入 torch_npu（静默）"""
        try:
            import torch
            if hasattr(torch, 'npu') and torch.npu.is_available():
                return True
        except ImportError:
            pass
        # 尝试 torch_npu 单独包
        try:
            import torch_npu  # type: ignore
            return True
        except ImportError:
            pass
        return False
    
    def _get_chip_info(self, driver_path: str) -> tuple:
        """获取芯片数量与内存"""
        chip_count = 0
        total_memory = 0
        
        # 尝试 npu-smi info
        try:
            import subprocess
            r = subprocess.run(
                ["npu-smi", "info", "-m"],
                capture_output=True, text=True, timeout=10
            )
            if r.returncode == 0:
                for line in r.stdout.split("\n"):
                    if "Chip" in line or "chip" in line:
                        chip_count += 1
                    if "Memory" in line or "mem" in line.lower():
                        try:
                            parts = line.split()
                            for p in parts:
                                n = p.replace("MB", "").replace("mb", "").strip()
                                if n.isdigit():
                                    total_memory += int(n)
                        except Exception:
                            pass
        except Exception:
            pass
        
        return max(chip_count, 1) if chip_count > 0 else 0, total_memory
    
    def _get_temperature(self, driver_path: str) -> float:
        """获取温度"""
        try:
            import subprocess
            r = subprocess.run(
                ["npu-smi", "info", "-t"],
                capture_output=True, text=True, timeout=10
            )
            if r.returncode == 0:
                for line in r.stdout.split("\n"):
                    if "Temperature" in line or "temp" in line.lower():
                        import re
                        temps = re.findall(r'(\d+\.?\d*)', line)
                        if temps:
                            return float(temps[0])
        except Exception:
            pass
        return 0.0


# ══════════════════════════════════════════════
# 计算路由
# ══════════════════════════════════════════════

@dataclass
class ComputeRoute:
    """计算路由结果"""
    target: ComputeTarget
    reason: str
    npu_status: Optional[NpuStatus] = None
    fallback_available: bool = True
    
    def __repr__(self):
        return f"ComputeRoute({self.target.value}: {self.reason})"


def compute_route(config: Optional[Dict[str, Any]] = None) -> ComputeRoute:
    """
    自动选择 NPU/CPU 执行路径。
    
    策略:
      - prefer="npu": 优先 NPU，不可用则降级 CPU
      - prefer="cpu": 强制 CPU
      - prefer="auto" or None: 智能路由 → NPU 可用就用 NPU，否则 CPU
    
    返回 ComputeRoute，包含目标 + 理由。
    无 NPU 时静默降级，不抛异常。
    """
    config = config or {}
    prefer = config.get("prefer", "auto")
    
    # 强制 CPU
    if prefer == "cpu":
        return ComputeRoute(
            target=ComputeTarget.CPU,
            reason="用户指定 CPU 模式"
        )
    
    # 检测 NPU
    detector = AscendNpuDetector()
    npu_status = detector.detect()
    
    # 强制 NPU
    if prefer == "npu":
        if not npu_status.available:
            return ComputeRoute(
                target=ComputeTarget.CPU,
                reason="NPU 不可用，降级到 CPU",
                npu_status=npu_status,
                fallback_available=True,
            )
        if npu_status.torch_npu_available:
            return ComputeRoute(
                target=ComputeTarget.NPU_ASCEND,
                reason=f"昇腾 NPU 可用 ({npu_status.npu_type.value})",
                npu_status=npu_status,
            )
        return ComputeRoute(
            target=ComputeTarget.CPU,
            reason="NPU 驱动存在但 torch_npu 未安装，降级 CPU",
            npu_status=npu_status,
        )
    
    # auto 模式：智能路由
    if prefer == "auto" or prefer is None:
        if npu_status.available and npu_status.torch_npu_available:
            return ComputeRoute(
                target=ComputeTarget.NPU_ASCEND,
                reason=f"自动选择 NPU ({npu_status.npu_type.value}·{npu_status.chip_count}芯)",
                npu_status=npu_status,
            )
        
        # 尝试坤鹏加速
        chip = detect_chip()
        if chip.boost_available and chip.vendor.value == "huawei":
            return ComputeRoute(
                target=ComputeTarget.NPU_KUNPENG,
                reason=f"鲲鹏硬件加速可用 ({chip.model})",
                npu_status=npu_status,
            )
        
        return ComputeRoute(
            target=ComputeTarget.CPU,
            reason="无 NPU/加速器，使用 CPU",
            npu_status=npu_status,
        )
    
    # 默认 CPU
    return ComputeRoute(
        target=ComputeTarget.CPU,
        reason=f"未知偏好 '{prefer}'，降级 CPU",
    )


# ══════════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════════

if __name__ == "__main__":
    import json
    
    detector = AscendNpuDetector()
    status = detector.detect()
    print("=== NPU 状态 ===")
    print(f"可用: {status.available}")
    print(f"类型: {status.npu_type.value}")
    print(f"驱动: {status.driver_version}")
    print(f"芯片数: {status.chip_count}")
    print(f"显存: {status.total_memory_mb}MB")
    print(f"torch_npu: {status.torch_npu_available}")
    print()
    
    print("=== 计算路由 ===")
    for mode in ["auto", "npu", "cpu"]:
        route = compute_route({"prefer": mode})
        print(f"  {mode}: {route}")
