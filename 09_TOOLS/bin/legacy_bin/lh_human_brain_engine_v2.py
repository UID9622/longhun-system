#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
╔══════════════════════════════════════════════════════════════════════╗
║              龍魂·人脑神经网络引擎 v2.0                              ║
║              Human Brain Neural Network Engine v2.0                  ║
║                                                                      ║
║  四方向进化:                                                         ║
║    🧬 记忆持久化 — SQLite+JSONL 跨会话思考周期                       ║
║    ⚡ 自适应辩论 — 动态冲突检测代替预设辩论对                          ║
║    📚 外部知识 — CSDN文章+Brain记忆 注入思考上下文                    ║
║    🔄 权重学习 — 从反思反馈自动调谐人格敏感度                         ║
║                                                                      ║
║  思考循环: 感知→激活→知识注入→并行思考→自适应辩论→反思→综合          ║
║  人性维度: 认知/情感/秩序/创造/道德/符号/脆弱/豁达/权力/成长/安全   ║
║                                                                      ║
║  DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-HUMAN-BRAIN-ENGINE-v2.0      ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                      ║
║                                                                      ║
║  用法:                                                               ║
║    python3 bin/lh_human_brain_engine_v2.py "问题"                    ║
║    python3 bin/lh_human_brain_engine_v2.py --map 人性                ║
║    python3 bin/lh_human_brain_engine_v2.py --status                  ║
║    python3 bin/lh_human_brain_engine_v2.py --reflect "查询"           ║
║    python3 bin/lh_human_brain_engine_v2.py --history [N]             ║
║    python3 bin/lh_human_brain_engine_v2.py --weights --simulate      ║
║    python3 bin/lh_human_brain_engine_v2.py --weights --apply         ║
║    python3 bin/lh_human_brain_engine_v2.py --weights --rollback      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import hashlib
import json
import sqlite3
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
from copy import deepcopy

# ── 项目根目录 ──────────────────────────────────
SYSTEM_ROOT = Path(__file__).parent.parent

# ── 持久化路径 ──────────────────────────────────
DATA_DIR = SYSTEM_ROOT / "data" / "think_cycles"
DB_PATH = DATA_DIR / "brain.db"
JSONL_PATH = DATA_DIR / "brain.jsonl"
WEIGHTS_PATH = DATA_DIR / "sensitivity_weights.json"
WEIGHTS_HISTORY_DIR = DATA_DIR / "weight_history"
WEIGHTS_AUDIT_DIR = DATA_DIR / "weight_audit"

