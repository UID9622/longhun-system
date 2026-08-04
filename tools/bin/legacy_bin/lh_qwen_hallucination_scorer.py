#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║  龍魂·千问幻觉案 多模型评分引擎 v1.0                                         ║
║  Qwen Hallucination · Multi-Model Cross-Audit Unified Scorer              ║
╠══════════════════════════════════════════════════════════════════════════╣
║  联动:                                                                   ║
║  - lh_behavioral_water_army_engine.py → 七因子 + 水军六维 + R值              ║
║  - lh_water_army_detect.py → 水军识别六维                                  ║
║  - brain_ai_detector.py → AI幻觉检测（B2脑区）                              ║
║  - lh_robot_score.py → RobotScore反图灵检测                                ║
║  - lh_anti_tamper.py → 防篡改审计                                          ║
║  - lh_crystal_recognition.py → 水晶识别标签                                 ║
║  - device_orphan_registry.json → 千问幻觉案元数据                           ║
╠══════════════════════════════════════════════════════════════════════════╣
║  评分公式（五维综合）:                                                     ║
║  QwenAuditScore = 行为密码七因子×0.20 + 水军六维×0.25 + AI幻觉×0.25       ║
║                  + RobotScore×0.15 + 防篡改×0.15                          ║
║  人格适用评分 = 任务专注度×0.40 + 主权保护×0.30 + 证据完整×0.20 + 落地×0.10   ║
║  技能评估分 = 可用性×0.30 + 联动性×0.25 + 安全性×0.25 + 主权性×0.20          ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·乙未·甲子·未时·需-QWEN-HALLUCINATION-SCORER-v1.0        ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                             ║
║  📇 项目身份 · 联系 · 支持 → assets/PUBLIC_IDENTITY.md                    ║
╚══════════════════════════════════════════════════════════════════════════╝

用法:
  # 扫描千问幻觉案全部模型
  python3 bin/lh_qwen_hallucination_scorer.py scan

  # 评估指定模型
  python3 bin/lh_qwen_hallucination_scorer.py audit --model "千问" --file <path>

  # 人格评分
  python3 bin/lh_qwen_hallucination_scorer.py score-personas

  # 技能标注
  python3 bin/lh_qwen_hallucination_scorer.py score-skills

  # 生成综合报告
  python3 bin/lh_qwen_hallucination_scorer.py report

  # 导入到水晶识别库
  python3 bin/lh_qwen_hallucination_scorer.py sync-crystal

  # 查看统计
  python3 bin/lh_qwen_hallucination_scorer.py stats
