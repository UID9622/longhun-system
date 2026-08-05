#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🛡️ 龍魂DNA网络铁门系统 v1.0
“数字长城” —— 让网络行为过DNA，溯源到人，存证到链

DNA: #龍芯⚡️2026-08-02-NETWORK-IRON-DOOR-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

核心功能：
  1. DNA数字身份注册（GPG + e-CNY + 实名）
  2. 行为追溯码生成（每一条消息/操作打DNA标）
  3. 证据链验证（链上比对，揭穿伪造/栽赃）
  4. 防埋雷、防污点、防AI乱飘、防道德套路

用法:
  lh iron-door register --gpg "指纹" --payment "凭证" --name "姓名"
  lh iron-door trace --dna "DNA-XXX" --action "EMAIL" --content "Hello"
  lh iron-door verify --dna "DNA-XXX" --content "某句话" --time "2026-08-02 12:00:00"
  lh iron-door query --dna "DNA-XXX" --start "2026-08-01" --end "2026-08-03"
  lh iron-door api                     # 启动API服务 (FastAPI)
"""

import os
import sys
import json
import hashlib
import sqlite3
import datetime
import time
import argparse
import base64
import hmac
import secrets
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
import logging

# ─── 龍魂体系导入 ───
try:
    from cnsh_constants import (
        CNSH_369_ANCHOR, CNSH_FIVE_ELEMENTS, CNSH_TRIGRAM_MAP
    )
except ImportError:
    CNSH_369_ANCHOR = {"sn": 369, "log369": 5.911, "perm369": 108}
    CNSH_FIVE_ELEMENTS = ["金", "水", "木", "火", "土"]
    CNSH_TRIGRAM_MAP = {}

# ─── 配置 ───
HOME = Path.home()
LONGHUN_HOME = HOME / "longhun-system"
CONFIG_FILE = HOME / ".network_iron_door.conf"
DEFAULT_DB = LONGHUN_HOME / "data" / "iron_door.db"
LOG_DIR = LONGHUN_HOME / "logs"

# 确保数据目录存在
DEFAULT_DB.parent.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ─── 日志（双写：控制台 + 文件） ───
LOG_FILE = LOG_DIR / "iron_door.log"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8")
    ]
)
logger = logging.getLogger("iron_door")


# ================================================================
# 异常体系（统一错误码）
# ================================================================

class IronDoorError(Exception):
    """基础异常"""
    error_code: str = "IRON_DOOR_ERROR"
    http_status: int = 500


class IdentityError(IronDoorError):
    error_code = "IDENTITY_ERROR"
    http_status = 400


class TraceError(IronDoorError):
    error_code = "TRACE_ERROR"
    http_status = 400


class VerificationError(IronDoorError):
    error_code = "VERIFICATION_ERROR"
    http_status = 400


class ChainIntegrityError(IronDoorError):
    error_code = "CHAIN_INTEGRITY_ERROR"
    http_status = 500


class ConfigurationError(IronDoorError):
    error_code = "CONFIG_ERROR"
    http_status = 500


# ─── 错误码表（可对外暴露） ───
ERROR_CODES = {
    0: "操作成功",
    1001: "GPG指纹格式无效",
    1002: "支付凭证无效",
    1003: "实名信息缺失",
    1004: "DNA身份不存在或已禁用",
    1005: "DNA身份已注册（重复）",
    2001: "追溯内容为空",
    2002: "行为类型不支持",
    3001: "时间格式无效",
    3002: "链上记录不匹配（疑似栽赃）",
    3003: "链完整性校验失败",
    4001: "配置加载失败",
    5001: "内部错误",
}


# ================================================================
# 工具函数
# ================================================================

def now_iso() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


def today_str() -> str:
    return datetime.datetime.now().strftime("%Y%m%d")


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def sha256_file(filepath: str) -> str:
    """文件 SHA-256 哈希"""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def generate_random_id(length: int = 16) -> str:
    return secrets.token_hex(length // 2).upper()


def parse_time(time_str: str) -> datetime.datetime:
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d", "%Y%m%d%H%M%S", "%Y%m%d"):
        try:
            return datetime.datetime.strptime(time_str, fmt)
        except ValueError:
            continue
    raise VerificationError("时间格式无效，请使用 YYYY-MM-DD HH:MM:SS 或 YYYY-MM-DD")


def generate_dna_trace(prefix: str, action: str, uid: str, content_hash: str) -> str:
    """生成标准DNA追溯码"""
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return f"#龍芯⚡️{ts}-{action}-{uid}-{content_hash[:8].upper()}"


def action_type_to_element(action_type: str) -> str:
    """行为类型→五行映射"""
    mapping = {
        "REGISTER": "金", "CHAT": "水", "EMAIL": "水",
        "POST": "木", "AI": "火", "FILE": "土",
        "PAYMENT": "金", "CONTRACT": "金", "GOVERN": "火"
    }
    return mapping.get(action_type.upper(), "土")


# ================================================================
# 1. 数据模型层（ORM → SQLite / PostgreSQL）
# ================================================================

class Database:
    """单例数据库连接管理器 · 开发=SQLite · 生产=PostgreSQL"""
    _instance = None
    _conn = None
    _backend: str = "sqlite"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def configure(self, backend: str = "sqlite", connection_string: str = None):
        """切换后端：sqlite 或 postgresql"""
        self._backend = backend
        if connection_string:
            self._connection_string = connection_string
        if self._conn:
            self.close()

    def connect(self, db_path: str = str(DEFAULT_DB)):
        if self._conn:
            return self._conn

        if self._backend == "sqlite":
            self._conn = sqlite3.connect(db_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
        else:
            import psycopg2
            self._conn = psycopg2.connect(self._connection_string)
            self._conn.autocommit = False

        self._init_tables()
        logger.info(f"数据库连接: {self._backend} ({db_path if self._backend == 'sqlite' else self._connection_string})")
        return self._conn

    def _init_tables(self):
        c = self._conn.cursor()

        # 用户身份表
        c.execute("""
            CREATE TABLE IF NOT EXISTS identities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dna_id TEXT UNIQUE NOT NULL,
                gpg_fingerprint_hash TEXT NOT NULL,
                payment_proof_hash TEXT NOT NULL,
                real_name_hash TEXT NOT NULL,
                country TEXT DEFAULT 'CN',
                tier INTEGER DEFAULT 1,
                element TEXT DEFAULT '土',
                created_at TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                revocation_reason TEXT,
                extra TEXT
            )
        """)

        # 追溯码记录表
        c.execute("""
            CREATE TABLE IF NOT EXISTS traces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trace_code TEXT UNIQUE NOT NULL,
                dna_id TEXT NOT NULL,
                action_type TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                content_length INTEGER,
                element TEXT DEFAULT '土',
                timestamp TEXT NOT NULL,
                block_hash TEXT,
                previous_hash TEXT,
                extra TEXT,
                FOREIGN KEY(dna_id) REFERENCES identities(dna_id)
            )
        """)

        # 证据链表（互动哈希）
        c.execute("""
            CREATE TABLE IF NOT EXISTS evidence_chain (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interaction_hash TEXT UNIQUE NOT NULL,
                from_dna TEXT NOT NULL,
                to_dna TEXT,
                trace_code1 TEXT,
                trace_code2 TEXT,
                timestamp TEXT NOT NULL,
                verified INTEGER DEFAULT 0,
                extra TEXT
            )
        """)

        # 耻辱墙表（三分区：候选区/永久区/改造区）
        c.execute("""
            CREATE TABLE IF NOT EXISTS shame_wall (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dna_id TEXT NOT NULL,
                zone TEXT NOT NULL DEFAULT 'candidate',
                reason TEXT NOT NULL,
                evidence_hash TEXT,
                reported_at TEXT NOT NULL,
                moved_to_permanent_at TEXT,
                reviewed_by TEXT,
                auto_expire_at TEXT,
                FOREIGN KEY(dna_id) REFERENCES identities(dna_id)
            )
        """)

        # 操作日志表（审计·append-only）
        c.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                user_dna TEXT,
                details TEXT,
                timestamp TEXT NOT NULL,
                ip_address TEXT,
                session_id TEXT,
                result TEXT
            )
        """)

        # 配置表（运行时配置 key-value）
        c.execute("""
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # 索引
        c.execute("CREATE INDEX IF NOT EXISTS idx_traces_dna ON traces(dna_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_traces_time ON traces(timestamp)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_traces_hash ON traces(content_hash)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_audit_time ON audit_log(timestamp)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_audit_dna ON audit_log(user_dna)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_shame_dna ON shame_wall(dna_id)")

        self._conn.commit()
        logger.info("数据库表初始化完成·8表+6索引")

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None


db = Database()


# ================================================================
# 2. 区块链存证模拟器（可对接真实链：长安链/BSN/FISCO BCOS）
# ================================================================

class BlockchainSimulator:
    """
    模拟区块链存证，实际可替换为真实链。
    提供存证、查询、完整性验证、防篡改检测。
    链数据结构：prev_hash → current_block（哈希链）
    """

    def __init__(self):
        self.chain: List[Dict] = []
        self._init_chain()

    def _init_chain(self):
        conn = db.connect()
        c = conn.cursor()
        c.execute("SELECT trace_code, content_hash, timestamp, block_hash, previous_hash, extra FROM traces WHERE block_hash IS NOT NULL ORDER BY id ASC")
        rows = c.fetchall()
        for row in rows:
            try:
                extra = json.loads(row[5]) if row[5] else {}
            except json.JSONDecodeError:
                extra = {}
            self.chain.append({
                "trace_code": row[0],
                "content_hash": row[1],
                "timestamp": row[2],
                "block_hash": row[3],
                "previous_hash": row[4],
                "data": extra
            })
        logger.info(f"区块链加载 {len(self.chain)} 条存证")

    def record(self, trace_code: str, data: Dict) -> str:
        """存证一条记录，返回区块哈希（链式·不可篡改）"""
        prev_hash = self.chain[-1]["block_hash"] if self.chain else "0" * 64
        data_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        block_hash = hashlib.sha256((prev_hash + data_str).encode()).hexdigest()

        block = {
            "trace_code": trace_code,
            "content_hash": data.get("content_hash", ""),
            "timestamp": data.get("timestamp", now_iso()),
            "block_hash": block_hash,
            "previous_hash": prev_hash,
            "data": data
        }
        self.chain.append(block)

        # 持久化
        conn = db.connect()
        c = conn.cursor()
        c.execute(
            "UPDATE traces SET block_hash = ?, previous_hash = ? WHERE trace_code = ?",
            (block_hash, prev_hash, trace_code)
        )
        conn.commit()
        logger.info(f"⛓ 存证: {trace_code} → {block_hash[:12]}...")
        return block_hash

    def query_by_dna_time(self, dna_id: str, start_time: str, end_time: str) -> List[Dict]:
        conn = db.connect()
        c = conn.cursor()
        c.execute(
            """SELECT trace_code, content_hash, timestamp, block_hash, previous_hash, action_type, element, content_length
               FROM traces
               WHERE dna_id = ? AND timestamp >= ? AND timestamp <= ?
               ORDER BY timestamp ASC""",
            (dna_id, start_time, end_time)
        )
        return [dict(row) for row in c.fetchall()]

    def query_by_hash(self, content_hash: str, time_window_hours: int = 24) -> List[Dict]:
        """根据内容哈希追溯所有匹配记录"""
        since = (datetime.datetime.now() - datetime.timedelta(hours=time_window_hours)).isoformat()
        conn = db.connect()
        c = conn.cursor()
        c.execute(
            "SELECT trace_code, dna_id, timestamp, block_hash FROM traces WHERE content_hash = ? AND timestamp >= ?",
            (content_hash, since)
        )
        return [dict(row) for row in c.fetchall()]

    def verify_integrity(self) -> Tuple[bool, Optional[int]]:
        """验证整条链的完整性·返回(是否完整, 断裂位置)"""
        if len(self.chain) <= 1:
            return True, None
        for i in range(1, len(self.chain)):
            prev_block = self.chain[i - 1]
            curr_block = self.chain[i]
            if curr_block.get("previous_hash", "") != prev_block.get("block_hash", ""):
                return False, i
            data_str = json.dumps(curr_block["data"], sort_keys=True, ensure_ascii=False)
            computed = hashlib.sha256((prev_block["block_hash"] + data_str).encode()).hexdigest()
            if computed != curr_block["block_hash"]:
                return False, i
        return True, None

    def get_chain_length(self) -> int:
        return len(self.chain)

    def get_latest_block_hash(self) -> str:
        return self.chain[-1]["block_hash"][:12] + "..." if self.chain else "创世区块·空链"

    def export_chain(self, output_path: str):
        """导出完整链数据"""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump([{
                "index": i,
                "trace_code": b.get("trace_code"),
                "content_hash": b.get("content_hash"),
                "timestamp": b.get("timestamp"),
                "block_hash": b.get("block_hash"),
                "previous_hash": b.get("previous_hash"),
                "data": b.get("data", {})
            } for i, b in enumerate(self.chain)], f, ensure_ascii=False, indent=2)


blockchain = BlockchainSimulator()


# ================================================================
# 3. DNA身份注册中心
# ================================================================

class DNAIdentitySystem:
    """DNA数字身份注册·管理·吊销"""

    MIN_GPG_LENGTH = 40
    MIN_PAYMENT_LENGTH = 10
    SUPPORTED_COUNTRIES = ["CN", "HK", "MO", "TW"]

    @staticmethod
    def register(gpg_fingerprint: str, payment_proof: str,
                 real_name: str, country: str = "CN") -> Dict:
        """注册DNA数字身份"""
        # ─── 输入校验 ───
        if len(gpg_fingerprint.strip()) < DNAIdentitySystem.MIN_GPG_LENGTH:
            raise IdentityError(f"GPG指纹长度不足，至少{DNAIdentitySystem.MIN_GPG_LENGTH}位")

        payment_proof = payment_proof.strip()
        if not payment_proof or len(payment_proof) < DNAIdentitySystem.MIN_PAYMENT_LENGTH:
            raise IdentityError(f"支付凭证无效，需e-CNY交易哈希（至少{DNAIdentitySystem.MIN_PAYMENT_LENGTH}字符）")

        real_name = real_name.strip()
        if not real_name:
            raise IdentityError("实名信息不能为空")
        if country not in DNAIdentitySystem.SUPPORTED_COUNTRIES:
            logger.warning(f"非标准国家代码: {country}, 回退为 CN")
            country = "CN"

        # ─── 查重 ───
        conn = db.connect()
        c = conn.cursor()
        gpg_hash = sha256_hex(gpg_fingerprint)
        c.execute("SELECT dna_id FROM identities WHERE gpg_fingerprint_hash = ?", (gpg_hash,))
        if c.fetchone():
            raise IdentityError("该GPG指纹已注册")

        # ─── 生成DNA ID ───
        ts = int(time.time())
        raw = f"{gpg_fingerprint}{payment_proof}{real_name}{ts}"
        hash16 = sha256_hex(raw)[:16].upper()
        uid = gpg_fingerprint.strip().replace(" ", "")[:8].upper()
        tier = DNAIdentitySystem._calculate_tier(payment_proof)
        element = DNAIdentitySystem._calculate_element(real_name)
        dna_id = f"DNA-{uid}-T{tier}-{hash16}"

        # ─── 存储（只存哈希，保护隐私） ───
        real_name_hash = sha256_hex(real_name)
        payment_hash = sha256_hex(payment_proof)
        c.execute("""
            INSERT INTO identities
            (dna_id, gpg_fingerprint_hash, payment_proof_hash, real_name_hash, country, tier, element, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (dna_id, gpg_hash, payment_hash, real_name_hash, country, tier, element, now_iso()))
        conn.commit()

        # ─── 上链 ───
        blockchain.record(dna_id, {
            "type": "IDENTITY",
            "gpg_hash": gpg_hash,
            "country": country,
            "tier": tier,
            "element": element,
            "timestamp": now_iso()
        })

        # ─── 审计 ───
        DNAIdentitySystem._audit("IDENTITY_REGISTER", dna_id, {
            "country": country, "tier": tier, "element": element
        }, result="SUCCESS")

        logger.info(f"✅ 注册: {dna_id} (T{tier}·{element})")
        return {
            "status": "success",
            "dna_id": dna_id,
            "tier": tier,
            "element": element,
            "country": country,
            "created_at": now_iso()
        }

    @staticmethod
    def lookup(dna_id: str) -> Dict:
        """查询DNA身份信息（脱敏）"""
        conn = db.connect()
        c = conn.cursor()
        c.execute("""
            SELECT dna_id, country, tier, element, created_at, is_active, revocation_reason
            FROM identities WHERE dna_id = ?
        """, (dna_id,))
        row = c.fetchone()
        if not row:
            raise IdentityError(f"DNA身份不存在: {dna_id}")
        return dict(row)

    @staticmethod
    def revoke(dna_id: str, reason: str, operator_dna: str):
        """吊销DNA身份（软删除·冻结不删除）"""
        conn = db.connect()
        c = conn.cursor()
        c.execute("""
            UPDATE identities SET is_active = 0, revocation_reason = ?, extra = json_set(coalesce(extra,'{}'), '$.revoked_by', ?)
            WHERE dna_id = ?
        """, (reason, operator_dna, dna_id))
        conn.commit()
        DNAIdentitySystem._audit("IDENTITY_REVOKE", dna_id, {"reason": reason, "by": operator_dna}, result="SUCCESS")
        logger.warning(f"🔒 吊销: {dna_id} | 原因: {reason}")

    @staticmethod
    def list_all(active_only: bool = True) -> List[Dict]:
        """列出所有DNA身份"""
        conn = db.connect()
        c = conn.cursor()
        cond = "WHERE is_active=1" if active_only else ""
        c.execute(f"SELECT dna_id, country, tier, element, created_at, is_active FROM identities {cond} ORDER BY created_at DESC")
        return [dict(row) for row in c.fetchall()]

    @staticmethod
    def _calculate_tier(payment_proof: str) -> int:
        """根据支付凭证计算信任层级 (1-3)"""
        # 简化版：凭证长度+复杂度决定层级
        score = len(payment_proof) + sum(1 for c in payment_proof if c.isupper())
        if score >= 80: return 3
        elif score >= 50: return 2
        return 1

    @staticmethod
    def _calculate_element(real_name: str) -> str:
        """根据姓名计算五行属性"""
        code = sum(ord(c) for c in real_name)
        elements = ["金", "水", "木", "火", "土"]
        return elements[code % 5]

    @staticmethod
    def _audit(action: str, user_dna: str, details: Dict = None, result: str = "UNKNOWN"):
        conn = db.connect()
        c = conn.cursor()
        c.execute("""
            INSERT INTO audit_log (action, user_dna, details, timestamp, result)
            VALUES (?, ?, ?, ?, ?)
        """, (action, user_dna, json.dumps(details or {}, ensure_ascii=False), now_iso(), result))
        conn.commit()


# ================================================================
# 4. DNA追溯码生成器
# ================================================================

class DNATraceGenerator:
    """行为追溯码生成器"""

    VALID_ACTIONS = {"EMAIL", "CHAT", "POST", "AI", "FILE", "PAYMENT", "CONTRACT", "GOVERN", "REGISTER"}

    @staticmethod
    def generate_trace(dna_id: str, action_type: str, content: str,
                       extra: Dict = None, content_is_file: bool = False) -> Dict:
        """生成行为追溯码"""
        action_type = action_type.upper().strip()
        if action_type not in DNATraceGenerator.VALID_ACTIONS:
            logger.warning(f"未知行为类型: {action_type}，使用 FILE 兜底")
            action_type = "FILE"
        if not content:
            raise TraceError("追溯内容不能为空")

        # 验证DNA
        conn = db.connect()
        c = conn.cursor()
        c.execute("SELECT dna_id, element FROM identities WHERE dna_id = ? AND is_active=1", (dna_id,))
        identity = c.fetchone()
        if not identity:
            raise IdentityError(f"DNA身份不存在或已禁用: {dna_id}")

        # 计算内容哈希
        if content_is_file and os.path.isfile(content):
            content_hash = sha256_file(content)
            content_len = os.path.getsize(content)
        else:
            content_hash = sha256_hex(content)
            content_len = len(content)

        uid_part = dna_id.split("-")[1]
        trace_code = generate_dna_trace("#龍芯", action_type, uid_part, content_hash)
        element = action_type_to_element(action_type)

        # 存储
        c.execute("""
            INSERT INTO traces (trace_code, dna_id, action_type, content_hash, content_length, element, timestamp, extra)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (trace_code, dna_id, action_type, content_hash, content_len, element, now_iso(), json.dumps(extra or {})))
        conn.commit()

        # 上链
        blockchain.record(trace_code, {
            "content_hash": content_hash,
            "timestamp": now_iso(),
            "action": action_type,
            "dna": dna_id,
            "element": element,
            "content_length": content_len
        })

        DNAIdentitySystem._audit("TRACE_GENERATE", dna_id, {
            "trace_code": trace_code, "action_type": action_type, "element": element
        }, result="SUCCESS")

        logger.info(f"🔗 追溯: {trace_code} [{action_type}]")
        return {
            "trace_code": trace_code,
            "content_hash": content_hash,
            "content_length": content_len,
            "timestamp": now_iso(),
            "dna_id": dna_id,
            "action_type": action_type,
            "element": element
        }

    @staticmethod
    def get_trace_history(dna_id: str, limit: int = 100) -> List[Dict]:
        conn = db.connect()
        c = conn.cursor()
        c.execute(
            "SELECT trace_code, action_type, content_hash, timestamp, element FROM traces WHERE dna_id = ? ORDER BY id DESC LIMIT ?",
            (dna_id, limit)
        )
        return [dict(row) for row in c.fetchall()]


# ================================================================
# 5. 证据链验证系统
# ================================================================

class EvidenceChainVerifier:
    """证据链验证系统"""

    @staticmethod
    def verify_claim(accused_dna: str, claim_content: str,
                     claim_time: str, time_window: int = 3600) -> Dict:
        """
        验证指控真伪
        - accused_dna: 被指控者的DNA
        - claim_content: 指控的内容原文
        - claim_time: 声称时间
        - time_window: 时间窗口（秒），默认1小时
        """
        try:
            dt = parse_time(claim_time)
        except VerificationError:
            raise VerificationError("时间格式无效")

        start_dt = dt - datetime.timedelta(seconds=time_window)
        end_dt = dt + datetime.timedelta(seconds=time_window)
        start_str = start_dt.isoformat(timespec="seconds")
        end_str = end_dt.isoformat(timespec="seconds")

        records = blockchain.query_by_dna_time(accused_dna, start_str, end_str)
        claim_hash = sha256_hex(claim_content)

        for rec in records:
            if rec["content_hash"] == claim_hash:
                return {
                    "result": "VERIFIED",
                    "message": "✅ 链上存证确认，指控内容属实",
                    "evidence": {
                        "trace_code": rec["trace_code"],
                        "timestamp": rec["timestamp"],
                        "block_hash": rec["block_hash"],
                        "action_type": rec.get("action_type", "UNKNOWN"),
                        "element": rec.get("element", "土")
                    },
                    "matched": True
                }

        # 扩大窗口再试一次（24小时）
        if time_window < 86400:
            return EvidenceChainVerifier.verify_claim(accused_dna, claim_content, claim_time, 86400)

        return {
            "result": "FALSE_CLAIM",
            "message": "❌ 链上无此记录，疑似栽赃或伪造",
            "suggestion": "建议反诉诬告，提供司法鉴定；同时扩大时间范围复查",
            "matched": False
        }

    @staticmethod
    def build_interaction_hash(from_dna: str, to_dna: str,
                               trace1: str, trace2: str) -> str:
        """构建互动证据链（双方互动哈希）"""
        raw = f"{from_dna}|{to_dna}|{trace1}|{trace2}|{now_iso()}"
        ihash = sha256_hex(raw)
        conn = db.connect()
        c = conn.cursor()
        c.execute("""
            INSERT INTO evidence_chain (interaction_hash, from_dna, to_dna, trace_code1, trace_code2, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ihash, from_dna, to_dna, trace1, trace2, now_iso()))
        conn.commit()

        DNAIdentitySystem._audit("INTERACTION_RECORD", from_dna, {
            "to": to_dna, "trace1": trace1, "trace2": trace2, "interaction_hash": ihash
        }, result="SUCCESS")
        return ihash

    @staticmethod
    def verify_interaction(ihash: str) -> Dict:
        """验证互动哈希是否存在"""
        conn = db.connect()
        c = conn.cursor()
        c.execute(
            "SELECT from_dna, to_dna, trace_code1, trace_code2, timestamp FROM evidence_chain WHERE interaction_hash = ?",
            (ihash,)
        )
        row = c.fetchone()
        if not row:
            return {"result": "NOT_FOUND", "message": "互动记录不存在"}
        return {"result": "VERIFIED", "message": "互动记录确认", "data": dict(row)}


# ================================================================
# 6. 耻辱墙（三分区：候选区·永久区·改造区）
# ================================================================

class ShameWall:
    """数字身份耻辱墙"""

    ZONES = {"candidate": "候选区", "permanent": "永久区", "reformed": "改造区"}

    @staticmethod
    def report(dna_id: str, reason: str, evidence_hash: str = None, auto_expire_days: int = 90):
        """举报一个DNA到耻辱墙候选区"""
        conn = db.connect()
        c = conn.cursor()
        # 验证DNA存在
        c.execute("SELECT dna_id FROM identities WHERE dna_id = ?", (dna_id,))
        if not c.fetchone():
            raise IdentityError(f"DNA身份不存在: {dna_id}")

        expire_at = (datetime.datetime.now() + datetime.timedelta(days=auto_expire_days)).isoformat()
        c.execute("""
            INSERT INTO shame_wall (dna_id, zone, reason, evidence_hash, reported_at, auto_expire_at)
            VALUES (?, 'candidate', ?, ?, ?, ?)
        """, (dna_id, reason, evidence_hash, now_iso(), expire_at))
        conn.commit()
        DNAIdentitySystem._audit("SHAME_REPORT", dna_id, {"reason": reason, "zone": "candidate"}, result="SUCCESS")
        logger.warning(f"⚡ 耻辱墙: {dna_id} 进入候选区 | {reason}")

    @staticmethod
    def promote_to_permanent(dna_id: str, reviewer_dna: str):
        """提升到永久区（需审核人DNA）"""
        conn = db.connect()
        c = conn.cursor()
        c.execute("""
            UPDATE shame_wall SET zone = 'permanent', moved_to_permanent_at = ?, reviewed_by = ?
            WHERE dna_id = ? AND zone = 'candidate'
        """, (now_iso(), reviewer_dna, dna_id))
        conn.commit()
        DNAIdentitySystem._audit("SHAME_PROMOTE", dna_id, {"by": reviewer_dna, "to": "permanent"}, result="SUCCESS")

    @staticmethod
    def mark_reformed(dna_id: str, reviewer_dna: str):
        """标记已改造（移到改造区）"""
        conn = db.connect()
        c = conn.cursor()
        c.execute("""
            UPDATE shame_wall SET zone = 'reformed', reviewed_by = ?
            WHERE dna_id = ? AND zone IN ('candidate', 'permanent')
        """, (reviewer_dna, dna_id))
        conn.commit()
        DNAIdentitySystem._audit("SHAME_REFORMED", dna_id, {"by": reviewer_dna}, result="SUCCESS")

    @staticmethod
    def query(dna_id: str) -> List[Dict]:
        conn = db.connect()
        c = conn.cursor()
        c.execute("SELECT zone, reason, reported_at, reviewed_by FROM shame_wall WHERE dna_id = ?", (dna_id,))
        return [dict(row) for row in c.fetchall()]

    @staticmethod
    def list_zone(zone: str = "candidate") -> List[Dict]:
        conn = db.connect()
        c = conn.cursor()
        c.execute(
            "SELECT dna_id, reason, reported_at, auto_expire_at FROM shame_wall WHERE zone = ? ORDER BY reported_at DESC",
            (zone,)
        )
        return [dict(row) for row in c.fetchall()]


# ================================================================
# 7. 监控与统计仪表盘
# ================================================================

class Dashboard:
    """系统仪表盘：统计·健康·实时状态"""

    @staticmethod
    def get_stats() -> Dict:
        conn = db.connect()
        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM identities")
        total_identities = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM identities WHERE is_active = 1")
        active_identities = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM traces")
        total_traces = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM traces WHERE timestamp >= ?",
                  ((datetime.datetime.now() - datetime.timedelta(hours=24)).isoformat(),))
        traces_24h = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM evidence_chain")
        total_evidence = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM audit_log WHERE timestamp >= ?",
                  ((datetime.datetime.now() - datetime.timedelta(hours=24)).isoformat(),))
        audits_24h = c.fetchone()[0]

        chain_ok, break_at = blockchain.verify_integrity()

        return {
            "identities": {"total": total_identities, "active": active_identities},
            "traces": {"total": total_traces, "last_24h": traces_24h},
            "evidence_chain": {"total": total_evidence},
            "blockchain": {"length": blockchain.get_chain_length(), "integrity": chain_ok, "break_at": break_at},
            "audits_24h": audits_24h,
            "latest_block": blockchain.get_latest_block_hash(),
            "timestamp": now_iso()
        }


