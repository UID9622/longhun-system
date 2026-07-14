#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂文化标签体系 v1.1 | LongHun Tag System v1.1
UID: 9622
DNA: #龍芯⚡️2026-07-01-LONGHUN-TAG-SYSTEM-v1.1
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

功能: 中国传统文化标签系统，替代西方emoji
支持: 五行、八卦、甲骨文、二十八星宿
作者: 龍魂系统(UID9622)

v1.1 迭代要点（小艺设计评审）:
- 深化文化解释：五行生克制化、八卦易象、甲骨字源、星宿神话
- 统一视觉配色：定义标准五行色板并在全体系复用
- 支持动态扩展：TagExtensionRegistry + JSON Schema + 版本控制
- 增强渲染：组合标签、CSS 变量、ANSI 真彩色
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

__version__ = "1.1.0"
LAST_UPDATED = "2026-07-01T01:19:08Z"

# ==================== 0. 标准配色与状态映射 ====================
COLOR_PALETTE: Dict[str, Dict[str, str]] = {
    "金": {
        "base": "#FFD700", "light": "#FFF8DC", "dark": "#B8860B",
        "peak": "#FFD700", "rest": "#C0C0C0", "trap": "#808080",
    },
    "木": {
        "base": "#228B22", "light": "#90EE90", "dark": "#006400",
        "peak": "#006400", "rest": "#8FBC8F", "trap": "#556B2F",
    },
    "水": {
        "base": "#1E90FF", "light": "#87CEEB", "dark": "#00008B",
        "peak": "#00008B", "rest": "#4682B4", "trap": "#191970",
    },
    "火": {
        "base": "#DC143C", "light": "#FF6347", "dark": "#8B0000",
        "peak": "#8B0000", "rest": "#CD5C5C", "trap": "#800000",
    },
    "土": {
        "base": "#8B4513", "light": "#D2B48C", "dark": "#654321",
        "peak": "#8B4513", "rest": "#A0522D", "trap": "#654321",
    },
}

STATE_TO_PALETTE_KEY = {"生": "light", "旺": "peak", "休": "rest", "囚": "trap"}

WUXING_CULTURAL_NOTES: Dict[str, Dict[str, str]] = {
    "金": {
        "生克": "金曰从革，性收敛肃杀。秋金收敛而春木生发，故金克木；金液化露而生水，故土能生金。制化：金旺需火炼方能成器，过刚则折。",
        "生成": "金生水（金寒水凝、液化成露），土生金（矿藏出于土中）。",
    },
    "木": {
        "生克": "木曰曲直，性生发条达。春木破土，故木克土；水生木而木生火。制化：木旺需金修剪，过盛则折，故金克木以成栋梁。",
        "生成": "木生火（木性温暖，火伏其中），水生木（水润草木）。",
    },
    "水": {
        "生克": "水曰润下，性寒凉下行。水润草木故生水生木；水能灭火故水克火。制化：水旺需土堤防，否则泛滥成灾。",
        "生成": "水生木，金生水（金液凝露、少阴生水）。",
    },
    "火": {
        "生克": "火曰炎上，性温热升腾。火烬成土故火生土；火能熔金故火克金。制化：火旺需水济，否则焚原。",
        "生成": "火生土（灰烬归土），木生火（钻木取火）。",
    },
    "土": {
        "生克": "土爰稼穑，性承载化育。土中藏金故土能生金；土能止水故土克水。制化：土旺需木疏，否则板结不化。",
        "生成": "土生金，火生土（火烬成土）。",
    },
}


# ==================== 1. 五行标签体系 ====================
五行标签 = {
    "金": {
        "unicode": "金",
        "color": COLOR_PALETTE["金"]["base"], "bg_color": "#F5F5DC",
        "cultural_note": WUXING_CULTURAL_NOTES["金"]["生克"],
        "states": {
            "生": {"symbol": "金🌱", "desc": "金生·萌发", "hex": COLOR_PALETTE["金"]["light"],
                   "usage": "新功能开发、资源初始化", "code": "METAL_BIRTH"},
            "旺": {"symbol": "金🔥", "desc": "金旺·鼎盛", "hex": COLOR_PALETTE["金"]["peak"],
                   "usage": "性能峰值、满载运行", "code": "METAL_PEAK"},
            "休": {"symbol": "金💤", "desc": "金休·收敛", "hex": COLOR_PALETTE["金"]["rest"],
                   "usage": "资源回收、低功耗模式", "code": "METAL_REST"},
            "囚": {"symbol": "金⛔", "desc": "金囚·受限", "hex": COLOR_PALETTE["金"]["trap"],
                   "usage": "权限不足、资源锁定", "code": "METAL_TRAP"},
        }
    },
    "木": {
        "unicode": "木",
        "color": COLOR_PALETTE["木"]["base"], "bg_color": "#E8F5E9",
        "cultural_note": WUXING_CULTURAL_NOTES["木"]["生克"],
        "states": {
            "生": {"symbol": "木🌱", "desc": "木生·萌芽", "hex": COLOR_PALETTE["木"]["light"],
                   "usage": "项目立项、架构设计", "code": "WOOD_BIRTH"},
            "旺": {"symbol": "木🌳", "desc": "木旺·繁茂", "hex": COLOR_PALETTE["木"]["peak"],
                   "usage": "功能完备、生态繁荣", "code": "WOOD_PEAK"},
            "休": {"symbol": "木🍂", "desc": "木休·落叶", "hex": COLOR_PALETTE["木"]["rest"],
                   "usage": "版本归档、迭代暂停", "code": "WOOD_REST"},
            "囚": {"symbol": "木🐘", "desc": "木囚·受压", "hex": COLOR_PALETTE["木"]["trap"],
                   "usage": "技术债务、依赖阻塞", "code": "WOOD_TRAP"},
        }
    },
    "水": {
        "unicode": "水",
        "color": COLOR_PALETTE["水"]["base"], "bg_color": "#E3F2FD",
        "cultural_note": WUXING_CULTURAL_NOTES["水"]["生克"],
        "states": {
            "生": {"symbol": "水💧", "desc": "水生·滴落", "hex": COLOR_PALETTE["水"]["light"],
                   "usage": "数据接入、流程启动", "code": "WATER_BIRTH"},
            "旺": {"symbol": "水🌊", "desc": "水旺·奔流", "hex": COLOR_PALETTE["水"]["peak"],
                   "usage": "高并发、数据洪流", "code": "WATER_PEAK"},
            "休": {"symbol": "水🧜", "desc": "水休·静潭", "hex": COLOR_PALETTE["水"]["rest"],
                   "usage": "缓存待机、连接池休眠", "code": "WATER_REST"},
            "囚": {"symbol": "水🔒", "desc": "水囚·冰封", "hex": COLOR_PALETTE["水"]["trap"],
                   "usage": "安全冻结、访问拒绝", "code": "WATER_TRAP"},
        }
    },
    "火": {
        "unicode": "火",
        "color": COLOR_PALETTE["火"]["base"], "bg_color": "#FFEBEE",
        "cultural_note": WUXING_CULTURAL_NOTES["火"]["生克"],
        "states": {
            "生": {"symbol": "火🔥", "desc": "火生·点燃", "hex": COLOR_PALETTE["火"]["light"],
                   "usage": "UI渲染、告警触发", "code": "FIRE_BIRTH"},
            "旺": {"symbol": "火💀", "desc": "火旺·炽烈", "hex": COLOR_PALETTE["火"]["peak"],
                   "usage": "系统过载、紧急告警", "code": "FIRE_PEAK"},
            "休": {"symbol": "火♨", "desc": "火休·余温", "hex": COLOR_PALETTE["火"]["rest"],
                   "usage": "降级运行、维护模式", "code": "FIRE_REST"},
            "囚": {"symbol": "火🚨", "desc": "火囚·熄灭", "hex": COLOR_PALETTE["火"]["trap"],
                   "usage": "服务宕机、系统崩溃", "code": "FIRE_TRAP"},
        }
    },
    "土": {
        "unicode": "土",
        "color": COLOR_PALETTE["土"]["base"], "bg_color": "#F5F5DC",
        "cultural_note": WUXING_CULTURAL_NOTES["土"]["生克"],
        "states": {
            "生": {"symbol": "土🌱", "desc": "土生·播种", "hex": COLOR_PALETTE["土"]["light"],
                   "usage": "基础设施部署", "code": "EARTH_BIRTH"},
            "旺": {"symbol": "土🏔", "desc": "土旺·稳重", "hex": COLOR_PALETTE["土"]["peak"],
                   "usage": "核心系统稳定运行", "code": "EARTH_PEAK"},
            "休": {"symbol": "土🗻", "desc": "土休·沉淀", "hex": COLOR_PALETTE["土"]["rest"],
                   "usage": "数据归档、日志沉淀", "code": "EARTH_REST"},
            "囚": {"symbol": "土⛰", "desc": "土囚·塌陷", "hex": COLOR_PALETTE["土"]["trap"],
                   "usage": "存储满、基础设施故障", "code": "EARTH_TRAP"},
        }
    },
}

