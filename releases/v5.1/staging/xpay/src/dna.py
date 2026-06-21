#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA 存根生成與驗證
DNA:#龍芯⚡️2026-06-17-XPAY-DNA-v2.0
"""
import hashlib
import uuid
from datetime import datetime
from typing import Dict


def generate_tx_id() -> str:
    """生成唯一交易 ID"""
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    suffix = uuid.uuid4().hex[:8].upper()
    return f"TXN-{now}-{suffix}"


def generate_dna_signature(tx_id: str, amount: float, currency: str,
                           sender: str, recipient: str, timestamp: str) -> str:
    """
    生成交易 DNA 簽名：所有關鍵字段的 SHA256 哈希前 16 位。
    這是交易在宇宙中留下的不可刪除指紋。
    """
    payload = "|".join([
        tx_id,
        f"{amount:.6f}",
        currency,
        sender,
        recipient,
        timestamp
    ])
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16].upper()
    return f"#龍芯⚡️{timestamp.replace('-', '').replace(':', '').replace('.', '')[:14]}-XPAY-{currency}-{digest}"


def verify_dna_signature(tx: Dict, signature: str) -> bool:
    """驗證 DNA 簽名是否與交易字段匹配"""
    expected = generate_dna_signature(
        tx_id=tx.get("tx_id", ""),
        amount=float(tx.get("amount", 0)),
        currency=tx.get("currency", ""),
        sender=tx.get("sender_id", ""),
        recipient=tx.get("recipient_id", ""),
        timestamp=tx.get("created_at", "")
    )
    return expected == signature
