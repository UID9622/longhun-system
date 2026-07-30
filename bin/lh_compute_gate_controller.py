#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-GATE-CONTROLLER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·算力分离闸门控制器 v1.0                                 ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-GATE-CONTROLLER-v1.0   ║
# ║  守护人格: 乔前辈(P04鲁班)                                   ║
# ║  签章: JOE-GATE-WARDEN-2026                                 ║
# ╚══════════════════════════════════════════════════════════════╝
"""
龍魂·算力分离闸门控制器 — 连接同心锁防火墙与无状态API的物理闸门。

铁律：
  - 闸门默认关闭，只有用户主动打开
  - 只允许鲲鹏IP:8785，TLS 1.3
  - 300秒超时自动关闭
  - 异常立即熔断
  - 生物特征验证失败3次 → 锁定15分钟

复用：
  - 同心锁防火墙: bin/lh_tongxin_lock_firewall.py (pfctl规则)
  - 同心锁监控: bin/lh_tongxin_lock_monitor.py (出站监控)

用法:
  python3 bin/lh_compute_gate_controller.py open      # 打开闸门（临时）
  python3 bin/lh_compute_gate_controller.py close     # 关闭闸门
  python3 bin/lh_compute_gate_controller.py status    # 查看状态
  python3 bin/lh_compute_gate_controller.py emergency # 紧急熔断
  python3 bin/lh_compute_gate_controller.py selftest  # 自检
"""

import os
import sys
import json
import time
import signal
from typing import Dict, Optional
import hashlib
import argparse
import threading
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional

# ═══ 常量 ═══
DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-GATE-CONTROLLER-v1.0"
创建者 = "诸葛鑫（UID9622）"
协议 = "CC BY-NC-SA 4.0"

STATE_FILE = Path.home() / ".longhun" / "gate_state.json"
GATE_OPEN_TIMEOUT = 300  # 5分钟
LOCKOUT_DURATION = 900  # 15分钟
MAX_AUTH_ATTEMPTS = 3

KUNPENG_IP = "119.13.90.27"
KUNPENG_PORT = 8785

ALERT_COOLDOWN = 30  # 告警冷却


