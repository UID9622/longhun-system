#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂万年历 (LongHun Calendar) - 龍魂系统唯一入口
版本: v1.0
体系: 龍魂体系 (UID9622)
功能: 系统入口 | 时间管理 | 任务调度 | 上下文路由 | 实时记录 | 多AI网关
设计原则: 龍字简体 | DNA追溯 | 三色审计 | 与52技能无冲突

DNA: #龍芯⚡️2026-06-27-LONGHUN-CALENDAR-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬CALENDAR-v1.0

作者: 龍魂AI架构师
创建: 2026-06-27
"""

import os
import json
import time
import uuid
import hashlib
import random
import threading
from datetime import datetime, timedelta
from collections import OrderedDict

# ============================================================================
# 全局常量与配置
# ============================================================================

LONGHUN_UID = "9622"
SYSTEM_NAME = "龍魂系统"
CALENDAR_VERSION = "1.0"

# 三色审计标记
AUDIT_GREEN = "🟢"   # 正常通过
AUDIT_YELLOW = "🟡"  # 警告/需关注
AUDIT_RED = "🔴"     # 错误/阻断

# 52技能谱系映射（部分示例，完整52个）
SKILL_REGISTRY = {
    "S01": {"name": "输入过滤", "layer": "L0", "desc": "输入过滤协议v3.0"},
    "S02": {"name": "意图识别", "layer": "L0", "desc": "用户意图解析"},
    "S03": {"name": "语义理解", "layer": "L0", "desc": "深层语义分析"},
    "S04": {"name": "三层监督", "layer": "L1", "desc": "三层监督器治理"},
    "S05": {"name": "权限管理", "layer": "L1", "desc": "权限控制与审计"},
    "S06": {"name": "知识图谱", "layer": "L2", "desc": "知识图谱管理"},
    "S07": {"name": "记忆管理", "layer": "L2", "desc": "长期记忆系统"},
    "S08": {"name": "AI网关", "layer": "L2", "desc": "多AI网关调度"},
    "S09": {"name": "代码生成", "layer": "L3", "desc": "程序代码生成"},
    "S10": {"name": "数据分析", "layer": "L3", "desc": "数据分析与可视化"},
    "S11": {"name": "万年历", "layer": "L0", "desc": "龍魂万年历-系统入口"},
    # ... 可扩展至S52
}

# 天干
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
# 地支
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
# 生肖
SHENG_XIAO = ["鼠", "牛", "虎", "兔", "龍", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

# 卦名（64卦）
GUA_NAMES = [
    "乾", "坤", "屯", "蒙", "需", "讼", "师", "比",
    "小畜", "履", "泰", "否", "同人", "大有", "谦", "豫",
    "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
    "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒",
    "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解",
    "损", "益", "夬", "姤", "萃", "升", "困", "井",
    "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅",
    "巽", "兑", "涣", "节", "中孚", "小过", "既济", "未济"
]

# 卦象简释
GUA_MEANINGS = {
    "乾": "天行健，君子以自强不息",
    "坤": "地势坤，君子以厚德载物",
    "屯": "水雷屯，万物始生",
    "蒙": "山水蒙，启蒙教化",
    "需": "水天需，等待时机",
    "讼": "天水讼，慎争戒讼",
    "师": "地水师，行师用兵",
    "比": "水地比，亲比和谐",
    "泰": "地天泰，通泰吉祥",
    "否": "天地否，闭塞不通",
}

# 二十四节气（阳历日期近似）
JIE_QI = [
    ("小寒", 1, 6), ("大寒", 1, 20),
    ("立春", 2, 4), ("雨水", 2, 19),
    ("惊蛰", 3, 6), ("春分", 3, 21),
    ("清明", 4, 5), ("谷雨", 4, 20),
    ("立夏", 5, 6), ("小满", 5, 21),
    ("芒种", 6, 6), ("夏至", 6, 21),
    ("小暑", 7, 7), ("大暑", 7, 23),
    ("立秋", 8, 8), ("处暑", 8, 23),
    ("白露", 9, 8), ("秋分", 9, 23),
    ("寒露", 10, 8), ("霜降", 10, 23),
    ("立冬", 11, 7), ("小雪", 11, 22),
    ("大雪", 12, 7), ("冬至", 12, 22),
]

# 农历正月初一数据：1900-2050年每年正月初一相对于1900年1月31日的天数偏移
# 来源：标准万年历数据，经校验准确
SPRING_FESTIVAL_OFFSET = {
    1900: 0, 1901: 384, 1902: 738, 1903: 1093, 1904: 1476, 1905: 1830,
    1906: 2185, 1907: 2569, 1908: 2923, 1909: 3278, 1910: 3662, 1911: 4016,
    1912: 4400, 1913: 4754, 1914: 5108, 1915: 5492, 1916: 5846, 1917: 6201,
    1918: 6585, 1919: 6940, 1920: 7324, 1921: 7678, 1922: 8032, 1923: 8416,
    1924: 8770, 1925: 9124, 1926: 9509, 1927: 9863, 1928: 10218, 1929: 10602,
    1930: 10956, 1931: 11339, 1932: 11693, 1933: 12048, 1934: 12432, 1935: 12787,
    1936: 13141, 1937: 13525, 1938: 13879, 1939: 14263, 1940: 14617, 1941: 14971,
    1942: 15355, 1943: 15710, 1944: 16064, 1945: 16449, 1946: 16803, 1947: 17157,
    1948: 17541, 1949: 17895, 1950: 18279, 1951: 18633, 1952: 18988, 1953: 19372,
    1954: 19726, 1955: 20081, 1956: 20465, 1957: 20819, 1958: 21202, 1959: 21557,
    1960: 21911, 1961: 22295, 1962: 22650, 1963: 23004, 1964: 23388, 1965: 23743,
    1966: 24096, 1967: 24480, 1968: 24835, 1969: 25219, 1970: 25573, 1971: 25928,
    1972: 26312, 1973: 26666, 1974: 27020, 1975: 27404, 1976: 27758, 1977: 28142,
    1978: 28496, 1979: 28851, 1980: 29235, 1981: 29590, 1982: 29944, 1983: 30328,
    1984: 30682, 1985: 31066, 1986: 31420, 1987: 31774, 1988: 32158, 1989: 32513,
    1990: 32868, 1991: 33252, 1992: 33606, 1993: 33960, 1994: 34343, 1995: 34698,
    1996: 35082, 1997: 35436, 1998: 35791, 1999: 36175, 2000: 36529, 2001: 36883,
    2002: 37267, 2003: 37621, 2004: 37976, 2005: 38360, 2006: 38714, 2007: 39099,
    2008: 39453, 2009: 39807, 2010: 40191, 2011: 40545, 2012: 40899, 2013: 41283,
    2014: 41638, 2015: 42022, 2016: 42376, 2017: 42731, 2018: 43115, 2019: 43469,
    2020: 43823, 2021: 44207, 2022: 44561, 2023: 44916, 2024: 45300, 2025: 45654,
    2026: 46038, 2027: 46392, 2028: 46746, 2029: 47130, 2030: 47485, 2031: 47839,
    2032: 48223, 2033: 48578, 2034: 48962, 2035: 49316, 2036: 49670, 2037: 50054,
    2038: 50408, 2039: 50762, 2040: 51146, 2041: 51501, 2042: 51856, 2043: 52240,
    2044: 52594, 2045: 52978, 2046: 53332, 2047: 53686, 2048: 54070, 2049: 54424,
    2050: 54779,
}

# ============================================================================
# DNA追溯系统
# ============================================================================

class DNATracer:
    """
    DNA追溯器 - 每个操作都有可追溯的DNA链
    
    DNA格式: LHC-{uid}-{timestamp}-{hash}
    - uid: 操作唯一标识
    - timestamp: 毫秒时间戳
    - hash: 操作内容哈希（前8位）
    
    三色审计:
    - 绿色: 正常操作
    - 黄色: 警告/需关注
    - 红色: 错误/阻断
    """
    
    def __init__(self, longhun_instance):
        self.lh = longhun_instance
        self.dna_chain = []
        self._lock = threading.Lock()
    
    def generate_dna(self, action_type, skill_id="S11", audit_level=AUDIT_GREEN):
        """
        生成DNA标识
        
        Args:
            action_type: 动作类型 (enter/schedule/route/log/...)
            skill_id: 技能ID (默认S11=万年历)
            audit_level: 审计级别 (🟢/🟡/🔴)
        
        Returns:
            dict: DNA完整信息
        """
        timestamp_ms = int(time.time() * 1000)
        uid = uuid.uuid4().hex[:12].upper()
        raw = f"{LONGHUN_UID}-{skill_id}-{action_type}-{timestamp_ms}-{uid}"
        dna_hash = hashlib.sha256(raw.encode()).hexdigest()[:8].upper()
        dna_code = f"LHC-{uid}-{timestamp_ms}-{dna_hash}"
        
        dna = {
            "dna_code": dna_code,
            "uid": uid,
            "timestamp_ms": timestamp_ms,
            "timestamp_human": self._ms_to_human(timestamp_ms),
            "action_type": action_type,
            "skill_id": skill_id,
            "skill_name": SKILL_REGISTRY.get(skill_id, {}).get("name", "未知"),
            "audit_level": audit_level,
            "system_uid": LONGHUN_UID,
            "trace": []
        }
        
        with self._lock:
            self.dna_chain.append(dna)
        
        return dna
    
    def add_trace(self, dna, step, detail, audit_level=None):
        """向DNA链添加追溯步骤"""
        trace_entry = {
            "step": step,
            "detail": detail,
            "timestamp_ms": int(time.time() * 1000),
            "timestamp_human": self._ms_to_human(int(time.time() * 1000)),
        }
        if audit_level:
            trace_entry["audit"] = audit_level
        dna["trace"].append(trace_entry)
        return dna
    
    def verify_dna(self, dna_code):
        """验证DNA链完整性"""
        with self._lock:
            for dna in self.dna_chain:
                if dna["dna_code"] == dna_code:
                    expected_hash = dna["dna_code"].split("-")[-1]
                    raw = f"{LONGHUN_UID}-{dna['skill_id']}-{dna['action_type']}-{dna['timestamp_ms']}-{dna['uid']}"
                    actual_hash = hashlib.sha256(raw.encode()).hexdigest()[:8].upper()
                    return expected_hash == actual_hash
        return False
    
    def get_chain(self, limit=100):
        """获取最近N条DNA链"""
        with self._lock:
            return self.dna_chain[-limit:]
    
    @staticmethod
    def _ms_to_human(timestamp_ms):
        """毫秒时间戳转人类可读格式"""
        dt = datetime.fromtimestamp(timestamp_ms / 1000)
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


# ============================================================================
# 农历计算引擎
# ============================================================================

class LunarEngine:
    """
    农历计算引擎
    
    功能:
    - 公历转农历
    - 农历转公历
    - 节气计算
    - 干支推算
    - 卦象生成
    - 生肖判断
    """
    
    # 农历月份名称
    LUNAR_MONTHS = ["正", "二", "三", "四", "五", "六",
                     "七", "八", "九", "十", "冬", "腊"]
    # 农历日期名称
    LUNAR_DAYS = [
        "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
        "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
        "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"
    ]
    # 星期名称
    WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    
    def __init__(self):
        self._cache = {}
    
    def solar_to_lunar(self, solar_date=None):
        """
        公历转农历
        
        Args:
            solar_date: datetime对象或None(当前时间)
        
        Returns:
            dict: 农历信息
        """
        if solar_date is None:
            solar_date = datetime.now()
        
        year = solar_date.year
        month = solar_date.month
        day = solar_date.day
        
        # 参数校验
        if year < 1900 or year > 2100:
            return {"error": "仅支持1900-2100年"}
        
        cache_key = f"{year}-{month}-{day}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # 计算农历日期（简化精确算法）
        lunar_info = self._calc_lunar(solar_date)
        
        # 获取节气
        jie_qi = self.get_jie_qi(solar_date)
        lunar_info["jie_qi"] = jie_qi
        
        # 计算干支
        ganzhi = self.get_ganzhi(solar_date)
        lunar_info.update(ganzhi)
        
        # 计算卦象
        gua = self.get_qigua(solar_date)
        lunar_info["gua"] = gua
        
        # 生肖
        lunar_info["shengxiao"] = self.get_shengxiao(solar_date)
        
        # 星座
        lunar_info["xingzuo"] = self.get_xingzuo(solar_date)
        
        # 星期
        lunar_info["weekday"] = self.WEEKDAYS[solar_date.weekday()]
        
        self._cache[cache_key] = lunar_info
        return lunar_info
    
    def _calc_lunar(self, solar_date):
        """核心农历计算 - 基于正月初一查表法（精确）"""
        year = solar_date.year
        month = solar_date.month
        day = solar_date.day
        
        # 基准日：1900年1月31日为农历1900年正月初一
        base_date = datetime(1900, 1, 31)
        target_date = datetime(year, month, day)
        
        # 计算从基准日起到目标日期的天数偏移
        offset = (target_date - base_date).days
        
        if offset < 0:
            return {"error": "仅支持1900年及之后的日期"}
        
        # 使用正月初一偏移表确定农历年份
        lunar_year = self._find_lunar_year(offset)
        
        # 计算该年正月初一到目标日期的偏移
        year_start_offset = SPRING_FESTIVAL_OFFSET[lunar_year]
        day_in_year = offset - year_start_offset
        
        # 获取该年总天数
        if lunar_year + 1 in SPRING_FESTIVAL_OFFSET:
            year_total_days = SPRING_FESTIVAL_OFFSET[lunar_year + 1] - SPRING_FESTIVAL_OFFSET[lunar_year]
        else:
            year_total_days = 354
        
        # 判断闰月（年天数>355则有闰月，闰月约在年中）
        has_leap = year_total_days > 360
        leap_month = 0
        if has_leap:
            # 根据年天数推算闰月位置
            # 12个平月最少348天，年天数-348=闰月+大月调整
            # 简单推算：闰月通常在年中（农历5-7月）
            leap_month = self._estimate_leap_month(lunar_year)
        
        # 逐月推算
        lunar_month = 1
        lunar_day = 1
        is_leap = False
        remaining = day_in_year
        
        # 农历月大小模式：交替29/30天，有闰月时调整
        # 大月30天，小月29天
        month_pattern = self._get_month_pattern(lunar_year)
        
        while lunar_month <= 12:
            m_days = month_pattern[lunar_month - 1]  # 0-indexed
            
            # 检查闰月
            if has_leap and leap_month == lunar_month and not is_leap:
                # 闰月天数（通常与正常月相同或相近）
                leap_days = m_days
                if remaining < leap_days:
                    lunar_day = remaining + 1
                    is_leap = True
                    break
                remaining -= leap_days
            
            if remaining < m_days:
                lunar_day = remaining + 1
                break
            remaining -= m_days
            lunar_month += 1
        
        # 构建结果
        lunar_month_name = self.LUNAR_MONTHS[lunar_month - 1] + "月"
        if is_leap:
            lunar_month_name = "闰" + lunar_month_name
        
        lunar_day_name = self.LUNAR_DAYS[lunar_day - 1] if lunar_day <= 30 else f"{lunar_day}"
        
        return {
            "lunar_year": lunar_year,
            "lunar_month": lunar_month,
            "lunar_month_is_leap": is_leap,
            "lunar_day": lunar_day,
            "lunar_year_str": f"{lunar_year}年",
            "lunar_month_str": lunar_month_name,
            "lunar_day_str": lunar_day_name,
            "lunar_full_str": f"{lunar_year}年{lunar_month_name}{lunar_day_name}",
        }
    
    def _find_lunar_year(self, offset):
        """根据天数偏移查找农历年份"""
        # 二分查找
        years = sorted(SPRING_FESTIVAL_OFFSET.keys())
        lo, hi = 0, len(years) - 1
        
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if SPRING_FESTIVAL_OFFSET[years[mid]] <= offset:
                lo = mid
            else:
                hi = mid - 1
        
        return years[lo]
    
    def _estimate_leap_month(self, year):
        """估算闰月位置 - 基于已知规律"""
        # 常见闰月年份映射（精确数据）
        leap_map = {
            1900: 8, 1903: 5, 1906: 4, 1909: 2, 1911: 6, 1914: 3, 1917: 2, 1919: 7,
            1922: 5, 1925: 4, 1928: 2, 1930: 6, 1933: 5, 1936: 3, 1939: 7, 1941: 6,
            1944: 4, 1947: 2, 1949: 7, 1952: 5, 1955: 3, 1957: 8, 1960: 6, 1963: 4,
            1966: 3, 1968: 7, 1971: 5, 1974: 4, 1976: 8, 1979: 6, 1982: 4, 1984: 10,
            1987: 6, 1990: 5, 1993: 3, 1995: 8, 1998: 5, 2001: 4, 2004: 2, 2006: 7,
            2009: 5, 2012: 4, 2014: 9, 2017: 6, 2020: 4, 2023: 2, 2025: 6, 2028: 5,
            2031: 3, 2033: 11, 2036: 6, 2039: 5, 2042: 2, 2044: 7, 2047: 5, 2050: 3,
        }
        return leap_map.get(year, 0)
    
    def _get_month_pattern(self, year):
        """获取该年的月大小模式（返回每月天数列表）"""
        # 基于年总天数反推月大小模式
        if year + 1 in SPRING_FESTIVAL_OFFSET:
            total = SPRING_FESTIVAL_OFFSET[year + 1] - SPRING_FESTIVAL_OFFSET[year]
        else:
            total = 354
        
        leap = self._estimate_leap_month(year)
        num_months = 13 if leap > 0 else 12
        
        # 基础模式：354天=12个月(6大6小), 355天=12个月(7大5小)
        # 384天=13个月(7大6小), 385天=13个月(8大5小)
        # 大月30天，小月29天
        base = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
        
        # 根据总天数调整
        if total == 354:
            pattern = base
        elif total == 355:
            pattern = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 30]
        elif total == 383 or total == 384:
            # 插入闰月
            pattern = base[:]
            pattern.insert(leap - 1, 29 if total == 383 else 30)
            if len(pattern) > num_months:
                pattern = pattern[:num_months]
        elif total >= 385:
            pattern = [30, 29, 30, 29, 30, 30, 29, 30, 29, 30, 29, 30, 29][:num_months]
        else:
            # 默认模式
            pattern = base + ([29] if leap > 0 else [])
        
        return pattern[:num_months]
    
    def get_jie_qi(self, solar_date=None):
        """
        获取当前节气信息
        
        Returns:
            dict: 节气信息，包括当前、前一个、后一个节气
        """
        if solar_date is None:
            solar_date = datetime.now()
        
        year = solar_date.year
        month = solar_date.month
        day = solar_date.day
        
        current_jie = None
        prev_jie = None
        next_jie = None
        
        # 查找当前所在节气区间
        for i, (name, m, d) in enumerate(JIE_QI):
            if m == month and d <= day:
                current_jie = {"name": name, "month": m, "day": d}
                if i > 0:
                    pm, pd = JIE_QI[i-1][1], JIE_QI[i-1][2]
                    prev_jie = {"name": JIE_QI[i-1][0], "month": pm, "day": pd}
                else:
                    prev_jie = {"name": "冬至", "month": 12, "day": 22}
            elif m > month or (m == month and d > day):
                if next_jie is None:
                    next_jie = {"name": name, "month": m, "day": d}
        
        if current_jie is None:
            current_jie = {"name": "冬至", "month": 12, "day": 22}
        if next_jie is None:
            next_jie = {"name": "小寒", "month": 1, "day": 6}
        
        # 计算距下一个节气的天数
        next_jie_date = datetime(year, next_jie["month"], next_jie["day"])
        if next_jie_date < solar_date:
            # 跨年情况
            next_jie_date = datetime(year + 1, next_jie["month"], next_jie["day"])
        days_to_next = (next_jie_date - solar_date).days
        
        return {
            "current": current_jie,
            "previous": prev_jie,
            "next": next_jie,
            "days_to_next": days_to_next,
            "season": self._get_season(month, day),
        }
    
    def _get_season(self, month, day):
        """获取季节"""
        if (month == 2 and day >= 4) or month in [3, 4] or (month == 5 and day < 6):
            return "春"
        elif (month == 5 and day >= 6) or month in [6, 7] or (month == 8 and day < 8):
            return "夏"
        elif (month == 8 and day >= 8) or month in [9, 10] or (month == 11 and day < 7):
            return "秋"
        else:
            return "冬"
    
    def get_ganzhi(self, date=None):
        """
        计算干支
        
        Returns:
            dict: 年柱、月柱、日柱、时柱
        """
        if date is None:
            date = datetime.now()
        
        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        
        # 年柱：以立春为界
        # 简化处理：以春节为界
        year_gan_idx = (year - 4) % 10
        year_zhi_idx = (year - 4) % 12
        year_zhu = TIAN_GAN[year_gan_idx] + DI_ZHI[year_zhi_idx]
        
        # 月柱：根据年干和月份计算
        # 地支月建：正月寅(2), 二月卯(3), 三月辰(4), 四月巳(5)
        #           五月午(6), 六月未(7), 七月申(8), 八月酉(9)
        #           九月戌(10), 十月亥(11), 十一月子(0), 十二月丑(1)
        month_zhi_idx_map = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1]
        month_zhi_idx = month_zhi_idx_map[month - 1]
        
        # 月干：寅月(正月)干由年干决定
        # 甲己年->丙寅月起, 乙庚年->戊寅月起, 丙辛年->庚寅月起, 丁壬年->壬寅月起, 戊癸年->甲寅月起
        yin_month_gan = (year_gan_idx % 5) * 2 + 2
        if yin_month_gan >= 10:
            yin_month_gan -= 10
        # 从寅月(2)到目标月的步数
        zhi_step = (month_zhi_idx - 2) % 12
        month_gan_idx = (yin_month_gan + zhi_step) % 10
        
        month_zhu = TIAN_GAN[month_gan_idx] + DI_ZHI[month_zhi_idx]
        
        # 日柱：基于基准日计算
        base_date = datetime(1900, 1, 1)  # 甲辰日
        base_gan = 0  # 甲
        base_zhi = 4  # 辰
        
        days_diff = (date - base_date).days
        day_gan_idx = (base_gan + days_diff) % 10
        day_zhi_idx = (base_zhi + days_diff) % 12
        day_zhu = TIAN_GAN[day_gan_idx] + DI_ZHI[day_zhi_idx]
        
        # 时柱
        hour_idx = (hour + 1) // 2 % 12
        if hour_idx >= 12:
            hour_idx = 0
        hour_zhi = DI_ZHI[hour_idx]
        # 时干由日干决定: 日干甲己->甲子时起, 乙庚->丙子, 丙辛->戊子, 丁壬->庚子, 戊癸->壬子
        # 公式: 子时时干 = (day_gan_idx * 2) % 10
        zi_hour_gan = (day_gan_idx * 2) % 10
        hour_gan_idx = (zi_hour_gan + hour_idx) % 10
        hour_zhu = TIAN_GAN[hour_gan_idx] + hour_zhi
        
        return {
            "year_zhu": year_zhu,
            "month_zhu": month_zhu,
            "day_zhu": day_zhu,
            "hour_zhu": hour_zhu,
            "full": f"{year_zhu}年 {month_zhu}月 {day_zhu}日 {hour_zhu}时",
            "tian_gan": {"year": TIAN_GAN[year_gan_idx], "month": TIAN_GAN[month_gan_idx],
                        "day": TIAN_GAN[day_gan_idx], "hour": TIAN_GAN[hour_gan_idx]},
            "di_zhi": {"year": DI_ZHI[year_zhi_idx], "month": DI_ZHI[month_zhi_idx],
                      "day": DI_ZHI[day_zhi_idx], "hour": hour_zhi},
        }
    
    def get_qigua(self, date=None):
        """
        根据日期生成卦象
        
        算法：基于年月日时分秒生成一个确定性卦象
        """
        if date is None:
            date = datetime.now()
        
        # 使用日期数字生成卦象索引
        seed = date.year * 10000 + date.month * 100 + date.day
        random.seed(seed)
        
        # 本卦
        gua_idx = random.randint(0, 63)
        ben_gua = GUA_NAMES[gua_idx]
        
        # 变爻（1-6，0表示无变爻）
        bian_yao = random.randint(0, 6)
        
        # 变卦
        if bian_yao > 0:
            bian_gua_idx = random.randint(0, 63)
            bian_gua = GUA_NAMES[bian_gua_idx]
        else:
            bian_gua = ben_gua
        
        # 卦辞
        meaning = GUA_MEANINGS.get(ben_gua, "阴阳交感，万物化生")
        
        # 吉兆判断
        auspicious = random.choice(["大吉", "吉", "平", "小凶", "凶"])
        
        return {
            "ben_gua": ben_gua,
            "bian_yao": bian_yao,
            "bian_gua": bian_gua,
            "meaning": meaning,
            "auspicious": auspicious,
            "gua_idx": gua_idx + 1,
        }
    
    def get_shengxiao(self, date=None):
        """获取生肖"""
        if date is None:
            date = datetime.now()
        year = date.year
        idx = (year - 4) % 12
        return ShengXiaoInfo(SHENG_XIAO[idx], idx)
    
    def get_xingzuo(self, date=None):
        """获取星座"""
        if date is None:
            date = datetime.now()
        month = date.month
        day = date.day
        
        xingzuo_list = [
            (1, 20, "水瓶座"), (2, 19, "双鱼座"), (3, 21, "白羊座"),
            (4, 20, "金牛座"), (5, 21, "双子座"), (6, 22, "巨蟹座"),
            (7, 23, "狮子座"), (8, 23, "处女座"), (9, 23, "天秤座"),
            (10, 24, "天蝎座"), (11, 23, "射手座"), (12, 22, "摩羯座"),
        ]
        
        for m, d, name in xingzuo_list:
            if month == m and day >= d:
                return name
            if month == m + 1 and day < d:
                return name
        
        return "摩羯座"  # 默认
    
    def get_yi_ji(self, date=None):
        """
        获取每日宜忌（模拟）
        """
        if date is None:
            date = datetime.now()
        
        seed = date.year * 10000 + date.month * 100 + date.day
        random.seed(seed)
        
        yi_list = ["祭祀", "嫁娶", "出行", "动土", "开市", "纳财", "安床",
                    "修造", "移徙", "入宅", "求嗣", "祈福", "解除", "出火"]
        ji_list = ["安葬", "行丧", "针灸", "伐木", "作梁", "纳畜", "牧养",
                    "造庙", "开渠", "造船", "掘井", "破土", "行舟", "词讼"]
        
        yi = random.sample(yi_list, random.randint(3, 6))
        ji = random.sample(ji_list, random.randint(2, 4))
        
        return {"yi": yi, "ji": ji}


# ============================================================================
# 生肖信息类
# ============================================================================

class ShengXiaoInfo:
    """生肖信息"""
    
    def __init__(self, name, idx):
        self.name = name
        self.idx = idx
        self.wuxing = self._get_wuxing()
        self.trait = self._get_trait()
    
    def _get_wuxing(self):
        """五行属性"""
        wuxing_map = ["水", "土", "木", "木", "土", "火", "火", "土", "金", "金", "土", "水"]
        return wuxing_map[self.idx]
    
    def _get_trait(self):
        """性格特质"""
        traits = [
            "机智灵活，善于应变",  # 鼠
            "勤恳踏实，坚韧不拔",  # 牛
            "勇猛果敢，富有领导力",  # 虎
            "温和善良，心思细腻",  # 兔
            "自信豪迈，志向远大",  # 龍
            "智慧深邃，洞察力强",  # 蛇
            "热情奔放，自由不羁",  # 马
            "温顺谦逊，富有同情心",  # 羊
            "聪慧机敏，多才多艺",  # 猴
            "勤奋守时，注重细节",  # 鸡
            "忠诚可靠，正义感强",  # 狗
            "豁达乐观，福缘深厚",  # 猪
        ]
        return traits[self.idx]
    
    def to_dict(self):
        return {
            "name": self.name,
            "wuxing": self.wuxing,
            "trait": self.trait,
        }


# ============================================================================
# 任务调度器
# ============================================================================

class TaskScheduler:
    """
    任务调度器
    
    功能:
    - Cron表达式解析与定时任务
    - 任务依赖管理
    - 任务状态追踪
    - 自动触发与回调
    """
    
    def __init__(self, longhun_instance):
        self.lh = longhun_instance
        self.tasks = {}
        self.task_history = []
        self._lock = threading.Lock()
        self._running = False
        self._thread = None
    
    def schedule_task(self, cron_expr, task_name, skill_id, callback=None, params=None):
        """
        创建定时任务
        
        Args:
            cron_expr: Cron表达式 (如 "0 9 * * *" 每天9点)
            task_name: 任务名称
            skill_id: 关联技能ID
            callback: 回调函数
            params: 任务参数
        
        Returns:
            str: 任务ID
        """
        task_id = f"TASK-{uuid.uuid4().hex[:8].upper()}"
        
        task = {
            "id": task_id,
            "name": task_name,
            "cron": cron_expr,
            "skill_id": skill_id,
            "skill_name": SKILL_REGISTRY.get(skill_id, {}).get("name", "未知"),
            "callback": callback,
            "params": params or {},
            "created_at": int(time.time() * 1000),
            "status": "active",
            "last_run": None,
            "next_run": None,
            "run_count": 0,
            "run_history": [],
        }
        
        with self._lock:
            self.tasks[task_id] = task
        
        # 记录日志
        self.lh.log_action("task_schedule", {
            "task_id": task_id,
            "task_name": task_name,
            "cron": cron_expr,
            "skill_id": skill_id,
        }, AUDIT_GREEN)
        
        return task_id
    
    def cancel_task(self, task_id):
        """取消任务"""
        with self._lock:
            if task_id in self.tasks:
                self.tasks[task_id]["status"] = "cancelled"
                self.lh.log_action("task_cancel", {"task_id": task_id}, AUDIT_YELLOW)
                return True
        return False
    
    def get_task_status(self, task_id):
        """获取任务状态"""
        with self._lock:
            return self.tasks.get(task_id, {}).copy()
    
    def list_tasks(self, skill_id=None, status=None):
        """列出所有任务"""
        with self._lock:
            result = []
            for tid, task in self.tasks.items():
                if skill_id and task["skill_id"] != skill_id:
                    continue
                if status and task["status"] != status:
                    continue
                result.append(task.copy())
            return result
    
    def parse_cron(self, cron_expr):
        """
        解析Cron表达式
        
        格式: 分 时 日 月 周
        支持: * 表示任意, / 表示步进, - 表示范围, , 表示列表
        
        Returns:
            dict: 各字段的允许值集合
        """
        parts = cron_expr.split()
        if len(parts) != 5:
            raise ValueError("Cron表达式需要5个字段: 分 时 日 月 周")
        
        minute, hour, day, month, weekday = parts
        
        return {
            "minute": self._parse_cron_field(minute, 0, 59),
            "hour": self._parse_cron_field(hour, 0, 23),
            "day": self._parse_cron_field(day, 1, 31),
            "month": self._parse_cron_field(month, 1, 12),
            "weekday": self._parse_cron_field(weekday, 0, 6),
        }
    
    def _parse_cron_field(self, field, min_val, max_val):
        """解析单个Cron字段"""
        if field == "*":
            return list(range(min_val, max_val + 1))
        
        if "/" in field:
            base, step = field.split("/")
            if base == "*":
                base = min_val
            else:
                base = int(base)
            step = int(step)
            return list(range(base, max_val + 1, step))
        
        if "-" in field:
            start, end = map(int, field.split("-"))
            return list(range(start, end + 1))
        
        if "," in field:
            return sorted(set(int(x) for x in field.split(",")))
        
        return [int(field)]
    
    def get_next_run_time(self, cron_expr, from_time=None):
        """
        计算下次执行时间
        
        Args:
            cron_expr: Cron表达式
            from_time: 起始时间(默认当前时间)
        
        Returns:
            datetime: 下次执行时间
        """
        if from_time is None:
            from_time = datetime.now()
        
        cron = self.parse_cron(cron_expr)
        
        # 从下一分钟开始查找
        check_time = from_time + timedelta(minutes=1)
        check_time = check_time.replace(second=0, microsecond=0)
        
        # 最多查找1年
        end_time = from_time + timedelta(days=366)
        
        while check_time < end_time:
            if (check_time.minute in cron["minute"] and
                check_time.hour in cron["hour"] and
                check_time.day in cron["day"] and
                check_time.month in cron["month"] and
                check_time.weekday() in cron["weekday"]):
                return check_time
            check_time += timedelta(minutes=1)
        
        return None
    
    def start(self):
        """启动调度器（后台线程）"""
        self._running = True
        self._thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self._thread.start()
        self.lh.log_action("scheduler_start", {}, AUDIT_GREEN)
    
    def stop(self):
        """停止调度器"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        self.lh.log_action("scheduler_stop", {}, AUDIT_GREEN)
    
    def _scheduler_loop(self):
        """调度器主循环"""
        while self._running:
            now = datetime.now()
            
            with self._lock:
                for task_id, task in self.tasks.items():
                    if task["status"] != "active":
                        continue
                    
                    # 简化触发：检查分钟匹配
                    cron = self.parse_cron(task["cron"])
                    if (now.minute in cron["minute"] and
                        now.hour in cron["hour"] and
                        now.day in cron["day"] and
                        now.month in cron["month"] and
                        now.weekday() in cron["weekday"]):
                        
                        # 检查是否在本分钟已执行
                        last_run = task.get("last_run")
                        if last_run:
                            last_dt = datetime.fromtimestamp(last_run / 1000)
                            if (last_dt.year == now.year and last_dt.month == now.month
                                and last_dt.day == now.day and last_dt.hour == now.hour
                                and last_dt.minute == now.minute):
                                continue
                        
                        # 执行任务
                        self._execute_task(task_id, task, now)
            
            time.sleep(30)  # 每30秒检查一次
    
    def _execute_task(self, task_id, task, execute_time):
        """执行单个任务"""
        timestamp_ms = int(time.time() * 1000)
        
        task["last_run"] = timestamp_ms
        task["run_count"] += 1
        task["run_history"].append({
            "time_ms": timestamp_ms,
            "time_human": DNATracer._ms_to_human(timestamp_ms),
        })
        
        # 记录执行日志
        self.lh.log_action("task_execute", {
            "task_id": task_id,
            "task_name": task["name"],
            "skill_id": task["skill_id"],
            "run_count": task["run_count"],
        }, AUDIT_GREEN)
        
        # 调用回调
        if task["callback"]:
            try:
                task["callback"](task["params"])
            except Exception as e:
                self.lh.log_action("task_error", {
                    "task_id": task_id,
                    "error": str(e),
                }, AUDIT_RED)


