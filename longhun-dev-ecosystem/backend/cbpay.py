# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · 数字人民币（CBPay）通道适配层 v1.0
DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CBPAY-ADAPTER-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

设计（正规支付网关契约·与 gateway.PaymentGateway 对齐）:
  1. 下单   create_cbpay_order()  → 数币收银台/付款码（返回 pay_url + 二维码）
  2. 回调   cbpay_verify_notify() 验签 → cbpay_parse_notify() 标准化
           （验签通过后交 monthly_fee.handle_payment_notify 幂等入账）
  3. 查单   cbpay_query_order()    对账兜底
  4. 沙箱   cbpay_sandbox_*()      无商户号时的本地闭环（可 import 可 CLI 直跑自测）

【接入真实商户】
  ① 向数币运营机构（银行）开通数币商户，获得: 商户号 + 应用ID + 密钥/证书 + 接口基址
  ② 配置（环境变量注入 config，严禁硬编码）:
       CBPay_MERCHANT_NO / CBPay_APP_ID / CBPay_API_BASE
       CBPay_SIGN_MODE = hmac(对称·默认) | rsa(非对称·需 cryptography) | sm2(预留)
       CBPay_API_KEY（hmac 模式=对称密钥；rsa 模式=商户私钥串）
       CBPay_PLATFORM_PUBKEY（验签平台公钥·rsa 模式必需）
  ③ 把 config.PAYMENT_GATEWAY 切为 "cbpay" 即全线接通（接口签名不变）

【签名规范】
  hmac 模式（默认·沙箱/演示）:
    payload = "&".join(f"{k}={v}" for k,v in sorted(params) if v is not None)
    sign    = hex(hmac_sha256(secret, payload))
  rsa 模式（真实商户·RSA-SHA256）:
    同一 payload，用商户私钥 SHA256withRSA 签名；
    验签用平台公钥 SHA256withRSA。
  sm2 模式: 预留（数研所 SM2 规范落地位）。

