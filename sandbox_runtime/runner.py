#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂插件沙箱 · 启动器 v1.1
DNA: #龍芯⚡️2026-08-22-RUNNER-v1.1
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

v1.1 安全加固（P77 实测后补丁）：
  1. 子进程零继承：spawn 目标改为模块级函数，只传 plugin_id + queue，
     子进程内全新重建 gate/audit/api，不 pickle 父进程状态。
  2. 进程组收割：子进程 setsid 成为新组长，超时用 killpg 整组 SIGKILL，
     防插件 fork 出的孙进程残留逃逸。
  3. 资源限制补全：内存 + CPU + 打开文件数(256) + 单文件大小(8MB)。
"""

import multiprocessing
import os
import resource
import signal
from pathlib import Path
from typing import Dict, Any

from .capability_gate import CapabilityGate
from .audit_hook import AuditHook
from .sandbox_api import SandboxAPI
from .plugin_loader import PluginLoader

MEM_LIMIT = 512 * 1024 * 1024     # 内存上限 512MB（尽力而为，见 _limit_resources）
FD_LIMIT = 256                    # 打开文件描述符上限
FSIZE_LIMIT = 8 * 1024 * 1024     # 单文件大小上限 8MB
TIMEOUT_BUFFER = 5                # 超时缓冲秒


def _limit_resources(timeout: int) -> None:
    """子进程资源限制（macOS 上 RLIMIT_AS 对 Python 堆为尽力而为 · 诚实标注）"""
    try:
        resource.setrlimit(resource.RLIMIT_AS, (MEM_LIMIT, MEM_LIMIT))
    except Exception:
        pass
    try:
        resource.setrlimit(resource.RLIMIT_CPU,
                           (timeout, timeout + TIMEOUT_BUFFER))
    except Exception:
        pass
    try:
        resource.setrlimit(resource.RLIMIT_NOFILE, (FD_LIMIT, FD_LIMIT))
    except Exception:
        pass
    try:
        resource.setrlimit(resource.RLIMIT_FSIZE, (FSIZE_LIMIT, FSIZE_LIMIT))
    except Exception:
        pass


def _spawn_plugin(plugin_id: str, queue: multiprocessing.Queue) -> None:
    """
    子进程入口（模块级函数 · spawn 兼容 · 零继承父进程状态）
    在子进程内全新重建所有沙箱组件
    """
    # 1. 新会话组长（超时可由父进程 killpg 整组收割）
    try:
        os.setsid()
    except Exception:
        pass

    # 2. 全新构建（不依赖父进程传对象）
    sandbox_root = Path(__file__).resolve().parent.parent
    plugin_path = sandbox_root / "plugins" / plugin_id
    (plugin_path / "sandbox").mkdir(parents=True, exist_ok=True)
    (plugin_path / "logs").mkdir(parents=True, exist_ok=True)

    manifest = PluginLoader.load_manifest(plugin_id)
    if manifest is None:
        queue.put({"status": "error",
                   "error": f"无法加载插件清单: {PluginLoader._last_error}",
                   "plugin_id": plugin_id})
        return

    _limit_resources(manifest.timeout)

    audit_hook = AuditHook()
    capability_gate = CapabilityGate(audit_hook=audit_hook)
    capability_gate.grant(plugin_id, manifest.capabilities)
    api = SandboxAPI(plugin_id=plugin_id, gate=capability_gate,
                     audit_hook=audit_hook)

    os.chdir(plugin_path / "sandbox")
    audit_hook.log(plugin_id, "PLUGIN_STARTED",
                   f"Plugin {plugin_id} started", "🟢")
    try:
        module, _ = PluginLoader.load_plugin_module(plugin_id)
        entry_func = getattr(module, "main", None) or getattr(module, "run", None)
        if entry_func is None:
            raise ValueError("插件没有 main() 或 run() 入口函数")
        result = entry_func(api)
        audit_hook.log(plugin_id, "PLUGIN_FINISHED",
                       f"Plugin {plugin_id} finished", "🟢")
        queue.put({"status": "ok", "result": result, "plugin_id": plugin_id})
    except Exception as e:
        error_dna = audit_hook.log(plugin_id, "PLUGIN_ERROR", str(e), "🔴")
        queue.put({"status": "error", "error": str(e), "dna": error_dna,
                   "plugin_id": plugin_id})


class PluginSandbox:
    """插件沙箱主类 · 每插件独立进程"""

    def __init__(self, plugin_id: str):
        self.plugin_id = plugin_id
        self.plugin_path = Path(__file__).resolve().parent.parent / "plugins" / plugin_id
        self.sandbox_dir = self.plugin_path / "sandbox"
        self.log_dir = self.plugin_path / "logs"
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.manifest = PluginLoader.load_manifest(plugin_id)
        if self.manifest is None:
            raise ValueError(f"无法加载插件 {plugin_id} 的清单: {PluginLoader._last_error}")

        self.audit_hook = AuditHook()

    def execute(self) -> Dict[str, Any]:
        queue = multiprocessing.Queue()
        p = multiprocessing.Process(
            target=_spawn_plugin, args=(self.plugin_id, queue))
        p.start()
        p.join(self.manifest.timeout + TIMEOUT_BUFFER)
        if p.is_alive():
            # 整进程组收割（防插件 fork 的孙进程残留）
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            except PermissionError:
                p.terminate()
            p.join()
            timeout_dna = self.audit_hook.log(
                self.plugin_id, "PLUGIN_TIMEOUT",
                f"Plugin exceeded {self.manifest.timeout}s limit", "🔴")
            return {"status": "timeout",
                    "error": f"插件执行超时 ({self.manifest.timeout}s)",
                    "dna": timeout_dna, "plugin_id": self.plugin_id}
        if not queue.empty():
            return queue.get()
        return {"status": "error", "error": "未知执行错误", "plugin_id": self.plugin_id}


def run_plugin(plugin_id: str) -> Dict[str, Any]:
    sandbox = PluginSandbox(plugin_id)
    return sandbox.execute()


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python3 -m sandbox_runtime.runner <plugin_id>")
        sys.exit(1)
    result = run_plugin(sys.argv[1])
    print("执行结果:", result)
