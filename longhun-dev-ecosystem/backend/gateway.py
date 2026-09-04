# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · 正规支付网关层
DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-DEV-GATEWAY-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

设计规范（按正规支付网关）:
  1. 预支付: create_prepay() 生成订单 → 返回支付参数（二维码/收银台链接）
  2. 回调: 网关异步 notify → verify_notify() 验签 → parse_notify() 标准化 → 幂等入账
  3. 查单: query_order() 对账兜底（定时对账任务可复用）
  4. 通道: sandbox(默认·验签闭环) / wechat(微信Native) / alipay(支付宝当面付) / cbpay(数字人民币)

换真实网关: 仅需填充 config 中商户参数并把 PAYMENT_GATEWAY 切换为对应通道。
接口签名、验签、幂等、金额核对逻辑保持不变。
"""

import hashlib
import hmac
import json
import time
import random
import uuid
from datetime import datetime

from .config import (
    PAYMENT_MIN_AMOUNT,
    PAYMENT_GATEWAY,
    SANDBOX_SECRET,
    WECHAT_MCH_ID,
    WECHAT_APP_ID,
    WECHAT_API_KEY,
    ALIPAY_APP_ID,
    ALIPAY_PRIVATE_KEY,
    CBPay_MERCHANT_NO,
)


def _gen_order_id(prefix: str = "LH") -> str:
    """生成商户订单号：{前缀}{yyyyMMddHHmmss}{随机6位}"""
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{prefix}{ts}{random.randint(100000, 999999)}"


def _hmac_sign(payload: str, secret: str) -> str:
    """HMAC-SHA256 签名（正规网关统一验签算法）"""
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


def _sandbox_qr(order_id: str, amount: float, subject: str) -> str:
    """沙箱二维码（内联 SVG，避免外链死链）"""
    return (
        'data:image/svg+xml;utf8,'
        '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="230">'
        f'<rect width="200" height="230" fill="#0a0a12"/>'
        f'<rect x="20" y="20" width="60" height="60" fill="#d4af37"/>'
        f'<rect x="120" y="20" width="60" height="60" fill="#d4af37"/>'
        f'<rect x="20" y="120" width="60" height="60" fill="#d4af37"/>'
        f'<rect x="85" y="85" width="30" height="30" fill="#d4af37"/>'
        f'<circle cx="120" cy="150" r="12" fill="#4ade80"/>'
        f'<text x="100" y="205" font-size="11" fill="#e8e6e3" text-anchor="middle">沙箱支付 {amount:.2f} 元</text>'
        f'<text x="100" y="222" font-size="9" fill="#888" text-anchor="middle">{order_id[-10:]}</text>'
        '</svg>'
    )


class PaymentGateway:
    """支付网关抽象基类（正规接口契约）"""

    channel = "base"

    def create_prepay(self, order_id: str, amount: float, subject: str, developer_dna: str = "") -> dict:
        """预支付：返回 {order_id, amount, status, qr_code / pay_url, ...}"""
        raise NotImplementedError

    def verify_notify(self, params: dict, signature: str) -> bool:
        """回调验签：params 为网关回调参数（含金额/订单号）"""
        raise NotImplementedError

    def parse_notify(self, params: dict) -> dict:
        """标准化回调：返回 {order_id, transaction_id, amount, status, paid_at}"""
        raise NotImplementedError

    def query_order(self, order_id: str) -> dict:
        """订单查询（对账兜底）"""
        raise NotImplementedError


class SandboxGateway(PaymentGateway):
    """沙箱网关（默认）：验签闭环·模拟支付·无需真实商户号"""

    channel = "sandbox"

    def create_prepay(self, order_id: str, amount: float, subject: str, developer_dna: str = "") -> dict:
        if amount < PAYMENT_MIN_AMOUNT:
            return {"success": False, "error": f"最低支付金额 {PAYMENT_MIN_AMOUNT} 元"}
        return {
            "success": True,
            "order_id": order_id,
            "amount": amount,
            "subject": subject,
            "status": "pending",
            "channel": self.channel,
            "qr_code": _sandbox_qr(order_id, amount, subject),
            "expires_at": int(time.time()) + 900,  # 15分钟有效
        }

    def verify_notify(self, params: dict, signature: str) -> bool:
        # 沙箱签名规则: 按参数 key 排序拼接 + HMAC-SHA256
        payload = "&".join(f"{k}={params[k]}" for k in sorted(params) if params[k] is not None)
        return _hmac_sign(payload, SANDBOX_SECRET) == signature

    def parse_notify(self, params: dict) -> dict:
        return {
            "order_id": params.get("order_id", ""),
            "transaction_id": params.get("transaction_id", ""),
            "amount": float(params.get("amount", 0)),
            "status": "paid" if params.get("status") == "paid" else "pending",
            "paid_at": datetime.now().isoformat(),
        }

    def query_order(self, order_id: str) -> dict:
        return {"order_id": order_id, "status": "unknown", "channel": self.channel}


class WechatGateway(PaymentGateway):
    """微信支付 Native 通道（注册位·接入时填 config 商户参数）"""

    channel = "wechat"

    def create_prepay(self, order_id: str, amount: float, subject: str, developer_dna: str = "") -> dict:
        if not WECHAT_MCH_ID or not WECHAT_API_KEY:
            return {"success": False, "error": "微信支付未配置商户参数（WECHAT_MCH_ID / WECHAT_API_KEY）"}
        # 接入位: 调用微信 Native 下单 API → 返回 code_url 生成二维码
        # 参考: POST https://api.mch.weixin.qq.com/v3/pay/transactions/native
        raise NotImplementedError("微信Native接入位：按微信支付APIv3文档实现 create_prepay")

    def verify_notify(self, params: dict, signature: str) -> bool:
        # 接入位: 微信回调使用平台证书/APIv3密钥验签
        raise NotImplementedError("微信回调验签接入位")

    def parse_notify(self, params: dict) -> dict:
        raise NotImplementedError("微信回调解析接入位")

    def query_order(self, order_id: str) -> dict:
        raise NotImplementedError("微信查单接入位")


class AlipayGateway(PaymentGateway):
    """支付宝当面付通道（注册位·接入时填 config 商户参数）"""

    channel = "alipay"

    def create_prepay(self, order_id: str, amount: float, subject: str, developer_dna: str = "") -> dict:
        if not ALIPAY_APP_ID or not ALIPAY_PRIVATE_KEY:
            return {"success": False, "error": "支付宝未配置商户参数（ALIPAY_APP_ID / ALIPAY_PRIVATE_KEY）"}
        # 接入位: 调用 alipay.trade.precreate → 返回 qr_code
        raise NotImplementedError("支付宝当面付接入位：按支付宝开放平台文档实现 create_prepay")

    def verify_notify(self, params: dict, signature: str) -> bool:
        # 接入位: 支付宝 RSA2 签名验签
        raise NotImplementedError("支付宝验签接入位")

    def parse_notify(self, params: dict) -> dict:
        raise NotImplementedError("支付宝回调解析接入位")

    def query_order(self, order_id: str) -> dict:
        raise NotImplementedError("支付宝查单接入位")


class CBPayGateway(PaymentGateway):
    """数字人民币通道（适配层 cbpay.py·接口契约对齐）"""

    channel = "cbpay"

    def create_prepay(self, order_id: str, amount: float, subject: str, developer_dna: str = "") -> dict:
        from .cbpay import create_cbpay_order
        return create_cbpay_order(order_id, amount, subject, developer_dna)

    def verify_notify(self, params: dict, signature: str) -> bool:
        from .cbpay import cbpay_verify_notify
        return cbpay_verify_notify(params, signature)

    def parse_notify(self, params: dict) -> dict:
        from .cbpay import cbpay_parse_notify
        return cbpay_parse_notify(params)

    def query_order(self, order_id: str) -> dict:
        from .cbpay import cbpay_query_order
        return cbpay_query_order(order_id)


_GATEWAYS = {
    "sandbox": SandboxGateway,
    "wechat": WechatGateway,
    "alipay": AlipayGateway,
    "cbpay": CBPayGateway,
}


def get_gateway(channel: str = "") -> PaymentGateway:
    """获取支付网关实例（默认取 config 当前通道）"""
    ch = channel or PAYMENT_GATEWAY
    cls = _GATEWAYS.get(ch, SandboxGateway)
    return cls()


def sign_sandbox(params: dict) -> str:
    """生成沙箱签名（测试/模拟回调用）"""
    payload = "&".join(f"{k}={params[k]}" for k in sorted(params) if params[k] is not None)
    return _hmac_sign(payload, SANDBOX_SECRET)


def available_channels() -> list:
    """返回已可用通道（真实通道未配置商户参数时不列出）"""
    ready = ["sandbox"]
    if WECHAT_MCH_ID and WECHAT_API_KEY:
        ready.append("wechat")
    if ALIPAY_APP_ID and ALIPAY_PRIVATE_KEY:
        ready.append("alipay")
    if CBPay_MERCHANT_NO:
        ready.append("cbpay")
    return ready
