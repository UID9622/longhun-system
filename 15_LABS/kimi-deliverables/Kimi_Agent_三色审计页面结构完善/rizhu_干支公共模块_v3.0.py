#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
龍魂 · 干支公共模块 core/rizhu.py  v3.0（唯一口径）
=================================================
DNA: #龍芯⚡️丙午·丙申·丙辰·甲午·䷑蛊-RIZHU-CORE-v3.0-UID9622（生成器回填，禁止手写干支）

口径决议：2026-08-10 老大裁决采纳方案A —— 日柱统一为真实万年历口径。
  · 日柱锚点：1900-01-01 = 甲戌日（六十甲子索引10）
  · 交叉验证：1949-10-01 = 甲子日（开国大典，公认历法事实）
  · 年/月/时柱沿用 ganzhi_dna_engine.py 已验证算法（五虎遁月干）
  · lh_dna_generator v2.0 日柱口径（1900基准+9/+11）偏离万年历，
    标记 v2-legacy 冻结，既有DNA不追溯改动，注册表加「口径:v2-legacy」标注。

任何文档/代码需要干支，一律 import 本模块，禁止各自实现。
"""

import datetime

TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 五虎遁：年干 -> 寅月天干索引
_YIN_MONTH_GAN = [2, 4, 6, 8, 0, 2, 4, 6, 8, 0]


def get_rizhu(dt: datetime.datetime) -> str:
    """日柱干支 v3.0 —— 与公开万年历一致，任何人可外部验证。"""
    days = (dt.date() - datetime.date(1900, 1, 1)).days
    idx = (10 + days) % 60  # 1900-01-01 = 甲戌(索引10)
    return TIAN_GAN[idx % 10] + DI_ZHI[idx % 12]


def get_nianzhu(dt: datetime.datetime) -> str:
    """年柱：公元年-4 对60取模（立春口径的简化，与既有引擎一致）。"""
    idx = (dt.year - 4) % 60
    return TIAN_GAN[idx % 10] + DI_ZHI[idx % 12]


def _solar_term_month(dt: datetime.datetime) -> int:
    """节气月（1=寅月/正月...12=丑月），近似以每月7日为节气分界。

    干支月柱按节气划分而非公历整月：如2026-08-07立秋后即为申月（节气月7）。
    节气月n对应公历月n+1（寅月≈公历2月）。近似以每月7日为节气分界，
    误差±1天，用于逻辑时间戳足够；精确节气表可后续扩展。
    """
    sm = dt.month - 1 if dt.day >= 7 else dt.month - 2
    return sm if sm >= 1 else sm + 12


def get_yuezhu(dt: datetime.datetime) -> str:
    """月柱：五虎遁，寅月起正月，按节气月。"""
    year_gan_idx = (dt.year - 4) % 10
    yin_gan = _YIN_MONTH_GAN[year_gan_idx]
    sm = _solar_term_month(dt)
    gan = TIAN_GAN[(yin_gan + sm - 1) % 10]
    zhi = DI_ZHI[(2 + sm - 1) % 12]  # 寅(2)起正月
    return gan + zhi


def get_shizhu(dt: datetime.datetime) -> str:
    """时柱：日干起时（甲己还加甲...）。"""
    ri_gan_idx = TIAN_GAN.index(get_rizhu(dt)[0])
    hour_zhi_idx = ((dt.hour + 1) // 2) % 12
    hour_gan_idx = (ri_gan_idx % 5 * 2 + hour_zhi_idx) % 10
    return TIAN_GAN[hour_gan_idx] + DI_ZHI[hour_zhi_idx]


def sizhu_ganzhi(dt: datetime.datetime) -> str:
    """四柱干支：年·月·日·时，唯一对外口径。"""
    return f"{get_nianzhu(dt)}·{get_yuezhu(dt)}·{get_rizhu(dt)}·{get_shizhu(dt)}"


def quick_dna(dt: datetime.datetime, tag: str, version: str, uid: str = "UID9622") -> str:
    """标准DNA签名：#龍芯⚡️{四柱}-{标签}-{版本}-{UID}"""
    return f"#龍芯⚡️{sizhu_ganzhi(dt)}-{tag}-{version}-{uid}"


# ================= 自检（入库/部署前必跑） =================
def self_test() -> bool:
    # 日柱四锚点（公开万年历可验）
    assert get_rizhu(datetime.datetime(1900, 1, 1)) == '甲戌', '锚点1失败'
    assert get_rizhu(datetime.datetime(1949, 10, 1)) == '甲子', '锚点2失败(开国大典)'
    assert get_rizhu(datetime.datetime(2000, 1, 1)) == '戊午', '锚点3失败'
    assert get_rizhu(datetime.datetime(2026, 8, 10)) == '丙辰', '锚点4失败'
    # 年柱锚点：2026 = 丙午
    assert get_nianzhu(datetime.datetime(2026, 8, 10)) == '丙午'
    # 月柱锚点：2026-08-10 立秋后为申月，丙午年五虎遁庚寅起 -> 丙申月
    assert get_yuezhu(datetime.datetime(2026, 8, 10)) == '丙申'
    # 时柱锚点：丙辰日 午时为 甲午时（丙辛日起戊子 -> 午=甲）
    assert get_shizhu(datetime.datetime(2026, 8, 10, 12)) == '甲午'
    # 四柱整锚：2026-08-10 12:00 = 丙午·丙申·丙辰·甲午
    assert sizhu_ganzhi(datetime.datetime(2026, 8, 10, 12)) == '丙午·丙申·丙辰·甲午'
    return True


if __name__ == '__main__':
    assert self_test()
    now = datetime.datetime.now()
    print('✅ rizhu.py v3.0 自检全绿')
    print('当前四柱:', sizhu_ganzhi(now))
    print('示例DNA:', quick_dna(now, 'EXAMPLE', 'v1.0'))
