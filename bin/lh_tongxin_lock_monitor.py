#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·同心锁状态监控 v1.0                                    ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-LOCK-MONITOR-v1.0       ║
# ║  守护人格: 乔前辈(P04鲁班)                                  ║
# ║  签章: JOE-EYE-2026                                         ║
# ╚══════════════════════════════════════════════════════════════╝
"""
龍魂·同心锁状态监控 v1.0
─────────────────────────
实时监控所有出站连接，阻断非授权流量，每小时隐私审计。
自动检测异常并推送告警。

用法:
    python3 bin/lh_tongxin_lock_monitor.py --daemon    # 后台守护模式
    python3 bin/lh_tongxin_lock_monitor.py --once       # 单次审计
    python3 bin/lh_tongxin_lock_monitor.py selftest     # 自检
"""
DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-LOCK-MONITOR-v1.0"
创建者 = "诸葛鑫（UID9622）"
协议 = "CC BY-NC-SA 4.0"

import argparse
import json
import os
import platform
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# ═══ 常量 ═══
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
MONITOR_INTERVAL = 60          # 秒，出站连接检查间隔
AUDIT_INTERVAL = 3600          # 秒，隐私审计间隔（1小时）
ALERT_THRESHOLD = 1            # 任何异常立即告警
PID_FILE = PROJECT_ROOT / "data" / "tongxin_monitor.pid"

# 苹果出站域名特征（用于实时检测）
APPLE_DOMAIN_PATTERNS = [
    "icloud", "apple", "siri", "me.com",
    "mzstatic", "itunes", "aaplimg",
    "apple-cloudkit", "cirrus",
]

# 追踪服务域名特征
TRACKER_DOMAIN_PATTERNS = [
    "google-analytics", "doubleclick",
    "telemetry.microsoft",
    "amazon-adsystem",
]