# ================================================================
# 8. 配置文件管理
# ================================================================

class ConfigManager:
    """统一配置管理：环境变量 > 配置文件 > 数据库 > 默认值"""

    DEFAULTS = {
        "db_path": str(DEFAULT_DB),
        "api_host": "0.0.0.0",
        "api_port": "8010",
        "log_level": "INFO",
        "blockchain_backend": "simulator",
        "blockchain_endpoint": "",
        "evidence_retention_days": "3650",
        "shame_wall_auto_expire_days": "90",
        "verify_default_window_hours": "1",
    }

    @staticmethod
    def load() -> Dict:
        config = dict(ConfigManager.DEFAULTS)

        # 1. 从数据库加载
        try:
            conn = db.connect()
            c = conn.cursor()
            c.execute("SELECT key, value FROM config")
            for row in c.fetchall():
                config[row[0]] = row[1]
        except Exception:
            pass

        # 2. 从配置文件加载（覆盖数据库）
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            config[k.strip()] = v.strip().strip('"').strip("'")
            except Exception:
                pass

        # 3. 环境变量覆盖（最高优先级）
        for key in config:
            env_key = f"IRON_DOOR_{key.upper()}"
            if env_key in os.environ:
                config[key] = os.environ[env_key]

        return config

    @staticmethod
    def set(key: str, value: str):
        conn = db.connect()
        c = conn.cursor()
        c.execute(
            "INSERT OR REPLACE INTO config (key, value, updated_at) VALUES (?, ?, ?)",
            (key, value, now_iso())
        )
        conn.commit()


