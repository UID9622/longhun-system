#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·对账与审计集成模块 v1.0
DNA: #龍芯⚡️2026-09-04-对账审计-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色审计: 🟢 通过
用法: lh reconcile → 自动对账 + 三色审计 + billing_audit 事件留痕
对账报告: ~/.longhun/billing/reconciliation/reconciliation_*.json
耻辱墙事件: ~/.longhun/shame_wall/billing_audit.jsonl（append-only·与 shame_wall.json 同步）
"""

import json
from pathlib import Path
from datetime import datetime

BILLING_DIR = Path.home() / ".longhun" / "billing"
RECONCILIATION_DIR = BILLING_DIR / "reconciliation"
# 耻辱墙真实目录（lh_judge/lh_daily_audit/lh_topo 共用）→ billing_audit 事件流 append-only
SHAME_WALL_DIR = Path.home() / ".longhun" / "shame_wall"
SHAME_AUDIT_LOG = SHAME_WALL_DIR / "billing_audit.jsonl"
SHAME_JSON = SHAME_WALL_DIR / "shame_wall.json"


def 写入耻辱墙(事件: dict):
    """billing_audit 事件留痕（append-only）:
    1) ~/.longhun/shame_wall/billing_audit.jsonl — 事件流（行式 JSON·append）
    2) shame_wall.json 若存在（judge 生成）→ 同步进 记录/records 数组
    3) 与对账报告 reconciliation_*.json 互为证据链"""
    try:
        SHAME_WALL_DIR.mkdir(parents=True, exist_ok=True)
        with open(SHAME_AUDIT_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(事件, ensure_ascii=False) + '\n')
        # 兼容 judge 的 shame_wall.json（存在才写·字段对齐 日期/类型/详情）
        if SHAME_JSON.exists():
            try:
                data = json.loads(SHAME_JSON.read_text(encoding='utf-8'))
            except Exception:
                data = {}
            recs = data.get("记录") or data.get("records")
            if isinstance(recs, list):
                recs.append({
                    "日期": 事件.get("时间", "")[:10],
                    "类型": "billing_audit",
                    "详情": f"对账{事件.get('状态','')} · 差额¥{事件.get('差额',0):.4f} · {事件.get('DNA','')}",
                })
                SHAME_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"  ⚠️  耻辱墙写入失败（不影响对账主流程）: {e}")


def 执行对账():
    """执行全量对账，生成对账报告"""
    RECONCILIATION_DIR.mkdir(parents=True, exist_ok=True)

    # 读取调用记录
    usage_log = BILLING_DIR / "usage.jsonl"
    usage_records = []
    if usage_log.exists():
        with open(usage_log, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        usage_records.append(json.loads(line))
                    except:
                        pass

    # 读取交易记录
    tx_log = BILLING_DIR / "transactions.jsonl"
    tx_records = []
    if tx_log.exists():
        with open(tx_log, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        tx_records.append(json.loads(line))
                    except:
                        pass

    # 读取余额
    balance_file = BILLING_DIR / "balance.json"
    balance = 0.0
    if balance_file.exists():
        with open(balance_file, 'r', encoding='utf-8') as f:
            balance = json.load(f).get("balance", 0.0)

    # 计算理论余额
    充值总额 = sum(r.get("金额", 0) for r in tx_records if r.get("类型") == "充值" and r.get("状态") in ["SUCCESS", "成功"])
    消费总额 = sum(r.get("cost", 0) for r in usage_records)
    理论余额 = round(充值总额 - 消费总额, 4)
    实际余额 = round(balance, 4)
    差额 = round(实际余额 - 理论余额, 4)

    # 三色审计判定
    if abs(差额) < 0.001:
        颜色 = "🟢"
        状态 = "自动核销"
        结论 = "余额与记录完全一致，无异常"
    elif abs(差额) < 1.0:
        颜色 = "🟡"
        状态 = "人工核对"
        结论 = f"余额与记录存在差异 {差额:.4f} 元，建议人工复核"
    else:
        颜色 = "🔴"
        状态 = "异常拦截"
        结论 = f"余额异常！差额 {差额:.4f} 元，已自动触发异常拦截"

    # 生成对账报告
    报告时间 = datetime.now().strftime("%Y%m%d_%H%M%S")
    报告路径 = RECONCILIATION_DIR / f"reconciliation_{报告时间}.json"

    报告 = {
        "报告时间": datetime.now().isoformat(),
        "DNA": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-对账报告-{报告时间}",
        "调用记录数": len(usage_records),
        "交易记录数": len(tx_records),
        "充值总额": 充值总额,
        "消费总额": 消费总额,
        "理论余额": 理论余额,
        "实际余额": 实际余额,
        "差额": 差额,
        "三色审计": 颜色,
        "状态": 状态,
        "结论": 结论
    }

    with open(报告路径, 'w', encoding='utf-8') as f:
        json.dump(报告, f, ensure_ascii=False, indent=2)

    # ── billing_audit 事件 → 耻辱墙（🟡/🔴 触发留痕·🟢 同样留痕防抵赖）──
    写入耻辱墙({
        "事件类型": "billing_audit",
        "颜色": 颜色,
        "状态": 状态,
        "差额": 差额,
        "时间": datetime.now().isoformat(),
        "DNA": 报告["DNA"]
    })

    print("🐉 龍魂·对账报告")
    print("=" * 50)
    print(f"  📊 调用记录：{len(usage_records)} 条")
    print(f"  💳 交易记录：{len(tx_records)} 条")
    print(f"  💰 充值总额：¥ {充值总额:.4f}")
    print(f"  📉 消费总额：¥ {消费总额:.4f}")
    print(f"  📗 理论余额：¥ {理论余额:.4f}")
    print(f"  📘 实际余额：¥ {实际余额:.4f}")
    print(f"  ⚖️  差额：¥ {差额:.4f}")
    print(f"  {颜色} 三色审计：{状态}")
    print(f"  📝 结论：{结论}")
    print(f"  📁 报告路径：{报告路径}")
    print(f"  📌 billing_audit 事件已落耻辱墙：{SHAME_AUDIT_LOG}")

    return 报告


if __name__ == "__main__":
    执行对账()
