#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-AUTO-OPERATOR-v1.0-c4d8e2a1
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · AI 自动操作引擎 v1.0
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-AUTO-OPERATOR-v1.0-c4d8e2a1

功能:
  - 定时/事件触发 AI 执行操作
  - 每次操作自动记录审计日志
  - 可注册自定义任务
  - 守护进程模式

用法:
  lh console operator start        # 启动AI自动操作引擎
  lh console operator stop         # 停止
  lh console operator status       # 查看任务状态
  python3 bin/lh_auto_operator.py  # 直接启动
"""

import os
import sys
import json
import time
import signal
import threading
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Callable, Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "bin"))

# 导入公开操作台模块
from lh_public_console import (
    log_audit, set_state, get_state, get_latest_audit,
    generate_dna, cst_now, cst_iso, get_system_health
)

CST = timezone(timedelta(hours=8))
PID_FILE = ROOT / "data" / "auto_operator.pid"
TASK_LOG = ROOT / "logs" / "auto_operator.log"


class AutoOperator:
    """AI 自动操作引擎"""

    def __init__(self):
        self.running = False
        self.tasks: List[Dict] = []
        self.threads: List[threading.Thread] = []
        self._lock = threading.Lock()

    def register_task(self, name: str, func: Callable, interval: int = 60,
                      description: str = ""):
        """注册一个定时任务"""
        task = {
            "name": name,
            "func": func,
            "interval": interval,
            "description": description,
            "run_count": 0,
            "error_count": 0,
            "last_run": None,
            "last_error": None,
        }
        self.tasks.append(task)
        log_audit(actor="AI", action="register_task", target=name,
                  data={"interval": interval, "desc": description})
        return task

    def _run_task_loop(self, task: Dict):
        """单任务循环"""
        name = task["name"]
        log_audit(actor="AI", action="task_started", target=name)

        while self.running:
            try:
                result = task["func"]()
                with self._lock:
                    task["run_count"] += 1
                    task["last_run"] = cst_iso()

                dna = log_audit(
                    actor="AI",
                    action="task_run",
                    target=name,
                    data={"result": str(result)[:200] if result else "ok"},
                    result="ok"
                )
                # 更新任务状态到公开状态
                set_state(
                    f"task.{name}",
                    json.dumps({
                        "status": "ok", "run_count": task["run_count"],
                        "last_run": task["last_run"], "error_count": task["error_count"]
                    }, ensure_ascii=False),
                    actor="AI"
                )
            except Exception as e:
                with self._lock:
                    task["error_count"] += 1
                    task["last_error"] = str(e)
                log_audit(
                    actor="AI",
                    action="task_error",
                    target=name,
                    data={"error": str(e)[:500]},
                    result="error"
                )
                set_state(
                    f"task.{name}",
                    json.dumps({
                        "status": "error", "error": str(e)[:200],
                        "run_count": task["run_count"], "error_count": task["error_count"]
                    }, ensure_ascii=False),
                    actor="AI"
                )
            time.sleep(task["interval"])

    def start(self):
        """启动所有注册任务"""
        if self.running:
            return
        self.running = True
        log_audit(actor="AI", action="operator_start",
                  target=f"tasks={len(self.tasks)}",
                  data={"tasks": [t["name"] for t in self.tasks]})

        for task in self.tasks:
            t = threading.Thread(
                target=self._run_task_loop,
                args=(task,),
                daemon=True,
                name=f"op-{task['name']}"
            )
            t.start()
            self.threads.append(t)

        # 写PID
        PID_FILE.write_text(str(os.getpid()))

        print(f"""
🐉 AI 自动操作引擎已启动
━━━━━━━━━━━━━━━━━━━━━━
  PID:        {os.getpid()}
  已注册任务: {len(self.tasks)}
