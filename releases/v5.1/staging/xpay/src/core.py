#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SovereignGateway 主引擎
DNA:#龍芯⚡️2026-06-17-XPAY-CORE-v2.0
"""
import importlib
import pkgutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from xpay.src.adapter import CurrencyAdapter, ExecutionResult, SovereignInfo
from xpay.src.dna import generate_dna_signature, generate_tx_id
from xpay.src.transaction import Transaction, TransactionStore


class SovereignGateway:
    """
    龍魂主權支付網關。
    只負責：選擇幣種適配器 -> 調用官方 API -> 生成 DNA 存根。
    不持有資金，不當中間商。
    """

    DNA_SIGNATURE = "#龍芯⚡️2026-06-17-XPAY-CORE-v2.0"

    def __init__(self, db_path: Optional[Path] = None):
        self.store = TransactionStore(db_path)
        self.adapters: Dict[str, CurrencyAdapter] = {}
        self._register_builtin_adapters()

    def _register_builtin_adapters(self):
        """自動掃描並註冊 xpay.src.adapters 下的所有適配器"""
        from xpay.src import adapters
        for _, name, _ in pkgutil.iter_modules(adapters.__path__):
            try:
                module = importlib.import_module(f"xpay.src.adapters.{name}")
                for attr in dir(module):
                    obj = getattr(module, attr)
                    if isinstance(obj, type) and issubclass(obj, CurrencyAdapter) and obj is not CurrencyAdapter:
                        adapter = obj()
                        self.register_adapter(adapter)
            except Exception as e:
                print(f"⚠️  加載適配器 {name} 失敗: {e}")

    def register_adapter(self, adapter: CurrencyAdapter):
        """手動註冊一個貨幣適配器"""
        code = adapter.info.currency_code.upper()
        self.adapters[code] = adapter

    def supported_currencies(self) -> List[str]:
        """返回已註冊的幣種列表"""
        return sorted(self.adapters.keys())

    def sovereign_info(self, currency: str) -> Optional[SovereignInfo]:
        """查詢某幣種的主權信息"""
        adapter = self.adapters.get(currency.upper())
        return adapter.info if adapter else None

    def pay(self, amount: float, currency: str, recipient: str,
            sender: str = "UID9622", memo: str = "") -> Dict:
        """
        用戶級最簡 API：發起一筆支付。
        所有複雜邏輯封裝在適配器內部。
        """
        currency = currency.upper()
        adapter = self.adapters.get(currency)
        if not adapter:
            return {
                "success": False,
                "error": f"不支持的幣種：{currency}",
                "supported": self.supported_currencies()
            }

        # 參數驗證
        if not adapter.validate(amount, recipient, memo):
            return {
                "success": False,
                "error": "交易參數未通過適配器驗證"
            }

        # 計算費用
        fee_breakdown = adapter.calculate_fee(amount)
        processing_fee = fee_breakdown.get("processing", 0.0)
        dna_fee = fee_breakdown.get("dna", 0.0)
        total_fee = fee_breakdown.get("total", processing_fee + dna_fee)

        # 生成交易 ID 與 DNA
        tx_id = generate_tx_id()
        created_at = datetime.now().isoformat()
        dna_signature = generate_dna_signature(
            tx_id, amount, currency, sender, recipient, created_at
        )

        # 調用國家適配器執行清結算（演示模式）
        result: ExecutionResult = adapter.execute(amount, recipient, memo)

        tx = Transaction(
            tx_id=tx_id,
            amount=amount,
            currency=currency,
            sender_id=sender,
            recipient_id=recipient,
            status="completed" if result.success else "failed",
            memo=memo,
            processing_fee=processing_fee,
            dna_fee=dna_fee,
            total_fee=total_fee,
            created_at=created_at,
            dna_signature=dna_signature,
            settlement_ref=result.settlement_ref,
            sovereign_country=adapter.info.country_code
        )
        self.store.save(tx)

        return {
            "success": result.success,
            "tx_id": tx_id,
            "currency": currency,
            "amount": amount,
            "fees": fee_breakdown,
            "recipient": recipient,
            "status": tx.status,
            "dna_signature": dna_signature,
            "settlement_ref": result.settlement_ref,
            "message": result.message,
            "details": result.details
        }

    def query(self, tx_id: str) -> Optional[Dict]:
        """查詢交易詳情"""
        tx = self.store.get(tx_id)
        if not tx:
            return None
        return tx.__dict__

    def stats(self) -> Dict:
        """統計所有交易"""
        return self.store.stats()

    def migrate_legacy(self, legacy_json: Path = Path.home() / ".龍魂" / "xpay" / "transactions.json"):
        """遷移舊版 XPay 交易數據"""
        count = self.store.migrate_json(legacy_json)
        return {"migrated": count}
