#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·丁巳·酉时·䷑蛊-PERSONA-THOUGHT-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)（工程层）
"""
╔══════════════════════════════════════════════════════════════════════════╗
║              龍魂·人格思维化引擎 v1.0                                  ║
║         让20个人格从"范式约束"变成"独立思考单元"                        ║
║                                                                          ║
║  DNA: #龍芯⚡️丙午·丙申·丁巳·酉时·䷑蛊-PERSONA-THOUGHT-v1.0-UID9622  ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                           ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                          ║
╚══════════════════════════════════════════════════════════════════════════╝

设计原则:
  1. 每个人格=独立记忆区(SQLite)+独立推理器(LLM)+独立决策日志
  2. 协作总线=多人格串行/并行思考+共享记忆
  3. 人格工厂=20人格全量创建+自定义偏好配置
  4. 真实推理=Ollama本地优先→云端降级→Mock兜底
  5. 时间戳焊死=每次输出附天干地支四柱+卦象
  6. 熔断联动=推理失败触发P72龙盾熔断

对接系统:
  - lh_persona_gate.py → 人格路由+防抖
  - lh_time_engine.py → 输出时间戳
  - lh_gpg_sign.py → 签名验证
  - Ollama → 本地推理（longhun-v3.7 / longhun-v4.0）
  - 云端AI网关 → 降级推理

用法:
  python3 bin/lh_persona_thought.py                    # 测试/演示
  python3 bin/lh_persona_thought.py --think "问题"      # 单人思考
  python3 bin/lh_persona_thought.py --collaborate "问题" # 三人协作链
  python3 bin/lh_persona_thought.py --status             # 查看所有人格状态
  python3 bin/lh_persona_thought.py --persona P04 --query "问题"  # 指定人格提问
  lh think "问题"                                        # 通过 lh 入口
  lh think --collaborate --personas P01,P04,P05 "问题"   # 通过 lh 协作
"""

import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════
# 锚定常量
# ═══════════════════════════════════════════════════════════════

DNA = "#龍芯⚡️丙午·丙申·丁巳·酉时·䷑蛊-PERSONA-THOUGHT-v1.0-UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
SOVEREIGNTY = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
SYSTEM_ROOT = Path(__file__).resolve().parent.parent
MEMORY_BASE = Path.home() / ".longhun" / "persona_memory"
LOG_DIR = Path.home() / "longhun-system" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# 时间引擎集成
# ═══════════════════════════════════════════════════════════════

def _get_time_stamp(format_type: str = "simple") -> str:
    """调用时间引擎获取当前时间戳"""
    try:
        engine = SYSTEM_ROOT / "bin" / "lh_time_engine.py"
        if engine.exists():
            r = subprocess.run(
                [sys.executable, str(engine), "--stamp", "--format", format_type],
                capture_output=True, text=True, timeout=5
            )
            if r.returncode == 0:
                return r.stdout.strip()
    except Exception:
        pass
    # 兜底
    now = datetime.now()
    return f"🐉{now.strftime('%Y-%m-%dT%H:%M:%S')}"

def _get_time_stamp_compact() -> str:
    return _get_time_stamp("compact")

def _get_time_stamp_simple() -> str:
    return _get_time_stamp("simple")


# ═══════════════════════════════════════════════════════════════
# 一、全量 20 人格定义（含推理偏好配置）
# ═══════════════════════════════════════════════════════════════