五行生克 = {
    "生": [("金", "水"), ("水", "木"), ("木", "火"), ("火", "土"), ("土", "金")],
    "克": [("金", "木"), ("木", "土"), ("土", "水"), ("水", "火"), ("火", "金")],
}

# ==================== 2. 八卦标签体系 ====================
八卦标签 = {
    "乾": {
        "unicode_char": "乾", "unicode_trigram": "☰",
        "element": "金", "direction": "西北", "modern_map": "系统/天",
        "color": COLOR_PALETTE["金"]["base"],
        "palette": COLOR_PALETTE["金"],
        "yi_jing_context": {"name_meaning": "健", "natural_image": "天", "virtue": "刚健中正，自强不息"},
        "variants": {
            "正": {"label": "乾·正位", "usage": "系统正常运行、天级服务", "state": "stable"},
            "反": {"label": "乾·反转", "usage": "系统降级、天地交泰", "state": "degraded"},
            "动": {"label": "乾·动爻", "usage": "系统告警、天变预警", "state": "alert"},
        }
    },
    "坤": {
        "unicode_char": "坤", "unicode_trigram": "☷",
        "element": "土", "direction": "西南", "modern_map": "数据/地",
        "color": COLOR_PALETTE["土"]["base"],
        "palette": COLOR_PALETTE["土"],
        "yi_jing_context": {"name_meaning": "顺", "natural_image": "地", "virtue": "厚德载物，柔顺承天"},
        "variants": {
            "正": {"label": "坤·正位", "usage": "数据库正常、地稳存储", "state": "stable"},
            "反": {"label": "坤·反转", "usage": "数据迁移、天地倒悬", "state": "migrating"},
            "动": {"label": "坤·动爻", "usage": "数据同步、地质变动", "state": "syncing"},
        }
    },
    "震": {
        "unicode_char": "震", "unicode_trigram": "☳",
        "element": "木", "direction": "东", "modern_map": "启动/雷",
        "color": COLOR_PALETTE["木"]["base"],
        "palette": COLOR_PALETTE["木"],
        "yi_jing_context": {"name_meaning": "动", "natural_image": "雷", "virtue": "恐惧修省，奋发而动"},
        "variants": {
            "正": {"label": "震·正位", "usage": "服务启动、雷鸣触发", "state": "starting"},
            "反": {"label": "震·反转", "usage": "启动失败、雷风相薄", "state": "failed"},
            "动": {"label": "震·动爻", "usage": "紧急启动、雷霆万钧", "state": "urgent"},
        }
    },
    "巽": {
        "unicode_char": "巽", "unicode_trigram": "☴",
        "element": "木", "direction": "东南", "modern_map": "传播/风",
        "color": COLOR_PALETTE["木"]["base"],
        "palette": COLOR_PALETTE["木"],
        "yi_jing_context": {"name_meaning": "入", "natural_image": "风", "virtue": "谦逊顺从，无孔不入"},
        "variants": {
            "正": {"label": "巽·正位", "usage": "消息分发、风行天下", "state": "distributing"},
            "反": {"label": "巽·反转", "usage": "传播阻塞、风雷乱序", "state": "blocked"},
            "动": {"label": "巽·动爻", "usage": "广播风暴、飓风传播", "state": "storm"},
        }
    },
    "坎": {
        "unicode_char": "坎", "unicode_trigram": "☵",
        "element": "水", "direction": "北", "modern_map": "安全/水",
        "color": COLOR_PALETTE["水"]["base"],
        "palette": COLOR_PALETTE["水"],
        "yi_jing_context": {"name_meaning": "陷/习坎", "natural_image": "水", "virtue": "行险而不失其信，外柔内刚"},
        "variants": {
            "正": {"label": "坎·正位", "usage": "安全防护、水润无声", "state": "protected"},
            "反": {"label": "坎·反转", "usage": "安全突破、水火不容", "state": "breached"},
            "动": {"label": "坎·动爻", "usage": "洪水攻击、安全告警", "state": "attacked"},
        }
    },
    "离": {
        "unicode_char": "离", "unicode_trigram": "☲",
        "element": "火", "direction": "南", "modern_map": "显示/火",
        "color": COLOR_PALETTE["火"]["base"],
        "palette": COLOR_PALETTE["火"],
        "yi_jing_context": {"name_meaning": "丽/附丽", "natural_image": "火", "virtue": "光明正大，柔丽乎中正"},
        "variants": {
            "正": {"label": "离·正位", "usage": "UI正常、光明普照", "state": "display_ok"},
            "反": {"label": "离·反转", "usage": "显示异常、火火未济", "state": "display_error"},
            "动": {"label": "离·动爻", "usage": "渲染过载、烈火焚原", "state": "render_overload"},
        }
    },
    "艮": {
        "unicode_char": "艮", "unicode_trigram": "☶",
        "element": "土", "direction": "东北", "modern_map": "停止/山",
        "color": COLOR_PALETTE["土"]["base"],
        "palette": COLOR_PALETTE["土"],
        "yi_jing_context": {"name_meaning": "止", "natural_image": "山", "virtue": "知止而定，敦厚沉静"},
        "variants": {
            "正": {"label": "艮·正位", "usage": "服务停止、山止行止", "state": "stopped"},
            "反": {"label": "艮·反转", "usage": "强制关闭崩解、山泽通气", "state": "crashed"},
            "动": {"label": "艮·动爻", "usage": "优雅关闭、山脉崩塌", "state": "shutting_down"},
        }
    },
    "兑": {
        "unicode_char": "兑", "unicode_trigram": "☱",
        "element": "金", "direction": "西", "modern_map": "交流/泽",
        "color": COLOR_PALETTE["金"]["base"],
        "palette": COLOR_PALETTE["金"],
        "yi_jing_context": {"name_meaning": "悦/说", "natural_image": "泽", "virtue": "和悦接物，朋友讲习"},
        "variants": {
            "正": {"label": "兑·正位", "usage": "API正常、泽润万物", "state": "connected"},
            "反": {"label": "兑·反转", "usage": "通信中断、泽山咸阻", "state": "disconnected"},
            "动": {"label": "兑·动爻", "usage": "高频通信、泽涌洪波", "state": "high_freq"},
        }
    },
}

