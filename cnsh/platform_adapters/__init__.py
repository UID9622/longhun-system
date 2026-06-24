#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  龍魂中国平台DNA授权适配器包                                   ║
║  Dragon Soul China Platform DNA Authorization Adapter Package ║
║  DNA: #龍芯⚡️2026-06-19-CNSH-PLATFORM-ADAPTERS-v1.0          ║
╚══════════════════════════════════════════════════════════════╝

    ╔═══════════════════════════════════════════╗
    ║  🐉 龍魂体系 — 中国平台适配器               ║
    ║  Dragon Soul System — China Adapters      ║
    ╚═══════════════════════════════════════════╝

支持平台 (Supported Platforms):
    🍑 淘宝    — 电商购物 / E-commerce shopping
    💬 微信    — 社交通讯 / Social messaging
    💰 支付宝  — 支付平台 / Payment platform
    🚗 滴滴    — 出行服务 / Ride-hailing service
    🍜 美团    — 生活服务 / Lifestyle service

核心组件 (Core Components):
    • 平台适配器基类    — 抽象基类与通用接口
    • 适配器管理器      — 统一注册与管理
    • DNA令牌           — 安全授权令牌
    • 三色审计          — 安全审计体系

使用示例 (Usage Example):
    >>> from platform_adapters import 适配器管理器, DNA令牌
    >>> 管理器 = 适配器管理器(模式="模拟")
    >>> 令牌 = 管理器.创建DNA令牌("user_001", ["淘宝:商品搜索"])
    >>> 结果 = 管理器.跨平台操作("淘宝", "商品搜索", {"关键词": "手机"}, 令牌)

君子协议 (Gentleman Agreement):
    本代码仅用于合法授权场景，遵循最小权限原则。
    This code is for authorized use only, following the least privilege principle.
"""

from datetime import datetime, timedelta

# 导入基类 / Import base class
from .平台适配器基类 import (
    平台适配器基类,
    DNA令牌,
    审计级别,
    审计记录,
    操作类型,
)

# 导入各平台适配器 / Import platform adapters
from .淘宝适配器 import 淘宝适配器
from .微信适配器 import 微信适配器
from .支付宝适配器 import 支付宝适配器, 五行元素
from .滴滴适配器 import 滴滴适配器, 车型, 订单状态
from .美团适配器 import 美团适配器, 业务类型

# 导入管理器 / Import manager
from .适配器管理器 import 适配器管理器

# 包元数据 / Package metadata
__version__ = "1.0.0"
__DNA__ = "#龍芯⚡️2026-06-19-CNSH-PLATFORM-ADAPTERS-v1.0"
__author__ = "龍魂体系"
__date__ = "2026-06-19"

# 导出列表 / Export list
__all__ = [
    # 基类 / Base classes
    "平台适配器基类",
    "DNA令牌",
    "审计级别",
    "审计记录",
    "操作类型",
    
    # 平台适配器 / Platform adapters
    "淘宝适配器",
    "微信适配器",
    "支付宝适配器",
    "滴滴适配器",
    "美团适配器",
    
    # 管理器 / Manager
    "适配器管理器",
    
    # 枚举 / Enums
    "五行元素",
    "车型",
    "订单状态",
    "业务类型",
]


def 获取版本信息() -> dict:
    """获取包版本信息 / Get package version info"""
    return {
        "版本": __version__,
        "DNA": __DNA__,
        "作者": __author__,
        "日期": __date__,
        "支持平台": ["淘宝", "微信", "支付宝", "滴滴出行", "美团"],
        "平台数量": 5,
    }


def 快速开始(模式: str = "模拟") -> tuple:
    """
    快速开始 — 创建管理器和示例令牌 / Quick start
    
    返回:
        (管理器, 示例令牌)
    """
    管理器 = 适配器管理器(模式=模式)
    令牌 = 管理器.创建DNA令牌(
        用户标识="quick_start_user",
        授权范围=["*"],  # 通配符授权所有权限
        有效小时=1
    )
    return 管理器, 令牌


# 包加载时输出信息 / Print info on package load
print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🐉 龍魂中国平台DNA授权适配器包 v{__version__}                   ║
║  DNA: {__DNA__}                     ║
║                                                              ║
║  支持平台: 🍑淘宝 💬微信 💰支付宝 🚗滴滴 🍜美团              ║
║  平台数量: 5                                                 ║
║                                                              ║
║  快速开始: from platform_adapters import 快速开始             ║
║           管理器, 令牌 = 快速开始()                           ║
╚══════════════════════════════════════════════════════════════╝
""")