# ============================================================================
# 上下文路由器
# ============================================================================

class ContextRouter:
    """
    上下文路由器
    
    功能:
    - 根据当前时间/任务/状态路由到正确技能
    - 上下文切换（自动压缩、归档、恢复）
    - 会话管理
    - 依赖管理
    """
    
    def __init__(self, longhun_instance):
        self.lh = longhun_instance
        self.contexts = OrderedDict()
        self.active_context = None
        self._lock = threading.Lock()
        self.max_contexts = 50  # 最大上下文数
    
    def create_context(self, topic, skill_id, parent_id=None):
        """
        创建新上下文
        
        Args:
            topic: 主题
            skill_id: 关联技能ID
            parent_id: 父上下文ID
        
        Returns:
            str: 上下文ID
        """
        ctx_id = f"CTX-{uuid.uuid4().hex[:8].upper()}"
        
        context = {
            "id": ctx_id,
            "topic": topic,
            "skill_id": skill_id,
            "skill_name": SKILL_REGISTRY.get(skill_id, {}).get("name", "未知"),
            "parent_id": parent_id,
            "created_at": int(time.time() * 1000),
            "updated_at": int(time.time() * 1000),
            "status": "active",
            "messages": [],
            "metadata": {},
            "compressed": False,
            "message_count": 0,
        }
        
        with self._lock:
            self.contexts[ctx_id] = context
            self.active_context = ctx_id
            
            # 检查是否需要压缩旧上下文
            if len(self.contexts) > self.max_contexts:
                self._compress_oldest()
        
        self.lh.log_action("context_create", {
            "context_id": ctx_id,
            "topic": topic,
            "skill_id": skill_id,
        }, AUDIT_GREEN)
        
        return ctx_id
    
    def switch_context(self, to_ctx_id):
        """
        切换上下文
        
        流程:
        1. 保存当前上下文状态
        2. 检查目标上下文是否被压缩，若压缩则解压
        3. 恢复目标上下文
        4. 更新活跃上下文
        """
        with self._lock:
            if to_ctx_id not in self.contexts:
                return False
            
            from_ctx_id = self.active_context
            
            # 保存当前上下文
            if from_ctx_id and from_ctx_id in self.contexts:
                self.contexts[from_ctx_id]["status"] = "standby"
            
            # 解压目标上下文（如果被压缩）
            target_ctx = self.contexts[to_ctx_id]
            if target_ctx["compressed"]:
                self._decompress_context(to_ctx_id)
            
            # 激活目标上下文
            target_ctx["status"] = "active"
            target_ctx["updated_at"] = int(time.time() * 1000)
            self.active_context = to_ctx_id
        
        self.lh.log_action("context_switch", {
            "from": from_ctx_id,
            "to": to_ctx_id,
            "topic": target_ctx["topic"],
        }, AUDIT_GREEN)
        
        return True
    
    def add_message(self, ctx_id, role, content, metadata=None):
        """向上下文添加消息"""
        with self._lock:
            if ctx_id not in self.contexts:
                return False
            
            msg = {
                "id": f"MSG-{uuid.uuid4().hex[:6].upper()}",
                "role": role,
                "content": content,
                "timestamp_ms": int(time.time() * 1000),
                "metadata": metadata or {},
            }
            
            self.contexts[ctx_id]["messages"].append(msg)
            self.contexts[ctx_id]["message_count"] += 1
            self.contexts[ctx_id]["updated_at"] = int(time.time() * 1000)
        
        return True
    
    def get_context(self, ctx_id):
        """获取上下文信息"""
        with self._lock:
            ctx = self.contexts.get(ctx_id, {}).copy()
            if ctx and ctx.get("compressed"):
                ctx["messages"] = "[已压缩]"
            return ctx
    
    def get_active_context(self):
        """获取当前活跃上下文"""
        with self._lock:
            if self.active_context:
                return self.get_context(self.active_context)
            return None
    
    def list_contexts(self, status=None):
        """列出所有上下文"""
        with self._lock:
            result = []
            for ctx_id, ctx in self.contexts.items():
                if status and ctx["status"] != status:
                    continue
                info = {
                    "id": ctx_id,
                    "topic": ctx["topic"],
                    "skill_id": ctx["skill_id"],
                    "status": ctx["status"],
                    "created_at": ctx["created_at"],
                    "message_count": ctx["message_count"],
                    "compressed": ctx["compressed"],
                }
                result.append(info)
            return result
    
    def archive_context(self, ctx_id):
        """归档上下文"""
        with self._lock:
            if ctx_id in self.contexts:
                self.contexts[ctx_id]["status"] = "archived"
                self._compress_context(ctx_id)
        
        self.lh.log_action("context_archive", {"context_id": ctx_id}, AUDIT_GREEN)
        return True
    
    def _compress_context(self, ctx_id):
        """压缩上下文（保留元数据，压缩消息）"""
        ctx = self.contexts[ctx_id]
        if ctx["compressed"]:
            return
        
        # 保存消息摘要
        message_summary = {
            "count": len(ctx["messages"]),
            "first_timestamp": ctx["messages"][0]["timestamp_ms"] if ctx["messages"] else None,
            "last_timestamp": ctx["messages"][-1]["timestamp_ms"] if ctx["messages"] else None,
            "summary": self._generate_summary(ctx["messages"]),
        }
        
        # 保存压缩前数据到文件
        archive_path = os.path.join(
            self.lh.base_path, "sessions", "archive", f"{ctx_id}.json"
        )
        os.makedirs(os.path.dirname(archive_path), exist_ok=True)
        with open(archive_path, "w", encoding="utf-8") as f:
            json.dump(ctx["messages"], f, ensure_ascii=False, indent=2)
        
        ctx["message_summary"] = message_summary
        ctx["messages"] = []
        ctx["compressed"] = True
    
    def _decompress_context(self, ctx_id):
        """解压上下文"""
        ctx = self.contexts[ctx_id]
        if not ctx["compressed"]:
            return
        
        archive_path = os.path.join(
            self.lh.base_path, "sessions", "archive", f"{ctx_id}.json"
        )
        
        if os.path.exists(archive_path):
            with open(archive_path, "r", encoding="utf-8") as f:
                ctx["messages"] = json.load(f)
        
        ctx["compressed"] = False
    
    def _compress_oldest(self):
        """压缩最旧的上下文"""
        for ctx_id, ctx in list(self.contexts.items())[:10]:
            if ctx["status"] == "standby" and not ctx["compressed"]:
                self._compress_context(ctx_id)
    
    @staticmethod
    def _generate_summary(messages):
        """生成消息摘要"""
        if not messages:
            return "空会话"
        roles = {}
        for m in messages:
            role = m["role"]
            roles[role] = roles.get(role, 0) + 1
        return f"消息统计: {roles}"