# ================================================================
# 9. API 服务（FastAPI）
# ================================================================

def run_api_server(host="0.0.0.0", port=8010):
    try:
        from fastapi import FastAPI, HTTPException, Query
        from fastapi.middleware.cors import CORSMiddleware
        from pydantic import BaseModel, Field
        import uvicorn
    except ImportError:
        print("请先安装: pip install fastapi uvicorn pydantic")
        sys.exit(1)

    app = FastAPI(
        title="龍魂DNA网络铁门系统",
        description="数字长城 · 溯源到人 · 存证到链 · 防埋雷防栽赃",
        version="1.0"
    )
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    # ─── 请求模型 ───
    class RegisterRequest(BaseModel):
        gpg_fingerprint: str = Field(..., min_length=40)
        payment_proof: str = Field(..., min_length=10)
        real_name: str = Field(..., min_length=1)
        country: str = "CN"

    class TraceRequest(BaseModel):
        dna_id: str
        action_type: str = Field(..., pattern=r"^(EMAIL|CHAT|POST|AI|FILE|PAYMENT|CONTRACT|GOVERN)$")
        content: str
        extra: Optional[Dict] = None

    class VerifyClaimRequest(BaseModel):
        accused_dna: str
        claim_content: str
        claim_time: str
        time_window: int = 3600

    class ShameReportRequest(BaseModel):
        dna_id: str
        reason: str
        evidence_hash: str = None
        auto_expire_days: int = 90

    # ─── 接口 ───
    @app.post("/api/v1/identity/register")
    def api_register(req: RegisterRequest):
        try:
            result = DNAIdentitySystem.register(req.gpg_fingerprint, req.payment_proof, req.real_name, req.country)
            return {"code": 0, "message": "注册成功", "data": result}
        except IronDoorError as e:
            raise HTTPException(status_code=e.http_status, detail={"code": e.error_code, "message": str(e)})

    @app.get("/api/v1/identity/{dna_id}")
    def api_lookup(dna_id: str):
        try:
            return {"code": 0, "data": DNAIdentitySystem.lookup(dna_id)}
        except IronDoorError as e:
            raise HTTPException(status_code=e.http_status, detail={"code": e.error_code, "message": str(e)})

    @app.get("/api/v1/identity/list")
    def api_list(active_only: bool = True):
        return {"code": 0, "data": DNAIdentitySystem.list_all(active_only)}

    @app.post("/api/v1/trace/generate")
    def api_trace(req: TraceRequest):
        try:
            result = DNATraceGenerator.generate_trace(req.dna_id, req.action_type, req.content, req.extra)
            return {"code": 0, "message": "追溯码已生成", "data": result}
        except IronDoorError as e:
            raise HTTPException(status_code=e.http_status, detail={"code": e.error_code, "message": str(e)})

    @app.post("/api/v1/evidence/verify")
    def api_verify(req: VerifyClaimRequest):
        try:
            result = EvidenceChainVerifier.verify_claim(req.accused_dna, req.claim_content, req.claim_time, req.time_window)
            return {"code": 0, "data": result}
        except IronDoorError as e:
            raise HTTPException(status_code=e.http_status, detail={"code": e.error_code, "message": str(e)})

    @app.post("/api/v1/evidence/build-interaction")
    def api_build_interaction(from_dna: str, to_dna: str, trace1: str, trace2: str):
        ihash = EvidenceChainVerifier.build_interaction_hash(from_dna, to_dna, trace1, trace2)
        return {"code": 0, "interaction_hash": ihash}

    @app.get("/api/v1/evidence/query")
    def api_query(dna_id: str, start: str, end: str):
        records = blockchain.query_by_dna_time(dna_id, start, end)
        return {"code": 0, "data": records, "count": len(records)}

    @app.post("/api/v1/shame/report")
    def api_shame_report(req: ShameReportRequest):
        ShameWall.report(req.dna_id, req.reason, req.evidence_hash, req.auto_expire_days)
        return {"code": 0, "message": "已加入耻辱墙候选区"}

    @app.get("/api/v1/shame/query/{dna_id}")
    def api_shame_query(dna_id: str):
        return {"code": 0, "data": ShameWall.query(dna_id)}

    @app.get("/api/v1/dashboard")
    def api_dashboard():
        return {"code": 0, "data": Dashboard.get_stats()}

    @app.get("/api/v1/health")
    def health():
        chain_ok, break_at = blockchain.verify_integrity()
        return {
            "status": "ok" if chain_ok else "degraded",
            "chain_integrity": chain_ok,
            "chain_length": blockchain.get_chain_length(),
            "latest_block": blockchain.get_latest_block_hash(),
            "break_at": break_at,
            "db_path": str(DEFAULT_DB)
        }

    @app.get("/api/v1/stats")
    def stats():
        return {"code": 0, "data": Dashboard.get_stats()}

    print(f"🚀 网络铁门API启动: http://{host}:{port}")
    print(f"📖 API文档: http://{host}:{port}/docs")
    print(f"🔍 健康检查: http://{host}:{port}/api/v1/health")
    uvicorn.run(app, host=host, port=port, log_level="info")


