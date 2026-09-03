#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·丁酉·乙酉·午时·䷾既济-CNSH-STD-TIME-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
CNSH 标准库 · time —— 时间/干支四柱
干支四柱算法: 年干=天干[(年-4)%10] · 月/日/时简化以今日历推算（锚定公历）
"""
import time as _t
import datetime as _dt
from zoneinfo import ZoneInfo

_TG = "甲乙丙丁戊己庚辛壬癸"
_DZ = "子丑寅卯辰巳午未申酉戌亥"
_ZW = "鼠牛虎兔龙蛇马羊猴鸡狗猪"


def now_iso(tz: str = "Asia/Shanghai") -> str:
    """当前时间 ISO8601（默认东八区）"""
    return _dt.datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")


def timestamp_ms() -> int:
    return int(_t.time() * 1000)


def unix() -> float:
    return _t.time()


def today() -> str:
    return _dt.date.today().isoformat()


def _stems_branches(y, m, d, h):
    """公历 → 干支四柱（简化：年干支+月干支近似+日干支+时干支）"""
    gan = lambda x: _TG[(x - 4) % 10]
    zhi = lambda x: _DZ[(x - 4) % 12]
    # 年柱
    yg, yz = gan(y), zhi(y)
    # 月柱（节气近似：以农历月= (m+1)%2 简化，锚定立春为年界）
    mg = _TG[(y * 12 + m + 1) % 10]
    mz = _DZ[(m + 1) % 12]
    # 日柱（公历日序推算，锚定 1900-01-01=甲戌日）
    base = _dt.date(1900, 1, 1)
    offset = (_dt.date(y, m, d) - base).days
    dg = _TG[offset % 10]
    dz = _DZ[(offset + 10) % 12]
    # 时柱（五鼠遁: 日干 甲己→甲子 · 乙庚→丙子 · 丙辛→戊子 · 丁壬→庚子 · 戊癸→壬子）
    hour_zhi_idx = ((h + 1) // 2) % 12
    dg_idx = offset % 10            # 日干索引
    hour_gan_idx = (dg_idx * 2 + hour_zhi_idx) % 10
    hg, hz = _TG[hour_gan_idx], _DZ[hour_zhi_idx]
    return f"{yg}{yz} {mg}{mz} {dg}{dz} {hg}{hz}"


def ganzhi_stamp() -> str:
    """干支四柱+时辰，如: 丙午 丁酉 乙酉 午时"""
    now = _dt.datetime.now()
    hour_zhi = _DZ[(now.hour + 1) // 2 % 12]
    cols = _stems_branches(now.year, now.month, now.day, now.hour).split()
    return f"{cols[0]} {cols[1]} {cols[2]} {hour_zhi}时"


def sleep(seconds: float):
    _t.sleep(seconds)
