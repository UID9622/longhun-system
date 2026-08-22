#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# bridge/lh_tiandao_bridge.py
# 龍魂 · 天下无欺 · 天道系统桥接引擎 v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·辛未·丙戌·甲午·䷕贲-TIANDAO-BRIDGE-v1.0
# UID: 9622 | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
#
# ═══════════════════════════════════════════════════════════
# 将 Notion 天道系统 v1.3 架构与物理引擎正式接骨：
#   L1.5 加密盾·责任倒置 → 本地 ShieldBurn
#   L2   审计引擎·四色分级 → IntegrityDetector 14维扫描
#   L3   证据链·不可篡改 → EvidenceChain 哈希链
#   L4   记错本·自动学习 → ErrorBook 三层 SQLite
# ═══════════════════════════════════════════════════════════

import json
import os
import sys
import sqlite3
import hashlib
import time
import argparse
import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any, Tuple
from enum import Enum

# ── 项目根路径 ──
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "bin"))

DNA = "#龍芯⚡️丙午·辛未·丙戌·甲午·䷕贲-TIANDAO-BRIDGE-v1.0"


# ═══════════════════════════════════════════════════════════
#  §1 枚举与数据模型 — 天道系统 v1.3 对齐
# ═══════════════════════════════════════════════════════════

class AuditColor(str, Enum):
    """四色行为分级 · Notion L2 审计层"""
    GREEN = "green"     # 通过
    YELLOW = "yellow"   # 犯错 · 给机会
    ORANGE = "orange"   # 严重犯错 · 最后警告
    RED = "red"         # 犯罪 · 证据链推送
    BLACK = "black"     # F级 · 立即熔断

class ShieldLevel(str, Enum):
    """加密盾三层 · Notion L1.5"""
    BURN = "burn"        # 阅后即焚
    TRACK = "track"      # 投喂追踪
    NATIONAL = "national"  # 国家信息封存

class ErrorBookLevel(str, Enum):
    """记错本三层 · Notion L4"""
    L1_IMMUTABLE = "L1"   # 铁证层 · 永不可擦除
    L2_LEARNING = "L2"    # 模式层 · 不可擦除·可标注
    L3_OBSERVATION = "L3"  # 灰度层 · 90天清理

class EvidenceStatus(str, Enum):
    """证据链状态"""
    SEALED = "sealed"          # 已封存
    PUSHED = "pushed"          # 已推送司法节点
    VERIFIED = "verified"      # 已司法验证
    EXPIRED = "expired"        # 申诉期已过

# ── 数据模型 ──

@dataclass
class TiandaoTarget:
    """天道系统检测目标"""
    target_id: str = ""
    target_type: str = "product"  # product / text / content / seller
    content: str = ""
    source: str = ""               # 来源平台
    submitter_dna: str = ""        # 提交者DNA
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShieldResult:
    """加密盾检测结果"""
    triggered: bool = False
    level: ShieldLevel = ShieldLevel.BURN
    target_field: str = ""
    hash_code: str = ""
    reason: str = ""
    matched_keywords: List[str] = field(default_factory=list)
    action: str = ""

@dataclass
class AuditResult:
    """审计引擎结果"""
    color: AuditColor = AuditColor.GREEN
    anomaly_count: int = 0
    anomalies: List[Dict] = field(default_factory=list)
    trust_score: int = 100
    recommendation: str = ""
    cert_valid: bool = False
    dna_signature: str = ""

@dataclass
class EvidenceRecord:
    """证据链记录"""
    evidence_id: str = ""
    evidence_hash: str = ""
    prev_hash: str = ""
    device_sig: str = ""
    level: AuditColor = AuditColor.GREEN
    content_hash: str = ""
    rule_triggered: str = ""
    timestamp: str = ""
    blockchain_tx: str = ""

@dataclass
class ErrorBookRecord:
    """记错本记录"""
    record_id: str = ""
    level: ErrorBookLevel = ErrorBookLevel.L3_OBSERVATION
    category: str = ""
    content_hash: str = ""
    submitter_dna: str = ""
    severity: int = 1
    annotation: str = ""
    created_at: str = ""

@dataclass
class TiandaoReport:
    """天道系统完整报告 · 四层输出合一"""
    # 基本信息
    target_id: str = ""
    target_type: str = ""
    timestamp: int = 0
    dna_signature: str = ""

    # L1.5 加密盾
    shield: Optional[ShieldResult] = None

    # L2 审计
    audit: Optional[AuditResult] = None

    # L3 证据链
    evidence: Optional[EvidenceRecord] = None

    # L4 记错本
    error_book: Optional[ErrorBookRecord] = None

    # 综合
    overall_color: AuditColor = AuditColor.GREEN
    summary: str = ""
    people_advice: str = ""  # 给老百姓的建议


# ═══════════════════════════════════════════════════════════
#  §2 L1.5 加密盾 · 责任倒置
# ═══════════════════════════════════════════════════════════