# ================================================================
# 10. 命令行工具（子命令模式）
# ================================================================

def cmd_register(args):
    """lh iron-door register"""
    result = DNAIdentitySystem.register(args.gpg, args.payment, args.name, args.country)
    _output(result, args.json, f"✅ 注册成功！DNA ID: {result['dna_id']}\n   层级: T{result['tier']} · 五行: {result['element']}")


def cmd_trace(args):
    """lh iron-door trace"""
    result = DNATraceGenerator.generate_trace(args.dna, args.action, args.content, json.loads(args.extra) if args.extra else None)
    _output(result, args.json, f"🔗 追溯码: {result['trace_code']}\n   内容哈希: {result['content_hash']}\n   五行属性: {result['element']}")


def cmd_verify(args):
    """lh iron-door verify"""
    result = EvidenceChainVerifier.verify_claim(args.dna, args.content, args.time, args.window)
    _output(result, args.json, f"📋 验证结果: {result['result']}\n   {result['message']}" + (
        f"\n   匹配记录: {result['evidence']['trace_code']} @ {result['evidence']['timestamp']}" if result.get('matched') else f"\n   建议: {result['suggestion']}"
    ))


def cmd_query(args):
    """lh iron-door query"""
    records = blockchain.query_by_dna_time(args.dna, args.start, args.end)
    _output(records, args.json, f"📊 DNA {args.dna} 在 {args.start} 至 {args.end} 的记录 ({len(records)}条):\n" + "\n".join(f"   {r['timestamp']} [{r.get('action_type','?')}] {r['trace_code']}" for r in records))


