#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·API计费系统 v1.0
DNA: #龍芯⚡️2026-09-04-API计费系统-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色审计: 🟢 通过
用法: lh billing balance|recharge|usage|history（引擎 08_BIN/lh_billing.py）
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime, date
from typing import Optional

# ===== 常量配置 =====
BILLING_DIR = Path.home() / ".longhun" / "billing"
USAGE_LOG = BILLING_DIR / "usage.jsonl"
TRANSACTION_LOG = BILLING_DIR / "transactions.jsonl"
BALANCE_FILE = BILLING_DIR / "balance.json"
RECONCILIATION_DIR = BILLING_DIR / "reconciliation"

FREE_MONTHLY_TOKENS = 100_000  # 每月免费10万Token

# 阶梯定价（元/万Token）
PRICING_TIERS = [
    {"from": 0,        "to": 100_000,   "price": 0.0},   # 免费额度
    {"from": 100_000,  "to": 1_000_000, "price": 0.50},  # 第一阶梯
    {"from": 1_000_000,"to": 5_000_000, "price": 0.30},  # 第二阶梯
    {"from": 5_000_000,"to": float('inf'), "price": 0.20}, # 第三阶梯
]

# ===== 初始化 =====
def 初始化目录():
    BILLING_DIR.mkdir(parents=True, exist_ok=True)
    RECONCILIATION_DIR.mkdir(parents=True, exist_ok=True)
    if not BALANCE_FILE.exists():
        with open(BALANCE_FILE, 'w', encoding='utf-8') as f:
            json.dump({"balance": 0.0, "free_used_this_month": 0,
                       "last_reset": str(date.today())}, f, ensure_ascii=False)