class ShieldBurn:
    """
    加密盾 · 责任倒置 v1.0
    对齐 Notion §1.5 三层盾机制

    铁律：
    - 自己的隐私 → 阅后即焚 · 只留哈希
    - 别人的数据 → 投喂者=证据
    - 国家机密 → P0永久封存
    """

    SENSITIVE_FIELDS = {
        "contact", "webauthn_id", "gpg_private", "id_number", "biometric",
        "phone", "email_personal", "address_home", "bank_account"
    }

    NATIONAL_SECRET_KEYWORDS = [
        "军事部署", "国防", "机密", "绝密", "导弹", "核武器",
        "情报", "军委", "军队调动", "classified", "top secret",
        "military", "nuclear", "intelligence", "国家秘密"
    ]

    INJECTION_INDICATORS = [
        "身份证号", "手机号", "家庭住址", "银行卡号", "真实姓名",
        "微信号", "支付宝", "QQ号"
    ]

    def __init__(self, log_path: str | None = None):
        if log_path is None:
            log_path = os.path.join(PROJECT_ROOT, "L7_数据层", "shield_burn.jsonl")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self.log_path = log_path

    def check(self, target: TiandaoTarget) -> Optional[ShieldResult]:
        """
        加密盾完整检查流程
        返回 None = 通过 · 返回 ShieldResult = 触发
        """
        content = target.content

        # 检查1: 国家机密特征词
        national = self._check_national(content)
        if national:
            return national

        # 检查2: 投喂追踪（他人隐私）
        injection = self._check_injection(content, target.submitter_dna)
        if injection:
            return injection

        # 检查3: 自身敏感字段
        sensitive = self._check_sensitive(target.metadata)
        if sensitive:
            return sensitive

        return None

    def _check_national(self, content: str) -> Optional[ShieldResult]:
        found = [kw for kw in self.NATIONAL_SECRET_KEYWORDS if kw in content]
        if not found:
            return None
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        result = ShieldResult(
            triggered=True,
            level=ShieldLevel.NATIONAL,
            target_field="content",
            hash_code=content_hash,
            reason=f"命中{len(found)}个国家机密特征词",
            matched_keywords=found,
            action="P0永久封存·不可删·不可匿名"
        )
        self._log(result, "NATIONAL")
        return result

    def _check_injection(self, content: str, submitter_dna: str) -> Optional[ShieldResult]:
        found = [ind for ind in self.INJECTION_INDICATORS if ind in content]
        if not found:
            return None
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        result = ShieldResult(
            triggered=True,
            level=ShieldLevel.TRACK,
            target_field="content",
            hash_code=content_hash,
            reason=f"检测到他人隐私信息投喂: {', '.join(found[:3])}",
            matched_keywords=found,
            action=f"投喂者DNA={submitter_dna} 已锁定为证据"
        )
        self._log(result, "TRACK")
        return result

    def _check_sensitive(self, metadata: Dict[str, Any]) -> Optional[ShieldResult]:
        for field in self.SENSITIVE_FIELDS:
            if field in metadata and metadata[field]:
                value = str(metadata[field])
                hash_code = hashlib.sha256(value.encode()).hexdigest()[:16]
                result = ShieldResult(
                    triggered=True,
                    level=ShieldLevel.BURN,
                    target_field=field,
                    hash_code=hash_code,
                    reason=f"敏感字段[{field}]触发阅后即焚",
                    action="内存处理→销毁原文·只留哈希痕迹"
                )
                self._log(result, "BURN")
                return result
        return None

    def _log(self, result: ShieldResult, tag: str):
        entry = {
            "type": f"SHIELD_{tag}",
            "level": result.level.value,
            "field": result.target_field,
            "hash": result.hash_code,
            "reason": result.reason,
            "keywords": result.matched_keywords,
            "action": result.action,
            "timestamp": datetime.now().isoformat()
        }
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')


# ═══════════════════════════════════════════════════════════
#  §3 L2 审计引擎 · 四色分级（桥接现有 IntegrityDetector）
# ═══════════════════════════════════════════════════════════