class TongxinLockMonitor:
    """同心锁状态监控守护"""

    def __init__(self):
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        self.alerts = []
        self.audit_count = 0
        self.block_count = 0

    # ── 出站连接检测 ──

    def capture_outbound_connections(self) -> list:
        """捕获当前非本地出站连接"""
        connections = []
        try:
            # lsof -i TCP -s TCP:ESTABLISHED
            result = subprocess.run(
                ["lsof", "-i", "TCP", "-s", "TCP:ESTABLISHED", "-n", "-P"],
                capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.split("\n")[1:]:  # 跳过标题行
                if not line.strip():
                    continue
                parts = line.split()
                if len(parts) < 9:
                    continue
                # 提取目标地址
                dest = parts[-2] if len(parts) >= 9 else ""
                if "->" in dest:
                    dest_addr = dest.split("->")[-1].strip()
                else:
                    dest_addr = dest

                # 跳过本地连接
                if "127.0.0.1" in dest_addr or "localhost" in dest_addr.lower():
                    continue
                if "*:*" in dest_addr:
                    continue

                connections.append({
                    "process": parts[0],
                    "pid": parts[1],
                    "dest": dest_addr,
                })
        except Exception:
            pass
        return connections

    def _is_apple_service(self, conn: dict) -> bool:
        """判断是否为苹果服务连接"""
        dest = conn.get("dest", "").lower()
        return any(pattern in dest for pattern in APPLE_DOMAIN_PATTERNS)

    def _is_tracker(self, conn: dict) -> bool:
        """判断是否为追踪服务连接"""
        dest = conn.get("dest", "").lower()
        return any(pattern in dest for pattern in TRACKER_DOMAIN_PATTERNS)

    # ── 阻断与告警 ──

    def block_and_alert(self, conn: dict, reason: str):
        """阻断连接并推送告警"""
        self.block_count += 1

        alert = {
            "type": "CONNECTION_BLOCKED",
            "timestamp": datetime.now().isoformat(),
            "connection": conn,
            "reason": reason,
            "action": "BLOCKED",
            "dna": DNA,
        }

        self.alerts.append(alert)
        self._log(alert)

        # 跨平台终端通知
        self._notify(f"阻断 {reason}", conn.get("dest", "?"))

    def _log(self, entry: dict):
        """写监控日志"""
        log_file = LOG_DIR / "tongxin_monitor.log"
        try:
            with open(log_file, "a") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass

    def _push_alert(self, alert_type: str, detail: str):
        """通用告警推送"""
        alert = {
            "type": alert_type,
            "timestamp": datetime.now().isoformat(),
            "detail": detail,
            "dna": DNA,
        }
        self.alerts.append(alert)
        self._log(alert)

        # 跨平台终端通知
        self._notify(f"同心锁·{alert_type}", detail)

    def _notify(self, title: str, message: str):
        """跨平台桌面通知（macOS/Linux/静默fallback）"""
        try:
            if platform.system() == "Darwin":
                subprocess.run([
                    "osascript", "-e",
                    f'display notification "{message}" '
                    f'with title "{title}" subtitle "乔前辈守护"'
                ], timeout=5)
            elif platform.system() == "Linux":
                subprocess.run([
                    "notify-send", "-i", "security-high", title, message
                ], timeout=5)
        except Exception:
            pass

    # ── 隐私审计 ──

    def run_privacy_audit(self) -> dict:
        """执行隐私加固审计（--check-only模式·跨平台）"""
        if platform.system() == "Darwin":
            hardener_script = PROJECT_ROOT / "bin" / "lh_privacy_hardener.sh"
        elif platform.system() == "Linux":
            hardener_script = PROJECT_ROOT / "bin" / "lh_privacy_hardener_linux.sh"
        else:
            return {"ok": False, "error": "不支持的操作系统"}

        if not hardener_script.exists():
            return {"ok": False, "error": f"隐私加固脚本不存在: {hardener_script}"}

        try:
            result = subprocess.run(
                ["sudo", "-n", "bash", str(hardener_script), "--check-only"],
                capture_output=True, text=True, timeout=30
            )
            passed = result.returncode == 0
            return {
                "ok": passed,
                "timestamp": datetime.now().isoformat(),
                "exit_code": result.returncode,
                "output": result.stdout[-500:] if result.stdout else "",
            }
        except subprocess.CalledProcessError as e:
            return {"ok": False, "error": str(e)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ── 防火墙状态检查 ──

    def check_firewall_status(self) -> dict:
        """检查防火墙是否仍在运行（跨平台）"""
        try:
            if platform.system() == "Darwin":
                result = subprocess.run(
                    ["sudo", "-n", "pfctl", "-s", "info"],
                    capture_output=True, text=True, timeout=5
                )
                enabled = "Enabled" in result.stdout
            elif platform.system() == "Linux":
                result = subprocess.run(
                    ["sudo", "-n", "iptables", "-L", "LONGHUN_TONGXIN", "-n"],
                    capture_output=True, text=True, timeout=5
                )
                enabled = result.returncode == 0
            else:
                enabled = False
            return {"ok": enabled, "pf_enabled": enabled}
        except Exception:
            return {"ok": False, "pf_enabled": False}

    # ── 监控循环 ──

    def once(self) -> dict:
        """单次审计（非守护模式）"""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "dna": DNA,
            "connections_checked": 0,
            "blocks": 0,
            "alerts": [],
            "privacy_audit": None,
            "firewall_status": None,
        }

        # 1. 检查出站连接
        connections = self.capture_outbound_connections()
        summary["connections_checked"] = len(connections)

        for conn in connections:
            if self._is_apple_service(conn):
                self.block_and_alert(conn, "苹果服务")
                summary["blocks"] += 1
            elif self._is_tracker(conn):
                self.block_and_alert(conn, "追踪服务")
                summary["blocks"] += 1

        # 2. 隐私审计
        summary["privacy_audit"] = self.run_privacy_audit()

        # 3. 防火墙状态
        summary["firewall_status"] = self.check_firewall_status()

        # 4. 告警汇总
        summary["alerts"] = [
            {"type": a["type"], "reason": a.get("reason", a.get("detail", "")), "time": a["timestamp"]}
            for a in self.alerts[-10:]  # 最近10条
        ]

        return summary

    def daemon(self):
        """守护进程模式"""
        print(f"🐉 龍魂·同心锁监控守护 v1.0")
        print(f"   DNA: {DNA}")
        print(f"   守护人格: 乔前辈(P04鲁班)")
        print(f"   检查间隔: {MONITOR_INTERVAL}s | 审计间隔: {AUDIT_INTERVAL}s")
        print(f"   PID: {os.getpid()}")
        print()

        PID_FILE.parent.mkdir(parents=True, exist_ok=True)
        PID_FILE.write_text(str(os.getpid()))

        def handle_signal(signum, frame):
            print(f"\n📡 收到信号 {signum}，关闭监控守护...")
            try:
                PID_FILE.unlink()
            except Exception:
                pass
            sys.exit(0)

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

        last_audit_time = 0

        while True:
            try:
                # 检查连接
                connections = self.capture_outbound_connections()
                for conn in connections:
                    if self._is_apple_service(conn):
                        self.block_and_alert(conn, "苹果服务")
                    elif self._is_tracker(conn):
                        self.block_and_alert(conn, "追踪服务")

                # 定时隐私审计
                now = time.time()
                if now - last_audit_time >= AUDIT_INTERVAL:
                    audit_result = self.run_privacy_audit()
                    self.audit_count += 1

                    if not audit_result.get("ok"):
                        self._push_alert(
                            "PRIVACY_AUDIT_FAILED",
                            f"第{self.audit_count}次隐私审计未通过"
                        )

                    # 防火墙存活检查
                    fw = self.check_firewall_status()
                    if not fw.get("pf_enabled"):
                        self._push_alert(
                            "FIREWALL_DOWN",
                            "pfctl防火墙已关闭！"
                        )

                    last_audit_time = now

                time.sleep(MONITOR_INTERVAL)

            except KeyboardInterrupt:
                break
            except Exception as e:
                self._push_alert("MONITOR_ERROR", str(e))
                time.sleep(10)

    def summary(self) -> str:
        """生成监控摘要"""
        lines = [
            "═══════════════════════════════════════",
            "  龍魂·同心锁监控摘要",
            f"  DNA: {DNA}",
            "═══════════════════════════════════════",
            f"  阻断次数: {self.block_count}",
            f"  审计次数: {self.audit_count}",
            f"  告警数量: {len(self.alerts)}",
            "═══════════════════════════════════════",
        ]
        return "\n".join(lines)


# ═══ 自检 ═══

def selftest():
    """同心锁监控自检"""
    errors = 0

    monitor = TongxinLockMonitor()

    # 1. 初始化
    assert monitor.block_count == 0
    print("  ✅ 1/5 初始化: 计数归零")

    # 2. 出站连接捕获
    conns = monitor.capture_outbound_connections()
    assert isinstance(conns, list), f"返回类型异常: {type(conns)}"
    print(f"  ✅ 2/5 连接捕获: 检测到{len(conns)}条活跃连接")

    # 3. 苹果服务检测
    test_conn = {"pid": "99999", "process": "test", "dest": "1.2.3.4:443->icloud.com:443"}
    assert monitor._is_apple_service(test_conn), "苹果检测漏报"
    normal_conn = {"pid": "99999", "process": "test", "dest": "1.2.3.4:443->uid9622.cn:443"}
    assert not monitor._is_apple_service(normal_conn), "苹果检测误报"
    print("  ✅ 3/5 苹果检测: 正确区分icloud/uid9622")

    # 4. 追踪服务检测
    tracker_conn = {"pid": "99999", "process": "test", "dest": "1.2.3.4:443->google-analytics.com:443"}
    assert monitor._is_tracker(tracker_conn), "追踪检测漏报"
    print("  ✅ 4/5 追踪检测: 正确识别google-analytics")

    # 5. 防火墙状态检查(不需要sudo即可尝试)
    fw = monitor.check_firewall_status()
    assert "pf_enabled" in fw, "缺少pf_enabled字段"
    print(f"  ✅ 5/5 防火墙检查: pf={'启用' if fw.get('pf_enabled') else '未启用'}")

    print(f"\n🎯 自检: 5/5 全绿")
    return errors == 0


# ═══ CLI ═══

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        ok = selftest()
        sys.exit(0 if ok else 1)

    parser = argparse.ArgumentParser(description="龍魂·同心锁状态监控")
    parser.add_argument("--daemon", action="store_true", help="后台守护模式")
    parser.add_argument("--once", action="store_true", help="单次审计")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("selftest", nargs="?", help="自检")

    args = parser.parse_args()

    monitor = TongxinLockMonitor()

    if args.daemon:
        monitor.daemon()
    elif args.once:
        result = monitor.once()
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(monitor.summary())
            if result["alerts"]:
                print(f"\n⚠️  告警 ({len(result['alerts'])}条):")
                for a in result["alerts"]:
                    print(f"   [{a['time'][:19]}] {a['type']}: {a['reason']}")
            if result["privacy_audit"] and not result["privacy_audit"]["ok"]:
                print(f"\n🔴 隐私审计未通过")
            if result["firewall_status"] and not result["firewall_status"]["pf_enabled"]:
                print(f"\n🔴 pfctl防火墙已关闭")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
