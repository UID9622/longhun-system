#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️乙巳·癸未·丁亥·☷坤-PANGDONGLAI-SCHEDULER-v1.0-b7c3e8f2
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
"""
龍魂·胖东来分成审计自动调度器 v1.0

功能:
  - 每季度自动触发一次全量审计（季度末+15天宽限期）
  - 每次审计自动落档（无需手动 --save）
  - 事件触发：新企业签约后48h自动审计
  - 守护模式：常驻运行，定时巡检

用法:
  python3 bin/lh_pangdonglai_scheduler.py run           # 单次巡检
  python3 bin/lh_pangdonglai_scheduler.py daemon         # 守护模式（每小时巡检）
  python3 bin/lh_pangdonglai_scheduler.py trigger        # 立即全量触发审计
  python3 bin/lh_pangdonglai_scheduler.py status         # 查看调度状态
"""

import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CST = timezone(timedelta(hours=8))

# 路径
CONTRACT_DIR = PROJECT_ROOT / "01_protocols" / "contracts"
REGISTRY_FILE = CONTRACT_DIR / "enterprise_registry.json"
AUDIT_LOG_DIR = PROJECT_ROOT / "logs" / "pangdonglai_audit"
SCHEDULER_STATE = PROJECT_ROOT / "logs" / "pangdonglai_scheduler_state.json"

sys.path.insert(0, str(PROJECT_ROOT / "bin"))
from lh_pangdonglai_audit import PangDongLaiAuditor, FinancialData


def load_registry() -> Dict[str, Dict[str, Any]]:
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_registry(registry: Dict[str, Dict[str, Any]]):
    CONTRACT_DIR.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)


def load_scheduler_state() -> Dict[str, Any]:
    default = {"last_full_audit": None, "last_patrol": None, "audit_count": 0, "auto_saved_count": 0}
    if SCHEDULER_STATE.exists():
        with open(SCHEDULER_STATE, "r", encoding="utf-8") as f:
            return {**default, **json.load(f)}
    return default


