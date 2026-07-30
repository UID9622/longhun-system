#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·午时·IMMUTABLE-HISTORY-DAEMON-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║     🛡️ 龍魂·不可篡改历史守护进程 v1.0                                     ║
║     Immutable History Watchdog — 定时巡检 · 篡改即告警 · 篡改即留痕        ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·乙未·丁酉·午时·IMMUTABLE-HISTORY-DAEMON-v1.0          ║
║  哲学: 历史可以被追加 · 但永远不会被静默修改                                ║
║  铁律:                                                                   ║
║    定时校验 — 每 N 分钟自动验证哈希链与 payload 完整性                       ║
║    篡改即告警 — 发现异常立即 Bark / 日志 / 审计记录                          ║
║    篡改即留痕 — 把“发现篡改”这件事本身也追加为不可篡改记录                    ║
║    本地优先 — 不依赖云端，单机即可运行                                       ║
╚══════════════════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_immutable_history_daemon.py              # 单次巡检
  python3 bin/lh_immutable_history_daemon.py --daemon     # 守护模式(默认每10分钟)
  python3 bin/lh_immutable_history_daemon.py --interval 60 # 每60分钟
  python3 bin/lh_immutable_history_daemon.py --status     # 查看最新状态

退出码:
  0 — 巡检通过或守护正常启动
  1 — 发现篡改或参数错误
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
ENGINE = ROOT / "bin" / "lh_immutable_history.py"

# 动态导入引擎模块，复用 provenance 与威胁行为体追踪
_engine_spec = importlib.util.spec_from_file_location("lh_immutable_history", ENGINE)
_engine_module = importlib.util.module_from_spec(_engine_spec)
_engine_spec.loader.exec_module(_engine_module)
collect_local_provenance = _engine_module.collect_local_provenance

STATE_DIR = Path.home() / ".longhun" / "ledger"
STATE_DIR.mkdir(parents=True, exist_ok=True)

WATCHDOG_LOG = STATE_DIR / "immutable_history_watchdog.jsonl"
WATCHDOG_STATE = STATE_DIR / "immutable_history_watchdog_state.json"

DNA = "#龍芯⚡️丙午·乙未·丁酉·午时·IMMUTABLE-HISTORY-DAEMON-v1.0"

# 默认巡检间隔：10 分钟
DEFAULT_INTERVAL_SEC = 600


@dataclass
class WatchdogReport:
    """单次巡检报告"""
    timestamp: str
    ledger_file: str
    total_records: int
    integrity_valid: bool
    issues: List[str]
    elapsed_ms: float
    dna: str
    status: str  # GREEN / YELLOW / RED


