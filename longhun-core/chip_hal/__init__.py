# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-CHIP-HAL-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""龍魂芯片硬件抽象层（HAL）· 中国芯片统一适配"""
from .chip_detect import detect_chip, ChipInfo, ChipArch, ChipVendor
from .ascend_npu import AscendNpuDetector, compute_route

__all__ = [
    "detect_chip", "ChipInfo", "ChipArch", "ChipVendor",
    "AscendNpuDetector", "compute_route",
]
