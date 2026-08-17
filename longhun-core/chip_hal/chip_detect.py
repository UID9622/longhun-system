#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-CHIP-DETECT-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
"""
龍魂芯片检测引擎 · 中国芯片统一特征发现

支持检测:
  - 鲲鹏 920 (HiSilicon Kunpeng) — ARMv8.2+ · 华为服务器
  - 昇腾 310/910 (Ascend) — NPU · 华为AI加速
  - 飞腾 S2500 (Phytium) — ARMv8 · 天津飞腾
  - 龍芯 3A5000/3A6000 (Loongson) — LoongArch · 中科院
  - 申威 SW26010 (Sunway) — Sunway64 · 无锡超级计算
  - Apple Silicon (M1/M2/M3) — ARMv8.5+ · Mac本地开发
  - 通用 ARM64 / x86_64 — 降级兜底

检测策略:
  1. /proc/cpuinfo → vendor_id·model name·flags
  2. /sys/class/devicetree/base/model → 华为设备树
  3. /usr/local/Ascend/driver → NPU 驱动检测
  4. 降级 → 通用架构
"""

import os
import platform
import re
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from pathlib import Path
from typing import Optional, List, Dict, Any


# ══════════════════════════════════════════════
# 枚举定义
# ══════════════════════════════════════════════

class ChipArch(Enum):
    """芯片架构"""
    ARMv8  = "armv8"
    ARMv8_2 = "armv8.2"      # 鲲鹏 920
    ARMv8_5 = "armv8.5"      # Apple Silicon
    ARMv9  = "armv9"
    LoongArch = "loongarch"
    Sunway64 = "sunway64"
    X86_64 = "x86_64"
    X86_32 = "x86_32"
    UNKNOWN = "unknown"


class ChipVendor(Enum):
    """芯片厂商"""
    HUAWEI  = "huawei"       # 鲲鹏 / 昇腾
    PHYTIUM = "phytium"      # 飞腾
    LOONGSON = "loongson"    # 龍芯
    SUNWAY  = "sunway"       # 申威
    APPLE   = "apple"        # Apple Silicon
    INTEL   = "intel"
    AMD     = "amd"
    GENERIC = "generic"


class NpuType(Enum):
    """NPU 类型"""
    NONE   = "none"
    ASCEND_310 = "ascend_310"
    ASCEND_710 = "ascend_710"
    ASCEND_910 = "ascend_910"
    KUNPENG_DAVINCI = "kunpeng_davinci"  # 鲲鹏内置 Da Vinci


@dataclass
class ChipInfo:
    """芯片完整信息"""
    arch: ChipArch = ChipArch.UNKNOWN
    vendor: ChipVendor = ChipVendor.GENERIC
    model: str = ""
    model_name: str = ""         # /proc/cpuinfo 完整 model name
    revision: str = ""
    cores: int = 0
    npu_available: bool = False
    npu_type: NpuType = NpuType.NONE
    flags: List[str] = field(default_factory=list)
    features: Dict[str, bool] = field(default_factory=dict)
    boost_available: bool = False
    raw_cpuinfo: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        d = {
            "arch": self.arch.value,
            "vendor": self.vendor.value,
            "model": self.model,
            "model_name": self.model_name,
            "revision": self.revision,
            "cores": self.cores,
            "npu_available": self.npu_available,
            "npu_type": self.npu_type.value,
            "boost_available": self.boost_available,
            "features": self.features,
        }
        return d
    
    def __repr__(self) -> str:
        npu_str = f"+{self.npu_type.value}" if self.npu_available else ""
        return f"ChipInfo({self.vendor.value}·{self.model}·{self.arch.value}·{self.cores}核{npu_str})"


# ══════════════════════════════════════════════
# 检测函数
# ══════════════════════════════════════════════

def _read_file_safe(path: str) -> Optional[str]:
    """安全读取文件"""
    try:
        if os.path.exists(path) and os.access(path, os.R_OK):
            with open(path, "r") as f:
                return f.read()
    except Exception:
        pass
    return None


def _run_cmd(cmd: List[str], timeout: int = 5) -> Optional[str]:
    """安全运行命令"""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def _detect_from_cpuinfo() -> Dict[str, Any]:
    """从 /proc/cpuinfo 检测芯片信息"""
    info: Dict[str, Any] = {
        "vendor_id": "", "model_name": "", "flags": [],
        "cpu_arch": "", "cores": 0, "revision": "",
    }
    cpuinfo = _read_file_safe("/proc/cpuinfo")
    if not cpuinfo:
        return info
    
    for line in cpuinfo.split("\n"):
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip().lower()
            val = val.strip()
            
            if key == "vendor_id":
                info["vendor_id"] = val
            elif key == "model name" or key == "cpu model":
                info["model_name"] = val
            elif key == "flags" or key == "features":
                info["flags"] = [f.strip() for f in val.split()]
            elif key == "cpu architecture":
                info["cpu_arch"] = val
            elif key == "revision":
                info["revision"] = val
    
    # 统计核心数
    proc_count = sum(1 for line in cpuinfo.split("\n") if line.strip().startswith("processor"))
    info["cores"] = proc_count if proc_count > 0 else (os.cpu_count() or 1)
    
    return info


