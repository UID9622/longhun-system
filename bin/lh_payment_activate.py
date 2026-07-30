#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-PAYMENT-ACTIVATE-v1.0-9E1D4C7B
# CREATOR: 诸葛鑫（UID9622）
# PROTOCOL: CC BY-NC-SA 4.0
# 功能: 龍魂系统 · 激活经济主权引擎 v1.0
# 说明: 一元起步 · 上不封顶 · 实名留痕 · 本地账本
"""
龍魂系统 · 激活经济主权引擎 v1.0

用法:
  生成订单:
    python bin/lh_payment_activate.py --amount 1.00 --name 张三

  确认到账（手动/自动）:
    python bin/lh_payment_activate.py --confirm ORDER_ID --tx-id TX123456

  查询状态:
    python bin/lh_payment_activate.py --status

DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-PAYMENT-ACTIVATE-v1.0-9E1D4C7B
"""

import os
import sys
import json
import hashlib
import time
import re
import uuid
from datetime import datetime
from pathlib import Path
from decimal import Decimal, InvalidOperation

try:
    import qrcode
except ImportError:
    qrcode = None

# ═══════════════════════════════════════════════════════════════════════════════
# P0 配置
# ═══════════════════════════════════════════════════════════════════════════════

P0_CONFIG = {
    "uid": "9622",
    "founder": "龍芯北辰 UID9622",
    "min_amount": Decimal("1.00"),
    "currency": "CNY",
    "log_dir": os.path.expanduser("~/.longhun"),
    "registry_file": "payment_registry.json",
    "audit_log": "payment_activate.log",
    "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
}


# ═══════════════════════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════════════════════

def _now_iso() -> str:
    return datetime.now().isoformat()


def _header(title: str):
    print("=" * 72)
    print(f"🐉 {title}")
    print("=" * 72)


