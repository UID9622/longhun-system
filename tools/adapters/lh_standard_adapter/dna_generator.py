# DNA: #龍芯⚡️丙午·乙未·乙丑·观-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
DNA Generator — produces v∞ DNA traceability codes.

Format: #LongHun⚡️{Stem}·{Stem}·{Stem}·{ShiChen}·{Hexagram}-{Module}-{Action}-{Version}-{Hash8}

This is a shell tool. Core algorithm logic is protected.
"""

import hashlib
import time
from datetime import datetime, timezone, timedelta
from typing import Optional


# Canonical Hexagram → Domain mapping (public subset)
HEXAGRAM_MAP = {
    "乾 Qian": {"symbol": "䷀", "unichar": "\u4dc0", "domain": "governance|sovereignty|constitution|codebuddy|rules|naming"},
    "坤 Kun":   {"symbol": "䷁", "unichar": "\u4dc1", "domain": "storage|archive|memory|data|backup"},
    "屯 Zhun":  {"symbol": "䷂", "unichar": "\u4dc2", "domain": "birth|init|startup|bootstrap"},
    "蒙 Meng":  {"symbol": "䷃", "unichar": "\u4dc3", "domain": "learning|teaching|education|tutorial"},
    "需 Xu":    {"symbol": "䷄", "unichar": "\u4dc4", "domain": "waiting|patience|async|queue"},
    "讼 Song":  {"symbol": "䷅", "unichar": "\u4dc5", "domain": "conflict|legal|dispute|compliance"},
    "坎 Kan":   {"symbol": "䷜", "unichar": "\u4ddc", "domain": "engine|flow|stream|taiji|sync"},
    "离 Li":    {"symbol": "䷝", "unichar": "\u4ddd", "domain": "audit|clarity|dashboard|state|test"},
    "震 Zhen":  {"symbol": "䷲", "unichar": "\u4df2", "domain": "security|guard|minor|alarm|dna|meltdown"},
    "艮 Gen":   {"symbol": "䷳", "unichar": "\u4df3", "domain": "privacy|sovereignty|gate|boundary"},
    "巽 Xun":   {"symbol": "䷸", "unichar": "\u4df8", "domain": "persona|route|deploy|train|model"},
    "兑 Dui":   {"symbol": "䷹", "unichar": "\u4df9", "domain": "trust|exchange|ecom|register"},
    "既济 JiJi":{"symbol": "䷾", "unichar": "\u4dfe", "domain": "completion|audit|release|final"},
    "未济 WeiJi":{"symbol": "䷿", "unichar": "\u4dff", "domain": "progress|incomplete|draft|ongoing"},
}


# Heavenly Stems · Earthly Branches
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

TIAN_GAN_ROMAN = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
DI_ZHI_ROMAN = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]

SHI_CHEN = ["ZiShi", "ChouShi", "YinShi", "MaoShi", "ChenShi", "SiShi",
            "WuShi", "WeiShi", "ShenShi", "YouShi", "XuShi", "HaiShi"]


class DNAGenerator:
    """
    Generates v∞ DNA traceability codes.

    Note: Core stem-branch calculation and hexagram mapping algorithms
    are simplified in this public adapter. The full engine is protected.
    """

    def __init__(self, uid="9622", device="HM-9622-001", locale="Asia/Shanghai"):
        self.uid = uid
        self.device = device
        self.locale = locale
        self._tz = timezone(timedelta(hours=8), name="CST")  # China Standard Time

    def generate(self, task_type="default", action="WRAP", version="v1.0") -> str:
        """
        Generate a v∞ DNA traceability code.

        Parameters:
            task_type: Task category (maps to module domain)
            action: Action descriptor
            version: Semantic version

        Returns:
            Full DNA code string
        """
        now = datetime.now(self._tz)
        stem = self._compute_stem_branch(now)
        hexagram = self._select_hexagram(task_type)
        body = f"ADAPTER-{task_type.upper()}-{action.upper()}-{version.upper()}"
        hash8 = hashlib.sha256(f"{stem}{hexagram['symbol']}{body}{self.device}".encode()).hexdigest()[:8]

        return (
            f"#LongHun⚡️{stem['year']}·{stem['month']}·{stem['day']}·{stem['shichen']}"
            f"·{hexagram['symbol']}{hexagram['en_name']}"
            f"-{body}-{hash8}"
        )

    def _compute_stem_branch(self, dt: datetime) -> dict:
        """
        Compute the four-pillar stem-branch for a datetime.

        Simplified public implementation. Full astronomical-precision
        calculation is part of the protected core engine.
        """
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour

        # Year stem-branch (base: AD 4 = JiaZi)
        year_idx = year - 4
        yg = year_idx % 10
        yz = year_idx % 12

        # Month stem-branch (simplified: month-based offset)
        mg = (year_idx % 10 * 2 + month + 1) % 10
        mz = (month + 1) % 12

        # Day stem-branch (simplified Julian-based calculation)
        yy = year % 100
        base = ((yy + 7) * 5 + 15 + (yy + 19) // 4) % 60
        month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
            month_days[2] = 29
        doy = sum(month_days[:month]) + day
        seq = (base + doy) % 60
        dg = (seq - 1) % 10
        dz = (seq - 1) % 12

        # ShiChen
        sc_idx = ((hour + 1) // 2) % 12

        return {
            "year": f"{TIAN_GAN_ROMAN[yg]}{DI_ZHI_ROMAN[yz]}",
            "year_cn": f"{TIAN_GAN[yg]}{DI_ZHI[yz]}",
            "month": f"{TIAN_GAN_ROMAN[mg]}{DI_ZHI_ROMAN[mz]}",
            "day": f"{TIAN_GAN_ROMAN[dg]}{DI_ZHI_ROMAN[dz]}",
            "shichen": SHI_CHEN[sc_idx],
            "raw": {"yg": yg, "yz": yz, "mg": mg, "mz": mz, "dg": dg, "dz": dz, "sc": sc_idx},
        }

    def _select_hexagram(self, task_type: str) -> dict:
        """Select hexagram by domain keyword matching."""
        task_lower = task_type.lower()
        for key, info in HEXAGRAM_MAP.items():
            domains = info["domain"].split("|")
            for d in domains:
                if d.lower() in task_lower or any(t in d for t in task_lower.split("-")):
                    parts = key.split()
                    return {
                        "symbol": info["symbol"],
                        "cn_name": parts[0],
                        "en_name": parts[1] if len(parts) > 1 else parts[0],
                    }
        # Default: Completion hexagram
        return {"symbol": "䷾", "cn_name": "既济", "en_name": "JiJi"}

    def _now_iso(self) -> str:
        return datetime.now(self._tz).isoformat()


def generate_dna(task_type="default", action="WRAP", version="v1.0",
                 uid="9622", device="HM-9622-001") -> str:
    """Convenience function for quick DNA generation."""
    gen = DNAGenerator(uid=uid, device=device)
    return gen.generate(task_type=task_type, action=action, version=version)