# ==================== 3. 甲骨文标签体系 ====================
甲骨文标签 = {
    "启": {"unicode": "启", "category": "状态", "pinyin": "qi",
        "modern": "开始/启动", "usage": "项目启动、功能开启", "color": "#00C853", "tag": "START",
        "oracle_context": "甲骨文像以手启户，本义开门，引申为开始、启动。"},
    "止": {"unicode": "止", "category": "状态", "pinyin": "zhi",
        "modern": "停止/终止", "usage": "进程停止、服务终止", "color": "#FF1744", "tag": "STOP",
        "oracle_context": "甲骨文像足趾形，本义足、行走，引申为停止、止步。"},
    "行": {"unicode": "行", "category": "状态", "pinyin": "xing",
        "modern": "运行/执行", "usage": "任务运行、进行中", "color": "#2979FF", "tag": "RUN",
        "oracle_context": "甲骨文像十字路口，本义道路，引申为运行、执行。"},
    "立": {"unicode": "立", "category": "状态", "pinyin": "li",
        "modern": "建立/就绪", "usage": "实例就绪、资源就位", "color": "#651FFF", "tag": "READY",
        "oracle_context": "甲骨文像人正面站立于地，本义站立，引申为建立、就绪。"},
    "生": {"unicode": "生", "category": "状态", "pinyin": "sheng",
        "modern": "生成/创建", "usage": "资源创建、实例生成", "color": "#00E676", "tag": "CREATE",
        "oracle_context": "甲骨文像草木出土生长，本义生长，引申为生成、创建。"},
    "死": {"unicode": "死", "category": "状态", "pinyin": "si",
        "modern": "销毁/死亡", "usage": "实例销毁、资源释放", "color": "#424242", "tag": "DESTROY",
        "oracle_context": "甲骨文像人跪拜于枯骨旁，本义死亡，引申为销毁、终结。"},
    "变": {"unicode": "变", "category": "状态", "pinyin": "bian",
        "modern": "变更/转换", "usage": "状态变更、配置更新", "color": "#FF9100", "tag": "CHANGE",
        "oracle_context": "甲骨文从攴从丝，本义更改、变换，引申为变更。"},
    "等": {"unicode": "等", "category": "状态", "pinyin": "deng",
        "modern": "等待/队列", "usage": "任务排队、等待资源", "color": "#78909C", "tag": "WAIT",
        "oracle_context": "甲骨文从竹从寺，本义整齐、等级，引申为等待、队列。"},
    "成": {"unicode": "成", "category": "状态", "pinyin": "cheng",
        "modern": "成功/完成", "usage": "操作成功、任务完成", "color": "#00C853", "tag": "SUCCESS",
        "oracle_context": "甲骨文像斧钺斩物，本义完成、成就，引申为成功。"},
    "败": {"unicode": "败", "category": "状态", "pinyin": "bai",
        "modern": "失败/错误", "usage": "操作失败、异常捕获", "color": "#D50000", "tag": "FAIL",
        "oracle_context": "甲骨文从攴从贝，本义毁坏、败坏，引申为失败。"},

    "喜": {"unicode": "喜", "category": "情绪", "pinyin": "xi",
        "modern": "喜悦/好评", "usage": "用户满意、正向反馈", "color": "#FFEA00", "tag": "JOY",
        "oracle_context": "甲骨文像鼓上置口，本义喜乐，引申为喜悦、好评。"},
    "怒": {"unicode": "怒", "category": "情绪", "pinyin": "nu",
        "modern": "愤怒/告警", "usage": "严重告警、用户投诉", "color": "#DD2C00", "tag": "ANGER",
        "oracle_context": "从心奴声，本义愤怒，引申为强烈告警。"},
    "哀": {"unicode": "哀", "category": "情绪", "pinyin": "ai",
        "modern": "哀伤/降级", "usage": "服务降级、功能下线", "color": "#546E7A", "tag": "SORROW",
        "oracle_context": "从口衣声，本义悲伤，引申为哀伤、降级。"},
    "乐": {"unicode": "乐", "category": "情绪", "pinyin": "le",
        "modern": "快乐/庆祝", "usage": "里程碑达成、发布庆祝", "color": "#FFD600", "tag": "CELEBRATE",
        "oracle_context": "甲骨文像丝弦乐器，本义音乐、快乐，引申为庆祝。"},
    "恐": {"unicode": "恐", "category": "情绪", "pinyin": "kong",
        "modern": "恐惧/危险", "usage": "安全威胁、高危漏洞", "color": "#4A148C", "tag": "FEAR",
        "oracle_context": "从心巩声，本义恐惧，引申为高危危险。"},
    "惊": {"unicode": "惊", "category": "情绪", "pinyin": "jing",
        "modern": "惊讶/异常", "usage": "意外异常、罕见错误", "color": "#FF6D00", "tag": "SURPRISE",
        "oracle_context": "从心京声，本义惊动、惊慌，引申为异常告警。"},
    "爱": {"unicode": "爱", "category": "情绪", "pinyin": "ai2",
        "modern": "喜爱/推荐", "usage": "用户喜爱、推荐系统", "color": "#FF4081", "tag": "LOVE",
        "oracle_context": "从心旡声，本义亲爱、喜爱，引申为推荐、喜爱。"},
    "恶": {"unicode": "恶", "category": "情绪", "pinyin": "wu",
        "modern": "厌恶/屏蔽", "usage": "内容过滤、黑名单", "color": "#212121", "tag": "BLOCK",
        "oracle_context": "从心亚声，本义厌恶，引申为屏蔽、过滤。"},
    "疑": {"unicode": "疑", "category": "情绪", "pinyin": "yi",
        "modern": "怀疑/待审", "usage": "待审核、可疑行为", "color": "#827717", "tag": "SUSPECT",
        "oracle_context": "像人持杖侧首犹豫，本义怀疑，引申为待审。"},
    "信": {"unicode": "信", "category": "情绪", "pinyin": "xin",
        "modern": "信任/认证", "usage": "身份认证、信任链", "color": "#0091EA", "tag": "TRUST",
        "oracle_context": "从人从言，本义言语真实，引申为信任、认证。"},

    "见": {"unicode": "见", "category": "功能", "pinyin": "jian",
        "modern": "查看/读取", "usage": "数据查询、日志查看", "color": "#00B0FF", "tag": "READ",
        "oracle_context": "甲骨文像人上有目，本义看见，引申为读取、查询。"},
    "闻": {"unicode": "闻", "category": "功能", "pinyin": "wen",
        "modern": "监听/通知", "usage": "事件监听、消息通知", "color": "#76FF03", "tag": "LISTEN",
        "oracle_context": "甲骨文像人附耳于门，本义听闻，引申为监听、通知。"},
    "言": {"unicode": "言", "category": "功能", "pinyin": "yan",
        "modern": "写入/发言", "usage": "数据写入、用户评论", "color": "#FF3D00", "tag": "WRITE",
        "oracle_context": "甲骨文像舌从口出，本义说话，引申为写入、发言。"},
    "思": {"unicode": "思", "category": "功能", "pinyin": "si",
        "modern": "分析/计算", "usage": "数据分析、算法运算", "color": "#651FFF", "tag": "ANALYZE",
        "oracle_context": "甲骨文从囟从心，本义思考，引申为分析、计算。"},
    "守": {"unicode": "守", "category": "功能", "pinyin": "shou",
        "modern": "守护/监控", "usage": "系统监控、守护进程", "color": "#1DE9B6", "tag": "MONITOR",
        "oracle_context": "甲骨文从宀从寸，本义守护，引申为监控、守护。"},
    "攻": {"unicode": "攻", "category": "功能", "pinyin": "gong",
        "modern": "攻击/测试", "usage": "渗透测试、压力测试", "color": "#C62828", "tag": "PENTEST",
        "oracle_context": "从攴从工，本义攻击，引申为测试、攻防。"},
    "取": {"unicode": "取", "category": "功能", "pinyin": "qu",
        "modern": "获取/拉取", "usage": "数据拉取、资源获取", "color": "#2962FF", "tag": "FETCH",
        "oracle_context": "甲骨文像以手取耳，本义获取，引申为拉取、获取。"},
    "与": {"unicode": "与", "category": "功能", "pinyin": "yu",
        "modern": "给予/推送", "usage": "数据推送、消息发送", "color": "#AA00FF", "tag": "PUSH",
        "oracle_context": "甲骨文像双手共举一物，本义给予，引申为推送。"},
    "分": {"unicode": "分", "category": "功能", "pinyin": "fen",
        "modern": "分割/分区", "usage": "数据分片、服务分区", "color": "#0097A7", "tag": "PARTITION",
        "oracle_context": "甲骨文像刀分物，本义分开，引申为分区、分片。"},
    "合": {"unicode": "合", "category": "功能", "pinyin": "he",
        "modern": "合并/聚合", "usage": "数据聚合、服务合并", "color": "#43A047", "tag": "MERGE",
        "oracle_context": "甲骨文像上下两口相合，本义闭合，引申为合并、聚合。"},

    "上": {"unicode": "上", "category": "等级", "pinyin": "shang",
        "modern": "高级/P0", "usage": "最高优先级、核心服务", "color": "#D50000", "tag": "P0",
        "oracle_context": "甲骨文像短横在长横之上，本义上面，引申为高级、优先。"},
    "中": {"unicode": "中", "category": "等级", "pinyin": "zhong",
        "modern": "中级/P1", "usage": "普通优先级、一般任务", "color": "#FF6D00", "tag": "P1",
        "oracle_context": "甲骨文像旗旒正中，本义中间，引申为适中、中级。"},
    "下": {"unicode": "下", "category": "等级", "pinyin": "xia",
        "modern": "低级/P2", "usage": "低优先级、后台任务", "color": "#64DD17", "tag": "P2",
        "oracle_context": "甲骨文像短横在长横之下，本义下面，引申为低级、后台。"},
    "大": {"unicode": "大", "category": "等级", "pinyin": "da",
        "modern": "大规模/L", "usage": "大数据量、大规模集群", "color": "#B71C1C", "tag": "LARGE",
        "oracle_context": "甲骨文像张开双臂的人，本义大人，引申为宏大、大规模。"},
    "小": {"unicode": "小", "category": "等级", "pinyin": "xiao",
        "modern": "小规模/S", "usage": "轻量服务、小规模部署", "color": "#81C784", "tag": "SMALL",
        "oracle_context": "甲骨文像沙粒细微，本义细小，引申为轻量、小规模。"},
    "初": {"unicode": "初", "category": "等级", "pinyin": "chu",
        "modern": "初级/L1", "usage": "初级问题、入门级", "color": "#69F0AE", "tag": "L1",
        "oracle_context": "从刀从衣，本义裁衣之始，引申为初级、开始。"},
    "高": {"unicode": "高", "category": "等级", "pinyin": "gao",
        "modern": "高级/L3", "usage": "高级工程师、高难度", "color": "#E53935", "tag": "L3",
        "oracle_context": "甲骨文像楼阁高耸，本义高大，引申为高级、高难度。"},
    "低": {"unicode": "低", "category": "等级", "pinyin": "di",
        "modern": "低级/L0", "usage": "基础服务、低配置", "color": "#A5D6A7", "tag": "L0",
        "oracle_context": "从人氐声，本义低下，引申为基础、低配置。"},
    "王": {"unicode": "王", "category": "等级", "pinyin": "wang",
        "modern": "王者/核心", "usage": "核心模块、主服务", "color": "#FFD700", "tag": "CORE",
        "oracle_context": "甲骨文像斧钺形，象征权力，本义君主，引申为核心。"},
    "民": {"unicode": "民", "category": "等级", "pinyin": "min",
        "modern": "普通/边缘", "usage": "边缘服务、普通节点", "color": "#9E9E9E", "tag": "EDGE",
        "oracle_context": "甲骨文像锥刺目，本义被征服者，今指人民、普通节点。"},
}

