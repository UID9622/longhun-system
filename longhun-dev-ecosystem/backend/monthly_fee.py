#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · 月度主权确认金模块
DNA: #龍芯⚡️丙午·丙申·庚申·亥时-MONTHLY-FEE-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

约定（LH-DEVELOPER-FEE-CONVENTION-v1.0.md）:
  - 每月1元起步·上不封顶·杜绝一毛不拔
  - 状态机: active(活跃) / grace(宽限1-3月) / frozen(冻结>3月)
  - 支付走 gateway.py 正规网关: 预支付 → 回调验签 → 幂等入账
"""

import csv
import io
import json
import time
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from .models import Developer, PaymentOrder, MonthlyFeeRecord, Contribution
from .dna_generator import generate_dna
from .gateway import get_gateway, sign_sandbox
from .config import ADMIN_TOKEN, PAYMENT_MIN_AMOUNT

MONTHLY_FEE_MIN = PAYMENT_MIN_AMOUNT  # 1元起步
GRACE_MONTHS = 3                       # 宽限3个月
FREEZE_MONTHS = 3                      # 超过3个月冻结


# ============================================================
# 基础工具
# ============================================================

def get_current_month() -> str:
    """当前月份 YYYY-MM"""
    return datetime.now().strftime("%Y-%m")


def get_month_delta(month_from: str, month_to: str) -> int:
    """两月份月数差（month_to - month_from），year_month 格式 YYYY-MM"""
    try:
        y1, m1 = map(int, month_from.split("-"))
        y2, m2 = map(int, month_to.split("-"))
        return (y2 - y1) * 12 + (m2 - m1)
    except (ValueError, AttributeError):
        return 0


def _biz_month() -> str:
    """业务月份：月初（1号）计上月，其余计当月——保证"当月1日生成当月账单"语义"""
    now = datetime.now()
    if now.day <= 1:
        # 1号当天：账单归属上月（上月欠费判定更准确）
        return get_current_month()
    return get_current_month()


# ============================================================
# 状态机
# ============================================================

def check_developer_fee_status(dev_dna: str, db: Session) -> dict:
    """
    检查开发者月费状态（协议第四条）
    返回: {status: active/grace/frozen/invalid, message, arrears, current_month, last_paid}
    """
    dev = db.query(Developer).filter(Developer.dna == dev_dna).first()
    if not dev:
        return {"status": "invalid", "message": "开发者不存在"}

    current_month = get_current_month()
    # 计费起始：未设置则按注册月（注册月免缴）
    fee_start = dev.fee_start_month or (dev.registered_at.strftime("%Y-%m") if dev.registered_at else current_month)
    last_paid = dev.last_paid_month or fee_start

    # 已冻结 → 直接返回冻结（需补缴恢复）
    if dev.monthly_fee_status == "frozen":
        return {
            "status": "frozen",
            "message": f"🔴 已冻结，欠缴 {dev.fee_arrears or 1} 个月，需补缴后恢复",
            "arrears": dev.fee_arrears or get_month_delta(last_paid, current_month),
            "current_month": current_month,
            "last_paid": last_paid,
        }

    # 新注册首月免缴（未到计费起始月之前都算 active）
    if get_month_delta(fee_start, current_month) <= 0:
        return {
            "status": "active",
            "message": "✅ 注册首月免缴，身份活跃",
            "arrears": 0,
            "current_month": current_month,
            "last_paid": last_paid,
            "free_first_month": True,
        }

    months_diff = get_month_delta(last_paid, current_month)
    if months_diff <= 0:
        return {
            "status": "active",
            "message": "✅ 本月月费已缴",
            "arrears": 0,
            "current_month": current_month,
            "last_paid": last_paid,
        }
    if months_diff <= GRACE_MONTHS:
        return {
            "status": "grace",
            "message": f"🟡 宽限期内，欠缴 {months_diff} 个月",
            "arrears": months_diff,
            "current_month": current_month,
            "last_paid": last_paid,
        }
    return {
        "status": "frozen",
        "message": f"🔴 已欠缴 {months_diff} 个月，超过宽限期，已冻结",
        "arrears": months_diff,
        "current_month": current_month,
        "last_paid": last_paid,
    }


# ============================================================
# 账单 & 支付（正规网关链路）
# ============================================================

def create_monthly_bill(dev_dna: str, db: Session, amount: float = None, channel: str = "") -> dict:
    """
    生成当月账单（幂等）: 未支付复用订单 → 已支付返回已缴
    返回: {order_id, year_month, amount, min_amount, channel, qr_code/pay_url, message, status}
    """
    dev = db.query(Developer).filter(Developer.dna == dev_dna).first()
    if not dev:
        return {"error": "开发者不存在"}

    current_month = get_current_month()

    # 幂等1: 当月已有 paid 记录 → 已缴
    paid = db.query(MonthlyFeeRecord).filter(
        MonthlyFeeRecord.developer_dna == dev_dna,
        MonthlyFeeRecord.year_month == current_month,
        MonthlyFeeRecord.status == "paid",
    ).first()
    if paid:
        return {
            "message": "✅ 本月已缴",
            "year_month": current_month,
            "amount": paid.amount,
            "status": "paid",
            "order_id": paid.order_id,
        }

    # 幂等2: 当月已有 pending 订单 → 复用
    pending_order = db.query(PaymentOrder).filter(
        PaymentOrder.developer_dna == dev_dna,
        PaymentOrder.subject == f"{current_month} 月费",
        PaymentOrder.status == "pending",
    ).first()

    fee_amount = max(MONTHLY_FEE_MIN, amount or MONTHLY_FEE_MIN)
    gateway = get_gateway(channel)
    ch = gateway.channel

    if pending_order:
        order_id = pending_order.order_id
        # 金额变更则更新
        pending_order.amount = fee_amount
        db.commit()
    else:
        # 新建订单（正规网关商户订单号）
        from .gateway import _gen_order_id
        order_id = _gen_order_id("LH")
        order = PaymentOrder(
            order_id=order_id,
            developer_dna=dev_dna,
            amount=fee_amount,
            channel=ch,
            subject=f"{current_month} 月费",
            status="pending",
            created_at=datetime.now(),
        )
        db.add(order)
        db.commit()

    # 预支付（沙箱返回二维码；真实通道返回支付参数）
    prepay = gateway.create_prepay(order_id, fee_amount, f"{current_month} 月费", dev_dna)
    if not prepay.get("success", True):
        return prepay

    return {
        "year_month": current_month,
        "amount": fee_amount,
        "min_amount": MONTHLY_FEE_MIN,
        "order_id": order_id,
        "channel": ch,
        "qr_code": prepay.get("qr_code"),
        "pay_url": prepay.get("pay_url"),
        "expires_at": prepay.get("expires_at"),
        "message": f"📌 请支付 {current_month} 月费 {fee_amount} 元",
        "status": "pending",
    }


def handle_payment_notify(params: dict, signature: str, db: Session, channel: str = "") -> dict:
    """
    支付回调入账（正规网关链路·幂等）:
      验签 → 标准化 → 订单校验 → 金额核对 → 幂等入账 → 联动开发者状态+贡献分
    返回: {success, message, order_id, amount}
    """
    gateway = get_gateway(channel or params.get("channel", ""))
    if not gateway.verify_notify(params, signature):
        return {"success": False, "error": "验签失败"}

    parsed = gateway.parse_notify(params)
    order_id = parsed.get("order_id", "")
    if not order_id:
        return {"success": False, "error": "回调缺少订单号"}

    order = db.query(PaymentOrder).filter(PaymentOrder.order_id == order_id).first()
    if not order:
        return {"success": False, "error": "订单不存在"}

    # 幂等: 已支付直接返回成功（不重复入账）
    if order.status == "paid":
        return {"success": True, "message": "订单已入账", "order_id": order_id, "amount": order.amount, "duplicated": True}

    if parsed.get("status") != "paid":
        return {"success": False, "error": "回调状态非成功"}

    # 金额核对（防篡改）: 回调金额 >= 订单金额（多缴计入公共池）
    callback_amount = parsed.get("amount", 0)
    if callback_amount < order.amount:
        return {"success": False, "error": f"回调金额不符: 订单 {order.amount} vs 回调 {callback_amount}"}

    # 入账
    order.status = "paid"
    order.paid_at = datetime.now()
    order.transaction_id = parsed.get("transaction_id") or order.transaction_id
    order.amount = callback_amount  # 以实际支付为准（多缴入池）
    order.notify_raw = json.dumps(params, ensure_ascii=False)

    dev = db.query(Developer).filter(Developer.dna == order.developer_dna).first()
    if not dev:
        db.commit()
        return {"success": False, "error": "关联开发者不存在"}

    # 更新开发者月费状态
    current_month = order.subject.replace(" 月费", "") if order.subject else get_current_month()
    if not current_month or "-" not in current_month:
        current_month = get_current_month()
    dev.last_paid_month = current_month
    dev.monthly_fee_status = "active"
    dev.fee_arrears = 0
    dev.total_contributed = (dev.total_contributed or 0) + callback_amount

    # 月费记录（幂等 upsert）
    fee_rec = db.query(MonthlyFeeRecord).filter(
        MonthlyFeeRecord.developer_dna == order.developer_dna,
        MonthlyFeeRecord.year_month == current_month,
    ).first()
    if not fee_rec:
        fee_rec = MonthlyFeeRecord(
            developer_dna=order.developer_dna,
            year_month=current_month,
            amount=callback_amount,
            paid_at=datetime.now(),
            status="paid",
            order_id=order_id,
        )
        db.add(fee_rec)
    else:
        fee_rec.status = "paid"
        fee_rec.paid_at = datetime.now()
        fee_rec.amount = callback_amount
        fee_rec.order_id = order_id

    db.commit()

    # 贡献分联动: 按时缴纳月费 +10
    contrib_dna = generate_dna("FEE")
    contrib = Contribution(
        developer_dna=order.developer_dna,
        contribution_type="monthly_fee",
        content=f"支付 {current_month} 月费 {callback_amount} 元",
        score=10,
        dna=contrib_dna,
    )
    db.add(contrib)
    dev.contribution_score = (dev.contribution_score or 0) + 10
    db.commit()

    return {
        "success": True,
        "message": f"✅ {current_month} 月费支付成功",
        "order_id": order_id,
        "amount": callback_amount,
        "year_month": current_month,
    }


def confirm_monthly_payment(dev_dna: str, order_id: str, db: Session, channel: str = "sandbox") -> dict:
    """
    确认月费支付（沙箱模式：本地生成回调闭环；真实通道由网关异步回调 handle_payment_notify）
    """
    if channel != "sandbox":
        return {"success": False, "error": "非沙箱通道请走网关回调 /api/pay/notify"}

    order = db.query(PaymentOrder).filter(
        PaymentOrder.order_id == order_id,
        PaymentOrder.developer_dna == dev_dna,
    ).first()
    if not order:
        return {"success": False, "error": "订单不存在或不属于该开发者"}
    if order.status == "paid":
        return {"success": True, "message": "已支付", "order_id": order_id, "amount": order.amount}

    # 构造沙箱回调并走统一入账链路（验签闭环）
    params = {
        "order_id": order_id,
        "transaction_id": f"SANDBOX-{int(time.time())}",
        "amount": order.amount,
        "status": "paid",
        "channel": "sandbox",
    }
    signature = sign_sandbox(params)
    return handle_payment_notify(params, signature, db)


# ============================================================
# 冻结任务（每月1日 cron 调用）
# ============================================================

def freeze_expired_developers(db: Session) -> dict:
    """冻结超期开发者（协议第五条）"""
    current_month = get_current_month()
    devs = db.query(Developer).filter(Developer.monthly_fee_status != "frozen").all()
    frozen = 0
    restored = 0
    for dev in devs:
        st = check_developer_fee_status(dev.dna, db)
        if st["status"] == "frozen":
            if dev.monthly_fee_status != "frozen":
                dev.monthly_fee_status = "frozen"
                dev.fee_arrears = st["arrears"]
                frozen += 1
    db.commit()
    return {"checked": len(devs), "frozen": frozen, "restored": restored, "month": current_month}


# ============================================================
# 历史账单 / 统计
# ============================================================

def get_fee_history(dev_dna: str, db: Session, limit: int = 12) -> dict:
    """缴费历史（含 pending 账单状态）"""
    records = (
        db.query(MonthlyFeeRecord)
        .filter(MonthlyFeeRecord.developer_dna == dev_dna)
        .order_by(MonthlyFeeRecord.year_month.desc())
        .limit(limit)
        .all()
    )
    return {
        "records": [r.to_dict() for r in records],
        "total": len(records),
    }


def get_public_fee_stats(db: Session) -> dict:
    """公开统计（公共贡献池·聚合数据·不暴露个体敏感字段）"""
    paid = db.query(MonthlyFeeRecord).filter(MonthlyFeeRecord.status == "paid")
    total_count = paid.count()
    total_amount = sum(r.amount for r in paid.all()) or 0

    top = (
        db.query(
            Developer.nickname,
            Developer.dna,
            func.sum(MonthlyFeeRecord.amount).label("total"),
            func.count(MonthlyFeeRecord.id).label("months"),
        )
        .join(MonthlyFeeRecord, Developer.dna == MonthlyFeeRecord.developer_dna)
        .filter(MonthlyFeeRecord.status == "paid")
        .group_by(Developer.dna)
        .order_by(func.sum(MonthlyFeeRecord.amount).desc())
        .limit(10)
        .all()
    )

    return {
        "total_payments": total_count,
        "total_amount": round(total_amount, 2),
        "min_fee": MONTHLY_FEE_MIN,
        "top_contributors": [
            {"nickname": c.nickname, "dna": c.dna, "total": round(c.total, 2), "months": c.months}
            for c in top
        ],
    }


# ============================================================
# 导出（管理员 Token 鉴权 · CSV/JSON）
# ============================================================

def _check_admin(token: str) -> bool:
    """管理员 Token 校验（防导出裸奔）"""
    return token == ADMIN_TOKEN


def _csv_out(rows: list, headers: list) -> str:
    """CSV 输出（带 BOM，Excel 中文不乱码）"""
    buf = io.StringIO()
    buf.write("\ufeff")
    writer = csv.writer(buf)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)
    return buf.getvalue()


def _dump(rows: list, headers: list, fmt: str) -> dict:
    """统一导出格式转换"""
    if fmt == "csv":
        return {
            "success": True,
            "format": "csv",
            "filename": "export.csv",
            "content": _csv_out(rows, headers),
        }
    return {
        "success": True,
        "format": "json",
        "content": json.dumps(rows, ensure_ascii=False, indent=2),
    }


def export_fee_records(db: Session, token: str, fmt: str = "csv") -> dict:
    """导出全部缴费记录（历史账单）"""
    if not _check_admin(token):
        return {"success": False, "error": "管理员 Token 无效"}
    rows = db.query(MonthlyFeeRecord).order_by(MonthlyFeeRecord.year_month.desc()).all()
    data = [
        [r.developer_dna, r.year_month, r.amount, r.status, r.paid_at.isoformat() if r.paid_at else "", r.order_id or ""]
        for r in rows
    ]
    headers = ["developer_dna", "year_month", "amount", "status", "paid_at", "order_id"]
    return _dump(data, headers, fmt)


def export_contributions(db: Session, token: str, fmt: str = "csv") -> dict:
    """导出全部贡献记录"""
    if not _check_admin(token):
        return {"success": False, "error": "管理员 Token 无效"}
    rows = db.query(Contribution).order_by(Contribution.created_at.desc()).all()
    data = [
        [c.developer_dna, c.contribution_type, c.score, c.content or "", c.created_at.isoformat() if c.created_at else "", c.dna]
        for c in rows
    ]
    headers = ["developer_dna", "type", "score", "content", "created_at", "dna"]
    return _dump(data, headers, fmt)


def export_code_dna(db: Session, token: str, fmt: str = "csv") -> dict:
    """导出全部代码 DNA 记录"""
    if not _check_admin(token):
        return {"success": False, "error": "管理员 Token 无效"}
    from .models import CodeDNA

    rows = db.query(CodeDNA).order_by(CodeDNA.created_at.desc()).all()
    data = [
        [c.developer_dna, c.file_path, c.language, c.line_count, c.file_hash, c.created_at.isoformat() if c.created_at else "", c.dna]
        for c in rows
    ]
    headers = ["developer_dna", "file_path", "language", "line_count", "file_hash", "created_at", "dna"]
    return _dump(data, headers, fmt)


def export_developers(db: Session, token: str, fmt: str = "csv") -> dict:
    """导出开发者名册"""
    if not _check_admin(token):
        return {"success": False, "error": "管理员 Token 无效"}
    rows = db.query(Developer).order_by(Developer.registered_at.desc()).all()
    data = [
        [
            d.dna,
            d.name,
            d.email,
            d.nickname,
            d.status,
            d.monthly_fee_status,
            d.last_paid_month or "",
            d.total_contributed or 0,
            d.contribution_score,
            d.dna_count,
            d.registered_at.isoformat() if d.registered_at else "",
        ]
        for d in rows
    ]
    headers = [
        "dna", "name", "email", "nickname", "status", "monthly_fee_status",
        "last_paid_month", "total_contributed", "contribution_score", "dna_count", "registered_at",
    ]
    return _dump(data, headers, fmt)
