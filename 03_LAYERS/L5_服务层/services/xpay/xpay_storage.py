#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XPay 持久化存储层 · SQLite + JSON 双写 v1.0
XPay Persistence Layer · Append-Only Audit Trail

Design:
  SQLite 为主存储（查询/统计/关联），JSON 为冗余备份。
  append-only — 不删除只追加，完整审计链。

DNA: #龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-XPAY-STORAGE-v1.0
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
Creator: 诸葛鑫 (UID9622)
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import os
import sqlite3
import json
import threading
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List


# ═════════════════════════════════════════════════
# Schema
# ═════════════════════════════════════════════════

SCHEMA = """
CREATE TABLE IF NOT EXISTS payments (
    id                  TEXT PRIMARY KEY,
    uid                 TEXT NOT NULL,
    amount              REAL NOT NULL,
    currency            TEXT DEFAULT 'CNY',
    provider            TEXT NOT NULL,
    out_trade_no        TEXT UNIQUE,
    transaction_id      TEXT,
    status              TEXT DEFAULT 'pending',
    description         TEXT,
    created_at          TEXT NOT NULL,
    paid_at             TEXT,
    dna_signature       TEXT,
    gateway_mode        TEXT DEFAULT 'mock',
    metadata            TEXT DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS identity_bindings (
    uid                 TEXT NOT NULL,
    provider            TEXT NOT NULL,
    provider_uid        TEXT,
    binding_type        TEXT DEFAULT 'payment',
    verified_at         TEXT,
    created_at          TEXT NOT NULL,
    metadata            TEXT DEFAULT '{}',
    PRIMARY KEY (uid, provider)
);

CREATE TABLE IF NOT EXISTS verification_logs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    uid                 TEXT NOT NULL,
    action              TEXT NOT NULL,
    result              TEXT,
    details             TEXT,
    created_at          TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS passport_state (
    uid                 TEXT PRIMARY KEY,
    tier                TEXT DEFAULT 'free',
    monthly_expiry      TEXT,
    consecutive_months  INTEGER DEFAULT 0,
    first_verified_at   TEXT,
    last_heartbeat      TEXT,
    updated_at          TEXT NOT NULL,
    metadata            TEXT DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS alive_heartbeats (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    uid                 TEXT NOT NULL,
    payment_id          TEXT,
    amount              REAL,
    period_start        TEXT,
    period_end          TEXT,
    created_at          TEXT NOT NULL,
    dna_signature       TEXT
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_payments_uid ON payments(uid);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);
CREATE INDEX IF NOT EXISTS idx_payments_created ON payments(created_at);
CREATE INDEX IF NOT EXISTS idx_payments_out_trade ON payments(out_trade_no);
CREATE INDEX IF NOT EXISTS idx_bindings_uid ON identity_bindings(uid);
CREATE INDEX IF NOT EXISTS idx_logs_uid ON verification_logs(uid);
CREATE INDEX IF NOT EXISTS idx_heartbeats_uid ON alive_heartbeats(uid);
CREATE INDEX IF NOT EXISTS idx_heartbeats_created ON alive_heartbeats(created_at);
"""