def _audit(path: Path, message: str, level: str = "INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{level}] {message}"
    with open(path, "a", encoding="utf-8") as f:
        f.write(entry + "\n")
    print(entry)


def _now_ganzhi():
    now = datetime.now()
    gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    year_g = gan[(now.year - 4) % 10]
    year_z = zhi[(now.year - 4) % 12]
    month_g = gan[(now.year * 12 + now.month + 12) % 10]
    month_z = zhi[(now.month + 1) % 12]
    day_g = gan[(now.toordinal() + 40) % 10]
    day_z = zhi[(now.toordinal() + 40) % 12]
    return f"{year_g}{year_z}·{month_g}{month_z}·{day_g}{day_z}"


def _gua_name():
    gua_list = [
        "乾", "坤", "屯", "蒙", "需", "讼", "师", "比", "小畜", "履",
        "泰", "否", "同人", "大有", "谦", "豫", "随", "蛊", "临", "观",
        "噬嗑", "贲", "剥", "复", "无妄", "大畜", "颐", "大过", "坎", "离",
        "咸", "恒", "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解",
        "损", "益", "夬", "姤", "萃", "升", "困", "井", "革", "鼎",
        "震", "艮", "渐", "归妹", "丰", "旅", "巽", "兑", "涣", "节",
        "中孚", "小过", "既济", "未济",
    ]
    return gua_list[datetime.now().minute % 64]


def _generate_dna(order_id: str) -> str:
    dev_hash = hashlib.sha256(order_id.encode()).hexdigest()[:8]
    return f"#龍芯⚡️{_now_ganzhi()}·{_gua_name()}-激活经济-v1.0-{dev_hash}"


def _parse_amount(value: str) -> Decimal:
    try:
        d = Decimal(value)
    except InvalidOperation:
        raise ValueError(f"金额格式错误: {value}")
    if d != d.quantize(Decimal("0.01")):
        raise ValueError("金额最多两位小数")
    return d


def _generate_order_id() -> str:
    return f"PAY-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"


# ═══════════════════════════════════════════════════════════════════════════════
# 龍魂支付激活引擎
# ═══════════════════════════════════════════════════════════════════════════════

class LonghunPayment:
    """龍魂系统 · 激活经济主权引擎"""

    def __init__(self):
        self.log_dir = Path(P0_CONFIG["log_dir"])
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.registry_path = self.log_dir / P0_CONFIG["registry_file"]
        self.audit_path = self.log_dir / P0_CONFIG["audit_log"]
        self.registry = self._load_registry()

    def _load_registry(self):
        if self.registry_path.exists():
            try:
                with open(self.registry_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        return {
            "orders": [],
            "tx_ids": [],
            "total_amount": "0.00",
            "total_orders": 0,
            "confirmed_orders": 0,
        }

    def _save_registry(self):
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(self.registry, f, ensure_ascii=False, indent=2)

    def generate_order(self, amount: Decimal, name: str = "匿名", note: str = ""):
        """生成支付订单与二维码"""
        _header("龍魂系统 · 激活经济主权 · 生成订单")

        if amount < P0_CONFIG["min_amount"]:
            print(f"\n❌ 金额不得低于 {P0_CONFIG['min_amount']} 元")
            _audit(self.audit_path, f"订单生成失败: 金额过低 {amount}", "WARN")
            return False

        order_id = _generate_order_id()
        dna = _generate_dna(order_id)

        # 支付二维码内容：订单信息 + 激活舱链接
        qr_payload = (
            f"龍魂激活订单\n"
            f"订单号: {order_id}\n"
            f"金额: {amount} {P0_CONFIG['currency']}\n"
            f"支付人: {name}\n"
            f"备注: 支持龍魂系统\n"
            f"激活舱: https://uid9622.cn/activation-lab/?order={order_id}"
        )

        img_path = self.log_dir / f"longhun_payment_{order_id}.png"
        if qrcode:
            qr = qrcode.QRCode(version=3, box_size=8, border=2)
            qr.add_data(qr_payload)
            qr.make(fit=True)
            qr.make_image(fill_color="black", back_color="white").save(img_path)
        else:
            img_path = None
            print("⚠️ 未安装 qrcode，仅输出文本订单")

        order = {
            "order_id": order_id,
            "amount": str(amount),
            "currency": P0_CONFIG["currency"],
            "name": name,
            "note": note,
            "status": "pending",
            "created_at": _now_iso(),
            "confirmed_at": None,
            "tx_id": None,
            "dna": dna,
        }
        self.registry["orders"].append(order)
        self.registry["total_orders"] = len(self.registry["orders"])
        self._save_registry()

        print(f"\n✅ 订单已生成")
        print(f"   订单号: {order_id}")
        print(f"   金额:   {amount} {P0_CONFIG['currency']}")
        print(f"   支付人: {name}")
        print(f"   DNA:    {dna}")
        if img_path:
            print(f"   二维码: {img_path}")
        print(f"\n💡 请扫码支付并备注订单号: {order_id}")
        print(f"   支付完成后回填交易单号:")
        print(f"      python bin/lh_payment_activate.py --confirm {order_id} --tx-id <交易单号>")
        print(f"\n🔒 确认码: {P0_CONFIG['confirm']}")

        _audit(self.audit_path, f"生成订单: {order_id}, 金额={amount}, 支付人={name}")
        return True

    def confirm_order(self, order_id: str, tx_id: str):
        """确认订单到账并发放激活票"""
        _header("龍魂系统 · 激活经济主权 · 确认到账")

        if not order_id or not tx_id:
            print("\n❌ 订单号和交易单号都不能为空")
            return False

        if tx_id in self.registry["tx_ids"]:
            print("\n❌ 交易单号已使用 · 防重放拒绝")
            _audit(self.audit_path, f"确认失败: tx_id 已使用 {tx_id}", "WARN")
            return False

        order = None
        for o in self.registry["orders"]:
            if o["order_id"] == order_id:
                order = o
                break

        if not order:
            print(f"\n❌ 订单不存在: {order_id}")
            _audit(self.audit_path, f"确认失败: 订单不存在 {order_id}", "WARN")
            return False

        if order["status"] == "confirmed":
            print(f"\n❌ 订单已确认，无需重复确认")
            return False

        order["status"] = "confirmed"
        order["tx_id"] = tx_id
        order["confirmed_at"] = _now_iso()

        self.registry["tx_ids"].append(tx_id)
        total = Decimal(self.registry["total_amount"]) + Decimal(order["amount"])
        self.registry["total_amount"] = str(total.quantize(Decimal("0.01")))
        self.registry["confirmed_orders"] = sum(
            1 for o in self.registry["orders"] if o["status"] == "confirmed"
        )
        self._save_registry()

        print(f"\n✅ 订单确认成功 · 激活票已发放")
        print(f"   订单号:   {order_id}")
        print(f"   交易单号: {tx_id}")
        print(f"   金额:     {order['amount']} {order['currency']}")
        print(f"   支付人:   {order['name']}")
        print(f"   DNA:      {order['dna']}")
        print(f"   确认时间: {order['confirmed_at']}")
        print(f"\n🎫 该订单现在可用于 MFA/核心功能激活")

        _audit(self.audit_path, f"确认到账: {order_id}, tx={tx_id}, 金额={order['amount']}", "SUCCESS")
        return True

    def status(self):
        """查询激活经济状态"""
        _header("龍魂系统 · 激活经济主权 · 状态")

        total_amount = Decimal(self.registry.get("total_amount", "0.00"))
        total_orders = self.registry.get("total_orders", 0)
        confirmed = self.registry.get("confirmed_orders", 0)
        pending = total_orders - confirmed

        print(f"\n累计支持金额: {total_amount} {P0_CONFIG['currency']}")
        print(f"订单总数:     {total_orders}")
        print(f"已确认:       {confirmed}")
        print(f"待支付:       {pending}")

        if not self.registry["orders"]:
            print("\n暂无订单")
            return

        print("\n订单列表:")
        for o in self.registry["orders"][-10:]:
            icon = {"confirmed": "🟢", "pending": "🟡", "refunded": "🔴"}.get(o["status"], "⚪")
            print(
                f"  {icon} {o['order_id']} | {o['amount']:>8s} {o['currency']} | "
                f"{o['name']:8s} | {o['status']:10s} | {o.get('tx_id', '-') or '-'}"
            )


# ═══════════════════════════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂系统 · 激活经济主权引擎 v1.0")
    parser.add_argument("--amount", help="支付金额（元），最低 1.00")
    parser.add_argument("--name", default="匿名", help="支付人真实姓名（默认匿名）")
    parser.add_argument("--note", default="", help="备注")
    parser.add_argument("--confirm", help="确认订单到账，指定订单号")
    parser.add_argument("--tx-id", help="交易单号")
    parser.add_argument("--status", action="store_true", help="查询激活经济状态")
    args = parser.parse_args()

    lp = LonghunPayment()

    if args.amount:
        try:
            amount = _parse_amount(args.amount)
        except ValueError as e:
            print(f"\n❌ {e}")
            sys.exit(1)
        lp.generate_order(amount, args.name, args.note)
    elif args.confirm:
        if not args.tx_id:
            print("\n❌ 确认订单必须提供 --tx-id")
            sys.exit(1)
        lp.confirm_order(args.confirm, args.tx_id)
    elif args.status:
        lp.status()
    else:
        parser.print_help()
        print(f"\nDNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-PAYMENT-ACTIVATE-v1.0-9E1D4C7B")
        print(f"确认码: {P0_CONFIG['confirm']}")


if __name__ == "__main__":
    main()