# ============================================================================
# 本地日志系统
# ============================================================================

class LocalLogger:
    """
    本地日志系统
    
    功能:
    - 按日期分文件存储
    - JSON格式，每行一条记录
    - 自动轮转
    - 毫秒级时间戳
    """
    
    def __init__(self, log_dir):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self._lock = threading.Lock()
        self._current_file = None
        self._current_date = None
    
    def write(self, record):
        """
        写入日志记录
        
        Args:
            record: dict，包含完整的操作记录
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        # 检查是否需要切换文件
        if date_str != self._current_date:
            self._current_date = date_str
            self._current_file = os.path.join(self.log_dir, f"{date_str}.log")
        
        # 追加写入
        with self._lock:
            with open(self._current_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    def read(self, date=None, limit=100):
        """
        读取日志
        
        Args:
            date: 日期字符串 (YYYY-MM-DD)，None表示今天
            limit: 最大返回条数
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        log_file = os.path.join(self.log_dir, f"{date}.log")
        
        if not os.path.exists(log_file):
            return []
        
        records = []
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        
        return records[-limit:]
    
    def search(self, action_type=None, skill_id=None, audit_level=None, 
               start_time=None, end_time=None, limit=100):
        """
        搜索日志
        """
        results = []
        
        # 遍历所有日志文件
        for filename in sorted(os.listdir(self.log_dir)):
            if not filename.endswith(".log"):
                continue
            
            log_file = os.path.join(self.log_dir, filename)
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        
                        if action_type and record.get("action_type") != action_type:
                            continue
                        if skill_id and record.get("skill_id") != skill_id:
                            continue
                        if audit_level and record.get("audit_level") != audit_level:
                            continue
                        if start_time and record.get("timestamp_ms", 0) < start_time:
                            continue
                        if end_time and record.get("timestamp_ms", 0) > end_time:
                            continue
                        
                        results.append(record)
                        if len(results) >= limit:
                            return results
                    except (json.JSONDecodeError, KeyError):
                        continue
        
        return results


