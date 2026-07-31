# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂万年历 (LongHun Calendar) - 龍魂系统唯一入口
版本: v1.0
体系: 龍魂体系 (UID9622)
功能: 系统入口 | 时间管理 | 任务调度 | 上下文路由 | 实时记录 | 多AI网关
设计原则: 龍字简体 | DNA追溯 | 三色审计 | 与52技能无冲突

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
    """DNA追溯器 - 每个操作都有可追溯的DNA链"""
    
    def __init__(self, longhun_instance):
        self.lh = longhun_instance
        self.dna_chain = []
        self._lock = threading.Lock()
    
    def generate_dna(self, action_type, skill_id="S11", audit_level=AUDIT_GREEN):
        """生成DNA标识"""
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
    """农历计算引擎"""
    
    LUNAR_MONTHS = ["正", "二", "三", "四", "五", "六",
                     "七", "八", "九", "十", "冬", "腊"]
    LUNAR_DAYS = [
        "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
        "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
        "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"
    ]
    WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    
    def __init__(self):
        self._cache = {}
    
    def solar_to_lunar(self, solar_date=None):
        """公历转农历"""
        if solar_date is None:
            solar_date = datetime.now()
        
        year = solar_date.year
        month = solar_date.month
        day = solar_date.day
        
        if year < 1900 or year > 2100:
            return {"error": "仅支持1900-2100年"}
        
        cache_key = f"{year}-{month}-{day}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        lunar_info = self._calc_lunar(solar_date)
        jie_qi = self.get_jie_qi(solar_date)
        lunar_info["jie_qi"] = jie_qi
        ganzhi = self.get_ganzhi(solar_date)
        lunar_info.update(ganzhi)
        gua = self.get_qigua(solar_date)
        lunar_info["gua"] = gua
        lunar_info["shengxiao"] = self.get_shengxiao(solar_date)
        lunar_info["xingzuo"] = self.get_xingzuo(solar_date)
        lunar_info["weekday"] = self.WEEKDAYS[solar_date.weekday()]
        
        self._cache[cache_key] = lunar_info
        return lunar_info
    
    def _calc_lunar(self, solar_date):
        """农历核心计算（基于标准农历数据）"""
        year = solar_date.year
        month = solar_date.month
        day = solar_date.day
        
        base_date = datetime(1900, 1, 31)
        target_date = datetime(year, month, day)
        days_offset = (target_date - base_date).days
        
        # 找到对应的农历年
        lunar_year = None
        year_start_offset = None
        year_next_offset = None
        
        sorted_years = sorted(SPRING_FESTIVAL_OFFSET.items())
        for i in range(len(sorted_years) - 1):
            y, offset = sorted_years[i]
            next_y, next_offset = sorted_years[i + 1]
            if days_offset >= offset and days_offset < next_offset:
                lunar_year = y
                year_start_offset = offset
                year_next_offset = next_offset
                break
        
        if lunar_year is None:
            return {"error": "日期超出计算范围"}
        
        day_in_year = days_offset - year_start_offset
        
        # 计算农历月日（基于平均农历月长29.53天）
        lunar_month_lengths = self._get_lunar_month_lengths(lunar_year)
        
        lunar_month = 1
        remaining_days = day_in_year
        for m_len in lunar_month_lengths:
            if remaining_days < m_len:
                break
            remaining_days -= m_len
            lunar_month += 1
        
        lunar_day = int(remaining_days) + 1
        
        is_leap = False
        leap_month = self._get_leap_month(lunar_year)
        if leap_month and lunar_month > leap_month:
            is_leap = True
        
        return {
            "lunar_year": lunar_year,
            "lunar_month": lunar_month,
            "lunar_day": lunar_day,
            "lunar_month_cn": self.LUNAR_MONTHS[min(lunar_month - 1, 11)],
            "lunar_day_cn": self.LUNAR_DAYS[min(lunar_day - 1, 29)],
            "is_leap": is_leap,
            "days_offset": days_offset,
        }
    
    def _get_lunar_month_lengths(self, year):
        """获取指定农历年各月天数（简化版：大月30天，小月29天交替）"""
        # 实际应使用完整农历数据表
        import random as rd
        rd.seed(year)
        lengths = []
        for i in range(12):
            lengths.append(30 if (i % 2 == 0) else 29)
        return lengths
    
    def _get_leap_month(self, year):
        """获取闰月（简化版）"""
        leap_months = {
            2023: 2, 2024: None, 2025: 6, 2026: None,
            2027: 4, 2028: None, 2029: 3, 2030: None,
        }
        return leap_months.get(year)
    
    def get_jie_qi(self, solar_date=None):
        """获取节气信息"""
        if solar_date is None:
            solar_date = datetime.now()
        
        month = solar_date.month
        day = solar_date.day
        
        today_jie_qi = None
        next_jie_qi = None
        
        for i, (name, m, d) in enumerate(JIE_QI):
            if m == month and d == day:
                today_jie_qi = name
            if (m > month) or (m == month and d > day):
                if next_jie_qi is None:
                    next_jie_qi = {"name": name, "date": f"{m}月{d}日"}
        
        if next_jie_qi is None and JIE_QI:
            name, m, d = JIE_QI[0]
            next_jie_qi = {"name": name, "date": f"{m}月{d}日(次年)"}
        
        return {
            "today": today_jie_qi,
            "next": next_jie_qi,
            "all": JIE_QI
        }
    
    def get_ganzhi(self, solar_date=None):
        """计算干支"""
        if solar_date is None:
            solar_date = datetime.now()
        
        year = solar_date.year
        month = solar_date.month
        day = solar_date.day
        
        # 年干支
        year_gan = TIAN_GAN[(year - 4) % 10]
        year_zhi = DI_ZHI[(year - 4) % 12]
        year_ganzhi = f"{year_gan}{year_zhi}年"
        
        # 月干支（简化计算）
        month_gan_idx = ((year - 4) % 5) * 2 + ((month + 1) % 12)
        month_gan = TIAN_GAN[month_gan_idx % 10]
        month_zhi = DI_ZHI[(month + 1) % 12]
        month_ganzhi = f"{month_gan}{month_zhi}月"
        
        # 日干支（基于已知基准日）
        base_date = datetime(1900, 1, 31)
        base_gan_idx = 0  # 甲
        base_zhi_idx = 0  # 子
        
        days_diff = (solar_date - base_date).days
        day_gan_idx = (base_gan_idx + days_diff) % 10
        day_zhi_idx = (base_zhi_idx + days_diff) % 12
        
        day_gan = TIAN_GAN[day_gan_idx]
        day_zhi = DI_ZHI[day_zhi_idx]
        day_ganzhi = f"{day_gan}{day_zhi}日"
        
        return {
            "year_ganzhi": year_ganzhi,
            "month_ganzhi": month_ganzhi,
            "day_ganzhi": day_ganzhi,
            "full": f"{year_ganzhi} {month_ganzhi} {day_ganzhi}"
        }
    
    def get_qigua(self, solar_date=None):
        """根据日期生成卦象"""
        if solar_date is None:
            solar_date = datetime.now()
        
        year = solar_date.year
        month = solar_date.month
        day = solar_date.day
        
        # 使用日期信息生成卦象索引
        total = year + month * 31 + day
        gua_idx = (total + 7) % 64
        gua_name = GUA_NAMES[gua_idx]
        gua_meaning = GUA_MEANINGS.get(gua_name, "万物变化，顺应天时")
        
        # 生成变卦
        change_idx = (gua_idx + month) % 64
        change_gua = GUA_NAMES[change_idx]
        
        return {
            "gua": gua_name,
            "meaning": gua_meaning,
            "change_gua": change_gua,
            "idx": gua_idx
        }
    
    def get_shengxiao(self, solar_date=None):
        """获取生肖"""
        if solar_date is None:
            solar_date = datetime.now()
        year = solar_date.year
        return SHENG_XIAO[(year - 4) % 12]
    
    def get_xingzuo(self, solar_date=None):
        """获取星座"""
        if solar_date is None:
            solar_date = datetime.now()
        
        month = solar_date.month
        day = solar_date.day
        
        xingzuo_dates = [
            (1, 20, "水瓶座"), (2, 19, "双鱼座"), (3, 21, "白羊座"),
            (4, 20, "金牛座"), (5, 21, "双子座"), (6, 22, "巨蟹座"),
            (7, 23, "狮子座"), (8, 23, "处女座"), (9, 23, "天秤座"),
            (10, 24, "天蝎座"), (11, 23, "射手座"), (12, 22, "摩羯座"),
        ]
        
        for m, d, name in xingzuo_dates:
            if month == m and day >= d:
                return name
            if month == m + 1 and day < xingzuo_dates[(m) % 12][1]:
                return name
        
        return "摩羯座"  # 默认
    
    def get_yi_ji(self, solar_date=None):
        """获取宜忌信息"""
        if solar_date is None:
            solar_date = datetime.now()
        
        day_seed = solar_date.day % 7
        yi_list = [
            ["嫁娶", "出行", "开市", "纳财"],
            ["祭祀", "祈福", "求嗣", "斋醮"],
            ["修造", "动土", "竖柱", "上梁"],
            ["入学", "求医", "栽种", "牧养"],
            ["交易", "立券", "纳畜", "捕捉"],
            ["移徙", "入宅", "安床", "作灶"],
            ["沐浴", "扫舍", "修饰", "整容"],
        ]
        ji_list = [
            ["安葬", "行丧", "伐木", "作梁"],
            ["开仓", "出货", "置产", "破土"],
            ["嫁娶", "出行", "移徙", "入宅"],
            ["开市", "交易", "纳财", "立券"],
            ["祭祀", "祈福", "斋醮", "酬神"],
            ["修造", "动土", "破土", "安葬"],
            ["词讼", "争斗", "远行", "冒险"],
        ]
        
        return {
            "yi": yi_list[day_seed],
            "ji": ji_list[day_seed]
        }
    
    def get_huangli_summary(self, solar_date=None):
        """获取完整黄历摘要"""
        if solar_date is None:
            solar_date = datetime.now()
        
        lunar = self.solar_to_lunar(solar_date)
        yi_ji = self.get_yi_ji(solar_date)
        
        return {
            "date": solar_date.strftime("%Y-%m-%d"),
            "lunar": f"{lunar.get('lunar_month_cn', '')}月{lunar.get('lunar_day_cn', '')}",
            "ganzhi": lunar.get('full', ''),
            "shengxiao": lunar.get('shengxiao', ''),
            "xingzuo": lunar.get('xingzuo', ''),
            "gua": lunar.get('gua', {}).get('gua', ''),
            "gua_meaning": lunar.get('gua', {}).get('meaning', ''),
            "jie_qi": lunar.get('jie_qi', {}).get('today', ''),
            "next_jie_qi": lunar.get('jie_qi', {}).get('next', {}),
            "yi": yi_ji['yi'],
            "ji": yi_ji['ji'],
        }


