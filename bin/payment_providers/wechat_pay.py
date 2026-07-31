# DNA: #龍芯⚡️丙午·乙未·乙丑·未济-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-WECHAT-PAY-PROVIDER-v1.0

import os
from pathlib import Path
from decimal import Decimal
from typing import Dict, Any


class WechatPayProvider:
    """微信支付 Native 扫码支付 Provider"""

    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = cfg
        self.appid = cfg["appid"]
        self.mch_id = cfg["mch_id"]
        self.api_v3_key = cfg["api_v3_key"]
        self.cert_serial_no = cfg["cert_serial_no"]
        self.notify_url = cfg.get("notify_url", "")
        self._init_client()

    def _init_client(self):
        try:
            from wechatpayv3 import WeChatPay, WeChatPayType
        except ImportError as e:
            raise RuntimeError("未安装 wechatpayv3，请执行: pip install wechatpayv3") from e

        private_key_path = Path(os.path.expanduser(self.cfg["private_key_path"])).expanduser()
        with open(private_key_path, "r", encoding="utf-8") as f:
            private_key = f.read()

        self.client = WeChatPay(
            wechatpay_type=WeChatPayType.NATIVE,
            mchid=self.mch_id,
            private_key=private_key,
            cert_serial_no=self.cert_serial_no,
            apiv3_key=self.api_v3_key,
            appid=self.appid,
            notify_url=self.notify_url,
        )

    def create_order(self, out_trade_no: str, amount: Decimal, description: str) -> Dict[str, Any]:
        """调用微信 Native 支付，返回二维码链接"""
        try:
            code, content = self.client.pay(
                description=description,
                out_trade_no=out_trade_no,
                amount={"total": int(amount * 100)},
                pay_type="native",
            )
            if code == 200 and content.get("code_url"):
                return {
                    "success": True,
                    "provider": "wechat_pay",
                    "out_trade_no": out_trade_no,
                    "qr_code": content["code_url"],
                    "amount": str(amount),
                    "raw": content,
                }
            return {"success": False, "error": f"微信返回异常: {code} {content}"}
        except Exception as e:
            return {"success": False, "error": f"微信下单失败: {str(e)}"}

    def query_order(self, out_trade_no: str) -> Dict[str, Any]:
        try:
            code, content = self.client.query(out_trade_no=out_trade_no)
            return {
                "success": code == 200,
                "provider": "wechat_pay",
                "out_trade_no": out_trade_no,
                "status": content.get("trade_state", "UNKNOWN"),
                "raw": content,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def verify_notify(self, headers: Dict[str, str], body: str) -> Dict[str, Any]:
        """验证微信支付回调签名并解析"""
        try:
            result = self.client.callback(headers, body)
            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
