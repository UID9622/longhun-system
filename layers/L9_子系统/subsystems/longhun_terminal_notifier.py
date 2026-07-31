# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂终端通知模块 v1.0

支持 macOS 原生通知中心（osascript），失败时回退到命令行打印。
DNA: #龍芯⚡️2026-06-29-LONGHUN-NOTIFIER-v1-UID9622
"""
from __future__ import annotations

import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

DNA = "#龍芯⚡️2026-06-29-LONGHUN-NOTIFIER-v1-UID9622"


def notify(
    title: str,
    message: str,
    subtitle: Optional[str] = None,
    sound: bool = False,
    timeout: int = 5,
) -> bool:
    """发送一条终端/桌面通知。"""
    system = platform.system()
    sent = False

    if system == "Darwin" and shutil.which("osascript"):
        sent = _notify_macos(title, message, subtitle, sound)

    if not sent:
        # 回退：打印到 stderr，避免污染 stdout 管道
        print(f"\n[龍魂通知] {title}", file=sys.stderr)
        if subtitle:
            print(f"  子标题: {subtitle}", file=sys.stderr)
        print(f"  {message}\n", file=sys.stderr)
        sent = True

    return sent


def _notify_macos(title: str, message: str, subtitle: Optional[str], sound: bool) -> bool:
    try:
        script = f'display notification "{message}" with title "{title}"'
        if subtitle:
            script += f' subtitle "{subtitle}"'
        if sound:
            script += ' sound name "Glass"'
        subprocess.run(
            ["osascript", "-e", script],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception:
        return False


def main(argv: list[str] = sys.argv) -> int:
    if len(argv) < 3:
        print("用法: python3 longhun_terminal_notifier.py <标题> <内容> [子标题]", file=sys.stderr)
        return 1
    notify(argv[1], argv[2], argv[3] if len(argv) > 3 else None, sound=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