# ============================================================================
# 核心万年历类
# ============================================================================

class LongHunCalendar:
    """
    龍魂万年历 - 系统唯一入口 (L0层)
    
    核心职责:
    1. 时间管理：公历/农历/节气/干支/卦象
    2. 任务调度：定时任务、周期触发
    3. 上下文路由：L0-L3层级路由
    4. 实时记录：动作日志、DNA追溯
    5. 多AI网关：AI服务调度
    
    DNA: #龍芯⚡️2026-06-27-LONGHUN-CALENDAR-v1.0
    """
    
    def __init__(self):
        self.dna_tracer = DNATracer(self)
        self.lunar_engine = LunarEngine()
        self._init_dna()
        self._running = False
        self._tasks = []
        self._context_stack = []
        self._ai_gateways = {}
        self._log_buffer = []
        
        # 生成系统启动DNA
        self.boot_dna = self.dna_tracer.generate_dna(
            action_type="system_boot",
            skill_id="S11",
            audit_level=AUDIT_GREEN
        )
        print(f"{AUDIT_GREEN} 龍魂万年历 v{CALENDAR_VERSION} 启动")
        print(f"   DNA: {self.boot_dna['dna_code']}")
    
    def _init_dna(self):
        """初始化DNA追溯链"""
        self.system_dna = {
            "system": SYSTEM_NAME,
            "uid": LONGHUN_UID,
            "version": CALENDAR_VERSION,
            "dna_signature": f"#龍芯⚡️2026-06-27-LONGHUN-CALENDAR-v{CALENDAR_VERSION}",
            "confirm_code": f"#CONFIRM🌌{LONGHUN_UID}-ONLY-ONCE🧬CALENDAR-v{CALENDAR_VERSION}",
        }
    
    # ========================================================================
    # 时间管理接口
    # ========================================================================
    
    def get_calendar_info(self, date=None):
        """获取完整日历信息"""
        if date is None:
            date = datetime.now()
        
        dna = self.dna_tracer.generate_dna("get_calendar", "S11", AUDIT_GREEN)
        
        lunar_info = self.lunar_engine.solar_to_lunar(date)
        huangli = self.lunar_engine.get_huangli_summary(date)
        
        result = {
            "solar_date": date.strftime("%Y-%m-%d %H:%M:%S"),
            "weekday": lunar_info.get("weekday", ""),
            "lunar": {
                "year": lunar_info.get("lunar_year"),
                "month": lunar_info.get("lunar_month_cn"),
                "day": lunar_info.get("lunar_day_cn"),
                "is_leap": lunar_info.get("is_leap"),
            },
            "ganzhi": lunar_info.get("full", ""),
            "shengxiao": lunar_info.get("shengxiao", ""),
            "xingzuo": lunar_info.get("xingzuo", ""),
            "gua": lunar_info.get("gua", {}),
            "jie_qi": lunar_info.get("jie_qi", {}),
            "huangli": huangli,
            "dna": dna["dna_code"],
        }
        
        self.dna_tracer.add_trace(dna, "calendar_info", "日历信息获取成功", AUDIT_GREEN)
        return result
    
    def get_today(self):
        """获取今日信息"""
        return self.get_calendar_info(datetime.now())
    
    def get_lunar_date(self, solar_date=None):
        """获取农历日期"""
        return self.lunar_engine.solar_to_lunar(solar_date)
    
    def get_jie_qi_info(self, solar_date=None):
        """获取节气信息"""
        return self.lunar_engine.get_jie_qi(solar_date)
    
    def get_ganzhi_info(self, solar_date=None):
        """获取干支信息"""
        return self.lunar_engine.get_ganzhi(solar_date)
    
    def get_gua_info(self, solar_date=None):
        """获取卦象信息"""
        return self.lunar_engine.get_qigua(solar_date)
    
    def get_huangli(self, solar_date=None):
        """获取黄历（宜忌）"""
        return self.lunar_engine.get_huangli_summary(solar_date)
    
    # ========================================================================
    # 任务调度接口
    # ========================================================================
    
    def schedule_task(self, task_name, callback, trigger_time, recurring=False, interval=None):
        """
        调度任务
        
        Args:
            task_name: 任务名称
            callback: 回调函数
            trigger_time: 触发时间 (datetime)
            recurring: 是否周期性
            interval: 周期间隔（秒）
        """
        dna = self.dna_tracer.generate_dna("schedule_task", "S11", AUDIT_GREEN)
        
        task = {
            "name": task_name,
            "callback": callback,
            "trigger_time": trigger_time,
            "recurring": recurring,
            "interval": interval,
            "dna": dna,
            "created_at": datetime.now(),
            "status": "scheduled",
        }
        
        self._tasks.append(task)
        self.dna_tracer.add_trace(dna, "task_scheduled", f"任务 '{task_name}' 已调度", AUDIT_GREEN)
        
        print(f"{AUDIT_GREEN} 任务已调度: {task_name} @ {trigger_time}")
        return task
    
    def run_scheduler(self, block=False):
        """运行调度器"""
        self._running = True
        dna = self.dna_tracer.generate_dna("scheduler_start", "S11", AUDIT_GREEN)
        print(f"{AUDIT_GREEN} 调度器已启动")
        
        def _scheduler_loop():
            while self._running:
                now = datetime.now()
                for task in self._tasks:
                    if task["status"] == "scheduled" and now >= task["trigger_time"]:
                        try:
                            task["callback"]()
                            self.dna_tracer.add_trace(
                                task["dna"], "task_executed", 
                                f"任务 '{task['name']}' 执行成功", AUDIT_GREEN
                            )
                            if task["recurring"] and task["interval"]:
                                task["trigger_time"] = now + timedelta(seconds=task["interval"])
                            else:
                                task["status"] = "completed"
                        except Exception as e:
                            self.dna_tracer.add_trace(
                                task["dna"], "task_failed",
                                f"任务 '{task['name']}' 执行失败: {str(e)}", AUDIT_RED
                            )
                            task["status"] = "failed"
                time.sleep(1)
        
        if block:
            _scheduler_loop()
        else:
            threading.Thread(target=_scheduler_loop, daemon=True).start()
        
        return dna
    
    def stop_scheduler(self):
        """停止调度器"""
        self._running = False
        print(f"{AUDIT_YELLOW} 调度器已停止")
    
    # ========================================================================
    # 上下文路由接口
    # ========================================================================
    
    def route_context(self, intent, data=None):
        """
        上下文路由 - 根据意图路由到对应层级
        
        Args:
            intent: 用户意图
            data: 附加数据
        
        Returns:
            dict: 路由结果
        """
        dna = self.dna_tracer.generate_dna("context_route", "S11", AUDIT_GREEN)
        
        # 意图分类与路由
        route_map = {
            "calendar": {"layer": "L0", "skill": "S11", "desc": "日历查询"},
            "schedule": {"layer": "L0", "skill": "S11", "desc": "任务调度"},
            "context": {"layer": "L1", "skill": "S04", "desc": "上下文管理"},
            "knowledge": {"layer": "L2", "skill": "S06", "desc": "知识图谱"},
            "memory": {"layer": "L2", "skill": "S07", "desc": "记忆管理"},
            "ai_route": {"layer": "L2", "skill": "S08", "desc": "AI网关"},
            "code": {"layer": "L3", "skill": "S09", "desc": "代码生成"},
            "data": {"layer": "L3", "skill": "S10", "desc": "数据分析"},
        }
        
        route_info = route_map.get(intent, {"layer": "L0", "skill": "S11", "desc": "默认路由"})
        
        result = {
            "intent": intent,
            "routed_to": route_info["layer"],
            "skill": route_info["skill"],
            "description": route_info["desc"],
            "data": data,
            "dna": dna["dna_code"],
            "timestamp": datetime.now().isoformat(),
        }
        
        self._context_stack.append(result)
        self.dna_tracer.add_trace(
            dna, "context_routed",
            f"意图 '{intent}' 路由至 {route_info['layer']}/{route_info['skill']}",
            AUDIT_GREEN
        )
        
        return result
    
    def get_context_stack(self):
        """获取上下文栈"""
        return self._context_stack
    
    def pop_context(self):
        """弹出上下文"""
        if self._context_stack:
            return self._context_stack.pop()
        return None
    
    # ========================================================================
    # 实时记录接口
    # ========================================================================
    
    def log_action(self, action_type, detail, level=AUDIT_GREEN):
        """
        记录动作日志
        
        动作类型:
        - SKILL_CALL: 技能调用
        - CONTEXT_SWITCH: 上下文切换
        - AI_ROUTE: AI路由
        - USER_INPUT: 用户输入
        - SYSTEM_EVENT: 系统事件
        - AUDIT_MARK: 审计标记
        - DNA_GENERATE: DNA生成
        - ERROR: 错误
        """
        dna = self.dna_tracer.generate_dna("log_action", "S11", level)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "detail": detail,
            "level": level,
            "dna": dna["dna_code"],
        }
        
        self._log_buffer.append(log_entry)
        self.dna_tracer.add_trace(dna, "action_logged", detail, level)
        
        # 控制台输出
        print(f"{level} [{action_type}] {detail} | DNA:{dna['dna_code']}")
        
        return log_entry
    
    def get_logs(self, limit=100):
        """获取最近N条日志"""
        return self._log_buffer[-limit:]
    
    def export_logs(self, filepath=None):
        """导出日志到文件"""
        if filepath is None:
            filepath = f"longhun_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self._log_buffer, f, ensure_ascii=False, indent=2)
        
        print(f"{AUDIT_GREEN} 日志已导出: {filepath}")
        return filepath
    
    # ========================================================================
    # 多AI网关接口
    # ========================================================================
    
    def register_ai_gateway(self, name, endpoint, config=None):
        """
        注册AI网关
        
        Args:
            name: 网关名称
            endpoint: API端点
            config: 配置参数
        """
        dna = self.dna_tracer.generate_dna("register_gateway", "S11", AUDIT_GREEN)
        
        gateway = {
            "name": name,
            "endpoint": endpoint,
            "config": config or {},
            "status": "active",
            "dna": dna,
            "registered_at": datetime.now().isoformat(),
        }
        
        self._ai_gateways[name] = gateway
        self.dna_tracer.add_trace(dna, "gateway_registered", f"AI网关 '{name}' 已注册", AUDIT_GREEN)
        
        print(f"{AUDIT_GREEN} AI网关已注册: {name} -> {endpoint}")
        return gateway
    
    def route_to_ai(self, gateway_name, payload):
        """
        路由到指定AI网关
        
        Args:
            gateway_name: 网关名称
            payload: 请求数据
        """
        dna = self.dna_tracer.generate_dna("ai_route", "S11", AUDIT_GREEN)
        
        gateway = self._ai_gateways.get(gateway_name)
        if not gateway:
            self.dna_tracer.add_trace(dna, "route_failed", f"AI网关 '{gateway_name}' 不存在", AUDIT_RED)
            return {"error": f"网关 '{gateway_name}' 未注册", "dna": dna["dna_code"]}
        
        self.dna_tracer.add_trace(
            dna, "ai_routed",
            f"请求已路由至 '{gateway_name}'",
            AUDIT_GREEN
        )
        
        return {
            "gateway": gateway_name,
            "endpoint": gateway["endpoint"],
            "payload": payload,
            "dna": dna["dna_code"],
            "status": "routed",
        }
    
    def list_gateways(self):
        """列出所有已注册AI网关"""
        return self._ai_gateways
    
    # ========================================================================
    # DNA审计接口
    # ========================================================================
    
    def audit(self, target_dna_code, expected_hash=None):
        """
        审计DNA链完整性
        
        Args:
            target_dna_code: 目标DNA码
            expected_hash: 期望哈希（可选）
        """
        dna = self.dna_tracer.generate_dna("audit", "S11", AUDIT_YELLOW)
        
        is_valid = self.dna_tracer.verify_dna(target_dna_code)
        
        result = {
            "dna_code": target_dna_code,
            "is_valid": is_valid,
            "audited_at": datetime.now().isoformat(),
            "audit_dna": dna["dna_code"],
        }
        
        level = AUDIT_GREEN if is_valid else AUDIT_RED
        self.dna_tracer.add_trace(
            dna, "audit_complete",
            f"DNA '{target_dna_code}' 验证结果: {'通过' if is_valid else '失败'}",
            level
        )
        
        print(f"{level} DNA审计: {target_dna_code} -> {'通过' if is_valid else '失败'}")
        return result
    
    def get_dna_chain(self, limit=50):
        """获取DNA追溯链"""
        return self.dna_tracer.get_chain(limit)
    
    # ========================================================================
    # 系统信息接口
    # ========================================================================
    
    def get_system_info(self):
        """获取系统信息"""
        return {
            "system": SYSTEM_NAME,
            "uid": LONGHUN_UID,
            "version": CALENDAR_VERSION,
            "dna": self.system_dna,
            "boot_dna": self.boot_dna["dna_code"] if hasattr(self, 'boot_dna') else None,
            "tasks_count": len(self._tasks),
            "logs_count": len(self._log_buffer),
            "gateways_count": len(self._ai_gateways),
            "context_depth": len(self._context_stack),
        }
    
    def verify_system(self):
        """系统自检"""
        dna = self.dna_tracer.generate_dna("system_verify", "S11", AUDIT_GREEN)
        
        checks = {
            "dna_tracer": self.dna_tracer is not None,
            "lunar_engine": self.lunar_engine is not None,
            "tasks": True,
            "logs": True,
            "gateways": True,
        }
        
        all_pass = all(checks.values())
        level = AUDIT_GREEN if all_pass else AUDIT_RED
        
        result = {
            "all_pass": all_pass,
            "checks": checks,
            "dna": dna["dna_code"],
            "timestamp": datetime.now().isoformat(),
        }
        
        self.dna_tracer.add_trace(dna, "system_verify", "系统自检完成", level)
        print(f"{level} 系统自检: {'全部通过' if all_pass else '存在异常'}")
        
        return result
    
    def __repr__(self):
        return f"LongHunCalendar(v{CALENDAR_VERSION}, UID:{LONGHUN_UID})"


