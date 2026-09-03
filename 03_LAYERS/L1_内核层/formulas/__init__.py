# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·丁丑·酉时·䷐随-CORE-FORMULA-REGISTRY-v1.0-UNIFY-UID9622
"""龍魂公式体系 · 核心公式统一部位（唯一权威）
统一规则（2026-08-31·老大指令焊死）：
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
  - 所有公式收口到本目录·一套口径·只引用 FXX 不重写
  - 扩展位：F46-F60(D组已收口) / F61-F99(E组预留) / F100-F200(F组预留)
  - 完整注册表见 README.md（核心公式统一注册表 v1.0）
  - 冲突台账见 README.md §五（三套五行映射以 v4.0 为准）
"""
from .formula_core import *
from .formula_chain import *
from . import formula_catalog
from . import formula_manifest
from . import wuxing_system
from . import wuxing_hexagram
from . import wuxing_monitor
from . import wuxing_kg

__all__ = [
    'formula_catalog',
    'formula_manifest',
    'wuxing_system',
    'wuxing_hexagram',
    'wuxing_monitor',
    'wuxing_kg',
]