def cmd_stats(args):
    """lh iron-door stats"""
    data = Dashboard.get_stats()
    _output(data, args.json, f"📊 系统统计\n   身份: {data['identities']['active']}/{data['identities']['total']} 活跃\n   追溯: {data['traces']['total']} 总·{data['traces']['last_24h']} 24h\n   链长: {data['blockchain']['length']} 块·完整: {data['blockchain']['integrity']}\n   审计: {data['audits_24h']} 次/24h")


def cmd_shame(args):
    """lh iron-door shame"""
    if args.shame_action == "list":
        zone = args.zone or "candidate"
        entries = ShameWall.list_zone(zone)
        _output(entries, args.json, f"📛 耻辱墙·{zone}区 ({len(entries)}条):\n" + "\n".join(f"   {e['dna_id']} | {e['reason'][:40]}... | {e['reported_at']}" for e in entries))
    elif args.shame_action == "query":
        entries = ShameWall.query(args.dna)
        _output(entries, args.json, f"📛 DNA {args.dna} 耻辱记录:\n" + "\n".join(f"   [{e['zone']}] {e['reason']} | {e['reported_at']}" for e in entries))


def cmd_chain(args):
    """lh iron-door chain"""
    ok, at = blockchain.verify_integrity()
    print(f"⛓ 链完整性: {'✅ 完整' if ok else f'❌ 断裂于 #{at}'}")
    print(f"   链长: {blockchain.get_chain_length()} 块")
    print(f"   最新区块: {blockchain.get_latest_block_hash()}")
    if args.export:
        path = args.export
        blockchain.export_chain(path)
        print(f"   已导出: {path}")