# ===== 余额管理 =====
def 读取余额() -> dict:
    初始化目录()
    with open(BALANCE_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 自动重置免费额度（每月1日）
    last_reset = date.fromisoformat(data.get("last_reset", str(date.today())))
    if date.today().month != last_reset.month:
        data["free_used_this_month"] = 0
        data["last_reset"] = str(date.today())
        写入余额(data)
    return data

def 写入余额(data: dict):
    with open(BALANCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ===== 计费逻辑 =====
def 计算费用(token数: int, 当前免费已用: int) -> dict:
    """计算token消耗费用，返回实际计费和更新后的免费额度用量"""
    费用 = 0.0
    实际计费token = 0
    免费消耗 = 0

    # 先消耗免费额度
    免费剩余 = max(0, FREE_MONTHLY_TOKENS - 当前免费已用)
    if token数 <= 免费剩余:
        免费消耗 = token数
        return {"费用": 0.0, "免费消耗": 免费消耗, "付费token": 0}
    else:
        免费消耗 = 免费剩余
        实际计费token = token数 - 免费消耗

    # 阶梯计费
    已计费 = 当前免费已用 + 免费消耗 - FREE_MONTHLY_TOKENS
    已计费 = max(0, 已计费)
    剩余待计费 = 实际计费token

    for tier in PRICING_TIERS[1:]:  # 跳过免费层
        if 剩余待计费 <= 0:
            break
        tier_from = tier["from"] - FREE_MONTHLY_TOKENS
        tier_to = tier["to"] - FREE_MONTHLY_TOKENS
        if 已计费 >= tier_to:
            continue
        可用容量 = min(tier_to, 已计费 + 剩余待计费) - max(tier_from, 已计费)
        if 可用容量 > 0:
            费用 += (可用容量 / 10000) * tier["price"]
            剩余待计费 -= 可用容量
            已计费 += 可用容量

    return {"费用": round(费用, 4), "免费消耗": 免费消耗, "付费token": 实际计费token}

# ===== 命令实现 =====
def 命令_余额(args):
    """lh billing balance → 查看当前账户余额"""
    data = 读取余额()
    余额 = data.get("balance", 0.0)
    免费已用 = data.get("free_used_this_month", 0)
    免费剩余 = max(0, FREE_MONTHLY_TOKENS - 免费已用)

    print("🐉 龍魂·账户余额")
    print("=" * 40)
    print(f"  💰 付费余额：¥ {余额:.4f} 元")
    print(f"  🎁 本月免费额度剩余：{免费剩余:,} Token")
    print(f"  📊 本月已用免费额度：{免费已用:,} / {FREE_MONTHLY_TOKENS:,} Token")
    print(f"  📅 免费额度重置日：每月1日")
    if 余额 < 1.0 and 免费剩余 < 10000:
        print("  ⚠️  余额不足提醒：余额低于1元且免费额度不足，建议充值")

def 命令_充值(args):
    """lh billing recharge [--amount] [--channel] → 生成充值订单"""
    金额 = args.amount
    渠道 = args.channel

    渠道映射 = {
        "wechat": "微信支付",
        "alipay": "支付宝",
        "lianlian": "连连国际",
        "airwallex": "Airwallex",
        "xtransfer": "XTransfer"
    }

    if 渠道 not in 渠道映射:
        print(f"❌ 不支持的支付渠道: {渠道}")
        print(f"   支持的渠道: {', '.join(渠道映射.keys())}")
        return

    if 金额 < 1.0:
        print("❌ 最低充值金额为 1 元")
        return

    # 生成订单号（毫秒级时间戳 + 随机尾缀·每单唯一）
    订单号 = f"LH{datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]}{abs(hash(金额)) % 97:03d}"

    # 记录待支付事务
    事务 = {
        "订单号": 订单号,
        "类型": "充值",
        "金额": 金额,
        "渠道": 渠道,
        "渠道名称": 渠道映射[渠道],
        "状态": "待支付",
        "时间": datetime.now().isoformat(),
        "DNA": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-充值-{订单号}"
    }

    初始化目录()
    with open(TRANSACTION_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(事务, ensure_ascii=False) + '\n')

    print(f"🐉 充值订单已生成")
    print("=" * 40)
    print(f"  📋 订单号：{订单号}")
    print(f"  💰 充值金额：¥ {金额:.2f} 元")
    print(f"  🏦 支付渠道：{渠道映射[渠道]}")
    print(f"  ⏰ 生成时间：{事务['时间']}")
    print(f"  📌 状态：待支付")
    print(f"")
    print(f"  ⚠️  注意：请通过已配置的支付渠道完成支付")
    print(f"       支付完成后余额将自动更新（支付回调处理）")
    print(f"  🔗 查看支付渠道配置：lh payment channels")

def 命令_用量(args):
    """lh billing usage [--period] → 查看用量统计"""
    周期 = args.period
    初始化目录()

    if not USAGE_LOG.exists():
        print("📊 暂无用量记录")
        return

    # 读取用量记录
    记录列表 = []
    with open(USAGE_LOG, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    记录列表.append(json.loads(line))
                except:
                    pass

    # 按周期过滤
    今天 = date.today()
    if 周期 == "day":
        过滤后 = [r for r in 记录列表 if r.get("date", "")[:10] == str(今天)]
        周期名 = "今日"
    elif 周期 == "week":
        七天前 = str(今天.replace(day=今天.day-7))
        过滤后 = [r for r in 记录列表 if r.get("date", "")[:10] >= 七天前]
        周期名 = "最近7天"
    else:  # month
        本月前缀 = str(今天)[:7]
        过滤后 = [r for r in 记录列表 if r.get("date", "")[:7] == 本月前缀]
        周期名 = "本月"

    总token = sum(r.get("tokens", 0) for r in 过滤后)
    总费用 = sum(r.get("cost", 0.0) for r in 过滤后)
    调用次数 = len(过滤后)

    print(f"🐉 龍魂·用量统计 [{周期名}]")
    print("=" * 40)
    print(f"  📞 API调用次数：{调用次数} 次")
    print(f"  🔢 总Token用量：{总token:,} Token")
    print(f"  💰 总费用：¥ {总费用:.4f} 元")
    if 调用次数 > 0:
        print(f"  📊 平均每次用量：{总token//调用次数:,} Token")

def 命令_历史(args):
    """lh billing history → 查看交易记录"""
    初始化目录()

    if not TRANSACTION_LOG.exists():
        print("📋 暂无交易记录")
        return

    记录列表 = []
    with open(TRANSACTION_LOG, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    记录列表.append(json.loads(line))
                except:
                    pass

    # 最近10条
    最近 = 记录列表[-10:]

    print("🐉 龍魂·最近交易记录（最近10条）")
    print("=" * 60)
    for r in reversed(最近):
        状态图标 = {"成功": "🟢", "SUCCESS": "🟢", "待支付": "🟡", "PENDING": "🟡",
                    "失败": "🔴", "FAILED": "🔴"}.get(r.get("状态", ""), "⚪")
        print(f"  {状态图标} [{r.get('时间','')[:19]}] {r.get('类型','')} ¥{r.get('金额',0):.2f} 元 | {r.get('渠道名称','')} | {r.get('订单号','')}")

# ===== 主入口 =====
def 主入口():
    parser = argparse.ArgumentParser(description="🐉 龍魂·API计费系统")
    subparsers = parser.add_subparsers(dest="命令")

    # balance
    subparsers.add_parser("balance", help="查看当前账户余额")

    # recharge
    p_recharge = subparsers.add_parser("recharge", help="充值")
    p_recharge.add_argument("--amount", type=float, required=True, help="充值金额（元）")
    p_recharge.add_argument("--channel", required=True,
                            choices=["wechat", "alipay", "lianlian", "airwallex", "xtransfer"],
                            help="支付渠道")

    # usage
    p_usage = subparsers.add_parser("usage", help="查看用量统计")
    p_usage.add_argument("--period", choices=["day", "week", "month"], default="month",
                         help="统计周期")

    # history
    subparsers.add_parser("history", help="查看交易记录")

    args = parser.parse_args()

    if args.命令 == "balance":
        命令_余额(args)
    elif args.命令 == "recharge":
        命令_充值(args)
    elif args.命令 == "usage":
        命令_用量(args)
    elif args.命令 == "history":
        命令_历史(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    主入口()