def _detect_vendor(cpuinfo: Dict[str, Any], machine: str) -> tuple:
    """根据 cpuinfo 和 machine 推断厂商和型号"""
    vendor = ChipVendor.GENERIC
    model = ""
    arch = ChipArch.UNKNOWN
    model_name = cpuinfo.get("model_name", "")
    vendor_id = cpuinfo.get("vendor_id", "")
    flags = set(cpuinfo.get("flags", []))
    cpu_arch_str = cpuinfo.get("cpu_arch", "")
    
    # ── LoongArch 检测（优先：独立指令集架构） ──
    if "loongarch" in machine.lower() or "loongarch" in model_name.lower():
        arch = ChipArch.LoongArch
        vendor = ChipVendor.LOONGSON
        if "3A6000" in model_name or "3A6000" in cpu_arch_str:
            model = "龍芯3A6000"
        elif "3A5000" in model_name or "3A5000" in cpu_arch_str:
            model = "龍芯3A5000"
        elif "3B" in model_name:
            model = "龍芯3B系列"
        else:
            model = "龍芯（LoongArch）"
        return vendor, model, arch, model_name
    
    # ── 华为鲲鹏检测 ──
    huawei_indicators = [
        "kunpeng", "kunpeng", "鲲鹏",
        "hisilicon", "huawei", "taishan",
        "hi1616", "hi1620", "hi1630",
        "hi1610", "hi1612", "hi1635",
    ]
    if any(ind in model_name.lower() or ind in vendor_id.lower() for ind in huawei_indicators):
        vendor = ChipVendor.HUAWEI
        # 判断具体型号
        if "920" in model_name or "kunpeng920" in model_name.lower():
            model = "鲲鹏920"
            arch = ChipArch.ARMv8_2
        elif "916" in model_name:
            model = "鲲鹏916"
            arch = ChipArch.ARMv8
        else:
            model = "鲲鹏（通用）"
            arch = ChipArch.ARMv8_2
        return vendor, model, arch, model_name
    
    # ── 华为设备树检测 ──
    dt_model = _read_file_safe("/sys/firmware/devicetree/base/model")
    if dt_model:
        dt_lower = dt_model.lower()
        if any(ind in dt_lower for ind in huawei_indicators):
            vendor = ChipVendor.HUAWEI
            model = "鲲鹏（设备树检测）"
            arch = ChipArch.ARMv8_2
            return vendor, model, arch, model_name
    
    # ── 飞腾检测 ──
    phytium_indicators = ["phytium", "ft-", "ft2000", "s2500", "ft1500a",
                          "ft2000+", "d2000", "ft2004"]
    if any(ind in model_name.lower() or ind in vendor_id.lower() for ind in phytium_indicators):
        vendor = ChipVendor.PHYTIUM
        if "s2500" in model_name.lower():
            model = "飞腾S2500"
        elif "ft2000+" in model_name.lower() or "ft2000plus" in model_name.lower():
            model = "飞腾FT2000+"
        elif "ft2000" in model_name.lower():
            model = "飞腾FT2000/4"
        elif "d2000" in model_name.lower():
            model = "飞腾D2000"
        else:
            model = "飞腾（通用）"
        arch = ChipArch.ARMv8
        return vendor, model, arch, model_name
    
    # ── 申威检测 ──
    sunway_indicators = ["sunway", "sw26010", "sw1621", "sw3231", "申威"]
    if any(ind in model_name.lower() or ind in vendor_id.lower() for ind in sunway_indicators):
        vendor = ChipVendor.SUNWAY
        model = "申威SW26010" if "sw26010" in model_name.lower() else "申威"
        arch = ChipArch.Sunway64
        return vendor, model, arch, model_name
    
    # ── Apple Silicon 检测 ──
    if machine == "arm64" and sys.platform == "darwin":
        # 通过 sysctl 进一步确认
        brand = _run_cmd(["sysctl", "-n", "machdep.cpu.brand_string"])
        if brand and "Apple" in brand:
            vendor = ChipVendor.APPLE
            model = brand.strip()
            arch = ChipArch.ARMv8_5
            return vendor, model, arch, model_name
    
    # ── x86 Intel / AMD ──
    if machine in ("x86_64", "amd64", "i386", "i686"):
        arch = ChipArch.X86_64 if machine in ("x86_64", "amd64") else ChipArch.X86_32
        if "intel" in vendor_id.lower() or "genuineintel" in vendor_id.lower():
            vendor = ChipVendor.INTEL
            model = model_name.split("@")[0].strip() if model_name else "Intel x86_64"
        elif "amd" in vendor_id.lower() or "authenticamd" in vendor_id.lower():
            vendor = ChipVendor.AMD
            model = model_name.split("@")[0].strip() if model_name else "AMD x86_64"
        else:
            vendor = ChipVendor.GENERIC
            model = "Generic x86_64"
        return vendor, model, arch, model_name
    
    # ── 通用 ARM64 降级 ──
    if machine in ("aarch64", "arm64"):
        arch = ChipArch.ARMv8
        vendor = ChipVendor.GENERIC
        model = "Generic ARM64"
        return vendor, model, arch, model_name
    
    # 无法识别
    return vendor, model, arch, model_name


