#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂文化标签体系 v1.0 | LongHun Tag System v1.0
UID: 9622
DNA: #龍芯⚡️2026-07-01-LONGHUN-TAG-SYSTEM-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

功能: 中国传统文化标签系统，替代西方emoji
支持: 五行、八卦、甲骨文、二十八星宿
作者: 龍魂系统(UID9622)
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ==================== 1. 五行标签体系 ====================
五行标签 = {
    "金": {
        "unicode": "\u91d1",
        "color": "#FFFFFF", "bg_color": "#F5F5DC",
        "states": {
            "生": {"symbol": "\u91d1\U0001f331", "desc": "金生·萌发", "hex": "#F0F8FF",
                   "usage": "新功能开发、资源初始化", "code": "METAL_BIRTH"},
            "旺": {"symbol": "\u91d1\U0001f525", "desc": "金旺·鼎盛", "hex": "#FFD700",
                   "usage": "性能峰值、满载运行", "code": "METAL_PEAK"},
            "休": {"symbol": "\u91d1\U0001f4a4", "desc": "金休·收敛", "hex": "#C0C0C0",
                   "usage": "资源回收、低功耗模式", "code": "METAL_REST"},
            "囚": {"symbol": "\u91d1\u26d4", "desc": "金囚·受限", "hex": "#808080",
                   "usage": "权限不足、资源锁定", "code": "METAL_TRAP"},
        }
    },
    "木": {
        "unicode": "\u6728",
        "color": "#228B22", "bg_color": "#E8F5E9",
        "states": {
            "生": {"symbol": "\u6728\U0001f331", "desc": "木生·萌芽", "hex": "#90EE90",
                   "usage": "项目立项、架构设计", "code": "WOOD_BIRTH"},
            "旺": {"symbol": "\u6728\U0001f333", "desc": "木旺·繁茂", "hex": "#006400",
                   "usage": "功能完备、生态繁荣", "code": "WOOD_PEAK"},
            "休": {"symbol": "\u6728\U0001f342", "desc": "木休·落叶", "hex": "#8FBC8F",
                   "usage": "版本归档、迭代暂停", "code": "WOOD_REST"},
            "囚": {"symbol": "\u6728\U0001f418", "desc": "木囚·受压", "hex": "#556B2F",
                   "usage": "技术债务、依赖阻塞", "code": "WOOD_TRAP"},
        }
    },
    "水": {
        "unicode": "\u6c34",
        "color": "#1E90FF", "bg_color": "#E3F2FD",
        "states": {
            "生": {"symbol": "\u6c34\U0001f4a7", "desc": "水生·滴落", "hex": "#87CEEB",
                   "usage": "数据接入、流程启动", "code": "WATER_BIRTH"},
            "旺": {"symbol": "\u6c34\U0001f30a", "desc": "水旺·奔流", "hex": "#00008B",
                   "usage": "高并发、数据洪流", "code": "WATER_PEAK"},
            "休": {"symbol": "\u6c34\U0001f9dc", "desc": "水休·静潭", "hex": "#4682B4",
                   "usage": "缓存待机、连接池休眠", "code": "WATER_REST"},
            "囚": {"symbol": "\u6c34\U0001f512", "desc": "水囚·冰封", "hex": "#191970",
                   "usage": "安全冻结、访问拒绝", "code": "WATER_TRAP"},
        }
    },
    "火": {
        "unicode": "\u706b",
        "color": "#DC143C", "bg_color": "#FFEBEE",
        "states": {
            "生": {"symbol": "\u706b\U0001f525", "desc": "火生·点燃", "hex": "#FF6347",
                   "usage": "UI渲染、告警触发", "code": "FIRE_BIRTH"},
            "旺": {"symbol": "\u706b\U0001f480", "desc": "火旺·炽烈", "hex": "#8B0000",
                   "usage": "系统过载、紧急告警", "code": "FIRE_PEAK"},
            "休": {"symbol": "\u706b\u2668", "desc": "火休·余温", "hex": "#CD5C5C",
                   "usage": "降级运行、维护模式", "code": "FIRE_REST"},
            "囚": {"symbol": "\u706b\U0001f6a8", "desc": "火囚·熄灭", "hex": "#800000",
                   "usage": "服务宕机、系统崩溃", "code": "FIRE_TRAP"},
        }
    },
    "土": {
        "unicode": "\u571f",
        "color": "#8B4513", "bg_color": "#F5F5DC",
        "states": {
            "生": {"symbol": "\u571f\U0001f331", "desc": "土生·播种", "hex": "#D2B48C",
                   "usage": "基础设施部署", "code": "EARTH_BIRTH"},
            "旺": {"symbol": "\u571f\U0001f3d4", "desc": "土旺·稳重", "hex": "#8B4513",
                   "usage": "核心系统稳定运行", "code": "EARTH_PEAK"},
            "休": {"symbol": "\u571f\U0001f5fb", "desc": "土休·沉淀", "hex": "#A0522D",
                   "usage": "数据归档、日志沉淀", "code": "EARTH_REST"},
            "囚": {"symbol": "\u571f\u26f0", "desc": "土囚·塌陷", "hex": "#654321",
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
        "unicode_char": "\u4e7e", "unicode_trigram": "\u2630",
        "element": "\u91d1", "direction": "\u897f\u5317", "modern_map": "\u7cfb\u7edf/\u5929",
        "color": "#FFD700",
        "variants": {
            "正": {"label": "\u4e7e·\u6b63\u4f4d", "usage": "\u7cfb\u7edf\u6b63\u5e38\u8fd0\u884c\u3001\u5929\u7ea7\u670d\u52a1", "state": "stable"},
            "反": {"label": "\u4e7e·\u53cd\u8f6c", "usage": "\u7cfb\u7edf\u964d\u7ea7\u3001\u5929\u5730\u4ea4\u6cf0", "state": "degraded"},
            "动": {"label": "\u4e7e·\u52a8\u59fb", "usage": "\u7cfb\u7edf\u544a\u8b66\u3001\u5929\u53d8\u9884\u8b66", "state": "alert"},
        }
    },
    "坤": {
        "unicode_char": "\u5764", "unicode_trigram": "\u2637",
        "element": "\u571f", "direction": "\u897f\u5357", "modern_map": "\u6570\u636e/\u5730",
        "color": "#8B4513",
        "variants": {
            "正": {"label": "\u5764·\u6b63\u4f4d", "usage": "\u6570\u636e\u5e93\u6b63\u5e38\u3001\u5730\u7a33\u5b58\u50a8", "state": "stable"},
            "反": {"label": "\u5764·\u53cd\u8f6c", "usage": "\u6570\u636e\u8fc1\u79fb\u3001\u5929\u5730\u5012\u60ac", "state": "migrating"},
            "动": {"label": "\u5764·\u52a8\u59fb", "usage": "\u6570\u636e\u540c\u6b65\u3001\u5730\u8d28\u53d8\u52a8", "state": "syncing"},
        }
    },
    "震": {
        "unicode_char": "\u9707", "unicode_trigram": "\u2633",
        "element": "\u6728", "direction": "\u4e1c", "modern_map": "\u542f\u52a8/\u96f7",
        "color": "#228B22",
        "variants": {
            "正": {"label": "\u9707·\u6b63\u4f4d", "usage": "\u670d\u52a1\u542f\u52a8\u3001\u96f7\u9e23\u89e6\u53d1", "state": "starting"},
            "反": {"label": "\u9707·\u53cd\u8f6c", "usage": "\u542f\u52a8\u5931\u8d25\u3001\u96f7\u98ce\u76f8\u8584", "state": "failed"},
            "动": {"label": "\u9707·\u52a8\u59fb", "usage": "\u7d27\u6025\u542f\u52a8\u3001\u96f7\u9706\u4e07\u9497", "state": "urgent"},
        }
    },
    "巽": {
        "unicode_char": "\u5dfd", "unicode_trigram": "\u2634",
        "element": "\u6728", "direction": "\u4e1c\u5357", "modern_map": "\u4f20\u64ad/\u98ce",
        "color": "#32CD32",
        "variants": {
            "正": {"label": "\u5dfd·\u6b63\u4f4d", "usage": "\u6d88\u606f\u5206\u53d1\u3001\u98ce\u884c\u5929\u4e0b", "state": "distributing"},
            "反": {"label": "\u5dfd·\u53cd\u8f6c", "usage": "\u4f20\u64ad\u963b\u585e\u3001\u98ce\u96f7\u4e71\u5e8f", "state": "blocked"},
            "动": {"label": "\u5dfd·\u52a8\u59fb", "usage": "\u5e7f\u64ad\u98ce\u66b4\u3001\u98d3\u98ce\u4f20\u64ad", "state": "storm"},
        }
    },
    "坎": {
        "unicode_char": "\u574e", "unicode_trigram": "\u2635",
        "element": "\u6c34", "direction": "\u5317", "modern_map": "\u5b89\u5168/\u6c34",
        "color": "#1E90FF",
        "variants": {
            "正": {"label": "\u574e·\u6b63\u4f4d", "usage": "\u5b89\u5168\u9632\u62a4\u3001\u6c34\u6da6\u65e0\u58f0", "state": "protected"},
            "反": {"label": "\u574e·\u53cd\u8f6c", "usage": "\u5b89\u5168\u7a81\u7834\u3001\u6c34\u706b\u4e0d\u5bb9", "state": "breached"},
            "动": {"label": "\u574e·\u52a8\u59fb", "usage": "\u6d2a\u6c34\u653b\u51fb\u3001\u5b89\u5168\u544a\u8b66", "state": "attacked"},
        }
    },
    "离": {
        "unicode_char": "\u79bb", "unicode_trigram": "\u2632",
        "element": "\u706b", "direction": "\u5357", "modern_map": "\u663e\u793a/\u706b",
        "color": "#DC143C",
        "variants": {
            "正": {"label": "\u79bb·\u6b63\u4f4d", "usage": "UI\u6b63\u5e38\u3001\u5149\u660e\u666e\u7167", "state": "display_ok"},
            "反": {"label": "\u79bb·\u53cd\u8f6c", "usage": "\u663e\u793a\u5f02\u5e38\u3001\u706b\u6c34\u672a\u6d4e", "state": "display_error"},
            "动": {"label": "\u79bb·\u52a8\u59fb", "usage": "\u6e32\u67d3\u8fc7\u8f7d\u3001\u70c8\u706b\u711a\u539f", "state": "render_overload"},
        }
    },
    "艮": {
        "unicode_char": "\u826e", "unicode_trigram": "\u2636",
        "element": "\u571f", "direction": "\u4e1c\u5317", "modern_map": "\u505c\u6b62/\u5c71",
        "color": "#696969",
        "variants": {
            "正": {"label": "\u826e·\u6b63\u4f4d", "usage": "\u670d\u52a1\u505c\u6b62\u3001\u5c71\u6b62\u884c\u6b62", "state": "stopped"},
            "反": {"label": "\u826e·\u53cd\u8f6c", "usage": "\u5f3a\u5236\u5173\u95ed\u5d29\u89e3\u3001\u5c71\u6cfd\u901a\u6c14", "state": "crashed"},
            "动": {"label": "\u826e·\u52a8\u59fb", "usage": "\u4f18\u96c5\u5173\u95ed\u3001\u5c71\u8109\u5d29\u584c", "state": "shutting_down"},
        }
    },
    "兑": {
        "unicode_char": "\u5151", "unicode_trigram": "\u2631",
        "element": "\u91d1", "direction": "\u897f", "modern_map": "\u4ea4\u6d41/\u6cfd",
        "color": "#FFD700",
        "variants": {
            "正": {"label": "\u5151·\u6b63\u4f4d", "usage": "API\u6b63\u5e38\u3001\u6cfd\u6da6\u4e07\u7269", "state": "connected"},
            "反": {"label": "\u5151·\u53cd\u8f6c", "usage": "\u901a\u4fe1\u4e2d\u65ad\u3001\u6cfd\u5c71\u54b8\u963b", "state": "disconnected"},
            "动": {"label": "\u5151·\u52a8\u59fb", "usage": "\u9ad8\u9891\u901a\u4fe1\u3001\u6cfd\u6d8c\u6d2a\u6ce2", "state": "high_freq"},
        }
    },
}

# ==================== 3. 甲骨文标签体系 ====================
甲骨文标签 = {
    "启": {"unicode": "\u542f", "category": "状态", "pinyin": "qi",
        "modern": "开始/启动", "usage": "项目启动、功能开启", "color": "#00C853", "tag": "START"},
    "止": {"unicode": "\u6b62", "category": "状态", "pinyin": "zhi",
        "modern": "停止/终止", "usage": "进程停止、服务终止", "color": "#FF1744", "tag": "STOP"},
    "行": {"unicode": "\u884c", "category": "状态", "pinyin": "xing",
        "modern": "运行/执行", "usage": "任务运行、进行中", "color": "#2979FF", "tag": "RUN"},
    "立": {"unicode": "\u7acb", "category": "状态", "pinyin": "li",
        "modern": "建立/就绪", "usage": "实例就绪、资源就位", "color": "#651FFF", "tag": "READY"},
    "生": {"unicode": "\u751f", "category": "状态", "pinyin": "sheng",
        "modern": "生成/创建", "usage": "资源创建、实例生成", "color": "#00E676", "tag": "CREATE"},
    "死": {"unicode": "\u6b7b", "category": "状态", "pinyin": "si",
        "modern": "销毁/死亡", "usage": "实例销毁、资源释放", "color": "#424242", "tag": "DESTROY"},
    "变": {"unicode": "\u53d8", "category": "状态", "pinyin": "bian",
        "modern": "变更/转换", "usage": "状态变更、配置更新", "color": "#FF9100", "tag": "CHANGE"},
    "等": {"unicode": "\u7b49", "category": "状态", "pinyin": "deng",
        "modern": "等待/队列", "usage": "任务排队、等待资源", "color": "#78909C", "tag": "WAIT"},
    "成": {"unicode": "\u6210", "category": "状态", "pinyin": "cheng",
        "modern": "成功/完成", "usage": "操作成功、任务完成", "color": "#00C853", "tag": "SUCCESS"},
    "败": {"unicode": "\u8d25", "category": "状态", "pinyin": "bai",
        "modern": "失败/错误", "usage": "操作失败、异常捕获", "color": "#D50000", "tag": "FAIL"},

    "喜": {"unicode": "\u559c", "category": "情绪", "pinyin": "xi",
        "modern": "喜悦/好评", "usage": "用户满意、正向反馈", "color": "#FFEA00", "tag": "JOY"},
    "怒": {"unicode": "\u6012", "category": "情绪", "pinyin": "nu",
        "modern": "愤怒/告警", "usage": "严重告警、用户投诉", "color": "#DD2C00", "tag": "ANGER"},
    "哀": {"unicode": "\u54c0", "category": "情绪", "pinyin": "ai",
        "modern": "哀伤/降级", "usage": "服务降级、功能下线", "color": "#546E7A", "tag": "SORROW"},
    "乐": {"unicode": "\u4e50", "category": "情绪", "pinyin": "le",
        "modern": "快乐/庆祝", "usage": "里程碑达成、发布庆祝", "color": "#FFD600", "tag": "CELEBRATE"},
    "恐": {"unicode": "\u6050", "category": "情绪", "pinyin": "kong",
        "modern": "恐惧/危险", "usage": "安全威胁、高危漏洞", "color": "#4A148C", "tag": "FEAR"},
    "惊": {"unicode": "\u60ca", "category": "情绪", "pinyin": "jing",
        "modern": "惊讶/异常", "usage": "意外异常、罕见错误", "color": "#FF6D00", "tag": "SURPRISE"},
    "爱": {"unicode": "\u7231", "category": "情绪", "pinyin": "ai2",
        "modern": "喜爱/推荐", "usage": "用户喜爱、推荐系统", "color": "#FF4081", "tag": "LOVE"},
    "恶": {"unicode": "\u6076", "category": "情绪", "pinyin": "wu",
        "modern": "厌恶/屏蔽", "usage": "内容过滤、黑名单", "color": "#212121", "tag": "BLOCK"},
    "疑": {"unicode": "\u7591", "category": "情绪", "pinyin": "yi",
        "modern": "怀疑/待审", "usage": "待审核、可疑行为", "color": "#827717", "tag": "SUSPECT"},
    "信": {"unicode": "\u4fe1", "category": "情绪", "pinyin": "xin",
        "modern": "信任/认证", "usage": "身份认证、信任链", "color": "#0091EA", "tag": "TRUST"},

    "见": {"unicode": "\u89c1", "category": "功能", "pinyin": "jian",
        "modern": "查看/读取", "usage": "数据查询、日志查看", "color": "#00B0FF", "tag": "READ"},
    "闻": {"unicode": "\u95fb", "category": "功能", "pinyin": "wen",
        "modern": "监听/通知", "usage": "事件监听、消息通知", "color": "#76FF03", "tag": "LISTEN"},
    "言": {"unicode": "\u8a00", "category": "功能", "pinyin": "yan",
        "modern": "写入/发言", "usage": "数据写入、用户评论", "color": "#FF3D00", "tag": "WRITE"},
    "思": {"unicode": "\u601d", "category": "功能", "pinyin": "si",
        "modern": "分析/计算", "usage": "数据分析、算法运算", "color": "#651FFF", "tag": "ANALYZE"},
    "守": {"unicode": "\u5b88", "category": "功能", "pinyin": "shou",
        "modern": "守护/监控", "usage": "系统监控、守护进程", "color": "#1DE9B6", "tag": "MONITOR"},
    "攻": {"unicode": "\u653b", "category": "功能", "pinyin": "gong",
        "modern": "攻击/测试", "usage": "渗透测试、压力测试", "color": "#C62828", "tag": "PENTEST"},
    "取": {"unicode": "\u53d6", "category": "功能", "pinyin": "qu",
        "modern": "获取/拉取", "usage": "数据拉取、资源获取", "color": "#2962FF", "tag": "FETCH"},
    "与": {"unicode": "\u4e0e", "category": "功能", "pinyin": "yu",
        "modern": "给予/推送", "usage": "数据推送、消息发送", "color": "#AA00FF", "tag": "PUSH"},
    "分": {"unicode": "\u5206", "category": "功能", "pinyin": "fen",
        "modern": "分割/分区", "usage": "数据分片、服务分区", "color": "#0097A7", "tag": "PARTITION"},
    "合": {"unicode": "\u5408", "category": "功能", "pinyin": "he",
        "modern": "合并/聚合", "usage": "数据聚合、服务合并", "color": "#43A047", "tag": "MERGE"},

    "上": {"unicode": "\u4e0a", "category": "等级", "pinyin": "shang",
        "modern": "高级/P0", "usage": "最高优先级、核心服务", "color": "#D50000", "tag": "P0"},
    "中": {"unicode": "\u4e2d", "category": "等级", "pinyin": "zhong",
        "modern": "中级/P1", "usage": "普通优先级、一般任务", "color": "#FF6D00", "tag": "P1"},
    "下": {"unicode": "\u4e0b", "category": "等级", "pinyin": "xia",
        "modern": "低级/P2", "usage": "低优先级、后台任务", "color": "#64DD17", "tag": "P2"},
    "大": {"unicode": "\u5927", "category": "等级", "pinyin": "da",
        "modern": "大规模/L", "usage": "大数据量、大规模集群", "color": "#B71C1C", "tag": "LARGE"},
    "小": {"unicode": "\u5c0f", "category": "等级", "pinyin": "xiao",
        "modern": "小规模/S", "usage": "轻量服务、小规模部署", "color": "#81C784", "tag": "SMALL"},
    "初": {"unicode": "\u521d", "category": "等级", "pinyin": "chu",
        "modern": "初级/L1", "usage": "初级问题、入门级", "color": "#69F0AE", "tag": "L1"},
    "高": {"unicode": "\u9ad8", "category": "等级", "pinyin": "gao",
        "modern": "高级/L3", "usage": "高级工程师、高难度", "color": "#E53935", "tag": "L3"},
    "低": {"unicode": "\u4f4e", "category": "等级", "pinyin": "di",
        "modern": "低级/L0", "usage": "基础服务、低配置", "color": "#A5D6A7", "tag": "L0"},
    "王": {"unicode": "\u738b", "category": "等级", "pinyin": "wang",
        "modern": "王者/核心", "usage": "核心模块、主服务", "color": "#FFD700", "tag": "CORE"},
    "民": {"unicode": "\u6c11", "category": "等级", "pinyin": "min",
        "modern": "普通/边缘", "usage": "边缘服务、普通节点", "color": "#9E9E9E", "tag": "EDGE"},
}

# ==================== 4. 二十八星宿标签体系 ====================
星宿标签 = {
    "角": {"unicode": "\u89d2", "beast": "\u9752\u9f99", "beast_code": "dragon",
        "position": 1, "modern": "初始化/入口", "color": "#4CAF50", "tag": "INIT",
        "usage": "系统初始化、项目入口"},
    "亢": {"unicode": "\u4ea2", "beast": "\u9752\u9f99", "beast_code": "dragon",
        "position": 2, "modern": "防御/守护", "color": "#43A047", "tag": "DEFENSE",
        "usage": "安全防护、访问控制"},
    "氐": {"unicode": "\u6c10", "beast": "\u9752\u9f99", "beast_code": "dragon",
        "position": 3, "modern": "根基/基础", "color": "#388E3C", "tag": "FOUNDATION",
        "usage": "基础设施、核心依赖"},
    "房": {"unicode": "\u623f", "beast": "\u9752\u9f99", "beast_code": "dragon",
        "position": 4, "modern": "存储/仓库", "color": "#2E7D32", "tag": "STORAGE",
        "usage": "数据仓库、存储服务"},
    "心": {"unicode": "\u5fc3", "beast": "\u9752\u9f99", "beast_code": "dragon",
        "position": 5, "modern": "核心/引擎", "color": "#1B5E20", "tag": "ENGINE",
        "usage": "核心引擎、主服务"},
    "尾": {"unicode": "\u5c3e", "beast": "\u9752\u9f99", "beast_code": "dragon",
        "position": 6, "modern": "日志/追踪", "color": "#66BB6A", "tag": "TRACE",
        "usage": "日志系统、调用链追踪"},
    "箕": {"unicode": "\u7b95", "beast": "\u9752\u9f99", "beast_code": "dragon",
        "position": 7, "modern": "收集/汇聚", "color": "#81C784", "tag": "COLLECT",
        "usage": "数据收集、日志汇聚"},

    "斗": {"unicode": "\u6597", "beast": "\u7384\u6b66", "beast_code": "tortoise",
        "position": 8, "modern": "调度/编排", "color": "#1976D2", "tag": "SCHEDULER",
        "usage": "任务调度、容器编排"},
    "牛": {"unicode": "\u725b", "beast": "\u7384\u6b66", "beast_code": "tortoise",
        "position": 9, "modern": "负载/计算", "color": "#1565C0", "tag": "COMPUTE",
        "usage": "计算节点、负载均衡"},
    "女": {"unicode": "\u5973", "beast": "\u7384\u6b66", "beast_code": "tortoise",
        "position": 10, "modern": "编织/关联", "color": "#0D47A1", "tag": "RELATE",
        "usage": "数据编织、关联分析"},
    "虚": {"unicode": "\u865a", "beast": "\u7384\u6b66", "beast_code": "tortoise",
        "position": 11, "modern": "虚拟/抽象", "color": "#42A5F5", "tag": "VIRTUAL",
        "usage": "虚拟化、抽象层"},
    "危": {"unicode": "\u5371", "beast": "\u7384\u6b66", "beast_code": "tortoise",
        "position": 12, "modern": "风险/预警", "color": "#EF5350", "tag": "RISK",
        "usage": "风险预警、危机处理"},
    "室": {"unicode": "\u5ba4", "beast": "\u7384\u6b66", "beast_code": "tortoise",
        "position": 13, "modern": "空间/环境", "color": "#1E88E5", "tag": "ENV",
        "usage": "运行环境、命名空间"},
    "壁": {"unicode": "\u58c1", "beast": "\u7384\u6b66", "beast_code": "tortoise",
        "position": 14, "modern": "边界/防火墙", "color": "#2196F3", "tag": "BOUNDARY",
        "usage": "网络边界、防火墙"},

    "奎": {"unicode": "\u594e", "beast": "\u767d\u864e", "beast_code": "tiger",
        "position": 15, "modern": "缓存/加速", "color": "#E0E0E0", "tag": "CACHE",
        "usage": "缓存层、CDN加速"},
    "娄": {"unicode": "\u5a04", "beast": "\u767d\u864e", "beast_code": "tiger",
        "position": 16, "modern": "聚合/汇总", "color": "#BDBDBD", "tag": "AGGREGATE",
        "usage": "数据聚合、报表汇总"},
    "胃": {"unicode": "\u80c3", "beast": "\u767d\u864e", "beast_code": "tiger",
        "position": 17, "modern": "消化/处理", "color": "#9E9E9E", "tag": "PROCESS",
        "usage": "数据处理、ETL管道"},
    "昴": {"unicode": "\u6634", "beast": "\u767d\u864e", "beast_code": "tiger",
        "position": 18, "modern": "星群/集群", "color": "#757575", "tag": "CLUSTER",
        "usage": "服务集群、星型拓扑"},
    "毕": {"unicode": "\u6bd5", "beast": "\u767d\u864e", "beast_code": "tiger",
        "position": 19, "modern": "完成/终结", "color": "#616161", "tag": "COMPLETE",
        "usage": "任务完成、流水线结束"},
    "觜": {"unicode": "\u89dc", "beast": "\u767d\u864e", "beast_code": "tiger",
        "position": 20, "modern": "精细/优化", "color": "#F5F5F5", "tag": "OPTIMIZE",
        "usage": "性能优化、精细调参"},
    "参": {"unicode": "\u53c2", "beast": "\u767d\u864e", "beast_code": "tiger",
        "position": 21, "modern": "参考/基准", "color": "#424242", "tag": "BENCHMARK",
        "usage": "基准测试、参考实现"},

    "井": {"unicode": "\u4e95", "beast": "\u6731\u96c0", "beast_code": "phoenix",
        "position": 22, "modern": "源头/输入", "color": "#FF5722", "tag": "SOURCE",
        "usage": "数据源、消息入口"},
    "鬼": {"unicode": "\u9b3c", "beast": "\u6731\u96c0", "beast_code": "phoenix",
        "position": 23, "modern": "隐藏/秘钥", "color": "#E64A19", "tag": "SECRET",
        "usage": "密钥管理、隐藏配置"},
    "柳": {"unicode": "\u67f3", "beast": "\u6731\u96c0", "beast_code": "phoenix",
        "position": 24, "modern": "灵活/弹性", "color": "#D84315", "tag": "FLEX",
        "usage": "弹性伸缩、柔性架构"},
    "星": {"unicode": "\u661f", "beast": "\u6731\u96c0", "beast_code": "phoenix",
        "position": 25, "modern": "标记/亮点", "color": "#FF8A65", "tag": "FEATURE",
        "usage": "功能亮点、星标项目"},
    "张": {"unicode": "\u5f20", "beast": "\u6731\u96c0", "beast_code": "phoenix",
        "position": 26, "modern": "展开/扩张", "color": "#FF7043", "tag": "EXPAND",
        "usage": "业务扩张、规模增长"},
    "翼": {"unicode": "\u7ffc", "beast": "\u6731\u96c0", "beast_code": "phoenix",
        "position": 27, "modern": "辅助/增强", "color": "#FFAB91", "tag": "AUGMENT",
        "usage": "辅助服务、增强功能"},
    "轸": {"unicode": "\u8f78", "beast": "\u6731\u96c0", "beast_code": "phoenix",
        "position": 28, "modern": "循环/反馈", "color": "#BF360C", "tag": "FEEDBACK",
        "usage": "反馈循环、迭代优化"},
}


# ═══════════════════════════════════════════════════════════════
# LongHunTagSystem 类封装
# ═══════════════════════════════════════════════════════════════

class LongHunTagSystem:
    """
    龍魂标签系统封装类
    提供五行、八卦、甲骨文、二十八星宿的统一查询与渲染
    """

    DNA = "#龍芯⚡️2026-07-01-LONGHUN-TAG-SYSTEM-v1.0"

    def __init__(self):
        self.五行 = 五行标签
        self.八卦 = 八卦标签
        self.甲骨文 = 甲骨文标签
        self.星宿 = 星宿标签
        self.生克 = 五行生克

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
                    return {"type": "五行", "element": elem, "state": state, **sdata}

        # 2. 八卦
        for gua, data in self.八卦.items():
            for var, vdata in data["variants"].items():
                if code == vdata["label"] or code == f"{gua}·{var}":
                    return {"type": "八卦", "gua": gua, "variant": var, "color": data["color"], **vdata}

        # 3. 甲骨文
        if code in self.甲骨文:
            return {"type": "甲骨文", "char": code, **self.甲骨文[code]}

        # 4. 星宿
        if code in self.星宿:
            return {"type": "星宿", "star": code, **self.星宿[code]}

        return None

    def get_wuxing_tags(self) -> List[Dict]:
        """返回全部五行标签列表"""
        result = []
        for elem, data in self.五行.items():
            for state, sdata in data["states"].items():
                result.append({"type": "五行", "element": elem, "state": state, **sdata})
        return result

    def get_bagua_tags(self) -> List[Dict]:
        """返回全部八卦标签列表"""
        result = []
        for gua, data in self.八卦.items():
            for var, vdata in data["variants"].items():
                result.append({"type": "八卦", "gua": gua, "variant": var, "color": data["color"], **vdata})
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
            return f"\033[38;2:{rgb[0]};{rgb[1]};{rgb[2]}m{text}\033[0m"
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

    def metadata(self) -> Dict:
        """返回系统元数据"""
        return {
            "system": "龍魂文化标签体系",
            "version": "v1.0",
            "uid": "9622",
            "dna": self.DNA,
            "counts": {
                "五行标签": len(self.五行) * 4,
                "八卦标签": len(self.八卦) * 3,
                "甲骨文标签": len(self.甲骨文),
                "星宿标签": len(self.星宿),
            },
            "total_tags": len(self.五行) * 4 + len(self.八卦) * 3 + len(self.甲骨文) + len(self.星宿),
        }


# 保持向后兼容的模块级函数
LongHunTag = LongHunTagSystem


def main():
    print("=" * 50)
    print("龍魂文化标签体系 v1.0")
    print(f"UID: 9622 | DNA: {LongHunTagSystem.DNA}")
    print("=" * 50)

    ts = LongHunTagSystem()
    meta = ts.metadata()
    print("\n标签统计:")
    for k, v in meta["counts"].items():
        print(f"  {k}: {v}")
    print(f"  总计: {meta['total_tags']}")

    print("\n查询示例:")
    print(f"  get_tag('METAL_PEAK'): {ts.get_tag('METAL_PEAK')['desc']}")
    print(f"  get_tag('启')['modern']: {ts.get_tag('启')['modern']}")

    print("\n渲染示例:")
    print(f"  text: {ts.render_tag('火·旺', 'text')}")
    print(f"  html: {ts.render_tag('火·旺', 'html')}")
    print(f"  md:   {ts.render_tag('成', 'md')}")

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