class ImmutableHistoryWatchdog:
    """不可篡改历史守护进程"""

    def __init__(self):
        self.bark_key = self._load_bark_key()
        self.state = self._load_state()

    def _load_bark_key(self) -> str:
        bark_path = Path.home() / ".longhun" / "bark_key.txt"
        if bark_path.exists():
            return bark_path.read_text().strip()
        return ""

    def _load_state(self) -> Dict[str, Any]:
        if WATCHDOG_STATE.exists():
            return json.loads(WATCHDOG_STATE.read_text())
        return {
            "last_check": None,
            "consecutive_failures": 0,
            "total_checks": 0,
            "tamper_events": 0,
            "dna": DNA,
        }

    def _save_state(self):
        WATCHDOG_STATE.write_text(
            json.dumps(self.state, ensure_ascii=False, indent=2)
        )

    def _log(self, entry: Dict[str, Any]):
        entry["ts"] = datetime.now().isoformat()
        with open(WATCHDOG_LOG, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _record_tamper_event(self, report: WatchdogReport):
        """
        把“发现篡改”本身追加为不可篡改记录，并捕获现场指纹。
        这符合宪法 6.2 与创作者保护协议：任何对历史的攻击行为都必须被记录。
        """
        try:
            provenance = collect_local_provenance()
            payload = {
                "event": "tamper_detected",
                "ledger_file": report.ledger_file,
                "total_records": report.total_records,
                "issues": report.issues,
                "watchdog_dna": report.dna,
            }
            subprocess.run(
                [
                    sys.executable, str(ENGINE),
                    "--record", "tamper_detected",
                    "--payload", json.dumps(payload, ensure_ascii=False),
                    "--source", "audit",
                    "--actor", "lh_immutable_history_daemon",
                    "--sign",
                    "--ip", provenance.get("ip", ""),
                    "--device-fingerprint", provenance.get("device_fingerprint", ""),
                    "--hostname", provenance.get("hostname", ""),
                    "--user-agent", "lh_immutable_history_daemon/1.0",
                ],
                capture_output=True,
                timeout=30,
                check=False,
            )
        except Exception as e:
            # 如果追加失败，至少写到 watchdog log
            self._log({
                "level": "ERROR",
                "message": f"无法追加篡改事件到主账本: {e}",
                "issues": report.issues,
            })

    def _send_alert(self, report: WatchdogReport):
        """发送告警：终端 + Bark"""
        print("\n" + "=" * 60)
        print(f"  🔴 龍魂不可篡改历史 — 篡改告警")
        print(f"  时间: {report.timestamp[:19]}")
        print(f"  账本: {report.ledger_file}")
        print(f"  记录数: {report.total_records}")
        print("-" * 60)
        for issue in report.issues:
            print(f"  {issue}")
        print("=" * 60 + "\n")

        if self.bark_key:
            try:
                import urllib.request
                title = "龍魂历史篡改告警"
                body = f"账本 {report.total_records} 条记录异常 | " + " | ".join(report.issues[:2])
                url = f"https://api.day.app/{self.bark_key}/{title}/{body}?level=active"
                urllib.request.urlopen(url, timeout=5)
                print("📱 Bark 篡改告警已发送")
            except Exception as e:
                print(f"⚠️ Bark 推送失败: {e}")

    def check(self) -> WatchdogReport:
        """执行一次完整性巡检"""
        start = datetime.now()

        # 调用引擎 --report
        proc = subprocess.run(
            [sys.executable, str(ENGINE), "--report"],
            capture_output=True,
            text=True,
            timeout=60,
        )

        elapsed_ms = (datetime.now() - start).total_seconds() * 1000

        if proc.returncode != 0 and not proc.stdout.strip():
            # 引擎异常
            report = WatchdogReport(
                timestamp=datetime.now().isoformat(),
                ledger_file=str(STATE_DIR / "immutable_history.jsonl"),
                total_records=-1,
                integrity_valid=False,
                issues=[f"引擎异常: {proc.stderr or 'unknown error'}"],
                elapsed_ms=elapsed_ms,
                dna=DNA,
                status="RED",
            )
        else:
            try:
                engine_report = json.loads(proc.stdout)
            except json.JSONDecodeError:
                engine_report = {
                    "ledger_file": str(STATE_DIR / "immutable_history.jsonl"),
                    "total_records": -1,
                    "integrity_valid": False,
                    "issues": [f"引擎输出无法解析: {proc.stdout[:200]}"],
                }

            is_valid = engine_report.get("integrity_valid", False)
            report = WatchdogReport(
                timestamp=engine_report.get("timestamp", datetime.now().isoformat()),
                ledger_file=engine_report.get("ledger_file", ""),
                total_records=engine_report.get("total_records", 0),
                integrity_valid=is_valid,
                issues=engine_report.get("issues", []),
                elapsed_ms=elapsed_ms,
                dna=DNA,
                status="GREEN" if is_valid else "RED",
            )

        # 更新状态
        self.state["total_checks"] = self.state.get("total_checks", 0) + 1
        self.state["last_check"] = report.timestamp
        if report.integrity_valid:
            self.state["consecutive_failures"] = 0
        else:
            self.state["consecutive_failures"] = self.state.get("consecutive_failures", 0) + 1
            self.state["tamper_events"] = self.state.get("tamper_events", 0) + 1
            self._record_tamper_event(report)
            self._send_alert(report)

        self._save_state()
        self._log({
            "event": "watchdog_check",
            "integrity_valid": report.integrity_valid,
            "total_records": report.total_records,
            "elapsed_ms": report.elapsed_ms,
            "status": report.status,
            "issues": report.issues,
        })

        return report

    def print_status(self):
        """打印当前守护状态"""
        print("=" * 60)
        print("🛡️ 龍魂不可篡改历史守护状态")
        print("=" * 60)
        print(f"DNA: {DNA}")
        print(f"总巡检次数: {self.state.get('total_checks', 0)}")
        print(f"篡改事件数: {self.state.get('tamper_events', 0)}")
        print(f"连续失败次数: {self.state.get('consecutive_failures', 0)}")
        print(f"最后巡检: {self.state.get('last_check', '从未')}")
        print("=" * 60)

    def run_daemon(self, interval_sec: int = DEFAULT_INTERVAL_SEC):
        """守护模式"""
        print("🛡️ 龍魂不可篡改历史守护启动")
        print(f"   DNA: {DNA}")
        print(f"   巡检间隔: {interval_sec} 秒")
        print(f"   引擎: {ENGINE}\n")

        try:
            while True:
                ts = datetime.now().strftime("%H:%M:%S")
                print(f"[{ts}] 巡检不可篡改历史...", end=" ", flush=True)

                report = self.check()
                status_icon = "🟢" if report.integrity_valid else "🔴"
                print(
                    f"{status_icon} {report.total_records} 条 | "
                    f"{report.elapsed_ms:.1f} ms | "
                    f"状态: {report.status}"
                )

                time.sleep(interval_sec)
        except KeyboardInterrupt:
            print("\n🛑 不可篡改历史守护已停止")


def main():
    parser = argparse.ArgumentParser(description="龍魂不可篡改历史守护进程")
    parser.add_argument("--daemon", action="store_true", help="守护模式持续巡检")
    parser.add_argument(
        "--interval", type=int, default=DEFAULT_INTERVAL_SEC,
        help=f"巡检间隔秒数（默认 {DEFAULT_INTERVAL_SEC}）"
    )
    parser.add_argument("--status", action="store_true", help="查看守护状态")
    args = parser.parse_args()

    watchdog = ImmutableHistoryWatchdog()

    if args.status:
        watchdog.print_status()
        return

    if args.daemon:
        watchdog.run_daemon(args.interval)
        return

    # 单次巡检
    report = watchdog.check()
    if report.integrity_valid:
        print("🟢 历史账本完整")
        print(f"   账本: {report.ledger_file}")
        print(f"   记录: {report.total_records} 条")
        print(f"   耗时: {report.elapsed_ms:.1f} ms")
        sys.exit(0)
    else:
        print("🔴 历史账本异常")
        for issue in report.issues:
            print(f"   {issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