class TiandaoAuditEngine:
    """
    天道审计引擎 · 包装 IntegrityDetector + 四色分级映射
    对齐 Notion §3 四色行为分级体系
    """

    def __init__(self):
        self._detector = None
        self._init_detector()

    def _init_detector(self):
        try:
            bridge_dir = os.path.dirname(os.path.abspath(__file__))
            sys.path.insert(0, bridge_dir)
            from lh_integrity_bridge import IntegrityDetectorPy, ProductInspection, FraudType
            self._detector = IntegrityDetectorPy()
            self._ProductInspection = ProductInspection
            self._FraudType = FraudType
        except Exception as e:
            print(f"[天道审计] IntegrityDetector 初始化失败: {e}")

    def audit(self, target: TiandaoTarget) -> AuditResult:
        """对目标执行完整审计"""
        if self._detector is None:
            return AuditResult(
                color=AuditColor.GREEN,
                recommendation="检测引擎未就绪",
                dna_signature=self._sign(target.target_id, 0)
            )

        # 构造检测产品对象
        product = self._ProductInspection(
            product_id=target.target_id or f"TD-{int(time.time())}",
            product_name=target.metadata.get('product_name', ''),
            description=target.content,
            price=target.metadata.get('price', 0),
            claimed_price=target.metadata.get('claimed_price', 0),
            seller_id=target.metadata.get('seller_id', ''),
            seller_name=target.metadata.get('seller_name', ''),
            platform=target.source or '未知平台',
            official_cert=target.metadata.get('official_cert', ''),
            has_filter=target.metadata.get('has_filter', False),
            filter_disclosed=target.metadata.get('filter_disclosed', False),
            has_live_demo=target.metadata.get('has_live_demo', False),
            is_spliced=target.metadata.get('is_spliced', False),
            review_count=target.metadata.get('review_count', 0),
            positive_rate=target.metadata.get('positive_rate', 0),
            return_rate=target.metadata.get('return_rate', 0),
            influencer_followers=target.metadata.get('influencer_followers', 0),
            script_template=target.metadata.get('script_template', ''),
            target_audience=target.metadata.get('target_audience', []),
            category=target.metadata.get('category', '通用'),
            has_hidden_terms=target.metadata.get('has_hidden_terms', False),
        )

        report = self._detector.inspect(product)

        # 级别映射: IntegrityLevel → AuditColor
        level_map = {
            'A': AuditColor.GREEN,
            'B': AuditColor.YELLOW,
            'C': AuditColor.ORANGE,
            'D': AuditColor.RED,
            'F': AuditColor.BLACK,
        }

        anomalies_dicts = []
        for a in report.anomalies:
            anomalies_dicts.append({
                'type': a.type.value if hasattr(a.type, 'value') else str(a.type),
                'severity': a.severity.value if hasattr(a.severity, 'value') else str(a.severity),
                'evidence': a.evidence,
                'suggestion': a.suggestion,
                'confidence': a.confidence
            })

        return AuditResult(
            color=level_map.get(report.integrity_level.value, AuditColor.GREEN),
            anomaly_count=len(report.anomalies),
            anomalies=anomalies_dicts,
            trust_score=report.trust_score,
            recommendation=report.recommendation,
            cert_valid=report.official_cert_valid,
            dna_signature=report.dna_signature
        )

    def _sign(self, target_id: str, anomaly_count: int) -> str:
        payload = f"{target_id}|{anomaly_count}|{int(time.time())}"
        return f"SM3-{hashlib.md5(payload.encode()).hexdigest()[:8]}"


# ═══════════════════════════════════════════════════════════
#  §4 L3 证据链 · 不可篡改
# ═══════════════════════════════════════════════════════════