def cmd_lookup(args):
    """lh iron-door lookup"""
    data = DNAIdentitySystem.lookup(args.dna)
    _output(data, args.json, f"🔍 DNA: {data['dna_id']}\n   状态: {'🟢活跃' if data['is_active'] else '🔴冻结'} | T{data['tier']} | {data['element']} | {data['country']}\n   创建: {data['created_at']}")


def _output(data, as_json: bool, text: str):
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(text)


def main():
    parser = argparse.ArgumentParser(
        prog="lh iron-door",
        description="🛡️ 龍魂DNA网络铁门系统 v1.0 —— 数字长城",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh iron-door register --gpg A2D0... --payment eCNY_xxx --name '张三'
  lh iron-door trace --dna DNA-XXX --action EMAIL --content "项目合作"
  lh iron-door verify --dna DNA-XXX --content "某句话" --time "2026-08-02 12:00"
  lh iron-door stats
  lh iron-door api --port 8010
        """
    )
    sub = parser.add_subparsers(dest="command", help="子命令")

    # register
    p_reg = sub.add_parser("register", aliases=["reg"], help="注册DNA数字身份")
    p_reg.add_argument("--gpg", required=True, help="GPG指纹 (≥40位)")
    p_reg.add_argument("--payment", required=True, help="e-CNY支付凭证")
    p_reg.add_argument("--name", required=True, help="实名")
    p_reg.add_argument("--country", default="CN")
    p_reg.add_argument("--json", action="store_true")

    # trace
    p_tr = sub.add_parser("trace", help="生成行为追溯码")
    p_tr.add_argument("--dna", required=True)
    p_tr.add_argument("--action", required=True, help="EMAIL/CHAT/POST/AI/FILE/PAYMENT/CONTRACT/GOVERN")
    p_tr.add_argument("--content", required=True)
    p_tr.add_argument("--extra")
    p_tr.add_argument("--json", action="store_true")

    # verify
    p_ve = sub.add_parser("verify", help="验证指控真伪")
    p_ve.add_argument("--dna", required=True)
    p_ve.add_argument("--content", required=True)
    p_ve.add_argument("--time", required=True, help="声称时间 (YYYY-MM-DD HH:MM:SS)")
    p_ve.add_argument("--window", type=int, default=3600, help="时间窗口(秒)")
    p_ve.add_argument("--json", action="store_true")

    # query
    p_q = sub.add_parser("query", help="查询DNA历史追溯记录")
    p_q.add_argument("--dna", required=True)
    p_q.add_argument("--start", required=True)
    p_q.add_argument("--end", required=True)
    p_q.add_argument("--json", action="store_true")

    # lookup
    p_lu = sub.add_parser("lookup", help="查询DNA身份信息")
    p_lu.add_argument("--dna", required=True)
    p_lu.add_argument("--json", action="store_true")

    # stats
    p_st = sub.add_parser("stats", help="系统统计仪表盘")
    p_st.add_argument("--json", action="store_true")

    # shame
    p_sh = sub.add_parser("shame", help="耻辱墙管理")
    p_sh.add_argument("shame_action", nargs="?", default="list", choices=["list", "query"], help="list=列出某区 | query=查某人")
    p_sh.add_argument("--zone", default="candidate", choices=["candidate", "permanent", "reformed"])
    p_sh.add_argument("--dna")
    p_sh.add_argument("--json", action="store_true")

    # chain
    p_ch = sub.add_parser("chain", help="区块链状态")
    p_ch.add_argument("--export", help="导出链数据到文件")

    # api
    p_api = sub.add_parser("api", help="启动API服务")
    p_api.add_argument("--host", default="0.0.0.0")
    p_api.add_argument("--port", type=int, default=8010)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 数据库初始化
    db.connect()

    try:
        if args.command in ("register", "reg"):
            cmd_register(args)
        elif args.command == "trace":
            cmd_trace(args)
        elif args.command == "verify":
            cmd_verify(args)
        elif args.command == "query":
            cmd_query(args)
        elif args.command == "lookup":
            cmd_lookup(args)
        elif args.command == "stats":
            cmd_stats(args)
        elif args.command == "shame":
            cmd_shame(args)
        elif args.command == "chain":
            cmd_chain(args)
        elif args.command == "api":
            run_api_server(args.host, args.port)
    except IronDoorError as e:
        print(f"❌ [{e.error_code}] {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception("未预期错误")
        print(f"💥 内部错误: {e}")
        sys.exit(2)
    finally:
        db.close()


if __name__ == "__main__":
    main()