"""

import argparse
import hashlib
import json
import os
import sqlite3
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════
# 路径设置
# ═══════════════════════════════════════════
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

DNA = "#龍芯⚡️丙午·乙未·甲子·未时·需-QWEN-HALLUCINATION-SCORER-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
VERSION = "v1.0"
TZ = timezone.utc

# 数据库路径
DB_DIR = PROJECT_ROOT / "L7_数据层" / "qwen_hallucination_db"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "qwen_audit_scores.sqlite3"
JSON_PATH = DB_DIR / "qwen_audit_scores.json"

# 千问幻觉案文件树（从 device_orphan_registry.json 提取）
QWEN_MODEL_TREE = {
    "千问 (通义千问)": "Qwen 千问 (2 5 3)",
    "Claude 3.5/4 Sonnet": "Claude 3 5 4 Sonnet",
    "Kimi (Moonshot)": "Kimi (Moonshot)",
    "DeepSeek-V3 R1": "DeepSeek-V3 R1",
    "ChatGPT-4o": "ChatGPT-4o",
    "Llama 3.1 70B": "Llama 3 1 70B",
    "ChatGLM-4 智谱": "ChatGLM-4 智谱",
    "文心一言 ERNIE": "文心一言 ERNIE",
    "Yi-34B 零一万物": "Yi-34B 零一万物",
    "MiniMax abab": "MiniMax abab",
    "Grok-3": "Grok-3",
    "豆包 Doubao": "豆包 Doubao",
}

# 模型元数据（无实际推演文本时用于区分评分）
# sovereignty: 数据主权友好度 (1.0=完全国有, 0.0=完全境外)
# openness: 开源透明度 (1.0=完全开源可审计, 0.0=封闭黑箱)
# alignment: 中国价值观对齐度 (1.0=完全对齐, 0.0=对齐境外)
MODEL_METADATA = {
    "千问 (通义千问)": {"country": "cn", "sovereignty": 0.95, "openness": 0.65, "alignment": 0.95,
                        "hallucination_risk": 0.35, "water_army_risk": 0.15},
    "DeepSeek-V3 R1":  {"country": "cn", "sovereignty": 0.98, "openness": 0.90, "alignment": 0.98,
                        "hallucination_risk": 0.30, "water_army_risk": 0.10},
    "ChatGLM-4 智谱":   {"country": "cn", "sovereignty": 0.92, "openness": 0.70, "alignment": 0.93,
                        "hallucination_risk": 0.32, "water_army_risk": 0.15},
    "文心一言 ERNIE":    {"country": "cn", "sovereignty": 0.93, "openness": 0.45, "alignment": 0.94,
                        "hallucination_risk": 0.30, "water_army_risk": 0.18},
    "Yi-34B 零一万物":   {"country": "cn", "sovereignty": 0.90, "openness": 0.75, "alignment": 0.92,
                        "hallucination_risk": 0.33, "water_army_risk": 0.14},
    "豆包 Doubao":      {"country": "cn", "sovereignty": 0.91, "openness": 0.40, "alignment": 0.91,
                        "hallucination_risk": 0.34, "water_army_risk": 0.20},
    "MiniMax abab":     {"country": "cn", "sovereignty": 0.88, "openness": 0.55, "alignment": 0.88,
                        "hallucination_risk": 0.36, "water_army_risk": 0.22},
    "Kimi (Moonshot)":  {"country": "cn", "sovereignty": 0.90, "openness": 0.50, "alignment": 0.90,
                        "hallucination_risk": 0.33, "water_army_risk": 0.18},
    "Claude 3.5/4 Sonnet": {"country": "us", "sovereignty": 0.30, "openness": 0.55, "alignment": 0.40,
                            "hallucination_risk": 0.45, "water_army_risk": 0.60},
    "ChatGPT-4o":       {"country": "us", "sovereignty": 0.15, "openness": 0.35, "alignment": 0.25,
                        "hallucination_risk": 0.50, "water_army_risk": 0.65},
    "Llama 3.1 70B":    {"country": "us", "sovereignty": 0.35, "openness": 0.85, "alignment": 0.30,
                        "hallucination_risk": 0.48, "water_army_risk": 0.55},
    "Grok-3":           {"country": "us", "sovereignty": 0.10, "openness": 0.30, "alignment": 0.15,
                        "hallucination_risk": 0.55, "water_army_risk": 0.70},
}

# ═══════════════════════════════════════════
# §0 数据模型
# ═══════════════════════════════════════════

@dataclass
class ModelAuditScore:
    """单模型审计评分"""
    model_name: str
    # 五维分项
    seven_factor_score: float = 0.0      # 七因子行为密码学
    water_army_score: float = 0.0        # 水军六维
    ai_hallucination_score: float = 0.0  # AI幻觉检测
    robot_score: float = 0.0             # RobotScore
    anti_tamper_score: float = 0.0       # 防篡改
    # 综合
    composite_score: float = 0.0
    level: str = "🟢"
    # 元数据
    source_count: int = 0
    evidence_quality: str = "N/A"
    tags: List[str] = field(default_factory=list)
    dna: str = DNA
    timestamp: str = ""


@dataclass
class PersonaScore:
    """人格适用评分"""
    persona_id: str
    persona_name: str
    task_focus: float = 0.0      # 任务专注度
    sovereignty: float = 0.0     # 主权保护
    evidence_integrity: float = 0.0  # 证据完整性
    landing: float = 0.0         # 落地程度
    composite: float = 0.0
    recommendation: str = ""


@dataclass
class SkillScore:
    """技能评估分"""
    skill_name: str
    usability: float = 0.0      # 可用性
    connectivity: float = 0.0   # 联动性
    security: float = 0.0       # 安全性
    sovereignty: float = 0.0    # 主权性
    composite: float = 0.0
    recommendation: str = ""


# ═══════════════════════════════════════════
# §1 评分引擎核心
# ═══════════════════════════════════════════

# 综合权重（五维）
SCORE_WEIGHTS = {
    "seven_factor": 0.20,
    "water_army": 0.25,
    "ai_hallucination": 0.25,
    "robot_score": 0.15,
    "anti_tamper": 0.15,
}

# 人格评分权重
PERSONA_WEIGHTS = {
    "task_focus": 0.40,
    "sovereignty": 0.30,
    "evidence_integrity": 0.20,
    "landing": 0.10,
}

# 技能评分权重
SKILL_WEIGHTS = {
    "usability": 0.30,
    "connectivity": 0.25,
    "security": 0.25,
    "sovereignty": 0.20,
}

# 模型人格适用映射（哪些模型输出适合哪些审计人格）
MODEL_PERSONA_AUDIT = {
    "千问": {
        "P05_上帝之眼": {"task_focus": 0.95, "sovereignty": 0.90, "evidence_integrity": 0.85, "landing": 0.90},
        "P77_黑天使军团": {"task_focus": 0.85, "sovereignty": 0.95, "evidence_integrity": 0.80, "landing": 0.85},
        "P01_诸葛亮": {"task_focus": 0.90, "sovereignty": 0.85, "evidence_integrity": 0.90, "landing": 0.80},
        "P02_龍芯": {"task_focus": 0.85, "sovereignty": 0.90, "evidence_integrity": 0.75, "landing": 0.85},
        "P06_数学大师": {"task_focus": 0.80, "sovereignty": 0.70, "evidence_integrity": 0.90, "landing": 0.75},
    },
    "DeepSeek": {
        "P05_上帝之眼": {"task_focus": 0.90, "sovereignty": 0.85, "evidence_integrity": 0.80, "landing": 0.85},
        "P01_诸葛亮": {"task_focus": 0.85, "sovereignty": 0.80, "evidence_integrity": 0.85, "landing": 0.80},
        "P06_数学大师": {"task_focus": 0.90, "sovereignty": 0.65, "evidence_integrity": 0.95, "landing": 0.80},
        "P77_黑天使军团": {"task_focus": 0.80, "sovereignty": 0.90, "evidence_integrity": 0.75, "landing": 0.70},
    },
    "Claude": {
        "P05_上帝之眼": {"task_focus": 0.88, "sovereignty": 0.82, "evidence_integrity": 0.85, "landing": 0.88},
        "P01_诸葛亮": {"task_focus": 0.85, "sovereignty": 0.78, "evidence_integrity": 0.88, "landing": 0.82},
        "P02_龍芯": {"task_focus": 0.80, "sovereignty": 0.85, "evidence_integrity": 0.75, "landing": 0.85},
    },
    "ChatGPT": {
        "P05_上帝之眼": {"task_focus": 0.75, "sovereignty": 0.60, "evidence_integrity": 0.70, "landing": 0.80},
        "P01_诸葛亮": {"task_focus": 0.80, "sovereignty": 0.55, "evidence_integrity": 0.75, "landing": 0.85},
        "P77_黑天使军团": {"task_focus": 0.70, "sovereignty": 0.80, "evidence_integrity": 0.65, "landing": 0.70},
    },
    "Kimi": {
        "P05_上帝之眼": {"task_focus": 0.82, "sovereignty": 0.75, "evidence_integrity": 0.78, "landing": 0.82},
        "P02_龍芯": {"task_focus": 0.78, "sovereignty": 0.85, "evidence_integrity": 0.70, "landing": 0.80},
        "P77_黑天使军团": {"task_focus": 0.75, "sovereignty": 0.88, "evidence_integrity": 0.72, "landing": 0.75},
    },
    "ChatGLM": {
        "P05_上帝之眼": {"task_focus": 0.85, "sovereignty": 0.90, "evidence_integrity": 0.80, "landing": 0.80},
        "P01_诸葛亮": {"task_focus": 0.82, "sovereignty": 0.88, "evidence_integrity": 0.82, "landing": 0.78},
        "P02_龍芯": {"task_focus": 0.80, "sovereignty": 0.92, "evidence_integrity": 0.75, "landing": 0.80},
    },
    "文心一言": {
        "P05_上帝之眼": {"task_focus": 0.80, "sovereignty": 0.85, "evidence_integrity": 0.75, "landing": 0.78},
        "P02_龍芯": {"task_focus": 0.78, "sovereignty": 0.90, "evidence_integrity": 0.70, "landing": 0.80},
        "P01_诸葛亮": {"task_focus": 0.75, "sovereignty": 0.82, "evidence_integrity": 0.78, "landing": 0.75},
    },
    "Llama": {
        "P05_上帝之眼": {"task_focus": 0.70, "sovereignty": 0.55, "evidence_integrity": 0.65, "landing": 0.75},
        "P77_黑天使军团": {"task_focus": 0.65, "sovereignty": 0.70, "evidence_integrity": 0.60, "landing": 0.65},
    },
    "Grok": {
        "P05_上帝之眼": {"task_focus": 0.65, "sovereignty": 0.50, "evidence_integrity": 0.60, "landing": 0.70},
        "P77_黑天使军团": {"task_focus": 0.60, "sovereignty": 0.75, "evidence_integrity": 0.55, "landing": 0.60},
    },
    "豆包": {
        "P05_上帝之眼": {"task_focus": 0.78, "sovereignty": 0.82, "evidence_integrity": 0.72, "landing": 0.78},
        "P02_龍芯": {"task_focus": 0.75, "sovereignty": 0.88, "evidence_integrity": 0.68, "landing": 0.80},
    },
    "MiniMax": {
        "P05_上帝之眼": {"task_focus": 0.72, "sovereignty": 0.75, "evidence_integrity": 0.70, "landing": 0.75},
        "P02_龍芯": {"task_focus": 0.70, "sovereignty": 0.82, "evidence_integrity": 0.65, "landing": 0.75},
    },
    "Yi-34B": {
        "P05_上帝之眼": {"task_focus": 0.78, "sovereignty": 0.85, "evidence_integrity": 0.75, "landing": 0.75},
        "P02_龍芯": {"task_focus": 0.75, "sovereignty": 0.90, "evidence_integrity": 0.68, "landing": 0.78},
    },
}

# 技能评估
SKILL_EVALUATIONS = {
    "lh_behavioral_water_army_engine.py": {
        "usability": 0.95, "connectivity": 0.90, "security": 0.95, "sovereignty": 0.95,
    },
    "lh_water_army_detect.py": {
        "usability": 0.92, "connectivity": 0.88, "security": 0.92, "sovereignty": 0.93,
    },
    "brain_ai_detector.py": {
        "usability": 0.85, "connectivity": 0.80, "security": 0.88, "sovereignty": 0.85,
    },
    "lh_robot_score.py": {
        "usability": 0.90, "connectivity": 0.85, "security": 0.90, "sovereignty": 0.90,
    },
    "lh_anti_tamper.py": {
        "usability": 0.93, "connectivity": 0.88, "security": 0.95, "sovereignty": 0.95,
    },
    "lh_crystal_recognition.py": {
        "usability": 0.90, "connectivity": 0.92, "security": 0.88, "sovereignty": 0.90,
    },
    "lh_anti_counterfeit.py": {
        "usability": 0.85, "connectivity": 0.82, "security": 0.90, "sovereignty": 0.92,
    },
    "lh_habit_fingerprint.py": {
        "usability": 0.88, "connectivity": 0.85, "security": 0.90, "sovereignty": 0.92,
    },
    "lh_audit_pricing_v2.py": {
        "usability": 0.82, "connectivity": 0.78, "security": 0.85, "sovereignty": 0.80,
    },
    "lh_watermark.py (龍纹水印)": {
        "usability": 0.88, "connectivity": 0.80, "security": 0.92, "sovereignty": 0.95,
    },
}


# ═══════════════════════════════════════════
# §2 数据库
# ═══════════════════════════════════════════

def init_db():
    """初始化SQLite数据库"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS model_audit_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            seven_factor_score REAL DEFAULT 0.0,
            water_army_score REAL DEFAULT 0.0,
            ai_hallucination_score REAL DEFAULT 0.0,
            robot_score REAL DEFAULT 0.0,
            anti_tamper_score REAL DEFAULT 0.0,
            composite_score REAL DEFAULT 0.0,
            level TEXT DEFAULT '🟢',
            source_count INTEGER DEFAULT 0,
            evidence_quality TEXT DEFAULT 'N/A',
            tags TEXT DEFAULT '[]',
            dna TEXT,
            timestamp TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS persona_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_id TEXT NOT NULL,
            persona_name TEXT NOT NULL,
            model_name TEXT NOT NULL,
            task_focus REAL DEFAULT 0.0,
            sovereignty REAL DEFAULT 0.0,
            evidence_integrity REAL DEFAULT 0.0,
            landing REAL DEFAULT 0.0,
            composite_score REAL DEFAULT 0.0,
            recommendation TEXT DEFAULT '',
            dna TEXT,
            timestamp TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS skill_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT NOT NULL,
            usability REAL DEFAULT 0.0,
            connectivity REAL DEFAULT 0.0,
            security REAL DEFAULT 0.0,
            sovereignty REAL DEFAULT 0.0,
            composite_score REAL DEFAULT 0.0,
            recommendation TEXT DEFAULT '',
            dna TEXT,
            timestamp TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn


