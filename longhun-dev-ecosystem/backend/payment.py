# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · 支付接口（正规网关链路）
DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-DEV-PAY-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
说明: 注册激活支付 = 首月费（月度主权确认金公约 v1.0）。
      全部走 gateway.py 正规链路: 预支付订单持久化 → 回调验签 → 幂等入账。
      换真实网关: config.PAYMENT_GATEWAY 切换通道即可，接口签名不变。
"""

from datetime import datetime

from .models import Developer, SessionLocal, Contribution, PaymentOrder
from .monthly_fee import create_monthly_bill, confirm_monthly_payment, get_current_month
from .config import PAYMENT_MIN_AMOUNT


def create_payment_order(developer_dna: str, amount: float = 1.0, channel: str = ""):
    """创建支付订单（注册激活 = 当月月费）: 返回订单号 + 支付参数（二维码/收银台）"""
    db = SessionLocal()
    try:
        if amount < PAYMENT_MIN_AMOUNT:
            return {"success": False, "error": f"最低支付金额 {PAYMENT_MIN_AMOUNT} 元"}
        dev = db.query(Developer).filter(Developer.dna == developer_dna).first()
        if not dev:
            return {"success": False, "error": "开发者不存在"}
        if dev.status == "active" and dev.paid_at is not None:
            return {"success": False, "error": "已激活，无需重复支付"}

        bill = create_monthly_bill(developer_dna, db, amount=amount, channel=channel)
        if "error" in bill:
            return {"success": False, "error": bill["error"]}
        if bill.get("status") == "paid":
            return {"success": False, "error": "本月已缴"}

        return {
            "success": True,
            "order_id": bill["order_id"],
            "amount": bill["amount"],
            "status": "pending",
            "qr_code": bill.get("qr_code"),
            "pay_url": bill.get("pay_url"),
            "expires_at": bill.get("expires_at"),
            "channel": bill.get("channel", "sandbox"),
        }
    finally:
        db.close()


def confirm_payment(developer_dna: str, order_id: str, channel: str = "sandbox"):
    """
    确认支付（沙箱模式走本地回调闭环；真实通道由网关异步回调 /api/pay/notify）
    首次支付 = 注册激活 + 首月费入账
    """
    db = SessionLocal()
    try:
        dev = db.query(Developer).filter(Developer.dna == developer_dna).first()
        if not dev:
            return {"success": False, "error": "开发者不存在"}

        result = confirm_monthly_payment(developer_dna, order_id, db, channel=channel)
        if not result["success"]:
            return result

        # 首次激活补全
        if dev.status != "active" or dev.paid_at is None:
            dev.status = "active"
            dev.paid_at = datetime.now()
            order = db.query(PaymentOrder).filter(PaymentOrder.order_id == order_id).first()
            dev.payment_amount = order.amount if order else 1.0
            # 计费起始月（注册当月免缴首月费，月费记录已入账当月）
            if not dev.fee_start_month:
                dev.fee_start_month = get_current_month()
            db.commit()

            # 注册留痕（贡献分已由月费联动 +10，这里仅记录来源不重复加分）
            if not db.query(Contribution).filter(
                Contribution.developer_dna == developer_dna,
                Contribution.contribution_type == "registration",
            ).first():
                from .dna_generator import generate_dna
                db.add(Contribution(
                    developer_dna=developer_dna,
                    contribution_type="registration",
                    content="注册激活（首月费支付）",
                    score=0,
                    dna=generate_dna("CONTRIB"),
                ))
                db.commit()

        result["message"] = "支付确认成功，开发者已激活，首月费入账"
        return result
    finally:
        db.close()
