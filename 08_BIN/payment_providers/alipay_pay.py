#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷿未济-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-ALIPAY-PROVIDER-v1.0

import os
from pathlib import Path
from decimal import Decimal
from typing import Dict, Any


class AlipayProvider:
    """支付宝当面付（扫码支付）Provider"""

    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = cfg
        self.app_id = cfg["app_id"]
        self.notify_url = cfg.get("notify_url", "")
        self._init_client()

    def _init_client(self):
        try:
            from alipay import AliPay
        except ImportError as e:
            raise RuntimeError("未安装 python-alipay-sdk，请执行: pip install python-alipay-sdk") from e

        app_private_key_path = Path(os.path.expanduser(self.cfg["app_private_key_path"])).expanduser()
        alipay_public_key_path = Path(os.path.expanduser(self.cfg["alipay_public_key_path"])).expanduser()

        with open(app_private_key_path, "r", encoding="utf-8") as f:
            app_private_key = f.read()
        with open(alipay_public_key_path, "r", encoding="utf-8") as f:
            alipay_public_key = f.read()

        self.client = AliPay(
            appid=self.app_id,
            app_notify_url=self.notify_url,
            app_private_key_string=app_private_key,
            alipay_public_key_string=alipay_public_key,
            sign_type="RSA2",
            debug=bool(self.cfg.get("sandbox", True)),
        )

    def create_order(self, out_trade_no: str, amount: Decimal, description: str) -> Dict[str, Any]:
        """调用支付宝预创建订单，返回二维码链接"""
        try:
            result = self.client.api_alipay_trade_precreate(
                subject=description,
                out_trade_no=out_trade_no,
                total_amount=str(amount),
            )
            if result.get("code") == "10000" and result.get("qr_code"):
                return {
                    "success": True,
                    "provider": "alipay",
                    "out_trade_no": out_trade_no,
                    "qr_code": result["qr_code"],
                    "amount": str(amount),
                    "raw": result,
                }
            return {"success": False, "error": f"支付宝返回异常: {result}"}
        except Exception as e:
            return {"success": False, "error": f"支付宝下单失败: {str(e)}"}

    def query_order(self, out_trade_no: str) -> Dict[str, Any]:
        try:
            result = self.client.api_alipay_trade_query(out_trade_no=out_trade_no)
            return {
                "success": result.get("code") == "10000",
                "provider": "alipay",
                "out_trade_no": out_trade_no,
                "status": result.get("trade_status", "UNKNOWN"),
                "raw": result,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def verify_notify(self, data: Dict[str, Any], signature: str) -> Dict[str, Any]:
        """验证支付宝回调签名"""
        try:
            ok = self.client.verify(data, signature)
            return {"success": ok, "data": data if ok else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