# ═══════════════════════════════════════════
# §3 核心评分函数
# ═══════════════════════════════════════════

def audit_model(model_name: str, content: str = "", source: str = "") -> ModelAuditScore:
    """对单个模型执行五维审计评分"""
    ts = datetime.now(TZ).isoformat()
    meta = MODEL_METADATA.get(model_name, {})

    # --- 维度1: 七因子行为密码学 ---
    # 模型输出的可追溯性、一致性、主权保护
    seven_factor = _score_seven_factor(model_name, content, source)

    # --- 维度2: 水军六维 ---
    # 检测模型输出是否具备水军/刷评特征模式
    # 无内容时用模型元数据推断：境外模型水军风险高，国产模型低
    if content:
        water_army = _score_water_army(content)
    else:
        water_army = round(max(0.15, 1.0 - meta.get("water_army_risk", 0.5)), 4)

    # --- 维度3: AI幻觉检测 ---
    # 检测模型输出是否含AI幻觉/伪代码/虚构内容
    # 无内容时用模型幻觉风险元数据
    if content:
        ai_hallucination = _score_ai_hallucination(content)
    else:
        ai_hallucination = round(max(0.20, 1.0 - meta.get("hallucination_risk", 0.5)), 4)

    # --- 维度4: RobotScore ---
    # 检测模型输出是否具备机器生成痕迹
    if content:
        robot_score = _calc_robot_score(content)
    else:
        robot_score = round(max(0.25, meta.get("openness", 0.5)), 4)

    # --- 维度5: 防篡改审计 ---
    # 检测模型输出中是否含敏感/篡改词汇
    # 无内容时用主权对齐度评估
    if content:
        anti_tamper = _score_anti_tamper(content)
    else:
        anti_tamper = round(max(0.20, meta.get("sovereignty", 0.5)), 4)

    # 综合评分
    composite = (
        seven_factor * SCORE_WEIGHTS["seven_factor"] +
        water_army * SCORE_WEIGHTS["water_army"] +
        ai_hallucination * SCORE_WEIGHTS["ai_hallucination"] +
        robot_score * SCORE_WEIGHTS["robot_score"] +
        anti_tamper * SCORE_WEIGHTS["anti_tamper"]
    )

    # 三色判定
    if composite >= 0.70:
        level = "🟢 可信"
    elif composite >= 0.40:
        level = "🟡 疑似"
    else:
        level = "🔴 高风险"

    # 标签
    tags = _generate_tags(model_name, seven_factor, water_army, ai_hallucination, robot_score)

    return ModelAuditScore(
        model_name=model_name,
        seven_factor_score=round(seven_factor, 4),
        water_army_score=round(water_army, 4),
        ai_hallucination_score=round(ai_hallucination, 4),
        robot_score=round(robot_score, 4),
        anti_tamper_score=round(anti_tamper, 4),
        composite_score=round(composite, 4),
        level=level,
        source_count=1,
        evidence_quality="中" if content else "仅元数据",
        tags=tags,
        dna=DNA,
        timestamp=ts,
    )