def save_scheduler_state(state: Dict[str, Any]):
    SCHEDULER_STATE.parent.mkdir(parents=True, exist_ok=True)
    with open(SCHEDULER_STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def should_quarterly_audit(state: Dict[str, Any]) -> bool:
    """判断是否需要季度审计（季度末+15天宽限期）"""
    now = datetime.now(CST)
    quarter_end_months = {3, 6, 9, 12}
    if now.month not in quarter_end_months:
        return False
    if now.day < 15:
        return False
    last = state.get("last_full_audit")
    if last:
        last_q = datetime.fromisoformat(last)
        current_q = (now.year, (now.month - 1) // 3 + 1)
        last_q_tuple = (last_q.year, (last_q.month - 1) // 3 + 1)
        if current_q == last_q_tuple:
            return False
    return True


def should_auto_audit_new_enterprise(ent: Dict[str, Any]) -> bool:
    """新签约48h后自动触发审计"""
    if ent.get("last_audit_at"):
        return False
    signed_at = ent.get("signed_at", "")
    if not signed_at:
        return False
    try:
        signed_dt = datetime.fromisoformat(signed_at)
        elapsed = datetime.now(CST) - signed_dt
        return elapsed.total_seconds() > 48 * 3600
    except (ValueError, TypeError):
        return False


def run_patrol(force_all: bool = False) -> Dict[str, Any]:
    """单次巡检：检查注册企业，对符合条件的触发审计"""
    auditor = PangDongLaiAuditor()
    state = load_scheduler_state()
    registry = load_registry()

    now = datetime.now(CST)
    now_iso = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
    results = {"time": now_iso, "triggered": [], "skipped": [], "errors": []}

    # 判断是否触发季度全量
    do_quarterly = force_all or should_quarterly_audit(state)

    for code, ent in registry.items():
        if ent.get("status") != "active":
            results["skipped"].append(f"{code}: 非活跃状态")
            continue

        should_audit = False
        reason = ""

        if force_all or do_quarterly:
            should_audit = True
            reason = "季度全量审计"
        elif should_auto_audit_new_enterprise(ent):
            should_audit = True
            reason = "新签约·48h自动触发"

        if not should_audit:
            continue

        try:
            # 生成示例审计数据（实际应接入企业财报API）
            period = now.strftime("%Y-Q") + str((now.month - 1) // 3 + 1)
            data = FinancialData(
                N=0.0, R_e=0.0, R_f=0.0, R_i=0.0, R_p=0.0, R_b=0.0,
                enterprise_name=ent.get("enterprise_name", ""),
                uscc=ent.get("uscc", ""),
                period=period,
                employee_count=ent.get("employee_count", 10),
            )
            report = auditor.audit(data)

            # 自动落档（焊死·不可跳过）
            AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)
            report_file = AUDIT_LOG_DIR / f"{report.audit_id}.json"
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)

            # 更新企业注册表
            ent["last_audit_id"] = report.audit_id
            ent["last_audit_verdict"] = report.overall
            ent["last_audit_at"] = report.timestamp
            ent["audit_count"] = ent.get("audit_count", 0) + 1

            results["triggered"].append({
                "code": code,
                "name": ent.get("enterprise_name"),
                "reason": reason,
                "audit_id": report.audit_id,
                "verdict": report.overall,
            })

            state["audit_count"] = state.get("audit_count", 0) + 1
            state["auto_saved_count"] = state.get("auto_saved_count", 0) + 1

        except Exception as e:
            results["errors"].append(f"{code} ({ent.get('enterprise_name', '')}): {e}")

    # 保存
    if do_quarterly or force_all:
        state["last_full_audit"] = now_iso
    state["last_patrol"] = now_iso
    save_registry(registry)
    save_scheduler_state(state)

    return results


def run_single_audit(code: str) -> Optional[Dict]:
    """对单个企业执行审计（由API调用）"""
    auditor = PangDongLaiAuditor()
    registry = load_registry()

    ent = registry.get(code)
    if not ent:
        return None

    now = datetime.now(CST)
    period = now.strftime("%Y-Q") + str((now.month - 1) // 3 + 1)

    data = FinancialData(
        N=0.0, R_e=0.0, R_f=0.0, R_i=0.0, R_p=0.0, R_b=0.0,
        enterprise_name=ent.get("enterprise_name", ""),
        uscc=ent.get("uscc", ""),
        period=period,
    )
    report = auditor.audit(data)

    # 自动落档
    AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)
    report_file = AUDIT_LOG_DIR / f"{report.audit_id}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)

    ent["last_audit_id"] = report.audit_id
    ent["last_audit_verdict"] = report.overall
    ent["last_audit_at"] = report.timestamp
    ent["audit_count"] = ent.get("audit_count", 0) + 1
    save_registry(registry)

    return report.to_dict()


def daemon_mode():
    """守护模式：每小时巡检一次"""
    import signal

    print("""
╔══════════════════════════════════════════════════════╗
║  龍魂·胖东来分成审计调度器 v1.0 · 守护模式           ║
║  巡检间隔: 每小时                                     ║
║  季度全量: 季度末15日后自动触发                       ║
║  新签约48h: 自动审计                                  ║
║  审计落档: 焊死·不可跳过                              ║
╚══════════════════════════════════════════════════════╝
    """)

    shutdown = False

    def handle_signal(signum, frame):
        nonlocal shutdown
        print(f"\n🛑 收到信号 {signum}，安全退出...")
        shutdown = True

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    while not shutdown:
        try:
            print(f"\n⏰ 巡检 {datetime.now(CST).strftime('%Y-%m-%d %H:%M:%S')}")
            results = run_patrol()
            if results["triggered"]:
                for t in results["triggered"]:
                    print(f"  📋 审计触发: [{t['code']}] {t['name']} → {t['verdict']} ({t['reason']})")
            else:
                print("  ✅ 无待审计企业")
            if results["errors"]:
                for e in results["errors"]:
                    print(f"  🔴 错误: {e}")
        except Exception as e:
            print(f"  🔴 巡检异常: {e}")

        # 等待1小时
        for _ in range(360):  # 360 × 10s = 1h
            if shutdown:
                break
            time.sleep(10)

    print("守护模式已退出")


def print_status():
    """打印调度器状态"""
    state = load_scheduler_state()
    registry = load_registry()

    print(f"""
╔══════════════════════════════════════════════════════╗
║  龍魂·胖东来分成审计调度器 — 状态                     ║
╠══════════════════════════════════════════════════════╣
║  上次全量审计: {state.get('last_full_audit') or '从未'}
║  上次巡检:     {state.get('last_patrol') or '从未'}
║  累计审计次数: {state.get('audit_count', 0)}
║  自动落档次数: {state.get('auto_saved_count', 0)}
╠══════════════════════════════════════════════════════╣
║  注册企业总数: {len(registry)}
║  已审计: {sum(1 for e in registry.values() if e.get('last_audit_verdict'))}
║  未审计: {sum(1 for e in registry.values() if not e.get('last_audit_verdict') and e.get('status') == 'active')}
╚══════════════════════════════════════════════════════╝
""")

    if registry:
        print("企业明细:")
        for code, e in registry.items():
            v = e.get("last_audit_verdict", "未审计")
            t = e.get("last_audit_at", "-")
            print(f"  [{code}] {e.get('enterprise_name', '未命名'):15s} {v:4s}  {t}")
    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="龍魂·胖东来分成审计自动调度器 v1.0")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("run", help="单次巡检")
    sub.add_parser("daemon", help="守护模式（持续运行）")
    sub.add_parser("trigger", help="立即全量触发审计")
    sub.add_parser("status", help="查看调度状态")

    args = parser.parse_args()

    if args.command == "run":
        print("单次巡检...")
        results = run_patrol()
        print(json.dumps(results, ensure_ascii=False, indent=2))

    elif args.command == "daemon":
        daemon_mode()

    elif args.command == "trigger":
        print("强制全量审计...")
        results = run_patrol(force_all=True)
        print(json.dumps(results, ensure_ascii=False, indent=2))

    elif args.command == "status":
        print_status()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
