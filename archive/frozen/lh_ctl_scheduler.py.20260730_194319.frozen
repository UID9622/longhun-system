#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂引擎主控 · 定时任务调度器 v1.0
DNA: #龍芯⚡️丙午·丙申·癸酉·庚申·临-LH-CTL-SCHEDULER-v1.0-B2C3D4E5
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

用法:
  python3 bin/lh_ctl_scheduler.py add "0 2 * * *" --job "lh audit"
  python3 bin/lh_ctl_scheduler.py list
  python3 bin/lh_ctl_scheduler.py remove <job_id>
  python3 bin/lh_ctl_scheduler.py daemon
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh_ctl_config import load_config, state_dir, project_root

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
    from apscheduler.triggers.cron import CronTrigger
    from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
    HAS_APSCHEDULER = True
except ImportError:
    HAS_APSCHEDULER = False

CST = timezone(timedelta(hours=8))
DNA = "#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH-CTL-SCHEDULER-v1.0-B2C3D4E5"
PID_FILE = Path.home() / ".longhun" / "state" / "scheduler.pid"


def _now() -> str:
    return datetime.now(CST).isoformat()


def _ensure_db(cfg: Dict[str, Any]) -> str:
    d = state_dir(cfg)
    return f"sqlite:///{d / 'scheduler.sqlite'}"


def _get_scheduler(cfg: Dict[str, Any]):
    if not HAS_APSCHEDULER:
        raise RuntimeError("未安装 APScheduler，请运行: pip install apscheduler>=3.10.4")
    db_url = _ensure_db(cfg)
    jobstores = {"default": SQLAlchemyJobStore(url=db_url)}
    scheduler = BackgroundScheduler(jobstores=jobstores)
    return scheduler


def _parse_cron(cron_expr: str) -> Dict[str, str]:
    """把 cron 表达式五段解析为 minute/hour/day/month/day_of_week。"""
    parts = cron_expr.split()
    if len(parts) != 5:
        raise ValueError("cron 表达式必须是 5 段: 分 时 日 月 周")
    return {
        "minute": parts[0],
        "hour": parts[1],
        "day": parts[2],
        "month": parts[3],
        "day_of_week": parts[4],
    }


def _job_to_dict(job) -> Dict[str, Any]:
    trigger = job.trigger
    fields = {}
    if hasattr(trigger, "fields"):
        for f in trigger.fields:
            fields[f.name] = str(f)
    return {
        "id": job.id,
        "name": job.name,
        "next_run_time": str(job.next_run_time) if job.next_run_time else None,
        "trigger": fields,
    }


def _execute_job(command_line: str):
    """实际执行定时任务，并记录到 lh-ctl 日志。"""
    parts = command_line.split()
    if not parts:
        return
    # 支持 "lh audit" 或 "python3 bin/lh_ctl.py audit"
    if parts[0] == "lh":
        cfg = load_config()
        cmd = [sys.executable, str(project_root(cfg) / "bin" / "lh_ctl.py")] + parts[1:]
    else:
        cmd = parts
    subprocess.run(cmd, cwd=Path.home() / "longhun-system")


def cmd_add(cfg: Dict[str, Any], cron_expr: str, job_line: str, name: Optional[str] = None):
    scheduler = _get_scheduler(cfg)
    scheduler.start()
    try:
        cron = _parse_cron(cron_expr)
        job_id = f"sched-{uuid.uuid4().hex[:8]}"
        trigger = CronTrigger(**cron, timezone="Asia/Shanghai")
        scheduler.add_job(
            id=job_id,
            name=name or job_line,
            func=_execute_job,
            args=[job_line],
            trigger=trigger,
            replace_existing=True,
        )
        print(f"✅ 已添加定时任务: {job_id}")
        print(f"   表达式: {cron_expr}")
        print(f"   命令: {job_line}")
        # 立即列出确认
        cmd_list(cfg)
    finally:
        scheduler.shutdown()


def cmd_list(cfg: Dict[str, Any]):
    scheduler = _get_scheduler(cfg)
    scheduler.start()
    try:
        jobs = scheduler.get_jobs()
        if not jobs:
            print("📭 暂无定时任务")
            return
        print(f"\n📅 定时任务列表 ({len(jobs)} 个):")
        for job in jobs:
            d = _job_to_dict(job)
            print(f"  · {d['id']}: {d['name']}")
            print(f"    下次执行: {d['next_run_time']}")
    finally:
        scheduler.shutdown()


def cmd_remove(cfg: Dict[str, Any], job_id: str):
    scheduler = _get_scheduler(cfg)
    scheduler.start()
    try:
        scheduler.remove_job(job_id)
        print(f"✅ 已移除任务: {job_id}")
    finally:
        scheduler.shutdown()


def cmd_daemon(cfg: Dict[str, Any]):
    if not HAS_APSCHEDULER:
        print("❌ 未安装 APScheduler")
        sys.exit(1)

    scheduler = _get_scheduler(cfg)

    def on_event(event):
        if event.exception:
            print(f"[{_now()}] 任务执行失败: {event.job_id} - {event.exception}")
        else:
            print(f"[{_now()}] 任务执行成功: {event.job_id}")

    scheduler.add_listener(on_event, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()

    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    print(f"{DNA}")
    print(f"🕐 调度器守护进程已启动 (PID {os.getpid()})")
    print("   按 Ctrl+C 停止")

    try:
        # 保持主线程存活
        import time
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()
        if PID_FILE.exists():
            PID_FILE.unlink()
        print("🛑 调度器已停止")


def main():
    parser = argparse.ArgumentParser(description="龍魂引擎主控定时任务调度器")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="添加定时任务")
    add_p.add_argument("cron", help="cron 表达式，如 '0 2 * * *'")
    add_p.add_argument("--job", required=True, help="要执行的命令，如 'lh audit'")
    add_p.add_argument("--name", help="任务名称")

    sub.add_parser("list", help="列出定时任务")

    rm_p = sub.add_parser("remove", help="移除定时任务")
    rm_p.add_argument("job_id", help="任务 ID")

    sub.add_parser("daemon", help="启动守护进程（前台）")

    args = parser.parse_args()

    cfg = load_config()

    if args.command == "add":
        cmd_add(cfg, args.cron, args.job, args.name)
    elif args.command == "list":
        cmd_list(cfg)
    elif args.command == "remove":
        cmd_remove(cfg, args.job_id)
    elif args.command == "daemon":
        cmd_daemon(cfg)


if __name__ == "__main__":
    main()
