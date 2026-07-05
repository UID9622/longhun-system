#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 CNSH 红线引擎 · 开机自启入口
DNA: #龍芯⚡️2026-06-29-CNSH-REDLINES-BOOT-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬REDLINES-BOOT-001 ✅

功能：
  1. 启动时加载红线词组定义
  2. 写入状态文件与心跳
  3. 提供 Unix Domain Socket 接口供本地进程查询
  4. 支持 SIGTERM/SIGINT 优雅退出
"""

import os
import sys
import json
import time
import signal
import socket
import hashlib
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cnsh_redlines


# ============================================================
# 配置
# ============================================================

STATUS_FILE = Path.home() / "longhun-system" / "logs" / "cnsh_redlines.status"
SOCKET_PATH = Path.home() / "longhun-system" / "cnsh" / "redlines.sock"
PID_FILE = Path.home() / "longhun-system" / "logs" / "cnsh_redlines.pid"


# ============================================================
# 启动
# ============================================================

def 生成DNA(模块: str, 动作: str) -> str:
    时间戳 = time.strftime("%Y-%m-%d-%H%M%S")
    熵 = hashlib.sha256(f"{模块}-{动作}-{time.time_ns()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{时间戳}-{模块}-{动作}-HASH{熵}"


def 写入状态(状态: dict):
    STATUS_FILE.write_text(json.dumps(状态, ensure_ascii=False, indent=2), encoding="utf-8")


def 加载引擎():
    熔断器 = cnsh_redlines.红线熔断器()
    统计 = {}
    for 级别, 词组列表 in cnsh_redlines.红线分级.items():
        统计[级别] = len(词组列表)
    return 熔断器, 统计


# ============================================================
# Socket 服务
# ============================================================

class 红线Socket服务:
    def __init__(self, 熔断器):
        self.熔断器 = 熔断器
        self.运行中 = True
        self.服务器 = None

    def 启动(self):
        # 清理旧 socket
        if SOCKET_PATH.exists():
            SOCKET_PATH.unlink()

        self.服务器 = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.服务器.bind(str(SOCKET_PATH))
        self.服务器.listen(5)
        os.chmod(SOCKET_PATH, 0o600)

        while self.运行中:
            try:
                self.服务器.settimeout(1.0)
                连接, _ = self.服务器.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            线程 = threading.Thread(target=self.处理连接, args=(连接,))
            线程.daemon = True
            线程.start()

        if SOCKET_PATH.exists():
            SOCKET_PATH.unlink()

    def 处理连接(self, 连接):
        try:
            数据 = 连接.recv(65535).decode("utf-8")
            try:
                请求 = json.loads(数据)
            except json.JSONDecodeError:
                响应 = {"错误": "请求必须是 JSON"}
                连接.sendall(json.dumps(响应, ensure_ascii=False).encode("utf-8"))
                return

            动作 = 请求.get("动作")
            if 动作 == "扫描":
                文本 = 请求.get("文本", "")
                结果 = self.熔断器.熔断检查(文本)
                响应 = {
                    "触发": 结果["触发"],
                    "最高级别": 结果["最高级别"],
                    "命中": 结果["命中"],
                    "DNA": 结果["DNA"],
                }
            elif 动作 == "心跳":
                响应 = {"状态": "存活", "DNA": 生成DNA("REDLINE-DAEMON", "HEARTBEAT")}
            elif 动作 == "清单":
                响应 = {"红线分级": cnsh_redlines.红线分级}
            else:
                响应 = {"错误": f"未知动作: {动作}"}

            连接.sendall(json.dumps(响应, ensure_ascii=False).encode("utf-8"))
        finally:
            连接.close()

    def 停止(self):
        self.运行中 = False
        if self.服务器:
            self.服务器.close()


# ============================================================
# 主流程
# ============================================================

def main():
    DNA = 生成DNA("CNSH-REDLINES", "BOOT")

    # 写入 PID
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")

    # 加载引擎
    熔断器, 统计 = 加载引擎()

    # 启动状态
    状态 = {
        "状态": "已启动",
        "启动时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "DNA": DNA,
        "PID": os.getpid(),
        "词组统计": 统计,
        "套接字": str(SOCKET_PATH),
    }
    写入状态(状态)

    print(f"🐉 龍魂 CNSH 红线引擎已启动")
    print(f"   {DNA}")
    print(f"   状态文件: {STATUS_FILE}")
    print(f"   查询套接字: {SOCKET_PATH}")

    # 启动 socket 服务
    服务 = 红线Socket服务(熔断器)

    def 信号处理(signum, frame):
        print(f"\n🛑 收到信号 {signum}，红线引擎优雅退出")
        服务.停止()
        状态["状态"] = "已停止"
        状态["停止时间"] = time.strftime("%Y-%m-%d %H:%M:%S")
        写入状态(状态)
        PID_FILE.unlink(missing_ok=True)
        sys.exit(0)

    signal.signal(signal.SIGTERM, 信号处理)
    signal.signal(signal.SIGINT, 信号处理)

    服务.启动()


if __name__ == "__main__":
    main()
