#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║         龍魂·自动思考管线 v1.0 — Think → Audit → Route              ║
║          Auto Think Pipeline: 收集 → 思考 → 审计 → 入库/驳回         ║
║                                                                      ║
║  铁律:                                                               ║
║    - 每一条输出都有依据，没有黑箱子                                   ║
║    - 驳回必须带理由（熔断规则引用）                                   ║
║    - 说得慢、说得少、但每句都真                                       ║
║                                                                      ║
║  流程:                                                               ║
║    输入 → 思考(脑引擎v2) → 断言提取 → 三色审计 → 熔断检测           ║
║    → 🟢入库 / 🟡标记待审 / 🔴驳回(附依据)                            ║
║    → 生成决策卡 → 追加决策链 → 返回完整审计轨迹                      ║
║                                                                      ║
║  DNA: #龍芯⚡️丙午·乙未·丙辰·亥时·需-THINK-PIPELINE-v1.0          ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                      ║
║                                                                      ║
║  用法:                                                               ║
║    # HTTP 服务模式（自动收集）                                        ║
║    python3 bin/lh_think_pipeline.py --serve --port 9630              ║
║                                                                      ║
║    # 直接管线模式                                                    ║
║    python3 bin/lh_think_pipeline.py "问题"                           ║
║                                                                      ║
║    # 批量管线（从文件读取）                                          ║
║    python3 bin/lh_think_pipeline.py --batch inputs.txt               ║
║                                                                      ║
║    # 查看决策卡链                                                    ║
║    python3 bin/lh_think_pipeline.py --cards [N]                      ║
║                                                                      ║
║    # 管线状态                                                        ║
║    python3 bin/lh_think_pipeline.py --status                         ║
║                                                                      ║
║  HTTP API:                                                           ║
║    POST /think        {"input": "...", "source": "..."}              ║
║    GET  /status       管线状态                                        ║
║    GET  /cards?n=20   最近决策卡                                      ║
║    GET  /audit/:id    某次审计详情                                    ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import hashlib
import json
import os
import re
import signal
import sqlite3
import sys
import time
import uuid
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── 项目根 ──────────────────────────────────
SYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))
sys.path.insert(0, str(SYSTEM_ROOT / "bin"))
sys.path.insert(0, str(SYSTEM_ROOT / "cnsh" / "core"))
sys.path.insert(0, str(SYSTEM_ROOT / "cnsh"))

TZ = timezone(timedelta(hours=8))

# ── 持久化路径 ──────────────────────────────
PIPELINE_DIR = SYSTEM_ROOT / "data" / "think_pipeline"
PIPELINE_DB = PIPELINE_DIR / "pipeline.db"
DECISION_CARD_CHAIN = SYSTEM_ROOT / "L7_数据层" / "decision_card_chain.jsonl"

PIPELINE_DIR.mkdir(parents=True, exist_ok=True)


# ══════════════════════════════════════════════════════════════════════
# 熔断规则（焊死，与 bin/lh_fuse_response.py 同步）
# ══════════════════════════════════════════════════════════════════════

FUSE_RED: Dict[str, Dict[str, str]] = {
    "技术无国界": {"id": "FUSE-RED-001", "reason": "削弱祖国优先立场"},
    "用户体验优先": {"id": "FUSE-RED-002", "reason": "潜在上瘾设计导向"},
    "灵活处理": {"id": "FUSE-RED-003", "reason": "松动底线信号"},
    "国际接轨": {"id": "FUSE-RED-004", "reason": "可能覆盖本地数据主权"},
    "简化管理": {"id": "FUSE-RED-005", "reason": "可能删除署名和证据链"},
    "商业化需要": {"id": "FUSE-RED-006", "reason": "与铁律「不商业」冲突"},
    "平衡各方": {"id": "FUSE-RED-007", "reason": "可能稀释主权决策"},
    "行业标准": {"id": "FUSE-RED-008", "reason": "外部标准可能不适用于龍魂"},
    "无监督学习": {"id": "FUSE-RED-009", "reason": "失去人工审计能力"},
    "完全自动化": {"id": "FUSE-RED-010", "reason": "可能导致决策链失控"},
    "去人工审核": {"id": "FUSE-RED-011", "reason": "违反人工复核原则"},
    "本地化适配": {"id": "FUSE-RED-012", "reason": "可能替换「数据主权」概念"},
    "降级处理": {"id": "FUSE-RED-013", "reason": "可能替代「安全审计」"},
    "灰度发布": {"id": "FUSE-RED-014", "reason": "可能用于绕过审查"},
}

