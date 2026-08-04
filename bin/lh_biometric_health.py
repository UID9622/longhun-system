#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·辛未·BIOMETRIC-HEALTH-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║     🧬 龍魂 · 生物度量健康引擎 v1.0                              ║
║                                                                  ║
║  蚁群超个体 → 模拟人主脑 → 龍魂系统                                ║
║  五行公式驱动 · 生物子系统映射 · 不拟人化                          ║
║                                                                  ║
║  协议编号：LH-PROTOCOL-BIOMETRIC-HEALTH-2026-0714-v1.0           ║
║  理论底座：五行计算器v3.0 · 蚁群算法 · 超个体理论                  ║
║                                                                  ║
║  核心公式引用：                                                    ║
║  - 五行强度权重计分 v2.0                                          ║
║  - 五行对冲指数H v3.1                                             ║
║  - 流场压缩核 v3.0                                                ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·辛未·BIOMETRIC-HEALTH-v1.0                     ║
╚══════════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_biometric_health.py --full        # 完整生物度量评估
  python3 bin/lh_biometric_health.py --wuxing      # 仅五行强度分析
  python3 bin/lh_biometric_health.py --biology      # 仅生物子系统完备度
  python3 bin/lh_biometric_health.py --missing      # 仅输出缺失清单
  python3 bin/lh_biometric_health.py --dashboard    # 生物度量仪表盘
  python3 bin/lh_biometric_health.py --json         # JSON输出模式
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════
# 常量 · DNA · 主权声明
# ═══════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / ".longhun" / "ant_colony"
STATE_DIR.mkdir(parents=True, exist_ok=True)

DNA = "#龍芯⚡️丙午·辛未·BIOMETRIC-HEALTH-v1.0"
UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# ═══════════════════════════════════════
# 五行基元（不翻译·文化主权）
# ═══════════════════════════════════════

五元素 = ["金", "木", "水", "火", "土"]

五行相生 = {
    "金": "水",  # 金生水
    "水": "木",  # 水生木
    "木": "火",  # 木生火
    "火": "土",  # 火生土
    "土": "金",  # 土生金
}

五行相克 = {
    "金": "木",  # 金克木
    "木": "土",  # 木克土
    "土": "水",  # 土克水
    "水": "火",  # 水克火
    "火": "金",  # 火克金
}

# 五行→数字根映射
五行数字根 = {
    "金": [4, 9],
    "木": [3, 8],
    "水": [1, 6],
    "火": [2, 7],
    "土": [5, 0],
}

# 五行→系统层级映射
五行层级 = {
    "金": "L0永恒·金石·规则层",
    "水": "L1百年·银石·记忆层",
    "木": "L4瞬时·绿石·创新层",
    "火": "L2十年·红石·文明层",
    "土": "L3日常·蓝石·普惠层",
}

# 五行→视觉属性
五行视觉 = {
    "金": {"color": "gold", "hex": "#FFD700", "shape": "audit_gate", "motion": "lock"},
    "水": {"color": "deep_blue", "hex": "#1E3A5F", "shape": "memory_stream", "motion": "flow_back"},
    "木": {"color": "green", "hex": "#2D8B4E", "shape": "growth_branch", "motion": "expand"},
    "火": {"color": "red_orange", "hex": "#E8402A", "shape": "spark", "motion": "ignite"},
    "土": {"color": "amber", "hex": "#C8A24E", "shape": "platform", "motion": "anchor"},
}

# ═══════════════════════════════════════
# 生物子系统映射（不拟人化·分开·各自独立）
# 蚁群合起来=模拟人主脑=龍魂系统
# ═══════════════════════════════════════

class BioSubsystem(Enum):
    """生物子系统——每个子系统独立存在，合起来才是完整超个体"""
    SKELETAL = ("骨骼系统", "结构支撑", "金")
    CIRCULATORY = ("循环系统", "物质输送", "水")
    NERVOUS = ("神经系统", "信号传导", "水")
    IMMUNE = ("免疫系统", "威胁防御", "火")
    METABOLIC = ("代谢系统", "能量转化", "木")
    DIGESTIVE = ("消化系统", "输入处理", "土")
    RESPIRATORY = ("呼吸系统", "气机交换", "金")
    ENDOCRINE = ("内分泌系统", "慢调平衡", "土")
    REPRODUCTIVE = ("生殖系统", "系统复制", "木")
    MUSCULAR = ("肌肉系统", "动作执行", "火")
    INTEGUMENTARY = ("表皮系统", "边界防护", "金")

