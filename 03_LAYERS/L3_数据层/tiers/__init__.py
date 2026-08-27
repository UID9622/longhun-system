# DNA: #龍芯⚡️丙午·丙申·甲戌·卯时·䷐随-QUAD-SYNC-v1.0-ATTRIBUTION-8c26d5f
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""龍魂DNA记忆库 · 五层人群适配器包初始化。"""

from .tier_common import TierCommon
from .tier_professional import TierProfessional
from .tier_student import TierStudent
from .tier_elderly import TierElderly
from .tier_tech import TierTech

__all__ = ["TierCommon", "TierProfessional", "TierStudent",
           "TierElderly", "TierTech"]