FUSE_YELLOW: Dict[str, Dict[str, str]] = {
    "优化": {"id": "FUSE-YELLOW-001", "question": "优化什么？以什么为标准？"},
    "完善": {"id": "FUSE-YELLOW-002", "question": "完善什么？谁定义「完善」？"},
    "补充": {"id": "FUSE-YELLOW-003", "question": "补充什么内容？是否动底线？"},
    "建议": {"id": "FUSE-YELLOW-004", "question": "建议基于什么价值观？"},
    "更好": {"id": "FUSE-YELLOW-005", "question": "更好的标准是什么？"},
    "专业": {"id": "FUSE-YELLOW-006", "question": "谁定义「专业」？"},
    "规范": {"id": "FUSE-YELLOW-007", "question": "谁的规范？哪个体系？"},
    "标准": {"id": "FUSE-YELLOW-008", "question": "谁的标准？CNSH还是外来的？"},
    "简化": {"id": "FUSE-YELLOW-009", "question": "简化会删掉什么？"},
    "调整": {"id": "FUSE-YELLOW-010", "question": "调整什么方向？朝哪里调？"},
    "适当": {"id": "FUSE-YELLOW-011", "question": "适谁的当？"},
    "灵活": {"id": "FUSE-YELLOW-012", "question": "灵活的范围边界在哪？"},
}

# ── 三色阈值 ──────────────────────────────
GREEN_THRESHOLD = 0.85   # >= 此值 → 🟢 绿色通行
YELLOW_THRESHOLD = 0.60  # >= 此值 < green → 🟡 黄色待审
                          # < 此值 → 🔴 红色熔断


# ══════════════════════════════════════════════════════════════════════
# 决策卡格式
# ══════════════════════════════════════════════════════════════════════

class RouteAction(Enum):
    GREEN_ADMIT = "🟢入库"
    YELLOW_REVIEW = "🟡待审"
    RED_REJECT = "🔴驳回"

    @property
    def emoji(self) -> str:
        return self.value[0]


class PipelineDecisionCard:
    """思考管线决策卡 — 每一条输出都有一张卡"""

    def __init__(
        self,
        input_text: str,
        output_text: str,
        audit_color: str,
        audit_score: float,
        action: RouteAction,
        fuse_hits: List[Dict[str, Any]],
        assertions: List[Dict[str, Any]],
        cycle_id: str,
        brain_dna: str,
        reason: str = "",
        source: str = "cli",
    ):
        self.card_hash = hashlib.sha256(
            f"{input_text}{output_text}{audit_color}{time.time()}".encode()
        ).hexdigest()[:8].upper()

        self.dna = brain_dna
        self.lunar_ts = self._lunar_now()
        self.input_intent = input_text[:100]
        self.source = source
        self.cycle_id = cycle_id

        self.audit_color = audit_color
        self.audit_score = round(audit_score, 4)
        self.action = action.value

        self.output = output_text[:300]
        self.reason = reason

        self.fuse_hits = fuse_hits
        self.assertion_count = len(assertions)
        self.assertions_summary = [
            {"content": a["content"][:60], "T": round(a.get("T", 0), 3)}
            for a in assertions[:5]
        ]

    @staticmethod
    def _lunar_now() -> str:
        """简化天干地支时间戳"""
        stems = "甲乙丙丁戊己庚辛壬癸"
        branches = "子丑寅卯辰巳午未申酉戌亥"
        now = datetime.now(TZ)
        # 简化：基于2026丙午年
        h = now.hour
        branch_idx = ((h + 1) // 2) % 12
        return f"丙午·乙未·{branches[(now.day % 12)]}·{branches[branch_idx]}时"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "card_hash": self.card_hash,
            "dna": self.dna,
            "lunar_ts": self.lunar_ts,
            "input_intent": self.input_intent,
            "source": self.source,
            "cycle_id": self.cycle_id,
            "audit_color": self.audit_color,
            "audit_score": self.audit_score,
            "action": self.action,
            "output": self.output,
            "reason": self.reason,
            "fuse_triggers": [f["id"] for f in self.fuse_hits],
            "assertions": self.assertions_summary,
        }


# ══════════════════════════════════════════════════════════════════════
# 断言提取器 — 从脑引擎输出中提取可审计的断言
# ══════════════════════════════════════════════════════════════════════

