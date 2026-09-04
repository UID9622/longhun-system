"""🐉 龍魂引擎：__init__
路径：engines/lh_mental_immune/__init__.py
TODO：请补充详细功能说明（不少于20字）。"""
# 龍魂·精神免疫系统 v1.0
# DNA: #龍芯⚡️丙午·乙未·丁酉·丙午·䷨损-MENTAL-IMMUNE-v1.0-a1b2c3d4
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 铁律: 纯本地·匿名化·无评判·不上传·不收集

from .anxiety_detector import AnxietyDetector
from .noise_shield import NoiseShield
from .digital_detox import DigitalDetox
from .behavior_anchor import BehaviorAnchor
from .community_resonance import CommunityResonance

__version__ = "1.0.0"
__all__ = [
    "AnxietyDetector",
    "NoiseShield", 
    "DigitalDetox",
    "BehaviorAnchor",
    "CommunityResonance",
]
