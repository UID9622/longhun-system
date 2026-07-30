#!/usr/bin/env python3
#龍芯⚡️2026-06-25-DAILY-REVIEW-v2.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

# DNA: #龍芯⚡️2026-06-25-DAILY-REVIEW-v2.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""
龍魂系统 · 每日复盘 v2.0

功能:
- 检查核心文件是否存在
- 检查远程仓库配置
- 检查审计日志是否可写入
- 检查过载状态
- 输出带 evidence + stats 的完成报告
- 自动写入 audit.jsonl
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "persona"))
from overload_guard import 龍魂过载守护
from audit_logger import 龍魂审计日志器


def main():
    start = time.time()
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{today}] 龍魂系统每日复盘开始")

    # 检查核心文件
    core_files = [
        "longhun_persona_hub.py",
        "personas/runtime/system_status_panel.py",
        "personas/runtime/compression_engine.py",
        "personas/runtime/dna_tracer.py",
        "personas/runtime/audit_logger.py",
        "personas/runtime/output_contract.py",
        "personas/runtime/overload_guard.py",
        "personas/runtime/anti_blowout_guard.py",
    ]
    missing = [f for f in core_files if not (ROOT / f).exists()]
    file_check_ok = len(missing) == 0
    if missing:
        print(f"❌ 缺失核心文件: {', '.join(missing)}")
    else:
        print("✅ 核心文件齐全")

    # 检查远程仓库
    try:
        import subprocess
        remotes = subprocess.check_output(["git", "remote", "-v"], cwd=str(ROOT), text=True).strip()
        remote_count = len(remotes.splitlines()) // 2
        print(f"✅ 已配置 {remote_count} 个远程仓库")
    except Exception as e:
        print(f"⚠️ 无法读取远程仓库: {e}")
        remote_count = 0

    # 检查过载
    guard = 龍魂过载守护()
    status = guard.请求检查()
    print(f"{status['emoji']} 系统状态: {status['level']} ({status['description']})")

    # 写入审计日志
    logger = 龍魂审计日志器()
    duration_ms = int((time.time() - start) * 1000)
    record = logger.记录(
        op="daily_review",
        status="success" if file_check_ok else "partial",
        evidence={
            "artifact_path": "daily_review.py",
            "core_files_checked": len(core_files),
            "remote_count": remote_count,
        },
        stats={
            "duration_ms": duration_ms,
            "missing_files": len(missing),
            "overload_score": status.get("score", 0),
        },
        error_code=",".join(missing) if missing else None,
        user_id=os.environ.get("USER", "system"),
    )

    print(f"✅ 每日复盘完成，审计ID: {record['id']}")
    return 0 if file_check_ok else 1


if __name__ == "__main__":
    exit(main())
