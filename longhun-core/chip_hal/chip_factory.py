#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-CHIP-FACTORY-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
"""
龍魂·适配器工厂 · 自动选择最佳芯片适配器

按优先级尝试:
  Apple Silicon → 鲲鹏 → 昇腾 → 飞腾 → 龍芯 → 申威 → 通用降级
"""
from typing import Union

try:
    from .chip_detect import detect_chip, ChipVendor
    from .apple_adapter import AppleSiliconAdapter
    from .kunpeng_adapter import KunpengAdapter
    from .ascend_adapter import AscendAdapter
    from .phytium_adapter import PhytiumAdapter
    from .loongson_adapter import LoongsonAdapter
    from .sunway_adapter import SunwayAdapter
    from .generic_adapter import GenericAdapter
except ImportError:
    from chip_hal.chip_detect import detect_chip, ChipVendor
    from chip_hal.apple_adapter import AppleSiliconAdapter
    from chip_hal.kunpeng_adapter import KunpengAdapter
    from chip_hal.ascend_adapter import AscendAdapter
    from chip_hal.phytium_adapter import PhytiumAdapter
    from chip_hal.loongson_adapter import LoongsonAdapter
    from chip_hal.sunway_adapter import SunwayAdapter
    from chip_hal.generic_adapter import GenericAdapter

AdapterType = Union[
    AppleSiliconAdapter, KunpengAdapter, AscendAdapter,
    PhytiumAdapter, LoongsonAdapter, SunwayAdapter,
    GenericAdapter,
]


def get_best_adapter() -> AdapterType:
    """
    自动选择最佳芯片适配器。
    按厂商优先级链式尝试，找到第一个匹配的返回。
    最低保证返回 GenericAdapter（永远兜底）。
    """
    chip = detect_chip()
    vendor = chip.vendor
    
    # 优先级: Apple > 华为(鲲鹏+昇腾) > 飞腾 > 龍芯 > 申威 > 通用
    if vendor == ChipVendor.APPLE:
        adapter = AppleSiliconAdapter()
        if adapter.is_supported():
            return adapter
    
    if vendor == ChipVendor.HUAWEI:
        # 先判断是否昇腾 NPU
        if chip.npu_available:
            adapter = AscendAdapter()
            if adapter.is_supported():
                return adapter
        # 鲲鹏
        adapter = KunpengAdapter()
        if adapter.is_supported():
            return adapter
    
    if vendor == ChipVendor.PHYTIUM:
        adapter = PhytiumAdapter()
        if adapter.is_supported():
            return adapter
    
    if vendor == ChipVendor.LOONGSON:
        adapter = LoongsonAdapter()
        if adapter.is_supported():
            return adapter
    
    if vendor == ChipVendor.SUNWAY:
        adapter = SunwayAdapter()
        if adapter.is_supported():
            return adapter
    
    return GenericAdapter()


if __name__ == "__main__":
    adapter = get_best_adapter()
    print(f"最佳适配器: {type(adapter).__name__}")
    print(f"  {adapter}")
    print(f"  编译标志: {adapter.get_compile_flags()}")
    print(f"  Docker镜像: {adapter.get_docker_base_image()}")