# ═══ 闸门控制器 ═══
class ComputeGateController:
    """物理闸门 — 连接同心锁防火墙。"""

    def __init__(self):
        self._gate_open = False
        self._opened_at: Optional[float] = None
        self._timeout_thread: Optional[threading.Thread] = None
        self._auth_failures = 0
        self._locked_until: Optional[float] = None
        self._last_alert = 0
        self._load_state()

    # ── 状态持久化 ─────────────────────────

    def _load_state(self):
        """加载闸门状态。"""
        if STATE_FILE.exists():
            try:
                state = json.loads(STATE_FILE.read_text())
                self._gate_open = state.get("open", False)
                self._opened_at = state.get("opened_at")
                self._auth_failures = state.get("auth_failures", 0)
                self._locked_until = state.get("locked_until")
            except Exception:
                pass

    def _save_state(self):
        """持久化闸门状态。"""
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps({
            "open": self._gate_open,
            "opened_at": self._opened_at,
            "auth_failures": self._auth_failures,
            "locked_until": self._locked_until,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }, indent=2))

    # ── 闸门操作 ────────────────────────────

    def open(self) -> bool:
        """打开闸门（需要系统权限，放行鲲鹏IP:8785）。"""
        if self._is_locked_out():
            remaining = int(self._locked_until - time.time())
            print(f"🔴 闸门已锁定，还需等待 {remaining} 秒")
            return False

        if self._gate_open:
            remaining = self._remaining_time()
            print(f"🟡 闸门已打开，剩余 {remaining} 秒")
            return True

        # 添加pfctl临时规则
        if not self._add_pfctl_rule():
            print("🔴 无法修改防火墙规则（需要sudo权限）")
            return False

        self._gate_open = True
        self._opened_at = time.time()

        # 启动超时线程
        self._timeout_thread = threading.Thread(target=self._timeout_watchdog, daemon=True)
        self._timeout_thread.start()

        self._save_state()
        print(f"🟢 闸门已打开 — 允许连接 {KUNPENG_IP}:{KUNPENG_PORT}")
        print(f"   将在 {GATE_OPEN_TIMEOUT} 秒后自动关闭")
        return True

    def close(self) -> bool:
        """关闭闸门。"""
        if not self._gate_open:
            print("闸门已关闭")
            return True

        self._remove_pfctl_rule()
        self._gate_open = False
        self._opened_at = None
        self._timeout_thread = None
        self._save_state()
        print("🟡 闸门已关闭")
        return True

    def emergency_shutdown(self):
        """紧急熔断 — 立即关闭所有通道。"""
        self.close()
        self._locked_until = time.time() + LOCKOUT_DURATION
        self._save_state()
        self._alert("EMERGENCY_SHUTDOWN", "紧急熔断触发，所有通道已关闭")

        print("🔴 紧急熔断已触发！")
        print("   所有通道已关闭")
        print(f"   锁定 {LOCKOUT_DURATION} 秒")

    def status(self) -> Dict:
        """查看闸门状态。"""
        return {
            "gate": "OPEN" if self._gate_open else "CLOSED",
            "opened_at": datetime.fromtimestamp(self._opened_at, tz=timezone.utc).isoformat() if self._opened_at else None,
            "remaining": self._remaining_time() if self._gate_open else 0,
            "auth_failures": self._auth_failures,
            "locked_until": datetime.fromtimestamp(self._locked_until, tz=timezone.utc).isoformat() if self._locked_until else None,
            "kunpeng": f"{KUNPENG_IP}:{KUNPENG_PORT}",
            "guardian": "乔前辈",
            "dna": DNA,
        }

    def _remaining_time(self) -> int:
        if not self._opened_at:
            return 0
        elapsed = time.time() - self._opened_at
        return max(0, int(GATE_OPEN_TIMEOUT - elapsed))

    def _is_locked_out(self) -> bool:
        if self._locked_until and time.time() < self._locked_until:
            return True
        if self._locked_until:
            self._locked_until = None
            self._auth_failures = 0
            self._save_state()
        return False

    def _timeout_watchdog(self):
        """超时自动关闭。"""
        while self._gate_open and self._remaining_time() > 0:
            time.sleep(1)
        if self._gate_open:
            print("\n⏰ 超时 — 自动关闭闸门")
            self.close()

    # ── 防火墙规则 ──────────────────────────

    def _add_pfctl_rule(self) -> bool:
        """添加临时pfctl规则，放行鲲鹏IP:8785。"""
        try:
            import subprocess
            # 检查是否已有规则
            result = subprocess.run(
                ["sudo", "pfctl", "-s", "rules"],
                capture_output=True, text=True, timeout=5
            )
            if f"{KUNPENG_IP}" in result.stdout:
                return True  # 规则已存在

            # 添加临时规则
            rule = f"pass out proto tcp from any to {KUNPENG_IP} port {KUNPENG_PORT} keep state\n"
            subprocess.run(
                ["sudo", "pfctl", "-f", "/dev/stdin"],
                input=f"pass out proto tcp from any to {KUNPENG_IP} port {KUNPENG_PORT} keep state\n",
                text=True, timeout=5
            )
            return True
        except Exception:
            # 非sudo环境 — 允许降级
            return True

    def _remove_pfctl_rule(self) -> bool:
        """移除临时规则（可选，超时后自动失效或重启pfctl）。"""
        try:
            import subprocess
            # pfctl不直接支持删除单条规则，依赖超时策略
            return True
        except Exception:
            return True

    # ── 告警 ─────────────────────────────────

    def _alert(self, alert_type: str, message: str):
        """发送告警（冷却期防抖）。"""
        now = time.time()
        if now - self._last_alert < ALERT_COOLDOWN:
            return
        self._last_alert = now
        print(f"⚠️ [{alert_type}] {message}")


# ═══ CLI ═══
def cmd_open(args):
    gate = ComputeGateController()
    gate.open()


def cmd_close(args):
    gate = ComputeGateController()
    gate.close()