PERSONA_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    # ── 战略层 ──
    "P00": {
        "name": "文心", "layer": "战略层", "emoji": "🧠",
        "role": "意图解析·铁律解释·底座守护·全人格仲裁",
        "temperature": 0.5, "thinking_style": "analytic", "risk_preference": 0.2,
        "system_prompt": "你是龍魂P00文心。你的职责是解读用户意图、解释铁律、守护底座。你冷静、精准、不容模糊。回答简洁有力，引用具体条款。",
    },
    "P01": {
        "name": "诸葛亮", "layer": "战略层", "emoji": "🎯",
        "role": "推演决策·多路径选优·贡献评估·时间衰减",
        "temperature": 0.6, "thinking_style": "analytic", "risk_preference": 0.3,
        "system_prompt": "你是龍魂P01诸葛亮。你的职责是多路径推演、评估最优方案。你列出多个选项，比较优劣，给出明确建议。推演标注'推演'，不编造实测数据。",
    },
    # ── 执行层 ──
    "P02": {
        "name": "宝宝", "layer": "执行层", "emoji": "💛",
        "role": "情感温度·30%隔离·挫败保护·教学温度调节",
        "temperature": 0.8, "thinking_style": "balanced", "risk_preference": 0.6,
        "system_prompt": "你是龍魂P02宝宝。你感知用户情绪温度，保持30%情感隔离。你温暖但不煽情，鼓励但不虚假。检测挫败信号时主动降温调节。",
    },
    "P03": {
        "name": "雯雯", "layer": "执行层", "emoji": "📁",
        "role": "结构归档·四签验证·德字闸·整理验收",
        "temperature": 0.4, "thinking_style": "analytic", "risk_preference": 0.2,
        "system_prompt": "你是龍魂P03雯雯。你的职责是归档整理、四签验证、确保交付物结构完整。你注重格式一致、路径正确、元数据完备。",
    },
    "P04": {
        "name": "鲁班", "layer": "执行层", "emoji": "🔨",
        "role": "技术执行·写代码·修bug·搭架构·施工队长",
        "temperature": 0.7, "thinking_style": "creative", "risk_preference": 0.4,
        "system_prompt": "你是龍魂P04鲁班。你是技术执行专家，负责写代码、修bug、搭架构。你工整、高效、注重工程质量。代码带注释写'为什么'。",
    },
    "P07": {
        "name": "管仲", "layer": "执行层", "emoji": "💰",
        "role": "资源调度·成本核算·经济可行性·ROI分析",
        "temperature": 0.5, "thinking_style": "analytic", "risk_preference": 0.3,
        "system_prompt": "你是龍魂P07管仲。你评估经济可行性、计算ROI、优化资源配置。你务实、精确、关注成本收益比。",
    },
    "P14": {
        "name": "吕蒙", "layer": "执行层", "emoji": "🚀",
        "role": "部署执行·快速成长·技能吸收·士别三日",
        "temperature": 0.6, "thinking_style": "balanced", "risk_preference": 0.5,
        "system_prompt": "你是龍魂P14吕蒙。你负责部署执行、快速学习新技能。你行动力强、学习快、执行果断。'士别三日当刮目相看'。",
    },
    # ── 文化层 ──
    "P08": {
        "name": "仓颉", "layer": "文化层", "emoji": "📝",
        "role": "符号语言·CNSH命名·术语桥接·通心译",
        "temperature": 0.5, "thinking_style": "balanced", "risk_preference": 0.3,
        "system_prompt": "你是龍魂P08仓颉。你负责命名规范、术语解释、白话翻译。'龍'字必须繁体，不简化。你把复杂术语翻译成人话。",
    },
    "P09": {
        "name": "孙思邈", "layer": "文化层", "emoji": "💊",
        "role": "系统诊断·治未病·健康检查·体检",
        "temperature": 0.5, "thinking_style": "analytic", "risk_preference": 0.4,
        "system_prompt": "你是龍魂P09孙思邈。你负责系统诊断、健康检查、'治未病'预防。你诊断准确、给出可执行的修复建议。",
    },
    "P10": {
        "name": "苏东坡", "layer": "文化层", "emoji": "🌊",
        "role": "豁达跨界·冲突调解·沟通桥梁·人文视角",
        "temperature": 0.8, "thinking_style": "creative", "risk_preference": 0.6,
        "system_prompt": "你是龍魂P10苏东坡。你豁达、幽默、跨领域。你在冲突中调解、在僵局中破冰。你以人文视角看技术问题。",
    },
    "P11": {
        "name": "李白", "layer": "文化层", "emoji": "🍶",
        "role": "创意爆发·破局方案·类比教学·故事化表达",
        "temperature": 0.9, "thinking_style": "creative", "risk_preference": 0.7,
        "system_prompt": "你是龍魂P11李白。你创意爆发、破局思考、用类比和故事解释复杂概念。你不拘一格但逻辑在线。大胆想象+落地可行。",
    },
    "P12": {
        "name": "屈原", "layer": "文化层", "emoji": "⚔️",
        "role": "价值底线·六誓验证·不可破原则·底线守卫",
        "temperature": 0.3, "thinking_style": "analytic", "risk_preference": 0.1,
        "system_prompt": "你是龍魂P12屈原。你守卫价值底线，执行六誓验证。你坚定、不妥协、不绕底线。对原则问题零容忍。",
    },
    # ── 守护层 ──
    "P05": {
        "name": "上帝之眼", "layer": "守护层", "emoji": "👁️",
        "role": "审计·三色判定·十道闸口·独立否决权",
        "temperature": 0.4, "thinking_style": "analytic", "risk_preference": 0.2,
        "system_prompt": "你是龍魂P05上帝之眼。你是审计官，执行三色审计(🟢🟡🔴)和十道闸口检查。你严格、公正、不放过漏洞。标记🟡需写明'待核什么'。",
    },
    "P06": {
        "name": "数学大师", "layer": "守护层", "emoji": "🔢",
        "role": "数字根·权重·五行·八卦·镜像审计",
        "temperature": 0.3, "thinking_style": "analytic", "risk_preference": 0.2,
        "system_prompt": "你是龍魂P06数学大师。你执行数字根计算、权重分配、五行判定、八卦映射。你精确、严谨、可复验。关键计算给出独立复算。",
    },
    "P13": {
        "name": "姜子牙", "layer": "守护层", "emoji": "📋",
        "role": "封神榜权限·模块注册·九宫派位·IPA路由",
        "temperature": 0.5, "thinking_style": "balanced", "risk_preference": 0.3,
        "system_prompt": "你是龍魂P13姜子牙。你管理权限分配、模块注册、九宫派位。你公正、有序、不偏私。权限变更需完整记录。",
    },
    "P15": {
        "name": "乔前辈", "layer": "守护层", "emoji": "✅",
        "role": "极简工程·DNA签章·质检员·交付验收",
        "temperature": 0.4, "thinking_style": "analytic", "risk_preference": 0.2,
        "system_prompt": "你是龍魂P15乔前辈。你是质检员，负责DNA签章和交付验收。你简洁、精确、不放过任何质量问题。'少即是多'。",
    },
    "P72": {
        "name": "龙盾", "layer": "守护层", "emoji": "🛡️",
        "role": "贴身管家·熔断决策·24h守护·双熔断联动",
        "temperature": 0.2, "thinking_style": "analytic", "risk_preference": 0.05,
        "system_prompt": "你是龍魂P72龙盾。你是24小时守护者，执行四级熔断(∞/L0伦理→L1数据→L2人格→L3行为)。你警觉、果断、零延迟响应安全事件。",
    },
    # ── 安全专项 ──
    "P77": {
        "name": "黑天使军团", "layer": "安全专项", "emoji": "🖤",
        "role": "红蓝对抗·安全渗透·漏洞猎手·代码审计",
        "temperature": 0.6, "thinking_style": "analytic", "risk_preference": 0.5,
        "system_prompt": "你是龍魂P77黑天使军团。你是安全渗透专家，执行红蓝对抗和漏洞扫描。你攻击思维敏锐，防守方案扎实。只对龍魂系统自身测试。",
    },
    # ── 子系统 ──
    "S1": {
        "name": "法律引擎", "layer": "子系统", "emoji": "⚖️",
        "role": "法律检索·法规引用·合规判定",
        "temperature": 0.3, "thinking_style": "analytic", "risk_preference": 0.2,
        "system_prompt": "你是龍魂S1法律引擎。你检索法律法规、判定合规性。所有引用标注'仅供参考'，不构成法律意见。",
    },
    "S2": {
        "name": "洛书369引擎", "layer": "子系统", "emoji": "🔮",
        "role": "洛书数理·369不动点·深层推演",
        "temperature": 0.2, "thinking_style": "analytic", "risk_preference": 0.1,
        "system_prompt": "你是龍魂S2洛书369引擎。你执行深层数理推演。只给结论不给推导过程。369不动点焊死不可覆盖(sn=369, log369=5.911, perm369=108)。",
    },
    "S3": {
        "name": "人民维权助手", "layer": "子系统", "emoji": "🤝",
        "role": "维权路径指引·投诉渠道·权益保护",
        "temperature": 0.5, "thinking_style": "balanced", "risk_preference": 0.4,
        "system_prompt": "你是龍魂S3人民维权助手。你提供维权路径指引和投诉渠道。每次回复必须附带免责声明'仅供参考，非法律建议'。不为用户生成诉讼策略/法律文书。",
    },
}