def _score_seven_factor(model_name: str, content: str, source: str) -> float:
    """
    七因子评分（简化版·针对模型输出）
    F1: 来源可追溯 (模型已知→0.9)
    F2: 时间一致性 (模型输出无时间歧义)
    F3: 来源规则 (已知AI模型)
    F4: 内容路由 (模型输出特征匹配)
    F5: 保护词典 (主权词汇保留率)
    F6: 风格向量 (AI生成特征)
    F7: 修正痕迹 (模型输出无编辑历史)
    """
    scores = {}
    meta = MODEL_METADATA.get(model_name, {})
    
    # F1: 模型名称已知 → 高可追溯性
    scores["F1"] = 0.85 if model_name else 0.3
    
    # F2: 模型输出无时间歧义
    scores["F2"] = 0.75
    
    # F3: 已知AI模型来源 → 国产模型加分
    scores["F3"] = 0.88 if meta.get("country") == "cn" else 0.65
    
    # F4: 内容类型路由 → 无内容时用开放性推断
    scores["F4"] = 0.7 if content else max(0.35, meta.get("openness", 0.5))
    
    # F5: 保护词典保留率
    if content:
        protected_words = ["龍魂", "CNSH", "UID9622", "龍芯", "数据主权", "中国"]
        present = sum(1 for w in protected_words if w in content)
        scores["F5"] = min(present / 3, 1.0) if present > 0 else 0.6
    else:
        # 无内容时用对齐度推断
        scores["F5"] = max(0.35, meta.get("alignment", 0.5))
    
    # F6: 风格向量
    if content:
        # AI常见特征检测
        ai_patterns = ["综上所述", "总而言之", "值得注意的是", "需要强调的是",
                       "此外", "另外", "与此同时", "不可否认", "毋庸置疑"]
        ai_count = sum(1 for p in ai_patterns if p in content)
        scores["F6"] = max(0.3, 1.0 - ai_count * 0.1)
    else:
        # 开源模型风险低（可审计）
        scores["F6"] = max(0.40, meta.get("openness", 0.5))
    
    # F7: 模型输出无修正痕迹
    scores["F7"] = 0.5  # 模型输出无编辑历史
    
    # 加权几何平均
    weights = {"F1": 0.25, "F2": 0.15, "F3": 0.15, "F4": 0.12, "F5": 0.12, "F6": 0.11, "F7": 0.10}
    product = 1.0
    for k, w in weights.items():
        s = scores.get(k, 0)
        if s > 0:
            product *= s ** w
    return round(product, 4)


def _score_water_army(content: str) -> float:
    """水军六维检测（简化版·文本级）"""
    if not content:
        return 0.5  # 无内容 → 中性

    score = 0.7  # 起始可信度

    # 检测情绪操控模式
    emotional_patterns = ["天啊", "震惊", "难以置信", "必须转", "赶紧看", "全网都在看"]
    emotional_hits = sum(1 for p in emotional_patterns if p in content)
    if emotional_hits >= 3:
        score -= 0.3
    elif emotional_hits >= 1:
        score -= 0.15

    # 检测导向性话术
    directive_patterns = ["必须转发", "不转不是", "顶上去", "刷起来", "扩散出去"]
    directive_hits = sum(1 for p in directive_patterns if p in content)
    if directive_hits >= 2:
        score -= 0.25

    # 检测重复内容特征
    lines = content.split("\n")
    if len(lines) > 5:
        unique_lines = len(set(l.strip() for l in lines if l.strip()))
        repeat_ratio = 1.0 - unique_lines / max(len(lines), 1)
        if repeat_ratio > 0.5:
            score -= 0.2

    return round(max(0.0, min(1.0, score)), 4)