金额一律以「分」为最小单位与机构交互，对外（业务层）以「元」计。
"""

import hashlib
import hmac
import json
import time
import random
from datetime import datetime

# ---- 配置（与 config.py 同名变量对齐·直接跑本文件时用默认值） ----
try:
    from .config import (
        CBPay_MERCHANT_NO,
        CBPay_APP_ID,
        CBPay_API_BASE,
        CBPay_SIGN_MODE,
        CBPay_API_KEY,
        CBPay_PLATFORM_PUBKEY,
        PAYMENT_MIN_AMOUNT,
    )
    _CONFIGURED = True
except (ImportError, ValueError):
    CBPay_MERCHANT_NO = ""
    CBPay_APP_ID = ""
    CBPay_API_BASE = ""
    CBPay_SIGN_MODE = "hmac"
    CBPay_API_KEY = "cbpay-sandbox-key-9622"
    CBPay_PLATFORM_PUBKEY = ""
    PAYMENT_MIN_AMOUNT = 1.0
    _CONFIGURED = False


# ============================================================
# 基础工具
# ============================================================

def yuan_to_fen(amount: float) -> int:
    """元 → 分（数币接口最小单位）"""
    return int(round(amount * 100))


def fen_to_yuan(fen) -> float:
    """分 → 元"""
    try:
        return round(float(fen) / 100.0, 2)
    except (TypeError, ValueError):
        return 0.0


def _payload(params: dict) -> str:
    """规范化待签名串: 参数按 key 排序拼接（与沙箱网关一致）"""
    return "&".join(f"{k}={params[k]}" for k in sorted(params) if params[k] is not None)


def _hmac_sign(payload: str, secret: str) -> str:
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


def _rsa_sign(payload: str, private_key_pem: str) -> str:
    """SHA256withRSA 签名（lazy 依赖 cryptography·真实商户用）"""
    try:
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import padding
    except ImportError:
        raise RuntimeError("rsa 验签需要 cryptography: pip install cryptography")
    key = serialization.load_pem_private_key(private_key_pem.encode(), password=None)
    sig = key.sign(payload.encode(), padding.PKCS1v15(), hashes.SHA256())
    return sig.hex()


def _rsa_verify(payload: str, signature: str, public_key_pem: str) -> bool:
    """SHA256withRSA 验签（平台公钥）"""
    try:
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import padding
    except ImportError:
        raise RuntimeError("rsa 验签需要 cryptography: pip install cryptography")
    try:
        key = serialization.load_pem_public_key(public_key_pem.encode())
        key.verify(
            bytes.fromhex(signature), payload.encode(), padding.PKCS1v15(), hashes.SHA256()
        )
        return True
    except Exception:
        return False


def _render_qr(pay_url: str, amount: float, order_id: str) -> str:
    """内联 SVG 二维码占位（真实通道建议前端用 qrcode 库渲染 pay_url）"""
    return (
        'data:image/svg+xml;utf8,'
        '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="230">'
        '<rect width="200" height="230" fill="#0a0a12"/>'
        '<rect x="20" y="20" width="60" height="60" fill="#c0392b"/>'
        '<rect x="120" y="20" width="60" height="60" fill="#c0392b"/>'
        '<rect x="20" y="120" width="60" height="60" fill="#c0392b"/>'
        '<rect x="85" y="85" width="30" height="30" fill="#c0392b"/>'
        '<circle cx="120" cy="150" r="12" fill="#e67e22"/>'
        f'<text x="100" y="205" font-size="11" fill="#e8e6e3" text-anchor="middle">数字人民币 {amount:.2f} 元</text>'
        f'<text x="100" y="222" font-size="9" fill="#888" text-anchor="middle">{order_id[-10:]}</text>'
        '</svg>'
    )


# ============================================================
# 签名（按 CBPay_SIGN_MODE 分发）
# ============================================================

def sign_payload(params: dict) -> str:
    """商户侧签名（下单请求/模拟回调）"""
    payload = _payload(params)
    mode = CBPay_SIGN_MODE.lower()
    if mode == "rsa":
        if not CBPay_API_KEY:
            raise RuntimeError("CBPay_SIGN_MODE=rsa 但未配置 CBPay_API_KEY（商户私钥）")
        return _rsa_sign(payload, CBPay_API_KEY)
    if mode == "sm2":
        raise RuntimeError("SM2 签名模式为预留位，暂未启用（请先用 hmac 或 rsa）")
    return _hmac_sign(payload, CBPay_API_KEY or "cbpay-sandbox-key-9622")


def verify_notify_signature(params: dict, signature: str) -> bool:
    """回调验签（按模式分发）"""
    if not signature:
        return False
    payload = _payload(params)
    mode = CBPay_SIGN_MODE.lower()
    if mode == "rsa":
        if not CBPay_PLATFORM_PUBKEY:
            return False
        return _rsa_verify(payload, signature, CBPay_PLATFORM_PUBKEY)
    if mode == "sm2":
        return False  # 预留
    return _hmac_sign(payload, CBPay_API_KEY or "cbpay-sandbox-key-9622") == signature


# ============================================================
# 下单（真实通道: POST 数币下单接口）
# ============================================================

def create_cbpay_order(order_id: str, amount: float, subject: str, developer_dna: str = "") -> dict:
    """
    数字人民币下单:
      - 已配置商户号 → 调运营机构下单接口（返回收银台 pay_url）
      - 未配置商户号 → 沙箱收银台（本地闭环·可先行联调）
    返回: {success, order_id, amount, status, pay_url, qr_code, expires_at}
    """
    if amount < PAYMENT_MIN_AMOUNT:
        return {"success": False, "error": f"最低支付金额 {PAYMENT_MIN_AMOUNT} 元"}

    if not CBPay_MERCHANT_NO:
        # 沙箱收银台: 无商户号时先跑通全链路
        pay_url = f"https://cbpay-sandbox.longhun.local/pay/{order_id}?amount={yuan_to_fen(amount)}"
        return {
            "success": True,
            "order_id": order_id,
            "amount": amount,
            "subject": subject,
            "status": "pending",
            "channel": "cbpay",
            "mode": "sandbox",
            "pay_url": pay_url,
            "qr_code": _render_qr(pay_url, amount, order_id),
            "expires_at": int(time.time()) + 900,  # 15 分钟有效
        }

    # 真实通道: 调运营机构下单接口（机构差异收敛到请求组装·字段名按实际接入微调）
    req = {
        "merchantNo": CBPay_MERCHANT_NO,
        "appId": CBPay_APP_ID,
        "orderNo": order_id,
        "amount": yuan_to_fen(amount),          # 分
        "subject": subject,
        "developerDna": developer_dna or "",
        "notifyUrl": "",                        # 回调地址: 接入时注入
        "timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
        "nonce": random.randint(100000, 999999),
    }
    req["sign"] = sign_payload(req)
    body = json.dumps(req, ensure_ascii=False)

    # urllib 标准库直连（零三方依赖）
    import urllib.request
    if not CBPay_API_BASE:
        return {"success": False, "error": "数字人民币未配置接口基址（CBPay_API_BASE）"}
    try:
        r = urllib.request.Request(
            CBPay_API_BASE + "/open/v1/order/create",
            data=body.encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(r, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:  # 机构接口不可达时给出明确错误
        return {"success": False, "error": f"数币下单失败: {e}"}

    if str(data.get("code", "")).startswith(("0", "00", "SUCCESS")):
        pay_url = data.get("payUrl") or data.get("cashierUrl") or data.get("qrCodeUrl") or ""
        return {
            "success": True,
            "order_id": order_id,
            "amount": amount,
            "subject": subject,
            "status": "pending",
            "channel": "cbpay",
            "mode": "live",
            "pay_url": pay_url,
            "qr_code": _render_qr(pay_url, amount, order_id) if pay_url else "",
            "expires_at": int(time.time()) + 900,
        }
    return {"success": False, "error": f"数币下单被拒: {data.get('msg') or data.get('message') or data}"}


# ============================================================
# 回调验签 & 标准化解析
# ============================================================

def cbpay_verify_notify(params: dict, signature: str) -> bool:
    """回调验签（对外接口·供 gateway 使用）"""
    return verify_notify_signature(params, signature)


def cbpay_parse_notify(params: dict) -> dict:
    """
    标准化回调（对外接口）:
    返回 {order_id, transaction_id, amount(元), status, paid_at}
    字段映射按运营机构常规命名收敛，接入实际机构时在映射表微调。
    """
    order_id = params.get("order_id") or params.get("orderNo") or params.get("outTradeNo") or ""
    tx_id = params.get("transaction_id") or params.get("transId") or params.get("payNo") or ""
    amount_fen = params.get("amount") or params.get("payAmount") or params.get("totalFee") or 0
    status = params.get("status") or params.get("payStatus") or ""
    # 状态归一: 数币机构常见成功标记
    paid = (
        str(status).lower() in ("paid", "success", "succeeded", "00", "0")
        or params.get("success") is True
    )
    return {
        "order_id": str(order_id),
        "transaction_id": str(tx_id),
        "amount": fen_to_yuan(amount_fen) if not params.get("amountIsYuan") else round(float(amount_fen), 2),
        "status": "paid" if paid else "pending",
        "paid_at": datetime.now().isoformat(),
    }


def cbpay_query_order(order_id: str) -> dict:
    """查单（对账兜底）: 沙箱返回 unknown；真实通道调查单接口"""
    if not CBPay_MERCHANT_NO:
        return {"order_id": order_id, "status": "unknown", "channel": "cbpay", "mode": "sandbox"}
    if not CBPay_API_BASE:
        return {"order_id": order_id, "status": "unknown", "channel": "cbpay", "error": "CBPay_API_BASE 未配置"}
    req = {"merchantNo": CBPay_MERCHANT_NO, "appId": CBPay_APP_ID, "orderNo": order_id}
    req["sign"] = sign_payload(req)
    import urllib.request
    try:
        r = urllib.request.Request(
            CBPay_API_BASE + "/open/v1/order/query",
            data=json.dumps(req, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(r, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return {
            "order_id": order_id,
            "status": "paid" if str(data.get("status", "")).lower() in ("paid", "success", "0", "00") else "pending",
            "channel": "cbpay",
            "mode": "live",
            "raw": data,
        }
    except Exception as e:
        return {"order_id": order_id, "status": "unknown", "channel": "cbpay", "error": str(e)}


# ============================================================
# 沙箱模拟（无商户号时完整闭环·联调/演示用）
# ============================================================

def cbpay_sandbox_sign(params: dict) -> str:
    """生成沙箱模拟回调签名（测试用·与验签同构）"""
    return sign_payload(params)


def cbpay_sandbox_notify_params(order_id: str, amount_yuan: float, transaction_id: str = "") -> dict:
    """构造沙箱模拟回调参数（模拟用户已用数币 App 扫码支付成功）"""
    return {
        "order_id": order_id,
        "transaction_id": transaction_id or f"CBPay-{int(time.time())}",
        "amount": yuan_to_fen(amount_yuan),  # 数币回调单位: 分
        "status": "paid",
        "channel": "cbpay",
        "payTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


# ============================================================
# 自测（最小闭环: 直接 python3 backend/cbpay.py）
# ============================================================

def _self_test() -> dict:
    """沙箱全链路自测: 下单 → 模拟回调 → 验签 → 标准化解析 → 金额核对"""
    results = []
    ok = True

    # ① 下单
    order = create_cbpay_order("LH20260901120000123456", 1.0, "2026-09 月费")
    ok = ok and order.get("success") is True and order.get("pay_url")
    results.append(("下单", "✅" if ok else "❌", order.get("mode", "")))

    # ② 模拟回调 + 验签
    params = cbpay_sandbox_notify_params(order["order_id"], 1.0)
    sig = cbpay_sandbox_sign(params)
    verified = cbpay_verify_notify(params, sig)
    ok = ok and verified
    results.append(("验签", "✅" if verified else "❌", f"hmac::{sig[:16]}…"))

    # ③ 标准化解析
    parsed = cbpay_parse_notify(params)
    ok = ok and parsed["status"] == "paid" and parsed["amount"] == 1.0
    results.append(("解析", "✅" if parsed["status"] == "paid" else "❌", f"amount={parsed['amount']}元 status={parsed['status']}"))

    # ④ 篡改防护: 改金额必须验签失败
    tampered = dict(params, amount=99999)
    ok = ok and not cbpay_verify_notify(tampered, sig)
    results.append(("防篡改", "✅" if not cbpay_verify_notify(tampered, sig) else "❌", "改金额→拒签"))

    # ⑤ 查单（沙箱）
    query = cbpay_query_order(order["order_id"])
    results.append(("查单", "✅", query.get("status", "")))

    print(f"{'# 数字人民币(CBPay)通道自测 v1.0':=^60}")
    print(f"归属名: 诸葛鑫 | UID9622 · 龍芯北辰 · DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CBPAY-ADAPTER-UID9622")
    print(f"配置: 商户号={'已配置(live)' if CBPay_MERCHANT_NO else '未配置(沙箱)'} · 签名模式={CBPay_SIGN_MODE}")
    print("-" * 60)
    for name, mark, detail in results:
        print(f"  {mark} {name:<6} {detail}")
    print("=" * 60)
    print("结论:", "🟢 全链路通过·等待商户号即可切真实通道" if ok else "🔴 存在失败项")
    return {"success": ok, "results": results}


if __name__ == "__main__":
    _self_test()
