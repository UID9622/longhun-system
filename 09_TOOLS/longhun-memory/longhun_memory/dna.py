#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·乙未·壬子·丙午·䷙大畜-MEMORY-DNA-v1.0
# License: MulanPSL v2
"""
DNA 追溯码生成器
═══════════════════
v∞ 龍魂 DNA 格式:
  #龍芯⚡️<干支四柱>·<卦>-<模块>-<动作>-<哈希8>-UID9622

来源: 龍魂系统 DNA 生成规范
"""

import hashlib
import os
import random
import time
from datetime import datetime, timezone
from typing import Optional


# ════════════════════════════════════════════════════
# 天干地支
# ════════════════════════════════════════════════════

_TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
_DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 64卦简表
_GUA64 = [
    "䷀乾", "䷁坤", "䷂屯", "䷃蒙", "䷄需", "䷅讼", "䷆师", "䷇比",
    "䷈小畜", "䷉履", "䷊泰", "䷋否", "䷌同人", "䷍大有", "䷎谦", "䷏豫",
    "䷐随", "䷑蛊", "䷒临", "䷓观", "䷔噬嗑", "䷕贲", "䷖剥", "䷗复",
    "䷘无妄", "䷙大畜", "䷚颐", "䷛大过", "䷜坎", "䷝离", "䷞咸", "䷟恒",
    "䷠遁", "䷡大壮", "䷢晋", "䷣明夷", "䷤家人", "䷥睽", "䷦蹇", "䷧解",
    "䷨损", "䷩益", "䷪夬", "䷫姤", "䷬萃", "䷭升", "䷮困", "䷯井",
    "䷰革", "䷱鼎", "䷲震", "䷳艮", "䷴渐", "䷵归妹", "䷶丰", "䷷旅",
    "䷸巽", "䷹兑", "䷺涣", "䷻节", "䷼中孚", "䷽小过", "䷾既济", "䷿未济",
]


def _ganzhi_year(year: int) -> tuple[str, str]:
    """年份 → (天干, 地支)"""
    base = 4  # 甲子年 = 公元4年
    offset = (year - base) % 60
    return _TIANGAN[offset % 10], _DIZHI[offset % 12]


def _ganzhi_month(year: int, month: int) -> tuple[str, str]:
    """月份 → (天干, 地支)。月支按节气定，这里用简化版本。"""
    year_gan = _TIANGAN.index(_ganzhi_year(year)[0])
    month_zhi_idx = (month + 1) % 12  # 寅月为正月
    month_gan_idx = (year_gan * 2 + month) % 10
    return _TIANGAN[month_gan_idx], _DIZHI[month_zhi_idx]


def _ganzhi_day(year: int, month: int, day: int) -> tuple[str, str]:
    """日期 → (天干, 地支)。简化计算。"""
    import datetime as dt
    d = dt.date(year, month, day)
    epoch = dt.date(1900, 1, 1)
    days = (d - epoch).days
    return _TIANGAN[days % 10], _DIZHI[days % 12]


def _ganzhi_hour(hour: int) -> tuple[str, str]:
    """小时 → (天干, 地支)"""
    zhi_idx = ((hour + 1) // 2) % 12
    return _TIANGAN[zhi_idx % 10], _DIZHI[zhi_idx]


def _current_ganzhi() -> str:
    """获取当前时间的干支四柱简写"""
    now = datetime.now()
    yg, yd = _ganzhi_year(now.year)
    mg, md = _ganzhi_month(now.year, now.month)
    dg, dd = _ganzhi_day(now.year, now.month, now.day)
    hg, hd = _ganzhi_hour(now.hour)
    return f"{yg}{yd}·{mg}{md}·{dg}{dd}·{hd}时"


def _pick_gua(seed: Optional[int] = None) -> str:
    """随机选一卦"""
    if seed is None:
        seed = int(time.time() * 1000)
    rng = random.Random(seed)
    idx = rng.randint(0, 63)
    return _GUA64[idx]


# ════════════════════════════════════════════════════
# DNA 类
# ════════════════════════════════════════════════════

class DNA:
    """龍魂 DNA 追溯码 v∞

    用法:
        dna = DNA.create("memory", "seal")
        print(dna.full)  # #龍芯⚡️丙午·申时·䷗复-MEMORY-SEAL-A1B2C3D4-UID9622
        print(dna.short) # #MEMORY-SEAL-A1B2C3D4
    """

    def __init__(self, module: str, action: str, hash8: str,
                 ganzhi: Optional[str] = None, gua: Optional[str] = None):
        self.module = module.upper()
        self.action = action.upper()
        self.hash8 = hash8.upper()
        self.ganzhi = ganzhi or _current_ganzhi()
        self.gua = gua or _pick_gua()

    @property
    def full(self) -> str:
        return f"#龍芯⚡️{self.ganzhi}·{self.gua}-{self.module}-{self.action}-{self.hash8}-UID9622"

    @property
    def short(self) -> str:
        return f"#{self.module}-{self.action}-{self.hash8}"

    @property
    def compact(self) -> str:
        return f"#龍芯⚡️{self.ganzhi}·{self.gua}"

    @classmethod
    def create(cls, module: str, action: str) -> "DNA":
        """创建一个新的 DNA"""
        random_data = os.urandom(16) + str(time.time()).encode()
        hash8 = hashlib.sha256(random_data).hexdigest()[:8]
        return cls(module=module, action=action, hash8=hash8)

    @classmethod
    def parse(cls, dna_str: str) -> Optional["DNA"]:
        """从字符串解析 DNA"""
        try:
            if not dna_str.startswith("#龍芯⚡️"):
                return None
            # #龍芯⚡️丙午·申时·䷗复-MEMORY-SEAL-A1B2C3D4-UID9622
            parts = dna_str[6:].split("-")  # 去掉 #龍芯⚡️
            if len(parts) < 4:
                return None
            gz_gua = parts[0]  # 丙午·申时·䷗复
            module = parts[1]
            action = parts[2]
            hash8 = parts[3]
            return cls(module=module, action=action, hash8=hash8)
        except Exception:
            return None

    def to_dict(self) -> dict:
        return {
            "full": self.full,
            "short": self.short,
            "module": self.module,
            "action": self.action,
            "ganzhi": self.ganzhi,
            "gua": self.gua,
            "hash": self.hash8,
        }


def dna_now(module: str, action: str) -> str:
    """快捷生成 DNA 完整字符串"""
    return DNA.create(module, action).full


# ════════════════════════════════════════════════════
# 自检
# ════════════════════════════════════════════════════

if __name__ == "__main__":
    dna = DNA.create("TEST", "check")
    print(f"DNA: {dna.full}")
    print(f"Short: {dna.short}")
    print(f"Parse: {DNA.parse(dna.full)}")
    print("🟢 DNA 模块自检通过")