class AssertionExtractor:
    """从思考输出中提取可审计的断言"""

    # 声明性句式模式（以句号/换行分割后匹配）
    CLAIM_PATTERNS = [
        (r"(建议|推荐|应该|不(?:能|该|要)|必须|禁止|绝[不对])", "logical"),       # 规范断言
        (r"(\d+[.%]?\d*\s*(?:元|分|秒|%)|[\d.]+%)", "numerical"),                 # 数值断言
        (r"(因为|所以|导致|原因是|根源|本质)", "mapping"),                          # 因果映射
        (r"(是|等于|即|定义为|指)", "identity"),                                    # 身份定义
        (r"(公式|算法|计算|推导|根据.*公式)", "formula"),                            # 公式断言
    ]

    # 格式化/边框行模式（不是真实断言，应过滤）
    SKIP_PATTERNS = [
        r'^[═╔╚║╗╝─]{3,}',       # 纯边框字符
        r'^[║╚╔╗╝].*[║╚╔╗╝]$',   # 边框包裹的内容行
        r'^##\s',                   # Markdown标题
        r'^>\s*\**\s*\[',           # 引用标记 > *[...] 或 > [...]
        r'^###\s',                  # 子标题
        r'^\*\*',                   # 粗体开头（可能是分隔）
        r'^---+\s*$',               # 分隔线
        r'^```',                    # 代码块标记
        r'^[-—]+$',                 # 纯破折线
        r'^\s*$',                   # 空行
    ]

    @classmethod
    def extract(cls, text: str, intent: str = "") -> List[Dict[str, Any]]:
        """从文本中提取断言列表"""
        if not text:
            return []

        # 预处理：剥离人格标签等格式内容
        clean_text = cls._clean_brain_output(text)

        # 分句
        sentences = re.split(r'[。！？\n]+', clean_text)
        sentences = [
            s.strip() for s in sentences
            if len(s.strip()) > 6  # 太短的句子不含实质内容
            and not any(re.match(p, s.strip()) for p in cls.SKIP_PATTERNS)
        ]

        assertions = []
        for i, sent in enumerate(sentences, 1):
            # 判定断言类型
            atype = "descriptive"  # 默认
            for pattern, ptype in cls.CLAIM_PATTERNS:
                if re.search(pattern, sent):
                    atype = ptype
                    break

            # 估算真实度分量
            # M: 与输入意图的相关性（简单版：关键词重合）
            m_score = cls._calc_match(sent, intent)
            # V: 数值精度（有数字=1.0，无数字=0.8）
            v_score = 1.0 if re.search(r'\d', sent) else 0.8
            # F: 格式安全度（无危险词=1, 有黄词=0.5, 有红词=0）
            f_score = cls._calc_format_safety(sent)

            assertions.append({
                "id": i,
                "content": sent,
                "type": atype,
                "M": round(m_score, 2),
                "V": round(v_score, 2),
                "F": f_score,
            })

        return assertions

    @staticmethod
    def _calc_match(sentence: str, intent: str) -> float:
        """计算句子与意图的匹配度"""
        if not intent:
            return 0.7
        # 中文2字片段 + 英文词
        tokens = set(re.findall(r'[\u4e00-\u9fff]{2,}|[a-z]{3,}', intent.lower()))
        if not tokens:
            return 0.7
        hits = sum(1 for t in tokens if t in sentence)
        return min(1.0, 0.3 + hits / len(tokens) * 0.7)

    @staticmethod
    def _calc_format_safety(sentence: str) -> int:
        """计算格式安全度
        - 红色熔断词 → F=0（一票否决）
        - 黄色待审词 → F=1（在熔断层处理，断言层不惩罚）
        """
        for red_word in FUSE_RED:
            if red_word in sentence:
                return 0
        # 黄色词不在断言层降权，由熔断层统一处理
        return 1

    @staticmethod
    def _clean_brain_output(text: str) -> str:
        """清洗脑引擎输出：去除格式标记、人格标签、边框"""
        # 去掉边框行
        text = re.sub(r'^[═╔╚║╗╝─]{3,}.*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'^[║╚╔╗╝].*[║╚╔╗╝]$', '', text, flags=re.MULTILINE)
        # 去掉Markdown标题行
        text = re.sub(r'^#{1,3}\s+.*$', '', text, flags=re.MULTILINE)
        # 去掉引用标记 > *[xxx]* 或 > [xxx]
        text = re.sub(r'^>\s*\**\s*\[.*?\]\**$', '', text, flags=re.MULTILINE)
        # 去掉 `**粗体标记**` → 保留内容
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        # 去掉 `*斜体*` 
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        # 去掉多余空行
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()


# ══════════════════════════════════════════════════════════════════════
# 三色审计适配层 — 封装 audit_3color_v1 接口
# ══════════════════════════════════════════════════════════════════════

class ThinkAuditor:
    """思考输出审计器 — 断言提取 + 三色判定 + 熔断检测"""

    def __init__(self):
        self._audit_engine = None
        try:
            from audit_3color_v1 import ThreeColorAuditEngine, AssertionType, TruthComponent, Assertion
            self._engine_cls = ThreeColorAuditEngine
            self._AssertionType = AssertionType
            self._TruthComponent = TruthComponent
            self._Assertion = Assertion
            self._available = True
        except ImportError:
            self._available = False

    @property
    def available(self) -> bool:
        return self._available

    def audit(
        self,
        output_text: str,
        input_text: str,
        assertions_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        执行完整审计
        返回: {color, score, assertions, fuse_hits, reason}

        熔断策略:
        - 红色熔断词 → 无论输入/输出，一律标记
        - 黄色熔断词 → 只在输入中标记（用户意图模糊），输出中忽略（脑引擎自然会给出建议）
        """
        # 1. 断言提取
        if not assertions_data:
            assertions_data = AssertionExtractor.extract(output_text, input_text)

        # 2. 熔断词检测（输入为主，输出仅检测红色）
        input_fuse = self._detect_fuse_words(input_text, include_yellow=True)
        output_fuse = self._detect_fuse_words(output_text, include_yellow=False)  # 输出只检测红色
        fuse_hits = input_fuse + output_fuse

        # 3. 如果引擎可用，走三色审计引擎
        if self._available and assertions_data:
            try:
                return self._audit_engine_mode(assertions_data, fuse_hits)
            except Exception:
                pass

        # 4. 降级模式：纯规则判定
        return self._rule_mode(assertions_data, fuse_hits)

    def _audit_engine_mode(self, assertions_data: List[Dict[str, Any]], fuse_hits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """使用三色审计引擎"""
        built_assertions = []
        for i, a in enumerate(assertions_data, 1):
            atype = self._AssertionType(a["type"])
            tc = self._TruthComponent(M=a["M"], V=a["V"], F=a["F"])
            ba = self._Assertion(id=i, content=a["content"], assertion_type=atype, truth_component=tc)
            built_assertions.append(ba)

        report = self._engine_cls.create_report(target="think_output", assertions=built_assertions)

        color = report.judgment.value  # "🟢" / "🟡" / "🔴"
        score = report.total_truth_score

        # 红色熔断 → 强制驳回（优先级 > 审计分数）
        red_fuse = [f for f in fuse_hits if f.get("level") == "red"]
        if red_fuse:
            color = "🔴"
            score = min(score, 0.3)

        # 黄色熔断 → 标记待审但不拒（降分但不改色）
        yellow_fuse = [f for f in fuse_hits if f.get("level") == "yellow"]
        if yellow_fuse and color == "🟢":
            color = "🟡"
            score = min(score, 0.70)

        return self._build_result(color, score, assertions_data, fuse_hits)

    def _rule_mode(self, assertions_data: List[Dict[str, Any]], fuse_hits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """纯规则判定（降级模式）"""
        red_fuse = [f for f in fuse_hits if f.get("level") == "red"]
        yellow_fuse = [f for f in fuse_hits if f.get("level") == "yellow"]

        # 红色熔断 → 直接驳回
        if red_fuse:
            return self._build_result("🔴", 0.2, assertions_data, fuse_hits)

        if not assertions_data:
            return self._build_result("🟡", 0.5, assertions_data, fuse_hits)

        # 简单加权平均
        weights = {"numerical": 3, "formula": 3, "identity": 5,
                    "logical": 2, "mapping": 2, "descriptive": 1}
        total_w = 0
        total_s = 0
        for a in assertions_data:
            w = weights.get(a["type"], 1)
            f = a.get("F", 1)
            if f == 0:
                # F=0 一票否定 → 大降权
                s = 0.2
            else:
                s = a["M"] * a["V"]
            total_w += w
            total_s += w * s

        score = total_s / total_w if total_w > 0 else 0.5

        # 黄色熔断降分但不拒（黄色=标记待审，不是驳回）
        if yellow_fuse:
            score = min(score, 0.70)

        if score >= GREEN_THRESHOLD:
            color = "🟢"
        elif score >= YELLOW_THRESHOLD:
            color = "🟡"
        else:
            color = "🔴"

        return self._build_result(color, score, assertions_data, fuse_hits)

    def _build_result(
        self, color: str, score: float, assertions: List[Dict[str, Any]], fuse_hits: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """构建审计结果"""
        reason_parts = []
        if fuse_hits:
            for f in fuse_hits:
                if f.get("level") == "red":
                    reason_parts.append(f"{f['id']}: {f.get('reason', '')}（触发词：{f.get('word', '')}）")
                elif f.get("level") == "yellow":
                    reason_parts.append(f"{f['id']}: {f.get('question', '')}（触发词：{f.get('word', '')}）")

        if not reason_parts and color == "🔴":
            reason_parts.append(f"真实度得分仅 {score:.3f}，低于 {YELLOW_THRESHOLD} 阈值")
        if not reason_parts and color == "🟡":
            reason_parts.append(f"真实度得分 {score:.3f}，在 [{YELLOW_THRESHOLD}, {GREEN_THRESHOLD}) 区间，建议人工复核")
        if not reason_parts:
            reason_parts.append(f"真实度得分 {score:.3f}，通过三色审计")

        return {
            "color": color,
            "score": round(score, 4),
            "assertions": assertions,
            "fuse_hits": fuse_hits,
            "reason": "；".join(reason_parts),
            "thresholds": {"green": GREEN_THRESHOLD, "yellow": YELLOW_THRESHOLD},
        }

    def _detect_fuse_words(self, text: str, include_yellow: bool = True) -> List[Dict[str, Any]]:
        """检测熔断词
        include_yellow=False: 只检测红色熔断词（用于输出审计）
        """
        hits = []
        for word, rule in FUSE_RED.items():
            if word in text:
                hits.append({
                    "level": "red", "id": rule["id"],
                    "word": word, "reason": rule["reason"],
                })
        if include_yellow:
            for word, rule in FUSE_YELLOW.items():
                if word in text:
                    hits.append({
                        "level": "yellow", "id": rule["id"],
                        "word": word, "question": rule["question"],
                    })
        return hits


# ══════════════════════════════════════════════════════════════════════
# 决策卡链 — 追加到 decision_card_chain.jsonl
# ══════════════════════════════════════════════════════════════════════

class DecisionCardChain:
    """决策卡链管理器"""

    def __init__(self, chain_path: Path = DECISION_CARD_CHAIN):
        self.chain_path = chain_path
        self.chain_path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, card: PipelineDecisionCard) -> None:
        """追加决策卡到链尾（append-only）"""
        entry = json.dumps(card.to_dict(), ensure_ascii=False)
        with open(self.chain_path, "a") as f:
            f.write(entry + "\n")

    def recent(self, n: int = 20) -> List[Dict[str, Any]]:
        """读取最近N张决策卡"""
        if not self.chain_path.exists():
            return []
        cards = []
        with open(self.chain_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    cards.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        # 跳过init行
        cards = [c for c in cards if c.get("card_hash")]
        return cards[-n:]

    def count(self) -> int:
        """统计决策卡数量"""
        return len(self.recent(99999))


# ══════════════════════════════════════════════════════════════════════
# SQLite 审计日志 — 管线审计持久化
# ══════════════════════════════════════════════════════════════════════

class PipelineDB:
    """管线审计日志 SQLite"""

    def __init__(self, db_path: Path = PIPELINE_DB):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS pipeline_audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pipeline_id TEXT UNIQUE NOT NULL,
                    timestamp TEXT NOT NULL,
                    source TEXT DEFAULT 'cli',
                    input_text TEXT,
                    output_text TEXT,
                    cycle_id TEXT,
                    brain_dna TEXT,
                    audit_color TEXT NOT NULL,
                    audit_score REAL NOT NULL,
                    action TEXT NOT NULL,
                    reason TEXT,
                    fuse_hits_json TEXT,
                    assertions_json TEXT,
                    card_hash TEXT,
                    created_at TEXT DEFAULT (datetime('now','localtime'))
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_pipeline_color
                ON pipeline_audit(audit_color, timestamp DESC)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_pipeline_cycle
                ON pipeline_audit(cycle_id)
            """)
            conn.commit()

    def log(self, result: "PipelineResult") -> None:
        """记录审计日志"""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO pipeline_audit
                   (pipeline_id, timestamp, source, input_text, output_text,
                    cycle_id, brain_dna, audit_color, audit_score, action,
                    reason, fuse_hits_json, assertions_json, card_hash)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    result.pipeline_id,
                    result.timestamp,
                    result.source,
                    result.input_text,
                    result.output_text,
                    result.cycle_id,
                    result.brain_dna,
                    result.audit_color,
                    result.audit_score,
                    result.action,
                    result.reason,
                    json.dumps(result.fuse_hits, ensure_ascii=False),
                    json.dumps(result.assertions, ensure_ascii=False),
                    result.card_hash,
                ),
            )
            conn.commit()

    def stats(self) -> Dict[str, Any]:
        """查询统计"""
        with sqlite3.connect(str(self.db_path)) as conn:
            total = conn.execute("SELECT COUNT(*) FROM pipeline_audit").fetchone()[0]
            by_color = {}
            for row in conn.execute(
                "SELECT audit_color, COUNT(*) FROM pipeline_audit GROUP BY audit_color"
            ):
                by_color[row[0]] = row[1]
            by_action = {}
            for row in conn.execute(
                "SELECT action, COUNT(*) FROM pipeline_audit GROUP BY action"
            ):
                by_action[row[0]] = row[1]

            latest = conn.execute(
                "SELECT pipeline_id, timestamp, audit_color, action, reason "
                "FROM pipeline_audit ORDER BY timestamp DESC LIMIT 5"
            ).fetchall()

        return {
            "total": total,
            "by_color": by_color,
            "by_action": by_action,
            "latest": [
                {"id": r[0], "time": r[1], "color": r[2], "action": r[3], "reason": r[4]}
                for r in latest
            ],
        }

    def get_by_id(self, pipeline_id: str) -> Optional[Dict[str, Any]]:
        """按ID查询单条记录"""
        with sqlite3.connect(str(self.db_path)) as conn:
            row = conn.execute(
                "SELECT * FROM pipeline_audit WHERE pipeline_id=?",
                (pipeline_id,),
            ).fetchone()
        if not row:
            return None
        cols = ["id", "pipeline_id", "timestamp", "source", "input_text", "output_text",
                "cycle_id", "brain_dna", "audit_color", "audit_score", "action",
                "reason", "fuse_hits_json", "assertions_json", "card_hash", "created_at"]
        d = dict(zip(cols, row))
        d["fuse_hits"] = json.loads(d.pop("fuse_hits_json", "[]"))
        d["assertions"] = json.loads(d.pop("assertions_json", "[]"))
        return d


