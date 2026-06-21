#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交易數據結構與持久化
DNA:#龍芯⚡️2026-06-17-XPAY-TRANSACTION-FILE1-v2.0
"""
import json
import sqlite3
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Transaction:
    tx_id: str
    amount: float
    currency: str
    sender_id: str
    recipient_id: str
    status: str           # pending / completed / failed / rolled_back
    memo: str
    processing_fee: float
    dna_fee: float
    total_fee: float
    created_at: str
    dna_signature: str
    settlement_ref: str
    sovereign_country: str


class TransactionStore:
    """SQLite 交易存儲，append-only"""

    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            db_path = Path(__file__).resolve().parents[2] / "var" / "xpay.db"
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    tx_id TEXT PRIMARY KEY,
                    amount REAL NOT NULL,
                    currency TEXT NOT NULL,
                    sender_id TEXT NOT NULL,
                    recipient_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    memo TEXT,
                    processing_fee REAL NOT NULL,
                    dna_fee REAL NOT NULL,
                    total_fee REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    dna_signature TEXT NOT NULL,
                    settlement_ref TEXT NOT NULL,
                    sovereign_country TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_currency ON transactions(currency)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_created ON transactions(created_at)
            """)

    def save(self, tx: Transaction):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO transactions
                (tx_id, amount, currency, sender_id, recipient_id, status, memo,
                 processing_fee, dna_fee, total_fee, created_at, dna_signature,
                 settlement_ref, sovereign_country)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                tx.tx_id, tx.amount, tx.currency, tx.sender_id, tx.recipient_id,
                tx.status, tx.memo, tx.processing_fee, tx.dna_fee, tx.total_fee,
                tx.created_at, tx.dna_signature, tx.settlement_ref, tx.sovereign_country
            ))

    def get(self, tx_id: str) -> Optional[Transaction]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT * FROM transactions WHERE tx_id = ?", (tx_id,)
            ).fetchone()
        if not row:
            return None
        return Transaction(*row)

    def list_all(self, limit: int = 100) -> List[Transaction]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT * FROM transactions ORDER BY created_at DESC LIMIT ?",
                (limit,)
            ).fetchall()
        return [Transaction(*row) for row in rows]

    def stats(self) -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute(
                "SELECT COUNT(*), COALESCE(SUM(amount), 0), COALESCE(SUM(total_fee), 0) FROM transactions"
            ).fetchone()
            currencies = conn.execute(
                "SELECT currency, COUNT(*), SUM(amount) FROM transactions GROUP BY currency"
            ).fetchall()
        return {
            "transaction_count": total[0],
            "total_volume": round(total[1], 4),
            "total_dna_fees": round(total[2], 4),
            "currencies": {c[0]: {"count": c[1], "volume": round(c[2], 4)} for c in currencies},
        }

    def migrate_json(self, json_path: Path):
        """從舊版 transactions.json 遷移數據"""
        if not json_path.exists():
            return 0
        data = json.loads(json_path.read_text(encoding="utf-8"))
        migrated = 0
        for tx in data.get("history", []):
            existing = self.get(tx.get("id"))
            if existing:
                continue
            tx_obj = Transaction(
                tx_id=tx.get("id", ""),
                amount=float(tx.get("amount", 0) or 0),
                currency=tx.get("currency", "CNY"),
                sender_id=tx.get("sender_id", "UID9622"),
                recipient_id=tx.get("recipient_id", ""),
                status=tx.get("status", "completed"),
                memo=tx.get("memo", ""),
                processing_fee=float(tx.get("fee", 0) or 0),
                dna_fee=0.0,
                total_fee=float(tx.get("fee", 0) or 0),
                created_at=tx.get("created_at", datetime.now().isoformat()),
                dna_signature=tx.get("dna_signature", ""),
                settlement_ref="legacy-migration",
                sovereign_country="CHN" if tx.get("currency") == "CNY" else "UNKNOWN"
            )
            self.save(tx_obj)
            migrated += 1
        return migrated
