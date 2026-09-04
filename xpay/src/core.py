#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
SovereignGateway 主引擎
DNA:#龍芯⚡️丙午·甲午·壬戌·丙午·䷕贲-XPAY-CORE-FILE1-v2.0
"""
import importlib
import pkgutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from xpay.src.adapter import CurrencyAdapter, ExecutionResult, SovereignInfo
from xpay.src.dna import generate_dna_signature, generate_tx_id
from xpay.src.transaction import Transaction, TransactionStore


class SovereignGateway:
    """
    龍魂主权支付网关。
    只负责：选择币种适配器 -> 调用官方 API -> 生成 DNA 存根。
    不持有资金，不当中间商。
    """

    DNA_SIGNATURE = "#龍芯⚡️丙午·甲午·壬戌·丙午·䷕贲-XPAY-CORE-v2.0"

    def __init__(self, db_path: Optional[Path] = None):
        self.store = TransactionStore(db_path)
        self.adapters: Dict[str, CurrencyAdapter] = {}
        self._register_builtin_adapters()

    def _register_builtin_adapters(self):
        """自动扫描并注册 xpay.src.adapters 下的所有适配器"""
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
                print(f"⚠️  加载适配器 {name} 失败: {e}")

    def register_adapter(self, adapter: CurrencyAdapter):
        """手动注册一个货币适配器"""
        code = adapter.info.currency_code.upper()
        self.adapters[code] = adapter

    def supported_currencies(self) -> List[str]:
        """返回已注册的币种列表"""
        return sorted(self.adapters.keys())

    def sovereign_info(self, currency: str) -> Optional[SovereignInfo]:
        """查询某币种的主权信息"""
        adapter = self.adapters.get(currency.upper())
        return adapter.info if adapter else None

    def pay(self, amount: float, currency: str, recipient: str,
            sender: str = "UID9622", memo: str = "") -> Dict[str, Any]:
        """
        用户级最简 API：发起一笔支付。
        所有复杂逻辑封装在适配器内部。
        """
        currency = currency.upper()
        adapter = self.adapters.get(currency)
        if not adapter:
            return {
                "success": False,
                "error": f"不支持的币种：{currency}",
                "supported": self.supported_currencies()
            }

        # 参数验证
        if not adapter.validate(amount, recipient, memo):
            return {
                "success": False,
                "error": "交易参数未通过适配器验证"
            }

        # 计算费用
        fee_breakdown = adapter.calculate_fee(amount)
        processing_fee = fee_breakdown.get("processing", 0.0)
        dna_fee = fee_breakdown.get("dna", 0.0)
        total_fee = fee_breakdown.get("total", processing_fee + dna_fee)

        # 生成交易 ID 与 DNA
        tx_id = generate_tx_id()
        created_at = datetime.now().isoformat()
        dna_signature = generate_dna_signature(
            tx_id, amount, currency, sender, recipient, created_at
        )

        # 调用国家适配器执行清结算（演示模式）
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
        """查询交易详情"""
        tx = self.store.get(tx_id)
        if not tx:
            return None
        return tx.__dict__

    def stats(self) -> Dict[str, Any]:
        """统计所有交易"""
        return self.store.stats()

    def migrate_legacy(self, legacy_json: Path = Path.home() / ".龍魂" / "xpay" / "transactions.json"):
        """迁移旧版 XPay 交易数据"""
        count = self.store.migrate_json(legacy_json)
        return {"migrated": count}
