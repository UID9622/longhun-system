#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
數字人民幣（CNY）演示適配器
DNA:#龍芯⚡️2026-06-17-XPAY-CNY-ADAPTER-v2.0

聲明：本適配器為演示框架，不連接真實的數字人民幣 SDK 或央行 API。
"""
import uuid
from datetime import datetime

from xpay.src.adapter import CurrencyAdapter, ExecutionResult, SovereignInfo


class CNYAdapter(CurrencyAdapter):
    """
    數字人民幣適配器。
    設計原則：0% 處理費，僅收取 DNA 維護費 0.001 CNY。
    """

    def _sovereign_info(self) -> SovereignInfo:
        return SovereignInfo(
            country_code="CHN",
            currency_code="CNY",
            issuer="中国人民银行",
            p2p_capable=True,
            traceable=True,
            immutable=True,
            audit_score=12,
            status="active"
        )

    def validate(self, amount: float, recipient: str, memo: str = "") -> bool:
        if amount <= 0:
            return False
        if not recipient or not recipient.startswith("UID"):
            return False
        if len(memo) > 200:
            return False
        return True

    def calculate_fee(self, amount: float) -> dict:
        dna_fee = 0.001
        return {
            "processing": 0.0,
            "dna": dna_fee,
            "total": dna_fee
        }

    def execute(self, amount: float, recipient: str, memo: str = "") -> ExecutionResult:
        # 演示：生成虛擬結算引用，不觸發真實資金轉移
        ref = f"PBOC-DEMO-{uuid.uuid4().hex[:12].upper()}"
        return ExecutionResult(
            success=True,
            settlement_ref=ref,
            message="數字人民幣演示結算成功（未發生真實轉帳）",
            details={
                "channel": "e-CNY simulated",
                "settled_at": datetime.now().isoformat(),
                "recipient": recipient,
                "amount": amount
            }
        )

    def verify_settlement(self, settlement_ref: str) -> bool:
        return settlement_ref.startswith("PBOC-DEMO-")

    def rollback(self, settlement_ref: str) -> ExecutionResult:
        return ExecutionResult(
            success=True,
            settlement_ref=settlement_ref,
            message="演示回滾完成",
            details={"rolled_back_at": datetime.now().isoformat()}
        )