# ==================== 4. 二十八星宿标签体系 ====================
星宿标签 = {
    "角": {"unicode": "角", "beast": "青龍", "beast_code": "dragon",
        "position": 1, "modern": "初始化/入口", "color": "#4CAF50", "tag": "INIT",
        "usage": "系统初始化、项目入口",
        "constellation_myth": "青龍之角，象征万物萌生，天门初开。"},
    "亢": {"unicode": "亢", "beast": "青龍", "beast_code": "dragon",
        "position": 2, "modern": "防御/守护", "color": "#43A047", "tag": "DEFENSE",
        "usage": "安全防护、访问控制",
        "constellation_myth": "青龍之颈，高昂护主，主风云变化。"},
    "氐": {"unicode": "氐", "beast": "青龍", "beast_code": "dragon",
        "position": 3, "modern": "根基/基础", "color": "#388E3C", "tag": "FOUNDATION",
        "usage": "基础设施、核心依赖",
        "constellation_myth": "青龍之胸，根基所在，主安定与财富。"},
    "房": {"unicode": "房", "beast": "青龍", "beast_code": "dragon",
        "position": 4, "modern": "存储/仓库", "color": "#2E7D32", "tag": "STORAGE",
        "usage": "数据仓库、存储服务",
        "constellation_myth": "青龍之腹，又称天驷，主车马仓储。"},
    "心": {"unicode": "心", "beast": "青龍", "beast_code": "dragon",
        "position": 5, "modern": "核心/引擎", "color": "#1B5E20", "tag": "ENGINE",
        "usage": "核心引擎、主服务",
        "constellation_myth": "青龍之心，又称大火，主帝王政事。"},
    "尾": {"unicode": "尾", "beast": "青龍", "beast_code": "dragon",
        "position": 6, "modern": "日志/追踪", "color": "#66BB6A", "tag": "TRACE",
        "usage": "日志系统、调用链追踪",
        "constellation_myth": "青龍之尾，摆动生风，主后宫与子孙。"},
    "箕": {"unicode": "箕", "beast": "青龍", "beast_code": "dragon",
        "position": 7, "modern": "收集/汇聚", "color": "#81C784", "tag": "COLLECT",
        "usage": "数据收集、日志汇聚",
        "constellation_myth": "青龍之尾末，簸扬谷物，主口舌是非。"},

    "斗": {"unicode": "斗", "beast": "玄武", "beast_code": "tortoise",
        "position": 8, "modern": "调度/编排", "color": "#1976D2", "tag": "SCHEDULER",
        "usage": "任务调度、容器编排",
        "constellation_myth": "玄武之首，南斗主生，司寿命爵禄。"},
    "牛": {"unicode": "牛", "beast": "玄武", "beast_code": "tortoise",
        "position": 9, "modern": "负载/计算", "color": "#1565C0", "tag": "COMPUTE",
        "usage": "计算节点、负载均衡",
        "constellation_myth": "玄武之躯，牵牛织女传说所在，主农耕。"},
    "女": {"unicode": "女", "beast": "玄武", "beast_code": "tortoise",
        "position": 10, "modern": "编织/关联", "color": "#0D47A1", "tag": "RELATE",
        "usage": "数据编织、关联分析",
        "constellation_myth": "玄武之龟身，又称婺女，主女工纺织。"},
    "虚": {"unicode": "虚", "beast": "玄武", "beast_code": "tortoise",
        "position": 11, "modern": "虚拟/抽象", "color": "#42A5F5", "tag": "VIRTUAL",
        "usage": "虚拟化、抽象层",
        "constellation_myth": "玄武之龟腹，主秋冬虚耗、祭祀。"},
    "危": {"unicode": "危", "beast": "玄武", "beast_code": "tortoise",
        "position": 12, "modern": "风险/预警", "color": "#EF5350", "tag": "RISK",
        "usage": "风险预警、危机处理",
        "constellation_myth": "玄武之龟尾，高峻危险，主丧葬建筑。"},
    "室": {"unicode": "室", "beast": "玄武", "beast_code": "tortoise",
        "position": 13, "modern": "空间/环境", "color": "#1E88E5", "tag": "ENV",
        "usage": "运行环境、命名空间",
        "constellation_myth": "玄武之龟壳，营室主土功、宫室。"},
    "壁": {"unicode": "壁", "beast": "玄武", "beast_code": "tortoise",
        "position": 14, "modern": "边界/防火墙", "color": "#2196F3", "tag": "BOUNDARY",
        "usage": "网络边界、防火墙",
        "constellation_myth": "玄武之尾末，主文章典籍、边界。"},

    "奎": {"unicode": "奎", "beast": "白虎", "beast_code": "tiger",
        "position": 15, "modern": "缓存/加速", "color": "#E0E0E0", "tag": "CACHE",
        "usage": "缓存层、CDN加速",
        "constellation_myth": "白虎之股，主库兵戎马、文章。"},
    "娄": {"unicode": "娄", "beast": "白虎", "beast_code": "tiger",
        "position": 16, "modern": "聚合/汇总", "color": "#BDBDBD", "tag": "AGGREGATE",
        "usage": "数据聚合、报表汇总",
        "constellation_myth": "白虎之腰，主聚众、牺牲。"},
    "胃": {"unicode": "胃", "beast": "白虎", "beast_code": "tiger",
        "position": 17, "modern": "消化/处理", "color": "#9E9E9E", "tag": "PROCESS",
        "usage": "数据处理、ETL管道",
        "constellation_myth": "白虎之腹，主仓廪饮食。"},
    "昴": {"unicode": "昴", "beast": "白虎", "beast_code": "tiger",
        "position": 18, "modern": "星群/集群", "color": "#757575", "tag": "CLUSTER",
        "usage": "服务集群、星型拓扑",
        "constellation_myth": "白虎之胸，昴日星君居此，主狱讼。"},
    "毕": {"unicode": "毕", "beast": "白虎", "beast_code": "tiger",
        "position": 19, "modern": "完成/终结", "color": "#616161", "tag": "COMPLETE",
        "usage": "任务完成、流水线结束",
        "constellation_myth": "白虎之首，状如捕兔之网，主边兵弋猎。"},
    "觜": {"unicode": "觜", "beast": "白虎", "beast_code": "tiger",
        "position": 20, "modern": "精细/优化", "color": "#F5F5F5", "tag": "OPTIMIZE",
        "usage": "性能优化、精细调参",
        "constellation_myth": "白虎之口，主葆旅、珍贵之物。"},
    "参": {"unicode": "参", "beast": "白虎", "beast_code": "tiger",
        "position": 21, "modern": "参考/基准", "color": "#424242", "tag": "BENCHMARK",
        "usage": "基准测试、参考实现",
        "constellation_myth": "白虎前肢，主斩刈、军事。"},

    "井": {"unicode": "井", "beast": "朱雀", "beast_code": "phoenix",
        "position": 22, "modern": "源头/输入", "color": "#FF5722", "tag": "SOURCE",
        "usage": "数据源、消息入口",
        "constellation_myth": "朱雀之首，主水陆道路、泉源。"},
    "鬼": {"unicode": "鬼", "beast": "朱雀", "beast_code": "phoenix",
        "position": 23, "modern": "隐藏/秘钥", "color": "#E64A19", "tag": "SECRET",
        "usage": "密钥管理、隐藏配置",
        "constellation_myth": "朱雀之目，主祭祀、鬼神。"},
    "柳": {"unicode": "柳", "beast": "朱雀", "beast_code": "phoenix",
        "position": 24, "modern": "灵活/弹性", "color": "#D84315", "tag": "FLEX",
        "usage": "弹性伸缩、柔性架构",
        "constellation_myth": "朱雀之颈，主庖厨、酒食。"},
    "星": {"unicode": "星", "beast": "朱雀", "beast_code": "phoenix",
        "position": 25, "modern": "标记/亮点", "color": "#FF8A65", "tag": "FEATURE",
        "usage": "功能亮点、星标项目",
        "constellation_myth": "朱雀之胸，七星如冠，主衣裳文绣。"},
    "张": {"unicode": "张", "beast": "朱雀", "beast_code": "phoenix",
        "position": 26, "modern": "展开/扩张", "color": "#FF7043", "tag": "EXPAND",
        "usage": "业务扩张、规模增长",
        "constellation_myth": "朱雀之胃，主觞客、宗庙。"},
    "翼": {"unicode": "翼", "beast": "朱雀", "beast_code": "phoenix",
        "position": 27, "modern": "辅助/增强", "color": "#FFAB91", "tag": "AUGMENT",
        "usage": "辅助服务、增强功能",
        "constellation_myth": "朱雀之翼，主乐府、戏乐。"},
    "轸": {"unicode": "轸", "beast": "朱雀", "beast_code": "phoenix",
        "position": 28, "modern": "循环/反馈", "color": "#BF360C", "tag": "FEEDBACK",
        "usage": "反馈循环、迭代优化",
        "constellation_myth": "朱雀之尾，主车骑、邮驿。"},
}


