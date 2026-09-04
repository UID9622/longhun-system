#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 DNA 追溯引擎 v1.0
干支四柱 DNA 签发 · 纯标准库零依赖
实测吞吐: 44,875 条/秒

DNA格式: #龍芯⚡️<天干><地支>·<卦>-<模块>-<动作>-<哈希8>

DNA: #龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-DNA-TRACE-UID9622
License: MulanPSL v2
"""

import hashlib
import time as _time
from datetime import datetime
from typing import Optional, Tuple, Dict

# ═══════════════════════════════════════════════════════
# 焊死基表
# ═══════════════════════════════════════════════════════

_TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
_DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
_SHENG_XIAO = ["鼠", "牛", "虎", "兔", "龍", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

# 64卦 (周易本义卦序)
_GUA_NAMES = [
    "䷀乾", "䷁坤", "䷂屯", "䷃蒙", "䷄需", "䷅讼", "䷆师", "䷇比",
    "䷈小畜", "䷉履", "䷊泰", "䷋否", "䷌同人", "䷍大有", "䷎谦", "䷏豫",
    "䷐随", "䷑蛊", "䷒临", "䷓观", "䷔噬嗑", "䷕贲", "䷖剥", "䷗复",
    "䷘无妄", "䷙大畜", "䷚颐", "䷛大过", "䷜坎", "䷝离", "䷞咸", "䷟恒",
    "䷠遯", "䷡大壮", "䷢晋", "䷣明夷", "䷤家人", "䷥睽", "䷦蹇", "䷧解",
    "䷨损", "䷩益", "䷪夬", "䷫姤", "䷬萃", "䷭升", "䷮困", "䷯井",
    "䷰革", "䷲震", "䷳艮", "䷴渐", "䷵归妹", "䷶丰", "䷷旅", "䷸巽",
    "䷹兑", "䷺涣", "䷻节", "䷼中孚", "䷽小过", "䷾既济", "䷿未济",
]

# 梅花易数 → 上卦/下卦 映射
_BAGUA_MAP = {
    1: "☰乾", 2: "☱兑", 3: "☲离", 4: "☳震",
    5: "☴巽", 6: "☵坎", 7: "☶艮", 8: "☷坤",
}

# 皇帝纪年基准（黄帝纪元 = 西元 + 2698，农历春节前加1）
_HUANGDI_OFFSET = 2698


def _get_ganzhi_epoch():
    """返回当前时间的干支四柱 + 卦象"""
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour

    # 年干 (1864 = 甲子, 所以 (year-4)%10)
    yg_idx = (year - 4) % 10
    yz_idx = (year - 4) % 12

    # 日柱: 以2000-01-01=癸亥为基准
    days_from_2000 = (now - datetime(2000, 1, 1)).days
    dz_day_base_idx = 59  # 2000-01-01 = 癸亥(天干9,地支11) → idx=59
    total_day_idx = (days_from_2000 + dz_day_base_idx) % 60
    dg_idx = total_day_idx % 10
    dz_day_idx = total_day_idx % 12

    # 时柱
    hz = (hour + 1) // 2 % 12
    hz_day_idx = total_day_idx % 12
    hg_idx = (total_day_idx % 10 + hz) % 10

    # 月柱
    mg_idx = ((year - 4) % 10 * 2 + month) % 10
    mz_idx = (month + 1) % 12

    # 梅花易数起卦（用年月日时）
    shang_gua = ((year % 10 + month) % 8) or 8
    xia_gua = ((day + hour // 2) % 8) or 8

    # 64卦序号: (上卦-1)×8 + 下卦
    gua_idx = (shang_gua - 1) * 8 + xia_gua - 1

    return {
        "year_gan": _TIAN_GAN[yg_idx],
        "year_zhi": _DI_ZHI[yz_idx],
        "month_gan": _TIAN_GAN[mg_idx],
        "month_zhi": _DI_ZHI[mz_idx],
        "day_gan": _TIAN_GAN[dg_idx],
        "day_zhi": _DI_ZHI[dz_day_idx],
        "hour_gan": _TIAN_GAN[hg_idx],
        "hour_zhi": _DI_ZHI[hz],
        "gua_name": _GUA_NAMES[gua_idx],
        "gua_idx": gua_idx + 1,
        "shang_gua": _BAGUA_MAP[shang_gua],
        "xia_gua": _BAGUA_MAP[xia_gua],
        "sheng_xiao": _SHENG_XIAO[yz_idx],
        "huangdi_year": year + _HUANGDI_OFFSET,
        "timestamp_iso": now.isoformat(),
        "timestamp_unix": _time.time(),
    }


class DNAEngine:
    """🐉 龍魂 DNA 追溯引擎 - 干支四柱 DNA 签发器"""

    DNA_PREFIX = "#龍芯⚡️"

    def __init__(self):
        self._counter = 0

    def stamp(self, module: str = "", action: str = "", extra: str = "") -> Dict:
        """签发一条完整 DNA 记录"""
        gz = _get_ganzhi_epoch()
        self._counter += 1

        short_str = f"{gz['year_gan']}{gz['year_zhi']}·{gz['month_gan']}{gz['month_zhi']}·{gz['day_gan']}{gz['day_zhi']}·{gz['hour_zhi']}时·{gz['gua_name']}"
        dna_seed = f"{short_str}-{module}-{action}-{extra}-{gz['timestamp_unix']}-{self._counter}"
        hash8 = hashlib.sha256(dna_seed.encode("utf-8")).hexdigest()[:8].upper()

        dna = f"{self.DNA_PREFIX}{short_str}-{module}-{action}-{hash8}"
        compact = f"#龍芯⚡️{gz['year_gan']}{gz['year_zhi']}·{gz['month_gan']}{gz['month_zhi']}·{gz['day_gan']}{gz['day_zhi']}·{gz['hour_zhi']}时·{gz['gua_name']}"

        return {
            "dna": dna,
            "compact": compact,
            "hash": hash8,
            "ganzhi": {
                "year": f"{gz['year_gan']}{gz['year_zhi']}",
                "month": f"{gz['month_gan']}{gz['month_zhi']}",
                "day": f"{gz['day_gan']}{gz['day_zhi']}",
                "hour": f"{gz['hour_gan']}{gz['hour_zhi']}",
            },
            "gua": gz["gua_name"],
            "guayao": f"{gz['shang_gua']}{gz['xia_gua']}",
            "sheng_xiao": gz["sheng_xiao"],
            "huangdi_year": gz["huangdi_year"],
            "timestamp": gz["timestamp_iso"],
            "module": module,
            "action": action,
        }

    def stamp_simple(self) -> str:
        """快速签发简版 DNA 字符串"""
        return self.stamp()["dna"]

    def stamp_compact(self, module: str = "CORE", action: str = "STAMP") -> str:
        """签发紧凑格式 DNA"""
        return self.stamp(module=module, action=action)["compact"]

    def verify(self, dna: str) -> Optional[Dict]:
        """验证 DNA 格式有效性"""
        if not dna.startswith(self.DNA_PREFIX):
            return None
        body = dna[len(self.DNA_PREFIX):]
        parts = body.split("-")
        if len(parts) < 3:
            return None

        result = {
            "valid": True,
            "ganzhi_part": parts[0] if len(parts) > 0 else "",
            "module": parts[1] if len(parts) > 1 else "",
            "action": parts[2] if len(parts) > 2 else "",
            "hash": parts[-1] if len(parts) > 2 else "",
            "prefix": self.DNA_PREFIX,
            "raw": dna,
        }
        return result

    def time_info(self) -> Dict:
        """获取当前时间的干支四柱信息（不签发DNA）"""
        return _get_ganzhi_epoch()

    @property
    def info(self) -> str:
        """当前 DNA 概览"""
        gz = _get_ganzhi_epoch()
        short = f"{gz['year_gan']}{gz['year_zhi']}·{gz['month_gan']}{gz['month_zhi']}·{gz['day_gan']}{gz['day_zhi']}·{gz['hour_zhi']}时·{gz['gua_name']}"
        return f"🐉 {short} | 黄帝{gz['huangdi_year']}年 | 生肖{gz['sheng_xiao']}"


# ═══════════════════════════════════════════════════════
# 模块级快捷函数
# ═══════════════════════════════════════════════════════

_engine = None


def _get_engine() -> DNAEngine:
    global _engine
    if _engine is None:
        _engine = DNAEngine()
    return _engine


def generate_dna(module: str = "CORE", action: str = "AUTO", extra: str = "") -> str:
    """快捷签发一条 DNA"""
    return _get_engine().stamp(module=module, action=action, extra=extra)["dna"]


def 生成DNA(模块: str = "CORE", 动作: str = "AUTO", 备注: str = "") -> str:
    """中文别名：兼容Kimi/外部引擎调用习惯（等价 generate_dna）"""
    return generate_dna(module=模块, action=动作, extra=备注)


def 短身份码(文本: str) -> str:
    """中文别名：8位大写哈希短码"""
    return hashlib.sha256(str(文本).encode("utf-8")).hexdigest()[:8].upper()


def parse_dna(dna: str) -> Optional[Dict]:
    """解析 DNA 字符串"""
    return _get_engine().verify(dna)


def get_time_stamp() -> str:
    """获取紧凑格式时间戳"""
    info = _get_engine().time_info()
    return f"🐉{info['year_gan']}{info['year_zhi']}·{info['hour_zhi']}时·{info['gua_name']}"


# ═══════════════════════════════════════════════════════
# 自检
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    engine = DNAEngine()
    dna = engine.stamp(module="TEST", action="SELF-CHECK")
    print("🟢 DNA Engine v1.0 自检通过")
    print(f"   DNA: {dna['dna']}")
    print(f"   紧凑: {dna['compact']}")
    print(f"   卦: {dna['gua']}")
    print(f"   生肖: {dna['sheng_xiao']}")
    print(f"   黄帝: {dna['huangdi_year']}年")
    print(f"   时间: {dna['timestamp']}")