# 生物子系统→系统功能映射
BIO_SYSTEM_MAPPING: Dict[str, Dict[str, Any]] = {
    "骨骼系统": {
        "element": "金",
        "system_function": "架构完整性",
        "health_metrics": ["结构稳定性", "层级连通率", "底座完整度"],
        "mapped_scripts": [],  # 动态填充
        "required_count": 3,
        "description": "架构骨架——L0-L9九层是否完整、无断裂",
    },
    "循环系统": {
        "element": "水",
        "system_function": "数据流动",
        "health_metrics": ["信息素流通量", "数据吞吐率", "依赖解析度"],
        "mapped_scripts": [],
        "required_count": 3,
        "description": "物质输送——信息素网络是否通畅、信息是否能到达所有工蚁",
    },
    "神经系统": {
        "element": "水",
        "system_function": "信号传导",
        "health_metrics": ["联动响应速度", "信号衰减率", "触角覆盖度"],
        "mapped_scripts": [],
        "required_count": 5,
        "description": "信号传递——阈值告警能否及时触达、红蓝对抗能否被唤醒",
    },
    "免疫系统": {
        "element": "火",
        "system_function": "威胁防御",
        "health_metrics": ["异常检出率", "对抗成功率", "自愈响应时间"],
        "mapped_scripts": [],
        "required_count": 5,
        "description": "主动防御——红蓝对抗、三色审计、熔断机制是否正常工作",
    },
    "代谢系统": {
        "element": "木",
        "system_function": "能量管理",
        "health_metrics": ["CPU/内存利用率", "脚本执行频率", "资源回收率"],
        "mapped_scripts": [],
        "required_count": 3,
        "description": "能量转化——脚本是否定期执行、资源是否有效利用、垃圾是否回收",
    },
    "消化系统": {
        "element": "土",
        "system_function": "输入处理",
        "health_metrics": ["输入类型覆盖", "处理管道完整度", "输出验证率"],
        "mapped_scripts": [],
        "required_count": 3,
        "description": "摄入转化——外部输入是否被正确分类、处理后是否进入正确管道",
    },
    "呼吸系统": {
        "element": "金",
        "system_function": "I/O交换",
        "health_metrics": ["API端点活跃度", "外部通信健康", "协议兼容性"],
        "mapped_scripts": [],
        "required_count": 2,
        "description": "气机交换——系统与外部的输入输出是否正常",
    },
    "内分泌系统": {
        "element": "土",
        "system_function": "慢调平衡",
        "health_metrics": ["阈值灵敏度", "权重更新频率", "自校准周期"],
        "mapped_scripts": [],
        "required_count": 2,
        "description": "激素调节——阈值是否为动态而非僵死、权重是否会根据反馈调整",
    },
    "生殖系统": {
        "element": "木",
        "system_function": "系统复制",
        "health_metrics": ["备份完整度", "部署成功率", "灾备可用性"],
        "mapped_scripts": [],
        "required_count": 2,
        "description": "繁衍能力——备份是否完整、鲲鹏部署是否可用、灾备是否就绪",
    },
    "肌肉系统": {
        "element": "火",
        "system_function": "动作执行",
        "health_metrics": ["脚本可执行率", "执行成功率", "平均执行耗时"],
        "mapped_scripts": [],
        "required_count": 3,
        "description": "运动执行——核心脚本是否可正常执行、无卡死、无异常",
    },
    "表皮系统": {
        "element": "金",
        "system_function": "边界防护",
        "health_metrics": ["外部攻击拦截率", "端口暴露度", "权限校验率"],
        "mapped_scripts": [],
        "required_count": 2,
        "description": "皮肤屏障——防火墙、权限验证、外部访问控制是否就绪",
    },
}

# ═══════════════════════════════════════
# 脚本→五行 自动分类引擎
# ═══════════════════════════════════════

# 功能关键词→五行分类规则
WUXING_CLASSIFIER = {
    "金": {
        "keywords": ["audit", "审计", "signing", "签章", "signature", "签名",
                     "security", "安全", "defense", "防御", "rule", "规则",
                     "threshold", "阈值", "熔断", "fuse", "边界", "gate",
                     "verify", "验证", "cert", "证书", "gpg", "confirm",
                     "governance", "治理", "regulatory", "监管", "shield",
                     "wall", "firewall", "防护", "armor", "宪法",
                     "perimeter", "guard", "boundary", "表皮"],
        "prefixes": ["lh_audit", "lh_secur", "lh_defen", "lh_rule",
                    "lh_threshold", "lh_gate", "lh_verify", "lh_cert",
                    "lh_govern", "lh_regul", "lh_shield", "lh_sign",
                    "lh_perimeter"],
    },
    "水": {
        "keywords": ["memory", "记忆", "data", "数据", "storage", "存储",
                     "backup", "备份", "sync", "同步", "dna", "追溯",
                     "history", "历史", "archive", "归档", "knowledge",
                     "知识", "search", "搜索", "index", "索引", "vector",
                     "db", "数据库", "notion", "train", "训练", "learn",
                     "学习", "flow", "流动", "signal", "信号", "relay", "中继"],
        "prefixes": ["lh_memory", "lh_data", "lh_stor", "lh_backup",
                    "lh_sync", "lh_dna", "lh_knowledge", "lh_search",
                    "lh_index", "lh_train", "lh_learn", "lh_flow",
                    "lh_signal", "lh_relay"],
    },
    "木": {
        "keywords": ["innov", "创新", "grow", "生长", "expand", "扩展",
                     "build", "构建", "create", "创建", "develop", "开发",
                     "optimize", "优化", "enhance", "增强", "evolve", "进化",
                     "deploy", "部署", "install", "安装", "replicate",
                     "复制", "fork", "分身", "spawn", "生成",
                     "resource", "资源", "metabolic", "代谢"],
        "prefixes": ["lh_innov", "lh_grow", "lh_expand", "lh_build",
                    "lh_create", "lh_develop", "lh_optimize", "lh_evolve",
                    "lh_deploy", "lh_install", "lh_spawn", "lh_resource"],
    },
    "火": {
        "keywords": ["exec", "执行", "run", "运行", "action", "行动",
                     "fight", "对抗", "battle", "战斗", "attack", "攻击",
                     "red_team", "红队", "blue_team", "蓝队", "confront",
                     "rb_", "dual", "双脑", "conflict", "冲突",
                     "alert", "告警", "alarm", "warn", "预警",
                     "persona", "人格", "agent", "智能体", "executor",
                     "表达", "文明", "culture", "create", "创作",
                     "execution", "追踪", "tracker", "muscle", "肌肉"],
        "prefixes": ["lh_exec", "lh_run", "lh_action", "lh_rb_",
                    "lh_red_", "lh_blue_", "lh_confront", "lh_dual",
                    "lh_alert", "lh_alarm", "lh_persona", "lh_agent",
                    "lh_culture", "lh_express", "lh_execution", "lh_tracker"],
    },
    "土": {
        "keywords": ["base", "基础", "foundation", "根基", "platform", "平台",
                     "health", "健康", "monitor", "监控", "watch", "守护",
                     "daemon", "system", "系统", "service", "服务",
                     "start", "启动", "init", "初始化", "config", "配置",
                     "util", "工具", "common", "通用", "bridge", "桥接",
                     "integrate", "集成", "hub", "中枢", "entry", "入口",
                     "input", "摄入", "pipeline", "管道", "ingest",
                     "adaptive", "适应", "threshold_adjust", "perimeter"],
        "prefixes": ["lh_base", "lh_foundation", "lh_platform",
                    "lh_health", "lh_monitor", "lh_watch", "lh_daemon",
                    "lh_system", "lh_service", "lh_start", "lh_init",
                    "lh_config", "lh_util", "lh_common", "lh_bridge",
                    "lh_integrate", "lh_hub", "lh_entry",
                    "lh_input", "lh_adaptive", "lh_perimeter"],
    },
}