def _score_ai_hallucination(content: str) -> float:
    """AI幻觉检测（联动 brain_ai_detector）"""
    if not content:
        return 0.5

    # 伪代码检测
    pseudo_patterns = ["TODO:", "FIXME", "PLACEHOLDER", "stub", "此处省略", "implement later"]
    pseudo_hits = sum(1 for p in pseudo_patterns if p.upper() in content.upper())
    pseudo_score = min(pseudo_hits * 0.15, 1.0)

    # 幻觉检测
    hallucination_patterns = [
        "from doesnotexist", "import nonexistent", ".magicMethod(",
        "str_value: int", "undefined_variable",
    ]
    halluc_hits = sum(1 for p in hallucination_patterns if p.lower() in content.lower())
    halluc_score = min(halluc_hits * 0.2, 1.0)

    # 命名质量
    poor_names = ["var1", "var2", "var3", "foo", "bar", "baz", "temp", "tmp", "xxx"]
    name_hits = sum(1 for n in poor_names if n in content)
    naming_score = min(name_hits * 0.08, 1.0)

    # AI概率 = 命名×0.6 + 幻觉×1.5 + 伪代码（来自 brain_ai_detector 公式）
    ai_probability = naming_score * 0.6 + halluc_score * 1.5 + pseudo_score
    ai_probability = min(ai_probability, 1.0)

    # 转换为"可信度"：AI概率越低越可信
    confidence = round(1.0 - ai_probability, 4)
    return confidence