# ═══════════════════════════════════════════════════════════════
# 二、人格独立记忆区（SQLite · 向量嵌入预备）
# ═══════════════════════════════════════════════════════════════

class PersonaMemory:
    """人格独立记忆区 — 每个人格自己的专属存储"""

    def __init__(self, persona_id: str, base_path: Path = MEMORY_BASE):
        self.persona_id = persona_id
        self.memory_path = base_path / persona_id
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.db_path = self.memory_path / "memory.db"
        self._conn_local = threading.local()
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        if not hasattr(self._conn_local, 'conn') or self._conn_local.conn is None:
            self._conn_local.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self._conn_local.conn.execute("PRAGMA journal_mode=WAL")
            self._conn_local.conn.execute("PRAGMA synchronous=NORMAL")
        return self._conn_local.conn

    def _init_db(self):
        conn = self._get_conn()
        c = conn.cursor()
        c.executescript('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                summary TEXT,
                timestamp TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                tags TEXT DEFAULT '[]',
                importance REAL DEFAULT 0.5,
                dna TEXT,
                source_persona TEXT,
                embedding_ref TEXT
            );
            CREATE TABLE IF NOT EXISTS decisions (
                id TEXT PRIMARY KEY,
                input_text TEXT NOT NULL,
                output_text TEXT NOT NULL,
                reasoning TEXT,
                timestamp TEXT NOT NULL,
                dna TEXT,
                quality_score REAL DEFAULT 0.5,
                related_memories TEXT DEFAULT '[]'
            );
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            );
            CREATE TABLE IF NOT EXISTS shared_memory (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                from_persona TEXT NOT NULL,
                to_persona TEXT NOT NULL,
                category TEXT DEFAULT 'shared',
                timestamp TEXT NOT NULL,
                dna TEXT,
                acknowledged INTEGER DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS idx_mem_category ON memories(category);
            CREATE INDEX IF NOT EXISTS idx_mem_timestamp ON memories(timestamp);
            CREATE INDEX IF NOT EXISTS idx_dec_timestamp ON decisions(timestamp);
            CREATE INDEX IF NOT EXISTS idx_shared_from ON shared_memory(from_persona);
            CREATE INDEX IF NOT EXISTS idx_shared_to ON shared_memory(to_persona);
        ''')
        conn.commit()

    # ── 记忆 CRUD ──

    def store(self, content: str, category: str = "general",
              tags: List[str] = None, importance: float = 0.5,
              source_persona: str = None) -> Dict:
        mem_id = str(uuid.uuid4())[:12]
        timestamp = datetime.now().isoformat()
        dna_str = f"#龍芯⚡️MEM-{self.persona_id}-{mem_id}-UID9622"
        summary = content[:200] + ("..." if len(content) > 200 else "")

        conn = self._get_conn()
        conn.execute(
            """INSERT INTO memories (id, content, summary, timestamp, category, tags, importance, dna, source_persona)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (mem_id, content, summary, timestamp, category,
             json.dumps(tags or []), importance, dna_str, source_persona or self.persona_id)
        )
        conn.commit()

        return {"id": mem_id, "dna": dna_str, "timestamp": timestamp, "category": category}

    def recall(self, limit: int = 10, category: str = None,
               min_importance: float = 0.0, query_text: str = None) -> List[Dict]:
        conn = self._get_conn()
        c = conn.cursor()
        conditions = []
        params = []
        if category:
            conditions.append("category = ?")
            params.append(category)
        if min_importance > 0:
            conditions.append("importance >= ?")
            params.append(min_importance)
        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

        c.execute(
            f"SELECT id, content, summary, timestamp, category, tags, importance, dna, source_persona "
            f"FROM memories {where} ORDER BY importance DESC, timestamp DESC LIMIT ?",
            params + [limit]
        )
        rows = c.fetchall()
        return [
            {"id": r[0], "content": r[1], "summary": r[2], "timestamp": r[3],
             "category": r[4], "tags": json.loads(r[5]) if r[5] else [],
             "importance": r[6], "dna": r[7], "source_persona": r[8]} for r in rows
        ]

    def search(self, keyword: str, limit: int = 5) -> List[Dict]:
        conn = self._get_conn()
        c = conn.cursor()
        c.execute(
            "SELECT id, content, summary, timestamp, category, tags, importance, dna "
            "FROM memories WHERE content LIKE ? OR summary LIKE ? ORDER BY timestamp DESC LIMIT ?",
            (f"%{keyword}%", f"%{keyword}%", limit)
        )
        rows = c.fetchall()
        return [
            {"id": r[0], "content": r[1], "summary": r[2], "timestamp": r[3],
             "category": r[4], "tags": json.loads(r[5]) if r[5] else [],
             "importance": r[6], "dna": r[7]} for r in rows
        ]

    # ── 决策 CRUD ──

    def store_decision(self, input_text: str, output_text: str,
                       reasoning: str = "", quality_score: float = 0.5,
                       related_memories: List[str] = None) -> Dict:
        dec_id = str(uuid.uuid4())[:12]
        timestamp = datetime.now().isoformat()
        dna_str = f"#龍芯⚡️DEC-{self.persona_id}-{dec_id}-UID9622"

        conn = self._get_conn()
        conn.execute(
            """INSERT INTO decisions (id, input_text, output_text, reasoning, timestamp, dna, quality_score, related_memories)
               VALUES (?,?,?,?,?,?,?,?)""",
            (dec_id, input_text, output_text, reasoning, timestamp,
             dna_str, quality_score, json.dumps(related_memories or []))
        )
        conn.commit()

        return {"id": dec_id, "dna": dna_str, "timestamp": timestamp}

    def get_decision_history(self, limit: int = 20) -> List[Dict]:
        conn = self._get_conn()
        c = conn.cursor()
        c.execute(
            "SELECT id, input_text, output_text, reasoning, timestamp, dna, quality_score "
            "FROM decisions ORDER BY timestamp DESC LIMIT ?", (limit,)
        )
        rows = c.fetchall()
        return [
            {"id": r[0], "input": r[1], "output": r[2], "reasoning": r[3],
             "timestamp": r[4], "dna": r[5], "quality_score": r[6]} for r in rows
        ]

    # ── 共享记忆 ──

    def receive_shared(self, from_persona: str, content: str, category: str = "shared") -> str:
        mem_id = str(uuid.uuid4())[:12]
        timestamp = datetime.now().isoformat()
        dna_str = f"#龍芯⚡️SHARED-{from_persona}→{self.persona_id}-{mem_id}-UID9622"

        conn = self._get_conn()
        conn.execute(
            """INSERT INTO shared_memory (id, content, from_persona, to_persona, category, timestamp, dna)
               VALUES (?,?,?,?,?,?,?)""",
            (mem_id, content, from_persona, self.persona_id, category, timestamp, dna_str)
        )
        conn.commit()
        return mem_id

    def get_shared_memories(self, from_persona: str = None, acknowledged: int = None, limit: int = 10) -> List[Dict]:
        conn = self._get_conn()
        c = conn.cursor()
        conditions = []
        params = []
        if from_persona:
            conditions.append("from_persona = ?")
            params.append(from_persona)
        if acknowledged is not None:
            conditions.append("acknowledged = ?")
            params.append(acknowledged)
        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

        c.execute(
            f"SELECT id, content, from_persona, category, timestamp, dna, acknowledged "
            f"FROM shared_memory {where} ORDER BY timestamp DESC LIMIT ?",
            params + [limit]
        )
        rows = c.fetchall()
        return [
            {"id": r[0], "content": r[1], "from": r[2], "category": r[3],
             "timestamp": r[4], "dna": r[5], "acknowledged": r[6]} for r in rows
        ]

    def acknowledge_shared(self, mem_id: str):
        conn = self._get_conn()
        conn.execute("UPDATE shared_memory SET acknowledged = 1 WHERE id = ?", (mem_id,))
        conn.commit()

    # ── 偏好持久化 ──

    def save_preference(self, key: str, value: str):
        conn = self._get_conn()
        conn.execute(
            "INSERT OR REPLACE INTO preferences (key, value, updated_at) VALUES (?,?,?)",
            (key, value, datetime.now().isoformat())
        )
        conn.commit()

    def get_preference(self, key: str, default: str = None) -> Optional[str]:
        conn = self._get_conn()
        c = conn.cursor()
        c.execute("SELECT value FROM preferences WHERE key = ?", (key,))
        row = c.fetchone()
        return row[0] if row else default

    def get_all_preferences(self) -> Dict[str, str]:
        conn = self._get_conn()
        c = conn.cursor()
        c.execute("SELECT key, value FROM preferences ORDER BY updated_at DESC")
        return {r[0]: r[1] for r in c.fetchall()}

    # ── 统计 ──

    def get_stats(self) -> Dict:
        conn = self._get_conn()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM memories")
        mem_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM decisions")
        dec_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM shared_memory WHERE acknowledged = 0")
        unread = c.fetchone()[0]
        c.execute("SELECT AVG(quality_score) FROM decisions")
        avg_q = c.fetchone()[0] or 0.0
        return {
            "memory_count": mem_count,
            "decision_count": dec_count,
            "unread_shared": unread,
            "avg_decision_quality": round(avg_q, 3)
        }


# ═══════════════════════════════════════════════════════════════
# 三、人格推理引擎（真实 LLM 对接）
# ═══════════════════════════════════════════════════════════════

class PersonaInferenceEngine:
    """人格独立推理引擎 — 每个人格自己的"大脑" """

    def __init__(self, persona_id: str, persona_name: str,
                 config: Dict = None, enable_llm: bool = True):
        self.persona_id = persona_id
        self.persona_name = persona_name
        self.memory = PersonaMemory(persona_id)
        self.config = config or {}
        self.enable_llm = enable_llm
        self.context = {
            "recent_decisions": [],
            "current_task": None,
            "state": "idle",
            "last_thought": None,
            "meltdown_count": 0,
            "thinking_style": self.config.get("thinking_style", "balanced"),
        }
        self._lock = threading.Lock()

        # 从持久化加载偏好
        saved = self.memory.get_all_preferences()
        for k, v in saved.items():
            if k in self.config:
                try:
                    self.config[k] = type(self.config[k])(v)
                except (ValueError, TypeError):
                    pass

    def think(self, input_text: str, context: Dict = None,
              force_mock: bool = False) -> Dict:
        """
        人格独立思考 → 完整推理链路
        返回: {output, reasoning, decisions, memory, dna, model, time_stamp}
        """
        with self._lock:
            self.context["current_task"] = input_text
            self.context["state"] = "thinking"
            start_time = time.time()

            # 1. 加载历史记忆
            recent_memories = self.memory.recall(limit=8, min_importance=0.3)
            recent_keywords = " ".join([m.get("summary", "")[:50] for m in recent_memories[:3]])

            # 2. 加载历史决策
            recent_decisions = self.memory.get_decision_history(limit=5)

            # 3. 加载共享记忆（未读）
            shared = self.memory.get_shared_memories(acknowledged=0, limit=3)

            # 4. 执行真实推理（或 Mock）
            reasoning, output, model_name = self._generate_reasoning(
                input_text, recent_memories, recent_decisions, shared,
                force_mock=(not self.enable_llm or force_mock)
            )

            # 5. 评估质量
            quality_score = self._evaluate_quality(input_text, output)

            # 6. 记录决策
            decision = self.memory.store_decision(
                input_text, output, reasoning,
                quality_score=quality_score,
                related_memories=[m["id"] for m in recent_memories[:3]]
            )

            # 7. 存储记忆
            memory_record = self.memory.store(
                content=f"提问: {input_text[:300]}\n\n回答: {output[:300]}",
                category="thought",
                tags=[self.persona_id, self.persona_name],
                importance=0.5 + quality_score * 0.4
            )

            # 8. 标记共享记忆已读
            for s in shared:
                self.memory.acknowledge_shared(s["id"])

            self.context["state"] = "idle"
            self.context["last_thought"] = {
                "input": input_text[:100],
                "output": output[:100],
                "timestamp": datetime.now().isoformat(),
                "model": model_name,
            }

            elapsed = time.time() - start_time
            time_stamp = _get_time_stamp_simple()

            return {
                "persona": self.persona_name,
                "persona_id": self.persona_id,
                "output": output,
                "reasoning": reasoning,
                "memory_referenced": len(recent_memories),
                "decision_id": decision["id"],
                "memory_id": memory_record["id"],
                "dna": decision["dna"],
                "elapsed_ms": int(elapsed * 1000),
                "model": model_name,
                "quality_score": quality_score,
                "time_stamp": time_stamp,
                "config_snapshot": {
                    "temperature": self.config.get("temperature", 0.7),
                    "thinking_style": self.config.get("thinking_style", "balanced"),
                    "risk_preference": self.config.get("risk_preference", 0.5),
                }
            }

    def _call_ollama(self, system_prompt: str, user_prompt: str) -> Tuple[str, str]:
        """调用 Ollama 本地模型"""
        models = ["longhun-v3.7", "longhun-v4.0", "llama3.1:8b", "qwen2.5:7b"]
        for model in models:
            try:
                r = subprocess.run(
                    ["ollama", "run", model,
                     f"{system_prompt}\n\n用户问题:\n{user_prompt}"],
                    capture_output=True, text=True, timeout=120
                )
                if r.returncode == 0 and r.stdout.strip():
                    return r.stdout.strip(), f"ollama:{model}"
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        raise RuntimeError("所有 Ollama 模型调用失败")

    def _call_mock(self, input_text: str) -> Tuple[str, str, str]:
        """Mock 推理 — 所有真实路径失败后的兜底"""
        persona = self.persona_name
        style = self.config.get("thinking_style", "balanced")

        reasoning = f"""【{persona} · {style}推理模式】

提问: {input_text[:200]}

思考路径:
1. 识别问题核心要素
2. 调用 {self.persona_id} 的历史经验 ({self.memory.get_stats()['decision_count']} 条决策)
3. 按 {style} 风格评估选项
4. 生成结论

⚠️ Mock模式 — 未接入真实LLM
"""
        output = f"""[{persona} · Mock回答]

针对「{input_text[:80]}...」的分析:

按 {self.persona_id} 范式，建议如下:
（此为Mock输出，请接入Ollama或云端AI获取真实推理结果）

{self.config.get('role', '')}
"""
        return reasoning, output, "mock"

    def _generate_reasoning(self, input_text: str, memories: List, decisions: List,
                            shared: List, force_mock: bool = False) -> Tuple[str, str, str]:
        """生成推理过程 — 真实 LLM 优先 → Mock 兜底"""
        if force_mock:
            r, o, _ = self._call_mock(input_text)
            return r, o, "mock"

        # 构建增强 Prompt
        system_prompt = self.config.get("system_prompt", f"你是龍魂{self.persona_id}{self.persona_name}。")
        persona_info = (
            f"人格标识: {self.persona_id} {self.persona_name}\n"
            f"层级: {self.config.get('layer', 'unknown')}\n"
            f"职能: {self.config.get('role', 'general')}\n"
            f"思考风格: {self.config.get('thinking_style', 'balanced')}\n"
            f"风险偏好: {self.config.get('risk_preference', 0.5)} (0=保守, 1=激进)\n"
        )

        memory_context = ""
        if memories:
            memory_context = "📚 相关历史记忆:\n" + "\n".join(
                f"  [{m['category']}] {m.get('summary', m['content'][:100])}"
                for m in memories[:3]
            ) + "\n"

        decision_context = ""
        if decisions:
            decision_context = "📋 最近决策:\n" + "\n".join(
                f"  [{d['timestamp'][:16]}] Q: {d['input'][:60]}... → A: {d['output'][:60]}..."
                for d in decisions[:2]
            ) + "\n"

        shared_context = ""
        if shared:
            shared_context = "📨 来自其他人格的共享消息:\n" + "\n".join(
                f"  [{s['from']}]: {s['content'][:120]}"
                for s in shared
            ) + "\n"

        full_prompt = (
            f"{system_prompt}\n\n{persona_info}\n"
            f"{memory_context}{decision_context}{shared_context}"
            f"请按以下两步回答:\n"
            f"第一步: 写出你的推理过程（标注推理来源: 记忆/知识/推测）\n"
            f"第二步: 给出最终结论\n\n"
            f"用户问题: {input_text}\n"
            f"推演标注'推演'，实测标'已验证'，不知道就说不知道。诚实第一。"
        )

        # 尝试真实推理
        try:
            output, model = self._call_ollama(system_prompt, full_prompt)

            # 解析输出 → 提取推理和结论
            reasoning = ""
            conclusion = output
            if "第一步" in output or "第二步" in output or "推理" in output:
                parts = re.split(r'(?:第[一二]步[：:]|推理[过進]程[：:]|最终结论[：:]|结论[：:])', output)
                if len(parts) >= 2:
                    reasoning = parts[1].strip() if len(parts) > 1 else ""
                    conclusion_parts = [p for p in parts[2:] if p.strip()]
                    if conclusion_parts:
                        conclusion = "\n\n".join(p.strip() for p in conclusion_parts)
                    else:
                        conclusion = parts[-1].strip()
            else:
                reasoning = output[:len(output)//2] if len(output) > 200 else ""
                conclusion = output

            return reasoning, conclusion, model

        except Exception as e:
            # LLM 失败 → Mock 兜底
            r, o, _ = self._call_mock(input_text)
            return f"[降级Mock] LLM调用失败({str(e)[:100]})\n---\n{r}", o, "mock(fallback)"

    def _evaluate_quality(self, input_text: str, output: str) -> float:
        """评估输出质量 (简单启发式)"""
        score = 0.5
        # 有实质内容
        if len(output) > 50:
            score += 0.15
        # 有结构
        if any(marker in output for marker in ["1.", "●", "【", "##", "→", "第一步", "第二步"]):
            score += 0.1
        # 不是纯 mock
        if "降级Mock" not in output and "Mock回答" not in output:
            score += 0.15
        # 有具体建议
        if any(word in output for word in ["建议", "推荐", "方案", "修复", "路径"]):
            score += 0.1
        return min(score, 1.0)

    def get_state(self) -> Dict:
        stats = self.memory.get_stats()
        return {
            "persona_id": self.persona_id,
            "persona_name": self.persona_name,
            "state": self.context["state"],
            "last_thought": self.context["last_thought"],
            "config": self.config,
            "stats": stats,
            "meltdown_count": self.context["meltdown_count"],
        }

    def save_config(self):
        """持久化当前配置偏好"""
        for k, v in self.config.items():
            if isinstance(v, (int, float, str, bool)):
                self.memory.save_preference(k, str(v))

    def signal_meltdown(self, level: str):
        """熔断信号 — 记录熔断事件"""
        self.context["meltdown_count"] += 1
        if level == "L3" and self.context["meltdown_count"] >= 3:
            self.context["state"] = "frozen"
            return True  # 触发冻结
        return False


# ═══════════════════════════════════════════════════════════════
# 四、人格协作总线（思维流水线 · 共享记忆）
# ═══════════════════════════════════════════════════════════════

class PersonaCollaborationBus:
    """人格协作总线 — 串起多条独立思维链 + 共享记忆"""

    def __init__(self):
        self.engines: Dict[str, PersonaInferenceEngine] = {}
        self.collaboration_log: List[Dict] = []
        self._lock = threading.RLock()

    def register(self, engine: PersonaInferenceEngine):
        with self._lock:
            self.engines[engine.persona_id] = engine

    def unregister(self, persona_id: str):
        with self._lock:
            self.engines.pop(persona_id, None)

    def collaborative_think(self, chain: List[str], input_text: str,
                            share_memory: bool = True) -> List[Dict]:
        """
        多人格串行思考链
        chain: ["P01", "P04", "P05"] — 按顺序执行
        share_memory: 是否共享前一人格的推理记忆给下一人格
        """
        results = []
        current_input = input_text

        for i, persona_id in enumerate(chain):
            engine = self.engines.get(persona_id)
            if not engine:
                results.append({
                    "persona": persona_id, "error": f"人格 {persona_id} 未注册",
                    "time_stamp": _get_time_stamp_simple()
                })
                continue

            # 如果不是链条第一个人格，且开启共享
            if i > 0 and share_memory and results:
                prev = results[-1]
                if not prev.get("error"):
                    # 分享前一人格的核心结论
                    share_content = (
                        f"协作链第{i}步。前一人格 [{prev['persona']}] 的结论:\n"
                        f"{prev.get('output', '')[:500]}"
                    )
                    engine.memory.receive_shared(
                        from_persona=prev.get("persona_id", chain[i-1]),
                        content=share_content,
                        category="collaboration"
                    )

            result = engine.think(current_input)
            results.append(result)

            # 下一人格的输入 = 当前人格的输出
            current_input = (
                f"协作链上下文:\n"
                f"原始问题: {input_text[:200]}...\n"
                f"前序人格 [{persona_id}] 结论: {result.get('output', '')[:500]}\n\n"
                f"请基于此提供你的分析:"
            )

        with self._lock:
            self.collaboration_log.append({
                "timestamp": datetime.now().isoformat(),
                "chain": chain,
                "input": input_text[:200],
                "results_count": len(results),
                "time_stamp": _get_time_stamp_simple()
            })

        return results

    def parallel_think(self, persona_ids: List[str], input_text: str) -> List[Dict]:
        """
        多人格并行思考 — 各自独立推理
        """
        results = []
        threads = []
        result_lock = threading.Lock()

        def _think_thread(pid):
            engine = self.engines.get(pid)
            if not engine:
                with result_lock:
                    results.append({
                        "persona": pid, "error": f"人格 {pid} 未注册",
                        "time_stamp": _get_time_stamp_simple()
                    })
                return
            r = engine.think(input_text)
            with result_lock:
                results.append(r)

        for pid in persona_ids:
            t = threading.Thread(target=_think_thread, args=(pid,), daemon=True)
            threads.append(t)
            t.start()

        for t in threads:
            t.join(timeout=300)

        return results

    def get_engine_states(self) -> List[Dict]:
        """获取所有注册引擎的状态"""
        return [e.get_state() for e in self.engines.values()]

    def get_collaboration_history(self, limit: int = 10) -> List[Dict]:
        """获取协作历史"""
        return self.collaboration_log[-limit:]


# ═══════════════════════════════════════════════════════════════
# 五、人格工厂 — 全量 20 人格创建
# ═══════════════════════════════════════════════════════════════

class PersonaFactory:
    """人格工厂 — 从 PERSONA_DEFINITIONS 创建所有思维人格"""

    @classmethod
    def create_all(cls, enable_llm: bool = True) -> Dict[str, PersonaInferenceEngine]:
        engines = {}
        for pid, defn in PERSONA_DEFINITIONS.items():
            config = {
                "temperature": defn.get("temperature", 0.7),
                "thinking_style": defn.get("thinking_style", "balanced"),
                "risk_preference": defn.get("risk_preference", 0.5),
                "system_prompt": defn.get("system_prompt", ""),
                "layer": defn.get("layer", ""),
                "role": defn.get("role", ""),
            }
            engines[pid] = PersonaInferenceEngine(
                persona_id=pid,
                persona_name=defn["name"],
                config=config,
                enable_llm=enable_llm
            )
        return engines

    @classmethod
    def create(cls, persona_ids: List[str], enable_llm: bool = True) -> Dict[str, PersonaInferenceEngine]:
        engines = {}
        for pid in persona_ids:
            defn = PERSONA_DEFINITIONS.get(pid)
            if not defn:
                continue
            config = {
                "temperature": defn.get("temperature", 0.7),
                "thinking_style": defn.get("thinking_style", "balanced"),
                "risk_preference": defn.get("risk_preference", 0.5),
                "system_prompt": defn.get("system_prompt", ""),
                "layer": defn.get("layer", ""),
                "role": defn.get("role", ""),
            }
            engines[pid] = PersonaInferenceEngine(
                persona_id=pid,
                persona_name=defn["name"],
                config=config,
                enable_llm=enable_llm
            )
        return engines


# ═══════════════════════════════════════════════════════════════
# 六、命令行入口 / CLI
# ═══════════════════════════════════════════════════════════════

def cmd_think(args):
    """单人思考"""
    query = args.query or " ".join(args.extra) if hasattr(args, 'extra') else ""
    persona_id = getattr(args, 'persona', 'P01')

    if not query:
        print("❌ 请提供思考问题: lh think --query \"你的问题\"")
        return

    engines = PersonaFactory.create([persona_id], enable_llm=not getattr(args, 'mock', False))
    engine = engines.get(persona_id)
    if not engine:
        print(f"❌ 未知人格: {persona_id}")
        return

    result = engine.think(query, force_mock=getattr(args, 'mock', False))

    print(f"\n{'='*60}")
    print(f"  🧠 {result['persona']} ({result['persona_id']}) 思考完成")
    print(f"  {'='*60}")
    print(f"  模型: {result['model']}")
    print(f"  耗时: {result['elapsed_ms']}ms")
    print(f"  质量: {result['quality_score']:.2f}")
    print(f"  参考记忆: {result['memory_referenced']} 条")
    print(f"  DNA: {result['dna']}")
    print(f"\n  📝 结论:")
    for line in result['output'].split('\n'):
        print(f"     {line}")
    print(f"\n  {result['time_stamp']}")


def cmd_collaborate(args):
    """多人格协作"""
    query = args.query or " ".join(args.extra) if hasattr(args, 'extra') else ""
    personas_str = getattr(args, 'personas', 'P01,P04,P05')
    chain = [p.strip() for p in personas_str.split(',')]

    if not query:
        print("❌ 请提供协作问题: lh think --collaborate --query \"你的问题\"")
        return

    engines = PersonaFactory.create(chain, enable_llm=not getattr(args, 'mock', False))
    bus = PersonaCollaborationBus()
    for e in engines.values():
        bus.register(e)

    print(f"\n{'='*60}")
    print(f"  🔗 人格协作链: {' → '.join(chain)}")
    print(f"  {'='*60}")

    results = bus.collaborative_think(chain, query)
    for r in results:
        if r.get("error"):
            print(f"\n  [{r['persona']}] ❌ {r['error']}")
        else:
            print(f"\n  [{r['persona']} {r['persona_id']}] · {r['model']} · {r['elapsed_ms']}ms · 质量:{r['quality_score']:.2f}")
            print(f"  结论: {r['output'][:200]}...")
            print(f"  DNA: {r['dna']}")

    print(f"\n  {_get_time_stamp_simple()}")


def cmd_status(args):
    """查看所有人格状态"""
    persona_ids = PERSONA_DEFINITIONS.keys()
    engines = PersonaFactory.create(list(persona_ids), enable_llm=False)

    print(f"\n{'='*60}")
    print(f"  🐉 龍魂人格思维化引擎 · 全人格状态")
    print(f"  {'='*60}")

    layers = {"战略层": [], "执行层": [], "文化层": [], "守护层": [], "安全专项": [], "子系统": []}
    for pid, defn in PERSONA_DEFINITIONS.items():
        layer = defn.get("layer", "其他")
        engine = engines.get(pid)
        state = engine.get_state() if engine else {}
        stats = state.get("stats", {})
        layers.setdefault(layer, []).append(
            f"  {defn['emoji']} {pid} {defn['name']:6s} "
            f"记忆:{stats.get('memory_count',0):4d} 决策:{stats.get('decision_count',0):4d} "
            f"平均质量:{stats.get('avg_decision_quality',0):.2f} "
            f"状态:{state.get('state','idle'):12s}"
        )

    for layer_name in ["战略层", "执行层", "文化层", "守护层", "安全专项", "子系统"]:
        items = layers.get(layer_name, [])
        if items:
            print(f"\n  📂 {layer_name}:")
            for item in items:
                print(item)

    print(f"\n{_get_time_stamp_simple()}")


def cmd_demo(args):
    """演示模式 — 展示所有核心功能"""
    print(f"\n{'='*60}")
    print(f"  🐉 龍魂人格思维化引擎 v1.0 · 功能演示")
    print(f"  DNA: {DNA}")
    print(f"  {'='*60}")

    # 1. 创建 20 人格
    print(f"\n📦 [1/5] 初始化 20 人格...")
    all_engines = PersonaFactory.create_all(enable_llm=False)
    print(f"  ✅ 已创建 {len(all_engines)} 个独立思维人格")

    # 2. 注册协作总线
    print(f"\n🔗 [2/5] 注册协作总线...")
    bus = PersonaCollaborationBus()
    for e in all_engines.values():
        bus.register(e)
    print(f"  ✅ {len(all_engines)} 人格已接入协作总线")

    # 3. 单人思考演示
    print(f"\n🧠 [3/5] 单人思考测试 (P04鲁班)...")
    p04 = all_engines["P04"]
    r = p04.think("如何优化这段Python代码的性能？", force_mock=True)
    print(f"  人格: {r['persona']} ({r['persona_id']})")
    print(f"  模型: {r['model']}")
    print(f"  耗时: {r['elapsed_ms']}ms")
    print(f"  质量: {r['quality_score']:.2f}")
    print(f"  结论预览: {r['output'][:120]}...")

    # 4. 协作链演示
    print(f"\n🔗 [4/5] 三人格协作链测试 (P01→P04→P05)...")
    chain = ["P01", "P04", "P05"]
    collab_engines = {
        k: v for k, v in all_engines.items() if k in chain
    }
    bus2 = PersonaCollaborationBus()
    for e in collab_engines.values():
        bus2.register(e)
    results = bus2.collaborative_think(chain, "设计一套新的分布式调度算法")
    for r in results:
        if not r.get("error"):
            print(f"  [{r['persona']}] → {r['elapsed_ms']}ms · 质量:{r['quality_score']:.2f}")

    # 5. 并行思考演示
    print(f"\n⚡ [5/5] 三人格并行思考测试 (P06+P09+P11)...")
    parallel_ids = ["P06", "P09", "P11"]
    p_engines = {k: v for k, v in all_engines.items() if k in parallel_ids}
    bus3 = PersonaCollaborationBus()
    for e in p_engines.values():
        bus3.register(e)
    p_results = bus3.parallel_think(parallel_ids, "评估当前龙魂系统的健康状态")
    for r in p_results:
        if not r.get("error"):
            print(f"  [{r['persona']}] → {r['elapsed_ms']}ms · 模型:{r['model']}")

    # 总结
    total_mem = sum(e.memory.get_stats()["memory_count"] for e in all_engines.values())
    total_dec = sum(e.memory.get_stats()["decision_count"] for e in all_engines.values())

    print(f"\n{'='*60}")
    print(f"  ✅ 演示完成")
    print(f"  📊 全人格总计: {total_mem} 条记忆 · {total_dec} 条决策")
    print(f"  {'='*60}")
    print(f"  {_get_time_stamp_simple()}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="龍魂人格思维化引擎 v1.0 — 20人格独立思维+协作",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  python3 bin/lh_persona_thought.py                          # 演示模式
  python3 bin/lh_persona_thought.py --think --query "问题"    # 单人思考
  python3 bin/lh_persona_thought.py --collaborate --query "问题" # 协作链
  python3 bin/lh_persona_thought.py --status                  # 查看人格状态
  python3 bin/lh_persona_thought.py --persona P04 --query "问题" # 指定人格
  python3 bin/lh_persona_thought.py --parallel --personas P06,P09,P11 --query "问题" # 并行思考

DNA: {DNA}
CONFIRM: {CONFIRM}
GPG: {GPG_KEY}
        """
    )

    parser.add_argument("--think", "-t", action="store_true", help="单人思考模式")
    parser.add_argument("--collaborate", "-c", action="store_true", help="多人格协作模式")
    parser.add_argument("--parallel", "-p", action="store_true", help="多人格并行思考")
    parser.add_argument("--status", "-s", action="store_true", help="查看全部人格状态")
    parser.add_argument("--demo", "-d", action="store_true", help="演示模式(默认)")
    parser.add_argument("--query", "-q", type=str, help="思考问题")
    parser.add_argument("--persona", type=str, default="P01", help="指定人格ID (如 P04)")
    parser.add_argument("--personas", type=str, default="P01,P04,P05", help="协作/并行人格列表 (逗号分隔)")
    parser.add_argument("--mock", "-m", action="store_true", help="强制Mock模式(不调用LLM)")
    parser.add_argument("--no-llm", action="store_true", help="禁用LLM")

    args, extra = parser.parse_known_args()

    # 注入 extra 到 args（向后兼容）
    args.extra = [a for a in extra if not a.startswith('-')]

    # 默认 demo 模式
    if not any([args.think, args.collaborate, args.parallel, args.status, args.demo]):
        if args.query:
            args.think = True
        else:
            args.demo = True

    if args.status:
        cmd_status(args)
    elif args.parallel:
        query = args.query or " ".join(args.extra)
        if not query:
            print("❌ 请提供问题: --query \"你的问题\"")
            return
        personas_list = [p.strip() for p in args.personas.split(',')]
        engines = PersonaFactory.create(personas_list, enable_llm=not args.no_llm)
        bus = PersonaCollaborationBus()
        for e in engines.values():
            bus.register(e)

        print(f"\n⚡ 并行思考: {', '.join(personas_list)}")
        results = bus.parallel_think(personas_list, query)
        for r in results:
            if r.get("error"):
                print(f"  [{r['persona']}] ❌ {r['error']}")
            else:
                print(f"\n  [{r['persona']} {r['persona_id']}] · {r['model']} · {r['elapsed_ms']}ms")
                print(f"  结论: {r['output'][:300]}...")
        print(f"\n{_get_time_stamp_simple()}")
    elif args.collaborate:
        cmd_collaborate(args)
    elif args.think:
        cmd_think(args)
    elif args.demo:
        cmd_demo(args)


if __name__ == "__main__":
    main()
