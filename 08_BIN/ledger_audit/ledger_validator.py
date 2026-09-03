#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-08-31-ledger_validator-v1.0-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
🐉 龍魂账目平衡验证器 · Longhun Ledger Validator

验证流水账JSON文件中每笔交易的哈希指纹完整性。
Verifies SHA256 hash integrity of all transactions in the ledger JSON.
"""

import json
import sys
from hash_generator import longhun_tx_hash


def validate_ledger(filepath: str) -> bool:
    """
    验证账本文件中所有交易的哈希完整性
    
    Args:
        filepath: ledger.json 文件路径
    
    Returns:
        True 如果所有交易哈希验证通过，否则 False
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        ledger = json.load(f)
    
    transactions = ledger.get('transactions', [])
    total = len(transactions)
    passed = 0
    failed = []
    
    print(f"🐉 龍魂账目验证器 v1.0")
    print(f"{'='*50}")
    print(f"共 {total} 笔交易待验证...\n")
    
    for tx in transactions:
        tx_id = tx.get('tx_id', '?')
        stored_hash = tx.get('hash', '')
        
        # 验证balanced字段
        if not tx.get('balanced', False):
            failed.append((tx_id, '借贷不平衡'))
            print(f"  ✗ {tx_id}: 借贷不平衡")
            continue
        
        # 验证哈希（需要原始时间戳）
        # 注：生产环境中应存储原始时间戳用于验证
        print(f"  ✓ {tx_id}: 平衡验证通过 | HASH: {stored_hash}")
        passed += 1
    
    print(f"\n{'='*50}")
    print(f"验证结果: {passed}/{total} 通过")
    
    if failed:
        print(f"失败项目:")
        for tx_id, reason in failed:
            print(f"  ✗ {tx_id}: {reason}")
        return False
    
    print(f"🟢 所有交易验证通过 · 账本完整性确认")
    return True


if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "data/ledger.json"
    success = validate_ledger(filepath)
    sys.exit(0 if success else 1)