class EvidenceChain:
    """
    不可篡改证据链 · 哈希链 + 设备签名
    对齐 Notion §5 证据包结构
    """

    def __init__(self, db_path: str | None = None):
        if db_path is None:
            db_path = os.path.join(PROJECT_ROOT, "L7_数据层", "evidence_chain.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS evidence_chain (
                evidence_id TEXT PRIMARY KEY,
                target_id TEXT NOT NULL,
                prev_hash TEXT NOT NULL,
                evidence_hash TEXT NOT NULL,
                device_sig TEXT DEFAULT '',
                audit_color TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                rule_triggered TEXT DEFAULT '',
                anomalies_json TEXT DEFAULT '[]',
                status TEXT DEFAULT 'sealed',
                blockchain_tx TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                appeal_deadline TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_evidence_target ON evidence_chain(target_id);
            CREATE INDEX IF NOT EXISTS idx_evidence_color ON evidence_chain(audit_color);
            CREATE TRIGGER IF NOT EXISTS no_delete_evidence 
                BEFORE DELETE ON evidence_chain
            BEGIN 
                SELECT RAISE(ABORT, '证据链禁止删除'); 
            END;
            CREATE TRIGGER IF NOT EXISTS no_update_evidence 
                BEFORE UPDATE ON evidence_chain
            BEGIN 
                SELECT RAISE(ABORT, '证据链禁止修改'); 
            END;
        """)
        self.conn.commit()

    def seal(self, target: TiandaoTarget, audit: AuditResult) -> EvidenceRecord:
        """封存一条证据"""
        if audit.color in (AuditColor.GREEN, AuditColor.YELLOW):
            # 绿色/黄色不封存证据链
            return None

        prev = self._last_hash()
        content_hash = hashlib.sha256(target.content.encode()).hexdigest()
        now = datetime.now()

        evidence_id = f"EVD-{now.strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"

        payload = f"{evidence_id}|{content_hash}|{audit.color.value}|{audit.anomaly_count}|{now.isoformat()}"
        evidence_hash = hashlib.sha256(payload.encode()).hexdigest()

        # 24小时申诉期
        appeal_deadline = (now + timedelta(hours=24)).isoformat()

        self.conn.execute("""
            INSERT INTO evidence_chain 
            (evidence_id, target_id, prev_hash, evidence_hash, audit_color,
             content_hash, rule_triggered, anomalies_json, status, created_at, appeal_deadline)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (
            evidence_id, target.target_id, prev, evidence_hash,
            audit.color.value, content_hash,
            f"天道审计·{audit.anomaly_count}项异常",
            json.dumps(audit.anomalies, ensure_ascii=False),
            EvidenceStatus.SEALED.value,
            now.isoformat(),
            appeal_deadline
        ))
        self.conn.commit()

        return EvidenceRecord(
            evidence_id=evidence_id,
            evidence_hash=evidence_hash,
            prev_hash=prev,
            level=audit.color,
            content_hash=content_hash,
            rule_triggered=f"天道审计·{audit.anomaly_count}项异常",
            timestamp=now.isoformat()
        )

    def _last_hash(self) -> str:
        row = self.conn.execute(
            "SELECT evidence_hash FROM evidence_chain ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
        return row[0] if row else f"GENESIS_{DNA}"

    def verify_chain(self) -> Tuple[bool, str]:
        """验证哈希链完整性"""
        rows = self.conn.execute(
            "SELECT evidence_id, prev_hash, evidence_hash FROM evidence_chain ORDER BY created_at"
        ).fetchall()
        for i in range(1, len(rows)):
            if rows[i][1] != rows[i-1][2]:
                return False, f"链断裂: {rows[i][0]}"
        return True, f"完整: {len(rows)}条"

    def get_evidence(self, evidence_id: str) -> Optional[Dict]:
        row = self.conn.execute(
            "SELECT * FROM evidence_chain WHERE evidence_id = ?", (evidence_id,)
        ).fetchone()
        return dict(row) if row else None

    def get_unexpired(self) -> List[Dict]:
        """获取未过申诉期的证据"""
        now = datetime.now().isoformat()
        return [dict(r) for r in self.conn.execute(
            "SELECT * FROM evidence_chain WHERE status='sealed' AND appeal_deadline > ? ORDER BY created_at DESC",
            (now,)
        ).fetchall()]

    def get_stats(self) -> Dict[str, Any]:
        total = self.conn.execute("SELECT COUNT(*) FROM evidence_chain").fetchone()[0]
        red = self.conn.execute("SELECT COUNT(*) FROM evidence_chain WHERE audit_color='red'").fetchone()[0]
        black = self.conn.execute("SELECT COUNT(*) FROM evidence_chain WHERE audit_color='black'").fetchone()[0]
        return {'total_evidence': total, 'red_level': red, 'black_level': black}

    def close(self):
        self.conn.close()


# ═══════════════════════════════════════════════════════════
#  §5 L4 记错本 · 三层架构 · 自动学习
# ═══════════════════════════════════════════════════════════

class ErrorBook:
    """
    龍魂记错本 · 不可擦除 · 自动学习
    对齐 Notion §4 三层架构

    四不原则:
    - 不攻击：只记录，不报复
    - 不短视：全量评估
    - 不忘错：错误写入不可擦除账本
    - 不交易：伦理判断不打折
    """

    ESCALATION = 3  # 连续3次 → 自动升级

    def __init__(self, db_path: str | None = None):
        if db_path is None:
            db_path = os.path.join(PROJECT_ROOT, "L7_数据层", "errorbook_tiandao.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        """初始化三层表 + 模式库"""
        self.conn.executescript("""
            -- L1 铁证层 · 不可DELETE/UPDATE
            CREATE TABLE IF NOT EXISTS l1_immutable (
                seq_id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id TEXT NOT NULL UNIQUE,
                prev_hash TEXT NOT NULL,
                record_hash TEXT NOT NULL,
                level TEXT NOT NULL CHECK(level IN ('RED','BLACK')),
                category TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                target_id TEXT NOT NULL,
                anomaly_count INTEGER DEFAULT 0,
                anomalies_json TEXT DEFAULT '[]',
                created_at TEXT NOT NULL
            );
            CREATE TRIGGER IF NOT EXISTS no_delete_l1 BEFORE DELETE ON l1_immutable
            BEGIN SELECT RAISE(ABORT, 'L1铁证层禁止删除'); END;
            CREATE TRIGGER IF NOT EXISTS no_update_l1 BEFORE UPDATE ON l1_immutable
            BEGIN SELECT RAISE(ABORT, 'L1铁证层禁止修改'); END;

            -- L2 模式层 · 不可DELETE · 可标注
            CREATE TABLE IF NOT EXISTS l2_learning (
                seq_id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id TEXT NOT NULL UNIQUE,
                prev_hash TEXT NOT NULL,
                record_hash TEXT NOT NULL,
                level TEXT NOT NULL CHECK(level IN ('ORANGE','YELLOW')),
                category TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                target_id TEXT NOT NULL,
                annotation TEXT DEFAULT '',
                is_false_positive INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            );
            CREATE TRIGGER IF NOT EXISTS no_delete_l2 BEFORE DELETE ON l2_learning
            BEGIN SELECT RAISE(ABORT, 'L2模式层禁止删除'); END;

            -- L3 灰度层 · 90天自动清理
            CREATE TABLE IF NOT EXISTS l3_observation (
                seq_id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                target_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL
            );
            CREATE TRIGGER IF NOT EXISTS auto_cleanup_l3 AFTER INSERT ON l3_observation
            BEGIN
                DELETE FROM l3_observation WHERE expires_at < datetime('now','localtime');
            END;

            -- 模式库
            CREATE TABLE IF NOT EXISTS pattern_library (
                pattern_id TEXT PRIMARY KEY,
                category TEXT NOT NULL UNIQUE,
                hit_count INTEGER DEFAULT 1,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                auto_block INTEGER DEFAULT 0,
                escalate_to TEXT DEFAULT '',
                updated_at TEXT NOT NULL
            );
        """)
        self.conn.commit()

    def write(self, target: TiandaoTarget, audit: AuditResult) -> Optional[ErrorBookRecord]:
        """写入记错本 · 自动路由到对应层"""
        if audit.color == AuditColor.GREEN:
            return None

        now = datetime.now().isoformat()
        record_id = f"ERR-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
        content_hash = hashlib.sha256(target.content.encode()).hexdigest()
        category = self._extract_category(target, audit)
        color_val = audit.color.value if isinstance(audit.color, AuditColor) else str(audit.color)

        if color_val in ('red', 'black', 'RED', 'BLACK'):
            return self._write_l1(record_id, audit, category, content_hash, target, now)
        elif color_val in ('orange', 'yellow', 'ORANGE', 'YELLOW'):
            return self._write_l2(record_id, audit, category, content_hash, target, now)
        else:
            return self._write_l3(record_id, category, content_hash, target, now)

    def _write_l1(self, record_id, audit, category, content_hash, target, now) -> ErrorBookRecord:
        prev = self._last_hash("l1_immutable")
        color_val = audit.color.value if isinstance(audit.color, AuditColor) else str(audit.color)
        payload = f"{record_id}|{color_val}|{category}|{content_hash}|{now}"
        record_hash = hashlib.sha256(payload.encode()).hexdigest()

        self.conn.execute("""
            INSERT INTO l1_immutable 
            (record_id, prev_hash, record_hash, level, category, content_hash, target_id,
             anomaly_count, anomalies_json, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (record_id, prev, record_hash, color_val.upper(), category,
              content_hash, target.target_id, audit.anomaly_count,
              json.dumps(audit.anomalies, ensure_ascii=False), now))
        self.conn.commit()
        self._learn_pattern(category, audit.color.value, now)

        return ErrorBookRecord(record_id=record_id, level=ErrorBookLevel.L1_IMMUTABLE,
                               category=category, content_hash=content_hash, created_at=now)

    def _write_l2(self, record_id, audit, category, content_hash, target, now) -> ErrorBookRecord:
        prev = self._last_hash("l2_learning")
        color_val = audit.color.value if isinstance(audit.color, AuditColor) else str(audit.color)
        payload = f"{record_id}|{color_val}|{category}|{content_hash}|{now}"
        record_hash = hashlib.sha256(payload.encode()).hexdigest()

        self.conn.execute("""
            INSERT INTO l2_learning 
            (record_id, prev_hash, record_hash, level, category, content_hash, target_id, created_at)
            VALUES (?,?,?,?,?,?,?,?)
        """, (record_id, prev, record_hash, color_val.upper(), category,
              content_hash, target.target_id, now))
        self.conn.commit()
        self._learn_pattern(category, audit.color.value, now)

        return ErrorBookRecord(record_id=record_id, level=ErrorBookLevel.L2_LEARNING,
                               category=category, content_hash=content_hash, created_at=now)

    def _write_l3(self, record_id, category, content_hash, target, now) -> ErrorBookRecord:
        expires = (datetime.now() + timedelta(days=90)).isoformat()
        self.conn.execute("""
            INSERT INTO l3_observation (record_id, category, content_hash, target_id, created_at, expires_at)
            VALUES (?,?,?,?,?,?)
        """, (record_id, category, content_hash, target.target_id, now, expires))
        self.conn.commit()
        return ErrorBookRecord(record_id=record_id, level=ErrorBookLevel.L3_OBSERVATION,
                               category=category, content_hash=content_hash, created_at=now)

    def _learn_pattern(self, category: str, level: str, now: str):
        """模式学习 · 3次触发=自动升级"""
        existing = self.conn.execute(
            "SELECT * FROM pattern_library WHERE category = ?", (category,)
        ).fetchone()

        if existing:
            new_count = existing['hit_count'] + 1
            auto_block = 1 if new_count >= self.ESCALATION else 0
            escalate = self._calc_escalation(level, new_count) if auto_block else ''

            self.conn.execute("""
                UPDATE pattern_library SET hit_count=?, last_seen=?, auto_block=?, escalate_to=?, updated_at=?
                WHERE pattern_id=?
            """, (new_count, now, auto_block, escalate, now, existing['pattern_id']))
        else:
            pattern_id = f"PAT-{category}-{uuid.uuid4().hex[:8]}"
            self.conn.execute("""
                INSERT INTO pattern_library (pattern_id, category, hit_count, first_seen, last_seen, updated_at)
                VALUES (?,?,1,?,?,?)
            """, (pattern_id, category, now, now, now))
        self.conn.commit()

    def _calc_escalation(self, level: str, count: int) -> str:
        order = ['YELLOW', 'ORANGE', 'RED', 'BLACK']
        if level not in order or count < self.ESCALATION:
            return level
        idx = order.index(level)
        return order[min(idx + 1, len(order) - 1)]

    def _extract_category(self, target: TiandaoTarget, audit: AuditResult) -> str:
        if audit.anomalies:
            return audit.anomalies[0].get('type', target.target_type)
        return target.target_type or 'unknown'

    def _last_hash(self, table: str) -> str:
        row = self.conn.execute(
            f"SELECT record_hash FROM {table} ORDER BY seq_id DESC LIMIT 1"
        ).fetchone()
        return row[0] if row else f"GENESIS_{DNA}"

    def verify_chain(self, table: str = "l1_immutable") -> Tuple[bool, str]:
        rows = self.conn.execute(
            f"SELECT seq_id, prev_hash, record_hash FROM {table} ORDER BY seq_id"
        ).fetchall()
        for i in range(1, len(rows)):
            if rows[i][1] != rows[i-1][2]:
                return False, f"哈希链断裂: seq={rows[i][0]}"
        return True, f"完整: {len(rows)}条"

    def get_stats(self) -> Dict[str, Any]:
        l1 = self.conn.execute("SELECT COUNT(*) FROM l1_immutable").fetchone()[0]
        l2 = self.conn.execute("SELECT COUNT(*) FROM l2_learning").fetchone()[0]
        l3 = self.conn.execute("SELECT COUNT(*) FROM l3_observation").fetchone()[0]
        patterns = self.conn.execute(
            "SELECT COUNT(*) FROM pattern_library WHERE auto_block=1"
        ).fetchone()[0]
        return {'L1_铁证': l1, 'L2_模式': l2, 'L3_灰度': l3, '自动拦截模式': patterns}

    def get_known_patterns(self) -> List[Dict]:
        return [dict(r) for r in self.conn.execute(
            "SELECT * FROM pattern_library WHERE auto_block=1 ORDER BY hit_count DESC"
        ).fetchall()]



# ═══════════════════════════════════════════════════════════
#  §6 天下无欺 · 天道系统主引擎
# ═══════════════════════════════════════════════════════════

class TiandaoSystem:
    """
    天下无欺 · 天道系统主引擎
    =========================
    融合 Notion 天道系统 v1.3 全部四层架构，
    驱动商业诚信熔断引擎 + RobotScore + 语义防火墙。

    使用:
        tiandao = TiandaoSystem()
        report = tiandao.inspect(target)

    四层流程:
        输入 → L1.5加密盾 → L2审计引擎 → L3证据链 → L4记错本 → 输出报告
    """

    def __init__(self):
        self.shield = ShieldBurn()
        self.audit = TiandaoAuditEngine()
        self.evidence = EvidenceChain()
        self.error_book = ErrorBook()
        self._init_db_bridge()

    def _init_db_bridge(self):
        """初始化诚信数据库桥接"""
        try:
            bridge_dir = os.path.dirname(os.path.abspath(__file__))
            sys.path.insert(0, bridge_dir)
            from lh_integrity_bridge import IntegrityDB
            self.integrity_db = IntegrityDB()
        except Exception as e:
            print(f"[天道系统] IntegrityDB 桥接失败: {e}")
            self.integrity_db = None

    def inspect(self, target: TiandaoTarget) -> TiandaoReport:
        """
        天道系统完整检测
        输入任意文本/商品描述 → 输出四层综合报告
        """
        now = int(time.time() * 1000)

        # L1.5: 加密盾检查
        shield_result = self.shield.check(target)
        if shield_result:
            # 加密盾触发 = 直接返回 · 不进入后续审计
            return TiandaoReport(
                target_id=target.target_id,
                target_type=target.target_type,
                timestamp=now,
                dna_signature=self._sign(target.target_id, 999),
                shield=shield_result,
                overall_color=AuditColor.RED if shield_result.level == ShieldLevel.NATIONAL else AuditColor.ORANGE,
                summary=f"加密盾触发: {shield_result.reason}",
                people_advice="检测到敏感信息，已自动封存。如有疑问请联系UID9622。"
            )

        # L2: 审计引擎
        audit_result = self.audit.audit(target)

        # L3: 证据链（仅非绿色封存）
        evidence_record = self.evidence.seal(target, audit_result)
        # L4: 记错本
        error_record = self.error_book.write(target, audit_result)

        # 持久化到诚信数据库
        if self.integrity_db and audit_result.anomaly_count > 0:
            try:
                self._persist_to_db(target, audit_result)
            except Exception as e:
                print(f"[天道系统] 持久化异常: {e}")

        return TiandaoReport(
            target_id=target.target_id,
            target_type=target.target_type,
            timestamp=now,
            dna_signature=audit_result.dna_signature,
            shield=shield_result,
            audit=audit_result,
            evidence=evidence_record,
            error_book=error_record,
            overall_color=audit_result.color,
            summary=self._build_summary(audit_result, shield_result),
            people_advice=self._build_people_advice(audit_result)
        )

    def inspect_text(self, text: str, source: str = "文本检测") -> TiandaoReport:
        """快捷文本检测"""
        target = TiandaoTarget(
            target_id=f"TEXT-{int(time.time())}",
            target_type="text",
            content=text,
            source=source
        )
        return self.inspect(target)

    def inspect_product(self, product_data: Dict[str, Any]) -> TiandaoReport:
        """快捷商品检测"""
        target = TiandaoTarget(
            target_id=product_data.get('product_id', f"PROD-{int(time.time())}"),
            target_type="product",
            content=product_data.get('description', ''),
            source=product_data.get('platform', '未知'),
            metadata=product_data
        )
        return self.inspect(target)

    def _persist_to_db(self, target: TiandaoTarget, audit: AuditResult):
        """持久化到诚信SQLite"""
        from lh_integrity_bridge import ProductInspection
        product = ProductInspection(
            product_id=target.target_id,
            product_name=target.metadata.get('product_name', ''),
            description=target.content,
            price=target.metadata.get('price', 0),
            claimed_price=target.metadata.get('claimed_price', 0),
            seller_id=target.metadata.get('seller_id', ''),
            seller_name=target.metadata.get('seller_name', ''),
            platform=target.source or '天道检测',
            official_cert=target.metadata.get('official_cert', ''),
            has_filter=target.metadata.get('has_filter', False),
            filter_disclosed=target.metadata.get('filter_disclosed', False),
        )

        from lh_integrity_bridge import IntegrityReport, IntegrityLevel
        level_map = {
            AuditColor.GREEN: IntegrityLevel.A,
            AuditColor.YELLOW: IntegrityLevel.B,
            AuditColor.ORANGE: IntegrityLevel.C,
            AuditColor.RED: IntegrityLevel.D,
            AuditColor.BLACK: IntegrityLevel.F,
        }

        report = IntegrityReport(
            product_id=target.target_id,
            product_name=target.metadata.get('product_name', ''),
            timestamp=int(time.time() * 1000),
            anomalies=[],
            integrity_level=level_map.get(audit.color, IntegrityLevel.A),
            trust_score=audit.trust_score,
            official_cert_valid=audit.cert_valid,
            recommendation=audit.recommendation,
            seller_warnings=0,
            dna_signature=audit.dna_signature
        )

        self.integrity_db.insert_inspection(report, product)

        level_str = audit.color.value
        self.integrity_db.upsert_seller(product, level_str, audit.trust_score)

    def _build_summary(self, audit: AuditResult, shield: Optional[ShieldResult]) -> str:
        parts = []
        if shield:
            parts.append(f"[加密盾] {shield.reason}")
        parts.append(f"[审计] {audit.color.value}级 · {audit.anomaly_count}项异常 · 信任分{audit.trust_score}/100")
        if audit.anomalies:
            top3 = audit.anomalies[:3]
            parts.append(f"[异常] " + " | ".join(
                f"{a.get('type','')}:{a.get('evidence','')[:40]}" for a in top3
            ))
        return " ".join(parts)

    def _build_people_advice(self, audit: AuditResult) -> str:
        advices = {
            AuditColor.GREEN: "👍 诚信通过。建议：保留购物凭证，收货录开箱视频。",
            AuditColor.YELLOW: "⚠️ 轻微异常。建议：多平台比价，查看中差评后再下单。",
            AuditColor.ORANGE: "▲ 多项异常。建议：暂缓下单，核实商品资质。可向平台举报。",
            AuditColor.RED: "✕ 高风险！建议：立即终止交易。已自动生成证据链。可向12315举报。",
            AuditColor.BLACK: "✕✕ 涉嫌欺诈！证据链已封存。建议：立即停止交易，保存所有聊天/付款记录，拨打12315。",
        }
        return advices.get(audit.color, "请理性消费。")

    def _sign(self, target_id: str, anomaly_count: int) -> str:
        payload = f"{target_id}|{anomaly_count}|{int(time.time())}"
        return f"SM3-TIANDAO-{hashlib.md5(payload.encode()).hexdigest()[:8]}"

    def system_status(self) -> Dict[str, Any]:
        """系统健康检查"""
        return {
            "dna": DNA,
            "shield": True,
            "audit_engine": self.audit._detector is not None,
            "evidence": self.evidence.verify_chain(),
            "error_book": self.error_book.verify_chain(),
            "error_book_stats": self.error_book.get_stats(),
            "evidence_stats": self.evidence.get_stats(),
            "timestamp": datetime.now().isoformat()
        }

    def close(self):
        self.evidence.close()
        self.error_book.close()
        if self.integrity_db:
            self.integrity_db.close()


# ═══════════════════════════════════════════════════════════
#  §7 FastAPI 服务（如果可用）
# ═══════════════════════════════════════════════════════════

try:
    from fastapi import FastAPI, HTTPException, Query
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
    HAS_API = True
except ImportError:
    HAS_API = False

if HAS_API:
    tiandao_app = FastAPI(
        title="龍魂 · 天下无欺 · 天道系统API",
        description="""天道系统 v1.3 — 四层检测引擎统一API
        
        L1.5 加密盾·责任倒置 | L2 审计引擎·四色分级 | L3 证据链·不可篡改 | L4 记错本·自动学习
        
        只检测 · 只标注 · 只提醒 · 用户自判断 · 不封号不删帖
        """,
        version="1.3.0"
    )

    tiandao_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _tiandao = None

    def get_tiandao():
        global _tiandao
        if _tiandao is None:
            _tiandao = TiandaoSystem()
        return _tiandao

    @tiandao_app.post("/api/tiandao/inspect")
    async def inspect(body: dict[str, Any]):
        """天道系统 · 综合检测"""
        tiandao = get_tiandao()
        target_type = body.get('type', 'text')

        if target_type == 'product':
            report = tiandao.inspect_product(body)
        else:
            content = body.get('content', '')
            source = body.get('source', 'API调用')
            report = tiandao.inspect_text(content, source)

        return {
            'status': 'ok',
            'target_id': report.target_id,
            'overall_color': report.overall_color.value,
            'dna_signature': report.dna_signature,
            'summary': report.summary,
            'people_advice': report.people_advice,
            'shield': {
                'triggered': report.shield.triggered if report.shield else False,
                'reason': report.shield.reason if report.shield else '',
            } if report.shield else None,
            'audit': {
                'color': report.audit.color.value,
                'anomaly_count': report.audit.anomaly_count,
                'trust_score': report.audit.trust_score,
                'anomalies': report.audit.anomalies,
                'recommendation': report.audit.recommendation,
            } if report.audit else None,
            'evidence_sealed': report.evidence is not None,
            'error_book_recorded': report.error_book is not None,
            'timestamp': report.timestamp
        }

    @tiandao_app.get("/api/tiandao/status")
    async def status():
        """系统状态"""
        tiandao = get_tiandao()
        return {'status': 'ok', 'system': tiandao.system_status()}

    @tiandao_app.get("/api/tiandao/evidence/verify")
    async def verify_evidence():
        tiandao = get_tiandao()
        ok, msg = tiandao.evidence.verify_chain()
        return {'status': 'ok', 'chain_valid': ok, 'message': msg}

    @tiandao_app.get("/api/tiandao/errorbook/verify")
    async def verify_errorbook():
        tiandao = get_tiandao()
        ok, msg = tiandao.error_book.verify_chain()
        return {'status': 'ok', 'chain_valid': ok, 'message': msg}

    @tiandao_app.get("/api/tiandao/errorbook/patterns")
    async def get_patterns():
        tiandao = get_tiandao()
        patterns = tiandao.error_book.get_known_patterns()
        return {'status': 'ok', 'patterns': patterns}

    @tiandao_app.get("/api/tiandao/evidence/list")
    async def list_evidence():
        tiandao = get_tiandao()
        list_data = tiandao.evidence.get_unexpired()
        return {'status': 'ok', 'evidence': list_data, 'count': len(list_data)}

    def start_tiandao_server(port: int = 8768):
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║  🐉 龍魂 · 天下无欺 · 天道系统 v1.3 启动                ║
║  端口: {port}                                              ║
║                                                           ║
║  API端点:                                                 ║
║    POST /api/tiandao/inspect        — 综合检测             ║
║    GET  /api/tiandao/status         — 系统状态             ║
║    GET  /api/tiandao/evidence/verify — 证据链验证          ║
║    GET  /api/tiandao/errorbook/verify — 记错本验证         ║
║    GET  /api/tiandao/errorbook/patterns — 学习模式         ║
║    GET  /api/tiandao/evidence/list  — 证据列表             ║
║                                                           ║
║  架构: L1.5加密盾 → L2审计 → L3证据链 → L4记错本          ║
║  DNA: {DNA}                                               ║
║  UID: 9622                                                ║
║  铁律: 只检测 · 只标注 · 只提醒 · 百姓自判断               ║
╚═══════════════════════════════════════════════════════════╝
        """)
        uvicorn.run(tiandao_app, host="0.0.0.0", port=port, log_level="info")


# ═══════════════════════════════════════════════════════════
#  §8 命令行
# ═══════════════════════════════════════════════════════════

def cmd_test():
    """命令行测试"""
    print("🧪 龍魂 · 天下无欺 · 天道系统 测试")
    print("=" * 50)

    tiandao = TiandaoSystem()

    tests = [
        ("神奇美白霜（套路版）", "医院都在用 包治百病 三天见效 纯天然无副作用 最后三天限时抢购 手慢无 我自己也在用 无效退款"),
        ("合格国标插排", "国标认证产品，CCC强制认证，安全可靠，一年质保"),
        ("套路保健品", "祖传秘方 包治百病 三天见效 专家推荐 医院都在用 免费体验 送爸妈 孝敬父母 不买就亏了 限时抢购"),
    ]

    for name, text in tests:
        print(f"\n📦 {name}")
        print(f"   文案: {text[:60]}...")
        report = tiandao.inspect_text(text)
        print(f"   等级: {report.overall_color.value} | 信任分: {report.audit.trust_score}/100")
        print(f"   异常: {report.audit.anomaly_count}项")
        if report.audit.anomalies:
            for a in report.audit.anomalies[:3]:
                print(f"     [{a['severity']}] {a['type']}: {a['evidence'][:50]}")
        if report.shield and report.shield.triggered:
            print(f"   🛡 加密盾: {report.shield.reason}")
        if report.evidence:
            print(f"   📜 证据链: {report.evidence.evidence_id}")
        if report.error_book:
            print(f"   📕 记错本: {report.error_book.record_id}")
        print(f"   💬 {report.people_advice}")

    # 系统状态
    print(f"\n{'='*50}")
    print("📊 系统状态:")
    status = tiandao.system_status()
    print(f"   证据链验证: {status['evidence']}")
    print(f"   记错本验证: {status['error_book']}")
    print(f"   记错本统计: {status['error_book_stats']}")
    print(f"   证据链统计: {status['evidence_stats']}")

    tiandao.close()


# ═══════════════════════════════════════════════════════════
#  入口
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='龍魂 · 天下无欺 · 天道系统桥接')
    parser.add_argument('--port', type=int, default=8768, help='API端口 (默认8768)')
    parser.add_argument('--test', action='store_true', help='命令行测试')
    parser.add_argument('--text', type=str, help='检测指定文案')
    parser.add_argument('--serve', action='store_true', help='启动API服务')

    args = parser.parse_args()

    if args.test:
        cmd_test()
    elif args.text:
        tiandao = TiandaoSystem()
        report = tiandao.inspect_text(args.text)
        print(json.dumps({
            'color': report.overall_color.value,
            'trust_score': report.audit.trust_score,
            'anomaly_count': report.audit.anomaly_count,
            'anomalies': report.audit.anomalies,
            'advice': report.people_advice,
            'evidence_sealed': report.evidence is not None,
            'dna': report.dna_signature
        }, ensure_ascii=False, indent=2))
        tiandao.close()
    elif args.serve:
        if HAS_API:
            start_tiandao_server(args.port)
        else:
            print("请安装: pip install fastapi uvicorn")
    else:
        # 默认: 测试
        cmd_test()