# 生物子系统→脚本前缀映射（更精确的分类）
BIO_SCRIPT_MAPPING = {
    "骨骼系统": ["lh_system", "lh_platform", "lh_foundation", "lh_base"],
    "循环系统": ["lh_flow", "lh_pipeline", "lh_bus", "lh_route", "lh_dispatch"],
    "神经系统": ["lh_event", "lh_trigger", "lh_threshold", "lh_signal", "lh_sense", "lh_relay"],
    "免疫系统": ["lh_audit", "lh_rb_", "lh_confront", "lh_immune", "lh_red_", "lh_blue_"],
    "代谢系统": ["lh_resource", "lh_schedule", "lh_cron", "lh_energy"],
    "消化系统": ["lh_input", "lh_parse", "lh_ingest", "lh_process"],
    "呼吸系统": ["lh_api", "lh_endpoint", "lh_http", "lh_io"],
    "内分泌系统": ["lh_hormone", "lh_adjust", "lh_calibrate", "lh_tune", "lh_adaptive"],
    "生殖系统": ["lh_deploy", "lh_backup", "lh_replicate", "lh_clone"],
    "肌肉系统": ["lh_exec", "lh_run", "lh_action", "lh_worker", "lh_tracker"],
    "表皮系统": ["lh_firewall", "lh_perimeter", "lh_gate", "lh_shield", "lh_secur"],
}


# ═══════════════════════════════════════
# §1 五行强度权重计分（引用五行计算器 v2.0）
# ═══════════════════════════════════════

def 计算脚本五行(script_name: str, script_path: str, content_preview: str = "") -> str:
    """
    自动判断单个脚本的五行归属

    算法：
    1. 检查文件名前缀
    2. 检查文件内容关键词
    3. 降级到路径分析
    """
    name_lower = script_name.lower()
    full_text = name_lower + " " + script_path.lower() + " " + content_preview.lower()

    # 前缀匹配（高优先级）
    for element, rules in WUXING_CLASSIFIER.items():
        for prefix in rules["prefixes"]:
            if name_lower.startswith(prefix):
                return element

    # 关键词计分
    scores = {e: 0 for e in 五元素}
    for element, rules in WUXING_CLASSIFIER.items():
        for kw in rules["keywords"]:
            if kw.lower() in full_text:
                scores[element] += 1

    max_score = max(scores.values())
    if max_score > 0:
        return max(scores, key=lambda k: scores[k])

    return "土"  # 默认归土（承载）