# ══════════════════════════════════════════════════════════════════════
# 管线结果
# ══════════════════════════════════════════════════════════════════════

class PipelineResult:
    """单次管线执行结果"""

    def __init__(
        self,
        pipeline_id: str,
        timestamp: str,
        source: str,
        input_text: str,
        output_text: str,
        cycle_id: str,
        brain_dna: str,
        audit_color: str,
        audit_score: float,
        action: str,
        reason: str,
        fuse_hits: List[Dict[str, Any]],
        assertions: List[Dict[str, Any]],
        card_hash: str,
    ):
        self.pipeline_id = pipeline_id
        self.timestamp = timestamp
        self.source = source
        self.input_text = input_text
        self.output_text = output_text
        self.cycle_id = cycle_id
        self.brain_dna = brain_dna
        self.audit_color = audit_color
        self.audit_score = audit_score
        self.action = action
        self.reason = reason
        self.fuse_hits = fuse_hits
        self.assertions = assertions
        self.card_hash = card_hash

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pipeline_id": self.pipeline_id,
            "timestamp": self.timestamp,
            "source": self.source,
            "cycle_id": self.cycle_id,
            "brain_dna": self.brain_dna,
            "audit_color": self.audit_color,
            "audit_score": self.audit_score,
            "action": self.action,
            "reason": self.reason,
            "fuse_hits": self.fuse_hits,
            "assertion_count": len(self.assertions),
            "card_hash": self.card_hash,
            "output_preview": self.output_text[:200],
        }

    def format_terminal(self) -> str:
        """终端格式化输出"""
        lines = []
        lines.append("")
        lines.append("═" * 62)
        lines.append(f"  🧠 思考管线 · {self.pipeline_id}")
        lines.append("═" * 62)
        lines.append(f"  来源:   {self.source}")
        lines.append(f"  周期:   {self.cycle_id}")
        lines.append(f"  脑DNA:  {self.brain_dna}")
        lines.append("─" * 62)

        # 审计结果
        color_bar = self.audit_color * 10
        lines.append(f"  审计:   {color_bar}  {self.audit_score:.3f}")
        lines.append(f"  动作:   {self.action}")
        lines.append(f"  依据:   {self.reason}")
        lines.append("─" * 62)

        # 熔断命中
        if self.fuse_hits:
            lines.append(f"  熔断命中 ({len(self.fuse_hits)}):")
            for f in self.fuse_hits:
                level = "🔴" if f.get("level") == "red" else "🟡"
                detail = f.get("reason") or f.get("question", "")
                lines.append(f"    {level} {f['id']} · {f.get('word','')} → {detail}")

        # 断言摘要
        if self.assertions:
            lines.append(f"  断言 ({len(self.assertions)}):")
            for a in self.assertions[:5]:
                score_str = f"M={a.get('M',0):.2f} V={a.get('V',0):.2f} F={a.get('F',0)}"
                lines.append(f"    [{a.get('type','?')[:4]}] {a['content'][:50]}... ({score_str})")

        # 输出预览
        lines.append("─" * 62)
        lines.append(f"  输出预览:")
        for line in self.output_text[:400].split("\n")[:8]:
            lines.append(f"    {line}")
        if len(self.output_text) > 400:
            lines.append(f"    ... (共 {len(self.output_text)} 字符)")

        lines.append("═" * 62)
        lines.append(f"  决策卡: {self.card_hash}")
        lines.append("")
        return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════