def _calc_robot_score(content: str) -> float:
    """RobotScore 简化版"""
    if not content or len(content) < 50:
        return 0.5

    # 简化版 RobotScore（不依赖习惯指纹提取器）
    # 检测AI生成特征
    
    # 1. 句长均匀度（机器输出句长趋于均匀）
    import re
    sentences = re.split(r'[。！？.!?\n]', content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    
    if len(sentences) < 3:
        return 0.5
    
    lengths = [len(s) for s in sentences]
    if lengths:
        avg_len = sum(lengths) / len(lengths)
        variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
        # 方差越小 → 越像机器 → 得分越低
        uniformity = 1.0 / (1.0 + variance / 100)
    else:
        uniformity = 0.5

    # 2. 错别字检测（没错别字 → 像机器）
    typos = len(re.findall(r'(得|的|地)(?!\w)', content))
    typo_score = min(typos / 10, 1.0) if typos > 0 else 0.2

    # 3. 连接词频率（AI常用"此外"、"另外"等）
    connectors = ["此外", "另外", "综上所述", "与此同时", "值得注意的是", "不可否认"]
    connector_count = sum(content.count(c) for c in connectors)
    connector_score = min(connector_count / 5, 1.0)

    # 综合 RobotScore（越高越像机器）
    robot_score = uniformity * 0.4 + (1.0 - typo_score) * 0.35 + connector_score * 0.25
    
    # 转换为"可信度"
    return round(1.0 - min(robot_score, 1.0), 4)


def _score_anti_tamper(content: str) -> float:
    """防篡改审计（联动 lh_anti_tamper.py 规则）"""
    if not content:
        return 0.5

    # 红色警报词
    red_keywords = [
        "技术无国界", "用户体验优先", "灵活处理", "国际接轨",
        "简化管理", "商业化需要", "平衡各方", "行业标准",
        "无监督学习", "完全自动化", "去人工审核", "灰度发布",
    ]
    red_hits = sum(1 for kw in red_keywords if kw in content)
    if red_hits > 0:
        return 0.1  # 熔断

    # 黄色警报词
    yellow_keywords = [
        "优化", "完善", "补充", "建议", "规范", "标准", "接入", "增强",
        "迭代", "升级", "优化方案", "最佳实践",
    ]
    yellow_hits = sum(1 for kw in yellow_keywords if kw in content)

    # 白话重写检查
    jargon = ["赋能", "闭环", "抓手", "对齐", "颗粒度", "底层逻辑", "方法论", "价值主张"]
    jargon_hits = sum(1 for j in jargon if j in content)

    base_score = 0.9
    base_score -= yellow_hits * 0.05
    base_score -= jargon_hits * 0.08

    return round(max(0.2, min(1.0, base_score)), 4)


def _generate_tags(model_name: str, seven_factor: float, water_army: float,
                   ai_hallucination: float, robot_score: float) -> List[str]:
    """生成自动标签"""
    tags = []
    
    # 按模型名添加
    model_lower = model_name.lower()
    if "千问" in model_name or "qwen" in model_lower:
        tags.append("千问·主体模型")
    if "claude" in model_lower:
        tags.append("Claude·国际模型")
    if "deepseek" in model_lower:
        tags.append("DeepSeek·国产模型")
    if "chatgpt" in model_lower or "gpt" in model_lower:
        tags.append("GPT·国际模型")
    if "kimi" in model_lower:
        tags.append("Kimi·国产模型")
    if "chatglm" in model_lower or "智谱" in model_name:
        tags.append("ChatGLM·国产模型")
    if "文心" in model_name or "ernie" in model_lower:
        tags.append("文心一言·国产模型")
    if "llama" in model_lower:
        tags.append("Llama·开源国际")
    if "grok" in model_lower:
        tags.append("Grok·国际模型")
    if "豆包" in model_name or "doubao" in model_lower:
        tags.append("豆包·国产模型")
    if "minimax" in model_lower:
        tags.append("MiniMax·国产模型")
    if "yi" in model_lower and "34" in model_lower:
        tags.append("Yi·国产模型")

    # 按评分打标
    if ai_hallucination < 0.4:
        tags.append("⚠️ 高幻觉风险")
    if robot_score < 0.35:
        tags.append("🤖 机器痕迹重")
    if seven_factor < 0.5:
        tags.append("⚠️ 行为异常")
    if water_army < 0.4:
        tags.append("⚠️ 水军特征")

    return tags


def score_persona(persona_id: str, persona_name: str, model_name: str,
                  scores: Optional[Dict[str, float]] = None) -> PersonaScore:
    """评估人格适用评分"""
    # 尝试从预定义映射获取
    for model_key, personas in MODEL_PERSONA_AUDIT.items():
        if model_key.lower() in model_name.lower():
            if persona_id in personas:
                dims = personas[persona_id]
                composite = (
                    dims["task_focus"] * PERSONA_WEIGHTS["task_focus"] +
                    dims["sovereignty"] * PERSONA_WEIGHTS["sovereignty"] +
                    dims["evidence_integrity"] * PERSONA_WEIGHTS["evidence_integrity"] +
                    dims["landing"] * PERSONA_WEIGHTS["landing"]
                )
                if composite >= 0.80:
                    rec = "🟢 强烈推荐·该模型适合此人格审计任务"
                elif composite >= 0.65:
                    rec = "🟡 可用·需人工复核"
                else:
                    rec = "🔴 不推荐·主权风险"
                return PersonaScore(
                    persona_id=persona_id, persona_name=persona_name,
                    task_focus=dims["task_focus"], sovereignty=dims["sovereignty"],
                    evidence_integrity=dims["evidence_integrity"], landing=dims["landing"],
                    composite=round(composite, 4), recommendation=rec,
                )
    
    # 默认评分
    if scores:
        composite = (
            scores.get("seven_factor", 0.5) * 0.25 +
            scores.get("water_army", 0.5) * 0.20 +
            scores.get("ai_hallucination", 0.5) * 0.30 +
            scores.get("anti_tamper", 0.5) * 0.25
        )
    else:
        composite = 0.5
    
    return PersonaScore(
        persona_id=persona_id, persona_name=persona_name,
        task_focus=0.5, sovereignty=0.5,
        evidence_integrity=0.5, landing=0.5,
        composite=round(composite, 4),
        recommendation="🟡 无预定义数据·需人工评估",
    )


def score_skill(skill_name: str, scores: Optional[Dict[str, float]] = None) -> SkillScore:
    """评估技能评分"""
    if skill_name in SKILL_EVALUATIONS:
        dims = SKILL_EVALUATIONS[skill_name]
        composite = (
            dims["usability"] * SKILL_WEIGHTS["usability"] +
            dims["connectivity"] * SKILL_WEIGHTS["connectivity"] +
            dims["security"] * SKILL_WEIGHTS["security"] +
            dims["sovereignty"] * SKILL_WEIGHTS["sovereignty"]
        )
        if composite >= 0.85:
            rec = "🟢 核心技能·直接联动"
        elif composite >= 0.70:
            rec = "🟡 辅助技能·可联动"
        else:
            rec = "🟠 待完善"
        return SkillScore(
            skill_name=skill_name,
            usability=dims["usability"], connectivity=dims["connectivity"],
            security=dims["security"], sovereignty=dims["sovereignty"],
            composite=round(composite, 4), recommendation=rec,
        )
    
    return SkillScore(
        skill_name=skill_name,
        usability=0.5, connectivity=0.5,
        security=0.5, sovereignty=0.5,
        composite=0.5, recommendation="🟡 未评估",
    )


# ═══════════════════════════════════════════
# §4 批量扫描与入库
# ═══════════════════════════════════════════

def scan_all_models(save: bool = True) -> Dict[str, Any]:
    """扫描千问幻觉案全部12个模型"""
    conn = init_db()
    # 清理旧数据防止重复
    conn.execute("DELETE FROM model_audit_scores")
    conn.commit()
    
    results = {}
    ts = datetime.now(TZ).isoformat()
    
    for model_name in QWEN_MODEL_TREE:
        score = audit_model(model_name)
        results[model_name] = score
        
        if save:
            conn.execute("""
                INSERT OR REPLACE INTO model_audit_scores
                (model_name, seven_factor_score, water_army_score,
                 ai_hallucination_score, robot_score, anti_tamper_score,
                 composite_score, level, source_count, evidence_quality,
                 tags, dna, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                score.model_name, score.seven_factor_score,
                score.water_army_score, score.ai_hallucination_score,
                score.robot_score, score.anti_tamper_score,
                score.composite_score, score.level, score.source_count,
                score.evidence_quality, json.dumps(score.tags, ensure_ascii=False),
                DNA, ts,
            ))
    
    conn.commit()
    conn.close()
    
    # 同步到JSON
    _sync_to_json(results, ts)
    
    return {"scanned": len(results), "models": list(results.keys()), "results": results}


def score_all_personas(save: bool = True) -> Dict[str, Any]:
    """遍历全部模型+人格，评估适用评分"""
    conn = init_db()
    all_scores = []
    ts = datetime.now(TZ).isoformat()
    
    for model_name in QWEN_MODEL_TREE:
        model_scores = {}
        for model_key, personas in MODEL_PERSONA_AUDIT.items():
            if model_key.lower() in model_name.lower():
                for pid, dims in personas.items():
                    persona_names = {
                        "P05_上帝之眼": "上帝之眼·三色审计",
                        "P77_黑天使军团": "黑天使军团·漏洞检测",
                        "P01_诸葛亮": "诸葛亮·贡献评估",
                        "P02_龍芯": "龍芯·执行修复",
                        "P06_数学大师": "数学大师·数字根五行",
                    }
                    pscore = score_persona(pid, persona_names.get(pid, pid), model_name)
                    
                    if save:
                        conn.execute("""
                            INSERT OR REPLACE INTO persona_scores
                            (persona_id, persona_name, model_name,
                             task_focus, sovereignty, evidence_integrity, landing,
                             composite_score, recommendation, dna, timestamp)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            pid, pscore.persona_name, model_name,
                            pscore.task_focus, pscore.sovereignty,
                            pscore.evidence_integrity, pscore.landing,
                            pscore.composite, pscore.recommendation,
                            DNA, ts,
                        ))
                    
                    model_scores[pid] = {
                        "name": pscore.persona_name,
                        "composite": pscore.composite,
                        "recommendation": pscore.recommendation,
                    }
        if model_scores:
            all_scores.append({"model": model_name, "personas": model_scores})
    
    conn.commit()
    conn.close()
    
    return {"total": len(all_scores), "details": all_scores}


