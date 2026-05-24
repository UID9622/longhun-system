# -*- coding: utf-8 -*-
"""
CNSH 责任卡网关：由 .cnsh 执行链（或手动）在 before/after/error/reject/audit 时触发 decision_cli。
不修改 dragon_daemon；由集成方显式 import 本模块或调用 CLI。
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def _cli_path() -> Path:
    return Path(__file__).resolve().parent / "decision_cli.py"


def build_trigger(event: str, file_path: str, status: str, detail: str) -> str:
    return (
        f"CNSH责任卡触发\n"
        f"事件: {event}\n"
        f"文件: {file_path}\n"
        f"状态: {status}\n"
        f"详情: {detail}\n"
        f"时间: {datetime.now().isoformat(timespec='seconds')}"
    )


def invoke(
    event: str,
    file_path: str,
    *,
    status: str = "pending",
    detail: str = "",
    light: bool = False,
) -> subprocess.CompletedProcess[str]:
    trig = build_trigger(event, file_path, status, detail)
    cmd = [sys.executable, str(_cli_path())]
    cmd.append("--light" if light else "--full")
    cmd.append(trig)
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(_cli_path().parent))


def main() -> int:
    ap = argparse.ArgumentParser(description="CNSH → 责任卡网关")
    ap.add_argument("--event", required=True)
    ap.add_argument("--file", required=True)
    ap.add_argument("--status", default="pending")
    ap.add_argument("--detail", default="")
    ap.add_argument("--light", action="store_true")
    args = ap.parse_args()
    r = invoke(
        args.event,
        args.file,
        status=args.status,
        detail=args.detail,
        light=args.light,
    )
    if r.stdout:
        print(r.stdout, end="")
    if r.stderr:
        print(r.stderr, end="", file=sys.stderr)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
