# P0声明: 本文件属龍魂体系P0合规范围，受LH-P0-CONSTITUTION约束
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂五行八门协议 v1.0
DNA: #龍芯⚡️2026-08-25-DOOR-PROTOCOL-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
修正：惊门枚举值 jingmen_alert，避免与景门 jingmen 混淆
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime


class 五行(Enum):
    """五行分类（门机归属）"""
    金 = "metal"
    木 = "wood"
    水 = "water"
    火 = "fire"
    土 = "earth"


class 八门(Enum):
    """
    八门机制定义（奇门遁甲）
    巽四宫：杜门（土）- 主动隔离
    离九宫：景门（水）- 展示/演示
    坤二宫：死门（金）- 异常崩溃
    兑七宫：惊门（火）- 入侵检测
    乾六宫：开门（木）- 正常启动 → 生门
    坎一宫：休门（土）- 主动休眠
    艮八宫：生门（木）- 服务复活/正常
    震三宫：伤门（金）- 攻击响应
    升门：自定义 - 服务扩容/升级
    """
    生门 = "shengmen"
    升门 = "shengmen_up"   # 扩容/升级
    休门 = "xiumen"
    伤门 = "shangmen"
    杜门 = "dumen"
    景门 = "jingmen"        # 展示/演示
    死门 = "simen"
    惊门 = "jingmen_alert"  # 修正：避免与景门 jingmen 混淆


class 三色(Enum):
    绿 = "🟢"
    黄 = "🟡"
    红 = "🔴"


@dataclass
class 门机事件:
    门名: 八门
    五行归属: 五行
    三色等级: 三色
    服务名: str
    端口: int
    触发时间: datetime
    事件描述: str
    处置动作: Optional[str] = None
    DNA记录: Optional[str] = None
    附加数据: Optional[Dict[str, Any]] = field(default_factory=dict)


# 门机规则映射（五行归属 + 三色等级 + 处置动作）
门机规则: Dict[八门, Dict] = {
    八门.生门: {
        "触发条件": "服务正常启动或重启成功",
        "三色": 三色.绿,
        "五行": 五行.木,
        "处置": "记录DNA → 允许运行"
    },
    八门.升门: {
        "触发条件": "服务扩容/升级",
        "三色": 三色.黄,
        "五行": 五行.木,
        "处置": "三色审计 → 审计通过后执行"
    },
    八门.休门: {
        "触发条件": "服务主动休眠",
        "三色": 三色.绿,
        "五行": 五行.土,
        "处置": "保存状态 → 保留DNA链"
    },
    八门.伤门: {
        "触发条件": "检测到攻击行为",
        "三色": 三色.红,
        "五行": 五行.金,
        "处置": "触发公安联动 → 熔断服务 → DNA取证"
    },
    八门.杜门: {
        "触发条件": "服务主动隔离",
        "三色": 三色.黄,
        "五行": 五行.土,
        "处置": "暂停服务 → 等待三色审计"
    },
    八门.景门: {
        "触发条件": "服务对外展示/演示",
        "三色": 三色.绿,
        "五行": 五行.水,
        "处置": "记录访问日志 → DNA追溯"
    },
    八门.死门: {
        "触发条件": "服务异常崩溃",
        "三色": 三色.红,
        "五行": 五行.金,
        "处置": "熔断 → DNA取证 → 自动重启 → 记录耻辱墙"
    },
    八门.惊门: {
        "触发条件": "检测到入侵尝试",
        "三色": 三色.红,
        "五行": 五行.火,
        "处置": "触发报警 → 锁定IP → DNA取证"
    },
}


def 获取门机规则(门名: 八门) -> dict:
    return 门机规则.get(门名, {})


def 获取五行(门名: 八门) -> 五行:
    """从规则表中动态获取五行归属，避免硬编码"""
    return 门机规则.get(门名, {}).get("五行", 五行.土)


def 判定门机(
    服务状态: str,
    是否异常: bool,
    是否攻击: bool = False,
    是否入侵: bool = False
) -> 八门:
    if 是否攻击:
        return 八门.伤门
    if 是否入侵:
        return 八门.惊门
    if 服务状态 == "crashed":
        return 八门.死门
    if 服务状态 == "upgrading":
        return 八门.升门
    if 服务状态 == "sleeping":
        return 八门.休门
    if 服务状态 == "stopped" and 是否异常:
        return 八门.杜门
    if 服务状态 == "running":
        return 八门.生门
    return 八门.景门
