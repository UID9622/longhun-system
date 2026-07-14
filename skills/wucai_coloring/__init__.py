#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂五色引擎包

暴露：
- audit(...): 五色审计
- detect_emotion(...): 五行情绪识别
- check_scene_safety(...): 场景安全审查
- evaluate(...): 代码即时权重 + 跑马灯色带

DNA: #龍芯⚡️2026-06-23-WUCAI-PACKAGE-v1.0
"""
from skills.wucai_coloring.audit import audit, AuditResult
from skills.wucai_coloring.emotion_scene import detect_emotion, check_scene_safety, EmotionState, SceneSafety
from skills.wucai_coloring.runtime_weight import evaluate, RuntimeWeight

__all__ = [
    "audit", "AuditResult",
    "detect_emotion", "EmotionState",
    "check_scene_safety", "SceneSafety",
    "evaluate", "RuntimeWeight",
]
