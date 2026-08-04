#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA 存根生成与验证
DNA:#龍芯⚡️2026-06-17-XPAY-DNA-FILE1-v2.0
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
    生成交易 DNA 签名：所有关键字段的 SHA256 哈希前 16 位。
    这是交易在宇宙中留下的不可删除指纹。
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
    """验证 DNA 签名是否与交易字段匹配"""
    expected = generate_dna_signature(
        tx_id=tx.get("tx_id", ""),
        amount=float(tx.get("amount", 0)),
        currency=tx.get("currency", ""),
        sender=tx.get("sender_id", ""),
        recipient=tx.get("recipient_id", ""),
        timestamp=tx.get("created_at", "")
    )
    return expected == signature
