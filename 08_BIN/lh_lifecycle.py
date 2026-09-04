#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·脚本生命周期管理器 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷝离-LIFECYCLE-MANAGER-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

核心能力：
  1. 启动管理 — subprocess.Popen + 非阻塞 + PID注册
  2. 流式监控 — stdout/stderr实时输出 + 超时倒计时
  3. 自动停止 — 正常结束/超时kill/空闲检测/错误熔断
  4. 僵尸清理 — 进程组kill + PID注销 + 资源释放
  5. 审计日志 — 每次执行留痕（开始/结束/超时/错误）

使用方式：
  from lh_lifecycle import ScriptRunner

  runner = ScriptRunner(timeout=300, idle_timeout=60)
  result = runner.run("python3 bin/lh_search_engine.py search 龍魂")
  # result.status: 'success' | 'timeout' | 'idle_kill' | 'error' | 'crashed'
  # result.stdout, result.stderr, result.duration, result.exit_code
"""

import os
import sys
import time
import signal
import psutil
import json
import shlex
import hashlib
import threading
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

# ============================================================
# 数据类型
# ============================================================

class RunStatus(Enum):
    """执行状态"""
    PENDING = "pending"        # 等待中
    RUNNING = "running"        # 运行中
    SUCCESS = "success"        # 正常完成
    TIMEOUT = "timeout"        # 超时强制终止
    IDLE_KILL = "idle_kill"    # 空闲超时终止
    ERROR = "error"            # 运行错误
    CRASHED = "crashed"        # 崩溃
    REJECTED = "rejected"      # 被拒绝（安全规则）


@dataclass
class RunResult:
    """执行结果"""
    run_id: str                          # 唯一运行ID
    command: str                         # 原始命令
    status: RunStatus = RunStatus.PENDING
    exit_code: int = -1
    stdout: str = ""
    stderr: str = ""
    started_at: str = ""
    finished_at: str = ""
    duration: float = 0.0                # 秒
    pid: int = -1
    error_message: str = ""
    cpu_peak: float = 0.0                # CPU峰值%
    mem_peak_mb: float = 0.0             # 内存峰值MB
    last_activity: str = ""              # 最后活跃时间

    def to_dict(self) -> dict:
        d = {k: (v.value if isinstance(v, RunStatus) else v) for k, v in self.__dict__.items()}
        return d

    def is_ok(self) -> bool:
        return self.status == RunStatus.SUCCESS


# ============================================================
# 进程守护器
# ============================================================

class ProcessGuard:
    """进程守护：追踪PID·收割僵尸·资源监控"""

    def __init__(self):
        self._pids: Dict[int, Dict] = {}  # pid → {run_id, command, started_at}
        self._lock = threading.Lock()

    def register(self, pid: int, run_id: str, command: str):
        with self._lock:
            self._pids[pid] = {
                "run_id": run_id,
                "command": command,
                "started_at": datetime.now().isoformat()
            }

    def unregister(self, pid: int):
        with self._lock:
            self._pids.pop(pid, None)

    def kill_pid(self, pid: int, force: bool = False) -> bool:
        """终止进程（先SIGTERM，再SIGKILL）"""
        try:
            proc = psutil.Process(pid)
            children = proc.children(recursive=True)

            # 先温柔终止
            sig = signal.SIGKILL if force else signal.SIGTERM
            for child in children:
                try:
                    child.send_signal(sig)
                except psutil.NoSuchProcess:
                    pass
            proc.send_signal(sig)

            if not force:
                # 等2秒
                try:
                    proc.wait(timeout=2)
                except psutil.TimeoutExpired:
                    # 还不死就SIGKILL
                    return self.kill_pid(pid, force=True)

            self.unregister(pid)
            return True
        except psutil.NoSuchProcess:
            self.unregister(pid)
            return True
        except Exception:
            return False

    def kill_all(self) -> int:
        """终止所有追踪中的进程"""
        killed = 0
        with self._lock:
            pids = list(self._pids.keys())
        for pid in pids:
            if self.kill_pid(pid, force=True):
                killed += 1
        return killed

    def get_resource(self, pid: int) -> Tuple[float, float]:
        """获取进程CPU%和内存MB"""
        try:
            proc = psutil.Process(pid)
            cpu = proc.cpu_percent(interval=0.1)
            mem = proc.memory_info().rss / 1024 / 1024
            return cpu, mem
        except psutil.NoSuchProcess:
            return 0, 0

    @property
    def active_count(self) -> int:
        with self._lock:
            return len(self._pids)

    def list_processes(self) -> List[Dict]:
        with self._lock:
            return [{"pid": pid, **info} for pid, info in self._pids.items()]


# ============================================================
# 脚本执行器（核心）
# ============================================================

class ScriptRunner:
    """
    脚本生命周期执行器

    参数:
      - timeout: 硬超时（秒），超时后SIGTERM→SIGKILL，默认300秒
      - idle_timeout: 空闲超时（秒），stdout/stderr无输出超此时长后终止，默认0=禁用
      - stream_output: 是否实时打印输出，默认True
      - max_output_lines: 最大捕获行数，默认5000
      - audit_dir: 审计日志目录，默认 ~/.longhun/audit/
    """

    def __init__(self, timeout: int = 300, idle_timeout: int = 0,
                 stream_output: bool = True, max_output_lines: int = 5000,
                 audit_dir: str = None):
        self.timeout = timeout
        self.idle_timeout = idle_timeout
        self.stream_output = stream_output
        self.max_output_lines = max_output_lines
        self.audit_dir = Path(audit_dir or Path.home() / ".longhun" / "audit")
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        self.guard = ProcessGuard()
        self._active_runs: Dict[str, RunResult] = {}
        self._run_lock = threading.Lock()

    def run(self, command: str, cwd: str = None,
            env: dict = None, label: str = "") -> RunResult:
        """
        执行一条命令，完整生命周期管理。

        返回 RunResult，包含状态、输出、耗时等信息。
        """
        run_id = self._gen_run_id(command)
        result = RunResult(
            run_id=run_id,
            command=command,
            status=RunStatus.PENDING,
            started_at=datetime.now().isoformat()
        )

        # 解析命令
        try:
            cmd_parts = shlex.split(command)
        except ValueError:
            cmd_parts = command.split()
        if not cmd_parts:
            result.status = RunStatus.ERROR
            result.error_message = "空命令"
            return result

        # 处理 python3 script.py 的情况
        if cmd_parts[0].endswith('.py') and not cmd_parts[0].startswith('/'):
            cmd_parts = [sys.executable] + cmd_parts
        elif cmd_parts[0].endswith('.sh'):
            cmd_parts = ['bash'] + cmd_parts

        if label:
            print(f"\n🚀 [{label}] {command}")

        # 启动子进程
        try:
            proc = subprocess.Popen(
                cmd_parts,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=cwd or os.getcwd(),
                env=env or os.environ.copy(),
                preexec_fn=os.setsid if sys.platform != 'win32' else None
            )
        except FileNotFoundError:
            result.status = RunStatus.ERROR
            result.error_message = f"命令不存在: {cmd_parts[0]}"
            result.finished_at = datetime.now().isoformat()
            return result
        except Exception as e:
            result.status = RunStatus.ERROR
            result.error_message = str(e)
            result.finished_at = datetime.now().isoformat()
            return result

        result.pid = proc.pid
        result.status = RunStatus.RUNNING
        self.guard.register(proc.pid, run_id, command)

        with self._run_lock:
            self._active_runs[run_id] = result

        # 流式读取 + 超时监控
        stdout_lines = []
        stderr_lines = []
        last_output_time = time.time()
        start_time = time.time()
        cpu_peak = 0.0
        mem_peak = 0.0
        killed_by_timeout = False
        killed_by_idle = False

        def read_stream(stream, lines_list, is_stderr=False):
            nonlocal last_output_time
            prefix = "  ⚠️ " if is_stderr else "  "
            for line in iter(stream.readline, ''):
                if len(lines_list) < self.max_output_lines:
                    lines_list.append(line)
                last_output_time = time.time()
                if self.stream_output:
                    sys.stdout.write(f"{prefix}{line}")
                    sys.stdout.flush()

        # 启动读取线程
        stdout_thread = threading.Thread(target=read_stream, args=(proc.stdout, stdout_lines))
        stderr_thread = threading.Thread(target=read_stream, args=(proc.stderr, stderr_lines, True))
        stdout_thread.daemon = True
        stderr_thread.daemon = True
        stdout_thread.start()
        stderr_thread.start()

        # 主监控循环
        try:
            while proc.poll() is None:
                elapsed = time.time() - start_time

                # 硬超时检查
                if self.timeout > 0 and elapsed > self.timeout:
                    killed_by_timeout = True
                    self.guard.kill_pid(proc.pid, force=True)
                    break

                # 空闲超时检查
                if self.idle_timeout > 0:
                    idle = time.time() - last_output_time
                    if idle > self.idle_timeout:
                        killed_by_idle = True
                        self.guard.kill_pid(proc.pid, force=True)
                        break

                # 资源采样（每5秒）
                if int(elapsed) % 5 == 0:
                    cpu, mem = self.guard.get_resource(proc.pid)
                    if cpu > cpu_peak:
                        cpu_peak = cpu
                    if mem > mem_peak:
                        mem_peak = mem

                time.sleep(0.5)

            # 等读取线程结束
            stdout_thread.join(timeout=2)
            stderr_thread.join(timeout=2)

        except KeyboardInterrupt:
            print("\n⚠️ 用户中断，正在终止...")
            self.guard.kill_pid(proc.pid, force=True)
            result.status = RunStatus.CRASHED
        except Exception as e:
            result.status = RunStatus.CRASHED
            result.error_message = str(e)
        finally:
            # 确保进程终止
            try:
                if proc.poll() is None:
                    self.guard.kill_pid(proc.pid, force=True)
            except Exception:
                pass

        # 结算
        result.duration = time.time() - start_time
        result.finished_at = datetime.now().isoformat()
        result.exit_code = proc.returncode if proc.returncode is not None else -9
        result.stdout = ''.join(stdout_lines)
        result.stderr = ''.join(stderr_lines)
        result.cpu_peak = cpu_peak
        result.mem_peak = mem_peak
        result.last_activity = datetime.fromtimestamp(last_output_time).isoformat()

        if killed_by_timeout:
            result.status = RunStatus.TIMEOUT
            result.error_message = f"执行超时（>{self.timeout}秒），已强制终止"
        elif killed_by_idle:
            result.status = RunStatus.IDLE_KILL
            result.error_message = f"空闲超时（>{self.idle_timeout}秒无输出），已终止"
        elif result.exit_code == 0:
            result.status = RunStatus.SUCCESS
        else:
            result.status = RunStatus.ERROR
            result.error_message = result.stderr[:500] if result.stderr else f"退出码 {result.exit_code}"

        # 清理
        self.guard.unregister(proc.pid)
        with self._run_lock:
            self._active_runs.pop(run_id, None)

        # 写审计日志
        self._write_audit(result)

        # 报告
        self._print_report(result, label)

        return result

    def _gen_run_id(self, command: str) -> str:
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        h = hashlib.sha256(command.encode()).hexdigest()[:8]
        return f"run-{ts}-{h}"

    def _write_audit(self, result: RunResult):
        """审计日志 """
        try:
            audit_file = self.audit_dir / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
            with open(audit_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(result.to_dict(), ensure_ascii=False) + '\n')
        except Exception:
            pass

    def _print_report(self, result: RunResult, label: str = ""):
        """打印执行报告"""
        emoji_map = {
            RunStatus.SUCCESS: "✅",
            RunStatus.TIMEOUT: "⏰",
            RunStatus.IDLE_KILL: "💤",
            RunStatus.ERROR: "❌",
            RunStatus.CRASHED: "💥",
            RunStatus.REJECTED: "🚫",
        }
        emoji = emoji_map.get(result.status, "❓")
        label_str = f" [{label}]" if label else ""
        print(f"\n{emoji}{label_str} 耗时 {result.duration:.1f}s · "
              f"退出码 {result.exit_code} · {result.status.value}")

        if result.error_message and result.status != RunStatus.SUCCESS:
            print(f"  原因: {result.error_message[:200]}")

        if result.cpu_peak > 0 or result.mem_peak_mb > 0:
            print(f"  CPU峰值 {result.cpu_peak:.1f}% · 内存峰值 {result.mem_peak_mb:.1f}MB")

    def stop_all(self) -> int:
        """停止所有正在运行的脚本"""
        return self.guard.kill_all()

    def list_running(self) -> List[Dict]:
        """列出正在运行的进程"""
        return self.guard.list_processes()


# ============================================================
# 便捷函数
# ============================================================

_default_runner: Optional[ScriptRunner] = None


def get_runner(timeout: int = 300, idle_timeout: int = 0) -> ScriptRunner:
    """获取或创建默认执行器（单例）"""
    global _default_runner
    if _default_runner is None:
        _default_runner = ScriptRunner(timeout=timeout, idle_timeout=idle_timeout)
    return _default_runner


def quick_run(command: str, timeout: int = 300, label: str = "") -> RunResult:
    """快速执行一条命令（一行搞定）"""
    runner = ScriptRunner(timeout=timeout)
    return runner.run(command, label=label)


def stop_running():
    """停止所有正在运行的脚本"""
    global _default_runner
    if _default_runner:
        killed = _default_runner.stop_all()
        print(f"🛑 已终止 {killed} 个进程")
        return killed
    return 0


def ps_list():
    """列出所有运行中的进程"""
    global _default_runner
    if _default_runner:
        procs = _default_runner.list_running()
        if not procs:
            print("  ✅ 没有正在运行的脚本")
        else:
            print(f"  📊 正在运行的脚本 ({len(procs)}):")
            for p in procs:
                print(f"     PID {p['pid']} · {p['command'][:60]} · {p['started_at']}")
        return procs
    return []


# ============================================================
# 命令行入口
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐉 龍魂·脚本生命周期管理器")
    parser.add_argument('command', nargs='?', help='要执行的命令')
    parser.add_argument('--timeout', type=int, default=300, help='超时秒数（默认300）')
    parser.add_argument('--idle-timeout', type=int, default=0, help='空闲超时秒数（默认0=禁用）')
    parser.add_argument('--no-stream', action='store_true', help='不实时输出')
    parser.add_argument('--ps', action='store_true', help='查看运行中的进程')
    parser.add_argument('--kill-all', action='store_true', help='终止所有运行中的进程')
    parser.add_argument('--label', type=str, default='', help='任务标签')

    args = parser.parse_args()

    if args.ps:
        ps_list()
        return

    if args.kill_all:
        stop_running()
        return

    if not args.command:
        parser.print_help()
        return

    runner = ScriptRunner(
        timeout=args.timeout,
        idle_timeout=args.idle_timeout,
        stream_output=not args.no_stream
    )
    result = runner.run(args.command, label=args.label)

    # 返回退出码
    sys.exit(0 if result.is_ok() else 1)


if __name__ == "__main__":
    main()