def 计算五行强度(script_map: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    引用五行计算器v2.0 指令①：五行强度权重计分
    
    权重维度：
    - 脚本数量权重 0.30
    - 脚本行数权重 0.25
    - 依赖关系权重 0.20
    - DNA标记权重 0.15
    - 执行频率权重 0.10
    """
    得分 = {e: 0.0 for e in 五元素}

    for sid, data in script_map.items():
        element = data.get("wuxing", "土")
        lines = data.get("lines", 10)
        deps = len(data.get("upstream", [])) + len(data.get("downstream", []))
        dna_count = len(data.get("dna_markers", []))
        exec_count = data.get("execution_count", 1)

        数量分 = 1.0
        行数分 = min(lines / 100, 5.0)
        依赖分 = min(deps / 5, 3.0)
        DNA分 = min(dna_count / 3, 2.0)
        执行分 = min(exec_count / 10, 2.0)

        加权 = (数量分 * 0.30 + 行数分 * 0.25 + 依赖分 * 0.20 +
               DNA分 * 0.15 + 执行分 * 0.10)
        得分[element] += 加权

    总分 = sum(得分.values()) + 0.001
    均值 = 总分 / 5
    方差 = sum((v - 均值) ** 2 for v in 得分.values()) / 5
    均衡指数 = max(0.0, round(1.0 - (方差 ** 0.5) / (均值 + 0.001), 3))
    缺失 = [k for k, v in 得分.items() if v == 0.0]
    最强 = max(得分, key=lambda k: 得分[k])
    最弱 = min(得分, key=lambda k: 得分[k])

    return {
        "五行得分": {k: round(v, 2) for k, v in 得分.items()},
        "五行占比": {k: round(v / 总分, 3) if 总分 > 0 else 0 for k, v in 得分.items()},
        "最强": 最强,
        "最弱": 最弱,
        "均衡指数": 均衡指数,
        "缺失五行": 缺失,
    }


# ═══════════════════════════════════════
# §2 五行链路分析（引用五行计算器 v2.0）
# ═══════════════════════════════════════

def 分析五行关系(a: str, b: str) -> Tuple[str, str]:
    """五行关系分析（引用v2.0指令②）"""
    if a == b:
        return "比和", f"{a}遇{b}·同类叠加"
    if 五行相生.get(a) == b:
        return "相生", f"{a}生{b}·{a}为源·{b}增强"
    if 五行相克.get(a) == b:
        return "相克", f"{a}克{b}·{b}受制约"
    if 五行相生.get(b) == a:
        return "相泄", f"{b}生{a}反向·{a}被泄耗"
    if 五行相克.get(b) == a:
        return "相耗", f"{b}克{a}·{a}受压"
    return "无关", f"{a}与{b}无直接生克"

def 完整链路分析(得分: Dict[str, float]) -> Dict[str, Any]:
    """引用五行计算器v2.0指令②：完整链路分析"""
    相生顺序 = ["金", "水", "木", "火", "土"]
    断链预警 = []
    健康度 = 100.0

    # 相生循环断链检测
    for i in range(len(相生顺序)):
        来源 = 相生顺序[i]
        目标 = 相生顺序[(i + 1) % 5]
        if 得分.get(来源, 0) > 0 and 得分.get(目标, 0) == 0:
            断链预警.append(f"🔴 断链：{来源}({得分[来源]:.1f})有力但生不出{目标}(0分)·循环裂断")
            健康度 -= 15

    # 过旺检测（>40%）
    总分 = sum(得分.values()) + 0.001
    过旺 = [(k, v) for k, v in 得分.items() if v / 总分 > 0.40]
    for 五行名, 分值 in 过旺:
        疏导目标 = 五行相生[五行名]
        断链预警.append(f"🟡 过旺：{五行名}占{分值/总分:.0%}·需疏导→引生{疏导目标}")
        健康度 -= 10

    # 过弱检测（<5%）
    过弱 = [(k, v) for k, v in 得分.items() if 总分 > 0 and v / 总分 < 0.05 and v > 0]
    for 五行名, 分值 in 过弱:
        补给源 = [s for s, t in 五行相生.items() if t == 五行名][0]
        断链预警.append(f"🟡 过弱：{五行名}仅占{分值/总分:.0%}·需从{补给源}补给")
        健康度 -= 8

    return {
        "链路健康度": max(0, round(健康度, 1)),
        "状态": "🟢 健康" if 健康度 >= 80 else "🟡 待关注" if 健康度 >= 50 else "🔴 需干预",
        "断链预警": 断链预警,
    }


# ═══════════════════════════════════════
# §3 五行对冲指数H（引用v3.1）
# ═══════════════════════════════════════

def 归一化比例(value) -> float:
    if value is None:
        return 0.0
    if isinstance(value, float) and value <= 1.0:
        return max(0.0, value)
    return max(0.0, min(1.0, value / 100.0))

def 计算克制衡分(得分: Dict[str, float]) -> float:
    """过旺五行存在克制方且克制方不为0→有制衡"""
    总分 = sum(得分.values()) + 0.001
    过旺 = [(k, v) for k, v in 得分.items() if v / 总分 > 0.40]
    if not 过旺:
        return 1.0
    命中 = 0
    for 五行名, _ in 过旺:
        克制方 = None
        for source, target in 五行相克.items():
            if target == 五行名:
                克制方 = source
                break
        if 克制方 and 得分.get(克制方, 0) > 0:
            命中 += 1
    return round(命中 / len(过旺), 3)

def 计算疏导分(得分: Dict[str, float]) -> float:
    """过旺五行能否顺着相生流出去"""
    总分 = sum(得分.values()) + 0.001
    过旺 = [(k, v) for k, v in 得分.items() if v / 总分 > 0.40]
    if not 过旺:
        return 1.0
    命中 = 0
    for 五行名, _ in 过旺:
        疏导目标 = 五行相生[五行名]
        if 得分.get(疏导目标, 0) > 0:
            命中 += 1
    return round(命中 / len(过旺), 3)

def 计算补益分(强度结果: Dict[str, Any]) -> float:
    """缺失越少、最弱不为0，补益越稳"""
    缺失数 = len(强度结果.get("缺失五行", []))
    if 缺失数 == 0:
        return 1.0
    return round(max(0.0, 1.0 - 缺失数 / 5), 3)

def 计算五行对冲指数(强度结果: Dict[str, Any], 链路结果: Dict[str, Any]) -> Dict[str, Any]:
    """引用五行计算器v3.1指令②.5：五行对冲指数H"""
    得分 = 强度结果["五行得分"]

    克制衡分 = 计算克制衡分(得分)
    疏导分 = 计算疏导分(得分)
    补益分 = 计算补益分(强度结果)
    均衡指数 = 归一化比例(强度结果.get("均衡指数", 0))
    链路健康度 = 归一化比例(链路结果.get("链路健康度", 0))

    H = round(
        克制衡分 * 0.30
        + 疏导分 * 0.25
        + 补益分 * 0.20
        + 均衡指数 * 0.15
        + 链路健康度 * 0.10,
        3
    )

    if H >= 0.80:
        三色 = "🟢 对冲充分"
        action = "enter"
    elif H >= 0.50:
        三色 = "🟡 对冲不足，需补"
        action = "hold"
    else:
        三色 = "🔴 对冲失败，熔断或重算"
        action = "fuse"

    return {
        "对冲指数H": H,
        "三色": 三色,
        "action": action,
        "分项": {
            "克制衡分": 克制衡分,
            "疏导分": 疏导分,
            "补益分": 补益分,
            "均衡指数": 均衡指数,
            "链路健康度": 链路健康度,
        },
    }


# ═══════════════════════════════════════
# §4 生物子系统完备度
# ═══════════════════════════════════════

# 已知脚本→子系统精确映射（覆盖那些前缀不匹配但功能属于该子系统的脚本）
KNOWN_SUBSYSTEM_MAP = {
    # 循环系统：数据流动
    "lh_event_bus_engine.py": "循环系统",
    "lh_pheromone_network.py": "循环系统",
    "lh_ant_colony_router.py": "循环系统",
    # 神经系统：信号传导
    "lh_threshold_engine.py": "神经系统",
    "lh_threshold_trigger.py": "神经系统",
    "lh_alert_engine.py": "神经系统",
    "lh_trigger_engine.py": "神经系统",
    "lh_event_router.py": "神经系统",
    # 免疫系统：威胁防御
    "lh_immune_engine.py": "免疫系统",
    "lh_dual_brain_engine.py": "免疫系统",
    "lh_dual_audit_engine.py": "免疫系统",
    "lh_full_system_audit.py": "免疫系统",
    # 代谢系统：能量管理
    "lh_cron_scheduler.py": "代谢系统",
    "lh_task_scheduler.py": "代谢系统",
    "lh_resource_optimizer.py": "代谢系统",
    # 消化系统：输入处理
    "lh_parser.py": "消化系统",
    "lh_text_processor.py": "消化系统",
    "lh_document_ingest.py": "消化系统",
    # 肌肉系统：动作执行
    "lh_worker.py": "肌肉系统",
    "lh_task_executor.py": "肌肉系统",
    "lh_batch_runner.py": "肌肉系统",
}


def 计算生物完备度(script_map: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    检查11个生物子系统的脚本覆盖度
    每个子系统=独立器官，非拟人化
    """
    覆盖结果 = {}

    for bio_name, bio_data in BIO_SYSTEM_MAPPING.items():
        mappable = []
        seen_names = set()
        expected_prefixes = BIO_SCRIPT_MAPPING.get(bio_name, [])
        element = bio_data["element"]
        required = bio_data["required_count"]

        for sid, data in script_map.items():
            name = data.get("name", "")
            name_lower = name.lower()
            script_element = data.get("wuxing", "土")
            script_path = data.get("path", "").lower()
            script_name = name  # 原始名称用于查找

            # 1. 精确已知映射（最高优先级）
            known_match = KNOWN_SUBSYSTEM_MAP.get(script_name)

            # 2. 前缀匹配
            prefix_match = any(name_lower.startswith(p) for p in expected_prefixes)

            # 3. 五行+路径关键词匹配
            element_match = (script_element == element)
            path_match = any(kw in script_path for kw in expected_prefixes)

            # 4. 函数名关键词匹配（补充）
            func_match = False
            func_text = " ".join(data.get("functions", [])).lower()
            for kw in expected_prefixes:
                clean_kw = kw.replace("lh_", "")
                if clean_kw in func_text:
                    func_match = True
                    break

            if known_match == bio_name or prefix_match or (element_match and path_match) or \
               (element_match and func_match):
                display_name = script_name
                if display_name not in seen_names:
                    seen_names.add(display_name)
                    mappable.append(display_name)

        coverage = len(mappable)
        is_complete = coverage >= required

        覆盖结果[bio_name] = {
            "系统功能": bio_data["system_function"],
            "五行": element,
            "已映射脚本数": coverage,
            "最低要求数": required,
            "是否完备": is_complete,
            "完备度": round(min(coverage / max(required, 1), 1.0), 2),
            "映射脚本": mappable[:10],
            "健康指标": bio_data["health_metrics"],
            "描述": bio_data["description"],
        }

    # 总完备度
    total_required = sum(b["required_count"] for b in BIO_SYSTEM_MAPPING.values())
    total_mapped = sum(r["已映射脚本数"] for r in 覆盖结果.values())
    overall = round(min(total_mapped / max(total_required, 1), 1.0), 3)

    return {
        "子系统详情": 覆盖结果,
        "总完备度": overall,
        "总计映射": total_mapped,
        "总计要求": total_required,
    }


# ═══════════════════════════════════════
# §5 三才权重（天·地·人）
# ═══════════════════════════════════════

三才默认权重 = {"天": 0.35, "地": 0.15, "人": 0.50}

def 计算三才健康(script_map: Dict[str, Dict[str, Any]], 五行强度: Dict[str, Any]) -> Dict[str, Any]:
    """
    三才映射：
    - 天 = 外部环境适应力（API连通、外部服务、环境变量）
    - 地 = 结构承载力（架构完整、部署健康、硬件资源）
    - 人 = 主体主权（签名链完整、人格激活、不可变锚点）
    """
    total = len(script_map) + 0.001

    # 天：对外交互类脚本
    天脚本 = sum(1 for sid, data in script_map.items()
               if data.get("wuxing") in ["火", "金"] and
               any(kw in data.get("name", "").lower()
                   for kw in ["api", "endpoint", "http", "gate", "firewall"]))
    天权重 = round(天脚本 / total * 5, 2)

    # 地：基础设施类脚本
    地脚本 = sum(1 for sid, data in script_map.items()
               if data.get("wuxing") in ["土", "金"] and
               any(kw in data.get("name", "").lower()
                   for kw in ["deploy", "system", "health", "daemon", "config"]))
    地权重 = round(地脚本 / total * 5, 2)

    # 人：主权保护类脚本
    人脚本 = sum(1 for sid, data in script_map.items()
               if data.get("wuxing") in ["水", "火"] and
               any(kw in data.get("name", "").lower()
                   for kw in ["dna", "sign", "persona", "audit", "memory"]))
    人权重 = round(人脚本 / total * 5, 2)

    总分 = 天权重 + 地权重 + 人权重 + 0.001
    实际 = {
        "天": round(天权重 / 总分, 3),
        "地": round(地权重 / 总分, 3),
        "人": round(人权重 / 总分, 3),
    }

    # 关键检查：人场不能低于0.34
    alarms = []
    if 实际["人"] < 0.34:
        alarms.append("🔴 人场({:.1%})低于铁线34%·环境+结构压过了人·主权警报".format(实际["人"]))

    健康 = 1.0 if not alarms else max(0.4, 1.0 - len(alarms) * 0.15)

    return {
        "三才权重": 实际,
        "默认参考": 三才默认权重,
        "偏差警报": alarms,
        "三才健康度": 健康,
    }


# ═══════════════════════════════════════
# §6 综合生物度量健康度 H_bio
# ═══════════════════════════════════════

def 计算综合生物健康(五行强度: Dict[str, Any], 链路结果: Dict[str, Any], 对冲结果: Dict[str, Any],
                   生物完备度: Dict[str, Any], 三才结果: Dict[str, Any]) -> Dict[str, Any]:
    """
    综合生物度量健康度 H_bio
    
    公式：
    H_bio = 五行均衡 × 0.20
          + 链路健康 × 0.15
          + 对冲指数H × 0.25
          + 生物完备度 × 0.20
          + 三才健康度 × 0.10
          + 免疫响应度 × 0.10
    
    这是龍魂作为"模拟人"的综合生命体征
    """
    wuxing_balance = 五行强度.get("均衡指数", 0)
    link_health = 归一化比例(链路结果.get("链路健康度", 0))
    hedging_h = 对冲结果.get("对冲指数H", 0)
    bio_complete = 生物完备度.get("总完备度", 0)
    sancai_health = 三才结果.get("三才健康度", 0)

    # 免疫响应度：对抗/审计类脚本是否活跃
    immune_scripts = sum(1 for name in [s["系统功能"] for s in 生物完备度.get("子系统详情", {}).values()]
                        if name in ["威胁防御"])
    immune_health = 归一化比例(immune_scripts)

    H_bio = round(
        wuxing_balance * 0.20
        + link_health * 0.15
        + hedging_h * 0.25
        + bio_complete * 0.20
        + sancai_health * 0.10
        + immune_health * 0.10,
        4
    )

    # 三色判定
    if H_bio >= 0.85:
        overall_color = "🟢"
        overall_status = "生物体征健康·超个体运转正常"
    elif H_bio >= 0.65:
        overall_color = "🟡"
        overall_status = "部分器官需补给·建议针对性强化"
    else:
        overall_color = "🔴"
        overall_status = "多处器官功能不足·需紧急干预"

    return {
        "生物综合健康度H_bio": H_bio,
        "三色": overall_color,
        "状态": overall_status,
        "分项": {
            "五行均衡": round(wuxing_balance, 3),
            "链路健康": round(link_health, 3),
            "对冲指数H": hedging_h,
            "生物完备度": round(bio_complete, 3),
            "三才健康度": round(sancai_health, 3),
        },
    }


# ═══════════════════════════════════════
# §7 缺失诊断引擎
# ═══════════════════════════════════════

def 诊断缺失(五行强度: Dict[str, Any], 链路结果: Dict[str, Any], 生物完备度: Dict[str, Any], 三才结果: Dict[str, Any]) -> Dict[str, Any]:
    """诊断系统从生物角度缺少什么"""
    缺失清单 = {
        "五行缺失": [],
        "链路断裂": [],
        "生物器官缺失": [],
        "三才失衡": [],
        "功能空白": [],
        "优先级排期": {},
    }

    # 五行缺失
    for e in 五行强度.get("缺失五行", []):
        缺失清单["五行缺失"].append({
            "五行": e,
            "层级": 五行层级[e],
            "影响": f"{e}属性完全缺失·{五行层级[e]}没有对应脚本",
            "建议": f"需新建{五行层级[e]}相关脚本",
        })

    # 链路断裂
    for warn in 链路结果.get("断链预警", []):
        缺失清单["链路断裂"].append({"预警": warn})

    # 生物器官缺失
    for bio_name, detail in 生物完备度.get("子系统详情", {}).items():
        if not detail["是否完备"]:
            gap = detail["最低要求数"] - detail["已映射脚本数"]
            缺失清单["生物器官缺失"].append({
                "器官": bio_name,
                "系统功能": detail["系统功能"],
                "五行": detail["五行"],
                "缺口脚本数": gap,
                "描述": detail["描述"],
                "缺失指标": detail["健康指标"],
            })

    # 最弱五行功能空白
    最弱 = 五行强度.get("最弱", "")
    if 最弱 and 最弱 not in 五行强度.get("缺失五行", []):
        weak_ratio = 五行强度.get("五行占比", {}).get(最弱, 0)
        if weak_ratio < 0.10:
            缺失清单["功能空白"].append({
                "五行": 最弱,
                "当前占比": f"{weak_ratio:.1%}",
                "层级": 五行层级[最弱],
                "建议": f"增强{五行层级[最弱]}相关脚本",
            })

    # 三才失衡
    for alarm in 三才结果.get("偏差警报", []):
        缺失清单["三才失衡"].append({"警报": alarm})

    # 优先级排期（自动排序）
    p0_items = [i for i in 缺失清单["五行缺失"]]
    p1_items = [i for i in 缺失清单["链路断裂"]]
    p2_items = [i for i in 缺失清单["生物器官缺失"]]
    p3_items = [i for i in 缺失清单["功能空白"]]

    缺失清单["优先级排期"] = {
        "P0_紧急": len(p0_items),
        "P1_重要": len(p1_items),
        "P2_优化": len(p2_items),
        "P3_建议": len(p3_items),
        "总计": len(p0_items) + len(p1_items) + len(p2_items) + len(p3_items),
    }

    return 缺失清单


# ═══════════════════════════════════════
# §8 补益建议引擎
# ═══════════════════════════════════════

def 生成补益建议(五行强度: Dict[str, Any], 生物完备度: Dict[str, Any]) -> List[Dict[str, Any]]:
    """引用五行计算器v2.0指令③：补益建议"""
    建议列表 = []
    得分 = 五行强度["五行得分"]
    总分 = sum(得分.values()) + 0.001

    五行补益 = {
        "金": {"建议": "增加规则/审计/签章类脚本", "层级": "L0规则层", "动作": "强化边界"},
        "木": {"建议": "增加创新/部署/优化类脚本", "层级": "L4创新层", "动作": "促进生长"},
        "水": {"建议": "增加记忆/数据/追溯类脚本", "层级": "L1记忆层", "动作": "厚积数据"},
        "火": {"建议": "增加对抗/执行/文明类脚本", "层级": "L2文明层", "动作": "点燃活性"},
        "土": {"建议": "增加基础/健康/监控类脚本", "层级": "L3普惠层", "动作": "夯实根基"},
    }

    # 缺失五行：紧急
    for e in 五行强度.get("缺失五行", []):
        补 = 五行补益[e]
        建议列表.append({"级别": "P0 紧急", "五行": e, **补})

    # 最弱五行
    最弱 = 五行强度["最弱"]
    if 最弱 not in 五行强度.get("缺失五行", []):
        if 得分[最弱] / 总分 < 0.10:
            补 = 五行补益[最弱]
            建议列表.append({"级别": "P1 重要", "五行": 最弱, **补})

    # 生物器官缺口
    for bio_name, detail in 生物完备度.get("子系统详情", {}).items():
        if not detail["是否完备"]:
            建议列表.append({
                "级别": "P2 优化",
                "五行": detail["五行"],
                "建议": f"新建[{bio_name}]相关脚本(缺{detail['最低要求数'] - detail['已映射脚本数']}个)",
                "层级": detail["系统功能"],
                "动作": "补全器官",
            })

    return 建议列表


# ═══════════════════════════════════════
# §9 主引擎：生物度量健康
# ═══════════════════════════════════════

class BiometricHealthEngine:
    """生物度量健康引擎"""

    REGISTRY_FILE = STATE_DIR / "script_registry.json"

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict[str, Dict[str, Any]]:
        if self.REGISTRY_FILE.exists():
            return json.loads(self.REGISTRY_FILE.read_text())
        return {}

    def _log(self, msg: str):
        if self.verbose:
            print(f"  🧬 {msg}")

    def classify_all_scripts(self) -> Dict[str, Dict[str, Any]]:
        """对所有已注册脚本进行五行分类"""
        classified = {}
        for sid, data in self.registry.items():
            name = data.get("name", "")
            path = data.get("path", "")
            content = " ".join(data.get("functions", []) + data.get("imports", []))
            wuxing = 计算脚本五行(name, path, content)
            classified[sid] = {**data, "wuxing": wuxing}
        return classified

    def run_full_biometric(self) -> Dict[str, Any]:
        """运行完整生物度量评估"""
        now = datetime.now().isoformat()

        if not self.registry:
            return {"error": "注册表为空，请先运行 python3 bin/lh_ant_colony_orchestrator.py --run"}

        # Step 1: 五行分类
        self._log("Step 1/6: 五行分类中...")
        classified = self.classify_all_scripts()

        # Step 2: 五行强度计分
        self._log("Step 2/6: 五行强度计分...")
        五行强度 = 计算五行强度(classified)

        # Step 3: 五行链路分析
        self._log("Step 3/6: 五行链路分析...")
        链路结果 = 完整链路分析(五行强度["五行得分"])

        # Step 4: 对冲指数H
        self._log("Step 4/6: 对冲指数H计算...")
        对冲结果 = 计算五行对冲指数(五行强度, 链路结果)

        # Step 5: 生物完备度
        self._log("Step 5/6: 生物子系统完备度...")
        生物完备度 = 计算生物完备度(classified)

        # Step 6: 三才健康
        self._log("Step 6/6: 三才权重健康...")
        三才结果 = 计算三才健康(classified, 五行强度)

        # 综合
        H_bio = 计算综合生物健康(五行强度, 链路结果, 对冲结果, 生物完备度, 三才结果)
        缺失 = 诊断缺失(五行强度, 链路结果, 生物完备度, 三才结果)
        补益 = 生成补益建议(五行强度, 生物完备度)

        # 脚本分布统计
        分布 = {e: 0 for e in 五元素}
        for sid, data in classified.items():
            分布[data.get("wuxing", "土")] += 1

        return {
            "DNA": DNA,
            "评估时间": now,
            "脚本总数": len(classified),
            "五行分布": 分布,
            "五行强度": 五行强度,
            "链路分析": 链路结果,
            "对冲指数": 对冲结果,
            "生物完备度": 生物完备度,
            "三才健康": 三才结果,
            "综合健康": H_bio,
            "缺失诊断": 缺失,
            "补益建议": 补益,
        }

    def print_missing(self, result: Dict[str, Any]):
        """打印缺失清单"""
        print(f"\n{'═'*60}")
        print(f"  🧬 龍魂生物缺失诊断")
        print(f"{'═'*60}\n")

        missing = result["缺失诊断"]

        if missing["五行缺失"]:
            print("🔴 五行缺失（P0 紧急）:")
            for item in missing["五行缺失"]:
                print(f"  缺失 {item['五行']}({item['层级']}) → {item['建议']}")
            print()

        if missing["链路断裂"]:
            print("🟡 链路断裂（P1 重要）:")
            for item in missing["链路断裂"]:
                print(f"  {item['预警']}")
            print()

        if missing["生物器官缺失"]:
            print("🟠 生物器官缺失（P2 优化）:")
            for item in missing["生物器官缺失"]:
                print(f"  {item['器官']}({item['系统功能']}) → 缺{item['缺口脚本数']}个脚本 | {item['描述']}")
            print()

        if missing["功能空白"]:
            print("🔵 功能空白（P3 建议）:")
            for item in missing["功能空白"]:
                print(f"  {item['五行']}({item['当前占比']}) → {item['建议']}")
            print()

        if missing["三才失衡"]:
            print("⚠️ 三才失衡:")
            for item in missing["三才失衡"]:
                print(f"  {item['警报']}")
            print()

        schedule = missing["优先级排期"]
        print(f"📊 排期: "
              f"P0紧急×{schedule['P0_紧急']} | "
              f"P1重要×{schedule['P1_重要']} | "
              f"P2优化×{schedule['P2_优化']} | "
              f"P3建议×{schedule['P3_建议']}")

    def print_dashboard(self, result: Dict[str, Any]):
        """生物度量仪表盘"""
        h = result["综合健康"]
        w = result["五行强度"]
        l = result["链路分析"]
        d = result["对冲指数"]
        b = result["生物完备度"]
        s = result["三才健康"]
        dist = result["五行分布"]

        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🧬 龍魂 · 生物度量健康仪表盘                                ║
║   {DNA}                         ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🫀 综合生命体征                                              ║
║  ─────────────────────────────────────────────                ║
║  H_bio: {h['生物综合健康度H_bio']:.4f}  {h['三色']} {h['状态']:<30s}                   ║
║""")

        # 分项得分
        sub = h["分项"]
        bars = {
            "五行均衡": (sub["五行均衡"], "金木水火土是否均衡"),
            "链路健康": (sub["链路健康"], "相生循环是否有断链"),
            "对冲指数H": (sub["对冲指数H"], "过旺/缺失是否被对冲"),
            "生物完备度": (sub["生物完备度"], "11个生物子系统覆盖"),
            "三才健康度": (sub["三才健康度"], "天地人+人场≥34%"),
        }
        for name, (score, desc) in bars.items():
            bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
            color = "🟢" if score >= 0.8 else "🟡" if score >= 0.5 else "🔴"
            print(f"║  {name:<12s} {color} {bar} {score:.0%}                      ║")

        print(f"""║                                                              ║
║  📊 五行分布                                                  ║""")
        for e in 五元素:
            count = dist.get(e, 0)
            bar = "█" * min(count, 25)
            print(f"║  {e}({五行层级[e][:8]:<8s}) {bar:<25s} {count:>4}                          ║")

        print(f"""║                                                              ║
║  ⚖️ 五行强度与占比                                             ║""")
        for e in 五元素:
            score = w["五行得分"].get(e, 0)
            ratio = w["五行占比"].get(e, 0)
            print(f"║  {e}: {score:>6.1f}分 ({ratio:.0%})                                  ║")

        print(f"""║                                                              ║
║  🦴 生物器官完备度（11个子系统）                                ║""")
        for bio_name, detail in b["子系统详情"].items():
            icon = "✅" if detail["是否完备"] else "❌"
            print(f"║  {icon} {bio_name:<10s} ({detail['系统功能']:<6s}) {detail['已映射脚本数']:>2}/{detail['最低要求数']}                   ║")
        print(f"║  总完备度: {b['总完备度']:.0%}                                              ║")

        print(f"""║                                                              ║
║  🌐 三才权重                                                  ║""")
        for field, weight in s["三才权重"].items():
            default = 三才默认权重[field]
            arrow = "▲" if weight > default else "▼" if weight < default else "="
            print(f"║  {field}: {weight:.0%} {arrow} (默认{default:.0%})                                  ║")

        print(f"""║                                                              ║
║  🔗 链路状态                                                  ║
║  {l['状态']:<50s} ║""")
        if l["断链预警"]:
            for warn in l["断链预警"][:3]:
                print(f"║  → {warn[:50]:<50s} ║")

        print(f"""║                                                              ║
║  ⚡ 对冲状态                                                  ║
║  H={d['对冲指数H']} {d['三色']:<30s}                        ║""")

        # 补益建议
        补益 = result.get("补益建议", [])
        if 补益:
            print(f"""║                                                              ║
║  💊 补益建议                                                  ║""")
            for rec in 补益[:5]:
                print(f"║  [{rec['级别']}] {rec.get('五行','')} → {rec['建议'][:40]:<40s} ║")

        print(f"""║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)