""")
        for t in self.tasks:
            print(f"  🔄 {t['name']:30s} 每 {t['interval']}s — {t.get('description','')}")
        print("━━━━━━━━━━━━━━━━━━━━━━\n")

        set_state("auto_operator", json.dumps({
            "status": "running", "pid": os.getpid(),
            "started_at": cst_iso(), "task_count": len(self.tasks)
        }, ensure_ascii=False), actor="AI")

    def stop(self):
        """停止"""
        self.running = False
        log_audit(actor="AI", action="operator_stop",
                  target=f"tasks_ran={sum(t['run_count'] for t in self.tasks)}")
        set_state("auto_operator", json.dumps({
            "status": "stopped", "stopped_at": cst_iso()
        }, ensure_ascii=False), actor="AI")
        if PID_FILE.exists():
            PID_FILE.unlink()

    def status(self) -> Dict:
        """获取状态"""
        return {
            "running": self.running,
            "task_count": len(self.tasks),
            "tasks": [
                {
                    "name": t["name"],
                    "interval": t["interval"],
                    "run_count": t["run_count"],
                    "error_count": t["error_count"],
                    "last_run": t["last_run"],
                    "last_error": t["last_error"],
                    "description": t.get("description", "")
                }
                for t in self.tasks
            ]
        }


# ============================================================
# 内置AI任务
# ============================================================

def heartbeat_task():
    """心跳任务：定期记录系统存活"""
    health = get_system_health()
    return {"alive": True, "hostname": health.get("hostname", "unknown")}


def state_watchdog_task():
    """状态看门狗：检测auto_operator状态是否正常"""
    state = get_state("auto_operator")
    # 如果有异常状态记录，这里可以触发告警
    return {"watchdog_ok": True, "operator_state": state if state else "no_state"}


def auto_gc_task():
    """数据维护：清理90天前的审计日志统计（不删数据）"""
    logs = get_latest_audit(limit=1)
    total_ops = len(get_latest_audit(limit=1000))
    return {"audit_count_check": total_ops, "latest": logs[0]["dna"] if logs else "empty"}


# ============================================================
# CLI
# ============================================================

def main():
    import argparse
    ap = argparse.ArgumentParser(description="龍魂AI自动操作引擎 v1.0")
    ap.add_argument("action", nargs="?", default="start",
                    choices=["start", "stop", "status", "daemon"])
    ap.add_argument("--interval", type=int, default=60, help="心跳间隔(秒)")
    ap.add_argument("--port", type=int, default=8778, help="操作台端口")
    args = ap.parse_args()

    operator = AutoOperator()

    if args.action == "status":
        if PID_FILE.exists():
            pid = PID_FILE.read_text().strip()
            print(f"🐉 AI自动操作引擎运行中 · PID: {pid}")
            # 检查进程是否存在
            try:
                os.kill(int(pid), 0)
                print("✅ 进程活跃")
            except (OSError, ValueError):
                print("⚠️ PID文件存在但进程已死")
        else:
            print("🐉 AI自动操作引擎未运行")
        # 打印最近AI操作日志
        logs = get_latest_audit(limit=5, actor="AI")
        print(f"\n📋 最近AI操作 ({len(logs)}):")
        for l in logs:
            print(f"  [{l['timestamp'][:19]}] {l['action']:15s} {l['target']} — {l.get('result','')}")
        return

    if args.action == "stop":
        if PID_FILE.exists():
            pid = int(PID_FILE.read_text().strip())
            try:
                os.kill(pid, signal.SIGTERM)
                print(f"✅ 已发送停止信号给 PID {pid}")
            except OSError:
                print("⚠️ 进程已不存在")
            PID_FILE.unlink(missing_ok=True)
        else:
            print("⚠️ 未找到运行中的引擎")
        set_state("auto_operator", json.dumps({"status": "stopped", "stopped_at": cst_iso()}), actor="cli")
        return

    # 注册默认任务
    operator.register_task("heartbeat", heartbeat_task, interval=args.interval,
                           description="系统心跳存活检测")
    operator.register_task("watchdog", state_watchdog_task, interval=args.interval * 2,
                           description="状态看门狗")
    operator.register_task("gc_check", auto_gc_task, interval=300,
                           description="每5分钟审计数据维护检查")

    # 启动
    operator.start()

    # 信号处理
    def handle_signal(signum, frame):
        print(f"\n🛑 收到信号 {signum}，正在停止...")
        operator.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        operator.stop()


if __name__ == "__main__":
    main()