# ═══════════════════════════════════════════════════════════════
# 扩展注册表
# ═══════════════════════════════════════════════════════════════

class TagExtensionRegistry:
    """
    动态标签扩展注册表
    支持运行时注册新标签、JSON Schema 风格校验、导入导出与版本控制
    """

    VERSION = "1.0.0"

    # 按分类的最小必填字段
    _REQUIRED_FIELDS = {
        "五行": {"category", "code", "element", "state", "desc", "hex"},
        "八卦": {"category", "code", "gua", "variant", "label"},
        "甲骨文": {"category", "code", "char", "modern"},
        "星宿": {"category", "code", "star", "modern"},
        "custom": {"category", "code", "label"},
    }

    def __init__(self):
        self.entries: Dict[str, Dict[str, Any]] = {}

    def validate(self, entry: Dict[str, Any]) -> bool:
        """校验扩展条目是否符合 schema 要求"""
        if not isinstance(entry, dict):
            raise TypeError("条目必须是 dict")
        category = entry.get("category", "custom")
        required = self._REQUIRED_FIELDS.get(category, self._REQUIRED_FIELDS["custom"])
        missing = required - set(entry.keys())
        if missing:
            raise ValueError(f"缺少必填字段: {missing}")
        color = entry.get("color") or entry.get("hex")
        if color and not re.fullmatch(r"#[0-9A-Fa-f]{6}", str(color)):
            raise ValueError(f"颜色格式错误: {color}")
        return True

    def register(self, category: str, code: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """注册一个新扩展标签"""
        entry = {"category": category, "code": code, **data}
        self.validate(entry)
        self.entries[code] = entry
        return entry

    def export(self, path: str) -> None:
        """将扩展条目导出为 JSON"""
        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        with open(path_obj, "w", encoding="utf-8") as f:
            json.dump({
                "version": self.VERSION,
                "count": len(self.entries),
                "entries": self.entries,
            }, f, ensure_ascii=False, indent=2)

    def load(self, path: str) -> "TagExtensionRegistry":
        """从 JSON 加载并注册扩展条目"""
        with open(Path(path), "r", encoding="utf-8") as f:
            payload = json.load(f)
        entries = payload.get("entries", {})
        for code, entry in entries.items():
            cat = entry.get("category", "custom")
            data = {k: v for k, v in entry.items() if k not in ("category", "code")}
            self.register(cat, code, data)
        return self

    @property
    def version(self) -> str:
        return self.VERSION


# ═══════════════════════════════════════════════════════════════
# LongHunTagSystem 类封装
# ═══════════════════════════════════════════════════════════════

class LongHunTagSystem:
    """
    龍魂标签系统封装类
    提供五行、八卦、甲骨文、二十八星宿的统一查询与渲染
    v1.1 新增：文化解释、标准色板、扩展注册表、状态持久化
    """

    DNA = "#龍芯⚡️2026-07-01-LONGHUN-TAG-SYSTEM-v1.1"

    def __init__(self):
        self.五行 = 五行标签
        self.八卦 = 八卦标签
        self.甲骨文 = 甲骨文标签
        self.星宿 = 星宿标签
        self.生克 = 五行生克
        self.extensions = TagExtensionRegistry()
        self.version = __version__
        self.last_updated = LAST_UPDATED

    # ─────────────────────────────────────────────────────────
    # 查询方法
    # ─────────────────────────────────────────────────────────

    def get_tag(self, code: str) -> Optional[Dict]:
        """
        根据标签代码或中文键查询标签详情
        code 支持: METAL_PEAK, 金·旺, 乾·正位, 启, 角
        """
        # 1. 五行状态码
        for elem, data in self.五行.items():
            for state, sdata in data["states"].items():
                if code == sdata["code"] or code == f"{elem}·{state}" or code == sdata["desc"]:
                    return {"type": "五行", "element": elem, "state": state,
                            "cultural_note": data.get("cultural_note"), **sdata}

        # 2. 八卦
        for gua, data in self.八卦.items():
            for var, vdata in data["variants"].items():
                if code == vdata["label"] or code == f"{gua}·{var}":
                    return {"type": "八卦", "gua": gua, "variant": var,
                            "color": data["color"], "palette": data.get("palette"),
                            "yi_jing_context": data.get("yi_jing_context"), **vdata}

        # 3. 甲骨文
        if code in self.甲骨文:
            return {"type": "甲骨文", "char": code, **self.甲骨文[code]}

        # 4. 星宿
        if code in self.星宿:
            return {"type": "星宿", "star": code, **self.星宿[code]}

        # 5. 扩展标签
        if code in self.extensions.entries:
            return {"type": "扩展", **self.extensions.entries[code]}

        return None

    def get_wuxing_tags(self) -> List[Dict]:
        """返回全部五行标签列表"""
        result = []
        for elem, data in self.五行.items():
            for state, sdata in data["states"].items():
                result.append({"type": "五行", "element": elem, "state": state,
                               "cultural_note": data.get("cultural_note"), **sdata})
        return result

    def get_bagua_tags(self) -> List[Dict]:
        """返回全部八卦标签列表"""
        result = []
        for gua, data in self.八卦.items():
            for var, vdata in data["variants"].items():
                result.append({"type": "八卦", "gua": gua, "variant": var,
                               "color": data["color"], "palette": data.get("palette"),
                               "yi_jing_context": data.get("yi_jing_context"), **vdata})
        return result

    def get_oracle_tags(self) -> List[Dict]:
        """返回全部甲骨文标签列表"""
        return [{"type": "甲骨文", "char": k, **v} for k, v in self.甲骨文.items()]

    def get_xingxiu_tags(self) -> List[Dict]:
        """返回全部星宿标签列表"""
        return [{"type": "星宿", "star": k, **v} for k, v in self.星宿.items()]

    # ─────────────────────────────────────────────────────────
    # 渲染方法
    # ─────────────────────────────────────────────────────────

    def render_tag(self, code: str, style: str = "html") -> str:
        """
        渲染标签
        style: html | md | text | ansi
        """
        tag = self.get_tag(code)
        if not tag:
            return code

        label = tag.get("desc") or tag.get("label") or tag.get("char") or code
        color = tag.get("hex") or tag.get("color", "#333333")
        symbol = tag.get("symbol") or tag.get("unicode") or ""
        title = tag.get("usage", label)

        text = f"{symbol} {label}" if symbol and symbol not in label else label

        if style == "html":
            return f'<span style="color:{color};font-weight:bold" title="{title}">{text}</span>'
        elif style == "md":
            return f"`{text}`"
        elif style == "ansi":
            rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{text}\033[0m"
        else:
            return text

    def resolve_emoji(self, emoji: str) -> Optional[Dict]:
        """
        将西方emoji映射到龍魂标签
        简单内置映射 + 字符语义推断
        """
        try:
            from .cnsh_tag_variables import EMOJI_TO_LONGHUN
        except ImportError:
            from cnsh_tag_variables import EMOJI_TO_LONGHUN
        mapped = EMOJI_TO_LONGHUN.get(emoji)
        if mapped:
            tag = self.get_tag(mapped)
            if tag:
                tag["龍魂标签"] = mapped
                return tag

        # 语义推断
        infer_map = {
            "🔥": "火·旺", "💧": "水·生", "🌱": "木·生", "🌳": "木·旺",
            "⚡": "震·动", "🛡️": "坎·正", "🚨": "火·囚", "✅": "成",
            "❌": "败", "⏳": "等", "🚀": "震·动", "💀": "死",
            "⭐": "星", "🔒": "水·囚", "📊": "思", "❤️": "爱",
        }
        mapped = infer_map.get(emoji)
        if mapped:
            tag = self.get_tag(mapped)
            if tag:
                tag["龍魂标签"] = mapped
                return tag
        return None

    # ─────────────────────────────────────────────────────────
    # 组合与验证
    # ─────────────────────────────────────────────────────────

    def compose(self, base: str, variant: Optional[str] = None, modifier: Optional[str] = None) -> str:
        """组合标签，最多3层"""
        parts = [base]
        if variant:
            parts.append(variant)
        if modifier:
            parts.append(modifier)
        return "·".join(parts)

    def validate_combo(self, tag_a: str, tag_b: str) -> Tuple[bool, str]:
        """验证两个标签是否可以组合（基于五行生克）"""
        if tag_a in self.五行 and tag_b in self.五行:
            for sheng, bei in self.生克["生"]:
                if (tag_a == sheng and tag_b == bei) or (tag_b == sheng and tag_a == bei):
                    return True, f"{tag_a}与{tag_b}相生组合吉"
            for ke, bei in self.生克["克"]:
                if (tag_a == ke and tag_b == bei) or (tag_b == ke and tag_a == bei):
                    return False, f"{tag_a}克{tag_b}，相克组合凶，建议避免"
            return True, f"{tag_a}与{tag_b}同气相求，中性组合"
        return True, "非五行组合，无特殊限制"

    # ─────────────────────────────────────────────────────────
    # 扩展与持久化
    # ─────────────────────────────────────────────────────────

    def save(self, path: str) -> None:
        """保存整个系统状态（含扩展注册表）到 JSON"""
        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": self.version,
            "last_updated": self.last_updated,
            "dna": self.DNA,
            "五行": self.五行,
            "八卦": self.八卦,
            "甲骨文": self.甲骨文,
            "星宿": self.星宿,
            "生克": self.生克,
            "extensions": self.extensions.entries,
        }
        with open(path_obj, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def load(self, path: str) -> "LongHunTagSystem":
        """从 JSON 加载系统状态并合并扩展条目"""
        with open(Path(path), "r", encoding="utf-8") as f:
            payload = json.load(f)
        if "五行" in payload:
            self.五行 = payload["五行"]
        if "八卦" in payload:
            self.八卦 = payload["八卦"]
        if "甲骨文" in payload:
            self.甲骨文 = payload["甲骨文"]
        if "星宿" in payload:
            self.星宿 = payload["星宿"]
        if "生克" in payload:
            self.生克 = payload["生克"]
        self.version = payload.get("version", self.version)
        self.last_updated = payload.get("last_updated", self.last_updated)
        if "extensions" in payload:
            for code, entry in payload["extensions"].items():
                self.extensions.register(
                    entry.get("category", "custom"), code,
                    {k: v for k, v in entry.items() if k not in ("category", "code")}
                )
        return self

    def metadata(self) -> Dict:
        """返回系统元数据"""
        return {
            "system": "龍魂文化标签体系",
            "version": self.version,
            "last_updated": self.last_updated,
            "uid": "9622",
            "dna": self.DNA,
            "extension_registry_version": self.extensions.version,
            "counts": {
                "五行标签": len(self.五行) * 4,
                "八卦标签": len(self.八卦) * 3,
                "甲骨文标签": len(self.甲骨文),
                "星宿标签": len(self.星宿),
                "扩展标签": len(self.extensions.entries),
            },
            "total_tags": (len(self.五行) * 4 + len(self.八卦) * 3 +
                           len(self.甲骨文) + len(self.星宿) + len(self.extensions.entries)),
        }


# 保持向后兼容的模块级函数
LongHunTag = LongHunTagSystem


def main():
    print("=" * 60)
    print("龍魂文化标签体系 v1.1")
    print(f"UID: 9622 | DNA: {LongHunTagSystem.DNA}")
    print(f"版本: {__version__} | 更新时间: {LAST_UPDATED}")
    print("=" * 60)

    ts = LongHunTagSystem()
    meta = ts.metadata()
    print("\n标签统计:")
    for k, v in meta["counts"].items():
        print(f"  {k}: {v}")
    print(f"  总计: {meta['total_tags']}")

    print("\n文化解释示例:")
    for elem in ["金", "木", "水", "火", "土"]:
        note = ts.五行[elem].get("cultural_note", "")
        print(f"  {elem}: {note[:40]}...")

    print("\n八卦易象示例:")
    for gua in ["乾", "坤", "震", "离"]:
        ctx = ts.八卦[gua].get("yi_jing_context", {})
        print(f"  {gua}: {ctx.get('name_meaning')} | {ctx.get('natural_image')} | {ctx.get('virtue')}")

    print("\n甲骨字源示例:")
    for char in ["启", "信", "王", "民"]:
        ctx = ts.甲骨文[char].get("oracle_context", "")
        print(f"  {char}: {ctx[:40]}...")

    print("\n星宿神话示例:")
    for star in ["角", "斗", "奎", "井"]:
        myth = ts.星宿[star].get("constellation_myth", "")
        print(f"  {star}: {myth[:40]}...")

    print("\n查询示例:")
    print(f"  get_tag('METAL_PEAK'): {ts.get_tag('METAL_PEAK')['desc']}")
    print(f"  get_tag('启')['modern']: {ts.get_tag('启')['modern']}")

    print("\n渲染示例:")
    print(f"  text: {ts.render_tag('火·旺', 'text')}")
    print(f"  html: {ts.render_tag('火·旺', 'html')}")
    print(f"  ansi: {ts.render_tag('火·旺', 'ansi')}")
    print(f"  md:   {ts.render_tag('成', 'md')}")

    print("\n扩展注册表示例:")
    ts.extensions.register("custom", "CUSTOM_001", {"label": "自定义标签", "color": "#123456", "usage": "动态扩展测试"})
    print(f"  已注册扩展数: {len(ts.extensions.entries)}")

    print("\n持久化示例:")
    tmp_path = Path(__file__).resolve().parent.parent / "data" / "longhun_tags_state.json"
    ts.save(str(tmp_path))
    print(f"  系统状态已保存到: {tmp_path}")

    print("\nEmoji 解析:")
    for e in ["🔥", "✅", "🚨"]:
        r = ts.resolve_emoji(e)
        print(f"  {e} -> {r['龍魂标签'] if r else 'None'} ({r['desc'] if r and 'desc' in r else r.get('modern', '') if r else ''})")

    print("\n组合验证:")
    ok, msg = ts.validate_combo("火", "金")
    print(f"  火+金: {'OK' if ok else 'NG'} {msg}")
    ok2, msg2 = ts.validate_combo("木", "火")
    print(f"  木+火: {'OK' if ok2 else 'NG'} {msg2}")


if __name__ == "__main__":
    main()
