#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂插件沙箱 · 启动器 v1.0
DNA: #龍芯⚡️2026-08-22-RUNNER-v1.0
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

每个插件在独立进程运行 · 资源受限(内存/CPU/超时) · 全程审计
"""

import multiprocessing
import resource
import os
from pathlib import Path
from typing import Dict, Any

from .capability_gate import CapabilityGate
from .audit_hook import AuditHook
from .sandbox_api import SandboxAPI
from .plugin_loader import PluginLoader


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
            raise ValueError(f"无法加载插件 {plugin_id} 的清单")

        self.audit_hook = AuditHook()
        self.capability_gate = CapabilityGate(audit_hook=self.audit_hook)
        self.capability_gate.grant(plugin_id, self.manifest.capabilities)
        self.api = SandboxAPI(plugin_id=plugin_id, gate=self.capability_gate,
                              audit_hook=self.audit_hook)

    def _limit_resources(self):
        try:
            resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
        except Exception:
            pass
        try:
            resource.setrlimit(resource.RLIMIT_CPU,
                               (self.manifest.timeout, self.manifest.timeout + 5))
        except Exception:
            pass

    def _run_plugin_in_process(self, queue):
        self._limit_resources()
        os.chdir(self.sandbox_dir)
        self.audit_hook.log(self.plugin_id, "PLUGIN_STARTED",
                            f"Plugin {self.plugin_id} started", "🟢")
        try:
            module, manifest = PluginLoader.load_plugin_module(self.plugin_id)
            entry_func = getattr(module, "main", None) or getattr(module, "run", None)
            if entry_func is None:
                raise ValueError("插件没有 main() 或 run() 入口函数")
            result = entry_func(self.api)
            self.audit_hook.log(self.plugin_id, "PLUGIN_FINISHED",
                                f"Plugin {self.plugin_id} finished", "🟢")
            queue.put({"status": "ok", "result": result, "plugin_id": self.plugin_id})
        except Exception as e:
            error_dna = self.audit_hook.log(self.plugin_id, "PLUGIN_ERROR",
                                            str(e), "🔴")
            queue.put({"status": "error", "error": str(e), "dna": error_dna,
                       "plugin_id": self.plugin_id})

    def execute(self) -> Dict[str, Any]:
        queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=self._run_plugin_in_process, args=(queue,))
        p.start()
        p.join(self.manifest.timeout + 5)
        if p.is_alive():
            p.terminate()
            p.join()
            timeout_dna = self.audit_hook.log(self.plugin_id, "PLUGIN_TIMEOUT",
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