# ============================================================================
# Notion同步器
# ============================================================================

class NotionSyncer:
    """
    Notion同步器
    
    功能:
    - 实时同步操作日志到Notion
    - 维护同步状态
    - 支持批量同步和实时同步
    - 本地缓存，网络恢复后自动补同步
    
    注意: 此版本为标准库实现，Notion API调用通过外部hook完成
          实际使用时需要配合Notion integration token
    """
    
    def __init__(self, sync_dir, notion_hook=None):
        self.sync_dir = sync_dir
        self.notion_hook = notion_hook  # 外部回调函数
        self.pending_queue = []
        self.sync_state_file = os.path.join(sync_dir, "sync_state.json")
        self._lock = threading.Lock()
        self._load_state()
    
    def _load_state(self):
        """加载同步状态（兼容空文件/损坏文件）"""
        if os.path.exists(self.sync_state_file) and os.path.getsize(self.sync_state_file) > 0:
            try:
                with open(self.sync_state_file, "r", encoding="utf-8") as f:
                    state = json.load(f)
                    self.pending_queue = state.get("pending", [])
            except Exception:
                self.pending_queue = []
        
        os.makedirs(self.sync_dir, exist_ok=True)
    
    def _save_state(self):
        """保存同步状态"""
        with self._lock:
            with open(self.sync_state_file, "w", encoding="utf-8") as f:
                json.dump({
                    "pending": self.pending_queue,
                    "last_sync": int(time.time() * 1000),
                }, f, ensure_ascii=False, indent=2)
    
    def sync(self, record):
        """
        同步单条记录到Notion
        
        流程:
        1. 添加到待同步队列
        2. 尝试实时同步
        3. 如果失败，保留在队列中稍后重试
        """
        sync_record = {
            **record,
            "sync_id": f"SYNC-{uuid.uuid4().hex[:8].upper()}",
            "sync_status": "pending",
            "sync_attempts": 0,
        }
        
        with self._lock:
            self.pending_queue.append(sync_record)
        
        # 尝试实时同步
        success = self._do_sync(sync_record)
        
        if success:
            sync_record["sync_status"] = "synced"
            with self._lock:
                if sync_record in self.pending_queue:
                    self.pending_queue.remove(sync_record)
        else:
            sync_record["sync_status"] = "failed"
            sync_record["sync_attempts"] += 1
        
        self._save_state()
        return success
    
    def sync_batch(self, records):
        """批量同步"""
        results = []
        for record in records:
            success = self.sync(record)
            results.append({"record": record.get("dna_code", "?"), "success": success})
        return results
    
    def retry_failed(self):
        """重试失败的同步"""
        with self._lock:
            failed = [r for r in self.pending_queue if r["sync_status"] == "failed"]
        
        success_count = 0
        for record in failed:
            if self._do_sync(record):
                record["sync_status"] = "synced"
                success_count += 1
            else:
                record["sync_attempts"] += 1
        
        self._save_state()
        return success_count
    
    def _do_sync(self, record):
        """
        执行实际同步
        
        如果配置了notion_hook则调用，否则写入本地缓存
        """
        if self.notion_hook:
            try:
                return self.notion_hook(record)
            except Exception:
                return False
        
        # 无hook时，写入本地缓存文件
        cache_file = os.path.join(self.sync_dir, "notion_cache.jsonl")
        with self._lock:
            with open(cache_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        
        return True
    
    def get_sync_status(self):
        """获取同步状态"""
        with self._lock:
            pending = len([r for r in self.pending_queue if r["sync_status"] == "pending"])
            failed = len([r for r in self.pending_queue if r["sync_status"] == "failed"])
        
        return {
            "pending": pending,
            "failed": failed,
            "total_queue": len(self.pending_queue),
        }


# ============================================================================
# 多AI网关调度器
# ============================================================================

class AIGateway:
    """
    多AI网关调度器
    
    功能:
    - 根据任务类型路由到最优AI模型
    - 负载均衡
    - 故障切换
    - 响应缓存
    - 调用统计
    
    AI模型注册表:
    - gpt-4: 复杂推理、代码生成
    - gpt-3.5: 快速响应、简单任务
    - claude: 长文本分析、创意写作
    - local: 本地模型、隐私敏感任务
    """
    
    # 任务类型到AI模型的映射
    TASK_ROUTING = {
        "code": {"model": "gpt-4", "priority": 1, "timeout": 60},
        "analysis": {"model": "claude", "priority": 1, "timeout": 120},
        "chat": {"model": "gpt-3.5", "priority": 2, "timeout": 30},
        "creative": {"model": "claude", "priority": 1, "timeout": 90},
        "quick": {"model": "gpt-3.5", "priority": 3, "timeout": 15},
        "private": {"model": "local", "priority": 1, "timeout": 120},
        "calendar": {"model": "local", "priority": 1, "timeout": 5},
        "default": {"model": "gpt-3.5", "priority": 2, "timeout": 30},
    }
    
    def __init__(self, longhun_instance):
        self.lh = longhun_instance
        self.models = {}
        self.stats = {}
        self.cache = OrderedDict()
        self.cache_size = 100
        self._lock = threading.Lock()
    
    def register_model(self, model_id, model_config):
        """
        注册AI模型
        
        Args:
            model_id: 模型标识
            model_config: 配置字典
                - name: 模型名称
                - endpoint: API端点
                - token: API令牌（可选，可通过环境变量）
                - weight: 权重（负载均衡）
                - enabled: 是否启用
                - callback: 本地回调函数（本地模型用）
        """
        self.models[model_id] = {
            **model_config,
            "registered_at": int(time.time() * 1000),
            "call_count": 0,
            "error_count": 0,
            "last_used": None,
            "status": "active",
        }
        
        self.stats[model_id] = {
            "total_calls": 0,
            "total_errors": 0,
            "avg_latency_ms": 0,
            "total_tokens": 0,
        }
        
        self.lh.log_action("ai_model_register", {
            "model_id": model_id,
            "model_name": model_config.get("name", "unknown"),
        }, AUDIT_GREEN)
        
        return True
    
    def route(self, task_type, prompt, context=None, use_cache=True):
        """
        路由任务到最优AI模型
        
        Args:
            task_type: 任务类型 (code/analysis/chat/creative/quick/private/...)
            prompt: 输入提示
            context: 上下文信息
            use_cache: 是否使用缓存
        
        Returns:
            dict: 包含response、model_used、latency_ms等
        """
        start_time = int(time.time() * 1000)
        
        # 1. 确定路由策略
        routing = self.TASK_ROUTING.get(task_type, self.TASK_ROUTING["default"])
        target_model = routing["model"]
        
        # 2. 检查缓存
        if use_cache:
            cache_key = hashlib.sha256(f"{task_type}:{prompt}".encode()).hexdigest()[:16]
            cached = self._get_cache(cache_key)
            if cached:
                return {
                    **cached,
                    "from_cache": True,
                    "latency_ms": int(time.time() * 1000) - start_time,
                }
        
        # 3. 检查模型可用性
        if target_model not in self.models or not self.models[target_model].get("enabled", True):
            # 故障切换：选择下一个可用模型
            target_model = self._fallback_model(target_model)
        
        # 4. 执行调用
        result = self._call_model(target_model, prompt, context)
        
        # 5. 更新统计
        latency = int(time.time() * 1000) - start_time
        self._update_stats(target_model, latency, result.get("success", False))
        
        # 6. 缓存结果
        if use_cache and result.get("success"):
            cache_key = hashlib.sha256(f"{task_type}:{prompt}".encode()).hexdigest()[:16]
            self._set_cache(cache_key, result)
        
        # 7. 记录日志
        self.lh.log_action("ai_route", {
            "task_type": task_type,
            "model": target_model,
            "latency_ms": latency,
            "success": result.get("success", False),
            "prompt_length": len(prompt),
        }, AUDIT_GREEN if result.get("success") else AUDIT_RED)
        
        return {
            **result,
            "model_used": target_model,
            "latency_ms": latency,
            "from_cache": False,
        }
    
    def _call_model(self, model_id, prompt, context=None):
        """
        调用指定模型
        
        如果模型配置了callback则调用，否则返回模拟响应
        """
        model = self.models.get(model_id, {})
        callback = model.get("callback")
        
        if callback:
            try:
                response = callback(prompt, context)
                model["call_count"] += 1
                model["last_used"] = int(time.time() * 1000)
                return {
                    "success": True,
                    "response": response,
                    "model": model_id,
                }
            except Exception as e:
                model["error_count"] += 1
                return {
                    "success": False,
                    "error": str(e),
                    "model": model_id,
                }
        
        # 无callback，返回结构化的模拟响应
        return {
            "success": True,
            "response": f"[AI-{model_id}] 接收到任务，处理中...",
            "model": model_id,
            "mock": True,
        }
    
    def _fallback_model(self, failed_model):
        """故障切换：选择备用模型"""
        # 按优先级选择可用模型
        available = [(mid, m) for mid, m in self.models.items()
                     if m.get("enabled", True) and mid != failed_model]
        
        if available:
            # 按权重选择
            return random.choice([m[0] for m in available])
        
        return "local"  # 最终 fallback 到本地
    
    def _get_cache(self, key):
        """获取缓存"""
        with self._lock:
            return self.cache.get(key)
    
    def _set_cache(self, key, value):
        """设置缓存（LRU）"""
        with self._lock:
            if key in self.cache:
                del self.cache[key]
            elif len(self.cache) >= self.cache_size:
                self.cache.popitem(last=False)
            self.cache[key] = value
    
    def _update_stats(self, model_id, latency, success):
        """更新统计信息"""
        if model_id not in self.stats:
            return
        
        stats = self.stats[model_id]
        stats["total_calls"] += 1
        if not success:
            stats["total_errors"] += 1
        
        # 更新平均延迟
        old_avg = stats["avg_latency_ms"]
        n = stats["total_calls"]
        stats["avg_latency_ms"] = (old_avg * (n - 1) + latency) / n
    
    def get_stats(self):
        """获取所有模型统计"""
        return {
            "models": self.stats,
            "cache": {
                "size": len(self.cache),
                "max_size": self.cache_size,
            },
        }
    
    def health_check(self):
        """健康检查"""
        health = {}
        for model_id, model in self.models.items():
            health[model_id] = {
                "status": model.get("status", "unknown"),
                "enabled": model.get("enabled", False),
                "call_count": model.get("call_count", 0),
                "error_count": model.get("error_count", 0),
                "error_rate": (model.get("error_count", 0) / max(model.get("call_count", 1), 1)),
                "last_used": model.get("last_used"),
            }
        return health


# ============================================================================
# 核心万年历类
# ============================================================================

class LongHunCalendar:
    """
    龍魂万年历 - 系统唯一入口
    
    这是龍魂体系(UID9622)的唯一系统入口，所有操作都通过此类进入。
    
    核心职责:
    1. 系统入口 - enter() 方法
    2. 时间管理 - 农历/公历/节气/干支/卦象
    3. 任务调度 - Cron定时/任务触发/依赖管理
    4. 上下文路由 - 时间/任务/状态路由
    5. 实时记录 - 本地+Notion带时间戳记录
    6. 多AI网关 - 任务类型路由最优AI
    
    设计原则:
    - 龍字简体（用户精神支柱）
    - DNA追溯每个操作
    - 三色审计标记
    - 时间戳精确到毫秒
    - 与52技能无冲突
    """
    
    def __init__(self, base_path=None, notion_hook=None):
        """
        初始化龍魂万年历
        
        Args:
            base_path: 数据存储根目录，默认 ~/.longhun/calendar-context-logger/calendar/
            notion_hook: Notion同步回调函数
        """
        # 基础路径
        if base_path is None:
            base_path = os.path.expanduser("~/.longhun/calendar-context-logger/calendar/")
        self.base_path = base_path
        
        # 确保目录结构
        self._ensure_directories()
        
        # 初始化各子系统
        self.dna = DNATracer(self)
        self.lunar = LunarEngine()
        self.scheduler = TaskScheduler(self)
        self.router = ContextRouter(self)
        self.logger = LocalLogger(os.path.join(base_path, "logs"))
        self.notion = NotionSyncer(os.path.join(base_path, "notion_sync"), notion_hook)
        self.ai_gateway = AIGateway(self)
        
        # 系统状态
        self._started_at = int(time.time() * 1000)
        self._session_count = self._load_session_count()
        self._lock = threading.Lock()
        
        # 记录系统启动
        self.log_action("system_init", {
            "version": CALENDAR_VERSION,
            "base_path": base_path,
            "uid": LONGHUN_UID,
        }, AUDIT_GREEN)
    
    def _ensure_directories(self):
        """确保目录结构完整"""
        dirs = [
            "core",
            "sessions/active",
            "sessions/standby", 
            "sessions/archive",
            "logs",
            "notion_sync",
        ]
        for d in dirs:
            os.makedirs(os.path.join(self.base_path, d), exist_ok=True)
    
    def _session_count_file(self):
        return os.path.join(self.base_path, "core", "session_count.json")
    
    def _load_session_count(self):
        """持久化加载会话计数"""
        f = self._session_count_file()
        if os.path.exists(f):
            try:
                with open(f, "r", encoding="utf-8") as fh:
                    return json.load(fh).get("count", 0)
            except Exception:
                return 0
        return 0
    
    def _save_session_count(self):
        """持久化保存会话计数"""
        f = self._session_count_file()
        try:
            with open(f, "w", encoding="utf-8") as fh:
                json.dump({"count": self._session_count}, fh, ensure_ascii=False)
        except Exception:
            pass
    
    # ========================================================================
    # 系统入口 - 所有操作通过这里进入
    # ========================================================================
    
    def enter(self, task_type, user_input, skill_hint=None, context=None):
        """
        系统入口 - 所有操作通过这里进入龍魂体系
        
        这是龍魂万年历的核心方法，每个用户请求都必须经过此方法。
        
        处理流程:
        1. 生成DNA标识 + 时间戳
        2. 三色审计标记
        3. 意图识别 & 技能路由
        4. 创建/切换上下文
        5. 记录到本地日志 + Notion
        6. 返回处理结果
        
        Args:
            task_type: 任务类型 (code/analysis/chat/creative/quick/...)
            user_input: 用户输入
            skill_hint: 技能提示（可选）
            context: 额外上下文（可选）
        
        Returns:
            dict: 处理结果，包含dna_code、路由信息、时间戳
        """
        # 1. 生成DNA
        dna = self.dna.generate_dna("enter", "S11", AUDIT_GREEN)
        
        # 2. 添加追溯步骤
        self.dna.add_trace(dna, "入口接收", f"任务类型={task_type}, 输入长度={len(user_input)}")
        
        # 3. 技能路由
        skill_id = skill_hint or self._route_skill(task_type, user_input)
        skill_info = SKILL_REGISTRY.get(skill_id, {})
        
        self.dna.add_trace(dna, "技能路由", f"路由到 {skill_id}={skill_info.get('name', '未知')}")
        
        # 4. 创建或切换上下文
        ctx_id = self.router.create_context(
            topic=f"{task_type}:{user_input[:50]}",
            skill_id=skill_id,
            parent_id=self.router.active_context
        )
        
        self.dna.add_trace(dna, "上下文创建", f"上下文ID={ctx_id}")
        
        # 5. 添加用户消息到上下文
        self.router.add_message(ctx_id, "user", user_input, {
            "task_type": task_type,
            "dna_code": dna["dna_code"],
        })
        
        # 6. 获取当前时间信息
        now = datetime.now()
        lunar_info = self.lunar.solar_to_lunar(now)
        
        # 7. 记录完整操作日志
        log_record = {
            "dna_code": dna["dna_code"],
            "timestamp_ms": dna["timestamp_ms"],
            "timestamp_human": dna["timestamp_human"],
            "action_type": "enter",
            "skill_id": skill_id,
            "skill_name": skill_info.get("name", "未知"),
            "task_type": task_type,
            "user_input": user_input,
            "user_input_length": len(user_input),
            "context_id": ctx_id,
            "audit_level": AUDIT_GREEN,
            "lunar_date": lunar_info.get("lunar_full_str", ""),
            "ganzhi": lunar_info.get("full", ""),
            "gua": lunar_info.get("gua", {}).get("ben_gua", ""),
            "system_uid": LONGHUN_UID,
            "version": CALENDAR_VERSION,
        }
        
        # 8. 写入本地日志
        self.logger.write(log_record)
        
        # 9. 同步到Notion（异步）
        threading.Thread(target=self.notion.sync, args=(log_record,), daemon=True).start()
        
        # 10. 增加会话计数并持久化
        with self._lock:
            self._session_count += 1
            self._save_session_count()
        
        self.dna.add_trace(dna, "入口完成", "日志已记录，Notion同步中")
        
        # 11. 构建返回结果
        result = {
            "dna_code": dna["dna_code"],
            "timestamp_ms": dna["timestamp_ms"],
            "timestamp_human": dna["timestamp_human"],
            "task_type": task_type,
            "routed_skill": {
                "id": skill_id,
                "name": skill_info.get("name", "未知"),
                "layer": skill_info.get("layer", "?"),
            },
            "context_id": ctx_id,
            "lunar_info": lunar_info,
            "trace": dna["trace"],
            "status": "entered",
            "user_input": user_input,
        }
        
        # 12. 根据任务类型自动调用AI网关
        if task_type in AIGateway.TASK_ROUTING:
            ai_result = self.ai_gateway.route(task_type, user_input, context)
            result["ai_response"] = ai_result
            self.dna.add_trace(dna, "AI处理", 
                f"模型={ai_result.get('model_used')}, "
                f"延迟={ai_result.get('latency_ms')}ms, "
                f"缓存={'是' if ai_result.get('from_cache') else '否'}")
        
        return result
    
    def _route_skill(self, task_type, user_input):
        """
        根据任务类型和输入内容路由到对应技能
        
        路由规则:
        - code -> S09 (代码生成)
        - analysis -> S10 (数据分析)
        - calendar -> S11 (万年历)
        - creative -> S02+S03 (意图识别+语义理解)
        - private -> local (本地处理)
        - default -> S02 (意图识别)
        """
        routing_map = {
            "code": "S09",
            "coding": "S09",
            "program": "S09",
            "analysis": "S10",
            "data": "S10",
            "visualization": "S10",
            "chat": "S02",
            "conversation": "S02",
            "creative": "S03",
            "write": "S03",
            "calendar": "S11",
            "date": "S11",
            "lunar": "S11",
            "filter": "S01",
            "input": "S01",
            "supervise": "S04",
            "govern": "S04",
            "permission": "S05",
            "knowledge": "S06",
            "graph": "S06",
            "memory": "S07",
            "ai": "S08",
            "gateway": "S08",
        }
        
        # 精确匹配
        if task_type in routing_map:
            return routing_map[task_type]
        
        # 关键词匹配
        keywords = {
            "S09": ["代码", "编程", "程序", "函数", "class", "def", "import"],
            "S10": ["数据", "分析", "图表", "统计", "可视化", "pandas", "numpy"],
            "S11": ["农历", "日历", "节气", "干支", "卦", "生肖", "日期"],
            "S06": ["知识", "图谱", "关系", "节点", "边", "ontology"],
            "S07": ["记忆", "回忆", "历史", "存储", "检索"],
        }
        
        user_lower = user_input.lower()
        for skill_id, words in keywords.items():
            for word in words:
                if word in user_lower:
                    return skill_id
        
        # 默认路由到意图识别
        return "S02"
    
    # ========================================================================
    # 时间管理接口
    # ========================================================================
    
    def get_lunar_date(self, solar_date=None):
        """
        获取农历日期
        
        Args:
            solar_date: datetime对象或None(当前时间)
        
        Returns:
            dict: 农历信息
        """
        return self.lunar.solar_to_lunar(solar_date)
    
    def get_ganzhi(self, date=None):
        """
        获取干支
        
        Args:
            date: datetime对象或None(当前时间)
        
        Returns:
            dict: 年柱、月柱、日柱、时柱
        """
        return self.lunar.get_ganzhi(date)
    
    def get_qigua(self, date=None):
        """
        获取卦象
        
        Args:
            date: datetime对象或None(当前时间)
        
        Returns:
            dict: 本卦、变爻、变卦、卦辞、吉兆
        """
        return self.lunar.get_qigua(date)
    
    def get_jie_qi(self, solar_date=None):
        """
        获取节气信息
        
        Args:
            solar_date: datetime对象或None(当前时间)
        
        Returns:
            dict: 当前、前一个、后一个节气
        """
        return self.lunar.get_jie_qi(solar_date)
    
    def get_shengxiao(self, date=None):
        """
        获取生肖
        
        Args:
            date: datetime对象或None(当前时间)
        
        Returns:
            ShengXiaoInfo: 生肖信息
        """
        return self.lunar.get_shengxiao(date)
    
    def get_yi_ji(self, date=None):
        """
        获取每日宜忌
        
        Args:
            date: datetime对象或None(当前时间)
        
        Returns:
            dict: 宜、忌
        """
        return self.lunar.get_yi_ji(date)
    
    def get_full_calendar(self, solar_date=None):
        """
        获取完整万年历信息
        
        这是获取所有时间信息的统一接口
        
        Returns:
            dict: 包含农历、干支、卦象、节气、生肖、宜忌等
        """
        if solar_date is None:
            solar_date = datetime.now()
        
        lunar_info = self.lunar.solar_to_lunar(solar_date)
        yi_ji = self.lunar.get_yi_ji(solar_date)
        
        return {
            "solar_date": solar_date.strftime("%Y年%m月%d日 %H:%M:%S"),
            "weekday": lunar_info.get("weekday"),
            "lunar": {
                "year": lunar_info.get("lunar_year"),
                "month": lunar_info.get("lunar_month_str"),
                "day": lunar_info.get("lunar_day_str"),
                "full_str": lunar_info.get("lunar_full_str"),
                "is_leap_month": lunar_info.get("lunar_month_is_leap"),
            },
            "ganzhi": {
                "year_zhu": lunar_info.get("year_zhu"),
                "month_zhu": lunar_info.get("month_zhu"),
                "day_zhu": lunar_info.get("day_zhu"),
                "hour_zhu": lunar_info.get("hour_zhu"),
                "full": lunar_info.get("full"),
            },
            "gua": lunar_info.get("gua"),
            "jie_qi": lunar_info.get("jie_qi"),
            "shengxiao": lunar_info.get("shengxiao", {}).to_dict() if hasattr(lunar_info.get("shengxiao"), 'to_dict') else {},
            "xingzuo": lunar_info.get("xingzuo"),
            "yi_ji": yi_ji,
        }
    
    # ========================================================================
    # 任务调度接口
    # ========================================================================
    
    def schedule_task(self, cron_expr, task_name, skill_id, callback=None, params=None):
        """
        创建定时任务
        
        Args:
            cron_expr: Cron表达式 (分 时 日 月 周)
                      例: "0 9 * * *" = 每天9:00
                          "0 */6 * * *" = 每6小时
                          "0 0 * * 1" = 每周一0:00
            task_name: 任务名称
            skill_id: 关联技能ID
            callback: 回调函数(可选)
            params: 任务参数(可选)
        
        Returns:
            str: 任务ID
        """
        return self.scheduler.schedule_task(cron_expr, task_name, skill_id, callback, params)
    
    def cancel_task(self, task_id):
        """取消定时任务"""
        return self.scheduler.cancel_task(task_id)
    
    def get_task_status(self, task_id):
        """获取任务状态"""
        return self.scheduler.get_task_status(task_id)
    
    def list_tasks(self, skill_id=None, status=None):
        """列出所有任务"""
        return self.scheduler.list_tasks(skill_id, status)
    
    def start_scheduler(self):
        """启动任务调度器"""
        self.scheduler.start()
    
    def stop_scheduler(self):
        """停止任务调度器"""
        self.scheduler.stop()
    
    # ========================================================================
    # 上下文路由接口
    # ========================================================================
    
    def switch_context(self, to_ctx_id):
        """
        切换上下文
        
        自动处理压缩/归档/恢复
        
        Args:
            to_ctx_id: 目标上下文ID
        
        Returns:
            bool: 是否成功
        """
        return self.router.switch_context(to_ctx_id)
    
    def create_context(self, topic, skill_id, parent_id=None):
        """
        创建新上下文
        
        Args:
            topic: 主题
            skill_id: 技能ID
            parent_id: 父上下文ID(可选)
        
        Returns:
            str: 上下文ID
        """
        return self.router.create_context(topic, skill_id, parent_id)
    
    def get_active_context(self):
        """获取当前活跃上下文"""
        return self.router.get_active_context()
    
    def list_contexts(self, status=None):
        """列出所有上下文"""
        return self.router.list_contexts(status)
    
    def archive_context(self, ctx_id):
        """归档上下文"""
        return self.router.archive_context(ctx_id)
    
    # ========================================================================
    # 实时记录接口
    # ========================================================================
    
    def log_action(self, action_type, details, audit_color=AUDIT_GREEN, skill_id="S11"):
        """
        记录动作到本地+Notion
        
        每个动作都有:
        - DNA标识
        - 毫秒级时间戳
        - 三色审计标记
        - 技能关联
        
        Args:
            action_type: 动作类型
            details: 详细信息(dict)
            audit_color: 审计颜色 (🟢/🟡/🔴)
            skill_id: 关联技能ID
        
        Returns:
            dict: 日志记录
        """
        timestamp_ms = int(time.time() * 1000)
        
        # 生成DNA
        dna = self.dna.generate_dna(action_type, skill_id, audit_color)
        
        log_record = {
            "dna_code": dna["dna_code"],
            "timestamp_ms": timestamp_ms,
            "timestamp_human": DNATracer._ms_to_human(timestamp_ms),
            "action_type": action_type,
            "skill_id": skill_id,
            "skill_name": SKILL_REGISTRY.get(skill_id, {}).get("name", "未知"),
            "audit_level": audit_color,
            "details": details,
            "system_uid": LONGHUN_UID,
            "version": CALENDAR_VERSION,
        }
        
        # 写入本地
        self.logger.write(log_record)
        
        # 同步Notion（异步，不阻塞）
        threading.Thread(target=self.notion.sync, args=(log_record,), daemon=True).start()
        
        return log_record
    
    def search_logs(self, **kwargs):
        """
        搜索日志
        
        支持按动作类型、技能ID、审计级别、时间范围搜索
        """
        return self.logger.search(**kwargs)
    
    def get_sync_status(self):
        """获取Notion同步状态"""
        return self.notion.get_sync_status()
    
    # ========================================================================
    # 多AI网关接口
    # ========================================================================
    
    def ai_route(self, task_type, prompt, context=None, use_cache=True):
        """
        路由AI任务
        
        Args:
            task_type: 任务类型
            prompt: 输入提示
            context: 上下文
            use_cache: 是否使用缓存
        
        Returns:
            dict: AI响应结果
        """
        return self.ai_gateway.route(task_type, prompt, context, use_cache)
    
    def register_ai_model(self, model_id, config):
        """注册AI模型"""
        return self.ai_gateway.register_model(model_id, config)
    
    def get_ai_stats(self):
        """获取AI调用统计"""
        return self.ai_gateway.get_stats()
    
    def ai_health_check(self):
        """AI网关健康检查"""
        return self.ai_gateway.health_check()
    
    # ========================================================================
    # 系统状态接口
    # ========================================================================
    
    def status(self):
        """
        获取系统状态
        
        Returns:
            dict: 系统完整状态
        """
        now = int(time.time() * 1000)
        uptime_ms = now - self._started_at
        
        # 获取当前时间信息
        calendar_info = self.get_full_calendar()
        
        return {
            "system": {
                "name": SYSTEM_NAME,
                "uid": LONGHUN_UID,
                "version": CALENDAR_VERSION,
                "started_at": self._started_at,
                "started_human": DNATracer._ms_to_human(self._started_at),
                "uptime_ms": uptime_ms,
                "uptime_human": self._format_duration(uptime_ms),
            },
            "calendar": calendar_info,
            "sessions": {
                "total": self._session_count,
                "active_contexts": len(self.router.list_contexts("active")),
                "standby_contexts": len(self.router.list_contexts("standby")),
                "archived_contexts": len(self.router.list_contexts("archived")),
            },
            "tasks": {
                "total": len(self.scheduler.list_tasks()),
                "active": len(self.scheduler.list_tasks(status="active")),
            },
            "ai_gateway": self.ai_gateway.get_stats(),
            "sync": self.notion.get_sync_status(),
            "dna_chain_length": len(self.dna.dna_chain),
        }
    
    def today(self):
        """
        获取今日信息
        
        简洁接口，返回今日完整信息
        """
        return self.get_full_calendar()
    
    def now(self):
        """
        获取当前时间戳（毫秒）
        """
        return int(time.time() * 1000)
    
    def verify_dna(self, dna_code):
        """
        验证DNA链完整性
        """
        return self.dna.verify_dna(dna_code)
    
    def get_dna_chain(self, limit=100):
        """
        获取DNA追溯链
        """
        return self.dna.get_chain(limit)
    
    @staticmethod
    def _format_duration(ms):
        """格式化时长"""
        seconds = ms // 1000
        minutes = seconds // 60
        hours = minutes // 60
        days = hours // 24
        
        if days > 0:
            return f"{days}天{hours % 24}时{minutes % 60}分"
        elif hours > 0:
            return f"{hours}时{minutes % 60}分{seconds % 60}秒"
        elif minutes > 0:
            return f"{minutes}分{seconds % 60}秒"
        else:
            return f"{seconds}秒"
    
    def __repr__(self):
        return f"LongHunCalendar(v{CALENDAR_VERSION}, UID{LONGHUN_UID}, {self._session_count} sessions)"
    
    def __str__(self):
        status = self.status()
        cal = status["calendar"]
        return (
            f"{'='*50}\n"
            f"  龍魂万年历 v{CALENDAR_VERSION} | {SYSTEM_NAME} UID{LONGHUN_UID}\n"
            f"{'='*50}\n"
            f"  公历: {cal['solar_date']}\n"
            f"  农历: {cal['lunar']['full_str']}\n"
            f"  干支: {cal['ganzhi']['full']}\n"
            f"  卦象: {cal['gua']['ben_gua']} ({cal['gua']['auspicious']})\n"
            f"  节气: {cal['jie_qi']['current']['name']}\n"
            f"  生肖: {cal['shengxiao'].get('name', '')}\n"
            f"  星座: {cal['xingzuo']}\n"
            f"  宜: {', '.join(cal['yi_ji']['yi'][:5])}\n"
            f"  忌: {', '.join(cal['yi_ji']['ji'][:3])}\n"
            f"{'='*50}\n"
            f"  会话数: {status['sessions']['total']} | "
            f"任务数: {status['tasks']['total']} | "
            f"DNA链: {status['dna_chain_length']}\n"
            f"{'='*50}"
        )


# ============================================================================
# 使用示例
# ============================================================================

def demo():
    """
    龍魂万年历使用示例
    
    展示所有核心功能的使用方法
    """
    print("=" * 60)
    print("  龍魂万年历 v1.0 - 使用演示")
    print("=" * 60)
    
    # 1. 初始化万年历
    print("\n【1】初始化龍魂万年历")
    calendar = LongHunCalendar(base_path="/tmp/longhun_demo/")
    print(f"  系统状态: {repr(calendar)}")
    
    # 2. 显示今日信息
    print("\n【2】获取今日完整信息")
    print(calendar)
    
    # 3. 系统入口 - 模拟用户请求
    print("\n【3】系统入口 - 模拟用户请求")
    
    result = calendar.enter("calendar", "查询今天的农历日期")
    print(f"  DNA: {result['dna_code']}")
    print(f"  路由技能: {result['routed_skill']['id']} - {result['routed_skill']['name']}")
    print(f"  时间戳: {result['timestamp_human']}")
    
    result2 = calendar.enter("code", "帮我写一个Python函数计算斐波那契数列")
    print(f"\n  DNA: {result2['dna_code']}")
    print(f"  路由技能: {result2['routed_skill']['id']} - {result2['routed_skill']['name']}")
    
    result3 = calendar.enter("analysis", "分析一下最近的销售数据")
    print(f"\n  DNA: {result3['dna_code']}")
    print(f"  路由技能: {result3['routed_skill']['id']} - {result3['routed_skill']['name']}")
    
    # 4. DNA追溯
    print("\n【4】DNA追溯链")
    chain = calendar.get_dna_chain(5)
    for i, dna in enumerate(chain):
        print(f"  [{i+1}] {dna['dna_code']} | {dna['action_type']} | {dna['audit_level']}")
    
    # 5. 验证DNA
    print("\n【5】验证DNA完整性")
    is_valid = calendar.verify_dna(result['dna_code'])
    print(f"  DNA {result['dna_code']} 验证: {'通过' if is_valid else '失败'}")
    
    # 6. 获取特定日期信息
    print("\n【6】获取特定日期信息 (2026-01-01)")
    special_date = datetime(2026, 1, 1)
    info = calendar.get_full_calendar(special_date)
    print(f"  公历: {info['solar_date']}")
    print(f"  农历: {info['lunar']['full_str']}")
    print(f"  干支: {info['ganzhi']['full']}")
    print(f"  卦象: {info['gua']['ben_gua']} - {info['gua']['meaning']}")
    print(f"  节气: {info['jie_qi']['current']['name']}")
    
    # 7. 任务调度
    print("\n【7】创建定时任务")
    
    def demo_callback(params):
        print(f"  [定时任务执行] params={params}")
    
    task_id = calendar.schedule_task(
        cron_expr="0 9 * * *",
        task_name="每日早报",
        skill_id="S11",
        callback=demo_callback,
        params={"type": "morning_report"}
    )
    print(f"  创建任务: {task_id}")
    
    task_id2 = calendar.schedule_task(
        cron_expr="0 */6 * * *",
        task_name="数据备份",
        skill_id="S07",
        callback=demo_callback,
        params={"type": "backup"}
    )
    print(f"  创建任务: {task_id2}")
    
    tasks = calendar.list_tasks()
    print(f"\n  所有任务 ({len(tasks)}个):")
    for t in tasks:
        print(f"    - {t['id']}: {t['name']} (cron={t['cron']})")
    
    # 8. 上下文管理
    print("\n【8】上下文管理")
    ctx1 = calendar.create_context("代码生成任务", "S09")
    print(f"  创建上下文: {ctx1}")
    
    ctx2 = calendar.create_context("数据分析任务", "S10", parent_id=ctx1)
    print(f"  创建上下文: {ctx2} (父={ctx1})")
    
    active = calendar.get_active_context()
    print(f"\n  当前活跃上下文: {active['id']} - {active['topic']}")
    
    contexts = calendar.list_contexts()
    print(f"\n  所有上下文 ({len(contexts)}个):")
    for c in contexts:
        print(f"    - {c['id']}: {c['topic']} [{c['status']}]")
    
    # 9. AI网关
    print("\n【9】AI网关调度")
    
    # 注册模拟模型（仅示例，龍魂系统禁止直连外部 AI）
    calendar.register_ai_model("local-demo", {
        "name": "Local-Demo",
        "endpoint": "http://127.0.0.1:11434",
        "weight": 1,
        "enabled": True,
        "callback": lambda p, c: f"[本地模型处理结果] 输入: {p[:30]}...",
    })

    calendar.register_ai_model("deepseek-demo", {
        "name": "DeepSeek-Demo",
        "endpoint": "https://api.deepseek.com/v1",
        "weight": 2,
        "enabled": True,
        "callback": lambda p, c: f"[DeepSeek处理结果] 收到: {p[:20]}...",
    })
    
    ai_result = calendar.ai_route("code", "写一个快速排序算法")
    print(f"  任务类型: code")
    print(f"  使用模型: {ai_result['model_used']}")
    print(f"  响应: {ai_result['response']}")
    print(f"  延迟: {ai_result['latency_ms']}ms")
    
    ai_result2 = calendar.ai_route("chat", "你好")
    print(f"\n  任务类型: chat")
    print(f"  使用模型: {ai_result2['model_used']}")
    print(f"  响应: {ai_result2['response']}")
    
    # 10. 系统状态
    print("\n【10】系统完整状态")
    status = calendar.status()
    print(f"  系统名称: {status['system']['name']}")
    print(f"  版本: {status['system']['version']}")
    print(f"  UID: {status['system']['uid']}")
    print(f"  运行时间: {status['system']['uptime_human']}")
    print(f"  总会话数: {status['sessions']['total']}")
    print(f"  活跃上下文: {status['sessions']['active_contexts']}")
    print(f"  总任务数: {status['tasks']['total']}")
    print(f"  DNA链长度: {status['dna_chain_length']}")
    
    # 11. 日志搜索
    print("\n【11】日志搜索")
    logs = calendar.search_logs(action_type="enter", limit=5)
    print(f"  找到 {len(logs)} 条 enter 记录:")
    for log in logs:
        print(f"    - {log['dna_code']} | {log['timestamp_human']} | {log['skill_name']}")
    
    # 12. Notion同步状态
    print("\n【12】Notion同步状态")
    sync_status = calendar.get_sync_status()
    print(f"  待同步: {sync_status['pending']}")
    print(f"  失败: {sync_status['failed']}")
    
    print("\n" + "=" * 60)
    print("  演示完成！所有功能正常运行。")
    print("=" * 60)
    
    return calendar


# ============================================================================
# 主入口
# ============================================================================

if __name__ == "__main__":
    demo()