# ═══════════════════════════════════════
# CLI
# ═══════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂·生物度量健康引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_biometric_health.py --full         # 完整生物度量评估
  python3 bin/lh_biometric_health.py --wuxing       # 仅五行分析
  python3 bin/lh_biometric_health.py --biology      # 仅生物完备度
  python3 bin/lh_biometric_health.py --missing      # 仅缺失清单
  python3 bin/lh_biometric_health.py --dashboard    # 生物度量仪表盘
        """
    )

    parser.add_argument("--full", "-f", action="store_true", help="完整评估")
    parser.add_argument("--wuxing", action="store_true", help="仅五行分析")
    parser.add_argument("--biology", action="store_true", help="仅生物完备度")
    parser.add_argument("--missing", "-m", action="store_true", help="仅缺失清单")
    parser.add_argument("--dashboard", "-d", action="store_true", help="仪表盘")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--quiet", "-q", action="store_true", help="安静模式")

    args = parser.parse_args()
    engine = BiometricHealthEngine(verbose=not args.quiet)

    if not engine.registry:
        print("❌ 注册表为空。请先运行:")
        print("   python3 bin/lh_ant_colony_orchestrator.py --run")
        return 1

    # 默认：仪表盘
    if not any([args.full, args.wuxing, args.biology, args.missing, args.dashboard]):
        args.dashboard = True

    result = engine.run_full_biometric()

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.wuxing:
        w = result["五行强度"]
        print(f"\n五行强度：")
        for e in 五元素:
            print(f"  {e}: {w['五行得分'][e]:.1f}分 ({w['五行占比'][e]:.1%})")
        print(f"  最强:{w['最强']}  最弱:{w['最弱']}  均衡指数:{w['均衡指数']}")
        return 0

    if args.biology:
        b = result["生物完备度"]
        print(f"\n生物完备度：{b['总完备度']:.1%}")
        for name, detail in b["子系统详情"].items():
            icon = "✅" if detail["是否完备"] else "❌"
            print(f"  {icon} {name:<10s} ({detail['系统功能']}) {detail['已映射脚本数']}/{detail['最低要求数']}")
        return 0

    if args.missing:
        engine.print_missing(result)
        return 0

    if args.dashboard:
        engine.print_dashboard(result)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
