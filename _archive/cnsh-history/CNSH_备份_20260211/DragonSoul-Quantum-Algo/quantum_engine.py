#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂量子算法核心引擎
DNA追溯码: #龍芯⚡️2026-02-09-QUANTUM-ENGINE-v1.0
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class HookType:
    """钩子类型枚举"""
    BEFORE_REQUEST = "before_request"
    AFTER_REQUEST = "after_request"
    BEFORE_SCENE_DETECT = "before_scene_detect"
    AFTER_SCENE_DETECT = "after_scene_detect"
    BEFORE_WEIGHT_CALC = "before_weight_calc"
    AFTER_WEIGHT_CALC = "after_weight_calc"
    ON_PERSONALITY_ACTIVATE = "on_personality_activate"
    ON_AUDIT_TRIGGER = "on_audit_trigger"

class HookManager:
    """钩子管理器"""
    
    def __init__(self):
        self._hooks: Dict[str, List] = {}
        self._priorities: Dict[str, Dict] = {}
    
    def register(self, hook_type: str, callback, priority: int = 0):
        """注册钩子"""
        if hook_type not in self._hooks:
            self._hooks[hook_type] = []
            self._priorities[hook_type] = {}
        
        self._hooks[hook_type].append(callback)
        self._priorities[hook_type][callback] = priority
        
        self._hooks[hook_type].sort(
            key=lambda cb: self._priorities[hook_type][cb],
            reverse=True
        )
    
    def trigger(self, hook_type: str, *args, **kwargs) -> List:
        """触发钩子"""
        results = []
        
        if hook_type in self._hooks:
            for callback in self._hooks[hook_type]:
                try:
                    result = callback(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    print(f"钩子执行错误 [{hook_type}]: {e}")
        
        return results

hook_manager = HookManager()