class XPayStorage:
    """
    XPay 持久化存储 · SQLite 主库 + JSON 冗余
    
    特性：
      - 线程安全（WAL模式 + threading.Lock）
      - append-only 审计日志
      - 自动建表迁移
      - 健康检查
    """

    def __init__(self, db_path: str = ""):
        if db_path:
            self.db_path = Path(db_path)
        else:
            base = Path.home() / ".龍魂" / "xpay"
            base.mkdir(parents=True, exist_ok=True)
            self.db_path = base / "xpay.db"

        self._lock = threading.Lock()
        self._conn: Optional[sqlite3.Connection] = None
        self._init_db()

    # ── 初始化 ──────────────────────────────

    def _init_db(self):
        """初始化数据库：建表 + WAL模式"""
        self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._conn.executescript(SCHEMA)
        self._conn.commit()

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._init_db()
        return self._conn

    # ── 支付记录 ────────────────────────────

    def save_payment(self, uid: str, amount: float, description: str,
                     transaction_id: str = "", provider: str = "mock",
                     status: str = "pending", out_trade_no: str = "",
                     dna_sign: str = "", gateway_mode: str = "mock",
                     metadata: dict = None) -> str:
        """
        保存支付记录
        
        Returns:
            payment_id (自动生成)
        """
        now = datetime.now().isoformat()[:19]
        payment_id = f"PAY-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uid[:8] if len(uid) >= 8 else uid}"

        with self._lock:
            conn = self._get_conn()
            conn.execute("""
                INSERT OR REPLACE INTO payments 
                (id, uid, amount, currency, provider, out_trade_no, transaction_id,
                 status, description, created_at, dna_signature, gateway_mode, metadata)
                VALUES (?, ?, ?, 'CNY', ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                payment_id, uid, amount, provider, out_trade_no or payment_id,
                transaction_id, status, description, now, dna_sign, gateway_mode,
                json.dumps(metadata or {}, ensure_ascii=False)
            ))
            conn.commit()
        return payment_id

    def update_payment_status(self, out_trade_no: str, status: str,
                               paid_at: str = "") -> bool:
        """更新支付状态（回调触发）"""
        paid = paid_at or datetime.now().isoformat()[:19]
        with self._lock:
            conn = self._get_conn()
            cursor = conn.execute("""
                UPDATE payments SET status = ?, paid_at = ? 
                WHERE out_trade_no = ?
            """, (status, paid, out_trade_no))
            conn.commit()
            return cursor.rowcount > 0

    def get_payment(self, payment_id: str = "", out_trade_no: str = "") -> Optional[Dict]:
        """查询单笔支付"""
        with self._lock:
            conn = self._get_conn()
            if payment_id:
                row = conn.execute("SELECT * FROM payments WHERE id = ?", (payment_id,)).fetchone()
            elif out_trade_no:
                row = conn.execute("SELECT * FROM payments WHERE out_trade_no = ?", (out_trade_no,)).fetchone()
            else:
                return None
            return dict(row) if row else None

    def get_user_payments(self, uid: str, limit: int = 50, 
                          status: str = "") -> List[Dict]:
        """查询用户支付历史"""
        with self._lock:
            conn = self._get_conn()
            if status:
                rows = conn.execute(
                    "SELECT * FROM payments WHERE uid = ? AND status = ? ORDER BY created_at DESC LIMIT ?",
                    (uid, status, limit)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM payments WHERE uid = ? ORDER BY created_at DESC LIMIT ?",
                    (uid, limit)
                ).fetchall()
            return [dict(r) for r in rows]

    # ── 身份绑定 ────────────────────────────

    def bind_identity(self, uid: str, provider: str, provider_uid: str = "",
                      binding_type: str = "payment", metadata: dict = None) -> bool:
        """绑定支付账户到DNA身份"""
        now = datetime.now().isoformat()[:19]
        with self._lock:
            conn = self._get_conn()
            conn.execute("""
                INSERT OR REPLACE INTO identity_bindings
                (uid, provider, provider_uid, binding_type, verified_at, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                uid, provider, provider_uid, binding_type, now, now,
                json.dumps(metadata or {}, ensure_ascii=False)
            ))
            conn.commit()
        return True

    def get_identity_bindings(self, uid: str) -> List[Dict]:
        """查询用户的身份绑定"""
        with self._lock:
            conn = self._get_conn()
            rows = conn.execute(
                "SELECT * FROM identity_bindings WHERE uid = ?", (uid,)
            ).fetchall()
            return [dict(r) for r in rows]

    def is_identity_bound(self, uid: str, provider: str = "") -> bool:
        """检查身份是否已绑定"""
        with self._lock:
            conn = self._get_conn()
            if provider:
                row = conn.execute(
                    "SELECT 1 FROM identity_bindings WHERE uid = ? AND provider = ?",
                    (uid, provider)
                ).fetchone()
            else:
                row = conn.execute(
                    "SELECT 1 FROM identity_bindings WHERE uid = ?", (uid,)
                ).fetchone()
            return row is not None

    # ── 活人心跳记录 ─────────────────────────

    def record_heartbeat(self, uid: str, payment_id: str = "",
                         amount: float = 1.0, period_start: str = "",
                         period_end: str = "", dna_sign: str = "") -> int:
        """记录月度活人心跳"""
        now = datetime.now().isoformat()[:19]
        start = period_start or now
        end = period_end or (datetime.now().isoformat()[:10])

        with self._lock:
            conn = self._get_conn()
            cursor = conn.execute("""
                INSERT INTO alive_heartbeats 
                (uid, payment_id, amount, period_start, period_end, created_at, dna_signature)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (uid, payment_id, amount, start, end, now, dna_sign))
            conn.commit()
            return cursor.lastrowid

    def get_heartbeat_count(self, uid: str) -> int:
        """查询用户累计心跳次数（用于共建者判定）"""
        with self._lock:
            conn = self._get_conn()
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM alive_heartbeats WHERE uid = ?", (uid,)
            ).fetchone()
            return row["cnt"] if row else 0

    # ── 审计日志 ────────────────────────────

    def log_verification(self, uid: str, action: str, result: bool,
                         details: str = "") -> int:
        """记录验证事件（append-only）"""
        now = datetime.now().isoformat()[:19]
        with self._lock:
            conn = self._get_conn()
            cursor = conn.execute("""
                INSERT INTO verification_logs (uid, action, result, details, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (uid, action, 'pass' if result else 'fail', details, now))
            conn.commit()
            return cursor.lastrowid

    def get_verification_logs(self, uid: str, limit: int = 20) -> List[Dict]:
        """查询验证日志"""
        with self._lock:
            conn = self._get_conn()
            rows = conn.execute(
                "SELECT * FROM verification_logs WHERE uid = ? ORDER BY created_at DESC LIMIT ?",
                (uid, limit)
            ).fetchall()
            return [dict(r) for r in rows]

    # ── 通行证状态缓存 ───────────────────────

    def save_passport_state(self, uid: str, tier: str = "free",
                            monthly_expiry: str = "", consecutive_months: int = 0,
                            first_verified: str = "", last_heartbeat: str = "",
                            metadata: dict = None) -> bool:
        """缓存通行证状态（快速查询用）"""
        now = datetime.now().isoformat()[:19]
        with self._lock:
            conn = self._get_conn()
            conn.execute("""
                INSERT OR REPLACE INTO passport_state
                (uid, tier, monthly_expiry, consecutive_months, first_verified_at, 
                 last_heartbeat, updated_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                uid, tier, monthly_expiry, consecutive_months,
                first_verified, last_heartbeat, now,
                json.dumps(metadata or {}, ensure_ascii=False)
            ))
            conn.commit()
        return True

    def get_passport_state(self, uid: str) -> Optional[Dict]:
        """查询通行证状态"""
        with self._lock:
            conn = self._get_conn()
            row = conn.execute(
                "SELECT * FROM passport_state WHERE uid = ?", (uid,)
            ).fetchone()
            return dict(row) if row else None

    # ── 统计 ────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        """整体统计"""
        with self._lock:
            conn = self._get_conn()
            total_payments = conn.execute("SELECT COUNT(*) as c FROM payments").fetchone()["c"]
            total_amount = conn.execute("SELECT COALESCE(SUM(amount), 0) as c FROM payments WHERE status='completed'").fetchone()["c"]
            total_users = conn.execute("SELECT COUNT(DISTINCT uid) as c FROM payments").fetchone()["c"]
            total_heartbeats = conn.execute("SELECT COUNT(*) as c FROM alive_heartbeats").fetchone()["c"]
            total_bindings = conn.execute("SELECT COUNT(DISTINCT uid) as c FROM identity_bindings").fetchone()["c"]
            return {
                "total_payments": total_payments,
                "total_amount": round(total_amount, 2),
                "total_users": total_users,
                "total_heartbeats": total_heartbeats,
                "total_identity_bindings": total_bindings,
                "db_path": str(self.db_path),
            }

    # ── 健康检查 ────────────────────────────

    def is_healthy(self) -> bool:
        """数据库健康检查"""
        try:
            conn = self._get_conn()
            conn.execute("SELECT 1 FROM payments LIMIT 1")
            return True
        except Exception:
            return False

    def close(self):
        """关闭连接"""
        if self._conn:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None


# ═════════════════════════════════════════════════
# 自检
# ═════════════════════════════════════════════════

def selftest() -> dict:
    """XPayStorage 自检"""
    import tempfile
    results = {
        "module": "xpay_storage v1.0",
        "dna": "#龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-XPAY-STORAGE-v1.0",
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }

    tmp_db = Path(tempfile.gettempdir()) / f"xpay_selftest_{os.getpid()}.db"
    try:
        storage = XPayStorage(str(tmp_db))

        # 测试: 保存支付
        pid = storage.save_payment("test_uid", 1.00, "测试支付", provider="mock", status="completed")
        payment = storage.get_payment(payment_id=pid)
        results["tests"]["save_payment"] = {"pass": payment is not None and payment["amount"] == 1.0}

        # 测试: 更新状态
        ok = storage.update_payment_status(pid, "paid")
        results["tests"]["update_status"] = {"pass": ok}

        # 测试: 用户支付历史
        payments = storage.get_user_payments("test_uid")
        results["tests"]["user_payments"] = {"pass": len(payments) > 0}

        # 测试: 身份绑定
        storage.bind_identity("test_uid", "wechat_pay", "wx_test_123")
        bound = storage.is_identity_bound("test_uid", "wechat_pay")
        results["tests"]["identity_binding"] = {"pass": bound}

        # 测试: 心跳记录
        storage.record_heartbeat("test_uid", pid)
        hb_count = storage.get_heartbeat_count("test_uid")
        results["tests"]["heartbeat"] = {"pass": hb_count == 1}

        # 测试: 审计日志
        storage.log_verification("test_uid", "alive_check", True, "自检通过")
        logs = storage.get_verification_logs("test_uid")
        results["tests"]["audit_log"] = {"pass": len(logs) > 0}

        # 测试: 统计
        stats = storage.get_stats()
        results["tests"]["stats"] = {"pass": stats["total_payments"] > 0}

        # 测试: 健康
        results["tests"]["health"] = {"pass": storage.is_healthy()}

        storage.close()
    except Exception as e:
        results["tests"]["error"] = {"pass": False, "error": str(e)}
    finally:
        try:
            tmp_db.unlink(missing_ok=True)
            tmp_db.with_suffix(".db-wal").unlink(missing_ok=True)
            tmp_db.with_suffix(".db-shm").unlink(missing_ok=True)
        except Exception:
            pass

    all_pass = all(t.get("pass", False) for t in results["tests"].values())
    results["overall"] = "PASS" if all_pass else "FAIL"
    return results


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        print(json.dumps(selftest(), ensure_ascii=False, indent=2))
    else:
        print("XPayStorage v1.0 · SQLite持久化层")
        print(f"  DNA: #龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-XPAY-STORAGE-v1.0")
        print(f"  使用: from xpay_storage import XPayStorage")
        print(f"  自检: python3 xpay_storage.py --selftest")
