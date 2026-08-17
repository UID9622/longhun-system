#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-08-06-LONGHUN-SAVE-v1.0-SDK
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·算力省钱代理 v1.0

帮开发者省 AI 调用成本的本地代理：
  - 智能路由：本地 Ollama 优先 → 云端兜底
  - 请求缓存：相同请求不重复调用
  - 成本统计：知道省了多少钱
  - OpenAI 兼容 API：无缝替换

用法:
    # 命令行启动
    longhun-save start --port 8088
    
    # 然后设环境变量
    export OPENAI_BASE_URL=http://localhost:8088/v1
    
    # Python 编程方式
    from longhun_save import SaveProxy
    proxy = SaveProxy()
    proxy.start(port=8088)
"""

from .proxy import SaveProxy, create_app
from .router import SmartRouter, RouteDecision
from .cache_engine import RequestCache
from .stats import CostStats, TokenPrice

__version__ = "1.0.0"
__all__ = [
    "SaveProxy", "create_app",
    "SmartRouter", "RouteDecision",
    "RequestCache",
    "CostStats", "TokenPrice",
]
