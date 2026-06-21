#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CurrencyAdapter 抽象接口
DNA:#龍芯⚡️2026-06-17-XPAY-ADAPTER-FILE1-v2.0
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class SovereignInfo:
    """貨幣主權信息"""
    country_code: str          # ISO 3166-1 alpha-3，例如 CHN
    currency_code: str         # ISO 4217，例如 CNY
    issuer: str                # 發行機構，例如 "中国人民银行"
    p2p_capable: bool          # 是否支持點對點直達
    traceable: bool            # 是否完全可追蹤
    immutable: bool            # 是否不可篡改
    audit_score: int           # DNA 審計得分 0-12
    status: str                # active / trial / pending / rejected


@dataclass
class ExecutionResult:
    """適配器執行結果"""
    success: bool
    settlement_ref: str
    message: str
    details: Dict[str, Any]


class CurrencyAdapter(ABC):
    """
    主權貨幣適配器接口。
    每個國家的法幣/CBDC 都應該有自己實現，直連該國官方 API。
    """

    def __init__(self):
        self.info = self._sovereign_info()

    @abstractmethod
    def _sovereign_info(self) -> SovereignInfo:
        """返回該幣種主權信息"""
        pass

    @abstractmethod
    def validate(self, amount: float, recipient: str, memo: str = "") -> bool:
        """驗證交易參數合法性"""
        pass

    @abstractmethod
    def calculate_fee(self, amount: float) -> Dict[str, float]:
        """
        計算費用結構。
        返回 dict：{"processing": 0.0, "dna": 0.001, "total": 0.001}
        """
        pass

    @abstractmethod
    def execute(self, amount: float, recipient: str, memo: str = "") -> ExecutionResult:
        """
        執行真實或模擬清結算。
        注意：演示適配器不會觸發真實資金轉移。
        """
        pass

    @abstractmethod
    def verify_settlement(self, settlement_ref: str) -> bool:
        """驗證清結算結果"""
        pass

    @abstractmethod
    def rollback(self, settlement_ref: str) -> ExecutionResult:
        """回滾交易（若支持）"""
        pass