def _detect_features(arch: ChipArch, flags: List[str]) -> Dict[str, bool]:
    """检测指令集特性"""
    flag_set = set(flags)
    features: Dict[str, bool] = {}
    
    # ARM 特性
    features["asimd"] = "asimd" in flag_set
    features["fp"] = "fp" in flag_set
    features["aes"] = "aes" in flag_set
    features["pmull"] = "pmull" in flag_set
    features["sha1"] = "sha1" in flag_set
    features["sha2"] = "sha2" in flag_set
    features["sha3"] = "sha3" in flag_set
    features["sm3"] = "sm3" in flag_set
    features["sm4"] = "sm4" in flag_set
    features["crc32"] = "crc32" in flag_set
    features["atomics"] = "atomics" in flag_set
    features["fp16"] = "fp16" in flag_set        # ARMv8.2+
    features["rcpc"] = "rcpc" in flag_set        # ARMv8.3+
    features["dotprod"] = "dotprod" in flag_set  # ARMv8.4+
    
    # x86 特性
    features["avx"] = "avx" in flag_set
    features["avx2"] = "avx2" in flag_set
    features["avx512"] = any("avx512" in f for f in flag_set)
    features["sse4_2"] = "sse4_2" in flag_set
    features["aesni"] = "aes" in flag_set
    
    # 鲲鹏加速器特性
    features["kunpeng_crypto"] = all(
        f in flag_set for f in ["aes", "sha2", "sm3", "sm4"]
    )
    features["kunpeng_accel"] = features.get("kunpeng_crypto", False) and \
        features.get("fp16", False) and features.get("dotprod", False)
    
    return features


def _detect_npu() -> tuple:
    """检测 NPU 是否存在"""
    ascend_paths = [
        "/usr/local/Ascend/driver",
        "/usr/local/Ascend/nnae",
        "/opt/ascend",
        "/etc/ascend",
    ]
    
    for path in ascend_paths:
        if os.path.exists(path):
            # 判断版本
            version_file = f"/usr/local/Ascend/driver/version.cfg"
            if os.path.exists(version_file):
                version_content = _read_file_safe(version_file) or ""
                if "910" in version_content:
                    return True, NpuType.ASCEND_910
                elif "310" in version_content:
                    return True, NpuType.ASCEND_310
                elif "710" in version_content:
                    return True, NpuType.ASCEND_710
            return True, NpuType.ASCEND_910  # 默认 910
    
    # 检测 npu-smi 命令
    npu_smi = _run_cmd(["npu-smi", "info"])
    if npu_smi:
        if "910" in npu_smi:
            return True, NpuType.ASCEND_910
        elif "310" in npu_smi:
            return True, NpuType.ASCEND_310
        return True, NpuType.ASCEND_910
    
    return False, NpuType.NONE


def _detect_boost() -> bool:
    """检测是否有性能提升路径（NPU或硬件加速）"""
    npu_avail, _ = _detect_npu()
    if npu_avail:
        return True
    # 鲲鹏硬件加密加速也算 boost
    cpuinfo = _detect_from_cpuinfo()
    flags = set(cpuinfo.get("flags", []))
    has_kunpeng_crypto = all(f in flags for f in ["aes", "sha2", "sm3", "sm4"])
    return has_kunpeng_crypto


# ══════════════════════════════════════════════
# 主入口
# ══════════════════════════════════════════════

def detect_chip() -> ChipInfo:
    """
    检测当前 CPU 架构并返回最佳配置。
    自动识别: 鲲鹏920·昇腾910·飞腾S2500·龍芯3A6000·申威SW26010·Apple Silicon
    降级: 通用 ARM64 或 x86_64
    """
    machine = platform.machine().lower()
    cpuinfo = _detect_from_cpuinfo()
    
    # 厂商 & 型号 & 架构
    vendor, model, arch, model_name = _detect_vendor(cpuinfo, machine)
    
    # NPU 检测
    npu_avail, npu_type_enum = _detect_npu()
    
    # 特性集
    features = _detect_features(arch, cpuinfo.get("flags", []))
    
    # Boost
    boost = npu_avail or features.get("kunpeng_accel", False)
    
    chip = ChipInfo(
        arch=arch,
        vendor=vendor,
        model=model if model else model_name,
        model_name=model_name or model,
        revision=cpuinfo.get("revision", ""),
        cores=cpuinfo.get("cores", 1),
        npu_available=npu_avail,
        npu_type=npu_type_enum,
        flags=cpuinfo.get("flags", []),
        features=features,
        boost_available=boost,
        raw_cpuinfo=str(cpuinfo),
    )
    
    return chip


# ══════════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════════

if __name__ == "__main__":
    import json
    chip = detect_chip()
    print(json.dumps(chip.to_dict(), ensure_ascii=False, indent=2))
    print(f"\n{chip}")
    print(f"Python: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Machine: {platform.machine()}")
