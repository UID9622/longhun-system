#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
🐉 龍魂交易哈希生成器 · Longhun Transaction Hash Generator

DNA: #龍帳⚡️2026-08-31-LONGHUN-LEDGER-GENESIS-v1.0-UID9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

每笔交易的防篡改哈希指纹生成工具。
Generates SHA256 hash fingerprints for ledger transactions.
"""

import hashlib
import datetime
import json
from typing import Optional


def longhun_tx_hash(
    dna: str,
    dr_account: str,
    cr_account: str,
    amount: str,
    timestamp: Optional[str] = None
) -> str:
    """
    生成龍魂交易哈希指纹（8位大写十六进制）
    
    Args:
        dna:        交易DNA字符串，格式: #龍帳⚡️YYYY-MM-DD-{借方}-{贷方}-{量}-{序号}-UID9622
        dr_account: 借方科目代码（如 "1001"）
        cr_account: 贷方科目代码（如 "3201"）
        amount:     交易量+单位（如 "1条", "100元", "1模块"）
        timestamp:  ISO 8601 时间戳，默认为当前时间
    
    Returns:
        8位大写十六进制哈希字符串（如 "A3F7D291"）
    
    Example:
        >>> h = longhun_tx_hash(
        ...     dna="#龍帳⚡️2026-08-31-1001-3201-1条-001-UID9622",
        ...     dr_account="1001",
        ...     cr_account="3201",
        ...     amount="1条",
        ...     timestamp="2026-08-31T21:56:00+08:00"
        ... )
        >>> print(h)  # e.g. "A3F7D291"
    """
    ts = timestamp or datetime.datetime.now().isoformat()
    raw = f"{dna}|{dr_account}|{cr_account}|{amount}|{ts}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()[:8].upper()


def build_dna(
    date: str,
    dr_account: str,
    cr_account: str,
    amount: str,
    seq: int,
    uid: str = "UID9622"
) -> str:
    """
    构建龍魂交易DNA字符串
    
    Args:
        date:       日期字符串 YYYY-MM-DD
        dr_account: 借方科目代码
        cr_account: 贷方科目代码
        amount:     交易量+单位
        seq:        当日序号（从1开始）
        uid:        主权人UID（默认UID9622）
    
    Returns:
        完整DNA字符串
    
    Example:
        >>> dna = build_dna("2026-08-31", "1001", "3201", "1条", 1)
        >>> print(dna)
        #龍帳⚡️2026-08-31-1001-3201-1条-001-UID9622
    """
    return f"#龍帳⚡️{date}-{dr_account}-{cr_account}-{amount}-{seq:03d}-{uid}"


def create_transaction(
    description: str,
    dr_account: str,
    dr_name: str,
    cr_account: str,
    cr_name: str,
    amount: str,
    tx_type: str,
    witness: str,
    health: str,
    note: str = "",
    date: Optional[str] = None,
    seq: int = 1,
    uid: str = "UID9622"
) -> dict:
    """
    创建完整的龍魂交易记录
    
    Returns:
        完整交易记录字典，包含DNA、哈希等所有字段
    """
    now = datetime.datetime.now()
    date_str = date or now.strftime("%Y-%m-%d")
    timestamp = now.isoformat()
    
    dna = build_dna(date_str, dr_account, cr_account, amount, seq, uid)
    tx_hash = longhun_tx_hash(dna, dr_account, cr_account, amount, timestamp)
    
    return {
        "tx_id": f"TX-{date_str}-{seq:03d}",
        "dna": dna,
        "hash": tx_hash,
        "date": date_str,
        "timestamp": timestamp,
        "description": description,
        "dr_account": dr_account,
        "dr_name": dr_name,
        "cr_account": cr_account,
        "cr_name": cr_name,
        "amount": amount,
        "tx_type": tx_type,
        "witness": witness,
        "balanced": True,
        "health": health,
        "github_sync": "🔄 待同步",
        "note": note,
        "uid": uid
    }


if __name__ == "__main__":
    # 演示：生成一笔焊死铁律的交易记录
    print("🐉 龍魂交易哈希生成器 v1.0")
    print("=" * 50)
    
    tx = create_transaction(
        description="焊死铁律：API自给自足",
        dr_account="1001",
        dr_name="焊点·铁律",
        cr_account="3201",
        cr_name="协议资产净值",
        amount="1条",
        tx_type="T1",
        witness="🧠 ASI-001·至诚智魂",
        health="🟢 资产增加",
        note="知识资产升级"
    )
    
    print(f"凭证编号: {tx['tx_id']}")
    print(f"DNA:      {tx['dna']}")
    print(f"哈希指纹: {tx['hash']}")
    print(f"借：{tx['dr_account']} {tx['dr_name']} +{tx['amount']}")
    print(f"贷：{tx['cr_account']} {tx['cr_name']} +{tx['amount']}")
    print(f"见证：    {tx['witness']}")
    print(f"平衡验证: {'✓ 平衡' if tx['balanced'] else '✗ 不平衡'}")
    print(f"健康度:   {tx['health']}")
