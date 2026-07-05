#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 CNSH 红线引擎 · 本地守护进程查询客户端
DNA: #龍芯⚡️2026-06-29-CNSH-REDLINES-CLIENT-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬REDLINES-CLIENT-001 ✅

用法：
  python3 cnsh_redline_client.py scan "文本..."
  python3 cnsh_redline_client.py scan-file article.txt
  python3 cnsh_redline_client.py heartbeat
  python3 cnsh_redline_client.py list
"""

import sys
import json
import socket
from pathlib import Path

SOCKET_PATH = Path.home() / "longhun-system" / "cnsh" / "redlines.sock"


def 查询(请求: dict) -> dict:
    if not SOCKET_PATH.exists():
        print(f"❌ 守护进程未启动，套接字不存在: {SOCKET_PATH}")
        print("   尝试执行: launchctl load ~/Library/LaunchAgents/com.longhun.cnsh-redlines.plist")
        sys.exit(1)

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect(str(SOCKET_PATH))
        s.send(json.dumps(请求, ensure_ascii=False).encode("utf-8"))
        s.shutdown(socket.SHUT_WR)
        数据 = b""
        while True:
            块 = s.recv(65535)
            if not 块:
                break
            数据 += 块
        return json.loads(数据.decode("utf-8"))
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        sys.exit(1)
    finally:
        s.close()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    命令 = sys.argv[1]

    if 命令 == "scan":
        if len(sys.argv) < 3:
            print("❌ 请提供要扫描的文本")
            return
        文本 = " ".join(sys.argv[2:])
        结果 = 查询({"动作": "扫描", "文本": 文本})
        print(json.dumps(结果, ensure_ascii=False, indent=2))

    elif 命令 == "scan-file":
        if len(sys.argv) < 3:
            print("❌ 请提供文件路径")
            return
        path = Path(sys.argv[2])
        if not path.exists():
            print(f"❌ 文件不存在: {path}")
            return
        文本 = path.read_text(encoding="utf-8")
        结果 = 查询({"动作": "扫描", "文本": 文本})
        print(json.dumps(结果, ensure_ascii=False, indent=2))

    elif 命令 == "heartbeat":
        结果 = 查询({"动作": "心跳"})
        print(json.dumps(结果, ensure_ascii=False, indent=2))

    elif 命令 == "list":
        结果 = 查询({"动作": "清单"})
        print(json.dumps(结果, ensure_ascii=False, indent=2))

    else:
        print(f"❌ 未知命令: {命令}")
        print(__doc__)


if __name__ == "__main__":
    main()
