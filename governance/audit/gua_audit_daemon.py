#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
👁️ 上帝之眼 · 64卦审计守护进程
DNA:#龍芯⚡️2026-06-29-64GUA-AUDIT-DAEMON-FILE1-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬64GUA-DAEMON-001 ✅

功能：
  1. 常驻后台运行 Flask API 服务
  2. 每5分钟执行一次高频系统审计
  3. 每天凌晨2:00执行全量审计 + 日志归档
  4. 审计日志写入 ~/.龍魂/audit/audit_log.jsonl
"""

import os
import sys
import json
import time
import signal
import shutil
import hashlib
import threading
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent))
from gua_audit_engine import GuaAuditEngine
from audit_api import app as flask_app, write_audit_log, AUDIT_LOG_FILE, AUDIT_LOG_DIR


# ============================================================
# 配置
# ============================================================

DAEMON_PID_FILE = Path.home() / "longhun-system" / "logs" / "gua_audit_daemon.pid"
DAEMON_STATUS_FILE = Path.home() / "longhun-system" / "logs" / "gua_audit_daemon.status"
ARCHIVE_DIR = AUDIT_LOG_DIR / "archive"
HIGH_FREQ_INTERVAL = 300  # 5分钟
DAILY_HOUR = 2
DAILY_MINUTE = 0
PORT = int(os.environ.get("GUA_AUDIT_PORT", "9623"))


# ============================================================
# DNA 追溯
# ============================================================

def 生成DNA(動作: str) -> str:
    時間戳 = datetime.now().strftime("%Y%m%d-%H%M%S")
    熵 = hashlib.sha256(f"{動作}-{time.time_ns()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{時間戳}-64GUA-AUDIT-DAEMON-{動作}-HASH{熵}"


# ============================================================
# 指标采集
# ============================================================

def collect_metrics() -> dict[str, Any]:
    """采集系统8维度指标"""
    metrics = {
        "innovation": 70,
        "support": 75,
        "response": 80,
        "optimization": 70,
        "risk_control": 75,
        "communication": 80,
        "defense": 90,
        "collaboration": 80,
    }

    try:
        # 创新度：最近7天新增Python文件数
        root = Path.home() / "longhun-system"
        if root.exists():
            recent_files = list(root.rglob("*.py"))
            week_ago = time.time() - 7 * 24 * 3600
            new_files = sum(1 for f in recent_files if f.exists() and f.stat().st_mtime > week_ago)
            metrics["innovation"] = min(100, 60 + new_files * 5)

        # 支持度：文档文件数
        docs = list(root.rglob("*.md")) if root.exists() else []
        metrics["support"] = min(100, 50 + len(docs) * 2)

        # 响应度：核心服务端口
        sock = Path.home() / "longhun-system" / "cnsh" / "redlines.sock"
        metrics["response"] = 90 if sock.exists() else 60

        # 风险管控：关键文件完整性
        core_files = [
            Path.home() / "longhun-system" / "audit" / "gua_audit_engine.py",
            Path.home() / "longhun-system" / "audit" / "audit_api.py",
            Path.home() / "longhun-system" / "audit" / "gua_audit_daemon.py",
        ]
        exists = sum(1 for f in core_files if f.exists())
        metrics["risk_control"] = min(100, 50 + exists * 15)

        # 防御度：DNA标记覆盖率
        py_files = list(root.rglob("*.py")) if root.exists() else []
        if py_files:
            dna_count = 0
            for f in py_files[:50]:
                try:
                    content = f.read_text(encoding="utf-8", errors="ignore")
                    if "#龍芯⚡️" in content or "#ZHUGEXIN⚡️" in content:
                        dna_count += 1
                except Exception:
                    pass
            metrics["defense"] = min(100, int(dna_count / len(py_files[:50]) * 100))

        # 协作度：能力注册数量
        registry = Path.home() / "longhun-system" / "capabilities" / "capability_registry.json"
        if registry.exists():
            try:
                data = json.loads(registry.read_text(encoding="utf-8"))
                cap_count = len(data.get("capabilities", {}))
                metrics["collaboration"] = min(100, 50 + cap_count * 3)
            except Exception:
                pass

    except Exception:
        pass

    return {k: min(100, max(0, v)) for k, v in metrics.items()}


# ============================================================
# 审计执行
# ============================================================

def run_audit(context: str = "高频巡检") -> dict[str, Any]:
    engine = GuaAuditEngine()
    metrics = collect_metrics()
    result = engine.calculate_gua(metrics, context=context)
    record = result.to_dict()
    record["context"] = context
    record["trigger"] = "daemon"
    write_audit_log(record)
    return record


def archive_logs():
    """归档审计日志：按月份压缩保存"""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    if not AUDIT_LOG_FILE.exists():
        return

    now = datetime.now()
    archive_name = f"audit_log_{now.strftime('%Y%m')}.jsonl"
    archive_path = ARCHIVE_DIR / archive_name

    # 把当前日志追加到月归档
    with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as src, \
         open(archive_path, "a", encoding="utf-8") as dst:
        for line in src:
            dst.write(line)

    # 清空当前日志
    AUDIT_LOG_FILE.write_text("", encoding="utf-8")

    # 压缩旧归档
    for old_file in ARCHIVE_DIR.glob("audit_log_*.jsonl"):
        if old_file.name != archive_name:
            gz_path = old_file.with_suffix(".jsonl.gz")
            subprocess.run(["gzip", "-f", str(old_file)], check=False, capture_output=True)


# ============================================================
# 调度循环
# ============================================================

class AuditDaemon:
    def __init__(self):
        self.running = True
        self.last_daily = None

    def start_api(self):
        """在后台线程启动 Flask API"""
        def run():
            flask_app.run(host="127.0.0.1", port=PORT, debug=False, use_reloader=False)
        t = threading.Thread(target=run, daemon=True)
        t.start()

    def scheduler_loop(self):
        """主调度循环"""
        while self.running:
            now = datetime.now()

            # 每5分钟高频审计
            record = run_audit(context=f"高频巡检 {now.strftime('%H:%M')}")

            # 每天凌晨2:00全量审计 + 归档
            if now.hour == DAILY_HOUR and now.minute == DAILY_MINUTE:
                if self.last_daily != now.date():
                    run_audit(context="每日全量审计")
                    archive_logs()
                    self.last_daily = now.date()

            # 更新状态文件
            status = {
                "status": "running",
                "last_run": now.isoformat(),
                "last_gua": record.get("gua_name"),
                "last_color": record.get("audit_color"),
                "pid": os.getpid(),
                "port": PORT,
                "dna": 生成DNA("HEARTBEAT"),
            }
            DAEMON_STATUS_FILE.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")

            # 等待下一个周期
            for _ in range(HIGH_FREQ_INTERVAL):
                if not self.running:
                    break
                time.sleep(1)

    def stop(self):
        self.running = False


def write_pid():
    DAEMON_PID_FILE.write_text(str(os.getpid()), encoding="utf-8")


def remove_pid():
    DAEMON_PID_FILE.unlink(missing_ok=True)


def main():
    write_pid()
    daemon = AuditDaemon()

    def signal_handler(signum, frame):
        print(f"\n🛑 收到信号 {signum}，64卦审计守护进程优雅退出")
        daemon.stop()
        remove_pid()
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    print(f"""
╔══════════════════════════════════════════╗
║   上帝之眼 · 64卦审计守护进程 v1.0        ║
║   API Port: {PORT:<5}                        ║
║   高频巡检: 每5分钟                       ║
║   全量审计: 每天 {DAILY_HOUR:02d}:{DAILY_MINUTE:02d}                    ║
║   DNA: #龍芯⚡️2026-06-29-64GUA-AUDIT-DAEMON-v1.0 ║
╚══════════════════════════════════════════╝
""")

    daemon.start_api()
    time.sleep(1)  # 等待API启动
    daemon.scheduler_loop()


if __name__ == "__main__":
    main()
