#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 良心支付系统 v1.0
DNA: #龍芯⚡️丙午·丙申·壬戌·巳时- PAYMENT-LIANGXIN-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）· License: MulanPSL v2（工程层）
说明: 一元起步 · 上不封顶 · 人人平等 · 良心支付。
      用户自主填金额，系统不设上限；当月首次使用触发扣款；
      良心支付不做强冻结，只做到期提醒——信任优先。
      数据: ~/.longhun/payment/payment.db（本地·append-only 审计留痕）
"""

import argparse
import hashlib
import sqlite3
import sys
import time
from datetime import datetime, date
from pathlib import Path
from typing import Dict, Optional

# 复用龍魂时间引擎生成标准干支四柱时间戳（失败则降级 datetime）
try:
    from bin.lh_time_engine import get_output_stamp
except Exception:
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "bin"))
        from lh_time_engine import get_output_stamp
    except Exception:
        get_output_stamp = None

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
MIN_AMOUNT = 1  # 一元起步
DB_PATH = Path.home() / ".longhun" / "payment" / "payment.db"


def _now_stamp() -> str:
    """标准时间戳: 干支四柱·卦象（降级为 ISO）"""
    if get_output_stamp:
        try:
            return get_output_stamp(format_type="compact")
        except Exception:
            pass
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


def generate_dna(suffix: str = "PAY") -> str:
    """生成 v∞ 干支卦 DNA 追溯码（SHA-256 截断，禁 MD5）"""
    h = hashlib.sha256(f"{suffix}{time.time()}{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{suffix}-{h}-{UID}"


def _next_due_date(from_date: Optional[date] = None) -> str:
    """下期应缴日: 每月1号（本月1号之后 → 下月1号；1号当天 → 下月1号）"""
    today = from_date or date.today()
    if today.day > 1:
        if today.month == 12:
            return f"{today.year + 1}-01-01"
        return f"{today.year}-{today.month + 1:02d}-01"
    if today.month == 12:
        return f"{today.year + 1}-01-01"
    return f"{today.year}-{today.month + 1:02d}-01"


class PaymentSystem:
    """良心支付系统（本地 SQLite · append-only 审计）"""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                dna TEXT PRIMARY KEY,
                user_id TEXT,
                amount INTEGER DEFAULT 1,
                start_date TEXT,
                last_pay_date TEXT,
                next_due_date TEXT,
                status TEXT DEFAULT 'active',
                total_paid INTEGER DEFAULT 0,
                created_at TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS payment_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dna TEXT,
                amount INTEGER,
                method TEXT,
                timestamp TEXT,
                status TEXT,
                note TEXT
            )
        """)
        conn.commit()
        conn.close()

    def register(self, dna: str, user_id: str, amount: int = 1) -> Dict:
        """注册: 一元起步 · 已存在不覆盖（防止误改已有账目）"""
        amount = max(MIN_AMOUNT, int(amount or MIN_AMOUNT))
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT amount, next_due_date FROM subscribers WHERE dna = ?", (dna,))
        existing = cur.fetchone()
        if existing:
            conn.close()
            return {
                "status": "exists",
                "dna": dna,
                "amount": existing[0],
                "next_due": existing[1],
                "message": f"ℹ️ {user_id} 已注册（每月 {existing[0]} 元）——直接 lh-pay --pay 续费即可",
            }
        now = datetime.now().isoformat(timespec="seconds")
        next_due = _next_due_date()
        cur.execute("""
            INSERT INTO subscribers
            (dna, user_id, amount, start_date, last_pay_date, next_due_date, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 'active', ?)
        """, (dna, user_id, amount, now, now, next_due, now))
        conn.commit()
        conn.close()
        return {
            "status": "registered",
            "dna": dna,
            "amount": amount,
            "next_due": next_due,
            "message": f"✅ 注册成功！每月 {amount} 元，感谢信任！",
        }

    def pay(self, dna: str, amount: Optional[int] = None, method: str = "良心支付") -> Dict:
        """支付/续费: 用户自主填金额 · 上不封顶 · 1元起"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT amount, total_paid, user_id FROM subscribers WHERE dna = ?", (dna,))
        row = cur.fetchone()
        if not row:
            conn.close()
            return {"status": "error", "message": "❌ 未找到用户，请先 lh-pay --register 注册"}

        default_amount, total_paid, user_id = row
        pay_amount = int(amount) if amount and amount > 0 else default_amount
        pay_amount = max(MIN_AMOUNT, pay_amount)

        now = datetime.now().isoformat(timespec="seconds")
        next_due = _next_due_date()
        cur.execute("""
            UPDATE subscribers
            SET last_pay_date = ?, next_due_date = ?, total_paid = total_paid + ?
            WHERE dna = ?
        """, (now, next_due, pay_amount, dna))
        cur.execute("""
            INSERT INTO payment_log (dna, amount, method, timestamp, status, note)
            VALUES (?, ?, ?, ?, 'success', ?)
        """, (dna, pay_amount, method, now, f"next_due={next_due}"))
        conn.commit()
        conn.close()
        return {
            "status": "success",
            "dna": dna,
            "amount": pay_amount,
            "total_paid": total_paid + pay_amount,
            "next_due": next_due,
            "message": f"✅ {user_id} 收到 {pay_amount} 元！下期 {next_due}，感谢支持！",
        }

    def status(self, dna: str) -> Dict:
        """查询状态: 显示累计 · 下期应缴 · 是否到期（到期仅提醒，不冻结）"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            SELECT user_id, amount, start_date, last_pay_date, next_due_date, status, total_paid
            FROM subscribers WHERE dna = ?
        """, (dna,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return {"status": "error", "message": "❌ 未找到用户"}
        user_id, amount, start_date, last_pay, next_due, status, total_paid = row
        due = ""
        try:
            if date.fromisoformat(next_due) <= date.today():
                due = "（已到期，请续费）"
        except (ValueError, TypeError):
            pass
        return {
            "user_id": user_id,
            "amount": amount,
            "start_date": start_date,
            "last_pay_date": last_pay,
            "next_due_date": next_due,
            "status": status,
            "total_paid": total_paid,
            "due_hint": due,
        }

    def stats(self) -> Dict:
        """全局统计（公开聚合数据）"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM subscribers")
        total_users = cur.fetchone()[0]
        cur.execute("SELECT COALESCE(SUM(total_paid), 0) FROM subscribers")
        total_revenue = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM payment_log WHERE status = 'success'")
        total_payments = cur.fetchone()[0]
        conn.close()
        return {
            "total_users": total_users,
            "total_payments": total_payments,
            "total_revenue": total_revenue,
            "average": round(total_revenue / total_users, 2) if total_users > 0 else 0,
            "message": f"📊 目前 {total_users} 位支持者 · 共 {total_payments} 笔 · 总收入 {total_revenue} 元",
        }

    def list_all(self, limit: int = 20) -> list:
        """支持者名册（公开昵称+累计，不暴露敏感字段）"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT user_id, amount, total_paid, status, last_pay_date FROM subscribers "
            "ORDER BY total_paid DESC LIMIT ?",
            (limit,),
        )
        rows = cur.fetchall()
        conn.close()
        return rows


def _print_signature():
    print("=" * 60)
    print(" 🐉 龍魂 · 良心支付系统")
    print(" 一元起步 · 上不封顶 · 人人平等 · 良心支付")
    print(f" DNA: {_now_stamp()}-LIANGXIN-PAY")
    print(f" 确认码: {CONFIRM}")
    print(" GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
    print("=" * 60)


def main(argv=None):
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 良心支付系统（一元起步·上不封顶·人人平等）")
    parser.add_argument("--register", "-r", help="注册 (dna,用户名,金额)")
    parser.add_argument("--pay", "-p", help="支付/续费 (dna,金额) — 金额不设上限")
    parser.add_argument("--status", "-s", help="查看状态 (dna)")
    parser.add_argument("--stats", action="store_true", help="全局统计")
    parser.add_argument("--list", "-l", action="store_true", help="支持者名册")
    parser.add_argument("--dna", help="生成新 DNA 追溯码")

    args = parser.parse_args(argv)
    ps = PaymentSystem()

    if args.dna:
        print(generate_dna(args.dna.upper() if args.dna.isalpha() else "PAY"))
        return

    if args.register:
        parts = args.register.split(",")
        if len(parts) < 2:
            print("❌ 用法: lh-pay --register \"DNA,用户名,金额\"")
            return
        dna = parts[0].strip()
        user_id = parts[1].strip()
        amount = int(parts[2]) if len(parts) > 2 and parts[2].strip().isdigit() else 1
        result = ps.register(dna, user_id, amount)
        print(result["message"])
        print(f"  DNA: {dna}")
        print(f"  每月: {result['amount']} 元 · 下期应缴: {result.get('next_due', '-')}")
        return

    if args.pay:
        parts = args.pay.split(",")
        if not parts or not parts[0].strip():
            print("❌ 用法: lh-pay --pay \"DNA,金额\"")
            return
        dna = parts[0].strip()
        amount = int(parts[1]) if len(parts) > 1 and parts[1].strip().isdigit() else None
        result = ps.pay(dna, amount)
        print(result["message"])
        if result["status"] == "success":
            print(f"  累计支持: {result['total_paid']} 元")
        return

    if args.status:
        result = ps.status(args.status)
        if result.get("status") == "error":
            print(result["message"])
        else:
            print(f"📊 用户: {result['user_id']}")
            print(f"  每月: {result['amount']} 元")
            print(f"  累计: {result['total_paid']} 元")
            print(f"  状态: {result['status']}{result['due_hint']}")
            print(f"  注册: {result['start_date']}")
            print(f"  最近: {result['last_pay_date']}")
            print(f"  下期: {result['next_due_date']}")
        return

    if args.stats:
        stats = ps.stats()
        _print_signature()
        print()
        print(stats["message"])
        print()
        print("💡 感谢每一位支持者！")
        print("   1元不嫌少，1亿不嫌多")
        print("   所有用户平等，无VIP特权")
        return

    if args.list:
        rows = ps.list_all()
        print("🏆 支持者名册（累计贡献排行）")
        print("=" * 50)
        if not rows:
            print("🟡 还没有支持者——第一个吃螃蟹的人是你吗？")
            return
        for idx, (user_id, amount, total, status, last_pay) in enumerate(rows, 1):
            print(f"  {idx}. {user_id:<16} 月供{amount}元 · 累计{total}元 · {status}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
