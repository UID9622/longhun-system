#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · 干支公共模块 rizhu_core.py v3.0（唯一口径）
========================================================================
DNA: #龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-RIZHU-CORE-v3.0-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

设计原则:
  锚点 1900-01-01 = 甲戌日（六十甲子索引10），任何人打开万年历App可核对
  交叉验证 1949-10-01 = 甲子日（开国大典，公认历法事实）
  弃用蔡勒公式变体，改用锚点顺推——信任闭环前提是可外部验证

v2.0→v3.0 修正:
  v2.0 蔡勒变体 JDN 拼装错误，2026-08-10 错算为己丑（实为丙辰）
  v3.0 统一锚点顺推，与公开万年历一致

参考来源: Kimi三色审计实测记录 + 公开万年历交叉验证
关联: harmonyos/ 下 ArkTS 端 GanzhiUtil.ets v3.0 为同算法移植
"""

import datetime
import unittest

# ===== 常量 =====
TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
_YIN_MONTH_GAN = [2, 4, 6, 8, 0, 2, 4, 6, 8, 0]  # 五虎遁：年干 -> 寅月天干索引
_ANCHOR_DATE = datetime.date(1900, 1, 1)
_ANCHOR_IDX = 10  # 1900-01-01 = 甲戌(六十甲子索引10)


def get_rizhu(dt: datetime.datetime) -> str:
    """日柱 v3.0 —— 锚点顺推，与公开万年历一致，任何人可外部验证。

    Args:
        dt: datetime.datetime 对象

    Returns:
        日干支字符串，如 '丙辰'
    """
    days = (dt.date() - _ANCHOR_DATE).days
    idx = (_ANCHOR_IDX + days) % 60
    return TIAN_GAN[idx % 10] + DI_ZHI[idx % 12]


def get_nianzhu(dt: datetime.datetime) -> str:
    """年柱：公元年-4 对60取模。立春前属上年（简化：按公历年）。"""
    idx = (dt.year - 4) % 60
    return TIAN_GAN[idx % 10] + DI_ZHI[idx % 12]


def _solar_term_month(dt: datetime.datetime) -> int:
    """节气月（1=寅月...12=丑月），近似每月7日分界。

    误差±1天，精确节气需查表。逻辑时间戳/审计场景够用。
    精确版在路线图。
    """
    sm = dt.month - 1 if dt.day >= 7 else dt.month - 2
    return sm if sm >= 1 else sm + 12


def get_yuezhu(dt: datetime.datetime) -> str:
    """月柱：五虎遁，寅月起正月，按节气月。"""
    yin_gan = _YIN_MONTH_GAN[(dt.year - 4) % 10]
    sm = _solar_term_month(dt)
    return TIAN_GAN[(yin_gan + sm - 1) % 10] + DI_ZHI[(2 + sm - 1) % 12]


def get_shizhu(dt: datetime.datetime) -> str:
    """时柱：日干起时（甲己还加甲）。"""
    ri_gan = TIAN_GAN.index(get_rizhu(dt)[0])
    hz = ((dt.hour + 1) // 2) % 12
    return TIAN_GAN[(ri_gan % 5 * 2 + hz) % 10] + DI_ZHI[hz]


def sizhu_ganzhi(dt: datetime.datetime) -> str:
    """四柱：年·月·日·时，唯一对外口径。"""
    return f"{get_nianzhu(dt)}·{get_yuezhu(dt)}·{get_rizhu(dt)}·{get_shizhu(dt)}"


def sizhu_dna_stamp(dt: datetime.datetime, module: str = "", action: str = "") -> str:
    """生成含四柱的 DNA 戳。
    Args:
        dt: 时间
        module: 模块名（可选）
        action: 动作（可选）
    Returns:
        DNA 戳字符串
    """
    sz = sizhu_ganzhi(dt)
    tail = f"-{module}-{action}" if module else ""
    return f"#龍芯⚡️{sz}{tail}"


# ===== 交叉验证测试 =====


class RizhuCoreTest(unittest.TestCase):
    """锚点顺推算法的可验证性测试。

    所有锚点均可通过公开万年历/历法常识独立核对。
    """

    def test_anchor_1900(self):
        """锚点1: 1900-01-01 = 甲戌"""
        self.assertEqual(get_rizhu(datetime.datetime(1900, 1, 1)), '甲戌')

    def test_anchor_1949(self):
        """锚点2: 1949-10-01 = 甲子（开国大典，公认事实）"""
        self.assertEqual(get_rizhu(datetime.datetime(1949, 10, 1)), '甲子')

    def test_anchor_2000(self):
        """锚点3: 2000-01-01 = 戊午"""
        self.assertEqual(get_rizhu(datetime.datetime(2000, 1, 1)), '戊午')

    def test_anchor_2026_0810(self):
        """锚点4: 2026-08-10 = 丙辰"""
        self.assertEqual(get_rizhu(datetime.datetime(2026, 8, 10)), '丙辰')

    def test_yuezhu_liquid(self):
        """月柱：立秋后申月"""
        self.assertEqual(get_yuezhu(datetime.datetime(2026, 8, 10)), '丙申')

    def test_sizhu_full(self):
        """完整四柱验证"""
        self.assertEqual(
            sizhu_ganzhi(datetime.datetime(2026, 8, 10, 12)),
            '丙午·丙申·丙辰·甲午'
        )

    def test_dna_stamp(self):
        """DNA 戳生成"""
        stamp = sizhu_dna_stamp(
            datetime.datetime(2026, 8, 11), 'CAR-SYSTEM', 'v2.1'
        )
        self.assertTrue(stamp.startswith('#龍芯⚡️'))
        self.assertIn('丙午', stamp)
        self.assertIn('CAR-SYSTEM', stamp)


def run_tests():
    """入库/部署前必跑。全绿才准合并。"""
    suite = unittest.TestLoader().loadTestsFromTestCase(RizhuCoreTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    if run_tests():
        print(f'\n✅ rizhu_core v3.0 自检全绿 | 当前四柱: {sizhu_ganzhi(datetime.datetime.now())}')
    else:
        print('\n🔴 rizhu_core v3.0 自检失败！')
        exit(1)