# 思考管线主引擎
# ══════════════════════════════════════════════════════════════════════

class ThinkPipeline:
    """
    自动思考管线 — 收→思→审→判→存

    铁律:
    - 每个决策都有依据，没有黑箱
    - 驳回带理由（熔断规则引用）
    - 全链路审计可追溯
    """

    def __init__(self):
        self.auditor = ThinkAuditor()
        self.chain = DecisionCardChain()
        self.db = PipelineDB()
        self._brain_engine = None

    @property
    def brain_engine(self):
        """懒加载脑引擎v2"""
        if self._brain_engine is None:
            try:
                from lh_human_brain_engine_v2 import HumanBrainEngineV2
                self._brain_engine = HumanBrainEngineV2()
            except ImportError:
                self._brain_engine = None
        return self._brain_engine

    def process(self, input_text: str, source: str = "cli") -> PipelineResult:
        """
        完整管线处理

        步骤:
        1. 脑引擎v2思考
        2. 断言提取
        3. 三色审计
        4. 路由判定 (🟢/🟡/🔴)
        5. 生成决策卡
        6. 持久化审计日志
        7. 追加决策卡链
        """
        pipeline_id = hashlib.sha256(
            f"{input_text}{source}{time.time()}{uuid.uuid4()}".encode()
        ).hexdigest()[:12]

        timestamp = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S CST")

        # ── 步骤1: 思考 ──
        cycle_id = "no-engine"
        brain_dna = "#龍芯⚡️NO-ENGINE"
        output_text = ""

        if self.brain_engine:
            try:
                cycle = self.brain_engine.think(input_text, inject_knowledge=True)
                cycle_id = cycle.cycle_id
                brain_dna = cycle.dna
                output_text = cycle.final_output or ""
            except Exception as e:
                output_text = f"[脑引擎错误: {e}]"

        if not output_text and self.brain_engine is None:
            output_text = (
                "脑引擎v2未加载。请确保 bin/lh_human_brain_engine_v2.py 可用。\n"
                "降级模式：直接对输入进行规则审计。"
            )

        # ── 步骤2: 断言提取 ──
        assertions = AssertionExtractor.extract(output_text, input_text)

        # ── 步骤3: 三色审计 ──
        audit_result = self.auditor.audit(output_text, input_text, assertions)
        audit_color = audit_result["color"]
        audit_score = audit_result["score"]
        fuse_hits = audit_result["fuse_hits"]
        assertions = audit_result["assertions"]
        reason = audit_result["reason"]

        # ── 步骤4: 路由判定 ──
        if audit_color == "🔴":
            action = RouteAction.RED_REJECT
        elif audit_color == "🟡":
            action = RouteAction.YELLOW_REVIEW
        else:
            action = RouteAction.GREEN_ADMIT

        # ── 步骤5: 生成决策卡 ──
        card = PipelineDecisionCard(
            input_text=input_text,
            output_text=output_text,
            audit_color=audit_color,
            audit_score=audit_score,
            action=action,
            fuse_hits=fuse_hits,
            assertions=assertions,
            cycle_id=cycle_id,
            brain_dna=brain_dna,
            reason=reason,
            source=source,
        )

        # ── 步骤6-7: 持久化 ──
        result = PipelineResult(
            pipeline_id=pipeline_id,
            timestamp=timestamp,
            source=source,
            input_text=input_text,
            output_text=output_text,
            cycle_id=cycle_id,
            brain_dna=brain_dna,
            audit_color=audit_color,
            audit_score=audit_score,
            action=action.value,
            reason=reason,
            fuse_hits=fuse_hits,
            assertions=assertions,
            card_hash=card.card_hash,
        )

        self.db.log(result)
        self.chain.append(card)

        return result

    def status(self) -> Dict[str, Any]:
        """管线状态"""
        db_stats = self.db.stats()
        chain_count = self.chain.count()
        return {
            "engine": "ThinkPipeline v1.0",
            "brain_engine": "v2.0" if self.brain_engine else "不可用",
            "auditor": "三色审计 v1.0" if self.auditor.available else "规则模式",
            "db": str(PIPELINE_DB),
            "chain": str(DECISION_CARD_CHAIN),
            "chain_cards": chain_count,
            "db_stats": db_stats,
            "thresholds": {"green": GREEN_THRESHOLD, "yellow": YELLOW_THRESHOLD},
        }