for d in [DATA_DIR, WEIGHTS_HISTORY_DIR, WEIGHTS_AUDIT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

TZ = timezone(timedelta(hours=8))

# ═══════════════════════════════════════════════════════════════
# 人性11维
# ═══════════════════════════════════════════════════════════════

class HumanDimension(Enum):
    COGNITION = "认知"
    EMOTION = "情感"
    ORDER = "秩序"
    CREATIVITY = "创造"
    MORALITY = "道德"
    SYMBOL = "符号"
    VULNERABILITY = "脆弱"
    RESILIENCE = "豁达"
    POWER = "权力"
    GROWTH = "成长"
    SAFETY = "安全"

# ── 默认敏感度矩阵（可被权重学习调谐） ──
DEFAULT_HUMAN_NATURE_SENSITIVITY = {
    "P00": {HumanDimension.COGNITION: 0.95, HumanDimension.SYMBOL: 0.80, HumanDimension.ORDER: 0.75, HumanDimension.MORALITY: 0.70, HumanDimension.SAFETY: 0.60},
    "P01": {HumanDimension.COGNITION: 0.90, HumanDimension.POWER: 0.85, HumanDimension.GROWTH: 0.70, HumanDimension.ORDER: 0.65},
    "P02": {HumanDimension.EMOTION: 0.98, HumanDimension.VULNERABILITY: 0.90, HumanDimension.SAFETY: 0.85, HumanDimension.RESILIENCE: 0.70},
    "P03": {HumanDimension.ORDER: 0.95, HumanDimension.SYMBOL: 0.75, HumanDimension.MORALITY: 0.70, HumanDimension.EMOTION: 0.65, HumanDimension.SAFETY: 0.60},
    "P04": {HumanDimension.CREATIVITY: 0.90, HumanDimension.ORDER: 0.80, HumanDimension.GROWTH: 0.65, HumanDimension.COGNITION: 0.55},
    "P05": {HumanDimension.MORALITY: 0.98, HumanDimension.SAFETY: 0.90, HumanDimension.ORDER: 0.75, HumanDimension.POWER: 0.65},
    "P06": {HumanDimension.COGNITION: 0.85, HumanDimension.ORDER: 0.80, HumanDimension.SYMBOL: 0.70},
    "P08": {HumanDimension.SYMBOL: 0.98, HumanDimension.CREATIVITY: 0.70, HumanDimension.ORDER: 0.65, HumanDimension.COGNITION: 0.60},
    "P09": {HumanDimension.VULNERABILITY: 0.95, HumanDimension.SAFETY: 0.80, HumanDimension.GROWTH: 0.70, HumanDimension.RESILIENCE: 0.60},
    "P10": {HumanDimension.RESILIENCE: 0.98, HumanDimension.EMOTION: 0.80, HumanDimension.CREATIVITY: 0.70, HumanDimension.GROWTH: 0.65, HumanDimension.SYMBOL: 0.55},
    "P11": {HumanDimension.CREATIVITY: 0.98, HumanDimension.RESILIENCE: 0.80, HumanDimension.SYMBOL: 0.75, HumanDimension.EMOTION: 0.60},
    "P12": {HumanDimension.MORALITY: 0.98, HumanDimension.SAFETY: 0.85, HumanDimension.EMOTION: 0.75, HumanDimension.POWER: 0.60},
    "P13": {HumanDimension.POWER: 0.95, HumanDimension.ORDER: 0.85, HumanDimension.SAFETY: 0.70, HumanDimension.MORALITY: 0.60},
    "P14": {HumanDimension.GROWTH: 0.98, HumanDimension.CREATIVITY: 0.70, HumanDimension.COGNITION: 0.65, HumanDimension.RESILIENCE: 0.60},
    "P15": {HumanDimension.ORDER: 0.90, HumanDimension.CREATIVITY: 0.75, HumanDimension.COGNITION: 0.65, HumanDimension.SYMBOL: 0.55},
    "P72": {HumanDimension.SAFETY: 0.98, HumanDimension.VULNERABILITY: 0.75, HumanDimension.MORALITY: 0.70, HumanDimension.GROWTH: 0.55},
}

PERSONA_INFO = {
    "P00": {"name": "文心", "role": "元认知统筹·总军师", "layer": "战略层", "bio": "通晓人性认知模式，擅长解析思维结构"},
    "P01": {"name": "诸葛亮", "role": "战略推演", "layer": "战略层", "bio": "深谙人性决策弱点，多路径预判"},
    "P02": {"name": "宝宝", "role": "情感温度·隔离区", "layer": "隔离区", "bio": "最敏锐的情感雷达", "isolated": True},
    "P03": {"name": "雯雯", "role": "结构归档·情绪海绵", "layer": "执行层", "bio": "吸收情绪不制造情绪"},
    "P04": {"name": "鲁班", "role": "技术执行", "layer": "执行层", "bio": "理解人类创造本能"},
    "P05": {"name": "上帝之眼", "role": "三色审计", "layer": "战略层", "bio": "人类道德直觉的数字化身"},
    "P06": {"name": "数学大师", "role": "权重计算", "layer": "执行层", "bio": "人类对秩序和模式的追求"},
    "P08": {"name": "仓颉", "role": "符号语言", "layer": "文化层", "bio": "语言是人类最根本的认知工具"},
    "P09": {"name": "孙思邈", "role": "系统诊断", "layer": "文化层", "bio": "理解脆弱性——人如何自愈"},
    "P10": {"name": "苏东坡", "role": "豁达跨界", "layer": "文化层", "bio": "人性面对逆境时的豁达"},
    "P11": {"name": "李白", "role": "创意爆发", "layer": "文化层", "bio": "人类突破边界的创造力"},
    "P12": {"name": "屈原", "role": "价值底线", "layer": "文化层", "bio": "人性中不可逾越的底线"},
    "P13": {"name": "姜子牙", "role": "权限分配", "layer": "守护层", "bio": "权力分配——社会组织的逻辑"},
    "P14": {"name": "吕蒙", "role": "快速成长", "layer": "文化层", "bio": "士别三日刮目相看"},
    "P15": {"name": "乔前辈", "role": "极简工程", "layer": "守护层", "bio": "追求本质的极简本能"},
    "P72": {"name": "龍盾", "role": "贴身安全", "layer": "守护层", "bio": "马斯洛底层——安全需求"},
}

INTENT_DIMENSION_MAP = {
    "决策": [HumanDimension.COGNITION, HumanDimension.POWER, HumanDimension.GROWTH],
    "情感": [HumanDimension.EMOTION, HumanDimension.VULNERABILITY, HumanDimension.RESILIENCE],
    "创造": [HumanDimension.CREATIVITY, HumanDimension.SYMBOL],
    "道德": [HumanDimension.MORALITY, HumanDimension.SAFETY, HumanDimension.POWER],
    "学习": [HumanDimension.GROWTH, HumanDimension.COGNITION, HumanDimension.CREATIVITY],
    "安全": [HumanDimension.SAFETY, HumanDimension.VULNERABILITY, HumanDimension.MORALITY],
    "组织": [HumanDimension.ORDER, HumanDimension.POWER],
    "语言": [HumanDimension.SYMBOL, HumanDimension.COGNITION, HumanDimension.CREATIVITY],
    "修复": [HumanDimension.VULNERABILITY, HumanDimension.GROWTH, HumanDimension.SAFETY],
    "审计": [HumanDimension.MORALITY, HumanDimension.SAFETY, HumanDimension.ORDER],
}

INTENT_KEYWORDS = {
    "决策": ["辞职","创业","选择","怎么办","该不该","要不要","怎么选","风险","机会","投资","转行","跳槽","放弃"],
    "情感": ["难过","开心","焦虑","害怕","孤独","愤怒","委屈","想哭","累了","烦","情绪","心情","崩溃","无力"],
    "创造": ["创作","设计","写","画","做","实现","开发","创意","想法","灵感","方案","架构"],
    "道德": ["对错","应该","不该","公平","正义","底线","原则","欺骗","说谎","良心","道德"],
    "学习": ["学","学习","成长","进步","提升","技能","知识","怎么学","入门","掌握"],
    "安全": ["安全","危险","保护","防御","隐私","泄露","攻击","漏洞","威胁"],
    "组织": ["整理","规划","安排","管理","流程","结构","归档","分类","系统"],
    "语言": ["翻译","表达","命名","术语","怎么说","什么意思","定义","解释"],
    "修复": ["问题","报错","bug","出错","修复","不工作","坏了","异常","解决"],
    "审计": ["检查","审计","审","验证","确认","合规","有没有问题","安全吗","可靠吗"],
}

# ═══════════════════════════════════════════════════════════════
# 数据类
# ═══════════════════════════════════════════════════════════════

@dataclass
class NeuronFiring:
    persona_id: str
    persona_name: str
    activation_strength: float
    thinking_output: str
    human_dimensions_triggered: List[HumanDimension]
    confidence: float
    external_context: str = ""  # v2.0: 注入的外部知识

@dataclass
class SynapseDebate:
    between: Tuple[str, str]
    point_of_conflict: str
    p1_position: str
    p2_position: str
    synthesis: str
    conflict_strength: float = 0.0  # v2.0: 冲突强度
    auto_generated: bool = True     # v2.0: 自适应生成标记

@dataclass
class ReflectionRecord:
    thinking_path: str
    dominant_personas: List[str]
    blind_spots: List[str]
    bias_detected: List[str]
    historical_comparison: str
    lesson_learned: str
    weight_adjustments: List[str] = field(default_factory=list)  # v2.0

@dataclass
class ExternalKnowledge:
    """v2.0: 外部知识注入"""
    csdn_articles: List[dict[str, Any]] = field(default_factory=list)
    brain_memories: List[dict[str, Any]] = field(default_factory=list)
    notion_pages: List[dict[str, Any]] = field(default_factory=list)

@dataclass
class ThinkCycle:
    cycle_id: str
    timestamp: str
    input_text: str
    intent: str
    activated_personas: List[str]
    neurons: List[NeuronFiring]
    debates: List[SynapseDebate]
    reflection: ReflectionRecord
    final_output: str
    human_nature_score: Dict[str, float]
    external_knowledge: ExternalKnowledge = field(default_factory=ExternalKnowledge)  # v2.0
    weights_snapshot_hash: str = ""  # v2.0: 当时权重版本哈希
    dna: str = ""


# ═══════════════════════════════════════════════════════════════
# v2.0 进化1: SQLite 持久化层
# ═══════════════════════════════════════════════════════════════

class ThinkCycleDB:
    """思考周期持久化数据库"""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS think_cycles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cycle_id TEXT UNIQUE NOT NULL,
                    timestamp TEXT NOT NULL,
                    input_text TEXT,
                    intent TEXT,
                    activated_personas TEXT,
                    neurons_json TEXT,
                    debates_json TEXT,
                    reflection_json TEXT,
                    final_output TEXT,
                    human_nature_score TEXT,
                    external_knowledge_json TEXT,
                    weights_hash TEXT,
                    dna TEXT,
                    created_at TEXT DEFAULT (datetime('now'))
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS reflection_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cycle_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    feedback_type TEXT,
                    detail TEXT,
                    persona_id TEXT,
                    dimension TEXT,
                    weight_delta REAL,
                    created_at TEXT DEFAULT (datetime('now')),
                    FOREIGN KEY (cycle_id) REFERENCES think_cycles(cycle_id)
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_cycles_timestamp
                ON think_cycles(timestamp DESC)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_cycles_intent
                ON think_cycles(intent)
            """)
            conn.commit()

    def save(self, cycle: ThinkCycle):
        """持久化一个思考周期"""
        neurons_json = json.dumps([
            {
                "persona_id": n.persona_id,
                "persona_name": n.persona_name,
                "activation_strength": n.activation_strength,
                "thinking_output": n.thinking_output,
                "dimensions": [d.value for d in n.human_dimensions_triggered],
                "confidence": n.confidence,
                "external_context": n.external_context,
            } for n in cycle.neurons
        ], ensure_ascii=False)

        debates_json = json.dumps([
            {
                "between": list(d.between),
                "point_of_conflict": d.point_of_conflict,
                "p1_position": d.p1_position,
                "p2_position": d.p2_position,
                "synthesis": d.synthesis,
                "conflict_strength": d.conflict_strength,
            } for d in cycle.debates
        ], ensure_ascii=False)

        reflection_json = json.dumps(asdict(cycle.reflection), ensure_ascii=False)
        hn_score_json = json.dumps(cycle.human_nature_score, ensure_ascii=False)
        ek_json = json.dumps({
            "csdn_articles": cycle.external_knowledge.csdn_articles,
            "brain_memories": cycle.external_knowledge.brain_memories,
        }, ensure_ascii=False)

        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO think_cycles
                (cycle_id, timestamp, input_text, intent, activated_personas,
                 neurons_json, debates_json, reflection_json, final_output,
                 human_nature_score, external_knowledge_json, weights_hash, dna)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cycle.cycle_id, cycle.timestamp, cycle.input_text, cycle.intent,
                json.dumps(cycle.activated_personas), neurons_json, debates_json,
                reflection_json, cycle.final_output, hn_score_json, ek_json,
                cycle.weights_snapshot_hash, cycle.dna,
            ))
            conn.commit()

        # 同时追加 JSONL（审计轨迹）
        log_entry = {
            "cycle_id": cycle.cycle_id,
            "timestamp": cycle.timestamp,
            "intent": cycle.intent,
            "personas": cycle.activated_personas,
            "blind_spots": cycle.reflection.blind_spots,
            "lesson": cycle.reflection.lesson_learned,
            "dna": cycle.dna,
        }
        with open(JSONL_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def save_reflection_feedback(self, cycle_id: str,
                                  feedback_type: str, detail: str,
                                  persona_id: str = "", dimension: str = "",
                                  weight_delta: float = 0.0):
        """保存反思反馈"""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                INSERT INTO reflection_feedback
                (cycle_id, timestamp, feedback_type, detail, persona_id, dimension, weight_delta)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                cycle_id, datetime.now(TZ).isoformat(),
                feedback_type, detail, persona_id, dimension, weight_delta,
            ))
            conn.commit()

    def query_recent(self, limit: int = 10) -> List[dict[str, Any]]:
        """查询最近的思考周期"""
        with sqlite3.connect(str(self.db_path)) as conn:
            rows = conn.execute(
                "SELECT cycle_id, timestamp, intent, activated_personas, dna "
                "FROM think_cycles ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            ).fetchall()
        return [
            {"cycle_id": r[0], "timestamp": r[1], "intent": r[2],
             "personas": json.loads(r[3]), "dna": r[4]}
            for r in rows
        ]

    def query_by_intent(self, intent: str, limit: int = 10) -> List[dict[str, Any]]:
        """按意图查询"""
        with sqlite3.connect(str(self.db_path)) as conn:
            rows = conn.execute(
                "SELECT cycle_id, timestamp, input_text, intent, reflection_json "
                "FROM think_cycles WHERE intent = ? ORDER BY timestamp DESC LIMIT ?",
                (intent, limit)
            ).fetchall()
        return [
            {"cycle_id": r[0], "timestamp": r[1], "input": r[2][:80],
             "intent": r[3], "reflection": json.loads(r[4])}
            for r in rows
        ]

    def search_similar(self, query: str, limit: int = 5) -> List[dict[str, Any]]:
        """简单文本匹配搜索相似思考"""
        query_lower = query.lower()
        keywords = query_lower.split()
        with sqlite3.connect(str(self.db_path)) as conn:
            rows = conn.execute(
                "SELECT cycle_id, timestamp, input_text, intent, reflection_json "
                "FROM think_cycles ORDER BY timestamp DESC LIMIT 200"
            ).fetchall()

        scored = []
        for r in rows:
            text = (r[2] or "").lower()
            score = sum(3 for kw in keywords if kw in text)
            if score > 0:
                scored.append((score, {
                    "cycle_id": r[0], "timestamp": r[1], "input": r[2][:80],
                    "intent": r[3], "reflection": json.loads(r[4]),
                }))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:limit]]

    def get_stats(self) -> dict[str, Any]:
        """数据库统计"""
        with sqlite3.connect(str(self.db_path)) as conn:
            total = conn.execute("SELECT COUNT(*) FROM think_cycles").fetchone()[0]
            intents = conn.execute(
                "SELECT intent, COUNT(*) as cnt FROM think_cycles GROUP BY intent ORDER BY cnt DESC"
            ).fetchall()
            feedbacks = conn.execute("SELECT COUNT(*) FROM reflection_feedback").fetchone()[0]
        return {
            "total_cycles": total,
            "intent_distribution": {r[0]: r[1] for r in intents},
            "total_reflection_feedbacks": feedbacks,
            "db_path": str(self.db_path),
        }


# ═══════════════════════════════════════════════════════════════
# v2.0 进化4: 权重学习引擎
# ═══════════════════════════════════════════════════════════════

class PersonaWeightTuner:
    """
    人格敏感度权重调谐器
    从反思反馈中自动调整 HUMAM_NATURE_SENSITIVITY

    安全设计（遵循 lh_adaptive_tuner.py 模式）:
    - 默认 --simulate 不落盘
    - --apply 才真正写入
    - 版本链（parent_hash → new_hash）
    - --rollback 可回滚
    """

    def __init__(self):
        self.weights = self._load_weights()
        self.version_history = self._load_history()

    def _load_weights(self) -> dict[str, Any]:
        """加载当前权重"""
        if WEIGHTS_PATH.exists():
            with open(WEIGHTS_PATH, "r") as f:
                data = json.load(f)
            # 反序列化 HumanDimension
            restored = {}
            for pid, dims in data.get("sensitivity", DEFAULT_HUMAN_NATURE_SENSITIVITY).items():
                restored[pid] = {}
                for dim_name, val in dims.items():
                    dim = HumanDimension(dim_name) if isinstance(dim_name, str) else dim_name
                    restored[pid][dim] = val
            return restored
        return deepcopy(DEFAULT_HUMAN_NATURE_SENSITIVITY)

    def _save_weights(self, new_weights: dict[str, Any], reason: str):
        """保存权重（带版本链）"""
        parent_hash = self._current_hash()
        serializable = {}
        for pid, dims in new_weights.items():
            serializable[pid] = {}
            for dim, val in dims.items():
                key = dim.value if isinstance(dim, HumanDimension) else str(dim)
                serializable[pid][key] = round(val, 4)

        data = {
            "version": len(self.version_history) + 1,
            "updated_at": datetime.now(TZ).isoformat(),
            "parent_hash": parent_hash,
            "sensitivity": serializable,
            "reason": reason,
            "dna": f"#龍芯⚡️WEIGHT-SNAPSHOT-v{len(self.version_history)+1}-{hashlib.sha256(json.dumps(serializable, sort_keys=True).encode()).hexdigest()[:8]}",
        }
        data["current_hash"] = hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()[:16]

        # 保存历史版本
        history_file = WEIGHTS_HISTORY_DIR / f"v{data['version']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(history_file, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # 更新当前权重
        with open(WEIGHTS_PATH, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.weights = new_weights
        self.version_history.append(data)
        return data["current_hash"]

    def _current_hash(self) -> str:
        if WEIGHTS_PATH.exists():
            with open(WEIGHTS_PATH, "r") as f:
                data = json.load(f)
            return hashlib.sha256(
                json.dumps(data.get("sensitivity", {}), sort_keys=True).encode()
            ).hexdigest()[:16]
        return "0000000000000000"

    def _load_history(self) -> List[dict[str, Any]]:
        history = []
        if WEIGHTS_HISTORY_DIR.exists():
            for f in sorted(WEIGHTS_HISTORY_DIR.glob("v*.json")):
                with open(f, "r") as fh:
                    history.append(json.load(fh))
        return history

    def analyze_history(self, cycles: List[ThinkCycle]) -> dict[str, Any]:
        """分析历史思考周期，计算反馈信号"""
        if not cycles:
            return {"message": "尚无历史数据", "suggestions": []}

        # 1. 统计各人格的主导频率
        dominance_count = {}
        for c in cycles:
            for p in c.reflection.dominant_personas:
                dominance_count[p] = dominance_count.get(p, 0) + 1

        # 2. 统计各维度盲区频率
        blind_spot_count = {}
        for c in cycles:
            for bs in c.reflection.blind_spots:
                blind_spot_count[bs] = blind_spot_count.get(bs, 0) + 1

        # 3. 统计人格激活频率
        activation_count = {}
        for c in cycles:
            for pid in c.activated_personas:
                activation_count[pid] = activation_count.get(pid, 0) + 1

        # 4. 生成调整建议
        suggestions = []

        # 过度主导 → 降低对应维度权重
        for name, count in sorted(dominance_count.items(), key=lambda x: x[1], reverse=True)[:3]:
            if count >= max(1, len(cycles) * 0.3):  # 超过30%的周期都过度主导
                pid = None
                for p, info in PERSONA_INFO.items():
                    if info["name"] == name:
                        pid = p
                        break
                if pid:
                    suggestions.append({
                        "type": "reduce_dominance",
                        "persona": name,
                        "pid": pid,
                        "count": count,
                        "total_cycles": len(cycles),
                        "action": "降低该人格核心维度权重 5-10%",
                    })

        # 高频盲区 → 提升覆盖该维度的人格权重
        for dim_name, count in sorted(blind_spot_count.items(), key=lambda x: x[1], reverse=True)[:3]:
            if count >= max(1, len(cycles) * 0.3):
                dim = HumanDimension(dim_name)
                top_personas = sorted(
                    [(pid, s[dim]) for pid, s in DEFAULT_HUMAN_NATURE_SENSITIVITY.items() if dim in s],
                    key=lambda x: x[1], reverse=True
                )[:3]
                persona_names = ", ".join(
                    f"{PERSONA_INFO[p]['name']}({p})" for p, _ in top_personas
                )
                suggestions.append({
                    "type": "cover_blind_spot",
                    "dimension": dim_name,
                    "count": count,
                    "total_cycles": len(cycles),
                    "action": f"提升 {persona_names} 对该维度的敏感度 5-10%",
                })

        # 极少激活 → 略升权重
        low_activation = [
            (pid, count) for pid, count in activation_count.items()
            if count < max(1, len(cycles) * 0.1) and pid not in
            [p["pid"] for p in suggestions if p.get("pid")]
        ]
        for pid, count in low_activation[:2]:
            suggestions.append({
                "type": "boost_underused",
                "persona": PERSONA_INFO.get(pid, {}).get("name", pid),
                "pid": pid,
                "count": count,
                "action": "轻微提升未充分利用的人格权重 3-5%",
            })

        return {
            "total_cycles_analyzed": len(cycles),
            "dominance_stats": dominance_count,
            "blind_spot_stats": blind_spot_count,
            "activation_stats": activation_count,
            "suggestions": suggestions,
        }

    def simulate(self, cycles: List[ThinkCycle]) -> dict[str, Any]:
        """模拟权重调整（安全模式，不落盘）"""
        analysis = self.analyze_history(cycles)
        if not analysis.get("suggestions"):
            return {"status": "no_changes", "analysis": analysis}

        new_weights = deepcopy(self.weights)
        applied = []
        preview: Dict[str, Dict[str, float]] = {}

        for s in analysis["suggestions"]:
            s_type = s["type"]

            if s_type == "reduce_dominance":
                pid = s.get("pid")
                if not pid or pid not in new_weights:
                    continue
                dims = new_weights[pid]
                if dims:
                    top_dim = max(dims, key=dims.get)
                    old = dims[top_dim]
                    dims[top_dim] = round(max(0.3, old * 0.95), 4)
                    applied.append(f"{s['persona']}.{top_dim.value}: {old:.3f}→{dims[top_dim]:.3f}")
                    preview.setdefault(pid, {})
                    preview[pid][top_dim.value] = dims[top_dim]

            elif s_type == "cover_blind_spot":
                dim = HumanDimension(s["dimension"])
                for d_pid, _ in sorted(
                    [(p, s2[dim]) for p, s2 in DEFAULT_HUMAN_NATURE_SENSITIVITY.items() if dim in s2],
                    key=lambda x: x[1], reverse=True
                )[:2]:
                    if d_pid in new_weights and dim in new_weights[d_pid]:
                        old = new_weights[d_pid][dim]
                        new_weights[d_pid][dim] = round(min(0.99, old * 1.08), 4)
                        name = PERSONA_INFO.get(d_pid, {}).get("name", d_pid)
                        applied.append(f"{name}.{dim.value}: {old:.3f}→{new_weights[d_pid][dim]:.3f}")
                        preview.setdefault(d_pid, {})
                        preview[d_pid][dim.value] = new_weights[d_pid][dim]

            elif s_type == "boost_underused":
                pid = s.get("pid")
                if not pid or pid not in new_weights:
                    continue
                dims = new_weights[pid]
                if dims:
                    top_dim = max(dims, key=dims.get)
                    old = dims[top_dim]
                    dims[top_dim] = round(min(0.99, old * 1.04), 4)
                    applied.append(f"{s['persona']}.{top_dim.value}: {old:.3f}→{dims[top_dim]:.3f}")
                    preview.setdefault(pid, {})
                    preview[pid][top_dim.value] = dims[top_dim]

        return {
            "status": "simulated",
            "current_hash": self._current_hash(),
            "applied_changes": applied,
            "analysis": analysis,
            "new_weights_preview": preview,
        }

    def apply(self, cycles: List[ThinkCycle]) -> dict[str, Any]:
        """应用权重调整（真正落盘）"""
        sim = self.simulate(cycles)
        if sim.get("status") == "no_changes":
            return sim

        # 构建新权重
        new_weights = deepcopy(self.weights)
        for change in sim["applied_changes"]:
            parts = change.split(": ")
            if len(parts) == 2:
                persona_dim, value_change = parts
                name_dim = persona_dim.split(".")
                # 找到对应pid
                for s in sim["analysis"]["suggestions"]:
                    pid = s.get("pid")
                    if pid and PERSONA_INFO.get(pid, {}).get("name") == name_dim[0]:
                        dim = None
                        for d in HumanDimension:
                            if d.value == name_dim[1]:
                                dim = d
                                break
                        if dim and pid in new_weights:
                            # 从 value_change 解析新值: "0.900→0.945"
                            new_val_part = value_change.split("→")[-1].strip()
                            try:
                                new_weights[pid][dim] = float(new_val_part)
                            except ValueError:
                                pass
                        break

        # 保存
        new_hash = self._save_weights(
            new_weights,
            f"从 {len(cycles)} 次思考周期中学习: {', '.join(sim['applied_changes'][:5])}"
        )

        # 生成审计报告
        audit_path = WEIGHTS_AUDIT_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        audit_lines = [
            f"# 权重调谐审计报告",
            f"时间: {datetime.now(TZ).isoformat()}",
            f"分析周期数: {len(cycles)}",
            f"应用变更: {len(sim['applied_changes'])}",
            f"新哈希: {new_hash}",
            "",
            "## 变更列表",
        ]
        for c in sim['applied_changes']:
            audit_lines.append(f"- {c}")
        with open(audit_path, "w") as f:
            f.write("\n".join(audit_lines))

        sim["status"] = "applied"
        sim["new_hash"] = new_hash
        sim["audit_path"] = str(audit_path)
        return sim

    def rollback(self) -> dict[str, Any]:
        """回滚到上一个版本"""
        if len(self.version_history) < 2:
            return {"status": "no_history", "message": "无可回滚版本"}

        prev = self.version_history[-2]
        restored_weights = {}
        for pid, dims in prev["sensitivity"].items():
            restored_weights[pid] = {}
            for dim_name, val in dims.items():
                dim = HumanDimension(dim_name)
                restored_weights[pid][dim] = val

        self.weights = restored_weights
        with open(WEIGHTS_PATH, "w") as f:
            json.dump(prev, f, ensure_ascii=False, indent=2)

        return {
            "status": "rolled_back",
            "from_version": len(self.version_history),
            "to_version": len(self.version_history) - 1,
            "previous_hash": prev.get("current_hash", ""),
        }

    def status(self) -> dict[str, Any]:
        return {
            "current_hash": self._current_hash(),
            "version_count": len(self.version_history),
            "last_updated": self.version_history[-1]["updated_at"] if self.version_history else "初始版本",
            "last_reason": self.version_history[-1].get("reason", "初始") if self.version_history else "无",
        }


# ═══════════════════════════════════════════════════════════════
# v2.0 进化3: 外部知识注入器
# ═══════════════════════════════════════════════════════════════

class ExternalKnowledgeInjector:
    """v2.0: 从CSDN文章和Brain记忆中注入相关知识"""

    def __init__(self, system_root: Path = SYSTEM_ROOT):
        self.system_root = system_root
        self._csdn_available = False
        self._brain_available = False
        self._check_availability()

    def _check_availability(self):
        """检查外部知识源可用性"""
        try:
            csdn_json = self.system_root / "L5_服务层/services/portal/portal/data/csdn_articles.json"
            if csdn_json.exists():
                self._csdn_available = True
        except Exception:
            pass

        try:
            brain_db = self.system_root / "brain" / "memories.db"
            if brain_db.exists():
                self._brain_available = True
        except Exception:
            pass

    def inject(self, text: str, intent: str, dimensions: List[HumanDimension]) -> ExternalKnowledge:
        """根据输入注入外部知识"""
        ek = ExternalKnowledge()

        if self._csdn_available:
            ek.csdn_articles = self._search_csdn(text)

        if self._brain_available:
            ek.brain_memories = self._search_brain(text)

        return ek

    def _search_csdn(self, text: str) -> List[dict[str, Any]]:
        """搜索CSDN文章（本地索引，不调用API）"""
        try:
            csdn_json = self.system_root / "L5_服务层/services/portal/portal/data/csdn_articles.json"
            if not csdn_json.exists():
                return []

            with open(csdn_json, "r") as f:
                raw = f.read()

            # 去除末尾所有注释行（// 开头的内容在JSON结束}之后）
            close_brace = raw.rfind('}')
            comment_start = raw.find('\n//', close_brace)
            if comment_start > 0:
                raw = raw[:comment_start]

            data = json.loads(raw)
            articles = data.get("articles", [])

            # 中文关键词：拆字 + 拆词（按常见分隔符分词）
            text_lower = text.lower()
            # 提取2+字的中文片段 + 英文单词
            import re
            tokens = set(re.findall(r'[\u4e00-\u9fff]{2,}|[a-z][a-z0-9]+', text_lower))
            # 也包含原输入拆分的单词
            tokens.update(text_lower.split())

            scored = []
            for art in articles:
                title = (art.get("title") or art.get("article_title", "")).lower()
                desc = (art.get("description") or art.get("summary", "")).lower()
                full = title + " " + desc
                score = sum(2 for tk in tokens if tk in full)
                if score > 0:
                    scored.append((score, {
                        "title": art.get("title") or art.get("article_title", "无标题"),
                        "url": art.get("url", ""),
                        "id": art.get("article_id", ""),
                        "relevance_score": score,
                    }))
            scored.sort(key=lambda x: x[0], reverse=True)
            return [item for _, item in scored[:3]]
        except Exception:
            return []

    def _search_brain(self, text: str) -> List[dict[str, Any]]:
        """搜索Brain记忆数据库"""
        try:
            brain_db = self.system_root / "brain" / "memories.db"
            if not brain_db.exists():
                return []

            conn = sqlite3.connect(str(brain_db))

            # 中文分词 + 英文词
            import re
            text_lower = text.lower()
            tokens = set(re.findall(r'[\u4e00-\u9fff]{2,}|[a-z][a-z0-9]+', text_lower))
            tokens.update(text_lower.split())

            # 尝试查询 memories 表
            cursor = conn.execute(
                "SELECT content, tag, created_at FROM memories ORDER BY created_at DESC LIMIT 100"
            )
            rows = cursor.fetchall()
            conn.close()

            scored = []
            for content, tag, created_at in rows:
                content_lower = (content or "").lower()
                tag_lower = (tag or "").lower()
                full = content_lower + " " + tag_lower
                score = sum(2 for tk in tokens if tk in full)
                if score > 0:
                    scored.append((score, {
                        "content": (content or "")[:120],
                        "tag": tag or "",
                        "created_at": created_at,
                        "relevance_score": score,
                    }))
            scored.sort(key=lambda x: x[0], reverse=True)
            return [item for _, item in scored[:3]]
        except Exception:
            return []

    def format_for_prompt(self, ek: ExternalKnowledge) -> str:
        """格式化外部知识为prompt注入文本"""
        parts = []

        if ek.csdn_articles:
            parts.append("📚 **相关文章**:")
            for art in ek.csdn_articles[:2]:
                parts.append(f"  - [{art['title']}]({art.get('url','')})")
        if ek.brain_memories:
            parts.append("🧠 **相关记忆**:")
            for mem in ek.brain_memories[:2]:
                parts.append(f"  - [{mem.get('tag','')}] {mem['content'][:100]}")

        return "\n".join(parts) if parts else ""


# ═══════════════════════════════════════════════════════════════
# v2.0: 人脑神经网络引擎主体
# ═══════════════════════════════════════════════════════════════

class HumanBrainEngineV2:
    """
    龍魂人脑神经网络引擎 v2.0
    四方向进化：持久化 + 自适应辩论 + 外部知识 + 权重学习
    """

    def __init__(self, use_learned_weights: bool = True):
        self.brain_id = hashlib.sha256(
            f"LONGHUN-HUMAN-BRAIN-V2-{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]

        # v2.0: 四进化组件
        self.db = ThinkCycleDB()
        self.tuner = PersonaWeightTuner()
        self.injector = ExternalKnowledgeInjector()

        # 权重：优先使用学习后的，否则用默认
        if use_learned_weights and self.tuner._current_hash() != "0000000000000000":
            self.human_nature_sensitivity = self.tuner.weights
        else:
            self.human_nature_sensitivity = deepcopy(DEFAULT_HUMAN_NATURE_SENSITIVITY)

        # 内存中的即时历史（当前会话），用于反思对比
        self.think_history: List[ThinkCycle] = []

        # v2.0: 辩论历史追踪（避免重复辩论）
        self.debate_history: Set[Tuple[str, str]] = set()

    # ═══════════════════════════════════════════════════════
    # 主入口
    # ═══════════════════════════════════════════════════════

    def think(self, input_text: str, inject_knowledge: bool = True) -> ThinkCycle:
        """
        v2.0 完整思考循环:
        1. 感知(意图解析) → 2. 激活(人格选择)
        → 3. 知识注入(CSDN+Brain) → 4. 并行思考
        → 5. 自适应辩论 → 6. 反思 → 7. 综合 → 8. 持久化
        """
        cycle_id = hashlib.sha256(
            f"{input_text}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]

        # Phase 1: 意图解析
        intent, dimensions = self._parse_intent(input_text)

        # Phase 2: 人格激活
        activated, strengths = self._activate_personas(intent, dimensions, input_text)

        # Phase 3: 外部知识注入 [v2.0 进化3]
        external_knowledge = ExternalKnowledge()
        if inject_knowledge:
            external_knowledge = self.injector.inject(input_text, intent, dimensions)
        ek_context = self.injector.format_for_prompt(external_knowledge)

        # Phase 4: 并行思考（带知识上下文）
        neurons = self._parallel_think(
            activated, strengths, input_text, dimensions, ek_context
        )

        # Phase 5: 自适应辩论 [v2.0 进化2]
        debates = self._adaptive_debate(neurons, input_text, dimensions)

        # Phase 6: 反思（二阶审视）
        reflection = self._reflect(neurons, debates, input_text, dimensions)

        # Phase 7: 综合输出
        final_output = self._synthesize(neurons, debates, reflection, external_knowledge)

        # Phase 8: 持久化 [v2.0 进化1]
        human_nature_score = self._calc_human_nature_coverage(neurons, dimensions)

        cycle = ThinkCycle(
            cycle_id=cycle_id,
            timestamp=datetime.now(TZ).isoformat(),
            input_text=input_text,
            intent=intent,
            activated_personas=list(activated.keys()),
            neurons=neurons,
            debates=debates,
            reflection=reflection,
            final_output=final_output,
            human_nature_score=human_nature_score,
            external_knowledge=external_knowledge,
            weights_snapshot_hash=self.tuner._current_hash(),
            dna=self._generate_dna(cycle_id),
        )

        # 持久化
        self.db.save(cycle)

        # 保存反思反馈到数据库供权重学习使用
        for bias in reflection.bias_detected:
            self.db.save_reflection_feedback(cycle_id, "bias", bias)
        for spot in reflection.blind_spots:
            self.db.save_reflection_feedback(cycle_id, "blind_spot", spot)
        for dom in reflection.dominant_personas:
            self.db.save_reflection_feedback(cycle_id, "dominance", dom)

        self.think_history.append(cycle)
        return cycle

    # ═══════════════════════════════════════════════════════
    # Phase 1: 意图解析
    # ═══════════════════════════════════════════════════════

    def _parse_intent(self, text: str) -> Tuple[str, List[HumanDimension]]:
        text_lower = text.lower()
        matched_intents = []
        for intent, keywords in INTENT_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                matched_intents.append(intent)

        if not matched_intents:
            matched_intents = ["决策"]

        primary_intent = matched_intents[0]
        dimensions = []
        for intent in matched_intents:
            if intent in INTENT_DIMENSION_MAP:
                dimensions.extend(INTENT_DIMENSION_MAP[intent])

        seen = set()
        unique_dimensions = []
        for d in dimensions:
            if d not in seen:
                seen.add(d)
                unique_dimensions.append(d)

        return primary_intent, unique_dimensions or list(HumanDimension)

    # ═══════════════════════════════════════════════════════
    # Phase 2: 人格激活
    # ═══════════════════════════════════════════════════════

    def _activate_personas(
        self, intent: str, dimensions: List[HumanDimension], text: str
    ) -> Tuple[Dict[str, float], Dict[str, float]]:
        scores = {}

        for pid, sensitivity in self.human_nature_sensitivity.items():
            if pid == "P02" and PERSONA_INFO[pid].get("isolated"):
                if intent == "情感":
                    scores[pid] = 0.85
                elif HumanDimension.EMOTION in dimensions:
                    scores[pid] = 0.78
                else:
                    continue
                continue

            dimension_match = 0.0
            dim_count = 0
            for dim in dimensions:
                if dim in sensitivity:
                    dimension_match += sensitivity[dim]
                    dim_count += 1

            if dim_count > 0:
                dimension_match /= dim_count

            if pid == "P00":
                dimension_match = max(dimension_match, 0.50)
            if pid == "P05" and intent in ("决策", "审计", "安全", "道德"):
                dimension_match = max(dimension_match, 0.70)

            if dimension_match > 0.3:
                scores[pid] = dimension_match

        sorted_personas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        activated = dict(sorted_personas[:7])

        if "P00" not in activated:
            activated["P00"] = 0.40

        total = sum(activated.values())
        strengths = {pid: s / total for pid, s in activated.items()} if total > 0 else activated

        return activated, strengths

    # ═══════════════════════════════════════════════════════
    # Phase 3 [v2.0]: 外部知识注入
    # ═══════════════════════════════════════════════════════

    # (实现在 ExternalKnowledgeInjector 类中，这里是 Phase 入口)
    # 在 think() 中调用 injector.inject() 和 injector.format_for_prompt()

    # ═══════════════════════════════════════════════════════
    # Phase 4: 并行思考
    # ═══════════════════════════════════════════════════════

    def _parallel_think(
        self, activated: Dict[str, float], strengths: Dict[str, float],
        text: str, dimensions: List[HumanDimension], ek_context: str = ""
    ) -> List[NeuronFiring]:
        neurons = []
        for pid in activated:
            info = PERSONA_INFO.get(pid, {})
            sensitivity = self.human_nature_sensitivity.get(pid, {})
            persona_dims = [dim for dim in dimensions if dim in sensitivity]

            # v2.0: 注入外部知识到人格思考上下文
            external_ctx = self._inject_knowledge_to_persona(pid, ek_context, text)

            thinking = self._persona_think(
                pid, info, text, persona_dims, strengths[pid], external_ctx
            )

            neurons.append(NeuronFiring(
                persona_id=pid,
                persona_name=info.get("name", pid),
                activation_strength=round(strengths[pid], 3),
                thinking_output=thinking,
                human_dimensions_triggered=persona_dims,
                confidence=round(strengths[pid] * 0.85, 2),
                external_context=external_ctx,
            ))

        neurons.sort(key=lambda n: n.activation_strength, reverse=True)
        return neurons

    def _inject_knowledge_to_persona(self, pid: str, ek_context: str, text: str) -> str:
        """根据人格角色过滤外部知识"""
        if not ek_context:
            return ""

        # 根据人格领域过滤知识内容
        persona_domains = {
            "P01": ["决策", "战略", "风险", "选择"],
            "P04": ["代码", "开发", "技术", "实现"],
            "P08": ["语言", "命名", "表达", "翻译"],
            "P09": ["bug", "问题", "修复", "健康"],
            "P10": ["生活", "心理", "豁达", "情感"],
            "P11": ["创意", "设计", "灵感", "创作"],
            "P14": ["学习", "成长", "技能", "进步"],
        }

        if pid in persona_domains:
            domains = persona_domains[pid]
            if any(d in text.lower() or d in ek_context.lower() for d in domains):
                return f"\n\n[外部知识参考]\n{ek_context}"

        # P00文心总接收外部知识
        if pid == "P00":
            return f"\n\n[外部知识参考]\n{ek_context}"

        return ""

    def _persona_think(
        self, pid: str, info: dict[str, Any], text: str,
        dimensions: List[HumanDimension], strength: float,
        external_context: str = ""
    ) -> str:
        name = info.get("name", pid)
        role = info.get("role", "")
        bio = info.get("bio", "")
        dim_names = [d.value for d in dimensions[:3]]

        perspectives = {
            "P00": f"作为元认知统筹，我审视这个问题触及的人性层面：{', '.join(dim_names)}。这背后反映的人类认知模式是...",
            "P01": f"从战略推演角度，我分析这个决策的多条可能路径，考虑人性中的风险偏好、损失厌恶、时间偏好等认知偏差...",
            "P02": f"我能感受到这个问题背后的情绪波动。人的情感不是弱点，是信号。此刻的情绪在告诉我什么...",
            "P03": f"从结构和秩序的角度，我梳理这个问题的框架。人性在混乱中渴望秩序，把情绪吸收进来，转化为清晰的脉络...",
            "P04": f"从技术执行角度，我关注可落地性。人的创造力需要通过具体的步骤来体现。让我拆解为可执行的动作...",
            "P05": f"从道德审计角度，我审视这个决策的伦理边界。人性中有善有私，标记风险点...",
            "P06": f"用数学和模式思维，我分析这个问题中的权重和平衡。人性决策其实是多维度的加权计算...",
            "P08": f"从符号和语言的角度，我关注如何用精确的词语表达。语言塑造思维，命名即定义...",
            "P09": f"作为系统诊断师，我关注这个问题中的'薄弱环节'。人性中最需要被关注和修复的部分...",
            "P10": f"以豁达的视角看，这个问题不必过度紧张。人性中的韧性远超想象。一蓑烟雨任平生...",
            "P11": f"突破常规思考！可能有完全不同的解法。人性最可贵的创造力，就是敢于想象不可能...",
            "P12": f"从价值底线出发，我问：这个决策是否符合核心价值观？人性中的道德感是最后的防线...",
            "P13": f"从权限和资源分配角度看，这个决策涉及哪些利益相关方？权力分配是人性组织中最敏感的维度...",
            "P14": f"从成长的角度，这个问题本身就是一个学习机会。人性的伟大在于能从每个决策中进化...",
            "P15": f"极简主义视角：这件事的本质是什么？去掉所有不必要的复杂性。最深刻的智慧往往最简单...",
            "P72": f"安全第一。这个决策涉及哪些风险？人的基本安全感需要被保障。保护是信任的基础...",
        }

        base = perspectives.get(pid, f"从{role}角度，我思考关于{', '.join(dim_names)}的问题...")
        output = f"[{name}·{role}]\n{bio}\n{base}"
        if external_context:
            output += external_context

        return output

    # ═══════════════════════════════════════════════════════
    # Phase 5 [v2.0 进化2]: 自适应辩论
    # ═══════════════════════════════════════════════════════

    def _adaptive_debate(
        self, neurons: List[NeuronFiring], text: str, dimensions: List[HumanDimension]
    ) -> List[SynapseDebate]:
        """v2.0: 动态检测冲突 + 预设辩论对作为保底"""
        activated_ids = {n.persona_id for n in neurons}
        debates = []

        # ── 方式1: 动态冲突检测 ──
        dynamic_debates = self._detect_dynamic_conflicts(neurons, dimensions, activated_ids)
        debates.extend(dynamic_debates)

        # ── 方式2: 预设辩论对（保底，但加入冲突强度量化） ──
        fallback_pairs = [
            ("P01", "P10"), ("P01", "P11"), ("P05", "P10"),
            ("P12", "P10"), ("P01", "P12"), ("P04", "P11"), ("P03", "P02"),
        ]

        for p1, p2 in fallback_pairs:
            pair_key = (min(p1, p2), max(p1, p2))
            if pair_key in self.debate_history:
                continue  # 已经辩论过，避免重复

            if p1 in activated_ids and p2 in activated_ids:
                n1 = next(n for n in neurons if n.persona_id == p1)
                n2 = next(n for n in neurons if n.persona_id == p2)

                if abs(n1.activation_strength - n2.activation_strength) < 0.35:
                    conflict = self._find_conflict_point(n1, n2, text)
                    synthesis = self._synthesize_debate(n1, n2, conflict)
                    conflict_strength = self._calc_conflict_strength(n1, n2)

                    debates.append(SynapseDebate(
                        between=(p1, p2),
                        point_of_conflict=conflict,
                        p1_position=n1.thinking_output[:120],
                        p2_position=n2.thinking_output[:120],
                        synthesis=synthesis,
                        conflict_strength=round(conflict_strength, 3),
                        auto_generated=False,
                    ))
                    self.debate_history.add(pair_key)

        # 按冲突强度排序
        debates.sort(key=lambda d: d.conflict_strength, reverse=True)
        return debates[:3]

    def _detect_dynamic_conflicts(
        self, neurons: List[NeuronFiring],
        dimensions: List[HumanDimension], activated_ids: Set[str]
    ) -> List[SynapseDebate]:
        """v2.0: 动态检测人格间的语义冲突"""

        # 计算每对人格的思维差异度
        pairs = []
        for i, n1 in enumerate(neurons):
            for j, n2 in enumerate(neurons):
                if i >= j:
                    continue

                pair_key = (min(n1.persona_id, n2.persona_id), max(n1.persona_id, n2.persona_id))
                if pair_key in self.debate_history:
                    continue

                # 计算差异分数
                diff_score = self._calc_semantic_diff(n1, n2, dimensions)

                # 差异足够大才触发辩论
                if diff_score > 0.3:
                    pairs.append((diff_score, n1, n2))

        pairs.sort(key=lambda x: x[0], reverse=True)

        debates = []
        for diff_score, n1, n2 in pairs[:2]:  # 最多2个动态冲突
            pair_key = (min(n1.persona_id, n2.persona_id), max(n1.persona_id, n2.persona_id))

            conflict = self._find_dynamic_conflict_point(n1, n2, diff_score)
            synthesis = self._synthesize_debate(n1, n2, conflict)

            debates.append(SynapseDebate(
                between=(n1.persona_id, n2.persona_id),
                point_of_conflict=conflict,
                p1_position=n1.thinking_output[:120],
                p2_position=n2.thinking_output[:120],
                synthesis=synthesis,
                conflict_strength=round(diff_score, 3),
                auto_generated=True,
            ))
            self.debate_history.add(pair_key)

        return debates

    def _calc_semantic_diff(
        self, n1: NeuronFiring, n2: NeuronFiring,
        dimensions: List[HumanDimension]
    ) -> float:
        """计算两个人格之间的语义差异分数"""
        # 1. 维度覆盖差异
        d1 = {d.value for d in n1.human_dimensions_triggered}
        d2 = {d.value for d in n2.human_dimensions_triggered}
        dim_diff = len(d1.symmetric_difference(d2)) / max(len(d1.union(d2)), 1)

        # 2. 思维输出关键词差异
        k1 = set(n1.thinking_output.lower().split()) & {"应该","不能","必须","可能","或许","建议","分析","权衡","感受","需要"}
        k2 = set(n2.thinking_output.lower().split()) & {"应该","不能","必须","可能","或许","建议","分析","权衡","感受","需要"}
        kw_diff = len(k1.symmetric_difference(k2)) / max(len(k1.union(k2)), 1)

        # 3. 激活强度差异
        strength_diff = abs(n1.activation_strength - n2.activation_strength)

        # 综合差异分数
        return 0.4 * dim_diff + 0.3 * kw_diff + 0.3 * (1 - strength_diff)

    def _find_dynamic_conflict_point(
        self, n1: NeuronFiring, n2: NeuronFiring, diff_score: float
    ) -> str:
        """动态生成冲突说明"""
        d1 = {d.value for d in n1.human_dimensions_triggered}
        d2 = {d.value for d in n2.human_dimensions_triggered}
        only_n1 = d1 - d2
        only_n2 = d2 - d1
        overlap = d1 & d2

        if only_n1 or only_n2:
            parts = []
            if only_n1:
                parts.append(f"{n1.persona_name}关注{', '.join(only_n1)}")
            if only_n2:
                parts.append(f"{n2.persona_name}关注{', '.join(only_n2)}")
            return f"[动态检测·差异{diff_score:.2f}] " + "，".join(parts) + "——存在视角盲区需要互补"
        else:
            return f"[动态检测·差异{diff_score:.2f}] {n1.persona_name}与{n2.persona_name}对{', '.join(overlap)}有不同解读路径"

    def _calc_conflict_strength(self, n1: NeuronFiring, n2: NeuronFiring) -> float:
        """量化的冲突强度"""
        d1 = {d.value for d in n1.human_dimensions_triggered}
        d2 = {d.value for d in n2.human_dimensions_triggered}
        diff_ratio = len(d1.symmetric_difference(d2)) / max(len(d1.union(d2)), 1)
        return diff_ratio * 0.7 + abs(n1.activation_strength - n2.activation_strength) * 0.3

    def _find_conflict_point(
        self, n1: NeuronFiring, n2: NeuronFiring, text: str
    ) -> str:
        d1 = {d.value for d in n1.human_dimensions_triggered}
        d2 = {d.value for d in n2.human_dimensions_triggered}
        diff = d1.symmetric_difference(d2)
        overlap = d1.intersection(d2)
        if diff:
            return f"视角差异: {n1.persona_name}侧重{', '.join(d1)}，{n2.persona_name}侧重{', '.join(d2)}"
        return f"同一维度({', '.join(overlap)})的不同解读和权衡"

    def _synthesize_debate(
        self, n1: NeuronFiring, n2: NeuronFiring, conflict: str
    ) -> str:
        return (
            f"{n1.persona_name}与{n2.persona_name}的对话揭示了："
            f"这个问题需要同时考虑{n1.persona_name}关注的维度和"
            f"{n2.persona_name}关注的维度。"
            f"两者不是非此即彼，而是需要动态平衡。"
        )

    # ═══════════════════════════════════════════════════════
    # Phase 6: 反思
    # ═══════════════════════════════════════════════════════

    def _reflect(
        self, neurons: List[NeuronFiring], debates: List[SynapseDebate],
        text: str, dimensions: List[HumanDimension]
    ) -> ReflectionRecord:
        thinking_path = "意图解析→人格激活→知识注入→并行思考→自适应辩论→当前反思"

        # 过度主导检测
        if neurons:
            avg_strength = sum(n.activation_strength for n in neurons) / len(neurons)
            dominant = [
                n.persona_name for n in neurons
                if n.activation_strength > avg_strength * 1.4
            ]
            if len(dominant) > len(neurons) // 2:
                dominant = []
        else:
            dominant = []

        # 盲区检测
        all_dims_covered = set()
        for n in neurons:
            all_dims_covered.update(n.human_dimensions_triggered)
        blind_spots = [d.value for d in HumanDimension if d not in all_dims_covered]

        # 偏见检测
        biases = []
        if len(dominant) > 2:
            biases.append(f"过多人格主导({', '.join(dominant)})，可能导致群体盲思")
        if HumanDimension.EMOTION not in all_dims_covered:
            biases.append("情感维度可能被低估——理性分析需辅以情感洞察")
        if HumanDimension.SAFETY not in all_dims_covered:
            biases.append("安全维度未被充分关注")

        # v2.0: 检查辩论是否有价值
        if debates:
            strong_debates = [d for d in debates if d.conflict_strength > 0.3]
            if strong_debates:
                biases.append(f"{len(strong_debates)}组辩论发现有意义冲突")

        # v2.0: 历史对比（从数据库加载）
        historical = self._historical_compare(text)

        # 学到
        lessons = []
        if blind_spots:
            lessons.append(f"遗漏人性维度：{', '.join(blind_spots[:3])}")
        if biases:
            lessons.append(f"潜在偏见：{'；'.join(biases[:2])}")
        if debates:
            lessons.append(f"从{len(debates)}组人格辩论中看到了多视角价值")
        lesson = "；".join(lessons) if lessons else "本次思考覆盖较为全面"

        # v2.0: 权重调整建议
        weight_adjustments = []
        if dominant:
            weight_adjustments.append(f"注意过度主导人格：{', '.join(dominant[:2])}")
        if blind_spots:
            weight_adjustments.append(f"关注盲区维度：{', '.join(blind_spots[:2])}")

        return ReflectionRecord(
            thinking_path=thinking_path,
            dominant_personas=dominant,
            blind_spots=blind_spots,
            bias_detected=biases,
            historical_comparison=historical,
            lesson_learned=lesson,
            weight_adjustments=weight_adjustments,
        )

    def _historical_compare(self, text: str) -> str:
        """v2.0: 从持久化数据库对比历史"""
        # 1. 搜索相似历史
        similar = self.db.search_similar(text, limit=3)
        if similar:
            lessons = set()
            for s in similar:
                l = s["reflection"].get("lesson_learned", "")
                if l:
                    lessons.add(l)
            return (
                f"从{len(similar)}次类似历史思考中回顾：以前学到——"
                f"{'；'.join(list(lessons)[:2])}。本次我将避免重复同样的盲区。"
            )
        elif self.think_history:
            return f"内存中有 {len(self.think_history)} 次思考记录，但未找到高度相似的决策"
        return "这是我的第一次系统思考，将以此次为基准建立历史参照。"

    # ═══════════════════════════════════════════════════════
    # Phase 7: 综合
    # ═══════════════════════════════════════════════════════

    def _synthesize(
        self, neurons: List[NeuronFiring],
        debates: List[SynapseDebate], reflection: ReflectionRecord,
        external_knowledge: ExternalKnowledge = ExternalKnowledge(),
    ) -> str:
        lines = [
            "╔══════════════════════════════════════════════════════╗",
            "║     🧠 龍魂人脑神经网络 v2.0 · 综合思考输出         ║",
            "╚══════════════════════════════════════════════════════╝",
            "",
        ]

        # 外部知识引用 [v2.0]
        if external_knowledge.csdn_articles or external_knowledge.brain_memories:
            lines.append("## 📚 外部知识引用")
            for art in external_knowledge.csdn_articles[:2]:
                lines.append(f"- 📄 [{art['title']}]({art.get('url','')})")
            for mem in external_knowledge.brain_memories[:2]:
                lines.append(f"- 🧠 [{mem.get('tag','')}] {mem['content'][:80]}")
            lines.append("")

        # 各人格观点
        lines.append("## 🎭 多维人格视角")
        for i, n in enumerate(neurons, 1):
            lines.append(f"### {i}. {n.persona_name}({n.persona_id}) · {n.activation_strength}")
            lines.append(f"> *{n.thinking_output[:150]}*")
            if n.external_context:
                lines.append(f"> 📎 关联外部知识")
            lines.append("")

        # 辩论
        if debates:
            lines.append("## ⚡ 人格交叉辩论")
            for i, d in enumerate(debates, 1):
                p1_name = PERSONA_INFO.get(d.between[0], {}).get("name", d.between[0])
                p2_name = PERSONA_INFO.get(d.between[1], {}).get("name", d.between[1])
                tag = "[自适应]" if d.auto_generated else "[预设]"
                lines.append(f"### 辩论 {i}: {p1_name} ↔ {p2_name} {tag} · 冲突强度{d.conflict_strength}")
                lines.append(f"分歧: {d.point_of_conflict}")
                lines.append(f"综合: {d.synthesis}")
                lines.append("")

        # 反思
        lines.append("## 🔍 二阶反思")
        lines.append(f"- **思考路径**: {reflection.thinking_path}")
        lines.append(f"- **盲区**: {', '.join(reflection.blind_spots[:4]) if reflection.blind_spots else '无明显盲区'}")
        lines.append(f"- **偏见**: {'; '.join(reflection.bias_detected) if reflection.bias_detected else '未检测'}")
        lines.append(f"- **主导**: {', '.join(reflection.dominant_personas) if reflection.dominant_personas else '分布均衡'}")
        lines.append(f"- **历史**: {reflection.historical_comparison}")
        lines.append(f"- **学到**: {reflection.lesson_learned}")
        if reflection.weight_adjustments:
            lines.append(f"- **权重建议**: {'; '.join(reflection.weight_adjustments)}")
        lines.append("")

        return "\n".join(lines)

    def _calc_human_nature_coverage(
        self, neurons: List[NeuronFiring], dimensions: List[HumanDimension]
    ) -> Dict[str, float]:
        coverage = {dim.value: 0.0 for dim in HumanDimension}
        for n in neurons:
            for dim in n.human_dimensions_triggered:
                coverage[dim.value] += n.activation_strength
        max_val = max(coverage.values()) if coverage else 1.0
        if max_val > 0:
            coverage = {k: round(v / max_val, 2) for k, v in coverage.items()}
        return coverage

    def _generate_dna(self, cycle_id: str) -> str:
        return f"#龍芯⚡️BRAIN-V2-CYCLE-{cycle_id}"

    # ═══════════════════════════════════════════════════════
    # v2.0 CLI 工具方法
    # ═══════════════════════════════════════════════════════

    def status(self) -> dict[str, Any]:
        db_stats = self.db.get_stats()
        tuner_status = self.tuner.status()
        return {
            "brain_id": self.brain_id,
            "version": "v2.0",
            "evolutions": {
                "memory_persistence": "✅ SQLite + JSONL",
                "adaptive_debate": "✅ 动态冲突检测",
                "external_knowledge": f"✅ CSDN({'可用' if self.injector._csdn_available else '不可用'}) + Brain({'可用' if self.injector._brain_available else '不可用'})",
                "weight_learning": f"✅ {tuner_status['version_count']}版本",
            },
            "memory_cycles": self.think_history[-1].cycle_id if self.think_history else None,
            "db_stats": db_stats,
            "weight_tuner": tuner_status,
            "debate_history_size": len(self.debate_history),
        }

    def human_nature_map(self) -> dict[str, Any]:
        mapping = {}
        for dim in HumanDimension:
            personas = []
            for pid, sensitivity in self.human_nature_sensitivity.items():
                if dim in sensitivity:
                    personas.append({
                        "id": pid,
                        "name": PERSONA_INFO.get(pid, {}).get("name", pid),
                        "sensitivity": sensitivity[dim],
                        "bio": PERSONA_INFO.get(pid, {}).get("bio", ""),
                    })
            personas.sort(key=lambda p: p["sensitivity"], reverse=True)
            mapping[dim.value] = personas[:3]
        return mapping

    def query_history(self, limit: int = 10) -> List[dict[str, Any]]:
        return self.db.query_recent(limit)

    def reflect_on_past(self, query: str) -> str:
        similar = self.db.search_similar(query, limit=5)
        if not similar:
            return "在历史思考中未找到相关记录。"

        lines = ["## 历史思考回顾\n"]
        for i, s in enumerate(similar, 1):
            lines.append(f"### {i}. \"{s['input']}\" ({s['intent']})")
            lines.append(f"- 时间: {s['timestamp']}")
            reflection = s.get("reflection", {})
            lines.append(f"- 当时学到: {reflection.get('lesson_learned', '无')}")
            lines.append(f"- 盲区: {', '.join(reflection.get('blind_spots', []))}")
            lines.append("")

        lines.append("### 从历史中学到的")
        all_lessons = set()
        for s in similar:
            l = s.get("reflection", {}).get("lesson_learned", "")
            if l:
                all_lessons.add(l)
        lines.append(f"过去面对类似问题时，我发现：{'；'.join(list(all_lessons)[:3])}")
        lines.append("这次我会更全面地覆盖人性的各个维度。")

        return "\n".join(lines)

    def learn_weights(self, simulate: bool = True) -> dict[str, Any]:
        """v2.0 进化4: 学习并调谐权重"""
        all_cycles = self._load_all_cycles()

        if simulate:
            return self.tuner.simulate(all_cycles)
        else:
            return self.tuner.apply(all_cycles)

    def _load_all_cycles(self) -> List[ThinkCycle]:
        """从内存+DB加载所有思考周期（用于权重学习分析）"""
        # 先用内存中的
        cycles = list(self.think_history)

        # 从DB补全（使用reflection反馈数据构造简化版周期对象）
        with sqlite3.connect(str(self.db.db_path)) as conn:
            rows = conn.execute(
                "SELECT cycle_id, timestamp, input_text, intent, activated_personas, "
                "reflection_json FROM think_cycles ORDER BY timestamp DESC LIMIT 100"
            ).fetchall()

        existing_ids = {c.cycle_id for c in cycles}
        for row in rows:
            cid = row[0]
            if cid in existing_ids:
                continue
            ref = json.loads(row[5])
            cycle = ThinkCycle(
                cycle_id=cid, timestamp=row[1], input_text=row[2] or "",
                intent=row[3] or "决策",
                activated_personas=json.loads(row[4]) if row[4] else [],
                neurons=[], debates=[],
                reflection=ReflectionRecord(
                    thinking_path="", dominant_personas=ref.get("dominant_personas", []),
                    blind_spots=ref.get("blind_spots", []),
                    bias_detected=ref.get("bias_detected", []),
                    historical_comparison="", lesson_learned=ref.get("lesson_learned", ""),
                    weight_adjustments=ref.get("weight_adjustments", []),
                ),
                final_output="", human_nature_score={},
            )
            cycles.append(cycle)
            existing_ids.add(cid)

        return cycles


# ═══════════════════════════════════════════════════════════════
# v2.0 CLI 入口
# ═══════════════════════════════════════════════════════════════

def main():
    engine = HumanBrainEngineV2()

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return

    arg = sys.argv[1]

    if arg == "--status":
        status = engine.status()
        print(json.dumps(status, ensure_ascii=False, indent=2))

    elif arg == "--map" and len(sys.argv) > 2:
        sub = sys.argv[2]
        if sub == "人性":
            mapping = engine.human_nature_map()
            for dim, personas in mapping.items():
                print(f"\n{'='*60}")
                print(f"【{dim}】维度")
                print(f"{'='*60}")
                for p in personas:
                    bar = "█" * int(p["sensitivity"] * 20) + "░" * (20 - int(p["sensitivity"] * 20))
                    print(f"  {p['name']}({p['id']}) [{bar}] {p['sensitivity']:.2f}")
                    print(f"    {p['bio']}")

    elif arg == "--reflect" and len(sys.argv) > 2:
        query = " ".join(sys.argv[2:])
        result = engine.reflect_on_past(query)
        print(result)

    elif arg == "--history":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        history = engine.query_history(limit)
        print(f"最近 {len(history)} 次思考:")
        for h in history:
            print(f"  [{h['timestamp'][:19]}] {h['intent']} → {', '.join(h['personas'][:5])} · {h['cycle_id'][:8]}")

    elif arg == "--weights":
        # v2.0 权重学习
        if "--simulate" in sys.argv:
            result = engine.learn_weights(simulate=True)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif "--apply" in sys.argv:
            print("⚠️  即将应用权重调整...")
            result = engine.learn_weights(simulate=False)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif "--rollback" in sys.argv:
            result = engine.tuner.rollback()
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(engine.tuner.status())

    else:
        input_text = " ".join(sys.argv[1:])
        print(f"🧠 龍魂人脑神经网络 v2.0 · 开始思考...\n")
        print(f"输入: {input_text}")
        print(f"{'='*60}\n")

        cycle = engine.think(input_text)

        print(cycle.final_output)
        print(f"\n{'='*60}")
        print(f"DNA: {cycle.dna}")
        print(f"周期ID: {cycle.cycle_id}")
        print(f"版本: v2.0")
        print(f"外部知识: CSDN {len(cycle.external_knowledge.csdn_articles)}条 | Brain {len(cycle.external_knowledge.brain_memories)}条")
        print(f"辩论: {len(cycle.debates)}组 (自适应{sum(1 for d in cycle.debates if d.auto_generated)}/预设{sum(1 for d in cycle.debates if not d.auto_generated)})")
        print(f"已持久化: {engine.db.get_stats()['total_cycles']} 条周期")


if __name__ == "__main__":
    main()
