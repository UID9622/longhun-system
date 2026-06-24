#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂流场·数字根计算模块（四源优先级）
CNSH Flow - Digital Root Calculator (Four-Source Priority)

DNA:#龍芯⚡️2026-05-03-CNSH-FLOW-DIGITAL-ROOT-v4.1
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

责任: UID9622·不免责
"""

import hashlib
from typing import Optional, Tuple
from .schemas import DigitalRootConfig, WuxingEnum


class DigitalRootCalculator:
    """四源数字根计算器（IPA-FLOW-GATE-DR）"""

    @staticmethod
    def extract_dna_digits(dna: str) -> Optional[int]:
        """
        从DNA字符串提取数字
        例:#龍芯⚡️2026-05-03-XXX-v4.1 → 2026050341 → dr
        """
        digits = ''.join(c for c in dna if c.isdigit())
        if not digits:
            return None
        return DigitalRootCalculator.sum_to_digit_root(int(digits))

    @staticmethod
    def extract_raw_digits(content: str) -> Optional[int]:
        """
        从原文内容提取所有数字
        """
        digits = ''.join(c for c in content if c.isdigit())
        if not digits:
            return None
        return DigitalRootCalculator.sum_to_digit_root(int(digits))

    @staticmethod
    def content_hash_dr(content: str) -> int:
        """
        内容SHA256哈希前8位转数值
        """
        h = hashlib.sha256(content.encode('utf-8')).hexdigest()
        hex8 = h[:8]
        decimal = int(hex8, 16)
        return DigitalRootCalculator.sum_to_digit_root(decimal)

    @staticmethod
    def sum_to_digit_root(num: int) -> int:
        """
        数字递归求和至个位（数字根）
        例: 2026 → 2+0+2+6=10 → 1+0=1
        """
        num = abs(int(num))
        while num >= 10:
            num = sum(int(d) for d in str(num))
        return num if num > 0 else 9  # 0映射为9

    @staticmethod
    def calculate_dr(
        config: DigitalRootConfig,
        dna: str = "",
        content: str = ""
    ) -> Tuple[int, str]:
        """
        按四源优先级计算dr，返回(dr值, 来源说明)

        优先级：
        1. explicit_dr     (显式给定)
        2. dna_digits      (DNA字符串)
        3. content_hash_dr (内容hash)
        4. raw_digits_dr   (原文数字)
        5. fallback_dr     (默认土)
        """
        if config.explicit_dr is not None:
            return config.explicit_dr, "explicit"

        if config.dna_digits is not None:
            return config.dna_digits, "dna_digits"

        # 实时计算DNA数字根
        if dna:
            extracted = DigitalRootCalculator.extract_dna_digits(dna)
            if extracted is not None:
                config.dna_digits = extracted
                return extracted, "dna_extracted"

        if config.content_hash_dr is not None:
            return config.content_hash_dr, "content_hash_preset"

        # 实时计算内容hash
        if content:
            computed = DigitalRootCalculator.content_hash_dr(content)
            config.content_hash_dr = computed
            return computed, "content_hash_computed"

        if config.raw_digits_dr is not None:
            return config.raw_digits_dr, "raw_digits_preset"

        # 实时提取原文数字
        if content:
            extracted = DigitalRootCalculator.extract_raw_digits(content)
            if extracted is not None:
                config.raw_digits_dr = extracted
                return extracted, "raw_digits_extracted"

        return config.fallback_dr, "fallback_earth"

    @staticmethod
    def dr_to_wuxing(dr: int) -> WuxingEnum:
        """
        数字根到五行映射（公式对准表）
        1/9→水 | 2/3→木 | 4/5→火 | 6/7→金 | 8→金 | 0→土
        """
        mapping = {
            1: WuxingEnum.WATER,      # 坎
            2: WuxingEnum.WOOD,       # 巽
            3: WuxingEnum.WOOD,       # 震
            4: WuxingEnum.FIRE,       # 离
            5: WuxingEnum.FIRE,       # 中（变）
            6: WuxingEnum.METAL,      # 干
            7: WuxingEnum.METAL,      # 兑
            8: WuxingEnum.METAL,      # 艮
            9: WuxingEnum.WATER,      # 坎（变）
            0: WuxingEnum.EARTH,      # 默认
        }
        dr_mod = dr % 10
        return mapping.get(dr_mod, WuxingEnum.EARTH)

    @staticmethod
    def validate_dr(dr: int) -> bool:
        """验证dr是否有效（0-9）"""
        return 0 <= dr <= 9


# 便利函数
def quick_dr(content: str, explicit: Optional[int] = None) -> Tuple[int, WuxingEnum]:
    """快速计算dr及对应五行"""
    config = DigitalRootConfig(explicit_dr=explicit)
    dr, _ = DigitalRootCalculator.calculate_dr(config, content=content)
    wuxing = DigitalRootCalculator.dr_to_wuxing(dr)
    return dr, wuxing