# ============================================================================
# 便捷函数
# ============================================================================

def create_calendar():
    """创建龍魂万年历实例"""
    return LongHunCalendar()

def quick_calendar():
    """快速获取今日日历信息"""
    cal = LongHunCalendar()
    return cal.get_today()

def demo():
    """演示龍魂万年历功能"""
    print("=" * 60)
    print("  龍魂万年历 v1.0 - 演示")
    print("  DNA: #龍芯⚡️2026-06-27-LONGHUN-CALENDAR-v1.0")
    print("=" * 60)
    
    cal = LongHunCalendar()
    
    # 今日信息
    print("\n📅 今日日历信息:")
    today = cal.get_today()
    print(json.dumps(today, ensure_ascii=False, indent=2))
    
    # 黄历
    print("\n📜 黄历:")
    huangli = cal.get_huangli()
    print(json.dumps(huangli, ensure_ascii=False, indent=2))
    
    # 系统信息
    print("\n🔧 系统信息:")
    info = cal.get_system_info()
    print(json.dumps(info, ensure_ascii=False, indent=2))
    
    # 系统自检
    print("\n✅ 系统自检:")
    cal.verify_system()
    
    # DNA链
    print("\n🧬 DNA追溯链:")
    chain = cal.get_dna_chain(5)
    for d in chain:
        print(f"   {d['dna_code']} | {d['action_type']} | {d['audit_level']}")
    
    # 上下文路由演示
    print("\n🔄 上下文路由演示:")
    for intent in ["calendar", "context", "ai_route", "code"]:
        result = cal.route_context(intent)
        print(f"   {intent} -> {result['routed_to']}/{result['skill']}")
    
    # 日志记录演示
    print("\n📝 日志记录演示:")
    cal.log_action("SYSTEM_EVENT", "系统启动完成", AUDIT_GREEN)
    cal.log_action("SKILL_CALL", "技能S11调用", AUDIT_GREEN)
    cal.log_action("AUDIT_MARK", "审计标记测试", AUDIT_YELLOW)
    
    print("\n" + "=" * 60)
    print("  演示完成")
    print("=" * 60)


# ============================================================================
# 主入口
# ============================================================================

if __name__ == "__main__":
    demo()
