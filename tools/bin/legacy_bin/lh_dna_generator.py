#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂·DNA 生成器 v2.0
新格式：#龍芯⚡️{年干支}·{月干支}·{日干支}·{卦名}-{动作标签}-{版本}

- 年/月/日 干支按传统八字算法自动计算（月柱以节气为界）
- 卦名由动作标签 + 时间戳哈希映射到六十四卦
- 全系统统一调用，禁止手写 DNA

DNA: #龍芯⚡️丙午·辛未·乙酉·需-DNA-GENERATOR-v2.0
"""

import hashlib
import re
import time
from datetime import datetime, timezone
from typing import Tuple, Optional

# ═══════════════════════════════════════════════════════════
# L0 常量
# ═══════════════════════════════════════════════════════════

天干 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
地支 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 年上起月：甲己之年丙作首，乙庚之岁戊为头，丙辛之岁寻庚起，丁壬壬位顺行流，戊癸之年甲寅上
年上起月 = {
    "甲": "丙", "己": "丙",
    "乙": "戊", "庚": "戊",
    "丙": "庚", "辛": "庚",
    "丁": "壬", "壬": "壬",
    "戊": "甲", "癸": "甲",
}

# 日上起时：甲己还加甲，乙庚丙作初，丙辛从戊起，丁壬庚子居，戊癸何方发，壬子是真途
日上起时 = {
    "甲": "甲", "己": "甲",
    "乙": "丙", "庚": "丙",
    "丙": "戊", "辛": "戊",
    "丁": "庚", "壬": "庚",
    "戊": "壬", "癸": "壬",
}

# 六十四卦（按先天八卦次序排列，便于哈希映射）
六十四卦 = [
    "乾", "坤", "屯", "蒙", "需", "讼", "师", "比",
    "小畜", "履", "泰", "否", "同人", "大有", "谦", "豫",
    "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
    "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒",
    "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解",
    "损", "益", "夬", "姤", "萃", "升", "困", "井",
    "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅",
    "巽", "兑", "涣", "节", "中孚", "小过", "既济", "未济",
]

# 二十四节气（公历月日近似表，用于确定月支）
# 格式：(month, day) -> (branch_index, branch_name)
# 寅月从立春开始，依次类推
节气表 = [
    ((2, 3), (2, 5), "寅"),    # 立春
    ((2, 5), (3, 7), "寅"),    # 立春-惊蛰
    ((3, 7), (3, 20), "卯"),   # 惊蛰
    ((3, 20), (4, 5), "卯"),   # 惊蛰-清明
    ((4, 5), (4, 20), "辰"),   # 清明
    ((4, 20), (5, 6), "辰"),   # 清明-立夏
    ((5, 6), (5, 21), "巳"),   # 立夏
    ((5, 21), (6, 6), "巳"),   # 立夏-芒种
    ((6, 6), (6, 21), "午"),   # 芒种
    ((6, 21), (7, 7), "午"),   # 芒种-小暑
    ((7, 7), (7, 23), "未"),   # 小暑
    ((7, 23), (8, 7), "未"),   # 小暑-立秋
    ((8, 7), (8, 23), "申"),   # 立秋
    ((8, 23), (9, 7), "申"),   # 立秋-白露
    ((9, 7), (9, 23), "酉"),   # 白露
    ((9, 23), (10, 8), "酉"),  # 白露-寒露
    ((10, 8), (10, 23), "戌"), # 寒露
    ((10, 23), (11, 7), "戌"), # 寒露-立冬
    ((11, 7), (11, 22), "亥"), # 立冬
    ((11, 22), (12, 7), "亥"), # 立冬-大雪
    ((12, 7), (12, 21), "子"), # 大雪
    ((12, 21), (1, 6), "子"),  # 大雪-小寒
    ((1, 6), (1, 20), "丑"),   # 小寒
    ((1, 20), (2, 3), "丑"),   # 小寒-立春
]


# ═══════════════════════════════════════════════════════════
# 干支计算
# ═══════════════════════════════════════════════════════════

def _julian_day(year: int, month: int, day: int) -> int:
    """计算儒略日（简化算法，公元 1582 年后有效）"""
    if month <= 2:
        year -= 1
        month += 12
    a = year // 100
    b = 2 - a + a // 4
    return int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524


def _compute_year_pillar(dt: datetime) -> str:
    """年柱：以立春为界"""
    year = dt.year
    # 立春通常在 2 月 3-5 日，简化为 2 月 4 日 0 时
    spring_start = datetime(year, 2, 4, 0, 0, 0, tzinfo=dt.tzinfo)
    if dt < spring_start:
        year -= 1
    gan = 天干[(year - 4) % 10]
    zhi = 地支[(year - 4) % 12]
    return f"{gan}{zhi}"


def _compute_month_branch(dt: datetime) -> str:
    """月支：以二十四节气为界"""
    m, d = dt.month, dt.day
    for start, end, branch in 节气表:
        sm, sd = start
        em, ed = end
        # 处理跨年的情况
        in_range = False
        if sm <= em:
            if (m > sm or (m == sm and d >= sd)) and (m < em or (m == em and d < ed)):
                in_range = True
        else:
            # 跨年的区间（如 12 月到 1 月）
            if (m == sm and d >= sd) or (m > sm) or (m < em) or (m == em and d < ed):
                in_range = True
        if in_range:
            return branch
    return "寅"  # 默认立春


def _compute_month_pillar(dt: datetime, year_pillar: str) -> str:
    """月柱：年干定月干，节气定月支"""
    year_gan = year_pillar[0]
    month_zhi = _compute_month_branch(dt)
    month_zhi_idx = 地支.index(month_zhi)
    # 正月为寅，索引 2
    month_offset = (month_zhi_idx - 2) % 12  # 0=正月，1=二月，...
    start_gan = 年上起月[year_gan]
    start_gan_idx = 天干.index(start_gan)
    month_gan = 天干[(start_gan_idx + month_offset) % 10]
    return f"{month_gan}{month_zhi}"


def _compute_day_pillar(dt: datetime) -> str:
    """日柱：基于儒略日"""
    jd = _julian_day(dt.year, dt.month, dt.day)
    # 1900-01-31 为甲辰日，JD=2415051
    offset = (jd - 2415051) % 60
    gan = 天干[offset % 10]
    zhi = 地支[offset % 12]
    return f"{gan}{zhi}"


def _compute_hour_pillar(dt: datetime, day_pillar: str) -> str:
    """时柱：日干定时干，时辰定时支（保留，供扩展）"""
    day_gan = day_pillar[0]
    hour = dt.hour
    # 23-1 子，1-3 丑，...
    zhi_idx = ((hour + 1) // 2) % 12
    zhi = 地支[zhi_idx]
    start_gan = 日上起时[day_gan]
    start_gan_idx = 天干.index(start_gan)
    gan = 天干[(start_gan_idx + zhi_idx) % 10]
    return f"{gan}{zhi}"


def compute_ganzhi_pillars(dt: Optional[datetime] = None) -> Tuple[str, str, str]:
    """
    计算年/月/日 三柱干支
    
    Returns:
        (年柱, 月柱, 日柱)
    """
    if dt is None:
        dt = datetime.now(timezone.utc)
    year = _compute_year_pillar(dt)
    month = _compute_month_pillar(dt, year)
    day = _compute_day_pillar(dt)
    return year, month, day


# ═══════════════════════════════════════════════════════════
# 卦象计算
# ═══════════════════════════════════════════════════════════

def compute_hexagram(action_tag: str = "", dt: Optional[datetime] = None) -> str:
    """
    由动作标签 + 时间戳哈希映射到六十四卦之一
    同一秒内同一动作标签结果稳定，不同动作或时间自然分流
    """
    if dt is None:
        dt = datetime.now(timezone.utc)
    seed = f"{action_tag}:{dt.strftime('%Y-%m-%d %H:%M:%S')}"
    h = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    idx = int(h[:16], 16) % 64
    return 六十四卦[idx]


# ═══════════════════════════════════════════════════════════
# DNA 生成 / 验证
# ═══════════════════════════════════════════════════════════

DNA_PATTERN = re.compile(
    r"^#龍芯⚡️"
    r"([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])·"
    r"([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])·"
    r"([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])·"
    r"([\u4e00-\u9fa5]{1,2})-"
    r"([A-Za-z0-9_\-]+)-"
    r"v([\d.]+)$"
)


def generate_dna(action_tag: str, version: str = "1.0", dt: Optional[datetime] = None) -> str:
    """
    生成新格式 DNA
    
    Args:
        action_tag: 动作标签，如 DNA-GENERATOR、VALIDATION-REPORT
        version: 版本号，如 1.0、2.0
        dt: 可选指定时间，默认 UTC 当前时间
    
    Returns:
        #龍芯⚡️{年干支}·{月干支}·{日干支}·{卦名}-{动作标签}-{版本}
    """
    if dt is None:
        dt = datetime.now(timezone.utc)
    
    year, month, day = compute_ganzhi_pillars(dt)
    hexagram = compute_hexagram(action_tag, dt)
    
    return f"#龍芯⚡️{year}·{month}·{day}·{hexagram}-{action_tag}-v{version}"


def parse_dna(dna: str) -> Optional[dict]:
    """解析 DNA，返回结构化字段；格式错误返回 None"""
    m = DNA_PATTERN.match(dna)
    if not m:
        return None
    return {
        "year": m.group(1),
        "month": m.group(2),
        "day": m.group(3),
        "hexagram": m.group(4),
        "action": m.group(5),
        "version": m.group(6),
    }


def validate_dna(dna: str) -> Tuple[bool, str]:
    """
    验证 DNA 格式是否合法
    
    Returns:
        (是否合法, 消息)
    """
    parsed = parse_dna(dna)
    if parsed is None:
        return False, "DNA 格式不匹配新规范"
    return True, f"✅ DNA 合法: {parsed['action']} v{parsed['version']}"


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print(__doc__)
        print("用法:")
        print("  python3 bin/lh_dna_generator.py <动作标签> [版本]")
        print("  python3 bin/lh_dna_generator.py validate <DNA>")
        print("示例:")
        print("  python3 bin/lh_dna_generator.py TEST-OPERATION 1.0")
        sys.exit(0)
    
    if sys.argv[1] == "validate":
        dna = sys.argv[2] if len(sys.argv) > 2 else ""
        ok, msg = validate_dna(dna)
        print(msg)
        sys.exit(0 if ok else 1)
    
    action = sys.argv[1]
    version = sys.argv[2] if len(sys.argv) > 2 else "1.0"
    
    dna = generate_dna(action, version)
    print(dna)
    
    parsed = parse_dna(dna)
    print(f"  年柱: {parsed['year']}")
    print(f"  月柱: {parsed['month']}")
    print(f"  日柱: {parsed['day']}")
    print(f"  卦名: {parsed['hexagram']}")
    print(f"  动作: {parsed['action']}")
    print(f"  版本: {parsed['version']}")
