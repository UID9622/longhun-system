"""龍魂 Python SDK

DNA: #龍芯⚡️丙午·丙申·丙辰·戊子·坎-SDK-INIT-v2.1

中国自主可控的全模态 AI 人格系统。
语音 · 视觉 · 文本 · 人格路由 · 声纹DNA · 安全审计
数据不出境，主权归本地。

v2.1: 内联引擎全面可用 — Auditor(三色审计) · PersonaRouter(人格路由) · CNSHParser(语义解析) 已对接内联规则，零外部依赖即可运行。
"""

__version__ = "2.1.0"
__author__ = "UID9622 · 诸葛鑫"
__status__ = "Preview"  # 发布状态：Preview | Stable

from .router import PersonaRouter, RouteResult, RouteInfo
from .parser import CNSHParser, Intent
from .dna import DNA
from .auditor import Auditor, AuditReport
from .voice import (
    VoiceSynthesizer, PersonaVoice, VoiceDNA,
    VoiceResult, VoiceProfile, VoiceRegisterResult, VoiceVerifyResult,
)
from .vision import (
    VisionAnalyzer, VisionBridge,
    VisionResult, SymbolResult, Scene, VideoResult,
)

__all__ = [
    # 核心类
    "PersonaRouter", "CNSHParser", "DNA", "Auditor",
    "VoiceSynthesizer", "PersonaVoice", "VoiceDNA",
    "VisionAnalyzer", "VisionBridge",
    # 数据类
    "RouteResult", "RouteInfo", "Intent", "AuditReport",
    "VoiceResult", "VoiceProfile", "VoiceRegisterResult", "VoiceVerifyResult",
    "VisionResult", "SymbolResult", "Scene", "VideoResult",
]