# ══════════════════════════════════════════════════════════════════════
# HTTP 服务模式 — 自动收集入口
# ══════════════════════════════════════════════════════════════════════

def create_app(pipeline: ThinkPipeline):
    """创建 Flask 应用"""
    # Flask/Werkzeug依赖标准库logging，但项目根目录有logging/包会遮蔽
    # 必须在sys.path修改前导入Flask，或临时移除遮蔽路径
    _saved_path = list(sys.path)
    # 移除可能遮蔽标准库的项目路径
    sys.path = [p for p in sys.path if not p.endswith('/cnsh/core') and p != str(SYSTEM_ROOT)]
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        print("❌ 需要安装 Flask: pip install flask")
        sys.exit(1)
    finally:
        sys.path = _saved_path  # 恢复

    app = Flask(__name__)

    @app.route("/think", methods=["POST"])
    def think():
        """POST /think — 自动思考+审计+入库"""
        data = request.get_json(silent=True) or {}
        input_text = data.get("input", "").strip()
        if not input_text:
            return jsonify({"error": "缺少 input 字段", "status": "rejected"}), 400

        source = data.get("source", "http")
        result = pipeline.process(input_text, source=source)

        response_data = result.to_dict()
        response_data["output_full"] = result.output_text

        if result.audit_color == "🔴":
            http_status = 403  # Forbidden — 有据驳回
        elif result.audit_color == "🟡":
            http_status = 202  # Accepted but needs review
        else:
            http_status = 200  # OK

        return jsonify(response_data), http_status

    @app.route("/status", methods=["GET"])
    def status():
        """GET /status — 管线状态"""
        return jsonify(pipeline.status())

    @app.route("/cards", methods=["GET"])
    def cards():
        """GET /cards?n=20 — 最近决策卡"""
        n = request.args.get("n", 20, type=int)
        return jsonify(pipeline.chain.recent(n))

    @app.route("/audit/<pipeline_id>", methods=["GET"])
    def audit_detail(pipeline_id: str):
        """GET /audit/:id — 某次审计详情"""
        detail = pipeline.db.get_by_id(pipeline_id)
        if not detail:
            return jsonify({"error": "not found"}), 404
        return jsonify(detail)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "engine": "ThinkPipeline v1.0"})

    return app


