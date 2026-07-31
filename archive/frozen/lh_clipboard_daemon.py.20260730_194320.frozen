#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·剪贴板意图守护进程 v1.0
==========================
DNA: #龍芯⚡️丙午·癸未·丁未·申时·☴巽-CLIPBOARD-DAEMON-v1.0

你复制/粘贴的每一段文字，系统都自动读、自动分析、自动触发引擎。
默认 dry-run（只看不执行），加 --execute 才真正动作。

用法:
  python3 engines/lh_clipboard_daemon.py              # dry-run 模式监听
  python3 engines/lh_clipboard_daemon.py --execute    # 自动执行
  python3 engines/lh_clipboard_daemon.py --interval 1 # 每秒检查一次
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from engines.lh_auto_intent import run


def _get_clipboard() -> str:
    try:
        proc = subprocess.run(["pbpaste"], capture_output=True, text=True, timeout=5)
        return proc.stdout if proc.returncode == 0 else ""
    except Exception:
        return ""


def main():
    parser = argparse.ArgumentParser(description="龍魂·剪贴板意图守护进程")
    parser.add_argument("--execute", action="store_true", help="真正执行匹配到的引擎/动作")
    parser.add_argument("--interval", type=float, default=2.0, help="检查间隔秒数")
    args = parser.parse_args()

    print("📋 龍魂剪贴板守护进程已启动")
    print(f"   模式: {'执行' if args.execute else 'dry-run（只分析不执行）'}")
    print(f"   间隔: {args.interval}s")
    print("   按 Ctrl+C 停止\n")

    last_content = ""
    try:
        while True:
            content = _get_clipboard()
            if content and content != last_content and len(content.strip()) > 3:
                last_content = content
                print(f"🔔 检测到新剪贴板内容 ({len(content)} 字符)")
                print(f"    前50字: {content[:50].replace(chr(10), ' ')}...")
                result = run(content, dry_run=not args.execute)
                from engines.lh_auto_intent import _format_report
                print(_format_report(result))
                print("-" * 64)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n👋 剪贴板守护进程已停止")


if __name__ == "__main__":
    main()