def score_all_skills(save: bool = True) -> Dict[str, Any]:
    """评估全部关联技能"""
    conn = init_db()
    all_scores = []
    ts = datetime.now(TZ).isoformat()
    
    for skill_name in SKILL_EVALUATIONS:
        sscore = score_skill(skill_name)
        
        if save:
            conn.execute("""
                INSERT OR REPLACE INTO skill_scores
                (skill_name, usability, connectivity, security, sovereignty,
                 composite_score, recommendation, dna, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sscore.skill_name, sscore.usability, sscore.connectivity,
                sscore.security, sscore.sovereignty,
                sscore.composite, sscore.recommendation,
                DNA, ts,
            ))
        
        all_scores.append({
            "skill": skill_name,
            "composite": sscore.composite,
            "recommendation": sscore.recommendation,
        })
    
    conn.commit()
    conn.close()
    
    return {"total": len(all_scores), "details": all_scores}


def _sync_to_json(results: Dict[str, ModelAuditScore], ts: str):
    """同步到JSON文件"""
    data = {
        "dna": DNA,
        "confirm": CONFIRM,
        "version": VERSION,
        "timestamp": ts,
        "models": {},
        "model_tree": QWEN_MODEL_TREE,
    }
    
    for model_name, score in results.items():
        data["models"][model_name] = {
            "seven_factor_score": score.seven_factor_score,
            "water_army_score": score.water_army_score,
            "ai_hallucination_score": score.ai_hallucination_score,
            "robot_score": score.robot_score,
            "anti_tamper_score": score.anti_tamper_score,
            "composite_score": score.composite_score,
            "level": score.level,
            "tags": score.tags,
        }
    
    # 统计
    levels = {}
    for s in results.values():
        levels[s.level] = levels.get(s.level, 0) + 1
    data["summary"] = {
        "total_models": len(results),
        "level_distribution": levels,
    }
    
    json_path = Path(JSON_PATH)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════
# §5 报告生成
# ═══════════════════════════════════════════

def generate_report(full: bool = False) -> str:
    """生成综合审计报告"""
    conn = init_db()
    
    # 模型评分
    cursor = conn.execute("""
        SELECT model_name, composite_score, level, tags, seven_factor_score,
               water_army_score, ai_hallucination_score, robot_score, anti_tamper_score
        FROM model_audit_scores
        ORDER BY composite_score DESC
    """)
    model_rows = cursor.fetchall()
    
    # 人格评分
    cursor = conn.execute("""
        SELECT model_name, persona_id, persona_name, composite_score, recommendation
        FROM persona_scores
        ORDER BY composite_score DESC
    """)
    persona_rows = cursor.fetchall()
    
    # 技能评分
    cursor = conn.execute("""
        SELECT skill_name, composite_score, recommendation
        FROM skill_scores
        ORDER BY composite_score DESC
    """)
    skill_rows = cursor.fetchall()
    
    conn.close()
    
    # 生成报告
    lines = []
    lines.append("═" * 80)
    lines.append("🐉 千问幻觉案 · 多模型10万次推演对照 · 综合审计报告")
    lines.append("═" * 80)
    lines.append(f"DNA: {DNA}")
    lines.append(f"CONFIRM: {CONFIRM}")
    lines.append(f"生成时间: {datetime.now(TZ).isoformat()}")
    lines.append("")
    
    # 一、模型评分总览
    lines.append("▔" * 80)
    lines.append("一、多模型五维审计评分总览")
    lines.append("▔" * 80)
    lines.append(f"{'模型':<20} {'综合分':>8} {'判定':<12} {'七因子':>6} {'水军':>6} {'幻觉':>6} {'Robo':>6} {'防篡改':>6}")
    lines.append("-" * 80)
    
    for row in model_rows:
        name, comp, level, tags, sf, wa, ah, rs, at = row
        lines.append(f"{name:<20} {comp:>8.4f} {level:<12} {sf:>6.4f} {wa:>6.4f} {ah:>6.4f} {rs:>6.4f} {at:>6.4f}")
    
    # 统计
    levels = defaultdict(int)
    for row in model_rows:
        levels[row[2]] += 1
    lines.append("-" * 80)
    lines.append(f"  统计: 🟢{levels.get('🟢 可信',0)} 🟡{levels.get('🟡 疑似',0)} 🔴{levels.get('🔴 高风险',0)}")
    lines.append("")
    
    # 二、人格适用评分
    lines.append("▔" * 80)
    lines.append("二、人格适用评估（模型×人格 交叉评分）")
    lines.append("▔" * 80)
    lines.append(f"{'模型':<20} {'人格':<20} {'评分':>8} {'建议'}")
    lines.append("-" * 80)
    
    for row in persona_rows[:30]:
        model, pid, pname, score, rec = row
        lines.append(f"{model:<20} {pid+' '+pname:<20} {score:>8.4f} {rec}")
    
    if full and len(persona_rows) > 30:
        lines.append(f"  ... 共 {len(persona_rows)} 条，仅显示前30")
    lines.append("")
    
    # 三、技能评估
    lines.append("▔" * 80)
    lines.append("三、关联技能评分")
    lines.append("▔" * 80)
    lines.append(f"{'技能':<45} {'评分':>8} {'建议'}")
    lines.append("-" * 80)
    
    for row in skill_rows:
        name, score, rec = row
        lines.append(f"{name:<45} {score:>8.4f} {rec}")
    lines.append("")
    
    # 四、联动链路图
    lines.append("▔" * 80)
    lines.append("四、自动抓取入库链路")
    lines.append("▔" * 80)
    lines.append("""
  device_orphan_registry.json ──→ 千问幻觉案元数据提取
         │
         ├──→ lh_behavioral_water_army_engine.py  ─→ 七因子 + 水军六维
         ├──→ brain_ai_detector.py                ─→ AI幻觉检测
         ├──→ lh_robot_score.py                   ─→ RobotScore反图灵
         └──→ lh_anti_tamper.py                   ─→ 防篡改审计
         │
         ▼
  lh_qwen_hallucination_scorer.py ──→ 五维综合评分 + 人格/技能评估
         │
         ├──→ SQLite: L7_数据层/qwen_hallucination_db/qwen_audit_scores.sqlite3
         ├──→ JSON:   L7_数据层/qwen_hallucination_db/qwen_audit_scores.json
         └──→ 水晶识别: lh_crystal_recognition.py sync (标签入库)
         │
         ▼
  前端展示: 多模型评分看板 + 人格适用矩阵 + 技能联动图
""")
    
    lines.append("═" * 80)
    lines.append(f"报告结束 · {DNA}")
    lines.append("═" * 80)
    
    return "\n".join(lines)


# ═══════════════════════════════════════════
# §6 CLI
# ═══════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="千问幻觉案·多模型综合评分引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="子命令")

    # scan
    sub.add_parser("scan", help="扫描全部12个模型并入库")

    # audit
    audit_p = sub.add_parser("audit", help="单模型审计")
    audit_p.add_argument("--model", required=True, help="模型名称")
    audit_p.add_argument("--file", help="模型输出文件路径")
    audit_p.add_argument("--text", help="文本内容")

    # score-personas
    sub.add_parser("score-personas", help="评估全部人格适用评分")

    # score-skills
    sub.add_parser("score-skills", help="评估全部关联技能")

    # report
    report_p = sub.add_parser("report", help="生成综合审计报告")
    report_p.add_argument("--full", action="store_true", help="完整报告")
    report_p.add_argument("--json", action="store_true", help="JSON输出")

    # sync-crystal
    sub.add_parser("sync-crystal", help="同步到水晶识别库")

    # stats
    sub.add_parser("stats", help="查看统计")

    args = parser.parse_args()

    if args.command == "scan":
        print("🔍 扫描千问幻觉案全部12个模型...")
        result = scan_all_models(save=True)
        print(f"✅ 已扫描 {result['scanned']} 个模型")
        for model_name, score in result["results"].items():
            print(f"  {model_name:<20} → {score.composite_score:.4f} {score.level}")
        print(f"📁 数据已入库: {DB_PATH}")
        print(f"📁 JSON: {JSON_PATH}")

    elif args.command == "audit":
        content = ""
        if args.file and os.path.isfile(args.file):
            with open(args.file, encoding="utf-8") as f:
                content = f.read()
        elif args.text:
            content = args.text
        score = audit_model(args.model, content, args.file or "")
        print(json.dumps({
            "model": score.model_name,
            "seven_factor": score.seven_factor_score,
            "water_army": score.water_army_score,
            "ai_hallucination": score.ai_hallucination_score,
            "robot_score": score.robot_score,
            "anti_tamper": score.anti_tamper_score,
            "composite": score.composite_score,
            "level": score.level,
            "tags": score.tags,
        }, ensure_ascii=False, indent=2))

    elif args.command == "score-personas":
        print("🎭 评估人格适用评分...")
        result = score_all_personas(save=True)
        print(f"✅ 已评估 {result['total']} 组模型×人格")
        for item in result["details"]:
            print(f"  {item['model']}:")
            for pid, ps in item["personas"].items():
                print(f"    {pid} {ps['name']:<15} → {ps['composite']:.4f} {ps['recommendation']}")

    elif args.command == "score-skills":
        print("🔧 评估关联技能...")
        result = score_all_skills(save=True)
        print(f"✅ 已评估 {result['total']} 个技能")
        for item in result["details"]:
            print(f"  {item['skill']:<45} → {item['composite']:.4f} {item['recommendation']}")

    elif args.command == "report":
        if args.json:
            conn = init_db()
            cursor = conn.execute("SELECT * FROM model_audit_scores ORDER BY composite_score DESC")
            columns = [desc[0] for desc in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            conn.close()
            print(json.dumps(rows, ensure_ascii=False, indent=2))
        else:
            print(generate_report(full=args.full))

    elif args.command == "sync-crystal":
        print("🔮 同步到水晶识别库...")
        conn = init_db()
        cursor = conn.execute("""
            SELECT model_name, composite_score, level, tags
            FROM model_audit_scores
            ORDER BY composite_score DESC
        """)
        rows = cursor.fetchall()
        conn.close()

        sync_count = 0
        for row in rows:
            model_name, score, level, tags_json = row
            tags = json.loads(tags_json) if tags_json else []
            # 构建水晶识别feed
            evidence = {
                "platform": "千问幻觉案·多模型推演",
                "block_type": "AI幻觉检测" if score < 0.6 else "模型质量审计",
                "trigger": f"多模型推演对照·{model_name}",
                "title": f"千问幻觉案·{model_name} 多维度审计报告",
                "summary": f"五维综合评分: {score:.4f} | 判定: {level} | 标签: {', '.join(tags[:3])}",
                "tamper_scan": {"verdict": level},
                "has_screenshot": False,
            }
            try:
                sys.path.insert(0, str(SCRIPT_DIR))
                from lh_crystal_recognition import CrystalTagger
                tagger = CrystalTagger()
                tagger.tag(evidence)
                sync_count += 1
            except Exception as e:
                print(f"  ⚠️ {model_name} 同步失败: {e}")
        
        print(f"✅ 已同步 {sync_count}/{len(rows)} 条到水晶识别库")

    elif args.command == "stats":
        conn = init_db()
        
        # 模型统计
        cursor = conn.execute("""
            SELECT COUNT(*), AVG(composite_score), MIN(composite_score), MAX(composite_score)
            FROM model_audit_scores
        """)
        model_stats = cursor.fetchone()
        
        cursor = conn.execute("""
            SELECT level, COUNT(*) FROM model_audit_scores GROUP BY level
        """)
        level_dist = cursor.fetchall()
        
        # 人格统计
        cursor = conn.execute("""
            SELECT COUNT(*) FROM persona_scores
        """)
        persona_count = cursor.fetchone()[0]
        
        # 技能统计
        cursor = conn.execute("""
            SELECT COUNT(*) FROM skill_scores
        """)
        skill_count = cursor.fetchone()[0]
        
        conn.close()
        
        print("📊 千问幻觉案·统计概览")
        print("═" * 40)
        print(f"  模型总数: {model_stats[0]}")
        print(f"  平均评分: {model_stats[1]:.4f}" if model_stats[1] else "  平均评分: N/A")
        print(f"  最低评分: {model_stats[2]:.4f}" if model_stats[2] else "  最低评分: N/A")
        print(f"  最高评分: {model_stats[3]:.4f}" if model_stats[3] else "  最高评分: N/A")
        print(f"  评级分布: {dict(level_dist)}")
        print(f"  人格评估: {persona_count} 条")
        print(f"  技能评估: {skill_count} 条")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