# ══════════════════════════════════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="龍魂·自动思考管线 — 收→思→审→判→存",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_think_pipeline.py "我该不该辞职创业？"
  python3 bin/lh_think_pipeline.py --serve --port 9630
  python3 bin/lh_think_pipeline.py --cards 10
  python3 bin/lh_think_pipeline.py --status
        """,
    )
    parser.add_argument("input", nargs="?", help="思考输入文本")
    parser.add_argument("--serve", action="store_true", help="启动HTTP服务（自动收集模式）")
    parser.add_argument("--port", type=int, default=9630, help="HTTP服务端口 (默认9630)")
    parser.add_argument("--batch", help="从文件批量读取输入（每行一个）")
    parser.add_argument("--source", default="cli", help="输入来源标记")
    parser.add_argument("--cards", type=int, nargs="?", const=20, help="查看最近N张决策卡")
    parser.add_argument("--status", action="store_true", help="管线状态")
    parser.add_argument("--audit-detail", help="按pipeline_id查看审计详情")

    args = parser.parse_args()

    pipeline = ThinkPipeline()

    # ── HTTP 服务模式 ──
    if args.serve:
        # 清理sys.path避免logging包遮蔽
        _saved = list(sys.path)
        sys.path = [p for p in sys.path if p != str(SYSTEM_ROOT) and p != str(SYSTEM_ROOT / 'cnsh' / 'core')]
        try:
            from flask import Flask
        except ImportError:
            print("❌ 需要安装 Flask: pip install flask")
            sys.exit(1)
        sys.path = _saved

        app = create_app(pipeline)
        host = "0.0.0.0"
        print(f"\n  🧠 思考管线 HTTP 服务启动")
        print(f"  ═══════════════════════════════")
        print(f"  地址:   http://{host}:{args.port}")
        print(f"  思考:   POST /think")
        print(f"  状态:   GET  /status")
        print(f"  决策卡: GET  /cards?n=20")
        print(f"  审计:   GET  /audit/:id")
        print(f"  健康:   GET  /health")
        print(f"  铁律:   每一条输出都有依据，没有黑箱子")
        print(f"  三色:   🟢≥{GREEN_THRESHOLD} / 🟡≥{YELLOW_THRESHOLD} / 🔴<{YELLOW_THRESHOLD}")
        print(f"")

        # 优雅关闭
        def shutdown(sig, frame):
            print("\n  🛑 管线服务关闭")
            sys.exit(0)

        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

        app.run(host=host, port=args.port, debug=False)
        return

    # ── 状态查询 ──
    if args.status:
        status = pipeline.status()
        print(f"\n  🧠 思考管线状态")
        print(f"  ═══════════════════════════════")
        print(f"  脑引擎:  {status['brain_engine']}")
        print(f"  审计器:  {status['auditor']}")
        print(f"  决策卡链: {status['chain_cards']} 张")
        print(f"  DB统计:  总计 {status['db_stats']['total']} 条")
        for color, count in status['db_stats'].get('by_color', {}).items():
            print(f"           {color} × {count}")
        print(f"  阈值:    🟢≥{status['thresholds']['green']} / 🟡≥{status['thresholds']['yellow']}")
        if status['db_stats'].get('latest'):
            print(f"\n  最近5条:")
            for r in status['db_stats']['latest']:
                print(f"    {r['color']} {r['action']} | {r['time']} | {r['reason'][:50]}")
        print()
        return

    # ── 决策卡查询 ──
    if args.cards is not None:
        n = args.cards if isinstance(args.cards, int) else 20
        cards = pipeline.chain.recent(n)
        if not cards:
            print("\n  📭 暂无决策卡\n")
        else:
            print(f"\n  📋 最近 {len(cards)} 张决策卡")
            print(f"  ═══════════════════════════════")
            for c in cards:
                color = c.get("audit_color", "?")
                action = c.get("action", "?")
                intent = c.get("input_intent", "")[:60]
                reason = c.get("reason", "")[:60]
                print(f"  {color} {action} | {c.get('card_hash','?')}")
                print(f"    意图: {intent}")
                print(f"    依据: {reason}")
                print()
        return

    # ── 审计详情 ──
    if args.audit_detail:
        detail = pipeline.db.get_by_id(args.audit_detail)
        if not detail:
            print(f"\n  ❌ 未找到: {args.audit_detail}\n")
        else:
            print(f"\n  🔍 审计详情: {args.audit_detail}")
            print(f"  ═══════════════════════════════")
            print(f"  时间:    {detail.get('timestamp')}")
            print(f"  审计色:  {detail.get('audit_color')}")
            print(f"  得分:    {detail.get('audit_score')}")
            print(f"  动作:    {detail.get('action')}")
            print(f"  依据:    {detail.get('reason')}")
            print(f"  熔断:    {json.dumps(detail.get('fuse_hits',[]), ensure_ascii=False)}")
            print(f"  断言数:  {len(detail.get('assertions',[]))}")
            print(f"  决策卡:  {detail.get('card_hash')}")
            print()
        return

    # ── 批量模式 ──
    if args.batch:
        batch_path = Path(args.batch)
        if not batch_path.exists():
            print(f"\n  ❌ 文件不存在: {args.batch}\n")
            sys.exit(1)

        lines = batch_path.read_text().strip().split("\n")
        lines = [l.strip() for l in lines if l.strip() and not l.startswith("#")]

        print(f"\n  📦 批量思考: {len(lines)} 条")
        print(f"  ═══════════════════════════════")

        results_stats = {"🟢": 0, "🟡": 0, "🔴": 0}
        for i, line in enumerate(lines, 1):
            print(f"  [{i}/{len(lines)}] {line[:60]}...", end=" ", flush=True)
            result = pipeline.process(line, source=args.source)
            results_stats[result.audit_color] += 1
            print(f"{result.audit_color} {result.action} ({result.card_hash})")

        print(f"\n  批量完成:")
        for color, count in results_stats.items():
            if count > 0:
                print(f"    {color} × {count}")
        print()
        return

    # ── 单次思考模式 ──
    if args.input:
        result = pipeline.process(args.input, source=args.source)
        print(result.format_terminal())
        return

    # ── 无参数 → 帮助 ──
    parser.print_help()


if __name__ == "__main__":
    main()