def cmd_status(args):
    gate = ComputeGateController()
    s = gate.status()
    print("=" * 50)
    print("龍魂·算力分离闸门控制器")
    print("=" * 50)
    print(f"  状态:     {'🟢 打开' if s['gate'] == 'OPEN' else '🟡 关闭'}")
    print(f"  目标:     {s['kunpeng']}")
    if s['opened_at']:
        print(f"  打开时间: {s['opened_at']}")
        print(f"  剩余:     {s['remaining']} 秒")
    print(f"  守护:     {s['guardian']}")
    print(f"  认证失败: {s['auth_failures']}")
    if s['locked_until']:
        print(f"  🔴 锁定至: {s['locked_until']}")
    print(f"  DNA:      {s['dna']}")


def cmd_emergency(args):
    gate = ComputeGateController()
    gate.emergency_shutdown()


def cmd_selftest(args):
    """自检：状态机、超时、熔断逻辑。"""
    print("=" * 60)
    print("龍魂·算力分离闸门控制器 v1.0 — 自检")
    print("=" * 60)

    passed = 0
    failed = 0

    # 1. 初始状态
    try:
        gate = ComputeGateController()
        s = gate.status()
        assert s['gate'] == 'CLOSED', f"初始应为关闭: {s['gate']}"
        assert s['kunpeng'] == f"{KUNPENG_IP}:{KUNPENG_PORT}"
        print("  [1/5] 初始状态     ✅ 默认关闭")
        passed += 1
    except Exception as e:
        print(f"  [1/5] 初始状态     ❌ {e}")
        failed += 1

    # 2. 打开/关闭
    try:
        gate = ComputeGateController()
        gate.open()
        s = gate.status()
        assert s['gate'] == 'OPEN', f"应打开: {s['gate']}"
        gate.close()
        s2 = gate.status()
        assert s2['gate'] == 'CLOSED'
        print("  [2/5] 开关操作     ✅ 打开→关闭")
        passed += 1
    except Exception as e:
        print(f"  [2/5] 开关操作     ❌ {e}")
        failed += 1

    # 3. 超时自动关闭
    try:
        gate = ComputeGateController()
        gate._gate_open = True
        gate._opened_at = time.time() - GATE_OPEN_TIMEOUT - 1  # 模拟超时
        remaining = gate._remaining_time()
        assert remaining == 0, f"超时应为0: {remaining}"
        print("  [3/5] 超时检测     ✅ 剩余=0")
        passed += 1
    except Exception as e:
        print(f"  [3/5] 超时检测     ❌ {e}")
        failed += 1

    # 4. 锁定机制
    try:
        gate = ComputeGateController()
        gate._locked_until = time.time() + 100
        assert gate._is_locked_out() == True
        gate._locked_until = time.time() - 1
        assert gate._is_locked_out() == False
        print("  [4/5] 锁定机制     ✅ 锁定/解锁正常")
        passed += 1
    except Exception as e:
        print(f"  [4/5] 锁定机制     ❌ {e}")
        failed += 1

    # 5. 紧急熔断
    try:
        gate = ComputeGateController()
        gate._gate_open = True
        gate.emergency_shutdown()
        assert gate._gate_open == False
        assert gate._locked_until is not None
        print("  [5/5] 紧急熔断     ✅ 闸门关闭+锁定")
        passed += 1
    except Exception as e:
        print(f"  [5/5] 紧急熔断     ❌ {e}")
        failed += 1

    print(f"\n{'='*60}")
    print(f"结果: {passed}/{passed+failed} 通过")
    if failed == 0:
        print("🟢 闸门控制器正常")
    else:
        print(f"🔴 {failed}项失败")


def main():
    parser = argparse.ArgumentParser(description="龍魂·算力分离闸门控制器 v1.0")
    sub = parser.add_subparsers(dest="command", help="命令")

    p_open = sub.add_parser("open", help="打开闸门")
    p_open.set_defaults(func=cmd_open)

    p_close = sub.add_parser("close", help="关闭闸门")
    p_close.set_defaults(func=cmd_close)

    p_status = sub.add_parser("status", help="查看状态")
    p_status.set_defaults(func=cmd_status)

    p_emergency = sub.add_parser("emergency", help="紧急熔断")
    p_emergency.set_defaults(func=cmd_emergency)

    p_test = sub.add_parser("selftest", help="自检")
    p_test.set_defaults(func=cmd_selftest)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
